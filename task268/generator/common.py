"""Shared constants for task268: the Dunvarra Fish Producers' Organisation, its six haddock grounds, the autumn survey,
the members' fleet, its landing ports and quota pools."""
import datetime as dt

ORG = "Dunvarra Fish Producers' Organisation"
ORG_LTD = ORG + " Ltd"
ORG_SHORT = "Dunvarra FPO"
PEOPLE = {"science": "Carol Thorpe", "ceo": "Iain Ali"}

PLAN_ADOPTED = dt.date(2026, 3, 24)        # the members' general meeting adopts the recovery plan
RULES_ISSUED = dt.date(2026, 1, 12)        # the 2026 quota management rules
MANUAL_REV = dt.date(2023, 9, 4)           # the survey manual, revision 3
PACK_DATE = dt.date(2026, 11, 6)           # the science officer's evidence pack for the committee
COMMITTEE = dt.date(2026, 12, 9)           # the management committee's December meeting
AS_OF = dt.date(2026, 9, 30)               # the date the asks are taken at

YEARS = list(range(2019, 2027))
BASE = [2019, 2020, 2021]
LATEST = 2026
PAPER_YEARS = [2019, 2020, 2021, 2022]     # paper trip forms
ELOG_YEARS = [2023, 2024, 2025, 2026]      # the members' e-logbook app

# the six grounds in Annex A order: name, code on the organisation's charts, how its depth runs
GROUNDS = [("Skiravie Bank", "SKB", "bank"), ("Halmorie Deep", "HMD", "deep"), ("Moraskie Ground", "MRG", "slope"),
           ("Brettach Bank", "BRB", "bank"), ("Vallaskie Hole", "VKH", "deep"), ("Cullardy Patch", "CLP", "slope")]
GROUND_NAMES = [g[0] for g in GROUNDS]
GROUND_CODE = {g[0]: g[1] for g in GROUNDS}
CODE_GROUND = {g[1]: g[0] for g in GROUNDS}

# depth bands of the organisation's grid (Annex A), by a cell's charted depth
BANDS = ["A", "B", "C"]
BAND_LIMITS = {"A": (0, 100), "B": (100, 140), "C": (140, 400)}
BAND_TEXT = {"A": "under 100 m", "B": "100 m to under 140 m", "C": "140 m and deeper"}
STATIONS_PER_BAND = 12

# the landing ports and their port letters; the quota pools
PORTS = [("Eastquay", "EQ"), ("Kelmoor", "KR"), ("Tolsetter", "TL"), ("Haldness", "HN")]
PORT_NAMES = [p[0] for p in PORTS]
PORT_LETTERS = {p[0]: p[1] for p in PORTS}
POOLS = [("N", "North trawl"), ("E", "East trawl"), ("T", "Twin rig"), ("S", "Seine net"), ("I", "Inshore")]
POOL_CODES = [p[0] for p in POOLS]

SPECIES = {"HAD": "Haddock", "COD": "Cod", "WHG": "Whiting", "POK": "Saithe", "HKE": "Hake", "MON": "Monkfish",
           "LEM": "Lemon sole", "PLE": "Plaice", "WIT": "Witch"}

FILES = {
    "plan": "stock_recovery_plan_2026.pdf",
    "grid": "ground_grid_annex_a.csv",
    "paper": "tow_sheets_2019_2022.csv",
    "elog": "elogbook_hauls_2023_2026.csv",
    "survey": "survey_tows_2019_2026.csv",
    "manual": "autumn_survey_manual_rev3.pdf",
    "members": "member_vessels.xlsx",
    "factors": "conversion_factors.csv",
    "notes": "sales_notes_2026.csv",
    "ledger": "quota_ledger_2026.csv",
    "rules": "quota_rules_2026.pdf",
    "temperature": "sea_temperature_rectangles_2019_2026.csv",
    "gear_trial": "gear_trial_note_2025.pdf",
    "contents": "pack_contents.txt",
}
DISTRACTORS = ["temperature", "gear_trial"]

PLAN_CLAUSES = {"closure": "4.1", "stock": "4.2", "season": "4.3"}
