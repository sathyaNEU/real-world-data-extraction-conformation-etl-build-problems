"""task180 world: Ellesmere Lines, a Canterbury (New Zealand) lines company, and its 44 zone-substation
power transformers.

Every constant the pack is built from lives here. Nothing in the shipped bundle states a figure that
is not derived from these by sim.py and the writers.
"""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 1803
TZ = ZoneInfo("Pacific/Auckland")
UTC = dt.timezone.utc

START = dt.date(2021, 1, 1)            # first SCADA day (counters at 00:00, hourly top oil)
EXTRACT_DATE = dt.date(2026, 10, 16)   # Friday; the pull for the board paper
BOARD_DATE = dt.date(2026, 10, 28)
ORG = "Ellesmere Lines"
LAB = "Waihora Laboratories"

# --------------------------------------------------------------------------------------------
# substations in the sampling route order (two a day on a quarterly round)
SUBSTATIONS = [
    ("LST", "Leeston"), ("SBG", "Southbridge"),
    ("DYL", "Doyleston"), ("DSL", "Dunsandel"),
    ("LIN", "Lincoln"), ("SPN", "Springston"),
    ("LDB", "Ladbrooks"), ("PRB", "Prebbleton"),
    ("RLS", "Rolleston"), ("BNM", "Burnham"),
    ("WDS", "Weedons"), ("WML", "West Melton"),
    ("KRW", "Kirwee"), ("DFD", "Darfield"),
    ("TPR", "Te Pirita"), ("HOR", "Hororata"),
    ("CGT", "Coalgate"), ("GLT", "Glentunnel"),
    ("SHF", "Sheffield"), ("SPF", "Springfield"),
    ("WDN", "Waddington"), ("GDL", "Greendale"),
]
SUB_NAME = dict(SUBSTATIONS)
FOOTHILLS = {"CGT", "GLT", "SHF", "SPF", "WDN", "HOR", "DFD"}   # colder, a little higher

# makers (fictional)
TX_MAKERS = {"BR": "Brannock Electric", "TW": "Tullis & Webb", "MP": "Morvane Power", "HC": "Harcastle"}
OLTC = {  # model: (maker, type as the register writes it)
    "AR-10": ("Ashby Ridley", "In-oil arcing"),
    "AR-14": ("Ashby Ridley", "In-oil arcing"),
    "F-35": ("Fendale", "In-oil arcing"),
    "FV-6": ("Fendale", "Vacuum"),
    "VZ-3": ("Velmora", "Vacuum"),
    "VZ-5": ("Velmora", "Vacuum"),
}

