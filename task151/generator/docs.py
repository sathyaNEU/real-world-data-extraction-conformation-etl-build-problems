"""The documents: the club's accounting policy FIN-14 and its close-file working paper CF-14.4, the five term sheets,
the League's injured-list rules excerpt, the statistics feed notes and the finance close-file index of the December 11
pull."""
from __future__ import annotations

import datetime as dt
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import common as K
import records as R

F_FIN14 = "FIN-14_player_compensation_accounting_policy.pdf"
F_TERMS = "term_sheets_2027_free_agent_hitters.pdf"
F_ILRULES = "league_rules_art22_injured_lists_excerpt.pdf"
F_NOTES = "lsf_feed_notes.txt"
F_MANIFEST = "ral_close_file_index_2026-12-11.csv"
F_WP = "CF-14.4_look-back_working_paper.pdf"

BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9.6, leading=12.6, alignment=TA_LEFT, spaceAfter=4.5)
HEAD = ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=10, leading=13, spaceBefore=6, spaceAfter=2.5,
                      keepWithNext=1)
TITLE = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=3)
SMALL = ParagraphStyle("small", fontName="Helvetica", fontSize=8.4, leading=10.4, textColor=colors.HexColor("#333333"))
CELL = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.8, leading=11)
CELLB = ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=8.8, leading=11)


def _pdf(path, story, title, author, stamp, footer, producer):
    def on_page(c, d):
        c.setFont("Helvetica", 7.6)
        c.drawString(0.85 * inch, 0.5 * inch, footer)
        c.drawRightString(7.65 * inch, 0.5 * inch, "Page %d" % d.page)

    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.8 * inch, title=title, author=author, subject=title,
                            creator=author, producer=producer, invariant=1)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    K.fix_pdf(path, stamp, producer)


# ------------------------------------------------------------------------------------------------------------ FIN-14
def write_fin14(out):
    s = [Paragraph(K.CLUB_LEGAL.upper() + " (RALEIGH OAKS)", SMALL), Paragraph("Finance Department", SMALL),
         Spacer(1, 6), Paragraph("Accounting Policy FIN-14: Player Compensation", TITLE),
         Paragraph("Effective January 1, 2025, as revised November 12, 2026; supersedes FIN-14 of March 2019. Policy "
                   "owner: Controller. Approved by the Audit Committee, November 12, 2026.", SMALL), Spacer(1, 6)]
    secs = [
        ("1. Scope", [
            "This policy sets how the Club records the cost of its players' contracts: salaries, signing bonuses, "
            "deferred compensation, playing-time bonuses and award bonuses. It applies to every major league and minor "
            "league player contract the Club signs or acquires."]),
        ("2. Salaries", [
            "Salary is expensed in the championship season for which it is paid, in the payroll periods in which it is "
            "earned. Salary continuation for a player on an injured list is salary."]),
        ("3. Signing bonuses and deferred compensation", [
            "3.1 A signing bonus is recorded as a prepaid asset when it becomes payable and is expensed on a "
            "straight-line basis over the guaranteed seasons of the contract.",
            "3.2 Salary deferred under a contract is expensed in the season in which it is earned at its present value, "
            "discounted at the Club's incremental borrowing rate at the date the contract is signed. The discount is "
            "accreted to interest expense until payment."]),
        ("4. Playing-time bonuses", [
            "4.1 This section applies to bonuses payable for reaching a threshold of playing time in a championship "
            "season: plate appearances, games played, games started, innings pitched, relief appearances and days on "
            "the Active List.",
            "4.2 When a contract is signed, the Club accrues each such bonus at its expected amount: the amount of the "
            "bonus multiplied by the probability, assessed at the date the contract is signed, that the player reaches "
            "its threshold in the championship season for which the bonus is payable.",
            "4.3 The probability is assessed on the footing that the contract stands as signed through the season: "
            "the player is not traded or released and the contract is not renegotiated, and he is in the role the "
            "Club plans for him at the date of signing. His own health and playing time are not assumed: the chance "
            "that he is hurt, or plays less than planned, is part of the probability.",
            "4.4 The Controller chooses the basis for the probabilities by a look-back: each basis considered is "
            "tried on the championship seasons before the contract is signed, using only what was published before "
            "each began, and the Club uses the basis the look-back scores best. The hitters tried, the thresholds and "
            "the score are set in close-file working paper CF-14.4, kept in the close file for the auditors.",
            "4.5 The accrual is remeasured at each quarter end during the season and settled at the end of the season "
            "against the bonuses earned."]),
        ("5. Award bonuses", [
            "Bonuses for All-Star selection, league awards and postseason honors are not accrued. They are expensed in "
            "the period in which the selection or award is announced."]),
        ("6. Documentation", [
            "Each accrual under section 4 is documented in the close file of the period in which the contract is "
            "signed: the contract's bonus terms, the expected amount of each bonus, the basis for each probability and "
            "the look-back that chose it. Expected amounts are carried unrounded; a total is the sum of the unrounded "
            "amounts, rounded only where it is reported. Baseball Operations provides the Club's plans for the player; "
            "the Controller is responsible for the estimate."]),
    ]
    for h, paras in secs:
        s.append(Paragraph(h, HEAD))
        for p in paras:
            s.append(Paragraph(p, BODY))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Revision history: March 2019, issued. January 2025, section 4 added (playing-time bonuses "
                       "were previously expensed when earned); section 3.2 discount rate basis changed. November 2026, "
                       "4.3 restated and 4.4 added (the look-back, after the auditors' review of the 2025 close, with "
                       "working paper CF-14.4); 4.4 renumbered 4.5; section 6 extended.", SMALL))
    _pdf(os.path.join(out, F_FIN14), s, "FIN-14 Player Compensation", K.PEOPLE["controller"],
         dt.datetime(2026, 11, 13, 9, 41), "Triangle Baseball Club, LLC: Finance policies", "Finance policy library")


