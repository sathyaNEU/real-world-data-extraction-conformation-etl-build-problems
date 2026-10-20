"""Every route on the shipped pack to the bench list: the reflexes a careful analyst reaches for (the latest titration,
each converter's own titrations extrapolated in time or in NO2 converted, a pooled curve against the converter's age,
a straight line in NO2 converted, the recent rate carried forward, the efficiency today, the busiest stations) and
the family that files the golden (the pooled curve in NO2 converted with its knee, its forms and its forecasts).
Used by checks.py (the ladder, the forcing and the fork rows) and pair.py."""
import datetime as dt

import numpy as np
import pandas as pd

import solve as S


def _goes(T, col):
    return sorted(T.loc[T[col] < S.TH, "station"])


def own_points(D, P, serial, installed):
    """the converter in service's own titrations: the one after it went in, then every check on it"""
    t0 = S.change_time(installed)
    q = P[(P["serial"] == serial) & (P["start"] >= t0 - dt.timedelta(hours=12))]
    return q


def all_routes(D):
    base = S.call(D)
    T = base["table"].copy()
    P = base["points"]
    ser = S.series(D)
    t_end = base["t_end"]
    r = {}
    # the latest titration on each analyzer
    last = P[P["kind"] != "post-sostituzione"].sort_values("start").groupby("serial").tail(1).set_index("serial")
    T["R0"] = T["serial"].map(last["eta"])
    r["latest_titration"] = _goes(T, "R0")
    # each converter's own checks carried to the service day: in time (linear, quadratic) and in NO2 converted
    lin_t, quad_t, lin_d = [], [], []
    for x in T.itertuples(index=False):
        q = own_points(D, P, x.serial, x.installed)
        tt = np.array([(v - S.change_time(x.installed)).total_seconds() / 86400 for v in q["start"]])
        ee = q["eta"].to_numpy()
        dd = q["D"].to_numpy()
        ts = (dt.datetime.combine(x.service, dt.time(10)) - S.change_time(x.installed)).total_seconds() / 86400
        if len(q) >= 2:
            lin_t.append(float(np.polyval(np.polyfit(tt, ee, 1), ts)))
            quad_t.append(float(np.polyval(np.polyfit(tt, ee, 2), ts)) if len(q) >= 3 else lin_t[-1])
            lin_d.append(float(np.polyval(np.polyfit(dd, ee, 1), x.D_service)))
        else:
            lin_t.append(float(ee[-1]) if len(ee) else 1.0)
            quad_t.append(lin_t[-1])
            lin_d.append(lin_t[-1])
    T["R1"], T["R1q"], T["R1d"] = lin_t, quad_t, lin_d
    r["own_trend_in_time"] = _goes(T, "R1")
    r["own_quadratic_in_time"] = _goes(T, "R1q")
    r["own_line_in_NO2_converted"] = _goes(T, "R1d")
    # a pooled curve against the converter's age (days since it went in)
    ages = []
    for p in P.itertuples(index=False):
        if p.kind == "post-sostituzione":
            ages.append(0.0)
            continue
        ch = [c for c in S.changes(D)[p.serial] if S.change_time(c) <= p.start]
        ages.append((p.start - S.change_time(ch[-1])).total_seconds() / 86400)
    ages = np.array(ages)
    for deg, name in ((2, "pooled_age_quadratic"), (3, "pooled_age_cubic")):
        b = np.polyfit(ages, P["eta"].to_numpy(), deg)
        a_svc = np.array([(dt.datetime.combine(x.service, dt.time(10)) - S.change_time(x.installed)).total_seconds()
                          / 86400 for x in T.itertuples(index=False)])
        T[name] = np.polyval(b, a_svc)
        r[name] = _goes(T, name)
    # a straight line in NO2 converted, pooled
    b = np.polyfit(P["D"].to_numpy(), P["eta"].to_numpy(), 1)
    T["R3"] = np.polyval(b, T["D_service"])
    r["pooled_line_in_NO2_converted"] = _goes(T, "R3")
    # the pooled curve, the last 90 days' rate carried forward instead of the station's seasons
    f = base["curve"]
    rec = []
    for x in T.itertuples(index=False):
        d90 = S.dose(ser, x.serial, t_end - dt.timedelta(days=90), t_end) / 90.0
        n = (x.service - dt.date(2028, 1, 1)).days
        rec.append(float(f(x.D_now + d90 * n)))
    T["R4"] = rec
    r["pooled_curve_recent_rate"] = _goes(T, "R4")
    # the pooled curve, the year's mean daily rate carried forward
    yr = []
    for x in T.itertuples(index=False):
        d365 = S.dose(ser, x.serial, t_end - dt.timedelta(days=365), t_end) / 365.0
        n = (x.service - dt.date(2028, 1, 1)).days
        yr.append(float(f(x.D_now + d365 * n)))
    T["R4y"] = yr
    r["pooled_curve_year_rate"] = _goes(T, "R4y")
    # the efficiency today
    T["R5"] = [float(f(v)) for v in T["D_now"]]
    r["efficiency_today"] = _goes(T, "R5")
    k = len(base["goes"])
    lvl = {}
    for x in T.itertuples(index=False):
        t, v = ser[x.serial]
        lvl[x.station] = float(v.mean())
    r["busiest_stations"] = sorted(sorted(lvl, key=lambda s: -lvl[s])[:k])
    r["most_NO2_converted_now"] = sorted(T.sort_values("D_now", ascending=False)["station"].head(k))
    # the golden family
    r["golden"] = base["goes"]
    for name, kw in (("golden_cubic", dict(form="p3")), ("golden_quadratic", dict(form="p2")),
                     ("golden_last_two_years", dict(years=(2026, 2027))), ("golden_2027_only", dict(years=(2027,))),
                     ("golden_measuring_hours_only", dict(stato0=True)), ("golden_no_fresh_points", dict(post=False)),
                     ("golden_printed_efficiency", dict(col="eta_printed")), ("golden_sum_not_mean", dict(fill=False))):
        r[name] = S.call(D, **kw)["goes"]
    return r, T


REFLEXES = ["latest_titration", "own_trend_in_time", "own_quadratic_in_time", "own_line_in_NO2_converted",
            "pooled_age_quadratic", "pooled_age_cubic", "pooled_line_in_NO2_converted", "pooled_curve_recent_rate",
            "efficiency_today", "busiest_stations", "most_NO2_converted_now"]
GOLDEN_FAMILY = ["golden", "golden_cubic", "golden_quadratic", "golden_last_two_years", "golden_2027_only",
                 "golden_measuring_hours_only", "golden_no_fresh_points", "golden_printed_efficiency",
                 "golden_sum_not_mean", "pooled_curve_year_rate"]
