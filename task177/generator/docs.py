"""task177 documents: Billing Operations' note on the move to the subscriptions platform and the retention model's
validation summary (PDFs), the January 2027 offer plan (Word) and the field descriptions (Excel). Their text is held here
as data so checks.py can quote it and verify.py can read it back."""
from __future__ import annotations

import datetime as dt
import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                        # noqa: E402
from reportlab.lib.pagesizes import A4                                                  # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                         # noqa: E402
from reportlab.lib.units import mm                                                      # noqa: E402
from reportlab.pdfbase import pdfmetrics                                                # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                            # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as C          # noqa: E402
import postprocess as PP    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d1f23")
GREY = colors.HexColor("#5f6670")
ACCENT = colors.HexColor("#7a2e1f")
RULE = colors.HexColor("#cfd4da")

# ---------------------------------------------------------------------------------------- the billing move note
NOTE_DATE = dt.date(2026, 10, 15)
NOTE_TITLE = "Monthly digital billing on the subscriptions platform"
NOTE_SUB = ("Billing Operations, Daily Lantern Media. Version 1.3, 15 October 2026. Owner: Bernard Peacock, Billing "
            "Operations Manager.")
NOTE = [
    ("1. The move", [
        "1.1 The subscriptions platform bills every monthly digital subscription from the 1 October 2026 bill run. "
        "The legacy billing system billed each subscription on its own billing day; its last scheduled bills were "
        "raised on 30 September 2026.",
        "1.2 From 1 November 2026 every monthly digital subscription is billed on the 1st of the month. A subscription "
        "that starts on the platform has its first bill raised on its start day, for the days to the end of that month. "
        "The platform's first bill for a migrated subscription, raised in the 1 October run, covers the days from the "
        "end of its last legacy billing period to 31 October.",
        "1.3 Plans and prices do not change with the move. Digital news subscriptions are zero-rated for VAT on both "
        "systems.",
    ]),
    ("2. Identifiers", [
        "2.1 Every legacy subscription reference has a platform subscription id and a platform account id. The "
        "crosswalk issued with this note lists them. Customer numbers do not change.",
    ]),
    ("3. Exports", [
        "3.1 Legacy invoice exports give dates as day/month/year and amounts in pence.",
        "3.2 Platform exports give times in UTC and amounts in pounds. Billing Operations reports each bill in the "
        "month of the UK date it was raised.",
    ]),
    ("4. 1 October run (added 15 October)", [
        "4.1 The legacy system's 1 October run was not switched off for seven migration batches until 06:00, so "
        "subscriptions billed on the 1st in those batches were billed by both systems for October.",
        "4.2 The platform credited each affected account on 14 October. Customers were told by email the same day.",
    ]),
]
NOTE_REVISIONS = ("Version 1.3 (15 October 2026): section 4. Version 1.2 (22 September 2026): batch dates confirmed. "
                  "Version 1.1 (1 September 2026): export formats.")

# ----------------------------------------------------------------------------------- the model validation summary
VAL_DATE = dt.date(2026, 12, 9)
VAL_TITLE = "Retention model 3.2: validation summary"
VAL_SUB = "Audience Data Science, Daily Lantern Media. 9 December 2026."
VAL_BODY = [
    "Model 3.2 scores every monthly digital subscription each night for the chance that it is cancelled within 30 "
    "days. It replaced model 3.1 on 2 December 2026.",
    "Validation: subscriptions scored on 1 August 2026 and followed for 30 days. AUC 0.781 (model 3.1: 0.764).",
    "The at-risk list for retention offers takes reader-paid monthly digital subscriptions scored 0.25 or above with no "
    "cancellation pending.",
]
VAL_BANDS = (("A", "0.55 and above", "61.4%", "58.9%"), ("B", "0.40 to 0.549", "46.8%", "47.5%"),
             ("C", "0.25 to 0.399", "31.9%", "33.2%"))
VAL_FEATURES = ("articles read in the last 28 days", "months subscribed", "support contacts in the last 90 days",
                "newsletters taken", "plan", "main device", "payment failures in the last year")

