"""task122 generator: sites, screening, randomisation and each patient's baseline for VMK-4410-202."""
from datetime import date, timedelta

import numpy as np
import pandas as pd

import params as P

CITIES = {
    "DK": ["Copenhagen", "Aarhus", "Odense", "Aalborg", "Herlev", "Roskilde"],
    "SE": ["Stockholm", "Gothenburg", "Malmo", "Uppsala", "Linkoping"],
    "DE": ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt", "Leipzig", "Dresden", "Hannover", "Nuremberg",
           "Essen", "Freiburg", "Mainz"],
    "PL": ["Warsaw", "Krakow", "Lodz", "Wroclaw", "Poznan", "Gdansk", "Lublin", "Katowice", "Bialystok", "Szczecin"],
    "ES": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao", "Malaga", "Zaragoza", "Murcia", "Valladolid"],
    "GB": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow", "Bristol", "Cardiff", "Newcastle"],
}
PREFIX = {"DK": 11, "SE": 12, "DE": 13, "PL": 14, "ES": 15, "GB": 16}


def sites(rng):
    rows = []
    for cc, name, n, hub in P.COUNTRIES:
        for k in range(n):
            sid = "%d%02d" % (PREFIX[cc], k + 1)
            act = P.FIRST_RAND - timedelta(days=int(rng.integers(20, 75))) + timedelta(days=int(rng.integers(0, 120)))
            rows.append({"SITEID": sid, "COUNTRY": cc, "COUNTRY_NAME": name, "CITY": CITIES[cc][k], "LAB_HUB": hub,
                         "ACTIVATED": act, "weight": float(rng.gamma(2.2, 1.0))})
    return pd.DataFrame(rows)


def _enrol_dates(rng, n):
    """randomisation dates over the enrolment period, slow at first, steady, then a final push"""
    span = (P.LAST_RAND - P.FIRST_RAND).days
    u = rng.beta(1.35, 1.1, n)
    days = np.sort((u * span).astype(int))
    out = [P.FIRST_RAND + timedelta(days=int(d)) for d in days]
    return [x + timedelta(days=P.weekday_shift(x)) for x in out]


def screen_and_randomise(rng, st, rng_blocks=None):
    """screen patients until 600 are randomised; a screened patient fails on a screening eGFR, UACR or potassium
    outside the range, or for another reason, and keeps the subject number the site gave at screening"""
    n_rand = len(P.ARMS) * P.N_PER_ARM
    rdates = _enrol_dates(rng, n_rand)
    w = st["weight"].to_numpy() / st["weight"].sum()
    seq = {s: 0 for s in st["SITEID"]}
    pats, fails = [], []
    strata_blocks = {}
    r_i = 0
    while r_i < n_rand:
        site = st.iloc[int(rng.choice(len(st), p=w))]
        sd = rdates[r_i] - timedelta(days=int(rng.integers(8, 22)))
        if sd < site["ACTIVATED"]:
            sd = site["ACTIVATED"] + timedelta(days=int(rng.integers(1, 10)))
        sd = sd + timedelta(days=P.weekday_shift(sd))
        seq[site["SITEID"]] += 1
        subj = "%s-%03d" % (site["SITEID"], seq[site["SITEID"]])
        age = int(np.clip(rng.normal(63.5, 10.5), 31, 84))
        sex = "M" if rng.random() < 0.62 else "F"
        g0 = float(np.clip(rng.normal(41.5, 9.5), 21.0, 66.0))
        uacr = float(np.exp(rng.normal(np.log(720), 0.75)))
        k0 = float(rng.normal(4.48, 0.36))
        fail = None
        scr_egfr = g0 * float(np.exp(rng.normal(0, 0.045)))
        scr_k = k0 + float(rng.normal(0, 0.18))
        if scr_egfr < 25 or scr_egfr > 60:
            fail = "EGFR OUT OF RANGE"
        elif uacr < 200 or uacr > 5000:
            fail = "UACR OUT OF RANGE"
        elif scr_k > 4.8:
            fail = "POTASSIUM ABOVE 4.8"
        elif rng.random() < 0.07:
            fail = ["OTHER INCLUSION CRITERION NOT MET", "WITHDRAWAL BY SUBJECT", "OTHER EXCLUSION CRITERION MET"][int(rng.integers(0, 3))]
        base = {"SITEID": site["SITEID"], "COUNTRY": site["COUNTRY"], "LAB_HUB": site["LAB_HUB"], "SUBJID": subj,
                "SCRDT": sd, "AGE": age, "SEX": sex, "G0": g0, "UACR0": uacr, "K0": k0, "SCR_EGFR": scr_egfr,
                "SCR_K": scr_k}
        if fail:
            base["FAILREASON"] = fail
            fails.append(base)
            continue
        base["RANDDT"] = rdates[r_i]
        if base["RANDDT"] <= sd:
            base["RANDDT"] = sd + timedelta(days=int(rng.integers(7, 15)))
            base["RANDDT"] = base["RANDDT"] + timedelta(days=P.weekday_shift(base["RANDDT"]))
        stratum = ("<45" if scr_egfr < 45 else ">=45", "<1000" if uacr < 1000 else ">=1000")
        blk = strata_blocks.setdefault(stratum, [])
        if not blk:
            b = list(P.ARMS) * 2
            (rng if rng_blocks is None else rng_blocks).shuffle(b)
            blk.extend(b)
        base["ARM"] = blk.pop(0)
        base["STRAT_EGFR"], base["STRAT_UACR"] = stratum
        pats.append(base)
        r_i += 1
    pats = pd.DataFrame(pats).sort_values(["RANDDT", "SUBJID"]).reset_index(drop=True)
    pats["RANDNO"] = ["R%04d" % (i + 101) for i in range(len(pats))]
    fails = pd.DataFrame(fails)
    return pats, fails


def baseline(rng, pats):
    """background therapy, comorbidity and the patient-level effects the simulation draws on"""
    n = len(pats)
    pats = pats.copy()
    pats["DIAB"] = rng.random(n) < 0.56
    pats["LOOP"] = rng.random(n) < 0.40
    pats["SGLT2"] = rng.random(n) < 0.54
    pats["RAS"] = np.where(rng.random(n) < 0.58, "ACEI", "ARB")
    pats["HEIGHT"] = np.where(pats["SEX"] == "M", rng.normal(177, 7, n), rng.normal(164, 6.5, n)).round(0)
    bmi = np.clip(rng.normal(30.5, 5.0, n), 20, 46)
    pats["WEIGHT0"] = (bmi * (pats["HEIGHT"] / 100) ** 2).round(1)
    pats["SBP0"] = np.clip(rng.normal(137, 13, n), 105, 175)
    pats["DBP0"] = np.clip(rng.normal(78, 9, n), 55, 105)
    # placebo course of eGFR a year; faster with more albumin in the urine
    pats["SLOPE"] = rng.normal(P.PBO_SLOPE, P.SLOPE_SD, n) - 0.55 * (np.log(pats["UACR0"]) - np.log(720))
    pats["H_MULT"] = np.exp(rng.normal(0, 0.25, n))
    pats["V_MULT"] = np.exp(rng.normal(0, 0.45, n))
    pats["C_DEV"] = rng.normal(0, P.C_SD, n)
    pats["K_MULT"] = np.exp(rng.normal(0, 0.35, n))
    pats["EASE_U"] = rng.random(n)
    pats["EASE_V"] = rng.choice(list(P.EASE_VISITS), n, p=list(P.EASE_VISITS.values()))
    pats["RHO"] = rng.uniform(0.65, 1.0, n)
    return pats
