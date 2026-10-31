"""The golden from the shipped files: what each candidate adds, net of the demand that went to the category's other
lines on the out days and to the line itself after the restock, and the three asks.

Recapture accounting, line by line within each store. A line's level on a day is its mean units on the same weekday
within four weeks either side, over the days it was on the shelf, outside the fortnight after its own restock and
with no other line of its category out (eight weeks either side where four hold fewer than two such days). Over the
twelve months to 30 June 2026 the category lost the levels of its out lines on their out days, less what its lines
sold above their levels on the days another of its lines was out and in the fortnight after their own restock.
"""
import os

import numpy as np
import pandas as pd

import params as P

CATS = ["Bottled water", "Infant formula", "Dry pet food", "Gluten-free bakery"]
BASE = (P.BASE_LO - P.D0).days
ND = P.ND


def load(folder, returns=True, codes="history"):
    """returns=False drops the till rows that net to negative units; codes="current" maps the tills' codes by
    lines.csv alone (article numbers and each line's current GTIN), the two readings the fork table tests."""
    f = lambda n: os.path.join(folder, n)
    ln = pd.read_csv(f("lines.csv")).rename(columns={"shelf_price_fy2025_incl_gst": "shelf_price_fy2025", "shelf_price_fy2026_incl_gst": "shelf_price_fy2026"})
    ch = pd.read_csv(f("till_item_codes.csv"), dtype={"item_code": str})
    st = pd.read_csv(f("stores.csv"))
    pos = pd.read_parquet(f("pos_daily_sales_2024-07_2026-06.parquet")).rename(columns={"net_sales_nzd_incl_gst": "net_sales_nzd"})
    stk = pd.read_csv(f("stock_positions_2024-07_2026-06.csv"))
    art = dict(zip(ch.item_code, ch.article))
    if codes == "current":
        art = {**{str(a): a for a in ln.article}, **{str(g): a for g, a in zip(ln.gtin, ln.article)}}
        pos = pos[pos.item_code.isin(list(art))]
    if not returns:
        pos = pos[pos.units > 0]
    s_idx = {s: k for k, s in enumerate(st.store_no)}
    l_idx = {a: k for k, a in enumerate(ln.article)}
    S, L = len(st), len(ln)
    U = np.zeros((S, L, ND))
    d_pos = (pd.to_datetime(pos.trade_date) - P.D0).dt.days.values
    li = pos.item_code.map(art).map(l_idx).values
    assert not np.isnan(li.astype(float)).any()
    np.add.at(U, (pos.store_no.map(s_idx).values, li.astype(int), d_pos), pos.units.values)
    traded = np.zeros((S, ND), bool)
    traded[pos.store_no.map(s_idx).values, d_pos] = True
    on = np.zeros((S, L, ND), np.int64)
    d_stk = (pd.to_datetime(stk.date) - P.D0).dt.days.values
    on[stk.store_no.map(s_idx).values, stk.article.map(l_idx).values, d_stk] = stk.on_hand_open.values
    closed = ~traded
    O = (on == 0) & ~closed[:, None, :]
    return dict(ln=ln, st=st, U=U, O=O, closed=closed, price=ln.shelf_price_fy2026.values,
                cat=ln.category.values)


def restock_mask(o, reb):
    end = np.zeros_like(o)
    end[:, :, :-1] = o[:, :, :-1] & ~o[:, :, 1:]
    after = np.zeros_like(o)
    for k in range(1, reb + 1):
        after[:, :, k:] |= end[:, :, :-k]
    return after & ~o


def sym_levels(U, ok, half=28, step=7):
    num = np.zeros_like(U)
    den = np.zeros_like(U)
    for k in range(step, half + 1, step):
        num[:, :, k:] += (U * ok)[:, :, :-k]
        den[:, :, k:] += ok[:, :, :-k]
        num[:, :, :-k] += (U * ok)[:, :, k:]
        den[:, :, :-k] += ok[:, :, k:]
    return num / np.maximum(den, 1), den


