"""Governing documents and the survey release: the order's program guide (the pin), the job board's employer terms,
and the Quarterly Employer Vacancy Survey release tables."""
import datetime as dt
import os

import numpy as np

import common as C
import params as P
import world as W


def survey_estimates(vac, rng, emps):
    """The survey's published sector estimates: the true stock of unfilled positions on each quarter's last day,
    with sampling error, rounded to the nearest 5; and the public-sector table by broad occupational category."""
    dates = [dt.date(2025, 9, 30)] + P.REF_DATES
    days = [W.d2i(d) for d in dates]
    true = {(sc, d): 0 for sc in P.SECTOR_CODES for d in dates}
    public_true = {}
    starts = np.array([v["start"] for v in vac])
    ends = starts + np.array([v["T"] for v in vac])
    posn = np.array([v["positions"] for v in vac])
    secs = np.array([v["sector"] for v in vac])
    pub = np.array([(v["emp"] is not None and emps[v["emp"]]["public"]) for v in vac])
    occ = np.array([v["occ"] for v in vac])
    for d, day in zip(dates, days):
        live = (starts <= day) & (day < ends)
        for sc in P.SECTOR_CODES:
            true[(sc, d)] = int(posn[live & (secs == sc)].sum())
        lp = live & pub
        for broad in sorted(set(o[0] for o in occ[lp])):
            public_true[(broad, d)] = int(posn[lp & np.array([o[0] == broad for o in occ])].sum())
    cv = {s[0]: s[4] for s in P.SECTORS}
    est = {}
    for (sc, d), t in sorted(true.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        e = t * (1.0 + rng.normal(0.0, cv[sc] * 0.8))
        est[(sc, d)] = int(5 * round(e / 5.0))
    pub_est = {}
    for (b, d), t in sorted(public_true.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        e = t * (1.0 + rng.normal(0.0, 0.05))
        pub_est[(b, d)] = int(5 * round(e / 5.0))
    cvs = {}
    for sc in P.SECTOR_CODES:
        for d in dates:
            cvs[(sc, d)] = round(100 * cv[sc] * float(rng.uniform(0.85, 1.15)), 1)
    return dates, true, est, cvs, public_true, pub_est


BROAD = {
    "0": "Legislative and senior management occupations",
    "1": "Business, finance and administration occupations",
    "2": "Natural and applied sciences and related occupations",
    "3": "Health occupations",
    "4": "Occupations in education, law and social, community and government services",
    "5": "Occupations in art, culture, recreation and sport",
    "6": "Sales and service occupations",
    "7": "Trades, transport and equipment operators and related occupations",
    "8": "Natural resources, agriculture and related production occupations",
    "9": "Occupations in manufacturing and utilities",
}


def write_survey_release(vac, rng, emps, tgt):
    import openpyxl
    from openpyxl.styles import Font, Alignment
    dates, true, est, cvs, public_true, pub_est = survey_estimates(vac, rng, emps)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Table 1"
    ws.append(["Quarterly Employer Vacancy Survey (QEVS), third quarter 2026"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Table 1. Job vacancies by industry sector, Laurentide, last day of the quarter"])
    ws.append(["Provincial Statistics Bureau. Released 6 November 2026."])
    ws.append([])
    hdr = ["Industry sector", "NAICS 2017"]
    for d in dates:
        hdr += [d.strftime("%d %b %Y"), "CV (%)"]
    ws.append(hdr)
    for c in ws[5]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True)
    for s in P.SECTORS:
        row = [s[1], s[2]]
        for d in dates:
            row += [est[(s[0], d)], cvs[(s[0], d)]]
        ws.append(row)
    tot = ["All sectors", ""]
    for d in dates:
        tot += [sum(est[(sc, d)] for sc in P.SECTOR_CODES), ""]
    ws.append(tot)
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    ws.append([])
    ws.append(["Estimates are rounded to the nearest 5 and may not add to the total."])
    ws.append(["The 31 December 2025 to 30 June 2026 estimates are revised; earlier releases are superseded."])
    ws.column_dimensions["A"].width = 52
    ws2 = wb.create_sheet("Table 2")
    ws2.append(["Quarterly Employer Vacancy Survey (QEVS), third quarter 2026"])
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.append(["Table 2. Public sector job vacancies by broad occupational category (NOC 2021), Laurentide"])
    ws2.append(["Public sector: the provincial government, health authorities, school divisions and municipalities."])
    ws2.append([])
    hdr2 = ["Broad occupational category"] + [d.strftime("%d %b %Y") for d in P.REF_DATES]
    ws2.append(hdr2)
    for c in ws2[5]:
        c.font = Font(bold=True)
    for b in sorted(BROAD):
        vals = [pub_est.get((b, d)) for d in P.REF_DATES]
        if all(v is None or v == 0 for v in vals):
            continue
        ws2.append(["%s %s" % (b, BROAD[b])] + [("x" if (v is None or v < 10) else v) for v in vals])
    ws2.append([])
    ws2.append(["x suppressed to meet the confidentiality requirements of the Statistics Act (Laurentide)."])
    ws2.column_dimensions["A"].width = 70
    C.save_workbook(wb, os.path.join(tgt, "qevs_2026q3_release_tables.xlsx"),
                    dt.datetime(2026, 11, 6, 8, 30), "Provincial Statistics Bureau")
    return dates, true, est, public_true, pub_est


# ---------------------------------------------------------------------------------------------- PDFs
def _styles():
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=10, leading=13.5, spaceAfter=6)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=14, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=8,
                        spaceAfter=4)
    small = ParagraphStyle("small", parent=body, fontSize=8.5, leading=11)
    return body, h1, h2, small


def _doc(path, title, author):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate
    C.pdf_invariant()
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=72, rightMargin=72, topMargin=64, bottomMargin=64,
                             title=title, author=author, subject="", creator=author, producer=author)


