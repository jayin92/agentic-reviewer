#!/usr/bin/env python3
"""Resolve bibliography entries without an LLM in the loop. Standard library only.

Input:  JSON list of {key, title, authors?, year?, venue?, arxiv_id?, doi?}
Output: --out gets the full records (incl. abstracts); stdout (and --summary) get a
        compact {"resolved": [...]} without abstracts, for the workflow to consume.

Semantic Scholar often throttles keyed clients far below its nominal 1 request/second,
so per-title S2 lookups are the last resort:
  1. OpenAlex title search (fast; set OPENALEX_API_KEY, free) finds a DOI / arXiv id for entries that lack one.
  2. One S2 batch call fetches S2 ids, abstracts and PDF links for every entry with an id.
  3. Only entries neither source matched go to S2 title match, until --deadline.
An entry OpenAlex matched still counts as found when S2 is unavailable (abstract from OpenAlex).
Duplicate titles (e.g. a supplementary bibliography repeating the main one) are looked up once.
"""

import argparse
import difflib
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

S2 = "https://api.semanticscholar.org"
OA = "https://api.openalex.org"
FIELDS = "paperId,externalIds,title,year,authors,venue,abstract,openAccessPdf"
OA_FIELDS = "id,doi,title,publication_year,authorships,primary_location,locations,open_access,abstract_inverted_index"
KEY = os.environ.get("S2_API_KEY", "")
OA_KEY = os.environ.get(
    "OPENALEX_API_KEY", ""
)  # without one, OpenAlex allows only a small shared daily budget
GAP = {"s2": 1.05, "oa": 0.12}  # seconds between calls per service
_last = {"s2": 0.0, "oa": 0.0}
DEADLINE = [float("inf")]  # wall-clock cutoff; set from --deadline
ERR = (
    object()
)  # sentinel: request failed after retries (distinct from a 404 "no match")


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def sim(a, b):
    a, b = norm(a), norm(b)
    return difflib.SequenceMatcher(None, a, b).ratio() if a and b else 0.0


def norm_arxiv(x):
    x = re.sub(r"^arxiv:", "", str(x or "").strip(), flags=re.I)
    return re.sub(r"v\d+$", "", x)


def norm_doi(x):
    """'https://doi.org/10.1/x', 'doi:10.1/x' and '10.1/x' all become '10.1/x'."""
    x = re.sub(
        r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", str(x or "").strip(), flags=re.I
    )
    return x.rstrip(".") or None


# Major venues by canonical name. Only two DIFFERENT known venues count as a mismatch, so preprint
# servers, workshops and unknown venues are never flagged.
VENUES = {
    "CVPR": r"\bcvpr\b|computer vision and pattern recognition",
    "ICCV": r"\biccv\b|international conference on computer vision",
    "ECCV": r"\beccv\b|european conference on computer vision",
    "NeurIPS": r"\bneurips\b|\bnips\b|neural information processing systems",
    "ICML": r"\bicml\b|international conference on machine learning",
    "ICLR": r"\biclr\b|international conference on learning representations",
    "AAAI": r"\baaai\b",
    "WACV": r"\bwacv\b|winter conference on applications of computer vision",
    "TPAMI": r"\bt?pami\b|pattern analysis and machine intelligence",
    "IJCV": r"\bijcv\b|international journal of computer vision",
    "SIGGRAPH/TOG": r"\bsiggraph\b|transactions on graphics|\btog\b",
    "ACM MM": r"\bacm ?mm\b|acm multimedia|international conference on multimedia",
}


def venue_of(v):
    v = norm(v)
    if not v or "workshop" in v or re.search(r"\b(cvprw|iccvw|eccvw)\b", v):
        return None
    return next((name for name, pat in VENUES.items() if re.search(pat, v)), None)


