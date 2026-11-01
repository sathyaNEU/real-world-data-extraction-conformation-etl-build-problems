"""Every rung of the ladder, the golden and the asks, computed from target/ alone (the shipped files as a solver
reads them). checks.py, ceiling.py, golden.py and writeup.py all take their figures from here."""
import math
import os
import re

import numpy as np
import openpyxl
import pandas as pd
from scipy import stats

import io_util as IO
import lp3 as L

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
RAISES = [0, 1, 2, 3, 4]


def sta_int(s):
    a, b = str(s).strip().split("+")
    return int(a) * 100 + int(b)


def _find(target, pat):
    for f in sorted(os.listdir(target)):
        if re.search(pat, f):
            return os.path.join(target, f)
    raise FileNotFoundError(pat)


def water_year(ts):
    return ts.year + 1 if ts.month >= 10 else ts.year


class Pack:
    """The shipped files, parsed the way the documents describe them."""

    def __init__(self, target=TARGET):
        self.target = target
        self._peaks()
        self._docs()
        self._inventory()

    # ---------------------------------------------------------------- main-call files
    def _peaks(self):
        df = pd.read_csv(_find(self.target, r"annual_peaks.*\.csv$"), comment="#", dtype={"site_no": str,
                                                                                          "peak_cd": str})
        df["peak_dt"] = pd.to_datetime(df["peak_dt"])
        df["wy"] = [water_year(t) for t in df["peak_dt"]]
        self.peaks_df = df
        self.hal = df[df.site_no == "05433000"].set_index("wy")["peak_va"].astype(float).sort_index()
        self.coy = df[df.site_no == "05432100"].set_index("wy")["peak_va"].astype(float).sort_index()
        self.fen = df[df.site_no == "05433500"].set_index("wy")["peak_va"].astype(float).sort_index()
        self.ash = df[df.site_no == "05431500"].set_index("wy")["peak_va"].astype(float).sort_index()

    def _docs(self):
        sk = IO.pdf_text(_find(self.target, r"regional_skew.*\.pdf$"))
        m = re.search(r"2 Central Lowlands\s+(-?\d\.\d+)\s+(\d\.\d+)", sk)
        self.gr, self.mse_r = float(m.group(1)), float(m.group(2))
        st = IO.pdf_text(_find(self.target, r"LS-02.*\.pdf$"))
        self.fb_gen = float(re.search(r"Levee generally\s+(\d\.\d) ft", st).group(1))
        self.fb_bridge = float(re.search(r"closure structure\s+(\d\.\d) ft", st).group(1))
        self.fb_up = float(re.search(r"(\d\.\d) ft at station 0\+00", st).group(1))
        self.len_ft = sta_int(re.search(r"downstream end, station (\d+\+\d\d)", st).group(1))
        self.aep = float(re.search(r"has a (\d+) per cent chance", st).group(1)) / 100.0
        t4 = IO.pdf_text(_find(self.target, r"Table4.*\.pdf$"))
        qs = [int(x.replace(",", "")) for x in re.findall(r"(\d{2,3},000)", t4)]
        qs = sorted(set(qs))
        rows = {}
        for m in re.finditer(r"(\d+\+\d\d)(?:[^0-9+]*?)((?:\s*\d{3}\.\d\d){10})", t4):
            rows[sta_int(m.group(1))] = [float(v) for v in m.group(2).split()]
        self.t4 = pd.DataFrame(rows, index=qs).T.sort_index()

    def _inventory(self):
        wb = openpyxl.load_workbook(_find(self.target, r"levee_inventory.*\.xlsx$"), data_only=True)
        seg = pd.DataFrame(list(wb["Segments"].values)[1:], columns=list(wb["Segments"].values)[0])
        self.segments = seg
        cr = list(wb["Orrinsford crown"].values)
        self.crown = {sta_int(r[0]): float(r[2]) for r in cr[1:]}
        g = pd.DataFrame(list(wb["Gauges"].values)[1:], columns=list(wb["Gauges"].values)[0])
        self.gauges = g
        sx = list(wb["Structures"].values)[1:]
        self.bridges = [sta_int(r[1]) for r in sx if "bridge" in str(r[2]).lower()]

    # ---------------------------------------------------------------- the levee raises between the gauges
    def raises_between(self):
        """(segment, in-force water year) for every levee segment between Coyle Bridge and Orrinsford whose crown was
        raised: a raise reported complete in a calendar year is in force from the next water year's flood season."""
        rm = self.gauges.set_index("Site")["River mile"]
        up, dn = float(rm["05432100"]), float(rm["05433000"])
        out = []
        for _, r in self.segments.iterrows():
            a, b = float(r["From RM"]), float(r["To RM"])
            if not (dn < min(a, b) and max(a, b) < up):
                continue
            txt = str(r["Crown raised"] or "").strip()
            if not txt:
                continue
            yr = int(re.search(r"(\d{4})", txt).group(1))
            out.append((r["Segment ID"], yr + 1))
        return out

    def first_post_wy(self):
        return max(w for _, w in self.raises_between())


