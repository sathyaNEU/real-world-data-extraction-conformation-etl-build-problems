"""The pack's documents: the mining authority's traffic-light scheme (2024), the 2026 monitoring ordinance, the
survey's traffic-light bulletin for the third quarter of 2026, the authority's summary of the 2027 operating plans,
and the data office's extract notes."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.pagesizes import A4                                     # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import mm                                         # noqa: E402
from reportlab.pdfbase import pdfmetrics                                   # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                               # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import records as R    # noqa: E402
import world as W      # noqa: E402

SCHEME = "tls_scheme_2024.pdf"
ORDINANCE = "monitoring_ordinance_2026.pdf"
BULLETIN = "tls_bulletin_2026Q3.pdf"
PLANS = "operating_plans_2027.pdf"
NOTES = "datenabgabe_ampel_2026-10-12.md"

PEOPLE = {"lead": "Gundula Atzler", "analyst": "Arndt Ernst", "field": "Eugen Scheel", "data": "Amalie Mende"}

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LiberationSans", FONT_DIR + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans-Bold", FONT_DIR + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSerif", FONT_DIR + "LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSerif-Bold", FONT_DIR + "LiberationSerif-Bold.ttf"))
SANS, SANS_B, SERIF, SERIF_B = "LiberationSans", "LiberationSans-Bold", "LiberationSerif", "LiberationSerif-Bold"
INK = colors.HexColor("#1b1f24")
GREY = colors.HexColor("#5c636a")
RULE = colors.HexColor("#a3abb3")

# the authority's house style: serif, numbered paragraphs
A_BODY = ParagraphStyle("abody", fontName=SERIF, fontSize=10.4, leading=14, textColor=INK, spaceAfter=5)
A_PARA = ParagraphStyle("apara", parent=A_BODY, leftIndent=30, firstLineIndent=-30)
A_H1 = ParagraphStyle("ah1", fontName=SERIF_B, fontSize=14, leading=18, textColor=INK, spaceAfter=3)
A_H2 = ParagraphStyle("ah2", fontName=SERIF_B, fontSize=10.8, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3)
A_META = ParagraphStyle("ameta", fontName=SERIF, fontSize=8.8, leading=11.5, textColor=GREY, spaceAfter=9)
# the survey's: sans
S_BODY = ParagraphStyle("sbody", fontName=SANS, fontSize=9.4, leading=12.8, textColor=INK, spaceAfter=5)
S_H1 = ParagraphStyle("sh1", fontName=SANS_B, fontSize=14, leading=17.5, textColor=INK, spaceAfter=2)
S_H2 = ParagraphStyle("sh2", fontName=SANS_B, fontSize=10, leading=13.5, textColor=INK, spaceBefore=8, spaceAfter=3)
S_META = ParagraphStyle("smeta", fontName=SANS, fontSize=8, leading=10.5, textColor=GREY, spaceAfter=7)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=8.6, leading=10.4, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName=SANS_B)
A_CELL = ParagraphStyle("acell", fontName=SERIF, fontSize=9.4, leading=11.6, textColor=INK)
A_CELLB = ParagraphStyle("acellb", parent=A_CELL, fontName=SERIF_B)


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                             bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")


def _frame(top_left, top_right, foot):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(SERIF, 8)
        if top_left:
            canvas.drawString(22 * mm, A4[1] - 12 * mm, top_left)
            canvas.drawRightString(A4[0] - 22 * mm, A4[1] - 12 * mm, top_right)
        canvas.setFont(SANS, 7.4)
        canvas.drawString(22 * mm, 11 * mm, foot)
        canvas.drawRightString(A4[0] - 22 * mm, 11 * mm, "%d" % doc.page)
        canvas.restoreState()
    return draw


def _grid(rows, widths, style_head=CELLB, style=CELL, align_from=1, box=False):
    data = [[Paragraph(str(c), style_head if i == 0 else style) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    cmds = [("ALIGN", (align_from, 0), (-1, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]
    if box:
        cmds += [("BOX", (0, 0), (-1, -1), 0.6, INK), ("INNERGRID", (0, 0), (-1, -1), 0.3, RULE),
                 ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eceef0"))]
    else:
        cmds += [("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, -1), (-1, -1), 0.5, RULE)]
    t.setStyle(TableStyle(cmds))
    return t


# ------------------------------------------------------------------------------------------------- the scheme
SCHEME_PARAS = [
    ("1", "Scope", [
        ("1.1", "This scheme applies to every deep geothermal plant in the district of %s that reinjects produced "
                "thermal water into the Upper Jurassic carbonate reservoir. It forms part of each plant's main operating "
                "plan approval." % W.AUTHORITY),
        ("1.2", "The seismological monitoring of the plants is carried out by the %s (%s), Seismologischer Dienst, on "
                "behalf of the operators under the monitoring agreement of 2019." % (W.SURVEY, W.SURVEY_SHORT)),
    ]),
    ("2", "Monitoring zone", [
        ("2.1", "The monitoring zone of a plant is the area within 5 km epicentral distance of the open-hole section of "
                "any of its injection wells, as surveyed and entered in the well register."),
    ]),
    ("3", "What is counted", [
        ("3.1", "For each plant and calendar quarter the %s counts the earthquakes with an epicentre in the monitoring "
                "zone and a local magnitude ML of 1.0 or more. Quarters are calendar quarters in local time." % W.SURVEY_SHORT),
        ("3.2", "Locations, magnitudes and event types are those of the %s's reviewed catalogue. Events the review "
                "classes as explosions are not earthquakes." % W.SURVEY_SHORT),
    ]),
    ("4", "Traffic-light levels", [
        ("4.1", "Green: normal operation."),
        ("4.2", "Amber: more than 120 earthquakes counted under section 3 in a calendar quarter. The operator reduces the "
                "injection rate of the plant by at least a quarter within 48 hours of the notice and submits an "
                "assessment to the authority within four weeks. Amber is lifted when a following quarter's count is 120 "
                "or fewer."),
        ("4.3", "Red: a peak ground velocity of 5 mm/s or more at any station of the plant's network from an earthquake "
                "in the monitoring zone. Injection stops until the authority permits a restart."),
    ]),
    ("5", "The networks", [
        ("5.1", "Each plant's network has at least four stations within 6 km of its injection wells. The counts of a "
                "quarter are valid while at least four stations of the plant's network are recording; the %s reports "
                "the hours of each quarter in which fewer than four were recording." % W.SURVEY_SHORT),
        ("5.2", "A station is recording while its vertical channel delivers data to the %s's archive." % W.SURVEY_SHORT),
    ]),
    ("6", "Injection data", [
        ("6.1", "The operator transmits every hour, for each injection well, the mean injection rate, wellhead pressure "
                "and injection temperature of the hour to the %s." % W.SURVEY_SHORT),
        ("6.2", "The operator reports to the authority each month, for each well, the volume injected or produced in "
                "that month as metered at the wellhead. Under this scheme the injected volume of a plant is the sum of "
                "these reported volumes over its injection wells."),
    ]),
    ("7", "Reporting", [
        ("7.1", "The %s publishes a traffic-light bulletin after each quarter with each plant's count under section 3 "
                "and its traffic-light level." % W.SURVEY_SHORT),
        ("7.2", "With each plant's operating plan for the coming year the %s submits an annex giving, for each quarter "
                "of the current year to date, the plant's injected volume, the earthquakes its automatic system located "
                "with ML 1.0 or more in the monitoring zone (each at the system's final automatic solution), and the "
                "hours its network had fewer than four stations recording, together with its outlook for the coming "
                "year." % W.SURVEY_SHORT),
    ]),
]


def write_scheme(path):
    doc = _doc(path, "Ampelsystem Tiefe Geothermie", W.AUTHORITY)
    story = [Paragraph("%s" % W.AUTHORITY, A_META),
             Paragraph("Traffic-light scheme for induced seismicity at deep geothermal plants", A_H1),
             Paragraph("Ampelsystem Tiefe Geothermie. Reference BBS-GT-AMP-2024. Issued 12 February 2024, in force from "
                       "1 April 2024 for all plants in operation; replaces the plant-specific reaction schemes of the "
                       "approvals of 2014 to 2019.", A_META)]
    for no, head, paras in SCHEME_PARAS:
        story.append(Paragraph("%s&nbsp;&nbsp;%s" % (no, head), A_H2))
        for pno, text in paras:
            story.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (pno, text), A_PARA))
    story += [Spacer(1, 6), Paragraph("Annex: plants under the scheme on 1 April 2024", A_H2),
              _grid([["Plant", "Operator", "Injection wells"]] +
                    [[W.NAME[p], W.OPERATOR[p], {"MOS": "MST-GT2, MST-GT4"}.get(p, "%s-GT2" % p)] for p in W.PLANTS],
                    [34 * mm, 78 * mm, 40 * mm], A_CELLB, A_CELL, align_from=3, box=True)]
    frame = _frame("%s  |  BBS-GT-AMP-2024" % W.AUTHORITY, "Ampelsystem Tiefe Geothermie", "Bekanntgemacht im Amtsblatt der Bergbehörde, Heft 3/2024")
    doc.build(story, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------- the ordinance
ORD_PARAS = [
    ("§ 1", "Scope", "This ordinance applies to the seismological monitoring of deep geothermal projects that reinject "
                     "thermal water, and to the networks used for the traffic-light schemes of the mining authorities."),
    ("§ 2", "Borehole stations", "(1) From 1 January 2027 each monitoring network includes at least three borehole "
                                 "stations with the sensor at a depth of 150 m or more below ground, each within 5 km of "
                                 "the open-hole section of an injection well. (2) Surface stations may remain part of the "
                                 "network."),
    ("§ 3", "Design completeness", "(1) The network is designed so that it locates every earthquake of local magnitude "
                                   "0.6 or more with an epicentre within 5 km of the open-hole section of an injection "
                                   "well. (2) The body operating the network shows the design to the mining authority "
                                   "before the network is used for counts under § 4."),
    ("§ 4", "Counts", "From 1 January 2027 the counts of a traffic-light scheme are made on the network under § 2. "
                      "Counting rules, zones and thresholds are those of the scheme in force."),
    ("§ 5", "Data", "The body operating the network keeps the continuous data of every station for at least ten years "
                    "and makes them available to the mining authority on request."),
    ("§ 6", "Entry into force", "This ordinance enters into force on 1 April 2026; § 2 and § 4 apply from 1 January 2027."),
]


def write_ordinance(path):
    doc = _doc(path, "Verordnung über die seismische Überwachung tiefer Geothermievorhaben", "Staatsministerium")
    story = [Paragraph("Ordinance on the seismological monitoring of deep geothermal projects", A_H1),
             Paragraph("Verordnung über die seismische Überwachung tiefer Geothermievorhaben (SeisÜV) of 17 March 2026. "
                       "Issued by the state ministry for economic affairs and energy; published in the law and ordinance "
                       "gazette of 27 March 2026. Unofficial English text prepared by the %s for its monitoring partners."
                       % W.SURVEY_SHORT, A_META)]
    for no, head, text in ORD_PARAS:
        story.append(Paragraph("%s&nbsp;&nbsp;%s" % (no, head), A_H2))
        story.append(Paragraph(text, A_BODY))
    frame = _frame("SeisÜV 2026", "Unofficial translation", "Only the German text published in the gazette is authentic.")
    doc.build(story, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------- the bulletin
def write_bulletin(path, counts, largest):
    """counts: {plant: {(year, q): n}} for 2025 Q4 to 2026 Q3; largest: {plant: ML} in 2026 Q3."""
    doc = _doc(path, "Ampelbericht 3. Quartal 2026", PEOPLE["lead"])
    qs = [(2025, 4), (2026, 1), (2026, 2), (2026, 3)]
    rows = [["Plant", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026", "Largest ML, Q3 2026", "Level"]]
    for p in W.PLANTS:
        rows.append([W.NAME[p]] + [str(counts[p][k]) for k in qs] + ["%.1f" % largest[p], "green"])
    story = [Paragraph("%s, Seismologischer Dienst" % W.SURVEY, S_META),
             Paragraph("Traffic-light bulletin, third quarter 2026", S_H1),
             Paragraph("Ampelbericht Tiefe Geothermie. %s-SD-AB-2026-03, 9 October 2026. To the %s, Referat Geothermie, "
                       "and the plant operators." % (W.SURVEY_SHORT, W.AUTHORITY), S_META),
             Paragraph("All five plants stayed green in the third quarter of 2026. No earthquake reached a peak ground "
                       "velocity of 1 mm/s at any station.", S_BODY),
             Paragraph("Earthquakes counted under section 3 of the scheme", S_H2),
             _grid(rows, [30 * mm, 17 * mm, 17 * mm, 17 * mm, 17 * mm, 30 * mm, 14 * mm], align_from=1),
             Paragraph("Earthquakes of ML 1.0 or more with an epicentre within 5 km of the open-hole section of an "
                       "injection well, by calendar quarter in local time, from the reviewed catalogue as at 8 October "
                       "2026. Amber is more than 120 in a quarter.", S_META),
             Paragraph("Networks", S_H2),
             Paragraph("From 1 January 2027 the counts are made on the networks the 2026 ordinance requires; the "
                       "borehole stations are being drilled and fitted this autumn at all five plants.", S_BODY),
             Paragraph("Contact: %s, induced seismicity" % PEOPLE["lead"], S_META)]
    frame = _frame("", "", "%s  |  Seismologischer Dienst  |  %s-SD-AB-2026-03" % (W.SURVEY, W.SURVEY_SHORT))
    doc.build(story, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------- the 2027 plans
REVISION_2027 = {"MOS": "2 to 13 August", "PFB": "12 to 25 July", "LZR": "16 to 25 August", "WDR": "5 to 16 July",
                 "OTM": "9 to 21 August"}
FILED = {"MOS": "8 September 2026", "PFB": "1 September 2026", "LZR": "11 September 2026", "WDR": "29 August 2026",
         "OTM": "15 September 2026"}


def write_plans(path):
    doc = _doc(path, "Hauptbetriebspläne 2027", W.AUTHORITY)
    story = [Paragraph("%s, Referat Geothermie" % W.AUTHORITY, A_META),
             Paragraph("Operating plans 2027: summary for the seismological service", A_H1),
             Paragraph("Note of 24 September 2026 on the main operating plans filed for 2027. For the %s's outlook under "
                       "section 7.2 of the traffic-light scheme; the plans are approved in December." % W.SURVEY_SHORT, A_META),
             Paragraph("All five operators have filed their plans for 2027. No plant adds a well, changes its reservoir "
                       "section or changes the share between its injection wells. Heat demand on each district heating "
                       "network is planned as in 2026.", A_BODY),
             Paragraph("Injection", A_H2),
             Paragraph("Every plan sets the injection of each quarter of 2027 at the volume injected in the same quarter "
                       "of 2026: flow rates, running hours and the summer revision as in 2026. The fourth quarter is "
                       "planned as the fourth quarter of 2025, the last complete one.", A_BODY),
             Paragraph("Plans by plant", A_H2),
             _grid([["Plant", "Filed", "Summer revision 2027", "Remarks"]] +
                   [[W.NAME[p], FILED[p], REVISION_2027[p],
                     {"MOS": "two injection wells, share as in 2026",
                      "PFB": "town network; no extension planned in 2027",
                      "LZR": "production pump replacement during the revision",
                      "WDR": "", "OTM": ""}[p]] for p in W.PLANTS],
                   [30 * mm, 32 * mm, 40 * mm, 64 * mm], A_CELLB, A_CELL, align_from=4, box=True),
             Spacer(1, 6),
             Paragraph("The approvals keep the traffic-light scheme of 2024 in force. From 1 January 2027 its counts are "
                       "made on the networks of the 2026 ordinance.", A_BODY)]
    frame = _frame("%s  |  Referat Geothermie" % W.AUTHORITY, "Az. GT-BP-2027", "Vermerk, nur für den Dienstgebrauch")
    doc.build(story, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------- the notes
NOTES_TEXT = """# Extract for the 2027 traffic-light outlook

