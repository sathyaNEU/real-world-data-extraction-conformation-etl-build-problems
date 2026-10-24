"""The physical world of task279: each monitoring point's peat column tracked as one-centimetre parcels from the
start of its drainage to the 2024 re-coring. Oxidation removes organic matter (and its carbon) above the summer
water table and leaves the ash; a parcel shrinks when it first drains; after a water-level cut the soft peat below the
new water table consolidates over three years; a slow secondary compression runs below the water table every year.
The 1997 and 2024 cores are cut from the parcel stacks at those dates, so a core's slices are the parcels that sat
in its depth interval at the time."""
import numpy as np

import common as K

# role -> parameter ranges; every unit carries one role (ROLE_OF below). y0 drainage began, w1 summer water-table
# depth below the surface (cm) before any cut, w2 after the cut in year yd, cons and cdep the consolidation the cut
# sets off below the new water table (share at the water table and its e-folding depth), k0 and lam the oxidation rate
# at the surface (per year) and its e-folding depth, ash the pristine peat's ash share, bd0 its dry bulk density
# (g/cm3), thick its pristine thickness above the sand (cm), sdry the share of a parcel's thickness left when it first
# drains, landuse the unit's use.
ROLES = {
    "G": dict(y0=(1926, 1938), w1=(68, 74), k0=(0.045, 0.049), lam=(29, 32), ash=(0.11, 0.13), bd0=(0.115, 0.125),
              sdry=(0.86, 0.90), thick=(460, 520), landuse="maize and grass in rotation"),
    "B1": dict(y0=(1940, 1950), w1=(60, 64), k0=(0.041, 0.044), lam=(27, 29), ash=(0.15, 0.17), sdry=(0.86, 0.90),
               thick=(450, 510), landuse="grassland, dairy"),
    "B2": dict(y0=(1944, 1954), w1=(58, 62), k0=(0.040, 0.043), lam=(27, 29), ash=(0.17, 0.19), sdry=(0.86, 0.90),
               thick=(450, 510), landuse="grassland, dairy"),
    "D": dict(y0=(1928, 1938), w1=(50, 54), w2=(70, 74), yd=(2011, 2011), cons=(0.12, 0.14), cdep=(320, 360),
              k0=(0.031, 0.034), ash=(0.19, 0.21), thick=(640, 700), bd0=(0.105, 0.115),
              landuse="grassland, dairy and young stock"),
    "A": dict(y0=(1950, 1958), w1=(34, 38), w2=(64, 68), yd=(2012, 2012), cons=(0.11, 0.13), cdep=(220, 260),
              k0=(0.026, 0.029), ash=(0.17, 0.19), thick=(560, 600), bd0=(0.115, 0.125), sdry=(0.72, 0.76),
              landuse="grassland, dairy"),
    "F3": dict(y0=(1955, 1963), w1=(36, 40), w2=(58, 62), yd=(2009, 2009), cons=(0.10, 0.12), cdep=(230, 270),
               k0=(0.027, 0.030), ash=(0.16, 0.18), thick=(560, 600), sdry=(0.74, 0.78), landuse="grassland, dairy"),
    "C": dict(y0=(1910, 1920), w1=(56, 60), k0=(0.046, 0.050), ash=(0.45, 0.50), bd0=(0.170, 0.180),
              landuse="grassland, dairy"),
    "F2": dict(y0=(1920, 1930), w1=(54, 58), k0=(0.045, 0.049), ash=(0.42, 0.47), bd0=(0.160, 0.170),
               landuse="grassland, dairy"),
    "F6": dict(y0=(1905, 1915), w1=(54, 58), k0=(0.045, 0.049), ash=(0.43, 0.48), bd0=(0.160, 0.170),
               landuse="grassland, sheep and young stock"),
    "F0": dict(y0=(1930, 1940), w1=(43, 47), k0=(0.028, 0.032), ash=(0.22, 0.26), landuse="grassland, dairy"),
    "F1": dict(y0=(1945, 1955), w1=(38, 42), k0=(0.026, 0.030), ash=(0.18, 0.22), lam=(21, 23),
               landuse="grassland, dairy"),
    "F4": dict(y0=(1900, 1910), w1=(46, 50), k0=(0.027, 0.031), ash=(0.26, 0.30), lam=(25, 27),
               landuse="grassland, dairy"),
}
ROLE_OF = {"PG-104": "F0", "PG-107": "A", "PG-111": "D", "PG-115": "C", "PG-118": "B1", "PG-122": "F2",
           "PG-126": "G", "PG-129": "F3", "PG-133": "F1", "PG-137": "B2", "PG-140": "F6", "PG-144": "F4"}
BASE = dict(thick=480, bd0=0.13, ash=0.25, y0=1950, w1=50, w2=None, yd=None, sdry=0.82, cons=0.0, cdep=80,
            sec=0.0001, k0=0.05, lam=25, beta=1.25, anaer=0.0004)
