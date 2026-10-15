"""Each candidate store's planned rooftop array, modelled by the engineering firm on 2025 weather: hourly AC output
in kilowatts on the store's local standard time, hour beginning, for the 8,760 hours of 2025."""
import datetime as dt

import numpy as np

import grid as G
import world as W

H = 8760


def lst_clock():
    t = [dt.datetime(2025, 1, 1) + dt.timedelta(hours=k) for k in range(H)]
    lh = np.array([x.hour for x in t])
    doy = np.array([x.timetuple().tm_yday for x in t])
    return t, lh, doy


def model(world, seed=W.SEED + 11):
    """kW AC by store, indexed by local standard hour of 2025. The array's sky follows its area's daily cloud
    (the same weather the area's own solar plants saw), with the site's own scatter."""
    rng = np.random.default_rng(seed)
    t, lh, doy = lst_clock()
    out = {}
    for code in W.ORDER:
        s = W.STORES[code]
        g = world[code]
        nd = len(g["cloud_d"])
        site = np.clip(g["cloud_d"] * (1 + rng.normal(0, 0.05, nd)), 0.22, 1.0)
        sky = site[doy] * (1 + G.ar1(rng, H, 0.7, 0.025))
        temp = 1.0 - 0.06 * np.clip(np.cos(2 * np.pi * (doy - 200) / 365), 0, None)       # summer heat derate
        dc = s["dc"] * 0.86 * G.solar_shape(lh, doy, s["lat"], s["tilt"]) * np.clip(sky, 0.15, 1.04) * temp
        ac = np.minimum(dc * 0.975, s["ac"])
        out[code] = np.round(np.where(ac < 0.05, 0.0, ac), 1)
    return out


def utc_index(code):
    """For each local-standard hour k of 2025 at the store, the UTC hour index of the grid row covering it, or -1
    past the end of the grid's UTC year."""
    off = W.AREAS[code]["utc"]
    k = np.arange(H) - off
    return np.where(k < H, k, -1)