# ------------------------------------------------------------------------------------------- working paper CF-14.4
def write_working_paper(out):
    s = [Paragraph(K.CLUB_LEGAL.upper() + " (RALEIGH OAKS)", SMALL), Paragraph("Finance Department: close file", SMALL),
         Spacer(1, 6), Paragraph("Working paper CF-14.4: the look-back for plate-appearance bonuses", TITLE),
         Paragraph("Standing paper under Accounting Policy FIN-14 4.4. Prepared by %s, Controller, November 12, 2026, "
                   "after the auditors' review of the 2025 close." % K.PEOPLE["controller"], SMALL), Spacer(1, 6)]
    paras = [
        ("1. Seasons", "Each basis considered is applied to each of the four championship seasons before the contract "
                       "is signed, as if that season were still to be played and using only what was published before "
                       "it began."),
        ("2. Hitters", "The basis is tried on every hitter in a starting lineup of the January 31 depth charts for that "
                       "season who made at least 100 plate appearances in each of the two seasons before it, counting "
                       "his plate appearances for every club he played for."),
        ("3. Thresholds and score", "For each such hitter the basis gives the probability that he makes at least 450, "
                                    "500, 550, 600 and 650 plate appearances in the season. The score is the average, "
                                    "over every hitter, season and threshold, of the squared difference between that "
                                    "probability and 1 where he reached the threshold or 0 where he did not."),
        ("4. Use", "The Club uses the basis with the lowest average. The scores of every basis considered are kept with "
                   "the accrual in the close file of the period in which the contract is signed (FIN-14 6)."),
    ]
    for h, p in paras:
        s.append(Paragraph(h, HEAD))
        s.append(Paragraph(p, BODY))
    _pdf(os.path.join(out, F_WP), s, "CF-14.4 Look-back", K.PEOPLE["controller"], dt.datetime(2026, 11, 13, 9, 52),
         "Triangle Baseball Club, LLC: Finance close file", "Finance policy library")


# ------------------------------------------------------------------------------------------------------- term sheets
def money(x):
    return "${:,.0f}".format(x)


