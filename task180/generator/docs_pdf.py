"""The two PDFs in the pack: the governing standard ES-DGA-02 and the 2026 switchboard thermal
imaging survey. reportlab runs with invariant output so two builds give the same bytes."""
import re

from reportlab import rl_config

rl_config.invariant = 1

from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import (KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table,  # noqa: E402
                                TableStyle)

import world as W  # noqa: E402

SS = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12.2,
                      spaceAfter=3)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=7.8, leading=9.8)
H1 = ParagraphStyle("h1", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14,
                    spaceBefore=8, spaceAfter=3, keepWithNext=1)
H2 = ParagraphStyle("h2", parent=BODY, fontName="Helvetica-Bold", fontSize=9.4, spaceBefore=4, spaceAfter=1,
                    keepWithNext=1)
TITLE = ParagraphStyle("title", parent=SS["Title"], fontName="Helvetica-Bold", fontSize=15, leading=19,
                       alignment=0, spaceAfter=2)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.2, leading=10, spaceAfter=0)
GRID = TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.2),
                   ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.2),
                   ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#7d8590")),
                   ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e9ee")),
                   ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                   ("ALIGN", (1, 1), (-1, -1), "RIGHT")])


def _pin_dates(path, stamp):
    """Replace reportlab's invariant date with the document's own date, at equal length."""
    b = open(path, "rb").read()
    new = stamp.encode()
    for m in set(re.findall(rb"D:\d{14}\+00'00'", b)):
        b = b.replace(m, b"D:" + new + b"+12'00'")
    open(path, "wb").write(b)


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555b63"))
        canvas.drawString(18 * mm, 11 * mm, text)
        canvas.drawRightString(A4[0] - 18 * mm, 11 * mm, f"Page {doc.page}")
        canvas.restoreState()
    return draw


def table_a(tab, title):
    head = ["Gas (ppm)", "Sealed\nunder 10", "Sealed\n10 to 30", "Sealed\nover 30",
            "Free-breathing\nunder 10", "Free-breathing\n10 to 30", "Free-breathing\nover 30"]
    rows = [head]
    for g in W.GASES:
        name = {"H2": "Hydrogen H2", "CH4": "Methane CH4", "C2H6": "Ethane C2H6", "C2H4": "Ethylene C2H4",
                "C2H2": "Acetylene C2H2", "CO": "Carbon monoxide CO", "CO2": "Carbon dioxide CO2"}[g]
        vals = list(tab["SL"][g]) + list(tab["FB"][g])
        rows.append([name] + [f"{v:,}" for v in vals])
    t = Table(rows, colWidths=[36 * mm] + [23 * mm] * 6, repeatRows=1)
    t.setStyle(GRID)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 7.4)]))
    return [Paragraph(title, H2), t, Spacer(1, 4)]


