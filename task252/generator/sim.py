"""task252 world: eight plants' raw, filtered and final water ammonia through the fourth quarter of 2027, each
plant's three-stream analyser (carryover from the two samples before, a zero error at Holmedale, a span error at
Calderwood), the monthly checks, the analysers' faults, the telemetry's failed polls and the historian's lost hours,
the weekly sampling round and the laboratory's clock.

The water and the analysers repeat prototype cw12 draw for draw (seed 45), so the decisive margins measured there
hold; everything else draws from its own generator."""
import datetime as dt

import numpy as np

import params as P


def _water(rng, w, code):
    t = np.arange(P.NS)
    worn = code in P.WORN
    k1 = rng.uniform(0.06, 0.08) if worn else rng.uniform(0.002, 0.006)
    k2 = 0.35 * k1
    lo, hi = (0.30, 0.45) if code in P.HIGH else ((0.08, 0.15) if worn else (0.10, 0.20))
    base = rng.uniform(lo, hi) + 0.025 * np.sin(2 * np.pi * t / (144 * 9) + w)
    raw = base.copy()
    events = []
    for e in rng.uniform(0, P.NS, 20):
        h = rng.uniform(0.2, 1.0); up = rng.uniform(6, 12); dn = rng.uniform(24, 60)
        d = t - e
        raw += h * np.where(d < 0, np.exp(-0.5 * (d / up) ** 2), np.exp(-d / dn))
        events.append((float(e), float(h)))
    raw += rng.normal(0, 0.004, P.NS)
    if code in P.ZERO or code in P.GAIN:
        fil = rng.uniform(0.016, 0.022) + rng.normal(0, 0.0015, P.NS)
        fin = rng.uniform(0.014, 0.019) + rng.normal(0, 0.0012, P.NS)
    elif worn and code not in P.HIGH:
        fil = rng.uniform(0.040, 0.055) + rng.normal(0, 0.002, P.NS)
        fin = rng.uniform(0.006, 0.012) + rng.normal(0, 0.0012, P.NS)
    else:
        fil = rng.uniform(0.020, 0.045) + rng.normal(0, 0.002, P.NS)
        fin = rng.uniform(0.006, 0.012) + rng.normal(0, 0.0012, P.NS)
    lags = None
    if code in P.WEAK:
        b = rng.uniform(0.07, 0.12)
        lf = int(rng.uniform(15, 21)); ln = int(rng.uniform(24, 30))
        ex = (raw - np.percentile(raw, 5)).clip(0)
        fil = fil + b * np.r_[np.zeros(lf), ex[:-lf]]
        fin = fin + 0.7 * b * np.r_[np.zeros(ln), ex[:-ln]]
        lags = (b, lf, ln)
    return dict(k1=k1, k2=k2, raw=raw, fil=fil, fin=fin, events=events, breakthrough=lags)


def _check_days(rng, w):
    """the technician's monthly check: a weekday in the second week of each month, about nine to eleven"""
    out = []
    for m, d0 in ((10, 11), (11, 8), (12, 6)):
        day = dt.date(2027, m, d0) + dt.timedelta(days=int((w * 3 + rng.integers(0, 3)) % 5))
        while day.weekday() >= 5:
            day += dt.timedelta(days=1)
        hh = 9 + int(rng.integers(0, 3)); mm = int(rng.choice([0, 10, 20, 30, 40, 50]))
        t = dt.datetime(day.year, day.month, day.day, hh, mm, tzinfo=P.NZ)
        s = P.slot_of(t)
        s += (3 - s % 3) % 3                       # the check starts at the top of a cycle
        out.append(s)
    return out


