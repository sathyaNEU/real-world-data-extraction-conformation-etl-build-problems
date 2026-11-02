"""task483 world: Hollinbrook Health Federation's member practices, their UTI consultations and antibiotic issues,
and the urine cultures and renal results the pathology laboratory reported for their patients, 2024 to 2026.

The clean truth. Every record a file ships is drawn here from the process that makes it: a woman consults with
symptoms of lower urinary tract infection, the practice issues a first course, sometimes sends a urine culture
at that consultation, and when the course fails she comes back and the practice nearly always cultures then. One
culture reports its organism against every drug on the panel. Nothing is placed to be caught; the mess is added
in pack.py the way each producing system writes its records.
"""
import datetime as dt
from collections import defaultdict

import numpy as np

D = dt.date
TD = dt.timedelta
START, END = D(2024, 1, 1), D(2026, 12, 31)
YEARS = (2024, 2025, 2026)
SEED = 483099

DRUGS = ("NIT", "TMP", "MEC", "CEX", "AMC", "FOS", "AMX")
OFF = ("TMP", "MEC", "CEX", "AMC", "FOS", "AMX")
PANEL = ("AMX", "AMC", "CEX", "CPD", "CIP", "FOS", "GEN", "MEC", "NIT", "TMP", "ETP")
ORGS = ("ECOL", "SSAP", "KPNE", "KOXY", "KAER", "PMIR", "MMOR", "EFAE", "CFRE", "ECLO", "PAER", "SAGA")
LIMS_GO_LIVE = D(2026, 9, 7)     # the pathology network's new laboratory system takes every specimen from this day

# --- networks and practices ------------------------------------------------------------------------------------
# name, PCN code, practices: (code, name, women 16-64 on the list, clinical system)
NETWORKS = [
    ("Kesterby", "U47318", [("J83014", "Kesterby Medical Centre", 9960, "EMIS"),
                            ("J83207", "The Old Forge Surgery", 5790, "EMIS"),
                            ("J83351", "Dr N Okafor & Partners", 6900, "SystmOne"),
                            ("J83088", "Linthwaite Road Surgery", 4530, "EMIS")]),
    ("Ashwell Vale", "U52906", [("J83119", "Ashwell Vale Health Centre", 10400, "EMIS"),
                                ("J83402", "Priory Lane Surgery", 5490, "EMIS"),
                                ("J83066", "Cotterill Street Practice", 6120, "SystmOne")]),
    ("Morrow Cross", "U38841", [("J83025", "Morrow Cross Group Practice", 12720, "SystmOne"),
                                ("J83290", "St Aldhelm's Surgery", 6420, "SystmOne"),
                                ("J83463", "Brookfield Medical Practice", 5220, "EMIS"),
                                ("J83137", "The Willows Surgery", 4840, "SystmOne")]),
    ("Tamsey", "U61257", [("J83371", "Tamsey Family Practice", 9640, "EMIS"),
                          ("J83048", "Hadley Green Surgery", 6750, "EMIS"),
                          ("J83226", "Mill Race Medical Centre", 6020, "SystmOne"),
                          ("J83514", "Dr A Haworth & Partners", 3810, "EMIS")]),
    ("Stanbridge North", "U29470", [("J83102", "Hollin Lane Medical Practice", 8920, "SystmOne"),
                                    ("J83386", "Stanbridge Road Surgery", 4350, "SystmOne"),
                                    ("J83255", "Northgate Health Partnership", 7830, "EMIS"),
                                    ("J83077", "Quarry Bank Surgery", 5320, "EMIS")]),
    ("Upper Lode", "U73015", [("J83440", "Upper Lode Surgery", 8020, "EMIS"),
                              ("J83163", "Fernbrook Practice", 6560, "EMIS"),
                              ("J83318", "Riverside Medical Centre, Lode", 5100, "SystmOne")]),
    ("Brackenholt", "U85142", [("J83059", "Brackenholt Health Partnership", 11220, "EMIS"),
                               ("J83281", "Market Street Surgery", 5000, "SystmOne"),
                               ("J83497", "Coldwell Surgery", 5970, "EMIS")]),
]
MERGE_FROM, MERGE_INTO, MERGE_DAY = "J83386", "J83102", D(2026, 7, 1)   # Stanbridge Road into Hollin Lane
HUB = "Y07214"                                                        # the federation's extended access hub

