"""task122 generator: the two asks, computed from the files as written.

Ask 1: each policy's change in buyer-protection fee income per 1,000 carousel sessions in each of the
eight cells while the slot runs (euros, one decimal). Ask 2: each policy's extra orders and extra fee
income over the twelve weeks (nearest hundred). The golden path and every wrong path the ask ledger
names: the checkout the slot runs on (FC: Checkout 3, in force since 21 September 2026, has every order paid
at checkout, so every logged order carries the fee in the slot; the logged window's checkout, where a pickup
paid to the seller in person carries none and which Finance's Q3 statement reproduces, is its wrong path), fee
income booked with the VAT in it (F1), purchases paid from a Vouwlijn balance left without a fee because they
have no provider payment (F2), the asking price (HZ2), the tariff register's newest row (HZ1), the first
release of the weekly table (P2), all twelve weeks on the app (HZ3), the in-session basis, the pooled lift,
and the over-cleaners.
"""
import itertools
import os

import numpy as np
import pandas as pd

import analysis as A
import params as P
import traffic as Tr
import writers as Wr

F_WEEKLY = "home_carousel_sessions_weekly_2025W01_2026W39.csv"
F_R2 = "home_carousel_sessions_weekly_R2_2026W01_2026W26.csv"
F_TARIFF = "kopersbescherming_tarieven.csv"

VAT = 1.0 + P.VAT_RATE
DEVICES = ("f1", "f2", "fc", "hz2", "hz1")       # VAT, balance-paid, the checkout in force, price paid, newest row
HAZ = list(itertools.product(("right", "wrong"), repeat=4))          # (f1, f2, hz2, hz1)
FC = ("new", "old")        # Checkout 3 (every order charged, the golden's); the logged window's checkout
GOLD = ("right", "right", "new", "right", "right")
READ_KEYS = [(h[0], h[1], fc, h[2], h[3]) for fc in FC for h in HAZ if (h[0], h[1], fc, h[2], h[3]) != GOLD]
NATURAL = ("wrong", "right", "new", "wrong", "wrong")   # every order priced on the formula, gross, asking, newest row


def offers_file(tgt):
    return [f for f in os.listdir(tgt) if f.startswith("offers_accepted_")][0]


def load_fee_path(tgt, M):
    """Every order with its provider payment and its price paid, and the orders in each logged
    session's 21-day window."""
    S, O = M.S, M.O
    pay = pd.read_parquet(os.path.join(tgt, Wr.F_PAYMENTS))
    off = pd.read_csv(os.path.join(tgt, offers_file(tgt)), parse_dates=["offered_at", "accepted_at", "expires_at"])
    o = O.merge(pay, on="order_id", how="left")
    o["paid_through"] = o.payment_id.notna()
    o["inperson"] = (~o.paid_through) & (o.delivery == "pickup")
    o["balance"] = (~o.paid_through) & (o.delivery != "pickup")
    o["price_paid_pay"] = np.round(o.amount_eur - o.shipping_eur - o.buyer_protection_fee_eur, 2)
    # price paid from the offers export: an accepted offer still valid at checkout, else the asking price
    m = o[["order_id", "buyer_id", "listing_id", "ordered_at"]].merge(off, on=["buyer_id", "listing_id"], how="left")
    live = m[(m.accepted_at <= m.ordered_at) & (m.expires_at >= m.ordered_at)].drop_duplicates("order_id")
    anyoff = m[m.offer_id.notna()].drop_duplicates("order_id")
    o["offer_live"] = o.order_id.map(live.set_index("order_id").offer_eur)
    o["offer_any"] = o.order_id.map(anyoff.set_index("order_id").offer_eur)
    o["price_paid_off"] = o.offer_live.fillna(o.asking_price_eur)
    o["price_paid"] = np.where(o.paid_through, o.price_paid_pay, o.price_paid_off)
    # window: the 21 days from each logged session's start
    w = o.merge(S[["session_id", "buyer_id", "started_at", "ended_at", "ranker", "cell"]], on="buyer_id", how="inner")
    dt = (w.ordered_at - w.started_at).dt.total_seconds()
    w = w[(dt >= 0) & (dt <= 21 * 86400)].copy()
    # in-session: ordered from one of the session's tiles before the session ended (the render log's count)
    w["in_session"] = ((w.channel == "carousel") & (w.home_session_id == w.session_id) &
                       (w.ordered_at <= w.ended_at))
    return o, w


