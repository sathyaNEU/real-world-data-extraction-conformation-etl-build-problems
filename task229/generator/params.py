"""task229 generator: constants. Architecture 3, hydrometry (the Corriston Hydrometric Network)."""
from datetime import date

SEED = 2292027
LST_OFFSET_H = -8                       # local standard time, UTC-8 all year (the standard's day)
TZ = "America/Vancouver"                # local clock time (the operating plan's windows)
AS_OF = date(2026, 11, 6)               # the pack's export date
RECORD_START = date(2022, 10, 1)        # WY2023
RECORD_END = date(2026, 9, 30)          # WY2026
WY_START = date(2025, 10, 1)            # the 2026 water year
WY_END = date(2026, 9, 30)
REVIEWED_TO = date(2026, 6, 30)         # WY2026 review complete through June
MOVE = date(2026, 4, 1)                 # database move: every rating refitted, in force from this day
RELOC_START = date(2026, 6, 4)          # C122 (new site) first day
RELOC_END = date(2026, 6, 8)            # C110 (old site) last day
GAUGING_FROM = 2016
STEP_MIN = 5                            # within-day step for the truth, minutes
YEAR = 2027
OUTLOOK_ISSUED = date(2026, 11, 2)
PLAN_ISSUED = date(2026, 10, 19)
DATA_PLAN_DATE = date(2026, 11, 5)
RATING_BOOK_DATE = date(2026, 4, 1)
STANDARD_DATE = date(2025, 3, 14)
GRADE_B = 0.05
EXTRAP = 1.5
WINDOWS = ((6.0, 10.0), (16.0, 21.0))   # local clock hours
RAMP_H = 0.5
