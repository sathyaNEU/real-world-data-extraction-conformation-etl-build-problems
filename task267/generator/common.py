"""Shared constants for task267: Sallowfield Health's community diabetes screening, the 2026 season and the
2027 referral rule."""
import datetime as dt

ORG = "Sallowfield Health"
PROGRAM = "Community Screening Program"
REGION = "Orlenby"
LAB = "Thessler Laboratories"
ANALYSER = "Glyquant A1c point-of-care analyzer, model GQ-200"
AREAS = ["Orlenby City", "Fenwater", "Drummery", "Pellowmoor", "Quessly"]
AREA_W = [0.34, 0.20, 0.18, 0.16, 0.12]

PEOPLE = {"director": "Aaron Bradley", "medical": "Ariel Tucker", "data": "Bryan Gardner", "analyst": "Matthew Garcia"}

SEASON_START = dt.date(2026, 3, 2)
SEASON_END = dt.date(2026, 11, 20)
TRAINING_DAY = dt.date(2026, 2, 24)
EXTRACT = dt.date(2027, 1, 15)
MONTHS = [3, 4, 5, 6, 7, 8, 9, 10, 11]
MONTH_NAME = {3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October",
              11: "November"}

# the 2026 rule and the evaluation draw
RULE_SCORE, RULE_GLUCOSE = 6, 140
EVAL_FRACTION = 0.2
TARGET = 85.0

# the six candidate rules for 2027, in the order the candidates file lists them
RULES = [
    ("A60", "HbA1c of 6.0% or higher", "HBA1C >= 6.0"),
    ("A57", "HbA1c of 5.7% or higher", "HBA1C >= 5.7"),
    ("R26A60", "2026 rule, or HbA1c of 6.0% or higher", "SCORE >= 6 OR GLUCOSE >= 140 OR HBA1C >= 6.0"),
    ("A57G120", "HbA1c of 5.7% or higher, or random glucose of 120 mg/dL or higher",
     "HBA1C >= 5.7 OR GLUCOSE >= 120"),
    ("A55", "HbA1c of 5.5% or higher", "HBA1C >= 5.5"),
    ("SC5", "Risk score of 5 or higher", "SCORE >= 5"),
]
RULE_IDS = [r[0] for r in RULES]
RULE_NAME = {r[0]: r[1] for r in RULES}


def flags(rule, score, glucose, a1c):
    """The tablet's logic for each candidate, on one screening's values."""
    if rule == "A60":
        return a1c >= 6.0
    if rule == "A57":
        return a1c >= 5.7
    if rule == "R26A60":
        return (score >= RULE_SCORE) | (glucose >= RULE_GLUCOSE) | (a1c >= 6.0)
    if rule == "A57G120":
        return (a1c >= 5.7) | (glucose >= 120)
    if rule == "A55":
        return a1c >= 5.5
    if rule == "SC5":
        return score >= 5
    raise KeyError(rule)


ASSETS = ["A%02d" % i for i in range(1, 13)]
OGTT_PRICE = 38.50
OGTT_CODE = "OGTT2H"

FILES = {
    "encounters": "screening_encounters_2026.csv",
    "ogtt": "ogtt_results_2026.txt",
    "protocol": "screening_referral_protocol_2026-27.pdf",
    "notes": "season_2026_extract_notes.pdf",
    "rules": "candidate_referral_rules_2027.xlsx",
    "closeout": "season_close_out_2026.xlsx",
    "events": "event_calendar_2026.csv",
    "runlog": "gq200_run_log_2026.csv",
    "assets": "analyzer_asset_register.xlsx",
    "errors": "gq200_error_codes.pdf",
    "invoices": "thessler_invoice_lines_2026.csv",
    "feedback": "participant_feedback_2026.csv",
    "profile": "orlenby_chronic_disease_profile_2024.xlsx",
    "manifest": "export_manifest.csv",
}
DISTRACTORS = ["feedback", "profile"]
ASK_FILES = ["runlog", "assets", "errors", "invoices"]
DELIVERABLES = ["referral_rule_review_2027.xlsx", "referral_rule_2027_memo.docx"]
