"""Shared constants for task269: Callowfield University School of Medicine, its 2026 final-year OSCE, the 2027
sitting with Fennabeg Clinical School's first graduate-entry cohort, the case bank and the examiner register."""
import datetime as dt

UNIVERSITY = "Callowfield University"
SCHOOL = "Callowfield University School of Medicine"
FENNABEG = "Fennabeg Clinical School"
HOSPITAL = "Callowfield University Hospital"
BOARD = "Medical Programmes Accreditation Board"
PEOPLE = {"assessment": "Meghan Daniel", "skills": "Cillian Garland"}

# the 2026 sitting: one circuit at the Clinical Skills Centre, the same two examiners at each station both days
SIT26 = (dt.date(2026, 5, 12), dt.date(2026, 5, 13))
ROUNDS26 = {1: (1, 2, 3, 4), 2: (5, 6, 7)}             # day -> rounds; twelve candidates a round
N_CAND26 = 84
SYSTEM_UPDATE = dt.datetime(2026, 5, 12, 21, 30)      # the OSCE system's overnight update between the two days

# the 2027 sitting and its delivery plan
SIT27 = (dt.date(2027, 5, 11), dt.date(2027, 5, 12))
SITES27 = [("CSC", "Clinical Skills Centre, Callowfield"), ("CUH", "Simulation Suite, Callowfield University Hospital"),
           ("FCS", "Clinical Skills Unit, Fennabeg Clinical School")]
ROOMS27 = 18                                           # rooms each site can hold an OSCE station in
STANDARD = 0.80                                        # the policy's reliability standard for the total mark
SETTINGS = list(range(12, ROOMS27 + 1))               # the numbers of stations the plan allows

# the policy's dates for the two supporting checks
REVIEW_FROM = dt.date(2024, 5, 11)                     # a case reviewed in the three years before the sitting
EXPOSURE_YEARS = (2025, 2026)                          # a case set at a final OSCE sitting (main or supplemental)
ALLOCATION = dt.date(2026, 12, 7)                      # the examinations office allocates examiners
TRAINED_FROM = dt.date(2023, 12, 7)                    # examiner training completed in the three years before it
BANK_MIGRATION = dt.date(2025, 11, 14)                 # the case bank's move to its new system
FORM_OPENED = dt.datetime(2026, 10, 19, 9, 0)          # the examiners' availability form, sent and closed
FORM_CLOSED = dt.datetime(2026, 11, 27, 17, 0)
REGISTER_EXPORT = dt.date(2026, 11, 30)
BANK_EXPORT = dt.date(2026, 11, 30)
PACK_DATE = dt.date(2026, 12, 2)

DOMAINS = ["History taking", "Physical examination", "Communication", "Procedural skills"]
DOMAIN_PREFIX = {"History taking": "HIS", "Physical examination": "EXM", "Communication": "COM",
                 "Procedural skills": "PRO"}
SESSIONS = [("d1_am", "Tuesday 11 May, morning"), ("d1_pm", "Tuesday 11 May, afternoon"),
            ("d2_am", "Wednesday 12 May, morning"), ("d2_pm", "Wednesday 12 May, afternoon")]

# the twelve 2026 stations: number, case code, title, domain, checklist items, simulated patient or trainer
STATIONS26 = [
    (1, "HIS-031", "Chest pain: history", "History taking", 18, "SP"),
    (2, "EXM-017", "Cardiovascular examination", "Physical examination", 20, "SP"),
    (3, "COM-024", "Explaining a new diagnosis of type 2 diabetes", "Communication", 15, "SP"),
    (4, "PRO-009", "Venepuncture and blood cultures", "Procedural skills", 19, "SP and task trainer"),
    (5, "HIS-044", "Tiredness in a young woman: history", "History taking", 16, "SP"),
    (6, "EXM-022", "Knee examination", "Physical examination", 16, "SP"),
    (7, "COM-030", "Consent for a lumbar puncture", "Communication", 16, "SP"),
    (8, "PRO-014", "Male urinary catheterisation", "Procedural skills", 21, "Manikin"),
    (9, "HIS-038", "Altered bowel habit: history", "History taking", 17, "SP"),
    (10, "EXM-029", "Cranial nerve examination", "Physical examination", 22, "SP"),
    (11, "COM-027", "Breaking bad news: biopsy result", "Communication", 14, "SP"),
    (12, "PRO-019", "Adult basic life support", "Procedural skills", 15, "Manikin"),
]
WITHDRAWN = (7, 14)          # station 7's item 14, withdrawn by the board of examiners after day 1
NA_ITEMS = {1: 17, 5: 15, 9: 16}   # an item the simulated patient's cue opens, not applicable when it was not given

LABELS_DAY1 = {0: "Not done", 1: "Partly done", 2: "Done well", None: "N/A"}
GLOBAL = ["Clear fail", "Borderline", "Clear pass", "Good", "Excellent"]

FILES = {
    "marks": "osce2026_marks_export.csv",
    "global": "osce2026_global_grades.csv",
    "stations": "osce2026_station_sheet.xlsx",
    "examiners26": "osce2026_examiner_allocation.xlsx",
    "minutes": "board_of_examiners_minutes_2026-05-14.pdf",
    "policy": "assessment_policy_v7.pdf",
    "plan": "final_osce_2027_delivery_plan.docx",
    "bank": "case_bank_export_2026-11-30.xlsx",
    "usage": "case_usage_history_2021_2026.csv",
    "migration": "casebank_migration_report_2025-11.pdf",
    "register": "examiner_register_2026-11-30.xlsx",
    "availability": "examiner_availability_2027_responses.csv",
    "training": "examiner_training_attendance_2021_2026.csv",
    "sp_invoices": "sp_agency_invoices_2026.xlsx",
    "feedback": "osce2026_candidate_feedback_summary.pdf",
    "contents": "osce2027_blueprint_working_pack_index.txt",
}
