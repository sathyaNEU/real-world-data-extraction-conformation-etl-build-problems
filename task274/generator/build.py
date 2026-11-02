"""task274 pack builder: writes target/, golden/, generator/figures.json and metadata.json.

    python3 task274/generator/build.py

Deterministic: two runs produce byte-identical files (checks.py and verify.py assert the figures; the
rebuild check compares digests).
"""
import datetime as dt
import json
import os
from collections import Counter, defaultdict

import numpy as np

import fileutil as FU
import records as R
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
D = dt.date
WHEN = dt.datetime(2026, 9, 1, 8, 0, 0)

FILES = dict(
    legacy_events="legacy_docket_events_2025_2026.csv",
    cms_events="cms_docket_events_2026.csv",
    legacy_charges="legacy_case_charges.csv",
    cms_charges="cms_case_charges.csv",
    roster="diversion_lottery_draws_2025_2026.xlsx",
    codes="legacy_event_codes.csv",
    conversion="penal_code_conversion_table_2026.csv",
    resolution="board_resolution_2025_31.pdf",
    agreement="nethercote_services_agreement_2025.pdf",
    policy="pretrial_diversion_policy_pdu_2026_01.docx",
    court_stats="district_court_annual_statistics_fy2025.pdf",
    jail="county_jail_population_2025_2026.csv",
)
REPORT_DIR = "nethercote_reports"


def hm(h):
    return "%d:%02d" % (int(h), int(round((h - int(h)) * 60)))


# ---------------------------------------------------------------------------------------------------------
# data files


def write_data(A):
    FU.write_csv(os.path.join(TARGET, FILES["legacy_events"]),
                 ["case_number", "division", "event_date", "event_code", "event_description", "clerk"], A["legacy_ev"])
    FU.write_csv(os.path.join(TARGET, FILES["cms_events"]),
                 ["case_number", "court_division", "event_timestamp_utc", "event_type", "event_detail", "entry_source"],
                 A["cms_ev"])
    FU.write_csv(os.path.join(TARGET, FILES["legacy_charges"]),
                 ["case_number", "division", "case_type", "filed_date", "party_id", "defendant_name", "birth_date",
                  "offense_date", "charge_seq", "statute_section"], A["legacy_ch"])
    FU.write_csv(os.path.join(TARGET, FILES["cms_charges"]),
                 ["case_number", "court_division", "case_category", "filing_date", "defendant", "date_of_birth",
                  "offense_date", "count_number", "statute_section"], A["cms_ch"])
    FU.write_csv(os.path.join(TARGET, FILES["codes"]), ["event_code", "description"],
                 [(k, v) for k, v in R.LEG.items()])
    conv = [(o[2], o[0], o[3], o[0]) for o in sorted(W.OFFENCES, key=lambda o: o[2])]
    FU.write_csv(os.path.join(TARGET, FILES["conversion"]),
                 ["section_2025", "offense_title_2025", "section_2026", "offense_title_2026"], conv)
    write_roster(A)
    write_reports(A)
    write_jail()


