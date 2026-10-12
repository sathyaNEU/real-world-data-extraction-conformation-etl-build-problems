"""The pack's documents: the department's planning standard PS-07, the regional immunisation office's options paper,
the national planning unit's circular on local health office areas, the national guidelines' MMR chapter excerpt, the
national quarterly uptake report, the register data manager's extract notes and the case export's field notes."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.pagesizes import A4                                     # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import mm                                         # noqa: E402
from reportlab.pdfbase import pdfmetrics                                   # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                               # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LiberationSans", FONT_DIR + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans-Bold", FONT_DIR + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSerif", FONT_DIR + "LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSerif-Bold", FONT_DIR + "LiberationSerif-Bold.ttf"))
SANS, SANS_B, SERIF, SERIF_B = "LiberationSans", "LiberationSans-Bold", "LiberationSerif", "LiberationSerif-Bold"
INK = colors.HexColor("#1d2329")
GREY = colors.HexColor("#5b6670")
TEAL = colors.HexColor("#0b5f63")
RULE = colors.HexColor("#9aa6ad")


def _styles(font, bold, size=10.2, accent=INK):
    body = ParagraphStyle("b", fontName=font, fontSize=size, leading=size * 1.36, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        num=ParagraphStyle("n", parent=body, leftIndent=26, firstLineIndent=-26),
        h1=ParagraphStyle("h1", fontName=bold, fontSize=size + 5, leading=size + 9, textColor=accent, spaceAfter=4),
        h2=ParagraphStyle("h2", fontName=bold, fontSize=size + 1, leading=size + 5, textColor=accent, spaceBefore=7,
                          spaceAfter=3),
        small=ParagraphStyle("s", fontName=font, fontSize=size - 1.6, leading=(size - 1.6) * 1.35, textColor=GREY,
                             spaceAfter=3),
        cell=ParagraphStyle("c", fontName=font, fontSize=size - 1.4, leading=(size - 1.4) * 1.25, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=bold, fontSize=size - 1.9, leading=(size - 1.9) * 1.25, textColor=INK),
    )


def _doc(path, title, author, subject, footer):
    def page(canvas, doc):
        canvas.saveState()
        canvas.setFont(SANS, 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(18 * mm, 10 * mm, footer)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                          bottomMargin=18 * mm, title=title, author=author, subject=subject, creator=author,
                          producer=W.REGION)
    return d, page


def _table(rows, widths, st, header_rows=1, align_right_from=None, zebra=False):
    data = []
    for i, r in enumerate(rows):
        data.append([Paragraph(str(c), st["cellb"] if i < header_rows else st["cell"]) for c in r])
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=header_rows)
    style = [("LINEBELOW", (0, header_rows - 1), (-1, header_rows - 1), 0.6, RULE),
             ("LINEBELOW", (0, -1), (-1, -1), 0.4, RULE),
             ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.2),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2), ("LEFTPADDING", (0, 0), (-1, -1), 3),
             ("RIGHTPADDING", (0, 0), (-1, -1), 3)]
    if zebra:
        for i in range(header_rows, len(rows)):
            if (i - header_rows) % 2 == 1:
                style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f1f4f5")))
    t.setStyle(TableStyle(style))
    return t


# ----------------------------------------------------------------------------------------------------------------
def standard(path):
    st = _styles(SERIF, SERIF_B, 10.4, TEAL)
    d, page = _doc(path, "PS-07 Measles winter planning standard", W.PEOPLE["director"],
                   "Planning standard", "%s | PS-07 Measles winter planning standard | version 3.0" % W.DEPT)
    P = lambda t: Paragraph(t, st["num"])
    s = [Paragraph(W.DEPT.upper(), st["small"]),
         Paragraph("PS-07 Measles winter planning standard", st["h1"]),
         _table([["Version", "Approved", "Owner", "Review"],
                 ["3.0", "10 March 2026", "%s, Director of Public Health" % W.PEOPLE["director"], "March 2028"]],
                [22, 34, 80, 30], st),
         Spacer(1, 6),
         Paragraph("1 Purpose and scope", st["h2"]),
         P("1.1&nbsp;&nbsp;This standard sets how the department decides each year, before the measles season, whether "
           "to fund a catch-up MMR campaign and, if so, which one."),
         P("1.2&nbsp;&nbsp;It applies to the autumn campaign and to the winter that follows it. Routine childhood "
           "immunisation and outbreak control are covered by PS-02 and PS-05."),
         Paragraph("2 Roles", st["h2"]),
         P("2.1&nbsp;&nbsp;The regional immunisation manager prepares an options paper by 30 June, setting out the "
           "catch-up options the office can deliver between September and November, the people in each option's "
           "birth cohorts and the number of people each option is expected to make immune."),
         P("2.2&nbsp;&nbsp;The director of public health makes the winter assessment in section 3 and recommends an "
           "option, or none, to the executive management team, which funds at most one catch-up a year."),
         Paragraph("3 The winter assessment", st["h2"]),
         P("3.1&nbsp;&nbsp;The department's aim is that measles cannot sustain transmission in the region through the "
           "winter: the reproduction number, with the year's programme in place, is below one."),
         P("3.2&nbsp;&nbsp;The department plans on a basic reproduction number (R0) of 15 for measles: the "
           "reproduction number measles would have in the region if nobody in it were immune."),
         P("3.3&nbsp;&nbsp;The winter is assessed on the region's population and immunity on 1 January of the winter's "
           "second year, using the department's projection of the region's usual residents for that date."),
         P("3.4&nbsp;&nbsp;Immunity by year of birth is taken from the national immunisation programme's latest measles "
           "immunity profile for the region, which projects each year of birth to the assessment date."),
         P("3.5&nbsp;&nbsp;A catch-up option counts for the people the options paper expects it to make immune."),
         P("3.6&nbsp;&nbsp;If the reproduction number without a catch-up is below one, the department runs none. "
           "Otherwise it funds an option that brings the reproduction number below one; where more than one does, "
           "the one with the lowest cost; where none does, the option that brings it lowest, and the director reports "
           "the shortfall to the national immunisation programme."),
         Paragraph("4 Timetable", st["h2"]),
         _table([["Step", "By"],
                 ["Options paper to the director", "30 June"],
                 ["Winter assessment and recommendation to the executive management team", "July meeting"],
                 ["Catch-up delivered", "September to November"],
                 ["Report on uptake to the director", "15 December"]], [120, 46], st),
         Paragraph("5 Records", st["h2"]),
         P("5.1&nbsp;&nbsp;The options paper, the winter assessment, the recommendation and the executive management "
           "team's decision are kept on the year's file for seven years."),
         Spacer(1, 8),
         Paragraph("Supersedes version 2.1 (February 2023). Changes in 3.0: the options paper deadline moved from 31 "
                   "July to 30 June; section 3.6 adds the report to the national immunisation programme.", st["small"])]
    d.build(s, onFirstPage=page, onLaterPages=page)


def options(path, opts, reg_people):
    st = _styles(SANS, SANS_B, 9.6, TEAL)
    d, page = _doc(path, "Autumn 2027 MMR catch-up: options", W.PEOPLE["manager"], "Options paper",
                   "%s | Autumn 2027 MMR catch-up: options | 9 June 2027" % W.RIO)
    P = lambda t: Paragraph(t, st["num"])
    rows = [["Option", "Born", "Age on 1 Jan 2028", "Delivered through", "People", "Estimated susceptible",
             "Expected uptake", "Expected made immune", "Cost (EUR)"]]
    for k in W.OPTION_KEYS:
        o = W.OPTIONS[k]
        parts = opts[k]
        if k != "E":
            p = parts[0]
            a, b = p["years"]
            rows.append([k, "%d to %d" % (a, b), "%d to %d" % (2027 - b, 2027 - a), o["setting"], "{:,}".format(p["people"]),
                         "{:,}".format(p["susceptible"]), "%d%%" % round(o["uptake"] * 100), "{:,}".format(p["made"]),
                         "{:,}".format(o["cost"])])
        else:
            for i, p in enumerate(parts):
                a, b = p["years"]
                rows.append(["E" if i == 0 else "", "%d to %d" % (a, b), "%d to %d" % (2027 - b, 2027 - a),
                             o["setting"] if i == 0 else "", "{:,}".format(p["people"]), "{:,}".format(p["susceptible"]),
                             "%d%%" % round(o["uptake"] * 100), "{:,}".format(p["made"]), ""])
            rows.append(["", "1993 to 2002", "25 to 34", "Option E in total", "{:,}".format(sum(p["people"] for p in parts)),
                         "{:,}".format(sum(p["susceptible"] for p in parts)), "", "{:,}".format(sum(p["made"] for p in parts)),
                         "{:,}".format(o["cost"])])
    s = [Paragraph(W.RIO.upper(), st["small"]),
         Paragraph("Autumn 2027 MMR catch-up: options", st["h1"]),
         Paragraph("For the Director of Public Health. Prepared by %s, Regional Immunisation Manager, 9 June 2027."
                   % W.PEOPLE["manager"], st["small"]),
         Paragraph("1 Purpose", st["h2"]),
         P("1.1&nbsp;&nbsp;Under PS-07 (2.1) this paper sets out the catch-up options the office can deliver between "
           "September and November 2027, the people in each option's birth cohorts and the people each is expected to "
           "make immune. The executive management team meets on 21 July 2027 and can fund one."),
         Paragraph("2 Background", st["h2"]),
         P("2.1&nbsp;&nbsp;On 2 April 2027 a man with measles acquired abroad attended a GP surgery and the emergency "
           "department in Navan before he was diagnosed. Two adults who were in the department that afternoon became "
           "ill on 15 and 17 April. The director asked for catch-up options the same week."),
         P("2.2&nbsp;&nbsp;The options cover the birth cohorts outside the routine programme with the largest immunity "
           "gaps in the national profile (May 2027): the children born 2008 to 2012, whose MMR uptake fell during the "
           "2010-12 vaccine scare; the children born 2013 to 2017; the young adults born 2003 to 2007; and the adults "
           "born 1993 to 2002, who were at school before the second dose moved to junior infants."),
         P("2.3&nbsp;&nbsp;Each option is costed at the office's 2027 rates for the delivery route shown. The budget "
           "allocated for an autumn catch-up is EUR 470,000, so every option is affordable and only one can run."),
         Paragraph("3 Options", st["h2"]),
         _table(rows, [12, 21, 15, 37, 15, 18, 17, 17, 17], st, zebra=True),
         Spacer(1, 3),
         Paragraph("People: the department's projection of usual residents at 1 January 2028 for those years of birth. "
                   "Estimated susceptible: those people less the immune share the national profile gives for each year "
                   "of birth. Expected people made immune: susceptible people expected to become immune (estimated "
                   "susceptible x expected uptake among the susceptible x 0.97, the effectiveness of a catch-up course), "
                   "to the nearest ten; doses given to people already immune do not count. Cost: vaccine, staff, venues "
                   "and invitations.", st["small"]),
         Paragraph("4 Delivery", st["h2"]),
         P("4.1&nbsp;&nbsp;Options A and B use the school immunisation team's autumn sessions; the team can add catch-up "
           "sessions in 61 primary and 38 post-primary schools between 15 September and 20 November. Further education "
           "colleges and school leavers in option B are reached through the colleges and by GP letter."),
         P("4.2&nbsp;&nbsp;Option C runs clinics on the three third-level campuses in Freshers' weeks and invites the rest "
           "by GP letter. Options D and E invite by letter and text message through GP practices and pharmacies, and E "
           "adds workplace clinics at the four largest employers."),
         P("4.3&nbsp;&nbsp;Invitation lists come from the regional immunisation register; people not on it are reached "
           "through schools, colleges, practices and employers."),
         Paragraph("5 Next step", st["h2"]),
         P("5.1&nbsp;&nbsp;The director's winter assessment under PS-07 section 3, and the recommendation to the "
           "executive management team.")]
    d.build(s, onFirstPage=page, onLaterPages=page)


def circular(path):
    st = _styles(SANS, SANS_B, 9.8, colors.HexColor("#283c6b"))
    d, page = _doc(path, "Local health office areas: revision of 1 July 2024", "National health service planning unit",
                   "Circular 03/2024", "National health service planning unit | Circular 03/2024")
    P = lambda t: Paragraph(t, st["num"])
    s = [Paragraph("NATIONAL HEALTH SERVICE PLANNING UNIT", st["small"]),
         Paragraph("Circular 03/2024: Local health office areas, revision of 1 July 2024", st["h1"]),
         Paragraph("12 April 2024. To: health regions, national and regional registers, information services.", st["small"]),
         Paragraph("1 The revision", st["h2"]),
         P("1.1&nbsp;&nbsp;Following the 2023 review of local health office boundaries, the areas and codes below change "
           "on 1 July 2024. All other areas and codes are unchanged."),
         P("1.2&nbsp;&nbsp;The full list of areas and codes in force from 1 July 2024 is published with this circular."),
         Paragraph("2 Changes", st["h2"]),
         _table([["Area before 1 July 2024", "From 1 July 2024", "Health region"],
                 ["LH26 Monaghan East", "LH26 Monaghan (Monaghan East and Monaghan West together)", W.REGION],
                 ["LH27 Monaghan West", "Merged into LH26 Monaghan", W.REGION],
                 ["LH31 Laois (Portlaoise town and hinterland)", "New area LH27 Portlaoise", "Midlands"],
                 ["LH31 Laois (the rest)", "LH31 Laois", "Midlands"],
                 ["LH11 Longford/Westmeath", "LH11 Longford and Westmeath (name only)", "Midlands"],
                 ["LH09 Kildare North and LH10 Kildare South", "Three electoral divisions move from LH10 to LH09 (annex)",
                  "Midlands"]], [56, 74, 36], st),
         Paragraph("3 Annex: electoral divisions moving between areas", st["h2"]),
         _table([["Electoral division", "From", "To"],
                 ["Maynooth (part)", "LH10", "LH09"], ["Kilcock", "LH10", "LH09"], ["Donadea", "LH10", "LH09"],
                 ["Portlaoise Urban", "LH31", "LH27"], ["Portlaoise Rural", "LH31", "LH27"], ["Maryborough", "LH31", "LH27"],
                 ["Clones Urban", "LH27", "LH26"], ["Clones Rural", "LH27", "LH26"], ["Carrickmacross Urban", "LH27", "LH26"],
                 ["Carrickmacross Rural", "LH27", "LH26"], ["Castleblayney Rural", "LH27", "LH26"]], [70, 30, 30], st),
         Spacer(1, 6),
         Paragraph("Queries to the planning unit's geography team.", st["small"])]
    d.build(s, onFirstPage=page, onLaterPages=page)


def guidelines(path):
    st = _styles(SERIF, SERIF_B, 10.2, colors.HexColor("#5a2a5f"))
    d, page = _doc(path, "Immunisation guidelines chapter 12: measles, mumps and rubella (excerpt)",
                   "National immunisation programme", "Guidelines", "National immunisation guidelines | Chapter 12 "
                   "Measles, mumps and rubella | revised November 2025")
    P = lambda t: Paragraph(t, st["num"])
    s = [Paragraph("NATIONAL IMMUNISATION GUIDELINES", st["small"]),
         Paragraph("Chapter 12. Measles, mumps and rubella (MMR): sections 12.4 to 12.6", st["h1"]),
         Paragraph("Revised November 2025. Sections 12.1 to 12.3 (the diseases) and 12.7 to 12.9 (adverse events, "
                   "contraindications, outbreak control) are not reproduced.", st["small"]),
         Paragraph("12.4 Schedule", st["h2"]),
         P("12.4.1&nbsp;&nbsp;Two doses of MMR vaccine are given: the first at 12 months of age by the child's GP, the "
           "second at 4 to 5 years (junior infants) by the school immunisation team."),
         P("12.4.2&nbsp;&nbsp;MMR was introduced in 1988 at 15 months. A second dose was added in 1992 at 10 to 14 "
           "years and moved to 4 to 5 years from 1999. The first dose moved to 12 months for children born from 2008."),
         Paragraph("12.5 Valid doses", st["h2"]),
         P("12.5.1&nbsp;&nbsp;A dose given before the first birthday does not count towards the two doses. A child "
           "vaccinated before 12 months, for example during an outbreak, needs two further doses from 12 months of age."),
         P("12.5.2&nbsp;&nbsp;The minimum interval between two doses of MMR is four weeks (28 days). A dose given "
           "sooner after the previous dose does not count and should be repeated."),
         P("12.5.3&nbsp;&nbsp;Doses given abroad count when they are documented with the date given."),
         Paragraph("12.6 Catch-up", st["h2"]),
         P("12.6.1&nbsp;&nbsp;Children and adults born in or after 1978 who do not have two documented valid doses "
           "should be offered MMR, whatever their age, to complete two doses."),
         P("12.6.2&nbsp;&nbsp;People born before 1978 are likely to have had measles and are presumed immune unless "
           "they work in healthcare or have no history of the disease."),
         P("12.6.3&nbsp;&nbsp;There is no harm in giving MMR to a person who is already immune. Serology before "
           "vaccination is not needed."),
         P("12.6.4&nbsp;&nbsp;MMR may be given at the same visit as other vaccines. Live vaccines not given on the same "
           "day are separated by four weeks."),
         Paragraph("12.6 Table. Doses needed by documented history", st["h2"]),
         _table([["Documented valid doses", "Born 1978 or later", "Born before 1978"],
                 ["None", "Two doses, four weeks apart", "None needed (healthcare workers: two doses)"],
                 ["One", "One dose", "None needed (healthcare workers: one dose)"],
                 ["Two", "None", "None"]], [52, 56, 62], st)]
    d.build(s, onFirstPage=page, onLaterPages=page)


def uptake(path):
    st = _styles(SANS, SANS_B, 9.6, colors.HexColor("#5a2a5f"))
    d, page = _doc(path, "MMR uptake at 24 months and 5 years, quarter 1 2027", "National immunisation programme",
                   "Quarterly uptake report", "National immunisation programme | MMR uptake, quarter 1 2027")
    P = lambda t: Paragraph(t, st["body"])
    rows = [["Health region", "MMR1 at 24 months (born Jan to Mar 2025)", "MMR2 at 5 years (born Jan to Mar 2022)",
             "MMR1 at 24 months, quarter 4 2026"],
            ["Dublin and North Coast", "88.6%", "84.2%", "88.9%"],
            ["Dublin and Mid-Leinster", "89.9%", "85.8%", "90.4%"],
            ["Midlands", "90.8%", "87.1%", "91.0%"],
            [W.REGION, "90.3%", "86.4%", "89.7%"],
            ["South East", "91.6%", "88.0%", "91.2%"],
            ["South West", "90.9%", "86.9%", "91.4%"],
            ["Mid-West", "90.2%", "86.3%", "90.6%"],
            ["West", "91.4%", "88.4%", "91.1%"],
            ["North West", "92.0%", "88.9%", "92.3%"],
            ["Ireland", "90.1%", "86.3%", "90.4%"]]
    s = [Paragraph("NATIONAL IMMUNISATION PROGRAMME", st["small"]),
         Paragraph("MMR uptake at 24 months and at 5 years, quarter 1 2027", st["h1"]),
         Paragraph("Published 20 June 2027. Provisional; figures for earlier quarters are revised as late returns arrive.",
                   st["small"]),
         Paragraph("Uptake by health region", st["h2"]),
         _table(rows, [44, 42, 42, 38], st, zebra=True),
         Spacer(1, 4),
         Paragraph("Uptake is the share of children in the cohort, resident in the health region on the last day of the "
                   "quarter, with the dose recorded by the age shown. The target for both doses is 95 per cent.",
                   st["small"]),
         Paragraph("Commentary", st["h2"]),
         P("First-dose uptake at 24 months fell for a third quarter in a row in five of the nine health regions and is "
           "4.9 points below target nationally. Second-dose uptake at 5 years is unchanged on the quarter. Regions with "
           "uptake under 90 per cent at 24 months should review GP reminder and recall arrangements."),
         P("From quarter 3 2027 the report will add uptake at 12 months for the first dose, to show delays in the "
           "routine schedule earlier.")]
    d.build(s, onFirstPage=page, onLaterPages=page)


def extract_notes(path):
    import docx
    from docx.shared import Pt
    doc = docx.Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)
    doc.add_heading("Regional immunisation register: extract for the autumn 2027 catch-up options", level=1)
    doc.add_paragraph("%s, Register Data Manager, 5 July 2027" % W.PEOPLE["register"])
    doc.add_heading("Extract", level=2)
    doc.add_paragraph("Run on 3 July 2027 for registrations of people born in 1993 to 2017, as at 30 June 2027, for the "
                      "Regional Immunisation Office's catch-up options.")
    doc.add_heading("Files", level=2)
    for t in [
        "register_people_active_born_1993-2017.csv: one row per active registration. An active registration closes only "
        "on death or when another region confirms a transfer; people who have moved away remain active until then.",
        "register_mmr_events_born_1993-2017.csv: one row per MMR event loaded to a registration of a person born in 1993 "
        "to 2017, whatever the registration's status (active, transferred, deceased or merged).",
        "register_merges_born_1993-2017.csv: one row per merge of two registrations found to be the same person. The "
        "retired registration's number is not reused.",
        "gp_return_queries_mmr_2005-2027.csv: the immunisation office's log of queries on GP return lines carrying an "
        "MMR dose, for children and adults of every age, from January 2005.",
    ]:
        doc.add_paragraph(t, style="List Bullet")
    doc.add_heading("Fields", level=2)
    tbl = doc.add_table(rows=1, cols=2)
    tbl.style = "Table Grid"
    tbl.rows[0].cells[0].text = "Field"
    tbl.rows[0].cells[1].text = "Meaning"
    for f, m in [
        ("person_number", "Register number: OR and seven digits, the last a check digit."),
        ("date_of_birth, sex", "As registered."),
        ("lho_code", "Local health office of the person's address as recorded on lho_recorded."),
        ("lho_recorded", "Date the person's address was last recorded."),
        ("registered_on", "Date the registration was opened."),
        ("gp_practice", "Practice the person is registered with, from the GP returns."),
        ("event_number", "Register event number."),
        ("person_number (events)", "The registration the event was loaded to."),
        ("product", "Vaccine product as returned."),
        ("date_given", "Date the dose was given, as returned."),
        ("given_by", "GP, School team, Hospital, Pharmacy, Occupational health or Abroad (keyed from a record from abroad)."),
        ("source_ref", "GP return line (GPR-yyyymm-practice-line), school session (SIT-yyyy-nnnn), hospital clinic "
                       "(HOS-), pharmacy (PHA-), occupational health (OCH-) or record from abroad (ABR-)."),
        ("loaded_on", "Date the event was loaded to the register."),
        ("retired_number, surviving_number", "The registration closed by the merge and the one kept."),
    ]:
        r = tbl.add_row().cells
        r[0].text = f
        r[1].text = m
    doc.add_heading("Loading", level=2)
    doc.add_paragraph("GP doses are loaded from each practice's monthly return, line by line as received. School doses "
                      "are loaded from the school immunisation team's session uploads. Hospital, pharmacy and "
                      "occupational health doses are loaded from their returns, and records from abroad are keyed at "
                      "registration from the documents the person brings.")
    doc.add_paragraph("The extract ran on the morning of 3 July 2027; returns received on 1 and 2 July were loaded.")
    doc.add_heading("Contact", level=2)
    doc.add_paragraph("Register data manager, Regional Immunisation Office.")
    doc.save(path)


FIELDS_TXT = """NOTIFIABLE DISEASE SYSTEM (NDS) - CASE EXPORT FIELD NOTES
Version 3.1, 3 March 2025. Department of Public Health, surveillance.

