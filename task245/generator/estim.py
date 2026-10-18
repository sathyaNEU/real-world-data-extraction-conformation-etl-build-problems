"""task245 estimators on the clean truth: each station's count of days above 50 over its valid days, the whole-year count
under every reading the ladder and the closure walk (the station's own days: scaling, the 90.4th percentile,
interpolation; the network alone; the network plus the station's own response to the wind), and the call."""
import datetime as dt

import numpy as np

import params as P

D, H = P.DAYS, P.HOURS
HOD = np.arange(H) % 24
LIMIT, ALLOWED = 50.0, 35


def daily(xv, valid):
    """daily means over valid hours where 18 or more are valid; nan elsewhere"""
    n = xv.shape[0]
    cnt = valid.reshape(n, D, 24).sum(2)
    tot = np.where(valid, xv, 0.0).reshape(n, D, 24).sum(2)
    dm = np.where(cnt >= 18, tot / np.maximum(cnt, 1), np.nan)
    return dm, cnt >= 18


def whole_year(xv, valid, vd, dm, pred, mix):
    """days above 50 over the year: measured daily means on valid days, rebuilt ones on the others (all 24 hours from the
    rebuild, or the valid hours kept and the rest rebuilt)"""
    hrs = np.where(valid, xv, pred) if mix else pred
    reb = hrs.reshape(D, 24).mean(1)
    full = np.where(vd, dm, reb)
    return int((full > LIMIT).sum())


