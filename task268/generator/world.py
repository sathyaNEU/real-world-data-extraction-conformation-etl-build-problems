"""The world under task268: six haddock grounds on the organisation's grid, each ground's stock by cell and year, the
members' fleet and where it tows, and the autumn survey's fixed stations. Everything downstream (the records, the
documents, the analysis, the checks) reads from build().

A ground's stock follows its own path from 2019 to 2026. As it shrinks it keeps its density longest in its best
cells (the deep band), to a degree set by alpha: alpha 1 is an even decline, alpha near 0 holds the best cells while
the rest empty. The boats work a ground's cells in proportion to the square of their density and leave a cell once
its density is under three-tenths of the ground's best. The survey tows the same stations every October, twelve in
each depth band of every ground, wherever the fish are."""
import datetime as dt
import math

import numpy as np

import common as K

SEED = 69

# relative stock by year 2019..2026, alpha, cells, band shares (A, B, C), base mean density (kg per km2), fleet hours
SPEC = {
    "Skiravie Bank":   dict(trend=[1.00, 0.98, 1.02, 0.95, 0.88, 0.81, 0.75, 0.70], alpha=0.5, cells=46,
                            shares=(0.45, 0.35, 0.20), d0=1250, hours=4800),
    "Halmorie Deep":   dict(trend=[1.00, 1.03, 0.97, 0.89, 0.77, 0.62, 0.50, 0.41], alpha=0.12, mid=2.0, cells=80,
                            shares=(0.68, 0.24, 0.08), d0=1150, hours=6800),
    "Moraskie Ground": dict(trend=[1.00, 1.02, 0.99, 0.95, 0.90, 0.85, 0.80, 0.76], alpha=0.7, cells=44,
                            shares=(0.40, 0.40, 0.20), d0=1150, hours=4400),
    "Brettach Bank":   dict(trend=[1.00, 0.99, 1.01, 0.91, 0.81, 0.71, 0.62, 0.53], alpha=1.0, cells=58,
                            shares=(0.40, 0.35, 0.25), d0=1300, hours=6400),
    "Vallaskie Hole":  dict(trend=[1.00, 1.01, 1.00, 0.97, 0.93, 0.89, 0.85, 0.82], alpha=0.8, cells=40,
                            shares=(0.35, 0.40, 0.25), d0=1050, hours=4000),
    "Cullardy Patch":  dict(trend=[1.00, 0.97, 1.03, 1.00, 0.97, 0.94, 0.91, 0.88], alpha=0.9, cells=48,
                            shares=(0.45, 0.35, 0.20), d0=1100, hours=4600),
}
CENTRES = {"Skiravie Bank": (6, 5), "Halmorie Deep": (6, 17), "Moraskie Ground": (17, 6),
           "Brettach Bank": (18, 18), "Vallaskie Hole": (29, 5), "Cullardy Patch": (29, 17)}
QUAL = {"A": 0.10, "B": 0.35, "C": 1.0}     # habitat quality by depth band
BETA, FLOOR = 2.0, 0.30                      # the fleet's preference for density and the density it leaves a cell at
SIGMA_COMM = 0.45                            # haul-to-haul noise in the members' catches
QC = 0.08                                    # km2 a member trawler fishes in an hour, at full efficiency
QS = 0.039                                   # km2 the survey trawl fishes in a standard 30-minute tow
NB_K = 8.0                                   # overdispersion of the survey's haddock counts
STATION_SD = 0.35                            # a station's lasting patchiness
MONTH_W = [0.70, 0.75, 0.90, 1.00, 1.05, 1.10, 1.05, 1.00, 0.95, 0.90, 0.80, 0.60]
LAT_N, LON_W = 61.5, -2.0                    # the grid's north-west corner; rows of 5', columns of 10'
ELOG_END = dt.date(2026, 10, 31)             # the e-logbook export runs to the end of October 2026


