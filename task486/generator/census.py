"""The county's census geography, its census-day residents and the formally private release of their counts.

Truth is drawn per block (housing units, group quarters residents, persons by sex and age group); the release adds
noise to every count at every level and post-processes each level, top down, into non-negative whole numbers that add
up to the level above: county, tract, block group, block. Housing units and group quarters facilities are exact."""
import numpy as np

import world as W

# ---------------------------------------------------------------- geography
# (tract code, kind, provider areas, number of block groups); kind is core, edge or rural.
TRACTS = [
    ("000100", "core", ("Wickmoor City",), 3), ("000200", "core", ("Wickmoor City",), 3),
    ("000300", "core", ("Wickmoor City",), 3), ("000400", "core", ("Wickmoor City",), 2),
    ("000500", "core", ("Wickmoor City",), 3), ("000600", "core", ("Wickmoor City",), 2),
    ("000700", "core", ("Wickmoor City",), 3), ("000800", "core", ("Wickmoor City",), 2),
    ("000901", "edge", ("Wickmoor City", "North Kelvane"), 3),
    ("000902", "edge", ("Wickmoor City", "North Kelvane"), 2),
    ("001000", "edge", ("Wickmoor City", "East Kelvane"), 3),
    ("001100", "edge", ("Wickmoor City", "South Kelvane"), 3),
    ("960100", "core", ("Fallowmere Town",), 3), ("960200", "core", ("Fallowmere Town",), 2),
    ("960300", "edge", ("Fallowmere Town", "West Kelvane"), 3),
    ("960400", "edge", ("Fallowmere Town", "South Kelvane"), 2),
    ("950100", "rural", ("North Kelvane",), 2), ("950200", "rural", ("North Kelvane",), 2),
    ("950300", "rural", ("East Kelvane",), 2), ("950400", "rural", ("East Kelvane",), 3),
    ("950500", "rural", ("South Kelvane",), 2), ("950600", "rural", ("South Kelvane",), 2),
    ("950700", "rural", ("West Kelvane",), 2), ("950800", "rural", ("West Kelvane",), 3),
    ("950900", "rural", ("West Kelvane",), 2),
]

# Base share of residents in each age group (both sexes), and the share of each group that is female.
BASE_AGE = np.array([5.6, 6.0, 6.3, 3.9, 2.6, 1.3, 1.3, 3.8, 6.4, 6.3, 6.1, 5.9, 6.0, 6.3, 6.6,
                     2.7, 3.9, 2.4, 3.4, 4.9, 3.4, 2.2, 2.6])
FEMALE = np.array([0.49, 0.49, 0.49, 0.49, 0.48, 0.48, 0.48, 0.49, 0.50, 0.50, 0.50, 0.50, 0.50, 0.51, 0.51,
                   0.52, 0.52, 0.53, 0.53, 0.54, 0.56, 0.59, 0.66])


def build(rng):
    """Blocks with their tract, block group, provider area (as drawn since July 2023), housing units, residents by cell
    and group quarters residents. Returns a dict of arrays and lists."""
    blocks = []
    for tract, kind, areas, nbg in TRACTS:
        older = {"core": rng.uniform(0.85, 1.10), "edge": rng.uniform(0.95, 1.25),
                 "rural": rng.uniform(1.15, 1.45)}[kind]
        age = BASE_AGE.copy()
        age[15:] *= older
        age[:15] *= (100 - age[15:].sum()) / age[:15].sum()
        per_hu = rng.uniform(2.15, 2.6) * 0.91           # persons per housing unit (occupancy folded in)
        for g in range(1, nbg + 1):
            bg_age = age.copy()                           # block groups within a tract differ in age
            bg_age[15:] *= rng.uniform(0.72, 1.38)
            bg_age[:15] *= (100 - bg_age[15:].sum()) / bg_age[:15].sum()
            nb = int(rng.integers(26, 58)) if kind != "rural" else int(rng.integers(40, 75))
            cut = kind == "edge" and not (nbg == 3 and g == 1)
            share_town = rng.uniform(0.45, 0.65)
            for b in range(nb):
                if kind == "core" or (kind == "edge" and (not cut or b < nb * share_town)):
                    side = "town"
                    area = areas[0]
                    hu = 0 if rng.random() < 0.07 else int(rng.integers(6, 46))
                else:
                    side = "rural"
                    area = areas[-1]
                    hu = 0 if rng.random() < 0.36 else int(rng.integers(1, 9))
                mu = hu * per_hu * bg_age / 100.0
                cells = np.zeros(W.NCELL, int)
                for a in range(23):
                    f = rng.poisson(mu[a] * FEMALE[a])
                    m = rng.poisson(mu[a] * (1 - FEMALE[a]))
                    cells[a], cells[23 + a] = m, f
                blocks.append(dict(tract=tract, bg=tract + str(g), block=str(g) + "%03d" % (b + 1), kind=kind,
                                   side=side, cut=cut, area=area, hu=hu, cells=cells, gq=None))
    return blocks