def sectors(theta, k):
    return (((theta + 180.0 / k) % 360) // (360.0 / k)).astype(int)


def wind_cells(inc, ok, theta, speed, wet_h, k, bands, wetsplit):
    """the station's mean increment over the background in each wind cell (sector x speed band x wet), from its valid
    hours; thin cells fall back to the sector, then to the station's mean"""
    sec = sectors(theta, k)
    sb = np.zeros(H, int) if bands == 1 else np.digitize(speed, [4.0] if bands == 2 else [3.0, 6.0])
    key = (sec * 4 + sb) * 2 + (wet_h.astype(int) if wetsplit else 0)
    m = ok & ~np.isnan(inc)
    nk = np.bincount(key[m], minlength=key.max() + 1)
    sk = np.bincount(key[m], weights=inc[m], minlength=key.max() + 1)
    ns = np.bincount(sec[m], minlength=k)
    ss = np.bincount(sec[m], weights=inc[m], minlength=k)
    overall = inc[m].mean()
    by_sec = np.where(ns > 0, ss / np.maximum(ns, 1), overall)
    return np.where(nk[key] >= 5, sk[key] / np.maximum(nk[key], 1), by_sec[sec])


def wind_harmonic(inc, ok, theta, speed, wet_h, order, use_speed, wetsplit):
    """the increment regressed on harmonics of the wind direction (times speed, and split wet and dry), valid hours"""
    th = np.radians(theta)
    cols = [np.ones(H)]
    for j in range(1, order + 1):
        cols += [np.cos(j * th), np.sin(j * th)]
    Z = np.column_stack(cols)
    if use_speed:
        Z = np.column_stack([Z, Z[:, 1:] * speed[:, None]])
    if wetsplit:
        Z = np.column_stack([Z * (~wet_h)[:, None], Z * wet_h[:, None]])
    m = ok & ~np.isnan(inc)
    coef, *_ = np.linalg.lstsq(Z[m], inc[m], rcond=None)
    return Z @ coef


def backgrounds(xv, valid, todo=None):
    """hourly background candidates for each station: the median of the other stations' valid hours, the mean of the
    council's background stations, the hour effect of a two-way (station plus hour) fit to the other stations, the rural
    station alone (todo: the stations to compute, the rest left at zero)"""
    n = xv.shape[0]
    todo = range(n) if todo is None else todo
    x = np.where(valid, xv, np.nan)
    out = {}
    med = np.zeros((n, H))
    for i in todo:
        o = [j for j in range(n) if j != i]
        with np.errstate(all="ignore"):
            med[i] = np.nanmedian(x[o], 0)
    out["median"] = med
    bgs = [P.CODES.index(c) for c in ("TH1", "TH2", "TH7")]
    with np.errstate(all="ignore"):
        b = np.nanmean(x[bgs], 0)
    out["council_bg"] = np.array([np.where(np.isnan(b), med[i], b) for i in range(n)])
    tw = np.zeros((n, H))
    for i in todo:
        o = [j for j in range(n) if j != i]
        xo = x[o]
        with np.errstate(all="ignore"):
            hb = np.nanmean(xo, 0)
            for _ in range(30):
                a = np.nanmean(xo - hb[None, :], 1)
                hb = np.nanmean(xo - a[:, None], 0)
        tw[i] = np.where(np.isnan(hb), np.nanmean(hb), hb)
    out["two_way"] = tw
    r7 = P.CODES.index("TH7")
    out["rural"] = np.array([np.where(valid[r7], xv[r7], med[i]) for i in range(n)])
    return out


def readings(xv, valid, W, which="all", only=None):
    """every reading of every station's whole-year count; returns {name: array of counts} (only: the stations to compute,
    the rest left at -1)"""
    n = xv.shape[0]
    todo = list(range(n)) if only is None else list(only)
    dm, vd = daily(xv, valid)
    M = np.array([int((dm[i][vd[i]] > LIMIT).sum()) for i in range(n)])
    R = {"valid_days": M}
    nv = vd.sum(1)
    R["pro_rata"] = M * D / nv

    def per(f):
        out = np.full(n, -1.0)
        for i in todo:
            out[i] = f(i)
        return out
    for meth in ("linear", "lower", "higher", "nearest"):
        R["p904_" + meth] = per(lambda i: np.percentile(dm[i][vd[i]], 90.4, method=meth))
    t = np.arange(D)
    hh = np.arange(H)
    R["interp_daily"] = per(lambda i: M[i] + int(((np.interp(t, t[vd[i]], dm[i][vd[i]]) > LIMIT) & ~vd[i]).sum()))
    R["interp_hourly"] = per(lambda i: whole_year(xv[i], valid[i], vd[i], dm[i], np.interp(hh, hh[valid[i]], xv[i][valid[i]]), True))
    # the network alone (daily)
    with np.errstate(all="ignore"):
        ldm = np.log(dm)
        a = np.zeros(n)
        b = np.nanmean(ldm, 0)
        for _ in range(60):
            a = np.nanmean(ldm - b[None, :], 1)
            b = np.nanmean(ldm - a[:, None], 0)
    R["net_twoway_daily"] = per(lambda i: M[i] + int(((np.exp(a[i] + b) > LIMIT) & ~vd[i]).sum()))
    pos = np.array([[s[4], s[5]] for s in P.STATIONS], float)

    def net_daily(i):
        o = [j for j in range(n) if j != i]
        with np.errstate(all="ignore"):
            md = np.nanmedian(dm[o], 0)
        ok = vd[i] & ~np.isnan(md)
        r_ = np.exp(np.mean(np.log(dm[i][ok]) - np.log(md[ok])))
        bb, aa = np.polyfit(md[ok], dm[i][ok], 1)
        dist = np.hypot(*(pos[o] - pos[i]).T)
        pred = np.full(D, np.nan)
        for j in np.array(o)[np.argsort(dist)]:
            okj = vd[i] & vd[j]
            rj = np.mean(dm[i][okj]) / np.mean(dm[j][okj])
            pred = np.where(np.isnan(pred) & vd[j], rj * dm[j], pred)
        return (M[i] + int(((r_ * md > LIMIT) & ~vd[i]).sum()), M[i] + int((((aa + bb * md) > LIMIT) & ~vd[i]).sum()),
                M[i] + int(((pred > LIMIT) & ~vd[i]).sum()))
    nd = {i: net_daily(i) for i in todo}
    for j, name in enumerate(("net_ratio_daily", "net_regression_daily", "net_nearest_daily")):
        R[name] = per(lambda i: nd[i][j])
    BG = backgrounds(xv, valid, todo)
    for bname, bg in BG.items():
        def net_hourly(i, bg=bg):
            inc = xv[i] - bg[i]
            off = np.nanmean(np.where(valid[i], inc, np.nan))
            return whole_year(xv[i], valid[i], vd[i], dm[i], bg[i] + off, True)
        R["net_hourly_" + bname] = per(net_hourly)
    # the count scaled by data capture month by month (a month with no valid day at the year's rate)
    mon = np.array([(P.START + dt.timedelta(days=int(d))).month for d in range(D)])

    def pro_month(i):
        tot = 0.0
        for m in range(1, 13):
            sel = mon == m
            nv_m = (vd[i] & sel).sum()
            tot += ((dm[i][vd[i] & sel] > LIMIT).sum() * sel.sum() / nv_m) if nv_m else M[i] * sel.sum() / nv[i]
        return tot
    R["pro_rata_month"] = per(pro_month)
    # short gaps interpolated in time, longer ones from the network median and the station's mean offset
    for L in (24, 72, 168):
        def hybrid(i, L=L):
            interp = np.interp(hh, hh[valid[i]], xv[i][valid[i]])
            net = BG["median"][i] + np.nanmean(np.where(valid[i], xv[i] - BG["median"][i], np.nan))
            pred = net.copy()
            run = np.flatnonzero(np.diff(np.concatenate([[1], valid[i].astype(int), [1]])))
            for a, b in zip(run[::2], run[1::2]):
                if b - a <= L:
                    pred[a:b] = interp[a:b]
            return whole_year(xv[i], valid[i], vd[i], dm[i], pred, True)
        R["interp_hybrid_%d" % L] = per(hybrid)
    if which == "rungs":
        return R
    # the network plus the station's own response to the wind
    th, sp, wh = W["theta"], W["speed"], W["wet_h"]
    for bname, bg in BG.items():
        for k in (4, 8, 12, 16, 36):
            for bands in (1, 2, 3):
                for wetsplit in (False, True):
                    cells = {i: wind_cells(xv[i] - bg[i], valid[i], th, sp, wh, k, bands, wetsplit) for i in todo}
                    for mix in (True, False):
                        name = "wind_cells_%s_%d_%d_%s_%s" % (bname, k, bands, "wet" if wetsplit else "all", "mix" if mix else "pred")
                        R[name] = per(lambda i: whole_year(xv[i], valid[i], vd[i], dm[i], bg[i] + cells[i], mix))
        for order in (2, 3, 4):
            for use_speed in (False, True):
                for wetsplit in (False, True):
                    name = "wind_harmonic_%s_%d_%s_%s" % (bname, order, "speed" if use_speed else "dir", "wet" if wetsplit else "all")
                    R[name] = per(lambda i: whole_year(xv[i], valid[i], vd[i], dm[i],
                                                       bg[i] + wind_harmonic(xv[i] - bg[i], valid[i], th, sp, wh, order, use_speed, wetsplit), True))
    return R


RUNG_KEYS = ("valid_days", "pro_rata", "p904", "interp", "net_")


def call(R):
    """the golden call: noted where the count over valid days is 35 or fewer and the whole-year count (the reference
    reading) is more than 35"""
    ref = R[REFERENCE]
    return [P.CODES[i] for i in range(len(P.CODES)) if R["valid_days"][i] <= ALLOWED and ref[i] > ALLOWED]


REFERENCE = "wind_cells_median_16_2_wet_mix"
