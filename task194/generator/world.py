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
REF_RATE = 96.6                          # complications per 1,000 episodes, published with specification 4.0
PUBLIC_HOLIDAYS = {    # the network's own calendar: separations fall away and admissions stop
    (1, 1), (1, 26), (4, 25), (6, 9), (10, 6), (12, 24), (12, 25), (12, 26), (12, 27), (12, 31),
}
EASTER = {2024: dt.date(2024, 3, 29), 2025: dt.date(2025, 4, 18), 2026: dt.date(2026, 4, 3),
          2027: dt.date(2027, 3, 26)}      # Good Friday; Easter Monday is three days later
CODESET_CHANGE = dt.date(2026, 7, 1)     # national complication list revision, list 2022 -> list 2026

PEOPLE = {
    "director": ("Maureen Watts", "Director, Clinical Improvement"),
    "governance": ("Joseph Hunter", "Manager, Clinical Information and Coding"),
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

# What the network's own rate in each risk band now sits at, against the rate published with specification
# 4.0. The published table was built on FY2023-24 activity and clause 3.1 says it is not re-estimated
# between specifications; since it was set, a falls and pressure-injury programme has pulled the
# orthopaedic and medical bands below it while theatre throughput has pushed the surgical bands above it.
NETWORK_DRIFT = {"ORTH-MAJ": 0.962, "ORTH-MIN": 0.971, "MED-COMPLEX": 0.993, "MED-GEN": 1.008,
                 "SURG-MAJ": 1.034, "SURG-MIN": 1.046, "SAME-DAY": 1.0}

# the unit whose case mix moved between two closed quarters while its own practice did not: the
# orthopaedic theatre at Marrowfield was closed for ventilation works for two quarters, elective
# joint replacement stopped, and the ward's beds carried the hospital's emergency general surgical
# admissions instead. The unit's volume is unchanged and its own practice is unchanged.
MIX_SHIFT_UNIT = "41410"
MIX_SHIFT_QUARTERS = (5, 6)
MIX_SHIFT_PROFILE = "ortho_backfill"
ADDITIVE_UNIT = "41410"       # its rate is the network's rate in each band plus a constant per episode
ADDITIVE_C = 0.0091

# The day-procedure feed did not deliver for two months at three units while the theatre management system
# was migrated, one unit at each of the two sites whose theatre suites were on the old system. The patient administration system counted those
# separations, so the activity summary carries them and the episode extract does not. Every unit here is a
# unit the improvement team has already been placed with, so none is a candidate, and every record the feed
# missed is a same-day separation, which specification 2.1 puts outside the indicator: the gap can reach
# neither a candidate's separations nor any in-scope episode.
FEED_GAP = {"41250": ("2026-04", "2026-05"),
            "41350": ("2026-07", "2026-08")}

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
    # the two quarters the orthopaedic theatre at Marrowfield was closed: elective joint replacement
    # stopped and the ward carried emergency general surgical admissions instead. The same unit, the
    # same staff and the same number of beds, a different mix of patients.
    "ortho_backfill": {"ORTH-MAJ": (0.09, [0.04, 0.14, 0.40, 0.42]), "ORTH-MIN": (0.27, [0.19, 0.24, 0.31, 0.26]),
                       "SURG-MIN": (0.52, [0.24, 0.27, 0.30, 0.19]), "MED-GEN": (0.12, [0.13, 0.22, 0.34, 0.31])},
    "resp": {"MED-COMPLEX": (0.74, [0.06, 0.16, 0.38, 0.40]), "MED-GEN": (0.26, [0.10, 0.20, 0.36, 0.34])},
    "vasc": {"SURG-MAJ": (0.44, [0.05, 0.21, 0.43, 0.31]), "SURG-MIN": (0.33, [0.09, 0.24, 0.39, 0.28]),
             "MED-COMPLEX": (0.23, [0.06, 0.18, 0.40, 0.36])},
    # a renal medicine unit's own theatre work: vascular access for the dialysis population
    "renal": {"MED-COMPLEX": (0.57, [0.12, 0.24, 0.37, 0.27]), "MED-GEN": (0.31, [0.15, 0.26, 0.34, 0.25]),
              "SURG-MIN": (0.12, [0.14, 0.27, 0.36, 0.23])},
    # the Carrowdean medical wards: a district hospital's general medicine, less complex than a principal
    # referral hospital's and carrying its own minor surgical list
    "gen_med_district": {"MED-GEN": (0.58, [0.13, 0.23, 0.34, 0.30]),
                         "MED-COMPLEX": (0.30, [0.08, 0.19, 0.36, 0.37]),
                         "SURG-MIN": (0.12, [0.17, 0.26, 0.34, 0.23])},
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
    ("41210", "General Medicine", "H1", "gen_med", "acute", 1.11656, 3680, 4259, None, "largest", "eligible"),
    ("41220", "General Surgery", "H1", "gen_surg", "acute", 1.03850, 4160, 4760, None, "runner_up", "eligible"),
    ("41230", "Orthopaedics", "H1", "ortho", "acute", 1.10461, 3040, 3100, None, "answer", "eligible"),
    ("41240", "Respiratory Medicine", "H1", "resp", "acute", 1.07756, 1680, 1700, 1.34562, "hot2", "eligible"),
    ("41310", "General Medicine", "H2", "gen_med", "acute", 1.03335, 2150, 2000, 1.10427, "mid", "eligible"),
    ("41320", "General Surgery", "H2", "gen_surg", "acute", 1.04986, 1920, 2100, 1.14160, "hot3", "eligible"),
    ("41330", "Vascular Surgery", "H2", "vasc", "acute", 1.04915, 688, 760, 1.16906, "worst_level", "eligible"),
    ("41410", "Orthopaedics", "H3", "ortho", "acute", 1.04301, 992, 1100, None, "hot1", "eligible"),
    ("41420", "General Medicine", "H3", "gen_med", "acute", 1.03471, 1568, 1600, 1.11042, "mid", "eligible"),
    ("41430", "Renal Medicine", "H3", "renal", "acute", 1.03488, 896, 950, 1.14649, "mid", "eligible"),
    ("41510", "General Medicine", "H4", "gen_med_district", "acute", 1.03565, 624, 700, 1.05577, "merged", "eligible"),
    ("41520", "Surgical Services", "H4", "gen_surg", "acute", 1.02896, 800, 1100, 1.07843, "rising", "eligible"),
    # units the programme has already been placed with inside the twelve closed quarters. Earlier cycles
    # were decided on the quarter closed at the time, so the register holds units that were standing badly
    # over their own record beside units that were having one bad quarter on an ordinary record.
    ("41250", "Colorectal Surgery", "H1", "colorectal", "acute", 1.01100, 3520, 3584, None, "embed", "embedded"),
    ("41260", "Aged Care", "H2", "aged", "acute", 1.09800, 2672, 2720, None, "embed", "embedded"),
    ("41270", "Neurosciences", "H1", "neuro", "acute", 1.06100, 3520, 3600, None, "embed", "embedded"),
    ("41340", "Orthopaedics", "H3", "ortho", "acute", 1.02100, 2000, 2064, None, "embed", "embedded"),
    ("41350", "Respiratory Medicine", "H2", "resp", "acute", 1.08300, 2128, 2176, None, "embed", "embedded"),
    ("41360", "Aged Care", "H1", "aged", "acute", 1.06200, 1784, 1824, None, "embed", "embedded"),
    ("41440", "General Surgery", "H3", "gen_surg", "acute", 0.99100, 4832, 4928, None, "embed", "embedded"),
    ("41450", "Geriatric Evaluation and Management", "H1", "aged", "acute", 1.10600, 1731, 1776, None, "embed", "embedded"),
    # the unit the team is with now, for the quarter in progress: no closed data for the placement
    ("41460", "Rehabilitation and Aged Care", "H3", "aged", "acute", 1.07400, 752, 800, None, "current", "embedded"),
    # non-acute units: outside the indicator's scope (specification 4.0 clause 2.3)
    ("41610", "Sub-acute Rehabilitation", "H2", "subacute", "rehabilitation", 1.0, 528, 560, None, "scope", "nonacute"),
    ("41620", "Older Persons Mental Health", "H3", "subacute", "psychiatric", 1.0, 464, 480, None, "scope", "nonacute"),
    ("41630", "Sub-acute Rehabilitation", "H4", "subacute", "rehabilitation", 1.0, 384, 400, None, "scope", "nonacute"),
    # predecessor units amalgamated into 41510 on 1 October 2025
    ("41511", "Medical Ward 1", "H4", "gen_med_district", "acute", 1.05800, 328, None, None, "pred", "merged_into"),
    ("41512", "Medical Ward 2", "H4", "gen_med_district", "acute", 1.05800, 296, None, None, "pred", "merged_into"),
]

