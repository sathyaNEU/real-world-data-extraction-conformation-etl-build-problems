"""The clean truth of task134 architecture 4, generated from one seed before any file is written.

Physics: a dredged part's bed relaxes toward the natural bed beside it at rate k * (held depth - natural depth); the
port holds each part at its maintained depth, so the part's yearly in-situ maintenance is k * (held - natural) * area
times that year's storminess. The disused North Quay Berth 2 has relaxed freely since March 2019.
"""
import datetime as dt
import math

import numpy as np

import geo
import params as P


def month_iter(y0, m0, y1, m1):
    y, m = y0, m0
    while (y, m) <= (y1, m1):
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def licence_year(y, m):
    return y if m >= 10 else y - 1


class World:
    pass


def nat_bed(s, t):
    """Natural bed depth below CD at chainage s, offset t (side by the sign of t), blended across part boundaries."""
    s = np.asarray(s, float)
    t = np.asarray(t, float)
    north = t > 0
    vals = []
    bounds = []
    for code, name, c0, c1, half, nn, ns, k in P.PARTS:
        vals.append((nn, ns))
        bounds.append((c0, c1))
    out = np.zeros(s.shape)
    # piecewise constant by part with 150 m linear blends centred on each internal boundary
    for i, (c0, c1) in enumerate(bounds):
        nn, ns = vals[i]
        v = np.where(north, nn, ns)
        lo = -1e9 if i == 0 else c0
        hi = 1e9 if i == len(bounds) - 1 else c1
        out = np.where((s >= lo) & (s < hi), v, out)
    for i in range(len(bounds) - 1):
        b = bounds[i][1]
        a_nn, a_ns = vals[i]
        c_nn, c_ns = vals[i + 1]
        w = np.clip((s - (b - 0.15)) / 0.30, 0.0, 1.0)
        inb = (s > b - 0.15) & (s < b + 0.15)
        va = np.where(north, a_nn, a_ns)
        vc = np.where(north, c_nn, c_ns)
        out = np.where(inb, va + (vc - va) * w, out)
    return out


def relief(E, N, ph):
    E = np.asarray(E, float)
    N = np.asarray(N, float)
    return 0.10 * (np.sin(E / 317.0 + ph[0]) * np.sin(N / 281.0 + ph[1]) + 0.6 * np.sin((E + N) / 523.0 + ph[2])
                   + 0.4 * np.sin((E - 0.6 * N) / 211.0 + ph[3]))


def years_between(d0, d1):
    return (d1 - d0).days / 365.25


def coverage(spacing):
    """Grid points (E, N) on the OSGB grid at the given spacing inside the survey coverage, with their (s, t)."""
    Emin, Emax = 642000.0, 653100.0
    Nmin, Nmax = 295500.0, 299900.0
    xs = np.arange(math.ceil(Emin / spacing) * spacing, Emax, spacing)
    ys = np.arange(math.ceil(Nmin / spacing) * spacing, Nmax, spacing)
    EE, NN = np.meshgrid(xs, ys)
    E, N = EE.ravel(), NN.ravel()
    s, t = geo.chain_offset(E, N)
    keep = np.zeros(E.shape, bool)
    for code, name, c0, c1, half, nn, ns, k in P.PARTS:
        if code == "TB":
            continue
        lo = c0
        keep |= (s >= lo) & (s < c1) & (np.abs(t) <= half + P.MARGIN)
    keep |= (s >= 9.40) & (s <= 10.20) & (t >= -210.0 - P.MARGIN) & (t <= 250.0)
    keep |= (s > 10.20) & (s <= 10.255) & (np.abs(t) <= 165.0)
    return E[keep], N[keep], s[keep], t[keep]


def classify(s, t):
    """Area code for each point: a part code, a berth code, 'SLOPE', 'MARGIN:<part>', 'QUAY' (no data)."""
    out = np.empty(s.shape, dtype=object)
    out[:] = "MARGIN"
    for code, name, c0, c1, half, nn, ns, k in P.PARTS:
        if code == "TB":
            m = (s >= c0) & (s <= c1) & (np.abs(t) <= half)
        else:
            m = (s >= c0) & (s < c1) & (np.abs(t) <= half)
        out[m] = code
    for code, name, s0, s1, t0, t1, depth, nat, k in P.BERTHS:
        m = (s >= s0) & (s <= s1) & (t > t0) & (t <= t1)
        out[m] = code
    quay = (s >= 9.40) & (s <= 10.20) & (t > 210.0) & (out == "MARGIN")
    out[quay] = "QUAY"
    return out