# ------------------------------------------------------------------ the frequency curve and the crown
def q_aep(series, P, aep=None):
    return L.quantile(L.fit(series, P.gr, P.mse_r), P.aep if aep is None else aep)


def fit(series, P):
    return L.fit(series, P.gr, P.mse_r)


def freeboard(P, s):
    near = any(abs(s - b) <= 100 for b in P.bridges)
    return (P.fb_bridge if near else P.fb_gen) + P.fb_up * (1 - s / P.len_ft)


def wse_at(P, q, s):
    row = P.t4.loc[s]
    return float(np.interp(q, list(P.t4.columns), row.values))


def q_at_wse(P, z, s):
    """Discharge whose Table 4 water surface at station s is z (linear in discharge between the columns, extended
    along the end segments)."""
    qs = np.array(P.t4.columns, float)
    zs = P.t4.loc[s].values
    if z <= zs[0]:
        return qs[0] + (z - zs[0]) * (qs[1] - qs[0]) / (zs[1] - zs[0])
    if z >= zs[-1]:
        return qs[-1] + (z - zs[-1]) * (qs[-1] - qs[-2]) / (zs[-1] - zs[-2])
    return float(np.interp(z, zs, qs))


def need(P, q):
    """Largest shortfall of the crown below the design water surface plus freeboard over the cross-sections (ft)."""
    return max(wse_at(P, q, s) + freeboard(P, s) - P.crown[s] for s in P.t4.index)


def raise_for(P, q):
    n = need(P, q)
    return 0 if n <= 0 else int(math.ceil(n - 1e-9))


def capacity(P, r):
    """Discharge the levee raised r ft holds with its freeboard at every cross-section."""
    return min(q_at_wse(P, P.crown[s] + r - freeboard(P, s), s) for s in P.t4.index)


def governing(P, r):
    return min(P.t4.index, key=lambda s: q_at_wse(P, P.crown[s] + r - freeboard(P, s), s))


def settings(P, f):
    return [100.0 * L.exceedance(f, capacity(P, r)) for r in RAISES]


# ------------------------------------------------------------------ the routes
def present_series(P, how="ratio", cut=None, fit_from=None):
    """Orrinsford's peaks for the river as it now runs: the observed peaks from the first water year with every levee
    between the gauges raised, and Coyle Bridge's peaks carried across by the relation the two gauges show over
    those years for the water years before it."""
    cut = P.first_post_wy() if cut is None else cut
    fit_from = cut if fit_from is None else fit_from
    wy = np.array(P.hal.index)
    T = P.hal.values
    U = P.coy.reindex(wy).values
    pf = wy >= fit_from
    post = wy >= cut
    if how == "ratio":
        r = np.sum(T[pf] * U[pf]) / np.sum(U[pf] ** 2)
        est = r * U
    elif how == "meanratio":
        est = np.mean(T[pf] / U[pf]) * U
    elif how == "ratio_of_means":
        est = np.mean(T[pf]) / np.mean(U[pf]) * U
    elif how == "logols":
        b = np.polyfit(np.log10(U[pf]), np.log10(T[pf]), 1)
        est = 10 ** np.polyval(b, np.log10(U))
    elif how == "move1":
        x, y = np.log10(U[pf]), np.log10(T[pf])
        est = 10 ** (y.mean() + y.std(ddof=1) / x.std(ddof=1) * (np.log10(U) - x.mean()))
    elif how == "ols":
        b = np.polyfit(U[pf], T[pf], 1)
        est = np.polyval(b, U)
    elif how == "max_obs":
        r = np.sum(T[pf] * U[pf]) / np.sum(U[pf] ** 2)
        est = np.maximum(r * U, T)
    else:
        raise ValueError(how)
    return np.where(post, T, est)


