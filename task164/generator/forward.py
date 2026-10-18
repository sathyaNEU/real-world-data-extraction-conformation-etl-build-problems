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


def const_table(t, e):
    """One figure for every default-rate vehicle and one for every R-EV2 vehicle (OP 4's granularity)."""
    return {"tou": {(sg, p): float(t) for sg in "SML" for p in (1, 2, 3)}, "ev": {0: float(e), 1: float(e)}}


def pooled(P, col="adj"):
    """The mean rise over the transitions that added exactly one vehicle on the schedule and nothing else."""
    return const_table(P[(P.dk == 1) & (P.de == 0)][col].mean(), P[(P.de == 1) & (P.dk == 0)][col].mean())


def one_or_two(P, col="adj"):
    """The rise per vehicle over the transitions that added one or two vehicles on the schedule and nothing else."""
    t = pd.concat([P[(P.dk == 1) & (P.de == 0)][col], P[(P.dk == 2) & (P.de == 0)][col] / 2])
    e = pd.concat([P[(P.de == 1) & (P.dk == 0)][col], P[(P.de == 2) & (P.dk == 0)][col] / 2])
    return const_table(t.mean(), e.mean())


def ols(P, col="adj", fe=None, added_only=True):
    """Least squares of the change in recorded peak on the vehicles added on each schedule, with group effects swept
    out where given."""
    sel = P[(P.dk >= 0) & (P.de >= 0)] if added_only else P
    y = sel[col].values.astype(float)
    X = np.c_[sel.dk.values, sel.de.values].astype(float)
    if fe is not None:
        g = np.asarray(fe(sel))
        y = y - pd.Series(y).groupby(g).transform("mean").values
        X = X - pd.DataFrame(X).groupby(g).transform("mean").values
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return const_table(b[0], b[1])


def cross_section_table(tx):
    """2026 recorded peaks on the vehicles present at the peak, within district, kVA rating and premises served."""
    d = tx.copy()
    cell = d["district"] + "/" + d["kva"].astype(str) + "/" + d["n_prem"].astype(str)
    d["res"] = d["pk2026"] - d.groupby(cell)["pk2026"].transform("mean")
    d["kc"] = d["k2026"] - d.groupby(cell)["k2026"].transform("mean")
    d["ec"] = d["e2026"] - d.groupby(cell)["e2026"].transform("mean")
    X = np.c_[d.kc.values, d.ec.values]
    b = np.linalg.lstsq(X, d.res.values, rcond=None)[0]
    return const_table(b[0], b[1])


def family(tx, rate_code=None):
    """Every defensible estimate of OP 4's per-schedule expected effect from the recorded peaks."""
    P = transitions(tx)
    fam = {
        "pooled by schedule": pooled(P),
        "pooled, 2024 to 2025": pooled(P[P.y == 2025]),
        "pooled, 2025 to 2026": pooled(P[P.y == 2026]),
        "pooled, additive weather": pooled(P, "add"),
        "pooled, no weather adjustment": pooled(P, "raw"),
        "one or two added, per vehicle": one_or_two(P),
        "least squares, weather-adjusted": ols(P, "adj"),
        "least squares, district and year effects": ols(P, "raw", fe=lambda s: s.district + "/" + s.y.astype(str)),
        "least squares, year effects": ols(P, "raw", fe=lambda s: s.y),
        "least squares, every change": ols(P, "adj", added_only=False),
        "2026 cross-section": cross_section_table(tx),
    }
    return fam, P


GOLD = "pooled by schedule"


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
