"""task286 world: eight shortlisted community areas of an invented English coastal county, every home in them,
who used each home on each day of the extract, the water each home's meter registered, and the councils' and
the rating list's records about the same homes (clean truth plus the records the systems keep).

Deterministic (seed 286). build.py writes the pack from it; checks.py, asks.py and verify.py read it or the pack.
"""
from datetime import date, timedelta

import numpy as np

SEED = 286
EXTRACT_START = date(2025, 9, 1)       # Pennimouth Water's extract: Monday 1 September 2025 ...
EXTRACT_END = date(2026, 10, 4)        # ... to Sunday 4 October 2026 (UTC meter days)
WINDOW_START = date(2025, 9, 29)       # the pilot's 52 weeks: Monday 29 September 2025 ...
WINDOW_END = date(2026, 9, 27)         # ... to Sunday 27 September 2026
NDAYS = (EXTRACT_END - EXTRACT_START).days + 1          # 399
W0 = (WINDOW_START - EXTRACT_START).days                 # 28
W1 = (WINDOW_END - EXTRACT_START).days                   # 391
NWEEKS = 52
ASOF = WINDOW_END                                        # the councils' and the list's records are read for this day
GO_LIVE = date(2026, 5, 5)                               # Teversby's new revenues system (Tuesday after the bank holiday)
SIX_MONTHS_BEFORE = date(2026, 3, 27)                    # more than six months empty on 27 Sep 2026: since before this
USE_MIN = 100                                            # every day somebody is in a home it draws at least this
LEAK_JITTER = 0.012                                      # a steady flow's day-to-day wobble (pressure), fraction
WEEK_RANGE_MIN = 95                                      # a week somebody spends wholly in a home still varies this much

DAYS = [EXTRACT_START + timedelta(days=i) for i in range(NDAYS)]

# type codes
MAIN, WEEKENDER, SEASONAL, LET, EMPTY, PARTYEAR = range(6)
TYPE_NAMES = ["main residence", "weekend home", "seasonal second home", "holiday let", "long-term empty", "part-year"]

# community areas: code, name, district, homes, type mix, the share of older homes (terraces, older flats over
# shops), the chance an empty home is neglected (water left on, the council never told), the chance a neglected
# empty older home runs a cistern or weeps from its supply pipe, the outward postcode and the UPRN block.
AREAS = [
    # code    name          district    homes  MAIN   WKND   SEAS   LET    EMPTY  PART    old   negl  leak  pc     uprn
    ("TV01", "Brackwater", "Teversby", 1010, (0.835, 0.020, 0.020, 0.020, 0.060, 0.045), 0.55, 0.40, 0.30, "PN4", 100041),
    ("TV02", "Wennaby",    "Teversby",  520, (0.780, 0.060, 0.060, 0.030, 0.035, 0.035), 0.35, 0.35, 0.30, "PN6", 100042),
    ("TV03", "Quellby",    "Teversby",  790, (0.896, 0.010, 0.010, 0.009, 0.040, 0.035), 0.20, 0.35, 0.25, "PN5", 100043),
    ("TV04", "Tarnhithe",  "Teversby",  560, (0.680, 0.060, 0.060, 0.120, 0.045, 0.035), 0.60, 0.40, 0.30, "PN9", 100044),
    ("SW01", "Orrimouth",  "Swanholt",  930, (0.705, 0.010, 0.025, 0.015, 0.195, 0.050), 0.85, 0.80, 0.75, "PN11", 100046),
    ("SW02", "Crackmoor",  "Swanholt",  450, (0.820, 0.030, 0.040, 0.020, 0.055, 0.035), 0.65, 0.45, 0.40, "PN14", 100047),
    ("SW03", "Ellingsea",  "Swanholt",  870, (0.750, 0.030, 0.045, 0.035, 0.110, 0.030), 0.10, 0.45, 0.04, "PN12", 100048),
    ("SW04", "Kittlesea",  "Swanholt",  600, (0.672, 0.073, 0.135, 0.050, 0.035, 0.035), 0.45, 0.20, 0.25, "PN15", 100049),
]
AREA_CODES = [a[0] for a in AREAS]
AREA_NAME = {a[0]: a[1] for a in AREAS}
AREA_DISTRICT = {a[0]: a[2] for a in AREAS}
AREA_PC = {a[0]: a[8] for a in AREAS}
AREA_UPRN = {a[0]: a[9] for a in AREAS}