def write_roster(A):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    wb.remove(wb.active)
    for L in range(12):
        ld = W.LOTTERY_DATES[L]
        pm = W.add_months(ld, -1)
        ws = wb.create_sheet(ld.strftime("%Y-%m"))
        lines = A["roster"][L]
        pol = "PDU-2025-02" if pm < D(2026, 1, 1) else "PDU-2026-01"
        ws.append(["LARKMOOR COUNTY PROSECUTING ATTORNEY - PRETRIAL DIVERSION UNIT"])
        ws.append(["Diversion lottery: draw of %s" % ld.strftime("%d %B %Y").lstrip("0")])
        ws.append(["List: defendants arraigned %s to %s found eligible under %s" % (
            pm.strftime("%d %B %Y").lstrip("0"), W.month_end(pm).strftime("%d %B %Y").lstrip("0"), pol)])
        ws.append(["Places offered: %d of %d listed (Board Resolution 2025-31, section 2)" % (len(lines) // 2, len(lines))])
        ws.append([])
        ws.append(["Case No.", "Defendant", "Division", "Arraigned", "Lead count (section)", "Offered"])
        ws["A1"].font = Font(bold=True)
        for cell in ws[6]:
            cell.font = Font(bold=True)
        for num, name, div, arr, code, off in lines:
            ws.append([num, name, div, arr.strftime("%m/%d/%Y"), code, off])
        ws.append([])
        ws.append(["Draw conducted by M. Nielsen, Chief Deputy Prosecuting Attorney; witnessed by A. Aguilar, Court Administration"])
        ws.column_dimensions["A"].width = 18
        ws.column_dimensions["B"].width = 28
        ws.column_dimensions["E"].width = 20
    FU.fix_xlsx_props(wb, dt.datetime(2025, 6, 5, 10, 12), "Pretrial Diversion Unit")
    p = os.path.join(TARGET, FILES["roster"])
    wb.save(p)
    FU.normalise_zip(p, modified=dt.datetime(2026, 5, 7, 11, 40))


def report_name(label, start, system):
    if system == "old":
        return "Nethercote_Monthly_Report_%s.xlsx" % start.strftime("%b%Y")
    return "NCJS_Larkmoor_Participants_%s.xlsx" % start.strftime("%Y-%m")


def write_reports(A):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    parts = A["parts"]
    os.makedirs(os.path.join(TARGET, REPORT_DIR), exist_ok=True)
    rng = R.rng_for(7)
    for label, start, end, system in R.report_months():
        rows = R.report_rows(parts, start, end, system)
        wb = Workbook()
        ws = wb.active
        if system == "old":
            ws.title = "Participants"
            run = (end + dt.timedelta(1)) if end.day == 15 else (end + dt.timedelta(int(rng.integers(3, 8))))
            ws.append(["Nethercote Community Justice Services"])
            ws.append(["Larkmoor County Pretrial Diversion - Monthly Participant Report"])
            ws.append(["Report month: %s" % label])
            hh, mi = int(rng.integers(7, 10)), int(rng.integers(0, 60))
            ws.append(["Run: %s %02d:%02d" % (run.strftime("%m/%d/%Y"), hh, mi)])
            ws.append(["Prepared by: N. Hansen"])
            ws.append([])
            ws.append(["Client No", "Client Name", "Court Ref", "Site", "Term Start", "Term End", "Status", "Exit Date",
                       "Exit Type", "CS Hrs", "Restitution Rcvd"])
            hdr = 7
            rows.sort(key=lambda r: r["p"]["client_no"])
            for r in rows:
                p = r["p"]
                c = p["case"]
                ws.append([p["client_no"], p["name"], p["ref"], p["site"], c.term_start.strftime("%d-%b-%y"),
                           c.term_end.strftime("%d-%b-%y"), r["status"],
                           r["exit_date"].strftime("%d-%b-%y") if r["exit_date"] else "", r["exit_txt"], hm(r["hrs"]),
                           round(float(r["pay"]), 2)])
            ws.append([])
            ws.append(["Enrolled during month: %d" % len(rows)])
        else:
            ws.title = "Report"
            gen = end + dt.timedelta(int(rng.integers(2, 6)))
            ws.append(["Nethercote Community Justice Services - Participant Report"])
            ws.append(["County: Larkmoor | Period: %s" % label])
            hh, mi = int(rng.integers(7, 10)), int(rng.integers(0, 60))
            ws.append(["Generated: %s %02d:%02d" % (gen.isoformat(), hh, mi)])
            ws.append(["Prepared by: Natalie Hansen, Data Coordinator"])
            ws.append([])
            ws.append(["Participant ID", "Participant Name", "Case Number", "Location", "Program Start", "Program End",
                       "Status", "Discharge Date", "Discharge Reason", "Community Service Hours", "Restitution"])
            hdr = 6
            rows.sort(key=lambda r: r["p"]["pid_new"])
            for r in rows:
                p = r["p"]
                c = p["case"]
                casenum = c.number_legacy if c.number_legacy else c.number_cms
                ws.append([p["pid_new"], p["name"], casenum, p["site"], c.term_start.isoformat(), c.term_end.isoformat(),
                           r["status"], r["exit_date"].isoformat() if r["exit_date"] else "", r["exit_txt"],
                           round(float(r["cum"]), 1), round(float(r["pay"]) * (1 - R.RETENTION), 2)])
        ws["A1"].font = Font(bold=True)
        for cell in ws[hdr]:
            cell.font = Font(bold=True)
        for col, w in zip("ABCDEFGHIJK", (12, 24, 20, 15, 12, 12, 11, 12, 30, 14, 14)):
            ws.column_dimensions[col].width = w
        day = run if system == "old" else gen
        stamp = dt.datetime(day.year, day.month, day.day, hh, mi)
        FU.fix_xlsx_props(wb, stamp, "Nethercote Community Justice Services")
        p = os.path.join(TARGET, REPORT_DIR, report_name(label, start, system))
        wb.save(p)
        FU.normalise_zip(p, modified=stamp)


def write_jail():
    rng = R.rng_for(8)
    rows = []
    level = {"Larkmoor County Detention Center": 1180.0, "Bramwick Annex": 214.0}
    season = [0.97, 0.96, 0.99, 1.0, 1.02, 1.03, 1.04, 1.03, 1.01, 1.0, 0.98, 0.95]
    m = D(2025, 1, 1)
    while m <= D(2026, 8, 1):
        for fac in level:
            base = 1180.0 if fac.startswith("Larkmoor") else 214.0
            level[fac] = 0.8 * level[fac] + 0.2 * base * (1 - 0.002 * ((m.year - 2025) * 12 + m.month)) + rng.normal(0, 0.012 * base)
            adp = int(round(level[fac] * season[m.month - 1]))
            days = (W.add_months(m, 1) - m).days
            bookings = int(round(adp * 2.05 * days / 30.4 + rng.normal(0, 0.03 * adp)))
            rows.append((m.strftime("%Y-%m"), fac, adp, bookings, int(round(adp * (0.70 + rng.normal(0, 0.012))))))
        m = W.add_months(m, 1)
    FU.write_csv(os.path.join(TARGET, FILES["jail"]),
                 ["month", "facility", "average_daily_population", "bookings", "pretrial_detainees_adp"], rows)


# ---------------------------------------------------------------------------------------------------------
# governing documents and the distractor report


def pdf_doc(path, title, blocks):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    from reportlab.lib import colors
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Times-Roman", fontSize=10.5, leading=14)
    head = ParagraphStyle("h", parent=ss["Normal"], fontName="Times-Bold", fontSize=12, leading=15, alignment=1)
    sub = ParagraphStyle("s", parent=ss["Normal"], fontName="Times-Bold", fontSize=10.5, leading=14)
    doc = SimpleDocTemplate(path, pagesize=letter, invariant=1, title=title, author="", subject="", creator="",
                            producer="", leftMargin=inch, rightMargin=inch, topMargin=0.9 * inch, bottomMargin=0.9 * inch)
    story = []
    for kind, content in blocks:
        if kind == "h":
            story.append(Paragraph(content, head))
        elif kind == "s":
            story.append(Paragraph(content, sub))
        elif kind == "p":
            story.append(Paragraph(content, body))
        elif kind == "sp":
            story.append(Spacer(1, content))
        elif kind == "t":
            t = Table(content, hAlign="LEFT")
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Times-Roman", 9.5),
                                   ("FONT", (0, 0), (-1, 0), "Times-Bold", 9.5),
                                   ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                                   ("ALIGN", (1, 1), (-1, -1), "RIGHT")]))
            story.append(t)
        story.append(Spacer(1, 6))
    doc.build(story)


