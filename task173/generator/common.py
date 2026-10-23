"""Shared constants for the task173 generator (architecture 2): Varner Valley Public Utility District's April to
September 2027 irrigation pumping forecast under the Varner River watermaster's 2027 order.

Every figure the write-up states is computed by calc.py from the shipped pack and written to figures.json."""
from __future__ import annotations

import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

SEED = 173_2027
YEARS = list(range(2015, 2027))          # irrigation seasons on the billing extract
ET_YEARS = list(range(2007, 2027))       # the station record the normal is struck on
WY_GSA = list(range(2017, 2027))         # water years the agency's metered extraction reports cover
SEASON = [4, 5, 6, 7, 8, 9]

# Lone Bench Irrigation District allocations to its landowners, share of contract (the watermaster's
# curtailment of the district's post-1914 right in each season).
LBID_ALLOC = {2015: 0.15, 2016: 0.50, 2017: 1.00, 2018: 0.60, 2019: 1.00, 2020: 0.55, 2021: 0.10,
              2022: 0.00, 2023: 1.00, 2024: 0.75, 2025: 0.40, 2026: 0.05}
LBID_2027 = 0.0          # the 2027 order suspends the district's right
SENIOR_LIMIT_2027 = 0.25  # riparian and pre-1914 diversions held to a quarter of the decreed allotment

ASOF = "2026-10-16"       # the extracts were pulled on this day
DUE = "2026-12-01"

# Pack file names (the organisations' own export names).
F_BILL = "vvpud_ip_billing_2015-2026.csv"
F_REG = "vvpud_ip_service_register_2026-09-30.xlsx"
F_XW = "vvpud_cis_account_crosswalk_2020.csv"
F_SPT = "vvpud_gis_service_points_2026-09-30.csv"
F_FDR = "vvpud_oms_feeder_sources.csv"
F_GSA = "vsga_extraction_reports_wy2017-wy2026.xlsx"
F_DIV = "varner_watermaster_diversion_statements_2015-2026.csv"
F_ALT = "varner_decree_allotment_schedule_2026.xlsx"
F_LBID = "lbid_contracts_and_allocations_2015-2026.xlsx"
F_ETO = "station247_daily_eto_2007-2026.csv"
F_ORDER = "varner_watermaster_order_2027_season.pdf"
F_INSTR = "hpa_member_load_forecast_instructions_2027.pdf"
F_DPI = "hpa_dp_interval_export_2026.csv"
F_PEAK = "hpa_2026_monthly_system_peaks.csv"
F_RATE = "hpa_wholesale_rate_schedule_w2_excerpt.pdf"
F_PTEST = "vvpud_pump_efficiency_program_2019-2026.xlsx"
F_CROP = "kestrel_county_crop_report_2025_excerpt.pdf"
F_DICT = "data_dictionary.txt"
F_MAN = "export_manifest.csv"

DISTRACTORS = [F_PTEST, F_CROP]

DELIVERABLE = "irrigation_forecast_2027.xlsx"

DPS = ["RIVERSIDE", "MILL SLOUGH", "BENCH", "CORWIN ROAD"]
DP_CODES = {"RIVERSIDE": "VV-01", "MILL SLOUGH": "VV-02", "BENCH": "VV-03", "CORWIN ROAD": "VV-04"}

# Rounding the prompt states.
CALL_UNIT = 5_000        # MWh
