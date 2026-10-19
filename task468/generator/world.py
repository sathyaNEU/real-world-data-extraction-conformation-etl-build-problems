"""The world of task468 (architecture 2): Merrow Health Plan's specialty pharmacy benefit, its two pharmacy benefit
managers (Orrin Rx to December 2025, Tallis Pharmacy Services from January 2026), the specialty classes its Specialty
Clinical Pharmacy Program manages, and the program's staffing standard for the year from 1 July 2026."""
import datetime as dt

SEED = 468
FIRST_MONTH = dt.date(2019, 1, 1)          # the claim files begin
LAST_DAY = dt.date(2026, 6, 30)            # the claims run to here; the program year begins the next day
SWITCH = dt.date(2026, 1, 1)               # Tallis takes the benefit
N_MONTHS = 90                              # January 2019 to June 2026
HORIZON = 12                               # the program year, July 2026 to June 2027
PRE_MONTHS = 84                            # members' therapy simulated from seven years before the files begin
PER_PHARMACIST = 1_500_000                 # the charter: one clinical pharmacist per $1.5 million of managed spend, or part
AS_OF = "2026-08-03"
EXEC_MEETING = dt.date(2026, 8, 4)


def month_index(d):
    return (d.year - FIRST_MONTH.year) * 12 + d.month - FIRST_MONTH.month


def month_start(i):
    y, m = divmod(FIRST_MONTH.month - 1 + i, 12)
    return dt.date(FIRST_MONTH.year + y, m + 1, 1)


# ---------------------------------------------------------------- the classes the program manages
# code: name, the starts a month (month index -> mean), the monthly chance a member stops (by months on therapy),
# fixed course (fills), loading (extra units on the first fill), days' supply options and their shares
CLASSES = {
    "IMM": dict(name="Inflammatory conditions (biologic and targeted therapy)", starts=lambda m: 9.0,
                stop=lambda t: 0.035 if t < 12 else 0.012, load=2.0, supply=((28, 0.85), (84, 0.15))),
    "MS": dict(name="Multiple sclerosis", starts=lambda m: 2.4, stop=lambda t: 0.02 if t < 12 else 0.008, load=1.0,
               supply=((30, 0.7), (90, 0.3))),
    "ONC": dict(name="Oral oncology", starts=lambda m: 7.0, stop=lambda t: 0.16 if t < 6 else 0.03, load=1.0,
                supply=((30, 1.0),)),
    "HCV": dict(name="Hepatitis C", starts=lambda m: 30.0 if 76 <= m < 90 else 6.0, stop=lambda t: 0.02, load=1.0,
                course=(2, 3), supply=((28, 1.0),)),
    "GLP": dict(name="Weight management (GLP-1 receptor agonists)",
                starts=lambda m: 380.0 if m >= 84 else (30.0 if m >= 48 else 0.0),
                stop=lambda t: 0.18 if t < 6 else 0.025, load=1.0, supply=((28, 0.9), (84, 0.1))),
    "HIV": dict(name="HIV", starts=lambda m: 3.4, stop=lambda t: 0.006, load=1.0, supply=((30, 0.6), (90, 0.4))),
    "AST": dict(name="Severe asthma (biologics)", starts=lambda m: 40.0 if m >= 84 else 5.0,
                stop=lambda t: 0.15 if t < 9 else 0.015, load=2.0, supply=((28, 1.0),)),
    "CF": dict(name="Cystic fibrosis", starts=lambda m: 0.25, stop=lambda t: 0.003, load=1.0, supply=((28, 1.0),)),
    "CGR": dict(name="Migraine prevention (CGRP)", starts=lambda m: 150.0 if m >= 84 else 18.0,
                stop=lambda t: 0.2 if t < 6 else 0.03, load=1.0, supply=((30, 0.85), (90, 0.15))),
}
CANDIDATES = list(CLASSES)
STEP_THERAPY_REMOVED = ("GLP", "AST", "CGR")   # the January 2026 formulary change
OUTREACH_START = dt.date(2025, 5, 1)           # the hepatitis C outreach drive
RESTART = {"IMM": 0.12, "MS": 0.10, "ONC": 0.05, "HCV": 0.0, "GLP": 0.12, "HIV": 0.15, "AST": 0.10, "CF": 0.10,
           "CGR": 0.10}                       # a stopped member's chance of a later episode in the class
RETURN_FROM = 48                               # members of the step-therapy classes who stopped from January 2023
RETURN_WAVE = {"GLP": 0.60, "AST": 0.60, "CGR": 0.60}   # ... and came back January to June 2026
REBATE_2024 = 0.91                             # the 2024 contract year's rebate per unit against 2025's

