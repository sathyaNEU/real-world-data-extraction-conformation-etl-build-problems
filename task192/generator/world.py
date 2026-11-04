"""Kestrel Falls Municipal Utilities, electric division: the 12.47 kV distribution network, its feeders,
protective devices, transformers and service points, and the dates the records run over.

Distances are miles along the line; positions are kilometres east and north of the city centre."""
import datetime as dt
import math

import numpy as np

SEED = 19204
UTILITY = "Kestrel Falls Municipal Utilities"
DIVISION = "Electric Distribution"
VPH = 12470 / math.sqrt(3)

# record window (local Central time) and the reporting year
DATA0 = dt.date(2025, 1, 1)
DATA1 = dt.date(2026, 10, 31)
REP0 = dt.date(2026, 1, 1)
REP1 = dt.date(2026, 10, 31)
WIN0 = dt.date(2026, 8, 1)          # the weeks before the patrol decision
WIN1 = dt.date(2026, 10, 31)
BASE0 = dt.date(2025, 8, 1)
BASE1 = dt.date(2025, 10, 31)
DECIDED = dt.date(2026, 11, 4)
PATROL_WEEK = dt.date(2026, 11, 9)
REBUILD = dt.date(2026, 3, 14)      # Cotter Road substation rebuild energised, feeders renumbered
OMS_CUTOVER = dt.date(2026, 4, 1)   # outage management system replaced
CLEARANCE = (dt.date(2026, 3, 23), dt.date(2026, 4, 17))   # MLR-2 full-circuit line clearance

T_MED_2026 = 4.62                   # minutes of daily system SAIDI (2021 to 2025 daily values, 2.5 beta)

LAT0, LON0 = 37.803, -92.198
KM_PER_DEG_LAT = 111.0
KM_PER_DEG_LON = 111.0 * math.cos(math.radians(LAT0))

SUBS = {
    # id: name, x km, y km, source Z1 (ohm), Z0 (ohm)
    "BLV": ("Bluffview", 0.0, 0.0, complex(0.21, 1.18), complex(0.09, 0.91)),
    "CTR": ("Cotter Road", -7.6, 5.7, complex(0.34, 1.62), complex(0.15, 1.27)),
    "MLR": ("Millrace", 5.9, -1.3, complex(0.26, 1.37), complex(0.11, 1.04)),
    "NYD": ("North Yard", 1.6, 6.4, complex(0.23, 1.29), complex(0.10, 0.98)),
    "SYC": ("Sycamore", -2.3, -6.6, complex(0.29, 1.49), complex(0.13, 1.16)),
}
AIRPORT = ("Kestrel Falls Regional Airport", -3.9, 1.8)

# conductor impedance, ohm per mile: main line 336.4 ACSR, laterals 1/0 ACSR
Z1_MAIN, Z0_MAIN = complex(0.306, 0.627), complex(0.692, 1.948)
Z1_LAT, Z0_LAT = complex(0.888, 0.759), complex(1.276, 2.081)
SPAN_FT = 300.0

