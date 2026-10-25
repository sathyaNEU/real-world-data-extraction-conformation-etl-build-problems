"""The clean truth of task485 (architecture 2): every herd, every animal's life and movements over the programme
year 1 November 2025 to 31 October 2026, the census on 1 June 2026, each herd's farmed land, and the slurry
contractors' spring jobs. Nothing here is a file; pack.py cuts the files from it.

The world: an unnamed Atlantic country of twelve regions. Lowland dairy regions send their yearling heifers out on
summer grazing lets in May and house them at home all winter; the winter-finishing regions buy stores in autumn,
house them and send them to slaughter before June; the grassland let regions and the western regions take in the
summer lets, and the western rearers buy the dairy regions' calves in spring.
"""
import datetime as dt
from collections import defaultdict

import numpy as np

D = dt.date
Y0, Y1 = D(2025, 11, 1), D(2026, 10, 31)     # the programme year, inclusive
NDAY = (Y1 - Y0).days + 1
CENSUS_DATE = D(2026, 6, 1)
EXTRACT = D(2026, 11, 9)
LINE = 26.0                                     # kg NH3 a hectare of farmed land, the programme's line
WIN0, WIN1 = D(2026, 1, 13), D(2026, 4, 30)     # the ask's spreading window
SEED = 4485


def di(d):
    return (d - Y0).days


def dd(i):
    return Y0 + dt.timedelta(int(i))


CENSUS = di(CENSUS_DATE)

# region, type, 2024 code, herd-number letter, (housing in), (housing out)
REGIONS = [
    ("Northern Vale", "D", "01", "N", (11, 6), (3, 18)), ("Eastern Vale", "D", "02", "E", (11, 3), (3, 22)),
    ("Southern Vale", "D", "03", "S", (11, 8), (3, 15)), ("Coastal Vale", "D", "04", "C", (11, 1), (3, 27)),
    ("Midland Basin", "B", "05", "M", (10, 30), (4, 8)), ("Inner Basin", "B", "06", "B", (11, 2), (4, 5)),
    ("Lower Basin", "B", "07", "L", (10, 28), (4, 12)),
    ("Lake Uplands", "G", "08", "K", (10, 22), (4, 24)), ("Middle Uplands", "G", "09", "D", (10, 19), (4, 28)),
    ("Eastern Uplands", "G", "10", "U", (10, 25), (4, 21)),
    ("Western Seaboard", "W", "11", "W", (10, 24), (4, 18)), ("Atlantic Coast", "W", "12", "A", (10, 20), (4, 23)),
]
REG = [r[0] for r in REGIONS]
RTYPE = {r[0]: r[1] for r in REGIONS}
RCODE = {r[0]: r[2] for r in REGIONS}
RLETTER = {r[0]: r[3] for r in REGIONS}
HOUSING = {r[0]: (r[4], r[5]) for r in REGIONS}
# 2024: three of Coastal Vale's districts moved to Southern Vale; their herds keep their L numbers
MOVED_DISTRICTS = ("0412", "0415", "0418")

# the factor note's mass flow: nitrogen excreted (kg N a head a day, housed and at grass; Table 1), the share of it
# that is ammoniacal and the share of that lost as ammonia-N at each stage (Table 2); Table 3's rates, kg NH3 a head a
# day, are rounded to four decimals and are the factors applied
NEX = {"dairy_cow": (0.2860, 0.4100), "suckler_cow": (0.1900, 0.1950), "over24": (0.1760, 0.1820),
       "m12_24": (0.1490, 0.1540), "calf": (0.0680, 0.0700)}
TAN_HOUSED, TAN_GRASS = 0.60, 0.70
EF_HOUSING, EF_STORAGE, EF_SPREADING, EF_GRAZING = 0.24, 0.12, 0.36, 0.08
NH3_PER_N = 17.0 / 14.0
CHAIN = EF_HOUSING + (1 - EF_HOUSING) * EF_STORAGE + (1 - EF_HOUSING) * (1 - EF_STORAGE) * EF_SPREADING
RATE = {c: (round(h * TAN_HOUSED * CHAIN * NH3_PER_N, 4), round(g * TAN_GRASS * EF_GRAZING * NH3_PER_N, 4))
        for c, (h, g) in NEX.items()}