def write_documents():
    res = [
        ("h", "LARKMOOR COUNTY BOARD OF COMMISSIONERS"),
        ("h", "RESOLUTION NO. 2025-31"),
        ("p", "<b>A resolution authorizing a pretrial diversion pilot and a services agreement with Nethercote Community "
              "Justice Services, and setting the terms of the pilot's evaluation and of the agreement's renewal.</b>"),
        ("p", "Adopted 22 April 2025."),
        ("p", "WHEREAS the Prosecuting Attorney proposes that first-time defendants charged with eligible offenses be "
              "offered pretrial diversion before plea, under which the case is continued while the defendant completes "
              "a program of case management, classes, community service and restitution, and is dismissed when the "
              "program is completed;"),
        ("p", "WHEREAS Nethercote Community Justice Services can supervise about half of the defendants the Prosecuting "
              "Attorney expects to find eligible each month, and the Board wishes to learn what the program achieves "
              "before it funds a place for every eligible defendant;"),
        ("p", "NOW, THEREFORE, BE IT RESOLVED by the Board of Commissioners of Larkmoor County:"),
        ("s", "Section 1. Pilot."),
        ("p", "The County shall fund a pretrial diversion pilot from 1 June 2025, delivered by Nethercote Community "
              "Justice Services under the agreement authorized in Section 4."),
        ("s", "Section 2. Allocation of places."),
        ("p", "Because places are fewer than eligible defendants, the Prosecuting Attorney's Pretrial Diversion Unit "
              "shall, in each month from June 2025 to May 2026, list the defendants arraigned in the preceding month "
              "whom it finds eligible under its policy, and offer a place to one half of the list, rounded down, chosen "
              "by random draw. A defendant who is not offered a place shall be prosecuted in the ordinary way and shall "
              "not be offered a place later in the pilot. A defendant who is offered a place may decline it."),
        ("s", "Section 3. Evaluation."),
        ("p", "By 30 September 2026 the County Administrator shall report to the Board the pilot's effect on conviction, "
              "estimated from the courts' records to 31 August 2026: the share of the defendants on the lottery lists "
              "who are convicted in the referred case at its final disposition, for those not offered a place less "
              "that for those offered one, in percentage points. Every defendant on a list counts, whether or not a "
              "defendant offered a place took it up. A case that has not reached its final disposition by 31 August "
              "2026 counts by how it will end, not as a case without a conviction."),
        ("s", "Section 4. Services agreement."),
        ("p", "The County Administrator is authorized to execute the pretrial diversion services agreement with "
              "Nethercote Community Justice Services for the period 1 June 2025 to 31 December 2026 in the form "
              "presented to the Board, at a cost not to exceed the amounts appropriated for the pilot."),
        ("s", "Section 5. Renewal."),
        ("p", "On receiving the report under Section 3 the Board will act on the agreement for 2027 as follows: (a) "
              "where the reported reduction is 25 percentage points or more, renew the agreement at full scale, so that "
              "a place is offered to every eligible defendant; (b) where it is 15 percentage points or more but less "
              "than 25, renew the agreement at the pilot's scale; (c) where it is less than 15 percentage points, let "
              "the agreement lapse at the end of its term."),
        ("s", "Section 6. Fiscal year."),
        ("p", "The County's fiscal year runs from 1 July to 30 June; fiscal year 2026 is the year that ends on 30 June 2026."),
        ("sp", 14),
        ("p", "ADOPTED by the Board of Commissioners of Larkmoor County on 22 April 2025."),
        ("p", "Chair, Board of Commissioners"),
        ("p", "ATTEST: Clerk of the Board"),
    ]
    pdf_doc(os.path.join(TARGET, FILES["resolution"]), "Resolution 2025-31", res)
    FU.finish_pdf(os.path.join(TARGET, FILES["resolution"]), "Larkmoor County", "Clerk of the Board",
                  dt.datetime(2025, 4, 23, 10, 15))

    agr = [
        ("h", "PRETRIAL DIVERSION SERVICES AGREEMENT"),
        ("p", "This agreement is made on 20 May 2025 between Larkmoor County (the County) and Nethercote Community "
              "Justice Services (Nethercote), under Resolution No. 2025-31 of the Board of Commissioners."),
        ("s", "1. Term"),
        ("p", "This agreement runs from 1 June 2025 to 31 December 2026 unless ended earlier under clause 10."),
        ("s", "2. Services"),
        ("p", "Nethercote shall deliver the County's pretrial diversion program to every defendant who signs a pretrial "
              "diversion agreement with the Prosecuting Attorney under the pilot: an intake assessment, case "
              "management, cognitive skills classes, supervision of community service and the collection of "
              "restitution. Nethercote shall deliver the program from its sites at Larkmoor City, Bramwick, Wendmoor "
              "and Strandham, assigning each participant to the site nearest the participant's home."),
        ("s", "3. Program term and conditions"),
        ("p", "Each participant's program term begins on the first day of the month following the date the diversion "
              "agreement is filed with the court and ends twelve months later. The conditions are those of the "
              "participant's diversion agreement, including community service of 24 hours on a misdemeanor and 40 "
              "hours on a felony and payment in full of any restitution agreed."),
        ("s", "4. Places"),
        ("p", "Nethercote shall hold places for up to 1,150 participants at any one time."),
        ("s", "5. Fees"),
        ("p", "The County shall pay Nethercote an intake fee of 350 dollars for each participant and a monthly fee of "
              "410 dollars for each participant enrolled on any day of a calendar month, invoiced monthly in arrears."),
        ("s", "6. Restitution"),
        ("p", "Nethercote shall receive restitution payments from participants, may retain five percent of each "
              "payment towards its collection costs, and shall remit the balance to the Clerk of the District Court by "
              "the tenth day of the month following receipt."),
        ("s", "7. Reporting"),
        ("p", "By the tenth day of each month Nethercote shall send the County Administrator a participant report for "
              "the preceding month, listing each participant enrolled on any day of that month with the participant's "
              "court case reference, site, program term, status and any discharge, community service hours and "
              "restitution."),
        ("s", "8. Records"),
        ("p", "Nethercote shall keep its participant records for six years after this agreement ends and make them "
              "available to the County on request."),
        ("s", "9. Fiscal year"),
        ("p", "Payments under this agreement are subject to appropriation in each County fiscal year, which runs from "
              "1 July to 30 June."),
        ("s", "10. Termination"),
        ("p", "Either party may end this agreement on ninety days' written notice."),
        ("sp", 14),
        ("p", "For Nethercote Community Justice Services: Roy Goodwin, Director of Programs"),
        ("p", "For Larkmoor County: County Administrator"),
    ]
    pdf_doc(os.path.join(TARGET, FILES["agreement"]), "Pretrial Diversion Services Agreement", agr)
    FU.finish_pdf(os.path.join(TARGET, FILES["agreement"]), "Larkmoor County", "County Administrator's Office",
                  dt.datetime(2025, 5, 20, 15, 40))

    write_policy()

    stats = [("h", "LARKMOOR COUNTY DISTRICT COURT"), ("h", "Annual Statistical Report, Fiscal Year 2025"),
             ("p", "Office of the Court Administrator. Fiscal year 2025 ran from 1 July 2024 to 30 June 2025."),
             ("s", "Table 1. Criminal cases filed, by division and case type")]
    rng = R.rng_for(9)
    t1 = [["Division", "Misdemeanor", "Felony", "Total"]]
    tot = [0, 0]
    for dv, sh in zip(W.DIVISIONS, W.DIV_SHARE):
        cm = int(8150 * sh + rng.integers(-60, 61))
        cr = int(2310 * sh + rng.integers(-25, 26))
        tot[0] += cm
        tot[1] += cr
        t1.append([W.DIV_NAME[dv], "{:,}".format(cm), "{:,}".format(cr), "{:,}".format(cm + cr)])
    t1.append(["All divisions", "{:,}".format(tot[0]), "{:,}".format(tot[1]), "{:,}".format(sum(tot))])
    stats += [("t", t1), ("s", "Table 2. Criminal cases disposed, by manner of disposition")]
    t2 = [["Manner", "Misdemeanor", "Felony"], ["Plea of guilty", "4,912", "1,402"], ["Found guilty at trial", "214", "131"],
          ["Dismissed", "1,766", "386"], ["Nolle prosequi", "794", "171"], ["Acquitted", "103", "39"]]
    stats += [("t", t2), ("s", "Table 3. Median days from filing to disposition"),
              ("t", [["Division", "Misdemeanor", "Felony"], ["Larkmoor City", "101", "171"], ["Bramwick", "96", "158"],
                     ["Wendmoor", "108", "176"], ["Strandham", "92", "149"]])]
    pdf_doc(os.path.join(TARGET, FILES["court_stats"]), "Annual Statistical Report FY2025", stats)
    FU.finish_pdf(os.path.join(TARGET, FILES["court_stats"]), "Larkmoor County District Court",
                  "Office of the Court Administrator", dt.datetime(2025, 9, 12, 9, 5))


