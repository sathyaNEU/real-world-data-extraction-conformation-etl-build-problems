"""The physical world behind the pack: the panel's 160 homes, the sky over each region, each home's solar and
general-supply use half hour by half hour in market time (UTC+10), the network's export limits and what the inverters
recorded under them. Nothing here is shipped as it stands; records.py writes the files from it."""
import numpy as np

import params as P

HH = 17520                      # half hours in 2025, market time
H = HH // 2
DOY = (np.arange(HH) // 48) + 1           # day of year 1..365
TOD = (np.arange(HH) % 48) * 0.5 + 0.25   # mid-point of the half hour, market-time clock hours
DOW = (np.arange(HH) // 48 + 2) % 7        # 1 Jan 2025 was a Wednesday: 0 = Monday

# region climate: latitude, longitude, mean clearness, its spread, seasonal swing of clearness, cooling and heating
REGION = {
    "WEN": dict(lat=-34.9, lon=151.3, k=0.60, ksd=0.20, kseas=0.04, cool=0.35, heat=0.30),
    "BEL": dict(lat=-34.2, lon=150.6, k=0.60, ksd=0.21, kseas=0.06, cool=0.80, heat=0.45),
    "YAR": dict(lat=-33.6, lon=148.9, k=0.66, ksd=0.18, kseas=0.08, cool=1.10, heat=0.40),
    "TAR": dict(lat=-35.6, lon=149.6, k=0.54, ksd=0.22, kseas=0.06, cool=0.20, heat=1.10),
}

# load shapes, half-hourly weights over the day (market time), weekday and weekend
_FAM_WD = [.42,.36,.33,.32,.31,.31,.32,.33,.36,.42,.55,.85,1.15,1.25,1.05,.80,.62,.55,.52,.52,.52,.53,.55,.57,
           .58,.60,.62,.66,.72,.80,.92,1.05,1.25,1.55,1.85,2.05,2.15,2.10,1.95,1.75,1.55,1.35,1.15,.95,.80,.66,.55,.48]
_RET_WD = [.40,.35,.33,.32,.31,.31,.31,.32,.34,.38,.45,.58,.75,.92,1.02,1.08,1.10,1.12,1.10,1.06,1.02,1.00,1.00,1.02,
           1.05,1.06,1.05,1.04,1.04,1.06,1.10,1.18,1.30,1.45,1.58,1.62,1.55,1.42,1.28,1.15,1.02,.90,.78,.66,.56,.49,.45,.42]
_CPL_WD = [.40,.35,.32,.31,.30,.30,.31,.32,.36,.45,.62,.95,1.20,1.15,.85,.55,.42,.38,.36,.35,.35,.35,.36,.37,
           .38,.39,.40,.42,.46,.52,.62,.78,1.05,1.40,1.75,1.95,2.00,1.90,1.72,1.52,1.32,1.12,.94,.78,.64,.54,.47,.43]
_WKE = [.45,.38,.34,.33,.32,.32,.32,.33,.34,.36,.40,.48,.62,.80,.98,1.12,1.22,1.28,1.30,1.30,1.28,1.25,1.22,1.20,
        1.18,1.17,1.16,1.16,1.18,1.22,1.28,1.36,1.48,1.62,1.75,1.82,1.80,1.70,1.55,1.40,1.25,1.10,.96,.82,.70,.60,.52,.47]
SHAPES = {}
for name, wd in {"family": _FAM_WD, "retired": _RET_WD, "couple": _CPL_WD}.items():
    a, b = np.array(wd), np.array(_WKE)
    SHAPES[name] = (a / a.sum(), b / b.sum())

# the panel: homes per region and how they were drawn
PANEL_SPEC = {
    "WEN": [dict(n=40, kwp=(5.4, 6.6), ac=(4.6, 5.0), day=(8.35, 11.25), types={"retired": .60, "couple": .25, "family": .15},
                 conn=(2012, 2022), limit=5.0, code="BMEG-5K")],
    "BEL": [dict(n=32, kwp=(3.28, 4.68), ac=(3.0, 4.6), day=(20.0, 28.0), types={"family": .72, "couple": .18, "retired": .10},
                 conn=(2011, 2021), limit=5.0, code="BMEG-5K"),
            dict(n=8, kwp=(4.2, 5.2), ac=(4.0, 5.0), day=(19.0, 26.0), types={"family": .75, "couple": .25},
                 conn=(2022, 2023), limit=1.5, code="BMEG-1K5")],
    "YAR": [dict(n=12, kwp=(2.43, 3.43), ac=(2.5, 3.6), day=(11.0, 15.0), types={"retired": .45, "couple": .30, "family": .25},
                 conn=(2010, 2021), limit=5.0, code="BMEG-5K"),
            dict(n=28, kwp=(6.6, 8.0), ac=(5.0, 6.0), day=(18.6, 24.6), types={"family": .80, "couple": .20},
                 conn=(2023.55, 2024.15), limit=0.5, code="BMEG-ZX", az="N")],
    "TAR": [dict(n=40, kwp=(2.88, 4.34), ac=(2.8, 4.5), day=(14.0, 19.0), types={"family": .50, "retired": .30, "couple": .20},
                 conn=(2011, 2022), limit=5.0, code="BMEG-5K")],
}
AZIMUTHS = {"N": 0.0, "NE": 45.0, "NW": -45.0, "EW": None}
AZ_P = {"N": .62, "NE": .13, "NW": .13, "EW": .12}


def _sun(lat, lon):
    phi = np.radians(lat)
    gamma = 2 * np.pi * (DOY - 1 + (TOD - 12) / 24) / 365
    decl = (0.006918 - 0.399912 * np.cos(gamma) + 0.070257 * np.sin(gamma) - 0.006758 * np.cos(2 * gamma)
            + 0.000907 * np.sin(2 * gamma) - 0.002697 * np.cos(3 * gamma) + 0.00148 * np.sin(3 * gamma))
    eot = 229.18 * (0.000075 + 0.001868 * np.cos(gamma) - 0.032077 * np.sin(gamma) - 0.014615 * np.cos(2 * gamma)
                    - 0.040849 * np.sin(2 * gamma))
    solar_time = TOD + (lon - 150.0) / 15.0 + eot / 60.0
    omega = np.radians(15.0 * (solar_time - 12.0))
    sin_alt = np.sin(phi) * np.sin(decl) + np.cos(phi) * np.cos(decl) * np.cos(omega)
    alt = np.arcsin(np.clip(sin_alt, -1, 1))
    cos_az = (np.sin(decl) - np.sin(alt) * np.sin(phi)) / np.maximum(np.cos(alt) * np.cos(phi), 1e-9)
    az = np.arccos(np.clip(cos_az, -1, 1))
    az = np.where(omega > 0, 2 * np.pi - az, az)        # degrees from north, clockwise
    sun = np.stack([np.cos(alt) * np.sin(az), np.cos(alt) * np.cos(az), np.sin(alt)])
    return sun, sin_alt


def _poa(sun, sin_alt, k, az_deg, tilt):
    """Plane-of-array irradiance (W/m2) for a plane facing az_deg from north at tilt degrees, under clearness k."""
    s = np.clip(sin_alt, 0, None)
    ghi_clear = 1040.0 * s ** 1.15
    ghi = k * ghi_clear
    df = np.clip(1.0 - 0.95 * k + 0.12 * (1 - s), 0.12, 1.0)
    dhi = ghi * df
    dni = np.where(s > 0.03, (ghi - dhi) / np.maximum(s, 0.03), 0.0)
    b = np.radians(tilt)
    if az_deg is None:
        parts = []
        for a in (90.0, 270.0):
            ar = np.radians(a)
            n = np.array([np.sin(b) * np.sin(ar), np.sin(b) * np.cos(ar), np.cos(b)])
            cos_t = np.clip(n @ sun, 0, None)
            parts.append(dni * cos_t + dhi * (1 + np.cos(b)) / 2 + ghi * 0.2 * (1 - np.cos(b)) / 2)
        return 0.5 * (parts[0] + parts[1])
    ar = np.radians(az_deg)
    n = np.array([np.sin(b) * np.sin(ar), np.sin(b) * np.cos(ar), np.cos(b)])
    cos_t = np.clip(n @ sun, 0, None)
    return dni * cos_t + dhi * (1 + np.cos(b)) / 2 + ghi * 0.2 * (1 - np.cos(b)) / 2


def _sky(rng, r):
    c = REGION[r]
    seas = c["kseas"] * np.cos(2 * np.pi * (np.arange(365) - 15) / 365)     # clearer in summer
    z = np.zeros(365)
    e = rng.normal(0, 1, 365)
    for i in range(1, 365):
        z[i] = 0.55 * z[i - 1] + np.sqrt(1 - 0.55 ** 2) * e[i]
    kd = np.clip(c["k"] + seas + c["ksd"] * z, 0.06, 0.92)
    k = np.repeat(kd, 48)
    sd = 0.22 * 4 * k * (1 - k)
    u = rng.normal(0, 1, HH)
    v = np.convolve(u, np.ones(3) / np.sqrt(3), mode="same")
    k = np.clip(k + sd * v, 0.04, 1.0)
    temp = 17.0 + 8.5 * np.cos(2 * np.pi * (np.arange(365) - 20) / 365) + rng.normal(0, 3.0, 365)
    return k, temp


def _load(rng, typ, day_kwh, temp, c):
    wd, we = SHAPES[typ]
    shape = np.where(DOW[:, None] >= 5, we[None, :], wd[None, :])[:, 0] if False else None
    hh_of_day = np.arange(HH) % 48
    weekend = DOW >= 5
    base_shape = np.where(weekend, we[hh_of_day], wd[hh_of_day])
    t = np.repeat(temp, 48)
    cool = c["cool"] * np.clip(np.repeat(temp, 48) - 24.0, 0, None) / 10.0
    heat = c["heat"] * np.clip(14.0 - t, 0, None) / 8.0
    cool_shape = np.clip(np.sin(np.pi * (TOD - 11.0) / 12.0), 0, None)            # afternoon into evening
    heat_shape = np.where((TOD >= 6) & (TOD < 9), 1.0, 0.0) + np.where((TOD >= 17) & (TOD < 23), 1.3, 0.0)
    daily = day_kwh * np.repeat(np.clip(rng.lognormal(0, 0.12, 365), 0.6, 1.6), 48)
    load = daily * base_shape * (1 + cool * cool_shape * 1.6 + heat * heat_shape * 0.9)
    load = load * np.clip(rng.lognormal(0, 0.28, HH), 0.35, 3.5)
    return load


SUBURBS = {
    "WEN": [("Coral Bay", "2587"), ("Pelican Heads", "2589"), ("Sandhaven", "2590"), ("Port Ellery", "2592")],
    "BEL": [("Eastbrook", "2711"), ("Cedar Park", "2713"), ("Ashgrove", "2714"), ("Stonebridge South", "2716")],
    "YAR": [("Yarrandale", "2804"), ("Mulga Flats", "2806"), ("Riverbend Estate", "2807"), ("Quarry Hill Estate", "2809")],
    "TAR": [("Tarrock", "2902"), ("Mount Ellis", "2904"), ("Glenvale", "2905"), ("Fernhill", "2907")],
}
# the new estates in Yarrandale sit on the two feeders out of the Riverbend zone substation
NEW_ESTATE_SUBURBS = [("Riverbend Estate", "2807"), ("Quarry Hill Estate", "2809")]


def build():
    rng = np.random.default_rng(P.SEED)
    srng = np.random.default_rng([P.SEED, 7])
    homes = []
    skies = {}
    for r in P.REGION_ORDER:
        sun, sin_alt = _sun(REGION[r]["lat"], REGION[r]["lon"])
        k, temp = _sky(rng, r)
        skies[r] = dict(k=k, temp=temp, sun=sun, sin_alt=sin_alt)
        idx = 0
        for spec in PANEL_SPEC[r]:
            for j in range(spec["n"]):
                idx += 1
                kwp = round(float(rng.uniform(*spec["kwp"])) * 10) / 10
                ac = min(round(float(rng.uniform(*spec["ac"])) * 2) / 2, spec["ac"][1])
                # arrays are sized to at most 133 per cent of the inverter, the installers' rule for the rebate
                kwp = min(kwp, np.floor(ac * 1.33 * 10) / 10)
                azk = rng.choice(list(AZ_P), p=list(AZ_P.values()))
                azk = spec.get("az", azk)                     # the estates' builder put every array on the north roof
                tilt = float(rng.uniform(14, 24))
                typ = rng.choice(list(spec["types"]), p=list(spec["types"].values()))
                day_kwh = float(rng.uniform(*spec["day"]))
                conn = float(rng.uniform(*spec["conn"]))
                hf = float(np.clip(rng.normal(1.0, 0.015), 0.96, 1.04))           # shading, soiling, panel quality
                poa = _poa(sun, sin_alt, k, AZIMUTHS[azk], tilt)
                pr = 0.82 - 0.05 * np.clip((np.repeat(temp, 48) - 20) / 15, 0, 1)
                noise = np.clip(rng.normal(1.0, 0.01, HH), 0.96, 1.04)
                pot_kw = np.minimum(kwp * poa / 1000.0 * pr * hf * noise, ac)
                pot = pot_kw * 0.5                                                  # kWh in the half hour
                load = _load(rng, typ, day_kwh, temp, REGION[r]) 
                lim = spec["limit"]
                if lim >= ac:
                    rec = pot.copy()
                else:
                    over = np.where(rng.random(HH) < 0.06, rng.uniform(0.0, 0.03, HH), 0.0) if lim == 0 else 0.0
                    rec = np.minimum(pot, load + lim * 0.5 + over)
                exp_ = np.maximum(rec - load, 0.0)
                imp = np.maximum(load - rec, 0.0)
                if lim == 0.5:
                    sub = NEW_ESTATE_SUBURBS[int(srng.integers(0, 2))]
                else:
                    pool = [x for x in SUBURBS[r] if x not in NEW_ESTATE_SUBURBS]
                    sub = pool[int(srng.integers(0, len(pool)))]
                cl_p = {"WEN": .22, "BEL": .30, "YAR": .45, "TAR": .55}[r]
                cl_kwh = float(srng.uniform(2.6, 4.6)) if srng.random() < cl_p else 0.0
                homes.append(dict(region=r, idx=idx, kwp=kwp, ac=ac, az=azk, tilt=round(tilt, 1), typ=typ,
                                  day_kwh=day_kwh, conn=conn, hf=hf, limit=lim, code=spec["code"],
                                  suburb=sub[0], postcode=sub[1], cl_kwh=cl_kwh,
                                  pot=pot, load=load, rec=rec, imp=imp, exp=exp_))
    return dict(homes=homes, skies=skies)


def hourly(a):
    return a.reshape(-1, 2).sum(axis=1)


def battery(gen_h, load_h, cap=P.BAT_USABLE_KWH, pmax=P.BAT_POWER_KW, ec=P.BAT_CHARGE_EFF, ed=P.BAT_DISCHARGE_EFF):
    """Hour-by-hour self-consumption battery over many homes at once: gen_h and load_h are (homes, hours) arrays.
    Returns the energy delivered to each home's use over the period."""
    n, T = gen_h.shape
    soc = np.zeros(n)
    out = np.zeros(n)
    sur = gen_h - load_h
    for t in range(T):
        s = sur[:, t]
        c = np.minimum(np.minimum(np.clip(s, 0, None), pmax), (cap - soc) / ec)
        soc = soc + c * ec
        d = np.minimum(np.minimum(np.clip(-s, 0, None), pmax), soc * ed)
        soc = soc - d / ed
        out += d
    return out
