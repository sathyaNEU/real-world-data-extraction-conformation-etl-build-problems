"""task178 records: how the city's systems recorded the world. The verified 15-minute product (station datum, feet,
gaps interpolated up to six hours, the 2017-18 bracket offset never reprocessed), the provisional 6-minute telemetry
(metres on the 2026 station datum), the harbormaster's hourly tide board, the published tide tables, DPW's closure
work orders and the station log."""
from __future__ import annotations

import datetime as dt
from functools import lru_cache

import numpy as np

import common as C
import world as W

BASE = np.datetime64('2000-01-01T12:00')


def ymd_arrays(t):
    d = BASE + (np.asarray(t) * 3600).astype('timedelta64[s]')
    return (d.astype('datetime64[Y]').astype(int) + 1970, d.astype('datetime64[M]').astype(int) % 12 + 1, d)


# ------------------------------------------------------------------------------------- outages of the primary
FORCED_OUTAGES = [  # (start UTC, hours) the primary lost power or comms
    (dt.datetime(2026, 4, 21, 13, 0), 168.0),     # sensor off for the pier cap replacement
]


@lru_cache(None)
def outages():
    """(start hours, end hours) intervals with no primary reading, random plus forced"""
    rng = C.stream("outages")
    out = []
    t0, t1 = C.hours(C.REC_START), C.hours(C.VER_END)
    t = t0
    while True:
        t += rng.exponential(24 * 365.25 / 7.0)        # about seven a year
        if t >= t1:
            break
        dur = float(np.clip(rng.lognormal(np.log(2.5), 0.9), 0.5, 40.0))
        out.append((t, t + dur))
    for s, h in FORCED_OUTAGES:
        a = C.hours(s)
        out.append((a, a + h))
    out.sort()
    return out


@lru_cache(None)
def verified():
    """the verified product: times (hours), value ft above the 1995 station datum (nan where missing), quality"""
    t, z = W.true_15min()
    v = W.to_ft_mllw(z) + C.STND_BELOW_MLLW
    a, b = C.hours(C.BRACKET_FAIL), C.hours(C.BRACKET_RESET)
    v = np.where((t >= a) & (t < b), v - C.BRACKET_OFFSET, v)
    q = np.array(["V"] * len(t), dtype="<U1")
    for s, e in outages():
        m = (t >= s) & (t < e)
        if not m.any():
            continue
        i0, i1 = np.where(m)[0][[0, -1]]
        if e - s <= 6.0 and i0 > 0 and i1 + 1 < len(t):
            lo, hi = v[i0 - 1], v[i1 + 1]
            frac = (t[i0:i1 + 1] - t[i0 - 1]) / (t[i1 + 1] - t[i0 - 1])
            v[i0:i1 + 1] = lo + (hi - lo) * frac
            q[i0:i1 + 1] = "I"
        else:
            v[i0:i1 + 1] = np.nan
            q[i0:i1 + 1] = "M"
    return t, np.round(v, 3), q


@lru_cache(None)
def telemetry():
    """provisional 6-minute telemetry: metres above the 2026 station datum, a few unscreened spikes"""
    t, z = W.true_6min()
    v = (W.to_ft_mllw(z) + C.STND_BELOW_MLLW - C.NEW_STND_SHIFT) * C.FT
    rng = C.stream("telemetry")
    keep = np.ones(len(t), bool)
    for _ in range(9):                      # short comms drops
        i = int(rng.integers(0, len(t) - 40))
        keep[i:i + int(rng.integers(2, 30))] = False
    spikes = rng.choice(len(t), 6, replace=False)
    v = v.copy()
    v[spikes] += rng.choice([-1, 1], 6) * rng.uniform(0.08, 0.20, 6)
    return t[keep], np.round(v[keep], 3)


@lru_cache(None)
def tide_board():
    """the harbormaster's float tide board, hourly, local clock time, feet above the float zero"""
    t, z = W.true_hourly_board()
    v = W.to_ft_mllw(z) + C.BOARD_ZERO_BELOW_MLLW
    rng = C.stream("boardgaps")
    keep = np.ones(len(t), bool)
    for _ in range(40):
        i = int(rng.integers(0, len(t) - 200))
        keep[i:i + int(rng.integers(3, 160))] = False
    return t[keep], np.round(v[keep], 2)


# --------------------------------------------------------------------------------------------- the tide tables
@lru_cache(None)
def tide_table_rows():
    """published predictions: (local datetime, height ft MLLW to 0.1, 'H' or 'L') for 1995-2027"""
    hw_t, hw_h, lw_t, lw_h = W.predicted_hw()
    rows = []
    for tt, hh, kind in ((hw_t, hw_h, "H"), (lw_t, lw_h, "L")):
        ft = W.to_ft_mllw(hh)
        for x, y in zip(tt, ft):
            u = C.from_hours(x)
            u = u.replace(second=0, microsecond=0) + dt.timedelta(minutes=1 if u.second >= 30 else 0)
            loc, zone = C.to_local(u)
            if 1995 <= loc.year <= 2027:
                rows.append((loc, round(float(y) + 1e-9, 1), kind, zone))
    rows.sort()
    return rows


