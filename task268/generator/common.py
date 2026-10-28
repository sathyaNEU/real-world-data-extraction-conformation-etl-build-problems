"""Shared constants for task268: Heronmere Health, its five hospitals, the heart failure registry and the 2027
early-diagnosis programme."""
import datetime as dt

ORG = "Heronmere Health"
ORG_INC = "Heronmere Health, Inc."
REGISTRY = "Heronmere Heart Failure Registry"
COMMITTEE = "Heart and Vascular Service Line Committee"
PEOPLE = {"epi": "Louis Harrington", "director": "Megan Swanson"}

# the five hospitals: code, name, county (real Florida counties, used only to place the fictional hospitals)
HOSPITALS = [("FEN", "Fennick General Hospital", "Pinellas"), ("LIN", "Linmoor Hospital", "Pasco"),
             ("BRE", "Brenmoor Regional Medical Center", "Hernando"), ("GUL", "Gullhaven Hospital", "Citrus"),
             ("WRE", "Wrenhaven Medical Center", "Hillsborough")]
CODES = [h[0] for h in HOSPITALS]
NAME = {h[0]: h[1] for h in HOSPITALS}
SHORT = {"FEN": "Fennick", "LIN": "Linmoor", "BRE": "Brenmoor", "GUL": "Gullhaven", "WRE": "Wrenhaven"}
COUNTY = {h[0]: h[2] for h in HOSPITALS}
SATELLITE = ("BRN", "Brenmoor Regional Medical Center, North Campus")   # shared BRE's code until 1 July 2024
SPLIT = dt.date(2024, 7, 1)

COHORT = (dt.date(2022, 1, 1), dt.date(2023, 12, 31))   # the programme charter's cohort
YEARS_ENROLLED = (2022, 2023, 2024, 2025)
MIGRATION = dt.date(2024, 6, 1)        # the record-number migration to the new electronic record
MODULE_UPDATE = dt.date(2024, 11, 18)  # a registry module update overwrote diagnosis dates from the problem list
MODULE_FIX = dt.date(2025, 2, 3)       # the release that stopped it
RECONSENT = dt.date(2025, 5, 1)        # Wrenhaven's re-consent: patients who had not returned the form left follow-up
DEATHS_TO = dt.date(2025, 12, 31)      # both death sources are complete to this date
EXTRACT = dt.date(2026, 3, 31)         # the registry extract
LAB_FROM, LAB_TO = dt.date(2025, 1, 1), dt.date(2026, 1, 6)   # the laboratory export: results released in this window
CHARTER_DATE = dt.date(2026, 2, 17)
MANUAL_DATE = dt.date(2025, 3, 3)
PACK_DATE = dt.date(2026, 4, 14)
REFERRAL = 400                          # pg/mL, the programme's referral level for NT-proBNP

EXCHANGE = "Southeast Tri-State Vital Records Exchange"
EXCHANGE_STATES = ("GA", "AL", "SC")
STATES_NORTH = ["NY", "NJ", "PA", "OH", "MI", "IL", "MA", "CT", "IN", "WI", "MD", "MN", "VA", "NC", "TN", "KY"]
STATE_W = [16, 9, 10, 12, 11, 8, 6, 4, 5, 4, 3, 3, 3, 3, 2, 2]

CLASSES = ["I", "II", "III", "IV"]
# the class as each era writes it: the legacy record (to 31 May 2024) and the new record (from 1 June 2024)
SPELL_LEGACY = {0: ["I", "Class I"], 1: ["II", "Class II"], 2: ["III", "Class III"], 3: ["IV", "Class IV"]}
SPELL_NEW = {0: ["1", "NYHA 1"], 1: ["2", "NYHA 2"], 2: ["3", "NYHA 3"], 3: ["4", "NYHA 4"]}

FILES = {
    "patients": "hf_registry_patients.csv",
    "visits": "hf_registry_visits_2022_2026.csv",
    "events": "hf_registry_followup_events.csv",
    "fl_deaths": "fl_death_linkage_2022_2025.xlsx",
    "exchange": "tristate_exchange_deaths_2022_2025.txt",
    "crosswalk": "mrn_crosswalk_2024.csv",
    "hospitals": "hospital_reference.xlsx",
    "lab": "ntprobnp_results_2025.csv",
    "charter": "hf_early_diagnosis_programme_charter_2027.pdf",
    "manual": "hf_registry_manual_v5.pdf",
    "echo": "echo_lab_activity_2025.xlsx",
    "clinics": "hf_clinic_sessions_2026.csv",
    "contents": "pack_contents.txt",
}
DISTRACTORS = ["echo", "clinics"]

CHARTER_CLAUSES = {"host": "3.1", "survival": "3.2", "referral": "2.3"}
MANUAL_SECTIONS = {"enrolment": "2.1", "hospital": "2.2", "spelling": "3.2", "relocation": "3.3", "florida": "4.1",
                   "exchange": "4.2", "no_source": "4.3", "reconsent": "4.4"}
