"""task193: the world behind Laegemiddelstyrelsen's quarterly prescription-sequence screen.

Extract span 2023-10-01 to 2026-09-30, day indices 0 to 1095.
Clearance period days 0 to 730 (2023-10-01 to 2025-09-30), 24 months.
Screen window days 731 to 1095 (2025-10-01 to 2026-09-30), 365 days.

Everything here is the clean truth: first-ever receipt dates per patient per medicine, and the
dispensing lines that carry them. The mess is applied in pack.py and never touches these dates.
"""
import datetime as dt

import numpy as np

D0 = dt.date(2023, 10, 1)
NDAY = 1096
WIN_A, WIN_B = 731, 1095
CLEAR_A, CLEAR_B = 0, 730
MULTIPLE = 1.25
MIN_PATIENTS = 25
N_PAT = 13000
SEED = 193002
MESS_SEED = 777
PULL_DAY = 1115                      # 2026-10-20, the extract pull
REFERRAL_QUARTER = "2027 Q1"


def day(d):
    return (D0 + dt.timedelta(days=int(d)))


def iso(d):
    return day(d).isoformat()


def dk(d):
    return day(d).strftime("%d-%m-%Y")


def flat():
    return np.ones(NDAY)


def seasonal(base, amp, phase=0.0):
    t = np.arange(NDAY)
    return base * (1.0 + amp * np.sin(2 * np.pi * (t / 365.25 + phase)))


def launch(L):
    p = np.zeros(NDAY)
    p[L:] = (np.arange(L, NDAY) - L) + 1.0
    return p


def peak(a, top, b):
    p = np.zeros(NDAY)
    up = np.arange(a, min(top, NDAY))
    p[a:min(top, NDAY)] = (up - a) / float(top - a)
    dn = np.arange(top, min(b, NDAY))
    p[top:min(b, NDAY)] = 1.0 - (dn - top) / float(b - top)
    return np.maximum(p, 0.0)