def call(svc, url, body=None, tries=6, until=None):
    """GET/POST with per-service pacing and backoff on 429/5xx.
    Stops at `until` (or the global deadline, whichever is earlier).
    Returns parsed JSON, None on 404, ERR if it gave up or ran out of time."""
    limit = min(DEADLINE[0], until or float("inf"))
    data = json.dumps(body).encode() if body is not None else None
    headers = {"User-Agent": "paper-review-resolver"}
    if data:
        headers["Content-Type"] = "application/json"
    if svc == "s2" and KEY:
        headers["x-api-key"] = KEY
    if svc == "oa" and OA_KEY:
        headers["Authorization"] = "Bearer " + OA_KEY
    for attempt in range(tries):
        wait = GAP[svc] - (time.time() - _last[svc])
        if wait > 0:
            time.sleep(wait)
        if time.time() > limit:
            break
        _last[svc] = time.time()
        retry_in = 3
        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code != 429 and e.code < 500:
                print(f"HTTP {e.code} for {url[:110]}", file=sys.stderr)
                return None
            retry_in = min(3 * 2**attempt, 40)  # 3, 6, 12, 24, 40 s
        # Network failures, including ones while reading the body, and non-JSON replies.
        except (OSError, http.client.HTTPException, ValueError) as e:
            print(f"request failed ({e!r}) for {url[:110]}", file=sys.stderr)
        if attempt == tries - 1 or time.time() + retry_in > limit:
            break
        time.sleep(retry_in)
    print(f"giving up on {url[:110]}", file=sys.stderr)
    return ERR


def year_of(y):
    m = re.search(r"(19|20)\d\d", str(y or ""))
    return int(m.group()) if m else None


def judge(entry, rec, via_id):
    """Return (accept, mismatch_note) for a database record against a bib entry."""
    s = sim(entry.get("title"), rec.get("title"))
    by, ry = year_of(entry.get("year")), year_of(rec.get("year"))
    dy = abs(by - ry) if by and ry else 0
    if via_id:
        if s < 0.6:
            return False, None  # printed id points elsewhere; fall back to title match
    # A near-exact title with a wrong year is kept and flagged below.
    elif s < 0.9 or (dy > 2 and s < 0.97):
        return False, None
    notes = []
    if via_id and s < 0.9:
        notes.append(
            f'title differs: bib "{entry.get("title")}" vs database "{rec.get("title")}"'
        )
    # Off-by-one years are usually arXiv-vs-proceedings, not an error worth flagging.
    if dy >= 2:
        notes.append(f"year: bib {by} vs database {ry}")
    bv, rv = venue_of(entry.get("venue")), venue_of(rec.get("venue"))
    if bv and rv and bv != rv:
        notes.append(
            f'venue: bib "{entry.get("venue")}" vs database "{rec.get("venue")}"'
        )
    # First-author check: any name token of the bib's first author must appear somewhere in the
    # record's author list. Token overlap tolerates reversed (e.g. CJK) name order and initials.
    db_tokens = {
        t for a in rec.get("authors") or [] for t in norm(a.get("name")).split()
    }
    first = re.split(r",| and |;", entry.get("authors") or "")[0]
    bib_tokens = [
        t for t in norm(first).split() if len(t) > 1 and t not in ("et", "al")
    ]
    # Organisation authors ("Team Wan", "Gemini Team", "MiniMax") are listed by member names in databases.
    is_org = "team" in bib_tokens or len(norm(entry.get("authors")).split()) == 1
    if (
        db_tokens
        and bib_tokens
        and not is_org
        and not any(t in db_tokens for t in bib_tokens)
    ):
        notes.append(f'first author "{first.strip()}" not among database authors')
    return True, "; ".join(notes) or None


