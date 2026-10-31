"""task481 documents and workbooks: the Records Division's code values for the extract, the Return A workbooks, the
department's general order on domestic violence, the Lab's methods note for the scorecard's crime chapter, the State
UCR Program's certification letter and its 2025 agency table."""
import docx
import openpyxl
from docx.shared import Pt, RGBColor
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1c1f22")
GREY = colors.HexColor("#5d636a")
NAVY = colors.HexColor("#1f3a5f")
GREEN = colors.HexColor("#2f4f3a")
SANS = ParagraphStyle("sans", fontName="LiberationSans", fontSize=9.2, leading=12.8, textColor=INK, spaceAfter=6)
SERIF = ParagraphStyle("serif", fontName="LiberationSerif", fontSize=10.8, leading=14.6, textColor=INK, spaceAfter=8)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=7.8, leading=9.8, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=7.6, leading=9.8, textColor=GREY)


def _styles(accent, serif=False):
    face = "LiberationSerif" if serif else "LiberationSans"
    h1 = ParagraphStyle("h1", fontName=face + "-Bold", fontSize=13.5, leading=17, textColor=accent, spaceAfter=2)
    h1s = ParagraphStyle("h1s", fontName=face, fontSize=9, leading=12, textColor=GREY, spaceAfter=10)
    h2 = ParagraphStyle("h2", fontName=face + "-Bold", fontSize=10.2, leading=13.5, textColor=INK, spaceBefore=7,
                        spaceAfter=3, keepWithNext=1)
    return h1, h1s, h2


def _doc(path, title, author, footer, serif=False):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSerif" if serif else "LiberationSans", 7.4)
        canvas.drawString(0.9 * inch, 0.55 * inch, footer)
        canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.85 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, head="#e4e9ef", right=(), size=None):
    data = []
    for i, r in enumerate(rows):
        line = []
        for j, v in enumerate(r):
            st = CELLB if i == 0 else CELL
            if size:
                st = ParagraphStyle("s%d" % i, parent=st, fontSize=size, leading=size + 2)
            if i > 0 and j in right:
                st = ParagraphStyle("r", parent=st, alignment=2)
            line.append(Paragraph(str(v), st))
        data.append(line)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#a0a6ad")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head)),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 3.5)]))
    return t


def _n(v):
    return "{:,}".format(int(v))


# ------------------------------------------------------------------------------------------------ the Records Division's code values
OFFENSES = [("09A", "Murder and nonnegligent manslaughter"), ("100", "Kidnapping/abduction"), ("11A", "Rape"),
            ("11D", "Fondling"), ("120", "Robbery"), ("13A", "Aggravated assault"), ("13B", "Simple assault"),
            ("13C", "Intimidation"), ("200", "Arson"), ("220", "Burglary/breaking and entering"),
            ("23C", "Shoplifting"), ("23D", "Theft from building"), ("23F", "Theft from motor vehicle"),
            ("23G", "Theft of motor vehicle parts or accessories"), ("23H", "All other larceny"),
            ("240", "Motor vehicle theft"), ("26A", "False pretenses/swindle/confidence game"),
            ("26F", "Identity theft"), ("280", "Stolen property offenses"), ("290", "Destruction/damage/vandalism"),
            ("35A", "Drug/narcotic violations"), ("35B", "Drug equipment violations"),
            ("520", "Weapon law violations"), ("90C", "Disorderly conduct"), ("90D", "Driving under the influence"),
            ("90Z", "All other offenses")]
WEAPONS = [("11", "Firearm (type not stated)"), ("12", "Handgun"), ("13", "Rifle"), ("15", "Other firearm"),
           ("20", "Knife/cutting instrument"), ("30", "Blunt object"), ("35", "Motor vehicle/vessel"),
           ("40", "Personal weapons (hands, fists, feet, teeth)"), ("85", "Asphyxiation (drowning, strangulation, "
           "suffocation)"), ("90", "Other"), ("99", "No weapon or force")]
INJURIES = [("B", "Apparent broken bones"), ("I", "Possible internal injury"), ("L", "Severe laceration"),
            ("M", "Apparent minor injury"), ("N", "No injury"), ("O", "Other major injury"), ("T", "Loss of teeth"),
            ("U", "Unconsciousness")]
