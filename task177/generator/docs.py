"""task177 documents: the assistant-first rollout plan, the vendor's acceptance test summary and its usage-tier order
form (PDFs). Their text is held here as data so checks.py can quote it and verify.py can read it back."""
from __future__ import annotations

import datetime as dt
import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                        # noqa: E402
from reportlab.lib.pagesizes import letter                                              # noqa: E402
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
from reportlab.pdfbase.pdfmetrics import registerFontFamily   # noqa: E402
registerFontFamily("Carlito", normal="Carlito", bold="Carlito-Bold", italic="Carlito", boldItalic="Carlito-Bold")
INK = colors.HexColor("#1f2328")
GREY = colors.HexColor("#5d646d")
ACCENT = colors.HexColor("#1c4e80")
RULE = colors.HexColor("#c9d1d9")

PLAN_DATE = dt.date(2026, 12, 16)
PLAN_TITLE = "Ask Prairie Works 4.0: assistant-first rollout plan"
PLAN_SUB = ("Digital Channels, Prairie Works Manitoba. Version 1.4, 16 December 2026. Owner: Sabrina Ward, product "
            "owner, Ask Prairie Works. Approved: Loretta Rodgers, Head of Contact Services.")
PLAN = [
    ("1. Release 4.0", [
        "1.1 Release 4.0 of Ask Prairie Works, the vendor's rebuilt assistant, replaces release 3.4 in the app, on the "
        "web and on the voice service at 06:00 on Monday 4 January 2027.",
        "1.2 Release 4.0 passed the vendor's acceptance test on 30 November 2026. The summary is filed with this plan.",
        "1.3 Rollout planning takes release 4.0 to resolve conversations in the app, on the web and on the voice "
        "service at the rate it resolved the acceptance test's conversations.",
    ]),
    ("2. Assistant-first weeks", [
        "2.1 From 06:00 on Monday 4 January to the end of Sunday 28 February 2027, Ask Prairie Works answers every call "
        "that reaches the Claimant Services queue on the claimant line (204-945-0100). A call it cannot resolve ends "
        "with an adviser callback booked.",
        "2.2 The general enquiries option on the claimant line and the employer line (204-945-0200) keep their advisers "
        "throughout.",
        "2.3 Jobseekers can still open a conversation in the app or on the web at any time.",
    ]),
    ("3. From 1 March 2027", [
        "3.1 From Monday 1 March the Claimant Services queue returns to advisers.",
        "3.2 The overflow transfer to the assistant's voice service stays on, with the thresholds set for 2026.",
        "3.3 Rollout planning takes the calls the Claimant Services queue keeps, those an adviser answers and those "
        "abandoned in the queue, to resolve as those calls did in 2026.",
    ]),
    ("4. Check-ins", [
        "4.1 A jobseeker on a claim checks in every 14 days, counted from the day the claim opened, by phone or through "
        "Ask Prairie Works, until the claim closes. The rollout does not change the check-in. Rollout planning takes "
        "each check-in on its due date.",
    ]),
    ("5. Reporting", [
        "5.1 Rollout reporting counts every contact jobseekers start themselves. A jobseeker starts a contact in Ask "
        "Prairie Works by opening a conversation in the app or on the web, and on the phone by calling the claimant "
        "line, whether an adviser or the assistant's voice service answers the call.",
        "5.2 A conversation counts once however many sessions it runs to.",
    ]),
    ("6. Vendor tiers", [
        "6.1 The vendor bills the assistant by monthly usage tier. The January and February 2027 tiers were ordered "
        "on 14 December 2026. The March and April 2027 tiers are due on the vendor's order form by Friday 8 January "
        "2027.",
    ]),
]
PLAN_REVISIONS = ("Version 1.4 (16 December 2026): section 6 after the January and February order. Version 1.3 "
                  "(9 December 2026): 1.3 and section 4 added. Version 1.2 (25 November 2026): dates confirmed with "
                  "the vendor. Version 1.1 (2 November 2026): 3.2 and 3.3.")

ACC_DATE = dt.date(2026, 12, 1)
ACC_TITLE = "Acceptance test summary, Ask Prairie Works release 4.0"
ACC_SUB = ("Riverlot Dialogue Inc., delivery team, for Prairie Works Manitoba. Test window 16 to 27 November 2026; "
           "signed off 30 November 2026.")
