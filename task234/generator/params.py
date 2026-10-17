"""task234 world: Tamsen County's respiratory laboratory feeds, ten laboratories, MMWR week 3 of 2027, and the week's
escalations the surveillance data manager sets for the laboratory liaison."""
import datetime as dt

SEED = 234
WORLD_SEED = 20                      # the epidemic world (sim.World)
RECORDS_SEED = SEED * 1009 + 7       # reports, cancelled orders, message ids, distractors (records.Records)
WEEK_SEED = {2: 76, 3: 195}   # each week's tests and messages
TZ_OFFSET_H = -6                     # America/Chicago in January (CST)
COUNTY = "Tamsen County"
POPULATION = 5_100_000
DEPT = "Tamsen County Department of Public Health"
UNIT = "Epidemiology Unit"
PEOPLE = {"manager": "Michaela Mclean", "liaison": "Travis Humphrey", "epi": "Kaitlyn Sanchez"}

# MMWR weeks: week 1 of a year starts on the Sunday on or before 4 January
def mmwr_start(y):
    j4 = dt.date(y, 1, 4)
    return j4 - dt.timedelta(days=(j4.weekday() + 1) % 7)

FIRST_WEEK = mmwr_start(2022) + dt.timedelta(weeks=39)      # MMWR 2022-W40, Sunday 2 October 2022
CUR_WEEK = mmwr_start(2027) + dt.timedelta(weeks=2)         # MMWR 2027-W03, Sunday 17 January 2027
PREV_WEEK = CUR_WEEK - dt.timedelta(weeks=1)                # MMWR 2027-W02, Sunday 10 January 2027
EXTRACT_LOCAL = dt.datetime(2027, 1, 25, 8, 0)              # the Monday check, 08:00 local
CUTOFF_W2_LOCAL = dt.datetime(2027, 1, 18, 8, 0)            # 08:00 local on the Monday after week 2
BROKER_MIGRATION_LOCAL = dt.datetime(2027, 1, 19, 6, 0)     # the state hub's new broker: receipt times in UTC from here
REPORTS_DUE = dt.date(2027, 1, 27)                          # week-3 aggregate reports due the Wednesday after the week
LINE = 0.80

VIRUSES = ("flu", "rsv", "cov")
VNAME = {"flu": "Influenza", "rsv": "RSV", "cov": "SARS-CoV-2"}
POPS = ("child", "adult", "elder", "rural")

# laboratories: code, name, type, population mix (child, adult, elder, rural), base weekly tests at floor
# positivity by virus, trend a year, accession practice, influenza row grain, facility identifiers
LABS = [
    ("CHH", "Tamsen Children's Hospital Laboratory", "children's hospital", (1, 0, 0, 0),
     {"flu": 1137.5, "rsv": 1057, "cov": 656.25}, 0.02, "panel", "target", ["05D2187341"]),
    ("AH1", "Ellery Memorial Hospital Laboratory", "hospital", (0.03, 0.62, 0.35, 0),
     {"flu": 1531.25, "rsv": 755, "cov": 1662.5}, 0.02, "per_test", "test", ["05D0961572"]),
    ("AH2", "Wexmoor Regional Medical Center Laboratory", "hospital", (0.03, 0.62, 0.35, 0),
     {"flu": 1400.0, "rsv": 704, "cov": 1531.25}, 0.02, "per_test", "test", ["05D1044836"]),
    ("AH3", "Corrigan Valley Hospital Laboratory", "hospital", (0.02, 0.48, 0.50, 0),
     {"flu": 1225.0, "rsv": 654, "cov": 1356.25}, 0.03, "per_test", "test", ["05D0877219", "05D2290465"]),
    ("AH4", "Brandmoor Hospital Laboratory", "hospital", (0.03, 0.62, 0.35, 0),
     {"flu": 1050.0, "rsv": 553, "cov": 1181.25}, 0.01, "per_test", "target", ["05D1530087"]),
    ("CM1", "Bluestem Urgent Care Laboratory", "urgent care", (0.10, 0.80, 0.10, 0),
     {"flu": 1968.75, "rsv": 906, "cov": 2143.75}, 0.03, "per_test", "test", ["05D2341908"]),
    ("CM2", "Ridgeline Clinics Laboratory", "urgent care", (0.10, 0.80, 0.10, 0),
     {"flu": 1881.25, "rsv": 830, "cov": 2012.5}, 0.03, "per_test", "target", ["05D2412776"]),
    ("CM3", "Copperleaf Urgent Care Laboratory", "urgent care", (0.10, 0.80, 0.10, 0),
     {"flu": 1575.0, "rsv": 730, "cov": 1706.25}, 0.02, "per_test", "test", ["05D2508319"]),
    ("LTC", "Arbor Point Laboratory Services", "long-term care", (0, 0, 1, 0),
     {"flu": 831.25, "cov": 2625.0}, 0.00, "panel", "test", ["05D1967450"]),
    ("REF", "Westmarch Reference Laboratory", "reference", (0.08, 0.12, 0.0, 0.80),
     {"flu": 1225.0, "rsv": 654, "cov": 1137.5}, 0.03, "panel", "test", ["05D1189903"]),
]
LAB = {l[0]: l for l in LABS}
LAB_ID = {"CHH": "L01", "AH1": "L02", "AH2": "L03", "AH3": "L04", "AH4": "L05", "CM1": "L06", "CM2": "L07", "CM3": "L08",
          "LTC": "L09", "REF": "L10"}
