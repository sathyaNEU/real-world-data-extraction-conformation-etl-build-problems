"""Write the golden deliverables into task181/golden/ from the shipped bundle alone: the huddle slide
(response_team_brief.pptx) and the quarterly table (pertussis_cases_by_lga.csv)."""
import csv
import os
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G         # noqa: E402
import postprocess as PP   # noqa: E402

TASK = os.path.dirname(HERE)
SLIDE = "response_team_brief.pptx"
TABLE = "pertussis_cases_by_lga.csv"
CSV_COLUMNS = ["lga", "period_from", "period_to", "confirmed_cases", "probable_cases", "infants_under_6_months",
               "infants_admitted_to_hospital", "infants_mother_vaccinated_14d_before_birth"]

INK = RGBColor(0x1D, 0x27, 0x33)
INK2 = RGBColor(0x4A, 0x55, 0x63)
RULE = RGBColor(0xC9, 0xCF, 0xD6)
CALL = RGBColor(0xB4, 0x3C, 0x1E)       # the call
CALL_BG = RGBColor(0xFB, 0xEE, 0xE8)
QUIET_BG = RGBColor(0xF2, 0xF4, 0xF6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def one_decimal(x):
    return ("%.1f" % x)


def fmt_pct(x):
    return "%d%%" % int(round(100 * x))


def _text(slide, x, y, w, h, paras, size=12, color=INK, bold=False, anchor=MSO_ANCHOR.TOP, fill=None):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.margin_top = tf.margin_bottom = Inches(0.04)
    if fill is not None:
        box.fill.solid()
        box.fill.fore_color.rgb = fill
    for i, p in enumerate(paras):
        runs = p if isinstance(p, list) else [(p, {})]
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.space_after = Pt(4)
        for text, st in runs:
            r = para.add_run()
            r.text = text
            r.font.size = Pt(st.get("size", size))
            r.font.bold = st.get("bold", bold)
            r.font.name = "Calibri"
            r.font.color.rgb = st.get("color", color)
    return box


def _table(slide, x, y, w, rows, widths, highlight=None, quiet=(), size=10.5, height=0.27, right=()):
    shape = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(height * len(rows)))
    tbl = shape.table
    for j, wd in enumerate(widths):
        tbl.columns[j].width = Inches(wd)
    for i, row in enumerate(rows):
        tbl.rows[i].height = Inches(height)
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            cell.text = str(val)
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            para = cell.text_frame.paragraphs[0]
            para.alignment = PP_ALIGN.RIGHT if j in right else PP_ALIGN.LEFT
            run = para.runs[0]
            run.font.size = Pt(size)
            run.font.name = "Calibri"
            run.font.bold = i == 0 or (highlight is not None and i == highlight)
            run.font.color.rgb = WHITE if i == 0 else (CALL if (highlight is not None and i == highlight) else INK)
            cell.fill.solid()
            if i == 0:
                cell.fill.fore_color.rgb = INK
            elif highlight is not None and i == highlight:
                cell.fill.fore_color.rgb = CALL_BG
            elif i in quiet:
                cell.fill.fore_color.rgb = QUIET_BG
            else:
                cell.fill.fore_color.rgb = WHITE
    return shape


def main_route(cases, area):
    sub = cases[(cases["area"] == area)]
    hosp = int((sub["lab"] == G.HOSP).sum())
    priv = int((sub["lab"] == G.PRIV).sum())
    return "Inland Pathology" if priv > hosp else "Hospital laboratory"


