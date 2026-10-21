"""The Tarrow Sound world before any file is written: fourteen Gulf Coast counties' insurable buildings (old slab
houses on the river bottoms and the bay front, newer houses built to the flood maps, condominium blocks), the
NFIP coverage each building carried from 2001 to 2026, the floods of those years and the claims they brought, the
authority's elevation and acquisition projects after the 2005, 2008, 2016, 2020 and 2024 floods, and the 2026 season.

Elevations are kept in feet on NAVD 1988 here; the files write records made before 2012 on NGVD 1929."""
import datetime as dt

import numpy as np

SEED = 4790
STATE = "58"
AS_OF = dt.date(2026, 9, 30)          # the guidelines' in-force date
PULL = dt.date(2026, 10, 2)           # FEMA's data-sharing extract
WIN0, WIN1 = dt.date(2001, 1, 1), dt.date(2025, 12, 31)
DATUM_CUT = dt.date(2012, 1, 1)       # records made before this carry NGVD 1929 elevations
EXIT = dt.date(2026, 7, 1)            # Gulfline Mutual leaves the NFIP; its book moves to NFIP Direct
YEAR_DAYS = 365.25

# county: FIPS, name, kind, NAVD88 = NGVD29 + offset, NFIP community numbers, pre-FIRM stock by reach A B C,
# post-FIRM stock by reach, zone X stock, condominium blocks, base flood elevation range (ft NAVD88)
COUNTIES = [
    ("58003", "Hensby", "coast", -0.8, ("580112", "580113"), (700, 420, 160), (90, 330, 460), 900, 6, (8.0, 12.0)),
    ("58007", "Dunholme", "river", -0.9, ("580204", "580205", "580211"), (2300, 1050, 380), (40, 330, 480), 1100, 0, (31.0, 58.0)),
    ("58011", "Eastmarsh", "coast", -0.9, ("580301", "580308"), (820, 480, 180), (80, 300, 420), 800, 8, (8.5, 12.5)),
    ("58015", "Gorran", "river", -1.0, ("580412", "580415"), (980, 520, 210), (40, 260, 380), 700, 0, (44.0, 71.0)),
    ("58019", "Menhaden Point", "coast", -0.8, ("580507", "580509"), (980, 500, 190), (90, 420, 560), 950, 14, (9.0, 13.5)),
    ("58023", "Ivesby", "river", -1.0, ("580602",), (900, 470, 200), (40, 240, 360), 650, 0, (52.0, 80.0)),
    ("58027", "Kettlemoor", "river", -1.0, ("580703", "580706"), (1900, 900, 330), (40, 280, 420), 1000, 0, (28.0, 52.0)),
    ("58031", "Amberjack Bay", "coast", -0.8, ("580810", "580811"), (1350, 640, 230), (100, 520, 720), 1000, 12, (8.5, 13.0)),
    ("58035", "Tesmond", "river", -1.1, ("580901",), (720, 410, 180), (40, 210, 300), 600, 0, (60.0, 88.0)),
    ("58039", "Thornock", "river", -1.1, ("581004", "581006"), (520, 300, 140), (30, 230, 360), 700, 0, (71.0, 96.0)),
    ("58043", "Ravensholt", "river", -1.0, ("581102", "581107"), (640, 360, 150), (35, 240, 350), 650, 0, (40.0, 66.0)),
    ("58047", "Saltreach", "coast", -0.8, ("581203", "581204"), (1700, 780, 260), (120, 640, 900), 1100, 18, (9.5, 14.5)),
    ("58051", "Lisgrove", "river", -1.0, ("581301",), (560, 330, 150), (30, 220, 340), 600, 0, (66.0, 90.0)),
    ("58055", "Wickmere", "river", -1.1, ("581402", "581405"), (500, 300, 130), (30, 210, 330), 650, 0, (74.0, 99.0)),
]
FIPS = [c[0] for c in COUNTIES]
CIDX = {f: i for i, f in enumerate(FIPS)}
NAME = {c[0]: c[1] for c in COUNTIES}
KIND = {c[0]: c[2] for c in COUNTIES}
OFFSET = {c[0]: c[3] for c in COUNTIES}
COMMUNITIES = {c[0]: c[4] for c in COUNTIES}
BY_NAME = {c[1]: c[0] for c in COUNTIES}
REACHES = ("A", "B", "C")
F = BY_NAME

