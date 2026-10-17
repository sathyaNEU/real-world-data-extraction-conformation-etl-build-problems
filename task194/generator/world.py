"""The fiction: Mid-Rivers Health Network, its four hospitals, its inpatient units, the hospital-acquired
complication indicator and the improvement embed programme. Every constant the pack states lives here once.

Quarters are the network's fiscal quarters (1 July to 30 June). The extract covers the ten closed quarters
on indicator specification 4.0 (1 July 2024 onwards); the placement being decided is the quarter beginning
1 April 2027.
"""
import datetime as dt

NETWORK = "Mid-Rivers Health Network"
PULL_DATE = dt.date(2027, 3, 5)          # the extract's export date
AS_OF = dt.date(2027, 3, 18)             # the date the placement is decided
EMBED_QUARTER = "2026-27 Q4"
EMBED_FROM = dt.date(2027, 4, 1)
EMBED_TO = dt.date(2027, 6, 30)
SPEC_VERSION = "4.0"
SPEC_EFFECTIVE = dt.date(2024, 7, 1)
REF_RATE = 96.5                          # complications per 1,000 episodes, published with specification 4.0
CODESET_CHANGE = dt.date(2026, 7, 1)     # national complication list revision, list 2022 -> list 2026

PEOPLE = {
    "director": ("Katherine Klein", "Director, Clinical Improvement"),
    "governance": ("Nicholas Fields", "Manager, Clinical Information and Coding"),
}

HOSPITALS = [
    ("H1", "Alderbrook Hospital", "Principal referral"),
    ("H2", "Stonecreek Hospital", "Public acute group A"),
    ("H3", "Marrowfield Hospital", "Public acute group A"),
    ("H4", "Carrowdean District Hospital", "Public acute group B"),
]

# Quarters: (label, fiscal year, start date, end date, three month starts)
def _quarters():
    out = []
    starts = [(2024, 7), (2024, 10), (2025, 1), (2025, 4), (2025, 7), (2025, 10),
              (2026, 1), (2026, 4), (2026, 7), (2026, 10)]
    for y, m in starts:
        fy = y if m >= 7 else y - 1
        qn = {7: 1, 10: 2, 1: 3, 4: 4}[m]
        label = "%d-%02d Q%d" % (fy, (fy + 1) % 100, qn)
        start = dt.date(y, m, 1)
        end_m, end_y = (m + 2, y) if m + 2 <= 12 else (m + 2 - 12, y + 1)
        last = (dt.date(end_y + (1 if end_m == 12 else 0), 1 if end_m == 12 else end_m + 1, 1)
                - dt.timedelta(days=1))
        months = []
        for k in range(3):
            mm, yy = (m + k, y) if m + k <= 12 else (m + k - 12, y + 1)
            months.append(dt.date(yy, mm, 1))
        out.append((label, "%d-%02d" % (fy, (fy + 1) % 100), start, last, months))
    return out


QUARTERS = _quarters()
QLABELS = [q[0] for q in QUARTERS]

