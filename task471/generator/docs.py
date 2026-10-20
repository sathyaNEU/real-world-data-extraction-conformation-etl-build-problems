"""The pack's documents and workbooks: the survey's methods report, the vital and border series notes, the Commission's
campaign plan, the Office's file specification, the roll extract's dictionary and migration notes, the census workbook,
the historical deaths workbook, and the census field operations summary."""
import docx
import openpyxl
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import cm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P     # noqa: E402
import world as W    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1d1f")
GREY = colors.HexColor("#5b6067")
TEAL = colors.HexColor("#14505c")
PLUM = colors.HexColor("#4a2c5a")
SANS = ParagraphStyle("sans", fontName="LiberationSans", fontSize=9.4, leading=13.0, textColor=INK, spaceAfter=6)
SERIF = ParagraphStyle("serif", fontName="LiberationSerif", fontSize=10.6, leading=14.6, textColor=INK, spaceAfter=7)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.0, leading=10.0, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=7.8, leading=10.2, textColor=GREY)
HEAD_FILL = PatternFill("solid", fgColor="DCE3EA")


def styles(accent, serif=False):
    face = "LiberationSerif" if serif else "LiberationSans"
    h1 = ParagraphStyle("h1", fontName=face + "-Bold", fontSize=14, leading=18, textColor=accent, spaceAfter=2)
    h1s = ParagraphStyle("h1s", fontName=face, fontSize=9.2, leading=12.5, textColor=GREY, spaceAfter=10)
    h2 = ParagraphStyle("h2", fontName=face + "-Bold", fontSize=10.4, leading=14, textColor=INK, spaceBefore=7,
                        spaceAfter=3, keepWithNext=1)
    return h1, h1s, h2


def _doc(path, title, author, footer, serif=False):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSerif" if serif else "LiberationSans", 7.6)
        canvas.drawString(2.2 * cm, 1.4 * cm, footer)
        canvas.drawRightString(A4[0] - 2.2 * cm, 1.4 * cm, "%d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2.0 * cm,
                          bottomMargin=2.2 * cm, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, head="#e3e9ef", right=()):
    data = []
    for i, r in enumerate(rows):
        line = []
        for j, v in enumerate(r):
            st = CELLB if i == 0 else CELL
            if i > 0 and j in right:
                st = ParagraphStyle("r", parent=st, alignment=2)
            line.append(Paragraph(str(v), st))
        data.append(line)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head)),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


def _n(v):
    return "{:,}".format(int(v))


