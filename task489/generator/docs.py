"""task489: the pack's documents. Larchmere's reporting standard MRS-03 (rev. 4) and its 2027 methane reduction
plan, Sheldrake's 2026 pneumatic survey report, and the three controller makers' data sheets."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1c1e21")
GREY = colors.HexColor("#5c6166")


def styles(accent):
    acc = colors.HexColor(accent)
    s = {"body": ParagraphStyle("body", fontName="LiberationSans", fontSize=9.6, leading=13.0, textColor=INK, spaceAfter=5),
         "h1": ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14.5, leading=18, textColor=acc, spaceAfter=3),
         "sub": ParagraphStyle("sub", fontName="LiberationSans", fontSize=9.2, leading=12, textColor=GREY, spaceAfter=8),
         "h2": ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.2, leading=13.5, textColor=acc,
                              spaceBefore=7, spaceAfter=3),
         "cell": ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.3, leading=10.4, textColor=INK),
         "cellb": ParagraphStyle("cellb", fontName="LiberationSans-Bold", fontSize=8.3, leading=10.4, textColor=INK),
         "small": ParagraphStyle("small", fontName="LiberationSans", fontSize=7.8, leading=10, textColor=GREY),
         "num": ParagraphStyle("num", fontName="LiberationSans", fontSize=9.6, leading=13.0, textColor=INK, spaceAfter=5,
                               leftIndent=30, firstLineIndent=-30)}
    s["acc"] = acc
    return s


def _doc(path, title, author, header, footer, producer="Microsoft® Word for Microsoft 365"):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(18 * mm, LETTER[1] - 12 * mm, header)
        canvas.drawString(18 * mm, 11 * mm, footer)
        canvas.drawRightString(LETTER[0] - 18 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=19 * mm,
                          bottomMargin=19 * mm, title=title, author=author, subject="", creator=producer, producer=producer)
    return d, frame


def _table(rows, widths, st, head=True):
    data = [[Paragraph(str(c), st["cellb"] if (i == 0 and head) else st["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0, hAlign="LEFT")
    style = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LEFTPADDING", (0, 0), (-1, -1), 3.5), ("RIGHTPADDING", (0, 0), (-1, -1), 3.5)]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf1")))
    t.setStyle(TableStyle(style))
    return t


# ------------------------------------------------------------------------------------------------ MRS-03 rev 4
def write_standard(path):
    st = styles("#24456b")
    d, frame = _doc(path, "MRS-03 Methane Measurement and Reporting Standard", W.PEOPLE["lead"],
                    "Larchmere Resources Ltd.  |  MRS-03 Methane Measurement and Reporting Standard  |  Revision 4",
                    "Controlled copy when viewed in the document system. Printed copies are uncontrolled.")
    b, P = [], Paragraph
    b.append(P("Methane Measurement and Reporting Standard", st["h1"]))
    b.append(P("Document MRS-03, Revision 4. Effective 1 January 2026. Applies to Larchmere-operated well sites in the "
               "Kakwa and Elmworth areas.", st["sub"]))
    b.append(_table([["Owner", "Approved", "Effective", "Supersedes"],
                     ["%s, %s" % (W.PEOPLE["lead"], W.TITLES["lead"]), "%s, %s" % (W.PEOPLE["vp"], W.TITLES["vp"]),
                      "2026-01-01", "MRS-03 Revision 3 (2024-02-15)"]], [55 * mm, 58 * mm, 24 * mm, 43 * mm], st))
    b.append(P("1. Purpose", st["h2"]))
    b.append(P("1.1 This standard sets how Larchmere quantifies and reports the methane vented and leaked at its operated "
               "well sites, so that the company's annual inventory is built the same way each year and can be checked "
               "against the source records.", st["num"]))
    b.append(P("1.2 Revision 4 moves pneumatic controllers from population factors to source-level reporting, starting "
               "with the 2026 reporting year.", st["num"]))
    b.append(P("2. Terms", st["h2"]))
    for t in ("2.1 <b>Source.</b> One piece of equipment that releases methane to the atmosphere, identified by its tag "
              "in the equipment register.",
              "2.2 <b>Intermittent-vent controller.</b> A pneumatic controller that releases supply gas to the atmosphere "
              "only when it actuates. On a wellsite separator this is the liquid level controller and its dump valve.",
              "2.3 <b>Continuous-bleed controller.</b> A pneumatic controller that releases supply gas at a steady rate "
              "while its supply is on, such as a throttling pressure controller or a line heater bath temperature "
              "controller.",
              "2.4 <b>Dump cycle.</b> One opening and closing of a separator's dump valve by its level controller.",
              "2.5 <b>Pad.</b> A well site as named in the equipment register, with its surface location."):
        b.append(P(t, st["num"]))
    b.append(P("3. Reporting year and records", st["h2"]))
    for t in ("3.1 The reporting year for the 2026 inventory is 2026.",
              "3.2 Volumes and events are taken by production day, the 24 hours from 08:00 local time on the stated date, "
              "as production accounting closes them. The reporting year is the production days 1 January to 31 December.",
              "3.3 A source's methane content is the methane mole fraction of its pad's laboratory gas analysis taken in "
              "the reporting year.",
              "3.4 Source records are kept for six years: SCADA and plunger controller histories, daily allocations and "
              "their re-runs, work orders, survey reports and the equipment register."):
        b.append(P(t, st["num"]))
    b.append(P("4. Quantification at source level", st["h2"]))
    for t in ("4.1 The inventory reports the methane each source vented in the reporting year.",
              "4.2 An intermittent-vent controller vents its maker's rated supply gas per dump cycle each time it cycles. "
              "Its methane is its dump cycles in the reporting year times that volume. Where a pad's SCADA counts a "
              "separator's dump cycles, the counted cycles are used.",
              "4.3 A continuous-bleed controller vents its steady bleed for every hour its instrument supply is on. Its "
              "bleed is the rate the reporting year's pneumatic survey measured on that device, and otherwise its maker's "
              "rated bleed.",
              "4.4 Volumes stated in standard cubic feet (60 F, 14.696 psia) are converted at 0.02826 m3 per scf "
              "(15 C, 101.325 kPa). Methane mass is the gas volume times the methane mole fraction times 0.678 kg per m3.",
              "4.5 Leaks found by optical gas imaging and tank vents are reported under MRS-05 and MRS-07 and are not "
              "part of the pneumatic inventory."):
        b.append(P(t, st["num"]))
    b.append(P("5. Reporting form", st["h2"]))
    b.append(P("5.1 Sources are reported in Annex B, one row per source, and each pad's totals in the Annex B pads sheet. "
               "A source in service for part of the year is reported for the part it was in service.", st["num"]))
    b.append(P("5.2 Methane is reported in kilograms per source and in tonnes per pad.", st["num"]))
    b.append(P("6. Revision history", st["h2"]))
    b.append(_table([["Rev.", "Date", "Change", "By"],
                     ["1", "2019-03-01", "First issue", "S. Eaton"],
                     ["2", "2021-01-15", "Tank vents moved to MRS-07", "S. Eaton"],
                     ["3", "2024-02-15", "Optical gas imaging frequency from MRS-05", W.PEOPLE["lead"]],
                     ["4", "2025-11-28", "Pneumatic controllers at source level from the 2026 reporting year (sections "
                                         "2 to 5)", W.PEOPLE["lead"]]],
                    [12 * mm, 22 * mm, 116 * mm, 30 * mm], st))
    b.append(Spacer(1, 10))
    b.append(P("Approved for issue: %s, %s, 2025-12-04" % (W.PEOPLE["vp"], W.TITLES["vp"]), st["small"]))
    d.build(b, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------ survey report
def write_survey(path, wd):
    st = styles("#2f5e3a")
    d, frame = _doc(path, "Pneumatic device emission survey, Larchmere Resources Deep Basin, 2026", W.PEOPLE["contractor"],
                    "Sheldrake Field Measurement Ltd.  |  Report SFM-26-114  |  Larchmere Resources Ltd., Deep Basin",
                    "Sheldrake Field Measurement Ltd., 11 Clearwater Industrial Way, Grande Prairie AB.  Report SFM-26-114.")
    b, P = [], Paragraph
    b.append(P("Pneumatic Device Emission Survey", st["h1"]))
    b.append(P("Larchmere Resources Ltd., Kakwa and Elmworth areas. Field work 25 May to 1 June 2026. Report SFM-26-114, "
               "issued 8 July 2026.", st["sub"]))
    b.append(P("1. Scope", st["h2"]))
    b.append(P("Larchmere asked Sheldrake to measure a sample of the pneumatic devices on its operated pads ahead of its "
               "first source-level inventory. We tested %d separator level controllers and %d continuous-bleed "
               "controllers at %d pads. Level controllers are identified by the well their separator takes, "
               "continuous-bleed controllers by the tag on the device and its model."
               % (len(wd["survey"]["lcs"]), len(wd["survey"]["bleeds"]),
                  len({x["site"] for x in wd["survey"]["lcs"]} | {x["site"] for x in wd["survey"]["bleeds"]})), st["body"]))
    b.append(P("2. Method", st["h2"]))
    b.append(P("Level controllers: the controller and actuator exhaust was enclosed and routed through a calibrated "
               "positive displacement meter for 60 minutes with the separator in normal service; each dump cycle was "
               "counted at the valve. Continuous-bleed controllers: the bleed port was connected to a thermal mass flow "
               "meter and read over 15 minutes once flow was steady. All volumes are corrected to 60 F and 14.696 psia. "
               "Instrument supply was at the pads' regulated 241 kPa (35 psig) throughout.", st["body"]))
    b.append(P("3. Results, level controllers", st["h2"]))
    pad = {s["code"]: s["name"] for s in wd["sites"]}
    well = {sp["lc_tag"]: sp["well"] for sp in wd["seps"]}
    rows = [["Date", "Separator inlet well", "Model", "Minutes", "Dump cycles", "Gas vented (scf)", "Per cycle (scf)"]]
    for x in wd["survey"]["lcs"]:
        per = "%.3f" % (x["scf"] / x["cycles"]) if x["cycles"] else "n/a"
        rows.append([x["date"].isoformat(), well[x["tag"]], x["model"], x["minutes"], x["cycles"], "%.2f" % x["scf"], per])
    b.append(_table(rows, [20 * mm, 45 * mm, 17 * mm, 15 * mm, 18 * mm, 24 * mm, 21 * mm], st))
    b.append(P("4. Results, continuous-bleed controllers", st["h2"]))
    rows = [["Date", "Pad", "Tag", "Model", "Measured bleed (scf/h)", "Maker's rating (scf/h)"]]
    for x in wd["survey"]["bleeds"]:
        rows.append([x["date"].isoformat(), pad[x["site"]], x["tag"], x["model"], "%.2f" % x["scf_h"],
                     "%.2f" % W.BLEED_MODELS[x["model"]]["scf_per_h"]])
    b.append(_table(rows, [21 * mm, 27 * mm, 16 * mm, 18 * mm, 40 * mm, 40 * mm], st))
    lc = wd["survey"]["lcs"]
    rate = sum(x["scf"] for x in lc) / sum(x["minutes"] for x in lc) * 60.0
    bl = wd["survey"]["bleeds"]
    hi = sum(1 for x in bl if x["scf_h"] > 1.5 * W.BLEED_MODELS[x["model"]]["scf_per_h"])
    words = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
             "thirteen", "fourteen", "fifteen", "sixteen"]
    b.append(P("5. Summary", st["h2"]))
    b.append(P("The level controllers tested vented %.2f scf per hour on average over their test hours. Gas per dump "
               "cycle was within 4 per cent of each maker's published figure on every controller that cycled during its "
               "test. %s of the %s continuous-bleed controllers bled at more than one and a half times their "
               "rating; worn relay seats are the usual cause and were reported to the pad operators on the day."
               % (rate, words[hi].capitalize(), words[len(bl)]), st["body"]))
    b.append(Spacer(1, 12))
    b.append(KeepTogether([_table([["Prepared", "Reviewed"],
                                   ["%s, %s" % (W.PEOPLE["contractor"], W.TITLES["contractor"]),
                                    "Michael Espinoza, P.Eng., Technical Director"]],
                                  [86 * mm, 86 * mm], st)]))
    d.build(b, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------ data sheets
SHEETS = {
    "Corrigan": {"addr": "Corrigan Controls, 4410 72 Avenue SE, Calgary AB T2C 2G9", "doc": "DS-CL200-CP10 Rev. F",
                 "date": "2023-03-14", "lc": "CL-200", "bl": "CP-10", "accent": "#7a2f1c", "author": "Stephanie Clements",
                 "producer": "Adobe PDF Library 17.0",
                 "lc_text": "The CL-200 is a float-operated snap controller for vertical separators. Rising liquid lifts the float "
                            "until the pilot snaps the dump valve fully open at the upper setting; the valve stays open "
                            "while the level falls and snaps shut at the lower setting. Each opening is one dump cycle. "
                            "The span is set by moving the float rod clamp, 2 to 16 inches.",
                 "bl_text": "The CP-10 holds separator or sales back pressure with a throttling relay that bleeds to atmosphere "
                            "all the time it is supplied, at a rate fixed by supply pressure.",
                 "valve": [["1 in, 1/4 in trim", "2.1 m3/h water at 700 kPa differential"],
                           ["2 in, 1/2 in trim", "6.4 m3/h water at 700 kPa differential"]]},
    "Aldous": {"addr": "Aldous Valve and Instrument Inc., 2209 Kingsway Industrial Park, Nisku AB T9E 8P3",
               "doc": "AVI-PDS-114 Issue 7", "date": "2022-09-30", "lc": "SV-40", "bl": "PC-60", "accent": "#1f4f63",
               "author": "Todd Harrison", "producer": "Microsoft® Word for Microsoft 365",
               "lc_text": "SV-40 packages combine a displacer level pilot with a 1 or 2 inch snap-action dump valve. The pilot "
                          "trips the valve open when liquid reaches the high set point and closes it when the liquid has "
                          "drained to the low set point. Pilot and actuator exhaust at every trip; nothing bleeds "
                          "while the valve is at rest.",
               "bl_text": "The PC-60 low-bleed pressure controller throttles a control valve against a set point. Its relay "
                          "bleed is continuous and depends only on supply pressure.",
               "valve": [["1 in body", "2.6 m3/h water at 700 kPa differential"],
                         ["2 in body", "7.9 m3/h water at 700 kPa differential"]]},
    "Brannick": {"addr": "Brannick Instrument Company, 81 Tower Road, Red Deer AB T4P 3K2", "doc": "BI-DS-0310 Rev. 4",
                 "date": "2021-06-02", "lc": "DLC-3", "bl": "TC-5", "accent": "#4d3a6b", "author": "Donna Simpson",
                 "producer": "Microsoft® Word 2016",
                 "lc_text": "DLC-3 displacer controllers mount on the vessel's side connections. Operation is on and off: at "
                            "the high level setting the output goes to full supply and opens the dump valve, and it vents to "
                            "zero at the low level setting, closing the valve. Supply gas is consumed only on these changes "
                            "of state. Level span is adjustable from 2 to 16 inches on the linkage.",
                 "bl_text": "TC-5 bath temperature controllers for line heaters use a capillary bulb in the bath and a "
                            "throttling relay with a constant bleed while supply is on.",
                 "valve": [["1 in angle valve", "1.8 m3/h water at 700 kPa differential"],
                           ["2 in angle valve", "5.7 m3/h water at 700 kPa differential"]]},
}


def write_sheet(path, maker):
    m = SHEETS[maker]
    st = styles(m["accent"])
    lc, bl = W.LC_MODELS[m["lc"]], W.BLEED_MODELS[m["bl"]]
    d, frame = _doc(path, "%s %s and %s product data" % (W.MAKERS[maker], m["lc"], m["bl"]), m["author"],
                    "%s  |  %s" % (W.MAKERS[maker], m["doc"]),
                    "%s.  Specifications subject to change without notice." % m["addr"], producer=m["producer"])
    b, P = [], Paragraph
    b.append(P(W.MAKERS[maker], st["h1"]))
    b.append(P("%s and %s. %s, %s." % (lc["name"], bl["name"], m["doc"], m["date"]), st["sub"]))
    b.append(P(lc["name"], st["h2"]))
    b.append(P(m["lc_text"], st["body"]))
    rows = [["Specification", "Value"],
            ["Supply pressure", "140 to 350 kPa (20 to 50 psig); rated at 241 kPa (35 psig)"],
            ["Supply gas per dump cycle", "%.2f scf (60 F, 14.696 psia) at 35 psig supply" % lc["scf_per_cycle"]],
            ["Steady-state bleed", "None"],
            ["Ambient temperature", "-40 C to 70 C"]]
    for v in m["valve"]:
        rows.append(["Dump valve capacity, " + v[0], v[1]])
    b.append(_table(rows, [62 * mm, 112 * mm], st))
    b.append(P(bl["name"], st["h2"]))
    b.append(P(m["bl_text"], st["body"]))
    b.append(_table([["Specification", "Value"],
                     ["Supply pressure", "140 to 350 kPa (20 to 50 psig); rated at 241 kPa (35 psig)"],
                     ["Steady-state bleed", "%.2f scf/h (60 F, 14.696 psia) at 35 psig supply" % bl["scf_per_h"]],
                     ["Ambient temperature", "-40 C to 70 C"]], [62 * mm, 112 * mm], st))
    b.append(Spacer(1, 8))
    notes = {"Corrigan": "Consumption figures are bench values with a new pilot at rated supply.",
             "Aldous": "Published gas use is measured at the factory on new pilots and relays at 35 psig.",
             "Brannick": "Figures apply to new relays at rated supply; worn seats raise consumption."}
    b.append(P(notes[maker], st["small"]))
    d.build(b, onFirstPage=frame, onLaterPages=frame)


def write_controller_sheet(path):
    st = styles("#3b5d2a")
    d, frame = _doc(path, "Trellick PCX-300 plunger lift controller", "Laura Mendoza",
                    "Trellick Automation  |  PCX-300 Plunger Lift Controller  |  TA-PCX300-SPEC-02",
                    "Trellick Automation Ltd., 5120 Gateway Boulevard NW, Edmonton AB T6H 5K3.",
                    producer="Microsoft® Word 2019")
    b, P = [], Paragraph
    b.append(P("PCX-300 Plunger Lift Controller", st["h1"]))
    b.append(P("Specification sheet TA-PCX300-SPEC-02, 2024-02-19. Firmware 4.2 and later.", st["sub"]))
    b.append(P("The PCX-300 runs a plunger lift well on timers, pressures or plunger travel time. It opens and closes the "
               "well's motor valve, detects the plunger at the lubricator with a magnetic arrival sensor and reports each "
               "cycle to a SCADA host over Modbus.", st["body"]))
    b.append(P("Counters", st["h2"]))
    b.append(_table([["Register", "Meaning"],
                     ["Cycle count (40011)", "Number of times the controller has opened the motor valve. Not reset by power loss."],
                     ["Arrival count (40013)", "Number of plunger arrivals registered by the arrival sensor. Not reset by power loss."],
                     ["Travel time (40021)", "Seconds from motor valve open to arrival on the last cycle; 0 when the plunger "
                                             "did not arrive within the travel timer."]], [52 * mm, 122 * mm], st))
    b.append(P("Specifications", st["h2"]))
    b.append(_table([["Item", "Value"],
                     ["Power", "12 V DC, solar charged, 0.3 W average"],
                     ["Valve output", "Latching solenoid, 3-way, 140 to 700 kPa supply"],
                     ["Event buffer", "2,000 cycles"],
                     ["Communications", "Modbus RTU and TCP, RS-485 and radio"],
                     ["Operating temperature", "-40 C to 70 C"]], [52 * mm, 122 * mm], st))
    b.append(Spacer(1, 8))
    b.append(P("Counters are 32-bit and roll over at 4,294,967,295.", st["small"]))
    d.build(b, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------ the 2027 plan
def write_plan(path):
    import docx
    from docx.shared import Pt
    doc = docx.Document()
    s = doc.styles["Normal"]
    s.font.name = "Calibri"
    s.font.size = Pt(10.5)
    doc.add_heading("Larchmere Resources Ltd. 2027 Methane Reduction Plan", level=1)
    doc.add_paragraph("Issued 12 January 2027. Owner: %s, %s. Endorsed by the executive team, 8 January 2027."
                      % (W.PEOPLE["lead"], W.TITLES["lead"]))
    doc.add_heading("1. Where we start", level=2)
    doc.add_paragraph("The 2026 inventory is the first one built at source level for pneumatic controllers under MRS-03 "
                      "Revision 4. It sets the baseline for this plan and for the instrument air programme that follows "
                      "in 2028.")
    doc.add_heading("2. 2027 programme", level=2)
    t = doc.add_table(rows=1, cols=3)
    t.style = "Table Grid"
    for c, h in zip(t.rows[0].cells, ("Work", "Scope", "Timing")):
        c.text = h
    for row in (("Zero-emission controller conversion", "Section 3", "Kits ordered by 15 February; installs May to September"),
                ("Optical gas imaging", "Every pad twice a year (MRS-05)", "Spring and autumn rounds"),
                ("Tank vapour control", "Thief hatch replacements at the pads the 2026 tests flagged (MRS-07)",
                 "Second quarter"),
                ("Instrument air study", "Continuous-bleed controllers, all pads", "Report by November for 2028")):
        cells = t.add_row().cells
        for c, v in zip(cells, row):
            c.text = v
    doc.add_heading("3. Zero-emission controller conversion", level=2)
    doc.add_paragraph("In 2027 we convert the separator level controllers to electric actuation, with a solar and battery "
                      "package, at every pad whose intermittent-vent controllers vented more than 0.5 tonnes of methane "
                      "in 2026 as reported under MRS-03. Pads at or under that line keep their controllers until the 2028 "
                      "programme.")
    doc.add_paragraph("The conversion kits are bought on one order placed with the supplier by 15 February 2027, so the list "
                      "of pads is fixed when the order is placed. Installs run from May, after spring break-up, to the end "
                      "of September.")
    doc.add_heading("4. Continuous-bleed controllers", level=2)
    doc.add_paragraph("Pressure and temperature controllers that bleed continuously are not part of the 2027 conversion. "
                      "Their 2026 methane is reported at source level so that the 2028 instrument air programme starts from "
                      "a measured baseline.")
    doc.add_heading("5. Reporting", level=2)
    doc.add_paragraph("Progress is reported to the executive team each quarter. The 2027 inventory will be built under the same "
                      "revision of MRS-03.")
    doc.save(path)
