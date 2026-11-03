"""The credit union's own documents: its AML/ATF compliance programme (version 6.1) and the AML
Compliance Committee's terms of reference.

The programme files what the January review tests and how the credit union counts large cash for
reporting. It says nothing about how the cash a member's trade produced is estimated.
"""
import datetime as dt
import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import common as C

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Helvetica", fontSize=9, leading=12.4,
                      alignment=TA_JUSTIFY, spaceAfter=4.5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10, spaceAfter=3, spaceBefore=7)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=7.6, leading=9.6)
CELL = ParagraphStyle("c", fontName="Helvetica", fontSize=7.8, leading=9.6)
TBL = TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.5, 0.5, 0.5)),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.88, 0.91, 0.94)),
                  ("VALIGN", (0, 0), (-1, -1), "TOP"),
                  ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                  ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)])

CONTROL = {
    "hrcu_aml_atf_compliance_programme_v6-1.pdf": "by at least twice the cash that trade produced",
    "aml_compliance_committee_terms_of_reference.docx": "up to four new enhanced investigations",
}


def _footer(canv, doc):
    canv.saveState()
    canv.setFont("Helvetica", 7)
    canv.drawString(20 * mm, 11 * mm, "Harlow Reach Credit Union  |  AML/ATF Compliance Programme v6.1  |  Internal")
    canv.drawRightString(196 * mm, 11 * mm, "Page %d" % doc.page)
    canv.restoreState()


def _scrub(path):
    """Put the credit union's compliance office in the producer fields instead of the writing library's
    name, keeping every byte offset (reduce-house-fixes H1)."""
    data = bytearray(open(path, "rb").read())
    org = C.PRODUCER.encode()
    for comment in (b"ReportLab Generated PDF document (opensource)",
                    b"ReportLab generated PDF document -- digest (opensource)"):
        i = data.find(comment)
        while i != -1:
            data[i:i + len(comment)] = org[:len(comment)].ljust(len(comment), b" ")
            i = data.find(comment)
    for key in (b"/Producer (", b"/Creator ("):
        i = data.find(key)
        while i != -1:
            j = i + len(key)
            while j < len(data):
                if data[j:j + 1] == b"\\":
                    j += 2
                    continue
                if data[j:j + 1] == b")":
                    break
                j += 1
            old = data[i + len(key):j]
            data[i + len(key):j] = org[:len(old)].ljust(len(old), b" ")
            i = data.find(key, j)
    stamp = b"D:20260324090000+00'00'"
    for field in (b"/CreationDate (", b"/ModDate ("):
        i = data.find(field)
        while i != -1:
            j = data.find(b")", i + len(field))
            if j != -1 and j - (i + len(field)) == len(stamp):
                data[i + len(field):j] = stamp
            i = data.find(field, j if j != -1 else i + len(field))
    open(path, "wb").write(bytes(data))


