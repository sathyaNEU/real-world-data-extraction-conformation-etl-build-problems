"""The analyses: the call's ladder and the asks, on arrays indexed by turbine and UTC interval.

`frame()` turns either the generator's clean truth or a bundle read back from target/ into the same arrays, so every
rung runs on both. The main call works on normal-operation intervals (OM-07 3.1); the asks on OM-07 section 4."""
import datetime as dt

import numpy as np

import wind as WD
import world as W

EDGES = np.arange(-0.25, 30.0, 0.5)
CENT = EDGES[:-1] + 0.25
NORMAL = (10, 20)


def curve_at(curve, v):
    """Warranted power at wind v (OM-07 4.6): linear between listed speeds, zero below 3.0 and above 25.0 m/s."""
    speeds, kw = np.asarray(curve[0], float), np.asarray(curve[1], float)
    out = np.interp(v, speeds, kw)
    return np.where((v < speeds[0]) | (v > speeds[-1]), 0.0, out)


def curve_bins(curve):
    """The warranted power at each 0.5 m/s bin centre (zero outside 3.0 to 25.0)."""
    return curve_at(curve, CENT)


def density(temp_c, pres_hpa):
    return pres_hpa * 100.0 / (287.05 * (temp_c + 273.15))


# ------------------------------------------------------------------ the main call

def blade_set_mask(k, turbine):
    """OM-07 2.5: CH09 from its present rotor's return to service."""
    if turbine == "CH09":
        return k >= W.interval_index(W.CH09_BACK)
    return np.ones(len(k), bool)


def bins_short(veff, p, curve):
    """Method of bins: hours in each 0.5 m/s bin x (warranted at the bin centre less the bin's mean power), MWh."""
    i = np.clip(np.digitize(veff, EDGES) - 1, 0, len(CENT) - 1)
    pm = np.bincount(i, weights=p, minlength=len(CENT))
    n = np.bincount(i, minlength=len(CENT))
    return float((curve_bins(W_CURVE[0]) * n - pm).sum() / 6000.0)


W_CURVE = [None]


def set_curve(curve):
    W_CURVE[0] = curve


def default_shortfall(F, whole_year=False, lo=None, hi=None):
    """R0 (and R0' with whole_year): each turbine's energy shortfall against the warranted curve by the method of
    bins over its normal-operation intervals, density-corrected nacelle wind; lo/hi restrict the bins (R1)."""
    out = {}
    wc = curve_bins(W_CURVE[0])
    for t in W.TURBINES:
        x = F[t]
        m = x["normal"] & (whole_year | blade_set_mask(x["k"], t))
        i = np.clip(np.digitize(x["veff"][m], EDGES) - 1, 0, len(CENT) - 1)
        pm = np.bincount(i, weights=x["p"][m], minlength=len(CENT))
        n = np.bincount(i, minlength=len(CENT))
        sel = np.ones(len(CENT), bool)
        if lo is not None:
            sel = (CENT >= lo) & (CENT <= hi)
        out[t] = float(((wc * n - pm) / 6000.0)[sel].sum())
    return out


def interp_shortfall(F):
    """R0 by per-record interpolation of the warranted curve."""
    out = {}
    for t in W.TURBINES:
        x = F[t]
        m = x["normal"] & blade_set_mask(x["k"], t)
        out[t] = float((curve_at(W_CURVE[0], x["veff"][m]) - x["p"][m]).sum() / 6000.0)
    return out


def zero_ti_fit(curve, ti_ref):
    """Annex M: the zero-turbulence curve (rated power, cut-in, Cp max) whose Gaussian average at the reference
    turbulence (by bin centre) best matches the warranted curve between 4 and 12 m/s."""
    speeds, kw = np.asarray(curve[0], float), np.asarray(curve[1], float)
    sel = (speeds >= 4.0) & (speeds <= 12.0)
    best = None
    for cp in np.arange(0.440, 0.500, 0.001):
        for vci in (2.5, 2.75, 3.0, 3.25, 3.5):
            sim = annex_m_power(speeds[sel], ti_ref(speeds[sel]), cp, vci)
            err = float(((sim - kw[sel]) ** 2).sum())
            if best is None or err < best[0]:
                best = (err, cp, vci)
    return best[1], best[2]