Pulled 12 Oct 2026 by {data} (data office) for {lead}. Five plants under the {authority} scheme: Moorstetten (MOS),
Pfeilbrunn (PFB), Lanzenried (LZR), Wendelsried (WDR), Ottenmoos (OTM). Record 1 Jan 2023 to 30 Sep 2026 unless a
file says otherwise.

Files
- {cat}: reviewed catalogue, every event the analysts finalised in the region, one row per event. Times UTC, ML is the
  survey's local magnitude, depth below sea level. event_type earthquake or explosion (quarry blasts). analyst is the
  reviewer's initials, reviewed_utc when the event was finalised.
- {auto}: the event database's origin table as stored, same period. Times UTC; ml is the local magnitude computed
  with each origin. Events the analysts deleted as false triggers are purged with their origins.
- {hourly}: hourly means from each injection well's telemetry (scheme 6.1), stamped at the start of the hour, UTC.
  Rate in litres per second, wellhead pressure in bar.
- {reports}: the operators' monthly reports of metered volumes (scheme 6.2), as received, one sheet per year.
- {plant_reg}, {well_reg}: our registers. Open-hole sections as surveyed; depths are true vertical depth below ground.
- {inventory}: station metadata as exported from the station database on 12 Oct, every channel epoch with its
  location code; dates UTC.
- {gaps}: data gaps of 60 s or more per channel from the archive's availability check, for 1 Jan to 30 Sep 2026
  local time; times UTC.
- {visits}: the field crew's visit sheet as kept.
- {scheme}, {ordinance}, {plans}: from the authority. {bulletin}: ours, as published.
- {federal}: the federal agency's catalogue for the region (their ids and magnitudes, 2.0 and over), as downloaded.
- {gw}: shallow groundwater monitoring at the plants (water-law permits), monthly.
"""


def write_notes(path):
    text = NOTES_TEXT.format(data=PEOPLE["data"], lead=PEOPLE["lead"], authority=W.AUTHORITY, cat=R.CAT, auto=R.AUTO,
                             hourly=R.HOURLY, reports=R.REPORTS, plant_reg=R.PLANT_REG, well_reg=R.WELL_REG,
                             inventory=R.INVENTORY, gaps=R.GAPS, visits=R.VISITS, scheme=SCHEME, ordinance=ORDINANCE,
                             plans=PLANS, bulletin=BULLETIN, federal=R.FEDERAL, gw=R.GW)
    with open(path, "w", newline="\n", encoding="utf-8") as fh:
        fh.write(text)
