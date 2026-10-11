"""The fixed world of task181: the unit's ten areas, postcodes, laboratories, calendars, schools,
hospitals and people. Everything here is a parameter the fiction chose, not a figure the data gave."""
import datetime as dt
import zlib
from zoneinfo import ZoneInfo

import numpy as np

SYD = ZoneInfo("Australia/Sydney")
UTC = dt.timezone.utc
SEED = 1812026

START = dt.date(2019, 1, 1)
LAST_SPECIMEN = dt.date(2026, 10, 4)
EXTRACT_LOCAL = dt.datetime(2026, 10, 5, 7, 0, 2, tzinfo=SYD)
EXTRACT_UTC = EXTRACT_LOCAL.astimezone(UTC)
EXTRACT_DAY = dt.date(2026, 10, 5)
FORTNIGHT = (dt.date(2026, 9, 21), dt.date(2026, 10, 4))
CLUSTER_WINDOW = (dt.date(2026, 9, 5), dt.date(2026, 10, 4))
ASK_PERIOD = (dt.date(2026, 1, 1), dt.date(2026, 8, 31))
PRIOR_YEARS = (2021, 2022, 2023, 2024, 2025)
REVISION = dt.date(2024, 7, 1)          # PR-07 2.3: serology-only cases probable from this date
SLIDE_HISTORY = (dt.date(2025, 8, 1), dt.date(2026, 7, 31))

HOSP_LAB = "Wagga Wagga Hospital Laboratory"
PRIV_LAB = "Inland Pathology"

# name, 2021 census usual residents, ERP 30 June 2025, share of cases notified through the private route
AREAS = [
    ("Wagga Wagga", 67609, 68892, 0.04),
    ("Griffith", 27134, 27705, 0.94),
    ("Leeton", 11391, 11512, 0.90),
    ("Narrandera", 5847, 5791, 0.12),
    ("Murrumbidgee", 3902, 3884, 0.18),
    ("Hay", 2896, 2861, 0.10),
    ("Edward River", 8456, 8462, 0.07),
    ("Junee", 6595, 6703, 0.05),
    ("Cootamundra-Gundagai", 11292, 11344, 0.05),
    ("Snowy Valleys", 14395, 14488, 0.04),
]
AREA_NAMES = [a[0] for a in AREAS]
POP = {a[0]: a[1] for a in AREAS}
ERP = {a[0]: a[2] for a in AREAS}
PRIVATE_SHARE = {a[0]: a[3] for a in AREAS}

