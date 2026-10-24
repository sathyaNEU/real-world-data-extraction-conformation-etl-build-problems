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
        for lev in calc.LEVELS:
            small, big = o["groups"][(fc, lev)]
            tag = "200" if lev == "200" else "300up"
            F["ask_groups_s1_2026_%s_%s_30orfewer" % (fc.lower(), tag)] = small
            F["ask_groups_s1_2026_%s_%s_over30" % (fc.lower(), tag)] = big
    F["_model_form"] = o["form"]
    F["_stated"] = {"rounding_of_the_call": 250, "paper_levels": [200, 300]}
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
    head = ["Faculty", "Level", "30 students or fewer", "More than 30", "Groups"]
    for j, h in enumerate(head, 1):
        c = ws2.cell(row=1, column=j, value=h)
        c.font = bold
        c.fill = fill
    i = 2
    for fc in C.FAC_CODES:
        for lev in calc.LEVELS:
            small, big = o["groups"][(fc, lev)]
            ws2.cell(row=i, column=1, value=FAC_SHORT[fc])
            ws2.cell(row=i, column=2, value="200" if lev == "200" else "300 and above")
            ws2.cell(row=i, column=3, value=small)
            ws2.cell(row=i, column=4, value=big)
            ws2.cell(row=i, column=5, value="=C%d+D%d" % (i, i))
            i += 1
    ws2.cell(row=i, column=1, value="Total").font = bold
    for col in "CDE":
        ws2["%s%d" % (col, i)] = "=SUM(%s2:%s%d)" % (col, col, i - 1)
        ws2["%s%d" % (col, i)].font = bold
    ws2.column_dimensions["A"].width = 28
    ws2.column_dimensions["B"].width = 15
    for col in "CDE":
        ws2.column_dimensions[col].width = 19
    ws4 = wb.create_sheet("Notes")
    notes = [
        "Definitions follow Continuing Enrolment Projection 2027: Conventions (Planning and Insight, 5 October 2026).",
        "Intake: first-time bachelor's entrants with an enrolled programme attempt at the 1 October census; entrants "
        "with credit are excluded. Approved leave counts as not enrolled.",
        "Earlier intakes: enrolment at the next census from the census history; the 2025 intake through the "
        "SIRIUS to ARC crosswalk.",
        "Projection: logistic model fitted on the 2019 to 2025 intakes (admissions attributes, week-6 progress check, "
        "faculty, and whether the entrant met 10 or more other entrants in two or more Semester 1 classes, the form "
        "with the lowest AIC), applied to the 2026 intake; reported to the nearest 250.",
        "Teaching groups, 200 level and above: each distinct set of active Semester 1 2026 classes meeting together "
        "in one room at one time is a group, so papers sharing only a lecture are the lecture and each workshop. A "
        "group's size is the students on its classes' lists who are enrolled at the 2026 census in the census history; "
        "places still held by students on approved leave or who left before the census are not counted.",
        "Sources: Registry census history and first-year cohort extracts; Admissions; Student Success week-6 "
        "progress check; Timetabling Semester 1 2026 timetable at the census; ARC class enrolments at the census.",
    ]
    ws4["A1"] = "Notes"
    ws4["A1"].font = bold
    for i, t in enumerate(notes, 3):
        ws4.cell(row=i, column=1, value=t).alignment = Alignment(wrap_text=True, vertical="top")
    ws4.column_dimensions["A"].width = 110
    ws2.freeze_panes = "A2"
    wb.save(path)
    import postprocess as PP
    PP.normalize_ooxml(path, "Cillian Coholan", "Cillian Coholan", "2026-10-15T22:05:00Z", "2026-10-16T03:31:00Z",
                       excel=True)


