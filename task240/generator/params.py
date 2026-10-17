"""task240 constants: Larchmere Social Research's 2027 Household Resources Survey for the Statistics and Surveys Branch."""
import datetime as dt

SEED = 61
POP_SEED = 2351                                  # the population estimates' band-to-band variation

AGENCY = "Larchmere Social Research"
CLIENT = "Statistics and Surveys Branch"
SURVEY = "Household Resources Survey"
STANDARD = "QS-7"

FIELD_OPEN = dt.date(2027, 4, 7)
FIELD_CLOSE = dt.date(2027, 9, 26)
OUTCOME_EXTRACT = dt.date(2027, 9, 30)          # the outcome file as extracted for the fieldwork close-out
CALLS_EXPORT = dt.date(2027, 10, 18)            # the call records once every tablet had synced
WEIGHTS_FROZEN = dt.date(2027, 11, 12)
ASOF = dt.date(2027, 12, 3)
DUE = dt.date(2027, 12, 10)
POP_REF = dt.date(2027, 7, 1)
BOUNDARY_REVIEW = dt.date(2025, 4, 1)

LINE = 20.0                                     # coefficient of variation, per cent, at which the warning applies

# health regions: code, name, adults (thousands), urban share of the region's PSUs
REGIONS = [
    ("R01", "Far North", 38, 0.30),
    ("R02", "North West", 46, 0.35),
    ("R03", "North East", 61, 0.40),
    ("R04", "Lakes", 79, 0.45),
    ("R05", "Capital", 905, 0.92),
    ("R06", "Central", 768, 0.85),
    ("R07", "East", 640, 0.70),
    ("R08", "South East", 520, 0.68),
    ("R09", "South", 418, 0.65),
    ("R10", "South West", 331, 0.60),
    ("R11", "West", 262, 0.58),
    ("R12", "Valley", 205, 0.50),
]
ADULTS_PER_THOUSAND = 1.9                       # responding adults per thousand adults in the region, by design
ADULTS_PER_PSU = 11.5

# the 2025 boundary review moved some master-sample PSUs between regions; the issued file keeps the region code the
# PSU was selected under
MOVED = [("R02", "R01", [3]), ("R04", "R03", [0]), ("R06", "R05", [0, 1, 2]), ("R07", "R08", [0, 49]),
         ("R10", "R09", [0, 1, 5]), ("R12", "R11", [0, 33])]   # (old region, new region, which of the new region's
                                                               # 2023 PSUs in frame order)

AGE_GROUPS = ["16-29", "30-49", "50-64", "65 and over"]
AGE_CUTS = [30, 50, 65]
AGE_SHARE = [0.22, 0.32, 0.26, 0.20]

INDICATORS = [
    ("PEN", "Adults receiving a public pension"),
    ("RENT", "Adults in privately rented homes"),
    ("CARE", "Adults providing unpaid care"),
    ("ARR", "Adults in households behind on a household bill"),
]

# address eligibility and fieldwork
P_VACANT, P_NONRES, P_DEMOL = 0.052, 0.024, 0.012
P_UNKNOWN_IF_NOCONTACT = 0.45                  # a no-contact address whose occupancy was never established
P_REISSUE = 0.10                               # first-issue non-response and unknown addresses reissued
P_REISSUE_CONVERT = 0.27
P_UNWORKED = 0.012                             # issued, never worked
P_LATE_SYNC = 0.028                            # interviews whose tablet synced after the outcome extract
P_RESENT = 0.035                               # calls a tablet sent again after a failed sync
