"""The City of Calderbrook and the Ridgemont Line: the fixed facts of the world.

Money in Canadian dollars. Areas in square feet. The market indices are the reference tables' own series; the
redevelopment rates are the generating process (never shipped)."""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 13427
TZ = ZoneInfo("America/Vancouver")


def utc_stamp(local):
    return local.replace(tzinfo=TZ).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def posix(local):
    return local.replace(tzinfo=TZ).timestamp()


YEARS = list(range(2014, 2027))          # roll years and permit years on record
FWD = list(range(2027, 2032))            # the target period
ASOF = dt.date(2026, 12, 31)
ORDER_DATE = dt.date(2026, 6, 30)        # the order is made and Schedule A drawn
IN_FORCE = dt.date(2027, 1, 1)
ROLL_CONDITION = {y: dt.date(y - 1, 10, 31) for y in YEARS}   # physical condition date of each roll

# ------------------------------------------------------------------------------------------------ places
STATIONS = ["ELL", "WES", "HAL", "PEL"]
AREA_NAME = {"ELL": "Ellery", "WES": "Westerly", "HAL": "Haldane", "PEL": "Pell Road", "CC": "Calderbrook Centre",
             "NC": "North Calder", "RAV": "Ravensdale", "FER": "Fernlea"}
NEIGHBOURHOODS = ["NC", "RAV", "FER"]
TIER_BAND = {1: "Within 200 m", 2: "200 m to 400 m", 3: "400 m to 800 m"}
TIER_FAR = {1: 5.0, 2: 4.0, 3: 3.0}
TIER_STOREYS = {1: 20, 2: 12, 3: 8}
# assessment district code of each area (the first block of the folio)
DISTRICT = {"ELL": "4113", "WES": "4121", "HAL": "4136", "PEL": "4142", "CC": "4105", "NC": "4158", "RAV": "4164",
            "FER": "4172"}
# street grid: each station at an avenue and street crossing; corridors are the arterials through it
GRID = {"ELL": (104, 136), "WES": (104, 148), "HAL": (100, 160), "PEL": (96, 172), "CC": (88, 132),
        "NC": (112, 128), "RAV": (76, 144), "FER": (68, 164)}
ARTERIAL = {"ELL": "Ellery Road", "WES": "Westerly Avenue", "HAL": "Haldane Boulevard", "PEL": "Pell Road",
            "CC": "Calder Way", "NC": "Kerslake Road", "RAV": "Ravensdale Road", "FER": "Fernlea Drive"}

# ------------------------------------------------------------------------------------------------ zoning
# zone history: code before the 2020 consolidation, code after, residential form permitted, maximum FAR by year
ZONES = {
    "RS-1": dict(new="R1", name="Single detached residential", form="house", far=lambda y: 0.7),
    "RT-2": dict(new="RM1", name="Townhouse infill residential", form="town", far=lambda y: 1.2),
    "C-2": dict(new="C2", name="Community commercial", form="none", far=lambda y: 0.0),
    "RM-3": dict(new="RA1", name="Low-rise apartment residential", form="apartment", far=lambda y: 1.5),
    "CR-3": dict(new="MU3", name="Corridor mixed use", form="apartment", far=lambda y: 3.0),
    "C-3": dict(new="CC1", name="Town centre commercial", form="apartment", far=lambda y: 3.0),
    "CD-CC": dict(new="CC1", name="City Centre comprehensive development", form="tower", far=lambda y: 5.5),
    "RM-5": dict(new="RA3", name="Apartment and townhouse residential (strata)", form="apartment", far=lambda y: 1.8),
}
CONSOLIDATION = dt.date(2020, 3, 2)      # the zoning bylaw consolidation renames every code

# rezonings: (group, from code, to code, effective date)
REZONINGS = {
    "CC": ("C-3", "CD-CC", dt.date(2016, 4, 18)),
    "CORR_H": ("RS-1", "CR-3", dt.date(2013, 4, 15)),
    "CORR_C": ("C-2", "CR-3", dt.date(2013, 4, 15)),
    "CORR_R": ("RM-3", "CR-3", dt.date(2013, 4, 15)),
    "TH": ("RS-1", "RT-2", dt.date(2019, 6, 10)),
}

# ------------------------------------------------------------------------------------------------ buildings
# building types (reference tables): FAR reached on a typical lot (None: the permitted maximum), net-to-gross,
# average net floor area per home, product for the sale value, residential form needed
BTYPES = {
    "TH3": dict(far=1.2, eff=0.92, nsf=1350.0, product="town", form="town", storeys=3, cons="Wood frame",
                desc="Townhouses and rowhouses"),
    "LR4": dict(far=2.0, eff=0.85, nsf=820.0, product="wood", form="apartment", storeys=4, cons="Wood frame",
                desc="Low-rise apartment"),
    "MR6": dict(far=3.0, eff=0.85, nsf=820.0, product="wood", form="apartment", storeys=6, cons="Wood frame",
                desc="Mid-rise apartment"),
    "HR": dict(far=None, eff=0.82, nsf=790.0, product="conc", form="tower", storeys=None, cons="Concrete",
               desc="High-rise apartment"),
}
COST26 = {"TH3": 680.0, "LR4": 700.0, "MR6": 720.0, "HR": 1085.0}
WOOD26 = {"ELL": 1240, "WES": 1205, "HAL": 1175, "PEL": 1150, "CC": 1480, "NC": 1195, "RAV": 1170, "FER": 1140}
CONC26 = {"ELL": 1312, "WES": 1281, "HAL": 1247, "PEL": 1219, "CC": 1760, "NC": 1268, "RAV": 1239, "FER": 1206}
TOWN26 = {"ELL": 884, "WES": 857, "HAL": 840, "PEL": 818, "CC": 1056, "NC": 849, "RAV": 834, "FER": 814}


