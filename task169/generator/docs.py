"""The pack's documents: the allocation policy, the design guide's section 4, and the counter data notes (PDF),
written with reportlab's invariant mode so that two builds give the same bytes."""
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import names as N

CLAUSE_CROWDED, CLAUSE_REPLAY, CLAUSE_EVIDENCE, TABLE_CAPACITY = "3.3", "3.4", "4.2", "4.3"
STAMP = {"policy": b"D:20260318101500+00'00'", "guide": b"D:20250214113000+00'00'",
         "notes": b"D:20261002143000+01'00'"}

SS = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=SS["Normal"], fontName="Helvetica", fontSize=9.6, leading=12.6, alignment=TA_LEFT,
                      spaceAfter=4)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8.2, leading=10.4, textColor=colors.HexColor("#333333"))
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=14.5, leading=18, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10.8, leading=14, spaceBefore=7,
                    spaceAfter=3)


def _reserialise(path, stamp, author, title):
    """rewrite the PDF through a second library (H25): a fresh structure and cross-reference table, the issuing
    office as producer and creator, and the issue date as the creation and modification date"""
    import io
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter(clone_from=PdfReader(path))
    w.add_metadata({"/Producer": N.COUNCIL, "/Creator": N.COUNCIL, "/CreationDate": stamp.decode(),
                    "/ModDate": stamp.decode(), "/Author": author, "/Title": title})
    buf = io.BytesIO()
    w.write(buf)
    with open(path, "wb") as fh:
        fh.write(buf.getvalue())


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, subject=subject, creator=N.COUNCIL,
                             producer=N.COUNCIL, invariant=1)


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 10 * mm, text)
        canvas.drawRightString(190 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _grid(rows, widths, head=True):
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    st = [("FONT", (0, 0), (-1, -1), "Helvetica", 8.6), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if head:
        st += [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.6), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6"))]
    t.setStyle(TableStyle(st))
    return t


def policy_pdf(path):
    atl = N.PEOPLE["atl"][0]
    hts = N.PEOPLE["hts"][0]
    d = _doc(path, "Cycleway Widening Allocation Policy", atl, "Cycleway Capacity Fund")
    s = []
    s.append(Paragraph("Calvermouth City Council", SMALL))
    s.append(Paragraph("Cycleway Widening Allocation Policy", H1))
    s.append(_grid([["Reference", "AT-POL-07"], ["Version", "1.0"],
                    ["Approved", "Transport and Environment Committee, 17 March 2026 (minute TE/25-26/118)"],
                    ["Owner", "%s, Active Travel Team Leader" % atl], ["Next review", "March 2028"]],
                   [32 * mm, 130 * mm], head=False))
    s.append(Spacer(1, 6))
    s.append(Paragraph("1. Purpose", H2))
    s.append(Paragraph("1.1 The Cycleway Capacity Fund pays for one widening scheme on the city's cycleways in each "
                       "financial year. This policy sets how that scheme is chosen.", BODY))
    s.append(Paragraph("1.2 It applies to the six cycleways of the Cycle Network Plan 2022: CW1 Tolland Road, CW2 "
                       "Brickfields, CW3 Estuary Path, CW4 Wardle Park, CW5 Market Street and CW6 Southfield.", BODY))
    s.append(Paragraph("2. Allocation", H2))
    s.append(Paragraph("2.1 Each year's scheme is allocated to the cycleway forecast to be crowded on the most days of the "
                       "coming summer, 1 June to 31 August.", BODY))
    s.append(Paragraph("2.2 For the 2026-27 round the coming summer is 1 June to 31 August 2027. The scheme is designed "
                       "from November 2026 and built between January and the end of May 2027.", BODY))
    s.append(Paragraph("2.3 The Active Travel Team reports the forecast and its recommendation to the Transport and "
                       "Environment Committee. Where two cycleways' forecasts are equal the committee chooses between "
                       "them.", BODY))
    s.append(Paragraph("3. Definitions", H2))
    s.append(Paragraph("3.1 A cycleway's counted segments are its segments in the Path Inventory that carry a counter.", BODY))
    s.append(Paragraph("3.2 A segment's capacity is the two-way flow given in Table 4.3 of the Cycle Design Guide for "
                       "the segment's minimum width in the Path Inventory.", BODY))
    s.append(Paragraph(CLAUSE_CROWDED + " A cycleway is crowded on a day when, in any clock hour from 06:00 to 22:00 local time, the "
                       "cyclists counted past any of its counted segments, both directions together, exceed that "
                       "segment's capacity. An hour a counter did not record cannot make the day crowded.", BODY))
    s.append(Paragraph(CLAUSE_REPLAY + " The forecast for a coming summer takes each day of the three most recent summers on record, "
                       "with that day's own weather and calendar, as an equally likely day of the coming summer, at the "
                       "numbers of cyclists expected in the coming summer. A cycleway's forecast crowded days are the "
                       "mean, over those three summers, of the days on which it would be crowded. For the 2026-27 round "
                       "the three summers are those of 2024, 2025 and 2026.", BODY))
    s.append(Paragraph("4. Evidence", H2))
    s.append(Paragraph("4.1 The forecast draws on the Traffic Monitoring Unit's counter exports and register and the Path "
                       "Inventory kept by Highways Design.", BODY))
    s.append(Paragraph("4.2 Counter data are used as the counters recorded them. The volunteer counts organised with "
                       "the Calvermouth Cycle Forum are reported beside the forecast as a check on the counters and do "
                       "not enter it.", BODY))
    s.append(Paragraph("5. Document history", H2))
    s.append(_grid([["Version", "Date", "Change"], ["0.3", "January 2026", "Draft for consultation with Highways Design"],
                    ["1.0", "17 March 2026", "Approved by committee; replaces the 2022 widening criteria"]],
                   [18 * mm, 30 * mm, 114 * mm]))
    s.append(Spacer(1, 4))
    s.append(Paragraph("Approved for issue: %s, Head of Transport Strategy." % hts, SMALL))
    d.build(s, onFirstPage=_footer("AT-POL-07 v1.0"), onLaterPages=_footer("AT-POL-07 v1.0"))
    _reserialise(path, STAMP["policy"], atl, "Cycleway Widening Allocation Policy")


def design_guide_pdf(path, bands):
    hde = N.PEOPLE["hde"][0]
    d = _doc(path, "Cycle Design Guide 2023, Section 4", hde, "Cycle tracks")
    s = []
    s.append(Paragraph("Calvermouth City Council, Highways Design", SMALL))
    s.append(Paragraph("Cycle Design Guide (2023 edition)", H1))
    s.append(Paragraph("Section 4: Cycle tracks", H2))
    s.append(Paragraph("4.1 This section covers segregated cycle tracks on the city's cycleways. Shared paths are in "
                       "Section 6 and junctions in Section 7.", BODY))
    s.append(Paragraph("4.2 Width. A track's minimum width is the narrowest clear width between kerbs, walls or edges "
                       "along a segment. Where a parapet, rail or fence borders the track the width is measured 0.5 m "
                       "above the surface. Highways Design records each segment's minimum width in the Path Inventory "
                       "after every survey.", BODY))
    s.append(Paragraph("4.3 Capacity. Table 4.3 gives, for two-way tracks, the flow in both directions together above "
                       "which a track of each minimum width is crowded: riders can no longer pass one another without "
                       "slowing and oncoming riders meet at close quarters (level of service D in the guide's terms).", BODY))
    rows = [["Minimum width (m)", "Two-way capacity (cyclists per hour)"]]
    for lo, hi, cap in bands:
        rows.append([("%.1f and over" % lo) if hi > 9 else ("%.1f to under %.1f" % (lo, hi)), "{:,}".format(cap)])
    s.append(Spacer(1, 3))
    s.append(Paragraph("Table 4.3 Two-way cycle track capacity", SMALL))
    s.append(_grid(rows, [55 * mm, 70 * mm]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("4.4 New tracks are designed to 4.0 m two-way wherever the corridor allows, and never below 3.0 m "
                       "without the Principal Engineer's approval. Widening an existing track is designed to the same "
                       "standard.", BODY))
    s.append(Paragraph("4.5 One-way tracks are designed to Table 4.5 (not reproduced here).", BODY))
    s.append(Spacer(1, 4))
    s.append(Paragraph("Issued by %s, Principal Engineer, Highways Design. Edition of 2023, unchanged in the 2025 "
                       "reprint." % hde, SMALL))
    d.build(s, onFirstPage=_footer("Cycle Design Guide 2023, Section 4"), onLaterPages=_footer("Cycle Design Guide 2023, Section 4"))
    _reserialise(path, STAMP["guide"], hde, "Cycle Design Guide 2023, Section 4")


def data_notes_pdf(path):
    tmo = N.PEOPLE["tmo"][0]
    d = _doc(path, "Cycle counter data: notes for users", tmo, "Traffic Monitoring Unit")
    s = []
    s.append(Paragraph("Calvermouth City Council, Traffic Monitoring Unit", SMALL))
    s.append(Paragraph("Cycle counter data: notes for users", H1))
    s.append(Paragraph("Issue 4, 2 October 2026. Contact: %s, Traffic Monitoring Officer." % tmo, SMALL))
    s.append(Paragraph("1. The counters", H2))
    s.append(Paragraph("Six dashboard counters run all year at fixed sites, one on each cycleway. Summer counters are "
                       "installed on the cycleway segments in the last days of May and removed in the first days of "
                       "September. The register lists every logger unit with its site, cycleway, segment and dates.", BODY))
    s.append(Paragraph("2. Platforms", H2))
    s.append(Paragraph("Loggers reported to the legacy logging platform until 31 December 2024. The dashboard counters "
                       "moved to the current counter platform on 6 January 2025 and the summer counters reported to it "
                       "from June 2025.", BODY))
    s.append(Paragraph("3. Legacy exports", H2))
    s.append(Paragraph("Semicolon separated, with two header lines. One row per site per hour, local time "
                       "(Europe/London), the hour beginning. Ch1 and Ch2 are the logger's two directions; the register's "
                       "ch1_direction gives which way Ch1 counts at each site. A blank count means the logger kept "
                       "nothing for that hour.", BODY))
    s.append(Paragraph("4. Current platform exports", H2))
    s.append(Paragraph("Hourly exports give one row per counter, hour and direction. timestamp_utc is the hour "
                       "beginning, in UTC. Direction in is towards the city centre. Status ok is a recorded count; "
                       "estimated is the platform's estimate for a gap of up to three hours; no_data is an hour the "
                       "counter did not record and carries a count of 0.", BODY))
    s.append(Paragraph("Interval exports give 15-minute counts with counter_id, timestamp_utc, direction and count. "
                       "Intervals the logger did not keep are left out of the export.", BODY))
    s.append(Paragraph("5. The register", H2))
    s.append(Paragraph("Where a unit was replaced, both units appear with their installed and removed dates and the "
                       "dates each was the unit of record for the site. Only the unit of record supplies the site's "
                       "counts.", BODY))
    s.append(Paragraph("6. The dashboard", H2))
    s.append(Paragraph("The public dashboard shows monthly totals at the six dashboard sites, both directions together. "
                       "Days a site did not record are filled with the platform's estimate before publication. Figures "
                       "to 2023 come from the legacy platform's monthly reports.", BODY))
    s.append(Paragraph("7. The maintenance log", H2))
    s.append(Paragraph("The log is the council's job system export for the counter assets: one row per job, with the "
                       "contractor's jobs alongside the unit's own. parent_job links a follow-up visit to the job it "
                       "follows up. Times are local. downtime is entered when the job is closed.", BODY))
    s.append(Paragraph("8. Weather", H2))
    s.append(Paragraph("The council's station on the Civic Centre roof (CVM-WX1) records the day's maximum and minimum "
                       "temperature, rainfall for the calendar day and hours of bright sunshine. Days the station did "
                       "not report are blank.", BODY))
    d.build(s, onFirstPage=_footer("TMU data notes, issue 4"), onLaterPages=_footer("TMU data notes, issue 4"))
    _reserialise(path, STAMP["notes"], tmo, "Cycle counter data: notes for users")
