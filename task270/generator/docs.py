"""The pack's documents for task270: Hallowmere's Refrigerant Strategy (revision 2026), Kelbray's service
specification, Tarnley's service description and Kelbray's 2026 KPI report (PDF), the data dictionary and the pack
contents."""
from __future__ import annotations

import csv

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import mm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"),
              ("Sans-I", "LiberationSans-Italic"), ("Serif", "LiberationSerif-Regular"),
              ("Serif-B", "LiberationSerif-Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1d2126"), colors.HexColor("#5b636d"), colors.HexColor("#c3c9d0")
TEAL = colors.HexColor("#14545a")
NAVY = colors.HexColor("#1d3557")


def uk(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def styles(face, accent):
    body = ParagraphStyle("b", fontName=face, fontSize=9.8, leading=13.2, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=face + "-B", fontSize=14, leading=17.5, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=face + "-B", fontSize=10.4, leading=13.5, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=face, fontSize=8.4, leading=11, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=face, fontSize=8.2, leading=10.2, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=face + "-B", fontSize=8.2, leading=10.2, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=24, firstLineIndent=-24),
        note=ParagraphStyle("n", fontName=face, fontSize=7.9, leading=10.2, textColor=GREY, spaceBefore=4))


def _frame(left, right, face):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(face, 7.4)
        canvas.drawString(20 * mm, A4[1] - 13 * mm, left)
        canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 13 * mm, right)
        canvas.drawCentredString(A4[0] / 2.0, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.6),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _build(path, story, left, right, title, author, face="Sans"):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm,
                            bottomMargin=18 * mm, title=title, author=author, subject="", creator="", producer="")
    fr = _frame(left, right, face)
    doc.build(story, onFirstPage=fr, onLaterPages=fr)


def strategy(path):
    S = styles("Sans", TEAL)
    P = lambda t, s="body": Paragraph(t, S[s])   # noqa: E731
    gw = [["Refrigerant", "GWP"]] + [[g, "{:,}".format(K.GWP[g])] for g in
                                     ("R404A", "R407F", "R448A", "R449A", "R134a", "R290", "R744")]
    st = [P(K.ORG_LTD, "meta"), P("Refrigerant Strategy", "h1"),
          P("Revision 2026, approved by the Executive Committee on %s. Owner: Head of Property and Sustainability."
            % uk(K.STRATEGY_DATE), "meta"),
          P("1. Purpose", "h2"),
          P("We are moving our refrigeration off HFC refrigerants. This strategy sets the order in which our "
            "central refrigeration packs are replaced with transcritical CO2 packs and how we account for the "
            "refrigerant our equipment releases. Integral cabinets and cold rooms are replaced at the end of their "
            "lives and are outside the pack programme."),
          P("2. Terms", "h2"),
          P("2.1&nbsp;&nbsp;A <i>pack</i> is a central refrigeration plant serving a store's cases and cold rooms, "
            "listed on the Packs sheet of the F-gas register with its full charge.", "clause"),
          P("2.2&nbsp;&nbsp;A pack's <i>loss</i> in a year is the refrigerant that escaped from it during that "
            "calendar year.", "clause"),
          P("2.3&nbsp;&nbsp;A pack is <i>in service throughout</i> a year when it was in service on 1 January and "
            "had not been decommissioned by 31 December.", "clause"),
          P("2.4&nbsp;&nbsp;Carbon dioxide equivalent is counted at the global warming potentials of the GB "
            "F-gas Regulation, as listed below.", "clause"),
          _table(S, gw, (40, 30), right=(1,)),
          P("3. The pack programme", "h2"),
          P("Packs are replaced region by region, one region a year, by Kelbray Refrigeration's projects team. "
            "The programme starts in the region whose HFC packs in service throughout the year lost, together, the "
            "largest share of their full charge in that year: the region's packs' losses added up and set against "
            "their full charges added up. For the 2027 programme the year is 2026, and the region is fixed when "
            "the 2026 records close."),
          P("4. Records", "h2"),
          P("Kelbray Refrigeration keeps the F-gas records of every job on our equipment. The F-gas register is kept "
            "by the property team and updated from Kelbray's commissioning and decommissioning certificates."),
          Spacer(1, 6),
          P("Questions on this strategy go to %s, Head of Property and Sustainability." % K.REQUESTER, "note")]
    _build(path, st, K.ORG, "Refrigerant Strategy, revision 2026", "Refrigerant Strategy", K.ORG)


