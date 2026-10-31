"""Hartcombe Mutual's windstorm world: the storms of record, the 2027 year loss table, the 2026 season's claims and the
2027 exposure. Everything a file shows is drawn here once, seeded, and every later module reads it from here.

The process the record carries and no column names: windstorms reach the mutual in trains inside a season, and the
claims of a storm that strikes within weeks of another (roofs still sheeted, builders and roofers still booked) cost
the mutual more per pound of the catastrophe model's loss than a storm on a quiet season."""
import datetime as dt
import math

import numpy as np

SEED = 306
N_YEARS = 10000                 # the vendor's simulated years
FLOOR = 250_000.0               # the vendor's table holds storms costing the mutual this or more
LAM = 1.3                       # trains of storms a year
P_MORE = 0.40                   # chance a train carries one more storm
MED, SIG = 0.8e6, 1.50          # a storm's modelled loss to the 2027 portfolio, lognormal
GAP_IN = (2, 24)                # days between storms in one train
GAP_TRAINS = 70                 # days at least between the last storm of a train and the first of the next
FOLLOW_DAYS = 42                # a storm within this many days of the one before it follows it (the generating rule)
LOAD_LONE, LOAD_FOLLOW = 1.00, 1.60
NOISE = 0.10                    # storm-to-storm scatter of the claims about the loaded model, lognormal sd

ORG = "Hartcombe Mutual Insurance Society Limited"
ORG_SHORT = "Hartcombe Mutual"
VENDOR = "Seaborne Risk"
MODEL = "Seaborne UK Windstorm Model 8.2"
BROKER = "Penwarden Reinsurance Brokers Limited"
PEOPLE = {"reinsurance": "Mandy George", "actuary": "Arthur Begum"}
COUNTIES = ["Cornwall", "Devon", "Somerset", "Dorset"]

# the 2027 programme: the occurrence cover renewed on its 2026 terms, and the second-event cover the broker quoted
BASE = {"name": "Occurrence cover", "limit": 18_000_000.0, "retention": 12_000_000.0, "reinstatements": 1,
        "premium": 2_160_000.0}
SEC = {"name": "Second-event cover", "limit": 7_500_000.0, "retention": 4_000_000.0, "reinstatements": 1,
       "premium": 1_310_000.0}
COC = 0.12                      # the mutual's cost of capital, a year
# the expiring 2026 programme (the occurrence cover on the same terms at its 2026 premium)
EXP = {"limit": 18_000_000.0, "retention": 12_000_000.0, "reinstatements": 1, "premium": 2_100_000.0}
HOURS = 72
RANK_1IN200 = 50                # the 50th largest of the 10,000 simulated years

WINDOWS = [(1, 90), (274, 365)]  # day-of-year windows storms reach the mutual in (January to March, October to December)


def _day_ok(d):
    return any(a <= d <= b for a, b in WINDOWS)


def _year(rng, lam=LAM, before=None):
    """one year's storms as (day of year, modelled loss): trains placed in the windows, storms inside a train
    2 to 24 days apart, trains at least 70 days apart, storms below the vendor's floor never reaching the table"""
    days = []
    for _ in range(int(rng.poisson(lam))):
        n = 1
        while rng.random() < P_MORE and n < 5:
            n += 1
        w = WINDOWS[int(rng.integers(0, 2))]
        start = int(rng.integers(w[0], w[1] + 1))
        train = [start]
        for _ in range(n - 1):
            train.append(train[-1] + int(rng.integers(GAP_IN[0], GAP_IN[1] + 1)))
        train = [d for d in train if _day_ok(d)]
        if not train:
            continue
        # trains keep their distance across the turn of the year too, where the year before is known (the record)
        if any(abs(d - e) < GAP_TRAINS for d in train for e in days + ([before] if before is not None else [])):
            continue
        days.extend(train)
    days.sort()
    out = []
    for d in days:
        # the vendor's table holds the storms that cost the mutual its floor or more; a storm's loss is drawn from the
        # severity above that floor, so no storm drops out of the middle of a train
        loss = float(math.exp(rng.normal(math.log(MED), SIG)))
        while loss < FLOOR:
            loss = float(math.exp(rng.normal(math.log(MED), SIG)))
        out.append((d, loss))
    return out


def follows(days):
    """for each storm in a year's sorted days, whether it strikes within FOLLOW_DAYS of the storm before it"""
    return [i > 0 and days[i] - days[i - 1] <= FOLLOW_DAYS for i in range(len(days))]


def ylt(seed=SEED):
    """the vendor's 2027 year loss table: (year, day, modelled loss), and the generating class of each storm"""
    rng = np.random.default_rng(seed)
    rows = []
    for y in range(1, N_YEARS + 1):
        st = _year(rng)
        fl = follows([d for d, _ in st])
        for (d, l), f in zip(st, fl):
            rows.append((y, d, l, f))
    return rows


# the storms of record: 2001 to 2025, the mutual's exposure growing from about half of 2027's
RECORD_YEARS = list(range(2001, 2026))
RECORD_LAM = 1.45     # the 2001 to 2025 seasons ran stormier than the model's long run


def exposure_index(year):
    """the mutual's portfolio in a year as a share of 2027's (sums insured grew about 2.8 per cent a year)"""
    return 1.028 ** (year - 2027)


RECORD_SEED = 2703     # the record's draw (its shapes are asserted in checks.py)


def record(seed=RECORD_SEED):
    """the storms of 2001 to 2025: (date, the model's hindcast loss to the portfolio of the time, the mutual's
    incurred loss, follows-another)"""
    rng = np.random.default_rng(seed)
    rows = []
    last = None
    for y in RECORD_YEARS:
        # the record is one run of seasons: the last storm of the year before, as a day of this year
        before = None if last is None else (last - dt.date(y, 1, 1)).days + 1
        st = _year(rng, lam=LAM * RECORD_LAM, before=before)
        for d, l in st:
            date = dt.date(y, 1, 1) + dt.timedelta(days=d - 1)
            # the record is one run of seasons, so a storm follows the one before it across the turn of the year too
            f = last is not None and (date - last).days <= FOLLOW_DAYS
            last = date
            hind = l * exposure_index(y)
            load = LOAD_FOLLOW if f else LOAD_LONE
            actual = hind * load * float(math.exp(rng.normal(0.0, NOISE) - NOISE ** 2 / 2))
            rows.append((date, hind, actual, f))
    return rows, seed
