"""Fixed parameters of the Corrowan Valley Community Health world (task281, architecture 3)."""
import datetime as dt

SEED = 5327
VAL_STREAM = 37            # the validation study's own draws (enrolment, reads, grading)
ASSEMBLED = dt.datetime(2026, 11, 16, 16, 40, 0)        # every file's mtime, the in-fiction export date
ASOF = dt.date(2026, 11, 16)

ORG = "Corrowan Valley Community Health"
ORG_SHORT = "CVCH"
STATE = "Oregon"
VENDOR = "Kelvory Health Systems"
PRODUCT = "Kelvory RetinaCheck"
READING_CENTER = "Pellam Eye Reading Center"
CAMERA_MAKER = "Halvard Optics"

# the reference year the governance standard files, and the validation window
REF_START = dt.date(2025, 10, 1)
REF_END = dt.date(2026, 9, 30)
VAL_START = dt.date(2025, 1, 13)
VAL_END = dt.date(2025, 8, 22)

# the vendor's operating points: a screen refers when its DR score is at or above the cutoff, or it is ungradable
OPS = [("Standard", 50), ("Enhanced", 42), ("High", 34), ("Maximum", 26)]
FLOOR = 0.85                 # governance standard: sensitivity at least 85 per cent at the clinic
OVERREAD_CAPACITY = 7500     # reading center agreement: overreads a contract year

# the AI's latent score model (score = 100 * logistic(latent))
MU_REF = {"NR-70": 1.18, "NR-40": 0.138}     # referable eyes, by camera model
MU_REF_AGE75 = -0.22                         # older referable patients score a little lower on both models
SD_REF = 0.605                               # spread of the latent among referable eyes
MU_NON = -1.40                               # non-referable
UNGRADABLE = {"NR-70": 0.036, "NR-40": 0.038}
SD_LAT = 1.0                                 # spread of the latent among non-referable eyes

# twelve clinics: code, EHR department, portal site, biomed location, annual screens, referable prevalence
CLINICS = [
    # code   EHR department name                 portal site name           biomed location   screens prev
    ("OF", "CVCH ORRIN FALLS FAMILY MED", "Orrin Falls Health Center", "LOC-112 Orrin Falls", 2610, 0.108),
    ("TB", "CVCH THISTLEBROOK CLINIC", "Thistlebrook", "LOC-118 Thistlebrook", 2190, 0.121),
    ("WM", "CVCH WENDMERE PRIMARY CARE", "Wendmere Primary Care", "LOC-121 Wendmere", 2440, 0.097),
    ("PB", "CVCH PELLSBURY HEALTH CTR", "Pellsbury Health Center", "LOC-104 Pellsbury", 2075, 0.114),
    ("QH", "CVCH QUARRY HILL MED GROUP", "Quarry Hill", "LOC-109 Quarry Hill", 2330, 0.103),
    ("RW", "CVCH ROOKWOOD FAMILY HEALTH", "Rookwood Family Health", "LOC-115 Rookwood", 1985, 0.126),
    ("SC", "CVCH SALLOW CREEK CLINIC", "Sallow Creek Clinic", "LOC-102 Sallow Creek", 2260, 0.111),
    ("VD", "CVCH VELDANE COMMUNITY CLINIC", "Veldane", "LOC-123 Veldane", 2390, 0.099),
    ("BF", "CVCH BRACKENFIELD HEALTH CTR", "Brackenfield Health Ctr", "LOC-107 Brackenfield", 2155, 0.118),
    ("YB", "CVCH YARROWBY MEDICAL", "Yarrowby Medical", "LOC-126 Yarrowby", 2480, 0.106),
    ("KN", "CVCH KESTLE ROAD FAMILY MED", "Kestle Road", "LOC-111 Kestle Road", 2035, 0.123),
    ("HM", "CVCH HOLLINMOOR CLINIC", "Hollinmoor Clinic", "LOC-129 Hollinmoor", 2365, 0.101),
]
PILOTS = {"A": "WM", "B": "QH", "C": "YB"}      # the validation study's site labels
PELLAM_SITE = {"OF": "CVCH/ORRIN FALLS", "TB": "CVCH/THISTLEBROOK", "WM": "CVCH/WENDMERE", "PB": "CVCH/PELLSBURY",
               "QH": "CVCH/QUARRY HILL", "RW": "CVCH/ROOKWOOD", "SC": "CVCH/SALLOW CRK", "VD": "CVCH/VELDANE",
               "BF": "CVCH/BRACKENFIELD", "YB": "CVCH/YARROWBY", "KN": "CVCH/KESTLE RD", "HM": "CVCH/HOLLINMOOR"}
REGISTRY_EXTRA = {"OF": 0.12, "TB": 0.31, "WM": 0.05, "PB": 0.22, "QH": 0.09, "RW": 0.27, "SC": 0.17, "VD": 0.36,
                  "BF": 0.02, "YB": 0.14, "KN": 0.25, "HM": 0.07}
OUTSIDE_RATE = {"OF": 0.27, "TB": 0.16, "WM": 0.221, "PB": 0.11, "QH": 0.244, "RW": 0.095, "SC": 0.19, "VD": 0.15,
                "BF": 0.29, "YB": 0.212, "KN": 0.182, "HM": 0.23}
VISIT_SHARE = 0.06           # screenings of patients whose home clinic is another one
MANUAL_SHARE = 0.032         # teleretinal photo sessions for patients excluded from AI screening, per AI screen
NOT_READ = 0.04              # AI referrals the reading center never received (referral cancelled)

PEOPLE = {
    "quality": "Natalie Mckinney",       # Director of Quality and Clinical AI
    "biomed": "Noah Odonnell",           # Biomedical Engineering Manager
    "grader": "Christy Francis",         # lead certified retinal grader, validation study
}

FILES = {
    "results": "retina_ai_results_2025-10_2026-09.csv",
    "validation": "local_validation_study_2025.csv",
    "protocol": "validation_study_protocol_2025.pdf",
    "assets": "biomed_asset_register_2026-09-30.xlsx",
    "standard": "clinical_ai_governance_standard_v3.pdf",
    "opspec": "retinacheck_operating_points.pdf",
    "siteconfig": "retinacheck_site_configuration_2026-10-01.json",
    "agreement": "pellam_reading_agreement_2027.pdf",
    "orders": "ehr_retinal_screening_orders_2025-26.csv",
    "directory": "clinic_directory.csv",
    "reads": "pellam_overread_log_2025-26.csv",
    "registry": "diabetes_registry_2026-09-30.csv",
    "outside": "him_outside_eye_reports_2025-26.csv",
    "tickets": "biomed_service_tickets_2025-26.csv",
    "dashboard": "retinacheck_site_dashboard_2026q3.xlsx",
    "survey": "eye_screening_patient_survey_2026.csv",
}
DISTRACTORS = ["dashboard", "survey", "outside"]
