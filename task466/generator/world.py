"""The simulated world for task466 (architecture 2): Breck Hollow Landfill, a closed landfill owned by the Quarrow
Valley Regional Solid Waste Authority, its gas plant (two blowers, an enclosed flare, two engine-generators run by
Leyland Renewable Gas) and its surface emissions monitoring, January 2024 to December 2026.

Physics that carries the call (never written in any shipped file):
- the waste generates methane at a smooth, slowly declining rate G(t);
- while the blowers run, the gas plant captures CE x G(t) (CE = 0.90, the rule's Schedule 2 value) with a small
  weather-driven wobble;
- during a blower outage nothing is captured; the waste mass holds part of what it generates (up to about ten hours'
  generation) and lets the rest out through the cap;
- after the restart the wells draw off the held gas on top of the steady capture, limited by the blowers' spare
  capacity, so the capture runs high for a few hours to most of a day.

Everything is drawn from a fixed seed, so two builds are byte-identical.
"""
import datetime as dt

import numpy as np

import common as C

SEED = 466
T0 = C.utc(2024, 1, 1)
NH = 26376                      # hours, 2024-01-01 00:00 UTC to 2027-01-04 00:00 UTC (the export runs into January)
YEARS = (2024, 2025, 2026)

# rule constants (filed in the rule extract)
CE = 0.90                       # Schedule 2: final cap with geomembrane, gas system running continuously
OX = 0.10                       # share of uncaptured methane oxidised in the cap
DE = 0.99                       # destruction efficiency, engines and enclosed flare
RHO_N = 0.7168                  # kg of methane per normal cubic metre (0 C, 101.325 kPa)
RHO_S = RHO_N * 273.15 / 293.15  # kg per standard cubic metre at 20 C (the flare meter's own basis, never shipped)
TIERS = ((375.0, 0, "Tier 1"), (450.0, 118000, "Tier 2"), (1e9, 312000, "Tier 3"))

# generation and capture
G0 = 459.1                      # kg CH4 per hour at 2024-01-01
K_DECAY = 0.046                 # per year
W_PHI, W_SD = 0.95, 0.008       # hourly AR(1) wobble of the steady capture (barometric and wellfield)
KAPPA, D_STORE, CE_REC, TAU = 0.95, 10.0, 0.90, 3.0
BLOWER_NM3H = 1780.0            # the duty blower's capacity, normal m3/h of landfill gas

# engines and flare
ENG_CAP = 181.0                 # kg CH4 per hour each at full load
ENG_EFF = 0.392                 # electrical efficiency on methane LHV
LHV_KWH_PER_KG = 13.89          # methane lower heating value, kWh per kg
FLARE_CUTOFF_M3H = 45.0         # the flare meter's low-flow cut-off, in its own (standard) cubic metres

AREA_ACRES = 74.2


def rng(k=0):
    return np.random.default_rng(SEED * 1000 + k)


def hours():
    return [T0 + dt.timedelta(hours=i) for i in range(NH)]


def year_index(times):
    return np.array([t.year for t in times])


# ------------------------------------------------------------------------------------------------ outages
OUTAGE_TYPES = [
    # (cause text in the contractor's words, count per year, duration range h, planned?)
    ("Utility power failure", 12, (1.0, 5.5), False),
    ("Blower trip - high bearing temperature", 7, (0.8, 3.8), False),
    ("Condensate knockout high level - plant ESD", 5, (1.5, 6.0), False),
    ("Gas analyser fault - plant ESD", 4, (0.7, 2.6), False),
    ("Planned shutdown - blower and valve maintenance", 5, (9.0, 22.0), True),
    ("Storm - damage to plant supply line", 4, (18.0, 36.0), False),
    ("Annual shutdown - flare and header inspection", 1, (55.0, 72.0), True),
]