def make():
    W = World()
    rng = np.random.default_rng(P.SEED)
    W.rng_seed = P.SEED
    part = {p[0]: dict(code=p[0], name=p[1], c0=p[2], c1=p[3], half=p[4], nat_n=p[5], nat_s=p[6], k=p[7]) for p in P.PARTS}
    for c, d in part.items():
        d["nat"] = d["nat_s"] if c == "TB" else 0.5 * (d["nat_n"] + d["nat_s"])
        d["area"] = (d["c1"] - d["c0"]) * 1000.0 * 2.0 * d["half"]
        d["held"] = P.DEPTH_NOW
    berth = {b[0]: dict(code=b[0], name=b[1], s0=b[2], s1=b[3], t0=b[4], t1=b[5], held=b[6], nat=b[7], k=b[8]) for b in P.BERTHS}
    for c, d in berth.items():
        d["area"] = (d["s1"] - d["s0"]) * 1000.0 * (d["t1"] - d["t0"])
    W.part, W.berth = part, berth
    # in-situ dry density (t/m3) and dry-solids fraction by mass of the material in each area
    W.dry_density = {"OC": 0.630, "FR": 0.585, "MR": 0.505, "IR": 0.455, "TB": 0.425, "NQ1": 0.400, "NQ2": 0.400,
                     "NQ3": 0.405, "CT5": 0.395}

    # storminess by licence year (2015-16 covers April to September 2016) and part noise
    years = list(range(2015, P.LY_LAST + 1))
    storm = {y: 1.0 + P.STORM_SD * rng.standard_normal() for y in years}
    W.storm = storm
    areas = list(part) + list(berth)
    pnoise = {(a, y): P.PART_SD * rng.standard_normal() for a in areas for y in years}
    mnoise_sd = 0.05
    monthly = {}      # (area, y, m) -> in-situ m3
    for y, m in month_iter(2016, 4, 2026, 9):
        ly = licence_year(y, m)
        for a in areas:
            if a in part:
                d = part[a]
                rate = d["k"] * (d["held"] - d["nat"]) * d["area"]
            else:
                d = berth[a]
                if a == "NQ2":
                    if dt.date(y, m, 1) > dt.date(2019, 3, 1):
                        continue
                    held = 12.8
                else:
                    held = d["held"]
                rate = d["k"] * (held - d["nat"]) * d["area"]
            v = rate * storm[ly] * (1.0 + pnoise[(a, ly)]) * P.MONTH_WEIGHTS[m] * (1.0 + mnoise_sd * rng.standard_normal())
            monthly[(a, y, m)] = v
    W.monthly = monthly

    # survey surfaces
    ph = rng.uniform(0, 2 * math.pi, 4)
    W.relief_phase = ph
    surveys = []
    for contractor, dates, spacing, noise in (("A", P.SURVEY_A_DATES, P.GRID_A, 0.06), ("B", P.SURVEY_B_DATES, P.GRID_B, 0.04)):
        E, N, s, t = coverage(spacing)
        cls = classify(s, t)
        nat = nat_bed(s, t)
        for code, name, s0, s1, t0, t1, depth, natb, k in P.BERTHS:
            pass
        base_relief = relief(E, N, ph)
        for d in dates:
            seas = 0.03 if d.month == 10 else -0.03
            z = np.empty(E.shape)
            z[:] = np.nan
            # natural margins and slopes
            for code in P.REACHES:
                dd = part[code]
                inpart = (s >= dd["c0"]) & (s < dd["c1"])
                at = np.abs(t)
                od = P.DEPTH_NOW - nat
                toe = dd["half"] + P.SLOPE * od
                chan = inpart & (at <= dd["half"])
                slope = inpart & (at > dd["half"]) & (at < toe)
                marg = inpart & (at >= toe)
                z = np.where(chan, P.DEPTH_NOW + 0.10 * rng.standard_normal(E.shape), z)
                frac = np.clip((at - dd["half"]) / np.maximum(toe - dd["half"], 1e-6), 0, 1)
                z = np.where(slope, P.DEPTH_NOW - frac * od, z)
                z = np.where(marg, nat + base_relief + seas, z)
            # basin, its south slope and margin
            inb = (s >= 9.40) & (s <= 10.20)
            od_tb = P.DEPTH_NOW - part["TB"]["nat"]
            toe_tb = 210.0 + P.SLOPE * od_tb
            z = np.where(inb & (np.abs(t) <= 210.0), P.DEPTH_NOW + 0.10 * rng.standard_normal(E.shape), z)
            sl = inb & (t < -210.0) & (t > -toe_tb)
            frac = np.clip((-t - 210.0) / (toe_tb - 210.0), 0, 1)
            z = np.where(sl, P.DEPTH_NOW - frac * od_tb, z)
            z = np.where(inb & (t <= -toe_tb), part["TB"]["nat"] + base_relief + seas, z)
            # berths
            for code, name, s0, s1, t0, t1, depth, natb, k in P.BERTHS:
                m = cls == code
                if code == "NQ2":
                    if d <= P.NQ2_LAST_DREDGED:
                        lev = 12.8 + 0.10 * rng.standard_normal(E.shape)
                    else:
                        yrs = years_between(P.NQ2_LAST_DREDGED, d)
                        lev = natb + (P.NQ2_LAST_DEPTH - natb) * math.exp(-k * yrs) + 0.08 * rng.standard_normal(E.shape)
                else:
                    lev = depth + 0.10 * rng.standard_normal(E.shape)
                z = np.where(m, lev, z)
            quay = cls == "QUAY"
            z = np.where(quay, np.nan, z)
            z = z + noise * rng.standard_normal(E.shape)
            z = np.where(quay, np.nan, z)
            surveys.append(dict(contractor=contractor, date=d, E=E, N=N, s=s, t=t, cls=cls, depth=z))
    W.surveys = surveys
    make_distractors(W, rng)
    tune_asks(W)
    return W


