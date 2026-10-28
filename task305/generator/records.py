"""The main call's records: Census 2021 households and centroids by output area, the provider's spend estimates, the
ONSPD extract, the VOA rating list (list entries and summary valuations), the estate, the card feed and the shortlist.
Every record is cut from the world in world.py; nothing here is placed to be caught."""
import datetime as dt
import math

import numpy as np

import params as P
import world as Wd

LETTERS = "ABDEFGHJLNPQRSTUWXYZ"
STREETS = ["High Street", "Church Street", "Station Road", "Mill Lane", "Market Place", "Victoria Road", "King Street",
           "Bridge Street", "London Road", "Park Road", "Queen Street", "North Street", "School Lane", "Castle Street",
           "Chapel Street", "West Street", "New Road", "Green Lane", "The Square", "Broad Street", "Sheep Street",
           "Westgate", "Eastgate", "Northgate", "Southgate", "Fore Street", "Pound Lane", "Crown Street", "Albert Road",
           "Mount Pleasant", "Forge Lane", "Union Street", "Brook Street", "Bell Lane", "Wharf Road", "Orchard Way",
           "Fenton Road", "Sutton Road", "Westway", "Northfield", "Tanners Row", "Cattle Market", "Bowling Green Lane"]
VSTREETS = ["Main Street", "Church Lane", "Church Road", "The Green", "School Lane", "Back Lane", "Low Road", "High Street",
            "Mill Lane", "Station Road", "Chapel Lane", "Manor Road", "Moor Lane", "Fen Lane", "Marsh Lane", "North End",
            "Hall Lane", "Long Lane", "Carr Lane", "Field Lane", "Westfield Road", "Sandy Lane"]
N_HEREDITAMENTS = 4200        # the list's non-domestic entries apart from the grocery stores, parks and filling stations
GRID_E = lambda x: int(round(P.E0 + 1000 * x))
GRID_N = lambda y: int(round(P.N0 + 1000 * y))


