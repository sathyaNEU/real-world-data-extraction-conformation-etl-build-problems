"""The Tollaver Basin as it ran in the rating year: each producer's sites (well pads, tank batteries, compressor
stations) with their state facility numbers and operators, the emission sources at them (persistent leaks,
intermittent tank dumps, long episodes), Talmora's four campaigns (flight lines, passes, cloud losses, overlaps) and
the plumes each pass detected, and Talmora's 2025 controlled-release study."""
import datetime as dt
import math

import numpy as np

import world as W

LAT0, LAT1 = 36.21, 36.94
LON0, LON1 = -101.46, -100.57
M_PER_DEG_LAT = 111_000.0
M_PER_DEG_LON = 111_000.0 * math.cos(math.radians(36.6))

# site packages that changed operator during the rating year: (from, to, number of sites, effective date)
TRANSFERS = [("Ruskmoor Exploration", "Pellisto Gas Partners", 6, dt.date(2026, 4, 1)),
             ("Calbrent Energy", "Sunmere Natural Gas", 7, dt.date(2026, 7, 1))]


LON_EDGES = np.linspace(LON0, LON1, 19)            # Talmora's 18 north-south flight lines


def lines_of(lon):
    """The flight lines that image a point: its own, and the neighbour's where the lines overlap at the edge."""
    ln = int(np.searchsorted(LON_EDGES, lon) - 1)
    frac = (lon - LON_EDGES[ln]) / (LON_EDGES[ln + 1] - LON_EDGES[ln])
    if frac > 0.955 and ln < 17:
        return [ln, ln + 1]
    if frac < 0.045 and ln > 0:
        return [ln, ln - 1]
    return [ln]


def pod(q):
    q = np.asarray(q, dtype=float)
    return 1.0 / (1.0 + np.exp(-(np.log(q) - math.log(W.POD_Q50)) / W.POD_S))


def _blocks(rng):
    """Each producer's acreage: one to three rectangles, laid out over the basin with a few shared edges."""
    out = {}
    cols, rows = 6, 5
    cells = [(i, j) for i in range(cols) for j in range(rows)]
    order = rng.permutation(len(cells))
    k = 0
    for p in W.PRODUCERS:
        nb = 1 if p[3] <= 55 else (2 if p[3] <= 85 else 3)
        mine = []
        for _ in range(nb):
            i, j = cells[order[k]]
            k += 1
            mine.append((LAT0 + (LAT1 - LAT0) * j / rows, LAT0 + (LAT1 - LAT0) * (j + 1) / rows,
                         LON0 + (LON1 - LON0) * i / cols, LON0 + (LON1 - LON0) * (i + 1) / cols))
        out[p[0]] = mine
    return out


