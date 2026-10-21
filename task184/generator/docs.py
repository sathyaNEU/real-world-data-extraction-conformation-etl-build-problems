"""The pack's documents: the force's recording standard extract, the 2027 tasking contract with its slot schedule
and class schedule, the records management extract notes, and the system's data dictionary."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                   # noqa: E402
from reportlab.lib.pagesizes import A4                                             # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import mm                                                 # noqa: E402
from reportlab.pdfbase import pdfmetrics                                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                       # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import places as PL    # noqa: E402
import world as W      # noqa: E402

RULES = "kcp_crime_recording_standard_extract.pdf"
CONTRACT = "harbourgate_patrol_tasking_contract_2027.pdf"
SCHEDULE = "harbourgate_tasking_schedule.csv"
NOTES = "kcp_rms_extract_notes.md"
DICTIONARY = "kcp_rms_data_dictionary.csv"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
INK, GREY, RULE = colors.HexColor("#1b2733"), colors.HexColor("#59636f"), colors.HexColor("#97a1ab")

BODY = ParagraphStyle("b", fontName="Serif", fontSize=10.2, leading=13.8, textColor=INK, spaceAfter=5)
CLAUSE = ParagraphStyle("c", parent=BODY, leftIndent=26, firstLineIndent=-26)
H1 = ParagraphStyle("h1", fontName="Serif-B", fontSize=13.6, leading=17, textColor=INK, spaceAfter=3)
H2 = ParagraphStyle("h2", fontName="Serif-B", fontSize=10.6, leading=14, textColor=INK, spaceBefore=9, spaceAfter=3)
META = ParagraphStyle("m", fontName="Serif", fontSize=8.6, leading=11, textColor=GREY, spaceAfter=9)
CELL = ParagraphStyle("cell", fontName="Sans", fontSize=8.4, leading=10.2, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Sans-B")


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                             bottomMargin=18 * mm, title=title, author=author, subject="", creator="", producer="")


def _frame(left, right, foot):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.4)
        canvas.drawString(22 * mm, A4[1] - 12 * mm, left)
        canvas.drawRightString(A4[0] - 22 * mm, A4[1] - 12 * mm, right)
        canvas.setFont("Sans", 7.0)
        canvas.drawString(22 * mm, 10 * mm, foot)
        canvas.drawRightString(A4[0] - 22 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(rows, widths, head=True):
    data = [[Paragraph(str(c), CELLB if (head and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1 if head else 0)
    style = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.6),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6), ("LINEBELOW", (0, 0), (-1, -2), 0.3, RULE)]
    if head:
        style += [("LINEBELOW", (0, 0), (-1, 0), 0.7, INK)]
    t.setStyle(TableStyle(style))
    return t


RULES_CLAUSES = [
    ("2  When an offence is recorded", [
        "2.1  An offence is recorded as soon as the reporting officer is satisfied, on the balance of probability, "
        "that the circumstances as reported amount to a notifiable offence and that no credible evidence to the "
        "contrary exists. The record is made on the day that test is met, which may be later than the day of the "
        "report and later again than the day of the occurrence.",
        "2.2  One offence is recorded for each victim of each offence class in each separate incident. Where a "
        "single incident gives rise to offences of more than one class, each class is recorded separately.",
        "2.3  The recorded date of an offence is the date on which it occurred, not the date on which it was "
        "reported or recorded, and remains so when the two fall in different recording periods.",
    ]),
    ("3  Occurrence date and time", [
        "3.1  Where the time an offence occurred is known, it is recorded as that time.",
        "3.2  Where the time an offence occurred is not known, the occurrence is recorded as the earliest and the "
        "latest time at which it can have occurred, taken from the account of the person reporting it. Both are "
        "recorded; neither is to be left blank, and neither is to be amended to the other.",
    ]),
    ("4  Classification", [
        "4.1  An offence is classified by the Home Office class of the principal offence disclosed by the "
        "circumstances, on the information available when the record is made.",
        "4.2  A class is not changed by the outcome of an investigation unless the circumstances as recorded are "
        "found to have been wrong.",
    ]),
    ("7  Location", [
        "7.1  The location of an offence is recorded as the place at which it occurred, to the address held in the "
        "corporate street gazetteer where one applies.",
        "7.2  A location code is entered for every offence falling within an area subject to a tasking agreement. "
        "For all other offences the location code is entered where the address is known at the time of recording.",
    ]),
]

CONTRACT_CLAUSES = [
    ("1  The agreement", [
        "1.1  This agreement is between the %s and %s for the provision of a hotspot patrol in the Harbourgate "
        "quarter for the 2027 season." % (W.PARTNERSHIP, W.FORCE),
        "1.2  The 2027 season runs from 1 April 2027 to 30 September 2027 inclusive.",
    ]),
    ("2  What is bought", [
        "2.1  The partnership buys eight patrol slots in each week of the season.",
        "2.2  A patrol slot is a period of four hours beginning at one of the times listed in the tasking schedule "
        "at Annex A, on a named day of the week. The schedule holds the whole week; the eight the partnership "
        "commissions are the same eight in every week of the season.",
        "2.3  A patrol slot is worked by two officers on foot within the quarter for the whole of the four hours.",
    ]),
    ("3  The quarter", [
        "3.1  The Harbourgate quarter is the five locations recorded in the location register published with this "
        "agreement. An offence is within the quarter if it occurred at one of those five locations.",
    ]),
    ("4  Offences covered", [
        "4.1  An offence is covered by this agreement if it is of a class listed in the schedule at Annex B, it "
        "occurred within the quarter, and it occurred while a commissioned patrol slot was being worked.",
        "4.2  Nothing in this agreement requires an offence to have been reported, recorded or detected during a "
        "patrol slot for it to be covered. The time that governs is the time the offence occurred.",
        "4.3  The classes at Annex B are those for which the partnership has agreed that visible patrol is the "
        "appropriate response. The partnership may propose a change to the schedule at the annual review.",
        "4.4  A count of the offences covered by this agreement is built from the force's record of those offences "
        "and from nothing else.",
    ]),
    ("5  Reporting", [
        "5.1  The force reports to the partnership, at the end of each month of the season, the hours worked in "
        "each commissioned slot and the offences of the Annex B classes recorded in the quarter that month.",
        "5.2  A report is made on the force's recorded data as it stands at the end of the month and is not "
        "restated afterwards.",
    ]),
    ("6  Review", [
        "6.1  The eight commissioned slots are settled at the annual review that follows the close of the "
        "preceding season, by the council committee that funds the patrol, and may not be changed inside the "
        "season.",
        "6.2  The partnership publishes the slate and the figures it rests on with the papers of the review.",
    ]),
]


def rules_pdf(path):
    d = _doc(path, "Crime Recording Standard: extract", W.FORCE)
    f = [Paragraph("Crime Recording Standard", H1),
         Paragraph("Extract: recording, occurrence date and time, classification and location. Issued to analysts "
                   "and recording staff. This extract is current at 1 January 2027.", META)]
    for head, paras in RULES_CLAUSES:
        f.append(Paragraph(head, H2))
        for p in paras:
            f.append(Paragraph(p, CLAUSE))
    d.build(f, onFirstPage=_frame(W.FORCE, "Crime Recording Standard", "Extract CRS-2027-01"),
            onLaterPages=_frame(W.FORCE, "Crime Recording Standard", "Extract CRS-2027-01"))


def contract_pdf(path):
    d = _doc(path, "Harbourgate hotspot patrol: tasking agreement 2027", W.PARTNERSHIP)
    f = [Paragraph("Harbourgate hotspot patrol", H1),
         Paragraph("Tasking agreement for the 2027 season, between %s and %s. Signed 4 December 2026."
                   % (W.PARTNERSHIP, W.FORCE), META)]
    for head, paras in CONTRACT_CLAUSES:
        f.append(Paragraph(head, H2))
        for p in paras:
            f.append(Paragraph(p, CLAUSE))
    f.append(Paragraph("Annex A  Tasking schedule", H2))
    f.append(Paragraph("The week's patrol slots. The schedule is published as a file with this agreement "
                       "(%s) and is reproduced here." % SCHEDULE, BODY))
    rows = [["Slot start", "Slot end", "Days"]]
    for h in range(0, 24, W.SLOT_H):
        rows.append(["%02d:00" % h, "%02d:00" % ((h + W.SLOT_H) % 24), "Monday to Sunday"])
    f.append(_table(rows, [30, 30, 60]))
    f.append(Spacer(1, 6))
    f.append(Paragraph("Annex B  Classes covered", H2))
    rows = [["Home Office class", "Recorded as"]]
    for c in W.CONTRACTED:
        rows.append([c, "an offence of this class recorded in the force's records management system"])
    f.append(_table(rows, [48, 78]))
    d.build(f, onFirstPage=_frame(W.PARTNERSHIP, "Tasking agreement 2027", "HG/PAT/2027"),
            onLaterPages=_frame(W.PARTNERSHIP, "Tasking agreement 2027", "HG/PAT/2027"))


def schedule_rows():
    rows = [("slot_id", "day_of_week", "slot_start_local", "slot_end_local", "hours")]
    for i, (d, h) in enumerate(W.SLOTS, start=1):
        rows.append(["S%02d" % i, W.DAYS[d], "%02d:00" % h, "%02d:00" % ((h + W.SLOT_H) % 24), W.SLOT_H])
    return rows


DICT_ROWS = [
    ("table", "column", "type", "definition"),
    ("offence", "crime_reference", "text", "the force's reference for the recorded offence, unique within the "
     "records management system"),
    ("offence", "offence_class", "text", "the Home Office class the offence is recorded under"),
    ("offence", "occurred_from", "timestamp", "the earliest time at which the offence can have occurred, as the "
     "person reporting it gave it. Where the time of occurrence is known, occurred_from and occurred_to hold that "
     "time and are equal"),
    ("offence", "occurred_to", "timestamp", "the latest time at which the offence can have occurred, as the person "
     "reporting it gave it. The system holds no time between the two, and none is derived"),
    ("offence", "reported_at", "timestamp", "when the offence was reported to the force"),
    ("offence", "location_code", "text", "the code of the registered location the offence is recorded at, from the "
     "location register. Empty where no location code was entered"),
    ("offence", "address_text", "text", "the address as entered by the recording officer, against the corporate "
     "street gazetteer where one applies"),
    ("offence", "beat_code", "text", "the neighbourhood beat the address falls in"),
    ("offence", "record_status", "text", "recorded, transferred or cancelled"),
]


def notes_md():
    m = W.MIGRATION
    p0, p1 = W.PARALLEL
    out = []
    out.append("# Harbourgate offence extract: notes\n")
    out.append("Extract run %s by the Performance and Analysis unit for the community safety partnership.\n"
               % W.AS_OF.strftime("%d %B %Y"))
    out.append("## Scope\n")
    out.append("The extract covers offences recorded against an address in Harbourgate Street, Quayside, "
               "Lamphouse Lane, Fishmarket Square or Netherbow Wynd, for the 2025 and 2026 seasons "
               "(1 April to 30 September). It was pulled on the street name, so it also holds offences on the "
               "Cranstoun length of Harbourgate Street; the location register gives the numbers the quarter runs "
               "to. Addresses are as the recording officer entered them, against the corporate street gazetteer.\n")
    out.append("## The two systems\n")
    out.append("The force replaced its crime information system (CIS) with the records management system (RMS) "
               "class by class through 2025. The extract therefore comes in two files. %s holds everything the RMS "
               "has for both seasons; %s holds the classes CIS was still taking in the 2025 season, up to and "
               "including 27 July 2025.\n" % ("`kcp_rms_offence_extract_2027-01-22.csv`",
                                              "`kcp_cis_offence_extract_2025.csv`"))
    out.append("Migration dates, by class, being the date the RMS became the system of record:\n")
    out.append("| Home Office class | RMS from |\n|---|---|")
    for c in W.CLASSES:
        out.append("| %s | %s |" % (c, m[c].strftime("%d %B %Y")))
    out.append("")
    out.append("For the fortnight %s to %s, recording staff entered assault without injury, public order and "
               "shoplifting in both systems while the RMS classification screens were being settled. Those "
               "offences are in both files, each under that system's own reference; the references do not "
               "correspond. Theft from the person was not part of that arrangement.\n"
               % (p0.strftime("%d %B %Y"), p1.strftime("%d %B %Y")))
    out.append("## Class names\n")
    out.append("CIS held its own offence names. The mapping is one to one:\n")
    out.append("| CIS offence_type | Home Office class |\n|---|---|")
    for c, nm in W.LEGACY_NAMES.items():
        out.append("| %s | %s |" % (nm, c))
    out.append("")
    out.append("## Known differences\n")
    out.append("- CIS recorded the occurrence as four fields (date and time from, date and time to) and left the "
               "second pair empty where the time of occurrence was known. The RMS holds two timestamps and repeats "
               "the known time in both.\n")
    out.append("- Shoplifting was recorded once per incident in CIS and is recorded once per victim in the RMS, so "
               "the 2026 season's shoplifting count is not comparable with the 2025 season's.\n")
    out.append("- A location code is held for every offence of a class under a tasking agreement. For the other "
               "classes it is present only where it was entered, and the address is the only location held for "
               "the rest.\n")
    out.append("- Times are local. The footfall feed published by the business improvement district is stamped in "
               "UTC and is an hour behind local time through both seasons.\n")
    return "\n".join(out) + "\n"
