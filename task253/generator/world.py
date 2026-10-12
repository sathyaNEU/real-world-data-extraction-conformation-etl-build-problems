"""The named world on top of core.py: school codes, localities and names, the secondary colleges, the five
hubs, the August 2026 census by year level, the hub-to-school road distances and the facilities service
directory's servicing hubs. The 2027 visit plan is laid in asks.py, once the schools' figures are known."""
import numpy as np

import core
import names as NM

REGION_NAME = {"MN": "Metropolitan North", "MS": "Metropolitan South", "NO": "Northern", "WE": "Western",
               "SO": "Southern", "CO": "Coastal"}
BASES = {"MN": 23, "MS": 22, "NO": 17, "WE": 15, "SO": 17, "CO": 14}
VARIANTS = ["{}", "North {}", "{} West", "East {}", "{} South", "Upper {}", "{} Heights", "West {}", "{} Park",
            "South {}", "{} East", "Lower {}"]
N_SECONDARY = {"MN": 16, "MS": 14, "NO": 8, "WE": 6, "SO": 8, "CO": 6}
HUB_REGION = {"A": "MN", "B": "MS", "C": "NO", "D": "SO", "E": "CO"}
HUB_ANCHOR = {"A": (34.0, 52.0), "B": (48.0, -25.0), "C": (115.0, 195.0), "D": (140.0, -45.0),
              "E": (25.0, 440.0)}


def _kmeans(xy, k, rng):
    # farthest-point initialisation, then Lloyd iterations
    c = [xy[int(rng.integers(len(xy)))]]
    for _ in range(k - 1):
        d = np.min([((xy - q) ** 2).sum(1) for q in c], axis=0)
        c.append(xy[int(np.argmax(d))])
    c = np.array(c)
    for _ in range(30):
        lab = np.argmin(((xy[:, None, :] - c[None]) ** 2).sum(2), axis=1)
        for j in range(k):
            if (lab == j).any():
                c[j] = xy[lab == j].mean(0)
    return lab


def build(seed, shift):
    w = core.draw(seed, shift)
    rng = np.random.default_rng([seed, 11])
    S = w["S"]
    region = w["region"]
    # localities: k clusters per region, a base name per cluster, suburb variants inside a cluster
    pool = list(NM.LOCALITIES)
    order = rng.permutation(len(pool))
    pool = [pool[i] for i in order]
    loc = np.empty(S, dtype=object)
    region_bases = {}
    for r in core.REGIONS:
        idx = np.where(region == r)[0]
        k = BASES[r]
        bases = [pool.pop() for _ in range(k)]
        region_bases[r] = bases
        lab = _kmeans(w["xy"][idx], k, rng)
        for j in range(k):
            members = idx[lab == j]
            members = members[np.argsort(-w["n5"][members], kind="stable")]
            vi = 0
            for m in members:
                if vi > 0 and rng.random() < 0.15:
                    loc[m] = loc[members[0]]          # a second school in the same suburb or town
                    continue
                loc[m] = VARIANTS[vi % len(VARIANTS)].format(bases[j])
                vi += 1
    # school names: a title not repeated inside a locality
    title = np.empty(S, dtype=object)
    for L in sorted(set(loc)):
        idx = np.where(loc == L)[0]
        picks = rng.choice(len(NM.SAINTS), size=len(idx), replace=False)
        for m, p in zip(idx, picks):
            title[m] = NM.SAINTS[p]
    # secondary colleges in the larger localities of each region
    sec = []
    for r in core.REGIONS:
        idx = np.where(region == r)[0]
        idx = idx[np.argsort(-w["n5"][idx], kind="stable")][: N_SECONDARY[r]]
        for m in idx:
            t = NM.SAINTS[int(rng.integers(len(NM.SAINTS)))]
            kind = ["College", "Catholic College", "Regional College"][int(rng.integers(3))] if r not in core.METRO \
                else ["College", "Catholic College"][int(rng.integers(2))]
            nm = (t.replace("'s", "").replace("'", "") if t.endswith(("'s", "'")) and rng.random() < 0.5 else t)
            sec.append({"region": r, "locality": loc[m], "name": "%s %s" % (nm, kind),
                        "xy": w["xy"][m] + rng.normal(0, 2, 2)})
    # school codes: four characters, about a third with a leading zero
    allc = rng.choice(np.arange(150, 2900), size=S + len(sec), replace=False)
    codes = ["%04d" % c for c in allc]
    # hubs at the town nearest each anchor
    hubs = {}
    for h, r in HUB_REGION.items():
        idx = np.where(region == r)[0]
        d = ((w["xy"][idx] - np.array(HUB_ANCHOR[h])) ** 2).sum(1)
        m = idx[int(np.argmin(d))]
        hubs[h] = {"code": h, "locality": loc[m], "region": r, "xy": w["xy"][m] + rng.normal(0, 1.5, 2)}
    # one-way road distances, hub to school (km)
    road = np.zeros((S, 5))
    detour = rng.uniform(1.18, 1.38, (S, 5))
    for k, h in enumerate("ABCDE"):
        e = np.sqrt(((w["xy"] - hubs[h]["xy"]) ** 2).sum(1))
        road[:, k] = np.maximum(3, np.round(e * detour[:, k] + 2))
    # August 2026 census, Foundation to Year 6, primaries
    levels = ["F", "1", "2", "3", "4", "5", "6"]
    census = np.zeros((S, 7), int)
    n5c = np.maximum(4, w["enrol"][:, 2] + rng.integers(-2, 3, S))
    gc = np.where(w["metro"], w["g"] + 0.012, w["g"])       # the census's younger cohorts, by level
    for li in range(7):
        if li == 5:
            census[:, li] = n5c
        else:
            census[:, li] = np.maximum(2, np.round(n5c * gc ** (5 - li) * np.exp(rng.normal(0, 0.05, S))))
    # facilities service directory (February 2026): nearest of hubs A to D; six pilot schools at E
    dir_hub = np.array(["ABCD"[i] for i in np.argmin(road[:, :4], axis=1)], dtype=object)
    co = np.where(region == "CO")[0]
    pilots = co[np.argsort(road[co, 4], kind="stable")][:6]
    dir_hub[pilots] = "E"
    return {"w": w, "loc": loc, "title": title, "codes": codes[:S], "sec": sec, "sec_codes": codes[S:],
            "hubs": hubs, "road": road, "census": census, "levels": levels, "dir_hub": dir_hub,
            "pilots": pilots, "region_bases": region_bases}