def write_policy():
    from docx import Document
    from docx.shared import Pt
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    doc.add_heading("Larkmoor County Prosecuting Attorney", level=1)
    doc.add_paragraph("Pretrial Diversion Unit Policy PDU-2026-01: Eligibility for pretrial diversion")
    doc.add_paragraph("Effective 1 January 2026. Replaces PDU-2025-02.")
    doc.add_heading("1. Purpose", level=2)
    doc.add_paragraph("This policy sets which defendants and which cases the Unit may offer pretrial diversion, and "
                      "how places are offered while the County's pilot runs under Board Resolution 2025-31. It restates "
                      "the eligible offenses under the state penal code as renumbered with effect from 1 January 2026.")
    doc.add_heading("2. Eligible defendants", level=2)
    doc.add_paragraph("A defendant is eligible who has no prior conviction, no other pending criminal case and is not "
                      "on probation or parole when the case is filed.")
    doc.add_heading("3. Eligible offenses", level=2)
    doc.add_paragraph("A case is eligible when every count charges an offense in one of the classes below.")
    tbl = doc.add_table(rows=1, cols=3)
    tbl.style = "Table Grid"
    h = tbl.rows[0].cells
    h[0].text, h[1].text, h[2].text = "Class", "Section", "Offense"
    for cls in "ABCDE":
        for o in W.OFFENCES:
            if o[1] == cls:
                r = tbl.add_row().cells
                r[0].text, r[1].text, r[2].text = "%s, %s" % (cls, W.CLASS_NAME[cls].lower()), o[3], o[0]
    doc.add_heading("4. Monthly list and draw", level=2)
    doc.add_paragraph("While the pilot runs, the Unit lists in the first week of each month the eligible defendants "
                      "arraigned in the preceding month, and offers places by random draw as section 2 of Board "
                      "Resolution 2025-31 requires. The draw is witnessed by Court Administration.")
    doc.add_heading("5. Exclusions", level=2)
    doc.add_paragraph("A case is not eligible where the victim objects in writing to diversion, where restitution "
                      "agreed would exceed 2,000 dollars, or where the defendant has had pretrial diversion before.")
    doc.add_paragraph("")
    doc.add_paragraph("Melanie Nielsen, Chief Deputy Prosecuting Attorney")
    FU.fix_docx_props(doc, dt.datetime(2025, 12, 15, 14, 5), "Pretrial Diversion Unit")
    p = os.path.join(TARGET, FILES["policy"])
    doc.save(p)
    FU.normalise_zip(p, modified=dt.datetime(2025, 12, 15, 14, 5))


