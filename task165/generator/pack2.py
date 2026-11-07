"""task165 pack, part 2: the storm log, the transit agency's street list, the fleet, the yards' own records, the
contractor's returns, the distractors, the data dictionary and the export manifest; build_pack writes everything."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

import common as K
import docs as D
import pack as P
import postprocess as PP
import records as R
import world as Wd
import yards as Y

BOLD = Font(bold=True)
HEAD_FILL = PatternFill("solid", fgColor="DCE6F1")


def _sheet(ws, head, rows, widths=None, fmt=None, start=1):
    if start > 1:
        pass
    ws.append(head)
    for c in ws[ws.max_row]:
        c.font = BOLD
        c.fill = HEAD_FILL
    hdr_row = ws.max_row
    for r in rows:
        ws.append(list(r))
    for i, h in enumerate(head):
        ws.column_dimensions[get_column_letter(i + 1)].width = (widths[i] if widths else max(10, len(h) + 2))
    ws.freeze_panes = "A%d" % (hdr_row + 1)
    if fmt:
        for col, nf in fmt.items():
            for cell in ws[col][hdr_row:]:
                cell.number_format = nf


# ------------------------------------------------------------------------------------------------------ storm log
def write_storm(out, W):
    path = os.path.join(out, P.F_STORM)
    wb = Workbook()
    first = True
    for w in K.WINTERS:
        ws = wb.active if first else wb.create_sheet(w)
        if first:
            ws.title = w
            first = False
        evs = W.events[w]
        if w in K.LEGACY_WINTERS:
            ws.append(["Roads Operations Centre: winter event log %s" % w])
            ws["A1"].font = BOLD
            ws.append(["Exported from the incident board, %s" % ("15 April 2022" if w == "2021-22" else "12 April 2023")])
            ws.append([])
            rows = []
            for e in evs:
                rows.append((e["event_no"], e["start"].strftime("%Y-%m-%d %H:%M"), e["end"].strftime("%Y-%m-%d %H:%M"),
                             {"SN": "Snow", "FZ": "Freezing rain", "MX": "Mixed", "IC": "Ice / frost"}[e["type"]],
                             e["snow_cm"], e["fzra_mm"], e["points"]))
            _sheet(ws, ["Event", "Declared", "Stood down", "Type", "Snow cm", "FZRA mm", "Points"], rows,
                   [8, 17, 17, 14, 9, 9, 8])
        else:
            rows = []
            for e in evs:
                rows.append(("%s-%03d" % (w[2:4], e["event_no"]), e["start"], e["end"], e["type"], e["snow_cm"],
                             e["fzra_mm"], e["min_pave_c"], e["points"]))
            _sheet(ws, ["event_id", "declared_local", "stood_down_local", "event_type", "snow_cm", "fzra_mm",
                        "min_pavement_c", "wsi_points"], rows, [10, 18, 18, 11, 9, 9, 14, 11],
                   fmt={"B": "yyyy-mm-dd hh:mm", "C": "yyyy-mm-dd hh:mm"})
            ws.append([])
            ws.append(["Season WSI", None, None, None, None, None, None, round(sum(e["points"] for e in evs), 1)])
    ws = wb.create_sheet("Codes")
    for line in (["event_type", "SN snow, FZ freezing rain, MX mixed, IC ice or frost"],
                 ["Points", "Event points scored when the event is stood down (RO-OP-03)."],
                 ["Times", "Local time."]):
        ws.append(line)
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 80
    wb.save(path)
    PP.normalize_ooxml(path, "Roads Operations Centre", K.PEOPLE["winter_manager"], "2022-04-15T13:20:00Z",
                       "2026-04-09T15:42:00Z", excel=True, company=K.ORG)
    return sum(len(W.events[w]) for w in K.WINTERS)


# ------------------------------------------------------------------------------------------------------ QRT street list
def write_qrt(out, W):
    path = os.path.join(out, P.F_QRT)
    tags = P.transit_tags(W)
    by_st = {}
    for s in W.segments:
        if s["pool"] == "NEW":
            by_st.setdefault(s["street"], []).append(s)
    rows = []
    for st, ss in sorted(by_st.items()):
        rt = tags[ss[0]["segment_id"]]
        rows.append((rt, st, ss[0]["from_street"], ss[-1]["to_street"], "Both", "10 to 15 min",
                     round(sum(s["centreline_km"] for s in ss), 2)))
    rows.sort(key=lambda r: (int(r[0].split(",")[0]), r[1]))
    wb = Workbook()
    ws = wb.active
    ws.title = "Frequent streets"
    ws.append(["Quellbrook Regional Transit: frequent network 2026, streets newly on the frequent network"])
    ws["A1"].font = BOLD
    ws.append(["Service Planning, for the City of Quellbrook Roads Division route audit. Contact: %s."
               % K.PEOPLE["transit_planner"]])
    ws.append([])
    _sheet(ws, ["Route(s)", "Street", "From", "To", "Direction", "Weekday headway", "Street km"], rows,
           [10, 26, 26, 26, 10, 16, 10])
    wb.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["transit_planner"], K.PEOPLE["transit_planner"], "2026-06-22T14:10:00Z",
                       "2026-08-11T19:35:00Z", excel=True, company=K.TRANSIT)
    return len(rows)


# ------------------------------------------------------------------------------------------------------ yards
def write_scale(out, Yd):
    path = os.path.join(out, P.F_SCALE)
    wb = Workbook()
    first = True
    for y in K.YARDS:
        ws = wb.active if first else wb.create_sheet(y)
        if first:
            ws.title = y
            first = False
        rows = Yd.scale_sheet(y)
        _sheet(ws, ["Ticket", "Date", "Time in", "Time out", "Direction", "Carrier", "Vehicle", "Supplier ticket",
                    "Material", "Gross kg", "Tare kg", "Net kg", "Remarks"], rows,
               [13, 11, 8, 8, 9, 22, 13, 14, 11, 10, 9, 9, 18], fmt={"B": "yyyy-mm-dd"})
    wb.save(path)
    PP.normalize_ooxml(path, "Scale house", "Scale house", "2026-08-24T10:30:00Z", "2026-09-25T12:50:00Z",
                       excel=True, company=K.ORG)
    return sum(len(Yd.scale_sheet(y)) for y in K.YARDS)


def write_domes(out):
    rows = [("KLV", "KLV-D1", "%.0f" % Y.CAPACITY["KLV"], "2004", "", "Fabric-roof dome on concrete push walls"),
            ("MPF", "MPF-D1", "%.0f" % Y.CAPACITY["MPF"], "2011", "", "Timber dome"),
            ("RDG", "RDG-D1", "%.0f" % Y.CAPACITY["RDG"], "1998", "2017", "Timber dome, walls raised 2017"),
            ("LKS", "LKS-D2", "%.0f" % Y.CAPACITY["LKS"], "2026", "", "Replaces LKS-D1 (demolished November 2025)")]
    P._csv(os.path.join(out, P.F_DOMES), ["yard", "dome", "rated_capacity_t", "built", "upgraded", "notes"], rows)
    return len(rows)


def write_dispatch(out, Yd):
    head = ["delivery_date", "ship_to", "trailer", "planned_net_t", "booking_ref", "status"]
    P._csv(os.path.join(out, P.F_DISPATCH1), head, Yd.dispatch_rows(1))
    P._csv(os.path.join(out, P.F_DISPATCH2), head, Yd.dispatch_rows(2))
    return len(Yd.dispatch[2])


def write_pellard(out, W, S):
    path = os.path.join(out, P.F_PELLARD)
    ret = Y.contractor_returns(W, S)
    wb = Workbook()
    first = True
    names = {rc: "KRS-%d" % (i + 1) for i, rc in enumerate(sorted(W.contract_circuits))}
    lk = {rc: sum(W.by_id[sid]["lane_km"] for sid in W.circuits[rc]["segments"]) for rc in W.contract_circuits}
    for w in K.NEW_WINTERS:
        ws = wb.active if first else wb.create_sheet(w)
        if first:
            ws.title = w
            first = False
        ws.append(["Kettlewood Road Services: material returns, contract RW-2023-07, winter %s" % w])
        ws["A1"].font = BOLD
        ws.append([])
        rows = []
        for (ww, m, rc), t in sorted(ret.items()):
            if ww != w:
                continue
            rows.append((m, names[rc], rc, round(lk[rc], 2), round(t, 1)))
        _sheet(ws, ["Month", "Route", "City circuit", "Lane km", "Rock salt (t)"], rows, [10, 8, 12, 9, 13])
    wb.save(path)
    PP.normalize_ooxml(path, "Kettlewood Road Services", "Kettlewood Road Services", "2024-04-08T13:00:00Z",
                       "2026-04-10T16:15:00Z", excel=True, company="Kettlewood Road Services")
    return sum(1 for k in ret)


def write_fleet(out, W):
    rows = P.fleet_rows(W)
    P._csv(os.path.join(out, P.F_FLEET), ["unit_id", "yard", "class", "home_circuit", "model_year"], rows)
    return len(rows)


def write_work_orders(out, W, S):
    rows = Y.work_orders(W, S)
    P._csv(os.path.join(out, P.F_WORKORDERS), ["work_order", "unit_id", "opened", "closed", "system", "description",
                                               "labour_hours", "parts_cost"], rows)
    return len(rows)


# ------------------------------------------------------------------------------------------------------ distractors
def write_timesheets(out, W, S):
    rng = np.random.default_rng(W.seed + 50)
    emp = {u["unit_id"]: "E%05d" % (30400 + 17 * i) for i, u in enumerate(W.units)}
    per = {}
    for p in S.passes:
        if p["winter"] != "2025-26" or p["contract"] or not p["rows"]:
            continue
        t = p["rows"][0]["entry"]
        sd = t.date() if t.hour >= 7 else t.date() - dt.timedelta(days=1)
        sh = "DAY" if 7 <= t.hour < 19 else "NIGHT"
        per[(p["unit"], sd, sh)] = per.get((p["unit"], sd, sh), 0.0) + \
            sum((r["exit"] - r["entry"]).total_seconds() for r in p["rows"]) / 3600.0
    rows = []
    for (unit, sd, sh), h in sorted(per.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[0][0])):
        u = W.unit_by_id[unit]
        reg = min(12.0, max(4.0, round((h * 1.9 + float(rng.uniform(1.5, 3.0))) * 4) / 4))
        ot = max(0.0, round((h * 1.9 + 2.5 - 12.0) * 4) / 4)
        rows.append((u["yard"], sd.isoformat(), sh, emp[unit], unit, "%.2f" % reg, "%.2f" % ot))
    P._csv(os.path.join(out, P.F_TIMESHEETS), ["yard", "shift_date", "shift", "employee", "unit_id", "regular_hours",
                                               "overtime_hours"], rows)
    return len(rows)


def write_brine(out, W):
    rng = np.random.default_rng(W.seed + 51)
    rows = []
    for w in K.NEW_WINTERS:
        a, b = K.SEASON[w]
        evdays = sorted({e["start"].date() for e in W.events[w]})
        for d in evdays:
            for y in K.YARDS:
                if rng.random() < 0.55:
                    lit = int(rng.integers(8, 30)) * 1000
                    rows.append((y, (d - dt.timedelta(days=1)).isoformat(), lit, "%.1f" % float(rng.normal(23.2, 0.3))))
    rows.sort()
    P._csv(os.path.join(out, P.F_BRINE), ["yard", "production_date", "brine_litres", "salinity_pct"], rows)
    return len(rows)


# ------------------------------------------------------------------------------------------------------ edges
def _local(utc):
    return K.to_local(utc)


def arterial_cells(W, S, pr):
    """Each yard's Priority 1 arterial rock salt in each of the three winters, from the pass rows as written (run
    totals once, the older controllers' brine taken off) and the contractor's returns as rounded."""
    tot, seen = {}, set()
    for r in pr:
        if "-A" not in r["route_code"] or r["material_code"] != "RS":
            continue
        w = K.winter_of(_local(r["entry_utc"]).date())
        if w not in K.NEW_WINTERS:
            continue
        key = (r["route_code"][:3], w)
        ctl = W.controller_on(r["unit_id"], _local(r["entry_utc"]).date())
        if ctl == "M410":
            if r["run_ref"] in seen:
                continue
            seen.add(r["run_ref"])
            v = r["applied_t"] - r["prewet_l"] * P.BRINE_KG_L / 1000.0
        else:
            v = r["applied_t"]
        tot[key] = tot.get(key, 0.0) + v
    for (w, m, rc), t in Y.contractor_returns(W, S).items():
        tot[(rc[:3], w)] = tot.get((rc[:3], w), 0.0) + round(t, 1)
    return tot


ART_UNIT = 50.0     # the arterial figures are asked to the nearest 50 t
ART_EDGE = 16.0     # each route's figure at least this far from a 50 t rounding edge (a quarter bin is 12.5 t)


def loader_cells(W, S, pr):
    """The loading-log calibration of the same cells: each older-controller unit's winter taken at the tonnes the yard's
    loader scale put into it, every other arterial row as the platform wrote it, the contractor's returns added."""
    lt = {}
    for (yard, sd, sh, unit, loads, tl) in Y.loading_log(W, S, np.random.default_rng(W.seed + 42)):
        w = K.winter_of(dt.date.fromisoformat(sd))
        if w in K.NEW_WINTERS:
            lt[(unit, w)] = lt.get((unit, w), 0.0) + float(tl)
    tot, old = {}, set()
    for r in pr:
        if "-A" not in r["route_code"] or r["material_code"] != "RS":
            continue
        day = _local(r["entry_utc"]).date()
        w = K.winter_of(day)
        if w not in K.NEW_WINTERS:
            continue
        if W.controller_on(r["unit_id"], day) == "M410":
            old.add((r["unit_id"], w))
            continue
        key = (r["route_code"][:3], w)
        tot[key] = tot.get(key, 0.0) + r["applied_t"]
    for u, w in old:
        key = (W.unit_by_id[u]["yard"], w)
        tot[key] = tot.get(key, 0.0) + lt.get((u, w), 0.0)
    for (w, m, rc), t in Y.contractor_returns(W, S).items():
        tot[(rc[:3], w)] = tot.get((rc[:3], w), 0.0) + round(t, 1)
    return tot