# ----------------------------------------------------------------------------------------------- the survey's report
def write_pes_report(path, n_mb, n_people, n_records):
    h1, h1s, h2 = styles(TEAL)
    d, frame = _doc(path, "2025 Post-Enumeration Survey: design, fieldwork and files", W.OFFICE,
                    "%s, %s. 2025 Post-Enumeration Survey methods report." % (W.OFFICE, W.DIVISION))
    S = []
    S.append(Paragraph("2025 Post-Enumeration Survey", h1))
    S.append(Paragraph("Design, fieldwork and files. %s, %s. Methods report, September 2025." % (W.OFFICE, W.DIVISION), h1s))
    S.append(Paragraph("1. Purpose", h2))
    S.append(Paragraph(
        "The Post-Enumeration Survey (PES) measures how completely the 2025 Census of Population and Dwellings counted "
        "the people usually resident in the country on census day, Tuesday 4 March 2025: the people the census missed, "
        "and the census records that should not have been counted.", SANS))
    S.append(Paragraph("2. Sample", h2))
    S.append(Paragraph(
        "The survey covered every dwelling in a sample of meshblocks: one meshblock in 30 in every region, taken "
        "systematically from a random start down the region's meshblock list (2025 boundaries), so that every meshblock "
        "in a region had the same chance of selection. Communal dwellings in a sampled meshblock (hostels, care homes, "
        "camps and the like) were covered with the private dwellings. %s meshblocks were sampled; "
        "pes_2025_sampled_meshblocks.csv lists them with the dwellings and people the survey listed in each and the "
        "visits it took to complete them." % _n(n_mb), SANS))
    S.append(Paragraph("3. Fieldwork and matching", h2))
    S.append(Paragraph(
        "3.1 Interviewers who had not worked on the census listed every dwelling in the sampled meshblocks between 7 "
        "April and 27 June 2025 and recorded every person usually resident in each on census day, including people "
        "who had moved out since. The survey's staff, listings and fieldwork systems were kept separate from the "
        "census's throughout.", SANS))
    S.append(Paragraph(
        "3.2 Each person the survey recorded was searched for among the census records for the meshblock and the "
        "meshblocks around it. In pes_2025_people.csv MATCH is M where the person was found, with CENSUS_RECORD giving "
        "the census record, and N where the person had no census record. Every case was resolved, by a follow-up visit "
        "where the interview left doubt; none is left unresolved. The file holds %s people." % _n(n_people), SANS))
    S.append(Paragraph(
        "3.3 The census records for the sampled meshblocks were checked against the survey's listing and follow-up. "
        "pes_2025_census_records.csv holds every census record for the sampled meshblocks (%s) except the records the "
        "census imputed for dwellings it could not contact, which name no one to check. STATUS is one of:"
        % _n(n_records), SANS))
    S.append(_table([
        ["STATUS", "Meaning"],
        ["C", "counted correctly: usually resident in the meshblock on census day"],
        ["D", "counted twice: the person was also counted at another address"],
        ["V", "not usually resident in the country (a visitor counted as a resident)"],
        ["O", "out of scope: born after census day or died before it"],
        ["W", "usually resident outside the meshblock and the meshblocks around it"],
    ], [2.0 * cm, 13.6 * cm]))
    S.append(Spacer(1, 6))
    S.append(Paragraph("4. Estimation cells", h2))
    S.append(Paragraph(
        "The survey's results are produced for estimation cells: region by sex by age group, the age groups being 0 to "
        "14, 15 to 17, 18 to 24, 25 to 34, 35 to 49, 50 to 64, and 65 and over. Ages in both files are completed years "
        "at census day.", SANS))
    S.append(Paragraph("5. Files", h2))
    S.append(_table([
        ["File", "One row is"],
        ["pes_2025_people.csv", "a person the survey recorded as usually resident in a sampled meshblock on census day"],
        ["pes_2025_census_records.csv", "a census record for a sampled meshblock, imputed records excepted"],
        ["pes_2025_sampled_meshblocks.csv", "a sampled meshblock"],
    ], [5.6 * cm, 10.0 * cm]))
    S.append(Spacer(1, 6))
    S.append(Paragraph(
        "Region codes are those of the census tables. Meshblock codes begin with the region code. The census's counts "
        "for every region, by sex and single year of age, are in census_2025_usual_residents_by_region.xlsx.", SMALL))
    d.build(S, onFirstPage=frame, onLaterPages=frame)


