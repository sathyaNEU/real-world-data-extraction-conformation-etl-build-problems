"""The estimates computed from the shipped files alone: the dwelling stock on any date rebuilt from the roll, the
certificates of occupancy and the demolitions; the 2020 block groups; and every rung of the ladder, the golden's
family and the backcasts that separate them."""
import datetime as dt
import functools
import os

import numpy as np
import pandas as pd

import world as W

TYPES = ("SF", "TH", "AP", "MH")
LU_TYPE = {"1010": "SF", "1020": "TH", "1030": "TH", "1050": "AP", "1080": "MH"}
CO_TYPE = {"Single-family dwelling": "SF", "Two-family dwelling": "TH", "Townhouse unit": "TH",
           "Multi-family dwelling": "AP", "Manufactured home": "MH"}
NAME_OF_NO = {"002": "Town of Ashgrove", "006": "Town of Cedar Run", "010": "Town of Elk Prairie",
              "012": "Town of Glenmoor", "014": "Town of Harwick", "016": "Town of Kessler", "018": "Town of Maple Ford",
              "020": "Town of Northfield", "106": "Village of Barrow", "116": "Village of Fallon",
              "131": "Village of Ivydale", "146": "Village of Lorne", "221": "City of Dunmore", "241": "City of Juniper"}
AGEB = [(0, 5), (5, 10), (10, 15), (15, 20), (20, 30), (30, 40), (40, 60), (60, 999)]
BANDS = {"age": AGEB,
         "age10": [(0, 10), (10, 20), (20, 30), (30, 50), (50, 999)],
         "age5": [(0, 5), (5, 10), (10, 15), (15, 20), (20, 25), (25, 30), (30, 35), (35, 40), (40, 50), (50, 70), (70, 999)],
         "age3": [(0, 3), (3, 6), (6, 9), (9, 12), (12, 16), (16, 20), (20, 25), (25, 32), (32, 40), (40, 55), (55, 999)]}
VINTAGE = [(2010, 2021), (2000, 2010), (1990, 2000), (1980, 1990), (1960, 1980), (0, 1960)]


def yf(d):
    d = pd.to_datetime(d)
    y0 = pd.to_datetime(d.dt.year.astype(str) + "-01-01")
    y1 = pd.to_datetime((d.dt.year + 1).astype(str) + "-01-01")
    return d.dt.year + (d - y0).dt.days / (y1 - y0).dt.days


def xf(date):
    y0 = dt.date(date.year, 1, 1)
    return date.year + (date - y0).days / (dt.date(date.year + 1, 1, 1) - y0).days


@functools.lru_cache(maxsize=None)
def load(t):
    f = lambda k: os.path.join(t, W.FILES[k])
    roll = pd.read_csv(f("roll"), dtype=str)
    cos = pd.read_csv(f("cos"), dtype=str)
    demo = pd.read_csv(f("demo"), dtype=str)
    bg = pd.read_csv(f("bg2020"), dtype=str, skiprows=[1])
    hist = {y: pd.read_excel(f("history"), sheet_name=str(y), header=3, dtype={"FIPS code": str}) for y in (2000, 2010, 2020)}
    bnd = pd.read_csv(f("boundary"), dtype=str)
    gq = pd.read_excel(f("gq"), sheet_name=0, header=3)
    return roll, cos, demo, bg, hist, bnd, gq