def draw_outages(year, r):
    """Outages for one year as (start UTC, duration hours, cause, planned), at least 60 hours apart."""
    events = []
    for cause, n, (lo, hi), planned in OUTAGE_TYPES:
        for _ in range(n):
            events.append((cause, float(r.uniform(lo, hi)), planned))
    order = r.permutation(len(events))
    events = [events[i] for i in order]
    jan1 = C.utc(year, 1, 1)
    n = len(events)
    # spread starts across the year with jitter, then enforce a 60-hour gap
    slots = np.linspace(30, 8700, n + 1)[:-1] + r.uniform(0, 8700 / n * 0.7, n)
    out = []
    last_end = None
    for (cause, d, planned), s in zip(events, slots):
        start = jan1 + dt.timedelta(hours=float(s))
        if planned:
            # planned work starts at 07:00 or 07:30 local on a weekday
            loc = C.local(start)
            day = loc.date()
            while dt.date.weekday(day) >= 5:
                day = day + dt.timedelta(days=1)
            minute = 0 if r.uniform() < 0.5 else 30
            start = dt.datetime(day.year, day.month, day.day, 7, minute, tzinfo=C.TZ).astimezone(C.UTC)
        else:
            start = start.replace(minute=int(r.integers(0, 60)), second=0, microsecond=0)
        if last_end is not None and start < last_end + dt.timedelta(hours=60):
            start = last_end + dt.timedelta(hours=60 + float(r.uniform(0, 30)))
            start = start.replace(second=0, microsecond=0)
        dur_min = int(round(d * 60))
        end = start + dt.timedelta(minutes=dur_min)
        if end.year != year:
            continue
        out.append(dict(start=start, end=end, hours=dur_min / 60.0, cause=cause, planned=planned))
        last_end = end
    return out


# ------------------------------------------------------------------------------------------------ the plant, hourly
def build():
    times = hours()
    yrs = year_index(times)
    t_years = np.arange(NH) / 8766.0
    r = rng(1)
    G = G0 * np.exp(-K_DECAY * t_years)                      # kg CH4/h generated
    # steady wobble, de-meaned within each year
    w = np.zeros(NH)
    innov = W_SD * np.sqrt(1 - W_PHI ** 2)
    e = r.normal(0, innov, NH)
    for i in range(1, NH):
        w[i] = W_PHI * w[i - 1] + e[i]
    for y in YEARS + (2027,):
        m = yrs == y
        w[m] -= w[m].mean()
    steady = CE * G * (1 + w)

    outages = []
    for y in YEARS:
        outages += draw_outages(y, rng(10 + y))

    # minute-resolution running fraction per hour from the outage list
    run_frac = np.ones(NH)
    for o in outages:
        a = (o["start"] - T0).total_seconds() / 3600.0
        b = (o["end"] - T0).total_seconds() / 3600.0
        for h in range(int(np.floor(a)), int(np.ceil(b))):
            lo, hi = max(a, h), min(b, h + 1)
            if hi > lo:
                run_frac[h] -= (hi - lo)
    run_frac = np.clip(run_frac, 0, 1)

    # methane captured each hour (kg), with the held gas recovered after each restart
    ch4_pct = 50.9 - 0.17 * t_years + np.zeros(NH)
    rr = rng(2)
    ch4_noise = np.zeros(NH)
    en = rr.normal(0, 0.09, NH)
    for i in range(1, NH):
        ch4_noise[i] = 0.93 * ch4_noise[i - 1] + en[i]
    ch4_pct = ch4_pct + ch4_noise
    capture = steady * run_frac
    excess = np.zeros(NH)
    held_total = 0.0
    recovered_total = {y: 0.0 for y in YEARS}
    escaped_total = {y: 0.0 for y in YEARS}
    held_by_year = {y: 0.0 for y in YEARS}
    for o in outages:
        a = (o["start"] - T0).total_seconds() / 3600.0
        h0 = int(np.floor(a))
        gen_out = G[h0] * o["hours"]
        held = KAPPA * G[h0] * min(o["hours"], D_STORE)
        rec = CE_REC * held
        o["held_kg"] = held
        o["recovered_kg"] = rec
        o["generated_kg"] = gen_out
        held_by_year[o["start"].year] += held
        recovered_total[o["start"].year] += rec
        escaped_total[o["start"].year] += gen_out - rec
        held_total += held
        # recovery starts in the hour the plant restarts, on the running part of that hour
        b = (o["end"] - T0).total_seconds() / 3600.0
        h = int(np.floor(b))
        rem = rec
        first = True
        while rem > 1e-6 and h < NH:
            cap_kg = BLOWER_NM3H * (ch4_pct[h] + 3.0) / 100.0 * RHO_N
            room = max(0.0, cap_kg - steady[h]) * (run_frac[h] if first else 1.0)
            take = min(room, max(rem / TAU, min(rem, 22.0)), rem)
            excess[h] += take
            rem -= take
            h += 1
            first = False
    capture = capture + excess
    # gas quality during the recovery: richer, less oxygen
    rich = np.zeros(NH)
    nz = excess > 0
    rich[nz] = 3.2 * np.clip(excess[nz] / np.maximum(steady[nz], 1.0), 0, 1)
    ch4_meas = np.where(run_frac > 0, ch4_pct + rich, np.nan)
    o2 = np.where(run_frac > 0, 0.72 + 0.18 * np.sin(np.arange(NH) / 211.0) - 0.35 * np.clip(rich / 3.2, 0, 1)
                  + rr.normal(0, 0.06, NH), np.nan)
    o2 = np.where(run_frac > 0, np.clip(o2, 0.15, 2.5), np.nan)
    co2 = np.where(run_frac > 0, 100.0 - ch4_meas - o2 * 4.78 - 9.1 + rr.normal(0, 0.15, NH), np.nan)
    flow = np.where(run_frac > 0, capture / (ch4_meas / 100.0 * RHO_N), 0.0)
    vac = np.where(run_frac > 0, -(21.5 + 2.5 * np.sin(np.arange(NH) / 97.0) + rr.normal(0, 0.4, NH)) * run_frac
                   - 4.0 * np.clip(excess / np.maximum(steady, 1.0), 0, 1), rr.normal(0.25, 0.08, NH))

    engines = build_engines(times, capture, run_frac, outages)
    plant = dict(times=times, yrs=yrs, G=G, steady=steady, capture=capture, excess=excess, run_frac=run_frac,
                 ch4=ch4_meas, o2=o2, co2=co2, flow=flow, vac=vac, outages=outages,
                 recovered=recovered_total, escaped=escaped_total, held=held_by_year)
    plant.update(engines)
    return plant