# ----------------------------------------------------------------------------------------------- the series notes
def write_series_notes(path):
    h1, h1s, h2 = styles(TEAL)
    d, frame = _doc(path, "Vital and border series: notes", W.OFFICE,
                    "%s. Vital and border series, notes for users." % W.OFFICE)
    S = []
    S.append(Paragraph("Vital and border series", h1))
    S.append(Paragraph("Notes for users. %s, population statistics. Updated 14 April 2025." % W.OFFICE, h1s))
    for head, text in (
        ("Live births", "Live births registered in the country, by sex and by the year in which the birth took place, "
         "from 1925. Registration of births has been compulsory since 1912 and is complete. File: "
         "live_births_by_sex_1925_2025.csv."),
        ("Deaths", "Deaths registered in the country, by sex, the year of death and the year of birth on the death "
         "registration. Deaths from 1925 to 1990 are in the historical workbook deaths_by_year_of_birth_1925_1990.xlsx "
         "(a sheet for each sex, one row a year of death and one column a year of birth); deaths from 1991 are in "
         "deaths_by_year_of_birth_1991_2025.csv."),
        ("Long-term movements", "Arrivals of people coming to live in the country for 12 months or more, and departures "
         "of residents leaving it for 12 months or more, by sex, period and year of birth, from 1950. Every traveller "
         "is recorded at the border: the country's only ports of entry are its four international airports and two "
         "seaports, and arrival and departure records are kept for every passenger and crew member. File: "
         "long_term_movements_by_year_of_birth_1950_2025.csv."),
        ("The 2025 period", "Each series carries a provisional period for 2025, written 2025-01-01/2025-03-03: 1 January "
         "to 3 March 2025, the day before the 2025 census. Births in that period are registrations by 14 April 2025; "
         "a few late registrations will be added."),
        ("Year of birth", "Taken from the registered date of birth; a death or movement record without one is assigned "
         "from the age recorded."),
    ):
        S.append(Paragraph(head, h2))
        S.append(Paragraph(text, SANS))
    d.build(S, onFirstPage=frame, onLaterPages=frame)


# ----------------------------------------------------------------------------------------------- the campaign plan
def write_plan(path):
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    t = doc.add_paragraph()
    r = t.add_run("Electoral Commission")
    r.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x4A, 0x2C, 0x5A)
    h = doc.add_paragraph()
    r = h.add_run("2027 Enrolment Campaign: field plan")
    r.bold = True
    r.font.size = Pt(16)
    doc.add_paragraph("Enrolment and Outreach. Approved by the Commission on 22 September 2026.")
    sections = [
        ("1. Purpose", [
            "The campaign enrols the people who are entitled to vote but are not on the roll, ahead of the 2027 general "
            "election. Its field organisers work in the regions through 2027, alongside the national advertising and the "
            "online channel."]),
        ("2. Who is counted", [
            "2.1 A region's adults are the people aged 18 or over usually resident in the region on census day, 4 March "
            "2025, whether or not the census counted them.",
            "2.2 A region's electors are the electors on the roll at the close of census day with a residential address "
            "in the region. Overseas electors are not counted in any region.",
            "2.3 A region's adults not on the roll are its adults less its electors."]),
        ("3. Organisers", [
            "3.1 The campaign's 200 field organisers are shared among the 16 regions in proportion to their adults not "
            "on the roll, by largest remainders: each region takes the whole number in its share, and the organisers "
            "left over go one each to the regions with the largest fractions. Every region has at least two: a region "
            "whose share is under two takes two, and the rest are shared again among the other regions in the same "
            "way.",
            "3.2 The National Statistics Office supplies each region's adults and the Commission its electors, both "
            "in the Office's enrolment-gap file."]),
        ("4. Timetable", [
            "Organisers are recruited in the last quarter of 2026 and start on 1 February 2027. The allocation is "
            "reviewed only if a region's organisers cannot be recruited."]),
        ("5. Monitoring", [
            "The Commission's monthly reports set each region's organisers beside the roll's movement in the region "
            "since census day, as the enrolment-gap file gives it to 30 June 2026: the people added to the roll who had "
            "not been on it on census day, and the electors removed because they had died."]),
    ]
    for head, paras in sections:
        p = doc.add_paragraph()
        rr = p.add_run(head)
        rr.bold = True
        rr.font.size = Pt(11.5)
        for tx in paras:
            q = doc.add_paragraph(tx)
            q.alignment = WD_ALIGN_PARAGRAPH.LEFT
    doc.add_paragraph("Contact: %s, Enrolment and Outreach Manager." % W.PEOPLE["commission"])
    doc.core_properties.title = "2027 Enrolment Campaign: field plan"
    doc.save(path)


