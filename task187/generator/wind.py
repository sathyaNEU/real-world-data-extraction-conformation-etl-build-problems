"""The wind and the turbines' physics on the UTC interval index.

The met mast sees the free stream at 80 m. Each turbine sees its own wind: the mast's, scaled by its place, slowed in
a neighbour's wake, and slowed in the plantation's lee; and its own turbulence: the ambient turbulence, plus a wake's
added turbulence (Frandsen), plus the plantation's eddies at the three west-row turbines nearest the trees, less over
the loch at CH02. A ten-minute mean power is the zero-turbulence power curve averaged over a Gaussian spread of wind
inside the interval (sd = turbulence intensity x mean wind, IEC 61400-12-1 Annex M), at the density-corrected wind,
with the blade set's loss of power coefficient below rated."""
import numpy as np
from scipy import stats

import world as W

N = W.N
R = W.ROTOR_D / 2.0
AREA = np.pi * R ** 2
CP = 0.47
U = np.linspace(-3.5, 3.5, 57)
WQ = stats.norm.pdf(U)
WQ = WQ / WQ.sum()

# the plantation's eddies (sector of mast wind direction, added turbulence at full strength) and the loch
FOREST = {"CH07": (200.0, 305.0, 0.17), "CH05": (215.0, 285.0, 0.12), "CH01": (255.0, 320.0, 0.23)}
FOREST_SLOW = 0.96
LOCH = {"CH02": (190.0, 320.0, 0.45, 0.85)}   # over the loch: smooth at low wind, rougher water as the wind rises
WAKE_K = 0.075


def rng(*keys):
    return np.random.default_rng([W.SEED] + [abs(hash_key(k)) for k in keys])


def hash_key(k):
    import hashlib
    return int(hashlib.sha256(str(k).encode()).hexdigest()[:12], 16)


def p0(v, loss=0.0):
    """The zero-turbulence power curve at standard density (kW), with a fractional loss of power coefficient. A gust
    above cut-out inside the ten minutes does not stop the turbine (the controller stops on the mean), so the curve
    holds rated power above rated wind speed."""
    v = np.asarray(v, float)
    p = 0.5 * 1.225 * AREA * CP * (1.0 - loss) * v ** 3 / 1000.0
    p = np.where(v < W.CUT_IN, 0.0, p)
    return np.minimum(p, W.RATED_KW)


def p_ti(v, ti, loss=0.0):
    """The ten-minute mean power at mean wind v (density-corrected) and turbulence intensity ti."""
    v = np.asarray(v, float)
    ti = np.asarray(ti, float)
    loss = np.broadcast_to(np.asarray(loss, float), np.broadcast(v, ti).shape)
    out = np.empty(np.broadcast(v, ti).shape)
    vb, tb = np.broadcast_to(v, out.shape), np.broadcast_to(ti, out.shape)
    flat = out.reshape(-1)
    vf, tf, lf = vb.reshape(-1), tb.reshape(-1), loss.reshape(-1)
    step = 200000
    for a in range(0, flat.size, step):
        vv = vf[a:a + step, None] * (1.0 + tf[a:a + step, None] * U)
        flat[a:a + step] = (p0(np.maximum(vv, 0.0), lf[a:a + step, None]) * WQ).sum(-1)
    return out


def ti_typical(v):
    """The site's ambient turbulence intensity at hub height by mean wind (the warranted curve's own)."""
    return 0.065 + 0.30 / np.maximum(v, 1.5)


def warranted():
    """The warranted power curve, 3.0 to 25.0 m/s in 0.5 m/s steps at 1.225 kg/m3: the bin-mean power of a sound
    turbine in the type test's turbulence (the site's ambient), as the supply agreement's Schedule 3 states it."""
    speeds = np.round(np.arange(3.0, 25.01, 0.5), 1)
    fine = np.linspace(-0.24, 0.24, 25)
    kw = np.array([p_ti(c + fine, ti_typical(c + fine)).mean() for c in speeds])
    kw = np.round(kw).astype(int)
    cp = kw * 1000.0 / (0.5 * 1.225 * AREA * speeds ** 3)
    return speeds, kw, np.round(cp, 3)


def bearing(a, b):
    (xa, ya), (xb, yb) = a, b
    return np.degrees(np.arctan2(xb - xa, yb - ya)) % 360.0


def angdiff(a, b):
    return (np.asarray(a) - b + 180.0) % 360.0 - 180.0


def in_sector(d, lo, hi):
    return (d > lo) & (d < hi)


def ct(v):
    return np.interp(v, [0, 3, 8, 10, 12, 15, 20, 25], [0.0, 0.85, 0.80, 0.65, 0.45, 0.25, 0.10, 0.06])


