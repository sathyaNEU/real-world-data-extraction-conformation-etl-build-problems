"""The world of task453: a national statistics office's monthly Labour Force Survey, kept in six rotation groups,
moving to a redesigned questionnaire through the dwellings entering the sample from July 2025, and the statutory
trigger of the Regional Employment Support Act 2021 that reads the survey's regional rates.

Everything the pack holds is computed forward from these constants: the sample, the responses, the weighted cells
both collection systems export, the published release and the fourth-quarter fieldwork log."""
import numpy as np

SEED = 453

OFFICE = "Statistics Office"
STATISTICIAN = "Government Statistician"
SURVEY = "Labour Force Survey"
ACT = "Regional Employment Support Act 2021"
MINISTRY = "Ministry of Employment and Skills"
OLD_SYSTEM = "CAI 2014"            # the computer-assisted interviewing system the previous questionnaire ran on
NEW_SYSTEM = "ICS"                 # the integrated collection system the redesigned questionnaire runs on
TRIGGER = 6.0

PEOPLE = {"statistician": "Jared Elliott", "methods": "Debra O'Brien", "operations": "Gabrielle Esson"}

# regions on the 2025 classification (code, name); the 2019 classification numbered the same regions alphabetically
REGIONS = [("01", "Capital"), ("02", "Harbour"), ("03", "North Coast"), ("04", "Inland Plains"),
           ("05", "Eastern Ranges"), ("06", "Southern Valleys"), ("07", "Western Coast"), ("08", "River Delta"),
           ("09", "Highlands")]
RCODE = [c for c, _ in REGIONS]
RNAME = dict(REGIONS)
CODE19 = {c: "%02d" % (1 + sorted(RNAME.values()).index(n)) for c, n in REGIONS}
R = len(REGIONS)

# months: January 2022 to December 2026; the redesign enters with the rotation group replaced in July 2025
MONTHS = ["%d-%02d" % (y, m) for y in range(2022, 2027) for m in range(1, 13)]
T = len(MONTHS)
PHASE = MONTHS.index("2025-07")
Y26 = MONTHS.index("2026-01")
Q4 = [MONTHS.index(m) for m in ("2026-10", "2026-11", "2026-12")]
GROUPS = "ABCDEF"                   # group A's dwellings are replaced in January and July, B's in February and August


def mis(t, g):
    """month in sample (1 to 6) of rotation group g (0 for A .. 5 for F) in month index t (January 2022 is 0)"""
    return ((t - g) % 6) + 1


def entered(t, g):
    """the month index in which group g's dwellings of month t entered the sample"""
    return t - (mis(t, g) - 1)


def redesigned(t, g):
    return entered(t, g) >= PHASE


# persons aged 15 and over (thousands, January 2026) by region; age and sex structure
POP15 = np.array([9150, 5240, 3290, 4130, 2280, 2940, 1910, 3680, 1430], float)
AGES = ["15-24", "25-34", "35-44", "45-54", "55+"]
AGE_SHARE = np.array([0.155, 0.178, 0.168, 0.162, 0.337])
SEX = ["M", "F"]
SEX_SHARE = np.array([0.49, 0.51])
PART = np.array([[0.63, 0.92, 0.93, 0.90, 0.44], [0.57, 0.80, 0.81, 0.79, 0.34]])   # participation, sex x age
UFAC = np.array([[2.15, 1.10, 0.80, 0.74, 0.79], [2.02, 1.12, 0.84, 0.78, 0.74]])   # unemployment against the region

# each region's 2026 unemployment rate on the redesigned questionnaire (the generator tunes the regional level to it)
TARGET26 = {"01": 4.32, "02": 5.38, "03": 6.44, "04": 6.21, "05": 6.60, "06": 4.91, "07": 6.64, "08": 7.45, "09": 8.31}

SEAS = np.array([0.45, 0.35, 0.15, -0.10, -0.30, -0.35, -0.05, 0.05, -0.15, -0.20, -0.05, 0.20])
# the national cycle: easing through 2022 and 2023, flat into 2024, edging up from mid-2025
NAT = np.interp(np.arange(T), [0, 12, 24, 30, 36, 42, 48, 54, 59],
                [0.40, 0.10, -0.15, -0.25, -0.22, -0.12, 0.02, 0.10, 0.14])
DRIFT = {"01": -0.10, "02": 0.15, "03": 0.30, "04": -0.20, "05": 0.25, "06": -0.15, "07": 0.10, "08": 0.20, "09": -0.25}

# the previous questionnaire's rotation-group bias (points, by month in sample) and the redesign's effect on it
MIS_BIAS = np.array([1.30, 0.15, -0.12, -0.30, -0.45, -0.58])
FIRST_EFFECT = -0.45          # the revised job-search questions at a first interview
LATER_EFFECT = 0.688          # the revised questions with dependent interviewing, second to sixth interview

# the sample: primary sampling units allocated by the square root of each region's population, 12 dwellings in each
# rotation group of a unit, one rotation group replaced each month
PSUS = 1180
LINES = 12
VACANT = 0.072                # dwellings found vacant (code 31), derelict or demolished (code 32)
DERELICT = 0.006              # of which derelict or demolished
NONPRIVATE = 0.013            # not private dwellings (code 33)
RESPONSE = np.array([0.82, 0.79, 0.78, 0.77, 0.76, 0.75])   # eligible dwellings responding, by month in sample
# response is lowest in the Capital's apartment blocks and highest in the rural regions, dips over the summer holidays
# and in July, and drifts down a little each year
RESP_REGION = {"01": -0.050, "02": -0.024, "03": 0.011, "04": 0.026, "05": 0.017, "06": 0.004, "07": 0.031,
               "08": -0.009, "09": 0.043}
RESP_MONTH = np.array([-0.031, -0.009, 0.0, 0.004, 0.006, 0.003, -0.011, -0.004, 0.003, 0.005, 0.002, -0.023])
RESP_TREND = -0.008           # a year
RESP_SEAS_AMP = {"01": 1.35, "02": 1.15, "03": 0.95, "04": 0.80, "05": 1.00, "06": 0.85, "07": 1.10, "08": 0.90,
                 "09": 0.70}   # the summer dip deepest in the cities
PARTIAL = 0.06                # responding interviews only partly completed (code 12)
PERSONS = 2.42                # persons aged 15 and over in a responding dwelling

EXTRACT = "2027-01-25"
RELEASE = "2027-01-21"        # Labour Force Survey, December 2026


def response(t, code, m):
    """the chance an eligible dwelling responds in month t, in region code, at month in sample m"""
    return RESPONSE[m - 1] + RESP_REGION[code] + RESP_MONTH[t % 12] * RESP_SEAS_AMP[code] + RESP_TREND * t / 12.0
