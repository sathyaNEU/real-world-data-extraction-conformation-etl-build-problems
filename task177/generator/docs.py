"""The data room's documents: the MFI's operating policy, the bank's term sheet and guardrails policy, the MFI's field
update after the cyclone (PDF, reportlab, fixed metadata so builds are byte-identical), and the MFI's monthly
portfolio report (xlsx, openpyxl, fixed document properties)."""
from __future__ import annotations

import datetime as dt
import io
import zipfile

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab import rl_config

import params as P

rl_config.invariant = 1

BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=5)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=4)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=12.5, leading=15, spaceAfter=3)
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8, leading=10, textColor=colors.HexColor("#444444"))


def _pdf(path, story, title, author, created):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, producer=author,
                            subject="", keywords="")
    doc.build(story)
    data = buf.getvalue()
    stamp = created.strftime("D:%Y%m%d%H%M%S+05'30'").encode()
    import re
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + stamp + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + stamp + b")", data)
    # the writer's comment lines, blanked after their % marker at equal length so no offset moves
    for sig in (b"ReportLab Generated PDF document (opensource)",
                b"ReportLab generated PDF document -- digest (opensource)"):
        data = data.replace(sig, b" " * len(sig))
    assert b"reportlab" not in data.lower()
    with open(path, "wb") as f:
        f.write(data)


def _p(t, s=BODY):
    return Paragraph(t, s)


def operating_policy(path):
    s = [_p("Prachi Valley Microfinance Pvt Ltd", SMALL), _p("Joint Liability Group Lending: Operating Policy", TITLE),
         _p("Version 6.1, approved by the Board on 24 April 2025, effective 1 May 2025 (supersedes version 6)", SMALL),
         Spacer(1, 6)]
    secs = [
        ("1. Groups and centres",
         "Loans are made to women in joint liability groups (JLGs) of five members. Members of a group live in the "
         "same village, are not closely related to one another and agree to be jointly responsible for each "
         "other's repayment. Three to five groups meeting at the same place form a centre. A centre meets every "
         "fourteen days on a fixed weekday at a fixed place; where the meeting day is a public holiday or Sunday "
         "the meeting is held on the next working day. The field officer attends every meeting."),
        ("2. Loans",
         "The JLG loan (product JLG-24F) is repaid in 52 equal fortnightly instalments of principal and interest at "
         "the centre meeting, the first falling due at the meeting fourteen days after disbursement. A member who "
         "repays a loan in full may be offered a further loan at the next meeting. A group that has stopped "
         "repaying is not given further loans; a new group may be formed at the centre."),
        ("3. Group responsibility",
         "Each member pays her own instalment at the meeting. Where a member cannot pay, the other members of her "
         "group may pay it on her behalf at the meeting, as the group's joint responsibility provides. The company "
         "does not require a group to pay for a member and does not charge one member's dues to another member's "
         "loan account."),
        ("4. Recording collections",
         "The field officer records each instalment collected against the member's own loan account, with the "
         "member number of the person who paid it. Transaction types in Kshetra: OWN, paid by the member herself; "
         "GRP_SUPP, paid at the meeting by another member of the group on her behalf; NOT_PAID, not paid at the "
         "meeting. Until 31 March 2025 CollectPro recorded the same as SELF, GS and NIL. An instalment recorded "
         "OWN, GRP_SUPP, SELF or GS is paid in full on its due date."),
        ("5. Migration",
         "All members, groups and loans held in CollectPro on 31 March 2025 were migrated to Kshetra on 1 April "
         "2025 under new identifiers; the migration map lists each CollectPro identifier and its Kshetra "
         "identifier. CollectPro numbered groups within a centre (1 to 5); Kshetra gives each group its own "
         "identifier."),
        ("6. Days past due and portfolio quality",
         "An instalment not paid in full on its due date is overdue from the following day. A loan's days past due "
         "on any date is the number of days from the due date of its oldest instalment not paid in full to that "
         "date; a loan with no such instalment is current. Portfolio at risk (PAR 30, PAR 90) is the principal "
         "outstanding of loans 30 or more (90 or more) days past due, as a share of the gross loan portfolio, at "
         "the month end. Collection efficiency for a month is the instalments collected at the meetings of that "
         "month as a share of the instalments falling due in it."),
        ("7. Write-off",
         "A loan 360 or more days past due is written off at the month end; recovery continues."),
    ]
    for h, b in secs:
        s += [_p(h, HEAD), _p(b)]
    _pdf(path, s, "JLG Operating Policy v6.1", "Prachi Valley Microfinance Pvt Ltd", dt.datetime(2025, 4, 28, 11, 0))