# --------------------------------------------------------------------------------------------
# the fleet. pres: FB free-breathing conservator (silica gel breather), SL sealed (air cell)
# rating: ONAN/ONAF MVA. ops: mean tap operations per day. rs: target relative saturation (%).
# role: normal, L1/L2 (tap-changer barrier weeping), V (vacuum OLTC, internal arc), A3 (in-oil OLTC,
# arcing at the tap selector in the main tank, in step with the operations), T1/T2/T3 (thermal faults
# in oil), and ordinary ageing variants.
FLEET = [
    # id,       maker, year, rewind, rating,      pres, oltc,    oltc_year, ops,  rs,   role
    ("LST-T1", "BR", 1984, None, (7.5, 10.0),   "FB", "AR-10", 1984, 41.0, 22.0, "normal"),
    ("LST-T2", "TW", 1999, None, (7.5, 10.0),   "FB", "F-35",  1999, 0.0,  18.0, "L1"),
    ("SBG-T1", "BR", 1975, None, (7.5, 10.0),   "FB", "AR-10", 1975, 22.0, 26.0, "normal"),
    ("SBG-T2", "MP", 2008, None, (7.5, 10.0),   "FB", "VZ-3",  2008, 0.0,  14.0, "V"),
    ("DYL-T1", "BR", 1973, None, (5.0, 7.5),    "FB", "AR-10", 1973, 18.0, 33.0, "normal"),
    ("DYL-T2", "BR", 1973, None, (5.0, 7.5),    "FB", "AR-10", 1973, 43.0, 24.0, "normal"),
    ("DSL-T1", "BR", 1978, None, (7.5, 10.0),   "FB", "AR-14", 1978, 0.0,  21.0, "L2"),
    ("DSL-T2", "BR", 1978, 2003, (7.5, 10.0),   "FB", "AR-14", 2003, 38.0, 17.0, "normal"),
    ("LIN-T1", "TW", 2001, None, (11.5, 23.0),  "FB", "F-35",  2001, 46.0, 19.0, "normal"),
    ("LIN-T2", "TW", 2001, None, (11.5, 23.0),  "FB", "F-35",  2001, 44.0, 27.5, "normal"),
    ("SPN-T1", "TW", 2002, None, (11.5, 23.0),  "SL", "FV-6",  2002, 30.0, 12.0, "normal"),
    ("SPN-T2", "TW", 2002, None, (11.5, 23.0),  "SL", "FV-6",  2002, 29.0, 11.0, "T2"),
    ("LDB-T1", "BR", 1977, None, (7.5, 10.0),   "FB", "AR-10", 1977, 16.0, 25.0, "code2_CO"),
    ("LDB-T2", "TW", 1994, None, (7.5, 10.0),   "FB", "F-35",  1994, 42.0, 21.0, "normal"),
    ("PRB-T1", "MP", 2012, None, (11.5, 23.0),  "SL", "VZ-5",  2012, 27.0, 9.0,  "normal"),
    ("PRB-T2", "MP", 2012, None, (11.5, 23.0),  "SL", "VZ-5",  2012, 26.0, 10.0, "normal"),
    ("RLS-T1", "MP", 2013, None, (11.5, 23.0),  "SL", "VZ-5",  2013, 33.0, 8.0,  "normal"),
    ("RLS-T2", "TW", 2004, None, (11.5, 23.0),  "SL", "F-35",  2004, 22.0, 13.0, "A3"),
    ("BNM-T1", "MP", 2011, None, (11.5, 23.0),  "SL", "VZ-5",  2011, 31.0, 9.0,  "normal"),
    ("BNM-T2", "MP", 2019, None, (11.5, 23.0),  "SL", "VZ-5",  2019, 30.0, 7.0,  "normal"),
    ("WDS-T1", "TW", 2000, None, (7.5, 10.0),   "SL", "F-35",  2000, 45.0, 15.0, "normal"),
    ("WDS-T2", "MP", 2012, None, (7.5, 10.0),   "SL", "VZ-5",  2012, 30.0, 10.0, "normal"),
    ("WML-T1", "HC", 1983, None, (7.5, 10.0),   "FB", "AR-14", 1983, 24.0, 16.0, "degassed"),
    ("WML-T2", "MP", 2007, None, (7.5, 10.0),   "FB", "VZ-3",  2007, 25.0, 19.0, "normal"),
    ("KRW-T1", "HC", 1990, None, (7.5, 10.0),   "FB", "AR-14", 1990, 47.0, 28.5, "normal"),
    ("KRW-T2", "MP", 2010, None, (7.5, 10.0),   "SL", "VZ-5",  2010, 29.0, 11.0, "normal"),
    ("DFD-T1", "BR", 1981, None, (11.5, 23.0),  "FB", "AR-14", 1981, 23.0, 20.0, "T3"),
    ("DFD-T2", "MP", 2006, None, (11.5, 23.0),  "SL", "VZ-3",  2006, 28.0, 12.0, "normal"),
    ("TPR-T1", "MP", 2005, None, (5.0, 7.5),    "FB", "VZ-3",  2005, 26.0, 18.0, "normal"),
    ("TPR-T2", "HC", 1985, None, (5.0, 7.5),    "FB", "AR-14", 1985, 40.0, 32.0, "normal"),
    ("HOR-T1", "HC", 1988, None, (5.0, 7.5),    "FB", "AR-14", 1988, 43.0, 27.0, "normal"),
    ("HOR-T2", "MP", 2005, None, (5.0, 7.5),    "FB", "VZ-3",  2005, 27.0, 16.0, "normal"),
    ("CGT-T1", "BR", 1972, 1998, (5.0, 7.5),    "FB", "AR-14", 1998, 19.0, 23.0, "T1"),
    ("CGT-T2", "HC", 1986, None, (5.0, 7.5),    "FB", "AR-14", 1986, 44.0, 28.0, "normal"),
    ("GLT-T1", "HC", 1987, None, (5.0, 7.5),    "SL", "AR-14", 1987, 42.0, 20.0, "normal"),
    ("GLT-T2", "BR", 1982, None, (5.0, 7.5),    "SL", "AR-10", 1982, 11.0, 18.0, "code2_C2H6"),
    ("SHF-T1", "BR", 1976, None, (5.0, 7.5),    "FB", "AR-10", 1976, 9.0,  36.0, "normal"),
    ("SHF-T2", "TW", 2003, None, (5.0, 7.5),    "FB", "FV-6",  2003, 24.0, 17.0, "normal"),
    ("SPF-T1", "BR", 1980, None, (5.0, 7.5),    "FB", "AR-10", 1980, 17.0, 31.5, "code2_CO2"),
    ("SPF-T2", "TW", 1993, None, (5.0, 7.5),    "FB", "F-35",  1993, 45.0, 22.0, "normal"),
    ("WDN-T1", "HC", 1989, None, (5.0, 7.5),    "FB", "AR-14", 1989, 21.0, 34.0, "normal"),
    ("WDN-T2", "MP", 2009, None, (5.0, 7.5),    "FB", "VZ-3",  2009, 26.0, 15.0, "normal"),
    ("GDL-T1", "HC", 1991, None, (5.0, 7.5),    "FB", "AR-14", 1991, 20.0, 35.0, "normal"),
    ("GDL-T2", "HC", 1992, None, (5.0, 7.5),    "FB", "VZ-3",  2014, 27.0, 21.0, "normal"),
]
FLEET_COLS = ["id", "maker", "year", "rewind", "rating", "pres", "oltc", "oltc_year", "ops", "rs", "role"]
UNITS = [dict(zip(FLEET_COLS, r)) for r in FLEET]
UNIT = {u["id"]: u for u in UNITS}
IDS = [u["id"] for u in UNITS]
ROLE_UNIT = {u["role"]: u["id"] for u in UNITS if u["role"] in ("L1", "L2", "V", "A3", "T1", "T2", "T3")}
CODE3_UNITS = sorted(ROLE_UNIT.values())        # the main call's row population (naive code 3)
IN_OIL = [u["id"] for u in UNITS if OLTC[u["oltc"]][1] == "In-oil arcing"]
VACUUM = [u["id"] for u in UNITS if OLTC[u["oltc"]][1] == "Vacuum"]
WATCH_LIST = ["LST-T2", "SBG-T2", "DSL-T1", "RLS-T2", "SPN-T2",      # monthly day A (the plains)
              "DFD-T1", "CGT-T1", "GLT-T2", "SHF-T1", "WML-T1"]      # monthly day B (the foothills)

