"""task309 constants: the company, the files, the people and the dates."""

ORG = "Sandpiper Mutual Insurance Company"
ORG_SHORT = "Sandpiper Mutual"
VENDOR = "Corvane Risk Analytics"
MODEL = "Corvane HU 27.1"
ASOF = "2026-09-30"
BRIEF_DATE = "2026-11-06"
SEASON_START = "2027-06-01"
PEOPLE = {"cat": "Sherry Lang", "claims": "Andrew Mack", "cro": "Eric Brown"}
TITLES = {"cat": "Catastrophe Risk Manager", "claims": "Claims Director", "cro": "Chief Risk Officer"}

COUNTY_NAME = {"MRS": "Marlin Shoals", "HRB": "Heron Bay", "CLF": "Calloway Flats", "CYR": "Cypress Ridge",
               "PNH": "Pine Hollow", "SUM": "Sumner", "BRK": "Bracken"}
CANDIDATES = ["MRS", "HRB", "CLF", "CYR"]
PORTFOLIO_CODE = {"MRS": "SPM-RF27-MRS", "HRB": "SPM-RF27-HRB", "CLF": "SPM-RF27-CLF", "CYR": "SPM-RF27-CYR"}
ROUND_HOMES = 1500           # homes the round re-roofs in the chosen county

# The model-governance standard MG-04 (filed general criterion for adjustments to vendor event losses)
MG04_FROM_YEAR = 2012        # storms the reproduction test runs over: since the company's first FORTIFIED homes
MG04_MIN_PAID = 10_000_000   # a storm enters the test where the company paid at least this on the homes carrying it
MG04_TOL = 0.10              # reproduced within this share of the paid loss

FILES = {
    "claims": "claims_payment_lines_2012-01_to_2026-09.csv",
    "legacy": "legacy_claims_valuations_2008-2011.csv",
    "storms": "named_storm_register_2008-2025.csv",
    "footprints": "storm_peak_gust_footprints_2008-2025.xlsx",
    "inforce": "inforce_at_landfall_by_zip_2008-2025.parquet",
    "elt": "corvane_hu27_elt_sandpiper_retrofit_2027.parquet",
    "hazard": "corvane_hu27_event_hazard_summary.csv",
    "portfolios": "retrofit_2027_modeled_portfolios.csv",
    "policies": "policy_master_2006-2026.csv",
    "certs": "fortified_certificate_register_2012-2026.csv",
    "permits": "county_building_permits_roofing_2013-2026.csv",
    "brief": "retrofit_grant_round_2027_board_brief.pdf",
    "mg04": "MG-04_vendor_model_adjustment_standard.pdf",
    "vendor": "corvane_hu27_release_note_sandpiper.pdf",
    "closeout": "storm_closeout_summaries_2012-2025.pdf",
    "reins": "catastrophe_reinsurance_program_2026-27.pdf",
    "quotes": "roofing_contractor_quotes_2027.xlsx",
}
