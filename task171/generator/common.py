"""Constants shared by the task171 generator: calendar, plazas and lanes, the toll schedule, the enforcement cycle,
file names."""
from __future__ import annotations

import datetime as dt
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
SEED = 1_712_101

D = dt.date
CLOSE_START = D(2025, 3, 3)        # cash booths closed 11 p.m. to 5 a.m. from this night
LAST_CROSS = D(2026, 9, 30)        # last crossing day in the toll-by-mail extract
ASOF = D(2026, 10, 31)             # records as of
EXPORT = D(2026, 11, 9)            # the back office's export run
CUTOVER = D(2027, 1, 4)            # all-electronic tolling begins
MONTHS = [(y, m) for y in (2025, 2026) for m in range(1, 13) if D(2025, 3, 1) <= D(y, m, 1) <= D(2026, 9, 1)]

PLAZAS = ["VEL", "BRN", "OST"]
PLAZA_NAME = {"VEL": "Vellacott", "BRN": "Brannock", "OST": "Ostrey"}
MILEPOST = {"VEL": 6.2, "BRN": 24.8, "OST": 41.5}
DIRS = ["NB", "SB"]
ETC_LANES = ["E1", "E2"]           # open-road express lanes, MarrowPass only
BOOTH_LANES = ["B1", "B2", "B3", "B4"]

# cash toll for a two-axle vehicle; MarrowPass pays 80 per cent; axles 3, 4, 5 and 6 or more pay 2, 3, 4 and 5 times
CASH = {2025: {"VEL": 1.75, "BRN": 2.25, "OST": 1.50}, 2026: {"VEL": 1.90, "BRN": 2.45, "OST": 1.65}}
MULT = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5}
INVOICE_FEE = 1.50
VIOLATION_FEE = 5.00
LATE_FEE = 5.00
AGENCY_PCT = 0.20

HOME = "HM"   # the pack writes the home state's plates with this code
OUT_STATES = ["PA", "OH", "NY", "NJ", "MD", "WV", "VA", "IN", "MI", "IL", "NC", "TX", "FL", "ON", "QC"]
OUT_P = [0.21, 0.19, 0.12, 0.08, 0.07, 0.06, 0.05, 0.04, 0.04, 0.03, 0.03, 0.02, 0.02, 0.03, 0.01]

# 2027 plan: toll on the crossings of vehicles without a MarrowPass that pay cash today, 2026 traffic at 2027 rates
# (unchanged from 2026), after image review, by plate state; written into the cutover plan
PLAN_TOLL = {"IS": 11_908_500, "OS": 4_292_700}

F_LINES = "tbm_invoice_lines_2025-03_2026-09.parquet"
F_INV = "tbm_invoices_2025-04_2026-10.csv"
F_PAY = "tbm_payments_2025-04_2026-11.csv"
F_MVD = "dmv_registration_holds_2025-2026.csv"
F_AGY = "agency_placements_2025-2026.csv"
F_TAG = "marrowpass_commercial_postings_2026-01_2026-09.parquet"
F_LANES = "plaza_lanes.csv"
F_POLICY = "toll_schedule_and_toll_by_mail_policy_2026.pdf"
F_PLAN = "aet_cutover_revenue_plan_2027.docx"
F_TRAFFIC = "plaza_traffic_by_hour_2025-2026.csv"
F_IMG = "image_review_summary_2025-2026.csv"
F_DICT = "data_dictionary.xlsx"
F_MAN = "export_manifest.csv"
