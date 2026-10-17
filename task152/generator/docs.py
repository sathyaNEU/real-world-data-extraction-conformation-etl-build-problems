"""The pack's documents: the treasury's energy risk policy, the module replacement scope (Word), the O&M agreement's
cleaning and availability schedules, the interconnection agreement's metering exhibit, Corvane's side-by-side
report, the two module datasheets, the Westmark confirmations, the district's 2025 interruption report, Tresco's
repowering program summary and the README. Their text is kept here as data so checks.py can quote and execute it."""
from __future__ import annotations

import datetime as dt
import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("LibSerif", "liberation/LiberationSerif-Regular.ttf"), ("LibSerif-Bold", "liberation/LiberationSerif-Bold.ttf"),
               ("LibMono", "liberation/LiberationMono-Regular.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1f2329")
GREY = colors.HexColor("#5f6670")
MV = colors.HexColor("#7a4a12")          # Marden-Vail's ochre
TIANRUN = colors.HexColor("#0f5c8a")
TRESCO = colors.HexColor("#2f6b3a")
VSIPD = colors.HexColor("#1e3f66")
WEST = colors.HexColor("#4a2f6b")
RULE = colors.HexColor("#a3abb5")
HEAD = colors.HexColor("#e7ebf0")


def styles(font, bold, accent, size=10.2):
    return dict(
        body=ParagraphStyle("b" + font, fontName=font, fontSize=size, leading=size * 1.36, textColor=INK, spaceAfter=5),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=14.5, leading=18.5, textColor=accent, spaceAfter=3),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=8.9, leading=11.8, textColor=GREY, spaceAfter=9),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=10.8, leading=14.0, textColor=accent, spaceBefore=7,
                          spaceAfter=3),
        cell=ParagraphStyle("c" + font, fontName=font, fontSize=8.4, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb" + font, fontName=bold, fontSize=8.4, leading=10.4, textColor=INK),
        small=ParagraphStyle("sm" + font, fontName=font, fontSize=8.2, leading=10.6, textColor=GREY, spaceAfter=4))


def _doc(path, title, author, margins=1.0):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=margins * inch, rightMargin=margins * inch,
                             topMargin=0.8 * inch, bottomMargin=0.8 * inch, title=title, author=author, subject="",
                             creator="", producer="")


def _footer(left, font="Carlito", right="Page "):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(0.9 * inch, 0.5 * inch, left)
        canvas.drawRightString(letter[0] - 0.9 * inch, 0.5 * inch, "%s%d" % (right, doc.page))
        canvas.restoreState()
    return draw


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("$", "&#36;")


def grid(rows, widths, st, head=True, align_right=()):
    data = []
    for k, row in enumerate(rows):
        data.append([Paragraph(esc(str(c)), st["cellb"] if (head and k == 0) else st["cell"]) for c in row])
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1 if head else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), HEAD))
    t.setStyle(TableStyle(style))
    return t


def sentences(paras):
    return [s for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9(])", p)]


# ---------------------------------------------------------------------------------------------------- the policy
F_POLICY = "marden-vail_energy_risk_policy_rev4.pdf"
POLICY = [
    ("1", "Purpose", "purpose", [
        "1.1 Marden-Vail buys the power its Arizona plants use at retail and owns Hadley Ranch Solar, whose output it "
        "sells into the Palo Verde market. This policy sets how much of the plant's output the energy and commodities "
        "desk sells forward, so that the price of that part of the output is fixed a year ahead.",
        "1.2 The policy applies to forward sales of Hadley Ranch Solar's output. Retail supply contracts for the "
        "company's plants are covered by the procurement policy."]),
    ("2", "The hedge year", "year", [
        "2.1 The hedge year is the calendar year, January 1 to December 31.",
        "2.2 The desk sells each hedge year's volume forward by October 31 of the year before, in one or more trades "
        "with counterparties on the approved list, as a fixed-volume product in the plant's solar shape."]),
    ("3", "The quantity hedged", "quantity", [
        "3.1 The quantity hedged is the plant's net energy at its delivery point: the energy the revenue meter at the "
        "district's Hadley Ranch 69 kV substation registers as received from the plant, less the energy it registers "
        "as delivered to the plant."]),
    ("4", "The volume", "volume", [
        "4.1 The volume for a hedge year is the plant's one-year P90 for that year, rounded down to the nearest "
        "1,000 MWh.",
        "4.2 The one-year P90 is the P50 less 1.2816 standard deviations. Both are taken over the plant's annual net "
        "energy under the weather of each full calendar year of the long-term irradiance record: the energy the "
        "plant, as it will stand in the hedge year, would deliver in a year with that year's weather. The P50 is the "
        "mean of those annual energies and the standard deviation is their sample standard deviation.",
        "4.3 The long-term irradiance record is the irradiance provider's site-adapted series for the plant, as last "
        "delivered.",
        "4.4 For a plant in operation, the annual energies are built from its own monitoring record, with the twelve "
        "complete months before the sale as the base period."]),
    ("5", "Approval", "approval", [
        "5.1 The desk brings each hedge year's volume to the treasurer in October with the workbook it rests on. The "
        "treasurer approves the volume or sets a lower one.",
        "5.2 Trades are executed by the energy and commodities manager or the treasurer and confirmed in writing by "
        "the counterparty."]),
]


