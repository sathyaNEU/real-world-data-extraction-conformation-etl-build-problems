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

# The collaborative's regions, as its member list carries them.
REGION = {
    "H01": "Portland and Vancouver", "H18": "Portland and Vancouver",
    "H02": "Willamette Valley", "H03": "Willamette Valley", "H06": "Willamette Valley", "H12": "Willamette Valley",
    "H04": "Southern Oregon", "H07": "Southern Oregon", "H13": "Southern Oregon",
    "H05": "Central Oregon", "H08": "Klamath Basin",
    "H09": "Columbia Basin", "H14": "Columbia Basin", "H23": "Columbia Basin", "H26": "Columbia Basin",
    "H30": "Columbia Basin",
    "H10": "Columbia Gorge", "H11": "Oregon Coast",
    "H15": "Puget Sound", "H16": "Puget Sound", "H19": "Puget Sound", "H21": "Puget Sound",
    "H17": "Inland Northwest",
    "H20": "Central Washington", "H24": "Central Washington", "H31": "Central Washington",
    "H22": "Northwest Washington", "H29": "Northwest Washington",
    "H25": "Southwest Washington", "H27": "Southwest Washington", "H28": "Olympic Peninsula",
}
# The share of each hospital's applicant households whose main earner's work follows a season (generator only).
SEASONAL_SHARE = {
    "H01": (0.03, 0.05), "H02": (0.14, 0.20), "H03": (0.05, 0.08), "H04": (0.14, 0.20), "H05": (0.12, 0.18),
    "H06": (0.06, 0.10), "H07": (0.10, 0.15), "H08": (0.12, 0.18), "H09": (0.12, 0.18), "H10": (0.20, 0.28),
    "H11": (0.12, 0.18), "H12": (0.16, 0.22), "H13": (0.08, 0.12), "H14": (0.22, 0.30), "H15": (0.02, 0.04),
    "H16": (0.02, 0.04), "H17": (0.04, 0.07), "H18": (0.03, 0.05), "H19": (0.03, 0.05), "H20": (0.24, 0.32),
    "H21": (0.03, 0.05), "H22": (0.12, 0.18), "H23": (0.16, 0.24), "H24": (0.22, 0.30), "H25": (0.08, 0.12),
    "H26": (0.14, 0.20), "H27": (0.12, 0.18), "H28": (0.10, 0.15), "H29": (0.18, 0.26), "H30": (0.20, 0.28),
    "H31": (0.10, 0.15),
}
# The chance a household denied or given part of its balance applies again once its pay has fallen: seasonal
# work, year-round work (generator only).
REAPPLY = (0.10, 0.03)
# Each hospital's share under the golden estimate, as designed (generator only): the documents-denial rate is set to
# land it. Qualifying hospitals sit between 7.27 and 9.71, the others between 2.46 and 4.92.
TARGET = {
    "H01": 4.63, "H02": 7.68, "H03": 3.88, "H04": 4.68, "H05": 4.81, "H06": 3.59, "H07": 4.29, "H08": 7.31,
    "H09": 4.37, "H10": 7.93, "H11": 7.42, "H12": 8.57, "H13": 4.92, "H14": 7.36, "H15": 8.83, "H16": 3.12,
    "H17": 9.71, "H18": 2.46, "H19": 4.14, "H20": 8.38, "H21": 3.79, "H22": 7.62, "H23": 7.84, "H24": 7.27,
    "H25": 4.71, "H26": 8.14, "H27": 4.47, "H28": 7.55, "H29": 9.06, "H30": 7.47, "H31": 4.26,
}
# Applicant households over 2024 and 2025 (generator only).
HOUSEHOLDS = {c: (3200, 5400) for c in [h[0] for h in HOSPITALS]}
HOUSEHOLDS.update({"H01": (11000, 14000), "H15": (11000, 14000), "H16": (9500, 12500), "H17": (8000, 11000),
                   "H18": (7000, 9500), "H19": (7000, 9500), "H20": (8000, 11000), "H03": (7000, 9500),
                   "H02": (7000, 9500), "H04": (6500, 8800), "H05": (5600, 8000), "H21": (5600, 8000),
                   "H22": (5600, 8000), "H23": (6500, 8800), "H24": (5600, 8000), "H29": (5200, 7200),
                   "H30": (4800, 6700)})