RELS = [("SE", "Spouse"), ("CS", "Common-law spouse"), ("PA", "Parent"), ("SB", "Sibling"), ("CH", "Child"),
        ("GP", "Grandparent"), ("GC", "Grandchild"), ("IL", "In-law"), ("SP", "Stepparent"), ("SC", "Stepchild"),
        ("SS", "Stepsibling"), ("OF", "Other family member"), ("BG", "Boyfriend/girlfriend"), ("XS", "Ex-spouse"),
        ("XR", "Ex-relationship (ex-boyfriend/girlfriend)"), ("CF", "Child of boyfriend/girlfriend"),
        ("AQ", "Acquaintance"), ("FR", "Friend"), ("NE", "Neighbor"), ("EE", "Employee"), ("ER", "Employer"),
        ("OK", "Otherwise known"), ("ST", "Stranger"), ("RU", "Relationship unknown")]
PLACES = [("03", "Bar/nightclub"), ("05", "Commercial/office building"), ("07", "Convenience store"),
          ("12", "Grocery/supermarket"), ("13", "Highway/road/alley/street/sidewalk"), ("14", "Hotel/motel"),
          ("18", "Parking/drop lot/garage"), ("20", "Residence/home"), ("23", "Service/gas station"),
          ("24", "Specialty store"), ("25", "Other/unknown")]


RA_LINES = [("1A", "Murder and nonnegligent homicide"), ("1B", "Manslaughter by negligence"), ("2", "Rape"),
            ("3A", "Robbery, firearm"), ("3B", "Robbery, knife or cutting instrument"),
            ("3C", "Robbery, other dangerous weapon"), ("3D", "Robbery, strong-arm (hands, fists, feet, etc.)"),
            ("4A", "Aggravated assault, firearm"), ("4B", "Aggravated assault, knife or cutting instrument"),
            ("4C", "Aggravated assault, other dangerous weapon"),
            ("4D", "Aggravated assault, hands, fists, feet, etc. (aggravated injury)"),
            ("4E", "Other assaults (simple, not aggravated)"), ("5A", "Burglary, forcible entry"),
            ("5B", "Burglary, unlawful entry (no force)"), ("5C", "Burglary, attempted forcible entry"),
            ("6", "Larceny-theft"), ("7A", "Motor vehicle theft, autos"), ("7B", "Motor vehicle theft, trucks and buses"),
            ("7C", "Motor vehicle theft, other vehicles"),
            ("NS", "Not scored on Return A under the hierarchy rule (the incident was scored under a higher offense)"),
            ("P2", "Outside the Return A lines")]


def write_codes(path):
    """The Records Division's code values for the NIBRS extract, by NIBRS data element, with the department's own
    elements after them."""
    rows = [("6", "UCR Offense Code", c, v) for c, v in OFFENSES]
    rows += [("7", "Offense Attempted/Completed", "A", "Attempted"), ("7", "Offense Attempted/Completed", "C", "Completed")]
    rows += [("9", "Location Type", c, v) for c, v in PLACES]
    rows += [("13", "Type Weapon/Force Involved", c, v) for c, v in WEAPONS]
    rows += [("25", "Type of Victim", "I", "Individual"), ("25", "Type of Victim", "B", "Business"),
             ("25", "Type of Victim", "S", "Society/public")]
    rows += [("33", "Type Injury", c, v) for c, v in INJURIES]
    rows += [("35", "Relationship of Victim to Offender", c, v) for c, v in RELS]
    rows += [("EPD-1", "Clearance", "A", "Cleared by arrest"), ("EPD-1", "Clearance", "E", "Cleared by exceptional means")]
    rows += [("EPD-2", "Return A line scored, October to December 2024", c, v) for c, v in RA_LINES]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("data_element,element_name,code,value\r\n")
        for r in rows:
            fh.write(",".join('"%s"' % x if ("," in x or '"' in x) else x for x in r) + "\r\n")
    return len(rows)


# ------------------------------------------------------------------------------------------------ the Return A workbooks
RA_ROWS = [("1A", "1a. Murder and nonnegligent homicide"), ("1B", "1b. Manslaughter by negligence"),
           ("2", "2. Rape"), ("3", "3. Robbery total"), ("3A", "a. Firearm"), ("3B", "b. Knife or cutting instrument"),
           ("3C", "c. Other dangerous weapon"), ("3D", "d. Strong-arm (hands, fists, feet, etc.)"),
           ("4", "4. Assault total"), ("4A", "a. Firearm"), ("4B", "b. Knife or cutting instrument"),
           ("4C", "c. Other dangerous weapon"), ("4D", "d. Hands, fists, feet, etc. (aggravated injury)"),
           ("4E", "e. Other assaults (simple, not aggravated)"), ("5", "5. Burglary total"),
           ("5A", "a. Forcible entry"), ("5B", "b. Unlawful entry (no force)"), ("5C", "c. Attempted forcible entry"),
           ("6", "6. Larceny-theft total"), ("7", "7. Motor vehicle theft total"), ("7A", "a. Autos"),
           ("7B", "b. Trucks and buses"), ("7C", "c. Other vehicles")]
