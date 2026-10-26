"""The pack's documents: the Department for the Economy's prospectus for the 2027 Town Centre Renewal Fund, the
Revenue Office's specification of its PAYE employer extract, and the Valuation Office's guide to its rating list
extracts."""
import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import names as N

reportlab.rl_config.invariant = 1
STY = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=STY["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.8, spaceAfter=6)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10)
H = ParagraphStyle("h", parent=STY["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
T = ParagraphStyle("t", parent=STY["Title"], fontName="Helvetica-Bold", fontSize=14, spaceAfter=10, alignment=0)


def _pdf(path, title, story, author, org):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=17 * mm,
                            bottomMargin=17 * mm, title=title, author=author, creator=org, subject=title, producer=org)

    def footer(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.drawString(18 * mm, 10 * mm, org + "  |  " + title)
        c.drawRightString(A4[0] - 18 * mm, 10 * mm, "%d" % d.page)
        c.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def P(text, style=BODY):
    return Paragraph(text, style)


def _table(rows, widths=None, size=8.2):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", size), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    return t


def _cell(text, size=7.8):
    return Paragraph(text, ParagraphStyle("c", parent=SMALL, fontSize=size, leading=size + 2))


def prospectus(path):
    dname = dict(N.DISTRICTS_NAMES)
    s = [P("Town Centre Renewal Fund 2027: prospectus", T),
         P("Department for the Economy, Government of Torvasay. Town Centres Unit. Published 7 September 2026. "
           "Reference DfE/TC/2026/07.", SMALL),
         P("1. The fund", H),
         P("The Town Centre Renewal Fund provides GBP 12 million over 2027 to 2029 for projects that bring activity "
           "back into Torvasay's designated town centres where retail trade has contracted since the pandemic. The 2027 "
           "round is open to the centres that meet the eligibility test in section 3. The Council of Ministers approves the "
           "list of eligible centres at its meeting of 10 December 2026, on the eligibility schedule that Torvasay "
           "Statistics prepares for it."),
         P("2. Designated town centres", H),
         P("The 31 town centres designated under the Town Centres (Designation) Order 2019 are listed in the annex. A "
           "centre's boundary is the Department's schedule of the postcode units inside it (town_centre_schedule_2026.csv), "
           "which also lists the units the postal administration has terminated since the Order was made."),
         P("3. Eligibility", H),
         P("3.1 Workplace retail employment, for a March, is the number of employees of employers classified to SIC 2007 "
           "division 47 (retail trade, except of motor vehicles and motorcycles) who were paid in the PAYE tax month "
           "ending 5 April, counted at the premises where they work."),
         P("3.2 A premises is in a designated centre when the postcode of its entry in the valuation list in force on "
           "31 March of that year is in the centre's schedule."),
         P("3.3 A centre is eligible for the 2027 round when its workplace retail employment in March 2026 is 8 per cent "
           "or more below its workplace retail employment in March 2022, the change being taken on unrounded figures."),
         P("3.4 Torvasay Statistics compiles the figures from the Revenue Office's PAYE returns for month 12 of 2021-22 "
           "and 2025-26, the Valuation Office's rating lists and the district councils' business rates accounts, which it "
           "receives under the data-sharing provisions of the Statistics (Torvasay) Act 2014."),
         P("4. The eligibility schedule", H),
         P("The schedule gives each centre's workplace retail employment in March 2022 and March 2026, rounded to the "
           "nearest 50 so that no employer's payroll can be read from it, and its change to the nearest whole per cent. "
           "Its annex sets out, for each district, the shop premises in the district's designated centres that stood "
           "empty at 31 March 2022 and at 31 March 2026, and how many of those had then been empty for twelve months or "
           "more, which the Department reads alongside eligibility when it assesses bids. In the annex a shop premises is "
           "an entry the valuation list in force on that day describes as a shop and premises; it stood empty when no one "
           "was in occupation of it on the day, and had been empty for twelve months or more when it had been in the "
           "list throughout the twelve months to that 31 March and no one was in occupation of it on any of those days."),
         P("5. Timetable", H),
         _table([["Date", "Step"],
                 ["10 December 2026", "Council of Ministers approves the eligible centres"],
                 ["18 January 2027", "Bids open to the eligible centres' district councils and town partnerships"],
                 ["31 March 2027", "Bids close"],
                 ["June 2027", "Awards announced"]], widths=[38 * mm, 120 * mm]),
         Spacer(1, 6),
         P("Programme manager: Irene Walters, Town Centres Unit. Eligibility schedule: Frances Davies, Head of Economic "
           "Statistics, Torvasay Statistics.", SMALL),
         P("Annex: the designated town centres", H),
         _table([["Code", "Centre", "District"]] + [[c, n, dname[d]] for c, n, d, t in N.CENTRES],
                widths=[18 * mm, 60 * mm, 40 * mm], size=7.8)]
    _pdf(path, "Town Centre Renewal Fund 2027: prospectus", s, "Town Centres Unit", "Department for the Economy")


def paye_spec(path):
    v3 = [["Field", "Content"],
          ["scheme_ref", "the PAYE scheme reference: tax office number, a stroke, the employer reference"],
          ["employer_name", "the employer's name as registered for the scheme, in capitals"],
          ["company_no", "the Companies Registry number where the employer is a company"],
          ["sic2007", "the employer's main activity, SIC 2007 subclass, as registered or as the employer has since notified"],
          ["scheme_postcode", "the postcode of the address the Revenue Office holds for the scheme"],
          ["employees_paid", "employees with a payment in the tax month on the scheme's final submission for the month"],
          ["return_period", "the tax year and month of the return"]]
    v4 = [["Field", "Content"],
          ["tax_office", "the tax office number of the scheme reference"],
          ["employer_ref", "the employer reference part of the scheme reference"],
          ["employer_name", "the employer's name as registered for the scheme"],
          ["trading_name", "the name the employer trades under, where it differs and the employer has given one"],
          ["crn", "the Companies Registry number where the employer is a company"],
          ["sic_2007", "the employer's main activity, SIC 2007 subclass"],
          ["paye_postcode", "the postcode of the address the Revenue Office holds for the scheme"],
          ["paid_employees", "employees with a payment in the tax month on the scheme's final submission for the month"],
          ["period", "the tax year and month of the return"]]
    s = [P("PAYE employer extract: specification", T),
         P("Revenue Office, Statistics and Data Sharing. Version 4, 11 May 2026. Supplied to Torvasay Statistics under the "
           "2024 data-sharing agreement.", SMALL),
         P("1. Coverage", H),
         P("The extract lists every PAYE scheme that made a return for the tax month named, with the number of employees it "
           "paid in that month. A scheme that filed an employer payment summary for the month showing no payments appears "
           "with no employees paid. Month 12 runs from 6 March to 5 April."),
         P("2. Layout version 3 (extracts for 2023-24 and earlier)", H), _table(v3, widths=[32 * mm, 128 * mm]),
         P("3. Layout version 4 (extracts from 2024-25)", H),
         P("Version 4 splits the scheme reference into its tax office and employer reference, adds the trading name, "
           "writes names as registered rather than in capitals and renames some fields."),
         _table(v4, widths=[32 * mm, 128 * mm]),
         P("4. Notes", H),
         P("The address the Revenue Office holds for a scheme is the address for PAYE correspondence. It may be one of the "
           "employer's premises, its head office, or the address of an agent (a payroll bureau or an accountant) the "
           "employer has authorised to act for the scheme. It is not a record of where the employees work."),
         P("An employer may operate more than one scheme, for example one for weekly and one for monthly paid staff, and "
           "the extract lists schemes, not employers. An employee paid by two schemes in the month is counted by each. A "
           "scheme that is closed and replaced, after a change of payroll provider or of legal entity, appears under its "
           "new reference from the month of the change."),
         P("Contact: Stewart Sheppard, data-sharing lead, Statistics and Data Sharing.", SMALL)]
    _pdf(path, "PAYE employer extract: specification", s, "Statistics and Data Sharing", "Revenue Office")


def list_guide(path):
    f17 = [["Field", "Content"], ["UARN", "unique address reference number of the hereditament"],
           ["BA_CODE", "billing authority (district council) code"], ["BA_REFERENCE", "the council's own property reference"],
           ["NUMBER_OR_NAME, STREET, TOWN", "the address"], ["POSTCODE", "the postcode held for the entry"],
           ["DESCRIPTION_CODE, DESCRIPTION", "the primary description (valuation_description_codes.json)"],
           ["TOTAL_AREA, AREA_BASIS", "the area the value is assessed on, in square metres, and its measurement basis"],
           ["RATEABLE_VALUE", "the rateable value in pounds"],
           ["EFFECTIVE_DATE, EFFECTIVE_TO", "the first and last days the entry had effect; EFFECTIVE_TO is blank while it does"]]
    f23 = [["Field", "Content"], ["uarn", "unique address reference number of the hereditament"],
           ["billing_authority, ba_ref", "the district council's code and its property reference"],
           ["address, postcode", "the address and the postcode held for the entry"],
           ["primary_desc_code, primary_description", "the primary description"],
           ["floor_area_m2, measurement_basis", "the area the value is assessed on and its measurement basis"],
           ["rateable_value", "the rateable value in pounds"],
           ["effective_from, effective_to", "the first and last days the entry had effect; effective_to is blank while it does"]]
    s = [P("Rating list extracts: field guide", T),
         P("Torvasay Valuation Office. Issued with the extracts of the 2017 list (4 April 2022) and the 2023 list (13 April 2026).", SMALL),
         P("1. The lists", H),
         P("The 2017 list had effect from 1 April 2017 to 31 March 2023 and the 2023 list has effect from 1 April 2023, its "
           "values set at 1 April 2021. Each extract holds every entry that has had effect in its list up to the extract "
           "date: an entry altered or deleted carries the last day it had effect, and its successor, if any, the day it took "
           "effect. A hereditament is a unit of property assessed separately; one occupier may occupy several."),
         P("2. Areas", H),
         P("Areas are measured as the code of measuring practice sets for each description: net internal area for shops, "
           "offices, banks, cafes and restaurants, and gross internal area for department stores, supermarkets, retail "
           "warehouses, warehouses and industrial premises."),
         P("3. 2017 list extract", H), _table(f17, widths=[52 * mm, 108 * mm]),
         P("4. 2023 list extract", H), _table(f23, widths=[52 * mm, 108 * mm]),
         P("Postcodes are those the Valuation Office held when each list was compiled or the entry made, so a postcode the "
           "postal administration has since replaced may appear on a 2017 list entry.", SMALL)]
    _pdf(path, "Rating list extracts: field guide", s, "Valuation Office", "Torvasay Valuation Office")
