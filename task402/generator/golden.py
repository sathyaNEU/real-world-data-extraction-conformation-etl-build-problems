"""task402 goldens: figures.json from the clean truth and the pack's ask truths, the improvement case (docx with a
chart of monthly recoveries) and the review evidence workbook (xlsx)."""
import io
import json
import os
from datetime import date

import numpy as np
import pandas as pd

import harness as H
import postprocess as PP
import world as W

ORG = "Fenwold Wellbeing Partnership"
A_UNIT = 50          # the prompt's rounding for A's cost
COST_UNIT = 100      # the prompt's rounding for the agency cost


def r50(v):
    return int(round(v / float(A_UNIT)) * A_UNIT)


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def figures(w, m, pk):
    f = {}
    rec = m[m.rec].copy()
    rec["mon"] = pd.to_datetime(rec.end).dt.to_period("M")
    months = {}
    for fy, (a, b) in (("2024-25", W.FY24), ("2025-26", W.FY25)):
        rr = rec[(rec.end >= a) & (rec.end <= b)]
        months[fy] = {str(p): int(n) for p, n in rr.groupby("mon").size().items()}
        f["recoveries_" + fy] = int(len(rr))
    f["monthly_recoveries"] = months
    s3 = m[(m.fy == 25) & (m.step == 3) & (m.n_treat_att >= 1)]
    br = s3[(s3.broken == True) & (s3.broken_kind == "agency")]
    ub = s3[~((s3.broken == True) & (s3.broken_kind == "agency"))]
    exp = 0.0
    for k, g in br.groupby("broken_at"):
        exp += len(g) * ub[ub.n_treat_att >= max(1, k)].rec.mean()
    f["call"] = "A"
    f["call_name"] = "Agency high-intensity therapists on 12-week assignments"
    f["broken_courses"] = int(len(br))
    f["broken_recovered"] = int(br.rec.sum())
    f["broken_expected"] = round(float(exp), 1)
    f["a_cost_exact"] = round(float(exp - br.rec.sum()), 1)
    f["a_cost"] = r50(exp - br.rec.sum())
    f["a_cost_edge"] = round(edge(exp - br.rec.sum(), 50), 1)
    f["a_cost_rounding"] = A_UNIT
    f["cost_rounding"] = COST_UNIT
    # the asks
    a3 = pk.truth["ask3"]
    f["ask_waiting"] = {k: int(v) for k, v in a3.items()}
    a1 = pk.truth["ask1"]
    f["ask_digital"] = {k: int(a1[k][1]) for k in ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"]}
    f["ask_digital_began"] = {k: int(a1[k][0]) for k in ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"]}
    a2 = pk.truth["ask2"]
    keep = ["2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10"]
    f["ask_hours_exact"] = {k: round(a2[k]["hours"], 4) for k in keep}
    f["ask_cost_exact"] = {k: round(a2[k]["cost"], 2) for k in keep}
    f["ask_hours"] = {k: int(round(a2[k]["hours"])) for k in keep}
    f["ask_cost"] = {k: int(round(a2[k]["cost"] / float(COST_UNIT)) * COST_UNIT) for k in keep}
    return f


MONTH_LABELS = ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]


def chart_png(f):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "svg.hashsalt": "task402"})
    fig, ax = plt.subplots(figsize=(11.4, 4.7), dpi=150)
    c24, c25 = "#c2772f", "#1d5c96"
    y24 = list(f["monthly_recoveries"]["2024-25"].values())
    y25 = list(f["monthly_recoveries"]["2025-26"].values())
    x = np.arange(12)
    ax.plot(x, y24, color=c24, lw=2, marker="o", ms=4, label="2024-25")
    ax.plot(x, y25, color=c25, lw=2, marker="o", ms=4, label="2025-26")
    ax.set_xticks(x)
    ax.set_xticklabels(MONTH_LABELS)
    ax.set_ylabel("Recoveries (discharges in month)")
    ax.set_ylim(0, max(y24 + y25) * 1.18)
    ax.grid(axis="y", color="#e3e3e0", lw=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#9a9a96")
    ax.tick_params(colors="#3d3d3a")
    ax.text(11.15, y24[-1], "2024-25", color="#3d3d3a", va="center", fontsize=8)
    ax.text(11.15, y25[-1], "2025-26", color="#3d3d3a", va="center", fontsize=8)
    ax.legend(loc="lower left", frameon=False, fontsize=8, ncol=2)
    ax.set_title("Recoveries by month of discharge, national measure", loc="left", fontsize=10, color="#222220")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def case_docx(path, f):
    from docx import Document
    from docx.shared import Pt, Cm, Inches
    d = Document()
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2.3)
        s.top_margin = Cm(1.8)
        s.bottom_margin = Cm(1.8)
    d.styles["Normal"].font.name = "Calibri"
    d.styles["Normal"].font.size = Pt(10.5)
    hdr = d.sections[0].header.paragraphs[0]
    hdr.text = "Fenwold Talking Therapies | 2026-27 improvement fund | review paper"
    hdr.runs[0].font.size = Pt(8)
    d.add_heading("Agency cover on lapsing 12-week blocks cost about %d recoveries in 2025-26" % f["a_cost"], level=1)
    meta = d.add_paragraph()
    run = meta.add_run("To: Jemma Fletcher, Mental Health Commissioning Manager, NHS Fenwold Integrated Care Board\n"
                       "From: Wendy Gibson, Head of Psychological Therapies, Fenwold Wellbeing Partnership\n"
                       "Date: 26 May 2026\nFor: contract review, 17 June 2026 (improvement plan 2026-27, section 3)")
    run.font.size = Pt(9)
    d.add_heading("Recommendation", level=2)
    d.add_paragraph(
        "Commit the 2026-27 improvement fund to change A and replace the agency cover with fixed-term high-intensity "
        "posts. The agency therapists brought in from May 2025 cost the service about %d recoveries in 2025-26, "
        "several times more than any other change on the list." % f["a_cost"])
    d.add_heading("What the cover cost", level=2)
    d.add_paragraph(
        "The cover took the step 3 backlog. When a therapist's block was not renewed, the therapist left on the block's "
        "end date and each patient still in treatment was passed to one of our own therapists after a gap, without a "
        "joint session. Most of those patients did not attend again. %s step 3 courses that ended in 2025-26 were "
        "broken off in this way, and %d of them ended in recovery. Set against the year's other step 3 referrals that "
        "had attended as many treatment appointments, they would have been expected to produce %.1f recoveries, so the "
        "cover's lapses cost %.1f, or %d to the nearest 50." % ("{:,}".format(f["broken_courses"]), f["broken_recovered"],
                                                             f["broken_expected"], f["a_cost_exact"], f["a_cost"]))
    d.add_paragraph(
        "The loss does not show in the clinician figures. The monthly report measures each staff group on the courses it "
        "discharged, and every broken-off course was discharged by one of our own therapists after the handover, so the "
        "agency therapists' own recovery rate looks sound. Nor is it the waiting list's: the long waiters' poorer "
        "outcomes sit on the same courses, because the cover held the backlog, so a reading by wait band counts the "
        "cover's loss a second time.")
    d.add_heading("Recoveries by month, both years", level=2)
    d.add_picture(io.BytesIO(chart_png(f)), width=Inches(6.2))
    cap = d.add_paragraph("Recoveries on the national measure (improvement plan annex), counted in the month of discharge. "
                          "2024-25: %s; 2025-26: %s. Source: refreshed extract of 6 May 2026."
                          % ("{:,}".format(f["recoveries_2024-25"]), "{:,}".format(f["recoveries_2025-26"])))
    cap.runs[0].font.size = Pt(8.5)
    d.add_heading("The other lines", level=2)
    d.add_paragraph(
        "The waiting list (C) cost the recoveries of the patients who gave up waiting; telephone-first step 2 (B), the "
        "digital platform (D) and the withdrawn groups (E) each moved recovery by far less than the cover did. The "
        "monthly evidence for those lines is in review_evidence_2025-26.xlsx.")
    fn = d.add_paragraph("Year as defined in section 3.1 of the plan: courses ended 1 April 2025 to 31 March 2026 by "
                         "discharge date. The provisional March report is superseded by the extract.")
    fn.runs[0].font.size = Pt(8)
    d.save(path)
    PP.normalize_ooxml(path, "Wendy Gibson", "Wendy Gibson", "2026-05-19T08:40:00Z", "2026-05-26T16:12:00Z", company=ORG)
    PP.scrub_docx(path, total_time=148, title="2026-27 improvement fund: review paper", company=ORG)



