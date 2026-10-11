"""The oil sampling calendar and the laboratory results (main tank and tap-changer compartments).

Gas trajectories per role:
  normal / code2_*  ageing gases with drift and laboratory scatter
  degassed          oil processed (degassed and dried), gases rebuilding afterwards
  L1, L2            the tap-changer barrier weeps from LEAK_ONSET: every tap operation carries
                    diverter-compartment oil into the main tank, so acetylene (and a little hydrogen,
                    ethylene and methane) rises in proportion to the operations
  V, A3             internal arcing from ARC_ONSET: acetylene with hydrogen at about twice
                    (V) and 1.7 times (A3) the acetylene, a slight ethylene rise, in bursts that have
                    nothing to do with the tap changer's operations
  T1, T2, T3        thermal faults in oil: ethylene, methane and ethane rising, little acetylene
"""
import datetime as dt
import math

import numpy as np

import world as W
import sim

D = dt.date.fromisoformat
GAS_ALL = ["H2", "CH4", "C2H6", "C2H4", "C2H2", "CO", "CO2", "O2", "N2"]


def rng(k):
    return np.random.default_rng(W.SEED * 7919 + k)


def workday(d):
    return d.weekday() < 5 and d not in W.HOLIDAYS


def next_workday(d):
    while not workday(d):
        d += dt.timedelta(1)
    return d


# ---------------------------------------------------------------------------------------------
# calendar
def round_list():
    out = []
    for y in range(2021, 2027):
        for m in (3, 6, 9, 12):
            if (y, m) <= (2026, 9):
                out.append((y, m))
    return out


def round_days(y, m, r):
    key = f"{y}-{m:02d}"
    if key in W.ROUND_AS_WORKED:
        return [(D(d), pair) for d, pair in W.ROUND_AS_WORKED[key]]
    d = dt.date(y, m, 7)
    while d.weekday() != 0:
        d += dt.timedelta(1)
    skip = None
    if r.random() < 0.35:
        skip = int(r.integers(1, 10))
    out = []
    k = 0
    while len(out) < 11:
        if workday(d):
            if skip is not None and k == skip:
                skip = None
            else:
                out.append(d)
            k += 1
        d += dt.timedelta(1)
    return list(zip(out, W.ROUTE))


def plan():
    """Every main-tank sample: (tid, sampled local naive datetime, round key)."""
    r = rng(1)
    samples = []
    for y, m in round_list():
        key = f"{y}-{m:02d}"
        for d, pair in round_days(y, m, r):
            t = dt.datetime.combine(d, dt.time(9, 0)) + dt.timedelta(minutes=int(r.integers(5, 70)))
            for j, sub in enumerate(pair):
                if j == 1:
                    t = t + dt.timedelta(minutes=int(r.integers(80, 150)))
                for pos in ("T1", "T2"):
                    samples.append((f"{sub}-{pos}", t, key))
                    t = t + dt.timedelta(minutes=int(r.integers(12, 26)))
    for mth, (da, db) in W.MONTHLY_2026.items():
        for day, units in ((D(da), W.WATCH_LIST[:5]), (D(db), W.WATCH_LIST[5:])):
            t = dt.datetime.combine(day, dt.time(8, 50)) + dt.timedelta(minutes=int(r.integers(0, 25)))
            for tid in units:
                samples.append((tid, t, f"2026-{mth:02d}m"))
                t = t + dt.timedelta(minutes=int(r.integers(38, 72)))
    samples.sort(key=lambda s: (s[1], s[0]))
    return samples


def analysis_dates(samples):
    r = rng(2)
    lag = {}
    out = []
    for tid, t, key in samples:
        d = t.date()
        if d not in lag:
            a = next_workday(d + dt.timedelta(int(r.integers(3, 8))))
            if a > W.EXTRACT_DATE - dt.timedelta(1):
                a = next_workday(d + dt.timedelta(3))
            lag[d] = a
        out.append(lag[d])
    return out


