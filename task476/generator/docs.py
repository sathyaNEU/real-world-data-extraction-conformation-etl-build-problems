"""The pack's documents: the program guidelines (PDF), the extract notes (txt), the customer counts workbook and the
lost-and-unaccounted-for gas report (the last two are distractors)."""
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                    # noqa: E402
from reportlab.lib.pagesizes import letter                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                     # noqa: E402
from reportlab.lib.units import inch                                # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle  # noqa: E402
from openpyxl import Workbook                                       # noqa: E402
from openpyxl.styles import Alignment, Font                         # noqa: E402

import world as W   # noqa: E402

SECTIONS = {"designation": "2.1", "methane": "2.2", "miles": "2.3", "reporting": "3.1"}
BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.5, spaceAfter=6)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=15, leading=19, spaceAfter=4)
SUB = ParagraphStyle("s", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#444444"),
                     spaceAfter=10)


def _doc(path, title):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                          topMargin=0.9 * inch, bottomMargin=0.9 * inch, title=title, author=W.UTILITY,
                          creator=W.UTILITY, producer=W.UTILITY, subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.95 * inch, 0.55 * inch, "%s  |  %s" % (W.UTILITY, title))
        c.drawRightString(letter[0] - 0.95 * inch, 0.55 * inch, "Page %d" % d_.page)
        c.restoreState()
    return d, frame


def _table(rows, widths):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9), ("FONT", (0, 1), (-1, -1), "Times-Roman", 10),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def write_guidelines(path):
    title = "Accelerated Main Replacement Program 2027-2029: Guidelines"
    d, frame = _doc(path, title)
    s = [Paragraph("Accelerated Main Replacement Program 2027-2029: District Designation Guidelines", TITLE),
         Paragraph("%s, %s. Issued %s." % (W.UTILITY, W.DEPT, W.GUIDELINE_DATE), SUB)]
    secs = [
        ("1. Purpose", [
            "1.1 The program replaces cast-iron and bare-steel distribution mains, with their services, in designated "
            "districts ahead of the base replacement schedule. The City Council approves the program's capital budget "
            "for 2027 to 2029 in its 2027 budget round."]),
        ("2. Designation", [
            "%s A district is designated when its 2026 leak methane per mile of cast-iron and bare-steel main is %.2f "
            "tonnes or more." % (SECTIONS["designation"], W.LINE),
            "%s A district's 2026 leak methane is the methane emitted by the leaks found in calendar 2026 on its "
            "cast-iron and bare-steel mains and their services, whether found at the district's leak survey or after "
            "an odor call, each from when the leak began until it was repaired, or until 31 December 2026 if it had "
            "not been repaired by then, at the rate in Table 1 for the grade the leak was given when it was found. A "
            "leak found after an odor call began when the call was received. Dates and times are local (Central time)." %
            SECTIONS["methane"],
            "%s A district's miles of cast-iron and bare-steel main are its in-service cast-iron and bare-steel "
            "segments in the GIS on 31 December 2026." % SECTIONS["miles"]]),
        ("3. Reporting", [
            "%s The designation memo gives, for every district, its leaks found in 2026, its 2026 leak methane and its "
            "methane per mile; and, for the Council's budget hearing, its 2026 leak repair cost (the cost posted to its "
            "leaks' work orders in calendar 2026) and its 2026 customer interruptions from leak repairs (each "
            "customer's service shut off for a leak repair in 2026, counted once for each shut-off; a customer is a "
            "meter). A district's "
            "leaks are those on its own mains." % SECTIONS["reporting"]]),
    ]
    for h, ps in secs:
        s.append(Paragraph(h, HEAD))
        for p in ps:
            s.append(Paragraph(p, BODY))
    s.append(Paragraph("Table 1. Leak methane emission rate by grade", HEAD))
    s.append(_table([["Grade", "Description", "Methane, kg per hour"],
                     ["1", "Hazardous: repaired at once", "%.2f" % W.RATE[1]],
                     ["2", "Non-hazardous, scheduled for repair", "%.2f" % W.RATE[2]],
                     ["3", "Non-hazardous, monitored", "%.2f" % W.RATE[3]]], [0.7 * inch, 3.6 * inch, 1.7 * inch]))
    s.append(Paragraph("4. Timeline", HEAD))
    s.append(_table([["Date", "Step"], ["15 March 2027", "Integrity data extract"],
                     ["20 April 2027", "Designation memo to the City Council"],
                     ["18 May 2027", "Council budget hearing"], ["1 July 2027", "Program begins"]],
                    [1.4 * inch, 4.9 * inch]))
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_notes(path, n):
    F = W.FILES
    lines = [
        "%s - DISTRIBUTION INTEGRITY DATA EXTRACT NOTES" % W.UTILITY.upper(),
        "Extract date 03/15/2027",
        "",
        "%s  (%d rows)" % (F["schedule"], n["schedule"]),
        "  One row per main segment per survey year: the date the segment was walked by the leak survey crew.",
        "  Each district is walked once a year in its scheduled month.",
        "",
        "%s  (%d rows)" % (F["finds"], n["finds"]),
        "  Leaks found by the leak survey. found_local is the time the leak was found. Grades were A, B, C before",
        "  01/01/2025 and 1, 2, 3 after (A is 1).",
        "",
        "%s  (%d rows)" % (F["odor"], n["odor"]),
        "  Every odor call received. received_utc is in UTC. A call that found a leak carries its leak number.",
        "",
        "%s  (%d rows)" % (F["repairs"], n["repairs"]),
        "  Every repair-crew visit to a leak: CHECKED, MONITORED or REPAIRED, with the grade at the visit.",
        "",
        "%s  (%d rows)" % (F["mains"], n["mains"]),
        "  In-service main segments on 12/31/2026: district, material, length in feet.",
        "",
        "%s  (%d rows)" % (F["costs"], n["costs"]),
        "  Postings to leak work orders. cost_center is the district of the crew that did the work.",
        "",
        "%s  (%d rows)" % (F["closeouts"], n["closeouts"]),
        "  Leak work orders closed in 2025 or 2026: closing date and total cost.",
        "",
        "%s  (%d rows)" % (F["tickets"], n["tickets"]),
        "  Service interruption tickets opened in 2026, one per service address shut off.",
        "",
        "%s  (%d rows)" % (F["meters"], n["meters"]),
        "  Meter premises: service address, district, the number of meters at the premise, its service line.",
    ]
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write("\n".join(lines) + "\n")