def placed_dry_solids(W):
    """{(site, quarter, campaign, area): dry solids placed} over the licence year 2025-26, by the UK civil date of placement."""
    out = {}
    for r in W.loads:
        tl = r["t_dump"] + dt.timedelta(hours=uk_offset_hours(r["t_dump"]))
        if not (dt.datetime(2025, 10, 1) <= tl < dt.datetime(2026, 10, 1)):
            continue
        q = {10: 1, 11: 1, 12: 1, 1: 2, 2: 2, 3: 2, 4: 3, 5: 3, 6: 3, 7: 4, 8: 4, 9: 4}[tl.month]
        camp = 2026 if (tl.year, tl.month) >= (2026, 4) else 2025
        k = (r["site"], q, camp, r["area"])
        out[k] = out.get(k, 0.0) + r["tds_true"]
    return out


def ask_a_truth(W, fractions=None):
    fr = W.ds_summary if fractions is None else fractions
    out = {}
    for (site, q, camp, area), tds in placed_dry_solids(W).items():
        out[(site, q)] = out.get((site, q), 0.0) + tds / fr[(camp, area)]
    return out


def ask_b_truth(W):
    groups = {}
    byref = {x["ref"]: x for x in W.samples}
    for x in W.samples:
        if x["qa"] or x["part"] not in P.DEEPENED:
            continue
        v = {k: x["rep"][k] for k in ("Cd", "Hg", "Pb", "Cu")}
        dup = [q for q in W.samples if q["qa"] and q["primary"] == x["ref"]]
        if dup:
            v = {k: 0.5 * (v[k] + dup[0]["rep"][k]) for k in v}
        groups.setdefault(x["part"], []).append(v)
    return {(p, k): float(np.mean([v[k] for v in vs])) for p, vs in groups.items() for k in ("Cd", "Hg", "Pb", "Cu")}


def edge_distance(v, unit):
    r = v - round(v / unit) * unit
    return unit / 2.0 - abs(r)


