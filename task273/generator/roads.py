"""The Stonereach Valley's road network as the state's linear referencing system holds it (routes, mileposts,
functional class, urban or rural, the city whose police patrol it) and the Department's continuous count stations."""
import numpy as np

import common as K
import world as W

# routes: (route id, [(begin milepost, end milepost, functional class, urban or rural, city)])
STATE_ROUTES = [
    ("I-47", [(0.0, 21.0, 1, "R", ""), (21.0, 43.0, 1, "U", ""), (43.0, 96.0, 1, "R", "")]),
    ("I-247", [(0.0, 14.0, 1, "U", "")]),
    ("SR-9", [(0.0, 11.5, 2, "U", "")]),
    ("SR-512", [(0.0, 15.0, 2, "R", ""), (15.0, 24.0, 2, "U", ""), (24.0, 40.0, 2, "R", "")]),
    ("SR-14", [(0.0, 20.0, 3, "R", ""), (20.0, 31.0, 3, "U", K.CITY_A), (31.0, 58.0, 3, "R", "")]),
    ("SR-26", [(0.0, 9.0, 3, "U", K.CITY_A), (9.0, 44.0, 3, "R", "")]),
    ("SR-31", [(0.0, 12.0, 3, "R", ""), (12.0, 22.0, 3, "U", K.CITY_B), (22.0, 50.0, 3, "R", "")]),
    ("SR-58", [(0.0, 61.0, 4, "R", "")]),
    ("SR-62", [(0.0, 38.0, 4, "R", ""), (38.0, 44.5, 4, "U", K.CITY_B)]),
    ("SR-71", [(0.0, 72.0, 4, "R", "")]),
    ("SR-88", [(0.0, 54.0, 3, "R", ""), (54.0, 91.0, 4, "R", "")]),
    ("SR-103", [(0.0, 47.0, 4, "R", ""), (47.0, 55.0, 4, "U", K.CITY_A)]),
]
# local networks: (route prefix, city or "" for the county, functional class, urban or rural, number of routes,
# miles a route (low, high), segment miles (low, high), AADT (low, high))
LOCAL = [
    ("KW", K.CITY_A, 3, "U", 14, (3.0, 7.5), (0.25, 0.9), (16000, 38000)),
    ("FH", K.CITY_B, 3, "U", 6, (2.5, 6.0), (0.25, 0.9), (14000, 30000)),
    ("KW", K.CITY_A, 4, "U", 38, (2.0, 6.5), (0.2, 0.8), (7000, 19000)),
    ("FH", K.CITY_B, 4, "U", 16, (2.0, 5.5), (0.2, 0.8), (6000, 16000)),
    ("CR", "", 4, "U", 12, (2.0, 5.0), (0.3, 1.0), (6000, 15000)),
    ("KW", K.CITY_A, 5, "U", 70, (1.5, 5.0), (0.2, 0.7), (2500, 8000)),
    ("FH", K.CITY_B, 5, "U", 30, (1.5, 4.5), (0.2, 0.7), (2000, 7000)),
    ("CR", "", 5, "U", 26, (1.5, 4.0), (0.3, 0.9), (1800, 6000)),
    ("KW", K.CITY_A, 7, "U", 420, (1.0, 4.0), (0.3, 1.2), (400, 1800)),
    ("FH", K.CITY_B, 7, "U", 170, (1.0, 3.5), (0.3, 1.2), (350, 1600)),
    ("CR", "", 7, "U", 110, (1.0, 3.0), (0.4, 1.2), (300, 1400)),
    ("CR", "", 5, "R", 70, (6.0, 16.0), (0.8, 3.5), (1200, 4200)),
    ("CR", "", 6, "R", 120, (5.0, 14.0), (0.8, 3.5), (350, 1200)),
    ("CR", "", 7, "R", 380, (3.0, 12.0), (1.0, 4.0), (60, 450)),
]
ROUTE_NUM_START = {("KW", 3): 101, ("FH", 3): 101, ("KW", 4): 201, ("FH", 4): 201, ("KW", 5): 501, ("FH", 5): 501,
                   ("KW", 7): 1001, ("FH", 7): 1001, ("CR", 4): 401, ("CR", 5): 501, ("CR", 6): 601,
                   ("CR", 7): 1001}


