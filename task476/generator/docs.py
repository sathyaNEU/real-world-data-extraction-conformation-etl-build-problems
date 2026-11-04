"""The pack's documents: the station register (XLSX), the consultant's 2023 Rating 7 memo, the license articles, the
2024 flow monitoring plan and the 2025 compliance report (PDF). Each is written in its issuer's own form."""
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                    # noqa: E402
from reportlab.lib.pagesizes import letter                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                     # noqa: E402
from reportlab.lib.units import inch                                # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402
from openpyxl import Workbook                                       # noqa: E402
from openpyxl.styles import Font                                    # noqa: E402

import world as W   # noqa: E402

BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=6)
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8.2, leading=10.4, spaceAfter=3)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5, leading=13.5, spaceBefore=8, spaceAfter=3)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=3)
SUB = ParagraphStyle("u", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#444444"), spaceAfter=10)


def _doc(path, title, owner, footer):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.8 * inch, title=title, author=owner, creator=owner, producer=owner, subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 7.4)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.9 * inch, 0.5 * inch, footer)
        c.drawRightString(letter[0] - 0.9 * inch, 0.5 * inch, "%d" % d_.page)
        c.restoreState()
    return d, frame


def _table(rows, widths, font=8.4):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", font), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", font),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6), ("TOPPADDING", (0, 0), (-1, -1), 1.6)]))
    return t


def table_q(h):
    """Rating 7's expanded table entry, as the register prints it (two decimals)."""
    return round(W.R7_C * (h - W.R7_E) ** W.R7_B, 2)