SUBS = {"3": ("3A", "3B", "3C", "3D"), "4": ("4A", "4B", "4C", "4D", "4E"), "5": ("5A", "5B", "5C"),
        "7": ("7A", "7B", "7C")}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
THIN = Side(style="thin", color="8C939A")


def _ra_values(table, ym):
    row = table[ym]
    out = {}
    for code, _ in RA_ROWS:
        if code in SUBS:
            out[code] = [sum(row[s][i] for s in SUBS[code]) for i in range(5)]
        else:
            out[code] = row[code]
    return out


def write_return_a(path, year, table, old_layout):
    """One sheet a month. The department kept its own form until 2021; from 2022 the state program's template, with
    the columns in its order and the agency block above."""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for m in range(1, 13):
        if (year, m) not in table:
            continue
        vals = _ra_values(table, (year, m))
        ws = wb.create_sheet("%s %d" % (MONTHS[m - 1][:3], year))
        if old_layout:
            ws["A1"] = "ELLSMERE POLICE DEPARTMENT - RECORDS DIVISION"
            ws["A2"] = "RETURN A - MONTH OF %s %d" % (MONTHS[m - 1].upper(), year)
            ws["A1"].font = Font(bold=True)
            hdr = ["Classification of offenses", "Offenses reported or known", "Unfounded", "Actual offenses",
                   "Cleared (total)", "Cleared (under 18)"]
            r0 = 4
            order = [0, 1, 2, 3, 4]
        else:
            ws["A1"] = "STATE UCR PROGRAM - RETURN A: MONTHLY RETURN OF OFFENSES KNOWN TO THE POLICE"
            ws["A2"] = "Agency: Ellsmere Police Department     ORI: XX0110100     Data month: %02d/%d" % (m, year)
            ws["A3"] = ("Prepared by: Records Division" if (year, m) < (2024, 10) else
                        "Prepared by: Records Division (generated from the records management system)")
            ws["A1"].font = Font(bold=True, size=11)
            hdr = ["Line", "Classification", "Col 2: Offenses reported or known to police (incl. unfounded and "
                   "attempts)", "Col 3: Unfounded (false or baseless complaints)", "Col 4: Number of actual offenses "
                   "(col 2 minus col 3)", "Col 5: Total offenses cleared by arrest or exceptional means",
                   "Col 6: Clearances involving only persons under 18"]
            r0 = 5
            order = [0, 1, 2, 3, 4]
        for j, h in enumerate(hdr):
            c = ws.cell(row=r0, column=j + 1, value=h)
            c.font = Font(bold=True)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.fill = PatternFill("solid", fgColor="E3E8EE")
            c.border = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
        for i, (code, label) in enumerate(RA_ROWS):
            rr = r0 + 1 + i
            v = vals[code]
            if old_layout:
                cells = [label] + [v[k] for k in order]
            else:
                cells = [code if code not in SUBS else code, label] + [v[k] for k in order]
            for j, x in enumerate(cells):
                c = ws.cell(row=rr, column=j + 1, value=x)
                c.border = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
                if code in SUBS:
                    c.font = Font(bold=True)
        widths = [44, 16, 12, 14, 14, 14] if old_layout else [6, 44, 18, 18, 18, 18, 18]
        for j, w in enumerate(widths):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j + 1)].width = w
        ws.row_dimensions[r0].height = 62 if not old_layout else 32
    wb.save(path)


