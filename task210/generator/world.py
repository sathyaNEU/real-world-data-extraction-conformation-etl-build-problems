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
SALES_OFF = 1144    # January 2026 sales
PAYLOAD_OFF = 647    # month-to-month payload, apart from the haul's own draws
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


# road centrelines, (x, y, z) vertices; screening class per vertex-to-vertex segment as seen from MP1. The pit lies 250
# to 520 m south-west of the village edge; the primary hopper sits 192 m from MP1 on a bearing between the pit and the
# Phase 4 extension, behind the short screening bund on the plant compound's village side.
AXIS_DEG = 226.0
HOPPER = (round(192.0 * math.cos(math.radians(AXIS_DEG)), 1), round(192.0 * math.sin(math.radians(AXIS_DEG)), 1), 62.0)

ROADS = {
    'floor': {'name': 'Pit floor road', 'pts': [(-282.8, -366.8, 31), (-296.8, -313.6, 26), (-294.0, -263.2, 24)],
              'seg': ['pit', 'pit']},
    'ramp': {'name': 'Haul road 1', 'pts': [(-294.0, -263.2, 24), (-249.2, -291.2, 30), (-204.4, -254.8, 41),
                                            (-186.0, -196.0, 54), (-170.2, -176.5, 60), (-152.0, -157.5, 62), HOPPER],
             'seg': ['pit', 'pit', 'pit', 'pit', 'bund', 'plant']},
    'north_up': {'name': 'North face ramp', 'pts': [(-335.0, -145.0, 46), (-300.0, -135.0, 52), (-270.0, -131.0, 57),
                                                    (-251.5, -127.5, 60)], 'seg': ['crest', 'crest', 'crest']},
    'north': {'name': 'Haul road 2', 'pts': [(-251.5, -127.5, 60), (-225.0, -124.0, 62), (-195.0, -126.0, 62),
                                             (-165.0, -131.0, 62), (-146.8, -135.1, 62), HOPPER],
              'seg': ['open', 'open', 'open', 'open', 'plant']},
    'west_down': {'name': 'Bench ramp W', 'pts': [(-442.4, -235.2, 40), (-392.0, -254.8, 32), (-336.0, -263.2, 26),
                                                  (-294.0, -263.2, 24)], 'seg': ['pit', 'pit', 'pit']},
    'north_down': {'name': 'Bench ramp N', 'pts': [(-335.0, -145.0, 46), (-322.0, -184.8, 37), (-305.2, -229.6, 28),
                                                   (-294.0, -263.2, 24)], 'seg': ['pit', 'pit', 'pit']},
}
FACES = {'north': ROADS['north_up']['pts'][0], 'west': ROADS['west_down']['pts'][0], 'south': ROADS['floor']['pts'][0]}
STOCKPILE = ROADS['floor']['pts'][-1]


def _mirror(p):
    """Reflection about the bearing from MP1 through the hopper."""
    r = math.hypot(p[0], p[1]); a = math.degrees(math.atan2(p[1], p[0]))
    b = math.radians(2 * AXIS_DEG - a)
    return (r * math.cos(b), r * math.sin(b)) + tuple(p[2:])


# the Phase 4 extension (January 2027): its first bench is worked east of the existing pit; trucks climb the bench's
# access ramp and run north-west over the original ground to the primary hopper. The road was set out on the far side
# of the plant compound from Haul road 2, at the same distances from the village edge; the surveyed alignment carries
# the setting-out's own small departures from that line (offsets in metres, levels in m AOD).
EXT_SETOUT = [(0.0, 0.0, 60.0), (1.3, -0.9, 62.5), (-1.1, 1.2, 62.9), (0.8, 1.0, 62.7), (0.0, 0.0, 62.4), (0.0, 0.0, 62.0)]


def build_ext():
    base = [_mirror(p) for p in ROADS['north']['pts']]
    pts = []
    for (x, y, _z), (dx, dy, z) in zip(base, EXT_SETOUT):
        pts.append((round(x + dx, 1), round(y + dy, 1), z))
    pts[-1] = HOPPER
    up = []
    for (x, y, _z), (dx, dy, z) in zip((_mirror(p) for p in ROADS['north_up']['pts']), EXT_UP_SETOUT):
        up.append((round(x + dx, 1), round(y + dy, 1), z))
    up[-1] = pts[0]
    return ({'name': 'Phase 4 haul road', 'pts': pts, 'seg': list(ROADS['north']['seg'])},
            {'name': 'Bench 1 access ramp', 'pts': up, 'seg': ['crest', 'crest', 'crest']})


