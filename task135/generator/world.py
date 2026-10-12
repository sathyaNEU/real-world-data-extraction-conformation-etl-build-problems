"""Fixed facts of the Wrexford Trust world: calendars, holdings, policy, the mandate's securities, the grants world."""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 1352                            # world seed (books, grants); the market seed is MARKET_SEED
MARKET_SEED = 2109                     # chosen by tune.py (see the design note's Build record)
LON = ZoneInfo("Europe/London")
NYC = ZoneInfo("America/New_York")
TYO = ZoneInfo("Asia/Tokyo")

SIM_START = dt.date(2023, 9, 1)        # the market model runs from here (the factsheets' three years need it)
WIN_START = dt.date(2024, 11, 29)      # first valuation in the export (the last business day of November 2024)
VAL_DATE = dt.date(2026, 11, 30)       # the last month-end valuation before the December meeting
EXPORT_RUN = dt.datetime(2026, 12, 2, 6, 41, 12)
MEETING = dt.date(2026, 12, 10)
BUDGET_DATE = dt.date(2026, 11, 24)
INC_FROM = dt.date(2025, 12, 1)        # procedure 7.2's twelve months
REPORT_FROM = dt.date(2025, 11, 1)     # the entitlements report's run (thirteen months)
EUR_RATE = 1.1460                      # procedure 7.5