# ------------------------------------------------------------------------------------------- the 2027 offer plan
PLAN_DATE = dt.date(2027, 1, 18)
PLAN_TITLE = "January 2027 retention offer"
PLAN_SUB = "Subscriber Retention, Audience Revenue. 18 January 2027. Natalie Taylor."
PLAN = [
    ("The offer", [
        "Half price on the next two monthly bills. A subscriber takes it from the offer email or the in-app message "
        "within 30 days of the send; it applies to the subscription's own plan price.",
    ]),
    ("Who gets it", [
        "The retention model's at-risk list of reader-paid monthly digital subscriptions, cut on 25 January 2027: "
        "48,000 subscriptions. Every subscription on the list is sent the offer; nobody is held back this year.",
    ]),
    ("When", [
        "Email and in-app message on Tuesday 26 January 2027 from 09:30.",
    ]),
    ("Last January", [
        "The same offer went to a random half of the 31 January 2026 at-risk list that day; the other half was not "
        "sent it.",
    ]),
    ("What the executive team needs before the send", [
        "The share of this list still subscribed on 31 March 2027 because of the offer, that is subscriptions that "
        "would have gone without it, set against what the offer gives away in discounts.",
    ]),
]

FIELDS = (
    (C.F_ASSIGN, "list_id", "text", "Campaign tool list"),
    (C.F_ASSIGN, "subscription_ref", "text", "Legacy billing subscription reference"),
    (C.F_ASSIGN, "customer_no", "text", "CRM customer number"),
    (C.F_ASSIGN, "arm", "text", "offer: sent the January offer on 31 January 2026; holdout: not sent"),
    (C.F_ASSIGN, "risk_score", "number", "Retention model score when the list was cut"),
    (C.F_ASSIGN, "risk_band", "text", "Band of the score (A, B, C)"),
    (C.F_ASSIGN, "offer_sent_at", "datetime", "When the campaign tool queued the send, UK time (dd/mm/yyyy hh:mm)"),
    (C.F_PROFILE, "customer_no", "text", "CRM customer number"),
    (C.F_PROFILE, "subscription_ref", "text", "Legacy billing subscription reference"),
    (C.F_PROFILE, "plan", "text", "Plan on 31 January 2026"),
    (C.F_PROFILE, "started_on", "date", "Date the subscription started"),
    (C.F_PROFILE, "region", "text", "Region of the billing address"),
    (C.F_PROFILE, "most_used_on", "text", "Device most used in the last 28 days"),
    (C.F_PROFILE, "articles_read_28d", "integer", "Articles read in the last 28 days"),
    (C.F_PROFILE, "newsletters", "integer", "Newsletters taken"),
    (C.F_PROFILE, "support_contacts_90d", "integer", "Contacts with customer services in the last 90 days"),
    (C.F_PROFILE, "payment_method", "text", "Payment method"),
    (C.F_PROFILE, "app_user_id", "text", "App user id, for subscribers who use the app"),
    (C.F_LIST, "list_id", "text", "Campaign tool list"),
    (C.F_LIST, "subscription_id", "text", "Platform subscription id"),
    (C.F_LIST, "account_id", "text", "Platform account id"),
    (C.F_LIST, "customer_no", "text", "CRM customer number"),
    (C.F_LIST, "plan", "text", "Plan on 25 January 2027"),
    (C.F_LIST, "started_on", "date", "Date the subscription started"),
    (C.F_LIST, "region", "text", "Region of the billing address"),
    (C.F_LIST, "most_used_on", "text", "Device most used in the last 28 days"),
    (C.F_LIST, "articles_read_28d", "integer", "Articles read in the last 28 days"),
    (C.F_LIST, "newsletters", "integer", "Newsletters taken"),
    (C.F_LIST, "support_contacts_90d", "integer", "Contacts with customer services in the last 90 days"),
    (C.F_LIST, "payment_method", "text", "Payment method"),
    (C.F_LIST, "risk_score", "number", "Retention model score when the list was cut"),
    (C.F_LIST, "risk_band", "text", "Band of the score (A, B, C)"),
    (C.F_LBS, "invoice_no", "text", "Legacy invoice number"),
    (C.F_LBS, "subscription_ref", "text", "Legacy billing subscription reference"),
    (C.F_LBS, "invoice_date", "date", "Bill date (dd/mm/yyyy); the legacy system billed each subscription monthly in "
                                      "advance on its billing day"),
    (C.F_LBS, "line_type", "text", "SUB charge for the subscription, DISC discount, CRED credit"),
    (C.F_LBS, "item_code", "text", "Plan, discount or credit code"),
    (C.F_LBS, "applied_ref", "text", "Reference of the request that applied the discount or credit"),
    (C.F_LBS, "amount_pence", "integer", "Pence; discounts and credits are negative"),
    (C.F_LBS, "vat_code", "text", "Z zero-rated"),
    (C.F_LBS, "status", "text", "Payment status"),
    (C.F_SPINV, "invoice_id", "text", "Platform invoice or credit note number"),
    (C.F_SPINV, "account_id", "text", "Platform account id"),
    (C.F_SPINV, "subscription_id", "text", "Platform subscription id"),
    (C.F_SPINV, "doc_type", "text", "invoice or credit_note"),
    (C.F_SPINV, "issued_at", "datetime", "When the document was raised, UTC"),
    (C.F_SPINV, "period_start", "date", "Start of the billing period"),
    (C.F_SPINV, "period_end", "date", "End of the billing period"),
    (C.F_SPINV, "amount_gbp", "number", "Invoice total in pounds; credit notes are negative"),
    (C.F_SPINV, "tax_rate", "number", "VAT rate, per cent"),
    (C.F_SPINV, "covers", "text", "For a credit note, the invoice numbers it reverses"),
    (C.F_SPINV, "status", "text", "Payment status"),
    (C.F_SPINV, "lines", "json", "The document's lines: line, subscription_id, item, text, from, to, amount"),
    (C.F_XWALK, "legacy_subscription_ref", "text", "Legacy billing subscription reference"),
    (C.F_XWALK, "platform_subscription_id", "text", "Platform subscription id"),
    (C.F_XWALK, "platform_account_id", "text", "Platform account id"),
    (C.F_XWALK, "migrated_on", "date", "Date the subscription moved"),
    (C.F_XWALK, "batch", "text", "Migration batch"),
    (C.F_EVENTS, "subscription_key", "text", "Legacy subscription reference, or platform subscription id from the move"),
    (C.F_EVENTS, "system", "text", "legacy or platform"),
    (C.F_EVENTS, "event", "text", "cancel_requested, access_ended, restarted"),
    (C.F_EVENTS, "event_date", "date", "UK date of the event. access_ended is the last day of access: a subscription "
                                       "is live until the end of its last paid period"),
    (C.F_EVENTS, "reason", "text", "Reason given when cancelling"),
    (C.F_OFFERS, "acceptance_ref", "text", "Offers engine acceptance reference"),
    (C.F_OFFERS, "offer", "text", "Offer"),
    (C.F_OFFERS, "customer_key", "text", "CRM customer number, or the app user id for acceptances in the app"),
    (C.F_OFFERS, "channel", "text", "email, web or app"),
    (C.F_OFFERS, "accepted_at", "datetime", "UTC"),
    (C.F_OFFERS, "status", "text", "Acceptance status"),
    (C.F_EMAIL, "message_id", "text", "Email platform message id"),
    (C.F_EMAIL, "customer_no", "text", "CRM customer number"),
    (C.F_EMAIL, "campaign", "text", "Campaign"),
    (C.F_EMAIL, "event", "text", "delivered, bounced, opened, clicked"),
    (C.F_EMAIL, "event_at", "datetime", "UTC"),
    (C.F_SURVEY, "customer_no", "text", "CRM customer number"),
    (C.F_SURVEY, "responded_on", "date", "Date of the response"),
    (C.F_SURVEY, "satisfaction", "integer", "How satisfied, 0 to 10"),
    (C.F_SURVEY, "likely_to_cancel_3m", "text", "How likely to cancel in the next three months"),
    (C.F_SURVEY, "main_reason", "text", "Main reason given"),
)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pdf_stamp(d, hh=10, mi=0):
    bst = C.BST[d.year][0].date() <= d < C.BST[d.year][1].date()
    return ("D:%04d%02d%02d%02d%02d00%+03d'00'" % (d.year, d.month, d.day, hh, mi, 1 if bst else 0)).encode()


