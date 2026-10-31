"""Write the pack under target/ from the clean truth: each producing system's own exports, conventions and gaps."""
import csv
import datetime as dt
import io
import json
import os
from collections import defaultdict

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import postprocess as PP
import world as W

FILES = {
    "legacy": "inspections_2019-01_2024-03.csv",
    "current": "inspections_2024-03_2026-12.csv",
    "permits": "food_establishment_permits.csv",
    "roster": "food_program_staff_roster.xlsx",
    "plan": "food_safety_program_plan_2027.pdf",
    "schedule": "routine_inspection_schedule_2027.xlsx",
    "fees": "environmental_health_fee_schedule_2026.pdf",
    "capacity": "return_team_capacity_report_2026.xlsx",
    "complaints": "complaints_2024-03_2026-12.csv",
    "letters": "correspondence_log_2026.csv",
    "holidays": "county_holidays_2025-2027.json",
    "illness": "foodborne_illness_investigations_2019-2026.xlsx",
    "invoices": "permit_fee_invoices_2026.csv",
}
DISTRACTORS = ("illness", "invoices")
CREATED = "2027-01-08T17:40:00Z"


def _w(path, header, rows):
    buf = io.StringIO()
    wr = csv.writer(buf, lineterminator="\r\n")
    wr.writerow(header)
    for r in rows:
        wr.writerow(["" if x is None else x for x in r])
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())


