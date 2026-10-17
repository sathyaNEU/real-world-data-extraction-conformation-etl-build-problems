"""The pack's documents: the contractor's fieldwork and weighting note, the Authority's levy papers for the January
2027 budget meeting (with the members' resolution of 9 July 2026), the survey codebook, the settlement gazetteer and
the export manifest."""
from __future__ import annotations

import csv

from reportlab import rl_config

rl_config.invariant = 1
from openpyxl import Workbook                                                       # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill                            # noqa: E402
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import mm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K   # noqa: E402
import world as W    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1d2326"), colors.HexColor("#5b646b"), colors.HexColor("#b7bec4")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=9.7, leading=13.6, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=14, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.4, leading=14, textColor=INK, spaceBefore=7,
                          spaceAfter=2),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.3, leading=11.2, textColor=GREY, spaceAfter=9),
        note=ParagraphStyle("n", fontName=font, fontSize=7.9, leading=10.4, textColor=GREY, spaceBefore=5),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.5, leading=10.8, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.5, leading=10.8, textColor=INK),
        para=ParagraphStyle("p", parent=body, leftIndent=14, firstLineIndent=-14))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.4)
        canvas.drawString(20 * mm, A4[1] - 11.5 * mm, left)
        canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 11.5 * mm, right)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=(), head=True):
    data = [[Paragraph(str(c), S["cellb"] if (head and i == 0) else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1 if head else 0)
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def fmt_day(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


# ---------------------------------------------------------------------------------------------- fieldwork note
def write_fieldnote(path, recs, m):
    S = styles("Sans", colors.HexColor("#2f5d50"))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm,
                            bottomMargin=17 * mm, title="Visitor survey 2025-26: fieldwork and weighting note",
                            author=K.CONTRACTOR, subject="", creator="", producer="")
    n1 = sum(1 for o in recs if o["wave"] == 1)
    n2 = len(recs) - n1
    approached = int(round(len(recs) / .68 / 10.0)) * 10
    st = []
    st.append(Paragraph("Daskbeck Valley Regional Park Authority visitor survey 2025-26", S["h1"]))
    st.append(Paragraph("Fieldwork and weighting note. %s for the Authority's parks and finance teams. Project "
                        "manager %s. Issued with the wave 2 delivery, 9 April 2026." % (K.CONTRACTOR, K.PEOPLE["contractor"]),
                        S["meta"]))
    st.append(Paragraph("1. What the survey covers", S["h2"]))
    st.append(Paragraph("The survey interviews adults aged 16 and over as they leave the Authority's six parks: "
                        "Brathden Woods, Crowside Common, Gorthfield Country Park, Daskbeck Water Park, Lockshaw Moor "
                        "and Thruscote Hall. Fieldwork ran from 1 April 2025 to 31 March 2026 and was delivered in two "
                        "waves: wave 1 (April to September 2025, %d interviews, delivered 14 October 2025) and wave 2 "
                        "(October 2025 to March 2026, %d interviews, delivered 9 April 2026)." % (n1, n2), S["body"]))
    st.append(Paragraph("2. How interviews were drawn", S["h2"]))
    st.append(Paragraph("Each park's year was divided into strata by season (spring April to June, summer July to "
                        "September, autumn October to December, winter January to March) and day type (weekdays; "
                        "weekends and bank holidays together), 48 strata in all. Survey days were drawn at random within "
                        "each stratum: four weekdays and three weekend or bank holiday days a season at each park, with "
                        "a fourth weekend day in the summer.", S["body"]))
    st.append(Paragraph("On a survey day one interviewer worked the park's main exit from 09:30 to 16:45. The "
                        "interviewer counted the adults leaving across the survey line and approached every eighth, "
                        "restarting the count after each interview or refusal; adults in a group were each eligible, and "
                        "an adult who took part answered for themselves only. About %s adults were approached and 68 per "
                        "cent took part. When the exit was busy the interviewer completed as many interviews as the shift "
                        "allowed." % "{:,}".format(approached), S["body"]))
    st.append(Paragraph("3. The questions used by the Authority", S["h2"]))
    qs = [["No.", "Question", "Field (wave 1 / wave 2)"],
          ["Q1", "Where do you live? (town or village; postcode if offered)", "Home town/village / home_place"],
          ["Q2", "Age", "Age group / age_band"],
          ["Q4", "How many adults and children are with you today?", "Adults in party, Children in party / n_adults, n_children"],
          ["Q6", "How did you travel here today?", "Arrived by / mode"],
          ["Q7", "What was the main thing you came to do?", "Main activity / activity"],
          ["Q9", "Including today, about how many times in the last 12 months have you visited any of the "
                 "Authority's six parks? (interviewers ask for a best estimate as a number)",
           "Visits to Authority parks, last 12 months (incl. today) / q9_visits_12m"],
          ["Q14", "Overall, how would you rate your visit today, from 1 (very poor) to 5 (excellent)?",
           "Overall rating (1-5) / q14_rating"]]
    st.append(_table(S, qs, [12, 104, 54]))
    st.append(Paragraph("Home area is coded by %s from the answer to Q1 using the Authority's settlement gazetteer: the "
                        "code of the member council the home lies in, OUT for a home outside the nine member councils, "
                        "NK where no home was given or it could not be placed. Wave 2 uses the shorter age bands of the "
                        "Authority's 2026 questionnaire standard." % K.CONTRACTOR, S["body"]))
    st.append(Paragraph("4. Weighting", S["h2"]))
    tot = sum(e for _, e in set((o["stratum"], o["stratum_est"]) for o in recs))
    st.append(Paragraph("Each interview carries a weight: the estimated number of adult visits to its park in its "
                        "stratum, divided by the number of interviews completed in that stratum. Adult visits by stratum "
                        "are estimated from the Authority's car-park counters and path counters, with vehicle occupancy "
                        "from the interviewers' tallies at each exit, and are rounded to the nearest ten. The weights "
                        "expand the %s interviews to the %s adult visits estimated for the year. They are supplied in "
                        "survey_weights_2025-26.csv, keyed by wave and interview number, and are the weights to use "
                        "with this survey." % ("{:,}".format(len(recs)), "{:,}".format(tot)), S["body"]))
    rows = [["Park", "Survey days", "Interviews", "Adult visits (estimated)"]]
    for pk in K.PARK_CODES:
        mine = [o for o in recs if o["park"] == pk]
        est = sum(e for _, e in set((o["stratum"], o["stratum_est"]) for o in mine))
        rows.append([K.PARK_NAME[pk], str(len({o["date"] for o in mine})), "{:,}".format(len(mine)), "{:,}".format(est)])
    st.append(_table(S, rows, [64, 26, 26, 40], right=(1, 2, 3)))
    st.append(Paragraph("5. Delivery notes", S["h2"]))
    st.append(Paragraph("Wave 1 is a workbook with one row per interview, interview numbers DV25-1-0001 onwards; "
                        "wave 2 is a CSV export from the new tablet system, interview numbers DV25/2/0001 onwards, with "
                        "parks as site codes (BW, CC, GF, DW, LM, TH). The weights file numbers interviews by wave and "
                        "serial (1-0001, 2-0001). Field names and codes are in the codebook.", S["body"]))
    doc.build(st, onFirstPage=_frame(K.CONTRACTOR, "Visitor survey 2025-26", "Sans"),
              onLaterPages=_frame(K.CONTRACTOR, "Visitor survey 2025-26", "Sans"))


# ---------------------------------------------------------------------------------------------- levy papers
BUDGET = [("Park operations and maintenance", 4816400), ("Visitor services and education", 1611900),
          ("Conservation and woodland management", 1208300), ("Car parks and access", 1027200),
          ("Central services and governance", 1173400), ("Capital financing", 512700)]
INCOME = [("Car parking charges", -1902600), ("Annual permits", -134200), ("Events and venue hire", -297800),
          ("Concessions and rents", -96500), ("Grants", -258000)]
RESERVES = -244500


def write_levypapers(path):
    S = styles("Serif", colors.HexColor("#3c3a6e"))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=21 * mm, rightMargin=21 * mm, topMargin=21 * mm,
                            bottomMargin=18 * mm, title="Item 7: Levy 2027-28", author=K.AUTH, subject="", creator="",
                            producer="")
    gross = sum(v for _, v in BUDGET)
    inc = sum(v for _, v in INCOME)
    req = gross + inc + RESERVES
    assert req == K.LEVY_2027, req
    st = []
    st.append(Paragraph("%s" % K.AUTH, S["meta"]))
    st.append(Paragraph("Item 7: Levy 2027-28", S["h1"]))
    st.append(Paragraph("Meeting of the Authority, 21 January 2027. Report of the Head of Finance (%s). For decision."
                        % K.PEOPLE["finance"], S["meta"]))
    st.append(Paragraph("1. Purpose", S["h2"]))
    st.append(Paragraph("To set the levy on the member councils for 2027-28 and to apportion it among them. This is "
                        "the first levy apportioned under the members' resolution 14/2026; the levy for 2026-27 and "
                        "earlier years was apportioned by population under resolution 6/1998.", S["body"]))
    st.append(Paragraph("2. The levy requirement", S["h2"]))
    rows = [["", "2027-28 (GBP)"]]
    for k, v in BUDGET:
        rows.append([k, "{:,}".format(v)])
    rows.append(["Gross expenditure", "{:,}".format(gross)])
    for k, v in INCOME:
        rows.append([k, "({:,})".format(-v)])
    rows.append(["Contribution from reserves", "({:,})".format(-RESERVES)])
    rows.append(["Levy requirement", "{:,}".format(req)])
    st.append(_table(S, rows, [110, 40], right=(1,)))
    st.append(Paragraph("The levy requirement for 2027-28 is %s pounds, 3.1 per cent more than the %s pounds levied for "
                        "2026-27." % ("{:,}".format(req), "{:,}".format(K.LEVY_2026)), S["body"]))
    st.append(Paragraph("3. Apportionment", S["h2"]))
    st.append(Paragraph("Members agreed on 9 July 2026 that from 2027-28 the levy should follow the use the member "
                        "councils' residents make of the parks, measured by the Authority's visitor survey, rather than "
                        "the councils' populations. The resolution is set out in Appendix A. The 2025-26 survey year is "
                        "the first to which it applies; the survey's fieldwork and weighting note and its data are with "
                        "these papers. Appendix B shows the 2026-27 levy as apportioned by population, for reference.",
                        S["body"]))
    st.append(Paragraph("4. Timetable", S["h2"]))
    st.append(Paragraph("The levy and its apportionment are to be approved at this meeting and notified to the member "
                        "councils by 15 February 2027. The 2027-28 levy is payable in four instalments, the first due on "
                        "15 April 2027 and the last on 31 March 2028.", S["body"]))
    st.append(Paragraph("Appendix A. Resolution 14/2026 (adopted 9 July 2026)", S["h2"]))
    paras = ["1. From 2027-28 the Authority's levy is apportioned among the member councils in proportion to the "
             "number of each council's residents who visited the Authority's parks.",
             "2. A council's number is the number of its residents aged 16 and over who visited at least one of the "
             "Authority's six parks at least once during the survey year, each resident counted once however many "
             "times they visited and however many of the parks they visited, and whether or not the visitor survey met "
             "them, as estimated from the Authority's visitor survey for that year.",
             "3. For the 2027-28 levy the survey year is 1 April 2025 to 31 March 2026.",
             "4. A respondent's council is the member council in which the home they give to the survey lies. "
             "Respondents whose home cannot be placed are not counted for any council.",
             "5. Each council's levy is the levy requirement multiplied by its number and divided by the nine "
             "councils' numbers added together, rounded to the nearest pound.",
             "6. Visitors whose homes lie outside the member councils are not counted."]
    for p in paras:
        st.append(Paragraph(p, S["para"]))
    old = W.apportion(K.LEVY_2026, {c: W.POP[c][1] for c in K.CODES})
    rows = [["Member council", "Population, mid-2024", "Levy 2026-27 (GBP)"]]
    for c in K.CODES:
        rows.append([K.NAME[c], "{:,}".format(W.POP[c][1]), "{:,}".format(old[c])])
    rows.append(["Total", "{:,}".format(sum(W.POP[c][1] for c in K.CODES)), "{:,}".format(sum(old.values()))])
    st.append(KeepTogether([Paragraph("Appendix B. Levy 2026-27, apportioned by population (resolution 6/1998)",
                                      S["h2"]), _table(S, rows, [76, 38, 40], right=(1, 2))]))
    doc.build(st, onFirstPage=_frame("Item 7: Levy 2027-28", "Meeting of 21 January 2027", "Serif"),
              onLaterPages=_frame("Item 7: Levy 2027-28", "Meeting of 21 January 2027", "Serif"))
    return req


# ---------------------------------------------------------------------------------------------- codebook
def _head(ws, header, widths):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2F5D50")
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    ws.freeze_panes = "A2"


def write_codebook(path):
    import records as R
    wb = Workbook()
    ws = wb.active
    ws.title = "Wave 1 fields"
    _head(ws, ["Column", "Question", "Values"], [44, 18, 70])
    for row in [("Interview No", "", "DV25-1- and a four-digit serial"), ("Park", "", "Park name"),
                ("Interview date", "", "Date of interview"), ("Start", "", "Interview start, local time"),
                ("Interviewer", "", "Interviewer code"), ("Home town/village", "Q1", "As given by the respondent"),
                ("Home area", "Q1 (coded)", "Area code, see Codes"), ("Age group", "Q2", ", ".join(R.AGE1)),
                ("Sex", "Q3", "Female, Male, Prefer not to say"), ("Adults in party", "Q4", "Number of adults in the group"),
                ("Children in party", "Q4", "Number of children in the group"), ("Dog with party", "Q5", "Yes, No"),
                ("Arrived by", "Q6", ", ".join(R.MODES)), ("Main activity", "Q7", "See Codes"),
                ("Visits to Authority parks, last 12 months (incl. today)", "Q9", "Number of visits to any of the six parks"),
                ("Overall rating (1-5)", "Q14", "1 very poor to 5 excellent")]:
        ws.append([x or None for x in row])
    ws = wb.create_sheet("Wave 2 fields")
    _head(ws, ["Field", "Question", "Values"], [20, 14, 70])
    for row in [("case_ref", "", "DV25/2/ and a four-digit serial"), ("site_code", "", "Park code, see Codes"),
                ("int_date", "", "Date of interview, DD/MM/YYYY"), ("int_time", "", "Interview start, local time"),
                ("int_id", "", "Interviewer code"), ("home_place", "Q1", "As given by the respondent"),
                ("home_area_code", "Q1 (coded)", "Area code, see Codes"), ("age_band", "Q2", ", ".join(R.AGE2)),
                ("gender", "Q3", "F, M, X (prefer not to say)"), ("n_adults", "Q4", "Number of adults in the group"),
                ("n_children", "Q4", "Number of children in the group"), ("dog", "Q5", "Y, N"),
                ("mode", "Q6", "CAR, ON, BICYCLE, BUS, MOTORCYCLE, OTHER"), ("activity", "Q7", "Upper case, see Codes"),
                ("q9_visits_12m", "Q9", "Number of visits to any of the six parks"),
                ("q14_rating", "Q14", "1 very poor to 5 excellent")]:
        ws.append([x or None for x in row])
    ws = wb.create_sheet("Codes")
    _head(ws, ["List", "Code", "Meaning"], [16, 12, 60])
    for c in K.CODES:
        ws.append(["Home area", c, K.NAME[c]])
    ws.append(["Home area", "OUT", "Lives outside the nine member councils"])
    ws.append(["Home area", "NK", "Not known: no home given, or it could not be placed"])
    for p in K.PARK_CODES:
        ws.append(["Park", p, K.PARK_NAME[p]])
    for a in R.ACTIVITIES:
        ws.append(["Main activity", a.upper().replace(" ", "_"), a])
    wb.save(path)


def write_gazetteer(path):
    parish = {"KDM": "Keldmere", "RVW": "Ravenwick", "SNG": "Snelgarth", "LKS": "Larkstead", "GRB": "Grinbury",
              "HNM": "Hornmere", "CHD": "Chaldale", "WDS": "Wendstow", "FNC": "Ferncote"}
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["settlement", "type", "parish", "area_code", "council"])
        rows = []
        for c in K.CODES:
            for i, s in enumerate(K.SETTLEMENTS[c]):
                rows.append((s, "Town" if i == 0 else "Village", s if i else parish[c], c, K.NAME[c]))
        for r in sorted(rows):
            w.writerow(r)
    return sum(len(v) for v in K.SETTLEMENTS.values())


def write_manifest(path, entries):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "what it is", "source", "prepared", "rows or pages"])
        for e in entries:
            w.writerow(e)
