#!/usr/bin/env python3
"""Save the workflow's review JSON to disk without an agent retyping it. Standard library only.

Workflow scripts have no filesystem access, so the paper-review workflow embeds the review JSON
in an agent prompt between BEGIN_<marker>>>> and <<<END_<marker> and passes its length and
checksum (FNV-1a 32-bit over UTF-16 code units, matching the workflow's fnv1a()).

  find      copy the JSON out of that agent's transcript (~/.claude/projects/**/agent-*.jsonl)
  chunk     check one hand-written part file (fallback path)
  assemble  join the checked parts into review.json (fallback path)

Usage:
  save_review_json.py find --marker M --hash H --length N --out reviews/x/review.json
  save_review_json.py chunk --file reviews/x/.review_parts/000.txt --hash H --length N
  save_review_json.py assemble --dir reviews/x/.review_parts --count K --hash H --length N --out reviews/x/review.json
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path


def fnv1a(s):
    h = 0x811C9DC5
    for u in memoryview(s.encode("utf-16-le")).cast("H"):
        h = ((h ^ u) * 0x01000193) & 0xFFFFFFFF
    return f"{h:08x}"


def utf16_len(s):
    return len(s.encode("utf-16-le")) // 2


def check(text, want_hash, want_len):
    got_len, got_hash = utf16_len(text), fnv1a(text)
    if got_len != want_len or got_hash != want_hash:
        return f"mismatch: length {got_len} (want {want_len}), hash {got_hash} (want {want_hash})"
    return None


def write_review(text, out):
    obj = json.loads(text)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"OK: wrote {out} ({out.stat().st_size} bytes)")


def strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from strings(v)


def cmd_find(a):
    begin, end = f"BEGIN_{a.marker}>>>", f"<<<END_{a.marker}"
    root = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "projects"
    cutoff = time.time() - a.max_age_hours * 3600
    files = [p for p in root.glob("**/agent-*.jsonl") if p.stat().st_mtime >= cutoff]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    problems = []
    for p in files:
        raw = p.read_text(encoding="utf-8", errors="replace")
        if begin not in raw:
            continue
        for line in raw.splitlines():
            if begin not in line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            for s in strings(entry):
                i = s.find(begin)
                j = s.find(end, i + len(begin))
                if i < 0 or j < 0:
                    continue
                text = s[i + len(begin):j]
                err = check(text, a.hash, a.length)
                if err:
                    problems.append(f"{p}: {err}")
                    continue
                write_review(text, a.out)
                return
    msg = f"FAIL: no transcript under {root} holds a verified copy of marker {a.marker}"
    sys.exit("\n".join([msg, *problems]))


def cmd_chunk(a):
    text = Path(a.file).read_text(encoding="utf-8")
    err = check(text, a.hash, a.length)
    if err and text.endswith("\n") and not check(text[:-1], a.hash, a.length):
        Path(a.file).write_text(text[:-1], encoding="utf-8")  # the Write tool may add a final newline
        err = None
    if err:
        sys.exit(f"FAIL: {a.file} {err}")
    print(f"OK: {a.file}")


def cmd_assemble(a):
    d = Path(a.dir)
    text = "".join((d / f"{i:03d}.txt").read_text(encoding="utf-8") for i in range(a.count))
    err = check(text, a.hash, a.length)
    if err:
        sys.exit(f"FAIL: assembled review.json {err}")
    write_review(text, a.out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find")
    f.add_argument("--marker", required=True)
    f.add_argument("--out", required=True)
    f.add_argument("--max-age-hours", type=float, default=24)
    c = sub.add_parser("chunk")
    c.add_argument("--file", required=True)
    s = sub.add_parser("assemble")
    s.add_argument("--dir", required=True)
    s.add_argument("--count", type=int, required=True)
    s.add_argument("--out", required=True)
    for p in (f, c, s):
        p.add_argument("--hash", required=True)
        p.add_argument("--length", type=int, required=True)
    a = ap.parse_args()
    {"find": cmd_find, "chunk": cmd_chunk, "assemble": cmd_assemble}[a.cmd](a)


if __name__ == "__main__":
    main()
