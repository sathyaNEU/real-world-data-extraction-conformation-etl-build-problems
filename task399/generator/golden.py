"""The golden, computed from the shipped files under target/ and nothing else."""
import bisect
import csv
import datetime as dt
import json
import math
import os
import re
from collections import defaultdict

import openpyxl

W0 = dt.date(2025, 10, 1)
W1 = dt.date(2026, 9, 30)
WS_IDS = ["W01", "W02", "W03", "W04", "W05", "W06"]
QUARTERS = [("2025 Q4", dt.date(2025, 10, 1), dt.date(2026, 1, 1)), ("2026 Q1", dt.date(2026, 1, 1), dt.date(2026, 4, 1)),
            ("2026 Q2", dt.date(2026, 4, 1), dt.date(2026, 7, 1)), ("2026 Q3", dt.date(2026, 7, 1), dt.date(2026, 10, 1))]
OLD_CODE = {"Wrong route": "RS1", "Late route setting": "RS2", "Route not set": "RS3", "Regulating": "RG1",
            "Communication": "CM1", "ARS": "AR1", "Workstation fault": "EQ1"}
FINDING = {"Competence": "competence", "Attention / distraction": "distraction", "Workload": "workload",
           "Fatigue": "fatigue", "ARS data": "ars", "Equipment": "equipment", "Not determined": "not determined",
           "Competence - route setting": "competence", "Competence - regulating": "competence",
           "Distraction": "distraction", "ARS timetable data": "ars", "Workstation equipment": "equipment"}
PROGRAMME_OF_FINDING = {"competence": "A", "fatigue": "C", "ars": "D", "workload": "E", "equipment": "B"}


def P(target, rel):
    return os.path.join(target, rel)


# --------------------------------------------------------------------------------------------- UK clock

