#!/usr/bin/env python3
"""task196 pair ceiling, on supplemental-stumping Part 0's weights (38 / 7 / 55).

    python3 task196/generator/ceiling.py [--pack]

Two responses are scored from DIFFERENT readings, never one reading counted twice:

  cracker  lands the main call (Castlegate at 30.0 cases per million payments), so it banks the
           recommendation band and the whole construction layer, which is the twelve-member bridge
           from each member's recorded case count to its estimated true count. It ran the hygiene
           battery, executed every filed rule the pack points at and reconciled every control, so
           every ask figure a column description or an unmatched join resolves is free to it. Its ask
           row must read 0 of N on the device figures.
  mirror   stops at rung 2: it finds the registration-lag spike from the two date columns, excludes
           mule registrations dated after its own case opened, and files 37.3. It misses the call and
           the construction layer's estimated-incidence column, keeps the recorded-count column, and
           is held off the device figures by the same devices plus the documented mess it does not
           chase.

Stage 2 runs on the designed stops (paper). Stage 3 re-runs with --pack, which reads the ask ladder
values recomputed from the cut bundle (generator/ask_stops.json) and fails if any cracker row hits.
"""
import json
import os
import sys

W_REC, W_INSTR, W_ASK = 38.0, 7.0, 55.0   # Part 0's weights; the gate reads a ceiling computed on these
R_WRONG_CALL = 5.0                        # recommendation weight a wrong call still keeps

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# The ask layer. owner "construction" is the decisive construction's output on a segment the trustees
# want anyway (supplemental 2.2): the cracker has it by design, so it is sized, not defended.
# owner "device" figures each sit on rows outside the main call's declared population and carry the
# primary device named in the design note's ask sheet.
# ---------------------------------------------------------------------------
ASKS = [
    # id, ask, figures, owner, cracker hit, mirror hit
    ("C1", "construction", "the index for each of the four review-group members", 4, "construction", True, False),
    ("C3", "construction", "the named member's bridge, one line per reconciling item", 3, "construction", True, True),
    ("C4", "construction", "the chart's named parts", 6, "construction", True, True),
    ("A",  "ask A", "indemnity paid on the unauthorised-fraud class, 4 quarters x 3 member tiers plus quarter totals", 16, "device", False, False),
    ("B",  "ask B", "cases notified in the quarter to 30 June 2027 and those closed by it, per member", 24, "device", False, False),
    ("C",  "ask C", "recovery share by route and quarter on cases closed in 2025/26, plus route totals", 15, "device", False, False),
]
# The mirror is credited with every construction figure it could plausibly keep, which flatters the
# pair's second column rather than the first: C3's opening line is the recorded case count, and three of
# the chart's six parts (the recorded series, its ordering and the highlighted member) survive a wrong
# estimate. C3 and C4 are therefore marked kept for the mirror in full.
# CUT, and the cut is recorded because it is a ceiling lever and a correctness check at once
# (supplemental-stumping Part 6): a per-member recorded case count for 2026/27, twelve figures, was
# graded in the first sizing. It is a group-by on one file that every strong response banks, it was the
# only construction figure the mirror also kept, and it put the measured pair at 41.6. The recorded
# count now appears once, as the opening line of the named member's bridge, where the mirror keeps it
# and nothing else. The twelve-member table still ships, carrying the recorded column as context the
# write-up does not grade.
# MIRROR NOTE: C3 is marked kept for the mirror because the bridge's opening line is the recorded
# count, which a response stopping at rung 2 has right; its other two lines and every C1 figure are
# wrong under the date-only correction, which files 37.3 against the golden 30.0.



def score(rows, keep_construction=None):
    """Return (cracker ask share, mirror ask share, N). keep_construction overrides how many of the
    construction layer's figures are graded, for the sweep."""
    n = 0
    hit_c = hit_m = 0
    for _id, _ask, _what, figs, owner, c_hit, m_hit in rows:
        f = figs
        if owner == "construction" and keep_construction is not None:
            f = keep_construction.get(_id, figs)
        n += f
        if c_hit:
            hit_c += f
        if m_hit:
            hit_m += f
    return hit_c / n, hit_m / n, n, hit_c, hit_m