def geography():
    """codes, sectors and unit postcodes on the world's output areas, plus postcodes for every store, site and park"""
    rs, oas = Wd.build()
    gs = np.random.default_rng(P.SEED + 11)
    towns = [t[0] for t in P.TOWNS]
    dist_of = {t: "%s%d" % (P.AREA, i + 1) for i, t in enumerate(towns)}
    rural = [("%s%d" % (P.AREA, 13 + i), x, y) for i, (x, y) in
             enumerate([(12, 38), (30, 40), (56, 36), (64, 24), (46, 10), (20, 6), (6, 26), (30, 20)])]
    for i, o in enumerate(oas):
        o["oa"] = "E00%06d" % (195004 + 3 * i + (i % 3))
        if o["town"]:
            o["sector"] = "%s %d" % (dist_of[o["town"]], o["sec"] + 1)
        else:
            d = min(rural, key=lambda r: (r[1] - o["x"]) ** 2 + (r[2] - o["y"]) ** 2)
            o["sector"] = "%s %d" % (d[0], (0 if o["x"] < d[1] else 1) + (0 if o["y"] < d[2] else 2) + 1)
    by_sec = {}
    for o in oas:
        by_sec.setdefault(o["sector"], []).append(o)
    # the villages' parishes: one seat per parish spread over the countryside, each village output area in the parish
    # of its nearest seat
    vill = [o for o in oas if not o["town"]]
    seats = [vill[0]]
    while len(seats) < len(P.PARISHES):
        seats.append(max(vill, key=lambda o: min((o["x"] - q["x"]) ** 2 + (o["y"] - q["y"]) ** 2 for q in seats)))
    for o in oas:
        if o["town"]:
            o["place"] = o["town"]
        else:
            k = min(range(len(seats)), key=lambda i: (seats[i]["x"] - o["x"]) ** 2 + (seats[i]["y"] - o["y"]) ** 2)
            o["place"] = P.PARISHES[k]
    place_of = {o["oa"]: o["place"] for o in oas}
    li = 0
    for sec in sorted(by_sec, key=lambda s: (int(s.split()[0][2:]), int(s.split()[1]))):
        for j, o in enumerate(sorted(by_sec[sec], key=lambda o: (o["x"], o["y"]))):
            if j % 5 == 0:
                li += 1
            o["lsoa"] = "E01%06d" % (36120 + 3 * li)
    used, pcs, where = set(), [], {}

    def newpc(sector, x, y, oa, lsoa, usertype=0, intro=None):
        while True:
            pc = "%s %s%s%s" % (sector.split()[0], sector.split()[1], gs.choice(list(LETTERS)), gs.choice(list(LETTERS)))
            if pc not in used:
                used.add(pc)
                where[pc] = place_of[oa]
                pcs.append(dict(pcds=pc, oa21=oa, lsoa21=lsoa, east=GRID_E(x), north=GRID_N(y), doterm="",
                                usertype=usertype, dointr=intro or "%d%02d" % (int(gs.integers(1980, 2020)),
                                                                              int(gs.integers(1, 13)))))
                return pc
    for o in oas:
        o["pcs"] = [newpc(o["sector"], o["x"] + gs.normal(0, .22), o["y"] + gs.normal(0, .22), o["oa"], o["lsoa"])
                    for _ in range(int(gs.integers(4, 10)))]

    def nearest(x, y, town=None):
        return min((o for o in oas if town is None or o["town"] == town),
                   key=lambda o: (o["x"] - x) ** 2 + (o["y"] - y) ** 2)

    jr = np.random.default_rng(P.SEED + 77)

    def place(x, y, usertype=0, intro=None, town=None):
        """a postcode at the point (its address point, a few tens of metres off the planner's grid), in the output
        area nearest to it within its own town"""
        o = nearest(x, y, town)
        x, y = x + float(jr.uniform(-0.045, 0.045)), y + float(jr.uniform(-0.045, 0.045))
        return newpc(o["sector"], x, y, o["oa"], o["lsoa"], usertype, intro)
    st = Wd.stores_now()
    ar = np.random.default_rng(P.SEED + 78)
    for s in st:
        s["pc"] = place(s["x"], s["y"], 1 if s["kind"] == "own" else int(gs.uniform() < .5), town=s["town"])
        # the valuation officer's measured area, to the hundredth of a square metre
        s["area"] = round(s["area"] * (1 + float(ar.uniform(-0.012, 0.012))), 2)
    hr = np.random.default_rng(P.SEED + 84)
    for s in st:
        if s["kind"] == "own" and s["id"] in P.OWN_STEPS:
            # each version of the entry measured when it was valued: the 2025 store and each 2026 extension
            s["area_2025"] = round(P.OWN_2025[s["id"]] * (1 + float(hr.uniform(-0.012, 0.012))), 2)
            s["area_steps"] = [(d, round(a * (1 + float(hr.uniform(-0.012, 0.012))), 2)) for d, a in
                               P.OWN_STEPS[s["id"]][:-1]] + [(P.OWN_STEPS[s["id"]][-1][0], s["area"])]
    sites = {}
    for site in P.SITES:
        sites[site[0]] = place(site[3], site[4], 0, "202%d%02d" % (int(gs.integers(3, 6)), int(gs.integers(1, 13))),
                               town=site[2])
    parks = {}
    for p in P.PARKS:
        parks[p[0]] = place(p[1], p[2], 1 if p[3] > 200 else 0)
    dc = place(P.DC[1], P.DC[2], 1, town="Loderwell")
    # terminated postcodes: re-coded streets, demolished blocks; each with its successor nearby
    live = list(pcs)
    for k in range(64):
        p = live[int(gs.integers(0, len(live)))]
        q = dict(p)
        out, inn = p["pcds"].split()
        q["pcds"] = "%s %s%s%s" % (out, inn[0], gs.choice(list(LETTERS)), gs.choice(list(LETTERS)))
        if q["pcds"] in used:
            continue
        used.add(q["pcds"])
        y0 = int(gs.integers(1985, 2012))
        q["dointr"] = "%d%02d" % (y0, int(gs.integers(1, 13)))
        q["doterm"] = "%d%02d" % (int(gs.integers(y0 + 2, 2026)), int(gs.integers(1, 13)))
        q["usertype"] = 0
        pcs.append(q)
        where[q["pcds"]] = where[p["pcds"]]
    seat_xy = [(P.PARISHES[i], q["x"], q["y"]) for i, q in enumerate(seats)]
    return dict(oas=oas, pcs=pcs, stores=st, sites=sites, parks=parks, dc=dc, dist_of=dist_of, rural=rural, where=where,
                seats=seat_xy)


