"""Simulate the Tamarack County world: every dwelling the county has built since 1890 with its building, parcel,
street address, census block and post office; the boundary changes; the households each dwelling holds at the three
censuses and on 1 July 2026; the certificates of occupancy, demolitions, group quarters, births and deaths."""
import datetime as dt
import functools

import numpy as np

import world as W

TYPES = ("SF", "TH", "AP", "MH")


def g(a):
    a = np.maximum(np.asarray(a, float), 0.0)
    return (1 + W.HUMP * a) * np.exp(-a / W.TAU)


def pph(t, a):
    return W.BASE[t] + W.LIFT * g(a)


def yfrac(d):
    """a date as a decimal year"""
    y0 = dt.date(d.year, 1, 1)
    return d.year + (d - y0).days / (dt.date(d.year + 1, 1, 1) - y0).days


def from_frac(x):
    y = int(x)
    y0 = dt.date(y, 1, 1)
    return y0 + dt.timedelta(days=int((x - y) * (dt.date(y + 1, 1, 1) - y0).days))


STEM = ["Cedar", "Maple", "Oak", "Willow", "Birch", "Aspen", "Hickory", "Juniper", "Spruce", "Tamarack", "Hawthorn",
        "Linden", "Sumac", "Alder", "Laurel", "Chestnut", "Walnut", "Poplar", "Elm", "Ash", "Pine", "Basswood", "Ironwood",
        "Cherry", "Plum", "Sycamore", "Beech", "Cottonwood", "Hazel", "Larch", "Meadow", "Prairie", "Brook", "Hollow",
        "Ridge", "Stone", "Fox", "Deer", "Heron", "Quail", "Wren", "Lark", "Robin", "Finch", "Sparrow", "Oriole", "Kestrel",
        "Hilltop", "Valley", "River", "Lake", "Pond", "Mill", "Orchard", "Harvest", "Clover", "Thistle", "Fern", "Bluff",
        "Summit", "Glen", "Spring", "Sunset", "Sunrise", "Garnet", "Granite", "Flint", "Copper", "Silver", "Golden",
        "Autumn", "Winter", "Highland", "Lowell", "Carver", "Hollis", "Mercer", "Grant", "Lincoln", "Jefferson", "Monroe",
        "Madison", "Franklin", "Adams", "Wilson", "Taylor", "Harrison", "Fillmore", "Pierce", "Polk", "Tyler", "Hayes"]
TAIL = ["", "wood", "field", "view", "crest", "dale", "brook", "ridge", "haven", "ton", "side", "gate", "mont", "vale",
        "hurst", "lea", "shire", "wick", "stead", "moor"]
STYPE = ["ST", "AVE", "DR", "LN", "CT", "RD", "CIR", "TRL", "PL", "WAY", "PKWY", "TER"]


SECOND = ["CREEK", "RIDGE", "HILL", "VALLEY", "POINT", "MEADOW", "GROVE", "WOODS", "BEND", "RUN", "HOLLOW", "CROSSING",
          "SPRINGS", "GLEN", "FARM", "ACRES", "HEIGHTS", "PRAIRIE", "ORCHARD", "TRACE"]


def _street_names(rng):
    """subdivision street names as plats name them: a word alone, a word and a landscape word, or a compound"""
    pool = set()
    for s_ in STEM:
        pool.add(s_.upper())
        for t in SECOND:
            if t != s_.upper():
                pool.add("%s %s" % (s_.upper(), t))
        for t in TAIL[1:8]:
            pool.add((s_ + t).upper())
    names = sorted(pool)
    rng.shuffle(names)
    return names


