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

# The register's own clock. A treatment confirmation usually follows the receipt within days, but
# a load held for aggregation, a disputed weighbridge ticket or a record re-keyed after the
# agency's July 2026 system move is confirmed long after the despatch, so a share of consignments
# runs on a second, much longer clock. Nothing here is set from a published figure: the tail falls
# where these parameters put it, and the 2025 release's recovered column is then taken off the
# register at the extract date the release states.
# a load waiting on a treatment slot or a queried ticket: weeks to months
CONF_MID_P = 0.110
CONF_MID = (55, 0.50, 150)        # median days, sigma, cap
# a load held for aggregation, a disputed weight, a record re-keyed after the system move: months
CONF_LONG_P = 0.040
CONF_LONG = (250, 0.60, 620)

# What is unconfirmed at an extract is two different things: records that never close (the facility
# never filed) and the register's own right censoring, a load despatched too close to the extract
# for its confirmation to have arrived. The first is spread over the year, the second concentrates
# towards the extract date; a year on, only the first is left, which is what the 2025 file shows.
UNC_NEVER_SHARE = 0.42            # of the unconfirmed class, the share that never closes

# The weighbridge offsets on a class of consignments sum to this many hundredths of a tonne rather
# than to zero, so a stream and stage total is a tonnage the register adds up to and not a whole
# number: each one lands inside the tonne the deliverables print and on neither of its edges. Every
# partial sum (recovered, recovered plus disposal, all three) stays inside half a tonne, which is
# what holds the printed cell, and none of them is zero.
CLASS_RESID = {
    2026: {"metal":     (-24,  32, -18), "mixed_ci":  ( 16, -28,  22),
           "paper":     ( 28, -14, -10), "wood":      (-12,  26,  18),
           "cd_rubble": ( 20,  14, -36), "glass":     (-30,  -8,  26),
           "plastic":   ( 14,  18, -24), "textile":   (-26,  22,  12)},
    2025: {"metal":     ( 10, -24,  18), "mixed_ci":  ( -6,  28, -20),
           "paper":     ( 22,  12, -28), "wood":      (-16, -12,  30),
           "cd_rubble": (  8,  26, -18), "glass":     ( 14, -22,  26),
           "plastic":   (-12,  16,  24), "textile":   ( 12, -26, -14)},
}

# The 2025 release was compiled from the register extract of 30 June 2026, and the register has
# taken more than confirmations since that cut: consignments notified late by their producer and
# tonnages re-certified at the weighbridge audit, neither of which the published series is revised
# for. So a recompute at the stated cut lands near the published column, above it on every stream
# and on no stream reproducing it, by a share that carries no constant ratio.
PRIOR_DRIFT = {"metal": -0.0036, "mixed_ci": -0.0052, "paper": -0.0024, "wood": -0.0061,
               "cd_rubble": -0.0043, "glass": -0.0075, "plastic": -0.0031, "textile": -0.0068}

BAR = 1.959963985          # two-sided 95 per cent normal bar
GOLDEN_STREAM = "metal"
LOUD_STREAM = "mixed_ci"

# ---------------------------------------------------------------- the ask layer's own structures
# Ask A1's primary (D7 keys). A waste permit lapses when its holder stops the permitted activity,
# and the agency's January 2027 licensing batch drew on the numbers freed at the end of 2026, so a
# number the division's 2026 collection cases were opened under is now held by another enterprise,
# usually in another region. Every contact in the log predates the reissue, so the holder at the
# contact date is the enterprise the case was opened for; the crosswalk's current row is not.
PERMIT_REISSUE_N = 150            # cases of the round whose permit number has since been reissued
PERMIT_REISSUE_FROM = "2027-01-05"
PERMIT_REISSUE_SAME_REGION = 24   # of those, reissued inside the same region: the benign twin

# Field cases are allocated by workload, so a team near a boundary works some of the neighbouring
# region's cases and the team identifier is not the region of the enterprise contacted.
CROSS_TEAM_P = 0.14
NEIGHBOURS = {"Norte": ["Centro"], "Centro": ["Norte", "Lisboa"], "Lisboa": ["Centro", "Alentejo"],
              "Alentejo": ["Lisboa", "Algarve"], "Algarve": ["Alentejo"]}

# Ask A3's primary (D9 self-validation). Five municipalities on the same returns software file the
# year's own confirmation in the December slot of the monthly return, so that row is the year and
# not the month: it does not sum with its own eleven.
ANNUAL_IN_DECEMBER = ("Valongo", "Pombal", "Alenquer", "Moura", "Olhao")
