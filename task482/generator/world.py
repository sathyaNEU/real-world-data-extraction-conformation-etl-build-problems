"""The world of task482: the Lakemoor Higher Education Coordinating Board's 2027-28 instructional investment grant to
the five public four-year reporting units with the lowest fiscal 2026 instruction expense per FTE student.

A campus's instruction expense follows the credit hours it teaches, and a freshman or sophomore credit hour costs a
fraction of an upper-division hour and far less than a graduate hour. Four parent campuses file one finance return for
themselves and their six branch campuses, which teach mostly lower-division hours; sixteen campuses report alone.

    x = build()    the truth: campuses, credit hours by level and term, FTE, instruction expense, the fall 2026 file"""
import numpy as np

SEED = 4821
COST = {"LD": 205.0, "UD": 431.0, "GR": 764.0}     # instruction expense per credit hour, fiscal 2026
LEVELS = ("LD", "UD", "GR")
TERMS = ("2025FA", "2026SP", "2026SU")
TERM_SHARE = {"2025FA": 0.47, "2026SP": 0.45, "2026SU": 0.08}

# unitid, name, kind (S standalone, P parent, C child), parent unitid, annual credit hours (thousands), share LD, UD,
# GR, efficiency (P and C share their system's)
CAMPUSES = [
    ("214330", "Lakemoor State University", "S", "", 452, 0.30, 0.45, 0.25, None),
    ("214418", "Lakemoor A&M University", "S", "", 610, 0.28, 0.40, 0.32, None),
    ("214506", "Carrow Valley State University", "S", "", 288, 0.66, 0.30, 0.04, None),
    ("214594", "Eastmarch University", "S", "", 336, 0.36, 0.53, 0.11, None),
    ("214682", "Felling State University", "S", "", 214, 0.70, 0.27, 0.03, None),
    ("214770", "Greywell University", "S", "", 377, 0.44, 0.32, 0.24, None),
    ("214858", "Harrowby State University", "S", "", 195, 0.58, 0.39, 0.03, None),
    ("214946", "Inglenook State University", "S", "", 168, 0.72, 0.26, 0.02, None),
    ("215034", "Jessamine University", "S", "", 259, 0.33, 0.49, 0.18, None),
    ("215122", "Kelderton State University", "S", "", 232, 0.52, 0.42, 0.06, None),
    ("215210", "Lowmoor University", "S", "", 304, 0.50, 0.28, 0.22, None),
    ("215298", "Marchbank State University", "S", "", 181, 0.62, 0.36, 0.02, None),
    ("215386", "Northgale University", "S", "", 349, 0.30, 0.46, 0.24, None),
    ("215474", "Orrinford State University", "S", "", 205, 0.60, 0.25, 0.15, None),
    ("215562", "Penmark University", "S", "", 268, 0.40, 0.52, 0.08, None),
    ("215650", "Quarrel Hill State University", "S", "", 176, 0.56, 0.42, 0.02, None),
    ("216102", "University of Lakemoor", "P", "", 820, 0.33, 0.40, 0.27, 0.98),
    ("216190", "University of Lakemoor at Ferris Bend", "C", "216102", 96, 0.81, 0.17, 0.02, 0.98),
    ("216278", "University of Lakemoor at Stoneleigh", "C", "216102", 74, 0.78, 0.20, 0.02, 0.98),
    ("216366", "Western Lakemoor University", "P", "", 402, 0.40, 0.41, 0.19, 1.00),
    ("216454", "Western Lakemoor University at Dunmere", "C", "216366", 63, 0.79, 0.19, 0.02, 1.00),
    ("216542", "Lakemoor Polytechnic University", "P", "", 455, 0.38, 0.42, 0.20, 1.18),
    ("216630", "Lakemoor Polytechnic at Ashby", "C", "216542", 58, 0.74, 0.24, 0.02, 1.18),
    ("216718", "Lakemoor Polytechnic at Corley", "C", "216542", 49, 0.76, 0.22, 0.02, 1.18),
    ("216806", "Southmoor University", "P", "", 318, 0.44, 0.40, 0.16, 1.14),
    ("216894", "Southmoor University at Pell", "C", "216806", 67, 0.72, 0.25, 0.03, 1.14),
]
EFF = {}      # two standalone campuses set apart from the fifth place
IDS = [c[0] for c in CAMPUSES]
KIND = {c[0]: c[2] for c in CAMPUSES}
PARENT = {c[0]: c[3] for c in CAMPUSES}
NAME = {c[0]: c[1] for c in CAMPUSES}


def fte(ch):
    """12-month FTE: undergraduate credit hours over 30 plus graduate credit hours over 24."""
    return (ch["LD"] + ch["UD"]) / 30.0 + ch["GR"] / 24.0


def build(eff=None):
    rng = np.random.default_rng(SEED)
    x = {"ch": {}, "eff": {}, "inst": {}, "fte": {}}
    for uid, name, kind, par, k, ld, ud, gr, e in CAMPUSES:
        tot = k * 1000 * float(rng.uniform(0.985, 1.015))
        ch = {"LD": round(tot * ld), "UD": round(tot * ud), "GR": round(tot * gr)}
        x["ch"][uid] = ch
        x["fte"][uid] = round(fte(ch), 1)
        x["eff"][uid] = float(rng.normal(1.0, 0.025)) if kind == "S" else e
    x["eff"].update(EFF)
    if eff:
        x["eff"].update(eff)
    for uid in IDS:
        x["inst"][uid] = round(x["eff"][uid] * sum(x["ch"][uid][lv] * COST[lv] for lv in LEVELS), 2)
    # the parents' returns carry their branches' instruction expense
    x["reported"] = {}
    for uid in IDS:
        if KIND[uid] == "C":
            x["reported"][uid] = 0.0
        elif KIND[uid] == "P":
            x["reported"][uid] = round(x["inst"][uid] + sum(x["inst"][c] for c in IDS if PARENT[c] == uid), 2)
        else:
            x["reported"][uid] = x["inst"][uid]
    return x


def truth_per_fte(x):
    return {u: x["inst"][u] / x["fte"][u] for u in IDS}
