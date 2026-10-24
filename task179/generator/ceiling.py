"""task179 ask layer against the careful solver's routes, on the cut pack.

    python3 task179/generator/ceiling.py [target]

Every route a careful reader takes on the teaching-groups ask, figure by figure, against figures.json. Two devices sit
under every cell. Grouping: papers carried from SIRIUS that share only their lecture are three groups (the lecture and
each workshop), which joining classes through any shared meeting, or merging identical meeting sets, does not give.
Size: a group's size is its students enrolled at the census, while ARC Scheduling's figure and the class lists also
count places still held by students on approved leave and by students who left before the census. The portal's
responses on the first pack ran the shared-meeting join with a repeated figure read once where the room could not
seat it added (the route labelled "portal"): it kept all 20 cells there. The cracker lands the call and runs the
hygiene battery; the mirror is the best response off the call. Pair ceiling on the generated rubric's weights (38
recommendation and components, 7 instruction following, 55 asks; a wrong call keeps about 5)."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc     # noqa: E402

ROUTES = {
    "portal: shared meetings joined, a repeated figure over the room once": ("uf", "tt_golden"),
    "shared meetings joined, figures added": ("uf", "tt_sum"),
    "identical meeting sets, repeated figure once": ("ident", "tt_golden"),
    "identical meeting sets, figures added": ("ident", "tt_sum"),
    "one group per class code, its figure": ("class", "tt_sum"),
    "each meeting its own group, figures": ("meeting", "tt_golden"),
    "grouping right, the timetable's figures": ("sets", "tt_golden"),
    "grouping right, every listed student": ("sets", "lists"),
    "grouping right, students on leave left in": ("sets", "keep_leave"),
    "grouping right, students who left kept": ("sets", "keep_left"),
    "shared meetings joined, enrolled students": ("uf", "enrolled"),
    "identical meeting sets, enrolled students": ("ident", "enrolled"),
    "shared meetings joined, every listed student": ("uf", "lists"),
    "identical meeting sets, every listed student": ("ident", "lists"),
}


def keyed(out):
    r = {}
    for (code, lev), (a, b) in out.items():
        tag = "200" if lev == "200" else "300up"
        r["ask_groups_s1_2026_%s_%s_30orfewer" % (code.lower(), tag)] = a
        r["ask_groups_s1_2026_%s_%s_over30" % (code.lower(), tag)] = b
    return r


def route(d, how, basis):
    out, _ = calc.teaching_groups(d, how, basis)
    return keyed(out)


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    asks = sorted(k for k in figs if k.startswith("ask_"))
    d = calc.load(target)
    gold = route(d, "sets", "enrolled")
    assert all(gold[k] == figs[k] for k in asks), "golden route does not reproduce figures.json"
    print("%-72s %s" % ("route", "figures kept"))
    best = 0
    for name, (how, basis) in ROUTES.items():
        r = route(d, how, basis)
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
