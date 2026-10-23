"""Halvern's delivery-point interval export for 2026 and its monthly system peaks.

The four delivery-point revenue meters record 15-minute energy in their own clock, which is Pacific standard time
the whole year (the meters are never moved to daylight time); the export stamps each interval at its end. Each point also has a check meter on the same instrument transformers, a different model that stamps each
interval at its start; Halvern keeps such a check meter at every delivery point. Loads are built hour by hour in local prevailing time, because that is the clock farms and towns keep."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as C
import records as R
import world as Wd

UTC0 = dt.datetime(2026, 1, 1, 8, 0)          # 00:00 PST on 1 January 2026
UTC1 = dt.datetime(2026, 10, 15, 8, 0)        # 00:00 PST on 15 October 2026 (the export's last interval)
DST0 = dt.datetime(2026, 3, 8, 10, 0)         # 02:00 PST -> 03:00 PDT, in UTC
DST1 = dt.datetime(2026, 11, 1, 9, 0)

NONIP = {"RIVERSIDE": (5200.0, 2100.0), "MILL SLOUGH": (1500.0, 650.0), "BENCH": (2300.0, 1150.0),
         "CORWIN ROAD": (1100.0, 520.0)}      # kW: base, cooling swing on a hot day
METERS = {"RIVERSIDE": ["81-2207"], "MILL SLOUGH": ["81-3318"], "BENCH": ["81-1940"], "CORWIN ROAD": ["81-4062"]}
CHECK_METERS = {"RIVERSIDE": "81-2251", "MILL SLOUGH": "81-3362", "BENCH": "81-1988", "CORWIN ROAD": "81-4107"}
BENCH_BANK2 = "81-1977"                       # Bench bank 2 and its revenue meter, energised 15 June 2026
BANK2_UTC = dt.datetime(2026, 6, 15, 17, 0)   # 10:00 PDT
BANK2_SHARE = 0.42


def prevailing(utc):
    return utc - dt.timedelta(hours=7 if DST0 <= utc < DST1 else 8)


def meter_time(utc):
    return utc - dt.timedelta(hours=8)


def ip_month_kwh(W, ids, dp, y, m, day):
    """A delivery point's IP energy in a month, each senior plant at the source its feeder had on `day`."""
    tot = 0.0
    for i in range(W.nJ):
        if R.feeder_dp(ids["fdrJ"][i], day) == dp:
            tot += float(W.J_kwh[(y, m)][i])
    for i in range(W.nS):
        if R.feeder_dp(ids["fdrS"][i], day) == dp:
            tot += float(W.S_kwh[(y, m)][i])
    return tot