def from_openalex(w):
    """Map an OpenAlex work onto the S2 record shape used everywhere else."""
    doi = norm_doi(w.get("doi"))
    arxiv = None
    for loc in w.get("locations") or []:
        m = re.search(
            r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})",
            loc.get("landing_page_url") or "",
        )
        if m:
            arxiv = m.group(1)
            break
    if not arxiv and doi:
        m = re.match(r"10\.48550/arxiv\.(\d{4}\.\d{4,5})", doi, flags=re.I)
        arxiv = m.group(1) if m else None
    inv = w.get("abstract_inverted_index") or {}
    pos = sorted((i, word) for word, idx in inv.items() for i in idx)
    return {
        "paperId": None,
        "externalIds": {"DOI": doi, "ArXiv": arxiv},
        "title": w.get("title"),
        "year": w.get("publication_year"),
        "authors": [
            {"name": (a.get("author") or {}).get("display_name")}
            for a in w.get("authorships") or []
        ],
        "venue": ((w.get("primary_location") or {}).get("source") or {}).get(
            "display_name"
        ),
        "abstract": " ".join(word for _, word in pos) or None,
        "openAccessPdf": {"url": (w.get("open_access") or {}).get("oa_url")},
        "_source": "OpenAlex",
    }


def openalex_match(entry, until):
    """Returns (record, note), None for no match, or ERR if the request failed."""
    q = urllib.parse.quote(re.sub(r"[,:;|?!]", " ", entry["title"])[:300])
    res = call(
        "oa",
        f"{OA}/works?search={q}&per-page=5&select={OA_FIELDS}",
        tries=3,
        until=until,
    )
    if res is ERR:
        return ERR
    if not res:
        return None
    best = max(
        res.get("results") or [],
        key=lambda w: sim(w.get("title"), entry["title"]),
        default=None,
    )
    if not best:
        return None
    rec = from_openalex(best)
    ok, note = judge(entry, rec, via_id=False)
    return (rec, note) if ok else None


