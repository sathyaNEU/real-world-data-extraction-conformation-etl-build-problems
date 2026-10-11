"""Fixed facts of the Tarrock Hydro world: dates, the PSU failure law, bands, lots, stock, stores."""
import datetime as dt

SEED = 150
ASOF = dt.date(2026, 9, 30)            # extract date; stock count at close of business
HORIZON_START = dt.date(2026, 10, 1)   # first month the stock has to cover
MIGRATION = dt.date(2021, 1, 1)        # EAM go-live; work-order and rotating-item history start here
REORG = dt.date(2024, 4, 1)            # operating regions reorganised
PM_MASTER_UPDATE = dt.date(2024, 5, 13)  # PM masters re-coded to the new regions and crews in one batch
PROGRAMME_END = dt.date(2035, 12, 1)   # last month of the Protection Renewal Programme
NOTICE_DATE = dt.date(2026, 8, 20)
LTB_CLOSE = dt.date(2026, 12, 15)

# VPR340-PSU-02 failures per module-year. Wear-out is a Weibull hazard in MODULE age (years since the module was
# fitted); on top of it a module fails at random at any age, and a module just placed in service carries an
# early-life excess over its first months (larger for a module back from repair). A failed module is pulled and
# another fitted, which starts again at age zero.
WEIBULL_K = 4.0
WEIBULL_SCALE = 26.0
RANDOM_RATE = 0.0020                   # per module-year, any age
EARLY_NEW = (0.0035, 0.60)             # monthly excess in the first month in service, and its decay per month
EARLY_REPAIRED = (0.0180, 0.65)

# filed in the obsolescence procedure
BANDS = [(0, 9), (10, 14), (15, 19), (20, 24), (25, None)]
BAND_LABELS = ["0-9", "10-14", "15-19", "20-24", "25+"]
LOT = 25
UNIT_PRICE = 1965.00                   # CAD per module, last-time-buy price in the notice
COVER = 0.95
SETTINGS = list(range(8, 23))          # lots shown in the settings table (asked range)

N_RELAY = 1240                          # VPR-340 relays in service on or after the go-live
N_SUBS = 142
N_TS = 27
TS_HOSTS, DS_HOSTS = 24, 94            # stations that carry VPR-340 feeders
DS_FEEDERS_MAX = 12                    # feeder bays a distribution station is built for
STAGE_MIN = 11                          # VPR-340 relays at a station before its scheme is staged
STAGE_LAG = (20, 49)                    # months between stage 1 and stage 2

# storms that brought crews out across a region (the current regions, which follow geography)
STORMS = ((dt.date(2021, 7, 24), ("Central", "South")), (dt.date(2021, 12, 11), ("North", "Central")),
          (dt.date(2022, 5, 21), ("North", "Central", "South")), (dt.date(2022, 12, 23), ("North", "Central")),
          (dt.date(2023, 4, 5), ("Central", "South")), (dt.date(2023, 7, 13), ("North",)),
          (dt.date(2024, 3, 23), ("South",)), (dt.date(2024, 7, 16), ("Central",)),
          (dt.date(2024, 8, 6), ("North", "Central")), (dt.date(2025, 3, 30), ("North", "Central")),
          (dt.date(2025, 6, 18), ("South",)), (dt.date(2026, 6, 9), ("Central", "South")))

# stores: new-in-box and repaired serviceable modules by location, modules awaiting bench test
SERVICEABLE = (("Central Stores (Barrie Road)", "A-14-03", 5), ("North Depot", "N-02-11", 4), ("South Depot", "S-05-07", 3))
QUARANTINE = (("Central Stores (Barrie Road)", "Q-01-02", 4), ("South Depot", "Q-02-01", 3))
# the store that serves a station: by the operating region of the day (Ridge and Valley drew on Central Stores
# until the 2024 reorganisation)
STORES = {"North": "North Depot", "Central": "Central Stores (Barrie Road)", "South": "South Depot"}
LEGACY_STORES = {"Lakeshore": "North Depot", "Ridge": "Central Stores (Barrie Road)",
                 "Valley": "Central Stores (Barrie Road)", "Harbour": "South Depot"}

# Veldtek's RMA register and Tarrock's returns
RMA_START = dt.date(2015, 4, 1)         # Veldtek's register for Tarrock's VPR-340 PSU returns opens with SB-15-02
REG_SAVED = dt.date(2026, 9, 29)        # Veldtek's last save of the register before the count
CUTOVER_HOLD = dt.date(2020, 12, 14)    # stores held shipments over the EAM cutover
SB_LAST_CODE = 1997                     # SB-15-02 covers modules with date codes 91 to 97
MFG_LAG = (20, 270)                     # days from manufacture to installation of a relay, control or RTU
HELD_LAG = (365, 1096)                  # the same for one held in stores for a year or more


def band_of(age):
    for i, (lo, hi) in enumerate(BANDS):
        if age >= lo and (hi is None or age <= hi):
            return i
    raise ValueError(age)


def hazard(age_years):
    """wear-out failures per module-year at an age"""
    k, s = WEIBULL_K, WEIBULL_SCALE
    a = max(age_years, 0.01)
    return (k / s) * (a / s) ** (k - 1)


def p_month(age, k, repaired):
    """chance a module in service on the first of a month fails in it: wear-out at its completed age plus half a
    year, the random rate, and the early-life excess k months after it was placed in service"""
    e0, decay = EARLY_REPAIRED if repaired else EARLY_NEW
    return (hazard(age + 0.5) + RANDOM_RATE) / 12.0 + e0 * decay ** k


def store_for(region, legacy_region, d):
    return STORES[region] if d >= REORG else LEGACY_STORES[legacy_region]


# settled by tune.py: the legacy fitted dates of a few modules that were already replacements at go-live moved by a
# month (index into those modules, months), so no graded figure sits on a rounding edge
TUNE = ()
