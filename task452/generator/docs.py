"""The pack's documents: the reference sample design (January 2026), the extract of the emission reductions payment
agreement, the extract of the program's monitoring plan, the forest reference level summary and the release note
of the final change map (April 2026)."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import landscape as L   # noqa: E402
import world as W       # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1d20")
GREY = colors.HexColor("#5b6067")
GREEN = colors.HexColor("#1f5a3d")
S_BODY = ParagraphStyle("b", fontName="LiberationSans", fontSize=9.6, leading=13.6, textColor=INK, spaceAfter=6)
S_H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14.5, leading=18.5, textColor=GREEN, spaceAfter=4)
S_SUB = ParagraphStyle("sub", fontName="LiberationSans", fontSize=9.2, leading=12.8, textColor=GREY, spaceAfter=12)
S_H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.5, leading=14, textColor=GREEN, spaceBefore=8,
                      spaceAfter=3)
S_CELL = ParagraphStyle("c", fontName="LiberationSans", fontSize=8.6, leading=11, textColor=INK)
S_NUM = ParagraphStyle("cn", parent=S_CELL, alignment=2)
L_BODY = ParagraphStyle("lb", fontName="LiberationSerif", fontSize=10.5, leading=14.5, textColor=INK, spaceAfter=6)
L_NUM = ParagraphStyle("ln", parent=L_BODY, leftIndent=22, firstLineIndent=-22)
L_SUB = ParagraphStyle("ls", parent=L_BODY, leftIndent=40, firstLineIndent=-18)
L_H1 = ParagraphStyle("lh1", fontName="LiberationSerif-Bold", fontSize=13, leading=17, textColor=INK, alignment=1,
                      spaceAfter=3)
L_CAP = ParagraphStyle("lc", fontName="LiberationSerif-Italic", fontSize=9.5, leading=12.5, textColor=GREY,
                       alignment=1, spaceAfter=14)
L_H2 = ParagraphStyle("lh2", fontName="LiberationSerif-Bold", fontSize=11, leading=15, textColor=INK, spaceBefore=7,
                      spaceAfter=4)


def _doc(path, title, author, footer, serif=False):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSerif" if serif else "LiberationSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 12 * mm, footer)
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "%d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                          bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, num_cols=()):
    data = [[Paragraph(str(v), S_NUM if j in num_cols and i > 0 else S_CELL) for j, v in enumerate(r)]
            for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, GREEN), ("LINEBELOW", (0, -1), (-1, -1), 0.4, GREY),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]))
    return t


def published_strata():
    """the stratum areas the design report states: the preliminary map's pixel counts on the 30 m grid, in whole
    hectares"""
    return {s: int(round(v)) for s, v in L.strata_areas().items()}


def write_design(path):
    Ah = published_strata()
    doc, frame = _doc(path, "Reference sample 2024-2025: sample design", W.LAB,
                      "%s  |  Reference sample 2024-2025: design" % W.LAB)
    P = lambda t, s=S_BODY: Paragraph(t, s)
    rows = [["Stratum", "Preliminary map class (version 0.9)", "Area (ha)", "Points"]]
    for s, _, label in W.STRATA:
        rows.append([s, label, format(Ah[s], ","), format(W.N_SAMPLE[s], ",")])
    rows.append(["", "Accounting area", format(sum(Ah.values()), ","), format(sum(W.N_SAMPLE.values()), ",")])
    s = [P("Reference sample for the 2024-2025 reporting period: design", S_H1),
         P("%s, for the %s. %s. 26 January 2026." % (W.LAB, W.PROGRAM, W.PEOPLE["reference"]), S_SUB),
         P("1  Purpose", S_H2),
         P("The reference sample provides the reference data for the 2024-2025 reporting period of the %s: the "
           "activity data the monitoring report states and the accuracy assessment of the period's forest change "
           "map. It covers the program's accounting area, the twelve lowland districts on the 2019 district layer "
           "(11.8 million hectares)." % W.PROGRAM),
         P("2  Sampling design", S_H2),
         P("Stratified random sampling. The strata are the three classes of the preliminary forest change map "
           "2024-2025, version 0.9 of 15 January 2026, within the accounting area. Points were drawn at random within "
           "each stratum on 20 January 2026, 400 in the deforestation stratum and the remaining 3,600 split two to "
           "one between stable forest and non-forest. Stratum areas are the preliminary map's pixel counts on the 30 m "
           "grid."),
         _table(rows, (18, 74, 32, 22), num_cols=(2, 3)), Spacer(1, 8),
         P("3  Response design", S_H2),
         P("Each point is interpreted on the high-resolution mosaics of January 2024 and December 2025 by an "
           "interpreter of the laboratory, who records the land cover and the tree canopy cover class at both dates, "
           "whether the trees are a plantation, the change seen between the dates and, for a loss, the year and month "
           "of the first image showing it. The point is classed for the reporting period on the national forest "
           "definition of the monitoring plan."),
         P("4  Quality control", S_H2),
         P("One point in five, drawn at random, is re-interpreted by the ministry's team on its own form; every field "
           "recorded differently is settled by the reference coordinator and logged."),
         P("5  Contacts", S_H2),
         P("Reference data: %s. Change maps: %s." % (W.PEOPLE["reference"], W.PEOPLE["maps"]))]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_erpa(path):
    doc, frame = _doc(path, "Emission reductions payment agreement (extract)", W.FUND,
                      "%s and %s  |  Emission reductions payment agreement  |  Extract: articles 1 to 9" %
                      (W.FUND, W.MINISTRY), serif=True)
    s = [Paragraph("EMISSION REDUCTIONS PAYMENT AGREEMENT", L_H1),
         Paragraph("between the %s and the %s for the %s. Extract of articles 1 to 9; the annexes are not reproduced."
                   % (W.FUND, W.MINISTRY, W.PROGRAM), L_CAP)]
    N = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), L_NUM))
    M = lambda n, t: s.append(Paragraph("(%s)&nbsp;&nbsp;%s" % (n, t), L_SUB))
    N("1", "<b>Definitions.</b> In this agreement, <i>Accounting Area</i> means the program's twelve districts listed "
           "in the monitoring plan; <i>Reporting Period</i> means 1 January 2024 to 31 December 2025; <i>Monitoring "
           "Plan</i> means the program's monitoring plan as approved by the Facility; <i>Emission Factor</i> means "
           "497.0 tonnes of carbon dioxide equivalent per hectare of deforestation.")
    N("2", "<b>Reference level.</b> The reference level is %s hectares of deforestation a year. The reference level "
           "emissions for a Reporting Period are the reference level times the number of years in the period times "
           "the Emission Factor." % format(int(W.RL_HA_YEAR), ","))
    N("3", "<b>Monitoring report.</b> The Ministry shall submit a monitoring report for the Reporting Period by 30 "
           "June 2026, prepared in accordance with the Monitoring Plan.")
    N("4", "<b>Emission reductions.</b>")
    M("1", "The emission reductions for a Reporting Period are the reference level emissions for the period less the "
           "program's emissions from deforestation in the period.")
    M("2", "The program's emissions from deforestation are the area of deforestation in the Accounting Area in the "
           "Reporting Period, as the monitoring report states it to the nearest hundred hectares, times the Emission "
           "Factor.")
    N("5", "<b>Buffer.</b> Eighteen per cent of the emission reductions are set aside in the Facility's buffer reserve "
           "against reversals. The emission reductions the Ministry may offer are the remainder, in whole tonnes, any "
           "fraction of a tonne being dropped. Where the emission reductions are zero or less, none are offered.")
    N("6", "<b>Price.</b> The Facility pays USD 5.00 for each tonne offered and transferred.")
    N("7", "<b>Transfer.</b> The Ministry transfers the tonnes offered within sixty days of the Facility's acceptance "
           "of the monitoring report.")
    N("8", "<b>Verification.</b> The Facility may have the monitoring report verified before acceptance.")
    N("9", "<b>Reversals.</b> Reversals are drawn first from the buffer reserve.")
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_plan(path):
    doc, frame = _doc(path, "Monitoring plan (extract)", W.MINISTRY,
                      "%s  |  %s monitoring plan  |  Extract: sections 3 and 4" % (W.MINISTRY, W.PROGRAM))
    P = lambda t, s=S_BODY: Paragraph(t, s)
    rows = [["District (2019 layer)", "Code"]] + [[n, c] for c, n in W.DNAME.items()]
    s = [P("%s: monitoring plan (extract)" % W.PROGRAM, S_H1),
         P("%s. Approved version, March 2023. Sections 3 and 4 reproduced." % W.MINISTRY, S_SUB),
         P("3  Definitions", S_H2),
         P("3.1&nbsp;&nbsp;<b>Forest</b> is land of 0.5 hectares or more with tree canopy cover of 30 per cent or more, "
           "excluding tree plantations."),
         P("3.2&nbsp;&nbsp;<b>Deforestation</b> in a reporting period is the conversion of forest to other land: land "
           "that is forest on the first day of the period and other land on its last."),
         P("3.3&nbsp;&nbsp;The <b>accounting area</b> is the program's twelve lowland districts on the 2019 district "
           "layer:"),
         _table(rows, (60, 18)), Spacer(1, 8),
         P("4  Activity data", S_H2),
         P("4.1&nbsp;&nbsp;The area of deforestation in a reporting period is estimated from the reference sample of "
           "the %s: a probability sample of points in the accounting area, each interpreted on high-resolution "
           "imagery at the start and the end of the period and classed on the definitions of section 3." % W.NFMS),
         P("4.2&nbsp;&nbsp;The monitoring report presents the period's final forest change map, which shows where "
           "deforestation is located, with its accuracy assessment."),
         P("4.3&nbsp;&nbsp;The monitoring report states the 90 per cent confidence interval of the area of "
           "deforestation."),
         P("4.4&nbsp;&nbsp;Every reference point is interpreted by one interpreter; one in five is re-interpreted for "
           "quality control and the differences are adjudicated."),
         P("4.5&nbsp;&nbsp;For the benefit-sharing plan the monitoring report also states each district's area of "
           "deforestation: the part of the accounting area's estimate contributed by the reference points lying in "
           "the district.")]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_frel(path):
    doc, frame = _doc(path, "Forest reference level 2015-2022: summary", W.MINISTRY,
                      "%s  |  Forest reference level 2015-2022  |  Summary" % W.MINISTRY)
    P = lambda t, s=S_BODY: Paragraph(t, s)
    rows = [["Component", "Value"], ["Deforestation 2015-2022 (8 years)", "%s ha" % format(int(8 * W.RL_HA_YEAR), ",")],
            ["Reference level", "%s ha a year" % format(int(W.RL_HA_YEAR), ",")], ["Above-ground biomass, lowland forest", "248.4 t dry matter per ha"],
            ["Root to shoot ratio", "0.24"], ["Carbon fraction", "0.47"], ["Carbon after conversion", "9.22 t C per ha"],
            ["Emission factor", "497.0 t CO2e per ha"]]
    s = [P("Forest reference level 2015-2022: summary", S_H1),
         P("%s. Assessed and approved by the %s, November 2023." % (W.MINISTRY, W.FUND), S_SUB),
         P("The reference level is the average annual area of deforestation in the accounting area over 2015-2022, "
           "estimated from the %s reference sample of that period (6,000 points interpreted on high-resolution "
           "imagery), times the emission factor. The emission factor is the carbon stock of lowland forest from the "
           "national forest inventory (610 plots measured 2018-2022) less the carbon of the land that replaces it, "
           "expressed in carbon dioxide equivalent." % W.NFMS),
         _table(rows, (90, 50), num_cols=(1,)), Spacer(1, 8),
         P("The reference level and the emission factor apply to every reporting period of the emission reductions "
           "payment agreement.")]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_release(path):
    doc, frame = _doc(path, "Final forest change map 2024-2025, version 2.0", W.LAB,
                      "%s  |  Forest change map 2024-2025  |  Release note, version 2.0" % W.LAB)
    P = lambda t, s=S_BODY: Paragraph(t, s)
    s = [P("Final forest change map 2024-2025, version 2.0", S_H1),
         P("%s. Release note. %s. 22 April 2026." % (W.LAB, W.PEOPLE["maps"]), S_SUB),
         P("Version 2.0 replaces the preliminary version 0.9 of 15 January 2026. The preliminary map was classified "
           "from the optical mosaics available in early January, and in the cloudier districts it carried cloud "
           "shadow and leaf-off canopy as loss and missed clearings under persistent cloud. Version 2.0 adds the "
           "radar time series and the late-season optical scenes, re-runs the classification over the whole country "
           "and applies the 0.5 hectare minimum mapping unit to each patch of change on the national mosaic."),
         P("Classes: deforestation 2024-2025, stable forest, non-forest. The class raster is delivered on the 30 m "
           "grid, the deforestation polygons by 10 km tile and by quarter of first detection. Class areas by district "
           "are in the statistics workbook."),
         P("Version 2.0 is the map the 2024-2025 monitoring report presents.")]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)