def annex_m_power(v, ti, cp, vci):
    v = np.asarray(v, float)
    ti = np.asarray(ti, float)
    out = np.empty(v.shape)
    step = 200000
    vf, tf, of = v.reshape(-1), np.broadcast_to(ti, v.shape).reshape(-1), out.reshape(-1)
    for a in range(0, vf.size, step):
        vv = np.maximum(vf[a:a + step, None] * (1.0 + tf[a:a + step, None] * WD.U), 0.0)
        p = 0.5 * 1.225 * WD.AREA * cp * vv ** 3 / 1000.0
        p = np.where(vv < vci, 0.0, np.minimum(p, W.RATED_KW))
        of[a:a + step] = (p * WD.WQ).sum(-1)
    return out


def matched_annex_m(F, ti_ref=None, whole_year=False):
    """R2 by Annex M: each record's expected as-new power at its own turbulence from the zero-turbulence curve fitted
    to the warranted curve at the reference turbulence (default: the mast's median turbulence by bin)."""
    ti_ref = ti_ref or F["_ti_ref"]
    cp, vci = zero_ti_fit(W_CURVE[0], ti_ref)
    out = {}
    for t in W.TURBINES:
        x = F[t]
        m = x["normal"] & (whole_year | blade_set_mask(x["k"], t))
        exp = annex_m_power(x["veff"][m], x["ti"][m], cp, vci)
        out[t] = float((exp - x["p"][m]).sum() / 6000.0)
    return out, (cp, vci)


def matched_bins(F, dv=0.5, dti=0.02, minn=20, ref="median", exclude=()):
    """R2 by turbulence bins: each record against the fleet's mean (or median of turbine means) power in the same
    wind-speed and turbulence bin, records in cells with too few fleet records scaled out."""
    vb = lambda v: np.floor((v + dv / 2) / dv).astype(int)
    tb = lambda ti: np.floor(ti / dti).astype(int)
    cells = {}
    for t in W.TURBINES:
        x = F[t]
        m = x["normal"] & blade_set_mask(x["k"], t)
        key = vb(x["veff"][m]) * 1000 + tb(x["ti"][m])
        u, inv = np.unique(key, return_inverse=True)
        s = np.bincount(inv, weights=x["p"][m])
        c = np.bincount(inv)
        cells[t] = (dict(zip(u.tolist(), range(len(u)))), s, c, key, m)
    out = {}
    for t in W.TURBINES:
        idx, s, c, key, m = cells[t]
        others = [o for o in W.TURBINES if o != t and o not in exclude]
        ref_mean = np.full(len(key), np.nan)
        ref_n = np.zeros(len(key))
        per = []
        for o in others:
            oi, os_, oc, _, _ = cells[o]
            pos = np.array([oi.get(kk, -1) for kk in key.tolist()])
            have = pos >= 0
            mean_o = np.where(have, os_[np.maximum(pos, 0)] / np.maximum(oc[np.maximum(pos, 0)], 1), np.nan)
            n_o = np.where(have, oc[np.maximum(pos, 0)], 0)
            per.append((mean_o, n_o))
        means = np.vstack([a for a, _ in per])
        ns = np.vstack([b for _, b in per])
        ref_n = ns.sum(0)
        if ref == "median":
            ref_mean = np.nanmedian(np.where(ns >= 3, means, np.nan), axis=0)
        else:
            ref_mean = np.nansum(means * ns, axis=0) / np.maximum(ref_n, 1)
        ok = (ref_n >= minn) & np.isfinite(ref_mean)
        p = F[t]["p"][m]
        out[t] = float(((ref_mean - p)[ok]).sum() / 6000.0 / max(ok.mean(), 1e-9))
    return out


