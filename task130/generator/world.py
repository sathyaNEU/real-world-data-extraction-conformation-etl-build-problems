"""The world of Redbud Line Services, a Georgia power line contractor working Pinewater EMC's system: its districts,
crews and technicians, the true injury rates, the recognition programme's rules and the reporting choice its
crews make under them. Every name, record and figure is fictional."""
import datetime as dt

SEED = 130624
BURN0 = dt.date(2020, 9, 28)       # the simulation starts here (staffing and turnover settle before the records)
HIST0 = dt.date(2021, 1, 11)       # first biweekly pay period in the extracts (Monday); HR-14 Revision 2 starts
#                                    every crew's count afresh on this day
HIST1 = dt.date(2026, 9, 27)       # last day in the timesheet extract (Sunday): pay period 20 of payroll year 2026
LOG1 = dt.date(2026, 10, 9)        # the case export's cut
CUTOVER = dt.date(2024, 6, 1)      # the case management system replaces the legacy EHS log
RENAME = dt.date(2025, 3, 2)       # the Lakes district takes over part of Piedmont, crews recoded
ASOF = dt.date(2026, 10, 16)       # when the director's team pulls the extracts
YEAR = 2027

COMPANY = "Redbud Line Services"
CLIENT = "Pinewater Electric Membership Corporation"
CLIENT_SHORT = "Pinewater EMC"
PEOPLE = {
    "director": "Samantha Galvan",      # Redbud's director of environment, health and safety
    "client": "Jerome Warren",          # Pinewater's contractor safety manager
    "ops": "Norma Hinton",              # Redbud's vice president of operations
    "payroll": "Sergio Phillips",       # Redbud's payroll and benefits manager
}

DISTRICTS = ["Blue Ridge", "Piedmont", "Lakes", "Coastal"]
DCODE = {"Blue Ridge": "BR", "Piedmont": "PD", "Lakes": "LK", "Coastal": "CS"}

# crew types: crews in Redbud's recognition programme. size is the crew's head count, rate the true recordable
# injuries per 200,000 hours worked; n is the number of crews of the type in each district.
CREW_TYPES = {
    "OH": dict(name="Overhead line", size=6, rate=3.90, n={"Blue Ridge": 80, "Piedmont": 110, "Lakes": 73, "Coastal": 125}),
    "UG": dict(name="Underground distribution", size=5, rate=2.90, n={"Blue Ridge": 35, "Piedmont": 75, "Lakes": 50, "Coastal": 55}),
    "SUB": dict(name="Substation", size=5, rate=2.40, n={"Blue Ridge": 18, "Piedmont": 30, "Lakes": 20, "Coastal": 27}),
    "VEG": dict(name="Vegetation management", size=4, rate=4.30, n={"Blue Ridge": 88, "Piedmont": 65, "Lakes": 57, "Coastal": 92}),
}
CREW_SIGMA = 0.22                  # lognormal spread of each crew's own rate around its type's
# technicians work alone and sit outside the recognition programme
TECH_TYPES = {
    "MTR": dict(name="Meter services", rate=1.70, n={"Blue Ridge": 105, "Piedmont": 165, "Lakes": 120, "Coastal": 150}),
    "LOC": dict(name="Underground locating", rate=2.30, n={"Blue Ridge": 60, "Piedmont": 120, "Lakes": 90, "Coastal": 105}),
}
TECH_SIGMA = 0.20

# the recognition programme: a crew earns USD 150 a member for every 90 consecutive calendar days without a
# recordable injury; a recordable on any of its members restarts the count from the day after the injury
MILESTONE = 90
BONUS = 150

# the reporting choice: an injury that keeps the worker off work the next day (days away) cannot be kept off the
# log; one that ends in restricted duty or medical treatment only goes unreported with a chance that rises from
# nil at day 35 of the crew's cycle to 85 per cent at day 60 and stays there to the milestone
HIDE_FROM = 35
HIDE_FULL = 60
P_REPORT_END = 0.15
CASE_MIX = (("DA", 0.15), ("RW", 0.23), ("MT", 0.62))
FIRST_AID_PER_RECORDABLE = 2.6     # first-aid cases logged per true recordable, never hidden

# the 24-hour nurse line that came with the case management system: an injured worker who calls it gets a case
# opened by the line's interface, always as first aid, dated the day of the call and never revised; the
# supervisor's own report, when there is one, goes in as a separate case. A recordable injury always has the
# supervisor's case; a first-aid injury the nurse line handled often has none.
NURSE_CALL = {"FA": 0.50, "MT": 0.32, "RW": 0.22, "DA": 0.10}   # share of injuries whose worker calls the line
NURSE_ALSO_REPORTED = 0.48         # share of nurse-line first-aid injuries the supervisor also reports
NURSE_LAG = ((0, 0.42), (1, 0.40), (2, 0.11), (3, 0.07))       # days from the injury to the call

