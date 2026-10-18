"""task163 documents: the 2027 sizing standard (FP&A), sales operations' counting notes, the research team's log of
state filing changes, the plan workbook with sales operations' share tab, the field guide and the pack manifest."""
from __future__ import annotations

import datetime as dt
import os

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import common as K
import postprocess as PP
import records as R
import world as WD

F_STANDARD = "plan_2027_sizing_standard.docx"
F_NOTES = "first_time_employer_counting_notes.docx"
F_LOG = "state_filing_changes_log.xlsx"
F_PLAN = "plan_2027_workbook.xlsx"
F_DICT = "plan_pack_field_guide.xlsx"
F_MANIFEST = "pack_manifest.csv"

P = K.PEOPLE
GREEN = "2F4F6B"


# ------------------------------------------------------------------------------------------------- word
def _page_field(par):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    for kind, text in (("begin", None), (None, " PAGE "), ("separate", None), (None, "1"), ("end", None)):
        r = par.add_run()
        if kind:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), kind)
            r._r.append(fc)
        elif text.strip() == "PAGE":
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = text
            r._r.append(it)
        else:
            r.text = text


def _word(path, title, byline, sections, footer):
    import docx
    from docx.shared import Cm, Pt, RGBColor
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    st.paragraph_format.space_after = Pt(6)
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)
    sec.left_margin = sec.right_margin = Cm(2.4)
    sec.top_margin, sec.bottom_margin = Cm(2.2), Cm(2.0)
    fp = sec.footer.paragraphs[0]
    fp.text = footer + ", page "
    _page_field(fp)
    for r in fp.runs:
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(0x5D, 0x67, 0x6E)
    blue = RGBColor(0x2F, 0x4F, 0x6B)
    p = doc.add_paragraph()
    r = p.add_run(title)
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = blue
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run(byline)
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x5D, 0x67, 0x6E)
    for head, paras in sections:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(head)
        r.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = blue
        for t in paras:
            doc.add_paragraph(t)
    doc.save(path)


STANDARD = [
    ("The line", [
        "The first-time-employer line counts the new customers whose first payroll ever runs with Kilbourne in the "
        "plan year, in our twelve core states: Ohio, Pennsylvania, Michigan, Indiana, Kentucky, Minnesota, Wisconsin, "
        "Iowa, Tennessee, Missouri, Virginia and West Virginia. Businesses moving their payroll to us from another "
        "provider or from their own books, and clients coming back, are in the switcher and returning lines.",
    ]),
    ("The market", [
        "The line's market is employer business formation as the Census Bureau measures it in the Business Formation "
        "Statistics: the business applications in a state that become employer businesses within four quarters of "
        "the application. The plan uses the October release, whose latest month of applications is the September "
        "before the plan year.",
    ]),
    ("Sizing", [
        "Each state's line is its 2025 share in the plan workbook times the business formations within four quarters "
        "that a year of business applications in the state, at the level of the twelve months to September 2026, will "
        "produce. The twelve states add up to the line, which goes into the plan to the nearest 100.",
        "Sales operations keeps the share tab: each state's 2025 first-time employers, counted from the January "
        "extract as the counting notes count them, over the state's business formations within four quarters from "
        "the applications of July 2024 to June 2025 in the October release.",
    ]),
    ("Timetable", [
        "Market Research pulls the October release on the day it comes out, Wednesday 14 October 2026, and sales "
        "operations refreshes the share tab from it. The line is sized for the CFO's sign-off of the operating plan "
        "on Friday 16 October.",
    ]),
]

NOTES = [
    ("Who counts", [
        "A first-time employer is a business whose first payroll ever runs with us. It is counted once, in the year "
        "of its first pay date with us and in the state it first employed in.",
        "A business is the employer, whatever its account or EIN. A client that comes back after cancelling, or "
        "re-forms as a new entity and carries on, is the same business, and its accounts count as one.",
    ]),
    ("Still with us", [
        "A business is still with us in a quarter when we paid wages for it, on any of its accounts, with a pay date "
        "in that quarter.",
    ]),
    ("Wages", [
        "A business's first quarter on payroll is the calendar quarter of its first pay date with us. Wages are the "
        "gross wages we ran on our payroll for the business, before deductions and taxes.",
    ]),
    ("Where the counts come from", [
        "The year-end planning extract pulled on 9 January 2026: every account with a first pay date from January 2022, "
        "the quarterly wages for each account, and each account's state registrations. Legacy client numbers map to "
        "current accounts through the migration crosswalk. Territories are as on the 2025 territory map.",
    ]),
]