def mast():
    """The met mast's ten-minute record (free stream at 80 m), on the UTC index."""
    g = rng("mast")
    t = np.arange(N)
    day = t / 144.0
    hour_utc = (t % 144) / 6.0
    season = 1 + 0.18 * np.cos(2 * np.pi * (day - 105) / 365.0)          # day 0 = 1 October; windiest mid-January
    diurnal = 1 + 0.05 * np.cos(2 * np.pi * (hour_utc - 14.4) / 24.0)
    x = np.zeros(N)
    e = g.normal(0, 1, N)
    phi = 0.995
    for i in range(1, N):
        x[i] = phi * x[i - 1] + np.sqrt(1 - phi ** 2) * e[i]
    v = 7.6 * season * diurnal * np.exp(0.42 * x - 0.5 * 0.42 ** 2)
    gd = rng("direction")
    spring = 0.72 - 0.10 * np.exp(-0.5 * ((day - 200) / 30.0) ** 2)      # more easterlies in April and May
    dmix = np.where(gd.random(N) < spring, gd.normal(245, 35, N), gd.normal(95, 40, N)) % 360
    d = np.empty(N)
    d[0] = dmix[0]
    sw = gd.random(N)
    for i in range(1, N):
        d[i] = d[i - 1] if sw[i] < 0.985 else dmix[i]
    d = (d + gd.normal(0, 8, N)) % 360
    west = in_sector(d, 200, 310)
    v = np.clip(v * np.where(west, 1.10, 0.86), 0.2, 32.0)
    gt = rng("turbulence")
    ti = np.clip(0.065 + 0.30 / np.maximum(v, 1.5) + gt.normal(0, 0.010, N), 0.04, 0.45)
    ti = ti * (1 + 0.10 * np.cos(2 * np.pi * (hour_utc - 13.5) / 24.0))
    ga = rng("air")
    xt = np.zeros(N)
    et = ga.normal(0, 1, N)
    for i in range(1, N):
        xt[i] = 0.998 * xt[i - 1] + np.sqrt(1 - 0.998 ** 2) * et[i]
    temp = 7.0 - 5.6 * np.cos(2 * np.pi * (day - 112) / 365.0) + 1.8 * np.cos(2 * np.pi * (hour_utc - 14.5) / 24.0) \
        + 2.6 * xt - 0.06 * (v - 8)
    xp = np.zeros(N)
    ep = ga.normal(0, 1, N)
    for i in range(1, N):
        xp[i] = 0.9993 * xp[i - 1] + np.sqrt(1 - 0.9993 ** 2) * ep[i]
    pres = 958.0 + 9.0 * xp - 0.55 * (v - 8.2)
    rh = np.clip(86 + 6 * np.cos(2 * np.pi * (day - 105) / 365.0) - 9 * np.cos(2 * np.pi * (hour_utc - 15) / 24.0)
                 + 7 * x + ga.normal(0, 3, N), 38, 100)
    rho = pres * 100.0 / (287.05 * (temp + 273.15))
    sd = ti * v * (1 + gt.normal(0, 0.04, N))
    return dict(v=v, dir=d, ti=ti, sd=sd, temp=temp, pres=pres, rh=rh, rho=rho)


def loss_series(name):
    loss = np.zeros(N)
    if name in W.EROSION:
        loss[:] = W.EROSION[name]
    if name == "CH09":
        loss[:W.interval_index(W.CH09_FAULT)] = W.CH09_OLD_ROTOR_LOSS
    return loss


def turbines(m):
    """Each turbine's wind, turbulence, nacelle direction and nacelle temperature, and the power it makes in normal
    operation with no limit (the free power), on the UTC index."""
    out = {}
    cti = ct(m["v"])
    for name in W.TURBINES:
        g = rng("turbine", name)
        place = 1.0 + 0.0008 * (W.ELEVATION[name] - W.MAST_ELEVATION) + g.normal(0, 0.006)
        loc = np.zeros(N)
        e = g.normal(0, 1, N)
        for i in range(1, N):
            loc[i] = 0.9 * loc[i - 1] + np.sqrt(1 - 0.81) * e[i]
        vfree = m["v"] * place * (1 + 0.03 * loc)
        dsum = np.zeros(N)
        isum = np.zeros(N)
        for other in W.TURBINES:
            if other == name:
                continue
            L = np.hypot(W.XY[other][0] - W.XY[name][0], W.XY[other][1] - W.XY[name][1])
            s = L / W.ROTOR_D
            if s > 15:
                continue
            b = bearing(W.XY[name], W.XY[other])
            half = np.degrees(np.arctan((1 + 2 * WAKE_K * s) / (2 * s)))
            w = np.exp(-0.5 * (angdiff(m["dir"], b) / (0.6 * half + 4.0)) ** 2)
            dsum += ((1 - np.sqrt(1 - cti)) / (1 + 2 * WAKE_K * s) ** 2 * w) ** 2
            isum += (1.0 / (1.5 + 0.8 * s / np.sqrt(np.maximum(cti, 0.05))) * w) ** 2
        v = vfree * (1 - np.sqrt(dsum))
        ti = np.sqrt((m["ti"] * (1.0 + g.normal(0, 0.02))) ** 2 + isum) * (1 + g.normal(0, 0.08, N))
        if name in FOREST:
            lo, hi, add = FOREST[name]
            sec = in_sector(m["dir"], lo, hi)
            v = np.where(sec, v * FOREST_SLOW, v)
            ramp = np.clip((v - 3.0) / 7.0, 0.15, 1.0)
            ti = np.where(sec, ti + add * ramp * (1 + g.normal(0, 0.15, N)), ti)
        if name in LOCH:
            lo, hi, f_low, f_high = LOCH[name]
            f = f_low + (f_high - f_low) * np.clip((v - 6.0) / 6.0, 0, 1)
            ti = np.where(in_sector(m["dir"], lo, hi), ti * f, ti)
        ti = np.clip(ti, 0.02, 0.6)
        v = np.clip(v, 0.1, 35.0)
        veff = v * (m["rho"] / 1.225) ** (1.0 / 3.0)
        loss = loss_series(name)
        p = p_ti(veff, ti, loss)
        gp = rng("power", name)
        sdp = 8.0 * np.clip((W.RATED_KW - p) / 150.0, 0, 1) * (p > 3)
        p = np.clip(p + gp.normal(0, 1, N) * sdp, 0, W.RATED_KW)
        sd = ti * v * (1 + gp.normal(0, 0.05, N))
        ndir = (m["dir"] + g.normal(0, 4, N) + g.normal(0, 2)) % 360
        ntemp = m["temp"] + 0.4 + g.normal(0, 0.25, N)
        out[name] = dict(v=v, veff=veff, ti=ti, sd=sd, ndir=ndir, ntemp=ntemp, pfree=p, loss=loss)
    return out
