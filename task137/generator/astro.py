"""Sunrise and sunset at each depot, Greenwich Mean Time, by seven-day calendar row (the driver handbook's Appendix C).

The world's darkness is defined by this table: a kilometre is driven in darkness when its time (UTC, which is GMT) falls
before the row's sunrise or after the row's sunset at the run's depot. Rows run from 1-7 January in seven-day blocks of a
common (non-leap) year by month and day; 29 February belongs to the row that holds 28 February.
"""
import datetime as dt
import math

import params as P


def _sun(doy, lat, lon):
    """NOAA approximation: sunrise and sunset in GMT hours for day of year doy (solar altitude -0.833 degrees)."""
    g = 2 * math.pi / 365 * (doy - 1)
    eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g) - 0.014615 * math.cos(2 * g)
                    - 0.040849 * math.sin(2 * g))
    decl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
            + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    latr = math.radians(lat)
    cosh = math.cos(math.radians(90.833)) / (math.cos(latr) * math.cos(decl)) - math.tan(latr) * math.tan(decl)
    ha = math.degrees(math.acos(max(-1.0, min(1.0, cosh))))
    return (720 - 4 * (lon + ha) - eqt) / 60.0, (720 - 4 * (lon - ha) - eqt) / 60.0


REF_YEAR = 2027          # a common year: the rows are month-day ranges


def rows():
    """[(row index, first date, last date)] in REF_YEAR: 52 rows of seven days and a last row for 31 December."""
    out, d0 = [], dt.date(REF_YEAR, 1, 1)
    for k in range(53):
        a = d0 + dt.timedelta(days=7 * k)
        b = min(a + dt.timedelta(days=6), dt.date(REF_YEAR, 12, 31))
        if a.year != REF_YEAR:
            break
        out.append((k, a, b))
    return out


ROWS = rows()


def row_of(d):
    """The table row a calendar date belongs to (by month and day; 29 February goes with 28 February)."""
    md = (d.month, d.day) if not (d.month == 2 and d.day == 29) else (2, 28)
    ref = dt.date(REF_YEAR, *md)
    return min((ref - dt.date(REF_YEAR, 1, 1)).days // 7, len(ROWS) - 1)


def hm(x):
    """hours to minutes, rounded to the whole minute"""
    return int(round(x * 60))


def table():
    """{(depot code, row): (sunrise minute GMT, sunset minute GMT)} for each depot, from the row's middle day."""
    T = {}
    for code, _, _, _, lat, lon, _ in P.DEPOTS:
        for k, a, b in ROWS:
            mid = a + (b - a) // 2
            doy = (mid - dt.date(REF_YEAR, 1, 1)).days + 1
            r, s = _sun(doy, lat, lon)
            T[(code, k)] = (hm(r), hm(s))
    return T


TABLE = table()


def last_sunday(y, m):
    d = dt.date(y, m, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def bst_offset(d):
    """1 on days when British Summer Time is in force at 12:00, else 0 (clocks change at 01:00 GMT on the last
    Sundays of March and October)."""
    return 1 if last_sunday(d.year, 3) <= d < last_sunday(d.year, 10) else 0