def spec(path):
    S = styles("Serif", NAVY)
    P = lambda t, s="body": Paragraph(t, S[s])   # noqa: E731
    st = [P(K.CONTRACTOR_LTD, "meta"), P("Service Specification: Hallowmere Foodstores refrigeration", "h1"),
          P("Schedule 2 to the maintenance contract, issued %s." % uk(K.SPEC_DATE), "meta"),
          P("1. Routine visits", "h2"),
          P("Each pack is visited twice a year on the regional team's routine round. At a routine visit the engineer "
            "leak tests the pack, reads the receiver level and charges refrigerant where the pack is short. Rounds "
            "are planned by each regional team and run over about three weeks."),
          P("2. Breakdowns", "h2"),
          P("Tarnley raises a low-level alarm when a pack's receiver level falls below 25 per cent. The regional "
            "team attends, finds and repairs the leak and restores the charge."),
          P("3. Charging and recovery", "h2"),
          P("Refrigerant is charged from cylinders weighed on a calibrated scale before and after the charge; the "
            "job sheet records the kilograms charged and the cylinder log the weights. Refrigerant recovered from a "
            "pack (to change a component, at a retrofit or at decommissioning) is weighed into a recovery cylinder "
            "and recorded on the job sheet. On pack jobs the engineer records the receiver level on arrival and on "
            "departure, read from the pack controller."),
          P("4. Integral cabinets and cold rooms", "h2"),
          P("Integral cabinets and cold rooms are repaired on breakdown. Propane (R290) cabinets are sealed units "
            "and are exchanged, not recharged."),
          P("5. Records", "h2"),
          P("Job sheets are completed on the engineer's handheld and exported to Hallowmere monthly. Each sheet "
            "line is one asset on one job."),
          Spacer(1, 6),
          P("Contract manager: %s." % K.CONTRACTS, "note")]
    _build(path, st, K.CONTRACTOR_LTD, "Schedule 2: Service Specification", "Service Specification",
           K.CONTRACTOR_LTD, face="Serif")


def bureau(path):
    S = styles("Sans", NAVY)
    P = lambda t, s="body": Paragraph(t, S[s])   # noqa: E731
    st = [P(K.BUREAU, "meta"), P("Service description: receiver level monitoring", "h1"),
          P("Issued %s for Hallowmere Foodstores." % uk(K.BUREAU_DOC_DATE), "meta"),
          P("What we log", "h2"),
          P("Each pack controller reports its receiver liquid level as a percentage of the receiver's working "
            "range every hour. Our daily export gives, for each pack and day, the mean of that day's hourly readings "
            "and the number of readings it was taken over. Days with no readings (a communications outage) are not "
            "exported; a reading the controller marks as a probe fault is exported blank with status SENSOR FAULT."),
          P("Alarms", "h2"),
          P("A low-level alarm is raised when the hourly reading falls below 25 per cent and is passed to the "
            "maintenance contractor."),
          P("Identifiers", "h2"),
          P("Packs are identified by our site tag (HFS, the store number and the pack). The tag list gives the "
            "customer's pack code for each tag."),
          Spacer(1, 6)]
    _build(path, st, K.BUREAU, "Receiver level monitoring", "Service description", K.BUREAU)


def kpi(path, stats):
    S = styles("Serif", NAVY)
    P = lambda t, s="body": Paragraph(t, S[s])   # noqa: E731
    rows = [["Region", "Routine visits", "Breakdowns attended", "Median hours to attend", "First-time fix"]]
    for reg in K.REGIONS:
        a = stats[reg]
        rows.append([K.REGION_NAME[reg], a["routine"], a["breakdown"], a["hours"], "%d%%" % a["fix"]])
    st = [P(K.CONTRACTOR_LTD, "meta"), P("Hallowmere Foodstores: service report, January to December 2026", "h1"),
          P("Prepared for the quarterly contract review.", "meta"),
          P("Service levels", "h2"),
          _table(S, rows, (34, 28, 34, 38, 26), right=(1, 2, 3, 4)),
          P("Breakdowns are counted from the alarm hand-over to the engineer's arrival on site; first-time fix is the "
            "share of breakdowns closed without a return visit."),
          Spacer(1, 6)]
    _build(path, st, K.CONTRACTOR_LTD, "Service report 2026", "Service report", K.CONTRACTOR_LTD, face="Serif")