# The floods of the record: each county's water against the base flood elevation (feet) in its three reaches; a
# flood's claims fall on the days of its first few dates.
MAJOR = [
    ("2002-09-26", 2, {F["Gorran"]: (-0.9, -1.8, -2.6), F["Ivesby"]: (-1.0, -1.9, -2.8), F["Tesmond"]: (-0.8, -1.7, -2.6),
                       F["Dunholme"]: (-1.2, -2.2, -3.0), F["Kettlemoor"]: (-1.3, -2.3, -3.1),
                       F["Ravensholt"]: (-1.5, -2.4, -3.2), F["Lisgrove"]: (-1.7, -2.6, -3.4), F["Thornock"]: (-2.0, -2.9, -3.7),
                       F["Wickmere"]: (-1.9, -2.8, -3.6)}),
    ("2005-08-29", 1, {F["Saltreach"]: (-0.6, -1.5, -2.4), F["Amberjack Bay"]: (-1.1, -2.0, -3.0),
                       F["Menhaden Point"]: (-0.4, -1.3, -2.2), F["Eastmarsh"]: (-0.9, -1.8, -2.6),
                       F["Hensby"]: (-1.4, -2.3, -3.2)}),
    ("2008-09-12", 3, {F["Gorran"]: (0.4, -0.6, -1.6), F["Ivesby"]: (0.2, -0.8, -1.8), F["Tesmond"]: (0.0, -1.0, -2.0),
                       F["Dunholme"]: (-0.3, -1.3, -2.3), F["Kettlemoor"]: (-0.5, -1.5, -2.4),
                       F["Ravensholt"]: (-1.0, -2.0, -2.8), F["Lisgrove"]: (-1.4, -2.3, -3.1), F["Thornock"]: (-2.2, -3.0, -3.8),
                       F["Wickmere"]: (-1.7, -2.6, -3.4)}),
    ("2012-08-29", 2, {F["Saltreach"]: (-1.8, -2.6, -3.4), F["Amberjack Bay"]: (-1.6, -2.5, -3.3),
                       F["Menhaden Point"]: (-1.2, -2.1, -2.9), F["Eastmarsh"]: (-1.0, -1.9, -2.7),
                       F["Hensby"]: (-1.7, -2.6, -3.4), F["Dunholme"]: (-2.0, -2.9, -3.6),
                       F["Kettlemoor"]: (-2.1, -3.0, -3.7)}),
    ("2016-08-12", 3, {F["Dunholme"]: (3.2, -0.4, -1.4), F["Kettlemoor"]: (2.4, -1.0, -1.8), F["Gorran"]: (1.2, 0.2, -0.8),
                       F["Ivesby"]: (0.6, -0.4, -1.4), F["Ravensholt"]: (-0.8, -1.8, -2.6), F["Tesmond"]: (-0.4, -1.4, -2.4),
                       F["Lisgrove"]: (-1.6, -2.5, -3.3), F["Wickmere"]: (-1.8, -2.7, -3.5), F["Thornock"]: (-2.3, -3.1, -3.9)}),
    ("2019-07-12", 2, {F["Dunholme"]: (-1.2, -2.1, -2.9), F["Kettlemoor"]: (-1.3, -2.2, -3.0), F["Gorran"]: (-1.1, -2.0, -2.8),
                       F["Ivesby"]: (-1.2, -2.1, -2.9), F["Tesmond"]: (-1.4, -2.3, -3.1), F["Ravensholt"]: (-1.6, -2.5, -3.3),
                       F["Lisgrove"]: (-1.7, -2.6, -3.4), F["Thornock"]: (-2.1, -3.0, -3.8), F["Wickmere"]: (-2.0, -2.9, -3.7)}),
    ("2020-10-09", 2, {F["Saltreach"]: (-0.6, -1.5, -2.4), F["Amberjack Bay"]: (-0.8, -1.7, -2.6),
                       F["Menhaden Point"]: (0.3, -0.6, -1.5), F["Eastmarsh"]: (-0.2, -1.1, -2.0),
                       F["Hensby"]: (-0.5, -1.4, -2.3)}),
    ("2024-09-26", 2, {F["Saltreach"]: (-1.5, -2.4, -3.2), F["Amberjack Bay"]: (-1.4, -2.3, -3.1),
                       F["Menhaden Point"]: (-0.9, -1.8, -2.6), F["Eastmarsh"]: (-0.8, -1.7, -2.5), F["Hensby"]: (-1.0, -1.9, -2.7),
                       F["Dunholme"]: (-0.8, -1.7, -2.5), F["Kettlemoor"]: (-0.9, -1.8, -2.6), F["Gorran"]: (-0.7, -1.6, -2.4),
                       F["Ivesby"]: (-0.9, -1.8, -2.6), F["Tesmond"]: (-1.0, -1.9, -2.7), F["Ravensholt"]: (-1.2, -2.1, -2.9),
                       F["Lisgrove"]: (-1.4, -2.3, -3.1), F["Thornock"]: (-1.9, -2.8, -3.6), F["Wickmere"]: (-1.6, -2.5, -3.3)}),
    ("2026-06-04", 3, {f: (-1.3 - 0.1 * (i % 4), -2.2 - 0.1 * (i % 4), -3.0 - 0.1 * (i % 4)) for i, f in enumerate(FIPS)}),
    ("2026-09-17", 2, {F["Saltreach"]: (-0.9, -1.8, -2.6), F["Amberjack Bay"]: (-1.0, -1.9, -2.7),
                       F["Menhaden Point"]: (-0.7, -1.6, -2.4), F["Eastmarsh"]: (-0.6, -1.5, -2.3),
                       F["Hensby"]: (-0.8, -1.7, -2.5), F["Dunholme"]: (-1.6, -2.5, -3.3), F["Kettlemoor"]: (-1.6, -2.5, -3.3),
                       F["Gorran"]: (-1.7, -2.6, -3.4), F["Ivesby"]: (-1.8, -2.7, -3.5), F["Tesmond"]: (-1.8, -2.7, -3.5),
                       F["Ravensholt"]: (-1.9, -2.8, -3.6), F["Lisgrove"]: (-2.0, -2.9, -3.7), F["Thornock"]: (-2.2, -3.1, -3.9),
                       F["Wickmere"]: (-2.1, -3.0, -3.8)}),
]
# the moderate floods' water stands lower against the map than the four the programs followed
SHIFT = {"2002-09-26": -1.8, "2012-08-29": -1.6, "2019-07-12": -1.9, "2024-09-26": -1.7, "2026-06-04": -2.3,
         "2026-09-17": -1.3}
EVENT_NAMES = {"2002-09-26": "Tropical Storm Isa", "2005-08-29": "Hurricane Delphine", "2008-09-12": "Tarrow River flood",
               "2012-08-29": "Hurricane Ottilie", "2016-08-12": "August rain flood", "2019-07-12": "July rain flood",
               "2020-10-09": "Hurricane Marlo", "2024-09-26": "Hurricane Saskia", "2026-06-04": "June rain flood",
               "2026-09-17": "Hurricane Teodor"}
TRIGGERS = {"2005-08-29": "2005", "2008-09-12": "2008", "2016-08-12": "2016", "2020-10-09": "2020", "2024-09-26": "2024"}
DISASTER = {"2005": "DR-1608", "2008": "DR-1792", "2016": "DR-4277", "2020": "DR-4559", "2024": "DR-4821"}

# the authority's projects after each flood: county -> (elevations, acquisitions, freeboard above the BFE, the depth
# the flood had to reach to qualify, first completion in years after the flood, spread of completions in years)
PROGRAMS = {
    "2005": {F["Saltreach"]: (720, 30, 2.0, 1.2, 1.4, 4.0), F["Amberjack Bay"]: (470, 25, 2.0, 1.2, 1.4, 4.0),
             F["Menhaden Point"]: (140, 45, 2.0, 1.2, 1.5, 4.0), F["Eastmarsh"]: (70, 15, 2.0, 1.2, 1.5, 4.0)},
    "2008": {F["Gorran"]: (210, 40, 1.0, 1.5, 1.6, 3.5), F["Ivesby"]: (160, 55, 1.0, 1.5, 1.6, 3.5),
             F["Tesmond"]: (110, 120, 1.0, 1.5, 1.6, 3.5)},
    "2016": {F["Dunholme"]: (660, 260, 1.0, 2.5, 1.5, 4.5), F["Kettlemoor"]: (500, 200, 1.0, 2.5, 1.5, 4.5),
             F["Gorran"]: (60, 20, 1.0, 2.0, 1.8, 3.5)},
    "2020": {F["Menhaden Point"]: (120, 30, 2.0, 1.2, 1.8, 5.5), F["Eastmarsh"]: (90, 20, 2.0, 1.2, 1.8, 5.5),
             F["Hensby"]: (40, 10, 2.0, 1.2, 2.2, 5.5)},
    "2024": {f: (int(18 + 9 * (i % 5)), int(4 + 3 * (i % 3)), 2.0 if KIND[f] == "coast" else 1.0, 1.2, 1.4, 3.0)
             for i, f in enumerate(FIPS)},
}

