"""task247 the 2023 post-bleaching survey: four 20 m belt transects at each of the 16 sites, every stony coral colony
of 10 cm or more whose centre lies in the belt, its genus, maximum diameter and condition, entered from the dive
slates one row per line written.

Two of the 2023 volunteers wrote a colony of 100 cm or more on the slate's line for every metre of tape it crossed,
with its full diameter each time; everyone else wrote each colony once, on the metre its centre lies in."""
import datetime as dt

import numpy as np

import estim as E
import params as P

DAYS = [dt.date(2023, 11, 6), dt.date(2023, 11, 7), dt.date(2023, 11, 8), dt.date(2023, 11, 9)]
STAFF = ["LC", "MS", "AV", "JR"]
VOLUNTEERS = ["KT", "DW"]            # wrote a wide colony once per metre crossed
QA_OBSERVER = "AV"

# genus code: (share of colonies, log-mean diameter cm, log-sd, bleaching susceptibility (logit shift))
GENERA = {
    "OFAV": (0.11, 4.25, 0.65, 0.9), "OANN": (0.08, 4.05, 0.60, 0.9), "OFRA": (0.05, 4.10, 0.60, 0.8),
    "MCAV": (0.07, 3.85, 0.60, 0.2), "CNAT": (0.03, 4.25, 0.50, 0.6), "DLAB": (0.03, 3.40, 0.45, 0.5),
    "PSTR": (0.08, 3.30, 0.45, 0.7), "SSID": (0.10, 3.20, 0.60, 0.1), "SINT": (0.04, 2.70, 0.40, -0.2),
    "AAGA": (0.13, 2.60, 0.40, 0.8), "PAST": (0.15, 2.60, 0.40, -0.1), "PPOR": (0.04, 2.80, 0.45, 0.0),
    "MMEA": (0.03, 3.00, 0.40, 0.3), "DSTO": (0.02, 2.50, 0.35, 0.2), "EFAS": (0.02, 2.60, 0.35, -0.3),
    "APAL": (0.02, 4.50, 0.50, 0.6),
}
FIRE = {"MALC": 0.5, "MCOM": 0.5}    # fire corals, not stony corals; some observers wrote them down anyway


def make(W, seed=P.SURVEY_SEED):
    rng = np.random.default_rng(seed)
    D = W["D"]
    yr = np.array([d.year for d in D]); mon = np.array([d.month for d in D])
    se = (yr == 2023) & (mon >= 6) & (mon <= 10)
    mmm = np.round(W["mmm"], 2)
    dhw23 = np.array([E.season_max(W["rep"][s], mmm[s], se) for s in range(P.NSITE)])
    codes = list(GENERA)
    share = np.array([GENERA[g][0] for g in codes]); share = share / share.sum()
    sites_by_day = [list(range(0, 4)), list(range(4, 8)), list(range(8, 12)), list(range(12, 16))]
    rows, transects = [], []
    site_rate = rng.normal(0, 0.35, P.NSITE)
    for k, sites in enumerate(sites_by_day):
        for s in sites:
            comp = share * np.exp(rng.normal(0, 0.3, len(codes)))
            comp = comp / comp.sum()
            # who wrote which transect: the two volunteers each take one, staff the others; staff repeat transect 1
            obs = [STAFF[(s + j) % 4] for j in range(2)] + VOLUNTEERS
            perm = rng.permutation(4)
            obs = [obs[p] for p in perm]
            sheets = [(j + 1, "S", obs[j]) for j in range(4)] + [(1, "QA", QA_OBSERVER if obs[0] != QA_OBSERVER else "JR")]
            depth = P.SITE_DEPTH[s]
            for (tr, sheet, who) in sheets:
                n = int(rng.poisson(46))
                tdepth = depth + round(float(rng.uniform(-0.8, 0.8)), 1)
                if s == 2 and tr == 2 and sheet == "S":
                    tdepth = 4.2                         # laid on the crest: the current at 10 m
                transects.append(dict(site=s, date=DAYS[k], transect=tr, sheet=sheet, observer=who, depth=tdepth))
                cols = []
                for c in range(n):
                    g = codes[int(rng.choice(len(codes), p=comp))]
                    mu, sd = GENERA[g][1], GENERA[g][2]
                    dia = float(np.exp(rng.normal(mu, sd)))
                    dia = int(round(min(dia, 240)))
                    if dia < 10:
                        if who in ("LC", "MS") and rng.random() < 0.6:
                            pass                          # staff also note recruits for the recruitment study
                        else:
                            continue
                    x = float(rng.uniform(0, 20))
                    z = (-0.4 + 0.42 * (dhw23[s] - 8) + GENERA[g][3] + site_rate[s] + 0.75 * np.log(max(dia, 5) / 30.0))
                    pb = 1 / (1 + np.exp(-z))
                    u = rng.random()
                    if rng.random() < 0.02 + 0.006 * max(dhw23[s] - 6, 0):
                        cond = "D"
                    elif rng.random() < 0.03 + 0.03 * min(dia, 200) / 200.0:
                        cond = "P"                        # paling seen in any November, heat or not
                    elif u < pb:
                        cond = rng.choice(["P", "PB", "BL"], p=[0.35, 0.40, 0.25])
                    else:
                        cond = "H"
                    cols.append(dict(genus=g, dia=dia, x=x, cond=str(cond)))
                if who in ("LC", "AV") and sheet == "S":
                    for g in FIRE:
                        for _ in range(int(rng.poisson(1.5))):
                            dia = int(round(float(np.exp(rng.normal(3.2, 0.5)))))
                            cols.append(dict(genus=g, dia=max(dia, 10), x=float(rng.uniform(0, 20)),
                                             cond=str(rng.choice(["H", "P", "PB", "BL"], p=[0.3, 0.25, 0.25, 0.2]))))
                cols.sort(key=lambda r: r["x"])
                for a in range(len(cols)):
                    for b in range(a):
                        ra, rb = cols[a], cols[b]
                        if (ra["dia"] >= 100 and rb["dia"] >= 100 and ra["genus"] == rb["genus"]
                                and ra["dia"] == rb["dia"] and ra["cond"] == rb["cond"]
                                and abs(ra["x"] - rb["x"]) < (ra["dia"] + rb["dia"]) / 200.0 + 1.5):
                            ra["dia"] += 1 + int(rng.integers(0, 3))
                lines = []
                for ci, r in enumerate(cols):
                    first = int(np.floor(r["x"])) + 1
                    if who in VOLUNTEERS and r["dia"] >= 100:
                        lo = int(np.floor(max(r["x"] - r["dia"] / 200.0, 0))) + 1
                        hi = int(np.floor(min(r["x"] + r["dia"] / 200.0, 19.999))) + 1
                        segs = list(range(lo, hi + 1))
                    else:
                        segs = [first]
                    for sg in segs:
                        lines.append(dict(segment=sg, genus=r["genus"], dia=r["dia"], cond=r["cond"],
                                          colony_id=ci))
                lines.sort(key=lambda r: (r["segment"], r["colony_id"]))
                for no, r in enumerate(lines, 1):
                    rows.append(dict(site=s, date=DAYS[k], transect=tr, sheet=sheet, observer=who, depth=tdepth,
                                     segment=r["segment"], line=no, genus=r["genus"], dia=r["dia"], cond=r["cond"],
                                     colony=r["colony_id"]))
    return dict(rows=rows, transects=transects, dhw23=dhw23)