# hours: a crew day is about 9.6 hours a member present; members take paid leave on about 4 per cent of days
DAY_HOURS = 9.6
PTO_SHARE = 0.042
WEEKEND_CALLOUT = 0.07             # chance a crew is called out on a weekend day
CALLOUT_HOURS = 5.5
# mutual-aid deployments off Pinewater's system (hours and cases outside the client's standard)
MUTUAL_AID = [(dt.date(2021, 8, 30), dt.date(2021, 9, 10), 0.18),
              (dt.date(2022, 9, 30), dt.date(2022, 10, 11), 0.22),
              (dt.date(2023, 8, 31), dt.date(2023, 9, 7), 0.12),
              (dt.date(2024, 10, 10), dt.date(2024, 10, 21), 0.26),
              (dt.date(2026, 3, 16), dt.date(2026, 3, 22), 0.10)]
MUTUAL_AID_RISK = 1.35
# storm support inside Pinewater's system: crews from two districts sent to a third for restoration, their
# timesheet rows coded to the district they worked in (Pinewater work)
SUPPORT = [(dt.date(2023, 1, 9), dt.date(2023, 1, 18), "Blue Ridge", ("Piedmont",), 0.10),
           (dt.date(2024, 8, 5), dt.date(2024, 8, 14), "Coastal", ("Lakes", "Piedmont"), 0.10),
           (dt.date(2026, 2, 9), dt.date(2026, 2, 20), "Blue Ridge", ("Piedmont", "Lakes"), 0.16),
           (dt.date(2026, 6, 15), dt.date(2026, 6, 26), "Coastal", ("Lakes", "Piedmont"), 0.14),
           (dt.date(2026, 8, 17), dt.date(2026, 8, 28), "Lakes", ("Coastal", "Blue Ridge"), 0.14)]

# the 2027 work plan: hours by district, crew type and quarter, Pinewater's 2027 release
PLAN_GROWTH = {"Blue Ridge": 1.02, "Piedmont": 1.00, "Lakes": 1.04, "Coastal": 1.03}
QUARTER_SHARE = (0.236, 0.258, 0.262, 0.244)
# each unit type's own season on the 2027 plan (per cent of its year by quarter), and each district's small lean
QUARTER_PROFILE = {"OH": (23.4, 25.6, 26.9, 24.1), "UG": (22.1, 26.4, 27.6, 23.9), "SUB": (24.6, 26.3, 22.7, 26.4),
                   "VEG": (20.4, 27.6, 29.1, 22.9), "MTR": (24.7, 25.1, 25.3, 24.9), "LOC": (21.6, 26.9, 28.1, 23.4)}
DISTRICT_LEAN = {"Blue Ridge": (-0.6, 0.2, 0.7, -0.3), "Piedmont": (0.0, 0.1, -0.2, 0.1),
                 "Lakes": (-0.4, 0.5, 0.3, -0.4), "Coastal": (0.5, -0.3, -0.5, 0.3)}

LIMIT = 3.0                        # the standard's ceiling on the contract year's recordable rate
RATE_BASE = 200000


def holidays(year):
    """Redbud's paid holidays: New Year's Day, Memorial Day, Independence Day, Labor Day, Thanksgiving and the day
    after, Christmas Eve and Christmas Day (observed on the nearest weekday)."""
    def nth(month, weekday, n):
        d = dt.date(year, month, 1)
        while d.weekday() != weekday:
            d += dt.timedelta(days=1)
        return d + dt.timedelta(days=7 * (n - 1))

    def last(month, weekday):
        d = dt.date(year, month + 1, 1) - dt.timedelta(days=1) if month < 12 else dt.date(year, 12, 31)
        while d.weekday() != weekday:
            d -= dt.timedelta(days=1)
        return d

    def observed(d):
        return d - dt.timedelta(days=1) if d.weekday() == 5 else d + dt.timedelta(days=1) if d.weekday() == 6 else d
    thanks = nth(11, 3, 4)
    days = {observed(dt.date(year, 1, 1)), last(5, 0), observed(dt.date(year, 7, 4)), nth(9, 0, 1), thanks,
            thanks + dt.timedelta(days=1), observed(dt.date(year, 12, 24)), observed(dt.date(year, 12, 25))}
    return days
