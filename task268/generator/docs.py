"""The pack's documents: the board paper that sets how the pilot metro is chosen, the survey's public-use file
codebook, Location Analytics' notes on the commuting extract, and the data pack manifest."""
from __future__ import annotations

import csv

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import letter                                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import mm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1d2326"), colors.HexColor("#5b646b"), colors.HexColor("#b7bec4")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=9.8, leading=13.6, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=14, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.6, leading=14, textColor=INK, spaceBefore=7,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.4, leading=11.4, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.2, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.2, leading=10.4, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=24, firstLineIndent=-24))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.4)
        canvas.drawString(19 * mm, letter[1] - 11.5 * mm, left)
        canvas.drawRightString(letter[0] - 19 * mm, letter[1] - 11.5 * mm, right)
        canvas.drawRightString(letter[0] - 19 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=20 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


# ---------------------------------------------------------------------------------------------- the board paper
def write_board(path):
    S = styles("Serif", colors.HexColor("#7A3E12"))
    doc = _doc(path, "Weekday dark-store pilot 2027: choosing the metro", K.ORG)
    st = [Paragraph("Weekday dark-store pilot, 2027: how the metro is chosen", S["h1"]),
          Paragraph("Paper to the Board of Directors, %s Inc. From %s, Vice President, Network Expansion. 17 September "
                    "2026. For decision now; the choice itself comes to the meeting of 9 December 2026."
                    % (K.ORG, K.PEOPLE["vp"]), S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    H = lambda t: st.append(Paragraph(t, S["h2"]))
    C = lambda n, t: st.append(Paragraph("%s&nbsp;&nbsp;%s" % (n, t), S["clause"]))
    H("1. What the board is asked to decide")
    P("The board is asked to fix, today, the measure on which the 2027 weekday pilot metro will be chosen, so that "
      "Network Expansion and Location Analytics can bring the choice to the December meeting with the measure "
      "settled in advance. The choice itself is not made in this paper.")
    H("2. The pilot")
    P("One dark store in one metro's core, delivering by e-bike within twenty minutes of the order, Monday to Friday "
      "from 9:00 to 18:00, for the twelve months from 1 February 2027. As in %s, the store will deliver to homes and "
      "to workplaces alike. Weekends stay out of the pilot: they are already well served by the national grocers' "
      "same-day slots in all six candidate metros." % K.HOME_METRO)
    H("3. The candidates")
    P("Six metros where %s has no store: %s. A metro's core is the set of 2020 census tracts the planning map lists "
      "for it (candidate_cores_2027.xlsx); the cores were drawn by Network Expansion in August around each metro's "
      "downtown and the inner neighbourhoods an e-bike courier reaches from it." % (K.ORG, ", ".join(sorted(K.METRO_NAMES))))
    H("4. The measure")
    C(K.CLAUSE["pick"], "The pilot goes to the metro whose core has the highest delivery-weighted density.")
    C(K.CLAUSE["density"], "A core's delivery-weighted density is the average over the core's tracts of each tract's people present "
             "per square kilometre of its land, each tract weighted by its people present.")
    C(K.CLAUSE["present"], "A tract's people present are the people in it on an average weekday of the pilot: its residents, except "
             "those who are at a workplace in another tract that day, and the people living in other tracts who are at "
             "a workplace in it that day. Residents are as the census population table counts them; workers are the "
             "people whose primary job the regional commuting table records, at the tract of the workplace.")
    C(K.CLAUSE["latest"], "The cores are compared as the latest releases describe them, with no growth projected to 2027.")
    P("Section 4 is the whole of the measure. It replaces the ranking by residents per square kilometre used for the "
      "%s launches, which counted the morning's empty office districts as low demand when a third of %s's weekday "
      "orders now go to workplaces." % (K.HOME_METRO, K.HOME_METRO))
    H("5. What else the December paper reports")
    P("For every core the December paper also reports the ground-floor units on the market that a dark store could "
      "take, with their asking rents, and the dark stores the two competitors run there. Neither decides the pilot: "
      "the first shows that a site can be found, the second what the store will compete with.")
    H("6. Timetable")
    P("Location Analytics assembles the data pack by early October 2026. Network Expansion brings the choice, with "
      "each core's figures, to the meeting of 9 December 2026; the lease and the courier hiring follow in January.")
    H("Resolution proposed")
    P("That the metro for the 2027 weekday dark-store pilot be chosen under section 4 of this paper.")
    doc.build(st, onFirstPage=_frame(K.ORG + " Inc. Board of Directors", "Paper BD-2026-41", "Serif"),
              onLaterPages=_frame(K.ORG + " Inc. Board of Directors", "Paper BD-2026-41", "Serif"))


# ---------------------------------------------------------------------------------------------- the codebook
def write_codebook(path):
    S = styles("Sans", colors.HexColor("#1F4E79"))
    doc = _doc(path, "Work Location Survey public-use file codebook", "WLS Consortium")
    st = [Paragraph("Work Location Survey (WLS): public-use file codebook", S["h1"]),
          Paragraph("Waves October 2025 to September 2026. Release 2026-2, 2 October 2026. WLS Consortium.", S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    H = lambda t: st.append(Paragraph(t, S["h2"]))
    H("The survey")
    P("The WLS interviews employed adults aged 18 and over in the United States online every month, about 5,000 a "
      "month, from a probability-recruited panel. Each respondent answers for the five weekdays (Monday to Friday) of "
      "the week before the interview, the reference week, and for their main job when they hold more than one.")
    H("Weights")
    P("FINALWT is each respondent's final weight, adjusted for panel nonresponse and raked by age, sex and education "
      "to the month's employed civilian population aged 18 and over. Each wave's weights sum to that month's "
      "population. Use FINALWT for every estimate. Estimates over several waves use the weights as they stand.")
    H("Variables")
    rows = [["Variable", "Content and codes"],
            ["WAVE", "Interview month, YYYYMM"],
            ["RESPID", "Respondent identifier, unique in the file"],
            ["FINALWT", "Final weight (people)"],
            ["AGEGRP", "1 18-24; 2 25-34; 3 35-44; 4 45-54; 5 55-64; 6 65 and over"],
            ["SEX", "1 male; 2 female"],
            ["EDUC", "1 high school or less; 2 some college or associate degree; 3 bachelor's degree; 4 graduate degree"],
            ["NAICS_SECTOR", "Sector of the main job, 2017 NAICS two-digit sector (31-33, 44-45 and 48-49 as ranges)"],
            ["HOMEREL", "Where the respondent lives relative to the metropolitan statistical area containing their usual "
                        "workplace, from home and workplace ZIP codes and the July 2023 OMB delineation: 1 in a central "
                        "county of that area; 2 in an outlying county of that area; 3 outside that area; 4 no usual "
                        "workplace, or a usual workplace outside any metropolitan statistical area; 9 not reported"],
            ["DAYS_PREM", "Weekdays of the reference week on which the respondent worked at their employer's premises, "
                          "for any part of the day, 0 to 5"],
            ["DAYS_HOME", "Weekdays on which the respondent worked from home and not at the premises, 0 to 5"],
            ["DAYS_NOTWORK", "Weekdays on which the respondent did not work (leave, holiday, sickness, not scheduled), "
                             "0 to 5"]]
    st.append(_table(S, rows, [30, 148]))
    st.append(Spacer(1, 6))
    P("The three day counts sum to five for every respondent. Respondents with HOMEREL 4 or 9 answer every other "
      "question.")
    H("Release notes")
    P("Release 2026-2 adds the September 2026 wave and revises no earlier wave. Sector codes follow the 2017 NAICS "
      "throughout. Respondent identifiers are not linked across waves.")
    doc.build(st, onFirstPage=_frame("WLS Consortium", "PUF codebook, release 2026-2", "Sans"),
              onLaterPages=_frame("WLS Consortium", "PUF codebook, release 2026-2", "Sans"))


# ---------------------------------------------------------------------------------------------- the extract notes
def write_od_notes(path, n_main, n_aux):
    S = styles("Sans", colors.HexColor("#3B5B2A"))
    doc = _doc(path, "Regional commuting extract, 2022: notes", "Location Analytics")
    st = [Paragraph("Regional commuting extract, 2022: notes", S["h1"]),
          Paragraph("Location Analytics, %s. Prepared 2 October 2026 for the 2027 pilot metro paper." % K.ORG, S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    H = lambda t: st.append(Paragraph(t, S["h2"]))
    H("Source")
    P("LEHD Origin-Destination Employment Statistics (LODES), version 8, origin-destination files for job type JT01 "
      "(primary jobs), year 2022, for Colorado, Indiana, Missouri, North Carolina, Ohio and Tennessee, downloaded on "
      "1 October 2026. A primary job is the highest-paying job of each worker in the year, so each worker counts once. "
      "Blocks are aggregated to 2020 census tracts (the first eleven digits of each block code).")
    H("What the extract keeps")
    P("Every tract pair whose work tract or home tract is a core tract on the planning map (candidate_cores_2027.xlsx). "
      "Pairs with neither end in a core are not kept.")
    H("Two parts")
    P("The agency publishes each state's flows in two parts, and the extract keeps them as they come: the main part "
      "(%s, %d tract pairs), where the worker lives and works in the same state, and the auxiliary part (%s, %d tract "
      "pairs), where the worker works in the state and lives in another." % (K.FILES["od_main"], n_main, K.FILES["od_aux"], n_aux))
    H("Columns")
    rows = [["Column", "Content"],
            ["w_tract", "Work tract, 2020 census tract code (state, county, tract), 11 characters"],
            ["h_tract", "Home tract, the same coding"],
            ["S000", "Total primary jobs"],
            ["SA01, SA02, SA03", "Jobs of workers aged 29 or younger; 30 to 54; 55 or older"],
            ["SE01, SE02, SE03", "Jobs with earnings of $1,250 a month or less; $1,251 to $3,333; more than $3,333"],
            ["SI01", "Jobs in the Goods Producing industry sectors (NAICS 11, 21, 23, 31-33)"],
            ["SI02", "Jobs in the Trade, Transportation, and Utilities industry sectors (NAICS 22, 42, 44-45, 48-49)"],
            ["SI03", "Jobs in All Other Services industry sectors (NAICS 51 to 92)"],
            ["createdate", "Date the agency created the file, YYYYMMDD"]]
    st.append(_table(S, rows, [34, 144]))
    st.append(Spacer(1, 6))
    P("S000 equals the sum of the three age bands, of the three earnings bands and of the three industry groups on "
      "every row.")
    doc.build(st, onFirstPage=_frame("Location Analytics", "Commuting extract 2022", "Sans"),
              onLaterPages=_frame("Location Analytics", "Commuting extract 2022", "Sans"))


def write_manifest(path, rows):
    with open(path, "w", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["file_name", "description", "source", "as_of", "extent", "terms"])
        wr.writerows(rows)
