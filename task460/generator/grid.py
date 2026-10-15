"""Each balancing area's 2025, hour by hour on the UTC clock: demand from a business-hours load shape with weather,
seasons and weekends; nuclear, run-of-river hydro, wind and utility solar; a day-ahead interchange schedule; and a
merit-order dispatch of the fossil fleet with seasonal must-run, blocks of equal cost sharing the margin pro rata.
The plant register's annual figures and the agency's published rates are computed from the same dispatch."""
import datetime as dt

import numpy as np

import world as W

H = 8760
T0 = dt.datetime(2025, 1, 1)


def season_of_month(m):
    return {12: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3}[m]


def ar1(rng, n, phi, sd):
    e = rng.normal(0, sd, n)
    x = np.zeros(n)
    for i in range(1, n):
        x[i] = phi * x[i - 1] + e[i]
    return x


def lg(x):
    return 1.0 / (1.0 + np.exp(-x))


def solar_shape(lh, doy, lat, tilt=10.0):
    """Clear-sky AC shape (0 to about 1) for the local standard hour beginning lh (centre lh + 0.5)."""
    dec = 23.45 * np.sin(2 * np.pi * (284 + doy) / 365)
    eot = 0.165 * np.sin(4 * np.pi * (doy - 81) / 364) - 0.126 * np.cos(2 * np.pi * (doy - 81) / 364) \
        - 0.025 * np.sin(2 * np.pi * (doy - 81) / 364)
    half = np.degrees(np.arccos(np.clip(-np.tan(np.radians(lat)) * np.tan(np.radians(dec)), -1, 1))) / 15.0
    x = (lh + 0.5 - (12.0 - eot)) / half
    v = np.clip(np.cos(np.pi / 2 * np.clip(x, -1, 1)), 0, None) ** 1.3
    elev = 90 - lat + dec
    return v * (0.55 + 0.45 * np.sin(np.radians(np.clip(elev + tilt * 0.3, 5, 90))))


def clocks(utc):
    """For an area's UTC offset: local standard hour, day of year, month, weekday, season and local day index, for
    each UTC hour beginning."""
    lst = [T0 + dt.timedelta(hours=h + utc) for h in range(H)]
    lh = np.array([t.hour for t in lst])
    doy = np.array([t.timetuple().tm_yday for t in lst])
    mon = np.array([t.month for t in lst])
    dow = np.array([t.weekday() for t in lst])
    season = np.array([season_of_month(m) for m in mon])
    dayidx = np.array([(t.date() - dt.date(2024, 12, 31)).days for t in lst])
    return lh, doy, mon, dow, season, dayidx


def load_profile(L, lh, doy, dow, tday, busy, rng):
    summ = np.clip(np.cos(2 * np.pi * (doy - 205) / 365), 0, None)
    wint = np.clip(np.cos(2 * np.pi * (doy - 20) / 365), 0, None)
    h = lh + 0.5
    biz = lg((h - L.get("up", 7.0)) / 0.25) * lg((L.get("down", 19.0) - h) / 0.25)
    mid = np.exp(-((h - 13.0) / 2.6) ** 2)
    aft = np.exp(-((h - L.get("cool_c", 15.0)) / L.get("cool_w", 2.4)) ** 2)
    eve = np.exp(-((h - L.get("heat_c", 18.0)) / L.get("heat_w", 1.2)) ** 2)
    shape = L["night"] + (L["plateau"] - L["night"]) * (1 + 0.06 * busy) * biz
    shape = shape + summ * (L.get("cool", 0.0) + 0.025 * tday) * aft
    shape = shape + wint * (L.get("heat", 0.0) + 0.025 * tday) * eve
    shape = shape + L.get("seas_s", 0.03) * summ + L.get("seas_w", 0.03) * wint
    shape = shape - np.where(dow >= 5, 0.05, 0.0) * mid
    return L["peak"] * (shape + ar1(rng, H, 0.6, 0.004))


