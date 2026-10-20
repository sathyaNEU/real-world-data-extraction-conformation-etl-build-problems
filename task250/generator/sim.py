"""The world: 148 agro-climatic stations in the middle Ebro valley, their daily mean air temperature over 2025 to 2027,
the anomalies the quality control reads, and the quality control itself (inverse-distance estimate from the three
nearest reporting stations, the 14-day drift statistic, alerts with a 14-day hold).

    W = world()      the stations, the true temperatures, the anomalies, the outages, the stations closing in 2028
    qc(W, a, pool)   the quality control run over anomalies `a` with the stations in `pool` as candidate neighbours
"""
import numpy as np
import pandas as pd

import params as P

D = P.DAYS
INV_LO, INV_HI = 0.5, 1.4
L_MESO, S_LOC = 28.0, 0.17
VALLEY_Z, PROG_R = 330.0, (3.0, 9.0)
KM = 1000.0
BOX = (600.0, 800.0, 4560.0, 4700.0)          # UTM 30N (ETRS89), km


def _layout(rng, elev):
    """108 core stations over the area; 34 programme stations that densified the irrigated valley floor, each a few
    kilometres from a core station there; 6 infill stations in the widest gaps left"""
    x0, x1, y0, y1 = BOX
    pts = []
    while len(pts) < 108:
        p = rng.uniform([x0 + 3, y0 + 3], [x1 - 3, y1 - 3])
        if all(np.hypot(*(p - q)) > 11.5 for q in pts):
            pts.append(p)
    core = np.array(pts)
    zc = elev(core[:, 0], core[:, 1])
    valley = np.where(zc < VALLEY_Z)[0]
    prog = []
    while len(prog) < 34:
        c = core[rng.choice(valley)]
        ang, r = rng.uniform(0, 2 * np.pi), rng.uniform(PROG_R[0], PROG_R[1])
        p = c + r * np.array([np.cos(ang), np.sin(ang)])
        if not (x0 + 2 < p[0] < x1 - 2 and y0 + 2 < p[1] < y1 - 2):
            continue
        allp = np.vstack([core] + ([np.array(prog)] if prog else []))
        if np.min(np.hypot(allp[:, 0] - p[0], allp[:, 1] - p[1])) > 3.0:
            prog.append(p)
    infill = []
    for _ in range(6):
        cand = rng.uniform([x0 + 3, y0 + 3], [x1 - 3, y1 - 3], size=(400, 2))
        allp = np.vstack([core, np.array(prog)] + ([np.array(infill)] if infill else []))
        dmin = np.min(np.hypot(cand[:, None, 0] - allp[None, :, 0], cand[:, None, 1] - allp[None, :, 1]), axis=1)
        infill.append(cand[rng.choice(np.argsort(-dmin)[:10])])
    xy = np.vstack([core, np.array(prog), np.array(infill)])
    group = ["core"] * 108 + ["programme"] * 34 + ["infill"] * 6
    return xy, group


def _district(x, y):
    if x < 650:
        return "CV" if y >= 4630 else "VJ"
    if x < 700:
        return "HH" if y >= 4630 else "RA"
    if x < 755:
        return "SB" if y >= 4645 else "MO"
    return "CM" if y >= 4615 else "BC"


def _elevation(x, y, rng):
    base = 175 + 0.032 * (y - 4560) ** 2 + 18 * np.sin((x - 600) / 23.0) + 25 * np.cos((y - 4560) / 17.0)
    hills = 160 * np.exp(-((x - 730) ** 2 + (y - 4600) ** 2) / 300.0) + 120 * np.exp(-((x - 640) ** 2 + (y - 4585) ** 2) / 220.0)
    return np.clip(base + hills + rng.normal(0, 22, size=np.shape(x)), 150, 980)