@functools.lru_cache(maxsize=None)
def stock(t, opts=()):
    """every dwelling unit the files know: the roll's units, the 2026 certificates' new units, and the demolished
    units; each with its municipality now, its type, its completion (decimal year), its demolition and its 2020
    block group"""
    roll, cos, demo, bg, hist, bnd, gq = load(t)
    roll = roll.copy()
    roll["units"] = roll["LIVING_UNITS"].astype(int)
    res = cos[cos["USE"].isin(list(CO_TYPE)) & (cos["NEW_DWELLING_UNITS"].astype(int) > 0)].copy()
    res["when"] = yf(res["ISSUED"])
    if "final_only" in opts:
        res = res[res["CO_TYPE"] == "Final"]
    first = res.sort_values(["when", "CO_NO"]).drop_duplicates("TAXKEY")
    mid = 0.0 if "year_start" in opts else (1.0 if "year_end" in opts else 0.5)
    comp_of = dict(zip(first["TAXKEY"], first["when"]))
    have = roll[roll["units"] > 0].copy()
    yb = have["YEAR_BUILT"].astype(int)
    have["comp"] = [comp_of.get(k, (y if y > 0 else 1900) + mid) for k, y in zip(have["TAXKEY"], yb)]
    if "drop_year0" in opts:
        have = have[yb.values > 0]
    have["type"] = have["LAND_USE"].map(LU_TYPE)
    have["muni"] = have["MUNI_NO"].map(NAME_OF_NO)
    have["bg"] = have["CENSUS_BLOCK_2020"].str[:12]
    rows = [have[["TAXKEY", "muni", "type", "comp", "bg", "units"]]]
    # dwellings finished in 2026: certificates after the roll date on lots the roll holds as vacant land
    vacant = roll[roll["units"] == 0].set_index("TAXKEY")
    new = first[(first["when"] >= xf(W.ROLL)) & first["TAXKEY"].isin(vacant.index)].copy()
    if "no_2026" in opts:
        new = new.iloc[0:0]
    new["muni"] = new["TAXKEY"].str[:3].map(NAME_OF_NO)
    new["type"] = new["USE"].map(CO_TYPE)
    new["comp"] = new["when"]
    new["bg"] = vacant.loc[new["TAXKEY"], "CENSUS_BLOCK_2020"].str[:12].values
    new["units"] = new["NEW_DWELLING_UNITS"].astype(int)
    rows.append(new[["TAXKEY", "muni", "type", "comp", "bg", "units"]])
    out = pd.concat(rows, ignore_index=True)
    out["demolished"] = np.nan
    out["muni_then"] = ""
    # demolitions: units in the roll that came down in 2026 get their date; units gone before the roll come back
    keep = demo["STATUS"].isin(["Completed", "Expired"]) if "expired_too" in opts else (demo["STATUS"] == "Completed")
    dm = demo[keep & (demo["DWELLING_UNITS"].astype(int) > 0)].copy()
    dm["when"] = yf(dm["COMPLETED"].where(dm["COMPLETED"].fillna("") != "", dm["ISSUED"]))
    in_roll = dm[dm["when"] >= xf(W.ROLL)]
    idx = out.index[out["TAXKEY"].isin(set(in_roll["TAXKEY"]))]
    when_of = dict(zip(in_roll["TAXKEY"], in_roll["when"]))
    out.loc[idx, "demolished"] = out.loc[idx, "TAXKEY"].map(when_of)
    gone = dm[dm["when"] < xf(W.ROLL)].copy()
    blk = dict(zip(roll["TAXKEY"], roll["CENSUS_BLOCK_2020"]))
    gone["bg"] = gone["TAXKEY"].map(blk).str[:12]
    gone["muni"] = gone["TAXKEY"].str[:3].map(NAME_OF_NO)
    gone["type"] = gone["STRUCTURE"].map(CO_TYPE)
    gone["comp"] = gone["YEAR_BUILT"].astype(int) + mid
    gone["units"] = gone["DWELLING_UNITS"].astype(int)
    gone["demolished"] = gone["when"]
    gone["muni_then"] = gone["MUNICIPALITY"]
    out = pd.concat([out, gone[["TAXKEY", "muni", "type", "comp", "bg", "units", "demolished", "muni_then"]]],
                    ignore_index=True)
    out = out.loc[out.index.repeat(out["units"])].reset_index(drop=True)
    out["units"] = 1
    return out


def standing(st, x):
    return st[(st["comp"] <= x) & ~(st["demolished"] <= x)]


def gq2026(t, opts=()):
    gq = load(t)[6]
    col = "Licensed beds" if "gq_beds" in opts else "Residents, 1 April 2026"
    if "gq_2020" in opts:
        h = census_hist(t, full=True)[2020]
        return {m: int(h.loc[m, "Group quarters population"]) for m in h.index}
    return gq.groupby("Municipality")[col].sum().to_dict()


def census_hist(t, full=False):
    """each census's municipalities on that census's boundaries, the Towns and the Village of Ivydale combined"""
    hist = load(t)[4]
    out = {}
    cols = ["Total population", "Household population", "Group quarters population", "Housing units",
            "Occupied housing units"]
    for y, h in hist.items():
        h = h[h["Municipality"].notna() & h["FIPS code"].notna()].copy()
        h["key"] = h["Municipality"].replace({W.IVY_TOWN[1]: "Village of Ivydale"})
        out[y] = h.groupby("key")[cols].sum()
    return out


def design(st, x, bands, bgs, by="age"):
    s = standing(st, x)
    X = np.zeros((len(bgs), 4 + len(bands) - 1))
    bi = {b: i for i, b in enumerate(bgs)}
    a = (x - s["comp"]).values if by == "age" else s["comp"].values
    ty = s["type"].map({t: i for i, t in enumerate(TYPES)}).values
    rows = s["bg"].map(bi).values
    np.add.at(X, (rows, ty), 1)
    for j, (lo, hi) in enumerate(bands[:-1]):
        m = (a >= lo) & (a < hi)
        np.add.at(X, (rows[m], 4 + j), 1)
    return X


