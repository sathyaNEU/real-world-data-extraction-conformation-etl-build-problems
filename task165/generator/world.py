"""task165 architecture 2: the world's truth, simulated once from the seed.

Rain falls on Vellmore in storms that cluster into wet spells, wetter and longer from March to June. The Clay Street
catchment's combined flow above its regulator's 18 MGD spills through Outfall 014; the Southside plant takes the
regulators' flow plus its sewershed's fast inflow and the groundwater that seeps in for days after rain (a store that
fills with rain and drains with a 40-hour half life, its reach strongest in spring), and holds at its 140 MGD headworks
limit while that sum exceeds it. The Northside tank captures Outfall 006's overflow and is pumped back into a plant that
always has room within hours. Every function here works on the world's own arrays; the pack is written from them in
build.py and the golden is read back from the pack in golden.py."""
import datetime as dt
import functools

import numpy as np

import params as P

STEPS_PER_H = 60 // P.STEP_MIN
N = int((P.END_UTC - P.START_UTC).total_seconds() // (60 * P.STEP_MIN))
NH = N // STEPS_PER_H


def utc_of(i):
    return P.START_UTC + dt.timedelta(minutes=P.STEP_MIN * int(i))


def est_of(i):
    return utc_of(i).astimezone(P.EST).replace(tzinfo=None)


def index_of_est(d):
    """The 15-minute index of a naive EST wall time."""
    return int((d.replace(tzinfo=P.EST) - P.START_UTC).total_seconds() // (60 * P.STEP_MIN))


def doy_array():
    days = np.arange(N) / (24 * STEPS_PER_H)
    base = dt.date(2014, 1, 1)
    out = np.empty(N)
    for i in range(0, N, STEPS_PER_H * 24):
        d = base + dt.timedelta(days=int(days[i]))
        out[i:i + STEPS_PER_H * 24] = d.timetuple().tm_yday
    return out


def season_rate(doy):
    """Storm frequency, wettest in late April."""
    return 0.76 + 0.24 * np.cos(2 * np.pi * (doy - 112) / 365.25)


def gw_reach(doy):
    """How far the groundwater store reaches into the Southside sewers: full from March to May, least in September."""
    return 0.62 + 0.38 * np.cos(2 * np.pi * (doy - 100) / 365.25)


def storms(rng, doy):
    out = []
    t = 0
    wet = False
    while True:
        d = doy[min(t, N - 1)]
        sr = season_rate(d)
        if wet:
            gap_h = rng.exponential(30.0)
            if rng.random() < 0.34:
                wet = False
        else:
            gap_h = rng.exponential(92.0 / sr)
            if rng.random() < 0.30 * sr:
                wet = True
        t += int(gap_h * STEPS_PER_H) + 1
        if t >= N:
            break
        summer = 1.0 if 150 <= d <= 260 else 0.0
        dur_h = max(0.5, rng.gamma(1.6, 3.4 if not summer else 1.6))
        depth = rng.gamma(0.75, P.STORM_SCALE) * (1.25 if wet else 1.0)
        out.append((t, dur_h, depth, rng.random() < 0.5 * summer))
        t += int(dur_h * STEPS_PER_H)
    return out


@functools.lru_cache(maxsize=1)
def simulate():
    rng = np.random.default_rng([P.SEED, 1])
    doy = doy_array()
    st = storms(rng, doy)
    rain = np.zeros((4, N))
    for (t0, dur_h, depth, convective) in st:
        k = max(1, int(round(dur_h * STEPS_PER_H)))
        shape = rng.dirichlet(np.ones(k) * (0.8 if convective else 2.5))
        for g in range(4):
            f = float(np.exp(rng.normal(0, 0.28 if convective else 0.12)))
            lag = int(rng.integers(-1, 2))
            a = max(0, t0 + lag)
            b = min(N, a + k)
            rain[g, a:b] += (shape * depth * f)[:b - a]
    # Rain arrives as 0.01-inch tips at the gauges; the true depth stays continuous here.
    hours = np.arange(N) / STEPS_PER_H
    diurnal = np.sin(2 * np.pi * ((hours % 24) - 8) / 24)
    uh = np.array([0.10, 0.22, 0.24, 0.18, 0.11, 0.07, 0.04, 0.025, 0.015])
    uh = uh / uh.sum()
    area14 = (rain[1] + rain[2] + rain[3]) / 3.0
    q14 = P.O14_DWF * (1 + 0.25 * diurnal) + np.convolve(area14, uh)[:N] * P.O14_RUNOFF * 96.0
    o14 = np.maximum(0.0, q14 - P.O14_REG)
    q06 = P.O06_DWF * (1 + 0.25 * diurnal) + np.convolve(rain[0], uh)[:N] * P.O06_RUNOFF * 96.0
    o06 = np.maximum(0.0, q06 - P.O06_REG)
    # The plants, hourly.
    areal = rain.mean(axis=0)
    rain_h = areal.reshape(NH, STEPS_PER_H).sum(axis=1)
    doy_h = doy[::STEPS_PER_H]
    hh = np.arange(NH)
    decay = 0.5 ** (1.0 / P.SS_HALF_LIFE_H)
    store = np.zeros(NH)
    s = 0.0
    for i in range(NH):
        s = s * decay + rain_h[i]
        store[i] = s
    fast = np.convolve(rain_h, np.array([0.45, 0.35, 0.15, 0.05]))[:NH]
    di_h = np.sin(2 * np.pi * ((hh % 24) - 9) / 24)
    seas = np.cos(2 * np.pi * (doy_h - 80) / 365.25)
    noise_s = rng.normal(0, 0.9, NH)
    noise_n = rng.normal(0, 0.5, NH)
    ss_raw = (P.SS_BASE + 5.5 * di_h + 3.0 * seas + P.SS_FAST * fast + P.SS_RDII * store * gw_reach(doy_h)
              + noise_s)
    ss = np.minimum(P.SS_CAP, ss_raw)
    ns_raw = P.NS_BASE + 3.0 * di_h + 1.5 * seas + P.NS_FAST * fast + P.NS_RDII * store * gw_reach(doy_h) + noise_n
    ns = np.minimum(P.NS_CAP, ns_raw)
    return dict(rain=rain, doy=doy, o14=o14, o06=o06, ss=ss, ss_raw=ss_raw, ns=ns, storms=st)


# ----------------------------------------------------------------------------------------------- replay and count
def replay(inflow, vol, pump, room=None, pump_during_inflow=False):
    """Route a 15-minute inflow (MGD) through a tank of `vol` MG pumped out at `pump` MGD, or at the lesser of the
    pumps and `room` (MGD, per 15-minute step) when given. Pumping starts once the flow to the tank has stopped.
    Returns the discharge past the full tank (MGD per step)."""
    dtd = P.STEP_MIN / 1440.0
    out = np.zeros(len(inflow))
    s = 0.0
    lim = np.full(len(inflow), pump) if room is None else np.minimum(pump, np.maximum(0.0, room))
    for i in range(len(inflow)):
        q = inflow[i] * dtd
        if q > 0:
            take = min(vol - s, q)
            s += take
            out[i] = (q - take) / dtd
            if pump_during_inflow and s > 0:
                s -= min(s, lim[i] * dtd)
        elif s > 0:
            s -= min(s, lim[i] * dtd)
    return out


def events(series, step_min=P.STEP_MIN, gap_h=P.EVENT_GAP_H):
    """Start indices of untreated overflow events: discharges separated by less than gap_h of no discharge are one."""
    on = np.flatnonzero(series > 1e-9)
    if len(on) == 0:
        return []
    starts = [on[0]]
    gaps = np.diff(on)
    gap_steps = gap_h * 60 / step_min
    for j in np.flatnonzero(gaps > gap_steps):
        starts.append(on[j + 1])
    return starts


def per_year(series):
    return len(events(series)) / P.YEARS


def ss_room_15(ss_hourly):
    return np.repeat(P.SS_CAP - ss_hourly, STEPS_PER_H)


# ----------------------------------------------------------------------------------------------- clocks
import zoneinfo  # noqa: E402

NY = zoneinfo.ZoneInfo("America/New_York")


def local_of(i):
    """Naive local (Eastern, with daylight saving) wall time of 15-minute index i."""
    return utc_of(i).astimezone(NY).replace(tzinfo=None)


def index_of_local(d):
    """The 15-minute index of a naive local wall time (the earlier instant on a repeated hour)."""
    u = d.replace(tzinfo=NY, fold=0).astimezone(P.UTC)
    return int((u - P.START_UTC).total_seconds() // (60 * P.STEP_MIN))


# ----------------------------------------------------------------------------------------------- Northside tank
def nt_wall_mg_per_ft():
    return (P.NT_VOL - P.NT_HOPPER_MG) / (P.NT_CREST_FT - P.NT_HOPPER_FT)


def nt_depth_of_volume(v):
    """The tank's water depth (ft) for a stored volume (MG): a sloped hopper floor to 3.0 ft, then straight walls."""
    if v <= P.NT_HOPPER_MG:
        return P.NT_HOPPER_FT * (max(v, 0.0) / P.NT_HOPPER_MG) ** 0.5
    return P.NT_HOPPER_FT + (v - P.NT_HOPPER_MG) / nt_wall_mg_per_ft()


def nt_volume_of_depth(h):
    if h <= P.NT_HOPPER_FT:
        return P.NT_HOPPER_MG * (max(h, 0.0) / P.NT_HOPPER_FT) ** 2
    return P.NT_HOPPER_MG + (min(h, P.NT_CREST_FT) - P.NT_HOPPER_FT) * nt_wall_mg_per_ft()


def station_rate(pumps, rebuilt):
    if rebuilt and "P2" in pumps:
        return P.NT_CURVE_P2[tuple(sorted(pumps))]
    return P.NT_CURVE[len(pumps)]


@functools.lru_cache(maxsize=1)
def northside_tank():
    """The Northside tank from 1 May 2020 (local): 15-minute volume, pumps, delivered volume and overflow."""
    w = simulate()
    i0 = index_of_local(P.NT_START_LOCAL)
    ir = index_of_local(P.NT_P2_REBUILT_LOCAL)
    iout = index_of_local(P.NT_P2_OUT_LOCAL)
    room = np.repeat(P.NS_CAP - w["ns"], STEPS_PER_H)
    inflow = w["o06"].copy()
    # the diversion's sluice gate SG-600 passing dry weather flow into the tank while its seals were failing
    for a, b, q in P.NT_LEAKS:
        inflow[index_of_local(a):index_of_local(b)] += q
    dtd = P.STEP_MIN / 1440.0
    n = N - i0
    vol = np.zeros(n)
    run = np.zeros((n, 3), dtype=np.int8)
    deliv = np.zeros(n)
    over = np.zeros(n)
    order = ("P1", "P2", "P3")
    s = 0.0
    running = False
    ca, cb = (index_of_local(x) for x in P.NT_CLEANOUT_LOCAL)
    for k in range(n):
        i = i0 + k
        q = inflow[i] * dtd
        if ca <= i < cb:
            assert s < 0.5, "the tank is near empty when it is taken out for the cleanout"
            s = 0.0
            running = False
            over[k] = inflow[i]
            continue
        if inflow[i] >= P.NT_HOLD_MGD:
            running = False
        elif not running and nt_depth_of_volume(min(P.NT_VOL, s + q)) >= P.NT_START_FT:
            running = True
        if not running:
            take = min(P.NT_VOL - s, q)
            s += take
            over[k] = (q - take) / dtd
        if running and s + q > 1e-9:
            # the pumps draw down while the trickle comes in; what they return is the fall plus the inflow
            s += q
            depth = nt_depth_of_volume(s)
            m = 3 if depth > 12.0 else (2 if depth > 5.0 else 1)
            week = (k // (96 * 7)) % 3
            lead = order[week:] + order[:week]
            if iout <= i < ir:
                lead = tuple(p for p in lead if p != "P2")
            pumps = lead[:m]
            rate = min(station_rate(pumps, i >= ir), room[i])
            d = min(s, rate * dtd)
            s -= d
            if s > P.NT_VOL:
                over[k] = (s - P.NT_VOL) / dtd
                s = P.NT_VOL
            deliv[k] = d
            for p in pumps:
                run[k, order.index(p)] = 1
            if s < 1e-9:
                s = 0.0
                running = False
        vol[k] = s
    return dict(i0=i0, vol=vol, run=run, deliv=deliv, over=over, inflow=inflow[i0:])


# ----------------------------------------------------------------------------------------------- rain gauges
ORIFICE_CM2 = np.pi * (P.ORIFICE_IN * 2.54 / 2) ** 2
POUR_NOTES = ["Routine visit. Funnel cleaned, screen clear. Cal check {ml} mL.",
              "Leveled gauge, cleared debris from screen. Cal check {ml} mL poured.",
              "Routine. Battery {v} V. Cal check {ml} mL.",
              "Cal check {ml} mL, tipping OK. Cleaned bucket.",
              "Site check, mowed around stand. Cal check {ml} mL."]
PLAIN_NOTES = ["Routine visit. Screen clear, no service needed.", "Site check only, rain on arrival, no cal check.",
               "Downloaded backup, battery {v} V. No cal check (time).", "Checked level and screen. No cal check."]


POUR_NOTES_ALL = POUR_NOTES + [
    "Cal check {ml} mL. Spider web in funnel cleared first.",
    "Pulled leaves off screen, checked bubble level OK. Cal check {ml} mL",
    "Cal check w/ {ml} mL bottle, steady tipping. Batt {v}V",
    "Routine, grass cut by parks crew already. Cal chk {ml} mL.",
    "Wasp nest under logger box removed. Cal check {ml} mL.",
    "Funnel had bird droppings, rinsed. Cal check {ml} mL poured slow.",
    "Checked mounting bolts, tight. Cal check {ml} mL. Battery {v} V.",
    "Cal check {ml} mL; bucket pivots look clean, no wear.",
    "Leveled (was slightly off after frost). Cal check {ml} mL.",
    "Routine visit, gate code changed (new code in van binder). Cal check {ml} mL."]
PLAIN_NOTES_ALL = [PLAIN_NOTES[0], PLAIN_NOTES[2], PLAIN_NOTES[3],
                   "Quick look only, called back to Clay St PS. Screen clear.",
                   "Downloaded logger, battery {v} V. Out of cal bottles, no cal check.",
                   "Site locked, waited for parks staff. Screen and funnel OK, no cal check.",
                   "Checked level, leaves on screen cleared. Ran out of time for cal check."]
RAIN_NOTES = [PLAIN_NOTES[1], "Raining on arrival, visual check only.", "Light rain, no cal check. Screen clear.",
              "Storm moving in, checked screen and left. No cal check."]


def _visit_dates(rng, g):
    """Visits every five to eight weeks to May 2025; from June 2025 the maintenance contract's monthly visit."""
    d = dt.date(2014, 1, 6) + dt.timedelta(days=int(rng.integers(0, 30)))
    out = []
    while d <= dt.date(2025, 6, 13):
        while d.weekday() >= 5:
            d += dt.timedelta(days=1)
        out.append(d)
        d += dt.timedelta(days=int(rng.integers(35, 56)))
    for m in range(7, 13):
        d = dt.date(2025, m, int(rng.integers(3, 20)))
        while d.weekday() >= 5:
            d += dt.timedelta(days=1)
        out.append(d)
    return out


def _gauge_raining(rain_g, i, before=6, after=6):
    a, b = max(0, i - before), min(N, i + after)
    return rain_g[a:b].sum() > 0


@functools.lru_cache(maxsize=1)
def rain_gauges():
    """Every tip each gauge's logger recorded (UTC instants), which were rain and which calibration pours, the bucket
    each tip measured, and the field service visits."""
    w = simulate()
    rng = np.random.default_rng([P.SEED, 2])
    note_rng = np.random.default_rng([P.SEED, 3])     # the wording only; the visits' own draws stay on rng
    tips = {}
    visits = []
    for gi, (g, site, logger_new) in enumerate(P.GAUGES):
        r = w["rain"][gi]
        swap = P.MECH_SWAPS[g]
        iswap = index_of_local(swap)
        sec = []
        bucket = []
        cum = 0.0
        for i in np.flatnonzero(r > 0):
            b = P.TIP_02MM_IN if i >= iswap else P.TIP_IN
            cum += r[i]
            k = int(cum // b)
            if k:
                cum -= k * b
                pos = np.sort(rng.random(k)) * 900.0
                base = (i * 900)
                for p in pos:
                    sec.append(base + int(p))
                    bucket.append(b)
        kind = ["rain"] * len(sec)
        # field visits and calibration pours
        for d in _visit_dates(rng, g):
            arrive = dt.datetime(d.year, d.month, d.day, 8, 30) + dt.timedelta(minutes=int(rng.integers(0, 360)))
            special = None
            if logger_new is not None and d == logger_new.date():
                arrive, special = logger_new, "logger"
            if (d.year, d.month) == (swap.year, swap.month):
                arrive, special = swap, "mech"
                d = swap.date()
            contract = d >= P.CONTRACT_START
            if contract and special != "mech":
                # the contract's monthly visit carries a cal check: the crew waits for a dry spell on the day
                for _ in range(40):
                    if not _gauge_raining(r, index_of_local(arrive), 8, 12):
                        break
                    arrive += dt.timedelta(hours=1)
                    if arrive.hour > 15:
                        arrive = (arrive + dt.timedelta(days=1)).replace(hour=8, minute=30)
                        while arrive.weekday() >= 5:
                            arrive += dt.timedelta(days=1)
                d = arrive.date()
            dur = int(rng.integers(20, 46))
            ia = index_of_local(arrive)
            raining = _gauge_raining(r, ia, 8, 12) if contract else _gauge_raining(r, ia)
            pour = (not raining) and (contract or rng.random() < 0.78) and special != "logger"
            ml = int(rng.choice([500, 500, 500, 1000, 250]))
            v = "%.1f" % rng.uniform(12.2, 13.4)
            if special == "logger":
                note = "Replaced datalogger with TipLink C200 cellular unit; old logger returned to shop. No cal check."
            elif special == "mech":
                note = ("Contract work: new TB mechanism installed (0.2mm unit, contract stock), old mech bagged for "
                        "return. Leveled. Cal check {ml} mL.").format(ml=ml) if pour else \
                    "Contract work: new TB mechanism installed (0.2mm unit, contract stock), old mech bagged for return."
            elif pour:
                rng.integers(0, len(POUR_NOTES))
                note = POUR_NOTES_ALL[int(note_rng.integers(0, len(POUR_NOTES_ALL)))].format(ml=ml, v=v)
            else:
                rng.integers(1 if raining else 0, len(PLAIN_NOTES))
                note = PLAIN_NOTES_ALL[int(note_rng.integers(0, len(PLAIN_NOTES_ALL)))].format(v=v)
                if raining:
                    note = RAIN_NOTES[int(note_rng.integers(0, len(RAIN_NOTES)))]
            # the technician logs arrival and departure to the five minutes, departure as the van leaves the gate
            arrive = arrive.replace(minute=arrive.minute - arrive.minute % 5)
            depart = arrive + dt.timedelta(minutes=dur - dur % 5)
            if pour:
                start = arrive + dt.timedelta(minutes=int(rng.integers(12, 33)))
                u0 = int((start.replace(tzinfo=NY).astimezone(P.UTC) - P.START_UTC).total_seconds())
                b = P.TIP_02MM_IN if u0 >= iswap * 900 else P.TIP_IN
                n_tips = int(round(ml / ORIFICE_CM2 / 2.54 / b))
                t = u0
                for _ in range(n_tips):
                    t += int(round(rng.normal(9.0, 0.7)))
                    sec.append(t)
                    bucket.append(b)
                    kind.append("pour")
            visits.append(dict(gauge=g, date=d, arrive=arrive, depart=depart, note=note, pour=pour, ml=ml if pour else 0))
        order = np.argsort(np.array(sec, dtype=np.int64), kind="stable")
        s = np.array(sec, dtype=np.int64)[order]
        bk = np.array(bucket)[order]
        kd = np.array(kind)[order]
        # one tip a second at most: a tip in the same second as the one before moves on a second
        for j in range(1, len(s)):
            if s[j] <= s[j - 1]:
                s[j] = s[j - 1] + 1
        tips[g] = dict(sec=s, bucket=bk, kind=kd)
    visits.sort(key=lambda v: (v["arrive"], v["gauge"]))
    return dict(tips=tips, visits=visits)


def logged_time(g, sec):
    """A tip's time as its logger stamped it: Eastern Standard Time on the original loggers, UTC on the cellular ones."""
    u = P.START_UTC + dt.timedelta(seconds=int(sec))
    new = dict((x[0], x[2]) for x in P.GAUGES)[g]
    if new is not None and u >= new.replace(tzinfo=NY).astimezone(P.UTC):
        return u.replace(tzinfo=None)
    return u.astimezone(P.EST).replace(tzinfo=None)


# ----------------------------------------------------------------------------------------------- the meter swap
def meter_swap():
    """The new Outfall 014 logger's first reading and the old one's last, a dry week apart."""
    a = index_of_local(P.METER_NEW_START_LOCAL)
    b = index_of_est(P.METER_OLD_END_LOCAL)
    return a, b