def write_policy(path):
    st = styles("LibSerif", "LibSerif-Bold", MV, 10.4)
    s = [Paragraph("Marden-Vail Building Products, Inc. &middot; Treasury", st["sub"]),
         Paragraph("Energy Risk Policy", st["h1"]),
         Paragraph("Revision 4, approved by the board's audit and finance committee on February 13, 2024. Supersedes "
                   "revision 3 (March 2, 2021). Policy owner: %s, Treasurer." % K.PEOPLE["treasurer"], st["sub"])]
    for num, head, _, paras in POLICY:
        s.append(Paragraph("%s&nbsp;&nbsp;%s" % (num, head), st["h2"]))
        for p in paras:
            s.append(Paragraph(esc(p), st["body"]))
    doc = _doc(path, "Energy Risk Policy, Revision 4", K.PEOPLE["treasurer"])
    f = _footer("Marden-Vail Building Products  |  Energy Risk Policy rev. 4  |  Confidential", font="LibSerif")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- the scope (Word)
F_SCOPE = "hadley_ranch_module_replacement_scope_2026-07.docx"
SCOPE = [
    ("Background", [
        "Hadley Ranch Solar has run since November 20, 2015 on 128,000 Kellerman KS-315P polycrystalline modules "
        "(40,320 kWp), 8,000 to each of the sixteen central inverters as 400 strings of 20. The plant's output has "
        "fallen since 2017, and the 2019 survey found cracked backsheets in all four blocks. Kellerman "
        "Solar left the module business in 2020 and no warranty settlement was reached. In June 2026 the board "
        "approved replacing every module."]),
    ("What is replaced", [
        "All 128,000 original modules are replaced with 82,944 Corvane CV-450BHC bifacial modules of 450 W, mounted on "
        "the existing fixed tables (25 degrees, facing south). Each inverter's array is restrung as 288 strings of 18 "
        "modules: 2,332.8 kWp per inverter and 37,324.8 kWp for the plant.",
        "The string length is set by the inverters' 1,000 V DC input limit at the site's record low temperature. The "
        "string count keeps each inverter's AC output under its 2,500 kW rating with the rear-side gain the site's "
        "ground gives; only the odd cloud-edge hour on a bright spring day reaches it."]),
    ("What stays", [
        "The tables and foundations, the DC cabling and combiner boxes, the sixteen central inverters, the 34.5 kV "
        "collection system, the substation and the district's revenue meter stay as they are. Tresco Field Services "
        "continues to operate, wash and maintain the plant under the current O&M agreement, which runs to December "
        "31, 2027."]),
    ("Schedule", [
        "The works run from October 5 to December 18, 2026, one block at a time, about eighteen working days a block. "
        "Each block returns to service with its new modules as it is finished, and the whole plant runs on the new "
        "modules from December 19, 2026. Tresco's December wash goes ahead as usual, one block a week, each block "
        "after Corvane hands it back.",
        "Corvane's side-by-side comparison inside block 3 ran from October 1, 2025 to September 30, 2026; its report "
        "is due in the first week of October."]),
    ("Contract", [
        "Supply and installation by Corvane Solar (Americas) under the contract signed on June 30, 2026, at a "
        "fixed price of $14.62 million including removal and recycling of the original modules. Liquidated damages "
        "apply for each block day beyond the schedule."]),
]


def scope_sentences():
    return sentences([p for _, ps in SCOPE for p in ps])


def write_scope(path):
    d = Document()
    stn = d.styles["Normal"]
    stn.font.name = "Calibri"
    stn.font.size = Pt(11)
    t = d.add_paragraph()
    run = t.add_run("Hadley Ranch Solar: module replacement, scope and schedule")
    run.bold = True
    run.font.size = Pt(15)
    run.font.color.rgb = RGBColor(0x7A, 0x4A, 0x12)
    m = d.add_paragraph()
    r2 = m.add_run("For the treasurer and the executive team. %s, Solar Asset Manager. July 8, 2026." % K.PEOPLE["asset"])
    r2.italic = True
    r2.font.size = Pt(9.5)
    for head, paras in SCOPE:
        h = d.add_paragraph()
        hr = h.add_run(head)
        hr.bold = True
        hr.font.size = Pt(11.5)
        for p in paras:
            q = d.add_paragraph(p)
            q.alignment = WD_ALIGN_PARAGRAPH.LEFT
    d.core_properties.title = "Hadley Ranch Solar module replacement"
    d.save(path)


# ---------------------------------------------------------------------------------------------------- the O&M agreement
F_OM = "tresco_om_agreement_2021_schedules_2_and_4.pdf"
OM_S2 = [
    "2.1 The Contractor shall wash every module in the Facility once in each Contract Year. The wash is carried out "
    "block by block in December, one block each week, each block in one working day where the weather allows.",
    "2.2 The Contractor shall carry out further washes of one or more blocks at the Owner's written request, at the "
    "rate per block in Schedule 6.",
    "2.3 Washing uses deionized water drawn from the Facility's Well 2 under the Owner's groundwater permit, whose "
    "weekly limit covers one block's wash. No further washes are requested or carried out while a drought restriction "
    "on non-essential industrial water use applies to that permit.",
    "2.4 The Contractor shall clean the meteorological station's pyranometer domes and check their level at every "
    "site round, and in any case at least once a week."]
