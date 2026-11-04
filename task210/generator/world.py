"""task210 world: Ravensby Quarry (Calderwick Stone), May to October 2026, and the January 2027 extension haul.

Everything here is the clean truth: the haul cycles each truck ran, every passage's sound exposure at the
Ulverthorpe Lane monitor (MP1), the plant's feed and running, the weighbridge's January 2026 sales. pack.py writes
the bundle from it; golden.py reads only the bundle.
"""
import datetime as dt
import math
import numpy as np

SEED = 21038
PLANT_OFF = 204      # the plant's own draws (stops, interruptions, loader), apart from the haul's
SALES_OFF = 905    # January 2026 sales
PAYLOAD_OFF = 606    # month-to-month payload, apart from the haul's own draws
GMT = dt.timezone.utc

# ------------------------------------------------------------------------------------------------ calendar and clock

def bst_offset(t_utc):
    """UK clock: BST (UTC+1) from 01:00 UTC on the last Sunday of March to 01:00 UTC on the last Sunday of October."""
    y = t_utc.year
    def last_sunday(m):
        d = dt.datetime(y, m, 31 if m in (3, 10) else 30, 1, 0, tzinfo=GMT)
        while d.weekday() != 6:
            d -= dt.timedelta(days=1)
        return d
    return 1 if last_sunday(3) <= t_utc < last_sunday(10) else 0


def local_to_utc(t_local_naive):
    """Local wall-clock (naive) to aware UTC; the generator never builds a time inside the missing or doubled hour."""
    guess = t_local_naive.replace(tzinfo=GMT) - dt.timedelta(hours=1)
    off = bst_offset(guess)
    return t_local_naive.replace(tzinfo=GMT) - dt.timedelta(hours=off)


BANK_HOLIDAYS = {dt.date(2026, 5, 4), dt.date(2026, 5, 25), dt.date(2026, 8, 31), dt.date(2026, 1, 1)}
PILOT_START, PILOT_END = dt.date(2026, 5, 1), dt.date(2026, 10, 30)


def pilot_days():
    d, out = PILOT_START, []
    while d <= PILOT_END:
        if d.weekday() < 5 and d not in BANK_HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


# ---------------------------------------------------------------------------------------------------- the ground

# local grid in metres, x east and y north, origin at MP1 (Ulverthorpe Lane); levels in m AOD
MP1 = (0.0, 0.0, 58.0)
MP1_HEIGHT = 1.5
REF_LAT, REF_LON = 54.30418, -1.86217


def to_latlon(x, y):
    lat = REF_LAT + y / 111132.0
    lon = REF_LON + x / (111320.0 * math.cos(math.radians(REF_LAT)))
    return lat, lon


# road centrelines, (x, y, z) vertices; screening class per vertex-to-vertex segment as seen from MP1
SCALE = 0.56   # the pit lies 250 to 400 m south-west of the village edge


def _s(pts):
    return [(round(x * SCALE, 1), round(y * SCALE, 1), z) for (x, y, z) in pts]


ROADS = {
    'floor': {'name': 'Pit floor road', 'pts': _s([(-505, -655, 31), (-530, -560, 26), (-525, -470, 24)]),
              'seg': ['pit', 'pit']},
    'ramp': {'name': 'Haul road 1', 'pts': _s([(-525, -470, 24), (-445, -520, 30), (-365, -455, 41), (-338, -360, 51),
                                               (-345, -265, 59), (-322, -205, 62), (-300, -165, 62)]),
             'seg': ['pit', 'pit', 'pit', 'pit', 'bund', 'plant']},
    'north': {'name': 'Haul road 2', 'pts': _s([(-585, -245, 46), (-570, -185, 55), (-525, -150, 62), (-455, -128, 62),
                                                (-385, -118, 62), (-330, -128, 62), (-300, -165, 62)]),
              'seg': ['crest', 'open', 'open', 'open', 'open', 'plant']},
    'west_down': {'name': 'Bench ramp W', 'pts': _s([(-790, -420, 40), (-700, -455, 32), (-600, -470, 26),
                                                     (-525, -470, 24)]), 'seg': ['pit', 'pit', 'pit']},
    'north_down': {'name': 'Bench ramp N', 'pts': _s([(-585, -245, 46), (-575, -330, 37), (-545, -410, 28),
                                                      (-525, -470, 24)]), 'seg': ['pit', 'pit', 'pit']},
}
FACES = {'north': ROADS['north']['pts'][0], 'west': ROADS['west_down']['pts'][0], 'south': ROADS['floor']['pts'][0]}
HOPPER = ROADS['ramp']['pts'][-1]
STOCKPILE = ROADS['floor']['pts'][-1]
EXT_TWEAK = 1.16
_np = ROADS['north']['pts']