# ---------------------------------------------------------------- Annex A, the screened products
# code, brand, atc, profile, incidence, first marketed (day or None), authorisation lapses, holder
PRODUCTS = [
    ("P01", "Dalvextin", "A10BX09", flat(),                    0.185, -1631, None, "H1"),
    ("P02", "Pirenoxol", "M01AH07", seasonal(1.0, 0.18, 0.10), 0.205, -2284, None, "H2"),
    ("P03", "Ternivast", "C10AX18", launch(860),               0.120, 860,   None, "H3"),
    ("P04", "Oxelumab",  "L04AC22", launch(745),               0.150, 745,   None, "H1"),
    ("P05", "Varenadol", "N02AX09", peak(380, 700, 930),       0.330, 380,   930,  "H4"),
    ("P06", "Hestroban", "J01DH08", seasonal(1.0, 0.26, 0.55), 0.215, -948,  None, "H5"),
    ("P07", "Kirunelle", "G03AA18", flat(),                    0.195, -3012, None, "H7"),
    ("P08", "Admirabin", "B01AF05", peak(260, 660, 1010),      0.290, 260,   1010, "H6"),
    ("P09", "Sovraxil",  "R03DX13", peak(60, 700, 1420),       0.235, -1265, None, "H5"),
]
# product -> (successor holder, the day the authorisation transferred)
TRANSFERS = {
    "P09": ("H6", 880),
}
# ---------------------------------------------------------------- Annex B, the marker treatments
# code, name, atc group, profile, incidence
MARKERS = [
    ("M1", "antiemetic",             "A04AD", flat(), 0.500),
    ("M2", "acid-suppressant",       "A02BC", flat(), 0.520),
    ("M3", "gout treatment",         "M04AA", flat(), 0.500),
    ("M4", "loop diuretic",          "C03CA", flat(), 0.500),
    ("M5", "antidepressant",         "N06AB", flat(), 0.500),
    ("M6", "hypnotic",               "N05CF", flat(), 0.505),
    ("M7", "topical corticosteroid", "D07AC", flat(), 0.580),
    ("M8", "antipsychotic",          "N05AH", flat(), 0.030),
]
# how a patient's age band at the window's start multiplies each marker treatment's incidence
AGE_TILT = {
    "M1": [0.92, 0.98, 1.04, 1.08], "M2": [0.74, 0.95, 1.15, 1.26],
    "M3": [0.55, 0.92, 1.24, 1.36], "M4": [0.48, 0.84, 1.28, 1.52],
    "M5": [1.18, 1.10, 0.92, 0.78], "M6": [0.70, 0.93, 1.16, 1.33],
    "M7": [1.14, 1.02, 0.95, 0.88], "M8": [0.86, 1.00, 1.08, 1.12],
}
ANNEX = {
    "P01": ["M4", "M2", "M3"],
    "P02": ["M2", "M6", "M5"],
    "P03": ["M3", "M6", "M1"],
    "P04": ["M5", "M7", "M4"],
    "P05": ["M6", "M1", "M2"],
    "P06": ["M1", "M8"],
    "P07": ["M6", "M8"],
    "P08": ["M4", "M5"],
    "P09": ["M7", "M8"],
}
# (product, marker) -> (probability the product brings the patient to the marker, mean onset lag)
# Solved against the design note's target shares; frozen so the build needs no search.
EFFECTS = {
    ("P01", "M4"): (0.379256, 48.0),
    ("P02", "M2"): (0.330292, 32.0),
    ("P03", "M3"): (0.274811, 45.0),
    ("P04", "M5"): (0.289278, 52.0),
    ("P06", "M1"): (0.426274, 24.0),
    ("P07", "M6"): (0.287018, 38.0),
    ("P09", "M7"): (0.475877, 41.0),
}
# the defined daily dose in milligrams, as the ATC index assigns it. A package's defined daily
# doses are its pack size times its strength divided by this. D07AC carries no defined daily dose.
DDD_MG = {
    "P01": 50.0, "P02": 90.0, "P03": 10.0, "P04": 300.0, "P05": 60.0,
    "P06": 1500.0, "P07": 2.0, "P08": 20.0, "P09": 400.0,
    "M1": 16.0, "M2": 30.0, "M3": 400.0, "M4": 40.0, "M5": 50.0, "M6": 7.5,
    "M7": None, "M8": 20.0,
}
# pack sizes per medicine, as the register's own package list holds them
PACK_SIZES = {
    "P01": [28, 56, 98], "P02": [20, 30, 60], "P03": [28, 98, 100],
    "P04": [1, 2, 6], "P05": [10, 20, 50], "P06": [14, 21, 30],
    "P07": [21, 63, 84], "P08": [28, 56, 100], "P09": [30, 60, 120],
    "M1": [10, 20, 30, 60], "M2": [14, 28, 56, 100], "M3": [30, 50, 100, 200],
    "M4": [20, 30, 60, 100], "M5": [14, 28, 56, 98], "M6": [10, 20, 30, 50],
    "M7": [15, 30, 60, 100], "M8": [20, 28, 50, 98],
}

PCODES = [p[0] for p in PRODUCTS]
MCODES = [m[0] for m in MARKERS]
PNAME = {p[0]: p[1] for p in PRODUCTS}
MNAME = {m[0]: m[1] for m in MARKERS}
PATC = {p[0]: p[2] for p in PRODUCTS}
MATC = {m[0]: m[2] for m in MARKERS}
MARKETED = {p[0]: (p[5], p[6]) for p in PRODUCTS}
HOLDER_OF = {p[0]: p[7] for p in PRODUCTS}
PAIRS = [(p, m) for p in PCODES for m in ANNEX[p]]

