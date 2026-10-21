"""task252 documents: the council's online monitoring data standard WQ-DS-04 (pdf), the plants' process summary
(pdf), the data dictionary (md) and the laboratory's notice of the new site codes (eml)."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import records as R


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    return body, h1, h2, small


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.6)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _table(rows, widths, size=8.2):
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size + 2.2)
    head = ParagraphStyle("head", parent=cell, fontName="Helvetica-Bold")
    rows = [[Paragraph(str(v), head if r == 0 else cell) for v in row] for r, row in enumerate(rows)]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF2")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def standard(path):
    body, h1, h2, small = _styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="WQ-DS-04 Online water quality monitoring: data standard",
                            author=P.ORG, creator=P.ORG, subject="Water Services data standard WQ-DS-04, issue 3",
                            invariant=1)
    s = [Paragraph(P.ORG + " | " + P.UNIT, small), Spacer(1, 2 * mm),
         Paragraph("WQ-DS-04 Online water quality monitoring: data standard", h1),
         Paragraph("Issue 3, 2 June 2027. Owner: Water Quality Compliance. Approved by the Water Services Manager. "
                   "Replaces issue 2 (2025).", small),
         Paragraph("1. Scope", h2),
         Paragraph("This standard applies to the online analysers whose readings feed the plants' control systems and "
                   "the quarterly online monitoring return: the ammonia analysers at the eight water treatment plants. "
                   "Quarters are calendar quarters in New Zealand time.", body),
         Paragraph("2. Channels", h2),
         Paragraph("A channel is one analyser reading one sample point. Each plant's ammonia analyser reads three "
                   "sample points, raw, filtered and final water, in turn through a three-stream sequencer, in the port "
                   "order the online analyser register gives. The register also gives each sample point's code in the "
                   "control system and in the laboratory.", body),
         Paragraph("3. Offset", h2),
         Paragraph("A channel's offset for a quarter is the average, over the channel's readings held in the historian "
                   "with quality code G for the quarter, of the difference between each reading and the ammonia actually "
                   "in the water at its sample point at the time of that reading, in mg/L as N.", body),
         Paragraph("4. Acceptance", h2),
         Paragraph("A treated water channel (filtered or final water) whose offset for the quarter is more than 0.005 "
                   "mg/L as N above or below zero is flagged in the quarterly return. A flagged channel's readings for "
                   "the quarter are marked provisional and the channel goes on the instrument technicians' list before "
                   "the next quarter.", body),
         Paragraph("5. Verification", h2),
         Paragraph("Each analyser is checked once a month against a 0.100 mg/L as N ammonium standard through its check "
                   "port. The technician flushes the measuring cell with the standard, takes three readings on it and "
                   "records them in the verification workbook; the mean of the three must lie within 10 per cent of the "
                   "standard. The check's three readings are also held in the historian with quality code V.", body),
         Paragraph("6. Laboratory samples", h2),
         Paragraph("The contract laboratory, %s, takes a grab sample at every sample point each week on the "
                   "sampling round. Ammonia samples are analysed within 24 hours of collection. The laboratory's limit "
                   "of detection for ammoniacal nitrogen is 0.030 mg/L as N; results below it are reported as less than "
                   "the limit." % P.LAB, body),
         Paragraph("7. The quarterly return", h2),
         Paragraph("The return for each quarter states:", body),
         Paragraph("(a) the flagged channels (section 4);", body),
         Paragraph("(b) for each plant, how many of the quarter's filtered and final water samples were analysed more "
                   "than 24 hours after collection;", body),
         Paragraph("(c) for each plant, the hours in the quarter that the plant's chlorine dose ran at its fixed dose "
                   "because the filtered water ammonia reading was not available to the dose control (the process "
                   "summary describes the dose control).", body),
         Paragraph("The return is filed by the Water Quality Compliance Officer by the twentieth working day after the "
                   "quarter ends.", body),
         Spacer(1, 3 * mm),
         _table([["Issue", "Date", "Change"],
                 ["1", "March 2023", "First issue (online ammonia analysers at Calderwood, Garrick and Holmedale)"],
                 ["2", "August 2025", "All eight plants; quarterly return; laboratory detection limit 0.030"],
                 ["3", "June 2027", "Return item (c) added with the feed-forward chlorine dose control"]],
                [18, 26, 128])]
    doc.build(s, onFirstPage=_footer("WQ-DS-04 issue 3"), onLaterPages=_footer("WQ-DS-04 issue 3"))


def process(path, W):
    body, h1, h2, small = _styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="Water treatment plants: process summary 2027", author=P.ORG,
                            creator=P.ORG, subject="Water Services operations reference", invariant=1)
    transit = {"BRN": (2.9, 4.6), "CAL": (2.4, 4.1), "ELS": (3.0, 4.8), "GAR": (2.8, 4.2), "HOL": (2.6, 4.7)}
    for c in P.WEAK:                       # where raw ammonia passes through, the tracer studies' times
        b, lf, ln = W[c]["breakthrough"]
        transit[c] = (round(lf / 6 - 0.15, 1), round(ln / 6 - 0.15, 1))
    rows = [["Plant", "Source", "Average output (ML/d)", "Intake to filtered water tap (h)",
             "Intake to final water tap (h)", "Fixed chlorine dose (mg/L)"]]
    src = {"ASH": "Harrow River", "BRN": "Kestrel Stream", "CAL": "Bramble River", "DUN": "Harrow River",
           "ELS": "Linnet Stream", "FEN": "Harrow River", "GAR": "Bramble River", "HOL": "Sedge Stream"}
    out = {"ASH": 9.6, "BRN": 6.3, "CAL": 15.1, "DUN": 7.9, "ELS": 5.0, "FEN": 11.5, "GAR": 8.8, "HOL": 12.6}
    fixed = {"ASH": 2.6, "BRN": 2.4, "CAL": 3.4, "DUN": 2.6, "ELS": 2.3, "FEN": 2.6, "GAR": 3.2, "HOL": 3.3}
    for c in P.CODES:
        a, b = transit[c]
        rows.append([P.NAME[c], src[c], "%.1f" % out[c], "%.1f to %.1f" % (a - 0.3, a + 0.6),
                     "%.1f to %.1f" % (b - 0.3, b + 0.7), "%.1f" % fixed[c]])
    s = [Paragraph(P.ORG + " | " + P.UNIT, small), Spacer(1, 2 * mm),
         Paragraph("Water treatment plants: process summary", h1),
         Paragraph("Operations reference, revised July 2027. Times are nominal at average output and shorten as "
                   "output rises.", small),
         Paragraph("Treatment", h2),
         Paragraph("All eight plants abstract river or stream water and treat it by coagulation, clarification and rapid "
                   "gravity filtration, then chlorination in a contact tank ahead of the outlet main. Raw water ammonia "
                   "rises after heavy rain in the dairying catchments and after effluent spills upstream of the intakes; "
                   "the filters remove some of it, and what is left consumes chlorine in the contact tank.", body),
         _table(rows, [24, 30, 26, 32, 30, 30]),
         Paragraph("Ammonia analysers", h2),
         Paragraph("Each plant has one colorimetric ammonia analyser (salicylate method, range 0 to 5 mg/L as N) with a "
                   "three-stream sequencer. Each sample point's water comes to the analyser in its own sample line, and the "
                   "sequencer passes each in turn through the one measuring cell for ten minutes, so each sample point is "
                   "read every 30 minutes. The "
                   "analyser's reading for a port is the measurement at the end of that port's ten minutes. A fault "
                   "(reagent, measuring cell or a blocked sample line) stops the readings it affects until a technician "
                   "clears it.", body),
         Paragraph("Chlorine dose control", h2),
         Paragraph("Each plant's PLC sets the chlorine dose ahead of the contact tank on a feed-forward from the filtered "
                   "water ammonia reading: the plant's base dose plus 7.6 mg/L of chlorine for each mg/L of ammonia as "
                   "N. If no good filtered water reading reaches the PLC for two hours, the PLC switches to the plant's "
                   "fixed dose (table above) and returns to the feed-forward with the next good filtered water "
                   "reading.", body),
         Paragraph("Telemetry", h2),
         Paragraph("Each plant's PLC reads its ammonia analyser directly and runs the dose control on what it reads. The "
                   "plant's telemetry outstation reads the PLC every ten minutes and keeps the last 72 hours of readings "
                   "with the analyser's status in memory, which a restart clears. The historian at the operations centre "
                   "in Fernvale polls each outstation every ten minutes and holds the readings for reporting and for the "
                   "quarterly return; when a poll fails it marks the slot and fills it from the outstation's store once "
                   "the link is back.", body)]
    doc.build(s, onFirstPage=_footer("Process summary, July 2027"), onLaterPages=_footer("Process summary, July 2027"))


def dictionary(path):
    txt = """# Water Services data dictionary: online ammonia monitoring and laboratory results

