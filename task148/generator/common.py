"""task148 constants and helpers shared by every generator module.

Fenmore Savings Bank (holding company Fenmore Financial Corporation), a savings bank whose fiscal year ends on
30 September, runs a national SBA 7(a) lending division under the Preferred Lenders Program from October 2009. It
sells the guaranteed portions, keeps the unguaranteed portions and services every loan. The controller books the
year-end allowance on the relief-era pool (loans approved in SBA fiscal years 2019 to 2021) at 30 September 2026."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 1482026

BANK = "Fenmore Savings Bank"
HOLDCO = "Fenmore Financial Corporation"
DIVISION = "SBA Lending"

PEOPLE = {
    "controller": "Erin Spence",        # books the allowance (not in the prompt)
    "cco": "Richard Fields",            # chief credit officer, SBA Lending; owns the allowance policy
    "servicing": "Johnny Nicholson",    # SBA servicing manager; the servicing extracts
    "special": "Donna Graves",          # special assets; workouts, charge-offs and recoveries
    "loanops": "Tara Williams",         # loan operations; SBA reporting, FTA and SBA cash
}

# ---------------------------------------------------------------------------------------------------- calendar
# month index 0 is October 2009, the division's first month; 203 is September 2026, the reserve month.
T_END = 203
H = T_END + 1
RESERVE_DATE = dt.date(2026, 9, 30)
POOL_FY = (2019, 2021)


def ym(m):
    """(year, month) of month index m."""
    y, mo = divmod(2009 * 12 + 9 + m, 12)
    return y, mo + 1


def m_of(d):
    return (d.year * 12 + d.month - 1) - (2009 * 12 + 9)


def month_end(m):
    y, mo = ym(m)
    nxt = dt.date(y + (mo == 12), mo % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


def month_first(m):
    y, mo = ym(m)
    return dt.date(y, mo, 1)


def fy_of_month(m):
    """Fiscal year (1 October to 30 September) of month index m: October 2009 is FY2010."""
    return 2010 + np.asarray(m) // 12 if isinstance(m, np.ndarray) else 2010 + m // 12


def fy_of_date(d):
    return d.year + 1 if d.month >= 10 else d.year


def fq_label(m):
    """'FY2021 Q1' style fiscal quarter of month index m."""
    fy = fy_of_month(m)
    q = (m % 12) // 3 + 1
    return "FY%d Q%d" % (fy, q)


# ---------------------------------------------------------------------------------------------------- prime rate
# the prime rate the servicing system applies at each variable-rate loan's quarterly reset (changes by effective date)
PRIME = [
    (dt.date(2008, 12, 16), 3.25), (dt.date(2015, 12, 17), 3.50), (dt.date(2016, 12, 15), 3.75),
    (dt.date(2017, 3, 16), 4.00), (dt.date(2017, 6, 15), 4.25), (dt.date(2017, 12, 14), 4.50),
    (dt.date(2018, 3, 22), 4.75), (dt.date(2018, 6, 14), 5.00), (dt.date(2018, 9, 27), 5.25),
    (dt.date(2018, 12, 20), 5.50), (dt.date(2019, 8, 1), 5.25), (dt.date(2019, 9, 19), 5.00),
    (dt.date(2019, 10, 31), 4.75), (dt.date(2020, 3, 4), 4.25), (dt.date(2020, 3, 16), 3.25),
    (dt.date(2022, 3, 17), 3.50), (dt.date(2022, 5, 5), 4.00), (dt.date(2022, 6, 16), 4.75),
    (dt.date(2022, 7, 28), 5.50), (dt.date(2022, 9, 22), 6.25), (dt.date(2022, 11, 3), 7.00),
    (dt.date(2022, 12, 15), 7.50), (dt.date(2023, 2, 2), 7.75), (dt.date(2023, 3, 23), 8.00),
    (dt.date(2023, 5, 4), 8.25), (dt.date(2023, 7, 27), 8.50), (dt.date(2024, 9, 19), 8.00),
    (dt.date(2024, 11, 8), 7.75), (dt.date(2024, 12, 19), 7.50), (dt.date(2025, 9, 18), 7.25),
    (dt.date(2025, 10, 30), 7.00), (dt.date(2025, 12, 11), 6.75),
]


def prime_on(d):
    v = PRIME[0][1]
    for when, rate in PRIME:
        if when <= d:
            v = rate
        else:
            break
    return v


# ---------------------------------------------------------------------------------------------------- helpers
def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def write_csv(path, cols, rows, crlf=False, delimiter=","):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n", delimiter=delimiter)
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(["" if r.get(c) is None else r.get(c) for c in cols] if isinstance(r, dict) else r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return n


def round_to(x, step):
    """Round half away from zero to a multiple of step (the deliverables' convention)."""
    q = x / step
    return int(math.floor(q + 0.5)) * step if q >= 0 else -int(math.floor(-q + 0.5)) * step


def bin_clearance(x, step):
    """Distance from x to the nearest rounding edge of its step-wide bin, as a share of the step (0.5 is mid-bin)."""
    q = x / step
    return 0.5 - abs(q - math.floor(q + 0.5))