# ---------------------------------------------------------------------------------------------
# helpers
def years(t):
    return (t - dt.datetime(2021, 1, 1)).total_seconds() / (365.25 * 86400)


def ws(temp):
    return 10 ** (7.42 - 1670.0 / (temp + 273.0))


def tracking_r(levels, ops_between, per_day=None):
    a = np.asarray(levels, float)
    inc = np.diff(a)
    o = np.asarray(ops_between, float)
    if per_day is not None:
        inc = inc / per_day
        o = o / per_day
    if len(inc) < 3 or inc.std() == 0 or o.std() == 0:
        return 0.0
    return float(np.corrcoef(inc, o)[0, 1])


# ---------------------------------------------------------------------------------------------
def unit_params(u, r):
    fb = u["pres"] == "FB"
    old = W.age_band(u) == ">30"
    p = {}
    if fb:
        p["H2"] = (r.uniform(3, 8), 0.0)
        p["CH4"] = (r.uniform(2, 6), r.uniform(0.0, 0.3))
        p["C2H6"] = (r.uniform(1.5, 4.5), r.uniform(0.0, 0.15))
        p["C2H4"] = (r.uniform(2.5, 8.0), r.uniform(0.0, 0.35))
        p["CO"] = (r.uniform(120, 290) + (40 if old else 0), r.uniform(5, 16))
        p["CO2"] = (r.uniform(1300, 2600) + (700 if old else 0), r.uniform(180, 520))
        p["O2"] = r.uniform(17500, 23500)
        p["N2"] = r.uniform(48000, 59000)
    else:
        p["H2"] = (r.uniform(14, 40), r.uniform(0.0, 1.2))
        p["CH4"] = (r.uniform(8, 26), r.uniform(0.2, 1.3))
        p["C2H6"] = (r.uniform(8, 42), r.uniform(0.2, 1.6))
        p["C2H4"] = (r.uniform(3, 11), r.uniform(0.0, 0.4))
        p["CO"] = (r.uniform(260, 600), r.uniform(10, 30))
        p["CO2"] = (r.uniform(1800, 4200) + (1000 if old else 0), r.uniform(260, 700))
        p["O2"] = r.uniform(1300, 4200)
        p["N2"] = r.uniform(33000, 51000)
    p["C2H2"] = (0.08, 0.0)
    role = u["role"]
    if role == "code2_CO":
        p["CO"] = (548.0, 5.0)
    elif role == "code2_C2H6":
        p["C2H6"] = (156.0, 2.0)
    elif role == "code2_CO2":
        p["CO2"] = (5620.0, 150.0)
    elif role == "L1":
        p["CO"] = (232.0, 71.0)
    elif role == "L2":
        p["CO2"] = (1650.0, 905.0)
    if u["id"] in ("SBG-T1", "GLT-T1"):
        p["C2H2"] = (0.72, 0.0)        # trace acetylene, stable since before 2021
    return p


def baseline(p, gas, t):
    b, s = p[gas]
    return b + s * years(t)


def processed_value(eq, gas, t, proc):
    """After oil processing the gases fall to a few per cent and rebuild toward the old trend."""
    if proc is None or t < proc:
        return eq
    tau = {"H2": 0.5, "CH4": 0.9, "C2H6": 1.0, "C2H4": 1.0, "C2H2": 1.0, "CO": 1.1, "CO2": 1.5}[gas]
    k = 1 - math.exp(-((t - proc).total_seconds() / (365.25 * 86400)) / tau)
    lo = 0.06 * eq
    return lo + (eq - lo) * k


