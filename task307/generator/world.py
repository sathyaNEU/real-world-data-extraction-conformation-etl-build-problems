"""Sørdal Kraft: the simulated world (hourly unit output 2016-2026, runner pitting, inspections, maintenance).

Everything is deterministic from SEED. Times are kept as UTC hour indexes from 2016-01-01 00:00 Europe/Oslo.
Truth: a Francis runner's cavitation pitting grows only in the hours its unit runs inside the rough zone
(30 per cent inclusive to 58 per cent exclusive of rated output), at K_Z cm2 per such hour.
"""
import datetime as dt
from zoneinfo import ZoneInfo
import numpy as np

SEED = 307
OSLO = ZoneInfo('Europe/Oslo')
UTC = dt.timezone.utc
T0 = dt.datetime(2016, 1, 1, 0, tzinfo=OSLO).astimezone(UTC)
T1 = dt.datetime(2027, 1, 1, 0, tzinfo=OSLO).astimezone(UTC)
NH = int((T1 - T0).total_seconds() // 3600)
K_Z = 0.240                     # cm2 of pitting per rough-zone hour
RZ_LO, RZ_HI = 0.30, 0.58
LIMIT = 2400.0
CUT_LOCAL = dt.datetime(2027, 1, 1, 0, tzinfo=OSLO)

UNITS = ['OSD-G1', 'OSD-G2', 'SDL-G1', 'SDL-G2', 'SDL-G3', 'NSV-G1', 'NSV-G2']
STATION = {'OSD': 'Øvre Sørdal', 'SDL': 'Sørdal', 'NSV': 'Nesvik'}
RATED = {'OSD-G1': 62.0, 'OSD-G2': 62.0, 'SDL-G1': 38.0, 'SDL-G2': 38.0, 'SDL-G3': 38.0, 'NSV-G1': 45.0, 'NSV-G2': 45.0}
COMMISSIONED = {'OSD-G1': 1971, 'OSD-G2': 1971, 'SDL-G1': 1963, 'SDL-G2': 1963, 'SDL-G3': 1988, 'NSV-G1': 1979, 'NSV-G2': 1979}
QUOTE_MNOK = {'OSD-G1': 18.4, 'OSD-G2': 18.4, 'SDL-G1': 14.6, 'SDL-G2': 13.9, 'SDL-G3': 14.2, 'NSV-G1': 14.4, 'NSV-G2': 14.4}
FCR_FROM = dt.datetime(2022, 1, 1, tzinfo=OSLO)
FCR_UNITS = ('SDL-G1', 'NSV-G1')
# duty: (share of running hours in the rough zone, share below 30 per cent, base on-probability)
DUTY = {'OSD-G1': (0.050, 0.015, 0.90), 'OSD-G2': (0.051, 0.015, 0.88), 'SDL-G1': (0.054, 0.015, 0.87),
        'SDL-G2': (0.050, 0.015, 0.86), 'SDL-G3': (0.600, 0.050, None), 'NSV-G1': (0.052, 0.015, 0.88),
        'NSV-G2': (0.030, 0.012, 0.90)}
FCR_DUTY = {'SDL-G1': (0.110, 0.008, 0.93), 'NSV-G1': (0.120, 0.008, 0.94)}


def local(i):
    return (T0 + dt.timedelta(hours=int(i))).astimezone(OSLO)


def hidx(local_dt):
    """Index of the hour starting at a local datetime (aware)."""
    return int((local_dt.astimezone(UTC) - T0).total_seconds() // 3600)


def L(y, m, d, h=0):
    return hidx(dt.datetime(y, m, d, h, tzinfo=OSLO))


# planned outages (overhauls, during which inspections happen), local dates, end exclusive
OVERHAULS = {
    'OSD-G1': [((2019, 8, 19), (2019, 10, 7)), ((2022, 8, 15), (2022, 9, 26))],
    'OSD-G2': [((2016, 7, 25), (2016, 9, 12)), ((2020, 7, 27), (2020, 9, 14)), ((2025, 8, 4), (2025, 9, 1))],
    'SDL-G1': [((2017, 6, 12), (2017, 7, 24)), ((2021, 6, 14), (2021, 7, 26))],
    'SDL-G2': [((2019, 6, 3), (2019, 8, 5)), ((2023, 6, 19), (2023, 7, 31))],
    'SDL-G3': [((2017, 5, 22), (2017, 6, 26)), ((2020, 5, 25), (2020, 6, 29)), ((2024, 5, 21), (2024, 7, 1))],
    'NSV-G1': [((2017, 7, 17), (2017, 8, 28)), ((2021, 7, 19), (2021, 8, 30))],
    'NSV-G2': [((2019, 5, 13), (2019, 6, 24)), ((2024, 8, 12), (2024, 8, 26))],
}
# inspections: runner, local date, unit, repaired-to (None = as found kept)
INSPECTIONS = [
    ('R-301', (2019, 9, 10), 'OSD-G1', None), ('R-301', (2022, 9, 6), 'OSD-G1', None),
    ('R-302', (2016, 8, 16), 'OSD-G2', 280.0), ('R-302', (2020, 8, 18), 'OSD-G2', None),
    ('R-205', (2017, 7, 4), 'SDL-G1', None), ('R-205', (2021, 7, 6), 'SDL-G1', None),
    ('R-206', (2019, 6, 11), 'SDL-G2', None),
    ('R-410', (2019, 7, 23), 'SDL-G2', None), ('R-410', (2023, 7, 11), 'SDL-G2', None),
    ('R-207', (2017, 6, 13), 'SDL-G3', 300.0), ('R-207', (2020, 6, 16), 'SDL-G3', 400.0), ('R-207', (2024, 6, 11), 'SDL-G3', None),
    ('R-208', (2024, 6, 25), 'SDL-G3', None),
    ('R-501', (2017, 8, 8), 'NSV-G1', None), ('R-501', (2021, 8, 10), 'NSV-G1', None),
    ('R-502', (2019, 6, 4), 'NSV-G2', None),
]
# runner pitting at 2016-01-01 (cm2), and which runner sits in which unit when
PIT0 = {'R-301': 640.0, 'R-302': 1010.0, 'R-205': 380.0, 'R-206': 1260.0, 'R-410': 220.0, 'R-207': 1150.0,
        'R-208': 0.0, 'R-501': 557.0, 'R-502': 1180.0}
RUNNER_IN = {  # unit -> [(from local date, runner)]
    'OSD-G1': [((2016, 1, 1), 'R-301')], 'OSD-G2': [((2016, 1, 1), 'R-302')], 'SDL-G1': [((2016, 1, 1), 'R-205')],
    'SDL-G2': [((2016, 1, 1), 'R-206'), ((2019, 7, 22), 'R-410')], 'SDL-G3': [((2016, 1, 1), 'R-207'), ((2024, 6, 24), 'R-208')],
    'NSV-G1': [((2016, 1, 1), 'R-501')], 'NSV-G2': [((2016, 1, 1), 'R-502')],
}
PRE_OVERHAUL_END = {'OSD-G1': (2015, 10, 5), 'OSD-G2': (2012, 9, 10), 'SDL-G1': (2013, 7, 29), 'SDL-G2': (2015, 7, 6),
                    'SDL-G3': (2014, 7, 7), 'NSV-G1': (2013, 9, 2), 'NSV-G2': (2015, 6, 22)}
# old-historian slots before each station's RTU replacement: tag -> unit whose output it carried
RTU_NEW = {'OSD': (2016, 8, 1), 'SDL': (2017, 6, 12), 'NSV': (2017, 7, 24)}
OLD_SLOT = {'OSD_U1': 'OSD-G2', 'OSD_U2': 'OSD-G1', 'SDL_U1': 'SDL-G2', 'SDL_U2': 'SDL-G3', 'SDL_U3': 'SDL-G1',
            'NES_U1': 'NSV-G2', 'NES_U2': 'NSV-G1'}
PRE_PERIOD_INSPECTIONS = [  # before the hourly record: runner, local date, unit, found, repaired-to
    ('R-301', (2015, 9, 8), 'OSD-G1', 1420.0, 300.0), ('R-302', (2012, 8, 14), 'OSD-G2', 1610.0, 290.0),
    ('R-205', (2013, 7, 2), 'SDL-G1', 1530.0, 240.0), ('R-206', (2015, 6, 9), 'SDL-G2', 980.0, None),
    ('R-410', (2015, 5, 26), 'NSV-G2', 1460.0, 220.0), ('R-207', (2014, 6, 10), 'SDL-G3', 1980.0, 350.0),
    ('R-501', (2013, 8, 6), 'NSV-G1', 1390.0, 230.0), ('R-502', (2015, 5, 27), 'NSV-G2', 1010.0, None),
]


TRIP_SEED = 3307
RM_OFF = 8
VALUE_WINTERS = [(y, 12, 1) for y in range(2021, 2026)]


def trip_layer(out, forced):
    """Protection trips, from their own generator so nothing above moves. Three kinds:
    'long'  a unit trip that opened a forced outage (the unit stands for hours, the hourly record shows the stop);
    'quick' a unit trip with the unit restarted and resynchronised inside the same clock hour (the hourly mean dips,
            the hour stays a running hour; the governor counts the start);
    'line'  the station's 132 kV line breaker tripped and reclosed inside the hour: every unit generating at the station
            loses the grid for those minutes and is held at no load on its own breaker (no stop, no start).
    Every dipped hour keeps the unit at 60 per cent of rating or more, so no hour enters or leaves the restricted band,
    and no dip falls inside a winter valuation window. Returns the event list; `out` is dipped in place."""
    r = np.random.default_rng(TRIP_SEED)
    rm = np.random.default_rng(TRIP_SEED + RM_OFF)
    blocked = np.zeros(NH, bool)
    for (y, m, d) in VALUE_WINTERS:
        s = L(y, m, d)
        blocked[s:hidx(dt.datetime(y, m, d, tzinfo=OSLO) + dt.timedelta(weeks=14))] = True
    blocked[:72] = True
    blocked[-72:] = True
    ev = []
    on = {u: out[u] > 0 for u in UNITS}
    for u in UNITS:
        for f0 in sorted(forced.get(u, [])):
            if 0 < f0 < NH and on[u][f0 - 1] and not on[u][f0]:
                h1 = f0 + int(np.argmax(on[u][f0:])) if on[u][f0:].any() else None
                if h1 is None or h1 == f0:
                    continue
                h0 = f0 - 1
                v, rt = out[u][h0], RATED[u]
                band = lambda x: RZ_LO * rt - 1e-9 <= x < RZ_HI * rt - 1e-9
                last_min = h0 * 3600 + 3540 + int(r.integers(18, 58))
                tries = [h0 * 3600 + int(rm.integers(6, 58)) * 60 + int(rm.integers(0, 60)) for _ in range(8)]
                ok_t = [t for t in tries if not blocked[h0] and round(v * (t - h0 * 3600) / 3600.0, 2) > 0
                        and band(round(v * (t - h0 * 3600) / 3600.0, 2)) == band(v)]
                t0 = ok_t[0] if ok_t else last_min
                nv = round(v * (t0 - h0 * 3600) / 3600.0, 2)
                if ok_t:     # otherwise tripped in the hour's last minute, the mean left as recorded
                    out[u][h0] = nv
                t1 = h1 * 3600 + int(r.integers(70, 530))
                ev.append({'kind': 'long', 'unit': u, 'station': u[:3], 'h': f0 - 1, 't0': t0, 't1': t1})
    for u in UNITS:
        o = out[u]
        ok = (~blocked[1:-1]) & on[u][:-2] & on[u][1:-1] & on[u][2:] & (o[1:-1] >= 0.86 * RATED[u])
        cand = np.nonzero(ok)[0] + 1
        k = int(r.integers(5, 10))
        chosen = []
        for h in r.permutation(cand):
            if all(abs(int(h) - c) > 24 * 45 for c in chosen):
                chosen.append(int(h))
            if len(chosen) == k:
                break
        for h in sorted(chosen):
            d = int(r.integers(10, 19))
            m0 = int(r.integers(3, 60 - d - 2))
            o[h] = round(o[h] * (60 - d) / 60.0, 2)
            ev.append({'kind': 'quick', 'unit': u, 'station': u[:3], 'h': h, 't0': h * 3600 + m0 * 60 + int(r.integers(0, 60)),
                       't1': h * 3600 + (m0 + d) * 60 + int(r.integers(0, 60))})
    lo, hi = L(2018, 1, 1), L(2022, 1, 1)
    for st in ('OSD', 'SDL', 'NSV'):
        us = [u for u in UNITS if u[:3] == st]
        need_on = {u: 2 for u in us}
        need_off = {u: 1 for u in us}
        chosen = []
        for h in r.permutation(np.arange(lo, hi)):
            h = int(h)
            if blocked[h] or any(abs(h - c) < 24 * 60 for c in chosen):
                continue
            steady = all(on[u][h - 1] == on[u][h] == on[u][h + 1] for u in us)
            running = [u for u in us if on[u][h]]
            if not steady or not running or any(out[u][h] < 0.86 * RATED[u] for u in running):
                continue
            gain = sum(need_on[u] > 0 for u in running) + sum(need_off[u] > 0 for u in us if u not in running)
            if gain == 0 and len(chosen) >= 4:
                continue
            chosen.append(h)
            for u in us:
                if u in running:
                    need_on[u] -= 1
                else:
                    need_off[u] -= 1
            if len(chosen) >= 4 and all(v <= 0 for v in need_on.values()) and all(v <= 0 for v in need_off.values()):
                break
        for h in sorted(chosen):
            d = int(r.integers(6, 15))
            m0 = int(r.integers(4, 60 - d - 2))
            running = [u for u in us if on[u][h]]
            for u in running:
                out[u][h] = round(out[u][h] * (60 - d) / 60.0, 2)
            ev.append({'kind': 'line', 'unit': '', 'station': st, 'h': h, 'units': running,
                       't0': h * 3600 + m0 * 60 + int(r.integers(0, 60)), 't1': h * 3600 + (m0 + d) * 60 + int(r.integers(0, 60))})
    ev.sort(key=lambda e: (e['t0'], e['station'], e['unit']))
    return ev


def build():
    rng = np.random.default_rng(SEED)
    hours_local = [local(i) for i in range(NH)]
    month = np.array([h.month for h in hours_local]); year = np.array([h.year for h in hours_local])
    season_on = np.where(np.isin(month, [12, 1, 2, 3]), 1.0, np.where(np.isin(month, [5, 6]), 1.02,
                np.where(np.isin(month, [7, 8]), 0.84, 0.95)))
    fcr_i = hidx(FCR_FROM)
    out = {}
    avail = {}
    forced = {}
    annual = {u: [] for u in UNITS}
    for u in UNITS:
        a = np.ones(NH, bool)
        for (s, e) in OVERHAULS[u]:
            a[L(*s):L(*e)] = False
        for y in range(2016, 2027):        # annual maintenance, ten days in April or May
            d0 = dt.datetime(y, 4, 8, tzinfo=OSLO) + dt.timedelta(days=int(rng.integers(0, 35)))
            a[hidx(d0):hidx(d0) + 240] = False
            annual[u].append(d0.date())
            for _ in range(int(rng.integers(0, 3))):   # forced outages
                f0 = int(rng.integers(0, 8760 - 200)) + hidx(dt.datetime(y, 1, 1, tzinfo=OSLO))
                n = int(rng.integers(12, 120))
                a[f0:f0 + n] = False
                forced.setdefault(u, []).append(f0)
        avail[u] = a
        rz, low, pon = DUTY[u]
        on = np.zeros(NH, bool)
        if u == 'SDL-G3':
            state = False
            for i in range(NH):
                if not a[i]:
                    state = False
                elif state:
                    state = rng.random() > 1 / 4.0
                else:
                    state = rng.random() < (1 / 9.0) * season_on[i]
                on[i] = state
        else:
            state = True
            for i in range(NH):
                p = pon
                if u in FCR_UNITS and i >= fcr_i:
                    p = FCR_DUTY[u][2]
                if not a[i]:
                    state = False
                elif state:
                    state = rng.random() > (1 - min(0.999, p * season_on[i])) / 30.0
                else:
                    state = rng.random() < 1 / 18.0
                on[i] = state
        frac = np.zeros(NH)
        r = rng.random(NH)
        rzv = np.full(NH, rz); lowv = np.full(NH, low)
        if u in FCR_UNITS:
            rzv[fcr_i:] = FCR_DUTY[u][0]; lowv[fcr_i:] = FCR_DUTY[u][1]
        hi = rng.uniform(0.70, 1.00, NH) ** 0.6
        if u in FCR_UNITS:
            hi[fcr_i:] = rng.uniform(0.585, 0.78, NH - fcr_i)
        if u == 'SDL-G3':
            hi = rng.uniform(0.60, 0.92, NH)
        mid = rng.uniform(RZ_LO, RZ_HI, NH)
        lo = rng.uniform(0.10, 0.295, NH)
        frac = np.where(r < lowv, lo, np.where(r < lowv + rzv, mid, hi))
        mw = np.where(on, np.round(frac * RATED[u], 2), 0.0)
        mw = np.where((mw > 0) & (mw < 0.01), 0.01, mw)
        out[u] = mw
    out_plain = {u: out[u].copy() for u in UNITS}
    trips = trip_layer(out, forced)
    # runner occupancy by hour
    occ = {}
    for u in UNITS:
        arr = np.empty(NH, dtype=object)
        spans = RUNNER_IN[u]
        for k, (d0, rn) in enumerate(spans):
            s = L(*d0); e = L(*spans[k + 1][0]) if k + 1 < len(spans) else NH
            arr[s:e] = rn
        occ[u] = arr
    # pitting simulation
    inz = {u: (out[u] >= RZ_LO * RATED[u] - 1e-9) & (out[u] < RZ_HI * RATED[u] - 1e-9) for u in UNITS}
    pit = dict(PIT0)
    events = sorted([(L(*d), rn, u, rep) for (rn, d, u, rep) in INSPECTIONS])
    noise = {}
    found = []
    last_i = {rn: 0 for rn in PIT0}
    runner_rz = {rn: np.zeros(NH, bool) for rn in PIT0}
    for u in UNITS:
        for i in np.nonzero(inz[u])[0]:
            runner_rz[occ[u][i]][i] = True
    for (i, rn, u, rep) in events:
        f = rng.uniform(0.9995, 1.0005)
        add = K_Z * runner_rz[rn][last_i[rn]:i].sum() * f
        pit[rn] += add
        found.append({'runner': rn, 'i': i, 'unit': u, 'found': round(pit[rn], 1), 'repaired_to': rep})
        if rep is not None:
            pit[rn] = rep
        else:
            pit[rn] = round(pit[rn], 1)
        last_i[rn] = i
    # before the hourly record: hours, starts and rough-zone hours since each unit's last pre-period overhaul,
    # at the unit's 2016 duty, and the pre-period inspections made consistent with the pitting at 2016-01-01
    y16 = year == 2016
    pre = {}
    for u in UNITS:
        on = out[u] > 0
        st = np.zeros(NH, bool); st[1:] = on[1:] & ~on[:-1]
        frac = on[y16].sum() / y16.sum()
        span = (T0 - dt.datetime(*PRE_OVERHAUL_END[u], tzinfo=OSLO).astimezone(UTC)).total_seconds() / 3600
        h = int(round(frac * span))
        runs = max(1, st[y16].sum())
        pre[u] = {'hours': h, 'starts': int(round(h * runs / on[y16].sum())), 'rz': h * DUTY[u][0]}
    pre_insp = []
    for (rn, d, u, f, rep) in PRE_PERIOD_INSPECTIONS:
        inside = RUNNER_IN[u][0][1] == rn and (rn, d) == max(((r, dd) for (r, dd, uu, ff, rr) in PRE_PERIOD_INSPECTIONS
                                                                if r == rn), key=lambda t: t[1])
        grow = K_Z * pre[u]['rz'] if inside else 0.0
        start = round(PIT0[rn] - grow, 1)
        if rep is not None:
            pre_insp.append({'runner': rn, 'date': d, 'unit': u, 'found': f, 'repaired_to': start})
        else:
            pre_insp.append({'runner': rn, 'date': d, 'unit': u, 'found': start, 'repaired_to': None})
    return {'out': out, 'out_plain': out_plain, 'trips': trips, 'avail': avail, 'occ': occ, 'inz': inz, 'found': found, 'runner_rz': runner_rz,
            'year': year, 'hours_local': hours_local, 'pre': pre, 'pre_insp': pre_insp, 'annual': annual}


if __name__ == '__main__':
    W = build()
    for f in W['found']:
        print(f['runner'], local(f['i']).date(), f['unit'], f['found'], f['repaired_to'])
    for u in UNITS:
        o = W['out'][u]; on = o > 0
        print(u, 'run h/yr', round(on.sum() / 11), 'rz share', round(W['inz'][u].sum() / max(1, on.sum()), 3))
