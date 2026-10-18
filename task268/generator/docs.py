"""The pack's documents: the haddock stock recovery plan the members adopted in March 2026, the autumn survey's field
manual (revision 3), the 2026 quota management rules, the 2025 square-mesh panel trial note and the pack's contents
list."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
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
INK, GREY, RULE = colors.HexColor("#1c2428"), colors.HexColor("#5a646b"), colors.HexColor("#b4bdc3")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=9.8, leading=13.6, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=14.5, leading=18.5, textColor=accent, spaceAfter=2),
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
        canvas.drawString(19 * mm, A4[1] - 11.5 * mm, left)
        canvas.drawRightString(A4[0] - 19 * mm, A4[1] - 11.5 * mm, right)
        canvas.drawRightString(A4[0] - 19 * mm, 10 * mm, "Page %d" % doc.page)
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
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=20 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


# ---------------------------------------------------------------------------------------------- the recovery plan
def write_plan(path, grounds):
    S = styles("Serif", colors.HexColor("#1F4E63"))
    doc = _doc(path, "Haddock stock recovery plan 2026", K.ORG_LTD)
    st = [Paragraph("Haddock Stock Recovery Plan", S["h1"]),
          Paragraph("%s. Adopted by the members in general meeting on 24 March 2026. Replaces nothing; it adds to the "
                    "organisation's fishing rules for 2026 and later years." % K.ORG_LTD, S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    H = lambda t: st.append(Paragraph(t, S["h2"]))
    C = lambda n, t: st.append(Paragraph("%s&nbsp;&nbsp;%s" % (n, t), S["clause"]))
    H("1. Why the members adopted this plan")
    P("Haddock is the members' main catch, and the members take most of it from six grounds east and north-east of the "
      "home ports. After the poorer seasons of 2023 to 2025 the members agreed at the November 2025 general meeting to "
      "add measures of their own, on their own grounds, to the national management of the stock, and asked the "
      "management committee to bring a plan to the spring meeting. This is that plan.")
    H("2. Scope")
    P("The plan applies to every member vessel fishing with towed gear on the six grounds named in Annex A, whatever "
      "the target species. A ground's stock area is the set of cells Annex A assigns to it. Fishing outside the six "
      "grounds is not affected.")
    H("3. Measures")
    C("3.1", "Codends of 120 mm mesh or more on the six grounds, as already required by the organisation's 2024 rules.")
    C("3.2", "Real-time closures: where a member's haul on one of the grounds holds more than 30 per cent haddock under "
             "30 cm by number, the cell is closed to members for 14 days and the closure is posted to every member that day.")
    C("3.3", "One ground closed to members' towed gear each year, chosen as section 4 sets out.")
    C("3.4", "Members keep reporting every haul through the organisation's e-logbook app, as they have done since "
             "January 2023.")
    H("4. The annual ground closure")
    C("4.1", "Each December the management committee closes one ground to members' towed gear for the following "
             "calendar year: the ground whose haddock stock in the year before that year has fallen furthest below its "
             "base, as a share of the base. A ground's base is its average stock over 2019, 2020 and 2021.")
    C("4.2", "A ground's haddock stock in a year is the weight of haddock on its stock area.")
    C("4.3", "A closed ground is closed from 1 January to 31 December of its closure year. Members may steam through it "
             "with their gear stowed.")
    C("4.4", "The science and sustainability officer puts the evidence for every ground to the committee before its "
             "December meeting. The first closure is for 2027.")
    H("5. Compliance")
    P("The organisation checks the closures against members' e-logbook positions and the vessel monitoring data the "
      "administration shares with producer organisations. A member vessel that tows in a closed ground or a closed "
      "cell is dealt with under article 14 of the organisation's articles: a first breach costs the licence 10 tonnes "
      "of the pool's haddock quota for the rest of the year, a second within three years suspends the member's quota "
      "transfers for twelve months. A skipper who believes a breach was recorded in error may ask the committee to "
      "review it within 28 days.")
    H("6. Costs and support")
    P("The organisation meets the cost of the real-time closure notices and of the science office's work for the plan "
      "from the members' levy. Members whose usual ground is closed may ask the quota office for help finding leases "
      "on other grounds; the office keeps a list of members willing to lease out haddock for the year.")
    H("7. Review")
    P("The general meeting reviews the plan in 2029, or sooner if the management committee asks it to.")
    H("Annex A. The grounds")
    P("The organisation's grid divides each ICES statistical rectangle into 36 cells, each 5 minutes of latitude by 10 "
      "minutes of longitude, numbered 1 to 36 from the north-west corner along each row. Annex A lists every cell of the "
      "six grounds with its depth band (A under 100 m, B 100 m to under 140 m, C 140 m and deeper, from the cell's "
      "charted depth), its charted depth, its bounds and its area. It is kept as a data file, ground_grid_annex_a.csv, "
      "so that the boundaries can be loaded into the members' plotters; this table summarises it.")
    rows = [["Ground", "Code", "Cells", "Stock area (km²)"]]
    for g, code, n, area in grounds:
        rows.append([g, code, str(n), "{:,.0f}".format(area)])
    st.append(_table(S, rows, (52, 22, 22, 34), right=(2, 3)))
    doc.build(st, onFirstPage=_frame(K.ORG_LTD, "Haddock Stock Recovery Plan", "Serif"),
              onLaterPages=_frame(K.ORG_LTD, "Haddock Stock Recovery Plan", "Serif"))


# ---------------------------------------------------------------------------------------------- the survey manual
def write_manual(path, replaced, missed, vessel):
    S = styles("Sans", colors.HexColor("#2C5F2D"))
    doc = _doc(path, "Autumn gear and bycatch survey: field manual, revision 3", K.ORG_LTD)
    st = [Paragraph("Autumn Gear and Bycatch Survey: Field Manual", S["h1"]),
          Paragraph("Revision 3, 4 September 2023. %s, science and sustainability office. Revision 1 (August 2019) set "
                    "the survey up; revision 2 (September 2021) changed the catch sheet; this revision records the 2023 "
                    "station replacements and the electronic catch records." % K.ORG_LTD, S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    H = lambda t: st.append(Paragraph(t, S["h2"]))
    H("1. What the survey is for")
    P("Each October the organisation charters a member vessel for about two weeks to do two jobs on the grounds the "
      "members fish. The first is to monitor bycatch: juvenile haddock, cod and whiting, spurdog, skates and rays, and "
      "the porpoises and seabirds the members must report, in every depth of every ground. The second is to give the "
      "members a fixed platform for trials of selective gear, such as square-mesh panels and larger codends, fished on "
      "the same grounds at the same season each year.")
    H("2. Stations")
    P("The survey tows the same stations every year. In August 2019 twelve stations were placed in each depth band of "
      "each of the six grounds, 216 in all: for each station a cell was drawn at random from the band's cells in the "
      "organisation's grid and a position drawn at random inside it, so a cell may hold more than one station. A "
      "station's depth band is the band the grid gives its cell. Each band has the same number of stations so that "
      "bycatch rates in shallow and in deep water are measured with the same precision.")
    P("A station where the net is torn on the bottom is replaced by a new position drawn the same way within the same "
      "ground and depth band, and the old position is not fished again. After the net was torn at stations %s in "
      "October 2022, they were replaced from 2023 by %s." % (" and ".join(r[0] for r in replaced),
                                                         " and ".join(r[1] for r in replaced)))
    P("A station that cannot be fished before the charter ends is left out that year and fished again the next. In "
      "2020 station %s was not fished: the weather closed in on the last two days of the charter." % missed)
    H("3. Gear and towing")
    P("The survey trawl is the organisation's own: a 32 m headline two-panel trawl with a 40 mm codend liner, rigged "
      "the same way since 2019 and carried from charter to charter. Each tow lasts 30 minutes from the moment the "
      "winch brakes are set to the start of hauling, at 3.5 knots over the ground. A tow that comes fast or is cut "
      "short before 25 minutes is towed again at the same station; only the valid tow is recorded. Towing is in "
      "daylight, from about 06:00 to 19:00 local time.")
    H("4. Catch")
    P("The whole catch is sorted on deck. Every species is weighed to 0.1 kg; haddock, cod and whiting are counted, "
      "and haddock under 30 cm counted separately; spurdog are counted; skates and rays weighed together. Porpoises "
      "and seabirds caught are recorded by number. A species not caught in a tow is recorded as zero.")
    H("5. Records")
    P("The survey's records are one row per valid tow: survey year; tow (year and running number); station; ground "
      "code; date; shot time (local time); shot latitude and longitude (decimal degrees); depth at the shot (m, from "
      "the sounder); duration (minutes); then haddock (kg, number, number under 30 cm), cod, whiting and saithe (kg), "
      "spurdog (number), skates and rays (kg), porpoises and seabirds (number). Revision 3 moves the records from the "
      "paper catch sheet to the survey laptop; the 2019 to 2022 sheets have been keyed in to the same layout.")
    H("6. Vessel and staff")
    P("The %s, a member trawler, has fished every survey since 2019 under charter, with her own skipper and crew. "
      "The science and sustainability officer leads the survey with one contracted observer; both sort and record the "
      "catch, and the observer keeps the protected species log." % vessel)
    H("7. Permits and safety")
    P("The administration's scientific fishing permit covers the 40 mm liner, the gear trials and the landing of "
      "undersized fish for measurement; it is renewed each August and carried on board. The observer holds a current "
      "sea survival certificate and is briefed by the skipper on the first day. Any protected species brought aboard "
      "alive is returned at once and logged; a dead porpoise is kept for the strandings scheme if the scheme asks for it.")
    H("8. Survey history")
    rows = [["Year", "Survey dates", "Valid tows", "Note"]]
    for y, d0, d1, n, note in MANUAL_HISTORY:
        rows.append([y, "%s to %s" % (d0, d1), str(n), note])
    st.append(Spacer(1, 4))
    st.append(_table(S, rows, (14, 50, 22, 86), right=(2,)))
    doc.build(st, onFirstPage=_frame(K.ORG_LTD, "Autumn survey field manual, rev. 3", "Sans"),
              onLaterPages=_frame(K.ORG_LTD, "Autumn survey field manual, rev. 3", "Sans"))


MANUAL_HISTORY = []   # filled by build.py from the survey records, years 2019 to 2022 (revision 3 is dated 2023)


# ---------------------------------------------------------------------------------------------- the quota rules
def write_rules(path):
    S = styles("Sans", colors.HexColor("#5B3A73"))
    doc = _doc(path, "Quota management rules 2026: haddock", K.ORG_LTD)
    st = [Paragraph("Quota Management Rules 2026: Haddock", S["h1"]),
          Paragraph("%s. Issued 12 January 2026 by the management committee under the organisation's articles; in force "
                    "for the 2026 quota year." % K.ORG_LTD, S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    H = lambda t: st.append(Paragraph(t, S["h2"]))
    C = lambda n, t: st.append(Paragraph("%s&nbsp;&nbsp;%s" % (n, t), S["clause"]))
    H("1. Pools")
    P("The organisation manages its members' haddock quota in five pools: North trawl (N), East trawl (E), Twin rig "
      "(T), Seine net (S) and Inshore (I). Each fishing licence the organisation manages belongs to one pool, as the "
      "members' list records. Quota is fished by the licences of a pool; a pool lends to another only by a lease "
      "between licences.")
    H("2. What moves a pool's quota")
    C("2.1", "Allocation: each licence's quota for the year, from its fixed quota allocation units, with effect from 1 "
             "January.")
    C("2.2", "Carry-in: quota banked from the previous year, once the fisheries administration confirms it, with effect "
             "from the date it is confirmed.")
    C("2.3", "Swaps with other producer organisations, agreed by the organisation for a pool, with effect from the date "
             "agreed.")
    C("2.4", "Leases between licences, with effect from the date the lease is agreed. A lease cancelled before the end "
             "of the year is reversed with effect from the date it is cancelled.")
    C("2.5", "Landings, in live weight, counted against the licence from the day of landing. The ledger records each "
             "licence's landings for a month as one entry dated the last day of the month, posted when the "
             "administration's monthly statement arrives.")
    H("3. Quota left")
    P("A pool's quota left on a date is everything under 2.1 to 2.4 with effect on or before that date, less its "
      "landings to that date. A licence's quota left is worked out the same way.")
    H("4. The ledger")
    P("The ledger keeps every entry with the date it takes effect and the date it was posted. No entry is changed once "
      "posted; a correction is a new entry. Members can see their own licence's entries in the members' area of the "
      "website; pool totals are reported to each pool meeting.")
    H("5. Leases")
    P("A member who wants to lease haddock in or out asks the quota office, which posts the request to the members' "
      "area for five working days. A lease between licences in different pools needs the agreement of both pools' "
      "representatives. The office charges a fee of 25 pence a tonne on leases between pools; leases within a pool are "
      "free. Leases run to the end of the quota year unless cancelled by both parties.")
    H("6. Overfishing")
    P("A pool that lands more than its quota for the year pays the excess back from its quota for the following year, "
      "as the administration deducts it from the organisation. The committee may close a pool's fishing for haddock "
      "for the rest of the year when its quota left falls under 5 per cent of its allocation.")
    doc.build(st, onFirstPage=_frame(K.ORG_LTD, "Quota management rules 2026", "Sans"),
              onLaterPages=_frame(K.ORG_LTD, "Quota management rules 2026", "Sans"))


# ---------------------------------------------------------------------------------------------- the gear trial note
def write_gear_trial(path, table):
    S = styles("Sans", colors.HexColor("#2C5F2D"))
    doc = _doc(path, "Square-mesh panel trial, autumn 2025", K.ORG_LTD)
    st = [Paragraph("Square-Mesh Panel Trial, Autumn 2025: Note to Members", S["h1"]),
          Paragraph("%s, science and sustainability office, 18 December 2025." % K.ORG_LTD, S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    H = lambda t: st.append(Paragraph(t, S["h2"]))
    H("What we tried")
    P("During the October 2025 survey charter the vessel fished 24 extra pairs of tows on Skiravie Bank and Moraskie "
      "Ground: in each pair one tow with the members' standard 120 mm codend and one with the same codend carrying a "
      "3 m panel of 140 mm square mesh, towed side by side in time, at the same depth, for 60 minutes each. The extra "
      "tows are not survey stations and are not in the survey's records.")
    H("What we found")
    P("Summed over the 24 pairs, the panel let out a third of the whiting and close to half of the haddock under 30 cm, "
      "for a loss of about one marketable haddock in fourteen by weight.")
    st.append(_table(S, [["Species", "Standard codend (kg)", "With panel (kg)", "Change"]] + table, (50, 38, 34, 24),
                     right=(1, 2, 3)))
    H("What happens next")
    P("The committee will consider at its March 2026 meeting whether to ask members to fit the panel on the six grounds "
      "from 2027. Members who want to try the panel before then can borrow one of the two the organisation holds.")
    doc.build(st, onFirstPage=_frame(K.ORG_LTD, "Square-mesh panel trial 2025", "Sans"),
              onLaterPages=_frame(K.ORG_LTD, "Square-mesh panel trial 2025", "Sans"))


# ---------------------------------------------------------------------------------------------- the contents list
def write_contents(path, rows):
    w = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    lines = ["%s: evidence pack for the management committee, ground closure 2027" % K.ORG_LTD,
             "Assembled by the science and sustainability office, 6 November 2026. Every file is the organisation's own",
             "record or document, for the committee's and members' use only.", ""]
    for k, r in enumerate(rows):
        lines.append("  ".join(c.ljust(w[i]) for i, c in enumerate(r)).rstrip())
        if k == 0:
            lines.append("  ".join("-" * w[i] for i in range(len(w))))
    open(path, "w", encoding="utf-8", newline="\r\n").write("\n".join(lines) + "\n")