def tune_asks(W):
    """The ask layers' own random streams, then two realistic free parameters set so every ask figure sits well inside
    its rounding bin: each channel area's sediment dry-solids level in the 2025 and the 2026 campaigns (within 0.8
    percentage points of its density-based value, the order seaward to landward kept), chosen by a fixed-seed search so
    every placement total clears its 1,000 t edge under the printed area summary and, for April to September 2026,
    under the licence 5.5 recomputation from the laboratory's values at full precision; and a metal mean within 0.0015
    of the 0.005 line has one sample's reported value moved by one reporting step."""
    make_loads(W, np.random.default_rng(P.SEED + 1000))
    make_sampling(W, np.random.default_rng(P.SEED + 2000))
    W.nudges = []
    srch = np.random.default_rng(P.SEED + 4000)
    placed = placed_dry_solids(W)

    def cells(fr, quarters):
        out = {}
        for (site, q, camp, area), tds in placed.items():
            if q in quarters:
                out[(site, q)] = out.get((site, q), 0.0) + tds / fr[(camp, area)]
        return out
    # 2025: the printed summary is the only reading (the campaign's results do not ship)
    best = None
    for i in range(4000):
        off = {a: 0.001 * int(srch.integers(-8, 9)) if i else 0.0 for a in CHANNEL5}
        fr = dict(W.ds_summary)
        for a in CHANNEL5:
            fr[(2025, a)] = round(W.ds_base_2025[a] + off[a], 3)
        if not all(fr[(2025, x)] > fr[(2025, y)] for x, y in zip(CHANNEL5, CHANNEL5[1:])):
            continue
        c = cells(fr, (1, 2))
        if any(round(v / 1000.0) % 10 == 0 for v in c.values()):
            continue                                       # no return reads as a round figure
        score = min(edge_distance(v, 1000.0) for v in c.values())
        key = (round(score, 6), -round(sum(abs(v) for v in off.values()), 6))
        if best is None or key > best[0]:
            best = (key, off, fr)
    W.ds_off_2025 = best[1]
    W.ds_summary = best[2]
    # 2026: the printed summary and the 5.5 recomputation at full precision, no area mean near a rounding midpoint
    pairs = ds_pairs(W)
    best = None
    for i in range(4000):
        off = {a: 0.0002 * int(srch.integers(-40, 41)) if i else 0.0 for a in CHANNEL5}
        full = {a: ds55_from(pairs[a], off.get(a, 0.0)) for a in AREAS8}
        prn = {a: round(full[a], 3) for a in AREAS8}
        if not all(prn[x] > prn[y] for x, y in zip(CHANNEL5, CHANNEL5[1:])):
            continue
        if any(abs(full[a] - prn[a]) > 0.0004 for a in AREAS8):
            continue
        fa, fb = dict(W.ds_summary), dict(W.ds_summary)
        for a in AREAS8:
            fa[(2026, a)], fb[(2026, a)] = prn[a], full[a]
        ca, cb = cells(fa, (3, 4)), cells(fb, (3, 4))
        if any(round(ca[k] / 1000.0) != round(cb[k] / 1000.0) for k in ca):
            continue
        if any(round(v / 1000.0) % 10 == 0 for v in ca.values()):
            continue
        score = min(min(edge_distance(ca[k], 1000.0), edge_distance(cb[k], 1000.0)) for k in ca)
        key = (round(score, 6), -round(sum(abs(v) for v in off.values()), 6))
        if best is None or key > best[0]:
            best = (key, off, prn)
    if best is None:
        raise SystemExit("no 2026 dry-solids level clears every placement edge")
    W.ds_off_2026 = best[1]
    for x in W.samples:
        o = best[1].get(x["part"], 0.0)
        x["vals"]["DS"] = x["vals"]["DS"] + 100.0 * o
        x["rep"]["DS"] = round(x["vals"]["DS"], 1)
    for a in AREAS8:
        W.ds_summary[(2026, a)] = round(ds55(W, a), 3)
        assert W.ds_summary[(2026, a)] == best[2][a]
    for _ in range(200):
        b = ask_b_truth(W)
        bad = [(k, v) for k, v in sorted(b.items()) if edge_distance(v, 0.01) < 0.0015]
        if not bad:
            break
        (part, det), v = bad[0]
        step = 0.001 if det in ("Cd", "Hg") else 0.01
        prim = [x for x in W.samples if not x["qa"] and x["part"] == part and not any(q["qa"] and q["primary"] == x["ref"] for q in W.samples)]
        x = prim[0]
        n = len([s for s in W.samples if not s["qa"] and s["part"] == part])
        r = v - round(v / 0.01) * 0.01
        x["rep"][det] = round(x["rep"][det] + (step if r < 0 else -step) * max(1, int(round(0.004 * n / step))), 3)
        W.nudges.append(("sample", x["ref"], det))
    else:
        raise SystemExit("metal means not clear of their edges")


def ddm_to_deg(d, m):
    return d + m / 60.0


