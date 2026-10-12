"""The asks, computed from the frames as shipped: 2027 investment income at each step, the 2027 grant payments, the
capital release at each step and the chart's title, under the golden handling and under every mishandling the ask
sheet prices."""
import datetime as dt
import itertools

import numpy as np
import pandas as pd

STEPS = [20, 30, 40, 50, 60, 70, 80, 90, 100]
GROWTH = {"MAND": 0.40, "NAEF": 0.30, "EUEF": 0.15, "JPEF": 0.15}
DEFENSIVE = {"GILT": 0.55, "CORP": 0.45}
FUND_BY_ISIN_TAIL = None
VAL = dt.date(2026, 11, 30)
INC_FROM = dt.date(2025, 12, 1)
REPORT_FROM = dt.date(2025, 11, 1)
EUR = 1.1460


def weights(step):
    s = step / 100.0
    w = {k: v * s for k, v in GROWTH.items()}
    w.update({k: v * (1 - s) for k, v in DEFENSIVE.items()})
    return w


def ukdate(s):
    return dt.datetime.strptime(s, "%d/%m/%Y").date()


class Pack:
    """the frames an ask reads: val (the 30 November valuation rows), ent, static, kest {fund: frame}, kest_isins
    {fund: (inc, acc)}, reg, inst, pays, running, capital"""

    def __init__(self, **kw):
        self.__dict__.update(kw)


def fund_map(P):
    """custodian security code -> holding, through the static data's ISIN and Kestwick's sheets"""
    isin = dict(zip(P.static["security_code"], P.static["isin"]))
    by_isin = {}
    for f, (i, a) in P.kest_isins.items():
        by_isin[i] = (f, "inc")
        by_isin[a] = (f, "acc")
    return {c: by_isin[v] for c, v in isin.items() if v in by_isin}


def income(P, lines="position", months=12, route="history", accrued_in=False, wts=weights):
    v = P.val
    fm = fund_map(P)
    eq = v["asset_class"].isin(["Equity - UK", "Cash", "Rights"])
    mand_mv = float(v.loc[eq, "market_value_gbp"].sum())
    if accrued_in:
        mand_mv += float(v.loc[eq, "accrued_income_gbp"].sum())
    fund_mv = {}
    for c, mv in zip(v["security_code"], v["market_value_gbp"]):
        if c in fm:
            fund_mv[fm[c][0]] = fund_mv.get(fm[c][0], 0.0) + float(mv)
    total = mand_mv + sum(fund_mv.values())
    if accrued_in:
        total += 0.0
    start = INC_FROM if months == 12 else REPORT_FROM
    e = P.ent
    e = e[(e["ex_date"] >= start.isoformat()) & (e["ex_date"] <= VAL.isoformat())]
    em = e[~e["security_code"].isin(list(fm))]
    if lines == "position":
        em = em.drop_duplicates(["sub_account", "security_code", "event_ref"])
    elif lines == "o1":
        em = em.drop_duplicates(["sub_account", "security_code", "ex_date"])
    elif lines == "o1_last":
        em = em.drop_duplicates(["sub_account", "security_code", "ex_date"], keep="last")
    elif lines == "o2":
        em = em.drop_duplicates(["security_code", "event_ref"])
    y = {"MAND": float(em["entitlement_gbp"].sum()) / mand_mv}
    for f in DEFENSIVE.keys() | GROWTH.keys():
        if f == "MAND":
            continue
        if route == "history":
            k = P.kest[f]
            d = k["Date"]
            sel = (d >= INC_FROM) & (d <= VAL)
            dist = float(k.loc[sel, "Distribution per income unit (GBP)"].fillna(0).sum())
            px = float(k.loc[d == VAL, "Income units (GBP)"].iloc[0])
            y[f] = dist / px
        else:
            ef = e[e["security_code"].isin([c for c, (ff, _) in fm.items() if ff == f])]
            y[f] = float(ef["entitlement_gbp"].sum()) / fund_mv[f]
    inc = {s: total * sum(w * y[h] for h, w in wts(s).items()) for s in STEPS}
    return inc, dict(total=total, mand_mv=mand_mv, fund_mv=fund_mv, yields=y)