def dispatch(code, rng):
    a = W.AREAS[code]
    lh, doy, mon, dow, season, dayidx = clocks(a["utc"])
    nd = dayidx.max() + 2
    tday = ar1(rng, nd, 0.75, 1.0)[dayidx]
    busy = rng.normal(0, 1, nd)[dayidx]
    load = load_profile(a["load"], lh, doy, dow, tday, busy, rng)
    w = 0.33 + ar1(rng, H, 0.985, 0.010) + a.get("wind_diurnal", 0.05) * np.cos(2 * np.pi * (lh - 2) / 24) \
        + 0.06 * np.cos(2 * np.pi * (doy - 40) / 365)
    wind = a.get("wind", 0) * np.clip(w, 0.03, 0.9)
    cloud_d = np.clip(rng.normal(a.get("sky", 0.84), 0.14, nd), 0.25, 1.0)
    cloud = cloud_d[dayidx] * (1 + ar1(rng, H, 0.8, 0.03))
    usolar = a.get("solar", 0) * solar_shape(lh, doy, a["lat"]) * np.clip(cloud, 0.2, 1.05)
    nuc = a.get("nuc", 0) * 0.95 * (1 + ar1(rng, H, 0.97, 0.0012)) * (1 - 0.006 * np.clip(np.cos(2 * np.pi * (doy - 205) / 365), 0, None))
    if code == "KSTP":                       # the Pescadero refuelling outage, 7 to 30 April (local)
        nuc[(doy >= 97) & (doy <= 120)] = 0.0
    # run-of-river: the season's flow, with the hour-to-hour wander of the river and the plants' own operation (its own
    # random stream, so the rest of the area's year is drawn as before)
    hrng = np.random.default_rng(W.SEED + 101 + W.ORDER.index(code))
    hydro = a.get("hydro", 0) * (1 + 0.35 * np.cos(2 * np.pi * (doy - 140) / 365)) * (1 + ar1(hrng, H, 0.9, 0.0025))
    ti = (a.get("ti", 0) + a.get("ti_sd", 50) * rng.normal(0, 1, nd))[dayidx] + np.round(rng.normal(0, 6, H))
    net = load + ti - nuc - hydro - wind - usolar
    blocks = sorted(a["blocks"], key=lambda b: b[3])
    caps = np.array([sum(p[2] for p in b[5]) for b in blocks], dtype=float)
    mn = np.array([[caps[k] * b[4][s] for s in range(4)] for k, b in enumerate(blocks)])[:, season]
    # peaking units (combustion turbines, oil steam) run a readiness test each month: the first Wednesday, 9 to 11 pm
    # on the local clock, one unit at part load (about a twelfth of the block's capacity)
    first_wed = np.zeros(H, bool)
    for mth in range(1, 13):
        days = np.unique(doy[(mon == mth) & (dow == 2)])
        if len(days):
            first_wed |= (doy == days.min()) & (mon == mth)
    test = first_wed & ((lh == 21) | (lh == 22))
    for k, b in enumerate(blocks):
        if b[2] == "GT" or b[1] == "petroleum":
            mn[k] = np.where(test, np.maximum(mn[k], 0.08 * caps[k]), mn[k])
    rooms = caps[:, None] - mn
    rem0 = net - mn.sum(axis=0)
    costs = sorted(set(b[3] for b in blocks))
    groups = [[k for k, b in enumerate(blocks) if b[3] == c] for c in costs]
    out = {b[0]: mn[k].copy() for k, b in enumerate(blocks)}
    brate = {b[0]: sum(p[2] * p[3] for p in b[5]) / sum(p[2] for p in b[5]) for b in blocks}
    mer = np.zeros(H)
    cum = np.zeros(H)
    for g in groups:
        groom = rooms[g].sum(axis=0)
        take = np.clip(rem0 - cum, 0, groom)
        share = take / groom
        for k in g:
            out[blocks[k][0]] += share * rooms[k]
        rate = sum(rooms[k] * brate[blocks[k][0]] for k in g) / groom
        m = (rem0 >= cum) & (rem0 < cum + groom)
        mer[m] = rate[m]
        cum = cum + groom
    # units off the margin drift a little around their set points (ambient temperature, auxiliary load); the
    # marginal group takes up the difference, so net generation still meets the area's need hour by hour
    wig = {b[0]: ar1(rng, H, 0.8, 0.0015) * caps[k] for k, b in enumerate(blocks)}
    on_margin = {}
    cum2 = np.zeros(H)
    for g in groups:
        groom = rooms[g].sum(axis=0)
        m = (rem0 >= cum2) & (rem0 < cum2 + groom)
        for k in g:
            on_margin[blocks[k][0]] = m
        cum2 = cum2 + groom
    drift = np.zeros(H)
    for k, b in enumerate(blocks):
        loaded = (out[b[0]] > 1.0) & ~on_margin[b[0]]
        d = np.where(caps[k] - out[b[0]] < 1.0, -np.abs(wig[b[0]]), wig[b[0]])     # at full output: below nameplate
        d = np.clip(np.where(loaded, d, 0.0), -(out[b[0]] - mn[k]) * 0.5, (caps[k] - out[b[0]]) * 0.5)
        out[b[0]] = out[b[0]] + d
        drift += d
    mroom = sum(rooms[j] * on_margin[blocks[j][0]] for j in range(len(blocks)))
    for k, b in enumerate(blocks):
        out[b[0]] = np.where(on_margin[b[0]], out[b[0]] - drift * rooms[k] / np.where(mroom > 0, mroom, 1.0), out[b[0]])
    if not ((rem0 >= 0).all() and (rem0 < cum).all()):
        raise RuntimeError("%s: %d hours below must-run, %d above capacity, net min %.0f must-run %.0f" % (code, (rem0 < 0).sum(), (rem0 >= cum).sum(), net.min(), mn.sum(axis=0).max()))
    plants = {}
    for b in blocks:
        tot = sum(p[2] for p in b[5])
        for p in b[5]:
            plants[p[0]] = dict(code=p[0], name=p[1], fuel=b[1], pm=b[2], mw=p[2], rate=p[3], block=b[0],
                                gen=out[b[0]] * p[2] / tot)
    fuel = {}
    for b in blocks:
        fuel.setdefault(b[1], np.zeros(H))
        fuel[b[1]] += out[b[0]]
    return dict(code=code, lh=lh, doy=doy, mon=mon, dow=dow, season=season, dayidx=dayidx, load=load, ti=ti,
                nuc=nuc, hydro=hydro, wind=wind, usolar=usolar, fuel=fuel, out=out, plants=plants, mer=mer,
                cloud_d=cloud_d, net=net)