def write_standard(path):
    story = []
    story.append(Paragraph("Ellesmere Lines Limited", SMALL))
    story.append(Paragraph("ES-DGA-02 Fleet DGA condition standard", TITLE))
    story.append(Paragraph("Zone substation power transformers, 33/11 kV", BODY))
    ctrl = Table([
        ["Document", "ES-DGA-02", "Revision", "3"],
        ["Owner", "Barry Forbes, Zone Substation Engineer", "Approved", "12 June 2025"],
        ["Approved by", "Emma Elliott, General Manager Network", "Next review", "June 2028"],
    ], colWidths=[24 * mm, 70 * mm, 22 * mm, 50 * mm])
    ctrl.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.2),
                              ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.2),
                              ("FONT", (2, 0), (2, -1), "Helvetica-Bold", 8.2),
                              ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#7d8590"))]))
    story += [Spacer(1, 4), ctrl, Spacer(1, 6)]

    def sec(title, paras):
        story.append(Paragraph(title, H1))
        for p in paras:
            story.append(Paragraph(p, BODY))

    sec("1 Scope", [
        "1.1 This standard sets how Ellesmere Lines samples, codes and prioritises its zone substation "
        "power transformers on the dissolved gas analysis (DGA) of their insulating oil. It applies to the "
        "44 transformers held in the asset register as in service at the 22 zone substations.",
        "1.2 Bushings, cooling plant and transformer protection are assessed under ES-MNT-07 and are outside "
        "this standard.",
    ])
    sec("2 References", [
        "IEC 60567 Oil-filled electrical equipment, sampling of free gases and analysis of dissolved gases. "
        "IEC 60599 Interpretation of the analysis of gases in transformers. IEEE C57.104 Guide for the "
        "interpretation of gases generated in mineral oil-immersed transformers. IEC 60422 Mineral "
        "insulating oils in electrical equipment, supervision and maintenance guidance. ES-MNT-07 Zone "
        "substation maintenance schedule.",
    ])
    sec("3 Sampling and laboratory results", [
        "3.1 Main-tank oil is sampled from every transformer in a quarterly round in March, June, September "
        "and December. The zone substation engineer may place a transformer on monthly sampling between "
        "rounds.",
        "3.2 Samples are drawn into glass syringes in accordance with IEC 60567 and analysed by the "
        "contracted laboratory for hydrogen, methane, ethane, ethylene, acetylene, carbon monoxide, carbon "
        "dioxide, oxygen and nitrogen, and for water content by coulometric titration to IEC 60814.",
        "3.3 The sampling technician writes the date and time of sampling and the top-oil temperature read "
        "from the transformer's gauge on the sample label.",
        "3.4 The laboratory report of record for a sample is the latest issue for its sample ID. Earlier "
        "issues are kept on file for audit.",
        "3.5 A result below the laboratory's limit of detection counts as half the limit of detection.",
    ])
    sec("4 Condition coding", [])
    story.append(Paragraph("4.1 Preservation class and age band", H2))
    story.append(Paragraph(
        "A transformer's preservation class is set by the ratio of oxygen to nitrogen in its latest main-tank "
        "sample: sealed where O2/N2 is 0.2 or less, free-breathing where it is above 0.2. Its age band is its "
        "age in whole years at the latest sample, counted from the year of manufacture or, for a rewound "
        "transformer, the year of the rewind: under 10 years, 10 to 30 years, or over 30 years.", BODY))
    story.append(Paragraph("4.2 Gas levels", H2))
    story.append(Paragraph(
        "Each gas in the latest sample is compared with its 90th and 95th percentile values in tables A1 and "
        "A2 for the transformer's preservation class and age band.", BODY))
    story.append(Paragraph("4.3 Twelve-month increase", H2))
    story.append(Paragraph(
        "The twelve-month increase of a gas is its value in the latest sample less its value in the base "
        "sample, multiplied by 365 and divided by the number of days between the sampling dates of the two "
        "samples. The base sample is the most recent main-tank sample taken 330 days or more before the "
        "latest sample. Each increase is compared with the rate limit for the gas in table A3 for the "
        "transformer's preservation class.", BODY))
    story.append(Paragraph("4.4 Condition code and severity score", H2))
    story.append(Paragraph(
        "Code 3: at least one gas exceeds its 95th percentile value and has a twelve-month increase above its "
        "rate limit. Code 2: not code 3, and at least one gas exceeds its 90th percentile value or has a "
        "twelve-month increase above its rate limit. Code 1: neither.", BODY))
    story.append(Paragraph(
        "The severity score of a transformer is the largest, over the seven fault gases (hydrogen, methane, "
        "ethane, ethylene, acetylene, carbon monoxide and carbon dioxide), of the gas's twelve-month increase "
        "divided by its rate limit. A gas whose value fell counts as zero. Severity scores are reported to two "
        "decimal places.", BODY))
    story.append(Paragraph(
        "4.5 Codes and severity scores are reviewed by the zone substation engineer after each quarterly "
        "round.", BODY))
    sec("5 Inspection priority", [
        "5.1 An internal inspection, with the oil drained and the main tank entered to examine the windings, "
        "leads, connections, core and clamping structure, is the remedy for a fault in the main tank.",
        "5.2 Internal inspection outages are allocated to the code 3 transformers with such a fault, in "
        "descending order of severity score.",
        "5.3 A transformer taken out for internal inspection is covered by the mobile substation for the "
        "outage, so the number of inspections in a year is the number of mobile substation windows held.",
    ])
    sec("6 Tap-changer service records", [
        "6.1 The maintenance log is the record of tap-changer services.",
        "6.2 On-load tap changers are serviced at the intervals in annex B. Operations since a service are "
        "counted on the tap changer's operations counter as read by SCADA.",
        "6.3 A tap changer whose operations or elapsed time since its last service exceed its interval is past "
        "its service interval.",
    ])
    sec("7 Water in oil", [
        "7.1 Water in oil is assessed as relative saturation at the oil temperature at sampling (annex C). "
        "Transformers above 30 per cent relative saturation are considered for oil processing.",
    ])
    story.append(Paragraph("Annex A Gas level and rate tables", H1))
    story += table_a(W.A1, "Table A1 90th percentile gas levels, ppm, by preservation class and age band")
    story += table_a(W.A2, "Table A2 95th percentile gas levels, ppm, by preservation class and age band")
    rows = [["Gas", "Sealed", "Free-breathing"]]
    for g in W.GASES:
        a, b = W.A3["SL"][g], W.A3["FB"][g]
        f = (lambda x: f"{x:.1f}" if g == "C2H2" else f"{int(x):,}")
        rows.append([{"H2": "Hydrogen H2", "CH4": "Methane CH4", "C2H6": "Ethane C2H6",
                      "C2H4": "Ethylene C2H4", "C2H2": "Acetylene C2H2", "CO": "Carbon monoxide CO",
                      "CO2": "Carbon dioxide CO2"}[g], f(a), f(b)])
    t = Table(rows, colWidths=[40 * mm, 30 * mm, 30 * mm], repeatRows=1)
    t.setStyle(GRID)
    story += [KeepTogether([Paragraph("Table A3 Rate limits, twelve-month increase in ppm", H2), t]),
              Spacer(1, 6)]
    story.append(Paragraph("Annex B Tap-changer service intervals", H1))
    t = Table([["Tap changer type", "Operations", "Years", "Interval"],
               ["In-oil arcing diverter", "60,000", "7", "whichever comes first"],
               ["Vacuum", "300,000", "10", "whichever comes first"]],
              colWidths=[48 * mm, 28 * mm, 20 * mm, 45 * mm])
    t.setStyle(GRID)
    story += [t, Spacer(1, 3),
              Paragraph("Operations and years are counted from the last service recorded in the maintenance "
                        "log. The tap changer type is as held in the asset register.", BODY)]
    story.append(Paragraph("Annex C Relative saturation of water in oil", H1))
    story.append(Paragraph(
        "The water saturation limit of mineral oil at temperature T (degrees C) is "
        "Ws = 10<super>(7.42 - 1670/(T + 273))</super> ppm, and the relative saturation is "
        "RS = water content / Ws x 100, in per cent.", BODY))
    story.append(Paragraph(
        "T is the oil temperature written on the sample record. Where none is written, T is the SCADA "
        "top-oil temperature for the hour in which the sample was drawn, New Zealand time.", BODY))
    story.append(Paragraph("Revision history", H1))
    t = Table([["Rev", "Date", "Change"],
               ["1", "March 2018", "First issue"],
               ["2", "August 2021", "Monthly sampling at the engineer's discretion"],
               ["3", "June 2025", "Level tables by preservation class and age band; twelve-month increase; "
                                  "severity score; annex C"]],
              colWidths=[12 * mm, 26 * mm, 128 * mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.0),
                           ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.0),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#7d8590"))]))
    story.append(t)
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="ES-DGA-02 Fleet DGA condition standard",
                            author="Ellesmere Lines", creator="Ellesmere Lines", subject="Network standard",
                            producer="Ellesmere Lines")
    foot = _footer("ES-DGA-02 Rev 3. Uncontrolled when printed. Ellesmere Lines Limited.")
    doc.build(story, onFirstPage=foot, onLaterPages=foot)
    _pin_dates(path, "20250612093000")


