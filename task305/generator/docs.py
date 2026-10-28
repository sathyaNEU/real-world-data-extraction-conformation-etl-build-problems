"""task305 documents: the monetisation team's paper (pdf), Finance's recurring revenue policy (pdf) and the thread that
asks for the numbers (eml)."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    return body, h1, h2, small


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "%d" % d.page)
        canvas.restoreState()
    return foot


def _table(rows, widths, size=8.6):
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size + 2.4)
    head = ParagraphStyle("head", parent=cell, fontName="Helvetica-Bold")
    rows = [[Paragraph(str(v), head if r == 0 else cell) for v in row] for r, row in enumerate(rows)]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9A9A9A")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E4E8EF")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


SOURCES = {"Tracewood": "template marketplace commission and advertising",
           "Taskfold": "integration partner referrals",
           "Ledgerline": "bank-feed and payments partner referrals",
           "Formbox": "payments partner referrals",
           "Notewell": "advertising"}


def paper(path):
    body, h1, h2, small = _styles()
    s = [Paragraph("Free plan: a three-project limit, and which app takes it first", h1),
         Paragraph("Paper for the executive team, meeting of 19 November 2026. Monetisation; %s, head of monetisation. "
                   "Draft 3, 12 October 2026." % P.PEOPLE["head"], small), Spacer(1, 4)]
    s.append(Paragraph("1. Proposal", h2))
    s.append(Paragraph("From 1 January 2027 the free plan of one of our apps keeps up to three active projects an account. "
                       "A free account over the limit can still open, share and export every project, but can edit only "
                       "three; to edit another it archives one, or it moves to Plus, which has no project limit. An archived "
                       "project can be restored at any time within the limit. The other four apps keep the free plan as it "
                       "is through 2027, and the executive looks at them again with a year of the first app's results.", body))
    s.append(Paragraph("2. The decision", h2))
    s.append(Paragraph("The executive takes the limit first in the app where it adds the most to 2027 revenue, and the "
                       "paper states that addition.", body))
    s.append(Paragraph("3. What the paper estimates", h2))
    s.append(Paragraph("For each app, the revenue the limit adds in calendar 2027: the app's 2027 revenue with the limit "
                       "less its 2027 revenue without it. A month on Plus counts at the app's Plus monthly price before VAT, "
                       "and a month in which a free account is used counts at the app's free-plan revenue per active free "
                       "account, both from the table in section 4. The limit reaches every free account with more than "
                       "three active projects on 1 January 2027 and every free account that reaches a fourth active "
                       "project during the year. Free accounts and paying customers act as our records show them acting.",
                       body))
    s.append(Paragraph("4. Prices and free-plan revenue", h2))
    rows = [["App", "Plus, a month (GBP, before VAT)", "Free-plan revenue per active free account, a month (GBP)",
             "Where free-plan revenue comes from"]]
    for i, a in enumerate(P.APPS):
        rows.append([a, "%.2f" % P.PLUS[i], "%.2f" % P.FREE_REV[i], SOURCES[a]])
    s.append(_table(rows, [26, 34, 46, 64]))
    s.append(Spacer(1, 4))
    s.append(Paragraph("Plus prices are the price list in force from 1 April 2026. Free-plan revenue is Finance's 2026 run "
                       "rate over the average number of active free accounts; an active free account is one used in the "
                       "month. Notewell was called Leafnote until April 2025.", small))
    s.append(Paragraph("5. Records", h2))
    s.append(Paragraph("Product Analytics' research panel (one account in twenty-five, drawn at sign-up) and the monthly "
                       "count of free accounts by active projects, both to 30 September 2026; the price list; Billing's "
                       "subscription records and Finance's recurring revenue policy for the board pack.", body))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="Free plan: a three-project limit", author=P.PEOPLE["head"],
                            creator=P.ORG, subject="Monetisation", invariant=1)
    doc.build(s, onFirstPage=_footer("Brindlecote Software, Monetisation. Internal: executive team."),
              onLaterPages=_footer("Brindlecote Software, Monetisation. Internal: executive team."))


def policy(path):
    body, h1, h2, small = _styles()
    s = [Paragraph("FIN-07 Recurring revenue", h1),
         Paragraph("Finance policy, issue 4, April 2026. Owner: financial controller. Supersedes issue 3 (March 2024).",
                   small), Spacer(1, 4),
         Paragraph("1. Scope", h2),
         Paragraph("Recurring revenue is how Finance reports the subscription business month by month and in the board "
                   "pack. It is a measure of what customers are signed up to pay, not of cash or of revenue under our "
                   "accounting policies.", body),
         Paragraph("2. The value of a subscription", h2),
         Paragraph("A subscription counts at its monthly value: a monthly price as it is, an annual price over twelve, a "
                   "seat price times the seats, before VAT, and after any discount that runs for twelve months or more. A "
                   "discount that runs for less than twelve months is left out.", body),
         Paragraph("3. Currency", h2),
         Paragraph("Subscriptions in euros and US dollars are translated into pounds at the plan rates for the plan year "
                   "in which the reporting period ends, so that a bridge moves only on what customers do. The plan year "
                   "runs from 1 April to 31 March.", body),
         Paragraph("4. Live subscriptions", h2),
         Paragraph("A subscription counts while it is live: from its start until it ends. A subscription whose payment has "
                   "failed stays live while the billing platform retries the payment.", body),
         Paragraph("5. The bridge", h2),
         Paragraph("The bridge for a period compares each customer's recurring revenue at the start and at the end of the "
                   "period, app by app: new where the customer had none at the start, churned where it has none at the "
                   "end, and expansion or contraction where it has some at both and the end is higher or lower. A "
                   "customer is the person or organisation that pays. Dates are UK dates; a period ends at midnight at "
                   "the end of its last day.", body)]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="FIN-07 Recurring revenue", author="Financial controller",
                            creator=P.ORG, subject="Finance policy", invariant=1)
    doc.build(s, onFirstPage=_footer("Brindlecote Software, Finance. Policy FIN-07."),
              onLaterPages=_footer("Brindlecote Software, Finance. Policy FIN-07."))


def thread(path):
    head, cfo, an = P.PEOPLE["head"], P.PEOPLE["cfo"], P.PEOPLE["analyst"]

    def addr(name):
        return "%s <%s@%s>" % (name, name.lower().replace(" ", "."), P.DOMAIN)
    text = "\r\n".join([
        "Message-ID: <20261012091422.4F1C7A@%s>" % P.DOMAIN,
        "Date: Mon, 12 Oct 2026 09:14:22 +0100",
        "From: %s" % addr(head),
        "To: %s" % addr(an),
        "Cc: %s" % addr(cfo),
        "Subject: Re: Free plan limit, which app first",
        "In-Reply-To: <20261009174803.11AB02@%s>" % P.DOMAIN,
        "MIME-Version: 1.0",
        "Content-Type: text/plain; charset=utf-8",
        "Content-Transfer-Encoding: 8bit",
        "",
        "Frederick,",
        "",
        "Leonard wants the paper's numbers before the 19 November meeting: which app should take the three-project",
        "limit first, and what it adds to that app's 2027 revenue. For the board pack he also wants each app's",
        "recurring revenue bridge for the year to 30 September, on FIN-07.",
        "",
        "Everything Product Analytics, Billing and Finance pulled for this is in the shared folder. Draft 3 of the",
        "paper is there too; the numbers in it are yours to fill.",
        "",
        "Thanks,",
        "Lynne",
        "",
        "On Fri, 9 Oct 2026 at 17:48, %s wrote:" % cfo,
        "> Lynne, before the 19th I'd like the limit sized app by app, so we put it where it earns most next",
        "> year, and the year's bridges for the board pack. L.",
        ""])
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