# ------------------------------------------------------------------------------------------------ calendars
UK_HOL = {
    "2023-12-25": "Christmas Day", "2023-12-26": "Boxing Day", "2024-01-01": "New Year's Day",
    "2024-03-29": "Good Friday", "2024-04-01": "Easter Monday", "2024-05-06": "Early May bank holiday",
    "2024-05-27": "Spring bank holiday", "2024-08-26": "Summer bank holiday",
    "2024-12-25": "Christmas Day", "2024-12-26": "Boxing Day", "2025-01-01": "New Year's Day",
    "2025-04-18": "Good Friday", "2025-04-21": "Easter Monday", "2025-05-05": "Early May bank holiday",
    "2025-05-26": "Spring bank holiday", "2025-08-25": "Summer bank holiday", "2025-12-25": "Christmas Day",
    "2025-12-26": "Boxing Day", "2026-01-01": "New Year's Day", "2026-04-03": "Good Friday",
    "2026-04-06": "Easter Monday", "2026-05-04": "Early May bank holiday", "2026-05-25": "Spring bank holiday",
    "2026-08-31": "Summer bank holiday", "2026-12-25": "Christmas Day", "2026-12-28": "Boxing Day (substitute day)",
    "2027-01-01": "New Year's Day", "2027-03-26": "Good Friday", "2027-03-29": "Easter Monday",
    "2027-05-03": "Early May bank holiday", "2027-05-31": "Spring bank holiday", "2027-08-30": "Summer bank holiday",
    "2027-12-27": "Christmas Day (substitute day)", "2027-12-28": "Boxing Day (substitute day)",
}
US_HOL = {
    "2023-09-04": "Labor Day", "2023-11-23": "Thanksgiving Day", "2023-12-25": "Christmas Day",
    "2024-01-01": "New Year's Day", "2024-01-15": "Martin Luther King Jr. Day", "2024-02-19": "Washington's Birthday",
    "2024-03-29": "Good Friday", "2024-05-27": "Memorial Day", "2024-06-19": "Juneteenth National Independence Day",
    "2024-07-04": "Independence Day", "2024-09-02": "Labor Day", "2024-11-28": "Thanksgiving Day",
    "2024-12-25": "Christmas Day", "2025-01-01": "New Year's Day", "2025-01-09": "National Day of Mourning",
    "2025-01-20": "Martin Luther King Jr. Day", "2025-02-17": "Washington's Birthday", "2025-04-18": "Good Friday",
    "2025-05-26": "Memorial Day", "2025-06-19": "Juneteenth National Independence Day", "2025-07-04": "Independence Day",
    "2025-09-01": "Labor Day", "2025-11-27": "Thanksgiving Day", "2025-12-25": "Christmas Day",
    "2026-01-01": "New Year's Day", "2026-01-19": "Martin Luther King Jr. Day", "2026-02-16": "Washington's Birthday",
    "2026-04-03": "Good Friday", "2026-05-25": "Memorial Day", "2026-06-19": "Juneteenth National Independence Day",
    "2026-07-03": "Independence Day (observed)", "2026-09-07": "Labor Day", "2026-11-26": "Thanksgiving Day",
    "2026-12-25": "Christmas Day", "2027-01-01": "New Year's Day", "2027-01-18": "Martin Luther King Jr. Day",
    "2027-02-15": "Washington's Birthday", "2027-03-26": "Good Friday", "2027-05-31": "Memorial Day",
    "2027-06-18": "Juneteenth National Independence Day (observed)", "2027-07-05": "Independence Day (observed)",
    "2027-09-06": "Labor Day", "2027-11-25": "Thanksgiving Day", "2027-12-24": "Christmas Day (observed)",
}
JP_HOL = {
    "2023-09-18": "Respect for the Aged Day", "2023-10-09": "Sports Day", "2023-11-03": "Culture Day",
    "2023-11-23": "Labour Thanksgiving Day", "2023-12-29": "Exchange holiday", "2024-01-01": "New Year's Day",
    "2024-01-02": "Exchange holiday", "2024-01-03": "Exchange holiday", "2024-01-08": "Coming of Age Day",
    "2024-02-12": "National Foundation Day (observed)", "2024-02-23": "Emperor's Birthday",
    "2024-03-20": "Vernal Equinox Day", "2024-04-29": "Showa Day", "2024-05-03": "Constitution Memorial Day",
    "2024-05-06": "Children's Day (observed)", "2024-07-15": "Marine Day", "2024-08-12": "Mountain Day (observed)",
    "2024-09-16": "Respect for the Aged Day", "2024-09-23": "Autumnal Equinox Day (observed)",
    "2024-10-14": "Sports Day", "2024-11-04": "Culture Day (observed)", "2024-12-31": "Exchange holiday",
    "2025-01-01": "New Year's Day", "2025-01-02": "Exchange holiday", "2025-01-03": "Exchange holiday",
    "2025-01-13": "Coming of Age Day", "2025-02-11": "National Foundation Day", "2025-02-24": "Emperor's Birthday (observed)",
    "2025-03-20": "Vernal Equinox Day", "2025-04-29": "Showa Day", "2025-05-05": "Children's Day",
    "2025-05-06": "Greenery Day (observed)", "2025-07-21": "Marine Day", "2025-08-11": "Mountain Day",
    "2025-09-15": "Respect for the Aged Day", "2025-09-23": "Autumnal Equinox Day", "2025-10-13": "Sports Day",
    "2025-11-03": "Culture Day", "2025-11-24": "Labour Thanksgiving Day (observed)", "2025-12-31": "Exchange holiday",
    "2026-01-01": "New Year's Day", "2026-01-02": "Exchange holiday", "2026-01-12": "Coming of Age Day",
    "2026-02-11": "National Foundation Day", "2026-02-23": "Emperor's Birthday", "2026-03-20": "Vernal Equinox Day",
    "2026-04-29": "Showa Day", "2026-05-04": "Greenery Day", "2026-05-05": "Children's Day",
    "2026-05-06": "Constitution Memorial Day (observed)", "2026-07-20": "Marine Day", "2026-08-11": "Mountain Day",
    "2026-09-21": "Respect for the Aged Day", "2026-09-22": "Citizens' Holiday", "2026-09-23": "Autumnal Equinox Day",
    "2026-10-12": "Sports Day", "2026-11-03": "Culture Day", "2026-11-23": "Labour Thanksgiving Day",
    "2026-12-31": "Exchange holiday", "2027-01-01": "New Year's Day", "2027-01-11": "Coming of Age Day",
    "2027-02-11": "National Foundation Day", "2027-02-23": "Emperor's Birthday", "2027-03-22": "Vernal Equinox Day (observed)",
    "2027-04-29": "Showa Day", "2027-05-03": "Constitution Memorial Day", "2027-05-04": "Greenery Day",
    "2027-05-05": "Children's Day", "2027-07-19": "Marine Day", "2027-08-11": "Mountain Day",
    "2027-09-20": "Respect for the Aged Day", "2027-09-23": "Autumnal Equinox Day", "2027-10-11": "Sports Day",
    "2027-11-03": "Culture Day", "2027-11-23": "Labour Thanksgiving Day", "2027-12-31": "Exchange holiday",
}
HOL = {"UK": UK_HOL, "US": US_HOL, "JP": JP_HOL}


