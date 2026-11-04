"""task461 architecture 2: the world's fixed facts. Brennock Fuels' Warrenby terminal, its fleet, its tanks, the
Coastal Air Quality Authority's licence and return protocol, the clocks and the file names."""
import datetime as dt
import math

SEED = 4770
ORG = "Brennock Fuels Pty Ltd"
ORG_SHORT = "Brennock Fuels"
TERMINAL = "Warrenby terminal"
CITY = "Warrenby"
AUTHORITY = "Coastal Air Quality Authority"
AUTH_SHORT = "the Authority"
LICENCE_NO = "20514"
CARRIER = "Oakhurst Haulage"
PARTNER = "Tarrant Energy"
PARTNER_TERMINAL = "Selwyn Point"
PEOPLE = {"manager": "Anna Gardner", "dispatch": "Jeffrey Pruitt"}
TITLES = {"manager": "Terminal Manager", "dispatch": "Dispatch Manager"}

# ------------------------------------------------------------------------------------------------ clocks
# Warrenby keeps AEST (UTC+10) and AEDT (UTC+11) from the first Sunday in October to the first Sunday in April.
DST_END_2026 = dt.datetime(2026, 4, 4, 16, 0)     # UTC: 03:00 AEDT on 5 April becomes 02:00 AEST
DST_START_2026 = dt.datetime(2026, 10, 3, 16, 0)  # UTC: 02:00 AEST on 4 October becomes 03:00 AEDT
SIM_START_UTC = dt.datetime(2025, 11, 30, 13, 0)  # 1 December 2025 00:00 AEDT
SIM_END_UTC = dt.datetime(2027, 1, 4, 13, 0)      # 5 January 2027 00:00 AEDT
EXPORT_END_LOCAL = dt.datetime(2027, 1, 4, 6, 0)   # the TMS and PLC exports run to 04/01/2027 06:00
YEAR_START_UTC = dt.datetime(2025, 12, 31, 13, 0)  # 1 January 2026 00:00 AEDT
YEAR_END_UTC = dt.datetime(2026, 12, 31, 13, 0)    # 1 January 2027 00:00 AEDT


def offset_h(utc):
    return 10 if DST_END_2026 <= utc < DST_START_2026 else 11


def to_local(utc):
    return utc + dt.timedelta(hours=offset_h(utc))


def local_to_utc(local):
    """Local wall time to UTC (no event is placed in the repeated or skipped hour)."""
    for h in (11, 10):
        u = local - dt.timedelta(hours=h)
        if offset_h(u) == h:
            return u
    raise ValueError(local)


def quarter_bounds_utc():
    """Each 2026 quarter's opening and closing local midnight, in UTC."""
    starts = [dt.datetime(2026, 1, 1), dt.datetime(2026, 4, 1), dt.datetime(2026, 7, 1), dt.datetime(2026, 10, 1),
              dt.datetime(2027, 1, 1)]
    u = [local_to_utc(s) for s in starts]
    return [(u[i], u[i + 1]) for i in range(4)]


def quarter_of_local(local):
    return (local.month - 1) // 3 + 1


# ------------------------------------------------------------------------------------------------ products
PRODUCTS = ["ULP", "P95", "P98", "DSL"]
PETROL = ["ULP", "P95", "P98"]
NAME_OLD_TAS = {"ULP": "ULP91", "P95": "PULP95", "P98": "PULP98", "DSL": "DIESEL"}
NAME_NEW_TAS = {"ULP": "ULP", "P95": "P95", "P98": "P98", "DSL": "DSL10"}
NAME_DOCKET = {"ULP": "Unleaded 91", "P95": "Premium 95", "P98": "Premium 98", "DSL": "Diesel"}
NAME_LONG = {"ULP": "Unleaded petrol 91", "P95": "Premium unleaded 95", "P98": "Premium unleaded 98", "DSL": "Diesel"}

# Return protocol, Table 1 and Table 2: ln(P / kPa) = A - B / (T + 273.15); vapour molecular weight (kg/kmol).
TVP = {"petrol_summer": (13.687, 2952.8), "petrol_winter": (13.642, 2891.9), "diesel": (14.032, 4948.3)}
VAP_MW = {"petrol_summer": 67.0, "petrol_winter": 65.0, "diesel": 130.0}
SUMMER_MONTHS = (11, 12, 1, 2, 3)
R_GAS = 8.314  # kPa m3 / (kmol K)


def grade_season(month):
    return "petrol_summer" if month in SUMMER_MONTHS else "petrol_winter"


