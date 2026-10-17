"""task239 constants: Lowfirth Parcels' 2027 Staff Voice survey and its Team Climate Index."""
import datetime as dt

SEED = 259

# calendar (local time is UK time, BST = UTC+1 throughout the fieldwork)
UTC_OFFSET = 1
REORG = dt.date(2027, 9, 1)                         # the reorganisation and the survey's census date
PACKS_PRINTED = dt.date(2027, 7, 21)
PACKS_POSTED = (dt.date(2027, 8, 23), dt.date(2027, 8, 25))
LIST_LOADED = dt.datetime(2027, 8, 24, 14, 0)       # the site tablets' team list, loaded before the reorganisation
OPEN = dt.datetime(2027, 9, 6, 8, 0)
REFRESH_OFF = dt.datetime(2027, 9, 13, 6, 0)        # tablets offline for the team list reload
REFRESH_ON = dt.datetime(2027, 9, 13, 7, 20)
REMINDERS = (dt.date(2027, 9, 20), dt.date(2027, 9, 29))
CLOSE = dt.datetime(2027, 10, 4, 23, 59, 59)
PAPER_DEADLINE = dt.date(2027, 10, 8)
LATE_SCANS = (dt.date(2027, 10, 11), dt.date(2027, 10, 14))
SYNC_FAULT = (dt.date(2027, 9, 13), dt.date(2027, 10, 1))
DASHBOARD = dt.date(2027, 11, 1)
DIVISION_MOVE = dt.date(2027, 11, 1)
REGISTER_EXTRACT = dt.date(2027, 11, 15)
ASOF = dt.date(2027, 11, 19)

DIVISIONS = [
    ("AM", "Hub Operations", 0.21),
    ("ST", "Linehaul and Fleet", 0.17),
    ("WC", "Customer Service", 0.10),
    ("MH", "Engineering", 0.14),
    ("CP", "Delivery Operations", 0.23),
    ("CS", "Corporate Services", 0.15),
]
PREFIX = {"AM": "HO", "ST": "LF", "WC": "CU", "MH": "EN", "CP": "DO", "CS": "CS"}   # each division's team-code prefix
EMAIL = {"AM": 0.70, "ST": 0.74, "WC": 0.76, "MH": 0.86, "CP": 0.80, "CS": 0.97}

# sites: (code, name, has tablets, divisions housed with weights)
SITES = [
    ("CHB", "Central Hub", True, {"AM": 0.62, "ST": 0.60, "WC": 0.55, "CS": 0.35}),
    ("WHB", "West Hub", True, {"AM": 0.38, "ST": 0.40, "WC": 0.25, "CS": 0.15}),
    ("NDP", "North Depot", True, {"CP": 0.28, "MH": 0.12, "WC": 0.08}),
    ("HRD", "Harbour Road Depot", True, {"CP": 0.30, "MH": 0.10, "WC": 0.12}),
    ("ENC", "Engineering Centre", True, {"MH": 0.60}),
    ("SDP", "South Depot", True, {"CP": 0.25, "MH": 0.18}),
    ("EDP", "East Depot", False, {"CP": 0.17}),
    ("HOF", "Head Office", False, {"CS": 0.50}),
]
SYNC_SITES = ("NDP", "HRD", "SDP", "ENC")
TABLETS = {"CHB": 9, "WHB": 6, "NDP": 3, "HRD": 3, "ENC": 4, "SDP": 3}

# structure: September teams and how they came from July's
N_TEAMS = 1638
REORG_SHARE = dict(renamed=0.081, merged=0.014, split=0.016, new=0.021)
REISSUED = 5                                         # split teams whose July code went to a new September team

# the Team Climate Index: code, wording, negatively worded, latent (icc, climate loading, workload loading,
# member loading), intercept, nonresponse rates (don't know, skipped)
ITEMS = [
    ("TC01", "It is safe to take a risk in this team.", False, (0.19, 0.92, 0.0, 0.75), 0.15, (0.005, 0.003)),
    ("TC02", "I can raise a problem in this team without worrying how it will be received.", False,
     (0.2, 0.92, 0.0, 0.73), 0.30, (0.004, 0.003)),
    ("TC03", "People in this team value the skills I bring.", False, (0.18, 0.92, 0.0, 0.76), 0.55, (0.004, 0.002)),
    ("TC04", "In this team, people are sometimes blamed when something goes wrong.", True,
     (0.2, 0.91, 0.0, 0.72), 0.05, (0.008, 0.003)),
    ("TC05", "I can ask colleagues in this team for help when I need it.", False, (0.19, 0.92, 0.0, 0.74), 0.70,
     (0.002, 0.002)),
    ("TC06", "My views are listened to in this team.", False, (0.2, 0.91, 0.0, 0.75), 0.25, (0.004, 0.003)),
    ("TC07", "It is difficult to disagree openly in this team.", True, (0.19, 0.92, 0.0, 0.71), 0.0, (0.009, 0.003)),
    ("TC08", "I am treated with respect by the people I work with.", False, (0.2, 0.91, 0.0, 0.74), 0.75,
     (0.002, 0.002)),
    ("TC09", "This team meets regularly to review how we are working.", False, (0.17, 0.90, 0.0, 0.08), 0.10,
     (0.015, 0.003)),
    ("TC10", "New starters in this team are given time to learn how things are done.", False,
     (0.19, 0.91, 0.0, 0.10), 0.20, (0.017, 0.003)),
    ("TC11", "I am able to do my job to a standard I am pleased with.", False, (0.04, 0.0, 0.85, 0.85), 0.35,
     (0.003, 0.002)),
    ("TC12", "Most days I go home feeling I have done a good job.", False, (0.045, 0.0, 0.80, 0.83), 0.45,
     (0.003, 0.002)),
]
RHO_CL = 0.2
THRESHOLDS = (-1.75, -0.85, 0.05, 1.0)               # latent cut points for the five answers, before intercepts

# the other questions on the form (not part of the index)
STAFF_GROUPS = ["Hub operatives", "Engineers", "Drivers", "Customer advisers", "Administrative",
                "Professional and technical", "Supervisors", "Senior managers"]
ENGAGE = [("EN01", "I would recommend the company as a place to work."), ("EN02", "I am enthusiastic about my job."),
          ("EN03", "Time passes quickly when I am working."), ("EN04", "I often think about leaving the company."),
          ("EN05", "I have the materials and equipment I need to do my work."),
          ("EN06", "I am given opportunities to develop my skills.")]

# who answers, and how
RESPONSE_MEAN = 0.49
CHANNEL = {"email_pack": (0.55, 0.10, 0.35), "email": (0.88, 0.12, 0.0), "pack": (0.0, 0.28, 0.72)}
PAPER_ALL_TEAMS = 0.07                               # teams whose manager asked for paper for everyone
SITE_CODE_ENTERED = 0.30
N_DUAL = 384
N_RESUBMIT = 71
P_REPLAY = 0.9
N_BLANK = 37
N_LATE = 83
DUAL_BOOST = 0.55                                    # members who return twice sit higher on the member factor
