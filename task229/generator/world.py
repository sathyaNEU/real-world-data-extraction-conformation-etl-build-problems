"""task229 world: Halvane Metering, a metering data provider in the NEM (New South Wales).

Every constant the generator uses lives here. Times are kept in three clocks, as the real systems do:
market time (AEST, UTC+10, no daylight saving), local field time (AEDT, UTC+11, daylight saving began
on 4 October 2026) and UTC (the head-end and the MDM receipt stamps).
"""
import datetime as dt

SEED = 229

UTC = dt.timezone.utc
AEST = dt.timezone(dt.timedelta(hours=10), "AEST")
AEDT = dt.timezone(dt.timedelta(hours=11), "AEDT")

# the assessment week, market days Monday 5 to Sunday 11 October 2026 (AEST)
WEEK_START = dt.datetime(2026, 10, 5, 0, 0, tzinfo=AEST)
DAYS = 7
SLOT = 5                                  # minutes, the finest interval any meter records
SLOTS_PER_DAY = 1440 // SLOT
WEEK_SLOTS = DAYS * SLOTS_PER_DAY
READ_DATES = [(WEEK_START + dt.timedelta(days=d)).date() for d in range(DAYS)]

# the MDM extract was pulled on Monday 12 October at 15:40 AEDT (14:40 AEST)
EXTRACT_AT = dt.datetime(2026, 10, 12, 15, 40, tzinfo=AEDT)
CUTOFF_HOUR_AEST = 6                      # 06:00 market time on the day after the read date
REFERENCE = 99.50                         # read-health reference, per cent
K_SE = 3

# head-end image ids, release names as the rollout desk writes them, module family, channel
BUILDS = [
    # release      image                    module  channel      released
    ("EM3.10.9", "em3-fw-031009-b2207", "EM3", "retiring", "2024-08-19"),
    ("EM3.11.4", "em3-fw-031104-b2391", "EM3", "GA", "2025-03-03"),
    ("EM3.12.0", "em3-fw-031200-b2468", "EM3", "GA", "2025-11-17"),
    ("EM3.12.1", "em3-fw-031201-b2479", "EM3", "hotfix", "2026-02-09"),
    ("EM3.12.2", "em3-fw-031202-b2531", "EM3", "GA", "2026-08-24"),
    ("PX5.2.7", "px5-fw-050207-r0714", "PX5", "GA", "2025-06-30"),
    ("PX5.3.0", "px5-fw-050300-r0802", "PX5", "GA", "2026-01-12"),
    ("PX5.3.1", "px5-fw-050301-r0839", "PX5", "pilot", "2026-08-31"),
]
RELEASES = [b[0] for b in BUILDS]
IMAGE = {b[0]: b[1] for b in BUILDS}
MODULE = {b[0]: b[2] for b in BUILDS}
# images that are history only (commissioning images and superseded builds)
OLD_IMAGES = {
    "EM3": [("EM3.9.6", "em3-fw-030906-b1874"), ("EM3.10.2", "em3-fw-031002-b2011")],
    "PX5": [("PX5.1.9", "px5-fw-050109-r0455"), ("PX5.2.3", "px5-fw-050203-r0610")],
}

# installation profiles: data streams (NMI suffixes), interval length in minutes, customer class
PROFILES = {
    "R30A": (["E1"], 30, "RES"),                 # household, general supply only
    "R30B": (["E1", "E2"], 30, "RES"),           # household with a controlled-load element
    "R30C": (["E1", "B1"], 30, "RES"),           # household with rooftop solar
    "R5B": (["E1", "B1"], 5, "RES"),             # newer 5-minute household with solar
    "R5C": (["E1", "E2", "B1"], 5, "RES"),       # 5-minute household, solar and controlled load
    "S15": (["E1", "Q1", "B1"], 15, "SME"),      # small business, 15-minute, reactive channel
    "S5": (["E1", "Q1", "B1"], 5, "SME"),        # small business on 5-minute
}
HEAVY = {"R5B", "R5C", "S15", "S5"}

