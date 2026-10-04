#!/usr/bin/env python3
"""Render reviews/<paper>/review.json into review.md, review_form.txt, cited_work.md,
uncited_work.md and report.html. Standard library only.

Usage: python3 scripts/render_review.py reviews/<paper>
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "report.html"

CATEGORIES = [
    ("competing_or_concurrent", "Competing or concurrent work"),
    ("missing_baseline", "Missing baselines"),
    ("should_cite_prior_work", "Prior work to cite"),
    ("related_technique", "Related techniques"),
]


def label(s):
    return str(s or "").replace("_", " ")


def link(title, url):
    return f"[{title}]({url})" if url else str(title)


def render_md(r):
    out = []
    add = out.append
    venue = r.get("venue")
    add(f"# Review: {r['paper']['title']}")
    add("")
    add(f"Venue: {venue['name']} {venue['year']}" if venue else "Venue: none given")
    add(f"Generated {date.today().isoformat()} by {r.get('generated_by', '')}")
    add("")

    flags = (r.get("integrity") or {}).get("injection_flags") or []
    if flags:
        add("## ⚠ Integrity note")
        add("The PDF contains hidden or reviewer-directed text. All agents ignored it.")
        for f in flags:
            add(f"- {f['location']} ({f['how_hidden']}): \"{f['text']}\"")
        add("")

    add("## Overview")
    add(r.get("overview", ""))
    add("")
    add("## Summary")
    add(r.get("summary", ""))
    add("")

    if r.get("strengths"):
        add("## Strengths")
        for s in r["strengths"]:
            loc = f" ({s['location']})" if s.get("location") else ""
            add(f"- {s['point']}{loc}")
        add("")

    for sev, heading in (("major", "Major weaknesses"), ("minor", "Minor issues")):
        items = [w for w in r.get("weaknesses", []) if w.get("severity") == sev]
        if not items:
            continue
        add(f"## {heading}")
        for w in items:
            status = " *(partially valid)*" if w.get("status") == "partially_valid" else ""
            raised = ", ".join(w.get("raised_by") or [])
            add(f"### {w['id']}. {w['title']}{status}")
            add(f"*{label(w.get('category'))} · {w.get('location', '')} · raised by {raised}*")
            add("")
            add(w.get("detail", ""))
            add("")
            add(f"**How to fix:** {w.get('suggestion', '')}")
            add("")

    nov = r.get("novelty") or {}
    if nov.get("verdicts") or nov.get("discussion"):
        add("## Novelty")
        if nov.get("verdicts"):
            add("| Contribution | Verdict | Closest prior work | Evidence |")
            add("|---|---|---|---|")
            for v in nov["verdicts"]:
                cells = [v.get("contribution", ""), label(v.get("verdict")), v.get("closest_work", ""), v.get("evidence", "")]
                add("| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " ") for c in cells) + " |")
            add("")
        if nov.get("discussion"):
            add(nov["discussion"])
            add("")

    cw = r.get("cited_work") or {}
    issues = [i for i in cw.get("issues", []) if (i.get("verification") or {}).get("verdict") != "refuted"]
    add("## Use of cited work")
    if issues:
        for i in issues:
            v = i.get("verification") or {}
            add(f"- **{label(i['kind'])}** {i['key']} {i.get('title', '')}: {i['claim']}")
            add(f"  - Verification ({label(v.get('verdict'))}): {v.get('evidence', '')}")
    else:
        add("No citation-accuracy or baseline-number issues survived verification.")
    add("")

    probs = cw.get("reference_problems") or []
    if probs:
        add("## Reference-list problems")
        for p in probs:
            status = "could not verify" if p.get("status") == "could_not_verify" else label(p.get("status"))
            note = f" ({p['note']})" if p.get("note") else ""
            src = f"; checked {p['source']}" if p.get("source") else ""
            add(f"- {p['key']} \"{p.get('title', '')}\": {status}{note}{src}")
        add("")
        add("\"Could not verify\" is not proof a reference is wrong. Books, theses and reports are often unindexed.")
        add("")

    uncited = r.get("uncited_work") or []
    if uncited:
        add("## Missing related work")
        for key, heading in CATEGORIES:
            items = [u for u in uncited if u.get("category") == key]
            if not items:
                continue
            add(f"**{heading}**")
            for u in items:
                add(f"- [{u['ref']}] {link(u['title'], u.get('url'))} ({u.get('year') or 'n/a'}): {u.get('relation', '')}")
            add("")

    if r.get("questions"):
        add("## Questions for the authors")
        for n, q in enumerate(r["questions"], 1):
            add(f"{n}. {q}")
        add("")

    if r.get("revision_plan"):
        add("## Revision plan")
        for p in r["revision_plan"]:
            addr = f" (addresses {', '.join(p['addresses'])})" if p.get("addresses") else ""
            add(f"- [ ] **{p.get('priority', '')}**: {p['step']}{addr}")
        add("")

    add("## Scores")
    if venue and r.get("venue_form"):
        types = {f["name"]: f.get("type") for f in venue.get("form_fields", [])}
        scored = [f for f in r["venue_form"] if types.get(f["field"], "text") != "text"]
        if scored:
            add(f"**{venue['name']} {venue['year']} form (uncalibrated AI estimate):**")
            add("")
            add("| Field | Value |")
            add("|---|---|")
            for f in scored:
                add(f"| {f['field']} | {f['value']} |")
            add("")
            add("The full form is in `review_form.txt`.")
            add("")
    add("| Dimension (1-5) | Median |")
    add("|---|---|")
    for d in (r.get("scores") or {}).get("dimensions", []):
        add(f"| {d['label']} | {d['median'] if d.get('median') is not None else 'n/a'} |")
    add("")
    add("*AI-generated review. It may contain errors.*")
    add("")

    dropped = r.get("dropped_criticisms") or []
    if dropped:
        add("## Appendix A: criticisms removed by fact-checking")
        for d in dropped:
            add(f"- ({d.get('persona')}, {d.get('location', '')}) {d['point']}")
            add(f"  - {label(d.get('verdict'))}: {d.get('evidence', '')}")
        add("")
    return "\n".join(out)


def render_form(r):
    venue = r.get("venue")
    if not venue or not r.get("venue_form"):
        return None
    lines = [
        f"{venue['name']} {venue['year']} review form: {r['paper']['title']}",
        "AI-generated; scores are an uncalibrated estimate. Check everything before using it.",
        "=" * 72,
        "",
    ]
    for f in r["venue_form"]:
        lines += [f"{f['field']}:", str(f["value"]).strip(), ""]
    return "\n".join(lines)


def render_cited(r):
    cw = r.get("cited_work") or {}
    reads = {x["key"]: x for x in cw.get("reads", [])}
    flags = {}
    for f in cw.get("light_flags", []):
        flags.setdefault(f["key"], []).append(f)
    probs = {p["key"]: p for p in cw.get("reference_problems", [])}
    refs = sorted(cw.get("references", []), key=lambda x: (not x.get("core"), x.get("key", "")))
    out = [f"# Cited work: {r['paper']['title']}", ""]
    for ref in refs:
        k = ref["key"]
        out.append(f"## {k} {link(ref['title'], ref.get('url'))} ({ref.get('year') or 'n/a'})")
        status = "verified" if ref.get("verified") else "not verified"
        if k in probs:
            status = label(probs[k].get("status")) + (f": {probs[k]['note']}" if probs[k].get("note") else "")
        out.append(f"Role: {label(ref.get('role'))} · {status} · {'core (read in full)' if ref.get('core') else 'abstract-level check'}")
        x = reads.get(k)
        if x:
            out += [
                "",
                x.get("summary", ""),
                "",
                f"- Citation accuracy: **{label(x['citation_accuracy']['verdict'])}**: {x['citation_accuracy']['detail']}",
                f"- Baseline numbers: **{label(x['baseline_numbers']['verdict'])}**: {x['baseline_numbers']['detail']}",
                f"- Novelty overlap: **{label(x['novelty_overlap']['level'])}**: {x['novelty_overlap']['detail']}",
            ]
        for f in flags.get(k, []):
            out.append(f"- Abstract-level flag ({f['severity']}): {f['issue']}")
        out.append("")
    return "\n".join(out)


def render_uncited(r):
    out = [f"# Related work not cited by: {r['paper']['title']}", ""]
    for key, heading in CATEGORIES:
        items = [u for u in r.get("uncited_work", []) if u.get("category") == key]
        if not items:
            continue
        out += [f"## {heading}", ""]
        for u in items:
            out.append(f"### [{u['ref']}] {link(u['title'], u.get('url'))}")
            out.append(f"{u.get('authors') or 'n/a'} · {u.get('year') or 'n/a'} · relevance {u.get('relevance')}/5 · found via {u.get('found_via') or 'search'}")
            out += ["", f"**Relation:** {u.get('relation', '')}", "", u.get("summary", ""), ""]
    return "\n".join(out)


def page_title(title):
    short = re.split(r"[:—–?]", title)[0].strip()
    words = short.split()
    if len(words) > 5:
        short = " ".join(words[:4])
    return f"{short} review"


def render_html(r):
    tpl = TEMPLATE.read_text(encoding="utf-8")
    data = json.dumps(r, ensure_ascii=False).replace("</", "<\\/")
    title = page_title(r["paper"]["title"]).replace("&", "&amp;").replace("<", "&lt;")
    return tpl.replace("__PAGE_TITLE__", title).replace("__REVIEW_JSON__", data)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out_dir = Path(sys.argv[1])
    r = json.loads((out_dir / "review.json").read_text(encoding="utf-8"))
    written = []

    def write(name, text):
        if text is None:
            return
        (out_dir / name).write_text(text, encoding="utf-8")
        written.append(str(out_dir / name))

    write("review.md", render_md(r))
    write("review_form.txt", render_form(r))
    write("cited_work.md", render_cited(r))
    write("uncited_work.md", render_uncited(r))
    write("report.html", render_html(r))
    print("Wrote:\n  " + "\n  ".join(written))


if __name__ == "__main__":
    main()
