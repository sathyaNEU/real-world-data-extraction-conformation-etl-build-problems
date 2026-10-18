"""task244 constants: the Esinmi State Bureau of Statistics' quarterly labour force survey (a fictional state in south-west
Nigeria), its twelve survey districts, the rotating panel of dwellings, the supervisors' reinterview and the 2027 annual
labour market flows release. Every figure the golden owes is computed from the pack; these only drive the simulation."""
import datetime as dt

SEED = 305            # the records' and documents' generator keys (callback days and the log's clock times)
SIM_SEED = 336        # the survey simulation's key: the households, their statuses and the published flows
REINT_SEED = 69       # the reinterview's own stream within the simulation
STATE = "Esinmi"
CAPITAL = "Ode-Esinmi"
BUREAU = "Esinmi State Bureau of Statistics"
BUREAU_SHORT = "ESBS"
SURVEY = "Esinmi Labour Force Survey"
SURVEY_SHORT = "ELFS"
DIVISION = "Labour and Social Statistics Division"
FIELD = "Field Operations Department"
FORUM = "management meeting"                   # the Statistician-General and the directors, who clear each release
DOMAIN = "esinmistats.gov.ng"

STATUS = ["E", "U", "N"]                       # employed, unemployed, outside the labour force
STATUS_NAME = {"E": "Employed", "U": "Unemployed", "N": "Outside the labour force"}
STATUS_CODE = {"E": 1, "U": 2, "N": 3}
WARN_SHARE = 1.0 / 3.0                         # the classification-error warning

# ------------------------------------------------------------------ quarters
QUARTERS = ["2026Q4", "2027Q1", "2027Q2", "2027Q3", "2027Q4"]
Q_START = {"2026Q4": dt.date(2026, 10, 5), "2027Q1": dt.date(2027, 1, 11), "2027Q2": dt.date(2027, 4, 5),
           "2027Q3": dt.date(2027, 7, 5), "2027Q4": dt.date(2027, 10, 4)}
FIELD_WEEKS = 11                               # interviews run over the quarter's first eleven weeks
REINT_WINDOW = 14                              # days from the original interview
# the tablet app update, installed at each supervisor's Friday sync at the area office (from then attempt_date is the
# date of the next sync)
APP_UPDATE = {"S1": dt.date(2027, 6, 18), "S2": dt.date(2027, 6, 25), "S3": dt.date(2027, 6, 18),
              "S4": dt.date(2027, 7, 2), "S5": dt.date(2027, 6, 25), "S6": dt.date(2027, 7, 9)}
BOUNDARY_DATE = dt.date(2027, 4, 1)            # six enumeration areas move from D04 to D02
REPLAY_DAY = dt.date(2027, 5, 14)              # the uploads the server re-ingested after its restore of 17 May 2027

# ------------------------------------------------------------------ classification error
# P(recorded status | true status), rows true E, U, N; the original interview, and the supervisor's own reinterview
# answers before reconciliation (independent of the original's error given the true status)
M_ORIG = {"EU": 0.0042, "EN": 0.0080, "UE": 0.0550, "UN": 0.1250, "NE": 0.0100, "NU": 0.0140}
M_REINT = {"EU": 0.0030, "EN": 0.0060, "UE": 0.0420, "UN": 0.0950, "NE": 0.0080, "NU": 0.0110}

# ------------------------------------------------------------------ districts
# quarterly transition rates by labour market type: settled farming districts (both flows small, so classification
# error dominates both), districts where layoffs run high and few find work, districts where work is found quickly and
# rarely lost, and the high-turnover urban and market districts
ARCH = {
    "HH": dict(EU=0.0052, EN=0.031, UE=0.105, UN=0.155, NE=0.056, NU=0.0118),
    "HL": dict(EU=0.0420, EN=0.023, UE=0.092, UN=0.220, NE=0.058, NU=0.0098),
    "LH": dict(EU=0.0078, EN=0.037, UE=0.420, UN=0.088, NE=0.032, NU=0.0440),
    "LL": dict(EU=0.0470, EN=0.026, UE=0.420, UN=0.220, NE=0.045, NU=0.0430),
}
# code, name, labour market type, adults aged 15 and over (thousands, 2027 projection), household splits per quarter
DISTRICTS = [
    ("D01", "Metropolitan Core", "LL", 912.0, 0.022),
    ("D02", "Metropolitan Fringe", "LL", 684.0, 0.020),
    ("D03", "Lagoon Coast", "LH", 418.0, 0.012),
    ("D04", "Industrial Corridor", "HL", 506.0, 0.016),
    ("D05", "Cocoa Belt East", "HH", 377.0, 0.008),
    ("D06", "Cocoa Belt West", "HH", 341.0, 0.008),
    ("D07", "Northern Savanna", "HH", 296.0, 0.007),
    ("D08", "Central Hills", "HH", 324.0, 0.009),
    ("D09", "River Basin", "LH", 389.0, 0.011),
    ("D10", "Creeks", "HL", 262.0, 0.010),
    ("D11", "Market Towns", "LL", 455.0, 0.018),
    ("D12", "University Towns", "LH", 351.0, 0.015),
]
DCODES = [d[0] for d in DISTRICTS]
DNAME = {d[0]: d[1] for d in DISTRICTS}
DTYPE = {d[0]: d[2] for d in DISTRICTS}
DPOP = {d[0]: d[3] for d in DISTRICTS}
DSPLIT = {d[0]: d[4] for d in DISTRICTS}
RATE_JITTER = 0.10                             # each district's rates within 10 per cent of its type's
LONG_CAL = (0.05, 1.3, 0.7)                    # the longitudinal weights' calibration factor by sex and age group

# ------------------------------------------------------------------ sample
EAS_PER_DISTRICT = 16
DWELLINGS_PER_COHORT = 320                     # dwellings entering the panel in each district each quarter
ADULTS = [1, 2, 3, 4, 5, 6]
ADULTS_P = [0.12, 0.26, 0.24, 0.20, 0.12, 0.06]
RESP_FIRST, RESP_LATER = 0.92, 0.95            # household response at the first and at later visits
MOVE_OUT = 0.025                               # a whole household leaves its dwelling between visits
LEAVE = 0.020                                  # one adult leaves the household between visits
PROXY = 0.38                                   # an adult's answers given by another household member
INTERVIEWERS_PER_DISTRICT = 6
MOVED_EAS = [("D04", 3), ("D04", 7), ("D04", 9), ("D04", 12), ("D04", 14), ("D04", 15)]   # to D02 from 1 April 2027

# ------------------------------------------------------------------ reinterview
REINT_SHARE = 0.08                             # of responding households each quarter, every adult in them
REINT_OUTCOMES = {"in_window": 0.880, "late": 0.040, "refused": 0.035, "no_contact": 0.045}
NEVER_ATTEMPTED = 0.015                        # a selected household that left before any attempt
# one supervisor's second-quarter workload left without any attempt (on leave, not reassigned)
SUPERVISOR_GAP = {"quarter": "2027Q2", "districts": ["D09", "D10"], "share": 0.55}
SUPERVISORS = {"S1": ["D01", "D02"], "S2": ["D03", "D04"], "S3": ["D05", "D06"], "S4": ["D07", "D08"],
               "S5": ["D09", "D10"], "S6": ["D11", "D12"]}