def tvp_kpa(key, temp_c):
    a, b = TVP[key]
    return math.exp(a - b / (temp_c + 273.15))


def vapour_kg_per_kl(key, temp_c, sat):
    """kg of vapour pushed out per kilolitre of liquid loaded: S P M / (R T), the field's loading-loss form."""
    return sat * tvp_kpa(key, temp_c) * VAP_MW[key] / (R_GAS * (temp_c + 273.15))


# ------------------------------------------------------------------------------------------------ tanks
# Tank register (as at January 2027): roof, current rim seal, diameter, capacity.
TANKS = {
    "TK-1": dict(product="ULP", roof="Internal floating roof", seal="Mechanical shoe primary, rim-mounted secondary",
                 diameter_m=26.0, capacity_kl=7800, heel_kl=310, built=1987, seal_from="2026-02-18 15:40"),
    "TK-2": dict(product="P95", roof="Internal floating roof", seal="Mechanical shoe primary, rim-mounted secondary",
                 diameter_m=20.5, capacity_kl=4650, heel_kl=220, built=1994, seal_from="2026-05-12 13:15"),
    "TK-3": dict(product="P98", roof="Internal floating roof", seal="Mechanical shoe primary, rim-mounted secondary",
                 diameter_m=16.0, capacity_kl=2900, heel_kl=160, built=2003, seal_from="2026-09-03 16:05"),
    "TK-4": dict(product="DSL", roof="Fixed cone roof", seal="n/a", diameter_m=28.0, capacity_kl=9500, heel_kl=340,
                 built=1987, seal_from=None, vents_from="2026-03-12 14:20"),
    "TK-5": dict(product="DSL", roof="Fixed cone roof", seal="n/a", diameter_m=28.0, capacity_kl=9500, heel_kl=340,
                 built=2011, seal_from=None, vents_from="2026-08-19 10:50"),
}
# Return protocol, Table 3: standing loss, kg per metre of diameter per day; Table 4: working loss per ML received.
STANDING = {"ifr_primary": 0.31, "ifr_secondary": 0.12, "fixed_distillate": 0.0175, "fixed_distillate_pv": 0.0105}
WORKING = {"petrol_ifr": 6.4, "distillate_fixed": 0.9}

# ------------------------------------------------------------------------------------------------ bays
PETROL_BAYS = [1, 2, 3]
# The petrol rack's terminal automation controller failed twice; bays 1 to 3 loaded on manual bills of lading, which
# the dispatch system holds and the terminal automation system never received (local start, local end).
TAS_FAULTS = [(dt.datetime(2026, 5, 19, 9, 12), dt.datetime(2026, 5, 19, 13, 47)),
              (dt.datetime(2026, 11, 24, 10, 5), dt.datetime(2026, 11, 24, 14, 40))]


def in_tas_fault(bay, local):
    return bay in PETROL_BAYS and any(a <= local < b for a, b in TAS_FAULTS)
DISTILLATE_BAYS = [4, 5]
LOADING_POINTS = ["VRU-1", "BAY-4", "BAY-5"]
LIMIT_T = 20.0

# ------------------------------------------------------------------------------------------------ files
FILES = {
    "licence": "EPL_20514_licence_conditions.pdf",
    "protocol": "CAQA_return_protocol_petroleum_premises_2026.pdf",
    "tas_old": "tas_loads_legacy_2026-01-01_to_2026-06-30.csv",
    "tas_new": "tas_loads_2026-06-29_to_2027-01-04.xlsx",
    "dockets": "dispatch_delivery_dockets_2025-12_to_2026-12.csv",
    "tankers": "tanker_register_2027-01.xlsx",
    "sites": "delivery_sites.csv",
    "vru_cems": "vru1_outlet_cems_15min_2026.csv",
    "vru_plc": "vru1_plc_events_2026-01-01_to_2027-01-04.csv",
    "gauging": "tank_gauging_daily_2025-12-31_to_2027-01-04.csv",
    "outturns": "ship_receipts_outturn_2026.xlsx",
    "shiftlog": "control_room_shift_log_2026.csv",
    "workorders": "maintenance_work_orders_2026.csv",
    "tankreg": "tank_register_2027-01.xlsx",
    "weather": "bom_warrenby_airport_daily_2026.csv",
    "stacktest": "vru1_stack_emission_survey_2026.pdf",
}
DISTRACTORS = ["weather", "stacktest", "sites"]
GOLDEN = {"return": "warrenby_2026_annual_return.csv", "note": "warrenby_2026_return_note.pdf",
          "stock": "warrenby_2026_stock_account.xlsx"}
