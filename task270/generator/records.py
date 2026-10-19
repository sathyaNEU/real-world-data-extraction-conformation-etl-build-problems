"""The pack's record files as each system exports them: the Commission's eligibility lists, the candidate numbers
crosswalk, Halvorsen's written test results and work style inventory scores, the oral board ratings, the physical
ability test results, Pellwyn's situational judgement scores, the academy gradebook, the two applicant tracking
exports, the general ledger and the recruitment campaign summary. Each writer returns its row count."""
import csv
import datetime as dt

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import common as K
import world as W

PREFIX = {"2024-1": "24S", "2024-2": "24F", "2025-1": "25S", "2025-2": "25F"}
NAME = {a["code"]: a["name"] for a in K.ADMIN}
DIMENSIONS = ["Oral communication", "Problem solving", "Integrity", "Interpersonal skills", "Community orientation",
              "Composure"]


def _csv(path, header, rows, delim=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delim, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def _sheet(ws, header, rows, widths, date_cols=(), freeze=True, fmt=None, date_fmt="mm/dd/yyyy"):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE7EE")
        c.alignment = Alignment(vertical="top", wrap_text=True)
    for row in rows:
        ws.append(row)
    for i, w in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    for c in date_cols:
        for cell in ws[openpyxl.utils.get_column_letter(c + 1)][1:]:
            if isinstance(cell.value, (dt.date, dt.datetime)):
                cell.number_format = date_fmt
    for c, f in (fmt or {}).items():
        for cell in ws[openpyxl.utils.get_column_letter(c + 1)][1:]:
            cell.number_format = f
    if freeze:
        ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions


def numbers(rows, seed=W.SEED):
    """Candidate numbers (in the order candidates registered), Halvorsen and Pellwyn identifiers and the employee
    numbers the city gave the appointees. Stored on the rows."""
    rng = np.random.default_rng([seed, 21])
    hss = rng.choice(np.arange(3100000, 3999999), size=len(rows), replace=False)
    for code in PREFIX:
        own = [r for r in rows if r["adm"] == code]
        reg = rng.permutation(len(own))
        for i, r in zip(reg, own):
            r["no"] = "%s-%04d" % (PREFIX[code], int(i) + 1)
    for r, h in zip(rows, hss):
        r["hss"] = "H%d" % int(h)
        r["ng"] = None
    letters = "ABCDEFGHJKLMNPQRSTUVWXYZ"
    used = set()
    for r in rows:
        if r["sat"]["sjt"]:
            while True:
                ng = "PW%s%05d" % ("".join(letters[int(x)] for x in rng.integers(0, len(letters), 2)),
                                   int(rng.integers(0, 100000)))
                if ng not in used:
                    used.add(ng)
                    break
            r["ng"] = ng
    emp = 40810
    for klass in K.CLASS_START:
        app = sorted([r for r in rows if r["klass"] == klass], key=lambda r: r["rank"])
        for r in app:
            emp += int(rng.integers(1, 4))
            r["emp"] = emp
        emp += int(rng.integers(30, 90))
    for r in rows:
        r.setdefault("emp", None)
    return rows


def _cand_sort(r):
    return (r["adm"], r["no"])


# ------------------------------------------------------------------------------------------------- the Commission
def write_register(path, rows, seed=W.SEED):
    """The eligibility lists as certified, with each listed candidate's disposition: one row a listed candidate."""
    rng = np.random.default_rng([seed, 22])
    out = []
    for adm in K.ADMIN:
        listed = sorted([r for r in rows if r["adm"] == adm["code"] and r["rank"] is not None],
                        key=lambda r: r["rank"])
        nxt = [a for a in K.ADMIN if a["certified"] > adm["certified"]]
        expiry = nxt[0]["certified"] if nxt else dt.date(2026, 5, 12)
        for r in listed:
            st = r["status"]
            if st == "Appointed":
                ddate = K.CLASS_START[r["klass"]]
            elif st in ("Passed over - background", "Declined offer"):
                ddate = adm["certified"] + dt.timedelta(days=int(rng.integers(12, 70)))
            else:
                ddate = expiry
                st = "List expired"
            out.append([NAME[adm["code"]], r["rank"], r["no"], r["last"], r["first"], r["written"],
                        "%.2f" % r["oral"], "5.00" if r["vet"] else "0.00", "%.2f" % r["final"],
                        adm["certified"].strftime("%m/%d/%Y"), st, ddate.strftime("%m/%d/%Y"),
                        r["klass"] or "", r["emp"] or ""])
    return _csv(path, ["examination", "list_rank", "candidate_no", "last_name", "first_name", "written_test",
                       "oral_board", "veteran_credit", "final_score", "list_certified", "disposition",
                       "disposition_date", "academy_class", "employee_no"], out)


def write_crosswalk(path, rows):
    out = [[NAME[r["adm"]], r["no"], r["hss"], r["ng"] or ""] for r in sorted(rows, key=_cand_sort)]
    return _csv(path, ["examination", "candidate_no", "hss_candidate_id", "pellwyn_id"], out)


# ------------------------------------------------------------------------------------------------- Halvorsen
def write_written(path, rows):
    out = []
    for r in sorted(rows, key=lambda r: (r["adm"], r["hss"])):
        adm = [a for a in K.ADMIN if a["code"] == r["adm"]][0]
        out.append([r["hss"], r["no"], "KESS-PO-%s" % PREFIX[r["adm"]], adm["written"].isoformat(),
                    "Form %s" % r["form"], r["raw"], r["written"]])
    return _csv(path, ["hss_candidate_id", "client_reference", "hss_project", "test_date", "form", "raw_score",
                       "scaled_score"], out)


def write_inventory(path, rows, seed=W.SEED):
    """Halvorsen's work style inventory: five scales on the T metric for every candidate who completed it."""
    rng = np.random.default_rng([seed, 23])
    out = []
    for r in sorted(rows, key=lambda r: (r["adm"], r["hss"])):
        if not r["sat"]["inventory"]:
            continue
        adm = [a for a in K.ADMIN if a["code"] == r["adm"]][0]
        z = r["z"]
        span = (adm["online"][1] - adm["online"][0]).days
        day = adm["online"][0] + dt.timedelta(days=int(rng.integers(0, span + 1)))
        other = [50 + 10 * (0.45 * z[4] + 0.2 * z[1] + rng.normal(0, 0.85)),
                 50 + 10 * (0.3 * z[1] + 0.25 * z[4] + rng.normal(0, 0.9)),
                 50 + 10 * (0.55 * z[4] + rng.normal(0, 0.8)),
                 50 + 10 * (0.15 * z[0] + rng.normal(0, 0.98))]
        sc = [int(min(max(round(v), 20), 80)) for v in other]
        out.append([r["hss"], "KESS-WSI-%s" % PREFIX[r["adm"]], day.isoformat(), r["inventory"], sc[0], sc[1], sc[2],
                    sc[3]])
    return _csv(path, ["hss_candidate_id", "hss_project", "completed_on", "dependability", "stress_tolerance",
                       "teamwork", "rule_compliance", "openness"], out)


# ------------------------------------------------------------------------------------------------- the boards
def write_oral(path, rows, panel_of):
    """One row a rating: candidate, board day, panel, seat, the member and the dimension rated. A member who stood
    down for a candidate they knew left no ratings for that candidate."""
    out = []
    for r in sorted(rows, key=lambda r: (r["adm"], panel_of[r["cand"]]["day"] if r["sat"]["oral"] else dt.date.min,
                                         panel_of[r["cand"]]["panel"] if r["sat"]["oral"] else "", r["no"])):
        if not r["sat"]["oral"]:
            continue
        p = panel_of[r["cand"]]
        for seat in range(3):
            if not r["present"][seat]:
                continue
            m = p["members"][seat]
            member = m if isinstance(m, str) else "#%d" % m
            for j, dim in enumerate(DIMENSIONS):
                out.append([r["no"], p["day"].isoformat(), p["panel"], seat + 1, member, dim, int(r["ratings"][seat][j])])
    return _csv(path, ["candidate_no", "board_date", "panel", "seat", "rater", "dimension", "rating"], out)


def write_pat(path, rows, seed=W.SEED):
    """One row an attempt at the course; a candidate over the limit on the first attempt ran it again that day."""
    rng = np.random.default_rng([seed, 24])
    out = []
    for r in sorted(rows, key=_cand_sort):
        if not r["sat"]["pat"]:
            continue
        adm = [a for a in K.ADMIN if a["code"] == r["adm"]][0]
        day = adm["pat"][int(rng.integers(0, 2))]
        for n, t in ((1, r["t1"]), (2, r["t2"])):
            if t is None:
                continue
            pts = int(min(max(round(100 - (t - 160) * 0.62), 0), 100))
            out.append([r["no"], day.isoformat(), n, "%.1f" % t, "Pass" if t <= K.PAT_LIMIT else "Fail", pts])
    return _csv(path, ["candidate_no", "test_date", "attempt", "course_seconds", "result", "points"], out)


def write_sjt(path, rows, seed=W.SEED):
    """Pellwyn's export: a sheet an administration, one row a candidate who completed the trial form."""
    rng = np.random.default_rng([seed, 25])
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    n = 0
    for adm in K.ADMIN:
        own = sorted([r for r in rows if r["adm"] == adm["code"] and r["sat"]["sjt"]], key=lambda r: r["ng"])
        span = (adm["online"][1] - adm["online"][0]).days
        data = []
        for r in own:
            day = adm["online"][0] + dt.timedelta(days=int(rng.integers(0, span + 1)))
            t = dt.datetime.combine(day, dt.time(int(rng.integers(7, 23)), int(rng.integers(0, 60))))
            raw = int(min(max(round(24 + (r["sjt"] - 500) / 84 * 5.2 + rng.normal(0, 0.6)), 3), 40))
            pct = int(min(max(round(100 * (0.5 + 0.5 * np.tanh((r["sjt"] - 500) / 84 * 0.85))), 1), 99))
            data.append([r["ng"], t, "PS-1", 40, raw, r["sjt"], pct])
        ws = wb.create_sheet("%s cohort" % adm["name"])
        _sheet(ws, ["Pellwyn ID", "Completed", "Form", "Items", "Raw score", "Scaled score", "Percentile"], data,
               [13, 17, 8, 7, 10, 12, 11], date_cols=(1,), date_fmt="mm/dd/yyyy hh:mm")
        n += len(data)
    wb.save(path)
    return n


# ------------------------------------------------------------------------------------------------- the academy
OLD_LAYOUT = ("24-2", "24-3", "25-1", "25-2")
BLOCKS = ["Academics", "Report writing", "Firearms", "Defensive tactics", "Physical conditioning"]
BLOCK_W = [0.40, 0.15, 0.15, 0.15, 0.15]


def _blocks(rng, target):
    """Block scores whose weighted average, to one decimal, is the recruit's final average."""
    for _ in range(200):
        b = [round(float(min(max(target + rng.normal(0, 3.2), 50.0), 100.0)), 1) for _ in range(4)]
        a = round((target - sum(w * x for w, x in zip(BLOCK_W[1:], b))) / BLOCK_W[0], 1)
        for adj in (0.0, 0.1, -0.1, 0.2, -0.2):
            aa = round(a + adj, 1)
            if 40.0 <= aa <= 100.0 and round(BLOCK_W[0] * aa + sum(w * x for w, x in zip(BLOCK_W[1:], b)) + 1e-9, 1) == target:
                return [aa] + b
    raise RuntimeError("no blocks for %s" % target)


def write_academy(path, rows, seed=W.SEED):
    rng = np.random.default_rng([seed, 26])
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    n = 0
    for klass in K.CLASS_START:
        rec = sorted([r for r in rows if r["klass"] == klass], key=lambda r: r["emp"])
        start = K.CLASS_START[klass]
        grad = start + dt.timedelta(weeks=K.ACADEMY_WEEKS) - dt.timedelta(days=3)
        data = []
        for r in rec:
            if r["separated"] is None:
                bl = _blocks(rng, r["acad"])
                outcome, odate = "Graduated", grad
            else:
                # blocks finish in the order firearms (week 8), defensive tactics (14), report writing (18), physical
                # conditioning (24) and academics (26); a recruit who left has scores for the blocks finished
                bl = [None] * 5
                done = int(np.searchsorted([8, 14, 18, 24, 26], r["separated"], side="right"))
                why = ["resigned", "resigned", "academic", "medical"][int(rng.integers(0, 4))]
                outcome, odate = "Separated - %s" % why, start + dt.timedelta(weeks=r["separated"], days=1)
                for j in range(done):
                    bl[[2, 3, 1, 4, 0][j]] = round(float(min(max(r["acad"] + rng.normal(0, 3.0), 40.0), 100.0)), 1)
            if klass in OLD_LAYOUT:
                data.append([r["emp"], r["last"], r["first"]] + bl + [r["acad"], outcome, odate])
            else:
                avg = r["acad"] if r["separated"] is None else None
                sep = r["acad"] if r["separated"] is not None else None
                data.append([r["emp"], "%s, %s" % (r["last"], r["first"])] + bl + [avg, sep,
                            "Graduated" if r["separated"] is None else "Separated", odate])
        if klass in OLD_LAYOUT:
            ws = wb.create_sheet("Class %s" % klass)
            _sheet(ws, ["Recruit No.", "Last Name", "First Name"] + BLOCKS + ["Final Average", "Status", "Status Date"],
                   data, [11, 14, 12, 11, 11, 10, 11, 12, 12, 21, 12], date_cols=(10,),
                   fmt={c: "0.0" for c in range(3, 9)})
        else:
            ws = wb.create_sheet(klass)
            _sheet(ws, ["Employee ID", "Recruit"] + ["Block %d %s" % (i + 1, b) for i, b in enumerate(BLOCKS)] +
                   ["Weighted Average", "Average at Separation", "Outcome", "Outcome Date"],
                   data, [12, 24, 11, 12, 10, 12, 13, 12, 13, 11, 13], date_cols=(10,),
                   fmt={c: "0.0" for c in range(2, 9)})
        n += len(data)
    wb.save(path)
    return n


# ------------------------------------------------------------------------------------------------- applications
def _fmt_phone(digits, source):
    if source == "Web":
        return "(%s) %s-%s" % (digits[:3], digits[3:6], digits[6:])
    if source == "Mobile":
        return digits
    return "%s-%s-%s" % (digits[:3], digits[3:6], digits[6:])


def _name_case(s, source):
    return s.upper() if source == "Mobile" else s


def write_ats_legacy(path, legacy):
    """The old applicant tracking system's export at its retirement: every posting from January 2024, one row an
    application form (drafts included), local time."""
    out = []
    for r in sorted(legacy, key=lambda r: (r["posting"], r["app_no"])):
        title = "Police Officer" if r["track"] == "entry" else "Police Officer - Lateral Entry"
        submitted = r["t"].strftime("%m/%d/%Y %H:%M") if r["status"] != "Incomplete" else ""
        opened = dt.datetime.combine([a for a in K.ADMIN if a["code"] == r["adm"]][0]["open"], dt.time(8, 0))
        started = max(r["t"] - dt.timedelta(minutes=17 + (r["app_no"] * 37) % 90), opened).strftime("%m/%d/%Y %H:%M")
        out.append([r["posting"], title, r["app_no"], _name_case(r["last"], r["source"]),
                    _name_case(r["first"], r["source"]), r["dob"].strftime("%m/%d/%Y"), r["email"],
                    _fmt_phone(r["phone"], r["source"]), r["source"], started, submitted, r["status"]])
    return _csv(path, ["posting_no", "posting_title", "application_no", "last_name", "first_name", "date_of_birth",
                       "email", "phone", "source", "started", "submitted", "status"], out)


def write_ats_new(path, new):
    """The new system's export: one row an application on the police officer requisitions, times in UTC."""
    out = []
    for r in sorted(new, key=lambda r: r["app_id"]):
        submitted = r["utc"].strftime("%Y-%m-%dT%H:%M:%SZ") if r["status"] != "Incomplete" else ""
        mig_mobile = r.get("migrated") and r["source"] == "Mobile"
        out.append([r["req"], r["title"], r["app_id"], r["cand_id"], _name_case(r["first"], "Mobile" if mig_mobile else ""),
                    _name_case(r["last"], "Mobile" if mig_mobile else ""), r["dob"].isoformat(),
                    r["email"], "+1" + r["phone"], r["source"], submitted, r["status"], r["officer"]])
    return _csv(path, ["requisition_id", "job_title", "application_id", "candidate_id", "first_name", "last_name",
                       "birth_date", "email", "phone", "source", "submitted_at_utc", "application_status",
                       "currently_employed_peace_officer"], out)


# ------------------------------------------------------------------------------------------------- the calendar
def write_calendar(path):
    """The Commission's examination calendar: the police officer entry examinations from autumn 2023 to spring 2026."""
    out = []
    every = [dict(a, online=a.get("online")) for a in K.ADMIN] + W.OUT_OF_SCOPE
    for a in sorted(every, key=lambda a: a["written"]):
        o = a.get("online")
        opn = a.get("open") or {"2023-2": dt.date(2023, 7, 17), "2026-1": dt.date(2026, 1, 20)}[a["code"]]
        cls = a.get("close") or {"2023-2": dt.date(2023, 8, 18), "2026-1": dt.date(2026, 2, 20)}[a["code"]]
        out.append([a["name"], opn.isoformat(), cls.isoformat(), a["written"].isoformat(),
                    a["boards"][0].isoformat(), a["boards"][1].isoformat(), a["pat"][0].isoformat(),
                    a["pat"][1].isoformat(), o[0].isoformat() if o else "", o[1].isoformat() if o else "",
                    a["certified"].isoformat(), ", ".join(a.get("classes", ())) or
                    {"2023-2": "24-1", "2026-1": "26-3, 26-4"}[a["code"]]])
    return _csv(path, ["examination", "applications_open", "applications_close", "written_test", "oral_boards_from",
                       "oral_boards_to", "physical_ability_test_from", "physical_ability_test_to",
                       "online_components_from", "online_components_to", "list_certified", "academy_classes"], out)


# ------------------------------------------------------------------------------------------------- the ledger
def write_ledger(path, L):
    out = []
    for l in L:
        out.append([l["date"].isoformat(), l["period"], l["cc"], K.CC[l["cc"]], l["account"], l["vendor"], l["source"],
                    l["ref"], l["po"], "%.2f" % l["amount"], l["narration"]])
    return _csv(path, ["posting_date", "fiscal_period", "cost_center", "cost_center_name", "account", "vendor",
                       "source", "document_no", "po_number", "amount", "line_description"], out)


# ------------------------------------------------------------------------------------------------- the campaign
def write_campaign(path, seed=W.SEED):
    """Recruitment's 2025 campaign workbook: spend and reach by channel and month, and the career fairs."""
    rng = np.random.default_rng([seed, 27])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Channels"
    months = [dt.date(2025, m, 1) for m in (1, 2, 6, 7, 8)]
    chans = [("Paid social", 1.0), ("Search ads", 0.8), ("Streaming radio", 0.5), ("Billboards", 0.4),
             ("Job boards", 0.6)]
    data = []
    for m in months:
        for ch, sc in chans:
            spend = round(float(rng.uniform(1800, 5200)) * sc, 2)
            imp = int(spend * float(rng.uniform(140, 420)))
            clicks = int(imp * float(rng.uniform(0.004, 0.019)))
            started = int(clicks * float(rng.uniform(0.05, 0.12)))
            data.append([m, ch, spend, imp, clicks, started])
    _sheet(ws, ["Month", "Channel", "Spend ($)", "Impressions", "Clicks to careers page", "Applications started (pixel)"],
           data, [10, 26, 11, 13, 14, 16], date_cols=(0,), fmt={2: "#,##0.00", 3: "#,##0", 4: "#,##0", 5: "#,##0"},
           date_fmt="mmm yyyy")
    ws2 = wb.create_sheet("Career fairs")
    fairs = [(dt.date(2025, 1, 25), "Kessling State College, student union"), (dt.date(2025, 2, 8), "Kessling Civic Center"),
             (dt.date(2025, 2, 13), "Tri-County Career Expo"), (dt.date(2025, 7, 19), "Kessling Civic Center"),
             (dt.date(2025, 7, 26), "County fairgrounds, 4-H building"), (dt.date(2025, 8, 7), "Kessling State College, summer job fair")]
    rows = [[d, place, int(rng.integers(40, 160)), int(rng.integers(8, 45))] for d, place in fairs]
    _sheet(ws2, ["Date", "Event", "Visitors to the booth", "Interest cards"], rows, [11, 32, 12, 12], date_cols=(0,))
    ws3 = wb.create_sheet("Notes")
    ws3.append(["Recruitment Unit, Kessling Division of Police. Campaign figures from the agency's dashboards; "
                "'applications started' is the careers page tracking pixel, not the applicant tracking system."])
    ws3.column_dimensions["A"].width = 120
    wb.save(path)
    return len(data) + len(rows)
