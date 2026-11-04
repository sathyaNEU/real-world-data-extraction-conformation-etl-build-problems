"""The pack's exports, each in the form its producing system writes it."""
import csv
import datetime as dt
import io
import json
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import postprocess as PP
import staffing as S
import world as W

PATHS = {
    "log": "control_system/roc_signaller_actions_20251001_20260930.csv",
    "reg25": "incidents/operating_incident_register_2025-26.xlsx",
    "reg26": "incidents/operating_incident_register_2026-27.xlsx",
    "delay": "delay_attribution/ocf_delay_records_2025-04_2026-09.csv",
    "reviews": "delay_attribution/attribution_reviews_2025-26_2026-27.csv",
    "layout": "control_system/workstation_layout_export_r8.2.1.json",
    "ros25": "staffing/signalling_roster_2025-26_P07-P13.xlsx",
    "ros26": "staffing/signalling_roster_2026-27_P01-P07.xlsx",
    "changes": "staffing/roster_changes_2025-26_2026-27.csv",
    "comp": "staffing/signaller_competence_register.xlsx",
    "ars": "control_system/ars_status_log_20251001_20260930.csv",
    "adhesion": "reference/railhead_adhesion_reports_autumn_2025.csv",
    "tor": "governance/2027_improvement_plan_terms_of_reference.pdf",
    "catalogue": "governance/improvement_catalogue_2027.docx",
    "workload": "reference/fenmoor_roc_workload_assessment_2025.pdf",
}

LOCATION_CODE = {
    "Fenmoor North Jn": "FENMRNJ", "Fenmoor station": "FENMOOR", "Fenmoor South Jn": "FENMRSJ",
    "Brackle Lane Jn": "BRKLLNJ", "Fenmoor Up Sidings": "FENMUSD", "Callowby Jn": "CALWBJN", "Callowby station": "CALWBY",
    "Pellow Loop": "PELWLP", "Ingham Road Jn": "INGHRDJ", "Hatherby West Jn": "HTHRWJN", "Hatherby station": "HATHRBY",
    "Hatherby East Jn": "HTHREJN", "Sowley Jn": "SOWLYJN", "Hatherby Down Loop": "HTHRDLP", "Tollinghurst Jn": "TLNGHJN",
    "Tollinghurst station": "TLNGHST", "Marrick Lane": "MRRCKLN", "Coldharbour Jn": "CLDHBJN", "Kestrow Jn": "KESTWJN",
    "Kestrow Yard": "KESTWYD", "Kestrow station": "KESTROW", "Thornbury Lane": "THRNBLN", "Wellanby Jn": "WLNBYJN",
    "Wellanby station": "WELLNBY", "Sellack Loop": "SELLKLP", "Ravenhurst Jn": "RVNHSTJ"}

OLD_CATEGORY = {"RS1": "Wrong route", "RS2": "Late route setting", "RS3": "Route not set", "RG1": "Regulating",
                "CM1": "Communication", "AR1": "ARS", "EQ1": "Workstation fault"}
NEW_CATEGORY = {"RS1": "Route setting - wrong route set", "RS2": "Route setting - route set late",
                "RS3": "Route setting - route not set", "RG1": "Regulating decision", "CM1": "Communication with driver",
                "AR1": "ARS routing", "EQ1": "Workstation equipment"}
OLD_FINDING = {"competence": "Competence", "distraction": "Attention / distraction", "workload": "Workload",
               "fatigue": "Fatigue", "ars": "ARS data", "equipment": "Equipment", "not determined": "Not determined"}
REASON = {"RS1": "OW", "RS2": "OL", "RS3": "OM", "RG1": "OR", "CM1": "OX", "AR1": "OA", "EQ1": "OE"}
STAMP = dict(created="2026-10-09T07:52:11Z", modified="2026-10-09T07:52:11Z")


def path(target, key):
    return os.path.join(target, PATHS[key])


def ensure(p):
    os.makedirs(os.path.dirname(p), exist_ok=True)


