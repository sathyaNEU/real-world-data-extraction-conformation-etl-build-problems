"""World constants and generation parameters for task118 (Bightline News, the 2027 headline squad).

Every number here is a generation parameter: a choice the fiction makes. Every figure a solver reads
is computed forward from the records these parameters produce, and build_pack.py asserts the results.
"""
import datetime as dt

SEED = 118

# ---------------------------------------------------------------------------------- the setting
AS_OF = dt.date(2026, 10, 19)            # the managing editor's question
EXPORT_DATE = dt.date(2026, 10, 16)      # Natalie Benjamin's export
WINDOW_START = dt.date(2025, 10, 1)      # base year (AEST), the plan's twelve months
WINDOW_END = dt.date(2026, 9, 30)
MIGRATION = dt.date(2025, 10, 1)         # web CMS migration; web testing history begins here
RESTORE_AT = dt.datetime(2025, 11, 14, 7, 40)   # UTC, Brisbane instance restore
RESTORE_LOOKBACK_DAYS = 14
MIGRATION_AT = dt.datetime(2025, 9, 30, 16, 5)   # UTC: 02:05 AEST on 1 October 2025
MIGRATION_LOOKBACK_DAYS = 14
AEST = dt.timedelta(hours=10)
MONTHS = [(2025, m) for m in range(10, 13)] + [(2026, m) for m in range(1, 10)]

ORG = "Bightline News"
ORG_LEGAL = "Bightline News Pty Ltd"

# ---------------------------------------------------------------------------------- desks
# code, name, vertical, edition, distribution, cms instance (web desks only)
DESKS = [
    ("POL-N", "Politics·national", "Politics", "national", "web and app", "national"),
    ("BUS-N", "Business·national", "Business", "national", "web and app", "national"),
    ("SPT-N", "Sport·national", "Sport", "national", "web and app", "national"),
    ("CUL-N", "Culture·national", "Culture", "national", "web and app", "national"),
    ("POL-M", "Politics·metro", "Politics", "Brisbane", "web and app", "brisbane"),
    ("SPT-M", "Sport·metro", "Sport", "Brisbane", "web and app", "brisbane"),
    ("LOC-M", "Local·metro", "Local", "Brisbane", "web and app", "brisbane"),
    ("GAM-A", "Games", "Puzzles & Games", "app", "app only", None),
    ("PZL-A", "Puzzles", "Puzzles & Games", "app", "app only", None),
    ("RCP-A", "Recipes", "Food & Wellbeing", "app", "app only", None),
    ("WEL-A", "Wellness", "Food & Wellbeing", "app", "app only", None),
]
DESK = {d[0]: d for d in DESKS}
SHORTLIST = ["POL-N", "SPT-M", "BUS-N", "SPT-N", "LOC-M", "CUL-N"]      # charter order
WEB = ["POL-N", "BUS-N", "SPT-N", "CUL-N", "POL-M", "SPT-M", "LOC-M"]
APP = ["GAM-A", "PZL-A", "RCP-A", "WEL-A"]
METRO = ["POL-M", "SPT-M", "LOC-M"]
SHORT = {"POL-N": "Pol", "SPT-M": "SpM", "BUS-N": "Bus", "SPT-N": "SpN", "LOC-M": "Loc", "CUL-N": "Cul",
         "POL-M": "PoM"}

# articles first published inside the base year (equal to the live stories and live blogs in the CMS)
N_ARTICLES = {"POL-N": 9007, "BUS-N": 7937, "SPT-N": 11043, "CUL-N": 3883, "POL-M": 3186,
              "SPT-M": 2463, "LOC-M": 6941, "GAM-A": 1128, "PZL-A": 1462, "RCP-A": 1815, "WEL-A": 903}
# older articles that still drew pageviews in the base year, as a share of the in-window count
OLD_ARTICLE_SHARE = {"POL-N": 0.06, "BUS-N": 0.08, "SPT-N": 0.05, "CUL-N": 0.10, "POL-M": 0.05,
                     "SPT-M": 0.04, "LOC-M": 0.05, "GAM-A": 0.0, "PZL-A": 0.0, "RCP-A": 0.12, "WEL-A": 0.10}
OLD_CLICK_SHARE = {"POL-N": 0.010, "BUS-N": 0.016, "SPT-N": 0.008, "CUL-N": 0.022, "POL-M": 0.009,
                   "SPT-M": 0.006, "LOC-M": 0.008, "GAM-A": 0.0, "PZL-A": 0.0, "RCP-A": 0.003, "WEL-A": 0.002}

