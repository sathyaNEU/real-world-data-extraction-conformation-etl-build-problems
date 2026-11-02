"""World parameters for task233 architecture 3: a national statistics office's price collection
quality assessment for the third quarter of 2026. Every random draw takes its own stream from SEED."""
import datetime as dt

SEED = 2332026

# reference months carried by the price database extract
MONTHS = [(2025, 10), (2025, 11), (2025, 12), (2026, 1), (2026, 2), (2026, 3),
          (2026, 4), (2026, 5), (2026, 6), (2026, 7), (2026, 8), (2026, 9)]
QUARTER = [(2026, 7), (2026, 8), (2026, 9)]
PATH_START = dt.date(2025, 8, 1)
PATH_END = dt.date(2026, 10, 31)

# public holidays of the fictional country (the collection calendar lists them)
HOLIDAYS = [dt.date(2025, 10, 27), dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1),
            dt.date(2026, 1, 2), dt.date(2026, 2, 6), dt.date(2026, 4, 3), dt.date(2026, 4, 6),
            dt.date(2026, 4, 27), dt.date(2026, 6, 1), dt.date(2026, 8, 17), dt.date(2026, 10, 26)]
WINDOW_WORKDAYS = 5          # the index day and the four working days after it

# collection regions: NSO code, NSO name, contractor's name for the region, ring of the
# Field Quality Team's circuit, multiples and independents in the CPI outlet sample
REGIONS = [
    ("CR01", "Halbrook Central", "Halbrook Central", 0, 12, 15),
    ("CR02", "Halbrook North", "Halbrook Nth", 0, 10, 14),
    ("CR03", "Halbrook South", "Halbrook Sth", 0, 11, 16),
    ("CR04", "Eastwick Coast", "Eastwick", 1, 9, 14),
    ("CR05", "Belmont Valley", "Belmont", 1, 8, 15),
    ("CR06", "Wexcombe Plains", "Wexcombe", 1, 9, 13),
    ("CR07", "Tamsin Bay", "Tamsin Bay", 2, 8, 14),
    ("CR08", "Greywater", "Greywater", 2, 9, 15),
    ("CR09", "Ardmore Uplands", "Ardmore", 2, 7, 13),
    ("CR10", "Fenwick", "Fenwick", 2, 8, 14),
    ("CR11", "Corran Peninsula", "Corran", 3, 7, 15),
    ("CR12", "Westholm", "Westholm", 3, 8, 13),
    ("CR13", "Rookby Downs", "Rookby", 3, 7, 14),
    ("CR14", "Northreach", "Northreach", 3, 8, 15),
]

# Field Quality Team circuit: calendar days after the index day on which the team re-collects
# in each region (moved to the next working day when it falls on a weekend or holiday)
FQT_OFFSET = {"CR01": 2, "CR02": 1, "CR03": 2, "CR04": 6, "CR05": 6, "CR06": 7, "CR07": 6,
              "CR08": 7, "CR09": 6, "CR10": 7, "CR11": 7, "CR12": 6, "CR13": 6, "CR14": 7}
FQT_MULTIPLES = 4            # outlets re-collected per region per month
FQT_INDEPENDENTS = 5
FQT_DRAW_DAYS = 4            # the team re-collects at outlets visited in the window's first four working days

# collector recording errors by region (truth): keying slips and wrong variety or size at a low,
# near-uniform rate, and the chance a collector keeps the handheld's pre-filled previous price when the
# shelf price has changed since the last visit, which carries the regions' differences
ERRORS = {
    "CR01": (0.0024, 0.0016, 0.0235),
    "CR02": (0.0031, 0.0019, 0.1900),
    "CR03": (0.0022, 0.0015, 0.0647),
    "CR04": (0.0026, 0.0017, 0.0691),
    "CR05": (0.0034, 0.0021, 0.5378),
    "CR06": (0.0027, 0.0016, 0.0428),
    "CR07": (0.0030, 0.0020, 0.2809),
    "CR08": (0.0025, 0.0018, 0.0175),
    "CR09": (0.0023, 0.0015, 0.0759),
    "CR10": (0.0032, 0.0019, 0.3603),
    "CR11": (0.0026, 0.0016, 0.0232),
    "CR12": (0.0029, 0.0020, 0.3878),
    "CR13": (0.0024, 0.0017, 0.0737),
    "CR14": (0.0027, 0.0016, 0.0032),
}