LOCAL_P = {"pre": 0.0042, "post": 0.00075, "condo": 0.0004, "x": 0.00035}
# how often a county's drainage fails in a local flood, against the region (soils, storm sewers, tide gates)
LOCAL_MULT = {F["Saltreach"]: 1.35 * 1.03, F["Amberjack Bay"]: 1.65 * 1.03, F["Wickmere"]: 2.25, F["Thornock"]: 2.55,
              F["Lisgrove"]: 3.4, F["Ravensholt"]: 3.75 * 0.97, F["Hensby"]: 2.97, F["Tesmond"]: 3.3, F["Eastmarsh"]: 3.4,
              F["Ivesby"]: 3.4, F["Menhaden Point"]: 3.2, F["Gorran"]: 2.6, F["Kettlemoor"]: 0.35 * 0.97, F["Dunholme"]: 0.35}
# how readily owners of the newer houses let their policies lapse, against the region
LAPSE = {F["Eastmarsh"]: 0.97, F["Menhaden Point"]: 0.97, F["Thornock"]: 0.97, F["Lisgrove"]: 0.97, F["Wickmere"]: 1.06}

CUTOVER = dt.date(2026, 1, 12)       # the authority's new grants system; the projects then open were migrated into it
# pre-FIRM garden condominiums on low ground, by county
OLD_CONDO = {F["Hensby"]: 9, F["Dunholme"]: 7, F["Eastmarsh"]: 10, F["Gorran"]: 5, F["Menhaden Point"]: 12,
             F["Ivesby"]: 5, F["Kettlemoor"]: 6, F["Amberjack Bay"]: 13, F["Tesmond"]: 4, F["Thornock"]: 4,
             F["Ravensholt"]: 4, F["Saltreach"]: 15, F["Lisgrove"]: 4, F["Wickmere"]: 4}
# write-your-own companies and NFIP Direct: Gulfline Mutual, Tarrow Southern, Bayward, Shorebrook, NFIP Direct
SERVICERS = ["GLFM", "TRSN", "BYWT", "SOUC", "NFDS"]
SERVICER_P = [0.27, 0.24, 0.19, 0.16, 0.14]
PREFIX = {"GLFM": "4418", "TRSN": "5306", "BYWT": "6127", "SOUC": "7452", "NFDS": "0099"}
REWRITE_P = 0.008                    # a policy moved to another company at a renewal

def d(s):
    return dt.date.fromisoformat(s)


def days(a, b):
    return (b - a).days


def rand_date(rng, a, b):
    return a + dt.timedelta(days=int(rng.integers(0, max(1, days(a, b)))))


def stream(*keys):
    """One random stream per component and unit, so a change in one county or flood re-rolls nothing else."""
    return np.random.default_rng([SEED] + [int(k) for k in keys])


def anniversary(d0, years):
    return dt.date(d0.year + years, d0.month, min(d0.day, 28))


# ---------------------------------------------------------------------------------------------- buildings
def make_buildings():
    out = []
    for ci, (fips, name, kind, off, comms, pre, post, nx, ncondo, bfe_rng) in enumerate(COUNTIES):
        rng = stream(1, ci)
        lo, hi = bfe_rng
        mine = []
        seq = [0]

        def new(reach, stock):
            seq[0] += 1
            b = dict(pid=None, fips=fips, reach=reach, stock=stock, community=comms[int(rng.integers(0, len(comms)))])
            rng.integers(0, 7)
            mine.append(b)
            return b

        for ri, r in enumerate(REACHES):
            for _ in range(pre[ri]):
                b = new(r, "pre")
                b["bfe"] = round(float(rng.uniform(lo, hi)) - 0.9 * ri, 1)
                dd = (1.0 + rng.gamma(2.5, 0.95)) if kind == "coast" else (0.5 + rng.gamma(2.2, 0.9))
                b["lfe0"] = round(b["bfe"] - min(float(dd), 6.5), 1)
                b["built"] = int(rng.integers(1935, 1980))
                b["zone"] = "VE" if (kind == "coast" and ri == 0 and rng.random() < 0.45) else "AE"
            for _ in range(post[ri]):
                b = new(r, "post")
                b["bfe"] = round(float(rng.uniform(lo, hi)) - 0.9 * ri, 1)
                b["lfe0"] = round(b["bfe"] + min(float(0.1 + rng.gamma(1.3, 0.55)), 3.5), 1)
                b["built"] = int(rng.choice(np.arange(1984, 2025), p=_built_p()))
                b["zone"] = "VE" if (kind == "coast" and ri == 0 and rng.random() < 0.5) else "AE"
        for _ in range(nx):
            r = REACHES[int(rng.choice(3, p=[0.15, 0.35, 0.5]))]
            b = new(r, "x")
            b["bfe"] = None
            ground = float(rng.uniform(lo, hi)) + float(rng.uniform(1.0, 6.0))
            b["lfe0"] = round(ground + float(rng.uniform(0.5, 2.0)), 1)
            b["hidden1pct"] = round(b["lfe0"] - float(1.6 + rng.gamma(2.0, 1.1)), 1)
            b["built"] = int(rng.integers(1950, 2024))
            b["zone"] = "X"
        for _ in range(ncondo):
            r = REACHES[int(rng.choice(3, p=[0.3, 0.4, 0.3]))]
            b = new(r, "condo")
            b["bfe"] = round(float(rng.uniform(lo, hi)), 1)
            b["lfe0"] = round(b["bfe"] + float(rng.uniform(0.3, 2.8)), 1)
            b["built"] = int(rng.integers(1986, 2019))
            b["zone"] = "VE" if (r == "A" and rng.random() < 0.6) else "AE"
            b["units"] = int(rng.choice([6, 8, 12, 16, 18, 24, 30, 36, 48]))
        for b in mine:
            b["post_firm"] = b["stock"] in ("post", "condo") or (b["stock"] == "x" and b["built"] >= 1981)
            b["occ"] = ("condo" if b["stock"] == "condo" else
                        ("sf" if rng.random() < 0.86 else ("2-4" if rng.random() < 0.6 else "nonres")))
            b["floors"] = (int(rng.integers(3, 9)) if b["stock"] == "condo" else
                           (1 if rng.random() < (0.72 if b["stock"] == "pre" else 0.45) else 2))
            b["value"] = int(round(float(rng.lognormal(np.log(235000 if b["stock"] == "pre" else 320000), 0.32)), -2))
            if b["stock"] == "condo":
                b["value"] = int(round(b["units"] * float(rng.uniform(150000, 260000)), -3))
            b["lfe"] = b["lfe0"]
            b["u"] = float(rng.normal(0.0, 0.45))
        out += mine
    # the garden condominiums of the 1970s on the low streets, each insured by its association
    for ci, (fips, name, kind, off, comms, pre, post, nx, ncondo, bfe_rng) in enumerate(COUNTIES):
        rng = stream(1, ci, 1)
        lo, hi = bfe_rng
        for _ in range(OLD_CONDO[fips]):
            r = "A" if rng.random() < 0.65 else "B"
            b = dict(pid=None, fips=fips, reach=r, stock="condo_old", community=comms[int(rng.integers(0, len(comms)))])
            b["bfe"] = round(float(rng.uniform(lo, hi)) - (0.9 if r == "B" else 0.0), 1)
            b["lfe0"] = round(b["bfe"] - float(rng.uniform(4.2, 6.2)), 1)
            b["built"] = int(rng.integers(1966, 1980))
            b["zone"] = "AE"
            b["units"] = int(rng.choice([8, 10, 12, 16, 20, 24]))
            b["floors"] = int(rng.choice([2, 2, 3]))
            b["post_firm"] = False
            b["occ"] = "condo"
            b["value"] = int(round(b["units"] * float(rng.uniform(90000, 150000)), -3))
            b["lfe"] = b["lfe0"]
            b["u"] = float(rng.normal(0.0, 0.35))
            out.append(b)
    # FEMA building identifiers: state, county, a six-digit serial and a check letter
    for ci, fips in enumerate(FIPS):
        mine = [b for b in out if b["fips"] == fips]
        serial = stream(1, ci, 2).choice(np.arange(100000, 1000000), size=len(mine), replace=False)
        for b, s in zip(mine, serial):
            core = "%s%s%06d" % (STATE, fips[2:], int(s))
            b["pid"] = core + "ABCDEFGHJKLMNPQRSTUVWXYZ"[sum(int(c) * (i + 1) for i, c in enumerate(core)) % 24]
    return out


