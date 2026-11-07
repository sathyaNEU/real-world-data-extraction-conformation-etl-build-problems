"""task145 architecture 2: the independent verifier. Reads only the bundle (target/ and golden/) on its own code path
(pandas tables, the bell schedule and the seat schedule read back from their PDFs, its own run and leaver logic), never
analysis.py or the generator's truth, and recomputes every graded figure against figures.json.

    python3 task145/generator/verify.py
"""
import datetime as dt
import email
import json
import os
import re
import subprocess
import sys

import openpyxl
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GD = os.path.join(TASK, "golden")
FAIL = []


def ok(label, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + label + (("  [" + detail + "]") if detail and not cond else ""))
    if not cond:
        FAIL.append(label)


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout


NO = {"0412": "CPP", "0418": "RBA", "0427": "MVH", "0433": "SHC"}
NAME = {"Cottonwood Plains Preparatory": "CPP", "Riverbend Academy": "RBA", "Mesa Vista High School": "MVH",
        "Sandhill Collegiate": "SHC"}
LEG = {"Cottonwood Plains Prep": "CPP", "Riverbend Acad": "RBA", "Mesa Vista HS": "MVH", "Sandhill Coll": "SHC"}
YEARS = {"2023-24": ("2023-08-14", "2023-12-20", "2024-01-08"), "2024-25": ("2024-08-12", "2024-12-19", "2025-01-06"),
         "2025-26": ("2025-08-13", "2025-12-19", "2026-01-05"), "2026-27": ("2026-08-12", "2026-12-18", "2027-01-05")}
YEARS = {k: tuple(dt.date.fromisoformat(x) for x in v) for k, v in YEARS.items()}
HIST = ["2023-24", "2024-25", "2025-26"]
CUR = "2026-27"
D = dt.timedelta


def school_year(d):
    for y, (f, fe, ss) in YEARS.items():
        if f <= d <= dt.date(ss.year, 6, 30):
            return y
    return None


def bells():
    txt = pdf_text(os.path.join(T, "bell_schedules_2026-27.pdf"))
    am = int(re.search(r"Morning\s.*?(\d{3})\s*$", txt, re.M).group(1))
    pm = int(re.search(r"Afternoon\s.*?(\d{3})\s*$", txt, re.M).group(1))
    std_part = txt.split("Monday, Tuesday, Thursday and Friday")[1].split("Wednesday block day")[0]
    wed_part = txt.split("Wednesday block day")[1]
    std = [(m.group(1), int(m.group(2))) for m in re.finditer(r"^\s*(\d|Advisory)\s+(\d+)\s*$", std_part, re.M)]
    wed = [(m.group(1), int(m.group(2))) for m in re.finditer(r"^\s*([A-D])\s+(\d+)\s*$", wed_part, re.M)]
    std = [("ADV" if n == "Advisory" else n, v) for n, v in std]
    return am, pm, dict(std), dict(wed)


def tiers():
    txt = pdf_text(os.path.join(T, "pathwise_schedule_B_spring_2027.pdf"))
    return [(m.group(1), int(m.group(2)), int(m.group(3).replace(",", "")))
            for m in re.finditer(r"(Tier \d)\s+(\d+)\s+([\d,]+)", txt)]