def world(seed=250):
    rng = np.random.default_rng(seed)
    er = np.random.default_rng(seed + 1)
    xy, group = _layout(rng, lambda x, y: _elevation(x, y, er))
    N = len(xy)
    order = np.argsort(rng.random(N))                      # station codes not in siting order
    xy = xy[order]
    group = [group[i] for i in order]
    z = _elevation(xy[:, 0], xy[:, 1], np.random.default_rng(seed + 1))
    dist = np.hypot(xy[:, None, 0] - xy[None, :, 0], xy[:, None, 1] - xy[None, :, 1])
    st = pd.DataFrame({"x_km": xy[:, 0], "y_km": xy[:, 1], "z_m": np.round(z), "group": group})
    st["district"] = [_district(a, b) for a, b in xy]

    # weather: large scale (shared), mesoscale field, winter inversions, station noise
    r2 = np.random.default_rng(seed + 2)
    t = np.arange(D)
    doy = t % 365
    clim = 15.4 + 9.6 * np.sin(2 * np.pi * (doy - 110) / 365)
    ls = np.zeros(D)
    for k in range(1, D):
        ls[k] = 0.8 * ls[k - 1] + r2.normal(0, 3.0 * np.sqrt(1 - 0.64))
    L = L_MESO
    C = np.exp(-dist / L) + 1e-9 * np.eye(N)
    Lc = np.linalg.cholesky(C)
    winter = np.clip(np.cos(2 * np.pi * (doy - 15) / 365), 0, None)
    sd_meso = 0.70 * (1 + 0.45 * winter)
    meso = np.zeros((D, N))
    zz = Lc @ r2.standard_normal(N)
    for k in range(D):
        zz = 0.65 * zz + np.sqrt(1 - 0.65 ** 2) * (Lc @ r2.standard_normal(N))
        meso[k] = sd_meso[k] * zz
    # inversion spells, November to February: stations below the lid run cold against the slopes
    inv = np.zeros(D)
    k = 0
    while k < D:
        m = (P.START + pd.Timedelta(days=int(k)).to_pytimedelta()).month
        if m in (11, 12, 1, 2) and r2.random() < 0.09:
            n = int(r2.integers(3, 13))
            inv[k:k + n] = r2.uniform(INV_LO, INV_HI)
            k += n
        else:
            k += 1
    lid = 360 + 40 * np.sin((xy[:, 0] - 600) / 40.0)
    below = 1 / (1 + np.exp((z - lid) / 50.0))
    inversion = -inv[:, None] * below[None, :]
    s_loc = S_LOC * r2.lognormal(0, 0.33, N)
    local = r2.standard_t(6, size=(D, N)) * np.sqrt(4 / 6) * s_loc[None, :]
    bias = r2.normal(0, 0.35, N)
    lapse = -0.0060 * (z - 300)
    T = clim[:, None] + lapse[None, :] + bias[None, :] + ls[:, None] + meso + inversion + local

    # the quality control's monthly normals (2015 to 2024; the infill stations' interpolated from their neighbours)
    month = np.array([(P.START + pd.Timedelta(days=int(k)).to_pytimedelta()).month for k in range(D)])
    mclim = np.array([clim[month == m].mean() for m in range(1, 13)])
    eps = r2.normal(0, 0.08, (12, N))
    for i in range(N):
        if group[i] == "infill":
            eps[:, i] = r2.normal(0, 0.22, 12)
    normals = mclim[:, None] + lapse[None, :] + bias[None, :] - 0.55 + eps   # the 2015-2024 decade ran cooler
    # availability: outages
    avail = np.ones((D, N), bool)
    r3 = np.random.default_rng(seed + 3)
    for i in range(N):
        for _ in range(r3.poisson(4.0)):
            s = int(r3.integers(0, D))
            n = int(min(40, r3.geometric(1 / 5.5)))
            avail[s:s + n, i] = False
    # the programme's stations the irrigation communities do not take over close on 31 December 2027
    rc = np.random.default_rng(seed + 103)
    prog = [i for i in range(N) if group[i] == "programme"]
    closing = sorted(int(x) for x in rc.choice(prog, P.N_CLOSING, replace=False))
    # the drift faults (ramps) are placed once the quality control's record is known (records.recorded)
    return {"st": st, "dist": dist, "T": T, "normals": normals, "month": month, "avail": avail, "faults": [],
            "closing": closing, "clim": clim, "doy": doy, "N": N}


