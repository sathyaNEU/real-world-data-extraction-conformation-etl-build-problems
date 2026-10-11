"""The Larkmoor world: constants, calendars and parameters. Everything else reads from here."""
import pandas as pd

SEED = 130
SIM_START = pd.Timestamp("2012-04-01")      # warm-up: the queue builds before the data window
START = pd.Timestamp("2018-04-01")          # first day the extracts cover
ASOF = pd.Timestamp("2026-09-30")          # extract cut: everything after this day is unknown
NOTICE = pd.Timestamp("2026-09-15")        # Corvane's notice; no placement into Tenter House from this day
VACANT = pd.Timestamp("2027-03-31")        # vacant possession
TH_OPEN = pd.Timestamp("2021-04-12")       # first placement into Tenter House
TH_RULE = pd.Timestamp("2023-04-03")       # from here a vacant flat goes to the longest nightly-paid household
MONTHS_FWD = pd.date_range("2026-10-01", "2027-03-01", freq="MS")

SIZES = [1, 2, 3, 4]                       # bedroom need; 4 means four or more
NEED_MIX = [0.35, 0.36, 0.23, 0.06]

# Tenter House: 178 self-contained flats by bedrooms
TH_UNITS = {1: 30, 2: 72, 3: 58, 4: 18}

# monthly move-on lets by bedroom size (social lets through nominations plus private lets
# through the council's lettings agency), history
def supply(month, size):
    y = month.year + (month.month - 1) / 12.0
    base = {1: 18.5, 2: 19.6, 3: 11.5, 4: 2.6}[size]
    if y < 2018.25:
        base *= 0.78                            # the queue builds up before the extracts begin
    if size == 3 and y >= 2024.25:
        base = 9.4                              # fewer three-bed relets after the 2024 stock transfer
    if size == 4 and y >= 2023.5:
        base = 1.8
    if size == 2 and y >= 2025.0:
        base = 22.4                             # the 2025 new-build programme lets two-bed flats
    if size == 1 and y >= 2024.0:
        base = 17.3
    return base

# the move-on plan, October 2026 to March 2027: planned lets by tenancy start month
PLAN_ORIGINAL = {  # drawn up in March 2026
    1: [15, 15, 13, 15, 15, 16],
    2: [19, 20, 17, 20, 20, 21],
    3: [8, 8, 7, 8, 8, 9],
    4: [2, 1, 1, 2, 2, 2],
}
PLAN_REVISED = {   # revised 14 September 2026: rephased, and the Brook Meadow phase 2 handover added
    1: [14, 16, 12, 15, 16, 16],
    2: [18, 21, 16, 21, 21, 20],
    3: [7, 9, 6, 8, 12, 14],         # Brook Meadow: 4 three-bed in February, 5 in March
    4: [1, 2, 1, 2, 7, 6],           # Brook Meadow: 5 four-bed in February, 4 in March
}
NEW_BUILD = {3: {4: 4, 5: 5}, 4: {4: 5, 5: 4}}   # size -> {month index: homes}

COUNCIL = "Larkmoor Borough Council"
BLOCK = "Tenter House"
PROVIDER = "Corvane Property Services Ltd"