# products: class, product name, labeler, product code, package, units per 28 or 30 days, 2026 price per unit, share,
# the package code a long (84- or 90-day) supply is dispensed in, and the manufacturer's rebate per unit dispensed in 2025
PRODUCTS = [
    ("IMM", "Ravelta 40 mg/0.4 mL pen", "71842", "0215", "02", 2, 1675.69, 0.45, "06", 431.70),
    ("IMM", "Ostinza 150 mg/mL pen", "71842", "0331", "01", 1, 3361.60, 0.30, "03", 812.40),
    ("IMM", "Cordafin 15 mg tablet", "60371", "0712", "30", 28, 121.19, 0.25, "90", 22.65),
    ("MS", "Velmira 20 mg/mL syringe", "60371", "0920", "28", 12, 355.52, 0.55, "36", 61.10),
    ("MS", "Antrelle 0.25 mg capsule", "68594", "0104", "30", 30, 149.19, 0.45, "90", 24.85),
    ("ONC", "Tessarib 100 mg tablet", "68594", "0451", "30", 30, 257.23, 0.5, None, 9.40),
    ("ONC", "Lonquivir 40 mg tablet", "70135", "0218", "60", 60, 141.32, 0.5, None, 5.15),
    ("HCV", "Sofivela 400/100 mg tablet", "70135", "0607", "28", 28, 228.60, 1.0, None, 71.90),
    ("GLP", "Semavex 2.4 mg/0.75 mL pen", "73299", "0124", "04", 4, 192.56, 0.6, "12", 58.35),
    ("GLP", "Tirzelor 10 mg/0.5 mL pen", "73299", "0287", "04", 4, 202.48, 0.4, "12", 49.80),
    ("HIV", "Bictavir 50/200/25 mg tablet", "61958", "0901", "30", 30, 62.12, 0.7, "90", 6.05),
    ("HIV", "Dovarine 50/300 mg tablet", "61958", "0802", "30", 30, 52.84, 0.3, "90", 3.90),
    ("AST", "Mepozum 100 mg/mL pen", "66415", "0310", "01", 1, 1854.67, 0.6, None, 512.20),
    ("AST", "Dupelta 300 mg/2 mL pen", "66415", "0440", "02", 2, 1784.11, 0.4, None, 447.65),
    ("CF", "Elexavor 100/50/75 mg tablet", "51167", "0331", "84", 84, 102.84, 1.0, None, 4.10),
    ("CGR", "Erelmab 70 mg/mL pen", "55513", "0841", "01", 1, 1244.11, 0.55, "03", 243.15),
    ("CGR", "Fremavo 225 mg/1.5 mL syringe", "55513", "0902", "01", 1, 1222.27, 0.45, "03", 231.70),
]
DISPENSING_FEE = 5.00                      # the 2026 schedule, per fill
ORRIN_PRICE_FACTOR = {2019: 0.86, 2020: 0.89, 2021: 0.91, 2022: 0.94, 2023: 0.97, 2024: 1.00, 2025: 1.03}   # Orrin's paid unit cost against Tallis 2026

MEMBERS = 482_000                          # the plan's members, June 2026

# ---------------------------------------------------------------- organisations, people, files
PLAN = "Merrow Health Plan"
OLD_PBM = "Orrin Rx"
NEW_PBM = "Tallis Pharmacy Services"
PROGRAM = "Specialty Clinical Pharmacy Program"
PEOPLE = {"director": "Erik Marks", "analyst": "John Henry", "account": "Caleb Fischer"}
TITLES = {"director": "Director of Pharmacy, Merrow Health Plan",
          "analyst": "Pharmacy Data Analyst, Merrow Health Plan",
          "account": "Account Manager, Tallis Pharmacy Services"}

FILES = {
    "orrin": "orrin_rx_specialty_claims_2019_2025.csv",
    "tallis": "tallis_specialty_claims_2026h1.csv",
    "crosswalk": "member_id_crosswalk_2026.csv",
    "drugs": "tallis_specialty_drug_list_2026.csv",
    "prices": "tallis_specialty_price_schedule_2026.xlsx",
    "charter": "specialty_clinical_pharmacy_program_charter_2026.pdf",
    "bulletin": "formulary_bulletin_january_2026.pdf",
    "transition": "pbm_transition_file_notes.pdf",
    "rebates": "orrin_rx_rebate_statement_2025.xlsx",
    "trend": "orrin_rx_specialty_trend_report_2025.pdf",
    "infusions": "medical_benefit_specialty_drugs_2025.xlsx",
}
GOLDEN = {"workbook": "merrow_specialty_pharmacist_staffing_2026_27.xlsx"}
DISTRACTORS = ["trend", "infusions"]
