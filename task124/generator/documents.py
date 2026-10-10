"""The pack's documents: the risk policy, the risk committee minute, last summer's close-out report, the Business
Saver terms, the desk procedures, the position report, the programme roster, Pecos's quote sheet, ERCOT's zone
outlook, the field notes and the extract log. Short, functional, each in its organisation's own voice."""
from __future__ import annotations

import re
import zipfile
from datetime import date, datetime, timezone
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

from reportlab import rl_config

rl_config.invariant = 1  # fixed document identifier and dates, so two builds are byte-identical

from reportlab.lib import colors  # noqa: E402
from reportlab.lib.enums import TA_LEFT  # noqa: E402
from reportlab.lib.pagesizes import letter  # noqa: E402
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # noqa: E402
from reportlab.lib.units import inch  # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

from common import BOOKS, CODE, PEAKS, SUMMERS, round_half_up  # noqa: E402

CT = ZoneInfo("America/Chicago")
INVARIANT_PDF_DATE = b"D:20000101000000+00'00'"


def _styles():
    ss = getSampleStyleSheet()
    base = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=12.6,
                          alignment=TA_LEFT, spaceAfter=5)
    small = ParagraphStyle("s", parent=base, fontSize=8, leading=10, textColor=colors.HexColor("#333333"))
    h1 = ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=12.5, leading=15, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=10, leading=13, spaceBefore=6,
                        spaceAfter=3)
    return base, small, h1, h2


def _table(data, widths, size=8.5, right_from=1):
    t = Table(data, colWidths=widths, hAlign="LEFT")
    style = [("FONT", (0, 0), (-1, -1), "Helvetica", size), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size),
             ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2),
             ("ALIGN", (right_from, 1), (-1, -1), "RIGHT")]
    t.setStyle(TableStyle(style))
    return t


def pdf_date(when: datetime) -> bytes:
    off = int(when.replace(tzinfo=CT).utcoffset().total_seconds() // 60)
    sign, off = ("-" if off < 0 else "+"), abs(off)
    return f"D:{when:%Y%m%d%H%M%S}{sign}{off // 60:02d}'{off % 60:02d}'".encode()


def stamp_pdf(path, when: datetime):
    new = pdf_date(when)
    assert len(new) == len(INVARIANT_PDF_DATE), new
    b = open(path, "rb").read()
    assert b.count(INVARIANT_PDF_DATE) == 2, path
    with open(path, "wb") as f:
        f.write(b.replace(INVARIANT_PDF_DATE, new))


def _doc(path, title, author, story, footer, when):
    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(0.85 * inch, 0.55 * inch, footer)
        canvas.drawRightString(7.65 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                            topMargin=0.8 * inch, bottomMargin=0.85 * inch, title=title, author=author,
                            subject="", creator=author)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    stamp_pdf(path, when)


def _ds(d: date) -> str:
    return f"{d.day} {d.strftime('%B')} {d.year}"


PDF_MADE = {"terms": datetime(2025, 3, 3, 10, 12, 41), "minute": datetime(2027, 3, 22, 16, 5, 9),
            "report": datetime(2027, 2, 2, 15, 38, 27)}


# ------------------------------------------------------------------------------ Business Saver terms
def terms(path):
    base, small, h1, h2 = _styles()
    s = [Paragraph("SABINE CREST ENERGY", small), Paragraph("Business Saver", h1),
         Paragraph("Program terms for refrigerated facilities, 2025 edition", base), Spacer(1, 6)]
    s.append(Paragraph("1. Who can take part", h2))
    s.append(Paragraph(
        "Business Saver is open to Sabine Crest commercial customers who operate refrigerated warehousing or ice "
        "manufacturing at a site served on an interval data recorder (IDR) meter. A site joins once its meter has "
        "recorded a full June through September of interval reads at the site. Each site is enrolled under the "
        "customer account that is billed for it.", base))
    s.append(Paragraph("2. What a member agrees to", h2))
    s.append(Paragraph(
        "At enrolment each site is given a firm service level in kW. On a called day the member holds the site's "
        "load at or below its firm service level from 2:00 p.m. to 6:00 p.m. Central Prevailing Time (the called "
        "window). Product temperatures stay the member's responsibility throughout.", base))
    s.append(Paragraph("3. Calls", h2))
    s.append(Paragraph(
        "Calls are made on business days from June through September. Sabine Crest notifies each member's "
        "nominated contact by 10:00 a.m. on the called day by text message and email. A business day is Monday "
        "to Friday other than Independence Day and Labor Day as observed.", base))
    s.append(Paragraph("4. Baseline and credits", h2))
    s.append(Paragraph(
        "A site's baseline for an hour of a called window is its average load in that hour on its ten most recent "
        "business days without a call. The member is credited for each kWh by which the site's load in the called "
        "window falls below its baseline, at $0.36 per kWh. Credits are calculated "
        "per account and called window and post to the following month's bill.", base))
    s.append(Paragraph("5. Term", h2))
    s.append(Paragraph(
        "Enrolment renews each season unless the member withdraws in writing by March 31. A member that misses its "
        "firm service level in two called windows in one season may be removed for the rest of that season.", base))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Program Desk: Donald Lee, Manager. businesssaver@sabinecrestenergy.com, (713) 555-0148.",
                       small))
    _doc(path, "Business Saver program terms, 2025", "Sabine Crest Energy", s,
         "Sabine Crest Energy | Business Saver terms | 2025 edition", PDF_MADE["terms"])


