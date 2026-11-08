"""task445 architecture 3: write the pack's data files from the world (docs.py writes the PDFs and the email)."""
import csv
import datetime as dt
import io
import os

import numpy as np
from openpyxl import Workbook

import postprocess as PP
import world as W

FILES = {
    "marks": "p2_essay_marks_2026.csv",
    "sec_a": "p2_section_a_scan_2026.csv",
    "entries": "asc_history_entries_2026.xlsx",
    "centres": "aeb_centres_register.csv",
    "code": "aeb_code_of_practice_2026.pdf",
    "minute": "history_awarding_minute_2026.pdf",
    "email": "results_certification_2026-12-01.eml",
    "reviews": "post_results_reviews_2025.csv",
    "predicted": "teacher_predicted_grades_2026.csv",
    "stats25": "p2_question_statistics_2025.xlsx",
    "markers": "aeb_markers_2026.csv",
}
DISTRACTORS = ["predicted", "stats25", "reviews"]


def _csv(path, header, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())


def _stamp(d):
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


def marks_rows(world):
    """One row per marking event. A senior examiner's re-mark is a later row for the same answer and its mark
    stands; an absent candidate is one ABSENT row; the best two essays by final mark are credited."""
    rng = np.random.default_rng(W.SEED + 7)
    markers = [m for m in world["markers"] if not m["senior"]]
    seniors = [m for m in world["markers"] if m["senior"]]
    old = {c["code"]: c.get("old_code") for c in world["centres"]}
    rows = []
    base = dt.datetime(2026, 11, 9, 22, 0)
    for x in world["cands"]:
        code = old.get(x["centre"]) or x["centre"]
        cand = x["no"]
        if "prev_no" in x:
            cand = x["prev_no"]
            code = old.get(x["prev_centre"]) or x["prev_centre"]
        if x["absent"]:
            rows.append(dict(cand=cand, centre=code, q="", mark="", credited="", event="", marker="",
                             when=base + dt.timedelta(days=float(rng.random() * 16)), status="ABSENT"))
            continue
        final = {q: x["senior"].get(q, m) for q, m in x["marks"].items()}
        best = sorted(final, key=lambda q: (-final[q], q))[:2]
        for q, m in sorted(x["marks"].items()):
            mk = markers[int(rng.integers(0, len(markers)))]
            when = base + dt.timedelta(days=float(rng.random() * 14), minutes=float(rng.integers(0, 600)))
            rows.append(dict(cand=cand, centre=code, q=q, mark=m, credited="Y" if q in best else "N",
                             event="FIRST", marker=mk["id"], when=when, status="MARKED"))
            if q in x["senior"]:
                sk = seniors[int(rng.integers(0, len(seniors)))]
                rows.append(dict(cand=cand, centre=code, q=q, mark=x["senior"][q],
                                 credited="Y" if q in best else "N", event="SENIOR", marker=sk["id"],
                                 when=when + dt.timedelta(days=float(1 + rng.random() * 3)), status="MARKED"))
    rows.sort(key=lambda r: (r["when"], r["cand"], r["q"]))
    out = []
    ev = 3300000
    for r in rows:
        ev += int(rng.integers(1, 4))
        out.append([ev, r["cand"], r["centre"], ("B" + r["q"]) if r["q"] else "", r["mark"], r["credited"], r["event"],
                    r["marker"], _stamp(r["when"]), r["status"]])
    return out