CATS = list(RATE)
DAIRY_BREEDS = ("HO", "FR", "JE", "NR", "MO")
DAIRY_DRAW = ["HO", "HO", "HO", "HO", "FR", "FR", "JE", "NR", "HO", "MO"]
BEEF_DRAW = ["LM", "LM", "LM", "CH", "CH", "AA", "AA", "HE", "SI", "BB", "SH", "LM", "CH", "AU"]


def housed_vec(r):
    (im, idd), (om, od) = HOUSING[r]
    v = np.zeros(NDAY, bool)
    for i in range(NDAY):
        d = dd(i)
        v[i] = d >= D(d.year, im, idd) or d < D(d.year, om, od)
    return v


HOUSED = {r: housed_vec(r) for r in REG}
CUMH = {r: np.concatenate([[0], np.cumsum(HOUSED[r])]) for r in REG}


def housed_days(r):
    return int(HOUSED[r].sum())


def annual_factor(r, c):
    """the factor note's Table 5: kg NH3 a head a year for an animal kept in region r all year (365 days)"""
    h = housed_days(r)
    return h * RATE[c][0] + (NDAY - h) * RATE[c][1]


# ----------------------------------------------------------------------------------------------- the herds
MIX = {"D": [("dairy", 62, 88, 34), ("suckler", 18, 22, 9), ("rearer", 3, 60, 20), ("finisher", 3, 80, 25)],
       "B": [("suckler", 60, 24, 10), ("finisher", 44, 135, 45), ("rearer", 4, 70, 25), ("dairy", 6, 75, 25)],
       "G": [("suckler", 80, 22, 8), ("letland", 30, 0, 0), ("finisher", 4, 60, 20), ("dairy", 3, 58, 18)],
       "W": [("suckler", 50, 21, 9), ("dairy", 12, 72, 26), ("rearer", 22, 75, 25), ("letland", 14, 0, 0)]}
LET_DEST = {"Northern Vale": [("Lake Uplands", 0.6), ("Western Seaboard", 0.4)], "Eastern Vale": [("Lake Uplands", 0.5), ("Middle Uplands", 0.5)],
            "Southern Vale": [("Middle Uplands", 0.7), ("Eastern Uplands", 0.3)], "Coastal Vale": [("Eastern Uplands", 0.6), ("Atlantic Coast", 0.4)],
            "Midland Basin": [("Lake Uplands", 1.0)], "Inner Basin": [("Middle Uplands", 1.0)], "Lower Basin": [("Eastern Uplands", 1.0)],
            "Western Seaboard": [("Western Seaboard", 1.0)], "Atlantic Coast": [("Atlantic Coast", 1.0)]}
LET_SHARE = {"D": 0.62, "B": 0.12, "W": 0.25}
WEAN_DEST = {"Lake Uplands": [("Midland Basin", 0.7), ("Northern Vale", 0.15), ("Lake Uplands", 0.15)],
             "Middle Uplands": [("Inner Basin", 0.7), ("Eastern Vale", 0.15), ("Middle Uplands", 0.15)],
             "Eastern Uplands": [("Lower Basin", 0.7), ("Southern Vale", 0.15), ("Eastern Uplands", 0.15)],
             "Western Seaboard": [("Midland Basin", 0.5), ("Western Seaboard", 0.5)], "Atlantic Coast": [("Lower Basin", 0.5), ("Atlantic Coast", 0.5)]}
CALF_ROUTE = (["Western Seaboard", "Atlantic Coast", "Midland Basin", "Inner Basin", "Lower Basin", None], [0.34, 0.34, 0.06, 0.06, 0.06, 0.14])
WINTER_SHARE = 0.67
# design targets: each region's golden kilograms a hectare as a multiple of the line (farmed land is set from them)
TARGET = {"Northern Vale": 1.22, "Eastern Vale": 1.15, "Southern Vale": 1.10, "Coastal Vale": 0.88, "Midland Basin": 1.32,
          "Inner Basin": 1.08, "Lower Basin": 1.09, "Lake Uplands": 0.93, "Middle Uplands": 0.91, "Eastern Uplands": 0.78,
          "Western Seaboard": 0.92, "Atlantic Coast": 0.77}