def build_ext(f):
    """The eastern extension's road (January 2027): it climbs out of the first bench and runs north over the original
    ground to the plant; its alignment holds Haul road 2's distances from the village edge (f fine-tunes them)."""
    pts = [(round((_np[0][1] + 6.0) * f, 1), round((_np[0][0] - 4.0) * f, 1), 50)]
    pts += [(round((y + 3.0) * f, 1), round((x - 2.0) * f, 1), 63) for (x, y, z) in _np[1:-1]]
    pts.append((round(HOPPER[0] + 22.0, 1), round(HOPPER[1] - 40.0, 1), 62))
    pts.append(HOPPER)
    return {'name': 'Phase 4 haul road', 'pts': pts, 'seg': ['crest', 'open', 'open', 'open', 'open', 'plant', 'plant']}


ROADS['ext'] = build_ext(EXT_TWEAK)
ROUTES = {
    ('south', 'crusher'): ['floor', 'ramp'], ('south', 'stock'): ['floor'],
    ('west', 'crusher'): ['west_down', 'ramp'], ('west', 'stock'): ['west_down'],
    ('north', 'crusher'): ['north'], ('north', 'stock'): ['north_down'],
}


def road_length(key):
    p = ROADS[key]['pts']
    return sum(math.dist(p[i][:2], p[i + 1][:2]) for i in range(len(p) - 1))


# --------------------------------------------------------------------------------------------- physics at MP1

def attenuation(x, y, z, cls, P):
    """dB from LWA to the A-weighted pressure at MP1 for a source at (x, y, z) in screening class cls."""
    r = math.sqrt(x * x + y * y + (z - MP1[2] - MP1_HEIGHT) ** 2)
    a = 20 * math.log10(r) + 8.0 + P['agr'] + P['aatm'] * r / 1000.0
    a += {'open': P['abar_open'], 'crest': P['abar_crest'], 'bund': P['abar_bund'], 'pit': P['abar_pit'],
          'plant': P['abar_plant']}[cls]
    return a


def passage_geometry(key, P, speed_kmh):
    """10log10 of the time-integrated transfer (seconds) for one passage of the whole road at a speed: the SEL of a
    passage is LWA minus this attenuation term plus this time term; computed at 5 m steps."""
    pts = ROADS[key]['pts']; seg = ROADS[key]['seg']
    v = speed_kmh / 3.6
    acc = 0.0
    for i in range(len(pts) - 1):
        (x0, y0, z0), (x1, y1, z1) = pts[i], pts[i + 1]
        L = math.dist((x0, y0), (x1, y1)); n = max(1, int(L / 5.0))
        for k in range(n):
            f = (k + 0.5) / n
            x, y, z = x0 + f * (x1 - x0), y0 + f * (y1 - y0), z0 + f * (z1 - z0)
            acc += 10 ** (-attenuation(x, y, z, seg[i], P) / 10.0) * (L / n) / v
    return 10 * math.log10(acc)


def params(seed):
    rng = np.random.default_rng(seed)
    P = dict(
        lwa_declared=109.0,
        lwa_loaded=float(rng.uniform(111.6, 112.4)),     # loaded, climbing out on the haul roads
        lwa_empty=float(rng.uniform(105.5, 106.3)),      # empty return
        agr=float(rng.uniform(3.2, 3.8)), aatm=1.9,
        abar_open=float(rng.uniform(0.0, 0.6)), abar_crest=float(rng.uniform(5.5, 7.0)),
        abar_bund=float(rng.uniform(3.6, 4.8)), abar_pit=float(rng.uniform(7.2, 8.4)), abar_plant=float(rng.uniform(9.0, 10.5)),
        v_loaded=float(rng.uniform(17.0, 19.0)), v_empty=float(rng.uniform(27.0, 30.0)),
        plant_spec=37.5, plant_jitter=float(rng.uniform(0.6, 0.9)),
        wind_coef=float(rng.uniform(0.7, 1.0)),
        crusher_share=float(rng.uniform(0.58, 0.66)),
        payload_mean=float(rng.uniform(35.2, 36.4)),
    )
    # month to month the loads vary with fragmentation from the month's blasts and with floor conditions
    P['month_payload'] = {m: float(rng.uniform(-1.6, 1.6)) for m in range(1, 13)}
    prng = np.random.default_rng(seed + PAYLOAD_OFF)
    for m in P['month_payload']:
        P['month_payload'][m] += float(prng.uniform(-0.3, 0.3))
    return P


