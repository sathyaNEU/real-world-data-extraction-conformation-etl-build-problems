"""Calendar, constants and the round arithmetic shared by the task123 generator modules.

Internal quarter index i runs from the quarter ending 30 June 2017 (i = 0) to the quarter
ending 30 June 2026 (i = 36). The portal extract (the spine) carries i >= 5, the quarter
ending 30 September 2018 onwards.
"""
import calendar
import datetime as dt

SEED = 123

Q0_YEAR, Q0_MONTH = 2017, 6
NQ = 37                      # internal quarters, Jun 2017 .. Jun 2026
SPINE_FIRST = 5              # Sep 2018
LAST_Q = 36                  # Jun 2026

MARCH_CENSUSES = [dt.date(y, 3, 31) for y in range(2021, 2027)]
SEPT_CENSUS = dt.date(2026, 9, 30)
EXTRACT_DATE = dt.date(2026, 10, 7)
FORM_CHANGE_Q = None         # set below: first new-form quarter (Dec 2024)

POTS = {2021: 540000, 2022: 575000, 2023: 610000, 2024: 650000, 2025: 690000, 2026: 720000}
SEPT_POT = 560000
LINE_PCT = 10.0
FLOOR = 15000
CAP = 150000


def qend(i):
    """Date of the last day of internal quarter i."""
    m = Q0_YEAR * 12 + (Q0_MONTH - 1) + 3 * i
    y, mo = divmod(m, 12)
    mo += 1
    return dt.date(y, mo, calendar.monthrange(y, mo)[1])


def qidx(y, m):
    return ((y * 12 + m - 1) - (Q0_YEAR * 12 + Q0_MONTH - 1)) // 3


FORM_CHANGE_Q = qidx(2024, 12)


def fyq(i, bal):
    """Quarter number 1..4 of internal quarter i inside a financial year ending in month bal."""
    m = qend(i).month
    return ((m - bal - 1) % 12) // 3 + 1


def fy_q4(i, bal):
    """Internal index of the fourth quarter of the financial year holding quarter i."""
    return i + (4 - fyq(i, bal))


def fiscal(o, q, labels="returns"):
    """(final quarter, position, length) of the financial year holding quarter q for organisation o.

    labels="returns" follows the organisation's own financial years, the year each return's figures run
    within (a balance-date change gives one year of other than four quarters); labels="app" keys every
    year to one balance date per organisation, the balance date of its latest annual return as held at
    the census (o.bal_app), which is the reading the stop takes."""
    cc = getattr(o, "cal_change", None)
    if labels == "app":
        bal = getattr(o, "bal_app", None) or o.bal
        return fy_q4(q, bal), fyq(q, bal), 4
    if cc:
        old_end, short_end = cc["old_end"], cc["short_end"]
        if q <= old_end:
            return fy_q4(q, cc["old_bal"]), fyq(q, cc["old_bal"]), 4
        if q <= short_end:
            return short_end, q - old_end, short_end - old_end
    return fy_q4(q, o.bal), fyq(q, o.bal), 4


def fpos(o, q, labels="returns"):
    return fiscal(o, q, labels)[1]


def fend(o, q, labels="returns"):
    return fiscal(o, q, labels)[0]


def fstart(o, q, labels="returns"):
    end, pos, n = fiscal(o, q, labels)
    return end - n + 1


def is_final(o, q, labels="returns"):
    return fend(o, q, labels) == q


def census_q(c):
    """Internal index of the quarter that ends on census date c."""
    return qidx(c.year, c.month)


def natural_end(c):
    return census_q(c) - 1


def prev_census(c):
    """The census before census c (rule 2: 31 March each year and, from 2026, 30 September)."""
    if c.month == 9:
        return dt.date(c.year, 3, 31)
    if c.year >= 2027:
        return dt.date(c.year - 1, 9, 30)
    return dt.date(c.year - 1, 3, 31)


def round_half_up_div(num, den):
    """floor(num/den + 1/2) for non-negative integers."""
    return (2 * num + den) // (2 * den)


def offer_for(rate_hc, fall):
    """Offer in whole dollars at a rate in hundredths of a cent per dollar, then floor and cap."""
    raw = round_half_up_div(rate_hc * fall, 10000)
    return min(max(raw, FLOOR), CAP)


def strike_rate(falls, pot, step=1, offer_fn=offer_for):
    """Highest rate (in hundredths of a cent, multiple of step) whose offers fit the pot.

    falls: list of eligible dollar falls (positive integers). Returns (rate_hc, offers, total).
    """
    if not falls:
        return None, [], 0

    def total(r):
        return sum(offer_fn(r, f) for f in falls)

    lo, hi = 0, 10000 // step          # rate up to 100 cents per dollar
    if total(hi * step) <= pot:
        r = hi * step
        offs = [offer_fn(r, f) for f in falls]
        return r, offs, sum(offs)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if total(mid * step) <= pot:
            lo = mid
        else:
            hi = mid
    r = lo * step
    offs = [offer_fn(r, f) for f in falls]
    return r, offs, sum(offs)


def pct1(x):
    """Round half away from zero to one decimal, the way the packs print a fall per cent."""
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def pay_date(year, month):
    """20th of the given month, moved back to the Friday when it falls on a weekend."""
    d = dt.date(year, month, 20)
    if d.weekday() == 5:
        d -= dt.timedelta(days=1)
    elif d.weekday() == 6:
        d -= dt.timedelta(days=2)
    return d


def month_add(y, m, k):
    t = y * 12 + (m - 1) + k
    return t // 12, t % 12 + 1


def quarter_of_date(d):
    """Internal quarter index whose span contains date d."""
    return qidx(d.year, ((d.month - 1) // 3 + 1) * 3)
