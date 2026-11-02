"""The golden deliverables and figures.json, computed from target/ alone through analysis.py.

    nov2026_paper2_results.csv          one row per candidate who sat: the mark counted on each question answered
                                        (moved and held within 0 to 20), the total and the result
    paper2_results_committee_paper.docx the Examinations Committee paper: the call, the moves with their bar
                                        chart, the centres table and the May reviews
"""
import csv
import io
import json
import os
from decimal import ROUND_HALF_UP, Decimal

import numpy as np

import analysis as A
import params as PR
from pack import normalise_zip

STAMP_DOCX = "2026-11-30T23:40:00Z"


def rnd(x, nd=0):
    q = Decimal(1).scaleb(-nd)
    v = Decimal(repr(float(x))).quantize(q if nd else Decimal(1), rounding=ROUND_HALF_UP)
    return float(v) if nd else int(v)


def signed(v):
    return "+%d" % v if v > 0 else ("%d" % v if v < 0 else "0")


def compute(target):
    P, M, B, C, R = A.run(target)
    m = M["m"]
    g = M["golden"]
    raw = m + g[None, :]
    held_top = int(np.nansum(raw > PR.QUESTION_MAX))
    held_zero = int(np.nansum(raw < 0))
    q6, q8 = 5, 7

    def others(j):
        s = ~np.isnan(m[:, j])
        oth = m[s].copy()
        oth[:, j] = np.nan
        return rnd(float(np.nanmean(np.nanmean(oth, axis=1))), 1), rnd(float(np.nanmean(m[s, j])), 1)

    o6, mean6 = others(q6)
    o8, mean8 = others(q8)
    codes = [c[0] for c in PR.CENTRES]
    tot = {k: sum(C[c][k] for c in codes) for k in ("withdrawals", "absentees", "may_sitters")}
    declined = sum(1 for d in R["detail"] if d["declined"])
    typos = sum(1 for r, d in zip(P.reviews, R["detail"]) if r["candidate_no"].strip() != d["cand"])
    f = {
        "moves": {"Q%d" % (j + 1): int(g[j]) for j in range(8)},
        "answered": {"Q%d" % (j + 1): int(M["answered"][j]) for j in range(8)},
        "sat": M["n_sat"],
        "passed": M["n_pass"],
        "failed": M["n_sat"] - M["n_pass"],
        "held_at_20": held_top,
        "held_at_0": held_zero,
        "q6_mean": mean6, "q6_choosers_other_mean": o6,
        "q8_mean": mean8, "q8_choosers_other_mean": o8,
        "facility_moves": {"Q%d" % (j + 1): int(M["rungs"]["R1 facility"][j]) for j in range(8)},
        "facility_passed": M["passes"]["R1 facility"],
        "facility_extra_passes": M["passes"]["R1 facility"] - M["n_pass"],
        "unmoved_passed": M["passes"]["R0 no moves"],
        "centres": {PR.CENTRE_NAME[c]: C[c] for c in codes},
        "centre_totals": tot,
        "may_moves_minutes": [int(x) for x in B["minutes"]],
        "may_pass_minutes": list(B["minutes_pass"]),
        "reviews_changed": R["changed"],
        "reviews_declined": declined,
        "reviews_rekeyed": typos,
        "refund_aud": rnd(R["refund"]),
        "refund_aud_cents": R["refund"],
        "pass_mark": PR.PASS_MARK,
        "four_answer": int(((~np.isnan(m)).sum(1) == 4).sum()),
        "references": {"regulations": [2, 11.2, 12, 14.1, 14.2, 16, 17.1, 17.3, 19.2, 19.4], "paper": 2,
                       "questions_named": [6, 8], "mark_limits": [0, 20]},
    }
    return P, M, B, C, R, f


def results_csv(M, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["candidate_no"] + ["Q%d" % (j + 1) for j in range(8)] + ["total", "result"])
        for row in M["rows"]:
            wr.writerow(row)


