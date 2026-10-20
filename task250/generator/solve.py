"""The golden, computed from the shipped files only: the 2028 setting and each setting's drift alerts a year (the quality
control re-run on the 2025 to 2027 record with the stations the network keeps in 2028, against the limits the January
configuration sets from the recorded statistic, plus one alert for every drift the record's own alerts cut short that
the re-run never alerted before its repair); each district's 2027 drift-alert visits and the days their alerts waited
for them; each district's 2027 breakdown visits at the stations the network keeps.

    S.solve(target) -> dict"""
import datetime as dt
import os
import re

import numpy as np
import pandas as pd
from pypdf import PdfReader

import params as P

FILES = dict(daily="estaciones_diario_2025-2027.csv", qc="control_calidad_2025-2027.parquet",
             register="registro_estaciones.xlsx", procedure="QC-02_control_calidad_temperatura_v4.pdf",
             orders="ordenes_trabajo_2025-2027.xlsx", checks="comprobaciones_patron_2025-2027.csv",
             plan="plan_campo_2028.pdf")
START = pd.Timestamp("2025-01-01")
NDAYS = 3 * 365
HISTORY = "Historial sensor T"


def register(target):
    return pd.read_excel(os.path.join(target, FILES["register"]), sheet_name="Estaciones")


def history(target):
    h = pd.read_excel(os.path.join(target, FILES["register"]), sheet_name=HISTORY)
    h["fecha"] = pd.to_datetime(h["fecha"])
    return h


def qc_matrix(target, reg):
    q = pd.read_parquet(os.path.join(target, FILES["qc"]))
    col = {c: j for j, c in enumerate(reg["codigo"])}
    k = ((q["fecha"] - START).dt.days).to_numpy()
    j = q["estacion"].map(col).to_numpy()
    A = np.full((NDAYS, len(reg)), np.nan)
    A[k, j] = q["anomalia"].to_numpy()
    Sx = np.full((NDAYS, len(reg)), np.nan)
    Sx[k, j] = q["estadistico_14d"].astype(float).to_numpy()
    return q, A, Sx


def budget(target):
    t = " ".join("\n".join(p.extract_text() for p in PdfReader(os.path.join(target, FILES["plan"])).pages).split())
    m = re.search(r"Drift alerts (\d+)", t)
    return int(m.group(1))


def rerun(A, xy, pool):
    """QC-02 sections 4 and 5 over the record with `pool` as the network"""
    N = A.shape[1]
    dist = np.hypot(xy[:, None, 0] - xy[None, :, 0], xy[:, None, 1] - xy[None, :, 1]) / 1000.0
    have = ~np.isnan(A)
    R = np.full_like(A, np.nan)
    for i in range(N):
        o = [j for j in np.argsort(dist[i], kind="stable") if j != i and pool[j] and dist[i, j] <= P.RADIUS_KM][:30]
        o = np.array(o, int)
        if len(o) < 3:
            continue
        av = have[:, o]
        c = np.cumsum(av, axis=1)
        pick = av & (c <= 3)
        ok = (c[:, -1] >= 3) & have[:, i]
        w = 1.0 / dist[i, o] ** 2
        num = (np.where(pick, np.nan_to_num(A[:, o]), 0.0) * w[None, :]).sum(1)
        den = (pick * w[None, :]).sum(1)
        R[ok, i] = A[ok, i] - num[ok] / den[ok]
    v = np.where(np.isnan(R), 0.0, R)
    n = (~np.isnan(R)).astype(int)
    cv = np.vstack([np.zeros((1, N)), np.cumsum(v, 0)])
    cn = np.vstack([np.zeros((1, N), int), np.cumsum(n, 0)])
    S = np.full_like(R, np.nan)
    for t in range(R.shape[0]):
        t0 = max(0, t + 1 - P.WINDOW)
        cnt = cn[t + 1] - cn[t0]
        mean = (cv[t + 1] - cv[t0]) / np.where(cnt > 0, cnt, 1)
        S[t] = np.where(cnt >= P.MIN_IN_WINDOW, mean, np.nan)
    S[~have] = np.nan
    return R, S