def pcd7(pc):
    out, inn = pc.split()
    return (out + " " * (4 - len(out)))[:4] + inn if len(out) < 4 else out + inn


def onspd_rows(G):
    rows = []
    qs = np.random.default_rng(P.SEED + 82)
    for p in sorted(G["pcs"], key=lambda p: (p["pcds"].split()[0][:2], int(p["pcds"].split()[0][2:]), p["pcds"].split()[1])):
        out, inn = p["pcds"].split()
        # most references sit within a matched building; a few rural and newer postcodes are placed less precisely
        q = qs.uniform()
        grd = 1 if q < .9 else (2 if q < .95 else (3 if q < .985 else 4))
        rows.append([pcd7(p["pcds"]), (out + " " * (5 - len(out))) + inn if len(out) < 5 else out + inn, p["pcds"],
                     p["dointr"], p["doterm"], p["usertype"], p["east"], p["north"], grd, p["oa21"], p["lsoa21"], P.LAD])
    return rows


# ----------------------------------------------------------------- the VOA rating list
DESCS = [  # description, code, scat, share, unit, area range m2, rate per m2
    ("SHOP AND PREMISES", "CS", "249", .29, "m2", (18, 260), 120), ("OFFICES AND PREMISES", "CO", "203", .13, "m2", (30, 1400), 95),
    ("WAREHOUSE AND PREMISES", "CW", "096", .07, "m2", (120, 6000), 38), ("WORKSHOP AND PREMISES", "IW", "096", .08, "m2", (40, 900), 45),
    ("FACTORY AND PREMISES", "IF", "096", .03, "m2", (200, 9000), 30), ("PUBLIC HOUSE AND PREMISES", "LP", "226", .03, "", None, None),
    ("RESTAURANT AND PREMISES", "CR", "227", .03, "m2", (40, 300), 110), ("CAFE AND PREMISES", "CR", "227", .03, "m2", (25, 160), 105),
    ("CAR PARK AND PREMISES", "CP", "176", .02, "spaces", (10, 300), 260), ("ADVERTISING RIGHT", "CA", "010", .03, "", None, None),
    ("COMMUNICATION STATION AND PREMISES", "NT", "189", .02, "", None, None), ("STORE AND PREMISES", "CS", "096", .05, "m2", (15, 500), 32),
    ("LAND USED FOR STORAGE AND PREMISES", "LS", "153", .02, "m2", (200, 4000), 6),
    ("VEHICLE REPAIR WORKSHOP AND PREMISES", "IW", "182", .03, "m2", (60, 700), 48),
    ("HAIRDRESSING SALON AND PREMISES", "CS", "249", .03, "m2", (20, 110), 100), ("SURGERY AND PREMISES", "MS", "197", .01, "m2", (90, 900), 85),
    ("HOTEL AND PREMISES", "LH", "084", .005, "", None, None), ("SHOWROOM AND PREMISES", "CS", "249", .015, "m2", (80, 1500), 70),
    ("SCHOOL AND PREMISES", "ED", "250", .01, "", None, None), ("PETROL FILLING STATION AND PREMISES", "CG", "211", .007, "", None, None),
    ("KENNELS AND PREMISES", "LX", "122", .004, "", None, None), ("STABLES AND PREMISES", "LX", "214", .006, "", None, None),
    ("BEAUTY SALON AND PREMISES", "CS", "249", .02, "m2", (20, 120), 95), ("TAKEAWAY AND PREMISES", "CS", "249", .02, "m2", (25, 120), 115),
    ("SUPERMARKET AND PREMISES", "CS", "249", .0016, "m2", (110, 270), 140)]


