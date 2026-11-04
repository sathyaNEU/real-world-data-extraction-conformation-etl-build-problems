"""The coal yard as the ground and the piles really are: the pad on reclaimed harbour land with its bowls under the
long-standing pile areas, each pile at each survey, the true volumes, and the two contractors' renderings of the
surface (contractor A on the plant grid in N60, contractor B on ETRS-TM35FIN in N2000)."""
import math

import numpy as np

import world as W

TAN = math.tan(math.radians(W.ANGLE))
CT, ST = math.cos(math.radians(W.THETA_DEG)), math.sin(math.radians(W.THETA_DEG))


def pile(name):
    return next(p for p in W.PILES if p[0] == name)


def pad_n60(x, y):
    """The pad surface (N60) at local plant-grid coordinates, bowls included; fixed features of the yard too."""
    z = (W.PAD + 0.0025 * (x - 200.0) / 10.0 - 0.0018 * (y - 115.0) / 10.0
         + 0.025 * np.sin(x / 37.0) * np.cos(y / 23.0) + 0.011 * np.sin(x / 11.3 + 1.1) * np.sin(y / 8.7))
    for (_, cx, cy, L, Wd, H, d, _) in W.PILES:
        if d <= 0:
            continue
        r2 = ((x - cx) / (L / 2 + W.SKIRT)) ** 2 + ((y - cy) / (Wd / 2 + W.SKIRT)) ** 2
        z = z - d * np.clip(1.0 - r2, 0.0, None) ** 1.8
    # the drainage ditch along the south fence and the conveyor gallery's footing strip on the yard's centre line
    z = z - 0.55 * np.clip(1.0 - y / 4.0, 0.0, None)
    z = z + np.where(np.abs(y - 115.0) < 2.5, 0.35, 0.0)
    return z


def pile_n60(x, y, name, m):
    """The absolute surface (N60) of pile area `name` at survey m, or -inf where the pile is not."""
    _, cx, cy, L, Wd, _, _, _ = pile(name)
    phi = W.FILL[name][m]
    if phi <= 0:
        return np.full(np.shape(x), -np.inf)
    H = W.HEIGHT[name][m]
    run = H / TAN
    foot = phi * L
    x0 = cx - L / 2
    xc0, xc1 = x0 + run, x0 + foot - run
    top = W.PAD + H
    if xc1 < xc0:
        xc0 = xc1 = x0 + foot / 2
        top = W.PAD + min(H, foot / 2 * TAN)
    yc0, yc1 = cy - Wd / 2 + run, cy + Wd / 2 - run
    dx = np.maximum(0.0, np.maximum(xc0 - x, x - xc1))
    dy = np.maximum(0.0, np.maximum(yc0 - y, y - yc1))
    s = top - TAN * np.hypot(dx, dy)
    inside = (np.abs(x - cx) < L / 2 + W.AREA_PAD) & (np.abs(y - cy) < Wd / 2 + W.AREA_PAD)
    return np.where(inside, s, -np.inf)


def surface_n60(x, y, m):
    z = pad_n60(x, y)
    for p in W.PILES:
        z = np.maximum(z, pile_n60(x, y, p[0], m))
    return z


def area_mask(x, y, name):
    _, cx, cy, L, Wd, *_ = pile(name)
    return (np.abs(x - cx) < L / 2 + W.AREA_PAD) & (np.abs(y - cy) < Wd / 2 + W.AREA_PAD)


def true_volume(name, m, step=0.5):
    """Volume of coal above the pad in pile area `name` at survey m, on a fine lattice (m3)."""
    _, cx, cy, L, Wd, *_ = pile(name)
    xs = np.arange(cx - L / 2 - W.AREA_PAD + step / 2, cx + L / 2 + W.AREA_PAD, step)
    ys = np.arange(cy - Wd / 2 - W.AREA_PAD + step / 2, cy + Wd / 2 + W.AREA_PAD, step)
    X, Y = np.meshgrid(xs, ys)
    th = np.clip(pile_n60(X, Y, name, m) - pad_n60(X, Y), 0.0, None)
    return float(th.sum() * step * step)


def to_tm35(x, y):
    """Local plant-grid coordinates to ETRS-TM35FIN."""
    return W.E0 + CT * x - ST * y, W.N0 + ST * x + CT * y


def to_local(E, N):
    dE, dN = E - W.E0, N - W.N0
    return CT * dE + ST * dN, -ST * dE + CT * dN


# ------------------------------------------------------------------------------------------------------ machines
def machines(m):
    """Where the stacker and the two reclaimers stood on their rails during survey m (local x, y, half sizes)."""
    rng = np.random.default_rng(W.SEED + 700 + m)
    return [(float(rng.uniform(20, 380)), 115.0, 6.0, 8.0),       # stacker on the centre rail
            (float(rng.uniform(15, 385)), 24.5, 5.0, 6.0),        # reclaimer RC-1, south rail
            (float(rng.uniform(15, 385)), 205.5, 5.0, 6.0)]       # reclaimer RC-2, north rail


def machine_mask(x, y, m):
    out = np.zeros(np.shape(x), bool)
    for (mx, my, hx, hy) in machines(m):
        out |= (np.abs(x - mx) < hx) & (np.abs(y - my) < hy)
    return out


# ------------------------------------------------------------------------------------------------------ renderings
def grid_a():
    """Contractor A's cell centres, local coordinates (rows south to north)."""
    nx, ny = int(W.YARD_W / W.A_CELL), int(W.YARD_H / W.A_CELL)
    x = (np.arange(nx) + 0.5) * W.A_CELL
    y = (np.arange(ny) + 0.5) * W.A_CELL
    return np.meshgrid(x, y)


def render_a(m):
    """Contractor A's surface for survey m: N60 heights on the plant grid, NODATA where a machine stood."""
    X, Y = grid_a()
    rng = np.random.default_rng(W.SEED + 1000 + m)
    z = surface_n60(X, Y, m) + rng.normal(0.0, W.A_NOISE, X.shape)
    z = np.round(z, 3)
    z[machine_mask(X, Y, m)] = np.nan
    return X, Y, z


def lattice_b():
    """Contractor B's lattice points inside the yard: ETRS-TM35FIN coordinates and their local coordinates."""
    cx, cy = np.array([0, W.YARD_W, W.YARD_W, 0]), np.array([0, 0, W.YARD_H, W.YARD_H])
    E, N = to_tm35(cx, cy)
    e0 = math.floor(E.min() / W.B_STEP) * W.B_STEP + W.B_STEP / 2
    n0 = math.floor(N.min() / W.B_STEP) * W.B_STEP + W.B_STEP / 2
    es = np.arange(e0, E.max(), W.B_STEP)
    ns = np.arange(n0, N.max(), W.B_STEP)
    EE, NN = np.meshgrid(es, ns)
    x, y = to_local(EE, NN)
    keep = (x >= 0.3) & (x <= W.YARD_W - 0.3) & (y >= 0.3) & (y <= W.YARD_H - 0.3)
    return EE[keep], NN[keep], x[keep], y[keep]


def render_b(m):
    """Contractor B's surface for survey m: N2000 heights at its lattice points, machines removed."""
    E, N, x, y = lattice_b()
    rng = np.random.default_rng(W.SEED + 2000 + m)
    z = surface_n60(x, y, m) + W.DH + rng.normal(0.0, W.B_NOISE, x.shape)
    keep = ~machine_mask(x, y, m)
    return E[keep], N[keep], np.round(z[keep], 3)