# ----------------------------------------------------------------------------------------------- the workbooks
def _head(ws, cols, widths, row=1):
    for i, c in enumerate(cols):
        cell = ws.cell(row=row, column=i + 1, value=c)
        cell.font = Font(bold=True)
        cell.fill = HEAD_FILL
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = widths[i]


def write_spec(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "File layout"
    ws["A1"] = "Enrolment-gap file for the Electoral Commission: layout"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "%s, %s. Version 1.2, 30 September 2026." % (W.OFFICE, W.DIVISION)
    _head(ws, ["Column", "Content", "Format"], [18, 92, 26], row=4)
    rows = [
        ("REGION_CODE", "Region code, as in the census tables", "two digits"),
        ("REGION", "Region name", "text"),
        ("ORGANISERS", "The region's campaign organisers under the Commission's field plan, section 3", "whole number"),
        ("NEW_ELECTORS", "People added to the roll in the region in the reporting period who were not on the roll at "
                         "the close of census day (definitions 3)", "whole number"),
        ("REMOVED_DIED", "Electors removed from the roll in the region in the reporting period because they had died "
                         "(definitions 4)", "whole number"),
    ]
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            ws.cell(row=5 + i, column=j + 1, value=v).alignment = Alignment(vertical="top", wrap_text=True)
    ws2 = wb.create_sheet("Definitions")
    ws2.column_dimensions["A"].width = 8
    ws2.column_dimensions["B"].width = 120
    defs = [
        ("1", "One row a region, 16 rows, in region code order, comma-separated with a header row."),
        ("2", "Dates and times are the country's time. The reporting period runs from the close of census day, 4 March "
              "2025, to the end of 30 June 2026."),
        ("3", "NEW_ELECTORS counts the people added to the roll in the reporting period who were not on the roll at the "
              "close of census day, each person once, in the region of the residential address they enrolled at. "
              "Enrolments with an overseas address are not counted in any region."),
        ("4", "REMOVED_DIED counts the electors removed from the roll in the reporting period because they had died, "
              "in the region of the address they were removed from. A removal later reversed was not a removal."),
        ("5", "Counts are whole people. Organisers are whole organisers."),
    ]
    for i, (k, v) in enumerate(defs):
        ws2.cell(row=1 + i, column=1, value=k)
        c = ws2.cell(row=1 + i, column=2, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def write_dictionary(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Columns"
    ws["A1"] = "Roll transactions extract: data dictionary"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Electoral Commission, Data Services. The extract holds the enrolments, removals and reinstatements "
                "processed from census day (4 March 2025) to 30 June 2026. Changes of name or address are not included.")
    _head(ws, ["Column", "Description"], [16, 100], row=4)
    cols = [
        ("TXN_ID", "The transaction's identifier"),
        ("PROCESSED", "When the platform processed the transaction (date and time)"),
        ("TXN_TYPE", "NEW an enrolment; DEL a removal from the roll; REI the reinstatement of a removed elector"),
        ("REASON", "A removal's reason (Codes)"),
        ("SOURCE", "An enrolment's channel (Codes)"),
        ("STATUS", "A accepted; R rejected (an application that did not result in an enrolment)"),
        ("ELECTOR_NO", "The elector number; blank on a rejected application"),
        ("PERSON_REF", "The Commission's reference for the person"),
        ("ELECTORATE", "The electorate of the address enrolled at or removed from (electorate code)"),
        ("ADDRESS_TYPE", "R residential address; O overseas address"),
        ("SEX", "M or F"),
        ("BIRTH_YEAR", "Year of birth"),
        ("REF_TXN", "On a reinstatement, the TXN_ID of the removal it reverses"),
    ]
    for i, (k, v) in enumerate(cols):
        ws.cell(row=5 + i, column=1, value=k)
        ws.cell(row=5 + i, column=2, value=v).alignment = Alignment(wrap_text=True)
    ws2 = wb.create_sheet("Codes")
    _head(ws2, ["Column", "Code", "Meaning"], [12, 8, 80])
    codes = [
        ("REASON", "01", "Removed at the elector's own request"),
        ("REASON", "02", "Overseas for more than three years"),
        ("REASON", "03", "Duplicate record"),
        ("REASON", "04", "Objection upheld"),
        ("REASON", "11", "Deceased: matched to a death registration"),
        ("REASON", "12", "Deceased: notified by family or a funeral director"),
        ("SOURCE", "ONL", "Online enrolment"),
        ("SOURCE", "PAP", "Paper enrolment form"),
        ("SOURCE", "PRV", "Provisional enrolment transferred to the roll at 18"),
        ("SOURCE", "CAM", "Enrolment taken at a campaign event"),
    ]
    for i, r in enumerate(codes):
        for j, v in enumerate(r):
            ws2.cell(row=2 + i, column=j + 1, value=v)
    wb.save(path)


def write_census_workbook(path, table):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Contents"
    ws["A1"] = "2025 Census of Population and Dwellings"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Usual residents by region, sex and single year of age. Census day: Tuesday 4 March 2025."
    ws["A3"] = "%s. Released 18 November 2025." % W.OFFICE
    ws["A5"] = "Sheet"
    ws["B5"] = "Region"
    ws["A5"].font = ws["B5"].font = Font(bold=True)
    for i, c in enumerate(W.CODES):
        ws.cell(row=6 + i, column=1, value="%s %s" % (c, W.NAME[c]))
        ws.cell(row=6 + i, column=2, value=W.NAME[c])
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 22
    notes = wb.create_sheet("Notes")
    notes.column_dimensions["A"].width = 6
    notes.column_dimensions["B"].width = 110
    for i, tx in enumerate((
            "Counts are of the people usually resident in each region on census day, by the region of their usual "
            "residence.",
            "Counts include the people the census imputed for dwellings it found occupied but could not contact; they "
            "are shown again in the 'of which imputed' columns.",
            "Age is the completed years at census day. The row 100 holds the people aged 100 and over.",
            "Region codes are used throughout the Office's census and survey files.")):
        notes.cell(row=1 + i, column=1, value=i + 1)
        notes.cell(row=1 + i, column=2, value=tx).alignment = Alignment(wrap_text=True)
    for c in W.CODES:
        sh = wb.create_sheet("%s %s" % (c, W.NAME[c]))
        sh["A1"] = "%s (%s): usual residents on census day, 4 March 2025" % (W.NAME[c], c)
        sh["A1"].font = Font(bold=True)
        sh["A2"] = "2025 Census of Population and Dwellings"
        _head(sh, ["Age", "Males", "Males, of which imputed", "Females", "Females, of which imputed", "Total"],
              [8, 12, 14, 12, 14, 12], row=4)
        tm = tf = 0
        for a in range(0, 101):
            m, mi = table[(c, "M", a)]
            f, fi = table[(c, "F", a)]
            tm += m
            tf += f
            row = 5 + a
            sh.cell(row=row, column=1, value=("100 and over" if a == 100 else a))
            for j, v in enumerate((m, mi, f, fi, m + f)):
                sh.cell(row=row, column=2 + j, value=int(v))
        sh.cell(row=107, column=1, value="Total").font = Font(bold=True)
        sh.cell(row=107, column=2, value=int(tm))
        sh.cell(row=107, column=4, value=int(tf))
        sh.cell(row=107, column=6, value=int(tm + tf))
        sh["A109"] = "See Notes for the counts and the imputed records."
        sh.freeze_panes = "B5"
    wb.save(path)


def write_deaths_history(path, cells):
    wb = openpyxl.Workbook()
    first = True
    for sex, title in (("M", "Males"), ("F", "Females")):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = title
        ws["A1"] = "Deaths registered, 1925 to 1990, by year of death and year of birth: %s" % title.lower()
        ws["A1"].font = Font(bold=True)
        ws["A2"] = "%s, vital statistics (historical series)" % W.OFFICE
        ws.cell(row=4, column=1, value="Year of death").font = Font(bold=True)
        for j, c in enumerate(range(1925, 1991)):
            ws.cell(row=4, column=2 + j, value=c).font = Font(bold=True)
        for i, y in enumerate(range(1925, 1991)):
            ws.cell(row=5 + i, column=1, value=y)
            for j, c in enumerate(range(1925, 1991)):
                v = cells.get((y, sex, c))
                if v:
                    ws.cell(row=5 + i, column=2 + j, value=int(v))
        ws.freeze_panes = "B5"
    wb.save(path)


# ----------------------------------------------------------------------------------------------- migration notes
def write_migration(path):
    h1, h1s, h2 = styles(PLUM)
    d, frame = _doc(path, "Roll platform migration: notes for data users", W.COMMISSION,
                    "Electoral Commission, Data Services. Roll platform migration notes.")
    S = []
    S.append(Paragraph("Roll platform migration", h1))
    S.append(Paragraph("Notes for users of roll extracts. Electoral Commission, Data Services. 9 September 2025.", h1s))
    for head, text in (
        ("The move", "On Monday 4 August 2025 the roll moved from the platform the Commission had run since 2004 to its "
         "new roll platform. Enrolment by every channel continued without a break; provisional enrolments now move to "
         "the roll on the day the person turns 18 rather than at the start of the next month, and the death "
         "registration match runs weekly rather than monthly."),
        ("Identifiers", "Transactions processed by the old platform carry its running numbers (R25- followed by seven "
         "digits); those processed by the new platform carry its 16-character keys. Person references and elector "
         "numbers were carried over unchanged, and electorate codes are those of the 2024 boundary review."),
        ("Removal reasons before 4 August 2025", "Removals processed by the old platform carry its reason codes: 01 "
         "deceased; 02 overseas for more than three years; 03 duplicate record; 04 objection upheld; 05 moved out of "
         "the electorate. The new platform's codes are in the data dictionary."),
        ("Extracts", "Extracts are produced by Data Services on request, as comma-separated files with a header row, in "
         "the order the platforms processed the transactions."),
    ):
        S.append(Paragraph(head, h2))
        S.append(Paragraph(text, SANS))
    d.build(S, onFirstPage=frame, onLaterPages=frame)


# ----------------------------------------------------------------------------------------------- field operations
def write_field_ops(path, rows):
    h1, h1s, h2 = styles(TEAL)
    d, frame = _doc(path, "2025 Census: field operations summary", W.OFFICE,
                    "%s. 2025 Census field operations summary." % W.OFFICE)
    S = []
    S.append(Paragraph("2025 Census: field operations summary", h1))
    S.append(Paragraph("%s, census field operations. July 2025." % W.OFFICE, h1s))
    S.append(Paragraph(
        "Census day was Tuesday 4 March 2025. Households could respond online from 17 February; paper forms went to "
        "the dwellings that asked for them and to every dwelling still without a response by 14 March, and field "
        "staff then visited non-responding dwellings up to six times until 30 April. Dwellings found occupied that "
        "could not be contacted had their residents imputed.", SANS))
    S.append(Paragraph("Response by region", h2))
    tab = [["Region", "Dwellings", "Online", "Paper", "Field visit", "Imputed"]]
    for r in rows:
        tab.append(list(r))
    S.append(_table(tab, [3.6 * cm, 2.4 * cm, 2.2 * cm, 2.2 * cm, 2.4 * cm, 2.2 * cm], right=(1, 2, 3, 4, 5)))
    S.append(Spacer(1, 6))
    S.append(Paragraph(
        "Online, paper and field visit give the share of responding dwellings by the way they responded; imputed "
        "gives the share of occupied dwellings with residents imputed. Staff: 11,860 enumerators and 1,214 field "
        "supervisors at the peak.", SMALL))
    d.build(S, onFirstPage=frame, onLaterPages=frame)