def passage_sel(P):
    """Mean SEL (dB re 1 s) at MP1 of one loaded passage and one empty passage of each road."""
    out = {}
    for key in ROADS:
        out[key] = (P['lwa_loaded'] + passage_geometry(key, P, P['v_loaded']),
                    P['lwa_empty'] + passage_geometry(key, P, P['v_empty']))
    return out


# --------------------------------------------------------------------------------------------- the haul record

FLEET = [  # fleet number, telematics unit, model
    ('T27', 'AX4-60117', 'Volvo A40G'), ('T31', 'AX4-60348', 'Volvo A40G'), ('T33', 'AX4-61902', 'Cat 740 GC'),
    ('T38', 'AX4-61477', 'Volvo A40G'), ('T41', 'AX4-62235', 'Cat 740 GC'), ('T44', 'AX4-60869', 'Volvo A40G'),
    ('T52', 'AX4-63081', 'Bell B40E'),
]


def day_faces(rng):
    u = rng.random()
    if u < 0.40:
        return ('south', 'north')
    if u < 0.70:
        return ('south', 'west')
    if u < 0.86:
        return ('west', 'north')
    return ('south', 'south')


def simulate_haul(seed, P, days=None, gps=True, outage=None):
    """Return the haul events and, when gps, the one-minute fixes. Each event is one loaded or empty passage of one
    road with its UTC midpoint, truck, face, destination and SEL at MP1."""
    rng = np.random.default_rng(seed + 1)
    days = days or pilot_days()
    sel = passage_sel(P)
    events, fixes, loads, day_rows = [], [], [], []
    for d in days:
        faces = day_faces(rng)
        n_trucks = int(rng.choice([3, 4, 5, 6, 7], p=[0.06, 0.14, 0.25, 0.30, 0.25]))
        trucks = sorted(rng.choice(len(FLEET), n_trucks, replace=False))
        # one loader at each face: the north bench, the narrowest, takes one or two trucks
        if faces[0] == faces[1]:
            k0 = n_trucks
        elif faces[1] == 'north':
            k0 = n_trucks - int(rng.integers(1, min(2, n_trucks - 1) + 1))
        else:
            k0 = int(rng.integers(1, n_trucks))
        order = rng.permutation(n_trucks)
        assign = {trucks[i]: (faces[0] if j < k0 else faces[1]) for j, i in enumerate(order)}
        # a truck off the haul for half a shift (service, tyres) and, some days, the haul stood down for rain
        off = {}
        for i in trucks:
            if rng.random() < 0.07:
                off[i] = 'am' if rng.random() < 0.5 else 'pm'
        sd = None
        if rng.random() < 0.09:
            s0 = dt.datetime.combine(d, dt.time(9, 0)) + dt.timedelta(minutes=float(rng.uniform(0, 330)))
            s0 = s0.replace(second=0, microsecond=0)
            sd = (s0, s0 + dt.timedelta(minutes=int(rng.integers(80, 190))))
        # crusher share by half hour, a slow walk through the shift
        cs_walk = np.clip(P['crusher_share'] + np.cumsum(rng.normal(0, 0.06, 22)), 0.30, 0.90)
        day_rows.append((d, faces, [FLEET[i][0] for i in trucks], {FLEET[i][0]: v for i, v in off.items()}, sd))
        for ti in trucks:
            face = assign[ti]
            t = dt.datetime.combine(d, dt.time(7, 0)) + dt.timedelta(minutes=float(rng.uniform(0, 6)))
            stop = dt.datetime.combine(d, dt.time(17, 0))
            if off.get(ti) == 'am':
                t = dt.datetime.combine(d, dt.time(12, 30)) + dt.timedelta(minutes=float(rng.uniform(5, 25)))
            elif off.get(ti) == 'pm':
                stop = dt.datetime.combine(d, dt.time(12, 0))
            lunch0, lunch1 = dt.datetime.combine(d, dt.time(12, 0)), dt.datetime.combine(d, dt.time(12, 30))
            while True:
                if lunch0 <= t < lunch1:
                    t = lunch1 + dt.timedelta(minutes=float(rng.uniform(0, 3)))
                if sd and sd[0] <= t < sd[1]:
                    t = sd[1] + dt.timedelta(minutes=float(rng.uniform(0, 6)))
                load_min = float(rng.uniform(2.4, 3.6)) + float(rng.uniform(2.5, 5.0))  # spotting and queueing at the face
                hh = (t.hour - 7) * 2 + t.minute // 30
                dest = 'crusher' if rng.random() < cs_walk[min(max(hh, 0), 21)] else 'stock'
                roads = ROUTES[(face, dest)]
                drive = sum(road_length(k) for k in roads)
                t_haul = drive / (P['v_loaded'] / 3.6) / 60 + float(rng.uniform(0.3, 1.0))
                t_tip = float(rng.uniform(0.8, 1.6)) + (float(rng.exponential(1.6)) + 1.5 if dest == 'crusher' else 0.5)
                t_ret = drive / (P['v_empty'] / 3.6) / 60 + float(rng.uniform(0.3, 0.8))
                end = t + dt.timedelta(minutes=load_min + t_haul + t_tip + t_ret)
                if t < lunch0 < end and stop > lunch1:
                    t = lunch1 + dt.timedelta(minutes=float(rng.uniform(0, 3)))
                    continue
                if end > stop:
                    break
                t_load_end = t + dt.timedelta(minutes=load_min)
                t_tipped = t_load_end + dt.timedelta(minutes=t_haul + t_tip)
                payload = float(rng.normal(P['payload_mean'] + P['month_payload'][d.month] + {'north': -1.3, 'west': 1.6, 'south': 0.0}[face], 1.5))
                mid_loaded = t_load_end + dt.timedelta(minutes=t_haul / 2)
                mid_empty = t_tipped + dt.timedelta(minutes=t_ret / 2)
                for k in roads:
                    events.append((local_to_utc(mid_loaded), FLEET[ti][0], face, dest, k, 'loaded',
                                   sel[k][0] + float(rng.normal(0, 1.8))))
                    events.append((local_to_utc(mid_empty), FLEET[ti][0], face, dest, k, 'empty',
                                   sel[k][1] + float(rng.normal(0, 1.5))))
                loads.append((local_to_utc(t_tipped), FLEET[ti][0], face, dest, payload))
                if gps:
                    fixes.extend(_fixes(t, load_min, t_haul, t_tip, t_ret, roads, ti, face, rng))
                t = end
    return events, fixes, loads, day_rows


