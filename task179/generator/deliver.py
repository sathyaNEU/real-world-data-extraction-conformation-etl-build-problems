"""task179 goldens: the projection workbook and the teaching-groups chart, figures.json, submission.md and
metadata.json, every figure computed once here from the pack."""
from __future__ import annotations

import json
import os

import numpy as np

import common as C
import calc

FAC_NAME = dict(C.FACULTIES)
FAC_SHORT = {"ASS": "Arts and Social Sciences", "BUS": "Business and Law", "SCI": "Science",
             "ENG": "Engineering and Computing", "HLT": "Health Sciences"}


def r250(x):
    return int(250 * round(x / 250.0))


def compute(target):
    r = calc.compute(target)
    a = r["frame"]
    f = a[a["intake"] == 2026]
    o = dict(r)
    o["call_r"] = r250(r["call"])
    o["no_repeat_2026"] = int((f["ties"] == 0).sum())
    hist = []
    for y in range(2019, 2026):
        h = a[a["intake"] == y]
        hist.append((y, int(len(h)), int(h["gone"].sum())))
    o["hist"] = hist
    return o


def figures(o):
    F = {"call_not_enrolled_2027": o["call_r"],
         "_unrounded": {"call_not_enrolled_2027": round(o["call"], 1)},
         "cc1_intake_2026_at_census": o["n2026"],
         "cc2_intake_2026_no_repeat_classmate": o["no_repeat_2026"]}
    for fc in C.FAC_CODES:
        n, big = o["groups"][fc]
        F["ask_groups_s1_2026_%s" % fc.lower()] = n
        F["ask_groups_over30_s1_2026_%s" % fc.lower()] = big
    for fc in C.FAC_CODES:
        for yv in (2, 3, 4):
            F["ask_continuing_2026_%s_y%d" % (fc.lower(), yv)] = o["cont"].get((fc, yv), 0)
    F["label_groups_30_or_fewer"] = {fc.lower(): o["groups"][fc][0] - o["groups"][fc][1] for fc in C.FAC_CODES}
    F["hist_intake_entrants_not_enrolled"] = [list(x) for x in o["hist"]]
    return F