def alert_days_by_station(S, limit, stations):
    """section 8 over a statistic: the alert days of each station (beyond its limit, none in the 14 days before)"""
    out = {}
    for i in stations:
        last = -10 ** 6
        s = S[:, i]
        for t in np.where(~np.isnan(s) & (np.abs(np.nan_to_num(s)) > limit[i]))[0]:
            if t - last > P.HOLD_DAYS:
                out.setdefault(int(i), []).append(int(t))
                last = t
    return out


def count_alerts(S, limit, stations):
    return sum(len(v) for v in alert_days_by_station(S, limit, stations).values())


def drift_repairs(target, reg, q, h=None):
    """the drifts the record's own alerts cut short: each adjustment or replacement the sensor history enters at a
    drift-alert visit, with the alert that sent the visit (the station's latest alert in the quality control's export
    on or before that day). Returns (station index, alert day, repair day)."""
    h = history(target) if h is None else h
    h = h[(h["motivo"] == "Alerta de deriva") & h["error_encontrado_C"].notna()]
    a = q[q["alerta"] == "S"]
    by = {}
    for st, d in zip(a["estacion"], a["fecha"]):
        by.setdefault(st, []).append(pd.Timestamp(d))
    col = {c: j for j, c in enumerate(reg["codigo"])}
    out = []
    for st, d in zip(h["codigo"], h["fecha"]):
        prior = [x for x in by.get(st, []) if x <= d and (d - x).days <= 10]
        al = max(prior)
        out.append((col[st], int((al - START).days), int((d - START).days)))
    return out


def cut_short(per, repairs, keep, lookback=14):
    """the drifts a setting's alerts never reached before their repair, from `lookback` days before the alert that
    sent the visit to the repair: each would have kept growing until it crossed that setting's limit"""
    return [(i, a, v) for (i, a, v) in repairs if keep[i] and not any(a - lookback <= t <= v for t in per.get(i, []))]


def the_call(target, reg=None, A=None, Sx=None, q=None, pool=None, lookback=14, censor=True, rerun_network=True):
    reg = register(target) if reg is None else reg
    if A is None:
        q, A, Sx = qc_matrix(target, reg)
    xy = reg[["x_utm", "y_utm"]].to_numpy(float)
    keep = reg["baja_prevista"].isna().to_numpy() if pool is None else pool
    sd = np.nanstd(Sx, axis=0, ddof=1)
    S28 = rerun(A, xy, keep)[1] if rerun_network else Sx
    stations = np.where(keep)[0]
    rep = drift_repairs(target, reg, q)
    per, parts = {}, {}
    for k in P.SETTINGS:
        days = alert_days_by_station(S28, k * sd, stations)
        n = sum(len(v) for v in days.values())
        c = len(cut_short(days, rep, keep, lookback)) if censor else 0
        per[k] = (n + c) / 3.0
        parts[k] = (n, c)
    b = budget(target)
    ok = [k for k in P.SETTINGS if per[k] <= b]
    return {"per_year": per, "parts": parts, "setting": min(ok) if ok else None, "budget": b, "sd": sd, "S28": S28,
            "repairs": rep, "repairs_kept": sum(1 for r in rep if keep[r[0]])}


# ------------------------------------------------------------------ the asks: the 2027 field visits
def alert_days(q, reg):
    a = q[q["alerta"] == "S"]
    return {(s, d.date()) for s, d in zip(a["estacion"], a["fecha"])}


def daily_span(target):
    """each station-day's range in the loggers' export (tmin, tmax), the re-sent repeats once"""
    d = pd.read_csv(os.path.join(target, FILES["daily"]), sep=";", decimal=",", encoding="utf-8")
    d["fecha"] = pd.to_datetime(d["fecha"], format="%d/%m/%Y").dt.date
    d = d.drop_duplicates(["estacion", "fecha"])
    return {(s_, f_): (lo, hi) for s_, f_, lo, hi in zip(d["estacion"], d["fecha"], d["tmin"], d["tmax"])}


def station_days(target):
    """the days a technician read each station's sensor in its air: the calibration database's reading days at the
    station, under whatever order the entry form recorded, less a day with a reading the station's air could not have
    given (outside the range its logger recorded that day: a sensor read away from the station)"""
    ck = pd.read_csv(os.path.join(target, FILES["checks"]))
    ck["d"] = pd.to_datetime(ck["fecha_hora"]).dt.date
    span = daily_span(target)
    out = {}
    for (st, d), g in ck.groupby(["estacion", "d"]):
        lo, hi = span.get((st, d), (-np.inf, np.inf))
        vals = np.r_[g["t_estacion"].to_numpy(float), g["t_patron"].to_numpy(float)]
        if vals.min() >= lo and vals.max() <= hi:
            out.setdefault(st, []).append(d)
    return {st: sorted(v) for st, v in out.items()}


