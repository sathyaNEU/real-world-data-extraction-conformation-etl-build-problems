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
                 "producer": "Adobe PDF Library 17.0"},
    "Aldous": {"addr": "Aldous Valve and Instrument Inc., 2209 Kingsway Industrial Park, Nisku AB T9E 8P3",
               "doc": "AVI-PDS-114 Issue 7", "date": "2022-09-30", "lc": "SV-40", "bl": "PC-60", "accent": "#1f4f63",
               "author": "Todd Harrison", "producer": "Microsoft® Word for Microsoft 365"},
    "Brannick": {"addr": "Brannick Instrument Company, 81 Tower Road, Red Deer AB T4P 3K2", "doc": "BI-DS-0310 Rev. 4",
                 "date": "2021-06-02", "lc": "DLC-3", "bl": "TC-5", "accent": "#4d3a6b", "author": "Donna Simpson",
                 "producer": "Microsoft® Word 2016"},
}


def write_sheet(path, maker):
    {"Corrigan": _sheet_corrigan, "Aldous": _sheet_aldous, "Brannick": _sheet_brannick}[maker](path)


def _sheet_corrigan(path):
    m = SHEETS["Corrigan"]
    st = styles(m["accent"])
    lc, bl = W.LC_MODELS["CL-200"], W.BLEED_MODELS["CP-10"]
    d, frame = _doc(path, "Corrigan Controls CL-200 and CP-10 product data", m["author"],
                    "CORRIGAN CONTROLS  |  PRODUCT DATA  |  %s" % m["doc"],
                    "%s.  Specifications subject to change without notice." % m["addr"], producer=m["producer"])
    b, P = [], Paragraph
    b.append(P("CL-200 Snap Level Controller and CP-10 Pressure Controller", st["h1"]))
    b.append(P("Product data %s, issued %s. Supersedes Rev. E." % (m["doc"], m["date"]), st["sub"]))
    b.append(P("CL-200", st["h2"]))
    b.append(P("The CL-200 is a float-operated snap controller for vertical separators and scrubbers. Rising liquid lifts "
               "the float until the pilot snaps the dump valve fully open at the upper setting; the valve stays open "
               "while the level falls and snaps shut at the lower setting. Each opening is one dump cycle. Span is set "
               "by moving the float rod clamp.", st["body"]))
    b.append(_table([["CL-200", ""],
                     ["Mounting", "2 in NPT side connection, external cage optional"],
                     ["Float", "4 x 9 in, 316 stainless steel, 1,000 psig"],
                     ["Span", "2 to 16 in, field adjustable"],
                     ["Supply", "20 to 50 psig (140 to 350 kPa) natural gas or air; rated at 35 psig"],
                     ["Gas used per dump cycle", "%.2f scf (60 F, 14.696 psia) at 35 psig supply" % lc["scf_per_cycle"]],
                     ["Output", "Snap, full supply or zero"],
                     ["Ambient", "-40 to 160 F (-40 to 70 C)"]], [52 * mm, 122 * mm], st))
    b.append(P("CP-10", st["h2"]))
    b.append(P("The CP-10 holds separator or sales back pressure with a throttling relay that bleeds to atmosphere all the "
               "time it is supplied, at a rate fixed by supply pressure.", st["body"]))
    b.append(_table([["CP-10", ""],
                     ["Set point range", "50 to 1,500 psig with range spring"],
                     ["Supply", "20 to 50 psig (140 to 350 kPa); rated at 35 psig"],
                     ["Bleed to atmosphere, steady state", "%.2f scf/h (60 F, 14.696 psia) at 35 psig supply" % bl["scf_per_h"]],
                     ["Proportional band", "2 to 100 per cent, adjustable"]], [52 * mm, 122 * mm], st))
    b.append(P("Ordering", st["h2"]))
    b.append(_table([["Code", "Description"],
                     ["CL-200-S2", "CL-200, 2 in side mount, standard float"],
                     ["CL-200-C2", "CL-200 in external cage, 2 in connections"],
                     ["CP-10-15", "CP-10 with 50 to 1,500 psig spring"]], [40 * mm, 134 * mm], st))
    b.append(Spacer(1, 6))
    b.append(P("Consumption figures are bench values with a new pilot at rated supply.", st["small"]))
    d.build(b, onFirstPage=frame, onLaterPages=frame)


def _sheet_aldous(path):
    m = SHEETS["Aldous"]
    st = styles(m["accent"])
    lc, bl = W.LC_MODELS["SV-40"], W.BLEED_MODELS["PC-60"]
    d, frame = _doc(path, "Aldous Valve and Instrument SV-40 and PC-60 product data", m["author"],
                    "Aldous Valve and Instrument  -  Product Information Sheet %s" % m["doc"],
                    m["addr"] + ".  This sheet is uncontrolled when printed.", producer=m["producer"])
    b, P = [], Paragraph
    b.append(P("Aldous Valve and Instrument", st["h1"]))
    b.append(P("Product Information Sheet %s, %s: SV-40 level package and PC-60 low-bleed pressure controller"
               % (m["doc"], m["date"]), st["sub"]))
    b.append(P("1. Application", st["h2"]))
    b.append(P("The SV-40 package is built for two-phase and three-phase wellsite vessels in sour and sweet service. The "
               "PC-60 is a low-bleed controller for back pressure and sales gas control.", st["body"]))
    b.append(P("2. Operation", st["h2"]))
    b.append(P("SV-40 packages combine a displacer level pilot with a 1 or 2 inch snap-action dump valve. The pilot trips "
               "the valve open when liquid reaches the high set point and closes it when the liquid has drained to the "
               "low set point. Pilot and actuator exhaust at every trip; nothing bleeds while the valve is at rest. The "
               "PC-60 throttles a control valve against its set point; its relay bleed is continuous and depends only on "
               "supply pressure.", st["body"]))
    b.append(P("3. Performance", st["h2"]))
    b.append(_table([["Item", "Value", "Unit", "Condition"],
                     ["SV-40 supply gas per valve trip", "%.2f" % lc["scf_per_cycle"], "scf",
                      "60 F, 14.696 psia; 35 psig supply"],
                     ["SV-40 displacer length", "14 or 32", "in", "level span up to the displacer length"],
                     ["PC-60 relay bleed", "%.2f" % bl["scf_per_h"], "scf/h", "steady state; 35 psig supply"],
                     ["Supply pressure", "140 to 350", "kPa", "rated 241 kPa (35 psig)"],
                     ["Operating temperature", "-40 to 70", "C", ""]], [66 * mm, 24 * mm, 16 * mm, 68 * mm], st))
    b.append(P("4. Notes", st["h2"]))
    b.append(P("Published gas use is measured at the factory on new pilots and relays at 35 psig.", st["body"]))
    d.build(b, onFirstPage=frame, onLaterPages=frame)


