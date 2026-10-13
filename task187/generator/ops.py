"""The farm's operations on the UTC interval index: what each turbine was doing and making in every interval.

Each turbine's true state and power come from its free power (wind.py) and, in order of precedence: the January grid
loss; downtime (faults and repairs, the CH09 main-bearing exchange, the CH06 gearbox exchange, the annual services);
ice; high wind; low wind; the network operator's ANM limits and trips; the planning condition's night-time noise mode.
Some intervals have no SCADA row: while a controller is isolated (service, the two crane jobs), after a fault that
cut a turbine's auxiliary supply, through the site communications outage (turbines running) and through the grid
loss. The counters keep the energy made through all of them."""
import datetime as dt

import numpy as np

import wind as WD
import world as W

N = W.N


def k_of(t):
    return W.interval_index(t)


def local_hour(k):
    t = W.start_of(k).astimezone(W.LONDON)
    return t.hour + t.minute / 60.0


def utc_of_local(d, hh, mm):
    """The UTC datetime of a local wall-clock time on date d (never on a clock-change night here)."""
    return dt.datetime(d.year, d.month, d.day, hh, mm, tzinfo=W.LONDON).astimezone(W.UTC)


def window(a, b):
    """Interval indices starting in [a, b) for UTC datetimes a, b."""
    return np.arange(k_of(a), k_of(b))


def protected(m):
    """Intervals no random event may touch: the communications outage and the grid loss, an hour either side, and
    the hour either side of the twelve months' edges and the October clock change."""
    bad = np.zeros(N, bool)
    for a, b in (W.COMMS_OUTAGE, W.GRID_LOSS):
        bad[max(0, k_of(a) - 6):k_of(b) + 6] = True
    bad[:12] = True
    bad[-12:] = True
    oct_change = k_of(dt.datetime(2025, 10, 26, 0, 0, tzinfo=W.UTC))
    bad[oct_change - 12:oct_change + 18] = True
    return bad


