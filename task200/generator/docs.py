"""The airport's own documents: the screener performance standard SPS-04 (the WHAT for the course order and the
definitions the 2027 plan uses), the course planning email, and the compliance team's 2026 review."""
import os

import office as O

SPS_BLOCKS = [
    ("Heading1", "SPS-04 Screener performance standard"),
    (None, "Brackenford Airport Ltd, Security Screening. Issue 3, effective 1 December 2026. Owner: Head of Security "
           "Screening. Approved by Marian Taylor, Head of Security Screening, 24 November 2026."),
    ("Heading2", "1 Purpose"),
    (None, "This standard sets how the airport keeps its X-ray screeners able to find prohibited articles in "
           "passengers' cabin baggage, what the screening teams' records count, and how the annual remedial image "
           "interpretation course is ordered."),
    ("Heading2", "2 Scope"),
    (None, "Every security officer (screener) and screening supervisor who works an X-ray screen at Central Search "
           "or at Pier B Search."),
    ("Heading2", "3 Definitions"),
    ("ListBullet", "**Team.** A screener belongs to the screening team they are rostered to on 31 December of the review "
                   "year, whichever team they worked in earlier in the year."),
    ("ListBullet", "**X-ray screen.** A remote screening workstation in the Central Search screening room, or one of "
                   "the Pier B X-ray screens."),
    ("ListBullet", "**Screen time.** The time a screener is logged on at an X-ray screen."),
    ("ListBullet", "**Threat image projection.** The screening system superimposes the image of a threat article on "
                   "the image of a passenger's bag at the screen. A projection the screener marks as a threat within the "
                   "time the screen allows is a hit and one the screener does not mark is a miss. A projection cancelled "
                   "before it is shown counts as neither."),
    ("ListBullet", "**Search.** Each tray an X-ray decision sends to the search position is a search, and it is charged "
                   "to the screener whose decision sent it. A search in which the search officer finds nothing at all, "
                   "prohibited or restricted, is a clear search."),
    ("ListBullet", "**Image interpretation certificate.** A screener holds one certificate at a time. It runs for three "
                   "years from the day of the assessment that awarded it, and a later pass at a certification "
                   "assessment replaces it. An assessment the screener does not pass awards nothing, and the annual "
                   "image interpretation refresher renews nothing."),
    ("Heading2", "4 The remedial image interpretation course"),
    (None, "4.1 Each year the Head of Security Screening sets the order in which the screening teams go through the "
           "remedial image interpretation course in the following year, one team a course month."),
    (None, "4.2 The course starts with the team whose X-ray operators are least likely to find a prohibited article in "
           "a passenger's cabin bag, and the order runs from there to the team most likely to find one."),
    (None, "4.3 The order is set each January, on how the teams screened in the year just ended."),
    ("Heading2", "5 Working at the screen"),
    (None, "5.1 No screener works an X-ray screen for more than 20 minutes at a stretch, and after a stretch a screener "
           "works at least 20 minutes away from the screens before the next."),
    (None, "5.2 A screener who is new to the airport works the screens only after passing the image interpretation "
           "assessment."),
    ("Heading2", "6 Records"),
    (None, "The screening systems' projection, session and reject records, the search team's search log and the training "
           "register are kept for five years from the end of the year they cover."),
    ("Heading2", "Revision history"),
    ("TABLE", ([["Issue", "Effective", "Change"],
                ["1", "4 March 2024", "First issue, with the Central Search CT lanes and screening room"],
                ["2", "1 September 2025", "Search definitions aligned with the search team's tablet log"],
                ["3", "1 December 2026", "Section 4 added: the order of the remedial image interpretation course"]],
               [1100, 2000, 6300])),
]

