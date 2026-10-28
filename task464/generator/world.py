"""task464 architecture 8: the world.

An adult education service reviews why its learners withdrew in 2025/26. Each withdrawal carries the learner's
own free-text exit comment and the category a coder placed it in against the service's coding manual. Every term
the service moderates a fixed number of comments per coded category: a second, senior coder re-reads them and
records the category the comment belongs in.

Nothing in this module states a corrected share, a hit rate or a ranking. Those are computed in sim.py and
answers.py and asserted in checks.py.
"""

SERVICE = "Thornmere Adult Education Service"
AUTHORITY = "Thornmere Combined Authority"
MANUAL = "Exit Comment Coding Manual"
CURRENCY = "GBP"
ASOF = "2026-11-18"          # the review is taken after this date
YEAR = "2025/26"
DECISION_YEAR = "2027"

PEOPLE = {
    "retention_lead": "Roger Nicholls",     # puts the target to the head of service
    "moderator": "Carly Leonard",           # senior coder who runs the termly moderation
}

# The six categories of the coding manual, in manual order.
CATEGORIES = [
    ("CR", "Caring responsibilities"),
    ("WH", "Work hours clash"),
    ("TR", "Travel or transport"),
    ("CD", "Course too difficult"),
    ("HL", "Health"),
    ("OT", "Other or not stated"),
]
CODES = [c for c, _ in CATEGORIES]
LABEL = dict(CATEGORIES)

# The composition of the reasons learners actually withdrew for. Latent: never shipped, never printed.
TRUE_SHARE = {"CR": 0.250, "WH": 0.205, "TR": 0.140, "CD": 0.155, "HL": 0.130, "OT": 0.120}

# How the coders behave. CODED_GIVEN_TRUE[coded][true] = P(a case of `true` is coded `coded`).
# A caring responsibility reaches the record as a sentence about hours ("could not get cover for mum on
# Tuesdays"), so CR is recognised in 68 of every 100 cases that belong to it and WH takes most of the spill.
CODED_GIVEN_TRUE = {
    "CR": {"CR": 0.68, "WH": 0.03, "TR": 0.05, "CD": 0.02, "HL": 0.04, "OT": 0.05},
    "WH": {"CR": 0.14, "WH": 0.90, "TR": 0.08, "CD": 0.03, "HL": 0.02, "OT": 0.08},
    "TR": {"CR": 0.06, "WH": 0.02, "TR": 0.74, "CD": 0.01, "HL": 0.02, "OT": 0.04},
    "CD": {"CR": 0.02, "WH": 0.01, "TR": 0.02, "CD": 0.86, "HL": 0.01, "OT": 0.07},
    "HL": {"CR": 0.02, "WH": 0.01, "TR": 0.02, "CD": 0.02, "HL": 0.84, "OT": 0.04},
    "OT": {"CR": 0.08, "WH": 0.03, "TR": 0.09, "CD": 0.06, "HL": 0.07, "OT": 0.72},
}

ENROLMENTS = 86000           # 2025/26 enrolments across the service
WITHDRAWALS = 17200          # of which withdrew before completing
MODERATED_PER_CODE = 450     # the termly moderation sample is a fixed number PER CODED CATEGORY

# Four terms. The student record system changed between T2 and T3, which is why the exports differ.
TERMS = [
    {"code": "T1", "label": "autumn 2025", "start": "2025-09-08", "end": "2025-10-24", "share": 0.29,
     "export": "A"},
    {"code": "T2", "label": "winter 2025", "start": "2025-11-03", "end": "2025-12-19", "share": 0.24,
     "export": "A"},
    {"code": "T3", "label": "spring 2026", "start": "2026-01-12", "end": "2026-03-27", "share": 0.27,
     "export": "B"},
    {"code": "T4", "label": "summer 2026", "start": "2026-04-20", "end": "2026-07-17", "share": 0.20,
     "export": "B"},
]

# Two sites were renamed by a merger between T2 and T3, so the earlier export carries the former names.
SITES = [
    {"code": "NMK", "name": "Northmarket Centre", "former": "Northmarket Adult College"},
    {"code": "HWD", "name": "Hollowdean Centre", "former": "Hollowdean Learning Shop"},
    {"code": "CSG", "name": "Cross Gate Centre", "former": None},
    {"code": "WBR", "name": "Westbury Centre", "former": None},
    {"code": "LTH", "name": "Lathe Street Centre", "former": None},
]

CURRICULUM = ["English and maths", "Digital skills", "ESOL", "Health and social care",
              "Business administration", "Construction skills"]

# Subcontracted delivery. These enrolments sit in the same extract because they run on the service's own
# student record, but they are not the service's own provision and the review's scope is the five centres.
# The code is absent from site_directory.csv, which is the only place the five centres are listed.
SUBCONTRACT_SITE = {"code": "MDV", "name": "Meadowvale (subcontracted)"}
SUBCONTRACT_ENROLMENTS = 4130

# Courses that run across two terms. The student record opens an enrolment row for the learner in EACH term
# the course spans, and both rows carry the WHOLE course's planned hours, because the hours belong to the
# course and not to the term. Summing the column over rows therefore counts a two-term course's hours twice.
# Nothing flags it: (learner, course, term) is unique, and a learner holding two rows for one course is
# correct data. Only course_catalogue.csv, which carries each course's hours once, resolves it.
TWO_TERM_SHARE = 0.34          # share of courses that span two terms
# Learners who move centre mid-course keep the same course and appear at both centres, the sending centre's
# row left at continuing and the receiving centre's closed at completed.
TRANSFER_SHARE = 0.047

SEED = 46486


def term(code):
    for t in TERMS:
        if t["code"] == code:
            return t
    raise KeyError(code)


def withdrawals_for(code):
    first = [int(round(WITHDRAWALS * t["share"])) for t in TERMS]
    diff = WITHDRAWALS - sum(first)
    first[0] += diff                      # the split sums exactly
    return dict(zip([t["code"] for t in TERMS], first))[code]
