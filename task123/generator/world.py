"""The fixed world of task123: dates, the region's twelve counties and three gas utilities, their read
calendars, the winter's heating degree days, and the seeded random streams every other module draws from.

Nothing here is shipped as a file. The heating degree days drive the simulated daily use and are not in the
pack: the only daily evidence a solver holds is Pine Harbor's AMI reads.
"""
import hashlib
from datetime import date, timedelta

import numpy as np

D = date
SIM_START = D(2025, 9, 1)          # first gas day simulated
SIM_END = D(2026, 5, 31)           # last gas day simulated
DAYS = [SIM_START + timedelta(i) for i in range((SIM_END - SIM_START).days + 1)]
NDAY = len(DAYS)
IDX = {d: i for i, d in enumerate(DAYS)}
JAN = np.array([d.year == 2026 and d.month == 1 for d in DAYS])

AMI_INSTALL_FROM, AMI_INSTALL_TO = D(2025, 10, 6), D(2025, 10, 24)
BILL_PULL = D(2026, 4, 15)         # billing extracts and MDMS reads pulled
KVG_ORDERS_PULL = D(2026, 2, 3)    # Kestrel Valley's January service-order extract
OTHER_PULL = D(2026, 4, 15)
THREAD_DATE = D(2026, 4, 20)       # the planning thread; the fiction's as-of date
GRANT = 18_640_000

UTILS = ("KVG", "NNG", "PHE")
UTIL_NAME = {"KVG": "Kestrel Valley Gas", "NNG": "Northbank Natural Gas", "PHE": "Pine Harbor Energy"}
RES_CLASS = {"KVG": "RS-1", "NNG": "R1", "PHE": "RES"}

# county: (utility, residential premises before tuning, housing-stock size factor, read centre, read spread,
#          Pine Harbor AMI share)
COUNTIES = {
    "Ashwell":    ("KVG", 3900, 1.14, 4, 3, 0.0),
    "Brennock":   ("KVG", 6100, 0.97, 11, 2, 0.0),
    "Carrow":     ("KVG", 2700, 0.88, 7, 2, 0.0),
    "Dellmoor":   ("KVG", 5000, 1.06, 17, 3, 0.0),
    "Evanshade":  ("KVG", 3400, 0.93, 20, 2, 0.0),
    "Farrish":    ("NNG", 3700, 1.17, 4, 2, 0.0),
    "Glenhollow": ("NNG", 2400, 0.90, 9, 2, 0.0),
    "Halvern":    ("NNG", 4300, 1.05, 15, 2, 0.0),
    "Keswin":     ("NNG", 3000, 0.95, 19, 2, 0.0),
    "Lorrance":   ("PHE", 5300, 0.99, 6, 4, 0.58),
    "Merrion":    ("PHE", 3300, 1.10, 12, 4, 0.44),
    "Tillery":    ("PHE", 4000, 0.91, 17, 4, 0.33),
}
COUNTY_ORDER = list(COUNTIES)
# The names the shipped files carry. Random streams are keyed on the internal names above; the pack, the goldens
# and the write-up use these, with the State's county codes in their alphabetical order.
DISPLAY = {"Ashwell": "Ashwell", "Brennock": "Brennock", "Carrow": "Sauvain", "Dellmoor": "Rennick",
           "Evanshade": "Ottercreek", "Farrish": "Farrish", "Glenhollow": "Wynnell", "Halvern": "Halvern",
           "Keswin": "Keswin", "Lorrance": "Pellow", "Merrion": "Merrion", "Tillery": "Tillery"}
INTERNAL = {v: k for k, v in DISPLAY.items()}
DISPLAY_ORDER = sorted(DISPLAY.values())
DCODE = {c: "N%02d" % (i + 1) for i, c in enumerate(DISPLAY_ORDER)}
# Kestrel Valley also serves the north-east corner of Tillery County, read on its late cycles.
TILLERY_KVG = 360
COUNTY_CODE = {c: "N%02d" % (i + 1) for i, c in enumerate(COUNTY_ORDER)}