_BP = None


def _built_p():
    global _BP
    if _BP is None:
        yrs = np.arange(1984, 2025)
        w = np.where(yrs < 2001, 0.6, 1.0) * np.where(yrs > 2017, 0.8, 1.0)
        _BP = w / w.sum()
    return _BP


# ---------------------------------------------------------------------------------------------- coverage
def insurance(rng, b, params=None):
    """Spells of NFIP coverage as [start, end, how]: end None while in force; how 'E' for a policy not renewed at
    its anniversary, 'C' for one cancelled mid-term."""
    kind = KIND[b["fips"]]
    if params is not None:
        p0, q, back = params
    elif b["stock"] == "condo":
        p0, q, back = 0.97, 0.015, 0.5
    elif b["stock"] == "post":
        p0, q, back = 0.80, 0.055 * LAPSE.get(b["fips"], 1.0), 0.04
    elif b["stock"] == "pre":
        p0, q, back = (0.62 if kind == "coast" else 0.57), 0.065, 0.035
    else:
        p0, q, back = 0.22, 0.12, 0.02
    built = dt.date(max(b["built"], 1975), 1, 1) + dt.timedelta(days=int(rng.integers(0, 330)))
    spells = []
    if built < dt.date(2001, 1, 1) and rng.random() < p0:
        cur = rand_date(rng, max(built, dt.date(1979, 1, 1)), dt.date(2000, 12, 20))
    elif built >= dt.date(2001, 1, 1) and rng.random() < (0.83 if b["stock"] in ("post", "condo") else p0):
        cur = built + dt.timedelta(days=int(rng.integers(20, 120)))
    else:
        cur = None
    t = max(dt.date(2001, 1, 1), built) if cur is None else cur
    while t < PULL:
        if cur is not None:
            k = 1
            while True:
                nxt = anniversary(cur, k)
                if nxt >= PULL:
                    spells.append([cur, None, None])
                    return spells
                if rng.random() < q:
                    end, how = nxt, "E"
                    if rng.random() < 0.35:   # cancelled mid-term (sold, paid off, no longer required)
                        end, how = anniversary(cur, k - 1) + dt.timedelta(days=int(rng.integers(30, 330))), "C"
                    spells.append([cur, end, how])
                    t = end
                    cur = None
                    break
                k += 1
        else:
            t2 = t + dt.timedelta(days=int(rng.integers(200, 900)))
            if t2 >= PULL:
                return spells
            if rng.random() < back * 6:
                cur = t2
            t = t2
    return spells


def insured_on(spells, day):
    for s, e, _ in spells:
        if s <= day and (e is None or day < e):
            return True
    return False


def in_window_days(spells, a=WIN0, z=WIN1):
    tot = 0
    z1 = z + dt.timedelta(days=1)
    for s, e, _ in spells:
        lo, hi = max(s, a), min(e or PULL, z1)
        if hi > lo:
            tot += (hi - lo).days
    return tot


# ---------------------------------------------------------------------------------------------- floods
def all_events():
    ev = []
    for s, n, xs in MAJOR:
        k = SHIFT.get(s, 0.0)
        ev.append((d(s), n, {f: tuple(round(v + k, 2) for v in x) for f, x in xs.items()}, "major"))
    rng = stream(2)
    for y in range(2001, 2027):
        for f in FIPS:
            for _ in range(int(rng.choice([1, 2, 2, 3]))):
                day = rand_date(rng, dt.date(y, 1, 5), dt.date(y, 12, 20) if y < 2026 else dt.date(2026, 9, 10))
                ev.append((day, 1, {f: float(rng.uniform(0.7, 1.3))}, "local"))
    ev.sort(key=lambda e: (e[0], e[3], sorted(e[2])[0]))
    return ev


def depth_damage(depth_ft):
    return min(0.92, 0.11 + 0.125 * depth_ft)