def calendars():
    wb = openpyxl.load_workbook(os.path.join(T, "instructional_calendars_2023-24_to_2026-27.xlsx"), read_only=True)
    cal = {}
    for ws in wb.worksheets:
        rows = list(ws.values)
        h = next(i for i, r in enumerate(rows) if r and r[0] == "Date")
        cols = {NAME[c]: j for j, c in enumerate(rows[h]) if c in NAME}
        for s in cols:
            cal[(ws.title, s)] = set()
        for r in rows[h + 1:]:
            if r and r[0] is not None:
                d = r[0].date() if hasattr(r[0], "date") else r[0]
                for s, j in cols.items():
                    if r[j] == "Instructional":
                        cal[(ws.title, s)].add(d)
    return cal


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    am, pm, mstd, mwed = bells()
    ok("bell schedule read back from its PDF", am == 200 and pm == 175 and sum(mstd.values()) == 375 and
       sum(mwed.values()) == 352, "%s %s %s %s" % (am, pm, mstd, mwed))
    tr = tiers()
    ok("seat schedule read back from its PDF", len(tr) == 3 and tr[0][1] == 125, str(tr))
    cal = calendars()
    ok("calendars read back: every school a sheet a year", len(cal) == 16)

    def day_minutes(s, d):
        if s == "MVH":
            return (mwed if d.weekday() == 2 else mstd)
        return {"AM": am, "PM": pm}

    # absences: (year, local id, school) -> {date: code}
    ab = {}
    leg = pd.read_csv(os.path.join(T, "attendance_absences_2023-24.csv"), dtype=str)
    for r in leg.itertuples(index=False):
        if r.Reason == "School activity":
            continue
        s = LEG[r.School]
        d = dt.datetime.strptime(r._2, "%m/%d/%Y").date()
        tot = sum(day_minutes(s, d).values())
        if int(r._3) * 2 >= tot:
            ab.setdefault(("2023-24", r._0, s), {})[d] = r.Reason
    new = pd.read_csv(os.path.join(T, "attendance_absences_2024-25_to_2026-27.csv"), dtype=str)
    for lid, sn, ds, por, code in zip(new.local_id, new.school_number, new.absence_date, new.portion, new.code):
        if code == "ACT":
            continue
        s = NO[sn]
        d = dt.date.fromisoformat(ds)
        parts = day_minutes(s, d)
        tot = sum(parts.values())
        m = tot if por == "FULL" else (sum(parts[x] for x in por[4:].split(",")) if por.startswith("PER:")
                                       else parts[por])
        if m * 2 >= tot:
            ab.setdefault((school_year(d), lid, s), {})[d] = code
    ok("both attendance layouts read", len(leg) > 1000 and len(new) > 25000, "%d %d" % (len(leg), len(new)))

    en = pd.read_csv(os.path.join(T, "enrollment_records_2023-24_to_2026-27.csv"), dtype=str).fillna("")
    sid_by_name = {}
    for r in en.itertuples(index=False):
        if r.state_id:
            sid_by_name[(r.last_name.lower(), r.first_name.lower(), r.birth_date)] = r.state_id
    recs = []
    for r in en.itertuples(index=False):
        nm = (r.last_name.lower(), r.first_name.lower(), r.birth_date)
        recs.append(dict(year=r.school_year, lid=r.local_id, s=NO[r.school_number], grade=int(r.grade),
                         entry=dt.date.fromisoformat(r.entry_date),
                         exit=dt.date.fromisoformat(r.exit_date) if r.exit_date else None, code=r.exit_code,
                         key=r.state_id or sid_by_name.get(nm, "|".join(nm)), nm=nm))
    by = {}
    for r in recs:
        by.setdefault((r["year"], r["key"]), []).append(r)
    for rs in by.values():
        rs.sort(key=lambda x: x["entry"])
        for i, r in enumerate(rs):
            nxt = rs[i + 1]["entry"] if i + 1 < len(rs) else None
            r["end"] = r["exit"] if nxt is None else (min(r["exit"], nxt - D(days=1)) if r["exit"] else nxt - D(days=1))
    req = pd.read_csv(os.path.join(T, "registrar_records_requests_2023-2026.csv"), dtype=str)
    reqd = {}
    for r in req.itertuples(index=False):
        k = (r.student_last_name.lower(), r.student_first_name.lower(),
             dt.datetime.strptime(r.student_dob, "%m/%d/%Y").date().isoformat())
        reqd.setdefault(k, []).append(dt.date.fromisoformat(r.received))
    gr = pd.read_csv(os.path.join(T, "course_grades_2023-24_to_2026-27.csv"), dtype=str)
    fails = gr[(gr.term == "S1") & (gr.grade == "F")].groupby(["school_year", "local_id"]).size().to_dict()

    # each student's fall: one read of each day, missed only when absent at every school enrolled that day
    feat = {}
    for (y, k), rs in by.items():
        fe = YEARS[y][1]
        day = {}
        f = 0
        for r in rs:
            a = ab.get((y, r["lid"], r["s"]), {})
            for d in sorted(cal[(y, r["s"])]):
                if d >= r["entry"] and d <= fe and (r["end"] is None or d <= r["end"]):
                    day[d] = day.get(d, True) and d in a
            f += fails.get((y, r["lid"]), 0)
        seq = [day[d] for d in sorted(day)] + [False]
        runs, n = 0, 0
        for x in seq:
            if x:
                n += 1
            else:
                runs += n >= 5
                n = 0
        feat[(y, k)] = (min(runs, 2), min(f, 2))

    def on_roll(y):
        ss = YEARS[y][2]
        return {k for (yy, k), rs in by.items() if yy == y and any(r["entry"] <= ss and (r["end"] is None or
                                                                                          r["end"] >= ss) for r in rs)}

    leave = {"DO", "GE", "EX", "W3", "W5", "W9"}
    transfer = {"TI", "TO", "TU", "W1", "W2", "WT"}
    out = {}
    for y in HIST:
        ss = YEARS[y][2]
        end = dt.date(ss.year, 6, 30)
        for k in on_roll(y):
            rs = by[(y, k)]
            left = False
            for i, r in enumerate(rs):
                if not (r["exit"] and ss <= r["exit"] <= end):
                    continue
                if any(x["entry"] >= r["exit"] and x["s"] != r["s"] for x in rs[i + 1:]):
                    continue
                if r["code"] in leave:
                    left = True
                elif r["code"] in transfer:
                    left = left or not any(r["exit"] <= g <= r["exit"] + D(days=45) for g in reqd.get(r["nm"], []))
            out[(y, k)] = left
    hl = {y: sum(v for (yy, k), v in out.items() if yy == y) for y in HIST}
    ok("closed springs' leavers", hl == fig["hist_leavers"], "%s %s" % (hl, fig["hist_leavers"]))
    num, den = {}, {}
    for kk, v in out.items():
        c = feat[kk]
        num[c] = num.get(c, 0) + v
        den[c] = den.get(c, 0) + 1
    cur = on_roll(CUR)
    ok("students on roll for 5 January 2027", len(cur) == fig["on_roll"], "%d" % len(cur))
    exp = sum(num.get(feat[(CUR, k)], 0) / den[feat[(CUR, k)]] for k in cur)
    ok("expected spring 2027 leavers", abs(exp - fig["expected_unrounded"]) < 1e-6 and round(exp) ==
       fig["call"]["expected"], "%.4f" % exp)
    tier = next(t for t, s, p in tr if exp <= s)
    ok("tier from the seat schedule", tier == fig["call"]["tier"], tier)
    wr = sum(1 for k in cur if feat[(CUR, k)][0] > 0)
    ok("students on roll with a run", wr == fig["with_run"], str(wr))
    for r, key in ((0, "rate_no_run"), (1, "rate_one_run"), (2, "rate_two_runs")):
        n = sum(v for c, v in num.items() if c[0] == r)
        d = sum(v for c, v in den.items() if c[0] == r)
        ok("closed springs' leaving rate, %d runs" % r, round(100.0 * n / d, 1) == fig[key])

    # the asks: suspension days from the behaviour log, one row per student and start, the last entered standing
    bh = pd.read_csv(os.path.join(T, "behavior_incidents_2023-24_to_2026-27.csv"), dtype=str)
    oss = bh[bh.action == "OSS"].sort_values("entered_utc").groupby(["local_id", "action_start"]).tail(1)
    rec_by_lid = {(r["year"], r["lid"]): r for r in recs}
    od = {}
    for lid, sn, st, n in zip(oss.local_id, oss.school_number, oss.action_start, oss.action_days):
        d0 = dt.date.fromisoformat(st)
        y = school_year(d0)
        s = NO[sn]
        rc = rec_by_lid.get((y, lid))
        for x in sorted(d for d in cal[(y, s)] if d >= d0)[:int(n)]:
            if rc is not None and rc["end"] is not None and x > rc["end"]:
                continue
            od.setdefault((y, lid, s), set()).add(x)
    months = {8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    for s in NAME.values():
        for m, mn in months.items():
            v = sum(1 for (y, lid, ss), ds in od.items() if y == CUR and ss == s for x in ds if x.month == m and
                    x <= YEARS[CUR][1])
            ok("ask B %s %s" % (s, mn), v == fig["ask_b"]["%s %s" % (s, mn)], "%d" % v)

    def chronic(y):
        fe = YEARS[y][1]
        per = {}
        for r in recs:
            if r["year"] != y:
                continue
            days = [d for d in cal[(y, r["s"])] if r["entry"] <= d <= fe and (r["end"] is None or d <= r["end"])]
            a = set(ab.get((y, r["lid"], r["s"]), {})) | od.get((y, r["lid"], r["s"]), set())
            p = per.setdefault((r["s"], r["key"]), [0, 0, r["grade"]])
            p[0] += len(days)
            p[1] += sum(1 for d in days if d in a)
            p[2] = r["grade"]
        cells = {}
        for (s, k), (n, a, g) in per.items():
            if n >= 10:
                c = cells.setdefault((s, g), [0, 0])
                c[0] += a * 10 >= n
                c[1] += 1
        return cells
    cc = chronic(CUR)
    for (s, g), (ch, n) in sorted(cc.items()):
        ok("ask A %s grade %d" % (s, g), round(100.0 * ch / n, 1) == fig["ask_a"]["%s %d" % (s, g)] and
           [ch, n] == fig["ask_a_counts"]["%s %d" % (s, g)], "%d/%d" % (ch, n))
    for y in ("2025-26", CUR):
        c = chronic(y)
        v = round(100.0 * sum(x[0] for x in c.values()) / sum(x[1] for x in c.values()), 1)
        ok("network fall chronic absence %s" % y, v == fig["chronic_fall"][y], "%.1f" % v)

    # every other format and document read back
    msg = email.message_from_string(open(os.path.join(T, "bridge_seats_for_spring.eml"), encoding="utf-8").read())
    ok("request email parses", msg["Subject"] == "Bridge seats for spring" and "Pathwise" in msg.get_payload())
    jf = pdf_text(os.path.join(T, "board_policy_JF-7_bridge_program.pdf"))
    ok("JF-7 read back: the 45-day records test and the smallest tier", "45 days" in jf and "smallest tier" in jf)
    jh = pdf_text(os.path.join(T, "attendance_regulation_JH-R_2026-27.pdf"))
    ok("JH-R read back: the half-day rule and the 10 per cent line", "half or more" in jh and "10 per cent" in jh)
    sv = openpyxl.load_workbook(os.path.join(T, "school_climate_survey_spring_2026.xlsx"), read_only=True)
    ok("climate survey opens", sv.worksheets[0].max_row >= 7)
    tx = pd.read_csv(os.path.join(T, "family_texts_fall_2026.csv"), dtype=str)
    ok("family texts parse", len(tx) > 1000 and set(tx.template) == {"UNEXCUSED_ABSENCE"})
    rt = pd.read_csv(os.path.join(T, "transportation_routes_2026-27.csv"), dtype=str)
    ok("transport routes parse", len(rt) > 100)
    codes = pd.read_csv(os.path.join(T, "sis_code_reference.csv"), dtype=str).fillna("")
    ok("code reference carries every exit code in the enrolment file",
       set(en.exit_code[en.exit_code != ""]) <= set(codes[codes.code_table == "exit"].code))
    bp = pdf_text(os.path.join(GD, "bridge_2027_board_paper.pdf"))
    ok("board paper states the tier and the number", fig["call"]["tier"] in bp and
       ("about %d" % fig["call"]["expected"]) in bp)
    wb = openpyxl.load_workbook(os.path.join(GD, "attendance_figures_2026.xlsx"), data_only=True)
    ws = wb["Chronic absence"]
    vals = {}
    for r in ws.iter_rows(min_row=5, max_row=8, values_only=True):
        for g, v in zip((9, 10, 11, 12), r[1:5]):
            vals["%s %d" % (NAME[r[0]], g)] = v
    ok("workbook chronic absence sheet equals the figures", vals == fig["ask_a"])
    ws2 = wb["Suspension days"]
    vb = {}
    for r in ws2.iter_rows(min_row=5, max_row=8, values_only=True):
        for mn, v in zip(months.values(), r[1:6]):
            vb["%s %s" % (NAME[r[0]], mn)] = v
    ok("workbook suspension sheet equals the figures", vb == fig["ask_b"])
    print("verify: %d failure(s)" % len(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
