"""Channel geometry: chainage and offset of OSGB points against the centreline in Notice to Mariners 3 of 2026.

Offsets are positive to the north of the centreline. Used by the world and, through its own copy of the arithmetic,
by verify.py.
"""
import numpy as np

import params as P

WP = np.array([[w[1], w[2]] for w in P.WAYPOINTS])
CH = np.array([w[0] for w in P.WAYPOINTS])


def chain_offset(E, N):
    """(s km, t m) of each point against the centreline: nearest segment, the projection clamped to the segment."""
    E = np.asarray(E, float)
    N = np.asarray(N, float)
    best_d = np.full(E.shape, np.inf)
    s_out = np.zeros(E.shape)
    t_out = np.zeros(E.shape)
    for i in range(len(WP) - 1):
        a, b = WP[i], WP[i + 1]
        d = b - a
        L = np.hypot(*d)
        ux, uy = d / L
        px, py = E - a[0], N - a[1]
        u = px * ux + py * uy
        uc = np.clip(u, 0.0, L)
        cx, cy = a[0] + uc * ux, a[1] + uc * uy
        dist = np.hypot(E - cx, N - cy)
        cross = ux * py - uy * px            # positive to the left of travel (west-going: south)
        better = dist < best_d - 1e-9
        best_d = np.where(better, dist, best_d)
        s_out = np.where(better, CH[i] + u / 1000.0, s_out)
        t_out = np.where(better, -cross, t_out)
    return s_out, t_out


def point_at(s_km, t_m):
    """OSGB point at chainage s (km) and offset t (m, north positive) on the segment holding s."""
    i = int(np.searchsorted(CH, s_km, side="right") - 1)
    i = min(max(i, 0), len(WP) - 2)
    a, b = WP[i], WP[i + 1]
    d = b - a
    L = np.hypot(*d)
    ux, uy = d / L
    u = (s_km - CH[i]) * 1000.0
    # offset t positive north = -(left normal); left normal of (ux, uy) is (-uy, ux)
    nx, ny = uy, -ux
    return a[0] + u * ux + t_m * nx, a[1] + u * uy + t_m * ny


def part_at(s):
    for code, name, c0, c1, half, nn, ns, k in P.PARTS:
        if c0 <= s < c1 or (code == "TB" and abs(s - c1) < 1e-9):
            return code
    return None


def half_width(code):
    for p in P.PARTS:
        if p[0] == code:
            return p[4]
    raise KeyError(code)