# AR-DRG style codes: (code, description, risk band)
DRGS = [
    ("I03A", "Hip replacement with catastrophic complexity", "ORTH-MAJ"),
    ("I03B", "Hip replacement without catastrophic complexity", "ORTH-MAJ"),
    ("I04A", "Knee replacement with catastrophic complexity", "ORTH-MAJ"),
    ("I04B", "Knee replacement without catastrophic complexity", "ORTH-MAJ"),
    ("I08A", "Other hip and femur procedures, major complexity", "ORTH-MAJ"),
    ("I75A", "Injury to shoulder, arm, elbow, knee, leg, major complexity", "ORTH-MIN"),
    ("I75B", "Injury to shoulder, arm, elbow, knee, leg, minor complexity", "ORTH-MIN"),
    ("G02A", "Major small and large bowel procedures, catastrophic complexity", "SURG-MAJ"),
    ("G02B", "Major small and large bowel procedures, severe complexity", "SURG-MAJ"),
    ("F05A", "Coronary bypass with invasive investigation", "SURG-MAJ"),
    ("G07A", "Appendicectomy with catastrophic complexity", "SURG-MIN"),
    ("G07B", "Appendicectomy without catastrophic complexity", "SURG-MIN"),
    ("H08A", "Laparoscopic cholecystectomy, major complexity", "SURG-MIN"),
    ("H08B", "Laparoscopic cholecystectomy, minor complexity", "SURG-MIN"),
    ("F62A", "Heart failure and shock with catastrophic complexity", "MED-COMPLEX"),
    ("F62B", "Heart failure and shock with severe complexity", "MED-COMPLEX"),
    ("E62A", "Respiratory infections with catastrophic complexity", "MED-COMPLEX"),
    ("E62B", "Respiratory infections with severe complexity", "MED-COMPLEX"),
    ("E65A", "Chronic obstructive airways disease, major complexity", "MED-COMPLEX"),
    ("B70A", "Stroke with catastrophic complexity", "MED-COMPLEX"),
    ("B70B", "Stroke with severe complexity", "MED-COMPLEX"),
    ("L61A", "Kidney failure with catastrophic complexity", "MED-COMPLEX"),
    ("T60A", "Septicaemia with catastrophic complexity", "MED-COMPLEX"),
    ("Q61A", "Red blood cell disorders, major complexity", "MED-GEN"),
    ("Q61B", "Red blood cell disorders, minor complexity", "MED-GEN"),
    ("F72A", "Unstable angina with complexity", "MED-GEN"),
    ("Z64A", "Other factors influencing health status, major complexity", "MED-GEN"),
    ("Z64B", "Other factors influencing health status, minor complexity", "MED-GEN"),
    ("J11Z", "Other skin, subcutaneous tissue and breast procedures", "SURG-MIN"),
    ("L61Z", "Haemodialysis, same day", "SAME-DAY"),
    ("960Z", "Ungroupable", None),
    ("961Z", "Unacceptable principal diagnosis", None),
]
DRG_BAND = {c: b for c, _, b in DRGS}
AGE_BANDS = ["U50", "50-64", "65-79", "80+"]

# Baseline stratum rates published with specification 4.0 (complications per episode), risk band x age band.
# Derived in the fiction from FY2023-24 network activity; the pack ships them as a lookup.
STRATUM_RATE = {
    ("ORTH-MAJ", "U50"): 0.0612, ("ORTH-MAJ", "50-64"): 0.0784, ("ORTH-MAJ", "65-79"): 0.1137,
    ("ORTH-MAJ", "80+"): 0.1683,
    ("ORTH-MIN", "U50"): 0.0329, ("ORTH-MIN", "50-64"): 0.0438, ("ORTH-MIN", "65-79"): 0.0671,
    ("ORTH-MIN", "80+"): 0.1024,
    ("SURG-MAJ", "U50"): 0.0871, ("SURG-MAJ", "50-64"): 0.1086, ("SURG-MAJ", "65-79"): 0.1452,
    ("SURG-MAJ", "80+"): 0.2013,
    ("SURG-MIN", "U50"): 0.0284, ("SURG-MIN", "50-64"): 0.0361, ("SURG-MIN", "65-79"): 0.0529,
    ("SURG-MIN", "80+"): 0.0817,
    ("MED-COMPLEX", "U50"): 0.0596, ("MED-COMPLEX", "50-64"): 0.0742, ("MED-COMPLEX", "65-79"): 0.1068,
    ("MED-COMPLEX", "80+"): 0.1541,
    ("MED-GEN", "U50"): 0.0271, ("MED-GEN", "50-64"): 0.0348, ("MED-GEN", "65-79"): 0.0512,
    ("MED-GEN", "80+"): 0.0769,
}