def recapture(U, O, closed, price, half=28, reb=14, strict=True, step=7, keep_after=False, span=1):
    """NZD over the base year: gross (levels of out lines on out days), the parts recaptured, and the net."""
    after = restock_mask(O, reb)
    other = (O.sum(axis=1, keepdims=True) - O) > 0
    ok = ~O & ~closed[:, None, :]
    if not keep_after:
        ok &= ~after
    if strict:
        ok &= ~other
    lev, den = sym_levels(U, ok.astype(float), half, step)
    lev2, _ = sym_levels(U, ok.astype(float), 2 * half, step)
    lev = np.where(den < 2, lev2, lev)
    pr = price[None, :, None]
    sl = slice(BASE, None) if span == 1 else slice(None)
    inst = ~O & ~closed[:, None, :]
    exc = (U - lev) * inst * pr
    gross = (lev * O * pr)[:, :, sl].sum()
    sub = (exc * other)[:, :, sl].sum()
    dfr = (exc * after)[:, :, sl].sum()
    rec = (exc * (other | after))[:, :, sl].sum()
    return {k: v / span for k, v in dict(gross=gross, sub_only=gross - sub, def_only=gross - dfr, net=gross - rec).items()}


def by_category(D, **kw):
    out = {}
    for c in CATS:
        m = D["cat"] == c
        out[c] = recapture(D["U"][:, m, :], D["O"][:, m, :], D["closed"], D["price"][m], **kw)
    return out


def golden(folder):
    D = load(folder)
    est = by_category(D)
    add = {c: est[c]["net"] * P.CUT for c in CATS}
    oos = {c: int(D["O"][:, D["cat"] == c, BASE:].sum()) for c in CATS}
    return D, est, add, oos


# ---------------------------------------------------------------------------------------------------------------
# Other constructions, for the checks

def global_levels(D):
    """Each store-line-weekday's mean over every open day on the shelf, both years: the levels with nothing kept out."""
    U, O, closed = D["U"], D["O"], D["closed"]
    dow = P.DAYS.dayofweek.values
    inst = (~O & ~closed[:, None, :]).astype(float)
    lev = np.zeros_like(U)
    for w in range(7):
        m = dow == w
        lev[:, :, m] = ((U[:, :, m] * inst[:, :, m]).sum(axis=2) / np.maximum(inst[:, :, m].sum(axis=2), 1))[:, :, None]
    out = {}
    for c in CATS:
        k = D["cat"] == c
        o, u, l_ = O[:, k, :], U[:, k, :], lev[:, k, :]
        pr = D["price"][k][None, :, None]
        other = (o.sum(axis=1, keepdims=True) - o) > 0
        after = restock_mask(o, 14)
        ins = ~o & ~closed[:, None, :]
        exc = (u - l_) * ins * pr
        sl = slice(BASE, None)
        out[c] = ((l_ * o * pr)[:, :, sl].sum() - (exc * (other | after))[:, :, sl].sum()) * P.CUT
    return out


def regression(D, freq):
    """Store-period category sales on the share of line-days out, store and month effects, both years: the NZD a
    line-day out costs the category, times the base year's line-days out."""
    months = P.DAYS.to_period("M")
    per = P.DAYS.to_period("W-SUN") if freq == "W" else months
    out = {}
    for c in CATS:
        k = D["cat"] == c
        val = (D["U"][:, k, :] * D["price"][k][None, :, None]).sum(axis=1)
        o = D["O"][:, k, :].sum(axis=1)
        rows = []
        for s in range(val.shape[0]):
            df = pd.DataFrame({"p": per, "m": months, "v": val[s], "o": o[s], "open": ~D["closed"][s]})
            g = df[df.open].groupby("p").agg(v=("v", "sum"), o=("o", "sum"), n=("v", "size"), m=("m", "first"))
            g["s"] = s
            rows.append(g.reset_index())
        d = pd.concat(rows)
        X = pd.get_dummies(d[["s", "m"]].astype(str), drop_first=True).astype(float)
        X["o_day"] = (d.o / d.n).values
        X["c"] = 1.0
        beta = np.linalg.lstsq(X.values, (d.v / d.n).values, rcond=None)[0][list(X.columns).index("o_day")]
        out[c] = -beta * D["O"][:, k, BASE:].sum() * P.CUT
    return out


def family(D):
    """Every netting construction the record leaves standing, and the rungs that stop short."""
    fam = {}
    for name, kw in (("base", {}), ("four weeks", dict(half=21)), ("five weeks", dict(half=35)),
                     ("ten-day rebound", dict(reb=10)), ("three-week rebound", dict(reb=21)),
                     ("all days within a fortnight", dict(step=1, half=14)),
                     ("other-out days kept in the levels", dict(strict=False)),
                     ("every day on the shelf in the levels", dict(strict=False, keep_after=True))):
        e = by_category(D, **kw)
        fam[name] = {c: e[c]["net"] * P.CUT for c in CATS}
        if name == "base":
            rungs = {"line-level lost sales": {c: e[c]["gross"] * P.CUT for c in CATS},
                     "net of the other lines on the out days only": {c: e[c]["sub_only"] * P.CUT for c in CATS},
                     "net of the restock only": {c: e[c]["def_only"] * P.CUT for c in CATS}}
    fam["global weekday levels"] = global_levels(D)
    fam["store-month regression"] = regression(D, "M")
    rungs["store-week regression"] = regression(D, "W")
    return fam, rungs