def write_standard(path):
    _word(path, "2027 operating plan: sizing the first-time-employer line",
          "Revenue Planning, FP&A. %s, 1 September 2026. For the 2027 operating plan." % P["planning"], STANDARD,
          "Kilbourne Payroll FP&A, 2027 plan sizing")


def write_notes(path):
    _word(path, "First-time employers: how we count them",
          "Sales Operations. %s, 3 February 2026." % P["salesops"], NOTES,
          "Kilbourne Payroll Sales Operations, first-time employer counts")


# ------------------------------------------------------------------------------------------------- excel helpers
HEAD_FILL = PatternFill("solid", fgColor="DCE4EC")
THIN = Side(style="thin", color="A9B4BE")


def _head(ws, row, cols, widths):
    for c, h in enumerate(cols, start=1):
        cell = ws.cell(row=row, column=c, value=h)
        cell.font = Font(name="Calibri", size=10, bold=True)
        cell.fill = HEAD_FILL
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        cell.border = Border(bottom=THIN)
    for c, w in enumerate(widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(c)].width = w


def _title(ws, title, note, span):
    ws["A1"] = title
    ws["A1"].font = Font(name="Calibri", size=13, bold=True, color=GREEN)
    ws["A2"] = note
    ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="5F6670")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:%s2" % span)
    ws.row_dimensions[2].height = 40


LOG = [
    # logged, state, effective, change type, change, source
    (dt.date(2023, 7, 6), "IN", dt.date(2023, 7, 1), "Fee change",
     "Online filing fee for new LLCs and corporations reduced.", "Secretary of State notice"),
    (dt.date(2023, 11, 8), "KY", dt.date(2023, 11, 6), "New filing system",
     "Secretary of State's online business filings move to a new system; it offers the state tax registration at "
     "the end of a formation filing. No IRS step.", "Secretary of State press release"),
    (dt.date(2024, 2, 7), "OH", dt.date(2024, 2, 5), "Integrated EIN application",
     "Online formation filings (LLC, corporation, partnership) let the filer apply for a federal EIN inside the "
     "filing; the state passes the application to the IRS. Optional. Paper forms and the previous online filing "
     "stay open.", "Secretary of State press release"),
    (dt.date(2024, 5, 15), "PA", dt.date(2024, 5, 13), "Integrated EIN application",
     "Online formation filings let the filer apply for a federal EIN inside the filing, passed to the IRS by the "
     "Department of State. Optional; the previous filing routes stay open.", "Department of State announcement"),
    (dt.date(2024, 8, 14), "MI", dt.date(2024, 8, 12), "Integrated EIN application",
     "Online formation filings let the filer apply for a federal EIN inside the filing. Optional; the previous "
     "routes stay open.", "Department of Licensing and Regulatory Affairs release"),
    (dt.date(2024, 9, 12), "WI", dt.date(2024, 9, 9), "New filing system",
     "Annual reports and amendments move to a new online portal. Formation filings unchanged.",
     "Department of Financial Institutions notice"),
    (dt.date(2025, 3, 5), "TN", dt.date(2025, 3, 3), "New filing system",
     "Business services portal relaunched for annual reports and certificates. Formation filings unchanged, no "
     "IRS step.", "Secretary of State press release"),
    (dt.date(2025, 10, 3), "OH", dt.date(2025, 10, 1), "Older filing route closed",
     "Paper formation forms and the previous online filing withdrawn. Every formation filing now goes through the "
     "integrated filing, which asks whether to apply for an EIN.", "Secretary of State notice"),
    (dt.date(2025, 12, 3), "PA", dt.date(2025, 12, 1), "Older filing route closed",
     "Previous formation filing routes closed; every formation filing goes through the integrated filing.",
     "Department of State notice"),
    (dt.date(2026, 2, 4), "MI", dt.date(2026, 2, 2), "Older filing route closed",
     "Previous formation filing routes closed; every formation filing goes through the integrated filing.",
     "Department of Licensing and Regulatory Affairs notice"),
    (dt.date(2026, 6, 22), "MO", dt.date(2026, 7, 1), "Fee change",
     "Annual registration report fee waived for reports filed in the second half of 2026.",
     "Secretary of State notice"),
]