# ---------------------------------------------------------------------------------------------------------
# the golden figures


def golden_figures(A):
    rows = A["main_rows"]
    o = W.routes(rows)
    cases = A["cases"]
    fy = lambda d: W.FY_START <= d <= W.FY_END
    cls = Counter()
    div = Counter()
    for c in cases:
        if fy(c.filed) and c.charges[0][1]:
            cls[c.charges[0][1]] += 1
            div[c.division] += 1
    hours = Counter()
    rest = Counter()
    for p in A["parts"]:
        hours[p["site"]] += sum(h for d, h in p["shifts"] if fy(d))
        rest[p["site"]] += sum(a for d, a in p["pays"] if fy(d))
    # chart: each arm's share convicted by months since the draw as the records stand (Aalen-Johansen)
    curve = {}
    for a, lab in ((0, "not_offered"), (1, "offered")):
        T, C = [], []
        for r in rows:
            if (1 if r["offered"] else 0) != a:
                continue
            fu = (W.CUT - r["draw"]).days
            if r["disp"] <= W.CUT:
                T.append((r["disp"] - r["draw"]).days)
                C.append(1 if r["convicted"] else 2)
            else:
                T.append(fu)
                C.append(0)
        curve[lab] = [round(100 * W.aj_cif(T, C, int(round(m * 30.44))), 2) for m in range(0, 15)]
    eff = o["golden"]
    call = ("Renew the agreement for 2027 at full scale" if eff >= W.FULL_AT else
            "Renew the agreement for 2027 at the pilot's scale" if eff >= W.PILOT_AT else "Let the agreement lapse")
    F = dict(
        call=call,
        cut_points=round(eff),
        cut_unrounded=round(eff, 3),
        share_not_offered=round(o["not_offered"]),
        share_offered=round(o["offered"]),
        termination_chance=round(o["p_term"]),
        terminated_convicted=round(o["c_term"]),
        declined_share=round(o["p_decline"]),
        declined_convicted=round(o["c_declined"]),
        final_review_rate=round(o["final_review_rate"]),
        recorded_cut_at_cut=round(o["naive"]),
        cif_longest_points=round(o["cif_max"]),
        recorded_not_offered=round(o["recorded_not_offered"]),
        recorded_offered=round(o["recorded_offered"]),
        open_offered=o["open_offered"],
        n_listed=o["n"], n_offered=o["n_offered"], n_not_offered=o["n_not_offered"],
        n_participants=o["n_participants"],
        filings_by_class={W.CLASS_NAME[k]: cls[k] for k in "ABCDE"},
        filings_by_division={W.DIV_NAME[k]: div[k] for k in W.DIVISIONS},
        filings_total=sum(cls.values()),
        hours_by_site={s: int(round(hours[s])) for s in W.SITES},
        restitution_by_site={s: int(round(rest[s])) for s in W.SITES},
        full_scale_at=W.FULL_AT,
        pilot_scale_at=W.PILOT_AT,
        evaluation_date="%d %s %d" % (W.CUT.day, W.CUT.strftime("%B"), W.CUT.year),
        evaluation_year=W.CUT.year,
        new_system_from="%d %s %d" % (W.NETHERCOTE_SWITCH.day, W.NETHERCOTE_SWITCH.strftime("%B"), W.NETHERCOTE_SWITCH.year),
        retention_percent=int(round(100 * R.RETENTION)),
        remitted_share=round(1 - R.RETENTION, 2),
        chart_months=len(curve["offered"]) - 1,
        curve=curve,
        routes={k: round(v, 3) for k, v in o.items() if isinstance(v, float)},
    )
    return F, o


