"""The clean truth for task449 architecture 2: Laurentide's vacancies, the Workshore Job Board's postings and the
survey's sector totals, simulated forward from params.py with one fixed seed.

Nothing here reads target/. pack.py writes the files from this truth; analysis.py reads only the files.
"""
import datetime as dt
import math

import numpy as np

import params as P

DAY0 = P.SIM_START


def d2i(d):
    return (d - DAY0).days


def i2d(i):
    return DAY0 + dt.timedelta(days=int(i))


def luhn_digit(digits):
    s = 0
    for k, ch in enumerate(reversed(digits)):
        n = int(ch)
        if k % 2 == 0:
            n *= 2
            if n > 9:
                n -= 9
        s += n
    return str((10 - s % 10) % 10)


# ---------------------------------------------------------------------------------------------- employers
FIRST_WORDS = ["Northgate", "Riverside", "Lakeshore", "Pinewood", "Saint-Ours", "Hollis", "Tamarack", "Cedar Point",
               "Bayfield", "Marchand", "Kettle Creek", "Brightwater", "Iron Range", "Fairhaven", "Grand Portage",
               "Ashford", "Belle-Rive", "Sandpiper", "Oxbow", "Highland", "Red Willow", "Stonebridge", "Westvale",
               "Duval", "Granger", "Pelletier", "Lindqvist", "Okafor", "Macleod", "Beaulieu", "Harcourt", "Thibodeau",
               "Kowalczyk", "Ferreira", "Nakamura", "Abernethy", "Gauthier", "Desrosiers", "MacInnis", "Halvorsen"]
NOUNS = {
    "AGR": ["Farms", "Orchards", "Greenhouses", "Agri Services", "Cattle Co.", "Berry Farm", "Seed Cleaning"],
    "CON": ["Construction", "Builders", "Contracting", "Electric", "Plumbing & Heating", "Excavating", "Homes", "Civil"],
    "MFG": ["Meats", "Foods", "Fabrication", "Manufacturing", "Machine Works", "Packers", "Metal Products", "Bakery"],
    "TRD": ["Foods", "Hardware", "Market", "Pharmacy", "Home Centre", "Wholesale", "Motors", "Grocery", "Outfitters"],
    "TRW": ["Transport", "Logistics", "Freight", "Trucking", "Distribution", "Cartage", "Warehousing"],
    "PBA": ["Consulting", "Software", "Staffing", "Cleaning Services", "Business Services", "Systems", "Accounting"],
    "EDU": ["Academy", "Learning Centre", "Montessori", "Language School", "Training Institute"],
    "HCS": ["Home Care", "Lodge", "Care Centre", "Medical Clinic", "Seniors Residence", "Child Care Centre", "Wellness"],
    "AFS": ["Grill", "Bistro", "Inn", "Diner", "Pizzeria", "Cafe", "Hotel", "Restaurant", "Brasserie", "Catering"],
    "OSP": ["Auto Service", "Collision", "Repairs", "Community Association", "Golf Club", "Recreation Society"],
}
SUFFIX = ["Ltd.", "Inc.", "Ltd.", "Corp.", "Ltd.", "Inc.", "Ltee", "Co-operative Ltd.", "Partnership", "Ltd."]
NAICS = {
    "AGR": ["111419", "111330", "112110", "115110", "111110"],
    "CON": ["236110", "238210", "238220", "237310", "236220", "238910"],
    "MFG": ["311611", "311814", "332319", "333990", "311119", "311410"],
    "TRD": ["445110", "444130", "446110", "413190", "441110", "448140", "452999"],
    "TRW": ["484121", "484110", "493110", "488510", "492210"],
    "PBA": ["541510", "561320", "561722", "541211", "561110", "518210"],
    "EDU": ["611110", "611690", "611630"],
    "HCS": ["623110", "621111", "624410", "623310", "621610", "622111"],
    "AFS": ["722511", "722512", "721111", "722320", "722410"],
    "OSP": ["811111", "811121", "813410", "713910", "911910", "912910"],
}
PUBLIC = {  # public employers: managed through employer services (operating names)
    "HCS": ["Laurentide Health Authority", "Saint-Ours Regional Health Centre", "Northern Shield Health District"],
    "EDU": ["Capital School Division", "Lakeshore School Division", "Pinewood Valley School Division",
            "Conseil scolaire francophone de la Laurentide"],
    "OSP": ["Government of Laurentide", "City of Port Laurent", "Town of Saint-Ours"],
}


