"""task464 architecture 8: the world.

An adult education service reviews why its learners withdrew in 2025/26. Each withdrawal carries the learner's
own free-text exit comment and the category a coder placed it in against the service's coding manual. Each year
the service moderates a sample drawn by coded category (every OT, a fixed number of each other code): a second,
senior coder re-reads them and records the category the comment belongs in.

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

ENROLMENTS = 86413           # 2025/26 enrolment rows across the service's five centres
WITHDRAWALS = 17231          # of which withdrew before completing
# The moderation sample is drawn by CODED category. Every withdrawal coded OT is moderated, because OT is the
# code the service learns least from; for each of the other five codes a fixed number is drawn across the year.
MODERATED_ALL = ("OT",)
MODERATED_PER_CODE = 400

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
    {"code": "HWD", "name": "Hollowdean Learning Hub", "former": "Hollowdean Learning Shop"},
    {"code": "CSG", "name": "Cassgrove", "former": None},
    {"code": "WBR", "name": "Wyebrook Adult Learning Centre", "former": None},
    {"code": "LTH", "name": "The Lathe Street Building", "former": None},
]

# planned guided hours a course may carry
GUIDED_HOURS = [30, 36, 45, 54, 60, 72, 90, 120]

CURRICULUM = ["English and maths", "Digital skills", "ESOL", "Health and social care",
              "Business administration", "Construction skills"]

# Subcontracted delivery. These enrolments sit in the same extract because they run on the service's own
# student record, but they are not the service's own provision and the review's scope is the five centres.
# The code is absent from site_directory.csv, which is the only place the five centres are listed.
SUBCONTRACT_SITE = {"code": "MDV", "name": "Meadowvale (subcontracted)"}
SUBCONTRACT_ENROLMENTS = 4127

# Courses that run across two terms. The student record opens an enrolment row for the learner in EACH term
# the course spans, and both rows carry the WHOLE course's planned hours, because the hours belong to the
# course and not to the term. Summing the column over rows therefore counts a two-term course's hours twice.
# Nothing flags it: (learner, course, term) is unique, and a learner holding two rows for one course is
# correct data. Only course_catalogue.csv, which carries each course's hours once, resolves it.
TWO_TERM_SHARE = 0.34          # share of courses that span two terms
# Learners who move centre mid-course keep the same course and appear at both centres, the sending centre's
# row left at continuing and the receiving centre's closed at completed.
TRANSFER_SHARE = 0.047
# The student record system changed between T2 and T3. A course running across the change could not be carried
# into the new system as an open occurrence, so it was closed in the old one after its winter term and created
# again in the new one for its spring term, under a new course reference with the same centre, curriculum area
# and planned hours. The catalogue keeps both references, the old one still showing the two terms it was
# planned for. Nothing on either row says the two are one course: the learners on the new reference are the
# learners of the old one, and that identity is the only thing that links them.
CUTOVER_AFTER = "T2"
# Winter withdrawals keyed in the last fortnight of term went into the new system as well as the old one.
LATE_KEYED_SHARE = 0.55

SEED = 46835
PACK_SEED = SEED + 17     # the enrolment extract and the catalogue, drawn apart from the withdrawals


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
