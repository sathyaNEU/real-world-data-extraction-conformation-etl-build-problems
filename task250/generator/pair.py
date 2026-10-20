"""The ask layer measured on the cut pack: each path a response could take through the work orders and the calibration
database, the figures it keeps against the golden, the cracker (on the call: the hygiene battery, every filed rule
executed, the readings as the record of a visit) and the mirror (off the call, the same care), and the pair ceiling.
    python3 pair.py [target]      (--paths prints every path's figures)"""
import datetime as dt
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P
import solve as S

TASK = os.path.dirname(HERE)
NAMES = [nm for _, nm in P.DISTRICTS]


def _load(target):
    reg = S.register(target)
    q, _, _ = S.qc_matrix(target, reg)
    xo = pd.ExcelFile(os.path.join(target, S.FILES["orders"]))
    old, new = xo.parse(xo.sheet_names[0]), xo.parse(xo.sheet_names[1])
    ck = pd.read_csv(os.path.join(target, S.FILES["checks"]))
    ck["d"] = pd.to_datetime(ck["fecha_hora"]).dt.date
    return reg, q, old, new, ck


def path(target, old_by="visita", new_by="station", alert_day="qc", link=3):
    """old_by: 'visita' (a closed order with a Visita, that day) or 'readings' (the first reading under the order, else
    the Visita); new_by: 'golden' (the station's reading days, a day with a reading outside the logger's range left out),
    'station' (the station's reading days under any order), 'order' (the readings under the order only), 'date' (every
    closed order a visit on its visit_date) or 'order_date' (the readings under the order, else the visit_date);
    alert_day: 'qc' (the export's alert) or 'order' (Aviso, opened)"""
    reg, q, old, new, ck = _load(target)
    alerts = S.alert_days(q, reg)
    dist = dict(zip(reg["codigo"], reg["comarca"]))
    keep = set(reg.loc[reg["baja_prevista"].isna(), "codigo"])
    first = {k: g["d"].min() for k, g in ck.groupby(["orden", "estacion"])}
    days = {}
    for st, d in zip(ck["estacion"], ck["d"]):
        days.setdefault(st, set()).add(d)
    good = S.station_days(target)

    def before(st, d, n):
        for j in range(n + 1):
            if (st, d - dt.timedelta(days=j)) in alerts:
                return d - dt.timedelta(days=j)
        return None

    A = {n: [0, 0] for n in NAMES}
    Bc = {n: 0 for n in NAMES}

    def drift(st, al, notice, d):
        if d is None or d.year != 2027:
            return
        a0 = al if alert_day == "qc" and al is not None else notice
        A[dist[st]][0] += 1
        A[dist[st]][1] += (d - a0).days

    def breakdown(st, d):
        if d is not None and d.year == 2027 and st in keep:
            Bc[dist[st]] += 1

    for r in old.itertuples(index=False):
        ref, st, tipo, aviso, visita, estado = r[0], r[1], r[2], r[3], r[4], r[5]
        av = pd.Timestamp(aviso).date() if pd.notna(aviso) else None
        vi = pd.Timestamp(visita).date() if pd.notna(visita) else None
        if estado != "Cerrada" or vi is None:
            continue
        d = first.get((ref, st), vi) if old_by == "readings" else vi
        if tipo == "Alerta deriva":
            drift(st, before(st, av, link), av, d)
        elif tipo == "Avería":
            breakdown(st, vi)
    for r in new.itertuples(index=False):
        ref, sts, wt, opened, vd, status = r[0], r[1], r[2], r[3], r[4], r[5]
        if wt != "Corrective" or status != "Closed" or pd.isna(vd):
            continue
        d0, d1 = pd.Timestamp(opened).date(), pd.Timestamp(vd).date()
        for st in str(sts).split(" / "):
            if new_by == "golden":
                x = [d for d in good.get(st, ()) if d0 <= d <= d1]
                d = x[0] if x else None
            elif new_by == "station":
                x = sorted(d for d in days.get(st, ()) if d0 <= d <= d1)
                d = x[0] if x else None
            elif new_by == "order":
                d = first.get((ref, st))
            elif new_by == "date":
                d = d1
            else:
                d = first.get((ref, st), d1)
            if d is None:
                continue
            al = before(st, d0, link)
            if al is not None:
                drift(st, al, d0, d)
            else:
                breakdown(st, d)
    return ({n: A[n][0] for n in NAMES}, {n: A[n][1] for n in NAMES}, Bc)