# ---------------------------------------------------------------------------------------------- the grid
def cell_geometry(row, col):
    """A sub-square's code, rectangle, number, bounds, centre and area (km2)."""
    lat_n = LAT_N - row * 5 / 60
    lat_s = lat_n - 5 / 60
    lon_w = LON_W + col * 10 / 60
    lon_e = lon_w + 10 / 60
    latc, lonc = (lat_n + lat_s) / 2, (lon_w + lon_e) / 2
    ices_row = int(math.floor((latc - 36.0) / 0.5)) + 1
    lon_deg = int(math.floor(lonc))
    colcode = ("E%d" % (lon_deg + 10)) if lon_deg < 0 else ("F%d" % lon_deg)
    rect = "%02d%s" % (ices_row, colcode)
    rect_lat_n = 36.0 + ices_row * 0.5
    sub_r = int(round((rect_lat_n - lat_n) * 12))
    sub_c = int(round((lon_w - lon_deg) * 6))
    sub = sub_r * 6 + sub_c + 1
    area = 9.26 * 18.52 * math.cos(math.radians(latc))
    return dict(row=row, col=col, rect=rect, sub=sub, code="%s/%02d" % (rect, sub), lat_n=lat_n, lat_s=lat_s,
                lon_w=lon_w, lon_e=lon_e, lat=latc, lon=lonc, area=round(area, 2))


def smooth_field(rng, n=3, scale=4.0):
    fr = rng.uniform(0.15, 0.45, (n, 2)) / scale * 4
    ph = rng.uniform(0, 2 * np.pi, n)
    amp = rng.uniform(0.5, 1.0, n)
    return lambda r, c: float(sum(a * math.cos(f[0] * r + f[1] * c + p) for a, f, p in zip(amp, fr, ph)))


def grid(rng):
    cells = []
    taken = set()
    for gname, gcode, kind in K.GROUNDS:
        s = SPEC[gname]
        r0, c0 = CENTRES[gname]
        ar, ac = rng.uniform(0.85, 1.25), rng.uniform(0.85, 1.25)
        noise = smooth_field(rng)
        cand = []
        for r in range(max(0, r0 - 9), min(36, r0 + 10)):
            for c in range(max(0, c0 - 9), min(24, c0 + 10)):
                if any((r + dr, c + dc) in taken for dr in (-1, 0, 1) for dc in (-1, 0, 1)):
                    continue
                d = math.hypot((r - r0) / ar, (c - c0) / ac) + 0.9 * noise(r, c)
                cand.append((d, r, c))
        cand.sort()
        chosen = cand[:s["cells"]]
        taken |= {(r, c) for _, r, c in chosen}
        theta = rng.uniform(0, 2 * np.pi)
        noise2 = smooth_field(rng)
        pots = []
        for d, r, c in chosen:
            if kind == "deep":
                pot = -d
            elif kind == "bank":
                pot = d
            else:
                pot = (r - r0) * math.cos(theta) + (c - c0) * math.sin(theta)
            pots.append(pot + 0.6 * noise2(r, c) + rng.normal(0, 0.25))
        order = np.argsort(pots)            # shallowest first
        n = s["cells"]
        nA = int(round(n * s["shares"][0]))
        nB = int(round(n * s["shares"][1]))
        band = {}
        for k, i in enumerate(order):
            band[i] = "A" if k < nA else ("B" if k < nA + nB else "C")
        deep_max = 212 if kind == "deep" else 178
        for k, i in enumerate(order):
            b = band[i]
            lo, hi = {"A": (68, 99), "B": (100, 139), "C": (140, deep_max)}[b]
            ranks = [j for j in order if band[j] == b]
            pos = ranks.index(i) / max(1, len(ranks) - 1)
            depth = int(round(lo + 1 + pos * (hi - lo - 2) + rng.normal(0, 1.5)))
            depth = min(hi, max(lo + 1, depth)) if b != "A" else min(99, max(lo, depth))
            if b == "B":
                depth = min(139, max(100, depth))
            if b == "C":
                depth = max(140, depth)
            _, r, c = chosen[i]
            g = cell_geometry(r, c)
            g.update(ground=gname, band=b, depth=depth)
            cells.append(g)
    codes = [c["code"] for c in cells]
    assert len(set(codes)) == len(codes), "grounds overlap"
    return cells