# --------------------------------------------------------------------------------------------
# ES-DGA-02 annex A. Columns: (class, age band) with class SL sealed / FB free-breathing and age
# bands "<10", "10-30", ">30".
GASES = ["H2", "CH4", "C2H6", "C2H4", "C2H2", "CO", "CO2"]
GAS_NAMES = {"H2": "hydrogen", "CH4": "methane", "C2H6": "ethane", "C2H4": "ethylene",
             "C2H2": "acetylene", "CO": "carbon monoxide", "CO2": "carbon dioxide"}
BANDS = ["<10", "10-30", ">30"]
A1 = {  # 90th percentile levels, ppm
    "SL": {"H2": (70, 90, 90), "CH4": (40, 80, 100), "C2H6": (30, 80, 140), "C2H4": (20, 45, 80),
           "C2H2": (1, 1, 2), "CO": (850, 850, 550), "CO2": (5000, 9000, 9500)},
    "FB": {"H2": (35, 40, 40), "CH4": (15, 20, 25), "C2H6": (10, 15, 20), "C2H4": (25, 55, 60),
           "C2H2": (2, 2, 2), "CO": (450, 500, 500), "CO2": (3500, 5500, 6000)},
}
A2 = {  # 95th percentile levels, ppm
    "SL": {"H2": (180, 200, 200), "CH4": (100, 150, 200), "C2H6": (70, 175, 250), "C2H4": (40, 95, 175),
           "C2H2": (2, 2, 4), "CO": (1100, 1100, 900), "CO2": (8000, 14000, 17000)},
    "FB": {"H2": (90, 90, 90), "CH4": (45, 50, 60), "C2H6": (30, 40, 40), "C2H4": (70, 120, 125),
           "C2H2": (5, 6, 7), "CO": (800, 850, 900), "CO2": (7000, 10000, 11000)},
}
A3 = {  # rate limits, twelve-month increase in ppm
    "SL": {"H2": 25, "CH4": 12, "C2H6": 10, "C2H4": 8, "C2H2": 1.0, "CO": 180, "CO2": 2200},
    "FB": {"H2": 12, "CH4": 5, "C2H6": 4, "C2H4": 7, "C2H2": 1.0, "CO": 120, "CO2": 1600},
}
O2N2_SEALED_MAX = 0.2
DETECTION = {"H2": 2, "CH4": 1, "C2H6": 1, "C2H4": 1, "C2H2": 0.5, "CO": 5, "CO2": 10}
BASE_GAP_DAYS = 330
SERVICE_INTERVAL = {"In-oil arcing": (60_000, 7), "Vacuum": (300_000, 10)}
COUNTER_MODULUS = 100_000

