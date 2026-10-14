"""The hourly truth: each offered plant's 2024 and 2025, hour by hour in local standard time (UTC-8).

Ambient temperature by climate zone; a dispatch the plant's style and the season drive; forced, maintenance and
planned outages and reserve shutdowns as GADS events; each monitored stack's operating time, gross load, heat input,
CO2, NOx and SO2; the plant's net output at its revenue meter (negative while it sits idle and draws station
service); the stacks' substitute-data episodes. Nothing here is written to the pack; pack.py does that."""
import datetime as dt
import math

import numpy as np

import world as W

N = W.NHOURS
DAYS = N // 24


def t_of(h):
    return dt.datetime.combine(W.FIRST_DAY, dt.time()) + dt.timedelta(hours=int(h))


def ambient(rng, zone):
    c = W.CLIMATE[zone]
    doy = np.array([(W.FIRST_DAY + dt.timedelta(days=d)).timetuple().tm_yday for d in range(DAYS)])
    seas = c["mean"] + c["amp"] * np.cos(2 * math.pi * (doy - 200) / 365.25)
    noise = np.zeros(DAYS)
    for d in range(1, DAYS):
        noise[d] = 0.78 * noise[d - 1] + rng.normal(0, c["sd"])
    daily = seas + noise
    hod = np.arange(24)
    diurnal = c["diurnal"] * np.cos(2 * math.pi * (hod - 15) / 24)
    T = (daily[:, None] + diurnal[None, :] + rng.normal(0, 1.2, (DAYS, 24))).reshape(-1)
    return T


# ------------------------------------------------------------------------------------------------- dispatch
SPRING = (3, 4, 5, 6)