# ---------------------------------------------------------------------------------- the main ladder targets
# rung-4 figure each desk is tuned to (unrounded clicks); planned clicks are solved from it
F_TARGET = {"POL-N": 552_400, "SPT-M": 100_400, "BUS-N": 697_600, "SPT-N": 648_300, "LOC-M": 808_100,
            "CUL-N": 1_252_300}
P_GUIDE = {"POL-N": 420e6, "SPT-M": 80.4e6, "BUS-N": 300e6, "SPT-N": 350e6, "LOC-M": 110e6, "CUL-N": 150e6,
           "POL-M": 61.3e6, "GAM-A": 41.7e6, "PZL-A": 52.6e6, "RCP-A": 46.2e6, "WEL-A": 27.9e6}
# source-class shares: platform (f), partner apps (q), the rest of the stored-headline surfaces (o = 1-f-q)
F_PLAT = {"POL-N": 0.19, "SPT-M": 0.55, "BUS-N": 0.28, "SPT-N": 0.29, "LOC-M": 0.95, "CUL-N": 0.50,
          "POL-M": 0.60}
Q_PART = {"POL-N": 0.55, "SPT-M": 0.05, "BUS-N": 0.35, "SPT-N": 0.35, "LOC-M": 0.00, "CUL-N": 0.30,
          "POL-M": 0.05}
# share of the desk's platform clicks on articles its own editors tested (t), share of all clicks on
# those articles (a), and the tested articles' partner-app share (q_t)
T_TESTED = {"POL-N": 0.395, "SPT-M": 0.556, "BUS-N": 0.593, "SPT-N": 0.499, "LOC-M": 0.714, "CUL-N": 0.083,
            "POL-M": 0.44}
A_TESTED = {"POL-N": 0.267, "SPT-M": 0.45, "BUS-N": 0.42, "SPT-N": 0.33, "LOC-M": 0.70, "CUL-N": 0.06,
            "POL-M": 0.35}
QT_TESTED = {"POL-N": 0.494, "SPT-M": 0.04, "BUS-N": 0.293, "SPT-N": 0.33, "LOC-M": 0.0, "CUL-N": 0.15,
             "POL-M": 0.04}

SOURCES_PLATFORM = ["home_web", "section_web", "feed_app", "section_app", "related_links"]
SOURCES_STORED = ["search", "discover", "partner_apps", "social", "newsletter", "alerts"]
SOURCES = SOURCES_PLATFORM + SOURCES_STORED
SOURCE_DESC = {
    "home_web": "Bightline web home page (national edition or Brisbane edition)",
    "section_web": "Web section fronts",
    "feed_app": "Bightline app home feed",
    "section_app": "App section tabs",
    "related_links": "Related-story links inside an article, web and app",
    "search": "Organic search results",
    "discover": "Discover-style recommendation cards in mobile browsers",
    "partner_apps": "Partner news apps carrying the Bightline feed",
    "social": "Link cards on social platforms",
    "newsletter": "Bightline email newsletters",
    "alerts": "Push and browser alerts",
}
PLAT_SPLIT = {"national": [0.30, 0.15, 0.30, 0.10, 0.15], "brisbane": [0.25, 0.15, 0.35, 0.10, 0.15],
              "app": [0.0, 0.0, 0.55, 0.35, 0.10]}
OTHER_SPLIT = {  # search, discover, social, newsletter, alerts
    "POL-N": [0.44, 0.21, 0.22, 0.05, 0.08], "BUS-N": [0.52, 0.17, 0.17, 0.08, 0.06],
    "SPT-N": [0.36, 0.26, 0.25, 0.03, 0.10], "CUL-N": [0.48, 0.26, 0.18, 0.06, 0.02],
    "SPT-M": [0.31, 0.21, 0.35, 0.03, 0.10], "LOC-M": [0.38, 0.17, 0.33, 0.07, 0.05],
    "POL-M": [0.38, 0.17, 0.29, 0.06, 0.10]}
AGE_BANDS = ["0-2h", "2-6h", "6-24h", "1-3d", "3-7d", "7d+"]
AGE_START_H = [0, 2, 6, 24, 72, 168]
AGE_PROFILE = {
    "platform": [0.44, 0.27, 0.19, 0.07, 0.025, 0.005],
    "platform_tested": [0.60, 0.21, 0.13, 0.042, 0.015, 0.003],
    "partner_apps": [0.25, 0.30, 0.28, 0.12, 0.04, 0.01],
    "search": [0.10, 0.18, 0.27, 0.25, 0.12, 0.08],
    "discover": [0.15, 0.30, 0.35, 0.15, 0.04, 0.01],
    "social": [0.30, 0.30, 0.25, 0.10, 0.04, 0.01],
    "newsletter": [0.05, 0.20, 0.55, 0.15, 0.04, 0.01],
    "alerts": [0.85, 0.10, 0.04, 0.01, 0.0, 0.0],
    "app": [0.17, 0.25, 0.33, 0.19, 0.056, 0.004],
    "app_tested": [0.31, 0.24, 0.27, 0.13, 0.046, 0.004],
}

