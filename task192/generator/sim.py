"""The clean truth: weather, lightning, every fault on the overhead lines, what each protective device did, every
sustained interruption with its restoration, and every momentary interruption event.

Times are integer milliseconds of UTC from 2025-01-01T00:00Z unless named otherwise."""
import datetime as dt
import math

import numpy as np
from scipy.spatial import cKDTree

import world as W

EPOCH = dt.datetime(2025, 1, 1)
MS_H = 3600 * 1000
MS_MIN = 60 * 1000
MS_DAY = 24 * MS_H


def ts(y, m, d, hh=0, mm=0, ss=0):
    return int((dt.datetime(y, m, d, hh, mm, ss) - EPOCH).total_seconds() * 1000)


DST = [(ts(2025, 3, 9, 8), ts(2025, 11, 2, 7)), (ts(2026, 3, 8, 8), ts(2026, 11, 1, 7))]
T0 = ts(2025, 1, 1, 6)           # local 2025-01-01 00:00 CST
T1 = ts(2026, 11, 1, 5)          # local 2026-11-01 00:00 CDT


def offset_ms(t):
    for a, b in DST:
        if a <= t < b:
            return -5 * MS_H
    return -6 * MS_H


def local_dt(t):
    return EPOCH + dt.timedelta(milliseconds=t + offset_ms(t))


def local_day(t):
    return local_dt(t).date()


def utc_dt(t):
    return EPOCH + dt.timedelta(milliseconds=t)


def from_local(d, hh, mm=0, ss=0):
    """UTC ms of a local wall-clock time (never inside a DST gap here)."""
    guess = int((dt.datetime(d.year, d.month, d.day, hh, mm, ss) - EPOCH).total_seconds() * 1000) + 6 * MS_H
    if offset_ms(guess - MS_H) == -5 * MS_H:
        guess -= MS_H
    return guess


def days():
    d = W.DATA0
    while d <= W.DATA1:
        yield d
        d += dt.timedelta(days=1)


# --------------------------------------------------------------------------- weather
MED_STORMS = {dt.date(2025, 4, 2): "squall", dt.date(2026, 5, 19): "supercell", dt.date(2026, 6, 27): "derecho"}
ICE = {dt.date(2025, 2, 12): (2, 8, 0.35), dt.date(2026, 1, 24): (1, 7, 0.75)}


def weather(rng):
    """Hourly airport observations (UTC hours) and the convective cells that cross the service territory."""
    nh = (T1 - T0) // MS_H + 30
    h0 = T0 - 6 * MS_H
    hours = h0 + np.arange(nh) * MS_H
    loc = [local_dt(int(h)) for h in hours]
    doy = np.array([l.timetuple().tm_yday for l in loc])
    lh = np.array([l.hour + l.minute / 60 for l in loc])
    dayidx = np.array([(l.date() - dt.date(2024, 12, 31)).days for l in loc])
    nd = dayidx.max() + 2
    anom = np.zeros(nd)
    for k in range(1, nd):
        anom[k] = 0.72 * anom[k - 1] + rng.normal(0, 4.2)
    tmean = 56.5 - 22.5 * np.cos(2 * np.pi * (doy - 20) / 365)
    amp = 10 + 1.5 * np.sin(2 * np.pi * (doy - 100) / 365)
    temp = tmean + amp * np.cos(2 * np.pi * (lh - 15.2) / 24) + anom[dayidx]
    # humidity: dawn maximum by night, afternoon minimum by day
    rhmax_d = np.clip(rng.normal(0, 1, nd), -3, 3)
    d_doy = np.array([(dt.date(2024, 12, 31) + dt.timedelta(days=int(k))).timetuple().tm_yday for k in range(nd)])
    humid = 0.5 + 0.5 * np.exp(-((d_doy - 245) / 55.0) ** 2)
    rhmax = np.clip(88 + 9 * humid + 4.5 * rhmax_d, 70, 100)
    rhmin = np.clip(48 + 12 * humid + rng.normal(0, 8, nd), 25, 85)
    night = 0.5 + 0.5 * np.cos(2 * np.pi * (lh - 6.0) / 24)
    rh = rhmin[dayidx] + (rhmax[dayidx] - rhmin[dayidx]) * night ** 1.6
    # synoptic wind days, fronts in the cool season
    windy = rng.random(nd) < (0.05 + 0.07 * (1 - humid))
    wspd = np.clip(6 + 3 * np.sin(2 * np.pi * (lh - 9) / 24) + rng.normal(0, 2.2, nh), 0, None)
    gust = np.zeros(nh)
    wd = windy[dayidx]
    wspd[wd] += rng.uniform(7, 15, wd.sum())
    gust[wd] = wspd[wd] + rng.uniform(6, 16, wd.sum())
    precip = np.zeros(nh)
    rainday = rng.random(nd) < (0.16 + 0.06 * np.cos(2 * np.pi * (d_doy - 120) / 365))
    for k in np.where(rainday)[0]:
        start = int(rng.integers(0, 24))
        dur = int(rng.integers(2, 9))
        idx = np.where((dayidx == k) & (lh >= start) & (lh < start + dur))[0]
        precip[idx] += rng.gamma(1.2, 0.04, len(idx))
        rh[idx] = np.maximum(rh[idx], rng.uniform(88, 99, len(idx)))
    # convective cells
    cells = []
    for k in range(1, nd):
        d = dt.date(2024, 12, 31) + dt.timedelta(days=int(k))
        if d < W.DATA0 or d > W.DATA1:
            continue
        yd = d.timetuple().tm_yday
        p = 0.035 + 0.30 * math.exp(-((yd - 168) / 52.0) ** 2)
        extra_nw = d.year == 2026 and 6 <= d.month <= 9
        if d in MED_STORMS:
            n = 3
        elif rng.random() < p:
            n = 1 + int(rng.poisson(0.8))
        else:
            n = 0
        if extra_nw and rng.random() < 0.20:
            cells.append(_cell(rng, d, nw=True))
        for _ in range(n):
            cells.append(_cell(rng, d, med=MED_STORMS.get(d)))
    # the airport sees the cells that pass near it
    ax, ay = W.AIRPORT[1], W.AIRPORT[2]
    ts_flag = np.zeros(nh, dtype=bool)
    for c in cells:
        hs = np.where((hours >= c["t0"] - MS_H) & (hours <= c["t0"] + c["dur"]))[0]
        for j in hs:
            tt = max(0.0, (hours[j] - c["t0"]) / MS_H)
            cx, cy = c["x0"] + c["vx"] * tt, c["y0"] + c["vy"] * tt
            dist = math.hypot(cx - ax, cy - ay)
            if dist < 14:
                ts_flag[j] = True
                precip[j] += float(rng.gamma(1.5, 0.12)) * (1.5 if dist < 6 else 0.6)
                rh[j] = max(rh[j], 92)
                g = c["gust"] * max(0.3, 1 - dist / 16) + float(rng.normal(0, 3))
                gust[j] = max(gust[j], g)
                wspd[j] = max(wspd[j], 0.55 * g)
    gust = np.where(gust < wspd + 9, 0, gust)
    rh = np.clip(rh, 15, 100)
    dew = _dewpoint(temp, rh)
    vis = np.full(nh, 10.0)
    calm = wspd < 5
    fog = (rh >= 98) & calm & (lh >= 3) & (lh <= 9)
    mist = (rh >= 95) & ~fog & (lh >= 2) & (lh <= 10)
    vis[mist] = np.round(rng.uniform(2, 6, mist.sum()), 0)
    vis[fog] = rng.choice([0.25, 0.5, 0.75], fog.sum())
    vis[precip > 0.1] = np.minimum(vis[precip > 0.1], 4)
    return dict(hours=hours, temp=temp, dew=dew, rh=rh, wspd=wspd, gust=gust, precip=precip, vis=vis,
                ts=ts_flag, fog=fog, mist=mist, lh=lh, cells=cells, loc=loc)