class World:
    pass


def build(seed=SEED):
    rng = np.random.default_rng(seed)
    w = World()
    herds = []

    def herd(region, typ, **kw):
        h = dict(id=len(herds), region=region, type=typ, **kw)
        herds.append(h)
        return h["id"]

    A = defaultdict(list)
    moves = []

    def animal(sex, breed, dam, birth, herd0, first_calf=None):
        a = len(A["sex"])
        for k, v in (("sex", sex), ("breed", breed), ("dam", dam), ("birth", birth), ("herd0", herd0), ("fc", first_calf),
                     ("exit", None), ("exit_type", None), ("exit_herd", None), ("loc", herd0), ("reg_lag", None),
                     ("role", None)):
            A[k].append(v)
        return a

    def move(a, to, day, lag=0, kind="FARM"):
        moves.append(dict(a=a, frm=A["loc"][a], dep=day, to=to, arr=day + lag, kind=kind, k=len(moves)))
        A["loc"][a] = to

    def exit_(a, day, typ, h):
        A["exit"][a], A["exit_type"][a], A["exit_herd"][a] = day, typ, h

    def bull(h, rng):
        a = animal("M", str(rng.choice(BEEF_DRAW)), None, di(D(2025, 3, 1)) - int(rng.integers(365 * 3, 365 * 8)), h)
        A["role"][a] = "bull"
        if rng.random() < 0.08:
            exit_(a, int(rng.integers(di(D(2026, 9, 1)), di(D(2026, 10, 31)))), "SL", int(rng.choice(factories)))
        return a

    marts = {r: herd(r, "mart") for r in REG}
    factories = [herd(r, "factory") for r in ("Midland Basin", "Southern Vale", "Inner Basin", "Western Seaboard", "Lower Basin")]
    export_c = [herd("Northern Vale", "export"), herd("Coastal Vale", "export")]
    knack = [herd(r, "knackery") for r in ("Eastern Vale", "Lower Basin", "Middle Uplands")]
    dealers = [herd(r, "dealer") for r in ("Midland Basin", "Inner Basin", "Eastern Vale", "Western Seaboard")]
    farms = defaultdict(list)
    used = set()
    for r in REG:
        while True:
            counts = [(typ, int(round(n * rng.uniform(0.86, 1.14))), m, s) for typ, n, m, s in MIX[RTYPE[r]]]
            tot = sum(c for _, c, _, _ in counts)
            if not {tot - 4, tot, tot + 4} & used:
                break
        used.add(tot)
        for typ, c, m, s in counts:
            for _ in range(c):
                size = max(6, int(rng.normal(m, s))) if m else 0
                farms[(r, typ)].append(herd(r, typ, size=size))

    def pick(r, typ):
        return int(rng.choice(farms[(r, typ)]))

    def wdest(r):
        opts = WEAN_DEST.get(r)
        if not opts:
            return r
        rs, ws = zip(*opts)
        return str(rng.choice(rs, p=np.array(ws) / sum(ws)))

    def finisher_in(r):
        return pick(r, "finisher") if farms[(r, "finisher")] else pick(r, "suckler")

    mart_wd = {r: k % 5 for k, r in enumerate(REG)}

    def mart_day(r, lo, hi):
        cands = [i for i in range(lo, hi + 1) if dd(i).weekday() == mart_wd[r]]
        return int(rng.choice(cands)) if cands else lo

    def sell_via_mart(a, src, dest, lo, hi, dealer_p=0.06):
        md = mart_day(src, lo, hi)
        move(a, marts[src], md, 0, "MART")
        if rng.random() < dealer_p:
            dl = int(rng.choice(dealers))
            move(a, dl, md, 0, "MART")
            move(a, dest, md + int(rng.integers(1, 5)), int(rng.integers(0, 2)), "DEALER")
        else:
            move(a, dest, md, int(rng.random() < 0.25), "MART")
        return md

    let_animals = []
    for r in REG:
        t = RTYPE[r]
        # ---- dairy herds
        for h in farms[(r, "dairy")]:
            n = herds[h]["size"]
            mcalv = int(rng.normal(di(D(2026, 2, 12)), 9))
            cows = []
            for _ in range(n):
                b = di(D(2025, 2, 1)) - int(rng.integers(365 * 2, 365 * 8))
                cows.append(animal("F", str(rng.choice(DAIRY_DRAW)), None, b, h, b + int(rng.normal(730, 40))))
            heif = [animal("F", str(rng.choice(DAIRY_DRAW)), None, int(rng.normal(di(D(2024, 2, 15)), 18)), h)
                    for _ in range(int(n * 0.24))]
            yl = [animal("F", str(rng.choice(DAIRY_DRAW)), None, int(rng.normal(di(D(2025, 2, 15)), 18)), h)
                  for _ in range(int(n * 0.25))]
            if rng.random() < 0.4:
                bull(h, rng)
            for a in heif:
                A["fc"][a] = 0          # set to the calf's birth below; cleared if she does not calve
                cows.append(a)
            calved = {}
            for a in cows:
                if rng.random() < 0.03:
                    if A["fc"][a] is not None and A["fc"][a] >= 0:
                        A["fc"][a] = None
                    continue
                cd = int(rng.normal(mcalv, 20))
                calved[a] = cd
                if A["fc"][a] is not None and A["fc"][a] >= 0:
                    A["fc"][a] = cd
                beef = rng.random() < 0.35
                sex = "F" if rng.random() < 0.5 else "M"
                br = (str(rng.choice(BEEF_DRAW)) + "X") if beef else A["breed"][a]
                c = animal(sex, br, a, cd, h)
                if rng.random() < 0.035:
                    exit_(c, cd + int(rng.integers(1, 30)), "DF", int(rng.choice(knack)))
                    continue
                sell = cd + int(rng.integers(14, 32))
                if (not beef) and sex == "F" and rng.random() < 0.72:
                    continue
                if (not beef) and sex == "M" and rng.random() < 0.45:
                    xc = int(rng.choice(export_c))
                    move(c, xc, sell, 0, "EXPORT")
                    exit_(c, sell + int(rng.integers(1, 3)), "EX", xc)
                    continue
                tr = str(rng.choice([x if x else r for x in CALF_ROUTE[0]], p=CALF_ROUTE[1]))
                dest = pick(tr, "rearer") if farms[(tr, "rearer")] else pick(tr, "suckler")
                if rng.random() < 0.5:
                    sell_via_mart(c, r, dest, sell, sell + 6)
                else:
                    move(c, dest, sell, 0)
            for a in cows:
                cd = calved.get(a)
                if rng.random() < 0.19:
                    u = rng.random()
                    if u >= 0.8 and cd is not None:
                        u = 0.6                 # a cow that calves this spring is not culled before it
                    d = int(rng.integers(di(D(2026, 4, 1)), di(D(2026, 6, 30)))) if u < 0.45 else (
                        int(rng.integers(di(D(2026, 9, 1)), di(D(2026, 10, 31)))) if u < 0.8 else int(rng.integers(0, di(D(2025, 12, 20)))))
                    if cd is not None:
                        d = max(d, cd + int(rng.integers(21, 50)))
                    exit_(a, d, "SL", int(rng.choice(factories)))
                elif rng.random() < 0.012:
                    d = int(rng.integers(0, NDAY))
                    if cd is not None and d <= cd:
                        d = min(NDAY - 1, cd + int(rng.integers(2, 200)))
                    exit_(a, d, "DF", int(rng.choice(knack)))
            share = LET_SHARE.get(t, 0)
            if share and rng.random() < 0.75:
                frac = min(1.0, share / 0.75 * rng.uniform(0.6, 1.4))
                dests = LET_DEST.get(r, [(r, 1.0)])
                dr = str(rng.choice([x for x, _ in dests], p=np.array([q for _, q in dests]) / sum(q for _, q in dests)))
                lh = pick(dr, "letland")
                out, back = int(rng.normal(di(D(2026, 5, 6)), 9)), int(rng.normal(di(D(2026, 10, 9)), 9))
                for a in yl:
                    if rng.random() < frac:
                        move(a, lh, out + int(rng.integers(-2, 3)), int(rng.random() < 0.2))
                        move(a, h, back + int(rng.integers(-2, 3)), int(rng.random() < 0.2))
                        let_animals.append(a)
        # ---- suckler herds and the let holdings' own herds
        for h in farms[(r, "suckler")] + farms[(r, "letland")]:
            n = herds[h]["size"] if herds[h]["type"] == "suckler" else int(rng.normal(14, 5))
            n = max(n, 4)
            mcalv = int(rng.normal(di(D(2026, 3, 18)), 12))
            cows = []
            for _ in range(n):
                b = di(D(2025, 3, 1)) - int(rng.integers(365 * 2, 365 * 10))
                cows.append(animal("F", str(rng.choice(BEEF_DRAW)), None, b, h, b + int(rng.normal(800, 60))))
            rep = [animal("F", str(rng.choice(BEEF_DRAW)), None, int(rng.normal(di(D(2024, 3, 15)), 20)), h)
                   for _ in range(int(n * 0.18))]
            for a in rep:
                A["fc"][a] = 0
                cows.append(a)
            for _ in range(int(n * 0.17)):
                animal("F", str(rng.choice(BEEF_DRAW)), None, int(rng.normal(di(D(2025, 3, 15)), 20)), h)
            for _ in range(1 + (n > 40)):
                bull(h, rng)
            calved = {}
            for a in cows:
                if rng.random() < 0.06:
                    if A["fc"][a] is not None and A["fc"][a] >= 0:
                        A["fc"][a] = None
                    continue
                cd = int(rng.normal(mcalv, 22))
                calved[a] = cd
                if A["fc"][a] is not None and A["fc"][a] >= 0:
                    A["fc"][a] = cd
                c = animal("F" if rng.random() < 0.5 else "M", A["breed"][a], a, cd, h)
                if rng.random() < 0.03:
                    exit_(c, cd + int(rng.integers(1, 60)), "DF", int(rng.choice(knack)))
                    continue
                if A["sex"][c] == "F" and rng.random() < 0.2:
                    continue
                dest = finisher_in(wdest(r) if t in ("G", "W") else r)
                sell_via_mart(c, r, dest, di(D(2026, 10, 1)), di(D(2026, 10, 30)))
            for a in cows:
                if rng.random() < 0.14:
                    early = rng.random() >= 0.65 and a not in calved
                    d = int(rng.integers(0, di(D(2025, 12, 15)))) if early else int(rng.integers(di(D(2026, 9, 10)), di(D(2026, 10, 31))))
                    exit_(a, d, "SL", int(rng.choice(factories)))
        # ---- finishers
        for h in farms[(r, "finisher")]:
            n = herds[h]["size"]
            nw = int(n * WINTER_SHARE)
            for _ in range(nw):
                a = animal(str(rng.choice(["M", "F"], p=[0.7, 0.3])), str(rng.choice(BEEF_DRAW)) + str(rng.choice(["", "X"])),
                           None, int(rng.normal(di(D(2024, 3, 20)), 25)), h)
                exit_(a, int(rng.normal(di(D(2026, 3, 25)), 28)), "SL", int(rng.choice(factories)))
            for _ in range(n - nw):
                a = animal(str(rng.choice(["M", "F"], p=[0.6, 0.4])), str(rng.choice(BEEF_DRAW)), None,
                           int(rng.normal(di(D(2025, 3, 20)), 25)), h)
                u = rng.random()
                if u < 0.15:
                    exit_(a, int(rng.normal(di(D(2026, 9, 20)), 20)), "SL", int(rng.choice(factories)))
                elif u < 0.30:
                    sell_via_mart(a, r, finisher_in(str(rng.choice([x for x in REG if RTYPE[x] == "B"]))),
                                  di(D(2026, 9, 1)), di(D(2026, 10, 30)))
                elif u < 0.30 + LET_SHARE.get("B", 0) * (t == "B"):
                    lh = pick(LET_DEST[r][0][0], "letland")
                    move(a, lh, int(rng.normal(di(D(2026, 5, 10)), 8)), 0)
                    move(a, h, int(rng.normal(di(D(2026, 10, 6)), 8)), 0)
                    let_animals.append(a)
        # ---- rearers: last spring's calves as yearlings, sold as stores in the autumn
        for h in farms[(r, "rearer")]:
            for _ in range(herds[h]["size"]):
                a = animal("M" if rng.random() < 0.8 else "F", str(rng.choice(["HO", "FR", "AAX", "HEX", "LMX"])), None,
                           int(rng.normal(di(D(2025, 2, 20)), 20)), h)
                if rng.random() < 0.55:
                    sell_via_mart(a, r, finisher_in(str(rng.choice([x for x in REG if RTYPE[x] == "B"]))),
                                  di(D(2026, 9, 1)), di(D(2026, 10, 30)))
    w.herds, w.A, w.moves, w.let_animals = herds, A, moves, let_animals
    w.farms = farms
    w.rng = rng
    return w


