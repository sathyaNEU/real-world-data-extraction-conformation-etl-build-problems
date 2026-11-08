"""The golden computation on the cut pack, and every rival route the checks, the ladder and the ceiling price.

Everything reads target/ through bundle.py. compute() is the golden; the keyword switches reproduce the other
complete pipelines a careful analyst could file.
"""
import numpy as np

import bundle as B
from world import *

STOCKED = 30000.0          # opening stock plus goods in, at cost, at which a store week counts as stocked
PROVISION_UNIT = 100_000   # the provision, the borrowing base and the headroom are reported to the nearest 0.1 million


def rnd(v, unit):
    return int(np.floor(v / unit + 0.5)) * unit


def excess_lines(target, transfers_as_demand=False):
    s = B.stock(target).copy()
    o = B.orders(target)
    keep = (o.year == 2026) & ((o.kind == "customer") | ((o.kind == "transfer") & transfers_as_demand))
    net = o[keep].groupby(["sub", "key"])["qty"].sum().to_dict()
    s["net26"] = [net.get((a, k), 0) for a, k in zip(s["sub"], s["key"])]
    s["excess_qty"] = [min(q, max(0, q - max(0, n))) for q, n in zip(s["qty"], s["net26"])]
    s["unit_gbp"] = [v / q if q else 0.0 for v, q in zip(s["value_gbp"], s["qty"])]
    s["excess_gbp"] = s["excess_qty"] * s["unit_gbp"]
    return s


def outlet_weeks(target):
    w = B.vh_weeks(target).sort_values(["store", "week"]).copy()
    w["opening"] = w.groupby("store")["closing_stock_at_cost"].shift(1).fillna(0.0)
    w["available"] = w["opening"] + w["goods_in_at_cost"]
    return w


def throughput_per_day(target, stocked=STOCKED, full_only=True, stat="mean", exclude=None, years=None):
    w = outlet_weeks(target)
    m = w["trading_days"] > 0
    if full_only:
        m &= w["trading_days"] == 7
    if stocked is not None:
        m &= w["available"] >= stocked
    if exclude:
        m &= ~w["promotion"].isin(exclude)
    if years:
        m &= w["week"].map(lambda d: d.year).isin(years)
    v = (w.loc[m, "sales_at_cost"] / w.loc[m, "trading_days"]).values
    return float(np.median(v) if stat == "median" else np.mean(v)), int(m.sum())


def outlet_recovery(target, years=None):
    w = B.vh_weeks(target)
    if years:
        w = w[w["week"].map(lambda d: d.year).isin(years)]
    return float(w["sales_ex_vat"].sum() / w["sales_at_cost"].sum())


def trade_recovery(target, years=None):
    l = B.lots(target)
    if years:
        l = l[l["Contract date"].dt.year.isin(years)]
    return float(l["Price ex VAT (GBP)"].sum() / l["Stock at cost (GBP)"].sum())


def compute(target, capacity="stocked", stocked=STOCKED, transfers_as_demand=False, rec_years=None, job_years=None,
            stat="mean", full_only=True):
    """capacity: "stocked" (the golden: the stocked store-day throughput times the 2027 store-days), "none" (every
    pound of the pool at Valuehall's recovery), "sales2026" (Valuehall's 2026 sales at cost), "fit" (annual sales at
    cost regressed on annual goods in and extended to the pool), "blended" (Valuehall's proceeds, its own trade lots
    included, over everything it received, on the whole pool), "jobber" (the whole pool to trade buyers)."""
    ex = excess_lines(target, transfers_as_demand=transfers_as_demand)
    gross_sub = ex.groupby("sub")["value_gbp"].sum().to_dict()
    vh = B.vh_year_end_stock(target)
    gross = sum(gross_sub.values()) + vh
    excess_sub = ex.groupby("sub")["excess_gbp"].sum().to_dict()
    excess_div = ex.groupby("division")["excess_gbp"].sum().to_dict()
    excess = sum(excess_sub.values())
    pool = excess + vh
    r_out = outlet_recovery(target, rec_years)
    r_job = trade_recovery(target, job_years)
    per_day, n_weeks = throughput_per_day(target, stocked=stocked, stat=stat, full_only=full_only)
    days27 = sum(B.PLAN_DAYS_2027.values())
    w = B.vh_weeks(target)
    yr = w["week"].map(lambda d: d.year)
    if capacity == "stocked":
        cap = per_day * days27
    elif capacity == "sales2026":
        cap = float(w[yr == 2026]["sales_at_cost"].sum())
    elif capacity == "fit":
        g = w.groupby(yr).agg(i=("goods_in_at_cost", "sum"), s=("sales_at_cost", "sum"))
        b1, b0 = np.polyfit(g["i"].values, g["s"].values, 1)
        cap = b1 * pool + b0
    elif capacity in ("none", "blended"):
        cap = pool
    elif capacity == "jobber":
        cap = 0.0
    cap = max(0.0, min(cap, pool))
    if capacity == "blended":
        l = B.lots(target)
        own = \
            float(l[l["Seller"] == "Valuehall Stores Ltd"]["Price ex VAT (GBP)"].sum())
        r_out = (float(w["sales_ex_vat"].sum()) + own) / float(w["goods_in_at_cost"].sum())
    nrv = cap * r_out + (pool - cap) * r_job
    provision = pool - nrv
    carried = gross - provision
    bb = BB_ADVANCE * carried
    dr = B.drawn(target)
    headroom = bb - dr
    return dict(gross_sub=gross_sub, vh_stock=vh, gross=gross, excess_sub=excess_sub, excess_div=excess_div,
                excess=excess, pool=pool, r_out=r_out, r_job=r_job, per_day=per_day, n_weeks=n_weeks, days27=days27,
                cap=cap, outlet_share=cap, trade_share=pool - cap, nrv=nrv, provision=provision, carried=carried, bb=bb,
                drawn=dr, headroom=headroom, waiver=headroom < 0)