def write_chart(F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    blue, orange, ink, ink2, grid, surface = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5})
    fig, ax = plt.subplots(figsize=(8.0, 4.6), dpi=120)
    fig.patch.set_facecolor(surface)
    ax.set_facecolor(surface)
    months = list(range(0, 15))
    no, off = F["curve"]["not_offered"], F["curve"]["offered"]
    ax.plot(months, no, color=blue, lw=2, solid_capstyle="round", label="Not offered a place, convicted as recorded")
    ax.plot(months, off, color=orange, lw=2, solid_capstyle="round", label="Offered a place, convicted as recorded")
    ax.plot([0, 14], [F["share_not_offered"]] * 2, color=blue, lw=1.2, ls=(0, (5, 3)), label="At final disposition")
    ax.plot([0, 14], [F["share_offered"]] * 2, color=orange, lw=1.2, ls=(0, (5, 3)))
    ax.text(14.15, F["share_not_offered"], "%d%% at final disposition" % F["share_not_offered"], va="center", color=ink, fontsize=8.5)
    ax.text(14.15, F["share_offered"], "%d%% at final disposition" % F["share_offered"], va="center", color=ink, fontsize=8.5)
    ax.annotate("", xy=(13.3, F["share_offered"]), xytext=(13.3, F["share_not_offered"]),
                arrowprops=dict(arrowstyle="<->", color=ink2, lw=1))
    ax.text(13.1, (F["share_not_offered"] + F["share_offered"]) / 2, "%d points" % F["cut_points"], ha="right",
            va="center", color=ink, fontsize=9, fontweight="bold")
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 65)
    ax.set_xticks(months)
    ax.set_xlabel("Months since the draw", color=ink2)
    ax.set_ylabel("Convicted in the referred case (%)", color=ink2)
    ax.grid(axis="y", color=grid, lw=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(grid)
    ax.tick_params(colors=ink2, length=0)
    ax.set_title("Conviction by draw result: as recorded to 31 August 2026, and at final disposition", loc="left",
                 color=ink, fontsize=10.5, fontweight="bold")
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, -0.13), ncol=3, frameon=False, fontsize=8, labelcolor=ink2)
    fig.subplots_adjust(left=0.08, right=0.79, top=0.90, bottom=0.22)
    os.makedirs(GOLDEN, exist_ok=True)
    fig.savefig(os.path.join(GOLDEN, "conviction_by_arm_2027.png"), metadata={"Software": None}, facecolor=surface)
    plt.close(fig)


