"""task490 documents: the back-pumping programme paper (water management) and the reservoir register extract
(reservoir safety and engineering), each in its own office's form."""
import hashlib
import logging
import os
import re

import world as W

F_PROG = "backpumping_programme_2027-28.pdf"
F_RESREG = "reservoir_register_extract_2025.pdf"
FONTS = {
    "water": ("Carlito", "/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf",
              "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"),
    "eng": ("LiberationSans", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
}
_REG = set()


def _font(kind):
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.fonts import addMapping
    name, reg, bold = FONTS[kind]
    if name not in _REG:
        pdfmetrics.registerFont(TTFont(name, reg))
        pdfmetrics.registerFont(TTFont(name + "-Bold", bold))
        addMapping(name, 0, 0, name)
        addMapping(name, 1, 0, name + "-Bold")
        addMapping(name, 0, 1, name)
        addMapping(name, 1, 1, name + "-Bold")
        _REG.add(name)
    return name


def _pdf(path, title, author, story, stamp, header, footer, font):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.lib.units import mm

    def on_page(c, d):
        c.saveState()
        c.setFont(font, 7.5)
        c.setFillGray(0.35)
        c.drawString(20 * mm, 287 * mm, header)
        c.drawString(20 * mm, 10 * mm, footer)
        c.drawRightString(190 * mm, 10 * mm, "Page %d" % d.page)
        c.restoreState()

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=22 * mm,
                            bottomMargin=20 * mm, title=title, author=author, subject="", creator="",
                            producer="", invariant=1)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    _scrub(path, stamp)


def _scrub(path, stamp):
    from pypdf import PdfReader
    raw = open(path, "rb").read()
    before = [p.extract_text() for p in PdfReader(path).pages]
    n0 = len(raw)
    for pat in (rb"ReportLab Generated PDF document \(opensource\)",
                rb"ReportLab generated PDF document -- digest \(opensource\)"):
        for m in re.findall(pat, raw):
            raw = raw.replace(m, b" " * len(m))
    old = b"D:20000101000000+00'00'"
    assert len(("D:" + stamp).encode()) == len(old), stamp
    raw = raw.replace(old, ("D:" + stamp).encode())
    for m in sorted(set(re.findall(rb"AAAA[A-Z]{2}\+[A-Za-z-]+", raw)), key=lambda x: (-len(x), x)):
        hx = hashlib.sha1(os.path.basename(path).encode() + m).digest()
        tag = bytes(65 + b % 26 for b in hx[:6])
        raw = raw.replace(m, tag + m[6:])
    assert len(raw) == n0 and b"eportLab" not in raw and b"reportlab" not in raw.lower()
    open(path, "wb").write(raw)
    cap = []
    h = logging.Handler()
    h.emit = lambda rec: cap.append(rec)
    logging.getLogger("pypdf").addHandler(h)
    try:
        after = [p.extract_text() for p in PdfReader(path).pages]
    finally:
        logging.getLogger("pypdf").removeHandler(h)
    assert after == before and not cap, (path, cap)


def _styles(font):
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName=font, fontSize=9.8, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName=font + "-Bold", fontSize=15, leading=18, spaceAfter=6)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName=font + "-Bold", fontSize=11, spaceBefore=8,
                        spaceAfter=4)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10.2)
    cell = ParagraphStyle("c", parent=body, fontSize=8.2, leading=10.0, spaceAfter=0)
    return body, h1, h2, small, cell