# ---------------------------------------------------------------------------------------------- the stock
def stock(rng, cells):
    """Density (kg per km2) by cell and year. A ground's deep band keeps a share B ** alpha of its base density, the
    middle band B ** mid (by default 1 + (1 - alpha) / 2), and the shallow band holds the rest of the stock, so the
    ground's total is B times its base total: the basin a shrinking stock retreats into."""
    dens = {}
    qual = {}
    for gname in K.GROUND_NAMES:
        s = SPEC[gname]
        idx = [i for i, c in enumerate(cells) if c["ground"] == gname]
        a = np.array([cells[i]["area"] for i in idx])
        band = np.array([cells[i]["band"] for i in idx])
        q = np.array([QUAL[b] for b in band]) * np.exp(rng.normal(0, 0.12, len(idx)))
        for i, v in zip(idx, q):
            qual[i] = float(v)
        tot = {b: float(np.sum((q * a)[band == b])) for b in K.BANDS}
        scale = s["d0"] * a.sum() / sum(tot.values())
        for yi, y in enumerate(K.YEARS):
            B = s["trend"][yi]
            m = {"C": B ** s["alpha"], "B": B ** s.get("mid", 1 + (1 - s["alpha"]) / 2)}
            m["A"] = (B * sum(tot.values()) - m["C"] * tot["C"] - m["B"] * tot["B"]) / tot["A"]
            assert m["A"] > 0, (gname, y, m)
            for i, qi, b in zip(idx, q, band):
                dens[(i, y)] = float(scale * qi * m[b])
    return dens, qual


# ---------------------------------------------------------------------------------------------- the fleet
VESSEL_NAMES = ["Arcturus", "Starlight", "Catriona Rose", "Dawn Harvester", "Emulator", "Fairwind", "Gleaming Star",
                "Heather Bell", "Islander", "Jasper", "Kestrel", "Harvest Moon", "Ocean Dawn", "Northern Lass",
                "Ocean Reaper", "Provider", "Quiet Waters", "Rosebud", "Sea Harvester", "Tranquility", "Unity",
                "Valhalla", "Golden Venture", "Brighter Morn", "Zephyr", "Brighter Dawn", "Celtic Mist", "Endurance",
                "Good Hope", "Silver Spray"]


