"""Routes, legs between charging points, feasibility and every pricing route a solver could take.

An energy function maps (band, stretch id, month, direction) to the kWh the band's reference car needs. The
grant rules make a trip completable for a band when the first leg (origin to the first charger) needs no more
than START_SOC - RESERVE of the reference car's usable battery and every later leg no more than
CHARGE_TO - RESERVE. A package's gain is the 2027 trips completable with its sites added less the trips today's
network already makes completable, each month's trips shared over the bands by the register.
"""
import world as W

# ------------------------------------------------------------------ paths
_ADJ = {}
for _sid, (_a, _b, _hw, _km, _cl, _de, _ex) in W.STRETCHES.items():
    _ADJ.setdefault(_a, []).append((_b, _sid, 'F'))
    _ADJ.setdefault(_b, []).append((_a, _sid, 'R'))


def path(a, b):
    """The unique path through the tree network: list of (stretch id, direction, from node, to node)."""
    stack = [(a, [])]
    seen = {a}
    while stack:
        node, acc = stack.pop()
        if node == b:
            return acc
        for nxt, sid, d in _ADJ.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                stack.append((nxt, acc + [(sid, d, node, nxt)]))
    raise ValueError((a, b))


def legs(a, b, chargers):
    """Split the path into legs at every charging node strictly inside it: [(is_first, [(sid, dir)...])]."""
    out, cur = [], []
    for sid, d, frm, to in path(a, b):
        cur.append((sid, d))
        if to in chargers and to != b:
            out.append(cur)
            cur = []
    out.append(cur)
    return [(i == 0, lg) for i, lg in enumerate(out)]


def avail(band, first):
    cap = W.BANDS[band][3]
    return cap * ((W.START_SOC if first else W.CHARGE_TO) - W.RESERVE)


def feasible(band, a, b, month, chargers, efn):
    for first, lg in legs(a, b, chargers):
        if sum(efn(band, sid, month, d) for sid, d in lg) > avail(band, first):
            return False
    return True


def completable(a, b, month, chargers, efn):
    """Share of the register's fleet whose reference car completes the trip in this month, both ways averaged."""
    tot = 0.0
    for bd in W.BAND_KEYS:
        tot += W.share(bd) * 0.5 * (feasible(bd, a, b, month, chargers, efn) + feasible(bd, b, a, month, chargers, efn))
    return tot


def gains(efn):
    """2027 trips each package makes completable, by month (list of 12) per package."""
    base_ch = set(W.EXISTING_NODES)
    out = {p: [0.0] * 12 for p in W.PACKAGES}
    for a, b, annual, prof in W.OD:
        for m in W.MONTHS:
            trips = W.od_month_trips(a, b, annual, prof, m)
            c0 = completable(a, b, m, base_ch, efn)
            for p, pk in W.PACKAGES.items():
                c1 = completable(a, b, m, base_ch | set(pk['nodes']), efn)
                out[p][m - 1] += trips * (c1 - c0)
    return out


def totals(g):
    return {p: sum(v) for p, v in g.items()}


# ------------------------------------------------------------------ pricing routes (energy functions)
def rated(band):
    return W.BANDS[band][4]


def km(sid):
    return W.STRETCHES[sid][3]


def climb(band, sid, d):
    return W.climb_kwh(W.MASS_PER_RATED * rated(band), *W.oriented(sid, d))


def e_rated(band, sid, m, d):
    """The reference car's rated combined consumption over the stretch's length."""
    return rated(band) / 100.0 * km(sid)


def e_rated_climb(band, sid, m, d):
    return e_rated(band, sid, m, d) + climb(band, sid, d)


def e_winter_derate(band, sid, m, d):
    """Rated consumption raised 30 per cent from November to March, the climb added."""
    f = 1.30 if m in (11, 12, 1, 2, 3) else 1.0
    return e_rated(band, sid, m, d) * f + climb(band, sid, d)


def e_valley_physics(band, sid, m, d):
    """Highway consumption at the valley's monthly air temperature, the climb added."""
    per = rated(band) / 100.0 * W.HIGHWAY_REAL * W.temp_factor(W.VALLEY_T[m])
    return per * km(sid) + climb(band, sid, d)


