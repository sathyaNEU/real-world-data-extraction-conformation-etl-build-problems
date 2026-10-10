"""Constants, the payment calendar and the fiction's fixed parameters for the task125 build.

Everything here is a choice the fiction makes (H2's line: parameters, not derived figures). Derived
figures are computed in world.py, screen.py and fernhollow.py and asserted in checks.py.
"""
import datetime as dt
import math

SEED = 125
AS_OF = dt.date(2027, 3, 3)
CALLOFF_DUE = dt.date(2027, 3, 12)
SPINE_FROM = dt.date(2023, 4, 1)
SPINE_TO = dt.date(2027, 2, 25)          # the Thursday 25 February 2027 creditor run
TSP_FROM = dt.date(2021, 7, 1)

# Financial years as (label, start, end) inclusive
FY = {
    "2021/22": (dt.date(2021, 4, 1), dt.date(2022, 3, 31)),
    "2022/23": (dt.date(2022, 4, 1), dt.date(2023, 3, 31)),
    "2023/24": (dt.date(2023, 4, 1), dt.date(2024, 3, 31)),
    "2024/25": (dt.date(2024, 4, 1), dt.date(2025, 3, 31)),
    "2025/26": (dt.date(2025, 4, 1), dt.date(2026, 3, 31)),
    "2026/27": (dt.date(2026, 4, 1), dt.date(2027, 3, 31)),
    "2027/28": (dt.date(2027, 4, 1), dt.date(2028, 3, 31)),
}
SCREEN_YEARS = ["2023/24", "2024/25", "2025/26"]
PLAN = "2027/28"


def fy_of(d):
    y = d.year if d.month >= 4 else d.year - 1
    return "%d/%02d" % (y, (y + 1) % 100)


# England and Wales bank holidays (published gov.uk lists)
BANK_HOLIDAYS = {dt.date.fromisoformat(s) for s in """
2021-01-01 2021-04-02 2021-04-05 2021-05-03 2021-05-31 2021-08-30 2021-12-27 2021-12-28
2022-01-03 2022-04-15 2022-04-18 2022-05-02 2022-06-02 2022-06-03 2022-08-29 2022-09-19 2022-12-26 2022-12-27
2023-01-02 2023-04-07 2023-04-10 2023-05-01 2023-05-08 2023-05-29 2023-08-28 2023-12-25 2023-12-26
2024-01-01 2024-03-29 2024-04-01 2024-05-06 2024-05-27 2024-08-26 2024-12-25 2024-12-26
2025-01-01 2025-04-18 2025-04-21 2025-05-05 2025-05-26 2025-08-25 2025-12-25 2025-12-26
2026-01-01 2026-04-03 2026-04-06 2026-05-04 2026-05-25 2026-08-31 2026-12-25 2026-12-28
2027-01-01 2027-03-26 2027-03-29 2027-05-03 2027-05-31 2027-08-30 2027-12-27 2027-12-28
2028-01-03 2028-04-14 2028-04-17 2028-05-01 2028-05-29 2028-08-28 2028-12-25 2028-12-26
""".split()}


def is_wd(d):
    return d.weekday() < 5 and d not in BANK_HOLIDAYS


def wd_before(d, k=2):
    """The k-th working day before d (the BACS submission date for a payment date d)."""
    while k:
        d -= dt.timedelta(days=1)
        if is_wd(d):
            k -= 1
    return d


def on_or_before_wd(d):
    while not is_wd(d):
        d -= dt.timedelta(days=1)
    return d


def last_wd(y, m):
    d = dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
    return on_or_before_wd(d)


