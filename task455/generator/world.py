"""task455: the world's constants. Wendmoor County (an invented county in an unnamed state), its residents' drug
overdose deaths 2019 to 2026 by the medical examiner's drug class, the coroner's certification practice, the state
file's close dates, the EMS system's overdose calls, and the people and organisations in the fiction."""
import datetime as dt

SEED = 455
D = dt.date

COUNTY = "Wendmoor"
COUNTY_CODE = "071"
# the state's other counties (invented), with the state's three-digit county codes
OTHER_COUNTIES = [("Varnholt", "113"), ("Ardemere", "005"), ("Quillon", "087"), ("Kesterly", "049"),
                  ("Ostrey", "095"), ("Lindquay", "059")]
NEAR = ["Varnholt", "Ardemere", "Quillon"]          # where residents who die elsewhere in the state mostly die
OUT_STATES = ["CA", "NV", "AZ", "CO", "TX", "WA", "UT", "NM", "FL", "OR", "MT", "NE"]

ORG = "Wendmoor County Department of Public Health"
SECTION = "Epidemiology and Vital Statistics"
FOUNDATION = "Wendmoor Valley Recovery Foundation"
INITIATIVE = "Overdose Reduction Initiative"
CORONER = "Wendmoor County Coroner"
OME = "State Office of the Medical Examiner"
OVR = "State Office of Vital Records"
EMS_SYSTEM = "Wendmoor County EMS Data System"
PEOPLE = {"manager": "Tammie Mcneil", "grants": "Jesse Mcdonald", "pathologist": "Leah Jackson"}
TITLES = {"manager": "Epidemiology and Vital Statistics Manager", "grants": "Director of Grants",
          "pathologist": "Associate Medical Examiner"}

YEARS = list(range(2019, 2027))
BASE = [2021, 2022, 2023]
TARGET = 2026
REVIEW_YEAR = 2025
THRESHOLD = 20.0

# Each data year's file closes on the date the State Office of Vital Records sets (2020 and 2022 late: the
# pandemic backlog and the move to the new registration system).
CLOSE = {2019: D(2020, 5, 1), 2020: D(2021, 6, 15), 2021: D(2022, 5, 2), 2022: D(2023, 7, 17),
         2023: D(2024, 5, 1), 2024: D(2025, 4, 30), 2025: D(2026, 4, 30), 2026: D(2027, 4, 30)}
RELEASED = {2019: D(2020, 9, 14), 2020: D(2021, 10, 4), 2021: D(2022, 9, 12), 2022: D(2023, 11, 6),
            2023: D(2024, 9, 9), 2024: D(2025, 9, 8), 2025: D(2026, 9, 14), 2026: None}
EXTRACT = D(2027, 5, 11)
NEW_SYSTEM = D(2023, 1, 1)          # versions registered from this day carry the new system's coding
REVIEW_LIST = D(2026, 5, 6)         # the department sends the medical examiner the 2025 file's overdose deaths
REVIEW_DONE = D(2027, 2, 12)
AGREEMENT = D(2024, 1, 22)
MEETING = D(2027, 6, 17)
CERTIFIED = D(2027, 6, 2)

# Residents' drug overdose deaths by the medical examiner's drug class, as the file stands at the extract
# (2025: the deaths on the file at its close, every one reviewed). O: an opioid caused or contributed; S: a
# stimulant did and no opioid; R: other drugs only.
CLASS_N = {
    "O": {2019: 211, 2020: 246, 2021: 248, 2022: 260, 2023: 248, 2024: 233, 2025: 216, 2026: 189},
    "S": {2019: 41, 2020: 47, 2021: 56, 2022: 71, 2023: 89, 2024: 105, 2025: 128, 2026: 151},
    "R": {2019: 88, 2020: 86, 2021: 83, 2022: 80, 2023: 76, 2024: 71, 2025: 64, 2026: 60},
}
# The coroner's certificate categories: OL an opioid listed (T40.0-T40.4, T40.6), SO a stimulant (T40.5, T43.6)
# and no opioid, N neither (other drugs or no drug named). Rates in eighths: a certificate names no drug one time
# in eight whatever the class; the coroner lists every drug toxicology reports, so fentanyl present but not
# contributing is listed on half of the stimulant deaths.
RATE = {"O": {"OL": 7, "SO": 0, "N": 1}, "S": {"OL": 4, "SO": 3, "N": 1}, "R": {"OL": 0, "SO": 0, "N": 8}}

BANDS = [(15, 34), (35, 44), (45, 54), (55, 84)]
# share of each class's deaths by (sex, band); the 2025 cells are whole multiples of eight
PROFILE = {
    "O": {("M", 0): .27, ("M", 1): .20, ("M", 2): .13, ("M", 3): .10, ("F", 0): .11, ("F", 1): .08, ("F", 2): .06, ("F", 3): .05},
    "S": {("M", 0): .12, ("M", 1): .22, ("M", 2): .22, ("M", 3): .16, ("F", 0): .05, ("F", 1): .08, ("F", 2): .09, ("F", 3): .06},
    "R": {("M", 0): .08, ("M", 1): .10, ("M", 2): .14, ("M", 3): .18, ("F", 0): .07, ("F", 1): .10, ("F", 2): .13, ("F", 3): .20},
}
POLY = 0.62           # opioid deaths in which a stimulant also contributed
PLACE = {"county": 0.885, "state": 0.085, "out": 0.03}

# EMS: residents' non-fatal opioid overdose encounters per quarter, first quarter of 2021 to last of 2026
EMS_START = 2021
EMS_BASE = [334, 352, 361, 340, 329, 345, 350, 326, 318, 331, 338, 312, 301, 314, 322, 298,
            289, 300, 307, 284, 271, 283, 291, 268]
ALL_CAUSE = {2019: 5262, 2020: 5918, 2021: 6034, 2022: 5701, 2023: 5486, 2024: 5531, 2025: 5604, 2026: 5662}
NONRES_OCC = 0.075    # deaths of non-residents occurring in the county, against residents' deaths
POP = {2019: 641800, 2020: 645900, 2021: 648300, 2022: 652100, 2023: 655400, 2024: 659800, 2025: 663200,
       2026: 667100}
