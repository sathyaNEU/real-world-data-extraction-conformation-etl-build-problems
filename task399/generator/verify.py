"""Independent verifier for task399: reads only the bundle under target/ and the goldens, on its own code path
(the UK clock from the tz database, its own parsers and joins), recomputes every graded figure and every rung,
and compares them with figures.json. Usage: python3 verify.py [target_dir]"""
import collections
import csv
import datetime as dt
import json
import math
import os
import re
import sys
from zoneinfo import ZoneInfo

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
UK = ZoneInfo("Europe/London")
UTC = dt.timezone.utc
FAILS = []


def check(name, cond, detail=""):
    print("%-4s %s %s" % ("ok" if cond else "FAIL", name, detail))
    if not cond:
        FAILS.append(name)


def utc_of_local(naive):
    return naive.replace(tzinfo=UK).astimezone(UTC).replace(tzinfo=None)


def local_of_utc(naive):
    return naive.replace(tzinfo=UTC).astimezone(UK).replace(tzinfo=None)


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)


def rows_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def sheet(path, name):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = [list(r) for r in wb[name].iter_rows(values_only=True)]
    wb.close()
    return out


def as_date(v):
    return v.date() if isinstance(v, dt.datetime) else v


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def docx_text(path):
    import docx
    d = docx.Document(path)
    out = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            out.extend(c.text for c in row.cells)
    return "\n".join(out)


