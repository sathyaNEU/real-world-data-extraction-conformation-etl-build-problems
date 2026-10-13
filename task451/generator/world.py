"""task451 (architecture 2): the Laurelford Building Trades Health and Welfare Fund's 2026 reconciliation with its
twelve accountable care partners. Everything fixed about the world lives here: dates, organisations, people, the
partners, the claims and pharmacy processes, and the administrator's adjudication before and after the Tallis
platform went live."""
import datetime as dt

D = dt.date

# ----------------------------------------------------------------------------------------------------------- dates
SERVICE_FROM = D(2025, 1, 1)          # the extract's first date of service
SERVICE_TO = D(2027, 1, 31)           # and its last
YEAR = 2026                           # the performance year
CUT = D(2027, 1, 29)                  # claims paid through the last business day of January (Schedule B)
ELIG_EXPORT = D(2027, 2, 1)           # the eligibility export holds the span versions posted by this day
EXTRACT_RUN = D(2027, 2, 1)           # Keswold's monthly extract
GOLIVE = D(2026, 10, 5)               # the Fund's claims adjudicated on Tallis from this Monday
BACKLOG_END = D(2026, 10, 16)         # claims pending at go-live, adjudicated in the first two weeks
TRUSTEES = D(2027, 2, 17)             # the trustees approve the settlement notices
ROSTER_DATE = D(2027, 1, 1)           # the partners' clinician roster snapshot
RX_FROM, RX_TO = D(2026, 1, 1), D(2026, 12, 31)

HOLIDAYS = {D(2025, 1, 1), D(2025, 1, 20), D(2025, 2, 17), D(2025, 5, 26), D(2025, 6, 19), D(2025, 7, 4), D(2025, 9, 1),
            D(2025, 10, 13), D(2025, 11, 11), D(2025, 11, 27), D(2025, 12, 25), D(2026, 1, 1), D(2026, 1, 19),
            D(2026, 2, 16), D(2026, 5, 25), D(2026, 6, 19), D(2026, 7, 3), D(2026, 9, 7), D(2026, 10, 12),
            D(2026, 11, 11), D(2026, 11, 26), D(2026, 12, 25), D(2027, 1, 1), D(2027, 1, 18)}

# ------------------------------------------------------------------------------------------------- organisations
FUND = "Laurelford Building Trades Health and Welfare Fund"
FUND_SHORT = "Laurelford Fund"
TPA = "Keswold Benefit Services"
PLATFORM = "Tallis"
PBM = "Corvane Pharmacy Benefits"
REPRICER = "Penn Hollow Preferred Network"
STOP_LOSS_CARRIER = "Wexley Mutual Life"
PEOPLE = {
    "administrator": ("Ariel Hogan", "Fund Administrator"),
    "controller": ("George Khan", "Fund Controller"),
    "tpa": ("Jason Pollard", "Account Executive, Keswold Benefit Services"),
    "chair": ("Linda Austin", "Chair, Health Committee of the Board of Trustees"),
}

# ------------------------------------------------------------------------------------------------------ agreement
TRUNCATION = 200000.0                 # each member's year above this is excluded (Schedule B)
CORRIDOR = 0.02                       # a partner owes if its TCOC PMPM is more than 2.0 per cent over its target
SHARE = 0.40                          # the partner's share of the excess
STOP_LOSS_DEDUCTIBLE = 175000.0       # the Fund's specific stop-loss (a different contract)