# ------------------------------------------------------------------------------ risk committee minute
def minute(path):
    base, small, h1, h2 = _styles()
    s = [Paragraph("SABINE CREST ENERGY LLC", small), Paragraph("Risk Committee", h1),
         Paragraph("Minute of the meeting held on Friday 19 March 2027, 9:30 a.m., Houston office, room 14B", base),
         Spacer(1, 4)]
    s.append(Paragraph("Present: Susan Kelley (Chair), Tammy Ochoa (Head of Supply Portfolio), Gregory Sheppard "
                       "(Head of Trading), Craig Stewart (Load Planning Lead), the Chief Financial Officer and the "
                       "Controller. In attendance: Treasury.", base))
    s.append(Paragraph("1. Minute of 19 February 2027", h2))
    s.append(Paragraph("Approved. The Chair signed the 2027 Summer Supply Risk Policy as adopted at that meeting.",
                       base))
    s.append(Paragraph("2. Summer 2027 firm capacity", h2))
    s.append(Paragraph(
        "The Committee caps the 2027 summer block at 400 MW of firm capacity, to be bought as monthly call "
        "options for June, July, August and September 2027 in 5 MW lots. Supply Portfolio will bring the split of "
        "the block across the eight weather-zone books to the meeting on Friday 16 April 2027, built on the spring "
        "enrolment extract. The Committee will sign the option premium for the block with the split.", base))
    s.append(Paragraph("3. Collateral", h2))
    s.append(Paragraph("Treasury reported posted collateral within the facility limit. No action.", base))
    s.append(Paragraph("4. Next meeting", h2))
    s.append(Paragraph("Friday 16 April 2027, 9:30 a.m.", base))
    s.append(Spacer(1, 10))
    s.append(Paragraph("Signed: Susan Kelley, Chair", base))
    _doc(path, "Risk Committee minute, 19 March 2027", "Sabine Crest Energy", s,
         "Sabine Crest Energy | Risk Committee | Confidential", PDF_MADE["minute"])


# ------------------------------------------------------------------------------ summer 2026 close-out
def report(path, an):
    base, small, h1, h2 = _styles()
    d26, he26, mw26 = PEAKS[2026]
    s = [Paragraph("SABINE CREST ENERGY | LOAD PLANNING", small), Paragraph("Summer 2026 close-out: supply risk", h1),
         Paragraph("Craig Stewart, Load Planning Lead. 2 February 2027. Distribution: Risk Committee, Supply "
                   "Portfolio, Trading.", small), Spacer(1, 6)]
    s.append(Paragraph("1. The summer", h2))
    s.append(Paragraph(
        f"ERCOT set its 2026 summer peak on {d26.strftime('%A')} {_ds(d26)} in the hour ending {he26}:00 "
        f"({mw26:,} MW). Table 1 gives each book at that hour: the maximum demand enrolled with us on the day and "
        "the book's settled load in the hour.", base))
    rows = [["Book", "Enrolled maximum demand (MW)", "Settled load, system peak hour (MW)"]]
    for b in BOOKS:
        rows.append([b, f"{an.md_peak[b][2026] / 1000.0:,.1f}", f"{an.peak_load[b][2026]:,.1f}"])
    s.append(_table(rows, [1.5 * inch, 2.1 * inch, 2.3 * inch]))
    s.append(Paragraph("Table 1. Summer 2026 at the system peak hour.", small))
    s.append(Paragraph("2. Replay of the closed summers", h2))
    s.append(Paragraph(
        "Table 2 restates each closed summer at the book we carried at the 2026 system peak: the summer's settled "
        "book load in ERCOT's system peak hour, divided by the book's enrolled maximum demand at that summer's "
        "system peak, times the book's enrolled maximum demand at the 2026 system peak. Figures are whole MW.",
        base))
    tab = an.replay_table()
    rows = [["Book"] + [str(y) for y in SUMMERS]]
    for b in BOOKS:
        rows.append([b] + [f"{int(round_half_up(tab[(b, y)])):,}" for y in SUMMERS])
    s.append(_table(rows, [1.05 * inch] + [0.53 * inch] * 10, size=8))
    s.append(Paragraph("Table 2. Book load in the system peak hour, closed summers replayed at the 2026 book (MW).",
                       small))
    s.append(Paragraph("3. Notes", h2))
    s.append(Paragraph(
        "Settled loads are ERCOT true-up settlement for the book. Enrolled maximum demand is from the enrolment "
        "system as of each date. This report closes out summer 2026; it does not size the 2027 block, which the "
        "Risk Committee sets in the spring.", base))
    _doc(path, "Summer 2026 close-out: supply risk", "Sabine Crest Energy", s,
         "Sabine Crest Energy | Load Planning | Internal", PDF_MADE["report"])
