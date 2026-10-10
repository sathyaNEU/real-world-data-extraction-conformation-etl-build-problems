"""task127 generator: the households, the pilot and the feeders.

The survey is built as weighted cells per neighbourhood, then split into sample records with integer
weights, so the weighted joint counts are exact and the published tables are computed from the records.
The pilot log is built from unit blocks of qualifying households per heating system, so every pilot
neighbourhood's installs follow the same rate per system.
"""
from datetime import date, timedelta

import numpy as np
import pandas as pd

import params as P

TWINS = {("NS", "Elm Park"): ("VA", "Birch Hollow"), ("LA", "Loon Point"): ("RB", "Sauk Flats")}
TWIN_PROFILE = dict(other=0.35, outband=0.30, mobile=0.20, rent_det=0.20, multi=0.08)
OTHER_FUELS = {"NG": 0.40, "FO": 0.14, "WD": 0.24, "HP": 0.12, "OT": 0.10}
PE_MIX = {"PF": 0.55, "ER": 0.30, "PB": 0.15}


def pilot_qual(c):
    u = P.PILOT_UNITS[c]
    return tuple(u[i] * P.UNIT[s][0] for i, s in enumerate(P.SYS))


def _split(n, shares):
    """Integer split of n by shares, largest remainder."""
    keys = list(shares)
    raw = np.array([shares[k] for k in keys], float) * n / sum(shares.values())
    base = np.floor(raw).astype(int)
    left = n - base.sum()
    order = np.argsort(-(raw - base), kind="stable")
    base[order[:left]] += 1
    return dict(zip(keys, base.tolist()))


