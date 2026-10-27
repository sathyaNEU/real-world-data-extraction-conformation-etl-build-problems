"""task304 constants: the world, the files, the people and the dates."""

SEED = 2
REC_OFFSET = 83                             # the recoveries records' random stream
ORG = "Calderbrook Building Society"
ASOF = "2026-09-30"
PLAN_DATE = "2026-10-09"
PEOPLE = {"head": "Aimee Atkinson", "fst": "Oliver O'Brien", "cro": "Elliot Hunt"}

BOOKS = ["FTB", "HLTV", "SO", "BTL"]
BOOKNAME = {"FTB": "First-time buyer 2019-21", "HLTV": "High LTV 2022-24", "SO": "Shared ownership",
            "BTL": "Buy to let"}
ORDER = ["First-time buyer 2019-21", "High LTV 2022-24", "Shared ownership", "Buy to let"]
SHORT = {"First-time buyer 2019-21": "FTB", "High LTV 2022-24": "HLTV", "Shared ownership": "SO", "Buy to let": "BTL"}

FILES = {
    "book": "mortgage_book_2026-09-30.parquet",
    "history": "mortgage_payment_history_2019-01_to_2026-09.parquet",
    "possessions": "possession_register_2019-01_to_2026-09.csv",
    "sales": "possession_sales_completed_2019-2026.csv",
    "receivers": "lpa_receiver_appointments_2019-2026.csv",
    "litigation": "litigation_open_claims_2023-01_to_2026-09.csv",
    "ratecard": "product_transfer_rate_card_2026-10.xlsx",
    "hpi": "house_price_index_2010-01_to_2026-09.csv",
    "contacts": "contact_centre_volumes_2025.csv",
    "plan": "financial_support_team_2027_plan_paper.pdf",
    "pilot": "financial_support_team_pilot_2024_report.pdf",
    "policy": "arrears_and_possessions_policy_2026.pdf",
    "appetite": "board_risk_appetite_statement_2026.pdf",
}

# planning conventions filed in the plan paper
EFFECT = 0.15                               # the pilot: the team cuts the chance of possession by 15 per cent
RATE_WINDOW = ("2022-01", "2025-03")      # entries whose 18-month possession outcome is complete by September 2026
POSS_HORIZON = 18
PART2_SHARE = 0.3                         # owner-occupied possessions whose account holds a further advance part
RETERM_SHARE = 0.35                       # suspended orders varied on new terms at a later hearing
RESEAL_SHARE = 0.25                       # Pennant Moss orders the court re-seals and sends again
DEV_OFFSET = 995                          # the loan parts and re-sealed orders draw from their own stream
PILOT = (2024 * 12, 2024 * 12 + 11)    # borrowers entering the pilot, January to December 2024

# litigation: two panel firms and the county court hearing centres
FIRMS = ["Pennant Moss LLP", "Ridley Varga Solicitors"]
COURTS = ["Bradford", "Halifax", "Huddersfield", "Leeds", "Oldham", "Wakefield"]

REGION_NAMES = ["Calderdale", "Kirklees", "Leeds", "Bradford", "Wakefield", "Oldham"]
REGION_PC = [["HX1", "HX2", "HX3", "HX6", "HX7"], ["HD1", "HD2", "HD3", "HD5", "HD8"],
             ["LS6", "LS11", "LS13", "LS27", "LS28"], ["BD2", "BD3", "BD5", "BD10", "BD18"],
             ["WF1", "WF2", "WF10", "WF13", "WF17"], ["OL1", "OL4", "OL8", "OL10", "OL12"]]

# the April 2026 re-cut of the lending books: the possession register keeps the book each row was written under
RECUT = "2026-04-01"
OLD_FTB = "First-time buyer"