def _footer(doc, text):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    sec = doc.sections[0]
    p = sec.footer.paragraphs[0]
    p.text = text + "   Page "
    run = p.add_run()
    for kind, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = txt
        run._r.append(el)


def _table(doc, header, rows, widths=None):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Light List Accent 1"
    for i, h in enumerate(header):
        t.rows[0].cells[i].text = h
    for r in rows:
        cells = t.add_row().cells
        for i, v in enumerate(r):
            cells[i].text = v
            if i > 0:
                cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for i in range(1, len(header)):
        t.rows[0].cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for row in t.rows:
        for c in row.cells:
            for par in c.paragraphs:
                for run in par.runs:
                    run.font.size = Pt(9.5)
    return t


def _noted(doc, before, mark, after):
    p = doc.add_paragraph()
    p.add_run(before)
    r = p.add_run(mark)
    r.font.superscript = True
    if after:
        p.add_run(after)
    return p


def _source(doc, text):
    from docx.shared import Pt, RGBColor
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x52, 0x51, 0x4E)


def write_memo(F):
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    _footer(doc, "Larkmoor County, County Administrator's Office, Justice Planning")
    doc.add_heading("Pretrial diversion pilot cut convictions by %d points: renew the agreement at the pilot's scale"
                    % F["cut_points"], level=1)
    p = doc.add_paragraph()
    for lab, val in (("To", "Board of Commissioners"), ("From", "County Administrator's Office, Justice Planning"),
                     ("Date", "18 September 2026"),
                     ("Subject", "Pretrial diversion pilot: report under Resolution 2025-31, sections 3 and 5")):
        p.add_run(lab + ": ").bold = True
        p.add_run(val + ("\n" if lab != "Subject" else ""))
    doc.add_heading("Requested action", level=2)
    _noted(doc,
           "%s. Being offered a place in the pilot's lotteries lowers the share of defendants convicted in the referred "
           "case by %d percentage points, from %d%% of defendants not offered a place to %d%% of those offered one." % (
               F["call"], F["cut_points"], F["share_not_offered"], F["share_offered"]), "1",
           " That clears the resolution's 15-point floor for renewal at the pilot's scale and falls short of the 25 "
           "points it sets for full scale.")
    doc.add_heading("What the pilot did to convictions", level=2)
    doc.add_paragraph(
        "The two groups cannot yet be compared as the docket stands. On 31 August, %d%% of defendants not offered a "
        "place had been convicted against %d%% of those offered one, but most offered defendants' cases were still "
        "open, and for a reason that has nothing to do with whether they will end in conviction: a participant's case "
        "is continued for the twelve-month term, can only come back to court if the program terminates them, and "
        "then waits its turn on the trial calendar. The resolution counts every listed defendant by how the case "
        "ends, so each open case has been carried to its end on the rates the records show:" % (
            F["recorded_not_offered"], F["recorded_offered"]))
    for txt in (
        "Defendants not offered a place, and offered defendants who declined, are prosecuted in the ordinary way; "
        "an open case ends as the disposed cases of its group have, %d%% convicted for those not offered and %d%% for "
        "the %d%% of offered defendants who declined." % (F["share_not_offered"], F["declined_convicted"], F["declined_share"]),
        "A participant still in the program fails in the months left on the term at the rate the program terminates "
        "participants month by month, counted over every participant's months on the program. Most terminations "
        "come early, and the review at the end of the term terminates %d%% of the participants who reach it; only "
        "participants from the June, July and August 2025 draws have reached it so far. The chance of termination "
        "within the term is %d%%." % (F["final_review_rate"], F["termination_chance"]),
        "A terminated case is tried on the stipulated record the agreement carries: %d%% of terminated cases already "
        "disposed ended in conviction, against %d%% for defendants never offered diversion." % (
            F["terminated_convicted"], F["share_not_offered"]),
    ):
        doc.add_paragraph(txt, style="List Bullet")
    doc.add_paragraph(
        "On those rates %d%% of offered defendants will be convicted against %d%% of those not offered, a reduction of "
        "%d percentage points. The chart shows why the recorded shares overstate the pilot's effect: the offered "
        "group's recorded share is still rising when the records stop, and the participants terminated at the final "
        "review will not be tried until after the evaluation date." % (
            F["share_offered"], F["share_not_offered"], F["cut_points"]))
    doc.add_picture(os.path.join(GOLDEN, "conviction_by_arm_2027.png"), width=Inches(6.3))
    _source(doc, "Source: Pretrial Diversion Unit lottery lists, June 2025 to May 2026; District Court docket, legacy "
                 "and new case management systems, events to 31 August 2026. Recorded shares are cumulative by month "
                 "since each defendant's draw.")
    doc.add_heading("Sizing full scale: eligible filings in fiscal 2026", level=2)
    _noted(doc,
           "A full-scale program would offer a place to every eligible defendant. As a first measure of that pool, the "
           "table counts the cases filed in fiscal 2026 whose lead charge falls in one of the program's eligible offense "
           "classes, before the Unit's screen for prior record and other exclusions.", "2", "")
    _table(doc, ["Eligible class (PDU-2026-01)", "Cases filed"],
           [[k, "{:,}".format(v)] for k, v in F["filings_by_class"].items()] + [["All eligible classes", "{:,}".format(F["filings_total"])]])
    _source(doc, "Source: District Court charge records, legacy and new systems; penal code conversion table 2026. "
                 "Each charge is read in the section numbering it was entered under.")
    _table(doc, ["Court division", "Eligible cases filed"], [[k, "{:,}".format(v)] for k, v in F["filings_by_division"].items()])
    _source(doc, "Source: as above, by the division in which the case was filed.")
    doc.add_heading("Program delivery under the agreement", level=2)
    doc.add_paragraph("Community service hours participants worked and restitution they paid in fiscal 2026, by the "
                      "Nethercote site that supervised them.")
    _table(doc, ["Site", "Community service hours", "Restitution paid ($)"],
           [[s_, "{:,}".format(F["hours_by_site"][s_]), "{:,}".format(F["restitution_by_site"][s_])] for s_ in W.SITES])
    _source(doc, "Source: Nethercote monthly participant reports, July 2025 to June 2026, from both of its case systems. "
                 "Restitution is what participants paid; Nethercote remits it to the Clerk less the five percent the "
                 "agreement lets it retain (clause 6).")
    p = doc.add_paragraph()
    r = p.add_run("Notes\n1. Shares count every defendant on the monthly lottery lists, whether or not the case had "
                  "ended by 31 August 2026 (Resolution 2025-31, section 3). Shares are rounded to whole percents and "
                  "the reduction is taken before rounding.\n2. Fiscal 2026 runs from 1 July 2025 to 30 June 2026 "
                  "(Resolution 2025-31, section 6).")
    r.font.size = Pt(8.5)
    doc.add_paragraph("Savannah Jordan, Criminal Justice Planner")
    FU.fix_docx_props(doc, dt.datetime(2026, 9, 18, 16, 20), "Justice Planning")
    os.makedirs(GOLDEN, exist_ok=True)
    p = os.path.join(GOLDEN, "diversion_renewal_memo_2027.docx")
    doc.save(p)
    FU.normalise_zip(p, modified=dt.datetime(2026, 9, 18, 16, 20))