def _table(data, widths, font, cell, head=True):
    from reportlab.platypus import Table, TableStyle, Paragraph
    from reportlab.lib import colors
    wrapped = [[Paragraph(str(x), cell) for x in row] for row in data]
    t = Table(wrapped, colWidths=widths, repeatRows=1 if head else 0)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.4, colors.Color(0.6, 0.6, 0.6)),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if head:
        st += [("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.87, 0.91, 0.89))]
    t.setStyle(TableStyle(st))
    return t


def _p(txt, st):
    from reportlab.platypus import Paragraph
    return Paragraph(txt, st)


def write_programme(path):
    from reportlab.platypus import Spacer
    from reportlab.lib.units import mm
    f = _font("water")
    body, h1, h2, small, cell = _styles(f)
    T = lambda d, w: _table(d, w, f, cell)
    s = [_p("<font size=9 color='#1f5c4a'><b>COLDMERE CANALS TRUST</b></font>  <font size=8>Water Management</font>", body),
         _p("Back-pumping programme 2027/28<br/>Scope and siting", h1),
         _p("Version 1.1, 21 September 2026. Owner: Head of Water Management. For the trustees' capital meeting, "
            "10 December 2026.", small),
         Spacer(1, 4 * mm),
         _p("1. Purpose", h2),
         _p("The 2026/27 business plan sets aside capital for one back-pumping scheme in 2027/28: pumps, a rising "
            "main and controls that return water from below a summit flight to its summit pound. Our three summits "
            "on the Kelsby, Harnock and Tilsey lines all depend on reservoirs that drew down hard in the dry summers "
            "of 2022 and 2025. This paper sets out how the scheme's site is chosen and what the trustees will be "
            "asked to approve.", body),
         _p("2. The scheme", h2),
         _p("Outline design for a pumping plant of up to 0.25 cubic metres a second with a rising main beside the "
            "flight, telemetry and a control panel at the top lock. Detailed design from January 2027, works in the "
            "2027/28 winter stoppage and the station in service for the 2028 boating season. The capital provision "
            "is GBP 1.9 million including contingency.", body),
         _p("3. Siting basis", h2),
         _p("3.1 The scheme will serve the summit whose summit locks drew the most water from the summit pound by "
            "filling their chambers over the 2026 boating season, 1 April to 31 October 2026, clock time at the lock.",
            body),
         _p("3.2 The summit locks are the two locks that rise to each summit pound:", body),
         T([["Summit", "Summit locks"],
            ["Kelsby summit", "Kelsby Top Lock (12) and Wharf Lock (13), Kelsby Canal"],
            ["Harnock summit", "Harnock Top Lock (31) and Steward's Lock (32), Harnock Navigation"],
            ["Tilsey summit", "Tilsey Top Lock (8) and Engine Lock (9), Tilsey Canal"]], [42 * mm, 128 * mm]),
         Spacer(1, 2 * mm),
         _p("3.3 Water is reckoned in lockfuls, a lockful being the chamber volume the 2025 chamber survey gives for "
            "the lock, and reported in megalitres.", body),
         _p("3.4 The record of lock use for the season is the LockCount counter network's movement export and, on "
            "the days the volunteer lock-keepers were on duty at Tilsey, their log.", body),
         _p("4. The summit water budget", h2),
         _p("4.1 The paper to the trustees sets each summit's lockage beside the water its reservoirs released to it "
            "and the water taken from it under abstraction agreements over the same season.", body),
         _p("4.2 Reservoir water is reckoned at each reservoir's outlet over the season's clock hours. Water "
            "released from Coldmere Reservoir reaches the Harnock and Tilsey summits in the proportions Fox Bridge "
            "weir divides it.", body),
         _p("4.3 Abstraction is each agreement's metered take between its March and October month-end meter "
            "readings.", body),
         _p("5. Timetable", h2),
         T([["When", "Step"],
            ["3 November 2026", "Season movement export from the counter network"],
            ["20 November 2026", "Siting paper and water budget to the Water Management Group"],
            ["10 December 2026", "Trustees' capital meeting: site and capital approved"],
            ["January to June 2027", "Detailed design, consents and procurement"],
            ["November 2027 to March 2028", "Works in the winter stoppage"]], [52 * mm, 118 * mm]),
         Spacer(1, 3 * mm),
         _p("Document control", h2),
         T([["Version", "Date", "Change", "By"],
            ["1.0", "2 September 2026", "First issue to the Water Management Group", W.PEOPLE["head"]],
            ["1.1", "21 September 2026", "Siting basis 3.1 to 3.4 and budget 4.1 to 4.3 agreed at the group's "
             "meeting of 17 September", W.PEOPLE["head"]]], [18 * mm, 32 * mm, 90 * mm, 30 * mm]),
         ]
    _pdf(path, "Back-pumping programme 2027/28: scope and siting", W.PEOPLE["head"], s, "20260921143107+01'00'",
         "Coldmere Canals Trust | Water Management | Back-pumping programme 2027/28",
         "Version 1.1, 21 September 2026", f)


def write_reservoir_register(path):
    from reportlab.platypus import Spacer
    from reportlab.lib.units import mm
    f = _font("eng")
    body, h1, h2, small, cell = _styles(f)
    T = lambda d, w: _table(d, w, f, cell)
    s = [_p("<font size=9><b>COLDMERE CANALS TRUST</b></font>  <font size=8>Reservoir Safety and Engineering</font>",
            body),
         _p("Reservoir register: extract for the summit supply reservoirs", h1),
         _p("Extract prepared 7 July 2026 from the register maintained under the Reservoirs Act 1975. Supervising "
            "engineer's annual statements are held separately.", small),
         Spacer(1, 3 * mm),
         _p("1. Reservoirs", h2),
         T([["Name", "Capacity (Ml)", "Outlet", "Discharges to"],
            ["Upper Kelsby", "1,180", "Valve tower, 300 mm outlet valve; daily return by the reservoir keeper",
             "Lower Kelsby Reservoir, by the Hollins Brook"],
            ["Lower Kelsby", "2,410", "Valve tower, 450 mm outlet valve, about 16 Ml/d at full bore at top water "
             "level; daily return by the reservoir keeper", "Kelsby feeder, entering Kelsby summit at Feeder Bridge"],
            ["Coldmere", "6,950", "Draw-off culvert to the outlet gauging weir (section 2); telemetered",
             "Coldmere feeder to Fox Bridge division weir (section 3)"],
            ["Tilsey", "1,730", "Valve house, 375 mm outlet valve; daily return by the reservoir keeper",
             "Tilsey feeder, entering Tilsey summit at Hollow Wood"]], [26 * mm, 20 * mm, 70 * mm, 54 * mm]),
         _p("2. Coldmere outlet gauging weir", h2),
         _p("Sharp-crested rectangular notch with end contractions in a steel crest plate. Discharge "
            "Q = 1.84 (b - 0.2h) h<super>1.5</super> cubic metres a second, b the notch width and h the head over "
            "the crest, both in metres. The telemetry outstation records the head and its computed discharge as "
            "15-minute means.", body),
         T([["Crest plate", "Notch width b (m)", "In service"],
            ["Plate C1", "0.75", "May 2009 to 16 June 2026"],
            ["Plate C2", "0.60", "From 10:30 UTC on 16 June 2026 (works order 26005944)"]],
           [40 * mm, 40 * mm, 90 * mm]),
         Spacer(1, 2 * mm),
         _p("3. Fox Bridge division weir", h2),
         _p("The Coldmere feeder enters a stilling pool at Fox Bridge with two sharp-crested rectangular notches "
            "with end contractions, each discharging Q = 1.84 (b - 0.2h) h<super>1.5</super> cubic metres a second "
            "for its own head h over its crest. The pool level is common to both notches.", body),
         T([["Notch", "Width b (m)", "Crest level (m AOD)", "Feeds"],
            ["Harnock arm", "0.50", "118.420", "Harnock summit at Fox Lock tail bridge"],
            ["Tilsey arm", "0.35", "118.480", "Tilsey feeder, joining below Tilsey Reservoir"]],
           [34 * mm, 26 * mm, 34 * mm, 76 * mm]),
         Spacer(1, 2 * mm),
         _p("4. Inspections", h2),
         T([["Name", "Last inspection under section 10", "Inspecting engineer"],
            ["Upper Kelsby", "March 2023", "Panel AR engineer (external)"],
            ["Lower Kelsby", "March 2023", "Panel AR engineer (external)"],
            ["Coldmere", "October 2024", "Panel AR engineer (external)"],
            ["Tilsey", "April 2022", "Panel AR engineer (external)"]], [40 * mm, 70 * mm, 60 * mm]),
         Spacer(1, 2 * mm),
         _p("Register extract prepared by %s, engineer, reservoirs and structures. Next full review: April 2027." % W.PEOPLE["asset"], small),
         ]
    _pdf(path, "Reservoir register: extract for the summit supply reservoirs", W.PEOPLE["asset"], s,
         "20260707101544+01'00'", "Coldmere Canals Trust | Reservoir Safety and Engineering | Register extract",
         "Extract, 7 July 2026", f)


def write_all(target):
    write_programme(os.path.join(target, F_PROG))
    write_reservoir_register(os.path.join(target, F_RESREG))
