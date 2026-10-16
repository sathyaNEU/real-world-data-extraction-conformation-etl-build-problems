"""task124 constants and helpers shared by every generator module.

Hollins Ford Regional Water District (fictional), Ohio: the lead service line replacement plan's twelve zones,
the 2027 to 2037 capital plan, the district's verification history 2021 to 2026, and the two ask paths."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np

SEED = 1240212

# Calendar of the fiction
AS_OF = dt.date(2027, 1, 11)                 # the programme manager's working date
INVENTORY_DATE = dt.date(2027, 1, 8)         # inventory extract
LOG_START = dt.date(2021, 1, 4)
LOG_END = dt.date(2026, 12, 18)              # last verification of the 2026 season
MIGRATION = dt.date(2023, 3, 13)             # customer system to GIS cut-over (legacy premise numbers before)
REV1_DATE = dt.date(2024, 9, 30)             # plan revision 1 (zones as first drawn)
REV2_DATE = dt.date(2026, 10, 20)            # plan revision 2 (zones redrawn)
BOARD_DATE = dt.date(2027, 1, 19)            # board adopts the 2027 to 2037 capital plan
DEADLINE = dt.date(2037, 11, 1)              # every lead and GRR line replaced by this date (LCRI)
FIRST_YEAR, LAST_YEAR = 2027, 2037           # programme years the appropriation runs

# Plan costs, 2027 dollars (unit cost schedule)
UNIT_FULL = 14_400        # full replacement of a lead or GRR line, both sides, restoration included (system rate)
UNIT_DIG = 2_600          # verification excavation that finds no lead, restored (system rate)
MOBILISATION = 230_000    # once per zone, when its work starts
APPROPRIATION = 25_400_000  # capital plan, lead service line construction, each programme year
# engineer's unit costs by zone (service length, pavement, traffic control): full replacement, non-lead dig
ZONE_PRICES = {
    "RZ-07": (13_500, 2_680), "RZ-02": (16_350, 2_710), "RZ-11": (14_400, 2_760), "RZ-04": (14_450, 2_770),
    "RZ-09": (14_400, 2_640), "RZ-01": (14_400, 2_600), "RZ-05": (14_400, 2_600), "RZ-12": (14_400, 2_600),
    "RZ-03": (14_400, 2_600), "RZ-08": (14_400, 2_640), "RZ-10": (14_400, 2_600), "RZ-06": (14_400, 2_600),
}

# Construction eras the plan reports unknown lines by
ERAS = ("before 1930", "1930 to 1949", "1950 to 1988")
ERA_EDGES = (1930, 1950, 1989)
AGE_RULE_YEAR = 1989      # built in or after: non-lead by construction date

# Zones of plan revision 2 (inventory zones). code, name, municipality, lines, era mix
# (before 1930, 1930-49, 1950-88, 1989 on), share of pre-1989 lines with a usable tap card record
ZONES = [
    ("RZ-01", "Foundry Hill", "City of Hollins Ford", 5673, (0.55, 0.25, 0.15, 0.05), 0.30),
    ("RZ-02", "Canal Street", "City of Hollins Ford", 7013, (0.40, 0.35, 0.20, 0.05), 0.35),
    ("RZ-03", "Millrace", "City of Hollins Ford", 5340, (0.20, 0.40, 0.35, 0.05), 0.40),
    ("RZ-04", "North Linden", "City of Hollins Ford", 8211, (0.10, 0.25, 0.55, 0.10), 0.45),
    ("RZ-05", "Depot Square", "City of Hollins Ford", 5962, (0.35, 0.30, 0.30, 0.05), 0.30),
    ("RZ-06", "Wexley", "City of Hollins Ford", 7286, (0.05, 0.20, 0.65, 0.10), 0.50),
    ("RZ-07", "Orchard Ridge", "City of Hollins Ford", 4709, (0.60, 0.25, 0.10, 0.05), 0.25),
    ("RZ-08", "Elm Park", "City of Hollins Ford", 6243, (0.15, 0.30, 0.45, 0.10), 0.40),
    ("RZ-09", "Burkhart", "Darrow Township", 5779, (0.25, 0.25, 0.40, 0.10), 0.35),
    ("RZ-10", "Lakeview Terrace", "Darrow Township", 4396, (0.05, 0.15, 0.70, 0.10), 0.55),
    ("RZ-11", "Southgate", "City of Hollins Ford", 6598, (0.45, 0.30, 0.20, 0.05), 0.30),
    ("RZ-12", "Kittering Village", "Kittering Township", 4300, (0.10, 0.20, 0.60, 0.10), 0.45),
    ("RZ-13", "Darrow Meadows", "Darrow Township", 9600, (0.0, 0.0, 0.08, 0.92), 0.90),
    ("RZ-14", "Kittering North", "Kittering Township", 10300, (0.0, 0.0, 0.05, 0.95), 0.90),
]
PLAN_ORDER = ["RZ-07", "RZ-02", "RZ-11", "RZ-04", "RZ-09", "RZ-01",
              "RZ-05", "RZ-12", "RZ-03", "RZ-08", "RZ-10", "RZ-06"]
# the order agreement outreach opened zone by zone from February 2022, the ranking before plan revision 2
OUTREACH_ORDER = ["RZ-07", "RZ-02", "RZ-11", "RZ-04", "RZ-09", "RZ-01",
                  "RZ-05", "RZ-03", "RZ-12", "RZ-08", "RZ-06", "RZ-10"]
# renewal tap cards (COPPER) on lead or galvanized streets that the 2026 records search read again as the street's
# original material, by plan zone (lines no crew has dug); and lots on the copper streets of 1950 to 1988 that were
# platted with a tap and never built on. Set so each zone's expected replacements and cost sit more than one sampling
# sigma inside their rounding bins
LEAD_CARDS_ADDED = {"RZ-07": 3, "RZ-02": 9, "RZ-11": 7, "RZ-04": 6, "RZ-09": 6, "RZ-01": 8, "RZ-05": 4, "RZ-12": 7,
                    "RZ-03": 5, "RZ-08": 3, "RZ-10": 1, "RZ-06": 7}
NEVER_BUILT_C2 = {"RZ-07": 1, "RZ-02": 1, "RZ-11": 15, "RZ-04": 26, "RZ-09": 2, "RZ-01": 44, "RZ-05": 17,
                  "RZ-12": 54, "RZ-10": 4, "RZ-06": 5}
ZONE_NAME = {z[0]: z[1] for z in ZONES}


def stream(*keys) -> np.random.Generator:
    """One RNG stream per named component, seeded by blake2b so no process salt reaches it."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8)
    return np.random.default_rng(int.from_bytes(h.digest(), "big"))


