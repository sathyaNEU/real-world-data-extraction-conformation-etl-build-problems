"""The filed documents: Thornacre's peak stock-record standard (PDF), Corderoy's perpetual count programme
for Thornacre (DOCX) and the BI extract notes for the pull of 7 December (TXT)."""
import os

from reportlab import rl_config
from reportlab.lib.pagesizes import A4

rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

FILES = {
    "standard": "Thornacre_SCS-07_peak_stock_record_standard_v3.pdf",
    "programme": "Corderoy_CP-THN-04_perpetual_count_programme.docx",
    "notes": "extract_notes_LF_20261207.txt",
}

STANDARD = [
    ("h", "1  Purpose"),
    ("p", "Thornacre's automated replenishment raises store orders on its distribution centres against the stock "
          "records each centre holds for its pick locations. Through the Christmas trading freeze the replenishment "
          "controllers run a reduced rota, so a centre whose records do not meet this standard has its order lines "
          "reviewed by a controller before release. This standard sets the test."),
    ("h", "2  Scope"),
    ("p", "Every distribution centre operated for Thornacre by a third-party logistics provider (the 3PL). Thornacre's "
          "own sites and its direct-to-store suppliers are out of scope."),
    ("h", "3  Definitions"),
    ("p", "3.1  <b>Line</b>: a Thornacre product line, identified by its Thornacre line number."),
    ("p", "3.2  <b>Stock unit</b>: the unit in which the 3PL's system holds a line, as set on the Thornacre line master "
          "(cases, or eaches for single-pick lines)."),
    ("p", "3.3  <b>Location</b>: a storage location on the 3PL's warehouse management system."),
    ("p", "3.4  <b>Freeze</b>: the Christmas trading freeze, during which no change is made to slotting, count "
          "programmes or replenishment parameters."),
    ("h", "4  Record accuracy"),
    ("p", "4.1  A location is in scope at a time when it is a pick face holding a slot for a Thornacre line on the "
          "3PL's location master and is not on quality hold or recall."),
    ("p", "4.2  A location's record is correct when its system quantity equals the quantity a count under the 3PL's "
          "count programme would record, in the line's stock unit (kilograms within the scale tolerance for weighed "
          "lines)."),
    ("p", "4.3  Record accuracy at a time is the number of in-scope locations whose record a full count at that time "
          "would find correct, divided by the number of in-scope locations at that time, as a percentage."),
    ("p", "4.4  For the peak gate the measurement time is the moment the 3PL stands its counting down for the freeze, "
          "06:00 on 7 December 2026."),
    ("p", "4.5  Where the 3PL does not count every in-scope location at the measurement time it estimates record "
          "accuracy from its count records, and the estimate is the one a full count at the measurement time would be "
          "expected to bear out."),
    ("h", "5  Peak gate"),
    ("p", "5.1  A centre's replenishment runs unattended through the freeze (06:00 on 7 December 2026 to 06:00 on "
          "4 January 2027) when its record accuracy at the measurement time is 97.0 per cent or more, and is "
          "supervised otherwise."),
    ("p", "5.2  The 3PL declares each centre's record accuracy and verdict to Thornacre Supply Chain by 12:00 on the "
          "day of the measurement time. The declaration is signed by the 3PL's account director."),
    ("p", "5.3  A supervised centre stays supervised for the whole freeze. A centre running unattended that reports "
          "three or more short-shipped store orders in one trading day is moved to supervised replenishment for the "
          "rest of the freeze."),
    ("h", "6  Records"),
    ("p", "The 3PL keeps its location master history and every count record, with the counted and system quantities, "
          "for two years, and provides them to Thornacre on request."),
]