def build():
    rng = np.random.default_rng(P.SEED_WORLD)
    W = {}
    for w, code in enumerate(P.CODES):
        x = _water(rng, w, code)
        order = [P.STREAM[c] for c in P.ORDER[code]]
        z = P.ZERO.get(code, 0.0); g = P.GAIN.get(code, 1.0)
        sl = np.array([order[i % 3] for i in range(P.NS)])
        val = np.zeros(P.NS)
        for s in ("raw", "fil", "fin"):
            m = sl == s
            val[m] = x[s][m]
        noise = {}
        for pos, s in enumerate(order):
            idx = np.arange(pos, P.NS, 3)
            noise[s] = rng.normal(0, 0.0008, idx.size)
        checks = [[round(g * P.CHECK_STD + z + rng.normal(0, 0.0012), 3) for _ in range(3)] for _ in range(3)]
        for d in range(3, 92, 7):                  # the prototype's grab draws, kept so later plants draw alike
            rng.integers(54, 72)
        for _ in range(13):
            rng.normal(0, 0.03); rng.normal(0, 0.002)
        W[code] = dict(code=code, w=w, order=order, z=z, g=g, k1=x["k1"], k2=x["k2"], true=dict(raw=x["raw"],
                       fil=x["fil"], fin=x["fin"]), sl=sl, val=val, noise=noise, checks=checks, events=x["events"],
                       breakthrough=x["breakthrough"])
    ops = np.random.default_rng(P.SEED_OPS)
    for code in P.CODES:
        x = W[code]
        x["check_slots"] = _check_days(ops, x["w"])
        val = x["val"].copy()
        for s0 in x["check_slots"]:
            val[s0:s0 + 3] = P.CHECK_STD          # the flushed cell holds the standard for the check's cycle
        x["cell"] = val
        _readings(x)
    _faults(ops, W)
    rep = np.random.default_rng(P.SEED_REPAIR)
    for code in P.CODES:
        x = W[code]
        x["repair_checks"] = [f["b"] for f in x["faults"]]
        x["repair_reads"] = [[round(x["g"] * P.CHECK_STD + x["z"] + rep.normal(0, 0.0012), 3) for _ in range(3)]
                             for _ in x["repair_checks"]]
        for s0 in x["repair_checks"]:
            x["cell"][s0:s0 + 3] = P.CHECK_STD    # the technician's check after clearing the fault
        _readings(x)
    _telemetry(ops, W)
    _round(np.random.default_rng(P.SEED_LAB), W)
    _bench(np.random.default_rng(P.SEED_BENCH), W)
    _lab_extras(np.random.default_rng(P.SEED_DUP), W)
    _outstations(np.random.default_rng(P.SEED_TELEM), W)
    _signals(np.random.default_rng(P.SEED_SIGNAL), W)
    return W


def _lab_extras(rng, W):
    """the 7 December round's treated bottles, which reception logged a second time when the delayed bins were
    unpacked, keying from the courier's docket rather than the bottles' labels: new sample numbers, the docket's pickup
    time as the collection time for every bottle, the reception time 25 minutes later, the one analysis and release"""
    rounds = W[P.CODES[0]]["round"]
    for r in rounds:
        r["extras"] = []
        if r["day"] == dt.date(2027, 12, 7):
            last = max(s["collected"] for s in r["samples"])
            docket = last + dt.timedelta(minutes=int(rng.integers(35, 55)))
            for s in r["samples"]:
                if s["stream"] != "raw":
                    r["extras"].append(dict(s, collected=docket, bottle=s["collected"],
                                            received=s["received"] + dt.timedelta(minutes=25), kind="logged again"))
    n = 0
    for r in rounds:
        for s in r["samples"] + r["extras"]:
            n += 1
            s["no"] = n