# Case mix profiles: band -> (weight, age distribution over AGE_BANDS)
MIX = {
    "gen_med": {"MED-COMPLEX": (0.58, [0.07, 0.17, 0.36, 0.40]), "MED-GEN": (0.34, [0.11, 0.21, 0.35, 0.33]),
                "SURG-MIN": (0.08, [0.14, 0.24, 0.34, 0.28])},
    "gen_surg": {"SURG-MAJ": (0.38, [0.13, 0.26, 0.38, 0.23]), "SURG-MIN": (0.47, [0.21, 0.28, 0.32, 0.19]),
                 "MED-GEN": (0.15, [0.16, 0.25, 0.33, 0.26])},
    "ortho": {"ORTH-MAJ": (0.52, [0.07, 0.19, 0.42, 0.32]), "ORTH-MIN": (0.37, [0.19, 0.24, 0.31, 0.26]),
              "MED-GEN": (0.11, [0.13, 0.22, 0.34, 0.31])},
    "resp": {"MED-COMPLEX": (0.74, [0.06, 0.16, 0.38, 0.40]), "MED-GEN": (0.26, [0.10, 0.20, 0.36, 0.34])},
    "vasc": {"SURG-MAJ": (0.44, [0.05, 0.21, 0.43, 0.31]), "SURG-MIN": (0.33, [0.09, 0.24, 0.39, 0.28]),
             "MED-COMPLEX": (0.23, [0.06, 0.18, 0.40, 0.36])},
    "renal": {"MED-COMPLEX": (0.63, [0.12, 0.24, 0.37, 0.27]), "MED-GEN": (0.37, [0.15, 0.26, 0.34, 0.25])},
    "aged": {"MED-COMPLEX": (0.49, [0.00, 0.03, 0.31, 0.66]), "MED-GEN": (0.44, [0.00, 0.04, 0.33, 0.63]),
             "SURG-MIN": (0.07, [0.00, 0.05, 0.35, 0.60])},
    "colorectal": {"SURG-MAJ": (0.61, [0.11, 0.25, 0.39, 0.25]), "SURG-MIN": (0.28, [0.18, 0.27, 0.34, 0.21]),
                   "MED-GEN": (0.11, [0.15, 0.24, 0.35, 0.26])},
    "neuro": {"MED-COMPLEX": (0.69, [0.09, 0.20, 0.38, 0.33]), "MED-GEN": (0.31, [0.13, 0.23, 0.35, 0.29])},
    "subacute": {"MED-GEN": (0.72, [0.06, 0.15, 0.37, 0.42]), "MED-COMPLEX": (0.28, [0.05, 0.14, 0.38, 0.43])},
}