# ------------------------------------------------------------------------------------------------ DVU field notes
def write_order(path):
    """General Order 417, the department's order on domestic violence, as revised for the new records system."""
    h1, h1s, h2 = _styles(NAVY, serif=True)
    d, frame = _doc(path, "General Order 417: Domestic violence", W.DEPT,
                    "%s | General Order 417 | Domestic violence" % W.DEPT, serif=True)
    s = [Paragraph("General Order 417: Domestic violence", h1),
         Paragraph("%s, Office of the Chief of Police. Revised and effective 1 October 2024; supersedes the order of "
                   "4 March 2019." % W.DEPT, h1s),
         Paragraph("417.1 Purpose", h2),
         Paragraph("This order sets how the department responds to domestic incidents, how it records them and how the "
                   "Special Victims Section follows them up.", SERIF),
         Paragraph("417.2 Definitions", h2),
         Paragraph("A domestic incident is an offense between family or household members, or between current or "
                   "former intimate partners. Intimate partners are persons who are or were dating, married or living "
                   "together, or who have a child in common.", SERIF),
         Paragraph("417.3 Response", h2),
         Paragraph("The responding officer offers every victim of an intimate partner incident the lethality screen and "
                   "completes it with the victim's agreement; a victim may decline the screen. Every domestic incident "
                   "is written up as an incident report in the records system, whatever the offense.", SERIF),
         Paragraph("417.4 Referral to the Domestic Violence Unit", h2),
         Paragraph("The Records Division refers every report of a domestic incident to the Domestic Violence Unit, "
                   "whether or not a detective is assigned. The unit opens one case for each victim, numbered in the "
                   "order its cases reach it each year, and keeps against the case the incident number the report was "
                   "referred under and the offense as the Records Division classified it for the department's crime "
                   "returns.", SERIF),
         Paragraph("417.5 Case outcomes", h2),
         Paragraph("A case is closed, referred to the prosecutor, or unfounded where the investigation finds the report "
                   "false or baseless. The Records Division deletes an unfounded incident from the records system, and "
                   "it is not counted in the department's crime returns.", SERIF),
         Paragraph("417.6 Records", h2),
         Paragraph("The unit's case log is its working record of cases and outcomes. The department's published crime "
                   "counts are the Records Division's returns.", SERIF)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------ the Lab's methods note
def write_methods(path):
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)

    def para(text, bold=False, size=None, color=None, italic=False):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        if size:
            run.font.size = Pt(size)
        if color:
            run.font.color.rgb = RGBColor.from_string(color)
        return p

    para("Public Safety Scorecard, 2026 edition", bold=True, size=15, color="1F3A5F")
    para("Crime chapter: methods", bold=True, size=12, color="1F3A5F")
    para("University of Ellsmere Public Safety Lab, for the City of Ellsmere. Draft for the executive team, "
         "October 2026.", italic=True, size=9.5)
    para("1. Sources", bold=True, size=11)
    para("The chapter uses the police department's records under the data-sharing agreement of 12 February 2025: the "
         "NIBRS offense extract run on 5 October 2026, the department's Return A workbooks for 2021 to 2024, and the "
         "Domestic Violence Unit's case log; the Gun Violence Reduction Unit's shooting log and the county Medical "
         "Examiner's homicide list; and the State UCR Program's published tables and repository download for "
         "Ellsmere.")
    para("The NIBRS offense extract holds every offense the department submitted to the State UCR Program for "
         "incidents reported from 1 October 2024, when its new records system went live, to 30 September 2026, one "
         "row for each offense against each victim; an incident the department has deleted, an unfounded report or a "
         "record entered in error, is not in it. The extract stores the time each offense was reported in UTC "
         "(Ellsmere keeps Central time) and the incident's own date and hour in local time. Its incident numbers are "
         "the records system's current ones: the system's March 2025 upgrade renumbered every incident it held from "
         "EPyy-nnnnn to yyyy-nnnnnn, keeping the sequence number. For the incidents reported from October to December "
         "2024, the three months in which the Records Division produced the monthly Return A from the new system as "
         "well as the NIBRS submission, the extract also carries the Return A line each offense against each victim "
         "was scored under. The Records Division's code values for the extract come with it.")
    para("2. Aggravated assault", bold=True, size=11)
    para("From this edition the scorecard reports aggravated assault as NIBRS offense 13A: one offense for each "
         "victim, counted in the month the offense was reported to the department, in Ellsmere local time, from the "
         "department's extract. Incidents the department has deleted are not counted.")
    para("The department reported to the State UCR Program in summary form (Return A) until December 2024 and in NIBRS "
         "from January 2025. So that 2024 and 2025 measure the same thing, the chapter shows 2024 restated: the "
         "number of aggravated assault offenses NIBRS would have recorded for the victims reported to the department "
         "in 2024, had the department reported to NIBRS all year. The 2024 figure the department published from "
         "Return A is shown beside it.")
    para("3. Shootings", bold=True, size=11)
    para("The chapter counts the people struck by gunfire in an assault within the City of Ellsmere's limits, by the "
         "quarter they were shot in Ellsmere local time, and the shootings they were struck in. A shooting is one "
         "event: the people struck at the same place and time, however many there were. Self-inflicted and "
         "unintentional shootings and shootings by police officers are reported in the chapter's notes, not in these "
         "counts.")
    para("4. The State UCR Program's figures", bold=True, size=11)
    para("The State UCR Program publishes each agency's annual counts from its repository at its data freeze. Where "
         "the program's figure for Ellsmere differs from the department's own count, the chapter sets out why.")
    para("5. Presentation", bold=True, size=11)
    para("Counts are whole numbers. The 2024 restated figure is an estimate and is given to the nearest hundred, and "
         "the change from it to 2025 to the nearest whole per cent. Changes are from 2024 to 2025 unless stated.")
    doc.core_properties.title = "Crime chapter methods"
    doc.save(path)


