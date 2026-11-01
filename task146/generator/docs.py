"""task146 architecture 2: the Society's documents (the ALM policy section, the Board minute, the treasury's email)."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ORG = "Trentmoor Building Society"
DOMAIN = "trentmoor.co.uk"
TREASURER = ("Hugh Clements", "hugh.clements")
ANALYST = ("Liam Bowen", "liam.bowen")
SECRETARY = ("Jennifer Russell", "jennifer.russell")


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.8, leading=13.6, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=5)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.6, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10.5, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=8.2, leading=10.2)
    return body, h1, h2, small, cell


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, creator=author, subject=subject,
                             invariant=1)


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3E8EF"))]))
    return t


def policy(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Asset and Liability Management Policy, Section 7: Structural hedge", "Treasury", "Policy")
    s = [Paragraph(ORG + " | Asset and Liability Management Policy", small),
         Paragraph("Section 7. The structural hedge", h1),
         Paragraph("Version 4, approved by the Board on 24 September 2024. Owner: the Treasurer. Reviewed annually "
                   "by the Asset and Liability Committee (ALCO).", small), Spacer(1, 4)]
    paras = [
        ("7.1 Purpose", ["Part of the money members keep in instant-access savings stays with the Society for years "
                         "whatever Bank Rate does. The Society invests the interest rate exposure on that part in "
                         "receive-fixed interest rate swaps, so that the margin it earns on it does not move with "
                         "each change in Bank Rate. This section sets how large the hedge is and how it is reset."]),
        ("7.2 Instant-access savings", ["Instant-access savings are the Society's savings products from which a "
                                        "member may withdraw on demand: Easy Saver, each issue of the Loyalty Saver, "
                                        "the Easy Access Cash ISA and Young Saver. Fixed-rate bonds and notice "
                                        "accounts are not instant-access savings."]),
        ("7.3 The stable balance", [
            "A balance held in instant-access savings at a 30 November is kept to an anniversary of that date to the "
            "extent the Society held it in instant-access savings at every month end from that 30 November to the "
            "anniversary.",
            "The share of a product's balances kept to an anniversary is the balances held in that product at every "
            "30 November from November 2021 whose anniversary has passed, taken together, set against the part of "
            "them kept to that anniversary.",
            "A product's stable balance at an anniversary of the measurement date is its balance at the measurement "
            "date times its share kept to the same anniversary. The Society's stable balance is the sum of its "
            "products' stable balances. The measurement date is the 30 November before each reset, and the stable "
            "balance is measured at its first, second and third anniversaries."]),
        ("7.4 The January reset", [
            "Each January the Board sets the hedge at the Society's stable balance at the first anniversary of the "
            "measurement date, to the nearest GBP 1 million. The swap maturing that January is replaced by a new "
            "three-year receive-fixed swap of the notional that brings the swaps outstanding to the hedge; where "
            "the swaps that remain already exceed the hedge, no new swap is taken and the excess is terminated, the "
            "swap with the nearest maturity first.",
            "After the reset, the swaps outstanding at the second and third anniversaries of the measurement date "
            "may not exceed the stable balance at those anniversaries. ALCO reports both to the Board with the "
            "reset."]),
        ("7.5 Governance", ["The Treasurer prepares the reset paper for the Board's January meeting from the "
                            "Society's own records as at the measurement date. Hedge accounting follows the "
                            "Society's accounting policies and is outside this section."]),
    ]
    for head, ps in paras:
        s.append(Paragraph(head, h2))
        for p in ps:
            s.append(Paragraph(p, body))
    s.append(Paragraph("Version history", h2))
    s.append(_grid([["Version", "Approved", "Change"],
                    ["2", "September 2019", "Hedge introduced on Easy Saver and the Cash ISA"],
                    ["3", "September 2022", "Loyalty Saver issues and Young Saver brought within the hedge"],
                    ["4", "September 2024", "Second and third anniversaries added to the reset (7.3, 7.4)"]],
                   [22 * mm, 34 * mm, 114 * mm], cell))
    doc.build(s, onFirstPage=_footer("ALM Policy s.7 v4 | " + ORG), onLaterPages=_footer("ALM Policy s.7 v4 | " + ORG))


def minutes(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Board minute extract, 27 January 2026", "Society Secretary", "Minutes")
    s = [Paragraph(ORG + " | Minutes of the Board, 27 January 2026 (extract)", small),
         Paragraph("Minute 2026/07: Structural hedge reset", h1),
         Paragraph("Present: the Chair, the Chief Executive, the Finance Director, the Treasurer and four "
                   "non-executive directors. In attendance: the Society Secretary.", small), Spacer(1, 3),
         Paragraph("The Treasurer presented the January reset of the structural hedge under section 7 of the Asset "
                   "and Liability Management Policy. The swap of GBP 47.0 million taken in January 2023 matured on "
                   "30 January 2026.", body),
         Paragraph("The Board approved a new three-year receive-fixed swap of GBP 52.4 million, cleared and maturing "
                   "on 29 January 2029, bringing the swaps outstanding to GBP 152.9 million. The Board noted that the "
                   "swaps outstanding at the second and third anniversaries were within the limits of section 7.4.", body),
         Paragraph("Action: the Treasurer to bring the January 2027 reset to the Board's meeting on 26 January 2027.",
                   body),
         Spacer(1, 6), Paragraph("Extract certified by the Society Secretary, " + SECRETARY[0] + ".", small)]
    doc.build(s, onFirstPage=_footer("Board minutes 27.01.2026 | " + ORG),
              onLaterPages=_footer("Board minutes 27.01.2026 | " + ORG))


def email(path):
    text = f"""From: {TREASURER[0]} <{TREASURER[1]}@{DOMAIN}>
To: {ANALYST[0]} <{ANALYST[1]}@{DOMAIN}>
Cc: {SECRETARY[0]} <{SECRETARY[1]}@{DOMAIN}>
Date: Thu, 03 Dec 2026 08:52:17 +0000
Subject: January hedge reset
Message-ID: <20261203085217.6620.hclements@{DOMAIN}>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 8bit

Liam,

The core system extract for 30 November came through last night, so we
can start on the reset. The paper goes in the Board pack on 19 January
for the meeting on the 26th, and the swap has to be traded on the 29th
when the 2024 swap matures.

I have put the swap register as at yesterday in the folder with the
extract, the product register and the rest.

Thanks,
Hugh

--
{TREASURER[0]}
Treasurer
{ORG}
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