# each network's first-course drug mix for women 16 to 64 (nitrofurantoin and the rest), stable 2024 to 2026
MIX = {
    "Kesterby":         {"NIT": 0.785, "TMP": 0.175, "MEC": 0.012, "CEX": 0.012, "AMC": 0.008, "FOS": 0.004, "AMX": 0.004},
    "Ashwell Vale":     {"NIT": 0.740, "TMP": 0.190, "CEX": 0.032, "AMC": 0.020, "MEC": 0.010, "FOS": 0.004, "AMX": 0.004},
    "Morrow Cross":     {"NIT": 0.598, "MEC": 0.264, "FOS": 0.100, "AMC": 0.016, "TMP": 0.012, "CEX": 0.006, "AMX": 0.004},
    "Tamsey":           {"NIT": 0.549, "MEC": 0.190, "FOS": 0.200, "TMP": 0.026, "AMC": 0.022, "CEX": 0.008, "AMX": 0.005},
    "Stanbridge North": {"NIT": 0.480, "CEX": 0.170, "AMC": 0.170, "FOS": 0.140, "TMP": 0.016, "MEC": 0.008, "AMX": 0.006},
    "Upper Lode":       {"NIT": 0.680, "MEC": 0.280, "AMC": 0.016, "CEX": 0.012, "TMP": 0.006, "FOS": 0.004, "AMX": 0.002},
    "Brackenholt":      {"NIT": 0.800, "TMP": 0.070, "CEX": 0.052, "AMC": 0.044, "MEC": 0.024, "FOS": 0.006, "AMX": 0.004},
}

# --- the process ---------------------------------------------------------------------------------------------------
EPISODE_RATE = 0.100          # mean new lower-UTI episodes a woman aged 16 to 64 a year (heterogeneous)
P_PREG = 0.022                # share of episodes in women 16 to 44 that are in pregnancy
OUTCOME = {"POS": 0.635, "MIX": 0.090, "NSG": 0.275}
P_CULT_PRES = 0.100           # culture sent at the first consultation (no relation to the organism)
P_FAIL_R = 0.66               # a course against a resistant organism fails
P_FAIL_R_GPOS = {("MEC", "SSAP"): 0.25, ("MEC", "SAGA"): 0.25}   # pivmecillinam's urinary levels still clear some
S_SAP_RESPONSE = 0.6          # an uncomplicated S. saprophyticus infection on an active drug fails less often
P_FAIL_S = {"NIT": 0.112, "TMP": 0.094, "MEC": 0.072, "CEX": 0.101, "AMC": 0.098, "FOS": 0.128, "AMX": 0.104}
P_FAIL_NEG = 0.052
P_CULT_FAIL = 0.90            # culture sent when she comes back
REFRACTORY = 35               # days before a later consultation is a new episode

# organism mix of culture-positive episodes, women 16 to 64 (S. saprophyticus by age)
def org_mix_women(age):
    ss = 0.165 if age < 30 else (0.105 if age < 45 else 0.048)
    rest = {"ECOL": 0.785, "KPNE": 0.056, "PMIR": 0.054, "EFAE": 0.034, "CFRE": 0.022, "ECLO": 0.018, "SAGA": 0.029}
    t = sum(rest.values())
    out = {k: v / t * (1 - ss) for k, v in rest.items()}
    out["SSAP"] = ss
    return out

ORG_OLDER = {"ECOL": 0.585, "KPNE": 0.104, "KOXY": 0.016, "KAER": 0.013, "PMIR": 0.078, "MMOR": 0.008, "EFAE": 0.088,
             "PAER": 0.033, "CFRE": 0.024, "ECLO": 0.031, "SAGA": 0.020}
ORG_MEN = {"ECOL": 0.548, "KPNE": 0.097, "KOXY": 0.014, "KAER": 0.014, "PMIR": 0.079, "MMOR": 0.010, "EFAE": 0.116,
           "PAER": 0.038, "CFRE": 0.026, "ECLO": 0.038, "SAGA": 0.020}

