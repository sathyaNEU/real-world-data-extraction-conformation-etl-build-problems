"""task461 architecture 3: the world's fixed facts. Wexmoor Office Trust's Pellow House, its tenancies and meters, the
standby generator and the chillers, Corvane Bank's KPI schedule, the clocks and the file names."""
import datetime as dt

SEED = 4613
ORG = "Wexmoor Office Trust plc"
ORG_SHORT = "Wexmoor Office Trust"
BUILDING = "Pellow House"
ADDRESS = "Pellow House, 22 Tanner Row, Wexmoor WX1 4DN"
BANK = "Corvane Bank plc"
CARRIER = "Mastlink Networks Ltd"
FM = "Kate Harding"
PEOPLE = {"sustainability": "Alice Evans", "facilities": "Kate Harding"}
TITLES = {"sustainability": "Head of Sustainability", "facilities": "Facilities Manager"}
CONTRACTOR = "Calbrook Cooling Services Ltd"
MPAN = "1600004417286"

D = dt.timedelta
YEAR = 2026
# UK clocks: BST from 01:00 UTC on 29 March 2026 to 01:00 UTC on 25 October 2026
BST_FROM_UTC = dt.datetime(2026, 3, 29, 1, 0)
BST_TO_UTC = dt.datetime(2026, 10, 25, 1, 0)


def offset_h(utc):
    return 1 if BST_FROM_UTC <= utc < BST_TO_UTC else 0


def to_local(utc):
    return utc + D(hours=offset_h(utc))


def local_to_utc(local):
    """Unambiguous local times only (no time inside the spring gap or the autumn repeat is ever asked)."""
    u = local - D(hours=1)
    return u if offset_h(u) == 1 else local


SIM_START_UTC = dt.datetime(2025, 12, 30, 0, 0)
SIM_END_UTC = dt.datetime(2027, 1, 3, 0, 0)
YEAR_START_UTC = local_to_utc(dt.datetime(2026, 1, 1))
YEAR_END_UTC = local_to_utc(dt.datetime(2027, 1, 1))
BANK_HOLIDAYS = {dt.date(2026, 1, 1), dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 5, 4),
                 dt.date(2026, 5, 25), dt.date(2026, 8, 31), dt.date(2026, 12, 25), dt.date(2026, 12, 28),
                 dt.date(2027, 1, 1)}

# ------------------------------------------------------------------------------------------------ the KPI schedule
NLA_M2 = 21460
FACTOR_KG_PER_KWH = 0.20705       # Schedule 9, part 2: the conversion factor for 2026
TARGET_KG_M2 = 17.6               # Schedule 9, part 3: the 2026 sustainability performance target
DIESEL_KG_PER_L = 2.6594          # Schedule 9, part 4: gas oil burned in the standby generator
GWP_R134A = 1430                  # Schedule 9, part 4: R-134a