def _styles():
    return dict(
        org=ParagraphStyle("org", fontName="Carlito-Bold", fontSize=9.5, leading=12, textColor=ACCENT, spaceAfter=2),
        h1=ParagraphStyle("h1", fontName="LibSans-Bold", fontSize=15, leading=19, textColor=INK, spaceAfter=4),
        sub=ParagraphStyle("sub", fontName="Carlito", fontSize=9.2, leading=12, textColor=GREY, spaceAfter=12),
        h2=ParagraphStyle("h2", fontName="LibSans-Bold", fontSize=11, leading=14, textColor=ACCENT, spaceBefore=8,
                          spaceAfter=3),
        body=ParagraphStyle("body", fontName="Carlito", fontSize=10.8, leading=14.4, textColor=INK, spaceAfter=5),
        cell=ParagraphStyle("cell", fontName="Carlito", fontSize=9.6, leading=12, textColor=INK),
        small=ParagraphStyle("small", fontName="Carlito", fontSize=8.6, leading=11, textColor=GREY, spaceBefore=10))


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Carlito", 7.8)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 11 * mm, text)
        canvas.drawRightString(A4[0] - 20 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm,
                             bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")


def _table(rows, widths, st):
    data = [[Paragraph(esc(str(c)), st["cell"]) for c in r] for r in rows]
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                           ("FONTNAME", (0, 0), (-1, 0), "Carlito-Bold")]))
    return t


