"""task245 simulator: Thornmouth's coast weather, the regional PM10 background, the bulk terminal's dust plume reaching
each station on its own bearing, each station's hourly PM10, the council stations' NO2, and the analysers' faults and
outages. Hours are GMT, hour index h covering [START + h, START + h + 1), so day d is hours 24d to 24d + 23."""
import numpy as np

import params as P

D, H = P.DAYS, P.HOURS
HOUR = np.arange(H)
DAY = HOUR // 24
HOD = HOUR % 24
DOW = (np.arange(D) + 4) % 7                     # 1 January 2027 is a Friday; Monday is 0


def rng(*k):
    return np.random.default_rng([P.SEED] + list(k))


def weather(stream=1):
    """hourly wind direction (degrees the wind blows from), speed (m/s), rain (mm), temperature; daily wet flag"""
    r = rng(stream, 0)
    dirs = np.array([x[0] for x in P.REGIMES], float)
    share = np.array([x[1] for x in P.REGIMES], float)
    daydir = np.zeros(D)
    d = 0
    while d < D:
        p = share.copy()
        if P.SPRING_EAST[0] <= d < P.SPRING_EAST[1]:
            p[[5, 6]] *= P.SPRING_EAST[2]
        p /= p.sum()
        nd = r.choice(dirs, p=p)
        n = r.geometric(P.REGIME_STOP)
        for j in range(n):
            if d + j < D:
                daydir[d + j] = (nd + r.normal(0, 18)) % 360
        d += n
    base = np.radians(daydir[DAY])
    if P.VEER_HOURS:
        k = np.ones(2 * P.VEER_HOURS + 1) / (2 * P.VEER_HOURS + 1)
        u = np.convolve(np.pad(np.sin(base), P.VEER_HOURS, mode="edge"), k, "valid")
        v = np.convolve(np.pad(np.cos(base), P.VEER_HOURS, mode="edge"), k, "valid")
        base = np.arctan2(u, v)
    z = r.normal(0, P.HOURLY_SD, H)
    if P.HOURLY_AR:
        for h in range(1, H):
            z[h] = P.HOURLY_AR * z[h - 1] + np.sqrt(1 - P.HOURLY_AR ** 2) * z[h]
    theta = (np.degrees(base) + z + 15 * np.sin(2 * np.pi * HOD / 24)) % 360
    speed = np.clip(np.repeat(r.gamma(4.0, 1.25, D), 24) * (0.8 + 0.4 * np.sin(np.pi * np.clip(HOD - 6, 0, 12) / 12)), 0.3, None)
    wet = r.random(D) < (0.48 + 0.12 * np.cos(2 * np.pi * (np.arange(D) - 340) / 365))
    rain = np.where(np.repeat(wet, 24) & (r.random(H) < 0.35), r.gamma(1.2, 0.9, H), 0.0)
    temp = 9.0 + 6.5 * np.cos(2 * np.pi * (np.arange(H) / 24 - 200) / 365) + 2.5 * np.sin(2 * np.pi * (HOD - 9) / 24) + r.normal(0, 1.2, H)
    return dict(theta=theta, speed=speed, wet=wet, wet_h=np.repeat(wet, 24), rain=rain, temp=temp)


def background(stream=2, W=None):
    """the regional PM10 background (daily, then hourly), higher in continental air off the North Sea and lower in
    Atlantic air, and the terminal's daily activity"""
    r = rng(stream, 0)
    t = np.arange(D)
    level = 2.65 + P.BG_SEASON * np.cos(2 * np.pi * (t - 100) / 365)
    if W is not None:
        day_dir = np.degrees(np.arctan2(np.sin(np.radians(W["theta"])).reshape(D, 24).mean(1),
                                        np.cos(np.radians(W["theta"])).reshape(D, 24).mean(1))) % 360
        level = level + P.AIRMASS * np.cos(np.radians(day_dir - 90.0))
    ar = np.zeros(D)
    e = r.normal(0, P.BG_SD, D)
    for i in range(1, D):
        ar[i] = 0.7 * ar[i - 1] + e[i]
    bd = np.exp(level + ar)
    for st, n, a in P.EPISODES:
        for j in range(n):
            bd[st + j] += a * np.sin(np.pi * (j + 0.5) / n)
    # ship calls: a bulk carrier at the berth every few days, discharging for one to three days, the stockyard busy while
    # it does; between calls the stacker and reclaimer only rework the stockpiles
    act = np.full(D, P.ACT_IDLE)
    d = int(r.integers(1, 5))
    while d < D:
        n = int(r.integers(1, 4))
        act[d:d + n] = P.ACT_DISCHARGE * np.exp(r.normal(0, 0.15, len(act[d:d + n])))
        d += n + int(r.integers(3, 8))
    act = act * np.exp(r.normal(0, 0.10, D))
    traffic = np.where(DOW[DAY] < 5, 1.0, 0.6) * (0.6 + 0.8 * np.exp(-((HOD - 8) / 2.0) ** 2)
                                                 + 0.7 * np.exp(-((HOD - 17.5) / 2.5) ** 2))
    return dict(bd=bd, b=np.repeat(bd, 24), act=np.repeat(act, 24), traffic=traffic)


