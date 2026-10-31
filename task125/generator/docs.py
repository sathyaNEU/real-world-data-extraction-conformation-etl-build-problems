"""The agency's governing document: the sulfate load allocation schedule (the WHAT of the call)."""
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

CEO = "Bhekisisa Mpangazitha"
AUTHOR = "Thandazile Nongalo"


def _styles():
    base = ParagraphStyle("p", fontName="Helvetica", fontSize=9.4, leading=12.6, spaceAfter=4, alignment=TA_LEFT)
    return {"p": base,
            "t": ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=3),
            "s": ParagraphStyle("s", parent=base, fontSize=8.2, leading=10.6, textColor=colors.HexColor("#4a5560")),
            "h": ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.2, leading=13, spaceBefore=6),
            "c": ParagraphStyle("c", parent=base, fontSize=8.6, leading=10.8, spaceAfter=0),
            "ch": ParagraphStyle("ch", parent=base, fontName="Helvetica-Bold", fontSize=8.6, leading=10.8, spaceAfter=0)}


def _table(rows, widths, st):
    def esc(x):
        return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    data = [[Paragraph(esc(c), st["ch"] if i == 0 else st["c"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#5b6b77")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    return t


def fix_dates(path, created, modified):
    data = open(path, "rb").read()
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + created.encode() + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + modified.encode() + b")", data)
    for sig in (b"ReportLab Generated PDF document (opensource)",
                b"ReportLab generated PDF document -- digest (opensource)"):
        data = data.replace(sig, b" " * len(sig))
    open(path, "wb").write(data)


def schedule(path):
    st = _styles()
    alloc = [("Resource unit", "River", "Reach", "Lower boundary", "Allocation, t/d of sulfate")]
    reach = {"MZ1": "Source to the Khambule Stream", "KH1": "Source to its Mzimela confluence",
             "MZ2": "Khambule Stream confluence to Esikhotheni weir", "MZ3": "Esikhotheni weir to the Silwane Stream",
             "SW1": "Source to its Mzimela confluence", "MZ4": "Silwane Stream confluence to Ngwelezane Drift weir",
             "GB1": "Source to its Mzimela confluence", "MZ5": "Gubhu River confluence to the Nkwali gorge weir",
             "NY1": "Source to the Ntsheketshe Stream", "NT1": "Source to its Nyathi confluence",
             "NY2": "Ntsheketshe Stream confluence to Mabhokweni weir", "MP1": "Source to its Nyathi confluence",
             "NY3": "Mpafa Stream confluence to Siphethu weir", "NY4": "Siphethu weir to the catchment outlet weir"}
    for code, river, name, inflows, weir, a in W.RU:
        alloc.append((code, river, reach[code], weir, "%.0f" % a))
    blocks = [
        Paragraph("Umzimela Catchment Management Agency", st["s"]),
        Paragraph("Sulfate Load Allocation Schedule for the Umzimela Catchment", st["t"]),
        Paragraph("Schedule 3 to the Catchment Management Strategy. Approved by the Chief Executive Officer, %s, on "
                  "17 March 2025; prepared by %s, Senior Manager: Water Resource Protection. Replaces the 2019 "
                  "schedule." % (CEO, AUTHOR), st["s"]),
        Spacer(1, 4),
        Paragraph("1. Purpose", st["h"]),
        Paragraph("Drainage from the coal mines of the Umzimela catchment carries sulfate into its streams and rivers. "
                  "This schedule divides the sulfate each river can carry without harm to the uses downstream into an "
                  "allocation for each resource unit, and sets how the agency assesses each unit against its "
                  "allocation and acts on the assessment.", st["p"]),
        Paragraph("2. Resource units", st["h"]),
        Paragraph("A resource unit is a reach of river or stream from its upper end to its lower boundary at the "
                  "agency's gauging weir named in Table 2. The water of a unit includes all that enters it at its "
                  "upper end, from the unit above it and from any stream joining it there.", st["p"]),
        Paragraph("3. Assessment", st["h"]),
        Paragraph("The load of a resource unit is the sulfate, as SO4, that its water carries past its lower "
                  "boundary, in tonnes a day. A resource unit is over its allocation for a dry season when its load on "
                  "the days of the routine sampling runs from 1 May to 30 September, averaged over those runs, "
                  "exceeds its allocation in Table 2. The agency assesses each dry season after the hydrological year "
                  "closes on 30 September.", st["p"]),
        Paragraph("4. Directives", st["h"]),
        Paragraph("For each resource unit over its allocation, the Chief Executive Officer directs the holders of "
                  "water use licences that discharge into the unit, under section 19 of the National Water Act, to "
                  "reduce their discharges in the following year. A unit within its allocation draws no directive "
                  "for that year.", st["p"]),
        Paragraph("5. Monitoring", st["h"]),
        Paragraph("The agency's field teams sample every monitoring site on a routine run every second week, each run "
                  "in one day, and the agency's laboratory analyses the samples. The gauging weirs record the flow "
                  "past each unit's lower boundary. Mines report their discharges monthly under their licences.",
                  st["p"]),
        Paragraph("Table 2. Sulfate load allocations", st["h"]),
        _table(alloc, [22, 30, 66, 24, 28], st),
    ]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title="Sulfate Load Allocation Schedule", author="Umzimela CMA",
                            creator="Umzimela CMA", producer="Umzimela CMA", invariant=1)
    doc.build(blocks)
    fix_dates(path, "D:20250303141200+02'00'", "D:20250317093500+02'00'")