# --------------------------------------------------------------------------------------------
# people (guard.py names, en_NZ). The four on the card plus the drawn names used in the pack.
PEOPLE = {
    "requester": "Donna Carson",          # network asset manager
    "engineer": "Barry Forbes",           # zone substation engineer, owner of ES-DGA-02
    "chair": "Wendy Godfrey",             # board chair
    "sampler": "Connor McGill",           # oil sampling technician
    "fitter": "Dennis Trask",             # tap-changer fitter, field services
    "fitter2": "Ethan Mason",             # field services technician
    "data": "Allan Simpson",              # SCADA and data engineer, runs the extract
    "planner": "Aroha O'Brien",           # maintenance planner, mobile substation bookings
    "thermo": "Aimee Craig",              # thermographer, contractor
    "approver": "Emma Elliott",            # general manager, network
}

# --------------------------------------------------------------------------------------------
# NZ public holidays (national, plus Canterbury anniversary) that fall on weekdays, 2019 to 2026
HOLIDAYS = {dt.date.fromisoformat(d) for d in """
2019-01-01 2019-01-02 2019-02-06 2019-04-19 2019-04-22 2019-04-25 2019-06-03 2019-10-28 2019-11-15 2019-12-25 2019-12-26
2020-01-01 2020-01-02 2020-02-06 2020-04-10 2020-04-13 2020-04-27 2020-06-01 2020-10-26 2020-11-13 2020-12-25 2020-12-28
2021-01-01 2021-01-04 2021-02-08 2021-04-02 2021-04-05 2021-04-26 2021-06-07 2021-10-25 2021-11-12 2021-12-27 2021-12-28
2022-01-03 2022-01-04 2022-02-07 2022-04-15 2022-04-18 2022-04-25 2022-06-06 2022-06-24 2022-09-26 2022-10-24 2022-11-11 2022-12-26 2022-12-27
2023-01-02 2023-01-03 2023-02-06 2023-04-07 2023-04-10 2023-04-25 2023-06-05 2023-07-14 2023-10-23 2023-11-17 2023-12-25 2023-12-26
2024-01-01 2024-01-02 2024-02-06 2024-03-29 2024-04-01 2024-04-25 2024-06-03 2024-06-28 2024-10-28 2024-11-15 2024-12-25 2024-12-26
2025-01-01 2025-01-02 2025-02-06 2025-04-18 2025-04-21 2025-04-25 2025-06-02 2025-06-20 2025-10-27 2025-11-14 2025-12-25 2025-12-26
2026-01-01 2026-01-02 2026-02-06 2026-04-03 2026-04-06 2026-04-27 2026-06-01 2026-07-10 2026-10-26 2026-11-13 2026-12-25 2026-12-28
""".split()}


def age_band(u, on=EXTRACT_DATE):
    base = max(u["year"], u["rewind"] or 0)
    age = on.year - base
    return "<10" if age < 10 else ("10-30" if age <= 30 else ">30")


def substation_of(tid):
    return tid.split("-")[0]

