"""task239 documents: the company's survey measurement standard (pdf), and the dashboard methodology note and the
fieldwork close-out (docx)."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import postprocess

BOARD = "Lowfirth Parcels"
UNIT = "Workforce Insight"
SURVEY = "Staff Voice survey"
PEOPLE = {"head": "Carolyn Burrows", "methods": "George Haynes", "programme": "Laura Miles"}


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=8,
                        spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10.5, textColor=colors.HexColor("#444444"))
    return dict(body=body, h1=h1, h2=h2, small=small)


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(rows, widths, size=8.2):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", size), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA3A8")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3ECE8")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _p(text, style):
    return Paragraph(text, style)


# ------------------------------------------------------------------ the measurement standard (pdf)
def standard(path):
    S = _styles()
    b, h1, h2, sm = S["body"], S["h1"], S["h2"], S["small"]
    st = [_p("%s: measurement standard" % SURVEY, h1),
          _p("%s, %s. Standard WI-SV-03, 2027 edition, issued 3 May 2027; applies to the 2027 survey and its "
             "dashboard. Owner: %s, Head of Workforce Insight." % (BOARD, UNIT, PEOPLE["head"]), sm),
          Spacer(1, 4),
          _p("1. Purpose and scope", h2),
          _p("The %s asks every member of staff in post on the survey's census date about working for the company. "
             "This standard sets which returns count, how a return is placed in a team, how the Team Climate Index "
             "is checked each year, and which teams the dashboard reports. Other dashboard figures are made as the "
             "dashboard methodology note for the year sets out." % SURVEY, b),
          _p("2. The Team Climate Index", h2),
          _p("The index is reported for teams. It has the twelve items in Table 1, each answered on a five-point "
             "scale from strongly disagree to strongly agree, with don't know offered beside the scale. An answer on "
             "the scale is scored 1 (strongly disagree) to 5 (strongly agree), except that the two items worded "
             "negatively, TC04 and TC07, are scored the other way round, 5 for strongly disagree, so that a higher "
             "score is always the better climate.", b)]
    rows = [["Item", "Wording", "Worded"]]
    for code, wording, neg, *_ in P.ITEMS:
        rows.append([code, Paragraph(wording, ParagraphStyle("c", fontName="Helvetica", fontSize=8.2, leading=10)),
                     "negatively" if neg else "positively"])
    st += [_table(rows, [16 * mm, 128 * mm, 24 * mm]), _p("Table 1. Team Climate Index items, 2027.", sm),
           _p("3. Returns that count", h2),
           _p("3.1 An online return, whether made through a member's personal link or on a site tablet, counts when it "
              "was submitted by 23:59 on 4 October 2027. A session that was not submitted does not count.", b),
           _p("3.2 A paper form counts when %s scanned it by 8 October 2027 and it carries at least one answer." % UNIT, b),
           _p("3.3 Each return counts once, and each member's views count once: where the company received more than one "
              "return from the same member, the return received last counts and the others do not.", b),
           _p("3.4 A return's team is the team named on it: the team code loaded with the member's personal link, the "
              "team the respondent chose on a site tablet, or the team code printed on the member's paper pack. A code "
              "from a team structure that was replaced before the survey closed is read through the reorganisation map "
              "HR published with the change. A return whose code cannot be read to a single team of the structure in "
              "force on the census date, 1 September 2027, counts in the company's figures but in no team's.", b),
           _p("4. The annual structure check", h2),
           _p("4.1 Because the index reports teams, the structure check examines the twelve items at team level. A "
              "team's level on an item is a property of the team itself: the score a member of the team is expected "
              "to give, which stays the same as staff come and go.", b),
           _p("4.2 The check fits a single common factor to the twelve items' team levels across the teams in 4.4. An "
              "item's team-level loading is its loading on that factor when each item's team level is standardised "
              "across those teams.", b),
           _p("4.3 An item whose team-level loading is 0.75 or more stays in the index for the next survey. An item "
              "below 0.75 is withdrawn, and %s proposes a replacement from the item bank for the survey after." % UNIT, b),
           _p("4.4 The check uses the returns that count under section 3 from the teams reported under section 5, "
              "taking each return that gives all twelve items an answer on the scale. Don't know is not an answer on "
              "the scale.", b),
           _p("5. Reporting", h2),
           _p("5.1 A team is reported on the dashboard when it holds five or more returns that count.", b),
           _p("6. Review", h2),
           _p("%s reviews this standard after each survey. The next review is due in May 2028." % UNIT, b)]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="Staff Voice survey measurement standard",
                            author=PEOPLE["head"], creator=UNIT, invariant=1)
    foot = "%s | %s | WI-SV-03 (2027 edition)" % (BOARD, UNIT)
    doc.build(st, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    postprocess.scrub(path, UNIT, "2027-05-03")


# ------------------------------------------------------------------ docx helpers
def _docx(title_line, meta, paras, path, author, created, modified, title, sign=None, table=None):
    import docx
    from docx.shared import Pt
    doc = docx.Document()
    stl = doc.styles["Normal"]
    stl.font.name = "Calibri"
    stl.font.size = Pt(10.5)
    head = doc.add_paragraph()
    r = head.add_run(title_line)
    r.bold = True
    r.font.size = Pt(12)
    for k, v in meta:
        p = doc.add_paragraph()
        a = p.add_run(k + ": ")
        a.bold = True
        p.add_run(v)
        p.paragraph_format.space_after = Pt(0)
    doc.add_paragraph()
    for t in paras:
        if isinstance(t, tuple):
            p = doc.add_paragraph()
            a = p.add_run(t[0])
            a.bold = True
            p.add_run(" " + t[1])
        else:
            p = doc.add_paragraph(t)
        p.paragraph_format.space_after = Pt(6)
    if table:
        tb = doc.add_table(rows=len(table), cols=len(table[0]))
        tb.style = "Light Grid Accent 1"
        for i, row in enumerate(table):
            for j, v in enumerate(row):
                tb.cell(i, j).text = str(v)
    if sign:
        p = doc.add_paragraph(sign)
        p.paragraph_format.space_before = Pt(8)
    doc.core_properties.author = author
    doc.core_properties.title = title
    doc.save(path)
    postprocess.scrub(path, author, created[:10])
    postprocess.finish_office(path, created, modified, BOARD)


def dashboard_note(path):
    paras = [
        ("Returns.", "The dashboard uses the returns that count under section 3 of the measurement standard "
                     "(WI-SV-03)."),
        ("Percent favourable.", "For an item, the percentage of answers on the five-point scale that are favourable: "
                                "agree or strongly agree, or, for TC04 and TC07, which are worded negatively, disagree or "
                                "strongly disagree. Don't know answers and items left unanswered are not in the base. A "
                                "figure for the company as a whole uses every return that counts, including returns whose "
                                "team is not reported and returns that leave some items unanswered."),
        ("Team pages.", "A team's page appears when the team is reported under section 5 of the standard. The page "
                        "lists the twelve items with the team's percent favourable on each, from the team's lowest "
                        "figure to its highest (items with the same figure in the order of Table 1 of the standard), "
                        "and shows the team's index score, the mean of its twelve percentages. A team's figures use all "
                        "of the team's returns that count."),
        ("Development plans.", "From 1 November each team leader can choose up to three items on the team's page as "
                               "the team's development targets for the year. The dashboard holds a plan from the "
                               "leader's first save: it is a draft until the leader sends it to their manager, with the "
                               "manager until the manager agrees it, and agreed once they have. A team has one plan: "
                               "when the leader saves it again, the new version replaces the earlier one."),
        ("Divisions.", "Each team is shown under the division it belonged to on the census date, 1 September 2027. A "
                       "move between divisions after the census date shows from the next survey."),
        ("Rounding.", "Percentages are shown to one decimal place."),
        ("Publication.", "The 2027 dashboard went live for team leaders on 1 November 2027."),
    ]
    _docx("%s | %s | 2027 dashboard" % (BOARD, UNIT),
          [("Title", "How the 2027 dashboard figures are made"), ("Author", "%s, Survey Methods Analyst" % PEOPLE["methods"]),
           ("Date", "28 October 2027")],
          paras, path, PEOPLE["methods"], "2027-10-27T14:20:00Z", "2027-10-28T09:05:00Z",
          "How the 2027 dashboard figures are made")


def close_out(path, f):
    paras = [
        "The 2027 Staff Voice survey ran from Monday 6 September to 23:59 on Monday 4 October, with paper forms taken "
        "in until Friday 8 October. Thank you to every team that made time for it.",
        ("Channels.", "Staff with a company email account got their personal link by email on the morning of 6 September. "
                      "Paper packs, each with the member's own cover letter and form, went out from 23 to 25 August to "
                      "staff without a company account and to the teams whose managers asked for paper. Site tablets were "
                      "set up at six sites in the second half of August for staff who prefer to answer at work without a "
                      "link; we ran tablet drives on the hub floors and in the depots in the first week."),
        ("Reminders.", "Email reminders went on 20 and 29 September to staff who had not yet submitted online."),
        ("Paper.", "Forms came back by internal mail and freepost and were scanned in %s on the day they arrived. A "
                   "few dozen arrived after 8 October; they were scanned all the same, but they are after "
                   "the deadline." % UNIT),
        ("Returns.", "About %s returns came in across the three channels, about %s per cent of staff in post, a little "
                     "up on 2026. The tablets were collected on 5 October." % (f["approx_returns"], f["approx_rate"])),
        ("Next.", "The dashboard is due to go live on 1 November. The structure check on the Team Climate Index follows, "
                  "in time for the 2028 questionnaire to go to the executive team in January."),
    ]
    _docx("%s | %s | Staff Voice 2027" % (BOARD, UNIT),
          [("To", "%s, Head of Workforce Insight" % PEOPLE["head"]),
           ("From", "%s, Staff Voice Programme Manager" % PEOPLE["programme"]), ("Date", "12 October 2027"),
           ("Subject", "Staff Voice 2027: fieldwork close-out")],
          paras, path, PEOPLE["programme"], "2027-10-11T15:40:00Z", "2027-10-12T08:55:00Z",
          "Staff Voice 2027 fieldwork close-out", sign=PEOPLE["programme"])
