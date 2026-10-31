"""task125 goldens: the command team deck and the ward figures CSV, both computed from target/ by analysis.py, and
figures.json with every figure the write-up states."""
import csv
import datetime as dt
import os

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

import analysis as A
import writeup as WR

DECK = "hot_spot_patrols_2027.pptx"
CSV = "patrol_figures_2026.csv"
NAVY = RGBColor(0x1F, 0x33, 0x55)
GREY = RGBColor(0x9A, 0xA4, 0xAE)
INK = RGBColor(0x22, 0x2B, 0x33)
SOFT = RGBColor(0x5B, 0x67, 0x72)


def r_half(x, nd=0):
    import decimal
    q = decimal.Decimal(1).scaleb(-nd)
    return float(decimal.Decimal(repr(x)).quantize(q, rounding=decimal.ROUND_HALF_UP))


def title_case(s):
    out = []
    for w in s.split():
        out.append(w if w in ("/",) else (w.capitalize() if not w.isdigit() else w))
    return " ".join(out).replace("Mcdonnel", "McDonnel").replace("Mckellar", "McKellar")


SUFFIX = {"St": "Street", "Rd": "Road", "Ave": "Avenue", "Dr": "Drive", "Line": "Line"}


def _street(name):
    words = title_case(name).split()
    if words and words[-1] in SUFFIX:
        words[-1] = SUFFIX[words[-1]]
    return " ".join(words)


def _bare(name):
    words = title_case(name).split()
    return " ".join(words[:-1]) if len(words) > 1 and words[-1] in SUFFIX else " ".join(words)


def label(seg):
    return "%s, %s to %s" % (_street(seg["street"]), _bare(seg["from_street"]), _bare(seg["to_street"]))


def figures(P):
    S = A.solve(P)
    segs = P.segs
    nights = S["nights"]
    top = S["top"]
    exp = S["exp"]
    yr = S["yearly"]
    order = S["order"]
    easy = A.designate(S["ids"], [yr[2026][s] for s in S["ids"]])[0]
    leaving = sorted(set(easy) - set(top), key=lambda s: -yr[2026][s])
    entering = sorted(set(top) - set(easy), key=lambda s: -exp[s])
    staying_g = [s for s in top if s in easy and s in _venue_set(S, "G")]
    base, eg, el = A.decompose(S["m"], nights)
    ids = S["ids"]
    pos = {s: k for k, s in enumerate(ids)}
    gnights = sorted(d for d in nights["G"] if 2022 <= d.year <= 2026)
    lnights = sorted(d for d in nights["L"] if 2022 <= d.year <= 2026)
    gi = A.indicators(nights, "G").astype(bool)
    li = A.indicators(nights, "L").astype(bool)
    m = S["m"]
    on_g = int(sum(m[pos[s], gi].sum() for s in leaving))
    tot_g = int(sum(m[pos[s]].sum() for s in leaving))
    on_l = int(sum(m[pos[s], li].sum() for s in entering))
    tot_l = int(sum(m[pos[s]].sum() for s in entering))
    ng27, nl27 = A.calendar_2027(nights)
    mar26 = sorted(d for d in nights["MG"] if d.year == 2026)
    mar27 = sorted(d for d in nights["ML"] if d.year == 2027)
    a, b = A.asks(P)
    fig = {
        "designated": sorted(top),
        "designated_ranked": [s for s in order[:20]],
        "leaving": leaving, "entering": entering, "staying_gardens": staying_g,
        "cut_20th": order[19], "cut_21st": order[20],
        "pool_size": len(S["pool"]),
        "expected_2027": {str(s): int(r_half(exp[s])) for s in S["pool"]},
        "recorded_2026": {str(s): yr[2026][s] for s in S["pool"]},
        "gardens_nights_2022_2026": len(gnights), "lakeshore_nights_2022_2026": len(lnights),
        "leaving_on_gardens_nights": on_g, "leaving_total": tot_g,
        "leaving_share_pct": r_half(100.0 * on_g / tot_g, 0),
        "gardens_nights_share_pct": r_half(100.0 * len(gnights) / A.NDAYS, 0),
        "entering_on_lakeshore_nights": on_l, "entering_total": tot_l,
        "entering_share_pct": r_half(100.0 * on_l / tot_l, 0),
        "lakeshore_nights_share_pct": r_half(100.0 * len(lnights) / A.NDAYS, 1),
        "nights_2027_gardens": int(ng27), "nights_2027_lakeshore": int(nl27), "days_2027": 365,
        "mariners_2026": len(mar26), "mariners_2027_booked": len(mar27),
        "mariners_last_gardens": mar26[-1].isoformat(), "mariners_first_lakeshore": mar27[0].isoformat(),
        "ask_officer_hours": {"%d Q%d" % k: v for k, v in sorted(a.items())},
        "ask_p1_median": {str(k): v for k, v in sorted(b.items())},
        "labels": {str(s): label(segs[s]) for s in S["pool"]},
        "wards": {str(s): int(segs[s]["ward"]) for s in S["pool"]},
    }
    return fig, S


