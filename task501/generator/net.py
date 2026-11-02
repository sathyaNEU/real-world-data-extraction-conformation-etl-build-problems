"""The physical year: every district's hourly draw, the network's arrangement hour by hour, the trunk flows it put
through each main, the material each unlined main shed, and the relining arrangement replayed on the same dates.
This is the generator's clean truth; the golden never reads it (it reads the shipped pack)."""
import datetime as dt
import math

import numpy as np

import world as W

N_HOURS = int((W.T1 - W.T0).total_seconds() // 3600)
UTC = [W.T0 + dt.timedelta(hours=i) for i in range(N_HOURS)]
OFFSET = np.array([W.utc_offset_hours(t) for t in UTC])
LOCAL = [t + dt.timedelta(hours=int(o)) for t, o in zip(UTC, OFFSET)]
LOC_HOUR = np.array([t.hour + 0.5 for t in LOCAL])           # the middle of each hour, wall clock
LOC_DOW = np.array([t.weekday() for t in LOCAL])
LOC_DATE = [t.date() for t in LOCAL]
DOY = np.array([t.timetuple().tm_yday for t in LOCAL])


def hour_index(t_utc):
    return int((t_utc - W.T0).total_seconds() // 3600)


# ------------------------------------------------------------------------------------------------ large users
# key, name, billed district (the premises' district on the customer record), supplying district, kind
USERS = [
    ("U01", "Pennick Dairies Ltd", "D05", "D04", "creamery"),
    ("U02", "Stavenham Linen Services", "D07", "D06", "laundry"),
    ("U03", "Sallowby Mill Bottling Co", "D09", "D08", "bottling"),
    ("U04", "Hollow Lane Leisure Centre", "D18", "D09", "pool"),
    ("U05", "Ferrars Lane Bakery", "D04", "D04", "bakery"),
    ("U06", "St Anne's Court Care Home", "D05", "D05", "care"),
    ("U07", "Mill Bridge Community Hospital", "D06", "D06", "hospital"),
    ("U08", "Weir Lane Brewery", "D07", "D07", "brewery"),
    ("U09", "Sallowby Gate Meats", "D08", "D08", "meats"),
    ("U10", "Sallowby Park Garden Centre", "D09", "D09", "garden"),
    ("U11", "Hollow Lane Primary School", "D18", "D18", "school"),
    ("U12", "Stavenham General Hospital", "D10", "D10", "hospital_big"),
    ("U13", "Eastgate Swimming Baths", "D11", "D11", "baths"),
    ("U14", "Coldharbour Ready Mix", "D13", "D13", "concrete"),
    ("U15", "North Lodge Farm Dairy", "D14", "D14", "milking"),
    ("U16", "Highfield Business Park", "D16", "D16", "offices"),
]
MOVED = [u[0] for u in USERS if u[2] != u[3]]


def _between(h, a, b):
    """Local hour h (middle of hour) inside [a, b) on a 24 h clock (b may pass midnight)."""
    return (h >= a) & (h < b) if a < b else (h >= a) | (h < b)


def school_term(d):
    holidays = [(dt.date(2025, 12, 20), dt.date(2026, 1, 5)), (dt.date(2026, 2, 14), dt.date(2026, 2, 22)),
                (dt.date(2026, 3, 28), dt.date(2026, 4, 12)), (dt.date(2026, 5, 23), dt.date(2026, 5, 31)),
                (dt.date(2026, 7, 22), dt.date(2026, 9, 2)), (dt.date(2025, 10, 25), dt.date(2025, 11, 2)),
                (dt.date(2026, 10, 24), dt.date(2026, 11, 1))]
    return not any(a <= d <= b for a, b in holidays)


def user_profile(kind, rng):
    h, dow = LOC_HOUR, LOC_DOW
    wd = dow < 5
    n = N_HOURS
    q = np.zeros(n)
    if kind == "creamery":
        q += np.where(_between(h, 6, 18), np.where(wd, 3.4, 1.6), 0.5)
        lvl = 11.6 + 1.2 * rng.random(n)
        q = np.where(_between(h, 0.75, 3.25), lvl, q)
    elif kind == "laundry":
        night = _between(h, 22, 6) & (((dow <= 4) & (h >= 22)) | ((dow >= 1) & (dow <= 5) & (h < 6)))
        q += np.where(_between(h, 7, 16) & (dow < 6), 2.4, 0.3)
        q = np.where(night, 9.6 + 1.3 * rng.random(n), q)
    elif kind == "bottling":
        night = (((dow == 6) | (dow <= 3)) & (h >= 23)) | ((dow <= 4) & (h < 5))
        q += np.where(_between(h, 7, 17) & wd, 3.1, 0.4)
        q = np.where(night, 10.3 + 1.6 * rng.random(n), q)
    elif kind == "pool":
        refill = np.isin(dow, [1, 3, 6]) & _between(h, 0.5, 4.5)
        summer = np.array([5 <= t.month <= 8 for t in LOCAL])
        q += np.where(_between(h, 7, 21), np.where(summer, 2.6, 1.8), 0.35)
        q = np.where(refill, 8.7 + 0.9 * rng.random(n), q)
    elif kind == "bakery":
        q += np.where(_between(h, 2, 6) & (dow != 6), 2.6, np.where(_between(h, 6, 14), 1.0, 0.15))
    elif kind == "care":
        q += 0.55 + 0.5 * np.exp(-((h - 8.5) / 1.8) ** 2) + 0.25 * np.exp(-((h - 18) / 2.0) ** 2)
    elif kind == "hospital":
        q += 1.5 + 1.4 * np.exp(-((h - 10) / 3.5) ** 2)
    elif kind == "hospital_big":
        q += 3.2 + 2.6 * np.exp(-((h - 10.5) / 3.8) ** 2)
    elif kind == "brewery":
        brew = np.isin(dow, [0, 2, 4])
        q += np.where(_between(h, 7, 17) & wd, np.where(brew, 6.4, 3.9), 0.4)
    elif kind == "meats":
        q += np.where(_between(h, 4, 6.5) & wd, 6.6, np.where(_between(h, 7, 15) & wd, 2.0, 0.3))
    elif kind == "garden":
        season = np.array([4 <= t.month <= 9 for t in LOCAL])
        water = season & (_between(h, 6, 8) | _between(h, 18, 20))
        q += np.where(water, 3.0, np.where(_between(h, 9, 17), 0.6, 0.15))
    elif kind == "school":
        term = np.array([school_term(d) for d in LOC_DATE])
        q += np.where(term & wd & _between(h, 8, 16), 1.25, 0.08)
    elif kind == "baths":
        backwash = np.isin(dow, [0, 4]) & _between(h, 1, 4)
        q += np.where(_between(h, 6.5, 21.5), 2.1, 0.3)
        q = np.where(backwash, 6.9 + 0.6 * rng.random(n), q)
    elif kind == "concrete":
        q += np.where(_between(h, 6, 15) & wd, 3.6, np.where(_between(h, 6, 12) & (dow == 5), 1.8, 0.1))
    elif kind == "milking":
        q += np.where(_between(h, 5, 6.5) | _between(h, 16, 17.5), 4.1, 0.5)
    elif kind == "offices":
        q += np.where(_between(h, 8, 18) & wd, 3.0, 0.35)
    shut = np.array([(t.month == 12 and t.day >= 24) or (t.month == 1 and t.day <= 1) for t in LOCAL])
    if kind in ("creamery", "laundry", "bottling", "brewery", "meats", "concrete", "offices", "bakery"):
        q = np.where(shut, np.minimum(q, 0.4), q)
    q = q * (1 + 0.035 * rng.standard_normal(n))
    return np.clip(q, 0.02, None)


# ------------------------------------------------------------------------------------------------ demand
def heat_amp():
    a = np.zeros(N_HOURS)
    for d0, d1, amp, pk in W.HEAT:
        half = max((pk - d0).days, (d1 - pk).days) + 1
        for i, d in enumerate(LOC_DATE):
            if d0 <= d <= d1:
                a[i] = amp * (1 - abs((d - pk).days) / half) ** 0.35
    return a


def res_diurnal(h, dow):
    wk = dow >= 5
    hm = np.where(wk, h - 1.3, h)
    f = (0.17 + 0.88 * np.exp(-((hm - 7.4) / 1.6) ** 2) + 0.58 * np.exp(-((h - 19.1) / 2.5) ** 2)
         + 0.30 * np.exp(-((h - 12.8) / 3.1) ** 2) + 0.12 * np.exp(-((h - 22.6) / 1.2) ** 2))
    return f / 0.556 * np.where(wk, 1.04, 1.0)


def demand(rng):
    """District inflows (l/s) on the UTC hour, the users' own hourly use and the parts the truth needs."""
    season = 1 + 0.085 * np.cos(2 * math.pi * (DOY - 200) / 365.0)
    amp = heat_amp()
    users = {}
    for key, name, bill, sup, kind in USERS:
        users[key] = user_profile(kind, np.random.default_rng(W.SEED + int(key[1:]) * 17))
    dem, parts = {}, {}
    for d in W.DISTRICTS:
        r = np.random.default_rng(W.SEED + 1000 + int(d[1:]))
        sens = 0.85 + 0.3 * r.random()
        heat = 1 + amp * sens * (0.5 + 0.95 * np.exp(-((LOC_HOUR - 19.4) / 2.4) ** 2))
        ar = np.zeros(N_HOURS)
        e = r.standard_normal(N_HOURS) * 0.012
        for i in range(1, N_HOURS):
            ar[i] = 0.85 * ar[i - 1] + e[i]
        res = W.RES[d] * res_diurnal(LOC_HOUR, LOC_DOW) * season * heat * (1 + ar)
        leak = W.LEAK[d] * (1 + 0.06 * np.cos(2 * math.pi * (DOY - 20) / 365.0)) * (1 + 0.01 * r.standard_normal(N_HOURS))
        bus = np.where(_between(LOC_HOUR, 8, 18) & (LOC_DOW < 5), 1.9, np.where(_between(LOC_HOUR, 9, 16), 0.7, 0.12))
        nh = W.NH_SMALL[d] * bus / 0.86 * (1 + 0.05 * r.standard_normal(N_HOURS))
        u = sum((users[k] for k, _, _, s, _ in USERS if s == d), np.zeros(N_HOURS))
        total = (res + leak + nh + u) * (1 + 0.004 * r.standard_normal(N_HOURS))
        dem[d] = total
        parts[d] = dict(res=res, leak=leak, nh=nh, users=u)
    return dem, users, parts


# ------------------------------------------------------------------------------------------------ arrangements
def tree(in_service):
    """Undirected walk from the works over the mains in service: parent main of every junction and each main's
    direction. Raises on a loop or an unfed junction."""
    adj = {}
    for m in sorted(in_service):
        _, _, a, b = W.MAINS[m][:4]
        adj.setdefault(a, []).append((m, b))
        adj.setdefault(b, []).append((m, a))
    parent = {"W": None}
    path = {"W": []}
    q = ["W"]
    used = set()
    while q:
        u = q.pop(0)
        for m, v in adj.get(u, []):
            if m in used:
                continue
            used.add(m)
            if v in path:
                raise ValueError("loop at %s through %s" % (v, m))
            parent[v] = (m, u)
            path[v] = path[u] + [m]
            q.append(v)
    for n in W.NODES:
        if n not in path:
            raise ValueError("unfed junction %s" % n)
    return path


NORMAL = frozenset(W.TRUNK)


def arrangement(out=(), opened=()):
    return frozenset((NORMAL - set(out)) | set(opened))


def _valve_ops():
    """Event key -> {(main, end): [(utc time, op), ...]} from the logged sequences."""
    out = {}
    for ev in W.EVENTS:
        ops = {}
        for ts, m, end, op in ev["seq"]:
            t = W.to_utc(dt.datetime.strptime(ts, "%Y-%m-%d %H:%M"))
            ops.setdefault((m, end), []).append((t, op))
        out[ev["key"]] = {k: sorted(v) for k, v in ops.items()}
    return out


def state_at(ev, ops, t):
    """The in-service set at UTC instant t under one event's valves (every other valve normal)."""
    s = set(NORMAL)
    for (m, end), seq in ops.items():
        normal = "OPEN" if m in NORMAL else "CLOSE"
        st = normal
        for tt, op in seq:
            if tt <= t:
                st = op
        if m in NORMAL and st == "CLOSE":
            s.discard(m)
        if m not in NORMAL and st == "OPEN":
            s.add(m)
    return frozenset(s)


def timeline(keys=None):
    """For every UTC hour, the in-service sets in force as [(fraction of the hour, set)]. A minute whose state is no
    tree (two routes in parallel while a back-feed is made, or the burst's minutes with no supply) counts under the
    last tree state before it. keys: the events to include (all by default)."""
    allops = _valve_ops()
    out = [[(1.0, NORMAL)] for _ in range(N_HOURS)]
    for ev in W.EVENTS:
        if keys is not None and ev["key"] not in keys:
            continue
        ops = allops[ev["key"]]
        times = sorted(t for v in ops.values() for t, _ in v)
        h0, h1 = hour_index(times[0].replace(minute=0)), hour_index(times[-1].replace(minute=0))
        op_hours = {hour_index(t.replace(minute=0)) for t in times}
        last_tree = NORMAL
        for h in range(h0, h1 + 1):
            if h not in op_hours:
                s = state_at(ev, ops, UTC[h] + dt.timedelta(minutes=30))
                if _is_tree(s):
                    last_tree = s
                out[h] = [(1.0, last_tree)]
                continue
            counts = {}
            for k in range(60):
                s = state_at(ev, ops, UTC[h] + dt.timedelta(minutes=k, seconds=30))
                if _is_tree(s):
                    last_tree = s
                counts[last_tree] = counts.get(last_tree, 0) + 1
            out[h] = [(c / 60.0, s) for s, c in counts.items()]
    return out


def dark_minutes():
    """Hour index -> minutes of the July burst during which Mill Bridge and Sallowby had no supply."""
    out = {}
    for ev in W.EVENTS:
        if "dark" in ev:
            a, b = (W.to_utc(t) for t in ev["dark"])
            t = a
            while t < b:
                h = hour_index(t.replace(minute=0, second=0))
                out[h] = out.get(h, 0) + 1
                t += dt.timedelta(minutes=1)
    return out


def flows_through(in_service, dem_cols):
    """Each main's flow (l/s, magnitude) and direction sign (+1 register direction, -1 against) for a block of hours
    under one in-service set; dem_cols: district -> array."""
    path = tree(in_service)
    n = len(next(iter(dem_cols.values())))
    f = {m: np.zeros(n) for m in W.MAINS}
    for d, node in W.DNODE.items():
        for m in path[node]:
            f[m] += dem_cols[d]
    sign = {}
    for m in sorted(in_service):
        _, _, a, b = W.MAINS[m][:4]
        # the main runs a->b when b is downstream of it
        sign[m] = 1 if (m in path[b] and (m not in path[a])) else -1
    return f, sign


def operated_flows(dem, tl=None, dark=None, burst=True):
    """Trunk flows hour by hour through the arrangement actually in force (minute-weighted in switch hours), with
    the burst's loss through the mains upstream of it."""
    tl = tl or timeline()
    dark = dark if dark is not None else dark_minutes()
    f = {m: np.zeros(N_HOURS) for m in W.MAINS}
    sgn = {m: np.ones(N_HOURS) for m in W.MAINS}
    groups = {}
    for h, parts in enumerate(tl):
        if len(parts) == 1:
            groups.setdefault(parts[0][1], []).append(h)
    for s, hh in groups.items():
        hh = np.array(hh)
        fl, sg = flows_through(s, {d: dem[d][hh] for d in dem})
        for m in W.MAINS:
            f[m][hh] = fl[m]
            if m in sg:
                sgn[m][hh] = sg[m]
    for h, parts in enumerate(tl):
        if len(parts) > 1:
            for frac, st in parts:
                fl, _ = flows_through(st, {d: dem[d][h:h + 1] for d in dem})
                for m in W.MAINS:
                    f[m][h] += frac * fl[m][0]
    if burst:
        a, b, q = W.BURST_LOSS
        a, b = W.to_utc(a), W.to_utc(b)
        t = a
        while t < b:
            h = hour_index(t.replace(minute=0, second=0))
            for m in ("T01", "T02", "T03", "T04"):
                f[m][h] += q / 60.0
            t += dt.timedelta(minutes=1)
    return f, sgn


def _is_tree(s):
    try:
        tree(s)
        return True
    except ValueError:
        return False


def static_flows(dem):
    fl, _ = flows_through(NORMAL, dem)
    return fl


def replay_mask():
    a, b = W.REPLAY
    return np.array([a <= t.date() <= b for t in UTC])


def plan_flows(dem):
    m = replay_mask()
    fl, sg = flows_through(arrangement(W.PLAN_OUT, W.PLAN_OPEN), {d: dem[d][m] for d in dem})
    return fl, sg, m


# ------------------------------------------------------------------------------------------------ deposits
DEPOSIT = dict(T03=2.7, T04=2.4, T10=2.2, T05=2.6, T06=2.0, T13=2.5, T08=2.8, T09=2.3,
               X02=4.1, X04=4.4, X05=3.9, X07=4.0)            # NTU scale of a main's loose deposit
SIGNIFICANT = 0.015                                            # a rise inside 1.5 per cent sheds nothing measurable
KERNEL = (0.48, 0.27, 0.15, 0.10)


def initial_conditioning(static):
    """Each main's level before the reference year: the summer of 2025 carried the normal arrangement at a little
    above 2026's early-June peaks; the interconnectors had stood shut for years."""
    win = np.array([dt.date(2026, 6, 1) <= d <= dt.date(2026, 6, 20) for d in LOC_DATE])
    return {m: (0.95 * float(static[m][win].max()) if m in W.TRUNK else 0.0) for m in W.MAINS}


def shed(op, static):
    """Material each main releases, hour by hour (NTU-equivalent at its own flow), and its conditioned level after
    every hour. A main sheds when its flow passes the highest it has carried; lined walls shed nothing."""
    c0 = initial_conditioning(static)
    rel = {m: np.zeros(N_HOURS) for m in W.MAINS}
    level = {m: np.zeros(N_HOURS) for m in W.MAINS}
    lined_from = hour_index(W.T06_LINED_FROM)
    for m in W.MAINS:
        c = c0[m]
        q = op[m]
        for t in range(N_HOURS):
            lined = m in W.LINED or (m == "T06" and t >= lined_from)
            if q[t] > c:
                x = min(3.0, q[t] / max(c, 8.0) - 1.0) - SIGNIFICANT
                if not lined and m in DEPOSIT and x > 0:
                    for k, w in enumerate(KERNEL):
                        if t + k < N_HOURS:
                            rel[m][t + k] += DEPOSIT[m] * x ** 0.6 * w
                c = q[t]
            level[m][t] = c
    return rel, level, c0


def inlet_turbidity(rel, tl):
    """Turbidity added at each district inlet: the material released in every main on its supply path that hour
    (the arrangement in force for most of the hour)."""
    add = {d: np.zeros(N_HOURS) for d in W.DISTRICTS}
    cache = {}
    for t, parts in enumerate(tl):
        s = max(parts, key=lambda p: p[0])[1]
        if s not in cache:
            cache[s] = tree(s)
        path = cache[s]
        for d, node in W.DNODE.items():
            v = 0.0
            for m in path[node]:
                v += rel[m][t]
            add[d][t] = v
    return add