def _dewpoint(tf, rh):
    tc = (tf - 32) / 1.8
    a, b = 17.62, 243.12
    g = np.log(np.clip(rh, 1, 100) / 100) + a * tc / (b + tc)
    return (b * g / (a - g)) * 1.8 + 32


def _cell(rng, d, nw=False, med=None):
    hr = float(rng.choice([rng.uniform(13, 21), rng.uniform(21, 28)], p=[0.72, 0.28]))
    if med == "derecho":
        hr = float(rng.uniform(2.6, 3.8))
    if med == "supercell":
        hr = float(rng.uniform(18.0, 19.5))
    if med == "squall":
        hr = float(rng.uniform(15.0, 17.0))
    base = W_from_local(d, hr)
    x0 = float(rng.uniform(-38, -26))
    y0 = float(rng.uniform(-18, 22))
    if nw:
        y0 = float(rng.uniform(1, 11))
    vx = float(rng.uniform(22, 48))
    vy = float(rng.uniform(-9, 12))
    dur = float(rng.uniform(1.4, 2.6))
    rate = float(rng.lognormal(math.log(1.05), 0.65))
    gust = float(rng.uniform(26, 44))
    if med:
        rate *= 2.2
        gust = float(rng.uniform(58, 72))
        dur = 2.2
        # a line that sweeps the whole territory, crossing the airport
        y0 = W.AIRPORT[2] - vy * (W.AIRPORT[1] - x0) / vx + float(rng.normal(0, 3))
    return dict(t0=base, x0=x0, y0=y0, vx=vx, vy=vy, dur=dur * MS_H, rate=rate, gust=gust, nw=nw, med=med)