def _bench(rng, W):
    """the bench each morning and the release of each run: on one morning the analyst put the ammonia run on as the
    bins were logged in, so its first cups ran within minutes of reception; the laboratory releases a run's results
    when the analyst has checked it, within minutes on the mornings with a short queue and after the morning's other
    runs otherwise. Every other normal round's start moves by up to 25 minutes, chosen so no treated sample's true
    time from collection to analysis falls within ten minutes of 24 hours (the analyser's clock is an hour behind, and
    the reception and release stamps bracket that hour to within ten minutes either way) and every plant keeps one,
    or three or more, treated samples analysed between 24 hours 10 minutes and 25 hours after collection"""
    rounds = W[P.CODES[0]]["round"]
    normal = [k for k, r in enumerate(rounds) if r["day"] != dt.date(2027, 12, 28) and k not in (3, 9)]
    band = (23 * 60 + 50, 24 * 60 + 10)
    base = {k: [q["analysed"] for q in r["samples"]] for k, r in enumerate(rounds)}

    def mins(q, t):
        return (t - q["collected"]).total_seconds() / 60

    def clear(k, shift):
        return all(not (band[0] < mins(q, t + shift) <= band[1]) and abs(mins(q, t + shift) - 1500) > 1
                   for q, t in zip(rounds[k]["samples"], base[k]) if q["stream"] != "raw")

    for attempt in range(2000):
        quick = None
        for k in rng.permutation(normal):
            k = int(k)
            smp = rounds[k]["samples"]
            recv, first = smp[0]["received"], min(base[k])
            ms = [m for m in rng.permutation(np.arange(3, 11)) if clear(k, recv + dt.timedelta(minutes=int(m)) - first)]
            if ms:
                quick = (k, recv + dt.timedelta(minutes=int(ms[0])) - first)
                break
        shifts = {}
        for k in range(len(rounds)):
            if quick and k == quick[0]:
                shifts[k] = quick[1]
            elif k in normal:
                ok = [dt.timedelta(minutes=int(m)) for m in rng.permutation(np.arange(-25, 26))]
                ok = [c for c in ok if clear(k, c) and min(base[k]) + c > rounds[k]["samples"][0]["received"]
                      + dt.timedelta(minutes=12)]
                if not ok:
                    break
                shifts[k] = ok[0]
            else:
                shifts[k] = dt.timedelta(0)
        if len(shifts) < len(rounds):
            continue
        cover = {c: 0 for c in P.CODES}
        for k, r in enumerate(rounds):
            for q, t in zip(r["samples"], base[k]):
                if q["stream"] != "raw" and band[1] < mins(q, t + shifts[k]) <= 25 * 60:
                    cover[q["code"]] += 1
        late = {c: 0 for c in P.CODES}
        raw1 = {c: 0 for c in P.CODES}
        raw0 = {c: 0 for c in P.CODES}
        early = 0
        for k, r in enumerate(rounds):
            for q, t in zip(r["samples"], base[k]):
                early += (t + shifts[k] - q["received"]).total_seconds() < 3600
                m = mins(q, t + shifts[k])
                if q["stream"] != "raw" and m > 24 * 60:
                    late[q["code"]] += 1
                if q["stream"] == "raw":
                    raw1[q["code"]] += m > 24 * 60
                    raw0[q["code"]] += m > 25 * 60
        vals = list(late.values())
        if (all(v not in (0, 2) for v in cover.values())     # the clock moves every plant, never by the 7 December
                and max(vals.count(v) for v in vals) <= 2    # round's second logging (two a plant), so the two never
                and early <= 16                              # net; no count shared by three plants; few early stamps;
                and sum(raw0[c] in (cover[c], cover[c] - 2) for c in P.CODES) <= 2):
            break                                            # raw samples counted with the clock missed: two at most
    else:
        raise RuntimeError("no bench plan clears the band and covers every plant")
    fast = set(int(k) for k in rng.choice(len(rounds), 3, replace=False))
    for k, r in enumerate(rounds):
        for q, t in zip(r["samples"], base[k]):
            q["analysed"] = t + shifts[k]
        last = max(q["analysed"] for q in r["samples"])
        lag = int(rng.integers(4, 9)) if k in fast else int(rng.integers(25, 200))
        for q in r["samples"]:
            q["released"] = last + dt.timedelta(minutes=lag)
        r["quick"] = k == quick[0]
        r["fast_release"] = k in fast


