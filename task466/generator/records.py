"""Record-level truth for task466: the plant event log (engines and flare), the engines' electricity, the surface
walkovers with the analyser's calibration checks, the wellfield rounds, weather, leachate and the weighbridge
archive. Built from world.build(); every draw on its own fixed stream."""
import datetime as dt

import numpy as np

import common as C
import world as W

FLARE_MIN_TEMP_F = 1400
GRID_TIE = (1000.0, 2000.0, 43.183150, -89.672840)   # site grid E, N (US survey ft) at this WGS84 latitude, longitude
FT_PER_DEG_LAT = 364000.0


def site_to_wgs84(x, y):
    import math
    e0, n0, la0, lo0 = GRID_TIE
    lat = la0 + (y - n0) / FT_PER_DEG_LAT
    lon = lo0 + (x - e0) / (FT_PER_DEG_LAT * math.cos(math.radians(la0)))
    return lat, lon


def minute_time(m):
    return W.T0 + dt.timedelta(minutes=int(m))


# ------------------------------------------------------------------------------------------------ flare
def flare_states(p):
    """The flare's lit state minute by minute and its combustion-temperature permissive (1,400 F reached).

    The flare is lit whenever the plant runs and the engines cannot take all the gas: an engine stopped, or the
    capture above the engines' capacity (the recovery after a restart). After each ignition the chamber takes 12 to
    24 minutes to reach 1,400 F; at very low flare flows it sags below the setpoint and recovers.
    """
    r = W.rng(60)
    nmin = W.NH * 60
    hourly = p["capture"] / np.maximum(p["run_frac"], 1e-9)                          # kg/h while running
    # minute-level rate: linear between hour centres plus a small wobble, so transitions fall on any minute
    xm = np.arange(W.NH * 60) / 60.0
    cap_rate = np.interp(xm, np.arange(W.NH) + 0.5, hourly)
    wob = np.convolve(r.normal(0, 3.0, W.NH * 60), np.ones(25) / 25.0, mode="same")
    cap_rate = cap_rate + wob
    plant_on = np.repeat(p["run_frac"], 60) > 0
    # minute-level plant running from the outage list
    run = np.ones(nmin, dtype=bool)
    for o in p["outages"]:
        a = int((o["start"] - W.T0).total_seconds() // 60)
        b = int((o["end"] - W.T0).total_seconds() // 60)
        run[a:b] = False
    eng_cap = W.ENG_CAP * (p["eng_on_min"][1].astype(float) + p["eng_on_min"][2].astype(float))
    need = run & (cap_rate - eng_cap > 1.0)
    lit = need.copy()
    # warm-up and low-temperature episodes
    permissive = lit.copy()
    starts = np.flatnonzero(lit[1:] & ~lit[:-1]) + 1
    if lit[0]:
        starts = np.r_[0, starts]
    for s in starts:
        warm = int(r.uniform(12, 25))
        permissive[s:s + warm] = False
    # low-flow sags: when the flare share is small, a few sags of 6 to 30 minutes
    flare_rate = np.maximum(cap_rate - eng_cap, 0)
    lowflow = lit & (flare_rate < 40)
    idx = np.flatnonzero(lowflow)
    if len(idx):
        picks = r.choice(idx, size=min(len(idx) // 900 + 6, len(idx)), replace=False)
        for s in sorted(picks):
            d = int(r.uniform(6, 31))
            seg = slice(s, min(nmin, s + d))
            permissive[seg] = permissive[seg] & ~lit[seg]
    permissive &= lit
    return lit, permissive


def flare_events(lit, permissive):
    ev = []
    n = len(lit)
    prev_l, prev_p = False, False
    for m in np.flatnonzero(np.r_[True, (lit[1:] != lit[:-1]) | (permissive[1:] != permissive[:-1])]):
        if m >= n:
            break
        l, pm = bool(lit[m]), bool(permissive[m])
        if l and not prev_l:
            ev.append((m, "FLR", "FLARE START", "pilot proven, main burner lit"))
            if pm:
                ev.append((m, "FLR", "TEMP PERMISSIVE", "combustion temperature at setpoint"))
        elif not l and prev_l:
            ev.append((m, "FLR", "FLARE STOP", "no demand"))
        elif l and prev_l:
            if pm and not prev_p:
                ev.append((m, "FLR", "TEMP PERMISSIVE" if not any(e[2] == "LOW TEMP" for e in ev[-1:]) else "TEMP RESTORED",
                           "combustion temperature at setpoint"))
            elif not pm and prev_p:
                ev.append((m, "FLR", "LOW TEMP", "combustion temperature below setpoint"))
        prev_l, prev_p = l, pm
    return ev


# ------------------------------------------------------------------------------------------------ engines
def engine_events(p):
    """The engine plant's event log lines per engine (tagged GEN1 and GEN2), minute resolution.

    A utility power failure takes the controllers down with the plant: no stop line is written, and when the supply
    returns the controller writes CONTROLLER POWER UP with the engine standing. Grid disturbances open an engine's
    breaker for under two minutes while it keeps turning; it re-synchronises and writes RUNNING again.
    """
    r = W.rng(70)
    ev = []
    outages = p["outages"]
    power_fail = {}
    for k, o in enumerate(outages):
        if o["cause"] == "Utility power failure":
            power_fail[int((o["start"] - W.T0).total_seconds() // 60)] = k
    reasons = {"oil": ("STOP", "operator stop - oil change"),
               "service": ("STOP", "operator stop - scheduled service"),
               "trip": None}
    trip_text = ["jacket water temperature high", "misfire cylinder 7", "gas quality low (methane)",
                 "knock limit", "oil pressure low", "exhaust temperature deviation"]
    for e in (1, 2):
        tag = "GEN%d" % e
        on = p["eng_on_min"][e]
        for s in p["eng_stops"][e]:
            a, b = s["start"], s["end"]
            if s["kind"] == "plant":
                o = outages[s["outage"]]
                if o["cause"] == "Utility power failure":
                    # the controller loses power: nothing written at the stop; power-up when the supply returns
                    up = int((o["end"] - W.T0).total_seconds() // 60) + int(r.uniform(1, 4))
                    ev.append((up, tag, "CONTROLLER POWER UP", "state: standstill"))
                else:
                    ev.append((a, tag, "TRIP", "gas supply pressure low"))
            elif s["kind"] == "trip":
                ev.append((a, tag, "TRIP", trip_text[int(r.integers(0, len(trip_text)))]))
            else:
                ev.append((a, tag, reasons[s["kind"]][0], reasons[s["kind"]][1]))
            # restart: start request, then running when synchronised (3 to 7 minutes)
            if b < len(on):
                req = max(a + 1, b - int(r.uniform(3, 8)))
                # occasionally a failed first attempt
                if r.uniform() < 0.10:
                    ev.append((req - 6, tag, "START REQUEST", "auto"))
                    ev.append((req - 4, tag, "START FAIL", "no ignition - retry"))
                ev.append((req, tag, "START REQUEST", "auto" if s["kind"] in ("plant", "trip") else "operator"))
                ev.append((b, tag, "RUNNING", "synchronised"))
        # grid disturbances while running: breaker opens, engine keeps turning, re-synchronises (candidate minutes
        # drawn on their own stream, so a change to a stop elsewhere does not move them)
        rd = W.rng(75 + e)
        cand = np.sort(rd.choice(len(on) - 5, size=int(rd.integers(26, 38)) * 3, replace=False))
        gaps = rd.integers(1, 3, size=len(cand))
        for m, g in zip(cand, gaps):
            if not on[m:m + 3].all():
                continue
            ev.append((int(m), tag, "BREAKER OPEN", "grid disturbance - load shed"))
            ev.append((int(m) + int(g), tag, "RUNNING", "synchronised"))
    ev.sort(key=lambda x: (x[0], x[1]))
    return ev


def engine_truth(p):
    """True running hours (on the grid) and starts per engine per local quarter of 2026."""
    out = {}
    for e in (1, 2):
        on = p["eng_on_min"][e]
        for q in range(4):
            a, b = quarter_minutes(2026, q)
            seg = on[a:b]
            hours = seg.sum() / 60.0
            prev = on[a - 1] if a > 0 else True
            starts = int(((seg[1:] & ~seg[:-1]).sum()) + (1 if (seg[0] and not prev) else 0))
            out[(e, q + 1)] = dict(hours=hours, starts=starts)
    return out


def quarter_minutes(year, q):
    m0 = (1, 4, 7, 10)[q]
    a = dt.datetime(year, m0, 1, tzinfo=C.TZ).astimezone(C.UTC)
    b = (dt.datetime(year, m0 + 3, 1, tzinfo=C.TZ) if q < 3 else dt.datetime(year + 1, 1, 1, tzinfo=C.TZ)).astimezone(C.UTC)
    return int((a - W.T0).total_seconds() // 60), int((b - W.T0).total_seconds() // 60)


def quarter_hours_utc(year, q):
    a, b = quarter_minutes(year, q)
    return a // 60, b // 60


# ------------------------------------------------------------------------------------------------ surface walkovers
def surface_walkovers(p):
    """Quarterly instrument walkovers of the cap: a 30 m grid plus every well boot, readings in ppm methane.

    Exceedances (over 500 ppm) are marked, repaired, and re-monitored within ten days; the re-monitoring is logged at
    the spot found on the day (by GPS), under a re-monitoring label. In the third quarter the analyser failed its
    midday drift check (reading 22 per cent high on the span gas) and the morning's points were walked again after
    recalibration; the morning readings stay in the logger export.
    """
    r = W.rng(80)
    # site grid in feet (local site coordinates)
    pts = []
    k = 0
    for i in range(23):
        for j in range(15):
            x, y = 1000 + i * 98.4, 2000 + j * 98.4
            # a lobed footprint: drop corners
            if (i < 3 and j > 11) or (i > 19 and j < 2):
                continue
            k += 1
            pts.append(dict(label="G-%03d" % k, x=x, y=y, kind="grid"))
    wells = []
    for w in range(1, 63):
        x = 1000 + (w * 7.37 % 21) * 98.4 + r.uniform(-20, 20)
        y = 2000 + (w * 3.11 % 14) * 98.4 + r.uniform(-20, 20)
        wells.append(dict(label="WB-EW%02d" % w, x=x, y=y, kind="boot"))
    allpts = pts + wells
    walk_days = {1: [(2026, 3, 17)], 2: [(2026, 6, 9), (2026, 6, 10)], 3: [(2026, 9, 15), (2026, 9, 16)],
                 4: [(2026, 12, 8)]}
    walks = []
    for q in (1, 2, 3, 4):
        days = walk_days[q]
        n = len(allpts)
        order = list(range(n))
        # true readings: background with hot spots at boots and seams
        base = r.lognormal(np.log(18), 0.8, n)
        hot = r.choice(n, size=int(r.integers(14, 22)), replace=False)
        true = base.copy()
        true[hot] = r.uniform(120, 480, len(hot))
        exc = r.choice([h for h in hot], size=int(r.integers(6, 10)), replace=False)
        true[exc] = r.uniform(560, 3800, len(exc))
        # the found peak lies a few feet off the grid point
        offx = r.uniform(-18, 18, n)
        offy = r.uniform(-18, 18, n)
        rows = []
        per_day = int(np.ceil(n / len(days)))
        for di, d in enumerate(days):
            seg = order[di * per_day:(di + 1) * per_day]
            t = dt.datetime(d[0], d[1], d[2], 7, 40, tzinfo=C.TZ)
            for idx in seg:
                t = t + dt.timedelta(seconds=int(r.uniform(48, 95)))
                if t.hour == 11 and t.minute < 50:
                    t = t.replace(hour=12, minute=30)
                pt = allpts[idx]
                rows.append(dict(t=t, label=pt["label"], x=pt["x"] + offx[idx], y=pt["y"] + offy[idx],
                                 ppm=float(true[idx]), idx=int(idx), void=False))
        walk = dict(q=q, days=days, rows=rows, true=true, exc=set(int(i) for i in exc), pts=allpts,
                    offx=offx, offy=offy)
        walks.append(walk)
    # the third quarter's drift: points read on day 1 between the 07:30 check and the failed 12:00 check
    w3 = walks[2]
    d1 = dt.datetime(2026, 9, 15, 12, 0, tzinfo=C.TZ)
    morning = [row for row in w3["rows"] if row["t"].date() == d1.date() and row["t"] < d1]
    rewalk = []
    t = dt.datetime(2026, 9, 16, 13, 10, tzinfo=C.TZ)
    for row in morning:
        row["void"] = True
        row["ppm_logged"] = row["ppm"] * 1.22
        t = t + dt.timedelta(seconds=int(r.uniform(50, 90)))
        rewalk.append(dict(t=t, label=row["label"], x=row["x"] + r.uniform(-4, 4), y=row["y"] + r.uniform(-4, 4),
                           ppm=row["ppm"], idx=row["idx"], void=False))
    for row in w3["rows"]:
        if "ppm_logged" not in row:
            row["ppm_logged"] = row["ppm"]
    for wk in walks:
        for row in wk["rows"]:
            row.setdefault("ppm_logged", row["ppm"])
    for rw in rewalk:
        rw["ppm_logged"] = rw["ppm"]
    w3["rows"] = w3["rows"] + rewalk
    # make the drift matter: a few morning points sit between 410 and 500 ppm, so the drifted reading crosses 500
    for row in morning[: min(len(morning), 60)]:
        pass
    cand = [row for row in morning if row["idx"] not in w3["exc"]]
    picks = r.choice(len(cand), size=min(4, len(cand)), replace=False)
    for pi in picks:
        row = cand[pi]
        v = float(r.uniform(420, 495))
        row["ppm"] = v
        row["ppm_logged"] = v * 1.22
        w3["true"][row["idx"]] = v
        for rw in rewalk:
            if rw["idx"] == row["idx"]:
                rw["ppm"] = v
    # re-monitoring at the spot (handheld GPS, WGS84), under a running re-monitoring number: a first re-check four
    # to nine days after the walkover, a second one for a location still over, and in two quarters a location that
    # fails both and is cleared at a third visit; the year opens with the re-checks of the fourth 2025 walkover
    rmrows = []
    seq = [0]

    def add(t, x, y, ppm, idx, q, visit):
        seq[0] += 1
        rmrows.append(dict(t=t, label="RM-26-%03d" % seq[0], x=x, y=y, ppm=ppm, idx=idx, q=q, visit=visit))

    for (d, x, y, ppm) in ((dt.datetime(2026, 1, 6, 10, 20, tzinfo=C.TZ), 1640.2, 2711.8, 640.0),
                           (dt.datetime(2026, 1, 6, 10, 55, tzinfo=C.TZ), 2391.5, 2203.4, 85.0),
                           (dt.datetime(2026, 1, 15, 9, 40, tzinfo=C.TZ), 1640.6, 2712.9, 120.0)):
        add(d, x, y, ppm, None, 0, 0)
    double_fail_q = (2, 4)
    for wk in walks:
        q = wk["q"]
        last_day = dt.date(*wk["days"][-1])
        rm = []
        exc_sorted = sorted(wk["exc"])
        for n_i, idx in enumerate(exc_sorted):
            still = r.uniform() < 0.30
            if q in double_fail_q and n_i == 0:
                still = True
            pt = wk["pts"][idx]
            bx, by = pt["x"] + wk["offx"][idx], pt["y"] + wk["offy"][idx]
            d1 = last_day + dt.timedelta(days=int(r.integers(4, 10)))
            t1 = dt.datetime(d1.year, d1.month, d1.day, int(r.integers(8, 15)), int(r.integers(0, 60)), tzinfo=C.TZ)
            ppm1 = float(r.uniform(540, 1600)) if still else float(r.uniform(30, 380))
            rm.append(dict(t=t1, idx=idx, still=still, ppm=ppm1, x=bx + r.uniform(-6, 6), y=by + r.uniform(-6, 6), visit=1))
            if still:
                d2 = d1 + dt.timedelta(days=int(r.integers(5, 10)))
                t2 = dt.datetime(d2.year, d2.month, d2.day, int(r.integers(8, 15)), int(r.integers(0, 60)), tzinfo=C.TZ)
                fail2 = q in double_fail_q and n_i == 0
                ppm2 = float(r.uniform(520, 900)) if fail2 else float(r.uniform(25, 300))
                rm.append(dict(t=t2, idx=idx, still=fail2, ppm=ppm2, x=bx + r.uniform(-6, 6), y=by + r.uniform(-6, 6), visit=2))
                if fail2:
                    d3 = d2 + dt.timedelta(days=int(r.integers(5, 9)))
                    t3 = dt.datetime(d3.year, d3.month, d3.day, int(r.integers(8, 15)), int(r.integers(0, 60)), tzinfo=C.TZ)
                    rm.append(dict(t=t3, idx=idx, still=False, ppm=float(r.uniform(20, 200)), x=bx + r.uniform(-6, 6),
                                   y=by + r.uniform(-6, 6), visit=3))
        wk["recheck"] = [x for x in rm if x["visit"] == 1]
        wk["recheck_all"] = rm
    allrm = []
    for wk in walks:
        for x in wk["recheck_all"]:
            allrm.append((x["t"], x, wk["q"]))
    for t_, x, q in sorted(allrm, key=lambda z: z[0]):
        add(x["t"], x["x"], x["y"], x["ppm"], x["idx"], q, x["visit"])
    for wk in walks:
        wk["rm_rows"] = rmrows
    return walks


def calibration_log(walks):
    """The analyser's zero and span checks on each walkover day: 07:30, 12:00 and 15:30 local."""
    r = W.rng(90)
    rows = []
    for wk in walks:
        for d in wk["days"]:
            for hh, mm in ((7, 30), (12, 0), (15, 30)):
                t = dt.datetime(d[0], d[1], d[2], hh, mm, tzinfo=C.TZ)
                span_ref = 500.0
                read = span_ref * (1 + r.normal(0, 0.012))
                ok = True
                if wk["q"] == 3 and d == (2026, 9, 15) and hh == 12:
                    read = span_ref * 1.22
                    ok = False
                rows.append(dict(t=t, zero=round(float(r.uniform(-0.6, 0.9)), 1), span_ref=span_ref,
                                 span_read=round(float(read), 1), result="PASS" if ok else "FAIL"))
                if not ok:
                    t2 = t + dt.timedelta(minutes=50)
                    rows.append(dict(t=t2, zero=0.2, span_ref=span_ref, span_read=round(span_ref * 1.004, 1),
                                     result="PASS", note="recalibrated"))
        # the day after a failure the walker re-walks the void points (afternoon, day 2)
    rows.sort(key=lambda x: x["t"])
    return rows


# ------------------------------------------------------------------------------------------------ distractors
def weather(p):
    r = W.rng(100)
    days = []
    d = dt.date(2024, 1, 1)
    while d.year < 2027:
        doy = d.timetuple().tm_yday
        t = 10.5 - 13.5 * np.cos(2 * np.pi * (doy - 18) / 365.25) + r.normal(0, 3.5)
        pr = 1016.5 + r.normal(0, 6.5)
        rain = float(max(0.0, r.gamma(0.45, 6.0) - 1.2))
        days.append(dict(d=d, tmax=round(t + 6 + r.uniform(0, 2), 1), tmin=round(t - 6 - r.uniform(0, 2), 1),
                         p=round(pr, 1), rain=round(rain, 1)))
        d += dt.timedelta(days=1)
    return days


def leachate(p):
    r = W.rng(110)
    rows = []
    d = dt.date(2026, 1, 1)
    while d.year == 2026:
        if d.weekday() < 5:
            rows.append(dict(d=d, sump="LS-1", level=round(float(r.uniform(1.2, 3.8)), 2),
                             pumped=int(r.uniform(2100, 9800)), hauled=int(r.choice([0, 0, 0, 6000, 7200]))))
        d += dt.timedelta(days=1)
    return rows


def weighbridge_archive():
    r = W.rng(120)
    rows = []
    for y in range(2004, 2018):
        for m in range(1, 13):
            if y == 2017 and m > 3:
                break
            for code, name, base in (("MSW", "Municipal solid waste", 21500), ("CI", "Commercial and industrial", 6200),
                                     ("CD", "Construction and demolition", 3100), ("SL", "Biosolids", 640),
                                     ("CV", "Cover soil (inbound)", 4200)):
                rows.append(dict(y=y, m=m, code=code, name=name,
                                 tons=int(base * (1 + 0.18 * np.sin(2 * np.pi * (m - 4) / 12)) * r.uniform(0.86, 1.14))))
    return rows