def lines_text(b):
    amt = b[0][0]
    ts = [T for _, T in b]
    return "%s each for %s and %d plate appearances" % (money(amt), ", ".join(str(t) for t in ts[:-1]), ts[-1])


def write_term_sheets(L, out):
    s = [Paragraph("RALEIGH OAKS: SUMMARY OF TERMS, FREE-AGENT HITTERS SIGNED FOR 2027", TITLE),
         Paragraph("Prepared by Baseball Operations for Finance from the executed Uniform Player Contracts. Each "
                   "contract was approved by the League office on the date signed.", SMALL), Spacer(1, 8)]
    for k in K.SIGN_ORDER:
        c = K.SIGNINGS[k]
        p = L.players[k]
        yrs = c["years"]
        term = "%d (one season)" % yrs[0] if yrs[0] == yrs[1] else "%d to %d (%d seasons)" % (yrs[0], yrs[1],
                                                                                            yrs[1] - yrs[0] + 1)
        sal = "; ".join("%d %s" % (y, money(v)) for y, v in sorted(c["salary"].items()))
        if "deferred" in c:
            sal += " (of which %s in each of %s deferred, payable in equal installments 2033 to 2037)" % (
                money(list(c["deferred"].values())[0]), " and ".join(str(y) for y in sorted(c["deferred"])))
        rows = [
            [Paragraph("Player", CELLB), Paragraph("%s (%s, bats %s, born %s)" % (
                p.name, c["pos"], p.bats, p.born.strftime("%B %-d, %Y")), CELL)],
            [Paragraph("Signed", CELLB), Paragraph(c["signed"].strftime("%B %-d, %Y"), CELL)],
            [Paragraph("Term", CELLB), Paragraph(term, CELL)],
            [Paragraph("Salary", CELLB), Paragraph(sal, CELL)],
            [Paragraph("Signing bonus", CELLB), Paragraph("%s, payable within 30 days of approval" % money(
                c["signing_bonus"]), CELL)],
            [Paragraph("Plate-appearance bonuses", CELLB), Paragraph(
                "2027 season: %s. No plate-appearance bonuses in later seasons." % lines_text(c["bonus"]) if
                yrs[1] > 2027 else "2027 season: %s." % lines_text(c["bonus"]), CELL)],
            [Paragraph("Plate appearances", CELLB), Paragraph(
                "Plate appearances the Player makes for the Club in the 2027 championship season, as the League's "
                "official statistics count them. Postseason and rehabilitation-assignment plate appearances are not "
                "counted. Each bonus is earned once, when the Player reaches its threshold.", CELL)],
        ]
        t = Table(rows, colWidths=[1.55 * inch, 5.2 * inch])
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EFEFEF")),
                               ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
        s.append(KeepTogether([t, Spacer(1, 10)]))
    _pdf(os.path.join(out, F_TERMS), s, "Summary of terms, 2027 free-agent hitters", K.PEOPLE["agm"],
         dt.datetime(2026, 12, 10, 16, 48), "Raleigh Oaks Baseball Operations. Confidential.", "Baseball Operations")