# E. coli phenotypes: share and the drugs each is resistant to (probabilities for partial members)
ECOLI_PHENO = [
    ("S", 0.575, {}),
    ("A", 0.172, {"AMX": 1}),
    ("AT", 0.098, {"AMX": 1, "TMP": 1}),
    ("ATC", 0.040, {"AMX": 1, "TMP": 1, "AMC": 1, "CIP": 0.25}),
    ("ESBL", 0.030, {"AMX": 1, "AMC": 0.6, "CEX": 1, "CPD": 1, "TMP": 0.7, "CIP": 0.55, "MEC": 0.18, "FOS": 0.06,
                     "NIT": 0.05, "GEN": 0.2}),
    ("M", 0.034, {"MEC": 1, "AMX": 0.3}),
    ("N", 0.016, {"NIT": 1, "TMP": 0.6, "AMX": 0.5}),
    ("T", 0.035, {"TMP": 1}),
]
OTHER_RES = {
    "SSAP": {"NIT": 0.0, "MEC": 1.0, "FOS": 1.0, "TMP": 0.08, "CEX": 0.02, "AMC": 0.02, "AMX": 0.25, "CIP": 0.03},
    "KPNE": {"AMX": 1.0, "NIT": 0.34, "MEC": 0.08, "TMP": 0.22, "CEX": 0.08, "CPD": 0.07, "AMC": 0.10, "FOS": 0.20,
             "CIP": 0.08, "GEN": 0.04},
    "PMIR": {"NIT": 1.0, "MEC": 0.04, "TMP": 0.36, "CEX": 0.05, "CPD": 0.03, "AMC": 0.06, "AMX": 0.30, "FOS": 0.10,
             "CIP": 0.10, "GEN": 0.05},
    "EFAE": {"NIT": 0.02, "MEC": 1.0, "TMP": 1.0, "CEX": 1.0, "CPD": 1.0, "AMC": 0.01, "AMX": 0.01, "CIP": 0.5,
             "GEN": 0.3},
    "CFRE": {"AMX": 1.0, "AMC": 1.0, "CEX": 1.0, "NIT": 0.08, "MEC": 0.10, "TMP": 0.18, "FOS": 0.15, "CPD": 0.15,
             "CIP": 0.08},
    "ECLO": {"AMX": 1.0, "AMC": 1.0, "CEX": 1.0, "NIT": 0.30, "MEC": 0.15, "TMP": 0.15, "FOS": 0.25, "CPD": 0.20,
             "CIP": 0.06},
    "KOXY": {"AMX": 1.0, "NIT": 0.12, "MEC": 0.06, "TMP": 0.12, "CEX": 0.10, "CPD": 0.08, "AMC": 0.10, "FOS": 0.15,
             "CIP": 0.05, "GEN": 0.03},
    "KAER": {"AMX": 1.0, "AMC": 1.0, "CEX": 1.0, "NIT": 0.35, "MEC": 0.12, "TMP": 0.12, "FOS": 0.20, "CPD": 0.20,
             "CIP": 0.05, "GEN": 0.03},
    "MMOR": {"AMX": 1.0, "AMC": 1.0, "CEX": 1.0, "NIT": 1.0, "MEC": 0.05, "TMP": 0.30, "FOS": 0.15, "CPD": 0.05,
             "CIP": 0.12, "GEN": 0.06},
    "PAER": {"AMX": 1.0, "AMC": 1.0, "CEX": 1.0, "CPD": 1.0, "NIT": 1.0, "MEC": 1.0, "TMP": 1.0, "FOS": 1.0,
             "CIP": 0.12, "GEN": 0.05},
    "SAGA": {"NIT": 0.0, "MEC": 1.0, "TMP": 0.20, "CEX": 0.0, "AMC": 0.0, "AMX": 0.0, "FOS": 1.0, "CIP": 0.0},
}
# drugs the laboratory does not report for an organism (blank on its report)
NOT_REPORTED = {"SSAP": {"CPD", "GEN", "ETP"}, "EFAE": {"FOS", "ETP"}, "SAGA": {"CPD", "GEN", "ETP", "CIP"},
                "PAER": {"ETP"}}


def rng_for(*keys):
    return np.random.default_rng([SEED] + [abs(hash_key(k)) for k in keys])


def hash_key(k):
    if isinstance(k, int):
        return k
    h = 2166136261
    for ch in str(k):
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return h


def draw(rng, mix):
    keys = list(mix)
    p = np.array([mix[k] for k in keys], dtype=float)
    p = p / p.sum()
    return keys[int(rng.choice(len(keys), p=p))]


def susceptibility(rng, org, older=False):
    """The organism's report: drug -> 'R' or 'S' (or None where the laboratory reports nothing)."""
    res = {}
    if org == "ECOL":
        ph = ECOLI_PHENO if not older else [(n, s * (1.25 if n not in ("S", "A") else 0.92), r) for n, s, r in ECOLI_PHENO]
        name = draw(rng, {n: s for n, s, _ in ph})
        rset = dict(ph[[n for n, _, _ in ph].index(name)][2])
        for d in PANEL:
            p = rset.get(d, 0.0)
            if d == "FOS" and p == 0.0:
                p = 0.010
            if d == "CIP" and p == 0.0:
                p = 0.03 if not older else 0.07
            res[d] = "R" if rng.random() < p else "S"
    else:
        base = OTHER_RES[org]
        for d in PANEL:
            if d in NOT_REPORTED.get(org, set()):
                res[d] = None
                continue
            p = base.get(d, 0.02)
            if older and p < 1.0:
                p = min(0.95, p * 1.2)
            res[d] = "R" if rng.random() < p else "S"
    if res.get("ETP") is not None:
        res["ETP"] = "S"
    return res