def routes(P):
    """Each rung and off-ladder route: (design discharge, the raise it files, the series or None)."""
    wy = np.array(P.hal.index)
    T = P.hal.values
    U = P.coy.reindex(wy).values
    cut = P.first_post_wy()
    out = {}
    out["R0_at_site"] = T
    out["R2_post_raise_only"] = T[wy >= cut]
    rp = np.sum(T * U) / np.sum(U ** 2)
    out["R3_whole_record_relation"] = rp * P.coy.values
    out["golden"] = present_series(P)
    out["off_coyle_unscaled"] = P.coy.values
    out["off_since_1994"] = T[wy >= 1994]
    res = {}
    for k, s in out.items():
        q = q_aep(s, P)
        res[k] = {"q": q, "raise": raise_for(P, q), "fit": fit(s, P), "n": len(s)}
    for b in (0.5, 0.7, 1.0):
        da = P.gauges.set_index("Site")["Drainage area (sq mi)"]
        q = q_aep(P.coy.values, P) * (float(da["05433000"]) / float(da["05432100"])) ** b
        res["off_area_ratio_%.1f" % b] = {"q": q, "raise": raise_for(P, q), "fit": None, "n": len(P.coy)}
    r_post = np.sum(T[wy >= cut] * U[wy >= cut]) / np.sum(U[wy >= cut] ** 2)
    q = r_post * q_aep(P.coy.values, P)
    res["golden_transfer"] = {"q": q, "raise": raise_for(P, q), "fit": None, "n": len(P.coy)}
    return res


def golden_family(P):
    """Every construction of the present river's record a competent analyst would defend once the raises are seen:
    the estimator of the two-gauge relation, the years it is fitted on, which pre-raise years are carried across."""
    fam = {}
    cut = P.first_post_wy()
    for how in ("ratio", "meanratio", "ratio_of_means", "logols", "move1", "ols", "max_obs"):
        fam["%s_cut%d" % (how, cut)] = present_series(P, how=how)
    for c in (cut - 1, cut + 1, cut + 3):
        fam["ratio_fit%d" % c] = present_series(P, how="ratio", fit_from=c)
    wy = np.array(P.hal.index)
    T = P.hal.values
    U = P.coy.reindex(wy).values
    r = np.sum(T[wy >= cut] * U[wy >= cut]) / np.sum(U[wy >= cut] ** 2)
    fam["all_years_from_coyle"] = r * U
    # carry across only the water years before the first raise, keep the partly raised years as observed
    first = min(w for _, w in P.raises_between())
    fam["keep_partial_years"] = np.where(wy >= first, T, r * U)
    return fam


def trend_tests(x):
    x = np.asarray(x, float)
    n = len(x)
    s = sum(np.sum(np.sign(x[i + 1:] - x[i])) for i in range(n - 1))
    var = n * (n - 1) * (2 * n + 5) / 18.0
    z = (s - np.sign(s)) / math.sqrt(var)
    p_mk = 2 * (1 - stats.norm.cdf(abs(z)))
    k = 0
    for t in range(1, n):
        k = max(k, abs(np.sum(np.sign(x[t:, None] - x[None, :t]))))
    p_pt = min(1.0, 2 * math.exp(-6 * k ** 2 / (n ** 3 + n ** 2)))
    return p_mk, p_pt


def grubbs_beck_low(series):
    """Bulletin 17B low-outlier threshold (10 per cent one-sided) on the logs; returns the count below it."""
    y = np.log10(np.asarray(series, float))
    n = len(y)
    kn = -0.9043 + 3.345 * math.sqrt(math.log10(n)) - 0.4046 * math.log10(n)
    lo = y.mean() - kn * y.std(ddof=1)
    return int(np.sum(y < lo))


def main_figures(P):
    s = present_series(P)
    f = fit(s, P)
    q = L.quantile(f, P.aep)
    return {"q_design": q, "q_design_5k": int(round(q / 5000.0) * 5000), "aep": settings(P, f),
            "aep_1dp": [round(a, 1) for a in settings(P, f)], "raise": raise_for(P, q), "need": need(P, q),
            "cut": P.first_post_wy(), "fit": f, "capacity": [capacity(P, r) for r in RAISES],
            "governing": [governing(P, r) for r in RAISES]}