# feeder: id, legacy id (Cotter Road before the rebuild), substation, heading (deg, 0 east), main OH miles,
# lateral OH miles, UG miles, customers at the start of 2025, exposures (lightning, wind and tree, wet tree,
# animal by year), recloser positions on the main line (miles), lateral phase weights A, B, C, three-phase
FEEDERS = [
    dict(id="BLV-1", sub="BLV", head=205, main=3.0, lat=2.8, ug=1.9, cust=2638, light=0.8, tree=0.75, wet=0.45,
         animal=(0.85, 0.9), recl=[], ph=(0.32, 0.32, 0.26, 0.10)),
    dict(id="BLV-2", sub="BLV", head=332, main=1.6, lat=1.2, ug=3.4, cust=2011, light=0.6, tree=0.6, wet=0.4,
         animal=(1.55, 1.6), recl=[], ph=(0.34, 0.30, 0.30, 0.06)),
    dict(id="BLV-3", sub="BLV", head=262, main=2.2, lat=8.5, ug=0.6, cust=2379, light=0.9, tree=1.0, wet=0.5,
         animal=(1.0, 1.05), recl=[1.95], ph=(0.03, 0.93, 0.03, 0.01)),
    dict(id="CTR-1", legacy="CR-12", sub="CTR", head=148, main=9.5, lat=11.9, ug=0.2, cust=1482, light=1.7,
         tree=0.7, wet=0.5, animal=(0.55, 0.6), recl=[3.2, 6.8], ph=(0.33, 0.33, 0.30, 0.04)),
    dict(id="CTR-2", legacy="CR-13", sub="CTR", head=214, main=6.0, lat=8.1, ug=0.4, cust=1917, light=1.25,
         tree=1.0, wet=0.55, animal=(0.7, 0.75), recl=[3.5], ph=(0.09, 0.08, 0.79, 0.04)),
    dict(id="CTR-3", legacy="CR-14", sub="CTR", head=301, main=4.4, lat=6.2, ug=1.2, cust=2563, light=1.15,
         tree=0.8, wet=0.5, animal=(0.8, 0.85), recl=[3.1], ph=(0.31, 0.31, 0.31, 0.07)),
    dict(id="MLR-1", sub="MLR", head=18, main=3.4, lat=3.8, ug=1.4, cust=2707, light=0.9, tree=0.8, wet=0.5,
         animal=(0.8, 0.85), recl=[], ph=(0.30, 0.33, 0.30, 0.07)),
    dict(id="MLR-2", sub="MLR", head=312, main=4.6, lat=5.0, ug=0.5, cust=2629, light=0.95, tree=(2.8, 0.3),
         wet=(1.8, 0.16), animal=(0.75, 2.6), recl=[71 * SPAN_FT / 5280], ph=(0.47, 0.44, 0.04, 0.05)),
    dict(id="MLR-3", sub="MLR", head=95, main=2.4, lat=2.5, ug=2.2, cust=2893, light=0.8, tree=0.6, wet=0.4,
         animal=(0.75, 0.8), recl=[], ph=(0.33, 0.30, 0.31, 0.06)),
    dict(id="NYD-1", sub="NYD", head=60, main=2.2, lat=1.6, ug=1.0, cust=641, light=0.7, tree=0.4, wet=0.3,
         animal=(0.5, 0.55), recl=[], ph=(0.25, 0.25, 0.25, 0.25)),
    dict(id="NYD-2", sub="NYD", head=128, main=5.0, lat=6.3, ug=0.3, cust=2238, light=0.95, tree=1.45, wet=1.6,
         animal=(0.8, 0.85), recl=[3.8], ph=(0.14, 0.70, 0.12, 0.04)),
    dict(id="NYD-3", sub="NYD", head=12, main=4.2, lat=4.9, ug=0.6, cust=2947, light=0.9, tree=0.85, wet=0.5,
         animal=(1.0, 1.6), recl=[], ph=(0.33, 0.31, 0.30, 0.06)),
    dict(id="NYD-4", sub="NYD", head=78, main=1.8, lat=1.3, ug=4.6, cust=1562, light=0.6, tree=0.4, wet=0.3,
         animal=(0.5, 0.55), recl=[], ph=(0.33, 0.33, 0.30, 0.04)),
    dict(id="SYC-1", sub="SYC", head=238, main=8.1, lat=10.6, ug=0.3, cust=1608, light=1.2, tree=1.15, wet=0.7,
         animal=(0.85, 0.9), recl=[3.0, 6.2], ph=(0.83, 0.07, 0.07, 0.03)),
    dict(id="SYC-2", sub="SYC", head=172, main=3.9, lat=4.3, ug=1.1, cust=2771, light=0.9, tree=1.35, wet=2.6,
         animal=(0.8, 0.85), recl=[], ph=(0.31, 0.32, 0.31, 0.06)),
    dict(id="SYC-3", sub="SYC", head=292, main=5.6, lat=6.8, ug=0.8, cust=2331, light=1.0, tree=0.9, wet=0.55,
         animal=(0.8, 0.85), recl=[3.1], ph=(0.33, 0.33, 0.30, 0.04)),
]
FID = [f["id"] for f in FEEDERS]
FIX = {f: i for i, f in enumerate(FID)}

