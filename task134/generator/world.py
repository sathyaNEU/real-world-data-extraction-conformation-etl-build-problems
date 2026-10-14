"""Strathallan Health and Social Care Partnership: the fixed facts of the world.

Days are counted from 1 January 2000 (day 0). Months since admission are days / 30.4375."""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 13494
LON = ZoneInfo("Europe/London")
EPOCH = dt.date(2000, 1, 1)
MONTH = 30.4375


def dn(d):
    return (d - EPOCH).days


def dd(n):
    return EPOCH + dt.timedelta(days=int(n))


def utc_stamp(local):
    return local.replace(tzinfo=LON).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def posix(local):
    return local.replace(tzinfo=LON).timestamp()


SIM_START = dn(dt.date(2006, 1, 1))     # the timeline opens here so the shipped window starts in a steady state
HIST_START = dn(dt.date(2021, 4, 1))    # the shipped history
GOLIVE = dn(dt.date(2023, 7, 3))        # the case system replacement (go-live Monday)
ASOF = dn(dt.date(2026, 12, 31))
EXTRACT = dn(dt.date(2027, 1, 18))
NRS_CUT = dn(dt.date(2027, 1, 15))
QEND = [dn(dt.date(2027, 6, 30)), dn(dt.date(2027, 9, 30)), dn(dt.date(2027, 12, 31)), dn(dt.date(2028, 3, 31))]
QLABEL = ["30 June 2027", "30 September 2027", "31 December 2027", "31 March 2028"]
SIM_END = dn(dt.date(2028, 6, 30))

LOCS = ["Allanvale", "Braeburn", "Carsefield", "Dunmorrow", "Kirkhallam"]
# postcode districts of each locality (the council area sits in the PH and FK postcode areas)
DISTRICTS = {
    "Allanvale": ["FK15", "FK16"],
    "Braeburn": ["PH3", "PH4"],
    "Carsefield": ["FK9", "FK7"],
    "Dunmorrow": ["PH6", "PH5"],
    "Kirkhallam": ["FK17", "FK18"],
}
# share of the partnership's older population by the locality team that serves them
TEAM_W = [0.27, 0.18, 0.21, 0.19, 0.15]