def bearing_to_terminal(x, y):
    return float(np.degrees(np.arctan2(-x, -y)) % 360)


def pm10(W, BG, i, scale):
    """one station's hourly PM10 (micrograms per cubic metre)"""
    code, name, op, typ, x, y, bm, tr = P.STATIONS[i][:8]
    r = rng(3, i)
    dist = np.hypot(x, y) / 1000.0
    phi = bearing_to_terminal(x, y)
    ali = np.exp(P.PLUME_KAPPA * (np.cos(np.radians(W["theta"] - phi)) - 1))
    lift = 1.0 + P.LIFT * (1 - np.exp(-(W["speed"] / 3.0) ** 2))
    plume = P.PLUME_AMP * scale * ali * lift / dist ** 1.3 * np.where(W["wet_h"], P.WET_FACTOR, 1.0) * BG["act"]
    z = r.normal(0, 0.15, H)
    return (bm * BG["b"] + tr * BG["traffic"] + plume) * np.exp(z)


def fit_scale(W, BG, i):
    """the plume scale that gives the station its target count of days above 50"""
    tgt = P.STATIONS[i][11]
    lo, hi = 0.0, 4.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if (pm10(W, BG, i, mid).reshape(D, 24).mean(1) > 50).sum() < tgt:
            lo = mid
        else:
            hi = mid
    return hi


def quiet_window(xd, n):
    """the n-day stretch with the fewest days above 45 (where a long outage leaves the least out)"""
    c = np.convolve((xd > 45).astype(float), np.ones(n), "valid")
    return int(np.argmin(c[20:300])) + 20


def outages(X, fault_mult, fault_seed, gaps, only=None, base=None):
    """hourly validity and cause: 'F' overload fault (down to the technician's next round at 10:00), 'X' the hours
    earlier on a fault's day and after the restart that ratification rejects, 'S' service, 'P' power or communications, 'G' long outage, '' valid"""
    n = X.shape[0]
    cause = np.full((n, H), "", dtype="<U1") if base is None else base.copy()
    rounds = {"TBT": P.ROUND_TBT, "TBC": P.ROUND_TBC}
    for i in (range(n) if only is None else only):
        cause[i] = ""
        r = rng(4, i, fault_seed[i])
        if P.STATIONS[i][9]:
            visit = np.isin(DOW[DAY], rounds[P.STATIONS[i][2]]) & (HOD == 10)
            u = r.random(H)
            down = False
            settle = 0
            load = 0.0
            for h in range(H):
                if visit[h]:
                    load = 0.0                     # the filter is exchanged on every round
                    if down:
                        down = False
                        settle = 24 - HOD[h] if P.STABILISE == "day" else P.STABILISE
                if down:
                    cause[i, h] = "F"
                    continue
                if settle:
                    cause[i, h] = "X"
                    settle -= 1
                    continue
                x = X[i, h]
                load += x
                onset = h > 0 and x > P.FAULT_T1 and X[i, h - 1] <= P.FAULT_T1
                if onset and load > P.FAULT_LOAD and u[h] < P.FAULT_Q * fault_mult[i]:
                    down = True
                    cause[i, h] = "F"
                    h0 = h - HOD[h] if P.FAULT_PRE == "day" else max(0, h - P.FAULT_PRE)
                    pre = cause[i, h0:h]
                    cause[i, h0:h] = np.where(pre == "", "X", pre)
        for q in range(4):
            d0 = int(q * 91) + int(r.integers(0, 85))
            cause[i, d0 * 24 + 9: d0 * 24 + 16] = "S"
        for _ in range(int(r.integers(2, 6))):
            h0, n0 = int(r.integers(0, H - 40)), int(r.integers(2, 20))
            seg = cause[i, h0:h0 + n0]
            cause[i, h0:h0 + n0] = np.where(seg == "", "P", seg)
        if i in gaps:
            g0, gl = gaps[i]
            cause[i, g0 * 24 + 9:(g0 + gl) * 24 + 10] = "G"      # disconnected at 09:00, back at 10:00
    return cause


def plume_index(W, BG, i):
    """the hourly share of the terminal's dust pointed at station i (bearing, lift, wet, activity), no scale"""
    code, name, op, typ, x, y = P.STATIONS[i][:6]
    phi = bearing_to_terminal(x, y)
    ali = np.exp(P.PLUME_KAPPA * (np.cos(np.radians(W["theta"] - phi)) - 1))
    lift = 1.0 + P.LIFT * (1 - np.exp(-(W["speed"] / 3.0) ** 2))
    return ali * lift * np.where(W["wet_h"], P.WET_FACTOR, 1.0) * BG["act"]


