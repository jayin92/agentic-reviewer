#!/usr/bin/env python3
"""Resolve bibliography entries without an LLM in the loop. Standard library only.

Input:  JSON list of {key, title, authors?, year?, venue?, arxiv_id?, doi?}
Output: --out gets the full records (incl. abstracts); --summary (stdout if not given) gets a
        compact {"resolved": [...], "warnings": [...]} without abstracts, for the workflow to consume.

Semantic Scholar often throttles keyed clients far below its nominal 1 request/second,
so per-title S2 lookups are the last resort:
  1. OpenAlex title search (fast; set OPENALEX_API_KEY, free) finds a DOI / arXiv id for entries that lack one.
  2. One S2 batch call fetches S2 ids, abstracts and PDF links for every entry with an id.
     Printed ids S2 cannot resolve (call failed, unknown id, another paper) get the OpenAlex search too.
  3. Only entries neither source matched go to S2 title match, until --deadline or 3 failures in a row.
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
import unicodedata
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
# Sentinel: a request failed after retries (distinct from a 404 "no match").
ERR = object()
WARNINGS = []  # problems the workflow should log; written to the --summary JSON


def warn(msg):
    if msg not in WARNINGS:
        WARNINGS.append(msg)
        print("WARNING: " + msg, file=sys.stderr)


_FOLD = str.maketrans({"ł": "l", "ø": "o", "đ": "d", "æ": "ae", "œ": "oe", "ı": "i"})


def norm(s):
    """Lowercase words in any script with accents folded ("Pérez" -> "perez", "Nießner" ->
    "niessner"), so names match databases that spell them without diacritics."""
    s = unicodedata.normalize("NFKD", (s or "").casefold().translate(_FOLD))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[\W_]+", " ", s).strip()


def sim(a, b):
    a, b = norm(a), norm(b)
    return difflib.SequenceMatcher(None, a, b).ratio() if a and b else 0.0


def norm_arxiv(x):
    """'arXiv:2106.09685v2', 'https://arxiv.org/abs/2106.09685' -> '2106.09685'; None if no id is in it."""
    s = str(x or "")
    m = re.search(r"(?<!\d)(\d{4}\.\d{4,5})(?:v\d+)?(?!\d)", s) or re.search(
        r"\b([a-z][a-z-]*(?:\.[a-z]{2})?/\d{7})(?:v\d+)?\b", s, flags=re.I
    )
    return m.group(1) if m else None


def norm_doi(x):
    """'https://doi.org/10.1109/x', 'doi:10.1109/x' and '10.1109/x' all become '10.1109/x'; None if not a DOI."""
    x = re.sub(
        r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", str(x or "").strip(), flags=re.I
    )
    x = x.rstrip(".")
    return x if re.match(r"10\.\d{4,9}/\S+$", x) else None


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
    Returns parsed JSON; None on 404 and other 4xx ("no match"); ERR if it gave up, ran out of
    time, or was refused (401/403: a bad or expired key, which retrying cannot fix)."""
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
            if e.code in (401, 403):
                name, key = {
                    "s2": ("Semantic Scholar", "S2_API_KEY"),
                    "oa": ("OpenAlex", "OPENALEX_API_KEY"),
                }[svc]
                warn(f"{name} refused requests with HTTP {e.code}; check {key}")
                return ERR
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
    # Titles that differ only in a number are usually different works ("Qwen2" vs "Qwen3").
    nums_differ = re.findall(r"\d+", norm(entry.get("title"))) != re.findall(
        r"\d+", norm(rec.get("title"))
    )
    if via_id:
        if s < 0.6:
            return False, None  # printed id points elsewhere; fall back to title match
    # A near-exact title with a wrong year is kept and flagged below.
    elif s < 0.9 or nums_differ or (dy > 2 and s < 0.97):
        return False, None
    notes = []
    if via_id and (s < 0.9 or nums_differ):
        notes.append(
            f'title differs: bib "{entry.get("title")}" vs database "{rec.get("title")}"'
        )
    # Off-by-one years are usually arXiv-vs-proceedings, not an error worth flagging. So is a later
    # bib year when the database year is just the arXiv posting year (arXiv 2015, journal 2017).
    ax = (rec.get("externalIds") or {}).get("ArXiv") or ""
    ax_year = 2000 + int(ax[:2]) if re.match(r"\d{4}\.\d", ax) else None
    if dy >= 2 and not (by > ry and ry == ax_year):
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
    # Latin-script tokens only: a name in another script can't be compared with a romanized one.
    bib_tokens = [
        t
        for t in norm(first).split()
        if len(t) > 1 and t.isascii() and t not in ("et", "al")
    ]
    # Organisation authors ("Team Wan", "Gemini Team", "MiniMax", "DeepSeek-AI") are listed by member
    # names in databases: one name, no "et al.", against a record with many authors.
    authors = entry.get("authors") or ""
    is_org = (
        "team" in bib_tokens
        or len(norm(authors).split()) == 1
        or (
            len(re.split(r",| and |;", authors)) == 1
            and not re.search(r"\bet al\b", authors, flags=re.I)
            and len(rec.get("authors") or []) > 3
        )
    )
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
    # open_access.oa_url is often a landing page; the workflow downloads pdf_url and reads it as a PDF.
    pdf = next(
        (
            loc["pdf_url"]
            for loc in w.get("locations") or []
            if loc.get("is_oa") and loc.get("pdf_url")
        ),
        None,
    )
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
        "openAccessPdf": {"url": pdf},
        "_source": "OpenAlex",
    }


