"""The clean truth for task259 architecture 2: the Tamarack Household Employment Survey (HES), 2025Q1 to 2026Q3.

Everything here is the world before any export convention is applied. pack.py writes the bundle from it.
"""
import numpy as np

SEED = 25902
QUARTERS = ["2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2", "2026Q3"]
REF_QUARTERS = ["2025Q4", "2026Q1", "2026Q2", "2026Q3"]
MIGRATION_Q = "2026Q2"          # the CAPI system change: household ids re-keyed from this quarter
FIELD_MONTH = {"2025Q1": (2025, 2), "2025Q2": (2025, 5), "2025Q3": (2025, 8), "2025Q4": (2025, 11),
               "2026Q1": (2026, 2), "2026Q2": (2026, 5), "2026Q3": (2026, 8)}

# Workforce areas. code, name, counties (3-digit), adults 16+ (thousands), MJH logit shift, away shift,
# share of households with one adult.
AREAS = [
    ("01", "Capital Region",   ["019", "023"],        612.4, -0.36, 0.00, 0.44),
    ("02", "Northern Basin",   ["003", "011", "037"], 228.9, 0.06, 0.35, 0.12),
    ("03", "Silver Creek",     ["041", "045"],        301.7, 0.25, 0.00, 0.40),
    ("04", "High Plains",      ["005", "013", "029", "047"], 164.2, -0.62, 0.08, 0.28),
    ("05", "Upper River",      ["007", "031"],        257.3, 0.12, 0.08, 0.28),
    ("06", "Southwest Lakes",  ["015", "021", "033"], 183.6, -0.33, 0.22, 0.14),
    ("07", "Eastern Prairie",  ["009", "027", "041"], 141.8, 0.00, 0.31, 0.12),
    ("08", "Timber Country",   ["001", "017", "025", "035"], 205.5, -0.15, -0.30, 0.66),
]
# county 041 is split between Silver Creek (03) and Eastern Prairie (07) by ZIP code
SPLIT_COUNTY = "041"
SPLIT_ZIPS_07 = ["59362", "59365", "59368", "59371"]
SPLIT_ZIPS_03 = ["59340", "59343", "59347", "59350", "59353"]

# Measurement parameters (the world's own facts; pack.py never reads them into a file)
S_PROXY = 0.55           # chance a household member answering for an absent adult reports a second job the adult holds
FP_PROXY = 0.002         # chance the answering member reports a second job the adult does not hold
PERSIST = 0.97           # a second job held one quarter is still held the next with this chance
AWAY_HOLD = 0.20         # extra chance an adult who holds a second job is out when the interviewer calls
ALLOC_SCALE = 3.0        # sample size multiplier on the base allocation
STREAM = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0}   # per-area stream offsets


def area_index():
    return {a[0]: i for i, a in enumerate(AREAS)}


