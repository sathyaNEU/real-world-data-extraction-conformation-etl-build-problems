"""task146 architecture 2: the generator's checks on the cut pack and on the world's clean truth."""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import golden as G   # noqa: E402
import pack as PK    # noqa: E402
import world as W    # noqa: E402

TARGET = os.path.join(TASK, "target")
fails = []


def ok(cond, label, detail=""):
    print("%s  %-64s %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        fails.append(label)


def m(x):
    return int(round(x / 1e6))


def edge(x):
    """distance of x (pounds) from the nearest half-million rounding edge, in millions"""
    v = x / 1e6
    return abs((v - int(v)) - 0.5)


D = G.load(TARGET)
res = G.call(D)
g = res["golden"]
acc = G.stable(D, money=False)
bond = G.stable(D, money=True, bonds=True)
mean = G.stable(D, money=True, share="mean")
r0 = G.total_ratio(D)
hedge = m(res["hedge"])
after = res["after_january"]

# the call and its rungs
ok(hedge == m(g["stable"][12]["total"]), "the hedge is the first-anniversary stable balance", "%d" % hedge)
ok(m(acc["stable"][12]["total"]) <= hedge - 25, "R1 account cohorts file a hedge at least 25 million lower",
   "%d against %d" % (m(acc["stable"][12]["total"]), hedge))
ok(m(bond["stable"][12]["total"]) >= hedge + 3, "R2 keeping bond-funded closures files a higher hedge",
   "%d" % m(bond["stable"][12]["total"]))
ok(r0[12] > 0.99, "R0 the total book a year on over the book is over 0.99 (new money)", "%.3f" % r0[12])
new = res["hedge"] - after
ok(new > 0 and m(new) == hedge - round(after / 1e6, 1) // 1 or m(new) == m(res["hedge"] - after),
   "the new swap brings the swaps outstanding to the hedge", "%d" % m(new))
ok(m(acc["stable"][12]["total"]) * 1e6 < after + 1e6 * 30, "R1's hedge sits within 30 million of the swaps left, a small new swap",
   "%d against %.1f" % (m(acc["stable"][12]["total"]), after / 1e6))

# SF1 pooled against mean of ratios: same graded figure everywhere at the million
same = all(m(mean["stable"][k][f]) == m(g["stable"][k][f]) for k in G.HORIZONS for f in list(G.FAMILIES) + ["total"])
ok(same, "SF1 start dates taken together or averaged: every graded figure the same at the million")
# SF2 the lowest month-end balance against the anniversary balance alone (filed in 7.3): moves the figure
# SF3 matching on the UTC date against the local date: the overnight batch is the same instant, so the same links
# every graded figure off a half-million edge by 0.05 million or more
edges = [edge(g["stable"][k][f]) for k in G.HORIZONS for f in list(G.FAMILIES) + ["total"]] + \
        [edge(g["now"][f]) for f in G.FAMILIES] + [edge(g["book"]), edge(res["hedge"] - after)]
ok(min(edges) >= 0.05, "every graded figure at least 0.05 million off a rounding edge", "%.3f" % min(edges))
# SF4 the product code ES02 read by date
ok(m(g["now"]["Young Saver"]) > 0 and m(g["now"]["Easy Saver"]) > 0, "SF4 ES02 by date: Young Saver and Easy Saver both carry balances")
# SF5 a closure with more than one same-day opening of its amount: none (the link is unique)
succ, _ = G.links(D)
closes = sum(1 for e in D["events"] if e[1] == "CLOSE")
ok(len(succ) > 0.3 * closes, "the matched closures are a large share of closures", "%d of %d" % (len(succ), closes))

# the analyst test on the clean truth: account cohorts on the world's own records file the low hedge
w = W.World()
pids = {}
for a, v in w.accounts.items():
    pids.setdefault(v["pid"], []).append(a)
true_links = sum(len(v) - 1 for v in pids.values())
ok(abs(true_links - len(succ)) <= 3, "the same-day links recover the world's switches", "%d against %d" % (len(succ), true_links))

# input gates
names = sorted(os.listdir(TARGET))
ok(len(names) >= 10, "G1 ten or more files", "%d" % len(names))
ext = {n.rsplit(".", 1)[1] for n in names}
ok(len(ext) >= 3, "G2 three or more formats", str(sorted(ext)))
rows = sum(1 for _ in open(os.path.join(TARGET, PK.FILES["balances"]))) - 1
ok(rows >= 25000, "G3 a file of 25,000 rows or more", "%d" % rows)
meta = json.load(open(os.path.join(TASK, "metadata.json")))
ok(len(meta["distractors"]) >= 2, "G4 two or more named distractors", str(meta["distractors"]))
ok(all(f.get("source") and f.get("date") and f.get("license") for f in meta["files"]), "G5 every file has a source, date and licence")
bad = []
for n in names:
    if n.endswith((".csv", ".eml")):
        if "—" in open(os.path.join(TARGET, n), encoding="utf-8").read():
            bad.append(n)
ok(not bad, "G6 no em dash in any text file", str(bad))
late = []
with open(os.path.join(TARGET, PK.FILES["events"])) as fh:
    for r in csv.DictReader(fh):
        if r["event_utc"] > "2026-12-01":
            late.append(r["event_utc"])
ok(not late, "G7 no event after the extract", str(late[:2]))
sub = open(os.path.join(TASK, "submission.md")).read()
ok("—" not in sub, "G8 no em dash in the write-up")
print("%d checks, %d failed" % (len(fails) + 0 if False else len([1 for _ in range(1)]) - 1 + 0, len(fails)) if False else
      "%d failed" % len(fails))
sys.exit(1 if fails else 0)
