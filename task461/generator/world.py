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
# The tenancy schedule's premises lines: (premises, occupier, floors, NLA m2, term start, term end, basis)
PREMISES = [
    ("Levels 1 and 2", "Ostrand Legal LLP", "1 and 2", 3150, "2019-09-01", "2029-08-31", "Lease"),
    ("Level 3", "Fenmore Studio Architects Ltd", "3", 1540, "2021-04-01", "2026-12-31", "Lease"),
    ("Levels 4 to 6", "Varnhold Insurance Services Ltd", "4 to 6", 4710, "2020-11-01", "2030-10-31", "Lease"),
    ("Ground floor suite G.04", "Varnhold Insurance Services Ltd", "G", 145, "2023-06-01", "2030-10-31",
     "Lease (data room)"),
    ("Level 7", "Orrin Health Clinics Ltd", "7", 1570, "2022-06-01", "2027-05-31", "Lease"),
    ("Level 8", "Tamsett Analytics Ltd", "8", 1575, "2018-05-14", "2028-05-13", "Lease"),
    ("Level 9", "Tamsett Analytics Ltd", "9", 1565, "2022-02-01", "2028-05-13", "Lease"),
    ("Level 10", "Selcourt Capital LLP", "10", 1560, "2023-01-09", "2028-01-08", "Lease"),
    ("Levels 11 and 12", "Mordaunt Partners LLP", "11 and 12", 3160, "2014-03-25", "2027-03-24", "Lease"),
    ("Level 13", "Brindle & Moss Ltd", "13", 1530, "2024-07-01", "2029-06-30", "Lease"),
]
VACANT_M2 = NLA_M2 - sum(x[3] for x in PREMISES)   # the rest of the ground floor, unlet all year
# (meter tag, occupier, location, kind, parent supply tag or None). Every tenancy meter carries one description in
# the register; which are supplies and which sit inside one is in the wiring, not in the register.
METERS = [
    ("EM-101", "Ostrand Legal LLP", "L2 east riser", "supply", None),
    ("EM-102", "Ostrand Legal LLP", "L2 east riser", "room", "EM-101"),
    ("EM-103", "Fenmore Studio Architects Ltd", "L3 east riser", "supply", None),
    ("EM-104", "Varnhold Insurance Services Ltd", "L4 east riser", "supply", None),
    ("EM-105", "Varnhold Insurance Services Ltd", "L5 east riser", "room", "EM-104"),
    ("EM-106", "Orrin Health Clinics Ltd", "L7 east riser", "supply", None),
    ("EM-119", "Orrin Health Clinics Ltd", "L7 east riser", "flat", None),
    ("EM-107", "Tamsett Analytics Ltd", "L8 east riser", "supply", None),
    ("EM-108", "Tamsett Analytics Ltd", "L9 east riser", "room", "EM-115"),
    ("EM-109", "Selcourt Capital LLP", "L10 east riser", "supply", None),
    ("EM-110", "Mordaunt Partners LLP", "L11 east riser", "supply", None),
    ("EM-116", "Mordaunt Partners LLP", "L12 east riser", "supply", None),
    ("EM-112", "Brindle & Moss Ltd", "L13 east riser", "supply", None),
    ("EM-117", "Brindle & Moss Ltd", "L13 east riser", "kitchen", "EM-112"),
    ("EM-113", "Varnhold Insurance Services Ltd", "Ground floor east riser", "flat", None),
    ("EM-114", CARRIER, "Roof plant room", "flat", None),
    ("EM-115", "Tamsett Analytics Ltd", "L9 east riser", "supply", None),
    ("EM-118", "Mordaunt Partners LLP", "L11 east riser", "supply", None),
    ("EM-201", "Base building", "Basement switch room", "base", None),
    ("EM-202", "Base building", "Lift motor room", "base", None),
    ("EM-203", "Base building", "Basement switch room", "base", None),
    ("EM-204", "Base building", "Car park plant room", "base", None),
]
BASE_DESC = {"EM-201": "Landlord energy meter, mechanical services board MSB-M", "EM-202": "Landlord energy meter, lifts",
             "EM-203": "Landlord energy meter, common area lighting and power",
             "EM-204": "Landlord energy meter, car park lighting and ventilation"}
TENANT_DESC = "Tenant energy meter"
# office-pattern supplies: (night kW, daytime peak kW)
OFFICE = {"EM-101": (6.5, 58.0), "EM-103": (2.4, 27.0), "EM-104": (8.0, 82.0), "EM-106": (3.1, 33.0),
          "EM-107": (2.7, 28.0), "EM-115": (2.5, 27.0), "EM-109": (2.2, 24.0), "EM-110": (2.4, 25.0),
          "EM-116": (2.2, 24.0), "EM-112": (2.9, 23.0)}
NESTED = {m[0]: m[4] for m in METERS if m[4]}                    # the golden's hierarchy (never shipped)
SUPPLIES = [m[0] for m in METERS if m[3] in ("supply", "flat") and m[0] != "EM-118"]
ROOM_KW = {"EM-102": 7.4, "EM-105": 12.6, "EM-108": 9.1}
FLAT_KW = {"EM-113": 8.2, "EM-119": 5.3}
KITCHEN = ("EM-117", 1.2, 13.5)          # a staff kitchen's base and lunchtime peak (kW), inside its tenancy
CARRIER_KW = 13.8
WH_METERS = {"EM-103", "EM-204"}                                  # older meters registering in watt-hours
REPLACED = ("EM-110", "EM-118", dt.datetime(2026, 8, 18, 10, 30))   # local time of the swap
BMS_GAP = (dt.datetime(2026, 2, 10, 1, 0), dt.datetime(2026, 2, 10, 10, 0))    # local, no rows
# The June switchboard maintenance (Saturday 13 June, local): each tenant section isolated in turn
SHUTDOWN_DAY = dt.date(2026, 6, 13)
ISOLATIONS = [("EM-101", "06:00", "06:45"), ("EM-103", "06:50", "07:30"), ("EM-104", "07:35", "08:30"),
              ("EM-106", "08:35", "09:15"), ("EM-107", "09:20", "09:55"), ("EM-115", "10:00", "10:40"),
              ("EM-109", "10:45", "11:20"), ("EM-110", "11:25", "12:05"), ("EM-116", "12:10", "12:45"),
              ("EM-112", "12:50", "13:25"), ("EM-113", "13:30", "14:00"), ("EM-119", "14:05", "14:35"),
              ("EM-114", "14:40", "15:10")]

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
