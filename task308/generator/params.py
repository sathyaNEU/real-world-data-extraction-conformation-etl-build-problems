"""task308 constants: Ardenmoor Mutual's four regional home books, the 2027 regional catastrophe layer the board buys,
the quotations, the files and the seed."""
import datetime as dt

ORG = "Ardenmoor Mutual"
ORG_LONG = "Ardenmoor Mutual Insurance Society Limited"
BROKER = "Whitlow Carrick Re Brokers"
COVERHOLDER = "Tellwright Underwriting"
SOCIETY = "Lowther and Pike Building Society"
TRANSFEROR = "Calder and Colne Insurance Services"
INDEX_HOUSE = "Hartwell Cost Data"

SEED = 5
AS_AT = dt.date(2026, 10, 31)          # the claims extract and the incurred values
QUOTE_DATE = dt.date(2026, 11, 18)
BOARD_DATE = dt.date(2026, 12, 9)
AS_OF = dt.date(2026, 11, 24)          # the paper's working folder
YEARS = list(range(2010, 2026))

REGIONS = ["Fenland", "Pennine", "Severn Vale", "Coastal North"]
CAT_PERILS = ["windstorm", "flood", "freeze"]
NONCAT = ["escape of water", "accidental damage", "theft", "fire", "subsidence"]
HOURS = {"windstorm": 72, "flood": 168, "freeze": 168}

RETENTION, LIMIT, ANNUAL = 10_000_000, 15_000_000, 30_000_000
PREMIUM = {"Fenland": 2_155_000, "Pennine": 2_930_000, "Severn Vale": 4_340_000, "Coastal North": 4_170_000}
LEAD = {"Fenland": "Merrow Re (Lloyd's syndicate 4417)", "Pennine": "Castellan Re", "Severn Vale": "Halvorsen Re",
        "Coastal North": "Halvorsen Re"}

FILES = {
    "claims": "home_claims_2010_2025.parquet",
    "exposure": "exposure_by_district_2010_2025.csv",
    "index": "rebuild_cost_index_2010_2026.xlsx",
    "plan": "business_plan_2027.xlsx",
    "quotes": "cat_xl_quotations_2027.pdf",
    "basis": "catastrophe_layer_valuation_basis.pdf",
    "events": "catastrophe_event_definitions.pdf",
    "ops": "claims_operations_report_2025.pdf",
    "mlu": "major_loss_unit_monthly_2023_2026.xlsx",
    "bdx": "lowther_pike_risk_bordereaux_2025-10_to_2026-02.csv",
    "direct": "direct_policies_in_force_2025-12-31.csv",
    "group": "group_catastrophe_programme_2026.pdf",
    "flood": "flood_resilience_survey_2024.csv",
}
DISTRACTORS = ["group", "flood"]