def rating_list(G):
    gs = np.random.default_rng(P.SEED + 23)
    ps = np.array([d[3] for d in DESCS]); ps /= ps.sum()
    oas = G["oas"]
    town_pc = [pc for o in oas if o["town"] for pc in o["pcs"]]
    vill_pc = [pc for o in oas if not o["town"] for pc in o["pcs"]]
    where = G["where"]
    rural = {pc for o in oas if not o["town"] for pc in o["pcs"]} | set(G["parks"].values())
    rows, smv = [], []
    ed = np.random.default_rng(P.SEED + 79)
    uarn = 10052000
    ref = 1000
    ent = 0

    meta = []

    def add(desc, code, scat, pc, firm, measure, unit, rv, town=None, name=None, road=None, stable=False,
            eff_on=None, hist=None):
        nonlocal uarn, ref, ent
        uarn += int(gs.integers(1, 40))
        ref += int(gs.integers(1, 9))
        ent += 1
        num = str(int(gs.integers(1, 180))) if gs.uniform() < .7 else gs.choice(["Unit %d" % int(gs.integers(1, 12)), "Land at", "Part"])
        street = (VSTREETS if pc in rural else STREETS)[int(gs.integers(0, len(VSTREETS if pc in rural else STREETS)))]
        num, street = name or num, road or street
        loc = (town or where[pc]).upper()
        alt = "" if gs.uniform() < .82 else "%02d-%s-%d" % (int(gs.integers(1, 28)), gs.choice(["APR", "MAY", "JUN", "JUL", "AUG", "SEP"]), 2026)
        if stable:
            alt = ""                                  # the grocery stores and the parks stand as compiled
        eff = "01-APR-2026"
        if eff_on is not None:                        # altered in 2026: effective that day, the list altered days later
            eff = eff_on.strftime("%d-%b-%Y").upper()
            alt = (eff_on + dt.timedelta(days=int(gs.integers(9, 30)))).strftime("%d-%b-%Y").upper()
        if alt and ed.uniform() < .55:
            # an alteration takes effect on or before the day the list is altered
            mon = ["APR", "MAY", "JUN", "JUL", "AUG", "SEP"]
            m_alt, d_alt = mon.index(alt[3:6]), int(alt[:2])
            m_eff = int(ed.integers(0, m_alt + 1))
            lo = 2 if m_eff == 0 else 1
            hi = d_alt if m_eff == m_alt else 28
            eff = "%02d-%s-2026" % (int(ed.integers(lo, hi + 1)) if hi >= lo else hi, mon[m_eff])
        rows.append([ent, "3510", "", "%011d" % (ref * 1000 + 1), code, desc, uarn,
                     ("%s, %s, %s, %s" % (num, street, loc, pc)).upper(), firm.upper(), num.upper(), street.upper(), loc, "",
                     "", pc, eff, "", rv, "", "%d" % (16200000 + ent * 7), alt, scat + "G", "", "", "", "",
                     eff, ""])
        if unit:
            smv.append([uarn, "%d" % (16200000 + ent * 7), scat + "G", "%.2f" % measure if unit == "m2" else measure, unit])
        meta.append(dict(row=rows[-1], measure=measure, unit=unit, rv=rv, scat=scat + "G", hist=hist,
                         altered=bool(alt) or eff != "01-APR-2026"))
        return uarn
    for j in range(N_HEREDITAMENTS):
        d = DESCS[int(gs.choice(len(DESCS), p=ps))]
        pc = town_pc[int(gs.integers(0, len(town_pc)))] if gs.uniform() < .8 else vill_pc[int(gs.integers(0, len(vill_pc)))]
        measure, unit = "", d[4]
        if d[5]:
            lo, hi = d[5]
            measure = math.exp(gs.uniform(math.log(lo), math.log(hi)))
            measure = round(measure, 2) if unit == "m2" else int(round(measure))
            rv = int(round(measure * d[6] * gs.uniform(0.6, 1.4) / 50.0)) * 50
        else:
            rv = int(round(math.exp(gs.uniform(math.log(1500), math.log(90000))) / 50.0)) * 50
        firm = ""
        if d[0] == "SUPERMARKET AND PREMISES":
            firm = gs.choice(["Village Stores", "The Village Shop", "Post Office and Stores", "General Stores",
                              "Community Shop"] if pc in rural else ["Corner Stores", "Food and Wine", "Mini Market",
                                                                     "Convenience Store", "Late Shop"]) \
                if gs.uniform() < .3 else ""
        add(d[0], d[1], d[2], pc, firm, measure, unit, max(rv, 500))
    for s in G["stores"]:
        kind = "SUPERSTORE AND PREMISES" if s["area"] >= 2000 else (
            "FOOD STORE AND PREMISES" if s["kind"] == "comp" and s["area"] < 1000 else "SUPERMARKET AND PREMISES")
        firm = "Marrable Foodstores Ltd" if s["kind"] == "own" else {"Fairbasket": "Fairbasket Ltd", "Brightmart": "Brightmart Retail Ltd",
                                                                   "Pettifer's": "", "Valuewise": "Valuewise Stores Ltd"}[s["fascia"]]
        rv = int(round(s["area"] * gs.uniform(105, 132) / 250.0)) * 250
        road = STREETS[int(s["id"]) % len(STREETS)] if s["kind"] == "own" else None
        number = str(3 + (sum(map(ord, s["id"])) * 37) % 140)
        steps = s.get("area_steps") if s["kind"] == "own" else None
        hist = None
        if steps:
            # the 2023 list's state to its close, then each 2026 version before the one now current
            first = s["area_2025"]
            hist = [(P.LIST_2023[0], P.LIST_2023[1], first), (P.LIST_2026, steps[0][0] - dt.timedelta(days=1), first)]
            for (d0, a0), (d1, _) in zip(steps, steps[1:]):
                hist.append((d0, d1 - dt.timedelta(days=1), a0))
        s["uarn"] = add(kind, "CS", "217" if s["area"] < 2000 else "218", s["pc"], firm, s["area"], "m2", rv, s["town"],
                        name=number, road=road, stable=True, eff_on=steps[-1][0] if steps else None, hist=hist)
    for name, x, y, n, desc in P.PARKS:
        rv = int(round(n * (330 if "CARAVAN PARK" in desc else 150) / 250.0)) * 250
        step = P.PARK_STEPS.get(name)
        hist = None
        if step:
            was = P.PARKS_2025[name]
            hist = [(P.LIST_2023[0], P.LIST_2023[1], was), (P.LIST_2026, step - dt.timedelta(days=1), was)]
        add(desc, "LC", "045" if "CARAVAN PARK" in desc else "049", G["parks"][name], "", n, "pitches", rv,
            name=name, road=P.PARK_ROAD[name], stable=True, eff_on=step, hist=hist)
    for s in G["stores"]:
        if s["kind"] == "own" and s["id"] in ("101", "102", "104"):
            add("PETROL FILLING STATION AND PREMISES", "CG", "211", s["pc"], "Marrable Foodstores Ltd", "", "",
                int(round(gs.uniform(38000, 61000) / 250.0)) * 250, s["town"], road=STREETS[int(s["id"]) % len(STREETS)])
    order = gs.permutation(len(rows))
    rows = [rows[i] for i in order]
    for i, r in enumerate(rows):
        r[0] = i + 1
    # the list's reference numbers were issued over decades: UARNs, billing authority references and assessment
    # references carry no order of their own
    ns = np.random.default_rng(P.SEED + 81)
    uarns = {}
    for v in sorted({r[6] for r in rows}):
        u = int(ns.integers(1000000, 99999999))
        while u in uarns.values():
            u = int(ns.integers(1000000, 99999999))
        uarns[v] = u
    used_ref, used_ass = set(), set()
    ass_map = {}
    for r in rows:
        b = "%05d%06d" % (int(ns.integers(0, 600)), int(ns.integers(0, 999999)))
        while b in used_ref:
            b = "%05d%06d" % (int(ns.integers(0, 600)), int(ns.integers(0, 999999)))
        used_ref.add(b)
        r[3] = b
        a = "%d" % int(ns.integers(10000000, 29999999))
        while a in used_ass:
            a = "%d" % int(ns.integers(10000000, 29999999))
        used_ass.add(a)
        ass_map[r[19]] = a
        r[19] = a
        r[6] = uarns[r[6]]
    for m in smv:
        m[0], m[1] = uarns[m[0]], ass_map[m[1]]
    smv.sort(key=lambda r: r[0])
    hist_rows, hist_smv = [], []
    hs = np.random.default_rng(P.SEED + 83)

    def fmt(d):
        return d.strftime("%d-%b-%Y").upper()

    def version(m, frm, to, measure, rv):
        a = "%d" % int(ns.integers(10000000, 29999999))
        while a in used_ass:
            a = "%d" % int(ns.integers(10000000, 29999999))
        used_ass.add(a)
        r = list(m["row"])
        r[15], r[17], r[19], r[20] = fmt(frm), rv, a, ""
        r[26], r[27] = fmt(frm), fmt(to)
        hist_rows.append(r)
        if m["unit"]:
            hist_smv.append([r[6], a, m["scat"], "%.2f" % measure if m["unit"] == "m2" else measure, m["unit"]])

    for m in meta:
        rv23 = int(round(m["rv"] * hs.uniform(0.80, 0.92) / 50.0)) * 50
        if m["hist"]:
            for frm, to, meas in m["hist"]:
                rv = rv23 if to <= P.LIST_2023[1] else m["rv"]
                version(m, frm, to, meas, int(round(rv * (meas / m["measure"]) / 50.0)) * 50 if m["unit"] else rv)
            continue
        if hs.uniform() < 0.04:                       # altered once during the 2023 list
            mid = P.LIST_2023[0] + dt.timedelta(days=int(hs.integers(120, 1000)))
            version(m, P.LIST_2023[0], mid - dt.timedelta(days=1), m["measure"],
                    int(round(rv23 * hs.uniform(0.9, 1.1) / 50.0)) * 50)
            version(m, mid, P.LIST_2023[1], m["measure"], rv23)
        else:
            version(m, P.LIST_2023[0], P.LIST_2023[1], m["measure"], rv23)
        if m["altered"]:
            eff = dt.datetime.strptime(m["row"][15], "%d-%b-%Y").date()
            if eff > P.LIST_2026:
                version(m, P.LIST_2026, eff - dt.timedelta(days=1), m["measure"],
                        int(round(m["rv"] * hs.uniform(0.9, 1.1) / 50.0)) * 50)
    order = hs.permutation(len(hist_rows))
    hist_rows = [hist_rows[i] for i in order]
    for i, r in enumerate(hist_rows):
        r[0] = i + 1
    hist_smv.sort(key=lambda r: (r[0], r[1]))
    return rows, smv, hist_rows, hist_smv