def case_pptx(path, f):
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.util import Inches, Pt
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    ink, muted, accent = RGBColor(0x22, 0x22, 0x20), RGBColor(0x5f, 0x5f, 0x5a), RGBColor(0x1d, 0x5c, 0x96)
    src = "Source: clinical system refreshed extract of 6 May 2026; agency booking register; national recovery measure."

    def text(slide, x, y, w, h, paras, size=16, bold=False, colour=ink):
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, ptxt in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = ptxt
            p.space_after = Pt(8)
            for r in p.runs:
                r.font.size, r.font.bold, r.font.color.rgb, r.font.name = Pt(size), bold, colour, "Calibri"
        return tb

    def frame(n, title):
        s_ = prs.slides.add_slide(prs.slide_layouts[6])
        text(s_, 0.6, 0.35, 12.1, 1.1, [title], size=26, bold=True)
        text(s_, 0.6, 6.85, 10.8, 0.4, [src], size=10, colour=muted)
        text(s_, 12.2, 6.85, 0.6, 0.4, [str(n)], size=10, colour=muted)
        return s_

    s1 = frame(1, "Agency cover on lapsing 12-week blocks cost about %d recoveries in 2025-26" % f["a_cost"])
    text(s1, 0.6, 1.7, 12.0, 1.2, ["Recommendation: commit the 2026-27 improvement fund to change A and replace the agency "
                                   "cover with fixed-term high-intensity posts."], size=20, colour=accent)
    text(s1, 0.6, 3.0, 12.0, 3.4, [
        "Fenwold Talking Therapies, review paper for the contract review of 17 June 2026 (improvement plan 2026-27, "
        "section 3).",
        "Prepared by Wendy Gibson, Head of Psychological Therapies, Fenwold Wellbeing Partnership, 26 May 2026."], size=14,
         colour=muted)
    s2 = frame(2, "%s step 3 courses were broken off when an agency block lapsed" % "{:,}".format(f["broken_courses"]))
    text(s2, 0.6, 1.6, 12.1, 5.0, [
        "When a therapist's block was not renewed, the therapist left on the block's end date and the patients still in "
        "treatment were passed to our own therapists after a gap, without a joint session. Most did not attend again.",
        "%d of those courses ended in recovery. Set against the year's other step 3 referrals that had attended as many "
        "treatment appointments, they would have produced %.1f, so the lapses cost %.1f recoveries: %d to the nearest 50."
        % (f["broken_recovered"], f["broken_expected"], f["a_cost_exact"], f["a_cost"]),
        "The clinician figures do not show it: every broken-off course was discharged by one of our own therapists after "
        "the handover. Nor is it the waiting list's loss: the long waiters' poorer outcomes sit on the same courses, "
        "because the cover held the backlog."], size=17)
    s3 = frame(3, "2025-26 against 2024-25: recoveries by month of discharge")
    s3.shapes.add_picture(io.BytesIO(chart_png(f)), Inches(0.9), Inches(1.45), width=Inches(11.4))
    text(s3, 0.9, 6.35, 11.4, 0.45, ["Recoveries on the improvement plan's annex measure. 2024-25: %s; 2025-26: %s."
                                    % ("{:,}".format(f["recoveries_2024-25"]), "{:,}".format(f["recoveries_2025-26"]))],
         size=12, colour=muted)
    s4 = frame(4, "The other lines moved recovery by far less")
    text(s4, 0.6, 1.6, 12.1, 4.8, [
        "C, the waiting list: the recoveries of the patients who gave up waiting.",
        "B, telephone-first step 2; D, the digital platform; E, the withdrawn groups: each moved recovery by far less than "
        "the cover did.",
        "The monthly evidence for those lines is in review_evidence_2025-26.xlsx."], size=18)
    prs.save(path)
    PP.normalize_ooxml(path, "Wendy Gibson", "Wendy Gibson", "2026-05-19T08:40:00Z", "2026-05-26T16:12:00Z", company=ORG)
    PP.scrub_pptx(path, total_time=131, company=ORG)