# ---------------------------------------------------------------------------------------------------------------
# The asks

TRIAL_LIVE = pd.Timestamp("2026-02-02")
TRIAL_STORES = [203, 204, 210]
DC_CATS = ["Bottled water", "Dry pet food", "Gluten-free bakery"]
QUARTERS = ["2025Q3", "2025Q4", "2026Q1", "2026Q2"]
MONTHS = [str(m) for m in pd.period_range("2025-07", "2026-06", freq="M")]


def ask_trial(folder):
    """Each trial store's cereal line-days that opened with nothing on hand, after go-live, and the share they were
    down on the thirteen weeks before: the export gives the opening stock to 1 February and the closing stock from 2
    February, so a day's opening after go-live is the previous day's close plus that morning's delivery."""
    t = pd.read_csv(os.path.join(folder, "cereal_trial_stock_2025-11_2026-05.csv"))
    t["date"] = pd.to_datetime(t.date)
    t = t.sort_values(["store_no", "article", "date"]).reset_index(drop=True)
    g = t.groupby(["store_no", "article"])
    prev_on = g.on_hand.shift(1)
    prev_sold = g.units_sold.shift(1)
    prev_close = np.where(t.date == TRIAL_LIVE, prev_on - prev_sold, prev_on)
    before = t.date < TRIAL_LIVE
    opening = np.where(before, t.on_hand, prev_close + t.delivered)
    t["out"] = opening == 0
    out = {}
    for st in TRIAL_STORES:
        x = t[t.store_no == st]
        b = int(x[x.date < TRIAL_LIVE].out.sum())
        a = int(x[x.date >= TRIAL_LIVE].out.sum())
        out[st] = dict(before=b, after=a, down_pct=100.0 * (1 - a / b))
    return out


def ask_stops(folder):
    """Each store's trailer stops that reached it after it opened that day: 6:30 while the tills' first sales come
    from 6:30, 7:00 once they come from 7:00 (1 April 2026)."""
    s = pd.read_csv(os.path.join(folder, "dc_trailer_stops_2025-26.csv"))
    tr = pd.read_csv(os.path.join(folder, "store_trading_days_2025-26.csv"))
    first = pd.to_datetime(tr.trade_date + " " + tr.first_sale)
    tr["opened"] = first.dt.floor("30min")
    s["arr"] = pd.to_datetime(s.arrived)
    s["trade_date"] = s.arr.dt.strftime("%Y-%m-%d")
    m = s.merge(tr[["store_no", "trade_date", "opened"]], on=["store_no", "trade_date"], how="left")
    assert m.opened.notna().all()
    st = pd.read_csv(os.path.join(folder, "stores.csv"))
    late = m[m.arr > m.opened].groupby("store_no").size().reindex(st.store_no).fillna(0).astype(int)
    return late


def ask_pallets(folder):
    """Pallets the distribution centre received from each candidate category's suppliers in each month of the twelve
    months to 30 June 2026. The receiving system books a truck's pallets onto every line it received from that truck,
    under every dispatch advice the truck carried, so each dock appointment counts once."""
    f = lambda n: os.path.join(folder, n)
    grn = pd.read_csv(f("dc_goods_received_2025-26.csv"))
    dock = pd.read_csv(f("dc_dock_appointments_2025-26.csv"))
    ln = pd.read_csv(f("lines.csv")).rename(columns={"shelf_price_fy2025_incl_gst": "shelf_price_fy2025", "shelf_price_fy2026_incl_gst": "shelf_price_fy2026"})
    cat = dict(zip(ln.article, ln.category))
    t = grn.assign(ap=grn.delivery_ref.map(dict(zip(dock.delivery_ref, dock.appointment_no)))).drop_duplicates("ap")
    t = t.assign(cat=t.article.map(cat), m=pd.to_datetime(t.received).dt.to_period("M").astype(str))
    return t.groupby(["cat", "m"]).pallets.sum().unstack().reindex(index=DC_CATS, columns=MONTHS)