# ----------------------------------------------------------------- the card feed
CITY = [("B", 98, 4.0), ("S", 36, 3.0), ("LS", 29, 2.5), ("NG", 25, 2.5), ("DE", 24, 2.0), ("LE", 19, 2.0),
        ("M", 46, 1.5), ("CV", 37, 1.5), ("WS", 15, 1.2), ("WF", 17, 1.2), ("BD", 24, 1.0), ("HU", 20, 1.0),
        ("YO", 62, .8), ("WV", 16, .8), ("DY", 14, .8), ("SE", 28, .8), ("N", 22, .8), ("E", 18, .7),
        ("NW", 11, .6), ("NN", 18, .6), ("MK", 46, .5), ("ST", 21, .5)]
NEAR = [("LN", 13, 3.0), ("PE", 38, 2.0), ("DN", 41, 1.5), ("NG", 34, 1.0), ("HU", 20, .8), ("S", 36, .6)]
GUEST_M = {"2025-04": .12, "2025-05": .12, "2025-06": .12, "2025-07": .19, "2025-08": .23, "2025-09": .11,
           "2025-10": .06, "2026-03": .05}


def _sector(gs, table):
    w = np.array([t[2] for t in table]); w = w / w.sum()
    a, n, _ = table[int(gs.choice(len(table), p=w))]
    return "%s%d %d" % (a, int(gs.integers(1, n + 1)), int(gs.integers(1, 10)))


