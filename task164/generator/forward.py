"""Panel states, the family of increment estimators, the forward fleet (registrations, departures and the winter
EV-rate enrollment drive, October 2026 to March 2027), every transformer's forecast and the allocation.

The forward events are placed clear of the line: a registration, departure or rate move that would leave a
transformer's forecast within DELTA kVA of 1.2 times nameplate under any member of the estimator family, or on
different sides of it under two members, is redrawn. The district counts are then steered, by moving a few forward
default-rate registrations between transformers that cross and transformers that do not, until every district's
proportional share sits clear of the largest-remainder cut."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as K
import world as W

DELTA = 0.20
MIN_CELL = 40


# ------------------------------------------------------------------------------------------------- states
def states_at(tx, veh, sw, pr_base, dates):
    """(TOU count, EV count) per transformer at a per-transformer date (Series aligned to tx) or a single date."""
    if not isinstance(dates, pd.Series):
        dates = pd.Series(pd.Timestamp(dates), index=tx.index)
    m = veh[["pi", "ti", "reg", "dep"]].copy()
    m["day"] = m["ti"].map(dict(zip(tx["ti"], dates)))
    pres = (m["reg"] <= m["day"]) & (m["dep"].isna() | (m["dep"] > m["day"]))
    s = m["pi"].map(sw)
    flat = m["pi"].map(lambda p: pr_base[p] == K.RATE_FLAT)
    ev = s.notna() & (s <= m["day"]) & ~flat
    k = m[pres & ~ev].groupby("ti").size()
    e = m[pres & ev].groupby("ti").size()
    return (tx["ti"].map(k).fillna(0).astype(int).values, tx["ti"].map(e).fillna(0).astype(int).values)


def panel_states(tx, veh, sw, pr_base):
    for y in K.SUMMERS:
        tx["k%d" % y], tx["e%d" % y] = states_at(tx, veh, sw, pr_base, W.peak_date(tx, y))
    return tx


# ------------------------------------------------------------------------------------------------- estimators
def transitions(tx, years=((2024, 2025), (2025, 2026))):
    rows = []
    for y0, y1 in years:
        dk = tx["k%d" % y1] - tx["k%d" % y0]
        de = tx["e%d" % y1] - tx["e%d" % y0]
        same = (dk == 0) & (de == 0)
        ratio = (tx["pk%d" % y1] / tx["pk%d" % y0])[same].groupby(tx["district"][same]).median()
        addm = (tx["pk%d" % y1] - tx["pk%d" % y0])[same].groupby(tx["district"][same]).mean()
        rows.append(pd.DataFrame({
            "y": y1, "ti": tx["ti"], "district": tx["district"], "sg": tx["sg"], "kva": tx["kva"],
            "k0": tx["k%d" % y0], "e0": tx["e%d" % y0], "dk": dk, "de": de,
            "adj": tx["pk%d" % y1] - tx["district"].map(ratio) * tx["pk%d" % y0],
            "add": tx["pk%d" % y1] - tx["pk%d" % y0] - tx["district"].map(addm),
            "raw": tx["pk%d" % y1] - tx["pk%d" % y0]}))
    return pd.concat(rows, ignore_index=True)


def table(P, col="adj", by_size=True, by_pos=True, ev_by_k=False):
    """TOU increments by (size group, position 1, 2, 3+) and the EV increment (constant, or split on whether the
    transformer already carried a TOU vehicle)."""
    t = P[(P.dk == 1) & (P.de == 0)]
    out = {}
    for sg in ("S", "M", "L"):
        for pos in (1, 2, 3):
            sel = t
            if by_size:
                sel = sel[sel.sg == sg]
            if by_pos:
                cell = sel[(sel.k0.clip(upper=2) + 1) == pos]
                # a cell with too few transitions to estimate takes the position's value pooled across sizes
                sel = cell if len(cell) >= MIN_CELL else t[(t.k0.clip(upper=2) + 1) == pos]
            out[(sg, pos)] = float(sel[col].mean())
    e = P[(P.de == 1) & (P.dk == 0)]
    if ev_by_k:
        ev = {0: float(e[e.k0 == 0][col].mean()), 1: float(e[e.k0 > 0][col].mean())}
    else:
        ev = {0: float(e[col].mean()), 1: float(e[col].mean())}
    return {"tou": out, "ev": ev}


def ols_table(P):
    sel = P[(P.dk >= 0) & (P.de >= 0) & ((P.dk + P.de) > 0) | ((P.dk == 0) & (P.de == 0))]
    X = np.c_[sel.dk.values, sel.de.values].astype(float)
    b = np.linalg.lstsq(X, sel["adj"].values, rcond=None)[0]
    return {"tou": {(sg, p): float(b[0]) for sg in "SML" for p in (1, 2, 3)}, "ev": {0: float(b[1]), 1: float(b[1])}}


def cross_section_table(tx):
    """2026 recorded peaks on the vehicles present at the peak, within district, kVA rating and premises served."""
    d = tx.copy()
    cell = d["district"] + "/" + d["kva"].astype(str) + "/" + d["n_prem"].astype(str)
    d["res"] = d["pk2026"] - d.groupby(cell)["pk2026"].transform("mean")
    d["kc"] = d["k2026"] - d.groupby(cell)["k2026"].transform("mean")
    d["ec"] = d["e2026"] - d.groupby(cell)["e2026"].transform("mean")
    X = np.c_[d.kc.values, d.ec.values]
    b = np.linalg.lstsq(X, d.res.values, rcond=None)[0]
    return {"tou": {(sg, p): float(b[0]) for sg in "SML" for p in (1, 2, 3)}, "ev": {0: float(b[1]), 1: float(b[1])}}


def family(tx, rate_code=None):
    P = transitions(tx)
    P26 = P[P.y == 2026]
    fam = {
        "size x position": table(P),
        "size only": table(P, by_pos=False),
        "position only": table(P, by_size=False),
        "pooled by rate": table(P, by_size=False, by_pos=False),
        "additive weather": table(P, "add"),
        "no weather adjustment": table(P, "raw"),
        "2025 to 2026 only": table(P26),
        "EV increment by TOU present": table(P, ev_by_k=True),
        "least squares on vehicles added": ols_table(P),
        "2026 cross-section": cross_section_table(tx),
    }
    return fam, P


GOLD = "size x position"


def F(tab, sg, k, e):
    tou = tab["tou"]
    s = 0.0
    for i in range(1, int(k) + 1):
        s += tou[(sg, min(i, 3))]
    if e > 0:
        s += tab["ev"][0] if k == 0 else tab["ev"][1]
        s += (e - 1) * tab["ev"][1]
    return s


def forecast(tab, sg, k0, e0, k1, e1, p26):
    return p26 + F(tab, sg, k1, e1) - F(tab, sg, k0, e0)


def margins(fam, row, k1, e1):
    return np.array([forecast(t, row["sg"], row["k2026"], row["e2026"], k1, e1, row["pk2026"]) - K.THRESH * row["kva"]
                     for t in fam.values()])


def clear(ms, delta=DELTA):
    return bool(np.all(ms > delta) or np.all(ms < -delta))


# ------------------------------------------------------------------------------------------------- allocation
def allocate(counts, total=K.TOTAL):
    """Largest remainder: whole parts first, the rest one each by fractional part (ties to the larger count)."""
    c = pd.Series(counts, dtype=float)
    q = total * c / c.sum()
    fl = np.floor(q)
    rem = q - fl
    order = sorted(c.index, key=lambda d: (-rem[d], -c[d]))
    out = fl.astype(int).copy()
    for d in order[: int(total - fl.sum())]:
        out[d] += 1
    return out, q