def standard_pdf(path):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=4)
    head = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=8, spaceAfter=3)
    title = ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=14, leading=17)
    small = ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica", fontSize=8, leading=10,
                           textColor=colors.HexColor("#444444"))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title="SCS-07 Peak stock-record standard", author="Thornacre Supply Chain",
                            subject="Supply chain standard", creator="Thornacre Supply Chain", producer="Thornacre Supply Chain")
    story = [Paragraph("Thornacre Stores Ltd &nbsp;&nbsp;|&nbsp;&nbsp; Supply Chain Standards", small), Spacer(1, 4),
             Paragraph("SCS-07 &nbsp;Peak stock-record standard for 3PL distribution centres", title), Spacer(1, 6)]
    ctl = Table([["Version", "3", "Effective", "01/09/2026"],
                 ["Owner", "Head of Replenishment (S. Sykes)", "Approved", "Supply Chain Director"],
                 ["Supersedes", "Version 2 (04/09/2025)", "Review due", "31/08/2027"]],
                colWidths=[24 * mm, 58 * mm, 22 * mm, 56 * mm])
    ctl.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.5),
                             ("FONT", (2, 0), (2, -1), "Helvetica-Bold", 8.5), ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                             ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story += [ctl, Spacer(1, 8)]
    for kind, text in STANDARD:
        story.append(Paragraph(text, head if kind == "h" else body))
    story += [Spacer(1, 10),
              Paragraph("Version history: v3 01/09/2026, freeze dates for 2026/27, 5.3 added; v2 04/09/2025, line raised "
                        "from 96.0 per cent; v1 22/08/2023, first issue.", small), Spacer(1, 4),
              Paragraph("Issued to contracted 3PL providers. Printed copies are uncontrolled.", small)]
    doc.build(story)


PROGRAMME = [
    ("t", "CP-THN-04  Perpetual count programme: Thornacre pick faces"),
    ("m", "Corderoy Logistics Ltd, Inventory Control. Version 7, effective 18 May 2026. Owner: Arthur Mason, Inventory "
          "Control Manager. Applies at every Corderoy site holding Thornacre pick faces."),
    ("h", "1. Scope"),
    ("p", "Every pick face holding a Thornacre line. Reserve locations are counted under CP-GEN-02 (annual wall-to-wall "
          "and reserve audits) and are not part of this programme. Random-weight Thornacre lines are stocked and counted in "
          "packs; no Thornacre pick face holds a weighed line."),
    ("h", "2. Count classes"),
    ("p", "Each face takes the slotting class set at the annual slotting review (May 2026), from the face's pick velocity "
          "over the previous 13 weeks. The class sets the routine count cycle:"),
    ("tbl", [["Class", "Routine cycle", "Typical face"], ["A", "28 days", "fast movers, top 15 to 30 per cent of picks"],
             ["B", "56 days", "medium movers"], ["C", "91 days", "slow movers"]]),
    ("p", "Faces are not re-classed between reviews. A face re-slotted to another line keeps the slot's class until the "
          "next review."),
    ("h", "3. Routine counts"),
    ("p", "Every face has a place on its class's count calendar. A routine count task (reason CYC) is generated on the "
          "night the face falls due under its class's cycle. A task not completed in that night's count window rolls "
          "to the next night and stays open until it is done. When a face takes an exception count on the night it "
          "falls due, the exception count closes the routine task as well."),
    ("h", "4. Exception counts"),
    ("p", "An exception count task is raised the same night on any of the following, from the WMS or from a picker's "
          "handheld:"),
    ("tbl", [["Code", "Raised by"], ["SHP", "short pick: the picker could not pick the quantity the system allocated"],
             ["NEG", "negative balance: a transaction would take the face's system quantity below zero"],
             ["EMP", "empty face reported by a picker or a replenishment driver"],
             ["OVR", "overflowed replenishment: a let-down did not fit the face and was returned to reserve"],
             ["CYC", "routine count (section 3)"]]),
    ("h", "5. How a count is done"),
    ("p", "Counts run in the count window, 02:00 to 05:30, after the last pick wave of the trading day and before the "
          "first replenishment wave. First counts are blind: the counter's handheld shows the location and the line, "
          "never the system quantity. Where the first count differs from the system quantity a supervisor recounts the "
          "face before anything is posted. The confirmed count (the recount where there is one, otherwise the first "
          "count) is posted as the location's record, and the difference is posted as a stock adjustment against the "
          "Thornacre line. Counts are recorded in the line's stock unit."),
    ("h", "6. Peak stand-down"),
    ("p", "For the Thornacre freeze all counting on Thornacre pick faces, routine and exception, stands down at 06:00 on "
          "7 December 2026 and resumes on the night of 4 January 2027. Short picks and negative balances during the "
          "freeze are logged for the first night after it."),
    ("h", "7. Records"),
    ("p", "Every count task, with its first count, recount, confirmed quantity and the system quantity at the time of "
          "the count, is kept on the WMS count history. The location master keeps each location's slotting history "
          "with effective dates."),
]