def _venue_set(S, v):
    base, eg, el = A.decompose(S["m"], S["nights"])
    k = eg if v == "G" else el
    return {s for s, x in zip(S["ids"], k) if x > 0.3}


# ----------------------------------------------------------------------------------------------- the deck
def _text(slide, x, y, w, h, text, size=12, bold=False, color=INK, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    lines = text if isinstance(text, list) else [text]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = line
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        run.font.name = "Calibri"
    return tb


def _frame(prs, title, n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _text(s, 0.45, 0.28, 12.4, 0.6, title, size=22, bold=True, color=NAVY)
    line = s.shapes.add_connector(1, Inches(0.45), Inches(0.92), Inches(12.88), Inches(0.92))
    line.line.color.rgb = NAVY
    line.line.width = Pt(1.25)
    _text(s, 0.45, 7.05, 10.0, 0.3, "Mountjoy Police Service  |  Crime Analysis Unit  |  2027 hot spot designation",
          size=8.5, color=SOFT)
    _text(s, 12.2, 7.05, 0.7, 0.3, str(n), size=8.5, color=SOFT, align=PP_ALIGN.RIGHT)
    return s


def _table(slide, x, y, w, rows, widths, size=9.5):
    shape = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w),
                                   Inches(0.27 * len(rows)))
    t = shape.table
    for j, wd in enumerate(widths):
        t.columns[j].width = Inches(wd)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = t.cell(i, j)
            cell.text = str(val)
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.RIGHT if (j >= len(row) - 2 and i > 0) else PP_ALIGN.LEFT
                for run in p.runs:
                    run.font.size = Pt(size)
                    run.font.bold = i == 0
                    run.font.name = "Calibri"
                    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i == 0 else INK
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if i == 0 else (RGBColor(0xF2, 0xF4, 0xF7) if i % 2 else
                                                          RGBColor(0xFF, 0xFF, 0xFF))
            cell.margin_top = cell.margin_bottom = Emu(18000)
    return t


PLOT = (0.33, 0.02, 0.64, 0.86)


def _fix_plot(ch):
    """Pin the plot area and show every category label."""
    from lxml import etree
    from pptx.oxml.ns import qn
    pa = ch._chartSpace.chart.plotArea
    lay = pa.find(qn("c:layout"))
    if lay is None:
        lay = etree.Element(qn("c:layout"))
        pa.insert(0, lay)
    for child in list(lay):
        lay.remove(child)
    ml = etree.SubElement(lay, qn("c:manualLayout"))
    for tag, val in (("c:layoutTarget", "inner"), ("c:xMode", "edge"), ("c:yMode", "edge"), ("c:x", PLOT[0]),
                     ("c:y", PLOT[1]), ("c:w", PLOT[2]), ("c:h", PLOT[3])):
        e = etree.SubElement(ml, qn(tag))
        e.set("val", str(val))
    cat = pa.find(qn("c:catAx"))
    skip = etree.Element(qn("c:tickLblSkip"))
    skip.set("val", "1")
    anchor = cat.find(qn("c:noMultiLvlLbl"))
    if anchor is not None:
        anchor.addprevious(skip)
    else:
        cat.append(skip)


