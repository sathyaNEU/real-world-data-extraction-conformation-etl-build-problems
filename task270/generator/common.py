"""Shared constants for task270: Hallowmere Foodstores' 2027 HFC pack replacements (the region whose packs lost the
largest share of their charge in 2026), the world's names, dates, regions and the pack's file names."""
import datetime as dt
from decimal import Decimal, ROUND_HALF_UP

SEED = 7
ORG = "Hallowmere Foodstores"
ORG_LTD = "Hallowmere Foodstores Ltd"
CONTRACTOR = "Kelbray Refrigeration"
CONTRACTOR_LTD = "Kelbray Refrigeration Ltd"
BUREAU = "Tarnley Monitoring"
RECLAIMER = "Arnside Gas Reclamation"
REQUESTER = "Jayne Gallagher"          # head of property and sustainability
CONTRACTS = "Denis Webster"            # Kelbray's contracts manager
CEO = "Steven Ashton"

REGIONS = ["YOR", "LAN", "NE", "CUM"]
REGION_NAME = {"YOR": "Yorkshire", "LAN": "Lancashire", "NE": "North East", "CUM": "Cumbria"}

START = dt.date(2024, 1, 1)
END = dt.date(2026, 12, 31)
YEAR = 2026
LINE = 10.0                           # per cent of full charge
STRATEGY_DATE = dt.date(2026, 3, 11)
SPEC_DATE = dt.date(2024, 2, 19)
BUREAU_DOC_DATE = dt.date(2025, 6, 2)
JOBS_EXPORT = dt.date(2027, 1, 7)
LEVELS_EXPORT = dt.date(2027, 1, 6)
ASSEMBLED = dt.datetime(2027, 1, 12, 15, 20)
EXEC_MEETING = dt.date(2027, 2, 3)

# refrigerants on the register, with the GB F-gas Regulation's (AR4) global warming potentials
GWP = {"R404A": 3922, "R448A": 1387, "R449A": 1397, "R407F": 1825, "R744": 1, "R290": 3, "R134a": 1430,
       "R410A": 2088, "R32": 675}
TRADE = {"R448A": "Solstice N40", "R449A": "Opteon XP40"}

FILES = {
    "register": "fgas_register_2026.xlsx",
    "stores": "hallowmere_stores.csv",
    "jobs": "kelbray_job_sheets_2024_2026.csv",
    "levels": "tarnley_receiver_levels_2024_2026.csv",
    "tags": "tarnley_pack_tags.csv",
    "strategy": "refrigerant_strategy_2026.pdf",
    "spec": "kelbray_service_specification_2024.pdf",
    "bureau": "tarnley_service_description_2025.pdf",
    "cylinders": "kelbray_cylinder_log_2026.csv",
    "power": "store_electricity_2024_2026.csv",
    "kpi": "kelbray_kpi_report_2026.pdf",
    "dictionary": "data_dictionary.csv",
    "contents": "pack_contents.txt",
}
DISTRACTORS = ["power", "kpi"]
BOOK = "hfc_pack_replacements_2027.xlsx"
CHART = "pack_leakage_2026.png"


def r(x, n=0):
    """half-up rounding, as the workbook and the write-up print"""
    q = Decimal(1).scaleb(-n)
    v = Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP)
    return float(v) if n else int(v)
