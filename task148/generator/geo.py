"""Geography of the north-east of Tavish County, in local kilometres (x east, y north) from the township's south-west
corner, and the conversion to WGS84. Halvorsen Township is a main part with the City of Tamsen cut out of it and a
detached part across Halvorsen Reservoir; the Wexley County line runs north and south at x = 9.6."""
from __future__ import annotations

import math

LAT0, LON0 = 39.8413, -88.1236
KM_LAT = 111.0
KM_LON = 111.32 * math.cos(math.radians(LAT0))

MAIN = [(0.0, 0.0), (3.1, 0.0), (3.1, -0.4), (6.3, -0.4), (6.3, 0.0), (9.6, 0.0), (9.6, 7.2), (8.1, 7.9),
        (6.4, 8.6), (4.9, 9.3), (3.2, 9.0), (1.6, 9.4), (0.0, 9.4)]
HOLE = [(4.0, 2.6), (6.5, 2.6), (6.5, 3.4), (7.0, 3.4), (7.0, 4.8), (5.6, 4.8), (5.6, 5.3), (4.0, 5.3)]
DETACHED = [(6.9, 10.4), (9.6, 10.4), (9.6, 12.6), (7.4, 12.9), (6.6, 11.6)]
RESERVOIR = [(3.2, 9.0), (4.9, 9.3), (6.4, 8.6), (8.1, 7.9), (9.6, 7.2), (9.6, 10.4), (6.9, 10.4), (6.6, 11.6),
             (5.1, 10.9), (3.6, 10.0)]
BOX = (-7.0, -4.5, 13.0, 13.5)          # x0, y0, x1, y1: the CHE extract's area
COUNTY_LINE_X = 9.6

# the cell sectors that route to the agency in the box: (id, x, y, radius m)
SECTORS = [
    ("TC31-1", -4.1, 2.0, 4800), ("TC31-2", -3.6, 7.6, 5200), ("TC32-1", -1.3, 11.6, 4000),
    ("TC33-1", 1.5, 4.6, 3100), ("TC33-2", 2.2, 8.0, 2600), ("TC34-1", 3.0, -2.3, 3600),
    ("TC35-1", 5.3, 3.8, 2200), ("TC35-2", 7.8, 1.2, 2900), ("TC36-1", 8.4, 6.0, 2400),
    ("TC37-1", 7.9, 11.6, 2000), ("TC37-2", 5.0, 12.4, 3500), ("TC38-1", 8.9, -3.0, 3800),
    ("TC38-2", 11.3, 3.5, 4400), ("TC38-3", 10.9, 9.1, 4000),
]


def to_latlon(x, y):
    return LAT0 + y / KM_LAT, LON0 + x / KM_LON


def to_xy(lat, lon):
    return (lon - LON0) * KM_LON, (lat - LAT0) * KM_LAT


def _inside(x, y, ring):
    """Even-odd ray cast on one ring."""
    inside = False
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xc = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xc > x:
                inside = not inside
    return inside


def _seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = 0.0 if L == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L))
    qx, qy = ax + t * dx, ay + t * dy
    return math.hypot(px - qx, py - qy)


def ring_dist(x, y, ring):
    return min(_seg_dist(x, y, *ring[i], *ring[(i + 1) % len(ring)]) for i in range(len(ring)))


def edge_dist_km(x, y):
    """Distance to the nearest edge of the township's three rings (the main part, the hole, the detached part)."""
    return min(ring_dist(x, y, MAIN), ring_dist(x, y, HOLE), ring_dist(x, y, DETACHED))


def in_township(x, y):
    return (_inside(x, y, MAIN) and not _inside(x, y, HOLE)) or _inside(x, y, DETACHED)


def area_of(x, y):
    """'main', 'detached', 'tamsen', 'reservoir', 'wexley' or 'tavish' for a point in the box."""
    if _inside(x, y, DETACHED):
        return "detached"
    if _inside(x, y, MAIN):
        return "tamsen" if _inside(x, y, HOLE) else "main"
    if _inside(x, y, RESERVOIR):
        return "reservoir"
    if x > COUNTY_LINE_X:
        return "wexley"
    return "tavish"


def ring_lonlat(ring, close=True):
    pts = [[round(LON0 + x / KM_LON, 6), round(LAT0 + y / KM_LAT, 6)] for x, y in ring]
    if close:
        pts.append(pts[0])
    return pts


def signed_area(ring):
    return 0.5 * sum(ring[i][0] * ring[(i + 1) % len(ring)][1] - ring[(i + 1) % len(ring)][0] * ring[i][1]
                     for i in range(len(ring)))
