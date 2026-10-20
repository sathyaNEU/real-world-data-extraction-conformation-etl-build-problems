"""The pack's documents and workbooks: the fund's guidelines (PDF), the candidate list and the payment journal
(xlsx), the city's extract notes (txt)."""
import datetime as dt

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                    # noqa: E402
from reportlab.lib.pagesizes import letter                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                     # noqa: E402
from reportlab.lib.units import inch                                # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402
from openpyxl import Workbook                                       # noqa: E402
from openpyxl.styles import Alignment, Font                         # noqa: E402

import pack as P    # noqa: E402
import world as W   # noqa: E402

SECTIONS = {"tests": "3.1", "rate": "3.2", "memo": "4.2"}
BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.5, spaceAfter=6)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=15, leading=19, spaceAfter=4)
SUB = ParagraphStyle("s", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#444444"),
                     spaceAfter=10)


def _doc(path, title):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                          topMargin=0.9 * inch, bottomMargin=0.9 * inch, title=title, author="City of %s" % W.CITY,
                          creator="City of %s" % W.CITY, producer="City of %s" % W.CITY, subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.95 * inch, 0.55 * inch, "City of %s, %s  |  %s" % (W.CITY, W.DEPT, title))
        c.drawRightString(letter[0] - 0.95 * inch, 0.55 * inch, "Page %d" % d_.page)
        c.restoreState()
    return d, frame