def is_bday(d, mkt):
    return d.weekday() < 5 and d.isoformat() not in HOL[mkt]


def bdays(a, b, mkt="UK"):
    out, d = [], a
    while d <= b:
        if is_bday(d, mkt):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def add_bdays(d, n, mkt="UK"):
    k = 0
    while k < n:
        d += dt.timedelta(days=1)
        if is_bday(d, mkt):
            k += 1
    return d


def utc_stamp(local):
    """a London wall-clock datetime as the UTC instant Office stores"""
    return local.replace(tzinfo=LON).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def posix(local):
    return local.replace(tzinfo=LON).timestamp()


# ------------------------------------------------------------------------------------------------ holdings
HOLDINGS = ["MAND", "NAEF", "EUEF", "JPEF", "GILT", "CORP"]
GROWTH = {"MAND": 0.40, "NAEF": 0.30, "EUEF": 0.15, "JPEF": 0.15}
DEFENSIVE = {"GILT": 0.55, "CORP": 0.45}
STEPS = [20, 30, 40, 50, 60, 70, 80, 90, 100]
SHARE_2026 = 80
CAP = 10.0


def weights(step):
    s = step / 100.0
    w = {k: v * s for k, v in GROWTH.items()}
    w.update({k: v * (1 - s) for k, v in DEFENSIVE.items()})
    return w


# the five Kestwick funds: code, name, ISIN (income units, accumulation units), distribution months, launch
FUNDS = {
    "NAEF": dict(name="Kestwick North American Equity Fund for Charities", short="North American Equity",
                 isin_inc="GB00BKW4NA16", isin_acc="GB00BKW4NB23", months=(3, 9), sedol="BKW4NA1"),
    "EUEF": dict(name="Kestwick European Equity Fund for Charities", short="European Equity",
                 isin_inc="GB00BKW4EU21", isin_acc="GB00BKW4EV38", months=(4, 10), sedol="BKW4EU2"),
    "JPEF": dict(name="Kestwick Japan Equity Fund for Charities", short="Japan Equity",
                 isin_inc="GB00BKW4JP56", isin_acc="GB00BKW4JQ63", months=(5, 11), sedol="BKW4JP5"),
    "GILT": dict(name="Kestwick Gilt Fund for Charities", short="Gilt",
                 isin_inc="GB00BKW4GL79", isin_acc="GB00BKW4GM86", months=(2, 5, 8, 11), sedol="BKW4GL7"),
    "CORP": dict(name="Kestwick Sterling Corporate Bond Fund for Charities", short="Sterling Corporate Bond",
                 isin_inc="GB00BKW4SC92", isin_acc="GB00BKW4SD00", months=(2, 5, 8, 11), sedol="BKW4SC9"),
}
FUND_YIELD = {"NAEF": 0.0098, "EUEF": 0.0262, "JPEF": 0.0207, "GILT": 0.0431, "CORP": 0.0538}