# The unit's postcode lookup (adapted from the 2021 Census postcode to LGA correspondence): postcode,
# localities, LGA, share of the postcode's usual residents living in that LGA.
CONCORDANCE = [
    ("2590", "Cootamundra, Stockinbingal, Wallendbeen, Brawlin", "Cootamundra-Gundagai", 1.0),
    ("2594", "Young, Bendick Murrell, Maimuru", "Hilltops", 1.0),
    ("2640", "Albury, East Albury, Lavington, Thurgoona", "Albury", 1.0),
    ("2642", "Jindera, Walla Walla, Culcairn, Gerogery", "Greater Hume", 1.0),
    ("2646", "Corowa, Mulwala, Howlong", "Federation", 1.0),
    ("2650", "Wagga Wagga, Ashmont, Glenfield Park, Kooringal, Lake Albert, Tolland, Turvey Park, Estella", "Wagga Wagga", 1.0),
    ("2651", "Forest Hill, Wagga Wagga RAAF", "Wagga Wagga", 1.0),
    ("2652", "Tarcutta, Humula, Mangoplah, Uranquinty, Ladysmith, Gregadoo", "Greater Hume", 0.19),
    ("2652", "Tarcutta, Humula, Mangoplah, Uranquinty, Ladysmith, Gregadoo", "Wagga Wagga", 0.81),
    ("2653", "Tumbarumba, Rosewood, Tooma, Laurel Hill", "Snowy Valleys", 1.0),
    ("2655", "The Rock, French Park, Bullenbung", "Lockhart", 0.71),
    ("2655", "The Rock, French Park, Bullenbung", "Wagga Wagga", 0.29),
    ("2661", "Kapooka", "Wagga Wagga", 1.0),
    ("2663", "Junee, Old Junee, Bethungra, Illabo", "Junee", 1.0),
    ("2665", "Ardlethan, Beckom, Mirrool, Kamarah", "Coolamon", 0.62),
    ("2665", "Ardlethan, Beckom, Mirrool, Kamarah", "Narrandera", 0.38),
    ("2666", "Temora, Springdale, Gidginbung", "Temora", 1.0),
    ("2675", "Hillston, Goolgowi, Merriwagga", "Carrathool", 1.0),
    ("2678", "Charles Sturt University", "Wagga Wagga", 1.0),
    ("2680", "Griffith, Beelbangera, Bilbul, Hanwood, Yoogali, Lake Wyangan, Tharbogang", "Griffith", 1.0),
    ("2681", "Yenda, Myall Park", "Griffith", 1.0),
    ("2700", "Narrandera, Grong Grong, Gillenbah, Corobimilla", "Narrandera", 1.0),
    ("2701", "Coolamon, Ganmain, Marrar", "Coolamon", 1.0),
    ("2703", "Yanco", "Leeton", 1.0),
    ("2705", "Leeton, Murrami, Whitton, Gogeldrie, Stanbridge", "Leeton", 1.0),
    ("2706", "Darlington Point", "Carrathool", 0.06),
    ("2706", "Darlington Point", "Murrumbidgee", 0.94),
    ("2707", "Coleambally, Argoon", "Murrumbidgee", 1.0),
    ("2710", "Deniliquin, Conargo, Wanganella, Pretty Pine", "Edward River", 1.0),
    ("2711", "Hay, Hay South, Booligal, Maude, One Tree", "Hay", 1.0),
    ("2720", "Tumut, Blowering, Wondalga, Gilmore, Lacmalac", "Snowy Valleys", 1.0),
    ("2722", "Gundagai, South Gundagai, Nangus, Muttama", "Cootamundra-Gundagai", 0.89),
    ("2722", "Gundagai, South Gundagai, Nangus, Muttama", "Snowy Valleys", 0.11),
    ("2727", "Coolac, Adjungbilly, Gobarralong", "Cootamundra-Gundagai", 0.52),
    ("2727", "Coolac, Adjungbilly, Gobarralong", "Snowy Valleys", 0.48),
    ("2729", "Adelong, Grahamstown, Mount Adrah", "Cootamundra-Gundagai", 0.18),
    ("2729", "Adelong, Grahamstown, Mount Adrah", "Snowy Valleys", 0.82),
    ("2730", "Batlow", "Snowy Valleys", 1.0),
    ("2732", "Barham, Koraleigh", "Murray River", 1.0),
    ("3644", "Cobram, Barooga", "Moira (Vic.)", 1.0),
]
NEIGHBOUR_POP = {"Albury": (56093, 57610), "Carrathool": (2733, 2690), "Coolamon": (4440, 4511),
                 "Federation": (12904, 13063), "Greater Hume": (10910, 11173), "Hilltops": (18986, 19352),
                 "Lockhart": (3285, 3307), "Murray River": (12620, 12931), "Temora": (6242, 6297)}


def allocate(postcode):
    """PR-07 3.4: the area of the postcode's larger population share (None when outside the ten)."""
    rows = [r for r in CONCORDANCE if r[0] == postcode]
    if not rows:
        return None
    best = max(rows, key=lambda r: r[3])
    return best[2] if best[2] in POP else None