def alert_led(target, window=14, temperature=False):
    """each 2027 alert's visit the station's first reading day within the window after it, whatever order it sits
    under (or the old sheet's Visita for its drift orders); breakdowns: the old sheet's closed Avería orders and every
    reading day since July 2027 that answered no alert, at kept stations"""
    reg, q, old, new, ck = _load(target)
    dist = dict(zip(reg["codigo"], reg["comarca"]))
    keep = set(reg.loc[reg["baja_prevista"].isna(), "codigo"])
    if temperature:
        days = {st: set(v) for st, v in S.station_days(target).items()}
    else:
        days = {}
        for st, d in zip(ck["estacion"], ck["d"]):
            days.setdefault(st, set()).add(d)
    od = old[(old["Tipo"] == "Alerta deriva") & old["Visita"].notna()]
    for st, v in zip(od["Estación"], od["Visita"]):
        days.setdefault(st, set()).add(pd.Timestamp(v).date())
    A = {n: [0, 0] for n in NAMES}
    used = set()
    for st, d in sorted(S.alert_days(q, reg)):
        c = sorted(x for x in days.get(st, ()) if d <= x <= d + dt.timedelta(days=window))
        if c:
            used.add((st, c[0]))
            if c[0].year == 2027:
                A[dist[st]][0] += 1
                A[dist[st]][1] += (c[0] - d).days
    Bc = {n: 0 for n in NAMES}
    ob = old[(old["Tipo"] == "Avería") & (old["Estado"] == "Cerrada") & old["Visita"].notna()]
    for st, v in zip(ob["Estación"], ob["Visita"]):
        if pd.Timestamp(v).year == 2027 and st in keep:
            Bc[dist[st]] += 1
    for st, ds in days.items():
        for d in ds:
            if d >= P.CONTRACT_SWITCH and d.year == 2027 and (st, d) not in used and st in keep:
                Bc[dist[st]] += 1
    return ({n: A[n][0] for n in NAMES}, {n: A[n][1] for n in NAMES}, Bc)


PATHS = {
    "golden": dict(new_by="golden"),
    "readings at the station while the order was open": dict(),
    "readings at the station, the order's notice as the alert": dict(alert_day="order"),
    "readings at the station, the old orders by their readings": dict(old_by="readings"),
    "readings under the order only": dict(new_by="order"),
    "readings under the order, else the visit_date": dict(new_by="order_date"),
    "every closed order on its visit_date": dict(new_by="date"),
    "every closed order on its visit_date, the notice as the alert": dict(new_by="date", alert_day="order"),
}
# the temperature test (a day with a reading outside the station's logged range left out) is the device's resolution,
# not a natural path; the alert-led route with it is reported beside the golden as a second route to the same figures
FOUND = ["golden", "alert-led within 14 days, the temperature test"]


def score(p, g):
    return (sum(p[0][n] == g[0][n] for n in NAMES), sum(p[1][n] == g[1][n] for n in NAMES),
            sum(p[2][n] == g[2][n] for n in NAMES))


def main(target):
    res = {k: path(target, **v) for k, v in PATHS.items()}
    for w in (9, 14, 21):
        res["alert-led within %d days" % w] = alert_led(target, w)
    res["alert-led within 14 days, the temperature test"] = alert_led(target, 14, temperature=True)
    g = res["golden"]
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    assert g[0] == fig["asks"]["drift_alert_visits_2027"] and g[1] == fig["asks"]["days_alerts_waited_2027"] \
        and g[2] == fig["asks"]["breakdown_visits_2027_stations_kept"], "pair.py's golden path is the golden"
    n = 3 * len(NAMES)
    sc = {}
    for k, p in res.items():
        a, b, c = score(p, g)
        sc[k] = a + b + c
        print("  %-62s visits %d/8  days %d/8  breakdowns %d/8   %2d/%d" % (k, a, b, c, a + b + c, n))
        if "--paths" in sys.argv:
            print("      ", [p[0][x] for x in NAMES], [p[1][x] for x in NAMES], [p[2][x] for x in NAMES])
    natural = [k for k in res if k not in FOUND]
    kc = max(sc[k] for k in natural)
    ks = kc
    lc, ls = kc / n, ks / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * ls
    print("cracker (the readings, the orders or both as the record of a visit, hygiene battery, no test of a reading "
          "against the station's logged range) keeps %d of %d; the mirror the same" % (kc, n))
    print("pair ceiling %.1f ((%.1f + %.1f) / 2); mirror leakage %.0f per cent of ask weight" % ((c + s) / 2, c, s, 100 * ls))
    worst = max(sc[k] for k in natural)
    print("worst case among the natural paths: keeps %d of %d (%.1f with the call)" % (worst, n, 38 + 7 + 55 * worst / n))
    return sc


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args[0] if args else os.path.join(TASK, "target"))
