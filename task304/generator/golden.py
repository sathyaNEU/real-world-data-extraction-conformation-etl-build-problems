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
MUTED = RGBColor(0x7C, 0x8C, 0x97)
ACCENT = RGBColor(0x0A, 0x6A, 0xA8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PAPER = RGBColor(0xF3, 0xF5, 0xF6)
TINT = RGBColor(0xDC, 0xE9, 0xF3)
PLOT = (0.08, 0.06, 0.90, 0.82)      # inner plot area as fractions of the chart frame (x, y, w, h)
AXIS_MAX = 140


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


def _strip(slide, n, source):
    _text(slide, 0.7, 7.0, 10.5, 0.35, source, 9.5, color=GREY)
    _text(slide, 12.0, 7.0, 0.7, 0.35, str(n), 9.5, color=GREY, align=PP_ALIGN.RIGHT)


def deck(path, F):
    hubs = F["hubs"]
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    best = F["call_hub"]
    ru = F["runner_up"]
    big = max(hubs, key=lambda h: F["pool"][h])
    assert big != best and F["levels"][big]["Lp"] >= 85, "slide titles state the largest pool's induct stays above 85"

    s = prs.slides.add_slide(blank)
    _text(s, 0.7, 0.55, 12, 0.5, "Noise undertaking EU-N-2026, Schedule 2 return for the regulator, due 31 January 2027", 13, color=GREY)
    _text(s, 0.7, 1.05, 12, 1.0, "%s gets the 2027 induct-line enclosure" % best, 34, bold=True)
    _text(s, 0.7, 2.25, 11.6, 2.4,
          ["The enclosure at %s brings %d workers from at or above 85 dB(A) to below it, more than at any other hub; "
           "%s is next at %d." % (best, F["below"][best], ru, F["below"][ru]),
           "",
           "%s has the most workers at or above the standard (%d), but its induct area is predicted at %.1f dB(A) with "
           "the enclosure, so it brings %d below." % (big, F["pool"][big], F["levels"][big]["Lp"], F["below"][big])],
          18)
    _text(s, 0.7, 6.45, 12, 0.4, "Hearing conservation program, National WHS  |  Melissa Hayes  |  27 November 2026", 11, color=GREY)
    _strip(s, 1, "Exposure per Schedule 2, clause %s; reference weeks 12 October to 8 November 2026"
           % F["clauses_cited"]["exposure"])

    s = prs.slides.add_slide(blank)
    _text(s, 0.7, 0.45, 12, 0.6, "%s: %d workers brought below 85 dB(A), the most of any hub" % (best, F["below"][best]), 24, bold=True)
    _text(s, 0.7, 1.05, 12, 0.5, "Workers at or above the standard in the reference weeks, and brought below it by the enclosure", 13, color=GREY)
    rows, cols = len(hubs) + 1, 3
    tbl = s.shapes.add_table(rows, cols, Inches(0.7), Inches(1.7), Inches(9.2), Inches(0.45 * rows)).table
    tbl.first_row = True
    tbl.horz_banding = False
    tbl.columns[0].width = Inches(3.4)
    tbl.columns[1].width = Inches(2.9)
    tbl.columns[2].width = Inches(2.9)
    head = ["Hub", "At or above 85 dB(A)", "Brought below by the enclosure"]
    for j, h in enumerate(head):
        c = tbl.cell(0, j)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = INK
        para = c.text_frame.paragraphs[0]
        para.runs[0].font.size = Pt(13)
        para.runs[0].font.bold = True
        para.runs[0].font.color.rgb = WHITE
        if j:
            para.alignment = PP_ALIGN.RIGHT
    for i, h in enumerate(hubs, start=1):
        vals = [h, "%d" % F["pool"][h], "%d" % F["below"][h]]
        for j, v in enumerate(vals):
            c = tbl.cell(i, j)
            c.text = v
            c.fill.solid()
            c.fill.fore_color.rgb = TINT if h == best else PAPER
            para = c.text_frame.paragraphs[0]
            para.runs[0].font.size = Pt(13)
            para.runs[0].font.bold = (h == best)
            para.runs[0].font.color.rgb = INK
            if j:
                para.alignment = PP_ALIGN.RIGHT
    _text(s, 0.7, 5.2, 11.8, 1.5,
          ["Each worker's LAeq,8h is built from the hours they were signed on to an induct station (sorter control system "
           "operator sessions, joined to people through the site badge register) over the shifts they worked, the rest of "
           "the working day on the floor and the hour of breaks in the amenities.",
           "Labour-hire operatives are counted at the hub of their timesheet shifts; contractors' maintenance log-ons carry "
           "no shift and are left out."], 12, color=GREY)
    _strip(s, 2, "Sources: WCS session export 16 Nov 2026; badge register 13 Nov 2026; survey KA-2611-R1; design report QAE-0927 rev 2")

    s = prs.slides.add_slide(blank)
    _text(s, 0.7, 0.45, 12, 0.6, "%s leads; %s's induct area stays above 85 dB(A)" % (best, big), 24, bold=True)
    cd = CategoryChartData()
    cd.categories = hubs
    cd.add_series("Workers brought below 85 dB(A)", [F["below"][h] for h in hubs])
    fx, fy, fw, fh = 0.7, 1.3, 11.8, 5.45
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(fx), Inches(fy), Inches(fw), Inches(fh), cd)
    ch = gf.chart
    ch.has_title = False
    ch.has_legend = False
    _plot_layout(ch)
    plot = ch.plots[0]
    plot.gap_width = 80
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format = "0"
    dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(13)
    dl.font.color.rgb = INK
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
    va.minimum_scale = 0
    va.maximum_scale = AXIS_MAX
    va.major_unit = 20
    va.tick_labels.font.size = Pt(11)
    va.tick_labels.font.color.rgb = GREY
    ch.category_axis.tick_labels.font.size = Pt(12)
    k = hubs.index(best)
    cx = fx + fw * (PLOT[0] + PLOT[2] * (k + 0.5) / len(hubs))
    top = fy + fh * (PLOT[1] + PLOT[3] * (1 - F["below"][best] / AXIS_MAX))
    _text(s, cx - 1.5, top - 0.85, 3.0, 0.4, "%s, the hub chosen" % best, 13, bold=True, color=ACCENT,
          align=PP_ALIGN.CENTER)
    _strip(s, 3, "Counts per Schedule 2; induct area after the enclosure at the levels in design report QAE-0927 rev 2")

    prs.core_properties.author = "Melissa Hayes"
    prs.core_properties.comments = ""
    prs.core_properties.last_modified_by = "Melissa Hayes"
    prs.core_properties.title = "Induct enclosure 2027"
    import datetime as dt
    prs.core_properties.created = dt.datetime(2026, 11, 27, 10, 12, 0)
    prs.core_properties.modified = dt.datetime(2026, 11, 27, 15, 40, 0)
    prs.core_properties.revision = 3
    prs.save(path)
    _normalise_zip(path)


