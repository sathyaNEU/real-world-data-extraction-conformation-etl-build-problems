"""The fixed world of task464 (architecture 2): an unnamed state's Department of Education, its districts, the retiring
and the new state reading tests, the spring 2026 bridge study and the 2027 Adolescent Literacy Partnership grants.
Names, scales, cut scores, dates and file names; every random quantity lives in sim.py."""
import math

import numpy as np

STATE_AGENCY = "State Department of Education"
OFFICE = "Office of Assessment"
LITERACY_OFFICE = "Office of Literacy"
BOARD = "State Board of Education"
PROGRAMME = "Adolescent Literacy Partnership"
GRANTS = 6
GRANT_YEAR = 2027
COUNT_DAY = "2026-10-01"
AS_OF = "2026-11-20"

OLD_TEST, OLD_ABBR = "Grade-Level Reading Assessment", "GLRA"
NEW_TEST, NEW_ABBR = "Statewide Literacy Measure", "SLM"
OLD_VENDOR = "Calderwood Testing Services"
NEW_VENDOR = "Northfield Assessment Group"
OLD_YEAR, NEW_YEAR = 2025, 2026

# Each test's grade 8 scale: score = mean + slope * ability + error; the two have the same reliability.
OLD = dict(mean=300.0, slope=50.0, err=20.0, lo=150, hi=450)
NEW = dict(mean=2500.0, slope=80.0, err=32.0, lo=2100, hi=2900)
GRADE_SHIFT = {6: -0.62, 7: -0.31, 8: 0.0}          # ability below grade 8's, on each grade's own form
GLRA_ITEMS = 30                                     # each grade's retiring form: 30 items scored right or wrong
OLD_CUTS = {6: (200, 262, 311), 7: (225, 278, 327), 8: (231, 293, 342)}   # Basic, Proficient, Advanced begin
NEW_CUTS = {6: (2365, 2458, 2529), 7: (2390, 2483, 2554), 8: (2415, 2508, 2579)}   # Level 2, 3, 4 begin (adopted)
# The vendor's June student file reports levels on the panel's recommended cut scores: the Board adopted grade 8's as
# recommended on 11 June 2026 and set grades 3 to 7 on 13 August 2026.
NEW_CUTS_JUNE = {6: (2361, 2455, 2526), 7: (2383, 2479, 2551), 8: (2415, 2508, 2579)}
GRADE8_RESOLUTION = ("2026-14", "2026-06-11")
LOWER_RESOLUTION = ("2026-22", "2026-08-13")
OLD_LEVELS = ("Below Basic", "Basic", "Proficient", "Advanced")
NEW_LEVELS = ("Level 1", "Level 2", "Level 3", "Level 4")

