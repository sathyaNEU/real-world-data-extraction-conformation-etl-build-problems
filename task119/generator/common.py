"""Shared constants and helpers for the task119 generator.

Times inside the generator are integers: minutes on the local wall clock (Europe/London) since
2023-01-01 00:00. No referral wait crosses a clock change, so a difference of two local minutes is
the elapsed time. UTC is used only where a source system held UTC.
"""
import datetime as dt
import zoneinfo

import numpy as np

SEED = 119
TZ = zoneinfo.ZoneInfo("Europe/London")
UTCZ = dt.timezone.utc
EPOCH = dt.datetime(2023, 1, 1, 0, 0)
DAY = 1440


def lm(d, hh=0, mm=0):
    """Local minute of a date (or datetime) plus a time of day."""
    if isinstance(d, dt.datetime):
        return int((d - EPOCH).total_seconds() // 60)
    return int((dt.datetime(d.year, d.month, d.day, hh, mm) - EPOCH).total_seconds() // 60)


def to_dt(m):
    return EPOCH + dt.timedelta(minutes=int(m))


def day_of(m):
    return (EPOCH + dt.timedelta(minutes=int(m))).date()


def dayidx(d):
    return (d - EPOCH.date()).days


def tod(m):
    return int(m) % DAY


def fmt(m):
    return to_dt(m).strftime("%Y-%m-%d %H:%M")


def local_to_utc_min(m):
    t = to_dt(m).replace(tzinfo=TZ)
    u = t.astimezone(UTCZ).replace(tzinfo=None)
    return int((u - EPOCH).total_seconds() // 60)


def utc_to_local_min(m):
    u = to_dt(m).replace(tzinfo=UTCZ)
    t = u.astimezone(TZ).replace(tzinfo=None)
    return int((t - EPOCH).total_seconds() // 60)


def is_bst(m):
    return local_to_utc_min(m) != m


# ------------------------------------------------------------------------------------------ calendar
RECORD0 = dt.date(2023, 7, 1)
RECORD1 = dt.date(2026, 6, 30)
FEED0 = dt.date(2023, 6, 1)
CAL1 = dt.date(2026, 7, 31)
GO_LIVE = dt.date(2024, 4, 2)          # first platform day; earlier decisions are migrated CCRS records
PARALLEL0 = dt.date(2024, 2, 19)       # pilot wards entered referrals on both systems
PARALLEL1 = dt.date(2024, 3, 29)       # last pilot-ward duplicate
CONSOLIDATION = dt.date(2024, 4, 1)    # level-3 beds leave ELL-ACC; PEL-W3 closed 31 March 2024
WINTER0, WINTER1 = dt.date(2023, 12, 4), dt.date(2024, 3, 31)
EXTRACT = dt.date(2026, 8, 14)
AS_OF = dt.date(2026, 10, 2)
YEARS = {1: (dt.date(2023, 7, 1), dt.date(2024, 6, 30)),
         2: (dt.date(2024, 7, 1), dt.date(2025, 6, 30)),
         3: (dt.date(2025, 7, 1), dt.date(2026, 6, 30))}

# England and Wales bank holidays inside the record
BANK_HOLIDAYS = {dt.date(*x) for x in [
    (2023, 8, 28), (2023, 12, 25), (2023, 12, 26), (2024, 1, 1), (2024, 3, 29), (2024, 4, 1), (2024, 5, 6),
    (2024, 5, 27), (2024, 8, 26), (2024, 12, 25), (2024, 12, 26), (2025, 1, 1), (2025, 4, 18), (2025, 4, 21),
    (2025, 5, 5), (2025, 5, 26), (2025, 8, 25), (2025, 12, 25), (2025, 12, 26), (2026, 1, 1), (2026, 4, 3),
    (2026, 4, 6), (2026, 5, 4), (2026, 5, 25)]}
# clock changes inside the feed span, as local minutes of the 01:00 wall-clock hour on each date
DST_DAYS = [dt.date(2023, 10, 29), dt.date(2024, 3, 31), dt.date(2024, 10, 27), dt.date(2025, 3, 30),
            dt.date(2025, 10, 26), dt.date(2026, 3, 29)]


def year_of(d):
    for y, (a, b) in YEARS.items():
        if a <= d <= b:
            return y
    return None


def is_list_day(d):
    return d.weekday() < 5 and d not in BANK_HOLIDAYS


def dst_window(d):
    """Local minutes [00:30, 02:30) on a clock-change date, kept free of every timed event."""
    return lm(d, 0, 30), lm(d, 2, 30)


DST_WINDOWS = [dst_window(d) for d in DST_DAYS]


def crosses_dst(a, b):
    for x, y in DST_WINDOWS:
        if a < y and b > x:
            return True
    return False


# ------------------------------------------------------------------------------------------ the world
REGION = "Wenmarsh"
BOARD = "Wenmarsh Regional Health Board"
NETWORK = "Wenmarsh Adult Critical Care Network"
PROVIDER = "Thornleholm Clinical Review LLP"
PROGRAMME = "National Rapid Review Programme"

# letter in the design note -> code, name, sites
TRUSTS = {
    "A": ("RIS", "Ristenholm Teaching Hospitals NHS Foundation Trust", "Ristenholm General Hospital"),
    "B": ("TAN", "Tannerby Hospital NHS Trust", "Tannerby Hospital"),
    "C": ("BRK", "Brackenford Hospitals NHS Foundation Trust", "Brackenford Royal Infirmary"),
    "D": ("STN", "Stennock University Hospitals NHS Foundation Trust", "Stennock University Hospital"),
    "E": ("LAT", "Lathingbury Hospitals NHS Trust", "Lathingbury District Hospital"),
    "F": ("ELL", "Ellerdyke Hospitals NHS Trust", "Ellerdyke Hospital"),
    "G": ("PRW", "Prideswick Hospitals NHS Foundation Trust", "Prideswick County Hospital"),
    "H": ("PEL", "Pellowham Hospitals NHS Trust", "Pellowham Hospital"),
}
LETTERS = list("ABCDEFGH")
CODE = {k: v[0] for k, v in TRUSTS.items()}
LETTER = {v[0]: k for k, v in TRUSTS.items()}
TRUST_CODES = [CODE[k] for k in LETTERS]

# level-3 bed units carried by the network feed; beds are staffed beds (equal to physical in the record)
UNIT_OF = {"A": "RIS-ACC", "C": "BRK-ACC", "D": "STN-ACC", "G": "PRW-ACC", "F": "ELL-ACC", "H": "PEL-W3"}
BEDS = {"RIS-ACC": 30, "BRK-ACC": 16, "STN-ACC": 18, "PRW-ACC": 12, "ELL-ACC": 8, "PEL-W3": 3}
FEED_UNITS = ["RIS-ACC", "BRK-ACC", "STN-ACC", "PRW-ACC", "ELL-ACC", "PEL-W3"]
CORE_UNITS = ["RIS-ACC", "BRK-ACC", "STN-ACC", "PRW-ACC"]
HDU = {"B": "TAN-HDU", "E": "LAT-HDU", "H": "PEL-HDU", "F": "ELL-ACC"}


def own_unit(letter, d):
    """The level-3 unit the trust held on date d, or None."""
    if letter in ("A", "C", "D", "G"):
        return UNIT_OF[letter]
    if letter == "F" and d <= dt.date(2024, 3, 31):
        return "ELL-ACC"
    if letter == "H" and WINTER0 <= d <= WINTER1:
        return "PEL-W3"
    return None


def unit_open(unit, d):
    if unit == "ELL-ACC":
        return d <= dt.date(2024, 3, 31)
    if unit == "PEL-W3":
        return WINTER0 <= d <= WINTER1
    return True


PEOPLE = {
    "requester": ("Andrea Davey", "Head of Quality Surveillance"),
    "chair": ("Norman Scott", "Chair"),
    "network": ("Maria Reynolds", "Critical Care Network Manager"),
    "info": ("Diana Smith", "Information Manager"),
    "programme": ("Sharon Banks", "Programme Coordinator"),
    "reviewer": ("Benjamin Davies", "Lead Reviewer"),
}

# neighbouring regions and the trusts the national programme reviewed there
CORPUS_REGIONS = {
    "Haskminster": ["Feningby", "Barlewick", "Calesgate", "Ashenstow"],
    "Isterdale": ["Ormerleby", "Elmowbury", "Rookerholm", "Vellesford"],
    "Tevermouth": ["Selarwell", "Frithleton", "Lestowe", "Cranerby"],
    "Morrowcombe": ["Morrerford", "Tamarwell", "Esklecombe", "Kirkenstead"],
}
TWIN_A = ("Ormerleby", 2022)
TWIN_B = ("Selarwell", 2023)
WINDOW_CASE = ("Feningby", 2021)

INVENTED_NAMES = ([REGION, "Thornleholm"] + [v[1] for v in TRUSTS.values()] + [v[2] for v in TRUSTS.values()]
                  + list(CORPUS_REGIONS) + [t for ts in CORPUS_REGIONS.values() for t in ts])


def rng(*keys):
    """An independent, stable random stream per component."""
    ss = np.random.SeedSequence([SEED] + [abs(hash_str(k)) % (2 ** 31) for k in keys])
    return np.random.Generator(np.random.PCG64(ss))


def hash_str(s):
    h = 2166136261
    for ch in str(s).encode():
        h = ((h ^ ch) * 16777619) & 0xFFFFFFFF
    return h