def site_box(code):
    pts = P.SITES[code][1]
    lats = [ddm_to_deg(p[0], p[1]) for p in pts]
    lons = [ddm_to_deg(p[2], p[3]) for p in pts]
    return min(lats), max(lats), min(lons), max(lons)


def uk_offset_hours(t_utc):
    """BST (UTC+1) from 01:00 UTC on the last Sunday of March to 01:00 UTC on the last Sunday of October."""
    y = t_utc.year

    def last_sunday(month):
        d = dt.datetime(y, month, 31 if month in (3, 10) else 30)
        while d.weekday() != 6:
            d -= dt.timedelta(days=1)
        return d.replace(hour=1)
    return 1 if last_sunday(3) <= t_utc < last_sunday(10) else 0


def make_loads(W, rng):
    """Every hopper load from October 2023 to September 2026, consistent with the monthly returns' dry solids."""
    areas = ["OC", "FR", "MR", "IR", "TB", "NQ1", "NQ3", "CT5"]
    loads = []
    tds_month = {}     # (area, y, m) -> true dry solids (t), the returns' basis
    hire0, hire1 = dt.datetime(*P.HIRE_FROM), dt.datetime(*P.HIRE_TO) + dt.timedelta(days=1)
    fault0, fault1 = dt.datetime(*P.GAUGE_FAULT_FROM), dt.datetime(*P.GAUGE_FAULT_TO) + dt.timedelta(days=1)
    # weather diversion days, drawn once
    start = dt.date(2023, 10, 1)
    days = [start + dt.timedelta(days=i) for i in range((dt.date(2026, 9, 30) - start).days + 1)]
    divert_to_fs = {d for d in days if rng.random() < 0.10}
    divert_to_wd = {d for d in days if rng.random() < 0.07}
    W.divert_to_fs, W.divert_to_wd = divert_to_fs, divert_to_wd
    for y, m in month_iter(2023, 10, 2026, 9):
        ndays = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.date(y, m, 1)).days
        for a in areas:
            v = W.monthly[(a, y, m)]
            tds = v * W.dry_density[a] * (1.0 + 0.01 * rng.standard_normal())
            n = max(1, int(round(tds / P.LOAD_TDS)))
            w = rng.dirichlet(np.full(n, 30.0))
            parts = tds * w
            for i in range(n):
                day = int(rng.integers(0, ndays))
                minute = int(rng.integers(0, 24 * 60))
                t0 = dt.datetime(y, m, 1) + dt.timedelta(days=day, minutes=minute)
                loads.append(dict(area=a, t_load=t0, tds_true=float(parts[i])))
    loads.sort(key=lambda r: (r["t_load"], r["area"]))
    # space the loads so one vessel never loads twice within 2.6 hours
    last = None
    for r in loads:
        if last is not None and r["t_load"] < last + dt.timedelta(hours=2.6):
            r["t_load"] = last + dt.timedelta(hours=2.6, minutes=int(rng.integers(0, 50)))
        last = r["t_load"]
    for r in loads:
        a = r["area"]
        hired = hire0 <= r["t_load"] < hire1
        r["vessel"] = P.HIRED if hired else P.DREDGER
        dur = dt.timedelta(minutes=int(rng.integers(55, 100)))
        route = P.ROUTE[a]
        local_day = (r["t_load"] + dt.timedelta(hours=uk_offset_hours(r["t_load"]))).date()
        site = route
        if r["t_load"].month in P.FS_CLOSED_MONTHS:
            site = "WD"
        elif route == "WD" and local_day in divert_to_fs:
            site = "FS"
        elif route == "FS" and local_day in divert_to_wd:
            site = "WD"
        sail = dt.timedelta(minutes=int(rng.integers(22, 40))) if site == "FS" else dt.timedelta(minutes=int(rng.integers(64, 88)))
        r["route"], r["site"] = route, site
        r["t_dump"] = r["t_load"] + dur + sail
        la0, la1, lo0, lo1 = site_box(site)
        r["lat"] = float(rng.uniform(la0 + 0.0008, la1 - 0.0008))
        r["lon"] = float(rng.uniform(lo0 + 0.0010, lo1 - 0.0010))
        if hired:
            vh = float(int(rng.integers(2950, 3360)))
            rho_m = round(P.RHO_W + r["tds_true"] * (P.RHO_S - P.RHO_W) / (vh * P.RHO_S), 3)
            r["hopper_m3"], r["rho_m"] = vh, rho_m
            r["tds_logged"] = None
            r["tds_true"] = vh * P.RHO_S * (rho_m - P.RHO_W) / (P.RHO_S - P.RHO_W)
        else:
            r["hopper_m3"] = float(int(rng.integers(2380, 2600)))
            r["rho_m"] = None
            tt = round(r["tds_true"])
            r["tds_true"] = float(tt)
            faulty = fault0 <= r["t_load"] < fault1
            r["tds_logged"] = float(round(tt * P.GAUGE_FACTOR)) if faulty else float(tt)
            r["fault"] = faulty
        key = (a, r["t_load"].year, r["t_load"].month)
        tds_month[key] = tds_month.get(key, 0.0) + (r["tds_true"])
    # loads working through midnight at the quarter ends (dumps in the last hour of the day in UTC, the next day local)
    for (y, m, d, n) in ((2025, 9, 30, 2), (2026, 3, 31, 2), (2026, 6, 30, 2), (2026, 9, 30, 1)):
        cand = [r for r in loads if r["t_load"].date() == dt.date(y, m, d) and r["vessel"] == P.DREDGER]
        if len(cand) < n:
            base = [r for r in loads if abs((r["t_load"].date() - dt.date(y, m, d)).days) <= 3 and r["vessel"] == P.DREDGER]
            cand = (cand + base)[:n]
        for i, r in enumerate(cand[:n]):
            dump = dt.datetime(y, m, d, 23, 12 + 21 * i)
            r["t_load"] = dump - dt.timedelta(minutes=125 if r["site"] == "WD" else 80)
            r["t_dump"] = dump
    loads.sort(key=lambda r: r["t_load"])
    # contractor's day-trip references (local calendar day, in loading order) for the Fend Endeavour
    seq = {}
    for i, r in enumerate(loads):
        ly = licence_year(r["t_load"].year, r["t_load"].month)
        r["load_ref"] = None
        if r["vessel"] == P.DREDGER:
            ld = (r["t_load"] + dt.timedelta(hours=uk_offset_hours(r["t_load"]))).date()
            seq[ld] = seq.get(ld, 0) + 1
            r["trip_ref"] = "FE%s/%d" % (ld.strftime("%y%m%d"), seq[ld])
    counters = {}
    for r in loads:
        ly = licence_year(r["t_load"].year, r["t_load"].month)
        # aborted loadings (a pump trip, a broken drag-head) take a number and are never dumped
        counters[ly] = counters.get(ly, 0) + (2 if rng.random() < 0.025 else 1)
        r["load_ref"] = "DDL-%02d%02d-%05d" % (ly % 100, (ly + 1) % 100, counters[ly])
    W.loads = loads
    W.tds_month = tds_month


