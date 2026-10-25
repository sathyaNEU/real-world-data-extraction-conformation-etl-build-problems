"""task301 documents: the development team's build decision note (docx), the candidates' terms (xlsx, a distractor),
the three module generations' datasheets (pdf, a distractor) and the pyranometer calibration certificates (xlsx, ask A)."""
import datetime as dt

import numpy as np
from docx import Document
from docx.shared import Pt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import postprocess


def _xlsx(path, sheets, made, saved, author):
    wb = Workbook()
    for i, (title, header, rows, widths, fmts) in enumerate(sheets):
        ws = wb.active if i == 0 else wb.create_sheet()
        ws.title = title
        if header is None:
            for r in rows:
                ws.append(list(r))
            for j, w in enumerate(widths, 1):
                ws.column_dimensions[get_column_letter(j)].width = w
            continue
        ws.append(header)
        for c in ws[1]:
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="DDE5EA")
            c.alignment = Alignment(vertical="top", wrap_text=True)
        for r in rows:
            ws.append(list(r))
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(j)].width = w
        for col, f in (fmts or {}).items():
            j = header.index(col) + 1
            for k in range(2, len(rows) + 2):
                ws.cell(row=k, column=j).number_format = f
        ws.freeze_panes = "A2"
    wb.properties.creator = author
    wb.properties.lastModifiedBy = author
    wb.save(path)
    postprocess.scrub(path, P.ORG, saved[:10])
    postprocess.finish_office(path, made, saved, P.ADVISER)


def note(path):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading("2027 build: choosing the next solar farm", level=1)
    d.add_paragraph("Development team, October 2026. For the investment committee's December meeting.")
    d.add_heading("1. The decision", level=2)
    d.add_paragraph("We will build one of the four consented candidate sites in 2027, each at %.1f MWp on the same "
                    "fixed-tilt layout and bifacial 410 W modules as Knowle Park, with an export limit above the "
                    "array's output. The planned inverter blocks for each candidate are in the array layout file with "
                    "the fleet's own blocks." % P.BUILD_MWP)
    d.add_heading("2. What the committee is asked to approve", level=2)
    d.add_paragraph("The site we build is the one that exports the most energy in its first full year of operation "
                    "(2028) in a year of average weather, taken as the 2016 to 2025 record in the site weather file, on "
                    "the fleet's own measured performance. Knowle Park is the only farm yet built to this design.")
    d.add_heading("3. The candidates", level=2)
    t = d.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    for j, h in enumerate(["Site", "Local authority", "Capacity (MWp)", "Grid offer energised by"]):
        t.rows[0].cells[j].text = h
    for nm, la, en in [("Hallam Down", "Maldon", "30 September 2027"), ("Kingsley Fields", "Test Valley", "31 August 2027"),
                       ("Larkhill Common", "Wiltshire", "29 October 2027"), ("Marston Vale", "Mendip", "30 July 2027")]:
        r = t.add_row().cells
        for j, v in enumerate([nm, la, "%.1f" % P.BUILD_MWP, en]):
            r[j].text = v
    d.add_heading("4. The records in the folder", level=2)
    for line in ["%s: each farm's daily export at its fiscal meter since 1 January 2022." % P.FILES["export"],
                 "%s: each inverter block's daily AC energy from the fleet SCADA since 1 January 2022." % P.FILES["scada"],
                 "%s: the weather provider's daily record for every farm and candidate, 2016 to 2025: irradiation in "
                 "the plane of a 25 degree south-facing array from satellite, rain, air temperature and wind direction "
                 "from reanalysis." % P.FILES["weather"],
                 "%s: the fleet and the candidates, with each site's capacity, modules and centroid on the national grid."
                 % P.FILES["register"],
                 "%s: every inverter block, built or planned, at its position on the national grid." % P.FILES["layout"],
                 "%s: the planning team's listing of features within 2 km of each site, from the landscape and "
                 "receptor surveys, measured from the site centroid." % P.FILES["environs"],
                 "%s: the O&M contractor's log of outages, farm-wide or at one inverter, with the share of the day's "
                 "output the farm or the inverter kept." % P.FILES["omlog"],
                 "%s and %s: the candidates' lease and grid terms, and the module datasheets." % (P.FILES["terms"],
                                                                                                  P.FILES["datasheets"]),
                 "%s, %s and %s: the met stations' pyranometer records for 2025, the pyranometer register at 31 "
                 "December 2025 and the laboratory's calibration certificates." % (P.FILES["met"], P.FILES["pyrreg"],
                                                                                    P.FILES["certs"]),
                 "%s, %s, %s and %s: the 2025 inverter alarms from the SCADA (a warning, W code, clears itself; a "
                 "fault, F code, stays raised until the inverter is reset on site), the O&M contractor's work orders, "
                 "the contractor's van tracker visits and its vans' technicians." % (P.FILES["alarms"],
                                                                                    P.FILES["workorders"],
                                                                                    P.FILES["geofence"], P.FILES["vans"])]:
        d.add_paragraph(line, style="List Bullet")
    d.core_properties.author = "Valerie Freeman"
    d.core_properties.title = "2027 build: choosing the next solar farm"
    d.save(path)
    postprocess.scrub(path, P.ORG, "2026-10-29")
    postprocess.finish_office(path, "2026-10-12T09:18:00Z", "2026-10-29T16:42:00Z", P.ADVISER, person="Valerie Freeman")


