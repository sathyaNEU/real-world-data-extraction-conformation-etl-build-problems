"""task129 generator: every constant the build uses. Nothing here is shipped as such; the
shipped files are computed from these by the other modules and every graded figure is computed
forward from the files as written."""
from datetime import date, datetime

SEED = 129_2026
TZ = "Europe/Copenhagen"

# ---------------------------------------------------------------- world
ORG = "Sønderå Medier"
PROGRAMME = "Bølge"
TITLES = ["ST", "LA", "KD"]
TITLE_NAME = {"ST": "Sønderå Tidende", "LA": "Lindå Avis", "KD": "Kærby Dagblad"}
TITLE_DOMAIN = {"ST": "www.soenderaa-tidende.dk", "LA": "www.lindaa-avis.dk",
                "KD": "www.kaerby-dagblad.dk"}
TITLE_SHARE = {"ST": 0.41, "LA": 0.33, "KD": 0.26}

# local editions: slug -> (name, masthead before move, masthead after move or None)
EDITIONS = {
    "soenderaa-by": ("Sønderå By", "ST", None),
    "vesterhede": ("Vesterhede", "ST", None),
    "lindaa": ("Lindå", "LA", None),
    "bjerre": ("Bjerre", "LA", "KD"),
    "tolstrup": ("Tolstrup", "LA", "KD"),
    "aaby-strand": ("Åby Strand", "LA", None),
    "kaerby": ("Kærby", "KD", None),
    "nordmarken": ("Nordmarken", "KD", None),
}
EDITION_MOVE = datetime(2026, 3, 16)            # local date the two editions changed masthead

# Bølge template groups in switch-on order (the six waves)
COHORTS = ["sektion", "galleri", "liveblog", "artikel", "sport", "forside"]
COHORT_SWITCH = {"sektion": date(2026, 6, 30), "galleri": date(2026, 7, 7),
                 "liveblog": date(2026, 7, 14), "artikel": date(2026, 7, 21),
                 "sport": date(2026, 7, 28), "forside": date(2026, 8, 4)}
LEGACY = ["arkiv", "tjenester"]
PUZZLE_T = "spil"
TEMPLATES = COHORTS + LEGACY + [PUZZLE_T]
HERO = set(COHORTS) | {"arkiv"}                 # templates that carry a hero image

# ---------------------------------------------------------------- the five changes
CHG = {
    "A": ("CHG-2611", "Header-bidding ad stack (Prebid wrapper)"),
    "B": ("CHG-2547", "Image pipeline (responsive renditions)"),
    "C": ("CHG-2598", "Bølge front end (client-side framework)"),
    "D": ("CHG-2583", "Consent banner (new CMP)"),
    "E": ("CHG-2529", "Brand web fonts"),
}
DATED = {"E": date(2026, 3, 3), "B": date(2026, 4, 7), "D": date(2026, 5, 5)}
SUB_FRONTEND = date(2026, 6, 30)                # ad-free layout: all six groups in one release
PUZZLE_AD_SWITCH = date(2026, 6, 24)

# dated steps in points of over-line share (uniform across groups, states, phones)
STEP = {"E": 0.46, "B": 0.68, "D": 0.72}
from knobs import STEP_T, KEEP_AUG  # noqa: E402  (tuning knobs)
TABLET_STEP_MULT = 0.40
# per-state effects at phone multiplier 1 (points): first load / cached load
EFF_C = {"F": 4.0, "K": 1.0}
EFF_A = {"F": 0.4, "K": 3.4}
PHONE_MULT = {"low": 1.45, "mid": 0.92, "high": 0.55}

# ---------------------------------------------------------------- baselines (points)
BASE_PHONE = {"low": 21.0, "mid": 20.4, "high": 19.8, "tablet": 12.0}
BASE_STATE = {"F": 0.0, "K": 0.0}
BASE_TEMPLATE = {"sektion": 0.0, "galleri": 1.0, "liveblog": 0.5, "artikel": 0.0,
                 "sport": 0.5, "forside": 0.5, "arkiv": -0.5, "tjenester": -1.0, "spil": -1.0}
