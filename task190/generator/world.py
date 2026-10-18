"""task190 world constants. Nothing here is derived at run time except where a comment says so.

The National Institute for Environment Statistics (NIES) compiles Portugal's official waste
statistics. Its Business Waste Survey (BWS) is a stratified element sample of enterprises: the
250-or-more employee stratum is enumerated completely and response is compulsory under the
statistics act, the three smaller strata are sampled and voluntary. The National Waste Movement
Register (NWMR), run by the Environment Permit Agency, records every movement of controlled waste.
"""
SEED = 190
REF_YEAR = 2026
EXTRACT_REGISTER = "2027-01-31"
EXTRACT_SURVEY = "2027-01-16"
COMPLAINT_DATE = "2027-01-14"
RESPONSE_DUE = "2027-02-28"
CODE_REVISION = "2026-07-01"
PRIOR_EXTRACT = "2026-06-30"       # the register extract the 2025 release's Table 1 was taken at
FIELD_DAY_HOURS = 8                # the division books field effort in field days of this length
NOTE_DATE = "2027-02-09"           # the head of collection operations' memo
MODULE_DAYS = 46                   # field days the 2027 establishment leaves for one module

INSTITUTE = "National Institute for Environment Statistics"
AGENCY = "Environment Permit Agency"
REGISTER = "National Waste Movement Register"
SURVEY = "Business Waste Survey"
PLAN = "National Waste Management Plan 2024-2030"
COUNCIL = "Waste and Resources Council"

# personas: drawn with guard.py names --geo Portugal --seed 190, never typed from memory
PEOPLE = {
    "head_collection": "Diego Carvalho",      # Head of Collection Operations, the stakeholder
    "division_director": "Tatiana Jesus",     # the line manager the recommendation goes to
    "register_liaison": "Lourenco Monteiro",  # Environment Permit Agency liaison
    "council_secretary": "Hugo Azevedo",      # Waste and Resources Council
}

REGIONS = ["Norte", "Centro", "Lisboa", "Alentejo", "Algarve"]
REGION_W = [0.33, 0.24, 0.26, 0.10, 0.07]

# stratum: code, label, frame size N, responding sample r. E1 is enumerated completely.
STRATA = [
    ("E1", "250 or more employees", 155, 155),
    ("E2", "50 to 249 employees", 780, 195),
    ("E3", "10 to 49 employees", 4300, 520),
    ("E4", "1 to 9 employees", 31500, 760),
]
ISSUED = {"E1": 155, "E2": 210, "E3": 580, "E4": 880}   # questionnaires issued before nonresponse
OUT_OF_SCOPE = {"E1": 0, "E2": 4, "E3": 14, "E4": 24}   # found ceased or out of activity scope

# The 2025 round: the same frame and strata, a larger issued sample before the 2026 budget cut, so
# more usable returns in the voluntary strata. Only its published precision measure leaves it: no
# 2025 micro-data, sample count or weight ships, so nothing in the bundle reproduces the figure the
# 2025 release publishes, and it cannot confirm or refute any estimator of the 2026 round's.
STRATA_2025 = [("E1", 155, 155), ("E2", 780, 292), ("E3", 4300, 780), ("E4", 31500, 1140)]

# the eight statistical waste streams of the plan's target table, with the arisings process:
# participation probability, mean tonnes and coefficient of variation per stratum.
STREAMS = [
    ("metal",     "Metal and metal-bearing wastes",            [0.97, 0.055, 0.007, 0.0010], [760, 105, 17, 3.2],   [0.60, 0.45, 0.60, 0.70]),
    ("mixed_ci",  "Mixed commercial and industrial wastes",     [0.95, 0.86, 0.72, 0.46],    [300, 60, 13.5, 2.5],  [0.90, 1.50, 2.80, 4.00]),
    ("paper",     "Paper and board wastes",                     [0.70, 0.55, 0.40, 0.22],    [180, 40, 9.0, 1.7],   [0.90, 1.30, 2.20, 3.00]),
    ("wood",      "Wood wastes",                                [0.45, 0.35, 0.22, 0.10],    [240, 52, 11.0, 2.2],  [1.00, 1.40, 2.40, 3.20]),
    ("cd_rubble", "Mineral construction and demolition wastes",  [0.30, 0.26, 0.20, 0.14],   [900, 210, 46, 8.0],   [1.10, 1.60, 2.60, 3.40]),
    ("glass",     "Glass wastes",                               [0.42, 0.26, 0.14, 0.055],   [150, 28, 5.8, 1.1],   [0.90, 1.30, 2.00, 2.80]),
    ("plastic",   "Plastic wastes",                             [0.60, 0.48, 0.32, 0.16],    [90, 19, 4.2, 0.8],    [1.00, 1.40, 2.30, 3.10]),
    ("textile",   "Textile and leather wastes",                 [0.26, 0.18, 0.10, 0.042],   [84, 17, 3.8, 0.72],   [1.00, 1.40, 2.30, 3.00]),
]
STREAM_NAME = {k: n for k, n, _, _, _ in STREAMS}

# the printed 2026 recovery rate each stream is built to carry, per cent to one decimal. The
# register's recovered tonnage is set to land the true rate at the centre of this printed cell,
# which is what buys every graded rate its bin distance.
PRINTED_RATE = {"metal": 56.6, "mixed_ci": 59.6, "paper": 49.9, "wood": 43.7,
                "cd_rubble": 60.2, "glass": 53.7, "plastic": 33.8, "textile": 28.3}

# the designed distance from the plan target in standard errors of the rate, under the correct
# (design-based, finite-population-corrected) variance. The plan target follows from it.
Z_DESIGN = {"metal": 4.60, "mixed_ci": 1.45, "paper": 0.55, "wood": 0.45,
            "cd_rubble": 0.30, "glass": 0.60, "plastic": 0.70, "textile": 0.35}

# chain pass-through: share of arisings despatched off-site, and share of despatched tonnage
# that reaches a final treatment facility and is confirmed there.
DESPATCH_SHARE = {"metal": 0.93, "mixed_ci": 0.96, "paper": 0.90, "wood": 0.88,
                  "cd_rubble": 0.72, "glass": 0.91, "plastic": 0.89, "textile": 0.86}
CONFIRMED_SHARE = {"metal": 0.978, "mixed_ci": 0.964, "paper": 0.971, "wood": 0.969,
                   "cd_rubble": 0.958, "glass": 0.974, "plastic": 0.967, "textile": 0.962}

BAR = 1.959963985          # two-sided 95 per cent normal bar
GOLDEN_STREAM = "metal"
LOUD_STREAM = "mixed_ci"