SUB_ACCOUNTS = {"WRX-PE01": "Permanent endowment", "WRX-EX02": "Expendable endowment"}
SUB_UNIT = {"WRX-PE01": "inc", "WRX-EX02": "acc"}     # the unit type each designation holds in the Kestwick funds
SUB_SHARE = {"WRX-PE01": 0.61, "WRX-EX02": 0.39}

# ------------------------------------------------------------------------------------------------ the mandate
# code, name, sector, beta, idiosyncratic daily vol, start price (GBP), dividend yield, payment months, REIT
STOCKS = [
    ("BF100231", "Ashgrove Industrial plc", "Industrials", 1.05, 0.0130, 7.84, 0.031, (4, 10), False),
    ("BF100248", "Carrick Water Group plc", "Utilities", 0.62, 0.0105, 11.92, 0.048, (1, 7), False),
    ("BF100255", "Dunmore Mining plc", "Basic Materials", 1.32, 0.0185, 24.65, 0.052, (3, 9), False),
    ("BF100262", "Elsworth Insurance plc", "Financials", 0.94, 0.0120, 6.115, 0.058, (5, 11), False),
    ("BF100279", "Fenwick Pharmaceuticals plc", "Health Care", 0.71, 0.0115, 42.30, 0.029, (3, 8), False),
    ("BF100286", "Garrow Banking Group plc", "Financials", 1.21, 0.0150, 3.882, 0.061, (4, 9), False),
    ("BF100293", "Hollins Brewery plc", "Consumer Staples", 0.66, 0.0110, 28.40, 0.033, (2, 8), False),
    ("BF100309", "Inchmore Telecom plc", "Telecommunications", 0.83, 0.0125, 1.264, 0.064, (6, 12), False),
    ("BF100316", "Jessop Defence plc", "Industrials", 0.88, 0.0130, 13.58, 0.022, (5, 11), False),
    ("BF100323", "Kelham Energy plc", "Energy", 1.15, 0.0160, 4.716, 0.055, (3, 6, 9, 12), False),
    ("BF100330", "Larkfield Housebuilders plc", "Consumer Discretionary", 1.28, 0.0170, 9.36, 0.047, (4, 10), False),
    ("BF100347", "Marlow Software plc", "Technology", 1.10, 0.0145, 15.72, 0.012, (6, 12), False),
    ("BF100354", "Netherby Foods plc", "Consumer Staples", 0.58, 0.0100, 18.05, 0.036, (1, 7), False),
    ("BF100361", "Oakhurst Logistics plc", "Industrials", 1.07, 0.0140, 5.48, 0.034, (5, 11), False),
    ("BF100378", "Penrose Media plc", "Consumer Discretionary", 0.97, 0.0150, 8.23, 0.041, (4, 9), False),
    ("BF100385", "Quayside Property REIT plc", "Real Estate", 0.79, 0.0115, 0.987, 0.062, (1, 4, 7, 10), True),
    ("BF100392", "Ravensworth Chemicals plc", "Basic Materials", 1.12, 0.0145, 21.40, 0.038, (3, 9), False),
    ("BF100408", "Sandown Asset Management plc", "Financials", 1.25, 0.0160, 2.315, 0.067, (2, 8), False),
    ("BF100415", "Thornbury Engineering plc", "Industrials", 1.03, 0.0130, 36.80, 0.026, (5, 11), False),
    ("BF100422", "Ullswater Retail plc", "Consumer Discretionary", 0.95, 0.0140, 2.982, 0.044, (6, 12), False),
    ("BF100439", "Vardon Healthcare plc", "Health Care", 0.69, 0.0115, 12.66, 0.024, (4, 10), False),
    ("BF100446", "Westbury Power plc", "Utilities", 0.60, 0.0100, 10.38, 0.053, (1, 7), False),
    ("BF100453", "Yarrowby Distribution plc", "Industrials", 0.92, 0.0130, 4.054, 0.039, (3, 9), False),
    ("BF100460", "Abernant Life plc", "Financials", 1.08, 0.0135, 5.672, 0.071, (5, 10), False),
    ("BF100477", "Brockley Storage REIT plc", "Real Estate", 0.74, 0.0115, 1.415, 0.049, (2, 5, 8, 11), True),
    ("BF100484", "Coldharbour Tobacco plc", "Consumer Staples", 0.54, 0.0105, 30.15, 0.069, (2, 8), False),
    ("BF100491", "Dalesford Packaging plc", "Industrials", 0.99, 0.0135, 3.416, 0.043, (5, 11), False),
    ("BF100507", "Eastgate Broadcasting plc", "Consumer Discretionary", 1.02, 0.0155, 1.873, 0.037, (4, 10), False),
    ("BF100514", "Furness Shipping plc", "Industrials", 1.14, 0.0165, 6.94, 0.050, (3, 9), False),
    ("BF100521", "Glenrothes Distillers plc", "Consumer Staples", 0.77, 0.0115, 25.72, 0.027, (6, 12), False),
    ("BF100538", "Hartwell Engineering Services plc", "Industrials", 1.06, 0.0140, 2.648, 0.035, (5, 11), False),
    ("BF100545", "Ivybridge Specialty Insurance plc", "Financials", 0.86, 0.0125, 8.91, 0.046, (4, 9), False),
]
# the demerged company (shares credited the business day after the parent goes ex)
DEMERGED = ("BF100552", "Larkfield Land plc", "Real Estate", 1.10, 0.0160, None, 0.030, (5, 11), False)

