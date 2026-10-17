"""The goldens, computed from the shipped pack only (bundle.py) with the concordance in methods.py: the grants
workbook with its chart and the conformed file of each counted student's latest grade 8 result and its level on the
new scale; generator/figures.json carries every figure the write-up states."""
import csv
import io
import json
import os

import numpy as np

import bundle as B
import methods as M
import world as W


def boundaries(old, new):
    """The highest retiring-test score each mainstream concordance places below each of the new test's grade 8 cuts;
    every convention must agree."""
    out = []
    for c in W.NEW_CUTS[8]:
        conv = M.conventions(old, new, c)
        ks = set(v[0] for k, v in conv.items() if k != "qcut_le")
        assert len(ks) == 1, (c, ks)
        out.append(ks.pop())
    return out


def level_new(score):
    return 1 + sum(score >= c for c in W.NEW_CUTS[8])


def level_old(score, ks):
    return 1 + sum(score > k for k in ks)


def compute(target):
    old, new, _, _ = B.bridge(target)
    ks = boundaries(old, new)
    pop = B.population(target, set(W.APPLICANTS))
    _, names = B.directory(target)
    lvl = {}
    for d, g, test, year, sc, sid, school in pop:
        lvl[sid] = level_new(sc) if test == "new" else level_old(sc, ks)
    counts = {d: [0, 0] for d in W.APPLICANTS}
    for d, g, test, year, sc, sid, school in pop:
        if lvl[sid] == 1:
            counts[d][g - 9] += 1
    top, nxt, tot = M.slate_of(counts)
    b, a = np.polyfit(old, new, 1)
    c = W.NEW_CUTS[8][0]
    reg_k = M.regression_boundary(old, new, c)[0]
    reg = {d: [0, 0] for d in W.APPLICANTS}
    for d, g, test, year, sc, sid, school in pop:
        if (test == "new" and sc < c) or (test == "old" and sc <= reg_k):
            reg[d][g - 9] += 1
    rtop, rnxt, rtot = M.slate_of(reg)
    g7 = B.grade7(target)
    F = {
        "call": {"funded": top, "funded_names": [names[d] for d in top], "first_out": nxt, "first_out_name": names[nxt],
                 "sixth": top[-1], "sixth_name": names[top[-1]], "gap": tot[top[-1]] - tot[nxt]},
        "level1": {d: tot[d] for d in W.APPLICANTS},
        "level1_grade9": {d: counts[d][0] for d in W.APPLICANTS},
        "level1_grade10": {d: counts[d][1] for d in W.APPLICANTS},
        "names": {d: names[d] for d in W.APPLICANTS},
        "boundaries": ks,
        "counted": len(pop),
        "counted_retiring": sum(1 for p in pop if p[2] == "old"),
        "grade7_level1": {d: g7[d][0] for d in W.APPLICANTS},
        "grade7_scored": {d: g7[d][1] for d in W.APPLICANTS},
        "grade7_share": {d: round(100.0 * g7[d][0] / g7[d][1], 1) for d in W.APPLICANTS},
        "bridge": {"n": len(old), "r": round(float(np.corrcoef(old, new)[0, 1]), 2), "slope": round(float(b), 2),
                   "share_new_l1": round(100 * float(np.mean(new < c)), 1),
                   "share_reg_l1": round(100 * float(np.mean(old <= reg_k)), 1),
                   "share_conc_l1": round(100 * float(np.mean(old <= ks[0])), 1)},
        "regression": {"boundary": reg_k, "funded": rtop, "first_out": rnxt, "level1": {d: rtot[d] for d in W.APPLICANTS}},
        "cuts": {"grade8": list(W.NEW_CUTS[8]), "grade7_level2": W.NEW_CUTS[7][0]},
    }
    return F, pop, lvl