def compact(entry, rec, note):
    if not rec:
        return {"key": entry["key"], "found": False}
    ext = rec.get("externalIds") or {}
    out = {
        "key": entry["key"],
        "found": True,
        "s2_id": rec.get("paperId"),
        "arxiv_id": ext.get("ArXiv"),
        "doi": ext.get("DOI"),
        "pdf_url": (rec.get("openAccessPdf") or {}).get("url") or None,
        "has_abstract": bool(rec.get("abstract")),
        "mismatch_note": note,
        "source": rec.get("_source", "Semantic Scholar"),
    }
    return {k: v for k, v in out.items() if v is not None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--summary", help="also write the compact stdout JSON here")
    ap.add_argument(
        "--deadline",
        type=float,
        default=480,
        help="seconds; stop looking up after this and report the rest as not found (keeps under a 600 s tool timeout)",
    )
    a = ap.parse_args()
    entries = json.load(open(a.inp))
    DEADLINE[0] = time.time() + a.deadline
    t0 = time.time()
    by_key = {e["key"]: e for e in entries}
    recs = {}  # key -> (record, note)
    stats = {"openalex": 0, "s2_batch": 0, "s2_title": 0}

    errors = 0

    def lookup():
        nonlocal errors
        # 1. Ids: printed ones, else from an OpenAlex title match (once per distinct title).
        #    OpenAlex gets at most half the time budget and is dropped after repeated failures,
        #    so a throttled OpenAlex cannot starve the S2 batch call that follows.
        oa_until = t0 + 0.5 * (DEADLINE[0] - t0)
        oa_fails = 0
        id_of, oa, oa_cache = {}, {}, {}
        for e in entries:
            doi = norm_doi(e.get("doi"))
            if e.get("arxiv_id"):
                id_of[e["key"]] = "ARXIV:" + norm_arxiv(e["arxiv_id"])
            elif doi:
                id_of[e["key"]] = "DOI:" + doi
            elif norm(e.get("title")) and oa_fails < 5 and time.time() < oa_until:
                t = norm(e["title"])
                if t not in oa_cache:
                    hit = openalex_match(e, oa_until)
                    oa_fails = oa_fails + 1 if hit is ERR else 0
                    if oa_fails == 5:
                        print("OpenAlex keeps failing; skipping it for the remaining titles", file=sys.stderr)
                    oa_cache[t] = None if hit is ERR else hit
                hit = oa_cache[t]
                if hit:
                    oa[e["key"]] = hit
                    ext = hit[0]["externalIds"]
                    if ext.get("ArXiv"):
                        id_of[e["key"]] = "ARXIV:" + ext["ArXiv"]
                    elif ext.get("DOI"):
                        id_of[e["key"]] = "DOI:" + ext["DOI"]
        stats["openalex"] = len(oa)
        print(
            f"OpenAlex matched {stats['openalex']} titles ({time.time() - t0:.0f}s)",
            file=sys.stderr,
        )

        # 2. One S2 batch call per 500 ids. Keep the OpenAlex record when S2 is unavailable.
        keys = list(id_of)
        for i in range(0, len(keys), 500):
            part = keys[i : i + 500]
            res = call(
                "s2",
                f"{S2}/graph/v1/paper/batch?fields={FIELDS}",
                {"ids": [id_of[k] for k in part]},
            )
            if res is ERR or not isinstance(res, list):
                print(
                    "S2 batch call failed; using OpenAlex records where available",
                    file=sys.stderr,
                )
                res = []
            for k, rec in zip(part, res):
                if rec:
                    ok, note = judge(by_key[k], rec, via_id=True)
                    if ok:
                        if not rec.get("abstract") and oa.get(k):
                            rec["abstract"] = oa[k][0]["abstract"]
                        recs[k] = (rec, note)
                        stats["s2_batch"] += 1
        for k, hit in oa.items():
            if hit and k not in recs:
                recs[k] = hit

        # 3. S2 title match for whatever is left, until the deadline.
        cache = {}
        todo = [e for e in entries if e["key"] not in recs and norm(e.get("title"))]
        print(f"{len(todo)} entries left for S2 title match", file=sys.stderr)
        for e in todo:
            t = norm(e["title"])
            if t not in cache:
                res = call(
                    "s2",
                    f"{S2}/graph/v1/paper/search/match?query={urllib.parse.quote(e['title'][:300])}&fields={FIELDS}",
                )
                cache[t] = ERR if res is ERR else ((res or {}).get("data") or [None])[0]
            rec = cache[t]
            if rec is ERR:
                errors += 1
            elif rec:
                ok, note = judge(e, rec, via_id=False)
                if ok:
                    recs[e["key"]] = (rec, note)
                    stats["s2_title"] += 1

    try:
        lookup()
    except Exception as ex:  # never lose the lookups done so far
        print(f"lookup stopped early: {ex!r}", file=sys.stderr)

    full, short = [], []
    for e in entries:
        rec, note = recs.get(e["key"], (None, None))
        short.append(compact(e, rec, note))
        row = {**short[-1]}
        if rec:
            row.update(
                title=rec.get("title"),
                year=str(rec.get("year") or ""),
                venue=rec.get("venue"),
                authors=[x.get("name") for x in rec.get("authors") or []],
                abstract=rec.get("abstract"),
                source=rec.get("_source", "Semantic Scholar"),
            )
        else:
            row.update(title=e.get("title"), year=e.get("year"))
        full.append(row)

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    json.dump(full, open(a.out, "w"), indent=1, ensure_ascii=False)
    found = sum(1 for s in short if s["found"])
    if errors:
        print(
            f"WARNING: {errors} S2 title lookups failed (rate limit / network / deadline); reported as not found",
            file=sys.stderr,
        )
    print(
        f"resolved {found}/{len(entries)} in {time.time() - t0:.0f}s "
        f"(S2 batch {stats['s2_batch']}, OpenAlex only {found - stats['s2_batch'] - stats['s2_title']}, "
        f"S2 title {stats['s2_title']}) -> {a.out}",
        file=sys.stderr,
    )
    if a.summary:
        json.dump({"resolved": short}, open(a.summary, "w"), ensure_ascii=False)
    json.dump({"resolved": short}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