# the components breaking down: feeder, main-line pole, phase, arc resistance, first and last flashover dates,
# flashovers by month
INCIPIENT = [
    dict(feeder="MLR-2", pole=57, phase="C", rf=0.80, months={8: 2, 9: 4, 10: 5}, first=dt.date(2026, 8, 12)),
    dict(feeder="SYC-3", pole=86, phase="A", rf=1.10, months={9: 2, 10: 5}, first=dt.date(2026, 9, 21)),
]

# the seasons the desk knows each feeder by (August to October): designed counts, times and places drawn
EPISODES = [
    dict(feeder="NYD-3", cause="animal", year=2026, n=27, when="fair"),
    dict(feeder="NYD-3", cause="animal", year=2025, n=5, when="fair"),
    dict(feeder="NYD-2", cause="wet_tree", year=2026, n=17, when="damp"),
    dict(feeder="NYD-2", cause="wet_tree", year=2025, n=16, when="damp"),
    dict(feeder="BLV-3", cause="animal", year=2026, n=21, when="fair", phase="B"),
    dict(feeder="BLV-3", cause="animal", year=2025, n=18, when="fair", phase="B"),
]

# load transfers: laterals moved from one feeder to another by moving an open point (count of laterals)
TRANSFERS = [
    dict(src="CTR-2", dst="CTR-3", date=REBUILD, n=2),
    dict(src="SYC-2", dst="SYC-1", date=dt.date(2026, 5, 11), n=1),
    dict(src="BLV-1", dst="BLV-3", date=dt.date(2026, 6, 8), n=1),
]
NEW_SUBDIVISION = dict(feeder="NYD-4", n=318, start=dt.date(2025, 9, 15), end=dt.date(2026, 10, 9))

PICKUP = {"BREAKER": (720.0, 360.0), "RECLOSER": (480.0, 240.0)}   # phase, ground (A)
SHOTS = {"BREAKER": 3, "RECLOSER": 4}


def miles_to_pole(m):
    return max(1, int(round(m * 5280 / SPAN_FT)))


def pole_to_miles(p):
    return p * SPAN_FT / 5280


def year_value(v, year):
    return v if not isinstance(v, tuple) else v[0 if year == 2025 else 1]


def _rid(rng, used, lo, hi):
    while True:
        v = int(rng.integers(lo, hi))
        if v not in used:
            used.add(v)
            return v