def build(W, ids):
    r = Wd.rng("dpi")
    ipm = {}
    for dp in C.DPS:
        for m in range(1, 10):
            ipm[(dp, m)] = ip_month_kwh(W, ids, dp, 2026, m, dt.date(2026, m, 1))
        ipm[(dp, 10)] = ip_month_kwh(W, ids, dp, 2025, 10, dt.date(2026, 10, 1))
    # feeder 1204 moved on 16 March: its March energy splits by days between the two delivery points
    f_mar = sum(float(W.S_kwh[(2026, 3)][i]) for i in range(W.nS) if ids["fdrS"][i] == R.TRANSFER_FEEDER)
    ipm[("RIVERSIDE", 3)] -= f_mar * 16 / 31
    ipm[("MILL SLOUGH", 3)] += f_mar * 16 / 31
    eto_day = {d: v for d, v in W.eto_daily if d.year == 2026}
    # daily weights within each month
    def dayw(d):
        m = d.month
        ndays = (R.month_end(2026, m) - dt.date(2026, m, 1)).days + 1
        if m in C.SEASON:
            tot = sum(eto_day[dt.date(2026, m, k)] for k in range(1, ndays + 1))
            return eto_day[d] / tot
        return 1.0 / ndays
    def ip_hour(hloc, m):
        w = 1.0
        if m in (6, 7, 8, 9) and 14 <= hloc < 20:
            w = 0.62
        elif hloc < 6 or hloc >= 22:
            w = 1.12
        return w
    norm = {m: sum(ip_hour(h, m) for h in range(24)) for m in range(1, 11)}
    def cool_shape(hloc):
        return max(0.0, np.sin(np.pi * (hloc - 9) / 13.0)) ** 1.6 if 9 <= hloc <= 22 else 0.0
    def res_shape(hloc):
        return 0.78 + 0.22 * np.exp(-((hloc - 19.0) / 2.6) ** 2) + 0.10 * np.exp(-((hloc - 7.5) / 1.5) ** 2)
    rows = []
    hourly = {dp: {} for dp in C.DPS}
    t = UTC0
    while t < UTC1:
        loc = prevailing(t)
        d = loc.date()
        if d.year != 2026:
            t += dt.timedelta(hours=1)
            continue
        m = d.month
        hl = loc.hour
        heat = max(0.0, (eto_day[d] - 0.12) / 0.20) if d in eto_day else 0.0
        for dp in C.DPS:
            ip = ipm[(dp, m)] * dayw(d) * ip_hour(hl, m) / norm[m] if m <= 10 else 0.0
            if m == 10:
                ip = ipm[(dp, 10)] / 31 * ip_hour(hl, m) / norm[m]
            base, swing = NONIP[dp]
            seas = 1.0 + 0.10 * np.cos(2 * np.pi * (d.timetuple().tm_yday - 15) / 365.0)
            non = base * seas * res_shape(hl) + swing * heat * cool_shape(hl)
            load = (ip + non) * float(r.normal(1, 0.02))
            loss = load * (0.034 + 0.018 * load / (base * 3.2 + 1))
            hourly[dp][t] = load + loss
        t += dt.timedelta(hours=1)
    for dp in C.DPS:
        for th, kwh_h in sorted(hourly[dp].items()):
            parts = np.clip(r.normal(1, 0.03, 4), 0.85, 1.15)
            parts = parts / parts.sum() * kwh_h
            for q in range(4):
                end_utc = th + dt.timedelta(minutes=15 * (q + 1))
                if end_utc > UTC1:
                    continue
                v = int(round(parts[q]))
                if dp == "BENCH" and end_utc > BANK2_UTC:
                    v2 = int(round(parts[q] * BANK2_SHARE * float(r.normal(1, 0.01))))
                    v = v - v2
                    rows.append((C.DP_CODES[dp], BENCH_BANK2, meter_time(end_utc), v2))
                rows.append((C.DP_CODES[dp], METERS[dp][0], meter_time(end_utc), v))
                # the check meter on the same instrument transformers, a model that stamps the interval's start
                rows.append((C.DP_CODES[dp], CHECK_METERS[dp], meter_time(end_utc - dt.timedelta(minutes=15)), v))
    df = pd.DataFrame(rows, columns=["dp_code", "meter_no", "stamp", "kwh"])
    rq = Wd.rng("dpi-kvar")
    df["kvarh"] = (df["kwh"] * rq.uniform(0.28, 0.42, len(df))).round().astype(int)
    df["status"] = np.where(rq.random(len(df)) < 0.0015, "E", "")
    df = df.sort_values(["dp_code", "meter_no", "stamp"]).reset_index(drop=True)
    df["interval_end"] = df["stamp"].dt.strftime("%Y-%m-%d %H:%M")
    return df[["dp_code", "meter_no", "interval_end", "kwh", "kvarh", "status"]]


def peaks(W):
    """Halvern's monthly system peak: the hottest weekday's late afternoon in summer, a winter evening in winter."""
    r = Wd.rng("peaks")
    eto_day = {d: v for d, v in W.eto_daily if d.year == 2026}
    rows = []
    for m in range(1, 10):
        ndays = (R.month_end(2026, m) - dt.date(2026, m, 1)).days + 1
        days = [dt.date(2026, m, k) for k in range(1, ndays + 1) if dt.date(2026, m, k).weekday() < 5]
        if m in (6, 7, 8, 9):
            day = max(days, key=lambda d: eto_day[d])
            he = int(r.choice([17, 18, 18, 19]))
        elif m in (4, 5):
            day = max(days, key=lambda d: eto_day[d])
            he = int(r.choice([18, 19, 20]))
        else:
            day = days[int(r.integers(0, len(days)))]
            he = int(r.choice([18, 19]))
        mw = 2380 + 900 * (m in (6, 7, 8, 9)) + float(r.normal(0, 60))
        rows.append({"month": "2026-%02d" % m, "peak_date": day.isoformat(), "hour_ending": "%02d:00" % he,
                     "system_peak_mw": round(mw, 1)})
    return pd.DataFrame(rows)