# ---------------------------------------------------------------------------------------------- injured-list rules
def write_il_rules(out):
    s = [Paragraph("LEAGUE RULES (2024 EDITION), ARTICLE 22: INJURED LISTS (EXCERPT)", TITLE),
         Paragraph("Issued by the League office. Sections 22.1 to 22.9 as in force for the 2024, 2025 and 2026 "
                   "championship seasons.", SMALL), Spacer(1, 6)]
    secs = [
        ("22.1 Lists", "A Club may place a Player who is unable to play because of injury or illness on the 10-day "
                       "Injured List (the 15-day Injured List for a pitcher) or the 60-day Injured List, and a Player "
                       "with a concussion on the 7-day Injured List. A placement takes effect on the date the Club "
                       "designates, which may be up to three days before the date of the transaction placing the "
                       "Player on the list."),
        ("22.2 Minimum periods", "A Player may not be reinstated from the 7-day, 10-day, 15-day or 60-day Injured List "
                                 "until seven, ten, fifteen or sixty days after his placement takes effect."),
        ("22.3 Transfers", "A Player on the 7-day, 10-day or 15-day Injured List may be transferred to the 60-day "
                           "Injured List. A transfer does not end the Player's placement."),
        ("22.4 Rehabilitation assignments", "A Player on an Injured List may be assigned to a minor league club for "
                                            "rehabilitation for up to 20 days. The assignment does not end his "
                                            "placement."),
        ("22.5 Assignment of contracts", "A Player's contract may be assigned to another Club while he is on an "
                                         "Injured List. He remains on the Injured List with the assignee Club."),
        ("22.6 Reinstatement", "A placement ends when the Player is reinstated to the Active List. A Player on an "
                               "Injured List at the end of the championship season is reinstated within five days "
                               "after the last game of the World Series."),
        ("22.7 Days on an Injured List", "Days on an Injured List are counted from the date the placement takes "
                                         "effect through the day before the Player is reinstated."),
        ("22.8 Other lists", "The paternity list, the bereavement list and the restricted list are not Injured "
                             "Lists."),
        ("22.9 Weekly report", "The League office issues an injured-list report each Monday of the championship "
                               "season. It lists every Player on an Injured List that day, the list, the date of the "
                               "transaction that placed him on it and the first date on which he may be reinstated."),
    ]
    for h, p in secs:
        s.append(Paragraph(h, HEAD))
        s.append(Paragraph(p, BODY))
    _pdf(os.path.join(out, F_ILRULES), s, "League Rules Article 22 excerpt", "League office",
         dt.datetime(2024, 2, 20, 9, 0), "League Rules, 2024 edition. Article 22 (excerpt).", "League office")