def _sheet_brannick(path):
    m = SHEETS["Brannick"]
    st = styles(m["accent"])
    lc, bl = W.LC_MODELS["DLC-3"], W.BLEED_MODELS["TC-5"]
    d, frame = _doc(path, "Brannick Instrument DLC-3 and TC-5 product data", m["author"],
                    "Brannick Instrument Company      %s" % m["doc"],
                    "Brannick Instrument Company, Red Deer, Alberta.  Tel 403 555 0164.", producer=m["producer"])
    b, P = [], Paragraph
    b.append(P("DLC-3 Displacer Level Controller", st["h1"]))
    b.append(P("with TC-5 Bath Temperature Controller.  Data sheet %s, %s." % (m["doc"], m["date"]), st["sub"]))
    b.append(P("DLC-3 displacer controllers mount on the vessel's side connections. Operation is on and off: at the high "
               "level setting the output goes to full supply and opens the dump valve, and it vents to zero at the low "
               "level setting, closing the valve. Supply gas is consumed only on these changes of state. Level span is "
               "adjustable from 2 to 16 inches on the linkage.", st["body"]))
    b.append(P("TC-5 bath temperature controllers for line heaters use a capillary bulb in the bath and a throttling relay "
               "with a constant bleed while supply is on.", st["body"]))
    b.append(P("Performance data", st["h2"]))
    b.append(_table([["", "DLC-3", "TC-5"],
                     ["Consumption per dump cycle", "%.2f scf" % lc["scf_per_cycle"], "n/a"],
                     ["Steady bleed", "nil at rest", "%.2f scf/h" % bl["scf_per_h"]],
                     ["Supply", "20 to 50 psig", "20 to 50 psig"],
                     ["Sensing element", "14 in displacer, 316 SS", "capillary bulb, 6 ft"]], [70 * mm, 52 * mm, 52 * mm], st))
    b.append(Spacer(1, 6))
    b.append(P("Figures apply to new relays at 35 psig supply, base conditions 60 F and 14.696 psia; worn seats raise "
               "consumption.", st["small"]))
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
    b.append(P("Operation", st["h2"]))
    b.append(P("The controller runs the well in cycles. With the motor valve closed, casing pressure builds while the plunger "
               "rests on the bumper spring. The controller opens the motor valve when the off timer has run or, in casing "
               "pressure mode, when the casing reaches its open set point. The plunger rises with the liquid that has "
               "gathered above it and brings that liquid to surface ahead of it as it arrives at the lubricator. The well "
               "then flows gas for the afterflow time, set on a timer or, in casing pressure mode, ended when the casing "
               "falls to its close set point, and the controller closes the motor valve and lets the plunger fall. A "
               "plunger that has not arrived when the travel timer runs out is logged as a non-arrival and the motor valve "
               "is closed.", st["body"]))
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
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    def field(par, instr, shown):
        fld = OxmlElement("w:fldSimple")
        fld.set(qn("w:instr"), instr)
        run = OxmlElement("w:r")
        txt = OxmlElement("w:t")
        txt.text = shown
        run.append(txt)
        fld.append(run)
        par._p.append(fld)
    sec = doc.sections[0]
    hp = sec.header.paragraphs[0]
    hp.text = "Larchmere Resources Ltd.\t2027 Methane Reduction Plan\tDocument EHS-PLN-027, Rev. 0"
    for run in hp.runs:
        run.font.size = Pt(8.5)
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.add_run("Uncontrolled when printed.  Page ").font.size = Pt(8.5)
    field(fp, "PAGE", "1")
    fp.add_run(" of ").font.size = Pt(8.5)
    field(fp, "NUMPAGES", "2")
    doc.add_heading("Larchmere Resources Ltd. 2027 Methane Reduction Plan", level=1)
    doc.add_paragraph("Issued 12 January 2027. Owner: %s, %s. Endorsed by the executive team, 8 January 2027."
                      % (W.PEOPLE["lead"], W.TITLES["lead"]))
    t = doc.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    for c, h in zip(t.rows[0].cells, ("", "Name", "Title", "Date")):
        c.text = h
    for row in (("Prepared", W.PEOPLE["lead"], W.TITLES["lead"], "2027-01-11"),
                ("Reviewed", "Jennifer Castro", "Manager, Regulatory and Environment", "2027-01-11"),
                ("Approved", W.PEOPLE["vp"], W.TITLES["vp"], "2027-01-12")):
        cells = t.add_row().cells
        for c, v in zip(cells, row):
            c.text = v
    doc.add_paragraph("Revision 0, issued for use 12 January 2027.")
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