# Care homes in Strathallan: (name, locality, provider, nursing?, registered places, registered date)
HOMES = [
    ("Allanmuir House", "Allanvale", "Holmcare Group Ltd", True, 64, "2004-03-12"),
    ("Ochilbrae Court", "Allanvale", "Ochilbrae Care Ltd", True, 58, "2008-11-03"),
    ("Kippen Rise", "Allanvale", "Caledonia Elder Care Ltd", False, 34, "2002-06-21"),
    ("Westerlea House", "Allanvale", "Westerlea House Trust", False, 28, "2002-04-01"),
    ("Muirhead Nursing Home", "Allanvale", "Holmcare Group Ltd", True, 72, "2011-01-17"),
    ("Allanbank Court", "Allanvale", "Kingsbrae Healthcare Ltd", True, 60, "2014-09-29"),
    ("Pathhead House", "Allanvale", "Pathhead Care Partnership", False, 22, "2002-04-01"),
    ("Fernlea Brae", "Allanvale", "Caledonia Elder Care Ltd", True, 46, "2006-05-15"),
    ("Craigmorrow Brae", "Braeburn", "Craigmorrow Care Ltd", True, 52, "2003-02-10"),
    ("Earnbank Residential Home", "Braeburn", "Earnbank Homes Ltd", False, 30, "2002-04-01"),
    ("Earnside Court", "Braeburn", "Kingsbrae Healthcare Ltd", True, 61, "2009-08-24"),
    ("Ruthbank Towers", "Braeburn", "Ruthbank Care Ltd", False, 26, "2005-10-03"),
    ("Glenmorrow House", "Braeburn", "Holmcare Group Ltd", True, 48, "2012-03-05"),
    ("Kinbrae Care Home", "Braeburn", "Caledonia Elder Care Ltd", False, 32, "2007-07-30"),
    ("Abbeymuir", "Carsefield", "Abbeymuir Care Ltd", True, 70, "2010-06-14"),
    ("Carsehaugh Nursing Home", "Carsefield", "Kingsbrae Healthcare Ltd", True, 66, "2013-02-18"),
    ("Polbeth Court", "Carsefield", "Caledonia Elder Care Ltd", False, 36, "2004-11-22"),
    ("Carsemill House", "Carsefield", "Forthbank Care Homes Ltd", True, 54, "2008-04-07"),
    ("Rapburn Lodge", "Carsefield", "Rapburn Lodge Trust", False, 24, "2002-04-01"),
    ("Fallowfield Care Home", "Carsefield", "Holmcare Group Ltd", True, 50, "2006-09-11"),
    ("Burnside House", "Carsefield", "Forthbank Care Homes Ltd", False, 40, "2005-01-24"),
    ("Larchgrove House", "Carsefield", "Larchgrove Living Ltd", True, 80, "2025-05-19"),
    ("Strathmorrow Nursing Home", "Dunmorrow", "Strathmorrow Care Ltd", True, 62, "2006-12-04"),
    ("Birchwood Brae", "Dunmorrow", "Holmcare Group Ltd", True, 56, "2011-10-10"),
    ("Taybank Lodge", "Dunmorrow", "Taybank Care Ltd", False, 30, "2003-08-18"),
    ("Dunmorrow House Care Home", "Dunmorrow", "Kingsbrae Healthcare Ltd", True, 64, "2015-04-20"),
    ("Morrow Grange", "Dunmorrow", "Caledonia Elder Care Ltd", False, 28, "2002-04-01"),
    ("Millbank House", "Dunmorrow", "Millbank Care Ltd", True, 44, "2009-02-23"),
    ("Inverbrae Court", "Dunmorrow", "Holmcare Group Ltd", False, 34, "2007-05-28"),
    ("Hallam House Nursing Home", "Kirkhallam", "Kingsbrae Healthcare Ltd", True, 58, "2010-01-11"),
    ("Lenmuir Lodge", "Kirkhallam", "Caledonia Elder Care Ltd", False, 26, "2004-06-14"),
    ("Kirkhallam Court", "Kirkhallam", "Holmcare Group Ltd", True, 52, "2012-11-26"),
    ("Venlaw House", "Kirkhallam", "Venlaw Care Ltd", False, 22, "2002-04-01"),
    ("Pinewell Lodge", "Kirkhallam", "Pinewell Care Homes Ltd", True, 72, "2025-08-25"),
    ("Strathmuir House", "Kirkhallam", "Strathmuir House Trust", False, 20, "2003-09-08"),
    ("Castle Brae", "Kirkhallam", "Caledonia Elder Care Ltd", True, 40, "2008-03-31"),
    ("Thornbank House", "Kirkhallam", "Thornbank Care Ltd", False, 24, "2005-12-12"),
]
# re-registrations on a change of provider in 2026: (home, new provider, date of the new registration)
REREG = {
    "Craigmorrow Brae": ("Ashmuir Care Group Ltd", dn(dt.date(2026, 3, 2))),
    "Strathmorrow Nursing Home": ("Ashmuir Care Group Ltd", dn(dt.date(2026, 8, 3))),
}
NEW_HOMES = {"Larchgrove House": dn(dt.date(2025, 6, 2)), "Pinewell Lodge": dn(dt.date(2025, 9, 15))}

# homes outside Strathallan used for council-funded placements (name, council, nursing?)
OOA_HOMES = [
    ("Wallacebank Lodge", "Stirling", True), ("Forthmuir Lodge", "Falkirk", True),
    ("Zetbank House", "Falkirk", False), ("Sconebank House", "Perth and Kinross", True),
    ("Earnhill Court", "Perth and Kinross", False), ("Inchmore House", "Clackmannanshire", True),
    ("Devonbrae Lodge", "Clackmannanshire", False), ("Endrick Grange", "Stirling", True),
    ("Lochmorrow House", "Perth and Kinross", True), ("Hillfoots House", "Clackmannanshire", False),
    ("Carronlea Court", "Falkirk", True), ("Ledbrae Lodge", "Stirling", False),
]