def write_csv(p, header, rows, newline="\r\n"):
    ensure(p)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator=newline)
    w.writerow(header)
    for row in rows:
        w.writerow(row)
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())


def xlsx_save(wb, p, creator, last_by, created, modified, title=None, company=None):
    ensure(p)
    wb.save(p)
    PP.normalize_ooxml(p, creator, last_by, created, modified, title=title, excel=True, company=company)


def header_row(ws, row, values, fill="DDE4EE"):
    for c, v in enumerate(values, start=1):
        cell = ws.cell(row=row, column=c, value=v)
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor=fill)
        cell.alignment = Alignment(vertical="top", wrap_text=True)


def iso_ms(t):
    return t.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (t.microsecond // 1000)


def ws_label(ws, t_utc, server):
    """The control system names a workstation by its desk until it takes release 8.2, by number after."""
    switch = W.RELEASE_A if server == "ROC-A" else W.RELEASE_B
    return ws if t_utc >= switch else W.DESK[ws]


def in_export(t):
    return W.local_to_utc(dt.datetime(2025, 10, 1)) <= t < W.local_to_utc(dt.datetime(2026, 10, 1))


# ------------------------------------------------------------------------------------------- control system log

def write_log(target, events, fails):
    """The signaller action log as the control system exports it: UTC to the millisecond, the active server,
    and through each server change both servers' copies of the minutes they overlapped."""
    r = W.rng(40)
    rows = []
    windows = []
    for f in fails:
        windows.append((f["a_down"] - dt.timedelta(seconds=float(r.uniform(60, 190))), f["a_down"]))
        windows.append((f["a_up"], f["a_up"] + dt.timedelta(seconds=float(r.uniform(60, 190)))))
    down = [(f["a_down"], f["a_up"]) for f in fails]
    for t, ws, user, act, ent, ex, rid, hc in events:
        if not in_export(t):
            continue
        srv = "ROC-B" if any(a <= t < b for a, b in down) else "ROC-A"
        rows.append((t, srv, ws, user, act, ent, ex, rid, hc))
        if any(a <= t < b for a, b in windows):
            other = "ROC-A" if srv == "ROC-B" else "ROC-B"
            rows.append((t + dt.timedelta(milliseconds=float(r.uniform(4, 61))), other, ws, user, act, ent, ex, rid, hc))
    rows.sort(key=lambda x: (x[0], x[1]))
    out = [(iso_ms(t), srv, ws_label(ws, t, srv), user, act, ent, ex, rid, hc) for t, srv, ws, user, act, ent, ex, rid, hc in rows]
    write_csv(path(target, "log"), ["event_utc", "server", "wkstn", "user", "action", "entrance", "exit", "route_id",
                                    "headcode"], out, newline="\n")
    return len(out)


# ---------------------------------------------------------------------------------------------- registers

def exit_line(net):
    r = W.rng(41)
    names = ["Up Main", "Down Main", "Up Relief", "Down Relief", "Up Slow", "Down Slow", "Platform 1", "Platform 2",
             "Platform 3", "Platform 4", "the Loop", "the Branch", "the Sidings", "the Goods Line"]
    lab = {}
    for rt in net["routes"]:
        lab[rt["route_id"]] = names[int(r.integers(0, len(names)))]
    return lab


def route_text(net, rid, style):
    rt = net["rmap"][rid]
    if style == 0:
        return "%s to %s" % (rt["entrance"], rt["exit"])
    if style == 1:
        return "%s-%s" % (rt["entrance"], rt["exit"])
    return rid


def narrative(r, inc, net, lab, minutes):
    typ = inc["type"]
    hc = inc["headcode"]
    jn = inc["junction"]
    if typ in ("RS1", "AR1"):
        a, b = lab[inc["route_set"]], lab[inc["route_required"]]
        who = "ARS set the route" if typ == "AR1" else r.choice(["Signaller set the route", "Route set by signaller",
                                                                  "Signaller routed the train"])
        lead = "%s for %s towards %s at %s; required %s." % (who, hc, a, jn, b)
        tail = r.choice(["Driver stopped short and reported. Route reset after %d min." % int(r.integers(4, 19)),
                         "Train ran onto %s and was brought back. %d min to recover." % (a, int(r.integers(9, 31))),
                         "Driver queried the route at the signal; train held, route corrected.",
                         "Train stopped at the next signal and routed back over the crossover."])
        return lead + " " + tail
    if typ == "RS2":
        return ("%s checked at %s; route set late. %s" % (hc, jn, r.choice(
            ["Other moves being dealt with.", "Signaller dealing with a possession handback.", "Telephone call in progress.",
             "Late running of a preceding service.", ""]))).strip()
    if typ == "RS3":
        return ("%s stood at %s; route not set until driver called. %s" % (hc, jn, r.choice(
            ["Signaller missed the train on the describer.", "No ARS in the area at the time.", "Overlooked during handback.",
             ""]))).strip()
    if typ == "RG1":
        return ("%s allowed out ahead of %s at %s; following service delayed. %s" % (
            hc, r.choice(["the stopper", "a late-running express", "the freight", "the ECS move"]), jn,
            r.choice(["Regulating policy not applied.", "Decision taken on the information available.", ""]))).strip()
    if typ == "CM1":
        return "%s given an incorrect instruction at %s. %s" % (hc, jn, r.choice(
            ["Message repeated and corrected.", "Driver challenged and clarified.", "Delay while instruction confirmed."]))
    where = ("Workstation %s" % inc["ws"]) if inc["utc"] >= W.RELEASE_A else ("%s desk" % W.DESK[inc["ws"]].title())
    return "%s %s; %s. %s" % (where, r.choice(["screens froze", "display lost on two screens",
                                               "changed over to the standby display"]),
                                       r.choice(["trains held while display restored", "routes set from the standby",
                                                 "fault logged with the maintainer"]),
                                       "Delay to %s and following trains." % hc)


def register_rows(incidents, fy):
    lst = [i for i in incidents if W.railway_period(W.utc_to_local(i["utc"]).date())[0] == fy]
    return sorted(lst, key=lambda i: i["ref"])


def write_registers(target, incidents, net):
    lab = exit_line(net)
    r = W.rng(42)
    # FY2025/26, the register as kept until 31 March 2026
    wb = openpyxl.Workbook()
    sh = wb.active
    sh.title = "Register 2025-26"
    head = ["Ref", "Incident date", "Time", "Desk", "Signaller", "Location", "Category", "Train", "Route set", "Route required",
            "TRUST", "Initial delay (mins)", "LI", "Finding", "LI closed", "Summary"]
    header_row(sh, 1, head)
    row = 2
    for inc in register_rows(incidents, 2025):
        loc = W.utc_to_local(inc["utc"])
        style = int(r.choice([0, 0, 1, 2], p=[0.45, 0.2, 0.2, 0.15]))
        init = inc.get("initial", 0)
        vals = [inc["ref"], loc.date(), loc.strftime("%H:%M"), W.DESK[inc["ws"]], inc["staff_no"],
                inc["junction"], OLD_CATEGORY[inc["type"]], inc["headcode"],
                route_text(net, inc["route_set"], style) if inc["route_set"] else "",
                route_text(net, inc["route_required"], style) if inc["route_required"] else "",
                inc["trust"] if inc.get("trust") else "", init, inc["li"], OLD_FINDING[inc["finding"]],
                inc["li_closed"], inc["summary"]]
        for c, v in enumerate(vals, start=1):
            cell = sh.cell(row=row, column=c, value=(None if v == "" else v))
            if c == 2 or c == 15:
                cell.number_format = "dd/mm/yyyy"
        row += 1
    for c, w in zip("ABCDEFGHIJKLMNOP", (13, 11, 7, 13, 10, 20, 18, 7, 16, 16, 9, 11, 10, 20, 11, 70)):
        sh.column_dimensions[c].width = w
    sh.freeze_panes = "B2"
    xlsx_save(wb, path(target, "reg25"), "Helen Douglas", "Helen Douglas", "2025-04-02T08:11:42Z",
              "2026-04-08T15:27:03Z", title="Operating incident register 2025-26")
    # FY2026/27, kept in the new incident tool's layout from 1 April 2026
    wb = openpyxl.Workbook()
    sh = wb.active
    sh.title = "Register"
    head = ["Incident ref", "Occurred", "Workstation", "Staff no", "Location", "Category code", "Headcode", "Route set",
            "Route required", "TRUST incident", "Initial delay", "Investigation ref", "Underlying cause", "Closed",
            "Narrative"]
    header_row(sh, 1, head)
    row = 2
    for inc in register_rows(incidents, 2026):
        loc = W.utc_to_local(inc["utc"])
        vals = [inc["ref"], loc.replace(second=0, microsecond=0), "%s %s" % (inc["ws"], W.DESK[inc["ws"]].title()),
                inc["staff_no"], inc["junction"], inc["type"], inc["headcode"], inc["route_set"] or "",
                inc["route_required"] or "", inc["trust"] if inc.get("trust") else "", inc.get("initial", 0), inc["li"],
                inc["finding26"], inc["li_closed"], inc["summary"]]
        for c, v in enumerate(vals, start=1):
            cell = sh.cell(row=row, column=c, value=(None if v == "" else v))
            if c == 2:
                cell.number_format = "yyyy-mm-dd hh:mm"
            if c == 14:
                cell.number_format = "yyyy-mm-dd"
        row += 1
    for c, w in zip("ABCDEFGHIJKLMNO", (13, 16, 16, 9, 20, 9, 9, 10, 12, 10, 9, 12, 24, 11, 70)):
        sh.column_dimensions[c].width = w
    sh.freeze_panes = "A2"
    codes = wb.create_sheet("Category codes")
    header_row(codes, 1, ["Code", "Category", "2025-26 register category"])
    for k, code in enumerate(("RS1", "RS2", "RS3", "RG1", "CM1", "AR1", "EQ1"), start=2):
        for c, v in enumerate((code, NEW_CATEGORY[code], OLD_CATEGORY[code]), start=1):
            codes.cell(row=k, column=c, value=v)
    codes.column_dimensions["A"].width = 7
    codes.column_dimensions["B"].width = 34
    codes.column_dimensions["C"].width = 26
    xlsx_save(wb, path(target, "reg26"), "Helen Douglas", "Helen Douglas", "2026-04-01T07:40:15Z",
              "2026-10-07T16:02:48Z", title="Operating incident register 2026-27")


# --------------------------------------------------------------------------------------------- delay records

def write_delay(target, incidents, moves):
    rows = []
    for inc in sorted(incidents, key=lambda i: i["trust"]):
        if not inc.get("trust"):
            continue
        loc = W.utc_to_local(inc["utc"])
        for hc, ev, m in inc["delay_records"]:
            rows.append((inc["trust"], loc.strftime("%d/%m/%Y %H:%M"), W.period_label(loc.date()), "OCF",
                         REASON[inc["type"]], hc, loc.strftime("%d/%m/%Y"), LOCATION_CODE[inc["junction"]], ev, m))
    write_csv(path(target, "delay"), ["trust_incident", "incident_start", "fin_period", "resp", "reason", "train_id",
                                      "train_date", "location", "delay_type", "pfpi_minutes"], rows)
    rv = []
    r = W.rng(43)
    for mv in sorted(moves, key=lambda m: m["ref"]):
        inc = mv["inc"]
        loc = W.utc_to_local(inc["utc"])
        frm, to = (inc["trust"], mv["other"]) if mv["out"] else (mv["other"], inc["trust"])
        rv.append((mv["ref"], mv["agreed"].strftime("%d/%m/%Y") if mv["agreed"] else "", frm, to, mv["headcode"],
                   loc.strftime("%d/%m/%Y"), mv["minutes"], mv["status"]))
    write_csv(path(target, "reviews"), ["review_ref", "decided", "from_incident", "to_incident", "train_id",
                                        "train_date", "pfpi_minutes", "status"], rv)
    return len(rows), len(rv)


# --------------------------------------------------------------------------------------------- layout export

def write_layout(target, net):
    r = W.rng(44)
    objs = []
    for sid, s in sorted(net["signals"].items(), key=lambda kv: (kv[1]["ws"], kv[1]["screen"], kv[1]["x"])):
        objs.append(dict(ws=s["ws"], screen_no=s["screen"], type="SIG", id=sid, x=s["x"], y=s["y"], ars=s["subarea"]))
    # the drawn track, the points at each crossover, train describer berths along the lines, location text
    for ws in W.WS_IDS:
        pre = W.PREFIX[ws]
        mine = [t for t in net["tracks"] if t["ws"] == ws]
        for t in mine:
            objs.append(dict(ws=ws, screen_no=t["screen"], type="TRK", id="", x=t["x1"], y=t["y1"], x2=t["x2"], y2=t["y2"]))
        links = [t for t in mine if t["y1"] != t["y2"]]
        pts_ids = [int(v) for v in r.choice(np.arange(1101, 1999), size=len(links), replace=False)]
        for t, n in zip(links, pts_ids):
            objs.append(dict(ws=ws, screen_no=t["screen"], type="PTS", id="%s%d" % (pre, n), x=t["x1"] + 6, y=t["y1"]))
        flat = [t for t in mine if t["y1"] == t["y2"]]
        berth_ids = [int(v) for v in r.choice(np.arange(1, 9999), size=int(r.integers(110, 150)), replace=False)]
        for n in berth_ids:
            t = flat[int(r.integers(0, len(flat)))]
            objs.append(dict(ws=ws, screen_no=t["screen"], type="BERTH", id="%s%04d" % (pre[:1], n),
                             x=int(r.integers(t["x1"] + 10, t["x2"] - 40)), y=t["y1"] - 14))
        for jn in W.JUNCTIONS[ws]:
            sigs = sorted((s for s in net["signals"].values() if s["ws"] == ws and s["junction"] == jn),
                          key=lambda s: (s["screen"], s["x"], s["y"]))
            s = sigs[int(r.integers(0, len(sigs)))] if sigs else dict(screen=1, x=600, y=400)
            objs.append(dict(ws=ws, screen_no=s["screen"], type="TEXT", id="", text=jn.upper(),
                             x=max(110, s["x"] - 40), y=max(110, s["y"] - 38)))
    uniq = objs
    routes = [dict(route_id=rt["route_id"], entrance=rt["entrance"], exit=rt["exit"]) for rt in
              sorted(net["routes"], key=lambda x: x["route_id"])]
    doc = {"vds_product": "Corvane VDS-3", "site": "FENMOOR ROC", "configuration": "8.2.1",
           "exported": "2026-10-02T10:41:07+01:00",
           "ws_list": [dict(number=ws, desk=W.DESK[ws], screen_list=[dict(screen_no=k, width=W.SCREEN_W, height=W.SCREEN_H)
                                                                     for k in range(1, 5)]) for ws in W.WS_IDS],
           "ars_subareas": [dict(subarea_code=sa, ws=ws, replaces=W.OLD_SUBAREA[sa]) for ws in W.WS_IDS
                            for sa in W.SUBAREAS[ws]],
           "objects": uniq, "routes": routes}
    p = path(target, "layout")
    ensure(p)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return len(uniq)


# --------------------------------------------------------------------------------------------- staffing

def period_bounds(fy, p):
    start = dt.date(fy, 4, 1)
    first_sat = start + dt.timedelta(days=(5 - start.weekday()) % 7)
    p01_end = first_sat + dt.timedelta(days=21)
    if p == 1:
        return start, p01_end
    a = p01_end + dt.timedelta(days=1 + 28 * (p - 2))
    b = a + dt.timedelta(days=27)
    if p == 13:
        b = dt.date(fy + 1, 3, 31)
    return a, b


def write_rosters(target, ros, staff):
    pub = ros["published"]
    groups = {ws: [p for p in staff if p["home"] == ws] for ws in W.WS_IDS}
    relief = [p for p in staff if p["relief"]]
    wb = openpyxl.Workbook()
    first = True
    for p in range(7, 14):
        a, b = period_bounds(2025, p)
        sh = wb.active if first else wb.create_sheet()
        first = False
        sh.title = "P%02d" % p
        sh.cell(row=1, column=1, value="Fenmoor ROC signalling roster, period %d 2025/26, %s to %s"
                % (p, a.strftime("%d/%m/%Y"), b.strftime("%d/%m/%Y"))).font = Font(bold=True)
        dates = list(W.days(a, b))
        header_row(sh, 3, ["Desk", "Staff no"] + [d.strftime("%a %d/%m") for d in dates])
        row = 4
        for ws in W.WS_IDS:
            for person in groups[ws]:
                sh.cell(row=row, column=1, value=W.DESK[ws])
                sh.cell(row=row, column=2, value=person["staff_no"])
                for k, d in enumerate(dates):
                    c = pub.get((person["staff_no"], d), "")
                    if c in ("D", "N", "AL", "TR"):
                        sh.cell(row=row, column=3 + k, value=c)
                row += 1
        for person in relief:
            sh.cell(row=row, column=1, value="Relief")
            sh.cell(row=row, column=2, value=person["staff_no"])
            for k, d in enumerate(dates):
                c = pub.get((person["staff_no"], d), "")
                if c in ("RD", "RN", "AL", "TR"):
                    sh.cell(row=row, column=3 + k, value=c)
            row += 1
        sh.column_dimensions["A"].width = 14
        sh.column_dimensions["B"].width = 9
        for k in range(len(dates)):
            sh.column_dimensions[openpyxl.utils.get_column_letter(3 + k)].width = 7
        sh.freeze_panes = "C4"
    key = wb.create_sheet("Key")
    header_row(key, 1, ["Code", "Duty", "Hours"])
    for k, (c, d, h) in enumerate((("D", "Day", "07:00-19:00"), ("N", "Night", "19:00-07:00"),
                                   ("RD", "Relief day", "07:00-19:00"), ("RN", "Relief night", "19:00-07:00"),
                                   ("AL", "Annual leave", ""), ("TR", "Training", "")), start=2):
        for cc, v in enumerate((c, d, h), start=1):
            key.cell(row=k, column=cc, value=(None if v == "" else v))
    xlsx_save(wb, path(target, "ros25"), "ROC Rostering", "Fenmoor ROC Rostering", "2025-08-21T10:03:55Z",
              "2026-02-27T13:44:20Z", title="Signalling roster 2025-26")
    # 2026/27 from the new rostering tool: one row per person per day
    wb = openpyxl.Workbook()
    sh = wb.active
    sh.title = "Roster"
    header_row(sh, 1, ["Duty date", "Staff no", "Duty", "Start", "Finish", "Desk"])
    row = 2
    duty = {"D": ("DAY", "07:00", "19:00"), "N": ("NIGHT", "19:00", "07:00"), "RD": ("RELIEF DAY", "07:00", "19:00"),
            "RN": ("RELIEF NIGHT", "19:00", "07:00"), "AL": ("LEAVE", "", ""), "TR": ("TRAINING", "08:00", "16:00")}
    home = {p["staff_no"]: p["home"] for p in staff}
    a, _ = period_bounds(2026, 1)
    _, b = period_bounds(2026, 7)
    for d in W.days(a, b):
        for person in sorted(staff, key=lambda q: q["staff_no"]):
            c = pub.get((person["staff_no"], d), "")
            if c not in duty:
                continue
            nm, s0, s1 = duty[c]
            desk = home[person["staff_no"]] if c in ("D", "N") else ""
            for cc, v in enumerate((d, person["staff_no"], nm, s0, s1, desk), start=1):
                cell = sh.cell(row=row, column=cc, value=(None if v == "" else v))
                if cc == 1:
                    cell.number_format = "dd/mm/yyyy"
            row += 1
    for c, w in zip("ABCDEF", (11, 9, 14, 7, 7, 6)):
        sh.column_dimensions[c].width = w
    sh.freeze_panes = "A2"
    sh.auto_filter.ref = "A1:F%d" % (row - 1)
    xlsx_save(wb, path(target, "ros26"), "ROC Rostering", "Fenmoor ROC Rostering", "2026-03-04T09:12:31Z",
              "2026-09-09T11:58:02Z", title="Signalling roster 2026-27")


def write_changes(target, ros):
    rows = []
    r = W.rng(45)
    managers = ["417305", "659021"]
    for c in sorted(ros["changes"], key=lambda x: (x["day"], x["shift"], x["ws"])):
        if not (dt.date(2025, 9, 14) <= c["day"] <= dt.date(2026, 10, 10)) or c.get("unrecorded"):
            continue
        desk = c["ws"] if c["day"] >= dt.date(2026, 4, 1) else W.DESK[c["ws"]]
        rows.append((c["day"].strftime("%d/%m/%Y"), c["shift"], c["rostered"], c["worked"], c["change"],
                     c["start"].strftime("%H:%M"), c["end"].strftime("%H:%M"), desk,
                     managers[int(r.integers(0, 2))]))
    write_csv(path(target, "changes"), ["duty_date", "duty", "rostered", "worked_by", "change_type", "from", "to", "desk",
                                        "approved_by"], rows)
    return len(rows)


def write_competence(target, staff, ros):
    wb = openpyxl.Workbook()
    sh = wb.active
    sh.title = "Competence"
    header_row(sh, 1, ["Staff no", "Grade", "Date qualified", "Home desk"] + ["Competent %s %s" % (ws, W.DESK[ws].title())
                                                                             for ws in W.WS_IDS])
    r = W.rng(46)
    first = {}
    for sn, ws, s0, s1, how in ros["spans"]:
        k2 = (sn, ws)
        if k2 not in first or s0.date() < first[k2]:
            first[k2] = s0.date()
    kept = dt.date(2026, 8, 28)   # the register as last updated
    for k, p in enumerate(sorted(staff, key=lambda q: q["staff_no"]), start=2):
        vals = [p["staff_no"], p["grade"], p["qualified"], p["home"] if p["home"] else "Relief"]
        for ws in W.WS_IDS:
            if ws in p["competent"]:
                if ws == (p["home"] or W.WS_IDS[0]):
                    d = p["qualified"]
                else:
                    # passed out on another desk some months after qualifying, and before first working it
                    d = p["qualified"] + dt.timedelta(days=int(r.integers(60, 400)))
                    cap = min(first.get((p["staff_no"], ws), kept), kept)
                    if d > cap:
                        d = max(p["qualified"], cap - dt.timedelta(days=int(r.integers(3, 40))))
                vals.append(d)
            else:
                vals.append(None)
        for c, v in enumerate(vals, start=1):
            cell = sh.cell(row=k, column=c, value=(None if v == "" else v))
            if isinstance(v, dt.date):
                cell.number_format = "dd/mm/yyyy"
    for c, w in zip("ABCDEFGHIJ", (9, 16, 14, 13, 16, 16, 16, 18, 16, 16)):
        sh.column_dimensions[c].width = w
    xlsx_save(wb, path(target, "comp"), "Alan Pope", "Alan Pope", "2019-06-11T09:20:44Z", "2026-08-28T14:06:39Z",
              title="Signaller competence register")


# ----------------------------------------------------------------------------------------------- ARS log

def write_ars(target, periods, drops, fails):
    """Both servers write the ARS status log; the export merges them. Server B's copy of an event lands a
    fraction of a second after A's and, being replicated, carries no user. While A is down for maintenance
    only B writes, with the user. Each server names sub-areas by the codes of the release it runs."""
    r = W.rng(47)
    down = [(f["a_down"], f["a_up"]) for f in fails]
    ev = []
    for p in periods:
        if p.get("ws_event"):
            continue
        ev.append((p["off"], p["sa"], p["ws"], "OFF", p["user_off"], {"ooc": "OOC", "data": "TTD", "poss": "POSS"}[p["kind"]]))
        ev.append((p["on"], p["sa"], p["ws"], "ON", p["user_on"], ""))
    back = {(p["ws"], p["sa"], p["on"]): p["user_on"] for p in periods if p.get("ws_event")}
    for d in drops:
        ev.append((d["off"], None, d["ws"], "OFF", "", "FAIL"))
        for sa, t in d["ons"].items():
            ev.append((t, sa, d["ws"], "ON", back.get((d["ws"], sa, t)) or "", ""))
    rows = []
    for t, sa, ws, state, user, reason in ev:
        pass
        a_down = any(a <= t < b for a, b in down)
        for srv in ("ROC-A", "ROC-B"):
            if srv == "ROC-A" and a_down:
                continue
            tt = t if srv == "ROC-A" or a_down else t + dt.timedelta(milliseconds=float(r.uniform(30, 900)))
            new = tt >= (W.RELEASE_A if srv == "ROC-A" else W.RELEASE_B)
            if sa is None:
                code = ws if new else W.DESK[ws]
            else:
                code = sa if new else W.OLD_SUBAREA[sa]
            u = user if (srv == "ROC-A" or a_down) else ""
            if sa is not None and state == "ON" and not u and srv == "ROC-A":
                u = ""
            rows.append((tt, srv, code, state, u, reason))
    # server B's ARS process stamps the server's own clock into the same column, and B's clock was left on the
    # supplier's Central European time when it was installed: an hour ahead of UK time all year. The export
    # selects on the column as stamped.
    rows = [((W.utc_to_local(t) + dt.timedelta(hours=1) if srv == "ROC-B" else t), srv, code, st, u, rs)
            for t, srv, code, st, u, rs in rows]
    rows = [x for x in rows if W.local_to_utc(dt.datetime(2025, 10, 1)) <= x[0] < W.local_to_utc(dt.datetime(2026, 10, 1))]
    rows.sort(key=lambda x: (x[0], x[1]))
    out = [(iso_ms(t), srv, code, st, u, rs) for t, srv, code, st, u, rs in rows]
    write_csv(path(target, "ars"), ["logged_utc", "server", "subarea", "state", "user", "reason"], out, newline="\n")
    return len(out)


# ---------------------------------------------------------------------------------------- adhesion (distractor)

def write_adhesion(target):
    r = W.rng(48)
    rows = []
    d = dt.date(2025, 9, 29)
    sites = list(LOCATION_CODE.items())
    n = 0
    while d <= dt.date(2025, 12, 19):
        for _ in range(int(r.poisson(2.6 if d.month in (10, 11) else 0.9))):
            name, code = sites[int(r.integers(0, len(sites)))]
            t = dt.datetime(d.year, d.month, d.day, int(r.integers(5, 23)), int(r.integers(0, 60)))
            n += int(r.integers(1, 4))
            rows.append(("LA%05d" % (31200 + n), t.strftime("%d/%m/%Y %H:%M"), code, name,
                         r.choice(["Up", "Down"]), r.choice(["Driver report", "Driver report", "RHTT observation",
                                                              "Signaller report"]),
                         r.choice(["Low", "Low", "Exceptionally low", "Moderate"]),
                         r.choice(["Sandite applied", "RHTT diagrammed", "Treatment on next run", "No action",
                                   "Caution advised to drivers"])))
        d += dt.timedelta(days=1)
    write_csv(path(target, "adhesion"), ["report_no", "reported", "location_code", "location", "line", "source",
                                         "adhesion", "action"], rows)
    return len(rows)
