"""The pack's documents for task271: the mutual's Frequency Model Standard, its homeowners underwriting guide and
the board's expansion brief, the water authority's master plan excerpt (PDF), and the data dictionary and pack
contents (CSV and text)."""
from __future__ import annotations

import csv

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import letter                                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import inch                                                # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic"), ("Sans", "LiberationSans-Regular"),
              ("Sans-B", "LiberationSans-Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans", boldItalic="Sans-B")
INK, GREY, RULE = colors.HexColor("#1b1f24"), colors.HexColor("#5a626c"), colors.HexColor("#bfc6ce")
GREEN = colors.HexColor("#1f4e3d")
BLUE = colors.HexColor("#1b3a5c")


def us_date(d):
    return "%s %d, %d" % (d.strftime("%B"), d.day, d.year)


def styles(face, accent):
    b = face
    body = ParagraphStyle("b", fontName=b, fontSize=10.2, leading=13.6, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=b + "-B", fontSize=14.5, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=b + "-B", fontSize=10.8, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=b, fontSize=8.6, leading=11.2, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=b, fontSize=8.3, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=b + "-B", fontSize=8.3, leading=10.4, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=28, firstLineIndent=-28),
        note=ParagraphStyle("n", fontName=b, fontSize=8.1, leading=10.4, textColor=GREY, spaceBefore=4))


def _frame(left, right, face):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(face, 7.6)
        canvas.drawString(0.9 * inch, letter[1] - 0.55 * inch, left)
        canvas.drawRightString(letter[0] - 0.9 * inch, letter[1] - 0.55 * inch, right)
        canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.8),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _build(path, story, left, right, title, author, face="Serif"):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.85 * inch, bottomMargin=0.8 * inch, title=title, author=author,
                            subject="", creator="", producer="")
    fr = _frame(left, right, face)
    doc.build(story, onFirstPage=fr, onLaterPages=fr)


def standard(path):
    S = styles("Serif", GREEN)
    P = lambda t, s="body": Paragraph(t, S[s])   # noqa: E731
    st = [P(K.ORG, "meta"), P("Frequency Model Standard", "h1"),
          P("Revision 2. Adopted by the Actuarial and Risk Committee of the Board of Directors on %s; prepared with "
            "the company's consulting actuary. Supersedes revision 1 (2019)." % us_date(K.STANDARD_DATE), "meta"),
          P("1. Purpose", "h2"),
          P("This standard sets how the company estimates the claim frequencies it uses for planning, for rate "
            "reviews and for its reinsurance submissions, so that a frequency quoted in any of them can be "
            "reproduced from the company's records."),
          P("2. Definitions", "h2"),
          P("2.1&nbsp;&nbsp;A <i>claim</i> is a reported loss given a claim number, whether or not anything is paid on "
            "it. A claim reopened under the original number with a suffix is the same claim.", "clause"),
          P("2.2&nbsp;&nbsp;<i>Non-weather water</i> is the sudden and accidental discharge of water from within a "
            "plumbing, heating or air-conditioning system or a household appliance: cause codes WTR-P and WTR-A "
            "before 2024 and 3110, 3120 and 3130 from January 1, 2024. Freezing, backup of sewers or drains, "
            "seepage and surface water are other perils.", "clause"),
          P("2.3&nbsp;&nbsp;The <i>accident year</i> of a claim is the calendar year of its date of loss.", "clause"),
          P("2.4&nbsp;&nbsp;A <i>house-year</i> is one home insured for one year. A policy term earns house-years day by "
            "day from its effective date to its expiration, or to a cancellation that was not reinstated; a "
            "cancellation reinstated without a lapse earns as if it had not happened. A calendar year of 366 days "
            "earns 1/366 of a house-year a day.", "clause"),
          P("2.5&nbsp;&nbsp;A <i>frequency</i> is claims per 1,000 house-years.", "clause"),
          P("3. Characteristics of a home", "h2"),
          P("A home's characteristics on a policy term are read as the rating plan groups them: the year built in "
            "four eras (before 1940, 1940 to 1969, 1970 to 1999, 2000 and later), construction, foundation, full "
            "bathrooms (1, 2, 3, 4 or more) and stories, each as recorded on the term. A home on the county "
            "assessment roll is described by its principal dwelling (card 1) in the same groupings; the roll's "
            "foundations map to the company's codes as the underwriting guide sets out."),
          P("4. Choosing a frequency model", "h2"),
          P("A frequency comes from a Poisson model of claim counts with the logarithm of house-years as an offset, "
            "whose terms are the main effects of categorical characteristics of the home. Of the models considered, "
            "the company uses the one that best predicts the latest full accident year's claims when it is fitted "
            "to the accident years before it, judged by the Poisson deviance on that year. The chosen model is then "
            "refitted on every accident year of the experience period."),
          P("5. A territory the company has not written", "h2"),
          P("For a territory where the company has no experience, the frequency is the mean, over the territory's "
            "homes, of each home's frequency under the chosen model."),
          P("6. Experience period", "h2"),
          P("For plans made in 2026 the experience period is accident years 2023 to 2025, with the claims and "
            "payments on the company's systems at the August 31, 2026 extract; the latest full accident year is "
            "2025."),
          Spacer(1, 6),
          P("Approved for the committee by %s, President. Questions on this standard go to the Underwriting "
            "Manager." % K.PRESIDENT, "note")]
    _build(path, st, K.ORG, "Frequency Model Standard, Rev. 2", "Frequency Model Standard", K.ORG)