def terms(path):
    rows = [["Hallam Down", "Maldon", 17.8, "Hallam Farms Ltd", 1050, "Consented 14 May 2026", 10.0, 1480, "2027-09-30"],
            ["Kingsley Fields", "Test Valley", 18.4, "Kingsley Estate", 1000, "Consented 2 Mar 2026", 10.0, 1210, "2027-08-31"],
            ["Larkhill Common", "Wiltshire", 19.1, "M. and J. Prothero", 900, "Consented 21 Jan 2026", 10.0, 1655, "2027-10-29"],
            ["Marston Vale", "Mendip", 18.0, "Marston Vale Farms", 950, "Consented 9 Jul 2026", 10.0, 980, "2027-07-30"]]
    _xlsx(path, [("Candidates", ["Site", "Local authority", "Lease area (ha)", "Landowner",
                                 "Rent (GBP per ha per year)", "Planning", "Grid offer (MW export)",
                                 "Connection cost (GBP k)", "Energisation date"],
                  rows, [18, 16, 14, 22, 16, 22, 14, 16, 16], None)],
          "2026-07-14T10:05:00Z", "2026-10-20T15:31:00Z", "Terence Coates")


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.0, leading=12.4, spaceAfter=4)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.6, leading=16, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.0, leading=13,
                        spaceBefore=8, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=7.8, leading=10.2, textColor=colors.HexColor("#444444"))
    return body, h1, h2, small


def _table(rows, widths, size=8.2):
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size + 2.2)
    head = ParagraphStyle("head", parent=cell, fontName="Helvetica-Bold")
    rows = [[Paragraph(str(v), head if r == 0 else cell) for v in row] for r, row in enumerate(rows)]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9A9A9A")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6ECEF")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def datasheets(path):
    body, h1, h2, small = _styles()
    spec = [("Polycrystalline 250 W (2012-14 supply)", "60 cells, 156 mm multicrystalline", "250", "15.4", "-0.45",
             "-0.32", "45", "monofacial"),
            ("Monocrystalline PERC 320 W", "60 cells, 158.75 mm PERC", "320", "19.2", "-0.40", "-0.29", "44",
             "monofacial"),
            ("Monocrystalline PERC 410 W bifacial", "108 half-cells, 182 mm PERC, glass-glass", "410", "21.0", "-0.34",
             "-0.26", "43", "70 +/- 5 per cent")]
    rows = [["Module", "Cells", "Pmax at STC (W)", "Efficiency (%)", "Temp. coeff. Pmax (%/C)",
             "Temp. coeff. Voc (%/C)", "NOCT (C)", "Bifaciality"]] + [list(s) for s in spec]
    s = [Paragraph(P.ORG + " | Asset management", small), Spacer(1, 2 * mm),
         Paragraph("Module datasheets for the fleet", h1),
         Paragraph("The manufacturers' figures for the three module types in the fleet, as supplied at purchase. "
                   "Standard test conditions: 1,000 W/m2, 25 C cell, AM 1.5.", small),
         _table(rows, [44, 30, 16, 15, 18, 18, 12, 18], size=7.6),
         Spacer(1, 3 * mm),
         Paragraph("Warranted output", h2),
         Paragraph("Polycrystalline 250 W: 97 per cent in year one, then 0.7 per cent a year to 80.2 per cent at year "
                   "25. Monocrystalline PERC 320 W: 97.5 per cent in year one, then 0.6 per cent a year. "
                   "Monocrystalline PERC 410 W bifacial: 98 per cent in year one, then 0.45 per cent a year to 87.2 per "
                   "cent at year 25.", body)]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="Module datasheets for the fleet", author=P.ORG, creator=P.ORG,
                            subject="Module datasheets", invariant=1)
    doc.build(s)
    postprocess.scrub(path, P.ORG, "2025-11-03")


def certificates(path, certs):
    rows = [[c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7]] for c in certs]
    notes = [["Met-station pyranometer calibrations, entered from the laboratories' certificates."],
             ["A certificate's sensitivity applies to the sensor from its calibration date until its next certificate."],
             ["Sent from is the mast the sensor was taken down from for calibration, or Stores for a sensor sent from stock."]]
    _xlsx(path, [("Certificates", ["certificate_no", "serial", "model", "calibration_date",
                                   "sensitivity_uv_per_w_m2", "expanded_uncertainty_pct", "laboratory", "sent_from"],
                  rows, [16, 15, 9, 14, 20, 20, 32, 18], {"calibration_date": "yyyy-mm-dd"}),
                 ("Notes", None, notes, [110], None)],
          "2023-02-06T11:20:00Z", "2026-01-15T09:02:00Z", "Clive Barber")


def write(W, F):
    note(F["note"])
    terms(F["terms"])
    datasheets(F["datasheets"])
