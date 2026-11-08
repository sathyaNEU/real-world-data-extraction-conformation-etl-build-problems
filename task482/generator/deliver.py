"""task482 architecture 17: the golden deliverables, written from golden.compute() on the shipped seed.

    council_memo.docx     the recommendation to the Council
    achieved_marks.png    each draft's expected Achieved mark against 25
    paper_choice.xlsx     the working, with the August 2026 regional figures
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import openpyxl  # noqa: E402
from docx import Document  # noqa: E402
from docx.shared import Cm, Pt, RGBColor  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402

import params as P  # noqa: E402
import postprocess as PP  # noqa: E402

REG = P.REGIONS


def chart(res, path):
    gold = res["gold"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig, ax = plt.subplots(figsize=(6.2, 3.3), dpi=150)
    xs = ["Paper A", "Paper B", "Paper C"]
    vals = [gold[d] for d in "ABC"]
    cols = ["#9db7c9", "#9db7c9", "#2f6f8f"]
    ax.bar(xs, vals, color=cols, width=0.55)
    ax.axhline(P.TARGET, color="#333333", lw=1.1, ls="--")
    ax.text(2.42, P.TARGET + 0.25, "Specification: 25", fontsize=8, ha="right", color="#333333")
    for i, v in enumerate(vals):
        ax.text(i, v + 0.3, "%d" % round(v), ha="center", fontsize=9, fontweight="bold")
    ax.set_ylim(0, 30)
    ax.set_ylabel("Expected mark out of 50")
    ax.set_title("Expected mark at the Achieved standard, November 2027 candidates", fontsize=9.5, loc="left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, format="png", metadata={"Software": None})
    plt.close(fig)


def _par(doc, text, bold=False, size=10, after=6, italic=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    r.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(after)
    return p


def memo(res, path):
    g, b = res["gold"], res["bank"]
    doc = Document()
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Cm(2.2)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    _par(doc, "Memo", bold=True, size=14, after=2)
    for k, v in (("To", "The Council"), ("From", "Jeremy York, Psychometrician"), ("Date", "20 November 2026"),
                 ("Subject", "Setting the 2027 Year 10 science paper")):
        p = doc.add_paragraph()
        r = p.add_run("%s: " % k)
        r.bold = True
        p.add_run(v)
        p.paragraph_format.space_after = Pt(0)
    _par(doc, "", after=2)
    _par(doc, "Recommendation", bold=True, size=11, after=3)
    _par(doc, "Set Paper C. For a candidate at the Achieved standard sitting in November 2027, its expected mark is 25 "
              "of 50, against 26 for Paper A and 23 for Paper B (before rounding %.2f, %.2f and %.2f)."
         % (g["C"], g["A"], g["B"]))
    _par(doc, "Why this differs from the bank as it stands", bold=True, size=11, after=3)
    _par(doc, "Read straight off the bank, Paper A looks on target and Paper C looks hard (%.2f and %.2f). The "
              "difference is all in the Term 3 items. The bank calibrated them on the August 2026 sitting, and when I "
              "set each candidate's sitting day against their own school's sequence in the course review, %d per cent "
              "of the responses to Term 3 items came before the school had finished that unit. Those items read about "
              "a logit harder than they will be for a November candidate, who will have been taught both units."
         % (b["A"], b["C"], res["untaught_pct"]))
    _par(doc, "For 2027 I re-estimated each Term 3 item on the responses of candidates whose school had finished the "
              "unit before they sat (%d to %d responses per item), with abilities held on the Term 1 and 2 items and "
              "the scale on the anchor block. The Term 1 and 2 items keep their bank values. Paper C carries %d Term 3 "
              "items, Paper B %d and Paper A %d, so the re-estimate moves C most."
         % (res["taught_min"], res["taught_max"], res["t3_count"]["C"], res["t3_count"]["B"], res["t3_count"]["A"]))
    _par(doc, "The choice holds if a unit counts as finished from its last day or a few days later, under a joint "
              "recalibration without the untaught responses, and with one shared adjustment for all Term 3 items. All "
              "three drafts meet the strand limits.")
    _par(doc, "August 2026 sitting, for the annual report", bold=True, size=11, after=3)
    t = doc.add_table(rows=1, cols=5)
    t.style = "Light Grid Accent 1"
    for c, h in zip(t.rows[0].cells, ["Region", "Entered", "Sat (online or make-up)", "Sat a make-up paper",
                                      "Mean make-up mark"]):
        c.text = h
    for r in REG:
        row = t.add_row().cells
        vals = [r, "{:,}".format(res["entered"][r]), "{:,}".format(res["sat"][r]), str(res["makeup_n"][r]),
                "%.1f" % res["makeup_mean"][r]]
        for c, v in zip(row, vals):
            c.text = v
    _par(doc, "", after=2)
    _par(doc, "Entered counts each candidate once: candidates who moved school before the sitting appear under both "
              "schools in the register. Make-up papers are counted at the candidate's home school, including the "
              "candidates who sat at a host without a booking, whose scripts were keyed without a roster line. One keying "
              "batch holds values above the paper's 50 marks, every one of them even; the roster's header says each "
              "cover carries the mark out of 50 and as a percentage and that a keyer's session is keyed as one batch "
              "on one template, so that batch's values are taken as percentages and halved.", size=9)
    _par(doc, "The working is in paper_choice.xlsx.", size=9, italic=True)
    doc.save(path)
    PP.normalize_ooxml(path, "Jeremy York", "Jeremy York", "2026-11-19T21:30:00Z", "2026-11-20T02:12:00Z",
                       title="Setting the 2027 Year 10 science paper")


def workbook(res, path):
    w, pl = res["w"], res["w"]["pool"]
    items = pl["items"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Recommendation"
    bold = Font(bold=True)
    ws.append(["Draft", "Term 3 items", "Expected mark, bank as calibrated", "Expected mark, November 2027",
               "Distance from 25", "Expected mark (nearest whole mark)"])
    for d in "ABC":
        ws.append(["Paper " + d, res["t3_count"][d], round(res["bank"][d], 2), round(res["gold"][d], 2),
                   round(res["dist"][d], 2), int(round(res["gold"][d]))])
    ws.append([])
    ws.append(["Set Paper %s: nearest 25 at the Achieved standard (%.2f logits on the bank scale)."
               % (res["pick"], P.THETA_ACHIEVED)])
    for c in ws[1]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for col, wd in zip("ABCDEF", [10, 12, 20, 20, 14, 18]):
        ws.column_dimensions[col].width = wd
    ws2 = wb.create_sheet("Term 3 items")
    ws2.append(["Item code", "Card", "Unit", "Bank difficulty", "Taught responses", "Difficulty for November 2027",
                "On drafts"])
    for i in pl["t3"]:
        on = "".join(d for d in "ABC" if i in res["drafts"][d])
        if not on:
            continue
        ws2.append([items[i]["code"], items[i]["card"], items[i]["unit"], round(float(res["b_bank"][i]), 3),
                    res["taught_n"][items[i]["code"]], round(float(res["b_gold"][i]), 3), on])
    for c in ws2[1]:
        c.font = bold
    for col, wd in zip("ABCDEFG", [11, 8, 6, 14, 15, 24, 10]):
        ws2.column_dimensions[col].width = wd
    ws3 = wb.create_sheet("Draft items")
    ws3.append(["Draft", "Card", "Item code", "Unit", "Difficulty used"])
    for d in "ABC":
        for i in sorted(res["drafts"][d], key=lambda i: items[i]["card"]):
            ws3.append(["Paper " + d, items[i]["card"], items[i]["code"], items[i]["unit"],
                        round(float(res["b_gold"][i]), 3)])
    for c in ws3[1]:
        c.font = bold
    ws4 = wb.create_sheet("August 2026 by region")
    ws4.append(["Region", "Entered", "Sat (online or make-up)", "Sat a make-up paper", "Mean make-up mark"])
    for r in REG:
        ws4.append([r, res["entered"][r], res["sat"][r], res["makeup_n"][r], round(res["makeup_mean"][r], 1)])
    ws4.append(["All regions", sum(res["entered"].values()), sum(res["sat"].values()), sum(res["makeup_n"].values()), None])
    for c in ws4[1]:
        c.font = bold
    for row in ws4.iter_rows(min_row=2, min_col=5, max_col=5):
        for c in row:
            c.number_format = "0.0"
    for col, wd in zip("ABCDE", [12, 10, 22, 20, 18]):
        ws4.column_dimensions[col].width = wd
    for sh in (ws, ws2, ws3, ws4):
        sh.freeze_panes = "A2"
    ws["A1"].fill = PatternFill("solid", fgColor="DDE7EE")
    wb.save(path)
    PP.normalize_ooxml(path, "Jeremy York", "Jeremy York", "2026-11-17T22:05:00Z", "2026-11-20T01:48:00Z", excel=True)


def write_all(res, golden_dir):
    os.makedirs(golden_dir, exist_ok=True)
    memo(res, os.path.join(golden_dir, "council_memo.docx"))
    chart(res, os.path.join(golden_dir, "achieved_marks.png"))
    workbook(res, os.path.join(golden_dir, "paper_choice.xlsx"))
