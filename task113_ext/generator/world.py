"""task113_ext: the fiction's constants.

Pellbrook Capital's systematic equity team keeps a research store of US small and mid cap common stocks. It buys
end-of-day prices, the security master and the corporate actions feed from Merriden Market Data (which moved its
delivery to a new platform at the start of 2024), point-in-time quarterly fundamentals and the earnings calendar
from Ledgerpoint Financial Data, its benchmark's constituents and levels from Northcote Indices, and takes the
exchanges' semi-monthly short interest as published. Its live book has traded since July 2023 through Kelloway
Securities, and its cash sits in the custodian's sweep. Everything here is synthetic; the exchange calendar is
the real one.
"""
import datetime as dt

SEED = 11300

START = dt.date(2018, 1, 2)          # first trading day in the store
END = dt.date(2026, 9, 30)           # last trading day in the store
OLD_LAST = dt.date(2023, 12, 29)     # the retired platform's history file ends here
BACKFILL_FROM = dt.date(2023, 10, 2) # the new platform's backfill starts here, overlapping the old file's last quarter
LIVE_FROM = dt.date(2023, 7, 3)      # the live book's first rebalance
FEE_CHANGE = dt.date(2025, 3, 3)     # Kelloway's commission falls from 1.5 to 1.0 cents a share (schedule of 10 Feb 2025)
SWEEP_SWITCH = dt.date(2023, 7, 1)   # the custodian re-bases its sweep on the overnight financing rate

N_START = 120                        # listed before the store begins
N_IPO = 20                           # listed during it
N_SPIN = 2                           # spun off during it

ORG = "Pellbrook Capital"
ORG_LEGAL = "Pellbrook Capital LLC"
TEAM = "Pellbrook Capital, Systematic Equity Research Data"
VENDOR_PX = "Merriden Market Data"
VENDOR_FUND = "Ledgerpoint Financial Data"
INDEX_CO = "Northcote Indices"
INDEX_NAME = "Northcote US Small Cap Select"
INDEX_CODE = "NUSSC"
BROKER = "Kelloway Securities"
CUSTODIAN = "Harrowgate Trust Company"