# streets: per area (name, kind) where kind is terrace, semi, detached, flats (a block with a building name) or
# new flats (built 2022 to 2024); every home sits on one, and each street has its own run of postcode units.
STREETS = {
    "TV01": [("Market Street", "flats_old"), ("Sheep Street", "terrace"), ("Station Road", "terrace"),
             ("Chapel Lane", "semi"), ("Mill Lane", "semi"), ("Westgate", "terrace"), ("Priory Close", "detached"),
             ("Tannery Row", "terrace"), ("Bridge Street", "flats_old"), ("Orchard Way", "semi"),
             ("Kingsway", "semi"), ("Riverside Court", "flats"), ("Brook Lane", "detached"), ("Eastfield Road", "semi")],
    "TV02": [("The Green", "detached"), ("Church Lane", "semi"), ("Back Lane", "terrace"), ("Wennaby Road", "semi"),
             ("Glebe Close", "detached"), ("School Lane", "terrace"), ("Hall Farm Close", "detached")],
    "TV03": [("Beech Avenue", "semi"), ("Elm Grove", "semi"), ("Oak Drive", "detached"), ("Ash Close", "semi"),
             ("Willow Road", "semi"), ("Cedar Court", "flats"), ("Larch Way", "detached"), ("Rowan Crescent", "semi"),
             ("Hawthorn Road", "terrace"), ("Sycamore Close", "semi")],
    "TV04": [("Quay Street", "terrace"), ("Fore Street", "terrace"), ("Net Loft Lane", "terrace"),
             ("Harbour Hill", "terrace"), ("Coastguard Cottages", "terrace"), ("Cliff Road", "detached"),
             ("Boatyard Lane", "flats_old"), ("Chapel Street", "terrace")],
    "SW01": [("Dock Street", "terrace"), ("Ropewalk", "terrace"), ("Custom House Lane", "flats_old"),
             ("Victoria Terrace", "terrace"), ("Albert Street", "terrace"), ("Jubilee Street", "terrace"),
             ("Coronation Road", "terrace"), ("Union Street", "terrace"), ("North Quay", "flats_old"),
             ("Gladstone Street", "terrace"), ("Alma Road", "terrace"), ("Seaview Road", "semi"),
             ("Mission Lane", "terrace"), ("Cable Street", "terrace")],
    "SW02": [("Moor Lane", "detached"), ("Top Road", "terrace"), ("Chapel Row", "terrace"), ("Quarry Lane", "semi"),
             ("Fell View", "semi"), ("Smithy Lane", "terrace")],
    "SW03": [("Esplanade", "flats_old"), ("Marine Parade", "flats_old"), ("Promenade", "terrace"),
             ("Shore Road", "semi"), ("Ellingsea Marina", "flats_new"), ("Dune Court", "flats_new"),
             ("Sandpiper Way", "flats_new"), ("Links Road", "detached"), ("Pier Approach", "flats_new"),
             ("Beach Road", "semi"), ("Clifftop Drive", "detached")],
    "SW04": [("High Street", "terrace"), ("The Square", "terrace"), ("Mill Hill", "detached"),
             ("Church Walk", "terrace"), ("Pound Lane", "detached"), ("Coombe Road", "semi"),
             ("Harbour Row", "terrace"), ("Old Forge Lane", "detached"), ("Kittlesea Farm Cottages", "terrace")],
}
BLOCK_NAMES = {"flats": ["House", "Court", "Lodge"], "flats_old": ["Chambers", "House", "Buildings"],
               "flats_new": ["Point", "Reach", "Quay", "Heights"]}

# council tax occupation states (internal)
OCC, SECOND, UNF, FUR, EXEMPT, NDR = "OCC", "SECOND", "UNF", "FUR", "EXEMPT", "NDR"


def day_index(d):
    return (d - EXTRACT_START).days


class Home:
    pass