def fit(t, bands, by="age", opts=()):
    st = stock(t, opts)
    bg = load(t)[3]
    bgs = [g[-12:] for g in bg["GEO_ID"]]
    y = bg["P1_001N" if "total_pop" in opts else "P15_001N"].astype(float).values
    X = design(st, xf(W.C2020), bands, bgs, by)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta


def apply(t, beta, bands, x, by="age", key="muni", mask=None, opts=()):
    st = standing(stock(t, opts), x)
    if mask is not None:
        st = st[mask(st)]
    a = (x - st["comp"]).values if by == "age" else np.minimum(st["comp"].values, 2020.9)
    cb = np.concatenate([beta[4:], [0.0]])
    j = np.zeros(len(st), int)
    for k, (lo, hi) in enumerate(bands):
        j[(a >= lo) & (a < hi)] = k
    v = beta[st["type"].map({t_: i for i, t_ in enumerate(TYPES)}).values] + cb[j]
    return pd.Series(v, index=st.index).groupby(st[key].values).sum().to_dict()


def hu(t, x, opts=()):
    return standing(stock(t, opts), x).groupby("muni").size().to_dict()


@functools.lru_cache(maxsize=None)
def rungs(t, opts=()):
    names = [m[1] for m in W.MUNIS]
    gq = gq2026(t, opts)
    x26 = xf(W.EST) - (1 / 365.0 if "june30" in opts else 0.0)
    h = census_hist(t)
    hu26 = hu(t, x26, opts)
    est = {}
    est["place"] = {n: hu26[n] * h[2020].loc[n, "Household population"] / h[2020].loc[n, "Housing units"] + gq.get(n, 0)
                    for n in names}
    est["trend"] = {}
    for n in names:
        p10 = h[2010].loc[n, "Household population"] / h[2010].loc[n, "Housing units"]
        p20 = h[2020].loc[n, "Household population"] / h[2020].loc[n, "Housing units"]
        est["trend"][n] = hu26[n] * (p20 + (p20 - p10) * (x26 - xf(W.C2020)) / 10.0) + gq.get(n, 0)
    bt = fit(t, [(0, 999)], opts=opts)
    e = apply(t, bt, [(0, 999)], x26, opts=opts)
    est["type"] = {n: e[n] + gq.get(n, 0) for n in names}
    bv = fit(t, VINTAGE, by="year", opts=opts)
    e = apply(t, bv, VINTAGE, x26, by="year", opts=opts)
    est["vintage"] = {n: e[n] + gq.get(n, 0) for n in names}
    for k, bands in BANDS.items():
        b = fit(t, bands, opts=opts)
        e = apply(t, b, bands, x26, opts=opts)
        est[k] = {n: e[n] + gq.get(n, 0) for n in names}
    est["curve"] = curve(t, opts)
    for k, bands in BANDS.items():
        est[k + "_x"] = by_type_and_age(t, bands, opts)
    return est


def by_type_and_age(t, bands, opts=()):
    """persons per dwelling with an age profile of its own for each type of dwelling (a column for every type and age
    band), fitted on the 2020 block groups and applied at each dwelling's 2026 age"""
    st = stock(t, opts)
    bg = load(t)[3]
    bgs = [g[-12:] for g in bg["GEO_ID"]]
    y = bg["P1_001N" if "total_pop" in opts else "P15_001N"].astype(float).values
    x20, x26 = xf(W.C2020), xf(W.EST) - (1 / 365.0 if "june30" in opts else 0.0)
    bi = {b: i for i, b in enumerate(bgs)}
    nb = len(bands)

    def cols(s, x):
        a = (x - s["comp"]).values
        j = np.zeros(len(s), int)
        for q, (lo, hi) in enumerate(bands):
            j[(a >= lo) & (a < hi)] = q
        return s["type"].map({t_: i for i, t_ in enumerate(TYPES)}).values * nb + j
    s20 = standing(st, x20)
    X = np.zeros((len(bgs), 4 * nb))
    np.add.at(X, (s20["bg"].map(bi).values, cols(s20, x20)), 1)
    keep = X.sum(axis=0) > 0
    beta = np.zeros(4 * nb)
    beta[keep] = np.linalg.lstsq(X[:, keep], y, rcond=None)[0]
    s26 = standing(st, x26)
    e = pd.Series(beta[cols(s26, x26)]).groupby(s26["muni"].values).sum().to_dict()
    gq = gq2026(t, opts)
    return {n: e[n] + gq.get(n, 0) for n in e}