# the first bench is worked at 46 m AOD; its access ramp and its crest as set out (the crest is the existing pit's north
# edge seen from the far side of the plant, as the bench was laid out to hold the haul's distances)
EXT_UP_SETOUT = [(0.8, -0.6, 46.0), (-0.7, 0.9, 52.3), (0.6, 0.5, 56.8), (0.0, 0.0, 60.0)]
BENCH_CREST_SETOUT = [(-0.5, 0.7, 61.9), (0.9, 0.3, 62.0), (-0.3, -0.8, 62.2), (0.4, 0.6, 61.9), (-0.7, -0.2, 62.0)]


def pit_crest(step=15):
    """The pit crest as surveyed in April 2026: (x, y, level) every 15 degrees round the pit."""
    out = []
    for k in range(0, 361, step):
        a = math.radians(k)
        out.append((-300 + 160 * math.cos(a), -250 + 128 * math.sin(a), 62.0 - (1.4 if 200 < k < 300 else 0.0)))
    return out


def bench_crest():
    arc = [p for k, p in zip(range(0, 361, 15), pit_crest()) if 60 <= k <= 120]
    return [(round(x + dx, 1), round(y + dy, 1), z) for ((x, y, _z), (dx, dy, z)) in
            zip((_mirror(p) for p in arc), BENCH_CREST_SETOUT)]


ROADS['ext'], ROADS['ext_up'] = build_ext()
ROUTES = {
    ('south', 'crusher'): ['floor', 'ramp'], ('south', 'stock'): ['floor'],
    ('west', 'crusher'): ['west_down', 'ramp'], ('west', 'stock'): ['west_down'],
    ('north', 'crusher'): ['north_up', 'north'], ('north', 'stock'): ['north_down'],
}
EXT_ROUTE = ['ext_up', 'ext']
BUND = []
BUND_HALF = 10.0
for _off, _dr, _z in ((-BUND_HALF, 0.0, 67.3), (-BUND_HALF / 3, -1.5, 67.8), (BUND_HALF / 3, -1.5, 67.7), (BUND_HALF, 0.0, 67.4)):
    _a = math.radians(AXIS_DEG)
    BUND.append((round(170.0 * math.cos(_a) + _off * -math.sin(_a) + _dr * math.cos(_a), 1),
                 round(170.0 * math.sin(_a) + _off * math.cos(_a) + _dr * math.sin(_a), 1), _z))
# the plant compound behind the bund (corners as distance along the hopper's bearing and offset across it), and the
# consented Phase 4 extension east of the pit
PLANT_COMPOUND = [(round(al * math.cos(_a) - ac * math.sin(_a), 1), round(al * math.sin(_a) + ac * math.cos(_a), 1))
                  for (al, ac) in ((171.0, -36.0), (174.0, 37.0), (238.0, 44.0), (233.0, -41.0), (206.0, -46.0))]
PHASE4_AREA = [(-140.0, -215.0), (-95.0, -212.0), (-45.0, -260.0), (-32.0, -340.0), (-48.0, -440.0), (-150.0, -452.0),
               (-205.0, -372.0), (-170.0, -330.0), (-146.0, -290.0), (-138.0, -250.0)]


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


LWA_LOADED = 112.4   # sound power of a loaded ADT climbing out on the haul roads, dB