OM_S4 = [
    "4.1 In this Schedule: Contract Year means a calendar year; Inverter means each of the sixteen central inverters "
    "of the Facility, and any inverter that replaces one of them; Production Hour means each clock hour, in Arizona "
    "time, in which the mean plane-of-array irradiance measured at the Facility's meteorological station is at least "
    "50 W/m2.",
    "4.2 An Unavailable Hour of an Inverter is a Production Hour in which the Inverter delivers no AC energy, other "
    "than an Excluded Hour. An Excluded Hour of an Inverter is a Production Hour in which the Inverter delivers no AC "
    "energy because of (a) an outage, curtailment or instruction of the Utility's system; (b) a stop the Owner has "
    "requested; or (c) Force Majeure.",
    "4.3 The Availability of an Inverter for a Contract Year is one less the ratio of its Unavailable Hours to its "
    "Production Hours less its Excluded Hours, expressed as a percentage to two decimal places.",
    "4.4 The Contractor guarantees an Availability of each Inverter of at least 98.0 per cent in each Contract Year. "
    "For each Inverter below the guarantee the Contractor shall pay the Owner liquidated damages of $1,850 for each "
    "tenth of a percentage point, or part of one, by which its Availability falls short.",
    "4.5 The Contractor shall report each Inverter's Availability for a Contract Year within 30 days after its end, "
    "with the hours it has counted as Excluded Hours and their causes."]


def write_om(path):
    st = styles("LibSans", "LibSans-Bold", TRESCO, 9.8)
    s = [Paragraph("Operations and Maintenance Agreement &middot; Hadley Ranch Solar", st["sub"]),
         Paragraph("Schedules 2 and 4", st["h1"]),
         Paragraph("Agreement dated December 18, 2020 between Marden-Vail Building Products, Inc. (the Owner) and "
                   "Tresco Field Services, LLC (the Contractor), for the term January 1, 2021 to December 31, 2027. "
                   "Extract of the executed copy.", st["sub"]),
         Paragraph("Schedule 2. Module cleaning", st["h2"])]
    for p in OM_S2:
        s.append(Paragraph(esc(p), st["body"]))
    s.append(Paragraph("Schedule 4. Availability guarantee", st["h2"]))
    for p in OM_S4:
        s.append(Paragraph(esc(p), st["body"]))
    s.append(Spacer(1, 10))
    s.append(Paragraph("Initialed for the Owner: CB &nbsp;&nbsp;&nbsp; Initialed for the Contractor: JD", st["small"]))
    doc = _doc(path, "O&M Agreement, Schedules 2 and 4", "Tresco Field Services")
    f = _footer("Hadley Ranch Solar O&M Agreement  |  Execution version", font="LibSans")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- exhibit C
F_EXHIBIT = "vsipd_lgia_hadley_ranch_exhibit_c_metering.pdf"
EXHIBIT = [
    ("C.1", "Revenue Meter", [
        "C.1.1 The Revenue Meter is the District's meter 69R0417A at the 69 kV Point of Interconnection in the Hadley "
        "Ranch substation, service point 0417. It is a bidirectional revenue-class meter (accuracy class 0.2S) with "
        "two energy channels: REC, the energy the District receives from the Facility, and DEL, the energy the "
        "District delivers to the Facility.",
        "C.1.2 The District tests the Revenue Meter every two years and after any repair. The Interconnection Customer "
        "may read the Revenue Meter's registers through its own SCADA by the meter's optical port and pulse "
        "outputs."]),
    ("C.2", "Station service", [
        "C.2.1 The Facility's control building and Well 2 have been supplied by the District as a retail customer at "
        "service point 0418, under the District's general service rate GS-3, from the 12 kV Vado Seco feeder 12-14, "
        "with the District's meter 12S0418C.",
        "C.2.2 With the retirement of feeder 12-14 the District closes service point 0418 on April 17, 2024. From "
        "that date the control building and Well 2 are supplied from the Facility's 34.5 kV collection system "
        "through the Interconnection Customer's own auxiliary transformer, on the Facility side of the Revenue "
        "Meter."]),
    ("C.3", "Data", [
        "C.3.1 The District makes the daily totals of each meter on the Interconnection Customer's account available "
        "through its customer data portal, and supplies interval data on request."]),
]


def write_exhibit(path):
    st = styles("LibSerif", "LibSerif-Bold", VSIPD, 10.0)
    s = [Paragraph("Large Generator Interconnection Agreement between Vado Seco Irrigation and Power District and "
                   "Marden-Vail Building Products, Inc.", st["sub"]),
         Paragraph("Exhibit C. Metering", st["h1"]),
         Paragraph("As amended by Amendment No. 2, executed March 21, 2024, effective April 17, 2024.", st["sub"])]
    for num, head, paras in EXHIBIT:
        s.append(Paragraph("%s&nbsp;&nbsp;%s" % (num, head), st["h2"]))
        for p in paras:
            s.append(Paragraph(esc(p), st["body"]))
    doc = _doc(path, "LGIA Exhibit C Metering", "Vado Seco Irrigation and Power District")
    f = _footer("VSIPD  |  LGIA Hadley Ranch Solar  |  Exhibit C (Amendment No. 2)", font="LibSerif")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- the side-by-side report
