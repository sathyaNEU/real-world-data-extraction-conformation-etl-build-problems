"""Fixed facts of the Bellbird Personal Finance world: calendars, products, pricing, credit policy, behaviour."""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 133
REPORT = dt.date(2026, 9, 30)          # quarter-end reporting date (a Wednesday)
PRIOR_QE = dt.date(2026, 6, 30)        # the June quarter end (a Tuesday)
GO_LIVE = dt.date(2019, 10, 1)         # loan system go-live; first drawdowns October 2019
DEV_OBS_END = dt.date(2026, 5, 31)     # development sample performance window ends (the May 2026 month end)
# development sample: every loan drawn from go-live to the last monthly vintage whose loans had all run their full term,
# defaulted or been repaid by the end of the performance window (asserted: no development loan is still open)
DEV_WINDOW = {"PL36": (GO_LIVE, dt.date(2023, 3, 31)), "PL60": (GO_LIVE, dt.date(2021, 3, 31))}
PRODUCTS = {"PL36": 36, "PL60": 60}
LGD = {"PL36": 0.70, "PL60": 0.76}     # filed in CRM-ECL-04
GRADES = ["A", "B", "C", "D", "E"]
SCENARIOS = [("Base", 0.55, 1.00), ("Downside", 0.30, 1.30), ("Upside", 0.15, 0.80)]
STAGE2_SCALAR = 2.4                    # filed in CRM-ECL-04 3.2
SICR_DROP = 60                         # behaviour score fall (current scorecard points) that triggers stage 2
SCORE_MAP = (1.12, -18.0)              # v3 -> v4: v4 = 1.12 * v3 - 18, rounded
SCORECARD_SWITCH = dt.date(2024, 7, 1)  # applications received on or after this date are scored on v4
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
# borrower state: near the resident population shares, tilted to the home state, varying by channel, with the early
# book heavier in New South Wales before the broker panel went national
STATE_BASE = [0.3384, 0.2563, 0.2117, 0.0912, 0.0634, 0.0143, 0.0178, 0.0069]
STATE_CHANNEL = [(1.00, 0.93, 1.24), (1.06, 1.00, 0.84), (1.04, 0.98, 0.91), (1.11, 0.92, 0.69),
                 (0.92, 1.12, 0.88), (0.79, 1.31, 1.07), (0.86, 1.24, 0.81), (0.97, 1.09, 0.58)]   # Broker, Online, Direct
STATE_HOME_TILT = (0.31, 2.4)          # extra NSW weight in the launch year, and its decay in years
# days from application to funding: same day for some online loans, about a week typically, up to a month
APP_GAP = {"Broker": (0.04, 2.05, 0.62), "Online": (0.27, 1.25, 0.80), "Direct": (0.12, 1.55, 0.70)}   # same day, log mean, log sd
APP_GAP_MAX = 31

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
POST_DEFAULT = (0.012, 0.013, 0.025)
# hardship arrangements: requests per loan-month by period, grade multipliers
HARDSHIP_RATE = [(dt.date(2019, 10, 1), 0.0014), (dt.date(2020, 7, 1), 0.0022), (dt.date(2021, 1, 1), 0.0015),
                 (dt.date(2022, 7, 1), 0.0024), (dt.date(2023, 1, 1), 0.0040), (dt.date(2024, 1, 1), 0.0050),
                 (dt.date(2025, 1, 1), 0.0054), (dt.date(2026, 1, 1), 0.0058)]
HARDSHIP_GRADE = {"A": 0.45, "B": 0.70, "C": 1.0, "D": 1.45, "E": 2.0}
# the 2021 lockdowns in Greater Sydney, Melbourne and Canberra: requests received in each window (borrower state index),
# as a share of the loans open there
LOCKDOWNS_2021 = {0: (dt.date(2021, 7, 5), dt.date(2021, 10, 8), 0.016), 1: (dt.date(2021, 8, 9), dt.date(2021, 10, 22), 0.016),
                  5: (dt.date(2021, 8, 16), dt.date(2021, 10, 15), 0.012)}
