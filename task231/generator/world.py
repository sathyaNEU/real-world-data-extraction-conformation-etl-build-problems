"""task231 architecture 2: the world before any file is written. The air (free atmosphere, basin cold pools, each
station's own air), the sensors (with their winter faults), the vendor's QC, the telemetry (messages, dropouts,
backlogs, re-polls, modem swaps, planned outages), the pavement sensors, and the two distractor feeds. One RNG
stream per component, so a change in one never reshuffles another."""
import datetime as dt
import math

import numpy as np

import params as P


def rng(k):
    return np.random.default_rng([P.SEED, k])


def local_of(u):
    if u < P.DST_OFF_UTC:
        return u - dt.timedelta(hours=6), "MDT"
    if u < P.DST_ON_UTC:
        return u - dt.timedelta(hours=7), "MST"
    return u - dt.timedelta(hours=6), "MDT"


def build():
    W = {}
    NS, NH = len(P.TAGS), P.NH
    # hour h covers [utc[h], utc[h] + 1h); the feed stamps an observation at the hour's end
    utc = [P.WIN_START_UTC + dt.timedelta(hours=h) for h in range(NH)]
    loc = [local_of(u)[0] for u in utc]
    lhour = np.array([l.hour for l in loc])
    lday = np.array([(l.date() - dt.date(2026, 10, 1)).days for l in loc])
    month = np.array([l.month for l in loc])
    ND = int(lday.max()) + 2
    W.update(utc=utc, loc=loc, lhour=lhour, lday=lday, month=month, ND=ND)

    X = np.array([s[6] for s in P.STATIONS]); Y = np.array([s[7] for s in P.STATIONS])
    Z = np.array([s[8] for s in P.STATIONS], float)
    D = np.sqrt((X[:, None] - X[None, :]) ** 2 + (Y[:, None] - Y[None, :]) ** 2)
    grp = [P.GROUP[t] for t in P.TAGS]
    W.update(X=X, Y=Y, Z=Z, D=D, grp=grp)

    # ---- regime by local day: a still clear night or a mixed one; long still spells in midwinter ----
    r = rng(1)
    still = np.zeros(ND, bool)
    s = False
    for d in range(ND):
        date = dt.date(2026, 10, 1) + dt.timedelta(days=d)
        winter = date.month in (12, 1)
        s = (r.random() < (0.80 if winter else 0.62)) if s else (r.random() < (0.30 if winter else 0.28))
        still[d] = s
    persist = np.zeros(ND, bool)
    for d in range(2, ND):
        date = dt.date(2026, 10, 1) + dt.timedelta(days=d)
        persist[d] = date.month in (12, 1, 2) and still[d] and still[d - 1] and still[d - 2]
    W.update(still=still, persist=persist)

    # ---- free atmosphere at 1,500 m ----
    r = rng(2)
    doy = np.array([(l - dt.datetime(2026, 10, 1)).total_seconds() / 86400 for l in loc])
    season = np.minimum(-6.0 + 13.0 * ((doy - 107.0) / 107.0) ** 2, 8.5)
    syn = np.zeros(NH)
    a = math.exp(-1 / 60.0)
    e = r.normal(0, 4.5, NH)
    for h in range(1, NH):
        syn[h] = a * syn[h - 1] + math.sqrt(1 - a * a) * e[h]
    for _ in range(5):
        c = int(r.integers(900, 4300)); w = int(r.integers(30, 70))
        syn[c:c + w] -= np.linspace(0, 12, w) * np.exp(-np.linspace(0, 2, w)) + 4
    diur = np.cos(2 * math.pi * (lhour - 15) / 24.0)
    amp = np.where(still[lday], 5.0, 1.8)
    Tref = season + syn + amp * diur
    W["Tref"] = Tref

    # ---- basin pools: the deficit at each basin floor, hour by hour ----
    r = rng(3)
    nights = {b: r.random(ND) for b in P.BASIN}
    scale = {b: r.uniform(0.80, 1.15, ND) for b in P.BASIN}
    night_of = np.where(lhour >= 17, lday, lday - 1)
    hours_in = np.where(lhour >= 17, lhour - 17, lhour + 7)
    in_night = (lhour >= 17) | (lhour < 9)
    deficit = {}
    for b, (dmax, depth, share, pers) in P.BASIN.items():
        ok = (night_of >= 0) & in_night & still[np.clip(night_of, 0, ND - 1)] & \
            (nights[b][np.clip(night_of, 0, ND - 1)] <= share)
        df = np.where(ok, dmax * scale[b][np.clip(night_of, 0, ND - 1)] * (1 - np.exp(-hours_in / 4.0)), 0.0)
        df = np.where(ok & (lhour == 8), df * 0.55, df)
        if pers:
            day = (lhour >= 9) & (lhour < 17) & persist[lday]
            df = np.where(day, dmax * scale[b][lday] * 0.72, df)
        deficit[b] = df
    floor = {b: min(P.ELEV[t] for t in P.TAGS if P.GROUP[t] == b) for b in P.BASIN}
    W.update(deficit=deficit, floor=floor)

    # ---- each station's air ----
    r = np.random.default_rng([P.SEED, 4, P.NOISE_KEY])
    offset = r.normal(0, 0.20, NS)
    T = np.zeros((NS, NH))
    for i, t in enumerate(P.TAGS):
        n = np.zeros(NH)
        ee = r.normal(0, 0.11, NH)
        for h in range(1, NH):
            n[h] = 0.85 * n[h - 1] + ee[h]
        air = Tref - P.SPATIAL_LAPSE_C_PER_KM * (Z[i] - 1500) / 1000.0 + offset[i] + n
        g = grp[i]
        b = g[0] if g[0] in P.BASIN and g not in ("G",) else None
        if b is not None and (g == b or g == b + "slope"):
            dmax, depth, share, pers = P.BASIN[b]
            fr = (Z[i] - floor[b]) / depth
            if fr < 1.0:
                f = 1.0 if fr <= 0.6 else (1 - fr) / 0.4
                air = air - deficit[b] * f
        T[i] = air
    W["T"] = T

    # ---- the sensors: noise, then the winter's faults ----
    r = rng(5)
    # a sound probe reads within its stated accuracy: the error is bounded at 0.2 C before the 0.1 C display step
    read = np.round(T + np.clip(r.normal(0, 0.07, (NS, NH)), -0.2, 0.2), 1)
    right = np.ones((NS, NH), bool)
    fault = np.full((NS, NH), "", dtype=object)
    for t in P.ICING_PASSES:
        i = P.TAGS.index(t)
        for _ in range(14):
            c = int(r.integers(700, 4200)); w = int(r.integers(10, 34))
            sl = slice(c, c + w)
            cold = T[i, sl] < -6.0
            v = np.round(r.normal(-0.4, 0.15, w), 1)
            read[i, sl] = np.where(cold, v, read[i, sl])
            right[i, sl] = np.where(cold, False, right[i, sl])
            fault[i, sl] = np.where(cold, "rime", fault[i, sl])
    # a wetted probe filter after the spring storms: on dry windy afternoons the probe reads toward the wet bulb
    i = P.TAGS.index(P.WET_FILTER)
    for d in [d for d in range(ND - 1) if (dt.date(2026, 10, 1) + dt.timedelta(days=d)).month in (3, 4)
              and not still[d] and r.random() < 0.42]:
        for h in np.where((lday == d) & (lhour >= 12) & (lhour < 18))[0]:
            read[i, h] = np.round(T[i, h] - r.uniform(5.5, 9.0), 1)
            right[i, h] = False
            fault[i, h] = "wet filter"
    t, h0 = P.CONNECTOR
    i = P.TAGS.index(t)
    for h in range(h0, NH):
        if r.random() < 0.10:
            read[i, h] = np.round(read[i, h] + r.choice([-1, 1]) * r.uniform(6, 14), 1)
            right[i, h] = False
            fault[i, h] = "connector"
    t, h0 = P.SHIELD
    i = P.TAGS.index(t)
    for h in range(h0, NH):
        if 10 <= lhour[h] < 16 and still[lday[h]]:
            read[i, h] = np.round(read[i, h] + r.uniform(5.5, 9.0), 1)
            right[i, h] = False
            fault[i, h] = "shield"
    # the standard's "right": within the sensor's stated accuracy of the air at the station
    assert ((np.abs(read - T) <= P.SENSOR_ACCURACY_C + 1e-9) == right).all()
    W.update(read=read, right=right, fault=fault)

    # ---- the other channels ----
    r = rng(6)
    still_h = still[np.clip(night_of, 0, ND - 1)] & in_night
    dep = np.where(still_h[None, :], r.uniform(0.3, 2.2, (NS, NH)), r.uniform(1.5, 9.0, (NS, NH)))
    dew = np.round(T - dep, 1)
    rh = np.clip(np.round(100 * np.exp(17.62 * dew / (243.12 + dew)) / np.exp(17.62 * T / (243.12 + T))), 8, 100)
    wind = np.where(still_h[None, :], r.gamma(1.6, 0.45, (NS, NH)), r.gamma(2.4, 1.9, (NS, NH)))
    for i, g in enumerate(grp):
        if g in ("G", "R"):
            wind[i] *= 1.8
    wdir = r.integers(0, 360, (NS, NH))
    W.update(dew=dew, rh=rh, wind=np.round(wind, 1), wdir=wdir)

    # ---- telemetry: planned outages, dropouts, messages; what the feed receives ----
    r = rng(7)
    outage = np.zeros((NS, NH), bool)
    notices = []
    # planned work is booked at the mountain sites: towers, power lines and RPUs on the passes, grades and gaps
    out_sites = [t for t in P.TAGS if P.GROUP[t] not in P.BASIN]
    for k in range(13):
        i = P.TAGS.index(out_sites[int(r.integers(0, len(out_sites)))])
        start = int(r.integers(300, NH - 300))
        length = int(r.integers(3, 30))
        outage[i, start:start + length] = True
        notices.append((P.TAGS[i], start, start + length, ["power line work", "tower and mast inspection",
                                                           "RPU firmware upgrade", "road widening",
                                                           "utility pole replacement"][int(r.integers(0, 5))]))
    W["outage"], W["notices"] = outage, sorted(notices, key=lambda x: (x[1], x[0]))
    cover = {t: v for t, v in zip(P.TAGS, r.uniform(0.002, 0.016, NS))}
    # dropout episodes in minutes from the window's start
    episodes = {}
    total_min = (NH + 200) * 60
    for i, t in enumerate(P.TAGS):
        eps = []
        m = 0.0
        while m < total_min:
            m += r.exponential(60.0 / cover[t])
            if r.random() < 0.012:
                dur = r.uniform(40, 90) * 60
            else:
                dur = r.exponential(95.0) + 10.0
            eps.append((m, m + dur))
            m += dur
        episodes[t] = eps
    W["episodes"] = episodes
    starts = {t: [a0 for a0, _ in episodes[t]] for t in P.TAGS}
    import bisect

    def up(t, minute):
        k = bisect.bisect_right(starts[t], minute) - 1
        return k < 0 or not (episodes[t][k][0] <= minute < episodes[t][k][1])

    msgs = []          # (tag, received_utc, kind, first_obs_h, last_obs_h)
    received = np.full((NS, NH), None, dtype=object)
    deliveries = np.zeros((NS, NH), int)
    for i, t in enumerate(P.TAGS):
        queue = []
        for h in range(NH):
            if outage[i, h]:
                continue
            queue.append(h)
            queue = [q for q in queue if h - q < 96]
            end_min = (h + 1) * 60.0
            if up(t, end_min + 5):
                slow = r.random() < 0.009
                lat = r.uniform(15.5, 48.0) if slow else r.uniform(3.5, 8.5)
                rec_min = end_min + 5 + lat
                if slow and rec_min > end_min + 35 and up(t, end_min + 35):
                    # the scheduled message is still missing 35 minutes after the hour: the server re-polls
                    rp = end_min + 35 + r.uniform(0.6, 2.4)
                    msgs.append((t, rp, "REPOLL", h, h, (h,)))
                    received[i, h] = rp
                    deliveries[i, h] += 1
                kind = "SCHED" if queue == [h] else "BACKLOG"
                msgs.append((t, rec_min, kind, queue[0], queue[-1], tuple(queue)))
                for q in queue:
                    if received[i, q] is None or rec_min < received[i, q]:
                        received[i, q] = rec_min
                    deliveries[i, q] += 1
                queue = []
            elif up(t, end_min + 35):
                rp = end_min + 35 + r.uniform(0.6, 2.4)
                msgs.append((t, rp, "REPOLL", h, h, (h,)))
                received[i, h] = rp
                deliveries[i, h] += 1
                queue = [q for q in queue if q != h]
    msgs.sort(key=lambda m: (m[1], m[0]))
    W["msgs"], W["received"], W["deliveries"] = msgs, received, deliveries

    # ---- modems: one per station, five swapped mid-winter ----
    r = rng(8)
    imei = {}
    swaps = {}
    for t in P.TAGS:
        imei[t] = "35" + "".join(str(int(x)) for x in r.integers(0, 10, 13))
    for t in ("K1", "M2", "R4", "Q3", "T2"):
        swaps[t] = (int(r.integers(900, 4200)), "35" + "".join(str(int(x)) for x in r.integers(0, 10, 13)))
    # four of those modems failed some days before their replacements came, and one of the district's two shop spares
    # carried the site meanwhile (the shop spare to Sheep Ridge and Ransom Creek, the Ashby yard spare to Fenwick and
    # Antelope Bench); the register keeps each spare's own row, with no site
    W["spare"] = {}
    for spare, sites in (("359441205583076", ("R4", "M2")), ("358713046622913", ("Q3", "T2"))):
        busy = []
        for t in sites:
            h_new, new = swaps[t]
            a = h_new - int(r.integers(70, 130))
            while any(not (h_new <= b0 or a >= b1) for b0, b1 in busy):
                h_new += 260
                a += 260
            swaps[t] = (h_new, new)
            busy.append((a, h_new))
            W["spare"][t] = (a, h_new, spare)
    W["imei"], W["swaps"] = imei, swaps

    # ---- the vendor's tests: the QC run at 20 minutes past each hour checks every reading received since the last
    # run, against the neighbours' readings for the same hour that the server held at that run ----
    have = np.array([[x is not None for x in row] for row in received])
    W["have"] = have
    rec = np.where(have, np.array([[x if x is not None else np.inf for x in row] for row in received], float), np.inf)
    run = np.where(have, np.ceil((rec - 20.0) / 60.0) * 60.0 + 20.0, np.inf)
    W["qc_run"] = run
    wts = np.where((D > 0) & (D <= P.SPATIAL_RADIUS_KM), 1.0 / np.maximum(D, 1.0) ** 2, 0.0)
    spatial = np.zeros((NS, NH), bool)
    est_all = np.full((NS, NH), np.nan)
    for h in range(NH):
        v = read[:, h]
        for i in range(NS):
            if not have[i, h]:
                continue
            okv = rec[:, h] <= run[i, h]
            w = wts[i] * okv
            if (w > 0).sum() < P.SPATIAL_MIN_NEIGHBOURS:
                continue
            est = (w * (v + P.SPATIAL_LAPSE_C_PER_KM * (Z - Z[i]) / 1000.0)).sum() / w.sum()
            est_all[i, h] = est
            if abs(v[i] - est) > P.SPATIAL_TOL_C:
                spatial[i, h] = True
    W.update(spatial=spatial, est=est_all)

    # ---- pavement: each station's travel-lane sensor (and a bridge deck sensor at some) ----
    r = rng(9)
    precip = np.zeros(NH, bool)
    for h in range(NH):
        if not still[lday[h]] and r.random() < 0.16:
            precip[h:h + int(r.integers(1, 6))] = True
    W["precip"] = precip
    surf = {}
    status = {}
    for i, t in enumerate(P.TAGS):
        sun = np.where((lhour >= 10) & (lhour < 16), r.uniform(1.0, 6.0, NH), 0.0)
        rad = np.where(still_h, -r.uniform(0.5, 2.8, NH), -r.uniform(0.0, 0.8, NH))
        s_lane = T[i] + sun + rad + r.normal(0, 0.4, NH)
        lanes = {"travel lane": s_lane}
        if P.STATIONS[i][12]:
            lanes["bridge deck"] = s_lane - np.where(in_night, r.uniform(0.8, 2.4, NH), r.uniform(0.0, 0.8, NH))
        for lane, sv in lanes.items():
            st = np.full(NH, "dry", dtype=object)
            wet_until = -100
            for h in range(NH):
                if precip[h]:
                    wet_until = h + 6
                    if sv[h] <= 0.0:
                        st[h] = "snow" if T[i, h] < -2.0 else "ice warning"
                    else:
                        st[h] = "wet"
                elif h <= wet_until:
                    st[h] = "ice watch" if sv[h] <= 0.0 else "moist"
                elif still_h[h] and sv[h] <= 0.0 and sv[h] <= dew[i, h] + 0.4:
                    st[h] = "frost"
                elif sv[h] > 0.0 and r.random() < 0.015:
                    st[h] = "chemically wet"
            surf[(t, lane)] = np.round(sv, 1)
            status[(t, lane)] = st
    W["surf"], W["status"] = surf, status

    # pavement sensors: serials, models, firmware dates, replacements
    r = rng(10)
    sensors = []     # (tag, lane, serial, model, from_h, to_h, port)
    fw_change = {}   # serial -> hour index the firmware went to 4.1 (IRS-31 only)
    repl = {"K3": (2610, "IRS-31"), "N2": (3070, "IRS-31"), "P3": (1700, "SCAN-16"), "Q1": (3670, "IRS-31")}
    for i, t in enumerate(P.TAGS):
        model = P.STATIONS[i][11]
        lanes = ["travel lane"] + (["bridge deck"] if P.STATIONS[i][12] else [])
        for k, lane in enumerate(lanes):
            port = 1 + k
            ser = ("IR" if model == "IRS-31" else "SC") + str(int(r.integers(20000, 99999)))
            if lane == "travel lane" and t in repl:
                h_r, new_model = repl[t]
                sensors.append((t, lane, ser, model, 0, h_r, port))
                ser2 = ("IR" if new_model == "IRS-31" else "SC") + str(int(r.integers(20000, 99999)))
                sensors.append((t, lane, ser2, new_model, h_r, NH, port))
                if new_model == "IRS-31":
                    fw_change[ser2] = h_r      # a new IRS-31 ships with firmware 4.1
                if model == "IRS-31":
                    int(r.integers(1600, 3400))  # the failing head was left on 3.4 until it came out
            else:
                bmodel = model if lane == "travel lane" else "IRS-31"
                if lane != "travel lane":
                    ser = "IR" + str(int(r.integers(20000, 99999)))
                sensors.append((t, lane, ser, bmodel, 0, NH, port))
                if bmodel == "IRS-31":
                    fw_change[ser] = int(r.integers(1600, 3400))
    W["sensors"], W["fw_change"] = sensors, fw_change

    # ---- distractors: model point forecasts (3-hourly) and daily traffic at the counters ----
    r = rng(11)
    nwp = np.zeros((NS, NH))
    for i in range(NS):
        free = Tref - P.SPATIAL_LAPSE_C_PER_KM * (Z[i] - 1500) / 1000.0
        nwp[i] = free + 0.3 * (T[i] - free) + r.normal(0, 1.3, NH)
    W["nwp"] = np.round(nwp, 1)
    r = rng(12)
    atr = []
    for k, (route, mp) in enumerate([("MT 271", 18.0), ("US 487", 64.5), ("US 487", 118.2), ("MT 309", 36.0),
                                     ("MT 52", 9.8), ("US 33", 131.7), ("US 33", 160.4), ("MT 52", 45.0)]):
        base = r.uniform(900, 7800)
        for d in range(365):
            day = dt.date(2026, 1, 1) + dt.timedelta(days=d)
            seas = 1.0 + 0.32 * math.cos(2 * math.pi * (d - 200) / 365.0)
            wk = 1.12 if day.weekday() in (4, 6) else (0.86 if day.weekday() == 1 else 1.0)
            atr.append(("ATR-%03d" % (101 + 7 * k), route, mp, day, int(round(base * seas * wk * r.uniform(0.9, 1.1)))))
    W["atr"] = atr

    # ---- the October 2026 pre-season checks: every air sensor against the reference thermometer ----
    r = rng(13)
    pre = []
    for i, t in enumerate(P.TAGS):
        day = dt.date(2026, 9, 21) + dt.timedelta(days=int(r.integers(0, 10)))
        ref = round(float(r.uniform(4.0, 16.0)), 2)
        pre.append((t, day, ref, round(ref + float(r.normal(0, 0.09)), 2)))
    W["preseason"] = pre
    return W