def _plot_layout(ch):
    """Pin the inner plot area so the annotation can sit over the chosen hub's bar."""
    from lxml import etree
    from pptx.oxml.ns import qn
    pa = ch._chartSpace.chart.plotArea
    old = pa.find(qn("c:layout"))
    if old is not None:
        pa.remove(old)
    lay = etree.SubElement(pa, qn("c:layout"))
    pa.remove(lay)
    pa.insert(0, lay)
    ml = etree.SubElement(lay, qn("c:manualLayout"))
    for tag, val in (("c:layoutTarget", "inner"), ("c:xMode", "edge"), ("c:yMode", "edge"),
                     ("c:x", PLOT[0]), ("c:y", PLOT[1]), ("c:w", PLOT[2]), ("c:h", PLOT[3])):
        etree.SubElement(ml, qn(tag)).set("val", str(val))


APP_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><TotalTime>94</TotalTime>'
           '<Words>{w}</Words><Application>Microsoft Office PowerPoint</Application>'
           '<PresentationFormat>Widescreen</PresentationFormat><Paragraphs>{p}</Paragraphs><Slides>{n}</Slides>'
           '<Notes>0</Notes><HiddenSlides>0</HiddenSlides><MMClips>0</MMClips><ScaleCrop>false</ScaleCrop>'
           '<HeadingPairs><vt:vector size="6" baseType="variant"><vt:variant><vt:lpstr>Fonts Used</vt:lpstr></vt:variant>'
           '<vt:variant><vt:i4>2</vt:i4></vt:variant><vt:variant><vt:lpstr>Theme</vt:lpstr></vt:variant><vt:variant>'
           '<vt:i4>1</vt:i4></vt:variant><vt:variant><vt:lpstr>Slide Titles</vt:lpstr></vt:variant><vt:variant>'
           '<vt:i4>{n}</vt:i4></vt:variant></vt:vector></HeadingPairs><TitlesOfParts><vt:vector size="{t}" '
           'baseType="lpstr"><vt:lpstr>Arial</vt:lpstr><vt:lpstr>Calibri</vt:lpstr><vt:lpstr>Office Theme</vt:lpstr>'
           '{titles}</vt:vector></TitlesOfParts><Company>Brolga Parcel Network</Company><LinksUpToDate>false'
           '</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>'
           '<AppVersion>16.0000</AppVersion></Properties>')


def _app_xml(zin):
    import re
    slides = sorted(n for n in zin.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n))
    words = paras = 0
    for n in slides:
        x = zin.read(n).decode("utf-8")
        for para in re.findall(r"<a:p>.*?</a:p>", x, flags=re.S):
            txt = " ".join(re.findall(r"<a:t>(.*?)</a:t>", para, flags=re.S)).strip()
            if txt:
                paras += 1
                words += len(txt.split())
    titles = "<vt:lpstr>PowerPoint Presentation</vt:lpstr>" * len(slides)
    return APP_XML.format(w=words, p=paras, n=len(slides), t=3 + len(slides), titles=titles).encode("utf-8")


def _normalise_zip(path):
    buf = io.BytesIO()
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in sorted(zin.infolist(), key=lambda i: i.filename):
            data = zin.read(item.filename)
            if item.filename == "docProps/app.xml":
                data = _app_xml(zin)
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