# Units. role is the generator's own label for the ladder; psi is the unit's persistent standardised ratio;
# sep is mean in-scope separations a quarter; plan is planned separations for the quarter from 1 April 2027;
# ylast is the designed standardised ratio for the last closed quarter (2026-27 Q2).
# status: "eligible" (a candidate), "embedded" (placed within twelve closed quarters), "nonacute", "merged_into".
UNITS = [
    # code, name, hospital, mix, service, psi, sep, plan, ylast, role, status
    ("41210", "General Medicine", "H1", "gen_med", "acute", 1.034, 2300, 2077, 1.188, "largest", "eligible"),
    ("41220", "General Surgery", "H1", "gen_surg", "acute", 1.112, 2600, 3560, 1.043, "runner_up", "eligible"),
    ("41230", "Orthopaedics", "H1", "ortho", "acute", 1.233, 1900, 2305, 1.090, "answer", "eligible"),
    ("41240", "Respiratory Medicine", "H1", "resp", "acute", 1.091, 1050, 1257, 1.272, "hot2", "eligible"),
    ("41310", "General Medicine", "H2", "gen_med", "acute", 1.158, 1350, 1364, 1.088, "mid", "eligible"),
    ("41320", "General Surgery", "H2", "gen_surg", "acute", 1.047, 1200, 1470, 1.102, "hot3", "eligible"),
    ("41330", "Vascular Surgery", "H2", "vasc", "acute", 1.307, 430, 506, 1.161, "worst_level", "eligible"),
    ("41410", "Orthopaedics", "H3", "ortho", "acute", 1.081, 620, 735, 1.462, "hot1", "eligible"),
    ("41420", "General Medicine", "H3", "gen_med", "acute", 1.245, 980, 1162, 1.112, "mid", "eligible"),
    ("41430", "Renal Medicine", "H3", "renal", "acute", 1.042, 560, 652, 1.119, "mid", "eligible"),
    ("41510", "General Medicine", "H4", "gen_med", "acute", 1.162, 390, 466, 1.071, "merged", "eligible"),
    ("41520", "Surgical Services", "H4", "gen_surg", "acute", 1.124, 500, 779, 1.121, "rising", "eligible"),
    # units the programme has already been placed with inside the twelve closed quarters
    ("41250", "Colorectal Surgery", "H1", "colorectal", "acute", 1.236, 1150, 1210, None, "embed", "embedded"),
    ("41260", "Aged Care", "H1", "aged", "acute", 1.288, 880, 920, None, "embed", "embedded"),
    ("41270", "Neurosciences", "H1", "neuro", "acute", 1.194, 1150, 800, None, "embed", "embedded"),
    ("41340", "Orthopaedics", "H2", "ortho", "acute", 1.252, 900, 950, None, "embed", "embedded"),
    ("41350", "Respiratory Medicine", "H2", "resp", "acute", 1.173, 1000, 870, None, "embed", "embedded"),
    ("41360", "Aged Care", "H2", "aged", "acute", 1.311, 640, 680, None, "embed", "embedded"),
    ("41440", "General Surgery", "H3", "gen_surg", "acute", 1.112, 2400, 1080, None, "embed", "embedded"),
    ("41450", "Aged Care", "H3", "aged", "acute", 1.464, 520, 550, None, "embed", "embedded"),
    # the unit the team is with now, for the quarter in progress: no closed data for the placement
    ("41460", "Rehabilitation and Aged Care", "H3", "aged", "acute", 1.221, 470, 500, None, "current", "embedded"),
    # non-acute units: outside the indicator's scope (specification 4.0 clause 2.3)
    ("41610", "Sub-acute Rehabilitation", "H2", "subacute", "rehabilitation", 1.0, 330, 350, None, "scope", "nonacute"),
    ("41620", "Older Persons Mental Health", "H3", "subacute", "psychiatric", 1.0, 290, 300, None, "scope", "nonacute"),
    ("41630", "Sub-acute Rehabilitation", "H4", "subacute", "rehabilitation", 1.0, 240, 250, None, "scope", "nonacute"),
    # predecessor units amalgamated into 41510 on 1 October 2025
    ("41511", "Medical Ward 1", "H4", "gen_med", "acute", 1.162, 205, None, None, "pred", "merged_into"),
    ("41512", "Medical Ward 2", "H4", "gen_med", "acute", 1.162, 185, None, None, "pred", "merged_into"),
]

MERGE_DATE = dt.date(2025, 10, 1)
MERGE_INTO = "41510"
MERGE_FROM = ["41511", "41512"]

# The improvement embeds already closed, quarter index -> unit code (quarter index into QUARTERS).
EMBEDS = {3: "41250", 4: "41260", 5: "41340", 6: "41440", 7: "41350", 8: "41450", 9: "41270"}
EMBED_CURRENT = ("2026-27 Q3", "41460")   # in progress, outside the extract
EMBED_EFFECT = 0.41                      # share of a unit's persistent excess an embed removes in its quarter
EMBED_RETAIN = [0.72, 0.84]              # the gain fades: excess back to these shares of persistent in later quarters
TEAM_FTE = 2.4

