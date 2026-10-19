"""task248 clocks: New Zealand local time against UTC (NZST UTC+12, NZDT UTC+13 from the last Sunday of September at
02:00 standard time to the first Sunday of April at 03:00 daylight time)."""
import datetime as dt


def _last_sunday(y, m):
    d = dt.date(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(y, 12, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def _first_sunday(y, m):
    d = dt.date(y, m, 1)
    while d.weekday() != 6:
        d += dt.timedelta(days=1)
    return d


def dst_bounds_utc(y):
    """the UTC instants daylight time ends (April) and starts (September) in year y"""
    end = dt.datetime.combine(_first_sunday(y, 4), dt.time(3, 0)) - dt.timedelta(hours=13)
    start = dt.datetime.combine(_last_sunday(y, 9), dt.time(2, 0)) - dt.timedelta(hours=12)
    return end, start


def offset(utc):
    end, start = dst_bounds_utc(utc.year)
    return 12 if end <= utc < start else 13


def to_local(utc):
    return utc + dt.timedelta(hours=offset(utc))


def to_utc(local):
    """a local wall time to UTC (the later instant where a wall hour repeats, NZST)"""
    for off in (12, 13):
        u = local - dt.timedelta(hours=off)
        if offset(u) == off:
            return u
    return local - dt.timedelta(hours=12)       # a wall time skipped by the spring change
