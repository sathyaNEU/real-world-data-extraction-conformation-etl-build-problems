"""The call's inputs as a solver builds them from the pack: each holding's daily total return on UK business days, under
the default handling or under any Layer 1 slip, and the benchmark indices' daily returns."""
import datetime as dt

import numpy as np
import pandas as pd

HOLD = ["MAND", "NAEF", "EUEF", "JPEF", "GILT", "CORP"]
MAND_CLASSES = ("Equity - UK", "Cash", "Rights")
WIN_FROM = "2024-11-29"
VAL = "2026-11-30"


def mandate_values(val, sub=None, cash=True, accrued=True, carry=None):
    v = val[val["asset_class"].isin(MAND_CLASSES)]
    if sub:
        v = v[v["sub_account"] == sub]
    if not cash:
        v = v[v["asset_class"] != "Cash"]
    tot = v.groupby("valuation_date")["market_value_gbp"].sum()
    if accrued:
        tot = tot + v.groupby("valuation_date")["accrued_income_gbp"].sum()
    if carry is not None:
        for d, amt in carry.items():
            tot.loc[d] += amt
    return tot.sort_index()


def demerger_carry(val, events, sub=None):
    """the demerged shares valued on the parent's ex-date at their first price"""
    e = events[events["action_type"] == "SOFF"].iloc[0]
    v = val[(val["security_code"] == e["new_security_code"]) & (val["valuation_date"] == e["effective_date"])]
    if sub:
        v = v[v["sub_account"] == sub]
    return {e["ex_date"]: float(v["market_value_gbp"].sum())}


def mandate_returns(val, moves, events, sub=None, flows_in=False, cash=True, accrued=True, carry=True):
    c = demerger_carry(val, events, sub) if carry else None
    V = mandate_values(val, sub, cash, accrued, c)
    m = moves[moves["movement_type"].isin(["Contribution", "Withdrawal"])]
    if sub:
        m = m[m["sub_account"] == sub]
    F = m.groupby("date")["amount_gbp"].sum()
    F = F.reindex(V.index).fillna(0.0)
    if flows_in:
        F = F * 0.0
    r = (V.values[1:] - F.values[1:]) / V.values[:-1] - 1
    return pd.Series(r, index=V.index[1:])


def fund_returns(kest, dates, dist_out=False, unit="inc"):
    out = {}
    for f, df in kest.items():
        d = df.set_index("Date")
        if unit == "acc":
            p = d["Accumulation units (GBP)"].astype(float)
            r = p.values[1:] / p.values[:-1] - 1
        else:
            p = d["Income units (GBP)"].astype(float)
            q = d["Distribution per income unit (GBP)"].fillna(0).astype(float)
            r = ((p.values[1:] + (0 if dist_out else q.values[1:])) / p.values[:-1]) - 1
        s = pd.Series(r, index=[x.isoformat() for x in d.index[1:]])
        out[f] = s.reindex(dates)
    return out


def matrix(val, moves, events, kest, **kw):
    """the six holdings' daily returns, ordered MAND NAEF EUEF JPEF GILT CORP, and the dates"""
    mk = {k: kw[k] for k in ("sub", "flows_in", "cash", "accrued", "carry") if k in kw}
    rm = mandate_returns(val, moves, events, **mk)
    dates = list(rm.index)
    fr = fund_returns(kest, dates, kw.get("dist_out", False), kw.get("unit", "inc"))
    X = np.column_stack([rm.values] + [fr[f].values for f in HOLD[1:]])
    assert not np.isnan(X).any(), "a holding has no return on a UK business day"
    return X, [dt.date.fromisoformat(d) for d in dates]


def post_holiday_rows(cal, dates):
    """UK business days whose North American or Japan fund price carries no new close of its market"""
    bd = {}
    for m, sub in cal.groupby("market"):
        bd[m] = set(sub.loc[sub["is_business_day"] == "Y", "date"])
    out = []
    prev = dt.date(2024, 11, 29)
    for k, d in enumerate(dates):
        span = [prev + dt.timedelta(days=j) for j in range(0, (d - prev).days)]       # prev .. d-1 (New York)
        us_new = any(x.isoformat() in bd["New York"] for x in span)
        span_jp = [prev + dt.timedelta(days=j) for j in range(1, (d - prev).days + 1)]  # prev+1 .. d (Tokyo)
        jp_new = any(x.isoformat() in bd["Tokyo"] for x in span_jp)
        if not us_new or not jp_new:
            out.append(k)
        prev = d
    return out


def index_matrix(index, dates):
    names = ["FTSE All-Share", "S&P 500", "FTSE World Europe ex UK", "TOPIX",
             "FTSE Actuaries UK Conventional Gilts All Stocks", "iBoxx GBP Non-Gilts"]
    cols = []
    ds = [WIN_FROM] + [d.isoformat() for d in dates]
    for nm in names:
        s = index[index["index_name"] == nm].set_index("date")["close"].sort_index()
        lv = s.reindex(sorted(set(s.index) | set(ds))).ffill().reindex(ds).values
        cols.append(lv[1:] / lv[:-1] - 1)
    return np.column_stack(cols)