def matched_band(F, band=0.25):
    """R2 by a turbulence band: each turbine's records whose turbulence is within the band of the mast's median at
    that wind (the type test's), binned against the warranted curve, scaled by the turbine's own year of bins."""
    ref = F["_ti_ref"]
    wc = curve_bins(W_CURVE[0])
    out = {}
    for t in W.TURBINES:
        x = F[t]
        m = x["normal"] & blade_set_mask(x["k"], t)
        mm = m & (np.abs(x["ti"] / ref(x["veff"]) - 1) < band)
        i = np.clip(np.digitize(x["veff"][mm], EDGES) - 1, 0, len(CENT) - 1)
        pc = np.bincount(i, weights=x["p"][mm], minlength=len(CENT)) / np.maximum(np.bincount(i, minlength=len(CENT)), 1)
        have = np.bincount(i, minlength=len(CENT)) >= 5
        ia = np.clip(np.digitize(x["veff"][m], EDGES) - 1, 0, len(CENT) - 1)
        na = np.bincount(ia, minlength=len(CENT))
        out[t] = float((na * np.where(have, wc - pc, 0)).sum() / 6000.0)
    return out


def mast_wind_shortfall(F):
    """R1b: the turbine's power against the warranted curve at the mast's density-corrected wind."""
    out = {}
    wc = curve_bins(W_CURVE[0])
    for t in W.TURBINES:
        x = F[t]
        m = x["normal"] & blade_set_mask(x["k"], t) & (F["_mast_veff"][x["k"]] < 20)
        i = np.clip(np.digitize(F["_mast_veff"][x["k"]][m], EDGES) - 1, 0, len(CENT) - 1)
        pm = np.bincount(i, weights=x["p"][m], minlength=len(CENT))
        n = np.bincount(i, minlength=len(CENT))
        out[t] = float((wc * n - pm).sum() / 6000.0)
    return out


def sector_free(t):
    """IEC 61400-12-1 Annex A: the directions disturbed by neighbouring turbines within 10 rotor diameters."""
    out = []
    for o in W.TURBINES:
        if o == t:
            continue
        L = np.hypot(W.XY[o][0] - W.XY[t][0], W.XY[o][1] - W.XY[t][1])
        if L / W.ROTOR_D > 10:
            continue
        a = 1.3 * np.degrees(np.arctan(2.5 * W.ROTOR_D / L + 0.15)) + 10
        out.append((WD.bearing(W.XY[t], W.XY[o]), a))
    return out


def wake_excluded_shortfall(F):
    """R1b: the method of bins on each turbine's undisturbed directions only, scaled by its year of bins."""
    wc = curve_bins(W_CURVE[0])
    out = {}
    for t in W.TURBINES:
        x = F[t]
        m = x["normal"] & blade_set_mask(x["k"], t)
        free = np.ones(len(x["k"]), bool)
        for b, a in sector_free(t):
            free &= np.abs(WD.angdiff(x["ndir"], b)) > a / 2
        mm = m & free
        i = np.clip(np.digitize(x["veff"][mm], EDGES) - 1, 0, len(CENT) - 1)
        pc = np.bincount(i, weights=x["p"][mm], minlength=len(CENT)) / np.maximum(np.bincount(i, minlength=len(CENT)), 1)
        have = np.bincount(i, minlength=len(CENT)) >= 5
        ia = np.clip(np.digitize(x["veff"][m], EDGES) - 1, 0, len(CENT) - 1)
        na = np.bincount(ia, minlength=len(CENT))
        out[t] = float((na * np.where(have, wc - pc, 0)).sum() / 6000.0)
    return out


def mast_ti_annex_m(F):
    """R1b: Annex M normalisation with the mast's turbulence in place of each turbine's own."""
    cp, vci = zero_ti_fit(W_CURVE[0], F["_ti_ref"])
    out = {}
    for t in W.TURBINES:
        x = F[t]
        m = x["normal"] & blade_set_mask(x["k"], t)
        exp = annex_m_power(x["veff"][m], F["_mast_ti"][x["k"]][m], cp, vci)
        out[t] = float((exp - x["p"][m]).sum() / 6000.0)
    return out