# Residential postcodes cases are drawn from: the clean path (main call windows) uses only
# postcodes wholly inside one area; the rest of the record also uses the split ones.
HOME_POSTCODES = {
    "Wagga Wagga": [("2650", 0.88), ("2651", 0.04), ("2661", 0.02), ("2678", 0.02), ("2652", 0.03), ("2655", 0.01)],
    "Griffith": [("2680", 0.86), ("2681", 0.14)],
    "Leeton": [("2705", 0.88), ("2703", 0.12)],
    "Narrandera": [("2700", 0.93), ("2665", 0.07)],
    "Murrumbidgee": [("2707", 0.55), ("2706", 0.45)],
    "Hay": [("2711", 1.0)],
    "Edward River": [("2710", 1.0)],
    "Junee": [("2663", 1.0)],
    "Cootamundra-Gundagai": [("2590", 0.62), ("2722", 0.30), ("2727", 0.04), ("2729", 0.04)],
    "Snowy Valleys": [("2720", 0.58), ("2729", 0.12), ("2730", 0.15), ("2653", 0.13), ("2722", 0.01), ("2727", 0.01)],
}
CLEAN_POSTCODES = {a: [p for p, _ in v if allocate(p) == a and all(r[3] == 1.0 for r in CONCORDANCE if r[0] == p)]
                   for a, v in HOME_POSTCODES.items()}
VISITOR_POSTCODES = [("2640", 0.25), ("2666", 0.16), ("2594", 0.10), ("2655", 0.12), ("2665", 0.07),
                     ("2701", 0.10), ("2675", 0.06), ("2646", 0.06), ("3644", 0.04), ("2732", 0.04)]

# Hospitals (the district's facilities) and the town each area's hospital-route specimens travel from.
FACILITIES = ["Wagga Wagga Hospital", "Griffith Hospital", "Leeton Hospital", "Narrandera Hospital",
              "Hay Hospital", "Deniliquin Hospital", "Junee Hospital", "Cootamundra Hospital",
              "Gundagai Hospital", "Tumut Hospital", "Batlow Hospital", "Tumbarumba Hospital"]
AREA_FACILITY = {"Wagga Wagga": "Wagga Wagga Hospital", "Griffith": "Griffith Hospital", "Leeton": "Leeton Hospital",
                 "Narrandera": "Narrandera Hospital", "Murrumbidgee": "Griffith Hospital", "Hay": "Hay Hospital",
                 "Edward River": "Deniliquin Hospital", "Junee": "Junee Hospital",
                 "Cootamundra-Gundagai": "Cootamundra Hospital", "Snowy Valleys": "Tumut Hospital"}


def _easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    month = (h + l_ - 7 * m + 114) // 31
    day = ((h + l_ - 7 * m + 114) % 31) + 1
    return dt.date(y, month, day)


