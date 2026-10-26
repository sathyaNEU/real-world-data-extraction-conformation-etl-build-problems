"""The county's ground in Pennsylvania South state plane feet: the water authority's four pressure zones as
polygons (the Valley zone a band along the creek from the south-west of the county to the north-east), the seven
townships as the areas their homes stand in, and the placement of homes in subdivisions."""
import math

import numpy as np
from matplotlib.path import Path

X0, X1 = 2058000.0, 2184000.0          # the authority's service area, ftUS
Y0, Y1 = 196000.0, 286000.0
STEP = 600.0


def centre(x):
    """the creek's line: rising from the south-west to the north-east, with a meander"""
    u = (x - X0)
    return 214500.0 + u * (51000.0 / 126000.0) + 2600.0 * math.sin(2 * math.pi * u / 44000.0)


def half_width(x):
    u = (x - X0)
    return 2700.0 + 850.0 * math.sin(2 * math.pi * u / 31000.0 + 1.1)


def ridge_edge(x):
    """the Ridge zone's limit, high on the north-west slope"""
    u = (x - X0)
    return centre(x) + half_width(x) + 21000.0 + 2500.0 * math.sin(2 * math.pi * u / 52000.0 + 0.4)


def south_edge(x):
    """the Southside zone's limit, low on the south-east slope"""
    u = (x - X0)
    return centre(x) - half_width(x) - 19500.0 - 2200.0 * math.sin(2 * math.pi * u / 47000.0 + 2.0)


def _xs():
    n = int(round((X1 - X0) / STEP))
    return [X0 + i * STEP for i in range(n + 1)]


def _clip(y):
    return min(max(y, Y0), Y1)


def zone_polygons():
    """zone id -> list of rings, each a closed list of (x, y) vertices; the Upper zone is the two slopes above the
    valley, both fed from the Kilns Road booster, so it has two parts; adjacent zones share boundary vertices"""
    xs = _xs()
    top = [(x, Y1) for x in xs]
    rg = [(x, _clip(ridge_edge(x))) for x in xs]
    vt = [(x, _clip(centre(x) + half_width(x))) for x in xs]
    vb = [(x, _clip(centre(x) - half_width(x))) for x in xs]
    se = [(x, _clip(south_edge(x))) for x in xs]
    bot = [(x, Y0) for x in xs]

    def band(lower, upper):
        ring = list(lower) + list(reversed(upper))
        ring.append(ring[0])
        return [(round(a, 1), round(b, 1)) for a, b in ring]
    return {"PZ-1": [band(rg, top)], "PZ-2": [band(vt, rg), band(se, vb)], "PZ-3": [band(vb, vt)],
            "PZ-4": [band(bot, se)]}


class Zoner:
    def __init__(self, polys=None):
        self.polys = polys or zone_polygons()
        self.paths = [(k, Path(np.array(ring))) for k, rings in self.polys.items() for ring in rings]

    def zone(self, x, y):
        hits = [k for k, p in self.paths if p.contains_point((x, y))]
        return hits[0] if len(hits) == 1 else None

    def margin(self, x, y):
        """vertical distance from a point to the nearest zone boundary on its x, ft (homes are kept off the lines)"""
        ys = [ridge_edge(x), centre(x) + half_width(x), centre(x) - half_width(x), south_edge(x)]
        return min(abs(y - b) for b in ys)


# the townships: the box their homes stand in (x0, x1, y0, y1), ftUS
REGIONS = {"WYV": (2139000, 2166000, 247000, 270000), "HLT": (2118000, 2142000, 229000, 252000),
           "VRN": (2142000, 2164000, 220000, 246000), "MRV": (2164000, 2182000, 240000, 266000),
           "DOR": (2062000, 2094000, 224000, 256000), "BRK": (2060000, 2094000, 205000, 224000),
           "SAL": (2094000, 2118000, 213000, 241000)}


def town_centroid(t):
    x0, x1, y0, y1 = REGIONS[t]
    return ((x0 + x1) / 2.0, (y0 + y1) / 2.0)


def place(rng, zoner, town, n, valley_share, other_zones=None, mean_cluster=90):
    """n homes in subdivisions inside the township's box, valley_share of them in the Valley zone; the rest in the
    other zones the box reaches (or those named). Each subdivision is a cluster of homes around a centre."""
    x0, x1, y0, y1 = REGIONS[town]
    want = {"V": int(round(n * valley_share))}
    want["O"] = n - want["V"]
    pts = {"V": [], "O": []}
    guard = 0
    while (len(pts["V"]) < want["V"] or len(pts["O"]) < want["O"]) and guard < 200000:
        guard += 1
        cx, cy = rng.uniform(x0, x1), rng.uniform(y0, y1)
        z0 = zoner.zone(cx, cy)
        if z0 is None:
            continue
        cls = "V" if z0 == "PZ-3" else "O"
        if cls == "O" and other_zones and z0 not in other_zones:
            continue
        if len(pts[cls]) >= want[cls]:
            continue
        size = max(8, int(rng.poisson(mean_cluster)))
        sd = rng.uniform(350, 900)
        for _ in range(size * 3):
            if len(pts[cls]) >= want[cls] or size <= 0:
                break
            x, y = cx + rng.normal(0, sd), cy + rng.normal(0, sd * 0.7)
            if not (x0 <= x <= x1 and y0 <= y <= y1):
                continue
            z = zoner.zone(x, y)
            if z is None or zoner.margin(x, y) < 40:
                continue
            if ("V" if z == "PZ-3" else "O") != cls or (cls == "O" and other_zones and z not in other_zones):
                continue
            pts[cls].append((round(x, 1), round(y, 1), z))
            size -= 1
    allp = pts["V"] + pts["O"]
    order = rng.permutation(len(allp))
    return [allp[i] for i in order]