def write_guidelines(path):
    d, frame = _doc(path, "Neighborhood Stabilization Fund, 2027 Round Guidelines")
    s = [Paragraph("Neighborhood Stabilization Fund: 2027 Round Guidelines", TITLE),
         Paragraph("City of %s, %s. Adopted by the Housing Committee %s." % (W.CITY, W.DEPT, W.GUIDELINE_DATE), SUB)]
    secs = [
        ("1. Purpose", [
            "1.1 The Neighborhood Stabilization Fund pays for owner-occupied and small rental rehabilitation grants, "
            "lead hazard reduction and targeted housing code enforcement support in designated neighborhoods. A "
            "round designates neighborhoods for three years; the 2027 round runs from 1 July 2027 to 30 June 2030.",
            "1.2 The Department publishes a list of candidate neighborhoods for each round, each with the 2020 census "
            "tracts that make it up. Only listed neighborhoods may be designated."]),
        ("2. Who decides", [
            "2.1 The Department recommends designations to the City Council in a memo; the Council votes on them. "
            "The Council may designate fewer neighborhoods than the Department recommends, never more."]),
        ("3. Designation", [
            "%s A candidate neighborhood is designated when at least three of its listed 2020 census tracts each "
            "meet both tests: (a) the tract's poverty rate in the American Community Survey 2019 to 2023 five-year "
            "estimates is 20.0 per cent or more; and (b) the tract's poverty rate rose from the 2014 to 2018 "
            "five-year estimates, the latest five-year release that shares no year with 2019 to 2023, by an amount "
            "statistically significant at the 90 per cent confidence level." % SECTIONS["tests"],
            "%s The poverty rate is the number of persons below the poverty level divided by the number of persons "
            "for whom poverty status is determined, in the Census Bureau's five-year detailed tables. Margins of error "
            "are the Bureau's, at the 90 per cent level. The margin of a sum of estimates is the square root of the "
            "sum of their squared margins, and the margin of a rate is the Bureau's formula for a derived proportion "
            "(its formula for a ratio where the proportion formula cannot be computed). A rise is significant when "
            "the difference between the two rates, divided by the square root of the sum of their squared standard "
            "errors (each margin divided by 1.645), is more than 1.645. For a 2020 tract whose boundaries differ from "
            "those of the 2010 tract it came from, its 2014 to 2018 rate is the rate for the area the 2020 tract "
            "covers." % SECTIONS["rate"]]),
        ("4. The recommendation memo", [
            "4.1 The memo names the neighborhoods recommended, gives each listed tract's two rates, their margins "
            "and its result on each test, and shows the tracts' changes in a chart.",
            "%s The memo also reports, for every candidate neighborhood, the residential properties with a housing "
            "code case open on 31 December 2026 and the average number of days those cases had then been open, and "
            "the rehabilitation grant dollars the Fund paid there in calendar 2026 and the number of properties they "
            "went to. A neighborhood's properties are the parcels in its listed 2020 tracts." % SECTIONS["memo"]]),
        ("5. Timeline", []),
    ]
    for h, ps in secs:
        s.append(Paragraph(h, HEAD))
        for p in ps:
            s.append(Paragraph(p, BODY))
    t = Table([["Date", "Step"], ["15 March 2027", "Candidate list and source extracts assembled"],
               ["12 April 2027", "Recommendation memo to the Council"], ["26 April 2027", "Council vote"],
               ["1 July 2027", "2027 round begins"]], colWidths=[1.4 * inch, 4.9 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9), ("FONT", (0, 1), (-1, -1), "Times-Roman", 10),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    s.append(t)
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def _sheet(ws, cols, rows, widths, fmts=None):
    ws.append(cols)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    if fmts:
        for col, f in fmts.items():
            for row in ws.iter_rows(min_row=2, min_col=col, max_col=col):
                for c in row:
                    c.number_format = f
    ws.freeze_panes = "A2"


def write_candidates(path, x):
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 candidates"
    rows = []
    ward = {"Calloway Flats": 2, "Dunmore Heights": 5, "Kestrel Park": 4, "Linden Row": 1, "Sorrel Bend": 3}
    for t in x["ts"]:
        if not t.nbhd:
            continue
        for code, _ in t.children:
            rows.append([t.nbhd, ward[t.nbhd], P.tract_name(code), W.STATE_FIPS + W.COUNTY_FIPS + code.replace(".", "")])
    rows.sort(key=lambda r: (r[0], r[3]))
    _sheet(ws, ["Neighborhood", "Council ward", "Census tract (2020)", "Tract GEOID"], rows, [20, 13, 18, 16])
    ws2 = wb.create_sheet("Notes")
    for line in ["Candidate neighborhoods for the 2027 round of the Neighborhood Stabilization Fund (guidelines 1.2).",
                 "Tracts are 2020 census tracts. A neighborhood's boundary follows its tracts' boundaries.",
                 "Prepared by the %s, 15 March 2027." % W.DEPT]:
        ws2.append([line])
    ws2.column_dimensions["A"].width = 100
    wb.save(path)


def write_journal(path, x):
    wb = Workbook()
    first = True
    by = P.journal_rows(x)
    for fy in sorted(by):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = "FY%d" % fy
        _sheet(ws, ["Entry", "Posting date", "Grant", "Parcel", "Payee", "Check", "Amount", "Reference", "Memo"],
               by[fy], [9, 12, 14, 16, 30, 9, 13, 14, 28], {2: "mm/dd/yyyy", 7: "#,##0.00;[Red]-#,##0.00"})
    wb.save(path)


def write_notes(path, x, n_parcels, n_cases, n_events):
    lines = [
        "CITY OF %s - OPEN DATA EXTRACT NOTES" % W.CITY.upper(),
        "Prepared for the %s, extract date 03/15/2027" % W.DEPT,
        "",
        "%s  (%d parcels)" % (W.FILES["parcels"], n_parcels),
        "  parcel_id          County parcel number (re-keyed by the County Assessor on 07/01/2025)",
        "  prior_parcel_id    Parcel number before the 07/01/2025 re-key",
        "  situs_address      Site address",
        "  land_use_code      Assessor land use (R1, R2, R3, RM, RC residential; C1, C2, I1, EX, VL other)",
        "  census_block_2020  2020 census block the parcel's centroid falls in (15-digit GEOID)",
        "",
        "%s  (%d cases)" % (W.FILES["cases"], n_cases),
        "  case_number        Code Enforcement case number (CEyy-nnnnn)",
        "  parcel_number      Parcel number recorded at intake (cases opened before 07/01/2025 carry the prior number)",
        "  case_type          HOUSING (housing code), NUISANCE, ZONING, BUILDING",
        "  status             OPEN or CLOSED",
        "  opened_date        Date the case was opened (MM/DD/YYYY)",
        "  closed_date        Date the case was closed (MM/DD/YYYY)",
        "",
        "%s  (%d events)" % (W.FILES["events"], n_events),
        "  case_number, event_date (YYYY-MM-DD), event, entered_by: each recorded step on a case",
        "",
        "%s" % W.FILES["payments"],
        "  One sheet per fiscal year (July 1 to June 30). Entry numbers rise with posting order.",
        "  Reference: the entry a reversal or a reissue refers to.",
    ]
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write("\n".join(lines) + "\n")
