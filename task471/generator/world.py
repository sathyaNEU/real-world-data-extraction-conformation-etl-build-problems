"""The world of task471 (architecture 2): the Board of Educator Standards and Licensure of an unnamed state, its
Elementary Literacy Instruction test (one administration a year, in June), and the sixteen educator preparation
programs whose 2025-26 completers' first-attempt pass rate decides the 2027 formal program reviews. The 2025 form
(25A) was scored and equated by the previous contractor; the 2026 form (26A) is scored by a new contractor and equated
to 25A by the Board's Office of Assessment Research through twenty shared multiple-choice items and one written
assignment carried over from 25A (WA2). The 2026 raters score every written assignment to a harsher standard than the
2025 raters did; the 2025 validity papers for WA2, scored by the 2026 raters, are the only place that shows it."""
import datetime as dt

SEED = 1491

BOARD = "Board of Educator Standards and Licensure"
OFFICE = "Office of Assessment Research"
TEST = "Elementary Literacy Instruction"
TEST_CODE = "ELI 104"
OLD_CO = "Pellmore Testing"               # scored and equated Form 25A (contract ended 31 December 2025)
NEW_CO = "Arcwright Assessment"           # scores Form 26A from 2026; the Board equates
PEOPLE = {"director": "Carolyn Jacobs",   # Director, Office of Assessment Research
          "scoring": "Wanda Reed",        # Arcwright's scoring director for the program
          "approval": "Renee Compton"}    # the Board's program approval coordinator

ADMIN = {2019: dt.date(2019, 6, 8), 2020: dt.date(2020, 6, 13), 2021: dt.date(2021, 6, 12),
         2022: dt.date(2022, 6, 11), 2023: dt.date(2023, 6, 10), 2024: dt.date(2024, 6, 8),
         2025: dt.date(2025, 6, 14), 2026: dt.date(2026, 6, 13)}
FORMS = {2019: "19A", 2020: "20A", 2021: "21A", 2022: "22A", 2023: "23A", 2024: "24A", 2025: "25A", 2026: "26A"}
PROGRAM_YEAR = (dt.date(2025, 7, 1), dt.date(2026, 6, 30))   # completers counted for the 2027 reviews
AS_OF = dt.date(2026, 8, 21)              # the office's working date; scores release 15 September 2026
RELEASE = dt.date(2026, 9, 15)
REVIEW_LINE = 0.70                        # a program under 70 per cent first-attempt pass goes to formal review

# the test: 60 multiple-choice items (one point) and three written assignments, each read twice on a 1 to 4 scoring guide,
# the two reads summed (2 to 8) and the sum counted twice; raw 0 to 108; reported 100 to 300, 240 passing
N_MC, N_WA, WA_WEIGHT = 60, 3, 2
MAX_RAW = N_MC + WA_WEIGHT * 8 * N_WA
N_SHARED = 20                             # multiple-choice items 26A carries from 25A
SHARED_WA = "WA2"                         # the written assignment 26A carries from 25A
PASS_SCALE = 240
PASS_RAW_25A = 56                         # Form 25A raw score at the passing standard (2025 technical report)

# the latent model: theta1 drives the multiple-choice items, theta2 the written assignments
RHO = 0.62
THRESHOLDS = (-0.95, 0.05, 1.05)          # scores 1 | 2 | 3 | 4 on (theta2 - assignment difficulty + rater severity)
RATER_SD = 0.50
LEADER_SD = 0.30                          # a scoring leader's resolution read
SEVERITY = {2025: 0.0, 2026: -0.34}       # the year's scoring standard on the latent scale
COHORT_SHIFT = {"pre": (0.0, 0.0), "new": (0.04, -0.30), "other26": (0.0, 0.0)}   # 2025-26 completers write less well

# the forms (difficulty shifts of the items each form does not share)
MC_B_MEAN, MC_B_SD = -0.55, 0.85
DMC_26A = 0.45                            # 26A's own multiple-choice items run harder than 25A's
DWA_26A = 0.10

N_VALIDITY = {"WA2": 120, "WA1": 160, "WA3": 160}   # validity papers seeded in 2026
VALIDITY_READS = (6, 10)                  # reads per paper (uniform)
BACKREAD_RATE = 0.05

# the sixteen programs: name, code, kind, 2025-26 completers, theta1 shift, theta2 shift, share testing before
# completing (a June 2025 first attempt), share not yet tested
PROGRAMS = [
    ('Ostrander State University', 'EPP-0112', 'university', 318, 0.2338, 0.1838, 0.10, 0.06),
    ('Whitcombe College', 'EPP-0147', 'university', 96, 0.6573, 0.6073, 0.12, 0.05),
    ('Delacourt University', 'EPP-0153', 'university', 224, -0.0852, -0.0852, 0.10, 0.07),
    ('Penhallow College', 'EPP-0168', 'university', 88, 0.1548, 0.1048, 0.08, 0.08),
    ('Marisford State University', 'EPP-0171', 'university', 276, -0.1523, -0.2023, 0.11, 0.06),
    ('Quillan College', 'EPP-0189', 'university', 64, 0.3117, 0.2617, 0.14, 0.05),
    ('Tarrance University', 'EPP-0204', 'university', 182, -0.4012, -0.3012, 0.09, 0.09),
    ('Hollis Creek College', 'EPP-0216', 'university', 71, -0.1320, -0.1820, 0.10, 0.07),
    ('Eastridge State University', 'EPP-0233', 'university', 249, -0.2821, -0.3321, 0.10, 0.06),
    ('Saint Aldric University', 'EPP-0241', 'university', 118, -0.0337, 0.0663, 0.13, 0.05),
    ('Corriden University', 'EPP-0258', 'university', 132, -0.0387, 0.0113, 0.10, 0.08),
    ('Linden Valley College', 'EPP-0262', 'university', 57, -0.6833, -0.7333, 0.07, 0.09),
    ('Statewide Teacher Residency', 'EPP-0307', 'alternative', 205, -0.2753, -0.2753, 0.03, 0.10),
    ('Riverbend Teaching Fellows', 'EPP-0315', 'alternative', 143, -0.1358, -0.2858, 0.04, 0.09),
    ('Harrowgate Teacher Academy', 'EPP-0322', 'alternative', 92, -0.5928, -0.4428, 0.03, 0.11),
    ('Brightwater College', 'EPP-0339', 'university', 77, 0.0690, 0.1690, 0.12, 0.06),
]
CANDIDATES = [p[0] for p in PROGRAMS]

# first-attempt candidates who are not 2025-26 completers of the sixteen programs: earlier completers testing late,
# out-of-state program completers, permit holders on the experience route
OTHERS_2025 = 1180
OTHERS_2026 = 1190
EARLIER_COMPLETERS_2025 = 1650            # 2024-25 completers testing first in June 2025
REPEAT_RATE = 0.55                        # a failed candidate tests again the next June

FILES = {}                                # filled by pack.py