def plan(rng, p, T):
    """desired hourly operation before outages: x[h] the unfired load as a fraction of capability (0 off) and
    fire[h] the duct firing MW"""
    style = p["disp"]
    x = np.zeros(N)
    fire = np.zeros(N)
    on_day_prob = {1: .78, 2: .62, 3: .32, 4: .14, 5: .2, 6: .46, 7: .86, 8: .88, 9: .62, 10: .5, 11: .62, 12: .78}
    week_prob = {1: .86, 2: .82, 3: .55, 4: .18, 5: .22, 6: .6, 7: .9, 8: .92, 9: .74, 10: .62, 11: .8, 12: .86}
    week_on = {}
    prev_day_on = False
    prev_stop_h = -1
    for d in range(DAYS):
        date = W.FIRST_DAY + dt.timedelta(days=d)
        m, wd = date.month, date.weekday()
        base = d * 24
        if style == "base":
            spring_weekend_off = (m in (4, 5) and wd >= 5 and ((date - W.FIRST_DAY).days // 7 + p["code"]) % 3 == 0)
            for hh in range(24):
                if spring_weekend_off:
                    continue
                night = hh < 6 or hh >= 23
                if night:
                    v = rng.uniform(0.76, 0.9) if m in SPRING else rng.uniform(0.88, 0.97)
                else:
                    v = rng.uniform(0.95, 1.0) if not (m in SPRING and 10 <= hh <= 15) else rng.uniform(0.84, 0.97)
                x[base + hh] = v
        elif style in ("cycle_daily", "cycle_seasonal", "mid"):
            if style == "cycle_seasonal":
                inseason = (date >= dt.date(date.year, 6, 12) and date <= dt.date(date.year, 9, 22)) or \
                    (date >= dt.date(date.year, 11, 8)) or (date <= dt.date(date.year, 2, 26))
                prob = (0.82 if wd < 5 else 0.3) if inseason else 0.0
            elif style == "mid":
                prob = None if m in (12, 1, 2, 7, 8, 9) else (0.74 if wd < 5 else 0.3)
            else:
                prob = on_day_prob[m] * (1.0 if wd < 5 else 0.42)
            if prob is None:              # mid in its base months
                for hh in range(24):
                    night = hh < 6 or hh >= 23
                    x[base + hh] = rng.uniform(0.62, 0.8) if night else rng.uniform(0.9, 1.0)
                prev_day_on = True
                continue
            on = rng.random() < prob
            if on:
                start = 5 if rng.random() < 0.5 else 6
                stop = 22 if rng.random() < 0.55 else 23
                overnight = prev_day_on and prev_stop_h >= 0 and m in (1, 7, 8, 12) and rng.random() < 0.35
                if overnight:              # stayed on through the night at minimum load
                    for h in range(prev_stop_h, base + start):
                        x[h] = rng.uniform(0.48, 0.53)
                for hh in range(start, stop):
                    if hh < start + 3:
                        v = rng.uniform(0.48, 0.62)
                    elif hh < 15:
                        v = rng.uniform(0.55, 0.8) if m not in (7, 8) else rng.uniform(0.7, 0.95)
                    elif hh < 21:
                        v = rng.uniform(0.72, 1.0)
                    else:
                        v = rng.uniform(0.48, 0.6)
                    x[base + hh] = v
                prev_stop_h = base + stop
            prev_day_on = on
        elif style == "cycle_weekly":
            wk = (date - W.FIRST_DAY).days // 7
            if wk not in week_on:
                week_on[wk] = rng.random() < week_prob[m]
            if not week_on[wk]:
                continue
            for hh in range(24):
                if wd == 0 and hh < 4:
                    continue
                if wd == 5 and hh >= 1:
                    continue
                if wd == 6:
                    continue
                night = hh < 6 or hh >= 23
                x[base + hh] = rng.uniform(0.55, 0.63) if night else rng.uniform(0.8, 1.0)
    # output follows load from hour to hour: a five-hour average inside each run (three hours near its ends)
    on = x > 0
    xs = x.copy()
    for h in range(N):
        if not on[h]:
            continue
        for k in (2, 1):
            if h - k >= 0 and h + k < N and on[h - k:h + k + 1].all():
                xs[h] = x[h - k:h + k + 1].mean()
                break
    x = xs
    # duct firing over the heavy-load hours of a hot or a cold day, at one level for the day
    if p["db"] > 0:
        for d in range(DAYS):
            base = d * 24
            tmax = T[base + 12:base + 20].max()
            tmin = T[base + 6:base + 22].min()
            if tmax > 86 and rng.random() < 0.8:
                hrs, level = range(10, 22), p["db"] * rng.uniform(0.55, 1.0)
            elif tmin < 22 and rng.random() < 0.65:
                hrs, level = range(6, 22), p["db"] * rng.uniform(0.4, 0.9)
            else:
                continue
            for hh in hrs:
                if x[base + hh] >= 0.8:
                    x[base + hh] = 1.0
                    fire[base + hh] = level * rng.uniform(0.97, 1.0)
    return x, fire


# ------------------------------------------------------------------------------------------------- outages
FORCED = ("U1", "U2", "U3", "SF")


def outage_events(rng, p, x=None):
    """forced, maintenance and planned events (truth), minute precision, local standard time. Each: dict(units,
    type, start, end, scope) where scope is 'plant', 'ct' (one combustion turbine) or 'st' (the steam turbine)"""
    units = W.gads_units(p["key"])
    ev = []
    t0 = dt.datetime.combine(W.FIRST_DAY, dt.time())
    t1 = dt.datetime.combine(W.LAST_DAY, dt.time()) + dt.timedelta(days=1)
    # planned outage each spring (combined cycles take theirs in the hydro season)
    for yr in (2024, 2025):
        s = dt.datetime(yr, 4, 1) + dt.timedelta(days=int(rng.integers(0, 40)), hours=int(rng.integers(0, 24)))
        dur = dt.timedelta(days=int(rng.integers(9, 22)), hours=int(rng.integers(0, 24)), minutes=int(rng.integers(0, 60)))
        ev.append(dict(units=list(units), type="PO", start=s, end=s + dur, scope="plant"))
    # forced events, a few a year
    lam = 6.5 if p["disp"] != "base" else 5.5
    for yr in (2024, 2025):
        k = int(rng.poisson(lam))
        for _ in range(k):
            s = dt.datetime(yr, 1, 1) + dt.timedelta(minutes=int(rng.integers(0, 365 * 24 * 60)))
            hours = float(np.clip(rng.lognormal(math.log(11), 1.0), 1.2, 140))
            e = s + dt.timedelta(minutes=int(round(hours * 60)))
            typ = rng.choice(["U1", "U1", "U1", "U2", "U3", "SF"] if p["disp"] != "base" else ["U1", "U1", "U1", "U2", "U3"])
            if typ == "SF" and x is not None:
                # a start-up failure: at one of the year's planned starts, delaying it
                lo = (dt.datetime(yr, 1, 1) - t0).days * 24
                want = x[lo:lo + 8760] > 0
                starts = np.nonzero(want[1:] & ~want[:-1])[0] + 1
                if len(starts):
                    hs = lo + int(starts[int(rng.integers(0, len(starts)))])
                    s = t0 + dt.timedelta(hours=hs, minutes=int(rng.integers(5, 50)))
                hours = float(rng.uniform(1.5, 9))
                e = s + dt.timedelta(minutes=int(round(hours * 60)))
            if p["config"] == "1x1ss":
                scope = "plant"
            else:
                r = rng.random()
                if p["config"] == "2x1":
                    scope = "plant" if r < 0.4 else ("ct" if r < 0.78 else "st")
                else:
                    scope = "plant" if r < 0.45 else ("ct" if r < 0.72 else "st")
            if scope == "plant":
                us = list(units)
            elif scope == "ct":
                cts = [u for u in units if u.startswith("CT")]
                us = [cts[int(rng.integers(0, len(cts)))]]
            else:
                us = ["ST1"]
            ev.append(dict(units=us, type=str(typ), start=s, end=e, scope=scope))
    # a maintenance outage or two
    for yr in (2024, 2025):
        if rng.random() < 0.7:
            s = dt.datetime(yr, int(rng.choice([3, 9, 10, 11])), int(rng.integers(1, 26)), int(rng.integers(0, 24)))
            e = s + dt.timedelta(hours=int(rng.integers(20, 70)))
            ev.append(dict(units=list(units), type="MO", start=s, end=e, scope="plant"))
    # every plant has a few forced events in 2025, and where a single unit's loss leaves the plant running (one
    # turbine of a 2x1, the steam turbine where the turbines can bypass their steam generators) at least one of those
    y0, y1 = dt.datetime(2025, 1, 1), dt.datetime(2026, 1, 1)
    def add(scope, typ="U1", lo=y0, span=364):
        s = lo + dt.timedelta(minutes=int(rng.integers(0, span * 24 * 60)))
        hours = float(np.clip(rng.lognormal(math.log(14), 0.7), 3.0, 90))
        if scope == "plant":
            us = list(units)
        elif scope == "ct":
            cts = [u for u in units if u.startswith("CT")]
            us = [cts[int(rng.integers(0, len(cts)))]]
        else:
            us = ["ST1"]
        ev.append(dict(units=us, type=typ, start=s, end=s + dt.timedelta(minutes=int(round(hours * 60))), scope=scope))
    single = "ct" if p["config"] == "2x1" else ("st" if p["config"] == "1x1" and p["bypass"] == "Y" else None)
    if single and not any(e["scope"] == single and e["type"] in FORCED and y0 <= e["start"] < y1 for e in ev):
        add(single)
    while sum(1 for e in ev if e["type"] in FORCED and y0 <= e["start"] < y1 and e["scope"] == "plant") < 2:
        add("plant")
    for key, (a, b) in W.BOUNDARY.items():
        if key == p["key"]:
            ev.append(dict(units=list(units), type="U1", start=a, end=b, scope="plant"))
    ev = [e for e in ev if e["start"] < t1 and e["end"] > t0]
    ev.sort(key=lambda e: (e["start"], e["type"] not in FORCED))
    # no two events on the same unit overlap (the later one starts after the earlier ends)
    out = []
    keep = [e for e in ev if (e["start"], e["end"]) in W.BOUNDARY.values()]
    for e in keep + [e for e in ev if e not in keep]:
        clash = any(set(e["units"]) & set(o["units"]) and e["start"] < o["end"] + dt.timedelta(hours=2)
                    and o["start"] < e["end"] + dt.timedelta(hours=2) for o in out)
        if not clash:
            out.append(e)
    out.sort(key=lambda e: e["start"])
    return out


def mode_by_hour(p, events):
    """per hour: the share of the hour each configuration held. mode codes: 'full', 'half' (one turbine of a 2x1 out),
    'sc' (steam turbine out, turbines on bypass), 'out'"""
    t0 = dt.datetime.combine(W.FIRST_DAY, dt.time())
    unit_out = {u: np.zeros(N) for u in W.gads_units(p["key"])}      # fraction of each hour the unit is out
    for e in events:
        a = (e["start"] - t0).total_seconds() / 3600.0
        b = (e["end"] - t0).total_seconds() / 3600.0
        a, b = max(a, 0.0), min(b, float(N))
        for u in e["units"]:
            h = int(math.floor(a))
            while h < b and h < N:
                lo, hi = max(a, h), min(b, h + 1)
                unit_out[u][h] = max(unit_out[u][h], hi - lo)
                h += 1
    return unit_out


def plant_state(p, unit_out):
    """the plant's configuration each hour from its units' availability, and the share of the hour available"""
    cfg = p["config"]
    full_out = np.zeros(N)
    mode = np.array(["full"] * N, dtype=object)
    if cfg == "1x1ss":
        full_out = unit_out["CS1"]
    elif cfg == "1x1":
        ct, st = unit_out["CT1"], unit_out["ST1"]
        st_kill = st if p["bypass"] == "N" else np.zeros(N)
        full_out = np.maximum(ct, st_kill)
        if p["bypass"] == "Y":
            mode[(st > 0.5) & (ct < 0.5)] = "sc"
    else:
        c1, c2, st = unit_out["CT1"], unit_out["CT2"], unit_out["ST1"]
        both = np.minimum(c1, c2)
        st_kill = st if p["bypass"] == "N" else np.zeros(N)
        full_out = np.maximum(both, st_kill)
        mode[((c1 > 0.5) ^ (c2 > 0.5)) & (full_out < 0.5)] = "half"
        if p["bypass"] == "Y":
            mode[(st > 0.5) & (full_out < 0.5)] = "sc"
    mode[full_out >= 0.999] = "out"
    return full_out, mode


# ------------------------------------------------------------------------------------------------- physics
def hr_unfired(p, x, t):
    return p["hr"] * (1.0 + 0.00045 * np.abs(t - 59.0)) * (1.0 + p["pl"] * np.clip(1.0 - x, 0.0, None) ** 1.7)


def plant_out_forced(p, events):
    """the intervals the whole plant was out on a forced event: every combustion turbine (or the single-shaft unit)
    out, a steam turbine trip taking the turbines with it where they cannot bypass their steam generators"""
    def kills(e):
        if e["type"] not in FORCED:
            return False
        if e["scope"] == "plant" or p["config"] == "1x1ss":
            return True
        if e["scope"] == "ct":
            return p["config"] == "1x1"
        return p["bypass"] == "N"
    iv = sorted((e["start"], e["end"]) for e in events if kills(e))
    if p["config"] == "2x1":
        cts = {}
        for e in events:
            if e["type"] in FORCED and e["scope"] == "ct":
                cts.setdefault(e["units"][0], []).append((e["start"], e["end"]))
        a, b = cts.get("CT1", []), cts.get("CT2", [])
        for s1, e1 in a:
            for s2, e2 in b:
                lo, hi = max(s1, s2), min(e1, e2)
                if lo < hi:
                    iv.append((lo, hi))
        iv.sort()
    out = []
    for a, b in iv:
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def forced_hours_2025(p, events):
    y0, y1 = dt.datetime(2025, 1, 1), dt.datetime(2026, 1, 1)
    tot = 0.0
    for a, b in plant_out_forced(p, events):
        lo, hi = max(a, y0), min(b, y1)
        if lo < hi:
            tot += (hi - lo).total_seconds() / 3600.0
    return tot


def nudge_forced(p, events, used=()):
    """keep the plant's 2025 forced outage hours off a rounding edge, off a round number and off another plant's
    count: the longest 2025 plant outage ends a few minutes later until they are"""
    y0, y1 = dt.datetime(2025, 1, 1), dt.datetime(2026, 1, 1)
    for _ in range(80):
        fo = forced_hours_2025(p, events)
        frac = fo - math.floor(fo)
        if abs(frac - 0.5) >= 0.15 and abs(fo - round(fo, -1)) >= 0.3 and int(round(fo)) not in used:
            return
        cands = [e for e in events if e["type"] in FORCED and e["scope"] == "plant" and y0 <= e["start"] and e["end"] < y1]
        e = max(cands, key=lambda e: e["end"] - e["start"])
        e["end"] = e["end"] + dt.timedelta(minutes=7)


def run_plant(rng, p, T, used=()):
    key = p["key"]
    x, fire = plan(rng, p, T)
    events = outage_events(rng, p, x)
    nudge_forced(p, events, used)
    unit_out = mode_by_hour(p, events)
    full_out, mode = plant_state(p, unit_out)
    avail = 1.0 - full_out                        # share of the hour the plant could run
    want = x > 0
    op = np.where(want, avail, 0.0)               # operating time (plant level)
    op[mode == "out"] = 0.0
    on = op > 0.001
    prev_on = np.concatenate([[False], on[:-1]])
    next_on = np.concatenate([on[1:], [False]])
    start = on & ~prev_on
    stop = on & ~next_on
    # hours off before each start, for the start's temperature (hot, warm, cold)
    off_run = np.zeros(N)
    c = 999.0
    for h in range(N):
        off_run[h] = c
        c = 0.0 if on[h] else c + 1.0
    cap = np.array([W.cap_unfired(p["pmax"], t) for t in T])
    xs = x.copy()
    xs[start] = rng.uniform(0.34, 0.46, start.sum())
    xs[stop & ~start] = np.minimum(xs[stop & ~start], rng.uniform(0.36, 0.52, (stop & ~start).sum()))
    after = np.concatenate([[False], start[:-1]]) & on
    xs[after] = np.maximum(np.minimum(xs[after], rng.uniform(0.6, 0.76, after.sum())), 0.6)
    fire = np.where(start | stop | after, 0.0, fire)
    # partial operating time at a start or a stop
    u = op.copy()
    u[start] = np.minimum(u[start], rng.uniform(0.35, 0.82, start.sum()))
    u[stop & ~start] = np.minimum(u[stop & ~start], rng.uniform(0.3, 0.75, (stop & ~start).sum()))
    # configuration
    modecap = np.where(mode == "half", 0.5, np.where(mode == "sc", 0.66, 1.0))
    xs = np.where(mode == "full", xs, np.minimum(xs, 0.97))
    fire = np.where(mode == "full", fire, 0.0)
    Pun = xs * cap * modecap                        # gross MW unfired, average over operating time
    Ptot = Pun + fire
    hr = hr_unfired(p, xs, T)
    hr = np.where(mode == "sc", hr * 1.45, np.where(mode == "half", hr * 1.03, hr))
    hr = np.where(after, hr * 1.06, hr)
    hi_rate = (Pun * hr + fire * p["dbhr"]) / 1000.0     # mmBtu per hour of operation
    hi = hi_rate * u
    sfac = np.where(off_run > 48, 4.6, np.where(off_run > 10, 3.4, 2.4)) * p.get("sf", 1.0)
    hi = hi + np.where(start, sfac * p["pmax"], 0.0)
    hi = np.where(on, hi * rng.normal(1.0, 0.004, N), 0.0)
    gross_mwh = np.where(on, Ptot * u, 0.0)
    aux_on = p["f0"] * p["pmax"] * modecap * u + p["f1"] * gross_mwh
    ss = 0.0022 * p["pmax"] * (1.0 - u) * rng.uniform(0.85, 1.15, N)
    net = np.where(on, gross_mwh - aux_on - ss, -0.0022 * p["pmax"] * rng.uniform(0.8, 1.2, N))
    co2 = hi * W.CO2_PER_MMBTU
    return dict(key=key, x=x, xs=xs, fire=fire, op=u, on=on, start=start, stop=stop, after=after, mode=mode,
                cap=cap, Ptot=np.where(on, Ptot, 0.0), hi=hi, co2=co2, net=net, gross_mwh=gross_mwh,
                events=events, unit_out=unit_out, full_out=full_out, T=T)


def commitment_truth(p, T):
    """the plant held at its contract capacity in every hour of the 2024 and 2025 weather (no starts, no outages):
    pounds of CO2 per net MWh"""
    offer = offer_mw(p)
    g = (offer + p["f0"] * p["pmax"]) / (1.0 - p["f1"])
    cap = np.array([W.cap_unfired(p["pmax"], t) for t in T])
    un = np.minimum(g, cap)
    fired = np.clip(g - cap, 0.0, None)
    hi = (un * hr_unfired(p, un / cap, T) + fired * p["dbhr"]) / 1000.0
    return hi.sum() * W.CO2_PER_MMBTU * 2000.0 / (offer * len(T))


def offer_mw(p):
    """the contract capacity each seller offered: net MW at the 100 F design day, unfired or with the duct burners
    at full, rounded down to 5 MW"""
    cap = W.cap_unfired(p["pmax"], W.DESIGN_T)
    g = cap + (p["db"] if p["offer"] == "fired" else 0.0)
    net = g * (1.0 - p["f1"]) - p["f0"] * p["pmax"]
    return float(int(net // 5) * 5)


def substitute_episodes(rng, p, stacks, on):
    """heat input substitute-data episodes per stack (a fuel flowmeter out of service or failing its quality
    assurance, a data acquisition outage) and NOx monitor substitute episodes; each a list of (first hour, hours). A
    data acquisition outage at a two-turbine plant takes both stacks' records at once."""
    def when(lo, need_on=True):
        for _try in range(600):
            h = lo + int(rng.integers(0, 8760 - 60))
            if not need_on or on[h]:
                return h
        return h
    hi_ep, nox_ep = {}, {}
    for s in stacks:
        eps = []
        for yr, lo in ((2024, 0), (2025, W.H2025)):
            for _ in range(1 + int(rng.integers(0, 3))):
                eps.append((when(lo), int(rng.integers(3, 38))))
        hi_ep[s] = eps
        eps = []
        for yr, lo in ((2024, 0), (2025, W.H2025)):
            for _ in range(2 + int(rng.integers(0, 4))):
                eps.append((when(lo, need_on=(yr == 2025)), int(rng.integers(2, 30))))
        nox_ep[s] = eps
    if len(stacks) == 2:
        for lo in (0, W.H2025):
            h, n = when(lo), int(rng.integers(8, 30))
            for s in stacks:
                hi_ep[s].append((h, n))
                nox_ep[s].append((h, n))
    return hi_ep, nox_ep


def simulate(seed=W.SEED):
    rng = np.random.default_rng(seed)
    T = {z: ambient(rng, z) for z in ("east", "west")}
    out = {}
    used = set()
    for p in W.PLANTS:
        r = run_plant(rng, p, T[p["zone"]], used)
        used.add(int(round(forced_hours_2025(p, r["events"]))))
        r["truth_commit"] = commitment_truth(p, T[p["zone"]])
        r["offer"] = offer_mw(p)
        stacks_all = W.stacks(p["key"])
        r["hi_sub"], r["nox_sub"] = substitute_episodes(rng, p, stacks_all, r["on"])
        out[p["key"]] = r
    # no two plants share a count of 2025 substitute-data hours: a later plant's first 2025 episode runs an hour longer
    seen = set()
    for p in W.PLANTS:
        r = out[p["key"]]
        for _ in range(30):
            n = substitute_hours_2025(r)
            if n not in seen and n % 10:
                break
            s0 = W.stacks(p["key"])[0]
            eps = r["hi_sub"][s0]
            i = next(i for i, (h, k) in enumerate(eps) if h >= W.H2025)
            eps[i] = (eps[i][0], eps[i][1] + 1)
        seen.add(substitute_hours_2025(r))
    return dict(T=T, plants=out, rng_state=rng.bit_generator.state["state"]["state"])


def substitute_hours_2025(r):
    """plant hours in 2025 in which an operating stack's heat input came from substitute data (stack operation
    as pack.stack_series reads it)"""
    import pack as P
    st = P.stack_series(dict(plants={r["key"]: r}), r["key"])
    sel = np.zeros(N, bool)
    for d in st.values():
        sel |= d["hi_sub"]
    return int(sel[W.H2025:].sum())
