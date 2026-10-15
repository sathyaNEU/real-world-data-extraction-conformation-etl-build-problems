"""The 2025 wave of the national household wealth survey as the survey's own systems hold it: every household with
its true members, wealth and design variables, the five implicates of its net worth, its final weight and its 200
bootstrap replicate weights. The decisive structure (common and age-specific area effects on wealth, households
placed by the older partner) is drawn from one stream fixed by DESIGN_SEED; everything layered on top comes from
its own labelled stream so the design cannot move."""
from __future__ import annotations

import numpy as np

import common as K


def core(design=None):
    """The design study's draw (search6.py's gen at DESIGN_SEED), unchanged: area effects, older-partner ages,
    couples and their age gap, which partner the survey's hierarchy makes the reference person, net worth before
    tuning, which households carry imputed items, base weights, implicate noise and the replicate draws."""
    P = dict(K.DESIGN, **(design or {}))
    rng = np.random.default_rng(P.get("seed", K.DESIGN_SEED))
    tgt = np.log(np.array(P["log_median"], float) * 1000)
    share = np.array(P["share_area"]); prem = np.array(P["couple_premium"])
    cols = {k: [] for k in ("h", "p", "ref", "older", "younger", "couple", "nw0", "imp", "w")}
    for h in range(K.STRATA):
        for p in range(K.PSU_PER_STRATUM):
            eff = rng.normal(0, P["common_sd"]); spec = rng.normal(0, P["specific_sd"], 6)
            n = K.HH_PER_PSU + int(rng.integers(-6, 7))
            olda = np.clip(rng.choice([29, 40, 50, 60, 70, 81], n, p=[.18, .17, .17, .18, .18, .12])
                           + rng.integers(-5, 5, n), 19, 97)
            pc = np.where(olda < 35, 0.4, np.where(olda < 75, 0.64, 0.50))
            couple = rng.random(n) < pc
            gap = np.abs(rng.normal(P.get("gap_mean", 3.0), P.get("gap_sd", 3.4), n)).round()
            younger = np.clip(olda - gap, 18, None)
            ref = np.where(couple & (rng.random(n) < P["ref_younger_p"]), younger, olda)
            b = K.band_of(olda)
            mu = tgt[b] + np.where(couple, prem[b], -prem[b] * 0.9) + share[b] * (eff + spec[b])
            nw = np.exp(mu + rng.normal(0, P["idio_sd"], n))
            nw = np.where((b == 0) & (rng.random(n) < 0.13), -rng.exponential(12000, n), nw)
            for key, v in (("h", [h] * n), ("p", [p] * n), ("ref", ref), ("older", olda), ("younger", younger),
                           ("couple", couple), ("nw0", nw), ("imp", rng.random(n) < P["imputed_share"]),
                           ("w", rng.uniform(4000, 11000, n))):
                cols[key] += list(v)
    d = {k: np.array(v) for k, v in cols.items()}
    N = len(d["h"])
    d["noise"] = np.stack([np.where(d["imp"], np.exp(rng.normal(0, P["imputation_sd"], N)), 1.0)
                           for _ in range(K.IMPLICATES)])
    pick = rng.integers(0, 2, (K.REPLICATES, K.STRATA))
    d["mult"] = np.where(d["p"][None, :] == pick[:, d["h"]], 2.0, 0.0)
    return d


STATES = [("NSW", 19), ("VIC", 15), ("QLD", 12), ("WA", 6), ("SA", 4), ("TAS", 2), ("ACT", 1), ("NT", 1)]
REL = {1: "Reference person", 2: "Husband, wife or registered partner", 3: "De facto partner", 4: "Child under 15",
       5: "Dependent student aged 15 to 24", 6: "Non-dependent child", 7: "Parent of reference person",
       8: "Other relative", 9: "Unrelated person"}


def wealth(d, k=None, older_area=None):
    """Net worth on each implicate (Australian dollars, whole dollars): the design's draw times the age group's factor
    k, the retirement-age areas' own effect (housing and retirement savings moving with the area for the two oldest
    groups, from its own stream) and, for a household with imputed items, the implicate's draw on the imputed share."""
    k = np.asarray(K.TUNE if k is None else k, float)
    sd = K.OLDER_AREA if older_area is None else older_area
    N = len(d["h"])
    b = K.band_of(d["older"])
    f = np.where(d["nw0"] > 0, k[b], 1.0)
    za = K.rng("older-areas").normal(0, 1, (K.STRATA, K.PSU_PER_STRATUM, 2))
    e = np.where(b == 4, sd[0] * za[d["h"], d["p"], 0], np.where(b == 5, sd[1] * za[d["h"], d["p"], 1], 0.0))
    f = f * np.where(d["nw0"] > 0, np.exp(e), 1.0)
    s = K.rng("imputed-share").uniform(K.IMPUTED_SHARE[0], K.IMPUTED_SHARE[1], N)
    mult = 1.0 - s[None, :] + s[None, :] * d["noise"]
    return np.rint(d["nw0"][None, :] * mult * f[None, :] * K.SCALE), mult


