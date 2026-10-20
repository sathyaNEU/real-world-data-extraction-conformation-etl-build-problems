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


# The asks run over the ten months 1 November 2025 to 31 August 2026, which is not the call's window. Both
# ends sit inside the record: the opening read is the November round and the closing read the September one,
# so each part-window is recoverable from the ten-minute series, and no graded figure sits near a rounding
# edge (the closest is 99 kWh clear of one, against about 1 kWh of numerical noise).
ASK_FROM = dt.datetime(2025, 11, 1, tzinfo=W.LONDON)
ASK_TO = dt.datetime(2026, 9, 1, tzinfo=W.LONDON)
ASK_MONTHS = ["2025-11", "2025-12", "2026-01", "2026-02", "2026-03",
              "2026-04", "2026-05", "2026-06", "2026-07", "2026-08"]


def ask_window():
    """The interval bounds of the eleven months 1 October 2025 to 31 August 2026, site local time."""
    return (W.interval_index(ASK_FROM.astimezone(W.UTC)), W.interval_index(ASK_TO.astimezone(W.UTC)))


def asks_truth(ops):
    """The two ask quantities on the generator's truth.

    A, each turbine's metered generation over the eleven months: the energy its revenue counter would record
    had it been read exactly at the window's two ends, which is the integral of its exported power there. The
    counter is export only, so negative power contributes nothing.
    B, the farm's metered export in each of those months: the connection meter's export register summed by
    the month the half-hour falls in locally, after the transformer and cable loss and the site's own demand.
    """
    import records as R
    k_a, k_b = ask_window()
    A = {}
    for t in W.TURBINES:
        e = np.concatenate([[0.0], np.cumsum(np.maximum(ops["power"][t], 0.0)) / 6.0])
        A[t] = float((e[k_b] - e[k_a]) / 1000.0)
    Bm = {k: 0.0 for k in ASK_MONTHS}
    for j, r in enumerate(R.meter_rows(ops)):
        st = W.START + dt.timedelta(minutes=30 * j)
        key = st.astimezone(W.LONDON).strftime("%Y-%m")
        if key in Bm:
            Bm[key] += float(r[2])
    return A, {k: v / 1000.0 for k, v in Bm.items()}


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
    with open(os.path.join(target, R.COUNTERS)) as fh:
        cnt = list(csv.DictReader(fh))
    with open(os.path.join(target, R.METER)) as fh:
        mtr = list(csv.DictReader(fh))
    return dict(scada=tab, mast=mast, anm=anm, wos=wos, curve=curve, counters=cnt, meter=mtr)


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
    """The two ask quantities from the shipped files, in the golden handling and at each stop.

    Ask A, each turbine's metered generation over the eleven months to 31 August 2026. The counters are not
    read at the window's ends: a technician walks the pads on the monthly round and the round slips, so the
    registers span the round's own window and the two part-windows at each end come from the ten-minute
    record. Stops: `energysum` sums the monthly energy column, which is the round's window and nothing else;
    `utcfill` and `localfill` integrate the part-windows with the SCADA clock read one way throughout;
    `readsutc` takes the read stamps as UTC rather than site local.

    Ask B, the farm's metered export in each of those months. The connection meter is stamped in UTC and its
    export register is export only. Stops: `utcmonths` sums the register on the file's own settlement date,
    so the British Summer Time months carry the wrong boundary hour; `netexport` nets the import register
    off the export register, which is not what the farm was paid for exporting.
    """
    import pandas as pd
    import records as R
    k_a, k_b = ask_window()
    clock = {"localfill": "local", "utcfill": "utc"}.get(variant, "golden")

    # --- the ten-minute record as a per-turbine exported-power series on the UTC index
    sc = B["scada"]
    P = {}
    for t in W.TURBINES:
        x = sc[sc.turbine == t]
        k = scada_k(x.timestamp.reset_index(drop=True), clock)
        ok = (k >= 0) & (k < W.N)
        p = np.zeros(W.N)
        p[k[ok]] = np.maximum(x.active_power_mean.to_numpy()[ok], 0.0)
        P[t] = np.concatenate([[0.0], np.cumsum(p) / 6.0])

    # --- ask A
    rows = B["counters"]
    tz = "UTC" if variant == "readsutc" else "Europe/London"
    A = {}
    for t in W.TURBINES:
        mine = [r for r in rows if r["turbine"] == t]
        by = {r["month"]: r for r in mine}
        first, last = by[ASK_MONTHS[0]], by[ASK_MONTHS[-1]]
        span = int(last["meter_end_kwh"]) - int(first["meter_start_kwh"])
        if variant == "energysum":
            A[t] = float(sum(int(by[m]["energy_kwh"]) for m in ASK_MONTHS) / 1000.0)
            continue
        r0 = int(round((pd.Timestamp(first["read_from_local"]).tz_localize(tz, ambiguous=True,
                                                                          nonexistent="shift_forward")
                        - pd.Timestamp(W.START)) / pd.Timedelta(minutes=10)))
        r1 = int(round((pd.Timestamp(last["read_to_local"]).tz_localize(tz, ambiguous=True,
                                                                       nonexistent="shift_forward")
                        - pd.Timestamp(W.START)) / pd.Timedelta(minutes=10)))
        r0, r1 = min(max(r0, 0), W.N), min(max(r1, 0), W.N)
        # The registers span [r0, r1]; the board asks about [k_a, k_b]. Each read sits inside the record,
        # so both part-windows come from the ten-minute series: the energy between the window's start and
        # the opening read belongs to the answer and is not in the registers, and the energy between the
        # window's end and the closing read is in the registers and does not belong to the answer.
        head = (P[t][max(r0, k_a)] - P[t][min(r0, k_a)]) / 1000.0
        tail = (P[t][max(r1, k_b)] - P[t][min(r1, k_b)]) / 1000.0
        head = head if r0 >= k_a else -head
        tail = tail if r1 >= k_b else -tail
        A[t] = float(span / 1000.0 + head - tail)

    # --- ask B
    Bm = {k: 0.0 for k in ASK_MONTHS}
    for r in B["meter"]:
        st = dt.datetime.strptime(r["settlement_date_utc"] + " " + r["period_start_utc"],
                                  "%Y-%m-%d %H:%M").replace(tzinfo=W.UTC)
        key = (st.strftime("%Y-%m") if variant == "utcmonths"
               else st.astimezone(W.LONDON).strftime("%Y-%m"))
        if key not in Bm:
            continue
        v = float(r["export_kwh"])
        if variant == "netexport":
            v -= float(r["import_kwh"])
        Bm[key] += v
    return A, {k: v / 1000.0 for k, v in Bm.items()}