# The hospital-acquired complication list, as the national list numbered the categories under the 2022
# revision (in force to 30 June 2026) and under the 2026 revision (in force from 1 July 2026). The 2026
# revision renumbered the middle of the list, so HAC04 and HAC05 name different categories either side of
# 1 July 2026 and HAC13 was folded into HAC03.
HAC_GROUPS = [
    ("G1", "Healthcare-associated infections"),
    ("G2", "Pressure injuries"),
    ("G3", "Falls resulting in fracture or intracranial injury"),
    ("G4", "Medication and anaesthetic complications"),
    ("G5", "Delirium"),
    ("G6", "Respiratory complications"),
    ("G7", "Venous thromboembolism"),
    ("G8", "Surgical complications requiring unplanned return to theatre"),
]
GROUP_NAME = dict(HAC_GROUPS)
LIST_2022 = [
    ("HAC01", "Healthcare-associated bloodstream infection", "G1"),
    ("HAC02", "Surgical site infection", "G1"),
    ("HAC03", "Pressure injury", "G2"),
    ("HAC04", "Fall resulting in fracture or intracranial injury", "G3"),
    ("HAC05", "Medication complication", "G4"),
    ("HAC06", "Anaesthetic complication", "G4"),
    ("HAC07", "Delirium", "G5"),
    ("HAC08", "Respiratory complication", "G6"),
    ("HAC09", "Hospital-acquired pneumonia", "G6"),
    ("HAC10", "Venous thromboembolism", "G7"),
    ("HAC11", "Unplanned return to theatre", "G8"),
    ("HAC12", "Wound dehiscence", "G8"),
    ("HAC13", "Catheter-associated urinary tract infection", "G1"),
]
LIST_2026 = [
    ("HAC01", "Healthcare-associated bloodstream infection", "G1"),
    ("HAC02", "Surgical site infection", "G1"),
    ("HAC03", "Catheter-associated urinary tract infection", "G1"),
    ("HAC04", "Pressure injury", "G2"),
    ("HAC05", "Fall resulting in fracture or intracranial injury", "G3"),
    ("HAC06", "Medication complication", "G4"),
    ("HAC07", "Delirium", "G5"),
    ("HAC08", "Respiratory complication", "G6"),
    ("HAC09", "Hospital-acquired pneumonia", "G6"),
    ("HAC10", "Venous thromboembolism", "G7"),
    ("HAC11", "Unplanned return to theatre", "G8"),
    ("HAC12", "Wound dehiscence", "G8"),
]
CODE_2022 = {c: g for c, _, g in LIST_2022}
CODE_2026 = {c: g for c, _, g in LIST_2026}
# the share of complications in each group, by case-mix profile
GROUP_MIX = {
    "surgical": {"G1": 0.21, "G2": 0.07, "G3": 0.05, "G4": 0.12, "G5": 0.08, "G6": 0.14, "G7": 0.11, "G8": 0.22},
    "medical": {"G1": 0.18, "G2": 0.16, "G3": 0.13, "G4": 0.13, "G5": 0.19, "G6": 0.17, "G7": 0.04, "G8": 0.00},
    "ortho": {"G1": 0.17, "G2": 0.11, "G3": 0.16, "G4": 0.10, "G5": 0.12, "G6": 0.09, "G7": 0.13, "G8": 0.12},
}
MIX_FAMILY = {"gen_med": "medical", "resp": "medical", "renal": "medical", "aged": "medical",
              "neuro": "medical", "subacute": "medical", "gen_surg": "surgical", "vasc": "surgical",
              "colorectal": "surgical", "ortho": "ortho"}
SECOND_COMPLICATION = 0.268     # share of affected episodes recording a second complication
THIRD_COMPLICATION = 0.031      # and a third
# the complication detail extract covers the units on the clinical information system; the wards on the
# Carrowdean campus record complications in the campus module and reach the warehouse through the extract
DETAIL_EXCLUDED = ("41510", "41511", "41512", "41520", "41630")

# The 2026 cost centre realignment: three units reported under another hospital site from 1 July 2026.
# unit_register.csv is the master at the export date, so only activity_summary_monthly.csv carries the
# site each unit sat under in each month.
REALIGNMENT_DATE = dt.date(2026, 7, 1)
REALIGNED = {"41430": ("H3", "H2"), "41270": ("H1", "H2"), "41520": ("H4", "H3")}
# the two feed migrations that re-sent a block of non-acute episodes under fresh episode identifiers
REPLAYS = [(dt.date(2025, 11, 1), 0.62), (dt.date(2026, 8, 1), 0.55)]

SEED = 194194
