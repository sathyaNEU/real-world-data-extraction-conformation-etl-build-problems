"""The clean truth of 2026 on the Marsh and Wolds network, simulated at one minute with event-exact pump switching.

Each station's inflow is its dry weather flow on a local-time diurnal profile, the runoff its impervious area
sends from the radar zone's rain through a fast and a slow store, winter infiltration and, at Hagworth Wold, the
chalk groundwater that fills its sewer from January to March. The wet well fills and draws between the duty
pump's stop and start levels; a pump delivers its own rate (rated duty times the station's delivered fraction,
the two pumps a fraction of a per cent apart) whatever the level; when inflow beats the running pump the level
rises to the overflow weir and the excess spills. Every switching time is solved inside the minute, so the
telemetry's start and stop seconds are what the outstation would log. The event duration monitors see the
spills through their own sensors, thresholds, debounce, clocks and outages, and the three flow meters average
what their pumps moved over each fifteen minutes."""
import datetime as dt

import numpy as np

import world as W

NDAY = 365
MIN = NDAY * 1440
T0 = dt.datetime(2026, 1, 1, 0, 0, 0)          # UTC
BST0 = int((W.BST_START_UTC - T0).total_seconds() // 60)
BST1 = int((W.BST_END_UTC - T0).total_seconds() // 60)


def local_offset_min(minute_utc):
    """Minutes to add to UTC for UK local time at a UTC minute of 2026."""
    return 60 if BST0 <= minute_utc < BST1 else 0


# ---------------------------------------------------------------- rainfall
def make_rain(rng):
    """Rain in mm per minute for the five radar zones. Frontal systems cross every zone with a lag and a
    zone-specific depth; convective cells hit one or two zones hard. Wetter October to February."""
    nz = len(W.ZONES)
    rain = np.zeros((nz, MIN))
    day = 0.0
    while True:
        season = np.cos(2 * np.pi * (day - 345) / 365)
        rate = 0.21 + 0.11 * season
        day += rng.exponential(1.0 / rate)
        if day >= NDAY:
            break
        start = int(day * 1440)
        frontal = rng.random() < (0.72 + 0.18 * season)
        if frontal:
            dur = int(np.clip(rng.gamma(2.2, 150), 45, 1500))
            depth = rng.gamma(1.6, 4.2)
            zones = range(nz)
        else:
            dur = int(np.clip(rng.gamma(1.8, 40), 15, 240))
            depth = rng.gamma(1.3, 6.5)
            zones = rng.choice(nz, size=rng.integers(1, 3), replace=False)
        nb = max(dur // 10, 1)
        prof = rng.dirichlet(np.ones(nb) * (0.9 if frontal else 0.5))
        mm = np.repeat(prof * depth / 10.0, 10)[:dur]
        for z in zones:
            lag = int(rng.integers(0, 50)) if frontal else int(rng.integers(0, 15))
            f = rng.lognormal(0, 0.28 if frontal else 0.55)
            s0 = start + lag
            e = min(s0 + len(mm), MIN)
            if s0 < MIN:
                rain[z, s0:e] += mm[: e - s0] * f
    return rain


def stores(x, k_fast, k_slow, slow_share):
    """Runoff in l/s from rain mm/min over one hectare through a fast and a slow linear store."""
    q = x * 10000.0 / 60.0
    out = np.empty_like(q)
    af, as_ = 1.0 / k_fast, 1.0 / k_slow
    sf = ss = 0.0
    for i in range(len(q)):
        sf += (1 - slow_share) * q[i] - af * sf
        ss += slow_share * q[i] - as_ * ss
        out[i] = af * sf + as_ * ss
    return out


def diurnal_local():
    """Dry weather flow multiplier for each UTC minute of 2026, following local clock time."""
    t = np.arange(MIN)
    loc = t + np.where((t >= BST0) & (t < BST1), 60, 0)
    hod = (loc % 1440) / 60.0
    m = (1.0 + 0.42 * np.exp(-0.5 * ((hod - 8.6) / 1.6) ** 2) + 0.30 * np.exp(-0.5 * ((hod - 19.8) / 2.1) ** 2)
         - 0.48 * np.exp(-0.5 * ((hod - 4.0) / 1.9) ** 2))
    return m / m.mean()


# ---------------------------------------------------------------- one station
def station_inflow(st, rain, diurnal, rng):
    z = W.ZONES.index(st["zone"])
    runoff = stores(rain[z], k_fast=rng.uniform(32, 55), k_slow=rng.uniform(1800, 3200), slow_share=0.16) * st["imperv"]
    doy = np.arange(MIN) / 1440.0
    winter = 1.0 + 0.10 * np.clip(np.cos(2 * np.pi * (doy - 30) / 365), 0, None)
    q = st["dwf"] * diurnal * winter + runoff
    if st.get("gw_base", 0) > 0:
        # chalk groundwater seeping into the sewer all year, highest in late winter
        q = q + st["gw_base"] * (0.85 + 0.15 * np.cos(2 * np.pi * (doy - 44) / 365)) * st["rated"] * st["d"]
    if st["gw"] > 0:
        # the late-winter rise: from late December, peaking mid February, gone by early April
        g = np.clip(np.cos(np.pi * (doy - 44) / 96), 0, None) ** 2 * (doy < 92)
        q = q + g * st["gw"] * st["rated"] * st["d"]
    noise = np.repeat(rng.normal(0, 0.035, MIN // 5 + 1), 5)[:MIN]
    return np.maximum(q * (1 + noise), 0.25 * st["dwf"])


def run_station(st, qin, rng):
    """Event-exact wet well. Returns pump events (seconds from T0 UTC, pump, state, level), spill intervals
    (seconds) and the level at every fifteen-minute mark."""
    A = (np.pi * (st["well"][1] / 2) ** 2 if st["well"][0] == "circular" else st["well"][1] * st["well"][2]) * 1000.0
    base = st["rated"] * st["d"]
    split = rng.uniform(0.001, 0.003)
    rate = {1: base * (1 + split / 2), 2: base * (1 - split / 2)}
    stop, start, weir = st["stop"], st["start"], st["weir"]
    hla = start + 0.55 * (weir - start)          # the high level float switch, resetting 60 mm below
    hla_lo = hla - 0.06
    h = 0.5 * (stop + start)
    running = 0          # 0 none, else pump number
    nxt = 1              # pump to start next
    spilling = False
    hl_on = False
    events, spills, highs, levels = [], [], [], np.empty(MIN // 15)
    for i in range(MIN):
        if i % 15 == 0:
            levels[i // 15] = h
        tt = 0.0
        q = qin[i]
        while tt < 60.0 - 1e-9:
            qp = rate[running] if running else 0.0
            net = q - qp
            r = net / A
            if spilling:
                if net < 0:
                    spilling = False
                    spills[-1][1] = i * 60 + tt
                else:
                    tt = 60.0
                    continue
            dt_ = None
            ev = None
            if r > 0:
                if not running and h < start:
                    dt_, ev = (start - h) / r, "start"
                elif not hl_on and h < hla:
                    dt_, ev = (hla - h) / r, "hla"
                elif h < weir:
                    dt_, ev = (weir - h) / r, "weir"
            elif r < 0 and running and h > stop:
                if hl_on and h > hla_lo:
                    dt_, ev = (hla_lo - h) / r, "hlo"
                else:
                    dt_, ev = (stop - h) / r, "stop"
            if dt_ is None or dt_ > 60.0 - tt:
                h += r * (60.0 - tt)
                tt = 60.0
                continue
            h += r * dt_
            tt += dt_
            ts = i * 60 + tt
            if ev == "start":
                h = start
                running = nxt
                nxt = 2 if nxt == 1 else 1
                events.append((ts, running, 1))
            elif ev == "stop":
                h = stop
                events.append((ts, running, 0))
                running = 0
            elif ev == "weir":
                h = weir
                spilling = True
                spills.append([ts, None])
            elif ev == "hla":
                h = hla
                hl_on = True
                highs.append([ts, None])
            elif ev == "hlo":
                h = hla_lo
                hl_on = False
                highs[-1][1] = ts
    if spills and spills[-1][1] is None:
        spills[-1][1] = MIN * 60.0
    if highs and highs[-1][1] is None:
        highs[-1][1] = MIN * 60.0
    return dict(events=events, spills=[(a, b) for a, b in spills], highs=[(a, b) for a, b in highs], levels=levels,
                rate=rate, area=A)


# ---------------------------------------------------------------- event duration monitors
def edm_detect(spills, rng, debounce_s, holdoff_s, clock_off_s, active, outages):
    """A monitor's own view of the spills: it logs a discharge once the chamber has been over the weir for its
    debounce, closes it once it has been back under for its hold-off (so short breaks merge), stamps its own
    clock and loses what falls in its outages. active: (from_s, to_s) the unit was installed; outages: list."""
    merged = []
    for a, b in spills:
        if b - a < debounce_s:
            continue
        a2 = a + debounce_s * rng.uniform(0.6, 1.0)
        b2 = b + holdoff_s * rng.uniform(0.7, 1.0)
        if merged and a2 <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b2)
        else:
            merged.append([a2, b2])
    out = []
    lo, hi = active
    for a, b in merged:
        a, b = max(a, lo), min(b, hi)
        if b <= a:
            continue
        pieces = [(a, b)]
        for (oa, ob) in outages:
            nxtp = []
            for (pa, pb) in pieces:
                if ob <= pa or oa >= pb:
                    nxtp.append((pa, pb))
                else:
                    if pa < oa:
                        nxtp.append((pa, oa))
                    if ob < pb:
                        nxtp.append((ob, pb))
            pieces = nxtp
        for (pa, pb) in pieces:
            if pb - pa >= 60:
                out.append((pa + clock_off_s, pb + clock_off_s))
    return out


def monitor_outages(rng, active, n_mean):
    """Offline spells: a flat battery or a lost logger, a few hours to several days."""
    lo, hi = active
    span = hi - lo
    k = rng.poisson(n_mean * span / (365 * 86400.0))
    out = []
    for _ in range(k):
        a = lo + rng.uniform(0, span)
        d = rng.choice([rng.uniform(2, 20) * 3600, rng.uniform(1, 6) * 86400], p=[0.6, 0.4])
        out.append((a, min(a + d, hi)))
    out.sort()
    return out


def meter_flow(r):
    """The flow meter's fifteen-minute mean of what the running pump moved."""
    pumped = np.zeros(MIN // 15)
    on = None
    for (ts, p, s) in r["events"]:
        if s == 1:
            on = (ts, p)
        elif on is not None:
            a, b = on[0], ts
            q = r["rate"][on[1]]
            ia, ib = int(a // 900), int(b // 900)
            for k in range(ia, ib + 1):
                lo_, hi_ = max(a, k * 900.0), min(b, (k + 1) * 900.0)
                if hi_ > lo_ and k < len(pumped):
                    pumped[k] += q * (hi_ - lo_) / 900.0
            on = None
    return pumped


def hydraulics(seed=W.SEED):
    rng = np.random.default_rng(seed)
    rain = make_rain(rng)
    diurnal = diurnal_local()
    S = dict(rain=rain, stations={})
    for st in W.STATIONS:
        srng = np.random.default_rng([seed, int(st["code"][3:])])
        qin = station_inflow(st, rain, diurnal, srng)
        r = run_station(st, qin, srng)
        r["qin_mean"] = float(qin.mean())
        r["qin_15"] = qin.reshape(-1, 15).mean(axis=1)
        if st["meter"]:
            r["meter_15"] = meter_flow(r)
        S["stations"][st["code"]] = r
    return S


def monitors(S, seed=W.SEED, variant=None):
    """Each overflow's event duration monitors in 2026: the register's unit, and at a replaced overflow the old
    unit that ran on beside its replacement until the crew came back for it."""
    variant = W.MON_VARIANT if variant is None else variant
    year_lo, year_hi = 0.0, MIN * 60.0
    for st in W.STATIONS:
        code = st["code"]
        r = S["stations"][code]
        mrng = np.random.default_rng([seed, int(code[3:]), 31, variant])
        mons = []
        if code in W.EDM_REPLACED:
            old, inst, rem = W.EDM_REPLACED[code]
            inst_s = ((dt.datetime.combine(inst, dt.time(10, 40)) - T0).total_seconds()
                      - 3600 + mrng.uniform(-5400, 7200))
            rem_s = ((dt.datetime.combine(rem, dt.time(11, 20)) - T0).total_seconds() - 3600
                     + mrng.uniform(-4000, 5000))
            mons.append(dict(serial=old, model="AQ7", active=(year_lo, rem_s)))
            mons.append(dict(serial=W.EDM_CURRENT[code], model="HX40", active=(inst_s, year_hi)))
        else:
            ser = W.EDM_CURRENT[code]
            mons.append(dict(serial=ser, model="HX40" if ser.startswith("HX") else "AQ7", active=(year_lo, year_hi)))
        hand = [mm["active"][0] for mm in mons if mm["model"] == "HX40" and code in W.EDM_REPLACED] + \
               [mm["active"][1] for mm in mons if mm["model"] == "AQ7" and code in W.EDM_REPLACED]
        for m in mons:
            if m["model"] == "AQ7":
                deb, hold, nout = 120.0, 300.0, 3.6
            else:
                deb, hold, nout = 60.0, 240.0, 1.6
            outs = monitor_outages(mrng, m["active"], nout)
            # no outage within two days of a handover, so a day watched by both units is watched by one at least
            outs = [(a, b) for (a, b) in outs if all(b < h - 2 * 86400 or a > h + 2 * 86400 for h in hand)]
            m["outages"] = outs
            m["clock_off"] = float(mrng.uniform(-45, 45))
            m["events"] = edm_detect(r["spills"], mrng, deb, hold, m["clock_off"], m["active"], m["outages"])
        r["monitors"] = mons
    return S


def run(seed=W.SEED):
    S = hydraulics(seed)
    monitors(S, seed)
    return S