def write_log(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Log"
    _title(ws, "State business filing changes, core states",
           "Market Research. Kept by %s since 2023; a row is logged when a state announces a change to how businesses "
           "form or file. Effective is the state's own date." % P["research"], "F")
    cols = ["Logged", "State", "Effective", "Change type", "Change", "Source"]
    _head(ws, 4, cols, [11, 7, 11, 24, 78, 34])
    for i, row in enumerate(LOG, start=5):
        for c, v in enumerate(row, start=1):
            cell = ws.cell(row=i, column=c, value=v)
            cell.font = Font(name="Calibri", size=10)
            cell.alignment = Alignment(wrap_text=(c == 5), vertical="top")
            if c in (1, 3):
                cell.number_format = "yyyy-mm-dd"
    ws.freeze_panes = "A5"
    wb.save(path)


def write_plan(path, share):
    """The plan workbook as FP&A circulates it for the October cycle: the share tab sales operations refreshed from the
    October release, and the workbook notes."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Share 2025"
    _title(ws, "2025 first-time employer share by state",
           "Sales Operations (%s), refreshed 15 October 2026. First-time employers: 2025, January 2026 extract, counted "
           "as in the counting notes. Formations: business formations within four quarters from applications of July "
           "2024 to June 2025, Census BFS October 2026 release, not seasonally adjusted." % P["salesops"], "E")
    cols = ["State", "State name", "First-time employers, 2025", "Formations within 4 quarters, Jul 2024 to Jun 2025 "
            "applications", "Share"]
    _head(ws, 4, cols, [8, 16, 14, 22, 10])
    ws.row_dimensions[4].height = 44
    r = 5
    for s in WD.STATES:
        c, b = share[s.usps]
        vals = [s.usps, s.name, c, b, c / b]
        for j, v in enumerate(vals, start=1):
            cell = ws.cell(row=r, column=j, value=v)
            cell.font = Font(name="Calibri", size=10)
            if j == 5:
                cell.number_format = "0.00%"
            elif j in (3, 4):
                cell.number_format = "#,##0"
        r += 1
    tc, tb = sum(v[0] for v in share.values()), sum(v[1] for v in share.values())
    for j, v in enumerate(["Total", "", tc, tb, tc / tb], start=1):
        cell = ws.cell(row=r, column=j, value=v)
        cell.font = Font(name="Calibri", size=10, bold=True)
        cell.border = Border(top=THIN)
        if j == 5:
            cell.number_format = "0.00%"
        elif j in (3, 4):
            cell.number_format = "#,##0"
    ws.freeze_panes = "A5"
    ws2 = wb.create_sheet("Notes")
    ws2["A1"] = "2027 operating plan workbook, first-time-employer line"
    ws2["A1"].font = Font(name="Calibri", size=13, bold=True, color=GREEN)
    notes = [
        "Owner: Revenue Planning, FP&A (%s)." % P["planning"],
        "Sizing: the 2027 sizing standard (1 September 2026).",
        "Share 2025 refreshed by Sales Operations on 15 October 2026 from the BFS October 2026 release.",
        "Sign-off: the CFO (%s) signs the operating plan on Friday 16 October 2026." % P["cfo"],
    ]
    for i, t in enumerate(notes, start=3):
        ws2.cell(row=i, column=1, value=t).font = Font(name="Calibri", size=10)
    ws2.column_dimensions["A"].width = 100
    wb.save(path)


DICT = [
    (R.F_BFS, "cell_value", "The statistic's value for the series, adjustment, month and state."),
    (R.F_BFS, "data_type_code", "Series: BA_BA business applications; BA_HBA high-propensity business applications; "
     "BA_WBA business applications with planned wages; BA_CBA business applications from corporations; BF_BF4Q "
     "business formations within four quarters; BF_BF8Q business formations within eight quarters; BF_DUR4Q and "
     "BF_DUR8Q average duration in quarters from application to formation, within four and eight quarters."),
    (R.F_BFS, "seasonally_adj", "yes for seasonally adjusted values, no for not adjusted."),
    (R.F_BFS, "time", "Month of the application (YYYY-MM). A formation series is published for an application month "
     "once its window and the payroll filings behind it have closed: in this release, formations within four "
     "quarters through June 2025 applications and within eight quarters through June 2024."),
    (R.F_BFS, "state", "State FIPS code."),
    (R.F_BFS, "time_slot_id, error_data, category_code", "Census API fields: 0; no; TOTAL (all industries)."),
    (R.F_BFS_APR, "sa", "A seasonally adjusted, U not adjusted."),
    (R.F_BFS_APR, "series, geo, year, jan to dec", "Series code as in the API pull; state postal code; year; monthly "
     "values (blank where the release has none)."),
    (R.F_ACCOUNTS, "account_id", "Current account number (KP and seven digits). Legacy clients were renumbered at the "
     "June 2024 migration (see the crosswalk)."),
    (R.F_ACCOUNTS, "ein", "Federal employer identification number on the account."),
    (R.F_ACCOUNTS, "legal_name, dba_name", "Legal name and trade name on the account."),
    (R.F_ACCOUNTS, "entity_type, naics", "Entity type and industry code (NAICS 2022) given at onboarding."),
    (R.F_ACCOUNTS, "address_state", "State of the business address on the account at the extract."),
    (R.F_ACCOUNTS, "opened_at", "When the account was opened: UTC on the current system; accounts opened on the legacy "
     "system keep their legacy client-since stamp (Eastern time, month/day/year)."),
    (R.F_ACCOUNTS, "first_pay_date", "First pay date run on the account."),
    (R.F_ACCOUNTS, "first_time_employer", "Onboarding answer: Y when the business has not paid employees before."),
    (R.F_ACCOUNTS, "previous_provider", "Who ran the business's payroll before, from onboarding."),
    (R.F_ACCOUNTS, "signup_channel", "How the client came to us. Accounts loaded at the June 2024 migration carry the "
     "legacy referral source as the migration load mapped it."),
    (R.F_ACCOUNTS, "pay_frequency, employees_at_signup", "Pay schedule; employees on the first payroll."),
    (R.F_ACCOUNTS, "product, product_since", "Current product (Payroll; Payroll + HR; Tax filing only) and the date it "
     "took effect when it changed after opening."),
    (R.F_ACCOUNTS, "status, cancelled_on", "Account status at the extract and the cancellation date."),
    (R.F_XWALK, "legacy_client_no, account_id", "Legacy client number and the current account it was loaded as."),
    (R.F_XWALK, "legacy_source_code", "Referral source on the legacy client record: ACCT accountant referral; CPA "
     "accountant referral (2022 referral form); BANK bank partner; BP bank partner (branch programme); WEB web "
     "sign-up; OUT outbound; TEL outbound (telesales); MKT partner marketplace; APX partner marketplace (app "
     "directory listing)."),
    (R.F_XWALK, "status_at_migration, migrated_at", "Client status on the legacy system at the load; load time (UTC)."),
    (R.F_LEGACY, "client_no", "Legacy client number."),
    (R.F_LEGACY, "tax_year, tax_qtr", "Calendar year and quarter of the pay date."),
    (R.F_LEGACY, "pay_group", "Legacy pay group code."),
    (R.F_LEGACY, "check_dates, employees_paid", "Pay dates in the quarter; employees paid."),
    (R.F_LEGACY, "gross_wages", "Gross wages, cents."),
    (R.F_WAGES, "account_id", "Current account number."),
    (R.F_WAGES, "quarter", "Calendar quarter of the pay date (YYYY-Qn)."),
    (R.F_WAGES, "pay_dates, employees_paid", "Pay dates in the quarter; employees paid."),
    (R.F_WAGES, "gross_wages", "Gross wages on the account's returns for the quarter, dollars."),
    (R.F_REG, "account_id, state", "Account and the state it is registered in for withholding and unemployment tax."),
    (R.F_REG, "withholding_account, ui_account", "State withholding and unemployment insurance account numbers."),
    (R.F_REG, "liability_date", "Liability date on the state registration."),
    (R.F_REG, "kilbourne_from, kilbourne_to", "Dates we filed in the state for the account (blank: still filing)."),
    (R.F_SUTA, "transfer_no", "Payroll tax team's transfer number."),
    (R.F_SUTA, "state, effective_date", "State and date of the transfer."),
    (R.F_SUTA, "predecessor_ein, predecessor_name, successor_ein, successor_name",
     "Successor-employer transfers we filed with the states: a client's business passes to a successor employer, a "
     "new entity carrying it on under a new EIN, and the state unemployment experience and wage base move with it."),
    (R.F_SUTA, "transfer, filed_on", "Total or partial transfer; date we filed it."),
    (R.F_TERR, "state, state_name, territory", "The 2025 sales territory of each core state."),
    (F_LOG, "Logged, State, Effective, Change type, Change, Source", "Research log of state business filing changes: "
     "the day it was logged, the state, the state's effective date, the kind of change, what changed and where it "
     "was announced."),
    (R.F_NES, "NESTAB, NRCPTOT", "Census nonemployer statistics, 2023: nonemployer establishments and their receipts "
     "($1,000), by state and NAICS sector."),
    (F_PLAN, "Share 2025", "State, 2025 first-time employers, formations base and share (see the tab's note)."),
]


def write_dictionary(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fields"
    _title(ws, "Planning pack field guide", "FP&A, for the 2027 plan pack. Field descriptions as each owner keeps "
           "them.", "C")
    _head(ws, 4, ["File", "Field", "Description"], [40, 30, 100])
    for i, (f, fld, d) in enumerate(DICT, start=5):
        for c, v in enumerate((f, fld, d), start=1):
            cell = ws.cell(row=i, column=c, value=v)
            cell.font = Font(name="Calibri", size=10)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A5"
    wb.save(path)


MANIFEST_COLS = ["file", "provided_by", "source", "as_of", "covers"]


def manifest_rows():
    return [
        [R.F_BFS, "Market Research (%s)" % P["research"], "U.S. Census Bureau, Business Formation Statistics, API "
         "pull of the October 2026 release (public domain)", "2026-10-14", "12 core states, applications January 2022 "
         "to September 2026"],
        [R.F_BFS_APR, "Market Research (%s)" % P["research"], "U.S. Census Bureau, Business Formation Statistics, "
         "monthly download of the April 2026 release (public domain)", "2026-04-15", "12 core states, applications "
         "January 2022 to March 2026"],
        [R.F_NES, "Market Research (%s)" % P["research"], "U.S. Census Bureau, Nonemployer Statistics 2023 (public "
         "domain)", "2026-05-28", "12 core states by NAICS sector"],
        [F_LOG, "Market Research (%s)" % P["research"], "Research log", "2026-10-14", "Changes logged since 2023"],
        [R.F_ACCOUNTS, "Sales Operations (%s)" % P["salesops"], "Current account system, year-end planning extract",
         "2026-01-09", "Accounts with a first pay date from January 2022 to December 2025"],
        [R.F_WAGES, "Sales Operations (%s)" % P["salesops"], "Current account system, year-end planning extract",
         "2026-01-09", "Pay dates 17 June 2024 to 31 December 2025"],
        [R.F_REG, "Sales Operations (%s)" % P["salesops"], "Current account system, year-end planning extract",
         "2026-01-09", "Registrations of the accounts in the onboarding export"],
        [R.F_XWALK, "Sales Operations (%s)" % P["salesops"], "Migration load log", "2024-06-15",
         "Legacy clients loaded to the current system"],
        [R.F_LEGACY, "Sales Operations (%s)" % P["salesops"], "Legacy client system, quarterly wage report (archive)",
         "2024-06-15", "Legacy clients with a first pay date from January 2022; pay dates to 14 June 2024"],
        [R.F_SUTA, "Payroll Tax", "Successor transfer register", "2026-03-02", "Transfers effective 2022 to 2025"],
        [R.F_TERR, "Sales Operations (%s)" % P["salesops"], "2025 territory map", "2025-01-06", "12 core states"],
        [F_NOTES, "Sales Operations (%s)" % P["salesops"], "Counting notes", "2026-02-03", ""],
        [F_STANDARD, "FP&A (%s)" % P["planning"], "2027 plan sizing standard", "2026-09-01", ""],
        [F_PLAN, "FP&A (%s)" % P["planning"], "Plan workbook (share tab by Sales Operations)", "2026-10-15", ""],
        [F_DICT, "FP&A (%s)" % P["planning"], "Field guide", "2026-10-15", ""],
    ]


def write_all(out, share):
    p = lambda f: os.path.join(out, f)
    write_standard(p(F_STANDARD))
    write_notes(p(F_NOTES))
    write_log(p(F_LOG))
    write_plan(p(F_PLAN), share)
    write_dictionary(p(F_DICT))
    K.write_csv(p(F_MANIFEST), MANIFEST_COLS, manifest_rows())
    PP.normalize_docx(p(F_STANDARD), P["planning"], P["planning"], "2026-08-27T14:12:00Z", "2026-09-01T15:46:00Z",
                      revision=9, total_time=143, seed="task163/standard",
                      title="2027 operating plan: sizing the first-time-employer line")
    PP.normalize_docx(p(F_NOTES), P["salesops"], P["salesops"], "2026-02-02T19:05:00Z", "2026-02-03T16:30:00Z",
                      revision=5, total_time=52, seed="task163/counting-notes",
                      title="First-time employers: how we count them")
    PP.normalize_ooxml(p(F_LOG), P["research"], P["research"], "2023-07-06T13:44:00Z", "2026-02-04T15:20:00Z",
                       excel=True)
    PP.normalize_ooxml(p(F_PLAN), P["planning"], P["salesops"], "2026-08-31T16:02:00Z", "2026-10-15T18:37:00Z",
                       excel=True)
    PP.normalize_ooxml(p(F_DICT), P["planning"], P["planning"], "2026-10-15T19:10:00Z", "2026-10-15T20:02:00Z",
                       excel=True)