ACC_BODY = [
    "The acceptance test ran scripted conversations against release 4.0 in the Prairie Works test tenant, written by "
    "Prairie Works Digital Channels from what jobseekers asked the assistant in 2026 and drawn in the same proportions "
    "by intent. Each conversation was scored resolved when the assistant completed the task or answered the question "
    "without an adviser.",
    "Voice conversations were placed through the claimant line's test number and passed to the voice service as the "
    "assistant-first routing will pass them.",
]
ACC_TABLE_HEAD = ("Intent", "Chat", "Voice", "Conversations", "Resolved", "Resolved share")
ACC_FOOT = ("Acceptance criterion (statement of work, schedule C): at least 80 per cent of test conversations resolved. "
            "Result: passed.")

ORDER_DATE = dt.date(2026, 12, 14)
ORDER_TITLE = "Usage tier order form, service months January to April 2027"
ORDER_CUSTOMER = [("Customer", C.ORG), ("Business number", C.BN), ("Tenant", "prairieworks-mb (production)"),
                  ("Contract", "RDI-PWM-2025-014, schedule B (usage tiers)"),
                  ("Customer contact", "Loretta Rodgers, Head of Contact Services"),
                  ("Vendor contact", "Account management, " + C.VENDOR)]
ORDER_NOTE = ("Tiers are per service month. Usage above a month's tier is billed at the overage rate in schedule B. "
              "The March and April tiers must reach the vendor by 8 January 2027 to be provisioned for 1 March.")
CHAT_TIERS = (("C1", "up to 5,000", 2900), ("C2", "5,001 to 7,500", 4100), ("C3", "7,501 to 10,000", 5300),
              ("C4", "10,001 to 12,500", 6400), ("C5", "12,501 to 15,000", 7400), ("C6", "15,001 to 20,000", 9300),
              ("C7", "20,001 to 25,000", 11200))
VOICE_TIERS = (("V1", "up to 5,000", 1500), ("V2", "5,001 to 15,000", 3900), ("V3", "15,001 to 40,000", 8700),
               ("V4", "40,001 to 80,000", 15600), ("V5", "80,001 to 120,000", 21900),
               ("V6", "120,001 to 160,000", 27400))
