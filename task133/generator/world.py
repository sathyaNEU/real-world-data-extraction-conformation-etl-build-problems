"""Fixed facts of the Bellbird Personal Finance world: calendars, products, pricing, credit policy, behaviour."""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 133
REPORT = dt.date(2026, 9, 30)          # quarter-end reporting date (a Wednesday)
GO_LIVE = dt.date(2019, 10, 1)         # loan system go-live; first drawdowns October 2019
DEV_CUTOFF = dt.date(2023, 10, 1)      # development sample: loans drawn before this date
DEV_OBS_END = dt.date(2026, 6, 30)     # development sample performance window ends
PRODUCTS = {"PL36": 36, "PL60": 60}
LGD = {"PL36": 0.70, "PL60": 0.76}     # filed in CRM-ECL-04
GRADES = ["A", "B", "C", "D", "E"]
SCENARIOS = [("Base", 0.55, 1.00), ("Downside", 0.30, 1.30), ("Upside", 0.15, 0.80)]
STAGE2_SCALAR = 2.4                    # filed in CRM-ECL-04 4.2
SICR_DROP = 60                         # behaviour score fall (current scorecard points) that triggers stage 2
SCORE_MAP = (1.12, -18.0)              # v3 -> v4: v4 = 1.12 * v3 - 18, rounded
SCORECARD_SWITCH = dt.date(2024, 7, 1)
SYD = ZoneInfo("Australia/Sydney")

# application score bands (approve at or above the floor); v4 floors re-set at the same approval rate
BANDS_V3 = [("A", 700), ("B", 655), ("C", 615), ("D", 580), ("E", 545)]
BANDS_V4 = [("A", 766), ("B", 716), ("C", 671), ("D", 632), ("E", 592)]
APP_SCORE = (640.0, 58.0)              # applicant score on the v3 scale
TIGHTENED = (dt.date(2020, 4, 1), dt.date(2020, 9, 30))   # E grade closed to new lending

# establishment fee: a share of the amount by grade, between a floor and a cap, re-set 1 July 2023; added to the
# amount financed unless the borrower pays it at settlement
FEE_PCT = {"A": (0.010, 0.0125), "B": (0.015, 0.0175), "C": (0.020, 0.0225), "D": (0.025, 0.0275), "E": (0.030, 0.0325)}
FEE_FLOOR, FEE_CAP = 95, 995
FEE_UPFRONT = 0.12
FEE_CHANGE = dt.date(2023, 7, 1)

# rate card: grade base at a 0.10 per cent cash rate, PL60 loading, cash-rate pass-through on reprice
RATE_BASE = {"A": 0.0799, "B": 0.1049, "C": 0.1349, "D": 0.1699, "E": 0.2049}
PL60_LOADING = 0.0075
PASS_THROUGH = 0.85
REPRICE_LAG_DAYS = 21
RATE_CAP = 0.2699
CASH_RATE = [(dt.date(2019, 7, 2), 0.0100), (dt.date(2019, 10, 1), 0.0075), (dt.date(2020, 3, 3), 0.0050),
             (dt.date(2020, 3, 19), 0.0025), (dt.date(2020, 11, 3), 0.0010), (dt.date(2022, 5, 3), 0.0035),
             (dt.date(2022, 6, 7), 0.0085), (dt.date(2022, 7, 5), 0.0135), (dt.date(2022, 8, 2), 0.0185),
             (dt.date(2022, 9, 6), 0.0235), (dt.date(2022, 10, 4), 0.0260), (dt.date(2022, 11, 1), 0.0285),
             (dt.date(2022, 12, 6), 0.0310), (dt.date(2023, 2, 7), 0.0335), (dt.date(2023, 3, 7), 0.0360),
             (dt.date(2023, 5, 2), 0.0385), (dt.date(2023, 6, 6), 0.0410), (dt.date(2023, 11, 7), 0.0435),
             (dt.date(2025, 2, 18), 0.0410), (dt.date(2025, 5, 20), 0.0385), (dt.date(2025, 8, 12), 0.0360)]

# origination volume: monthly log-growth by period, one-off shocks, calendar seasonality
VOL_START = 690.0
VOL_GROWTH = [(dt.date(2019, 10, 1), 0.018), (dt.date(2020, 3, 1), 0.004), (dt.date(2021, 1, 1), 0.018),
              (dt.date(2022, 1, 1), 0.011), (dt.date(2023, 1, 1), 0.002), (dt.date(2024, 1, 1), 0.004),
              (dt.date(2025, 1, 1), 0.008), (dt.date(2026, 1, 1), 0.009)]
VOL_SHOCK = {(2020, 3): 0.86, (2020, 4): 0.42, (2020, 5): 0.55, (2020, 6): 0.72, (2020, 7): 0.86, (2020, 8): 0.92,
             (2021, 7): 0.88, (2021, 8): 0.79, (2021, 9): 0.82, (2021, 10): 0.93}
