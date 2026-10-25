"""The world behind the pack: ten years of daily weather at the fourteen farms and four candidates, each farm's inverter
blocks and their output, the broiler litter dust that settles on the blocks nearest Wexcombe's sheds (and would on Hallam
Down's), the fleet's outages and the environs listing."""
import numpy as np
import pandas as pd

import params as P


class World:
    pass


def _layout(nm, dc):
    """inverter blocks around the centroid: the 2012 to 2014 farms on 500 kW central inverters (blocks of about 0.55 MWp
    on a 62 m by 55 m grid), later farms on blocks of about 1.1 MWp on a 95 m by 85 m grid; Hallam Down's planned blocks
    wrap the farmyard to its south-west"""
    if nm == "Hallam Down":
        cells = [(c, r) for r in range(3) for c in range(4) if (c, r) not in ((0, 2), (1, 2))]
        return [((c - 1.5) * 95.0, (1 - r) * 85.0) for c, r in cells]
    old = nm in ("Ashcombe", "Bramble Hill", "Wexcombe", "Coldharbour")
    bmw, dx, dy = (0.547, 62.0, 55.0) if old else (1.1, 95.0, 85.0)
    k = max(4, int(round(dc / bmw)))
    asp = {"Wexcombe": 5.0}.get(nm, 1.8 if old else 1.3)
    cols = int(np.ceil(np.sqrt(k * asp)))
    rows_ = int(np.ceil(k / cols))
    out = []
    for j in range(k):
        r, c = divmod(j, cols)
        out.append(((c - (cols - 1) / 2) * dx, ((rows_ - 1) / 2 - r) * dy))
    return out


def soil(rain, dep):
    """the deposit a block carries each day: it builds by the day's deposit when less than LO mm falls, is cut to
    WASH_LO of itself by LO to HI mm and to WASH_HI by HI mm or more, and never passes CAP"""
    s = 0.0
    out = np.zeros(len(rain))
    for i, r in enumerate(rain):
        if r >= P.HI:
            s *= P.WASH_HI
        elif r >= P.LO:
            s *= P.WASH_LO
        else:
            s = min(s + dep[i], P.CAP)
        out[i] = s
    return out