def card_feed(G, T):
    """card spend at our stores by month and the home sector of the cardholder; residents' spend shared by the model
    from every output area, visitors of residents all year, and the guests of the holiday parks in the season"""
    gs = np.random.default_rng(P.SEED + 31)
    oas = G["oas"]
    st = [dict(s, area=s.get("area_2025", s["area"])) for s in G["stores"]]
    own = [k for k, s in enumerate(st) if s["kind"] == "own"]
    res_w = np.array([.083, .083, .081, .083, .084, .080, .082, .081, .094, .077, .074, .083]); res_w /= res_w.sum()
    flow = {st[k]["id"]: {} for k in own}
    for o in oas:
        sh = Wd.shares(o["x"], o["y"], st)
        for k in own:
            sid = st[k]["id"]
            flow[sid][o["sector"]] = flow[sid].get(o["sector"], 0.0) + Wd.resident_spend(o) * sh[k] * (1 + T["eps"][sid])
    rows = []
    for k in own:
        sid = st[k]["id"]
        cs = T["card"][sid]
        for sec in sorted(flow[sid], key=lambda s: (int(s.split()[0][2:]), int(s.split()[1]))):
            for m, wm in zip(P.MONTHS, res_w):
                spend = flow[sid][sec] * wm * cs * gs.normal(1, 0.025)
                cards = int(round(spend / gs.uniform(150, 230)))
                if cards < 1:
                    continue
                rows.append([sid, m, sec, cards, int(round(cards * gs.uniform(2.6, 5.4))), round(spend, 2)])
        vfr = sum(flow[sid].values()) * P.VFR * cs / 12.0
        guests = T["vis"][k] * cs * (1 + T["capture"][sid])
        for m in P.MONTHS:
            wv = gs.normal(1, 0.08)
            wg = GUEST_M.get(m, 0.0) * (1 + gs.normal(0, 0.05))
            for amount, table, per in ((vfr * wv, NEAR + CITY, (55, 90)), (guests * wg, CITY + NEAR[:2], (38, 62))):
                if amount <= 0:
                    continue
                n = max(1, int(amount / 140.0))
                parts = gs.gamma(1.3, 1.0, n)
                parts = parts / parts.sum() * amount
                agg = {}
                for a in parts:
                    sec = _sector(gs, table)
                    agg[sec] = agg.get(sec, 0.0) + a
                for sec, a in agg.items():
                    cards = max(1, int(round(a / gs.uniform(*per))))
                    rows.append([sid, m, sec, cards, int(round(cards * gs.uniform(1.4, 2.8))), round(a, 2)])
    merged = {}
    for r in rows:
        key = (r[0], r[1], r[2])
        if key in merged:
            m = merged[key]
            m[3] += r[3]; m[4] += r[4]; m[5] = round(m[5] + r[5], 2)
        else:
            merged[key] = list(r)
    out = sorted(merged.values(), key=lambda r: (r[0], r[1], r[2]))
    totals = {}
    for r in out:
        totals[r[0]] = totals.get(r[0], 0.0) + r[5]
    return out, totals