def write_slide(path, D, g):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    s = prs.slides.add_slide(prs.slide_layouts[6])
    N, E = g["N"], g["E"]
    call = g["answer"]
    share = g["route_share"]
    ph, pp = share[G.HOSP][0], share[G.PRIV][0]
    _text(s, 0.45, 0.28, 12.4, 0.62, [[("Send the response team to %s this week" % call, {"size": 28, "bold": True, "color": CALL})]])
    _text(s, 0.45, 0.92, 12.4, 0.4, [[("Monday huddle, 5 October 2026. PR-07 4.2: the area with the largest excess of cases with "
                                       "specimens collected 21 September to 4 October over its expected count (4.3).",
                                       {"size": 12.5, "color": INK2})]])
    # the fortnight by area
    order = sorted(G.AREAS, key=lambda a: (-N[a], a))
    rows = [["Area", "Cases notified so far", "Expected (PR-07 4.3)", "Most cases swabbed by"]]
    for a in order:
        rows.append([a, N[a], one_decimal(E[a]), main_route(D["cases"][D["cases"]["date"] >= G.HIST_LO[12]], a)])
    hl = 1 + order.index(call)
    _text(s, 0.45, 1.5, 7.4, 0.32, [[("Cases with specimens collected 21 Sep to 4 Oct, on the 07:00 extract", {"size": 12, "bold": True})]])
    _table(s, 0.45, 1.86, 7.4, rows, [2.3, 1.65, 1.65, 1.8], highlight=hl, right=(1, 2), size=10.5, height=0.285)
    reason = [
        [("Why %s and not Wagga Wagga. " % call, {"bold": True}),
         ("On the extract Wagga Wagga leads, %d cases against %s expected, with %s on %d against %s. Wagga Wagga's cases "
          "are swabbed by the hospital laboratory, which notifies almost every specimen within days of collection, so its "
          "fortnight is nearly all on file." % (
              N["Wagga Wagga"], one_decimal(E["Wagga Wagga"]), call, N[call], one_decimal(E[call])), {})],
        [("%s's general practices send their swabs to Inland Pathology, which notifies few specimens within the first "
          "week and only %s within 14 days of collection (right). The fortnight's specimens are 1 to 14 days old, so at "
          "Inland Pathology's speed most of %s's fortnight has not been notified yet: its cases with specimens in the "
          "fortnight are several times the %d on file, and its excess is the largest in the district. Snowy Valleys has "
          "the same %d against %s, through the hospital laboratory, and is nearly all on file." % (
              call, fmt_pct(pp), call, N[call], N["Snowy Valleys"], one_decimal(E["Snowy Valleys"])), {})],
    ]
    _text(s, 0.45, 5.08, 7.4, 1.9, reason, size=11.5, fill=QUIET_BG)
    # clusters
    cl = g["ask_b"]
    crow = [["School", "Area", "Cases"]] + [[name, area, n] for name, area, n in cl]
    _text(s, 8.25, 1.5, 4.65, 0.32, [[("School clusters this week (PR-07 5.1)", {"size": 12, "bold": True})]])
    _table(s, 8.25, 1.86, 4.65, crow, [2.75, 1.3, 0.6], right=(2,), size=10.5, height=0.36)
    _text(s, 8.25, 1.95 + 0.36 * len(crow), 4.65, 1.3,
          [[("Two or more student cases at one school with specimens collected 5 September to 4 October; school names "
             "matched to the enrolment rosters. Staff and parents are not counted; a student notified twice is one case.",
             {"size": 10, "color": INK2})]])
    y0 = 1.95 + 0.36 * len(crow) + 1.0
    _text(s, 8.25, y0, 4.65, 0.5, [[("Laboratory route speed", {"size": 12, "bold": True})],
                                   [("Specimens collected August 2025 to July 2026", {"size": 10, "color": INK2})]])
    _table(s, 8.25, y0 + 0.62, 4.65, [["Laboratory", "Notified within 14 days of collection"],
                                      ["Hospital laboratory", fmt_pct(ph)], ["Inland Pathology", fmt_pct(pp)]],
           [1.9, 2.75], right=(1,), size=10.5, height=0.32)
    _text(s, 0.45, 7.02, 12.0, 0.36,
          [[("Source: state notifiable conditions line-list extract, 07:00 Monday 5 October 2026; PR-07 v3.1. Cases dated by "
             "first specimen, one per person per episode (3.3), areas by residential postcode (3.4). Prepared by surveillance "
             "for the Monday huddle.", {"size": 9, "color": INK2})]])
    _text(s, 12.45, 7.02, 0.5, 0.36, [[("1", {"size": 9, "color": INK2})]])
    prs.save(path)
    PP.normalize_ooxml(path, "Tiffany Peters", "Tiffany Peters", "2026-10-04T20:21:00Z", "2026-10-04T20:46:00Z",
                       title="Response team brief, 5 October 2026")


def write_table(path, g):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(CSV_COLUMNS)
        for a in G.AREAS:
            r = g["ask_a"][a]
            w.writerow([a, G.ASK[0].isoformat(), G.ASK[1].isoformat(), r["confirmed"], r["probable"], r["infants"],
                        r["admitted"], r["vaccinated"]])


def main(target=None, out=None):
    target = target or os.path.join(TASK, "target")
    out = out or os.path.join(TASK, "golden")
    os.makedirs(out, exist_ok=True)
    D, g = G.solve(target, with_grid=False)
    write_slide(os.path.join(out, SLIDE), D, g)
    write_table(os.path.join(out, TABLE), g)
    return D, g


if __name__ == "__main__":
    main()
