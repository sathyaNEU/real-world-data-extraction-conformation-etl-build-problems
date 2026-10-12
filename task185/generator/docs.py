"""The pack's documents: Southward Mutual's weather index pricing manual, the Merrin Flat station history from the
National Climate Service, the heat-day cover's term sheets for 2027/28 (quoted) and 2026/27 (last season's), and the
weather desk's extract notes."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                   # noqa: E402
from reportlab.lib.pagesizes import A4                                             # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import mm                                                 # noqa: E402
from reportlab.pdfbase import pdfmetrics                                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                       # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W      # noqa: E402

MANUAL = "southward_weather_index_pricing_manual_rev3.pdf"
HISTORY = "ncs_station_history_merrin_flat.pdf"
TERMS_27 = "heat_cover_term_sheet_2027_28_quote.pdf"
TERMS_26 = "heat_cover_term_sheet_2026_27.pdf"
NOTES = "extract_notes_merrin_valley_renewal_2027-08-27.md"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Serif", "LiberationSerif-Regular"),
              ("Serif-B", "LiberationSerif-Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
INK, GREY = colors.HexColor("#20242a"), colors.HexColor("#5f666e")

M_BODY = ParagraphStyle("mb", fontName="Serif", fontSize=10.3, leading=14, textColor=INK, spaceAfter=5)
M_CL = ParagraphStyle("mc", parent=M_BODY, leftIndent=24, firstLineIndent=-24)
M_H1 = ParagraphStyle("mh1", fontName="Serif-B", fontSize=15, leading=19, textColor=INK, spaceAfter=3)
M_H2 = ParagraphStyle("mh2", fontName="Serif-B", fontSize=11, leading=14, textColor=INK, spaceBefore=9, spaceAfter=3)
M_META = ParagraphStyle("mm", fontName="Serif", fontSize=8.8, leading=11.5, textColor=GREY, spaceAfter=8)
S_BODY = ParagraphStyle("sb", fontName="Sans", fontSize=9.4, leading=12.8, textColor=INK, spaceAfter=5)
S_H1 = ParagraphStyle("sh1", fontName="Sans-B", fontSize=13.5, leading=17, textColor=INK, spaceAfter=2)
S_H2 = ParagraphStyle("sh2", fontName="Sans-B", fontSize=10, leading=13, textColor=INK, spaceBefore=8, spaceAfter=3)
S_META = ParagraphStyle("sm", fontName="Sans", fontSize=8.1, leading=10.4, textColor=GREY, spaceAfter=7)
S_CELL = ParagraphStyle("sc", fontName="Sans", fontSize=8.8, leading=11.4, textColor=INK)
S_CELLB = ParagraphStyle("scb", parent=S_CELL, fontName="Sans-B")


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=23 * mm, rightMargin=23 * mm, topMargin=21 * mm,
                             bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")


def _frame(top_left, top_right, foot, font="Serif"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 8)
        canvas.drawString(23 * mm, A4[1] - 12 * mm, top_left)
        canvas.drawRightString(A4[0] - 23 * mm, A4[1] - 12 * mm, top_right)
        canvas.setFont(font, 7.4)
        canvas.drawString(23 * mm, 11 * mm, foot)
        canvas.drawRightString(A4[0] - 23 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


MANUAL_CLAUSES = [
    ("1  Scope", [
        ("1.1", "This manual sets how the weather desk prices the index covers Southward Mutual writes for growers and "
                "their co-operatives: heat-day covers, frost-night covers and rainfall-deficit covers. Each pays a fixed "
                "sum a hectare on an index read at one named station of the National Climate Service."),
        ("1.2", "A cover's terms (index station, triggers, deductible, rates, cap and period) are in its term sheet. "
                "This manual sets how the premium a hectare is built from the station's record."),
    ]),
    ("2  The station record", [
        ("2.1", "The record is the Service's approved daily readings for the index station. Provisional readings are "
                "not used, and a day the Service has not yet approved is left out of the record until it is."),
        ("2.2", "Where the Service renumbers a station the record runs across both numbers as one station."),
    ]),
    ("3  Heat-day covers", [
        ("3.1", "A heat-day cover is priced on the daily maximum temperature at its index station for every day from "
                "1 December 1965 to the last day of February of the latest complete season, each day's maximum as the "
                "station's present instrument would have recorded it."),
        ("3.2", "A season runs from 1 December to the last day of February and is named by its two years, as "
                "1965/66."),
        ("3.3", "Each season's heat days and severe heat days are counted under the triggers in the term sheet."),
        ("3.4", "Each count is fitted by least squares against the season's first year over the record, on its own "
                "line. A season's count is projected to the season being priced by adding the line's slope times the "
                "years between them. A projected count below zero is taken as zero; projected counts are not rounded."),
        ("3.5", "The expected heat days and severe heat days of the season being priced are the two lines' values at "
                "that season."),
        ("3.6", "The burn cost is the average, over the seasons of the record, of the payout a hectare each projected "
                "season would make under the terms being quoted."),
        ("3.7", "The premium a hectare is the burn cost times 1.32, rounded once to the whole dollar."),
    ]),
    ("4  Frost-night and rainfall-deficit covers", [
        ("4.1", "Frost-night covers count the nights from 1 September to 31 October whose minimum at the index station "
                "is minus 1.0 C or lower; rainfall-deficit covers measure the shortfall of the station's rainfall from "
                "1 April to 31 October against the cover's strike. Both are priced on the burn of section 3, on their "
                "own index, with the loading in their term sheets."),
    ]),
    ("5  Review", [
        ("5.1", "Rates are rebuilt from the record at each renewal and are not carried from the last season's quote."),
    ]),
]


def write_manual(path):
    who = W.PEOPLE["portfolio"][0]
    title = "Weather index pricing manual, revision 3"
    doc = _doc(path, title, who)
    s = [Paragraph("SOUTHWARD MUTUAL · WEATHER DESK", M_META), Paragraph(title, M_H1),
         Paragraph("Effective 1 March 2026. Owner: %s. Supersedes revision 2 (2021)." % W.PEOPLE["portfolio"][1], M_META)]
    for head, items in MANUAL_CLAUSES:
        s.append(Paragraph(head, M_H2))
        for num, text in items:
            s.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (num, text), M_CL))
    foot = "Southward Mutual | Weather index pricing manual | revision 3"
    doc.build(s, onFirstPage=_frame("Weather desk", "Revision 3", foot), onLaterPages=_frame("Weather desk", "Revision 3", foot))


HISTORY_EVENTS = [
    ("1 Jul 1964", "Station opened at the Merrin Flat Agricultural Research Station as a cooperative climate station, "
                   "number %s. Maximum and minimum thermometers in a large wooden screen on the research station's "
                   "lawn, read at 9 am by the station's observer." % W.OLD_ID),
    ("Mar 1972", "Rain gauge moved 12 m east when the lawn was re-laid; the screen did not move."),
    ("1 Nov 1995", "Automatic weather station commissioned on the same enclosure: platinum resistance probe in a small "
                   "plastic multi-plate shield, 1-minute sampling, the daily maximum the highest 1-minute value in the "
                   "24 hours from 9 am. The automatic station became the station's official instrument and was "
                   "numbered %s." % W.NEW_ID),
    ("1 Nov 1995 to 30 Apr 1998", "Observer read the glass maximum thermometer in the large screen each morning beside "
                                  "the automatic station as a check. The paired readings are in the Service's parallel "
                                  "observations archive with those of six other sites."),
    ("May 1998", "Large screen and glass thermometers removed."),
    ("2001 to 2027", "Probe calibrated against a travelling standard each year; probe and shield not replaced."),
]


def write_history(path):
    who, role = W.PEOPLE["climate"]
    title = "Station history: Merrin Flat"
    doc = _doc(path, title, who)
    s = [Paragraph("NATIONAL CLIMATE SERVICE · STATION HISTORY", S_META), Paragraph(title, S_H1),
         Paragraph("Stations %s (to 31 October 1995) and %s (from 1 November 1995). Compiled by %s, %s, from the "
                   "station file. Printed 9 August 2027." % (W.OLD_ID, W.NEW_ID, who, role), S_META),
         Paragraph("Site", S_H2),
         Paragraph("Merrin Flat Agricultural Research Station, on the valley floor 4 km south of Merrin township, "
                   "elevation 61 m. The enclosure has stood on the same lawn since 1964; the surrounding vineyard and "
                   "orchard blocks have been under drip irrigation since the 1980s.", S_BODY),
         Paragraph("Observing practice", S_H2),
         Paragraph("Observers entered the glass readings in the climatological register to the nearest half degree. "
                   "The register was digitised by the Service in 2009 from the original sheets.", S_BODY),
         Paragraph("Changes", S_H2)]
    rows = [[Paragraph("Date", S_CELLB), Paragraph("Change", S_CELLB)]]
    rows += [[Paragraph(d, S_CELL), Paragraph(t, S_CELL)] for d, t in HISTORY_EVENTS]
    t = Table(rows, colWidths=[38 * mm, 126 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.4, GREY), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    s.append(t)
    foot = "National Climate Service | Station history | %s" % W.NEW_ID
    doc.build(s, onFirstPage=_frame("Station history", W.STATION, foot, "Sans"),
              onLaterPages=_frame("Station history", W.STATION, foot, "Sans"))


def _terms_table(rows):
    data = [[Paragraph(k, S_CELLB), Paragraph(v, S_CELL)] for k, v in rows]
    t = Table(data, colWidths=[44 * mm, 120 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.3, GREY),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def money(x):
    return "${:,.2f}".format(x) if x != int(x) else "${:,}".format(int(x))


def write_terms(path, season, deductible, heat_rate, severe_rate, cap, status, issued):
    who = W.PEOPLE["portfolio"][0]
    label = W.season_label(season)
    title = "Heat-day cover, %s season: term sheet" % label
    doc = _doc(path, title, who)
    end = "29 February %d" % (season + 1) if (season + 1) % 4 == 0 else "28 February %d" % (season + 1)
    rows = [
        ("Insured", "%s, for its members' vineyard blocks on the schedule" % W.COOP),
        ("Insurer", "Southward Mutual"),
        ("Period", "1 December %d to %s" % (season, end)),
        ("Index station", "%s, National Climate Service station %s" % (W.STATION, W.NEW_ID)),
        ("Heat day", "a day of the period whose maximum temperature at the index station is 35.0 C or more"),
        ("Severe heat day", "a day of the period whose maximum temperature at the index station is 40.0 C or more; a "
                            "severe heat day is also a heat day"),
        ("Payout", "a hectare insured: %s for each heat day after the period's first %d, plus %s for each severe "
                   "heat day, up to %s a hectare for the period" % (money(heat_rate), deductible, money(severe_rate),
                                                                     money(cap))),
        ("Index data", "the Service's approved daily maximum for the index station; for a day it does not report, the "
                       "approved maximum at Tolbin Hill (station 041455)"),
        ("Attachment", "the cover attaches on 1 December %d to the blocks on the schedule that day" % season),
        ("Premium", "the rate a hectare times the insured hectares on the schedule when the cover attaches, to the "
                    "nearest whole dollar (50 cents up)"),
        ("Settlement", "an interim payment after the period on the Service's provisional readings and the balance once "
                       "the Service approves the period's readings"),
    ]
    s = [Paragraph("SOUTHWARD MUTUAL · WEATHER DESK", S_META), Paragraph(title, S_H1),
         Paragraph("%s Issued %s by %s, %s." % (status, issued, who, W.PEOPLE["portfolio"][1]), S_META),
         _terms_table(rows), Spacer(1, 8),
         Paragraph("The rate a hectare is set by the weather desk under the weather index pricing manual and stated in "
                   "the quote letter.", S_META)]
    foot = "Southward Mutual | Heat-day cover %s | %s" % (label, W.COOP_SHORT)
    doc.build(s, onFirstPage=_frame("Weather desk", label, foot, "Sans"), onLaterPages=_frame("Weather desk", label, foot, "Sans"))


NOTES_TEXT = """# Extract for the Merrin Valley heat-day renewal