def _field(target, reg, q, link=3):
    """every 2027 field visit: (order, station, kind, alert day or None, visit day). The old contractor's sheet gives the
    visit's day (Visita, blank on an order cancelled or closed without one). The new contractor's visit_date is the day
    the order was closed on its app, and every visit since July 2027 includes a check: a station of a Corrective was
    visited on the first day from the order's opening to its visit_date on which the technician read the station's
    sensor there, and not visited if there is none. A Corrective opened within `link` days of an alert at the station
    answered it."""
    alerts = alert_days(q, reg)
    xo = pd.ExcelFile(os.path.join(target, FILES["orders"]))
    old = xo.parse(xo.sheet_names[0])
    new = xo.parse(xo.sheet_names[1])
    at = station_days(target)

    def alert_before(st, d, days):
        for j in range(0, days + 1):
            if (st, d - dt.timedelta(days=j)) in alerts:
                return d - dt.timedelta(days=j)
        return None

    out = []
    for r in old.itertuples(index=False):
        ref, st, tipo, aviso, visita, estado = r[0], r[1], r[2], r[3], r[4], r[5]
        if estado != "Cerrada" or pd.isna(visita):
            continue
        d = pd.Timestamp(visita).date()
        if tipo == "Alerta deriva":
            out.append((ref, st, "drift", alert_before(st, pd.Timestamp(aviso).date(), link), d))
        elif tipo == "Avería":
            out.append((ref, st, "breakdown", None, d))
        else:
            out.append((ref, st, "scheduled", None, d))
    for r in new.itertuples(index=False):
        ref, sts, wt, opened, closed, status = r[0], r[1], r[2], r[3], r[4], r[5]
        if status != "Closed" or pd.isna(closed):
            continue
        d0, d1 = pd.Timestamp(opened).date(), pd.Timestamp(closed).date()
        for st in str(sts).split(" / "):
            x = [d for d in at.get(st, ()) if d0 <= d <= d1]
            if not x:
                continue
            if wt == "Corrective":
                al = alert_before(st, d0, link)
                out.append((ref, st, "drift" if al is not None else "breakdown", al, x[0]))
            else:
                out.append((ref, st, "scheduled", None, x[0]))
    return [v for v in out if v[4].year == 2027]


def ask_a(target, reg=None, q=None):
    """each district's 2027 drift-alert visits and the days their alerts waited for them, in total"""
    reg = register(target) if reg is None else reg
    if q is None:
        q, _, _ = qc_matrix(target, reg)
    dist_of = dict(zip(reg["codigo"], reg["comarca"]))
    out = {nm: {"visits": 0, "days_waited": 0} for _, nm in P.DISTRICTS}
    rows = [v for v in _field(target, reg, q) if v[2] == "drift"]
    for ref, st, kind, al, d in rows:
        nm = dist_of[st]
        out[nm]["visits"] += 1
        out[nm]["days_waited"] += (d - al).days
    return out, rows


def ask_b(target, reg=None, q=None):
    """each district's 2027 breakdown visits at the stations the network keeps in 2028"""
    reg = register(target) if reg is None else reg
    if q is None:
        q, _, _ = qc_matrix(target, reg)
    dist_of = dict(zip(reg["codigo"], reg["comarca"]))
    keep = set(reg.loc[reg["baja_prevista"].isna(), "codigo"])
    out = {nm: 0 for _, nm in P.DISTRICTS}
    rows = [v for v in _field(target, reg, q) if v[2] == "breakdown" and v[1] in keep]
    for v in rows:
        out[dist_of[v[1]]] += 1
    return out, rows


def solve(target):
    reg = register(target)
    q, A, Sx = qc_matrix(target, reg)
    call = the_call(target, reg, A, Sx, q)
    a, a_rows = ask_a(target, reg, q)
    b, b_rows = ask_b(target, reg, q)
    return {"call": call, "ask_a": a, "ask_a_rows": a_rows, "ask_b": b, "ask_b_rows": b_rows}
