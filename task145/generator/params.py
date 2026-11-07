"""task145 architecture 2: Cedar Prairie Charter Schools. Every constant the world, the pack and the goldens share."""
import datetime as dt

ORG = "Cedar Prairie Charter Schools"
CITY = "Cottonwood Plains"
SEED = 32
AS_OF = dt.date(2026, 12, 21)          # the extract date: the Monday after the fall semester closes
SPRING_START = dt.date(2027, 1, 5)     # first instructional day of the spring 2027 semester
WINDOW_END = dt.date(2027, 6, 30)      # the Bridge policy's window closes

SCHOOLS = ["CPP", "RBA", "MVH", "SHC"]
SCHOOL_NAME = {"CPP": "Cottonwood Plains Preparatory", "RBA": "Riverbend Academy",
               "MVH": "Mesa Vista High School", "SHC": "Sandhill Collegiate"}
SCHOOL_NO = {"CPP": "0412", "RBA": "0418", "MVH": "0427", "SHC": "0433"}
SHARE = {"CPP": 0.30, "RBA": 0.27, "MVH": 0.23, "SHC": 0.20}
GRADES = [9, 10, 11, 12]

# school years: (label, first day, last day of fall, first day of spring, last day)
YEARS = [
    ("2023-24", dt.date(2023, 8, 14), dt.date(2023, 12, 20), dt.date(2024, 1, 8), dt.date(2024, 5, 31)),
    ("2024-25", dt.date(2024, 8, 12), dt.date(2024, 12, 19), dt.date(2025, 1, 6), dt.date(2025, 5, 30)),
    ("2025-26", dt.date(2025, 8, 13), dt.date(2025, 12, 19), dt.date(2026, 1, 5), dt.date(2026, 5, 29)),
    ("2026-27", dt.date(2026, 8, 12), dt.date(2026, 12, 18), dt.date(2027, 1, 5), dt.date(2027, 5, 28)),
]
HIST = ["2023-24", "2024-25", "2025-26"]
CUR = "2026-27"

# Bridge contract tiers (seats) and the price a semester (USD)
TIERS = [("Tier 1", 125, 489000), ("Tier 2", 195, 741000), ("Tier 3", 265, 979000)]

# the bell schedule: instructional minutes of the halves and of Mesa Vista's periods
AM_MIN, PM_MIN = 200, 175                  # the AM session is longer than the PM session at every school
MVH_STD = [("1", 52), ("2", 52), ("ADV", 24), ("3", 52), ("4", 52), ("5", 52), ("6", 52), ("7", 39)]
MVH_WED = [("A", 88), ("B", 88), ("C", 88), ("D", 88)]

# truth: the clean world's rates (never shipped)
RUN_MIN = 5            # a run: this many consecutive instructional days or more, all missed
TEXT_FACTOR = 0.72     # the family texts from 12 August 2026 scale every scattered absence episode by this
RUN_P = 0.15           # an ordinary run's length: five days plus a geometric tail
LAM0 = 0.07            # an ordinary run's yearly rate at the mean of the engagement factor
DISP_SHARE = 0.105     # autumn 2026: the share of students whose families moved between addresses
DISP_SCHOOL = {"CPP": 0.7, "RBA": 1.6, "MVH": 0.6, "SHC": 1.2}
DISP_LAM = 0.0         # a displaced student has one long run, and a second at this chance
ILL_K = 2.0            # the illness factor: a gamma with this shape and mean one
PSC_CAP = 0.40         # the most a day a scattered absence episode can start
LONG_MIN = 10          # a long run: this many days or more
LONG_P = 0.22          # its geometric tail
LONG_UX = 0.90         # the share of long runs coded unexcused
DISP_Z = 0.2           # displacement leans on the engagement factor this much
B_RUN = 3.0            # the leaving logit step for a first run
B_RUN2 = 1.3           # and for each further run, to three
B0 = -4.8              # the leaving logit intercept
P_SC0 = 0.06           # a scattered absence episode's start a day at the mean of the engagement factor