def W_from_local(d, hr):
    extra = int(hr // 24)
    dd = d + dt.timedelta(days=extra)
    h = hr - 24 * extra
    hh = int(h)
    mm = int((h - hh) * 60)
    return from_local(dd, hh, mm, int(((h - hh) * 60 - mm) * 60))


def strokes(rng, cells):
    """Lightning strokes from each cell: cloud-to-ground strokes with their peak current, and cloud pulses."""
    rows = []
    for c in cells:
        n_flash = int(rng.poisson(c["rate"] * c["dur"] / MS_MIN))
        for _ in range(n_flash):
            u = float(rng.random())
            t = c["t0"] + int(u * c["dur"])
            cx = c["x0"] + c["vx"] * u * c["dur"] / MS_H
            cy = c["y0"] + c["vy"] * u * c["dur"] / MS_H
            fx, fy = cx + float(rng.normal(0, 3.2)), cy + float(rng.normal(0, 3.2))
            if rng.random() < 0.34:
                rows.append((t, fx, fy, round(float(rng.normal(0, 1) * 6 + 4), 1), "IC"))
                continue
            pos = rng.random() < 0.11
            nstk = 1 + int(rng.poisson(1.25 if not pos else 0.1))
            tt = t
            for s in range(nstk):
                amp = float(rng.lognormal(math.log(34 if pos else 21), 0.55))
                sx, sy = (fx, fy) if s == 0 or rng.random() < 0.55 else (fx + float(rng.normal(0, 0.9)),
                                                                          fy + float(rng.normal(0, 0.9)))
                rows.append((tt, sx, sy, round(amp if pos else -amp, 1), "CG"))
                tt += int(rng.uniform(25, 140))
    rows = [r for r in rows if -26 <= r[1] <= 26 and -24 <= r[2] <= 26 and T0 <= r[0] < T1]
    rows.sort()
    return rows


# --------------------------------------------------------------------------- the network's geometry
def line_points(net):
    """Points every 0.05 mile along every overhead main line and lateral: (x, y, feeder, lateral or None, position)."""
    pts = []
    for fid, F in net["feeders"].items():
        for k, (x, y) in enumerate(F["path"][1:]):
            pts.append((x, y, fid, None, (k + 1) * 0.05))
        for lat in F["laterals"]:
            L = net["laterals"][lat]
            k0 = min(len(F["path"]) - 1, int(L["tap"] / 0.05))
            x0, y0 = F["path"][k0]
            n = max(1, int(L["length"] / 0.05))
            for j in range(n):
                s = (j + 1) * 0.05
                pts.append((x0 + s * 1.609 * math.cos(L["ang"]), y0 + s * 1.609 * math.sin(L["ang"]), fid, lat, s))
    return pts


# --------------------------------------------------------------------------- faults
def _phase_for(rng, phase_avail, kind):
    if len(phase_avail) == 1:
        return phase_avail
    r = rng.random()
    if kind == "SLG" or r < 0.66:
        return "ABC"[int(rng.integers(0, 3))]
    if r < 0.93:
        return ["AB", "BC", "CA"][int(rng.integers(0, 3))]
    return "ABC"


def _random_location(rng, net, fid, at_transformer=False, trs_by_f=None):
    F = net["feeders"][fid]
    if at_transformer:
        wts = np.array([net["transformers"][t]["lure"] for t in trs_by_f[fid]])
        tid = trs_by_f[fid][int(rng.choice(len(wts), p=wts / wts.sum()))]
        T = net["transformers"][tid]
        return dict(lateral=T["lateral"], pos=T["pos"], lpos=T["lpos"], transformer=tid,
                    phases_avail=T["phase"] if len(T["phase"]) == 1 else "ABC")
    tot = F["main"] + F["lat_mi"]
    if rng.random() < F["main"] / tot:
        return dict(lateral=None, pos=float(rng.uniform(0.02, F["main"])), lpos=0.0, transformer=None,
                    phases_avail="ABC")
    lens = np.array([net["laterals"][l]["length"] * net["laterals"][l]["expo"] for l in F["laterals"]])
    lat = F["laterals"][int(rng.choice(len(lens), p=lens / lens.sum()))]
    L = net["laterals"][lat]
    return dict(lateral=lat, pos=L["tap"], lpos=float(rng.uniform(0.01, L["length"])), transformer=None,
                phases_avail=L["phase"])


# the share of faults that clear by themselves: on the main line's crossarms and insulators, and on a tap or at a
# transformer, where a fuse sits closer to the fault
TEMP_P = {"lightning": 0.97, "tree": 0.93, "wet_tree": 0.95, "animal": 0.97, "equipment": 0.3, "incipient": 1.0,
          "vehicle": 0.0, "storm_damage": 0.15, "ice": 0.0}
TEMP_P_TAP = {"lightning": 0.85, "tree": 0.8, "wet_tree": 0.85, "animal": 0.6, "equipment": 0.2, "incipient": 1.0,
              "vehicle": 0.0, "storm_damage": 0.12, "ice": 0.0}


def candidate_faults(rng, net, wx, stk):
    """Every fault before protection decides anything: time, feeder, place, phases, resistance, cause and whether
    it would clear by itself."""
    faults = []
    trs_by_f = {}
    for tid, T in net["transformers"].items():
        trs_by_f.setdefault(T["feeder"], []).append(tid)
    for f in trs_by_f:
        trs_by_f[f].sort()
    # lightning: strokes near an overhead line
    pts = line_points(net)
    tree = cKDTree(np.array([(p[0], p[1]) for p in pts]))
    for (t, x, y, amp, kind) in stk:
        if kind != "CG":
            continue
        dist, j = tree.query((x, y))
        if dist > 1.0:
            continue
        _, _, fid, lat, s = pts[j]
        spec = W.FEEDERS[W.FIX[fid]]
        p = 0.22 * spec["light"] * min(1.0, (abs(amp) / 30.0) ** 1.3) * math.exp(-dist / 0.22)
        if rng.random() < p:
            L = net["laterals"].get(lat)
            loc = dict(lateral=lat, pos=(L["tap"] if lat else s), lpos=(s if lat else 0.0), transformer=None,
                       phases_avail=(L["phase"] if lat else "ABC"))
            faults.append(_fault(rng, t + int(rng.uniform(0, 40)), fid, loc, "lightning",
                                 rf=float(rng.uniform(0.4, 2.2))))
    hours, gust, precip, rh, lh = wx["hours"], wx["gust"], wx["precip"], wx["rh"], wx["lh"]
    med_gust = np.zeros(len(hours))
    for c in wx["cells"]:
        if c["med"]:
            k = np.where((hours >= c["t0"] - MS_H) & (hours < c["t0"] + c["dur"]))[0]
            med_gust[k] = np.maximum(med_gust[k], c["gust"])
    for j, h in enumerate(hours):
        h = int(h)
        if h < T0 or h >= T1:
            continue
        d = local_day(h)
        yr = d.year
        med = MED_STORMS.get(d)
        g = max(gust[j], med_gust[j])
        doy = d.timetuple().tm_yday
        anim_season = 1 + 0.55 * math.exp(-((doy - 108) / 24.0) ** 2) + 1.05 * math.exp(-((doy - 272) / 30.0) ** 2)
        daylight = 6.5 <= lh[j] <= 18.5
        hour_profile = 1.6 if 7 <= lh[j] <= 10.5 else (1.0 if daylight else 0.0)
        damp_am = rh[j] >= 97 and 4 <= lh[j] <= 9
        for f in W.FEEDERS:
            fid = f["id"]
            F = net["feeders"][fid]
            ohm = F["main"] + F["lat_mi"]
            tr = W.year_value(f["tree"], yr)
            if fid == "MLR-2" and d >= W.CLEARANCE[1]:
                tr = f["tree"][1]
            elif fid == "MLR-2" and d >= W.CLEARANCE[0]:
                tr = 0.5 * (f["tree"][0] + f["tree"][1])
            elif fid == "MLR-2":
                tr = f["tree"][0]
            wet = W.year_value(f["wet"], yr) if not isinstance(f["wet"], tuple) else \
                (f["wet"][1] if (fid == "MLR-2" and d >= W.CLEARANCE[1]) else f["wet"][0])
            lam = 0.0
            if g > 22:
                lam += 0.00012 * tr * ohm * (g - 22) ** 1.5
            if med:
                lam *= 6.0
            for _ in range(int(rng.poisson(lam))):
                t = h + int(rng.uniform(0, MS_H))
                loc = _random_location(rng, net, fid)
                kind = "SLG" if rng.random() < 0.55 else "LL"
                rf = float(rng.lognormal(math.log(6.0), 0.85)) if kind == "SLG" else float(rng.uniform(0.4, 6))
                faults.append(_fault(rng, t, fid, loc, "storm_damage" if med else "tree", rf=rf, kind=kind))
            lam_w = 0.0
            if precip[j] > 0.01:
                lam_w += 0.0022 * wet * ohm
            if damp_am:
                lam_w += 0.0034 * wet * ohm
            for _ in range(int(rng.poisson(lam_w))):
                t = h + int(rng.uniform(0, MS_H))
                loc = _random_location(rng, net, fid)
                faults.append(_fault(rng, t, fid, loc, "wet_tree", rf=float(rng.lognormal(math.log(7), 0.5)),
                                     kind="SLG"))
            if hour_profile and not (precip[j] > 0.05):
                an = W.year_value(f["animal"], yr)
                lam_a = 0.00010 * an * ohm * anim_season * hour_profile
                for _ in range(int(rng.poisson(lam_a))):
                    t = h + int(rng.uniform(0, MS_H))
                    at_t = rng.random() < 0.72
                    loc = _random_location(rng, net, fid, at_transformer=at_t, trs_by_f=trs_by_f)
                    faults.append(_fault(rng, t, fid, loc, "animal", rf=float(rng.uniform(0.2, 2.0)), kind="SLG"))
            if rng.random() < 0.0000105 * ohm:
                t = h + int(rng.uniform(0, MS_H))
                loc = _random_location(rng, net, fid)
                faults.append(_fault(rng, t, fid, loc, "equipment", rf=float(rng.uniform(0.2, 2.5))))
    # ice: limbs come down on the main lines under freezing rain, and stay there
    for d, (h0, h1, k) in sorted(ICE.items()):
        a, b = from_local(d, h0), from_local(d, h1)
        for f in W.FEEDERS:
            fid = f["id"]
            F = net["feeders"][fid]
            tr = W.year_value(f["tree"], d.year) if not isinstance(f["tree"], tuple) else f["tree"][0]
            for _ in range(int(rng.poisson(k * tr * F["main"] / 5.0))):
                t = int(rng.uniform(a, b))
                loc = dict(lateral=None, pos=float(rng.uniform(0.1, F["main"])), lpos=0.0, transformer=None,
                           phases_avail="ABC")
                faults.append(_fault(rng, t, fid, loc, "ice", rf=float(rng.uniform(0.5, 4)), kind="LL"))
    # vehicles into poles
    for k in range(int(rng.poisson(3.5))):
        t = int(rng.uniform(T0, T1))
        fid = W.FID[int(rng.integers(0, len(W.FID)))]
        loc = _random_location(rng, net, fid)
        loc["lateral"], loc["lpos"], loc["phases_avail"] = None, 0.0, "ABC"
        faults.append(_fault(rng, t, fid, loc, "vehicle", rf=float(rng.uniform(0.2, 1.5)), kind="LL"))
    faults += incipient(rng, net, wx, stk)
    faults += episodes(rng, net, wx, stk, trs_by_f)
    faults.sort(key=lambda f: f["t"])
    return faults


def _near_storm_days(stk):
    near = {}
    for (t, x, y, amp, kind) in stk:
        if kind == "CG":
            for sid, v in W.SUBS.items():
                if math.hypot(x - v[1], y - v[2]) <= 8.05:
                    near.setdefault(sid, set()).add(local_day(t))
    return near


def episodes(rng, net, wx, stk, trs_by_f):
    """The seasons each feeder is known for, at the counts the operations desk remembers them by: the squirrel
    year on North Yard 3 (the 2025 acorn mast), the overgrown taps of North Yard 2 that sag onto the line on wet
    mornings, Bluffview 3's long phase B taps through the oaks."""
    out = []
    near = _near_storm_days(stk)
    damp = damp_mornings(wx)
    gusty = {local_day(int(h)) for j, h in enumerate(wx["hours"]) if wx["gust"][j] >= 30}
    wet = {local_day(int(h)) for j, h in enumerate(wx["hours"]) if wx["precip"][j] > 0.02}
    for e in W.EPISODES:
        fid = e["feeder"]
        sub = net["feeders"][fid]["sub"]
        a, b = dt.date(e["year"], 8, 1), dt.date(e["year"], 10, 31)
        days_ = [a + dt.timedelta(days=k) for k in range((b - a).days + 1)]
        quiet = [d for d in days_ if d not in near.get(sub, set()) and d not in gusty and d not in MED_STORMS]
        if e["when"] == "damp":
            pool = [d for d in quiet if d in damp]
        else:
            pool = [d for d in quiet if d not in wet]
        picks = sorted(rng.choice(pool, size=e["n"], replace=len(pool) < e["n"]))
        for d in picks:
            if e["when"] == "damp":
                hs = damp[d]
                t = hs[int(rng.integers(0, len(hs)))] + int(rng.uniform(0, MS_H))
            else:
                m = int(rng.choice([rng.integers(420, 660), rng.integers(660, 1050)], p=[0.6, 0.4]))
                t = from_local(d, m // 60, m % 60, int(rng.integers(0, 60)))
            if e.get("phase"):
                taps = [l for l in net["feeders"][fid]["laterals"] if net["laterals"][l]["phase"] == e["phase"]]
                lat = taps[int(rng.integers(0, len(taps)))]
                L = net["laterals"][lat]
                loc = dict(lateral=lat, pos=L["tap"], lpos=float(rng.uniform(0.01, L["length"])), transformer=None,
                           phases_avail=L["phase"])
            elif e["cause"] == "animal":
                loc = _random_location(rng, net, fid, at_transformer=True, trs_by_f=trs_by_f)
            else:
                loc = _random_location(rng, net, fid)
            rf = float(rng.uniform(0.2, 2.0)) if e["cause"] == "animal" else float(rng.lognormal(math.log(6), 0.45))
            f = _fault(rng, t, fid, loc, e["cause"], rf=rf, kind="SLG")
            f["temporary"] = rng.random() < 0.86
            f["k_clear"] = 1 if rng.random() < 0.88 else 2
            out.append(f)
    return out


def _fault(rng, t, fid, loc, cause, rf, kind=None):
    ph = _phase_for(rng, loc["phases_avail"], kind or ("SLG" if rng.random() < 0.7 else "ANY"))
    tap = loc["lateral"] is not None or loc["transformer"] is not None
    temp = rng.random() < (TEMP_P_TAP if tap else TEMP_P)[cause]
    k_clear = int(rng.choice([1, 2, 3, 4], p=[0.78, 0.15, 0.05, 0.02]))
    return dict(t=int(t), feeder=fid, cause=cause, phases=ph, rf=rf, temporary=bool(temp), k_clear=k_clear, **loc)


def damp_mornings(wx):
    out = {}
    for j, h in enumerate(wx["hours"]):
        if wx["rh"][j] >= 97 and 4.5 <= wx["lh"][j] <= 8.5:
            d = local_day(int(h))
            out.setdefault(d, []).append(int(h))
    return out


def incipient(rng, net, wx, stk):
    """The failing components' flashovers: damp mornings, as the cracked insulator wets; late-summer damp mornings
    often turn to afternoon thunderstorms, so some of those days are storm days near the substation."""
    out = []
    damp = damp_mornings(wx)
    near = {}
    for (t, x, y, amp, kind) in stk:
        if kind == "CG":
            for sid, v in W.SUBS.items():
                if math.hypot(x - v[1], y - v[2]) <= 8.05:
                    near.setdefault(sid, set()).add(local_day(t))
    for spec in W.INCIPIENT:
        fid = spec["feeder"]
        pos = W.pole_to_miles(spec["pole"])
        stormy = near.get(net["feeders"][fid]["sub"], set())
        chosen = []
        for month, n in sorted(spec["months"].items()):
            cands = sorted(d for d in damp if d.year == 2026 and d.month == month and d >= spec["first"]
                           and d not in MED_STORMS)
            first = []
            if month == spec["first"].month:
                d0 = min(d for d in damp if d >= spec["first"] and d not in MED_STORMS)
                first = [d0]
                cands = [d for d in cands if d > d0 + dt.timedelta(days=3)]
            k = n - len(first)
            st = [d for d in cands if d in stormy]
            ns = [d for d in cands if d not in stormy]
            k_st = min(len(st), int(round(0.4 * n)) - (1 if first and first[0] in stormy else 0))
            k_st = max(0, k_st)
            pick = first + list(rng.choice(st, size=k_st, replace=False)) + \
                list(rng.choice(ns, size=k - k_st, replace=False))
            chosen += pick
        for d in sorted(chosen):
            hs = damp.get(d) or [from_local(d, 6)]
            h = hs[int(rng.integers(0, len(hs)))]
            t = h + int(rng.uniform(0, MS_H))
            lt = local_dt(t)
            if not (5.25 <= lt.hour + lt.minute / 60 <= 6.8):
                m = int(rng.integers(315, 408))
                t = from_local(d, m // 60, m % 60, int(rng.integers(0, 60)))
            out.append(dict(t=t, feeder=fid, cause="incipient", phases=spec["phase"],
                            rf=float(spec["rf"] + rng.normal(0, 0.03)), temporary=True, k_clear=1, lateral=None,
                            pos=pos, lpos=0.0, transformer=None, phases_avail="ABC", tag=fid))
    return out


# --------------------------------------------------------------------------- protection and restoration
class Grid:
    """Which parts of the network are without supply, and since when."""

    def __init__(self):
        self.out = {}          # device or transformer or service point -> (start, final restore, outage index)

    def dead(self, chain_devs, t):
        for dvc in chain_devs:
            o = self.out.get(dvc)
            if o and o[0] <= t < o[1]:
                return True
        return False


def load_current(rng, t, feeder_head=True):
    """Load on the phase at the time: a feeder head's two to four megawatts, a recloser's downstream share."""
    lt = local_dt(t)
    h = lt.hour + lt.minute / 60
    doy = lt.timetuple().tm_yday
    season = 1.0 + 0.07 * math.cos(2 * math.pi * (doy - 205) / 365) + 0.03 * math.cos(4 * math.pi * (doy - 15) / 365)
    prof = 0.66 + 0.34 * math.sin(math.pi * max(0.0, min(1.0, (h - 5.0) / 16.5)))
    base = (148 if feeder_head else 62) * season * prof
    return base * float(rng.uniform(0.95, 1.05)), math.radians(float(rng.uniform(36, 50)))


def recorded_currents(rng, I, phases, t, head=True):
    """Phase and residual currents an event report holds: the fault current with the load it rides on."""
    L, ang = load_current(rng, t, head)
    out = {}
    for p in "ABC":
        lp = L * float(rng.uniform(0.9, 1.1))
        if p in phases:
            v = complex(I * (1 + float(rng.normal(0, 0.0022))), 0) + lp * complex(math.cos(ang), math.sin(ang))
            out[p] = abs(v)
        else:
            out[p] = lp
    if len(phases) == 1:
        res = float(rng.uniform(4, 30))
        out["G"] = abs(complex(I * (1 + float(rng.normal(0, 0.0022))), 0) + res * complex(math.cos(ang * 2), 0.4))
    elif len(phases) == 2:
        out["G"] = float(rng.uniform(2, 18))
    else:
        out["G"] = float(rng.uniform(3, 25))
    return out


def restore_time(rng, t0, kind, storm, med):
    med_f = {None: 1.0, "squall": 4.0, "supercell": 4.5, "derecho": 9.0}[med]
    st = (3.2 if kind in ("FUSE", "TRANSFORMER") else 1.7) if storm else 1.0
    lt = local_dt(t0)
    night = 1.25 if (lt.hour < 6 or lt.hour >= 22) else 1.0
    base = {"FUSE": 92, "TRANSFORMER": 138, "SERVICE": 118, "S1": 68}[kind]
    v = float(rng.lognormal(math.log(base * st * night * med_f), 0.42))
    return t0 + max(22, int(round(v))) * MS_MIN


def minute_floor(t):
    return t - (t % MS_MIN)


def simulate(rng, net, wx, stk):
    faults = candidate_faults(rng, net, wx, stk) + everyday(rng, net)
    faults.sort(key=lambda f: f["t"])
    per_day = {}
    for (t, x, y, amp, kind) in stk:
        if kind == "CG":
            d = local_day(t)
            per_day[d] = per_day.get(d, 0) + 1
    storm_days = {d for d, n in per_day.items() if n >= 150} | set(ICE)
    grid = Grid()
    busy = {}         # device -> instant its last sequence finished
    ops = []          # device operation sequences
    outages = []      # sustained interruptions
    for fl in faults:
        t = fl["t"]
        d = local_day(t)
        if fl["cause"] in ("TRANSFORMER", "SERVICE", "PLANNED", "LATERAL"):
            o = _everyday_outage(rng, net, grid, fl, d, storm_days)
            if o:
                outages.append(o)
            continue
        fid = fl["feeder"]
        lat = fl["lateral"]
        # the feeder and devices the faulted point is on, on that date
        if lat is not None:
            fid = W.device_feeder(net, lat, d)
            zone = W.device_parent(net, lat, d)
            above = W.chain(net, lat, d)
        else:
            zone = W.zone_device(net, fid, W.pole_to_miles(W.miles_to_pole(fl["pos"])))
            above = W.chain(net, zone, d)
        chain_devs = ([fl["transformer"]] if fl["transformer"] else []) + above
        if grid.dead(chain_devs, t):
            continue
        if any(busy.get(dvc, -1) + 5000 > t for dvc in above):
            continue
        z1, z0 = W.z_at(net, fl["feeder"], fl["pos"], lat, fl["lpos"], d)
        I = W.fault_current(z1, z0, fl["phases"], fl["rf"])
        ztype = net["devices"][zone]["type"]
        pk_p, pk_g = W.PICKUP[ztype]
        pick = pk_g if len(fl["phases"]) == 1 else pk_p
        F = net["feeders"][fid]
        on_branch = lat is not None or fl["transformer"] is not None
        med = MED_STORMS.get(d)
        storm = d in storm_days
        fl.update(feeder_at=fid, zone=zone, current=I, day=d)
        if I < pick:
            if on_branch and I > 90:
                dev = fl["transformer"] or lat
                outages.append(_sustained(rng, grid, net, t + int(rng.uniform(3, 50)) * 1000, dev,
                                          "TRANSFORMER" if fl["transformer"] else "FUSE", fl, storm, med, d))
            continue
        fs = F["fuse_saving"]
        if on_branch and not fs:
            dev = fl["transformer"] or lat
            outages.append(_sustained(rng, grid, net, t + int(rng.uniform(80, 400)), dev,
                                      "TRANSFORMER" if fl["transformer"] else "FUSE", fl, storm, med, d))
            continue
        shots = W.SHOTS[ztype]
        seq = _trips(rng, t, ztype, 1 if on_branch else (fl["k_clear"] if fl["temporary"] else shots), shots)
        rec = [recorded_currents(rng, I, fl["phases"], tt, head=(ztype == "BREAKER")) for tt, _ in seq["trips"]]
        op = dict(device=zone, feeder=fid, day=d, t=seq["trips"][0][0], trips=seq["trips"], closes=seq["closes"],
                  lockout=seq["lockout"], phases=fl["phases"], rec=rec, cause=fl["cause"], fault=fl, I=I)
        ops.append(op)
        busy[zone] = seq["lockout"] or seq["closes"][-1]
        scada = ztype == "BREAKER" or net["devices"][zone].get("scada")
        if seq["lockout"] and fl["temporary"] and scada and not med:
            # the operations desk test-closes from SCADA; the fault has burned clear and the device holds. The
            # outage management system opens an incident only for an outage still on after fifteen minutes.
            short = rng.random() < 0.42
            gap = float(rng.uniform(2.2, 4.4)) if short else float(rng.uniform(5.7, 13.6))
            tc = seq["lockout"] + int(gap * MS_MIN)
            op["test_close"] = tc
            busy[zone] = tc
            if not short:
                t_open = seq["trips"][-1][0] + soe_open_lag(seq["trips"][-1][0])
                o = dict(start=t_open, restore=tc, device=zone, kind=ztype, steps=[], cause=fl["cause"],
                         day=d, nested_in=None, pattern="TC", no_ticket=True)
                grid.out[zone] = (o["start"], o["restore"], None)
                outages.append(o)
                op["outage_ref"] = o
        elif seq["lockout"]:
            o = _lockout(rng, grid, net, seq["lockout"], zone, fl, storm, med, d)
            outages.append(o)
            op["outage_ref"] = o
        elif on_branch and (not fl["temporary"] or fl["k_clear"] >= 2):
            dev = fl["transformer"] or lat
            tf = seq["closes"][0] + int(rng.uniform(60, 700))
            outages.append(_sustained(rng, grid, net, tf, dev, "TRANSFORMER" if fl["transformer"] else "FUSE",
                                      fl, storm, med, d))
            op["absorbed_ref"] = outages[-1]
    outages += continuations(rng, net, grid, outages)
    outages.sort(key=lambda o: o["start"])
    return dict(faults=faults, ops=ops, outages=outages, storm_days=storm_days)


STORM_CAUSES = ("tree", "wet_tree", "lightning", "storm_damage", "ice")


def continuations(rng, net, grid, outages):
    """After a storm outage is restored, a few customers whose service drops came down stay dark; the outage
    management system opens a service ticket for each when it finds them, at the minute the device closed."""
    import truth
    R = truth.Reach(net)
    out = []
    for o in outages:
        if o["kind"] not in ("FUSE", "BREAKER", "RECLOSER") or o["steps"] or o.get("no_ticket"):
            continue
        if o["cause"] not in STORM_CAUSES or o["day"] in MED_STORMS or rng.random() > 0.6:
            continue
        sps = R.sps(o["device"], o["day"])
        if not sps:
            continue
        for _ in range(int(rng.choice([1, 1, 1, 2, 3]))):
            sp = sps[int(rng.integers(0, len(sps)))]
            a = o["restore"]
            b = a + int(rng.uniform(40, 290)) * MS_MIN
            chain_devs = set([sp] + _above(net, sp, local_day(a)))
            if any(p is not o and p["device"] in chain_devs and p["start"] - 30 * MS_MIN < b
                   and a < p["restore"] + 30 * MS_MIN for p in outages + out):
                continue
            c = dict(start=a, restore=b, device=sp, kind="SERVICE", steps=[], cause=o["cause"], day=local_day(a),
                     nested_in=None, continues=o)
            grid.out[sp] = (a, b, None)
            out.append(c)
    return out


def soe_open_lag(t):
    """Milliseconds from a trip to the breaker status change the SCADA RTU stamps (contact travel and scan)."""
    return 28 + (t * 7919 + 13) % 34


def soe_close_lag(t):
    return 22 + (t * 104729 + 7) % 27


def _trips(rng, t, ztype, k, shots):
    """Trip and reclose instants of one sequence: k trips, locking out when k reaches the shots to lockout."""
    trips, closes = [], []
    tt = t + int(rng.uniform(40, 95))
    intervals = [500, 15000] if ztype == "BREAKER" else [2000, 2000, 10000]
    for i in range(k):
        trips.append((tt, i))
        if i + 1 >= shots:
            return dict(trips=trips, closes=closes, lockout=tt + 70)
        c = tt + intervals[min(i, len(intervals) - 1)] + int(rng.uniform(-40, 60))
        closes.append(c)
        if i + 1 < k:
            tt = c + int(rng.uniform(260, 1500))
    return dict(trips=trips, closes=closes, lockout=None)


def _sustained(rng, grid, net, t0, dev, kind, fl, storm, med, d):
    start = minute_floor(t0)
    rest = restore_time(rng, start, kind, storm, med)
    o = dict(start=start, restore=rest, device=dev, kind=kind, steps=[], cause=fl["cause"] if fl else "unknown",
             day=d, nested_in=None)
    grid.out[dev] = (start, rest, None)
    return o


def _lockout(rng, grid, net, t_lock, zone, fl, storm, med, d):
    start = minute_floor(t_lock)
    # inner outages already in progress below the device: they stay out until after the main line is back
    below = [k for k, v in grid.out.items() if v[0] <= start < v[1] and k != zone and
             zone in _above(net, k, d)]
    r = rng.random()
    stepped_p = 0.85 if fl["cause"] == "ice" else 0.42
    pattern = "S1" if (r > stepped_p or below) else ("S2" if r < 0.75 * stepped_p else "S3")
    med_f = {None: 1.0, "squall": 3.0, "supercell": 3.5, "derecho": 7.0}[med]
    if pattern == "S1":
        rest = restore_time(rng, start, "S1", storm, med)
        steps = []
    else:
        s1 = start + max(18, int(rng.lognormal(math.log(44 * med_f), 0.3))) * MS_MIN
        fin = start + max(150, int(rng.lognormal(math.log(310 * med_f), 0.35))) * MS_MIN
        lo = 0.78 if fl["cause"] == "ice" else 0.45
        steps = [(s1, float(rng.uniform(lo, 0.95)))]
        if pattern == "S3":
            s2 = s1 + max(15, int(rng.lognormal(math.log(38 * med_f), 0.3))) * MS_MIN
            steps.append((min(s2, fin - 20 * MS_MIN), float(rng.uniform(0.2, 0.6))))
        rest = fin
    o = dict(start=start, restore=rest, device=zone, kind=net["devices"][zone]["type"], steps=steps,
             cause=fl["cause"], day=d, nested_in=None, pattern=pattern)
    for k in below:
        s0, r0, _ = grid.out[k]
        if r0 <= rest:
            grid.out[k] = (s0, rest + int(rng.uniform(12, 70)) * MS_MIN, None)
    grid.out[zone] = (start, rest, None)
    return o


def _above(net, dev, d):
    if dev in net["transformers"]:
        T = net["transformers"][dev]
        return W.chain(net, T["device"], d)
    if dev in net["sps"]:
        T = net["transformers"][net["sps"][dev]["transformer"]]
        return W.chain(net, T["device"], d)
    return W.chain(net, dev, d)[1:]


def everyday(rng, net):
    """Transformer failures, service drops and planned work: the OMS's everyday tickets with no relay behind them,
    as candidate events in the same time line as the faults."""
    out = []
    trs = sorted(net["transformers"])
    sps = sorted(net["sps"])
    n_t = int(rng.poisson(0.011 * len(trs) * 1.83))
    n_s = int(rng.poisson(0.0155 * len(sps) * 1.83))
    n_p = int(rng.poisson(38))
    lats = []
    for f in W.FEEDERS:
        F = net["feeders"][f["id"]]
        for l in F["laterals"]:
            lats.append((l, (f["ug"] * 0.42 + F["lat_mi"] * 0.05) / len(F["laterals"])))
    pl = np.array([w for _, w in lats])
    n_u = int(rng.poisson(pl.sum() * 1.83))
    for _ in range(n_u):
        l = lats[int(rng.choice(len(lats), p=pl / pl.sum()))][0]
        out.append(dict(t=int(rng.uniform(T0 + MS_DAY, T1 - MS_DAY)), cause="LATERAL", device=l))
    for kind, n, pool in (("TRANSFORMER", n_t, trs), ("SERVICE", n_s, sps), ("PLANNED", n_p, trs)):
        for _ in range(n):
            dev = pool[int(rng.integers(0, len(pool)))]
            if kind == "PLANNED":
                d = W.DATA0 + dt.timedelta(days=int(rng.integers(0, (W.DATA1 - W.DATA0).days)))
                while d.weekday() >= 5:
                    d += dt.timedelta(days=1)
                t0 = from_local(d, int(rng.integers(8, 14)), int(rng.choice([0, 15, 30, 45])))
            else:
                t0 = int(rng.uniform(T0 + MS_DAY, T1 - MS_DAY))
            out.append(dict(t=int(t0), cause=kind, device=dev))
    return out


def _everyday_outage(rng, net, grid, ev, d, storm_days):
    dev, kind, t0 = ev["device"], ev["cause"], ev["t"]
    if dev in net["sps"]:
        sp = net["sps"][dev]
        if sp["connected"] > d or (sp["disconnected"] and sp["disconnected"] <= d):
            return None
    chain_devs = [dev] + _above(net, dev, d)
    if grid.dead(chain_devs, t0) or any(_overlaps(grid, c, t0) for c in chain_devs):
        return None
    st = minute_floor(t0)
    if kind == "PLANNED":
        rest = st + int(rng.choice([120, 150, 180, 210, 240, 270])) * MS_MIN + int(rng.integers(-9, 25)) * MS_MIN
        o = dict(start=st, restore=rest, device=dev, kind="TRANSFORMER", steps=[], cause="planned", day=d,
                 nested_in=None)
    elif kind == "LATERAL":
        o = dict(start=st, restore=restore_time(rng, st, "FUSE", d in storm_days, MED_STORMS.get(d)), device=dev,
                 kind="FUSE", steps=[], cause="equipment", day=d, nested_in=None)
    else:
        o = dict(start=st, restore=restore_time(rng, st, kind, d in storm_days, MED_STORMS.get(d)), device=dev,
                 kind=kind, steps=[], cause="equipment" if kind == "TRANSFORMER" else
                 str(rng.choice(["equipment", "equipment", "unknown", "public"])), day=d, nested_in=None)
    grid.out[dev] = (o["start"], o["restore"], None)
    return o


def _overlaps(grid, dev, t):
    o = grid.out.get(dev)
    return bool(o and o[0] - 30 * MS_MIN <= t < o[1] + 30 * MS_MIN)