def price_credit_split(o):
    """Each AHL price credit (document type PRICE, on the non-stock code) as the order line it corrects: the one line on
    its order charged above the customer's price for the item before 1 April 2025 by exactly the credit (the quantity
    times the difference). Returns (code, value) pairs, one per credit."""
    import datetime as dt
    a = o[(o["sub"] == "AHL") & (o["kind"] == "customer")]
    desp = a[a["dtype"] == "DESP"]
    q1 = desp[desp["date"] < dt.date(2025, 4, 1)].assign(unit=lambda d: (d["value"] / d["qty"]).round(2))
    base = q1.groupby(["customer", "code"])["unit"].min().to_dict()
    over_of = {}
    for l in desp[desp["date"] >= dt.date(2025, 4, 1)].itertuples(index=False):
        b = base.get((l.customer, l.code))
        if b is not None and l.qty > 0:
            ov = round(l.value - l.qty * b, 2)
            if ov > 0.004:
                over_of.setdefault((l.doc, l.customer), []).append((l.code, ov))
    out = []
    for c in a[a["dtype"] == "PRICE"].itertuples(index=False):
        hits = [code for code, ov in over_of.get((c.doc, c.customer), []) if abs(ov + c.value) < 0.006]
        assert len(hits) == 1, (c.doc, c.value, hits)
        out.append((hits[0], c.value))
    return out


def shipped_2025(target, ahi_cases="each", price_credits="order"):
    """2025 net shipments to customers by division: units (eaches) and the net value invoiced in sterling (euro at the
    2025 average rate).

    price_credits: where AHL's July price credits sit ("order": the order line each corrects; "spread": over its
    order's lines by value; "customer": over the customer's 2025 lines by value; "dropped": left out)."""
    o = B.orders(target, ahi_cases=ahi_cases)
    o = o[(o.kind == "customer") & (o.year == 2025)].copy()
    o["division"] = o["code"].map(B.division(target))
    o["gbp"] = [v * (FX_AVG_2025 if c == "EUR" else 1.0) for v, c in zip(o["value"], o["cur"])]
    units = o.groupby("division")["qty"].sum().to_dict()
    is_pc = (o["sub"] == "AHL") & (o["dtype"] == "PRICE")
    gbp = o[~is_pc].groupby("division")["gbp"].sum().to_dict()
    div = B.division(target)
    if price_credits == "order":
        for code, v in price_credit_split(o):
            gbp[div[code]] = gbp.get(div[code], 0.0) + v
    elif price_credits in ("spread", "customer"):
        a = o[(o["sub"] == "AHL") & (o["dtype"] == "DESP")]
        for c in o[is_pc].itertuples(index=False):
            ol = a[(a["doc"] == c.doc) & (a["customer"] == c.customer)] if price_credits == "spread" else \
                a[a["customer"] == c.customer]
            tot = ol["value"].sum()
            for d, v in ol.groupby("division")["value"].sum().items():
                gbp[d] = gbp.get(d, 0.0) + c.value * v / tot
    return {d: int(units.get(d, 0)) for d in DIVISIONS}, {d: float(gbp.get(d, 0.0)) for d in DIVISIONS}


