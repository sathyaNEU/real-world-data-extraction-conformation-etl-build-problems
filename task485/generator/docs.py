"""The pack's documents: the Cabinet Office's Population Policy schedule of sector allowances, the Statistics Unit's
methods note for its long-term migration figures, and the Population Office's extract specification."""
import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import golden as G
import world as W

reportlab.rl_config.invariant = 1
STY = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=STY["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.8, spaceAfter=6)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10)
H = ParagraphStyle("h", parent=STY["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
T = ParagraphStyle("t", parent=STY["Title"], fontName="Helvetica-Bold", fontSize=14, spaceAfter=10, alignment=0)

# the Policy's allowances by year to 30 June, and the 2026 work permit quotas
ALLOW = {"HOS": (225, 230, 235, 240), "AGR": (105, 110, 110, 115), "CON": (205, 210, 215, 220),
         "FIN": (340, 350, 360, 370), "HSC": (410, 420, 430, 440), "RET": (165, 170, 170, 175),
         "DIG": (185, 190, 200, 210), "OTH": (290, 300, 305, 310)}
QUOTA26 = {"HOS": 540, "AGR": 170, "CON": 480, "FIN": 300, "HSC": 760, "RET": 430, "DIG": 205, "OTH": 250}
assert all(ALLOW[s][1] == G.ALLOWANCE[s] for s in G.ALLOWANCE)


def _pdf(path, title, story, author, org):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=17 * mm,
                            bottomMargin=17 * mm, title=title, author=author, creator=org, subject=title, producer=org)

    def footer(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.drawString(18 * mm, 10 * mm, org + "  |  " + title)
        c.drawRightString(A4[0] - 18 * mm, 10 * mm, "%d" % d.page)
        c.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def P(text, style=BODY):
    return Paragraph(text, style)


def _cell(text, size=7.8):
    return Paragraph(text, ParagraphStyle("c", parent=SMALL, fontSize=size, leading=size + 2.2))


def _table(rows, widths=None, size=8.2, wrap=False):
    if wrap:
        rows = [[_cell(str(c)) if i else c for i, c in enumerate(r)] if k else r for k, r in enumerate(rows)]
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", size), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    return t


def policy(path):
    names = dict(W.SECTORS)
    allow = [["Code", "Employment sector", "2024-25", "2025-26", "2026-27", "2027-28"]]
    allow += [[s, names[s]] + ["%d" % v for v in ALLOW[s]] for s in W.SECT]
    quota = [["Code", "Employment sector", "New work permits, 2026"]] + [[s, names[s], "%d" % QUOTA26[s]] for s in W.SECT]
    s = [P("Population Policy 2024 to 2028: sector allowances and work permit quotas", T),
         P("Cabinet Office, Population Policy Unit. Approved by the Council of Ministers on 26 March 2024 and published "
           "9 April 2024. Reference CO/POP/24/03.", SMALL),
         P("1. Purpose", H),
         P("The Population Policy 2024 to 2028 manages the island's growth through the work permit system, towards a "
           "resident population of no more than 90,000 in 2030. Long-term immigration for work is the part of that growth "
           "the Council of Ministers can steer, and the Policy steers it sector by sector: each employment sector has an "
           "annual allowance of long-term immigration, and the number of new work permits the Council allows a sector each "
           "calendar year follows how the sector stood against its allowance."),
         P("2. The allowances", H),
         P("Table 1 sets each sector's allowance of long-term immigration for each year to 30 June, in persons."),
         _table(allow, widths=[14 * mm, 70 * mm, 19 * mm, 19 * mm, 19 * mm, 19 * mm]),
         Spacer(1, 6),
         P("3. The October review", H),
         P("3.1 Each October the Statistics Unit certifies to the Council of Ministers its provisional long-term "
           "immigration by employment sector for the year to the previous 30 June, compiled on its methods for provisional "
           "migration statistics."),
         P("3.2 Where a sector's provisional long-term immigration exceeds its allowance for that year, the Council reduces "
           "the sector's work permit quota for the next calendar year by the excess. A sector at or below its allowance "
           "keeps its quota."),
         P("3.3 The Unit's final figures for a year, published a year after its provisional figures, do not reopen a quota "
           "once it has been set."),
         P("4. Definitions", H),
         P("Long-term immigration and the employment sectors are as the Statistics Unit defines them for its migration "
           "statistics. The sectors are those of the 2026 sector list, which the Unit applies to earlier registrations "
           "through the 2014 activity codes."),
         P("5. The 2026 quotas", H),
         P("Table 2 gives the new work permits each sector may be granted in calendar 2026, set by the Council on 16 October "
           "2025 on the Unit's provisional figures for 2024-25."),
         _table(quota, widths=[14 * mm, 70 * mm, 40 * mm]),
         Spacer(1, 8),
         P("Population Policy Unit, Cabinet Office. Contact: Melanie Hilton, Head of Population Policy.", SMALL)]
    _pdf(path, "Population Policy 2024 to 2028: sector allowances", s, "Population Policy Unit", "Cabinet Office")


def methods(path):
    s = [P("Long-term migration from the Population Register: methods for the provisional and final figures", T),
         P("Esklett Statistics Unit. Methods note, 2026 edition, published 1 September 2026. Jean Grant, Chief "
           "Statistician.", SMALL),
         P("1. What is counted", H),
         P("1.1 Long-term immigration for a year to 30 June counts the arrivals in the year whose stay on the island lasts "
           "twelve months or more. An arrival belongs to the year in which its arrival date falls. A stay lasts twelve "
           "months or more when its leaving date falls on or after the first anniversary of its arrival date (1 March for "
           "an arrival on 29 February), or when the person is still on the island on that anniversary. The definition "
           "follows the United Nations recommendations on statistics of international migration, under which a long-term "
           "migrant is a person who moves to a country other than that of usual residence for a period of at least a year."),
         P("1.2 The measure counts stays, not people. Each stay is classified on its own length, whatever the person's "
           "earlier stays: a person who leaves and comes back begins a new stay with a new arrival registration, and a "
           "stay of twelve months or more counts once, in the year of its arrival."),
         P("1.3 The figures cover arrivals registered for work. A stay's sector is the employment sector of the activity "
           "declared at its arrival registration. Registrations from 1 January 2026 carry the 2026 sector list and earlier "
           "registrations a 2014 activity code; each 2014 code belongs to one 2026 sector (the Unit's sector "
           "classification, 2026 edition)."),
         P("2. Final figures", H),
         P("Every arrival in a year has passed its first anniversary by the following 30 June, and the year's figures are "
           "final from the register's extract after that date. Final figures are published in whole persons."),
         P("3. Provisional figures", H),
         P("3.1 Each October the Unit publishes provisional figures for the year to the previous 30 June from the register "
           "as it stood at 31 August. The Population Office's extract of 30 September holds every stay registered by then "
           "with an arrival date on or before 31 August, and the leaving notices received by 30 September for departures "
           "on or before 31 August."),
         P("3.2 A stay that had ended before its first anniversary, or that had reached its first anniversary, by 31 August "
           "is counted as it is. A stay still open at 31 August that had not yet reached its first anniversary is counted "
           "at its chance of reaching it, estimated from the arrivals of the year before, all of whose stays are resolved. "
           "For the 2025-26 figures the year before is the year to 30 June 2025. A sector's provisional figure is the "
           "number of its stays counted as long-term plus the sum of those chances."),
         P("3.3 The Unit estimates those chances in the way that would have predicted them best a year earlier. "
           "Estimated in that way from the arrivals of the year to 30 June 2024, the chances given to the arrivals of "
           "the year to 30 June 2025 that were still open on 31 August 2025, as the extract of 30 September 2025 held "
           "them, should come closer than any other way to whether each of those stays went on to reach its first "
           "anniversary, judged "
           "by the mean of the squared differences between each chance and the outcome (one for a stay that reached its "
           "anniversary, nought for one that did not)."),
         P("3.4 Provisional figures are published rounded to the nearest 50, because each rests on an estimate. The "
           "comparison with a sector's Population Policy allowance is made on the unrounded figure."),
         P("4. The back series", H),
         P("The register-based series begins with the year to 30 June 2024, the first year whose arrivals were all "
           "registered in the current system. The Unit is compiling final figures for the years to 30 June 2019 to 2023 on "
           "the same definitions from the legacy register's archive and the current system's extract, for publication in "
           "whole persons with the 2025-26 provisional figures."),
         P("5. Revisions and the release timetable", H),
         P("Provisional figures are replaced by final figures a year later, when every stay in the year has passed its "
           "first anniversary. Between the two, the register enters the leaving notices that arrive late and the open "
           "stays resolve, and the Unit publishes each sector's revision with the final figures. Final figures can "
           "themselves move by a few persons when a later extract carries a leaving notice received after the extract "
           "they were compiled from; the Unit revises a published final figure only when its sector total moves by "
           "more than 2 per cent."),
         _table([["Release", "Extract", "Published"],
                 ["Provisional 2024-25", "30 September 2025", "16 October 2025"],
                 ["Final 2023-24", "30 September 2025", "16 October 2025"],
                 ["Provisional 2025-26", "30 September 2026", "8 October 2026"],
                 ["Final 2024-25", "30 September 2026", "8 October 2026"],
                 ["Back series 2018-19 to 2022-23", "30 September 2026", "8 October 2026"]],
                widths=[60 * mm, 45 * mm, 45 * mm]),
         Spacer(1, 6),
         P("6. Sources", H),
         P("The Population Register is kept by the Population Office under the Population Register Act 2013. Its current "
           "system replaced the legacy register on 13 March 2023; the Office's extract specification describes both and the "
           "crosswalk between their registration numbers."),
         Spacer(1, 8),
         P("Esklett Statistics Unit, Cabinet Office Buildings, Port Esklett. Population and migration statistics: "
           "Jean Grant.", SMALL)]
    _pdf(path, "Long-term migration from the Population Register: methods", s, "Esklett Statistics Unit",
         "Esklett Statistics Unit")


def specification(path):
    cur = [["Field", "Content"],
           ["reg_no", "the person's registration number"],
           ["stay_ref", "the stay's reference"],
           ["record_origin", "ARRIVAL, a stay registered in the current system; TRANSFER, a stay carried from the legacy "
                             "register at the move"],
           ["arrival_date", "the date the stay began; for a TRANSFER record, the date its legacy record was "
                            "registered"],
           ["registered_on", "the date of the arrival registration; for a TRANSFER record, the date of the move"],
           ["activity_code", "the activity on the record: a 2014 activity code for records registered before 1 January "
                             "2026, a 2026 sector code from then; for a TRANSFER record, the activity its legacy record "
                             "held on 12 March 2023"],
           ["parish_code", "the parish of the address given at registration (parish_codes.csv)"],
           ["sex, birth_year", "as registered"],
           ["nationality", "as registered, ISO 3166 alpha-3"],
           ["leaving_date", "the date of leaving the leaving notice gives"],
           ["notice_received", "the date the leaving notice was received"]]
    arc = [["Field", "Content"],
           ["LEGACY_NO", "the legacy registration number"],
           ["DATE_OF_ARRIVAL", "the date of arrival declared on the registration"],
           ["DATE_REGISTERED", "the date the registration was made"],
           ["ACTIVITY", "the activity declared on the registration (2014 activity codes)"],
           ["PARISH", "the parish of the address given, as the parish office coded it"],
           ["SEX, YOB, NATIONALITY", "as registered"],
           ["DATE_OF_LEAVING", "the date of leaving the leaving notice gave"],
           ["CLOSURE", "LEFT, closed on a leaving notice; TRANSFERRED, open on 12 March 2023 and carried into the "
                       "current system"],
           ["CLOSED_ON", "the date the record was closed"]]
    s = [P("Population Register: extract specification for the Statistics Unit", T),
         P("Population Office, Cabinet Office. Version 3, 1 September 2026. Gordon Hope, Population Register Manager.",
           SMALL),
         P("1. The register", H),
         P("Everyone who comes to Esklett to live or work registers with the Population Office within 14 days of arriving "
           "(within three months under the legacy register's rules) and gives a leaving notice within 14 days of leaving. "
           "Registrations and notices are taken at the parish offices and online. The legacy register ran from 1 January "
           "2014 to 12 March 2023, and the current system has run since 13 March 2023."),
         P("2. The move to the current system", H),
         P("On 13 March 2023 each legacy registration number was issued a current registration number, listed in "
           "registration_number_crosswalk_2023.csv, and each record open on the legacy register was carried into the "
           "current system as a TRANSFER record under it. The legacy register closed its open records on 12 March 2023 "
           "with the closure TRANSFERRED; the legacy archive keeps each record as it was registered."),
         P("3. The current system's extract", H),
         P("population_register_extract_20260930.csv holds every stay with an arrival date on or before 31 August 2026, "
           "with the leaving notices received by 30 September 2026 for departures on or before 31 August 2026, one row a "
           "stay. A stay with no leaving notice in the extract has a blank leaving_date. A person who leaves and returns "
           "keeps their registration number, and each return is a new stay with its own stay_ref. Dates are ISO 8601."),
         _table(cur, widths=[30 * mm, 132 * mm], wrap=True),
         P("4. The legacy register's archive", H),
         P("population_register_legacy_archive_2014_2023.csv holds one row for each record the legacy register held "
           "between 1 January 2014 and 12 March 2023. Dates are written day, month, year."),
         _table(arc, widths=[38 * mm, 124 * mm], wrap=True),
         P("5. The crosswalk", H),
         P("registration_number_crosswalk_2023.csv lists each legacy registration number (legacy_no) with the current "
           "registration number issued for it at the move (reg_no) and the date of issue."),
         P("6. Code lists", H),
         P("Activity and sector codes are those of the Statistics Unit's sector classification, 2026 edition "
           "(sector_classification_2026.json). Parish codes are in parish_codes.csv: Haldervoe and Ivarsby merged on "
           "1 April 2025, and records registered before then keep the parish code they were registered under."),
         Spacer(1, 8),
         P("Population Office, Cabinet Office. Register queries: Gordon Hope, Population Register Manager.", SMALL)]
    _pdf(path, "Population Register: extract specification", s, "Population Office", "Cabinet Office")
