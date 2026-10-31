"""The independent verifier: every graded figure recomputed from target/ by a second route, with pandas and a
KD-tree over points sampled along each stop-to-stop segment, never importing estim.py, and compared with the
figures the golden carries (figures.json).

    python3 task191/generator/verify.py
"""
import datetime as dt
import json
import math
import os
import sys

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
FIG = os.path.join(HERE, "figures.json")
DEPOTS = ["San Lázaro", "Hornacho", "Valdeolmos", "El Quiñón", "Las Tenerías", "La Ribera", "Santa Clara"]
OK = []
BAD = []


def same(name, a, b):
    (OK if a == b else BAD).append(name)
    if a != b:
        print("MISMATCH %s: %r against %r" % (name, a, b))


def main():
    fig = json.load(open(FIG))
    # ---- the call
    w = pd.read_csv(os.path.join(TARGET, "adas_collision_warnings_2025-10_2026-10.csv"), dtype=str, keep_default_na=False)
    w = w[w.warning_type.isin(["FCW", "PCW", "FWD_COLL", "PED_COLL"])].drop_duplicates("event_id", keep="first")
    t = pd.to_datetime(w.event_time_utc, utc=True).dt.tz_convert("Europe/Madrid")
    w = w.assign(local_day=t.dt.date)
    w = w[(w.local_day >= dt.date(2026, 1, 1)) & (w.local_day <= dt.date(2026, 10, 31))].copy()
    ms = pd.to_numeric(w.brake_reaction_ms, errors="coerce")
    w["braked"] = np.where(w.firmware.str.startswith("1."), w.brake_2s == "Y", ms.le(2000).fillna(False))
    alloc = pd.read_excel(os.path.join(TARGET, "fleet_register_2026.xlsx"), sheet_name="Allocations", dtype=str)
    alloc["a"] = pd.to_datetime(alloc["from"], format="%d/%m/%Y").dt.date
    alloc["b"] = pd.to_datetime(alloc["to"].fillna("31/12/2099"), format="%d/%m/%Y").dt.date
    amap = {}
    for r in alloc.itertuples():
        amap.setdefault(r.fleet_no, []).append((r.a, r.b, r.depot))
    w["depot"] = [next(dep for a, b, dep in amap[f] if a <= d <= b) for f, d in zip(w.fleet_no, w.local_day)]
    stops = pd.read_excel(os.path.join(TARGET, "red_paradas_recorridos_2025_2026.xlsx"), sheet_name="Paradas", dtype=str)
    sq = pd.read_excel(os.path.join(TARGET, "red_paradas_recorridos_2025_2026.xlsx"), sheet_name="Recorridos Red 2026",
                       dtype=str)
    sq["orden"] = sq.orden.astype(int)
    sq["a"] = pd.to_datetime(sq.vigente_desde, format="%d/%m/%Y").dt.date
    sq["b"] = pd.to_datetime(sq.vigente_hasta.fillna("31/12/2099"), format="%d/%m/%Y").dt.date
    xy = {r.codigo_2026: (float(r.latitud), float(r.longitud)) for r in stops.itertuples()}
    lat0 = np.mean([v[0] for v in xy.values()])
    kx, ky = 111_320.0 * math.cos(math.radians(lat0)), 111_320.0
    segs = {}
    periods = []
    for (line, sentido, a, b), g in sq.sort_values("orden").groupby(["linea", "sentido", "a", "b"]):
        if b < dt.date(2026, 1, 1):
            continue
        codes = list(g.codigo_parada)
        sl = [tuple(sorted(p)) for p in zip(codes, codes[1:])]
        periods.append((line, sentido, a, b, sl))
        for s in sl:
            segs[s] = True
    seg_list = sorted(segs)
    pts, owner, along = [], [], []
    for i, (p, q) in enumerate(seg_list):
        (la1, lo1), (la2, lo2) = xy[p], xy[q]
        x1, y1, x2, y2 = lo1 * kx, la1 * ky, lo2 * kx, la2 * ky
        L = math.hypot(x2 - x1, y2 - y1)
        n = max(2, int(L // 1.0))
        for k in range(n + 1):
            f = k / n
            pts.append((x1 + f * (x2 - x1), y1 + f * (y2 - y1)))
            owner.append(i)
            along.append(f * L)
    tree = cKDTree(np.array(pts))
    P = np.column_stack([w.longitude.astype(float) * kx, w.latitude.astype(float) * ky])
    _, idx = tree.query(P)
    w["seg"] = np.array(owner)[idx]
    w["pos"] = np.array(along)[idx]
    # Passes over each segment from the return.
    ret = pd.read_csv(os.path.join(TARGET, "service_return_2025-10_2026-10.csv"), sep=";", dtype=str)
    ret["day"] = pd.to_datetime(ret.fecha, format="%d/%m/%Y").dt.date
    ret = ret[(ret.day >= dt.date(2026, 1, 1)) & (ret.day <= dt.date(2026, 10, 31))]
    ret["op"] = ret.expediciones_realizadas.astype(int)
    passes = np.zeros(len(seg_list))
    sidx = {s: i for i, s in enumerate(seg_list)}
    for line, sentido, a, b, sl in periods:
        n = ret[(ret.linea == line) & (ret.sentido == sentido) & (ret.day >= a) & (ret.day <= b)].op.sum()
        for s in sl:
            passes[sidx[s]] += n
    # Places: 25 m windows centred on the densest 5 m cell of each segment, repeated while any window fires on a
    # tenth of the segment's passes.
    w["cell"] = (w.pos // 5).astype(int)
    drop = set()
    for s, g in w.groupby("seg"):
        cells = g.cell.value_counts()
        while len(cells):
            c = cells.index[0]
            win = g[(g.cell >= c - 2) & (g.cell <= c + 2)]
            if len(win) / passes[s] < 0.10:
                break
            drop.update(win.event_id)
            g = g[~g.event_id.isin(win.event_id)]
            cells = g.cell.value_counts()
    k = w[~w.event_id.isin(drop)]
    fleet = (~k.braked).sum() / len(k)
    for d in DEPOTS:
        g = k[k.depot == d]
        same("call %s warnings" % d, int(len(g)), fig["depots"][d]["warnings"])
        same("call %s not braked" % d, int((~g.braked).sum()), fig["depots"][d]["not_braked"])
        same("call %s rate" % d, round(100 * (~g.braked).mean(), 1), fig["depots"][d]["rate_pct"])
        same("call %s ratio" % d, round((~g.braked).mean() / fleet, 2), fig["depots"][d]["ratio"])
    same("fleet rate", round(100 * fleet, 1), fig["fleet_rate_pct"])
    taken = sorted(d for d in DEPOTS if (~k[k.depot == d].braked).mean() / fleet >= 1.3)
    same("depots taken", taken, fig["call"]["depots"])
    # ---- ask A: hours on service by depot and week
    e = pd.read_csv(os.path.join(TARGET, "etm_logons_2026-10.csv"), sep=";", dtype=str).drop_duplicates()
    e = e[~e.linea.isin(["000", "ESC"])].copy()
    e["on"] = pd.to_datetime(e.inicio_local)
    e["off"] = pd.to_datetime(e.fin_local)
    e = e.sort_values(["empleado", "on"])
    nxt = e.groupby("empleado").on.shift(-1)
    e["end"] = np.where(nxt.notna() & (nxt < e.off), nxt, e.off)
    e["end"] = pd.to_datetime(e["end"])
    h = (e.end - e.on).dt.total_seconds() / 3600
    change = pd.Timestamp("2026-10-25 03:00:00")
    h = h + np.where((e.on < change) & (e.end >= change), 1.0, 0.0)
    e["h"] = h
    hr = pd.read_csv(os.path.join(TARGET, "hr_depot_assignments_2026.csv"), sep=";", dtype=str)
    hr["a"] = pd.to_datetime(hr.desde, format="%d/%m/%Y").dt.date
    hr["b"] = pd.to_datetime(hr.hasta.fillna("31/12/2099"), format="%d/%m/%Y").dt.date
    hmap = {}
    for r in hr.itertuples():
        hmap.setdefault(r.empleado, []).append((r.a, r.b, r.cochera))
    e["day"] = e.on.dt.date
    e["depot"] = [next(dep for a, b, dep in hmap[x] if a <= d <= b) for x, d in zip(e.empleado, e.day)]
    weeks = [dt.date(2026, 10, 5) + dt.timedelta(days=7 * i) for i in range(4)]
    for d in DEPOTS:
        for i, w0 in enumerate(weeks):
            v = e[(e.depot == d) & (e.day >= w0) & (e.day <= w0 + dt.timedelta(days=6))].h.sum()
            same("A %s week %d" % (d, i + 1), int(math.floor(v + 0.5)), fig["hours_on_service"][d][i])
    # ---- ask C: kilometres in service by depot and month
    ret = pd.read_csv(os.path.join(TARGET, "service_return_2025-10_2026-10.csv"), sep=";", dtype=str)
    ret["day"] = pd.to_datetime(ret.fecha, format="%d/%m/%Y").dt.date
    ret = ret[(ret.day >= dt.date(2026, 7, 1)) & (ret.day <= dt.date(2026, 10, 31))].copy()
    km = ret.km_realizados.str.replace(",", ".").astype(float)
    km = np.where(ret.linea.isin(["40", "41", "44", "46"]), km / 1000.0, km)
    ret["km"] = km
    lines = {"San Lázaro": "1 3 7 9 N1", "Hornacho": "12 14 27 33 N2", "Valdeolmos": "40 41 44 46 N3",
             "El Quiñón": "5 16 21 N4", "Las Tenerías": "2 8 19 23 25 N5", "La Ribera": "4 10 17 29 N6",
             "Santa Clara": "6 11 31 35 N7"}
    l2d = {ln: d for d, s in lines.items() for ln in s.split()}
    ret["depot"] = ret.linea.map(l2d)
    ret["op"] = ret.expediciones_realizadas.astype(int)
    dv = pd.read_csv(os.path.join(TARGET, "mobility_diversions_register_2026.csv"), sep=";", dtype=str)
    extra = np.zeros(len(ret))
    rk = ret.reset_index(drop=True)
    for r in dv.itertuples():
        a = dt.datetime.strptime(r.desde, "%d/%m/%Y").date()
        b = dt.datetime.strptime(r.hasta, "%d/%m/%Y").date()
        m = (rk.linea.isin(r.lineas.split("/")) & rk.sentido.isin(r.sentidos.split("/")) & (rk.day >= a) & (rk.day <= b))
        extra += np.where(m, rk.op * float(r.km_por_expedicion.replace(",", ".")), 0.0)
    rk["km"] = rk.km + extra
    rk["month"] = [d.month for d in rk.day]
    for d in DEPOTS:
        for i, m in enumerate([7, 8, 9, 10]):
            v = rk[(rk.depot == d) & (rk.month == m)].km.sum()
            same("C %s month %d" % (d, m), int(math.floor(v + 0.5)), fig["kilometres_in_service"][d][i])
    # ---- ask B: at-fault collisions and claims paid
    inc = pd.read_excel(os.path.join(TARGET, "incident_register_2026.xlsx"), dtype=str)
    inc["t"] = pd.to_datetime(inc.fecha + " " + inc.hora_local, format="%d/%m/%Y %H:%M")
    inc = inc.sort_values(["coche", "t"]).reset_index(drop=True)
    keep = []
    last = None
    for r in inc.itertuples():
        if last is not None and last.coche == r.coche and last.culpa == r.culpa and \
                abs((r.t - last.t).total_seconds()) <= 1200:
            continue
        keep.append(r.Index)
        last = r
    inc = inc.loc[keep].copy()
    inc["day"] = inc.t.dt.date
    inc["depot"] = [next(dep for a, b, dep in amap[f] if a <= d <= b) for f, d in zip(inc.coche, inc.day)]
    regs = pd.read_excel(os.path.join(TARGET, "fleet_register_2026.xlsx"), sheet_name="Registrations", dtype=str)
    p2f = dict(zip(regs.plate, regs.fleet_no))
    bd = pd.read_csv(os.path.join(TARGET, "insurer_bordereau_2026-01_2026-10.csv"), dtype=str, keep_default_na=False)
    bd = bd[bd.snapshot == "2026-10-31"].copy()
    bd = bd[~bd.claim_no.isin(set(bd.reopened_from) - {""})]
    bd["fleet"] = bd.vehicle_plate.map(p2f)
    bd["it"] = pd.to_datetime(bd.incident_date + " " + bd.incident_time_local)
    paid = {}
    for r in bd.itertuples():
        c = inc[(inc.coche == r.fleet) & (inc.day == r.it.date())]
        if not len(c):
            continue
        j = (c.t - r.it).abs().idxmin()
        paid[j] = paid.get(j, 0.0) + float(r.paid_to_date_eur)
    inc["paid"] = [paid.get(i, 0.0) for i in inc.index]
    af = inc[inc.culpa.isin(["A", "C"])]
    for d in DEPOTS:
        g = af[af.depot == d]
        same("B %s at-fault collisions" % d, int(len(g)), fig["at_fault_collisions"][d])
        same("B %s claims paid" % d, int(math.floor(g.paid.sum() + 0.5)), fig["claims_paid_eur"][d])
    print("verify: %d figures agree, %d differ" % (len(OK), len(BAD)))
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
