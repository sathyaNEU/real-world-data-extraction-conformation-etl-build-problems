"""The pack's documents: the council's county allocation policy, the Department of Revenue's individual income tax
statistics for tax year 2023, the program's 2025 close-out summary, the data dictionary and the export manifest."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P      # noqa: E402
import world as W     # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1d2126")
GREY = colors.HexColor("#5a616b")
GREEN = colors.HexColor("#2c4a3e")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.5, leading=14.2, textColor=INK, spaceAfter=6)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.2, leading=10.4, textColor=INK)
CELLR = ParagraphStyle("cellr", parent=CELL, alignment=2)
CELLB = ParagraphStyle("cellb", fontName="LiberationSans-Bold", fontSize=8.2, leading=10.4, textColor=INK)
NOTE = ParagraphStyle("note", fontName="LiberationSans", fontSize=7.8, leading=10.0, textColor=GREY, spaceAfter=4)
H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14.5, leading=18.5, textColor=GREEN, spaceAfter=3)
H1S = ParagraphStyle("h1s", fontName="LiberationSans", fontSize=9.0, leading=12.2, textColor=GREY, spaceAfter=12)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.8, leading=14, textColor=INK, spaceBefore=8,
                    spaceAfter=4)


def _doc(path, title, footer, author):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.4)
        canvas.drawString(0.9 * inch, 0.6 * inch, footer)
        canvas.drawRightString(letter[0] - 0.9 * inch, 0.6 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.85 * inch,
                          bottomMargin=0.95 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, right=()):
    data = []
    for i, r in enumerate(rows):
        row = []
        for k, v in enumerate(r):
            st = CELLB if i == 0 else (CELLR if k in right else CELL)
            row.append(Paragraph(str(v), st))
        data.append(row)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("LINEBELOW", (0, -1), (-1, -1), 0.4, GREY),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return t


def fmt(n):
    return "{:,}".format(int(n))


# ---------------------------------------------------------------------------------------------- the policy
POLICY = [
    ("1. Purpose", [
        "1.1 This policy divides the weatherization fund of each program year among the Council's member counties. "
        "It does not choose the dwellings served, which the subgrantee agencies select under the State Weatherization "
        "Plan's priority rules.",
    ]),
    ("2. Definitions", [
        "2.1 A program year is a calendar year; program year 2027 runs from 1 January to 31 December 2027.",
        "2.2 The member counties are the fourteen counties listed in Schedule A.",
        "2.3 The plan date is 15 November of the year before the program year, when the Council files its "
        "weatherization plan for the program year with the State Energy Office.",
    ]),
    ("3. The basis", [
        "3.1 The fund of a program year is allocated among the member counties in proportion to each county's count "
        "of federal individual income tax returns that claimed the earned income credit with at least one qualifying "
        "child and were filed by residents of the county, for the latest tax year for which the Internal Revenue "
        "Service has published its ZIP code statistics at the plan date.",
    ]),
    ("4. Residence", [
        "4.1 A ZIP code's returns are assigned to counties in proportion to the residential addresses that the State "
        "Geographic Information Office's ZIP code to county relationship file for the fourth quarter of the tax year "
        "shows for the ZIP code in each county. A ZIP code with no residential addresses in the file is assigned in "
        "proportion to its total addresses.",
        "4.2 Returns that the IRS statistics place in no ZIP code, in the state line and in the line combining the "
        "ZIP codes with too few returns to publish, are counted for no county.",
    ]),
    ("5. Allocation", [
        "5.1 A member county's share is its count divided by the total of the fourteen counties' counts, and its "
        "allocation is its share of the fund.",
        "5.2 No county receives more than 12 per cent of the fund. The amount by which a county's allocation would "
        "exceed 12 per cent is shared among the other counties in proportion to their counts, and the step is "
        "repeated until no county is above 12 per cent.",
        "5.3 Counts and shares are carried unrounded; each county's allocation is rounded to the nearest hundred "
        "dollars.",
    ]),
    ("6. The plan", [
        "6.1 The Director of Community Energy Programs computes the allocation for the plan and brings it to the "
        "Council Board with each county's record in the last closed program year: the dwellings the program "
        "weatherized in the county, each in the program year in which its job was first completed, and the "
        "program's spending on dwellings in the county, counted as the program year's close-out counts spending.",
    ]),
]
POLICY_CONTROL = [["Revision", "Adopted", "Resolution", "Change"],
                  ["1", "12 November 2015", "15-31", "First issue: households below 150 per cent of poverty, "
                                                     "American Community Survey five-year estimates"],
                  ["2", "8 November 2018", "18-27", "12 per cent cap added (5.2)"],
                  ["3", "14 October 2021", "21-19", "Basis changed to the IRS ZIP code statistics: returns claiming "
                                                    "the earned income credit (3.1, 4.1, 4.2)"],
                  ["4", "14 May 2026", "26-11", "3.1 narrowed to returns claiming the credit with at least one "
                                                "qualifying child, the State Weatherization Plan's priority for "
                                                "households with children; 6.1 the county record added"]]


def write_policy(path):
    d, frame = _doc(path, "Weatherization Assistance Program: County Allocation Policy",
                    "Corran Valley Council of Governments  |  Weatherization Assistance Program  |  "
                    "County Allocation Policy, Revision 4", "Corran Valley Council of Governments")
    story = [Paragraph("Weatherization Assistance Program: County Allocation Policy", H1),
             Paragraph("Corran Valley Council of Governments, Community Energy Programs. Revision 4, adopted by the "
                       "Council Board on 14 May 2026 (Resolution 26-11), with Schedule A. Owner: Director of "
                       "Community Energy Programs.", H1S)]
    for head, paras in POLICY:
        story.append(Paragraph(head, H2))
        for p in paras:
            story.append(Paragraph(p, BODY))
    story.append(Paragraph("Schedule A. Member counties", H2))
    rows = [["County", "FIPS code", "Subgrantee agency"]] + [[W.NAME[f], f, W.AGENCIES[W.AGENCY_OF[f]][0]]
                                                             for f in W.FIPS]
    story.append(_table(rows, [1.4 * inch, 0.9 * inch, 3.2 * inch]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Document control", H2))
    story.append(_table(POLICY_CONTROL, [0.7 * inch, 1.15 * inch, 0.85 * inch, 3.9 * inch]))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def policy_text():
    out = []
    for head, paras in POLICY:
        out.append(head)
        out.extend(paras)
    return out


# ---------------------------------------------------------------------------------------------- the Department's report
DOR_LABEL = {1: "Under $10,000", 2: "$10,000 under $20,000", 3: "$20,000 under $25,000", 4: "$25,000 under $50,000",
             5: "$50,000 under $75,000", 6: "$75,000 or more"}
DOR_INTRO = [
    "This report counts the federal individual income tax returns of the state's residents for tax year 2023, from "
    "the extract of the Internal Revenue Service's individual master file that the Department receives under its "
    "information exchange agreement. It covers returns processed through 31 December 2024. Amounts are in thousands "
    "of dollars and may not add to totals because of rounding.",
    "Size of adjusted gross income follows the federal return; returns with no adjusted gross income are counted in "
    "the lowest class. A qualifying child is a child who meets the relationship, age and residency tests of the "
    "earned income credit (Internal Revenue Code, section 32(c)(3)).",
]


def dor_tables(x):
    ty = x["ty"]
    allr = {}
    for z, f, kids, mfj, a, cr in ty["claim"]:
        v = allr.setdefault(int(W.dor_class(a)), [0, 0.0])
        v[0] += 1
        v[1] += a
    for z, f, a in ty["other"]:
        v = allr.setdefault(int(W.dor_class(a)), [0, 0.0])
        v[0] += 1
        v[1] += a
    t1 = [["Size of adjusted gross income", "Returns", "Adjusted gross income", "Earned income credit returns",
           "Earned income credit amount"]]
    tot = [0, 0, 0, 0]
    for c in range(1, 7):
        n, s = allr.get(c, [0, 0.0])
        en = sum(x["dor"].get((c, k), (0, 0))[0] for k in range(4))
        ea = sum(x["dor"].get((c, k), (0, 0))[1] for k in range(4))
        t1.append([DOR_LABEL[c], fmt(n), fmt(round(s / 1000.0)), fmt(en), fmt(ea)])
        tot = [tot[0] + n, tot[1] + round(s / 1000.0), tot[2] + en, tot[3] + ea]
    t1.append(["All returns", fmt(tot[0]), fmt(tot[1]), fmt(tot[2]), fmt(tot[3])])
    t2 = [["Size of adjusted gross income", "None: returns", "None: amount", "One: returns", "One: amount",
           "Two: returns", "Two: amount", "Three or more: returns", "Three or more: amount"]]
    col = [0] * 8
    for c in range(1, 7):
        row = [DOR_LABEL[c]]
        for k in range(4):
            n, a = x["dor"].get((c, k), (0, 0))
            row += [fmt(n), fmt(a)]
            col[2 * k] += n
            col[2 * k + 1] += a
        t2.append(row)
    t2.append(["All returns"] + [fmt(v) for v in col])
    return t1, t2


def write_dor(path, x):
    d, frame = _doc(path, "Individual Income Tax Statistics, Tax Year 2023",
                    "Department of Revenue  |  Tax Research Division  |  Individual Income Tax Statistics, Tax Year "
                    "2023", "Department of Revenue")
    t1, t2 = dor_tables(x)
    story = [Paragraph("Individual Income Tax Statistics, Tax Year 2023", H1),
             Paragraph("Department of Revenue, Tax Research Division. Published 15 July 2026.", H1S)]
    for p in DOR_INTRO:
        story.append(Paragraph(p, BODY))
    story.append(Paragraph("Table 1. Returns, adjusted gross income and the earned income credit, by size of "
                           "adjusted gross income", H2))
    story.append(_table(t1, [1.7 * inch, 1.0 * inch, 1.2 * inch, 1.4 * inch, 1.4 * inch], right=(1, 2, 3, 4)))
    story.append(Paragraph("Adjusted gross income and credit amounts in thousands of dollars.", NOTE))
    story.append(Paragraph("Table 2. Federal earned income credit, by size of adjusted gross income and number of "
                           "qualifying children", H2))
    story.append(_table(t2, [1.58 * inch] + [0.635 * inch] * 8, right=tuple(range(1, 9))))
    story.append(Paragraph("Returns claiming the credit and the credit claimed (thousands of dollars), by the number "
                           "of qualifying children on the return.", NOTE))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- the close-out
CATEGORIES = [("Energy audits", ("AUDIT",)), ("Materials", ("MATERIALS",)), ("Labor", ("LABOR", "CALLBACK")),
              ("Subcontracted work", ("SUBCONTRACT",)), ("Health and safety", ("HEALTH-SAFETY",)),
              ("Administration", ("ADMIN",)), ("Vehicles", ("VEHICLE",)), ("Training", ("TRAINING",)),
              ("Insurance", ("INSURANCE",))]


def closeout_tables(x):
    p0, p1 = W.PY[W.ASK_YEAR]
    posted = [ln for ln in x["ledger"] if p0 <= ln["posted"] <= p1]
    t1 = [["Category", "DOE-WAP", "State fund", "Total"]]
    tot = [0.0, 0.0]
    for lab, accts in CATEGORIES:
        doe = sum(ln["amount"] for ln in posted if ln["acct"] in accts and ln["fund"] == "DOE-WAP")
        st = sum(ln["amount"] for ln in posted if ln["acct"] in accts and ln["fund"] == "STATE-WX")
        t1.append([lab, "{:,.2f}".format(doe), "{:,.2f}".format(st), "{:,.2f}".format(doe + st)])
        tot = [tot[0] + doe, tot[1] + st]
    t1.append(["All spending", "{:,.2f}".format(tot[0]), "{:,.2f}".format(tot[1]), "{:,.2f}".format(sum(tot))])
    return t1, tot


CLOSE_NOTES = [
    "Spending is counted in the program year in which the Council's grants ledger posts the line, at the amount "
    "posted. Spending on dwellings is the lines charged to jobs; administration, vehicles, training and insurance are "
    "the agencies' own lines.",
    "The program's jobs are those the Department of Energy grant or the State Weatherization Fund pays for; the "
    "agencies also keep the jobs of the utility's low-income weatherization program in the WX job system.",
]


def write_closeout(path, x):
    d, frame = _doc(path, "Weatherization Assistance Program, Program Year 2025 Close-out Summary",
                    "Corran Valley Council of Governments  |  Community Energy Programs  |  Program Year 2025 "
                    "Close-out", "Corran Valley Council of Governments")
    t1, tot = closeout_tables(x)
    story = [Paragraph("Weatherization Assistance Program: Program Year 2025 Close-out Summary", H1),
             Paragraph("Corran Valley Council of Governments, Community Energy Programs. Prepared for the Council "
                       "Board, 24 February 2026.", H1S),
             Paragraph("Program year 2025 ran from 1 January to 31 December 2025. Five subgrantee agencies delivered "
                       "the program in the fourteen member counties with the Department of Energy's Weatherization "
                       "Assistance Program grant and the State Weatherization Fund, and the year's financial "
                       "close-out was filed with the State Energy Office on 13 February 2026. This summary reports "
                       "the year's spending by fund and category.", BODY),
             Paragraph("Table 1. Spending in program year 2025, by category and fund (dollars)", H2),
             _table(t1, [2.2 * inch, 1.4 * inch, 1.4 * inch, 1.4 * inch], right=(1, 2, 3)),
             Paragraph("Notes", H2)]
    for n in CLOSE_NOTES:
        story.append(Paragraph(n, BODY))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- the dictionary
DICTIONARY = """Corran Valley Council of Governments, Community Energy Programs
Data dictionary for the program year 2027 allocation files. Issue 3, 2 October 2026.