def write_chart(path, o):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    labels, small, big = [], [], []
    for fc in C.FAC_CODES:
        for lev in calc.LEVELS:
            labels.append("200 level" if lev == "200" else "300 and up")
            small.append(o["groups"][(fc, lev)][0])
            big.append(o["groups"][(fc, lev)][1])
    fig, ax = plt.subplots(figsize=(11.5, 5.8), dpi=110)
    x = np.arange(len(labels)) + np.repeat(np.arange(5) * 0.6, 2)
    ax.bar(x, small, 0.8, color="#9db9d8", label="30 students or fewer")
    ax.bar(x, big, 0.8, bottom=small, color="#2f5d8c", label="More than 30 students")
    for i in range(len(x)):
        ax.text(x[i], small[i] / 2, str(small[i]), ha="center", va="center", fontsize=8.5)
        ax.text(x[i], small[i] + big[i] / 2, str(big[i]), ha="center", va="center", fontsize=8.5, color="white")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    for j, fc in enumerate(C.FAC_CODES):
        ax.text((x[2 * j] + x[2 * j + 1]) / 2, -0.11, FAC_SHORT[fc].replace(" and ", " and\n"), transform=ax.get_xaxis_transform(),
                ha="center", va="top", fontsize=9)
    ax.set_ylabel("Teaching groups")
    ax.set_title("Semester 1 2026 teaching groups at 200 level and above: most run with more than 30 students",
                 fontsize=10, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    fig.text(0.01, 0.01, "Source: Timetabling, Semester 1 2026 timetable at the 1 October 2026 census. Groups as taught.",
             fontsize=7.5, color="#555555")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def write_submission(path, o, F):
    g = o["groups"]
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
    L.append("4. Fitted logistic models of not being enrolled at the next census on the 2019 to 2025 entrants (ASC "
             "points, first in family, part-time, aged 21 or over, hardship grant, mean week-6 rating with Satisfactory "
             "0, Some concern 1 and At risk 2, living-learning community, hall, offer acceptance day, faculty) with that "
             "count in several forms, and kept the lowest Akaike information criterion, per the conventions: a flag "
             "for meeting 10 or more other entrants twice.")
    L.append("5. Applied it to the 2026 entrants and summed their probabilities: %s, about %s to the nearest 250."
             % ("{:,.1f}".format(o["call"]), "{:,}".format(o["call_r"])))
    L.append("6. Counted Semester 1 2026 teaching groups at 200 level and above from s1_2026_class_timetable.xlsx: each "
             "distinct set of active classes meeting together in one room at one time (day, start and teaching weeks) "
             "is one group, so two papers sharing only their lecture make three (the lecture and each workshop); a "
             "group's size is the students its classes list in arc_s1_2026_class_enrolments.csv who hold an enrolled "
             "programme attempt at the 2026 census in the census history, so places still held by students on approved "
             "leave or with no 2026 attempt are not counted (ARC Scheduling's Enrolled at Census counts them, and shows "
             "a combination's two classes together on each).")
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % C.DELIV_XLSX)
    L.append("1. First-time entrants enrolled at the 1 October 2026 census not enrolled at the 1 October 2027 census: "
             "**%s** (nearest 250)" % "{:,}".format(o["call_r"]))
    L.append("2. Semester 1 2026 teaching groups by faculty and level, with 30 students or fewer and with more than "
             "thirty at the census:")
    for fc in C.FAC_CODES:
        for lev in calc.LEVELS:
            sm, bg = g[(fc, lev)]
            L.append("   - %s, %s: **%s** with thirty or fewer, **%s** with more than thirty"
                     % (FAC_SHORT[fc], "200 level" if lev == "200" else "300 level and above", sm, bg))
    L.append("")
    L.append("### %s\n" % C.DELIV_PNG)
    L.append("1. One stacked bar per faculty and level, groups of 30 students or fewer and of more than 30, each "
             "segment labelled with its count as in answer 2 above.")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


def write_metadata(path):
    meta = {"task": C.TASK,
            "distractor_files": ["target/" + f for f in C.DISTRACTORS + [C.F_TRF, C.F_CAT]],
            "deliverables": [C.DELIV_XLSX, C.DELIV_PNG],
            "objective": "Forecasting & Predictive Modeling",
            "domain": "Education & Learning Sciences / Learning Analytics & Early-Warning Models",
            "setting": "Corriemoor University and the Republic of Aldmark are fictional; every record is synthetic, "
                       "built by the task's generator, and no real institution, student system or person is "
                       "represented.",
            "sources": {f: {"source": "synthetic (task generator)", "date": "2026-10-16", "license": "CC0-1.0"}
                        for f in [C.F_SCLS, C.F_ACLS, C.F_CENSUS, C.F_XWALK, C.F_ADM, C.F_PROG, C.F_TT, C.F_CLE, C.F_CAT,
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
        print("call %.1f -> %d (%s); intake %d; no repeat %d" % (o["call"], o["call_r"], o["form"], o["n2026"],
                                                                o["no_repeat_2026"]))
        print("groups", o["groups"])
