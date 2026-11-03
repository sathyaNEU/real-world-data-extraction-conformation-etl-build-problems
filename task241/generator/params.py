"""Constants of the task241 world (architecture 2): Kettle River Research's telephone centre, 2026."""
SEED = 241_2067
YEAR = 2026
FIRM = "Kettle River Research"
COMPANY = "Kettle River Research"
DIRECTOR = "Hailey Mullins"          # director of telephone operations
QA_LEAD = "Vincent Armstrong"        # quality assurance lead, ran the 2025 listening test
DIALER_ADMIN = "Brian Maynard"       # dialer administrator
LIMIT = 0.10                          # detection stays on only while fewer than one in ten machine-classed calls were people
CALL_OPEN, CALL_CLOSE = 8, 21         # the calling-hours rule, the called household's own local time
UPGRADE = "2026-07-01"                # the dialer software upgrade; exports from July use the new layout
INBOUND_END = "2027-01-15"            # the inbound switch extract runs to here
CERTIFIED = 0.021                     # the maker's false-machine rate on its reference set, balanced setting
LISTEN_N, LISTEN_PEOPLE = 400, 9      # the 2025 listening test on the pilot project

# detector behaviour: a person answering with a long greeting is classed as a machine far more often
Q_SHORT, Q_LONG = 0.010, 0.30
P_MACHINE_CLASSED = 0.93              # a machine (answering machine, voicemail, attendant) classed as a machine

# job, project name, 2027 client label, answered calls, machine share of answers, long-greeting share of people,
# prompt return propensity of a person hung up on, voicemail return propensity, abandoned share of live answers,
# share of sample households living away from the number's area (snowbirds, movers keeping the number)
PROJECTS = [
    ("KR-2611", "Minnesota Adult Health Survey (landline)", "state health agency", 31000, 0.44, 0.03, 0.27, 0.050, 0.065, 0.012),
    ("KR-2612", "Medicare Care Experience Survey", "regional quality improvement organization", 34000, 0.55, 0.75, 0.33, 0.050, 0.075, 0.050),
    ("KR-2613", "Large Employer Benefits Survey", "state workforce agency", 21500, 0.62, 0.10, 0.22, 0.060, 0.085, 0.004),
    ("KR-2614", "Statewide Voter Attitudes Poll", "university public affairs institute", 26000, 0.47, 0.05, 0.25, 0.055, 0.070, 0.015),
    ("KR-2615", "School Parents Survey", "school districts consortium", 16000, 0.40, 0.03, 0.24, 0.025, 0.065, 0.010),
    ("KR-2616", "Farm Operator Survey", "state agriculture department", 20500, 0.45, 0.55, 0.30, 0.055, 0.075, 0.008),
    ("KR-2617", "Crime Victimization Survey", "state statistical analysis center", 22000, 0.46, 0.08, 0.45, 0.050, 0.060, 0.014),
    ("KR-2618", "Alumni Outcomes Survey", "private university", 23000, 0.50, 0.56, 0.10, 0.040, 0.095, 0.060),
    ("KR-2619", "Cooperative Member Survey", "electric cooperative", 19500, 0.45, 0.10, 0.26, 0.030, 0.070, 0.020),
    ("KR-2620", "Veterans Health Survey", "state veterans affairs department", 30000, 0.55, 0.75, 0.34, 0.050, 0.080, 0.045),
    ("KR-2621", "Small Business Conditions Survey", "small business development network", 15000, 0.38, 0.80, 0.22, 0.060, 0.080, 0.006),
    ("KR-2622", "Retired Educators Survey", "retired educators association", 24500, 0.58, 0.07, 0.36, 0.045, 0.090, 0.070),
    ("KR-2623", "Child Care Provider Survey", "state child care resource agency", 18000, 0.36, 0.60, 0.25, 0.050, 0.075, 0.008),
]
ONE_OFF = ("KR-2624", "Library Users Study", "state library", 6000, 0.45, 0.06, 0.25, 0.03, 0.035, 0.01)  # ended in August, not recurring
PILOT_JOB = "KR-2611"

AREA_CODES = {  # area codes the samples' numbers carry, with the state the dialer's own table assigns
    "MN": ["218", "320", "507", "612", "651", "763", "952"], "WI": ["608", "715"], "IA": ["515", "712"],
    "ND": ["701"], "SD": ["605"],
}
ELSEWHERE = [("AZ", 0.34), ("FL", 0.30), ("TX", 0.12), ("CA", 0.08), ("CO", 0.06), ("IL", 0.05), ("NY", 0.05)]
# area codes of other states, for a household's second line kept from an earlier home (it rings at the household)
KEPT_CODES = {"AZ": ["480", "602", "520"], "FL": ["239", "941", "727", "561"], "CA": ["619", "760", "949"],
              "CO": ["303", "719"], "NY": ["212", "718", "914"], "TX": ["214", "512"], "IL": ["312", "847"]}
KEPT_FROM = [0.30, 0.10, 0.24, 0.16, 0.04, 0.08, 0.08]   # AZ, FL, CA, CO, NY, TX, IL: where the kept lines came from
APPT_SHARE = 0.22                     # callbacks where the respondent names another number and a time
APPT_LATE = 0.25                      # evening appointments the respondent set after 9 pm
APPT_KEPT = 0.50                      # of those numbers, the share carrying an area code from another state
REOPEN_SHARE, REOPEN_LAG = 0.10, (3, 60)    # supervisor verification callbacks on a tenth of completes, days after
INBOUND_TRANSFER_COMPLETE = 0.92
LINE_INTERVIEWS = 0.035               # interviews done when the household rings back after the last attempt, per complete      # inbound interviews the desk hands to an interviewer on a second leg
STATE_TZ = {  # state, IANA zone of the whole state as the samples reach it
    "MN": "America/Chicago", "WI": "America/Chicago", "IA": "America/Chicago", "ND": "America/Chicago",
    "SD": "America/Chicago", "IL": "America/Chicago", "TX": "America/Chicago", "AZ": "America/Phoenix",
    "FL": "America/New_York", "NY": "America/New_York", "CA": "America/Los_Angeles", "CO": "America/Denver",
}