MERGE_DATE = dt.date(2025, 10, 1)
MERGE_INTO = "41510"
MERGE_FROM = ["41511", "41512"]

# The improvement embeds already closed, quarter index -> unit code (quarter index into QUARTERS).
EMBEDS = {2: "41440", 3: "41250", 4: "41270", 5: "41260", 6: "41350", 7: "41340",
          8: "41360", 9: "41450"}
EMBED_CURRENT = ("2026-27 Q3", "41460")   # in progress, outside the extract
EMBED_EFFECT = 0.50                      # share of a unit's persistent excess an embed removes in its quarter
EMBED_RETAIN = [0.68, 0.85]              # the gain fades: excess back to these shares of persistent in later quarters
EMBED_Q = {v: k for k, v in EMBEDS.items()}
# Three units whose practice did not hold still across the specification period. A level for the first six
# closed quarters and another for the last four, rather than one level for all ten: a unit whose nursing
# establishment, its patient profile or its own practice changed partway through the period reports two
# levels, not one. The pair is normalised against the unit's own expected numbers, so the unit's pooled
# ratio over the ten closed quarters is still its persistent ratio and only the shape inside the window
# changes. Every other unit sits at one level and swings around it.
RATIO_PATH = {
    "41210": (0.9630, 1.0554),   # a general medicine unit whose complication rate rose through 2026
    "41220": (1.0278, 0.9584),   # a general surgical unit whose rate came down over the same quarters
    "41230": (1.0448, 0.9328),   # and an orthopaedic unit that had its bad quarters early
}
PATH_SPLIT = 6                   # the quarter index the second level starts at