def write_metadata(F):
    files = []
    for k, f in FILES.items():
        files.append(f)
    for label, start, end, system in R.report_months():
        files.append(REPORT_DIR + "/" + report_name(label, start, system))
    meta = dict(
        task="task274",
        title="Pretrial diversion pilot: the 2027 agreement",
        domain="Criminology & Justice",
        task_type="intervention-policing-policy-evaluation",
        objective="Experiment & Causal Analysis",
        deliverables=["diversion_renewal_memo_2027.docx", "conviction_by_arm_2027.png"],
        distractors=[FILES["court_stats"], FILES["jail"]],
        files=[dict(path=f, source="synthetic: generated for this task by task274/generator/build.py",
                    date="2026-11-02", license="CC0-1.0") for f in sorted(files)],
        notes="Every person, organization, place and record is fictional.",
    )
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")


def main():
    A = R.build_all()
    os.makedirs(TARGET, exist_ok=True)
    write_data(A)
    write_documents()
    F, o = golden_figures(A)
    write_chart(F)
    write_memo(F)
    write_metadata(F)
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(F, f, indent=1, sort_keys=True)
        f.write("\n")
    export = dt.datetime(2026, 9, 10, 8, 0).timestamp()
    for root, dirs, files in os.walk(TARGET):
        for n in files:
            os.utime(os.path.join(root, n), (export, export))
    print(json.dumps({k: v for k, v in F.items() if k not in ("curve", "routes")}, indent=1))


if __name__ == "__main__":
    main()