# Current districts: code, name, county, grade 8 cohort of 2025 (now grade 10), grade 8 cohort of 2026 (now grade 9),
# each cohort's mean reading ability against its own statewide cohort (in standard deviations).
DISTRICTS = [
    ("1010", "Kessick Public Schools", "Kessick", 2630, 2560, -0.16, -0.18),
    ("1020", "Varlow City Schools", "Varlow", 2250, 2290, -0.10, -0.12),
    ("1110", "Brenmoor County Schools", "Brenmoor", 1460, 1480, 0.00, 0.02),
    ("1120", "Calderidge Unified School District", "Calder", 1360, 1320, -0.04, -0.06),
    ("1210", "Dunstree Area Schools", "Dunstree", 960, 920, -0.05, -0.05),
    ("1220", "Elmorrow Public Schools", "Elmorrow", 2090, 1670, 0.30, 0.45),
    ("1230", "Garnet Hills School District", "Garnet", 1040, 1050, -0.10, -0.10),
    ("1240", "Harlenbrook County Schools", "Harlen", 650, 900, 0.00, -0.40),
    ("1310", "Ivelstone Public Schools", "Ivel", 940, 960, 0.10, 0.08),
    ("1320", "Jasperton Unified School District", "Jasper", 880, 900, 0.04, 0.06),
    ("1330", "Kilmarden County Schools", "Kilmarden", 850, 830, 0.10, 0.08),
    ("1340", "Lorrance Area Schools", "Lorrance", 800, 820, 0.05, 0.07),
    ("1410", "Marrowby School District", "Marrowby", 740, 760, -0.02, 0.00),
    ("1420", "Netherfold Public Schools", "Netherfold", 700, 690, 0.10, 0.12),
    ("1430", "Orlenwood Unified School District", "Orlen", 660, 670, 0.04, 0.01),
    ("1440", "Pemberwick County Schools", "Pemberwick", 610, 620, -0.05, -0.02),
    ("1510", "Quarrystone Area Schools", "Quarry", 560, 570, 0.12, 0.10),
    ("1520", "Saltmarrow Public Schools", "Saltmarrow", 520, 500, -0.02, 0.00),
    ("1530", "Thistlewade School District", "Thistle", 480, 490, 0.07, 0.05),
    ("1540", "Umberfield County Schools", "Umber", 440, 450, 0.00, -0.03),
    ("1610", "Vexley Unified School District", "Vexley", 400, 410, 0.09, 0.11),
    ("1620", "Wrenhollow Public Schools", "Wrenhollow", 370, 360, -0.06, -0.04),
    ("1630", "Yarrowdale Area Schools", "Yarrow", 330, 340, 0.03, 0.06),
    ("1640", "Caddock County Schools", "Caddock", 300, 290, 0.05, 0.02),
    ("1650", "Mistlefield Unified School District", "Mistle", 260, 270, 0.10, 0.08),
    ("1660", "Rookmoor Area Schools", "Rookmoor", 230, 220, -0.01, 0.03),
    ("1700", "Ashgrove-Fenley Consolidated Schools", "Ashgrove", 420, 430, 0.04, 0.02),
]
# The 2025 grade 8 cohort read less well than the 2026 one statewide (in standard deviations of reading ability).
COHORT_SHIFT = {2025: -0.20, 2026: 0.0}
# The districts that filed a notice of intent for the 2027 grants by 15 October 2026.
APPLICANTS = ["1010", "1020", "1110", "1120", "1210", "1220", "1230", "1240", "1310", "1320", "1410", "1440", "1520",
              "1700"]
NOTICE_DEADLINE = "2026-10-15"

# Nonpublic schools whose students sit the state tests by agreement: code (the district prefix of the district the
# school stands in and a number from 900), name, the district it stands in, students per grade, reading ability
# against the state's public cohorts. Their results come in the vendors' files under that district's code.
NONPUBLIC = [
    ("1010910", "Kessick Catholic Academy", "1010", 46, 0.32), ("1010925", "Kessick Hebrew Day School", "1010", 22, 0.45),
    ("1010931", "Kessick Christian School", "1010", 31, 0.18), ("1020912", "Varlow Catholic School", "1020", 38, 0.28),
    ("1020940", "Varlow Friends School", "1020", 26, 0.52), ("1110915", "Brenmoor Lutheran School", "1110", 34, 0.05),
    ("1120908", "Calderidge Parish School", "1120", 33, 0.30), ("1210921", "Dunstree Christian Academy", "1210", 24, 0.40),
    ("1220905", "Elmorrow Country Day School", "1220", 41, 0.61), ("1220933", "Elmorrow Parish School", "1220", 29, 0.34),
    ("1230917", "Garnet Hills Mennonite School", "1230", 18, 0.20), ("1240911", "Harlenbrook Catholic School", "1240",
                                                                             25, 0.15),
    ("1310926", "Ivelstone Adventist School", "1310", 17, 0.22), ("1320903", "Jasperton Parish School", "1320", 30, 0.70),
    ("1410918", "Marrowby Baptist Academy", "1410", 21, 0.10), ("1440909", "Pemberwick Montessori School", "1440",
                                                                  16, 0.40),
    ("1520914", "Saltmarrow Catholic School", "1520", 23, 0.25), ("1701907", "Ashgrove Christian School", "1701", 19,
                                                                   0.21),
    ("1330920", "Kilmarden Academy", "1330", 24, 0.36), ("1630912", "Yarrowdale Christian School", "1630", 14, 0.19),
]
# Registered nonpublic schools whose students do not sit the state tests: code, name, district it stands in, grades,
# affiliation.
NONPUBLIC_OTHER = [
    ("1010947", "Lindenhurst Preparatory School", "1010", "6-12", "Independent"),
    ("1020951", "Varlow Islamic Academy", "1020", "K-8", "Muslim"),
    ("1110938", "Pinecroft Waldorf School", "1110", "PK-8", "Independent"),
    ("1210944", "Covenant Hall School", "1210", "K-12", "Christian"),
    ("1310939", "Emberline Day School", "1310", "K-8", "Independent"),
    ("1410952", "Mount Hollis Academy", "1410", "6-12", "Christian"),
    ("1530918", "Thistlewade Amish School", "1530", "1-8", "Amish"),
    ("1540927", "Umberfield Christian Academy", "1540", "K-12", "Christian"),
    ("1620913", "Wrenhollow Montessori School", "1620", "PK-6", "Independent"),
]
NONPUBLIC_ENROL = {2025: 0.22, 2026: 0.31}   # grade 8 nonpublic test takers of each spring in a public high school now

