"""The pack's documents: the unit safety plan (the tolerance and its definitions), the summer 2026 safety close-out,
the operations manual's sector configuration chapter (edition of 26 March 2026), and the data office's extract
notes."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.pagesizes import A4                                     # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import mm                                         # noqa: E402
from reportlab.pdfbase import pdfmetrics                                   # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                               # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import configs as CF   # noqa: E402
import records as R    # noqa: E402
import world as W      # noqa: E402

PLAN_DOC = "HACC_unit_safety_plan_2026-2028.pdf"
CLOSEOUT = "HACC_summer2026_safety_closeout.pdf"
OM = "HACC_OM_part3_ch4_sector_configuration.pdf"
NOTES = "extract_notes_2026-10-12.md"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LiberationSans", FONT_DIR + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans-Bold", FONT_DIR + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSerif", FONT_DIR + "LiberationSerif-Regular.ttf"))
SANS, SANS_B, SERIF = "LiberationSans", "LiberationSans-Bold", "LiberationSerif"
INK = colors.HexColor("#14202b")
GREY = colors.HexColor("#5a6672")
RULE = colors.HexColor("#9aa5b1")
BODY = ParagraphStyle("body", fontName=SANS, fontSize=9.6, leading=13, textColor=INK, spaceAfter=5)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=26, firstLineIndent=-26)
H1 = ParagraphStyle("h1", fontName=SANS_B, fontSize=14.5, leading=18, textColor=INK, spaceAfter=3)
H2 = ParagraphStyle("h2", fontName=SANS_B, fontSize=10.4, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3)
META = ParagraphStyle("meta", fontName=SANS, fontSize=8, leading=10.5, textColor=GREY, spaceAfter=8)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=8.4, leading=10.2, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName=SANS_B)
pdfmetrics.registerFont(TTFont("LiberationSerif-Bold", FONT_DIR + "LiberationSerif-Bold.ttf"))
OPS_BODY = ParagraphStyle("opsbody", fontName=SERIF, fontSize=10.2, leading=13.6, textColor=INK, spaceAfter=5)
OPS_CLAUSE = ParagraphStyle("opsclause", parent=OPS_BODY, leftIndent=34, firstLineIndent=-34)
OPS_H1 = ParagraphStyle("opsh1", fontName="LiberationSerif-Bold", fontSize=15, leading=19, textColor=INK, spaceAfter=2)
OPS_H2 = ParagraphStyle("opsh2", fontName="LiberationSerif-Bold", fontSize=11, leading=14.5, textColor=INK,
                        spaceBefore=9, spaceAfter=3)
OPS_META = ParagraphStyle("opsmeta", fontName=SERIF, fontSize=8.6, leading=11, textColor=GREY, spaceAfter=9)


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(SANS, 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 12 * mm, left)
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "%s  |  Page %d" % (right, doc.page))
        canvas.restoreState()
    return draw


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")


def _grid(rows, widths, bold_last=False, align_from=1):
    data = [[Paragraph(str(c), CELLB if (i == 0 or (bold_last and i == len(rows) - 1)) else CELL) for c in r]
            for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, -1), (-1, -1), 0.5, RULE),
                           ("ALIGN", (align_from, 0), (-1, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]))
    return t


PLAN_CLAUSES = [
    ("1", "Purpose and scope", [
        ("1.1", "This plan sets the safety performance %s commits to for 2026 to 2028, the indicators the unit "
                "monitors, and how each summer's sector plan is checked before the Unit Safety Review Board approves "
                "it." % W.UNIT),
        ("1.2", "It applies to the eight elementary sectors of the Holmvik upper airspace (FL245 to FL660) listed in "
                "the sector register."),
    ]),
    ("2", "Indicators", [
        ("2.1", "The unit monitors the occurrences reported to the %s occurrence database and classified under the "
                "occurrence scheme AAN-OCC-01: separation minima infringements, ACAS resolution advisories, level busts, "
                "prolonged losses of communication, deviations from clearance, ATM technical occurrences, airspace "
                "infringements and wake turbulence encounters." % W.ANSP),
        ("2.2", "The indicator with a tolerance in this plan is the rate of ATM-related losses of separation. The other "
                "indicators are reviewed each quarter against their own trend."),
    ]),
    ("3", "Definitions", [
        ("3.1", "Elementary sector: one of the eight sectors in the sector register. A configuration that combines "
                "sectors on one controller position does not create a sector; occurrences and flight hours are counted "
                "for the elementary sector."),
        ("3.2", "Summer season: 1 June to 31 August inclusive, local time."),
        ("3.3", "Loss of separation: an occurrence classified SMI (separation minima infringement) under AAN-OCC-01."),
        ("3.4", "ATM-related: an occurrence whose ATM contribution is classified direct (D) or indirect (I)."),
        ("3.5", "Flight hours: the time from sector entry to sector exit, summed over every flight of the period. For a "
                "season still to come, the flights are those of the planning traffic that Network and Capacity Planning "
                "issues for that season."),
    ]),
    ("4", "Tolerance for the summer sector plan", [
        ("4.1", "For each elementary sector, the forecast rate of ATM-related losses of separation in the coming summer "
                "season shall not exceed 40.0 per 100,000 flight hours."),
        ("4.2", "The Safety Office prepares the forecast for every elementary sector from the unit's occurrence record "
                "since the present eight-sector structure came into use on 1 January 2025, and from the planning "
                "traffic, and presents it with the summer sector plan. A sector forecast above the tolerance is "
                "presented with the measures proposed (configuration, capacity or route changes)."),
        ("4.3", "The tolerance applies to each elementary sector and each season separately. It is not averaged across "
                "sectors or seasons."),
    ]),
    ("5", "Review cycle", [
        ("5.1", "The summer sector plan is presented to the Unit Safety Review Board in November of the year before; "
                "the plan for summer 2027 on 4 November 2026."),
        ("5.2", "Each summer is closed out in October against the same tolerance, on the season's recorded flight "
                "hours."),
    ]),
    ("6", "Responsibilities", [
        ("6.1", "The Head of Safety owns this plan, prepares the summer forecast and the close-out, and chairs the "
                "quarterly indicator review."),
        ("6.2", "The Head of Operations proposes and carries out configuration and staffing measures, and keeps the "
                "configuration tables of the Operations Manual Part 3."),
        ("6.3", "Network and Capacity Planning issues the planning traffic for the coming summer by 15 October, and the "
                "capacity plan with it."),
        ("6.4", "Data and Analytics supplies the FDPS, occurrence and network manager extracts the Safety Office "
                "asks for."),
    ]),
    ("7", "Occurrence reporting and investigation", [
        ("7.1", "All operational staff report occurrences under the just culture policy AAN-POL-07. Flight crew reports "
                "reach the unit through the operators and the national occurrence reporting system."),
        ("7.2", "The Safety Office classifies each report within ten working days (type, severity, ATM contribution) "
                "and closes the investigation of a loss of separation within 60 days."),
    ]),
]

INDICATORS = [
    ["Indicator", "Source", "Reviewed", "Owner"],
    ["Losses of separation (SMI), ATM-related", "occurrence database", "quarterly; forecast before each summer", "Safety Office"],
    ["ACAS resolution advisories", "crew and controller reports", "quarterly", "Safety Office"],
    ["Level busts", "occurrence database", "quarterly", "Operations"],
    ["Prolonged loss of communication", "occurrence database", "quarterly", "Operations"],
    ["ATM technical occurrences", "engineering reports", "monthly", "Engineering"],
    ["Airspace infringements", "occurrence database", "quarterly", "Operations"],
]
EDITIONS = [
    ["Edition", "Date", "Change"],
    ["1.0", "16 January 2023", "First issue (2023 to 2025)"],
    ["1.3", "4 March 2025", "Eight-sector structure from 1 January 2025; indicators reviewed quarterly"],
    ["2.0", "12 February 2026", "Plan extended to 2028; summer tolerance per elementary sector"],
]


def write_plan(path):
    doc = _doc(path, "Holmvik ACC Unit Safety Plan 2026 to 2028", W.PEOPLE["safety"])
    story = [Paragraph("Holmvik Area Control Centre: Unit Safety Plan 2026 to 2028", H1),
             Paragraph("HACC-SAF-PLN-03, edition 2.0, 12 February 2026. Owner: Head of Safety, Holmvik ACC (%s). "
                       "Approved by the Unit Safety Review Board on 10 February 2026. Supersedes edition 1.3."
                       % W.PEOPLE["safety"], META)]
    for no, head, clauses in PLAN_CLAUSES:
        story.append(Paragraph("%s&nbsp;&nbsp;%s" % (no, head), H2))
        for cno, text in clauses:
            story.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (cno, text), CLAUSE))
        if no == "2":
            story.append(Paragraph("Table 1&nbsp;&nbsp;Indicators and their review", META))
            story.append(_grid(INDICATORS, [58 * mm, 38 * mm, 46 * mm, 28 * mm], align_from=4))
            story.append(Spacer(1, 4))
    story.append(Paragraph("Edition history", H2))
    story.append(_grid(EDITIONS, [18 * mm, 32 * mm, 120 * mm], align_from=3))
    frame = _frame("%s  |  HACC-SAF-PLN-03 ed. 2.0" % W.ANSP, "Controlled copy, document library")
    doc.build(story, onFirstPage=frame, onLaterPages=frame)


def write_closeout(path, tab):
    """tab: {sector: dict(l25, l26, fh25, fh26)} (ATM-related losses and flight hours, summer 2025 and 2026), plus
    'sev' (B and C counts of the ATM-related losses, summer 2026) and 'non26' (losses with no ATM contribution)."""
    doc = _doc(path, "Summer 2026 safety performance close-out", W.PEOPLE["safety"])
    n26 = sum(tab[s]["l26"] for s in W.SECTORS)
    n25 = sum(tab[s]["l25"] for s in W.SECTORS)
    fh26 = sum(tab[s]["fh26"] for s in W.SECTORS)
    fh25 = sum(tab[s]["fh25"] for s in W.SECTORS)
    sev = tab["sev"]
    hal = (tab["HAL"]["fh26"] / tab["HAL"]["fh25"] - 1) * 100
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
    memo = _grid([["To", "Unit Safety Review Board"], ["From", "Safety Office (%s)" % W.PEOPLE["safety"]],
                  ["Date", "6 October 2026"], ["Reference", "HACC-SAF-RPT-2026-11"]], [26 * mm, 100 * mm], align_from=2)
    story = [Paragraph("Summer 2026 safety performance close-out, Holmvik ACC", H1), memo, Spacer(1, 6),
             Paragraph("Season 1 June to 31 August 2026, local time. Occurrence data as at 2 October 2026; flight hours "
                       "from the FDPS archive.", META),
             Paragraph("1&nbsp;&nbsp;Summary", H2),
             Paragraph("The eight sectors logged {fh:,.0f} flight hours over the season ({fh25:,.0f} in summer 2025). "
                       "There were {n} ATM-related losses of separation ({n25} in summer 2025), {b} of severity B and "
                       "{c} of severity C, none of severity A. No sector exceeded the unit safety plan's tolerance of "
                       "40.0 per 100,000 flight hours.".format(fh=fh26, fh25=fh25, n=n26, n25=n25, b=sev["B"],
                                                                 c=sev["C"]), BODY)]
    rows = [["Sector", "ATM-related losses, summer 2025", "ATM-related losses, summer 2026",
             "Flight hours, summer 2026", "Rate per 100,000 flight hours, summer 2026"]]
    for s in W.SECTORS:
        r = tab[s]
        rows.append([W.NAME[s], str(r["l25"]), str(r["l26"]), "{:,.0f}".format(r["fh26"]),
                     "%.1f" % (r["l26"] / r["fh26"] * 1e5)])
    rows.append(["All sectors", str(n25), str(n26), "{:,.0f}".format(fh26), "%.1f" % (n26 / fh26 * 1e5)])
    story += [Paragraph("Table 1&nbsp;&nbsp;ATM-related losses of separation by elementary sector", H2),
              _grid(rows, [28 * mm, 33 * mm, 33 * mm, 30 * mm, 40 * mm], bold_last=True),
              Paragraph("Tolerance (HACC-SAF-PLN-03, clause 4.1): 40.0 per 100,000 flight hours per elementary sector "
                        "and season.", META),
              Paragraph("Table 2&nbsp;&nbsp;Severity of the ATM-related losses of separation", H2),
              _grid([["Severity", "Summer 2025", "Summer 2026"]] +
                    [[{"A": "A, serious incident", "B": "B, major incident", "C": "C, significant incident"}[k],
                      str(tab["sev25"][k]), str(tab["sev"][k])] for k in "ABC"], [60 * mm, 30 * mm, 30 * mm]),
              Paragraph("Table 3&nbsp;&nbsp;Other indicators, all sectors", H2),
              _grid([["Occurrence type", "Summer 2025", "Summer 2026"]] +
                    [[label, str(tab["other25"][k]), str(tab["other26"][k])] for k, label in (
                        ("LB", "Level busts"), ("PLOC", "Prolonged loss of communication"),
                        ("DEV", "Deviations from clearance"), ("ATMT", "ATM technical"),
                        ("AI", "Airspace infringements"), ("WTE", "Wake turbulence encounters"))],
                    [60 * mm, 30 * mm, 30 * mm]),
              Paragraph("2&nbsp;&nbsp;Sector notes", H2),
              Paragraph("Hallin: the western arrival stream to Holmvik moved entirely onto the Hallin descent with AIRAC "
                        "2603 (19 March 2026), and the Karrow descent closed to it. Hallin's summer flight hours rose by "
                        "%.0f per cent and its ATM-related losses went from %s to %s." % (
                            hal, words.get(tab["HAL"]["l25"], tab["HAL"]["l25"]),
                            words.get(tab["HAL"]["l26"], tab["HAL"]["l26"])), BODY),
              Paragraph("All losses of separation of the season were investigated and closed by 2 October 2026; none is "
                        "open. %s with no ATM contribution (crew deviations from a correct clearance) %s outside the "
                        "indicator and %s reported with the level bust review." % (
                            words.get(tab["non26"], str(tab["non26"])).capitalize() + (" loss" if tab["non26"] == 1 else " losses"),
                            "is" if tab["non26"] == 1 else "are", "is" if tab["non26"] == 1 else "are"), BODY),
              Paragraph("3&nbsp;&nbsp;Actions from the season", H2),
              Paragraph("Hallin: a briefing on the western arrival stream and its hand-over to Holmvik approach for every "
                        "controller endorsed on Hallin, completed 30 June 2026. Level busts: the review with the three "
                        "operators most often involved is scheduled for October 2026.", BODY),
              Paragraph("4&nbsp;&nbsp;Next steps", H2),
              Paragraph("The forecast for summer 2027 will be presented with the summer sector plan to the Unit Safety "
                        "Review Board on 4 November 2026, on the planning traffic that Network and Capacity Planning "
                        "issues for the season.", BODY)]
    frame = _frame("%s  |  HACC-SAF-RPT-2026-11" % W.ANSP, "Safety Office")
    doc.build(story, onFirstPage=frame, onLaterPages=frame)


MONITORING = {"TRV": 46, "LYS": 44, "GRD": 42, "MSB": 40, "LNM": 36, "HAL": 34, "KRW": 34, "SDV": 36}


def _ops_grid(rows, widths, align_from=1):
    data = [[Paragraph(str(c), ParagraphStyle("oc", fontName="LiberationSerif-Bold" if i == 0 else SERIF, fontSize=9,
                                              leading=11, textColor=INK)) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.6, INK), ("INNERGRID", (0, 0), (-1, -1), 0.3, RULE),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e9ecef")),
                           ("ALIGN", (align_from, 0), (-1, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    return t


def _ops_frame(canvas, doc):
    canvas.saveState()
    canvas.setFont(SERIF, 8)
    canvas.setFillColor(GREY)
    canvas.drawString(20 * mm, A4[1] - 12 * mm, "Holmvik ACC Operations Manual  |  Part 3 Operating procedures  |  Chapter 4")
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 12 * mm, "Edition 26 March 2026, amdt 2026/1")
    canvas.drawString(20 * mm, 12 * mm, "Uncontrolled when printed. The controlled copy is in the document library.")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "3-4-%d" % doc.page)
    canvas.restoreState()


def write_om(path):
    doc = _doc(path, "HACC OM Part 3 Chapter 4 Sector configuration", "Holmvik ACC Operations")
    c = lambda no, text: Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (no, text), OPS_CLAUSE)
    story = [Paragraph("Chapter 4. Sector configuration", OPS_H1),
             Paragraph("Issued by Holmvik ACC Operations. Table 3.4-1 at revision 8.", OPS_META),
             Paragraph("4.1&nbsp;&nbsp;General", OPS_H2),
             c("4.1.1", "The Holmvik upper airspace is divided into the eight elementary sectors of the sector register. "
                        "Sectors are combined on one executive position when traffic allows, using only the "
                        "configurations of Table 3.4-1."),
             c("4.1.2", "The supervisor selects the configuration and records every change in the configuration log with "
                        "the local time and the configuration code. A change takes effect at the logged time."),
             Paragraph("4.2&nbsp;&nbsp;Selecting a configuration", OPS_H2),
             c("4.2.1", "A sector is opened on its own position when its entry count is forecast to exceed the monitoring "
                        "value of Table 3.4-2 in the configuration in use, or when the executive controller asks for it "
                        "because of complexity."),
             c("4.2.2", "The night configurations N3 and N2 are used from about 23:00 to 05:30 unless traffic requires "
                        "more positions. N2 is used only with the supervisor's agreement."),
             Paragraph("4.3&nbsp;&nbsp;Table 3.4-1 (revision 8): configurations", OPS_H2)]
    rows = [["Code", "Positions", "Sectors on each position"]]
    for code in CF.ORDER:
        rows.append([code, str(len(CF.REV8[code])), ", ".join("+".join(W.NAME[x] for x in g) for g in CF.REV8[code])])
    story.append(_ops_grid(rows, [16 * mm, 18 * mm, 136 * mm], align_from=3))
    story.append(Spacer(1, 3))
    story.append(Paragraph("C8 is the full split for peak hours; C7A, C7B, C6A, C6B and C5 step down through the shoulders "
                           "of the day; N3 and N2 are the night configurations.", OPS_META))
    story.append(Paragraph("4.4&nbsp;&nbsp;Table 3.4-2: monitoring values", OPS_H2))
    rows = [["Sector", "Monitoring value (entries per hour)"]] + [[W.NAME[s], str(MONITORING[s])] for s in W.SECTORS]
    story.append(_ops_grid(rows, [30 * mm, 60 * mm]))
    story += [Paragraph("4.5&nbsp;&nbsp;Amendments", OPS_H2),
              c("4.5.1", "Table 3.4-1 and Table 3.4-2 are changed only by an amendment to this Part. An amendment takes "
                         "effect at the time it states; the supervisor on duty records it in the configuration log."),
              Paragraph("4.6&nbsp;&nbsp;Carrying out a change", OPS_H2),
              c("4.6.1", "Before splitting a position, the supervisor confirms the receiving executive and planner are "
                         "plugged in and have taken the traffic picture; the giving position transfers each flight on its "
                         "frequency and the frequency change is broadcast."),
              c("4.6.2", "Before combining positions, the supervisor checks that the combined entry count stays under the "
                         "monitoring value of the busier sector for the next hour, and informs the adjacent units and "
                         "Holmvik approach of the new frequencies."),
              Paragraph("4.7&nbsp;&nbsp;The configuration log", OPS_H2),
              c("4.7.1", "Each entry carries the local time, the configuration code and the supervisor's initials. A "
                         "remark is added when the reason is other than traffic (staffing, weather, equipment, training) "
                         "and for any amendment taking effect."),
              c("4.7.2", "The log is kept in the supervisor's suite and exported weekly to the operations system."),
              Paragraph("4.8&nbsp;&nbsp;Degraded operations", OPS_H2),
              c("4.8.1", "In FDPS degraded mode the supervisor holds the configuration in use unless safety requires a "
                         "split, and logs the start and end of the degraded period as remarks."),
              c("4.8.2", "With a position unserviceable, the sector is combined with an adjacent sector by the nearest "
                         "configuration of Table 3.4-1 that leaves it open, and Engineering is called.")]
    doc.build(story, onFirstPage=_ops_frame, onLaterPages=_ops_frame)


NOTES_TEXT = """# Extract for the summer 2027 sector plan

