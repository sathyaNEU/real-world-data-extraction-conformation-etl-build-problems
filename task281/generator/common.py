"""Constants for task281: the State of Merrimont's FY2028 overtime-relief positions.

    The world: eight round-the-clock units of four titles, staffed by fixed lines on five-day rotas, FY2026 rosters
    (1 July 2025 to 30 June 2026) as the record, FY2028 (1 July 2027 to 30 June 2028) as the year planned for."""
import datetime as dt

SEED = 699
FUNDED = 60                     # relief positions in the FY2028 allowance
K_WEEKS = 4                     # the standard: met in every week but four (the fifth-heaviest week met in full)
SHIFT_H = 8.0
WEEK_H = 40.0                   # five eight-hour shifts
FY26_START = dt.date(2025, 7, 1)
FY26_DAYS = 365
FY28_START = dt.date(2027, 7, 1)
WEEKS = 52                      # fiscal weeks counted from 1 July; the year's last day or two are left out
ASSEMBLED = dt.datetime(2026, 10, 23, 16, 40)

STATE = "State of Merrimont"
DBM = "Department of Budget and Management"
TITLES = {
    "CO": "Correctional Officer",
    "PCO": "Police Communications Operator",
    "FSA": "Forensic Security Aide",
    "HMW": "Highway Maintenance Worker",
}
TITLE_ORDER = ["CO", "PCO", "FSA", "HMW"]
AGENCY = {"CO": "Department of Public Safety, Division of Correction",
          "PCO": "Department of Public Safety, Merrimont State Police",
          "FSA": "Department of Health, Behavioral Health Administration",
          "HMW": "Department of Transportation, State Highway Administration"}
# code, name, title, posts on the day, evening and night shifts
UNITS = [
    ("HRC", "Harlan Road Correctional Facility", "CO", (5, 5, 5)),
    ("ACF", "Avesford Correctional Facility", "CO", (5, 5, 5)),
    ("TWC", "Thornmere Women's Correctional Center", "CO", (5, 5, 5)),
    ("PCN", "State Police Communications Center North", "PCO", (5, 5, 5)),
    ("PCS", "State Police Communications Center South", "PCO", (5, 5, 5)),
    ("FFH", "Fennimore Forensic Hospital, Security Nursing", "FSA", (5, 5, 5)),
    ("OXG", "Oxbow Bend Maintenance Garage", "HMW", (5, 5, 5)),
    ("KPG", "Kettle Pass Maintenance Garage", "HMW", (5, 5, 5)),
]
UNIT_CODES = [u[0] for u in UNITS]
UNIT_NAME = {u[0]: u[1] for u in UNITS}
UNIT_TITLE = {u[0]: u[2] for u in UNITS}
# the cost centres the State's budget books each unit's pay to
COST_CENTER = {"HRC": "Q00-4120", "ACF": "Q00-4140", "TWC": "Q00-4160", "PCN": "W00-2210", "PCS": "W00-2230",
               "FFH": "M00-6340", "OXG": "J02-7715", "KPG": "J02-7740"}
SHIFTS = ("D", "E", "N")
SHIFT_START = {"D": "07:00", "E": "15:00", "N": "23:00"}

