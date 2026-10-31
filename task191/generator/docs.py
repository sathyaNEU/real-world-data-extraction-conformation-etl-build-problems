"""The governing texts: the alert handling procedure (PDF) and the BSA/AML officer's planning thread (EML)."""
from email.message import EmailMessage
from email.utils import format_datetime
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

import common as C


def _styles():
    base = ParagraphStyle("b", fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=5)
    return {"t": ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=3),
            "s": ParagraphStyle("s", parent=base, fontSize=8.4, leading=11, textColor=colors.HexColor("#4b5560")),
            "h": ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.4, leading=14, spaceBefore=7,
                                spaceAfter=3),
            "p": base}


def procedure_pdf(path):
    st = _styles()
    blocks = [
        ("t", "AML Alert Handling Procedure"),
        ("s", "Kestrel Pay, Inc. Financial Crimes Compliance. Procedure FCC-07, version 4.2, effective 1 February 2026. "
              "Owner: BSA/AML Officer. Applies to alerts raised by the transaction monitoring system on consumer wallets, "
              "merchant accounts and cards."),
        ("h", "1. Purpose"),
        ("p", "This procedure sets out how alerts raised by the transaction monitoring system are reviewed, escalated, "
              "investigated and, where suspicion is established, reported to FinCEN in a suspicious activity report "
              "(SAR) under 31 CFR 1022.320."),
        ("h", "2. Monitoring runs"),
        ("p", "The monitoring system runs each night after the payment ledger closes for the business day, which ends at "
              "22:00 Eastern time. Each alert carries the run that raised it; a run belongs to the business day it "
              "monitors. When a run is repeated because its input was incomplete, the repeated run raises the day's "
              "alerts again, and analysts close the second copies as duplicates."),
        ("h", "3. Triage"),
        ("p", "An analyst in the triage pool reviews each alert within seven calendar days of the run, using the "
              "customer's profile, the activity behind the alert and earlier alerts and cases. The analyst closes the "
              "alert when the activity is explained, or escalates it, and the escalation opens an investigation in the "
              "financial crimes case manager. An alert on a customer who already has an open investigation is added to "
              "that investigation when it is escalated, and opens no investigation of its own."),
        ("h", "4. Investigations"),
        ("p", "Investigations are worked in the financial crimes case manager by the investigation teams. The "
              "investigator gathers account, device and counterparty information, may send the customer a request for "
              "information, and refers the case to the Financial Intelligence Unit when the activity may be suspicious. "
              "Investigations aim at a decision within 90 days of escalation; the Investigations Manager may extend an "
              "investigation where counterparties, merchants or other institutions must be traced."),
        ("h", "5. The SAR decision"),
        ("p", "The Financial Intelligence Unit decides whether the activity is suspicious. When it is, the initial report "
              "is drafted, passes the SAR quality review and is filed within 30 calendar days of that determination; "
              "the case closes when the SAR is filed. When it is not, the case closes with no SAR and the reasons "
              "recorded."),
        ("h", "6. Continuing activity and corrections"),
        ("p", "Where the customer remains active, the account is reviewed 90 days after a SAR, and a continuing activity "
              "report on the investigation, covering the activity since the previous report, is filed within 120 days "
              "of the previous report. A filed report found to contain an error is corrected by a new filing that cites "
              "the report it corrects and covers the same activity."),
        ("h", "7. Quality assurance"),
        ("p", "The Quality Assurance team samples closed alerts and closed cases each month and reports its findings to "
              "the BSA/AML Officer."),
        ("h", "8. Records"),
        ("p", "Alerts, runs, cases and filings are kept for five years from the filing or the closure."),
    ]
    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                            bottomMargin=0.8 * inch, title="AML Alert Handling Procedure FCC-07", author="Kestrel Pay",
                            creator="Kestrel Pay", producer="Kestrel Pay", invariant=1)
    story = []
    for k, v in blocks:
        story.append(Paragraph(v, st[k]))
        if k == "s":
            story.append(Spacer(1, 6))
    doc.build(story)
    C.scrub_pdf(path, "D:20260122143000-05'00'", "D:20260129101500-05'00'")


THREAD = """Miguel,

The 2027 tuning set goes to the executive risk meeting on 18 November, and the independent AML review opens on 11 January, so the paper needs to be settled before the meeting.

As we agreed in March, a scenario goes into the year's tuning when its productivity over the twelve months to 30 September falls below 3 per cent. Productivity is the share of the alerts a scenario raised in those twelve months that end in a SAR. An alert belongs to the business date of the run that raised it, and it ends in a SAR when the investigation it was escalated into, or added to, files one; the continuing activity reports and the corrections that follow a SAR do not count again. Every alert raised in the twelve months counts, those still in triage or under investigation when the figures are drawn included, by how they will end. An alert closed as a duplicate of another is not an alert of its scenario, and a scenario replaced during the year is read together with its replacement in every figure we give by scenario.

Leah's team ran the case manager export first thing this morning, and the monitoring tables run to last night's run.

Thanks,
Katherine Cobb
BSA/AML Officer
Kestrel Pay, Inc.

-----Original message-----
From: Leah Berg
Sent: Friday, October 30, 2026 4:12 PM
To: Katherine Cobb
Subject: RE: 2027 tuning set

Katherine, the export will be in the shared folder by 7am Monday, with Sunday night's run in the monitoring tables.

Leah
"""


def thread_eml(path):
    m = EmailMessage()
    m["From"] = "Katherine Cobb <kcobb@kestrelpay.com>"
    m["To"] = "Miguel Swanson <mswanson@kestrelpay.com>"
    m["Cc"] = "Leah Berg <lberg@kestrelpay.com>"
    m["Subject"] = "RE: 2027 tuning set"
    m["Date"] = format_datetime(dt.datetime(2026, 11, 2, 7, 52, 41, tzinfo=dt.timezone(dt.timedelta(hours=-5))))
    m["Message-ID"] = "<20261102125212.4471@kestrelpay.com>"
    m.set_content(THREAD)
    with open(path, "wb") as f:
        f.write(bytes(m))
    C.set_mtime(path)