def true_values(u, p, t, extra):
    tid = u["id"]
    proc = extra["proc"].get(tid)
    v = {}
    for g in W.GASES:
        v[g] = processed_value(baseline(p, g, t), g, t, proc)
    if tid == "WML-T1":   # a heavier rebuild of carbon dioxide after the 2025 processing
        if proc is not None and t >= proc:
            k = 1 - math.exp(-((t - proc).total_seconds() / (365.25 * 86400)) / 1.45)
            v["CO2"] = 260 + (7200 - 260) * k
    o2 = p["O2"]
    if proc is not None and t >= proc:
        k = 1 - math.exp(-((t - proc).total_seconds() / (365.25 * 86400)) / 0.12)
        o2 = 600 + (p["O2"] - 600) * k
    v["O2"] = o2
    v["N2"] = p["N2"]
    role = u["role"]
    if role in ("L1", "L2"):
        k = extra["leak_k"][tid]
        ops = extra["leak_ops"](tid, t)
        c = k * ops
        v["C2H2"] += c
        v["H2"] += 0.10 * c
        v["C2H4"] += 0.20 * c
        v["CH4"] += 0.08 * c
        v["C2H6"] += 0.01 * c
    if role in ("V", "A3"):
        c = extra["arc_c2h2"](tid, t)
        v["C2H2"] = 0.08 + c
        v["H2"] += (2.0 if role == "V" else 1.67) * c
        v["C2H4"] += (0.25 if role == "V" else 0.30) * c
        v["CH4"] += 0.10 * c
    if role in ("T1", "T2", "T3"):
        onset = dt.datetime.combine(W.THERMAL_ONSET[tid], dt.time(0))
        if t > onset:
            f = extra["thermal_rate"][tid] * (t - onset).total_seconds() / (365.25 * 86400)
            v["C2H4"] += f
            v["CH4"] += 0.42 * f
            v["C2H6"] += 0.21 * f
            v["H2"] += 0.10 * f
            v["C2H2"] += (0.004 if role == "T2" else 0.009) * f
    return v


def report(g, x, r):
    """Laboratory reporting: scatter, resolution and the detection limit."""
    if g == "C2H2":
        y = x + r.normal(0, 0.02 + 0.0012 * x)
        if y < W.DETECTION[g]:
            return f"<{W.DETECTION[g]}"
        return f"{y:.1f}"
    sd = {"H2": (0.5, 0.03), "CH4": (0.4, 0.03), "C2H6": (0.4, 0.03), "C2H4": (0.4, 0.025),
          "CO": (3.0, 0.025), "CO2": (15.0, 0.02), "O2": (0.0, 0.025), "N2": (0.0, 0.02)}[g]
    y = x + r.normal(0, sd[0] + sd[1] * x)
    lim = W.DETECTION.get(g)
    if lim is not None and y < lim:
        return f"<{lim}"
    return str(int(round(y)))


def num(s):
    if s is None or s == "":
        return None
    if isinstance(s, str) and s.startswith("<"):
        return float(s[1:]) / 2
    return float(s)


# ---------------------------------------------------------------------------------------------
# building the results
def _fmt_c2h2(x):
    return f"{x:.1f}" if x >= W.DETECTION["C2H2"] else f"<{W.DETECTION['C2H2']}"


def _design_increments(total, n, fixed_inc, fixed_ops, free_ops, days_fixed, days_free, r, windows,
                       tries=40000, step=0.1):
    """Choose n non-negative increments (multiples of step) summing to total that keep the
    increments uncorrelated with the tap operations in every window, raw and per day.
    windows: list of (use_fixed, slice over the free increments)."""
    best, best_score = None, 9.0
    units = int(round(total / step))
    for _ in range(tries):
        w = r.dirichlet(np.full(n, 0.55))
        raw = w * units
        base = np.floor(raw).astype(int)
        rem = units - base.sum()
        order = np.argsort(-(raw - base))
        base[order[:rem]] += 1
        inc = base * step
        score = 0.0
        for use_fixed, sl in windows:
            a = list(fixed_inc) if use_fixed else []
            o = list(fixed_ops) if use_fixed else []
            dd = list(days_fixed) if use_fixed else []
            a += list(inc[sl])
            o += list(free_ops[sl])
            dd += list(days_free[sl])
            a, o, dd = np.array(a), np.array(o, float), np.array(dd, float)
            for x, y in ((a, o), (a / dd, o / dd)):
                if x.std() == 0:
                    continue
                score = max(score, abs(float(np.corrcoef(x, y)[0, 1])))
        if score < best_score:
            best, best_score = inc.copy(), score
            if score < 0.06:
                break
    return best, best_score