def fee_cents(price, fixed, pct=5):
    return fixed + pct * np.round(np.asarray(price, float)).astype(int)


def variant_fees(w, f1="right", f2="right", cover="new", hz2="right", hz1="right", special=None):
    """Fee income in cents per order in the window under one checkout and one reading of the four hazards: cover
    new charges every order (Checkout 3, the slot's), cover old leaves a pickup paid in person uncharged (the logged
    window's checkout); f1 wrong keeps the VAT in; f2 wrong charges nothing on a purchase paid from a balance (no
    provider payment); hz2 wrong prices on the asking price; hz1 wrong takes the register's newest row.
    special: the over-cleaners and the other conventions the ledger prices."""
    if special == "charged":
        return np.where(w.paid_through, np.round(w.buyer_protection_fee_eur.to_numpy() * 100), 0).astype(float)
    fixed = {"right": P.SLOT_FIXED_CENTS, "wrong": P.LATEST_FIXED_CENTS}[hz1]
    if special == "old_tariff":
        fixed = 70
    if hz2 == "wrong":
        price = w.asking_price_eur.to_numpy()
    elif special == "every_offer":
        price = w.offer_any.fillna(w.asking_price_eur).to_numpy()
    else:
        price = w.price_paid.to_numpy()
    f = fee_cents(price, fixed).astype(float)
    inperson, balance = w.inperson.to_numpy(), w.balance.to_numpy()
    if cover == "old":
        f = np.where(inperson, 0.0, f)
    if f2 == "wrong":
        f = np.where(balance, 0.0, f)
    if special == "drop_pickups":
        f = np.where(w.delivery.to_numpy() == "pickup", 0.0, f)
    if f1 == "wrong":
        return f
    if special == "vat_per_order":
        return np.round(f / VAT)
    if special == "vat_off_gross":
        return f * (1.0 - P.VAT_RATE)
    return f / VAT


def grid(S, w, values, in_session_only=False):
    """Change per 1,000 sessions against the incumbent, per (policy, cell): values are per order
    (orders count 1, fees in cents); returns orders or cents per 1,000 sessions."""
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


def logged_mix(S):
    n = np.array([(S.cell == c).sum() for c in range(8)], float)
    return n / n.sum()


