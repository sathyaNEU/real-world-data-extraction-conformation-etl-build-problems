"""Constants for task269: Ardley Valley Hospital, its fourteen inpatient wards and six other audited areas, the
2025-26 audit year, the Foundation's 2027 coaching grant, the people, the dates and the pack's file names."""
import datetime as dt

SEED = 11
YEAR_START = dt.date(2025, 7, 1)
YEAR_END = dt.date(2026, 6, 30)
DAYS = [YEAR_START + dt.timedelta(d) for d in range((YEAR_END - YEAR_START).days + 1)]
ASSEMBLED = dt.datetime(2026, 11, 4, 9, 40)
REQUEST_DATE = dt.date(2026, 11, 6)
BOARD_DATE = dt.date(2026, 12, 8)
TERMS_DATE = dt.date(2026, 9, 22)
BENCHMARK = 80.0
MAX_COACHES = 6

HOSPITAL = "Ardley Valley Hospital"
FOUNDATION = "Ardley Valley Hospital Foundation"
DISTRICT = "Ardley Valley"
GRANT = "Hand Hygiene Coaching Grant 2027"

# code, ward name, specialty, beds, base compliance, care hours a patient needs on a day shift (mean),
# share of days the ward runs over its beds, how far over (extra care hours as a share of the base),
# nursing hours rostered over the patients' forecast care on a covered shift, mean stay in days, kind
WARDS = [
    ("AMU", "Acute Medical Unit", "Acute medicine (admissions)", 28, 0.876, 1.70, 0.40, 0.44, 1.03, 2.2, "surge"),
    ("ESSU", "Emergency Short Stay Unit", "Emergency medicine (short stay)", 16, 0.870, 1.65, 0.36, 0.46, 1.03, 1.4,
     "surge"),
    ("4A", "Ward 4A", "General medicine", 32, 0.868, 1.45, 0.44, 0.46, 1.03, 6.5, "surge"),
    ("7A", "Ward 7A", "Respiratory medicine", 28, 0.876, 1.50, 0.40, 0.46, 1.03, 5.8, "surge"),
    ("5A", "Ward 5A", "General surgery", 30, 0.887, 1.40, 0.07, 0.18, 1.05, 4.6, "mod"),
    ("6A", "Ward 6A", "Orthopaedics", 30, 0.883, 1.35, 0.07, 0.16, 1.05, 5.2, "mod"),
    ("6B", "Ward 6B", "Cardiology", 26, 0.889, 1.45, 0.06, 0.16, 1.05, 3.9, "mod"),
    ("7B", "Ward 7B", "Renal medicine", 24, 0.891, 1.40, 0.06, 0.15, 1.05, 6.1, "mod"),
    ("8A", "Ward 8A", "Oncology and haematology", 26, 0.879, 1.50, 0.03, 0.06, 1.06, 7.4, "steady"),
    ("9A", "Ward 9A", "Rehabilitation", 30, 0.867, 1.20, 0.02, 0.05, 1.07, 16.0, "steady"),
    ("9B", "Ward 9B", "Aged care (geriatric medicine)", 30, 0.785, 1.30, 0.03, 0.06, 1.06, 11.5, "steady"),
    ("PCU", "Palliative Care Unit", "Palliative care", 16, 0.873, 1.60, 0.02, 0.05, 1.08, 9.8, "steady"),
    ("CCU", "Coronary Care Unit", "Cardiology (coronary care)", 12, 0.895, 2.60, 0.04, 0.10, 1.09, 2.6, "crit"),
    ("ICU", "Intensive Care Unit", "Intensive care", 20, 0.890, 4.80, 0.03, 0.08, 1.07, 4.1, "crit"),
]
# the share of each ward's day shifts that ran short (sick leave and bank requests left unfilled)
SHORT = {"AMU": 0.40, "ESSU": 0.41, "4A": 0.40, "7A": 0.39, "5A": 0.12, "6A": 0.11, "6B": 0.12, "7B": 0.13,
         "8A": 0.10, "9A": 0.09, "9B": 0.14, "PCU": 0.08, "CCU": 0.10, "ICU": 0.09}
