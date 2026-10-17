"""task241 world: the Iberian Basin's water column (a seasonal upper ocean, the Mediterranean water near 1,000 m and
the deep layer below it, whose temperature fixes its salinity), the vertical heave of that column by eddies and by year,
the westward thinning of the Mediterranean influence, the array's 24 floats (trajectories, each 10-day cycle's profile,
each conductivity sensor's offset and drift) and the ship reference casts (the generator's clean truth: the water each
float sampled and what its sensors made of it)."""
import datetime as dt

import numpy as np

import params as P
import seawater as SW


class World:
    pass


# ------------------------------------------------------------------ the water column
def theta_ref(z):
    """potential temperature (deg C) of the undisplaced column at depth z (m)"""
    z = np.asarray(z, dtype=float)
    deep = P.TH_DEEP + P.TH_AMP * np.exp(-(np.maximum(z, 1000.0) - 1000.0) / P.TH_SCALE)
    upper = 11.2 + 2.8 * (1000.0 - np.minimum(z, 1000.0)) / 850.0          # 14.0 at 150 m to 11.2 at 1000 m
    return np.where(z >= 1000.0, deep, upper)


def s_deep(theta, lon):
    """practical salinity of deep water of potential temperature theta at longitude lon"""
    w = (theta - 3.5) / 3.3
    return 35.00 + P.S_A * (theta - 3.5) + P.S_B * (theta - 3.5) ** 2 + P.GAMMA * w * (lon - P.LON0)


def column(z, h, lon, season):
    """the water's potential temperature and salinity at depths z when the column is displaced h metres down; season
    is the day of year (the upper ocean's own cycle, not tied to h)"""
    zr = np.asarray(z, dtype=float) - h
    th = theta_ref(zr)
    s_d = s_deep(th, lon)
    # the Mediterranean water: a salinity maximum near 1,050 m, stronger to the east
    mow = 35.62 + (0.42 + 0.02 * (lon - P.LON0)) * np.exp(-((zr - 1050.0) / 230.0) ** 2)
    # the central water above it: salinity falls with temperature towards the Mediterranean water
    enacw = 35.62 + 0.115 * (th - 11.2)
    upper_s = np.maximum(mow, enacw)
    blend = np.clip((zr - 1050.0) / 150.0, 0.0, 1.0)
    s = blend * s_d + (1 - blend) * upper_s
    # the seasonal layer: warm and light in late summer, mixed deep in late winter
    phase = np.cos(2 * np.pi * (season - 236) / 365.0)                  # 1 in late August
    sst = 17.4 + 3.1 * phase
    mld = 70.0 - 55.0 * phase                                           # 15 m in late summer, 125 m in late winter
    th_top = theta_ref(150.0)
    seas = np.where(np.asarray(z) <= mld, sst,
                    th_top + (sst - th_top) * np.exp(-(np.asarray(z) - mld) / 45.0))
    th = np.where(np.asarray(z) < 150.0, np.maximum(th, seas), th)
    s = np.where(np.asarray(z) < 60.0, s + 0.04 * phase * (60.0 - np.asarray(z)) / 60.0, s)
    return th, s


def in_situ(theta, s, p):
    """in-situ temperature from potential temperature, salinity and pressure (dbar), the adiabatic warming with depth"""
    return SW.in_situ(theta, s, p)


def reflect(x, box):
    """a float meeting the edge of the basin's recirculation turns back into it"""
    lo, hi = box
    if x < lo:
        x = 2 * lo - x
    if x > hi:
        x = 2 * hi - x
    return float(x)


# ------------------------------------------------------------------ pressure levels a float reports
def float_levels(rng, pmax):
    lv = list(np.arange(4.0, 100.0, 5.0)) + list(np.arange(100.0, 300.0, 10.0)) + \
        list(np.arange(300.0, 1000.0, 25.0)) + list(np.arange(1000.0, pmax + 1.0, 50.0))
    p = np.array(lv) + rng.uniform(-1.2, 1.2, len(lv))
    p[0] = max(p[0], 3.0)
    return p[p <= pmax]


# ------------------------------------------------------------------ the floats
# sensor truth: "drift" floats lose salinity linearly from a start date at a yearly rate, "offset" floats carried a
# constant error from deployment, "clean" floats a small one