EML = """Return-Path: <bernard.vincent@brackenfordairport.co.uk>
Received: from BRKEX02.brackenfordairport.local (10.20.4.12) by BRKEX01.brackenfordairport.local
 (10.20.4.11) with Microsoft SMTP Server id 15.2.1544.4; Tue, 12 Jan 2027 15:47:19 +0000
From: Bernard Vincent <bernard.vincent@brackenfordairport.co.uk>
To: Marian Taylor <marian.taylor@brackenfordairport.co.uk>
Subject: RE: Remedial course 2027
Date: Tue, 12 Jan 2027 15:47:12 +0000
Message-ID: <DB9PR03MB7713A2C5E91D44B0F2C1A6B4E8D20@BRKEX02.brackenfordairport.local>
In-Reply-To: <DB9PR03MB77135D0C41A24E6B93F1E2A8E8D10@BRKEX02.brackenfordairport.local>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 7bit

Marian,

The training rooms are booked for the first two weeks of each month from February to
July, so six blocks and one team in each, as SPS-04 has it. I need your order by Friday
22 January so the February team gets its roster in time.

For the cover plan can I also have each team's 2026 screen time, and how many clear
searches each team sent to search last year, so the trainers know how much of each
block to give to the clutter and false-alarm session? And anyone whose image
interpretation certificate runs out before 1 July, team by team, so we can recertify
them while they are on the course rather than book separate sittings at the centre.

Thanks
Bernard

Bernard Vincent
Security Training Manager
Brackenford Airport Ltd

-----Original Message-----
From: Marian Taylor <marian.taylor@brackenfordairport.co.uk>
Sent: 11 January 2027 09:05
To: Bernard Vincent <bernard.vincent@brackenfordairport.co.uk>
Subject: Remedial course 2027

Bernard,

We can start the 2027 remedial course in February. I'll set the order once the January
extracts are in, which IT say is this week.

Marian
"""


def compliance_review(path):
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12.6, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=14, spaceAfter=6)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=8, spaceAfter=3)
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=8.4, leading=10.4)

    def story():
        s = [Paragraph("Security compliance review 2026", h1),
             Paragraph("Compliance and Quality, Security Screening. Reviewed at the security management meeting of "
                       "14 December 2026.", body),
             Paragraph("1 Scope", h2),
             Paragraph("This review covers the airport's own quality control activity in 2026: the staff and vehicle "
                       "search point, the liquids, aerosols and gels screening at Central Search and Pier B, the "
                       "walk-through metal detector checks and the covert testing the airport commissions each year. "
                       "Screener image interpretation is covered by SPS-04 and is outside this review.", body),
             Paragraph("2 Findings", h2)]
        rows = [["Area", "Checks", "Finding", "Action"],
                ["Staff and vehicle search point", "48 audits", "Two audits found vehicle permits checked against an "
                 "out-of-date list (May)", "List now issued weekly by ID Centre; closed"],
                ["Liquids at Central Search", "36 audits", "Liquids explosive detection used on 98.6 per cent of "
                 "containers over 100 ml presented as medicines", "Briefing at team meetings; closed"],
                ["Liquids at Pier B", "18 audits", "Signage for the 100 ml rule missing at the Pier B divest tables "
                 "for three weeks in July", "Replaced 29 July; closed"],
                ["Walk-through metal detectors", "Daily test pieces", "All daily tests recorded; one archway failed "
                 "its test on 3 October and was taken out of use", "Repaired 4 October; closed"],
                ["Covert testing", "16 tests", "Fourteen test articles detected; the two not detected were at the "
                 "divest and archway stage, not at an X-ray screen", "Individual coaching; closed"]]
        t = Table([[Paragraph(c, cell) for c in r] for r in rows], colWidths=[34 * mm, 22 * mm, 66 * mm, 44 * mm])
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.55, 0.55, 0.55)),
                               ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.86, 0.89, 0.94)),
                               ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        s += [t, Spacer(1, 6),
              Paragraph("3 Next year", h2),
              Paragraph("The 2027 programme keeps the same audit counts, adds two covert tests at Pier B before the "
                        "summer schedule, and moves the liquids audits at Pier B to the early departure wave, when "
                        "most of the pier's passengers are screened.", body)]
        return s
    O.pdf(path, story, title="Security compliance review 2026", author="Compliance and Quality",
          created_pdf="20261216104500", footer="Brackenford Airport Ltd  |  Security compliance review 2026  |  Internal")


def write_all(target, F):
    O.docx(os.path.join(target, F["sps"]), SPS_BLOCKS, author="Marian Taylor", created="2024-02-19T10:22:00Z",
           modified="2026-11-24T14:36:00Z", revision=14, total_time=212)
    p = os.path.join(target, F["eml"])
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(EML.replace("\n", "\r\n"))
    compliance_review(os.path.join(target, F["review"]))
