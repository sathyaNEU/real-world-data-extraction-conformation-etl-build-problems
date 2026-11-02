"""Winter 2026 at Yarrabin zone substation: what each 22 kV feeder head carried every half hour from 1 June to 31
August 2026, the SCADA historian's archive of it, and the zone substation's 22 kV transformer check meters.

Each feeder head's flow is its customers' load less its rooftop PV's output: the PV is the world's own connected
capacity on the day (each NMI's latest connected configuration, on its feeder at the base date) under the day's sun
and cloud; the load follows a winter profile scaled to the feeder (its evening peak a feeder-specific share of its
summer forecast, its midday load near twice the hosting capacity assessment's spring minimum, so winter middays sit
above the spring minimum the assessment modelled). The historian archives each feeder head at its bay's old metering
CT ratio over the ratio installed at the May 2026 protection renewal (common.BAY_CT); the check meters measure each
bus section's flow through its transformer, which supplies only its four feeders (the station services take their
supply from the local network, so nothing else rides on the meter). Each system measures with its own error: every
feeder head with its own small gain and a random error in each half-hour average, each check meter with its own gain
and random error, so the two never agree exactly. Every draw comes from this module's own streams, so nothing in the
main pack moves.

Generator-only: the asks' figures are computed from the written files by calc.py and on its own code path by verify.py;
this module's arrays are the clean truth checks.py holds them to."""
from __future__ import annotations

import collections
import datetime as dt
import math

import numpy as np

import common as K

D0, D1 = K.WINTER
DAYS = [D0 + dt.timedelta(days=i) for i in range((D1 - D0).days + 1)]
T = len(DAYS) * 48
HH = np.arange(48) / 2.0 + 0.25                        # each half hour's midpoint, hours after midnight (AEST)
MONTHS = (6, 7, 8)
TAG = {f: "YRB.22KV.B%s.FDR%s.MW" % ("1" if f in K.BUS["T1"] else "2", f[-2:]) for f in K.FEEDERS}
METER = {"T1": "YRB-T1-22KV-CHK", "T2": "YRB-T2-22KV-CHK"}


def capacity_by_day(W):
    """MW of connected micro EG on each feeder at the end of each winter day: each NMI's latest connected configuration
    (an alteration replaces what it alters), less systems removed by the day, on the NMI's feeder at the base date."""
    events = collections.defaultdict(list)
    for a in W.apps:
        if a["status"] in ("Connected", "Removed") and a.get("connected") and a["nmi"] in W.nmi_by:
            events[a["nmi"]].append(a)
    caps = np.zeros((len(DAYS), len(K.FEEDERS)))

    def kw_on(apps, d):
        live = [a for a in apps if a["connected"] <= d and not (a.get("removed") and a["removed"] <= d)]
        return (max(live, key=lambda a: (a["connected"], a["type"]))["kw"] or 0.0) if live else 0.0

    for nmi, apps in events.items():
        fi = K.FEEDERS.index(W.nmi_by[nmi]["feeder"])
        marks = sorted({a["connected"] for a in apps} | {a["removed"] for a in apps if a.get("removed")})
        marks = [m for m in marks if D0 < m <= D1]
        prev = kw_on(apps, D0)
        caps[:, fi] += prev
        for m in marks:
            now = kw_on(apps, m)
            if now != prev:
                caps[(m - D0).days:, fi] += now - prev
                prev = now
    return caps / 1000.0


def load_shape(weekend):
    """A winter weekday (or weekend) profile, as a share of the evening peak, at each half hour's midpoint."""
    pts = [(0, .52), (2, .45), (4, .44), (5, .48), (6, .62), (7, .66 if weekend else .84), (8, .74 if weekend else .80),
           (9, .70 if weekend else .64), (10, .55), (12, .50), (14, .50), (15, .55), (16, .68), (17, .88), (18, 1.0),
           (19, .98), (20, .88), (21, .76), (22, .66), (23, .58), (24, .52)]
    xs, ys = zip(*pts)
    return np.interp(HH, xs, ys)


def sun(d):
    """Sunrise and sunset (AEST, decimal hours) at Merindah (about 27.6 degrees south) and the clear-day output per kW
    of inverter at solar noon, which rises from the winter solstice as the sun climbs."""
    c = (1 - math.cos(2 * math.pi * (d.timetuple().tm_yday - 172) / 365.0)) / 2.0
    return 6.62 - 0.30 * c, 17.05 + 0.40 * c, min(0.70 + 0.20 * c, 0.80)