def sites(rng):
    """The site list: id, producer at the start of the rating year, type, coordinates, facility numbers."""
    blocks = _blocks(rng)
    out = []
    fac_seq = iter(rng.permutation(np.arange(410_000, 489_999))[:4000])
    for p in W.PRODUCERS:
        name, ns = p[0], p[3]
        bl = blocks[name]
        per = [ns // len(bl) + (1 if b < ns % len(bl) else 0) for b in range(len(bl))]
        for b, nb in zip(bl, per):
            g = int(math.ceil(math.sqrt(nb * 1.4)))
            spots = [(a, c) for a in range(g) for c in range(g)]
            pick = rng.choice(len(spots), nb, replace=False)
            for s in sorted(pick):
                a, c = spots[s]
                lat = b[0] + (b[1] - b[0]) * (a + 0.5 + rng.uniform(-0.3, 0.3)) / g
                lon = b[2] + (b[3] - b[2]) * (c + 0.5 + rng.uniform(-0.3, 0.3)) / g
                u = rng.random()
                kind = "well pad" if u < 0.74 else ("tank battery" if u < 0.93 else "compressor station")
                out.append(dict(producer=name, kind=kind, lat=lat, lon=lon))
    # ids in a stable order: by producer then position
    for i, s in enumerate(out):
        s["site_id"] = "TS-%05d" % (10_000 + 7 * i + int(rng.integers(0, 7)))
        s["fac"] = ["F-%06d" % next(fac_seq)]
    # a few sites re-permitted under a second number, a few pad and battery pairs under one permit
    for s in rng.choice(out, 24, replace=False):
        s["fac"].append("F-%06d" % next(fac_seq))
    pads = [s for s in out if s["kind"] == "well pad"]
    bats = [s for s in out if s["kind"] == "tank battery"]
    for b in rng.choice(bats, 14, replace=False):
        near = min((p for p in pads if p["producer"] == b["producer"]),
                   key=lambda p: (p["lat"] - b["lat"]) ** 2 + (p["lon"] - b["lon"]) ** 2)
        if lines_of(near["lon"]) == lines_of(b["lon"]):        # one permit covers a pad and its battery on one lease road
            b["fac"][0] = near["fac"][0]
    # operator history
    for s in out:
        s["ops"] = [(W.RATING_START, s["producer"])]
    for frm, to, n, eff in TRANSFERS:
        cand = [s for s in out if s["producer"] == frm and s["kind"] == "well pad"]
        for s in sorted(rng.choice(cand, n, replace=False), key=lambda z: z["site_id"]):
            s["ops"].append((eff, to))
    return out


def operator_on(site, day):
    who = site["ops"][0][1]
    for eff, p in site["ops"]:
        if day >= eff:
            who = p
    return who


def sources(rng, site_list):
    """The emission sources: each producer's persistent leaks, tank dumps and episodes, sized to its target."""
    by_p = {}
    for s in site_list:
        by_p.setdefault(s["producer"], []).append(s)
    out = []
    for p in W.PRODUCERS:
        (name, _, typ, ns, bcf, fields, tgt, sl, st, se, lmed, trate, duty) = p
        ch4 = sum(sh * FIELD_CH4[f] for f, sh in fields)
        prod_t = bcf * 1e6 * ch4 * W.KG_PER_MCF / 1000.0
        tot = tgt / 100.0 * prod_t * 1000.0 / W.HOURS                 # kg/h, time-averaged
        my = by_p[name]
        nleak = max(1, int(round(sl * tot / (lmed * math.exp(0.45 ** 2 / 2)))))
        ntank = int(round(st * tot / (trate * math.exp(0.30 ** 2 / 2) * duty)))
        nev = int(round(se * tot / 260.0)) if se else 0
        tanky = [s for s in my if s["kind"] == "tank battery"] or my
        for _ in range(nleak):
            s = my[int(rng.integers(0, len(my)))]
            out.append(dict(site=s["site_id"], kind="leak", rate=float(rng.lognormal(math.log(lmed), 0.45)),
                            duty=1.0, start=None, end=None, dx=rng.normal(0, 20), dy=rng.normal(0, 20)))
        for _ in range(ntank):
            s = tanky[int(rng.integers(0, len(tanky)))]
            out.append(dict(site=s["site_id"], kind="tank", rate=float(rng.lognormal(math.log(trate), 0.30)),
                            duty=float(np.clip(rng.normal(duty, 0.03), 0.10, 0.40)), start=None, end=None,
                            dx=rng.normal(0, 20), dy=rng.normal(0, 20)))
        for _ in range(nev):
            s = my[int(rng.integers(0, len(my)))]
            st0 = W.RATING_START + dt.timedelta(days=int(rng.integers(0, 300)))
            out.append(dict(site=s["site_id"], kind="episode", rate=float(rng.lognormal(math.log(260), 0.30)),
                            duty=1.0, start=st0, end=st0 + dt.timedelta(days=int(rng.integers(45, 150))),
                            dx=rng.normal(0, 20), dy=rng.normal(0, 20)))
    return out


# each field's methane share (mole fraction) as the 2026 composite analyses give it
FIELD_CH4 = {"Fenholt Bend": 0.862, "East Tollaver": 0.874, "Pinyon Draw": 0.838, "Brushy Mesa": 0.881,
             "Lechuza Creek": 0.846, "Anchell Flats": 0.827, "Corran Ridge": 0.869, "Sotol Wash": 0.852,
             "Sunmere Dome": 0.831}


def campaigns(rng, site_list, src):
    """Talmora's passes and plumes. Returns (passes, plumes): each pass images one facility number set on one flight
    line at one time; the plumes are what the passes detected, at the coordinates Talmora estimated."""
    by_site = {}
    for k in src:
        by_site.setdefault(k["site"], []).append(k)
    lon_edges = LON_EDGES
    passes, plumes = [], []
    plan = {}
    pid = 0
    for ci, (cname, d0, d1) in enumerate(W.CAMPAIGNS):
        days = (d1 - d0).days + 1
        lost = set(rng.choice(18, 1, replace=False).tolist())          # one line lost to cloud
        line_day = {ln: d0 + dt.timedelta(days=int(ln * days // 18)) for ln in range(18)}
        line_hour = {ln: 15.0 + 6.0 * rng.random() for ln in range(18)}
        wind = {ln: float(np.clip(rng.lognormal(math.log(3.8), 0.30), 1.6, 8.0)) for ln in range(18)}
        plan[cname] = dict(lost=lost, day=line_day, hour=line_hour, wind=wind, edges=lon_edges)
        on_state = {}
        for s in sorted(site_list, key=lambda z: z["site_id"]):
            for ln2 in lines_of(s["lon"]):
                day = line_day[ln2]
                t = dt.datetime.combine(day, dt.time(0)) + dt.timedelta(hours=line_hour[ln2] + (s["lat"] - LAT0) / (LAT1 - LAT0) * 0.9)
                imaged = ln2 not in lost
                passes.append(dict(campaign=cname, line=ln2, time=t, site=s["site_id"], imaged=imaged, wind=wind[ln2]))
                if not imaged:
                    continue
                for k in by_site.get(s["site_id"], []):
                    key = (cname, id(k))
                    if key not in on_state:
                        if k["kind"] == "tank":
                            on_state[key] = bool(rng.random() < k["duty"])
                        elif k["kind"] == "episode":
                            on_state[key] = k["start"] <= day < k["end"]
                        else:
                            on_state[key] = True
                    if not on_state[key]:
                        continue
                    q_t = k["rate"] * math.exp(rng.normal(0, W.WITHIN_SD))
                    if rng.random() >= float(pod(q_t)):
                        continue
                    q_m = q_t * math.exp(rng.normal(0, W.QUANT_SD))
                    pid += 1
                    plumes.append(dict(n=pid, campaign=cname, line=ln2, time=t + dt.timedelta(seconds=int(rng.integers(0, 50))),
                                       lat=s["lat"] + (k["dy"] + rng.normal(0, 18)) / M_PER_DEG_LAT,
                                       lon=s["lon"] + (k["dx"] + rng.normal(0, 18)) / M_PER_DEG_LON,
                                       rate=q_m, sigma=q_m * (0.18 + 0.10 * rng.random()), wind=wind[ln2],
                                       site=s["site_id"], kind=k["kind"]))
    return passes, plumes, plan


def midstream(seed, site_list, plan):
    """The gathering company's compressor stations and the processing plant, which Talmora's lines image with the
    producers' sites; their plumes sit 400 m or more from any producer site. Their own random stream."""
    rng = np.random.default_rng(seed + 31)
    taken = {f for s in site_list for f in s["fac"]}
    fac = []
    while len(fac) < 13:
        lat = float(rng.uniform(LAT0 + 0.02, LAT1 - 0.02))
        lon = float(rng.uniform(LON0 + 0.02, LON1 - 0.02))
        near = min(math.hypot((lat - s["lat"]) * M_PER_DEG_LAT, (lon - s["lon"]) * M_PER_DEG_LON) for s in site_list)
        if near < 400:
            continue
        num = "F-%06d" % int(rng.integers(500_000, 599_999))
        if num in taken:
            continue
        taken.add(num)
        kind = "processing plant" if not fac else "gathering compressor station"
        fac.append(dict(fac=num, lat=lat, lon=lon, kind=kind,
                        name=W.PLANT if not fac else "%s CS-%02d" % ("Kelterra", len(fac)),
                        src=[dict(rate=float(rng.lognormal(math.log(14 if fac else 30), 0.6)), duty=1.0 if rng.random() < 0.7 else 0.3)
                             for _ in range(int(rng.integers(1, 5)))]))
    passes, plumes = [], []
    for cname, d0, d1 in W.CAMPAIGNS:
        p = plan[cname]
        for f in fac:
            ln = int(np.searchsorted(p["edges"], f["lon"]) - 1)
            day = p["day"][ln]
            t = dt.datetime.combine(day, dt.time(0)) + dt.timedelta(hours=p["hour"][ln] + (f["lat"] - LAT0) / (LAT1 - LAT0) * 0.9)
            imaged = ln not in p["lost"]
            passes.append(dict(campaign=cname, line=ln, time=t, fac=f["fac"], imaged=imaged, wind=p["wind"][ln]))
            if not imaged:
                continue
            for k in f["src"]:
                if rng.random() >= k["duty"]:
                    continue
                q_t = k["rate"] * math.exp(rng.normal(0, W.WITHIN_SD))
                if rng.random() >= float(pod(q_t)):
                    continue
                q_m = q_t * math.exp(rng.normal(0, W.QUANT_SD))
                plumes.append(dict(campaign=cname, line=ln, time=t + dt.timedelta(seconds=int(rng.integers(0, 50))),
                                   lat=f["lat"] + rng.normal(0, 25) / M_PER_DEG_LAT, lon=f["lon"] + rng.normal(0, 25) / M_PER_DEG_LON,
                                   rate=q_m, sigma=q_m * (0.18 + 0.10 * rng.random()), wind=p["wind"][ln], site=None, kind="midstream",
                                   fac=f["fac"]))
        # a few plumes along gathering lines, away from every facility
        for _ in range(int(rng.integers(3, 8))):
            lat = float(rng.uniform(LAT0, LAT1))
            lon = float(rng.uniform(LON0, LON1))
            if min(math.hypot((lat - s["lat"]) * M_PER_DEG_LAT, (lon - s["lon"]) * M_PER_DEG_LON) for s in site_list) < 400:
                continue
            ln = int(np.searchsorted(p["edges"], lon) - 1)
            if ln in p["lost"]:
                continue
            q_m = float(rng.lognormal(math.log(18), 0.5))
            t = dt.datetime.combine(p["day"][ln], dt.time(0)) + dt.timedelta(hours=p["hour"][ln] + 0.4)
            plumes.append(dict(campaign=cname, line=ln, time=t, lat=lat, lon=lon, rate=q_m, sigma=q_m * 0.25,
                               wind=p["wind"][ln], site=None, kind="pipeline", fac=None))
    return fac, passes, plumes


def releases(rng, n=182):
    """Talmora's 2025 single-blind controlled releases at its test range."""
    out = []
    d0 = dt.date(2025, 8, 18)
    for i in range(n):
        q = float(math.exp(rng.uniform(math.log(0.8), math.log(80.0))))
        wind = float(np.clip(rng.lognormal(math.log(3.6), 0.32), 1.5, 8.0))
        det = bool(rng.random() < float(pod(q)))
        qm = q * math.exp(rng.normal(0, W.QUANT_SD)) if det else None
        out.append(dict(i=i, day=d0 + dt.timedelta(days=int(i // 13)), rate=q, wind=wind, detected=det, est=qm))
    return out


def tenures(site):
    """The site's operators over the rating year: (producer, first day, day after the last)."""
    out = []
    ops = site["ops"]
    for i, (eff, p) in enumerate(ops):
        end = ops[i + 1][0] if i + 1 < len(ops) else W.RATING_END + dt.timedelta(days=1)
        out.append((p, max(eff, W.RATING_START), end))
    return out


def truth(site_list, src):
    """The time-averaged methane each producer's sites emitted at rates of 5 kg/h or more over the rating year, tonnes,
    each site to the producer operating it at the time."""
    site = {s["site_id"]: s for s in site_list}
    out = {p: 0.0 for p in W.NAMES}
    for k in src:
        if k["rate"] < W.FLOOR:
            continue
        for p, a, b in tenures(site[k["site"]]):
            if k["kind"] == "episode":
                lo, hi = max(a, k["start"]), min(b, k["end"])
                days = max(0, (hi - lo).days)
                out[p] += k["rate"] * days * 24 / 1000.0
            else:
                out[p] += k["rate"] * k["duty"] * (b - a).days * 24 / 1000.0
    return out


def register(seed, x):
    """Tarvane's site register as its producers filed it: a few sites the campaigns image, which carry no source and sit
    400 m or more from every plume, were never filed, so the coverage file carries their facility numbers alone. Its
    own random stream."""
    rng = np.random.default_rng(seed + 91)
    has_src = {k["site"] for k in x["sources"]}
    pts = x["plumes"] + x["mplumes"]
    pla = np.array([p["lat"] for p in pts])
    plo = np.array([p["lon"] for p in pts])
    free = {}
    for s in sorted(x["sites"], key=lambda z: z["site_id"]):
        if s["site_id"] in has_src or len(s["ops"]) > 1:
            continue
        if np.hypot((pla - s["lat"]) * M_PER_DEG_LAT, (plo - s["lon"]) * M_PER_DEG_LON).min() < 400:
            continue
        free.setdefault(s["producer"], []).append(s["site_id"])
    count = {}
    for s in x["sites"]:
        count[s["ops"][-1][1]] = count.get(s["ops"][-1][1], 0) + 1
    drop, used = set(), set()
    for p in W.NAMES:
        d = int(rng.integers(1, 5))
        while (count[p] - d) % 5 == 0 or (count[p] - d) in used:
            d += 1
        used.add(count[p] - d)
        drop.update(free[p][i] for i in rng.choice(len(free[p]), d, replace=False))
    return [s for s in x["sites"] if s["site_id"] not in drop]


def world(seed=W.SEED):
    rng = np.random.default_rng(seed)
    st = sites(rng)
    src = sources(rng, st)
    passes, plumes, plan = campaigns(rng, st, src)
    rel = releases(rng)
    mfac, mpasses, mplumes = midstream(seed, st, plan)
    return dict(sites=st, sources=src, passes=passes, plumes=plumes, releases=rel, truth=truth(st, src),
                plan=plan, mfac=mfac, mpasses=mpasses, mplumes=mplumes)
