"""task178 world: the Tumwick River at TUM-02 before any file is written. The true stage-discharge relation (a channel
control with a floodplain that takes flow above the left bank), the annual peaks of water years 1980 to 2025, the
15-minute record of water years 2016 to 2025, the field measurements, the site visits and their orifice purges, and
the pipe-bridge radar. Everything downstream (pack, golden, checks) reads this module; nothing here reads a file."""
from __future__ import annotations

import datetime as dt
from functools import lru_cache

import numpy as np
from scipy import stats

import common as C

# ------------------------------------------------------------------------------------------- the true rating
E0, A0, B0 = 0.85, 102.6, 1.72          # channel control: Q = A0 (h - E0)^B0, h on the current datum (ft), Q cfs
HBF = 10.20                              # left bank, current datum
AF, PF, WF = 1290.0, 1.70, 0.12          # floodplain: AF * d^PF with d the depth over the bank, softened over WF ft


def q_true(h):
    h = np.asarray(h, float)
    qc = A0 * np.clip(h - E0, 0.0, None) ** B0
    x = (h - HBF) / WF
    d = WF * np.logaddexp(0.0, x)          # a soft start: the pasture's swales take water a little before the bank
    d = np.where(x < -30, 0.0, d)
    return qc + AF * d ** PF


_HG = np.arange(0.86, 24.0, 0.0005)
_QG = q_true(_HG)


def h_true(q):
    return np.interp(np.asarray(q, float), _QG, _HG)


# --------------------------------------------------------------------------------------- the annual peaks
LP3_MU, LP3_SD, LP3_G = 3.687, 0.205, 0.05
N_WY = C.WY_LAST - C.WY_FIRST + 1


@lru_cache(None)
def annual_peak_q():
    """46 annual peak discharges (cfs), water years 1980 to 2025; the largest is put in water year 2025 (the January
    flood that damaged the pipe bridge), the order of the rest as drawn"""
    r = C.stream("ams")
    z = stats.pearson3.rvs(LP3_G, size=N_WY, random_state=r)
    q = 10 ** (LP3_MU + LP3_SD * z)
    k = int(np.argmax(q))
    q[k], q[-1] = q[-1], q[k]
    return np.round(q, 1)


FIXED_PEAKS = {2020: (2020, 2, 1), 2021: (2021, 1, 12), 2022: (2021, 11, 15), 2023: (2022, 12, 27),
               2024: (2023, 12, 5), 2025: (2025, 1, 8)}


def peak_dates():
    """the date and local time of each water year's peak, November to February mostly"""
    r = C.stream("peakdates")
    out = []
    months = (11, 12, 1, 2, 3, 10)
    pm = np.array([0.24, 0.30, 0.22, 0.14, 0.06, 0.04])
    for i, wy in enumerate(range(C.WY_FIRST, C.WY_LAST + 1)):
        m = int(r.choice(months, p=pm))
        y = wy - 1 if m >= 10 else wy
        d = dt.date(y, m, int(r.integers(1, 28)))
        if wy in FIXED_PEAKS:
            d = dt.date(*FIXED_PEAKS[wy])
        out.append(dt.datetime(d.year, d.month, d.day, int(r.integers(0, 24)), int(r.choice([0, 15, 30, 45]))))
    return out


# ------------------------------------------------------------------------------- the 15-minute record 2016-2025
T0 = dt.datetime(2015, 10, 1, 0, 0)        # PST
T1 = dt.datetime(2025, 10, 1, 0, 0)
STEP = dt.timedelta(minutes=15)
N15 = int((T1 - T0) / STEP)


def t_of(i):
    return T0 + STEP * int(i)


def i_of(t):
    return int(round((t - T0) / STEP))


_KNOTS = ((1, 1.0), (60, 0.9), (121, 0.55), (182, 0.18), (213, 0.07), (253, 0.0), (288, 0.1), (319, 0.6), (349, 0.95),
          (366, 1.0))


def season(doy):
    """the seasonal share of the base flow: high in midwinter, receding from spring to its low in early September"""
    x, y = zip(*_KNOTS)
    return np.interp(np.asarray(doy, float), x, y)


def _gamma_shape(n, tp_steps, k=3.6):
    t = np.arange(n, dtype=float)
    x = t / tp_steps
    return np.where(t > 0, (x ** k) * np.exp(k * (1 - x)), 0.0)