def evidence_xlsx(path, f):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment
    wb = Workbook()
    ws = wb.active
    ws.title = "Waiting list"
    ws.append(["Month end", "Step 3 patients waiting"])
    for k, v in f["ask_waiting"].items():
        ws.append([pd.Period(k, "M").end_time.date(), v])
    ws2 = wb.create_sheet("Digital programme")
    ws2.append(["Month began", "Patients who began", "Finished 4+ modules within 8 weeks"])
    for k in f["ask_digital"]:
        ws2.append([pd.Period(k, "M").strftime("%b %Y"), f["ask_digital_began"][k], f["ask_digital"][k]])
    ws3 = wb.create_sheet("Agency cover")
    ws3.append(["Month", "Hours worked", "Cost (GBP)"])
    for k in f["ask_hours"]:
        ws3.append([pd.Period(k, "M").strftime("%b %Y"), f["ask_hours"][k], f["ask_cost"][k]])
    ws4 = wb.create_sheet("Notes")
    for line in ["Step 3 patients waiting: on the step 3 waiting list at the end of the month, not yet seen for a first "
                 "treatment appointment. Source: waiting list month-end snapshots read against the appointments.",
                 "Digital programme: patients who began a programme on the Steadyway platform in the month; a module is "
                 "finished when all of its sections are completed.",
                 "Agency cover: the high-intensity therapists booked for the waiting list from May 2025 (the long-standing "
                 "locum excluded); hours by the days worked, cost at each booking line's charge rate.",
                 "Prepared 26 May 2026 from the refreshed extract of 6 May 2026."]:
        ws4.append([line])
    for sh, widths, fmts in ((ws, [12, 24], ["DD/MM/YYYY", "#,##0"]), (ws2, [12, 18, 32], ["@", "#,##0", "#,##0"]),
                             (ws3, [12, 14, 14], ["@", "#,##0", "#,##0"])):
        for i, wdt in enumerate(widths):
            sh.column_dimensions[chr(65 + i)].width = wdt
        for c in sh[1]:
            c.font = Font(bold=True)
        for row in sh.iter_rows(min_row=2):
            for i, c in enumerate(row):
                c.number_format = fmts[i]
        sh.freeze_panes = "A2"
    ws4.column_dimensions["A"].width = 110
    for row in ws4.iter_rows():
        for c in row:
            c.alignment = Alignment(wrap_text=True)
    wb.save(path)
    PP.normalize_ooxml(path, "Hollie Smith", "Wendy Gibson", "2026-05-20T09:02:00Z", "2026-05-26T15:58:00Z", excel=True,
                       company=ORG)


def deliverables(gdir, f):
    os.makedirs(gdir, exist_ok=True)
    case_pptx(os.path.join(gdir, "improvement_case_2026-27.pptx"), f)
    evidence_xlsx(os.path.join(gdir, "review_evidence_2025-26.xlsx"), f)