# National Care Home Contract weekly rates by financial year (residential, nursing), GBP
NCHC = {
    2016: (558.20, 646.98), 2017: (577.22, 669.04), 2018: (602.55, 698.38), 2019: (623.60, 722.82),
    2020: (650.96, 754.53), 2021: (712.79, 815.17), 2022: (764.75, 868.48), 2023: (825.12, 932.05),
    2024: (873.56, 984.43), 2025: (911.22, 1028.63), 2026: (948.72, 1071.04),
}
for y in range(2005, 2016):
    NCHC[y] = tuple(round(v * (0.966 ** (2016 - y)), 2) for v in NCHC[2016])
NCHC_DRAFT_2027 = (996.15, 1124.59)
# free personal care and free nursing care weekly payments by financial year (personal, nursing)
FPNC = {2021: (193.50, 87.10), 2022: (212.85, 95.80), 2023: (233.65, 105.15), 2024: (248.70, 112.10),
        2025: (254.20, 114.75), 2026: (262.35, 118.40)}
for y in range(2006, 2021):
    FPNC[y] = tuple(round(v * (0.975 ** (2021 - y)), 2) for v in FPNC[2021])
# the national capital limits (lower, upper) by the financial year they apply from: frozen from April 2019, then raised
# in two stages, on the first Monday in April 2026 and 2027
CAPITAL = {y: (18000, 28750) for y in range(2005, 2026)}
CAPITAL[2026] = (21000, 33750)
CAPITAL[2027] = (25000, 40750)
PEA = {2021: 30.15, 2022: 31.25, 2023: 33.35, 2024: 35.20, 2025: 36.40, 2026: 37.45}
# the 2026-27 National Care Home Contract rate was agreed on 6 November 2026, backdated to 1 April 2026; until then
# placements were paid at an interim uplift of 1.5 per cent on the 2025-26 rates, and the case system's fees still
# carry the interim rate at the extract (its uprating run for the agreed rate had not been made)
NCHC_INTERIM_2026 = tuple(round(v * 1.015, 2) for v in NCHC[2025])
NCHC_AGREED_DAY = dn(dt.date(2026, 11, 6))


def fy(day):
    d = dd(day)
    return d.year if d.month >= 4 else d.year - 1


def fy_start(y):
    return dn(dt.date(y, 4, 1))


# hazards per month by months since admission
def death_mult(mo):
    return 1.3 if mo < 3 else 1.15 if mo < 6 else 1.0 if mo < 12 else 0.97


DEATH_BASE = 0.0290
NURSING_DEATH = 1.07
DISCH = 0.0015
CONV = [(15, 0.0002), (18, 0.030), (24, 0.052), (36, 0.050), (48, 0.030), (10 ** 6, 0.012)]



def uprate_day(y):
    """the first Monday in April of year y: the day the national capital limits change"""
    d = dt.date(y, 4, 1)
    while d.weekday() != 0:
        d += dt.timedelta(days=1)
    return dn(d)


STAGE1 = uprate_day(2026)      # 6 April 2026
STAGE2 = uprate_day(2027)      # 5 April 2027
# self-funders' weekly fees at 2026-27 prices (residential, nursing) before the home's own level, rising 4.5 per cent a
# year; the partnership never holds them (a self-funder's fee is agreed with the home)
SF_FEE_2026 = (1180.0, 1420.0)
SF_FEE_GROWTH = 1.045

PEOPLE = {
    "cfo": "Richard Lynch", "commissioning": "Martyn Rogers", "analyst": "Hollie Todd",
    "finance": "Ruth Wong", "contracts": "Joseph Morris", "chair": "Margaret Booth",
}
ORG = "Strathallan Council"
