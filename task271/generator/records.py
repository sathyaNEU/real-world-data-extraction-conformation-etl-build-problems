"""The survey's files as the systems that hold them export them: the vendor's sample management file, its dialer
export, the plan's member services CRM export of the survey's activity, the vendor's interview file and the plan's
region reference."""
import csv
import datetime as dt

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font

import common as K

AGENTS_LSR = ["LSR%03d" % i for i in range(101, 129)]
AGENTS_MSC = ["MSC-%02d" % i for i in (3, 4, 6, 7, 9, 11, 12, 14, 15, 18, 21, 22)]
QUEUE = {0: "MWIS-DAY", 1: "MWIS-EVE", 2: "MWIS-SAT"}


def _talk(r, code):
    if code == 1100:
        return int(r.integers(560, 1260))
    if code == 2110:
        return int(r.integers(25, 190))
    if code == 3140:
        return int(r.integers(22, 48))
    if code == 2320:
        return int(r.integers(18, 95))
    return 0


def call_rows(w):
    """Every survey call as one record: (when, case index, centre, window, code)."""
    rows = []
    nc = iter(w["noncontact"])
    for i, row in enumerate(w["calls"]):
        cid, k, ctr, win, hit = (int(v) for v in row)
        when = w["sched"][cid][k - 1]
        if hit:
            code = 1100 if int(w["cases"][cid][5]) == 1 else 2110
            next(nc)
        else:
            code = next(nc)
        rows.append((when, cid, ctr, win, code, k))
    return rows


def write_sample(path, w):
    det = w["det"]
    out = []
    for c in w["cases"]:
        cid = int(c[0])
        out.append((det["case_no"][cid], det["member"][cid], K.CODES[int(c[1])], int(det["age"][cid]),
                    "F" if int(c[3]) == 0 else "M", det["lang"][cid], "R%d" % (w["wave"][cid] + 1),
                    "Trevanna MSC" if int(c[8]) else "Kestrelby"))
    out.sort()
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\r\n")
        wr.writerow(["case_id", "member_id", "region", "age", "sex", "preferred_language", "release", "first_contact_by"])
        wr.writerows(out)
    return len(out)


def write_dialer(path, w, rows, seed):
    """The vendor's calls to sampled members, its February pilot calls and its pre-launch test calls."""
    r = np.random.default_rng(seed + 41)
    det = w["det"]
    recs = []
    for (when, cid, ctr, win, code, k) in rows:
        if ctr != 1:
            continue
        transferred = int(w["cases"][cid][8]) == 1
        q = "MWIS-XFER" if transferred else QUEUE[win]
        recs.append((when, det["case_no"][cid], q, AGENTS_LSR[int(r.integers(0, len(AGENTS_LSR)))], code,
                     _talk(r, code), "-07:00"))
    # the pilot (February, before the change to daylight time) and the test calls of 10 April
    pilot_days = [d for d in (dt.date(2026, 2, 2) + dt.timedelta(days=i) for i in range(19)) if d.weekday() < 5]
    for p in range(1, 301):
        cno = "MW26P-%05d" % p
        day = pilot_days[int(r.integers(0, 5))]
        for k in range(int(r.integers(1, 5))):
            t = dt.time(int(r.integers(10, 19)), int(r.integers(0, 60)), int(r.integers(0, 60)))
            reached = r.random() < 0.32
            code = (1100 if r.random() < 0.88 else 2110) if reached else [3140, 3130, 3150, 2320][int(r.choice(4, p=[.5, .35, .05, .1]))]
            recs.append((dt.datetime.combine(day, t), cno, "MWIS-PILOT", AGENTS_LSR[int(r.integers(0, 8))], code,
                         _talk(r, code), "-08:00"))
            if reached:
                break
            nxt = [d for d in pilot_days if d > day]
            if not nxt:
                break
            day = nxt[int(r.integers(0, min(3, len(nxt))))]
    for t_i in range(1, 7):
        recs.append((dt.datetime(2026, 4, 10, 14, 5 + 6 * t_i, int(r.integers(0, 60))), "TEST-%04d" % t_i, "MWIS-TEST",
                     AGENTS_LSR[t_i], 1100, int(r.integers(300, 700)), "-07:00"))
    recs.sort(key=lambda x: (x[0], x[1]))
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["call_id", "case_id", "call_start", "queue", "agent", "disposition", "talk_seconds"])
        for i, (when, cno, q, ag, code, talk, off) in enumerate(recs, 1):
            wr.writerow(["C%07d" % (3_100_000 + i), cno, when.strftime("%Y-%m-%dT%H:%M:%S") + off, q, ag, code, talk])
    return len(recs)