# ------------------------------------------------------------------------------------------------------- feed notes
def write_feed_notes(out):
    txt = """LEAGUE STATISTICS FEED (LSF): BATTING LINES, PLAYER ID CROSSWALK, CLUB DIRECTORY, CALENDAR
Field notes for the extracts below. Issued by League Statistics, revised February 2025.

1. BATTING LINES
One line per player per game in which he appeared as a batter, a pinch hitter or a defensive substitute, for every
championship-season game. Postseason, exhibition and minor league games are not in the feed. A suspended game is one
game: its lines carry the date it began, with the date it was completed in COMPL_DT (legacy) or resumed_date
(platform). A doubleheader is two games on one date.

1.1 Legacy layout, seasons 2021 to 2024 (lsf_batting_2021_2024.txt)
Pipe-delimited, CRLF line ends, dates MM/DD/YYYY. The legacy statistics system was retired after the 2024 season.
  GAME_ID      home club legacy code, date YYYYMMDD and GAME_CT
  GAME_CT      0 single game; 1 and 2 first and second games of a doubleheader
  HOME_CD, TEAM_CD, OPP_CD   legacy club codes (see the club directory)
  PLAYER_CD    legacy player code
  LINEUP       batting-order position, 1 to 9
  SEQ          1 the player who started in that position; 2, 3, ... players who entered later, in order
  POS          position code: 1 P, 2 C, 3 1B, 4 2B, 5 3B, 6 SS, 7 LF, 8 CF, 9 RF, 10 DH, 11 PH
  AB R H D2 T3 HR RBI BB SO HBP SH SF CI   batting counts (D2 doubles, T3 triples, SH sacrifice bunts, SF sacrifice
               flies, CI reached on catcher's interference)
  The legacy layout has no plate-appearance field. Plate appearances are AB + BB + HBP + SH + SF + CI.

1.2 Platform layout, seasons 2025 and 2026 (lsf_batting_2025_2026.csv)
Comma-separated, ISO dates.
  game_pk          League game ID
  official_date    date the game began
  game_number      1, or 2 for the second game of a doubleheader
  venue_team_id, team_id, opponent_team_id   platform team IDs (see the club directory)
  player_id        League player ID
  batting_order    batting-order position x 100 + entry sequence: 100 to 900 the starters, 301 the first player to
                   enter in the third position after its starter, and so on
  is_substitute    true for a player who entered after the first pitch
  position         position at entry (C, 1B, 2B, 3B, SS, LF, CF, RF, DH, PH)
  pa               plate appearances
  ab r h doubles triples hr rbi bb so hbp sac_bunts sac_flies catchers_interference   batting counts
  resumed_date     completion date of a suspended game

2. PLAYER ID CROSSWALK (lsf_player_id_crosswalk.csv)
Built at the platform change: every legacy player code that appears in the 2021 to 2024 batting lines, with the League
player ID assigned to the same player. Names are as the legacy system held them (no accents).

3. CLUB DIRECTORY (league_club_directory.csv)
The 30 clubs: platform team ID, League abbreviation, legacy statistics code, name and Triple-A affiliate.

4. CALENDAR (league_calendar_2021_2027.csv)
Opening Day, the All-Star break and the last scheduled day of each championship season. The championship season runs
from Opening Day through the last scheduled day.
"""
    with open(os.path.join(out, F_NOTES), "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)


# ---------------------------------------------------------------------------------------------- close-file index
def write_manifest(out, rows):
    items = [
        (R.F_LEGACY, "League Statistics Feed", "Batting lines, legacy layout", "championship seasons 2021-2024"),
        (R.F_BAT, "League Statistics Feed", "Batting lines, platform layout", "championship seasons 2025-2026"),
        (R.F_XWALK, "League Statistics Feed", "Legacy player code to League player ID", "players in the 2021-2024 lines"),
        (R.F_CLUBS, "League Statistics Feed", "Club directory", "30 clubs"),
        (R.F_CAL, "League Statistics Feed", "Season calendar", "2021-2027"),
        (F_NOTES, "League Statistics", "Field notes for the batting lines, crosswalk, directory and calendar", ""),
        (R.F_TRANS, "League Statistics Feed", "Transaction wire", "2024-01-01 to 2026-12-11"),
        (R.F_ILREP, "League office", "Weekly injured-list report (Mondays)", "championship seasons 2024-2026"),
        (F_ILRULES, "League office", "League Rules Article 22 (excerpt)", ""),
        (R.F_SCHED27, "League office", "2027 championship-season schedule (published August 2026)", "2027"),
        (R.F_DC, K.VENDOR, "Projected depth charts, January 31 snapshots", "2021-2026"),
        (R.F_PROJ, K.VENDOR, "Preseason hitter projections (2027 preliminary, December 1, 2026)", "2022-2027"),
        (R.F_DC27, "Baseball Operations", "2027 depth chart", "as of 2026-12-10"),
        (F_TERMS, "Baseball Operations", "Summary of terms, five free-agent hitters", "signed 2026-11-24 to 2026-12-10"),
        (R.F_REG, "Finance / Baseball Operations", "Player contract register (extract)", "2024-2026 seasons"),
        (R.F_PAY, "HRIS payroll", "Player earnings register", "pay dates 2023-01-01 to 2026-12-11"),
        (R.F_HRIS, "HRIS", "Legacy employee number map (January 2025 migration)", "players"),
        (R.F_CODES, "HRIS payroll", "Earning codes, legacy and HRIS", ""),
        (F_FIN14, "Finance", "Accounting Policy FIN-14", "effective 2025-01-01"),
        (F_WP, "Finance", "Working paper CF-14.4, the FIN-14 4.4 look-back", "standing, from 2026-11-12"),
    ]
    out_rows = []
    for f, src, what, cover in items:
        out_rows.append([f, src, what, cover, rows.get(f, ""), "2026-12-11"])
    out_rows.append([F_MANIFEST, "Finance", "This index", "", "", "2026-12-11"])
    K.write_csv(os.path.join(out, F_MANIFEST), ["file", "source", "contents", "coverage", "rows", "pulled"], out_rows)
