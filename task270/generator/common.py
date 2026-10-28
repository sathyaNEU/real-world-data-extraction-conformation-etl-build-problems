"""task270 constants and helpers shared by every generator module.

Tidewell Coast and Ranges Primary Health Network is a not-for-profit company the Commonwealth funds to commission
primary care for twelve New South Wales local government areas: four on the coast, the regional city of
Bannockvale, five inland and two on the city's fringe. Its 2028 to 2030 late-life frailty program goes to each area
whose residents reaching 85 could expect fewer than seven more years under the area's 2024 to 2026 death rates. Every
file was taken on Wednesday 15 September 2027 for the program's area list."""
from __future__ import annotations

import csv
import datetime as dt
import io

import numpy as np

SEED = 27011

PHN = "Tidewell Coast and Ranges Primary Health Network"
PHN_SHORT = "Tidewell Coast and Ranges PHN"
AH_SERVICE = "Tidewell After Hours Medical Service"
DOMAIN = "tidewellphn.org.au"

PEOPLE = {
    "planning": "Melanie Howard",     # manager, population health planning: the program's area list (the requester)
    "commissioning": "Jack Armstrong",  # executive manager, commissioning: the program guidelines
    "analyst": "Julia Larson",        # senior data analyst: the data release agreement and the files
}

AS_OF = dt.date(2027, 9, 15)          # every file taken for the program's area list
EXTRACT_TO = dt.date(2027, 6, 30)     # the registry extract holds registrations to 30 June 2027
CENSUS = dt.date(2021, 8, 10)         # census night
WINDOW = (2024, 2025, 2026)           # the program's death-rate years
LINE = 7.0                            # an area qualifies when life expectancy at 85 is below seven years
TOP = 95                              # the life table's last group is 95 and over
AH_YEAR = 2026                        # the after-hours asks
MIGRATION = dt.date(2026, 7, 1)       # the after-hours service's new clinical system went live

# ------------------------------------------------------------------------------------------------- the twelve areas
# name, LGA code (2023), type, SA2 names, 2026 population, waves on the cohorts' sizes at 60 (amplitude, centre birth
# year, spread in years), share of residents' deaths registered in another state, golden target
AREAS = [
    ("Bannockvale", "10700", "city",
     ["Bannockvale - Central", "Bannockvale - East", "Bannockvale - North", "Bannockvale - South",
      "Bannockvale - West", "Bannockvale Surrounds"], 95400, [], 0.004),
    ("Cobbleton", "11640", "inland", ["Cobbleton", "Cobbleton Surrounds", "Brindlemere"], 25900,
     [(-0.40, 1940, 3.0)], 0.006),
    ("Coldwater Plains", "11680", "inland", ["Coldwater", "Coldwater Plains Surrounds", "Hessian Flat"], 23700,
     [(-0.15, 1938, 4.0)], 0.012),
    ("Dunesford", "12210", "coast", ["Dunesford - East", "Dunesford - West", "Ospreyvale", "Dunesford Surrounds"],
     47800, [(0.62, 1939.5, 2.5)], 0.003),
    ("Gannetmouth", "13560", "coast", ["Gannetmouth", "Gannetmouth - South", "Larkspur", "Gannetmouth Surrounds"],
     58300, [(0.70, 1928, 3.0), (0.40, 1941, 3.0)], 0.009),
    ("Kestrelmoor", "14590", "peri", ["Kestrelmoor - East", "Kestrelmoor - West", "Bramblewood"], 47200,
     [(0.15, 1930, 4.0)], 0.002),
    ("Mallowmere", "15110", "peri", ["Mallowmere - North", "Mallowmere - South", "Mallowmere Surrounds"], 53600,
     [(0.25, 1944, 4.0)], 0.002),
    ("Merriwold", "15320", "inland", ["Merriwold", "Merriwold Surrounds", "Fallowfield", "Tallowmere"], 30800,
     [(-0.10, 1936, 4.0)], 0.010),
    ("Saltwick Shoals", "16920", "coast", ["Saltwick Shoals - North", "Saltwick Shoals - South",
                                           "Saltwick Shoals - West", "Driftwood Bay", "Gullsby"], 62100,
     [(0.62, 1940, 2.5)], 0.008),
    ("Spraymouth", "17060", "coast", ["Spraymouth", "Spraymouth Surrounds", "Ribbonwood"], 36400,
     [(1.60, 1932, 2.0)], 0.010),
    ("Windermoor", "18290", "inland", ["Windermoor", "Windermoor Surrounds"], 17300, [(-0.20, 1940, 4.0)], 0.022),
    ("Wolfram Ranges", "18440", "inland", ["Wolfram", "Wolfram Ranges Surrounds", "Ironbridge Plains", "Thistlebank"],
     20400, [(-0.15, 1937, 4.0)], 0.018),
]
AREA_NAMES = [a[0] for a in AREAS]
AREA_CODE = {a[0]: a[1] for a in AREAS}
AREA_TYPE = {a[0]: a[2] for a in AREAS}
# Thistlebank was part of Merriwold until the 2023 boundary adjustment moved it to Wolfram Ranges (1 July 2023)
MOVED_SA2 = "Thistlebank"
MOVED_FROM = "Merriwold"
BOUNDARY_DATE = dt.date(2023, 7, 1)