# Price Collection Quality Standard bands on collection accuracy (per cent)
BAND_COMPLIANT = 98.0
BAND_CREDIT = 95.5
CREDIT_PERCENT = 4

# item groups: monthly frequency of a shelf-price change at multiples and at independents
GROUPS = {
    "FV": ("Fresh fruit and vegetables", 0.19, 0.15),
    "MF": ("Meat, fish and poultry", 0.11, 0.075),
    "BC": ("Bread and cereals", 0.075, 0.045),
    "DE": ("Milk, cheese and eggs", 0.085, 0.05),
    "OF": ("Other food and non-alcoholic drinks", 0.095, 0.06),
    "HS": ("Household supplies", 0.07, 0.035),
    "PC": ("Personal care", 0.075, 0.035),
    "CF": ("Clothing and footwear", 0.06, 0.025),
}

# outlet kinds: stratum, share of the stratum, quotes per outlet (low, high), item groups priced
KINDS = {
    "supermarket": ("M", 0.62, (34, 46), ["FV", "MF", "BC", "DE", "OF", "HS", "PC"]),
    "pharmacy_chain": ("M", 0.20, (8, 12), ["PC", "HS"]),
    "clothing_chain": ("M", 0.18, (7, 10), ["CF"]),
    "greengrocer": ("I", 0.24, (7, 10), ["FV"]),
    "butcher": ("I", 0.14, (5, 7), ["MF"]),
    "bakery": ("I", 0.13, (4, 6), ["BC"]),
    "convenience": ("I", 0.22, (7, 10), ["DE", "OF", "BC", "HS"]),
    "pharmacy": ("I", 0.11, (5, 7), ["PC"]),
    "boutique": ("I", 0.10, (4, 6), ["CF"]),
    "hardware": ("I", 0.06, (5, 7), ["HS"]),
}

CHAINS = {
    "supermarket": ["Freshway", "ValuMart", "Kettering's", "Harbour Fresh"],
    "pharmacy_chain": ["CareMed Pharmacy", "Lifeline Chemists"],
    "clothing_chain": ["Threadline", "Baxter & Co"],
}

STATUS_UNAVAILABLE = 0.028   # quote-months the collector could not price
STATUS_REPLACED = 0.012      # quote-months the collector moved to a new variety
LATE_VISIT = 0.045           # outlet-months first visited after the collection window
VISIT_WEIGHTS = {"M": [0.26, 0.24, 0.21, 0.16, 0.13], "I": [0.30, 0.25, 0.20, 0.15, 0.10]}
SPLIT_VISIT = 0.06           # large supermarket outlet-months collected over two visits
FQT_NOT_FOUND = 0.012        # back-checked items the team could not find on the day
FQT_TRIES = 23               # candidate draws of each month's back-check sample (generator only)

MISSED_VISIT = 0.012         # outlet-months scheduled but not visited at all
REBRAND_DATE = dt.date(2026, 8, 1)   # Lifeline Chemists' branches trade as CareMed Pharmacy from this day
EXTRACT_DATE = dt.date(2026, 10, 14) # the price database and review log extracts
REVIEW_QUERY = 0.12          # replacements first sent back to the contractor with a query
REVIEW_COMPARABLE = 0.74     # final decisions that accept the replacement as comparable
REVIEW_RECHECK = 0.14        # final decisions the senior commodity analyst re-checks
RESENT_BATCH = 0.012         # outlet-month uploads the handheld sent twice