def build(rng):
    """The network as it stands, with its history. Returns a dict of feeders, devices, laterals, transformers and
    service points. Every identifier is drawn, not counted."""
    used = set()
    net = dict(feeders={}, devices={}, laterals={}, transformers={}, sps={}, dev_hist=[])
    breaker_id = {}
    for f in FEEDERS:
        fid = f["id"]
        sub = SUBS[f["sub"]]
        n_poles = miles_to_pole(f["main"])
        # main line path: a gentle walk from the substation
        pts = [(sub[1], sub[2])]
        ang = math.radians(f["head"])
        step = 0.05
        heads = []
        for k in range(int(round(f["main"] / step))):
            if k % 10 == 0:
                ang += math.radians(float(rng.normal(0, 9)))
            heads.append(ang)
            x, y = pts[-1]
            pts.append((x + step * 1.609 * math.cos(ang), y + step * 1.609 * math.sin(ang)))
        n = f["id"].replace("-", "")
        bk = "%s-F%s-52" % (f["sub"], fid[-1])
        breaker_id[fid] = bk
        F = dict(id=fid, legacy=f.get("legacy"), sub=f["sub"], main=f["main"], lat_mi=f["lat"], ug=f["ug"],
                 path=pts, heads=heads, poles=n_poles, prefix=n, breaker=bk, reclosers=[], laterals=[],
                 fuse_saving=f.get("fuse_saving", True), spec=f)
        net["feeders"][fid] = F
        # devices: breaker, reclosers
        net["devices"][bk] = dict(id=bk, type="BREAKER", feeder=fid, pole="%s-P000" % n, pos=0.0, parent=None)
        prev = bk
        for r_mi in f["recl"]:
            rid = "R-%d" % _rid(rng, used, 2001, 3999)
            if fid == "MLR-2":
                rid = "R-2207"
            if fid == "SYC-3":
                rid = "R-3114"
            used.add(int(rid[2:]))
            pole = miles_to_pole(r_mi)
            phasing = list("ABC")
            rng.shuffle(phasing)
            net["devices"][rid] = dict(id=rid, type="RECLOSER", feeder=fid, pole="%s-P%03d" % (n, pole),
                                       pos=pole_to_miles(pole), parent=prev, terminals="".join(phasing),
                                       scada=False)
            F["reclosers"].append(rid)
            prev = rid
        # laterals: taps along the main line, lengths summing to the lateral miles
        n_lat = max(3, int(round(f["lat"] / 0.33)))
        w = rng.gamma(2.2, 1.0, n_lat)
        lens = w / w.sum() * f["lat"]
        taps = np.sort(rng.uniform(0.15, f["main"] - 0.05, n_lat))
        phw = np.array(f["ph"], dtype=float)
        for k in range(n_lat):
            tap_pole = miles_to_pole(float(taps[k]))
            ph = "ABCX"[int(rng.choice(4, p=phw / phw.sum()))]
            ph = "ABC" if ph == "X" else ph
            fuse = "F-%05d" % _rid(rng, used, 10000, 99999)
            zone = zone_device(net, fid, pole_to_miles(tap_pole))
            side = 1 if rng.random() < 0.5 else -1
            la = heads[min(len(heads) - 1, int(taps[k] / step))] + side * math.radians(float(rng.uniform(65, 115)))
            L = dict(id=fuse, feeder=fid, tap_pole=tap_pole, tap=pole_to_miles(tap_pole), length=float(lens[k]),
                     phase=ph, ang=la, size=None, parent=zone, moved=None, expo=float(rng.lognormal(0, 0.8)))
            net["laterals"][fuse] = L
            F["laterals"].append(fuse)
            net["devices"][fuse] = dict(id=fuse, type="FUSE", feeder=fid, pole="%s-P%03d" % (n, tap_pole),
                                        pos=L["tap"], parent=zone)
    # SCADA-connected reclosers
    for rid in ("R-3114",) + tuple(net["feeders"]["CTR-1"]["reclosers"]) + (net["feeders"]["SYC-1"]["reclosers"][0],):
        net["devices"][rid]["scada"] = True
    _place_customers(net, rng, used)
    _transfers(net, rng)
    return net


def zone_device(net, fid, pos):
    """The breaker or recloser whose zone holds a main-line position."""
    F = net["feeders"][fid]
    dev = F["breaker"]
    for rid in F["reclosers"]:
        if pos >= net["devices"][rid]["pos"]:
            dev = rid
    return dev


