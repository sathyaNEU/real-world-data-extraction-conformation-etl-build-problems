"""task122 generator: the fixed facts of VMK-4410-202, Varnmark Therapeutics' 52-week phase 2b of VMK-4410, an oral
aldosterone synthase inhibitor, in adults with chronic kidney disease and albuminuria, and of the draft phase 3
synopsis VMK-4410-301."""
from datetime import date

SEED = 12204410
R_SHIFT = 1241                # the randomisation list's block order
V_SHIFT = 42280                # the visit-date and withdrawal stream's seed offset
S_SHIFT = 43119                # the other stops and holds stream's seed offset
K_SHIFT = 84603               # the potassium stream's seed offset
NOISE_SEED = 3712          # the measurement-error stream
ORG = "Varnmark Therapeutics A/S"
STUDY = "VMK-4410-202"
P3 = "VMK-4410-301"
DRUG = "VMK-4410"

ARMS = ["Placebo", "VMK-4410 5 mg", "VMK-4410 10 mg", "VMK-4410 20 mg", "VMK-4410 40 mg"]
ARMCD = {"Placebo": "PBO", "VMK-4410 5 mg": "VMK5", "VMK-4410 10 mg": "VMK10", "VMK-4410 20 mg": "VMK20",
         "VMK-4410 40 mg": "VMK40"}
DOSE = {"Placebo": 0, "VMK-4410 5 mg": 5, "VMK-4410 10 mg": 10, "VMK-4410 20 mg": 20, "VMK-4410 40 mg": 40}
N_PER_ARM = 150

# Effects against placebo, in eGFR mL/min/1.73 m2: the haemodynamic fall every patient on the dose takes (H), the
# extra volume-related fall in patients already on a loop diuretic (V), the part of V that comes back when the
# diuretic is eased (RHO of V, in the patients eased), and the chronic benefit a year (C).
H = {5: 0.80, 10: 0.85, 20: 3.20, 40: 4.20}
V = {5: 0.25, 10: 0.50, 20: 1.40, 40: 6.25}
C = {5: 0.30, 10: 0.667, 20: 2.20, 40: 2.50}
# targets the arm means are calibrated to (the design note's draw): golden 36-month differences and week-52 values
GOLD_T = {5: 0.0, 10: 1.0, 20: 3.0, 40: 2.0}
W52_T = {5: -0.60, 10: -0.333, 20: -1.40, 40: -3.00}
R_T = {5: 0.0, 10: 0.0, 20: 0.15, 40: 1.40}
DIP_TAU_W = 1.2          # weeks: the fall on starting the drug develops over the first weeks
REC_TAU_W = 1.5          # weeks: the recovery after a diuretic is eased
EASE_VISITS = {12: 0.45, 16: 0.35, 20: 0.20}
PBO_SLOPE = -4.0         # placebo eGFR change a year (mean), individual sd below
SLOPE_SD = 2.0
C_SD = 0.35

# Study calendar
FIRST_RAND = date(2024, 3, 4)
LAST_RAND = date(2025, 1, 31)
LOCK = date(2026, 4, 14)
EXPORT = date(2026, 4, 15)
PACK_DATE = date(2026, 10, 12)

# Visits: (visit, number, nominal study day of the visit, window half-width in days)
VISITS = [("SCREENING", 1, -14, 7), ("DAY 1", 2, 1, 0), ("WEEK 2", 3, 15, 3), ("WEEK 4", 4, 29, 3),
          ("WEEK 8", 5, 57, 5), ("WEEK 12", 6, 85, 5), ("WEEK 16", 7, 113, 7), ("WEEK 20", 8, 141, 7),
          ("WEEK 24", 9, 169, 7), ("WEEK 32", 10, 225, 10), ("WEEK 40", 11, 281, 10), ("WEEK 52", 12, 365, 10),
          ("WEEK 56 FOLLOW-UP", 13, 393, 7)]
ON_TREAT = [v[0] for v in VISITS[1:12]]
URINE_VISITS = {"SCREENING", "DAY 1", "WEEK 4", "WEEK 12", "WEEK 24", "WEEK 52", "WEEK 56 FOLLOW-UP"}
DISPENSE = ["DAY 1", "WEEK 4", "WEEK 12", "WEEK 24", "WEEK 40"]

COUNTRIES = [("DK", "Denmark", 6, "COPENHAGEN"), ("SE", "Sweden", 5, "COPENHAGEN"), ("DE", "Germany", 12, "COPENHAGEN"),
             ("PL", "Poland", 10, "COPENHAGEN"), ("ES", "Spain", 9, "MADRID"), ("GB", "United Kingdom", 8, "MADRID")]
CENTRAL = {"COPENHAGEN": "Tavlund Central Laboratory, Copenhagen", "MADRID": "Tavlund Central Laboratory, Madrid"}

PEOPLE = {"clin_dev": "Benedicte Laursen", "biostat": "Nicolaj Lassen", "clin_pharm": "Kirsten Eriksen",
          "med_mon": "Lene Dam"}


def weekday_shift(d):
    """days to move a clinic date off the weekend: Saturday to Friday, Sunday to Monday"""
    return {5: -1, 6: 1}.get(d.weekday(), 0)