def make_employers(rng):
    emps = []
    used_num = set()
    used_bn = set()
    for sc in P.SECTOR_CODES:
        n_s = {"AGR": 70, "CON": 190, "MFG": 110, "TRD": 260, "TRW": 90, "PBA": 200, "EDU": 40,
               "HCS": 190, "AFS": 240, "OSP": 150}[sc]
        for k in range(n_s):
            public = False
            name = None
            if sc in PUBLIC and k < len(PUBLIC[sc]):
                public = True
                name = PUBLIC[sc][k]
            chan = "E" if public else ("E" if rng.random() < {"EDU": 0.45, "HCS": 0.40}.get(sc, 0.30) else "S")
            while True:
                num = "%06d" % rng.integers(100000, 999999)
                num = num + luhn_digit(num)
                if num not in used_num:
                    used_num.add(num)
                    break
            while True:
                bn = "%08d" % rng.integers(10000000, 99999999)
                bn = bn + luhn_digit(bn)
                if bn not in used_bn:
                    used_bn.add(bn)
                    break
            if name is None:
                shape = rng.random()
                fw = FIRST_WORDS[rng.integers(len(FIRST_WORDS))]
                nn = NOUNS[sc][rng.integers(len(NOUNS[sc]))]
                if shape < 0.62:
                    legal = "%s %s %s" % (fw, nn, SUFFIX[rng.integers(len(SUFFIX))])
                    oper = "%s %s" % (fw, nn)
                elif shape < 0.80:
                    legal = "%d Laurentide %s" % (rng.integers(100000, 999999), SUFFIX[rng.integers(len(SUFFIX))])
                    oper = "%s %s" % (fw, nn)
                elif shape < 0.92:
                    legal = "%s & %s %s" % (fw, FIRST_WORDS[rng.integers(len(FIRST_WORDS))], SUFFIX[rng.integers(len(SUFFIX))])
                    oper = "%s %s" % (fw, nn)
                else:
                    legal = "%s %s" % (fw, nn)
                    oper = legal
            else:
                legal = name
                oper = name
            size = float(rng.lognormal(0.0, 0.9)) * (6.0 if public else 1.0)
            emps.append({
                "employer_no": num, "bn9": bn, "sector": sc, "naics": NAICS[sc][rng.integers(len(NAICS[sc]))],
                "legal_name": legal, "operating_name": oper, "public": public, "channel": chan,
                "diligent": bool(rng.random() < P.DILIGENT_SHARE), "speed": float(rng.lognormal(0.0, P.EMPLOYER_SPEED_SD)),
                "size": size,
            })
    return emps


# ---------------------------------------------------------------------------------------------- vacancies
def weibull_scale(median, k):
    return median / (math.log(2.0) ** (1.0 / k))


def occupation_cells():
    """(occ, sector, weight, s_share, median, stock, seasonal, schedule_a) for every posting occupation."""
    cells = []
    for o in P.OCCUPATIONS:
        code, title, c16, sw, s_share, med, stock, seas, js = o
        for sc, w in sw.items():
            cells.append((code, sc, w, s_share, med, stock * w, seas, True))
    for o in P.OTHER_OCCUPATIONS:
        code, title, c16, sc, s_share, med, stock, seas = o
        cells.append((code, sc, 1.0, s_share, med, stock, seas, False))
    return cells