def pick(d):
    return max(d, key=lambda t: d[t])


def ranked(d):
    return sorted(d, key=lambda t: -d[t])


# ------------------------------------------------------------------ the asks

def lost(potential, p):
    return np.maximum(potential - p, 0.0) / 6000.0


def asks_truth(G):
    """D and G by OM-07 section 4 on the generator's truth: G holds per turbine the true downtime and ANM masks, the
    power (zero while silent and stopped) and the mast potential."""
    D, C = {}, {}
    for t in W.TURBINES:
        x = G[t]
        lp = lost(G["_potential"], x["p"])
        D[t] = float(lp[x["down"]].sum())
        C[t] = float(lp[x["curt"]].sum())
    return D, C


# ------------------------------------------------------------------ frames

def ti_ref_from_mast(veff, ti):
    """The mast's median turbulence by 0.5 m/s bin, as a function of wind (the warranted curve's reference)."""
    i = np.clip(np.digitize(veff, EDGES) - 1, 0, len(CENT) - 1)
    med = np.array([np.median(ti[i == b]) if (i == b).sum() >= 30 else np.nan for b in range(len(CENT))])
    good = np.isfinite(med)
    xs, ys = CENT[good], med[good]
    return lambda v: np.interp(v, xs, ys)


def frame_truth(m, T, ops, rounded=True):
    """The clean truth as analysis arrays: every interval of every turbine (silent ones included), at the precision
    the bundle stores (rounded=True) or exact."""
    r = (lambda a, d: np.round(a, d)) if rounded else (lambda a, d: a)
    temp, pres = r(m["temp"], 2), r(m["pres"], 1)
    rho = density(temp, pres)
    mv = r(m["v"], 2)
    F = {}
    k = np.arange(W.N)
    for t in W.TURBINES:
        v, sd = r(T[t]["v"], 2), r(T[t]["sd"], 2)
        F[t] = dict(k=k, veff=v * (rho / 1.225) ** (1.0 / 3.0), ti=sd / np.maximum(v, 0.5), p=r(ops["power"][t], 1),
                    state=ops["state"][t], normal=np.isin(ops["state"][t], NORMAL), ndir=r(T[t]["ndir"], 1))
    F["_mast_veff"] = mv * (rho / 1.225) ** (1.0 / 3.0)
    F["_mast_ti"] = r(m["sd"], 2) / np.maximum(mv, 0.5)
    F["_ti_ref"] = ti_ref_from_mast(F["_mast_veff"], F["_mast_ti"])
    return F


def asks_frame(m, T, ops, curve):
    """The truth for the asks: OM-07 4.4's classes per turbine and interval, the power with nothing made while a
    turbine was silent and stopped, and the potential from the mast at the bundle's precision."""
    temp, pres, mv = np.round(m["temp"], 2), np.round(m["pres"], 1), np.round(m["v"], 2)
    pot = curve_at(curve, mv * (density(temp, pres) / 1.225) ** (1.0 / 3.0))
    G = {"_potential": pot}
    has = ~np.isnan(ops["limit"])
    for t in W.TURBINES:
        st = ops["state"][t]
        down = ops["down"][t]
        neither = np.isin(st, (21, 22, 61)) & ~down
        curt = has & ~down & ~neither
        G[t] = dict(p=np.round(ops["power"][t], 1), down=down, curt=curt)
    return G


# ------------------------------------------------------------------ the bundle read back

def read_bundle(target):
    """The shipped files as the analyses need them (the golden handling of every clock)."""
    import csv
    import os
    import pyarrow.parquet as pq
    import records as R
    import docs as D
    tab = pq.read_table(os.path.join(target, R.SCADA)).to_pandas()
    mast = np.genfromtxt(os.path.join(target, R.MAST), delimiter=",", skip_header=1, usecols=(1, 2, 3, 4, 5, 6))
    with open(os.path.join(target, R.ANM)) as fh:
        anm = list(csv.DictReader(fh))
    with open(os.path.join(target, R.WORKORDERS)) as fh:
        wos = list(csv.DictReader(fh))
    curve = read_curve(os.path.join(target, D.SCHEDULE))
    return dict(scada=tab, mast=mast, anm=anm, wos=wos, curve=curve)