PREFIX = {"CHH": "TC", "AH1": "EM", "AH2": "WX", "AH3": "CV", "AH4": "BM", "CM1": "BS", "CM2": "RL", "CM3": "CL",
          "LTC": "AP", "REF": "WR"}
STREAMS = [(l[0], v) for l in LABS for v in l[4]]
# each laboratory numbers its accessions in one sequence across all its tests; the respiratory orders of a week take
# numbers from that week's run of the sequence
ACC_BASE = {"CHH": 2_418_300, "AH1": 5_207_100, "AH2": 3_662_400, "AH3": 1_904_700, "AH4": 6_120_900, "CM1": 4_385_200,
            "CM2": 7_031_600, "CM3": 2_976_800, "LTC": 1_250_400, "REF": 5_843_000}
ACC_PER_WEEK = 60_000

# testing response: tests rise with positivity, exp(gamma x (positivity - floor))
FLOOR = {"flu": 0.012, "rsv": 0.010, "cov": 0.030}
GAMMA_DEFAULT = {"flu": 4.2, "rsv": 5.0, "cov": 4.4}
GAMMA = {("LTC", "cov"): 4.6, ("CHH", "rsv"): 5.4, ("CHH", "flu"): 3.4}
NB_SIZE = 8000

# positivity curves: (peak week of season counted from MMWR week 40, peak positivity, width in weeks), seasons 2022-2025
HIST = {
    ("flu", "adult"): [(9, .30, 3.0), (12, .26, 3.4), (13, .32, 3.2), (11, .28, 3.0)],
    ("flu", "child"): [(8, .34, 3.0), (11, .30, 3.4), (12, .34, 3.2), (10, .30, 3.0)],
    ("flu", "elder"): [(10, .22, 3.0), (13, .20, 3.4), (14, .24, 3.2), (12, .22, 3.0)],
    ("flu", "rural"): [(11, .28, 3.0), (14, .24, 3.4), (15, .30, 3.2), (13, .26, 3.0)],
    ("rsv", "child"): [(12, .26, 3.4), (13, .22, 3.6), (12, .24, 3.6), (13, .23, 3.4)],
    ("rsv", "adult"): [(13, .09, 3.6), (14, .08, 3.8), (13, .09, 3.8), (14, .08, 3.6)],
    ("rsv", "elder"): [(13, .11, 3.6), (14, .10, 3.8), (13, .11, 3.8), (14, .10, 3.6)],
    ("rsv", "rural"): [(14, .12, 3.6), (15, .10, 3.8), (14, .11, 3.8), (15, .10, 3.6)],
    ("cov", "adult"): [(15, .23, 3.6), (16, .21, 3.6), (15, .20, 3.6), (16, .21, 3.6)],
    ("cov", "child"): [(15, .11, 3.6), (16, .10, 3.6), (15, .09, 3.6), (16, .09, 3.6)],
    ("cov", "elder"): [(15, .27, 3.6), (16, .25, 3.6), (15, .23, 3.6), (16, .24, 3.6)],
    ("cov", "rural"): [(16, .16, 3.8), (17, .14, 3.8), (17, .12, 3.8), (17, .13, 3.8)],
}
CUR = {
    ("flu", "adult"): (14.8, .37, 2.3), ("flu", "child"): (13.0, .42, 1.8), ("flu", "elder"): (14.1, .30, 2.3),
    ("flu", "rural"): (17.5, .35, 2.35), ("rsv", "child"): (11.3, .28, 2.0), ("rsv", "adult"): (13.7, .09, 2.8),
    ("rsv", "elder"): (12.7, .11, 2.8), ("rsv", "rural"): (17.6, .17, 2.2), ("cov", "adult"): (12.6, .22, 1.7),
    ("cov", "child"): (13.0, .10, 2.6), ("cov", "elder"): (12.9, .31, 1.4), ("cov", "rural"): (15.7, .23, 1.9),
}
# week 3: two laboratories' interfaces losing results all week (unknown to the county)
LOSS = {"AH2": 0.45, "REF": 0.40}
# every interface drops the odd message in any week
BG_LOSS = 0.006
# week 2: Brandmoor's interface lost every result it released from Tuesday morning to Friday morning; escalated on
# Monday 18 January, the laboratory fixed it that week and has still to resend what was lost
OUTAGE_W2 = {"AH4": (dt.datetime(2027, 1, 12, 9, 0), dt.datetime(2027, 1, 15, 9, 0))}
# each laboratory's interface holds results released from Saturday evening and flushes them on Monday morning
HOLD_FROM = {"CHH": 20, "AH1": 21, "AH2": 19, "AH3": 21, "AH4": 18, "CM1": 17, "CM2": 20, "CM3": 19, "LTC": 16, "REF": 15}
# (the hold starts at that hour on Sunday, local time)
FLUSH_AT = {"CHH": (9, 10), "AH1": (8, 30), "AH2": (10, 15), "AH3": (9, 45), "AH4": (11, 0), "CM1": (8, 20),
            "CM2": (12, 10), "CM3": (8, 50), "LTC": (9, 5), "REF": (10, 40)}
# turnaround from collection to release, hours (mean of a gamma), by laboratory
TAT_H = {"CHH": 7, "AH1": 9, "AH2": 10, "AH3": 11, "AH4": 9, "CM1": 20, "CM2": 22, "CM3": 18, "LTC": 26, "REF": 38}