def write_program_guide(tgt):
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    body, h1, h2, small = _styles()
    path = os.path.join(tgt, "in_demand_occupations_order_2027_program_guide.pdf")
    doc = _doc(path, "In-Demand Occupations Order, 2027: Program Guide", "Department of Labour, Skills and Immigration")
    st = []
    st.append(Paragraph("In-Demand Occupations Order, 2027", h1))
    st.append(Paragraph("Program Guide. Department of Labour, Skills and Immigration, with the Provincial Statistics "
                        "Bureau. Issued 20 October 2026.", small))
    st.append(Spacer(1, 8))
    st.append(Paragraph("1. What the order does", h2))
    st.append(Paragraph(
        "The In-Demand Occupations Order sets the occupations that are in demand in Laurentide for a calendar year. "
        "For 2027, an employer recruiting in a listed occupation may nominate a foreign national under the Skilled "
        "Worker stream of the Laurentide Provincial Nominee Program without a labour market test, and may claim the "
        "Employer Training Grant at the enhanced rate for an apprentice or trainee in that occupation. The Minister "
        "makes the order by 1 December 2026 on the figures the Provincial Statistics Bureau certifies.", body))
    st.append(Paragraph("2. The test", h2))
    st.append(Paragraph(
        "An occupation in Schedule A is listed for 2027 when its registered jobseekers, summed over the four "
        "reference dates, are no more than 1.5 times its vacancies summed over the same four dates. The reference "
        "dates are 31 December 2025, 31 March 2026, 30 June 2026 and 30 September 2026. The Bureau reports the ratio "
        "to one decimal and applies the test to the unrounded figures.", body))
    st.append(Paragraph("3. Terms used in the test", h2))
    st.append(Paragraph(
        "<b>Occupation.</b> A unit group of the National Occupational Classification (NOC) 2021 version 1.0.", body))
    st.append(Paragraph(
        "<b>Vacancy.</b> A paid position that is unfilled on the reference date, that is available to start within "
        "30 days, and that the employer is actively seeking to fill from outside the organisation. This is the "
        "definition the Quarterly Employer Vacancy Survey uses. Vacancies are counted in positions.", body))
    st.append(Paragraph(
        "<b>An occupation's vacancies</b> on a reference date are its vacancies with all employers in Laurentide, "
        "advertised on the Workshore Job Board or not. The survey's estimates of vacancies by industry sector are the "
        "Province's official totals.", body))
    st.append(Paragraph(
        "<b>Registered jobseeker.</b> A Workshore client who is registered as looking for work on the reference date. "
        "A client whose registration is on hold (for training, illness or leave) is not counted. Each client is "
        "counted once, under the primary occupation they are seeking.", body))
    st.append(Paragraph("4. Timetable", h2))
    st.append(Paragraph(
        "The Bureau certifies to the Minister, for each Schedule A occupation, the registered jobseekers and the "
        "vacancies summed over the four reference dates, the ratio, and the occupations that meet the test. Program "
        "contact: Sherri Underwood, Manager, Labour Market Statistics, Provincial Statistics Bureau.", body))
    st.append(Paragraph("Schedule A. Occupations tested for 2027", h2))
    rows = [["NOC 2021", "Occupation"]] + [[o[0], Paragraph(o[1], small)] for o in sorted(P.OCCUPATIONS, key=lambda o: o[0])]
    t = Table(rows, colWidths=[62, 390])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9), ("FONT", (0, 1), (0, -1), "Helvetica", 9),
                           ("GRID", (0, 0), (-1, -1), 0.25, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8E8E8"))]))
    st.append(t)
    doc.build(st)
    return path


def write_employer_terms(tgt):
    from reportlab.platypus import Paragraph, Spacer
    body, h1, h2, small = _styles()
    path = os.path.join(tgt, "workshore_job_board_terms_for_employers_2026.pdf")
    doc = _doc(path, "Workshore Job Board: Terms for Employers", "Workshore")
    st = []
    st.append(Paragraph("Workshore Job Board: Terms for Employers", h1))
    st.append(Paragraph("Effective 2 February 2026. These terms replace the terms of 3 April 2023 when the board moved "
                        "to its new platform. Posting terms and fees are unchanged.", small))
    st.append(Spacer(1, 8))
    st.append(Paragraph("1. Employer accounts", h2))
    st.append(Paragraph(
        "To post a job you need a Workshore employer account. Each account has an employer number, which appears on "
        "every posting and on every vacancy Workshore Employer Services manages for you. Posting is free.", body))
    st.append(Paragraph("2. Postings you publish yourself", h2))
    st.append(Paragraph(
        "You can publish a posting yourself from your employer account. A posting stays on the board for 42 days "
        "from the day it is published. Before the 42 days end you can renew it for a further 42 days, and you can "
        "renew it more than once. A posting that is not renewed comes off the board at the end of its 42nd day. "
        "Please take your posting down as soon as the position is filled or you stop recruiting.", body))
    st.append(Paragraph("3. Vacancies managed by Workshore Employer Services", h2))
    st.append(Paragraph(
        "If you ask Workshore Employer Services to manage a vacancy, your employment consultant publishes the posting "
        "on the board, refers suitable Workshore clients if you ask us to, and takes the posting down on the day you "
        "tell us the outcome.", body))
    st.append(Paragraph("4. What a posting shows", h2))
    st.append(Paragraph(
        "Each posting shows the job title, the occupation you choose from the National Occupational Classification "
        "list, the number of openings, the location, the wage or wage range and the hours. A posting for more than "
        "one opening stays on the board until it is taken down or its term ends.", body))
    st.append(Paragraph("5. Content and privacy", h2))
    st.append(Paragraph(
        "Postings must be for real, current jobs in Laurentide and must comply with the Employment Standards Code and "
        "the Human Rights Code. Workshore may remove a posting that does not. Workshore keeps posting records to run "
        "the board and to produce labour market information; the Provincial Statistics Bureau receives them under "
        "the Statistics Act (Laurentide).", body))
    doc.build(st)
    return path