def build(dlist, H, ops, cnt):
    samples = plan()
    adates = analysis_dates(samples)
    iday = {d: i for i, d in enumerate(dlist)}

    def ops_between(tid, d1, d2):
        j = W.IDS.index(tid)
        return int(ops[iday[d1]:iday[d2], j].sum())

    per = {}
    for i, (tid, t, key) in enumerate(samples):
        per.setdefault(tid, []).append(i)

    def sample_in(tid, key):
        return next(i for i in per[tid] if samples[i][2] == key)

    # leak coefficients so the twelve-month increase lands near its tuned value
    leak_k = {}
    for tid in W.LEAK_ONSET:
        b, l = sample_in(tid, "2025-09"), sample_in(tid, "2026-09")
        o = ops_between(tid, samples[b][1].date(), samples[l][1].date())
        leak_k[tid] = W.TUNED_INCREASE[tid][1] / o

    def leak_ops(tid, t):
        on = W.LEAK_ONSET[tid]
        return 0 if t.date() <= on else ops_between(tid, on, t.date())

    thermal_rate = {}
    for tid in W.THERMAL_ONSET:
        b, l = sample_in(tid, "2025-09"), sample_in(tid, "2026-09")
        days = (samples[l][1].date() - samples[b][1].date()).days
        thermal_rate[tid] = W.TUNED_INCREASE[tid][1] * 365.25 / days

    proc = {tid: dt.datetime.combine(d, dt.time(12)) for tid, d, n in W.OIL_PROCESSING}
    arc_levels = {}
    extra = {"proc": proc, "leak_k": leak_k, "leak_ops": leak_ops, "thermal_rate": thermal_rate,
             "arc_c2h2": lambda tid, t: arc_levels[tid].get(t, 0.0)}

    params = {}
    for j, u in enumerate(W.UNITS):
        params[u["id"]] = unit_params(u, rng(100 + j))

    rep = [None] * len(samples)
    truth = [None] * len(samples)

    def gen(tid):
        u = W.UNIT[tid]
        r = rng(300 + W.IDS.index(tid))
        for i in per[tid]:
            t = samples[i][1]
            v = true_values(u, params[tid], t, extra)
            truth[i] = v
            rep[i] = {g: report(g, v[g], r) for g in GAS_ALL}

    order = [t for t in W.IDS if W.UNIT[t]["role"] not in ("V", "A3")]
    for tid in order:
        gen(tid)

    def set_inc(tid, gas, delta, step):
        b, l = sample_in(tid, "2025-09"), sample_in(tid, "2026-09")
        bv = float(rep[b][gas])
        nv = round(bv + delta, 1 if step < 1 else 0)
        rep[l][gas] = (f"{nv:.1f}" if step < 1 else str(int(nv)))

    # the leaking units: twelve-month acetylene increase as tuned, hydrogen up by 1 ppm
    for tid in W.LEAK_ONSET:
        set_inc(tid, "C2H2", W.TUNED_INCREASE[tid][1], 0.1)
        b, l = sample_in(tid, "2025-09"), sample_in(tid, "2026-09")
        rep[l]["H2"] = str(int(rep[b]["H2"]) + 1)
    for tid in W.THERMAL_ONSET:
        set_inc(tid, "C2H4", W.TUNED_INCREASE[tid][1], 1)

    # V: the same main-tank acetylene as L1 at the samples the standard reads, in arcing bursts
    L1, V, A3u = W.ROLE_UNIT["L1"], W.ROLE_UNIT["V"], W.ROLE_UNIT["A3"]
    assert [samples[i][1].date() for i in per[L1]] == [samples[i][1].date() for i in per[V]]
    r = rng(901)
    vi = per[V]
    keys = [samples[i][2] for i in vi]
    k_mar, k_jun, k_sep, k_lat = keys.index("2025-03"), keys.index("2025-06"), keys.index("2025-09"), \
        keys.index("2026-09")
    l1v = [rep[i]["C2H2"] for i in per[L1]]
    anchor = {k: float(l1v[k]) for k in (k_jun, k_sep, k_lat)}
    vdays = [samples[i][1].date() for i in vi]
    vops = [ops_between(V, a, b) for a, b in zip(vdays[:-1], vdays[1:])]
    vdd = [(b - a).days for a, b in zip(vdays[:-1], vdays[1:])]
    nfree = k_lat - k_sep
    total = round(anchor[k_lat] - anchor[k_sep], 1)
    fixed_inc = [anchor[k_jun] - 0.25, anchor[k_sep] - anchor[k_jun]]
    fixed_ops = vops[k_mar:k_sep]
    fixed_dd = vdd[k_mar:k_sep]
    free_ops = np.array(vops[k_sep:k_lat], float)
    free_dd = np.array(vdd[k_sep:k_lat], float)
    m26 = next(i for i in range(nfree) if vdays[k_sep + i] >= dt.date(2025, 12, 1))
    windows = [(True, slice(0, nfree)), (False, slice(0, nfree)), (False, slice(m26, nfree))]
    inc, score_v = _design_increments(total, nfree, fixed_inc, fixed_ops, free_ops, fixed_dd, free_dd, r,
                                      windows)
    lv = {}
    for k in range(k_mar + 1):
        lv[k] = 0.08
    lv[k_jun] = anchor[k_jun]
    lv[k_sep] = anchor[k_sep]
    run = anchor[k_sep]
    for m in range(nfree):
        run = round(run + inc[m], 1)
        lv[k_sep + 1 + m] = run
    assert abs(lv[k_lat] - anchor[k_lat]) < 1e-9
    arc_levels[V] = {samples[i][1]: max(0.0, lv[k] - 0.08) for k, i in enumerate(vi)}
    gen(V)
    for k, i in enumerate(vi):
        rep[i]["C2H2"] = _fmt_c2h2(lv[k]) if lv[k] >= 0.5 else "<0.5"

    # A3: internal arcing from January 2025, acetylene in bursts
    ai = per[A3u]
    akeys = [samples[i][2] for i in ai]
    a_dec, a_sep, a_lat = akeys.index("2024-12"), akeys.index("2025-09"), akeys.index("2026-09")
    adays = [samples[i][1].date() for i in ai]
    aops = np.array([ops_between(A3u, a, b) for a, b in zip(adays[:-1], adays[1:])], float)
    add = np.array([(b - a).days for a, b in zip(adays[:-1], adays[1:])], float)
    r = rng(902)
    pre_n = a_sep - a_dec
    pre_total = 3.1
    inc_pre, s1 = _design_increments(pre_total - 0.25, pre_n, [], [], aops[a_dec:a_sep], [], add[a_dec:a_sep], r,
                                     [(False, slice(0, pre_n))], tries=8000)
    post_n = a_lat - a_sep
    post_total = W.TUNED_INCREASE[A3u][1]
    windows = [(True, slice(0, post_n)), (False, slice(0, post_n))]
    inc_post, s2 = _design_increments(post_total, post_n, list(inc_pre), list(aops[a_dec:a_sep]),
                                      aops[a_sep:a_lat], list(add[a_dec:a_sep]), add[a_sep:a_lat], r, windows)
    alv = {k: 0.08 for k in range(a_dec + 1)}
    run = 0.25
    for m in range(pre_n):
        run = round(run + inc_pre[m], 1)
        alv[a_dec + 1 + m] = run
    for m in range(post_n):
        run = round(run + inc_post[m], 1)
        alv[a_sep + 1 + m] = run
    arc_levels[A3u] = {samples[i][1]: max(0.0, alv[k] - 0.08) for k, i in enumerate(ai)}
    gen(A3u)
    for k, i in enumerate(ai):
        rep[i]["C2H2"] = _fmt_c2h2(alv[k]) if alv[k] >= 0.5 else "<0.5"

    # hydrogen alongside the arcing acetylene: about twice it at V, about 1.6 times at A3
    for tid, h2_inc in ((V, 16), (A3u, 8)):
        b, l = sample_in(tid, "2025-09"), sample_in(tid, "2026-09")
        rep[l]["H2"] = str(int(rep[b]["H2"]) + h2_inc)
        prev = per[tid][per[tid].index(l) - 1]
        if int(rep[prev]["H2"]) > int(rep[l]["H2"]):
            rep[prev]["H2"] = str(int(rep[l]["H2"]) - 1)

    return {"samples": samples, "adates": adates, "rep": rep, "truth": truth, "per": per,
            "leak_k": leak_k, "thermal_rate": thermal_rate, "design_scores": (score_v, s1, s2),
            "params": params, "ops_between": ops_between}