def write(target, world):
    os.makedirs(target, exist_ok=True)
    rng = np.random.default_rng(W.SEED + 11)
    _csv(os.path.join(target, FILES["marks"]),
         ["event_id", "candidate_no", "centre_code", "question", "mark", "credited", "marking_event", "marker_id",
          "marked_utc", "script_status"], marks_rows(world))
    # Section A from the scanning system: three source questions, its own item codes, local scan times
    rows = []
    for x in world["cands"]:
        if x["absent"]:
            continue
        s = x["section_a"]
        a1 = min(12, int(round(s * 12 / 40 + rng.normal(0, 0.8))))
        a2 = min(13, max(0, int(round(s * 13 / 40 + rng.normal(0, 0.8)))))
        a1 = max(0, a1)
        a3 = s - a1 - a2
        if a3 < 0 or a3 > 15:
            a3 = min(15, max(0, a3))
            a1 = min(12, max(0, s - a2 - a3))
            a2 = s - a1 - a3
        rows.append([x["no"], "H2SA-01", a1, "H2SA-02", a2, "H2SA-03", a3, a1 + a2 + a3,
                     "B%04d" % int(rng.integers(1, 2400))])
    rows.sort(key=lambda r: (r[8], r[0]))
    _csv(os.path.join(target, FILES["sec_a"]),
         ["candidate_no", "item_1", "mark_1", "item_2", "mark_2", "item_3", "mark_3", "section_a_total", "scan_batch"],
         rows, crlf=True)
    # the entries register (Excel): a moved candidate's first entry withdrawn, the new entry under a new number
    wb = Workbook()
    ws = wb.active
    ws.title = "Entries"
    ws.append(["Candidate number", "Previous candidate number", "Centre", "Entry status", "Components",
               "Entered on"])
    ent = []
    for x in world["cands"]:
        if "prev_no" in x:
            ent.append([x["prev_no"], None, x["prev_centre"], "WITHDRAWN", "P1;P2",
                        dt.date(2026, 5, 1) + dt.timedelta(days=int(rng.integers(0, 40)))])
            ent.append([x["no"], x["prev_no"], x["centre"], "ENTERED", "P1;P2",
                        dt.date(2026, 7, 20) + dt.timedelta(days=int(rng.integers(0, 60)))])
        else:
            ent.append([x["no"], None, x["centre"], "ENTERED", "P1;P2",
                        dt.date(2026, 5, 1) + dt.timedelta(days=int(rng.integers(0, 40)))])
    for r in sorted(ent, key=lambda r: r[0]):  # noqa: E501
        ws.append(r)
        ws.cell(row=ws.max_row, column=6).number_format = "dd/mm/yyyy"
    for col, w in zip("ABCDEF", (18, 24, 10, 13, 12, 12)):
        ws.column_dimensions[col].width = w
    p = os.path.join(target, FILES["entries"])
    wb.save(p)
    PP.normalize_ooxml(p, "Pamela Sullivan", "Pamela Sullivan", "2026-05-04T23:12:00Z", "2026-11-28T05:41:00Z",
                       excel=True)
    # the centres register
    rows = []
    for c in sorted(world["centres"], key=lambda c: c["code"]):
        rows.append([c["code"], c.get("old_code", ""), c["name"], c["region"], c["region_name"], c["country"], c["tz"]])
    _csv(os.path.join(target, FILES["centres"]),
         ["centre_code", "merged_from", "centre_name", "region_code", "region", "country", "time_zone"], rows)
    # the 2025 post-results reviews, one row per component, stamped in UTC
    rows = []
    old = {c["code"]: c.get("old_code") for c in world["centres"]}
    for r in W.reviews_2025(world):
        code = old.get(r["centre"]) if (old.get(r["centre"]) and r["local"] < dt.datetime(2026, 2, 1)) else r["centre"]
        rows.append([r["request"], r["candidate"], code, r["component"], _stamp(r["utc"]), r["outcome"]])
    rows.sort(key=lambda r: (r[4], r[0], r[3]))
    _csv(os.path.join(target, FILES["reviews"]),
         ["request_id", "candidate_no", "centre_code", "component", "requested_utc", "outcome"], rows)
    # distractors: the teachers' predicted grades, and the 2025 paper's question statistics
    rows = []
    for x in world["cands"]:
        if rng.random() < 0.93:
            g = x["a"] + rng.normal(0.25, 0.7)
            pg = "A" if g > 1.2 else "B" if g > 0.4 else "C" if g > -0.4 else "D" if g > -1.2 else "E"
            rows.append([x["no"], x["centre"], pg])
    _csv(os.path.join(target, FILES["predicted"]), ["candidate_no", "centre_code", "predicted_grade"], rows)
    wb = Workbook()
    ws = wb.active
    ws.title = "Paper 2 2025"
    ws.append(["Question", "Max", "Answers", "Mean", "SD", "Facility"])
    stats = [("1", 12, 29410, 7.62, 2.31), ("2", 13, 29410, 8.04, 2.47), ("3", 15, 29410, 8.71, 3.02),
             ("4", 25, 25120, 13.48, 4.86), ("5", 25, 24410, 13.92, 4.71), ("6", 25, 10230, 12.87, 4.95)]
    for q, mx, n, mean, sd in stats:
        ws.append(["Q" + q, mx, n, mean, sd, round(mean / mx, 3)])
    p = os.path.join(target, FILES["stats25"])
    wb.save(p)
    PP.normalize_ooxml(p, "Mary Deleon", "Mary Deleon", "2025-12-03T01:20:00Z", "2025-12-03T02:05:00Z", excel=True)
    rows = [[m["id"], m["team"], m["tz"], "Senior examiner" if m["senior"] else "Examiner"] for m in world["markers"]]
    _csv(os.path.join(target, FILES["markers"]), ["marker_id", "team", "home_time_zone", "role"], rows)