def chart_png(f):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    qs = ["Q%d" % (j + 1) for j in range(8)]
    vals = [f["moves"][q] for q in qs]
    cols = ["#2a78d6" if v > 0 else ("#e34948" if v < 0 else "#b8b6ae") for v in vals]
    fig, ax = plt.subplots(figsize=(6.4, 3.0), dpi=150)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")
    xs = np.arange(8)
    ax.bar(xs, [v if v else 0.06 for v in vals], width=0.56, color=cols, zorder=3)
    ax.axhline(0, color="#52514e", lw=0.8, zorder=4)
    for x, v in zip(xs, vals):
        ax.text(x, v + (0.18 if v >= 0 else -0.18), signed(v), ha="center", va="bottom" if v >= 0 else "top",
                fontsize=9, color="#0b0b0b")
    ax.set_xticks(xs)
    ax.set_xticklabels(qs)
    ax.set_ylim(-3.9, 3.9)
    ax.set_yticks(range(-3, 4))
    ax.set_ylabel("Marks (added + / taken away -)", fontsize=8.5, color="#52514e")
    ax.grid(axis="y", color="#e4e2dc", lw=0.6, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="both", length=0, colors="#52514e")
    ax.set_title("Figure 1. Questions 6 and 8 move three marks; the others one mark or none", loc="left",
                 fontsize=9.5, color="#0b0b0b")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def committee_paper(P, M, f, path):
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt, RGBColor
    import datetime as dt
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin = s.bottom_margin = Cm(1.8)

    def para(text, bold=False, size=None, italic=False, space=4, color=None, align=None):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        p.paragraph_format.space_after = Pt(space)
        if align:
            p.alignment = align
        return p

    def table(rows, widths, bold_last=False):
        t = doc.add_table(rows=len(rows), cols=len(rows[0]))
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.LEFT
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                cell = t.cell(i, j)
                cell.text = ""
                run = cell.paragraphs[0].add_run(str(val))
                run.font.size = Pt(9.5)
                run.bold = (i == 0) or (bold_last and i == len(rows) - 1)
                if j > 0 and i > 0 and str(val).lstrip("+-").replace(",", "").isdigit():
                    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
                cell.width = Cm(widths[j])
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        return t

    para("%s  |  Examinations Committee  |  Meeting of 10 December 2026  |  Paper EC 26/14" % PR.ORG_SHORT,
         size=8.5, color="52514E", space=2)
    para("November 2026 Paper 2: %d of %d candidates pass, with Questions 6 and 8 moved three marks" %
         (f["passed"], f["sat"]), bold=True, size=15, space=2)
    para("For decision. Prepared by %s, Assessment Analyst, Examinations Office, 1 December 2026, from the marks of "
         "record exported on 30 November." % PR.PEOPLE["analyst"], size=9, color="52514E", space=8)

    para("1. Recommendation", bold=True, size=11.5, space=2)
    para("That the Committee approve the moves in Table 1 for the optional questions under regulation 14, and the "
         "Paper 2 results in nov2026_paper2_results.csv: %d of the %d candidates who sat the paper pass." %
         (f["passed"], f["sat"]))

    para("2. Moves under regulation 14", bold=True, size=11.5, space=2)
    para("Candidates answer five of the eight questions, and they did not choose at random. The stronger candidates "
         "took Question 6 (fire safety performance solutions) and the weaker took Question 8 (development consent "
         "conditions), so a question's mean mark says as much about who chose it as about how hard it was. "
         "Regulation 14.1 asks how hard each question proved for the candidates who sat the paper, so I read each "
         "question's difficulty from the same candidates' marks across the questions they chose: a fit of a "
         "candidate effect and a question effect over all %d scripts, centred on the average question, each "
         "question counted once." % f["sat"])
    para("The candidates who answered Question 6 averaged %.1f on their other questions and %.1f on Question 6; "
         "those who answered Question 8 averaged %.1f on their other questions and %.1f on Question 8. Set against "
         "the paper's mean marks alone, Question 6 would move by %s and Question 8 by %s, and %d candidates would "
         "pass, %d more than under the moves recommended here." %
         (f["q6_choosers_other_mean"], f["q6_mean"], f["q8_choosers_other_mean"], f["q8_mean"],
          signed(f["facility_moves"]["Q6"]), signed(f["facility_moves"]["Q8"]), f["facility_passed"],
          f["facility_extra_passes"]))
    rows = [["Question", "Topic", "Answered by", "Move (marks)"]]
    for j, (title, _mx) in enumerate(PR.NOV_QUESTIONS):
        q = "Q%d" % (j + 1)
        rows.append([q, title, f["answered"][q], signed(f["moves"][q])])
    para("Table 1. Moves for the optional questions", bold=True, size=9.5, space=2)
    table(rows, [1.8, 9.6, 2.3, 2.6])
    para("Source: e-marking export, marks of record at 30 November 2026. The %d candidates who answered four questions "
         "are in the fit and in the results." % f["four_answer"], size=8.5, italic=True, color="52514E", space=6)
    png = chart_png(f)
    doc.add_picture(io.BytesIO(png), width=Cm(15.5))
    zero = "none" if f["held_at_0"] == 0 else "%d" % f["held_at_0"]
    para("The moves were applied to every answer with regulation 14.2's limits: %d moved marks were held at 20 and "
         "%s at zero, and neither limit changes any result." % (f["held_at_20"], zero), space=8)

    para("3. Results", bold=True, size=11.5, space=2)
    para("Of the %d candidates who sat, %d pass and %d fail. Scripts on 48 or 49 after the moves go to a senior "
         "examiner under regulation 15 before results are issued." % (f["sat"], f["passed"], f["failed"]), space=8)

    para("4. Withdrawals, absences and May sitters by centre", bold=True, size=11.5, space=2)
    para("Withdrawals are dated by the time each request reached the portal (regulation 17.1), not by the day it "
         "was actioned. May sitters are the November sitters who sat Paper 2 in May, matched on membership number "
         "or on name and date of birth, as candidate numbers are issued afresh at each sitting.")
    rows = [["Centre", "Withdrawals", "Absentees", "Sat Paper 2 in May"]]
    for code in PR.CODES:
        nm = PR.CENTRE_NAME[code]
        c = f["centres"][nm]
        rows.append([nm, c["withdrawals"], c["absentees"], c["may_sitters"]])
    t = f["centre_totals"]
    rows.append(["All centres", t["withdrawals"], t["absentees"], t["may_sitters"]])
    para("Table 2. November 2026 Paper 2 by centre", bold=True, size=9.5, space=2)
    table(rows, [4.2, 3.2, 3.2, 4.2], bold_last=True)
    para("Source: candidate portal entries and request log at 30 November 2026; the legacy register and the marks of "
         "the May sitting. Western Sydney is the Parramatta centre, renamed on 1 August 2026.", size=8.5, italic=True,
         color="52514E", space=8)

    para("5. May 2026 reviews", bold=True, size=11.5, space=2)
    para("Of the May results, %d changed on review, each from fail to pass. The review fees to refund come to AUD %s: the "
         "fees for those %d reviews and for the %d requests received after the closing date, which were declined "
         "(regulation 19.4). Fees billed to member firm accounts are refunded at the firm's agreed rate." %
         (f["reviews_changed"], "{:,}".format(f["refund_aud"]), f["reviews_changed"], f["reviews_declined"]))

    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    fp = doc.sections[0].footer.paragraphs[0]
    run = fp.add_run("%s Examinations Committee  |  EC 26/14  |  page " % PR.ORG_SHORT)
    run.font.size = Pt(8)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r_ = OxmlElement("w:r")
    t_ = OxmlElement("w:t")
    t_.text = "1"
    r_.append(t_)
    fld.append(r_)
    fp._p.append(fld)
    cp = doc.core_properties
    cp.comments = ""
    cp.subject = "November 2026 sitting"
    cp.category = "Committee paper"
    cp.author = PR.PEOPLE["analyst"]
    cp.last_modified_by = PR.PEOPLE["analyst"]
    cp.title = "EC 26/14 November 2026 Paper 2 results"
    cp.created = dt.datetime(2026, 12, 1, 9, 40)
    cp.modified = dt.datetime(2026, 12, 1, 9, 40)
    cp.revision = 3
    doc.save(path)
    words = sum(len(p.text.split()) for p in doc.paragraphs) + sum(
        len(c.text.split()) for t in doc.tables for r in t.rows for c in r.cells)
    chars = sum(len(p.text.replace(" ", "")) for p in doc.paragraphs)
    normalise_zip(path, when=STAMP_DOCX, app="Microsoft Office Word",
                  stats={"Pages": 2, "Words": words, "Characters": chars, "Lines": 48, "Paragraphs": 24,
                         "CharactersWithSpaces": chars + words})


def write_all(target, golden_dir, gen_dir):
    os.makedirs(golden_dir, exist_ok=True)
    os.makedirs(gen_dir, exist_ok=True)
    P, M, B, C, R, f = compute(target)
    results_csv(M, os.path.join(golden_dir, PR.RESULTS_CSV))
    committee_paper(P, M, f, os.path.join(golden_dir, PR.PAPER_DOCX))
    with open(os.path.join(gen_dir, "figures.json"), "w") as fh:
        json.dump(f, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return f
