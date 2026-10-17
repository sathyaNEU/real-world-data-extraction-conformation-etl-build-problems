"""The two asks from the bundle, with every stop the ask sheet names.

Ask A, the advance estimate's revision record: each quarter's growth in its advance release (that quarter on the
one before, the same release, compounded) against the latest estimates (the annual national accounts of 21 July);
graded: the September and December quarters 2025 and the March quarter 2026, and the mean revision and mean
absolute revision over the twelve quarters from June 2023.

Ask B, coal and LNG shipped to five markets: the June quarter 2026 (April and May from TBS's bulk download, June
from the bulletin's table) against the June quarter 2025 (the bulk download's months moved back to the month the
cargoes sailed, the lodgement month less one)."""
from __future__ import annotations

import numpy as np

import common as K

QUARTERS_A = K.quarter_list("2023Q2", "2026Q1")
GRADED_A = ["2025Q3", "2025Q4", "2026Q1"]
MARKETS = ["JP", "CN", "KR", "IN", "TW"]
MARKET_NAMES = {"JP": "Japan", "CN": "China", "KR": "Korea", "IN": "India", "TW": "Taiwan"}
COMMODITIES = [("32", "Coal"), ("34", "LNG")]
STALE_RELEASE = "2026Q1-T"


def prev_q(q):
    return K.prev_quarter(q)


def growth(level, q):
    return K.annualise((level[q] / level[prev_q(q)] - 1.0) * 100.0)


def db_series(B, release, series, basis="Chain"):
    return {q: v for (r, b, q, s), v in B["db"].items() if r == release and b == basis and s == series}


# ---------------------------------------------------------------------------------------------------- Ask A
def advance_growth(B, q, mix=False):
    adv = db_series(B, "%s-A" % q, "GDP")
    if mix:
        # the advance level of the quarter against the latest level of the quarter before (releases mixed)
        lat = B["latest"]["GDP"]
        return K.annualise((adv[q] / lat[prev_q(q)] - 1.0) * 100.0)
    return growth(adv, q)


def record(B, latest="annual", mix=False, sign=1.0):
    """{quarter: (advance, latest, revision)} over QUARTERS_A."""
    if latest == "annual":
        lat = B["latest"]["GDP"]
    elif latest == "stale":
        lat = db_series(B, STALE_RELEASE, "GDP")
    elif latest == "current":
        lat = None
    out = {}
    for q in QUARTERS_A:
        a = advance_growth(B, q, mix=mix)
        if latest == "current":
            l = growth(B["latest_cp"]["GDP"], q)
        else:
            l = growth(lat, q)
        out[q] = (a, l, sign * (l - a))
    return out


def ask_a(B, **kw):
    rec = record(B, **kw)
    revs = [rec[q][2] for q in QUARTERS_A]
    figs = {q: rec[q][2] for q in GRADED_A}
    figs["mean"] = float(np.mean(revs))
    figs["mar"] = float(np.mean(np.abs(revs)))
    return figs, rec


def ask_a_stops(B):
    return {
        "golden": ask_a(B)[0],
        "S1 the download's 25 June release as the latest": ask_a(B, latest="stale")[0],
        "S2 the advance growth against the latest level of the quarter before": ask_a(B, mix=True)[0],
        "S3 the annual accounts' current-price table": ask_a(B, latest="current")[0],
        "S4 revisions signed advance minus latest": ask_a(B, sign=-1.0)[0],
    }


# ---------------------------------------------------------------------------------------------------- Ask B
def bulk_value(B, month, country, div):
    v = B["bulk"].get((month, "Exports", country, div))
    return v[0] / 1000.0 if v else 0.0


def june_2026(B, country, div):
    e = B["bulletin"]["energy"].get(country, {}).get(div)
    return e[0] if e else 0.0


def quarter_2026(B, c, d):
    return bulk_value(B, "2026-04", c, d) + bulk_value(B, "2026-05", c, d) + june_2026(B, c, d)


def quarter_2025(B, c, d, shift=1):
    """The June quarter 2025's shipments: the download's months shift later (the lodgement month)."""
    months = [K.month_list("2025-01", "2025-12")[k + shift] for k in (3, 4, 5)]
    return sum(bulk_value(B, m, c, d) for m in months)


def ask_b(B, shift_coal=1, shift_lng=1):
    figs = {}
    for d, name in COMMODITIES:
        sh = shift_coal if d == "32" else shift_lng
        tot = 0.0
        for c in MARKETS:
            v = quarter_2026(B, c, d) - quarter_2025(B, c, d, shift=sh)
            figs[(c, d)] = v
            tot += v
        figs[("total", d)] = tot
    return figs


def ask_b_stops(B):
    return {
        "golden": ask_b(B),
        "S1 the download as it stands": ask_b(B, 0, 0),
        "S2 LNG moved back a month, coal left": ask_b(B, 0, 1),
        "S3 coal moved back a month, LNG left": ask_b(B, 1, 0),
        "S4 both moved back two months": ask_b(B, 2, 2),
    }


def tbs_tonnes(B, month, div):
    return sum(v[1] or 0 for (m, f, c, d), v in B["bulk"].items() if m == month and f == "Exports" and d == div)


def port_tonnes(B, month, cargo):
    return sum(t for (m, port, cg, t, n) in B["ports"] if m == month and cg == cargo)


def lag_evidence(B):
    """For each month of the download, TBS's coal and LNG tonnes against the ports' loadings in the same month and
    in the month before: the share gap (TBS over ports, less 1)."""
    out = {}
    for m in K.month_list("2023-01", "2026-05"):
        pm = K.month_list("2022-12", "2026-05")[K.month_list("2023-01", "2026-05").index(m)]
        row = {}
        for d, cargo in (("32", "Coal"), ("34", "LNG")):
            t = tbs_tonnes(B, m, d)
            row[d] = (t / port_tonnes(B, m, cargo) - 1.0, t / port_tonnes(B, pm, cargo) - 1.0)
        out[m] = row
    return out