def _signals(rng, W):
    """signal faults: a port's reading lost between the analyser and the PLC (a wet junction box, a failed loop
    isolator) while the analyser itself went on measuring; the electrician who clears it does not touch the analyser,
    so no check follows. One on each plant's filtered water port and three on final water ports"""
    fw = set(int(i) for i in rng.choice(len(P.CODES), 3, replace=False))
    for w, code in enumerate(P.CODES):
        x = W[code]
        busy = set(range(0, 288)) | set(range(P.NS - 288, P.NS))
        for f in x["faults"]:
            busy |= set(range(f["a"] - 18, f["b"] + 21))
        for c in x["check_slots"]:
            busy |= set(range(c - 18, c + 21))
        for s_, e_ in x["comms"]:
            busy |= set(range(s_ - 18, e_ + 18))
        for a_, b_ in (x["lost"], x["swap"]):
            busy |= set(range(a_ - 18, b_ + 18))
        x["signals"] = []
        for port, lo, hi in [("fil", 4.0, 9.0)] + ([("fin", 2.0, 6.0)] if w in fw else []):
            for _ in range(500):
                day = int(rng.integers(3, 88))
                start = dt.datetime(2027, 10, 1, tzinfo=P.NZ) + dt.timedelta(days=day, hours=float(rng.uniform(0, 24)))
                a, b = _span(start, float(rng.uniform(lo, hi)))
                if busy & set(range(a - 3, b + 3)):
                    continue
                busy |= set(range(a - 18, b + 18))
                x["signals"].append(dict(port=port, a=a, b=b))
                break
            else:
                raise RuntimeError("no free window for a signal fault at %s" % code)
        x["signals"].sort(key=lambda f: f["a"])


def _readings(x):
    """each port's reading: its own water plus the shares of the two slots before it in the cell, through the
    analyser's span and zero"""
    val = x["cell"]
    reading = np.full(P.NS, np.nan)
    for pos, s in enumerate(x["order"]):
        idx = np.arange(pos, P.NS, 3)
        p1 = np.maximum(idx - 1, 0); p2 = np.maximum(idx - 2, 0)
        co = x["k1"] * (val[p1] - val[idx]) + x["k2"] * (val[p2] - val[idx])
        reading[idx] = np.round(x["g"] * (val[idx] + co) + x["z"] + x["noise"][s], 3)
    x["reading"] = reading


def _span(t0, hours):
    a = P.slot_of(t0)
    return a, a + int(round(hours * 6))


def _faults(rng, W):
    """analyser faults the analyser itself reports (quality F at the ports it could not read): reagent run out until
    the technician's next visit, a blocked sample filter on one port after a storm, a cell fault; each stops the
    readings until a technician clears it, and the technician then runs the check on the standard (three check-port
    slots from the top of the next cycle) before returning the sequencer to its ports"""
    kinds = {"ASH": ["reagent", "filter:fil"], "BRN": ["filter:fil", "cell", "cell"], "CAL": ["reagent", "cell"],
             "DUN": ["filter:fil", "reagent", "filter:fin"], "ELS": ["cell", "filter:fil"],
             "FEN": ["reagent", "filter:fil", "cell"], "GAR": ["filter:fil", "filter:fil", "cell"],
             "HOL": ["reagent", "cell", "filter:fin"]}
    for code in P.CODES:
        x = W[code]
        x["faults"] = []
        busy = set()
        for c in x["check_slots"]:
            busy |= set(range(c - 12, c + 15))
        for k in kinds[code]:
            for _ in range(200):
                day = int(rng.integers(2, 89))
                if k == "reagent":
                    start = dt.datetime(2027, 10, 1, tzinfo=P.NZ) + dt.timedelta(days=day, hours=float(rng.uniform(0, 24)))
                    hours = float(rng.uniform(9, 30))
                elif k == "cell":
                    start = dt.datetime(2027, 10, 1, tzinfo=P.NZ) + dt.timedelta(days=day, hours=float(rng.uniform(0, 24)))
                    hours = float(rng.uniform(2.6, 4.5))
                else:
                    start = dt.datetime(2027, 10, 1, tzinfo=P.NZ) + dt.timedelta(days=day, hours=float(rng.uniform(0, 24)))
                    hours = float(rng.uniform(2.5, 14))
                a, b = _span(start, hours)
                b += (3 - b % 3) % 3
                if b + 3 >= P.NS or busy & set(range(a - 6, b + 9)):
                    continue
                busy |= set(range(a, b + 3))
                x["faults"].append(dict(kind=k.split(":")[0], port=(k.split(":")[1] if ":" in k else None), a=a, b=b))
                break
        x["faults"].sort(key=lambda f: f["a"])