# ------------------------------------------------------------------ derived records the exports carry
def derive(R):
    """Everything the exports need beyond the visit list: identifiers, complaint records, the dispatcher's
    reference, the paper-era entry stamps, the day-sheet log and the correspondence. Returns a dict the checks
    and the ask truth read too."""
    V, permits = R["visits"], R["permits"]
    prem = {p["pid"]: p for p in R["premises"]}
    out = {}
    # visit identifiers and the timestamps each system holds
    r = W.rng("ids2")
    leg_no, cur_no = {}, {}
    seq = defaultdict(lambda: 1000)
    order = sorted(range(len(V)), key=lambda i: (V[i]["day"], V[i]["time"], V[i]["permit"]))
    entry = {}
    rp = W.rng("paper")
    for i in order:
        v = V[i]
        if v["kind"] == "return" and v["who"] in W.RETURN_OFFICER.values() and W.CUTOVER <= v["day"] <= W.PAPER_END \
                and v["result"] != "No access":
            # the week's day sheets are handed in on Friday and keyed by the program assistant early the next week;
            # the record is stamped when it is saved
            d = v["day"] + dt.timedelta(days=7 - v["day"].weekday())          # the following Monday
            u = rp.random()
            if u < 0.30:
                d += dt.timedelta(days=1)
            elif u < 0.58:
                d += dt.timedelta(days=7)          # a week's sheets keyed late, the assistant on leave or at the counter
            while not W.working(d):
                d += dt.timedelta(days=1)
            entry[i] = dt.datetime.combine(d, dt.time(int(rp.integers(13, 17)), int(rp.integers(0, 60)),
                                                      int(rp.integers(0, 60))))
    out["entry"] = entry
    # legacy numbers in visit order, new-system ids in the order records were saved
    for i in order:
        v = V[i]
        if W.RECORD <= v["day"] < W.CUTOVER:
            y = v["day"].year
            seq[y] += 1 + (1 if r.random() < 0.06 else 0)
            leg_no[i] = "%d-%06d" % (y, seq[y])
    saved = []
    for i in order:
        v = V[i]
        if v["day"] >= W.CUTOVER:
            if i in entry:
                saved.append((entry[i], i))
            elif v["kind"] == "return" and v["result"] == "No access" and v["day"] <= W.PAPER_END and \
                    v["who"] in W.RETURN_OFFICER.values():
                continue          # a closed-premises call on a paper day sheet was never keyed
            else:
                saved.append((dt.datetime.combine(v["day"], v["time"]), i))
    saved.sort()
    n = 2410731
    for t, i in saved:
        n += 1 + (int(r.integers(1, 4)) if r.random() < 0.05 else 0)
        cur_no[i] = "INS-%07d" % n
    out["leg_no"], out["cur_no"] = leg_no, cur_no
    # complaint records: one per report; the investigation carries the report the intake desk dispatched on
    rc = W.rng("complaint-records")
    comp = []
    inv_ref = {}
    incidents = R["incidents"]
    for i, v in enumerate(V):
        if v["kind"] != "complaint" or v["day"] < W.CUTOVER:
            continue
        inc = incidents[v["incident"]]
        start = dt.datetime.combine(v["day"], v["time"])
        dispatch = start - dt.timedelta(minutes=int(rc.integers(25, 200)))
        recs = []
        for t, ch in zip(inc["times"], inc["channel"]):
            if t > start - dt.timedelta(minutes=20):
                continue
            recs.append(dict(t=t, channel=ch, permit=v["permit"], cat=inc["cat"], pri=inc["pri"], inv=i))
        if not recs:
            continue
        before = [x for x in recs if x["t"] <= dispatch] or recs[:1]
        ref = before[-1]
        pm = permits[v["permit"]]
        for x in recs:
            x["ref"] = x is ref
            x["perm_new"] = pm["new"]
            x["reported"] = _reported(rc, pm["name"], prem[pm["prem"]])
            comp.append(x)
        inv_ref[i] = ref
    comp.sort(key=lambda x: x["t"])
    cn = defaultdict(lambda: 100)
    for x in comp:
        y = x["t"].year % 100
        cn[y] += 1 + (1 if rc.random() < 0.04 else 0)
        x["id"] = "C%02d-%05d" % (y, cn[y])
    out["complaints"], out["inv_ref"] = comp, inv_ref
    # the return team's day-sheet log for 2026: completed return inspections, as written on the sheet
    rl = W.rng("daysheet")
    log = []
    for i in order:
        v = V[i]
        if v["kind"] == "return" and v["day"].year == 2026 and v["result"] != "No access" and \
                v["who"] in W.RETURN_OFFICER.values():
            pm = permits[v["permit"]]
            p = prem[pm["prem"]]
            log.append(dict(i=i, day=v["day"], who=v["who"], name=_as_written(rl, pm["name"]),
                            addr=_addr_as_written(rl, p["addr"]), result=v["result"]))
    out["daysheet"] = log
    # correspondence, 2026
    rm = W.rng("letters")
    letters = []
    for i in order:
        v = V[i]
        if v["day"].year != 2026 and not (v["day"].year == 2025 and v["day"].month == 12):
            continue
        pm = permits[v["permit"]]
        sent = W.add_working(v["day"], 1)
        if sent.year != 2026:
            continue
        if v["kind"] == "return" and v["result"] == "No access":
            letters.append(dict(sent=sent, template="RV-NA Return visit, premises closed", permit=pm["new"],
                                addressee=pm["name"], visit=v["day"], signed=v["who"]))
        elif v["kind"] == "routine" and v["result"] != "No access" and rm.random() < 0.34:
            letters.append(dict(sent=sent, template="RI-RPT Routine inspection report (mailed copy)",
                                permit=pm["new"], addressee=pm["name"], visit=v["day"], signed=v["who"]))
        elif v["kind"] == "routine" and v["result"] == "No access":
            letters.append(dict(sent=sent, template="RI-NA Routine inspection, premises closed", permit=pm["new"],
                                addressee=pm["name"], visit=v["day"], signed=v["who"]))
        elif v["kind"] == "complaint" and rm.random() < 0.5:
            letters.append(dict(sent=sent, template="CI-OUT Complaint investigation outcome", permit=pm["new"],
                                addressee=pm["name"], visit=v["day"], signed=v["who"]))
    for pm in permits:
        if pm["end"] is None and pm["new"]:
            letters.append(dict(sent=dt.date(2026, 11, 2) + dt.timedelta(days=int(rm.integers(0, 4))),
                                template="PR-REN Annual permit renewal notice", permit=pm["new"],
                                addressee=pm["name"], visit=None, signed=W.CLERK))
    letters.sort(key=lambda x: (x["sent"], x["template"], x["permit"]))
    k = 260117
    for x in letters:
        k += 1 + (1 if rm.random() < 0.03 else 0)
        x["ref"] = "L26-%06d" % k
    out["letters"] = letters
    return out


def _reported(r, name, p):
    """The establishment as the complainant named it."""
    u = r.random()
    street = p["addr"].split(" ", 1)[1]
    if u < 0.18:
        return "%s on %s" % (name.split(" #")[0], street)
    if u < 0.30:
        return name.split(" #")[0].lower()
    if u < 0.38:
        return "%s (%s)" % (name, p["city"])
    return name


def _as_written(r, name):
    u = r.random()
    if u < 0.12 and " #" in name:
        return name.split(" #")[0]
    if u < 0.22:
        return name.replace(" Restaurant", "").replace("'s", "s").replace(" & ", " and ")
    if u < 0.28:
        return name.upper()
    return name


def _addr_as_written(r, addr):
    u = r.random()
    rep = {" St": " Street", " Ave": " Avenue", " Rd": " Road", " Dr": " Drive", " Hwy": " Highway",
           " Ln": " Lane", " Blvd": " Boulevard"}
    if u < 0.25:
        for a, b in rep.items():
            if addr.endswith(a):
                return addr[: -len(a)] + b
    if u < 0.32:
        return addr.rsplit(" ", 1)[0]
    return addr


# ------------------------------------------------------------------ the exports
RES_LEG = {"Satisfactory": "SAT", "Unsatisfactory": "UNSAT", "IHH": "IHH CLOSURE", "No access": "NO ACCESS",
           "Approved": "APPROVED"}
