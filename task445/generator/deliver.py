"""task445 architecture 3: the three golden deliverables and figures.json, from golden.solve on target/."""
import csv
import io
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from docx import Document  # noqa: E402
from docx.shared import Cm, Pt  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Font  # noqa: E402

import golden as G  # noqa: E402
import postprocess as PP  # noqa: E402

RNAME = {"NT": "Northern Territory", "QT": "Queensland and Torres Strait", "WA": "Western Australia",
         "PC": "Pacific", "ID": "Indonesia and Timor-Leste", "MS": "Malaysia and Singapore"}
MNAME = {"2025-12": "December 2025", "2026-01": "January 2026", "2026-02": "February 2026"}


def chart(S, path):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "svg.hashsalt": "t445"})
    fig, ax = plt.subplots(figsize=(6.4, 3.3), dpi=150)
    qs = G.QS
    vals = [S["demand"][q] for q in qs]
    cols = ["#9aa7b8" if v < G.LINE else "#b5523b" for v in vals]
    ax.barh(["Question %s" % q for q in qs], vals, color=cols, height=0.55)
    ax.axvline(G.LINE, color="#333333", lw=1, ls="--")
    ax.axvline(0, color="#777777", lw=0.6)
    ax.text(G.LINE + 0.05, 2.38, "code 4.3 line, 1.5 marks", fontsize=8, color="#333333")
    for i, v in enumerate(vals):
        ax.text(v + (0.06 if v >= 0 else -0.06), i, "%+.1f" % v, va="center", ha="left" if v >= 0 else "right",
                fontsize=8)
    ax.set_xlim(-2.2, 3.2)
    ax.set_xlabel("Marks harder than the other two optional questions (candidates who wrote all three essays)")
    ax.invert_yaxis()
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, format="png", metadata={"Software": None})
    plt.close(fig)


def paper(S, path, png):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading("History Paper 2, 2026: optional questions (code of practice, section 4)", level=1)
    p = d.add_paragraph()
    p.add_run("Research and Standards, for the executive, 3 December 2026").italic = True
    r6 = S["raise_by"]["6"]
    dem = S["demand"]
    d.add_paragraph(
        "Recommendation: raise every candidate's mark on Question 6 by %d marks before the best two essays are "
        "credited and the Awarding Committee's boundaries are applied. Question 6 was %.1f marks more demanding than "
        "Questions 4 and 5 taken together, over the code's line of 1.5; Questions 4 and 5 were not more demanding "
        "than the others (%.1f and %.1f) and are not changed." % (r6, dem["6"], dem["4"], dem["5"]))
    d.add_paragraph(
        "Section 4.2 asks what the paper's candidates would have earned on each question against the others. "
        "Candidates chose their two essays, and chose by the topics they knew: Question 6 "
        "was answered by about a third of the candidates, and those who took it knew its topic. Their marks on it, "
        "whether compared with the other questions' marks, adjusted for Section A, or set beside their own other "
        "essay, carry that knowledge and put Question 6 about half a mark harder. The %s candidates who wrote all "
        "three essays chose nothing: every essay they wrote was marked, and the difference between each of their "
        "own three marks shows each question's demand with no choice in it. Their three essays were written in the "
        "time for two, which lowers all three marks alike and leaves the differences unchanged, and the candidates "
        "with low, middle and high Section A marks each put Question 6 over the line." % format(S["n_all_three"], ","))
    d.add_picture(png, width=Cm(15.5))
    d.add_paragraph("Grades after scaling (paper total, Section A and the two credited essays):")
    t = d.add_table(rows=2, cols=7)
    t.style = "Light Grid Accent 1"
    for j, g in enumerate(["A", "B", "C", "D", "E", "U"]):
        t.cell(0, j).text = g
        t.cell(1, j).text = format(S["grades"][g], ",")
    t.cell(0, 6).text = "Graded"
    t.cell(1, 6).text = format(len(S["results"]), ",")
    d.add_paragraph("Scaling Question 6 changes %s candidates' grades; no grade falls. The boundaries are those of "
                    "the committee's minute of 24 November and are not moved (code 5.2)." % format(S["changed"], ","))
    sec = d.sections[0]
    sec.left_margin = sec.right_margin = Cm(2.2)
    d.core_properties.author = "Mary Deleon"
    d.save(path)
    PP.normalize_ooxml(path, "Mary Deleon", "Mary Deleon", "2026-12-02T23:05:00Z", "2026-12-03T06:41:00Z",
                       title="History Paper 2 optional questions 2026")


def results_csv(S, path):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["candidate_no", "centre_code", "region", "section_a", "q4", "q5", "q6", "credited", "section_b",
                "paper_total", "grade"])
    for r in S["results"]:
        m = r["marks"]
        w.writerow([r["cand"], r["centre"], r["region"], r["section_a"]] + [m.get(q, "") for q in G.QS] +
                   ["Q" + "+Q".join(sorted(r["credited"])), r["section_b"], r["total"], r["grade"]])
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())


def entries_xlsx(S, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "By region"
    ws.append(["Region", "Sat Paper 2", "Answered Q4", "Answered Q5", "Answered Q6"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in G.REGIONS:
        e = S["entries"][r]
        ws.append([RNAME[r], e["sat"], e["q4"], e["q5"], e["q6"]])
    for col, wd in zip("ABCDE", (30, 13, 13, 13, 13)):
        ws.column_dimensions[col].width = wd
    wb.save(path)
    PP.normalize_ooxml(path, "Pamela Sullivan", "Mary Deleon", "2026-12-02T22:40:00Z", "2026-12-03T06:12:00Z", excel=True)


def write_all(target, golden, here):
    os.makedirs(golden, exist_ok=True)
    S = G.solve(target)
    png = os.path.join(golden, "optional_questions_chart.png")
    chart(S, png)
    paper(S, os.path.join(golden, "p2_question_scaling_2026.docx"), png)
    os.remove(png)
    results_csv(S, os.path.join(golden, "history_p2_results_2026.csv"))
    entries_xlsx(S, os.path.join(golden, "history_p2_entries_2026.xlsx"))
    fig = G.figures(S)
    json.dump(fig, open(os.path.join(here, "figures.json"), "w"), indent=1, sort_keys=True)
    return S, fig
