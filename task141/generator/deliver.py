"""The golden deliverables: presumptive_release_tier_2027.docx (the memo to the senior resident judge: the tier's top
score and each score's case), presumptive_release_tier_2027.xlsx (the safety floor by score and the three tables:
bed-days in custody and monitoring days by new-criminal-activity score, missed court dates by failure-to-appear score)
and missed_court_dates_by_fta_score.png, plus generator/figures.json. Every figure is computed from the shipped pack
(calc.py)."""
from __future__ import annotations

import json
import os

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import calc as CA
import common as K
import postprocess as PP

GOLDEN = "R3 leniency gradient (golden)"
DEFAULT = "R0 released defendants' rate"
MEMO_DATE = "14 October 2026"


def f0(x):
    return "{:,}".format(int(x))


def p1(x):
    """A rate in per cent to one decimal, half away from zero."""
    return "%.1f" % K.round1(100.0 * x)


def compute(target):
    fa, h = CA.everything(target)
    lad = CA.ladder(fa, h)
    g, d = lad[GOLDEN], lad[DEFAULT]
    n = h.groupby("nca").size().to_dict()
    rel = h.groupby("nca").released24.mean().to_dict()
    mags = h.mag.nunique()
    a = CA.ask_a(target, fa)
    b = CA.ask_b(target, fa)
    c = CA.ask_c(target, fa)
    return dict(fa=fa, h=h, lad=lad, g=g, d=d, n=n, rel=rel, mags=mags, tier=CA.tier(g), tier_default=CA.tier(d),
                a=a, b=b, c=c)


def figures(c):
    g, d = c["g"], c["d"]
    lad = c["lad"]
    out = {
        "call": {"tier_top_score": c["tier"], "tier_scores": "1 to %d" % c["tier"], "floor_pct": "85",
                 "first_failing_score": c["tier"] + 1},
        "components": {
            "score4_full_release_pct": p1(g[4]),
            "score4_full_release_shared_bound_pct": "80",
            "score3_full_release_pct": p1(g[3]),
            "score3_full_release_shared_bound_pct": "90",
            "score4_released_pct": p1(d[4]),
            "score4_held_pct": p1(1 - c["rel"][4]),
        },
        "steps": {
            "history_first_appearances": f0(sum(c["n"].values())),
            "history_by_score": {s: f0(c["n"][s]) for s in range(1, 7)},
            "magistrates": f0(c["mags"]),
            "released_share_pct": {s: p1(c["rel"][s]) for s in range(1, 7)},
            "released_safety_pct": {s: p1(d[s]) for s in range(1, 7)},
            "full_release_safety_pct": {s: p1(g[s]) for s in range(1, 7)},
            "window_days": "365", "ask_b_days": "90", "full_release_share_pct": "100",
            "history_start": "1 October 2021", "history_end": "30 September 2025",
            "draft_sections": ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6"],
        },
        "default_path": {"tier_scores": "1 to %d" % c["tier_default"], "score4_pct": p1(d[4]), "score5_pct": p1(d[5])},
        "rungs": {k: {"tier": CA.tier(v), "score3_pct": p1(v[3]), "score4_pct": p1(v[4])} for k, v in lad.items()},
        "ask_a": {s: f0(K.round_to(c["a"].get(s, 0), 10)) for s in range(1, 7)},
        "ask_b": {s: {"missed": f0(c["b"][s][0]), "releases": f0(c["b"][s][1]),
                      "share_pct": p1(c["b"][s][0] / c["b"][s][1])} for s in range(1, 7)},
        "ask_c": {s: f0(K.round_to(c["c"].get(s, 0), 10)) for s in range(1, 7)},
    }
    return out


def _title(ws, title, sub):
    ws["A1"] = title
    ws["A1"].font = Font(name="Calibri", bold=True, size=13, color="1F4E79")
    ws["A2"] = sub
    ws["A2"].font = Font(name="Calibri", italic=True, size=9.5, color="595959")


