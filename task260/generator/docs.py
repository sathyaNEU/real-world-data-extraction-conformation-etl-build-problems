"""The pack's documents: the service's evaluation protocol, ReadPoint's export field guide, the three vendors'
commercial proposals and the vendors' product summaries."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                   # noqa: E402
from reportlab.lib.pagesizes import A4                                             # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import mm                                                 # noqa: E402
from reportlab.pdfbase import pdfmetrics                                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                       # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
for nm, f in (("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Mono", "LiberationMono-Regular")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1d2329"), colors.HexColor("#5b6670"), colors.HexColor("#aab4bd")
BLUE = colors.HexColor("#1f4e79")
BODY = ParagraphStyle("b", fontName="Sans", fontSize=9.8, leading=13.6, textColor=INK, spaceAfter=5)
CL = ParagraphStyle("c", parent=BODY, leftIndent=24, firstLineIndent=-24)
H1 = ParagraphStyle("h1", fontName="Sans-B", fontSize=16, leading=20, textColor=BLUE, spaceAfter=2)
H2 = ParagraphStyle("h2", fontName="Sans-B", fontSize=10.6, leading=14, textColor=INK, spaceBefore=9, spaceAfter=3)
META = ParagraphStyle("m", fontName="Sans", fontSize=8.4, leading=11, textColor=GREY, spaceAfter=10)
NOTE = ParagraphStyle("n", fontName="Sans", fontSize=7.8, leading=10, textColor=GREY, spaceBefore=8)
CELL = ParagraphStyle("cell", fontName="Sans", fontSize=8.8, leading=11.4, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Sans-B")


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=22 * mm,
                             bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.6)
        canvas.drawString(22 * mm, A4[1] - 12 * mm, left)
        canvas.drawRightString(A4[0] - 22 * mm, A4[1] - 12 * mm, right)
        canvas.drawRightString(A4[0] - 22 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(rows, widths, bold_first=True):
    data = [[Paragraph(str(c), CELLB if (i == 0 and bold_first) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, 1), (-1, -1), 0.25, RULE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def write_protocol(path):
    lead, director = K.PEOPLE["lead"], K.PEOPLE["director"]
    story = [Paragraph("AI reading support: evaluation and procurement protocol", H1),
             Paragraph("%s. Owner: %s, AI evaluation lead. Version 2, approved by %s, clinical director, on 12 January "
                       "2026." % (K.ORG, lead, director), META)]
    sections = [
        ("1. Purpose and scope", [
            "1.1 This protocol governs how the service evaluates AI reading-support tools (software that shows a film "
            "reader marks and a suspicion score while they read a screening mammogram) and how it chooses one to "
            "license.",
            "1.2 The service will license at most one tool, for two years from 1 April 2027, for use by its film "
            "readers on its routine screening examinations. The service reads about 45,000 screening studies a year "
            "from four screening sites and three mobile units."]),
        ("2. Reader studies", [
            "2.1 Each shortlisted tool is evaluated in its own reader study on ReadPoint.",
            "2.2 Panel: ten of the service's film readers, drawn within each role (consultant radiologists, "
            "consultant and advanced practitioner radiographers, breast clinicians) in proportion to the service's "
            "film readers.",
            "2.3 Study set: 300 examinations from the service's 2019 to 2022 screening archive, sampled within two "
            "groups: 75 examinations of women whose breast cancer was confirmed by histology (cancers "
            "detected at that screen, and interval cancers diagnosed within 36 months of it) and 225 examinations "
            "that were normal at the woman's next screening round. Each study draws its own set.",
            "2.4 Every panel reader reads every examination in the set twice, once unaided and once with the tool, in "
            "sessions at least four weeks apart; half the panel reads unaided first.",
            "2.5 For each examination the reader records a probability of malignancy from 0 to 100 and a recall "
            "decision."]),
        ("3. Measure", [
            "3.1 A reader's accuracy in a condition is the area under the empirical ROC curve of their "
            "probability-of-malignancy ratings against the reference standard (cancer or normal, section 2.3).",
            "3.2 A tool's gain is the readers' average area with the tool minus their average area unaided."]),
        ("4. Decision", [
            "4.1 A tool qualifies when the two-sided 95 per cent confidence interval for its gain lies wholly above "
            "zero. The gain and its interval are for the service's film readers reading the service's screening "
            "examinations.",
            "4.2 The service licenses the qualifying tool with the largest gain.",
            "4.3 If no tool qualifies, the service keeps unaided double reading for 2027 and evaluates again in 2028.",
            "4.4 Cost, integration and support are assessed by procurement after the clinical decision and do not "
            "change it."]),
        ("5. Calendar", [
            "5.1 Reader studies run from February to September 2026; the procurement invitation is issued on 1 "
            "September 2026; the AI evaluation panel takes the decision on 18 November 2026."]),
    ]
    for h, paras in sections:
        story.append(Paragraph(h, H2))
        for t in paras:
            story.append(Paragraph(t, CL))
    story.append(Paragraph("Questions about this protocol go to the AI evaluation lead.", NOTE))
    doc = _doc(path, "AI reading support: evaluation and procurement protocol", lead)
    f = _frame(K.ORG, "AI evaluation protocol, version 2")
    doc.build(story, onFirstPage=f, onLaterPages=f)


def write_export_guide(path):
    story = [Paragraph("Reader study exports: field guide", H1),
             Paragraph("ReadPoint support. Applies to project exports from platform versions 4.1 and 4.2 (4.2 released "
                       "on 1 July 2026). Last revised 3 July 2026.", META)]
    story.append(Paragraph("About exports", H2))
    for t in ["An export holds one row for every submission made in the project, practice cases included. Each "
              "session can open with practice cases configured by the project owner.",
              "A reader can reopen a case from the session list until the session is closed. Every submission is "
              "exported; the reading of record is the reader's last submission for the case and condition.",
              "Reader identifiers are pseudonymous and unique within a project. Times are recorded in UTC."]:
        story.append(Paragraph(t, BODY))
    story.append(Paragraph("Version 4.1", H2))
    rows = [["Field", "Meaning"],
            ["project", "the project code"], ["user_id", "the reader's identifier in the project"],
            ["case_code", "the case as configured by the project owner"],
            ["arm", "UNAIDED, or AIDED when the project's decision-support overlay was shown"],
            ["session_no", "the reader's sessions in the order they were opened"],
            ["position", "the case's place in the session"],
            ["opened_utc, submitted_utc", "when the case was opened and the reading submitted"],
            ["pom", "the reader's probability of malignancy, a whole number from 0 to 100"],
            ["recall", "the reader's recall decision, Y or N"],
            ["revision", "1 for the first submission of a case in a session, 2 for the next"]]
    story += [_table(rows, (48, 118)), Spacer(1, 4)]
    story.append(Paragraph("Version 4.2", H2))
    rows = [["Field", "Meaning"],
            ["project_code", "the project code"], ["reader_ref", "the reader's identifier in the project"],
            ["case_ref", "the case as configured by the project owner"],
            ["condition", "Unaided, or AI-assisted when the decision-support overlay was shown"],
            ["session, seq", "the reader's session number and the case's place in it"],
            ["started_at, completed_at", "when the case was opened and the reading submitted (ISO 8601)"],
            ["malignancy_probability", "the reader's probability of malignancy, from 0 to 1 in steps of 0.01"],
            ["recall_decision", "Recall to assessment, or Return to routine recall"],
            ["edit_count", "0 for the first submission of a case in a session, 1 for the next"],
            ["workstation", "the reading workstation's identifier"]]
    story += [_table(rows, (48, 118))]
    story.append(Paragraph("ReadPoint support: exports are produced on request by the project owner.", NOTE))
    doc = _doc(path, "Reader study exports: field guide", "ReadPoint support")
    f = _frame("ReadPoint support centre", "Article RP-EXP-041")
    doc.build(story, onFirstPage=f, onLaterPages=f)


QUOTE_TEXT = {
    # Each vendor answers the same invitation to tender in its own house voice: its own scope sentence, its own way of
    # stating the basis of charge and its own commercial terms. The charges and their bases are the ones costs() uses.
    "Ondrix": dict(
        company="Ondrix Imaging Ltd", product="Ondrix Mammo", who="ondrix", role="Account Director",
        head="Quotation ONX-UK-2026-0187, {date}<br/>Prepared for {attn}<br/>Prepared by {person}, {role}<br/>"
             "In response to the invitation to tender issued on 1 September 2026",
        scope="Ondrix Imaging proposes a licence for Ondrix Mammo covering all of the service's film readers for two "
              "contract years from 1 April 2027, including integration with the service's PACS and reading "
              "workstations, user training and support. Ondrix Mammo marks suspicious regions on each view and gives "
              "every screening study a suspicion score from 1 to 10, shown to the film reader in the reading "
              "application.",
        charges=[["Item", "Charge"],
                 ["Analysis charge", "1.62 per screening study received for analysis"],
                 ["Minimum annual charge", "60,000 per contract year"],
                 ["Integration and training", "14,800, one-off, invoiced in the first contract year"]],
        basis=["A screening study is a mammography study of the screening programme that the service's PACS sends "
               "for analysis: routine screening studies and technical repeats. Assessment and symptomatic studies are "
               "not sent.",
               "First-year charges are calculated on the service's screening studies in the 12 months to 30 September "
               "2026, as the invitation to tender asks; the second year's charge is reconciled to first-year actuals."],
        terms="Charges are invoiced quarterly in arrears and the minimum annual charge applies to each contract year. "
              "Payment is due within 30 days of invoice. This quotation is open for acceptance until 31 January 2027 "
              "and is subject to contract."),
    "Halvic": dict(
        company="Halvic Medical Ltd", product="Halvic Breast", who="halvic", role="Key Account Manager",
        head="Prepared for {attn}, in response to the invitation to tender of 1 September 2026. {person}, {role}, "
             "{date}.",
        scope="Halvic Medical will supply Halvic Breast to the service for two contract years from 1 April 2027: a "
              "reader licence for each of the service's film readers and a site licence for each of its screening "
              "sites, with integration into the service's PACS and reading workstations, on-site training and second "
              "line support. Halvic Breast overlays region marks and a case score on the reading workstation and keeps "
              "a review log for each film reader.",
        charges=[["Item", "Charge"],
                 ["Reader licence", "2,450 per film reader seat per contract year"],
                 ["Site licence", "5,900 per screening site per contract year, the site's mobile units included"],
                 ["Implementation", "12,000, one-off, invoiced in the first contract year"]],
        basis=["Reader seats are licensed for each film reader in post at the start of the contract year. Site "
               "licences are charged for the service's four screening sites.",
               "There are no per-study or volume-based charges."],
        terms="Reader and site licences are invoiced annually in advance on 1 April, the implementation fee with the "
              "first invoice, on 30-day payment terms. Prices are held for both contract years. This proposal remains "
              "valid until 31 January 2027."),
    "Lumidra": dict(
        company="Lumidra AI Ltd", product="Lumidra Detect", who="lumidra", role="Customer Success Lead",
        head="For {attn}<br/>Your invitation to tender: 1 September 2026<br/>Quote prepared by {person}, {role}, on "
             "{date}",
        scope="Thank you for inviting us to quote. This is our price for licensing Lumidra Detect to all of your film "
              "readers for two contract years from 1 April 2027, with PACS and workstation integration, onboarding "
              "and support included. Lumidra Detect scores every screening case from 0 to 100 and highlights the "
              "regions behind the score in the reader's viewer.",
        charges=[["Item", "Charge"],
                 ["Episode charge", "2.08 per screening episode"],
                 ["Reader accounts", "340 per film reader account per contract year"],
                 ["Implementation", "9,500, one-off, invoiced in the first contract year"]],
        basis=["A screening episode is one woman's screening in a screening round, including any technical repeat "
               "needed to complete it. Each episode is counted once, in the period in which its routine screening "
               "study took place.",
               "We open a reader account for each film reader in post at the start of each contract year.",
               "Year one is charged on your screening episodes in the 12 months to 30 September 2026, as your "
               "invitation to tender asks; year two is reconciled to year-one actuals."],
        terms="We invoice quarterly in advance on 30-day terms. This quote is open for 90 days from the date above."),
}


QUOTE_STYLE = {
    # Ondrix: plain sans, blue rule under the title; Halvic: serif letter with numbered sections and a ruled grid;
    # Lumidra: sans with a dark band across the top, purple headings and its own section names.
    "Ondrix": dict(font="Sans", bold="Sans-B", ink="#1d2329", accent="#24548c", grid=False, band=None,
                   heads=("Scope", "Charges", "Basis of charge", "Terms"), size=9.8, margin=22),
    "Halvic": dict(font="Serif", bold="Serif-B", ink="#202020", accent="#2d5e3e", grid=True, band=None,
                   heads=("1. Scope of supply", "2. Pricing", "3. How charges are calculated", "4. Commercial terms"),
                   size=10.4, margin=25),
    "Lumidra": dict(font="Sans", bold="Sans-B", ink="#262a33", accent="#6b2f7a", grid=False, band="#2b2140",
                    heads=("Your quotation", "Fees", "What we count", "Terms"), size=10.2, margin=20),
}


def write_quote(path, key):
    q, st = QUOTE_TEXT[key], QUOTE_STYLE[key]
    person = K.PEOPLE[q["who"]]
    date = K.QUOTE_DATES[key]
    ink, acc = colors.HexColor(st["ink"]), colors.HexColor(st["accent"])
    body = ParagraphStyle("qb", fontName=st["font"], fontSize=st["size"], leading=st["size"] * 1.38, textColor=ink,
                          spaceAfter=5)
    h1 = ParagraphStyle("qh1", fontName=st["bold"], fontSize=16, leading=20, textColor=acc, spaceAfter=3)
    h2 = ParagraphStyle("qh2", fontName=st["bold"], fontSize=st["size"] + 1, leading=14, textColor=acc, spaceBefore=9,
                        spaceAfter=3)
    meta = ParagraphStyle("qm", fontName=st["font"], fontSize=8.6, leading=11.5, textColor=GREY, spaceAfter=10)
    cell = ParagraphStyle("qc", fontName=st["font"], fontSize=st["size"] - 0.8, leading=12, textColor=ink)
    cellb = ParagraphStyle("qcb", parent=cell, fontName=st["bold"])
    data = [[Paragraph(str(c), cellb if i == 0 else cell) for c in r] for i, r in enumerate(q["charges"])]
    t = Table(data, colWidths=[52 * mm, 114 * mm], hAlign="LEFT")
    style = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 4),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if st["grid"]:
        style += [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8efe9"))]
    else:
        style += [("LINEBELOW", (0, 0), (-1, 0), 0.8, acc), ("LINEBELOW", (0, 1), (-1, -1), 0.25, RULE)]
    t.setStyle(TableStyle(style))
    hd = st["heads"]
    attn = "%s, Procurement Manager, %s" % (K.PEOPLE["procurement"], K.ORG)
    head = q["head"].format(attn=attn, person=person, role=q["role"], date=date.strftime("%d %B %Y").lstrip("0"))
    story = [Paragraph("Commercial proposal: %s" % q["product"], h1),
             Paragraph(head, meta),
             Paragraph(hd[0], h2),
             Paragraph(q["scope"], body),
             Paragraph(hd[1], h2),
             Paragraph("Prices are in pounds sterling and exclude VAT.", body), t, Spacer(1, 6),
             Paragraph(hd[2], h2)]
    for x in q["basis"]:
        story.append(Paragraph(x, body))
    story.append(Paragraph(hd[3], h2))
    story.append(Paragraph(q["terms"], body))
    m = st["margin"] * mm
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=m, rightMargin=m, topMargin=m + (8 * mm if st["band"] else 0),
                            bottomMargin=20 * mm, title="Commercial proposal: %s" % q["product"], author=person,
                            subject="", creator="", producer="")

    def frame(canvas, doc_):
        canvas.saveState()
        if st["band"]:
            canvas.setFillColor(colors.HexColor(st["band"]))
            canvas.rect(0, A4[1] - 16 * mm, A4[0], 16 * mm, stroke=0, fill=1)
            canvas.setFillColor(colors.white)
            canvas.setFont(st["bold"], 11)
            canvas.drawString(m, A4[1] - 10 * mm, q["company"])
        else:
            canvas.setFillColor(GREY)
            canvas.setFont(st["font"], 7.8)
            canvas.drawString(m, A4[1] - 12 * mm, q["company"])
            canvas.drawRightString(A4[0] - m, A4[1] - 12 * mm, "Commercial in confidence")
        canvas.setFillColor(GREY)
        canvas.setFont(st["font"], 7.4)
        canvas.drawString(m, 11 * mm, "%s, registered in England and Wales." % q["company"])
        canvas.drawRightString(A4[0] - m, 11 * mm, "%d" % doc_.page if key == "Halvic" else "Page %d" % doc_.page)
        canvas.restoreState()
    doc.build(story, onFirstPage=frame, onLaterPages=frame)


def write_product_summaries(path):
    story = [Paragraph("AI reading support: vendor product summaries", H1),
             Paragraph("Compiled for the AI evaluation panel from the vendors' shortlisting submissions, January 2026. "
                       "Figures are the vendors' own and have not been checked by the service.", META)]
    rows = [["", "Lumidra Detect", "Ondrix Mammo", "Halvic Breast"],
            ["Regulatory status", "UKCA, class IIa", "UKCA, class IIa", "UKCA and CE, class IIa"],
            ["Output to the reader", "case score 0 to 100, region highlights",
             "suspicion score 1 to 10, region marks", "case score and region marks, reader review log"],
            ["Standalone performance reported by the vendor", "AUC 0.94 on 31,800 examinations (United States and "
             "Sweden)", "AUC 0.92 on 18,400 examinations (Netherlands)", "AUC 0.91 on 22,700 examinations (England)"],
            ["Reading-time effect claimed", "none stated", "about 10 per cent shorter", "about 5 per cent longer"],
            ["Integration", "DICOM structured report, viewer plug-in", "secondary capture and structured report",
             "workstation overlay"],
            ["Reference sites", "two", "four", "three"]]
    story += [_table(rows, (42, 41, 41, 42)), Spacer(1, 6)]
    story.append(Paragraph("Standalone figures describe each tool reading on its own, on the vendor's datasets; they "
                           "are not results of the service's reader studies.", BODY))
    doc = _doc(path, "AI reading support: vendor product summaries", K.PEOPLE["lead"])
    f = _frame(K.ORG, "Vendor product summaries")
    doc.build(story, onFirstPage=f, onLaterPages=f)
