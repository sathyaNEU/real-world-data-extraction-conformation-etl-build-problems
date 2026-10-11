"""task180 world: Corran Energy revenue protection, north of Scotland.

Every constant the pack is built from lives here. Nothing in the shipped bundle states a figure
that is not derived from these by sim.py and the writers.
"""
import datetime as dt

SEED = 180_2026

# Calendar ---------------------------------------------------------------------------------
EXTRACT_DATE = dt.date(2026, 12, 7)          # Monday; last midnight read closes Sunday 6 Dec
READS_START = dt.date(2024, 10, 1)           # first daily register read in the parquet
MART_START = dt.date(2023, 12, 4)            # first ISO week (Monday) in the analytics mart
HDD_START = dt.date(2023, 12, 1)
ASSESS_START = dt.date(2026, 10, 12)         # eight complete weeks, Mon 12 Oct to Sun 6 Dec
ASSESS_WEEKS = 8
BASELINE_WEEKS = 104                         # Mon 14 Oct 2024 to Sun 11 Oct 2026
BASELINE_START = ASSESS_START - dt.timedelta(weeks=BASELINE_WEEKS)
HDD_BASE_C = 15.5

# Referral standard (filed in RP-07) ---------------------------------------------------------
REFERRAL_SHORTFALL = 0.30

# Patches -----------------------------------------------------------------------------------
# station: the Met Office site the patch's degree days come from (Inverness and Nairn share one)
# n: premises on supply; heat: share of premises holding a second, heating-only supply number
# whole: premises whose (single) supply is bypassed; heatdiv: heating-only supplies bypassed
# voids: premises with a change of occupier inside the windows and empty through the assessment weeks
# retrofit: heat pumps fitted under the warm homes scheme in summer 2026 (storage heating retired)
# sens: kWh per degree day on the main supply (direct electric heating share)
PATCHES = [
    # code, name,                 station,            n,   heat, whole, heatdiv, voids, retrofit, prepay, sens, base
    ("INV", "Inverness City",     "Inverness Airport", 640, 0.03, 19, 0,  72, 0,  0.16, 0.10, 8.2),
    ("NRN", "Nairn and Ardersier","Inverness Airport", 270, 0.10, 14, 0,   6, 0,  0.12, 0.14, 8.6),
    ("FRS", "Forres",             "Kinloss",          260, 0.12, 11, 0,   5, 0,  0.11, 0.14, 8.4),
    ("ELG", "Elgin and Lossiemouth","Lossiemouth",    460, 0.06, 35, 0,   7, 0,  0.13, 0.12, 8.5),
    ("SPY", "Strathspey",         "Aviemore",         340, 0.48, 10, 6,   4, 54, 0.08, 0.20, 8.9),
    ("LOC", "Lochaber",           "Tulloch Bridge",   290, 0.30,  8, 0,   4, 0,  0.10, 0.22, 8.8),
    ("CAI", "Caithness",          "Wick Airport",     400, 0.56, 12, 42,  5, 0,  0.12, 0.22, 9.1),
    ("SKY", "Skye and Lochalsh",  "Lusa",             300, 0.40, 13, 4,   4, 0,  0.09, 0.26, 9.0),
]
PATCH_COLS = ["code", "name", "station", "n", "heat", "whole", "heatdiv", "voids", "retrofit",
              "prepay", "sens", "base"]

STATIONS = {
    # name: (mean annual temp C, seasonal amplitude C, autumn-2025 anomaly C, autumn-2026 anomaly C)
    "Inverness Airport": (8.9, 5.6, -0.6, 0.4),
    "Kinloss":           (9.0, 5.5, -0.5, 0.4),
    "Lossiemouth":       (9.1, 5.3, -0.5, 0.5),
    "Aviemore":          (7.2, 6.4, -0.9, 0.3),
    "Tulloch Bridge":    (7.4, 5.8, -0.7, 0.6),
    "Wick Airport":      (8.0, 4.9, -0.4, -0.6),
    "Lusa":              (9.0, 4.6, -1.4, 1.1),
}

# Consumption model ---------------------------------------------------------------------------
HEAT_SENS = (0.42, 0.62)       # kWh per degree day on a heating-only supply (uniform range)
DAILY_NOISE_MAIN = 0.11
DAILY_NOISE_HEAT = 0.09
LEGIT_DRIFT = (0.88, 1.12)     # level of the assessment weeks against the baseline, ordinary households
WHOLE_DIV_F = (0.42, 0.60)     # share of a bypassed single supply's consumption not recorded
HEAT_DIV_F = (0.40, 0.58)      # share of a bypassed heating supply's consumption not recorded
DIV_ONSET = (dt.date(2026, 9, 1), dt.date(2026, 10, 2))
VOID_FACTOR = (0.10, 0.24)
HP_COP = 2.8
RETROFIT_WINDOW = (dt.date(2026, 6, 15), dt.date(2026, 9, 18))