def days(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


def months(a, b):
    """(y, m) pairs from date a's month to date b's month."""
    y, m = a.year, a.month
    while (y, m) <= (b.year, b.month):
        yield (y, m)
        m += 1
        if m == 13:
            y, m = y + 1, 1


def creditor_runs(a, b):
    """Creditor payment runs: Tuesdays and Thursdays that are working days."""
    return [d for d in days(a, b) if d.weekday() in (1, 3) and is_wd(d)]


# Shared Lives four-weekly carer runs: Wednesdays on a 28-day cadence through 31 March 2027
SL_ANCHOR = dt.date(2027, 3, 31)


def sl_runs(a, b):
    out = []
    k = -200
    while True:
        d = SL_ANCHOR + dt.timedelta(days=28 * k)
        if d > b:
            break
        if d >= a:
            out.append(d)
        k += 1
    return out


def dp_date(y, m):
    """Direct payments: the 10th, or the working day before."""
    return on_or_before_wd(dt.date(y, m, 10))


def tsp_date(y, m):
    """Tenancy Sustainment instalments: the 15th, or the working day before."""
    return on_or_before_wd(dt.date(y, m, 15))


def contract_date(y, m, day):
    """Monthly contract payments go on the first creditor run on or after the given day."""
    d = dt.date(y, m, day)
    while not (d.weekday() in (1, 3) and is_wd(d)):
        d += dt.timedelta(days=1)
    return d


# ---------------------------------------------------------------------------------------- Benford
P = {d: math.log10(1 + 1 / d) for d in range(10, 100)}
LO, HI = 1000.00, 999999.99


def cell_of(x):
    """First two digits of an amount of 10 pounds or more."""
    s = str(int(abs(x)))
    return int(s[:2])


# ---------------------------------------------------------------------------------------- Shared Lives
RATES = dict(B1=330, B2=366, B3=412, SDs=395, SDe=452, SDc=515)
RATE_LABEL = dict(B1="Long-term, band 1", B2="Long-term, band 2", B3="Long-term, band 3",
                  SDs="Home First step-down, standard", SDe="Home First step-down, enhanced",
                  SDc="Home First step-down, complex")
COMBOS = [
    (("B1",), 40), (("B2",), 102), (("B3",), 30),
    (("SDs",), 20), (("SDe",), 10), (("SDc",), 6),
    (("B2", "SDs"), 22), (("B2", "SDe"), 20), (("B2", "SDc"), 18),
    (("B1", "SDs"), 12), (("B1", "SDe"), 8), (("B1", "SDc"), 6),
    (("B3", "SDs"), 4), (("B3", "SDe"), 4), (("B3", "SDc"), 3),
    (("B2", "B2", "SDs"), 4),
    (("B1", "B2"), 10), (("B2", "B2"), 8), (("B1", "B1"), 6),
]
SHORT_BREAK_NIGHTLY = [68.50, 74.00, 88.50]
CLOSURE = dt.date(2027, 3, 31)


def carer_amount(combo, when=None):
    keep = combo if (when is None or when <= CLOSURE) else tuple(g for g in combo if not g.startswith("SD"))
    return 4 * sum(RATES[g] for g in keep)


# ---------------------------------------------------------------------------------------- Tenancy Sustainment
TSP_TERM = 30
TSP_2021 = dict(first=(2021, 7), months=12, per_month=24)
TSP_2024 = dict(first=(2024, 7), months=12, per_month=18)

# ---------------------------------------------------------------------------------------- flagged streams
# monthly recurring streams sitting in the 2025/26 flagged cells (department, cell) besides SL and TSP
STREAMS = {
    "ASC_DP14": dict(dept="ASC", n=115, lo=1400.0, hi=1500.0, vat=0.0),
    "HS_FS14": dict(dept="HS", n=14, lo=14000.0, hi=15000.0, vat=0.0, day=18),
    "HT_V49": dict(dept="HT", n=66, lo=4900.0, hi=5000.0, vat=0.20, day=18),
    "HT_S99": dict(dept="HT", n=36, lo=9900.0, hi=10000.0, vat=0.20, day=20),
    "PF_C12": dict(dept="PF", n=83, lo=12000.0, hi=13000.0, vat=0.20, day=16),
}
WE_HAULAGE_END = dt.date(2024, 9, 30)

# ---------------------------------------------------------------------------------------- Fernhollow
BASE_2526, PREM_2526 = 18.40, 27.60
BASE_2627, PREM_2627 = 19.15, 28.70
UNUSED_SHARE = 0.40
MIN_BATCH = 25
ORDER_2526 = 7600
ALLOC_ORIG = 1900
ALLOC_VARIED = 2200
VARIATION_FROM = dt.date(2025, 10, 1)

PEOPLE = {
    "requester": "Tina Rogers",        # head of exchequer services
    "audit": "Julia Burgess",           # head of internal audit
    "hs": "Pauline Pollard",            # Housing Support finance manager
    "analyst": "Wendy Lyons",           # payment assurance analyst
    "s151": "Abigail McDonald",         # director of finance
    "provider": "Douglas Harris",       # Fernhollow account director
    "commissioning": "Adam White",      # ASC commissioning manager
    "fh_service": "Lynda Donnelly",     # Fernhollow service delivery manager
    "sl_manager": "Bethan Carpenter",   # Shared Lives scheme manager
    "procurement": "Shaun Collins",     # category manager, procurement
    "audit_mgr": "Anne McKenzie",       # audit manager
}