def fleet(rng):
    vessels = []
    used = set()
    for i, name in enumerate(VESSEL_NAMES):
        port = K.PORT_NAMES[i % 4] if i < 28 else K.PORT_NAMES[(i + 1) % 4]
        while True:
            num = int(rng.integers(12, 480))
            pln = "%s %d" % (K.PORT_LETTERS[port], num)
            if pln not in used:
                used.add(pln)
                break
        while True:
            rss = "C%05d" % int(rng.integers(15000, 22999))
            if rss not in used:
                used.add(rss)
                break
        pool = K.POOL_CODES[[0, 1, 2, 3, 0, 1, 2, 4, 1, 0, 3, 2, 0, 1, 2, 3, 4, 0, 1, 2, 0, 1, 3, 2, 0, 1, 4, 2, 1, 0][i]]
        g = list(rng.choice(K.GROUND_NAMES, size=int(rng.integers(2, 4)), replace=False))
        length = round(float(rng.uniform(14.5, 27.9)), 2) if pool != "I" else round(float(rng.uniform(11.2, 14.9)), 2)
        registered = dt.date(int(rng.integers(1996, 2018)), int(rng.integers(1, 13)), int(rng.integers(1, 29)))
        since = max(registered, dt.date(int(rng.integers(2004, 2019)), int(rng.integers(1, 13)), 1))
        vessels.append(dict(name=name, pln=pln, port=port, rss=rss, pool=pool, grounds=g, length=length,
                            q=float(np.exp(rng.normal(0, 0.18))), registered=registered, since=since,
                            history=[(pln, registered, None, port)]))
    # every ground worked by at least four boats
    for gname in K.GROUND_NAMES:
        have = [v for v in vessels if gname in v["grounds"]]
        k = 0
        while len(have) < 4:
            v = vessels[(K.GROUND_NAMES.index(gname) * 5 + k) % len(vessels)]
            if gname not in v["grounds"]:
                v["grounds"].append(gname)
                have.append(v)
            k += 1
    # two re-registrations at a new home port: one in March 2024, one on 1 June 2026
    a, b = vessels[2], vessels[5]
    for v, when, newport in ((a, dt.date(2024, 3, 11), "Haldness"), (b, dt.date(2026, 6, 1), "Eastquay")):
        old = v["pln"]
        while True:
            num = int(rng.integers(12, 480))
            new = "%s %d" % (K.PORT_LETTERS[newport], num)
            if new not in used:
                used.add(new)
                break
        v["history"] = [(old, v["registered"], when - dt.timedelta(days=1), v["port"]), (new, when, None, newport)]
        v["pln"], v["port"] = new, newport
    return vessels


def pln_on(v, day):
    for pln, start, end, _ in v["history"]:
        if day >= start and (end is None or day <= end):
            return pln
    return v["history"][0][0]


def port_on(v, day):
    for _, start, end, port in v["history"]:
        if day >= start and (end is None or day <= end):
            return port
    return v["history"][0][3]


# ---------------------------------------------------------------------------------------------- the fishing
def fishing(rng, cells, dens, vessels):
    """Trips and hauls 2019 to October 2026: each trip works one ground, hauls rotating round a few cells chosen by
    the density the skipper expects there."""
    trips, hauls = [], []
    by_ground = {g: [i for i, c in enumerate(cells) if c["ground"] == g] for g in K.GROUND_NAMES}
    mw = np.array(MONTH_W) / sum(MONTH_W)
    tno = 0
    for y in K.YEARS:
        for gname in K.GROUND_NAMES:
            idx = by_ground[gname]
            d = np.array([dens[(i, y)] for i in idx])
            att = d ** BETA
            att[d < FLOOR * d.max()] = 0.0
            p = att / att.sum()
            target = SPEC[gname]["hours"] * float(np.exp(rng.normal(0, 0.05)))
            boats = [v for v in vessels if gname in v["grounds"]]
            bw = np.array([1.0 + 0.5 * (v["pool"] != "I") for v in boats])
            bw /= bw.sum()
            done = 0.0
            while done < target:
                v = boats[int(rng.choice(len(boats), p=bw))]
                m = int(rng.choice(12, p=mw)) + 1
                start = dt.date(y, m, 1) + dt.timedelta(days=int(rng.integers(0, 28)))
                ndays = int(rng.integers(4, 8))
                end = start + dt.timedelta(days=ndays)
                focus = [idx[int(j)] for j in rng.choice(len(idx), size=3, p=p)]
                t0 = dt.datetime(start.year, start.month, start.day, 4, 0) + dt.timedelta(hours=float(rng.uniform(8, 20)))
                stop = dt.datetime(end.year, end.month, end.day, 0, 0) - dt.timedelta(hours=float(rng.uniform(10, 18)))
                tno += 1
                trip = dict(id=tno, vessel=v["rss"], ground=gname, start=start, end=end, year=y, hauls=[])
                t = t0
                while True:
                    hrs = float(np.exp(rng.normal(math.log(3.8), 0.14)))
                    if t + dt.timedelta(hours=hrs) > stop:
                        break
                    c = focus[int(rng.integers(3))] if rng.random() < 0.8 else idx[int(rng.choice(len(idx), p=p))]
                    mon = t.month
                    mq = 1.0 + 0.15 * math.cos(2 * math.pi * (mon - 3) / 12)
                    live = v["q"] * mq * dens[(c, y)] * hrs * QC * float(np.exp(rng.normal(-SIGMA_COMM ** 2 / 2, SIGMA_COMM)))
                    h = dict(trip=tno, vessel=v["rss"], cell=c, start=t, hours=hrs, had=live,
                             cod=live * float(np.exp(rng.normal(math.log(0.16), 0.6))),
                             whg=live * float(np.exp(rng.normal(math.log(0.28), 0.5))),
                             pok=live * float(np.exp(rng.normal(math.log(0.12), 0.8))))
                    trip["hauls"].append(len(hauls))
                    hauls.append(h)
                    done += hrs
                    t = t + dt.timedelta(hours=hrs + float(rng.uniform(0.35, 1.1)))
                if trip["hauls"]:
                    trips.append(trip)
    # the e-logbook export ends with October 2026
    keep = [t for t in trips if not (t["year"] == 2026 and t["end"] > ELOG_END)]
    return keep, hauls