def _nth_monday(y, month, n):
    d = dt.date(y, month, 1)
    d += dt.timedelta(days=(0 - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def nsw_holidays(y):
    """NSW public holidays (state-wide) for year y, with the substitute days NSW observes."""
    h = set()
    nyd = dt.date(y, 1, 1)
    h.add(nyd if nyd.weekday() < 5 else nyd + dt.timedelta(days=7 - nyd.weekday()))
    aus = dt.date(y, 1, 26)
    h.add(aus if aus.weekday() < 5 else aus + dt.timedelta(days=7 - aus.weekday()))
    e = _easter(y)
    for k in (-2, -1, 0, 1):
        h.add(e + dt.timedelta(days=k))
    h.add(dt.date(y, 4, 25))
    h.add(_nth_monday(y, 6, 2))
    h.add(_nth_monday(y, 10, 1))
    xmas, box = dt.date(y, 12, 25), dt.date(y, 12, 26)
    if xmas.weekday() == 5:
        h |= {xmas, box, dt.date(y, 12, 27), dt.date(y, 12, 28)}
    elif xmas.weekday() == 6:
        h |= {xmas, box, dt.date(y, 12, 27)}
    elif xmas.weekday() == 4:
        h |= {xmas, box, dt.date(y, 12, 28)}
    else:
        h |= {xmas, box}
    if y == 2022:
        h.add(dt.date(2022, 9, 22))        # National Day of Mourning
    return h


HOLIDAYS = set()
for _y in range(2018, 2028):
    HOLIDAYS |= nsw_holidays(_y)


def working_day(d):
    return d.weekday() < 5 and d not in HOLIDAYS


# Schools the unit holds enrolment rosters for (received during follow-up this term). The roster
# spelling is the school's own; variants are how parents and students write it at interview.
SCHOOLS = [
    # key, roster name, sector, street address, town, LGA, enrolment
    ("banna", "Banna Avenue Public School", "Government", "211 Banna Avenue", "Griffith", "Griffith", 412),
    ("kooyoo", "Kooyoo Street Public School", "Government", "18 Kooyoo Street", "Griffith", "Griffith", 286),
    ("wollundry", "Wollundry Public School", "Government", "40 Fitzmaurice Street", "Wagga Wagga", "Wagga Wagga", 344),
    ("bolton", "Bolton Park High School", "Government", "2 Tarcutta Street", "Wagga Wagga", "Wagga Wagga", 731),
    ("blowering", "Blowering Road Public School", "Government", "57 Blowering Road", "Tumut", "Snowy Valleys", 238),
    ("canal", "Canal Road Public School", "Government", "9 Canal Road", "Leeton", "Leeton", 305),
    ("hurley", "Hurley Street Public School", "Government", "12 Hurley Street", "Cootamundra", "Cootamundra-Gundagai", 167),
    ("twynam", "Twynam Street Public School", "Government", "33 Twynam Street", "Narrandera", "Narrandera", 214),
    ("fernleigh", "Fernleigh Road Public School", "Government", "140 Fernleigh Road", "Wagga Wagga", "Wagga Wagga", 389),
]
SCHOOL = {s[0]: s for s in SCHOOLS}
SPELLINGS = {
    "banna": ["Banna Ave PS", "Banna Avenue Public", "banna ave public school", "Banna Av. P.S.",
              "Banna Avenue Public School", "Banna Ave Public School"],
    "kooyoo": ["Kooyoo St PS", "Kooyoo Street Public School", "Kooyoo Street Public", "kooyoo st public school griffith"],
    "wollundry": ["Wollundry PS", "Wollundry Public School", "Wollundry Public", "wollundry public school wagga"],
    "bolton": ["Bolton Park High", "Bolton Park HS", "Bolton Park High School", "bolton park high wagga"],
    "blowering": ["Blowering Rd PS", "Blowering Road Public School", "Blowering Road Public", "blowering rd public tumut"],
    "canal": ["Canal Rd PS", "Canal Road Public School", "Canal Road Public"],
    "hurley": ["Hurley St Public", "Hurley Street Public School", "Hurley Street PS"],
    "twynam": ["Twynam St PS", "Twynam Street Public School"],
    "fernleigh": ["Fernleigh Rd PS", "Fernleigh Road Public School", "Fernleigh Road Public"],
    "wollundry_pre": ["Wollundry Preschool", "Wollundry Pre-school"],
}

PEOPLE = {
    "director": "Nathan Olson",
    "epidemiologist": "Tiffany Peters",
    "team_leader": "Janice Barker",
    "immunisation": "Darryl Morales",
    "nurse": "Colleen Brown",
    "data_officer": "Cassandra Dawson",
}
UNIT = "Southern Inland Public Health Unit"
LHD = "Southern Inland Local Health District"


def stream(*keys):
    """A named, reproducible random stream."""
    ints = [SEED] + [zlib.crc32(str(k).encode()) for k in keys]
    return np.random.default_rng(np.random.SeedSequence(ints))


def local_to_utc(t):
    if t.tzinfo is None:
        t = t.replace(tzinfo=SYD)
    return t.astimezone(UTC)


def utc_to_local(t):
    return t.astimezone(SYD)


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)
