"""The world's constants: who sits the theory paper, how each paper reads a candidate, and the switch."""
import datetime as dt

SEED = 474_07

ORG = "Heatwise Qualifications"
OLD_VENDOR = "Brindle Assessment"
NEW_VENDOR = "Harrowgate Testing"
QUAL = "Heat Pump Installer Certificate"
PAPER = "HPI3 theory paper"

FIRST_DAY = dt.date(2020, 1, 6)
SWITCH = dt.date(2026, 4, 1)          # Harrowgate's first sitting day
LAST_DAY = dt.date(2026, 9, 30)       # the sittings the Board's mark is set from
EXTRACT = dt.date(2026, 10, 12)       # the register's extract and the vendors' exports
BOARD_MEETING = dt.date(2026, 11, 4)

OLD_PASS = 65                         # the standard, on Brindle's 0 to 100 scale
NEW_ITEMS = 60

# How each paper reads a candidate's proficiency theta (one latent scale). Equal reliability on the two papers, so
# observed-score equating is the same for every group (the equivalence does not move with the group's level).
OLD_A, OLD_B, OLD_ERR = 62.83, 10.0, 4.0
NEW_A, NEW_B, NEW_ERR = 36.0, 6.0, 2.4

RETEST_GAIN = 0.36                    # a second or later sitting reads this much higher, on any paper

# Candidate kinds: mean and spread of theta at the first sitting.
KINDS = {
    "college": (-0.25, 0.85),          # college and apprenticeship leavers
    "changer": (0.05, 0.85),           # career changers from other trades
    "installer": (0.55, 0.75),         # experienced plumbing and heating installers
    "gas": (0.95, 0.60),               # experienced gas engineers retraining (from autumn 2025)
}
# Base mix of first-time candidates by season half: April to September draws more experienced installers (the
# heating trade's slack season); October to March more college leavers.
MIX_SUMMER = {"college": 0.34, "changer": 0.31, "installer": 0.35}
MIX_WINTER = {"college": 0.47, "changer": 0.33, "installer": 0.20}

# The Boiler Upgrade Scheme's expansion: gas engineers' share of first-time candidates, ramping up from September 2025.
GAS_RAMP = [(dt.date(2025, 9, 1), 0.00), (dt.date(2025, 12, 1), 0.06), (dt.date(2026, 3, 1), 0.14),
            (dt.date(2026, 6, 1), 0.34), (dt.date(2026, 9, 30), 0.42)]

FIRST_TIMERS_PER_MONTH = {2020: 520, 2021: 560, 2022: 610, 2023: 660, 2024: 720, 2025: 900, 2026: 1050}
GAS_EXTRA = 0.55                      # the scheme's extra first-time volume, as a share of the base, at full ramp

RESIT_PROB = 0.70                     # a failed candidate resits
NEAR_MISS = (55, 64)                  # from 1 October 2025 a fail in this band carries one free resit
NEAR_MISS_FROM = dt.date(2025, 10, 1)
NEAR_MISS_RESIT_PROB = 0.96
NEAR_MISS_WAIT_DAYS = (14, 45)        # the free resit is booked within six weeks
LOW_WAIT_DAYS = (183, 260)            # from the same date a fail under 55 waits six months to resit, to retrain
RESIT_WAIT_DAYS = (42, 200)           # days from a fail to the resit booking
LAPSE_PROB = 0.14                     # a failed candidate who comes back only after a year or more
LAPSE_WAIT_DAYS = (330, 1100)
ABSENT_RATE = 0.035
VOID_RATE = 0.006