# ------------------------------------------------------------------------------------------------ engines and flare
def engine_stops(year, r, which):
    """Engine-only stops (the flare takes the gas): oil changes, services, trips. (start UTC, minutes, kind)."""
    jan1 = C.utc(year, 1, 1)
    stops = []
    # oil changes about every 950 running hours, about 6 h, on weekdays from 08:00 local
    t = jan1 + dt.timedelta(hours=float(r.uniform(150, 600)) + (300 if which == 2 else 0))
    while t.year == year:
        loc = C.local(t)
        day = loc.date()
        while dt.date.weekday(day) >= 5:
            day += dt.timedelta(days=1)
        st = dt.datetime(day.year, day.month, day.day, 8, int(r.choice([0, 15, 30])), tzinfo=C.TZ).astimezone(C.UTC)
        stops.append((st, int(r.uniform(300, 420)), "oil"))
        t = st + dt.timedelta(hours=float(r.uniform(900, 1010)))
    # a major service, about 38 h
    m = 5 + (3 if which == 2 else 0)
    day = dt.date(year, m, int(r.integers(4, 22)))
    while dt.date.weekday(day) >= 5:
        day += dt.timedelta(days=1)
    st = dt.datetime(day.year, day.month, day.day, 7, 0, tzinfo=C.TZ).astimezone(C.UTC)
    stops.append((st, int(r.uniform(2100, 2500)), "service"))
    # trips: jacket water temperature, misfire, gas quality
    for _ in range(int(r.integers(11, 24))):
        st = jan1 + dt.timedelta(minutes=int(r.uniform(0, 365 * 1440 - 3000)))
        stops.append((st, int(r.uniform(18, 170)), "trip"))
    stops.sort()
    return stops