# the hardship register: hardship_reason a required field from this date; arrangement_status moved to Completed by a
# weekly batch on Tuesday nights once the end date has passed (Monday 0)
REASON_REQUIRED = dt.date(2020, 7, 1)
REASON_MISSING = 0.08
STATUS_RUN_WEEKDAY = 1
# borrowers whose residential address on file is overseas (no state)
OVERSEAS_ADDRESS = 0.0012
# the service account the quarter-end extract job ECL_QE_BOOK runs under
JOB_ACCOUNT = "svc_crr_batch"
# agreed repayment under a reduced repayment arrangement: a round amount offered, interest only, a share of the
# instalment, a token amount, or an amount from the income and expense statement
REDUCED_MIX = (0.44, 0.24, 0.16, 0.06)
REDUCED_ROUND = [50, 60, 75, 80, 100, 120, 125, 150, 175, 200, 250, 300, 350, 400, 450, 500, 600, 700, 750, 800, 1000]
REDUCED_TOKEN = [10, 20, 20, 25, 30, 40, 50]
# after write-off: a payment plan with the collection agency, a lump-sum settlement, odd payments, or nothing; amounts
# received over two to three years
RECOVERY_MIX = (0.48, 0.15, 0.09)
RECOVERY_PLAN = (0.030, 0.064, 45, 320, 0.052)   # monthly amount: a share of the balance (low, high), but no more than
                                                # the borrower can afford (log-normal, median 320, sd 0.55), floor 45; stop hazard
RECOVERY_SETTLE = (0.38, 0.64)                  # lump sum as a share of the balance
# a settlement agreed with a borrower before write-off: a share of the balance owed, in round fifty dollars
SETTLEMENT_SHARE = (0.40, 0.70)
# how borrowers in collections pay (direct debit, BPAY, card), and how often a direct debit is dishonoured and taken again
PART_PAY_MIX = (0.50, 0.32)
CATCH_UP_MIX = (0.20, 0.45)
DD_DISHONOUR = 0.07
COLLECTION_AGENCY = "Wirraway Mercantile Agents"
# the sale of written-off accounts to a debt buyer in March 2026: accounts written off by the end of August 2025 with
# nothing received in the six months before the cut-off, at their balances at the cut-off, for a price per dollar of face
SALE_REF = "BPF-DS-2026-01"
SALE_BUYER = "Tarwin Receivables Pty Ltd"
SALE_CUTOFF = dt.date(2026, 3, 6)
SALE_SETTLED = dt.date(2026, 3, 27)
SALE_WRITTEN_OFF_BY = dt.date(2025, 8, 31)
SALE_QUIET_DAYS = 183
SALE_PRICE_CENTS = 3.85

# extra repayments settled by tune.py: loan_key -> amount (AUD), paid a few days after the loan's
# September 2026 instalment, so no graded figure sits on a rounding edge
TUNE = {38209: 4151.3, 42844: 5897.56, 70618: 4782.73, 78469: 3760.64, 78929: 5533.42, 80945: 5639.26, 81228: 4855.47}

# PLPD-2026.06 as Credit Risk Modelling released it: from month on book 4 the log of each month's increment is a natural
# cubic spline in month on book with these knots and coefficients (truncated power basis, Hastie and Tibshirani); months
# 1 to 3 are the development sample's own shares, and the final month, which collects the defaults recorded after the
# last repayment date, is not fitted. tune_curve.py fits the coefficients to the sample's monthly default shares
# (weighted by the defaults in each month) subject to the allowance and both stage amounts coming out as they do on the
# sample's unsmoothed shares, read either way in the divisor (closure row 6)
CURVE_FROM = 4
CURVE_KNOTS = {"PL36": [4, 5, 7, 10, 14, 20, 27, 35], "PL60": [4, 5, 7, 10, 14, 20, 28, 40, 59]}
CURVE_FIT = {"PL36": [-6.452902690007774, 0.3259712983836727, -1.3882885785797703, 1.9049587664148009, -0.4308075387717622,
                      -0.10407652747142933, 0.037741028968568624, -0.029706425387825523],
             "PL60": [-7.146364148973196, 0.4673099603949415, -4.047989699945275, 6.188526134187412, -2.434275014066228,
                      0.5203459145460895, -0.33003623312736424, 0.1399717320294233, -0.04470576809844909]}

# the June quarter-end extract was produced by ECL_QE_BOOK before change CHG-26-0418, when the job took days past due
# as at the run (07:30 on 1 July) rather than at close of business on the quarter end
JUNE_ARREARS_AT_RUN = True
# collections hardship arrangements approved on 2023-24 defaults and withdrawn before they started: Collections closes
# a default case as cured when the arrangement is approved, dated from the arrangement's start, and the case is not
# reopened when the arrangement is withdrawn (extracts.withdrawn_arrangements sets how many fall in each product and
# quarter of default)
WITHDRAWN_SEED = SEED + 61


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