The case export lists measles notifications for people resident in Oriel Health Region, one row per case
record, with the classification and fields as they stand when the export runs. Dates are dd/mm/yyyy.

case_id             NDS case number. Cases notified on the legacy system before 1 March 2021 were migrated
                    on that date and numbered NDS-L followed by six digits.
legacy_ref          The legacy system's case number, for migrated cases.
notified            Date of notification.
onset_date          Date of rash onset.
date_of_birth       Date of birth.
sex                 M or F.
county              County of residence at notification.
classification      Case classification under the measles case definition:
                      Confirmed  laboratory confirmed (measles IgM or RNA detected, at the national measles
                                 reference laboratory or a hospital laboratory);
                      Probable   clinically compatible, with an epidemiological link to a confirmed case;
                      Possible   clinically compatible;
                      Discarded  not a case.
importation         Imported: infected outside Ireland (exposure abroad 7 to 21 days before rash onset).
                    Import-related: infected in Ireland in a chain from an imported case.
                    Endemic or Unknown otherwise. Blank for discarded cases.
outbreak_ref        Outbreak record in the outbreak module (in use from May 2021).
epi_link            case_id of the case this case was linked to.
hospitalised        Y or N.
mmr_doses_reported  MMR doses before onset as reported on the notification (0, 1, 2 or Unknown).
comments            Free text from the case record.

The laboratory file lists specimens tested at the national measles reference laboratory, keyed to the NDS
case number (results for migrated cases carry their migrated numbers). Hospital laboratory results are
recorded on the case, not in the laboratory file.
"""


def fields(path):
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(FIELDS_TXT)