# ---------------------------------------------------------------- holders, chains, regions
HOLDERS = [
    ("H1", "Nordlys Pharma A/S", "DK19384417", None),
    ("H2", "Bregnholt Laegemidler A/S", "DK27105538", None),
    ("H3", "Vindeby Therapeutics ApS", "DK38624901", None),
    ("H4", "Soegaard Medica A/S", "DK16770284", None),
    ("H5", "Kastholm Pharma A/S", "DK29441863", None),
    ("H6", "Ellevang Biosciences A/S", "DK41208577", None),
    ("H7", "Strandby Farma ApS", "DK33915642", "H2"),   # merged into H2 on 2026-04-01
]
MERGER_DAY = 913                      # 2026-04-01
TRANSFER_DAY = 880                    # 2026-02-27, Sovraxil's authorisation moves H5 -> H6
CHAINS = [("APK", "Apotekerkaeden"), ("DSA", "Danmarks Sundhedsapotek"),
          ("NOR", "Nordapotek"), ("VST", "Vestjysk Apotek")]
REGIONS = ["Hovedstaden", "Midtjylland", "Nordjylland", "Sjaelland", "Syddanmark"]
REGION_W = [0.316, 0.230, 0.102, 0.147, 0.205]
AGE_BANDS = [(0, 39, "18-39"), (40, 59, "40-59"), (60, 74, "60-74"), (75, 200, "75 and over")]
FEE_BANDS = [(0, 250, 1480), (250, 1000, 1240), (1000, 4000, 1015), (4000, 10 ** 9, 860)]
FEE_BANDS_AMENDED = [(0, 250, 1595), (250, 1000, 1335), (1000, 4000, 1095), (4000, 10 ** 9, 930)]
FEE_AMENDMENT_DAY = 913               # 2026-04-01


def packages():
    """Package codes per medicine: Nordic article numbers as the register issues them."""
    rng = np.random.default_rng(SEED + 7)
    pool = sorted(set(int(x) for x in rng.integers(100000, 599999, size=400)))
    rng.shuffle(pool)
    it = iter(pool)
    out = {}
    for code in PCODES:
        lst = [("%06d" % next(it), code, "product", None, None) for _ in range(3)]
        if code == "P09":                       # reissued at the authorisation transfer
            lst = [(v, c, k, None, TRANSFER_DAY - 1) for v, c, k, _, _ in lst]
            lst += [("%06d" % next(it), code, "product", TRANSFER_DAY, None) for _ in range(3)]
        out[code] = lst
    for code in MCODES:
        out[code] = [("%06d" % next(it), code, "marker", None, None) for _ in range(4)]
    return out


PACKAGES = packages()
PKG_OF = {}
for _c, _lst in PACKAGES.items():
    for _vnr, _code, _kind, _vf, _vt in _lst:
        PKG_OF[_vnr] = (_code, _kind, _vf, _vt)


BIRTH_LO, BIRTH_HI = 1934, 2008


def age_bands(n_pat, seed=SEED + 101):
    """Each patient's year of birth and their age band index at the window's start."""
    rng = np.random.default_rng(seed)
    birth = rng.integers(BIRTH_LO, BIRTH_HI, size=n_pat)
    age = 2025 - birth
    band = np.zeros(n_pat, dtype=int)
    band = np.where(age >= 40, 1, band)
    band = np.where(age >= 60, 2, band)
    band = np.where(age >= 75, 3, band)
    return birth, band


def draw(seed=SEED, n_pat=N_PAT):
    """First-ever receipt day per medicine per patient; -1 where the patient never receives it."""
    rng = np.random.default_rng(seed)
    birth, band = age_bands(n_pat)
    first = {}
    for row in PRODUCTS:
        code, prof, pi = row[0], row[3], row[4]
        p = prof / prof.sum()
        hit = rng.random(n_pat) < pi
        first[code] = np.where(hit, rng.choice(NDAY, size=n_pat, p=p), -1)
    for code, name, atc, prof, pi in MARKERS:
        p = prof / prof.sum()
        tilt = np.array(AGE_TILT[code], dtype=float)
        share = np.bincount(band, minlength=4) / float(n_pat)
        tilt = tilt / float((tilt * share).sum())          # mean preserving
        hit = rng.random(n_pat) < np.clip(pi * tilt[band], 0.0, 0.98)
        first[code] = np.where(hit, rng.choice(NDAY, size=n_pat, p=p), -1)
    for (pc, mc), (e, lag_mean) in EFFECTS.items():
        tp = first[pc]
        fire = (tp >= 0) & (rng.random(n_pat) < e)
        lag = rng.exponential(lag_mean, size=n_pat).astype(int) + 1
        induced = np.where(fire, tp + lag, 10 ** 6)
        induced = np.where(induced < NDAY, induced, 10 ** 6)
        cur = np.where(first[mc] >= 0, first[mc], 10 ** 6)
        new = np.minimum(cur, induced)
        first[mc] = np.where(new < 10 ** 6, new, -1)
    return first