# ------------------------------------------------------------------------------------------------------- partners
# code, name, kind (adult, family, pediatric), PCP clinicians, specialists, relative practice cost, and the partner's
# role in the ladder, which build.py turns into its Exhibit 1 target from the shipped data:
#   owe        owes on every golden route and on paid-as-extracted (x = golden TCOC PMPM / 1.02 target, fixed)
#   owe_r1     owes on every golden route, not on paid-as-extracted (x set mid-band)
#   band_l4    owes on no golden route, owes on the paid-date ladders over four, six and twelve months and all history
#   band_r0    owes only on the paid-date ladders over twelve months and all history
#   clear      owes on no route (x fixed)
PARTNERS = [
    ("RPG", "Ridgeline Physician Group", "adult", 16, 9, 1.00, "band_r0", None),
    ("BMA", "Brookhollow Medical Associates", "adult", 13, 6, 1.05, "clear", 0.860),
    ("SPP", "Sycamore Pediatric Partners", "pediatric", 14, 5, 0.95, "clear", 0.850),
    ("SIM", "Stonecrest Internal Medicine", "adult", 10, 7, 1.10, "owe", 1.070),
    ("KRH", "Kettle Run Health Partners", "family", 12, 4, 0.97, "owe_r1", None),
    ("HPM", "Harrow Point Medical Group", "adult", 9, 8, 1.12, "owe_r1", None),
    ("WVP", "Wren Valley Physicians", "adult", 8, 3, 0.92, "clear", 0.830),
    ("BCN", "Bellmont Clinic Network", "family", 14, 5, 1.02, "owe", 1.050),
    ("CFP", "Calder Family Practice", "family", 9, 3, 0.90, "band_r0", None),
    ("THA", "Tamarack Health Alliance", "adult", 9, 6, 1.06, "band_r0", None),
    ("JHP", "Juniper Hollow Primary Care", "adult", 7, 2, 0.88, "band_r0", None),
    ("ALM", "Ashby Lane Medical", "adult", 7, 4, 1.08, "band_l4", None),
]
CODES = [p[0] for p in PARTNERS]
NAME = {p[0]: p[1] for p in PARTNERS}
KIND = {p[0]: p[2] for p in PARTNERS}
STYLE = {p[0]: p[5] for p in PARTNERS}
ROLE = {p[0]: p[6] for p in PARTNERS}
PLACE = {p[0]: p[7] for p in PARTNERS}

# ------------------------------------------------------------------------------------------------------ population
SUBSCRIBERS = 4300
SPOUSE_SHARE = 0.56
CHILDREN_MEAN = 0.80

# ------------------------------------------------------------------------------------------------------ claims
# claims per member-month, mean Fund paid amount, lognormal sigma, provider submission lag (gamma shape, mean days),
# late share and late mean days; the lag is from the last date of service to the administrator's receipt
CLAIM_TYPES = {
    "P": (0.62, 118.0, 1.05, 1.4, 13.0, 0.05, 80.0),      # professional (CMS-1500)
    "O": (0.17, 905.0, 1.15, 2.0, 22.0, 0.06, 95.0),      # outpatient facility (UB-04 13x)
    "I": (0.0064, 21500.0, 0.95, 2.0, 30.0, 0.08, 120.0),  # inpatient facility (UB-04 11x)
}
# the administrator before Tallis: network repricing and review, then the Thursday payment run; a pended claim
# waits for a letter or a medical review
OLD_REVIEW = (2.0, 9.0)               # gamma shape and scale, days from receipt to ready
OLD_PEND = 0.22
OLD_PEND_DAYS = (25, 75)
# on Tallis: repriced and adjudicated on receipt, paid in the next business day's run unless pended
NEW_PEND = 0.13
NEW_PEND_DAYS = (5, 30)
REPLACE_SHARE = 0.04                  # claims later replaced (re-priced or corrected)
VOID_SHARE = 0.015                    # claims later voided
DENY_SHARE = 0.035                    # claims denied (paid zero)

# ------------------------------------------------------------------------------------------------------ pharmacy
RX_RATE = {"child": 0.32, "adult": 0.72, "older": 1.35}   # fills per member-month
RX_MEAN, RX_SIGMA = 74.0, 1.15
SPECIALTY_SHARE, SPECIALTY_RANGE = 0.007, (2400.0, 9200.0)
RX_REVERSAL = 0.03

SEED = 4512
