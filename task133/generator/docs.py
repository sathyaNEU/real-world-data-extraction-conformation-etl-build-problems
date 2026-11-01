"""Governing documents: the cartage planning basis (DOCX), the 50MAX route approval (PDF) and the export grade
specification (PDF)."""
import os
import re

from docx import Document
from docx.shared import Pt

import params as P
from io_util import save_docx, pdf_text

BASIS = "cartage_planning_basis_FY2028.docx"
APPROVAL = "50MAX_route_approval_RDC-2026-114.pdf"
GRADESPEC = "export_log_grade_specifications_2025.pdf"

S_LOAD = ("A load is one truck-and-trailer trip carrying export logs from one of our forests to Port Kowhai, as weighed over "
          "the port weighbridge. Sawlog and pulp deliveries to the domestic mills are not loads for this round.")
S_YEAR = "FY2028 runs from 1 July 2027 to 30 June 2028."
S_FLEET = ("We are sizing the round on the fleet we have: the units on the cartage fleet register at 30 June 2026, as the "
           "register records them. No new units are assumed.")
S_LOADS = ("For each export grade, FY2028 loads are the harvest plan's export tonnes for the grade divided by the average "
           "payload that grade's FY2026 port loads would carry on the same units in FY2028.")
S_PLAN = "The export tonnes are the Board-approved FY2028 harvest plan of 18 September 2026 (its Export sheet)."
S_LIMITS = ("RDC-2026-114 opens the port route to 50MAX from 1 July 2027. From then, units holding a 50MAX permit run at 50 "
            "tonnes gross on the route to Port Kowhai; every other unit stays at 44 tonnes gross.")
S_CART = ("Cartage for FY2026 is what we paid for FY2026's loads, reported against the carrier whose unit hauled the load "
          "and net of any credit note.")
S_MILL = "Domestic deliveries are reported by delivery date, in tonnes delivered."


def _p(doc, text, bold=False, size=10.5, italic=False):
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    return para


def write_basis(out):
    doc = Document()
    doc.styles["Normal"].font.name = "Calibri"
    _p(doc, "MATIRI FOREST PRODUCTS LIMITED", bold=True, size=11)
    _p(doc, "Logistics planning note: export cartage basis for FY2028", bold=True, size=13)
    _p(doc, "John Morris, Logistics Manager. Version 2, 6 October 2026. For Harvest Planning, Finance and the Port Kowhai "
            "log yard.", size=9, italic=True)
    _p(doc, "Background", bold=True)
    _p(doc, "The FY2028 export cartage contract goes to tender in November. Carriers will price against the number of loads "
            "we tell them to expect, and Finance is building its benchmark rates from what we paid this year, so everyone "
            "working on the round needs to size it the same way. This note is that basis. It replaces version 1 now that "
            "the council has approved 50MAX on the port route.")
    _p(doc, "What we are sizing", bold=True)
    _p(doc, S_LOAD)
    _p(doc, S_YEAR + " " + S_FLEET)
    _p(doc, "How we get to FY2028 loads", bold=True)
    _p(doc, S_LOADS + " " + S_PLAN)
    _p(doc, S_LIMITS)
    _p(doc, "Anything the plan does not already carry, such as a change of grade mix or roading, sits outside this basis "
            "and will be dealt with at the contract review.")
    _p(doc, "What we report beside it", bold=True)
    _p(doc, S_CART + " Finance uses these figures for the benchmark rates.")
    _p(doc, S_MILL + " The mills have asked for them by quarter for their supply reviews.")
    _p(doc, "Change record", bold=True)
    t = doc.add_table(rows=1, cols=3)
    t.style = "Table Grid"
    for i, h in enumerate(("Version", "Date", "Change")):
        t.rows[0].cells[i].text = h
    for row in (("1", "14 August 2026", "First issue for the contract round."),
                ("2", "6 October 2026", "Route approval RDC-2026-114 received; FY2028 limits added. Cartage tied to the "
                                        "year's loads.")):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = v
    save_docx(doc, os.path.join(out, BASIS), "Export cartage basis FY2028", "John Morris", "2026-10-06T01:30:00Z")


def _pdf(path, title, author, lines, stamp):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(path, pagesize=A4, invariant=1)
    c.setTitle(title)
    c.setAuthor(author)
    c.setCreator(author)
    c.setProducer(author)
    c.setSubject(title)
    w, h = A4
    y = h - 60
    for font, size, text, xs in lines:
        c.setFont(font, size)
        if xs is None:
            c.drawString(56, y, text)
        else:
            for x, cell in zip(xs, text):
                c.drawString(x, y, cell)
        y -= 17 if size >= 10 else 14
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


def write_approval(out):
    lines = [("Helvetica-Bold", 12, "Ruawharo District Council - Roading", None),
             ("Helvetica", 9, "Ref RDC-2026-114    29 September 2026", None),
             ("Helvetica", 9, "To: Logistics Manager, Matiri Forest Products Limited", None),
             ("Helvetica-Bold", 10, "Approval: 50MAX vehicles on the Port Kowhai route", None),
             ("Helvetica", 9, "The bridge strengthening on the Port Kowhai route is due for completion in June 2027. From 1 July 2027", None),
             ("Helvetica", 9, "the route from the Puketitiri, Te Pohue, Esk, Waitara Downs and Glenross forest roads to Port Kowhai", None),
             ("Helvetica", 9, "is approved for 50MAX vehicles: nine-axle combinations holding a current 50MAX permit may operate at up", None),
             ("Helvetica", 9, "to 50 tonnes gross. All other vehicles remain at the general access limit of 44 tonnes gross.", None),
             ("Helvetica", 9, "Permit holders remain responsible for axle-group limits and for carrying their permit in the vehicle.", None),
             ("Helvetica", 9, "Signed: Roading Asset Manager", None)]
    _pdf(os.path.join(out, APPROVAL), "50MAX route approval RDC-2026-114", "Ruawharo District Council", lines,
         "D:20260929143000+13'00'")


def write_gradespec(out):
    rows = [("A", "A grade", "12.1", "30-60", "Long unpruned sawlog"),
            ("P", "Pruned", "5.9", "40-80", "Pruned butt log"),
            ("K", "K grade", "5.9", "26-60", "Short unpruned sawlog"),
            ("KI", "KI grade", "3.9", "24-40", "Short industrial sawlog"),
            ("KIS", "KIS grade", "3.9", "20-30", "Short small industrial log")]
    xs = [56, 110, 190, 260, 340]
    lines = [("Helvetica-Bold", 12, "Matiri Forest Products - export log grades (2025 specification)", None),
             ("Helvetica", 9, "Lengths are cut lengths in metres including trim allowance; SED is small-end diameter in cm.", None),
             ("Helvetica-Bold", 9, ("Code", "Grade", "Length (m)", "SED (cm)", "Description"), xs)]
    for r in rows:
        lines.append(("Helvetica", 9, r, xs))
    lines.append(("Helvetica", 8, "Issued by Marketing, 1 March 2025. Scaling at Port Kowhai to the JAS standard.", None))
    _pdf(os.path.join(out, GRADESPEC), "Export log grade specifications 2025", "Matiri Forest Products Limited", lines,
         "D:20250301090000+13'00'")
