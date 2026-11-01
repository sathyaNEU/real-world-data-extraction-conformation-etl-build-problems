"""Fixed parameters of the Kaitanga bore field world (task273, architecture 6).

Every number the world is simulated from sits here; nothing below is tuned to an answer by hand. The plan's
monthly takes are the one place the generator nudges values, and only inside the operations' own 0.05 ML/d
planning step (world.plan_takes), so that each graded level sits inside its reporting bin."""

SEED = 273_06

START = "2014-01-01"            # the daily telemetry record begins
END = "2026-10-31"              # the extract date: the record ends here
EXTRACT_DATE = "2026-11-02"     # files written on this date (in-fiction export date)

# Production bores: id, local easting and northing (m from PB1's headworks), ground level (m RL, Moturiki
# datum), measuring-point stick-up (m), own drawdown per ML/d (m), natural-head offset from the council
# monitoring bore (m), share of the plant's draw, pump capacity (ML/d), rated motor kW.
BORES = [
    # id    x      y     ground  stick  own   offset  share  cap   kW
    ("PB1",   0,     0,  54.62,  0.42, 1.38,  1.31,  0.142, 4.2,  55),
    ("PB2",  384,  212,  54.10,  0.55, 1.91,  1.12,  0.118, 3.6,  45),
    ("PB3",  826,  331,  53.47,  0.38, 2.27,  0.88,  0.131, 4.0,  55),
    ("PB4", 1181,  566,  56.45,  0.61, 1.64,  0.66,  0.127, 3.9,  55),
    ("PB5", 1652,  648,  52.88,  0.47, 1.47,  0.41,  0.124, 3.8,  45),
    ("PB6", 1994,  903,  52.31,  0.35, 2.05,  0.19,  0.108, 3.3,  37),
    ("PB7", 2407, 1012,  51.76,  0.50, 1.72, -0.07,  0.125, 3.8,  45),
    ("PB8", 2853, 1238,  51.20,  0.44, 1.56, -0.33,  0.125, 3.8,  55),
]
# The new bore, drilled in 2026 between PB3 and PB4 and test-pumped in October 2026.
PB9 = ("PB9", 1012, 598, 53.71, 0.52, 1.58, 0.74, 0.0, 5.2, 75)

# Pump intake depth below measuring point (m) and the minimum operating level (intake less 2.5 m of cover).
# Each pump's cover above its intake follows its maker's submergence figure, so the margin differs by pump.
COVER_M = {"PB1": 2.5, "PB2": 3.0, "PB3": 2.0, "PB4": 2.5, "PB5": 3.0, "PB6": 2.0, "PB7": 2.5, "PB8": 3.5, "PB9": 3.0}
MOL_MBMP = {"PB1": 31.6, "PB2": 33.2, "PB3": 35.0, "PB4": 36.1, "PB5": 32.6, "PB6": 31.9, "PB7": 31.2, "PB8": 29.6,
            "PB9": 38.0}
INTAKE_MBMP = {k: round(v + COVER_M[k], 1) for k, v in MOL_MBMP.items()}

# Interference between existing bores: a Thiem-like k * ln(R / r), with a per-pair departure (the gravels are
# not uniform), symmetric by reciprocity.
INTERF_K = 0.158
INTERF_R = 3150.0
PAIR_SPREAD = 0.09

# The new bore's real connection: PB9 is screened in the same buried channel as PB3 and sits behind a clay lens
# from PB4, so its drawdown on those two departs from what distance alone gives.
PB9_PAIR = {"PB3": 0.664, "PB4": 0.108}

# Council monitoring bore (unpumped), daily level in m RL on NZVD2016.
MB_MEAN = 33.85
MB_SEASON_AMP = 2.05
MB_DATUM_OFFSET = 0.27          # Moturiki 1953 = NZVD2016 + 0.27 m at this site

# The graded lowest levels are reported to the nearest half metre; the plan's 0.05 ML/d steps are nudged so each
# sits at least 0.15 m inside its half-metre bin.
GRADE_STEP = 0.5
BIN_FLOOR = 0.15

# Measurement noise on a daily mean pumping water level (m).
LEVEL_NOISE = 0.035

# The design drought: the council monitoring bore's 2019-20 summer, December to March.
DROUGHT_YEAR = 2019
PLAN_MONTHS = [(2026, 12), (2027, 1), (2027, 2), (2027, 3)]
SUMMER_MONTHS = [12, 1, 2, 3]

# Commissioning test of PB9 (local NZDT, UTC+13): step test on 6 October, constant rate 7 to 14 October.
TEST_STEP_DAY = "2026-10-06"
TEST_CR_START = "2026-10-07 09:00"
TEST_CR_END = "2026-10-14 09:00"
TEST_STEPS_LS = [24.0, 38.0, 53.0]
TEST_CR_LS = 51.0