def flows(caps, hca, peaks):
    """The true flow at every feeder head (MW, positive from the bus into the feeder), one row per half hour (AEST,
    the half hour starting at the row's time), columns in K.FEEDERS order, before the settle; and the PV's output."""
    rw = K.rng("scada", "weather")
    clear = np.where(rw.random(len(DAYS)) < 0.66, rw.uniform(0.88, 1.0, len(DAYS)), rw.uniform(0.15, 0.85, len(DAYS)))
    temp = rw.normal(0.0, 1.0, len(DAYS))
    cloud_hh = [rw.normal(0.0, 0.10 if c < 0.85 else 0.02, 48) for c in clear]
    out = np.zeros((T, len(K.FEEDERS)))
    pv_out = np.zeros((T, len(K.FEEDERS)))
    for fi, f in enumerate(K.FEEDERS):
        rf = K.rng("scada", "feeder", f)
        evening = peaks[f][1] * float(rf.uniform(0.70, 0.90))         # winter evening peak against the summer forecast
        midday = 2.0 * hca[f]["min26"] * float(rf.uniform(0.85, 1.15))   # winter middays above the spring minimum
        mid = min(max(midday / evening, 0.30), 0.75)
        w = np.exp(-((HH - 12.5) / 2.6) ** 2)
        day_noise = rf.normal(0.0, 0.03, len(DAYS))
        hh_noise = rf.normal(0.0, 0.025, (len(DAYS), 48))
        pv_noise = rf.normal(0.0, 0.03, (len(DAYS), 48))
        for di, d in enumerate(DAYS):
            wk = d.weekday() >= 5
            shp = load_shape(wk)
            shp = shp * (1 - w) + w * mid * (1.05 if wk else 1.0)
            load = evening * shp * (1 + 0.035 * temp[di]) * (1 + day_noise[di]) * (1 + hh_noise[di])
            rise, sset, peak = sun(d)
            x = np.clip((HH - rise) / (sset - rise), 0, 1)
            s = peak * np.sin(np.pi * x) ** 1.25
            pv = caps[di, fi] * s * np.clip(clear[di] * (1 + cloud_hh[di]) * (1 + pv_noise[di]), 0, 1.02)
            out[di * 48:(di + 1) * 48, fi] = load - pv
            pv_out[di * 48:(di + 1) * 48, fi] = pv
    return out, pv_out


def errors():
    """Each system's measurement error, drawn once on its own streams: every feeder head's gain (within 0.04 per cent)
    and random error in each half-hour average (0.08 per cent), each check meter's gain (within 0.02 per cent) and
    random error (0.03 per cent)."""
    rh = K.rng("scada", "historian error")
    rm = K.rng("scada", "meter error")
    return dict(h_gain=rh.uniform(-0.0004, 0.0004, len(K.FEEDERS)), h_eps=rh.normal(0.0, 0.0008, (T, len(K.FEEDERS))),
                m_gain={t: float(rm.uniform(-0.0002, 0.0002)) for t in K.BUS},
                m_eps={t: rm.normal(0.0, 0.0003, T) for t in K.BUS})


def archive(true, err):
    """The historian's value for each feeder head (MW, three decimals): the flow as its bay measures it, at the bay's
    old CT ratio over its new one, so each feeder head reads its measured flow divided by its bay's factor."""
    k = np.array([K.BAY_FACTOR[f] for f in K.FEEDERS])
    return np.round(true * (1 + err["h_eps"]) * (1 + err["h_gain"]) / k, 3)


def two_way(mu):
    """The export register's part of each half hour (MW averaged over the half hour) for a flow that runs through the
    half hour as two straight segments: from the mean of the half hour before and this one, through the level that
    gives this half hour its own mean, to the mean of this half hour and the next. Returns that part and whether the
    flow reverses within the half hour; import less export is the half hour's mean."""
    edge = np.empty(len(mu) + 1)
    edge[1:-1] = (mu[:-1] + mu[1:]) / 2.0
    edge[0], edge[-1] = mu[0], mu[-1]
    a, c = edge[:-1], edge[1:]
    m = 2.0 * mu - (a + c) / 2.0

    def below(p, q):
        """The mean of the flow below zero along one straight segment from p to q."""
        both = (p <= 0) & (q <= 0)
        cross = (p < 0) != (q < 0)
        span = np.where(cross, np.abs(p - q), 1.0)
        lo = np.minimum(p, q)
        return np.where(both, -(p + q) / 2.0, np.where(cross, lo * lo / (2.0 * span), 0.0))

    back = 0.5 * below(a, m) + 0.5 * below(m, c)
    rev = (np.minimum(np.minimum(a, m), c) < 0) & (np.maximum(np.maximum(a, m), c) > 0)
    return back, rev