def reported(vals):
    """Values as the laboratory reports them: cadmium and mercury to 0.001 mg/kg, the other metals to 0.01, dry solids 0.1 per cent."""
    out = {}
    for k, v in vals.items():
        out[k] = round(v, 3) if k in ("Cd", "Hg") else (round(v, 1) if k == "DS" else round(v, 2))
    return out


def make_sampling(W, rng):
    """Annual sediment sampling: the 2025 and 2026 campaigns' area summaries, the 2026 samples and lab results."""
    stations = []
    plan = {"OC": [0.45, 0.95, 1.40, 1.90, 2.40], "FR": [2.85, 3.35, 3.85, 4.40, 4.95], "MR": [5.30, 5.85, 6.40, 6.95, 7.50],
            "IR": [7.82, 8.30, 8.80, 9.25], "TB": [9.47, 9.70, 9.95, 10.12]}
    for code, ss in plan.items():
        half = geo.half_width(code)
        for i, s in enumerate(ss):
            t = float(rng.uniform(-0.6, 0.6) * half)
            E, N = geo.point_at(s, t)
            stations.append(dict(station="%s-%02d" % (code, i + 1), part=code, s=s, t=t, E=round(E, 1), N=round(N, 1)))
    for code, name, s0, s1, t0, t1, depth, nat, k in P.BERTHS:
        if depth is None:
            continue
        s = 0.5 * (s0 + s1)
        t = 0.5 * (t0 + t1)
        E, N = geo.point_at(s, t)
        stations.append(dict(station="%s-01" % code, part=code, s=s, t=t, E=round(E, 1), N=round(N, 1)))
    W.stations = stations
    # 2026 positions: three stations moved off obstructions into the neighbouring part
    moved = {"OC-05": 2.68, "FR-05": 5.28, "IR-01": 7.56, "TB-01": 9.33}
    W.moved = moved

    def conc(s, kind):
        base = {"Cd": (0.170, 0.300), "Hg": (0.110, 0.260), "Pb": (21.0, 38.0), "Cu": (13.5, 25.5)}[kind]
        x = min(max(s, 0.0), 10.25) / 10.25
        return base[0] + base[1] * x ** 1.3
    samples = []
    d0 = dt.datetime(*P.SAMPLING[2026][0], 8, 10)
    t = d0
    for st in stations:
        s_act = moved.get(st["station"], st["s"])
        if st["station"] in moved:
            half = geo.half_width(geo.part_at(s_act))
            t_off = float(rng.uniform(-0.5, 0.5) * half)
            E, N = geo.point_at(s_act, t_off)
        else:
            E, N = st["E"], st["N"]
        t = t + dt.timedelta(minutes=int(rng.integers(18, 34)))
        if t.hour >= 17:
            t = (t + dt.timedelta(days=1)).replace(hour=8, minute=int(rng.integers(5, 25)))
        vals = {k: conc(s_act, k) * float(np.exp(0.10 * rng.standard_normal())) for k in ("Cd", "Hg", "Pb", "Cu")}
        vals["Zn"] = 62.0 + 70.0 * (s_act / 10.25) ** 1.2 * float(np.exp(0.08 * rng.standard_normal()))
        vals["As"] = 11.0 + 6.0 * (s_act / 10.25) * float(np.exp(0.08 * rng.standard_normal()))
        vals["Cr"] = 38.0 + 22.0 * (s_act / 10.25) * float(np.exp(0.07 * rng.standard_normal()))
        vals["Ni"] = 21.0 + 9.0 * (s_act / 10.25) * float(np.exp(0.07 * rng.standard_normal()))
        part_act = geo.part_at(s_act) if st["part"] in P.DEEPENED else st["part"]
        rho_d = W.dry_density[part_act] * float(np.exp(0.02 * rng.standard_normal()))
        rho_b = P.RHO_W + rho_d * (1 - P.RHO_W / P.RHO_S)
        vals["DS"] = 100.0 * rho_d / rho_b
        samples.append(dict(ref="FEN26-%s" % st["station"], station=st["station"], qa=False, t=t, E=round(float(E), 1),
                            N=round(float(N), 1), s=s_act, part=part_act, vals=vals, rep=reported(vals)))
    # field duplicates
    dup_of = {"FEN26-QA1": "FEN26-OC-03", "FEN26-QA2": "FEN26-MR-02", "FEN26-QA3": "FEN26-IR-03", "FEN26-QA4": "FEN26-TB-03"}
    byref = {x["ref"]: x for x in samples}
    for qa, prim in dup_of.items():
        p = byref[prim]
        v = {k: x * float(np.exp(0.08 * rng.standard_normal())) for k, x in p["vals"].items()}
        samples.append(dict(ref=qa, station="QA", qa=True, primary=prim, t=p["t"] + dt.timedelta(minutes=int(rng.integers(2, 6))),
                            E=round(p["E"] + float(rng.uniform(-4, 4)), 1), N=round(p["N"] + float(rng.uniform(-4, 4)), 1),
                            s=p["s"], part=p["part"], vals=v, rep=reported(v)))
    W.samples = samples
    W.dup_of = dup_of
    # area dry-solids fractions by campaign: 2025 as the campaign reported it (its results do not ship), 2026 as licence
    # 5.5 reports it from the laboratory's values, each sample in the area it was taken in and each field duplicate
    # averaged with its primary first, printed to three decimals
    base25 = {}
    for yr in (2025, 2026):
        for a in AREAS8:
            if yr == 2026:
                continue
            rho_d = W.dry_density[a] * float(np.exp(0.015 * rng.standard_normal()))
            f = rho_d / (P.RHO_W + rho_d * (1 - P.RHO_W / P.RHO_S))
            base25[a] = round(f, 3)
    W.ds_base_2025 = base25
    W.ds_summary = {(2025, a): base25[a] for a in AREAS8}
    W.ds_summary.update({(2026, a): round(ds55(W, a), 3) for a in AREAS8})


