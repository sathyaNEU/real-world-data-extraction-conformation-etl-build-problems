"""task463 world: Statistics Kellesay's retail prices index, the sixteen grocery and household items it plans to move to
the three supermarkets' transaction data, and the parallel year September 2025 to September 2026. Every name and
number the generator shares sits here."""
import datetime as dt

SEED = 463
STREAM = 73463                      # the world's random stream
COVER_OFFSET = 310                    # the coverage files' stream, set by calibrate.py
NUDGE = {"1101": 6, "1103": 57, "1105": 46, "1108": 1, "1145": 3, "1146": 11, "1182": 9, "1211": 2, "1221": 2, "1222": 3, "1223": 1, "5611": 3, "5613": 3}
ISLAND = "Kellesay"
ORG = "Statistics Kellesay"
GST = 0.05
LINE = 1.5                          # points: the plan's agreement test
NOTICE = dt.date(2026, 11, 13)      # the Statistics Code's two months' notice before the January 2027 index
PACK_DATE = dt.date(2026, 10, 21)   # the folder as the prices team assembled it

# the parallel year: the months the plan's 12-month rate runs over (index 0 = September 2025)
MONTHS = [(2025, 9), (2025, 10), (2025, 11), (2025, 12), (2026, 1), (2026, 2), (2026, 3), (2026, 4), (2026, 5),
          (2026, 6), (2026, 7), (2026, 8), (2026, 9)]
NM = len(MONTHS)
MONTH_NAME = ["September 2025", "October 2025", "November 2025", "December 2025", "January 2026", "February 2026",
              "March 2026", "April 2026", "May 2026", "June 2026", "July 2026", "August 2026", "September 2026"]
# the supermarkets run their monthly offers from November to July; August to October, the visitor season and its
# tail, carry none
OFFER_FREE = {0, 1, 11, 12}

RETAILERS = ["W", "G", "C"]
RNAME = {"W": "Wrenfold Stores", "G": "Gorsedale Co-operative", "C": "Calderby's"}
RSHORT = {"W": "Wrenfold", "G": "Gorsedale", "C": "Calderby's"}
# the retailers' own GS1 company prefixes for their own-label lines
OWN_PREFIX = {"W": "5060417", "G": "5060582", "C": "5061093"}
MEMBER_START = 6                    # Wrenfold Rewards member prices from March 2026
MEMBER_ITEMS = {"1146", "1182"}

# code, name, stock-up dip after an offer month, share of months a line is on offer, offer depth range,
# regular price trend over the year, own-label extra trend (own lines +, brands -), price level (GBP), lines W/G/C
ITEMS = [
    ("1101", "Bread", 0.00, 0.06, (0.15, 0.25), 0.034, 0.000, 1.45, (30, 22, 18)),
    ("1103", "Breakfast cereals", 0.40, 0.24, (0.20, 0.32), 0.030, 0.000, 2.85, (38, 28, 22)),
    ("1105", "Pasta and rice", 0.20, 0.08, (0.20, 0.30), 0.025, 0.100, 1.65, (32, 24, 20)),
    ("1108", "Biscuits", 0.35, 0.24, (0.20, 0.32), 0.036, 0.000, 1.55, (40, 30, 24)),
    ("1145", "Yoghurt", 0.00, 0.22, (0.20, 0.30), 0.031, 0.000, 1.35, (34, 24, 20)),
    ("1146", "Cheese", 0.00, 0.16, (0.20, 0.30), 0.036, 0.000, 3.10, (30, 22, 18)),
    ("1151", "Butter and spreads", 0.00, 0.14, (0.20, 0.30), 0.024, 0.000, 2.40, (22, 16, 14)),
    ("1182", "Chocolate and sweets", 0.30, 0.24, (0.20, 0.32), 0.044, 0.000, 1.45, (44, 32, 26)),
    ("1211", "Coffee", 0.42, 0.24, (0.20, 0.32), 0.052, 0.000, 4.60, (30, 22, 18)),
    ("1212", "Tea", 0.40, 0.20, (0.20, 0.30), 0.027, 0.000, 2.95, (24, 18, 14)),
    ("1221", "Soft drinks", 0.42, 0.26, (0.22, 0.34), 0.041, 0.000, 1.70, (42, 30, 26)),
    ("1222", "Bottled water", 0.40, 0.22, (0.20, 0.32), 0.022, 0.000, 1.15, (18, 14, 12)),
    ("1223", "Fruit juice", 0.00, 0.20, (0.20, 0.30), 0.029, 0.000, 1.85, (24, 18, 14)),
    ("5611", "Laundry products", 0.45, 0.26, (0.22, 0.35), 0.026, 0.000, 5.40, (28, 20, 16)),
    ("5613", "Toilet and kitchen rolls", 0.45, 0.26, (0.22, 0.34), 0.031, 0.000, 3.60, (20, 16, 12)),
    ("6213", "Toiletries", 0.40, 0.24, (0.20, 0.32), 0.030, 0.000, 2.75, (46, 34, 26)),
]
ICODE = [i[0] for i in ITEMS]
INAME = {i[0]: i[1] for i in ITEMS}

PEOPLE = {"prices": "Diana Lawson"}
TITLE = {"prices": "Transaction Data Programme Manager"}

FILES = {
    "wrenfold": "wrenfold_weekly_item_sales_2025_2026.csv",
    "gorsedale": "gorsedale_period_sales_fy2026_fy2027.txt",
    "calendar": "gorsedale_fiscal_calendar_fy2026_fy2027.csv",
    "calderby": "calderby_pos_daily_2025_2026.sqlite",
    "classes": "statistics_kellesay_product_classification.csv",
    "published": "kellesay_rpi_item_indices_2024_2026.xlsx",
    "plan": "rpi_transaction_data_introduction_plan_2026.pdf",
    "dict": "transaction_data_dictionary.xlsx",
    "deliveries": "retailer_delivery_log_2025_2026.csv",
    "quotes": "rpi_field_quotes_2025_2026.csv",
    "returns": "retailer_annual_returns_2025.xlsx",
    "catmap": "retailer_category_map.csv",
    "spending": "household_spending_estimates_2025.xlsx",
    "rsi": "kellesay_retail_sales_index_2025_2026.xlsx",
    "manifest": "transaction_data_folder_register.csv",
}
DISTRACTORS = ["quotes", "rsi"]
DEADLINE_DAYS = 8                   # the plan: a month's records due by the end of the eighth day after it
CALDERBY_STORES = [(1, "Calderby's Westgate", 0.45), (2, "Calderby's Ferry Lane", 0.33), (3, "Calderby's Gullhaven", 0.22)]
GOLDEN = {"workbook": "kellesay_rpi_transaction_readiness_2027.xlsx",
          "products": "kellesay_transaction_product_months_2025_2026.csv",
          "chart": "kellesay_item_indices_parallel_year.png"}


def month_of(d):
    """The plan's month for a day (a calendar day) or a retailer week (the month in which the week ends)."""
    return (d.year, d.month)


def month_index(d):
    k = (d.year, d.month)
    return MONTHS.index(k) if k in MONTHS else None