def note_text():
    out = [NOTE_TITLE, NOTE_SUB]
    for h, paras in NOTE:
        out.append(h)
        out.extend(paras)
    out.append(NOTE_REVISIONS)
    return out


def write_note(out):
    path = os.path.join(out, C.F_NOTE)
    st = _styles()
    doc = _doc(path, NOTE_TITLE, "Billing Operations")
    story = [Paragraph(esc(C.ORG + " | Billing Operations"), st["org"]), Paragraph(esc(NOTE_TITLE), st["h1"]),
             Paragraph(esc(NOTE_SUB), st["sub"])]
    for h, paras in NOTE:
        story.append(Paragraph(esc(h), st["h2"]))
        for p in paras:
            story.append(Paragraph(esc(p), st["body"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(esc(NOTE_REVISIONS), st["small"]))
    foot = "Daily Lantern Media Ltd. Billing Operations. Internal."
    doc.build(story, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    PP.normalize_pdf(path, pdf_stamp(NOTE_DATE, 16, 42), pdf_stamp(NOTE_DATE, 16, 42))


def write_validation(out):
    path = os.path.join(out, C.F_VALID)
    st = _styles()
    doc = _doc(path, VAL_TITLE, "Audience Data Science")
    story = [Paragraph(esc(C.ORG + " | Audience Data Science"), st["org"]), Paragraph(esc(VAL_TITLE), st["h1"]),
             Paragraph(esc(VAL_SUB), st["sub"])]
    for p in VAL_BODY:
        story.append(Paragraph(esc(p), st["body"]))
    story.append(Paragraph(esc("Calibration by band (1 August 2026 scores)"), st["h2"]))
    story.append(_table([("Band", "Score", "Mean score", "Cancelled within 30 days")] + [list(r) for r in VAL_BANDS],
                        [18 * mm, 40 * mm, 30 * mm, 50 * mm], st))
    story.append(Paragraph(esc("Inputs"), st["h2"]))
    story.append(Paragraph(esc(", ".join(VAL_FEATURES).capitalize() + "."), st["body"]))
    foot = "Daily Lantern Media Ltd. Audience Data Science. Model 3.2."
    doc.build(story, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    PP.normalize_pdf(path, pdf_stamp(VAL_DATE, 14, 5), pdf_stamp(VAL_DATE, 14, 5))


def plan_text():
    out = [PLAN_TITLE, PLAN_SUB]
    for h, paras in PLAN:
        out.append(h)
        out.extend(paras)
    return out


def write_plan(out):
    from docx import Document
    from docx.shared import Pt, RGBColor
    path = os.path.join(out, C.F_PLAN)
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    h = doc.add_paragraph()
    r = h.add_run(PLAN_TITLE)
    r.bold = True
    r.font.size = Pt(16)
    r.font.color.rgb = RGBColor(0x7A, 0x2E, 0x1F)
    s = doc.add_paragraph(PLAN_SUB)
    s.runs[0].font.size = Pt(9.5)
    s.runs[0].font.color.rgb = RGBColor(0x5F, 0x66, 0x70)
    for head, paras in PLAN:
        p = doc.add_paragraph()
        rr = p.add_run(head)
        rr.bold = True
        rr.font.size = Pt(12)
        for t in paras:
            doc.add_paragraph(t)
    doc.save(path)
    PP.normalize_docx(path, "Natalie Taylor", "Natalie Taylor", "2027-01-14T10:12:00Z", "2027-01-18T15:47:00Z",
                      revision=6, total_time=94, seed="plan2027", title=PLAN_TITLE, company=C.ORG)


def write_dictionary(out):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    path = os.path.join(out, C.F_DICT)
    wb = Workbook()
    ws = wb.active
    ws.title = "fields"
    head = ("file", "field", "type", "description")
    fill = PatternFill("solid", fgColor="E7E2DC")
    for j, hname in enumerate(head):
        c = ws.cell(row=1, column=j + 1, value=hname)
        c.font = Font(bold=True)
        c.fill = fill
    for i, row in enumerate(FIELDS):
        for j, v in enumerate(row):
            c = ws.cell(row=i + 2, column=j + 1, value=v)
            if j == 3:
                c.alignment = Alignment(wrap_text=True, vertical="top")
    for col, w in zip("ABCD", (38, 26, 10, 100)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    wb.save(path)
    PP.normalize_ooxml(path, "Audience Data", "Natalie Taylor", "2026-02-03T11:20:00Z", "2027-01-25T17:58:00Z",
                       excel=True, company=C.ORG)
