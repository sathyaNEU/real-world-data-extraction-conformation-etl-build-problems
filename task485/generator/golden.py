"""The golden computation and the ladder's routes on the clean truth, vectorised. Each animal's herd intervals are cut
at its first and second birthdays and its first calving; each piece sits in the region of the herd holding the animal,
at the factor note's housed rate on the days inside that region's housing season and its grass rate on the others."""
from collections import defaultdict

import numpy as np

import world as W

REGI = {r: i for i, r in enumerate(W.REG)}
NREG = len(W.REG)
CUMH = np.array([W.CUMH[r] for r in W.REG])
CATI = {c: i for i, c in enumerate(W.CATS)}
NCAT = len(W.CATS)
RH = np.array([W.RATE[c][0] for c in W.CATS])
RG = np.array([W.RATE[c][1] for c in W.CATS])
# the census's categories against the factor note's
NSO_TO_CAT = {"dairy_cows": "dairy_cow", "other_cows": "suckler_cow", "bulls": "over24", "male_2yr_plus": "over24",
              "female_2yr_plus": "over24", "male_1_2yr": "m12_24", "female_1_2yr": "m12_24", "male_calves": "calf",
              "female_calves": "calf"}


class Truth:
    """the animal columns as arrays"""

    def __init__(self, A):
        self.birth = np.array(A["birth"])
        self.fc = np.array([x if x is not None else 10 ** 6 for x in A["fc"]])
        self.female = np.array([x == "F" for x in A["sex"]])
        self.dairy = np.array([b in W.DAIRY_BREEDS for b in A["breed"]])


def iv_arrays(IV):
    a, h, s, e = [], [], [], []
    for k, iv in IV.items():
        for hh, ss, ee in iv:
            a.append(k)
            h.append(hh)
            s.append(ss)
            e.append(ee)
    return np.array(a), np.array(h), np.array(s), np.array(e)


def split(T, a, s, e):
    c = np.stack([T.birth[a] + 365, T.birth[a] + 730, T.fc[a]], 1)
    c = np.minimum(np.maximum(c, s[:, None]), e[:, None])
    c.sort(1)
    pts = np.concatenate([s[:, None], c, e[:, None]], 1)
    p0, p1 = pts[:, :-1].ravel(), pts[:, 1:].ravel()
    rows = np.repeat(np.arange(len(a)), 4)
    keep = p1 > p0
    return rows[keep], p0[keep], p1[keep]


def cat_of(T, a, day):
    age = day - T.birth[a]
    cow = T.female[a] & (T.fc[a] <= day)
    return np.where(age < 365, CATI["calf"],
                    np.where(cow, np.where(T.dairy[a], CATI["dairy_cow"], CATI["suckler_cow"]),
                             np.where(age < 730, CATI["m12_24"], CATI["over24"])))


class Pieces:
    def __init__(self, T, ivs, herd_region):
        a, h, s, e = ivs
        rows, self.p0, self.p1 = split(T, a, s, e)
        self.a, self.h = a[rows], h[rows]
        self.r = herd_region[self.h]
        self.cat = cat_of(T, self.a, self.p0)
        first = {}
        for k in range(len(a) - 1, -1, -1):
            first[a[k]] = h[k]
        self.home = herd_region[np.array([first[x] for x in self.a])]


def ammonia(P, season=None):
    """kg NH3 by region; season: the region whose housing season applies to each piece (default its own region)"""
    sr = P.r if season is None else season
    hd = CUMH[sr, P.p1] - CUMH[sr, P.p0]
    kg = hd * RH[P.cat] + (P.p1 - P.p0 - hd) * RG[P.cat]
    return np.bincount(P.r, kg, NREG)


def days(P):
    return np.bincount(P.r * NCAT + P.cat, P.p1 - P.p0, NREG * NCAT).reshape(NREG, NCAT)


def stock(P, day):
    m = (P.p0 <= day) & (day < P.p1)
    return np.bincount(P.r[m] * NCAT + P.cat[m], None, NREG * NCAT).reshape(NREG, NCAT)


def table5():
    """the factor note's Table 5 as printed, kg NH3 a head a year to one decimal"""
    return np.array([[round(W.annual_factor(r, c), 1) for c in W.CATS] for r in W.REG])


def census_route(census_by_farm, farm_region, t5=None):
    t5 = table5() if t5 is None else t5
    out = np.zeros(NREG)
    for farm, cats in census_by_farm.items():
        ri = REGI[farm_region[farm]]
        for k, n in cats.items():
            out[ri] += n * t5[ri, CATI[NSO_TO_CAT[k]]]
    return out


def farmed_land(parcels, herd_no_region, whole_commonage=False, drop_commonage=False):
    land = np.zeros(NREG)
    for p in parcels:
        if p["use"] == "Commonage":
            if drop_commonage:
                continue
            f = 1.0 if whole_commonage else p["share"] / 100.0
        else:
            f = p["share"] / 100.0
        land[REGI[herd_no_region[p["herd"]]]] += p["area"] * f
    return land


def designated(kg, land):
    return [W.REG[i] for i in range(NREG) if kg[i] / land[i] >= W.LINE]


def by_region(x):
    return {r: float(x[i]) for i, r in enumerate(W.REG)}