def world():
    rng = np.random.default_rng(P.SEED_WORLD)
    W = World()
    days = pd.date_range(P.W0, P.W1, freq="D")
    W.days = days
    n = len(days)
    doy = days.dayofyear.values
    z = np.zeros(n)
    e = rng.normal(size=n)
    for i in range(1, n):
        z[i] = 0.62 * z[i - 1] + np.sqrt(1 - 0.62 ** 2) * e[i]
    season = 0.28 * np.sin(2 * np.pi * (doy - 100) / 365.25)
    sun = np.clip(rng.normal(1, 0.30, n) - 0.22 * z, 0.22, 1.7)
    clear = 2.9 + 2.3 * np.sin(2 * np.pi * (doy - 80) / 365.25)
    t_reg = 10.6 + 6.4 * np.sin(2 * np.pi * (doy - 112) / 365.25) + rng.normal(0, 2.0, n)
    wind = np.where(rng.uniform(size=n) < 0.58, rng.normal(232, 38, n), rng.uniform(0, 360, n)) % 360
    W.wind = wind
    W.site = {}
    for nm, dc, comm, mod, pf, ws, amt, td, E0, N0 in P.SITES + P.CAND:
        loc = z + 0.55 * rng.normal(size=n)
        wet = loc > (0.15 + season + ws)
        a = rng.gamma(0.85, 4.6, n) * amt * np.exp(0.35 * np.clip(loc, 0, None))
        rain = np.where(wet, np.round(a, 1), 0.0)
        poa = np.clip(clear * sun * pf * rng.lognormal(0, 0.04, n), 0.05, None)
        bias = float(rng.lognormal(0, 0.008))
        if nm in P.BIFACIAL:
            bias = 1.0 + (bias - 1.0) * 0.15      # the provider's tiles over the bifacial farms were validated on site
        sat = poa * bias * rng.lognormal(0, 0.06, n)
        temp = t_reg + td + rng.normal(0, 0.5, n)
        W.site[nm] = dict(dc=dc, comm=comm, mod=mod, E0=E0, N0=N0, rain=rain, poa=poa, poa_sat=sat, sat_bias=bias,
                          temp=temp, blocks=[])
        for (x, y) in _layout(nm, dc):
            dep = np.full(n, P.BG)
            d_src = None
            if nm in P.SOURCES:
                dist, brg, sheds = P.SOURCES[nm]
                sx, sy = dist * np.sin(np.radians(brg)), dist * np.cos(np.radians(brg))
                d_src = float(np.hypot(sx - x, sy - y))
                b_src = float(np.degrees(np.arctan2(sx - x, sy - y)) % 360)
                r0 = P.R0 * sheds / 10.0 * np.exp(-(d_src - P.D0) / P.DL)
                towards = np.abs(((wind - b_src) + 180) % 360 - 180) <= P.PLUME_HALF_ANGLE
                dep = np.where(towards, r0, P.OFF_PLUME * r0) + P.BG
            W.site[nm]["blocks"].append(dict(x=x, y=y, soil=soil(rain, dep), d_src=d_src))
    # the fleet's output from 2022, block by block, and its outages
    k0 = int(np.where(days == pd.Timestamp(P.F0))[0][0])
    W.k0 = k0
    W.events = []
    for nm, dc, comm, mod, pf, ws, amt, td, E0, N0 in P.SITES:
        S = W.site[nm]
        ks = max(k0, int(days.searchsorted(pd.Timestamp(comm))))     # the meter's first day
        S["k_start"] = ks
        pr0, tc, deg = P.MOD[mod]
        age = (days - pd.Timestamp(comm)).days.values / 365.25
        cell = S["temp"] + 3.2 * S["poa"]
        pr = pr0 * P.BOS[nm] * (1 + tc * (cell - 25)) * (1 - deg) ** np.clip(age, 0, None)
        pr = pr * (1 - 0.035 * np.exp(-S["poa"] / 0.9))
        nb = len(S["blocks"])
        site_av = np.ones(n)
        n_site = 2 if nm == "Knowle Park" else int(rng.integers(4, 10))
        for k in rng.choice(np.arange(ks, n), size=n_site, replace=False):
            f = round(float(rng.uniform(0.0, 0.75)), 2)
            site_av[k] = f
            W.events.append((days[k].date(), nm, "", str(rng.choice(["Grid outage (DNO)", "Transformer fault",
                                                                     "Planned maintenance"])), f))
        tot = np.zeros(n)
        for b, B in enumerate(S["blocks"]):
            av = site_av.copy()
            # the newest farm, still in its defects period, has had fewer inverter faults
            for k in rng.choice(np.arange(ks, n), size=int(rng.integers(0, 3 if nm == "Knowle Park" else 5)), replace=False):
                f = round(float(rng.uniform(0.0, 0.8)), 2)
                av[k] = min(av[k], f)
                W.events.append((days[k].date(), nm, "INV%02d" % (b + 1),
                                 str(rng.choice(["Inverter trip", "String fuse failures", "IGBT fault",
                                                 "AC breaker trip"])), f))
            eb = S["poa"] * (dc / nb) * pr * (1 - B["soil"]) * av * rng.lognormal(0, 0.010, n) * float(rng.lognormal(0, 0.006))
            B["energy"] = eb
            tot += eb
        S["export"] = tot * P.EXPORT_LOSS * rng.lognormal(0, 0.003, n)
        S["pr_model"] = pr
    return W


FEAT = [("Arable field", ["winter wheat", "oilseed rape", "spring barley", "maize", "potatoes", "sugar beet"], 40, 1900),
        ("Pasture", ["permanent grass", "sheep grazing", "horse paddocks"], 40, 1900),
        ("Hedgerow", ["mixed native", "hawthorn", "laid hedge"], 5, 400),
        ("Woodland", ["mixed broadleaf", "conifer plantation", "ancient woodland"], 120, 1900),
        ("Dwelling", ["detached house", "farmhouse", "pair of cottages", "bungalow"], 110, 1900),
        ("Settlement", ["hamlet", "village"], 500, 1950),
        ("Road", ["A-road", "B-road", "minor road", "unclassified lane"], 25, 1900),
        ("Track", ["farm track, surfaced", "farm track, unsurfaced", "bridleway"], 10, 900),
        ("Watercourse", ["stream", "drainage ditch", "river"], 30, 1500), ("Pond", ["field pond", "balancing pond"], 40, 1200),
        ("Overhead line", ["11 kV", "33 kV", "132 kV"], 20, 1900),
        ("Substation", ["33/11 kV primary", "pole-mounted transformer", "132/33 kV grid"], 150, 1950),
        ("Church", ["parish church (listed)"], 400, 1950),
        ("Listed building", ["grade II farmhouse", "grade II barn", "grade II* manor"], 250, 1950),
        ("Public right of way", ["footpath", "bridleway", "byway"], 0, 600),
        ("Farm buildings", ["general purpose shed", "machinery store", "Dutch barn"], 100, 1500),
        ("Livestock unit", ["beef cattle", "dairy, 180 cows", "pig finishing", "calf rearing"], 250, 1950),
        ("Poultry unit", ["free-range layers, 2 sheds", "free-range layers, 4 sheds", "turkey, 3 sheds", "broiler, 6 sheds"], 600, 1950),
        ("Grain store", ["on-farm store with drier", "co-operative store"], 200, 1800),
        ("Equestrian", ["livery yard", "riding school"], 400, 1900),
        ("Caravan site", ["touring park", "static caravans"], 600, 1950), ("Golf course", ["18-hole course"], 800, 1950),
        ("Telecom mast", ["lattice mast", "monopole"], 200, 1800),
        ("Wind turbine", ["single 500 kW turbine", "single 50 kW turbine"], 500, 1950),
        ("Reservoir", ["irrigation reservoir"], 300, 1900), ("Sewage works", ["small treatment works"], 700, 1950),
        ("Recreation ground", ["playing field", "cricket ground"], 600, 1950),
        ("Business unit", ["agricultural contractor yard", "small industrial unit"], 400, 1950),
        ("Railway", ["branch line", "main line"], 300, 1950), ("Scheduled monument", ["barrow", "moated site"], 300, 1950)]