def age_on(birth, day):
    return day.year - birth.year - ((day.month, day.day) < (birth.month, birth.day))


def practices():
    out = []
    for net, pcn, prs in NETWORKS:
        for code, name, women, system in prs:
            out.append({"code": code, "name": name, "network": net, "pcn": pcn, "women": women, "system": system})
    return out


def _episode_dates(rng, lam, n_years=3):
    """New-episode dates over 2024 to 2026 for one woman: a Poisson process with a refractory gap."""
    days = (END - START).days + 1
    n = rng.poisson(lam * n_years)
    if n == 0:
        return []
    ds = sorted(int(x) for x in rng.integers(0, days, size=n))
    out = []
    for x in ds:
        if not out or x - out[-1] >= REFRACTORY + 14:
            out.append(x)
    return [START + TD(days=x) for x in out]


def reconsult_gap(rng):
    return int(rng.choice([3, 4, 5, 6, 7, 8, 9, 10, 11, 12], p=[.07, .14, .18, .16, .13, .10, .08, .06, .05, .03]))


def second_line(rng, first, res_known=None):
    if first == "NIT":
        return draw(rng, {"MEC": 0.46, "FOS": 0.22, "CEX": 0.20, "AMC": 0.12})
    if first == "MEC":
        return draw(rng, {"NIT": 0.55, "FOS": 0.20, "CEX": 0.15, "AMC": 0.10})
    return draw(rng, {"NIT": 0.52, "MEC": 0.28, "FOS": 0.12, "CEX": 0.08})