def make(seed=P.SEED):
    rng = np.random.default_rng([seed, 1])                                  # the floats and their tracks
    W = World()
    year0 = dt.datetime(P.YEAR, 1, 1)
    # ---------------------------------------------------------------- the floats and where they went
    floats = []
    for i in range(P.N_FLOATS):
        dep = dt.date(2023, 3, 1) + dt.timedelta(days=int(rng.integers(0, 1400)))
        lon0 = float(rng.uniform(-18.7, -11.6))
        lat0 = float(rng.uniform(37.9, 42.1))
        floats.append(dict(index=i, kind="clean", deployed=dep, lon0=lon0, lat0=lat0))
    # the sensors: a conductivity cell drifts after a year or more in the water, so the drifting four are among the
    # floats deployed before October 2025; two cells carried an error from deployment
    old = [f for f in floats if f["deployed"] < dt.date(2025, 10, 1)]
    for f in rng.choice(old, 4, replace=False):
        f["kind"] = "drift"
    for f in rng.choice([f for f in floats if f["kind"] == "clean"], 2, replace=False):
        f["kind"] = "offset"
    for f in floats:
        if f["kind"] == "offset":
            f["offset"] = float(rng.choice([1, -1]) * rng.uniform(0.019, 0.023))
            f["drift_start"], f["drift_rate"] = None, 0.0
        else:
            f["offset"] = float(np.clip(rng.normal(0, 0.0013), -0.003, 0.003))
            f["drift_start"], f["drift_rate"] = None, 0.0
        if f["kind"] == "drift":
            f["drift_start"] = dt.date(2026, 7, 1) + dt.timedelta(days=int(rng.integers(0, 150)))
            f["drift_rate"] = -float(rng.uniform(0.030, 0.042))           # per year
    W.floats = floats
    # ---------------------------------------------------------------- each float's 2027 cycles
    for f in floats:
        start = max(dt.datetime.combine(f["deployed"], dt.time(0)), year0 - dt.timedelta(days=12))
        # the float's own clock: it surfaces every 10 days at a time of day set at deployment
        hour = float(rng.uniform(0, 24))
        t = dt.datetime.combine(f["deployed"], dt.time(0)) + dt.timedelta(hours=hour)
        lon, lat = f["lon0"], f["lat0"]
        # walk the float from deployment to the end of 2027
        e = float(rng.normal(0, P.EDDY_SD))
        cyc = []
        k = 0
        while t < dt.datetime(P.YEAR + 1, 1, 1):
            k += 1
            t = t + dt.timedelta(days=10, minutes=float(rng.normal(0, 25)))
            lon = reflect(lon + float(rng.normal(-0.012, 0.09)), P.FLOAT_LON)
            lat = reflect(lat + float(rng.normal(-0.006, 0.07)), P.FLOAT_LAT)
            e = P.EDDY_PHI * e + float(rng.normal(0, P.EDDY_SD * np.sqrt(1 - P.EDDY_PHI ** 2)))
            if year0 <= t < dt.datetime(P.YEAR + 1, 1, 1):
                cyc.append(dict(cycle=k, time=t, lon=lon, lat=lat, heave=P.H_2027 + e + float(rng.normal(0, 4.0))))
        f["cycles"] = cyc
        f["first_cycle_2027"] = cyc[0]["cycle"] if cyc else None
    # ---------------------------------------------------------------- what each profile measured
    rng = np.random.default_rng([seed, 2])
    for f in floats:
        for c in f["cycles"]:
            pmax = float(rng.uniform(1985, 2012))
            p = float_levels(rng, pmax)
            doy = c["time"].timetuple().tm_yday
            th, s = column(p, c["heave"], c["lon"], doy)
            th = th + rng.normal(0, 0.0015, p.size)                         # fine structure
            s = s + rng.normal(0, 0.0012, p.size)
            c["p_true"], c["theta_true"], c["s_true"] = p, th, s
            days = (c["time"].date() - dt.date(P.YEAR, 1, 1)).days
            if f["drift_start"] is not None and c["time"].date() > f["drift_start"]:
                d = f["offset"] + f["drift_rate"] * (c["time"].date() - f["drift_start"]).days / 365.25
            else:
                d = f["offset"]
            c["delta"] = d
            c["p"] = p + rng.normal(0, 0.4, p.size)
            c["t"] = in_situ(th, s, p) + rng.normal(0, 0.0012, p.size)
            c["s"] = s + d + rng.normal(0, 0.0015, p.size)
            c["day"] = days
    # ---------------------------------------------------------------- the ship reference casts
    # one institute cruise a year, a section worked station by station over two to three weeks
    rng = np.random.default_rng([seed, 3])
    rng_pos = np.random.default_rng([seed, 31])                           # station keeping and the first station's time
    casts = []
    for yr in range(2015, 2026):
        H = float(rng.normal(0, 10.0))
        n = int(rng.integers(12, 19))
        section = rng.choice(["zonal", "meridional", "mixed"], p=[0.5, 0.25, 0.25])
        start = dt.datetime(yr, int(rng.choice([4, 5, 6, 9, 10])), int(rng.integers(1, 11)), int(rng.integers(6, 18))) + \
            dt.timedelta(minutes=int(rng_pos.integers(0, 60)))
        merid = float(rng.choice([-18.0, -15.0, -12.0]))
        when = start
        for j in range(n):
            if section == "zonal":
                lon, lat = -10.0 - 10.5 * j / max(n - 1, 1) + rng.normal(0, 0.05), 40.5 + rng.normal(0, 0.15)
            elif section == "meridional":
                lon, lat = merid + rng.normal(0, 0.1), 36.8 + 6.4 * j / max(n - 1, 1) + rng_pos.normal(0, 0.012)
            else:
                lon, lat = rng.uniform(-20.8, -9.8), rng.uniform(36.6, 43.4)
            if j:
                when = when + dt.timedelta(hours=float(rng.uniform(16, 34)))
            p = np.arange(5.0, 2201.0, 10.0)                                  # 10-dbar bins
            h = H + float(rng.normal(0, P.EDDY_SD))
            th, s = column(p, h, float(lon), when.timetuple().tm_yday)
            th = th + rng.normal(0, 0.0015, p.size)
            s = s + rng.normal(0, 0.0010, p.size)
            casts.append(dict(year=yr, date=when.date(), when=when.replace(second=0, microsecond=0), lon=float(lon),
                              lat=float(lat), p=p, theta=th, s=s, heave=h))
    W.casts = casts
    return W