def _cell_safe(a, b):
    return round(a / ART_UNIT) == round(b / ART_UNIT) and \
        min(K.bin_edge_distance(a, ART_UNIT), K.bin_edge_distance(b, ART_UNIT)) >= ART_EDGE


def settle_arterial_cells(W, S):
    """Keep every yard-winter arterial figure, as the records give it and as the loading-log calibration gives it, in
    one 50 t cell at least ART_EDGE from its edges: where a cell sits closer, the City trucks' newer-controller passes
    of that yard and winter share the difference in proportion (a fraction of a per cent of each), on the simulated
    truth itself, so the platform rows, the loader log and every total follow. Returns the pass rows."""
    for _ in range(3):
        pr = P.pass_rows(W, S)
        g, c = arterial_cells(W, S, pr), loader_cells(W, S, pr)
        bad = [k for k in sorted(g) if not _cell_safe(g[k], c[k])]
        if not bad:
            return pr
        for key in bad:
            mid = (g[key] + c[key]) / 2.0
            target = round(mid / ART_UNIT) * ART_UNIT + (K.stable_int(key[0], key[1], "cell") % 11 - 5)
            ps_ = [p for p in S.passes if p["kind"] == "ART" and not p["contract"] and p["winter"] == key[1]
                   and p["route_code"][:3] == key[0] and p["rows"]
                   and W.controller_on(p["unit"], p["rows"][0]["entry"].date()) == "M720"]
            base = sum(r["t"] for p in ps_ for r in p["rows"])
            f = 1.0 + (target - mid) / base
            for p in ps_:
                for r in p["rows"]:
                    r["t"] *= f
        S.truth = {}
        for p in S.passes:
            for r in p["rows"]:
                k_ = (r["segment_id"], p["winter"])
                S.truth[k_] = S.truth.get(k_, 0.0) + r["t"]
    pr = P.pass_rows(W, S)
    g, c = arterial_cells(W, S, pr), loader_cells(W, S, pr)
    assert all(_cell_safe(g[k], c[k]) for k in g), {k: (round(g[k], 1), round(c[k], 1)) for k in g}
    return pr