# corporate events: (event_ref, security, action, ex/effective date, terms)
CONSOLIDATION = ("CA250412", "BF100309", dt.date(2025, 6, 16), 8)                # 1 new for every 8 held
DEMERGER = ("CA250731", "BF100330", dt.date(2025, 9, 22), 5, 0.165)              # 1 new for 5 held; 16.5 per cent of value
RIGHTS = ("CA260118", "BF100286", dt.date(2026, 3, 9), dt.date(2026, 3, 30), 4, 0.72)   # 1 for 4 at 72 per cent of price
TAKEOVER = ("CA260244", "BF100521", dt.date(2026, 5, 11), dt.date(2026, 7, 21), 1.31)   # announced, effective; cash at a 31 per cent premium

# external flows into and out of the mandate (beyond the quarter-end rebalancing, which the book computes)
LEGACY = (dt.date(2025, 5, 14), "WRX-PE01", 5_846_310.42, "Legacy: estate of the late Mrs E. M. Rushworth")

# ------------------------------------------------------------------------------------------------ grants
PROGRAMMES = {"CORE": "Core funding", "PROJ": "Project grants"}
RUNNING_COSTS = [  # the budget workbook's running costs lines (2027 draft), pounds
    ("Staff salaries", 187_420), ("Employer's National Insurance", 21_655), ("Pension contributions", 14_996),
    ("Office rent and service charge", 38_250), ("Utilities and insurance", 7_912), ("IT and grants system licence", 16_384),
    ("Audit and independent examination", 14_700), ("Legal and professional fees", 9_350),
    ("Trustee meetings and expenses", 4_418), ("Grantee visits and learning", 6_275),
    ("Annual review and communications", 3_840), ("Bank charges", 1_126), ("Sundry", 2_177),
]
CAPITAL_CHARGES = [("Investment management fee (Fernside Partners)", 61_750), ("Custody fees (Brackenfold Custody)", 18_420)]

# ------------------------------------------------------------------------------------------------ the chosen world
# (scan.py / tune.py and tune_asks.py; the design note's Build record carries the measured ladder for these)
START_TOTAL = 37_351_806.0
BOOK_KNOBS = {}
GRANT_SEED, GRANT_SCALE = 117, 1.2
RUNNING_ADJ = 0