Kept by Water Quality Compliance. Revised 3 November 2027.

## nh3_online_readings (historian export)

| Column | Meaning |
|---|---|
| site_code | Plant code (ASH Ashcombe, BRN Brannock, CAL Calderwood, DUN Dunmere, ELS Elstow, FEN Fenwick, GAR Garrick, HOL Holmedale) |
| analyser_tag | The plant's ammonia analyser, as in the online analyser register |
| reading_end_utc | End of the ten-minute port slot the reading belongs to, UTC |
| sample_point | Control system sample point code (register, Sample points sheet); `<plant>-CHK` is the analyser's check port |
| nh3_n_mgl | Ammoniacal nitrogen, mg/L as N, three decimals; blank when there is no reading |
| qc | G good; F no reading for the slot; V verification check reading through the check port |

A failed poll that the historian later fills from the plant's outstation keeps its F row, and the reading it was
filled with follows under the same time with qc G. A slot with no row at all is one the historian's own server
failed to store; the plants ran normally.

## lims_ammonia (laboratory export)

| Column | Meaning |
|---|---|
| sample_no | Laboratory sample number |
| lims_point | Laboratory sample point code (register, Sample points sheet) |
| location | Sample point as the laboratory describes it |
| collected | Date and time the sampler took the sample, New Zealand time, as written on the bottle |
| received | Date and time the laboratory's reception logged the sample, New Zealand time |
| analysed | Date and time of the ammonia analysis, from the laboratory's analyser run record |
| released | Date and time the laboratory released the result to Water Services, New Zealand time |
| determinand | Ammoniacal-N |
| result | mg/L as N; `<0.030` is below the limit of detection |
| units, lod | Units and limit of detection |
"""
    with open(path, "w", newline="\n") as fh:
        fh.write(txt)


def notice(path, W):
    body = """From: Suzanne Nelson <client.services@kowhaibay-analytical.co.nz>