def read_curve(path):
    import pdfplumber
    import re
    with pdfplumber.open(path) as pdf:
        text = "\n".join(p.extract_text() for p in pdf.pages)
    pts = []
    for line in text.splitlines():
        nums = re.findall(r"(\d+\.\d) (\d+) (0\.\d{3})", line)
        for v, p, _ in nums:
            pts.append((float(v), float(p)))
    pts.sort()
    return np.array([a for a, _ in pts]), np.array([b for _, b in pts])


def scada_k(stamps, clock="golden"):
    """The UTC interval index of each SCADA row from its end stamp. golden: UK local time up to the platform change
    on 3 February 2026 10:00, UTC after; a repeated local stamp is the later (GMT) interval the second time it
    appears for a turbine. local: local time throughout. utc: UTC throughout."""
    import pandas as pd
    s = pd.Series(stamps)
    naive = s.dt.tz_localize(None) if getattr(s.dt, "tz", None) is not None else s
    cut = pd.Timestamp(W.MIGRATION.replace(tzinfo=None))
    if clock == "utc":
        utc = naive
    else:
        loc = naive if clock == "local" else naive.where(naive <= cut)
        dup = loc.duplicated(keep="first") & loc.notna()
        first = loc.dt.tz_localize("Europe/London", ambiguous=np.ones(len(loc), bool), nonexistent="shift_forward")
        second = loc.dt.tz_localize("Europe/London", ambiguous=np.zeros(len(loc), bool), nonexistent="shift_forward")
        conv = first.where(~dup, second).dt.tz_convert("UTC").dt.tz_localize(None)
        utc = conv if clock == "local" else conv.where(naive <= cut, naive)
    start = pd.Timestamp(W.START.replace(tzinfo=None))
    return ((utc - start) / pd.Timedelta(minutes=10)).round().astype(int).to_numpy() - 1


def frame_bundle(B, clock="golden"):
    sc = B["scada"]
    mast = B["mast"]
    rho = density(mast[:, 3], mast[:, 4])
    F = {}
    for t in W.TURBINES:
        x = sc[sc.turbine == t]
        k = scada_k(x.timestamp.reset_index(drop=True), clock)
        ok = (k >= 0) & (k < W.N)
        k = k[ok]
        v = x.wind_speed_mean.to_numpy()[ok]
        st = x.state.to_numpy()[ok]
        F[t] = dict(k=k, veff=v * (rho[k] / 1.225) ** (1.0 / 3.0), ti=x.wind_speed_sd.to_numpy()[ok] / np.maximum(v, 0.5),
                    p=x.active_power_mean.to_numpy()[ok], state=st, normal=np.isin(st, NORMAL),
                    ndir=x.nacelle_position.to_numpy()[ok])
    mv = mast[:, 0]
    F["_mast_veff"] = mv * (rho / 1.225) ** (1.0 / 3.0)
    F["_mast_ti"] = mast[:, 1] / np.maximum(mv, 0.5)
    F["_ti_ref"] = ti_ref_from_mast(F["_mast_veff"], F["_mast_ti"])
    return F


def _wo_time(day, s):
    if not s:
        return None
    if len(s) > 5:
        d = dt.date.fromisoformat(s[:10])
        hh, mm = s[11:].split(":")
    else:
        d = day
        hh, mm = s.split(":")
    return dt.datetime(d.year, d.month, d.day, int(hh), int(mm), tzinfo=W.LONDON).astimezone(W.UTC)