def main(T):
    J = lambda *p: os.path.join(T, *p)
    F = json.load(open(os.path.join(HERE, "figures.json")))

    # ------------------------------------------------------------------------- formats, each with a control
    lay = json.load(open(J("control_system", "workstation_layout_export_r8.2.1.json"), encoding="utf-8"))
    check("json: layout export read", lay["configuration"] == "8.2.1" and len(lay["routes"]) > 300)
    tor = pdf_text(J("governance", "2027_improvement_plan_terms_of_reference.pdf"))
    tor1 = re.sub(r"\s+", " ", tor)
    for sent in ("The plan funds the programme whose cause produced the most of the operating centre's delay minutes "
                 "in the twelve months from 1 October 2025 to 30 September 2026.",
                 "An incident belongs to the twelve months by the date and time it occurred, UK time.",
                 "An incident counts for a programme when it would not have happened had that programme been in place.",
                 "after the moves the attribution review log records as agreed.",
                 "the plan begins with the stage that would have removed the most of those minutes."):
        check("pdf: terms of reference carry %r" % sent[:48], sent in tor1)
    wl = pdf_text(J("reference", "fenmoor_roc_workload_assessment_2025.pdf"))
    check("pdf: workload assessment read (Table 1 row for Hatherby)", re.search(r"W03 Hatherby\s+44\s+86\s+72\s+91\s+63", wl))
    cat = docx_text(J("governance", "improvement_catalogue_2027.docx"))
    progs = re.findall(r"^([A-E])\. (.+)$", cat, re.M)
    check("docx: catalogue lists five programmes", [p[0] for p in progs] == list("ABCDE"), str(progs))
    check("docx: B redraws every screen's layout", "every screen's track layout redrawn" in cat)
    adh = rows_csv(J("reference", "railhead_adhesion_reports_autumn_2025.csv"))
    check("csv: adhesion reports read", len(adh) > 100 and "adhesion" in adh[0])

    # ------------------------------------------------------------------------- the layout's geometry
    desk_no = {w["desk"]: w["number"] for w in lay["ws_list"]}
    pos = {o["id"]: (o["ws"], o["screen_no"], o["x"], o["y"]) for o in lay["objects"] if o["type"] == "SIG"}
    route = {r["route_id"]: (r["entrance"], r["exit"]) for r in lay["routes"]}
    pair = {v: k for k, v in route.items()}
    sub_ws = {s["subarea_code"]: s["ws"] for s in lay["ars_subareas"]}
    old_sub = {s["replaces"]: s["subarea_code"] for s in lay["ars_subareas"]}

    def norm_ws(v):
        v = str(v).strip()
        m = re.match(r"^(W0\d)\b", v)
        return m.group(1) if m else desk_no[v.upper()]

    def parse_route(v):
        if v is None or str(v).strip() == "":
            return None
        v = str(v).strip()
        if v in route:
            return route[v]
        m = re.fullmatch(r"([A-Z]{2}\d{3})(?: to |-)([A-Z]{2}\d{3})", v)
        if not m:
            raise ValueError("route text %r" % v)
        return (m.group(1), m.group(2))

    # ------------------------------------------------------------------------- incidents and minutes
    inc = []
    reg = sheet(J("incidents", "operating_incident_register_2025-26.xlsx"), "Register 2025-26")
    hd = reg[0]
    c = {k: hd.index(k) for k in hd}
    for r in reg[1:]:
        if not r[c["Ref"]]:
            continue
        d = as_date(r[c["Incident date"]])
        h, m = map(int, str(r[c["Time"]]).split(":"))
        inc.append(dict(ref=r[c["Ref"]], local=dt.datetime(d.year, d.month, d.day, h, m), ws=norm_ws(r[c["Desk"]]),
                        cat=r[c["Category"]], set=parse_route(r[c["Route set"]]), req=parse_route(r[c["Route required"]]),
                        trust=r[c["TRUST"]], finding=r[c["Finding"]]))
    reg = sheet(J("incidents", "operating_incident_register_2026-27.xlsx"), "Register")
    codes = sheet(J("incidents", "operating_incident_register_2026-27.xlsx"), "Category codes")
    old_cat = {row[2]: row[0] for row in codes[1:] if row and row[0]}
    check("xlsx: category crosswalk read", old_cat.get("Wrong route") == "RS1" and len(old_cat) == 7)
    hd = reg[0]
    c = {k: hd.index(k) for k in hd}
    for r in reg[1:]:
        if not r[c["Incident ref"]]:
            continue
        inc.append(dict(ref=r[c["Incident ref"]], local=r[c["Occurred"]], ws=norm_ws(r[c["Workstation"]]),
                        cat=r[c["Category code"]], set=parse_route(r[c["Route set"]]),
                        req=parse_route(r[c["Route required"]]), trust=r[c["TRUST incident"]],
                        finding=r[c["Underlying cause"]]))
    for i in inc:
        i["code"] = old_cat.get(i["cat"], i["cat"])
    check("xlsx: both registers read", len(inc) > 600 and {i["ref"][:7] for i in inc} == {"FROC/25", "FROC/26"})
    minutes = collections.Counter()
    for r in rows_csv(J("delay_attribution", "ocf_delay_records_2025-04_2026-09.csv")):
        if r["resp"] == "OCF":
            minutes[int(r["trust_incident"])] += int(r["pfpi_minutes"])
    rev = rows_csv(J("delay_attribution", "attribution_reviews_2025-26_2026-27.csv"))
    check("csv: review log read", len(rev) > 50 and {r["status"] for r in rev} >= {"Agreed", "Rejected"})
    for r in rev:
        if r["status"] == "Agreed":
            a, b, m = int(r["from_incident"]), int(r["to_incident"]), int(r["pfpi_minutes"])
            if a in minutes:
                minutes[a] -= m
            if b in minutes:
                minutes[b] += m
    w0, w1 = dt.datetime(2025, 10, 1), dt.datetime(2026, 10, 1)
    win = [i for i in inc if i["trust"] not in (None, "") and w0 <= i["local"] < w1]
    for i in win:
        i["min"] = minutes.get(int(i["trust"]), 0)

    def gap(i):
        if i["code"] != "RS1" or not i["set"] or not i["req"] or i["set"][0] != i["req"][0]:
            return None
        a, b = pos[i["set"][1]], pos[i["req"][1]]
        if a[:2] != b[:2]:
            return float("inf")
        return math.dist(a[2:], b[2:])
    for i in win:
        i["gap"] = gap(i)
    rs1 = [i for i in win if i["code"] == "RS1"]
    near = [i for i in rs1 if i["gap"] is not None and i["gap"] <= 12]
    eq = [i for i in win if i["code"] == "EQ1"]
    Bset = near + eq
    Bmin = sum(i["min"] for i in Bset)
    check("call: the display renewal's minutes", Bmin == F["call_minutes"], "%d against %d" % (Bmin, F["call_minutes"]))
    check("component: slips", (len(near), sum(i["min"] for i in near)) == (F["slip_count"], F["slip_minutes"]))
    check("component: display faults", (len(eq), sum(i["min"] for i in eq)) == (F["eq_count"], F["eq_minutes"]))
    gaps = sorted(i["gap"] for i in rs1 if i["gap"] is not None)
    lo_c, hi_c = min(g for g in gaps if g <= 12), max(g for g in gaps if g <= 12)
    lo_f = min(g for g in gaps if g > 12)
    check("step 3: the exit gaps split in two, the stated bounds holding every gap",
          F["gap_close_min_px"] <= lo_c < F["gap_close_min_px"] + 0.1 and F["gap_close_max_px"] - 0.1 < hi_c
          <= F["gap_close_max_px"] and F["gap_far_min_px"] <= lo_f < F["gap_far_min_px"] + 1
          and sum(1 for g in gaps if g > 12) == F["rs1_far"], "%s" % [round(g, 1) for g in gaps[:3]])
    by_ws = collections.Counter()
    for i in Bset:
        by_ws[i["ws"]] += i["min"]
    check("deck: minutes by workstation", all(by_ws[w] == F["b_by_ws"][w] for w in F["b_by_ws"]), str(dict(by_ws)))
    check("deck: delivery begins on the workstation with the most", max(by_ws, key=by_ws.get) == F["start_ws"])
    # the default path: the investigations' findings booked to the catalogue
    book = {"Competence": "A", "Competence - route setting": "A", "Competence - regulating": "A", "Fatigue": "C",
            "ARS data": "D", "ARS timetable data": "D", "Workload": "E", "Equipment": "B",
            "Workstation equipment": "B"}
    dp = collections.Counter()
    for i in win:
        if i["finding"] in book:
            dp[book[i["finding"]]] += i["min"]
    check("rung 0: the findings booked to the catalogue file A", max(dp, key=dp.get) == "A" and
          all(dp[k] == F["default_by_programme"][k] for k in dp), str(dict(dp)))
    check("rung 0: the display's own findings sit low", sorted(dp, key=lambda k: -dp[k]).index("B") >= 3)
    # the control system log: quick resets fall on the drawn-close pairs only
    log = rows_csv(J("control_system", "roc_signaller_actions_20251001_20260930.csv"))
    check("csv: control system log read", len(log) > 25000 and set(log[0]) >= {"event_utc", "action", "entrance"})
    seen = set()
    per_user = collections.defaultdict(list)
    for r in log:
        k = (r["user"], r["action"], r["entrance"], r["exit"], r["event_utc"][:19])
        if k in seen:
            continue
        seen.add(k)
        per_user[r["user"]].append((ts(r["event_utc"]), r["action"], r["entrance"], r["exit"]))
    quick = collections.Counter()
    for u, lst in per_user.items():
        lst.sort()
        for a, b, cc in zip(lst, lst[1:], lst[2:]):
            if (a[1] == "ST" and b[1] == "CN" and b[2:] == a[2:] and (b[0] - a[0]).total_seconds() <= 20
                    and cc[1] == "RQ" and cc[2] == a[2] and cc[3] != a[3] and (cc[0] - b[0]).total_seconds() <= 10):
                quick[(a[2], frozenset((a[3], cc[3])))] += 1
    reset_d = []
    for (e, xs), n in quick.items():
        x1, x2 = sorted(xs)
        p1, p2 = pos[x1], pos[x2]
        reset_d.append(math.dist(p1[2:], p2[2:]) if p1[:2] == p2[:2] else float("inf"))
    check("log: every quick reset pair is drawn under 12 px apart", reset_d and max(reset_d) <= 12,
          "%d pairs" % len(reset_d))
    by_log = {i["ref"] for i in rs1 if i["set"] and i["req"] and (i["req"][0], frozenset((i["set"][1], i["req"][1])))
              in quick}
    check("log: the quick-reset pairs pick out the same wrong routes", by_log == {i["ref"] for i in near})
    n_quick = n_beside = 0
    for u, lst in per_user.items():
        set_at = {}
        for k, (t, a, e, x) in enumerate(lst):
            if a == "ST":
                set_at[(e, x)] = t
            elif a == "CN" and (t - set_at.get((e, x), dt.datetime.min)).total_seconds() <= 20:
                n_quick += 1
                after = [r[3] for r in lst[k + 1:] if r[1] == "RQ" and r[2] == e]
                if after and after[0] != x:
                    p1, p2 = pos[x], pos[after[0]]
                    n_beside += p1[:2] == p2[:2] and math.dist(p1[2:], p2[2:]) <= 12
    check("step 4: routes cancelled within twenty seconds, and those followed by the exit drawn beside",
          (n_quick, n_beside) == (F["quick_cancels"], F["quick_cancels_beside"]), "%d, %d" % (n_quick, n_beside))

    # ------------------------------------------------------------------------- ask: hours by band
    comp = sheet(J("staffing", "signaller_competence_register.xlsx"), "Competence")
    hd = comp[0]
    qual = {str(r[0]): as_date(r[hd.index("Date qualified")]) for r in comp[1:] if r[0]}
    check("xlsx: competence register read", len(qual) > 30)

    def two_years(q):
        try:
            return q.replace(year=q.year + 2)
        except ValueError:
            return q.replace(year=q.year + 2, month=2, day=28)
    duty = {}
    wb = openpyxl.load_workbook(J("staffing", "signalling_roster_2025-26_P07-P13.xlsx"), read_only=True)
    check("xlsx: 2025-26 roster periods read", [s for s in wb.sheetnames if s.startswith("P")] ==
          ["P07", "P08", "P09", "P10", "P11", "P12", "P13"])
    for name in [s for s in wb.sheetnames if s.startswith("P")]:
        rr = [list(x) for x in wb[name].iter_rows(values_only=True)]
        d0 = dt.datetime.strptime(re.search(r"(\d\d/\d\d/\d{4}) to", rr[0][0]).group(1), "%d/%m/%Y").date()
        for row in rr[3:]:
            if not row or not row[1]:
                continue
            for k, v in enumerate(row[2:]):
                if v in ("D", "N", "RD", "RN"):
                    day = d0 + dt.timedelta(days=k)
                    desk = desk_no[str(row[0]).upper()] if v in ("D", "N") else None
                    duty[(str(row[1]), day, v[-1])] = desk
    wb.close()
    long = sheet(J("staffing", "signalling_roster_2026-27_P01-P07.xlsx"), "Roster")
    hd = long[0]
    for row in long[1:]:
        kind = row[hd.index("Duty")]
        if kind in ("DAY", "NIGHT", "RELIEF DAY", "RELIEF NIGHT"):
            duty[(str(row[hd.index("Staff no")]), as_date(row[hd.index("Duty date")]), "N" if "NIGHT" in kind else "D")] = (
                row[hd.index("Desk")] if not kind.startswith("RELIEF") else None)
    acts = collections.defaultdict(list)
    for r in log:
        acts[r["user"]].append((ts(r["event_utc"]), norm_ws(r["wkstn"])))
    for u in acts:
        acts[u].sort()

    def bounds(day, sh):
        s = dt.datetime(day.year, day.month, day.day, 7 if sh == "D" else 19)
        return s, s + dt.timedelta(hours=12)
    cover = {}
    for (sn, day, sh), desk in duty.items():
        s0, s1 = bounds(day, sh)
        if s1 <= w0 or s0 >= w1:
            continue
        if desk is None:
            a, b = utc_of_local(s0), utc_of_local(s1)
            n = collections.Counter(w for t, w in acts.get(sn, []) if a <= t < b)
            check("relief duty placed from the log", len(n) == 1, "%s %s %s %s" % (sn, day, sh, dict(n))) if len(
                n) != 1 else None
            desk = n.most_common(1)[0][0]
        cover[(desk, day, sh)] = [(sn, s0, s1)]
    ch = rows_csv(J("staffing", "roster_changes_2025-26_2026-27.csv"))
    check("csv: roster changes read", len(ch) > 50)
    for r in ch:
        day = dt.datetime.strptime(r["duty_date"], "%d/%m/%Y").date()
        s0, s1 = bounds(day, r["duty"])
        if s1 <= w0 or s0 >= w1:
            continue
        desk = norm_ws(r["desk"])
        h, m = map(int, r["from"].split(":"))
        frm = dt.datetime(day.year, day.month, day.day, h, m)
        if frm < s0:
            frm += dt.timedelta(days=1)
        if r["change_type"] == "Sickness cover" and frm > s0:
            first = cover[(desk, day, r["duty"])][0][0]
            cover[(desk, day, r["duty"])] = [(first, s0, frm), (r["worked_by"], frm, s1)]
        else:
            cover[(desk, day, r["duty"])] = [(r["worked_by"], s0, s1)]
    by_desk_user = collections.defaultdict(list)
    for u, lst in acts.items():
        for t, w in lst:
            by_desk_user[w].append((t, u))
    for w in by_desk_user:
        by_desk_user[w].sort()
    import bisect
    hours = collections.defaultdict(float)
    swapped = 0
    for (desk, day, sh), lst in cover.items():
        fixed = []
        for sn, a, b in lst:
            x, y = utc_of_local(a), utc_of_local(b)
            L2 = by_desk_user[desk]
            n = collections.Counter(u for t, u in L2[bisect.bisect_left(L2, (x, "")):bisect.bisect_left(L2, (y, ""))])
            if n:
                top = n.most_common()
                best = sorted(u for u, k in top if k == top[0][1])[0]
                if best != sn:
                    swapped += 1
                sn = best
            fixed.append((sn, a, b))
        cover[(desk, day, sh)] = fixed
    check("log: the signed-on signaller differs from the changes list on a few shifts", 6 <= swapped <= 30,
          "%d shifts" % swapped)
    for (desk, day, sh), lst in cover.items():
        for sn, a, b in lst:
            a, b = max(a, w0), min(b, w1)
            q = qual[sn]
            edges = [a] + [t for t in (dt.datetime.combine(q, dt.time()), dt.datetime.combine(two_years(q), dt.time()))
                           if a < t < b] + [b]
            for x, y in zip(edges, edges[1:]):
                band = "first two years" if q <= x.date() < two_years(q) else "other"
                hours[(desk, band)] += (utc_of_local(y) - utc_of_local(x)).total_seconds() / 3600
    for w in F["hours"]:
        for band in ("first two years", "other"):
            v = hours[(w, band)]
            check("workbook: hours %s %s" % (w, band), round(v, 1) == F["hours"][w][band] and abs(
                v - F["hours_raw"][w][band]) < 1e-6, "%.3f" % v)

    # ------------------------------------------------------------------------- ask: ARS hours off
    ars = rows_csv(J("control_system", "ars_status_log_20251001_20260930.csv"))
    check("csv: ARS log read", len(ars) > 5000 and {r["server"] for r in ars} == {"ROC-A", "ROC-B"})
    ev = []
    for r in ars:
        code = r["subarea"]
        if code in sub_ws:
            tg = [code]
        elif code in old_sub:
            tg = [old_sub[code]]
        else:
            w = norm_ws(code)
            tg = sorted(s for s, x in sub_ws.items() if x == w)
        t = ts(r["logged_utc"])
        if r["server"] == "ROC-B":
            t = t.replace(tzinfo=ZoneInfo("Europe/Berlin")).astimezone(UTC).replace(tzinfo=None)
        for sa in tg:
            ev.append((t, sa, r["state"]))
    ev.sort()
    state = {}
    since = {}
    last = {}
    lo, hi = utc_of_local(w0), utc_of_local(w1)
    spans = collections.defaultdict(list)
    for t, sa, st in ev:
        if (sa, st) in last and (t - last[(sa, st)]).total_seconds() <= 2:
            continue
        last[(sa, st)] = t
        if sa not in state:
            state[sa] = "ON"
            if st == "ON":
                spans[sa].append((lo, t))
        if st == "OFF" and state[sa] == "ON":
            since[sa] = t
        elif st == "ON" and state[sa] == "OFF":
            spans[sa].append((since[sa], t))
        state[sa] = st
    for sa, st in state.items():
        if st == "OFF":
            spans[sa].append((since[sa], hi))
    qb = [dt.datetime(2025, 10, 1), dt.datetime(2026, 1, 1), dt.datetime(2026, 4, 1), dt.datetime(2026, 7, 1),
          dt.datetime(2026, 10, 1)]
    qn = ["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3"]
    off = collections.defaultdict(float)
    for sa, lst in spans.items():
        for a, b in lst:
            for k in range(4):
                x, y = max(a, utc_of_local(qb[k])), min(b, utc_of_local(qb[k + 1]))
                if y > x:
                    off[(sub_ws[sa], qn[k])] += (y - x).total_seconds() / 3600
    for w in F["ars"]:
        for q in qn:
            v = off[(w, q)]
            check("workbook: ARS off %s %s" % (w, q), round(v, 1) == F["ars"][w][q] and abs(
                v - F["ars_raw"][w][q]) < 1e-6, "%.4f" % v)

    # ------------------------------------------------------------------------- the goldens read back
    G = os.path.join(TASK, "golden")
    from pptx import Presentation
    prs = Presentation(os.path.join(G, "improvement_plan_case_2027.pptx"))
    texts = []
    chart = None
    for s in prs.slides:
        for sh in s.shapes:
            if sh.has_text_frame:
                texts.append(sh.text_frame.text)
            if getattr(sh, "has_table", False) and sh.has_table:
                for row in sh.table.rows:
                    texts.append(" | ".join(cell.text for cell in row.cells))
            if getattr(sh, "has_chart", False) and sh.has_chart:
                chart = sh.chart
    deck = "\n".join(texts)
    check("pptx: two slides", len(prs.slides) == 2)
    check("pptx: the call and its minutes", "Fund B" in deck and "{:,}".format(F["call_minutes"]) in deck)
    check("pptx: delivery begins on the workstation with the most",
          "Delivery begins on %s %s" % (F["start_ws"], F["start_ws_name"]) in deck)
    cats = list(chart.plots[0].categories)
    vals = list(chart.plots[0].series[0].values)
    check("pptx: the bar chart carries every workstation's minutes",
          {c.split()[0]: v for c, v in zip(cats, vals)} == F["b_by_ws"], str(dict(zip(cats, vals))))
    wb = openpyxl.load_workbook(os.path.join(G, "staffing_and_ars_2025-26.xlsx"), data_only=True)
    hs = {str(r[0].value).split()[0]: (r[1].value, r[2].value) for r in wb["Signaller hours"].iter_rows(min_row=5)
          if r[0].value}
    check("xlsx golden: hours sheet", all(hs[w] == (F["hours"][w]["first two years"], F["hours"][w]["other"])
                                          for w in F["hours"]))
    asheet = {str(r[0].value).split()[0]: [c.value for c in r[1:5]] for r in wb["ARS off"].iter_rows(min_row=5)
              if r[0].value}
    check("xlsx golden: ARS sheet", all(asheet[w] == [F["ars"][w][q] for q in qn] for w in F["ars"]))
    print("%d failures" % len(FAILS))
    return not FAILS


if __name__ == "__main__":
    ok = main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
    sys.exit(0 if ok else 1)