def metered(true, err):
    """Each bus section's flow through its transformer's 22 kV check meter, as the meter's half-hour energy (kWh to one
    decimal, import into the bus and export back through the transformer). Each register accumulates its own
    direction, so a half hour the section's flow reverses within carries both (two_way); import less export is the
    half hour's energy at the meter's resolution, whatever the registers hold."""
    out = {}
    for t, fs in K.BUS.items():
        idx = [K.FEEDERS.index(f) for f in fs]
        raw = true[:, idx].sum(1) * (1 + err["m_gain"][t]) * (1 + err["m_eps"][t]) * 500.0
        kwh = np.round(raw, 1)
        back, rev = two_way(raw / 500.0)
        exp = np.where(rev, np.round(back * 500.0, 1), np.where(kwh < 0, -kwh, 0.0))
        imp = np.maximum(np.round(kwh + exp, 1), 0.0)
        out[t] = (imp + 0.0, np.round(imp - kwh, 1) + 0.0)
    return out


def fit(hist, meters):
    """Each feeder head's factor by least squares of its bus section's metered flow on the section's feeder heads, with
    an intercept (the route calc.bay_factors takes on the written files)."""
    net = {t: (imp - exp) / 500.0 for t, (imp, exp) in meters.items()}
    k = np.zeros(len(K.FEEDERS))
    for t, fs in K.BUS.items():
        idx = [K.FEEDERS.index(f) for f in fs]
        A = np.column_stack([hist[:, idx], np.ones(len(hist))])
        sol = np.linalg.lstsq(A, net[t], rcond=None)[0]
        k[idx] = sol[:-1]
    return k


def reconstruct(true, err):
    """What the files give back: the historian at the fitted factors, with the archive and the meters behind it."""
    hist, meters = archive(true, err), metered(true, err)
    return hist * fit(hist, meters), hist, meters


def month_of():
    """Each half hour's calendar month (Queensland time, the half hour's start)."""
    return np.array([d.month for d in DAYS for _ in range(48)])



def figures(flow, months=None):
    """Per feeder: the energy its head sent back to the zone substation in June, July and August (MWh) and its largest
    half-hour reverse flow (MW)."""
    months = month_of() if months is None else months
    out = {}
    for fi, f in enumerate(K.FEEDERS):
        rev = np.maximum(-flow[:, fi], 0.0)
        out[f] = tuple(float(rev[months == m].sum() * 0.5) for m in MONTHS) + (float(rev.max()),)
    return out


def room(v, unit):
    q = v / unit
    return abs(q - math.floor(q) - 0.5) * unit


def graded(fx):
    """The figures as the prompt rounds them: MWh to the nearest 10, MW to one decimal."""
    return {f: tuple(int(round(v / 10.0)) for v in fx[f][:3]) + (int(round(fx[f][3] * 10)),) for f in K.FEEDERS}


def careful_routes(hist, net):
    """The careful solver's routes on the archive: the historian as recorded, one factor fitted to both meters, and
    one factor per bus section fitted to its meter or taken as the ratio of its totals (the pro-rata repairs of a
    control that does not tie)."""
    tot = net["T1"] + net["T2"]
    out = {"as recorded": hist, "one factor": hist * (np.sum(tot * hist.sum(1)) / np.sum(hist.sum(1) ** 2))}
    sec, rat = hist.copy(), hist.copy()
    for t, fs in K.BUS.items():
        idx = [K.FEEDERS.index(f) for f in fs]
        x = hist[:, idx].sum(1)
        sec[:, idx] = hist[:, idx] * (np.sum(net[t] * x) / np.sum(x * x))
        rat[:, idx] = hist[:, idx] * (np.sum(net[t]) / np.sum(x))
    out["one factor per bus section"] = sec
    out["the ratio of each bus section's totals"] = rat
    return out