def no2(W, BG, code):
    """a council station's true hourly NO2 (micrograms per cubic metre at 20 C) and NOx (as NO2)"""
    i = P.CODES.index(code)
    bm, tr, ship = P.NO2[code]
    r = rng(5, i)
    t = np.arange(D)
    lvl = 13.0 + 6.5 * np.cos(2 * np.pi * (t - 15) / 365)
    ar = np.zeros(D)
    e = r.normal(0, 0.18, D)
    for k in range(1, D):
        ar[k] = 0.6 * ar[k - 1] + e[k]
    bg = np.repeat(lvl * np.exp(ar), 24) * (0.85 + 0.3 * np.exp(-((HOD - 20) / 4.0) ** 2))
    x, y = P.STATIONS[i][4], P.STATIONS[i][5]
    phi = bearing_to_terminal(x, y)
    berth = ship * np.exp(4.0 * (np.cos(np.radians(W["theta"] - phi)) - 1))
    v = (bm * bg + tr * BG["traffic"] + berth) * np.exp(r.normal(0, 0.18, H))
    nox = v * (1.25 + 0.9 * tr / 21.0 * BG["traffic"]) * np.exp(r.normal(0, 0.08, H))
    return v, nox


def deposit_periods():
    """the operator's gauge exchanges: the first Monday of each month, from December 2026 to January 2028"""
    import datetime as dt
    out = []
    for y, m in [(2026, 12)] + [(2027, k) for k in range(1, 13)] + [(2028, 1)]:
        d = dt.date(y, m, 1)
        while d.weekday() != 0:
            d += dt.timedelta(days=1)
        out.append(d)
    return list(zip(out[:-1], out[1:]))


def deposition(W, BG, scales):
    """each operator station's true deposition rate (mg/m2/day) in each exchange period"""
    import datetime as dt
    rows = []
    r = rng(6, 0)
    for i, st in enumerate(P.STATIONS):
        if st[2] != "TBT":
            continue
        x, y = st[4], st[5]
        pi = P.PLUME_AMP * scales[i] * plume_index(W, BG, i) / (np.hypot(x, y) / 1000.0) ** 1.3
        for a, b in deposit_periods():
            h0 = max(0, (a - P.START.date()).days * 24)
            h1 = min(H, (b - P.START.date()).days * 24)
            # the year before and after: the same climate as the same weeks of 2027
            if h1 <= h0:
                h0, h1 = (a.replace(year=2027) - P.START.date()).days * 24, min(H, (b.replace(year=2027) - P.START.date()).days * 24)
            k = P.DEPOSIT_K[st[0]]
            rate = P.DEPOSIT_BG * np.exp(r.normal(0, 0.15)) + k * P.DEPOSIT_PER_UG * float(pi[h0:h1].mean()) * np.exp(r.normal(0, 0.10))
            rows.append((st[0], a, b, (b - a).days, rate))
    return rows


def clear_of_line(X, valid):
    """no valid daily mean within 0.6 of the 50 line: a day whose valid hours average 49.4 to 50.6 is scaled to 49.2 (at
    or under the line) or 50.8 (over it), so no rounding convention moves a day across"""
    X = X.copy()
    n = X.shape[0]
    for i in range(n):
        for d in range(D):
            v = valid[i, d * 24:(d + 1) * 24]
            if v.sum() < 18:
                continue
            m = X[i, d * 24:(d + 1) * 24][v].mean()
            if 49.4 <= m <= 50.6:
                X[i, d * 24:(d + 1) * 24] *= (49.2 if m <= 50.0 else 50.8) / m
    return X


def make(tuned=True):
    """the whole simulated year: weather, background, PM10 truth and validity, NO2 truth and validity, deposition"""
    W = weather()
    BG = background(W=W)
    n = len(P.STATIONS)
    scales = [fit_scale(W, BG, i) for i in range(n)]
    X = np.array([pm10(W, BG, i, scales[i]) for i in range(n)])
    mult = [P.FAULT_MULT.get(c, 1.0) for c in P.CODES]
    seed = [P.FAULT_SEED.get(c, 0) for c in P.CODES]
    gaps = {P.CODES.index(c): g for c, g in P.GAP_START.items()}
    cause = outages(X, mult, seed, gaps)
    X = clear_of_line(X, cause == "")
    N = {}
    for c in P.NO2:
        v, nox = no2(W, BG, c)
        N[c] = (v, nox)
    return dict(W=W, BG=BG, X=X, scales=scales, cause=cause, NO2=N, dep=deposition(W, BG, scales), gaps=gaps)