# features placed by the survey where they stand: the two broiler units close upwind of blocks, broiler units downwind or
# far off, and the dusty workings close upwind of farms whose blocks show nothing
EXTRA = {"Wexcombe": [("Poultry unit", "broiler, 10 sheds", 545, 252)],
         "Hallam Down": [("Poultry unit", "broiler, 10 sheds", 105, 229)],
         "Elmstead": [("Poultry unit", "broiler, 8 sheds", 420, 48)],
         "Dunsford Lane": [("Poultry unit", "broiler, 8 sheds", 470, 75)],
         "Greystoke Barns": [("Poultry unit", "broiler, 6 sheds", 530, 352)],
         "Hartsfield": [("Poultry unit", "broiler, 8 sheds", 1450, 204), ("Business unit", "agricultural contractor yard", 380, 233)],
         "Furzedown": [("Poultry unit", "broiler, 12 sheds", 1320, 241)],
         "Larkhill Common": [("Poultry unit", "broiler, 12 sheds", 1890, 214)],
         "Brindle Moor": [("Poultry unit", "broiler, 6 sheds", 880, 118), ("Equestrian", "riding school", 410, 252)],
         "Marston Vale": [("Poultry unit", "broiler, 8 sheds", 1110, 87)],
         "Ashcombe": [("Track", "farm track, unsurfaced", 240, 214)],
         "Fairoak": [("Track", "farm track, unsurfaced", 310, 247)],
         "Jessop's Farm": [("Track", "farm track, unsurfaced", 190, 228)],
         "Coldharbour": [("Equestrian", "livery yard", 450, 238)],
         "Knowle Park": [("Business unit", "small industrial unit", 520, 221)],
         "Ivy Cross": [("Track", "farm track, unsurfaced", 270, 205)]}


def environs():
    rng = np.random.default_rng(P.SEED_ENV)
    env = []
    for nm in P.OPERATING + P.CANDIDATES:
        k = int(rng.integers(52, 68))
        for j in rng.choice(len(FEAT), size=k):
            t, descs, lo, hi = FEAT[j]
            if t == "Poultry unit" and rng.uniform() < 0.6:
                continue
            env.append((nm, t, descs[int(rng.integers(0, len(descs)))], int(rng.uniform(lo, hi) // 10 * 10),
                        int(rng.uniform(0, 360))))
    for nm in P.OPERATING + P.CANDIDATES:
        for t, d, dist, b in EXTRA.get(nm, []):
            env.append((nm, t, d, dist, b))
    e2 = pd.DataFrame(env, columns=["site", "feature", "description", "distance_m", "bearing_from_site_deg"])
    keep = set((nm, d, dist) for nm, lst in EXTRA.items() for t, d, dist, b in lst)
    placed = pd.Series([(a, b, c) in keep for a, b, c in zip(e2.site, e2.description, e2.distance_m)])
    # no other poultry or livestock unit lies within 700 m to the south and west of any site
    m = (e2.feature.isin(["Poultry unit", "Livestock unit"]) & (e2.distance_m < 700)
         & e2.bearing_from_site_deg.between(150, 310) & ~placed)
    e2.loc[m, "distance_m"] = e2.loc[m, "distance_m"] + 700
    # and at the two sites beside a broiler unit no other working that raises dust lies close upwind
    dusty = (e2.feature.isin(["Business unit", "Equestrian", "Livestock unit", "Sewage works", "Grain store", "Railway"])
             | e2.description.eq("farm track, unsurfaced"))
    m2 = (e2.site.isin(["Wexcombe", "Hallam Down"]) & dusty & (e2.distance_m < 900)
          & e2.bearing_from_site_deg.between(150, 310))
    e2.loc[m2, "distance_m"] = e2.loc[m2, "distance_m"] + 900
    order = {s: i for i, s in enumerate(P.OPERATING + P.CANDIDATES)}
    e2 = e2.sample(frac=1, random_state=7)
    e2["_o"] = e2.site.map(order)
    e2 = e2.sort_values(["_o", "distance_m"], kind="mergesort").drop(columns="_o").reset_index(drop=True)
    return e2