def nbhd_cells(c, nb, q, prof, pilot=False):
    """Weighted household counts for one neighbourhood: list of (system, tenure, structure, income, n)."""
    cells = []
    det, mob, att = P.STRUCT
    lo, hi = P.IN_BAND
    for i, s in enumerate(P.SYS):
        code = P.SYS_CODE[s]
        if pilot:
            units = P.PILOT_UNITS[c][i]
            ulo = units * 2 // 5 if units > 1 else 0
            cells.append((code, "owner", det, lo, ulo * P.UNIT[s][0]))
            cells.append((code, "owner", det, hi, (units - ulo) * P.UNIT[s][0]))
        else:
            nlo = int(round(q[i] * 0.44))
            cells.append((code, "owner", det, lo, nlo))
            cells.append((code, "owner", det, hi, q[i] - nlo))
    Q = sum(q)
    other = _split(int(round(prof["other"] * Q)), OTHER_FUELS)
    for code, n in other.items():
        cells.append((code, "owner", det, lo, n * 45 // 100))
        cells.append((code, "owner", det, hi, n - n * 45 // 100))
    ob = _split(int(round(prof["outband"] * Q)), PE_MIX)
    for code, n in ob.items():
        cells.append((code, "owner", det, P.INCOME[0], n * 55 // 100))
        cells.append((code, "owner", det, P.INCOME[3], n - n * 55 // 100))
    mo = _split(int(round(prof["mobile"] * Q)), {"PF": 0.6, "ER": 0.4})
    for code, n in mo.items():
        cells.append((code, "owner", mob, lo, n * 70 // 100))
        cells.append((code, "owner", mob, hi, n - n * 70 // 100))
    rd = _split(int(round(prof["rent_det"] * Q)), {"PF": 0.45, "ER": 0.40, "PB": 0.15})
    for code, n in rd.items():
        cells.append((code, "renter", det, lo, n * 65 // 100))
        cells.append((code, "renter", det, hi, n - n * 65 // 100))
    m = int(round(prof["multi"] * Q))
    cells.append(("NG", "renter", att, P.INCOME[0], m * 70 // 100))
    cells.append(("NG", "renter", att, P.INCOME[3], m - m * 70 // 100))
    return [x for x in cells if x[4] > 0]


def all_cells():
    out = {}
    twin_b = {v: k for k, v in TWINS.items()}
    for c in P.COOPS:
        out[(c, P.PILOT_NBHD[c])] = nbhd_cells(c, P.PILOT_NBHD[c], pilot_qual(c), P.PROFILE[c], pilot=True)
        for nb, q in P.QUAL[c].items():
            key = (c, nb)
            if key in TWINS or key in twin_b:
                out[key] = nbhd_cells(c, nb, q, TWIN_PROFILE)
            else:
                out[key] = nbhd_cells(c, nb, q, P.PROFILE[c])
    return out


# ------------------------------------------------------------------ survey sample records

YEAR_BUILT = ["before 1960", "1960 to 1979", "1980 to 1999", "2000 or later"]


def survey_records(cells):
    """Split each weighted cell into sample records with integer weights."""
    rows = []
    twin_b = {v: k for k, v in TWINS.items()}
    made = {}
    for (c, nb) in sorted(cells, key=lambda k: (P.COOPS.index(k[0]), k[1])):
        src = twin_b.get((c, nb))
        if src is not None and src in made:
            for r in made[src]:
                rows.append(dict(r, coop=c, neighbourhood=nb))
            continue
        g = P.rng("survey|" + nb)
        recs = []
        for code, ten, st, inc, n in cells[(c, nb)]:
            target = 9.0 if ten == "renter" else (14.0 if st != P.STRUCT[0] else 24.0)
            k = max(1, int(round(n / target)))
            k = min(k, n)
            cuts = np.sort(g.choice(np.arange(1, n), size=k - 1, replace=False)) if k > 1 else np.array([], int)
            w = np.diff(np.concatenate([[0], cuts, [n]]))
            for wi in w:
                recs.append(dict(coop=c, neighbourhood=nb, heating_system=code, tenure=ten, structure=st,
                                 income_band=inc, year_built=YEAR_BUILT[int(g.integers(0, 4))],
                                 bedrooms=int(g.choice([1, 2, 3, 4, 5], p=[.06, .24, .40, .23, .07])),
                                 weight=int(wi)))
        made[(c, nb)] = recs
        rows += recs
    df = pd.DataFrame(rows)
    g = P.rng("survey-order")
    df = df.iloc[g.permutation(len(df))].reset_index(drop=True)
    # case numbers follow the fieldwork order inside each co-op
    df["_k"] = df.coop.map(P.COOPS.index)
    df = df.sort_values(["_k"], kind="stable").reset_index(drop=True)
    base = {c: 100000 + 20000 * i for i, c in enumerate(P.COOPS)}
    seq = df.groupby("coop").cumcount()
    df["case_id"] = [f"HS25-{base[c] + 7 * int(s) + 3:06d}" for c, s in zip(df.coop, seq)]
    cols = ["case_id", "coop", "neighbourhood", "heating_system", "tenure", "structure", "income_band",
            "year_built", "bedrooms", "weight"]
    return df[cols]


PUB_FUELS = ["utility gas", "bottled, tank or LP gas", "electricity", "fuel oil, kerosene", "wood",
             "other fuel or none"]


def published_tables(sv):
    """Tables H1 to H4 by co-op, weighted, from the sample records."""
    sv = sv.assign(fuel=sv.heating_system.map(lambda x: P.FUEL_SURVEY[x][1]))
    h1 = sv.pivot_table(index="coop", columns="fuel", values="weight", aggfunc="sum", fill_value=0)
    h1 = h1.reindex(index=P.COOPS, columns=PUB_FUELS, fill_value=0)
    h2 = sv.pivot_table(index=["coop", "tenure"], columns="fuel", values="weight", aggfunc="sum", fill_value=0)
    h2 = h2.reindex(columns=PUB_FUELS, fill_value=0)
    h3 = sv.pivot_table(index=["coop", "tenure"], columns="structure", values="weight", aggfunc="sum", fill_value=0)
    h3 = h3.reindex(columns=P.STRUCT, fill_value=0)
    h4 = sv.pivot_table(index="coop", columns="income_band", values="weight", aggfunc="sum", fill_value=0)
    h4 = h4.reindex(index=P.COOPS, columns=P.INCOME, fill_value=0)
    return h1, h2, h3, h4


# ------------------------------------------------------------------ feeders and the map

def feeder_frames():
    fr, mp = [], []
    for c in P.COOPS:
        for f, sub, kw, nbs in P.FEEDERS[c]:
            fr.append(dict(coop=c, feeder=f, substation=sub, headroom_kw=kw))
            for nb in nbs:
                mp.append(dict(coop=c, neighbourhood=nb, feeder=f))
    return pd.DataFrame(fr), pd.DataFrame(mp)


# ------------------------------------------------------------------ the pilot installs (dates set later)

def pilot_installs():
    """One row per pilot install: co-op, neighbourhood, system, income band, season."""
    rows = []
    for c in P.COOPS:
        nb = P.PILOT_NBHD[c]
        for i, s in enumerate(P.SYS):
            units = P.PILOT_UNITS[c][i]
            ulo = units * 2 // 5 if units > 1 else 0
            per = P.UNIT[s][1]
            for inc, u in ((P.IN_BAND[0], ulo), (P.IN_BAND[1], units - ulo)):
                for _ in range(u * per):
                    rows.append(dict(coop=c, neighbourhood=nb, sys=s, income_band=inc))
    df = pd.DataFrame(rows)
    assert all((df.coop == c).sum() == P.PILOT_INSTALLS[c] for c in P.COOPS)
    g = P.rng("pilot-season")
    season = np.empty(len(df), object)
    for c in P.COOPS:
        idx = np.flatnonzero(df.coop.to_numpy() == c)
        k = P.PILOT_INSTALLS[c] // 4
        pick = g.permutation(idx)
        season[pick[:k]] = "spring"
        season[pick[k:]] = "autumn"
    df["season"] = season
    return df


def workdays(start, end, holidays, four_day=False):
    d, out = start, []
    while d <= end:
        wd = d.weekday()
        if wd < (4 if four_day else 5) and d not in holidays:
            out.append(d)
        d += timedelta(days=1)
    return out


def holidays(year):
    def nth(month, weekday, n):
        d = date(year, month, 1)
        while d.weekday() != weekday:
            d += timedelta(days=1)
        return d + timedelta(days=7 * (n - 1))

    def last(month, weekday):
        d = date(year, month + 1, 1) - timedelta(days=1)
        while d.weekday() != weekday:
            d -= timedelta(days=1)
        return d

    def observed(d):
        return d - timedelta(days=1) if d.weekday() == 5 else (d + timedelta(days=1) if d.weekday() == 6 else d)

    tg = nth(11, 3, 4)
    return {observed(date(year, 1, 1)), last(5, 0), observed(date(year, 7, 4)), nth(9, 0, 1), tg,
            tg + timedelta(days=1), observed(date(year, 12, 25))}
