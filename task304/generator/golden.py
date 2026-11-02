"""task304 architecture 4: the golden deliverables, written from figures.json (computed by analysis.py from target/).

induct_enclosure_2027.pptx: the Schedule 2.6 return to the regulator (the hub, every hub's pool and count brought below,
a native bar chart marking the hub chosen). hearing_program_2026.csv: the two asks."""
import csv
import io
import os
import zipfile

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

INK = RGBColor(0x1F, 0x2A, 0x33)
GREY = RGBColor(0x8A, 0x96, 0x9E)
MUTED = RGBColor(0xB9, 0xC2, 0xC8)
ACCENT = RGBColor(0x1C, 0x6E, 0x8C)


def _text(slide, x, y, w, h, text, size=14, bold=False, color=INK, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    lines = text if isinstance(text, list) else [text]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
        r.font.name = "Calibri"
    return tb


def deck(path, F):
    hubs = F["hubs"]
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    best = F["call_hub"]

    s = prs.slides.add_slide(blank)
    _text(s, 0.7, 0.55, 12, 0.5, "Noise undertaking EU-N-2026, Schedule 2.6 return", 13, color=GREY)
    _text(s, 0.7, 1.05, 12, 1.0, "2027 induct-line enclosure: %s" % best, 34, bold=True)
    _text(s, 0.7, 2.25, 11.6, 1.6,
          ["The enclosure at %s brings %d workers from at or above 85 dB(A) to below it, more than at any other hub."
           % (best, F["below"][best]),
           "%s is next at %d." % (F["runner_up"], F["below"][F["runner_up"]])], 20)
    _text(s, 0.7, 6.55, 12, 0.5, "Hearing conservation program, National WHS  |  M. Hayes  |  27 November 2026", 11, color=GREY)

    s = prs.slides.add_slide(blank)
    _text(s, 0.7, 0.45, 12, 0.6, "Workers at or above the standard, and brought below it, by hub", 24, bold=True)
    _text(s, 0.7, 1.05, 12, 0.5, "Reference weeks 12 October to 8 November 2026; employees and labour-hire operatives", 13, color=GREY)
    rows, cols = len(hubs) + 1, 3
    tbl = s.shapes.add_table(rows, cols, Inches(0.7), Inches(1.7), Inches(9.2), Inches(0.45 * rows)).table
    tbl.columns[0].width = Inches(3.4)
    tbl.columns[1].width = Inches(2.9)
    tbl.columns[2].width = Inches(2.9)
    head = ["Hub", "At or above 85 dB(A)", "Brought below by the enclosure"]
    for j, h in enumerate(head):
        c = tbl.cell(0, j)
        c.text = h
        para = c.text_frame.paragraphs[0]
        para.runs[0].font.size = Pt(13)
        para.runs[0].font.bold = True
        if j:
            para.alignment = PP_ALIGN.RIGHT
    for i, h in enumerate(hubs, start=1):
        vals = [h, "%d" % F["pool"][h], "%d" % F["below"][h]]
        for j, v in enumerate(vals):
            c = tbl.cell(i, j)
            c.text = v
            para = c.text_frame.paragraphs[0]
            para.runs[0].font.size = Pt(13)
            para.runs[0].font.bold = (h == best)
            if j:
                para.alignment = PP_ALIGN.RIGHT
    _text(s, 0.7, 5.3, 11.8, 1.2,
          ["Exposure is each worker's LAeq,8h over the shifts they worked (Schedule 2.3): induct hours from the sorter "
           "control system's operator sessions, joined to people through the badge register; zone levels from survey "
           "KA-2611-R1; after-state at the induct levels in design report QAE-0927 rev 2."], 12, color=GREY)

    s = prs.slides.add_slide(blank)
    _text(s, 0.7, 0.45, 12, 0.6, "Workers the enclosure would bring below 85 dB(A)", 24, bold=True)
    cd = CategoryChartData()
    cd.categories = hubs
    cd.add_series("Brought below", [F["below"][h] for h in hubs])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.7), Inches(1.25), Inches(11.8), Inches(5.6), cd)
    ch = gf.chart
    ch.has_legend = False
    plot = ch.plots[0]
    plot.gap_width = 70
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format = "0"
    dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(13)
    ser = plot.series[0]
    for i, h in enumerate(hubs):
        pt = ser.points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = ACCENT if h == best else MUTED
    va = ch.value_axis
    va.has_title = True
    va.axis_title.text_frame.text = "Workers brought below 85 dB(A)"
    va.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(12)
    va.has_major_gridlines = False
    va.tick_labels.font.size = Pt(11)
    ch.category_axis.tick_labels.font.size = Pt(12)
    _text(s, 9.2, 1.2, 3.4, 0.5, "Chosen: %s" % best, 13, bold=True, color=ACCENT)

    prs.core_properties.author = "Melissa Hayes"
    prs.core_properties.last_modified_by = "Melissa Hayes"
    prs.core_properties.title = "Induct enclosure 2027"
    import datetime as dt
    prs.core_properties.created = dt.datetime(2026, 11, 27, 10, 12, 0)
    prs.core_properties.modified = dt.datetime(2026, 11, 27, 15, 40, 0)
    prs.core_properties.revision = 3
    prs.save(path)
    _normalise_zip(path)


def _normalise_zip(path):
    buf = io.BytesIO()
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in sorted(zin.infolist(), key=lambda i: i.filename):
            data = zin.read(item.filename)
            if item.filename == "docProps/app.xml":
                data = data.replace(b"python-pptx", b"Microsoft Office PowerPoint")
            zi = zipfile.ZipInfo(item.filename, date_time=(2026, 11, 27, 15, 40, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            zout.writestr(zi, data)
    open(path, "wb").write(buf.getvalue())


def ask_csv(path, F):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["hub", "earplug_pairs_jul_2026", "earplug_pairs_aug_2026", "earplug_pairs_sep_2026",
                    "workers_confirmed_threshold_shift_2026"])
        for h in F["hubs"]:
            w.writerow([h, F["pairs"][h]["7"], F["pairs"][h]["8"], F["pairs"][h]["9"], F["sts"][h]])


def write(golden_dir, F):
    os.makedirs(golden_dir, exist_ok=True)
    deck(os.path.join(golden_dir, "induct_enclosure_2027.pptx"), F)
    ask_csv(os.path.join(golden_dir, "hearing_program_2026.csv"), F)