OVERDISPERSION = 1.45                    # Pearson residual of a unit-quarter count against its expected number
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
    "surgical": {"G1": 0.14, "G2": 0.04, "G3": 0.10, "G4": 0.14, "G5": 0.06, "G6": 0.13, "G7": 0.09, "G8": 0.30},
    "medical": {"G1": 0.20, "G2": 0.17, "G3": 0.09, "G4": 0.09, "G5": 0.19, "G6": 0.22, "G7": 0.04, "G8": 0.00},
    "ortho": {"G1": 0.16, "G2": 0.12, "G3": 0.19, "G4": 0.09, "G5": 0.10, "G6": 0.08, "G7": 0.14, "G8": 0.12},
}
# Which harms a unit's patients suffer runs on how old they are: an eighty-year-old medical inpatient's
# complications are pressure injuries and delirium, a fifty-year-old surgical patient's are a return to
# theatre and a wound infection. The group mix a unit produces is therefore its clinical family's mix
# pulled towards this profile by the share of its own episodes in the oldest age band, which the extract
# carries in its age_band column.
GROUP_MIX_OLDEST = {"G1": 0.18, "G2": 0.34, "G3": 0.06, "G4": 0.03, "G5": 0.30, "G6": 0.09,
                    "G7": 0.00, "G8": 0.00}
OLDEST_PULL = 1.35          # how strongly the oldest band's share pulls the mix towards that profile

# How complete each reporting group is when a quarter is first published and at each restatement after it.
# A complication is coded when it is documented, and documentation runs on the group's own clinical course:
# a fall resulting in fracture and an unplanned return to theatre are documented the day they happen, while
# a pressure injury is staged and audited retrospectively, delirium is often recorded on later review, and a
# surgical site infection or a venous thromboembolism is frequently identified after the patient has gone
# home and reaches the record through the readmission. The share is of the complications that quarter will
# ultimately carry, at the quarter's own close and at the two closes after it.
# How complete a quarter's complications are when it is first published and at each restatement after it,
# by how the complication was recorded. A complication recorded at the point of care on the clinical
# information system reaches the warehouse with the episode and is coded in the same cycle; one written in
# the paper notes is coded whenever the coder reaches that chart, which is often after the quarter has
# already been published. The share is of the complications the episode's quarter will ultimately carry, at
# the quarter's own close and at the three closes after it.
ELEC_COMPLETENESS = (0.966, 0.991, 0.998, 1.000)
PAPER_COMPLETENESS = (0.558, 0.762, 0.888, 0.962)
LAG_COMPLETE = 4            # a quarter stops moving four closes after its own