# The consolidated district was two districts until 30 June 2026; its students tested under their old codes.
MERGER = {"1700": (("1701", "Ashgrove Public Schools", 0.55), ("1702", "Fenley School District", 0.45))}
MERGER_DATE = "2026-07-01"

FILES = {
    "glra": "glra_2025_student_results.csv",
    "slm": "slm_2026_student_results.csv",
    "bridge": "glra_slm_bridge_study_2026.csv",
    "crosswalk": "calderwood_examinee_id_crosswalk_2025.csv",
    "enrollment": "enrollment_october_2026_grades_9_12.csv",
    "directory": "district_directory_2026.xlsx",
    "slm_report": "slm_2026_grade8_technical_summary.pdf",
    "glra_guide": "glra_2025_interpretive_guide.pdf",
    "bridge_memo": "glra_slm_bridge_study_memo.pdf",
    "rules": "alp_2027_grant_rules.pdf",
    "resolution": "sbe_resolution_2026_22_slm_cut_scores.pdf",
    "nonpublic": "nonpublic_schools_registry_2026.csv",
    "finance": "district_expenditure_per_pupil_2025.csv",
    "gradrate": "four_year_graduation_rates_2025.csv",
    "dict": "data_dictionary.csv",
    "register": "alp_2027_folder_index.csv",
}
DISTRACTORS = ["finance", "gradrate"]
GOLDEN = {"workbook": "alp_grants_2027.xlsx", "table": "alp_conformed_grade8_reading_2026.csv"}

PEOPLE = {"director": "Jeffrey Warren", "psychometrician": "William Holloway"}
TITLES = {"director": "Director, Adolescent Literacy Partnership", "psychometrician": "Psychometrician, Office of Assessment"}


def glra_table(grade):
    """The retiring test's raw-score-to-scale-score table for one grade's fixed form: only these scale scores occur. The
    new test is adaptive and reports any integer on its scale."""
    out = []
    for r in range(GLRA_ITEMS + 1):
        if r in (0, GLRA_ITEMS):
            s = OLD["lo"] if r == 0 else OLD["hi"]
        else:
            s = OLD["mean"] + OLD["slope"] * (math.log(r / (GLRA_ITEMS - r)) + GRADE_SHIFT[grade])
        out.append(int(min(max(round(s), OLD["lo"]), OLD["hi"])))
    return out


def glra_attainable(grade):
    return np.array(sorted(set(glra_table(grade))))


def glra_score(value, grade):
    """The reported scale score of a continuous score on one grade's form: the table's nearest scale score."""
    a = glra_attainable(grade)
    v = np.asarray(value, float)
    i = np.clip(np.searchsorted(a, v), 1, len(a) - 1)
    lo, hi = a[i - 1], a[i]
    return np.where(v - lo <= hi - v, lo, hi).astype(int)


def short_name(code):
    """A district's name without its organisational suffix (Kessick, Garnet Hills, Ashgrove-Fenley)."""
    name = dict((c, n) for c, n, *_ in DISTRICTS)[code]
    for suffix in (" Public Schools", " City Schools", " County Schools", " Unified School District", " School District",
                   " Area Schools", " Consolidated Schools"):
        if name.endswith(suffix):
            return name[:-len(suffix)]
    return name


def district_names():
    out = {c: n for c, n, *_ in DISTRICTS}
    for new, parts in MERGER.items():
        for code, name, _ in parts:
            out[code] = name
    return out