# ------------------------------------------------------------------ ask: crown settlement by reach
class AskFiles:
    def __init__(self, target=TARGET):
        self.target = target
        c24 = pd.read_csv(_find(target, r"crown_certification_survey_2024\.csv$"), comment="#")
        c24["sta"] = c24["station"].map(sta_int)
        self.c24 = c24
        c16 = pd.read_csv(_find(target, r"crown_survey_2016\.csv$"), comment="#")
        c16["sta"] = c16["STA"].map(sta_int)
        self.c16 = c16
        self.bench = pd.read_csv(_find(target, r"benchmark_list\.csv$"), comment="#")
        cy = pd.read_csv(_find(target, r"05432100_hourly.*\.csv$"), comment="#")
        cy["t"] = pd.to_datetime(cy["datetime_utc"])
        self.coy = cy
        with open(_find(target, r"ORF2_logger_export.*\.csv$")) as fh:
            head = [next(fh) for _ in range(4)]
        self.hb_datum = float(re.search(r"([\d.]+) ft NGVD 29", head[2]).group(1))
        hb = pd.read_csv(_find(target, r"ORF2_logger_export.*\.csv$"), skiprows=4)
        hb.columns = ["stamp", "stage"]
        hb["t"] = pd.to_datetime(hb["stamp"], format="%m/%d/%Y %H:%M")
        self.hb = hb
        with open(_find(target, r"05432100_hourly.*\.csv$")) as fh:
            head = [next(fh) for _ in range(4)]
        self.coy_datum_now = float(re.search(r"datum ([\d.]+) ft above NGVD 29", head[2]).group(1))
        pr = IO.pdf_text(_find(target, r"OP-04.*\.pdf$"))
        m = re.search(r"warning level, elevation ([\d.]+) ft NGVD 29 \(([\d.]+) ft on the gauge\)", pr)
        self.warn_elev, self.warn_stage = float(m.group(1)), float(m.group(2))
        self.sill = float(re.search(r"the closure sill, ([\d.]+) ft NAVD 88", pr).group(1))


def datum_shift(A):
    return float(np.mean(A.bench["elev_navd88_ft"] - A.bench["elev_ngvd29_ft"]))


def station_offset(A):
    """Old (2016) station minus present station, from the structures both surveys shot."""
    f24 = A.c24[A.c24.code != "CL"].set_index("code")["sta"]
    f16 = A.c16[~A.c16.DESC.isin(["CL"]) & ~A.c16.DESC.str.startswith("BM")].set_index("DESC")["sta"]
    common = [c for c in f24.index if c in f16.index]
    offs = sorted(set(int(f16[c] - f24[c]) for c in common))
    return offs, common


def settlement(A, offset=None, shift=None, use_features=False):
    offset = station_offset(A)[0][0] if offset is None else offset
    shift = datum_shift(A) if shift is None else shift
    c24 = A.c24 if use_features else A.c24[A.c24.code == "CL"]
    z24 = c24.groupby("sta")["elev_ft"].mean()
    reach = A.c24.groupby("sta")["reach"].first()
    rows = A.c16[A.c16.DESC == "CL"] if not use_features else A.c16[~A.c16.DESC.str.startswith("BM")]
    d = {}
    for _, r in rows.iterrows():
        s = int(r["sta"]) - offset
        if s in z24.index:
            d.setdefault(reach[s], []).append(float(r["ELEV"]) + shift - float(z24[s]))
    return {k: float(np.mean(v)) for k, v in sorted(d.items())}


# ------------------------------------------------------------------ ask: warning lead times
def coy_datum_change(A):
    """The hour the Coyle Bridge gauge height steps against discharge (a gauge datum change): the stage-discharge
    relation fitted over the flows every year shares, and the first sustained step in the residuals."""
    cy = A.coy.dropna()
    q = cy["discharge_cfs"].values.astype(float)
    h = cy["stage_ft"].values.astype(float)
    t = cy["t"].values
    band = (q >= 1500) & (q <= 15000)
    first = band & (t < np.datetime64("2018-10-01"))
    b = np.polyfit(np.log(q[first]), h[first], 2)
    res = np.full(len(h), np.nan)
    res[band] = h[band] - np.polyval(b, np.log(q[band]))
    s = pd.Series(res).dropna()
    med = s.rolling(48, min_periods=48).median()
    k = int(med[med > 1.0].index[0])
    j = int(s.index[s.index.get_loc(k) - 47])
    while not (res[j] > 1.0):
        j += 1
    after = res[j:j + 3000]
    before = res[max(j - 3000, 0):j]
    step = float(np.median(after[~np.isnan(after)]) - np.median(before[~np.isnan(before)]))
    return pd.Timestamp(t[j]), step