def params(seed):
    rng = np.random.default_rng(seed)
    P = dict(
        lwa_declared=109.0,
        lwa_loaded=float(rng.uniform(LWA_LOADED - 0.1, LWA_LOADED + 0.1)),     # loaded, climbing out on the haul roads
        lwa_empty=float(rng.uniform(105.8, 106.0)),      # empty return
        agr=float(rng.uniform(3.45, 3.55)), aatm=1.9,
        abar_open=float(rng.uniform(0.25, 0.35)), abar_crest=float(rng.uniform(5.5, 7.0)),
        abar_bund=float(rng.uniform(3.6, 4.8)), abar_pit=float(rng.uniform(7.2, 8.4)), abar_plant=float(rng.uniform(9.0, 10.5)),
        v_loaded=float(rng.uniform(17.8, 18.2)), v_empty=float(rng.uniform(28.2, 28.8)),
        plant_spec=37.5, plant_jitter=float(rng.uniform(0.6, 0.9)),
        wind_coef=float(rng.uniform(0.4, 0.6)),
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

DECLARED_LWA = {'Volvo A40G': 109, 'Cat 740 GC': 111, 'Bell B40E': 110}   # guaranteed LWA under 2000/14/EC, by model
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
    grng = np.random.default_rng(seed + 31)   # the fleet system's position scatter, apart from the haul's draws
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
                load_min = float(rng.uniform(2.4, 3.6)) + float(rng.uniform(4.0, 6.5))  # spotting and queueing at the face
                hh = (t.hour - 7) * 2 + t.minute // 30
                dest = 'crusher' if rng.random() < cs_walk[min(max(hh, 0), 21)] else 'stock'
                roads = ROUTES[(face, dest)]
                drive = sum(road_length(k) for k in roads)
                t_haul = drive / (P['v_loaded'] / 3.6) / 60 + float(rng.uniform(0.2, 0.5))
                t_tip = float(rng.uniform(0.8, 1.6)) + (float(rng.exponential(0.5)) + 0.2 if dest == 'crusher' else 0.5)
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
                # each road's passage is timed at the truck's arrival at the middle of that road
                done = 0.0
                for k in roads:
                    f_mid = (done + road_length(k) / 2) / drive
                    done += road_length(k)
                    mid_loaded = t_load_end + dt.timedelta(minutes=t_haul * f_mid)
                    mid_empty = t_tipped + dt.timedelta(minutes=t_ret * (1.0 - f_mid))
                    events.append((local_to_utc(mid_loaded), FLEET[ti][0], face, dest, k, 'loaded',
                                   sel[k][0] + float(rng.normal(0, 1.8))))
                    events.append((local_to_utc(mid_empty), FLEET[ti][0], face, dest, k, 'empty',
                                   sel[k][1] + float(rng.normal(0, 1.5))))
                # the payload sensor reads EMPTY from a quarter of a minute after arrival; the first fix after it is
                # the tip the fleet system shows (fixes fall on whole minutes)
                t_flip = (t_load_end + dt.timedelta(minutes=t_haul + 0.25)).replace(microsecond=0)
                if not t_flip.second:   # no fix logged on the change: the next minute's fix is the first EMPTY one
                    t_flip = t_flip + dt.timedelta(minutes=1)
                loads.append((local_to_utc(t_tipped), FLEET[ti][0], face, dest, payload, local_to_utc(t_flip)))
                if gps:
                    fixes.extend(_fixes(t, load_min, t_haul, t_tip, t_ret, roads, ti, face, grng))
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
            x, y, z, v, state = hx, hy, hz, 0.0, 'LOADED' if m < load_min + t_haul + 0.25 else 'EMPTY'
        else:
            f = (m - load_min - t_haul - t_tip) / t_ret
            x, y, z = _point_along(roads, f, reverse=True); v = float(rng.uniform(22, 34)); state = 'EMPTY'
        x += float(rng.normal(0, 2.5)); y += float(rng.normal(0, 2.5))
        out.append((local_to_utc(t), FLEET[ti][1], x, y, z + float(rng.normal(0, 3.5)), v, state))
        t += dt.timedelta(minutes=1)
    # the unit also logs a fix when the payload sensor changes state at the hopper
    tf = (t0 + dt.timedelta(minutes=load_min + t_haul + 0.25)).replace(microsecond=0)
    if tf.second and first <= tf < end:
        out.append((local_to_utc(tf), FLEET[ti][1], hx + float(rng.normal(0, 2.5)), hy + float(rng.normal(0, 2.5)),
                    hz + float(rng.normal(0, 3.5)), 0.0, 'EMPTY'))
        out.sort(key=lambda f: f[0])
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


RES_DAY = 37.9   # the village edge's daytime residual, before the morning and late-afternoon traffic


def filed_residual(mp1, ends):
    """The residual sound level at MP1 over weekdays 07:00 to 17:00 (energy mean of the clean residual, dB): what the
    noise management plan's site-stopped survey measured, the same process the pilot's record carries."""
    e = []
    for i, t in enumerate(ends):
        s = t - dt.timedelta(minutes=15)
        loc = s + dt.timedelta(hours=bst_offset(s))
        if loc.weekday() < 5 and 7 <= loc.hour < 17:
            e.append(10 ** (mp1['res'][i] / 10.0))
    return 10 * math.log10(float(np.mean(e)))


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
    base = np.where((loc_hour >= 6) & (loc_hour < 22), RES_DAY, 30.5) + np.where((loc_hour >= 7) & (loc_hour <= 8), 0.6, 0.0)
    base += np.where((loc_hour >= 16) & (loc_hour <= 18), 0.4, 0.0) - np.where(wkday >= 5, 0.4, 0.0)
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
    for (tu, truck, face, dest, payload, *_fl) in loads:
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
    weighed on the portable axle weigher; and the orders behind them. Account customers order a quantity and collect
    it in loads over the following days with their own lorries; cash customers buy a load at the office."""
    rng = np.random.default_rng(seed + SALES_OFF)
    accounts = [('C1043', 'Brackenridge Civils'), ('C1077', 'Holme & Pryor Ltd'), ('C1102', 'Wensdale Highways'),
                ('C1118', 'Thornber Groundworks'), ('C1135', 'Askrigg Building Supplies'), ('C1160', 'J. Metcalfe (Haulage)'),
                ('C1204', 'Leyburn Agricultural'), ('C1219', 'Pennine Surfacing')]
    acc_w = np.array([.15, .13, .18, .11, .10, .09, .08, .16]); acc_w = acc_w / acc_w.sum()
    regs = []
    for _ in range(64):
        regs.append('%s%02d %s' % (rng.choice(list('BDFGKLMNPRSVWY')) + rng.choice(list('ABCDEFGHJKLMNOPRSTVWXY')),
                                   int(rng.choice([18, 19, 20, 21, 22, 23, 24, 25, 68, 69, 70, 71, 72, 73, 74])),
                                   ''.join(rng.choice(list('ABCDEFGHJKLMNOPRSTUVWXYZ'), 3))))
    regs = sorted(set(regs))
    pool = [regs[i] for i in rng.permutation(len(regs))]
    fleet, i = {}, 0
    for (code, _n), k in zip(accounts, (6, 5, 7, 4, 3, 8, 2, 6)):
        fleet[code] = pool[i:i + k]; i += k
    walk_in = pool[i:]
    tare_of = {r: round(float(rng.uniform(13.1, 15.4)), 2) for r in regs}
    products = list(MIX)
    pmix = np.array([MIX[p] for p in products]); pmix = pmix / pmix.sum()
    QTY = [30, 50, 56, 60, 75, 80, 100, 100, 120, 140, 150, 150, 200, 250, 300, 400]
    orders, coll, open_orders = [], [], []
    onum = [25811]

    def new_order(acc, placed):
        onum[0] += int(rng.integers(1, 4))
        o = dict(order=onum[0], account=acc[0], customer=acc[1], product=products[rng.choice(len(products), p=pmix)],
                 qty=int(rng.choice(QTY)), placed=placed, delivery='Delivered' if rng.random() < 0.18 else 'Collected')
        o['left'] = float(o['qty'])
        orders.append(o)
        return o

    for _ in range(10):   # orders open over the New Year
        open_orders.append(new_order(accounts[rng.choice(len(accounts), p=acc_w)],
                                     dt.date(2025, 12, 1) + dt.timedelta(days=int(rng.integers(8, 23)))))
    d = dt.date(2026, 1, 2)
    while d <= dt.date(2026, 1, 31):
        if d.weekday() < 5 and d not in BANK_HOLIDAYS:
            portable = d in PORTABLE_DAYS
            n = int(rng.integers(36, 60)) if d.weekday() < 4 else int(rng.integers(28, 46))
            if portable:   # weighing axle by axle holds the gate to about half its usual run
                n = int(round(n * float(rng.uniform(0.40, 0.50))))
            last = {}
            for _ in range(n):
                if rng.random() < 0.11:   # a cash sale: a load ordered and paid for at the office
                    onum[0] += int(rng.integers(1, 3))
                    o = dict(order=onum[0], account='CASH', customer='Cash sales',
                             product=products[rng.choice(len(products), p=pmix)], qty=int(rng.choice([10, 20, 20, 25, 28, 30])),
                             placed=d, delivery='Collected', left=0.0)
                    orders.append(o)
                    reg = walk_in[int(rng.integers(0, len(walk_in)))]
                else:
                    if len(open_orders) < 9 or rng.random() < 0.16:
                        open_orders.append(new_order(accounts[rng.choice(len(accounts), p=acc_w)],
                                                     d - dt.timedelta(days=int(rng.integers(0, 6)))))
                    w = np.array([max(1.0, o['left'] / 28.0) for o in open_orders]); w = w / w.sum()
                    o = open_orders[int(rng.choice(len(open_orders), p=w))]
                    vs = fleet['C1160'] if o['delivery'] == 'Delivered' else fleet[o['account']]
                    reg = vs[int(rng.integers(0, len(vs)))]
                t = dt.datetime.combine(d, dt.time(7, 0)) + dt.timedelta(minutes=float(rng.uniform(0, 590)))
                for _try in range(6):   # a lorry is back for its next load an hour or more after its last
                    if all(abs((t - u).total_seconds()) >= 3600 for u in last.get(reg, [])):
                        break
                    t = dt.datetime.combine(d, dt.time(7, 0)) + dt.timedelta(minutes=float(rng.uniform(0, 590)))
                last.setdefault(reg, []).append(t)
                prod = o['product']
                if rng.random() < 0.075:   # changed at the gate: the lorry loads another product against the order
                    prod = products[int(rng.integers(0, len(products)))]
                net = round(float(np.clip(rng.normal(27.6 if prod not in ('Scalpings',) else 25.2, 1.7), 17.0, 31.5)), 2)
                tare = round(tare_of[reg] + float(rng.normal(0, 0.05)), 2)
                if portable:
                    net = round(round(net / 0.02) * 0.02, 2); tare = round(round(tare / 0.02) * 0.02, 2)
                coll.append(dict(order=o['order'], account=o['account'], product=prod, reg=reg, t=t, net=net, tare=tare,
                                 portable=portable))
                if o['account'] != 'CASH':
                    o['left'] -= net
                    if o['left'] < 12.0:
                        open_orders.remove(o)
        d += dt.timedelta(days=1)
    orders = [(o['order'], o['account'], o['customer'], o['product'], o['placed'], o['qty'], o['delivery']) for o in orders]
    import itertools
    # the office keys a lorry's portable runs on one order as one ticket, up to three runs a ticket in weighing order
    runs_of = {}
    for c in coll:
        if c['portable']:
            runs_of.setdefault((c['t'].date(), c['reg'], c['order']), []).append(c)
    for (day, reg, o), rs in runs_of.items():
        for j, c in enumerate(sorted(rs, key=lambda c: c['t'])):
            c['key'] = (day, reg, o, j // 3)
    # a ticket keyed from several runs sums to a figure no other runs of that lorry that day reach
    groups = {}
    for c in coll:
        if c['portable']:
            groups.setdefault((c['reg'], c['t'].date()), {}).setdefault(c['key'], []).append(c)
    for (reg, day), by_order in sorted(groups.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        runs = [c for o in sorted(by_order) for c in by_order[o]]
        for o in sorted(by_order):
            for it in range(400):
                own = by_order[o]
                target = round(sum(c['net'] for c in own), 2)
                clash = False
                for k in range(1, 4):
                    for sub in itertools.combinations(runs, k):
                        if set(map(id, sub)) != set(map(id, own)) and round(sum(c['net'] for c in sub), 2) == target:
                            clash = True
                if not clash:
                    break
                c = own[it % len(own)]   # turn about, so twin runs of equal weight are told apart
                c['net'] = round(c['net'] + 0.02, 2)
            else:
                raise RuntimeError('keyed tickets for %s on %s cannot be told apart' % (reg, day))
    # a lorry weighed on the weighbridge on the Monday after a portable day never shows the net of a portable
    # record (or of a vehicle's runs that day): two hundredths of a tonne either way would make it one
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