def chart_png(F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ds = sorted(W.APPLICANTS, key=lambda d: (F["level1"][d], d))
    vals = [F["level1"][d] for d in ds]
    funded = set(F["call"]["funded"])
    short = {d: F["names"][d].replace(" Public Schools", "").replace(" City Schools", "").replace(" County Schools", "")
             .replace(" Unified School District", "").replace(" School District", "").replace(" Area Schools", "")
             .replace(" Consolidated Schools", "") for d in ds}
    fig, ax = plt.subplots(figsize=(8.4, 5.6), dpi=130)
    cols = ["#1f5f5b" if d in funded else "#b9c0c6" for d in ds]
    bars = ax.barh([short[d] for d in ds], vals, color=cols, height=0.66, zorder=2)
    for bar, d in zip(bars, ds):
        ax.text(bar.get_width() + 12, bar.get_y() + bar.get_height() / 2, "{:,}".format(F["level1"][d]), va="center",
                fontsize=8.5, color="#1b1d1f")
    k = len(ds) - 6
    sixth, first = F["call"]["sixth"], F["call"]["first_out"]
    ax.axhline(k - 0.5, color="#8a3b12", linewidth=1.1, linestyle=(0, (4, 3)), zorder=3)
    ax.text(max(vals) * 1.17, k - 0.42, "six grants: the sixth %s, the first left out %s" % (
        "{:,}".format(F["level1"][sixth]), "{:,}".format(F["level1"][first])), ha="right", va="bottom", fontsize=8.5,
            color="#8a3b12")
    ax.set_xlim(0, max(vals) * 1.2)
    ax.set_xlabel("Grade 9 and 10 students at Level 1 on the October 1, 2026 roll", fontsize=9, color="#3b3f44")
    ax.set_title("%s takes the sixth grant, %d students ahead of %s" % (
        W.short_name(sixth), F["call"]["gap"], W.short_name(first)), fontsize=11, loc="left", color="#1b1d1f")
    ax.grid(axis="x", color="#d9dde1", linewidth=0.8, zorder=0)
    ax.tick_params(axis="both", labelsize=8.5, colors="#3b3f44")
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: "{:,}".format(int(v))))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#1f5f5b", label="Funded"), Patch(color="#b9c0c6", label="Not funded")],
              loc="lower right", fontsize=8.5, frameon=False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_workbook(path, F):
    import openpyxl
    from openpyxl.drawing.image import Image
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Grants 2027"
    bold = Font(name="Calibri", size=10, bold=True)
    norm = Font(name="Calibri", size=10)
    head_fill = PatternFill("solid", fgColor="DDEBE7")
    ws["A1"] = "Adolescent Literacy Partnership: the six districts to fund for 2027"
    ws["A1"].font = Font(name="Calibri", size=13, bold=True)
    ws["A2"] = ("The six applicants with the most grade 9 and 10 students on the October 1, 2026 roll whose latest "
                "grade 8 state reading result is at Level 1 of the Statewide Literacy Measure.")
    ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="595959")
    head = ["Rank", "District code", "District", "Grade 9 at Level 1", "Grade 10 at Level 1", "Students at Level 1"]
    for j, h in enumerate(head, start=1):
        c = ws.cell(row=4, column=j, value=h)
        c.font, c.fill = bold, head_fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
    order = F["call"]["funded"]
    for i, d in enumerate(order, start=1):
        vals = [i, d, F["names"][d], F["level1_grade9"][d], F["level1_grade10"][d], F["level1"][d]]
        for j, v in enumerate(vals, start=1):
            c = ws.cell(row=4 + i, column=j, value=v)
            c.font = norm
            if j >= 4:
                c.number_format = "#,##0"
    r = 4 + len(order) + 2
    d = F["call"]["first_out"]
    ws.cell(row=r, column=1, value="First district left out").font = bold
    ws.cell(row=r, column=3, value=F["names"][d]).font = norm
    c = ws.cell(row=r, column=6, value=F["level1"][d])
    c.font, c.number_format = norm, "#,##0"
    ws.cell(row=r + 1, column=1, value="Gap to the sixth (%s)" % F["names"][F["call"]["sixth"]]).font = bold
    ws.cell(row=r + 1, column=6, value=F["call"]["gap"]).font = norm
    for j, w in enumerate([8, 12, 38, 12, 12, 13], start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    ws.freeze_panes = "A5"
    ws2 = wb.create_sheet("Applicants")
    ws2["A1"] = "Applicants: students at Level 1 and the grade 7 students of spring 2026"
    ws2["A1"].font = Font(name="Calibri", size=13, bold=True)
    ws2["A2"] = ("Grade 7: the district's own middle schools, spring 2026 Statewide Literacy Measure, Level 1 below the "
                 "grade 7 cut score of %d adopted by the State Board on August 13, 2026." % W.NEW_CUTS[7][0])
    ws2["A2"].font = Font(name="Calibri", size=9, italic=True, color="595959")
    head = ["District code", "District", "Grade 9 at Level 1", "Grade 10 at Level 1", "Students at Level 1", "Funded",
            "Grade 7 students with a score", "Grade 7 students at Level 1", "Grade 7 share at Level 1 (%)"]
    for j, h in enumerate(head, start=1):
        c = ws2.cell(row=4, column=j, value=h)
        c.font, c.fill = bold, head_fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ds = sorted(W.APPLICANTS, key=lambda d: (-F["level1"][d], d))
    for i, d in enumerate(ds, start=5):
        vals = [d, F["names"][d], F["level1_grade9"][d], F["level1_grade10"][d], F["level1"][d],
                "Yes" if d in F["call"]["funded"] else "No", F["grade7_scored"][d], F["grade7_level1"][d],
                F["grade7_share"][d]]
        for j, v in enumerate(vals, start=1):
            c = ws2.cell(row=i, column=j, value=v)
            c.font = norm
            if j in (3, 4, 5, 7, 8):
                c.number_format = "#,##0"
            if j == 9:
                c.number_format = "0.0"
    for j, w in enumerate([12, 38, 11, 11, 11, 8, 13, 12, 12], start=1):
        ws2.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    ws2.freeze_panes = "C5"
    ws2.print_title_rows = "4:4"
    ws3 = wb.create_sheet("Chart")
    png = chart_png(F)
    img = Image(io.BytesIO(png))
    ws3.add_image(img, "A1")
    ws4 = wb.create_sheet("Notes")
    k1 = F["boundaries"][0]
    notes = [
        ("Count day", "Students in grade 9 or 10 on an applicant's roll on October 1, 2026 (enrolment spells open on "
                      "that day); a student who moved districts in August or September counts where enrolled on the day."),
        ("Level 1", "A latest grade 8 state reading result below %d on the Statewide Literacy Measure. Grade 10 students "
                    "and grade 9 students retained after grade 8 in 2025 carry a spring 2025 Grade-Level Reading "
                    "Assessment result; through the spring 2026 bridge study (%s students in both tests) its scale "
                    "scores of %d and below place at Level 1." % (W.NEW_CUTS[8][0], "{:,}".format(F["bridge"]["n"]), k1)),
        ("Not counted", "Students with no grade 8 state reading result (new to the state's public schools, absent or "
                        "exempt, or a session invalidated with no make-up)."),
        ("Ashgrove-Fenley", "Consolidated July 1, 2026; its students tested under the codes of Ashgrove Public Schools "
                            "(1701) and Fenley School District (1702)."),
        ("Grade 7, spring 2026", "Students tested in the district's own middle schools (students of nonpublic schools "
                                 "tested under the district's code left out); Level 1 below %d, the grade 7 cut score "
                                 "adopted by the State Board on August 13, 2026; share of the students with a score."
                                 % W.NEW_CUTS[7][0]),
        ("Prepared", "Office of Literacy, November 23, 2026, for the State Board's meeting of December 10, 2026."),
    ]
    ws4["A1"] = "Notes"
    ws4["A1"].font = Font(name="Calibri", size=13, bold=True)
    for i, (a, b) in enumerate(notes, start=3):
        ws4.cell(row=i, column=1, value=a).font = bold
        c = ws4.cell(row=i, column=2, value=b)
        c.font = norm
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws4.column_dimensions["A"].width = 22
    ws4.column_dimensions["B"].width = 100
    wb.save(path)
    return png


CONFORMED_COLS = ["state_student_id", "district_code", "school_code", "grade", "test", "test_year", "scale_score",
                  "slm_level"]


def write_conformed(path, pop, lvl):
    rows = sorted(pop, key=lambda p: (p[0], p[6], p[1], p[5]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(CONFORMED_COLS)
        for d, g, test, year, sc, sid, school in rows:
            wr.writerow([sid, d, school, g, "GLRA" if test == "old" else "SLM", year, sc, lvl[sid]])
    return len(rows)


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    F, pop, lvl = compute(target)
    write_workbook(os.path.join(gdir, W.GOLDEN["workbook"]), F)
    F["conformed_rows"] = write_conformed(os.path.join(gdir, W.GOLDEN["table"]), pop, lvl)
    F["conformed_levels"] = {str(k): sum(1 for v in lvl.values() if v == k) for k in (1, 2, 3, 4)}
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(F, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return F
