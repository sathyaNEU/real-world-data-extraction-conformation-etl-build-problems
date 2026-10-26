"""The golden analysis, read from the shipped pack only: the book's house-years and non-weather water claims by
home and accident year, each home's characteristics and water supply zone, the Frequency Model Standard's search
over main-effects Poisson models (fitted on 2023 and 2024, judged on 2025, refitted on 2023 to 2025), each
township's mean frequency, and the asks (protected homes, market value, the book's water claim payments by accident
year, the book's fire frequency by protection)."""
import csv
import datetime as dt
import itertools
import json
import os

import numpy as np
import pandas as pd
import statsmodels.api as sm
from matplotlib.path import Path
from scipy.spatial import cKDTree

import common as K

WATER = {"WTR-P", "WTR-A", "3110", "3120", "3130"}
FIRE = {"FIR", "5110", "5120"}
FOUND = {"BSMT FULL": "B", "BSMT PART": "B", "SLAB": "S", "CRAWL": "C", "PIERS": "C"}
WALL = {"FRAME": "F", "BRICK VENEER": "MV", "MASONRY": "M", "STONE": "M"}
FACTORS = ["found", "era", "bath", "cons", "st", "zone"]
RECORDED = ["found", "era", "bath", "cons", "st"]
RENUMBER = dt.date(2024, 4, 1)
CERTIFIED = dt.date(2026, 1, 1)


def read(target, key):
    return pd.read_csv(os.path.join(target, K.FILES[key]), dtype=str, keep_default_na=False)


def era(y):
    y = int(y)
    return "a<1940" if y < 1940 else "b1940-69" if y < 1970 else "c1970-99" if y < 2000 else "d2000+"


def bath(n):
    return str(min(int(n), 4))


def stories(s):
    return "2" if float(s) >= 2 else s


# ---- exposure and claims
def exposure(T):
    """house-years by parcel and accident year (standard 2.4): effective date to expiration, or to a cancellation
    that was not reinstated"""
    out = {}
    for r in T.itertuples(index=False):
        a = dt.date.fromisoformat(r.term_effective)
        b = dt.date.fromisoformat(r.term_expiration)
        if r.cancellation_effective and not r.reinstatement_effective:
            b = min(b, dt.date.fromisoformat(r.cancellation_effective))
        for y in K.YEARS:
            lo, hi = max(a, dt.date(y, 1, 1)), min(b, dt.date(y + 1, 1, 1))
            if hi > lo:
                k = (r.parcel_id, y)
                out[k] = out.get(k, 0.0) + (hi - lo).days / (366.0 if y == 2024 else 365.0)
    s = pd.Series(out, name="expo")
    s.index.names = ["parcel_id", "year"]
    return s


def claims_once(C):
    """one line per claim: the reopened lines (suffix -R1) are the same claim (standard 2.1)"""
    return C[C["reopened_from"] == ""]


def counts(C, codes):
    c = claims_once(C)
    c = c[c["cause_code"].isin(codes)].copy()
    c["year"] = c["date_of_loss"].str[:4].astype(int)
    c = c[c["year"].isin(K.YEARS)]
    return c.groupby(["parcel_id", "year"]).size().rename("n")


# ---- zones
def zone_paths(target):
    g = json.load(open(os.path.join(target, K.FILES["zones"])))
    paths = []
    for f in g["features"]:
        geom = f["geometry"]
        polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
        for poly in polys:
            paths.append((f["properties"]["ZONE_ID"], Path(np.array(poly[0]))))
    return paths


def zones_of(paths, xy):
    out = np.array([""] * len(xy), dtype=object)
    for zid, p in paths:
        m = p.contains_points(xy)
        out[m] = zid
    return out


