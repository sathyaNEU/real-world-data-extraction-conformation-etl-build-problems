"""The world of task466: the Town of Quillfield, the Varrow River at the old mill dam, the State Hydrologic Survey's
gauge above the dam, the town's water-works reports from 1894 to 1950, the State Water Resources Board's low-flow
guidance, the town's drought plan and permit, and Castlewick's offer of firm interconnect capacity for 2027."""
import datetime as dt
import math

SEED = 466

# ---------------------------------------------------------------- units and the filed constants
GAL_PER_CF = 7.48051948                         # US gallons in one cubic foot
MGD_PER_CFS = GAL_PER_CF * 86400 / 1e6          # 0.6463169 million gallons a day per cubic foot per second
SUSPEND_MGD = 2.0                               # the 1893 agreement: two million gallons in twenty-four hours
SUSPEND_CFS = SUSPEND_MGD / MGD_PER_CFS         # 3.0944 cfs
REGIONAL_SKEW = -0.30                           # the Board's regional low-flow skew of the logarithms
DESIGN_P = 0.02                                 # the 50-year recurrence interval
SCENARIOS = (10, 25, 50, 100)
PASSBY_CFS = 0.50                               # the permit's passby over the dam
PERMIT_MAX_MGD = 1.40                           # the permit's maximum withdrawal
STAGE2_DEMAND = {2025: 0.87, 2026: 0.89, 2027: 0.91, 2028: 0.93}   # the plan's Stage 2 demand, MGD
BLOCK_MGD = 0.1                                 # Castlewick's firm capacity blocks
BLOCK_PRICE = 28400                             # dollars per block per year (the offer)
COMMODITY = 4.12                                # dollars per thousand gallons delivered (the offer)
MAX_BLOCKS = 8                                  # the interconnect's hydraulic limit, 0.8 MGD
TRIGGER_STAGE2_CFS = 4.0                        # the permit's Stage 2 trigger, 7-day mean, June 1 to November 30
TRIGGER_STAGE1_CFS = 6.0                        # the plan's voluntary Stage 1

GAUGE_START = dt.date(1951, 4, 1)
APPROVED_THROUGH = dt.date(2025, 9, 30)
EXPORT_DAY = dt.date(2026, 10, 15)
FIRST_REPORT, LAST_REPORT = 1894, 1950
MISSING_REPORTS = (1909, 1918, 1944)
UNITS_CHANGE = 1921                              # second-feet from the 1921 report
FIT_YEARS = (1951, 2024)                         # complete climatic years of approved record
AS_OF = "2026-10-16"                             # the superintendent's memo, the day the folder was assembled
DRAINAGE_SQMI = 41.6

# ---------------------------------------------------------------- names
TOWN = "Quillfield"
RIVER = "Varrow River"
CITY = "Castlewick"
MILL = "Ansel and Hale Woolen Company"
SOCIETY = "Quillfield Historical Society"
SURVEY = "State Hydrologic Survey"
BOARD = "State Water Resources Board"
DISTRICT = "Elm Hollow Water District"
WELLS = "Hollow Road wellfield"
STATION_NO = "01-2297.40"
STATION = "Varrow River at Quillfield"
PERMIT_NO = "WD-0417"
GUIDANCE_NO = "WR-14"
PEOPLE = {"superintendent": "Jaime Galloway", "archivist": "Phyllis Mitchell", "castlewick": "Darryl Powell"}
TITLES = {"superintendent": "Water Superintendent, Town of Quillfield",
          "archivist": "Archivist, Quillfield Historical Society",
          "castlewick": "Director of Utilities, City of Castlewick"}

FILES = {
    "gauge": "varrow_river_at_quillfield_daily_values.txt",
    "reports": "quillfield_water_works_reports_1894_1950.pdf",
    "guidance": "swrb_guidance_wr14_design_drought_flows.pdf",
    "plan": "quillfield_drought_management_plan_2024.pdf",
    "permit": "quillfield_withdrawal_permit_wd0417.pdf",
    "station": "varrow_river_station_description.pdf",
    "offer": "castlewick_interconnect_offer_2027.pdf",
    "notices": "quillfield_drought_notices_2012_2026.csv",
    "scada": "quillfield_wtp_scada_daily_2012_2026.csv",
    "elmhollow": "elm_hollow_master_meter_daily_reads.csv",
    "welllog": "hollow_road_operator_log_2023_2026.csv",
    "meters": "quillfield_meter_register.xlsx",
    "dict": "data_dictionary.csv",
    "index": "folder_contents.csv",
    "regression": "swrb_regional_low_flow_regression_2019.pdf",
    "precip": "quillfield_2nw_monthly_precipitation.csv",
}
DISTRACTORS = ("regression", "precip")
GOLDEN = {"memo": "quillfield_interconnect_reservation_2027.pdf", "table": "varrow_river_annual_low_flows.csv"}

# ---------------------------------------------------------------- the town's records
RADIO_FAILED = dt.date(2023, 6, 14)
RESTORE = (dt.date(2020, 8, 3), dt.date(2020, 8, 23))     # the historian restore re-sent these days


def mgd(cfs):
    return cfs * MGD_PER_CFS


def cfs(mgd_):
    return mgd_ / MGD_PER_CFS


def climatic_year(d):
    return d.year if d.month >= 4 else d.year - 1


def round_dv(q):
    """The Survey's daily values: three significant figures, never more than two decimals."""
    if q < 10:
        return round(q + 1e-12, 2)
    if q < 100:
        return round(q + 1e-12, 1)
    return float(int(math.floor(q + 0.5)))
