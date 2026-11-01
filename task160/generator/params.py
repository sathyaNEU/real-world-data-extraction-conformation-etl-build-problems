"""Fixed parameters of the Quillfield Regional Medical Center world (task160, architecture 2)."""
import datetime as dt

SEED = 169
SIM_START = dt.date(2024, 12, 1)       # admissions simulated from here so the house is full on 1 January 2025
LOG_START = dt.date(2025, 1, 1)        # first day of the alert history extract
LOG_END = dt.date(2026, 10, 25)        # last day of every Quillfield extract (a Sunday)
PILOT_LIVE = dt.date(2024, 9, 9)       # package live on 7W, 5E and 8N
BG_START = dt.date(2026, 7, 6)         # package in background mode on every other adult unit
GO_LIVE = dt.date(2027, 1, 4)          # hospital-wide go-live, Monday
FC_START, FC_END = dt.date(2027, 1, 4), dt.date(2027, 4, 4)   # the thirteen weeks forecast
Q3_START, Q3_END = dt.date(2026, 7, 1), dt.date(2026, 9, 30)  # the asks' quarter
# the renovation decant: each pair of ward teams exchanges wings (and bed locations) from the date shown
DECANT = [(dt.datetime(2026, 7, 20, 7, 0), "4N", "4S"), (dt.datetime(2026, 8, 3, 7, 0), "9E", "9W"),
          (dt.datetime(2026, 8, 17, 7, 0), "10N", "10S"), (dt.datetime(2026, 8, 31, 7, 0), "6E", "6W"),
          (dt.datetime(2026, 9, 14, 7, 0), "11N", "11S")]
FC_SIM_START = dt.date(2026, 12, 13)

# code, name, type, admissions a day, mean length of stay (days), pilot unit
UNITS = [
    ("7W", "7 West Oncology", "onc", 4.2, 5.2, True),
    ("5E", "5 East Cardiology", "card", 6.0, 3.6, True),
    ("8N", "8 North Palliative and Supportive Care", "pall", 2.4, 6.0, True),
    ("4N", "4 North Medicine", "med", 7.4, 4.0, False),
    ("4S", "4 South Medicine", "med", 5.2, 4.0, False),
    ("9E", "9 East Medicine", "med", 7.0, 4.2, False),
    ("9W", "9 West Medicine", "med", 4.6, 4.2, False),
    ("2N", "2 North Medicine", "med", 6.2, 3.8, False),
    ("12N", "12 North Medicine", "med", 5.6, 4.1, False),
    ("11N", "11 North Geriatrics", "ger", 4.6, 5.0, False),
    ("11S", "11 South Pulmonary", "pulm", 5.0, 4.4, False),
    ("3E", "3 East Stroke and Spine", "neuro", 5.2, 4.3, False),
    ("3W", "3 West Renal", "renal", 4.2, 4.6, False),
    ("6E", "6 East Orthopaedics", "ortho", 7.8, 3.1, False),
    ("6W", "6 West General Surgery", "surg", 7.2, 3.6, False),
    ("10N", "10 North Surgery", "surg", 8.0, 3.4, False),
    ("10S", "10 South Surgery", "surg", 5.4, 3.4, False),
    ("5W", "5 West Vascular Surgery", "surg", 5.0, 3.9, False),
]
PILOT = [u[0] for u in UNITS if u[5]]
LIVE_UNITS = [u[0] for u in UNITS if not u[5]]

# by unit type: P(PRN opioid), P(second PRN opioid | first), P(sedative), P(second sedative | first),
# P(anticoagulant), P(NSAID), P(QT drug), P(second QT drug | first)
PROP = {
    "onc": (0.70, 0.42, 0.36, 0.18, 0.24, 0.08, 0.68, 0.40),
    "card": (0.38, 0.22, 0.28, 0.12, 0.55, 0.10, 0.50, 0.36),
    "pall": (0.90, 0.52, 0.56, 0.26, 0.15, 0.10, 0.66, 0.34),
    "med": (0.52, 0.365, 0.4, 0.18, 0.3, 0.15, 0.58, 0.299),
    "ger": (0.48, 0.347, 0.44, 0.2, 0.38, 0.1, 0.56, 0.299),
    "pulm": (0.46, 0.347, 0.44, 0.18, 0.28, 0.12, 0.64, 0.331),
    "neuro": (0.42, 0.315, 0.38, 0.16, 0.3, 0.1, 0.52, 0.278),
    "renal": (0.46, 0.347, 0.36, 0.16, 0.34, 0.04, 0.54, 0.267),
    "ortho": (0.92, 0.461, 0.36, 0.14, 0.45, 0.3, 0.56, 0.225),
    "surg": (0.88, 0.443, 0.36, 0.14, 0.4, 0.25, 0.66, 0.246),
}
# winter is busier; the volume plan carries the same shape
SEASON = {1: 1.04, 2: 1.04, 3: 1.02, 4: 1.00, 5: 0.99, 6: 0.98, 7: 0.98, 8: 0.98, 9: 0.99, 10: 1.00, 11: 1.01,
          12: 1.01}