def pair(lc, ls):
    c = W_REC + W_INSTR + W_ASK * lc
    s = R_WRONG_CALL + W_INSTR + W_ASK * ls
    return c, s, (c + s) / 2.0


def main():
    rows = ASKS
    if "--pack" in sys.argv:
        p = os.path.join(HERE, "ask_stops.json")
        if not os.path.exists(p):
            print("no generator/ask_stops.json: run the generator first", file=sys.stderr)
            return 2
        stops = json.load(open(p))
        rows = [(r[0], r[1], r[2], r[3], r[4],
                 bool(stops[r[0]]["cracker_hits"]), bool(stops[r[0]]["mirror_hits"])) for r in ASKS]

    lc, ls, n, hc, hm = score(rows)
    c, s, avg = pair(lc, ls)
    print("task196 pair ceiling, weights %.0f recommendation / %.0f instruction / %.0f asks" % (W_REC, W_INSTR, W_ASK))
    print()
    print("%-9s %-54s %5s %-12s %-8s %-8s" % ("id", "figures", "n", "owner", "cracker", "mirror"))
    for _id, _ask, what, figs, owner, c_hit, m_hit in rows:
        print("%-9s %-54s %5d %-12s %-8s %-8s" % (_id, what[:54], figs, owner,
                                                  "keeps" if c_hit else "miss", "keeps" if m_hit else "miss"))
    print()
    print("ask criteria N                 %d" % n)
    dev_total = sum(r[3] for r in rows if r[4] == "device")
    dev_c = sum(r[3] for r in rows if r[4] == "device" and r[5])
    dev_m = sum(r[3] for r in rows if r[4] == "device" and r[6])
    con_total = sum(r[3] for r in rows if r[4] == "construction")
    print("ask criteria behind each row   %d construction + %d device" % (con_total, dev_total))
    print("cracker keeps                  %d of %d  (%.3f of ask weight)   device figures kept %d of %d"
          % (hc, n, lc, dev_c, dev_total))
    print("mirror keeps                   %d of %d  (%.3f of ask weight)   device figures kept %d of %d"
          % (hm, n, ls, dev_m, dev_total))
    print("cracker score                  %.1f" % c)
    print("mirror score                   %.1f" % s)
    print("PAIR CEILING                   %.1f   (gate: 40.0 or under)" % avg)
    print("mirror leakage                 %.1f per cent of ask weight   (gate: under 35)" % (100.0 * ls))
    print()
    print("sweep: the two sizing decisions, against the pair")
    print("%-46s %5s %7s %7s %8s %7s" % ("construction layer", "N", "Lc", "Ls", "cracker", "pair"))
    for label, n_index, recorded_col in (
            ("all twelve members indexed, recorded column graded", 12, True),
            ("all twelve members indexed", 12, False),
            ("review group of four indexed, recorded column graded", 4, True),
            ("review group of four indexed (shipped)", 4, False),
            ("review group of four, no chart criteria", 4, None)):
        trial = [r for r in rows if r[4] == "device"]
        trial.append(("C1", "construction", "index per indexed member", n_index, "construction", True, False))
        trial.append(("C3", "construction", "the named member's bridge items", 3, "construction", True, True))
        if recorded_col is not None:
            trial.append(("C4", "construction", "the chart's named parts", 6, "construction", True, True))
        if recorded_col:
            trial.append(("C2", "construction", "recorded case count per member (cut)", 12, "construction", True, True))
        lc2, ls2, n2, _, _ = score(trial)
        c2, s2, avg2 = pair(lc2, ls2)
        print("%-46s %5d %7.3f %7.3f %8.1f %7.1f" % (label[:46], n2, lc2, ls2, c2, avg2))
    print()
    bad = [r[0] for r in rows if r[4] == "device" and r[5]]
    if bad:
        print("FAIL cracker keeps device figures: %s" % ", ".join(bad))
        return 1
    if avg > 40.0:
        print("FAIL pair ceiling over 40")
        return 1
    if 100.0 * ls >= 35.0:
        print("FAIL mirror leakage 35 or over")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
