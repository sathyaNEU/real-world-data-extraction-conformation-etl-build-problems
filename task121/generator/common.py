"""Constants for task121 (architecture 6): the Quellmont County Emergency Communications District, its call-takers,
the 2025-26 window, the dates of the changes around March 2026, the people and the pack's file names."""
import datetime as dt

SEED = 7
START = dt.date(2025, 9, 1)             # the window the committee reviews: September 2025 to August 2026
END = dt.date(2026, 8, 31)
ROSTER_FROM = dt.date(2025, 8, 18)      # the roster extract starts two weeks early, so every shift has its previous one
DAYS = [START + dt.timedelta(d) for d in range((END - START).days + 1)]
MONTHS = [(2025, m) for m in range(9, 13)] + [(2026, m) for m in range(1, 9)]
ACADEMY = dt.date(2026, 2, 9)           # the six academy graduates take their first calls
ROTATION = dt.date(2026, 3, 2)          # the 2026 rotation: each call-taker's first block on or after this date
RELEASE = dt.datetime(2026, 3, 3, 6, 0)  # protocol software release 13.3 goes live on every position
SPLIT = dt.date(2026, 3, 1)             # the six months before March and the six months from March
DST_END = dt.datetime(2025, 11, 2, 2, 0)     # 02:00 CDT becomes 01:00 CST
DST_START = dt.datetime(2026, 3, 8, 2, 0)    # 02:00 CST becomes 03:00 CDT
ASSEMBLED = dt.datetime(2026, 11, 4, 16, 20)
COMMITTEE = dt.date(2026, 12, 10)

COUNTY = "Quellmont County"
CENTRE = "Quellmont County Emergency Communications District"
SHORT = "QCECD"
COMMITTEE_NAME = "Quellmont County EMS Quality Committee"

PEOPLE = {
    "qa": "Erica Schmitt",          # the centre's quality assurance manager, who assembled the folder
    "md": "Raymond Melendez",       # the county's EMS medical director, who chairs the committee
    "director": "Karen Hayes",      # the centre's director
    "scheduler": "Jerome Reed",     # the centre's workforce scheduler
}
REQUESTER = PEOPLE["qa"]

# shift types: start hour and length in hours (nights dated by the day they start)
SHIFT = {"D": (7, 8), "E": (15, 8), "N": (23, 8)}
QUICK_RETURN_HOURS = 11

# protocol code, chief complaint, share of medical calls, chance the patient is critical or emergent, the
# chance a critical or emergent patient's call is sent cold at full rest, and whether release 13.3 changed it
PROTOCOLS = [
    ("01", "Abdominal pain", 0.060, 0.20, 0.150, False),
    ("06", "Breathing problems", 0.110, 0.52, 0.090, False),
    ("09", "Cardiac or respiratory arrest", 0.012, 0.98, 0.020, False),
    ("10", "Chest pain", 0.110, 0.46, 0.080, True),
    ("12", "Seizures", 0.045, 0.34, 0.120, False),
    ("13", "Diabetic problems", 0.035, 0.30, 0.120, False),
    ("17", "Falls", 0.150, 0.13, 0.165, True),
    ("23", "Overdose or poisoning", 0.035, 0.38, 0.110, False),
    ("25", "Psychiatric problems", 0.040, 0.10, 0.140, False),
    ("26", "Sick person", 0.170, 0.21, 0.170, True),
    ("28", "Stroke", 0.045, 0.60, 0.085, True),
    ("29", "Traffic incident", 0.068, 0.33, 0.100, False),
    ("31", "Unconscious or fainting", 0.120, 0.40, 0.075, False),
]
PROTOCOL = {p[0]: p for p in PROTOCOLS}
RELEASE_CHANGED = sorted(p[0] for p in PROTOCOLS if p[5])
LEVELS_HOT = ("D", "E")
LEVELS_COLD = ("C", "B", "A", "O")

# the cause's strength: a call taken on a shift begun after a quick return, by a graduate in the first 120 days,
# or between midnight and six
QR_FACTOR = 3.0
NEW_FACTOR = 1.4
NEW_DAYS = 120
NIGHT_FACTOR = 1.10

# ambulances, the 911 trunks and the 10-digit emergency lines
UNITS = ["M%02d" % i for i in range(1, 23)]
TRUNKS = [
    ("TG01", "911 wireline", True),
    ("TG02", "911 wireless", True),
    ("TG03", "911 VoIP", True),
    ("TG05", "911 calls transferred from the Sheriff's Office", True),
    ("TG07", "10-digit emergency line (alarm companies, hospitals and other agencies)", False),
]
STANDARD_ANSWER = 15        # seconds
STANDARD_ANSWER_SHARE = 90  # per cent of 911 calls
MINSEC_REVIEWER = "QA7"     # keys review times as minutes and seconds without the colon

FILES = {
    "index": "qa_review_folder_index.txt",
    "definitions": "qa_program_definitions_2025.pdf",
    "release": "protocol_software_release_13_3.pdf",
    "reference": "centre_reference.xlsx",
    "takers": "call_takers.csv",
    "roster": "roster_shifts_worked_2025_2026.csv",
    "calls": "cad_medical_calls_2025_2026.csv",
    "epcr": "epcr_patient_records_2025_2026.csv",
    "units": "cad_unit_history_2025_2026.csv",
    "che": "che_call_detail_2025_2026.csv",
    "tcpr": "tcpr_arrest_reviews_2025_2026.csv",
    "casereview": "protocol_case_reviews_2025_2026.csv",
    "unithours": "ems_unit_hours_2025_2026.csv",
    "dictionary": "data_dictionary.csv",
}
DISTRACTORS = ("casereview", "unithours")
GOLDEN = "under_triage_cause_2026.xlsx"
CHART = "under_triage_2025_26.png"
DELIVERABLES = (GOLDEN, CHART)


def month_of(d):
    return (d.year, d.month)


def month_label(ym):
    y, m = ym
    return dt.date(y, m, 1).strftime("%b %Y")


def is_cdt(t):
    """True when a local wall-clock time falls in central daylight time (the second pass of the repeated hour on
    2 November 2025 is read as standard time by the caller)"""
    if dt.datetime(2025, 3, 9, 2) <= t < dt.datetime(2025, 11, 2, 1):
        return True
    if dt.datetime(2026, 3, 8, 3) <= t < dt.datetime(2026, 11, 1, 1):
        return True
    return False


def r1(x):
    """round half away from zero to one decimal"""
    import decimal
    return float(decimal.Decimal(repr(float(x))).quantize(decimal.Decimal("0.1"), rounding=decimal.ROUND_HALF_UP))


def r0(x):
    import decimal
    return int(decimal.Decimal(repr(float(x))).quantize(decimal.Decimal("1"), rounding=decimal.ROUND_HALF_UP))