RES_CUR = {"Satisfactory": "Satisfactory", "Unsatisfactory": "Unsatisfactory",
           "IHH": "Closed - imminent health hazard", "No access": "No access", "Approved": "Approved"}
TYP_LEG = {"routine": "ROUTINE", "return": "RETURN", "complaint": "COMPLAINT", "preopen": "PRE-OPENING"}
TYP_CUR = {"routine": "Routine", "return": "Return", "complaint": "Complaint", "preopen": "Pre-opening"}


def write_exports(R, D, target):
    V, permits = R["visits"], R["permits"]
    rows = []
    for i, no in sorted(D["leg_no"].items(), key=lambda kv: kv[1]):
        v = V[i]
        pm = permits[v["permit"]]
        t = v["time"]
        rows.append([no, pm["legacy"] or "", v["day"].strftime("%m/%d/%Y"),
                     dt.datetime.combine(v["day"], t).strftime("%I:%M %p").lstrip("0"),
                     W.initials(v["who"]), TYP_LEG[v["kind"]], v["red"], v["blue"], RES_LEG[v["result"]],
                     ""])
    _w(os.path.join(target, FILES["legacy"]),
       ["inspection_no", "permit_no", "insp_date", "time_in", "inspector", "insp_type", "red_pts", "blue_pts",
        "result", "complaint_ref"], rows)
    n_leg = len(rows)
    rows = []
    for i, no in sorted(D["cur_no"].items(), key=lambda kv: kv[1]):
        v = V[i]
        pm = permits[v["permit"]]
        t_local = D["entry"].get(i) or dt.datetime.combine(v["day"], v["time"])
        ref = D["inv_ref"].get(i)
        rows.append([no, pm["new"], W.to_utc(t_local).strftime("%Y-%m-%dT%H:%M:%SZ"), v["who"], TYP_CUR[v["kind"]],
                     v["red"], v["blue"], RES_CUR[v["result"]], ref["id"] if ref else ""])
    _w(os.path.join(target, FILES["current"]),
       ["inspection_id", "permit_id", "inspected_at_utc", "inspector_employee_no", "inspection_type", "red_points",
        "blue_points", "result", "complaint_id"], rows)
    return n_leg, len(rows)


def write_permits(R, target):
    prem = {p["pid"]: p for p in R["premises"]}
    rows = []
    for pm in sorted(R["permits"], key=lambda x: x["new"] or "~"):
        if not pm["new"]:
            continue
        p = prem[pm["prem"]]
        rows.append([pm["new"], pm["name"], p["addr"], p["city"], p["zip"],
                     p["risk"], p["type"], p["d26"], pm["start"].isoformat(),
                     pm["end"].isoformat() if pm["end"] else "", "May-Sep" if p["seasonal"] else ""])
    _w(os.path.join(target, FILES["permits"]),
       ["permit_id", "establishment", "street_address", "city", "zip", "risk_category",
        "establishment_type", "district_2026", "permit_issued", "permit_closed", "operating_months"], rows)
    return len(rows)


def write_complaints(D, target):
    rows = []
    for x in D["complaints"]:
        rows.append([x["id"], W.to_utc(x["t"]).strftime("%Y-%m-%dT%H:%M:%SZ"), x["channel"], x["perm_new"],
                     x["reported"], x["cat"], x["pri"], "Closed"])
    _w(os.path.join(target, FILES["complaints"]),
       ["complaint_id", "received_at_utc", "channel", "permit_id", "establishment_as_reported", "category",
        "priority", "status"], rows)
    return len(rows)


def write_letters(D, target):
    rows = [[x["ref"], x["sent"].isoformat(), x["template"], x["permit"], x["addressee"],
             x["visit"].isoformat() if x["visit"] else "", W.full_name(x["signed"])] for x in D["letters"]]
    _w(os.path.join(target, FILES["letters"]),
       ["letter_ref", "sent_on", "template", "permit_id", "addressee", "visit_date", "signed_by"], rows)
    return len(rows)


def write_holidays(target):
    out = {"jurisdiction": "Elkhorn County, Washington", "source": "Human Resources, observed county holidays",
           "years": {}}
    for y in (2025, 2026, 2027):
        out["years"][str(y)] = [{"date": d.isoformat(), "holiday": n} for d, n in sorted(W.holidays(y).items())]
    open(os.path.join(target, FILES["holidays"]), "w", encoding="utf-8").write(json.dumps(out, indent=2) + "\n")


HEAD = Font(name="Calibri", bold=True, size=11)
BODY = Font(name="Calibri", size=11)
FILL = PatternFill("solid", fgColor="DDEBF7")


