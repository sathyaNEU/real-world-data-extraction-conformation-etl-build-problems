"""Fixed facts of the Tarrock Hydro world: dates, the PSU wear-out law, bands, lots, stock."""
import datetime as dt

SEED = 150
ASOF = dt.date(2026, 9, 30)            # extract date; stock count at close of business
HORIZON_START = dt.date(2026, 10, 1)   # first month the stock has to cover
MIGRATION = dt.date(2021, 1, 1)        # EAM go-live; work-order and rotating-item history start here
REORG = dt.date(2024, 4, 1)            # operating regions reorganised
PROGRAMME_END = dt.date(2035, 12, 1)   # last month of the Protection Renewal Programme
NOTICE_DATE = dt.date(2026, 8, 20)
LTB_CLOSE = dt.date(2026, 12, 15)

# VPR340-PSU-02 wear-out: Weibull hazard in MODULE age (years since the module was fitted), failures per
# module-year. A failed module is pulled and a new one fitted, which starts again at age zero.
WEIBULL_K = 4.0
WEIBULL_SCALE = 26.0

# filed in the obsolescence procedure
BANDS = [(0, 9), (10, 14), (15, 19), (20, 24), (25, None)]
BAND_LABELS = ["0-9", "10-14", "15-19", "20-24", "25+"]
LOT = 25
UNIT_PRICE = 1965.00                   # CAD per module, last-time-buy price in the notice
COVER = 0.95
SETTINGS = list(range(8, 23))          # lots shown in the settings table (asked range)

N_RELAY = 1240                          # VPR-340 relays in service on or after the go-live
N_SUBS = 142
N_TS = 17
STAGE_MIN = 11                          # VPR-340 relays at a station before its scheme is staged
STAGE_LAG = (20, 49)                    # months between stage 1 and stage 2

# storms that brought crews out across a region (the current regions, which follow geography)
STORMS = ((dt.date(2021, 7, 24), ("Central", "South")), (dt.date(2021, 12, 11), ("North", "Central")),
          (dt.date(2022, 5, 21), ("North", "Central", "South")), (dt.date(2022, 12, 23), ("North", "Central")),
          (dt.date(2023, 4, 5), ("Central", "South")), (dt.date(2023, 7, 13), ("North",)),
          (dt.date(2024, 3, 23), ("South",)), (dt.date(2024, 7, 16), ("Central",)),
          (dt.date(2024, 8, 6), ("North", "Central")), (dt.date(2025, 3, 30), ("North", "Central")),
          (dt.date(2025, 6, 18), ("South",)), (dt.date(2026, 6, 9), ("Central", "South")))

# stores: new-in-box serviceable modules by location, recovered modules awaiting bench test
SERVICEABLE = (("Central Stores (Barrie Road)", "A-14-03", 5), ("North Depot", "N-02-11", 4), ("South Depot", "S-05-07", 3))
QUARANTINE = (("Central Stores (Barrie Road)", "Q-01-02", 4), ("South Depot", "Q-02-01", 3))


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
TUNE = ((93, -1), (119, 1), (162, -1), (85, -1), (51, 1), (115, 1), (0, 1), (59, -1), (135, -1), (183, -1), (86, 1), (84, -1))