# ---------------------------------------------------------------------------------------------
# finishing: rounding margins, moisture and oil temperature, re-issues, compartments
import standard as S   # noqa: E402


def bin_ok(v, places):
    f = (v * 10 ** places) % 1
    return (0.05 <= f <= 0.30) or (0.70 <= f <= 0.95)


def rows_from(R, ids=None):
    out = []
    for i, (tid, t, key) in enumerate(R["samples"]):
        if ids is not None and tid not in ids:
            continue
        d = dict(R["rep"][i])
        d.update(transformer_id=tid, sampled=t, date=R["adates"][i], sample_id=f"S{i:05d}", issue=1, _i=i)
        out.append(d)
    return out


def utc_index(H, t_local):
    aware = t_local.replace(tzinfo=W.TZ)
    u = aware.astimezone(W.UTC).replace(minute=0, second=0, microsecond=0)
    t0 = H["utc"][0].to_pydatetime()
    return int((u - t0).total_seconds() // 3600)


def tune_margins(R):
    """Every severity the CSV carries sits inside its two-decimal bin, no rate sits within 3 per cent
    of its limit and no latest level sits on a table value. Greedy: fix one violation at a time by
    moving one latest reading a few ppm, never changing the unit's code."""
    attributed = {W.ROLE_UNIT["L1"]: ("C2H2",), W.ROLE_UNIT["L2"]: ("C2H2",)}
    fixed = {W.ROLE_UNIT[k]: W.TUNED_INCREASE[W.ROLE_UNIT[k]][0] for k in ("V", "A3", "T1", "T2", "T3")}
    log = []
    for tid in W.IDS:
        ex = attributed.get(tid, ())
        lock = {fixed[tid], "H2"} if tid in fixed else set()
        lat_i = R["per"][tid][-1]

        def state():
            return S.code_unit(tid, rows_from(R, {tid}), exclude=ex)

        def violations(c, s, g, det):
            out = []
            if not bin_ok(s, 2) and g not in lock:
                out.append(g)
            for gg, rt in det["ratios"].items():
                if abs(rt - 1.0) < 0.03 and gg not in lock:
                    out.append(gg)
            bi = W.BANDS.index(det["band"])
            for gg in W.GASES:
                if gg in ex or gg in lock:
                    continue
                v = R["rep"][lat_i][gg]
                if str(v).startswith("<"):
                    continue
                v = float(v)
                for tab in (W.A1, W.A2):
                    if abs(v - tab[det["class"]][gg][bi]) < (0.15 if gg == "C2H2" else 1.5):
                        out.append(gg)
            return out

        c0, s0, g0, det0 = state()
        for _ in range(8):
            c, s, g, det = state()
            bad = violations(c, s, g, det)
            if not bad:
                break
            gas = bad[0]
            orig = R["rep"][lat_i][gas]
            if str(orig).startswith("<"):
                gas = "CO2"
                orig = R["rep"][lat_i][gas]
            if gas in lock:
                raise RuntimeError(f"{tid}: locked gas {gas} would move")
            fixed_one = False
            for dlt in (1, -1, 2, -2, 3, -3, 4, -4, 6, -6, 8, -8, 11, -11, 15, -15, 20, -20, 30, -30):
                R["rep"][lat_i][gas] = str(int(float(orig)) + dlt)
                c2, s2, g2, det2 = state()
                if c2 == c0 and len(violations(c2, s2, g2, det2)) < len(bad) and \
                        (tid not in fixed or (g2 == g and abs(s2 - s) < 1e-12)):
                    log.append((tid, gas, orig, R["rep"][lat_i][gas], round(s, 4), round(s2, 4)))
                    fixed_one = True
                    break
                R["rep"][lat_i][gas] = orig
            if not fixed_one:
                raise RuntimeError(f"no margin for {tid}: {bad} {s}")
        c, s, g, det = state()
        if violations(c, s, g, det):
            raise RuntimeError(f"margins not reached for {tid}")
    return log


def moisture_and_temps(R, H):
    """Moisture follows each unit's relative saturation at the oil temperature of the moment; the
    technician writes the top-oil gauge reading on the label, or leaves it blank."""
    r = rng(500)
    samples = R["samples"]
    proc = {tid: dt.datetime.combine(d, dt.time(12)) for tid, d, n in W.OIL_PROCESSING}
    latest = {tid: R["per"][tid][-1] for tid in W.IDS}
    temps, moist, written = [None] * len(samples), [None] * len(samples), [None] * len(samples)
    for i, (tid, t, key) in enumerate(samples):
        j = W.IDS.index(tid)
        T = float(H["top"][utc_index(H, t), j])
        temps[i] = T
        u = W.UNIT[tid]
        yrs = years(t)
        rs = u["rs"] * (1 + 0.07 * math.sin(2 * math.pi * (yrs - 0.3))) * (1 + r.normal(0, 0.03))
        if tid in proc and t > proc[tid]:
            k = 1 - math.exp(-((t - proc[tid]).total_seconds() / (365.25 * 86400)) / 1.6)
            rs = rs * (0.32 + 0.68 * k)
        m = rs / 100.0 * ws(T)
        moist[i] = max(2, int(round(m)))
        w = round((T + r.normal(0, 0.35)) * 2) / 2
        blank = r.random() < 0.09
        if i == latest[tid]:
            blank = tid in W.BLANK_TEMP_LATEST
        written[i] = None if blank else w
    R["oil_temp"] = written
    R["moisture"] = moist
    R["true_temp"] = temps
    return R


def rs_of(R, H, i, temp=None, moisture=None):
    tid, t, _ = R["samples"][i]
    T = temp if temp is not None else R["oil_temp"][i]
    if T is None:
        T = round(float(H["top"][utc_index(H, t), W.IDS.index(tid)]), 1)
    m = moisture if moisture is not None else R["moisture"][i]
    return m / ws(T) * 100.0


def tune_latest_rs(R, H):
    """Latest samples land on their unit's relative saturation, inside the one-decimal bin and at
    least half a point from 30 per cent."""
    log = []
    for tid in W.IDS:
        i = R["per"][tid][-1]
        tgt = W.UNIT[tid]["rs"]
        tl, j = R["samples"][i][1], W.IDS.index(tid)
        hi = utc_index(H, tl)
        T = R["oil_temp"][i]
        Tuse = T if T is not None else round(float(H["top"][hi, j]), 1)
        best = None
        for dm in range(-6, 7):
            m0 = int(round(tgt / 100 * ws(Tuse))) + dm
            for dT in ([0.0, 0.5, -0.5, 1.0, -1.0] if T is not None else
                       [0.0, 0.1, -0.1, 0.2, -0.2, 0.3, -0.3, 0.4, -0.4]):
                T2 = Tuse + dT
                v = m0 / ws(T2) * 100
                if not bin_ok(v, 1) or abs(v - 30.0) < 0.5:
                    continue
                score = abs(v - tgt) + 0.3 * abs(dT)
                if best is None or score < best[0]:
                    best = (score, m0, T2, v)
        _, m0, T2, v = best
        R["moisture"][i] = m0
        if T is not None:
            R["oil_temp"][i] = T2
        else:
            H["top"][hi, j] = T2
        log.append((tid, m0, T2, round(v, 3)))
    return log


def apply_reissues(R, H):
    """A corrected report keeps the sample ID and report number and takes the next issue."""
    out = []
    for tid, key, field, how, _ in W.REISSUES:
        i = next(k for k in R["per"][tid] if R["samples"][k][2] == key)
        if field == "moisture_ppm":
            m2 = R["moisture"][i]
            if how == "low":
                v2 = rs_of(R, H, i)
                m1 = m2
                while rs_of(R, H, i, moisture=m1) > 29.2:
                    m1 -= 1
            else:
                m1 = m2 + 6
            out.append((i, field, m1, m2))
        else:
            t2 = R["oil_temp"][i]
            if t2 is None:
                t2 = round(R["true_temp"][i] * 2) / 2
                R["oil_temp"][i] = t2
            if how == "blank":
                t1 = None
            else:
                whole = int(t2)
                a, b = divmod(whole, 10)
                t1 = float(b * 10 + a) + (t2 - whole) if a != b and b != 0 else t2 + 10.0
            out.append((i, field, t1, t2))
    R["reissues"] = out
    return out


def compartments(R, dlist, ops, cnt):
    """Diverter-compartment oil, sampled at the March visit to every in-oil tap changer. Gas builds
    with the operations since the compartment oil was last changed (at a service)."""
    r = rng(700)
    iday = {d: k for k, d in enumerate(dlist)}
    rows = []
    for i, (tid, t, key) in enumerate(R["samples"]):
        if tid not in W.IN_OIL or not key.endswith("-03"):
            continue
        j = W.IDS.index(tid)
        svcs = [d for d, _ in W.OLTC_SERVICES.get(tid, []) if d < t.date()]
        last = max(svcs) if svcs else dt.date(2017, 3, 1)
        if last >= W.START:
            n_ops = int(ops[iday[last]:iday[t.date()], j].sum())
        else:
            n_ops = int(ops[:iday[t.date()], j].sum()) + int(W.UNIT[tid]["ops"] * (W.START - last).days) \
                if W.UNIT[tid]["ops"] else int(ops[:iday[t.date()], j].sum()) + 11000 * (W.START - last).days // 365
        c2h2 = 9500 * (1 - math.exp(-n_ops / 42000.0))
        v = {"C2H2": c2h2, "H2": 0.17 * c2h2, "C2H4": 0.33 * c2h2, "CH4": 0.12 * c2h2,
             "C2H6": 0.025 * c2h2, "CO": 110 + 0.004 * n_ops, "CO2": 1700 + 0.045 * n_ops,
             "O2": r.uniform(17000, 22500), "N2": r.uniform(50000, 58000)}
        rep = {}
        for g in GAS_ALL:
            x = v[g] * (1 + r.normal(0, 0.04))
            if g == "C2H2":
                rep[g] = str(int(round(x)))
            else:
                rep[g] = str(int(round(x)))
        tt = t + dt.timedelta(minutes=int(r.integers(6, 14)))
        rows.append({"tid": tid, "sampled": tt, "rep": rep, "moisture": int(round(r.uniform(18, 41))),
                     "main_i": i})
    return rows