def write_register(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Station"
    rows = [("Station", "BP-1, Tallis Creek below diversion dam"), ("Owner", W.COMPANY),
            ("Operated by", "%s under contract" % W.CONSULTANT),
            ("Location", "Right bank, 300 ft downstream of the diversion dam spillway"),
            ("Gage datum", "1,184.62 ft NAVD88 (levels run 2024-08-14)"),
            ("Primary gage", "Vented pressure transducer, orifice at 1.12 ft gage height; 10-minute record"),
            ("Logger clock", "Pacific Standard Time (UTC-08:00) all year"),
            ("Reference gage", "Enamelled staff plate, 0.00 to 8.00 ft"),
            ("Control", "Gravel and cobble riffle 45 ft downstream of the orifice; channel control above about 4 ft"),
            ("Rating in use", "Rating 7, effective 2023-10-12"),
            ("Expanded table range", "1.00 to 4.00 ft"),
            ("Measurement section", "Wading section 60 ft upstream of the riffle; cableway for high water")]
    for r in rows:
        ws.append(list(r))
    ws["A1"].font = Font(bold=True)
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 78
    t = wb.create_sheet("Rating 7")
    t.append(["Gage height (ft)", "Discharge (cfs)"])
    for c in t[1]:
        c.font = Font(bold=True)
    n = int(round((W.TABLE_HI - W.TABLE_LO) * 100))
    for i in range(n + 1):
        h = round(W.TABLE_LO + i / 100.0, 2)
        t.append([h, table_q(h)])
    t.column_dimensions["A"].width = 16
    t.column_dimensions["B"].width = 16
    t.freeze_panes = "A2"
    hst = wb.create_sheet("Rating history")
    hst.append(["Rating", "Effective", "Range (ft)", "Developed from", "Remark"])
    for c in hst[1]:
        c.font = Font(bold=True)
    hst.append([5, "2017-06-02", "1.10-3.80", "11 measurements 2015-2017", "superseded"])
    hst.append([6, "2020-11-19", "1.00-3.90", "14 measurements 2018-2020", "superseded after the 2020 channel work"])
    hst.append([7, "2023-10-12", "1.00-4.00 table; equations to 7.5", "17 measurements 2021-2023", "in use"])
    for col, wd in zip("ABCDE", (8, 12, 26, 28, 40)):
        hst.column_dimensions[col].width = wd
    wb.save(path)


R7_MEAS = [("2021-05-18", 3.92, 0.004), ("2021-08-24", 2.19, -0.021), ("2021-10-07", 1.95, 0.017),
           ("2021-12-02", 2.74, -0.012), ("2022-03-29", 4.62, 0.026), ("2022-05-26", 5.48, -0.018),
           ("2022-07-20", 2.31, 0.009), ("2022-09-13", 2.27, -0.006), ("2022-11-30", 3.05, 0.031),
           ("2022-12-15", 7.36, -0.024), ("2023-01-12", 6.21, 0.013), ("2023-04-19", 4.18, -0.034),
           ("2023-06-06", 3.41, 0.015), ("2023-07-25", 2.29, 0.022), ("2023-08-29", 2.26, -0.011),
           ("2023-09-19", 2.02, 0.006), ("2023-10-03", 1.97, -0.015)]


def _sig3(v):
    from math import floor, log10
    p = 2 - int(floor(log10(abs(v))))
    return round(v, p) if p > 0 else int(round(v, p))


def write_rating_report(path):
    d, frame = _doc(path, "BP-1 Rating 7", W.CONSULTANT, "%s. BP-1 Rating 7 memorandum, October 2023" % W.CONSULTANT)
    top = W.R7_C * (W.R7_TOP - W.R7_E) ** W.R7_B
    meas = [["Date", "Gage height (ft)", "Measured (cfs)", "Rating 7 (cfs)", "Difference (%)"]]
    for date, gh, e in sorted(R7_MEAS):
        r = W.q_rating7(gh)
        q = _sig3(r * (1 + e))
        meas.append([date, "%.2f" % gh, "%g" % q, "%.1f" % r, "%+.1f" % (100 * (q / r - 1))])
    story = [Paragraph(W.CONSULTANT, TITLE),
             Paragraph("Memorandum to %s. Gauge BP-1, Tallis Creek below diversion dam: Rating 7. October 12, 2023."
                       % W.COMPANY, SUB),
             Paragraph("Summary", HEAD),
             Paragraph("Rating 7 replaces Rating 6 from October 12, 2023. It is fitted to the 17 discharge measurements made "
                       "at the station from May 2021 through October 2023, which span 1.95 to 7.36 ft. Low and medium flows "
                       "are controlled by the gravel and cobble riffle below the orifice; above about 4 ft the riffle drowns "
                       "and the channel controls.", BODY),
             Paragraph("Rating equations", HEAD),
             Paragraph("Low-water segment, 1.00 to 4.00 ft: Q = 22.0 (GH - 0.80)^2.30", BODY),
             Paragraph("High-water segment, above 4.00 ft: Q = %.1f + 260 (GH - 4.00)^1.60, continuous with "
                       "the low-water segment at 4.00 ft. The segment is defined by the cableway measurements of March 2022, "
                       "May 2022, December 2022, January 2023 and April 2023." % top, BODY),
             Paragraph("The expanded table in the station register lists the low-water segment at 0.01 ft from 1.00 to "
                       "4.00 ft.", BODY),
             Paragraph("Measurements", HEAD),
             _table(meas, [1.1 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch]),
             Paragraph("All 17 measurements plot within 5 per cent of Rating 7.", BODY)]
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def write_license(path):
    d, frame = _doc(path, "License Articles 403 and 404", W.COMPANY, "%s, license articles (excerpt)" % W.PROJECT)
    story = [Paragraph(W.PROJECT, TITLE), Paragraph("Order issuing new license, excerpt: Articles 403 and 404", SUB),
             Paragraph("Article 403. Minimum flow in the bypassed reach.", HEAD),
             Paragraph("The licensee shall maintain in the bypassed reach of Tallis Creek a minimum flow of 50 cubic feet "
                       "per second (cfs) from July 1 through September 30 and 30 cfs from October 1 through June 30. "
                       "Compliance is determined on the daily mean flow in the bypassed reach for each calendar day, local "
                       "time. A day whose mean flow is below the minimum for that day is a deviation. The licensee shall "
                       "report each deviation to the Commission, with its cause and the corrective action taken.", BODY),
             Paragraph("Article 404. Spring migration flows.", HEAD),
             Paragraph("From May 1 through June 30 the licensee shall pass at least 20,000 acre-feet through the bypassed "
                       "reach, and shall report the volume passed in each month and the peak flow of the period, with its date and "
                       "time, in its annual flow report.", BODY),
             Paragraph("Article 405. Flow monitoring.", HEAD),
             Paragraph("Within six months of license issuance the licensee shall file for approval a plan to monitor flows "
                       "in the bypassed reach, and shall operate the gauges the approved plan describes.", BODY)]
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def write_plan(path):
    d, frame = _doc(path, "Bypassed Reach Flow Monitoring Plan", W.COMPANY, "%s. Flow monitoring plan, revision 2024"
                    % W.PROJECT)
    story = [Paragraph("Bypassed Reach Flow Monitoring Plan", TITLE),
             Paragraph("%s. Revision 2, approved March 2024 under Article 405." % W.PROJECT, SUB),
             Paragraph("1. Gauge", HEAD),
             Paragraph("Flow in the bypassed reach is monitored at gauge BP-1, 300 feet downstream of the diversion dam "
                       "spillway, upstream of any tributary inflow. A vented pressure transducer records stage every 10 "
                       "minutes; an enamelled staff plate is the reference gauge.", BODY),
             Paragraph("2. Record computation", HEAD),
             Paragraph("Discharge is computed from the stage record by the standard methods of the U.S. Geological Survey "
                       "for stage-discharge stations. The licensee's hydrographer visits the gauge at least every six "
                       "weeks from May through October and after high flows, reads the reference gauge and measures "
                       "discharge.", BODY),
             Paragraph("3. Operations", HEAD),
             Paragraph("The bypass release gate is controlled from the plant to a flow setpoint read at BP-1. The setpoint "
                       "is held above the Article 403 minimum by an operating margin.", BODY),
             Paragraph("4. Reporting", HEAD),
             Paragraph("The licensee reports deviations under Article 403 and the monthly spring volumes under Article 404 "
                       "in its annual flow report, filed by January 31 of the following year, or sooner where Article 403 "
                       "requires.", BODY)]
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def write_prior(path):
    d, frame = _doc(path, "2025 Annual Flow Compliance Report", W.COMPANY, "%s. 2025 annual flow report" % W.PROJECT)
    story = [Paragraph(W.COMPANY, TITLE), Paragraph("2025 Annual Flow Compliance Report, filed January 22, 2026", SUB),
             Paragraph("Article 403", HEAD),
             Paragraph("The bypassed reach met its minimum flow on every day of 2025. The lowest daily mean flows were "
                       "53.6 cfs (July through September) and 33.4 cfs (October through June), both computed at BP-1 on "
                       "Rating 7.", BODY),
             Paragraph("Article 404", HEAD),
             Paragraph("The bypassed reach passed 17,640 acre-feet in May and 9,870 acre-feet in June 2025, 27,510 acre-feet "
                       "in all.", BODY),
             Paragraph("Marissa Harmon, Environmental Manager", BODY)]
    d.build(story, onFirstPage=frame, onLaterPages=frame)
