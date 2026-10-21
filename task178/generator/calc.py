"""task178 calculations from the shipped pack only: the golden deck elevation and its figures, the default path
and every rival route, and the two asks. deliver.py, checks.py and cracker.py call it; verify.py has its own code."""
from __future__ import annotations

import datetime as dt
import os
import re
import subprocess
from functools import lru_cache

import numpy as np
import openpyxl
import pandas as pd

import common as C

EPOCH_MSL_FT = None      # read from the datum sheet


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout


# ---------------------------------------------------------------------------------------------------- loaders
@lru_cache(None)
def datums(target):
    txt = pdf_text(os.path.join(target, C.F_DATUMS))
    out = {}
    for k in ("MHHW", "MHW", "MSL", "MLW", "MLLW", "NAVD88"):
        m = re.search(r"^\s*%s\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)" % k, txt, re.M)
        out[k] = float(m.group(2))
    out["STND1995"] = float(re.search(r"STND \(1995\) is (\d+\.\d+) ft below MLLW", txt).group(1))
    out["STND2026"] = float(re.search(r"STND 2026 is (\d+\.\d+) ft below MLLW", txt).group(1))
    out["BOARD"] = float(re.search(r"which is (\d+\.\d+) ft\s+below\s+MLLW", txt).group(1))
    return out


@lru_cache(None)
def guidance(target):
    txt = pdf_text(os.path.join(target, C.F_SLR))
    annual = {}
    for m in re.finditer(r"^\s*(\d{4})\s+(\d\.\d\d)(?:\s+(\d{4})\s+(\d\.\d\d))?\s*$", txt, re.M):
        annual[int(m.group(1))] = float(m.group(2))
        if m.group(3):
            annual[int(m.group(3))] = float(m.group(4))
    design = float(re.search(r"mean sea level of (\d+\.\d+) ft MLLW", txt).group(1))
    return annual, design


@lru_cache(None)
def verified(target):
    df = pd.read_csv(os.path.join(target, C.F_VER), comment="#", dtype={"quality": str})
    t = pd.to_datetime(df["timestamp_utc"]).values.astype("datetime64[m]")
    return t, df["water_level_ft"].to_numpy(float), df["quality"].to_numpy(str)


@lru_cache(None)
def telemetry(target):
    df = pd.read_csv(os.path.join(target, C.F_TEL))
    t = pd.to_datetime(df["time_utc"].str.replace("Z", "")).values.astype("datetime64[m]")
    return t, df["wl_m"].to_numpy(float)


def local_to_utc_np(loc):
    """naive local datetimes (list of datetime) to UTC datetime64[m] under each year's DST rule"""
    return np.array([np.datetime64(C.local_to_utc(x), "m") for x in loc])


@lru_cache(None)
def tide_tables(target):
    """every published high and low water: UTC datetime64, height ft MLLW, kind, local date"""
    wb = openpyxl.load_workbook(os.path.join(target, C.F_TABLES), read_only=True)
    T, H, K, LD = [], [], [], []
    for ws in wb.worksheets:
        y = int(ws.title)
        rows = list(ws.iter_rows(values_only=True))
        hdr = next(i for i, r in enumerate(rows) if r and r[0] == "Date")
        for r in rows[hdr + 1:]:
            if not r or r[0] is None:
                continue
            d = r[0].date() if isinstance(r[0], dt.datetime) else r[0]
            if y <= 2006:
                hh, mm = int(r[2][:2]), int(r[2][2:])
                std = dt.datetime(d.year, d.month, d.day, hh, mm)
                u = std + dt.timedelta(hours=5)
                loc_d, _ = C.to_local(u)
                kind, h = r[4], float(r[3])
                ld = loc_d.date()
            elif y <= 2018:
                tm = dt.datetime.strptime(r[2], "%I:%M %p")
                loc = dt.datetime(d.year, d.month, d.day, tm.hour, tm.minute)
                u = C.local_to_utc(loc)
                kind, h, ld = ("H" if r[1] == "High" else "L"), float(r[3]), d
            else:
                hh, mm = map(int, r[2].split(":"))
                loc = dt.datetime(d.year, d.month, d.day, hh, mm)
                u = C.local_to_utc(loc)
                kind, h, ld = r[4], float(r[3]), d
            T.append(np.datetime64(u, "m")); H.append(h); K.append(kind); LD.append(ld)
    T = np.array(T); H = np.array(H); K = np.array(K); LD = np.array(LD)
    o = np.argsort(T)
    return T[o], H[o], K[o], LD[o]


