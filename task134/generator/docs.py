"""Governing documents: Notice to Mariners 3 of 2026 (PDF), the marine licence (PDF) and the maintenance planning basis
for the 2027-2030 contract (DOCX)."""
import os
import re

from docx import Document
from docx.shared import Pt

import geo
import params as P
from io_util import pdf_text, save_docx

NOTICE = "notice_to_mariners_03-2026.pdf"
LICENCE = "marine_licence_L2021-00317-2.pdf"
BASIS = "deepening_2027_maintenance_planning_basis.docx"

# Filed sentences, each once, at authority.
S_DATUM = "Depths are in metres below chart datum. Chart datum at Fendmouth is 2.90 m below Ordnance Datum Newlyn."
S_WIDTH = "Each reach's maintained width and the turning basin's width are centred on the centreline."
S_NQ2 = "North Quay Berth 2 has not been maintained since 1 April 2019. Depths alongside are not guaranteed."
S_YEAR1 = ("The year 1 quantity is the in situ volume of material, as the contractor's monthly certificates measure it, that "
           "will settle in the maintained areas between 1 October 2027 and 30 September 2028: the four reaches and the "
           "turning basin held at 14.3 m below chart datum and the berth pockets at their present maintained depths, "
           "through a year of average conditions as the licence years 2016-17 to 2025-26 averaged them.")
S_REPORT = "It is reported for each reach, for the turning basin and for the berth pockets together, and in total."
S_DEEPEN = ("From 1 October 2027 the four reaches of the approach channel and the turning basin will be maintained at 14.3 m "
            "below chart datum within their present maintained widths. The berth pockets keep their present maintained "
            "depths and North Quay Berth 2 stays out of maintenance.")
S_QUARTER = ("A quarter is October to December, January to March, April to June or July to September of the licence year, "
             "taken by the date on which the material was placed in UK civil time (GMT, or BST while it is in force).")
S_WET = ("Wet tonnes are the dry solids placed divided by the dry-solids fraction by mass reported for the area the material "
         "was loaded in, from the most recent sampling campaign completed before the month in which it was placed, the "
         "month taken in UK civil time as in 5.3.")
S_NOMON = ("For a vessel without a loading monitor, dry solids are the hopper volume times 2.65 times the mixture density less "
           "1.025, divided by 1.625 (2.65 less 1.025).")
S_SAMPLE = ("Results are reported for the dredged area in which each sample was actually taken, and a field duplicate is "
            "averaged with its primary sample before area means are taken.")
S_CLOSED = "No material may be placed at Fend Spit from 1 December to the last day of February."


def _p(doc, text, bold=False, size=10.5, italic=False):
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    return para


def berth_corners(code):
    for c, name, s0, s1, t0, t1, depth, nat, k in P.BERTHS:
        if c == code:
            pts = [geo.point_at(s0, t0), geo.point_at(s1, t0), geo.point_at(s1, t1), geo.point_at(s0, t1)]
            return [(round(float(e)), round(float(n))) for e, n in pts]
    raise KeyError(code)


def _pdf(path, title, author, pages, stamp):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(path, pagesize=A4, invariant=1)
    c.setTitle(title)
    c.setAuthor(author)
    c.setCreator(author)
    c.setProducer(author)
    c.setSubject(title)
    w, h = A4
    for lines in pages:
        y = h - 60
        for font, size, text, xs in lines:
            c.setFont(font, size)
            if xs is None:
                c.drawString(56, y, text)
            else:
                for x, cell in zip(xs, text):
                    c.drawString(x, y, cell)
            y -= 17 if size >= 10 else 13.5
        c.showPage()
    c.save()
    _scrub(path, stamp)