def halbrook_clock(A, peaks=None):
    """The ORF2 stamps against the State Water Survey's published Orrinsford peak times (local standard time): each
    water year's highest ORF2 reading sits on the published time before the logger swap (the long gap in the
    stamps) and six hours after it since, so the earlier stamps are local standard time."""
    t = A.hb["t"]
    j = int(t.diff().idxmax())
    swap = t.iat[j]
    pk = peaks if peaks is not None else pd.read_csv(_find(A.target, r"annual_peaks.*\.csv$"), comment="#",
                                                      dtype={"site_no": str})
    pk = pk[pk.site_no == "05433000"].copy()
    pk["when"] = pd.to_datetime(pk["peak_dt"] + " " + pk["peak_tm"].fillna("00:00"))
    hb = A.hb.copy()
    hb["wy"] = [water_year(x) for x in hb["t"]]
    diffs = {"pre": [], "post": []}
    for _, r in pk[pk["when"] >= hb["t"].min()].iterrows():
        w = hb[(hb["t"] > r["when"] - pd.Timedelta(days=3)) & (hb["t"] < r["when"] + pd.Timedelta(days=3))]
        if w.empty:
            continue
        tm = w.loc[w["stage"].idxmax(), "t"]
        diffs["pre" if tm < swap else "post"].append((tm - r["when"]) / pd.Timedelta(hours=1))
    shift = int(round(np.median(diffs["post"]) - np.median(diffs["pre"])))
    return swap, shift


def lead_times(A, coy_mode="per_datum", clock_fix=True, hb_convert=True, convention="interp"):
    """For each flood that reached the Main Street sill at Orrinsford: hours from the Coyle Bridge warning to the
    sill. coy_mode: per_datum (21.0 ft before the datum change, the 2014 elevation on the present datum after),
    old_stage (21.0 ft throughout), elev_now (the 2014 elevation on the present datum throughout)."""
    change, _ = coy_datum_change(A)
    swap, shift_h = halbrook_clock(A)
    hb = A.hb.copy()
    if clock_fix:
        hb.loc[hb["t"] < swap, "t"] = hb.loc[hb["t"] < swap, "t"] + pd.Timedelta(hours=shift_h)
    sh = datum_shift(A) if hb_convert else 0.0
    sill_stage = A.sill - (A.hb_datum + sh)
    hs, ht = hb["stage"].values, hb["t"].values
    cy = A.coy
    cs, ct = cy["stage_ft"].values, cy["t"].values
    thr_now = A.warn_elev - A.coy_datum_now
    out = []
    for j in range(1, len(hs)):
        if not (hs[j] >= sill_stage > hs[j - 1]):
            continue
        if (ht[j] - ht[j - 1]) > np.timedelta64(1, "h"):
            continue
        th = _cross_time(ht[j - 1], hs[j - 1], ht[j], hs[j], sill_stage, convention)
        k = int(np.searchsorted(ct, ht[j]))
        best = None
        while k > 1 and (ht[j] - ct[k]) < np.timedelta64(160, "h"):
            k -= 1
            if coy_mode == "per_datum":
                thr = A.warn_stage if pd.Timestamp(ct[k]) < change else thr_now
            elif coy_mode == "old_stage":
                thr = A.warn_stage
            else:
                thr = thr_now
            if cs[k] >= thr > cs[k - 1]:
                best = _cross_time(ct[k - 1], cs[k - 1], ct[k], cs[k], thr, convention)
                break
        if best is None:
            continue
        out.append((pd.Timestamp(th), (th - best) / np.timedelta64(1, "h")))
    return out


def _cross_time(t0, v0, t1, v1, thr, convention):
    if convention == "first_at_or_above":
        return t1
    if convention == "last_below":
        return t0
    return t0 + (t1 - t0) * ((thr - v0) / (v1 - v0))


def ask_figures(A):
    st = settlement(A)
    lt = lead_times(A)
    return {"settlement": {k: round(v, 2) for k, v in st.items()}, "settlement_raw": st,
            "lead": [(t.strftime("%Y-%m-%d"), int(round(h))) for t, h in lt], "lead_raw": lt}


if __name__ == "__main__":
    P = Pack()
    m = main_figures(P)
    print("first fully raised water year", m["cut"])
    print("design discharge %.0f -> %d; need %.3f ft -> raise %d" % (m["q_design"], m["q_design_5k"], m["need"],
                                                                      m["raise"]))
    print("AEP by raise", ["%.3f" % a for a in m["aep"]], "capacities", [round(c) for c in m["capacity"]],
          "governing", m["governing"])
    for k, v in routes(P).items():
        print("  %-28s n=%2d  Q1%%=%7.0f  raise %d" % (k, v["n"], v["q"], v["raise"]))
    A = AskFiles()
    a = ask_figures(A)
    print(a["settlement"])
    print(a["lead"])