@lru_cache(None)
def observed_series(target, telemetry_datum="2026", prefer="verified", bracket=True):
    """one level series in ft MLLW: verified (V readings only, the readings between the bracket's re-securing and the
    sensor reset raised by the 0.08 ft the March 2018 levelling found) then telemetry after the verified product ends"""
    dat = datums(target)
    t, v, q = verified(target)
    ok = (q == "V") & np.isfinite(v)
    tv, lv = t[ok], v[ok] - dat["STND1995"]
    if bracket:
        a = np.datetime64(C.BRACKET_FAIL, "m"); b = np.datetime64(C.BRACKET_RESET, "m")
        lv = np.where((tv >= a) & (tv < b), lv + 0.08, lv)
    tt, wm = telemetry(target)
    off = dat["STND2026"] if telemetry_datum == "2026" else dat["STND1995"]
    lt = wm / C.FT - off
    end = t[-1]
    if prefer == "verified":
        m = tt > end
    else:
        m = np.ones(len(tt), bool)
        keep = tv < tt[0]
        tv, lv = tv[keep], lv[keep]
    return np.concatenate([tv, tt[m]]), np.concatenate([lv, lt[m]])


def tide_maxima(times, levels, hw_times, half_h=3.0):
    """highest reading within +-half_h hours of each predicted high water (nan if none)"""
    tm = times.astype("datetime64[m]").astype(np.int64)
    hw = hw_times.astype("datetime64[m]").astype(np.int64)
    w = int(half_h * 60)
    lo = np.searchsorted(tm, hw - w, side="left")
    hi = np.searchsorted(tm, hw + w, side="right")
    out = np.full(len(hw), np.nan)
    for i, (a, b) in enumerate(zip(lo, hi)):
        if b > a:
            out[i] = levels[a:b].max()
    return out


# ---------------------------------------------------------------------------------------------- the main call
def _hw(target):
    T, H, K, LD = tide_tables(target)
    m = K == "H"
    return T[m], H[m], LD[m]


def season_mask(ld, months=(4, 5), y0=1995, y1=2026):
    return np.array([(d.month in months) and (y0 <= d.year <= y1) for d in ld])


def forward_mask(ld):
    return np.array([C.WORK_START <= d <= C.WORK_END for d in ld])


@lru_cache(None)
def skew_surges(target, months=(4, 5), detrend="annual", telemetry_datum="2026", prefer="verified", y0=1995):
    """observed high water minus predicted high water for the season's tides, moved off each year's sea level"""
    dat = datums(target)
    annual, design = guidance(target)
    T, H, LD = _hw(target)
    ts, ls = observed_series(target, telemetry_datum, prefer)
    sel = season_mask(LD, months, y0)
    om = tide_maxima(ts, ls, T[sel])
    ss = om - H[sel]
    yrs = np.array([d.year for d in LD[sel]])
    ys = np.array(sorted(annual)); b, a = np.polyfit(ys + 0.5, [annual[y] for y in ys], 1)
    if detrend == "annual":
        off = np.array([annual.get(y, a + b * (y + 0.5)) for y in yrs]) - dat["MSL"]
    elif detrend == "trend":
        off = (a + b * (yrs + 0.5)) - dat["MSL"]
    else:
        off = np.zeros(len(yrs))
    s = ss - off
    return s[np.isfinite(s)]


def expected(target, settings=C.DECK_SETTINGS, surges=None, msl=None, tail=None):
    dat = datums(target)
    annual, design = guidance(target)
    T, H, LD = _hw(target)
    hf = H[forward_mask(LD)]
    s = np.sort(surges if surges is not None else skew_surges(target))
    n = len(s)
    z = (design if msl is None else msl) - dat["MSL"]
    out = []
    for L in settings:
        need = L - hf - z
        if tail is None:
            out.append(float(np.sum(n - np.searchsorted(s, need, side="left")) / n))
        else:
            out.append(float(np.sum(tail(need))))
    return np.array(out)


def pick(E, settings=C.DECK_SETTINGS, bar=C.DECK_BAR):
    for L, e in zip(settings, E):
        if e <= bar:
            return L
    return None


def golden(target):
    E = expected(target)
    p = pick(E)
    k = C.DECK_SETTINGS.index(p)
    return dict(E=E, pick=p, e_pick=float(E[k]), e_below=float(E[k - 1]), below=C.DECK_SETTINGS[k - 1])