def instalment_kinds(P):
    reg = P.reg.set_index("grant_ref")
    kinds = []
    for ref, no in zip(P.inst["grant_ref"], P.inst["instalment_no"]):
        if reg.loc[ref, "grant_type"] == "Core":
            kinds.append("core")
        elif no == 1:
            kinds.append("first")
        else:
            kinds.append("later")
    return kinds


def history_lags(P):
    """days from due date to payment for project grants' later instalments, from the payment ledger"""
    i = P.inst.copy()
    i["kind"] = instalment_kinds(P)
    m = P.pays.merge(i, on=["grant_ref", "instalment_no"])
    m["lag"] = [(dt.date.fromisoformat(a) - ukdate(b)).days for a, b in zip(m["payment_date"], m["due_date"])]
    return {k: sorted(m.loc[m["kind"] == k, "lag"]) for k in ("core", "first", "later")}


def grant_payments(P, clock=True, lag=50, withdrawn_out=True, convert=True, lag_all=False, year=2027):
    reg = P.reg.set_index("grant_ref")
    total = 0.0
    parts = dict(core_first=0.0, later=0.0, euro_gbp=0.0, withdrawn=0.0)
    for (ref, no, due, amt, st), kind in zip(P.inst[["grant_ref", "instalment_no", "due_date", "amount", "status"]].itertuples(index=False),
                                             instalment_kinds(P)):
        if st != "Scheduled":
            continue
        g = reg.loc[ref]
        d = ukdate(due)
        if lag_all or (clock and kind == "later"):
            d = d + dt.timedelta(days=lag)
        if d.year != year:
            continue
        if g["status"] == "Withdrawn":
            parts["withdrawn"] += float(amt) / (EUR if g["currency"] == "EUR" and convert else 1.0)
            if withdrawn_out:
                continue
        a = float(amt)
        if g["currency"] == "EUR" and convert:
            a = a / EUR
            parts["euro_gbp"] += a
        total += a
        parts["later" if kind == "later" else "core_first"] += a
    return total, parts


def release(P, inc, grants, running):
    return {s: grants + running - inc[s] for s in STEPS}


def title(inc, grants):
    ok = [s for s in STEPS if inc[s] >= grants]
    return max(ok) if ok else None


def r1000(x):
    return int(np.floor(x / 1000.0 + 0.5)) * 1000


# ------------------------------------------------------------------------------------------------ every stop

INCOME_VARIANTS = dict(lines=["position", "lines", "o1", "o1_last", "o2"], months=[12, 13], route=["history", "extract"],
                       accrued_in=[False])


def all_stops(P, running, capital_total):
    """every combination of the priced mishandlings: {label: (incomes, grants, releases, title)}"""
    lags = list(range(35, 71))
    inc_cache = {}
    for lines, months, route, acc in itertools.product(*INCOME_VARIANTS.values()):
        inc_cache[(lines, months, route, acc)] = income(P, lines, months, route, acc)[0]
    gr = {}
    for clock, wout, conv in itertools.product([True, False], [True, False], [True, False]):
        gr[("clock" if clock else "due", wout, conv, None)] = grant_payments(P, clock, 50, wout, conv)[0]
        if clock:
            for L in (35, 50, 70):
                gr[("lag_all", wout, conv, L)] = grant_payments(P, True, L, wout, conv, lag_all=True)[0]
    out = {}
    for ik, inc in inc_cache.items():
        for gk, g in gr.items():
            for fees in (False, True):
                R = running + (capital_total if fees else 0.0)
                rel = release(P, inc, g, R)
                out[(ik, gk, fees)] = (inc, g, rel, title(inc, g))
    return out