SEASON = {1: 0.95, 2: 1.02, 3: 1.08, 4: 0.93, 5: 1.04, 6: 1.00, 7: 0.97, 8: 1.03, 9: 1.02, 10: 1.05, 11: 1.07, 12: 0.83}
DOW_WEIGHT = [0.92, 1.00, 1.03, 1.07, 1.00]
CHANNEL_MIX = {2019: (0.36, 0.50, 0.14), 2020: (0.37, 0.50, 0.13), 2021: (0.40, 0.47, 0.13), 2022: (0.43, 0.45, 0.12),
               2023: (0.45, 0.43, 0.12), 2024: (0.47, 0.42, 0.11), 2025: (0.49, 0.40, 0.11), 2026: (0.50, 0.39, 0.11)}
CHANNELS = ["Broker", "Online", "Direct"]
STATES = ["NSW", "VIC", "QLD", "WA", "SA", "ACT", "TAS", "NT"]
STATE_P = [0.36, 0.25, 0.20, 0.08, 0.06, 0.02, 0.02, 0.01]

# default onset (first instalment of a run that is never made good) by instalment number, grade C,
# and the grade multipliers; the 90 days past due default follows about three months after the onset
ONSET_LEVEL = {"PL36": 0.00616, "PL60": 0.00701}
ONSET_PEAK = 3.0
ONSET_FLOOR = 0.24
GRADE_MULT = {"A": 0.32, "B": 0.62, "C": 1.0, "D": 1.55, "E": 2.30}
# full payout hazard per month, by grade
PREPAY = 0.0118
PREPAY_GRADE = {"A": 1.30, "B": 1.12, "C": 1.0, "D": 0.88, "E": 0.76}
# instalments paid late or missed and later made good, per instalment, by grade, with calendar seasonality
LATE = {"A": 0.032, "B": 0.048, "C": 0.066, "D": 0.090, "E": 0.122}
LATE_SEASON = {1: 1.35, 2: 1.15, 3: 1.0, 4: 0.97, 5: 0.95, 6: 1.0, 7: 1.08, 8: 0.96, 9: 0.95, 10: 0.95, 11: 1.0, 12: 1.22}
# after default: monthly chance of settling in full, catching up, or a collections hardship arrangement
POST_DEFAULT = (0.014, 0.009, 0.007)
# hardship arrangements: requests per loan-month by period, grade multipliers
HARDSHIP_RATE = [(dt.date(2019, 10, 1), 0.0014), (dt.date(2020, 7, 1), 0.0022), (dt.date(2021, 1, 1), 0.0015),
                 (dt.date(2022, 7, 1), 0.0024), (dt.date(2023, 1, 1), 0.0040), (dt.date(2024, 1, 1), 0.0050),
                 (dt.date(2025, 1, 1), 0.0054), (dt.date(2026, 1, 1), 0.0058)]
HARDSHIP_GRADE = {"A": 0.45, "B": 0.70, "C": 1.0, "D": 1.45, "E": 2.0}

# extra repayments settled by tune.py: loan_key -> amount (AUD), paid a few days after the loan's
# September 2026 instalment, so no graded figure sits on a rounding edge
TUNE = {75277: 1616.36}


def easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    return dt.date(y, (h + l - 7 * m + 114) // 31, (h + l - 7 * m + 114) % 31 + 1)


def nth_monday(y, m, n):
    d = dt.date(y, m, 1)
    d += dt.timedelta(days=(7 - d.weekday()) % 7)
    return d + dt.timedelta(days=7 * (n - 1))


def nsw_holidays(y):
    """NSW public holidays, with the August bank holiday (banks and payment systems closed)"""
    one = dt.timedelta(days=1)
    hs = set()
    nyd = dt.date(y, 1, 1)
    hs.add(nyd)
    if nyd.weekday() == 5:
        hs.add(nyd + 2 * one)
    elif nyd.weekday() == 6:
        hs.add(nyd + one)
    ad = dt.date(y, 1, 26)
    ad += {5: 2 * one, 6: one}.get(ad.weekday(), 0 * one)
    hs.add(ad)
    e = easter(y)
    hs |= {e - 2 * one, e - one, e, e + one}
    hs.add(dt.date(y, 4, 25))
    hs.add(nth_monday(y, 6, 2))
    hs.add(nth_monday(y, 8, 1))
    hs.add(nth_monday(y, 10, 1))
    x, bx = dt.date(y, 12, 25), dt.date(y, 12, 26)
    hs |= {x, bx}
    if x.weekday() == 5:
        hs |= {dt.date(y, 12, 27), dt.date(y, 12, 28)}
    elif x.weekday() == 6:
        hs.add(dt.date(y, 12, 27))
    elif x.weekday() == 4:
        hs.add(dt.date(y, 12, 28))
    if y == 2022:
        hs.add(dt.date(2022, 9, 22))   # National Day of Mourning
    return hs


def cash_rate(d):
    r = CASH_RATE[0][1]
    for when, v in CASH_RATE:
        if when <= d:
            r = v
    return r


def period_value(table, d):
    v = table[0][1]
    for when, x in table:
        if when <= d:
            v = x
    return v


def utc_stamp(local):
    """a Sydney wall-clock datetime as the UTC instant Office stores, e.g. 2026-09-18T06:52:00Z"""
    return local.replace(tzinfo=SYD).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def posix(local):
    return local.replace(tzinfo=SYD).timestamp()