irs_soi_zip_code_data_ty2023_extract.csv
Internal Revenue Service, Statistics of Income, individual income tax ZIP code data, tax year 2023, the state's
file as released on 18 June 2026, the latest the IRS has published. The program office's extract keeps the columns
below. One row per ZIP code and size of adjusted gross income.
  STATEFIPS       state FIPS code
  ZIPCODE         five-digit ZIP code; 00000 is the state total and 99999 combines the ZIP codes with fewer than
                  100 returns
  AGI_STUB        size of adjusted gross income: 1 $1 under $25,000; 2 $25,000 under $50,000; 3 $50,000 under
                  $75,000; 4 $75,000 under $100,000; 5 $100,000 under $200,000; 6 $200,000 or more
  N1              number of returns
  A00100          adjusted gross income (thousands of dollars)
  N59660          number of returns with earned income credit
  A59660          earned income credit amount (thousands of dollars)

irs_soi_zip_code_data_ty2022_extract.csv
The same statistics for tax year 2022, in the layout of the 2022 release (lower-case column names), kept from the
2026 allocation.

zip_county_relationship_2023q4.xlsx
State Geographic Information Office, ZIP code to county relationship file, fourth quarter of 2023, built from the
U.S. Postal Service's address counts. One row per ZIP code and county in which the ZIP code has addresses.
  ZIP             five-digit ZIP code
  COUNTY          county FIPS code
  RES_RATIO       share of the ZIP code's residential addresses that lie in the county
  BUS_RATIO       share of its business addresses that lie in the county
  OTH_RATIO       share of its other addresses (P.O. boxes and the like) that lie in the county
  TOT_RATIO       share of all its addresses that lie in the county