def _path(y, pts):
    ys = sorted(pts)
    if y <= ys[0]:
        return pts[ys[0]]
    for a, b in zip(ys, ys[1:]):
        if a <= y <= b:
            return pts[a] + (pts[b] - pts[a]) * (y - a) / (b - a)
    return pts[ys[-1]]


# indices to 2026 = 1.000: new home values, all-in construction costs, assessed land, assessed improvements
VP = {y: round(_path(y, {2014: .700, 2017: .861, 2022: 1.041, 2024: 1.012, 2026: 1.000}), 4) for y in YEARS}
CP = {y: round(_path(y, {2014: .712, 2018: .803, 2022: .968, 2026: 1.000}), 4) for y in YEARS}
LP = {y: round(_path(y, {2014: .658, 2017: .818, 2022: 1.052, 2024: 1.021, 2026: 1.000}), 4) for y in YEARS}
IP = {y: round(_path(y, {2014: .741, 2018: .826, 2022: .975, 2026: 1.000}), 4) for y in YEARS}
# per-area and per-type wobble on the published series (each series is its own survey)
AREA_WOBBLE = {"ELL": [0, 4, -3, 2, 0, -2, 3, 1, -1, 2, -2, 1, 0], "WES": [2, -1, 0, 3, -2, 1, -1, 2, 0, -3, 1, 0, 0],
               "HAL": [-1, 2, 1, -2, 3, 0, -2, 1, 2, 0, -1, 2, 0], "PEL": [1, 0, -2, 1, 2, -1, 0, -3, 1, 1, 2, -1, 0],
               "CC": [3, -2, 2, 0, -1, 3, 1, -2, 0, 2, 1, -2, 0], "NC": [0, 1, 2, -1, 0, 2, -2, 0, 3, -1, 0, 1, 0],
               "RAV": [-2, 0, 1, 2, -1, 0, 2, -1, 0, 1, -2, 2, 0], "FER": [1, -1, 0, 0, 2, -2, 1, 2, -1, 0, 1, -1, 0]}
TYPE_WOBBLE = {"TH3": [0, 2, -1, 1, 0, -2, 1, 0, 2, -1, 0, 1, 0], "LR4": [1, 0, 1, -1, 2, 0, -1, 1, 0, 1, -1, 0, 0],
               "MR6": [-1, 1, 0, 2, -1, 1, 0, -2, 1, 0, 2, -1, 0], "HR": [2, -1, 1, 0, 1, -1, 2, 0, -1, 2, 0, -2, 0]}


def value(area, product, y):
    base = {"wood": WOOD26, "conc": CONC26, "town": TOWN26}[product][area]
    return round(base * VP[y] + AREA_WOBBLE[area][y - 2014] * (0.6 if product == "town" else 1.0))


def cost(btype, y):
    return round(COST26[btype] * CP[y] + TYPE_WOBBLE[btype][y - 2014])


# ------------------------------------------------------------------------------------------------ process
RATE = {"house": 0.030, "comm": 0.085, "rental": 0.020}     # annual rebuild rate of a feasible lot, by kind
JITTER = 1.0                                                # systematic sampling slack, rebuilds per kind

# lots: station areas by tier (scaled), City Centre, neighbourhoods
TOD_BASE = {1: 120, 2: 230, 3: 380}
TOD_SCALE = 0.88
TOD_SHARE = {"comm": 0.17, "rental": 0.12}
TOD_EXTRA_HOUSES = 1493
NB_CORR = {"house": 500, "comm": 600, "rental": 150}
TH_N = 1200
CC_N = {"comm": 700, "rental": 150}
LAND_PSF = {"ELL": 330, "WES": 320, "HAL": 311, "PEL": 303, "CC": 470, "NC": 318, "RAV": 309, "FER": 300}
LOT_MU = {"house": 7800, "comm": 12000, "rental": 13000, "cc": 7500}

# ------------------------------------------------------------------------------------------------ people
PEOPLE = {"branch_lead": "Tonya Bartlett", "analyst": "Zachary Tyler", "city_gis": "Monique Knapp",
          "permits": "Alec Heath"}
MINISTRY = "Ministry of Housing"
BRANCH = "Housing Targets Branch"
CITY = "City of Calderbrook"