ORDER_ROWS = (("January 2027", "C3", "V4", "ordered 14 December 2026"),
              ("February 2027", "C3", "V4", "ordered 14 December 2026"),
              ("March 2027", "", "", "due 8 January 2027"),
              ("April 2027", "", "", "due 8 January 2027"))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pdf_stamp(d, hh=10, mi=0):
    off = -5 if (d.month, d.day) >= (3, 8) and (d.month, d.day) < (11, 1) else -6
    return ("D:%04d%02d%02d%02d%02d00%+03d'00'" % (d.year, d.month, d.day, hh, mi, off)).encode()


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
        canvas.drawString(22 * mm, 11 * mm, text)
        canvas.drawRightString(letter[0] - 22 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                             bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")


def _table(rows, widths, st, head=True, align_right=()):
    data = [[Paragraph(esc(str(c)), st["cell"]) for c in r] for r in rows]
    t = Table(data, colWidths=widths)
    style = [("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    if head:
        style.append(("FONTNAME", (0, 0), (-1, 0), "Carlito-Bold"))
    t.setStyle(TableStyle(style))
    return t


def plan_text():
    out = [PLAN_TITLE, PLAN_SUB]
    for h, paras in PLAN:
        out.append(h)
        out.extend(paras)
    out.append(PLAN_REVISIONS)
    return out


def write_plan(out):
    path = os.path.join(out, C.F_PLAN)
    st = _styles()
    doc = _doc(path, PLAN_TITLE, "Digital Channels")
    story = [Paragraph(esc(C.ORG + " | Digital Channels"), st["org"]), Paragraph(esc(PLAN_TITLE), st["h1"]),
             Paragraph(esc(PLAN_SUB), st["sub"])]
    for h, paras in PLAN:
        story.append(Paragraph(esc(h), st["h2"]))
        for p in paras:
            story.append(Paragraph(esc(p), st["body"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(esc(PLAN_REVISIONS), st["small"]))
    foot = "Prairie Works Manitoba internal. Ask Prairie Works 4.0 rollout plan v1.4"
    doc.build(story, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    PP.normalize_pdf(path, pdf_stamp(PLAN_DATE, 16, 12), pdf_stamp(PLAN_DATE, 16, 12))


def acceptance_rows():
    """the test's conversations by intent, chat and voice, and how many were resolved"""
    rows = (("Fortnightly check-in", 1069, 875, 1624), ("Payment status", 92, 76, 140),
            ("Reporting earnings", 59, 49, 90), ("Appointments", 46, 38, 70), ("Documents", 33, 27, 50),
            ("Other questions", 20, 16, 29))
    return rows


def write_acceptance(out):
    path = os.path.join(out, C.F_ACCEPT)
    st = _styles()
    doc = _doc(path, ACC_TITLE, C.VENDOR)
    story = [Paragraph(esc(C.VENDOR + " | Delivery"), st["org"]), Paragraph(esc(ACC_TITLE), st["h1"]),
             Paragraph(esc(ACC_SUB), st["sub"])]
    for p in ACC_BODY:
        story.append(Paragraph(esc(p), st["body"]))
    rows = [ACC_TABLE_HEAD]
    tc = tr = 0
    for name, chat, voice, res in acceptance_rows():
        n = chat + voice
        tc += n
        tr += res
        rows.append((name, "{:,}".format(chat), "{:,}".format(voice), "{:,}".format(n), "{:,}".format(res),
                     "%.1f%%" % (100.0 * res / n)))
    rows.append(("All intents", "", "", "{:,}".format(tc), "{:,}".format(tr), "%.1f%%" % (100.0 * tr / tc)))
    story.append(Spacer(1, 6))
    story.append(_table(rows, [52 * mm, 18 * mm, 18 * mm, 26 * mm, 22 * mm, 26 * mm], st))
    story.append(Paragraph(esc(ACC_FOOT), st["small"]))
    foot = "Riverlot Dialogue Inc. Prepared for Prairie Works Manitoba under contract RDI-PWM-2025-014"
    doc.build(story, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    PP.normalize_pdf(path, pdf_stamp(ACC_DATE, 9, 41), pdf_stamp(ACC_DATE, 9, 41))


def write_order(out):
    path = os.path.join(out, C.F_ORDER)
    st = _styles()
    doc = _doc(path, ORDER_TITLE, C.VENDOR)
    story = [Paragraph(esc(C.VENDOR + " | " + C.VENDOR_CITY), st["org"]), Paragraph(esc(ORDER_TITLE), st["h1"]),
             Paragraph(esc("Ask Prairie Works. Issued 14 December 2026."), st["sub"])]
    story.append(_table([(a, b) for a, b in ORDER_CUSTOMER], [45 * mm, 115 * mm], st, head=False))
    story.append(Paragraph(esc("Chat conversation tiers (per service month)"), st["h2"]))
    story.append(_table([("Tier", "Conversations", "Monthly fee, CAD")] +
                        [(a, b, "{:,}".format(c)) for a, b, c in CHAT_TIERS], [20 * mm, 60 * mm, 40 * mm], st))
    story.append(Paragraph(esc("Voice minute tiers (per service month)"), st["h2"]))
    story.append(_table([("Tier", "Minutes", "Monthly fee, CAD")] +
                        [(a, b, "{:,}".format(c)) for a, b, c in VOICE_TIERS], [20 * mm, 60 * mm, 40 * mm], st))
    story.append(Paragraph(esc("Service months"), st["h2"]))
    story.append(_table([("Month", "Chat tier", "Voice tier", "Status")] + [list(r) for r in ORDER_ROWS],
                        [40 * mm, 25 * mm, 25 * mm, 70 * mm], st))
    story.append(Paragraph(esc(ORDER_NOTE), st["small"]))
    foot = "Riverlot Dialogue Inc. Order form OF-2027-0112"
    doc.build(story, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    PP.normalize_pdf(path, pdf_stamp(ORDER_DATE, 11, 3), pdf_stamp(ORDER_DATE, 11, 3))