def golden_family(target):
    """every construction of the window's expected tides the data leave open"""
    fam = {}
    fam["annual detrend, 1995-2026"] = expected(target)
    fam["trend detrend"] = expected(target, surges=skew_surges(target, detrend="trend"))
    fam["recent 20 years"] = expected(target, surges=skew_surges(target, y0=2007))
    fam["telemetry for May-June 2026"] = expected(target, surges=skew_surges(target, prefer="telemetry"))
    # per month
    dat = datums(target); annual, design = guidance(target)
    T, H, LD = _hw(target)
    fw = forward_mask(LD)
    tot = np.zeros(len(C.DECK_SETTINGS))
    for mth in (4, 5):
        s = np.sort(skew_surges(target, months=(mth,)))
        n = len(s)
        hf = H[fw & np.array([d.month == mth for d in LD])]
        tot += np.array([np.sum(n - np.searchsorted(s, L - hf - (design - dat["MSL"]), side="left")) / n
                         for L in C.DECK_SETTINGS])
    fam["per month"] = tot
    # generalized Pareto tail above the 95th percentile
    from scipy import stats
    s = np.sort(skew_surges(target)); u = np.percentile(s, 95); exc = s[s > u] - u
    xi, _, sc = stats.genpareto.fit(exc, floc=0)
    n = len(s)

    def sf(x):
        x = np.asarray(x, float)
        emp = (n - np.searchsorted(s, x, side="left")) / n
        return np.where(x > u, 0.05 * stats.genpareto.sf(x - u, xi, 0, sc), emp)
    fam["GPD tail"] = expected(target, tail=sf)
    fam["15 March to 15 June season"] = expected(target, surges=skew_surges_window(target))
    return fam


def skew_surges_window(target):
    dat = datums(target); annual, design = guidance(target)
    T, H, LD = _hw(target)
    sel = np.array([(1995 <= d.year <= 2026) and ((d.month, d.day) >= (3, 15)) and ((d.month, d.day) <= (6, 15)) for d in LD])
    ts, ls = observed_series(target)
    om = tide_maxima(ts, ls, T[sel])
    yrs = np.array([d.year for d in LD[sel]])
    ys = np.array(sorted(annual)); b, a = np.polyfit(ys + 0.5, [annual[y] for y in ys], 1)
    s = om - H[sel] - (np.array([annual.get(y, a + b * (y + 0.5)) for y in yrs]) - dat["MSL"])
    return s[np.isfinite(s)]


def rivals(target):
    """the routes that do not read the window's own tides, and the tide-aware routes with a lesser error"""
    import statsmodels.api as sm
    from scipy import stats
    dat = datums(target); annual, design = guidance(target)
    T, H, LD = _hw(target)
    ts, ls = observed_series(target)
    sel = season_mask(LD)
    om = tide_maxima(ts, ls, T[sel])
    yrs = np.array([d.year for d in LD[sel]])
    ys = np.array(sorted(annual)); b, a = np.polyfit(ys + 0.5, [annual[y] for y in ys], 1)
    ymsl = np.array([annual.get(y, a + b * (y + 0.5)) for y in yrs])
    adj = om - ymsl + design                       # each year's high waters at 2027 sea level
    years = np.arange(1995, 2027)
    out = {}
    out["climatology at 2027 sea level"] = np.array([np.mean([np.nansum(adj[yrs == y] >= L) for y in years]) for L in C.DECK_SETTINGS])
    raw = np.array([[np.nansum(om[yrs == y] >= L) for L in C.DECK_SETTINGS] for y in years])
    out["linear trend on counts"] = np.array([np.polyval(np.polyfit(years, raw[:, j], 1), 2027) for j in range(len(C.DECK_SETTINGS))])
    pois = []
    for j in range(len(C.DECK_SETTINGS)):
        X = sm.add_constant(years - 2010.0)
        if raw[:, j].sum() == 0:
            pois.append(0.0); continue
        g = sm.GLM(raw[:, j], X, family=sm.families.Poisson()).fit()
        pois.append(float(np.exp(g.params[0] + g.params[1] * 17)))
    out["Poisson trend on counts"] = np.array(pois)
    out["last season (2026)"] = raw[-1].astype(float)
    out["last three seasons"] = raw[-3:].mean(axis=0)
    out["2008 and 2009 seasons at 2027 sea level"] = np.array([np.mean([np.nansum(adj[yrs == y] >= L) for y in (2008, 2009)]) for L in C.DECK_SETTINGS])
    # peaks over threshold on the season's high waters at 2027 sea level
    v = adj[np.isfinite(adj)]
    u = np.percentile(v, 97); e = v[v > u] - u
    xi, _, sc = stats.genpareto.fit(e, floc=0)
    rate = len(e) / len(years)
    out["peaks over threshold (GPD) at 2027 sea level"] = np.array([rate * stats.genpareto.sf(L - u, xi, 0, sc) if L > u
                                                                     else np.mean([np.nansum(adj[yrs == y] >= L) for y in years])
                                                                     for L in C.DECK_SETTINGS])
    # GEV on each season's highest tide at 2027 sea level, expected exceedances read as the annual probability
    mx = np.array([np.nanmax(adj[yrs == y]) for y in years])
    c, loc, scl = stats.genextreme.fit(mx)
    out["GEV on season maxima at 2027 sea level"] = np.array([-np.log(stats.genextreme.cdf(L, c, loc, scl)) for L in C.DECK_SETTINGS])
    # tide-aware with lesser errors
    out["pooled all-month surges (tide-aware)"] = expected(target, surges=skew_surges(target, months=tuple(range(1, 13))))
    out["surges not moved off each year's sea level (tide-aware)"] = expected(target, surges=skew_surges(target, detrend="none"))
    # highest predicted tide plus the surge exceeded once in the window
    fw = forward_mask(LD)
    s = np.sort(skew_surges(target))
    q = np.quantile(s, 1 - 1.0 / fw.sum())
    lvl = H[fw].max() + (design - dat["MSL"]) + q
    out["highest predicted tide plus a once-in-the-window surge"] = np.array([0.0 if L >= lvl else 9.9 for L in C.DECK_SETTINGS])
    return out


