"""task122 generator: the two asks, computed from the files as written.

Ask 1: each policy's change in buyer-protection fee income per 1,000 carousel sessions in each of the
eight cells while the slot runs (euros, one decimal). Ask 2: each policy's extra orders and extra fee
income over the twelve weeks (nearest hundred). The golden path and every wrong path the ask ledger
names: pickup orders paid in person priced (P1), the asking price (HZ2), the January tariff row and
the charged mix (HZ1), the first release of the weekly table (P2), all twelve weeks on the app (HZ3),
the pooled lift, the in-session basis, and the over-cleaners.
"""
import itertools
import os
import re

import numpy as np
import pandas as pd

import analysis as A
import params as P
import traffic as Tr
import writers as Wr

F_WEEKLY = "home_carousel_sessions_weekly_2025W01_2026W39.csv"
F_R2 = "home_carousel_sessions_weekly_R2_2026W01_2026W26.csv"
F_TARIFF = "kopersbescherming_tarieven.csv"


def offers_file(tgt):
    return [f for f in os.listdir(tgt) if f.startswith("offers_accepted_")][0]


def load_fee_path(tgt, M):
    """Orders in each logged session's 21-day window, with payment, price paid and offer details."""
    S, O = M.S, M.O
    pay = pd.read_parquet(os.path.join(tgt, Wr.F_PAYMENTS))
    off = pd.read_csv(os.path.join(tgt, offers_file(tgt)), parse_dates=["offered_at", "accepted_at", "expires_at"])
    o = O.merge(pay, on="order_id", how="left")
    o["paid_through"] = o.payment_id.notna()
    o["price_paid_pay"] = np.round(o.amount_eur - o.shipping_eur - o.buyer_protection_fee_eur, 2)
    # price paid from the offers export: an accepted offer still valid at checkout, else the asking price
    m = o[["order_id", "buyer_id", "listing_id", "ordered_at"]].merge(off, on=["buyer_id", "listing_id"], how="left")
    live = m[(m.accepted_at <= m.ordered_at) & (m.expires_at >= m.ordered_at)].drop_duplicates("order_id")
    anyoff = m[m.offer_id.notna()].drop_duplicates("order_id")
    o["offer_live"] = o.order_id.map(live.set_index("order_id").offer_eur)
    o["offer_any"] = o.order_id.map(anyoff.set_index("order_id").offer_eur)
    o["price_paid_off"] = o.offer_live.fillna(o.asking_price_eur)
    # window: the 21 days from each logged session's start
    w = o.merge(S[["session_id", "buyer_id", "started_at", "ranker", "cell"]], on="buyer_id", how="inner")
    dt = (w.ordered_at - w.started_at).dt.total_seconds()
    w = w[(dt >= 0) & (dt <= 21 * 86400)].copy()
    w["in_session"] = (w.channel == "carousel") & (w.home_session_id == w.session_id)
    return o, w


def fee_cents(price, fixed, pct=5):
    return fixed + pct * np.round(np.asarray(price, float)).astype(int)


def variant_fees(w, p1="right", hz2="right", hz1="right", charged=False):
    """Fee in cents per order in the window under one reading of the three fee devices."""
    if charged:
        return np.where(w.paid_through, np.round(w.buyer_protection_fee_eur * 100), 0).astype(int)
    fixed = {"right": 80, "jan": 95, "old": 70}[hz1]
    if hz2 == "right":
        price = np.where(w.paid_through, w.price_paid_pay, w.asking_price_eur)
    elif hz2 == "asking":
        price = w.asking_price_eur.to_numpy()
    elif hz2 == "every_offer":
        price = w.offer_any.fillna(w.asking_price_eur).to_numpy()
    else:
        raise ValueError(hz2)
    f = fee_cents(price, fixed)
    if p1 == "right":
        f = np.where(w.paid_through, f, 0)
    elif p1 == "wrong":
        pass
    elif p1 == "drop_pickups":
        f = np.where(w.paid_through & (w.delivery != "pickup"), f, 0)
    else:
        raise ValueError(p1)
    return f.astype(int)


def grid(S, w, values, in_session_only=False):
    """Change per 1,000 sessions against the incumbent, per (policy, cell): values are per order
    (orders count 1, fees in cents); returns euros or orders per 1,000 sessions."""
    v = np.asarray(values, float)
    if in_session_only:
        v = np.where(w.in_session.to_numpy(), v, 0.0)
    per = pd.Series(v, index=w.index).groupby(w.session_id).sum()
    tot = S.session_id.map(per).fillna(0).to_numpy()
    out = {}
    for c in range(8):
        cm = (S.cell == c).to_numpy()
        base = tot[cm & (S.ranker == "HC-24").to_numpy()].mean()
        for r in P.POLICIES:
            g = cm & (S.ranker == r).to_numpy()
            out[(r, c)] = (tot[g].mean() - base) * 1000
    return out


def to_euros(g):
    return {k: v / 100.0 for k, v in g.items()}