def write_workbook(path, o):
    import xlsx_writer as XW
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    wb = Workbook()
    ws = wb.active
    ws.title = "Projection"
    bold = Font(bold=True)
    fill = PatternFill("solid", fgColor="D9E1F2")
    ws["A1"] = "Continuing enrolment projection 2027: first-year intake"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Planning and Insight, prepared 16 October 2026 from the 1 October 2026 census"
    rows = [("2026 intake enrolled at the 1 October 2026 census", o["n2026"]),
            ("Projected not enrolled at the 1 October 2027 census (nearest 250)", o["call_r"]),
            ("Model sum of probabilities", round(o["call"], 1)),
            ("2026 entrants meeting no other entrant in two or more classes", o["no_repeat_2026"])]
    for i, (k, v) in enumerate(rows, 4):
        ws.cell(row=i, column=1, value=k)
        c = ws.cell(row=i, column=2, value=v)
        c.number_format = "#,##0.0" if isinstance(v, float) else "#,##0"
    ws.cell(row=5, column=1).font = bold
    ws.cell(row=5, column=2).font = bold
    ws.cell(row=9, column=1, value="Earlier intakes").font = bold
    for j, h in enumerate(["Intake", "Entrants at census", "Not enrolled at next census", "Share"], 1):
        c = ws.cell(row=10, column=j, value=h)
        c.font = bold
        c.fill = fill
    for i, (y, n, g) in enumerate(o["hist"], 11):
        ws.cell(row=i, column=1, value=y)
        ws.cell(row=i, column=2, value=n).number_format = "#,##0"
        ws.cell(row=i, column=3, value=g).number_format = "#,##0"
        ws.cell(row=i, column=4, value="=C%d/B%d" % (i, i)).number_format = "0.0%"
    ws.column_dimensions["A"].width = 62
    for col in "BCD":
        ws.column_dimensions[col].width = 16
    ws2 = wb.create_sheet("Teaching groups S1 2026")
    head = ["Faculty", "Teaching groups", "Over 30 students", "30 or fewer"]
    for j, h in enumerate(head, 1):
        c = ws2.cell(row=1, column=j, value=h)
        c.font = bold
        c.fill = fill
    for i, fc in enumerate(C.FAC_CODES, 2):
        n, big = o["groups"][fc]
        ws2.cell(row=i, column=1, value=FAC_SHORT[fc])
        ws2.cell(row=i, column=2, value=n)
        ws2.cell(row=i, column=3, value=big)
        ws2.cell(row=i, column=4, value="=B%d-C%d" % (i, i))
    ws2.cell(row=7, column=1, value="Total").font = bold
    for col in "BCD":
        ws2["%s7" % col] = "=SUM(%s2:%s6)" % (col, col)
        ws2["%s7" % col].font = bold
    ws2.column_dimensions["A"].width = 28
    for col in "BCD":
        ws2.column_dimensions[col].width = 17
    ws3 = wb.create_sheet("Continuing 2026 census")
    head = ["Faculty", "Year 2", "Year 3", "Year 4 or later", "Total"]
    for j, h in enumerate(head, 1):
        c = ws3.cell(row=1, column=j, value=h)
        c.font = bold
        c.fill = fill
    for i, fc in enumerate(C.FAC_CODES, 2):
        ws3.cell(row=i, column=1, value=FAC_SHORT[fc])
        for j, yv in enumerate((2, 3, 4), 2):
            ws3.cell(row=i, column=j, value=o["cont"].get((fc, yv), 0)).number_format = "#,##0"
        ws3.cell(row=i, column=5, value="=SUM(B%d:D%d)" % (i, i)).number_format = "#,##0"
    ws3.cell(row=7, column=1, value="Total").font = bold
    for col in "BCDE":
        ws3["%s7" % col] = "=SUM(%s2:%s6)" % (col, col)
        ws3["%s7" % col].number_format = "#,##0"
        ws3["%s7" % col].font = bold
    ws3.column_dimensions["A"].width = 28
    ws4 = wb.create_sheet("Notes")
    notes = [
        "Definitions follow Continuing Enrolment Projection 2027: Conventions (Planning and Insight, 5 October 2026).",
        "Intake: first-time bachelor's entrants with an enrolled programme attempt at the 1 October census; entrants "
        "with credit are excluded. Approved leave counts as not enrolled.",
        "Earlier intakes: enrolment at the next census from the census history; the 2025 intake through the "
        "SIRIUS to ARC crosswalk.",
        "Projection: logistic model fitted on the 2019 to 2025 intakes (admissions attributes, week-6 progress check, "
        "faculty, and the number of other entrants met in two or more Semester 1 classes, banded), applied to the "
        "2026 intake; reported to the nearest 250.",
        "Teaching groups: active Semester 1 2026 classes meeting in one room, on one day, at one start, over the same "
        "teaching weeks count as one group; size is the census enrolment of its classes.",
        "Continuing students: one row per student at the 2026 census; an attempt left enrolled after a transfer "
        "approved in ARC is not counted; conjoint students in the first-listed programme's faculty.",
        "Sources: Registry census history and first-year cohort extracts; Admissions; Student Success week-6 "
        "progress check; Timetabling Semester 1 2026 timetable at the census; Academic Office catalogue; Registry "
        "transfers register.",
    ]
    ws4["A1"] = "Notes"
    ws4["A1"].font = bold
    for i, t in enumerate(notes, 3):
        ws4.cell(row=i, column=1, value=t).alignment = Alignment(wrap_text=True, vertical="top")
    ws4.column_dimensions["A"].width = 110
    for ws_ in (ws2, ws3):
        ws_.freeze_panes = "A2"
    wb.save(path)
    import postprocess as PP
    PP.normalize_ooxml(path, "Cillian Coholan", "Cillian Coholan", "2026-10-15T22:05:00Z", "2026-10-16T03:31:00Z",
                       excel=True)