NAME = {h[0]: h[1] for h in HOSPITALS}
HUB = {h[0]: h[4] for h in HOSPITALS}
MIGRATED = "H23"
MIGRATION = dt.date(2025, 6, 2)            # H23's billing moved to the Puget hub's system; counsellor IDs re-keyed

YEAR = 2025
HOLIDAYS = [dt.date(2025, 1, 1), dt.date(2025, 1, 20), dt.date(2025, 2, 17), dt.date(2025, 5, 26),
            dt.date(2025, 6, 19), dt.date(2025, 7, 4), dt.date(2025, 9, 1), dt.date(2025, 11, 11),
            dt.date(2025, 11, 27), dt.date(2025, 11, 28), dt.date(2025, 12, 25)]
HOLIDAYS_2024 = [dt.date(2024, 1, 1), dt.date(2024, 1, 15), dt.date(2024, 2, 19), dt.date(2024, 5, 27),
                 dt.date(2024, 6, 19), dt.date(2024, 7, 4), dt.date(2024, 9, 2), dt.date(2024, 11, 11),
                 dt.date(2024, 11, 28), dt.date(2024, 11, 29), dt.date(2024, 12, 25)]
HOLIDAYS_ALL = set(HOLIDAYS) | set(HOLIDAYS_2024) | {dt.date(2026, 1, 1), dt.date(2026, 1, 19)}
WITHDRAWN = 0.012                            # the share of applications withdrawn before a decision
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
    "guide": "fac_data_guide_2024_2025_extracts.pdf",
    "puget": "fac_determinations_2024_2025_puget_hub.csv",
    "willamette": "fac_determinations_2024_2025_willamette_hub.csv",
    "columbia": "fac_determinations_2024_2025_columbia_hub.csv",
    "crosswalk": "fac_h23_id_crosswalk_2025.xlsx",
    "hospitals": "fac_member_hospitals_2025.xlsx",
    "ledger": "fac_assistance_adjustments_2025.csv",
    "accounts": "fac_patient_accounts_2025.csv",
    "survey": "fac_patient_experience_by_payer_2025.csv",
    "state": "state_charity_care_filings_fy2025.xlsx",
    "contents": "contents.txt",
}
# The main earner's work as the common application asks it (question 7): the generator's kind, the Willamette hub's
# numeric code, the Columbia hub's short code and the Puget hub's label.
WORK = [
    ("FIELD", 1, "FARM", "Farm or orchard"),
    ("PACK", 2, "PACK", "Packing or food processing"),
    ("FISH", 3, "FISH", "Fishing or seafood"),
    ("RESORT", 4, "RSRT", "Hotel, resort or ski area"),
    ("WOODS", 5, "LOGG", "Logging or tree farm"),
    ("BUILD", 6, "CONS", "Construction"),
    ("CARE", 7, "HLTH", "Health care"),
    ("SHOP", 8, "RETL", "Retail or warehouse"),
    ("OFFICE", 9, "OFFC", "Office, school or government"),
    ("PLANT", 10, "FACT", "Factory"),
    ("OTHER", 11, "OTHR", "Other work"),
    ("NONE", 12, "NONE", "Not working or retired"),
]
WORK_W = {k: n for k, n, _, _ in WORK}
WORK_C = {k: s for k, _, s, _ in WORK}
WORK_P = {k: lbl for k, _, _, lbl in WORK}
DELIVERABLES = ("fair_assistance_coaching_2027.xlsx", "fair_assistance_coaching_2027.png")