To: Emily Butler <emily.butler@fernvale.govt.nz>
Cc: Water Services Laboratory Results <wslab@fernvale.govt.nz>
Date: Thu, 28 Oct 2027 15:42:10 +1300
Subject: New site codes for your treated water sampling points from 1 November
Message-ID: <20271028154210.7731@kowhaibay-analytical.co.nz>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 7bit

Kia ora Emily,

As discussed, from Monday 1 November we will log your treated water samples under the
drinking water site codes you sent through, so our reports line up with your compliance
returns. The raw water points keep their current codes.

  Old code     New code
  TW-ASH-F     TUR0004B
  TW-ASH-W     TUR0004D
  TW-BRN-F     TUR0007B
  TW-BRN-W     TUR0007D
  TW-CAL-F     TUR0009B
  TW-CAL-W     TUR0009D
  TW-DUN-F     TUR0012B
  TW-DUN-W     TUR0012D
  TW-ELS-F     TUR0015B
  TW-ELS-W     TUR0015D
  TW-FEN-F     TUR0018B
  TW-FEN-W     TUR0018D
  TW-GAR-F     TUR0021B
  TW-GAR-W     TUR0021D
  TW-HOL-F     TUR0026B
  TW-HOL-W     TUR0026D

Results already reported keep the code they were reported under. Nothing changes for the
sampler: same bottles, same chilly bins, same courier.


Nga mihi,
Suzanne Nelson
Client Services Coordinator
Kowhai Bay Analytical
"""
    with open(path, "w", newline="\r\n") as fh:
        fh.write(body)