@lru_cache(None)
def series():
    """true discharge (cfs) every 15 minutes, PST, water years 2016 to 2025, with each water year's peak equal to its
    annual peak; returns (q, events) where events lists (wy, start index, rise steps, size, kind)"""
    r = C.stream("series")
    days = np.arange(N15) / 96.0
    doy = np.array([(T0 + dt.timedelta(days=float(d))).timetuple().tm_yday for d in np.arange(0, N15 / 96.0 + 1)])
    doy15 = doy[(np.arange(N15) // 96)]
    base = 235.0 + 980.0 * season(doy15)
    q = base.copy()
    events = []
    ams = annual_peak_q()
    pd = peak_dates()
    for wy in C.STAGE_WY:
        a = i_of(dt.datetime(wy - 1, 10, 1))
        b = i_of(dt.datetime(wy, 10, 1))
        # storms through the year
        t = a
        while t < b:
            m = t_of(t).month
            lam = {11: 0.20, 12: 0.20, 1: 0.18, 2: 0.13, 3: 0.12, 10: 0.10, 4: 0.07, 5: 0.05, 6: 0.03}.get(m, 0.012)
            t += int(r.exponential(1.0 / lam) * 96)
            if t >= b:
                break
            m = t_of(t).month
            summer = m in (7, 8, 9)
            size = float(np.exp(r.normal(np.log(110 if summer else 1500), 0.55 if summer else 0.70)))
            tp = int(r.uniform(36, 90))
            events.append([wy, t, tp, size, "summer" if summer else "storm"])
        # the annual peak storm, at its date
        tpk = pd[wy - C.WY_FIRST]
        ip = i_of(dt.datetime(tpk.year, tpk.month, tpk.day, tpk.hour, tpk.minute))
        tp = int(r.uniform(44, 84))
        events.append([wy, ip - tp, tp, 1.0, "annual"])
        # a freshet inside each work window
        ws = i_of(dt.datetime(wy, 7, 25))
        events.append([wy, ws + int(r.integers(0, 40 * 96)), int(r.uniform(30, 60)),
                       float(r.uniform(160, 420)), "window"])
    L = 50 * 96
    shapes = {}
    slow = np.zeros(N15)
    quick = np.zeros(N15)
    for ev in events:
        if ev[4] == "annual":
            continue
        wy, t0, tp, size, kind = ev
        sh = shapes.setdefault(tp, _gamma_shape(L, tp))
        n = min(L, N15 - t0)
        quick[t0:t0 + n] += size * sh[:n]
        rec = (1 - np.exp(-np.arange(L) / (1.5 * tp))) * (np.exp(-np.arange(L) / (9 * 96.0)) - np.exp(-L / (9 * 96.0)))
        slow[t0:t0 + n] += 0.22 * size * rec[:n]
    q = base + quick + slow
    # no other storm of a water year comes within 15 per cent of its annual peak
    for wy in C.STAGE_WY:
        a = i_of(dt.datetime(wy - 1, 10, 1))
        b = i_of(dt.datetime(wy, 10, 1))
        cap = 0.85 * ams[wy - C.WY_FIRST]
        if q[a:b].max() > cap:
            lo, hi = 0.0, 1.0
            for _ in range(60):
                f = (lo + hi) / 2
                if (base[a:b] + f * (q[a:b] - base[a:b])).max() > cap:
                    hi = f
                else:
                    lo = f
            q[a:b] = base[a:b] + lo * (q[a:b] - base[a:b])
    # scale each annual storm so the water year's maximum is the annual peak
    for ev in events:
        if ev[4] != "annual":
            continue
        wy, t0, tp, _, _ = ev
        target = ams[wy - C.WY_FIRST]
        sh = _gamma_shape(L, tp)
        rec = (1 - np.exp(-np.arange(L) / (1.5 * tp))) * (np.exp(-np.arange(L) / (9 * 96.0)) - np.exp(-L / (9 * 96.0)))
        a = i_of(dt.datetime(wy - 1, 10, 1))
        b = i_of(dt.datetime(wy, 10, 1))
        n = min(L, N15 - t0)
        size = target
        for _ in range(30):
            trial = q.copy()
            trial[t0:t0 + n] += size * sh[:n] + 0.22 * size * rec[:n]
            mx = trial[a:b].max()
            if abs(mx - target) < 0.05:
                break
            size *= target / mx
        ev[3] = size
        q = trial
    # each work window's freshet stands at least 0.25 ft above the window's first and last readings
    for ev in events:
        if ev[4] != "window":
            continue
        wy, t0, tp, size, _ = ev
        a = i_of(C.local_to_pst(dt.datetime(wy, 7, 15)))
        b = i_of(C.local_to_pst(dt.datetime(wy, 9, 16)))
        sh = shapes.setdefault(tp, _gamma_shape(L, tp))
        n = min(L, N15 - t0)
        for _ in range(40):
            hh = h_true(q[a:b])
            if hh.max() >= max(hh[0], hh[-1]) + 0.25 and a + int(np.argmax(hh)) in range(t0, t0 + 3 * tp):
                break
            q[t0:t0 + n] += 0.25 * size * sh[:n]
    return q, [tuple(e) for e in events]


def stage_true():
    q, _ = series()
    return h_true(q)


@lru_cache(None)
def stage_recorded():
    """the river's stage as the bubbler would read it with no visit and no offset (0.01 ft)"""
    r = C.stream("stagenoise")
    h = np.round(stage_true() + r.normal(0, 0.004, N15), 2)
    for wy in C.STAGE_WY:                     # one reading holds each water year's crest
        a = i_of(dt.datetime(wy - 1, 10, 1))
        b = i_of(dt.datetime(wy, 10, 1))
        k = a + int(np.argmax(h[a:b]))
        top = h[a:b].max()
        for j in np.where(h[a:b] == top)[0] + a:
            if j != k:
                h[j] = round(top - 0.01, 2)
    return h


# ------------------------------------------------------------------------------------------- the site visits
@lru_cache(None)
def visits():
    """routine visits to TUM-02, water years 2016 to 2025: (arrive local, depart local, purge local or None, party).
    Every in-water work window holds at least one routine visit with a purge."""
    r = C.stream("visits")
    out = []
    d = dt.date(2015, 10, 6)
    while d < dt.date(2025, 9, 30):
        if d.weekday() >= 5:
            d += dt.timedelta(days=2 if d.weekday() == 5 else 1)
            continue
        arrive = dt.datetime(d.year, d.month, d.day, int(r.integers(8, 14)), int(r.integers(0, 12)) * 5)
        depart = arrive + dt.timedelta(minutes=int(r.integers(14, 30)) * 5)
        purge = arrive + dt.timedelta(minutes=int(r.integers(3, 7)) * 5) if r.random() < 0.85 else None
        party = ["SH", "SH/GW", "GW", "TM", "SH/TM"][int(r.integers(0, 5))] if d.year < 2021 else \
            ["GW", "GW/DM", "DM", "BD/DM"][int(r.integers(0, 4))]
        out.append([arrive, depart, purge, party])
        d += dt.timedelta(days=int(r.integers(33, 52)))
    # the 2025 controller swap and the visit that reset its offset
    for when, a, b in ((C.LOGGER_SWAP, (10, 5), (12, 25)), (C.LOGGER_FIX, (10, 50), (12, 20))):
        out = [v for v in out if abs((v[0].date() - when.date()).days) > 6]
        arr = dt.datetime(when.year, when.month, when.day, *a)
        out.append([arr, dt.datetime(when.year, when.month, when.day, *b), arr + dt.timedelta(minutes=15), "GW/DM"])
    # a purge in every work window
    for y in C.ASK_A_YEARS:
        lo, hi = dt.datetime(y, 7, 15), dt.datetime(y, 9, 16)
        inside = [v for v in out if lo <= v[0] < hi]
        if not any(v[2] for v in inside):
            if inside:
                inside[0][2] = inside[0][0] + dt.timedelta(minutes=20)
            else:
                a = dt.datetime(y, 8, int(r.integers(4, 20)), 10, 5)
                out.append([a, a + dt.timedelta(minutes=95), a + dt.timedelta(minutes=20), "GW"])
    # no purge at high water: the line is purged only with the river under 6 ft
    h = stage_recorded()
    for v in out:
        if v[2] is None:
            continue
        j = i_of(C.local_to_pst(v[2]))
        wy = C.water_year(t_of(j).date())
        a = i_of(dt.datetime(wy - 1, 10, 1))
        b = i_of(dt.datetime(wy, 10, 1))
        if h[j] > 6.0 or h[j] + 1.5 > h[a:b].max() - 1.0:
            v[2] = None
    out.sort(key=lambda v: v[0])
    return [tuple(v) for v in out]


def purge_readings():
    """the 15-minute indices a purge lifts, with the lift (ft): the first and second reading after the purge"""
    r = C.stream("purges")
    lifts = {}
    for arrive, depart, purge, _ in visits():
        if purge is None:
            continue
        p = C.local_to_pst(purge)
        i = i_of(p)
        if t_of(i) < p:
            i += 1
        d1 = float(r.uniform(0.85, 1.45))
        lifts[i] = round(d1, 2)
        lifts[i + 1] = round(d1 * float(r.uniform(0.30, 0.55)), 2)
    return lifts


# ------------------------------------------------------------------------------------- the field measurements
def _seasonal_base(d):
    return 235.0 + 980.0 * float(season(d.timetuple().tm_yday))


@lru_cache(None)
def measurements():
    """every discharge measurement at TUM-02: dict(time local, gh current datum, q measured cfs, q true, method,
    era, party, kind). Routine measurements sit in the channel; flood measurements on the floodplain."""
    r = C.stream("meas")
    ams = annual_peak_q()
    pdts = peak_dates()
    out = []
    # 1980 to 2015: routine measurements at random flows, no continuous record in the pack
    d = dt.date(1979, 10, 12)
    while d < dt.date(2015, 10, 1):
        if d.weekday() < 5:
            q = _seasonal_base(d) * float(np.exp(r.normal(0.35, 0.55)))
            q = min(q, 0.93 * q_true(HBF))
            h = float(h_true(q)) + float(r.normal(0, 0.006))
            t = dt.datetime(d.year, d.month, d.day, int(r.integers(8, 15)), int(r.integers(0, 12)) * 5)
            meth = "ADCP" if d >= C.ADCP_FROM and q > 1800 else ("wading" if q < 1100 else "bridge")
            sig = {"wading": 0.040, "bridge": 0.050, "ADCP": 0.045}[meth]
            out.append(dict(time=t, gh=h, q_true=q, q=q * float(np.exp(r.normal(0, sig))), method=meth, kind="routine"))
            d += dt.timedelta(days=int(r.integers(34, 54)))
        else:
            d += dt.timedelta(days=1)
    # flood measurements before the record in the pack: the bridge current meter in 1990 and 1996, ADCP from 2005
    for i, wy in enumerate(range(C.WY_FIRST, 2016)):
        hp = float(h_true(ams[i]))
        if hp <= HBF + 0.08:
            continue
        if wy < 2005 and wy not in (1991, 1996, 2003):
            continue
        n = int(r.integers(1, 3)) if wy < 2005 else int(r.integers(2, 6))
        tp = pdts[i]
        for k in range(n):
            frac = float(r.uniform(0.86, 1.0)) if k == 0 else float(r.uniform(0.15, 0.95))
            h = HBF + (hp - HBF) * frac
            t = tp + dt.timedelta(hours=float(r.uniform(-6, -1.5)) if k == 0 else float(r.choice([-1, 1]) * r.uniform(3, 30)))
            meth = "bridge" if wy < 2005 else "ADCP"
            sig = 0.07 if meth == "bridge" else 0.055
            q = float(q_true(h))
            out.append(dict(time=t.replace(second=0, microsecond=0), gh=h, q_true=q, q=q * float(np.exp(r.normal(0, sig))),
                            method=meth, kind="flood"))
    # 2016 to 2025: routine measurements at the visits, flood measurements on the record's own floods
    h15 = stage_recorded()
    q15, _ = series()
    for arrive, depart, purge, _ in visits():
        if r.random() < 0.10:
            continue
        mid = arrive + (depart - arrive) / 2
        i = i_of(C.local_to_pst(mid))
        q = float(q15[i])
        meth = "wading" if q < 1100 else "ADCP"
        sig = 0.040 if meth == "wading" else 0.045
        out.append(dict(time=arrive + dt.timedelta(minutes=10), gh=float(stage_true()[i]), q_true=q,
                        q=q * float(np.exp(r.normal(0, sig))), method=meth, kind="routine"))
    st = stage_true()
    over = st > HBF + 0.05
    edges = np.flatnonzero(np.diff(over.astype(int)))
    starts, ends = edges[::2] + 1, edges[1::2] + 1
    for s0, e0 in zip(starts, ends):
        if e0 - s0 < 6:
            continue
        top = s0 + int(np.argmax(st[s0:e0]))
        picks = [top - int(r.integers(0, 3))]
        for _ in range(int(r.integers(1, 4))):
            picks.append(int(r.integers(s0, e0)))
        for j in picks:
            tl = C.pst_to_local(t_of(j))
            out.append(dict(time=tl, gh=float(st[j]), q_true=float(q15[j]), q=float(q15[j]) * float(np.exp(r.normal(0, 0.055))),
                            method="ADCP", kind="flood"))
    out.sort(key=lambda m: m["time"])
    return out


@lru_cache(None)
def peak_stages():
    """the 46 annual peak stages as recorded, current datum (ft): the register's readings 1980 to 2015 and the
    15-minute record's crest after"""
    r = C.stream("peakstage")
    ams = annual_peak_q()
    out = []
    h15 = stage_recorded()
    for i, wy in enumerate(range(C.WY_FIRST, C.WY_LAST + 1)):
        if wy < 2016:
            out.append(round(float(h_true(ams[i])) + float(r.normal(0, 0.006)), 2))
        else:
            a = i_of(dt.datetime(wy - 1, 10, 1))
            b = i_of(dt.datetime(wy, 10, 1))
            out.append(float(h15[a:b].max()))
    return tuple(out)


# ----------------------------------------------------------------------------------------- recorded 15-minute stage
def logger_offset_error(i):
    """the 2025 controller swap: the new unit's offset 0.47 ft high until the August visit reset it"""
    t = t_of(i)
    return C.LOGGER_OFFSET_ERR if C.local_to_pst(C.LOGGER_SWAP) <= t < C.local_to_pst(C.LOGGER_FIX) else 0.0


@lru_cache(None)
def stage_logged():
    """what the logger stored: the river's stage, the purges' lifts, the 2025 offset"""
    h = stage_recorded().copy()
    a, b = i_of(C.local_to_pst(C.LOGGER_SWAP)), i_of(C.local_to_pst(C.LOGGER_FIX))
    lo = a if t_of(a) >= C.local_to_pst(C.LOGGER_SWAP) else a + 1
    hi = b if t_of(b) >= C.local_to_pst(C.LOGGER_FIX) else b + 1
    h[lo:hi] = np.round(h[lo:hi] + C.LOGGER_OFFSET_ERR, 2)
    for j, lift in purge_readings().items():
        h[j] = round(h[j] + lift, 2)
    return h


# ------------------------------------------------------------------------------------------- the pipe radar
def fall_to_pipe(q):
    """water-surface fall from TUM-02 to the Sauer pipe bridge, 900 ft downstream (ft)"""
    return 0.92 + 0.30 * np.sqrt(np.asarray(q, float) / 10000.0)


@lru_cache(None)
def radar():
    """the radar on the pipe bridge, every 15 minutes (PST index) from its installation: true water level at the pipe
    (ft NAVD88), the distance the radar measures (ft), the level SCADA computes from it"""
    r = C.stream("radar")
    q, _ = series()
    i0 = i_of(C.local_to_pst(C.RADAR_INSTALL)) + 1
    wse = C.DATUM_NAVD_NEW + stage_true() - fall_to_pipe(q)
    lag = 1                                        # the pipe's water lags the gauge by about a reading
    pipe = np.concatenate([wse[:lag], wse[:-lag]])
    pipe = pipe + r.normal(0, 0.012, N15)
    jb = i_of(C.local_to_pst(C.BRACKET_DATE))
    jb = jb if t_of(jb) >= C.local_to_pst(C.BRACKET_DATE) else jb + 1
    face = np.where(np.arange(N15) >= jb, C.RADAR_FACE_NEW, C.RADAR_FACE_INSTALL)
    dist = np.round(face - pipe, 2)
    level = np.round(C.RADAR_FACE_INSTALL - dist, 2)
    return i0, pipe, dist, level


def window_bounds(y):
    """the in-water work window of year y as PST indices [a, b): 00:00 local on 15 July to 24:00 local on 15 September"""
    a = C.local_to_pst(dt.datetime(y, 7, 15))
    b = C.local_to_pst(dt.datetime(y, 9, 16))
    return i_of(a), i_of(b)


def crest_index(wy, h=None):
    h = stage_recorded() if h is None else h
    a = i_of(dt.datetime(wy - 1, 10, 1))
    b = i_of(dt.datetime(wy, 10, 1))
    return a + int(np.argmax(h[a:b]))


@lru_cache(None)
def protected_indices():
    """readings no telemetry gap removes: each water year's crest and its neighbours, each work window's highest river
    stage, the purge lifts"""
    keep = set()
    for wy in C.STAGE_WY:
        k = crest_index(wy)
        keep.update(range(k - 8, k + 9))
    h = stage_recorded()
    for y in C.ASK_A_YEARS:
        a, b = window_bounds(y)
        k = a + int(np.argmax(h[a:b]))
        keep.update(range(k - 4, k + 5))
    keep.update(purge_readings().keys())
    return frozenset(keep)