GQ_FACILITIES = [  # (name, type, tract, bg digit, residents)
    ("Linden Court Health and Rehabilitation", "Nursing facility", "000300", "2", 112),
    ("Wickmoor Lutheran Home", "Nursing facility", "000500", "1", 96),
    ("Briarwood Assisted Living", "Assisted living (group quarters)", "000700", "3", 64),
    ("Maple Terrace Nursing Center", "Nursing facility", "000200", "1", 78),
    ("Fallowmere Manor", "Nursing facility", "960100", "2", 88),
    ("Orchard View Senior Residence", "Assisted living (group quarters)", "960200", "1", 52),
]
GQ_AGE = {20: 0.2, 21: 0.3, 22: 0.4}   # residents 75+ mostly; a tenth 60 to 74
GQ_YOUNGER = {15: 0.15, 16: 0.2, 17: 0.2, 18: 0.2, 19: 0.25}


def add_group_quarters(blocks, rng):
    """Each facility sits in its own block of a core block group, a block with no housing units."""
    for name, typ, tract, g, n in GQ_FACILITIES:
        cand = [i for i, b in enumerate(blocks) if b["tract"] == tract and b["bg"] == tract + g and b["hu"] == 0
                and b["gq"] is None]
        if not cand:
            cand = [i for i, b in enumerate(blocks) if b["tract"] == tract and b["bg"] == tract + g]
        i = cand[int(rng.integers(0, len(cand)))]
        b = blocks[i]
        b["gq"] = (name, typ, n)
        younger = int(round(n * 0.1))
        older = n - younger
        ages = list(rng.choice(list(GQ_AGE), size=older, p=np.array(list(GQ_AGE.values())) / sum(GQ_AGE.values())))
        ages += list(rng.choice(list(GQ_YOUNGER), size=younger,
                                p=np.array(list(GQ_YOUNGER.values())) / sum(GQ_YOUNGER.values())))
        for a in ages:
            sex = 1 if rng.random() < 0.7 else 0
            b["cells"][sex * 23 + a] += 1
    return blocks


# ---------------------------------------------------------------- the release
def project(m, total):
    """Least-squares projection of noisy measurements m onto {x >= 0, sum x = total}, then whole numbers that keep the
    sum (largest remainders; ties by position)."""
    total = int(total)
    m = np.asarray(m, float)
    if len(m) == 1:
        return np.array([max(0, total)])
    lo, hi = m.min() - abs(total) - 2.0, m.max() + 2.0
    for _ in range(60):
        lam = (lo + hi) / 2
        if np.maximum(0, m - lam).sum() > total:
            lo = lam
        else:
            hi = lam
    x = np.maximum(0, m - hi)
    f = np.floor(x).astype(int)
    r = total - int(f.sum())
    if r > 0:
        f[np.argsort(-(x - f), kind="stable")[:r]] += 1
    elif r < 0:
        cand = np.where(f > 0)[0]
        f[cand[np.argsort((x - f)[cand], kind="stable")][:-r]] -= 1
    return f


def release(blocks, rng, sigma=None):
    """The published counts at every level: dict level -> {geo id: cells}."""
    sigma = sigma or W.SIGMA
    cells = np.array([b["cells"] for b in blocks])
    tr = [b["tract"] for b in blocks]
    bg = [b["bg"] for b in blocks]
    tracts = sorted(set(tr))
    bgs = sorted(set(bg))
    noise = lambda s, shape: np.rint(rng.normal(0, s, shape)).astype(int)
    county_true = cells.sum(0)
    county = np.maximum(0, county_true + noise(sigma["county"], W.NCELL))
    t_true = np.array([cells[[i for i, x in enumerate(tr) if x == t]].sum(0) for t in tracts])
    t_pub = np.zeros_like(t_true)
    t_noisy = t_true + noise(sigma["tract"], t_true.shape)
    for c in range(W.NCELL):
        t_pub[:, c] = project(t_noisy[:, c], county[c])
    g_pub = {}
    for k, t in enumerate(tracts):
        gl = [x for x in bgs if x[:6] == t]
        g_true = np.array([cells[[i for i, x in enumerate(bg) if x == g]].sum(0) for g in gl])
        g_noisy = g_true + noise(sigma["block_group"], g_true.shape)
        gp = np.zeros_like(g_true)
        for c in range(W.NCELL):
            gp[:, c] = project(g_noisy[:, c], t_pub[k, c])
        for j, g in enumerate(gl):
            g_pub[g] = gp[j]
    b_pub = np.zeros_like(cells)
    for g in bgs:
        # a block with no housing units and no group quarters facility is a structural zero: it stays empty
        idx = [i for i, x in enumerate(bg) if x == g and (blocks[i]["hu"] > 0 or blocks[i]["gq"] is not None)]
        b_noisy = cells[idx] + noise(sigma["block"], cells[idx].shape)
        for c in range(W.NCELL):
            b_pub[idx, c] = project(b_noisy[:, c], g_pub[g][c])
    return {"county": county, "tract": dict(zip(tracts, t_pub)), "block_group": g_pub, "block": b_pub}