F_RIG = "corvane_fa-2026-114_hadley_ranch_side_by_side.pdf"
RIG_TEXT = {
    "setup": [
        "Two tables were set up at the north edge of block 3. Table A carries 18 Kellerman KS-315P modules (5.67 kWp) "
        "taken unopened from the site's spares store, where they had been kept since 2015. Table B carries 12 "
        "CV-450BHC bifacial modules (5.40 kWp) drawn from the production lot shipped for the replacement. Both tables "
        "match the plant's tables in tilt (25 degrees), azimuth (south), height and row spacing.",
        "Each table is one string on its own string inverter, with the DC energy at the inverter input logged every "
        "five minutes. Both tables were washed every Monday. The plane-of-array irradiation in the table below is "
        "the plant's meteorological station pyranometer."],
    "modules": [
        "The CV-450BHC modules were new at the start of the comparison, so its twelve months include their first-year "
        "stabilization. The KS-315P modules on table A had no field exposure before October 1, 2025."],
    "result": [
        "Over the twelve months table B delivered {gain:.1f} per cent more DC energy per kWp of nameplate than table A. "
        "The gain is highest from May to August, when the lower temperature coefficient of the CV-450BHC counts most, "
        "and lowest in December and January."],
}


def rig_months(W):
    import numpy as np
    out = []
    days = W.rig_days
    for y, m in [(2025, 10), (2025, 11), (2025, 12)] + [(2026, k) for k in range(1, 10)]:
        idx = [k for k, d in enumerate(days) if d.year == y and d.month == m]
        poa = float(sum(W.pyr_d[W.day_index[days[k]]] for k in idx))
        a = float(W.rig_ref[idx].sum()) / 5.67
        b = float(W.rig_new[idx].sum()) / 5.40
        out.append(((y, m), round(poa, 1), round(a, 1), round(b, 1)))
    return out


def rig_figures(W):
    rows = rig_months(W)
    ta = round(float(W.rig_ref.sum()) / 5.67, 1)
    tb = round(float(W.rig_new.sum()) / 5.40, 1)
    tp = round(sum(r[1] for r in rows), 1)
    return rows, tp, ta, tb


def write_rig(path, W):
    st = styles("LibSans", "LibSans-Bold", TIANRUN, 9.6)
    rows, tp, ta, tb = rig_figures(W)
    gain = 100.0 * (tb / ta - 1.0)
    s = [Paragraph("Corvane Solar (Americas) &middot; Field Applications &middot; Report FA-2026-114, issue 1", st["sub"]),
         Paragraph("Side-by-side field comparison at Hadley Ranch Solar: CV-450BHC against unexposed KS-315P", st["h1"]),
         Paragraph("October 1, 2025 to September 30, 2026. Issued October 2, 2026 by %s, Field Test Engineer, for "
                   "Marden-Vail Building Products." % K.PEOPLE["test"], st["sub"]),
         Paragraph("1&nbsp;&nbsp;Setup", st["h2"])]
    for p in RIG_TEXT["setup"]:
        s.append(Paragraph(esc(p), st["body"]))
    s.append(Paragraph("2&nbsp;&nbsp;Modules", st["h2"]))
    for p in RIG_TEXT["modules"]:
        s.append(Paragraph(esc(p), st["body"]))
    s.append(Paragraph("3&nbsp;&nbsp;Monthly results", st["h2"]))
    tab = [["Month", "Plane-of-array irradiation (kWh/m2)", "Table A, KS-315P (kWh/kWp)", "Table B, CV-450BHC (kWh/kWp)",
            "B over A"]]
    for (y, m), poa, a, b in rows:
        tab.append(["%s %d" % (K.MON3[m], y), "%.1f" % poa, "%.1f" % a, "%.1f" % b, "%.3f" % (b / a)])
    tab.append(["Twelve months", "%.1f" % tp, "%.1f" % ta, "%.1f" % tb, "%.3f" % (tb / ta)])
    s.append(grid(tab, [1.15, 1.45, 1.35, 1.45, 0.8], st))
    s.append(Spacer(1, 6))
    s.append(Paragraph("4&nbsp;&nbsp;Result", st["h2"]))
    for p in RIG_TEXT["result"]:
        s.append(Paragraph(esc(p.format(gain=gain)), st["body"]))
    s.append(Paragraph("Specific yields are DC energy at each string inverter's input over the table's nameplate DC "
                       "capacity at standard test conditions (front side for the bifacial modules).", st["small"]))
    doc = _doc(path, "FA-2026-114 Hadley Ranch side-by-side comparison", K.PEOPLE["test"], margins=0.9)
    f = _footer("Corvane Solar (Americas)  |  FA-2026-114 issue 1", font="LibSans")
    doc.build(s, onFirstPage=f, onLaterPages=f)
    return tb / ta