def openalex_search(title, until):
    """OpenAlex works for a title search, in the S2 record shape, or ERR if the request failed.
    Not judged here: entries that share a title can differ in year and authors."""
    q = urllib.parse.quote(re.sub(r"[,:;|?!]", " ", title)[:300])
    res = call(
        "oa",
        f"{OA}/works?search={q}&per-page=5&select={OA_FIELDS}",
        tries=3,
        until=until,
    )
    if res is ERR:
        return ERR
    return [from_openalex(w) for w in (res or {}).get("results") or []]


def best_match(entry, recs):
    """(record, note) for the closest-titled record judge() accepts, preferring one with no
    mismatch note; None if it accepts none. Different works can share a title ("Deep Learning").
    """
    best = None
    for rec in sorted(recs, key=lambda r: -sim(r.get("title"), entry.get("title"))):
        ok, note = judge(entry, rec, via_id=False)
        if ok and not note:
            return rec, note
        if ok and best is None:
            best = (rec, note)
    return best


def compact(entry, rec, note, printed_arxiv=None):
    """The workflow's view of one entry. arxiv_id falls back to the printed id (when it was not
    shown to belong to another paper), so the workflow can take arxiv_id from here as is.
    """
    if not rec:
        return {"key": entry["key"], "found": False}
    ext = rec.get("externalIds") or {}
    pdf_url = (rec.get("openAccessPdf") or {}).get("url") or None
    # S2 sometimes omits the ArXiv external id even when its open-access PDF is on arXiv.
    m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", pdf_url or "")
    out = {
        "key": entry["key"],
        "found": True,
        "s2_id": rec.get("paperId"),
        "arxiv_id": ext.get("ArXiv") or (m and m.group(1)) or printed_arxiv,
        "doi": ext.get("DOI"),
        "pdf_url": pdf_url,
        "has_abstract": bool(rec.get("abstract")),
        "mismatch_note": note,
        "source": rec.get("_source", "Semantic Scholar"),
    }
    return {k: v for k, v in out.items() if v is not None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument(
        "--summary", help="write the compact JSON here instead of to stdout"
    )
    ap.add_argument(
        "--deadline",
        type=float,
        default=480,
        help="seconds; stop looking up after this and report the rest as not found (keeps under a 600 s tool timeout)",
    )
    a = ap.parse_args()
    with open(a.inp, encoding="utf-8") as f:
        entries = json.load(f)
    DEADLINE[0] = time.time() + a.deadline
    t0 = time.time()
    by_key = {e["key"]: e for e in entries}
    recs = {}  # key -> (record, note)
    # key -> note, when S2 shows that a printed id belongs to a different paper
    wrong_id = {}
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
        oa_wrong_id = set()  # OpenAlex matches whose id S2 shows to be another paper's

        def oa_match(e):
            """(record, note) from an OpenAlex title search, or None. Each distinct title is
            searched once; every entry is judged on its own (duplicates share results, not verdicts).
            """
            nonlocal oa_fails
            t = norm(e.get("title"))
            if t and t not in oa_cache and oa_fails < 5 and time.time() < oa_until:
                res = openalex_search(e["title"], oa_until)
                oa_fails = oa_fails + 1 if res is ERR else 0
                if oa_fails == 5:
                    warn("OpenAlex kept failing; skipped it for the remaining titles")
                oa_cache[t] = [] if res is ERR else res
            return best_match(e, oa_cache.get(t) or [])

        for e in entries:
            # Printed ids are LLM-extracted and can be junk ("N/A", a URL); use them only if valid.
            ax, doi = norm_arxiv(e.get("arxiv_id")), norm_doi(e.get("doi"))
            if ax:
                id_of[e["key"]] = "ARXIV:" + ax
            elif doi:
                id_of[e["key"]] = "DOI:" + doi
            else:
                hit = oa_match(e)
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
                warn(
                    "Semantic Scholar batch call failed; used OpenAlex where it matched"
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
                    elif k in oa:
                        # The id OpenAlex gave belongs to another paper on S2: don't pass that
                        # match on with a wrong arXiv id / DOI; S2 title match decides instead.
                        del oa[k]
                        oa_wrong_id.add(k)
                    else:  # a printed id; the entry falls back to title search
                        wrong_id[k] = (
                            f'printed id {id_of[k]} is a different paper ("{rec.get("title")}")'
                        )
        for k, hit in oa.items():
            if k not in recs:
                recs[k] = hit
        # Printed ids S2 did not resolve (batch failed, or no record for that id) get the
        # OpenAlex fallback too, before the slow S2 title match.
        for e in entries:
            k = e["key"]
            if k in id_of and k not in recs and k not in oa_wrong_id:
                hit = oa_match(e)
                if hit:
                    recs[e["key"]] = hit

        # 3. S2 title match for whatever is left, until the deadline or 3 failed titles in a row
        #    (fewer retries per title than the batch call: a throttled S2 must not eat the budget).
        cache, s2_fails = {}, 0
        todo = [e for e in entries if e["key"] not in recs and norm(e.get("title"))]
        print(f"{len(todo)} entries left for S2 title match", file=sys.stderr)
        for e in todo:
            t = norm(e["title"])
            if t not in cache:
                if s2_fails >= 3 or time.time() > DEADLINE[0]:
                    continue  # still let duplicates of titles already looked up through
                res = call(
                    "s2",
                    f"{S2}/graph/v1/paper/search/match?query={urllib.parse.quote(e['title'][:300])}&fields={FIELDS}",
                    tries=4,
                )
                s2_fails = s2_fails + 1 if res is ERR else 0
                errors += res is ERR
                cache[t] = (
                    None if res is ERR else ((res or {}).get("data") or [None])[0]
                )
            rec = cache[t]
            if rec:
                ok, note = judge(e, rec, via_id=False)
                if ok:
                    recs[e["key"]] = (rec, note)
                    stats["s2_title"] += 1
        errors += len({norm(e["title"]) for e in todo} - set(cache))  # never tried

    try:
        lookup()
    except Exception as ex:  # never lose the lookups done so far
        warn(f"lookup stopped early: {ex!r}")

    full, short = [], []
    for e in entries:
        rec, note = recs.get(e["key"], (None, None))
        if rec and e["key"] in wrong_id:
            note = "; ".join(filter(None, [wrong_id[e["key"]], note]))
        printed = None if e["key"] in wrong_id else norm_arxiv(e.get("arxiv_id"))
        short.append(compact(e, rec, note, printed))
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
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(full, f, indent=1, ensure_ascii=False)
    found = sum(1 for s in short if s["found"])
    if errors:
        warn(
            f"{errors} Semantic Scholar title lookups failed or were skipped "
            "(rate limit / network / deadline); reported as not found"
        )
    print(
        f"resolved {found}/{len(entries)} in {time.time() - t0:.0f}s "
        f"(S2 batch {stats['s2_batch']}, OpenAlex only {found - stats['s2_batch'] - stats['s2_title']}, "
        f"S2 title {stats['s2_title']}) -> {a.out}",
        file=sys.stderr,
    )
    summary = {"resolved": short, "warnings": WARNINGS}
    if a.summary:
        with open(a.summary, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False)
    else:
        json.dump(summary, sys.stdout)


if __name__ == "__main__":
    main()