def settle(true, err):
    """Keep every graded figure clear of its rounding edge (a month's energy at least 1.5 MWh, a feeder's largest half
    hour at least 0.015 MW) by small load moves that change no other figure: a month's energy is moved to a third or
    two thirds of its bin by adding or shedding load in that feeder's own midday reverse-flow half hours that month
    (never on its largest half hour's day), at most 0.12 MW in any half hour; a feeder's largest half hour is pushed a
    little deeper (more reverse flow there), so it stays the largest. Deterministic: the half hours are taken in time
    order."""
    true = true.copy()
    months = month_of()
    log = []
    for _ in range(12):
        moved = False
        seen = reconstruct(true, err)[0]
        fx = figures(seen)
        for fi, f in enumerate(K.FEEDERS):
            rev = np.maximum(-seen[:, fi], 0.0)
            peak_i = int(np.argmax(rev))
            peak_day = peak_i // 48
            # the largest half hour
            m_ = fx[f][3]
            if room(m_, 0.1) < 0.015:
                frac = m_ / 0.1 - math.floor(m_ / 0.1)
                shift = (0.7 - frac) * 0.1 if frac <= 0.7 else (1.3 - frac) * 0.1
                true[peak_i, fi] -= shift
                log.append(("peak", f, round(shift, 4)))
                moved = True
            for mi, m in enumerate(MONTHS):
                e = fx[f][mi]
                if room(e, 10) >= 1.5:
                    continue
                frac = e / 10.0 - math.floor(e / 10.0)
                up, down = (0.7 - frac) * 10.0, (frac - 0.3) * 10.0    # more reverse energy, or less
                shift = up if abs(up) <= abs(down) else -down
                cand = [i for i in np.nonzero((months == m) & (seen[:, fi] < -0.5))[0]
                        if i // 48 != peak_day and 22 <= i % 48 <= 27]
                n = max(1, int(math.ceil(abs(shift) * 2.0 / 0.12)))
                use = cand[:n]
                d = shift * 2.0 / len(use)
                for i in use:
                    true[i, fi] -= d                                    # -d to the flow is +d reverse flow
                log.append(("month", f, m, round(shift, 3), len(use)))
                moved = True
        if not moved:
            return true, log
    raise AssertionError("the winter figures did not settle")


def winter(W, hca, peaks):
    """The winter's flows, settled on what the files give back, the historian's archive of them and the check meters'
    record, with the clean truth's own figures beside them."""
    caps = capacity_by_day(W)
    err = errors()
    raw, pv = flows(caps, hca, peaks)
    true, log = settle(raw, err)
    seen, hist, meters = reconstruct(true, err)
    gold = figures(seen)
    g = graded(gold)
    k = np.array([K.BAY_FACTOR[f] for f in K.FEEDERS])
    if graded(figures(hist * k)) != g:
        raise AssertionError("the factors as CT quotients file other figures")
    for f in K.FEEDERS:
        if min(gold[f][:3]) < 120 or min(room(v, 10) for v in gold[f][:3]) < 1.0 or room(gold[f][3], 0.1) < 0.012:
            raise AssertionError("winter figure %s %s too small or near a rounding edge" % (f, gold[f]))
    net = {t: (imp - exp) / 500.0 for t, (imp, exp) in meters.items()}
    for name, x in careful_routes(hist, net).items():
        gx = graded(figures(x))
        hits = [(f, i) for f in K.FEEDERS for i in range(4) if gx[f][i] == g[f][i]]
        if hits:
            raise AssertionError("the careful route %r lands %s" % (name, hits))
    return dict(true=true, pv=pv, hist=hist, meters=meters, caps=caps, err=err, settle_log=log)


def start_label(di, j):
    t = dt.datetime(DAYS[di].year, DAYS[di].month, DAYS[di].day) + dt.timedelta(minutes=30 * j)
    return t.strftime("%Y-%m-%d %H:%M")


def end_label(di, j):
    t = dt.datetime(DAYS[di].year, DAYS[di].month, DAYS[di].day) + dt.timedelta(minutes=30 * (j + 1))
    return t.strftime("%Y-%m-%d %H:%M")


SCADA_COLS = ["interval_start_aest", "tag", "value"]
METER_COLS = ["meter_id", "interval_end_aest", "import_kwh", "export_kwh"]


def scada_rows(wt):
    """The historian's export: one row per tag per half hour, the half hour's start in Queensland time, sorted by
    time then tag."""
    hist = wt["hist"]
    order = sorted(K.FEEDERS, key=lambda f: TAG[f])
    for di in range(len(DAYS)):
        for j in range(48):
            ts = start_label(di, j)
            for f in order:
                yield [ts, TAG[f], "%.3f" % hist[di * 48 + j, K.FEEDERS.index(f)]]


def meter_rows(wt):
    """The metering database's interval export for the two check meters: kWh in the half hour ending at the row's
    local time, one meter after the other."""
    for t in ("T1", "T2"):
        imp, exp = wt["meters"][t]
        for di in range(len(DAYS)):
            for j in range(48):
                i = di * 48 + j
                yield [METER[t], end_label(di, j), "%.1f" % imp[i], "%.1f" % exp[i]]