def e_lapse_physics(band, sid, m, d):
    """Highway consumption at the stretch's lapse-rate temperature, the climb added."""
    per = rated(band) / 100.0 * W.HIGHWAY_REAL * W.temp_factor(W.stretch_temp(sid, m))
    return per * km(sid) + climb(band, sid, d)


HIGH = {'W2a', 'W2b', 'E1a', 'E1b'}


def e_high_derate(band, sid, m, d):
    """Lapse-rate physics with a further 25 per cent on the high stretches from November to March."""
    e = e_lapse_physics(band, sid, m, d)
    if sid in HIGH and m in (11, 12, 1, 2, 3):
        e *= 1.25
    return e


def e_truth(band, sid, m, d):
    return W.true_energy_rated(rated(band), sid, m, d)


def make_high_derate(pct, months=(11, 12, 1, 2, 3)):
    """Lapse-rate physics with a further pct on the high stretches in the cold months."""
    def fn(band, sid, m, d):
        e = e_lapse_physics(band, sid, m, d)
        if sid in HIGH and m in months:
            e *= 1.0 + pct
        return e
    return fn


def make_winter_derate(pct, months=(11, 12, 1, 2, 3)):
    """Valley physics with a further pct on every stretch in the cold months."""
    def fn(band, sid, m, d):
        e = e_valley_physics(band, sid, m, d)
        if m in months:
            e *= 1.0 + pct
        return e
    return fn


SENSITIVITY = {
    'high_derate_10': make_high_derate(0.10), 'high_derate_40': make_high_derate(0.40),
    'high_derate_60': make_high_derate(0.60), 'winter_all_20': make_winter_derate(0.20),
    'winter_all_40': make_winter_derate(0.40),
}


# today's legs between existing charging nodes along each highway, and which leg each stretch sits in
LEGS_TODAY = {}
STRETCH_LEG = {}
for _hw, _seq in W.HIGHWAYS.items():
    _cur, _start = [], _seq[0]
    for _i in range(len(_seq) - 1):
        _a, _b = _seq[_i], _seq[_i + 1]
        _s = [s for s, v in W.STRETCHES.items() if (v[0], v[1]) == (_a, _b)][0]
        _cur.append(_s)
        if _b in W.EXISTING_NODES:
            _key = f'{_start}-{_b}'
            LEGS_TODAY[_key] = list(_cur)
            for s in _cur:
                STRETCH_LEG[s] = _key
            _cur, _start = [], _b


def leg_true_factor(key, m, d):
    """km-weighted true factor over today's leg (every stretch in a leg runs in the leg's own direction)."""
    members = LEGS_TODAY[key]
    e = sum(W.true_factor(s, m, d) * km(s) for s in members)
    return e / sum(km(s) for s in members)


def truth_factor_table():
    return {(k, m, d): leg_true_factor(k, m, d) for k in LEGS_TODAY for m in W.MONTHS for d in ('F', 'R')}


def make_measured(table, alloc='km'):
    """Energy from measured as-driven factors per today's leg, month and direction.

    A stretch inside a leg takes the leg's factor times the reference car's rated consumption and the stretch's
    length ('km'), or the leg's measured energy shared with the climb read by physics ('physics')."""
    def fn(band, sid, m, d):
        key = STRETCH_LEG[sid]
        f = table[(key, m, d)]
        if alloc == 'km':
            return f * rated(band) / 100.0 * km(sid)
        members = LEGS_TODAY[key]
        total = f * rated(band) / 100.0 * sum(km(s) for s in members)
        cl = {s: climb(band, s, d) for s in members}
        flat = total - sum(cl.values())
        return flat * km(sid) / sum(km(s) for s in members) + cl[sid]
    return fn


ROUTES_ORDER = ['rated', 'rated_climb', 'winter_derate', 'valley_physics', 'lapse_physics', 'high_derate', 'truth']
ROUTE_FN = {
    'rated': e_rated, 'rated_climb': e_rated_climb, 'winter_derate': e_winter_derate,
    'valley_physics': e_valley_physics, 'lapse_physics': e_lapse_physics, 'high_derate': e_high_derate,
    'truth': e_truth,
}