def programme(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc = SimpleDocTemplate(path, pagesize=LETTER, title="AML/ATF Compliance Programme v6.1", author="",
                            subject="", creator="", leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=17 * mm, bottomMargin=18 * mm)
    P = lambda t: Paragraph(t, BODY)
    s = []
    s.append(Paragraph("Harlow Reach Credit Union<br/>Anti-Money Laundering and Anti-Terrorist Financing "
                       "Compliance Programme", H1))
    s.append(Table([[Paragraph("<b>Version</b>", CELL), Paragraph("6.1", CELL), Paragraph("<b>Approved</b>", CELL),
                     Paragraph("Board of Directors, 24 March 2026", CELL)],
                    [Paragraph("<b>Effective</b>", CELL), Paragraph("1 April 2026", CELL), Paragraph("<b>Owner</b>", CELL),
                     Paragraph("Chief Anti-Money Laundering Officer (Kristine Kirby)", CELL)],
                    [Paragraph("<b>Replaces</b>", CELL), Paragraph("Version 6.0 (April 2025)", CELL),
                     Paragraph("<b>Next review</b>", CELL), Paragraph("March 2027", CELL)]],
                   colWidths=[22 * mm, 40 * mm, 24 * mm, 88 * mm], style=TBL))
    s.append(Spacer(1, 5))
    s.append(Paragraph("1. Purpose and scope", H2))
    s.append(P("This programme sets out how Harlow Reach Credit Union meets its obligations under the Proceeds of "
               "Crime (Money Laundering) and Terrorist Financing Act and its regulations. It applies to every "
               "branch, deposit ATM, night depository and channel through which the credit union serves members, "
               "and to Regional Cash Services, which counts night deposits for the branches that have no vault "
               "staff. Version 6.1 adds section 7.3 and restates the large cash transaction window in section 6.2."))
    s.append(Paragraph("2. Governance", H2))
    s.append(P("The Board approves the programme and receives the Chief Anti-Money Laundering Officer's report each "
               "quarter. The AML Compliance Committee, under its own terms of reference, oversees the programme's "
               "operation and approves enhanced investigations. Business Services, which holds the business members' "
               "relationships, is the first line: it keeps their client due diligence current, performs the enhanced "
               "due diligence the higher-risk segments require and refers members to the Financial Intelligence Unit "
               "(the Unit). The Unit, led by the FIU Lead, Jeffrey Melendez, reviews monitoring alerts, conducts "
               "investigations and prepares reports to FINTRAC."))
    s.append(Paragraph("3. Risk assessment and segments", H2))
    s.append(P("Members are assigned to monitoring segments on the business type recorded in the member register. The "
               "cash-intensive business segment (CIB) holds the business members whose business type is a "
               "full-service restaurant; a quick-service or takeout restaurant; a cafe or bakery; a convenience "
               "store; a grocery or specialty food store; a bar or pub; a hair, nail or beauty salon; a car wash; a "
               "laundromat or dry cleaner; or a mobile food vendor. The segment is rated higher risk for the "
               "placement of criminal cash because its members take cash from the public in the ordinary course of "
               "trade."))
    s.append(Paragraph("4. Know your client", H2))
    s.append(P("The credit union identifies every member and every person holding 25 per cent or more of a business "
               "member, and records a client due diligence profile at onboarding: the nature of the business, its "
               "anticipated annual turnover and its anticipated monthly deposits, cash and total, as the member "
               "states them. The profile is reviewed annually for members rated High, every two years for Medium "
               "and every three years for Low, and whenever an event calls for it."))
    s.append(Paragraph("5. Ongoing monitoring", H2))
    s.append(P("Transactions on business accounts are monitored on the core banking system each night. Alerts are "
               "reviewed by the Unit within ten business days and are closed, escalated or referred for an "
               "enhanced investigation under section 7. For monitoring and the January review, cash is counted on "
               "the credit union's business date of each credit."))
    s.append(Paragraph("6. Reporting to FINTRAC", H2))
    s.append(P("<b>6.1 Large cash transaction reports.</b> The credit union reports the receipt of CAD 10,000 or more "
               "in cash in a single transaction, or in two or more transactions that together total CAD 10,000 or "
               "more within 24 consecutive hours, received from or on behalf of the same member."))
    s.append(P("<b>6.2 The window.</b> A window opens at a member's first cash receipt and closes 24 hours later. "
               "Cash the member pays into any of its accounts, at any branch, deposit ATM or night depository, "
               "counts toward the open window, and a receipt after the window closes opens a new one. A night "
               "deposit is received when its bag is opened and counted. Only the cash in a deposit counts; "
               "cheques deposited with it do not. Each window whose cash totals CAD 10,000 or more requires one "
               "report. A report is due within 15 calendar days after the day on which the first cash it reports "
               "was received. Windows belong to the quarter in which they open, on Pacific time, and a report to the "
               "quarter of the transaction date it reports."))
    s.append(P("<b>6.3 Suspicious transaction reports</b> are submitted as soon as practicable once the Unit has "
               "reasonable grounds to suspect that a transaction is related to money laundering or terrorist "
               "activity financing. <b>6.4 Electronic funds transfer reports</b> are made for international "
               "transfers of CAD 10,000 or more, under the same 24-hour rule."))
    s.append(Paragraph("7. Enhanced investigation", H2))
    s.append(P("<b>7.1 Triggers.</b> An enhanced investigation can follow an escalated alert, a branch referral, a "
               "request from law enforcement, or a referral from the January review in section 7.2."))
    s.append(P("<b>7.2 The January review.</b> Each January Business Services reviews every member of the "
               "cash-intensive business segment on the calendar year just closed, as the segment's enhanced due "
               "diligence."))
    s.append(P("<b>7.3 Case acceptance.</b> Business Services refers to the Unit for an enhanced investigation a "
               "member of the cash-intensive business segment where the cash paid into the member's accounts in the "
               "calendar year exceeds the cash the member's trade with its customers produced in that year by CAD "
               "100,000 or more, and by at least twice the cash that trade produced. Cash is counted on the credit "
               "union's business date of each credit. The members that meet the test are presented to the Committee "
               "at its January meeting, in descending order of the excess."))
    s.append(P("<b>7.4 Conduct.</b> An investigation reviews the member's accounts, its profile and its counterparties, "
               "and closes with no further action, a suspicious transaction report, or a recommendation to exit the "
               "relationship."))
    s.append(Paragraph("8. Records and training", H2))
    s.append(P("Records are kept for at least five years. Staff who handle cash or open accounts complete AML training "
               "on joining and each year. The programme's effectiveness is reviewed by an independent party every "
               "two years."))
    doc.build(s, onFirstPage=_footer, onLaterPages=_footer)
    _scrub(path)


def terms_of_reference(path):
    import docx
    from docx.shared import Pt
    os.makedirs(os.path.dirname(path), exist_ok=True)
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading("AML Compliance Committee: Terms of Reference", level=1)
    d.add_paragraph("Harlow Reach Credit Union. Approved by the Board of Directors on 14 November 2025.")
    d.add_heading("Purpose", level=2)
    d.add_paragraph("The Committee oversees the operation of the credit union's AML/ATF compliance programme and "
                    "approves the enhanced investigations the Financial Intelligence Unit brings to it.")
    d.add_heading("Membership", level=2)
    for t in ("Chief Anti-Money Laundering Officer, Kristine Kirby (Chair)", "FIU Lead, Jeffrey Melendez",
              "Vice-President, Member Services", "Manager, Business Services", "Director, Enterprise Risk",
              "Manager, Retail Banking"):
        d.add_paragraph(t, style="List Bullet")
    d.add_heading("Meetings", level=2)
    d.add_paragraph("The Committee meets in January, April, July and October, and whenever the Chair calls a "
                    "meeting. Three members, one of them the Chair, make a quorum. The January 2027 meeting is on "
                    "Wednesday 20 January 2027.")
    d.add_heading("Responsibilities", level=2)
    for t in ("Approve the enhanced investigations the Unit presents, including those Business Services refers "
              "under section 7.3 of the programme after the January review.",
              "Receive the Unit's quarterly report on large cash transaction, suspicious transaction and electronic "
              "funds transfer reporting.",
              "Track remediation of findings from FINTRAC examinations and the independent effectiveness review."):
        d.add_paragraph(t, style="List Bullet")
    d.add_heading("Capacity", level=2)
    d.add_paragraph("The Unit can take up to four new enhanced investigations in a quarter alongside its alert work. "
                    "Where more are approved, the Committee sets the order in which they start.")
    d.add_heading("Minutes", level=2)
    d.add_paragraph("The Unit keeps the minutes. They record each investigation approved and the reason, and are "
                    "kept with the programme's records.")
    cp = d.core_properties
    cp.author = ""
    cp.last_modified_by = ""
    cp.title = ""
    cp.created = dt.datetime(2025, 11, 14, 16, 5)
    cp.modified = dt.datetime(2025, 11, 14, 16, 5)
    cp.revision = 3
    d.save(path)
    C.freeze_zip(path, "Microsoft Office Word", stamp_iso="2025-11-14T16:05:00Z", app_version="16.0000")


def write_all(target):
    import pack
    programme(os.path.join(target, pack.P_PROG))
    terms_of_reference(os.path.join(target, pack.P_TOR))