AREAS8 = ["OC", "FR", "MR", "IR", "TB", "NQ1", "NQ3", "CT5"]
CHANNEL5 = ["OC", "FR", "MR", "IR", "TB"]


def ds_pairs(W):
    """{area: [(primary's dry solids per cent, its field duplicate's or None)]} for the 2026 samples, by the area each
    sample was taken in."""
    dups = {q["primary"]: q for q in W.samples if q["qa"]}
    out = {}
    for x in W.samples:
        if x["qa"]:
            continue
        d = dups.get(x["ref"])
        out.setdefault(x["part"], []).append((x["vals"]["DS"], None if d is None else d["vals"]["DS"]))
    return out


def ds55_from(pairs, off=0.0):
    vals = []
    for prim, dup in pairs:
        v = round(prim + 100.0 * off, 1)
        if dup is not None:
            v = 0.5 * (v + round(dup + 100.0 * off, 1))
        vals.append(v)
    return float(np.mean(vals)) / 100.0


def ds55(W, area, off=0.0):
    """An area's 2026 dry-solids fraction by licence 5.5 at full precision: each sample in the area it was taken in, a
    field duplicate averaged with its primary, the laboratory's reported per cent; off shifts the area's dry-solids
    level (a fraction) before the laboratory reports it."""
    return ds55_from(ds_pairs(W)[area], off)