# Merriden's sector code, name, name descriptors, dividend payer share, idiosyncratic volatility multiplier
SECTORS = [
    ("EN", "Energy", ["Energy", "Resources", "Petroleum", "Midstream Partners", "Oilfield Services"], 0.45, 1.25),
    ("MT", "Materials", ["Chemicals", "Materials", "Minerals", "Packaging", "Specialty Metals"], 0.55, 1.05),
    ("IN", "Industrials", ["Industries", "Manufacturing", "Engineered Products", "Fluid Systems", "Controls",
                           "Aerostructures", "Freight"], 0.5, 1.0),
    ("CD", "Consumer Discretionary", ["Brands", "Outdoor", "Home Furnishings", "Restaurants", "Apparel",
                                      "Leisure"], 0.3, 1.15),
    ("CS", "Consumer Staples", ["Foods", "Beverage", "Farms", "Household Products"], 0.6, 0.8),
    ("HC", "Health Care", ["Biosciences", "Therapeutics", "Medical", "Diagnostics", "Health Services"], 0.15, 1.35),
    ("FN", "Financials", ["Bancorp", "Financial", "Capital", "Insurance Holdings"], 0.8, 0.85),
    ("IT", "Information Technology", ["Systems", "Software", "Networks", "Semiconductor", "Photonics",
                                      "Data Solutions"], 0.2, 1.2),
    ("CM", "Communication Services", ["Media", "Communications", "Broadcasting", "Interactive"], 0.3, 1.1),
    ("UT", "Utilities", ["Water", "Utilities", "Power"], 0.95, 0.6),
    ("RE", "Real Estate", ["Realty Trust", "Properties", "Residential"], 0.9, 0.8),
]
INDUSTRY = {
    "Energy": "Oil & Gas Producers", "Resources": "Oil & Gas Producers", "Petroleum": "Oil & Gas Refining",
    "Midstream Partners": "Pipelines", "Oilfield Services": "Oilfield Services", "Chemicals": "Specialty Chemicals",
    "Materials": "Building Materials", "Minerals": "Metals & Mining", "Packaging": "Packaging",
    "Specialty Metals": "Metals & Mining", "Industries": "Industrial Machinery", "Manufacturing": "Industrial Machinery",
    "Engineered Products": "Building Products", "Fluid Systems": "Flow Control", "Controls": "Electrical Equipment",
    "Aerostructures": "Aerospace & Defense", "Freight": "Trucking & Freight", "Brands": "Apparel & Footwear",
    "Outdoor": "Leisure Products", "Home Furnishings": "Home Furnishings", "Restaurants": "Restaurants",
    "Apparel": "Specialty Retail", "Leisure": "Hotels & Leisure", "Foods": "Packaged Foods", "Beverage": "Beverages",
    "Farms": "Agricultural Products", "Household Products": "Household Products", "Biosciences": "Biotechnology",
    "Therapeutics": "Biotechnology", "Medical": "Medical Devices", "Diagnostics": "Diagnostics & Research",
    "Health Services": "Health Care Services", "Bancorp": "Regional Banks", "Financial": "Consumer Lending",
    "Capital": "Asset Management", "Insurance Holdings": "Property & Casualty Insurance",
    "Systems": "Electronic Instruments", "Software": "Application Software", "Networks": "Communications Equipment",
    "Semiconductor": "Semiconductors", "Photonics": "Electronic Instruments", "Data Solutions": "IT Services",
    "Media": "Broadcasting & Media", "Communications": "Telecom Services", "Broadcasting": "Broadcasting & Media",
    "Interactive": "Internet Media", "Water": "Water Utilities", "Utilities": "Gas & Electric Utilities",
    "Power": "Electric Utilities", "Realty Trust": "Diversified REITs", "Properties": "Office REITs",
    "Residential": "Residential REITs",
}
SECTOR_WEIGHT = [0.06, 0.07, 0.17, 0.12, 0.05, 0.14, 0.14, 0.12, 0.04, 0.03, 0.06]

PREFIX = ["Ash", "Bal", "Bel", "Birch", "Bram", "Bren", "Brook", "Calder", "Car", "Cedar", "Clay", "Cole", "Copper",
          "Cran", "Dal", "Deer", "Dun", "East", "Elder", "Elm", "Fal", "Fern", "Flint", "Fox", "Gar", "Glen", "Gran",
          "Hal", "Hart", "Haw", "Hazel", "Heath", "Hol", "Ives", "Kel", "Kers", "Lang", "Lark", "Lin", "Lyn", "Mar",
          "Mead", "Mer", "Mill", "Mor", "Nor", "Oak", "Orr", "Pen", "Quin", "Rad", "Rams", "Ren", "Ros", "Rush", "Sal",
          "Sand", "Sel", "Shel", "Sher", "Stan", "Stour", "Tal", "Tam", "Thorn", "Tor", "Tre", "Ul", "Val", "Wal",
          "Wen", "Whit", "Wick", "Wil", "Wor", "Yar"]
SUFFIX = ["bury", "by", "combe", "croft", "dale", "den", "field", "ford", "gate", "ham", "hurst", "ley", "mere",
          "more", "mount", "port", "ridge", "stead", "ton", "vale", "well", "wick", "worth", "wood", "brook", "shaw"]