def write_thermal(path, findings):
    story = [Paragraph("Weka Thermal Imaging Ltd", SMALL),
             Paragraph("Infrared survey: 11 kV switchboards and cable terminations", TITLE),
             Paragraph("Client: Ellesmere Lines Limited, zone substations. Survey dates 9 to 20 March 2026. "
                       "Report WTI-2603-118, issued 2 April 2026. Thermographer: Aimee Craig (Level II).", BODY),
             Spacer(1, 4)]
    story.append(Paragraph("Scope and conditions", H1))
    story.append(Paragraph(
        "Indoor 11 kV switchboards (circuit breaker panels, busbar chambers through inspection windows, "
        "cable termination boxes) and the outdoor 33 kV incoming connections at the 22 zone substations. "
        "Transformers, their tanks, radiators and tap changers were not part of the scope. Panels were scanned "
        "with doors closed through infrared windows where fitted, otherwise from the panel front. Ambient "
        "inside switchrooms was 14 to 23 C. Loads at the time of each scan are from the client's SCADA and are "
        "shown so that rises can be read against loading.", BODY))
    story.append(Paragraph("Method and priority", H1))
    story.append(Paragraph(
        "Temperature rise is measured against a like component in the same panel or phase under the same load. "
        "Priority 1: rise above 40 K, repair immediately. Priority 2: 20 to 40 K, repair within one month. "
        "Priority 3: 10 to 20 K, repair at the next planned outage. Priority 4: 3 to 10 K, monitor at the "
        "next survey.", BODY))
    story.append(Paragraph("Findings", H1))
    rows = [["Ref", "Substation", "Location", "Component", "Max C", "Rise K", "Load A", "Priority"]]
    for f in findings:
        rows.append(list(f))
    t = Table([[Paragraph(str(c), CELL) for c in r] for r in rows],
              colWidths=[13 * mm, 22 * mm, 30 * mm, 46 * mm, 14 * mm, 14 * mm, 14 * mm, 15 * mm],
              repeatRows=1)
    t.setStyle(GRID)
    story += [t, Spacer(1, 6)]
    story.append(Paragraph(
        "All other panels and connections scanned showed no rise above 3 K. Images for each finding are in the "
        "appendix supplied separately. Re-survey recommended in March 2027.", BODY))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="Infrared survey 11 kV switchboards March 2026",
                            author="Weka Thermal Imaging", creator="Weka Thermal Imaging",
                            subject="Thermography", producer="Weka Thermal Imaging")
    foot = _footer("Weka Thermal Imaging Ltd. Report WTI-2603-118.")
    doc.build(story, onFirstPage=foot, onLaterPages=foot)
    _pin_dates(path, "20260402141500")