# --------------------------------------------------------------------------------------------
# tap-changer services 2019 to 2026 as the maintenance log records them: (date, counter replaced).
# The last entry per unit is its last service. A unit is out of service from about 20:00 the
# evening before a service day to about 07:00 the morning after, so the service day itself
# carries no load operations.
D = dt.date.fromisoformat
OLTC_SERVICES = {
    # in-oil arcing tap changers
    "LST-T1": [(D("2019-06-25"), False), (D("2022-08-16"), False)],
    "LST-T2": [(D("2019-03-26"), False), (D("2023-05-16"), False)],
    "SBG-T1": [(D("2022-10-11"), True)],
    "DYL-T1": [(D("2021-11-09"), False)],
    "DYL-T2": [(D("2021-03-16"), False)],
    "DSL-T1": [(D("2021-05-18"), False)],
    "DSL-T2": [(D("2021-07-20"), False), (D("2025-04-08"), False)],
    "LIN-T1": [(D("2021-10-12"), False), (D("2025-11-04"), True)],
    "LIN-T2": [(D("2022-03-15"), False), (D("2026-03-03"), False)],
    "LDB-T1": [(D("2019-11-12"), False), (D("2023-04-18"), False)],
    "LDB-T2": [(D("2021-08-24"), False), (D("2025-09-02"), True)],
    "RLS-T2": [(D("2023-05-23"), False)],
    "WDS-T1": [(D("2021-05-25"), False), (D("2025-06-24"), False)],
    "WML-T1": [(D("2023-02-21"), False)],
    "KRW-T1": [(D("2022-01-25"), False), (D("2026-05-19"), True)],
    "DFD-T1": [(D("2020-02-18"), False), (D("2024-02-20"), False)],
    "TPR-T2": [(D("2022-05-10"), False)],
    "HOR-T1": [(D("2022-07-12"), False), (D("2026-07-14"), True)],
    "CGT-T1": [(D("2022-10-04"), False)],
    "CGT-T2": [(D("2019-09-10"), False), (D("2023-03-28"), False)],
    "GLT-T1": [(D("2021-11-30"), False)],
    "GLT-T2": [(D("2019-04-09"), False)],
    "SHF-T1": [(D("2019-08-20"), False)],
    "SPF-T1": [(D("2020-05-12"), True), (D("2024-05-14"), False)],
    "SPF-T2": [(D("2021-11-23"), False), (D("2026-02-17"), False)],
    "WDN-T1": [(D("2021-10-19"), True)],
    "GDL-T1": [(D("2019-10-15"), False), (D("2023-11-21"), True)],
    # vacuum tap changers (inspections)
    "SPN-T1": [(D("2020-09-29"), False)],
    "SPN-T2": [(D("2020-09-30"), False)],
    "DFD-T2": [(D("2021-06-29"), False)],
    "TPR-T1": [(D("2022-11-15"), False)],
    "HOR-T2": [(D("2023-08-08"), False)],
    "SHF-T2": [(D("2019-10-22"), False)],
    "GDL-T2": [(D("2024-04-16"), False)],
    "WML-T2": [(D("2024-10-15"), False)],
    "WDN-T2": [(D("2025-03-18"), False)],
}
# last service the register carries where none falls in the log (before 2019)
REGISTER_PRE_LOG_SERVICE = {
    "SBG-T2": D("2018-03-14"), "PRB-T1": D("2012-11-20"), "PRB-T2": D("2012-11-20"),
    "RLS-T1": D("2013-08-06"), "BNM-T1": D("2011-09-27"), "BNM-T2": D("2019-02-12"),
    "WDS-T2": D("2012-06-19"), "KRW-T2": D("2010-10-05"), "TPR-T1": D("2015-11-10"),
    "WDN-T2": D("2018-07-17"), "WML-T2": D("2017-10-24"),
}
# The asset register's last-service field has not been written back from work orders closed since
# the maintenance system upgrade of March 2025; units serviced after that carry the service before.
REGISTER_FROZEN_FROM = D("2025-03-01")

# rollover units: counter reading wanted on the last service day, so the five-digit counter passes
# 99,999 after the service and before the extract
ROLLOVER_AT_SERVICE = {"LST-T1": 56_420, "DYL-T2": 31_877, "TPR-T2": 48_905, "CGT-T2": 61_233,
                       "GLT-T1": 45_118, "WDS-T1": 88_064}

# other work that takes a transformer out of service: (unit, first day out, days out, kind)
OIL_PROCESSING = [("SPF-T2", D("2022-11-08"), 3), ("KRW-T1", D("2024-03-12"), 2),
                  ("WML-T1", D("2025-01-21"), 3)]
BREATHERS = [("SHF-T1", D("2024-07-09")), ("DYL-T1", D("2025-05-13")), ("TPR-T2", D("2023-09-19")),
             ("GDL-T1", D("2026-04-21")), ("WDN-T1", D("2025-08-05")), ("SPF-T1", D("2025-10-07")),
             ("LIN-T2", D("2022-08-23")), ("CGT-T2", D("2024-11-26")), ("HOR-T1", D("2021-04-13")),
             ("KRW-T1", D("2023-07-25")), ("WML-T2", D("2022-05-31")), ("SBG-T1", D("2024-02-27"))]