def _point_along(roads, frac, reverse=False):
    pts = []
    for k in roads:
        p = ROADS[k]['pts']
        pts.extend(p if not pts else p[1:])
    if reverse:
        pts = pts[::-1]
    seglen = [math.dist(pts[i][:2], pts[i + 1][:2]) for i in range(len(pts) - 1)]
    tot = sum(seglen); target = frac * tot
    for i, L in enumerate(seglen):
        if target <= L or i == len(seglen) - 1:
            f = min(1.0, target / L) if L else 0.0
            a, b = pts[i], pts[i + 1]
            return tuple(a[j] + f * (b[j] - a[j]) for j in range(3))
        target -= L


def _fixes(t0, load_min, t_haul, t_tip, t_ret, roads, ti, face, rng):
    """One fix per whole minute of the cycle: position, level, speed and payload state."""
    out = []
    tot = load_min + t_haul + t_tip + t_ret
    first = (t0 + dt.timedelta(minutes=1)).replace(second=0, microsecond=0)
    t = first
    end = t0 + dt.timedelta(minutes=tot)
    fx, fy, fz = FACES[face]
    hx, hy, hz = _point_along(roads, 1.0)
    while t < end:
        m = (t - t0).total_seconds() / 60.0
        if m < load_min:
            x, y, z, v, state = fx, fy, fz, 0.0, 'EMPTY'
        elif m < load_min + t_haul:
            f = (m - load_min) / t_haul
            x, y, z = _point_along(roads, f); v = float(rng.uniform(14, 22)); state = 'LOADED'
        elif m < load_min + t_haul + t_tip:
            x, y, z, v, state = hx, hy, hz, 0.0, 'LOADED' if m < load_min + t_haul + 0.4 else 'EMPTY'
        else:
            f = (m - load_min - t_haul - t_tip) / t_ret
            x, y, z = _point_along(roads, f, reverse=True); v = float(rng.uniform(22, 34)); state = 'EMPTY'
        x += float(rng.normal(0, 2.5)); y += float(rng.normal(0, 2.5))
        out.append((local_to_utc(t), FLEET[ti][1], x, y, z + float(rng.normal(0, 3.5)), v, state))
        t += dt.timedelta(minutes=1)
    return out