@functools.lru_cache(maxsize=None)
def world():
    rng = np.random.default_rng(W.SEED)
    streets = iter(_street_names(rng))
    units = []      # one dict per dwelling unit
    buildings = []  # one dict per building (a parcel, or a condominium of unit parcels)
    for mi, (code, name, kind, eras) in enumerate(W.MUNIS):
        r = np.random.default_rng(W.SEED * 1000 + mi)
        sc = W.SCALE.get(name, {})
        for ei, (y0, y1, rate, main) in enumerate(eras):
            k = sc.get(ei, sc.get("all", 1.0))
            street, number, on_street = None, 0, 0
            for y in range(y0, y1 + 1):
                n = int(r.poisson(rate * k * r.uniform(0.75, 1.25)))
                if y == 2026:
                    n = n // 2
                while n > 0:
                    t = main if r.random() < 0.86 else ("SF", "TH", "AP")[int(r.integers(0, 3))]
                    if t == "MH" and kind != "village":
                        t = "SF"
                    size = {"SF": 1, "MH": 1, "TH": int(r.choice([2, 2, 4, 5, 6])),
                            "AP": int(r.choice([6, 8, 12, 16, 24, 36]))}[t]
                    size = min(size, max(n, 1)) if t in ("TH", "AP") else 1
                    if t in ("TH", "AP") and size < 2:
                        t, size = "SF", 1
                    comp = y + r.random()
                    if comp > 2026.4959:
                        comp = 2026 + r.random() * 0.4959
                    if street is None or on_street >= int(r.integers(18, 46)):
                        street = (next(streets), STYPE[int(r.integers(0, len(STYPE)))])
                        number, on_street = int(r.choice([100, 200, 1000, 1200, 2000, 3400, 4100, 5600, 7000])), 0
                    number += int(r.choice([2, 4, 6, 8, 10, 12, 14]))
                    on_street += 1
                    b = dict(bid=len(buildings), muni=name, era=ei, type=t, size=size, comp=comp, street=street,
                             number=number, sub="%d-%d-%d" % (mi, ei, (y - y0) // 6))
                    buildings.append(b)
                    for u in range(size):
                        units.append(dict(uid=len(units), bid=b["bid"], muni=name, era=ei, type=t, comp=comp,
                                          unit=("%d" % (101 + u + (u // 6) * 94)) if t == "AP" else
                                          ("ABCDEF"[u] if t == "TH" else ""), demolished=None))
                    n -= size
    _demolish(units, buildings, rng)
    _geography(units, buildings, rng)
    hist = _boundaries(units, buildings)
    return dict(units=units, buildings=buildings, hist=hist)


def _demolish(units, buildings, rng):
    """single-family and manufactured homes come down at about one in a thousand a year from 2000, the oldest most;
    a third of the lots are rebuilt within two years"""
    rs = {m[1]: np.random.default_rng(W.SEED + 7 + 31 * i) for i, m in enumerate(W.MUNIS)}
    extra = []
    for b in buildings:
        r = rs[b["muni"]]
        if b["type"] not in ("SF", "MH") or b["comp"] > 2018:
            continue
        for y in range(2000, 2027):
            age = y - b["comp"]
            if age < 15:
                continue
            p = 0.00035 + 0.0011 * min(age, 110) / 110
            if r.random() < p:
                d = y + r.random()
                if d > 2026.4959:
                    break
                b["demolished"] = d
                if r.random() < 0.34 and d < 2025.5:
                    extra.append((b, d + 0.25 + r.random() * 1.5))
                break
    by_b = {}
    for u in units:
        by_b.setdefault(u["bid"], []).append(u)
    for b in buildings:
        if b.get("demolished"):
            for u in by_b[b["bid"]]:
                u["demolished"] = b["demolished"]
    for b, comp in extra:
        comp = min(comp, 2026.49)
        nb = dict(b, bid=len(buildings), comp=comp, demolished=None, rebuild_of=b["bid"])
        buildings.append(nb)
        units.append(dict(uid=len(units), bid=nb["bid"], muni=b["muni"], era=b["era"], type=b["type"], comp=comp,
                          unit="", demolished=None))


def _geography(units, buildings, rng):
    """census tracts, block groups and blocks (the 2020 delineation): each municipality's subdivisions in building
    order, block groups of about 420 dwellings, a block group holding fewer than 120 dwellings in 2020 joined to its
    neighbour; post offices and ZIP codes by era"""
    tract_no = 9501
    by_m = {}
    for b in buildings:
        by_m.setdefault(b["muni"], []).append(b)
    for mi, (code, name, kind, eras) in enumerate(W.MUNIS):
        r = np.random.default_rng(W.SEED + 11 + 37 * mi)
        bs = sorted(by_m[name], key=lambda b: (b["era"], b["comp"], b["bid"]))
        chunks, cur, n = [], [], 0
        for b in bs:
            if n >= 420:
                chunks.append(cur)
                cur, n = [], 0
            cur.append(b)
            n += b["size"]
        chunks.append(cur)
        merged = []
        for c in chunks:
            n20 = sum(b["size"] for b in c if b["comp"] < 2020.25)
            if merged and n20 < 120:
                merged[-1].extend(c)
            else:
                merged.append(c)
        # infill: one building in ten sits in the neighbouring block group
        for i, c in enumerate(merged):
            for b in c:
                j = i
                if len(merged) > 1 and r.random() < 0.10:
                    j = min(max(i + int(r.choice([-1, 1])), 0), len(merged) - 1)
                b["bgi"] = j
        groups = [[] for _ in merged]
        for c in merged:
            for b in c:
                groups[b["bgi"]].append(b)
        k = 0
        while k < len(groups):
            per = int(r.integers(2, 5))
            tr = "%04d00" % tract_no
            tract_no += 1
            for bgn, grp in enumerate(groups[k:k + per], 1):
                grp.sort(key=lambda b: (b["comp"], b["bid"]))
                for j, b in enumerate(grp):
                    b["tract"], b["bg"] = tr, str(bgn)
                    b["block"] = "%d%03d" % (bgn, 1 + j // 9)
            k += per
        po = W.POSTAL[name]
        for b in bs:
            city = po[b["era"]]
            zips = W.POST[city]
            b["postal"] = city
            b["zip"] = zips[0] if len(zips) == 1 else zips[(b["bid"] // 7) % len(zips)]
    for u in units:
        b = buildings[u["bid"]]
        u["geoid_bg"] = W.STATE_FIPS + W.COUNTY_FIPS + b["tract"] + b["bg"]
        u["geoid_block"] = W.STATE_FIPS + W.COUNTY_FIPS + b["tract"] + b["block"]


def _boundaries(units, buildings):
    """the municipality each dwelling stood in on any date: the annexations move the first dwellings of an era of the
    losing municipality, and the Ivydale consolidation folds the Town of Ivydale into the Village"""
    moves = {}
    for when, frm, to, era, n in W.ANNEX:
        cand = sorted((u for u in units if u["muni"] == frm and u["era"] == era), key=lambda u: (u["comp"], u["uid"]))
        bids = []
        for u in cand:
            if u["bid"] not in bids:
                bids.append(u["bid"])
            if len(bids) >= n:
                break
        for u in units:
            if u["bid"] in bids:
                u["muni"] = to
                moves[u["uid"]] = (when, frm, to)
        for b in buildings:
            if b["bid"] in bids:
                b["muni"] = to
    for u in units:
        u["annexed"] = moves.get(u["uid"])
        u["ivy_town"] = u["muni"] == "Village of Ivydale" and u["era"] == 1
    return moves


def muni_on(u, date):
    """the municipality a dwelling stood in on a date (the census's boundaries of that date)"""
    if u["annexed"] and date < u["annexed"][0]:
        return u["annexed"][1]
    if u["ivy_town"] and date < W.CONSOLIDATION:
        return W.IVY_TOWN[1]
    return u["muni"]


def standing(u, x):
    return u["comp"] <= x and (u["demolished"] is None or u["demolished"] > x)


@functools.lru_cache(maxsize=None)
def households(date):
    """occupied flag and household size of every dwelling at a date (decimal year), each municipality its own draw"""
    w = world()
    x = yfrac(date)
    key = {W.C2000: 1, W.C2010: 2, W.C2020: 3, W.EST: 9}[date]
    occ = np.zeros(len(w["units"]), bool)
    size = np.zeros(len(w["units"]), int)
    by_m = {}
    for u in w["units"]:
        by_m.setdefault(u["muni"], []).append(u)
    for mi, (code, name, kind, eras) in enumerate(W.MUNIS):
        r = np.random.default_rng(W.SEED * 100 + key * 20 + mi)
        for u in by_m.get(name, []):
            o = r.random() < W.OCC[u["type"]]
            m = float(pph(u["type"], x - u["comp"]))
            s = 1 + int(r.poisson(max(m - 1, 0.05)))
            if standing(u, x) and o:
                occ[u["uid"]] = True
                size[u["uid"]] = s
    return occ, size


def gq_on(date):
    """group quarters residents by facility at a census or on the Center's 2026 survey"""
    k = {W.C2000: 0, W.C2010: 1, W.C2020: 2, W.EST: 3}[date]
    return [(f, t, m, e, v[k]) for (f, t, m, e, v) in W.GQ]


def truth():
    """each municipality's residents on 1 July 2026: its households' members and its group quarters residents"""
    w = world()
    occ, size = households(W.EST)
    out = {m[1]: 0 for m in W.MUNIS}
    for u in w["units"]:
        out[u["muni"]] += int(size[u["uid"]])
    for f, t, m, e, v in gq_on(W.EST):
        out[m] += v
    return out


WRITE_SHARE = 0.66      # the share of residents outside a post office's namesake who write their municipality


def written_city(u_or_muni, postal, r, share=None):
    """the city a mother or an informant writes on the record: the post office's city, or for one resident in about
    two and a half outside a namesake municipality, the municipality's own name in one of its written forms"""
    muni = u_or_muni
    short = W.SHORT[muni].upper()
    if postal == short:
        return postal if r.random() < 0.8 else W.SHORT[muni]
    if r.random() < (WRITE_SHARE if share is None else share):
        forms = [W.SHORT[muni], short, muni, "%s %s" % (short, {"town": "TWP", "village": "VLG", "city": "CITY"}[
            [m for m in W.MUNIS if m[1] == muni][0][2]])]
        return forms[int(r.integers(0, len(forms)))]
    return postal if r.random() < 0.7 else postal.title()


@functools.lru_cache(maxsize=None)
def vital():
    """births to and deaths of county residents from mid-June 2025 to early August 2026: births where young
    households live, deaths where the stock (and so its residents) is old, and in the nursing facilities"""
    w = world()
    occ, size = households(W.EST)
    x = yfrac(W.EST)
    r = np.random.default_rng(W.SEED + 101)
    lo, hi = yfrac(dt.date(2025, 6, 10)), yfrac(dt.date(2026, 8, 10))
    span = hi - lo
    births, deaths = [], []
    for u in w["units"]:
        if not occ[u["uid"]]:
            continue
        b = w["buildings"][u["bid"]]
        gg = float(g(x - u["comp"]))
        young = float(np.exp(-max(x - u["comp"], 0.0) / 6.0))
        rate = {"SF": 0.016 + 0.120 * young, "TH": 0.019 + 0.095 * young, "AP": 0.026 + 0.060 * young, "MH": 0.021}[u["type"]]
        start = max(lo, u["comp"] + 0.04)
        live = max(hi - start, 0.0)
        nb = r.poisson(rate * live * min(size[u["uid"]], 6) / 3.0)
        for _ in range(nb):
            births.append(dict(uid=u["uid"], when=start + r.random() * live, twin=r.random() < 0.03,
                               mage=int(np.clip(r.normal(30 - 4 * (1 - gg), 5), 16, 46)), sex="MF"[int(r.integers(0, 2))]))
        drate = 0.003 + 0.0105 * (1 - min(gg, 1.0)) ** 1.5
        nd = r.poisson(drate * live * size[u["uid"]])
        for _ in range(nd):
            deaths.append(dict(uid=u["uid"], gq=None, when=start + r.random() * live,
                               age=int(np.clip(r.normal(77 - 25 * gg, 12), 0, 104)), sex="MF"[int(r.integers(0, 2))]))
    for f, t, m, e, v in gq_on(W.EST):
        rate = {"Nursing facility": 0.29, "Correctional facility for adults": 0.002, "Group home": 0.02,
                "College residence hall": 0.0004}[t]
        for _ in range(r.poisson(rate * span * v)):
            deaths.append(dict(uid=None, gq=f, when=lo + r.random() * span,
                               age=int(np.clip(r.normal(86 if t == "Nursing facility" else 50, 7), 18, 105)),
                               sex="MF"[int(r.integers(0, 2))]))
    births.sort(key=lambda e: e["when"])
    deaths.sort(key=lambda e: e["when"])
    return births, deaths