Pulled 12 Oct 2026 by {data} (Data and Analytics) for the Safety Office and Network and Capacity Planning. Holmvik ACC
upper sectors only. Actuals run 1 Jan 2025 to 30 Sep 2026 unless a file says otherwise.

Files
- {fdps}: FDPS archive, one row per flight per sector entered, with entry and exit time and entry and exit flight
  level. ifplid is the network manager's flight plan id. Sector codes as in the sector register.
- {occ}: safety database export, occurrences in the Holmvik ACC sectors dated 1 Jan 2025 to 30 Sep 2026, one row per
  occurrence number. Levels in feet as reported or measured. Sector by name.
- {codes}: the AAN-OCC-01 code lists.
- {plan}: planning traffic for summer 2027, issue 1 of 9 Oct 2026 from Network and Capacity Planning ({planning}).
  Built from the operators' summer 2027 schedules as filed and the forecast growth. One row per planned flight per
  traffic volume, keyed by their own flight key.
- {register}: sectors, traffic volumes and limits.
- {slots}: network manager slot allocation list for the regulations on the Holmvik traffic volumes and on Holmvik
  arrivals, EOBT 1 May to 30 Sep 2026. One row per flight plan per regulation that allocated it a slot; slot_delay_min
  is the delay that regulation's slot gave the plan. ATFM delay is the network manager's: it is counted for the
  flights that operated, as the time between the take-off time the operator last requested and the take-off slot the
  network manager allocated; a flight captured by more than one regulation takes the slot of its most penalising
  regulation, and its delay is that regulation's, counted against that regulation.
- {regs}: the regulations for the same period. Regulation ids are reused from month to month; reg_date tells them
  apart.
- {clog}: supervisors' configuration log, 30 Apr to 30 Sep 2026.
- {ctab}: configuration table as exported from the ops system on 9 Oct 2026.
- {om}, {plan_doc}, {closeout}: from the document library and the Safety Office.
- {roster}, {met}: rostering system and the met office's convective summaries, as asked.

Clocks
- FDPS, occurrences, the NM files and the planning traffic are in UTC. The configuration log is in local time (CET,
  CEST in summer).
"""


def write_notes(path):
    text = NOTES_TEXT.format(data=W.PEOPLE["data"], planning=W.PEOPLE["planning"], fdps=R.FDPS, occ=R.OCC,
                             codes=R.CODES, plan=R.PLAN, register=R.REGISTER, slots=R.SLOTS, regs=R.REGS, clog=R.CLOG,
                             ctab=R.CTAB, om=OM, plan_doc=PLAN_DOC, closeout=CLOSEOUT, roster=R.ROSTER, met=R.MET)
    with open(path, "w", newline="\n") as fh:
        fh.write(text)