DRUGS = {
    "OPI": ["oxycodone 5 mg tablet PRN", "hydromorphone 0.5 mg injection PRN", "morphine 2 mg injection PRN",
            "hydrocodone-acetaminophen 5-325 mg tablet PRN", "oxycodone 10 mg tablet PRN"],
    "SED": ["lorazepam 0.5 mg tablet", "alprazolam 0.25 mg tablet", "zolpidem 5 mg tablet", "temazepam 15 mg capsule",
            "diazepam 5 mg tablet"],
    "ACG": ["warfarin 5 mg tablet", "apixaban 5 mg tablet", "rivaroxaban 20 mg tablet"],
    "NSA": ["ibuprofen 600 mg tablet", "ketorolac 15 mg injection", "naproxen 500 mg tablet"],
    "QTP": ["ondansetron 4 mg injection", "haloperidol 2 mg injection", "levofloxacin 750 mg tablet",
            "azithromycin 500 mg tablet", "quetiapine 25 mg tablet"],
    "OTH": ["cefazolin 2 g injection", "metoprolol tartrate 25 mg tablet", "furosemide 40 mg injection",
            "insulin lispro sliding scale", "pantoprazole 40 mg tablet", "vancomycin 1250 mg injection",
            "potassium chloride 20 mEq tablet", "lisinopril 10 mg tablet", "gabapentin 300 mg capsule",
            "sertraline 50 mg tablet", "amlodipine 5 mg tablet", "piperacillin-tazobactam 4.5 g injection",
            "prednisone 20 mg tablet", "atorvastatin 40 mg tablet", "metformin 500 mg tablet"],
}

# rules, severity, and the share of each answered by removing the order (MAX_DOSE answered by modifying it)
RULES = {
    "DDI_SEVERE": ("Drug-drug interaction, severe", "High"),
    "DRUG_ALLERGY": ("Drug allergy or cross-sensitivity", "High"),
    "MAX_DOSE": ("Maximum dose exceeded", "High"),
    "DDI_MODERATE": ("Drug-drug interaction, moderate", "Moderate"),
    "MSP26_DUP_OPIOID_PRN": ("Duplicate PRN opioid therapy", "Moderate"),
    "MSP26_QT_COMBO": ("QT-prolonging drug combination", "High"),
}
P_REMOVE = {"DDI_SEVERE": 0.12, "DRUG_ALLERGY": 0.30, "MAX_DOSE": 0.0, "DDI_MODERATE": 0.03,
            "MSP26_DUP_OPIOID_PRN": 0.46, "MSP26_QT_COMBO": 0.42}
P_MODIFY = {"MAX_DOSE": 0.55}
P_ALLERGY = 0.008
P_DOSE = 0.010
LAMBDA_OTHER = 0.42      # alerting non-class orders per encounter
OTHER_MIX = (("DDI_MODERATE", 0.62), ("DRUG_ALLERGY", 0.22), ("MAX_DOSE", 0.16))

REVIEW_RULES = {"DDI_SEVERE", "DRUG_ALLERGY", "MAX_DOSE", "MSP26_QT_COMBO"}
EXISTING_HIGH = {"DDI_SEVERE", "DRUG_ALLERGY", "MAX_DOSE"}
SEVERE_PAIRS = {("OPI", "SED"), ("SED", "OPI"), ("ACG", "NSA"), ("NSA", "ACG")}

# the desk
SHIFTS = (("Day", 7, 15), ("Evening", 15, 23), ("Night", 23, 7))
P_RETURN = 0.05
QUEUE_SALT = 352