# ---------------------------------------------------------------------------------------------- DPW closures
@lru_cache(None)
def closures():
    """DPW street-closure work orders 2016 to November 2026 as the systems hold them.

    Returns the rows as exported and the truth (one entry per real closure: Front Street, start UTC, tidal)."""
    rng = C.stream("closures")
    hw_t, _, _, _ = W.predicted_hw()
    t15, z15 = W.true_15min()
    t6, z6 = W.true_6min()
    a, b = C.hours(dt.datetime(2016, 1, 1, 5)), C.hours(dt.datetime(2026, 12, 1, 5))
    truth = []
    for h in hw_t[(hw_t >= a) & (hw_t < b)]:
        if h < t15[-1] - 3:
            j = np.searchsorted(t15, h); seg = z15[j - 12:j + 13]
        else:
            j = np.searchsorted(t6, h); seg = z6[max(0, j - 30):j + 31]
        if len(seg) == 0:
            continue
        v = float(W.to_ft_mllw(seg.max()))
        fc = v + rng.normal(0, 0.22)          # what the night's forecast said
        p = np.clip((fc - 11.55) / 0.45, 0, 1)
        if rng.uniform() < p:
            start = h - rng.uniform(0.6, 1.9)
            end = h + rng.uniform(1.0, 2.6)
            truth.append(dict(start=start, end=end, tidal=True, level=v))
    for y in range(2016, 2027):                # drain and rain flooding, away from high water
        for _ in range(int(rng.poisson(2.5))):
            s = C.hours(dt.datetime(y, int(rng.integers(1, 12 if y == 2026 else 13)), int(rng.integers(1, 29)), 5)) \
                + rng.uniform(0, 24)
            near = hw_t[np.argmin(np.abs(hw_t - s))]
            if abs(near - s) < 4.0:
                s = near + 5.0 + rng.uniform(0, 1.5)
            if any(abs(s - q["start"]) < 9.0 for q in truth if q["tidal"]):
                continue
            truth.append(dict(start=s, end=s + rng.uniform(1.5, 5.0), tidal=False, level=None))
    truth.sort(key=lambda r: r["start"])
    LEGACY_END = C.hours(dt.datetime(2023, 7, 1, 4))
    rows = []
    n_leg = n_new = 0
    for r in truth:
        su, eu = C.from_hours(r["start"]), C.from_hours(r["end"])
        su = su.replace(second=0, microsecond=0); eu = eu.replace(second=0, microsecond=0)
        note = "" if r["tidal"] else rng.choice(["drain backup", "catch basins surcharged", "heavy rain", ""])
        loc_txt = rng.choice(["FRONT ST", "FRONT ST @ CUTLER WHARF", "FRONT ST (CUTLER WHF TO ROPEWALK RD)"])
        if r["start"] < LEGACY_END:
            n_leg += 1
            wo = "%02d-%05d" % (su.year % 100, 1000 + n_leg * 7 + int(rng.integers(0, 6)))
            rows.append(dict(wo=wo, system="WOMS", source="HM" if rng.uniform() < 0.1 else "DPW", opened=su, closed=eu, location=loc_txt,
                             reason="FLOOD", note=note, clock="utc", real=r))
            if rng.uniform() < 0.25:            # barricades reset after the crew moved them: a new work order
                s2 = (eu + dt.timedelta(minutes=int(rng.integers(40, 170)))).replace(second=0)
                e2 = s2 + dt.timedelta(minutes=int(rng.integers(50, 140)))
                wo2 = "%02d-%05d" % (s2.year % 100, 1000 + n_leg * 7 + 6)
                rows.append(dict(wo=wo2, system="WOMS", source="DPW", opened=s2, closed=e2, location=loc_txt,
                                 reason="FLOOD", note="", clock="utc", real=None))
        else:
            n_new += 1
            loc_l, _ = C.to_local(su)
            loc_e, _ = C.to_local(eu)
            wo = "PW-%d-%04d" % (loc_l.year, 200 + n_new * 3 + int(rng.integers(0, 3)))
            rows.append(dict(wo=wo, system="PWWORKS", source="DPW", opened=loc_l, closed=loc_e, location=loc_txt.title(),
                             reason="FLOOD", note=note, clock="local", real=r))
    # other streets' flooding closures on the same export
    for y in range(2016, 2027):
        for _ in range(int(rng.poisson(1.5))):
            s = C.hours(dt.datetime(y, int(rng.integers(1, 12 if y == 2026 else 13)), int(rng.integers(1, 29)), 13))
            su = C.from_hours(s).replace(second=0, microsecond=0)
            legacy = s < LEGACY_END
            op = su if legacy else C.to_local(su)[0]
            rows.append(dict(wo=("%02d-%05d" % (op.year % 100, 9000 + int(rng.integers(0, 999)))) if legacy
                             else "PW-%d-%04d" % (op.year, 7000 + int(rng.integers(0, 999))),
                             system="WOMS" if legacy else "PWWORKS", source="DPW", opened=op,
                             closed=op + dt.timedelta(hours=2), location=rng.choice(["FERRY LN", "WATER ST", "Water St"]),
                             reason="FLOOD", note="", clock="utc" if legacy else "local", real=None))
    rows.sort(key=lambda r: (r["opened"] + (dt.timedelta(hours=-5) if r["clock"] == "utc" else dt.timedelta(0)), r["wo"]))
    # work-order numbers run through every work order the systems open (potholes, signs, water), so the flooding
    # orders' numbers rise unevenly through each year
    counters = {}
    for r in rows:
        key = (r["system"], r["opened"].year)
        if key not in counters:
            counters[key] = int(rng.integers(3, 140))
        counters[key] += int(rng.integers(1, 11)) if False else int(rng.geometric(1 / 260.0))
        n = counters[key]
        if r["system"] == "WOMS":
            r["wo"] = "%02d-%05d" % (r["opened"].year % 100, n)
        else:
            r["wo"] = "PW-%d-%05d" % (r["opened"].year, n)
    return rows, truth