def settle_dome_edges(Yd):
    """Keep each dome's stock at least 0.03 t from a one-decimal edge: the yard's last supplier load after its survey
    is read 20 kg heavier or lighter at the scale where it sits closer."""
    for _ in range(3):
        Yd._stock_truth()
        for y in K.YARDS:
            v = Yd.stock[y]
            if K.bin_edge_distance(v, 0.1) >= 0.0295:
                continue
            cut = Yd.capture_end(y)
            loads = [r for r in Yd.loads if r["to"] == y and r["dir"] == "IN" and r["kind"] == "SUPPLIER"
                     and r["in"] > cut]
            r = loads[-1]
            r["gross_kg"] += 20
            r["net_kg"] += 20
    Yd._stock_truth()
    assert all(K.bin_edge_distance(v, 0.1) >= 0.0295 for v in Yd.stock.values()), Yd.stock


# ------------------------------------------------------------------------------------------------------ build
def build_pack(out, W=None, S=None):
    os.makedirs(out, exist_ok=True)
    W = W or Wd.World()
    S = S or R.Sim(W)
    pr = settle_arterial_cells(W, S)
    Yd = Y.Yards(W, S)
    n = {}
    lr = P.legacy_rows(W, S)
    P._csv(os.path.join(out, P.F_LEGACY), ["SHIFT_DATE", "SHIFT", "YARD", "ROUTE", "SEG_ID", "PASSES", "MATL", "KG"], lr)
    n[P.F_LEGACY] = len(lr)
    settle_dome_edges(Yd)
    Yd.add_changeover_weighings()
    Yd.assign_trucks()
    P.write_passes(os.path.join(out, P.F_PASSES), P.rekey_rows(W, pr))
    n[P.F_PASSES] = len(pr)
    rr = P.register_rows(W)
    P._csv(os.path.join(out, P.F_REGISTER), ["segment_id", "street", "from_street", "to_street", "yard", "route_code",
                                             "func_class", "priority", "lanes", "centreline_km", "lane_km",
                                             "frequent_transit", "operator", "last_audit"], rr)
    n[P.F_REGISTER] = len(rr)
    rv = P.revision_rows(W)
    P._csv(os.path.join(out, P.F_REVLOG), ["change_no", "effective_date", "segment_id", "field", "old_value",
                                           "new_value", "reason", "entered_by", "entered_on"], rv)
    n[P.F_REVLOG] = len(rv)
    xw = P.crosswalk_rows(W)
    P._csv(os.path.join(out, P.F_XWALK), ["legacy_segment_id", "segment_id", "length_share", "change", "gis_release"], xw)
    n[P.F_XWALK] = len(xw)
    n[P.F_STORM] = write_storm(out, W)
    n[P.F_QRT] = write_qrt(out, W)
    n[P.F_SCALE] = write_scale(out, Yd)
    n[P.F_DOMES] = write_domes(out)
    n[P.F_DISPATCH2] = write_dispatch(out, Yd)
    n[P.F_DISPATCH1] = len(Yd.dispatch[1])
    n[P.F_PELLARD] = write_pellard(out, W, S)
    n[P.F_FLEET] = write_fleet(out, W)
    n[P.F_WORKORDERS] = write_work_orders(out, W, S)
    n[P.F_TIMESHEETS] = write_timesheets(out, W, S)
    n[P.F_BRINE] = write_brine(out, W)
    D.write_plan(out, W)
    D.write_procedure(out)
    D.write_survey(out)
    return n, W, S, Yd