def agency_of(route, fc, ur, city):
    if route.startswith("I-") or route in ("SR-9", "SR-512"):
        return "SP6"
    if route.startswith("SR-"):
        if city == K.CITY_A:
            return "KPD"
        if city == K.CITY_B:
            return "FPD"
        return "SP6"
    if route.startswith("KW-"):
        return "KPD"
    if route.startswith("FH-"):
        return "FPD"
    return "SCSO"


def network(seed=K.SEED):
    """Segments with AADT (2025) scaled so each class's miles match the region's 2025 total for it."""
    rng = np.random.default_rng(seed * 1000 + 11)
    segs = []

    def cut(route, b, e, fc, ur, city, lo, hi, aadt_lo, aadt_hi, base=None):
        x = b
        level = base if base is not None else rng.uniform(aadt_lo, aadt_hi)
        while x < e - 1e-9:
            ln = rng.uniform(lo, hi)
            y = min(e, round(x + ln, 3))
            if e - y < lo * 0.5:
                y = e
            level = level * float(np.exp(rng.normal(0, 0.06)))
            segs.append(dict(route=route, b=round(x, 3), e=round(y, 3), fc=fc, ur=ur, city=city, aadt=level))
            x = y

    for route, pieces in STATE_ROUTES:
        for b, e, fc, ur, city in pieces:
            lo, hi = (0.4, 1.6) if ur == "U" else (1.0, 4.5)
            base = {1: 90000 if ur == "U" else 40000, 2: 60000 if ur == "U" else 20000,
                    3: 30000 if ur == "U" else 11000, 4: 15000 if ur == "U" else 6000}[fc]
            cut(route, b, e, fc, ur, city, lo, hi, 0, 0, base=base * float(np.exp(rng.normal(0, 0.15))))
    for pre, city, fc, ur, n, (ml, mh), (sl, sh), (al, ah) in LOCAL:
        start = ROUTE_NUM_START[(pre, fc)]
        used = [s["route"] for s in segs if s["route"].startswith(pre + "-")]
        num = start
        for _ in range(n):
            while "%s-%04d" % (pre, num) in used:
                num += 1
            rid = "%s-%04d" % (pre, num)
            used.append(rid)
            num += 1 + int(rng.integers(0, 3))
            ln = round(float(rng.uniform(ml, mh)), 2)
            cut(rid, 0.0, ln, fc, ur, city, sl, sh, al, ah)
    # scale each class to its 2025 miles
    for fu in W.VMT_SHARE:
        cls = [s for s in segs if (s["fc"], s["ur"]) == fu]
        tot = sum(s["aadt"] * (s["e"] - s["b"]) * 365.0 for s in cls)
        f = W.vmt(2025, fu) / tot
        for s in cls:
            s["aadt"] = max(20, int(round(s["aadt"] * f / 10.0)) * 10)
    for i, s in enumerate(segs):
        s["i"] = i
        s["group"] = K.GROUP_OF[(s["fc"], s["ur"])]
        s["agency"] = agency_of(s["route"], s["fc"], s["ur"], s["city"])
        s["vmt"] = s["aadt"] * (s["e"] - s["b"])
    return segs


def old_route_id(route):
    """How crash reports to 31 December 2022 wrote the route: interstates as the number and I, state routes as the
    bare number, county roads with C and the number padded to four, city streets with the city's two letters."""
    pre, num = route.split("-")
    if pre == "I":
        return "%03dI" % int(num)
    if pre == "SR":
        return "%03d" % int(num)
    if pre == "CR":
        return "C%04d" % int(num)
    return "%s%d" % (pre, int(num))


# the Department's continuous count stations in the region: four in each factor group
def stations(segs, seed=K.SEED):
    rng = np.random.default_rng(seed * 1000 + 13)
    out = []
    n = 0
    for g in K.GROUPS:
        cand = [s for s in segs if s["group"] == g and s["aadt"] >= {"UF": 50000, "UA": 9000, "UL": 1200,
                                                                     "RF": 12000, "RA": 3000, "RL": 250}[g]]
        cand.sort(key=lambda s: (s["route"], s["b"]))
        pick = rng.choice(len(cand), size=4, replace=False)
        for j in sorted(pick):
            s = cand[j]
            n += 1
            mp = round(float(rng.uniform(s["b"] + 0.05 * (s["e"] - s["b"]), s["e"] - 0.05 * (s["e"] - s["b"]))), 2)
            out.append(dict(id="%02d%04d" % (61, 100 + n * 7), seg=s["i"], route=s["route"], mp=mp, fc=s["fc"],
                            ur=s["ur"], group=g, aadt=s["aadt"]))
    return out
