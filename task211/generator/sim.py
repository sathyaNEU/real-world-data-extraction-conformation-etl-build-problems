"""The clean truth: Q3 2026 at ten-minute resolution for the network, before any export, unit or clock mess.

Natural dose rate = terrestrial and cosmic background (attenuated a little while the soil is wet) plus the
radon-progeny excess rain washes down, carried exactly through the lead-214 -> bismuth-214 chain. Artificial
dose rate = weld radiography trains near two lowland stations and the network's own source checks. Every
stream has its own seeded generator, so a rebuild is byte-identical."""
import datetime as dt
import math
import zlib

import numpy as np

import world as W

DT = 10.0
LPB = math.log(2) / W.T_PB214_MIN
LBI = math.log(2) / W.T_BI214_MIN
E1, E2 = math.exp(-LPB * DT), math.exp(-LBI * DT)
KBI = LBI / (LBI - LPB) * (E1 - E2)
C_PB, C_BI = 0.30, 0.70          # dose per unit activity, lead-214 and bismuth-214 (relative)
K_WASH = 12.0


def rng(name):
    return np.random.default_rng([W.SEED, zlib.crc32(name.encode())])


def t_index(when_utc):
    return int((when_utc - W.Q_START).total_seconds() // 600)


def when(t):
    return W.Q_START + dt.timedelta(minutes=10 * int(t))


def station_frame():
    r = rng("stations")
    rows = []
    for code, name, kind, e, n, alt, cty in W.STATIONS:
        if kind == "upland":
            bg, exh = r.normal(112, 6), r.uniform(1.75, 2.10)
        elif kind == "coastal":
            bg, exh = r.normal(68, 3.5), r.uniform(0.80, 0.95)
        else:
            bg, exh = r.normal(79, 4.5), r.uniform(0.90, 1.10)
        rows.append(dict(code=code, name=name, kind=kind, e=e, n=n, alt=alt, county=cty,
                         x=(e - 395000) / 1000.0, y=(n - 450000) / 1000.0, bg=float(bg), exh=float(exh)))
    return rows


def rain_fields(S):
    """Rain intensity (mm/h) in each ten-minute interval at every station and gauge."""
    n = W.N10
    pts = [(s["x"], s["y"]) for s in S] + [((e - 395000) / 1000.0, (nn - 450000) / 1000.0) for _, _, e, nn in W.GAUGES]
    P = len(pts)
    R = np.zeros((P, n))
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    upl = [i for i, s in enumerate(S) if s["kind"] == "upland"]
    # fronts: regional, moving west to east
    r = rng("fronts")
    k = int(r.uniform(10, 120))
    fronts = []
    while k < n - 80:
        dur = int(r.uniform(18, 54)); peak = r.uniform(0.8, 3.4); v = r.uniform(25, 45)
        phase = r.uniform(0, 2 * math.pi)
        fronts.append((k, dur))
        for i in range(P):
            off = int(round((xs[i] - 0.0) / v * 6))
            mod = 0.75 + 0.5 * (0.5 + 0.5 * math.sin(phase + 0.09 * xs[i] + 0.07 * ys[i]))
            st = k + off
            for j in range(dur):
                if 0 <= st + j < n:
                    R[i, st + j] += peak * mod * math.sin(math.pi * (j + 0.5) / dur) ** 0.8
        k += int(r.exponential(3.4 * 144)) + 60
    # inland afternoon convection, a third triggered over the moor
    r = rng("convection")
    for _ in range(640):
        day = int(r.integers(0, W.DAYS)); hl = r.normal(15.5, 2.4)
        k0 = int(day * 144 + (hl - 1.0) * 6)
        if r.random() < 0.36:
            u = upl[int(r.integers(0, len(upl)))]
            cx, cy = S[u]["x"] + r.normal(0, 2.5), S[u]["y"] + r.normal(0, 2.5)
        else:
            cx, cy = r.uniform(18, 72), r.uniform(2, 56)
        rad = r.uniform(3.0, 6.0); dur = int(r.uniform(3, 10)); inten = r.uniform(2, 11)
        d = np.hypot(xs - cx, ys - cy)
        for i in np.where(d < rad)[0]:
            for j in range(dur):
                if 0 <= k0 + j < n:
                    R[i, k0 + j] += inten * (1 - d[i] / rad) * math.sin(math.pi * (j + 0.5) / dur)
    # summer storm nights: thunderstorm cells over the vale and the moor in the small hours
    r = rng("storms")
    storm_days = sorted(r.choice(np.arange(4, W.DAYS - 2), 9, replace=False))
    for day in storm_days:
        for _ in range(int(r.integers(14, 25))):
            hu = r.uniform(-2.5, 4.5)                     # UTC hours around midnight
            k0 = int(day * 144 + hu * 6)
            cx, cy = r.uniform(14, 72), r.uniform(2, 56)
            rad = r.uniform(3.0, 6.5); dur = int(r.uniform(2, 7)); inten = r.uniform(5, 24)
            d = np.hypot(xs - cx, ys - cy)
            for i in np.where(d < rad)[0]:
                for j in range(dur):
                    if 0 <= k0 + j < n:
                        R[i, k0 + j] += inten * (1 - d[i] / rad) * math.sin(math.pi * (j + 0.5) / dur)
    # coastal night showers on the land breeze
    r = rng("coastal")
    for _ in range(470):
        day = int(r.integers(0, W.DAYS)); hl = r.normal(3.0, 2.3) % 24
        k0 = int(day * 144 + ((hl - 1.0) % 24) * 6)
        cx, cy = r.uniform(-4, 17), r.uniform(0, 52)
        rad = r.uniform(3.0, 6.0); dur = int(r.uniform(3, 9)); inten = r.uniform(2, 8)
        d = np.hypot(xs - cx, ys - cy)
        for i in np.where(d < rad)[0]:
            for j in range(dur):
                if 0 <= k0 + j < n:
                    R[i, k0 + j] += inten * (1 - d[i] / rad) * math.sin(math.pi * (j + 0.5) / dur)
    return R[:len(S)], R[len(S):], fronts


def radon_series():
    r = rng("radon")
    daily = np.exp(r.normal(0, 0.30, W.DAYS))
    t = np.arange(W.N10)
    h = (t % 144) / 6.0
    return np.repeat(daily, 144) * (1 + 0.7 * np.cos(2 * math.pi * (h - 4.0) / 24))


def natural(S, rain, radon):
    n = W.N10
    out = np.zeros((len(S), n)); wash = np.zeros((len(S), n))
    for i, s in enumerate(S):
        apb = abi = soil = 0.0
        for j in range(n):
            apb, abi = apb * E1, abi * E2 + apb * KBI
            rr = rain[i, j]
            if rr > 0:
                dep = K_WASH * s["exh"] * radon[j] * min(rr, 8.0) ** 0.8 * (DT / 60.0)
                a = dep / (C_PB + C_BI)
                apb += a; abi += a
                soil += 0.022 * rr * DT / 60.0
            soil *= math.exp(-DT / (60 * 72))
            w = C_PB * apb + C_BI * abi
            wash[i, j] = w
            out[i, j] = s["bg"] * (1 - min(soil, 0.06)) + w
    return out, wash


def nearest_gauge(s):
    best, bi = 1e9, 0
    for k, (_, _, e, nn) in enumerate(W.GAUGES):
        d = math.hypot((e - 395000) / 1000.0 - s["x"], (nn - 450000) / 1000.0 - s["y"])
        if d < best:
            best, bi = d, k
    return bi


def radiography(S, rain_st, rain_g, wash):
    """Night radiography at a pipeline contractor's double-jointing yards: trains of exposures inside one UTC
    date, which is also one BST date. The yards work through rain; about four nights in ten at each yard are
    evenings with rain at the network's nearest gauge, and a small-hours session never follows washout carried
    over midnight."""
    idx = {s["code"]: i for i, s in enumerate(S)}
    art = np.zeros((len(S), W.N10)); sessions = []
    for code, (d0, d1) in W.RADIOGRAPHY.items():
        r = rng("radiography/" + code)
        i = idx[code]
        g = nearest_gauge(S[i])
        days = [(d0 + dt.timedelta(days=k)) for k in range((d1 - d0).days + 1)]
        plan = {}
        for day in days:                      # each night's session as the yard would run it
            day_i = (day - W.Q_START.date()).days
            if r.random() < 0.55:
                start = day_i * 144 + int(r.uniform(19.0, 20.4) * 6); length = int(r.uniform(7, 10))
            else:
                start = day_i * 144 + int(r.uniform(0.5, 2.3) * 6); length = int(r.uniform(7, 15))
            plan[day] = (start, length, float(r.uniform(62, 100)), int(r.integers(0, 2 ** 31)))

        def gauge_wet(start, length):
            h0, h1 = start // 6, (start + length) // 6 + 1
            hourly = rain_g[g, h0 * 6:h1 * 6].reshape(-1, 6).mean(axis=1)
            return hourly.max() > 0.35

        for day in days:                      # on an evening the gauge records rain, the session starts in it
            day_i = (day - W.Q_START.date()).days
            hours = [h for h in (18, 19, 20) if rain_g[g, day_i * 144 + h * 6:day_i * 144 + h * 6 + 6].mean() > 0.45]
            if hours:
                st = day_i * 144 + max(114, min(122, hours[0] * 6 + int(r.integers(0, 4))))
                plan[day] = (st, int(r.uniform(7, 10)), plan[day][2], plan[day][3])

        def quiet(start, length):
            a = start - 18
            return wash[i, a:start].max() < 4.0 and rain_st[i, a:start + length + 6].max() < 0.2 and \
                (start % 144) >= 3 and (start + length + 3) % 144 > (start % 144)

        wet = [d for d in days if gauge_wet(plan[d][0], plan[d][1]) and (plan[d][0] % 144) >= 19 * 6]
        dry = [d for d in days if not gauge_wet(plan[d][0], plan[d][1]) and quiet(plan[d][0], plan[d][1])]
        r.shuffle(wet); r.shuffle(dry)
        picks = sorted(wet[:5] + dry[:3])
        for day in picks:
            start, length, lvl, sd = plan[day]
            rr = np.random.default_rng(sd)
            for j in range(length):
                if j == 0:
                    duty = rr.uniform(0.25, 0.65)
                elif j == length - 1:
                    duty = rr.uniform(0.75, 0.97)      # the last exposure runs to within a minute or two of the interval's end
                else:
                    duty = rr.uniform(0.6, 1.0)
                art[i, start + j] += lvl * duty
            sessions.append(dict(code=code, start=start, end=start + length, date=day, level=lvl,
                                 gauge_wet=day in wet[:5]))
    return art, sessions


def visits(S):
    """One quarterly visit per station: a source check (and the probe exchange at its station)."""
    r = rng("visits")
    out = []
    weekdays = [W.Q_START.date() + dt.timedelta(days=k) for k in range(W.DAYS)
                if (W.Q_START.date() + dt.timedelta(days=k)).weekday() < 5]
    order = list(range(len(S)))
    r.shuffle(order)
    used = set()
    for pos, i in enumerate(order):
        s = S[i]
        eng = "eng_b" if s["county"] == 1 and s["kind"] == "lowland" and pos % 3 != 0 else "eng_a"
        while True:
            d = weekdays[int(r.integers(2, len(weekdays) - 3))]
            if (d, eng) not in used:
                used.add((d, eng)); break
        local = dt.datetime.combine(d, dt.time(9, 0)) + dt.timedelta(minutes=int(r.uniform(0, 390)))
        if s["code"] == W.PROBE_EXCHANGE[0]:
            eng = "eng_a"; local = W.PROBE_EXCHANGE[1] + dt.timedelta(minutes=40)
        out.append(dict(code=s["code"], eng=eng, local=local))
    return out


def response_factors(S):
    r = rng("response")
    f = {s["code"]: float(r.uniform(0.955, 1.045)) for s in S}
    f["MV243"] = 0.874        # a probe reading low: fails its check
    f["MV184"] = 1.118        # a probe reading high: fails its check
    return f


def power_cuts(S):
    r = rng("power")
    cuts = {}
    for s in S:
        k = int(r.choice([0, 0, 1, 1, 2]))
        lst = []
        for _ in range(k):
            st = int(r.integers(200, W.N10 - 200)); ln = int(r.uniform(6, 48))
            lst.append((st, st + ln))
        cuts[s["code"]] = lst
    cuts["MV142"] = cuts["MV142"] + [(t_index(dt.datetime(2026, 7, 28, 13, 0)), t_index(dt.datetime(2026, 7, 29, 4, 30)))]
    cuts["MV327"] = cuts["MV327"] + [(t_index(dt.datetime(2026, 8, 6, 2, 0)), t_index(dt.datetime(2026, 8, 6, 23, 0)))]
    return cuts


def source_true(serial, jig, day):
    """What a check source truly gives in a jig on a day. The 2026 recertification of CS-0583 found its 2020
    certificate 2.4 per cent low; every other certificate is accurate."""
    certs = W.SOURCES[serial]
    no, ref, issued, vals = certs[-1]
    y = (day - ref).days / 365.25
    return vals[jig] * 2 ** (-y / W.CS137_HALF_LIFE_Y)


def cert_in_force(serial, day):
    """The certificate a check on `day` is read against: the latest issued on or before that day."""
    ok = [c for c in W.SOURCES[serial] if c[2] <= day]
    return ok[-1]


def expected(serial, jig, day):
    no, ref, issued, vals = cert_in_force(serial, day)
    y = (day - ref).days / 365.25
    return vals[jig] * 2 ** (-y / W.CS137_HALF_LIFE_Y), no


def clear_reading(bg, reading, exp):
    """The engineer's reading to the whole nSv/h, kept clear of a rounding line of the per cent of expected (and of
    the 90 and 110 per cent pass lines) by at most two nSv/h of the counting noise."""
    for adj in (0, 1, -1, 2, -2):
        rd = round(reading) + adj
        pct = (rd - round(bg)) / exp * 100.0
        edge = abs((pct * 10.0) % 1.0 - 0.5) / 10.0
        if edge > 0.02 and abs(pct - 90.0) > 0.06 and abs(pct - 110.0) > 0.06:
            return float(rd)
    return float(round(reading))


def check_records(T):
    """The engineers' source checks: background, then the reading with the source in the jig; a check whose
    source sat badly is repeated at the same visit. CS-0583 was at the metrology unit for recalibration from
    5 August to 4 September, and its engineer carried the laboratory's spare source in KIT-2 meanwhile."""
    r = rng("checks")
    S = {s["code"]: s for s in T["S"]}
    out = []
    repeat_codes = {"MV166", "MV318", "MV207"}
    for v in T["visits"]:
        s = S[v["code"]]
        day = v["local"].date()
        kit, serial, jig = W.KITS[v["eng"]]
        if kit == "KIT-2" and W.SPARE_IN_KIT2[0] <= day < W.SPARE_IN_KIT2[1]:
            serial = "CS-0417"                    # the spare source rode in KIT-2 while CS-0583 was recalibrated
        resp = T["resp"][s["code"]]
        if s["code"] == W.PROBE_EXCHANGE[0]:
            resp = 0.992                      # the new probe
        bg = s["bg"] * resp * r.normal(1, 0.006)
        src = source_true(serial, jig, day) * resp
        tries = []
        if s["code"] in repeat_codes:
            tries.append(bg + src * r.uniform(0.56, 0.71))
        exp, _ = expected(serial, jig, day)
        tries.append(clear_reading(bg, bg + src * r.normal(1, 0.004), exp))
        out.append(dict(code=s["code"], eng=v["eng"], local=v["local"], kit=kit, serial=serial, jig=jig,
                        background=bg, readings=tries, resp=resp))
    return out


def record(T):
    """The logger's ten-minute values: counting noise on what the probe sees, the source checks in test mode,
    the probe exchange and the power cuts (no record at all) and the gland faults (a record with no dose rate)."""
    S = T["S"]; n = W.N10
    r = rng("counting")
    idx = {s["code"]: i for i, s in enumerate(S)}
    resp = np.array([T["resp"][s["code"]] for s in S])[:, None]
    seen = (T["nat"] + T["art"]) * resp
    status = np.full((len(S), n), "V", dtype="<U1")
    probe = {}
    rs = rng("serials")
    for s in S:
        probe[s["code"]] = "GTP-%d" % int(rs.integers(41000, 49999))
    probe_after = "GTP-%d" % int(rs.integers(52000, 52999))
    # probe exchange: half an hour without a probe, then the new probe on the old probe's factor for a week
    code, when_local, ratio, applied_local = W.PROBE_EXCHANGE
    i = idx[code]
    a = t_index(when_local - W.BST); b = t_index(applied_local - W.BST)
    seen[i, a + 3:] = seen[i, a + 3:] / T["resp"][code] * 0.992
    seen[i, a + 3:b] *= ratio
    lost = np.zeros((len(S), n), dtype=bool)
    lost[i, a:a + 3] = True
    # source checks: the station is put in test mode from a few minutes before the source goes on
    for c in T["checks"]:
        j = idx[c["code"]]
        t0 = t_index(c["local"] - W.BST)
        n_try = len(c["readings"])
        span = 2 + n_try
        status[j, t0:t0 + span] = "T"
        for k, reading in enumerate(c["readings"]):
            frac = r.uniform(0.4, 0.8)
            seen[j, t0 + 1 + k] = c["background"] * (1 - frac) + reading * frac
    for c2, lst in T["cuts"].items():
        for st, en in lst:
            lost[idx[c2], st:en] = True
    fault = np.zeros((len(S), n), dtype=bool)          # a record arrives, but with no dose rate
    for c2, lst in T["faults"].items():
        for st, en in lst:
            fault[idx[c2], st:en] = True
            status[idx[c2], st:en] = "F"
    counts = r.poisson(np.clip(seen, 1, None) / 100.0 * W.COUNTS_PER_10MIN_AT_100)
    value = counts / W.COUNTS_PER_10MIN_AT_100 * 100.0
    value = np.round(value, 0)
    value[lost | fault] = np.nan
    return dict(value=value, status=status, lost=lost, fault=fault, probe=probe, probe_after=probe_after,
                exchange_t=(a, b))


def ingest(T):
    """The platform's telemetry receipts. Each outstation sends its last hour's values a few minutes after the
    hour on the primary channel; while the primary channel is down it uses its backup channel if it has one,
    otherwise it holds the values and sends them when the primary returns. The primary gateway sometimes misses
    its acknowledgement, and the outstation then sends that hour again with the next one."""
    S = T["S"]; n = W.N10
    r = rng("ingest")
    have = ~T["rec"]["lost"]
    backup = {s["code"]: (r.random() < 0.7) for s in S}
    outages = {}
    for s in S:
        k = int(r.choice([1, 1, 2, 2, 3]))
        lst = []
        for _ in range(k):
            st = int(r.integers(30, W.DAYS * 24 - 60)); ln = int(r.uniform(3, 40))
            lst.append((st, st + ln))
        outages[s["code"]] = lst
    rows = []
    bid = [700000]
    hours = W.DAYS * 24
    for i, s in enumerate(S):
        code = s["code"]
        down = np.zeros(hours + 2, dtype=bool)
        for st, en in outages[code]:
            down[st:en] = True
        pend = []          # held values while the primary is down and there is no backup
        resend = None      # an hour whose acknowledgement went missing
        for h in range(hours):
            ints = [t for t in range(h * 6, h * 6 + 6) if have[i, t]]
            send_at_min = h * 60 + 60   # the hour's end, minutes from the quarter start
            if down[h]:
                if backup[code]:
                    for t in ints:            # the backup channel carries one value at a time
                        rec = t * 10 + 10 + float(r.uniform(1.6, 5.8))
                        rows.append((bid[0], code, "backup", [t], rec)); bid[0] += int(r.integers(1, 3))
                else:
                    pend += ints
                continue
            batch = pend + (resend or []) + ints
            pend = []; resend = None
            if not batch:
                continue
            rec = send_at_min + float(r.uniform(1.2, 4.6))
            if len(batch) > 12:
                rec += float(r.uniform(0.5, 3.0))
            rows.append((bid[0], code, "primary", batch, rec)); bid[0] += int(r.integers(1, 4))
            if r.random() < 0.025 and ints:
                resend = ints
    return dict(rows=rows, backup=backup, outages=outages)


def air(T):
    """Weekly filters at three samplers, the pump controllers' fifteen-minute logs and the filters' gross beta.
    Each pump's measured flow falls through the week as its filter loads; the controllers' totalisers (AS1, AS3)
    count running time at the set flow, and AS2's old controller has only an hour meter."""
    start = dt.datetime(2026, 6, 30, 0, 0)   # UTC
    nq = (W.Q_END - start).days * 96
    tues = [dt.date(2026, 6, 30) + dt.timedelta(days=7 * k) for k in range(14)]
    out = {}
    for sampler, code, flow, style in W.AIR:
        rs = rng("air/" + sampler)
        changes = []
        for d in tues:
            local = dt.datetime.combine(d, dt.time(9, 20)) + dt.timedelta(minutes=int(rs.uniform(0, 140)))
            changes.append(local)
        status = np.full(nq, "RUN", dtype="<U5")
        q = lambda when_utc: int((when_utc - start).total_seconds() // 900)
        for c in changes:
            a = q(c - W.BST); status[a:a + 2] = "STOP"          # switched off for the filter change
        for st, en in T["cuts"][code]:
            a = q(W.Q_START + dt.timedelta(minutes=10 * st)); b = q(W.Q_START + dt.timedelta(minutes=10 * en))
            status[a:b + 1] = "STOP"
        if sampler == "AS1":
            a = q(dt.datetime(2026, 8, 18, 14, 0)); b = q(dt.datetime(2026, 8, 20, 16, 0))
            status[a:b] = "FAULT"
        load = np.ones(nq)
        lo, hi = (0.05, 0.10) if style == "hourmeter" else (0.035, 0.085)
        bounds = [q(c - W.BST) for c in changes] + [nq]
        for k in range(len(bounds) - 1):
            a, b = bounds[k], bounds[k + 1]
            s_k = float(rs.uniform(lo, hi))
            load[a:b] = 1.0 - s_k * np.linspace(0.0, 1.0, b - a)
        jitter = rs.normal(0, 0.006 if style == "hourmeter" else 0.010, nq)
        flows = np.where(status == "RUN", flow * load * (1 + jitter), 0.0)
        flows = np.round(flows, 2)
        inc = np.where(status == "RUN", flow * 0.25, 0.0)
        base = {"AS1": 61834.2, "AS2": 0.0, "AS3": 89084.3}[sampler]
        tot = base + np.concatenate([[0.0], np.cumsum(inc)[:-1]])
        if sampler == "AS1":                     # the faulty controller was replaced; the new one counts from zero
            rq = q(dt.datetime(2026, 8, 20, 16, 0))
            tot[rq:] = tot[rq:] - tot[rq]
        tot = np.round(tot, 1)
        drop = np.zeros(nq, dtype=bool)          # the flow transmitter's signal drops out; the pump keeps running
        rd = rng("dropouts/" + sampler)
        for k in range(len(bounds) - 2):
            lo_, hi_ = bounds[k] + 6, bounds[k + 1] - 6
            if rd.random() < 0.85:
                for _ in range(int(rd.choice([1, 1, 2]))):
                    ln = int(rd.integers(12, 41))
                    for _try in range(40):
                        st = int(rd.integers(lo_, hi_ - ln))
                        if (status[st - 3:st + ln + 3] == "RUN").all() and not drop[st - 12:st + ln + 12].any():
                            drop[st:st + ln] = True
                            break
        logged = np.where(drop, np.nan, flows)
        hm0 = 18412.6
        hours = np.concatenate([[0.0], np.cumsum(np.where(status == "RUN", 0.25, 0.0))[:-1]]) + hm0
        filters = []
        for k in range(1, 14):
            on, off = changes[k - 1], changes[k]
            a, b = q(on - W.BST), q(off - W.BST)
            true_vol = float(flows[a:b].sum() * 0.25)
            hours_run = float((status[a:b] == "RUN").sum() * 0.25)
            conc = float(rs.lognormal(math.log(0.52 if sampler != "AS3" else 0.41), 0.28))
            act = conc * true_vol / 1000.0
            meas = act * rs.normal(1, 0.025)
            vols = {how: logged_volume(logged, a, b, how) for how in VOLUME_ROUTES}
            filters.append(dict(sampler=sampler, k=k, on=on, off=off, true_vol=true_vol, hours_run=hours_run,
                                gold_vol=vols["linear"], vols=vols, logged_vol=float(np.nansum(logged[a:b]) * 0.25),
                                dropout_rows=int(drop[a:b].sum()),
                                set_vol=hours_run * flow, tot_on=float(tot[a]), tot_off=float(tot[b]),
                                hm_on=float(hours[a]), hm_off=float(hours[b]), conc=conc, act=act, meas=meas,
                                a=a, b=b))
        out[sampler] = dict(code=code, flow=flow, style=style, status=status, flows=flows, tot=tot,
                            filters=filters, start=start, drop=drop)
    return out


VOLUME_ROUTES = ("linear", "mean2", "ffill", "bfill", "filtermean")


def logged_volume(fl, a, b, how):
    """The air drawn from row a to row b (exclusive) on the logged measured flow, a dropout filled by `how`:
    linear interpolation, the mean of the values either side, the value before, the value after, or the filter's
    mean measured flow."""
    x = fl.copy()
    gaps = np.isnan(x)
    if gaps.any():
        idx = np.arange(len(x))
        if how == "linear":
            x[gaps] = np.interp(idx[gaps], idx[~gaps], x[~gaps])
        elif how == "filtermean":
            seg = x[a:b]
            x[gaps] = float(np.nanmean(seg[seg > 0]))
        else:
            t = 0
            while t < len(x):
                if gaps[t]:
                    e = t
                    while e < len(x) and gaps[e]:
                        e += 1
                    before, after = x[t - 1], x[e]
                    x[t:e] = {"mean2": (before + after) / 2.0, "ffill": before, "bfill": after}[how]
                    t = e
                else:
                    t += 1
    return float(x[a:b].sum() * 0.25)


def probe_faults(T):
    """Fault records: at the stations whose probe cable glands came from the 2025 batch, water gets in a few
    hours after heavy rain and the probe stops counting until the gland dries out or is reseated."""
    r = rng("glands")
    S = T["S"]; idx = {s["code"]: i for i, s in enumerate(S)}
    rain, wash = T["rain_st"], T["wash"]
    busy = {s["code"]: np.zeros(W.N10, dtype=bool) for s in S}
    for c in T["checks"]:
        t0 = t_index(c["local"] - W.BST); busy[c["code"]][t0 - 30:t0 + 40] = True
    for code, lst in T["cuts"].items():
        for st, en in lst:
            busy[code][st - 30:en + 30] = True
    code, when_local = W.PROBE_EXCHANGE[0], W.PROBE_EXCHANGE[1]
    t0 = t_index(when_local - W.BST); busy[code][t0 - 30:t0 + 40] = True
    for code, day in W.REINGEST:
        t0 = t_index(dt.datetime.combine(day, dt.time(0, 0))); busy[code][t0 - 30:t0 + 174] = True
    out = {}
    for code in W.GLAND_BATCH:
        i = idx[code]
        storm = np.convolve(rain[i] / 6.0, np.ones(18), mode="full")[:W.N10]     # mm in the last three hours
        cands = [t for t in range(300, W.N10 - 400, 7) if storm[t] > 5.0]
        r.shuffle(cands)
        want = int(r.choice([1, 1, 2]))
        lst = []
        for t in cands:
            if len(lst) == want:
                break
            st = t + int(r.integers(18, 60))
            ln = int(r.integers(18, 160))
            if wash[i, st - 12:st + 1].max() > 2.0 or rain[i, st - 6:st + 1].max() > 0.05:
                continue
            if busy[code][st - 6:st + ln + 6].any() or any(abs(st - a) < 900 for a, b in lst):
                continue
            lst.append((st, st + ln))
        out[code] = sorted(lst)
    return out


def timely_counts(T, without_test=False):
    """Each station's intervals whose value the platform first received within an hour of the interval's end
    (without_test: test-mode values left out, the reading agreement 2.3 rules out)."""
    have = ~(T["rec"]["lost"] | T["rec"]["fault"])
    if without_test:
        have &= T["rec"]["status"] != "T"
    idx = {s["code"]: i for i, s in enumerate(T["S"])}
    first = {s["code"]: np.full(W.N10, np.inf) for s in T["S"]}
    for bid, code, ch, ints, rec in T["ingest"]["rows"]:
        for t in ints:
            if rec < first[code][t]:
                first[code][t] = rec
    end = np.arange(W.N10) * 10.0 + 10.0
    return {c: int((have[idx[c]] & (first[c] - end <= 60.0)).sum()) for c in first}


def rounding_clearance(T):
    """Stations whose timeliness sits less than one interval from a rounding line, or rounds differently with its
    test-mode values left out, and how many values to lose to clear both."""
    need = {}
    unit = W.N10 / 1000.0

    def dist(m):
        edge = (math.floor(m / unit - 0.5) + 0.5) * unit
        return min(abs(m - edge), abs(m - edge - unit))

    full, bare = timely_counts(T), timely_counts(T, without_test=True)
    for c, n in full.items():
        if n == W.N10:
            continue
        n2 = bare[c]
        for k in range(0, 13):
            m, m2 = n - k, n2 - k
            if dist(m) >= 1.0 and dist(m2) >= 1.0 and round(m / unit) == round(m2 / unit):
                break
        if k:
            need[c] = k
    return need


def run():
    S = station_frame()
    rain_st, rain_g, fronts = rain_fields(S)
    radon = radon_series()
    nat, wash = natural(S, rain_st, radon)
    art, sessions = radiography(S, rain_st, rain_g, wash)
    V = visits(S)
    resp = response_factors(S)
    cuts = power_cuts(S)
    T = dict(S=S, rain_st=rain_st, rain_g=rain_g, fronts=fronts, radon=radon, nat=nat, wash=wash,
             art=art, sessions=sessions, visits=V, resp=resp, cuts=cuts)
    T["checks"] = check_records(T)
    T["faults"] = probe_faults(T)
    T["rec"] = record(T)
    T["ingest"] = ingest(T)
    need = rounding_clearance(T)
    if need:                                # a logger watchdog reset or two; the outstation loses those values
        r = rng("reboots")
        idx = {s["code"]: i for i, s in enumerate(S)}
        for code, k in sorted(need.items()):
            i = idx[code]
            down = np.zeros(W.N10, dtype=bool)
            for st, en in T["ingest"]["outages"][code]:
                down[st * 6:en * 6 + 6] = True
            quiet = [t for t in range(600, W.N10 - 600) if not down[t - 12:t + 12].any() and
                     T["wash"][i, t - 12:t + 12].max() < 2.0 and T["art"][i, t - 12:t + 12].max() == 0 and
                     T["rec"]["status"][i, t - 12:t + 12].tolist() ==
                     ["V"] * 24 and not T["rec"]["lost"][i, t - 12:t + 12].any() and t % 6 not in (0, 5)]
            for t in sorted(r.choice(quiet, size=k, replace=False)):
                T["rec"]["lost"][i, t] = True
                T["rec"]["value"][i, t] = np.nan
        T["ingest"] = ingest(T)
        assert not rounding_clearance(T), rounding_clearance(T)
    T["air"] = air(T)
    return T