def _place_customers(net, rng, used):
    for f in FEEDERS:
        fid = f["id"]
        F = net["feeders"][fid]
        total = f["cust"]
        main_share = 0.24 if fid != "NYD-4" else 0.55
        lat_ids = F["laterals"]
        lens = np.array([net["laterals"][l]["length"] for l in lat_ids])
        n_main = int(round(total * main_share))
        n_lat = total - n_main
        alloc = rng.multinomial(n_lat, lens / lens.sum())
        groups = [("MAIN", None, n_main)] + [("LAT", l, int(c)) for l, c in zip(lat_ids, alloc)]
        for kind, lat, n in groups:
            left = n
            while left > 0:
                three = kind == "MAIN" and rng.random() < 0.12
                k = int(rng.integers(1, 4)) if three else int(rng.choice([3, 4, 5, 6, 7, 8, 9, 10, 11],
                                                                           p=[.06, .1, .14, .17, .17, .14, .1, .07, .05]))
                k = min(k, left)
                tid = "T%06d" % _rid(rng, used, 100000, 999999)
                if kind == "MAIN":
                    pos = float(rng.uniform(0.05, F["main"]))
                    ph = "ABC" if three else "ABC"[int(rng.integers(0, 3))]
                    dev = zone_device(net, fid, pole_to_miles(miles_to_pole(pos)))
                    T = dict(id=tid, feeder=fid, lateral=None, pos=pos, lpos=0.0, phase=ph, device=dev,
                             pole="%s-P%03d" % (F["prefix"], miles_to_pole(pos)),
                             kva=int(rng.choice([150, 300, 500])) if three else int(rng.choice([25, 50, 50, 75])))
                else:
                    L = net["laterals"][lat]
                    lpos = float(rng.uniform(0.02, max(0.03, L["length"])))
                    lph = L["phase"]
                    ph = lph if len(lph) == 1 else "ABC"[int(rng.integers(0, 3))]
                    T = dict(id=tid, feeder=fid, lateral=lat, pos=L["tap"], lpos=lpos, phase=ph, device=lat,
                             pole="L%s-%03d" % (lat[2:], int(lpos * 17.6) + 1),
                             kva=int(rng.choice([25, 25, 37, 50, 50])))
                T["lure"] = float(rng.lognormal(0, 0.9))
                net["transformers"][tid] = T
                for _ in range(k):
                    sp = "%08d" % _rid(rng, used, 10000000, 99999999)
                    cls = "GS" if three or rng.random() < 0.08 else "RES"
                    if three and rng.random() < 0.25:
                        cls = "LP"
                    yr = int(rng.integers(1962, 2025))
                    con = dt.date(yr, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
                    net["sps"][sp] = dict(id=sp, transformer=tid, cls=cls, connected=con, disconnected=None)
                left -= k
    # retirements and new services across the record
    sps = sorted(net["sps"])
    for sp in sps:
        if rng.random() < 0.0085:
            d0 = (DATA0 - dt.date(2024, 12, 31)).days
            span = (DATA1 - DATA0).days
            net["sps"][sp]["disconnected"] = DATA0 + dt.timedelta(days=int(rng.integers(0, span)) + 0 * d0)
    # scattered new services on every feeder, and the new subdivision on NYD-4
    trs = sorted(net["transformers"])
    for _ in range(260):
        tid = trs[int(rng.integers(0, len(trs)))]
        sp = "%08d" % _rid(rng, used, 10000000, 99999999)
        con = DATA0 + dt.timedelta(days=int(rng.integers(0, (DATA1 - DATA0).days)))
        net["sps"][sp] = dict(id=sp, transformer=tid, cls="RES" if rng.random() < 0.9 else "GS", connected=con,
                              disconnected=None)
    nd = NEW_SUBDIVISION
    F = net["feeders"][nd["feeder"]]
    lat = F["laterals"][-1]
    L = net["laterals"][lat]
    left = nd["n"]
    span = (nd["end"] - nd["start"]).days
    while left > 0:
        k = min(left, int(rng.choice([4, 5, 6, 7, 8])))
        tid = "T%06d" % _rid(rng, used, 100000, 999999)
        lpos = float(rng.uniform(0.02, L["length"]))
        net["transformers"][tid] = dict(id=tid, feeder=F["id"], lateral=lat, pos=L["tap"], lpos=lpos,
                                        phase=L["phase"] if len(L["phase"]) == 1 else "B", device=lat,
                                        pole="L%s-%03d" % (lat[2:], int(lpos * 17.6) + 1), kva=50,
                                        lure=float(rng.lognormal(0, 0.9)))
        con0 = nd["start"] + dt.timedelta(days=int(rng.integers(0, span)))
        for _ in range(k):
            sp = "%08d" % _rid(rng, used, 10000000, 99999999)
            con = min(nd["end"], con0 + dt.timedelta(days=int(rng.integers(0, 20))))
            net["sps"][sp] = dict(id=sp, transformer=tid, cls="RES", connected=con, disconnected=None)
        left -= k


def _transfers(net, rng):
    """Move laterals between feeders at their effective dates: the lateral fuse takes a new parent on the
    receiving feeder, and its transformers and service points follow."""
    for t in TRANSFERS:
        src = net["feeders"][t["src"]]
        dst = net["feeders"][t["dst"]]
        cands = sorted(src["laterals"], key=lambda l: -net["laterals"][l]["tap"])
        cands = [l for l in cands if net["laterals"][l]["phase"] != "ABC"][: t["n"]]
        for lat in cands:
            L = net["laterals"][lat]
            newparent = dst["reclosers"][-1] if dst["reclosers"] else dst["breaker"]
            L["moved"] = dict(date=t["date"], feeder=dst["id"], parent=newparent,
                              tap=dst["main"] + 0.35 + float(rng.uniform(0.0, 0.4)))


def device_parent(net, dev, day):
    """A device's parent on a local date (the register's history)."""
    if dev in net["laterals"]:
        L = net["laterals"][dev]
        if L["moved"] and day >= L["moved"]["date"]:
            return L["moved"]["parent"]
        return L["parent"]
    return net["devices"][dev]["parent"]


def device_feeder(net, dev, day):
    if dev in net["laterals"]:
        L = net["laterals"][dev]
        if L["moved"] and day >= L["moved"]["date"]:
            return L["moved"]["feeder"]
        return L["feeder"]
    return net["devices"][dev]["feeder"]


def chain(net, dev, day):
    out = []
    while dev:
        out.append(dev)
        dev = device_parent(net, dev, day)
    return out


def legacy_name(fid, day):
    spec = FEEDERS[FIX[fid]]
    if spec.get("legacy") and day < REBUILD:
        return spec["legacy"]
    return fid


def breaker_name(net, fid, day):
    """The breaker's register id on a date: the Cotter Road breakers were replaced at the rebuild."""
    spec = FEEDERS[FIX[fid]]
    if spec.get("legacy") and day < REBUILD:
        return spec["legacy"].replace("-", "") + "-BKR"
    return net["feeders"][fid]["breaker"]


def to_latlon(x, y):
    return LAT0 + y / KM_PER_DEG_LAT, LON0 + x / KM_PER_DEG_LON


def z_at(net, fid, pos, lat=None, lpos=0.0, day=None):
    """Positive and zero sequence impedance from the source to a point: a main-line position, or a point on a
    lateral (which may be fed from another feeder after a transfer)."""
    feeder = fid
    tap = pos
    if lat is not None:
        L = net["laterals"][lat]
        if L["moved"] and day is not None and day >= L["moved"]["date"]:
            feeder = L["moved"]["feeder"]
            tap = L["moved"]["tap"]
        else:
            tap = L["tap"]
    s = SUBS[net["feeders"][feeder]["sub"]]
    z1 = s[3] + Z1_MAIN * tap + (Z1_LAT * lpos if lat is not None else 0)
    z0 = s[4] + Z0_MAIN * tap + (Z0_LAT * lpos if lat is not None else 0)
    return z1, z0


def fault_current(z1, z0, phases, rf):
    """Fault current magnitude (A) on the faulted phases for a fault of resistance rf."""
    if len(phases) == 1:
        return 3 * VPH / abs(2 * z1 + z0 + 3 * rf)
    if len(phases) == 2:
        return math.sqrt(3) * VPH / abs(2 * z1 + rf)
    return VPH / abs(z1 + rf / 2)
