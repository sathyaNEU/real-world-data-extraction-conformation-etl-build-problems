"""Constants shared by the task272 generator: the foundation and its collaborative, the 31 member hospitals and the
regional hub that sends each one's extracts, the calendar the records follow, the hubs' codes and the shipped file
names."""
import datetime as dt

FOUNDATION = "Vellacott Health Foundation"
COLLAB = "Fair Assistance Collaborative"
PROGRAM = "Decision Coaching Grants"
PEOPLE = {"requester": "Kristin Robertson", "requester_title": "Program Officer",
          "director": "Spencer Frank", "director_title": "Director of Programs"}

# (code, hospital, city, state, hub). H23 moved from the Columbia hub to the Puget hub on 2 June 2025.
HOSPITALS = [
    ("H01", "Whitlock Memorial Hospital", "Portland", "OR", "willamette"),
    ("H02", "Ostrander Community Hospital", "Salem", "OR", "willamette"),
    ("H03", "Brannigan Regional Medical Center", "Eugene", "OR", "willamette"),
    ("H04", "Copperhill Medical Center", "Medford", "OR", "willamette"),
    ("H05", "Halvorsen General Hospital", "Bend", "OR", "columbia"),
    ("H06", "Delacroix Memorial Hospital", "Corvallis", "OR", "willamette"),
    ("H07", "Underhill Community Hospital", "Roseburg", "OR", "willamette"),
    ("H08", "Pettibone Medical Center", "Klamath Falls", "OR", "willamette"),
    ("H09", "Carmody Memorial Hospital", "Pendleton", "OR", "columbia"),
    ("H10", "Kittredge Hospital", "The Dalles", "OR", "columbia"),
    ("H11", "Marchbanks Regional Hospital", "Coos Bay", "OR", "willamette"),
    ("H12", "Nesbitt Community Hospital", "McMinnville", "OR", "willamette"),
    ("H13", "Beckwith Medical Center", "Grants Pass", "OR", "willamette"),
    ("H14", "Jessup Memorial Hospital", "Hermiston", "OR", "columbia"),
    ("H15", "Lindqvist Medical Center", "Seattle", "WA", "puget"),
    ("H16", "Vandermeer Hospital", "Tacoma", "WA", "puget"),
    ("H17", "Thackery Memorial Hospital", "Spokane", "WA", "columbia"),
    ("H18", "Sorensen Regional Medical Center", "Vancouver", "WA", "puget"),
    ("H19", "Rasmussen Community Hospital", "Everett", "WA", "puget"),
    ("H20", "Ingersoll General Hospital", "Yakima", "WA", "columbia"),
    ("H21", "Stromberg Medical Center", "Olympia", "WA", "puget"),
    ("H22", "Jorgenson Memorial Hospital", "Bellingham", "WA", "puget"),
    ("H23", "Lundgren Regional Hospital", "Kennewick", "WA", "columbia"),
    ("H24", "Bellweather Community Hospital", "Wenatchee", "WA", "columbia"),
    ("H25", "Castellan Medical Center", "Longview", "WA", "puget"),
    ("H26", "Dunleavy Memorial Hospital", "Walla Walla", "WA", "columbia"),
    ("H27", "Mattingly Hospital", "Aberdeen", "WA", "puget"),
    ("H28", "Nygaard Community Hospital", "Port Angeles", "WA", "puget"),
    ("H29", "Petrakis Medical Center", "Mount Vernon", "WA", "puget"),
    ("H30", "Sundquist Memorial Hospital", "Moses Lake", "WA", "columbia"),
    ("H31", "Wennberg Regional Hospital", "Ellensburg", "WA", "columbia"),
]
CODES = [h[0] for h in HOSPITALS]
NAME = {h[0]: h[1] for h in HOSPITALS}
HUB = {h[0]: h[4] for h in HOSPITALS}
MIGRATED = "H23"
MIGRATION = dt.date(2025, 6, 2)            # H23's billing moved to the Puget hub's system; counsellor IDs re-keyed

YEAR = 2025
HOLIDAYS = [dt.date(2025, 1, 1), dt.date(2025, 1, 20), dt.date(2025, 2, 17), dt.date(2025, 5, 26),
            dt.date(2025, 6, 19), dt.date(2025, 7, 4), dt.date(2025, 9, 1), dt.date(2025, 11, 11),
            dt.date(2025, 11, 27), dt.date(2025, 11, 28), dt.date(2025, 12, 25)]
DST = (dt.datetime(2025, 3, 9, 2, 0), dt.datetime(2025, 11, 2, 2, 0))   # Pacific daylight time, local wall clock
EXTRACT_CUT = dt.date(2026, 3, 31)          # adjustments posted through this date on 2025 applications
CRITERIA_DATE = dt.date(2026, 12, 8)        # the foundation's program committee approves the criteria
ASSEMBLED = dt.datetime(2027, 1, 26, 14, 20)
BOARD = dt.date(2027, 3, 12)
COACHING_START = dt.date(2027, 7, 1)
THRESHOLD = 6.0                             # percentage points

# The hubs' outcome codes, as each hub's consolidation tool writes them.
PUGET_OUTCOME = {"approve": "APPROVED", "deny": "DENIED", "pend": "PENDED", "withdraw": "WITHDRAWN"}
WILLAMETTE_OUTCOME = {"approve": "A", "deny": "D", "pend": "P", "withdraw": "X"}
COLUMBIA_OUTCOME = {("approve", 100): 1, ("approve", 75): 2, ("approve", 50): 2, ("approve", 25): 2,
                    "deny": 3, "withdraw": 8, "pend": 9}
SYSTEM_USER = {"puget": "FA_PRESUMPTIVE", "willamette": "BATCHPE", "columbia": "PE-AUTOSCREEN"}
DENIAL_REASONS = ["INCOMPLETE", "OVER_INCOME", "OTHER_COVERAGE", "NOT_RESIDENT"]
# The collaborative's common denial-reason list. Version 2 (from 1 July 2025) is the one the data guide carries;
# determinations recorded before 1 July 2025 carry version 1's numbers.
REASON_V2 = {"INCOMPLETE": 1, "OVER_INCOME": 2, "OTHER_COVERAGE": 3, "NOT_RESIDENT": 4}
REASON_V1 = {"OVER_INCOME": 1, "INCOMPLETE": 2, "OTHER_COVERAGE": 3, "NOT_RESIDENT": 4}
REASON_SWITCH = dt.date(2025, 7, 1)

FILES = {
    "criteria": "fac_decision_coaching_criteria_fy2027.pdf",
    "guide": "fac_data_guide_2025_extracts.pdf",
    "puget": "fac_determinations_2025_puget_hub.csv",
    "willamette": "fac_determinations_2025_willamette_hub.csv",
    "columbia": "fac_determinations_2025_columbia_hub.csv",
    "crosswalk": "fac_counsellor_id_crosswalk_2025.xlsx",
    "hospitals": "fac_member_hospitals_2025.xlsx",
    "ledger": "fac_assistance_adjustments_2025.csv",
    "accounts": "fac_patient_accounts_2025.csv",
    "survey": "fac_patient_experience_by_payer_2025.csv",
    "state": "state_charity_care_filings_fy2025.xlsx",
    "contents": "contents.txt",
}
DELIVERABLES = ("fair_assistance_coaching_2027.xlsx", "fair_assistance_coaching_2027.png")