def wo_windows(wos):
    """Each work order's stopped intervals per turbine: (from, to) UTC, from the isolation columns of a service and
    from turbine_stopped to returned_to_service for corrective and major-component orders."""
    out = {t: [] for t in W.TURBINES}
    for r in wos:
        day = dt.date.fromisoformat(r["date"])
        if r["type"] == "Annual service":
            a, b = _wo_time(day, r["isolated_from"]), _wo_time(day, r["isolated_to"])
        else:
            a, b = _wo_time(day, r["turbine_stopped"]), _wo_time(day, r["returned_to_service"])
        if a and b:
            out[r["turbine"]].append((a, b))
    return out


def asks_bundle(B, variant="golden"):
    """D and G by OM-07 section 4 from the shipped files.

    golden: the clock as scada_k's golden; silent intervals are downtime inside a work order's stopped window, and
    nothing otherwise (the communications outage and the grid loss). Stops: states (silent intervals dropped),
    ffill/bfill (silent intervals take the neighbouring row's state), allsilent (every silent interval downtime),
    state11 (curtailment read from the power-limited state), local and utc (the SCADA's clock read one way)."""
    clock = variant if variant in ("local", "utc") else "golden"
    mast = B["mast"]
    pot = curve_at(B["curve"], mast[:, 0] * (density(mast[:, 3], mast[:, 4]) / 1.225) ** (1.0 / 3.0))
    inforce = np.zeros(W.N, bool)
    import pandas as pd
    start = pd.Timestamp(W.START.replace(tzinfo=None))
    for r in B["anm"]:
        a = int(round((pd.Timestamp(r["start_utc"][:19]) - start) / pd.Timedelta(minutes=10)))
        b = int(round((pd.Timestamp(r["end_utc"][:19]) - start) / pd.Timedelta(minutes=10)))
        inforce[max(a, 0):min(b, W.N)] = True
    win = wo_windows(B["wos"])
    sc = B["scada"]
    D, C = {}, {}
    for t in W.TURBINES:
        x = sc[sc.turbine == t]
        k = scada_k(x.timestamp.reset_index(drop=True), clock)
        ok = (k >= 0) & (k < W.N)
        st = np.full(W.N, -1)
        p = np.zeros(W.N)
        st[k[ok]] = x.state.to_numpy()[ok]
        p[k[ok]] = x.active_power_mean.to_numpy()[ok]
        silent = st < 0
        down = np.isin(st, (30, 40, 41))
        if variant in ("golden", "local", "utc", "state11"):
            for a, b in win[t]:
                ka = int(round((a - W.START).total_seconds() / 600))
                kb = int(round((b - W.START).total_seconds() / 600))
                sel = np.zeros(W.N, bool)
                sel[max(ka, 0):min(kb, W.N)] = True
                down |= sel & silent
        elif variant in ("ffill", "bfill"):
            idx = np.where(~silent, np.arange(W.N), -1 if variant == "ffill" else W.N)
            if variant == "ffill":
                idx = np.maximum.accumulate(idx)
                fill = np.where(idx >= 0, st[np.maximum(idx, 0)], 10)
            else:
                idx = np.minimum.accumulate(idx[::-1])[::-1]
                fill = np.where(idx < W.N, st[np.minimum(idx, W.N - 1)], 10)
            down = np.isin(np.where(silent, fill, st), (30, 40, 41))
        elif variant == "allsilent":
            down = down | silent
        neither = np.isin(st, (21, 22, 61))
        if variant in ("golden", "local", "utc", "state11", "ffill", "bfill", "allsilent", "states"):
            # silent intervals of the grid loss are neither (the grid state brackets them)
            gl = silent & (np.arange(W.N) >= W.interval_index(W.GRID_LOSS[0])) & (np.arange(W.N) < W.interval_index(W.GRID_LOSS[1]))
            neither = neither | (gl if variant != "allsilent" else np.zeros(W.N, bool))
        lp = np.maximum(pot - p, 0.0) / 6000.0
        D[t] = float(lp[down].sum())
        if variant == "state11":
            C[t] = float(lp[np.isin(st, (11,))].sum())
        else:
            C[t] = float(lp[inforce & ~down & ~neither].sum())
    return D, C