Pulled 27 Aug 2027 for {portfolio} (weather desk). Station data from the National Climate Service's data
portal; policy, claims and ledger extracts from our own systems. Questions on the station files to {climate} at
the Service, on the co-operative's register to {coop}.

Files:
- {daily}: the automatic station, daily TMAX, TMIN (C) and PRCP (mm), 1 Nov 1995 on.
- {register}: the climatological register for {old_id}, one sheet a year, 1964 to 1995, as the Service digitised it.
- {parallel}: the Service's parallel observations archive, daily maxima, seven sites.
- {district}: monthly mean maxima for the district's other stations, as asked.
- {stations}: the Service's station list for the district.
- {history}: station history for Merrin Flat.
- {manual}, {terms27}, {terms26}: ours.
- {schedule}: policy system extract, every block on the co-operative's policy since inception.
- {blocks}: the co-operative's block register, sent by {coop_first} on 3 Aug. Its sub-districts are the ones the
  co-operative reports by and splits the premium by.
- {claims}: claims register report, heat-day cover, one row per claim and insured block.
- {ledger}: GL 6120 weather claims payments, posting date and financial year (1 July to 30 June).

Things to know:
- quality on the daily file: A approved, P provisional. Approved runs to 30 Jun 2027.
- A day's maximum is the highest reading in the 24 hours from 9 am, filed against the day the 24 hours began. Same
  in the register and the automatic station.
- The register's blank cells are days with no reading, or days that do not exist.
- grower_ref on our extracts is the co-operative's member number with our MV- prefix.
"""


def write_notes(path, names):
    open(path, "w").write(NOTES_TEXT.format(portfolio=W.PEOPLE["portfolio"][0], climate=W.PEOPLE["climate"][0],
                                            coop=W.PEOPLE["coop"][0], coop_first=W.PEOPLE["coop"][0].split()[0],
                                            old_id=W.OLD_ID, history=HISTORY, manual=MANUAL, terms27=TERMS_27,
                                            terms26=TERMS_26, **names))