def simulate(rng=None):
    rng = rng or np.random.default_rng(P.SEED)
    emps = make_employers(rng)
    by_sc_ch = {}
    for i, e in enumerate(emps):
        by_sc_ch.setdefault((e["sector"], e["channel"]), []).append(i)
    pool_p = {}
    for key, idx in by_sc_ch.items():
        w = np.array([emps[i]["size"] for i in idx])
        pool_p[key] = (np.array(idx), w / w.sum())
    sec_cov = {s[0]: s[3] for s in P.SECTORS}
    pos_vals = np.array([p for p, _ in P.POSITIONS])
    pos_w = np.array([w for _, w in P.POSITIONS])
    mean_pos = float((pos_vals * pos_w).sum())
    n_days = d2i(P.EXTRACT) + 1
    month_of_day = np.array([i2d(i).month for i in range(n_days)])
    k = P.WEIBULL_SHAPE
    gamma_mean = math.gamma(1.0 + 1.0 / k)
    vac = []   # one dict per vacancy (requisition)
    for (code, sc, w, s_share, med, stock, seas, sched) in occupation_cells():
        scale = weibull_scale(med, k)
        mean_T = scale * gamma_mean
        lam = stock / mean_T / mean_pos * np.array([P.SEASONAL[seas][m - 1] for m in month_of_day])
        counts = rng.poisson(lam)
        for day in np.nonzero(counts)[0]:
            for _ in range(int(counts[day])):
                posted = rng.random() < sec_cov[sc]
                if posted:
                    ch = "S" if rng.random() < s_share else "E"
                    key = (sc, ch)
                    if key not in pool_p:
                        key = (sc, "S" if ch == "E" else "E")
                        ch = key[1]
                    idx, pp = pool_p[key]
                    ei = int(idx[np.searchsorted(np.cumsum(pp), rng.random())])
                else:
                    ch = None
                    ei = None
                spd = emps[ei]["speed"] if ei is not None else float(rng.lognormal(0.0, P.EMPLOYER_SPEED_SD))
                T = scale * spd * (-math.log(1.0 - rng.random())) ** (1.0 / k)
                t_days = max(1, int(math.ceil(T)))
                npos = int(pos_vals[np.searchsorted(np.cumsum(pos_w), rng.random())])
                vac.append({"occ": code, "sector": sc, "start": int(day), "T": t_days, "positions": npos,
                            "posted": posted, "channel": ch, "emp": ei, "sched": sched})
    # board behaviour for posted vacancies
    for v in vac:
        if not v["posted"]:
            continue
        if v["channel"] == "E":
            v["withdrawn"] = bool(rng.random() < P.WITHDRAWN_SHARE)
            v["listing_end"] = v["start"] + v["T"]          # first day not live
            v["end_kind"] = "CLOSED"
            v["renewals"] = []
        else:
            e = emps[v["emp"]]
            r = P.DILIGENT_REMOVAL if e["diligent"] else P.LAX_REMOVAL
            j = (v["T"] - 1) // P.TERM_DAYS                  # the term the job ends in
            v["renewals"] = [v["start"] + P.TERM_DAYS * (m + 1) for m in range(j)]
            if rng.random() < r:
                v["listing_end"] = v["start"] + v["T"]
                v["end_kind"] = "REMOVED"
            else:
                v["listing_end"] = v["start"] + P.TERM_DAYS * (j + 1)
                v["end_kind"] = "EXPIRED"
            v["withdrawn"] = False
    return emps, vac


def true_stock(vac, day, sector=None):
    """Positions unfilled on `day` (all employers): the survey's concept."""
    s = 0
    for v in vac:
        if v["start"] <= day < v["start"] + v["T"] and (sector is None or v["sector"] == sector):
            s += v["positions"]
    return s


if __name__ == "__main__":
    emps, vac = simulate()
    print(len(emps), "employers", len(vac), "vacancies", sum(v["posted"] for v in vac), "posted")
