"""task130 constants and helpers shared by every generator module.

Corvane Health (fictional), western Oregon: three hospitals and an employed medical group moving their employed
clinicians' professional liability from commercial occurrence policies into the new Corvane Professional Liability
Trust, claims-made, each on its policy's anniversary in 2027."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np

SEED = 1301012           # payroll world, documents, asks
CLAIMS_SEED = 0          # the claims world's own stream; set by build.py from SEED_CHOICE
SEED_CHOICE = 0

# Calendar of the fiction
VALUATION = dt.date(2026, 9, 30)          # claims register valuation date
REGISTER_RUN = dt.date(2026, 10, 2)       # register extract run (Friday)
HCM_RUN = dt.date(2026, 10, 2)            # HCM pay line extract run
LEGACY_FIRST, LEGACY_LAST = (2016, 1), (2025, 12)   # legacy payroll history in the pack
HCM_FIRST, HCM_LAST = (2026, 1), (2026, 9)
WORLD_FIRST = (2012, 1)                   # the simulation starts here (claims from older incidents are in the register)
ERP_START = dt.date(2015, 9, 1)           # the Early Resolution Program takes requests from this date
EXPERIENCE = (dt.date(2016, 1, 1), dt.date(2024, 12, 31))
PLAN_YEAR = 2027
PLAN_START, PLAN_END = dt.date(2027, 1, 1), dt.date(2027, 12, 31)
TREND = 0.05
MEETING = dt.date(2026, 11, 10)           # trustees set the 2027 contribution
CODE_SWITCH = (2020, 7)                   # legacy job architecture: 2020 code set from July 2020
MOVE_DATE = dt.date(2026, 10, 1)          # the October 2026 moves (after the asks' months)
LIMIT_PER_CLAIM = 2_000_000

COMPANY = "Corvane Health"
TRUST = "Corvane Professional Liability Trust"
CARRIERS = {
    "QM": "Quillan Mutual Professional Liability Company",
    "SC": "Stoneleigh Casualty Insurance Company",
    "HL": "Halberd Hospital Mutual Insurance Company",
    "CL": "Corrigan Lane Indemnity Company",
    "WP": "Westerholm Physicians Exchange",
    "TR": "Tallis Reciprocal Insurance Exchange",
}
# entity code: name, GL company, transition date, carrier, register coverage line, policy anniversary month,
# policy number pattern (by the policy year's start year), affiliation date
ENTITIES = {
    "TFH": dict(name="Tolliver Falls Hospital", company="120", transition=dt.date(2027, 1, 1), carrier="QM",
                line="QM-TFH", anniv=1, policy="QM-HPL-{yy}-0{n}", base_n=4172, joined=None,
                former="HL", carrier_from=dt.date(2021, 1, 1), former_policy="HHM-{yy}-17{n}",
                disclosure_from=dt.date(2019, 3, 1)),
    "AMC": dict(name="Alderwick Medical Center", company="110", transition=dt.date(2027, 4, 1), carrier="QM",
                line="QM-AMC", anniv=4, policy="QM-HPL-{yy}-0{n}", base_n=4406, joined=None,
                former="CL", carrier_from=dt.date(2019, 4, 1), former_policy="CLI-PL-{yy}{n}",
                disclosure_from=dt.date(2019, 1, 1)),
    "CMG": dict(name="Corvane Medical Group", company="300", transition=dt.date(2027, 7, 1), carrier="SC",
                line="SC-CMG", anniv=7, policy="SC-PPL-0091877-{yy}", base_n=0, joined=None,
                former="WP", carrier_from=dt.date(2019, 7, 1), former_policy="WPX-0{n}-{yy}",
                disclosure_from=dt.date(2019, 5, 1)),
    "BCH": dict(name="Brennick Community Hospital", company="140", transition=dt.date(2027, 10, 1), carrier="SC",
                line="SC-BCH", anniv=10, policy="SC-HPL-0102265-{yy}", base_n=0, joined=dt.date(2019, 7, 1),
                former="TR", carrier_from=dt.date(2022, 10, 1), former_policy="TRE-HPL-{yy}-{n}",
                disclosure_from=dt.date(2019, 7, 1)),
}
ENTITY_ORDER = ["TFH", "AMC", "CMG", "BCH"]

CLASSES = ["OB", "SUR", "EM", "AN", "HM", "PC", "APC"]
CLASS_NAME = {"OB": "Obstetrics", "SUR": "Surgery", "EM": "Emergency Medicine", "AN": "Anesthesiology",
              "HM": "Hospital and Medical Specialties", "PC": "Primary Care", "APC": "Advanced Practice"}

# jobs: key, 2016 code, 2020 code, payroll title, class (None: not a Covered Clinician), HCM profiles, FTE mix
JOBS = [
    ("OBG", "21410", "PHY-OBG", "Physician - Obstetrics and Gynecology", "OB",
     [("JP-20141", "Physician, Obstetrics & Gynecology")], "phys"),
    ("OBL", "21420", "PHY-OBL", "Physician - OB Hospitalist", "OB", [("JP-20142", "Physician, OB Hospitalist")], "hosp"),
    ("MFM", "21415", "PHY-MFM", "Physician - Maternal-Fetal Medicine", "OB",
     [("JP-20143", "Physician, Maternal-Fetal Medicine")], "phys"),
    ("GSU", "21510", "PHY-GSU", "Physician - General Surgery", "SUR", [("JP-20151", "Physician, General Surgery")], "phys"),
    ("ORT", "21520", "PHY-ORT", "Physician - Orthopaedic Surgery", "SUR",
     [("JP-20152", "Physician, Orthopaedic Surgery")], "phys"),
    ("URO", "21530", "PHY-URO", "Physician - Urology", "SUR", [("JP-20153", "Physician, Urology")], "phys"),
    ("ENT", "21540", "PHY-ENT", "Physician - Otolaryngology", "SUR", [("JP-20154", "Physician, Otolaryngology")], "phys"),
    ("VAS", "21550", "PHY-VAS", "Physician - Vascular Surgery", "SUR", [("JP-20155", "Physician, Vascular Surgery")],
     "phys"),
    ("EMR", "21610", "PHY-EMR", "Physician - Emergency Medicine", "EM",
     [("JP-20161", "Physician, Emergency Medicine"), ("JP-20162", "Physician, Emergency Medicine Nocturnist")], "hosp"),
    ("ANE", "21710", "PHY-ANE", "Physician - Anesthesiology", "AN", [("JP-20171", "Physician, Anesthesiology")], "hosp"),
    ("HOS", "21810", "PHY-HOS", "Physician - Hospitalist", "HM",
     [("JP-20181", "Physician, Hospital Medicine"), ("JP-20182", "Physician, Hospitalist Nocturnist")], "hosp"),
    ("CCM", "21820", "PHY-CCM", "Physician - Critical Care", "HM", [("JP-20183", "Physician, Critical Care Medicine")],
     "hosp"),
    ("CAR", "21830", "PHY-CAR", "Physician - Cardiology", "HM", [("JP-20184", "Physician, Cardiology")], "phys"),
    ("GAS", "21840", "PHY-GAS", "Physician - Gastroenterology", "HM", [("JP-20185", "Physician, Gastroenterology")],
     "phys"),
    ("ONC", "21850", "PHY-ONC", "Physician - Hematology/Oncology", "HM",
     [("JP-20186", "Physician, Hematology & Oncology")], "phys"),
    ("NEU", "21860", "PHY-NEU", "Physician - Neurology", "HM", [("JP-20187", "Physician, Neurology")], "phys"),
    ("RAD", "21870", "PHY-RAD", "Physician - Radiology", "HM", [("JP-20188", "Physician, Diagnostic Radiology")], "hosp"),
    ("PSY", "21880", "PHY-PSY", "Physician - Psychiatry", "HM", [("JP-20189", "Physician, Psychiatry")], "phys"),
    ("FAM", "21910", "PHY-FAM", "Physician - Family Medicine", "PC", [("JP-20191", "Physician, Family Medicine")], "clin"),
    ("INT", "21920", "PHY-INT", "Physician - Internal Medicine", "PC", [("JP-20192", "Physician, Internal Medicine")],
     "clin"),
    ("PED", "21930", "PHY-PED", "Physician - Pediatrics", "PC", [("JP-20193", "Physician, Pediatrics")], "clin"),
    ("NP", "31110", "APC-NP", "Nurse Practitioner", "APC",
     [("JP-30111", "Nurse Practitioner"), ("JP-30115", "Nurse Practitioner, Lead")], "clin"),
    ("PA", "31120", "APC-PA", "Physician Assistant", "APC", [("JP-30112", "Physician Assistant")], "clin"),
    ("CRNA", "31130", "APC-CRNA", "Nurse Anesthetist (CRNA)", "APC",
     [("JP-30113", "Certified Registered Nurse Anesthetist")], "hosp"),
    ("CNM", "31140", "APC-CNM", "Certified Nurse Midwife", "APC", [("JP-30114", "Certified Nurse Midwife")], "clin"),
    ("RES", "25010", "GME-RES", "Resident Physician", None,
     [("JP-40101", "Resident Physician"), ("JP-40102", "Chief Resident")], "res"),
    ("FEL", "25020", "GME-FEL", "Clinical Fellow", None,
     [("JP-40103", "Physician, Cardiology Fellow"), ("JP-40104", "Physician, Critical Care Fellow")], "res"),
    ("PSYC", "32110", "BHV-PSY", "Psychologist", None, [("JP-50110", "Psychologist, Clinical")], "clin"),
]
JOB = {j[0]: j for j in JOBS}
CODE16 = {j[1]: j[0] for j in JOBS}
CODE20 = {j[2]: j[0] for j in JOBS}
CLASS_OF_JOB = {j[0]: j[4] for j in JOBS}
COVERED_JOBS = [j[0] for j in JOBS if j[4]]

# Departments (cost centre suffix, name, the jobs it holds) by entity
DEPTS = {
    "AMC": [("6105", "Obstetrics and Gynecology", ["OBG", "OBL", "MFM", "CNM"]),
            ("6210", "General Surgery", ["GSU"]), ("6220", "Orthopaedics", ["ORT"]), ("6230", "Urology", ["URO"]),
            ("6240", "Otolaryngology", ["ENT"]), ("6250", "Vascular Surgery", ["VAS"]),
            ("6310", "Emergency Medicine", ["EMR"]), ("6410", "Anesthesiology", ["ANE", "CRNA"]),
            ("6510", "Hospital Medicine", ["HOS"]), ("6520", "Critical Care", ["CCM"]), ("6530", "Cardiology", ["CAR"]),
            ("6535", "Gastroenterology", ["GAS"]), ("6540", "Oncology", ["ONC"]), ("6545", "Neurology", ["NEU"]),
            ("6550", "Diagnostic Imaging", ["RAD"]), ("6560", "Inpatient Psychiatry", ["PSY"]),
            ("6610", "Hospital APC Services", ["NP", "PA"]), ("6910", "Graduate Medical Education", ["RES", "FEL"])],
    "TFH": [("6105", "Women's Services", ["OBG", "OBL", "CNM"]), ("6210", "Surgical Services", ["GSU", "URO", "ENT"]),
            ("6220", "Orthopaedics", ["ORT"]), ("6310", "Emergency Department", ["EMR"]),
            ("6410", "Anesthesia", ["ANE", "CRNA"]), ("6510", "Hospital Medicine", ["HOS"]),
            ("6520", "Intensive Care", ["CCM"]), ("6530", "Cardiology", ["CAR"]), ("6550", "Imaging", ["RAD"]),
            ("6610", "Hospital APC Services", ["NP", "PA"]), ("6910", "Family Medicine Residency", ["RES"])],
    "BCH": [("6210", "Surgery", ["GSU", "ORT"]), ("6310", "Emergency Department", ["EMR"]),
            ("6410", "Anesthesia", ["ANE", "CRNA"]), ("6510", "Hospital Medicine", ["HOS", "CAR"]),
            ("6550", "Imaging", ["RAD"]), ("6610", "APC Services", ["NP", "PA"]),
            ("7110", "Brennick Rural Health Clinic", ["FAM"])],
    "CMG": [("7110", "Alderwick Family Medicine", ["FAM", "NP", "PA"]),
            ("7115", "North Valley Family Medicine", ["FAM", "NP", "PA"]),
            ("7120", "Tolliver Falls Family Practice", ["FAM", "NP", "PA"]),
            ("7210", "Internal Medicine", ["INT", "NP", "PA"]), ("7310", "Pediatrics", ["PED", "NP"]),
            ("7410", "Women's Health", ["OBG", "MFM", "CNM", "NP"]), ("7510", "Heart and Vascular Clinic", ["CAR", "VAS", "PA"]),
            ("7520", "Digestive Health", ["GAS", "PA"]), ("7530", "Cancer Center", ["ONC", "NP"]),
            ("7540", "Neurology Clinic", ["NEU", "NP"]), ("7550", "Behavioral Health", ["PSY", "PSYC", "NP"]),
            ("7610", "Orthopaedics and Sports Medicine", ["ORT", "PA"]), ("7620", "Urology Clinic", ["URO", "PA"]),
            ("7630", "Ear, Nose and Throat", ["ENT", "PA"]), ("7640", "General Surgery Clinic", ["GSU", "PA"]),
            ("7810", "Ambulatory Surgery Center", ["CRNA"]), ("7020", "After Hours Care", ["FAM", "NP", "PA"])],
}


def cost_centre(entity, suffix):
    return "%s-%s" % (ENTITIES[entity]["company"], suffix)


def stream(*keys) -> np.random.Generator:
    """One RNG stream per named component, seeded by blake2b so no process salt reaches it."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8)
    return np.random.default_rng(int.from_bytes(h.digest(), "big"))


