"""The pack's documents and registers: Tarvane's low-methane rating standard, Talmora's survey methods note and controlled-release
workbook, the folder's data dictionary and manifest."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P    # noqa: E402
import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1d1f21")
GREY = colors.HexColor("#5a5f66")
RUST = colors.HexColor("#8a3b12")
NAVY = colors.HexColor("#1f3a5f")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.5, leading=14.5, textColor=INK, spaceAfter=6)
NUM = ParagraphStyle("num", parent=BODY, leftIndent=30, firstLineIndent=-30)
H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=RUST, spaceAfter=2)
H1N = ParagraphStyle("h1n", parent=H1, textColor=NAVY)
H1S = ParagraphStyle("h1s", fontName="LiberationSans", fontSize=10, leading=13, textColor=GREY, spaceAfter=10)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.5, leading=14, textColor=INK, spaceBefore=7, spaceAfter=3)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.8, leading=11, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.5, leading=11, textColor=GREY)


def _doc(path, title, author, footer):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(1.0 * inch, 0.6 * inch, footer)
        canvas.drawRightString(LETTER[0] - 1.0 * inch, 0.6 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=1.0 * inch, rightMargin=1.0 * inch, topMargin=0.9 * inch,
                          bottomMargin=0.95 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eaed")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))


TITLE = {"ratings": "Head of Methane Ratings", "provider": "Chief Scientist"}


# ------------------------------------------------------------------------------------------- the rating standard
def write_standard(path):
    doc, frame = _doc(path, "Low-Methane Producer Rating Standard", W.ORG,
                      "%s  |  TMR-STD-03 Low-Methane Producer Rating Standard, %s  |  Version 1.1, approved 2 September 2026"
                      % (W.ORG, W.BASIN))
    s = [Paragraph("Low-Methane Producer Rating Standard: %s" % W.BASIN, H1),
         Paragraph("%s. Standard TMR-STD-03, version 1.1, approved by the ratings committee on 2 September 2026. Owner: "
                   "%s, %s." % (W.ORG, W.PEOPLE["ratings"], TITLE["ratings"]), H1S)]
    P_ = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("1. Purpose", H2))
    P_("1.1", "%s rates the gas producers operating in the %s each year for the utilities and marketers that buy their "
              "gas. A producer rated low-methane carries the rating for the calendar year after the rating year it was "
              "measured on; the 2027 ratings rest on the rating year 1 October 2025 to 30 September 2026." %
              (W.ORG_SHORT, W.BASIN))
    s.append(Paragraph("2. Definitions", H2))
    P_("2.1", "<b>Rating year:</b> the twelve months from 1 October to 30 September.")
    P_("2.2", "<b>A producer's sites:</b> the well pads, tank batteries and compressor stations it operates in the basin, "
              "as %s's site register lists them. A site counts to the producer operating it on the day a campaign "
              "images it, and for the part of the rating year that producer operated it." % W.ORG_SHORT)
    P_("2.3", "<b>A producer's wells:</b> the wells for which it is the operator of record in the %s's production "
              "reports, each production month to the operator of record for that month." % W.AGENCY)
    P_("2.4", "<b>Methane produced:</b> the gas the producer's wells produced over the rating year, from the latest "
              "report for each well and month, at 14.73 psia and 60 °F, times the methane share of the field's gas "
              "in its latest composite analysis, at 19.2 kg of methane per thousand cubic feet; in metric tonnes.")
    P_("2.5", "<b>Measured methane intensity:</b> the methane the producer's sites emitted over the rating year at rates "
              "of 5 kg per hour or more, measured with the year's aerial campaigns, as a share of its methane produced, "
              "both in metric tonnes; in per cent.")
    s.append(Paragraph("3. The rating", H2))
    P_("3.1", "A producer is rated low-methane for the calendar year after the rating year when its measured methane "
              "intensity over the rating year is 0.20 per cent or less.")
    P_("3.2", "The ratings committee issues the ratings by 15 December. A rating is not revised during its year.")
    s.append(Paragraph("4. Measurement", H2))
    P_("4.1", "Each rating year %s commissions four basin-wide aerial campaigns about three months apart. A campaign "
              "flies the basin in north-south lines that image every producer site once; a site near the edge of two "
              "lines may be imaged on both, and a line lost to cloud leaves its sites without an image in that "
              "campaign." % W.ORG_SHORT)
    P_("4.2", "A plume belongs to the register site nearest its estimated origin within 150 m.")
    P_("4.3", "A site's methane emitted over the part of the rating year a producer operated it is the site's emission "
              "rate at 5 kg per hour or more, averaged over the campaigns flown in that part with each campaign counting "
              "equally, times the hours in that part. A site imaged on two lines in a campaign counts the mean of the two "
              "passes; a campaign that left a site without an image does not count for that site.")
    P_("4.4", "The records for this standard are %s's site register, the survey provider's plume detections, "
              "flight-line coverage and controlled-release study, the %s's production reports and the fields' composite "
              "gas analyses." % (W.ORG_SHORT, W.AGENCY))
    s.append(Spacer(1, 10))
    s.append(Paragraph("Supersedes version 1.0 (11 March 2025). Next review: after the 2027 ratings are issued.", SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------- Talmora's methods note
def write_methods(path, summary):
    doc, frame = _doc(path, "Survey methods note: Tollaver Basin campaigns", W.PROVIDER,
                      "%s  |  Technical note TA-TN-26-07  |  Issued 12 October 2026" % W.PROVIDER)
    s = [Paragraph("Survey Methods Note: %s Campaigns, 2025-2026" % W.BASIN, H1N),
         Paragraph("%s technical note TA-TN-26-07, issued 12 October 2026 for %s. Prepared by %s, %s." %
                   (W.PROVIDER, W.ORG, W.PEOPLE["provider"], TITLE["provider"]), H1S)]
    P_ = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("1. Instrument and flights", H2))
    P_("1.1", "Talmora's airborne imaging spectrometer measures methane's shortwave-infrared absorption from about "
              "3,000 m above ground, with ground pixels of about 3 m.")
    P_("1.2", "Each campaign flies 18 north-south lines over the basin. Adjacent lines overlap by a few hundred metres, so "
              "a facility near a line's edge can be imaged on two lines, minutes apart. A line lost to cloud is not "
              "re-flown within the campaign.")
    s.append(Paragraph("2. Detection and quantification", H2))
    P_("2.1", "A plume is reported when the methane enhancement over a source stands clear of the scene's background. A "
              "pass does not detect every plume: the chance of detecting a plume rises with its emission rate.")
    P_("2.2", "Each reported plume's emission rate is estimated from its integrated methane enhancement and the 10 m wind "
              "from a weather reanalysis, and is given with its one-sigma uncertainty, typically 20 to 30 per cent for a "
              "single plume.")
    P_("2.3", "Each plume's estimated origin is reported with the nearest facility in the %s's facility list within "
              "150 m and the distance to it; a plume with no facility within 150 m, along a gathering line for example, "
              "is reported without one." % W.AGENCY)
    P_("2.4", "Processing version L2-v2.3 was used for TB-2511 and TB-2602 and L2-v2.4 for TB-2605 and TB-2608; "
              "version 2.4 changes the output layout only.")
    s.append(Paragraph("3. Coverage", H2))
    P_("3.1", "The coverage file lists, for each campaign and flight line, every facility under the line, the times the "
              "line was flown and whether it was imaged.")
    rows = [["Campaign", "Flight days", "Lines flown", "Lines lost to cloud", "Plumes reported"]]
    for c in summary:
        rows.append(c)
    s.append(_table(rows, [1.0 * inch, 1.75 * inch, 1.0 * inch, 1.3 * inch, 1.2 * inch]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("4. Validation", H2))
    P_("4.1", "Talmora's 2025 single-blind controlled-release study at its test range: 182 releases of 0.8 to 80 kg/h "
              "between 18 August and 1 October 2025, metered by the range operator and flown with the same instrument, "
              "altitude and processing as the basin campaigns. Each release's metered rate, the wind, whether Talmora "
              "reported a plume and the rate it quantified are in the study workbook.")
    P_("4.2", "Talmora describes the chance that a pass detects a plume as a logistic function of the natural logarithm "
              "of the plume's emission rate alone, fitted by maximum likelihood to the study's releases; the wind over "
              "the study, 1.5 to 8 m/s, made no measurable difference to it.")
    s.append(Spacer(1, 10))
    s.append(Paragraph("Questions on this note: %s, %s." % (W.PEOPLE["provider"], TITLE["provider"]), SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_releases(path, rel):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Releases"
    ws.append(["release_id", "test_date", "metered_rate_kg_h", "wind_speed_10m_m_s", "plume_detected", "quantified_rate_kg_h"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in rel:
        ws.append(["CR25-%03d" % (r["i"] + 1), r["day"], round(r["rate"], 2), round(r["wind"], 1), "Y" if r["detected"] else "N",
                   round(r["est"], 1) if r["est"] is not None else None])
    for row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        for c in row:
            c.number_format = "yyyy-mm-dd"
    for col, w in zip("ABCDEF", (11, 12, 18, 19, 15, 21)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    n = wb.create_sheet("Notes")
    for line in ["Talmora Aerial 2025 single-blind controlled-release study, Talmora test range.",
                 "Releases 18 August to 1 October 2025. Rates metered by the range operator (Coriolis meter) and withheld "
                 "from Talmora's analysts until results were submitted.",
                 "Instrument, flight altitude and processing as flown for the Tollaver Basin campaigns.",
                 "plume_detected: Y where Talmora reported a plume at the release point; quantified_rate_kg_h is Talmora's rate "
                 "for it."]:
        n.append([line])
    n.column_dimensions["A"].width = 120
    wb.save(path)


# --------------------------------------------------------------------------------------------- the dictionary
def write_dictionary(path, counts):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    F = W.FILES
    c = lambda k: format(counts[k], ",")
    rows = [
        (F["plumes"], "", "%s's plume detections for the four %s campaigns of the 2025-2026 rating year, one row per "
                          "reported plume. %s rows." % (W.PROVIDER_SHORT, W.BASIN, c("plumes"))),
        (F["plumes"], "image_time_utc", "Time the plume was imaged, UTC."),
        (F["plumes"], "plume_lat, plume_lon", "The plume's estimated origin, decimal degrees (WGS 84)."),
        (F["plumes"], "emission_rate_kg_h", "Emission rate the plume was quantified at, kilograms of methane per hour."),
        (F["plumes"], "rate_uncertainty_kg_h", "One-sigma uncertainty of the rate, kilograms per hour."),
        (F["plumes"], "wind_speed_10m_m_s", "Reanalysis wind at 10 m used for the rate, metres per second."),
        (F["plumes"], "nearest_facility", "The commission's facility number nearest the origin within 150 m; blank where "
                                          "none is within 150 m."),
        (F["coverage"], "", "%s's flight-line coverage: one row per campaign, flight line and facility under the line. %s "
                            "rows." % (W.PROVIDER_SHORT, c("coverage"))),
        (F["coverage"], "imaged", "Y where the line was flown and imaged; N where the line was lost."),
        (F["releases"], "", "%s's 2025 controlled-release study, one row per release (sheet Releases)." % W.PROVIDER_SHORT),
        (F["sites"], "", "%s's register of the rated producers' sites in the basin. %s rows." % (W.ORG_SHORT, c("sites"))),
        (F["sites"], "facility_numbers", "The commission's facility number or numbers for the site, separated by semicolons."),
        (F["sites"], "operator, operator_since, previous_operator", "The producer operating the site, the date it took over, "
                                                                     "and the producer before it where the site changed hands."),
        (F["production"], "", "The %s's monthly well production reports for the basin's wells, production months October "
                              "2025 to September 2026 as received by the pull. %s rows." % (W.AGENCY, c("production"))),
        (F["production"], "gas_mcf", "Gas produced in the month, thousand cubic feet at 14.65 psia (the commission's "
                                     "pressure base)."),
        (F["production"], "report_type", "ORIGINAL or AMENDED. An amended report replaces the earlier report for the well "
                                         "and month."),
        (F["operators"], "", "The %s's operator list for the basin's operators." % W.AGENCY),
        (F["gas"], "", "Composite analyses of each field's gas, mole per cent, with the heating value in Btu per standard "
                       "cubic foot."),
        (F["flaring"], "", "The %s's monthly flaring and venting reports by lease. %s rows." % (W.AGENCY, c("flaring"))),
        (F["flaring"], "disposition_code", "Commission disposition code: FL flared, VT vented."),
        (F["flaring"], "volume_mcf", "Volume, thousand cubic feet."),
        (F["leases"], "", "The %s's lease register: each lease's operator and the date it took over the lease." % W.AGENCY),
        (F["basin"], "", "The %s's monthly basin summary of reported flared and vented gas, all operators, thousand cubic "
                         "feet." % W.AGENCY),
        (F["statements"], "", "The %s's monthly allocation statements to its shippers, one row per statement line. %s "
                              "rows." % (W.PLANT, c("statements"))),
        (F["statements"], "statement_month", "The month of the statement."),
        (F["statements"], "reference", "The plant's reference for the line."),
        (F["statements"], "volume_mcf, energy_mmbtu", "Gas received, thousand cubic feet at 14.73 psia, and its energy, "
                                                      "million Btu; the volume is blank where the station meters energy only."),
        (F["stations"], "", "The plant's meter stations, the shipper each delivers for and the shipper's commission operator "
                            "number."),
        (F["heating"], "", "Each station's monthly gas heating value, Btu per standard cubic foot."),
        (F["ghgrp"], "", "The producers' Subpart W greenhouse gas reports for their basin facilities, reporting years 2023 "
                         "to 2025, methane by emission source, metric tons (carbon dioxide equivalent at a GWP of 25)."),
        (F["satellite"], "", "A satellite product's monthly methane estimates for the basin as a whole, tonnes per hour."),
        (F["manifest"], "", "The files in this folder with their source, date and access."),
    ]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Field definitions"
    ws.append(["Source file", "Column", "What it holds"])
    for r in rows:
        ws.append([v or None for v in r])
    head = PatternFill("solid", fgColor="E8EAED")
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.fill = head
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["C"].width = 92
    ws.freeze_panes = "A2"
    wb.save(path)


def write_manifest(path, counts):
    F = W.FILES
    rows = [
        [F["plumes"], "%s, plume detections, %s campaigns TB-2511 to TB-2608" % (W.PROVIDER, W.BASIN), "2026-10-12",
         counts["plumes"], "Tarvane under the survey contract"],
        [F["coverage"], "%s, flight-line coverage, the same campaigns" % W.PROVIDER, "2026-10-12", counts["coverage"],
         "Tarvane under the survey contract"],
        [F["releases"], "%s, 2025 controlled-release study workbook" % W.PROVIDER, "2025-11-20", "", "Tarvane under the "
         "survey contract"],
        [F["methods"], "%s, technical note TA-TN-26-07" % W.PROVIDER, "2026-10-12", "", "Tarvane under the survey contract"],
        [F["standard"], "%s, TMR-STD-03 version 1.1" % W.ORG_SHORT, "2026-09-02", "", "Tarvane, published to subscribers"],
        [F["sites"], "%s site register, rated producers' sites" % W.ORG_SHORT, "2026-11-10", counts["sites"], "Tarvane internal"],
        [F["production"], "%s, well production reports, basin counties" % W.AGENCY, "2026-11-15", counts["production"],
         "public records"],
        [F["operators"], "%s, operator list" % W.AGENCY, "2026-11-15", counts["operators"], "public records"],
        [F["gas"], "Producers' composite gas analyses by field, as filed with %s" % W.ORG_SHORT, "2026-04-30", counts["gas"],
         "Tarvane under the producers' data agreements"],
        [F["flaring"], "%s, flaring and venting reports, basin leases" % W.AGENCY, "2026-11-15", counts["flaring"],
         "public records"],
        [F["leases"], "%s, lease register" % W.AGENCY, "2026-11-15", counts["leases"], "public records"],
        [F["basin"], "%s, monthly basin flaring and venting summary" % W.AGENCY, "2026-11-15", counts["basin"], "public records"],
        [F["statements"], "%s, monthly allocation statements" % W.PLANT, "2026-11-14", counts["statements"],
         "Tarvane under the plant's data agreement"],
        [F["stations"], "%s, meter station list" % W.PLANT, "2026-11-14", counts["stations"], "Tarvane under the plant's data "
         "agreement"],
        [F["heating"], "%s, station heating values" % W.PLANT, "2026-11-14", counts["heating"], "Tarvane under the plant's "
         "data agreement"],
        [F["ghgrp"], "EPA greenhouse gas reporting data, Subpart W, the producers' basin facilities", "2026-10-06",
         counts["ghgrp"], "public records"],
        [F["satellite"], "Satellite basin methane product, version 2.1", "2026-10-28", "", "licensed"],
        [F["dict"], "%s ratings team, field definitions for this folder" % W.ORG_SHORT, W.PACK_DATE.isoformat(), "",
         "Tarvane internal"],
    ]
    out = [[r[0], r[1], r[2], r[3], r[4]] for r in rows]
    return P.write_csv(path, ["file_name", "contents", "as_of", "rows", "terms"], out)