def load_traffic(tgt):
    r1 = pd.read_csv(os.path.join(tgt, F_WEEKLY))
    r2 = pd.read_csv(os.path.join(tgt, F_R2))
    def norm(df):
        y = df.iso_week.str.slice(0, 4).astype(int)
        wk = df.iso_week.str.slice(6, 8).astype(int)
        band = df.tenure_band.map({b: i for i, b in enumerate(Tr.BAND_LABELS)})
        return pd.DataFrame(dict(year=y, week=wk, platform=df.platform, band=band, sessions=df.logged_in_sessions))
    r1n, r2n = norm(r1), norm(r2)
    # R2 replaces the first release for the weeks it covers
    key = ["year", "week", "platform", "band"]
    rest = r1n.merge(r2n[key], on=key, how="left", indicator=True)
    rest = rest[rest["_merge"] == "left_only"].drop(columns="_merge")
    current = pd.concat([rest, r2n], ignore_index=True)
    return r1n, r2n, current


def totals(by_cell, arm):
    return {r: sum(by_cell[(r, c)] * arm[c] / 1000 for c in range(8)) for r in P.POLICIES}


def nearest_hundred(x):
    return int(np.floor(x / 100.0 + 0.5)) * 100


def compute(tgt, M=None):
    if M is None:
        M = A.load_main(tgt)
    S = M.S
    o, w = load_fee_path(tgt, M)
    res = {}
    res["price_routes_agree"] = bool(np.all(np.isclose(o[o.paid_through].price_paid_pay,
                                                       o[o.paid_through].price_paid_off, atol=0.004)))
    ones = np.ones(len(w))
    res["orders_kept"] = grid(S, w, ones)
    res["orders_insession"] = grid(S, w, ones, in_session_only=True)
    gold = to_euros(grid(S, w, variant_fees(w)))
    res["fee"] = gold
    # every combination of the three formula devices (P1 priced in person, HZ2 asking, HZ1 January)
    combos = {}
    for p1, hz2, hz1 in itertools.product(("right", "wrong"), ("right", "asking"), ("right", "jan")):
        if (p1, hz2, hz1) == ("right", "right", "right"):
            continue
        combos[(p1, hz2, hz1)] = to_euros(grid(S, w, variant_fees(w, p1, hz2, hz1)))
    res["fee_combos"] = combos
    res["fee_charged"] = to_euros(grid(S, w, variant_fees(w, charged=True)))
    res["fee_drop_pickups"] = to_euros(grid(S, w, variant_fees(w, p1="drop_pickups")))
    res["fee_every_offer"] = to_euros(grid(S, w, variant_fees(w, hz2="every_offer")))
    res["fee_old_tariff"] = to_euros(grid(S, w, variant_fees(w, hz1="old")))
    res["fee_natural"] = to_euros(grid(S, w, variant_fees(w, "wrong", "asking", "jan"), in_session_only=True))
    res["fee_insession_right"] = to_euros(grid(S, w, variant_fees(w), in_session_only=True))
    # traffic
    r1n, r2n, cur = load_traffic(tgt)
    arm = Tr.arm_sessions(cur)
    arm_r1 = Tr.arm_sessions(r1n)
    arm_12 = Tr.arm_sessions(cur, app_weeks=P.ISO_WEEKS_SLOT)
    res["arm_sessions"] = arm
    res["arm_sessions_r1"] = arm_r1
    res["arm_sessions_12wk"] = arm_12
    res["tot_orders"] = totals(res["orders_kept"], arm)
    res["tot_fee"] = totals(gold, arm)
    # pooled lift on the planned total (no cell-by-cell planning)
    pooled_k = A.est(S, A.followup(M, hours=21 * 24).astype(float), "session_ipw")
    res["pooled_kept"] = pooled_k
    res["tot_orders_pooled"] = {r: pooled_k[r] * arm.sum() / 1000 for r in P.POLICIES}
    # natural read: pooled in-session lift x all twelve weeks x first release
    pooled_in = A.est(S, S.y.to_numpy().astype(float), "session_ipw")
    arm_nat = Tr.arm_sessions(r1n, app_weeks=P.ISO_WEEKS_SLOT)
    res["tot_orders_natural"] = {r: pooled_in[r] * arm_nat.sum() / 1000 for r in P.POLICIES}
    res["tot_orders_r1"] = totals(res["orders_kept"], arm_r1)
    res["tot_orders_12wk"] = totals(res["orders_kept"], arm_12)
    arm_both = Tr.arm_sessions(r1n, app_weeks=P.ISO_WEEKS_SLOT)
    res["tot_orders_r1_12wk"] = totals(res["orders_kept"], arm_both)
    # fee totals under every subset of the five devices
    fee_subsets = {}
    for p2, hz3 in itertools.product((False, True), repeat=2):
        a = Tr.arm_sessions(r1n if p2 else cur, app_weeks=P.ISO_WEEKS_SLOT if hz3 else P.APP_WEEKS)
        for key, g in [(("right", "right", "right"), gold)] + list(combos.items()):
            if not p2 and not hz3 and key == ("right", "right", "right"):
                continue
            fee_subsets[(p2, hz3) + key] = totals(g, a)
    res["tot_fee_subsets"] = fee_subsets
    return res
