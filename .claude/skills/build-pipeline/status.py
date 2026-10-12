#!/usr/bin/env python3
"""status.py: the build board, read from each build's own pipeline.json. Nothing here is committed.

    python3 .claude/skills/build-pipeline/status.py                 every build in a lane block, by lane
    python3 .claude/skills/build-pipeline/status.py --owner HANDLE  one developer's lane
    python3 .claude/skills/build-pipeline/status.py --all           every task folder, legacy builds included
    python3 .claude/skills/build-pipeline/status.py next HANDLE     the lowest open number in that lane
    python3 .claude/skills/build-pipeline/status.py taskNN          the seed for a number: header and Situation only

Status is pipeline.json's `status` field (drawing, design, build, shipped, returned, paused, retired). Older
files without it are read from `stage` and `stage_name`. Lanes and owners come from the root START_HERE.md.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
START = os.path.join(REPO, "START_HERE.md")
CARDS = os.path.join(REPO, ".claude", "skills", "fingerprint", "cards")


def lanes():
    out = []
    for line in open(START, encoding="utf-8"):
        m = re.match(r"\| ([^|]+) \| task(\d+) to task(\d+) \| \d+ \| ([^|]+) \|", line)
        if m:
            out.append((m.group(1).strip(), int(m.group(2)), int(m.group(3)), m.group(4).strip()))
    return out


def lane_of(n, ls):
    for obj, lo, hi, owner in ls:
        if lo <= n <= hi:
            return obj, owner
    return "", ""


def infer(p):
    if p.get("status"):
        return p["status"]
    st, name = str(p.get("stage", "")).lower(), str(p.get("stage_name", "")).lower()
    if "retired" in (st, name) or name.startswith("retired"):
        return "retired"
    if st == "paused" or name.startswith("paused") or ", paused" in name or "paused " in name:
        return "paused"
    if "returned" in name:
        return "returned"
    if name.startswith("shipped") or name.startswith("delivered") or st in ("delivered", "shipped"):
        return "shipped"
    if st in ("1", "draw"):
        return "drawing"
    if st in ("2", "design"):
        return "design"
    return "build"


def builds():
    out = []
    for d in os.listdir(REPO):
        m = re.fullmatch(r"task(\d+)", d)
        if not m or not os.path.isdir(os.path.join(REPO, d)):
            continue
        p = os.path.join(REPO, d, "pipeline.json")
        data = {}
        if os.path.exists(p):
            try:
                data = json.load(open(p))
            except ValueError:
                data = {"status": "unreadable"}
        out.append((int(m.group(1)), d, data, os.path.exists(p)))
    return sorted(out)


def board(owner=None, show_all=False):
    ls = lanes()
    rows = []
    for n, t, p, has in builds():
        obj, own = lane_of(n, ls)
        if not show_all and not obj and not has:
            continue
        if owner and own != owner:
            continue
        st = infer(p) if has else "legacy"
        rows.append((obj or "outside the lanes", own, t, st, str(p.get("stage_name", ""))[:70], p.get("updated", "")))
    cur = None
    for obj, own, t, st, name, upd in rows:
        if obj != cur:
            print("\n%s (%s)" % (obj, own or "-"))
            cur = obj
        print("  %-8s %-9s %-10s %s" % (t, st, upd, name))
    counts = {}
    for r in rows:
        counts[r[3]] = counts.get(r[3], 0) + 1
    print("\n" + ", ".join("%d %s" % (v, k) for k, v in sorted(counts.items())))


def next_open(owner):
    taken = {n for n, *_ in builds()} | {int(re.sub(r"\D", "", f)) for f in os.listdir(CARDS) if re.fullmatch(r"task\d+\.json", f)}
    for obj, lo, hi, own in lanes():
        if own == owner:
            for n in range(lo, hi + 1):
                if n not in taken:
                    print("task%d (%s)" % (n, obj))
                    return 0
            print("lane %s is fully taken" % obj)
            return 1
    print("no lane for %s in START_HERE.md" % owner)
    return 1


def seed(t):
    row = None
    for line in open(START, encoding="utf-8"):
        if line.startswith("| %s |" % t):
            row = line
            break
    if not row:
        print("%s has no seed in START_HERE.md" % t)
        return 1
    m = re.search(r"\]\(([^)]+)\)", row)
    path = os.path.join(REPO, m.group(1))
    text = open(path, encoding="utf-8").read()
    out, sec = [], 0
    for line in text.splitlines():
        if re.match(r"#{2,3} ", line):
            sec += 1
            low = line.lower()
            if sec > 1 and "situation" not in low and len("\n".join(out)) > 400:
                break
        out.append(line)
    print(row.strip())
    print("seed: %s\n" % m.group(1))
    print("\n".join(out).strip())
    print("\n(The rest of the seed is decoy-era design and is not read: re-find the pitfall from the data.)")
    return 0


def main(argv):
    if len(argv) > 1 and re.fullmatch(r"task\d+", argv[1]):
        return seed(argv[1])
    if len(argv) > 2 and argv[1] == "next":
        return next_open(argv[2])
    owner = argv[argv.index("--owner") + 1] if "--owner" in argv else None
    board(owner, "--all" in argv)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