def _stays(rng, n, start_lo, start_hi, len_lo, len_hi, arr):
    for _ in range(n):
        s = int(rng.integers(start_lo, max(start_lo + 1, start_hi)))
        ln = int(rng.integers(len_lo, len_hi + 1))
        arr[s:min(NDAYS, s + ln)] = True


def presence(rng, typ):
    """who is in the home on each meter day of the extract (True: somebody lived in, stayed at or used it)."""
    p = np.zeros(NDAYS, dtype=bool)
    info = {}
    if typ == MAIN:
        p[:] = True
        k = rng.choice(4, p=[0.18, 0.37, 0.30, 0.15])
        for _ in range(k):
            s = int(rng.integers(0, NDAYS - 3))
            p[s:s + int(rng.integers(3, 15))] = False
        if rng.random() < 0.05:
            s = int(rng.integers(0, NDAYS - 30))
            p[s:s + int(rng.integers(21, 71))] = False
    elif typ == WEEKENDER:
        pw = rng.uniform(0.50, 0.85)
        for wk in range(NDAYS // 7):
            if rng.random() < pw:
                fri = wk * 7 + 4
                p[fri:min(NDAYS, fri + int(rng.integers(2, 4)))] = True
        _stays(rng, int(rng.integers(1, 3)), 0, NDAYS - 14, 5, 12, p)
    elif typ == SEASONAL:
        _stays(rng, int(rng.integers(1, 4)), day_index(date(2026, 7, 11)), day_index(date(2026, 8, 24)), 5, 14, p)
        if rng.random() < 0.6:
            _stays(rng, 1, day_index(date(2026, 3, 28)), day_index(date(2026, 4, 12)), 4, 7, p)
        if rng.random() < 0.5:
            _stays(rng, 1, day_index(date(2025, 12, 20)), day_index(date(2025, 12, 28)), 4, 8, p)
        if rng.random() < 0.5:
            _stays(rng, 1, 0, day_index(date(2025, 9, 20)), 4, 10, p)
        _stays(rng, int(rng.integers(0, 4)), 0, NDAYS - 4, 2, 3, p)
    elif typ == LET:
        hi, sh, lo = rng.uniform(0.70, 0.95), rng.uniform(0.25, 0.50), rng.uniform(0.03, 0.15)
        for wk in range(NDAYS // 7):
            d = DAYS[wk * 7]
            m = d.month
            pr = hi if m in (6, 7, 8) or (m == 5 and d.day > 20) or (m == 9 and d.day < 15) else (
                sh if m in (4, 5, 9, 10) else lo)
            if rng.random() < pr:
                start = wk * 7 + int(rng.choice([0, 4, 5]))
                p[start:min(NDAYS, start + int(rng.choice([3, 4, 7, 7, 7])))] = True
    elif typ == EMPTY:
        k = int(rng.choice(4, p=[0.45, 0.30, 0.17, 0.08]))
        for _ in range(k):
            s = int(rng.integers(0, NDAYS - 2))
            p[s:s + int(rng.integers(1, 3))] = True
    elif typ == PARTYEAR:
        run = int(rng.integers(5 * 7, 47 * 7))
        if rng.random() < 0.5:     # moved in part-way: empty before
            s = int(rng.integers(W0, W1 - run + 2))
            p[s:] = True
            info = {"kind": "in", "day": s}
        else:                      # moved out part-way: occupied before
            e = int(rng.integers(W0 + run, W1 + 1))
            lo, hi = day_index(SIX_MONTHS_BEFORE) - 5, day_index(SIX_MONTHS_BEFORE) + 5
            if lo <= e <= hi:          # nobody moves out within five days of the six-month line
                e = hi + 1 + (e - lo)
            p[:e] = True
            info = {"kind": "out", "day": e}
    return p, info


def daily_use(rng, persons, p):
    """litres used on each day somebody is in: events vary from day to day, never under USE_MIN."""
    u = np.zeros(NDAYS)
    n = int(p.sum())
    if n == 0:
        return u
    base = persons * rng.uniform(70, 125, n)
    shower = rng.binomial(persons, 0.75, n) * rng.uniform(35, 65, n)
    laundry = (rng.random(n) < 0.30) * rng.uniform(45, 85, n)
    dish = (rng.random(n) < 0.35) * rng.uniform(10, 15, n)
    x = np.maximum(base + shower + laundry + dish, USE_MIN + rng.uniform(0, 25, n))
    u[p] = x
    return u


def week_of(i):
    """window week (0..51) of extract day i, or None outside the window."""
    if i < W0 or i > W1:
        return None
    return (i - W0) // 7


def window_weeks_true(h):
    """the pilot's truth for one home: which of the 52 weeks somebody used it (any day of the week)."""
    return h.present[W0:W1 + 1].reshape(NWEEKS, 7).any(axis=1)


def _make_homes():
    homes = []
    for k, (code, name, dist, n, mix, old, neglect, leak_n, pc, ub) in enumerate(AREAS):
        rng = np.random.default_rng([SEED, 1, k])            # each area draws from its own stream
        types = rng.choice(6, size=n, p=np.array(mix) / np.sum(mix))
        for t in types:
            h = Home()
            h.i = len(homes)
            h.area = code
            h.typ = int(t)
            h.persons = int(rng.choice([1, 2, 3, 4, 5], p=[0.30, 0.36, 0.15, 0.13, 0.06]))
            h.old = bool(rng.random() < old)
            h.present, h.pinfo = presence(rng, h.typ)
            h.use_weeks = int(window_weeks_true(h).sum())
            h.empty_weeks = NWEEKS - h.use_weeks
            emptyish = h.typ in (EMPTY, SEASONAL, PARTYEAR) and h.empty_weeks >= 20
            h.neglect = bool(emptyish and rng.random() < neglect)
            h.leak = 0.0
            if h.neglect and h.old and rng.random() < leak_n:
                h.leak = float(np.exp(rng.normal(np.log(290), 0.45)))
            elif h.neglect and rng.random() < leak_n * 0.35:
                h.leak = float(np.exp(rng.normal(np.log(240), 0.45)))
            elif (not emptyish) and rng.random() < (0.025 if h.old else 0.008):
                h.leak = float(np.exp(rng.normal(np.log(180), 0.5)))
            elif emptyish and (not h.neglect) and rng.random() < 0.02:
                h.leak = float(np.exp(rng.normal(np.log(160), 0.4)))     # a supply pipe before the stopcock
            h.leak = float(min(max(h.leak, 0.0), 950.0))
            if 0 < h.leak < 110:
                h.leak = 110.0 + float(rng.uniform(0, 30))
            h.drip = 0.0
            if h.leak == 0 and rng.random() < (0.16 if h.old else 0.04):
                h.drip = float(rng.uniform(2, 24))
            h.use = daily_use(rng, h.persons, h.present)
            homes.append(h)
    return homes


def _series(homes):
    """the registered daily litres, with every whole week somebody spends in a home varying by WEEK_RANGE_MIN."""
    for h in homes:
        rng = np.random.default_rng([SEED, 2, h.i])
        steady = h.leak + h.drip
        # a running cistern or a weeping pipe wobbles with the mains pressure; a drip wanders more in proportion
        jitter = (rng.uniform(-1.0, 1.0, NDAYS) * ((2.0 + LEAK_JITTER * h.leak) if h.leak > 0 else 0.0)
                  + rng.uniform(-0.25, 0.25, NDAYS) * h.drip)
        u = h.use.copy()
        for w0 in range(0, NDAYS - 6, 7):
            seg = h.present[w0:w0 + 7]
            if seg.all():
                vals = u[w0:w0 + 7]
                if vals.max() - vals.min() < WEEK_RANGE_MIN:
                    j = int(np.argmax(vals))                 # the week's busiest day gets the wash or the bath
                    u[w0 + j] = vals.min() + WEEK_RANGE_MIN + float(rng.uniform(5, 40))
        h.use = u
        h.steady_day = steady + jitter
        h.total = np.rint(u + h.steady_day).astype(np.int64)


def build():
    homes = _make_homes()
    _series(homes)
    return homes


if __name__ == "__main__":
    hs = build()
    from collections import Counter
    c = Counter((h.area, h.empty_weeks >= 26) for h in hs)
    for a in AREA_CODES:
        print(a, AREA_NAME[a], c[(a, True)])