# When each cost centre's wards were registered on the clinical information system. The programme ran ward
# by ward from July 2022 and was still running at the export date, in the order the vendor's implementation
# partner and the network's own cabling and device procurement allowed, so it runs across sites and across
# specialties rather than with either.
CIS_MIGRATION = {
    "41210": dt.date(2027, 3, 1), "41220": dt.date(2022, 10, 1), "41230": dt.date(2023, 4, 1),
    "41240": dt.date(2023, 10, 1), "41310": dt.date(2022, 7, 1), "41320": dt.date(2024, 1, 1),
    "41330": dt.date(2023, 7, 1), "41410": dt.date(2024, 1, 1), "41420": dt.date(2023, 1, 1),
    "41430": dt.date(2022, 10, 1), "41510": dt.date(2023, 4, 1), "41520": dt.date(2027, 1, 4),
    "41250": dt.date(2024, 7, 1), "41260": dt.date(2025, 1, 1), "41270": dt.date(2024, 4, 1),
    "41340": dt.date(2025, 7, 1), "41350": dt.date(2024, 10, 1), "41360": dt.date(2023, 7, 1),
    "41440": dt.date(2025, 4, 1), "41450": dt.date(2025, 10, 1), "41460": dt.date(2026, 7, 1),
    "41610": dt.date(2025, 10, 1), "41620": dt.date(2026, 4, 1), "41630": dt.date(2026, 10, 1),
    "41511": dt.date(2023, 4, 1), "41512": dt.date(2023, 4, 1),
}
# How much of a ward's recording actually moved onto the system once its wards were registered. A ward is
# registered for orders and results long before the clinical team stops writing in the notes, and how far
# it gets depends on the ward: its device count, its establishment, how its nurse unit manager runs the
# round, whether its building has bedside terminals. Two cost centres registered in the same quarter sit
# years apart on this, which is why the registration date explains only part of how fast a cost centre's
# coding settles.
CIS_ADOPTION = {
    "41210": 0.000, "41220": 0.995, "41230": 0.985, "41240": 0.960, "41310": 0.975, "41320": 0.990,
    "41330": 0.460, "41410": 0.380, "41420": 0.930, "41430": 0.550, "41510": 0.900, "41520": 0.000,
    "41250": 0.970, "41260": 0.900, "41270": 0.955, "41340": 0.880, "41350": 0.945, "41360": 0.860,
    "41440": 0.965, "41450": 0.915, "41460": 0.890, "41610": 0.930, "41620": 0.905, "41630": 0.870,
    "41511": 0.700, "41512": 0.700,
}
# how far through its own adoption a ward is in each of the first three quarters after registration
CIS_RAMP = ((91, 0.55), (182, 0.82), (273, 0.94))
CIS_SETTLED = 0.985         # where a cost centre with no adoption of its own sits

IMMATURE = {9: 0, 8: 1, 7: 2, 6: 3}   # quarter index -> how many closes have passed since its own
# where each unit type's other quarterly indicators sit: deaths in hospital per 1,000 separations and
# unplanned readmissions within 28 days per 100, on the dashboard beside the complication indicator
OTHER_INDICATORS = {
    "aged": (26.0, 9.0, 13.2, 3.0), "gen_med": (17.5, 6.0, 11.8, 2.6), "resp": (14.0, 5.0, 12.6, 2.4),
    "gen_med_district": (15.0, 5.5, 10.9, 2.5),
    "renal": (11.0, 4.0, 14.1, 2.8), "neuro": (19.0, 7.5, 9.4, 2.2), "subacute": (6.0, 3.0, 7.2, 1.8),
    "ortho": (2.1, 1.2, 5.6, 1.5), "gen_surg": (5.4, 2.4, 6.9, 1.7),
    "colorectal": (6.8, 2.8, 8.3, 2.0), "vasc": (12.5, 4.5, 9.8, 2.5),
}
MIX_FAMILY = {"gen_med": "medical", "gen_med_district": "medical", "resp": "medical", "renal": "medical", "aged": "medical",
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