# --------------------------------------------------------------------------------- presence and the routes
def category(A, a, day):
    age = day - A["birth"][a]
    if age < 365:
        return "calf"
    fc = A["fc"][a]
    if A["sex"][a] == "F" and fc is not None and fc <= day:
        return "dairy_cow" if A["breed"][a] in DAIRY_BREEDS else "suckler_cow"
    return "m12_24" if age < 730 else "over24"


def intervals(A, moves, n_animals=None):
    """each animal's (herd, start, end) day intervals inside the programme year: in its departure herd until its
    arrival date, present from its birth date, gone from its exit date"""
    by_a = defaultdict(list)
    for m in moves:
        by_a[m["a"]].append((m["arr"], m["k"], m["to"]))
    out = {}
    for a in range(n_animals if n_animals is not None else len(A["sex"])):
        s = max(A["birth"][a], 0)
        e = A["exit"][a] if A["exit"][a] is not None else NDAY
        e = min(e, NDAY)
        if s >= NDAY or e <= 0 or e <= s:
            continue
        cur, t, iv = A["herd0"][a], s, []
        for arr, k, to in sorted(by_a[a]):
            if arr <= t:
                cur = to
                continue
            if arr >= e:
                break
            iv.append((cur, t, arr))
            cur, t = to, arr
        iv.append((cur, t, e))
        out[a] = [x for x in iv if x[1] < x[2]]
    return out