DICTIONARY = [
    ("hallowmere_stores.csv", "store_no", "Hallowmere store number, three digits"),
    ("hallowmere_stores.csv", "region", "Trading region"),
    ("hallowmere_stores.csv", "closed", "Date the store closed, day first; blank if trading"),
    ("fgas_register_2026.xlsx", "Packs: Pack", "Pack code: store number and pack (LT low temperature, MT medium)"),
    ("fgas_register_2026.xlsx", "Packs: Refrigerant", "Refrigerant on the register"),
    ("fgas_register_2026.xlsx", "Packs: Full charge (kg)", "The pack's full charge"),
    ("fgas_register_2026.xlsx", "Packs: In service from", "Date the pack entered service, day first"),
    ("fgas_register_2026.xlsx", "Packs: Decommissioned", "Date the pack was decommissioned, day first"),
    ("fgas_register_2026.xlsx", "Cabinets and cold rooms: Asset", "Asset number on the cabinet or cold room"),
    ("kelbray_job_sheets_2024_2026.csv", "store", "Store number as Kelbray's system holds it"),
    ("kelbray_job_sheets_2024_2026.csv", "asset", "Pack (LT1, MT1, MT2) or the asset number of a cabinet or cold room"),
    ("kelbray_job_sheets_2024_2026.csv", "charged_kg", "Refrigerant charged on the job"),
    ("kelbray_job_sheets_2024_2026.csv", "recovered_kg", "Refrigerant recovered on the job"),
    ("kelbray_job_sheets_2024_2026.csv", "receiver_arrival_pct", "Pack receiver level when the engineer arrived"),
    ("kelbray_job_sheets_2024_2026.csv", "receiver_departure_pct", "Pack receiver level when the engineer left"),
    ("kelbray_cylinder_log_2026.csv", "gross_before_kg", "Cylinder weight before the job, cylinder included"),
    ("kelbray_cylinder_log_2026.csv", "gross_after_kg", "Cylinder weight after the job, cylinder included"),
    ("tarnley_receiver_levels_2024_2026.csv", "receiver_level_pct", "Mean of the day's hourly receiver readings"),
    ("tarnley_receiver_levels_2024_2026.csv", "readings", "Hourly readings the mean is taken over"),
    ("tarnley_pack_tags.csv", "pack_code", "Hallowmere pack code for the Tarnley tag"),
    ("store_electricity_2024_2026.csv", "kwh", "Electricity billed for the month"),
]


def dictionary(path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["file", "field", "description"])
        w.writerows(DICTIONARY)


def contents(path, counts):
    lines = ["Hallowmere Foodstores: 2027 pack programme papers", "Assembled %s by the property team." % uk(K.ASSEMBLED),
             ""]
    desc = [("refrigerant_strategy_2026.pdf", "Refrigerant Strategy, revision 2026"),
            ("fgas_register_2026.xlsx", "F-gas register: packs, integral cabinets and cold rooms"),
            ("hallowmere_stores.csv", "Store list"),
            ("kelbray_job_sheets_2024_2026.csv", "Kelbray job sheets, January 2024 to December 2026"),
            ("kelbray_cylinder_log_2026.csv", "Kelbray cylinder log, 2026"),
            ("kelbray_service_specification_2024.pdf", "Kelbray service specification (contract schedule 2)"),
            ("kelbray_kpi_report_2026.pdf", "Kelbray service report, 2026"),
            ("tarnley_receiver_levels_2024_2026.csv", "Tarnley daily receiver levels, 2024 to 2026"),
            ("tarnley_pack_tags.csv", "Tarnley tag list"),
            ("tarnley_service_description_2025.pdf", "Tarnley service description"),
            ("store_electricity_2024_2026.csv", "Store electricity, monthly"),
            ("data_dictionary.csv", "Field notes")]
    for f, d in desc:
        lines.append("%-42s %s" % (f, d))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