# ---- the book and the townships' homes
def book_table(target):
    T, C, P = read(target, "terms"), read(target, "claims"), read(target, "parcels")
    ex = exposure(T)
    n = counts(C, WATER)
    d = pd.DataFrame(ex).join(n, how="left").fillna({"n": 0}).reset_index()
    d.columns = ["parcel_id", "year", "expo", "n"]
    last = T.sort_values(["policy_number", "term_number"], key=lambda s: s.astype(int) if s.name == "term_number"
                         else s).groupby("parcel_id").tail(1)
    ch = pd.DataFrame({"parcel_id": last["parcel_id"].values,
                       "found": last["foundation"].values,
                       "era": [era(y) for y in last["year_built"]],
                       "bath": [bath(b) for b in last["full_baths"]],
                       "cons": last["construction"].values,
                       "st": [stories(s) for s in last["stories"]],
                       "town": last["municipality_code"].values})
    xy = P.set_index("parcel_id").loc[ch["parcel_id"], ["x_coord_ft", "y_coord_ft"]].astype(float).values
    ch["zone"] = zones_of(zone_paths(target), xy)
    ch["x"], ch["y"] = xy[:, 0], xy[:, 1]
    d = d.merge(ch, on="parcel_id", how="left")
    return d, ch


def township_homes(target):
    P, D = read(target, "parcels"), read(target, "dwellings")
    h = P[P["municipality_code"].isin(K.CANDIDATES) & (P["land_use_code"] == "R-SFD") &
          (P["homestead_farmstead"] == "H")].copy()
    d1 = D[D["card_number"] == "1"].set_index("parcel_id")
    d1 = d1.loc[h["parcel_id"]]
    out = pd.DataFrame({"parcel_id": h["parcel_id"].values, "town": h["municipality_code"].values,
                        "found": [FOUND[f] for f in d1["foundation"]],
                        "era": [era(y) for y in d1["year_built"]],
                        "bath": [bath(b) for b in d1["full_baths"]],
                        "cons": [WALL[w] for w in d1["exterior_wall"]],
                        "st": [stories(s) for s in d1["stories"]],
                        "x": h["x_coord_ft"].astype(float).values, "y": h["y_coord_ft"].astype(float).values,
                        "assessed": h["assessed_total"].astype(int).values})
    out["zone"] = zones_of(zone_paths(target), out[["x", "y"]].values)
    return out


# ---- the standard's model search
def design(df, cols, levels):
    X = [np.ones(len(df))]
    for c in cols:
        v = df[c].values
        for lv in levels[c][1:]:
            X.append((v == lv).astype(float))
    return np.column_stack(X)


def deviance(y, mu):
    y, mu = np.asarray(y, float), np.asarray(mu, float)
    t = np.where(y > 0, y * np.log(np.where(y > 0, y, 1.0) / mu), 0.0)
    return float(2 * np.sum(t - (y - mu)))


def fit(df, cols, levels):
    m = sm.GLM(df["n"].values, design(df, cols, levels), family=sm.families.Poisson(),
               offset=np.log(df["expo"].values)).fit()
    return m.params


def search(d, homes, factors=FACTORS):
    """every main-effects model on the factors: its 2025 deviance (fitted on 2023 and 2024) and, refitted on 2023
    to 2025, each township's mean frequency per 1,000 house-years"""
    levels = {c: sorted(set(d[c])) for c in factors}
    tr, te = d[d["year"] < 2025], d[d["year"] == 2025]
    res = []
    for k in range(len(factors) + 1):
        for cols in itertools.combinations(factors, k):
            b = fit(tr, cols, levels)
            mu = np.exp(design(te, cols, levels) @ b + np.log(te["expo"].values))
            b2 = fit(d, cols, levels)
            f = np.exp(design(homes, cols, levels) @ b2) * 1000.0
            town = pd.Series(f).groupby(homes["town"].values).mean()
            res.append(dict(cols=cols, dev=deviance(te["n"].values, mu), town={t: float(town[t]) for t in K.CANDIDATES},
                            params=b2))
    res.sort(key=lambda r: r["dev"])
    return res


def run(target):
    import asks as AS
    d, ch = book_table(target)
    homes = township_homes(target)
    res = search(d, homes)
    best = res[0]
    H = AS.hydrants(target)
    homes["protected"] = AS.protected(H, homes[["x", "y"]].values)
    mv = AS.market(target, homes)
    clr = [float(r.common_level_ratio) for r in read(target, "clr").itertuples(index=False)
           if dt.date.fromisoformat(r.effective_from) <= CERTIFIED <= dt.date.fromisoformat(r.effective_to)][0]
    pay = AS.payments(target)
    fire = AS.fire(target, d)
    return dict(d=d, ch=ch, homes=homes, res=res, best=best, H=H, market=mv, clr=clr, pay=pay, fire=fire)
