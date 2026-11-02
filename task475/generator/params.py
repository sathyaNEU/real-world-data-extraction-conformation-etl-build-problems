"""Fixed parameters of the world: dates, centres, the two papers' questions, fees, file names and seeds."""
import datetime as dt

TASK = "task475"
D = dt.date

ORG = "Institute of Accredited Building Certifiers"
ORG_SHORT = "IABC"
EXAM = "Certifier Accreditation Examination"
PAPER2 = "Paper 2: Building Assessment and Certification Practice"

# seeds: one stream per sitting and one for the operating records
SEED_PEOPLE = 475_001
SEED_MAY = 475_249
SEED_NOV = 477_238
SEED_OPS = 476_065

ASOF = D(2026, 12, 1)
EXPORT_DAY = D(2026, 11, 30)
STAMP = (2026, 11, 30, 17, 5, 0)

MAY_SITTING = D(2026, 5, 16)
MAY_COMMITTEE = D(2026, 6, 18)
MAY_RELEASE = D(2026, 6, 30)
REVIEW_CLOSE = D(2026, 7, 21)
FEE_CHANGE = D(2026, 7, 1)
PORTAL_LIVE = D(2026, 8, 3)
NOV_OPEN = D(2026, 8, 3)
NOV_CLOSE = D(2026, 9, 25)
NOV_LATE_CLOSE = D(2026, 10, 9)
NOV_SITTING = D(2026, 11, 7)
NOV_COMMITTEE = D(2026, 12, 10)

PASS_MARK = 50
QUESTION_MAX = 20

# centre code, name, candidate number block, share of candidates, venue, state
CENTRES = [
    ("SYD", "Sydney", 1, 0.235, "Level 2, 160 Sussex Street, Sydney", "NSW"),
    ("WSY", "Western Sydney", 2, 0.125, "Ground floor, 9 Wentworth Street, Parramatta", "NSW"),
    ("MEL", "Melbourne", 3, 0.25, "Level 5, 452 Flinders Street, Melbourne", "VIC"),
    ("BNE", "Brisbane", 4, 0.17, "Level 1, 100 Edward Street, Brisbane", "QLD"),
    ("PER", "Perth", 5, 0.115, "Level 3, 12 St Georges Terrace, Perth", "WA"),
    ("ADL", "Adelaide", 6, 0.105, "Level 2, 33 King William Street, Adelaide", "SA"),
]
CODES = [c[0] for c in CENTRES]
CENTRE_NAME = {c[0]: c[1] for c in CENTRES}
# the Western Sydney centre is the Parramatta centre renamed when the portal went live
MAY_NAME = dict(CENTRE_NAME, WSY="Parramatta")

# November 2026 Paper 2: title and part maxima of each optional question
NOV_QUESTIONS = [
    ("Building classification and the NCC compliance pathways", [6, 8, 6]),
    ("Structural adequacy and reliance on engineers' certificates", [5, 5, 4, 6]),
    ("Energy efficiency: Section J and dwelling energy ratings", [6, 5, 4, 5]),
    ("Waterproofing, wet areas and external moisture", [4, 6, 4, 6]),
    ("Access for people with a disability under the Premises Standards", [5, 6, 5, 4]),
    ("Fire safety performance solutions and fire engineering reports", [5, 6, 4, 5]),
    ("Mandatory inspections, notices and orders", [6, 4, 5, 5]),
    ("Development consent conditions and the construction certificate", [6, 5, 5, 4]),
]
MAY_QUESTIONS = [
    ("Occupancy certificates and final inspections", [6, 6, 8]),
    ("Bushfire-prone land and BAL assessments", [5, 5, 5, 5]),
    ("Sound transmission and isolation between units", [7, 6, 7]),
    ("Swimming pool barriers and certification", [4, 6, 5, 5]),
    ("Combustible cladding and external walls", [8, 6, 6]),
    ("Variations to approved plans", [6, 7, 7]),
    ("Retaining walls, excavation and adjoining property", [5, 4, 6, 5]),
    ("Change of use and existing buildings", [7, 7, 6]),
]

# fee schedule (GST inclusive), by financial year of receipt
FEES = {
    "2025-26": {"remark": 138.00, "clerical": 58.00, "entry_p2": 690.00, "entry_p1": 540.00},
    "2026-27": {"remark": 145.00, "clerical": 62.00, "entry_p2": 725.00, "entry_p1": 565.00},
}

PEOPLE = {
    "chair": "Terri Brown",
    "analyst": "Stephanie Nguyen",
    "chief": "Joshua Fitzgerald",
}

FILES = {
    "export": "cae_marking_export_2026.csv",
    "may_reg": "cae_candidates_may2026.xlsx",
    "nov_reg": "cae_entries_nov2026.csv",
    "requests": "portal_requests_nov2026.json",
    "centres": "centre_directory.csv",
    "reviews": "results_review_requests_2026.csv",
    "invoices": "ar_invoices_2026.csv",
    "accounts": "corporate_accounts.csv",
    "regs": "cae_examination_regulations_2026.pdf",
    "paper": "cae_paper2_nov2026.pdf",
    "minutes": "examinations_committee_minutes_2026-06-18.pdf",
    "history": "cae_results_history_2019_2026.csv",
    "venues": "venue_holds_2027.xlsx",
}
DISTRACTORS = ["history", "venues"]

RESULTS_CSV = "nov2026_paper2_results.csv"
PAPER_DOCX = "paper2_results_committee_paper.docx"