# how keenly each ward's gold auditors audit, as a multiple of the program's 100 moments a month
KEEN = {"AMU": 1.3, "ESSU": 1.1, "4A": 1.0, "7A": 1.2, "5A": 1.0, "6A": 1.15, "6B": 1.0, "7B": 1.4, "8A": 1.1,
        "9A": 1.0, "9B": 1.25, "PCU": 1.0, "CCU": 1.5, "ICU": 1.8}
WARD = [w[0] for w in WARDS]
WARD_NAME = {w[0]: w[1] for w in WARDS}
WARD_SPEC = {w[0]: w[2] for w in WARDS}
BEDS = {w[0]: w[3] for w in WARDS}

# the other areas the gold auditors audit (the national submission covers every audited area)
AREAS = [("ED", "Emergency Department"), ("OT", "Operating Theatres and Recovery"), ("DSU", "Day Surgery Unit"),
         ("RDU", "Renal Dialysis Unit"), ("OPC", "Outpatient Clinics"), ("MI", "Medical Imaging")]
AREA = [a[0] for a in AREAS]

# Ward 6A moved to the new surgical block on 2 February 2026 and took the code S1A
MOVE_DATE = dt.date(2026, 2, 2)
MOVED = ("6A", "S1A")
# the audit application was unavailable from 9 to 20 March 2026
OUTAGE = (dt.date(2026, 3, 9), dt.date(2026, 3, 20))
REKEY_DATE = dt.date(2026, 4, 2)
# patient master index merge
MPI_MERGE = dt.date(2026, 3, 1)

SHIFTS = {"AM": (dt.time(7, 0), dt.time(15, 30)), "PM": (dt.time(13, 0), dt.time(21, 30)),
          "ND": (dt.time(21, 0), dt.time(7, 30))}

PEOPLE = {
    "grants": "Lisa Burns",         # the Foundation's grants manager, the request's author
    "ipc": "Trevor Macdonald",      # clinical nurse consultant, infection prevention and control
    "don": "Mary Patton",           # Director of Nursing and Midwifery
    "workforce": "Bryan Ramos",     # workforce information analyst
}
REQUESTER = PEOPLE["grants"]

FILES = {
    "contents": "application_pack_index.txt",
    "terms": "hand_hygiene_coaching_grant_terms_2027.pdf",
    "program": "hand_hygiene_program_2025_26.pdf",
    "bsidef": "hobsi_surveillance_definitions_v3.pdf",
    "notes": "acuity_and_roster_extract_notes.txt",
    "dictionary": "data_dictionary.csv",
    "wards": "ward_and_area_reference.xlsx",
    "audits": "hand_hygiene_audit_moments_2025_26.csv",
    "acuity": "acuity_patient_shifts_2025_26.csv",
    "roster": "nursing_roster_actuals_2025_26.csv",
    "isolates": "blood_culture_isolates_2025_26.csv",
    "admissions": "blood_culture_patient_admissions_2025_26.csv",
    "transfers": "ward_transfers_2025_26.csv",
    "census": "midnight_census_2025_26.csv",
    "issues": "store_issues_hand_hygiene_2025_26.csv",
    "rounds": "dispenser_rounds_2025_26.csv",
    "survey": "patient_experience_survey_2025_26.csv",
    "flu": "staff_influenza_vaccination_2025.csv",
}
DISTRACTORS = ("survey", "flu")
GOLDEN = "coaching_wards_2027.xlsx"
CHART = "ward_compliance_2025_26.png"
DELIVERABLES = (GOLDEN, CHART)


def nsw_dst(d):
    """True when the local date falls in New South Wales daylight saving time (first Sunday of October to the first
    Sunday of April)."""
    def first_sunday(y, m):
        x = dt.date(y, m, 1)
        return x + dt.timedelta(days=(6 - x.weekday()) % 7)
    if d.month >= 10:
        return d >= first_sunday(d.year, 10)
    if d.month <= 4:
        return d < first_sunday(d.year, 4)
    return False


def shift_key(d, s):
    return (d.isoformat(), s)


def r1(x):
    """round half away from zero to one decimal"""
    import decimal
    return float(decimal.Decimal(repr(float(x))).quantize(decimal.Decimal("0.1"), rounding=decimal.ROUND_HALF_UP))


def r0(x):
    import decimal
    return int(decimal.Decimal(repr(float(x))).quantize(decimal.Decimal("1"), rounding=decimal.ROUND_HALF_UP))