def _telemetry(rng, W):
    """failed polls: the link to a plant drops, the historian writes each missed slot with quality F, and when the link
    returns it reloads the readings from the plant's PLC, so the slot holds both rows; and one night the historian's
    own store lost five hours for every plant, which were never reloaded"""
    out = dt.datetime(2027, 11, 17, 1, 20, tzinfo=P.NZ)
    a, b = _span(out, 5 + 1 / 3)
    for code in P.CODES:
        x = W[code]
        x["lost"] = (a, b)
        busy = set(range(a - 12, b + 12))
        for f in x["faults"]:
            busy |= set(range(f["a"] - 6, f["b"] + 6))
        for c in x["check_slots"]:
            busy |= set(range(c - 6, c + 9))
        x["comms"] = []
        n = {"ASH": 2, "BRN": 1, "CAL": 2, "DUN": 1, "ELS": 3, "FEN": 2, "GAR": 1, "HOL": 2}[code]
        while len(x["comms"]) < n:
            day = int(rng.integers(2, 89))
            start = dt.datetime(2027, 10, 1, tzinfo=P.NZ) + dt.timedelta(days=day, hours=float(rng.uniform(0, 24)))
            s, e = _span(start, float(rng.uniform(2.3, 7.5)))
            if e >= P.NS or busy & set(range(s, e)):
                continue
            busy |= set(range(s - 6, e + 6))
            x["comms"].append((s, e))
        x["comms"].sort()


def _outstations(rng, W):
    """the telemetry renewal: in November each plant's outstation was swapped for a new unit during a working day.
    While the old unit was out the historian's polls of the plant failed, and the new unit came in with an empty
    store, so nothing was filled back; the PLC went on reading its analyser and dosing on it throughout"""
    days = [dt.date(2027, 11, d) for d in (9, 10, 11, 16, 17, 18, 23, 24)]
    order = ["CAL", "GAR", "HOL", "ASH", "FEN", "DUN", "BRN", "ELS"]      # the contractor's route, by repeater
    for code, day in zip(order, days):
        x = W[code]
        busy = set()
        for f in x["faults"]:
            busy |= set(range(f["a"] - 18, f["b"] + 21))
        for c in x["check_slots"]:
            busy |= set(range(c - 18, c + 21))
        for s, e in x["comms"]:
            busy |= set(range(s - 18, e + 18))
        a0, b0 = x["lost"]
        busy |= set(range(a0 - 18, b0 + 18))
        for _ in range(200):
            start = dt.datetime(day.year, day.month, day.day, 8, 30, tzinfo=P.NZ) + dt.timedelta(
                minutes=int(rng.integers(0, 37)) * 10 + int(rng.integers(0, 10)))
            hours = float(rng.uniform(2.7, 4.9))
            a, b = _span(start, hours)
            if not busy & set(range(a, b)):
                break
        else:
            raise RuntimeError("no free window for the outstation change at %s" % code)
        live = P.slot_end(b - 1).astimezone(P.NZ) + dt.timedelta(minutes=int(rng.integers(1, 9)))
        x["swap"] = (a, b)
        x["swap_live"] = live