def guide(path):
    S = styles("Serif", GREEN)
    P = lambda t, s="body": Paragraph(t, S[s])   # noqa: E731
    st = [P(K.ORG, "meta"), P("Underwriting Guide, Homeowners", "h1"),
          P("Edition of %s. Applies to new business and renewals effective on or after March 1, 2025." %
            us_date(K.GUIDE_DATE), "meta"),
          P("1. Eligible homes", "h2"),
          P("The company writes owner-occupied one-family dwellings on the HO-3 and HO-5 forms. Two-family "
            "dwellings, townhouses, manufactured homes and homes held for rent are referred to the Underwriting "
            "Manager. The dwelling must be on public water."),
          P("2. Fire protection", "h2"),
          P("A home is <i>protected</i> when an in-service fire hydrant of the Tamswold County Water Authority stands "
            "within 1,000 feet of it, measured in a straight line from the parcel point on the county assessment "
            "roll, and the hydrant's most recent flow test shows at least 500 gallons per minute available at a "
            "residual pressure of 20 psi. Private hydrants do not count. Protection is read from the Authority's "
            "hydrant register and flow-test log as published at the date of the review. An unprotected home is "
            "written at the class 9 rate."),
          P("3. Rating plan groupings", "h2"),
          _table(S, [["Characteristic", "Groups"],
                     ["Year built (era)", "Before 1940; 1940 to 1969; 1970 to 1999; 2000 and later"],
                     ["Construction", "F frame; MV masonry veneer; M masonry or stone"],
                     ["Foundation", "B basement, full or partial; S slab on grade; C crawlspace or piers"],
                     ["Full bathrooms", "1; 2; 3; 4 or more"],
                     ["Stories", "1; 1.5; 2 or more"],
                     ["Deductible", "$500; $1,000; $2,500"]], [1.6, 4.9]),
          Spacer(1, 4),
          P("The county roll's foundation entries map to the company's codes as follows: BSMT FULL and BSMT PART "
            "to B, SLAB to S, CRAWL and PIERS to C. Its exterior walls map FRAME to F, BRICK VENEER to MV, and "
            "MASONRY and STONE to M.", "note"),
          P("4. Claims history", "h2"),
          P("Applicants with two or more non-weather water claims in the five years before the application are "
            "referred. A claim closed without payment counts.")]
    _build(path, st, K.ORG, "Underwriting Guide, Homeowners (2025)", "Underwriting Guide, Homeowners", K.ORG)


