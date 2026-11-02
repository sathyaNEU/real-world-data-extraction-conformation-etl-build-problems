"""task304 architecture 5: fixed parameters of the world (Ardleshire's principal road network and its 2026 junction
screening, the 2027 Junction Safety Fund bid, and the county's 2026 provisional police data)."""
import datetime as dt

SEED = 304

YEARS = list(range(2016, 2027))          # traffic estimates run to 2026
REC_YEARS = list(range(2016, 2026))      # the validated collision record the county keeps (2016 to 2025)
WINDOW = list(range(2021, 2026))         # the fund's record: the validated years 2021 to 2025
PRESENT = 2026                           # the fund's "2026 traffic"
SCREEN_MIN = 12                          # the county's 2026 screening: 12 or more injury collisions in 2021 to 2025

AS_OF = dt.date(2026, 12, 4)             # the bid is being written; it closes 29 January 2027
BID_CLOSES = dt.date(2027, 1, 29)

DISTRICTS = ["Ardle Vale", "Brindham", "Kestermoor"]

# The fund's crash modification factors for a roundabout replacing a give-way or stop-controlled junction (guidance
# Table 2): injury collisions after = factor x injury collisions before.
CMF = {"X": 0.52, "T": 0.70, "ST": 0.70}

# Truth: safety performance by layout (injury collisions a year), ln mu = b0 + b1 ln(major AADT) + b2 ln(minor AADT)
SPF = {"T": (-9.30, 0.64, 0.31), "ST": (-9.30, 0.64, 0.31), "X": (-8.85, 0.64, 0.36),
       "MR": (-9.05, 0.62, 0.33), "RB": (-9.60, 0.66, 0.28), "SIG": (-8.70, 0.60, 0.30)}
K_TRUE = 0.24                            # junction-to-junction spread beyond chance (gamma variance)
YEAR_FACTOR = {2016: 1.07, 2017: 1.05, 2018: 1.03, 2019: 1.02, 2020: 0.80, 2021: 0.94,
               2022: 1.0, 2023: 1.0, 2024: 1.0, 2025: 1.0, 2026: 1.0}

# Network size by layout and control (give-way or stop for T, ST, X)
N_LAYOUT = {"T": 960, "ST": 118, "X": 352, "MR": 61, "RB": 88, "SIG": 47}

# The six junctions the 2026 screening lists (designed; their 2021 to 2025 counts are their own records).
# name, district, layout, control, major road, minor road, major AADT 2026, minor AADT 2026, theta, counts 2021..2025
CANDIDATES = [
    ("Saxby Cross", "Kestermoor", "X", "GW", "B4419 Saxby Road", "Holt Lane", 4010, 1400, 2.55, [4, 3, 5, 5, 4]),
    ("Tollgate Crossroads", "Brindham", "X", "STOP", "A6118 Brindham Road", "Tollgate Road", 23360, 4150, 0.62, [2, 3, 2, 2, 3]),
    ("Mill Lane Crossroads", "Ardle Vale", "X", "GW", "A5207 Ardle Road", "B4421 Mill Lane", 11720, 3600, 1.27, [4, 4, 3, 4, 3]),
    ("Church Street Junction", "Kestermoor", "X", "GW", "B4433 Kestermoor Road", "Church Street", 8420, 2280, 1.55, [3, 2, 3, 3, 3]),
    ("Fen Lane Junction", "Brindham", "T", "GW", "A6118 Station Road", "Fen Lane", 10680, 3800, 1.90, [3, 3, 2, 3, 2]),
    ("Coppice Way Junction", "Ardle Vale", "ST", "GW", "A5207 London Road", "Coppice Way", 21170, 3300, 1.10, [3, 2, 2, 3, 2]),
]

# Collisions away from junctions and at junction types the record keeps, per year (validated record)
LINK_COLLISIONS = 2150                    # non-junction injury collisions a year, about
SEVERITY_SHARE = (0.016, 0.205, 0.779)    # fatal, serious, slight

# 2026 provisional data (the annex asks)
PROV_START = dt.date(2026, 1, 1)
PROV_END = dt.date(2026, 9, 30)
MIGRATION = dt.date(2026, 6, 1)           # the force's new collision system went live
RESEND_SHARE = 0.065                      # pre-migration collisions amended after go-live, re-sent under new references
TRUNK_SHARE = 0.055                       # provisional collisions on trunk roads (national highway authority)