# ---------------------------------------------------------------------------------------------------- datasheets
F_SHEETS = "module_datasheets_ks-315p_cv-450bhc.pdf"
KS = [("Maximum power (Pmax)", "315 W"), ("Power tolerance", "0 to +5 W"), ("Voltage at Pmax", "36.6 V"),
      ("Current at Pmax", "8.61 A"), ("Open-circuit voltage", "45.1 V"), ("Short-circuit current", "9.09 A"),
      ("Module efficiency", "16.2%"), ("Cells", "72 polycrystalline, 156 x 156 mm"),
      ("Temperature coefficient of Pmax", "-0.42 %/degC"), ("Temperature coefficient of Voc", "-0.32 %/degC"),
      ("Temperature coefficient of Isc", "+0.05 %/degC"), ("Nominal operating cell temperature", "45 +/- 2 degC"),
      ("Maximum system voltage", "1,000 V DC"), ("Dimensions", "1,956 x 992 x 40 mm"), ("Weight", "26.5 kg"),
      ("Backsheet", "PA-based white backsheet"),
      ("Linear power warranty", "97.5% of nameplate in year 1, then no more than 0.7% a year; 80.7% at year 25")]
TR = [("Maximum power, front (Pmax)", "450 W"), ("Power tolerance", "0 to +5 W"), ("Bifaciality", "80 +/- 5%"),
      ("Voltage at Pmax", "41.8 V"), ("Current at Pmax", "10.77 A"), ("Open-circuit voltage", "49.6 V"),
      ("Short-circuit current", "11.42 A"), ("Module efficiency", "20.7%"), ("Cells", "144 half-cut monocrystalline"),
      ("Temperature coefficient of Pmax", "-0.29 %/degC"), ("Temperature coefficient of Voc", "-0.25 %/degC"),
      ("Temperature coefficient of Isc", "+0.046 %/degC"), ("Nominal module operating temperature", "43 +/- 2 degC"),
      ("Maximum system voltage", "1,500 V DC"), ("Dimensions", "2,094 x 1,038 x 30 mm"), ("Weight", "27.9 kg"),
      ("Construction", "glass-glass, 2.0 mm heat-strengthened glass both sides"),
      ("Linear power warranty", "98.0% of nameplate in year 1, then no more than 0.45% a year; 87.2% at year 30")]


def write_sheets(path):
    st = styles("LibSans", "LibSans-Bold", GREY, 9.4)
    s = []
    for maker, model, rev, rows, accent, note in [
            (K.OLD_MAKER, "KS-315P", "Datasheet KS-315P-US, rev. 2014-06", KS, colors.HexColor("#7d1f1f"),
             "Electrical values at standard test conditions: 1,000 W/m2, cell temperature 25 degC, AM 1.5."),
            (K.NEW_MAKER, "CV-450BHC", "Datasheet CV-450BHC-NA, rev. 2025-03", TR, TIANRUN,
             "Electrical values at standard test conditions, front side: 1,000 W/m2, cell temperature 25 degC, AM 1.5. "
             "Bifaciality is the ratio of rear to front Pmax at standard test conditions.")]:
        hs = ParagraphStyle("hh" + model, parent=st["h1"], textColor=accent)
        block = [Paragraph("%s &middot; %s" % (esc(maker), rev), st["sub"]), Paragraph(model, hs),
                 grid([["Parameter", "Value"]] + [list(r) for r in rows], [2.9, 3.6], st), Spacer(1, 4),
                 Paragraph(esc(note), st["small"]), Spacer(1, 18)]
        s.append(KeepTogether(block))
    doc = _doc(path, "KS-315P and CV-450BHC datasheets", "", margins=1.0)
    f = _footer("Module datasheets on file, Hadley Ranch Solar", font="LibSans")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- confirmations
F_CONF = "westmark_confirmations_hadley_ranch_cy2016-cy2026.pdf"


def conf_items(W):
    items = []
    for t in W.trades:
        side = "Seller: Marden-Vail Building Products, Inc. Buyer: Westmark Power Trading LLC." if t["side"] == "S" else \
            "Seller: Westmark Power Trading LLC. Buyer: Marden-Vail Building Products, Inc."
        items.append(dict(date=t["date"], ref=t["id"], title="Confirmation", lines=[
            "Trade date: %s. Reference: %s." % (K.us_date(t["date"]), t["id"]), side,
            "Product: fixed volume, Hadley Ranch solar shape, financially settled against the Palo Verde day-ahead index.",
            "Delivery period: January 1 to December 31, %d." % t["year"],
            "Contract Quantity: %s MWh for the delivery period, shaped by month as in Annex 1." % format(t["qty"], ","),
            "Fixed Price: $%.2f/MWh." % t["price"]]))
    amend_dates = {2021: dt.date(2021, 4, 20), 2024: dt.date(2024, 4, 9)}
    for y in (2021, 2024):
        ref = W.amend_trade[y]
        orig = [t for t in W.trades if t["id"] == ref][0]
        items.append(dict(date=amend_dates[y], ref=ref + "-A1", title="Amendment No. 1", lines=[
            "Date: %s. Amends the Confirmation of %s, reference %s." % (K.us_date(amend_dates[y]), K.us_date(orig["date"]), ref),
            "The Contract Quantity is amended to %s MWh for the delivery period January 1 to December 31, %d, the "
            "monthly shape in Annex 1 scaled to it, with effect from the date of this amendment for the months not yet "
            "settled and by a true-up in the next monthly settlement for the months already settled." % (
                format(W.amended[y], ","), y),
            "All other terms of the Confirmation are unchanged."]))
    items.sort(key=lambda x: (x["date"], x["ref"]))
    return items


