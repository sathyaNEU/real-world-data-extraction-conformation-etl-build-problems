"""The fiction's constants: the market, its North Hub and Redrock Draw's own settlement point, the battery and its
warranty, the owner's dispatch policy and threshold menu, the battery's 2026 operating events, the people, the dates and
the file names."""
import datetime as dt

SEED = 4612027

ORG = "Tallgrove Storage Partners, LLC"
ORG_SHORT = "Tallgrove"
PROJECT = "Redrock Draw Energy Storage"
PROJECT_SHORT = "Redrock Draw"
MARKET = "Midplains Power Market"
OPERATOR = "Midplains Interconnection, Inc."
OPERATOR_SHORT = "MPI"
HUB = "MP_NORTH_HUB"
HUB_NAME = "North Hub"
NODE_OLD = "RDRW_ESS1_RN"            # the node's name when it was created
NODE = "REDROCK_ESS_RN"              # after the March 2026 network model update
RESOURCE = "REDROCK_ESS1"            # the battery's market resource (constant through the rename)
NODE_RENAME = dt.date(2026, 3, 18)   # first operating day under the new name
NODE_CREATED = dt.date(2025, 12, 2)  # first operating day the market priced the node
NODE_PROVISIONAL_END = dt.date(2025, 12, 15)   # priced at the hub until the network model carried the resource
OEM = "Cordell Energy Systems"
QSE = "Barrowfield Energy Trading"
PEOPLE = {"asset": "Stacey Garrett", "analyst": "Hailey Cooper"}
TITLES = {"asset": "Asset Manager, Storage", "analyst": "Market Analyst"}
OEM_ENGINEER = "Cordell field services"

POWER_MW = 100.0
RATED_MWH = 400.0                    # Rated Energy: one Full Cycle is this much DC discharge
WARRANTY_CYCLES = 300
DC_TO_POI = 0.975                    # the warranty's conversion from energy at the meter to the DC terminals
RTE_AC = 0.86
MENU = [5, 10, 15, 20, 25, 30, 35, 40]           # the trading system's threshold settings, $/MWh
SETTING_2026 = 35

# Dates in the fiction.
WARRANTY_DATE = dt.date(2025, 6, 27)
COD = dt.date(2025, 12, 29)
POLICY_DATE = dt.date(2026, 2, 6)
FIRMWARE = dt.datetime(2026, 6, 23, 15, 0)        # UTC: the BMS firmware update (mode codes change after it)
TESTS = [dt.date(2026, 3, 12), dt.date(2026, 9, 14)]
ARCHIVE_PULL = dt.date(2026, 11, 2)
BMS_PULL = dt.date(2026, 11, 3)
METER_PULL = dt.date(2026, 11, 3)
SETTLE_PULL = dt.date(2026, 11, 4)
PACK_DATE = dt.date(2026, 11, 6)
PARAM_DUE = dt.date(2026, 12, 1)
MEMO_DATE = dt.date(2026, 11, 20)
OPS_FIRST = dt.date(2026, 1, 1)
OPS_LAST = dt.date(2026, 10, 31)

# Price model. Each day's swing (evening peak over the midday trough and the night) is set by the season and the
# weather; in windy stretches the swing's spread across days widens (more flat days and more sharp ones) while its
# average holds. The node's prices swing with the hub's, amplified by the congestion between them.
WINDY = [(dt.date(2019, 10, 1), dt.date(2020, 11, 15)), (dt.date(2025, 10, 1), dt.date(2026, 12, 31))]
SIG_ORDINARY = 0.55
SIG_WINDY = 0.90
SKEW_MIX = 0.30
SWING_SCALE = 1.017
LEVEL_WINDY = 3.0
NODE_K = 2.2
NODE_K_SD = 0.10
NODE_BASIS = -1.8

FILES = {
    "hub": "mpi_dam_settlement_point_prices_north_hub_2019_2026.csv",
    "node": "mpi_dam_settlement_point_prices_redrock_2025_2026.csv",
    "points": "mpi_settlement_point_list_2026.csv",
    "rt": "mpi_rtm_settlement_point_prices_north_hub_2026.csv",
    "as_prices": "mpi_dam_ancillary_service_clearing_prices_2026.csv",
    "bms": "redrock_draw_bms_hourly_export_2026.csv",
    "meter": "redrock_draw_revenue_meter_15min_2026.csv",
    "settle": "redrock_draw_dam_settlement_statement_lines_2026.csv",
    "policy": "tallgrove_storage_dispatch_policy_2026.pdf",
    "warranty": "redrock_draw_supply_warranty_excerpt.pdf",
    "tests": "cordell_capacity_tests_2026.pdf",
    "dict": "redrock_threshold_data_dictionary.xlsx",
    "manifest": "redrock_threshold_extract_manifest.csv",
}
GOLDEN = {"workbook": "redrock_draw_2027_cycling_threshold.xlsx", "daily": "redrock_draw_daily_spreads_conformed.csv"}
DISTRACTORS = ["rt", "as_prices"]