# ---------------------------------------------------------------------------------------------- the survey
def survey(rng, cells, dens):
    """Stations drawn in 2019, twelve in each depth band of every ground and fixed since; two replaced in 2023 after
    the net was torn on them in 2022; one not fished in 2020 for weather. One tow a station each October."""
    stations = []
    for gname in K.GROUND_NAMES:
        for b in K.BANDS:
            idx = [i for i, c in enumerate(cells) if c["ground"] == gname and c["band"] == b]
            n = K.STATIONS_PER_BAND
            pick = list(rng.choice(idx, size=min(n, len(idx)), replace=False))
            while len(pick) < n:
                pick.append(int(rng.choice(idx)))
            for i in pick:
                stations.append(dict(cell=int(i), ground=gname, band=b, eff=float(np.exp(rng.normal(-STATION_SD ** 2 / 2, STATION_SD)))))
    for s in stations:
        c = cells[s["cell"]]
        s["lat"] = c["lat_s"] + (c["lat_n"] - c["lat_s"]) * float(rng.uniform(0.12, 0.88))
        s["lon"] = c["lon_w"] + (c["lon_e"] - c["lon_w"]) * float(rng.uniform(0.12, 0.88))
        lo, hi = K.BAND_LIMITS[s["band"]]
        s["depth"] = int(min(hi - 1, max(lo, round(c["depth"] + rng.normal(0, 3)))))
    order = sorted(range(len(stations)), key=lambda k: (-round(stations[k]["lat"], 2), stations[k]["lon"]))
    for no, k in enumerate(order, 1):
        stations[k]["id"] = "S%03d" % no
        stations[k]["from"], stations[k]["to"] = 2019, 2026
    # replacements from 2023: drawn at random within the same ground and depth band
    torn = [k for k in rng.permutation(len(stations)) if stations[k]["band"] != "C"
            and stations[k]["ground"] == "Vallaskie Hole"][:2]
    nxt = len(stations)
    for k in sorted(torn, key=lambda k: stations[k]["id"]):
        s = stations[k]
        s["to"] = 2022
        idx = [i for i, c in enumerate(cells) if c["ground"] == s["ground"] and c["band"] == s["band"]]
        i = int(rng.choice(idx))
        c = cells[i]
        nxt += 1
        r = dict(cell=i, ground=s["ground"], band=s["band"], eff=float(np.exp(rng.normal(-STATION_SD ** 2 / 2, STATION_SD))),
                 id="S%03d" % nxt, lat=c["lat_s"] + (c["lat_n"] - c["lat_s"]) * float(rng.uniform(0.12, 0.88)),
                 lon=c["lon_w"] + (c["lon_e"] - c["lon_w"]) * float(rng.uniform(0.12, 0.88)), replaces=s["id"])
        lo, hi = K.BAND_LIMITS[s["band"]]
        r["depth"] = int(min(hi - 1, max(lo, round(c["depth"] + rng.normal(0, 3)))))
        r["from"], r["to"] = 2023, 2026
        stations.append(r)
    weather = [k for k in rng.permutation(len(stations)) if stations[k]["from"] == 2019 and stations[k]["to"] == 2026
               and stations[k]["ground"] == "Cullardy Patch"][0]
    missed = {(stations[weather]["id"], 2020)}
    tows = []
    mean_w = {(g, y): 0.45 * float(np.exp(rng.normal(0, 0.08))) for g in K.GROUND_NAMES for y in K.YEARS}
    juv = {y: float(rng.uniform(0.12, 0.34)) for y in K.YEARS}
    for y in K.YEARS:
        day0 = dt.date(y, 10, 1) + dt.timedelta(days=int(rng.integers(2, 7)))
        live = [s for s in stations if s["from"] <= y <= s["to"] and (s["id"], y) not in missed]
        route = sorted(live, key=lambda s: (s["ground"] != K.GROUND_NAMES[0], K.GROUND_NAMES.index(s["ground"]), -s["lat"], s["lon"]))
        per_day = int(rng.integers(17, 20))
        for k, s in enumerate(route):
            day = day0 + dt.timedelta(days=k // per_day + (1 if (k // per_day) >= 6 else 0))
            hh = 6 + (k % per_day) * 0.72 + float(rng.uniform(0, 0.3))
            mu_kg = dens[(s["cell"], y)] * s["eff"] * QS
            wbar = mean_w[(s["ground"], y)]
            mu_n = mu_kg / wbar
            n = int(rng.negative_binomial(NB_K, NB_K / (NB_K + mu_n))) if mu_n > 0 else 0
            kg = round(n * wbar * float(np.exp(rng.normal(0, 0.06))), 1) if n else 0.0
            if n and kg == 0.0:
                kg = 0.1
            c = cells[s["cell"]]
            lat = min(c["lat_n"] - 0.002, max(c["lat_s"] + 0.002, s["lat"] + float(rng.normal(0, 0.004))))
            lon = min(c["lon_e"] - 0.003, max(c["lon_w"] + 0.003, s["lon"] + float(rng.normal(0, 0.006))))
            tows.append(dict(year=y, station=s["id"], ground=s["ground"], band=s["band"], cell=s["cell"], date=day,
                             time="%02d:%02d" % (int(hh), int((hh % 1) * 60)), lat=round(lat, 4),
                             lon=round(lon, 4), depth=s["depth"] + int(rng.integers(-1, 2)),
                             had_kg=kg, had_n=n, had_juv=int(rng.binomial(n, juv[y])) if n else 0,
                             cod_kg=round(float(rng.gamma(1.2, 9.0)), 1), whg_kg=round(float(rng.gamma(1.5, 14.0)), 1),
                             pok_kg=round(float(rng.gamma(0.6, 12.0)), 1), spurdog_n=int(rng.poisson(1.4)),
                             skate_kg=round(float(rng.gamma(0.5, 6.0)), 1), porpoise_n=int(rng.random() < 0.006),
                             seabird_n=int(rng.random() < 0.004)))
    for t in tows:
        lo, hi = K.BAND_LIMITS[t["band"]]
        t["depth"] = int(min(hi - 1, max(lo, t["depth"])))
    return stations, tows, missed


def build(seed=SEED):
    rng = np.random.default_rng(seed)
    cells = grid(rng)
    dens, qual = stock(rng, cells)
    vessels = fleet(rng)
    trips, hauls = fishing(rng, cells, dens, vessels)
    stations, tows, missed = survey(rng, cells, dens)
    return dict(seed=seed, cells=cells, dens=dens, qual=qual, vessels=vessels, trips=trips, hauls=hauls,
                stations=stations, tows=tows, missed=missed)