def write_conf(path, W):
    st = styles("LibSans", "LibSans-Bold", WEST, 8.8)
    s = [Paragraph("Westmark Power Trading LLC &middot; Confirmations issued to Marden-Vail Building Products, Inc.",
                   st["sub"]),
         Paragraph("Hadley Ranch Solar forward sales, delivery years 2016 to 2026", st["h1"]),
         Paragraph("Copies from the desk's confirmation file, in date order. Each confirmation is subject to the EEI "
                   "Master Power Purchase and Sale Agreement between the parties dated October 2, 2015.", st["sub"])]
    for it in conf_items(W):
        block = [Paragraph("%s &middot; %s" % (it["title"], it["ref"]), st["h2"])]
        for ln in it["lines"]:
            block.append(Paragraph(esc(ln), st["body"]))
        block.append(Paragraph("Westmark Power Trading LLC, by %s, Director, Origination. Accepted for Marden-Vail "
                               "Building Products, Inc. by %s." % (K.PEOPLE["trader"], K.PEOPLE["desk"]), st["small"]))
        s.append(KeepTogether(block))
    doc = _doc(path, "Westmark confirmations, Hadley Ranch Solar", "Westmark Power Trading LLC", margins=0.9)
    f = _footer("Westmark Power Trading LLC  |  Confirmations", font="LibSans")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- interruptions 2025
F_INTERRUPT = "vsipd_interruptions_hadley_ranch_69kv_tap_2025.pdf"
CAUSES = {"monsoon": "Unplanned: monsoon storm, conductor contact on the Mesquite Draw to Hadley Ranch 69 kV line",
          "wind": "Unplanned: high wind, conductor slap on the Mesquite Draw to Hadley Ranch 69 kV line",
          "protection": "Unplanned: protection operation on the Mesquite Draw 69 kV bus, cause under review",
          "bird": "Unplanned: pole fire, structure 69-HR-114 (bird contact)"}


def interruptions(W):
    import common as KK
    r = KK.rng("interruptions")
    out = []
    lines = sorted([e for e in W.events if e["cause"] == "line" and e["start"].year == 2025], key=lambda e: e["start"])
    for n, e in enumerate(lines):
        rest = e["end"] - dt.timedelta(minutes=5)
        m = e["start"].month
        cause = CAUSES["monsoon" if m in (7, 8, 9) else ("wind" if m in (4, 5, 6) else ("protection" if m in (3, 10) else "bird"))]
        out.append(dict(ref="HR-25-%03d" % (n + 1), start=e["start"], rest=rest, cause=cause))
    return out


def write_interruptions(path, W):
    st = styles("LibSans", "LibSans-Bold", VSIPD, 9.4)
    rows = [["Ref", "Interruption (MST)", "Restoration (MST)", "Minutes", "Cause"]]
    for it in interruptions(W):
        mins = int(round((it["rest"] - it["start"]).total_seconds() / 60.0))
        rows.append([it["ref"], it["start"].strftime("%m/%d/%Y %H:%M"), it["rest"].strftime("%m/%d/%Y %H:%M"),
                     "%d" % mins, it["cause"]])
    rows.append(["HR-25-P07", "11/18/2025 08:00", "", "", "Planned: insulator washing, Mesquite Draw 69 kV yard. "
                 "Cancelled on 11/14/2025; no interruption."])
    s = [Paragraph("Vado Seco Irrigation and Power District &middot; System Operations", st["sub"]),
         Paragraph("Interruption report: Hadley Ranch 69 kV tap, calendar year 2025", st["h1"]),
         Paragraph("Issued January 14, 2026 to Marden-Vail Building Products, Inc. (account %s, service point 0417). "
                   "Times are Mountain Standard Time; restoration is the time the line was re-energized." % R.ACCOUNT,
                   st["sub"]),
         grid(rows, [0.8, 1.15, 1.15, 0.72, 3.0], st), Spacer(1, 8),
         Paragraph("Interruptions are recorded from the District's SCADA at the Mesquite Draw substation. Questions on "
                   "this report go to System Operations at the District's Coolidge office.", st["small"])]
    doc = _doc(path, "Interruption report Hadley Ranch 69 kV tap 2025", "VSIPD System Operations", margins=0.85)
    f = _footer("VSIPD System Operations  |  Interruption report 2025", font="LibSans")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- Tresco's program
