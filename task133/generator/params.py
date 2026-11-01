"""Fixed parameters of the Orari Bank world (task133, architecture 3).

Everything a rule or a document files is defined here once, and every script reads it from here.
"""
import datetime as dt

SEED = 133027

# Calendar of the fiction
BOOK_DATE = dt.date(2026, 9, 30)          # the book the stress runs on
WIN_START = dt.date(2025, 10, 1)          # operating-account credits window
WIN_END = dt.date(2026, 9, 30)
STD_EFFECTIVE = dt.date(2026, 7, 1)       # CR-ST-02 v3.1
SCEN_APPROVED = dt.date(2026, 9, 24)      # board approval of the severe scenario
BOARD_MEETING = dt.date(2026, 11, 26)
EXPORT_DATE = dt.datetime(2026, 10, 16, 9, 12, 0)   # every mtime in target/
H1 = (dt.date(2025, 10, 1), dt.date(2026, 3, 31))
H2 = (dt.date(2026, 4, 1), dt.date(2026, 9, 30))

# ANZSIC 2006 divisions
DIVISIONS = {
    "A": "Agriculture, Forestry and Fishing", "B": "Mining", "C": "Manufacturing",
    "D": "Electricity, Gas, Water and Waste Services", "E": "Construction", "F": "Wholesale Trade",
    "G": "Retail Trade", "H": "Accommodation and Food Services", "I": "Transport, Postal and Warehousing",
    "J": "Information Media and Telecommunications", "K": "Financial and Insurance Services",
    "L": "Rental, Hiring and Real Estate Services", "M": "Professional, Scientific and Technical Services",
    "N": "Administrative and Support Services", "O": "Public Administration and Safety",
    "P": "Education and Training", "Q": "Health Care and Social Assistance",
    "R": "Arts and Recreation Services", "S": "Other Services",
}

# Severe scenario: change in each division's sales in the stress year (year to 30 September 2027)
# against the year to 30 September 2026, per cent. Negative is a fall.
SCENARIO_CHANGE = {
    "A": -12.6, "B": -8.4, "C": -7.9, "D": -2.1, "E": -27.4, "F": -6.6, "G": -6.4, "H": -22.6,
    "I": -12.3, "J": -3.2, "K": -3.6, "L": -12.1, "M": -6.8, "N": -7.4, "O": 1.8, "P": 0.9,
    "Q": 1.6, "R": -17.8, "S": -7.0,
}

# CR-ST-02 Table 1: 12-month PD by risk grade (per cent)
GRADE_PD = {1: 0.25, 2: 0.45, 3: 0.75, 4: 1.20, 5: 1.90, 6: 3.10, 7: 5.20, 8: 9.00, 9: 16.00}

# CR-ST-02 Table 2: multiplier on the 12-month PD by the fall in the borrower's own sales over the
# stress year. Bands are [lower, upper) in per cent of sales; no fall keeps the PD (multiplier 1).
PD_BANDS = [(0.0, 5.0, 1.25), (5.0, 10.0, 1.60), (10.0, 15.0, 2.30), (15.0, 20.0, 3.30),
            (20.0, 25.0, 4.60), (25.0, 30.0, 6.20), (30.0, 1000.0, 8.00)]

# CR-ST-02 Table 3: stressed LGD by the facility's security code
LGD = {"CM1": 0.28, "RM1": 0.22, "GSA": 0.52, "EQP": 0.40, "UNS": 0.75}
SECURITY_TEXT = {
    "CM1": "First registered mortgage over commercial or industrial property",
    "RM1": "First registered mortgage over residential property",
    "GSA": "General security agreement over all present and after-acquired property",
    "EQP": "Specific security over financed plant, vehicles or equipment",
    "UNS": "No security held",
}

# CR-ST-02 3.3: credit conversion on revolving facilities
CCF_REVOLVING = 0.50
REVOLVING = {"Business overdraft", "Revolving credit facility"}

# CR-ST-02 Table 4: reporting segments by the borrower's ANZSIC division
SEGMENTS = [
    ("Construction", "E"),
    ("Manufacturing", "C"),
    ("Trade and logistics", "FI"),
    ("Hospitality, retail and leisure", "GHR"),
    ("Business and property services", "LMN"),
    ("Health, education and personal services", "PQS"),
]
SEG_OF = {d: s for s, ds in SEGMENTS for d in ds}


def multiplier(fall_pct):
    """Table 2. fall_pct is the fall in sales in per cent (positive is a fall)."""
    if fall_pct <= 0:
        return 1.0
    for lo, hi, m in PD_BANDS:
        if lo <= fall_pct < hi:
            return m
    raise ValueError(fall_pct)

# Exposure scale by reporting segment (the size of the book in each segment), applied to every facility's limit
# and balance after the world is drawn.
EXPOSURE_SCALE = {
    "Construction": 0.9069,
    "Manufacturing": 0.7244,
    "Trade and logistics": 0.9405,
    "Hospitality, retail and leisure": 0.9009,
    "Business and property services": 0.8398,
    "Health, education and personal services": 0.9771,
}

# The 2025 risk-grade back-test world
LEAVERS = 73            # business customers on the 30 September 2025 book who have since left it
YEAR_PD_FACTOR = 1.0    # realised one-year default rate against the grade PD in the year to 30 September 2026
GROUPS = 30             # connected groups among current business borrowers
FORCED_GROUPS = 5       # of which a member defaulted in the year (cross-default takes the group)
WO_MEDIAN = 40660       # median amount written off on a business facility (NZD)
WO_SEG_FACTOR = {"Construction": 1.7, "Hospitality, retail and leisure": 1.3, "Trade and logistics": 1.1}
GUARANTOR_SHARE = 0.6    # written-off companies whose directors' personal guarantees were called
RURAL_DEFAULTS = 3        # business borrowers moved to the rural book that defaulted there in the year
RURAL_SEED_OFFSET = 220
TRADING_NAME_SHARE = 0.3  # of firms with a registered trading name, the share whose bank sends that name
