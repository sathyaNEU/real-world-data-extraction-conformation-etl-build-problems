#!/usr/bin/env python3
"""status.py: the board, read from every build's pipeline.json, the backlog waves in each author file and the
portal record in the shipped ledger. Nothing here writes a file.

    python3 .claude/skills/build-pipeline/status.py                every developer's waves, each task with its status
    python3 .claude/skills/build-pipeline/status.py --owner HANDLE one developer's waves, one task per line
    python3 .claude/skills/build-pipeline/status.py --all          every task folder with its status, then the portal record
    python3 .claude/skills/build-pipeline/status.py next HANDLE    the next task to start, from the earliest wave
    python3 .claude/skills/build-pipeline/status.py wave HANDLE    the next six open numbers in the lane, as a wave row
    python3 .claude/skills/build-pipeline/status.py taskNN         the seed for a number: header and Situation only

Status (pipeline.json `status`, exact strings): DRAWING, DESIGN, BUILD, SHIPPED (submitted, pending review),
SHIPPED_APPROVED (shown as SHIPPED & APPROVED), RETURNED, FAILED_TO_STUMP (back in a backlog wave), PAUSED,
RETIRED. A number with no folder is OPEN, unless the portal record says otherwise. Older files without a
`status` are read from `stage` and `stage_name`.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
START = os.path.join(REPO, "START_HERE.md")
CARDS = os.path.join(REPO, ".claude", "skills", "fingerprint", "cards")
AUTHORS = os.path.join(REPO, ".claude", "authors")
LEDGER = os.path.join(REPO, ".claude", "skills", "stumping", "references", "shipped-ledger.md")

DONE = {"SHIPPED", "SHIPPED_APPROVED"}
IN_FLIGHT = {"DRAWING", "DESIGN", "BUILD", "RETURNED", "PAUSED"}
SHOW = {"SHIPPED_APPROVED": "SHIPPED & APPROVED"}
LEGACY = {"drawing": "DRAWING", "design": "DESIGN", "build": "BUILD", "shipped": "SHIPPED", "returned": "RETURNED",
          "paused": "PAUSED", "retired": "RETIRED", "approved": "SHIPPED_APPROVED", "failed_to_stump": "FAILED_TO_STUMP"}


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


def portal_record():
    rec, on = {}, False
    if not os.path.exists(LEDGER):
        return rec
    for line in open(LEDGER, encoding="utf-8"):
        if line.startswith("## "):
            on = line.strip() == "## Portal record"
            continue
        m = re.match(r"\| (task\d+) \| ([^|]+) \| ([A-Z_]+) \| ([^|]*) \|", line) if on else None
        if m:
            rec[m.group(1)] = (m.group(2).strip(), m.group(3), m.group(4).strip())
    return rec


def infer(p):
    st = p.get("status")
    if st:
        return LEGACY.get(str(st).lower(), str(st).upper())
    stage, name = str(p.get("stage", "")).lower(), str(p.get("stage_name", "")).lower()
    if "retired" in (stage, name) or name.startswith("retired"):
        return "RETIRED"
    if stage == "paused" or name.startswith("paused") or ", paused" in name or "paused " in name:
        return "PAUSED"
    if "returned" in name:
        return "RETURNED"
    if name.startswith("shipped") or name.startswith("delivered") or stage in ("delivered", "shipped"):
        return "SHIPPED"
    if stage in ("1", "draw"):
        return "DRAWING"
    if stage in ("2", "design"):
        return "DESIGN"
    return "BUILD"


def pipeline(t):
    p = os.path.join(REPO, t, "pipeline.json")
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p))
    except ValueError:
        return {"status": "UNREADABLE"}


def status_of(t, rec):
    p = pipeline(t)
    if p is not None:
        return infer(p)
    if t in rec:
        return "SHIPPED_APPROVED" if rec[t][1] == "APPROVED" else "SHIPPED"
    return "OPEN"


def authors():
    out = {}
    if not os.path.isdir(AUTHORS):
        return out
    for f in sorted(os.listdir(AUTHORS)):
        if f.endswith(".md"):
            out[f[:-3]] = os.path.join(AUTHORS, f)
    return out


def waves(handle):
    """[(wave number, [(task, note)])] from the author file's `## Backlog` table."""
    path = authors().get(handle)
    out, on = [], False
    if not path:
        return out
    for line in open(path, encoding="utf-8"):
        if line.startswith("## "):
            on = line.strip() == "## Backlog"
            continue
        m = re.match(r"\| (\d+) \| (.+) \|\s*$", line) if on else None
        if m:
            items = [(t, (note or "").strip()) for t, note in re.findall(r"(task\d+)(?:\s*\(([^)]*)\))?", m.group(2))]
            out.append((int(m.group(1)), items))
    return out


def show(st):
    return SHOW.get(st, st)


def board(owner=None):
    rec = portal_record()
    ls = lanes()
    for h in authors():
        if owner and h != owner:
            continue
        lane = next(((obj, lo, hi) for obj, lo, hi, o in ls if o == h), None)
        print("%s%s" % (h, ("  " + "%s, task%d to task%d" % lane) if lane else ""))
        ws = waves(h)
        if not ws:
            print("  no backlog waves")
        for n, items in ws:
            sts = [status_of(t, rec) for t, _ in items]
            done = sum(1 for s in sts if s in DONE)
            if owner:
                print("  wave %d (%d of %d shipped)" % (n, done, len(items)))
                for (t, note), s in zip(items, sts):
                    print("    %-8s %-19s %s" % (t, show(s), note))
            else:
                print("  wave %d (%d of %d shipped): %s" % (n, done, len(items),
                      " · ".join("%s %s" % (t, show(s)) for (t, _), s in zip(items, sts))))
        print()
    if not owner:
        a = sum(1 for v in rec.values() if v[1] == "APPROVED")
        print("portal record: %d approved, %d pending review" % (a, len(rec) - a))