TOWNS = {
    "Ashwell": ["Ashwell", "Corley", "Stannard"], "Brennock": ["Brennock", "Gilsey", "Marten Lake", "Pell"],
    "Carrow": ["Carrow", "Edgeworth"], "Dellmoor": ["Dellmoor", "Hask", "Rindge Mills"],
    "Evanshade": ["Evanshade", "Tolley"], "Farrish": ["Farrish", "Quarry Point", "Sedley"],
    "Glenhollow": ["Glenhollow", "Wick"], "Halvern": ["Halvern", "Orrin", "Bascom"],
    "Keswin": ["Keswin", "Lathe"], "Lorrance": ["Lorrance", "Pine Harbor", "Shale Bay"],
    "Merrion": ["Merrion", "Coldwater Inlet"], "Tillery": ["Tillery", "Ammon", "North Tillery"],
}

# Daily use per premise: size x (BASE + HEAT x HDD) x day noise (therms a gas day).
BASE, HEAT = 0.80, 0.135
DAY_NOISE = 0.055
AMI_SIZE = 0.82          # Pine Harbor converted its newer subdivisions first
HV_PHE = 1.034           # therms per CCF, Pine Harbor's fixed heating value for the winter
HV_NNG = 1.035           # Northbank's average heating value through the winter
# Northbank bills therms as CCF times the heating value of the month a bill is read in (its gate stations'
# monthly average); the gas delivered in a month carries that month's value.
HV_NNG_MONTH = {(2025, 9): 1.037, (2025, 10): 1.036, (2025, 11): 1.035, (2025, 12): 1.034, (2026, 1): 1.034,
                (2026, 2): 1.035, (2026, 3): 1.035, (2026, 4): 1.036, (2026, 5): 1.036}
# Daylight saving: the gas day of 2 November 2025 ran 25 hours and that of 8 March 2026 ran 23.
DST_HOURS = {D(2025, 11, 2): 25, D(2026, 3, 8): 23}


def seed(*parts):
    h = hashlib.blake2b("|".join(str(p) for p in ("task123",) + parts).encode(), digest_size=8).hexdigest()
    return int(h, 16)


def rng(*parts):
    return np.random.default_rng(seed(*parts))


def hdd_series():
    """Heating degree days (65 F base) for the region's gas days: a mild first half of January and a cold snap
    from 19 to 31 January, an ordinary December and a cooling February and March."""
    r = rng("hdd")
    base = np.zeros(NDAY)
    for i, d in enumerate(DAYS):
        doy = (d - D(2026, 1, 15)).days
        b = 47.0 * np.cos(doy / 365.25 * 2 * np.pi) + 18.0
        if d.year == 2026 and d.month == 1:
            b = 26.0 if d.day <= 18 else 69.0
        elif d.year == 2025 and d.month == 12 and d.day >= 20:
            b += 3.0
        elif d.year == 2026 and d.month == 2 and d.day <= 3:
            b = 52.0
        base[i] = b
    noise = np.zeros(NDAY)
    e = r.normal(0, 3.2, NDAY)
    for i in range(NDAY):
        noise[i] = (0.55 * noise[i - 1] if i else 0.0) + e[i]
    return np.clip(base + noise, 0.0, None)


HDD = hdd_series()


def business_days(y, m):
    out = []
    d = D(y, m, 1)
    hol = {D(2025, 9, 1), D(2025, 11, 27), D(2025, 11, 28), D(2025, 12, 25), D(2025, 12, 26), D(2026, 1, 1),
           D(2026, 5, 25)}
    while d.month == m:
        if d.weekday() < 5 and d not in hol:
            out.append(d)
        d += timedelta(1)
    return out


def cycle_day(y, m, k, ncycles):
    """The read date of cycle k (1-based) in month m: the cycles spread over the month's business days."""
    bd = business_days(y, m)
    j = int(round((k - 1) * (len(bd) - 1) / (ncycles - 1)))
    return bd[j]


MONTHS = [(2025, m) for m in range(9, 13)] + [(2026, m) for m in range(1, 6)]

# Bin placement from tune.py: premises each county keeps beyond (+) or short of (-) its base count, taken
# from the non-AMI end of the county's list.
TRIM = {"Ashwell": -38, "Brennock": -3, "Carrow": -63, "Dellmoor": -3, "Evanshade": -3, "Farrish": -14,
        "Glenhollow": 5, "Halvern": -15, "Keswin": 10, "Lorrance": 12, "Merrion": -13}