def era_of(year: int) -> int:
    """0, 1, 2 for the plan's three construction eras; 3 for built in or after 1989; -1 unknown year."""
    if not year:
        return -1
    if year < 1930:
        return 0
    if year < 1950:
        return 1
    if year < AGE_RULE_YEAR:
        return 2
    return 3


def daterange_days(a: dt.date, b: dt.date) -> int:
    return (b - a).days


# The pack's files (target/), in the district's own naming
INVENTORY = "hfrwd_service_line_inventory_20270108.csv"
VERIFICATIONS = "sl_field_verifications_2021_2026.csv"
CROSSWALK = "cis_gis_crosswalk_2023.csv"
CODES = "sl_material_result_codes.csv"
PLAN = "HFRWD_LSLR_plan_rev2_2026-10.pdf"
CAPITAL = "HFRWD_capital_improvement_plan_2027-2037_board_draft.docx"
UNIT_COSTS = "unit_cost_schedule_2027.xlsx"
PROGRESS = "LSLR_progress_report_2026.pdf"
NOTES = "lsl_extract_field_notes_2027-01.md"
EXTRACT_LOG = "extract_log_2027-01-08.csv"
COMPLETIONS = "lsl_completions_2026.csv"
CHANGE_ORDERS = "change_orders_2026.xlsx"
CONTRACTS = "contracts_2026.csv"
AGREEMENTS = "access_agreements_2022_2026.csv"
OUTREACH = "lslr_outreach_tracker_20270108.csv"
TAP_SAMPLES = "lcr_tap_samples_2025_2026.csv"
METER_EXCHANGES = "ami_meter_exchanges_2023_2025.csv"
DISTRACTORS = (TAP_SAMPLES, METER_EXCHANGES)
DELIVERABLES = ("lslr_2027_programme.xlsx", "lslr_2027_board_paper.pdf")

DISTRICT = "Hollins Ford Regional Water District"
PEOPLE = {"programme": "Gregory Sheppard", "engineer": "Bethany Davidson", "finance": "Seth Sullivan",
          "chair": "Craig Stewart"}

# 2026 replacement contracts: contract, contractor, vendor numbers (Tri-County's changed with its July 2026
# acquisition), zones, bid price per full replacement, extra service length rate per foot past 50 feet
TC_SWITCH = dt.date(2026, 7, 13)
CONTRACTS_2026 = [
    ("2026-LSL-01", "Brannigan Excavating Inc", ("V-10482",), ("RZ-02", "RZ-05", "RZ-11", "RZ-12"), 10_480.00, 62.00),
    ("2026-LSL-02", "Tri-County Underground", ("V-20877", "V-31560"), ("RZ-03", "RZ-04", "RZ-08", "RZ-09"),
     10_950.00, 58.50),
    ("2026-LSL-03", "Kestrel Pipe and Utility", ("V-11935",), ("RZ-01", "RZ-06", "RZ-07", "RZ-10"), 11_320.00, 66.00),
]
CREW_CONTRACT = {"BRN-1": "2026-LSL-01", "BRN-2": "2026-LSL-01", "TCU-1": "2026-LSL-02", "TCU-2": "2026-LSL-02",
                 "KPU-1": "2026-LSL-03"}

# Plan revision 2 redrew the boundary inside each of these pairs: main segments moved from the first zone to the
# second, codes and names kept
REDRAW_PAIRS = [("RZ-01", "RZ-05"), ("RZ-07", "RZ-02"), ("RZ-08", "RZ-03"), ("RZ-04", "RZ-12"), ("RZ-11", "RZ-06"),
                ("RZ-10", "RZ-09")]
PORTAL_OPEN = dt.date(2024, 6, 3)
QUARTER_ENDS = (dt.date(2026, 3, 31), dt.date(2026, 6, 30), dt.date(2026, 9, 30))


def quarter_of(d: dt.date) -> int:
    return (d.month - 1) // 3 + 1


def utc_offset_hours(d: dt.date) -> int:
    """US Eastern: daylight time from the second Sunday of March to the first Sunday of November."""
    mar = dt.date(d.year, 3, 8)
    dst_on = mar + dt.timedelta(days=(6 - mar.weekday()) % 7)
    nov = dt.date(d.year, 11, 1)
    dst_off = nov + dt.timedelta(days=(6 - nov.weekday()) % 7)
    return 4 if dst_on <= d < dst_off else 5