def board_all():
    rec = portal_record()
    ls = lanes()
    rows = []
    for d in os.listdir(REPO):
        m = re.fullmatch(r"task(\d+)", d)
        if m and os.path.isdir(os.path.join(REPO, d)):
            n = int(m.group(1))
            p = pipeline(d) or {}
            rows.append((n, d, status_of(d, rec), str(p.get("stage_name", ""))[:60], p.get("owner", "") or lane_of(n, ls)[1]))
    for n, t, st, name, own in sorted(rows):
        print("  %-8s %-19s %-11s %s" % (t, show(st), own or "-", name))
    print("\nportal record (no folder needed):")
    for t, (pid, st, dt) in sorted(rec.items(), key=lambda x: int(x[0][4:])):
        print("  %-8s %-15s %-6s %s" % (t, st, dt, pid))


def taken():
    nums = set()
    for d in os.listdir(REPO):
        m = re.fullmatch(r"task(\d+)(?:_ext)?", d)
        if m:
            nums.add(int(m.group(1)))
    for f in os.listdir(CARDS):
        m = re.fullmatch(r"task(\d+)\.json", f)
        if m:
            nums.add(int(m.group(1)))
    for h in authors():
        for _, items in waves(h):
            nums.update(int(t[4:]) for t, _ in items)
    return nums


def ten_ten(t):
    """What a rework still owes the client's 10/10 rules before it is resumed (empty when it owes nothing)."""
    card_p = os.path.join(CARDS, t + ".json")
    if not os.path.exists(card_p) or not os.path.isdir(os.path.join(REPO, t)):
        return ""
    owed = []
    try:
        card = json.load(open(card_p))
    except ValueError:
        card = {}
    if card.get("stump_class") != "analytical":
        owed.append("card stump_class is %s, not analytical" % (card.get("stump_class") or "missing"))
    for f in ("analyst_test", "domain_test"):
        if not card.get(f):
            owed.append("card has no %s" % f)
    if card.get("official_decoy") or card.get("validated_decoy"):
        owed.append("card is flagged as an official or validated decoy")
    note = os.path.join(REPO, t, "DESIGN_NOTE.md")
    text = open(note, encoding="utf-8").read() if os.path.exists(note) else ""
    if not re.search(r"^#+\s*Three rules", text, re.M):
        owed.append("the design note has no ## Three rules")
    return "; ".join(owed)


def next_task(handle):
    rec = portal_record()
    ws = waves(handle)
    flying = []
    for n, items in ws:
        for t, note in items:
            st = status_of(t, rec)
            if st in DONE:
                continue
            if st in IN_FLIGHT:
                flying.append("%s %s" % (t, st))
                continue
            print("next: %s (wave %d, %s%s)" % (t, n, show(st), ", " + note if note else ""))
            gate = ten_ten(t)
            if gate:
                print("10/10 gate before any resume: %s. Answer it, or re-root if the old stump is a decoy, a withheld"
                      " rule, a field reading or an executed procedure." % gate)
            if flying:
                print("in flight: " + ", ".join(flying))
            return 0
    if flying:
        print("in flight: " + ", ".join(flying))
    print("every wave is started or shipped: cut the next one with `status.py wave %s` and add it to the backlog" % handle)
    return 1


def next_wave(handle):
    lane = next(((lo, hi) for obj, lo, hi, o in lanes() if o == handle), None)
    if not lane:
        print("no lane for %s in START_HERE.md" % handle)
        return 1
    used = taken()
    free = [n for n in range(lane[0], lane[1] + 1) if n not in used][:6]
    if not free:
        print("the lane is fully taken")
        return 1
    k = max([n for n, _ in waves(handle)] or [0]) + 1
    print("| %d | %s |" % (k, " · ".join("task%d (new)" % n for n in free)))
    return 0


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
    keep = ("objective", "domain", "mirrors", "decision shape", "committed call", "client domain", "field")
    out, sec = [], 0
    for line in text.splitlines():
        if re.match(r"#{2,3} ", line):
            sec += 1
            if sec > 1 and "situation" not in line.lower() and len("\n".join(out)) > 400:
                break
        cell = re.match(r"\|\s*([^|]+?)\s*\|", line)
        if cell and sec <= 1 and not line.startswith("|---") and cell.group(1).lower() not in keep:
            continue  # decoy-era mechanism rows (gap, pattern, Gate G, traps, calibration, driving force) are not shown
        out.append(line)
    print(row.strip())
    print("seed: %s\n" % m.group(1))
    print("\n".join(out).strip())
    print("\n(The seed's mechanism rows and the rest of the note are decoy-era design and are not shown: keep the world,"
          " the decision and the quantity, and find the pitfall from the data under the 10/10 rules.)")
    return 0


def main(argv):
    if len(argv) > 1 and re.fullmatch(r"task\d+", argv[1]):
        return seed(argv[1])
    if len(argv) > 2 and argv[1] == "next":
        return next_task(argv[2])
    if len(argv) > 2 and argv[1] == "wave":
        return next_wave(argv[2])
    if "--all" in argv:
        board_all()
        return 0
    board(argv[argv.index("--owner") + 1] if "--owner" in argv else None)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