def _last_sunday(y, m):
    d = dt.date(y, m, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return dt.datetime(d.year, d.month, d.day, 1, 0)


def to_local(utc):
    bst = _last_sunday(utc.year, 3) <= utc < _last_sunday(utc.year, 10)
    return utc + dt.timedelta(hours=1 if bst else 0)


def to_utc(local):
    g = local - dt.timedelta(hours=1)
    if to_local(g) == local and _last_sunday(g.year, 3) <= g < _last_sunday(g.year, 10):
        return g
    return local


def parse_utc(s):
    return dt.datetime.strptime(s.rstrip("Z"), "%Y-%m-%dT%H:%M:%S.%f")


# --------------------------------------------------------------------------------------------- layout

def load_layout(target):
    d = json.load(open(P(target, "control_system/workstation_layout_export_r8.2.1.json"), encoding="utf-8"))
    desk = {w["desk"]: w["number"] for w in d["ws_list"]}
    sig = {o["id"]: o for o in d["objects"] if o["type"] == "SIG"}
    routes = {r["route_id"]: (r["entrance"], r["exit"]) for r in d["routes"]}
    by_pair = {(e, x): rid for rid, (e, x) in routes.items()}
    sub = {s["subarea_code"]: s["ws"] for s in d["ars_subareas"]}
    old = {s["replaces"]: s["subarea_code"] for s in d["ars_subareas"]}
    return dict(desk=desk, sig=sig, routes=routes, by_pair=by_pair, sub=sub, old=old)


def route_id(text, L):
    if not text:
        return None
    t = str(text).strip()
    if t in L["routes"]:
        return t
    m = re.match(r"^([A-Z]{2}\d+)\s*(?:to|-)\s*([A-Z]{2}\d+)$", t)
    if m:
        return L["by_pair"].get((m.group(1), m.group(2)))
    return None


# --------------------------------------------------------------------------------------------- registers

def load_incidents(target, L):
    out = []
    wb = openpyxl.load_workbook(P(target, "incidents/operating_incident_register_2025-26.xlsx"), read_only=True)
    sh = wb["Register 2025-26"]
    rows = list(sh.iter_rows(values_only=True))
    h = {k: i for i, k in enumerate(rows[0])}
    for r in rows[1:]:
        if r[h["Ref"]] is None:
            continue
        d = r[h["Incident date"]]
        hh, mm = (int(x) for x in str(r[h["Time"]]).split(":"))
        occ = dt.datetime(d.year, d.month, d.day, hh, mm)
        out.append(dict(ref=r[h["Ref"]], occurred=occ, ws=L["desk"][str(r[h["Desk"]]).upper()],
                        staff_no=str(r[h["Signaller"]]), code=OLD_CODE[r[h["Category"]]],
                        route_set=route_id(r[h["Route set"]], L), route_required=route_id(r[h["Route required"]], L),
                        trust=int(r[h["TRUST"]]) if r[h["TRUST"]] not in (None, "") else None,
                        finding=FINDING[r[h["Finding"]]]))
    wb = openpyxl.load_workbook(P(target, "incidents/operating_incident_register_2026-27.xlsx"), read_only=True)
    sh = wb["Register"]
    rows = list(sh.iter_rows(values_only=True))
    h = {k: i for i, k in enumerate(rows[0])}
    for r in rows[1:]:
        if r[h["Incident ref"]] is None:
            continue
        out.append(dict(ref=r[h["Incident ref"]], occurred=r[h["Occurred"]], ws=str(r[h["Workstation"]]).split()[0],
                        staff_no=str(r[h["Staff no"]]), code=r[h["Category code"]],
                        route_set=route_id(r[h["Route set"]], L), route_required=route_id(r[h["Route required"]], L),
                        trust=int(r[h["TRUST incident"]]) if r[h["TRUST incident"]] not in (None, "") else None,
                        finding=FINDING[r[h["Underlying cause"]]]))
    return out


def load_minutes(target):
    mins = defaultdict(int)
    with open(P(target, "delay_attribution/ocf_delay_records_2025-04_2026-09.csv"), newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["resp"] == "OCF":
                mins[int(row["trust_incident"])] += int(row["pfpi_minutes"])
    with open(P(target, "delay_attribution/attribution_reviews_2025-26_2026-27.csv"), newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["status"] != "Agreed":
                continue
            m = int(row["pfpi_minutes"])
            a, b = int(row["from_incident"]), int(row["to_incident"])
            if a in mins:
                mins[a] -= m
            if b in mins:
                mins[b] += m
    return dict(mins)


def in_window(occ):
    return W0 <= occ.date() <= W1


def slip(inc, L):
    """A wrong route set onto the exit drawn beside the required one: the same entrance, the two exits' buttons
    within a dozen pixels on the same screen."""
    if inc["code"] != "RS1" or not inc["route_set"] or not inc["route_required"]:
        return False, None
    e1, x1 = L["routes"][inc["route_set"]]
    e2, x2 = L["routes"][inc["route_required"]]
    if e1 != e2:
        return False, None
    a, b = L["sig"][x1], L["sig"][x2]
    d = math.hypot(a["x"] - b["x"], a["y"] - b["y"]) if a["screen_no"] == b["screen_no"] else float("inf")
    return d <= 12.0, d


def main_call(target):
    L = load_layout(target)
    inc = [i for i in load_incidents(target, L) if i["trust"] is not None and in_window(i["occurred"])]
    mins = load_minutes(target)
    for i in inc:
        i["minutes"] = mins.get(i["trust"], 0)
        s, d = slip(i, L)
        i["slip"], i["exit_gap_px"] = s, d
    total = sum(i["minutes"] for i in inc)
    B = [i for i in inc if i["slip"] or i["code"] == "EQ1"]
    b_min = sum(i["minutes"] for i in B)
    by_ws = {w: sum(i["minutes"] for i in B if i["ws"] == w) for w in WS_IDS}
    months = []
    d = dt.date(2025, 10, 1)
    while d <= W1:
        months.append(d)
        d = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    by_month = []
    for m in months:
        b = sum(i["minutes"] for i in B if (i["occurred"].year, i["occurred"].month) == (m.year, m.month))
        t = sum(i["minutes"] for i in inc if (i["occurred"].year, i["occurred"].month) == (m.year, m.month))
        by_month.append((m.strftime("%Y-%m"), b, t - b))
    # the investigations' findings booked to the catalogue (the default path)
    findings = defaultdict(int)
    for i in inc:
        findings[i["finding"]] += i["minutes"]
    by_prog_findings = defaultdict(int)
    for f, v in findings.items():
        if f in PROGRAMME_OF_FINDING:
            by_prog_findings[PROGRAMME_OF_FINDING[f]] += v
    gaps = sorted(i["exit_gap_px"] for i in inc if i["code"] == "RS1" and i["exit_gap_px"] is not None)
    return dict(incidents=inc, total=total, b_minutes=b_min, b_by_ws=by_ws, b_by_month=by_month,
                start_ws=max(WS_IDS, key=lambda w: by_ws[w]), n_slips=sum(1 for i in inc if i["slip"]),
                n_eq=sum(1 for i in inc if i["code"] == "EQ1"), slip_minutes=sum(i["minutes"] for i in inc if i["slip"]),
                eq_minutes=sum(i["minutes"] for i in inc if i["code"] == "EQ1"), findings=dict(findings),
                by_prog_findings=dict(by_prog_findings), rs1_gaps=gaps, layout=L)


# --------------------------------------------------------------------------------------------- ask 1: hours

def load_competence(target):
    wb = openpyxl.load_workbook(P(target, "staffing/signaller_competence_register.xlsx"), read_only=True)
    rows = list(wb["Competence"].iter_rows(values_only=True))
    h = {k: i for i, k in enumerate(rows[0])}
    q = {}
    for r in rows[1:]:
        if r[h["Staff no"]]:
            v = r[h["Date qualified"]]
            q[str(r[h["Staff no"]])] = v.date() if isinstance(v, dt.datetime) else v
    return q


def anniversary(q):
    try:
        return q.replace(year=q.year + 2)
    except ValueError:
        return q.replace(year=q.year + 2, day=28)


def shift_bounds(day, duty):
    if duty == "D":
        return dt.datetime(day.year, day.month, day.day, 7), dt.datetime(day.year, day.month, day.day, 19)
    n = day + dt.timedelta(days=1)
    return dt.datetime(day.year, day.month, day.day, 19), dt.datetime(n.year, n.month, n.day, 7)


def load_roster(target, L):
    """Published duties: (staff_no, day, duty D/N, desk or None for a relief duty)."""
    duties = []
    wb = openpyxl.load_workbook(P(target, "staffing/signalling_roster_2025-26_P07-P13.xlsx"), read_only=True)
    for name in wb.sheetnames:
        if not name.startswith("P"):
            continue
        rows = list(wb[name].iter_rows(values_only=True))
        title = rows[0][0]
        m = re.search(r"(\d\d/\d\d/\d{4}) to (\d\d/\d\d/\d{4})", title)
        start = dt.datetime.strptime(m.group(1), "%d/%m/%Y").date()
        hdr = rows[2]
        for r in rows[3:]:
            if not r or r[1] is None:
                continue
            desk = str(r[0])
            for k in range(2, len(hdr)):
                c = r[k]
                if c in ("D", "N"):
                    duties.append((str(r[1]), start + dt.timedelta(days=k - 2), c, L["desk"][desk.upper()]))
                elif c in ("RD", "RN"):
                    duties.append((str(r[1]), start + dt.timedelta(days=k - 2), c[1], None))
    wb = openpyxl.load_workbook(P(target, "staffing/signalling_roster_2026-27_P01-P07.xlsx"), read_only=True)
    rows = list(wb["Roster"].iter_rows(values_only=True))
    h = {k: i for i, k in enumerate(rows[0])}
    kinds = {"DAY": ("D", True), "NIGHT": ("N", True), "RELIEF DAY": ("D", False), "RELIEF NIGHT": ("N", False)}
    for r in rows[1:]:
        if r[h["Duty"]] in kinds:
            d = r[h["Duty date"]].date() if isinstance(r[h["Duty date"]], dt.datetime) else r[h["Duty date"]]
            sh, rostered = kinds[r[h["Duty"]]]
            duties.append((str(r[h["Staff no"]]), d, sh, r[h["Desk"]] if rostered else None))
    return duties


def load_logins(target, L):
    """Per user, sorted (utc, workstation) of every action in the control system log."""
    acts = defaultdict(list)
    with open(P(target, "control_system/roc_signaller_actions_20251001_20260930.csv"), newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            ws = row["wkstn"]
            ws = ws if ws in WS_IDS else L["desk"][ws]
            acts[row["user"]].append((parse_utc(row["event_utc"]), ws))
    for u in acts:
        acts[u].sort()
    return acts


def worked_spans(target, L):
    duties = load_roster(target, L)
    acts = load_logins(target, L)
    spans = {}
    lo, hi = dt.datetime(2025, 10, 1), dt.datetime(2026, 10, 1)
    for sn, day, sh, desk in duties:
        s0, s1 = shift_bounds(day, sh)
        if s1 <= lo or s0 >= hi:
            continue
        if desk is None:
            a, b = to_utc(s0), to_utc(s1)
            lst = acts.get(sn, [])
            k = bisect.bisect_left(lst, (a, ""))
            seen = set()
            while k < len(lst) and lst[k][0] < b:
                seen.add(lst[k][1])
                k += 1
            if len(seen) != 1:
                raise ValueError("relief duty %s %s %s on %s" % (sn, day, sh, sorted(seen)))
            desk = seen.pop()
        spans[(desk, day, sh)] = [[sn, s0, s1]]
    with open(P(target, "staffing/roster_changes_2025-26_2026-27.csv"), newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            day = dt.datetime.strptime(row["duty_date"], "%d/%m/%Y").date()
            desk = row["desk"] if row["desk"] in WS_IDS else L["desk"][row["desk"]]
            sh = row["duty"]
            s0, s1 = shift_bounds(day, sh)
            if s1 <= lo or s0 >= hi:
                continue
            hh, mm = (int(x) for x in row["from"].split(":"))
            frm = dt.datetime(day.year, day.month, day.day, hh, mm)
            if sh == "N" and hh < 12:
                frm += dt.timedelta(days=1)
            if row["change_type"] == "Rest day working":
                spans[(desk, day, sh)] = [[row["worked_by"], s0, s1]]
            elif row["change_type"] == "Swap":
                spans[(desk, day, sh)] = [[row["worked_by"], s0, s1]]
            elif row["change_type"] == "Sickness cover":
                cur = spans[(desk, day, sh)]
                if frm <= s0:
                    spans[(desk, day, sh)] = [[row["worked_by"], s0, s1]]
                else:
                    spans[(desk, day, sh)] = [[cur[0][0], s0, frm], [row["worked_by"], frm, s1]]
    # who worked each span is who the control system shows working the desk: a change agreed on the day and
    # never entered on the changes list still shows there
    desk_acts = defaultdict(list)
    for u, lst in acts.items():
        for t, w in lst:
            desk_acts[w].append((t, u))
    for w in desk_acts:
        desk_acts[w].sort()
    out = []
    for (desk, day, sh), lst in spans.items():
        for sn, a, b in lst:
            x, y = to_utc(a), to_utc(b)
            lst2 = desk_acts[desk]
            k = bisect.bisect_left(lst2, (x, ""))
            n = defaultdict(int)
            while k < len(lst2) and lst2[k][0] < y:
                n[lst2[k][1]] += 1
                k += 1
            if n:
                sn = max(sorted(n), key=lambda u: n[u])
            out.append((sn, desk, a, b))
    return out


def hours_by_band(target, L=None):
    L = L or load_layout(target)
    q = load_competence(target)
    lo, hi = dt.datetime(2025, 10, 1), dt.datetime(2026, 10, 1)
    res = {(w, b): 0.0 for w in WS_IDS for b in ("first two years", "other")}
    for sn, desk, a, b in worked_spans(target, L):
        a, b = max(a, lo), min(b, hi)
        if b <= a:
            continue
        ann = dt.datetime.combine(anniversary(q[sn]), dt.time(0))
        qd = dt.datetime.combine(q[sn], dt.time(0))
        cuts = sorted({a, b} | {t for t in (qd, ann) if a < t < b})
        for x, y in zip(cuts, cuts[1:]):
            band = "first two years" if qd <= x < ann else "other"
            res[(desk, band)] += (to_utc(y) - to_utc(x)).total_seconds() / 3600.0
    return res


# --------------------------------------------------------------------------------------------- ask 2: ARS

def ars_hours(target, L=None):
    L = L or load_layout(target)
    ev = []
    with open(P(target, "control_system/ars_status_log_20251001_20260930.csv"), newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            code = row["subarea"]
            if code in L["sub"]:
                key = ("SA", code)
            elif code in L["old"]:
                key = ("SA", L["old"][code])
            elif code in WS_IDS:
                key = ("WS", code)
            else:
                key = ("WS", L["desk"][code])
            t = parse_utc(row["logged_utc"])
            if row["server"] == "ROC-B":
                # B's copies of A's events sit an hour behind in winter and two in summer: B stamps Central
                # European time, an hour ahead of UK time
                t = to_utc(t - dt.timedelta(hours=1))
            ev.append((t, key, row["state"]))
    ev.sort()
    # one event logged by both servers: the same key and state within two seconds
    uniq = []
    last = {}
    for t, key, state in ev:
        k = (key, state)
        if k in last and (t - last[k]).total_seconds() <= 2.0:
            continue
        last[k] = t
        uniq.append((t, key, state))
    per = defaultdict(list)
    for t, (kind, code), state in uniq:
        targets = [code] if kind == "SA" else [s for s, w in L["sub"].items() if w == code]
        for sa in targets:
            per[sa].append((t, state))
    lo = to_utc(dt.datetime(2025, 10, 1))
    hi = to_utc(dt.datetime(2026, 10, 1))
    intervals = defaultdict(list)
    for sa, lst in per.items():
        lst.sort()
        off_since = None
        first = True
        for t, state in lst:
            if state == "OFF":
                if off_since is None:
                    off_since = t
            else:
                if off_since is not None:
                    intervals[sa].append((off_since, t))
                elif first:
                    intervals[sa].append((lo, t))
                off_since = None
            first = False
        if off_since is not None:
            intervals[sa].append((off_since, hi))
    res = {(w, q[0]): 0.0 for w in WS_IDS for q in QUARTERS}
    for sa, lst in intervals.items():
        w = L["sub"][sa]
        for a, b in lst:
            for name, q0, q1 in QUARTERS:
                x = max(a, to_utc(dt.datetime.combine(q0, dt.time(0))))
                y = min(b, to_utc(dt.datetime.combine(q1, dt.time(0))))
                if y > x:
                    res[(w, name)] += (y - x).total_seconds() / 3600.0
    return res, intervals


def compute(target):
    M = main_call(target)
    L = M["layout"]
    H = hours_by_band(target, L)
    A, _ = ars_hours(target, L)
    return dict(main=M, hours=H, ars=A)