LAB_NOISE = dict(bd=0.022, loi=0.35, c=0.25)       # CV of bulk density; LOI and C in percentage points


def smooth(rng, n, scale):
    x = rng.normal(0, 1, n)
    k = np.exp(-0.5 * (np.arange(-3 * scale, 3 * scale + 1) / scale) ** 2)
    k /= k.sum()
    y = np.convolve(x, k, mode="same")
    return y / (y.std() + 1e-12)


def draw_unit(role, rng):
    p = dict(BASE)
    for k, v in ROLES[role].items():
        if isinstance(v, tuple):
            x = rng.uniform(*v)
            p[k] = int(round(x)) if k in ("y0", "yd", "thick", "w1", "w2") else float(x)
        else:
            p[k] = v
    p["role"] = role
    return p


def strat(rng, p, n):
    """The unit's stratigraphy shared by its points: ash share and pristine bulk density by depth."""
    ash = np.clip(p["ash"] * (1 + 0.18 * smooth(rng, n, 22)), 0.02, 0.7)
    bd = p["bd0"] * (1 + 0.10 * smooth(rng, n, 18))
    return ash, bd


def simulate(p, ash, bd, rng, snaps=(K.T97, K.T24)):
    """One point's column. Returns {year: (h, mo, ma, cm)} parcel arrays at each snapshot year (start of the year's
    growing season) and the column thickness for every year from 1990 on."""
    n = len(ash)
    m = bd * 10.0                       # kg/m2 in a one-centimetre parcel
    ma = m * ash
    mo = m - ma
    cm = mo * (0.50 + 0.012 * smooth(rng, n, 25))
    h = np.ones(n)
    drained = np.zeros(n, bool)
    out, thick = {}, {}
    pending = []                         # consolidation still to come: (year, share of the step)
    for yr in range(p["y0"], K.T24 + 1):
        if yr in snaps:
            out[yr] = (h.copy(), mo.copy(), ma.copy(), cm.copy())
        if yr >= 1990:
            thick[yr] = h.sum()
        W = p["w2"] if (p.get("yd") and yr >= p["yd"]) else p["w1"]
        top = np.cumsum(h) - h
        mid = top + h / 2
        newly = (~drained) & (mid < W)
        h[newly] *= p["sdry"]
        drained |= newly
        if p.get("yd") and yr == p["yd"]:
            pending = [(yr, 0.5), (yr + 1, 0.3), (yr + 2, 0.2)]
        for (y, share) in pending:
            if y == yr:
                below = mid >= p["w2"]
                f = share * p["cons"] * np.exp(-(mid - p["w2"]) / p["cdep"])
                h[below] *= (1 - f[below])
        below = mid >= W
        h[below] *= (1 - p["sec"])
        rate = p["k0"] * np.exp(-mid / p["lam"]) * (mid < W) + p["anaer"] * (mid >= W)
        lost = mo * (1 - np.exp(-rate))
        frac_c = cm / np.maximum(mo, 1e-12)
        closs = lost * frac_c * 0.96
        before = mo + ma
        mo = mo - lost
        cm = cm - closs
        h *= ((mo + ma) / before) ** p["beta"]
    return out, thick


def slices(snap, edges):
    """True mass, ash and carbon (kg/m2) in each depth interval of a core cut from the parcel stack."""
    h, mo, ma, cm = snap
    bot = np.cumsum(h)
    top = bot - h
    rows = []
    for a, b in zip(edges[:-1], edges[1:]):
        ov = np.clip(np.minimum(bot, b) - np.maximum(top, a), 0, None) / h
        rows.append(((mo * ov).sum() + (ma * ov).sum(), (ma * ov).sum(), (cm * ov).sum()))
    return np.array(rows)


def measure(sl, thick_cm, rng):
    """The laboratory's numbers for each slice: dry bulk density (g/cm3), loss on ignition and total carbon (per cent
    of dry mass), each with its own analytical error."""
    mass = sl[:, 0] * (1 + rng.normal(0, LAB_NOISE["bd"], len(sl)))
    bd = mass / (thick_cm * 10.0)
    loi = 100 * (1 - sl[:, 1] / sl[:, 0]) + rng.normal(0, LAB_NOISE["loi"], len(sl))
    c = 100 * sl[:, 2] / sl[:, 0] + rng.normal(0, LAB_NOISE["c"], len(sl))
    return bd, np.clip(loi, 1, 99.5), np.clip(c, 0.2, 60)