def _scrub(path, stamp):
    before = pdf_text(path)
    b = open(path, "rb").read()
    n = len(b)

    def blank(m):
        return m.group(1) + b" " * (len(m.group(0)) - len(m.group(1)))
    b = re.sub(rb"(%\x93\x8c\x8b\x9e)[^\n]*ReportLab[^\n]*", blank, b)
    b = re.sub(rb"(%)[^\n]*ReportLab[^\n]*", blank, b)
    for o in set(re.findall(rb"/(?:CreationDate|ModDate) \((D:[^)]*)\)", b)):
        assert len(o) == len(stamp)
        b = b.replace(o, stamp.encode("latin-1"))
    assert len(b) == n and b"ReportLab" not in b
    open(path, "wb").write(b)
    assert pdf_text(path) == before


def wrap(text, width=104):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def para(text, size=9, width=104):
    return [("Helvetica", size, ln, None) for ln in wrap(text, width)]


def write_notice(out):
    xs = [56, 150, 230, 320]
    L = [("Helvetica-Bold", 12, "Port of Fendmouth - Notice to Mariners No. 3 of 2026", None),
         ("Helvetica-Bold", 10, "Maintained depths and maintained areas", None),
         ("Helvetica", 9, "This notice replaces Notice to Mariners No. 2 of 2024. Positions are OSGB36 National Grid eastings and northings.", None)]
    L += para(S_DATUM)
    L.append(("Helvetica-Bold", 9, "Approach channel centreline", None))
    L.append(("Helvetica-Bold", 9, ("Waypoint", "Chainage (km)", "Easting", "Northing"), xs))
    for i, (ch, e, n) in enumerate(P.WAYPOINTS):
        L.append(("Helvetica", 9, ("W%d" % i, "%.2f" % ch, "%.0f" % e, "%.0f" % n), xs))
    L.append(("Helvetica-Bold", 9, "Reaches and turning basin", None))
    xs2 = [56, 190, 300, 400]
    L.append(("Helvetica-Bold", 9, ("Area", "Chainage (km)", "Width (m)", "Maintained depth (m)"), xs2))
    for code, name, c0, c1, half, nn, ns, k in P.PARTS:
        L.append(("Helvetica", 9, (name, "%.2f to %.2f" % (c0, c1), "%.0f" % (2 * half), "%.1f" % P.DEPTH_NOW), xs2))
    L += para(S_WIDTH)
    L.append(("Helvetica-Bold", 9, "Berth pockets (corner positions, easting northing)", None))
    for code, name, s0, s1, t0, t1, depth, nat, k in P.BERTHS:
        cs = berth_corners(code)
        txt = "; ".join("%d %d" % c for c in cs)
        dep = "Not maintained." if depth is None else "Maintained depth %.1f m." % depth
        L.append(("Helvetica", 9, "%s: %s. %s" % (name, txt, dep), None))
    L += para(S_NQ2)
    L += para("Mariners are reminded that depths between surveys may be less than the maintained depth. The latest survey "
              "is available from the Harbour Office on request.")
    L.append(("Helvetica", 9, "D. Davies, Harbour Master, Harbour Office, Fendmouth. 3 February 2026.", None))
    _pdf(os.path.join(out, NOTICE), "Notice to Mariners No. 3 of 2026", "Harbour Office, Port of Fendmouth", [L],
         "D:20260203090000+00'00'")


