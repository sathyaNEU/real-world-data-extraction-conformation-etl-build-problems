"""The records: two years of valley weather, long-distance trips and their fast-charging sessions on the
corridor sites, and the remote sites' local sessions and charger status for Support Year 2.

Every session is generated from a simulated trip: a car leaves home charged, drives the route stretch by
stretch at the energy the day's weather and the stretch's own exposure cost it, and stops at a fast charger
when its planner says the next leg needs more than it has. Cars whose next leg cannot be done even from a
full battery do not make the trip by electric car, so the record only holds crossings that were possible.
"""
import datetime as dt
import math
import numpy as np
import world as W
import routes as R

RNG = np.random.default_rng(W.SEED)
START = dt.date(2024, 11, 1)
END = dt.date(2026, 10, 31)
DAYS = [START + dt.timedelta(days=i) for i in range((END - START).days + 1)]
GROWTH_2025 = 0.58                 # 2024-25 and 2025-26 electric long-distance trips relative to the 2027 projection
GROWTH_STEP = 0.16                 # second year above the first

# ---------------------------------------------------------------- weather
STATIONS = {
    'CAL': ('Calder Regional Airport', 540, 0.0),
    'COR': ('Corran Townsite', 1020, -2.1),
    'TAM': ('Tamarack Works Yard', 930, -1.6),
    'MIR': ('Mirren Airstrip', 690, -0.7),
}


def _weather():
    anom = 0.0
    wind_anom = 0.0
    out = {}
    for d in DAYS:
        m = d.month
        sd = 2.6 if m in (11, 12, 1, 2, 3) else 1.9
        anom = 0.5 * anom + RNG.normal(0, sd * math.sqrt(1 - 0.5 ** 2))
        wind_anom = 0.45 * wind_anom + RNG.normal(0, 1.0)
        # plateau storm intensity about its monthly mean: a gamma with mean one, capped at a closing gale
        storm = min(1.85, RNG.gamma(7.0, 1 / 7.0))
        precip = max(0.0, RNG.gamma(0.55, 4.2) - 1.1) if RNG.random() < 0.46 else 0.0
        out[d] = dict(anom=anom, wind=wind_anom, storm=storm, precip=precip)
    return out


WX = _weather()


def valley_temp(d, node='CAL'):
    st = STATIONS.get(node, STATIONS['CAL'])
    return W.VALLEY_T[d.month] + WX[d]['anom'] - W.LAPSE * (st[1] - 540) * 0.0 + st[2]


def day_factor(sid, d, direction):
    """The as-driven factor a car meets on a stretch on day d (before its own driving noise)."""
    s = W.STRETCHES[sid]
    m = d.month
    t = W.stretch_temp(sid, m) + WX[d]['anom']
    f = W.HIGHWAY_REAL * W.temp_factor(t)
    if s[6] > 0:
        ex = 1.0 + (W.EXPOSURE[m] - 1.0) * WX[d]['storm']
        f *= 1.0 + (ex - 1.0) * s[6] / 0.72
    cl, de = W.oriented(sid, direction)
    return f + W.climb_kwh(W.MASS_PER_RATED * 100.0, cl, de) / s[3]


# ---------------------------------------------------------------- the corridor sites
# CFC (Columbia Fast Charge Ltd.) runs every corridor site and three remote sites
CORRIDOR_SITES = {
    # node: [(svrd site id, CFC site code, name, charge point count, kW)]
    'HAL': [('SV-FC-03', 'CFC-0218', 'Halston Visitor Centre', 2, 150)],
    'COR': [('SV-FC-06', 'CFC-0233', 'Corran Village Square', 4, 150)],
    'FEN': [('SV-FC-09', 'CFC-0261', 'Fenwick Recreation Centre', 2, 150)],
    'CAL': [('SV-FC-01', 'CFC-0204', 'Calder Civic Plaza', 4, 150), ('SV-FC-12', 'CFC-0347', 'Calder Southgate', 2, 100)],
    'TAM': [('SV-FC-07', 'CFC-0249', 'Tamarack Community Hall', 2, 150)],
    'BRE': [('SV-FC-11', 'CFC-0318', 'Brennan Highway Services', 2, 150)],
    'ASH': [('SV-FC-14', 'CFC-0402', 'Ashby Fire Hall', 2, 100)],
    'MIR': [('SV-FC-16', 'CFC-0455', 'Mirren Library', 2, 100)],
    'RUT': [('SV-FC-19', 'CFC-0483', 'Rutherford Junction', 2, 150)],
}