def make_distractors(W, rng):
    # hourly tide gauge, GMT
    t0 = dt.datetime(2016, 1, 1)
    n = int(((dt.datetime(2027, 1, 1) - t0).total_seconds()) // 3600)
    hrs = np.arange(n, dtype=float)
    cons = [(28.984104, 1.52, 0.4), (30.0, 0.47, 1.1), (28.43973, 0.30, 2.3), (15.041069, 0.10, 0.7), (13.943035, 0.12, 4.0)]
    lev = np.full(n, 2.22)
    for speed, amp, phase in cons:
        lev += amp * np.cos(np.radians(speed * hrs) - phase)
    surge = np.zeros(n)
    eps = 0.035 * rng.standard_normal(n)
    for i in range(1, n):
        surge[i] = 0.985 * surge[i - 1] + eps[i]
    lev += surge
    W.tide = (t0, lev)
    # daily river flow, m3/s
    days = (dt.date(2026, 12, 31) - dt.date(2016, 1, 1)).days + 1
    doy = np.array([(dt.date(2016, 1, 1) + dt.timedelta(days=i)).timetuple().tm_yday for i in range(days)])
    base = 6.5 + 4.8 * np.cos(2 * np.pi * (doy - 25) / 365.25)
    ar = np.zeros(days)
    e = 0.25 * rng.standard_normal(days)
    for i in range(1, days):
        ar[i] = 0.93 * ar[i - 1] + e[i]
    W.flow = (dt.date(2016, 1, 1), np.round(base * np.exp(ar), 2))
    # vessel calls 2024 to 2026
    names = ["Baltic Venture", "Norrland Trader", "Celtic Mariner", "Fenland Star", "Hollandia Bulk", "Kattegat Sun",
             "Saxon Pride", "Tees Spirit", "Morven Bay", "Ostend Carrier", "Ijssel Breeze", "Humber Venture",
             "Skagen Trader", "Wash Endeavour", "Rotterdam Link", "Lowestoft Pride", "Elbe Courier", "Bergen Spirit",
             "Calais Express", "Thames Carrier", "Nordic Pioneer", "Dogger Bank", "Fendmouth Pilot", "Cuxhaven Star"]
    calls = []
    d = dt.datetime(2024, 1, 2, 5, 0)
    while d < dt.datetime(2026, 12, 31):
        d += dt.timedelta(hours=float(rng.uniform(5.0, 22.0)))
        nm = names[int(rng.integers(0, len(names)))]
        kind = ["general cargo", "bulk", "container", "ro-ro", "tanker"][int(rng.integers(0, 5))]
        loa = float(round(rng.uniform(88, 199), 1))
        draught = float(round(min(13.6, 4.5 + loa * 0.045 + rng.normal(0, 0.6)), 1))
        berth = ["NQ1", "NQ3", "CT5"][int(rng.integers(0, 3))] if kind != "container" else "CT5"
        calls.append((d, nm, kind, loa, draught, berth))
    W.calls = calls