def brief(path):
    S = styles("Sans", BLUE)
    P = lambda t, s="body": Paragraph(t, S[s])   # noqa: E731
    towns = ", ".join(K.TOWN_FULL[t] for t in K.CANDIDATES[:-1]) + " or " + K.TOWN_FULL[K.CANDIDATES[-1]]
    st = [P(K.ORG, "meta"), P("2027 agency: the township", "h1"),
          P("To: %s, Underwriting Manager. From: %s, President. %s. For the Board of Directors' meeting of %s." % (
              K.REQUESTER, K.PRESIDENT, us_date(K.BRIEF_DATE), us_date(K.BOARD_DATE)), "meta"),
          P("The Board will open the company's first agency outside its four townships on %s, in %s. All three "
            "border our territory and none has been written by us." % (us_date(K.AGENCY_OPENS), towns)),
          P("Non-weather water cost the company its 2025 underwriting result. The agency opens in the township "
            "whose homes would bring the fewest non-weather water claims per house-year at our own 2023 to 2025 "
            "experience, the frequency taken as the Frequency Model Standard sets out for a territory we have not "
            "written. A township's homes are its owner-occupied single-family detached homes on the county's "
            "certified 2026 assessment roll: land use R-SFD with the homestead exclusion."),
          P("The paper should also give, for each township, how many of those homes the underwriting guide would "
            "class as protected and the total market value of those homes, read as the county's 2026 assessments "
            "imply it at the common level ratio in effect when the 2026 roll was certified on January 1, 2026; and "
            "for the book, the average non-weather water claim payment for each accident year from 2023 to 2025 "
            "(indemnity paid to date per claim with indemnity paid, net of recoveries) and the fire and lightning "
            "frequency over 2023 to 2025 for the homes the guide classes as unprotected, which the agency would write "
            "at the class 9 rate."),
          P("Please send the workbook and a chart of the three townships against the book a week before the "
            "meeting.")]
    _build(path, st, K.ORG, "Board paper request", "2027 agency: the township", K.PRESIDENT, face="Sans")


def master_plan(path):
    S = styles("Sans", BLUE)
    P = lambda t, s="body": Paragraph(t, S[s])   # noqa: E731
    rows = [["Zone", "Name", "Supply", "HGL (ft)", "Service elevations (ft)"]]
    for z in K.ZONES:
        rows.append([z[0], z[1], z[2], "{:,}".format(z[3]), "{:,} to {:,}".format(*z[4])])
    st = [P(K.AUTHORITY, "meta"), P("Water System Master Plan, 2019: excerpt", "h1"),
          P("Chapters 3 and 6. Prepared by the Authority's engineering department; engineer of record %s, P.E. "
            "Adopted by the Authority Board on %s." % (K.ENGINEER, us_date(K.MASTER_PLAN)), "meta"),
          P("3.2 Pressure zones", "h2"),
          P("The Authority serves its customers through four pressure zones. Zone boundaries follow the ground and "
            "the history of the system rather than municipal lines, and several townships are served from two or "
            "more zones. The table gives each zone's hydraulic grade line at average day demand and the range of "
            "ground elevations at its service connections."),
          _table(S, rows, [0.55, 0.85, 2.6, 0.8, 1.6], right=(3,)),
          Spacer(1, 4),
          P("The Valley zone is fed directly from the Ostrander Ridge Tank by the 1961 transmission main. Its "
            "pressure-reducing station, carried in the 2014 plan, is deferred to the capital program after 2030; "
            "until then new connections on the valley floor are served at the zone's existing grade.", "body"),
          P("3.4 Upper zone", "h2"),
          P("The Kilns Road booster station lifts water to the Upper Tank, which serves the slopes on both sides of "
            "the valley through the 1988 crossing main; the zone is one hydraulic zone with two service areas."),
          P("6.3 Hydrant flow testing", "h2"),
          P("Every public hydrant is flow tested on a five-year cycle and after work on the main that serves it. "
            "Tests follow NFPA 291: the static pressure is read at a residual hydrant, a flowing hydrant is "
            "opened, and the residual pressure and the flow are recorded. Results are kept as recorded at the "
            "test. Private hydrants on commercial sites are tested by their owners."),
          P("Ground elevations are from the county's 2015 LiDAR survey. Hydraulic grades are from the Authority's "
            "calibrated model (2018).", "note")]
    _build(path, st, K.AUTHORITY, "Water System Master Plan 2019, excerpt", "Water System Master Plan, 2019 (excerpt)",
           K.AUTHORITY, face="Sans")


def dictionary(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["file", "field", "description"])
        for r in rows:
            w.writerow(r)
    return len(rows)