def _ampm(t):
    h = t.hour % 12 or 12
    return "%d:%02d %s" % (h, t.minute, "AM" if t.hour < 12 else "PM")


OTHER = [("Welcome call", ["Spoke to member", "Left voicemail", "No answer"]),
         ("Care coordination outreach", ["Spoke to member", "Left voicemail", "No answer", "Line busy"]),
         ("Pharmacy refill reminder", ["Automated message delivered", "No answer"])]


def write_crm(path, w, rows, seed):
    """The member services centre's activity on sampled members over the field period, from the plan's CRM."""
    r = np.random.default_rng(seed + 51)
    det = w["det"]
    recs = []
    last_msc = {}
    for (when, cid, ctr, win, code, k) in rows:
        if ctr != 0:
            continue
        recs.append((when, det["member"][cid], "MWIS outbound call", K.CRM_RESULT[code],
                     AGENTS_MSC[int(r.integers(0, len(AGENTS_MSC)))]))
        last_msc[cid] = when
    by = {}
    for (when, cid, ctr, win, code, k) in rows:
        by.setdefault(cid, []).append((when, ctr))
    for cid, calls in by.items():
        ctrs = [c for _, c in calls]
        if 0 in ctrs and 1 in ctrs:
            first_v = min(t for t, c in calls if c == 1)
            last_m = max(t for t, c in calls if c == 0)
            day = last_m.date() + dt.timedelta(days=1)
            while day.weekday() >= 5 or day in K.HOLIDAYS:
                day += dt.timedelta(days=1)
            stamp = dt.datetime.combine(day, dt.time(16, int(r.integers(40, 59)), int(r.integers(0, 60))))
            if stamp >= first_v:
                stamp = first_v - dt.timedelta(minutes=int(r.integers(30, 180)))
            recs.append((stamp, det["member"][cid], "MWIS case transfer", K.CRM_TRANSFER, "MSC-SUP"))
    days = [d for d in (dt.date(2026, 4, 13) + dt.timedelta(days=i) for i in range(47))
            if d.weekday() < 5 and d not in K.HOLIDAYS]
    n = len(w["cases"])
    for j in range(1100):
        cid = int(r.integers(0, n))
        kind, results = OTHER[int(r.choice(3, p=[0.25, 0.55, 0.20]))]
        day = days[int(r.integers(0, len(days)))]
        t = dt.time(int(r.integers(9, 16)), int(r.integers(0, 60)), int(r.integers(0, 60)))
        recs.append((dt.datetime.combine(day, t), det["member"][cid], kind, results[int(r.integers(0, len(results)))],
                     AGENTS_MSC[int(r.integers(0, len(AGENTS_MSC)))]))
    recs.sort(key=lambda x: (x[0], x[1]))
    wb = Workbook()
    ws = wb.active
    ws.title = "Activity"
    head = ["Member ID", "Activity Date", "Activity Time", "Activity Type", "Result", "Agent"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
    for when, mid, kind, res, ag in recs:
        ws.append([mid, when.date(), _ampm(when.time()), kind, res, ag])
    for row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        for c in row:
            c.number_format = "m/d/yyyy"
    for col, wdt in zip("ABCDEF", (14, 13, 13, 28, 44, 10)):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:F%d" % (len(recs) + 1)
    wb.save(path)
    return len(recs)


def write_interviews(path, w, rows):
    """One row per completed interview, and one per member who declined the interview but answered the key question
    on the same call."""
    det = w["det"]
    reached = {}
    for (when, cid, ctr, win, code, k) in rows:
        if code == 1100 or (code == 2110 and w["key"][cid]):
            reached[cid] = (when, ctr, code)
    out = []
    for cid, (when, ctr, code) in reached.items():
        site = "MSC" if ctr == 0 else "LSR"
        if code == 2110:
            out.append([det["case_no"][cid], when.date().isoformat(), site, det["lang"][cid], "Declined - key question",
                        "Yes" if int(w["cases"][cid][4]) else "No"] + [""] * 12)
            continue
        h = det["hours"][cid]
        jobs = h["jobs"] + [None] * (3 - len(h["jobs"]))
        kinds = h["kinds"] + [""] * (3 - len(h["kinds"]))
        out.append([det["case_no"][cid], when.date().isoformat(), site, det["lang"][cid], "Complete", "",
                    "Yes" if h["total"] > 0 else "No", len(h["jobs"]),
                    kinds[0], "" if jobs[0] is None else jobs[0], kinds[1], "" if jobs[1] is None else jobs[1],
                    kinds[2], "" if jobs[2] is None else jobs[2], h["total"], h["looking"], h["health_limits"],
                    h["wants_help"]])
    for t_i in range(1, 7):
        out.append(["TEST-%04d" % t_i, "2026-04-10", "LSR", "English", "Complete", "", "Yes", 1, "employee", 120, "", "",
                    "", "", 120, "", "No", "No"])
    out.sort(key=lambda x: (x[1], x[0]))
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["case_id", "interview_date", "site", "language", "status", "key_80_hours_march",
                     "any_paid_work_march", "job_count", "job1_type", "job1_hours_march", "job2_type", "job2_hours_march",
                     "job3_type", "job3_hours_march", "total_hours_march", "looking_for_work", "health_limits_work",
                     "wants_navigator_help"])
        wr.writerows(out)
    return len(out)