# ---------------------------------------------------------------------------------- the test archive
TRUE_MU, TRUE_TAU = -0.010, 0.045         # every headline variant's true relative lift, all desks
GATE = {"national": 1.645, "brisbane": 0.8416, "app": 1.645}  # z a variant must clear to ship
# web desks: tests in the base year, variant-count mix (1..4), clicks per package, control CTR
WEB_TESTS = {
    "POL-N": dict(n=205, kp=[0.80, 0.20, 0.0, 0.0], npk=10000, ctr=0.042, dur=(35, 95)),
    "BUS-N": dict(n=700, kp=[0.0, 0.72, 0.28, 0.0], npk=7400, ctr=0.046, dur=(35, 95)),
    "SPT-N": dict(n=800, kp=[0.68, 0.32, 0.0, 0.0], npk=7600, ctr=0.049, dur=(30, 90)),
    "CUL-N": dict(n=50, kp=[0.0, 0.25, 0.45, 0.30], npk=6200, ctr=0.038, dur=(45, 100)),
    "LOC-M": dict(n=1400, kp=[0.0, 0.10, 0.60, 0.30], npk=4000, ctr=0.052, dur=(25, 80)),
    "SPT-M": dict(n=150, kp=[0.0, 0.0, 0.20, 0.80], npk=120, ctr=0.055, dur=(9, 22)),
    "POL-M": dict(n=210, kp=[0.0, 0.30, 0.70, 0.0], npk=100, ctr=0.048, dur=(7, 16)),
}
# the squad's embeddings: number, year, desk, tests, clicks per package, planned clicks (M), closed
EMBEDDINGS = [
    dict(no=1, year=2019, desk="GAM-A", n=72, npk=2100, planned_m=36.4),
    dict(no=2, year=2020, desk="WEL-A", n=54, npk=1100, planned_m=22.8),
    dict(no=3, year=2021, desk="PZL-A", n=60, npk=4300, planned_m=48.0),
    dict(no=4, year=2022, desk="RCP-A", n=88, npk=3000, planned_m=41.5),
    dict(no=5, year=2023, desk="GAM-A", n=66, npk=450, planned_m=39.2),
    dict(no=6, year=2024, desk="RCP-A", n=60, npk=1000, planned_m=48.0),
    dict(no=7, year=2025, desk="WEL-A", n=58, npk=3800, planned_m=27.6),
]
OPEN_EMBEDDING = dict(year=2026, desk="PZL-A", n=47, npk=4000)
EMB7_IN_WINDOW = 12            # embedding #7 tests that ran on base-year Wellness items (Oct to Dec 2025)
APP_KP = [0.0, 0.30, 0.50, 0.20]
APP_CTR = 0.061
EMBED_SUBSEED = {1: 58, 2: 1, 3: 216, 4: 14, 5: 10, 6: 20, 7: 9}   # chosen by the back-test search
CUL_SUBSEED = 103
REALISED_NOISE = 0.014

# ---------------------------------------------------------------------------------- the ask layer
# a desk's own headline corrections over the base year: total, second corrections on an article
HEADLINE_CORR = {"POL-N": (44, 4), "BUS-N": (36, 2), "SPT-N": (38, 3), "CUL-N": (13, 1), "POL-M": (13, 1),
                 "SPT-M": (16, 1), "LOC-M": (32, 3)}
# headline corrections to live-blog entries (the entry's headline fixed, the note added to the live blog), one
# per live blog, none between QUIET_FROM and QUIET_TO; and entry text corrections made the same way
ENTRY_CORR = {"POL-N": 3, "BUS-N": 3, "SPT-N": 4, "CUL-N": 1, "POL-M": 1, "SPT-M": 2, "LOC-M": 2}
ENTRY_BODY = {"POL-N": 4, "BUS-N": 2, "SPT-N": 6, "CUL-N": 1, "POL-M": 1, "SPT-M": 2, "LOC-M": 3}
QUIET_FROM = (2026, 2, 26)     # AEST: no autosave-ahead headline fix and no entry headline fix in this span
QUIET_TO = (2026, 4, 3)
# scheduling: share of articles saved as scheduled; of those, the share an editor published by hand first
SCHED_SHARE = 0.36
EARLY_SHARE = 0.25
# autosaves of a live document: before a headline correction, (A) the new headline only, (B) headline and note
AUTO_A, AUTO_B = 0.34, 0.20
AUTO_B_QUIET = 0.25
AUTO_BODY, AUTO_UPD, AUTO_UPD_LB = 0.30, 0.22, 0.08
CMS_SUBSEED = {"POL-N": 4, "BUS-N": 0, "SPT-N": 4, "CUL-N": 5, "POL-M": 27, "SPT-M": 10, "LOC-M": 9}
BODY_PER_HEADLINE = 1.55
LIVEBLOG_SHARE = {"POL-N": 0.035, "BUS-N": 0.015, "SPT-N": 0.055, "CUL-N": 0.008, "POL-M": 0.03,
                  "SPT-M": 0.05, "LOC-M": 0.025}