def write_chart(path, o):
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams["svg.hashsalt"] = "task179"
    import matplotlib.pyplot as plt
    labels = [FAC_SHORT[f].replace(" and ", " and\n") for f in C.FAC_CODES]
    small = [o["groups"][f][0] - o["groups"][f][1] for f in C.FAC_CODES]
    big = [o["groups"][f][1] for f in C.FAC_CODES]
    fig, ax = plt.subplots(figsize=(8.6, 5.2), dpi=110)
    x = np.arange(len(labels))
    b1 = ax.bar(x, small, 0.62, color="#9db9d8", label="30 students or fewer")
    b2 = ax.bar(x, big, 0.62, bottom=small, color="#2f5d8c", label="More than 30 students")
    for i in range(len(x)):
        ax.text(x[i], small[i] / 2, "{:,}".format(small[i]), ha="center", va="center", fontsize=9)
        ax.text(x[i], small[i] + big[i] / 2, "{:,}".format(big[i]), ha="center", va="center", fontsize=9, color="white")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Teaching groups")
    ax.set_title("Arts and Social Sciences ran %s of the university's %s Semester 1 groups; most groups over 30 are upper-level"
                 % ("{:,}".format(o["groups"]["ASS"][0]), "{:,}".format(sum(o["groups"][f][0] for f in C.FAC_CODES))),
                 fontsize=10, loc="left")
    fig.text(0.01, 0.01, "Source: Timetabling, Semester 1 2026 timetable at the 1 October 2026 census. Groups as taught.",
             fontsize=7.5, color="#555555")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def write_submission(path, o, F):
    g = o["groups"]
    cont = o["cont"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Education and learning sciences, learning analytics and early-warning models.  ")
    L.append("**Analytical objective:** Forecasting and predictive modeling.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Plan for about %s of the %s first-time entrants enrolled at the 1 October 2026 census not to be "
             "enrolled at the 1 October 2027 census, to the nearest 250.**" % ("{:,}".format(o["call_r"]),
                                                                              "{:,}".format(o["n2026"])))
    L.append("The figure reads each entrant's chance at the number of other entrants met in two or more of the "
             "entrant's own Semester 1 classes, and %s of the 2026 entrants meet no other entrant twice. Not an "
             "early-warning model on entrant attributes and week-6 ratings alone, validated on intakes in which most "
             "full-time entrants shared three classes with the same 27 others. Not the earlier intakes' rate, for "
             "the same reason." % "{:,}".format(o["no_repeat_2026"]))
    L.append("")
    L.append("## 2. Critical Components\n")
    L.append("1. First-time entrants enrolled at the 1 October 2026 census: **%s**" % "{:,}".format(o["n2026"]))
    L.append("2. 2026 entrants who meet no other entrant in two or more of their classes: **%s**"
             % "{:,}".format(o["no_repeat_2026"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Took each intake's first-time entrants (Entry Basis First-time) from admissions_entrants_2019_2026.xlsx "
             "with an enrolled attempt at their own census in census_enrolments_2019_2026.csv: %s in 2026."
             % "{:,}".format(o["n2026"]))
    L.append("2. Marked each 2019 to 2025 entrant not enrolled at the next census when no EN or Enrolled attempt is "
             "there (leave is not enrolled, per the conventions), the 2025 intake through "
             "sirius_arc_student_crosswalk.csv.")
    L.append("3. Counted for every entrant the other entrants of the same intake met in two or more of the entrant's "
             "Semester 1 classes (sirius_fy_cohort_classes_2019_2025.csv by term and class number, "
             "arc_s1_2026_first_year_classes.csv by class code): %s of the 2026 entrants meet none."
             % "{:,}".format(o["no_repeat_2026"]))
    L.append("4. Fitted a logistic model of not being enrolled at the next census on the 2019 to 2025 entrants: ASC "
             "points, first in family, part-time, aged 21 or over, hardship grant, mean week-6 rating (Satisfactory "
             "0, Some concern 1, At risk 2), living-learning community, hall, offer acceptance day, faculty, and "
             "that count in bands of 0, 1, 2, 3, 4 to 5, 6 to 8, 9 to 14, 15 to 21 and 22 or more.")
    L.append("5. Counted Semester 1 2026 teaching groups in s1_2026_class_timetable.xlsx: active classes meeting in "
             "the same room on the same day, start and teaching weeks are one group whatever teacher of record each "
             "lists, a group's size is its classes' census enrolments added, by owning faculty.")
    L.append("6. Counted students in year of study 2 or later with an enrolled attempt at the 2026 census once each: "
             "a student whose two attempts match a transfer in programme_transfers_2025_2026.csv is in the "
             "transfer's new programme, other two-attempt students are conjoint and go to the combination's "
             "first-listed programme in programme_catalogue_2026.csv.")
    L.append("7. Applied the model to the 2026 entrants and summed their probabilities: %s, about %s to the "
             "nearest 250." % ("{:,.1f}".format(o["call"]), "{:,}".format(o["call_r"])))
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % C.DELIV_XLSX)
    L.append("1. First-time entrants enrolled at the 1 October 2026 census not enrolled at the 1 October 2027 census: "
             "**%s** (nearest 250)" % "{:,}".format(o["call_r"]))
    L.append("2. Semester 1 2026 teaching groups and groups of more than 30 students at the census, by faculty:")
    for fc in C.FAC_CODES:
        L.append("   - %s: **%s** groups, **%s** of them over thirty students" % (FAC_SHORT[fc], "{:,}".format(g[fc][0]), g[fc][1]))
    L.append("3. Students in their second, third, and fourth or later year of study enrolled at the 1 October 2026 census, by faculty:")
    for fc in C.FAC_CODES:
        L.append("   - %s: second year **%s**, third year **%s**, fourth year or later **%s**"
                 % (FAC_SHORT[fc], "{:,}".format(cont.get((fc, 2), 0)), "{:,}".format(cont.get((fc, 3), 0)),
                    "{:,}".format(cont.get((fc, 4), 0))))
    L.append("")
    L.append("### %s\n" % C.DELIV_PNG)
    L.append("1. One stacked bar per faculty, groups of 30 students or fewer and groups of more than 30, each "
             "segment labelled with its count as in answer 2 above.")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


def write_metadata(path):
    meta = {"task": C.TASK,
            "distractor_files": ["target/" + f for f in C.DISTRACTORS],
            "deliverables": [C.DELIV_XLSX, C.DELIV_PNG],
            "objective": "Forecasting & Predictive Modeling",
            "domain": "Education & Learning Sciences / Learning Analytics & Early-Warning Models",
            "setting": "Corriemoor University and the Republic of Aldmark are fictional; every record is synthetic, "
                       "built by the task's generator, and no real institution, student system or person is "
                       "represented.",
            "sources": {f: {"source": "synthetic (task generator)", "date": "2026-10-16", "license": "CC0-1.0"}
                        for f in [C.F_SCLS, C.F_ACLS, C.F_CENSUS, C.F_XWALK, C.F_ADM, C.F_PROG, C.F_TT, C.F_CAT,
                                  C.F_TRF, C.F_CUT, C.F_CONV, C.F_DICT, C.F_HALL, C.F_NSL]}}
    json.dump(meta, open(path, "w"), indent=2)
    open(path, "a").write("\n")


def main(target, golden, figpath, subpath, metapath, quiet=False):
    os.makedirs(golden, exist_ok=True)
    o = compute(target)
    F = figures(o)
    json.dump(F, open(figpath, "w"), indent=2, sort_keys=True)
    open(figpath, "a").write("\n")
    write_workbook(os.path.join(golden, C.DELIV_XLSX), o)
    write_chart(os.path.join(golden, C.DELIV_PNG), o)
    write_submission(subpath, o, F)
    write_metadata(metapath)
    if not quiet:
        print("call %.1f -> %d; intake %d; no repeat %d; stale %d" % (o["call"], o["call_r"], o["n2026"],
                                                                     o["no_repeat_2026"], o["n_stale"]))
        print("groups", o["groups"])
        print("continuing", sorted(o["cont"].items()))
