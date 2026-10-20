"""Every route on the shipped pack, station by station: the published regression refitted (the default path), the
reflexes a careful analyst reaches for, and the family of relations conditioned on rising water. Used by checks.py
(the ladder and the fork rows) and pair.py."""
import numpy as np
import pandas as pd

import solve as S

TOL = 15.0


def _ols(X, y):
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return b, float(np.mean(10 ** (y - X @ b)))


def station_arrays(rec, smp, code, shift_steps=0):
    r = S.station_series(rec, code)
    q = r["discharge_m3s"].interpolate(limit_direction="both").to_numpy()
    T = r["turbidity_fnu"].to_numpy()
    s = smp[smp["station"] == code]
    k = ((s["utc"].dt.round("15min") - pd.Timestamp("2025-01-01", tz="UTC")) / pd.Timedelta("15min")).astype(int).to_numpy()
    k = np.clip(k + shift_steps, 0, len(q) - 1)
    doy = ((r.index - pd.Timestamp("2025-01-01", tz="UTC")) / pd.Timedelta("1D")).to_numpy() % 365
    hod = r.index.hour.to_numpy() + r.index.minute.to_numpy() / 60
    y27 = (r.index >= pd.Timestamp("2027-01-01", tz="UTC"))
    return dict(q=q, T=T, k=k, y=np.log10(s["ssc"].to_numpy()), callout=(s["trip"] == "flood callout").to_numpy(),
                year=s["year"].to_numpy(), doy=doy, hod=hod, y27=y27)


def loads(d):
    """each route's 2027 concentration series -> its load in tonnes"""
    q, T, k, y = d["q"], d["T"], d["k"], d["y"]
    lT = np.log10(T)
    lq = np.log10(q)
    one = np.ones(len(k))
    c1, s1 = np.cos(2 * np.pi * d["doy"] / 365), np.sin(2 * np.pi * d["doy"] / 365)
    ch, sh = np.cos(2 * np.pi * d["hod"] / 24), np.sin(2 * np.pi * d["hod"] / 24)
    rate = np.gradient(q) / 0.25 / q
    rs = np.convolve(rate, np.ones(4) / 4, "same")
    cal = d["callout"].astype(float)
    m = d["y27"]
    out = {}

    def fit(cols, name, pred=None, rows=None):
        rows = np.ones(len(k), bool) if rows is None else rows
        X = np.c_[[one[rows]] + [(c[rows] if len(c) == len(k) else c[k][rows]) for c in cols]].T
        b, bcf = _ols(X, y[rows])
        P = cols if pred is None else pred
        conc = 10 ** (b[0] + sum(bi * (c[m] if len(c) == len(q) else c) for bi, c in zip(b[1:], P))) * bcf
        out[name] = float(np.sum(conc * q[m]) * 900 / 1e6)

    fit([lT], "refit")
    fit([lT, lq], "with_discharge")
    fit([lT, lq, c1, s1], "discharge_and_season")
    fit([lT, c1, s1], "season")
    fit([lT, ch, sh], "hour_of_day")
    fit([lT, cal], "trip_type", pred=[lT, np.zeros(m.sum())])
    fit([lT, lq, c1, s1, cal], "trip_type_and_more", pred=[lT, lq, c1, s1, np.zeros(m.sum())])
    fit([lT], "routine_only", rows=~d["callout"])
    fit([lT], "only_2027", rows=d["year"] == 2027)
    hi = (q > np.quantile(q, 0.8)).astype(float)
    fit([lT, hi], "flow_class")
    # rising water: the golden family
    for th in (0.0, 0.005, 0.01, 0.015, 0.02, 0.03):
        fit([lT, (rs > th).astype(float)], "rising_%.3f" % th)
    fit([lT, (rate > 0.01).astype(float)], "rising_unsmoothed")
    for lag_h in (1, 2):
        L = int(lag_h / 0.25)
        rr = np.r_[np.zeros(L), (q[L:] - q[:-L]) / q[:-L] / lag_h]
        fit([lT, (rr > 0.01).astype(float)], "rising_past_%dh" % lag_h)
    ind = rs > 0.015
    ii = ind[k]
    b1, f1 = _ols(np.c_[np.ones(ii.sum()), lT[k][ii]], y[ii])
    b0, f0 = _ols(np.c_[np.ones((~ii).sum()), lT[k][~ii]], y[~ii])
    conc = np.where(ind[m], 10 ** (b1[0] + b1[1] * lT[m]) * f1, 10 ** (b0[0] + b0[1] * lT[m]) * f0)
    out["rising_separate_fits"] = float(np.sum(conc * q[m]) * 900 / 1e6)
    fit([lT, lq, c1, s1, ind.astype(float)], "rising_with_discharge_and_season")
    fit([lT, rs], "rate_of_rise_linear")
    fit([lT, np.clip(rs, 0, None)], "rate_of_rise_positive")
    for w, nm in ((4, "turbidity_rising_1h"), (12, "turbidity_rising_3h"), (24, "turbidity_rising_6h")):
        lTs = np.convolve(lT, np.ones(w) / w, "same")
        fit([lT, (np.gradient(lTs) / 0.25 > 0.015 / np.log(10)).astype(float)], nm)
    return out


GOLDEN_FAMILY = ["rising_0.000", "rising_0.005", "rising_0.010", "rising_0.015", "rising_0.020", "rising_0.030",
                 "rising_unsmoothed", "rising_past_1h", "rising_past_2h", "rising_separate_fits",
                 "rising_with_discharge_and_season", "rate_of_rise_linear", "rate_of_rise_positive",
                 "turbidity_rising_1h", "turbidity_rising_3h", "turbidity_rising_6h"]
REFLEXES = ["refit", "with_discharge", "discharge_and_season", "season", "hour_of_day", "trip_type",
            "trip_type_and_more", "routine_only", "only_2027", "flow_class"]


def threshold_sweep(target, rec, smp, ths):
    """the golden relation at each threshold of the smoothed rate of rise -> {threshold: {station: published against it, %}}"""
    pub = S.read_report(target)
    out = {th: {} for th in ths}
    for code in sorted(smp["station"].unique()):
        d = station_arrays(rec, smp, code)
        q, k, y, m = d["q"], d["k"], d["y"], d["y27"]
        lT = np.log10(d["T"])
        rs = np.convolve(np.gradient(q) / 0.25 / q, np.ones(4) / 4, "same")
        for th in ths:
            ind = (rs > th).astype(float)
            b, bcf = _ols(np.c_[np.ones(len(k)), lT[k], ind[k]], y)
            L = float(np.sum(10 ** (b[0] + b[1] * lT[m] + b[2] * ind[m]) * bcf * q[m]) * 900 / 1e6)
            out[th][code] = 100 * (pub[code]["load_t"] / L - 1)
    return out


def all_routes(target, rec=None, smp=None, shift_steps=0):
    rec = S.record(target) if rec is None else rec
    smp = S.samples(target) if smp is None else smp
    pub = S.read_report(target)
    table = {}
    for code in sorted(smp["station"].unique()):
        L = loads(station_arrays(rec, smp, code, shift_steps))
        table[code] = {r: 100 * (pub[code]["load_t"] / v - 1) for r, v in L.items()}
    return table


def flagged(table, route):
    return sorted(c for c, v in table.items() if abs(v[route]) > TOL)