class World:
    def __init__(self, seed):
        self.seed = seed
        rng = np.random.default_rng(seed)
        self.units = {}
        for code in K.UNIT_CODES:
            p = draw_unit(ROLE_OF[code], rng)
            n = int(p["thick"] * 1.08) + 5
            ash, bd = strat(rng, p, n)
            pts = []
            for j in range(K.POINTS_PER_UNIT):
                q = dict(p)
                q["k0"] = p["k0"] * rng.uniform(0.95, 1.05)
                q["thick"] = int(p["thick"] * rng.uniform(0.96, 1.04))
                nn = q["thick"]
                a2 = np.clip(ash[:nn] * (1 + 0.06 * smooth(rng, nn, 12)), 0.02, 0.75)
                b2 = bd[:nn] * (1 + 0.05 * smooth(rng, nn, 10))
                snaps, thick = simulate(q, a2, b2, rng)
                e97 = np.arange(0, K.CORE97_DEPTH + 1, K.SLICE97)
                e24 = np.arange(0, K.CORE24_DEPTH + 1, K.SLICE24)
                s97, s24 = slices(snaps[K.T97], e97), slices(snaps[K.T24], e24)
                m97, m24 = measure(s97, K.SLICE97, rng), measure(s24, K.SLICE24, rng)
                h97, mo97, ma97, cm97 = snaps[K.T97]
                bot = np.cumsum(h97)
                ov = np.clip(np.minimum(bot, K.CORE97_DEPTH) - np.maximum(bot - h97, 0), 0, None) / h97
                truth = (ov * (cm97 - snaps[K.T24][3])).sum()     # kg C/m2 lost from the 1997 top metre's peat
                pts.append(dict(params=q, s97=s97, s24=s24, m97=m97, m24=m24, thick=thick, truth=truth,
                                lowering=thick[K.T97] - thick[K.T24]))
            self.units[code] = dict(params=p, points=pts)


# ------------------------------------------------------------------------------------------- the routes, in memory
def _cum(values):
    return np.concatenate([[0.0], np.cumsum(values)])


def depth_at(edges, per_slice, target):
    c = _cum(per_slice)
    if target > c[-1] + 1e-12:
        return None
    i = int(np.clip(np.searchsorted(c, target) - 1, 0, len(per_slice) - 1))
    return edges[i] + (target - c[i]) / (c[i + 1] - c[i]) * (edges[i + 1] - edges[i])


def amount_to(edges, per_slice, z):
    c = _cum(per_slice)
    i = int(np.clip(np.searchsorted(edges, z) - 1, 0, len(per_slice) - 1))
    return c[i] + (z - edges[i]) / (edges[i + 1] - edges[i]) * (c[i + 1] - c[i])


def point_routes(pt, years=27.0):
    """Every route on one point from its measured slices; kg C/m2 turned into t C/ha/yr."""
    e97 = np.arange(0, K.CORE97_DEPTH + 1, K.SLICE97)
    e24 = np.arange(0, K.CORE24_DEPTH + 1, K.SLICE24)
    bd97, loi97, c97 = pt["m97"]
    bd24, loi24, c24 = pt["m24"]
    mass97, mass24 = bd97 * K.SLICE97 * 10, bd24 * K.SLICE24 * 10
    ash97, ash24 = mass97 * (1 - loi97 / 100), mass24 * (1 - loi24 / 100)
    car97, car24 = mass97 * c97 / 100, mass24 * c24 / 100
    C97, M97, A97 = car97.sum(), mass97.sum(), ash97.sum()
    S = pt["lowering"]
    r = {}
    k = 10.0 / years
    r["ash"] = (C97 - amount_to(e24, car24, depth_at(e24, ash24, A97))) * k
    zm = depth_at(e24, mass24, M97)
    r["mass"] = (C97 - amount_to(e24, car24, zm)) * k if zm is not None else np.nan
    r["level"] = (C97 - amount_to(e24, car24, K.CORE97_DEPTH - S)) * k
    r["fixed"] = (C97 - amount_to(e24, car24, K.CORE97_DEPTH)) * k
    top = slice(0, 6)
    r["subsidence"] = S * (mass97[top].sum() / 30.0) * (car97[top].sum() / mass97[top].sum()) * k
    r["truth"] = pt["truth"] * k
    r["lowering"] = S
    return r


def unit_routes(world):
    out = {}
    for code, u in world.units.items():
        rs = [point_routes(pt) for pt in u["points"]]
        out[code] = {key: float(np.mean([r[key] for r in rs])) for key in rs[0]}
    return out


def ladder(world, ur=None):
    ur = ur or unit_routes(world)
    res = {}
    for key in ("ash", "subsidence", "level", "mass", "fixed", "truth"):
        order = sorted(ur, key=lambda c: -ur[c][key])
        v = [ur[c][key] for c in order]
        res[key] = dict(order=order, top3=order[:3], line=v[2] / v[3] if v[3] > 0 else 99.0,
                        first=v[0] / v[1] if v[1] > 0 else 99.0)
    return res, ur
