"""Calendar, identifiers and rounding shared by the task130 generator modules.

Nothing here is read by the independent verifier (verify.py), which carries its own parsing and
arithmetic so the two code paths share nothing.
"""
import datetime as dt
from decimal import Decimal, ROUND_HALF_UP

SEED = 130
D = dt.date

AS_OF = D(2026, 9, 30)            # deeds and ledger cut
JUNE26 = D(2026, 6, 30)
JUNE25 = D(2025, 6, 30)
JAN27 = D(2027, 1, 1)
JAN26 = D(2026, 1, 1)
FORMAT_CHANGE = D(2026, 4, 1)     # dwelling rows for returns lodged on or after this date
LINE = Decimal("25")
QUARTERS = [D(2024, 9, 30), D(2024, 12, 31), D(2025, 3, 31), D(2025, 6, 30),
            D(2025, 9, 30), D(2025, 12, 31), D(2026, 3, 31), D(2026, 6, 30)]
DEED_FROM = D(2024, 7, 1)
CLOCK = 120                       # the agency's completion interval, never stated in the pack

# Valencian Community public holidays (regional and national) 2024 to 2027, plus local ones the
# three cities share closely enough for scheduling: no deed, commitment or completion falls on them.
HOLIDAYS = {D(2024, 8, 15), D(2024, 10, 9), D(2024, 10, 12), D(2024, 11, 1), D(2024, 12, 6),
            D(2024, 12, 25), D(2025, 1, 1), D(2025, 1, 6), D(2025, 3, 19), D(2025, 4, 18),
            D(2025, 4, 21), D(2025, 5, 1), D(2025, 6, 24), D(2025, 8, 15), D(2025, 10, 9),
            D(2025, 11, 1), D(2025, 12, 6), D(2025, 12, 8), D(2025, 12, 25), D(2026, 1, 1),
            D(2026, 1, 6), D(2026, 3, 19), D(2026, 4, 3), D(2026, 4, 6), D(2026, 5, 1),
            D(2026, 6, 24), D(2026, 8, 15), D(2026, 10, 9), D(2026, 10, 12), D(2026, 12, 8),
            D(2026, 12, 25), D(2027, 1, 1), D(2027, 1, 6), D(2027, 3, 19), D(2027, 3, 29),
            D(2027, 4, 5), D(2027, 5, 1)}


def workday(d):
    return d.weekday() < 5 and d not in HOLIDAYS


def qlabel(q):
    return f"{q.year}T{(q.month - 1) // 3 + 1}"


def qend_of(d):
    m = ((d.month - 1) // 3 + 1) * 3
    nxt = D(d.year + (m == 12), m % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


def add_months(d, n):
    y, m = divmod(d.month - 1 + n, 12)
    y += d.year
    m += 1
    import calendar
    return D(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def add_workdays(d, n):
    while n:
        d += dt.timedelta(days=1)
        if workday(d):
            n -= 1
    return d


def pct(num, den):
    """Share in per cent as an exact Decimal (unrounded)."""
    return Decimal(num) * 100 / Decimal(den)


def r1(x):
    return Decimal(x).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def bin_margin(x):
    """Distance in points from an unrounded per-cent figure to the nearest one-decimal boundary."""
    t = (Decimal(x) * 10) % 1
    return abs(t - Decimal("0.5")) / 10


# ---- cadastral references -------------------------------------------------------------------
_PESOS = [13, 15, 12, 5, 4, 17, 9, 21, 3, 7, 1]
_LLETRES = "MQWERTYUIOPASDFGHJKLBZX"


def _val(c):
    if c.isdigit():
        return int(c)
    if "A" <= c <= "N":
        return ord(c) - 64
    if c == "Ñ":
        return 15
    return ord(c) - 63


def control_letters(ref18):
    out = ""
    for cad in (ref18[0:7] + ref18[14:18], ref18[7:14] + ref18[14:18]):
        s = 0
        for i, ch in enumerate(cad):
            s = (s + _val(ch) * _PESOS[i]) % 23
        out += _LLETRES[s]
    return out


def full_ref(parcel14, unit):
    r18 = f"{parcel14}{unit:04d}"
    return r18 + control_letters(r18)


# ---- tax identifiers ---------------------------------------------------------------------------
_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"


def dni(n8):
    return f"{n8:08d}{_DNI[n8 % 23]}"


def cif(letter, body7):
    digits = f"{body7:07d}"
    even = sum(int(digits[i]) for i in (1, 3, 5))
    odd = 0
    for i in (0, 2, 4, 6):
        v = int(digits[i]) * 2
        odd += v // 10 + v % 10
    c = (10 - (even + odd) % 10) % 10
    if letter in "PQSNW":
        return f"{letter}{digits}{'JABCDEFGHI'[c]}"
    return f"{letter}{digits}{c}"


def ddmmyyyy(d):
    return d.strftime("%d/%m/%Y")
