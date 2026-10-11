"""Fixed facts of the Tamarack Hydro world: dates, the VPR-340 wear-out law, bands, lots, stock."""
import datetime as dt

SEED = 132
ASOF = dt.date(2026, 9, 30)            # extract date; stock count at close of business
HORIZON_START = dt.date(2026, 10, 1)   # first month the stock has to cover
MIGRATION = dt.date(2021, 1, 1)        # EAM go-live; work-order history starts here
PROGRAMME_END = dt.date(2035, 12, 1)   # last month of the Protection Renewal Programme
NOTICE_DATE = dt.date(2026, 8, 20)
LTB_CLOSE = dt.date(2026, 12, 15)

# VPR-340 power-supply wear-out: Weibull hazard in relay age (years), failures per relay-year
WEIBULL_K = 4.0
WEIBULL_SCALE = 28.0

# filed in the obsolescence procedure
BANDS = [(0, 9), (10, 14), (15, 19), (20, 24), (25, 29), (30, None)]
BAND_LABELS = ["0-9", "10-14", "15-19", "20-24", "25-29", "30+"]
LOT = 25
UNIT_PRICE = 1965.00                   # CAD per module, last-time-buy price in the notice
COVER = 0.95
SETTINGS = list(range(15, 22))         # lots shown in the settings table (asked range)

N_RELAY = 1240                          # VPR-340 relays in the register (in service on or after migration)
N_OTHER = 4010                          # other protection assets in the register
N_SUBS = 142


def band_of(age):
    for i, (lo, hi) in enumerate(BANDS):
        if age >= lo and (hi is None or age <= hi):
            return i
    raise ValueError(age)


def hazard(age_years):
    k, s = WEIBULL_K, WEIBULL_SCALE
    a = max(age_years, 0.01)
    return (k / s) * (a / s) ** (k - 1)

# settled by tune.py: recorded failures moved by a month (index into the post-migration failures, months),
# so no graded figure sits on a rounding edge
TUNE = ((96, 1),)
