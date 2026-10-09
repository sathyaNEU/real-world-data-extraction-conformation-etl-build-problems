"""Shared time, calendar and load arithmetic for the task117 pack generator.

All instants are held as integer (or float) epoch seconds in UTC. Quarter-hours are 900-second
blocks of the UTC epoch, which line up with local civil quarter-hours because every offset in
America/Los_Angeles is a whole number of hours.
"""
from __future__ import annotations

import math
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

TZ = ZoneInfo("America/Los_Angeles")
PST = timezone(timedelta(hours=-8))
QH = 900

# The grid every load curve lives on: 2023-12-25 local through 2027-01-04 local.
GRID_T0 = int(datetime(2023, 12, 25, tzinfo=TZ).timestamp())
GRID_T1 = int(datetime(2027, 1, 4, tzinfo=TZ).timestamp())
NQ = (GRID_T1 - GRID_T0) // QH


def lt(y, m, d, hh=0, mm=0, ss=0) -> int:
    """Epoch seconds of a local civil time."""
    return int(datetime(y, m, d, hh, mm, ss, tzinfo=TZ).timestamp())


def lt_date(d: date, hh=0, mm=0, ss=0) -> int:
    return lt(d.year, d.month, d.day, hh, mm, ss)


def iso_local(t: float) -> str:
    """2026-02-17T08:41:30-08:00, seconds truncated."""
    return datetime.fromtimestamp(int(t), TZ).isoformat()


def local_dt(t: float) -> datetime:
    return datetime.fromtimestamp(t, TZ)


def daterange(d0: date, d1: date):
    d = d0
    while d <= d1:
        yield d
        d += timedelta(days=1)


# --- tariff holidays: the six NERC-style days, Saturday observed Friday, Sunday observed Monday
def _nth_weekday(y, m, wd, n):
    d = date(y, m, 1)
    while d.weekday() != wd:
        d += timedelta(days=1)
    return d + timedelta(weeks=n - 1)


def _last_weekday(y, m, wd):
    d = date(y, m + 1, 1) - timedelta(days=1) if m < 12 else date(y, 12, 31)
    while d.weekday() != wd:
        d -= timedelta(days=1)
    return d


def _observed(d: date) -> date:
    if d.weekday() == 5:
        return d - timedelta(days=1)
    if d.weekday() == 6:
        return d + timedelta(days=1)
    return d


def tariff_holidays(year: int) -> list[tuple[str, date]]:
    out = [
        ("New Year's Day", _observed(date(year, 1, 1))),
        ("Memorial Day", _last_weekday(year, 5, 0)),
        ("Independence Day", _observed(date(year, 7, 4))),
        ("Labor Day", _nth_weekday(year, 9, 0, 1)),
        ("Thanksgiving Day", _nth_weekday(year, 11, 3, 4)),
        ("Christmas Day", _observed(date(year, 12, 25))),
    ]
    return out


def holiday_set(years=(2023, 2024, 2025, 2026, 2027, 2028)) -> set[date]:
    s = set()
    for y in years:
        for _, d in tariff_holidays(y):
            s.add(d)
    return s


HOLIDAYS = holiday_set()


def city_holidays(year: int) -> set[date]:
    """City offices closed (not tariff holidays unless listed above too)."""
    s = {d for _, d in tariff_holidays(year)}
    s.add(_nth_weekday(year, 1, 0, 3))   # Martin Luther King Jr. Day
    s.add(_nth_weekday(year, 2, 0, 3))   # Presidents' Day
    s.add(_observed(date(year, 6, 19)))  # Juneteenth
    s.add(_observed(date(year, 11, 11)))  # Veterans Day
    s.add(_nth_weekday(year, 11, 3, 4) + timedelta(days=1))  # day after Thanksgiving
    return s


CITY_HOLIDAYS = set().union(*[city_holidays(y) for y in (2023, 2024, 2025, 2026, 2027)])


def last_weekday_of_month(y: int, m: int) -> date:
    d = date(y, m + 1, 1) - timedelta(days=1) if m < 12 else date(y, 12, 31)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


# --- sunrise and sunset, NOAA approximation, for the roof-level photocell lighting
LAT, LON = 48.02, -122.61


def sun_times(d: date) -> tuple[float, float]:
    """Sunrise and sunset as epoch seconds for local date d."""
    n = d.timetuple().tm_yday
    g = 2 * math.pi / 365 * (n - 1)
    eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                    - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    decl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
            + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    lat = math.radians(LAT)
    ha = math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(lat) * math.cos(decl))
                                - math.tan(lat) * math.tan(decl)))
    rise_utc_min = 720 - 4 * (LON + ha) - eqt
    set_utc_min = 720 - 4 * (LON - ha) - eqt
    base = int(datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp())
    return base + rise_utc_min * 60, base + set_utc_min * 60


# --- load arithmetic on the quarter-hour grid
def load_curve(start, end, rate, nq=NQ, t0=GRID_T0):
    """Sum of constant-rate charging blocks [start, end) at rate kW, as average kW per quarter-hour.

    start, end are float epoch seconds; rate kW. Returns an array of nq average-kW values."""
    start = np.asarray(start, dtype=np.float64)
    end = np.asarray(end, dtype=np.float64)
    rate = np.broadcast_to(np.asarray(rate, dtype=np.float64), start.shape)
    keep = end > start
    start, end, rate = start[keep], end[keep], rate[keep]
    s = (start - t0) / QH
    e = (end - t0) / QH
    i0 = np.floor(s).astype(np.int64)
    i1 = np.floor(e).astype(np.int64)
    out = np.zeros(nq + 2, dtype=np.float64)
    same = i0 == i1
    np.add.at(out, i0[same], rate[same] * (e[same] - s[same]))
    d = ~same
    np.add.at(out, i0[d], rate[d] * (i0[d] + 1 - s[d]))
    np.add.at(out, i1[d], rate[d] * (e[d] - i1[d]))
    diff = np.zeros(nq + 3, dtype=np.float64)
    np.add.at(diff, i0[d] + 1, rate[d])
    np.add.at(diff, i1[d], -rate[d])
    out += np.cumsum(diff)[: nq + 2]
    return out[:nq]


def grid_times(nq=NQ, t0=GRID_T0) -> np.ndarray:
    return t0 + QH * np.arange(nq, dtype=np.int64)


def grid_frame() -> pd.DataFrame:
    t = grid_times()
    loc = pd.to_datetime(t, unit="s", utc=True).tz_convert(TZ)
    df = pd.DataFrame({"t": t})
    df["date"] = loc.date
    df["year"] = loc.year
    df["month"] = loc.month
    df["hour"] = loc.hour
    df["minute"] = loc.minute
    df["wd"] = loc.weekday
    hol = np.array([d in HOLIDAYS for d in df["date"]])
    df["billing"] = (df["wd"] < 5) & (df["hour"] >= 12) & (df["hour"] < 20) & ~hol
    # the same window read one quarter-hour earlier, as a reader who takes the stamps as ends would
    df["billing_shift"] = np.roll(df["billing"].to_numpy(), -1)
    return df


def round_half_up(x: float, step: float = 1.0) -> float:
    return math.floor(x / step + 0.5) * step


def nearest5(x: float) -> int:
    return int(round_half_up(x, 5.0))


def up5(x: float) -> int:
    return int(math.ceil(x / 5.0 - 1e-12) * 5)