# laboratory re-issues: (unit, round "YYYY-MM", field corrected, issue-1 value, issue-2 value).
# None for a value means "take the simulated value"; a re-issue on a latest sample moves ask B.
REISSUES = [("SPF-T1", "2026-09", "moisture_ppm", "low", None),
            ("KRW-T1", "2026-09", "oil_temp_c", "transposed", None),
            ("GDL-T2", "2026-09", "oil_temp_c", "blank", None),
            ("LDB-T2", "2024-03", "moisture_ppm", "high", None),
            ("LIN-T1", "2025-12", "oil_temp_c", "blank", None)]

# latest samples (September 2026 round) where the technician left the oil temperature blank
BLANK_TEMP_LATEST = ["SHF-T1", "TPR-T2", "GDL-T1", "LIN-T2", "CGT-T2", "HOR-T1", "DSL-T2",
                     "LDB-T2", "WML-T2", "PRB-T1", "BNM-T1", "SPN-T1", "WDN-T2", "KRW-T2", "DYL-T1"]

# --------------------------------------------------------------------------------------------
# sampling calendar. Quarterly rounds in March, June, September and December run two substations a
# day along the route; the September rounds of 2025 and 2026 are as worked (the 2026 round was
# started a week late and finished after the change to daylight time on 27 September).
ROUTE = [("LST", "SBG"), ("DYL", "DSL"), ("LIN", "SPN"), ("LDB", "PRB"), ("RLS", "BNM"),
         ("WDS", "WML"), ("KRW", "DFD"), ("TPR", "HOR"), ("CGT", "GLT"), ("SHF", "SPF"), ("WDN", "GDL")]
ROUND_AS_WORKED = {
    "2025-09": [("2025-09-08", ("LST", "SBG")), ("2025-09-09", ("DYL", "DSL")), ("2025-09-10", ("LIN", "SPN")),
                ("2025-09-11", ("LDB", "PRB")), ("2025-09-12", ("RLS", "BNM")), ("2025-09-15", ("WDS", "WML")),
                ("2025-09-16", ("KRW", "DFD")), ("2025-09-17", ("TPR", "HOR")), ("2025-09-18", ("CGT", "GLT")),
                ("2025-09-19", ("SHF", "SPF")), ("2025-09-22", ("WDN", "GDL"))],
    "2026-09": [("2026-09-14", ("LST", "SBG")), ("2026-09-15", ("DYL", "DSL")), ("2026-09-16", ("LIN", "SPN")),
                ("2026-09-17", ("LDB", "PRB")), ("2026-09-21", ("RLS", "BNM")), ("2026-09-22", ("WDS", "WML")),
                ("2026-09-23", ("KRW", "WDN")), ("2026-09-24", ("TPR", "HOR")), ("2026-09-28", ("CGT", "GLT")),
                ("2026-09-29", ("DFD", "SHF")), ("2026-09-30", ("SPF", "GDL"))],
}
MONTHLY_2026 = {  # watch-list days outside the round months: (day A, day B)
    1: ("2026-01-13", "2026-01-14"), 2: ("2026-02-10", "2026-02-11"), 4: ("2026-04-14", "2026-04-15"),
    5: ("2026-05-12", "2026-05-13"), 7: ("2026-07-14", "2026-07-15"), 8: ("2026-08-11", "2026-08-12"),
}
LEAK_ONSET = {"DSL-T1": D("2024-07-01"), "LST-T2": D("2025-03-17")}   # barrier began to weep
ARC_ONSET = {"SBG-T2": D("2025-03-31"), "RLS-T2": D("2024-12-16")}    # internal arcing began
THERMAL_ONSET = {"CGT-T1": D("2022-09-26"), "SPN-T2": D("2023-05-29"), "DFD-T1": D("2021-04-19")}
# twelve-month increases the September 2026 results are tuned to (ppm, before scaling to 365 days)
TUNED_INCREASE = {"DSL-T1": ("C2H2", 9.8), "LST-T2": ("C2H2", 8.2), "SBG-T2": ("C2H2", 8.2),
                  "RLS-T2": ("C2H2", 5.1), "CGT-T1": ("C2H4", 34), "SPN-T2": ("C2H4", 36),
                  "DFD-T1": ("C2H4", 25)}
