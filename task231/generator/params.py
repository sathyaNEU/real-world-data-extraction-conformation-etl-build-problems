"""task231 parameters: the Brevland Central Bank's Business Conditions Survey panel, 2017 to the September 2026 round."""
from datetime import date

SEED = 23104
REC_SEED = 23177                         # the records layer (times, identifiers, call attempts, the asks' records)

# Rounds: March, June, September and December; the frame date is the first day of the round month.
BURN_IN = date(2014, 3, 1)              # the panel started in 2014; the round outcomes on file start in March 2017
FIRST_ROUND = date(2017, 3, 1)
CURRENT = date(2026, 9, 1)
MAIN_CLOSE = date(2026, 9, 25)          # Friday, 17:00 local time
EXTRACT = date(2026, 9, 25)             # business register extract and returns file as at the main close
EXT_START, EXT_END = date(2026, 9, 28), date(2026, 10, 9)
THRESHOLD = 0.55
CALL_DAY = 15                           # the contact centre calls the round's non-returners from day 15 to the close
RETIRE_AFTER = 6                        # a firm silent for six rounds in a row is retired before the next round
EXPANSION_ROUND = date(2024, 3, 1)      # the panel was doubled in March 2024
SETTLED_MONTHS = 48                     # rounds whose frame date is at least this far before the extract count as settled

# Region: (code, name, firms in the 2014 panel, response propensity beta (a, b), closure hazard multiplier)
REGIONS = [
    ("R01", "Capital",          560, (3.679, 4.921), 1.00),
    ("R02", "Harbour",          430, (4.174, 4.426), 1.00),
    ("R03", "North Coast",      330, (5.300, 3.300), 1.00),
    ("R04", "Islands",          250, (4.825, 3.775), 1.00),
    ("R05", "Border",           300, (5.159, 3.441), 1.00),
    ("R06", "Western Uplands",  310, (4.807, 3.793), 1.00),
    ("R07", "Northern Forests", 290, (5.335, 3.265), 1.00),
    ("R08", "South Coast",      450, (5.454, 3.146), 1.00),
    ("R09", "Eastern Lakes",    400, (5.442, 3.158), 1.00),
    ("R10", "Midlands",         470, (5.352, 3.248), 1.00),
    ("R11", "River Valley",     400, (5.753, 2.847), 1.00),
    ("R12", "Southern Plains",  380, (5.445, 3.155), 1.00),
]
EXPANSION_SHARE = 1.00
# Each region draws from its own streams; the offsets place every region clear of the 55 and 58 per cent lines.
REGION_SEEDS = {"R01": 0, "R02": 0, "R03": 28, "R04": 19, "R05": 23, "R06": 15, "R07": 53, "R08": 13, "R09": 8, "R10": 62, "R11": 8, "R12": 18}
AMBER = 0.58

INDUSTRIES = [("A", "Agriculture, forestry and fishing", 0.05), ("C", "Manufacturing", 0.14), ("F", "Construction", 0.12),
              ("G", "Wholesale and retail trade", 0.18), ("H", "Transport and storage", 0.07), ("I", "Accommodation and food", 0.09),
              ("J", "Information and communication", 0.08), ("M", "Professional and technical services", 0.15),
              ("N", "Administrative and support services", 0.12)]
SIZES = [("S1", "5 to 19", 0.46, 0.85), ("S2", "20 to 49", 0.27, 1.00), ("S3", "50 to 249", 0.20, 1.12), ("S4", "250 or more", 0.07, 1.25)]

# Closures: a quarterly hazard, the same in every region and size band.
HAZARD = 0.0215
SIZE_HAZARD = {"S1": 1.00, "S2": 1.00, "S3": 1.00, "S4": 1.00}
WITHDRAW = 0.004

# The register records a closure when it is notified: (share, median lag in days, log sd) by route.
LAG_ROUTES = [("voluntary", 0.28, 100, 0.55), ("administrative", 0.40, 500, 0.25), ("insolvency", 0.32, 780, 0.28)]

# Contact-centre call outcomes for a firm still not returned on day 15: alive firms, closed firms.
CALL_ALIVE = {"returned": 0.16, "promised": 0.22, "refused": 0.25, "ceased": 0.0, "unobtainable": 0.03, "no_answer": 0.34}
CALL_CLOSED = {"returned": 0.0, "promised": 0.0, "refused": 0.0, "ceased": 0.10, "unobtainable": 0.24, "no_answer": 0.66}
CALL_RETURN_LIFT = 0.55                 # a firm that answers and promises returns before the close with this probability