# ------------------------------------------------------------------------------------------------ tenancies, meters
# (meter tag, description in the register, occupier, floors, kind, parent supply tag or None)
TENANTS = {
    "Ostrand Legal LLP": dict(floors="1 and 2", nla=3150, night=6.5, peak=58.0),
    "Fenmore Studio Architects Ltd": dict(floors="3", nla=1540, night=2.4, peak=27.0),
    "Varnhold Insurance Services Ltd": dict(floors="4 to 6", nla=4710, night=8.0, peak=82.0),
    "Orrin Health Clinics Ltd": dict(floors="7", nla=1570, night=3.1, peak=33.0),
    "Tamsett Analytics Ltd": dict(floors="8 and 9", nla=3140, night=5.2, peak=55.0),
    "Selcourt Capital LLP": dict(floors="10", nla=1560, night=2.2, peak=24.0),
    "Mordaunt Partners LLP": dict(floors="11 and 12", nla=3160, night=4.6, peak=49.0),
    "Brindle & Moss Ltd": dict(floors="13", nla=1530, night=2.0, peak=23.0),
}
VACANT_M2 = NLA_M2 - sum(t["nla"] for t in TENANTS.values())   # the ground floor suite, unlet all year
METERS = [
    ("EM-101", "L1-L2 tenancy supply", "Ostrand Legal LLP", "supply", None),
    ("EM-102", "L2 comms room", "Ostrand Legal LLP", "room", "EM-101"),
    ("EM-103", "L3 tenancy supply", "Fenmore Studio Architects Ltd", "supply", None),
    ("EM-104", "L4-L6 tenancy supply", "Varnhold Insurance Services Ltd", "supply", None),
    ("EM-105", "L5 comms room", "Varnhold Insurance Services Ltd", "room", "EM-104"),
    ("EM-106", "L7 tenancy supply", "Orrin Health Clinics Ltd", "supply", None),
    ("EM-107", "L8-L9 tenancy supply", "Tamsett Analytics Ltd", "supply", None),
    ("EM-108", "L9 server room", "Tamsett Analytics Ltd", "room", "EM-107"),
    ("EM-109", "L10 tenancy supply", "Selcourt Capital LLP", "supply", None),
    ("EM-110", "L11-L12 tenancy supply", "Mordaunt Partners LLP", "supply", None),
    ("EM-112", "L13 tenancy supply", "Brindle & Moss Ltd", "supply", None),
    ("EM-114", "Roof comms equipment room", CARRIER, "supply", None),
    ("EM-118", "L11-L12 tenancy supply", "Mordaunt Partners LLP", "supply", None),
    ("EM-201", "Mechanical services board MSB-M", "Base building", "base", None),
    ("EM-202", "Lifts", "Base building", "base", None),
    ("EM-203", "Common area lighting and power", "Base building", "base", None),
    ("EM-204", "Car park lighting and ventilation", "Base building", "base", None),
]
NESTED = {m[0]: m[4] for m in METERS if m[4]}                    # the golden's hierarchy (never shipped)
ROOM_KW = {"EM-102": 7.4, "EM-105": 12.6, "EM-108": 9.1}
CARRIER_KW = 13.8
WH_METERS = {"EM-103", "EM-204"}                                  # older meters registering in watt-hours
REPLACED = ("EM-110", "EM-118", dt.datetime(2026, 8, 18, 10, 30))   # local time of the swap
BMS_GAP = (dt.datetime(2026, 2, 10, 1, 0), dt.datetime(2026, 2, 10, 10, 0))    # local, no rows
# The June switchboard maintenance (Saturday 13 June, local): each tenant section isolated in turn
SHUTDOWN_DAY = dt.date(2026, 6, 13)
ISOLATIONS = [("EM-101", "06:00", "06:45"), ("EM-103", "06:50", "07:30"), ("EM-104", "07:35", "08:30"),
              ("EM-106", "08:35", "09:15"), ("EM-107", "09:20", "10:10"), ("EM-109", "10:15", "10:50"),
              ("EM-110", "10:55", "11:40"), ("EM-112", "11:45", "12:20"), ("EM-114", "13:30", "14:00")]

# ------------------------------------------------------------------------------------------------ the generator
TANK_DIAMETER_MM = 1250
TANK_LENGTH_MM = 2100
OFFLOAD_LPH = 17.5
ONLOAD_LPH = 82.0
DIP_TIME = (7, 30)                 # Monday dips, local

# ------------------------------------------------------------------------------------------------ the chillers
CHILLERS = {"CH-1": dict(charge=186.0, code="PH-03", retube=dt.datetime(2026, 3, 10, 9, 0), loss=3.1,
                         topups=[(dt.datetime(2026, 1, 21, 11, 0), 4.5), (dt.datetime(2026, 10, 14, 10, 30), 3.2)]),
            "CH-2": dict(charge=186.0, code="PH-01", retube=dt.datetime(2026, 6, 16, 8, 30), loss=6.4,
                         topups=[(dt.datetime(2026, 2, 18, 9, 30), 6.8), (dt.datetime(2026, 8, 12, 14, 0), 2.4),
                                 (dt.datetime(2026, 12, 9, 10, 0), 5.1)]),
            "CH-3": dict(charge=240.0, code="PH-04", retube=dt.datetime(2026, 9, 8, 8, 0), loss=5.2,
                         topups=[(dt.datetime(2026, 5, 27, 13, 0), 9.6)]),
            "CH-4": dict(charge=240.0, code="PH-02", retube=dt.datetime(2026, 11, 3, 8, 30), loss=8.9,
                         topups=[(dt.datetime(2026, 4, 22, 10, 0), 3.9), (dt.datetime(2026, 7, 15, 11, 30), 7.7)])}

# ------------------------------------------------------------------------------------------------ files
FILES = {
    "schedule": "corvane_rcf_schedule9_sustainability_kpis.pdf",
    "hh": "supplier_hh_import_1600004417286_2026.csv",
    "bms": "bms_energy_meter_registers_2026.csv",
    "register": "pellow_house_meter_register.xlsx",
    "tenancy": "pellow_house_tenancy_schedule_2026.xlsx",
    "dips": "generator_tank_dips_2026.csv",
    "calib": "generator_day_tank_calibration.xlsx",
    "dockets": "gas_oil_delivery_dockets_2026.csv",
    "runs": "generator_controller_events_2026.csv",
    "fgas": "fgas_log_chillers_2026.csv",
    "recovery": "calbrook_recovery_record_2026.xlsx",
    "weather": "met_wexmoor_daily_2026.csv",
    "epc": "pellow_house_epc_2024.pdf",
}
DISTRACTORS = ["weather", "epc"]
GOLDEN = {"report": "pellow_house_2026_kpi_report.xlsx", "letter": "pellow_house_2026_kpi_letter.pdf"}
AS_OF = dt.date(2027, 1, 15)
