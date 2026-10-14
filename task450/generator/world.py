"""The fiction's fixed facts for task450: Coraza Independent School District (Texas), its elementary campuses and
learning communities, the two grade-5 mathematics forms, the reporting scale set in 2025, the calendar of the
2025-26 school year and the people named in the district's files."""
import datetime as dt

SEED = 450
DISTRICT = "Coraza Independent School District"
SHORT = "Coraza ISD"
OFFICE = "Office of Assessment and Accountability"
CITY = "Coraza, Texas"
TEST = "District Mathematics Assessment"

PEOPLE = {
    "director": ("Susan Bird", "Executive Director, Assessment and Accountability"),
    "superintendent": ("Christopher Murphy", "Superintendent of Schools"),
    "board": ("Katherine Padilla", "President, Board of Trustees"),
    "math": ("Debra Ward", "Director of Elementary Mathematics"),
}

# five learning communities as the board drew them for 2026-27
COMMUNITIES = ["North", "Central", "East", "South", "West"]

# elementary campuses open in 2025-26, in the legacy system's order (the order they opened); the last field is
# the learning community for 2026-27
CAMPUSES = [
    ("Alameda Park Elementary", "Central"), ("Barrow Street Elementary", "Central"),
    ("Cottonwood Draw Elementary", "West"), ("Delgadillo Elementary", "South"),
    ("Cenizo Flat Elementary", "South"), ("Fairlane Elementary", "North"),
    ("Tasajillo Draw Elementary", "East"), ("Hargis Elementary", "North"),
    ("Ironwood Point Elementary", "South"), ("Jessamine Elementary", "East"),
    ("Agarita Bend Elementary", "West"), ("Sotol Mesa Elementary", "West"),
    ("Mabry Elementary", "Central"), ("Northgate Elementary", "North"),
    ("Old Mill Road Elementary", "East"), ("Retama Hollow Elementary", "Central"),
    ("Javelina Run Elementary", "South"), ("Rosedale Terrace Elementary", "Central"),
    ("Granjeno Crossing Elementary", "East"), ("Tobar Elementary", "South"),
    ("Upland Prairie Elementary", "North"), ("Vance Avenue Elementary", "Central"),
    ("Windmill Hill Elementary", "West"), ("Ximenez Elementary", "South"),
    ("Guayacan Hill Elementary", "North"), ("Lechuguilla Gap Elementary", "South"),
    ("Ashe Juniper Elementary", "West"), ("Kidneywood Knoll Elementary", "North"),
    ("Wolfberry Trail Elementary", "South"), ("Sandbur Flat Elementary", "West"),
    ("Elmhurst Avenue Elementary", "Central"), ("Horsemint Meadow Elementary", "Central"),
    ("Gallardo Elementary", "East"), ("Huisachito Elementary", "East"),
    ("Indigo Prairie Elementary", "West"), ("Dewberry Terrace Elementary", "South"),
    ("Coyote Tank Elementary", "North"), ("Nopalito Vista Elementary", "West"),
    ("Lantana Loop Elementary", "West"), ("Larkin Street Elementary", "North"),
    ("Orozco Elementary", "East"), ("Pinto Mesa Elementary", "Central"),
    ("Mustang Grape Elementary", "North"), ("Riojas Elementary", "South"),
    ("Vereda Elementary", "East"), ("Tepeguaje Draw Elementary", "West"),
    ("Ursuline Avenue Elementary", "Central"), ("Bramble Ford Elementary", "East"),
    ("Hackberry Slough Elementary", "West"), ("Yucca Bloom Elementary", "North"),
    ("Arriaga Elementary", "East"), ("Chinaberry Lane Elementary", "North"),
    ("Caliche Ridge Elementary", "West"), ("Switchgrass Bend Elementary", "South"),
    ("Encino Grove Elementary", "Central"), ("Farias Elementary", "East"),
]

# Delgadillo Elementary closed in June 2026; its attendance zone moved to Tobar Elementary for 2026-27
CLOSED = ("Delgadillo Elementary", "Tobar Elementary")

# the 2025-26 school year
YEAR_START = dt.date(2025, 8, 13)
SNAPSHOT = dt.date(2025, 10, 31)          # the state's fall enrollment snapshot
MIGRATION = dt.date(2026, 1, 5)           # the new student information system went live after the winter break
WINDOW = (dt.date(2026, 4, 20), dt.date(2026, 5, 1))
YEAR_END = dt.date(2026, 5, 28)
WINDOW_2025 = (dt.date(2025, 4, 21), dt.date(2025, 5, 2))
PULL = dt.date(2026, 10, 9)               # the office's extract for the improvement plan
KEY_MEMO = dt.date(2026, 5, 19)

# the reporting scale, set on the 2025 grade-5 form in June 2025
SCALE_MID = 26.5                          # the proficiency standard, as a raw score on the 2025 form
SCALE_SLOPE = 6
STANDARD = 300
LINE = 0.40                               # the improvement plan's designation line
N_MIN = 10                                # campuses with fewer full-academic-year tested students are not rated

# the forms: 50 items each, 25 carried from the 2025 form to the 2026 form in the same positions
N_ITEMS = 50
ANCHOR_POS = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49]
# the 2026 cohort is the first the new curriculum has taught since grade 3, and it teaches simplifying numerical
# expressions a year earlier: the three shared items nearest the middle of the shared set's difficulty, written to
# that standard, are far easier for the 2026 students than their ability elsewhere implies (logits below 2025)
DRIFT_N = 3
DRIFT_LOGITS = 1.5
DRIFT_TAG = ("Algebraic reasoning", "5.4F")
FORM25 = "G5M-25"
FORM26 = "G5M-26"