# ----------------------------------------------------------------------------------------------- MP1 and weather

def period_ends(start=dt.datetime(2026, 5, 1, 0, 15, tzinfo=GMT), end=dt.datetime(2026, 11, 1, 0, 0, tzinfo=GMT)):
    out, t = [], start
    while t <= end:
        out.append(t)
        t += dt.timedelta(minutes=15)
    return out


def weather(seed, ends):
    """Hourly wind component toward MP1 from the working area (m/s) and the 10-minute station record."""
    rng = np.random.default_rng(seed + 2)
    hours = len(ends) // 4 + 2
    ws = np.clip(3.8 + np.cumsum(rng.normal(0, 0.35, hours)) * 0.15 + rng.normal(0, 1.2, hours), 0.3, 14)
    wd = (225 + np.cumsum(rng.normal(0, 18, hours))) % 360
    return ws, wd


def wind_toward(ws, wd):
    # bearing from the working area to MP1 is about 45 degrees; wind FROM 225 blows toward MP1
    return ws * np.cos(np.radians(wd - 225.0))


def mp1_record(seed, P, events, ends, ws, wd, plant_running):
    """15-minute LAeq, LA90, LA10, LAFmax at MP1 (period ending, UTC)."""
    rng = np.random.default_rng(seed + 3)
    n = len(ends)
    idx0 = ends[0] - dt.timedelta(minutes=15)
    E = np.zeros(n); Lmax_ev = np.full(n, -99.0)
    hour_i = np.array([int((e - idx0).total_seconds() // 3600) for e in ends])
    wcomp = wind_toward(ws[hour_i], wd[hour_i])
    wind_db = P['wind_coef'] * np.tanh(wcomp / 3.0)
    for (t, truck, face, dest, road, state, s) in events:
        k = int((t - idx0).total_seconds() // 900)
        if 0 <= k < n:
            e = 10 ** ((s + wind_db[k]) / 10.0)
            E[k] += e
            Lmax_ev[k] = max(Lmax_ev[k], s + wind_db[k] - 10 * math.log10(55.0) + float(rng.normal(3.0, 1.0)))
    loc_hour = np.array([(e - dt.timedelta(minutes=15) + dt.timedelta(hours=bst_offset(e))).hour for e in ends])
    wkday = np.array([(e - dt.timedelta(minutes=15) + dt.timedelta(hours=bst_offset(e))).weekday() for e in ends])
    base = np.where((loc_hour >= 6) & (loc_hour < 22), 37.2, 30.5) + np.where((loc_hour >= 7) & (loc_hour <= 9), 1.8, 0.0)
    base += np.where((loc_hour >= 16) & (loc_hour <= 18), 1.5, 0.0) - np.where(wkday >= 5, 1.2, 0.0)
    res = base + 0.35 * np.maximum(ws[hour_i] - 4, 0) + rng.normal(0, 1.4, n)
    E_res = 10 ** (res / 10.0) * 900
    plant = np.where(plant_running, 10 ** ((P['plant_spec'] + 0.5 * wind_db + rng.normal(0, P['plant_jitter'], n)) / 10.0) * 900, 0.0)
    tot = E * 1.0 + E_res + plant
    laeq = 10 * np.log10(tot / 900.0)
    la90 = 10 * np.log10((10 ** ((res - 4.6 + rng.normal(0, 0.6, n)) / 10.0)) + np.where(plant_running, 10 ** ((P['plant_spec'] - 1.2) / 10.0), 0.0))
    la10 = laeq + rng.uniform(1.0, 2.6, n) + np.where(E > 0, 0.6, 0.0)
    lmax = np.maximum(laeq + rng.uniform(6, 14, n), Lmax_ev)
    return dict(laeq=laeq, la90=np.minimum(la90, laeq - 0.4), la10=la10, lamax=lmax, haul_energy=E, wind_db=wind_db,
                res=res)


# ----------------------------------------------------------------------------------------- the plant (ask rows)

def plant_records(seed, P, loads, days, standdowns=None):
    """Crusher run events (PLC), supply interruptions, belt weigher 15-minute tonnes, loader buckets."""
    rng = np.random.default_rng(seed + PLANT_OFF)
    lrng = np.random.default_rng(seed + PLANT_OFF + 7)   # bucket spacing at the lorries, apart from the plant's draws
    run_ev, outages, belt, buckets = [], [], [], []
    running = {}  # local minute -> running flag, built per day
    loads_by_day = {}
    for (tu, truck, face, dest, payload) in loads:
        tl = tu + dt.timedelta(hours=bst_offset(tu))
        loads_by_day.setdefault(tl.date(), []).append((tl.replace(tzinfo=None), truck, dest, payload))
    order_no = 4410
    by_month = {}
    for d in days:
        by_month.setdefault((d.year, d.month), []).append(d)
    cut_days = set()
    for k in sorted(by_month):
        ds = by_month[k]
        for i in rng.choice(len(ds), int(rng.integers(1, 4)), replace=False):
            cut_days.add(ds[int(i)])
    for d in days:
        start = dt.datetime.combine(d, dt.time(6, 40)) + dt.timedelta(minutes=float(rng.uniform(0, 10)))
        stop = dt.datetime.combine(d, dt.time(17, 25)) + dt.timedelta(minutes=float(rng.uniform(0, 12)))
        runs = [(start, stop)]
        # a mechanical stop most weeks
        if rng.random() < 0.22:
            s0 = start + dt.timedelta(minutes=float(rng.uniform(90, 500)))
            s1 = s0 + dt.timedelta(minutes=float(rng.uniform(12, 55)))
            runs = [(start, s0), (s1, stop)]
        # a supply interruption on some days: the PLC loses power with the crusher and logs its stop on the supply's return
        cut = None
        if d in cut_days:
            c0 = start + dt.timedelta(minutes=float(rng.uniform(60, 520)))
            c1 = c0 + dt.timedelta(minutes=float(rng.uniform(25, 140)))
            if c1 < stop - dt.timedelta(minutes=30):
                cut = (c0, c1)
        segs = []
        for (a, b) in runs:
            if cut and a < cut[0] < b:
                restart = cut[1] + dt.timedelta(minutes=float(rng.uniform(6, 18)))
                segs.append((a, cut[0], False))          # ended by the interruption, no stop logged
                if restart < b:
                    segs.append((restart, b, True))
            else:
                segs.append((a, b, True))
        if cut:
            outages.append((cut[0], cut[1]))
        for (a, b, logged) in segs:
            run_ev.append((a, 'START'))
            if logged:
                run_ev.append((b, 'STOP'))
            else:   # the controller writes the stop it missed when it boots on the supply's return
                run_ev.append((cut[1] + dt.timedelta(seconds=int(rng.integers(40, 95))), 'STOP'))
        running[d] = [(a, b) for (a, b, _) in segs]
        # belt tonnes: haul tips to the crusher land on the belt while it runs; tips while stopped wait in the hopper
        tips = [l for l in loads_by_day.get(d, []) if l[2] == 'crusher']
        bins = {}
        def run_at(t):
            for (a, b) in running[d]:
                if a <= t < b:
                    return True
            return False
        for (tl, truck, dest, payload) in tips:
            tb = tl + dt.timedelta(minutes=2)
            while not run_at(tb) and tb < dt.datetime.combine(d, dt.time(18, 30)):
                tb += dt.timedelta(minutes=5)
            key = tb.replace(minute=(tb.minute // 15) * 15, second=0, microsecond=0)
            bins[key] = bins.get(key, 0.0) + payload
        # reclaim sessions: the loader feeds the primary hopper from the run-of-mine stockpile when the haul is short
        sess = []
        for _ in range(rng.poisson(0.55)):
            sess.append((dt.datetime.combine(d, dt.time(7, 30)) + dt.timedelta(minutes=float(rng.uniform(0, 520))),
                         float(rng.uniform(25, 85))))
        if standdowns and standdowns.get(d):
            a, b = standdowns[d]
            s_a = a + dt.timedelta(minutes=float(rng.uniform(6, 20)))
            sess.append((s_a, (b - s_a).total_seconds() / 60.0 - float(rng.uniform(0, 10))))
        for (s0, dur) in sess:
            t = s0
            while t < s0 + dt.timedelta(minutes=dur):
                if run_at(t) and not (dt.time(11, 55) <= t.time() < dt.time(12, 40)) and t.time() < dt.time(16, 58):
                    w = float(rng.normal(7.4, 0.6))
                    buckets.append((t, round(w, 2), ''))
                    tb = t + dt.timedelta(minutes=1)
                    key = tb.replace(minute=(tb.minute // 15) * 15, second=0, microsecond=0)
                    bins[key] = bins.get(key, 0.0) + w
                t += dt.timedelta(seconds=float(rng.uniform(70, 110)))
        # re-handling at the stockpile over the haul's lunch break, while the primary idles; and through an outage
        if rng.random() < 0.7 and run_at(dt.datetime.combine(d, dt.time(11, 40))) and run_at(dt.datetime.combine(d, dt.time(12, 50))) \
                and all(run_at(dt.datetime.combine(d, dt.time(11, 40)) + dt.timedelta(minutes=m)) for m in range(0, 71, 5)):
            t = dt.datetime.combine(d, dt.time(12, 15)) + dt.timedelta(seconds=float(rng.uniform(20, 120)))
            while t < dt.datetime.combine(d, dt.time(12, 29)):
                buckets.append((t, round(float(rng.normal(7.6, 0.6)), 2), ''))
                t += dt.timedelta(seconds=float(rng.uniform(75, 120)))
        if cut:
            t = cut[0] + dt.timedelta(minutes=float(rng.uniform(8, 20)))
            while t < cut[1] - dt.timedelta(minutes=3):
                buckets.append((t, round(float(rng.normal(7.6, 0.6)), 2), ''))
                t += dt.timedelta(seconds=float(rng.uniform(80, 140)))
        # the haul stops at five; the loader goes back to the stockpile while the primary runs the hopper down
        if rng.random() < 0.6 and run_at(dt.datetime.combine(d, dt.time(17, 22))):
            t = dt.datetime.combine(d, dt.time(17, 16)) + dt.timedelta(seconds=float(rng.uniform(10, 90)))
            while run_at(t):
                buckets.append((t, round(float(rng.normal(7.6, 0.6)), 2), ''))
                t += dt.timedelta(seconds=float(rng.uniform(75, 120)))
        # re-handling after the crusher stops: stockpile to stockpile, no belt
        if rng.random() < 0.45:
            t = stop + dt.timedelta(minutes=float(rng.uniform(22, 40)))
            for _ in range(int(rng.integers(6, 22))):
                buckets.append((t, round(float(rng.normal(7.6, 0.6)), 2), ''))
                t += dt.timedelta(seconds=float(rng.uniform(75, 120)))
        # lorry loading from the product stockpiles through the day (ticketed)
        for _ in range(int(rng.integers(18, 40))):
            t = dt.datetime.combine(d, dt.time(7, 0)) + dt.timedelta(minutes=float(rng.uniform(0, 600)))
            order_no += int(rng.integers(1, 5))
            for b in range(int(rng.integers(3, 5))):
                buckets.append((t + dt.timedelta(seconds=float(65 + 25 * b + lrng.uniform(0, 20) * b)),
                                round(float(rng.normal(7.3, 0.5)), 2), 'SO%06d' % (order_no + 30200)))
        for k in sorted(bins):
            belt.append((k, bins[k]))
    return run_ev, outages, belt, sorted(buckets), running


# -------------------------------------------------------------------------------------- January 2026 sales (ask rows)

PRODUCTS_OLD = {  # code in force until the June 2026 system change -> product
    '101': '6F2 capping', '104': 'Type 1 sub-base', '112': '40 mm clean', '115': '20 mm clean', '118': '10 mm clean',
    '130': '0-4 mm dust', '140': 'Scalpings'}
PRODUCTS_NEW = {  # the current product list, from 1 June 2026
    '101': 'Type 1 sub-base', '104': '10 mm clean', '112': '20 mm clean', '115': '6F2 capping', '118': 'Scalpings',
    '130': '40 mm clean', '140': '0-4 mm dust'}
PRICE_JAN = {'6F2 capping': 9.85, 'Type 1 sub-base': 13.40, '40 mm clean': 15.20, '20 mm clean': 16.75,
             '10 mm clean': 17.90, '0-4 mm dust': 8.60, 'Scalpings': 6.95}
MIX = {'6F2 capping': 0.12, 'Type 1 sub-base': 0.31, '40 mm clean': 0.09, '20 mm clean': 0.17, '10 mm clean': 0.10,
       '0-4 mm dust': 0.13, 'Scalpings': 0.08}
PORTABLE_DAYS = [dt.date(2026, 1, 2), dt.date(2026, 1, 6), dt.date(2026, 1, 15), dt.date(2026, 1, 21)]


def january_sales(seed):
    """Every collection weighed in January 2026: order, product, vehicle, weigh time, net tonnes; whether it was
    weighed on the portable axle weigher; and the orders behind them."""
    rng = np.random.default_rng(seed + SALES_OFF)
    accounts = [('C1043', 'Brackenridge Civils'), ('C1077', 'Holme & Pryor Ltd'), ('C1102', 'Wensdale Highways'),
                ('C1118', 'Thornber Groundworks'), ('C1135', 'Askrigg Building Supplies'), ('C1160', 'J. Metcalfe (Haulage)'),
                ('C1204', 'Leyburn Agricultural'), ('C1219', 'Pennine Surfacing'), ('CASH', 'Cash sales')]
    regs = []
    for _ in range(64):
        regs.append('%s%02d %s' % (rng.choice(list('BDFGKLMNPRSVWY')) + rng.choice(list('ABCDEFGHJKLMNOPRSTVWXY')),
                                   int(rng.choice([18, 19, 20, 21, 22, 23, 24, 25, 68, 69, 70, 71, 72, 73, 74])),
                                   ''.join(rng.choice(list('ABCDEFGHJKLMNOPRSTUVWXYZ'), 3))))
    regs = sorted(set(regs))
    products = list(MIX)
    pmix = np.array([MIX[p] for p in products]); pmix = pmix / pmix.sum()
    orders, coll = [], []
    onum = 25811
    d = dt.date(2026, 1, 2)
    while d <= dt.date(2026, 1, 31):
        if d.weekday() < 5 and d not in BANK_HOLIDAYS:
            n = int(rng.integers(34, 58)) if d.weekday() < 4 else int(rng.integers(26, 44))
            for _ in range(n):
                prod = products[rng.choice(len(products), p=pmix)]
                acc = accounts[rng.choice(len(accounts), p=[.14, .12, .16, .10, .09, .08, .07, .14, .10])]
                onum += int(rng.integers(1, 4))
                reg = regs[int(rng.integers(0, len(regs)))]
                t = dt.datetime.combine(d, dt.time(7, 0)) + dt.timedelta(minutes=float(rng.uniform(0, 590)))
                net = round(float(np.clip(rng.normal(27.6 if prod not in ('Scalpings',) else 25.2, 1.7), 17.0, 31.5)), 2)
                tare = round(float(rng.uniform(13.1, 15.4)), 2)
                portable = d in PORTABLE_DAYS
                if portable:
                    net = round(round(net / 0.02) * 0.02, 2); tare = round(round(tare / 0.02) * 0.02, 2)
                ordered = prod
                if rng.random() < 0.075:   # changed at the gate: the lorry loads another product against the order
                    ordered = products[int(rng.integers(0, len(products)))]
                orders.append((onum, acc[0], acc[1], ordered, d - dt.timedelta(days=int(rng.integers(0, 6)))))
                coll.append(dict(order=onum, account=acc[0], product=prod, reg=reg, t=t, net=net, tare=tare,
                                 portable=portable))
                if portable and rng.random() < 0.3 and t.hour < 14:
                    for k in range(int(rng.integers(1, 3))):
                        t2 = t + dt.timedelta(minutes=float(rng.uniform(75, 140)) * (k + 1))
                        n2 = round(round(float(np.clip(rng.normal(27.6, 1.7), 17.0, 31.5)) / 0.02) * 0.02, 2)
                        coll.append(dict(order=onum, account=acc[0], product=prod, reg=reg, t=t2, net=n2, tare=tare,
                                         portable=True))
        d += dt.timedelta(days=1)
    # a lorry weighed on the weighbridge on the Monday after a portable day never shows the net of a portable
    # record (or of a vehicle's runs that day): two hundredths of a tonne either way would make it one
    import itertools
    port = {}
    for c in coll:
        if c['portable']:
            port.setdefault((c['reg'], c['t'].date()), []).append(round(c['net'], 2))
    for c in coll:
        if c['portable'] or c['t'].weekday() != 0:
            continue
        while True:
            sums = set()
            for (reg, pd_), nets in port.items():
                if reg == c['reg'] and 0 < (c['t'].date() - pd_).days <= 7:
                    for k in range(1, 4):
                        for sub in itertools.combinations(nets, k):
                            sums.add(round(sum(sub), 2))
            if round(c['net'], 2) not in sums:
                break
            c['net'] = round(c['net'] + 0.01, 2)
    return coll, orders