F_TRESCO = "tresco_repowering_program_2019-2026.pdf"
TRESCO_PLANTS = [
    ("Palo Fierro Solar", "Yuma County, AZ", "20", "2012", "polycrystalline 300 W", "monofacial mono PERC 405 W", "Mar 2019", "+11.8"),
    ("Bisnaga Ridge Solar", "Maricopa County, AZ", "32", "2013", "polycrystalline 305 W", "bifacial mono PERC 440 W", "Nov 2020", "+16.9"),
    ("Red Tank Solar", "Clark County, NV", "25", "2014", "thin-film CdTe 110 W", "monofacial mono PERC 410 W", "Jan 2022", "+9.4"),
    ("Tinaja Flat Solar", "Imperial County, CA", "40", "2014", "polycrystalline 310 W", "bifacial TOPCon 445 W", "Dec 2023", "+14.6"),
    ("Dos Arroyos Solar", "Pima County, AZ", "15", "2011", "polycrystalline 290 W", "bifacial TOPCon 450 W", "Feb 2025", "+18.2"),
]
TRESCO_TEXT = [
    "Since 2019 Tresco has managed the repowering of five plants it operates in the Southwest, each with new modules "
    "on the original structures and inverters. The table gives each plant's energy at its revenue meter in the first "
    "full calendar year after the work against the last full calendar year before it.",
    "Results depend on each plant's original modules, its weather in the two years and the condition of its "
    "inverters and cleaning program. Tresco's repowering team prepares plant-specific estimates on request."]


def write_tresco(path):
    st = styles("Carlito", "Carlito-Bold", TRESCO, 10.0)
    rows = [["Plant", "Location", "MWac", "In service", "Original modules", "New modules", "Completed",
             "Change in annual energy (%)"]]
    rows += [list(p) for p in TRESCO_PLANTS]
    s = [Paragraph("Tresco Field Services &middot; Asset Services", st["sub"]),
         Paragraph("Repowering program 2019 to 2026", st["h1"]),
         Paragraph("Program summary for clients, March 2026.", st["sub"])]
    for p in TRESCO_TEXT[:1]:
        s.append(Paragraph(esc(p), st["body"]))
    s.append(grid(rows, [1.0, 1.0, 0.5, 0.62, 1.0, 1.0, 0.78, 0.9], st))
    s.append(Spacer(1, 8))
    for p in TRESCO_TEXT[1:]:
        s.append(Paragraph(esc(p), st["body"]))
    doc = _doc(path, "Tresco repowering program 2019 to 2026", "Tresco Field Services", margins=0.8)
    f = _footer("Tresco Field Services  |  Repowering program summary", font="Carlito")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- README
F_README = "README.md"


def readme_text(W):
    L = []
    L += ["# Hadley Ranch Solar: data pull for the 2027 forward sale", "",
          "Pulled by %s (Solar Asset Manager) on October 6, 2026 for %s (Energy and Commodities Manager). All times "
          "on site are Arizona time, which is Mountain Standard Time all year (UTC-7); files stamped in UTC say so."
          % (K.PEOPLE["asset"], K.PEOPLE["desk"]), "",
          "## The plant", "",
          "- Commercial operation November 20, 2015. Sixteen 2,500 kW central inverters in four blocks of four, each "
          "fed by 8,000 Kellerman KS-315P modules (400 strings of 20, 2,520 kWp per inverter, 40,320 kWp in all) on "
          "fixed tables at 25 degrees facing south.",
          "- The plant exports at 69 kV to the Vado Seco Irrigation and Power District (VSIPD) through the Hadley "
          "Ranch substation. The district's revenue meter there is service point 0417 on account 7731-0459.",
          "- Tresco Field Services has operated and maintained the plant since commercial operation; the current "
          "agreement started January 1, 2021.",
          "- Module replacement works started October 5, 2026 (scope in the July 2026 paper).", "",
          "## SCADA", "",
          "- `%s`: the original SCADA's daily report, one row per local day, energies in kWh, inverters INV01 to "
          "INV16. The server lost August 14 to 16, 2018 in a disk failure; those days are not in the file." % R.F_OLD,
          "- `%s`: the replacement SCADA's daily export from March 3, 2020, one row per device, point and day. "
          "`day_start_utc` is the start of the local day in UTC (07:00Z). Energies in MWh." % R.F_NEW,
          "- `%s`: the original inverter numbers against the replacement SCADA's block tags. Inverter 07 (B2-INV3) "
          "was destroyed by a power stage fire on March 2, 2021; its replacement has run as B2-INV3R since April 15, "
          "2021, on the same array." % R.F_TAGS,
          "- Points in both layouts: DC energy measured at each inverter's DC input (`E_DC`, `_DC_kWh`); AC energy at "
          "the inverter's AC output (`E_AC`, `_AC_kWh`); hours the inverter spent feeding the grid that day (`T_OP`, "
          "`_OpHrs`); plane-of-array irradiation from the met station's pyranometer (`H_POA`, kWh/m2); the "
          "back-of-module temperature at the met station averaged over the day weighted by plane-of-array "
          "irradiance (`T_MOD_IW`, `TMod_IW_C`); the daily mean air temperature; and the revenue meter's export and "
          "import registers as the SCADA reads them (`PLANT-RM` `E_EXP` and `E_IMP`, `Meter_Export_kWh` and "
          "`Meter_Import_kWh`).", "",
          "## 2025 detail", "",
          "- `%s`: each inverter's AC energy in each hour of 2025 and its lifetime AC energy register at the end of "
          "the hour (kWh), as the four block data loggers forward them. `interval_end_utc` is the end of the hour in "
          "UTC." % R.F_HOURLY,
          "- `%s`: the met station's hourly means for 2025; `hour_beginning_mst` is the local hour." % R.F_MET,
          "- `%s`: the inverters' alarm and event log for 2025 (raised and cleared in UTC; `ack_by` is the Tresco "
          "control room user who acknowledged it, blank when the event cleared itself)." % R.F_EVENTS, "",
          "## Work orders", "",
          "- `%s`: Tresco's work orders for the site from handover to the pull. Types: CLN cleaning, CM corrective, "
          "PM preventive, INSP inspection, OWN owner request, VEG vegetation, PROJ project work. Created and "
          "completed times are local." % R.F_WO, "",
          "## District files (account 7731-0459)", "",
          "- `%s`: the district's legacy billing system, daily totals from November 20, 2015 to February 29, 2020. "
          "Fixed width: account (10), service point (6), meter (10), channel (4), interval end date and time "
          "(YYYYMMDD HHMM), kWh, read status (A actual, E estimated). A day's total is stamped with the end of its "
          "interval." % R.F_LEGACY,
          "- `%s`: the district's meter data system from October 1, 2019, when it went live with its history load, to "
          "December 31, 2025; one row per service point, channel, day and version." % R.F_MDM,
          "- `%s`: the service points on the account." % R.F_SP,
          "- Channels are named from the district's side: REC is the energy the district received from the service "
          "point, DEL the energy it delivered to it.",
          "- The district's files are the meter of record (interconnection agreement, Exhibit C). The SCADA's "
          "`PLANT-RM` points are the control room's own read of the same meter and stop when the SCADA does.", "",
          "## Desk", "",
          "- `%s`: the desk's blotter of Hadley Ranch forward trades, quantities as traded." % R.F_BLOTTER,
          "- `%s`: Westmark's confirmations." % F_CONF,
          "- `%s`: the desk's Palo Verde forward marks for 2027 on October 5, 2026." % R.F_CURVE, "",
          "## Resource and documents", "",
          "- `%s`: Clearfield Solar Resource's site-adapted hourly series for the plant, 2001 to 2025 (delivered "
          "January 2026; details in the file header)." % R.F_LT,
          "- `%s`: the treasury's energy risk policy (revision 4)." % F_POLICY,
          "- `%s`: the module replacement scope and schedule (July 2026)." % F_SCOPE,
          "- `%s`: Corvane's report on the side-by-side comparison in block 3." % F_RIG,
          "- `%s`: the datasheets of the original and the new modules." % F_SHEETS,
          "- `%s`: the O&M agreement's cleaning and availability schedules." % F_OM,
          "- `%s`: the interconnection agreement's metering exhibit." % F_EXHIBIT,
          "- `%s`: the district's 2025 interruption report for the plant's 69 kV tap." % F_INTERRUPT,
          "- `%s`: Tresco's summary of the plants it has repowered." % F_TRESCO, ""]
    return "\n".join(L)


