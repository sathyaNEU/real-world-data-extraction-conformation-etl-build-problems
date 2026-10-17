"""task238 constants: the fiction's calendar, regions, the twelve headline indexes (items, scoring, continuity
tolerances, true mode effects) and the household model behind the contact strategy test."""
import datetime as dt

SEED = 238
TZ = "Pacific/Auckland"                 # Halvreth time: UTC+12, UTC+13 from the last Sunday in September to the first Sunday in April
QUARTERS = ["2027Q2", "2027Q3"]
ISSUED = 38000                          # addresses per quarter
BATCHES = 6                             # fortnightly releases per quarter
Q_START = {"2027Q2": dt.date(2027, 4, 1), "2027Q3": dt.date(2027, 7, 1)}
Q_END = {"2027Q2": dt.date(2027, 6, 30), "2027Q3": dt.date(2027, 9, 30)}
OUTAGE = (dt.date(2027, 8, 9), dt.date(2027, 8, 12))      # CATI system down; interviewers keyed through the web platform
CLOSE_OUT = dt.date(2027, 10, 15)
AS_OF = dt.date(2027, 10, 20)

REGIONS = [(1, "Harbour", 0.31), (2, "Northern", 0.19), (3, "Central", 0.17), (4, "Eastern", 0.14),
           (5, "Southern", 0.12), (6, "Outer Islands", 0.07)]

# code, name, item, kind, tolerance, true mode effect (web minus telephone; points on 0 to 10, percentage points)
INDEXES = [
    ("LS", "Life satisfaction", "Q01", "score", 0.03, -0.25),
    ("WW", "Worthwhile", "Q02", "score", 0.03, -0.18),
    ("HY", "Happiness yesterday", "Q03", "score", 0.04, -0.22),
    ("AX", "Anxiety yesterday", "Q04", "score", 0.05, 0.38),
    ("LN", "Loneliness", "Q10", "pct", 0.30, 3.4),
    ("TR", "Trust in others", "Q11", "pct", 0.40, -1.0),
    ("SF", "Safe after dark", "Q12", "pct", 0.30, -0.8),
    ("GH", "Good health", "Q13", "pct", 0.35, -2.6),
    ("SM", "Smoking", "Q14", "pct", 0.25, 2.0),
    ("BD", "Heavy drinking", "Q15", "pct", 0.30, 7.25),
    ("VL", "Volunteering", "Q16", "pct", 0.35, -5.4),
    ("FS", "Financial strain", "Q17", "pct", 0.30, 2.9),
]
CODES = [x[0] for x in INDEXES]
SCORE = [x[0] for x in INDEXES if x[3] == "score"]

# Phone-answer models. score: latent mean on 0 to 10 and the latent's spread; pct: linear probability of the counted
# answer. Terms: age per decade from 49, female, post-school, degree, employed, renter, household size from 2.4,
# away-from-home lifestyle and ease online (both standard normal, neither recorded), region shifts.
OUT = {
    #        base   age    fem    post   deg    emp    rent   hh     away   online
    "LS": (7.45, 0.06, 0.05, 0.08, 0.15, 0.20, -0.25, 0.03, 0.10, 0.02, 1.95),
    "WW": (7.80, 0.08, 0.12, 0.06, 0.12, 0.25, -0.15, 0.04, 0.10, 0.00, 1.85),
    "HY": (7.40, 0.07, 0.00, 0.04, 0.06, 0.05, -0.15, 0.02, 0.12, 0.02, 2.30),
    "AX": (3.15, -0.10, 0.30, 0.02, 0.04, -0.05, 0.15, 0.00, -0.08, -0.04, 2.70),
    "LN": (0.085, -0.008, 0.012, -0.004, -0.010, -0.025, 0.030, -0.020, -0.030, 0.000),
    "TR": (0.52, 0.010, -0.010, 0.040, 0.110, 0.010, -0.050, 0.000, 0.035, 0.020),
    "SF": (0.66, 0.005, -0.150, 0.010, 0.030, 0.020, -0.030, 0.005, 0.270, 0.010),
    "GH": (0.74, -0.040, 0.000, 0.030, 0.060, 0.060, -0.040, 0.000, 0.040, 0.010),
    "SM": (0.13, -0.020, -0.030, -0.040, -0.070, -0.010, 0.060, 0.000, 0.010, 0.000),
    "BD": (0.20, -0.045, -0.060, 0.000, 0.010, 0.030, 0.020, 0.005, 0.035, 0.000),
    "VL": (0.36, 0.010, 0.030, 0.050, 0.110, -0.020, -0.040, 0.020, 0.050, 0.010),
    "FS": (0.18, -0.015, 0.010, -0.040, -0.070, -0.070, 0.080, 0.010, -0.010, -0.020),
}
REGION_SHIFT = {"score": [0.0, 0.05, -0.04, 0.02, 0.06, 0.10], "pct": [0.0, 0.005, -0.006, 0.004, 0.008, 0.012]}

# Mode among completes: logit of answering online.
MODE = dict(base=-2.50, letter_a=4.60, age=-0.30, post=0.25, deg=0.55, emp=0.25, rent=0.05, away=0.90, online=0.95)
# Response (a complete by either mode) among eligible households: logit, the letter has no part in it.
RESP = dict(base=0.42, age=0.12, post=0.10, deg=0.20, emp=-0.05, rent=-0.25, away=-0.20, online=0.05)

ELIGIBILITY = [("4.1", 0.052), ("4.2", 0.012), ("4.3", 0.008)]   # vacant, not a private dwelling, not found
