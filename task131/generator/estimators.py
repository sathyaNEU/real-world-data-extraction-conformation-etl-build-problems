"""Readings of the test, computed from tables in the shipped layout.

facts:  card_no, iso_week, baskets, gross_sales_chf, gross_margin_chf, reward_cost_chf
alloc:  card_no, cell
cards:  card_no, membership_no
regions: membership_no -> region (whichever vintage the caller passes)
"""
import numpy as np
import pandas as pd

import world as W

BASE_W = [W.WEEKS[i] for i in W.BASE]
RUN_W = [W.WEEKS[i] for i in W.RUN]
TEST_W = [W.WEEKS[i] for i in W.TEST]


def card_panel(facts, alloc, value, weeks):
    """Mean per card-week over `weeks`, every allocated card, weeks without a row counted as zero."""
    f = facts[facts["iso_week"].isin(weeks)]
    tot = f.groupby("card_no")[value].sum()
    out = alloc[["card_no"]].copy()
    out["v"] = out["card_no"].map(tot).fillna(0.0) / len(weeks)
    return out.set_index("card_no")["v"]


def with_net(facts):
    f = facts.copy()
    f["net"] = f["gross_margin_chf"] - f["reward_cost_chf"]
    return f


def card_changes(facts, alloc, value="net", window=None):
    window = window or RUN_W
    f = with_net(facts)
    post = card_panel(f, alloc, value, window)
    pre = card_panel(f, alloc, value, BASE_W)
    return (post - pre).rename("delta")


def lift_by_cell(delta, alloc, mask=None, weight=None):
    a = alloc.set_index("card_no")
    d = pd.DataFrame({"delta": delta, "cell": a["cell"]})
    if mask is not None:
        d = d[mask.reindex(d.index).fillna(False).to_numpy()]
    if weight is None:
        means = d.groupby("cell")["delta"].mean()
    else:
        w = weight.reindex(d.index)
        means = (d["delta"] * w).groupby(d["cell"]).sum() / w.groupby(d["cell"]).sum()
    return {x: means[x] - means["K"] for x in W.OFFERS}


def same_cell_mask(alloc, cards):
    a = alloc.merge(cards[["card_no", "membership_no"]], on="card_no")
    n = a.groupby("membership_no")["cell"].nunique()
    a["same"] = a["membership_no"].map(n) == 1
    return a.set_index("card_no")["same"]


def single_card_mask(alloc, cards):
    a = alloc.merge(cards[["card_no", "membership_no"]], on="card_no")
    n = a.groupby("membership_no")["card_no"].count()
    a["single"] = a["membership_no"].map(n) == 1
    return a.set_index("card_no")["single"]


def membership_weight(alloc, cards):
    """Weight each card by 1 / cards in its membership, so every membership counts once."""
    a = alloc.merge(cards[["card_no", "membership_no"]], on="card_no")
    n = a.groupby("membership_no")["card_no"].count()
    return (1.0 / a.set_index("card_no")["membership_no"].map(n)).rename("w")


# ---- the ladder ----------------------------------------------------------------

def rung0_gross_sales(facts, alloc):
    d = card_changes(facts, alloc, value="gross_sales_chf", window=TEST_W)
    return lift_by_cell(d, alloc)


def rung1_net_all_test(facts, alloc):
    return lift_by_cell(card_changes(facts, alloc, window=TEST_W), alloc)


def rung2_net_run_rate(facts, alloc):
    return lift_by_cell(card_changes(facts, alloc), alloc)


def answer_net_same_cell(facts, alloc, cards, weight=False):
    m = same_cell_mask(alloc, cards)
    w = membership_weight(alloc, cards) if weight else None
    return lift_by_cell(card_changes(facts, alloc), alloc, mask=m, weight=w)


def answer_net_single_card(facts, alloc, cards):
    m = single_card_mask(alloc, cards)
    return lift_by_cell(card_changes(facts, alloc), alloc, mask=m)


def partial_main_card_arm(facts, alloc, cards):
    """Membership totals with mixed memberships kept, each membership in its main card's cell."""
    f = with_net(facts)
    a = alloc.merge(cards[["card_no", "membership_no", "card_type"]], on="card_no")
    post = card_panel(f, alloc, "net", RUN_W)
    pre = card_panel(f, alloc, "net", BASE_W)
    a["d"] = a["card_no"].map(post - pre)
    md = a.groupby("membership_no")["d"].sum()
    mc = a[a["card_type"] == "main"].set_index("membership_no")["cell"]
    ncards = a.groupby("membership_no")["card_no"].count()
    per_card = (md / ncards)
    g = pd.DataFrame({"pc": per_card, "cell": mc, "n": ncards})
    means = (g["pc"] * g["n"]).groupby(g["cell"]).sum() / g["n"].groupby(g["cell"]).sum()
    return {x: means[x] - means["K"] for x in W.OFFERS}


def grid(facts, alloc, cards, region_of_membership, same_cell=True):
    """Run-rate lift per active card-week by region and offer."""
    delta = card_changes(facts, alloc)
    a = alloc.merge(cards[["card_no", "membership_no"]], on="card_no")
    a["region"] = a["membership_no"].map(region_of_membership)
    m = same_cell_mask(alloc, cards) if same_cell else pd.Series(True, index=alloc["card_no"])
    out = {}
    for r, _ in W.REGIONS:
        cards_r = a.loc[a["region"] == r, "card_no"]
        mr = m.copy()
        mr[:] = False
        mr[cards_r] = m[cards_r]
        out[r] = lift_by_cell(delta, alloc, mask=mr)
    return out


def programme_value_2027(per_card_week, planned_cards):
    return per_card_week * 52 * planned_cards