# vehicle strings the CFC app shows for each model (owners pick their own profile)
VEHICLE_STRINGS = {
    'MY': ['Tesla Model Y Long Range', 'Model Y LR AWD', 'Tesla Model Y LR'],
    'M3L': ['Tesla Model 3 Long Range', 'Model 3 LR AWD'],
    'M3S': ['Tesla Model 3 RWD', 'Model 3 Standard RWD'],
    'IQ5': ['Hyundai IONIQ 5 LR AWD', 'IONIQ 5 Long Range AWD'],
    'EV6': ['Kia EV6 LR AWD', 'EV6 Long Range AWD'],
    'BLT': ['Chevrolet Bolt EUV', 'Bolt EUV'],
    'LF4': ['Nissan LEAF 40 kWh', 'Nissan Leaf'],
    'LFP': ['Nissan LEAF PLUS', 'Nissan Leaf Plus 62'],
    'NIR': ['Kia Niro EV', 'Niro EV'],
    'KON': ['Hyundai Kona Electric', 'Kona Electric'],
    'ID4': ['Volkswagen ID.4 Pro AWD', 'VW ID.4 AWD Pro'],
    'MME': ['Ford Mustang Mach-E ER AWD', 'Mach-E Extended Range AWD'],
    'EQX': ['Chevrolet Equinox EV 2LT', 'Equinox EV'],
    'PS2': ['Polestar 2 Long Range Dual Motor', 'Polestar 2 LR Dual'],
    'F15': ['Ford F-150 Lightning ER', 'F-150 Lightning Extended Range'],
    'R1S': ['Rivian R1S Large', 'R1S Large Pack'],
}

# ---------------------------------------------------------------- drivers and their cars
_model_keys = W.FLEET_KEYS
_model_p = np.array([W.FLEET[k][5] for k in _model_keys], dtype=float)
_model_p /= _model_p.sum()


def _drivers(n=11800):
    out = []
    for i in range(n):
        k = _model_keys[RNG.choice(len(_model_keys), p=_model_p)]
        usable = W.FLEET[k][2] * RNG.uniform(0.965, 1.01)
        drive = RNG.normal(1.0, 0.035)
        vs = VEHICLE_STRINGS[k][RNG.integers(len(VEHICLE_STRINGS[k]))]
        emsp = ['CFC', 'CFC', 'CFC', 'FLO', 'PLG', 'EVG'][RNG.integers(6)]
        token = f"CA*{emsp}*C{RNG.integers(10_000_000, 99_999_999)}*{RNG.integers(10)}"
        soc_report = RNG.random() > 0.07
        habit = RNG.choice(['planner', 'planner', 'planner', 'full', 'cautious'])
        out.append(dict(i=i, model=k, usable=usable, drive=drive, vstring=vs, token=token, soc_report=soc_report,
                        habit=habit))
    return out


DRIVERS = _drivers()


def _pick_driver(prev):
    if prev and RNG.random() < 0.45:
        return prev[RNG.integers(len(prev))]
    return DRIVERS[RNG.integers(len(DRIVERS))]


def _charge_minutes(kwh, kw, soc_from, soc_to):
    # a taper above 80 per cent roughly halves the power
    base = kwh / (0.78 * kw) * 60
    if soc_to > 0.8:
        base *= 1.0 + 0.9 * (soc_to - max(0.8, soc_from)) / max(soc_to - soc_from, 0.05)
    return max(6.0, base)