def _sheet(ws, head, rows, widths):
    ws.append(head)
    for c in ws[1]:
        c.font, c.fill = HEAD, FILL
    for r in rows:
        ws.append(r)
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    ws.freeze_panes = "A2"


def write_roster(target):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Current staff"
    cur, sep = [], []
    for s in W.STAFF:
        first, mid, last, emp, role, hired, left, held = s
        assign = ("District %d" % held[-1][2]) if held else (
            "Return team" if "Return" in role else ("Plan review" if "Plan" in role else "Office"))
        row = [emp, "%s, %s %s." % (last, first, mid), role, assign, hired, 1.0]
        if left is None or left >= W.END:
            cur.append(row)
        else:
            sep.append([emp, "%s, %s %s." % (last, first, mid), role, assign, left, "Retirement"])
    cur.sort(key=lambda r: r[1])
    _sheet(ws, ["Employee no.", "Name", "Position", "Assignment (Dec 2026)", "Date hired", "FTE"], cur,
           [13, 26, 36, 22, 13, 7])
    for r in ws.iter_rows(min_row=2, min_col=5, max_col=5):
        for c in r:
            c.number_format = "mm/dd/yyyy"
    ws2 = wb.create_sheet("Separations 2019-2026")
    _sheet(ws2, ["Employee no.", "Name", "Position", "Last assignment", "Separation date", "Reason"], sep,
           [13, 26, 36, 18, 15, 12])
    for r in ws2.iter_rows(min_row=2, min_col=5, max_col=5):
        for c in r:
            c.number_format = "mm/dd/yyyy"
    p = os.path.join(target, FILES["roster"])
    wb.save(p)
    PP.normalize_xlsx(p, "Elkhorn County Human Resources", "2026-12-31T22:10:00Z", "2027-01-05T17:02:00Z",
                      company=W.COUNTY)
    return len(cur), len(sep)


def write_schedule(R, target):
    prem = {p["pid"]: p for p in R["premises"]}
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Schedule 2027"
    rows = []
    for s in sorted(R["schedule"], key=lambda s: (s["d27"], R["permits"][s["permit"]]["new"])):
        pm = R["permits"][s["permit"]]
        p = prem[pm["prem"]]
        rows.append([pm["new"], pm["name"], p["addr"], p["city"], p["risk"], s["d27"], s["n"]])
    _sheet(ws, ["Permit", "Establishment", "Street address", "City", "Risk category", "District 2027",
                "Routine inspections 2027"], rows, [12, 34, 26, 10, 13, 13, 23])
    ws2 = wb.create_sheet("Districts 2027")
    drows = [[d, W.DISTRICT_2027_NAME[d], W.full_name(R["insp27"][d]), R["insp27"][d]] for d in sorted(R["insp27"])]
    _sheet(ws2, ["District", "Area", "Inspector", "Employee no."], drows, [9, 34, 22, 13])
    p = os.path.join(target, FILES["schedule"])
    wb.save(p)
    PP.normalize_xlsx(p, "Valerie Wood", "2027-01-06T19:15:00Z", "2027-01-11T16:48:00Z", company=W.COUNTY)
    return len(rows)


def write_capacity(R, D, target):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Summary"
    by = defaultdict(int)
    for x in D["daysheet"]:
        by[x["who"]] += 1
    rows = []
    for side, emp in sorted(W.RETURN_OFFICER.items()):
        rows.append([W.full_name(emp), "North districts 1, 2, 3, 5, 10" if side == "north" else
                     "South districts 4, 6, 7, 8, 9, 11", by[emp], 270])
    ws.append(["Return team capacity report, calendar 2026. Completed return inspections from the officers' day "
               "sheets; capacity per officer per year from the 2024 time study."])
    ws["A1"].font = Font(name="Calibri", italic=True, size=10)
    ws.append([])
    ws.append(["Officer", "Area", "Completed return inspections 2026", "Annual capacity"])
    for c in ws[3]:
        c.font, c.fill = HEAD, FILL
    for r in rows:
        ws.append(r)
    for i, w in enumerate([22, 34, 32, 16], start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    ws2 = wb.create_sheet("Day sheet log")
    lrows = [[x["day"], W.full_name(x["who"]), x["name"], x["addr"], x["result"]]
             for x in sorted(D["daysheet"], key=lambda x: (x["day"], x["who"], x["addr"]))]
    _sheet(ws2, ["Date", "Officer", "Establishment", "Address", "Outcome"], lrows, [12, 18, 34, 26, 15])
    for r in ws2.iter_rows(min_row=2, min_col=1, max_col=1):
        for c in r:
            c.number_format = "mm/dd/yyyy"
    p = os.path.join(target, FILES["capacity"])
    wb.save(p)
    PP.normalize_xlsx(p, "Valerie Wood", "2027-01-04T18:20:00Z", "2027-01-07T23:05:00Z", company=W.COUNTY)
    return len(lrows)
