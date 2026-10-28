"""task118 (architecture 4) constants: the States of Eskerholm, its Treasury's 2027 Budget envelope for one excise duty,
the five duties' demand, the appraisal manual's filed terms, Customs' bonded-warehouse declarations for the asks, and
file names."""
import datetime as dt

ORG = "States of Eskerholm"
TREASURY = "States of Eskerholm Treasury"
ASSEMBLY = "States Assembly of Eskerholm"
PANEL = "Economic Affairs Scrutiny Panel"
TREASURY_UNIT = "Treasury Economics Unit"
CUSTOMS = "Eskerholm Customs and Excise"
STATS = "Eskerholm Statistics Office"
PEOPLE = {"economist": "Rhys Armstrong", "minister": "Aimee Miah", "customs": "Elaine Hooper", "stats": "Benjamin Humphreys"}
SEED = 118
AS_OF = dt.date(2026, 10, 20)

# the appraisal manual's filed terms
ENVELOPE = 1.5e6            # revenue (duty and GST) the Budget gives up in 2027, after consumers respond
GST = 0.05                  # on the duty-inclusive price; 3 per cent until 31 March 2011
GST_FROM = 13               # quarter index of 2011Q2
UPRATE_2027 = 1.03          # the 2027 duty rates already set, before any Budget measure
BUDGET_YEAR = 2027

# the world's demand (never shipped): quarterly short-run elasticity, persistence, seasonal pattern, noise
DUTIES = [  # code, name, unit, annual litres (2026), producer price c (GBP a litre), duty d (2026, GBP a litre), beta, lam
    ("BEER", "Beer", "litre", 7.0e6, 2.30, 0.80, -0.30, 0.55),
    ("CIDR", "Cider", "litre", 5.2e6, 1.55, 0.64, -0.62, 0.35),
    ("WINE", "Wine", "litre", 3.6e6, 7.10, 2.30, -0.32, 0.45),
    ("SPIR", "Spirits", "litre", 0.95e6, 9.00, 10.50, -0.50, 0.35),
    ("FUEL", "Road fuel", "litre", 56.0e6, 0.55, 0.80, -0.060, 0.94),
]
SEASON = {"BEER": (-0.12, 0.05, 0.13, -0.06), "CIDR": (-0.20, 0.10, 0.22, -0.12), "WINE": (-0.10, -0.02, 0.00, 0.12),
          "SPIR": (-0.16, -0.05, -0.02, 0.23), "FUEL": (-0.03, 0.01, 0.03, -0.01)}
NOISE = {"BEER": 0.012, "CIDR": 0.015, "WINE": 0.012, "SPIR": 0.014, "FUEL": 0.004}
SHOCK = {"BEER": 0.03, "CIDR": 0.03, "WINE": 0.03, "SPIR": 0.03, "FUEL": 0.02}
STEPS = {"FUEL": ([0.0, 0.05, 0.08, 0.12, -0.06, -0.10], [0.15, 0.2, 0.2, 0.15, 0.15, 0.15])}
STEPS_DEFAULT = ([0.0, 0.03, 0.06, 0.10, -0.04, -0.08], [0.3, 0.2, 0.15, 0.1, 0.15, 0.1])
QUARTERS = 75               # 2008Q1 to 2026Q3
NEW_FROM = 16               # 2012Q1: the release in its current layout
FIRST_YEAR = 2008

# the asks: Customs' declarations for releases from bonded warehouses, October 2025 to September 2026
ASK_QUARTERS = ["2025Q4", "2026Q1", "2026Q2", "2026Q3"]
DECL_FROM, DECL_TO = dt.date(2025, 7, 1), dt.date(2026, 9, 30)
REBATED_RATE = 0.1062      # marked gas oil, GBP per litre (not one of the five duties)
LAPSED_DAILY = 0.10        # chance a day carries a removal to each lapsed premises, per duty

FILES = {
    "series_new": "excise_clearances_prices_quarterly_2012-2026.csv",
    "series_old": "excise_clearances_prices_quarterly_2008-2011.xlsx",
    "rates": "excise_duty_rates_2008-2027.xlsx",
    "manual": "treasury_budget_appraisal_manual_2026.pdf",
    "thread": "budget_2027_duty_envelope.eml",
    "declarations": "customs_excise_declarations_2025-07_2026-09.csv",
    "cpc": "customs_procedure_codes.csv",
    "cpc_note": "customs_excise_accounting_note_ce14.pdf",
    "warehouses": "bonded_warehouse_register_2026.xlsx",
    "receipts": "excise_receipts_monthly_cash_2020-2026.csv",
    "price_quotes": "retail_price_survey_quotes_2026.csv",
    "passengers": "passenger_allowance_declarations_2025-26.csv",
}
DISTRACTORS = ["receipts", "price_quotes", "passengers"]