FAMILY_UNITS = {"provision": 1_000_000, "inventories": 500_000, "bb": 500_000, "shortfall": 250_000}


def family(target):
    """Every defensible pairing of Valuehall's recovery (all years, each year, 2025 to 2026, non-promotion weeks, the
    January sale out), its daily rate (full stocked weeks from GBP 20,000 to 100,000 or every week, means and medians,
    part weeks by trading days, non-promotion, by year, store by store), the 2027 days (the plan's store-days or 258
    store-weeks) and the trade rate (pooled, lot by lot, lots over GBP 150,000, 2026), with the pass-2 probes at 1,390
    and 1,400 a day. Returns rows (provision, inventories, base, shortfall, label)."""
    import itertools
    g = compute(target)
    pool, gross, drawn = g["pool"], g["gross"], g["drawn"]
    w = B.vh_weeks(target)
    yr = w["week"].map(lambda d: d.year)

    def rec(m):
        return float(w[m]["sales_ex_vat"].sum() / w[m]["sales_at_cost"].sum())
    recs = {"all years": rec(w.index == w.index), "2025 to 2026": rec(yr.isin((2025, 2026))),
            "non-promotion weeks": rec(w["promotion"] == ""), "January sale out": rec(w["promotion"] != "January sale")}
    for y in range(2021, 2027):
        recs[str(y)] = rec(yr == y)
    wk = outlet_weeks(target)
    wyr = wk["week"].map(lambda d: d.year)

    def pd_(m, stat="mean"):
        v = (wk.loc[m, "sales_at_cost"] / wk.loc[m, "trading_days"]).values
        return float(np.median(v) if stat == "median" else v.mean())
    rates = {}
    for stk in (None, 20000, 25000, 30000, 35000, 40000, 50000, 60000, 80000, 100000):
        for full in (True, False):
            for stat in ("mean", "median"):
                m = wk["trading_days"] > 0
                if full:
                    m &= wk["trading_days"] == 7
                if stk is not None:
                    m &= wk["available"] >= stk
                if m.sum() >= 30:
                    rates["%s %s %s" % (stk, "full weeks" if full else "trading days", stat)] = pd_(m, stat)
    for stk in (20000, 30000, 40000):
        base = (wk["trading_days"] == 7) & (wk["available"] >= stk)
        rates["%s non-promotion" % stk] = pd_(base & (wk["promotion"] == ""))
        rates["%s January sale out" % stk] = pd_(base & (wk["promotion"] != "January sale"))
        for y in range(2021, 2027):
            if (base & (wyr == y)).sum() >= 30:
                rates["%s year %d" % (stk, y)] = pd_(base & (wyr == y))
        rates["%s store by store" % stk] = sum(pd_(base & (wk["store"] == s)) * d
                                               for s, d in B.PLAN_DAYS_2027.items()) / sum(B.PLAN_DAYS_2027.values())
    rates["probe 1,390 a day"] = 1390.0
    rates["probe 1,400 a day"] = 1400.0
    days = {"store-days": float(sum(B.PLAN_DAYS_2027.values())), "258 store-weeks": 258 * 7.0}
    l = B.lots(target)
    big = l[l["Stock at cost (GBP)"] > 150000]
    y26 = l[l["Contract date"].dt.year == 2026]
    jobs = {"pooled": float(l["Price ex VAT (GBP)"].sum() / l["Stock at cost (GBP)"].sum()),
            "lot by lot": float((l["Price ex VAT (GBP)"] / l["Stock at cost (GBP)"]).mean()),
            "lots over 150,000": float(big["Price ex VAT (GBP)"].sum() / big["Stock at cost (GBP)"].sum()),
            "2026 lots": float(y26["Price ex VAT (GBP)"].sum() / y26["Stock at cost (GBP)"].sum())}
    out = []
    for (rk, ro), (dk, rd), (dd, dv), (jk, rj) in itertools.product(recs.items(), rates.items(), days.items(),
                                                                     jobs.items()):
        cap = min(pool, rd * dv)
        prov = pool - (cap * ro + (pool - cap) * rj)
        inv = gross - prov
        out.append((prov, inv, BB_ADVANCE * inv, drawn - BB_ADVANCE * inv, (rk, dk, dd, jk)))
    return out
