"""Assertions over the built pack and the golden reading. Run after build; exits non-zero on failure."""
import json
import os
import shutil
import sys
import tempfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import estimators as E
import golden as G
from build import FILES, DISTRACTORS, TASK

N = {"n": 0}
FAIL = []


def check(cond, msg):
    N["n"] += 1
    if not cond:
        FAIL.append(msg)


def r2(v):
    return round(v + 1e-12, 2)


def clearance(v, unit=0.01):
    """distance from v to the nearest rounding edge of its bin, in units of the bin width"""
    x = v / unit
    return 0.5 - abs(x - round(x))


def run(target=None):
    target = target or os.path.join(TASK, "target")
    f, a, c, m, b, planned = G.load(target)
    fig = G.figures(target)
    ch = fig["chain"]

    # ---- input gates ----
    files = sorted(os.listdir(target))
    check(len(files) >= 10, "fewer than 10 files")
    fmts = {os.path.splitext(x)[1] for x in files}
    check(len(fmts) >= 3, "fewer than 3 formats")
    check(len(f) >= 25_000, "spine under 25,000 rows")
    check(len(DISTRACTORS) >= 2, "fewer than two distractors")
    for k in FILES:
        check(FILES[k] in files, "missing " + FILES[k])
    check(not any("distractor" in x.lower() for x in files), "a file name says distractor")

    # ---- allocation and keys ----
    check(a["card_no"].is_unique, "allocation register has a repeated card")
    check(set(a["card_no"]) == set(c["card_no"]), "allocated cards are not exactly the member cards")
    shares = a["cell"].value_counts(normalize=True)
    check(all(abs(shares[x] - 0.2) < 0.01 for x in W.ARMS), "cell shares not balanced")
    check(not f.duplicated(["card_no", "iso_week"]).any(), "card-week key not unique")
    check(set(f["card_no"]) <= set(a["card_no"]), "facts carry a card outside the register")
    base_cards = set(f.loc[f["iso_week"].isin(E.BASE_W), "card_no"])
    check(base_cards == set(a["card_no"]), "an allocated card has no baseline purchase")
    check((f["gross_sales_chf"] > 0).all(), "a fact row with no sales")
    check((f["reward_cost_chf"] >= 0).all(), "negative reward cost")
    check((f["gross_margin_chf"] < f["gross_sales_chf"]).all(), "margin above sales")
    check((f["gross_margin_chf"] < 0).mean() < 0.0002, "too many negative margin rows")
    check(c.groupby("membership_no")["card_type"].apply(lambda s: (s == "main").sum() == 1).all(),
          "a membership without exactly one main card")
    check(c.groupby("membership_no").size().max() <= 4, "a membership with more than four cards")
    check(set(m["home_branch"]) <= set(b["branch_no"]), "a home branch outside the January register")

    # ---- the ladder ----
    r0 = E.rung0_gross_sales(f, a)
    r1 = E.rung1_net_all_test(f, a)
    r2_ = E.rung2_net_run_rate(f, a)
    rank = lambda d: sorted(d, key=d.get, reverse=True)
    lead = lambda d: d[rank(d)[0]] / d[rank(d)[1]]
    check(rank(r0)[0] == "C", "rung 0 winner is not C: %s" % rank(r0))
    check(rank(r1)[0] == "B", "rung 1 winner is not B: %s" % rank(r1))
    check(rank(r2_)[0] == "D", "rung 2 winner is not D: %s" % rank(r2_))
    check(rank(ch)[0] == "A", "answer is not A: %s" % rank(ch))
    check(rank(ch)[1] == "D", "runner-up is not D")
    for name, d in (("r0", r0), ("r1", r1), ("r2", r2_)):
        check(lead(d) >= 1.15, "%s lead under 1.15x (%.3f)" % (name, lead(d)))
    check(lead(r2_) >= 1.20, "rung 2 lead under 1.20x")
    check(ch["A"] / ch["D"] >= 1.2, "final margin under 1.2x")
    check(rank(r0).index("A") >= 3, "answer not 4th on the natural pipeline")
    check(rank(r1).index("A") >= 2 and rank(r2_).index("A") >= 1, "answer leads or is 2nd on an intermediate rung")
    winners = [rank(r0)[0], rank(r1)[0], rank(r2_)[0], rank(ch)[0]]
    check(len(set(winners)) == 4, "two rungs share a winner: %s" % winners)
    # the stump sentence: the card-level run-rate reading files D
    check(r2(r2_["D"]) != r2(ch["D"]) and r2(r2_["A"]) != r2(ch["A"]), "card-level figures equal the golden")

    # ---- partial correction: membership totals, mixed memberships in the main card's cell ----
    pm = E.partial_main_card_arm(f, a, c)
    check(all(r2(pm[x]) != r2(ch[x]) for x in W.OFFERS), "partial correction reproduces a golden figure")

    # ---- C1 convergence: every same-cell estimator files the same figures ----
    alt = {"membership-weighted": E.answer_net_same_cell(f, a, c, weight=True),
           "single-card only": E.answer_net_single_card(f, a, c)}
    for k, d in alt.items():
        for x in W.OFFERS:
            check(r2(d[x]) == r2(ch[x]), "%s %s %.4f vs %.4f" % (k, x, d[x], ch[x]))
        check(r2(d["A"] - d["D"]) == r2(ch["A"] - ch["D"]), "%s gap differs" % k)
    single = E.single_card_mask(a, c)
    reg27 = G.region_2027(m, b)
    delta = E.card_changes(f, a)
    for r, _ in W.REGIONS:
        cards_r = set(c.loc[c["membership_no"].map(reg27) == r, "card_no"])
        ms = single.copy()
        ms[:] = False
        idx = [x for x in single.index if x in cards_r]
        ms[idx] = single[idx]
        d1 = E.lift_by_cell(delta, a, mask=ms)
        for x in W.OFFERS:
            check(r2(d1[x]) == r2(fig["grid"][r][x]), "grid %s %s single-card differs" % (r, x))

    # ---- bin clearance ----
    for x in W.OFFERS:
        check(clearance(ch[x]) >= 0.15, "chain %s near a bin edge (%.4f)" % (x, ch[x]))
        check(clearance(fig["value_chf"][x], 1000) >= 0.15, "2027 value %s near a bin edge" % x)
    check(clearance(fig["gap"]) >= 0.15, "gap near a bin edge")
    for r, _ in W.REGIONS:
        for x in W.OFFERS:
            check(clearance(fig["grid"][r][x]) >= 0.12, "grid %s %s near a bin edge (%.4f)" % (r, x, fig["grid"][r][x]))
    tot = fig["planned_total"]
    check(tot % 100 != 0, "plan total is a round hundred")

    # ---- the two grid devices ----
    regjan = m.set_index("membership_no")["home_branch"].map(b.set_index("branch_no")["region_code"])
    gjan = E.grid(f, a, c, regjan)
    for r in ("SGS", "RHT", "FUE", "APZ"):
        for x in W.OFFERS:
            check(r2(gjan[r][x]) != r2(fig["grid"][r][x]), "January regions reproduce %s %s" % (r, x))
    # moves applied, closures ignored (the closed branch read through the January register)
    reg_moves = regjan.copy()
    reg_moves[m.set_index("membership_no")["home_branch"].isin(["3107", "3112", "3115"])] = "SGS"
    gmov = E.grid(f, a, c, reg_moves)
    for r in ("FUE", "APZ"):
        for x in W.OFFERS:
            check(r2(gmov[r][x]) != r2(fig["grid"][r][x]), "closure device inert on %s %s" % (r, x))
    # closures dropped as unmatched in the July network
    reg_drop = reg27.copy()
    reg_drop[m.set_index("membership_no")["home_branch"].isin(["2209", "4105"]).to_numpy()] = None
    gdrop = E.grid(f, a, c, reg_drop)
    check(any(r2(gdrop["APZ"][x]) != r2(fig["grid"]["APZ"][x]) for x in W.OFFERS), "dropping the closed branches is inert")
    # card-level by region: every cell off the golden
    gcard = E.grid(f, a, c, reg27, same_cell=False)
    off = sum(r2(gcard[r][x]) != r2(fig["grid"][r][x]) for r, _ in W.REGIONS for x in W.OFFERS)
    check(off >= 20, "card-level grid reproduces %d golden cells" % (24 - off))

    # ---- separation: the main call reads no region, branch or membership attribute ----
    ch_noreg = E.answer_net_same_cell(f, a, c[["card_no", "membership_no"]])
    check(all(ch_noreg[x] == ch[x] for x in W.OFFERS), "main call depends on something beyond cards and cells")

    # ---- lens swap: the answer's population is not the naive population ----
    same = E.same_cell_mask(a, c)
    check(0.25 < same.mean() < 0.6, "same-cell share of cards out of range (%.3f)" % same.mean())

    # ---- distractors: the golden does not read them ----
    tmp = tempfile.mkdtemp()
    for x in files:
        if x not in [FILES[k] for k in DISTRACTORS]:
            shutil.copy(os.path.join(target, x), tmp)
    fig2 = G.figures(tmp)
    shutil.rmtree(tmp)
    check(fig2["chain"] == ch and fig2["value_chf"] == fig["value_chf"], "golden moves without the distractors")

    # ---- the stakeholder belief: C moved the most spend ----
    check(rank(r0)[0] == "C", "the monthly target did not move the most spend")

    # ---- generation tells ----
    for x in W.OFFERS:
        check(abs(fig["value_chf"][x] - round(fig["value_chf"][x], -4)) > 500, "a 2027 value near a round ten thousand")

    print("checks: %d assertions, %d failed" % (N["n"], len(FAIL)))
    for x in FAIL:
        print("  FAIL", x)
    return not FAIL


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