def _head(ws, row, values, widths=None):
    for k, v in enumerate(values, 1):
        cell = ws.cell(row=row, column=k, value=v)
        cell.font = Font(name="Calibri", bold=True)
        cell.fill = PatternFill("solid", fgColor="DCE6F0")
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    if widths:
        for k, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(k)].width = w


def _row(ws, row, values, fmts=None, bold=False):
    for k, v in enumerate(values, 1):
        cell = ws.cell(row=row, column=k, value=v)
        cell.font = Font(name="Calibri", bold=bold)
        if fmts and fmts[k - 1]:
            cell.number_format = fmts[k - 1]


def _note(ws, row, text, ncol):
    ws.cell(row=row, column=1, value=text)
    ws.cell(row=row, column=1).font = Font(name="Calibri", italic=True, size=9, color="595959")
    ws.cell(row=row, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncol)
    ws.row_dimensions[row].height = 30


def write_book(path, c, figs):
    g, d = c["g"], c["d"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Safety floor"
    _title(ws, "Presumptive release tier for 2027: the safety floor by new-criminal-activity score",
           "Eligible first appearances (draft 2.1) from 1 October 2021 to 30 September 2025, every pretrial period "
           "closed by 30 September 2026. Safety rate: share with no new-offense arrest (draft 2.4).")
    _head(ws, 4, ["NCA score", "Eligible first appearances", "Released at first appearance (%)",
                  "Released defendants: no new-offense arrest (%)", "Every eligible defendant released (%)",
                  "Meets the 85% floor"], [11, 14, 15, 18, 18, 12])
    r = 5
    for s in range(1, 7):
        _row(ws, r, [s, c["n"][s], float(p1(c["rel"][s])), float(p1(d[s])), float(p1(g[s])),
                     "yes" if g[s] >= K.FLOOR else "no"], [None, "#,##0", "0.0", "0.0", "0.0", None],
             bold=(s == c["tier"]))
        r += 1
    r += 1
    ws.freeze_panes = "A5"
    _note(ws, r, "Tier's top score (draft 2.5): %d. The last column is each score's rate for all its eligible "
          "defendants, read from the %d magistrates' first appearances: new-offense arrests per eligible appearance "
          "against the magistrate's release share at the score, a line weighted by caseload, read at full release."
          % (c["tier"], c["mags"]), 6)
    # Ask A
    ws = wb.create_sheet("Bed-days in custody")
    _title(ws, "Bed-days in custody of eligible defendants held after a first appearance, 1 October 2025 to "
           "30 September 2026", "Each stay from booking to release, boarding at Halsey County included; one bed-day "
           "for each midnight count held, to the count of 30 September 2026.")
    _head(ws, 4, ["NCA score", "Bed-days (nearest 10)"], [11, 16])
    for s in range(1, 7):
        _row(ws, 4 + s, [s, K.round_to(c["a"].get(s, 0), 10)], [None, "#,##0"])
    _row(ws, 11, ["All scores", K.round_to(sum(c["a"].values()), 10)], [None, "#,##0"], bold=True)
    _note(ws, 13, "Bed-days to the nearest 10; the total is summed before rounding. Defendants with no screen have no "
          "score and are not included.", 4)
    ws.freeze_panes = "A5"
    # Ask C
    ws = wb.create_sheet("Monitoring days")
    _title(ws, "Days on electronic monitoring to 30 September 2026, defendants released at a first appearance from "
           "1 October 2025 to 30 September 2026", "Sentry Point enrollments matched to the release; each calendar day "
           "a unit was on the defendant counted once.")
    _head(ws, 4, ["NCA score", "Days (nearest 10)"], [11, 16])
    for s in range(1, 7):
        _row(ws, 4 + s, [s, K.round_to(c["c"].get(s, 0), 10)], [None, "#,##0"])
    _row(ws, 11, ["All scores", K.round_to(sum(c["c"].values()), 10)], [None, "#,##0"], bold=True)
    _note(ws, 13, "Days to the nearest 10; the total is summed before rounding. Enrollments still open on 30 September "
          "2026 are counted to that day.", 4)
    ws.freeze_panes = "A5"
    # Ask B
    ws = wb.create_sheet("Missed court dates")
    _title(ws, "Releases at a first appearance, 1 October 2025 to 30 June 2026, followed within 90 days by a missed "
           "court date", "A called-and-failed court date (order for arrest issued) in a case carrying the "
           "appearance's charges, superior court cases opened by indictment included, from the release day to the "
           "90th day after it.")
    _head(ws, 4, ["FTA score", "Releases", "Followed by a missed court date", "Share (%)"], [11, 12, 16, 11])
    for s in range(1, 7):
        m, n = c["b"][s]
        _row(ws, 4 + s, [s, n, m, float(p1(m / n))], [None, "#,##0", "#,##0", "0.0"])
    tm, tn = sum(v[0] for v in c["b"].values()), sum(v[1] for v in c["b"].values())
    _row(ws, 11, ["All scores", tn, tm, float(p1(tm / tn))], [None, "#,##0", "#,##0", "0.0"], bold=True)
    ws.freeze_panes = "A5"
    # notes
    ws = wb.create_sheet("Notes")
    _title(ws, "Notes", "Dorrance County Pretrial Services, research. Prepared %s for the 2027 revision of the local "
           "bail policy." % MEMO_DATE)
    notes = [
        ("Sources", "Clerk of Superior Court first-appearance exports (legacy system to 3 March 2024, case management "
                    "system from 4 March 2024), the charges file, the case index and the court events; Pretrial "
                    "Assessment Scale screens; the Sheriff's Office jail export; the state arrest extract of "
                    "2 October 2026; Sentry Point invoice lines; Halsey County housing invoices; the magistrate roster."),
        ("Safety floor", "Draft revision of 6 October 2026, sections 2.1 to 2.5. A first appearance counts once per "
                         "booking; released at first appearance means released from the detention center within 24 "
                         "hours of the appearance."),
        ("Rounding", "Rates and shares in percent to one decimal, days to the nearest 10; each figure rounded once from "
                     "unrounded working."),
    ]
    _head(ws, 4, ["Item", "Note"], [16, 110])
    for k, (a, b) in enumerate(notes):
        _row(ws, 5 + k, [a, b])
        ws.cell(row=5 + k, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[5 + k].height = 44 if len(b) > 200 else 30
    for w in wb.worksheets:
        w.page_setup.orientation = "landscape"
        w.page_setup.paperSize = w.PAPERSIZE_LETTER
        w.sheet_properties.pageSetUpPr.fitToPage = True
        w.page_setup.fitToWidth = 1
        w.page_setup.fitToHeight = 0
    wb.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["analyst"], K.PEOPLE["analyst"], "2026-10-12T13:41:20Z", "2026-10-14T19:06:44Z",
                       excel=True, company="Dorrance County Pretrial Services")


def write_chart(path, c):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams["svg.hashsalt"] = "task141"
    scores = list(range(1, 7))
    shares = [100.0 * c["b"][s][0] / c["b"][s][1] for s in scores]
    fig, ax = plt.subplots(figsize=(9.0, 5.2), dpi=120)
    bars = ax.bar([str(s) for s in scores], shares, color="#1F4E79", width=0.62)
    for b_, s in zip(bars, scores):
        m, n = c["b"][s]
        ax.text(b_.get_x() + b_.get_width() / 2, b_.get_height() + 0.5, "%s%%\n%s of %s" % (p1(m / n), f0(m), f0(n)),
                ha="center", va="bottom", fontsize=9, color="#1D2330")
    ax.set_ylim(0, max(shares) * 1.25)
    ax.set_xlabel("Failure-to-appear score (Pretrial Assessment Scale)")
    ax.set_ylabel("Releases followed by a missed court date (%)")
    lo, hi = c["b"][1], c["b"][6]
    ax.set_title("Missed court dates rise with the failure-to-appear score: %s%% of releases at score 1, %s%% at score 6\n"
                 "Releases at first appearance, 1 October 2025 to 30 June 2026, with a missed court date within 90 days"
                 % (p1(lo[0] / lo[1]), p1(hi[0] / hi[1])), fontsize=11)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.text(0.01, 0.01, "Court events and case index to 30 September 2026; superior court cases opened by indictment "
             "included. Dorrance County Pretrial Services.", fontsize=7.5, color="#5A6270")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def _page_field(par):
    """A PAGE field in a footer paragraph, as Word writes one."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    for kind, text in (("begin", None), (None, " PAGE "), ("separate", None), (None, "1"), ("end", None)):
        r = par.add_run()
        if kind:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), kind)
            r._r.append(fc)
        elif text.strip() == "PAGE":
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = text
            r._r.append(it)
        else:
            r.text = text


def write_memo(path, c, figs):
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, RGBColor
    g, d = c["g"], c["d"]
    t = c["tier"]
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    sec = doc.sections[0]
    fp = sec.footer.paragraphs[0]
    fp.text = "Pretrial Services, research: presumptive release tier for 2027. Page "
    _page_field(fp)
    for r in fp.runs:
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    p = doc.add_paragraph()
    r = p.add_run("DORRANCE COUNTY PRETRIAL SERVICES")
    r.bold = True
    r.font.size = Pt(10)
    p = doc.add_paragraph()
    r = p.add_run("Memorandum")
    r.font.size = Pt(15)
    r.bold = True
    for a_, b_ in (("To:", "Zachary Henson, Senior Resident Superior Court Judge"),
                   ("Copy:", "Kristen Thompson, Chief District Court Judge; Jeffrey Francis, Chief Magistrate"),
                   ("From:", "Teresa Diaz, Director (prepared by Lauren Mullins, Research Analyst)"),
                   ("Date:", MEMO_DATE),
                   ("Re:", "Local bail policy revision for 2027, section 2.6: the top score for the presumptive "
                           "release tier")):
        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(0)
        q.add_run(a_ + " ").bold = True
        q.add_run(b_)
    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run("The tier should stop at new-criminal-activity score %d" % t)
    r.bold = True
    r.font.size = Pt(13)
    doc.add_paragraph(
        "We propose %d as the tier's top score. Scores 1 to %d each meet the 85 percent safety floor of section 2.3 "
        "for all the eligible defendants the tier would release at the score. Score %d does not: with every eligible "
        "score-%d defendant released, %s percent would complete the pretrial period without a new-offense arrest."
        % (t, t, t + 1, t + 1, p1(g[t + 1])))
    doc.add_paragraph(
        "Score %d looks safe on the record we have. Of the eligible score-%d defendants magistrates released at first "
        "appearance from October 2021 to September 2025, %s percent had no new-offense arrest in the pretrial period. "
        "But magistrates held %s percent of eligible score-%d defendants, and they hold the ones whose affidavits and "
        "appearance concern them. A held defendant's pretrial outcome is never recorded, so the released defendants' "
        "rate leaves out exactly the defendants the tier would add, and the tier releases every one of them."
        % (t + 1, t + 1, p1(d[t + 1]), p1(1 - c["rel"][t + 1]), t + 1))
    doc.add_paragraph(
        "The duty rota sends every magistrate the same mix of arrests, so the %d magistrates who heard these "
        "appearances differ in what they release, not in whom they see. At score %d, a magistrate who releases more "
        "of the same defendants sees more new-offense arrests per eligible appearance, by more than the released "
        "defendants' own rate would add: the defendants the lenient magistrates release and the others hold are "
        "riskier than those everyone releases. Carried out to release of every eligible defendant, score %d's rate is "
        "%s percent. The same reading puts score %d at %s percent, clear of the floor." % (
            c["mags"], t + 1, t + 1, p1(g[t + 1]), t, p1(g[t])))
    doc.add_paragraph("Eligible first appearances, October 2021 to September 2025, by score").runs[0].bold = True
    tb = doc.add_table(rows=1, cols=5)
    tb.style = "Table Grid"
    hdr = ["NCA score", "Eligible first appearances (1)", "Released at first appearance",
           "No new-offense arrest: defendants released", "No new-offense arrest: every eligible defendant released"]
    for k, x in enumerate(hdr):
        tb.rows[0].cells[k].text = x
    for s_ in range(1, 7):
        row = tb.add_row().cells
        row[0].text = str(s_)
        row[1].text = f0(c["n"][s_])
        row[2].text = p1(c["rel"][s_]) + "%"
        row[3].text = p1(d[s_]) + "%"
        row[4].text = p1(g[s_]) + "%" + ("" if g[s_] >= K.FLOOR else "  below floor")
    for rr in tb.rows:
        for cell in rr.cells:
            for para in cell.paragraphs:
                for run in para.runs:
                    run.font.size = Pt(9.5)
    q = doc.add_paragraph()
    r = q.add_run("Source: clerk's first-appearance exports (legacy system and case management system), Pretrial "
                  "Assessment Scale screens, the jail export and the state arrest extract of 2 October 2026; "
                  "pretrial period and new-offense arrest as in section 2.4.")
    r.italic = True
    r.font.size = Pt(8.5)
    doc.add_paragraph().add_run("How the full-release rate is read").bold = True
    doc.add_paragraph(
        "Every first appearance from 1 October 2021 to 30 September 2025, so each 365-day pretrial period had closed "
        "by the extracts' end on 30 September 2026. For each score and each magistrate: the share of eligible "
        "defendants released at first appearance, and the new-offense arrests per eligible appearance (arrests among "
        "the released, over all eligible appearances, held or not). Across the %d magistrates the two lie on a line, "
        "fitted with each magistrate weighted by caseload; its value at a release share of 100 percent is the "
        "score's new-offense rate under the tier." % c["mags"])
    doc.add_paragraph().add_run("Jail, monitoring and court dates").bold = True
    doc.add_paragraph(
        "presumptive_release_tier_2027.xlsx gives, by new-criminal-activity score, the bed-days in custody of "
        "eligible defendants held after a first appearance from 1 October 2025 and the monitoring days of defendants "
        "released at a first appearance in that year, and by failure-to-appear score the releases from 1 October "
        "2025 to 30 June 2026 followed within 90 days by a missed court date (charted in "
        "missed_court_dates_by_fta_score.png).")
    q = doc.add_paragraph()
    r = q.add_run("(1) Eligible under section 2.1 at that appearance: every charge a misdemeanor (Class A1, 1, 2 or 3), "
                  "none listed in Appendix B, and no hold from another jurisdiction. Appearances with no screen have no "
                  "score and are outside the tier and the table.")
    r.font.size = Pt(8.5)
    doc.core_properties.author = K.PEOPLE["analyst"]
    doc.core_properties.title = "Presumptive release tier 2027"
    doc.save(path)
    PP.normalize_docx(path, K.PEOPLE["analyst"], K.PEOPLE["director"], "2026-10-13T14:02:00Z", "2026-10-14T20:17:00Z",
                      revision=6, total_time=167, seed="task141/memo", title="Presumptive release tier 2027",
                      company="Dorrance County Pretrial Services")


def main(target, golden, figures_path):
    os.makedirs(golden, exist_ok=True)
    c = compute(target)
    figs = figures(c)
    write_memo(os.path.join(golden, K.GOLD_MEMO), c, figs)
    write_book(os.path.join(golden, K.GOLD_BOOK), c, figs)
    write_chart(os.path.join(golden, K.GOLD_CHART), c)
    with open(figures_path, "w") as fh:
        json.dump(figs, fh, indent=2, sort_keys=False)
        fh.write("\n")
    return c, figs