def simulate_corridor():
    """Simulate trips and return (sessions, trips)."""
    sessions, trips = [], []
    recent = []
    sid_counter = [700000]
    for d in DAYS:
        year_ix = 0 if d < dt.date(2025, 11, 1) else 1
        g = GROWTH_2025 * (1 + GROWTH_STEP * year_ix)
        dow = d.weekday()
        dow_f = 1.18 if dow in (4, 6) else (1.05 if dow == 5 else 0.93)
        for a, b, annual, prof in W.OD:
            lam = W.od_month_trips(a, b, annual, prof, d.month) * g * 12 / 365.25 * dow_f
            n = RNG.poisson(lam)
            for _ in range(n):
                x, y = (a, b) if RNG.random() < 0.5 else (b, a)
                drv = _pick_driver(recent)
                recent.append(drv)
                if len(recent) > 4000:
                    recent = recent[-3000:]
                t0 = dt.datetime.combine(d, dt.time(0)) + dt.timedelta(minutes=int(RNG.normal(10.5, 2.4) * 60))
                res = _drive(drv, x, y, d, t0, sid_counter)
                if res is None:
                    trips.append(dict(day=d, a=x, b=y, model=drv['model'], made=False))
                    continue
                sessions.extend(res)
                trips.append(dict(day=d, a=x, b=y, model=drv['model'], made=True, n_sessions=len(res)))
    return sessions, trips


def _drive(drv, a, b, d, t0, counter):
    path = R.path(a, b)
    usable = drv['usable']
    rated = W.FLEET[drv['model']][3]
    soc = RNG.uniform(0.86, 1.0)
    noise = {sid: RNG.normal(drv['drive'], 0.04) for sid, *_ in path}
    seg_e = [rated / 100.0 * W.STRETCHES[sid][3] * day_factor(sid, d, dirn) * noise[sid] for sid, dirn, *_ in path]
    seg_km = [W.STRETCHES[sid][3] for sid, *_ in path]
    nodes = [p[3] for p in path]
    chargers = set(W.EXISTING_NODES)
    # remaining energy from each node to the next charging node or the destination
    def to_next(i):
        e = 0.0
        for j in range(i, len(path)):
            e += seg_e[j]
            if nodes[j] in chargers or j == len(path) - 1:
                return e, j
        return e, len(path) - 1
    # pre-check: every leg must be possible from a full battery with 3 per cent to spare
    i = 0
    while i < len(path):
        e, j = to_next(i)
        if e / usable > 0.97:
            return None
        if i == 0:
            # a driver whose first leg needs more than tonight's charge tops up at home
            soc = max(soc, min(1.0, e / usable + RNG.uniform(0.10, 0.16)))
        i = j + 1
    t = t0
    out = []
    i = 0
    first = True
    while i < len(path):
        e_next, j = to_next(i)
        node = path[i][2]
        if node in chargers and not first:
            est = e_next / usable * RNG.normal(1.0, 0.05)
            buf = 0.11 + RNG.uniform(0.0, 0.08)
            need_charge = soc - est < buf
            opportunistic = node in ('CAL', 'COR') and soc < 0.72 and RNG.random() < 0.14
            if need_charge or opportunistic:
                if drv['habit'] == 'full':
                    target = min(1.0, max(0.92, est + buf + 0.05))
                elif drv['habit'] == 'cautious':
                    target = min(1.0, est + buf + RNG.uniform(0.10, 0.22))
                else:
                    target = min(1.0, est + buf + RNG.uniform(0.02, 0.12))
                if need_charge and target < soc + 0.05:
                    target = min(1.0, soc + 0.05)
                if target > soc + 0.03:
                    site = CORRIDOR_SITES[node][0]
                    if node == 'CAL' and RNG.random() < 0.38:
                        site = CORRIDOR_SITES[node][1]
                    kw = site[4]
                    kwh = (target - soc) * usable / RNG.uniform(0.905, 0.935)
                    mins = _charge_minutes(kwh, kw, soc, target)
                    t_arr = t
                    t_end = t_arr + dt.timedelta(minutes=mins + RNG.uniform(0.5, 3.0))
                    counter[0] += int(RNG.integers(1, 4))
                    out.append(dict(sid=counter[0], node=node, site=site, start=t_arr, end=t_end, kwh=kwh,
                                    soc0=soc, soc1=target, drv=drv, cp=int(RNG.integers(1, site[3] + 1))))
                    soc = target
                    t = t_end + dt.timedelta(minutes=RNG.uniform(2, 25))
        first = False
        # drive to node j
        for k in range(i, j + 1):
            soc -= seg_e[k] / usable
            sid = path[k][0]
            speed = 74.0 if W.STRETCHES[sid][6] > 0 or sid.startswith('E1') else 86.0
            t += dt.timedelta(minutes=seg_km[k] / speed * 60)
        i = j + 1
    return out