# ------------------------------------------------------------------------------------------------ the certification letter
def write_cert(path, test):
    h1, h1s, h2 = _styles(GREEN, serif=True)
    d, frame = _doc(path, "NIBRS certification: Ellsmere Police Department", "State UCR Program",
                    "State UCR Program, Criminal Justice Information Services Bureau, Department of Public Safety.",
                    serif=True)
    s = [Paragraph("Department of Public Safety", h1),
         Paragraph("Criminal Justice Information Services Bureau - State UCR Program", h1s),
         Paragraph("January 22, 2025", SERIF),
         Paragraph("Chief of Police<br/>Ellsmere Police Department<br/>ORI XX0110100", SERIF),
         Paragraph("Re: NIBRS certification", SERIF),
         Paragraph("The Program has completed its review of the department's NIBRS test submissions for incidents "
                   "reported from October 1 to December 31, 2024, the three months for which the department also "
                   "submitted its monthly Return A. The submissions met the Program's error-rate and data-quality "
                   "standards, and the department is certified to report in NIBRS from January 1, 2025. From that "
                   "date the Program accepts NIBRS submissions only and will not accept a Return A from the "
                   "department.", SERIF),
         Paragraph("As part of the review the Program compared the test submissions with the department's Return A "
                   "for the same three months. The comparison is summarized below for the department's records.", SERIF),
         _table([("October to December 2024", "Return A, actual offenses", "NIBRS test submissions")] + test,
                [2.4 * inch, 1.9 * inch, 1.9 * inch], head="#e2e8e3", right=(1, 2)),
         Spacer(1, 10),
         Paragraph("Differences between the two are expected. NIBRS counts every offense in an incident, where Return "
                   "A counted only the highest offense under the hierarchy rule, and NIBRS classifies an assault as "
                   "aggravated when the offender used a weapon or force or the victim suffered serious injury. Agencies should not compare NIBRS counts with earlier summary counts "
                   "without allowing for these differences.", SERIF),
         Paragraph("Please direct questions to the Program's NIBRS help desk.", SERIF),
         Paragraph("Sincerely,<br/><br/>NIBRS Certification Manager<br/>State UCR Program", SERIF)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------ the state's 2025 table
def write_state_table(path, rows):
    h1, h1s, h2 = _styles(NAVY)
    d, frame = _doc(path, "Crime in the State 2025: offenses known by agency", "State UCR Program",
                    "State UCR Program. Crime in the State 2025, table 8. Published September 2026.")
    s = [Paragraph("Crime in the State, 2025", h1),
         Paragraph("Table 8. Aggravated assault offenses known to law enforcement, cities of 100,000 and over", h1s),
         _table([("Agency", "2024", "2025", "Reporting")] + rows, [2.5 * inch, 1.1 * inch, 1.1 * inch, 1.9 * inch],
                right=(1, 2)),
         Spacer(1, 8),
         Paragraph("Counts for 2025 are NIBRS aggravated assault offenses (13A), one for each victim, in incidents that "
                   "occurred in 2025, as held in the Program's repository at the 2025 data freeze (11:59 p.m. on March "
                   "13, 2026). Counts for 2024 are as reported: summary (Return A) counts of aggravated assault for "
                   "agencies marked SRS, NIBRS counts for agencies marked NIBRS. Agencies that moved from summary to "
                   "NIBRS reporting during the period are marked; their counts are not comparable across the change.",
                   SMALL),
         Paragraph("Repository downloads are available to each agency for its own records.", SMALL)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)