def claims_stream(*keys) -> np.random.Generator:
    h = hashlib.blake2b(("claims|%d|" % CLAIMS_SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8)
    return np.random.default_rng(int.from_bytes(h.digest(), "big"))


def months(first, last):
    y, m = first
    out = []
    while (y, m) <= last:
        out.append((y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def days_in_month(y, m):
    nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
    return (nxt - dt.date(y, m, 1)).days


def month_key(y, m):
    return "%04d-%02d" % (y, m)


def trend_factor(incident_year):
    return (1 + TREND) ** (PLAN_YEAR - incident_year)


def carrier_on(entity, d):
    """The carrier whose occurrence policy covered the entity's clinicians on date d."""
    e = ENTITIES[entity]
    return e["carrier"] if d >= e["carrier_from"] else e["former"]


def policy_number(entity, d):
    """The occurrence policy in force on date d for the entity's clinicians (annual, on the anniversary)."""
    e = ENTITIES[entity]
    start_year = d.year if d.month >= e["anniv"] else d.year - 1
    yy = "%02d" % (start_year % 100)
    if carrier_on(entity, d) != e["carrier"]:
        return e["former_policy"].format(yy=yy, n={"TFH": 41 + start_year % 7, "AMC": 3306 + 11 * (start_year - 2010),
                                                   "CMG": 7712, "BCH": 205 + start_year % 9}[entity])
    if e["carrier"] == "QM":
        return e["policy"].format(yy=yy, n=e["base_n"] + 37 * (start_year - 2010))
    return e["policy"].format(yy=yy)


def policy_period(entity, d):
    e = ENTITIES[entity]
    start_year = d.year if d.month >= e["anniv"] else d.year - 1
    return dt.date(start_year, e["anniv"], 1), dt.date(start_year + 1, e["anniv"], 1)


# The pack's files (target/), in Corvane's own naming
REGISTER = "rm_claims_register_extract_20261002.csv"
PAYROLL = "clinician_fte_by_month_2016-01_2025-12.csv"
HCM = "hcm_clinician_pay_lines_2026-01_2026-09.csv"
CROSSWALK = "hcm_job_profile_crosswalk.csv"
DIRECTORY = "cost_centre_directory_2026.csv"
PLAN = "clinician_staffing_plan_2027.xlsx"
AGREEMENT = "CPLT_trust_agreement_executed_2026-08-14.pdf"
POLICY = "CPLT_funding_policy_adopted_2026-09-22.pdf"
QM_SEP = "QMPL_loss_run_Corvane_val_2026-09-30.xlsx"
QM_JUN = "QMPL_loss_run_Corvane_val_2026-06-30_rev1.xlsx"
SC_SEP = "Stoneleigh_lossrun_CORVANE_20260930.csv"
NOTICES = "rm_carrier_notices_2012_2026.csv"
SAFETY = "patient_safety_events_2019-01_2026-09.csv"
INVOICES = "defense_panel_invoices_2026Q3.csv"
PREMIUMS = "insurance_premium_history_2016-2026.xlsx"
DICTIONARY = "data_dictionary_rm_extracts.md"
EXTRACT_LOG = "extract_log_2026-10.csv"
DISTRACTORS = (SAFETY, INVOICES)
DELIVERABLES = ("trust_funding_2027.xlsx", "trustees_paper_2027.pptx")

PEOPLE = {"requester": "Nancy Holland", "cfo": "Derek White", "claims": "Lori Williams", "chair": "Walter Butler"}