def write_customers(path, x):
    wb = Workbook()
    ws = wb.active
    ws.title = "Customers 2026"
    ws.append(["District", "Residential customers", "Commercial customers", "Total"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for d in W.DISTRICTS:
        res = sum(p["meters"] for p in x["prem"] if p["district"] == d)
        com = int(res * 0.08)
        ws.append([d, res, com, res + com])
    for col, w in zip("ABCD", [16, 20, 20, 10]):
        ws.column_dimensions[col].width = w
    wb.save(path)


def write_lauf(path):
    title = "Lost and Unaccounted-for Gas, 2026"
    d, frame = _doc(path, title)
    s = [Paragraph("Lost and Unaccounted-for Gas: 2026 Annual Report", TITLE),
         Paragraph("%s, Gas Supply and Measurement. February 2027." % W.UTILITY, SUB),
         Paragraph("Lost and unaccounted-for gas (LAUF) is the difference between gas received at the city gate "
                   "stations and gas delivered through customer meters, adjusted for company use and for meter-reading "
                   "cycle timing. For 2026 it was 1.84 per cent of receipts, against 1.91 per cent in 2025 and a "
                   "five-year average of 1.97 per cent.", BODY),
         Paragraph("LAUF includes measurement differences at the gate stations and customer meters, theft, and "
                   "leakage. It is reported for the whole system; it is not allocated to districts.", BODY),
         _table([["Year", "Receipts (MMcf)", "LAUF (MMcf)", "LAUF %"], ["2022", "41,206", "830", "2.01"],
                 ["2023", "39,884", "793", "1.99"], ["2024", "40,512", "798", "1.97"], ["2025", "41,930", "801", "1.91"],
                 ["2026", "41,377", "761", "1.84"]], [1.0 * inch, 1.5 * inch, 1.3 * inch, 1.0 * inch])]
    d.build(s, onFirstPage=frame, onLaterPages=frame)
