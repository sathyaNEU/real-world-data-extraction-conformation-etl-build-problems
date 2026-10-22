"""task249 architecture 6: the Certified Clinical Coder examination's world (item bank, forms, timed sittings,
resits, reviews) and the request's settings."""
SEED = 2496

# windows: 2026 W1..W4, 2027 W5..W8 (February, May, August, November)
WINDOWS = ["2026-02", "2026-05", "2026-08", "2026-11", "2027-02", "2027-05", "2027-08", "2027-11"]
W_START = {"2026-02": (2026, 2, 9), "2026-05": (2026, 5, 11), "2026-08": (2026, 8, 10), "2026-11": (2026, 11, 9),
           "2027-02": (2027, 2, 8), "2027-05": (2027, 5, 10), "2027-08": (2027, 8, 9), "2027-11": (2027, 11, 8)}
WINDOW_DAYS = 12
RESULTS_AFTER = 24          # days from a window's first day to the release of its results
F26 = ["CC26-%s" % x for x in "ABCDEF"]
F27 = ["CC27-%s" % x for x in "ABCDEFGHIJ"]
W_FORMS = {0: [0, 1, 2], 1: [1, 2, 3], 2: [3, 4, 5], 3: [4, 5, 0],
           4: [6, 7, 8, 9, 10], 5: [6, 7, 8, 9, 10], 6: [11, 12, 13, 14, 15], 7: [11, 12, 13, 14, 15]}
NOP, NTR = 150, 20
TRIAL_SLOTS = [31, 32, 33, 34, 35, 66, 67, 68, 69, 70, 101, 102, 103, 104, 105, 136, 137, 138, 139, 140]  # 1-based
NFT = 3200                  # first-time candidates per window
PASS_RAW = 105              # of 150
P_RESIT = 0.75
GAP_P = {1: 0.55, 2: 0.30, 3: 0.15}
P_REVIEW = 0.30             # a failing candidate books a results review
P_REVIEW_HELD = 0.88        # a booked review is held (the rest cancelled or not attended)
P_RENUMBER = 0.07           # a returning candidate's number changed with their membership class
LEARN = 0.25
LEARN_SD = 0.30
C_GUESS = 0.20

# memory: logit lift on an item shown at an earlier sitting (decays with windows since)
M_WRONG, M_RIGHT, M_REVIEW = 0.75, 0.30, 1.80
M_SIB = 0.80                # an item written from the same item model carries this share
DECAY = 3.0

# time: a four-hour open-book sitting, items worked in delivery order, an item not answered at the limit left blank
LIMIT = 4 * 3600
T_SHORT, T_CASE, T_SD = 46.0, 114.0, 0.22     # median seconds of a single item and a case item for a typical candidate
EPS_SD = 0.30                                  # item-by-person time noise (log)
TAU_SD, TAU_RHO = 0.15, -0.30                  # person pace (log) and its correlation with ability
CASE_SHARE = {"CC26-A": .26, "CC26-B": .26, "CC26-C": .27, "CC26-D": .26, "CC26-E": .27, "CC26-F": .26}
# an item recognised from an earlier sitting skips the code lookup (time multiplied by), decaying like the memory
S_SEEN, S_REVIEW, S_SIB = 0.42, 0.36, 0.72

# 2027 form designs: items reused from the source forms, siblings of their items, trial items promoted; the rest new.
#   H1 forms (CC27-A..E) draw on the 2026 forms; H2 forms (CC27-F..J) on the H1 forms. case: the share of case items.
DESIGN = {
    "CC27-A": dict(reuse=55, sib=3, trial=4, case=.26),
    "CC27-B": dict(reuse=10, sib=4, trial=4, case=.45, rcase=True),
    "CC27-C": dict(reuse=6, sib=60, trial=4, case=.26),
    "CC27-D": dict(reuse=22, sib=2, trial=4, case=.45, easy=True, rcase=True),
    "CC27-E": dict(reuse=5, sib=6, trial=4, case=.27),
    "CC27-F": dict(reuse=4, sib=4, trial=4, case=.26),
    "CC27-G": dict(reuse=80, sib=4, trial=4, case=.26),
    "CC27-H": dict(reuse=8, sib=80, trial=4, case=.27),
    "CC27-I": dict(reuse=4, sib=4, trial=4, case=.45),
    "CC27-J": dict(reuse=5, sib=10, trial=4, case=.26),
}
THRESH = 1.0

CENTRES = ["Chennai", "Bengaluru", "Hyderabad", "Pune", "Kochi", "Noida"]
CENTRE_CODE = {"Chennai": "MAA", "Bengaluru": "BLR", "Hyderabad": "HYD", "Pune": "PNQ", "Kochi": "COK", "Noida": "NOI"}
CENTRE_W = [0.27, 0.19, 0.18, 0.13, 0.11, 0.12]
# each centre keeps its own sheet in the incident workbook: its column names, its dates and its names for the sessions
SHEETS = {
    "Chennai": dict(cols=["Date", "Session", "Time", "Workstation", "Report"], date="%d/%m/%Y", sess=("AM", "PM")),
    "Bengaluru": dict(cols=["Date", "Slot", "Time (IST)", "System", "Incident"], date="%d %b %Y",
                      sess=("Morning", "Afternoon")),
    "Hyderabad": dict(cols=["Exam date", "Session", "Time", "WS No", "Details"], date="%d.%m.%Y", sess=("AM", "PM")),
    "Pune": dict(cols=["Date", "Batch", "Time", "Terminal", "Report"], date="%Y-%m-%d", sess=("Batch 1", "Batch 2")),
    "Kochi": dict(cols=["Date", "Session", "Time", "Workstation", "Remarks"], date="%d/%m/%Y", sess=("FN", "AN")),
    "Noida": dict(cols=["Date", "Shift", "Reported at", "Seat", "What happened"], date="%d-%b-%y",
                  sess=("Morning", "Afternoon")),
}
AREAS = ["ICD-10-CM diagnosis coding", "ICD-10-PCS procedure coding", "CPT surgery coding",
         "CPT evaluation and management", "HCPCS and modifiers", "Coding guidelines and conventions",
         "Documentation and query practice", "Compliance and reimbursement"]

ORG = "Institute of Healthcare Coding Professionals"
ORG_SHORT = "IHCP"
DOMAIN = "ihcp.org.in"
EXAM = "Certified Clinical Coder"
VENDOR = "Pariksha Delivery Services Pvt Ltd"
PSYCH = ("Abhiram Sarin", "abhiram.sarin")          # examinations psychometrician (asks)
MANAGER = ("Yahvi Reddy", "yahvi.reddy")            # examinations manager
REQUEST_DATE = (2028, 1, 17)
COMMITTEE_DATE = "27 January 2028"
REPORT_DUE = "31 January 2028"
