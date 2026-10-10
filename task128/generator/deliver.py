"""The two golden deliverables: november_ticket_cut.csv and ticket_split_review.pptx."""
import csv

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

from params import ESTATES, LABEL, COLO
import ladder as G

CUT = "november_ticket_cut.csv"
DECK = "ticket_split_review.pptx"

NAVY = RGBColor(0x1F, 0x2A, 0x44)
BLUE = RGBColor(0x2E, 0x5A, 0x88)
GREY = RGBColor(0x6B, 0x72, 0x80)


def write_cut(path, W):
    rows = G.answer_tickets(W)
    out = []
    for i, r in enumerate(rows, 1):
        out.append([i, LABEL[r["estate"]], r["package"], r["hosts"], r["exposures"]])
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["rank", "estate", "package", "hosts_reached_november",
                     "exposures_taken_out_november"])
        wr.writerows(out)
    return rows


def open_exposure_today(W):
    """Open exploitable exposure per estate as of 23 October (before the round)."""
    out = {e: 0 for e in ESTATES}
    # colocated: every finding on the feed is exploitable
    for e in COLO:
        out[e] = sum(h.whole() for h in W["hosts"][e])
    # cloud: exploitable-now findings in the spine
    import ladder as golden
    sv = W["scorev"]
    for (e, p), v in sv.items():
        out[e] += v
    return out


def _txt(shape, text, size, bold=False, color=NAVY):
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Calibri"


def write_deck(path, W, rows):
    from params import ESTATES as EST
    split = W["answer_split"]
    figs = W["figs"]
    total = figs["_total"]
    ansA = W["ans_A"]
    ansB = W["ans_B"]
    open_exp = open_exposure_today(W)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # slide 1: the call
    s = prs.slides.add_slide(blank)
    box = s.shapes.add_textbox(Inches(0.6), Inches(0.5), Inches(12), Inches(1.0))
    _txt(box, f"November patch round: {total:,} exploitable host exposures taken out", 30, True)
    sub = s.shapes.add_textbox(Inches(0.6), Inches(1.5), Inches(12), Inches(0.6))
    _txt(sub, "The 300 tickets split across the six estates, signed for the 2 November cut.", 16,
         False, GREY)
    # split table
    r = len(EST) + 2
    tbl = s.shapes.add_table(r, 3, Inches(0.6), Inches(2.3), Inches(7.6), Inches(4.3)).table
    for j, h in enumerate(["Estate", "Tickets", "Exposures taken out (Nov)"]):
        c = tbl.cell(0, j); c.text = h
        c.text_frame.paragraphs[0].runs[0].font.size = Pt(13)
        c.text_frame.paragraphs[0].runs[0].font.bold = True
    for i, e in enumerate(EST, 1):
        tbl.cell(i, 0).text = LABEL[e]
        tbl.cell(i, 1).text = str(split[e])
        tbl.cell(i, 2).text = f"{figs[e]:,}"
        for j in range(3):
            tbl.cell(i, j).text_frame.paragraphs[0].runs[0].font.size = Pt(12)
    tbl.cell(r - 1, 0).text = "Total"
    tbl.cell(r - 1, 1).text = "300"
    tbl.cell(r - 1, 2).text = f"{total:,}"
    for j in range(3):
        run = tbl.cell(r - 1, j).text_frame.paragraphs[0].runs[0]
        run.font.bold = True; run.font.size = Pt(12)

    # chart: Nov take-out vs open exploitable today
    cd = CategoryChartData()
    cd.categories = [LABEL[e] for e in EST]
    cd.add_series("Taken out in November", [figs[e] for e in EST])
    cd.add_series("Open exploitable today", [open_exp[e] for e in EST])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(8.4), Inches(2.3),
                            Inches(4.4), Inches(4.3), cd)
    ch = gf.chart
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False

    # slide 2: boundary and the estate card
    s2 = prs.slides.add_slide(blank)
    b2 = s2.shapes.add_textbox(Inches(0.6), Inches(0.5), Inches(12), Inches(0.8))
    _txt(b2, "The line, and the estate card", 26, True)
    last_in = rows[299]
    first_below = W["first_below"]
    bl = s2.shapes.add_textbox(Inches(0.6), Inches(1.4), Inches(12), Inches(1.2))
    _txt(bl, f"Last ticket that made the cut: {LABEL[last_in['estate']]} / {last_in['package']}, "
             f"taking out {last_in['exposures']:,}. First ticket below the line: "
             f"{LABEL[first_below['estate']]} / {first_below['package']}, "
             f"{first_below['exposures']:,}.", 14, False, NAVY)
    # ask A/B card
    ar = len(EST) + 1
    t2 = s2.shapes.add_table(ar, 5, Inches(0.6), Inches(2.7), Inches(12), Inches(3.8)).table
    for j, h in enumerate(["Estate", "Patch pace median (days)", "Tickets missing target",
                           "Hosts in service", "Unscanned in 14 days"]):
        cell = t2.cell(0, j); cell.text = h
        cell.text_frame.paragraphs[0].runs[0].font.size = Pt(11)
        cell.text_frame.paragraphs[0].runs[0].font.bold = True
    for i, e in enumerate(EST, 1):
        t2.cell(i, 0).text = LABEL[e]
        t2.cell(i, 1).text = f"{ansA[e]['median_days']:.1f}"
        t2.cell(i, 2).text = str(ansA[e]['tickets_missed'])
        t2.cell(i, 3).text = str(ansB[e]['in_service']) if e in ansB else "-"
        t2.cell(i, 4).text = str(ansB[e]['unscanned_14d']) if e in ansB else "-"
        for j in range(5):
            t2.cell(i, j).text_frame.paragraphs[0].runs[0].font.size = Pt(10)
    import datetime as _dt
    cp = prs.core_properties
    cp.author = "Sendalia Viajes"
    cp.last_modified_by = "Sendalia Viajes"
    cp.comments = ""
    cp.title = "November patch round ticket split"
    cp.created = _dt.datetime(2026, 10, 23, 6, 0)
    cp.modified = _dt.datetime(2026, 10, 23, 6, 0)
    cp.revision = 1
    prs.save(path)