# per-build population of installations that run the build all week, by profile
FULL_WEEK = {
    "EM3.10.9": {"R30A": 300, "R30B": 82, "R30C": 41},
    "EM3.11.4": {"R30A": 905, "R30B": 386, "R30C": 291, "R5B": 61, "R5C": 19},
    "EM3.12.0": {"R30A": 1006, "R30B": 433, "R30C": 452, "R5B": 247, "R5C": 104},
    "EM3.12.1": {"R30A": 388, "R30B": 129, "R30C": 25, "R5B": 61, "R5C": 92},
    "EM3.12.2": {"R30A": 69, "R30B": 31, "R30C": 34, "R5B": 12, "R5C": 7},
    "PX5.2.7": {"R30A": 246, "R30B": 118, "R30C": 132, "S15": 106, "S5": 95, "R5B": 31},
    "PX5.3.0": {"R30A": 566, "R30B": 61, "R30C": 38, "R5C": 41, "S5": 72, "S15": 11},
    "PX5.3.1": {"R30A": 21, "R30B": 6, "R30C": 7, "R5C": 3},
}

# Wave 7 (this week): (from release, to release, profile mix, local night)
WAVE7 = [
    ("EM3.12.0", "EM3.12.2", {"R30A": 352, "R30B": 148, "R30C": 163, "R5B": 71, "R5C": 31}, "tue"),
    ("EM3.11.4", "EM3.12.2", {"R30A": 189, "R30B": 82, "R30C": 64, "R5B": 9}, "wed"),
    ("PX5.3.0", "PX5.3.1", {"R30A": 31, "R30B": 12, "R30C": 14, "S5": 6}, "wed"),
]
WAVE7_ROLLBACK_RETRY = 41          # of the Tuesday EM3.12.0 movers: failed Tuesday, rolled back, moved Wednesday
EXCHANGES = 29                     # installations whose meter was swapped mid-week (EM3.12.0 / EM3.11.4 meters)

# Wave 8 (next week) as the rollout desk cut the schedule on Thursday 1 October: every meter then on a
# source image behind the Wave 8 collectors and access points
WAVE8_EM_FULL = {"EM3.12.0": 872, "EM3.11.4": 402}   # full-week installations behind the Wave 8 collectors
WAVE8_PX_FULL = {"PX5.3.0": 109}
WAVE8_EXCHANGED = 22               # exchanged installations behind Wave 8 collectors (old meter on the sheet)
WAVE8_PULLED_FORWARD = 37          # meters behind a Wave 8 collector that went in Wave 7 instead
WAVE8_REBATCHED = 16               # meters listed on both batch sheets after the depot re-batch
WAVE8_PX_PULLED_FORWARD = 9
WAVE8_PX_REBATCHED = 5

# the two RF mesh networks: EM3 modules report through collectors, PX5 modules through access points.
# Firmware waves go out collector by collector (the head-end pushes an image through the collector).
EM_COLLECTORS = {"pilot": 7, "w7": 12, "w8": 13, "old": 11, "new": 13}
PX_APS = {"pilot": 3, "w7": 2, "w8": 3, "other": 8}
# a night on which a collector's backhaul or power fails and its meters' day is not collected before
# the delivery cut-off: probability per collector per read date, share of its meters caught
EVENT_P = {"EM3": 0.009, "PX5": 0.005}
EVENT_SHARE = (0.62, 0.96)
NET_SALT = 34

COMPANY = "Halvane Metering"
PEOPLE = {"lead": "Troy Phillips"}

# per-build texture salts and the network salt, chosen by tune.py so every graded figure sits clear of
# its rounding edge and every build clear of its limit
SALT = {"EM3.10.9": 3, "EM3.11.4": 3, "EM3.12.0": 9, "EM3.12.1": 10, "EM3.12.2": 7, "PX5.2.7": 10, "PX5.3.0": 5, "PX5.3.1": 12}
