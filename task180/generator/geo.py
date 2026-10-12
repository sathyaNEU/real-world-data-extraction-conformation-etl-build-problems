"""Distances on the scale of a plant's monitoring zone: a local flat projection is accurate to metres here."""
import math

import numpy as np

KM_LAT = 110.574


def km_lon(lat):
    return 111.320 * math.cos(math.radians(lat))


def to_xy(lat, lon, lat0, lon0):
    return (np.asarray(lon) - lon0) * km_lon(lat0), (np.asarray(lat) - lat0) * KM_LAT


def to_latlon(x, y, lat0, lon0):
    return lat0 + np.asarray(y) / KM_LAT, lon0 + np.asarray(x) / km_lon(lat0)


def dist_to_segment(lat, lon, seg):
    """Epicentral distance (km) from points to the surface projection of a well section ((lat, lon, d), (lat, lon, d))."""
    (la1, lo1, _), (la2, lo2, _) = seg
    lat0, lon0 = (la1 + la2) / 2, (lo1 + lo2) / 2
    px, py = to_xy(lat, lon, lat0, lon0)
    ax, ay = to_xy(la1, lo1, lat0, lon0)
    bx, by = to_xy(la2, lo2, lat0, lon0)
    vx, vy = bx - ax, by - ay
    t = np.clip(((px - ax) * vx + (py - ay) * vy) / max(vx * vx + vy * vy, 1e-12), 0, 1)
    return np.hypot(px - (ax + t * vx), py - (ay + t * vy))


def dist_to_point(lat, lon, pt):
    lat0, lon0 = pt[0], pt[1]
    px, py = to_xy(lat, lon, lat0, lon0)
    return np.hypot(px, py)