def curve(t, opts=()):
    """a smooth life cycle: persons per dwelling a level by type plus a common lift that rises for a few years and
    decays, fitted to the 2020 block groups by least squares"""
    from scipy.optimize import least_squares
    st = stock(t, opts)
    bg = load(t)[3]
    bgs = [g[-12:] for g in bg["GEO_ID"]]
    y = bg["P1_001N" if "total_pop" in opts else "P15_001N"].astype(float).values
    x20 = xf(W.C2020)
    s = standing(st, x20)
    bi = {b: i for i, b in enumerate(bgs)}
    rows = s["bg"].map(bi).values
    a = (x20 - s["comp"]).values
    ty = s["type"].map({t_: i for i, t_ in enumerate(TYPES)}).values
    C = np.zeros((len(bgs), 4))
    np.add.at(C, (rows, ty), 1)

    def res(p):
        lift = p[4] * (1 + p[6] * np.maximum(a, 0)) * np.exp(-np.maximum(a, 0) / p[5])
        L = np.zeros(len(bgs))
        np.add.at(L, rows, lift)
        return C @ p[:4] + L - y
    p = least_squares(res, [2, 1.8, 1.5, 2, 0.8, 12, 0.1], bounds=([0, 0, 0, 0, 0, 1, 0], [5, 5, 5, 5, 5, 60, 2])).x
    x26 = xf(W.EST)
    s26 = standing(st, x26)
    a26 = (x26 - s26["comp"]).values
    v = p[s26["type"].map({t_: i for i, t_ in enumerate(TYPES)}).values] + \
        p[4] * (1 + p[6] * np.maximum(a26, 0)) * np.exp(-np.maximum(a26, 0) / p[5])
    e = pd.Series(v).groupby(s26["muni"].values).sum().to_dict()
    gq = gq2026(t, opts)
    return {n: e[n] + gq.get(n, 0) for n in e}


def golden(t):
    return rungs(t)["age"]


def muni_then(t, date):
    """the municipality each unit of the stock stood in on a past census date: annexed parcels in the municipality
    they left until the annexation, the Town of Ivydale folded into the Village (the census history is combined)"""
    st = stock(t)
    bnd = load(t)[5]
    ann = bnd[bnd["CHANGE_TYPE"] == "Annexation"]
    eff = dict(zip(ann["TAXKEY"], ann["EFFECTIVE"]))
    frm = dict(zip(ann["TAXKEY"], ann["FROM_MUNICIPALITY"]))
    out = st["muni"].copy()
    gone = st["muni_then"] != ""
    out[gone] = st.loc[gone, "muni_then"].replace({W.IVY_TOWN[1]: "Village of Ivydale"})
    for i, k in zip(st.index, st["TAXKEY"]):
        if k in eff and dt.date.fromisoformat(eff[k]) > date and not gone[i]:
            out[i] = frm[k]
    return out


def backcast(t):
    """each model's household population at the 2000 and 2010 censuses from the dwellings standing then, against the
    census on its boundaries: per cent error by municipality"""
    st = stock(t)
    h = census_hist(t)
    out = {}
    models = {"age": (fit(t, AGEB), AGEB, "age"), "vintage": (fit(t, VINTAGE, by="year"), VINTAGE, "year")}
    for date in (W.C2010, W.C2000):
        x = xf(date)
        mt = muni_then(t, date)
        st2 = st.assign(then=mt)
        res = {}
        for k, (beta, bands, by) in models.items():
            s = standing(st2, x)
            a = (x - s["comp"]).values if by == "age" else s["comp"].values
            cb = np.concatenate([beta[4:], [0.0]])
            j = np.zeros(len(s), int)
            for q, (lo, hi) in enumerate(bands):
                j[(a >= lo) & (a < hi)] = q
            v = beta[s["type"].map({t_: i for i, t_ in enumerate(TYPES)}).values] + cb[j]
            res[k] = pd.Series(v).groupby(s["then"].values).sum().to_dict()
        s = standing(st2, x)
        units = s.groupby("then").size()
        pph20 = h[2020]["Household population"] / h[2020]["Housing units"]
        res["place"] = {m: units[m] * pph20[m] for m in units.index if m in pph20.index}
        hp = h[date.year]["Household population"]
        out[date.year] = {k: {m: 100.0 * (v[m] / hp[m] - 1) for m in v if m in hp.index} for k, v in res.items()}
    return out