def build_world(seed=SEED):
    # each area draws from its own streams, so an area's households do not depend on another area's draws
    streams = {a[0]: [np.random.default_rng([seed, i, k, STREAM[a[0]]]) for k in range(3)] for i, a in enumerate(AREAS)}
    rng_ops = np.random.default_rng(seed + 3)

    # Addresses issued: one rotation group enters each quarter and stays four quarters. Entry quarters run from
    # three quarters before 2025Q1 to 2026Q3, so every quarter in QUARTERS has four groups in sample.
    entries = list(range(-3, len(QUARTERS)))
    # allocation per area per rotation group (smaller areas take a larger share of their frame)
    alloc = {k: int(round(v * ALLOC_SCALE)) for k, v in
             {"01": 352, "02": 214, "03": 248, "04": 190, "05": 232, "06": 196, "07": 176, "08": 210}.items()}
    frame_size = {"01": 268400, "02": 104300, "03": 133900, "04": 79800, "05": 116200, "06": 86700,
                  "07": 66400, "08": 97100}
    addresses = []
    aid = 0
    for e in entries:
        for code, nm, ctys, adults, mshift, ashift, _p1 in AREAS:
            rng_hh = streams[code][0]
            for k in range(alloc[code]):
                aid += 1
                cty = ctys[rng_hh.integers(len(ctys))]
                if cty == SPLIT_COUNTY:
                    zips = SPLIT_ZIPS_03 if code == "03" else SPLIT_ZIPS_07
                    zp = zips[rng_hh.integers(len(zips))]
                else:
                    zp = "59%03d" % (100 + (int(cty) * 7 + rng_hh.integers(0, 6)) % 800)
                addresses.append(dict(aid=aid, entry=e, area=code, county=cty, zip=zp))

    # Households and persons. Each occupied address holds a household; a mover replaces it with prob 0.025 a quarter.
    def new_household(area_code):
        rng_hh = streams[area_code][0]
        ai = area_index()[area_code]
        p1 = AREAS[ai][6]
        n_ad = int(rng_hh.choice([1, 2, 3, 4], p=[p1, (1 - p1) * 0.64, (1 - p1) * 0.24, (1 - p1) * 0.12]))
        mem = []
        mshift = AREAS[ai][4]
        for j in range(n_ad):
            if j == 0:
                rel = 1
                age = int(rng_hh.integers(22, 80))
            elif j == 1 and n_ad >= 2 and rng_hh.random() < 0.82:
                rel = 2
                age = int(np.clip(mem[0]["age"] + rng_hh.integers(-6, 7), 19, 84))
            else:
                rel = int(rng_hh.choice([3, 4, 5], p=[0.62, 0.18, 0.20]))
                age = int(rng_hh.integers(16, 30)) if rel == 3 else int(rng_hh.integers(18, 85))
            sex = int(rng_hh.integers(1, 3))
            if j == 1 and rel == 2:
                sex = 3 - mem[0]["sex"] if rng_hh.random() < 0.93 else mem[0]["sex"]
            emp_p = 0.80 if 22 <= age < 60 else (0.55 if age < 22 else (0.52 if age < 66 else 0.16))
            emp = rng_hh.random() < emp_p
            pt = bool(rng_hh.random() < (0.32 if (age < 25 or age >= 60) else 0.17))
            occ = int(rng_hh.choice([11, 13, 15, 25, 29, 35, 37, 41, 43, 47, 49, 51, 53],
                                    p=[.08, .06, .05, .07, .07, .09, .04, .09, .10, .08, .06, .08, .13]))
            lp = (-3.02 + mshift + 0.55 * pt + 0.30 * (occ in (29, 35, 37, 41)) + 0.20 * (age < 35)
                  - 0.45 * (age >= 58) + rng_hh.normal(0, 0.85))
            mem.append(dict(rel=rel, age0=age, age=age, sex=sex, emp0=emp, pt=pt, occ=occ, lp=lp, mjh=None,
                            pid=int(rng_hh.integers(10 ** 8, 10 ** 9))))
        return mem

    households = {}
    for a in addresses:
        rng_hh = streams[a["area"]][0]
        a["occupied0"] = bool(rng_hh.random() < 0.905)
        a["vacant_from"] = None
        if a["occupied0"] and rng_hh.random() < 0.035:
            # becomes vacant or is demolished partway through its panel (found by the frame maintenance crew)
            a["vacant_from"] = a["entry"] + int(rng_hh.integers(1, 4))
            a["vacant_kind"] = "DEMOLISHED" if rng_hh.random() < 0.3 else "VACANT"
        households[a["aid"]] = None

    persons_q = []     # person-quarter clean truth
    hh_q = []          # address-quarter clean truth
    ai_map = area_index()
    for a in addresses:
        rng_hh, rng_p, rng_q = streams[a["area"]]
        mem = None
        hh_seq = 0
        for w in range(4):
            qi = a["entry"] + w
            occupied = a["occupied0"] and not (a["vacant_from"] is not None and qi >= a["vacant_from"])
            if occupied and (mem is None or rng_hh.random() < 0.025):
                mem = new_household(a["area"])
                hh_seq += 1
            if not occupied:
                mem = None
            # true statuses evolve every quarter, observed or not
            if mem is not None:
                for m in mem:
                    m["age"] = m["age0"] + (qi - a["entry"]) // 4
                    if m["emp0"] and rng_p.random() < 0.02:
                        m["emp0"] = False
                    elif (not m["emp0"]) and m["age"] < 64 and rng_p.random() < 0.03:
                        m["emp0"] = True
                    if not m["emp0"]:
                        m["mjh"] = 0
                    else:
                        p = 1.0 / (1.0 + np.exp(-m["lp"]))
                        if m["mjh"] is None:
                            m["mjh"] = int(rng_p.random() < p)
                        elif rng_p.random() >= PERSIST:
                            m["mjh"] = int(rng_p.random() < p)
            if qi < 0 or qi >= len(QUARTERS):
                continue
            q = QUARTERS[qi]
            rec = dict(aid=a["aid"], q=q, qi=qi, wave=w + 1, area=a["area"], county=a["county"], zip=a["zip"],
                       entry=a["entry"], occupied=occupied, hh_seq=hh_seq,
                       vacant_kind=(a.get("vacant_kind") if not occupied and a["occupied0"] else
                                    ("NOT_A_DWELLING" if not a["occupied0"] else None)))
            if not occupied:
                rec.update(outcome="INELIGIBLE", n_adults=0)
                hh_q.append(rec)
                continue
            # household response
            ashift = AREAS[ai_map[a["area"]]][5]
            p_resp = 0.74 - 0.04 * (w == 0) + 0.02 * (w >= 2) - 0.25 * ashift
            r = rng_q.random()
            if r < p_resp:
                outcome = "COMPLETE"
            elif r < p_resp + 0.11:
                outcome = "REFUSED"
            else:
                outcome = "NONCONTACT"
            converted = outcome == "REFUSED" and rng_q.random() < 0.18
            rec.update(outcome=("COMPLETE" if converted else outcome), refusal_converted=converted,
                       n_adults=len(mem))
            # interview timing: weekday evening, weekday daytime or Saturday
            slot = rng_q.choice(["EVE", "DAY", "SAT"], p=[0.58, 0.16, 0.26])
            rec["slot"] = str(slot)
            hh_q.append(rec)
            if rec["outcome"] != "COMPLETE":
                continue
            # who is home: the household respondent is the first adult present
            present = []
            for j, m in enumerate(mem):
                emp = m["emp0"]
                base = {"EVE": 0.24, "DAY": 0.38, "SAT": 0.28}[str(slot)]
                p_away = base + 0.16 * emp * (0.5 if m["pt"] else 1.0) + ashift + AWAY_HOLD * (m["mjh"] == 1)
                p_away += 0.06 * (m["age"] < 25)
                present.append(rng_q.random() >= min(0.92, p_away))
            if not any(present):
                present[0] = True     # the interviewer comes back until someone answers
            resp = [j for j, pr in enumerate(present) if pr][0]
            for j, m in enumerate(mem):
                emp = m["emp0"]
                self_rep = present[j]
                if not emp:
                    rep = -1
                elif self_rep:
                    rep = int(m["mjh"] == 1)
                else:
                    rep = int(rng_q.random() < (S_PROXY if m["mjh"] == 1 else FP_PROXY))
                # unemployed vs out of the labour force; want a job among those out of the labour force
                if emp:
                    lfs = 1 if rng_q.random() > 0.03 else 2
                    want = -1
                else:
                    looking = rng_q.random() < (0.13 if m["age"] < 60 else 0.02)
                    lfs = 3 if looking else 4
                    want = (1 if (rng_q.random() < (0.09 if m["age"] < 60 else 0.03)) else 2) if lfs == 4 else -1
                persons_q.append(dict(aid=a["aid"], hh_seq=hh_seq, q=q, qi=qi, wave=w + 1, area=a["area"],
                                      county=a["county"], zip=a["zip"], line=j + 1, pid=m["pid"], rel=m["rel"],
                                      age=m["age"], sex=m["sex"], lfs=lfs, pt=m["pt"], occ=m["occ"],
                                      mjh_true=int(m["mjh"] == 1) if emp else -1, mjh_rep=rep,
                                      self_rep=bool(self_rep), resp_line=(j + 1 if self_rep else resp + 1), want=want,
                                      slot=str(slot)))
    return dict(addresses=addresses, hh_q=hh_q, persons_q=persons_q, frame_size=frame_size, alloc=alloc,
                rng_ops=rng_ops, addr_by_id={a["aid"]: a for a in addresses})
