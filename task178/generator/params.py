"""task178 architecture 4: fixed parameters of the world (an aircraft maintenance organisation's 2027 C-check schedule).

Every number the generator, the analysis and the write-up use is read from here, so a parameter change moves every
file and every figure together.
"""
import datetime as dt

TASK = "task178"
SEED = 178041

# The fiction's clock: the quality forecast is written in early November 2026; every export is dated here.
EXPORT_DATE = dt.datetime(2026, 11, 6, 8, 40, 0)
AS_OF = dt.date(2026, 11, 6)
HISTORY_START = dt.date(2023, 1, 9)
HISTORY_END = dt.date(2026, 10, 31)
MIS_CUTOVER = dt.date(2025, 4, 1)          # legacy MIS export holds sessions before this local date
BADGE_REKEY = dt.date(2026, 2, 2)          # contractor badges re-keyed in the attendance system
TZ_NAME = "Europe/Lisbon"

# Organisations and people (people drawn with guard.py names --geo Portugal --locale pt_PT --seed 178).
MRO = "Ermida Aerotécnica, S.A."
MRO_SHORT = "Ermida Aerotécnica"
AIRPORT = "Valdessa"
HANGAR = "Hangar 3"
AIRLINE = "Cotovia Linhas Aéreas, S.A."
AIRLINE_SHORT = "Cotovia"
OTHER_CUSTOMER = "Brisamar Charter, Lda."
CONTRACT = "HMSA-2024-11"
QP = "QP-07"
PEOPLE = {
    "accountable_manager": "Filipe Pacheco",
    "quality_manager": "Yara Faria",
    "planning_manager": "Dinis Melo",
    "operator_technical_director": "Eva Moura",
    "operator_contracts": "Micael Freitas",
    "hangar_manager": "Alícia Rodrigues",
}

# The contract's check-quality KPI (Schedule 4): mean check-related defects per C-check over a contract year.
KPI_DEFECTS_PER_CHECK = 30.0
OPERATOR_WINDOW_DAYS = 30

# Hangar practice.
SHIFTS = {"D": (6, 0, 14, 30), "L": (14, 0, 22, 30)}   # local start h, m, end h, m (half-hour handover overlap)
AREAS = [  # (new MIS name, legacy code, description)
    ("NOSE", "11", "Nose, radome and avionics compartment"),
    ("FWD-HOLD", "21", "Forward cargo hold and lower fuselage forward"),
    ("AFT-HOLD", "22", "Aft cargo hold and lower fuselage aft"),
    ("CABIN-FWD", "31", "Cabin forward of the overwing exits, galleys and flight deck access"),
    ("CABIN-AFT", "32", "Cabin aft of the overwing exits, aft galley and lavatories"),
    ("WING-LH", "51", "Left wing, slats, flaps and fuel tank access"),
    ("WING-RH", "52", "Right wing, slats, flaps and fuel tank access"),
    ("EMPENNAGE", "60", "Horizontal and vertical stabilisers, tail cone and APU compartment"),
    ("ENGINES", "70", "Engines, nacelles and pylons"),
    ("MLG-CENTRE", "80", "Main landing gear bays, wing-to-body fairing and centre fuselage lower"),
]
TRADES = ["AIRFRAME", "STRUCTURES", "AVIONICS", "POWERPLANT", "CABIN", "NDT"]
TRADE_FACTOR = {"AIRFRAME": 1.0, "STRUCTURES": 1.25, "AVIONICS": 0.9, "POWERPLANT": 1.1, "CABIN": 0.8, "NDT": 0.5}
PHASES = ["OPEN-UP", "INSPECT", "REPAIR", "CLOSE-UP", "TEST"]
PH_WIN = {"OPEN-UP": (0.0, 0.045), "INSPECT": (0.04, 0.22), "REPAIR": (0.20, 0.78), "CLOSE-UP": (0.80, 0.93),
          "TEST": (0.93, 1.0)}
PH_MH = {"OPEN-UP": 1.9, "INSPECT": 2.7, "REPAIR": 3.6, "CLOSE-UP": 2.5, "TEST": 2.3}
SESSION_MAX_H = 7.0
CREW_MH_PER_SHIFT = 162.0     # the hangar's standing crew on one aircraft, man-hours booked per shift
AREA_CAP = 44                 # card sessions one work area's docks and access can take in a shift

# The world's defect process (clean truth): each session's chance of a check-related defect is
# BASE x hours x trade factor x (1 + KAPPA x other sessions in its work area that shift).
BASE_RATE = 0.00205
KAPPA = 0.25
NON_CHECK_SHARE = 0.06        # defects raised and then found not check-related by the joint investigation
DUP_REPORT_SHARE = 0.05       # defects reported twice (test log and operator tech log), one defect number

# Fleet and programme.
FLEET = list(range(401, 427))
A321 = set(range(419, 427))
N_HISTORY_CHECKS = 46
PLAN_DAYS = {"A": 14, "B": 10, "C": 10}
PLAN_SEQUENCE = {"A": "phase", "B": "phase", "C": "area"}
PLAN_PAID_HOURS_FACTOR = {"A": 1.0, "B": 1.012, "C": 1.043}   # paid hours per card hour (overtime, handover)
N_2027_CHECKS = 12

# Rounding the asking sentences state.
ROUND_DEFECTS = 0.1          # forecast check-related defects per check, one decimal
ROUND_TURN_H = 1             # turn time, whole hours
ROUND_CLOCKED_H = 10         # clocked hours by trade, nearest 10