def term_sheet(path, n_loans, principal_lakh):
    s = [_p("Tamralipta Bank Ltd, Inclusive Lending and Direct Assignment", SMALL),
         _p("Indicative term sheet: direct assignment of microfinance loans, Pool PVM/2026-12", TITLE),
         _p("Issued 8 January 2027. Indicative only and subject to due diligence and the Bank's approvals.", SMALL),
         Spacer(1, 6)]
    rows = [
        ["1. Assignor and servicer", "Prachi Valley Microfinance Pvt Ltd (NBFC-MFI)"],
        ["2. Assignee", "Tamralipta Bank Ltd"],
        ["3. Pool", "The loans listed in the pool tape dated 31 December 2026 (%s loans, principal outstanding "
                    "INR %.2f lakh at the cut-off)" % (f"{n_loans:,}", principal_lakh)],
        ["4. Cut-off date", "31 December 2026"],
        ["5. Eligibility", "JLG-24F loans current at the cut-off (no instalment due on or before the cut-off left "
                           "unpaid), disbursed on or before 1 October 2026 (minimum holding period of three "
                           "months), from the Assignor's fourteen branches in Odisha"],
        ["6. Minimum retention", "10 per cent of each loan retained by the Assignor; the Assignee acquires 90 per "
                                 "cent of the principal outstanding"],
        ["7. Consideration", "At par on the Assignee's share of principal outstanding at the cut-off"],
        ["8. Servicing", "By the Assignor at its centre meetings; collections remitted monthly"],
        ["9. Priority sector", "Microfinance loans to women borrowers; weaker sections"],
        ["10. Settlement", "On or before 30 March 2027, subject to the Assignee's credit approval"],
        ["11. Data room", "Pool tape; CollectPro collection exports (July 2023 to March 2025); Kshetra collections "
                          "(April 2025 to December 2026); the migration map; member KYC for the pool; centre "
                          "master; the Assignor's monthly portfolio report; credit bureau portfolio review of the "
                          "pool's borrowers at the cut-off"],
    ]
    t = Table([[_p(a), _p(b)] for a, b in rows], colWidths=[45 * mm, 120 * mm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.25,
                                                                   colors.HexColor("#bbbbbb"))]))
    s.append(t)
    _pdf(path, s, "Term sheet PVM/2026-12", "Tamralipta Bank Ltd", dt.datetime(2027, 1, 8, 16, 20))


def guardrails(path):
    s = [_p("Tamralipta Bank Ltd, Credit Policy Note CPN-MF-07", SMALL),
         _p("Microfinance guardrails for direct assignment and co-lending", TITLE),
         _p("Approved by the Credit Policy Committee on 2 May 2025; applies to pools assessed after that date", SMALL),
         Spacer(1, 6)]
    secs = [
        ("1. Purpose",
         "The Bank buys and co-lends microfinance loans only where the borrowers' total microfinance indebtedness "
         "is within the industry's guardrails. This note sets out how a borrower is assessed for a pool."),
        ("2. Breach",
         "A borrower is in breach of the guardrails if, on the credit bureau report at the pool's cut-off, she has "
         "active microfinance loans from four or more lending institutions, counting the institution whose loan is "
         "offered, or more than INR 2,00,000 outstanding in total across her active microfinance loans."),
        ("3. Counting",
         "Microfinance loans are the bureau's JLG and MFI-IND account types; closed accounts and other credit (gold "
         "loans, Kisan credit cards, consumer loans) are not counted. A lending institution is counted once. Loans "
         "reported under a member code that the bureau's member directory lists with an institution as its parent, "
         "and loans reported under the member code of an institution it succeeded, count as that institution's. "
         "A loan is counted once, at its latest report."),
        ("4. Reporting",
         "The assessment is reported to the Credit Committee with each pool, by branch of the assignor."),
    ]
    for h, b in secs:
        s += [_p(h, HEAD), _p(b)]
    _pdf(path, s, "CPN-MF-07 Microfinance guardrails", "Tamralipta Bank Ltd", dt.datetime(2025, 5, 2, 15, 5))


def field_update(path):
    s = [_p("Prachi Valley Microfinance Pvt Ltd, Operations", SMALL),
         _p("Field update after the October cyclone", TITLE),
         _p("Circulated to lenders on 18 November 2026", SMALL), Spacer(1, 6)]
    paras = [
        "The severe cyclonic storm that crossed the Odisha coast on the night of 16 October 2026 damaged houses, "
        "boats, nets and standing paddy across our branches in Kendrapara and Jagatsinghpur districts, and to a "
        "lesser extent in Bhadrak and Balasore. Our branches in Jajpur and Cuttack were not affected.",
        "All staff are safe. Centre meetings have continued on their schedule; where a meeting place was flooded "
        "the field officer held the meeting at the nearest dry place on the same day. Field officers had visited "
        "every coastal centre by 15 November.",
        "We have not announced a moratorium and no lender has asked for one. We will share our monthly portfolio "
        "report with lenders as usual.",
    ]
    for t in paras:
        s.append(_p(t))
    _pdf(path, s, "Field update, October cyclone", "Prachi Valley Microfinance Pvt Ltd", dt.datetime(2026, 11, 18, 10, 30))


APP_XML = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           b'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           b'<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
           b'<Company>%s</Company><AppVersion>16.0300</AppVersion></Properties>')


def fixed_xlsx(path, when=(2027, 1, 6, 9, 0, 0), company=b"Prachi Valley Microfinance Pvt Ltd", author=None):
    """openpyxl writes the current time into docProps/core.xml and itself into docProps/app.xml; pin the times to the
    file's own date, name the issuer, and fix the zip entries' dates."""
    stamp = ("%04d-%02d-%02dT%02d:%02d:%02dZ" % when).encode()
    with zipfile.ZipFile(path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    import re
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info, data in items:
            if info.filename == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + stamp + rb"\g<2>", data)
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + stamp + rb"\g<2>", data)
                if author:
                    data = re.sub(rb"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", rb"\g<1>" + author + rb"\g<2>", data)
            if info.filename == "docProps/app.xml":
                data = APP_XML % company
            zi = zipfile.ZipInfo(info.filename, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)