# entry classes: (title, class id, academy start, graduation, first shift on post, posted). The FY2026 mid-year
# classes are the world's fill days; the FY2028 classes fill the position control's new lines.
CLASSES = [
    ("CO", "2025-1", "2025-03-10", "2025-06-27", "2025-07-01"),
    ("CO", "2025-2", "2025-07-21", "2025-10-31", "2025-11-06"),
    ("CO", "2026-1", "2025-11-17", "2026-02-27", "2026-03-05"),
    ("CO", "2026-2", "2026-03-09", "2026-06-26", "2026-07-01"),
    ("CO", "2026-3", "2026-07-20", "2026-10-30", "2026-11-05"),
    ("CO", "2027-0", "2026-11-16", "2027-02-26", "2027-03-04"),
    ("CO", "2027-1", "2027-03-08", "2027-06-25", "2027-07-01"),
    ("CO", "2027-2", "2027-06-28", "2027-10-15", "2027-10-18"),
    ("CO", "2028-1", "2027-10-04", "2028-01-21", "2028-01-24"),
    ("PCO", "2025-1", "2025-04-07", "2025-06-27", "2025-07-01"),
    ("PCO", "2026-1", "2025-10-20", "2026-01-09", "2026-01-15"),
    ("PCO", "2026-2", "2026-04-06", "2026-06-26", "2026-07-01"),
    ("PCO", "2027-0", "2026-10-19", "2027-01-08", "2027-01-14"),
    ("PCO", "2027-1", "2027-04-05", "2027-06-25", "2027-07-01"),
    ("PCO", "2027-2", "2027-09-07", "2027-12-03", "2027-12-06"),
    ("FSA", "2025-1", "2025-04-21", "2025-06-27", "2025-07-01"),
    ("FSA", "2025-2", "2025-07-21", "2025-09-26", "2025-10-01"),
    ("FSA", "2026-1", "2025-11-17", "2026-01-23", "2026-01-31"),
    ("FSA", "2026-2", "2026-04-20", "2026-06-26", "2026-07-01"),
    ("FSA", "2027-0", "2026-11-16", "2027-01-22", "2027-01-30"),
    ("FSA", "2027-1", "2027-04-19", "2027-06-25", "2027-07-01"),
    ("FSA", "2027-2", "2027-06-21", "2027-09-03", "2027-09-07"),
    ("HMW", "2025-1", "2025-05-19", "2025-06-27", "2025-07-01"),
    ("HMW", "2025-2", "2025-08-25", "2025-10-03", "2025-10-08"),
    ("HMW", "2026-2", "2026-05-18", "2026-06-26", "2026-07-01"),
    ("HMW", "2026-3", "2026-08-24", "2026-10-02", "2026-10-07"),
    ("HMW", "2027-1", "2027-05-17", "2027-06-25", "2027-07-01"),
    ("HMW", "2028-1", "2028-02-21", "2028-03-31", "2028-04-03"),
]
# the world's FY2026 fill days (day indexes) to the class that posted on them
FY26_FILL_CLASS = {("CO", 128): "2025-2", ("CO", 247): "2026-1", ("PCO", 198): "2026-1", ("FSA", 92): "2025-2",
                   ("FSA", 214): "2026-1", ("HMW", 99): "2025-2"}
# the class that fills each title's new FY2028 lines, by the fiscal week of FY2028 its posting day falls in
FY28_FILL_CLASS = {("CO", 16): "2027-2", ("CO", 30): "2028-1", ("PCO", 23): "2027-2", ("FSA", 10): "2027-2",
                   ("HMW", 40): "2028-1"}

# officers who moved to another title outside the eight units after FY2026: home unit, new title, new unit, date
# (home unit in FY2026, new title, new unit, date, and for two of them the title and unit held before the FY2026 one)
MOVERS = [("FFH", "CO", "MCI", "2026-08-10", ("HMW", "SHG")), ("PCS", "CO", "BRF", "2026-09-14", None),
          ("KPG", "PCO", "PCW", "2026-08-24", None), ("ACF", "HMW", "LMG", "2026-09-21", ("PCO", "PCW"))]
OTHER_UNITS = {"MCI": "Merrimont Correctional Institution", "BRF": "Brannock Ridge Pre-Release Facility",
               "PCW": "State Police Communications Center West", "LMG": "Lamberton Mills Maintenance Garage",
               "SHG": "Shadwell Maintenance Garage"}
PEOPLE = {"desk": "James Cohen", "director": "Linda Wolf", "recruit": "Natalie Mckinney", "payroll": "Sean Crane",
          "negotiator": "Krystal Russell", "union": "Brandon Snyder"}

FILES = {
    "rosters": "merrimont_shift_rosters_fy2026.csv",
    "employees": "hr_employee_extract_2026-10-01.csv",
    "position": "position_control_fy2028_round_the_clock_units.csv",
    "classes": "entry_class_calendar_fy2025_fy2028.csv",
    "codes": "timekeeping_status_codes.csv",
    "payroll": "payroll_overtime_lines_checks_jul2025_jul2026.csv",
    "offers": "overtime_offer_log_fy2026.csv",
    "earn": "payroll_earnings_codes.csv",
    "standard": "relief_coverage_standard.pdf",
    "memo": "fy2028_allowance_relief_positions_memo.pdf",
    "agreement": "protective_services_agreement_excerpts.pdf",
    "dictionary": "data_dictionary.txt",
    "inmates": "doc_average_daily_population_fy2026.csv",
    "cad": "msp_communications_call_volume_fy2026.csv",
    "winter": "sha_winter_operations_log_fy2026.csv",
    "otprog": "overtime_expenditure_by_program_fy2026.xlsx",
}
DISTRACTORS = ("inmates", "cad", "winter", "otprog")
GOLDEN = "fy2028_relief_positions_by_unit.xlsx"
CHART = "fy2028_weekly_backfill_need.png"
DELIVERABLES = (GOLDEN, CHART)


def fy26_day(i):
    return FY26_START + dt.timedelta(days=i)


def fy28_day(i):
    return FY28_START + dt.timedelta(days=i)


def fweek(i):
    """fiscal week (1 to 52) of day index i, or None for the year's leftover day or two"""
    w = i // 7 + 1
    return w if w <= WEEKS else None