def anomalies(W, drift_end=None):
    """the anomaly the quality control reads: the day's mean against the station's normal for the month, with any drift"""
    T = W["T"].copy()
    for f in W["faults"]:
        t1 = drift_end.get(f["i"], {}).get(f["start"], D) if drift_end else D
        k = np.arange(f["start"], t1)
        T[k, f["i"]] += f["rate"] * (k - f["start"] + 1)
    a = T - W["normals"][W["month"] - 1, :]
    a[~W["avail"]] = np.nan
    return a, T


def neighbour_order(W, pool):
    dist = W["dist"]
    N = W["N"]
    out = []
    for i in range(N):
        o = [j for j in np.argsort(dist[i]) if j != i and pool[j] and dist[i, j] <= P.RADIUS_KM]
        out.append(np.array(o[:30], int))
    return out


def qc(W, a, pool):
    """the inverse-distance estimate from the three nearest pool stations reporting that day, the residual, and the
    14-day drift statistic on each read day (at least 10 residuals in the window); returns residual, statistic and
    neighbours used"""
    N = W["N"]
    dist = W["dist"]
    order = neighbour_order(W, pool)
    R = np.full((D, N), np.nan)
    NB = np.full((D, N, 3), -1, int)
    have = ~np.isnan(a)
    for i in range(N):
        o = order[i]
        if len(o) < 3:
            continue
        av = have[:, o]
        c = np.cumsum(av, axis=1)
        pick = av & (c <= 3)
        ok = (c[:, -1] >= 3) & have[:, i]
        w = 1.0 / dist[i, o] ** 2
        W3 = pick * w[None, :]
        est = np.nansum(np.where(pick, a[:, o], 0.0) * w[None, :], axis=1) / np.where(ok, W3.sum(1), 1)
        R[ok, i] = a[ok, i] - est[ok]
        idx = np.argsort(~pick, axis=1, kind="stable")[:, :3]
        NB[ok, i, :] = o[idx[ok]]
    Dst = rolling(R)
    Dst[~have] = np.nan                                    # a statistic on the station's read days only
    return R, Dst, NB


def rolling(R):
    v = np.where(np.isnan(R), 0.0, R)
    n = (~np.isnan(R)).astype(int)
    cv = np.vstack([np.zeros((1, R.shape[1])), np.cumsum(v, 0)])
    cn = np.vstack([np.zeros((1, R.shape[1]), int), np.cumsum(n, 0)])
    w = P.WINDOW
    S = np.full_like(R, np.nan)
    for t in range(R.shape[0]):                            # the record starts on 1 January 2025 with no residual before
        t0 = max(0, t + 1 - w)
        cnt = cn[t + 1] - cn[t0]
        s = (cv[t + 1] - cv[t0]) / np.where(cnt > 0, cnt, 1)
        S[t] = np.where(cnt >= P.MIN_IN_WINDOW, s, np.nan)
    return S


def alerts(stat, limit, stations=None):
    """alert days: the statistic beyond the limit with no alert for the station in the previous 14 days"""
    Dn, N = stat.shape
    out = []
    for i in (range(N) if stations is None else stations):
        s, th = stat[:, i], limit[i] if np.ndim(limit) == 1 else limit[:, i]
        last = -10 ** 6
        for t in range(Dn):
            v = s[t]
            if v != v:
                continue
            lim = th if np.ndim(th) == 0 else th[t]
            if abs(v) > lim and t - last > P.HOLD_DAYS:
                out.append((i, t))
                last = t
    return out