OFFICE = []


def write_all(out, W):
    p = lambda f: os.path.join(out, f)
    write_policy(p(F_POLICY))
    PP.normalize_pdf(p(F_POLICY), b"D:20240213101544-07'00'", b"D:20240213101544-07'00'")
    write_scope(p(F_SCOPE))
    PP.normalize_docx(p(F_SCOPE), K.PEOPLE["asset"], K.PEOPLE["asset"], "2026-07-01T16:20:00Z", "2026-07-08T21:47:00Z",
                      7, 186, "task152-scope", title="Hadley Ranch Solar module replacement", company=K.COMPANY)
    write_om(p(F_OM))
    PP.normalize_pdf(p(F_OM), b"D:20201218153012-07'00'", b"D:20210106091145-07'00'")
    write_exhibit(p(F_EXHIBIT))
    PP.normalize_pdf(p(F_EXHIBIT), b"D:20240321140522-07'00'", b"D:20240321140522-07'00'")
    W.report_gain = write_rig(p(F_RIG), W)
    PP.normalize_pdf(p(F_RIG), b"D:20261002083310-07'00'", b"D:20261002083310-07'00'")
    write_sheets(p(F_SHEETS))
    PP.normalize_pdf(p(F_SHEETS), b"D:20260612111907-07'00'", b"D:20260612111907-07'00'")
    write_conf(p(F_CONF), W)
    PP.normalize_pdf(p(F_CONF), b"D:20251030162258-07'00'", b"D:20251030162258-07'00'")
    write_interruptions(p(F_INTERRUPT), W)
    PP.normalize_pdf(p(F_INTERRUPT), b"D:20260114100431-07'00'", b"D:20260114100431-07'00'")
    write_tresco(p(F_TRESCO))
    PP.normalize_pdf(p(F_TRESCO), b"D:20260317134650-07'00'", b"D:20260317134650-07'00'")
    PP.normalize_ooxml(p(R.F_WO), "Tresco CMMS", K.PEOPLE["site"], "2026-10-06T16:02:00Z", "2026-10-06T16:02:00Z",
                       excel=True, company=K.CONTRACTOR)
    PP.normalize_ooxml(p(R.F_BLOTTER), K.PEOPLE["desk"], K.PEOPLE["desk"], "2015-10-20T22:14:00Z",
                       "2025-10-28T23:41:00Z", excel=True, company=K.COMPANY)
    with open(p(F_README), "w", encoding="utf-8", newline="") as fh:
        fh.write(readme_text(W))