def build_engines(times, capture, run_frac, outages):
    """Each engine's state minute by minute (on the grid or not), fuel per hour, and the flare's share."""
    nmin = NH * 60
    on = {1: np.ones(nmin, dtype=bool), 2: np.ones(nmin, dtype=bool)}
    stop_list = {1: [], 2: []}

    def minute_of(t):
        return int((t - T0).total_seconds() // 60)

    # plant outages stop both engines; the restart comes after the plant is back
    r = rng(30)
    rt = rng(31)
    restart_delay = {}
    for k, o in enumerate(outages):
        a, b = minute_of(o["start"]), minute_of(o["end"])
        for e in (1, 2):
            d = int(r.uniform(6, 26)) if e == 1 else int(r.uniform(14, 48))
            restart_delay[(k, e)] = d
            # a power failure stops everything at once; otherwise the engine runs on the header's residual pressure
            # for up to two minutes before it trips on low gas pressure
            lag = 0 if o["cause"] == "Utility power failure" else int(rt.integers(0, 3))
            on[e][a + lag:min(nmin, b + d)] = False
            stop_list[e].append(dict(start=a + lag, end=min(nmin, b + d), kind="plant", outage=k))
    for e in (1, 2):
        rt2 = rng(500 + e)
        for y in YEARS:
            for st, mins, kind in engine_stops(y, rng(40 + 10 * e + y), e):
                a = minute_of(st)
                b = min(nmin, a + mins)
                if a < 0 or a >= nmin:
                    continue
                # skip a stop that overlaps a plant outage window
                if not on[e][a:b].all():
                    continue
                on[e][a:b] = False
                stop = dict(start=a, end=b, kind=kind, outage=None)
                if kind in ("oil", "service"):
                    # the mechanic test-runs the engine off the grid before handing it back (8 to 20 minutes, ending
                    # 12 to 45 minutes before the operator's start)
                    dur = int(rt2.integers(8, 21))
                    gap = int(rt2.integers(12, 46))
                    stop["test"] = (b - gap - dur, b - gap)
                stop_list[e].append(stop)
        stop_list[e].sort(key=lambda s: s["start"])
    out = dict(eng_on_min=on, eng_stops=stop_list, restart_delay=restart_delay)
    split_fuel(out, capture)
    return out


def split_fuel(eng, capture):
    """Each hour's capture to the engines first (up to capacity times their on-share, plus about a third of full
    fuel while an engine test-runs off the grid), the rest to the flare."""
    on = eng["eng_on_min"]
    frac_on = {e: on[e].reshape(NH, 60).mean(axis=1) for e in (1, 2)}
    test = {}
    for e in (1, 2):
        tm = np.zeros(NH * 60, dtype=bool)
        for s in eng["eng_stops"][e]:
            if "test" in s:
                tm[s["test"][0]:s["test"][1]] = True
        test[e] = tm.reshape(NH, 60).mean(axis=1)
    c1 = ENG_CAP * (frac_on[1] + 0.34 * test[1])
    c2 = ENG_CAP * (frac_on[2] + 0.34 * test[2])
    take = np.minimum(capture, c1 + c2)
    tot = np.where(c1 + c2 > 0, c1 + c2, 1.0)
    eng_fuel = {1: np.where(capture > 0, take * c1 / tot, 0.0), 2: np.where(capture > 0, take * c2 / tot, 0.0)}
    flare = np.where(capture > 0, capture - take, 0.0)
    eng.update(eng_frac=frac_on, eng_fuel=eng_fuel, flare_kg=flare, eng_test_frac=test)


def extend_stop(p, e, k, extra_min):
    """Lengthen engine e's k-th stop by extra_min minutes (the restart comes later) and re-split the fuel."""
    s = p["eng_stops"][e][k]
    nmin = NH * 60
    b2 = min(nmin, s["end"] + extra_min)
    p["eng_on_min"][e][s["end"]:b2] = False
    s["end"] = b2
    split_fuel(p, p["capture"])