def write_licence(out):
    xs = [56, 150, 260, 370]
    p1 = [("Helvetica-Bold", 12, "Marine Licence L/2021/00317 - Variation 2", None),
          ("Helvetica", 9, "Licence holder: Fendmouth Borough Council (Harbour Department), Harbour Office, Fendmouth.", None),
          ("Helvetica", 9, "Licensed activity: maintenance dredging of the maintained areas in the Harbour Master's current notice", None),
          ("Helvetica", 9, "to mariners and the deposit at sea of the dredged material at the disposal sites below.", None),
          ("Helvetica", 9, "Licence period: 1 October 2021 to 30 September 2027. Variation 2 issued 14 June 2024.", None),
          ("Helvetica-Bold", 10, "Disposal sites (WGS84, corner points)", None),
          ("Helvetica-Bold", 9, ("Site", "Corner", "Latitude", "Longitude"), xs)]
    for code in ("FS", "WD"):
        name, pts = P.SITES[code]
        for i, (la, lam, lo, lom) in enumerate(pts):
            p1.append(("Helvetica", 9, ("%s (%s)" % (name, code) if i == 0 else "", "%d" % (i + 1),
                                        "%d %06.3f' N" % (la, lam), "%d %06.3f' E" % (lo, lom)), xs))
    p1.append(("Helvetica-Bold", 10, "Conditions", None))
    p1 += para("5.1 " + S_CLOSED)
    p1 += para("5.2 The quantity deposited must not exceed 2,000,000 wet tonnes in any licence year, a licence year "
               "running from 1 October to 30 September.")
    p1 += para("5.3 The licence holder must make a return for each quarter of the licence year giving the quantity placed "
               "at each disposal site in wet tonnes. " + S_QUARTER)
    p1 += para("5.4 " + S_WET + " Dry solids placed are taken from the vessel's loading monitor. " + S_NOMON)
    p1 += para("5.5 Sediment is sampled once in each licence year at the stations of the sampling plan agreed with the "
               "licensing authority, and analysed for dry solids and for the determinands of the plan. " + S_SAMPLE)
    p1 += para("5.6 Each return is due within 28 days of the end of its quarter.")
    p1.append(("Helvetica", 9, "Issued for the licensing authority, 14 June 2024.", None))
    _pdf(os.path.join(out, LICENCE), "Marine Licence L/2021/00317 Variation 2", "Marine licensing authority", [p1],
         "D:20240614120000+01'00'")


def write_basis(out):
    doc = Document()
    doc.styles["Normal"].font.name = "Calibri"
    _p(doc, "PORT OF FENDMOUTH, HARBOUR DEPARTMENT", bold=True, size=11)
    _p(doc, "Channel deepening 2027: maintenance dredging planning basis for the 2027-2030 contract", bold=True, size=13)
    _p(doc, "H. Thorpe, Dredging and Hydrography Manager. Version 2, 11 January 2027. For Procurement (G. Ellis), the "
            "Harbour Master and the tender evaluation panel.", size=9, italic=True)
    _p(doc, "Background", bold=True)
    _p(doc, "The capital deepening of the approach channel and the turning basin is let as a separate contract and runs "
            "from May to September 2027. The present maintenance contract with " + P.CONTRACTOR + " ends on 30 September "
            "2027. The 2027-2030 maintenance contract goes to tender in February 2027 and is awarded by Cabinet in April, "
            "and tenderers will price year 1 against the quantity this note sets. The licence variation for the "
            "disposal sites will be applied for on the same basis.")
    _p(doc, "What changes in October 2027", bold=True)
    _p(doc, S_DEEPEN + " The maintained areas and their present depths are in Notice to Mariners No. 3 of 2026.")
    _p(doc, "Year 1 quantity", bold=True)
    _p(doc, S_YEAR1 + " " + S_REPORT)
    _p(doc, "Years 2 and 3 will be reset at the first annual review from the certificates of year 1.")
    _p(doc, "Other tender items", bold=True)
    _p(doc, "Measurement stays as now: in situ volume by pre- and post-dredge survey for payment, dry solids by loading "
            "monitor for the disposal returns. The survey programme continues twice a year, in April and October, and "
            "both disposal sites remain in use under the varied licence.")
    _p(doc, "Document control", bold=True)
    t = doc.add_table(rows=1, cols=3)
    t.style = "Table Grid"
    for i, h in enumerate(("Version", "Date", "Change")):
        t.rows[0].cells[i].text = h
    for row in (("1", "2 December 2026", "First draft for Procurement."),
                ("2", "11 January 2027", "Year 1 quantity defined for the tender; licence variation timetable added.")):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = v
    save_docx(doc, os.path.join(out, BASIS), "Maintenance dredging planning basis 2027-2030", P.PEOPLE["manager"],
              "2026-12-02T14:45:00Z", modified="2027-01-11T16:20:00Z")