POSTS_PER_LIVEBLOG = {"POL-N": 18, "BUS-N": 28, "SPT-N": 21, "CUL-N": 48, "POL-M": 16, "SPT-M": 13,
                      "LOC-M": 15}
PULLED_SHARE = 0.012
MEDIAN_MIN_GUIDE = {"POL-N": 70, "BUS-N": 95, "SPT-N": 48, "CUL-N": 150, "POL-M": 80, "SPT-M": 37,
                    "LOC-M": 62}
# the note follows the fix: a story's corrected headline published on one live save and its note added on the
# next save (stories), and an entry fixed with the blog's note added minutes later (live blogs); never in the
# quiet span, so the bulletin's March figures read the same either way
LAG_SHARE = {"POL-N": 0.32, "BUS-N": 0.32, "SPT-N": 0.32, "CUL-N": 0.36, "POL-M": 0.30, "SPT-M": 0.34, "LOC-M": 0.32}
LAG_MINUTES = (1, 9)            # the save that publishes the corrected headline to the save that adds its note
ENTRY_LAG = {"POL-N": 2, "BUS-N": 2, "SPT-N": 2, "CUL-N": 1, "POL-M": 1, "SPT-M": 1, "LOC-M": 1}
ENTRY_LAG_MINUTES = (2, 9)      # an entry's fix to the note on its live blog
ENTRY_BODY_LAG = 0.5            # entry text fixes whose note also arrives minutes later
PAIR_GUARD = 60                 # minutes before a note on an unchanged headline in which no other headline change falls
LAG_WINDOW = 10                 # the golden pairing of a note with the headline fix it records, minutes
ENTRY_WINDOW = 30               # the golden pairing of a live blog's note with its entry's fix, minutes
LAG_SUBSEED = {"POL-N": 55, "BUS-N": 57, "SPT-N": 51, "CUL-N": 63, "POL-M": 0, "SPT-M": 50, "LOC-M": 57}   # chosen so every partial reading misses every median

# panel: average monthly unique audience the version of record should carry (people)
PANEL_TARGET = {"POL-N": 3_180_000, "BUS-N": 1_760_000, "SPT-N": 2_930_000, "CUL-N": 1_412_000,
                "POL-M": 331_000, "SPT-M": 470_000, "LOC-M": 616_000, "BLN-HOME": 4_870_000,
                "BLB-HOME": 792_000}
PANEL_REMAINDER = {"POL-N": 260, "BUS-N": 310, "SPT-N": 720, "CUL-N": 240, "POL-M": 180, "SPT-M": 290,
                   "LOC-M": 760, "BLN-HOME": 200, "BLB-HOME": 330}
RESTATED_PERIODS = ["2026-04", "2026-05", "2026-06"]
RESTATE_FACTOR = 1.176          # the duplication fault inflated the original releases by this factor
# the history release: November 2025 to February 2026 rerun on the 2026 content taxonomy, for the national
# sections whose content moved; the other sections were renumbered with their content unchanged and keep the
# figures first published
HISTORY_PERIODS = ["2025-11", "2025-12", "2026-01", "2026-02"]
HISTORY_PUBLISHED = (2026, 4, 24)
HISTORY_SECTIONS = {("BLN", "Politics"), ("BLN", "Culture"), ("BLN", "Home and other")}
# the cross-device duplication fault was in the Brisbane edition site's processing; only its rows are restated
RESTATED_SITES = {"BLB"}
# a section's audience on the 2024 content taxonomy against the 2026 one (content moved between three national
# sections in 2026; the rest were renumbered only)
OLD_BASIS = {("BLN", "Home and other"): 1.052, ("BLN", "Politics"): 0.957, ("BLN", "Sport"): 1.0,
             ("BLN", "Culture"): 0.968, ("BLN", "Business"): 1.0, ("BLB", "Home and other"): 1.0,
             ("BLB", "Politics"): 1.0, ("BLB", "Local"): 1.0, ("BLB", "Sport"): 1.0}