def write_regions(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Regions"
    ws.append(["Code", "Apple Health region", "Counties"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for code, name, counties in K.REGIONS:
        ws.append([code, name, ", ".join(counties)])
    ws.column_dimensions["A"].width, ws.column_dimensions["B"].width, ws.column_dimensions["C"].width = 8, 20, 78
    wc = wb.create_sheet("Counties")
    wc.append(["County", "Region code"])
    for c in wc[1]:
        c.font = Font(bold=True)
    for county, code in sorted((cty, code) for code, _, cs in K.REGIONS for cty in cs):
        wc.append([county, code])
    wc.column_dimensions["A"].width, wc.column_dimensions["B"].width = 16, 12
    wb.save(path)
    return 10


def write_cahps(path, seed):
    """The plan's 2025 CAHPS adult Medicaid results by region (member experience; the survey's own sample)."""
    r = np.random.default_rng(seed + 101)
    wb = Workbook()
    ws = wb.active
    ws.title = "Regions 2025"
    head = ["Region", "Completed surveys", "Response rate", "Rating of health plan (9 or 10)",
            "Getting needed care (usually or always)", "Getting care quickly (usually or always)",
            "Customer service (usually or always)"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
    for code in K.CODES:
        ws.append([K.NAME[code], int(r.integers(118, 241)), round(float(r.uniform(0.17, 0.27)), 3),
                   round(float(r.uniform(0.58, 0.71)), 3), round(float(r.uniform(0.76, 0.86)), 3),
                   round(float(r.uniform(0.74, 0.85)), 3), round(float(r.uniform(0.84, 0.92)), 3)])
    for row in ws.iter_rows(min_row=2, min_col=3, max_col=7):
        for c in row:
            c.number_format = "0.0%"
    for col, wdt in zip("ABCDEFG", (18, 11, 10, 16, 18, 18, 16)):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "B2"
    wn = wb.create_sheet("Notes")
    for line in ("CAHPS Health Plan Survey 5.1H, adult Medicaid version, fielded by mail with telephone follow-up from "
                 "February to May 2025.",
                 "Sample: adult members continuously enrolled for six months to 31 December 2024, all coverage groups.",
                 "Results are the percentage of respondents giving the top answers; the plan's certified vendor's file.",
                 "Prepared by Quality Improvement for the Programs and Quality Committee, 14 August 2025."):
        wn.append([line])
    wn.column_dimensions["A"].width = 110
    wb.save(path)
    return 10