def programme_docx(path):
    from docx import Document
    from docx.shared import Pt
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for kind, x in PROGRAMME:
        if kind == "t":
            d.add_heading(x, level=1)
        elif kind == "m":
            p = d.add_paragraph(x)
            p.runs[0].italic = True
        elif kind == "h":
            d.add_heading(x, level=2)
        elif kind == "p":
            d.add_paragraph(x)
        elif kind == "tbl":
            t = d.add_table(rows=len(x), cols=len(x[0]))
            t.style = "Table Grid"
            for i, row in enumerate(x):
                for j, v in enumerate(row):
                    t.cell(i, j).text = v
                    if i == 0:
                        t.cell(i, j).paragraphs[0].runs[0].bold = True
    d.core_properties.author = "Arthur Mason"
    d.core_properties.last_modified_by = "Arthur Mason"
    d.core_properties.title = "CP-THN-04 Perpetual count programme"
    import datetime as dt
    d.core_properties.created = dt.datetime(2026, 5, 11, 9, 4, 0)
    d.core_properties.modified = dt.datetime(2026, 5, 15, 16, 41, 0)
    d.core_properties.revision = 7
    d.save(path)


def notes_txt(path, files, counts):
    f = files
    text = """Thornacre peak gate 2026 - extract notes
Leonard Finch, BI, Corderoy Logistics. Pulled 07/12/2026 from 06:05.

All WMS timestamps are UTC (suffix Z). Sites trade 06:00 to 06:00 UK local time, so the count window
02:00-05:30 belongs to the trading day before; clocks went back on 25/10, so the same window is 01:00-04:30Z
before that date and 02:00-05:30Z after it.

{counts}
  WMS count history, Thornacre pick faces, all eight sites. One row per count task, every reason code,
  tasks posted from the start of trading on 01/06/2026 up to the stand-down at 06:00 on 07/12. The last
  window in the file is the night of 06/12 into 07/12. recount_qty and supervisor_id are blank where the
  first count agreed with the system. result is the WMS's own test (confirmed against system quantity, in
  the line's stock unit). {n_counts} rows.

{locations}
  WMS location master for the Thornacre client, pick faces and reserve, with effective dates (eff_to blank
  = current). One row per location per version. Other clients' pick faces at the two shared sites (HNK,
  THU) are in the extract because the WMS cannot filter that table by client; their client code is not THN.
  pick_velocity = picks per day over the 13 weeks to the May 2026 slotting review.

{snapshot}
  WMS stock by location at 06:00 on 07/12, Thornacre client, every location holding stock. One row per stock
  record. qty is in stock_unit.

{batches}
  WMS batch register at the same time: batches and best-before dates on date-coded lines.

{centres}
  Site codes, the Thornacre depot code each site trades under, and the WMS instance it runs on.

From Thornacre (as received):
{linemaster}  line master export, 04/12
{costbase}  cost price list, extracted 28/11
{costp10}  period 10 cost changes, received 02/12
{forecast}  store replenishment forecast, run of 23/11 (the last full run before the freeze)
{servicing}  store to depot servicing, with valid-from/valid-to dates
{calendar}  store trading calendar for Christmas and New Year
{stores}  store list from the estate service, 03/12
{categories}  category table used by the forecast

Ops planning (Corderoy): {labour}, {goodsin}.

Documents: {standard} is the version on Thornacre's supplier portal on 07/12; {programme} is
our current issue.
""".format(n_counts="{:,}".format(counts["counts"]), **f)
    with open(path, "w", newline="") as fh:
        fh.write(text.replace("\n", "\r\n"))