def build():
    buildings = make_buildings()
    for k, b in enumerate(buildings):
        ci = CIDX[b["fips"]]
        if b["stock"] == "condo_old":
            b["spells"] = insurance(stream(3, ci, k), b, (0.95, 0.02, 0.5))
        else:
            b["spells"] = insurance(stream(3, ci, k), b)
        b["proj"] = None
        b["changes"] = []          # (date, new lfe) from completed elevations
        b["gone"] = None           # acquisition date
    original = {}
    old = {}
    for i, b in enumerate(buildings):
        (old if b["stock"] == "condo_old" else original).setdefault(b["fips"], []).append(i)
    events = all_events()
    claims = []
    pending = []
    props = []
    last_loss = {}
    for ei, (day, ndays, xs, kind) in enumerate(events):
        still = []
        for item in pending:
            if item[0] <= day:
                _complete(buildings, item)
            else:
                still.append(item)
        pending = still
        for f, xv in xs.items():
            for idx, rng in ((original[f], stream(4, ei, CIDX[f])), (old.get(f, []), stream(4, ei, CIDX[f], 1))):
                if kind == "local":
                    for i in idx:
                        b = buildings[i]
                        if b["gone"] is not None and b["gone"] <= day:
                            continue
                        stock = "pre" if b["stock"] == "condo_old" else b["stock"]
                        p = LOCAL_P[stock] * xv * LOCAL_MULT[f]
                        if stock == "pre":
                            p *= 0.45 + 0.28 * max(0.0, b["bfe"] - b["lfe"])
                        if rng.random() >= p or not insured_on(b["spells"], day):
                            continue
                        over = 0.06 + float(rng.gamma(1.6, 0.32))
                        if i in last_loss and (day - last_loss[i]).days <= 3:
                            continue       # the same water: one loss
                        last_loss[i] = day
                        claims.append(dict(bi=i, day=day, event=day.isoformat(), kind=kind,
                                           over=over, lfe=b["lfe"], bfe=b["bfe"]))
                    continue
                X = dict(zip(REACHES, xv))
                for i in idx:
                    b = buildings[i]
                    if b["gone"] is not None and b["gone"] <= day:
                        continue
                    level = (b["bfe"] if b["bfe"] is not None else b["hidden1pct"]) + X[b["reach"]] + b["u"] \
                        + float(rng.normal(0.0, 0.55))
                    over = level - b["lfe"]
                    lag = int(rng.integers(0, ndays))
                    cw = rng.random()
                    if over < -1.5 or (over < 1.0 / 12 and cw > 0.12) or not insured_on(b["spells"], day):
                        continue
                    dol = day + dt.timedelta(days=lag)
                    if i in last_loss and abs((dol - last_loss[i]).days) <= 3:
                        continue
                    last_loss[i] = dol
                    claims.append(dict(bi=i, day=dol, event=day.isoformat(), kind=kind,
                                       over=over, lfe=b["lfe"], bfe=b["bfe"]))
        trig = TRIGGERS.get(day.isoformat())
        if trig:
            new_items = _programs(buildings, claims, day, trig, props)
            pending += new_items
    for item in pending:
        if item[0] <= AS_OF:
            _complete(buildings, item)
    for b in buildings:
        b["ecs"] = _ecs(b)
    _nudge(buildings, claims)
    for c in claims:
        _finish_claim(stream(5, c["bi"], c["day"].toordinal()), buildings[c["bi"]], c)
    _units_and_tenants(buildings, claims)
    book = _policies(buildings)
    _claims_to_policies(buildings, claims, book)
    projects = _projects(buildings, props)
    return dict(buildings=buildings, claims=claims, events=events, props=props, projects=projects, book=book)


def _programs(buildings, claims, day, trig, props):
    out = []
    flooded = {}
    for c in claims:
        if c["event"] == day.isoformat() and c["over"] > 0:
            flooded.setdefault(buildings[c["bi"]]["fips"], []).append(c)
    for f, (n_el, n_aq, fb, dmin, first, spread) in sorted(PROGRAMS[trig].items()):
        rng = stream(6, int(trig), CIDX[f])
        wd = stream(6, int(trig), CIDX[f], 1)
        cand = [c for c in flooded.get(f, []) if buildings[c["bi"]]["stock"] == "pre" and buildings[c["bi"]]["proj"] is None
                and c["over"] >= dmin]
        order = [cand[j] for j in rng.permutation(len(cand))]
        deep = sorted(order[: int(len(order) * 0.9)], key=lambda c: -c["over"])
        aq = deep[:n_aq]
        aq_ids = {c["bi"] for c in aq}
        el = [c for c in order if c["bi"] not in aq_ids][:n_el]
        for kind, lst in (("elevation", el), ("acquisition", aq)):
            for c in lst:
                bi = c["bi"]
                b = buildings[bi]
                yrs = first + float(rng.uniform(0.0, spread))
                done = day + dt.timedelta(days=int(yrs * 365))
                new = round(b["bfe"] + fb + float(rng.choice([0.0, 0.1, 0.2, 0.3, 0.5])), 1) if kind == "elevation" else None
                approved = day + dt.timedelta(days=int(rng.integers(240, 520)))
                if trig == "2024":       # two rounds of approvals, the second after the new grants system
                    approved = day + dt.timedelta(days=int(wd.integers(200, 640)))
                done = max(done, approved + dt.timedelta(days=330))
                withdrawn = None
                if wd.random() < 0.07:      # the owner withdrew before construction
                    withdrawn = approved + dt.timedelta(days=int(wd.integers(60, 400)))
                    if withdrawn >= done - dt.timedelta(days=270) or withdrawn > AS_OF or \
                            (approved < CUTOVER <= withdrawn):
                        withdrawn = None
                b["proj"] = dict(trigger=trig, kind=kind, done=None if withdrawn else done, new_lfe=new, fb=fb,
                                 approved=approved, withdrawn=withdrawn)
                props.append(dict(bi=bi, trigger=trig, fips=f, kind=kind, approved=approved, done=done,
                                  withdrawn=withdrawn, new_lfe=new, flood_over=c["over"]))
                if withdrawn is None:
                    out.append((done, bi, kind, new))
    return out


def _complete(buildings, item):
    done, bi, kind, new = item
    b = buildings[bi]
    if kind == "elevation":
        b["lfe"] = new
        b["changes"].append((done, new))
    else:
        b["gone"] = done
        kept = []
        for s in b["spells"]:
            if s[0] >= done:
                continue
            if s[1] is None or s[1] > done:
                s[1], s[2] = done, "A"
            kept.append(s)
        b["spells"] = kept