def survey(k=None, older_area=None, design=None):
    """The 2025 wave as the survey's systems hold it. k: the six net worth factors per older-partner age group
    (the design's tuning; default the tuned values in common.TUNE)."""
    d = core(design)
    N = len(d["h"])
    b = K.band_of(d["older"])
    nw, mult = wealth(d, k, older_area)
    # weights scaled to the household benchmark; replicate weights follow
    w = d["w"] * K.POPULATION_HOUSEHOLDS / d["w"].sum()
    d.update(nw=nw, wgt=np.round(w, 4), band=b)
    d["repw"] = np.round(d["mult"] * d["wgt"][None, :], 4)
    # strata to states (internal only; the public file carries the state)
    st = []
    for code, n in STATES:
        st += [code] * n
    d["state"] = np.array(st)[d["h"]]
    # members: reference person and partner from the design; children, students, adult children, parents of the
    # reference person and housemates from their own stream
    r = K.rng("members")
    sex_ref = np.where(r.random(N) < 0.53, "M", "F")
    same_sex = d["couple"] & (r.random(N) < 0.015)
    partner_age = np.where(d["couple"], np.where(d["ref"] == d["older"], d["younger"], d["older"]), -1)
    married = d["couple"] & (r.random(N) < np.where(d["older"] < 35, 0.42, np.where(d["older"] < 55, 0.74, 0.88)))
    kids = np.where(d["older"] < 55, r.poisson(np.where(d["couple"], 1.25, 0.45)), 0)
    kids = np.where(d["older"] < 30, np.minimum(kids, 2), kids)
    students = np.where((d["older"] >= 40) & (d["older"] < 65), r.binomial(1, 0.22, N), 0)
    adult_kids = np.where((d["older"] >= 48) & (d["older"] < 80), r.binomial(2, 0.12, N), 0)
    parents = np.where((d["older"] >= 35) & (d["older"] < 70), r.binomial(1, 0.022, N), 0)
    housemates = np.where(~d["couple"] & (d["older"] < 35), r.binomial(3, 0.18, N), 0)
    persons = []
    for i in range(N):
        a_ref = int(d["ref"][i])
        persons.append((i, 1, a_ref, sex_ref[i]))
        if d["couple"][i]:
            ps = sex_ref[i] if same_sex[i] else ("F" if sex_ref[i] == "M" else "M")
            persons.append((i, 2 if married[i] else 3, int(partner_age[i]), ps))
        young_parent = int(d["younger"][i]) if d["couple"][i] else a_ref
        for _ in range(int(kids[i])):
            persons.append((i, 4, int(np.clip(young_parent - r.integers(20, 40), 0, 14)), "M" if r.random() < .51 else "F"))
        for _ in range(int(students[i])):
            persons.append((i, 5, int(r.integers(15, 25)), "M" if r.random() < .5 else "F"))
        for _ in range(int(adult_kids[i])):
            persons.append((i, 6, int(np.clip(young_parent - r.integers(22, 34), 18, 60)), "M" if r.random() < .55 else "F"))
        for _ in range(int(parents[i])):
            persons.append((i, 7, int(np.clip(int(d["older"][i]) + r.integers(22, 33), 60, 99)), "F" if r.random() < .7 else "M"))
        for _ in range(int(housemates[i])):
            persons.append((i, 9, int(np.clip(a_ref + r.integers(-4, 6), 18, 40)), "M" if r.random() < .5 else "F"))
    d["persons"] = persons
    # wealth components per implicate: debts by age and tenure, assets = net worth + debts, home value and super
    r2 = K.rng("components")
    owner_p = np.array([0.38, 0.62, 0.72, 0.79, 0.83, 0.80])[b]
    owner = r2.random(N) < owner_p
    mort_p = np.array([0.88, 0.80, 0.62, 0.38, 0.14, 0.05])[b]
    mortgaged = owner & (r2.random(N) < mort_p)
    base_debt = np.exp(np.log(np.array([42, 60, 48, 30, 10, 4.0])[b] * 1000) + r2.normal(0, 0.9, N))
    mort_bal = np.where(mortgaged, np.exp(np.log(np.array([420, 470, 360, 230, 140, 110.0])[b] * 1000)
                                            + r2.normal(0, 0.45, N)), 0.0)
    debts = np.rint(base_debt * 0.25 + mort_bal)
    debts = np.where(nw.min(0) < 0, np.maximum(debts, -nw.min(0) + np.rint(r2.uniform(500, 9000, N))), debts)
    d["owner"], d["mortgaged"] = owner, mortgaged
    d["debts"] = np.tile(debts, (K.IMPLICATES, 1))
    d["assets"] = d["nw"] + d["debts"]
    home_share = np.clip(r2.normal(np.array([0.55, 0.62, 0.55, 0.47, 0.50, 0.58])[b], 0.12), 0.15, 0.92)
    d["house"] = np.where(owner[None, :], np.rint(d["assets"] * home_share[None, :]), 0.0)
    super_share = np.clip(r2.normal(np.array([0.30, 0.22, 0.26, 0.31, 0.24, 0.12])[b], 0.08), 0.0, 0.8)
    d["super"] = np.rint(np.maximum(d["assets"] - d["house"], 0) * super_share[None, :])
    inc = np.exp(np.log(np.array([88, 132, 141, 118, 74, 52.0])[b] * 1000) + np.where(d["couple"], 0.35, -0.2)
                 + 0.18 * np.log(np.maximum(d["nw0"], 1000) / 1e5) + r2.normal(0, 0.45, N))
    d["income"] = np.rint(inc[None, :] * np.where(d["imp"][None, :], mult ** 0.3, 1.0))
    d["tenure"] = np.where(owner, np.where(mortgaged, "Owner with a mortgage", "Owner without a mortgage"),
                           np.where(r2.random(N) < 0.86, "Renter, private landlord", "Renter, state housing authority"))
    # public identifiers in a shuffled order
    ids = r2.permutation(np.arange(10001, 10001 + 4 * N))[:N]
    d["hhid"] = np.array(["%06d" % x for x in ids])
    return d