# the golden life expectancy at 85 each area's mortality level is tuned to (tune.py), each on a one-decimal centre
TARGET = {"Windermoor": 6.70, "Coldwater Plains": 6.80, "Saltwick Shoals": 6.89, "Dunesford": 6.90,
          "Cobbleton": 7.11, "Spraymouth": 7.19, "Merriwold": 7.21, "Bannockvale": 7.29, "Wolfram Ranges": 7.31,
          "Kestrelmoor": 7.39, "Mallowmere": 7.41, "Gannetmouth": 7.49}

# each area's mortality level (its rate at 85 in mid 2025), set by tune.py so the golden sits on its target
LEVELS = {
    "Bannockvale": 0.065902,
    "Cobbleton": 0.069183,
    "Coldwater Plains": 0.075226,
    "Dunesford": 0.079860,
    "Gannetmouth": 0.064754,
    "Kestrelmoor": 0.068231,
    "Mallowmere": 0.062857,
    "Merriwold": 0.068699,
    "Saltwick Shoals": 0.074510,
    "Spraymouth": 0.068327,
    "Windermoor": 0.080469,
    "Wolfram Ranges": 0.065578,
}

# file names
F_DEATHS = "bdm_death_registrations_tidewell_2016_2027.csv"
F_INTERSTATE = "interstate_deaths_tidewell_residents_2016_2027.xlsx"
F_CENSUS = "census2021_sa2_age_sex_ur.csv"
F_ERP = "erp_lga_age_sex_2016_2026.xlsx"
F_NSW = "erp_nsw_single_year_age_sex_2016_2026.csv"
F_CORR = "asgs2021_sa2_to_lga2023.csv"
F_GUIDE = "late_life_frailty_program_guidelines_2028_2030.pdf"
F_AH = "afterhours_attendances_2026.csv"
F_RACF = "residential_aged_care_services_tidewell_2026.xlsx"
F_FALLS = "falls_injury_hospitalisations_65plus_lga_2024_25.csv"
DISTRACTORS = [F_NSW, F_RACF, F_FALLS]

G_BOOK = "lga_life_expectancy_at_85_2024_2026.xlsx"
G_CHART = "lga_life_expectancy_at_85.png"

NSW_HOLIDAYS_2026 = [dt.date(2026, 1, 1), dt.date(2026, 1, 26), dt.date(2026, 4, 3), dt.date(2026, 4, 4),
                     dt.date(2026, 4, 5), dt.date(2026, 4, 6), dt.date(2026, 4, 25), dt.date(2026, 6, 8),
                     dt.date(2026, 10, 5), dt.date(2026, 12, 25), dt.date(2026, 12, 26), dt.date(2026, 12, 28)]
# daylight saving in New South Wales: AEDT (+11:00) until 03:00 on 5 April 2026, AEST (+10:00) to 02:00 on 4 October
DST_END_2026 = dt.datetime(2026, 4, 5, 3, 0)
DST_START_2026 = dt.datetime(2026, 10, 4, 2, 0)


def rng(*keys):
    """A generator seeded by the build seed and a label, so each stream is independent and reproducible."""
    h = SEED
    for k in keys:
        for ch in str(k):
            h = (h * 1000003 + ord(ch)) % (2 ** 61 - 1)
    return np.random.default_rng(h)


def offset_for(local):
    """The NSW UTC offset in force at a local wall-clock time in 2026 (+11:00 in daylight time, else +10:00)."""
    return "+11:00" if (local < DST_END_2026 or local >= DST_START_2026) else "+10:00"


def write_csv(path, header, rows, preamble=None, footer=None, crlf=True):
    """Write a CSV the way the producing systems export it (CRLF line ends unless told otherwise)."""
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    for line in preamble or []:
        w.writerow(line)
    w.writerow(header)
    n = 0
    for r in rows:
        w.writerow(r)
        n += 1
    for line in footer or []:
        w.writerow(line)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return n


def age_on(dob, day):
    """Age in completed years on a date."""
    return day.year - dob.year - ((day.month, day.day) < (dob.month, dob.day))