county_zip_relationship_2023q4.xlsx
The same address counts the other way: one row per county and ZIP code; each ratio is the share of the county's
addresses of that kind that lie in the ZIP code.

dor_individual_income_tax_statistics_ty2023.pdf
Department of Revenue, Tax Research Division, Individual Income Tax Statistics, Tax Year 2023 (15 July 2026).

cvcog_weatherization_allocation_policy_rev4.pdf
The Council's county allocation policy for the Weatherization Assistance Program, Revision 4 (14 May 2026).

cvcog_member_counties.csv
The fourteen member counties: COUNTY_FIPS, COUNTY, AGENCY (the subgrantee agency serving the county).

wx_subgrantee_agencies.csv
The five subgrantee agencies: AGENCY code, AGENCY_NAME, COUNTIES_SERVED, CONTRACT_NO (the program year 2026
contract), OFFICE_COUNTY.

wx_job_export_2026-09-30.csv
WX job system export of 30 September 2026: one row per job, every job the agencies opened since 1 July 2023.
  JOB_NO          the job's number in the WX job system
  AGENCY          subgrantee agency code
  COUNTY          county the agency entered for the job
  TRACT           the dwelling's 2020 census tract (eleven-digit GEOID)
  BUILDING_TYPE   SF single family; MH manufactured home; MF2-4 two to four units; MF5+ five or more units
  UNITS           dwelling units the job covers
  FUNDING         the job record's funding codes, separated by semicolons where more than one is recorded:
                  DOE-WAP (Department of Energy Weatherization Assistance Program), STATE-WX (State
                  Weatherization Fund), UTIL-LIW (the utility's low-income weatherization program)
  HEATING_FUEL    main heating fuel
  STATUS          the job's status on 30 September 2026: AUDIT SCHEDULED, AUDITED, IN PROGRESS, COMPLETED,
                  REOPENED, DEFERRED, CANCELLED
  OPENED          date the job was opened
  AUDIT_DATE      date of the energy audit
  START_DATE      date work started
  COMPLETED_DATE  date the job was marked complete

wx_job_status_history_2026-09-30.csv
Every status change the WX job system holds, with the history of the jobs moved from the agencies' previous system
on 14 July 2025. One row per change.
  JOB_NO          the job's number in the WX job system
  STATUS          OPENED, AUDIT SCHEDULED, AUDITED, APPROVED, SCHEDULED, IN PROGRESS, COMPLETED, REOPENED,
                  DEFERRED, CANCELLED, MOVED
  CHANGED_AT      local date and time of the change
  CHANGED_BY      user
  NOTE            text entered with the change

cvcog_grants_ledger_2024-07_2026-09.csv
The Council's grants ledger: the expenditure lines posted from 1 July 2024 to 30 September 2026 for the agencies'
monthly invoices. One row per line.
  LINE_ID         ledger line
  POSTED_DATE     date the line was posted
  AGENCY          subgrantee agency code
  INVOICE_NO      the agency's invoice, by agency and service month
  JOB_NO          the job number the invoice gives for the line; blank on the agency's own lines
  ACCOUNT         AUDIT, MATERIALS, LABOR, SUBCONTRACT, HEALTH-SAFETY on jobs; ADMIN, VEHICLE, TRAINING, INSURANCE
                  for the agency
  FUND            DOE-WAP or STATE-WX
  SERVICE_DATE    date the work was done or the cost incurred
  DESCRIPTION     the invoice line's text
  AMOUNT          dollars

cvcog_wap_py2025_closeout_summary.pdf
The program's close-out summary for program year 2025, prepared for the Council Board on 24 February 2026.

export_manifest.csv
This list of files.
"""


def write_dictionary(path):
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(DICTIONARY)


MANIFEST_COLS = ["FILE", "DESCRIPTION", "SOURCE", "PULLED_OR_ISSUED", "COVERS", "ROWS"]
MANIFEST = {
    "irs23": ("IRS SOI ZIP code statistics, tax year 2023, program office extract", "Internal Revenue Service",
              "2026-06-18", "tax year 2023"),
    "irs22": ("IRS SOI ZIP code statistics, tax year 2022, program office extract", "Internal Revenue Service",
              "2025-04-02", "tax year 2022"),
    "rel": ("ZIP code to county relationship file", "State Geographic Information Office", "2024-03-05",
            "fourth quarter 2023"),
    "rel_rev": ("County to ZIP code relationship file", "State Geographic Information Office", "2024-03-05",
                "fourth quarter 2023"),
    "dor": ("Individual Income Tax Statistics, Tax Year 2023", "Department of Revenue", "2026-07-15", "tax year 2023"),
    "policy": ("County allocation policy, Revision 4", "Council Board", "2026-05-14", "program years from 2027"),
    "members": ("Member counties", "Community Energy Programs", "2026-10-02", "current"),
    "agencies": ("Subgrantee agencies", "Community Energy Programs", "2026-10-02", "program year 2026"),
    "jobs": ("WX job system, job export", "WX job system", "2026-09-30", "jobs opened 2023-07-01 to 2026-09-30"),
    "history": ("WX job system, status history", "WX job system", "2026-09-30",
                "status changes 2023-07-01 to 2026-09-30"),
    "ledger": ("Grants ledger, expenditure lines", "Council finance system", "2026-10-01",
               "lines posted 2024-07-01 to 2026-09-30"),
    "closeout": ("Program year 2025 close-out summary", "Community Energy Programs", "2026-02-24", "program year 2025"),
    "dictionary": ("Data dictionary", "Community Energy Programs", "2026-10-02", "these files"),
}


def manifest_rows(n):
    return [[P.FILES[k], d, s, p, c, n.get(k, "")] for k, (d, s, p, c) in MANIFEST.items()]
