"""task482 architecture 16: the pack's documents. Velden's SCR-2, the gas supplier's invoices, the cover email
and the workbook writer. PDFs carry their issue dates and wrap every table cell inside the page."""
import datetime as dt
import os
from email.message import EmailMessage
from email.utils import format_datetime

import openpyxl
import reportlab.rl_config
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import postprocess as PP

reportlab.rl_config.invariant = 1
SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["Normal"], fontName="Helvetica", fontSize=9.2, leading=12.4, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=13.5,
                    spaceBefore=6, spaceAfter=3)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=7.8, leading=10, textColor=colors.HexColor("#444444"))
CELL = ParagraphStyle("c", parent=BODY, fontSize=8.0, leading=10.0, spaceAfter=0)
CELLB = ParagraphStyle("cb", parent=CELL, fontName="Helvetica-Bold")


def _esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _table(rows, widths, right=()):
    data = [[Paragraph(_esc(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#333333")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5), ("TOPPADDING", (0, 0), (-1, -1), 2.0)]
    t.setStyle(TableStyle(st))
    return t


def _pdf(path, title, author, story, footer, subject=""):
    def page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, footer)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=17 * mm,
                            bottomMargin=17 * mm, title=title, author=author, subject=subject,
                            creator="ReportLab PDF Library - www.reportlab.com")
    doc.build(story, onFirstPage=page, onLaterPages=page)


def _pdfdate(d, tz="+00'00'"):
    return ("D:%s%s" % (d.strftime("%Y%m%d%H%M%S"), tz)).encode()


def scr2_pdf(path):
    s = [Paragraph("Supplier Carbon Requirement SCR-2: product carbon intensity of aluminium supplies", H1),
         Paragraph("%s, Purchasing, light metals. Revision 2, effective 1 January 2026; supersedes Revision 1 of "
                   "March 2025." % P.BUYER, SMALL), Spacer(1, 4),
         Paragraph("1. Scope", H2),
         Paragraph("This requirement applies to every works that supplies aluminium semi-finished goods or castings to "
                   "Velden. A supplier reports each product family it supplies to Velden, as listed in its supply "
                   "agreement, for each calendar year.", BODY),
         Paragraph("2. Specific direct emissions", H2),
         Paragraph("A product family's specific direct emissions for a year are the carbon dioxide from the fuel the "
                   "works burned to make that family in the year, in tonnes, divided by the tonnes of the family the "
                   "works produced in the year.", BODY),
         Paragraph("3. Attribution", H2),
         Paragraph("Each production process is attributed the fuel it burned, and a product family carries the fuel "
                   "each process burned on that family's metal. Fuel that heats the works' buildings, and fuel that "
                   "pilot flames burn whether or not a process is running, belongs to no process; it is shared over "
                   "the product families in proportion to the tonnes of each produced.", BODY),
         Paragraph("4. Fuel and emission factor", H2),
         Paragraph("Natural gas is taken at the energy the gas supplier billed it at, on gross calorific value, and "
                   "its carbon dioxide at 0.18296 kilograms per kilowatt-hour.", BODY),
         Paragraph("5. Production", H2),
         Paragraph("A family's production is the tonnes of it that passed the works' final inspection in the year. A "
                   "lot inspected more than once counts at its last result.", BODY),
         Paragraph("6. Periods", H2),
         Paragraph("Years, quarters, months and days are those of the works' local time.", BODY),
         Paragraph("7. Low-carbon premium", H2),
         Paragraph("For each contract year Velden pays a premium of EUR 38 per tonne of its call-offs of each product "
                   "family whose specific direct emissions for the year before were 0.235 tonnes of carbon dioxide per "
                   "tonne or less.", BODY),
         Paragraph("8. The supplier's data package", H2),
         Paragraph("By 31 January the supplier sends its fuel meters' interval records, its fuel invoices, its process "
                   "logs and its production records for the year, with its energy records and the waste and scrap "
                   "records Velden's supplier reporting asks for.", BODY),
         Spacer(1, 6), Paragraph("Issued by Velden Purchasing, light metals. Approved: Head of Sustainable Sourcing.",
                                 SMALL)]
    _pdf(path, "SCR-2 Product carbon intensity", "Velden Automobil AG", s, "Velden SCR-2 Revision 2  |  public to "
         "suppliers",
         subject="Supplier carbon requirement SCR-2, Revision 2")
    PP.normalize_pdf(path, _pdfdate(dt.datetime(2025, 11, 20, 9, 12, 0), "+01'00'"),
                     _pdfdate(dt.datetime(2025, 12, 8, 14, 3, 0), "+01'00'"))


def invoices_pdf(path, invoices):
    s = []
    for k, inv in enumerate(invoices):
        if k:
            s.append(PageBreak())
        s += [Paragraph("Northgate Gas Supply Ltd: VAT invoice %s" % inv["no"], H1),
              Paragraph("Customer: %s. Supply point MPRN 8804419362. Account 30-77152. Issued %s." % (
                  P.WORKS, inv["issued"].strftime("%d %B %Y")), SMALL), Spacer(1, 3)]
        rows = [["Meter", "Read from", "Read to", "Opening read", "Closing read", "Units", "Volume (m3)"]]
        for m in inv["meters"]:
            rows.append([m["serial"], m["from"].strftime("%d/%m/%Y %H:%M"), m["to"].strftime("%d/%m/%Y %H:%M"),
                         "%.0f" % m["open"], "%.0f" % m["close"], m["units"], "%.2f" % m["m3"]])
        s.append(_table(rows, [25, 30, 30, 21, 21, 13, 24]))
        s.append(Spacer(1, 4))
        rows = [["Energy", "Value"],
                ["Volume (m3)", "%.2f" % inv["m3"]],
                ["Volume correction factor", "%.5f" % P.VCF],
                ["Calorific value (MJ/m3)", "%.2f" % inv["cv"]],
                ["Energy (kWh), volume x correction factor x calorific value / 3.6", "{:,.0f}".format(inv["kwh"])],
                ["Unit rate (p/kWh)", "%.3f" % inv["rate"]],
                ["Gas charge (GBP)", "{:,.2f}".format(inv["charge"])],
                ["Standing charge, %d days (GBP)" % inv["days"], "{:,.2f}".format(inv["standing"])],
                ["Climate Change Levy (GBP)", "{:,.2f}".format(inv["ccl"])],
                ["VAT at 20 per cent (GBP)", "{:,.2f}".format(inv["vat"])],
                ["Total (GBP)", "{:,.2f}".format(inv["total"])]]
        s.append(_table(rows, [100, 50]))
        if inv.get("note"):
            s += [Spacer(1, 3), Paragraph(inv["note"], SMALL)]
    _pdf(path, "Gas invoices 2026", "Northgate Gas Supply Ltd", s, "Northgate Gas Supply Ltd  |  MPRN 8804419362",
         subject="VAT invoices, Brackwell Alloys Ltd, MPRN 8804419362, 2026")
    PP.normalize_pdf(path, _pdfdate(dt.datetime(2027, 1, 12, 10, 40, 0)), _pdfdate(dt.datetime(2027, 1, 12, 10, 40, 0)))


def email(path, files):
    m = EmailMessage()
    m["From"] = "%s <r.kent@brackwell-alloys.co.uk>" % P.PEOPLE["energy"]
    m["To"] = "%s <tony.coleman@velden-auto.de>" % P.PEOPLE["buyer"]
    m["Subject"] = "Brackwell Alloys: SCR-2 data package for 2026"
    m["Date"] = format_datetime(dt.datetime(2027, 1, 21, 16, 12, tzinfo=dt.timezone.utc))
    m["Message-ID"] = "<scr2-2026.brackwell.20270121161200@brackwell-alloys.co.uk>"
    body = ("Tony,\n\nAs SCR-2 asks, here is our 2026 data package for the four families we supply you. The gas "
            "meter export is the supplier's interval file for our one site meter, which was exchanged in April. The "
            "furnace, homogenizing and oven logs are the shift logs as kept, and the production file is the "
            "inspection system's export. The electricity, weighbridge and goods-in files are for your supplier "
            "reporting.\n\nFiles:\n" + "".join("  %s\n" % f for f in files) +
            "\nAny questions on the logs, Reece Parker in the works office can help.\n\nRegards,\n\n"
            "Rosemary Kent\nEnergy and Environment, Brackwell Alloys Ltd\n")
    m.set_content(body)
    with open(path, "wb") as f:
        f.write(bytes(m))


def workbook(path, sheets, owner, last_by, created, modified, company, widths=None, formats=None):
    """sheets: [(title, header, rows)]. Saved under the owner's name and stamps, in Excel's dialect."""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for title, header, rows in sheets:
        ws = wb.create_sheet(title)
        ws.append(header)
        for c in ws[1]:
            c.font = Font(bold=True)
        for r in rows:
            ws.append([None if x == "" else x for x in r])
        for col, fmt in ((formats or {}).get(title) or {}).items():
            for row in ws.iter_rows(min_row=2, min_col=col, max_col=col):
                for c in row:
                    c.number_format = fmt
        for i, w in enumerate((widths or {}).get(title, [16] * len(header))):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
        ws.freeze_panes = "A2"
    wb.save(path)
    PP.normalize_ooxml(path, owner, last_by, created, modified, excel=True, company=company)