BASE_TITLE = {"ST": 0.4, "LA": 0.0, "KD": -0.3}
BASE_LOCAL = -4.0
BASE_ADFREE = -1.0
BASE_APP = 3.0

# ---------------------------------------------------------------- time
EXTRACT_START = date(2026, 2, 1)                # local dates, inclusive
EXTRACT_END = date(2026, 8, 31)
SIM_START = date(2026, 1, 12)                   # warm-up so state is defined at extract start
COLLECTOR_V2 = datetime(2026, 6, 3, 0, 0)       # local: new sampling rates
FORWARDER_FIX = datetime(2026, 5, 4, 0, 0)      # local: tablets filtered, single forwarding
TAG_GAP = (date(2026, 4, 23), date(2026, 5, 3))  # LA and KD local-edition pages not firing
DUP_WINDOW = (date(2026, 3, 16), date(2026, 5, 3))  # ST app-webview beacons forwarded twice
DEPLOY_QUIET_MIN = 10
EXTRACT_PULLED = date(2026, 9, 5)
AS_OF = date(2026, 9, 7)
REVIEW = date(2026, 9, 17)

# ---------------------------------------------------------------- sampling
W_V1 = 200
W_V2_ANON = 600
W_V2_SIGNED = 50

# ---------------------------------------------------------------- audiences
# phone mixes (low, mid, high)
MIX = {"base": (0.42, 0.41, 0.17), "sub": (0.30, 0.40, 0.30), "puz": (0.30, 0.42, 0.28)}
# devices simulated (sampled devices only); hashed share present under collector v1
N_DEV = {"anon": 76500, "free": 15500, "sub": 8500, "puz": 3800, "tablet": 6600}
V1_SHARE = {"anon": 1.0, "free": 1 / 4, "sub": 1 / 4, "puz": 1 / 4, "tablet": 1.0}
V2_ANON_KEEP = 3                               # collector v2 keeps every third v1 anonymous device
APP_SHARE_ST = {"anon": 0.06, "free": 0.10, "sub": 0.22}
LOCAL_READER = 0.38                             # share of devices with a local edition

# session behaviour: mean sessions a day (gamma shape), views a session (geometric mean extra)
RATE = {"anon": (2.5, 0.070), "free": (2.5, 0.070), "tablet": (2.5, 0.06),
        "sub": (5.0, 0.72), "puz": (5.0, 0.72)}
EXTRA_VIEWS = {"anon": 0.18, "free": 0.18, "tablet": 0.18, "sub": 0.45, "puz": 0.45}
SUB_SIDE_VIEWS = {"spil": 0.10, "arkiv": 0.035, "tjenester": 0.02}  # per main view, in-session
BF_SHARE = 0.11                                 # of non-landing views restored from bfcache

LAND = {
    "anon": {"artikel": 0.42, "forside": 0.15, "sport": 0.20, "sektion": 0.07, "galleri": 0.045,
             "liveblog": 0.035, "arkiv": 0.06, "tjenester": 0.02},
    "sub": {"artikel": 0.44, "forside": 0.30, "sport": 0.12, "sektion": 0.05, "galleri": 0.03,
            "liveblog": 0.06},
}
BROWSE = {
    "anon": {"artikel": 0.20, "forside": 0.16, "sport": 0.22, "sektion": 0.12, "galleri": 0.09,
             "liveblog": 0.18, "arkiv": 0.02, "tjenester": 0.01},
    "sub": {"artikel": 0.36, "forside": 0.18, "sport": 0.14, "sektion": 0.09, "galleri": 0.06,
            "liveblog": 0.17},
}
SEASON = {2: 1.00, 3: 1.02, 4: 0.99, 5: 0.97, 6: 0.95, 7: 0.90, 8: 1.00, 1: 1.0}
DOW_NEWS = [1.06, 1.04, 1.03, 1.02, 1.00, 0.90, 0.95]
DOW_LOYAL = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

# ---------------------------------------------------------------- deliverable conventions
HEADLINE_BIN = 10_000
WORKBOOK_BIN = 10_000
