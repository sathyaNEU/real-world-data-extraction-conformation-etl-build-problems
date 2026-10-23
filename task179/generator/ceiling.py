"""task179 ask layer against the careful solver's routes, on the cut pack.

    python3 task179/generator/ceiling.py [target]

Every route a careful reader takes on the teaching-groups ask, figure by figure, against figures.json, the two stage 4
round 1 readers' verbatim paths among them (reader A: "classes of different papers sharing identical room/day/time
slots in every meeting merged ... summed"; reader B: "pairs of classes with identical meeting sets (same days, times,
rooms, weeks) ... merged and sizes summed"). The cracker lands the call and runs the hygiene battery, which includes
reading a repeated total on several lines once; the mirror is the best response off the call. Pair ceiling on the
generated rubric's weights (38 recommendation and components, 7 instruction following, 55 asks; a wrong call keeps
about 5)."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc     # noqa: E402

SLOT = ("Room", "Day", "Start", "Teaching Weeks")
ROUTES = {
    "one group per class code": (None, "sum"),
    "reader A: identical room, day, start in every meeting, summed": (("Room", "Day", "Start"), "sum"),
    "reader B: identical meeting sets with weeks, summed": (SLOT, "sum"),
    "identical meeting sets, a repeated enrolment read once (the battery)": (SLOT, "equal_once"),
    "identical meeting sets, the largest class only": (SLOT, "once"),
    "room, day, start, teacher, summed": (("Room", "Day", "Start", "Teacher"), "sum"),
    "room, day, start, weeks, teacher, repeated enrolment once": (SLOT + ("Teacher",), "equal_once"),
    "room, day, start, no weeks, the golden size rule": (("Room", "Day", "Start"), "golden"),
}


def route(d, cols, rule):
    cls = calc.slot_groups(d["tt"], cols)
    if rule == "equal_once":
        gs = []
        for gid, g in cls.groupby("grp"):
            ns = list(g["n"])
            size = ns[0] if len(set(ns)) == 1 else sum(ns)
            lv = int(g["level"].min())
            gs.append((g["fac"].iloc[0], "200" if lv == 200 else ("300+" if lv >= 300 else "100"), size, 1))
    else:
        gs = calc.group_sizes(cls, rule)
    out = {}
    for f, code in calc.FAC_ARC.items():
        for lev, tag in (("200", "200"), ("300+", "300up")):
            sz = [x[2] for x in gs if x[0] == f and x[1] == lev]
            out["ask_groups_s1_2026_%s_%s_30orfewer" % (code.lower(), tag)] = sum(1 for v in sz if v <= 30)
            out["ask_groups_s1_2026_%s_%s_over30" % (code.lower(), tag)] = sum(1 for v in sz if v > 30)
    return out


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    asks = sorted(k for k in figs if k.startswith("ask_"))
    d = calc.load(target)
    gold = route(d, SLOT, "golden")
    assert all(gold[k] == figs[k] for k in asks), "golden route does not reproduce figures.json"
    print("%-72s %s" % ("route", "figures kept"))
    best = 0
    for name, (cols, rule) in ROUTES.items():
        r = route(d, cols, rule)
        hit = [k for k in asks if r[k] == figs[k]]
        best = max(best, len(hit))
        print("%-72s %d of %d%s" % (name, len(hit), len(asks), (": " + ", ".join(hit)) if hit else ""))
    L = best / float(len(asks))
    crack = 38 + 7 + 55 * L
    mirror = 5 + 7 + 55 * L
    print("asks %d; worst route keeps %d; cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f"
          % (len(asks), best, crack, mirror, (crack + mirror) / 2, 100 * L))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