def simulate(seed=W.SEED):
    rng = np.random.default_rng(seed)
    return {code: dispatch(code, rng) for code in W.ORDER}


def published(g):
    """The agency's annual figures for one area from the register: net generation and CO2 by fuel, the output
    emission rates (all generation, fossil, by fuel) and the non-baseload output rate (combustion plants weighted by
    capacity factor: under 0.2 wholly non-baseload, over 0.8 wholly baseload, linear between)."""
    rows = list(g["plants"].values())
    gen = {r["code"]: float(r["gen"].sum()) for r in rows}
    co2 = {r["code"]: gen[r["code"]] * r["rate"] for r in rows}
    clean = {"nuclear": float(g["nuc"].sum()), "hydro": float(g["hydro"].sum()), "wind": float(g["wind"].sum()),
             "solar": float(g["usolar"].sum())}
    out = {"gen_fuel": {}, "co2_fuel": {}}
    for r in rows:
        out["gen_fuel"][r["fuel"]] = out["gen_fuel"].get(r["fuel"], 0.0) + gen[r["code"]]
        out["co2_fuel"][r["fuel"]] = out["co2_fuel"].get(r["fuel"], 0.0) + co2[r["code"]]
    for f, v in clean.items():
        if v > 0:
            out["gen_fuel"][f] = v
            out["co2_fuel"][f] = 0.0
    tot_gen = sum(out["gen_fuel"].values())
    tot_co2 = sum(out["co2_fuel"].values())
    fossil_gen = sum(gen.values())
    num = den = 0.0
    for r in rows:
        cf = gen[r["code"]] / (r["mw"] * H)
        f = 1.0 if cf < 0.2 else (0.0 if cf > 0.8 else (0.8 - cf) / 0.6)
        num += f * co2[r["code"]]
        den += f * gen[r["code"]]
    out.update(gen=tot_gen, co2=tot_co2, avg=tot_co2 / tot_gen, fossil=tot_co2 / fossil_gen, nb=num / den,
               rate_fuel={f: out["co2_fuel"][f] / out["gen_fuel"][f] for f in ("coal", "natural gas", "petroleum")
                          if out["gen_fuel"].get(f, 0) > 0},
               cf={r["code"]: gen[r["code"]] / (r["mw"] * H) for r in rows})
    return out