def deck(fig, path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    lab, ward, e27, r26 = fig["labels"], fig["wards"], fig["expected_2027"], fig["recorded_2026"]
    # 1 the designation
    s = _frame(prs, "2027 hot spot designation: the 20 segments", 1)
    _text(s, 0.45, 1.05, 12.4, 0.9, [
        "Designate the 20 segments below for 2027. Fifteen carry over from what the 2026 record alone would give; "
        "five segments around the Lakeshore Centre come in and five around the Memorial Gardens drop out, because "
        "the Mariners play their home games at the Lakeshore Centre from January."], size=12.5)
    ranked = fig["designated_ranked"]
    rows = [["#", "Segment", "Street and block", "Ward", "Exp. 2027", "2026"]]
    for i, sid in enumerate(ranked):
        rows.append([i + 1, sid, lab[str(sid)], ward[str(sid)], e27[str(sid)], r26[str(sid)]])
    half = 11
    _table(s, 0.45, 1.95, 6.1, rows[:half], [0.35, 0.85, 3.05, 0.55, 0.75, 0.55], size=9)
    _table(s, 6.75, 1.95, 6.1, [rows[0]] + rows[half:], [0.35, 0.85, 3.05, 0.55, 0.75, 0.55], size=9)
    _text(s, 0.45, 6.55, 12.4, 0.4, "Exp. 2027: founded patrol crimes expected in 2027. 2026: founded patrol crimes "
          "recorded in 2026. Both under the protocol's definitions.", size=9, color=SOFT)
    # 2 the chart
    s = _frame(prs, "Expected 2027 patrol crimes, every candidate segment", 2)
    pool = sorted(e27, key=lambda k: (-e27[k], int(k)))
    cd = CategoryChartData()
    cats = ["%s (%s)" % (lab[k], k) for k in pool]
    cd.categories = list(reversed(cats))
    des = set(str(x) for x in fig["designated"])
    cd.add_series("Designated", list(reversed([e27[k] if k in des else 0 for k in pool])))
    cd.add_series("Not designated", list(reversed([e27[k] if k not in des else 0 for k in pool])))
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED, Inches(0.45), Inches(1.0), Inches(9.2), Inches(6.0), cd)
    ch = gf.chart
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(9)
    ch.plots[0].gap_width = 35
    ch.series[0].format.fill.solid()
    ch.series[0].format.fill.fore_color.rgb = NAVY
    ch.series[1].format.fill.solid()
    ch.series[1].format.fill.fore_color.rgb = GREY
    ca = ch.category_axis
    ca.tick_labels.font.size = Pt(5.5)
    va = ch.value_axis
    va.tick_labels.font.size = Pt(8)
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RGBColor(0xDD, 0xE1, 0xE5)
    _fix_plot(ch)
    # the cut: a dashed rule between the 20th and 21st bars, the plot area pinned so the rule sits on it
    top, height = 1.0 + 6.0 * PLOT[1], 6.0 * PLOT[3]
    y = top + height * 20.0 / len(pool)
    x0, x1 = 0.45 + 9.2 * PLOT[0], 0.45 + 9.2 * (PLOT[0] + PLOT[2])
    cut = s.shapes.add_connector(1, Inches(x0), Inches(y), Inches(x1), Inches(y))
    cut.line.color.rgb = RGBColor(0xB0, 0x2A, 0x2A)
    cut.line.width = Pt(1.25)
    cut.line.dash_style = 4
    _text(s, x1 - 1.6, y - 0.27, 1.6, 0.25, "cut: 20 segments", size=8, color=RGBColor(0xB0, 0x2A, 0x2A),
          align=PP_ALIGN.RIGHT)
    c20, c21 = str(fig["cut_20th"]), str(fig["cut_21st"])
    _text(s, 9.85, 1.1, 3.0, 5.6, [
        "The cut falls between %s (%d expected) and %s (%d)." % (lab[c20], e27[c20], lab[c21], e27[c21]),
        "",
        "Candidates are the %d segments with 25 or more founded patrol crimes in at least one year from 2022 to "
        "2026 (protocol, section 3)." % fig["pool_size"],
        "",
        "Navy: designated. Grey: candidates below the cut."], size=10, color=INK)
    # 3 what moved
    s = _frame(prs, "What moves the designation: the Mariners go to the Lakeshore Centre", 3)
    _text(s, 0.45, 1.05, 12.4, 1.3, [
        "The Mariners played their last Memorial Gardens game on %s and the paid-duty register books %d home games "
        "at the Lakeshore Centre from %s. The segments around each venue record much of their street crime on its "
        "event nights: from 2022 to 2026 the five Gardens segments that drop out recorded %d of their %d founded "
        "patrol crimes on the Gardens' %d event nights, and the five Lakeshore segments that come in recorded %d of "
        "their %d on the Lakeshore Centre's %d."
        % (_d(fig["mariners_last_gardens"]), fig["mariners_2027_booked"], _d(fig["mariners_first_lakeshore"]),
           fig["leaving_on_gardens_nights"], fig["leaving_total"], fig["gardens_nights_2022_2026"],
           fig["entering_on_lakeshore_nights"], fig["entering_total"], fig["lakeshore_nights_2022_2026"])],
        size=12)
    rows = [["Drop out", "Ward", "2026", "Exp. 2027"]] + [[lab[str(x)], ward[str(x)], r26[str(x)], e27[str(x)]]
                                                       for x in fig["leaving"]]
    _table(s, 0.45, 2.6, 6.0, rows, [3.6, 0.7, 0.8, 0.9], size=10)
    rows = [["Come in", "Ward", "2026", "Exp. 2027"]] + [[lab[str(x)], ward[str(x)], r26[str(x)], e27[str(x)]]
                                                      for x in fig["entering"]]
    _table(s, 6.85, 2.6, 6.0, rows, [3.6, 0.7, 0.8, 0.9], size=10)
    _text(s, 0.45, 4.7, 12.4, 1.6, [
        "2027 is taken as 2026's calendar with the Mariners' home games at the Lakeshore Centre: %d event nights "
        "there and %d at the Gardens, against %d and %d in 2026."
        % (fig["nights_2027_lakeshore"], fig["nights_2027_gardens"], fig["lakeshore_nights_2026"],
           fig["gardens_nights_2026"]),
        "%s stays in: its steady crime alone keeps it above the cut." % ", ".join(lab[str(x)] for x in
                                                                              fig["staying_gardens"])],
        size=11)
    # 4 how the figures were built
    s = _frame(prs, "How the expected counts were built", 4)
    _text(s, 0.45, 1.1, 12.4, 5.6, [
        "Records: the RMS extract of 6 January 2027, each occurrence once on its latest version, legacy codes read "
        "through the 2023 crosswalk, unfounded occurrences out, dated by occurrence (report date where none).",
        "",
        "Venue nights: every event duty the paid-duty register holds at the Memorial Gardens and the Lakeshore "
        "Centre, 2022 to 2026, with the 2027 bookings.",
        "",
        "Expectation: for each segment, its founded patrol crimes a day on other nights and its excess on each "
        "venue's event nights, fitted on 2022 to 2026; 2027 = a year of the steady rate plus each excess times the "
        "venue's 2027 event nights.",
        "",
        "Cut: the 20 highest expected counts (protocol, section 2). The gap at the cut is wide enough that a shorter "
        "fitting window, a day-of-week adjustment or the five-year average calendar gives the same 20."],
        size=12)
    prs.core_properties.author = "Eric Gordon"
    prs.core_properties.last_modified_by = "Eric Gordon"
    prs.core_properties.title = "2027 hot spot designation"
    prs.core_properties.created = dt.datetime(2027, 1, 7, 9, 5, 0)
    prs.core_properties.modified = dt.datetime(2027, 1, 8, 16, 40, 0)
    prs.core_properties.revision = 6
    import zipnorm
    zipnorm.save(prs, path, "pptx", dt.datetime(2027, 1, 7, 9, 5, 0), dt.datetime(2027, 1, 8, 16, 40, 0))


def _d(iso):
    d = dt.date.fromisoformat(iso)
    return "%d %s" % (d.day, d.strftime("%B %Y"))


def write_csv(fig, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["figure", "ward", "period", "value", "unit"])
        for k, v in fig["ask_officer_hours"].items():
            ward, q = k.split()
            w.writerow(["officer_hours_on_calls", ward, "2026 %s" % q, v, "hours"])
        for k, v in fig["ask_p1_median"].items():
            w.writerow(["p1_median_minutes_to_first_arrival", k, "2026", "%.1f" % v, "minutes"])


def write_all(target, golden, base):
    os.makedirs(golden, exist_ok=True)
    P = A.Pack(target)
    fig, S = figures(P)
    fig["lakeshore_nights_2026"] = sum(1 for d in S["nights"]["L"] if d.year == 2026)
    fig["gardens_nights_2026"] = sum(1 for d in S["nights"]["G"] if d.year == 2026)
    deck(fig, os.path.join(golden, DECK))
    write_csv(fig, os.path.join(golden, CSV))
    WR.write(os.path.join(base, "submission.md"), fig)
    return fig
