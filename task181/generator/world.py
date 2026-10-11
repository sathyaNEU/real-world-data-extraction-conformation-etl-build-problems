"""task181 world: Larchmere Credit Union, eastern Ontario, the card reissue after the counterfeit wave.

Every constant the pack is built from lives here. Nothing in the shipped bundle states a figure that is
not derived from these by sim.py, fraud.py and the writers.
"""
import datetime as dt

SEED = 181_2026
ORG = "Larchmere Credit Union"

# Calendar -----------------------------------------------------------------------------------------
EXTRACT_DATE = dt.date(2026, 10, 5)            # Monday; card history as at this date
LOG_START_UTC = dt.datetime(2026, 6, 1, 0, 0)   # authorisation log window, UTC, end exclusive
LOG_END_UTC = dt.datetime(2026, 10, 5, 0, 0)
SIM_START = dt.date(2026, 5, 31)               # local (Eastern) days simulated
SIM_END = dt.date(2026, 10, 4)
UTC_OFFSET_H = 4                               # EDT all period: UTC = local + 4 h
COMMITTEE = dt.date(2026, 10, 8)

# holidays the credit union observes (MS-3 appendix); weekend rule only otherwise
HOLIDAYS_2026 = [
    (dt.date(2026, 1, 1), "New Year's Day"),
    (dt.date(2026, 2, 16), "Family Day"),
    (dt.date(2026, 4, 3), "Good Friday"),
    (dt.date(2026, 5, 18), "Victoria Day"),
    (dt.date(2026, 7, 1), "Canada Day"),
    (dt.date(2026, 8, 3), "Civic Holiday"),
    (dt.date(2026, 9, 7), "Labour Day"),
    (dt.date(2026, 10, 12), "Thanksgiving"),
    (dt.date(2026, 12, 25), "Christmas Day"),
    (dt.date(2026, 12, 28), "Boxing Day (observed)"),
]
HOLIDAY_SET = {d for d, _ in HOLIDAYS_2026}

# Branches and where members live ------------------------------------------------------------------
BRANCHES = [  # town, share of members, street address of the branch
    ("Smiths Falls", 0.255, "41 Beckwith St N"),
    ("Perth", 0.150, "88 Gore St E"),
    ("Carleton Place", 0.140, "160 Bridge St"),
    ("Kemptville", 0.150, "2 Clothier St W"),
    ("Merrickville", 0.068, "306 Main St W"),
    ("Brockville", 0.122, "95 King St W"),
    ("Kingston", 0.115, "1240 Princess St"),
]
N_MEMBERS = 9_840

# Counterfeit wave ---------------------------------------------------------------------------------
N_PUMP_VICTIMS = 205
N_PINPAD_VICTIMS = 47
N_BACKGROUND_VICTIMS = 31
CARWASH_TWIN_VICTIMS = 47                      # pump victims the car wash read in their lookback
LOOKBACK_DAYS = 60

PUMP_WINDOW = (dt.date(2026, 8, 5), dt.date(2026, 8, 31))   # skimmer on OPT 6
PUMP_OUT_OF_SERVICE = dt.date(2026, 9, 1)                    # reader replaced; new TID from 2 Sep
PUMP_DISPENSER_REPAIR = (dt.date(2026, 6, 29), dt.date(2026, 7, 24))   # OPT 6 dispenser bagged, same reader
SCO_WINDOW = (dt.date(2026, 8, 13), dt.date(2026, 9, 14))    # overlay on self-checkout lane 2
SCO_NEW_TIDS = dt.date(2026, 9, 15)                          # all self-checkout PIN pads re-terminalled

PUMP_FIRST_USE = (dt.date(2026, 8, 24), dt.date(2026, 9, 30))
PINPAD_FIRST_USE = (dt.date(2026, 8, 28), dt.date(2026, 10, 2))
BACKGROUND_FIRST_USE = (dt.date(2026, 8, 25), dt.date(2026, 10, 1))

# People (drawn with guard.py names, en_CA, seed 1813, plus the four on the card) ------------------
PEOPLE = {
    "requester": "Laurie Townsend",        # fraud and risk manager
    "chair": "Brenda Figueroa",            # chair, board risk committee
    "cards": "Stephanie Wise",             # card services manager
    "analyst": "Nicholas Rodriguez",       # fraud analyst
    "member_exp": "Erika Jenkins",         # member experience manager, owner of MS-3
    "brockville": "Eric Snyder",           # Brockville branch manager in 2025
    "cash_ops": "Donna Keller",            # cash operations
}

# FX: Bank of Canada style daily USD/CAD path (deterministic), markup the credit union applies
USD_CAD_START = 1.3684
FX_MARKUP = 0.025
