"""Constants for task268: Corriven Insurance, its five private-car sales regions, the claims system, the people, the
dates and the pack's file names."""
import datetime as dt
import os

SEED = 5
ORG = "Corriven Insurance"
ORG_LTD = "Corriven Insurance Limited"

# code, sales region, the postcode districts it is drawn on for 2025
REGIONS = [
    ("MSY", "Mersey", "L4 L5 L6 L7 L8 L9 L10 L11 L12 L13 L14 L15 L16 L17 L18 L19 L20 L21 L22 L23 L25 L31 L36 CH41 CH42 "
                      "CH43 CH44 CH45 CH46 CH47 CH49 CH60 CH62 CH63 CH64 CH65 CH66 WA1 WA2 WA4 WA5 WA7 WA8 WA9 WA10 "
                      "PR8 PR9"),
    ("PEN", "Pennine", "BD2 BD3 BD4 BD5 BD6 BD7 BD8 BD9 BD10 BD12 BD13 BD15 BD16 BD17 BD18 BD21 BD22 HX1 HX2 HX3 HX4 "
                       "HX6 HX7 HD1 HD2 HD3 HD4 HD5 HD6 HD7 HD8 HD9 OL1 OL2 OL4 OL6 OL8 OL9 OL10 OL11 OL12 OL14 BB1 "
                       "BB2 BB3 BB5 BB9 BB10 BB11 BB12"),
    ("WSX", "Wessex", "SO14 SO15 SO16 SO17 SO18 SO19 SO30 SO31 SO40 SO45 SO50 SO51 SO53 BH1 BH2 BH4 BH5 BH6 BH7 BH8 "
                      "BH9 BH10 BH11 BH12 BH14 BH15 BH17 BH18 BH23 BH25 DT1 DT2 DT3 DT4 DT6 DT11 SP1 SP2 SP4 SP5 SP10 "
                      "SP11 BA11 BA12 BA14"),
    ("FEN", "Fenland", "PE1 PE2 PE3 PE4 PE7 PE13 PE14 PE15 PE16 PE19 PE21 PE25 PE27 PE28 PE29 PE30 PE31 PE33 PE38 CB1 "
                       "CB2 CB4 CB5 CB6 CB7 CB21 CB22 CB23 CB24 NR1 NR2 NR3 NR4 NR5 NR6 NR7 NR8 NR9 NR13 NR14 NR17 "
                       "NR18 NR19 NR20 NR28 NR31 NR32"),
    ("SVN", "Severn", "GL1 GL2 GL3 GL4 GL5 GL6 GL7 GL10 GL11 GL15 GL20 GL50 GL51 GL52 GL53 GL54 WR1 WR2 WR3 WR4 WR5 "
                      "WR9 WR10 WR11 WR14 HR1 HR2 HR4 HR6 HR8 NP10 NP11 NP12 NP15 NP16 NP18 NP19 NP20 NP26 CF3 CF5 "
                      "CF10 CF11 CF14 CF23 CF24 CF62 CF64"),
]
REG = [r[1] for r in REGIONS]
REG_CODE = {r[1]: r[0] for r in REGIONS}
DISTRICTS = {r[1]: r[2].split() for r in REGIONS}
OLD_CODE = {"Mersey": "R2", "Pennine": "R3", "Wessex": "R5", "Fenland": "R1", "Severn": "R4"}  # the old pricing mart

HEADS = ["OD", "TPPD", "TPI", "THEFT", "FIRE", "GLASS"]
HEAD_NAME = {"OD": "Own damage", "TPPD": "Third-party property damage", "TPI": "Third-party injury",
             "THEFT": "Theft", "FIRE": "Fire", "GLASS": "Glass"}
DAMAGE = ("OD", "TPPD", "THEFT", "FIRE", "GLASS")
NOTIFIED_BY = ["Policyholder", "Third party", "Third-party insurer", "Representative"]
ROUTES = ["PH", "TPD", "INS", "SOL", "CMC"]         # the generator's own route of each claim; no file carries it

ACCIDENT_YEARS = range(2019, 2027)
CLOSED = (2019, 2020, 2021, 2022)        # three years after their last day, by 30 September 2026
OPEN_YEAR = 2025
BACKTEST_YEAR = 2022
EXTRACT = dt.date(2026, 9, 30)           # every claim notified to the end of this day, UK time
PULLED = dt.datetime(2026, 10, 1, 6, 12)
MIGRATION = dt.date(2023, 7, 3)          # the new claims system went live; earlier claims were migrated into it
ONLINE_FROM = dt.date(2026, 3, 2)        # the online accident-notification journey opened
LIMITATION_DAYS = 1094
TOLERANCE = 2.0                          # per cent, the reserving standard's back-test

TERMS_DATE = dt.date(2026, 10, 6)
STANDARD_DATE = dt.date(2025, 11, 24)
THREAD_FROM = dt.date(2026, 10, 7)
DECISION_DATE = dt.date(2026, 11, 13)
ORDER_DATE = dt.date(2026, 11, 27)
ASSEMBLED = dt.datetime(2026, 10, 14, 16, 5)

PEOPLE = {"actuary": "Carol Thorpe",          # motor portfolio actuary, the requester
          "cuo": "Damian Warren",             # chief underwriting officer, owns the pilot and decides its regions
          "claims": "Iain Ali"}               # claims director

FILES = {
    "claims": "motor_claims_notified_2019_2026.csv",
    "reps": "claimant_representatives.csv",
    "districts": "postcode_district_sales_regions.csv",
    "exposure": "earned_exposure_2019_2025.xlsx",
    "terms": "telematics_pilot_terms_2027.pdf",
    "standard": "motor_reserving_standard_v4.pdf",
    "thread": "telematics_pilot_thread.txt",
    "inforce": "policy_vehicles_in_force_20260930.csv",
    "changes": "policy_changes_2025_2026.csv",
    "quote": "telematics_supplier_quote_2026.pdf",
    "aggregator": "aggregator_quote_volumes_2025_26.xlsx",
}
DISTRACTORS = ("quote", "aggregator")
GOLDEN = "telematics_pilot_regions_2027.xlsx"
DECK = "telematics_pilot_regions_2027.pptx"
DELIVERABLES = (GOLDEN, DECK)


def bst(t):
    """True when a UTC datetime falls in British Summer Time (last Sunday of March to last Sunday of October, 01:00
    UTC)."""
    def last_sunday(y, m):
        d = dt.date(y, m, 31)
        return d - dt.timedelta(days=(d.weekday() + 1) % 7)
    a = dt.datetime.combine(last_sunday(t.year, 3), dt.time(1))
    b = dt.datetime.combine(last_sunday(t.year, 10), dt.time(1))
    return a <= t < b


def to_utc(t_local):
    u = t_local - dt.timedelta(hours=1)
    return u if bst(u) else t_local


def to_local(t):
    return t + dt.timedelta(hours=1) if bst(t) else t


def _font_dir():
    for d in ("/usr/share/fonts/truetype/liberation/", os.path.expanduser("~/Library/Fonts/"), "/Library/Fonts/"):
        if os.path.exists(os.path.join(d, "LiberationSans-Regular.ttf")):
            return d
    raise FileNotFoundError("LiberationSans-Regular.ttf")


FONT_DIR = _font_dir()