NAME_BLOCK = {"Ashford", "Brookfield", "Highwood", "Redwood", "Ironwood", "Westwood", "Silvergate", "Stonegate",
              "Kingsway", "Oakmont", "Eastgate", "Ridgewood", "Glenwood", "Elmwood", "Fairfield", "Woodbridge",
              "Cranbrook", "Hartford", "Sanford", "Stanley", "Holden", "Marlborough", "Wellington", "Salford",
              "Linton", "Carlton", "Langley", "Ashley", "Fernley", "Hawley", "Morley", "Shelby", "Selby", "Dalton",
              "Dunmore", "Mortimer", "Hollywood", "Sherwood", "Ramsgate", "Rosedale", "Glendale", "Oakley",
              "Garfield", "Marwood", "Penrose", "Thornton", "Whitley", "Wilton", "Walton", "Worthington", "Torrington",
              "Quinton", "Brenton", "Kelley", "Carrow", "Dalby", "Harley", "Lindale", "Merton", "Whitby", "Elmhurst",
              "Lynwood", "Lyndale", "Linwood", "Hazelwood", "Heathrow", "Millbrook", "Colby", "Carmel", "Calderdale",
              "Hawthorne", "Ashby", "Fenwright", "Corvane", "Larkspur", "Wexcombe", "Haldane", "Brackwater",
              "Calloway", "Thursby", "Stannard", "Ostler"}
LEGAL = ["Inc.", "Corp.", "Holdings, Inc.", "Co.", "Group, Inc.", "Inc.", "Corporation", "Inc."]

EXCHANGES = [("N", "NYSE", 1), ("A", "NYSE American", 2), ("Q", "Nasdaq", 3)]
EXCH_SHARE = [0.40, 0.05, 0.55]
MIC = {"N": "XNYS", "A": "XASE", "Q": "XNAS"}

FILES = {
    "px_old": "merriden_eod_us_equity_2018_2023.csv",
    "px_new": "merriden_eod_us_equity_2023q4_2026q3.parquet",
    "secmaster": "merriden_security_master_history.csv",
    "ca": "merriden_corporate_actions_2018_2026.json",
    "delist": "merriden_delisting_final_values.xlsx",
    "fund": "ledgerpoint_quarterly_pit_2017_2026.csv",
    "earn": "ledgerpoint_earnings_calendar.jsonl",
    "recon": "northcote_us_smallcap_select_reconstitutions.xlsx",
    "levels": "northcote_us_smallcap_select_levels.csv",
    "si": "short_interest_semimonthly_2018_2026.txt",
    "sweep": "harrowgate_sweep_rate_daily.csv",
    "orders": "pellbrook_oms_orders_2023_2026.csv",
    "fills": "kelloway_executions_2023_2026.csv",
    "dict_px": "merriden_eod_data_dictionary_v4.pdf",
    "spec_ca": "merriden_corporate_actions_feed_spec.pdf",
    "guide_fund": "ledgerpoint_pit_fundamentals_guide.pdf",
    "method_idx": "northcote_us_smallcap_select_methodology.pdf",
    "fees": "kelloway_commission_schedule_2025.pdf",
    "readme": "README_research_store_extracts.md",
}

# each file's date as its source dated it (delivery or extract date)
AS_OF = {
    "px_old": "2024-01-10", "px_new": "2026-10-06", "secmaster": "2026-10-06", "ca": "2026-10-06",
    "delist": "2026-10-07", "fund": "2026-10-08", "earn": "2026-10-08", "recon": "2026-07-10", "levels": "2026-10-02",
    "si": "2026-10-08", "sweep": "2026-10-07", "orders": "2026-10-05", "fills": "2026-10-05",
    "dict_px": "2024-01-08", "spec_ca": "2023-06-12", "guide_fund": "2025-03-17", "method_idx": "2025-02-14",
    "fees": "2025-02-10", "readme": "2026-10-09",
}
CA_PULLED = dt.date(2026, 10, 5)     # the corporate actions feed holds announcements to this date
FUND_PULLED = dt.date(2026, 10, 7)   # Ledgerpoint's knowledge dates run to this date
SI_LAST_PUB = dt.date(2026, 10, 8)
SWEEP_LAST = dt.date(2026, 10, 7)