def services(m):
    """Each turbine's two-day annual service, May to July 2026, local times: day 1 stopped and isolated straight from
    running, back on the controller in service mode, returned to service at the end of the day; day 2 stopped in
    service mode, isolated in the afternoon, restarted to ready. The contractor books two turbines a week in order
    and climbs only in moderate wind (the mast's mean over each isolation between 6 and 11 m/s), so a pair of days
    that fails the forecast moves to the next weekday pair."""
    g = WD.rng("services")
    order = ["CH07", "CH10", "CH05", "CH08", "CH03", "CH06", "CH09", "CH04", "CH02", "CH01"]
    d1 = dt.date(2026, 5, 5)
    out = {}
    hm = lambda x: (x // 60, x % 60)
    m10 = lambda lo, hi: int(g.integers(lo // 10, hi // 10 + 1)) * 10
    taken = set()
    for t in order:
        s1 = 8 * 60 + m10(0, 30)
        iso1_end = 11 * 60 + m10(10, 60)
        back1 = 16 * 60 + m10(20, 60)
        s2 = 8 * 60 + m10(0, 30)
        iso2_from = 13 * 60 + m10(0, 50)
        iso2_to = iso2_from + m10(140, 190)
        while True:
            assert d1 < dt.date(2026, 9, 21), "no service window left for %s" % t
            if d1.weekday() > 3 or d1 in taken:
                d1 += dt.timedelta(days=1)
                continue
            d2 = d1 + dt.timedelta(days=1)
            a1, b1 = k_of(utc_of_local(d1, *hm(s1))), k_of(utc_of_local(d1, *hm(iso1_end)))
            a2, b2 = k_of(utc_of_local(d2, *hm(iso2_from))), k_of(utc_of_local(d2, *hm(iso2_to)))
            w1, w2 = m["v"][a1:b1].mean(), m["v"][a2:b2].mean()
            clash = t in MAJOR and k_of(MAJOR[t][0]) - 288 < b2 and a1 < k_of(MAJOR[t][3]) + 288
            if 6.0 <= w1 <= 11.0 and 6.0 <= w2 <= 11.0 and m["v"][a1:b2].max() < 15.0 and not clash:
                break
            d1 += dt.timedelta(days=1)
        taken |= {d1, d2}
        out[t] = dict(
            d1=d1, d2=d2,
            stop1=utc_of_local(d1, *hm(s1)), iso1_end=utc_of_local(d1, *hm(iso1_end)), back1=utc_of_local(d1, *hm(back1)),
            stop2=utc_of_local(d2, *hm(s2)), iso2_from=utc_of_local(d2, *hm(iso2_from)),
            iso2_to=utc_of_local(d2, *hm(iso2_to)),
            arrive1=s1 - m10(10, 30), leave1=back1 + m10(10, 20), arrive2=s2 - m10(10, 30),
            leave2=iso2_to + m10(20, 40), techs=sorted(g.choice(len(W.TECHNICIANS), 2, replace=False).tolist()))
        d1 = d2 + dt.timedelta(days=1 + int(g.integers(0, 3)))
    return out


MAJOR = {
    # turbine: (fault start UTC, crane isolation from, crane isolation to, back in service UTC)
    "CH09": (W.CH09_FAULT, dt.datetime(2026, 4, 20, 6, 30, tzinfo=W.UTC), dt.datetime(2026, 4, 24, 16, 0, tzinfo=W.UTC),
             W.CH09_BACK),
    "CH06": (dt.datetime(2026, 6, 29, 2, 40, tzinfo=W.UTC), dt.datetime(2026, 7, 13, 6, 50, tzinfo=W.UTC),
             dt.datetime(2026, 7, 16, 16, 20, tzinfo=W.UTC), dt.datetime(2026, 7, 17, 11, 10, tzinfo=W.UTC)),
}
POWER_LOSS = {   # faults that cut the auxiliary supply: silent from the trip until the technician resets
    "CH03": (dt.datetime(2025, 12, 11, 19, 50, tzinfo=W.UTC), dt.datetime(2025, 12, 12, 10, 30, tzinfo=W.UTC)),
    "CH08": (dt.datetime(2026, 8, 3, 4, 10, tzinfo=W.UTC), dt.datetime(2026, 8, 3, 13, 40, tzinfo=W.UTC)),
    "CH10": (dt.datetime(2026, 4, 17, 22, 30, tzinfo=W.UTC), dt.datetime(2026, 4, 18, 9, 20, tzinfo=W.UTC)),
}


def faults(bad, svc):
    """Ordinary faults: about a dozen a turbine a year, most cleared by a remote reset within hours, a few waiting for
    a technician (repair after the first two hours)."""
    out = {}
    for t in W.TURBINES:
        g = WD.rng("faults", t)
        busy = bad.copy()
        if t in MAJOR:
            f0, _, _, back = MAJOR[t]
            busy[k_of(f0) - 36:k_of(back) + 36] = True
        if t in POWER_LOSS:
            a, b = POWER_LOSS[t]
            busy[k_of(a) - 36:k_of(b) + 36] = True
        s = svc[t]
        busy[k_of(s["stop1"]) - 144:k_of(s["iso2_to"]) + 144] = True
        n = int(g.poisson(12))
        evs = []
        for _ in range(n):
            for _try in range(50):
                k0 = int(g.integers(200, N - 200))
                dur = int(np.clip(np.round(np.exp(g.normal(np.log(15), 1.05))), 2, 6 * 144))
                if not busy[k0 - 6:k0 + dur + 6].any():
                    busy[k0 - 6:k0 + dur + 6] = True
                    evs.append((k0, dur))
                    break
        out[t] = sorted(evs)
    return out


def anm(m, bad):
    """The network operator's ANM instructions: export limits for the farm's connection (MW), on ten-minute
    boundaries, more often when the wind is high, in spring and summer around midday when demand is low and the sun is
    up, and on winter nights; now and then a trip (limit zero)."""
    g = WD.rng("anm")
    rows = []
    taken = bad.copy()
    for day in range(W.DAYS):
        k_day = day * 144
        vday = m["v"][k_day:k_day + 144].mean()
        date = (W.START + dt.timedelta(days=day)).date()
        summer = date.month in (4, 5, 6, 7, 8, 9)
        autumn = date.month == 10 and date.year == 2025
        p = np.clip(0.04 + 0.05 * (vday - 6.5), 0.0, 0.55) + (0.14 if summer else 0.0) + (0.25 if autumn else 0.0)
        nblocks = int(g.random() < p) + int(g.random() < p * 0.35)
        for _ in range(nblocks):
            for _try in range(20):
                if summer:
                    lh = g.normal(12.5, 2.3)
                else:
                    lh = (g.normal(3.0, 2.5)) % 24
                k0 = k_day + int(np.clip(round((lh % 24) * 6), 0, 143)) - 6   # local to UTC, about an hour in summer
                dur = int(g.integers(18, 49)) if autumn else int(g.integers(6, 43))
                if k0 < 12 or k0 + dur > N - 12 or taken[k0 - 3:k0 + dur + 3].any():
                    continue
                taken[k0 - 3:k0 + dur + 3] = True
                lim = 0.0 if g.random() < 0.12 else (float(g.integers(12, 21)) / 2.0 if autumn else float(g.integers(16, 37)) / 2.0)
                rows.append((k0, k0 + dur, lim))
                break
    rows.sort()
    return rows


def simulate(m, T):
    bad = protected(m)
    svc = services(m)
    flt = faults(bad, svc)
    instr = anm(m, bad)
    limit = np.full(N, np.nan)
    for a, b, lim in instr:
        limit[a:b] = lim
    st = {t: np.zeros(N, int) for t in W.TURBINES}
    silent = {t: np.zeros(N, bool) for t in W.TURBINES}
    down = {t: np.zeros(N, bool) for t in W.TURBINES}         # downtime in OM-07's sense: fault, repair, service
    kind = {t: np.zeros(N, "U2") for t in W.TURBINES}         # the downtime's kind for the work orders and checks
    for t in W.TURBINES:
        s = st[t]
        s[:] = 10
        # downtime: faults
        for k0, dur in flt[t]:
            s[k0:k0 + dur] = 40
            if dur > 18:
                s[k0 + 12:k0 + dur] = 41
            down[t][k0:k0 + dur] = True
            kind[t][k0:k0 + dur] = "F"
        if t in POWER_LOSS:
            a, b = POWER_LOSS[t]
            ka, kb = k_of(a), k_of(b)
            s[ka:kb + 5] = 41
            silent[t][ka:kb] = True
            down[t][ka:kb + 5] = True
            kind[t][ka:kb + 5] = "P"
        if t in MAJOR:
            f0, c0, c1, back = MAJOR[t]
            k0, kb = k_of(f0), k_of(back)
            s[k0:k0 + 12] = 40
            s[k0 + 12:kb] = 41
            silent[t][k_of(c0):k_of(c1)] = True
            down[t][k0:kb] = True
            kind[t][k0:kb] = "M"
        sv = svc[t]
        k1, ki1, kb1 = k_of(sv["stop1"]), k_of(sv["iso1_end"]), k_of(sv["back1"])
        k2, ki2a, ki2b = k_of(sv["stop2"]), k_of(sv["iso2_from"]), k_of(sv["iso2_to"])
        s[k1:kb1] = 30
        silent[t][k1:ki1] = True
        s[k2:ki2b] = 30
        silent[t][ki2a:ki2b] = True
        s[ki2b] = 20                                            # the restart: ready for one interval
        for a_, b_ in ((k1, kb1), (k2, ki2b)):
            down[t][a_:b_] = True
            kind[t][a_:b_] = "S"
    # grid loss: every turbine, recorded for the first half hour on the UPS and the twenty minutes of re-energising
    ga, gb = k_of(W.GRID_LOSS[0]), k_of(W.GRID_LOSS[1])
    for t in W.TURBINES:
        assert not down[t][ga - 6:gb + 8].any()
        st[t][ga:gb + 2] = 61
        silent[t][ga + 3:gb] = True
    co_a, co_b = k_of(W.COMMS_OUTAGE[0]), k_of(W.COMMS_OUTAGE[1])
    for t in W.TURBINES:
        silent[t][co_a:co_b] = True
    # ice: in-cloud freezing at the mast, detected turbine by turbine, cleared hours after the cloud lifts
    gi = WD.rng("ice")
    icy = (m["temp"] < -0.3) & (m["rh"] > 95.5)
    icy[bad] = False
    spans = []
    k = 0
    while k < N:
        if icy[k]:
            j = k
            while j < N and icy[j]:
                j += 1
            if j - k >= 4:
                spans.append((k, j))
            k = j
        else:
            k += 1
    for t in W.TURBINES:
        hi = (W.ELEVATION[t] - 390) / 70.0
        for a, b in spans:
            if gi.random() < 0.55 + 0.35 * hi:
                a2 = a + int(gi.integers(2, 6))
                b2 = min(N - 12, b + int(gi.integers(12, 36)))
                sel = np.arange(a2, b2)
                sel = sel[(st[t][sel] == 10) & ~bad[sel]]
                st[t][sel] = 22
    # wind: high-wind stops with hysteresis, low wind
    for t in W.TURBINES:
        v = T[t]["v"]
        s = st[t]
        stopped = False
        for k in range(N):
            if s[k] != 10:
                stopped = False if s[k] != 21 else stopped
                continue
            if stopped:
                if v[k] < W.RESTART:
                    stopped = False
                else:
                    s[k] = 21
                    continue
            if v[k] > W.CUT_OUT:
                s[k] = 21
                stopped = True
            elif T[t]["pfree"][k] < 0.5:
                s[k] = 20
    # power: free power where running; limits from ANM and noise mode; nothing where stopped
    p = {t: np.where(st[t] == 10, T[t]["pfree"], 0.0) for t in W.TURBINES}
    lh = np.array([local_hour(k) for k in range(N)])
    night = (lh >= W.NOISE_HOURS[0]) | (lh < W.NOISE_HOURS[1])
    noise = night & WD.in_sector(m["dir"], *W.NOISE_SECTOR)
    gl = WD.rng("limits")
    running = np.vstack([st[t] == 10 for t in W.TURBINES])
    nrun = running.sum(0)
    has = ~np.isnan(limit)
    for i, t in enumerate(W.TURBINES):
        # an external setpoint below rated (noise mode, or the turbine's share of an ANM limit) puts the controller
        # in state 11 for as long as it is in force, whether or not the wind reaches it
        share = np.where(has & (nrun > 0), np.nan_to_num(limit) * 1000.0 / np.maximum(nrun, 1), np.inf)
        cap = np.minimum(np.where(noise & (t in W.NOISE_TURBINES), W.NOISE_CAP_KW, np.inf), share)
        active = running[i] & (cap < W.RATED_KW)
        trip = running[i] & has & (np.nan_to_num(limit, nan=1.0) == 0.0)
        bind = active & (p[t] > cap)
        p[t] = np.where(bind, np.maximum(cap - np.abs(gl.normal(0, 4, N)), 0.0), p[t])
        st[t] = np.where(active, 11, st[t])
        st[t] = np.where(trip, 60, st[t])
        p[t] = np.where(trip, 0.0, p[t])
    return dict(state=st, power=p, silent=silent, down=down, kind=kind, services=svc, faults=flt, anm=instr,
                limit=limit, noise=noise)