def _round(rng, W):
    """the weekly sampling round (Tuesdays): one sampler drives the eight plants in a fixed order taking raw, filtered
    and final water; the chilly bins go by overnight courier to the laboratory, which runs ammonia in sample-number
    order from about nine the next morning; the 28 December round waited for the laboratory to reopen on 5 January;
    the laboratory's analyser stamps its runs in New Zealand standard time all year"""
    order = ["ASH", "FEN", "DUN", "BRN", "ELS", "CAL", "GAR", "HOL"]
    tuesdays = [dt.date(2027, 10, 5) + dt.timedelta(days=7 * k) for k in range(13)]
    rounds = []
    n = 0
    for wk, day in enumerate(tuesdays):
        t = dt.datetime(day.year, day.month, day.day, 8, 20, tzinfo=P.NZ) + dt.timedelta(minutes=int(rng.integers(0, 20)))
        samples = []
        k = (3 * wk) % 8                                          # the round starts at a different plant each week
        todays = order[k:] + order[:k]
        for code in (todays if wk % 2 == 0 else todays[::-1]):     # and is driven both ways
            t += dt.timedelta(minutes=int(rng.integers(22, 38)))
            for j, s in enumerate(("raw", "fil", "fin")):
                tc = t + dt.timedelta(minutes=6 * j + int(rng.integers(0, 3)))
                samples.append(dict(code=code, stream=s, collected=tc))
            t += dt.timedelta(minutes=18)
        late_courier = wk in (3, 9)                 # the courier van broke down: the bins came in at noon
        if day == dt.date(2027, 12, 28):
            recv = dt.datetime(2028, 1, 5, 8, 10, tzinfo=P.NZ)
            run0 = dt.datetime(2028, 1, 5, 9, 5, tzinfo=P.NZ)
        elif late_courier:
            recv = dt.datetime(day.year, day.month, day.day, 12, 40, tzinfo=P.NZ) + dt.timedelta(days=1)
            run0 = dt.datetime(day.year, day.month, day.day, 8, 50, tzinfo=P.NZ) + dt.timedelta(days=2)
        else:
            recv = dt.datetime(day.year, day.month, day.day, 8, 0, tzinfo=P.NZ) + dt.timedelta(
                days=1, minutes=int(rng.integers(0, 35)))
            if rng.random() < 0.4:                                   # ammonia first on the bench
                run0 = recv + dt.timedelta(minutes=int(rng.integers(12, 30)))
            else:                                                    # after the morning's nutrients run
                run0 = recv + dt.timedelta(minutes=int(rng.integers(55, 95)))
        # sample numbers follow the round; the bench runs the raw waters first (they need dilution), then the
        # filtered and then the final waters, each set in the order of the site codes, about four minutes a cup
        for smp in samples:
            n += 1
            smp["no"] = n
            smp["received"] = recv
        ta = run0
        for s in ("raw", "fil", "fin"):
            for smp in sorted((q for q in samples if q["stream"] == s), key=lambda q: q["code"]):
                ta += dt.timedelta(minutes=int(rng.integers(3, 6)))
                smp["analysed"] = ta                        # true time of analysis
        rounds.append(dict(day=day, samples=samples))
    for code in P.CODES:
        W[code]["grabs"] = []
    for r in rounds:
        for smp in r["samples"]:
            x = W[smp["code"]]
            i = P.slot_of(smp["collected"])
            tr = float(x["true"][smp["stream"]][min(i, P.NS - 1)])
            cv = 0.03 if smp["stream"] == "raw" else 0.04
            smp["true"] = tr
            smp["lab"] = tr * (1 + rng.normal(0, cv)) + rng.normal(0, 0.002)
            x["grabs"].append(smp)
    for code in P.CODES:
        W[code]["round"] = rounds


def channel_truth(W):
    """each channel's quarter offset over the readings the historian holds with quality G (the estimand)"""
    out = {}
    for code in P.CODES:
        x = W[code]
        q = qc_series(x)
        for s in ("fil", "fin"):
            idx = np.where((x["sl"] == s) & (q == "G"))[0]
            out[(code, s)] = float(np.mean(x["reading"][idx] - x["cell"][idx]))
    return out


def qc_series(x):
    """the quality code each slot's row carries once the historian has reloaded what it could: V on a check cycle, F
    where the analyser could not read or its signal never reached the PLC, 'lost' where the historian holds no row,
    'S' where an outstation change left the polls unfilled, G elsewhere (failed polls reloaded)"""
    q = np.array(["G"] * P.NS, dtype=object)
    for f in x["faults"]:
        if f["port"] is None:
            q[f["a"]:f["b"]] = "F"
        else:
            for i in range(f["a"], f["b"]):
                if x["sl"][i] == f["port"]:
                    q[i] = "F"
    for f in x.get("signals", []):
        for i in range(f["a"], f["b"]):
            if x["sl"][i] == f["port"]:
                q[i] = "F"
    for c in x["check_slots"] + x.get("repair_checks", []):
        q[c:c + 3] = "V"
    a, b = x["lost"]
    q[a:b] = "lost"
    if "swap" in x:
        a, b = x["swap"]
        q[a:b] = "S"
    return q