def default_path(target):
    E = rivals(target)["climatology at 2027 sea level"]
    return dict(E=E, pick=pick(E))


# --------------------------------------------------------------------------------------------- ask A: survival
@lru_cache(None)
def ask_a(target, bracket=True, telemetry_datum="2026"):
    """five highest tides 1 Nov 2016 to 30 Nov 2026 (local dates), no two within three days"""
    ts, ls = observed_series(target, telemetry_datum, bracket=bracket)
    T, H, LD = _hw(target)
    sel = np.array([C.ASK_A_FROM <= d <= C.ASK_A_TO for d in LD])
    om = tide_maxima(ts, ls, T[sel])
    cand = sorted([(float(x), T[sel][i], LD[sel][i]) for i, x in enumerate(om) if np.isfinite(x)], key=lambda r: -r[0])
    chosen = []
    for lvl, tm, ld in cand:
        if all(abs((tm - c[1]).astype("timedelta64[m]").astype(int)) > 3 * 24 * 60 for c in chosen):
            chosen.append((lvl, tm, ld))
        if len(chosen) == 5:
            break
    return [(c[2].isoformat(), round(c[0] + 1e-9, 2), c[0]) for c in chosen]


# ---------------------------------------------------------------------------------------------- ask B: closures
def _parse_close(s, system):
    if not s:
        return None
    if system == "WOMS":
        return dt.datetime.strptime(s, "%m/%d/%Y %H:%M")
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M")


@lru_cache(None)
def closure_rows(target):
    df = pd.read_csv(os.path.join(target, C.F_CLOSE), dtype=str, keep_default_na=False)
    rows = []
    for r in df.to_dict("records"):
        rows.append(dict(wo=r["wo_number"], system=r["system"], source=r["source"],
                         opened=_parse_close(r["opened"], r["system"]), closed=_parse_close(r["closed"], r["system"]),
                         location=r["location"], reason=r["reason"], notes=r["notes"]))
    return rows


def ask_b(target, legacy_clock="utc", same_tide=True, telemetry_datum="2026", bracket=True):
    """per year 2019-2026: Front Street flooding closures, each closure once, and those with the gauge at
    11.80 ft MLLW or more within three hours either side of the closure's start"""
    rows = [r for r in closure_rows(target) if "FRONT ST" in r["location"].upper() and r["reason"] == "FLOOD"]
    ev = []
    for r in rows:
        if r["system"] == "WOMS":
            u = r["opened"] if legacy_clock == "utc" else C.local_to_utc(r["opened"])
        else:
            u = C.local_to_utc(r["opened"])
        ev.append((u, r))
    ev.sort(key=lambda x: x[0])
    closures = []
    last_close = None
    for u, r in ev:
        cu = None
        if r["closed"] is not None:
            cu = r["closed"] if (r["system"] == "WOMS" and legacy_clock == "utc") else C.local_to_utc(r["closed"])
        if same_tide and closures and last_close is not None and (u - last_close).total_seconds() <= 3 * 3600:
            last_close = max(last_close, cu) if cu else last_close
            continue          # barricades reset on the same flooding: one closure
        closures.append((u, r))
        last_close = cu
    ts, ls = observed_series(target, telemetry_datum, bracket=bracket)
    tm = ts.astype("datetime64[m]").astype(np.int64)
    out = {}
    for y in C.ASK_B_YEARS:
        cs = [(u, r) for u, r in closures if C.to_local(u)[0].year == y]
        hit = 0
        for u, r in cs:
            k = np.datetime64(u, "m").astype(np.int64)
            a, b = np.searchsorted(tm, k - 180), np.searchsorted(tm, k + 180, side="right")
            if b > a and ls[a:b].max() >= C.STREET_LEVEL - 1e-9:
                hit += 1
        out[y] = (len(cs), hit)
    return out
