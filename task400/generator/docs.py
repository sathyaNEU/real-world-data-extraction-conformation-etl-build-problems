"""The pack's documents and workbooks: the review's terms, the inspectorate's notice, the collision avoidance
vendor's monthly report, the device register and the incident register."""
import datetime as dt
import os

import postprocess as PP

COMPANY = "Ternhallow Iron Ore Pty Ltd"
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _pdf(path, title, author, blocks, created, modified, producer="Microsoft\xae Word for Microsoft 365"):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    st = ParagraphStyle("b", fontName="Helvetica", fontSize=9.4, leading=13, spaceAfter=5)
    h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=16.5, spaceAfter=8)
    h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.2, leading=13.5, spaceBefore=6, spaceAfter=4)
    sm = ParagraphStyle("s", fontName="Helvetica", fontSize=7.8, leading=10, textColor=colors.HexColor("#444444"))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, subject="", creator="")
    flow = []
    for kind, val in blocks:
        if kind == "h1":
            flow.append(Paragraph(val, h1))
        elif kind == "h2":
            flow.append(Paragraph(val, h2))
        elif kind == "p":
            flow.append(Paragraph(val, st))
        elif kind == "small":
            flow.append(Paragraph(val, sm))
        elif kind == "sp":
            flow.append(Spacer(1, val))
        elif kind == "table":
            t = Table(val, hAlign="LEFT")
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 7.8),
                                   ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 7.8),
                                   ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9a9a9a")),
                                   ("ALIGN", (1, 1), (-1, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            flow.append(t)

    def _meta(c, d):
        c.setProducer(producer)
        c.setCreator(producer)
    doc.build(flow, onFirstPage=_meta, onLaterPages=_meta)
    PP.normalize_pdf(path, created, modified)


TERMS = [
    ("title", "Mount Bracken vehicle interaction review 2026: terms of reference"),
    ("small", "Ternhallow Iron Ore Pty Ltd, Mount Bracken Mine. Document HSE-TOR-026, version 1.1. Owner: Health and Safety "
              "Superintendent. Approved by the General Manager, 22 September 2026. Supersedes version 1.0 of 9 September 2026."),
    ("h", "1. Purpose"),
    ("p", "Improvement notice IN-2026-0417, issued to the mine by the Mines Safety Inspectorate on 2 September 2026, requires "
          "the mine to identify the cause of the increase in vehicle interaction incidents and to put in place a control that "
          "addresses it. This review is the basis on which the site safety steering committee chooses the one vehicle "
          "interaction programme it funds for 2027."),
    ("h", "2. Definitions"),
    ("p", "2.1 A vehicle interaction incident is a collision between two vehicles, or a significant potential incident "
          "between two vehicles, entered in the site incident register under classification VI-COL or VI-SPI. Each register "
          "entry is one incident, counted in the month in which it occurred, Western Australian time."),
    ("p", "2.2 A haul truck is one of the mine's rear dump trucks carrying a DT fleet number. A light vehicle is any vehicle "
          "on the light vehicle register."),
    ("h", "3. What the review compares"),
    ("p", "3.1 The review explains the rise in vehicle interaction incidents in July to October 2026 against July to October 2025."),
    ("p", "3.2 The review names the driver that accounts for most of that rise, and the committee funds the programme in "
          "section 4 that answers that driver."),
    ("h", "4. The programmes before the committee"),
    ("p", "A. Operator vigilance refresher for all haul truck operators. Answers a fall in haul truck operators' attention to "
          "other vehicles across the site."),
    ("p", "B. Separated light vehicle access at the North ramp junction. Answers light vehicles and haul trucks crossing at the "
          "junction."),
    ("p", "C. Collision avoidance alerting review on the haul truck units. Answers the alerts the haul trucks' collision "
          "avoidance units give their operators."),
    ("p", "D. Night shift fatigue monitoring. Answers haul truck operator fatigue on night shift."),
    ("p", "E. ROM crusher pad traffic management. Answers congestion and queuing at the crusher pad."),
    ("h", "5. Timing"),
    ("p", "The review paper goes to the committee meeting of 19 November 2026. The chosen programme's implementation plan goes "
          "to the inspectorate by 31 December 2026."),
]


def terms_docx(out):
    import docx
    from docx.shared import Pt
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for kind, text in TERMS:
        if kind == "title":
            doc.add_heading(text, level=1)
        elif kind == "h":
            doc.add_heading(text, level=2)
        elif kind == "small":
            p = doc.add_paragraph(text)
            for run in p.runs:
                run.font.size = Pt(8.5)
        else:
            doc.add_paragraph(text)
    p = os.path.join(out, "vi_review_terms_2026.docx")
    doc.save(p)
    PP.normalize_ooxml(p, "Shari Jefferson", "Shari Jefferson", "2026-09-04T01:20:00Z", "2026-09-22T06:05:00Z",
                       title="Vehicle interaction review 2026: terms of reference", company=COMPANY)
    PP.scrub_docx(p, total_time=63, title="Vehicle interaction review 2026: terms of reference", company=COMPANY)


def notice_pdf(out, col_when):
    blocks = [
        ("small", "Mines Safety Inspectorate  |  Improvement notice under the mine safety legislation  |  IN-2026-0417"),
        ("h1", "Improvement notice IN-2026-0417"),
        ("table", [["Issued to", "Ternhallow Iron Ore Pty Ltd, operator of the Mount Bracken Mine"],
                   ["Place", "Mount Bracken Mine, open pits, haul roads and ROM pad"],
                   ["Date of issue", "2 September 2026"],
                   ["Inspector", "Nancy Franco, Inspector of Mines"],
                   ["Compliance date", "31 December 2026"]]),
        ("sp", 8),
        ("h2", "Grounds"),
        ("p", "I believe that the operator is contravening, and is likely to continue to contravene, its duty to provide and "
              "maintain a working environment in which workers are not exposed to hazards, as regards interactions between "
              "mobile plant and light vehicles. The mine's register shows vehicle interaction incidents rising through July and "
              "August 2026, including a collision on %s between a haul truck and another vehicle at the North ramp "
              "junction." % ("%d %s %d" % (col_when.day, col_when.strftime("%B"), col_when.year))),
        ("h2", "Required"),
        ("p", "1. Identify the cause of the increase in vehicle interaction incidents at the mine."),
        ("p", "2. Implement a control that addresses that cause, and give the inspectorate the investigation and the control's "
              "implementation plan by the compliance date."),
        ("sp", 6),
        ("small", "A person who does not comply with an improvement notice commits an offence. This notice does not prevent the "
                  "inspectorate taking other action."),
    ]
    _pdf(os.path.join(out, "improvement_notice_IN-2026-0417.pdf"), "Improvement notice IN-2026-0417", "Mines Safety Inspectorate",
         blocks, b"D:20260902143112+08'00'", b"D:20260902143112+08'00'", producer="Inspectorate Notices 4.2")


def vendor_report_pdf(out, monthly, fw_line):
    head = ["Month", "Units reporting", "Operating hours", "Warning alerts", "Critical alerts", "Alerts per 100 h",
            "Acknowledged"]
    rows = [head]
    for m in monthly:
        rows.append([m["label"], str(m["units"]), "{:,.0f}".format(m["hours"]), "{:,}".format(m["warn"]),
                     "{:,}".format(m["crit"]), "%.1f" % m["per100"], "%.1f%%" % m["ack"]])
    blocks = [
        ("small", "Halcyon Proximity Systems  |  Site services  |  Report MB-2026-10  |  Prepared by Ana Cuevas, site support engineer"),
        ("h1", "Mount Bracken: monthly fleet performance report, October 2026"),
        ("p", "Alert volumes and acknowledgement by month for the collision avoidance units on Mount Bracken haul trucks, "
              "January 2025 to October 2026. Operating hours are the dispatch system's haul truck operating hours for the month."),
        ("table", rows),
        ("sp", 6),
        ("h2", "Fleet status"),
        ("p", fw_line),
        ("p", "Units reporting counts haul truck units that sent at least one heartbeat in the month. Alerts are counted at onset."),
    ]
    _pdf(os.path.join(out, "cas_monthly_report_2026-10.pdf"), "Mount Bracken monthly fleet performance report October 2026",
         "Halcyon Proximity Systems", blocks, b"D:20261102091544+08'00'", b"D:20261102091544+08'00'",
         producer="Halcyon Reports 3.8")


def device_register_xlsx(out, dev, fw):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Devices"
    ws.append(["Serial", "Device type", "Asset", "Installed", "Removed"])
    for s, kind, asset, a, b in dev:
        ws.append([s, kind, asset, a, b])
        ws.cell(row=ws.max_row, column=4).number_format = "yyyy-mm-dd"
        if b is not None:
            ws.cell(row=ws.max_row, column=5).number_format = "yyyy-mm-dd"
    for col, w in zip("ABCDE", (13, 17, 12, 12, 12)):
        ws.column_dimensions[col].width = w
    ws2 = wb.create_sheet("Firmware")
    ws2.append(["Serial", "Version", "Applied (UTC)"])
    for s, v, t in fw:
        ws2.append([s, v, t])
        ws2.cell(row=ws2.max_row, column=3).number_format = "yyyy-mm-dd hh:mm"
    for col, w in zip("ABC", (13, 10, 18)):
        ws2.column_dimensions[col].width = w
    p = os.path.join(out, "cas_device_register_2026-10-31.xlsx")
    wb.save(p)
    PP.normalize_ooxml(p, "Halcyon Portal", "Halcyon Portal", "2026-10-31T23:58:00Z", "2026-10-31T23:58:00Z", excel=True,
                       company="Halcyon Proximity Systems")


def incident_register_xlsx(out, rows):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Register"
    ws.append(["Incident no.", "Occurred", "Location code", "Location", "Classification", "Potential", "Employer",
               "Vehicles", "Description"])
    for r in rows:
        ws.append([None if v == "" else v for v in r])
        ws.cell(row=ws.max_row, column=2).number_format = "dd/mm/yyyy hh:mm"
    for col, w in zip("ABCDEFGHI", (14, 16, 9, 30, 12, 10, 22, 22, 90)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    p = os.path.join(out, "incident_register_2025-01_2026-10.xlsx")
    wb.save(p)
    PP.normalize_ooxml(p, "Shari Jefferson", "Shari Jefferson", "2026-11-01T22:40:00Z", "2026-11-01T22:44:00Z", excel=True,
                       company=COMPANY)