def women_episodes():
    """Every lower-UTI episode in a woman aged 16 to 64 at a member practice, 2024 to 2026, with what followed."""
    eps = []
    pid = 0
    for pr in practices():
        rng = rng_for("women", pr["code"])
        mix = dict(MIX[pr["network"]])
        # each practice's own habit around its network's mix
        jit = {d: max(0.0005, v * float(rng.lognormal(0, 0.06))) for d, v in mix.items()}
        t = sum(jit.values())
        mix = {d: v / t for d, v in jit.items()}
        lam = rng.gamma(0.55, EPISODE_RATE / 0.55, size=pr["women"])
        for i in range(pr["women"]):
            pid += 1
            dates = _episode_dates(rng, lam[i])
            if not dates:
                continue
            by = int(rng.integers(1960, 2010))
            birth = D(by, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
            for day in dates:
                age = age_on(birth, day)
                if age < 16 or age > 64:
                    continue
                preg = age <= 44 and rng.random() < P_PREG
                eps.append(_episode(rng, pr, pid, birth, day, age, preg, mix))
    return eps


def _episode(rng, pr, pid, birth, day, age, preg, mix):
    e = {"practice": pr["code"], "network": pr["network"], "patient": pid, "birth": birth, "day": day, "age": age,
         "sex": "F", "pregnant": preg, "group": "W"}
    if preg:
        e["drug"] = draw(rng, {"NIT": 0.55, "CEX": 0.33, "AMX": 0.12})
    else:
        e["drug"] = draw(rng, mix)
    oc = draw(rng, OUTCOME)
    e["outcome"] = oc
    if oc == "POS":
        e["org"] = draw(rng, org_mix_women(age))
        e["res"] = susceptibility(rng, e["org"])
    else:
        e["org"], e["res"] = None, {}
    e["cult_pres"] = rng.random() < P_CULT_PRES or preg
    e["cult_pres_lag"] = 0 if rng.random() < 0.72 else 1
    if e["org"]:
        r = e["res"].get(e["drug"]) == "R"
        pf = P_FAIL_R_GPOS.get((e["drug"], e["org"]), P_FAIL_R) if r else P_FAIL_S[e["drug"]]
        if not r and e["org"] == "SSAP":
            pf *= S_SAP_RESPONSE
    else:
        pf = P_FAIL_NEG
    e["failed"] = rng.random() < pf
    e["recon_gap"] = reconsult_gap(rng)
    e["cult_fail"] = e["failed"] and rng.random() < P_CULT_FAIL
    e["cult_fail_lag"] = 0 if rng.random() < 0.75 else 1
    e["second"] = second_line(rng, e["drug"]) if e["failed"] else None
    e["hub"] = rng.random() < 0.06
    e["third"] = None
    if e["failed"] and e["cult_fail"] and e["org"] and e["res"].get(e["second"]) == "R":
        ok = [d for d in ("NIT", "MEC", "FOS", "CEX", "AMC", "TMP") if e["res"].get(d) == "S"]
        if ok:
            e["third"] = ok[0]
    return e


def older_episodes():
    """Women aged 65 and over: episodes, cultures (sent at presentation far more often), first courses."""
    eps = []
    pid = 500000
    for pr in practices():
        rng = rng_for("older", pr["code"])
        n_old = int(pr["women"] * 0.43)
        lam = rng.gamma(0.7, 0.13 / 0.7, size=n_old)
        for i in range(n_old):
            pid += 1
            dates = _episode_dates(rng, lam[i])
            by = int(rng.integers(1925, 1959))
            birth = D(by, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
            for day in dates:
                age = age_on(birth, day)
                if age < 65:
                    continue
                e = {"practice": pr["code"], "network": pr["network"], "patient": pid, "birth": birth, "day": day,
                     "age": age, "sex": "F", "pregnant": False, "group": "O"}
                e["drug"] = draw(rng, {"NIT": 0.50, "TMP": 0.17, "MEC": 0.13, "CEX": 0.11, "AMC": 0.09})
                oc = draw(rng, {"POS": 0.70, "MIX": 0.12, "NSG": 0.18})
                e["outcome"] = oc
                if oc == "POS":
                    e["org"] = draw(rng, ORG_OLDER)
                    e["res"] = susceptibility(rng, e["org"], older=True)
                else:
                    e["org"], e["res"] = None, {}
                e["cult_pres"] = rng.random() < 0.46
                e["cult_pres_lag"] = 0 if rng.random() < 0.6 else 1
                r = e["org"] and e["res"].get(e["drug"]) == "R"
                e["failed"] = rng.random() < (0.55 if r else 0.13)
                e["recon_gap"] = reconsult_gap(rng)
                e["cult_fail"] = e["failed"] and rng.random() < 0.90
                e["cult_fail_lag"] = 0
                e["second"] = second_line(rng, e["drug"]) if e["failed"] else None
                e["third"] = None
                e["hub"] = False
                e["care_home"] = rng.random() < 0.12
                eps.append(e)
    return eps


def men_episodes():
    """Men aged 16 and over: cultured at nearly every first consultation (seven-day courses)."""
    eps = []
    pid = 800000
    for pr in practices():
        rng = rng_for("men", pr["code"])
        n_men = int(pr["women"] * 1.18)
        lam = rng.gamma(0.6, 0.032 / 0.6, size=n_men)
        for i in range(n_men):
            pid += 1
            dates = _episode_dates(rng, lam[i])
            by = int(rng.integers(1930, 2008))
            birth = D(by, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
            for day in dates:
                age = age_on(birth, day)
                if age < 16:
                    continue
                e = {"practice": pr["code"], "network": pr["network"], "patient": pid, "birth": birth, "day": day,
                     "age": age, "sex": "M", "pregnant": False, "group": "M"}
                e["drug"] = draw(rng, {"NIT": 0.33, "TMP": 0.31, "MEC": 0.14, "CEX": 0.09, "AMC": 0.08, "CIP": 0.05})
                oc = draw(rng, {"POS": 0.66, "MIX": 0.10, "NSG": 0.24})
                e["outcome"] = oc
                if oc == "POS":
                    e["org"] = draw(rng, ORG_MEN)
                    e["res"] = susceptibility(rng, e["org"], older=age >= 65)
                else:
                    e["org"], e["res"] = None, {}
                e["cult_pres"] = rng.random() < 0.93
                e["cult_pres_lag"] = 0 if rng.random() < 0.55 else int(rng.choice([1, 2], p=[0.75, 0.25]))
                r = e["org"] and e["res"].get(e["drug"]) == "R"
                e["failed"] = rng.random() < (0.55 if r else 0.12)
                e["recon_gap"] = reconsult_gap(rng)
                e["cult_fail"] = e["failed"] and rng.random() < 0.88
                e["cult_fail_lag"] = 0
                e["second"] = second_line(rng, e["drug"]) if e["failed"] else None
                e["third"] = None
                e["hub"] = rng.random() < 0.05
                eps.append(e)
    return eps


def presentation_truth(eps):
    """Each drug's chance that a first course meets an organism the laboratory reports resistant, over every
    non-pregnant episode in women 16 to 64 (the clean truth the presentation cultures sample)."""
    n = 0
    r = defaultdict(int)
    for e in eps:
        if e["group"] != "W" or e["pregnant"]:
            continue
        n += 1
        if e["org"]:
            for d in DRUGS:
                if e["res"].get(d) == "R":
                    r[d] += 1
    return {d: r[d] / n for d in DRUGS}, n
