"""Constants shared by the task171 generator: calendar, districts, rate schedules, file names."""
from __future__ import annotations

import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
SEED = 171_2026

# billing months carried by the AMI export, March 2023 to October 2026
MONTHS = [(y, m) for y in range(2023, 2027) for m in range(1, 13) if (y, m) >= (2023, 3) and (y, m) <= (2026, 10)]
MIDX = {ym: i for i, ym in enumerate(MONTHS)}
OFFER_A = MIDX[(2024, 3)]           # R-TOU open from 1 March 2024: first effective reads in March 2024
PRE_A = [MIDX[(2023, 3)] + k for k in range(12)]   # billing months March 2023 to February 2024
TEST = [MIDX[(2025, 11)] + k for k in range(12)]   # billing months November 2025 to October 2026
ASOF = (2026, 10, 31)
CYCLE_DAY = {1: 4, 2: 11, 3: 18, 4: 25}           # read day of each billing cycle

DISTRICTS = ["Sedge Flats", "Brisco Bend", "Kessel Mill", "Pike Ridge", "Tamsey"]
DCODE = {"Sedge Flats": "SF", "Brisco Bend": "BB", "Kessel Mill": "KM", "Pike Ridge": "PR", "Tamsey": "TY"}

# load-research periods of the wholesale provider (prevailing local time)
PERIODS = ["kwh_2300_0600", "kwh_0600_1600", "kwh_1600_2100", "kwh_2100_2300"]

# rate schedules, dollars per month and dollars per kWh
R1_2024 = dict(cc=26.50, e=0.1184)
RTOU_2024 = dict(cc=26.50, peak=0.2694, other=0.0620)          # peak 4 p.m. to 9 p.m.
R1_2027 = dict(cc=28.00, e=0.1295)
RON_2027 = dict(cc=28.00, off=0.0778, other=0.1465)            # off-peak 11 p.m. to 6 a.m.
R1_HIST = {2023: dict(cc=25.75, e=0.1139), 2024: R1_2024, 2025: dict(cc=27.25, e=0.1236), 2026: dict(cc=27.25, e=0.1236), 2027: R1_2027}
RTOU_HIST = {2024: RTOU_2024, 2025: dict(cc=27.25, peak=0.2130, other=0.0885), 2026: dict(cc=27.25, peak=0.2130, other=0.0885)}

F_AMI = "ami_load_research_extract_2023-03_2026-10.parquet"
F_SVC = "cis_service_accounts_2026-10-31.csv"
F_RATE = "cis_rate_assignments_2026-10-31.csv"
F_EXCH = "meter_exchanges_2023-2026.csv"
F_CRM = "crm_rate_requests_2024-03_2026-10.xlsx"
F_SCHED = "residential_rate_schedules_2024-2027.pdf"
F_PLAN = "r-on_launch_plan_rates_committee_nov2026.docx"
F_BILL = "billing_summary_by_office_2025-11_2026-10.csv"
F_DICT = "data_dictionary.xlsx"
F_MAN = "export_manifest.csv"
F_HDD = "degree_days_station_kbsx_2023-2026.csv"
F_EV = "ev_charger_rebates_2021-2026.csv"