def compute(tgt, M=None):
    if M is None:
        M = A.load_main(tgt)
    S = M.S
    o, w = load_fee_path(tgt, M)
    res = {}
    res["price_routes_agree"] = bool(np.all(np.isclose(o[o.paid_through].price_paid_pay,
                                                       o[o.paid_through].price_paid_off, atol=0.004)))
    res["no_payment_split"] = dict(inperson=int(o.inperson.sum()), balance=int(o.balance.sum()),
                                   paid=int(o.paid_through.sum()))
    ones = np.ones(len(w))
    res["orders_kept"] = grid(S, w, ones)
    res["orders_insession"] = grid(S, w, ones, in_session_only=True)
    # the checkout in the records: before Checkout 3 (21 September 2026) a pickup could be paid to the seller at the
    # handover, with no provider capture; from that day every pickup carries one
    t3 = pd.Timestamp(P.CHECKOUT3)
    pk = o[o.delivery == "pickup"]
    res["checkout3"] = dict(before_pickups=int((pk.ordered_at < t3).sum()),
                            before_handover=int((pk.inperson & (pk.ordered_at < t3)).sum()),
                            after_pickups=int((pk.ordered_at >= t3).sum()),
                            after_handover=int((pk.inperson & (pk.ordered_at >= t3)).sum()),
                            last_handover=str(pk[pk.inperson].ordered_at.max()))
    G = {}
    for h in HAZ:
        for cov in FC:
            G[(h, cov)] = to_euros(grid(S, w, variant_fees(w, h[0], h[1], cov, h[2], h[3])))
    res["fee_cover_grids"] = G

    def reading(key):
        f1, f2, cov, hz2, hz1 = key
        return G[((f1, f2, hz2, hz1), cov)]
    gold = reading(GOLD)
    res["fee"] = gold
    res["fee_old_cover"], res["fee_full_cover"] = G[(HAZ[0], "old")], G[(HAZ[0], "new")]
    # the checkout's two states by every reading of the four hazards
    combos = {key: reading(key) for key in READ_KEYS}
    res["fee_combos"] = combos
    res["fee_natural"] = to_euros(grid(S, w, variant_fees(w, *NATURAL), in_session_only=True))
    res["fee_insession_right"] = to_euros(grid(S, w, variant_fees(w), in_session_only=True))
    for nm in ("drop_pickups", "every_offer", "old_tariff", "vat_off_gross", "vat_per_order"):
        res[f"fee_{nm}"] = to_euros(grid(S, w, variant_fees(w, special=nm)))
    res["fee_charged"] = to_euros(grid(S, w, variant_fees(w, special="charged")))
    # traffic
    r1n, r2n, cur = load_traffic(tgt)
    arm = Tr.arm_sessions(cur)
    arm_r1 = Tr.arm_sessions(r1n)
    arm_12 = Tr.arm_sessions(cur, app_weeks=P.ISO_WEEKS_SLOT)
    arm_r1_12 = Tr.arm_sessions(r1n, app_weeks=P.ISO_WEEKS_SLOT)
    res["arm_sessions"] = arm
    res["arm_sessions_r1"] = arm_r1
    res["arm_sessions_12wk"] = arm_12
    res["arm_sessions_r1_12wk"] = arm_r1_12
    res["tot_orders"] = totals(res["orders_kept"], arm)
    arms = {(False, False): arm, (True, False): arm_r1, (False, True): arm_12, (True, True): arm_r1_12}

    def fee_total(key, a_):
        return totals(reading(key), a_)
    res["tot_fee"] = fee_total(GOLD, arm)
    res["tot_orders_r1"] = totals(res["orders_kept"], arm_r1)
    res["tot_orders_12wk"] = totals(res["orders_kept"], arm_12)
    res["tot_orders_r1_12wk"] = totals(res["orders_kept"], arm_r1_12)
    # natural read: pooled in-session lift x the planned total on the first release, all twelve weeks on app
    pooled_in = A.est(S, S.y.to_numpy().astype(float), "session_ipw")
    res["tot_orders_natural"] = {r: pooled_in[r] * arm_r1_12.sum() / 1000 for r in P.POLICIES}
    # the headline and the totals on the slot's own cell mix against the logged mix (they converge)
    lm = logged_mix(S)
    sm = arm / arm.sum()
    ok_ = res["orders_kept"]
    res["headline_logged_mix"] = {r: float(sum(lm[c] * ok_[(r, c)] for c in range(8))) for r in P.POLICIES}
    res["headline_slot_mix"] = {r: float(sum(sm[c] * ok_[(r, c)] for c in range(8))) for r in P.POLICIES}
    res["tot_orders_pooled"] = {r: res["headline_logged_mix"][r] * arm.sum() / 1000 for r in P.POLICIES}
    res["tot_fee_pooled"] = {r: float(sum(lm[c] * gold[(r, c)] for c in range(8))) * arm.sum() / 1000
                             for r in P.POLICIES}
    # fee totals under the checkout's two states by every reading of the four hazards, on each traffic reading
    fee_subsets = {}
    for (p2, hz3), a_ in arms.items():
        for key in [GOLD] + READ_KEYS:
            if not p2 and not hz3 and key == GOLD:
                continue
            fee_subsets[(p2, hz3) + key] = fee_total(key, a_)
    res["tot_fee_subsets"] = fee_subsets
    res["tot_fee_natural"] = totals(res["fee_natural"], arm_r1_12)
    return res