# ---------------------------------------------------------------- the screen, on the clean truth
def pair_rows(first, interval=None, edge=None, per_product_window=False):
    out = []
    for pc, mc in PAIRS:
        a0, b0 = WIN_A, WIN_B
        if per_product_window:
            mf, mt = MARKETED[pc]
            if mf is not None:
                a0 = max(a0, mf)
            if mt is not None:
                b0 = min(b0, mt)
        tp, tm = first[pc], first[mc]
        ok = (tp >= a0) & (tp <= b0) & (tm >= a0) & (tm <= b0) & (tp != tm)
        if edge:
            ok &= (tp >= a0 + edge) & (tp <= b0 - edge)
        t, s = tp[ok], tm[ok]
        if interval is not None:
            keep = np.abs(s - t) <= interval
            t, s = t[keep], s[keep]
        out.append({"product": pc, "marker": mc, "key": pc + "/" + mc, "n": int(len(t)),
                    "after": int((s > t).sum()), "t": t, "s": s, "lo": a0, "hi": b0})
    return out


def expected_perm(t, s):
    """The exchangeability expectation inside the pair: (1/N) #{(i,j): s_j > t_i}."""
    n = len(t)
    if n == 0:
        return 0.0
    ss = np.sort(s)
    return float((n - np.searchsorted(ss, t, side="right")).sum()) / n


def expected_incidence(first, pc, mc, n, lo=WIN_A, hi=WIN_B):
    tp, tm = first[pc], first[mc]
    t = tp[(tp >= lo) & (tp <= hi)]
    s = np.sort(tm[(tm >= lo) & (tm <= hi)])
    if len(t) == 0 or len(s) == 0:
        return 0.5 * n
    return n * float((len(s) - np.searchsorted(s, t, side="right")).sum()) / (len(t) * len(s))


def expected_pairprod(first, mc, t, n, lo=WIN_A, hi=WIN_B):
    tm = first[mc]
    s = np.sort(tm[(tm >= lo) & (tm <= hi)])
    if len(s) == 0 or len(t) == 0:
        return 0.5 * n
    return n * float((len(s) - np.searchsorted(s, t, side="right")).sum()) / (len(t) * len(s))


def expected_even(t, n, lo=WIN_A, hi=WIN_B):
    if len(t) == 0:
        return 0.5 * n
    return n * float(((hi - t) / float(hi - lo + 1)).mean())


ROUTES = ("half", "perm", "incidence", "pairprod", "even")


def expected(first, r, route):
    n = r["n"]
    if route == "half":
        return 0.5 * n
    if route == "perm":
        return expected_perm(r["t"], r["s"])
    if route == "incidence":
        return expected_incidence(first, r["product"], r["marker"], n, r["lo"], r["hi"])
    if route == "pairprod":
        return expected_pairprod(first, r["marker"], r["t"], n, r["lo"], r["hi"])
    if route == "even":
        return expected_even(r["t"], n, r["lo"], r["hi"])
    raise ValueError(route)


def referrals(first, rows, route, multiple=MULTIPLE, minimum=MIN_PATIENTS):
    out, detail = [], {}
    for r in rows:
        if r["n"] < minimum:
            detail[r["key"]] = None
            continue
        e = expected(first, r, route)
        ratio = r["after"] / e if e > 0 else 0.0
        detail[r["key"]] = {"n": r["n"], "after": r["after"], "before": r["n"] - r["after"],
                            "expected": e, "ratio": ratio}
        if ratio >= multiple:
            out.append(r["key"])
    return sorted(out), detail