# ---------------------------------------------------------------------------------------------- elevation certificates
def _ecs(b):
    """The elevation certificates the building's policies were rated on: (date, lfe, bfe) in NAVD 1988 feet, the
    first before the building's earliest cover, a re-survey for some, and one at each completed elevation."""
    rng = stream(11, CIDX[b["fips"]], int(b["pid"][5:11]))
    first = min([s[0] for s in b["spells"]] + [dt.date(2026, 6, 1)])
    if b["post_firm"]:
        d0 = dt.date(max(b["built"], 1984), 1, 1) + dt.timedelta(days=int(rng.integers(150, 360)))
        d0 = min(d0, first)
    else:
        d0 = min(first, dt.date(2000, 12, 1)) - dt.timedelta(days=int(rng.integers(20, 2400)))
    ecs = [(d0, b["lfe0"], b["bfe"])]
    if rng.random() < 0.38:   # re-surveyed (a refinance, a sale, the 2021 rating change)
        dr = rand_date(rng, dt.date(2012, 3, 1), dt.date(2024, 6, 30))
        if dr > d0 and not any(c[0] <= dr for c in b["changes"]):
            ecs.append((dr, b["lfe0"], b["bfe"]))
    for done, new in b["changes"]:
        ecs.append((done, new, b["bfe"]))
    ecs.sort()
    return ecs


def ec_on(b, day):
    cur = b["ecs"][0]
    for e in b["ecs"]:
        if e[0] <= day:
            cur = e
    return cur


def datum_of(ec_date):
    return "NGVD29" if ec_date < DATUM_CUT else "NAVD88"


def _nudge(buildings, claims):
    """Keep every replayed claim clear of the inch the payment turns on: no claim on a building raised since stands
    within two inches of the raised floor or at it."""
    for c in claims:
        b = buildings[c["bi"]]
        if not b["changes"] or c["day"] >= b["changes"][-1][0]:
            continue
        rep = 12 * (c["lfe"] + c["over"] - b["lfe"])
        if -2.5 < rep < 3.0:
            c["over"] += (3.6 - rep) / 12 if rep >= 0.25 else (-3.0 - rep) / 12
    for c in claims:
        dep = int(round(12 * c["over"]))
        if dep == 0 and c["over"] > 0:
            c["over"] = 0.0


# ---------------------------------------------------------------------------------------------- claims
def _finish_claim(rng, b, c):
    dep = int(round(12 * c["over"]))
    c["form"] = "B"
    c["unit"] = None
    c["depth_in"] = max(dep, 0)
    c["paid"] = dep >= 1
    ft = max(c["over"], 0.0)
    c["damage"] = int(round(b["value"] * depth_damage(ft) * float(rng.uniform(0.85, 1.15)))) if c["paid"] else 0
    c["cdamage"] = int(round(c["damage"] * float(rng.uniform(0.15, 0.45)))) if c["paid"] else 0
    lag = (1 + float(rng.exponential(5.0))) if c["kind"] == "major" else (1 + float(rng.exponential(4.0)))
    if rng.random() < 0.08:
        lag += float(rng.uniform(18, 55))
    c["reported"] = c["day"] + dt.timedelta(days=int(lag))
    dur = (25 + float(rng.gamma(2.0, 25.0))) if c["kind"] == "major" else (15 + float(rng.gamma(2.0, 14.0)))
    if not c["paid"]:
        dur = 8 + float(rng.gamma(2.0, 6.0))
    c["closed"] = c["reported"] + dt.timedelta(days=int(dur))
    c["adv_day"] = c["reported"] + dt.timedelta(days=int(rng.integers(3, 12)))
    c["adv_frac"] = float(rng.uniform(0.2, 0.4))
    c["icc"] = 0
    if c["paid"] and b["proj"] is not None and b["proj"]["done"] is not None and c["damage"] >= 0.5 * b["value"] \
            and c["day"] < b["proj"]["done"] and c["event"] in TRIGGERS:
        c["icc"] = 30000


