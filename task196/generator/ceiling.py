#!/usr/bin/env python3
"""task196 pair ceiling, on supplemental-stumping Part 0's weights (38 / 7 / 55).

    python3 task196/generator/ceiling.py [--pack]
    python3 task196/generator/ceiling.py --forcing

Two responses are scored from DIFFERENT readings, never one reading counted twice:

  cracker  lands the main call (Castlegate at 31 cases per million payments, 30.940), so it banks the
           recommendation band and the whole construction layer, which is the twelve-member bridge
           from each member's recorded case count to its estimated true count. It ran the hygiene
           battery, executed every filed rule the pack points at and reconciled every control, so
           every ask figure a column description or an unmatched join resolves is free to it. Its ask
           row must read 0 of N on the device figures.
  mirror   stops at rung 2: it finds the registration-lag spike from the two date columns, excludes
           mule registrations dated after its own case opened, and files 36 (35.669). It misses the call and
           the construction layer's estimated-incidence column, keeps the recorded-count column, and
           is held off the device figures by the same devices plus the documented mess it does not
           chase.

Stage 2 runs on the designed stops (paper). Stage 3 re-runs with --pack, which reads the ask ladder
values recomputed from the cut bundle (generator/ask_stops.json) and fails if any cracker row hits.

--forcing measures the other half on the cut bundle: per graded ask figure, the natural read's value
against the golden's, and whether the two print differently at the rounding that figure's own asking
sentence states. It fails if any figure does not move, because a figure the natural read already gets
right is a figure the device does not defend.
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
# primary device named in the design note's ask sheet. Ask A's row stays a miss after its basis and
# grain were pinned because the pin names the case and its closure, which the advices sheet cannot
# answer: the advice is a rollup above its own parts and the natural read is the rollup, measured at
# 16 of 16 figures and 320,142.56 on the Q1 total by --forcing and by ask_stops_build.py.
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


def _prints_apart(nat, gold, unit):
    """True when the two values print differently at the unit the asking sentence states. The test is
    the printed figure and not a tolerance: a count one whole case apart is a different graded answer,
    which a 'gap greater than the rounding' test scores as unmoved (ask B's narrowest cell, 14 against
    15, was the one row that failed it)."""
    return round(nat / unit) != round(gold / unit)


def forcing():
    """Per graded ask figure, the natural read against the golden, recomputed from the shipped bundle.

        python3 task196/generator/ceiling.py --forcing

    Ask A's natural read is the advice grain: the advices sheet's own totals, grouped by the advice's
    settlement month, which stands in for the quarter its cases closed in. Ask B's is the main Q1
    extract alone. Ask C's is the recovery statement's own stated route and quarter columns.
    """
    import csv as _csv
    import json as _json
    sys.path.insert(0, HERE)
    import verify as V

    fig = _json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    QM = {4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 1: 4, 2: 4, 3: 4}
    members = V.rows("member_register.csv")
    tier = {m["member_code"]: m["contribution_tier"] for m in members}
    adv = V.sheet("settlement_advices_2026_27.xlsx", "advices")
    q1 = V.rows("notifications_2027_28_q1.csv")
    stmt = V.rows("recovery_statement_2025_26.csv")
    moved = []

    nat = {}
    for r in adv:
        if r["cover_class"] != "unauthorised fraud":
            continue
        k = "Q%d %s" % (QM[int(str(r["settlement_month"])[5:7])], tier[r["member_code"]])
        nat[k] = round(nat.get(k, 0.0) + float(r["advice_total_gbp"]), 2)
    for q in (1, 2, 3, 4):
        nat["Q%d total" % q] = round(sum(nat.get("Q%d %s" % (q, t), 0.0) for t in "ABC"), 2)
    for k, v in sorted(fig["ask_a_indemnity_unauthorised"].items()):
        moved.append(("A %s" % k, "%.2f" % nat[k], "%.2f" % v, _prints_apart(nat[k], v, 1.0)))

    for m in members:
        mine = [r for r in q1 if r["member_code"] == m["member_code"]]
        for label, natv, gold in (
                ("notified", len(mine), fig["ask_b_q1_notifications"]["%s notified" % m["member_code"]]),
                ("value", round(sum(float(r["payment_amount_gbp"]) for r in mine)),
                 fig["ask_b_q1_notifications"]["%s value" % m["member_code"]])):
            moved.append(("B %s %s" % (m["member_code"], label), natv, gold,
                          _prints_apart(natv, gold, 1.0)))

    for r in stmt:
        k = "Q%s %s" % (r["quarter_closed"][1], r["recovery_route"])
        natv = round(float(r["recovered_stated_gbp"]) / float(r["reimbursed_in_quarter_gbp"]) * 100.0, 1)
        gold = fig["ask_c_recovery_share"][k]
        moved.append(("C %s" % k, natv, gold, _prints_apart(natv, gold, 0.1)))
    for route in V.ROUTES:
        natv = round(sum(float(r["recovered_stated_gbp"]) for r in stmt if r["recovery_route"] == route)
                     / sum(float(r["reimbursed_in_quarter_gbp"]) for r in stmt
                           if r["recovery_route"] == route) * 100.0, 1)
        gold = fig["ask_c_recovery_share"]["year %s" % route]
        moved.append(("C year %s" % route, natv, gold, _prints_apart(natv, gold, 0.1)))

    print("task196 ask forcing, measured on the cut bundle")
    print("=" * 78)
    print("  %-22s %14s %14s %8s" % ("figure", "natural", "golden", "moved"))
    for label, natv, gold, ok_ in moved:
        print("  %-22s %14s %14s %8s" % (label, natv, gold, "yes" if ok_ else "NO"))
    hit = sum(1 for _, _, _, o in moved if o)
    print("\n  %d of %d graded ask figures print differently under the natural read" % (hit, len(moved)))
    return 0 if hit == len(moved) else 1


if __name__ == "__main__":
    if "--forcing" in sys.argv:
        sys.exit(forcing())
    sys.exit(main())
