"""task169 world: the people released to parole in Pembroke since 2019 and those projected for release in 2027,
with the parameters of the processes that write the four agencies' records. Nothing here is shipped."""
from __future__ import annotations

import datetime as dt

import numpy as np

from common import stream, add, RECORD_START, CUT, DISTRICTS

OFFENCES = ("Violent", "Property", "Drug", "Public order")
OFF_P = (0.29, 0.29, 0.27, 0.15)
OFF_ETA = {"Violent": -0.05, "Property": 0.28, "Drug": 0.10, "Public order": -0.12}
DIST_P = (0.34, 0.27, 0.22, 0.17)
DIST_ETA = {"Garrison": 0.40, "Ridgway": 0.07, "Linwood": 0.08, "Corliss": -0.22}

FRAILTY_SHAPE = 8.0
A0 = 0.00186                                  # arrests per day at liberty at eta 0, z 1, g 1
G_BANDS = ((0, 90, 1.70), (90, 180, 1.35), (180, 365, 1.00), (365, 730, 0.78), (730, 99999, 0.62))
CLASS_BASE = {"Violent": (0.24, 0.37, 0.39), "Property": (0.13, 0.45, 0.42),
              "Drug": (0.14, 0.43, 0.43), "Public order": (0.15, 0.33, 0.52)}
# the Board's practice: share of a parolee's arrests it answers by revocation, by district (felony A-B scaled)
R_INLIEU = {"Garrison": 0.78, "Ridgway": 0.58, "Linwood": 0.40, "Corliss": 0.22}
R_F1_SCALE = 0.80
# the courts: a prosecuted arrest's chance of a prison commitment, by class; and the arrest-to-admission lag
P_PRISON = {"F1": 0.62, "F2": 0.27, "M": 0.025}
P_CONVICT_OTHER = {"F1": 0.20, "F2": 0.41, "M": 0.52}     # convicted, sentence not prison
LAG_MEAN = {"F1": 250.0, "F2": 190.0, "M": 110.0}
LAG_SHAPE = 5.0
TECH_RATE = 0.00070                         # condition violations reported per supervised day at liberty
TECH_REVOKE = 0.55
HEARING_DELAY = (18, 56)
REVOKE_TERM = (120, 271)
NEWCOMMIT_MONTHS = (26.0, 0.45)             # lognormal median months, sigma
DEATH_RATE = 0.00006


def g_of(d):
    for a, b, v in G_BANDS:
        if a <= d < b:
            return v
    return G_BANDS[-1][2]


def make_people(n, rng, first_release_lo, first_release_hi, prefix_num):
    """people with a first release in [lo, hi): covariates, latent frailty, term to the maximum date"""
    span = (first_release_hi - first_release_lo).days
    ppl = []
    for k in range(n):
        off = OFFENCES[rng.choice(4, p=OFF_P)]
        dist = DISTRICTS[rng.choice(4, p=DIST_P)]
        age = float(np.clip(rng.gamma(9.0, 4.2) + 18, 19, 74))
        female = rng.random() < 0.095
        priors = int(min(rng.poisson(0.35 + 0.045 * (age - 19) * rng.random() * 2.2), 11))
        z = rng.gamma(FRAILTY_SHAPE, 1 / FRAILTY_SHAPE)
        rel = add(first_release_lo, int(rng.integers(0, span)))
        term_m = float(np.clip(rng.lognormal(np.log(20.0), 0.55), 6, 84))
        ppl.append(dict(pid=prefix_num + k, off=off, dist=dist, age0=age, female=female, priors=priors,
                        z=float(z), rel0=rel, term0=int(term_m * 30.44)))
    return ppl


def eta_of(p, age, priors):
    return float(-0.034 * (age - 37) + 0.30 * np.log1p(priors) - 0.22 * p["female"] + OFF_ETA[p["off"]]
                 + DIST_ETA[p["dist"]])


def risk_score(p, rng):
    """the Department's Pembroke Release Assessment Tool: items from the record, scored 0 to 24"""
    s = 0
    a = p["age0"]
    s += 6 if a < 23 else 5 if a < 27 else 4 if a < 32 else 3 if a < 40 else 1 if a < 50 else 0
    s += min(p["priors"], 4) * 2
    s += {"Property": 4, "Drug": 3, "Violent": 2, "Public order": 1}[p["off"]]
    s += int(rng.integers(0, 6))          # needs items (employment, housing, peers) scored at the interview
    s += 0 if p["female"] else 1
    return int(min(s, 24))


def level(score):
    return "Low" if score <= 7 else "Moderate" if score <= 12 else "High" if score <= 17 else "Very high"


def history_people():
    rng = stream("people/history")
    return make_people(34000, rng, RECORD_START, CUT, 3_100_000)


def new_cohort_people(n=4300):
    rng = stream("people/cohort2027")
    return make_people(n, rng, dt.date(2027, 1, 1), dt.date(2028, 1, 1), 3_900_000)