def splits(A, a, s, e):
    cuts = {s, e}
    for c in (A["birth"][a] + 365, A["birth"][a] + 730, A["fc"][a]):
        if c is not None and s < c < e:
            cuts.add(c)
    cuts = sorted(cuts)
    return list(zip(cuts[:-1], cuts[1:]))


def ammonia(A, IV, region_of, season_of=None):
    """kg NH3 by region: each animal-day in the region of the herd holding it, at the housed rate inside that
    region's housing season and the grass rate outside it (season_of overrides whose season applies)"""
    g = defaultdict(float)
    for a, iv in IV.items():
        home = region_of(iv[0][0])
        for h, s, e in iv:
            r = region_of(h)
            sr = season_of(r, home) if season_of else r
            for s2, e2 in splits(A, a, s, e):
                c = category(A, a, s2)
                hd = CUMH[sr][e2] - CUMH[sr][s2]
                g[r] += hd * RATE[c][0] + (e2 - s2 - hd) * RATE[c][1]
    return g


def stock_on(A, IV, day, region_of):
    """cattle by (region, category) on a day"""
    st = defaultdict(int)
    for a, iv in IV.items():
        for h, s, e in iv:
            if s <= day < e:
                st[(region_of(h), category(A, a, day))] += 1
                break
    return st


def days_by(A, IV, region_of):
    dy = defaultdict(float)
    for a, iv in IV.items():
        for h, s, e in iv:
            for s2, e2 in splits(A, a, s, e):
                dy[(region_of(h), category(A, a, s2))] += e2 - s2
    return dy