def _units_and_tenants(buildings, claims):
    """Unit owners' policies in the condominiums and tenants' contents policies, with the claims a flood that
    entered the building brought them."""
    for k, b in enumerate(buildings):
        ci = CIDX[b["fips"]]
        b["unit_spells"] = {}
        b["tenant_spells"] = []
        if b["occ"] == "condo":
            rng = stream(7, ci, k)
            share = float(rng.uniform(0.35, 0.55))
            for u in range(b["units"]):
                if rng.random() < share:
                    unit = "%d%02d" % (1 + u // max(1, b["units"] // b["floors"]), 1 + u % max(1, b["units"] // b["floors"]))
                    b["unit_spells"][unit] = insurance(stream(8, ci, k, u), b, (0.75, 0.07, 0.15))
        elif b["occ"] in ("2-4", "nonres"):
            b["tenant_spells"] = insurance(stream(9, ci, k, 1), b, (0.28, 0.14, 0.03))
    extra = []
    for c in claims:
        if not c["paid"]:
            continue
        b = buildings[c["bi"]]
        rng = stream(10, c["bi"], c["day"].toordinal())
        if b["unit_spells"]:
            per_floor = max(1, b["units"] // b["floors"])
            for unit, sp in b["unit_spells"].items():
                if int(unit[0]) != 1 or not insured_on(sp, c["day"]):
                    continue
                uv = b["value"] / b["units"] * float(rng.uniform(0.25, 0.45))
                dmg = int(round(uv * depth_damage(c["over"]) * float(rng.uniform(0.85, 1.15))))
                u = dict(c)
                u.update(form="U", unit=unit, damage=dmg, cdamage=int(round(dmg * float(rng.uniform(0.4, 0.9)))), icc=0)
                u["reported"] = c["reported"] + dt.timedelta(days=int(rng.integers(0, 6)))
                u["closed"] = u["reported"] + dt.timedelta(days=int(20 + rng.gamma(2.0, 20.0)))
                u["adv_day"] = u["reported"] + dt.timedelta(days=int(rng.integers(3, 12)))
                extra.append(u)
            assert per_floor >= 1
        if b["tenant_spells"] and insured_on(b["tenant_spells"], c["day"]):
            t = dict(c)
            t.update(form="T", unit=None, damage=0, cdamage=int(round(float(rng.uniform(6000, 42000)) *
                                                                       min(1.0, 0.3 + 0.2 * c["over"]))), icc=0)
            t["reported"] = c["reported"] + dt.timedelta(days=int(rng.integers(0, 9)))
            t["closed"] = t["reported"] + dt.timedelta(days=int(15 + rng.gamma(2.0, 15.0)))
            t["adv_day"] = t["reported"]
            extra.append(t)
    claims += extra
    claims.sort(key=lambda c: (c["day"], c["bi"], c["form"], c["unit"] or ""))


# ---------------------------------------------------------------------------------------------- the policy book
def _segments(rng, spell, srv0):
    """One spell of cover cut into policies: a company change at a renewal rewrites the policy under a new number,
    and Gulfline Mutual's book moved to NFIP Direct on 1 July 2026."""
    start, end, how = spell
    stop = end if end is not None else PULL
    segs = []
    cur_s, cur = start, srv0
    k = 1
    while True:
        ann = anniversary(start, k)
        if ann >= stop:
            break
        if rng.random() < REWRITE_P:
            nxt = SERVICERS[int(rng.choice(5, p=SERVICER_P))]
            if nxt == cur or (nxt == "GLFM" and ann >= EXIT):
                nxt = "NFDS" if cur != "NFDS" else "TRSN"
            segs.append([cur_s, ann, cur, "R"])
            cur_s, cur = ann, nxt
        k += 1
    segs.append([cur_s, end, cur, how])
    out = []
    for s, e, srv, h in segs:
        if srv == "GLFM" and s < EXIT and (e is None or e > EXIT):
            out.append([s, EXIT, "GLFM", "R"])
            out.append([EXIT, e, "NFDS", h])
        elif srv == "GLFM" and s >= EXIT:
            out.append([s, e, "NFDS", h])
        else:
            out.append([s, e, srv, h])
    return out


def _policies(buildings):
    """Every policy: building policies (dwelling, general property, condominium association), unit owners' and
    tenants' policies, with the policy each rewrite replaced."""
    rng = stream(12)
    serials = {s: iter(rng.choice(np.arange(100000, 1000000), size=60000, replace=False)) for s in SERVICERS}
    book = []
    for k, b in enumerate(buildings):
        ci = CIDX[b["fips"]]
        r = stream(13, ci, k)
        lots = [("B", None, b["spells"])] + [("U", u, sp) for u, sp in b["unit_spells"].items()]
        if b["tenant_spells"]:
            lots.append(("T", None, b["tenant_spells"]))
        b["pols"] = {}
        for form, unit, spells in lots:
            mine = []
            for sp in spells:
                srv0 = SERVICERS[int(r.choice(5, p=SERVICER_P))]
                if srv0 == "GLFM" and sp[0] >= EXIT:
                    srv0 = "NFDS"
                prior = None
                for s, e, srv, h in _segments(r, sp, srv0):
                    num = PREFIX[srv] + "%06d" % int(next(serials[srv]))
                    pol = dict(number=num, prior=prior, bi=k, form=form, unit=unit, servicer=srv, start=s, end=e,
                               how=h, anchor=sp[0])
                    if h == "C":
                        pol["reason"] = "02" if r.random() < 0.55 else "01"
                    elif h == "A":
                        pol["reason"] = "08"
                    elif h == "R":
                        pol["reason"] = "22"
                    else:
                        pol["reason"] = None
                    prior = num if h == "R" else None
                    _rate(r, b, pol)
                    mine.append(pol)
                    book.append(pol)
            b["pols"][(form, unit)] = mine
    return book


def _rate(r, b, pol):
    """The last term's rating: coverage, deductible, premium and the elevation certificate it was rated on."""
    s, e = pol["start"], pol["end"]
    last = s
    k = 1
    while True:
        nxt = anniversary(pol["anchor"], k)
        if nxt <= s:
            k += 1
            continue
        if nxt >= (e or PULL) or nxt > PULL:
            break
        last = nxt
        k += 1
    pol["term_start"] = last
    nxt = last
    k = 1
    while nxt <= last:
        nxt = anniversary(pol["anchor"], k)
        k += 1
    pol["term_end"] = nxt
    ec = ec_on(b, min(PULL, (e or PULL) - dt.timedelta(days=1)))     # endorsed when a new certificate came in
    pol["ec"] = ec
    resid = b["occ"] != "nonres"
    if pol["form"] == "B":
        cap = 250000 * (b["units"] if b["occ"] == "condo" else 1) if resid else 500000
        pol["bcov"] = int(min(cap, round(b["value"] * float(r.uniform(0.7, 1.0)), -4)))
        pol["ccov"] = int(r.choice([0, 0, 20000, 40000, 60000, 100000])) if b["occ"] != "condo" else 0
    elif pol["form"] == "U":
        pol["bcov"] = int(r.choice([40000, 60000, 80000, 100000, 150000]))
        pol["ccov"] = int(r.choice([20000, 30000, 50000]))
    else:
        pol["bcov"] = 0
        pol["ccov"] = int(r.choice([10000, 20000, 30000, 50000, 80000]))
    pol["ded"] = int(r.choice([1000, 1250, 2000, 2000, 5000]))
    diff = ec[1] - (ec[2] if ec[2] is not None else ec[1] - 2.0)
    rate = 1.9 if diff >= 2 else (3.1 if diff >= 0 else (7.4 if diff >= -2 else 10.8))    # per $1,000 of coverage
    if b["zone"] == "VE":
        rate *= 2.1
    if b["zone"] == "X":
        rate = 1.2
    rate *= float(r.uniform(0.82, 1.22))           # the building's own rating factors under Risk Rating 2.0
    prem = pol["bcov"] / 1000 * rate + pol["ccov"] / 1000 * rate * 0.7
    fees = 50 + (250 if b["occ"] == "nonres" else 25) + (70 if pol["bcov"] else 0)
    pol["premium"] = int(round(max(float(r.uniform(55.0, 140.0)), prem) * 1.18 + fees))


def _claims_to_policies(buildings, claims, book):
    """Each claim under the policy in force on its date of loss; Gulfline Mutual's open June claims re-entered by
    NFIP Direct under the policy that replaced theirs, and late reports opened there from the start."""
    rng = stream(14)
    nums = {s: iter(rng.choice(np.arange(10000, 1000000), size=200000, replace=False)) for s in SERVICERS}
    extra = []
    for c in claims:
        b = buildings[c["bi"]]
        pols = b["pols"][({"B": "B", "U": "U", "T": "T"}[c["form"]], c["unit"])]
        on = lambda day: next((p for p in pols if p["start"] <= day and (p["end"] is None or day < p["end"])), None)
        pol = on(c["day"])
        if pol is None:      # the cover ended during the flood's later days: the loss dates from its first
            c["day"] = d(c["event"])
            pol = on(c["day"])
        c["policy"] = pol
        c["ec"] = ec_on(b, c["day"])
        bpay = 0
        if c["form"] in ("B", "U") and c["paid"]:
            bpay = max(0, min(pol["bcov"], c["damage"]) - pol["ded"])
        cpay = max(0, min(pol["ccov"], c["cdamage"]) - (pol["ded"] if pol["ccov"] else 0)) if c["paid"] else 0
        c["bpay"], c["cpay"] = bpay, cpay
        c["number"] = None
        c["twin"] = None
        srv = pol["servicer"]
        nxt = next((p for p in pols if p["prior"] == pol["number"]), None)
        if srv == "GLFM" and c["day"] < EXIT and nxt is not None and nxt["start"] == EXIT:
            adv = c["kind"] == "major" and c["paid"] and c["adv_day"] < EXIT
            if c["closed"] < EXIT:
                pass
            elif adv:
                # GLFM's record closes at the transfer with its advance; NFIP Direct re-enters the rest
                n = dict(c)
                n["policy"] = nxt
                n["reported"] = EXIT + dt.timedelta(days=int(rng.integers(0, 30)))
                n["bpay"] = bpay           # NFIP Direct's record carries the claim's payments to date
                n["cpay"] = cpay
                n["twin"] = c
                c["bpay"] = int(round(bpay * c["adv_frac"]))
                c["cpay"] = 0
                c["closed_at_transfer"] = True
                c["closed"] = EXIT - dt.timedelta(days=1)
                extra.append(n)
            else:
                c["policy"] = nxt
                if c["reported"] < EXIT:
                    c["reported"] = EXIT + dt.timedelta(days=int(rng.integers(0, 30)))
        # payments as of the extract: an advance on a major flood's open claim, nothing on an open local one
    for c in claims + extra:
        c["status"] = "CLOSED" if c["closed"] <= PULL else "OPEN"
        if c["status"] == "OPEN":
            if c["twin"] is not None:
                c["bpay_asof"], c["cpay_asof"] = c["twin"]["bpay"], 0
            elif c["kind"] == "major" and c["adv_day"] <= PULL and c["bpay"] > 0:
                c["bpay_asof"], c["cpay_asof"] = int(round(c["bpay"] * c["adv_frac"])), 0
            else:
                c["bpay_asof"], c["cpay_asof"] = 0, 0
        else:
            c["bpay_asof"], c["cpay_asof"] = c["bpay"], c["cpay"]
        if c["status"] == "CLOSED" and c["bpay_asof"] == 0 and c["cpay_asof"] == 0:
            c["status"] = "CWOP"
    claims += extra
    claims.sort(key=lambda c: (c["day"], c["bi"], c["form"], c["unit"] or "", c["reported"]))
    for c in claims:
        srv = c["policy"]["servicer"]
        c["number"] = "%s%02d%06d" % (PREFIX[srv], c["reported"].year % 100, int(next(nums[srv])))


# ---------------------------------------------------------------------------------------------- the authority's register
JOINT = [("Thornock", "Wickmere"), ("Lisgrove", "Tesmond"), ("Ravensholt", "Ivesby"), ("Hensby", "Eastmarsh")]


def _projects(buildings, props):
    """Group the properties into grant projects: elevations by community, acquisitions by county, and in 2024 the
    small counties' acquisitions in joint projects."""
    rng = stream(15)
    lead = {}
    for a, z in JOINT:
        lead[F[z]] = F[a]
    groups = {}
    for p in props:
        b = buildings[p["bi"]]
        rnd = 2 if p["approved"] >= CUTOVER else 1
        if p["kind"] == "elevation":
            key = (p["trigger"], rnd, p["fips"], "elevation", b["community"])
        elif p["trigger"] == "2024" and p["fips"] in set(lead) | set(lead.values()):
            key = (p["trigger"], rnd, lead.get(p["fips"], p["fips"]), "acquisition", "joint")
        else:
            key = (p["trigger"], rnd, p["fips"], "acquisition", "")
        groups.setdefault(key, []).append(p)
    projects = []
    seqs = {}
    for key in sorted(groups):
        trig, rnd, fl, kind, comm = key
        lst = groups[key]
        chunks = [lst[i:i + 45] for i in range(0, len(lst), 45)]
        for ch in chunks:
            seqs[trig] = seqs.get(trig, 0) + int(rng.integers(1, 4))
            if kind == "elevation":
                prog, pct = ("HMGP", 75) if rng.random() < 0.8 else ("FMA", 90)
            else:
                prog, pct = ("FMA", 100) if rng.random() < 0.5 else ("HMGP", 75)
            if trig == "2024" and comm == "joint":
                prog, pct = "BRIC", 90
            approved = min(p["approved"] for p in ch)
            number = "%s-%s-%04d" % (prog, DISASTER[trig][3:] if prog == "HMGP" else ("20%02d" % ((int(trig) + 1) % 100)),
                                     seqs[trig])
            for p in ch:
                b = buildings[p["bi"]]
                p["project"] = number
                p["approved"] = approved
                if p["kind"] == "elevation":
                    rise = (p["new_lfe"] - b["lfe0"]) if p["new_lfe"] is not None else 4.0
                    p["cost"] = int(round(92000 + 17500 * rise + float(rng.normal(0, 9000)), -2))
                else:
                    p["cost"] = int(round(b["value"] * float(rng.uniform(1.0, 1.1)) + float(rng.uniform(12000, 22000)), -2))
                p["share"] = 0 if p["withdrawn"] is not None else int(round(p["cost"] * pct / 100.0))
            live = [p for p in ch if p["withdrawn"] is None]
            share = sum(p["share"] for p in live)
            migrated = approved < CUTOVER
            # the old system kept the federal share on the project and spread it evenly over its properties
            for j, p in enumerate(live):
                p["share_shown"] = p["share"]
                if migrated:
                    p["share_shown"] = share // len(live) + (share - share // len(live) * len(live) if j == 0 else 0)
            for p in ch:
                if p["withdrawn"] is not None:
                    p["share_shown"] = 0
            projects.append(dict(number=number, trigger=trig, program=prog, pct=pct, lead=fl, kind=kind,
                                 approved=approved, props=ch, migrated=migrated, share=share,
                                 cost=sum(p["cost"] for p in live)))
    return projects


def prop_status(p, day):
    """The property's status on a day: Withdrawn, Completed (final inspection passed), Under construction, Approved."""
    if p["withdrawn"] is not None and p["withdrawn"] <= day:
        return "Withdrawn", p["withdrawn"]
    if p["done"] <= day:
        return "Completed", p["done"]
    start = p["done"] - dt.timedelta(days=270)
    if start <= day:
        return "Under construction", start
    return "Approved", p["approved"]


if __name__ == "__main__":
    import time
    t0 = time.time()
    x = build()
    print("buildings", len(x["buildings"]), "claims", len(x["claims"]), "policies", len(x["book"]),
          "projects", len(x["projects"]), "%.1fs" % (time.time() - t0))
