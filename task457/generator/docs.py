"""The bundle's two documents: the conflict-of-interest policy for the clinical faculty (June 2024) and the guide to
the 2026 edition of the annual disclosure form (November 2026)."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1d21")
GREY = colors.HexColor("#5d6168")
MAROON = colors.HexColor("#6b1f2a")
L_BODY = ParagraphStyle("lb", fontName="LiberationSerif", fontSize=10.5, leading=14.4, textColor=INK, spaceAfter=6)
L_NUM = ParagraphStyle("ln", parent=L_BODY, leftIndent=26, firstLineIndent=-26)
L_TITLE = ParagraphStyle("lt", fontName="LiberationSerif-Bold", fontSize=13.5, leading=17, textColor=INK, alignment=1,
                         spaceAfter=2)
L_CAP = ParagraphStyle("lc", fontName="LiberationSerif-Italic", fontSize=9.5, leading=12.5, textColor=GREY,
                       alignment=1, spaceAfter=14)
L_H2 = ParagraphStyle("lh2", fontName="LiberationSerif-Bold", fontSize=11, leading=15, textColor=INK, spaceBefore=8,
                      spaceAfter=4)
S_BODY = ParagraphStyle("b", fontName="LiberationSans", fontSize=9.6, leading=13.4, textColor=INK, spaceAfter=6)
S_H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=MAROON, spaceAfter=2)
S_SUB = ParagraphStyle("sub", fontName="LiberationSans", fontSize=9.2, leading=12.6, textColor=GREY, spaceAfter=12)
S_H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.5, leading=14, textColor=MAROON, spaceBefore=9,
                      spaceAfter=3)
S_CELL = ParagraphStyle("c", fontName="LiberationSans", fontSize=8.8, leading=11.4, textColor=INK)
S_CELLB = ParagraphStyle("cb", parent=S_CELL, fontName="LiberationSans-Bold")


def _doc(path, title, author, footer, serif):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSerif" if serif else "LiberationSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(22 * mm, 12 * mm, footer)
        canvas.drawRightString(letter[0] - 22 * mm, 12 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=24 * mm, rightMargin=24 * mm, topMargin=20 * mm,
                          bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def write_policy(path):
    d, frame = _doc(path, "Policy on Conflicts of Interest of the Clinical Faculty", W.ORG,
                    "%s, Policy RI-14, Conflicts of Interest of the Clinical Faculty, effective 1 July 2024" % W.ORG, True)
    P = lambda t, s=L_NUM: Paragraph(t, s)
    story = [
        Paragraph(W.ORG.upper(), L_TITLE),
        Paragraph("Policy RI-14: Conflicts of Interest of the Clinical Faculty", L_TITLE),
        Paragraph("Adopted by the Board of Trustees on 11 June 2024; effective 1 July 2024. Responsible office: the %s." % W.OFFICE, L_CAP),
        Paragraph("1. Scope", L_H2),
        P("1.1&nbsp;&nbsp;This policy applies to every member of the clinical faculty: physicians, nurse practitioners and "
          "physician assistants holding a faculty appointment in a clinical department of %s." % W.ORG),
        P("1.2&nbsp;&nbsp;It supplements, and does not replace, the university's policy on financial conflicts of interest in "
          "research funded by the Public Health Service."),
        Paragraph("2. Definitions", L_H2),
        P("2.1&nbsp;&nbsp;<i>Remuneration</i> is payment for services (consulting, advisory boards, speaking, teaching, "
          "honoraria, expert testimony and other paid services) made to the faculty member personally. A payment a company "
          "makes to the university, or to anyone else, at a faculty member's request is not the faculty member's "
          "remuneration. Equity interests and royalty or licensing income are disclosed under section 3.2 and are not "
          "remuneration."),
        P("2.2&nbsp;&nbsp;A <i>manufacturer</i> is a company that reports its payments to covered recipients to Open "
          "Payments, the federal program under which manufacturers of drugs, devices, biologicals and medical supplies "
          "report those payments to the Centers for Medicare &amp; Medicaid Services. A <i>single manufacturer</i> is the "
          "company Open Payments names as making a payment, identified by its Open Payments identifier."),
        P("2.3&nbsp;&nbsp;A faculty member's <i>department</i> for a year is the department of the faculty member's primary "
          "appointment on 31 December of that year."),
        Paragraph("3. Annual disclosure", L_H2),
        P("3.1&nbsp;&nbsp;Each member of the clinical faculty holding an appointment on 31 December files an annual disclosure "
          "for that calendar year by 11:59 p.m. Eastern time on 15 January of the following year, through the office's "
          "disclosure system."),
        P("3.2&nbsp;&nbsp;The annual disclosure names each company that paid the faculty member remuneration in the year, the "
          "kind of service and the remuneration received from it, and the faculty member's equity interests and royalty or "
          "licensing income."),
        P("3.3&nbsp;&nbsp;The office may return a disclosure for correction, and a faculty member may amend a disclosure at "
          "any time. A faculty member who has not filed the year's disclosure by the date the committee's docket is "
          "prepared is referred to the chair of the department."),
        Paragraph("4. Review against Open Payments", L_H2),
        P("4.1&nbsp;&nbsp;Open Payments publishes each calendar year's payments at the end of the following June and "
          "republishes them, with manufacturers' corrections and late reports, in later publications. When a year is "
          "published the office reviews each faculty member's disclosure for the year against it and writes to the faculty "
          "member about any difference it cannot explain."),
        KeepTogether([
            Paragraph("5. The committee's annual docket", L_H2),
            P("5.1&nbsp;&nbsp;Each February the %s reviews, as its docket, the fifteen members of the clinical faculty whose "
              "remuneration from a single manufacturer in the calendar year just ended was largest, counting the "
              "remuneration each manufacturer reports to Open Payments." % W.COMMITTEE),
            P("5.2&nbsp;&nbsp;The docket is drawn from the faculty members holding an appointment on 31 December of that year "
              "who have filed the year's annual disclosure. A faculty member who has not filed it by the date the docket is "
              "prepared is referred under section 3.3 and is not estimated."),
            P("5.3&nbsp;&nbsp;Open Payments publishes the year only after the docket. Until it does, the office estimates "
              "each faculty member's remuneration from each manufacturer named in the faculty member's annual disclosure for "
              "the year, using the faculty member's disclosures and Open Payments' publications."),
            P("5.4&nbsp;&nbsp;The office uses the estimate whose figures for the latest year Open Payments has published, made "
              "in the same way from that year's annual disclosures and the disclosures and publications of the years before "
              "it, come closest to the largest remuneration from a single manufacturer that Open Payments' latest "
              "publication shows for each faculty member it estimates, closeness being the total of the absolute "
              "differences over those faculty members."),
        ]),
        Paragraph("6. Records", L_H2),
        P("6.1&nbsp;&nbsp;The office keeps each disclosure, every version of it and its submission history for seven years, "
          "with the Open Payments extracts it reviews them against."),
        Spacer(1, 10),
        Paragraph("Approved: %s, Chair, %s. Responsible officer: %s, Director, %s." % (
            W.PEOPLE["chair"], W.COMMITTEE, W.PEOPLE["director"], W.OFFICE), L_CAP),
    ]
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def write_guide(path):
    d, frame = _doc(path, "Annual Disclosure of Outside Interests, 2026", W.OFFICE,
                    "%s, %s. Annual disclosure guide, 2026 edition of the form" % (W.ORG, W.OFFICE), False)
    P = lambda t: Paragraph(t, S_BODY)
    types = [["Relationship type (2024 edition)", "Use it for"],
             ["Consulting or advisory board", "consulting agreements, advisory boards, steering committees, product reviews"],
             ["Speaking or teaching", "speaker programs, lectures, courses and honoraria for talks or teaching"],
             ["Expert testimony", "retention as an expert witness, reports and testimony"],
             ["Other paid services", "any other service the company paid you for"]]
    t = Table([[Paragraph(c, S_CELLB if i == 0 else S_CELL) for c in row] for i, row in enumerate(types)],
              colWidths=[58 * mm, 104 * mm])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, MAROON), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 3)]))
    story = [
        Paragraph("Annual Disclosure of Outside Interests: calendar year 2026", S_H1),
        Paragraph("Guide to the 2026 edition of the form. %s, November 2026." % W.OFFICE, S_SUB),
        Paragraph("Who files, and when", S_H2),
        P("Every member of the clinical faculty holding an appointment on 31 December 2026 files the annual disclosure for "
          "calendar year 2026 in the disclosure system by <b>11:59 p.m. Eastern time on Friday 15 January 2027</b>. The system "
          "opens on 1 December 2026."),
        Paragraph("What to disclose", S_H2),
        P("For each company that paid you for services in calendar year 2026, enter the company, the relationship type and "
          "the remuneration you received from it in the year, in US dollars, before taxes. If one company paid you for more "
          "than one kind of service, enter one item for each kind. Pick the company from the list; if it is not on the list, "
          "type its full name. Payments a company made to the university or to a charity at your request are not your "
          "remuneration and are not entered as items."),
        t,
        Spacer(1, 6),
        P("The 2024 edition of the form combined consulting and advisory boards, combined speaking, teaching and honoraria, "
          "and added expert testimony. Disclosures for 2021 to 2023 used the earlier types: Consulting, Advisory board, "
          "Speaking, Honoraria and Other paid services."),
        P("Equity interests (stock, options, ownership in a privately held company) and royalty or licensing income are "
          "entered in their own sections, with the relationship types Equity and Royalties or licensing."),
        Paragraph("Amending and corrections", S_H2),
        P("You may amend a disclosure at any time. The office reviews disclosures after the deadline and may return one to "
          "you for correction; resubmit it from the same screen. The disclosure in force is the latest version you "
          "submitted."),
        Paragraph("Open Payments", S_H2),
        P("Manufacturers report what they pay you to Open Payments, which publishes calendar year 2026 at the end of June "
          "2027. You can review and dispute the records about you in the Open Payments system before each publication. The "
          "office compares your disclosures with each publication."),
        Paragraph("Questions", S_H2),
        P("%s, disclosure program manager, %s." % (W.PEOPLE["analyst"], W.OFFICE)),
    ]
    d.build(story, onFirstPage=frame, onLaterPages=frame)
