"""The pack's documents: Product Finance's reserve policy FIN-RS-04, the reliability lab's qualification memo QM-07
(the release model of record RL-3), the Model K pack specification, Zelvora's certificate of analysis for ZC2638
(a distractor), and the extracts note."""
from __future__ import annotations

import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import cm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("Carlito-Italic", "crosextra/Carlito-Italic.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
SANS, SANS_B, SANS_I = "Carlito", "Carlito-Bold", "Carlito-Italic"
INK = colors.HexColor("#1d2229")
GREY = colors.HexColor("#5a6270")
RULE = colors.HexColor("#a3aab3")
PALE = colors.HexColor("#e9edf2")
BRAND = colors.HexColor("#0f4c5c")

BODY = ParagraphStyle("body", fontName=SANS, fontSize=10.2, leading=13.6, textColor=INK, spaceAfter=5)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=26, firstLineIndent=-26)
H1 = ParagraphStyle("h1", fontName=SANS_B, fontSize=15.5, leading=19, textColor=BRAND, spaceAfter=3)
H1S = ParagraphStyle("h1s", fontName=SANS, fontSize=9.4, leading=12.2, textColor=GREY, spaceAfter=10)
H2 = ParagraphStyle("h2", fontName=SANS_B, fontSize=11.2, leading=14, textColor=INK, spaceBefore=7, spaceAfter=3)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=8.8, leading=10.6, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName=SANS_B, fontSize=8.8, leading=10.6, textColor=INK)
SMALL = ParagraphStyle("small", fontName=SANS_I, fontSize=8.6, leading=11, textColor=GREY, spaceBefore=4)


def _footer(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(SANS, 7.8)
        canvas.setFillColor(GREY)
        canvas.drawString(2.0 * cm, 1.2 * cm, left)
        canvas.drawRightString(A4[0] - 2.0 * cm, 1.2 * cm, "%s  |  page %d" % (right, doc.page))
        canvas.restoreState()
    return draw


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=2.1 * cm, rightMargin=2.1 * cm, topMargin=1.9 * cm,
                             bottomMargin=2.0 * cm, title=title, author=author, subject="", creator="", producer="")


def _table(rows, widths, head=True, align_right=()):
    data = [[Paragraph(str(c), CELLB if (head and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    st = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 2.0), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.0)]
    if head:
        st.append(("BACKGROUND", (0, 0), (-1, 0), PALE))
    t.setStyle(TableStyle(st))
    return t


def _c(n, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, text), CLAUSE)


# ---------------------------------------------------------------------------------------------------- FIN-RS-04
def write_policy(path):
    s = [Paragraph("Kalvenhorst Systeme GmbH &middot; Notebook Division &middot; Product Finance", H1S),
         Paragraph("FIN-RS-04 Battery warranty reserve at lot release", H1),
         Paragraph("Revision 3, effective 1 April 2025. Owner: %s, Product Finance Controller, Notebook Division. "
                   "Replaces revision 2 of 12 September 2023." % K.PEOPLE["controller"], H1S),
         Paragraph("1. Purpose and scope", H2),
         _c("1.1", "This policy sets how Product Finance books the warranty reserve for the battery packs built from a "
                   "supplier cell lot, on the day the battery reliability lab releases the lot for shipment."),
         _c("1.2", "It applies to the Model K pack (part 4100-2210, the battery of the K14 and K15 notebooks). The "
                   "Model J pack follows FIN-RS-05."),
         Paragraph("2. Terms", H2),
         _c("2.1", "Lot: a supplier cell lot, as the supplier's lot code names it."),
         _c("2.2", "The lot's Model K packs: every Model K pack the battery plant has built from the lot's cells by "
                   "the release day, whether it is in the bonded store, in a notebook or shipped."),
         _c("2.3", "Warranty replacement: a pack replaced under the battery warranty of the Model K pack "
                   "specification (rev. D, section 7): its full charge capacity, as its gauge reports it, is below 80 "
                   "per cent of rated capacity within its first 600 cycles."),
         _c("2.4", "Release: the reliability lab's release of the lot on its release test (QM-07)."),
         Paragraph("3. The reserve", H2),
         _c("3.1", "On a lot's release day Product Finance books a warranty reserve for the lot's Model K packs."),
         _c("3.2", "The reserve is the expected number of the lot's Model K packs that will need a warranty "
                   "replacement: the sum, over the lot's Model K packs, of each pack's probability that its full "
                   "charge capacity falls below 80 per cent of rated capacity within its first 600 cycles."),
         _c("3.3", "Cycles are full cycles as the pack's gauge counts them, which are the cycles of the reliability "
                   "lab's qualification protocol QP-3. A cell's cycle life to 80 per cent of rated capacity is "
                   "predicted from the lot's release test with the release model of record, RL-3 (QM-07), and the "
                   "model's error on the life tests of every earlier lot whose life tests have finished."),
         _c("3.4", "The reserve is stated in packs, rounded to the nearest 50. Service Operations controlling values it "
                   "for the lot's release record."),
         _c("3.5", "Warranty replacements of the lot's packs are charged against its reserve, and the reserve is "
                   "trued up each quarter against the lot's replacements to date."),
         Paragraph("4. Responsibilities", H2),
         _c("4.1", "The battery reliability lab supplies the release test, the release model and the lab's records "
                   "(QM-07)."),
         _c("4.2", "Manufacturing engineering supplies the genealogy of the lot's Model K packs."),
         _c("4.3", "Service Operations controlling supplies the cost of a replacement."),
         _c("4.4", "Product Finance books the reserve on the release day and files the reserve note with the lot's "
                   "release record."),
         ]
    d = _doc(path, "FIN-RS-04 Battery warranty reserve at lot release", K.PEOPLE["controller"])
    f = _footer("Kalvenhorst Systeme GmbH, Product Finance", "FIN-RS-04 rev. 3")
    d.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- QM-07
def write_memo(path, model, table, n_cells, n_stopped, rng_err):
    b0, b1, b2, rmse = model["b0"], model["b1"], model["b2"], model["rmse"]
    s = [Paragraph("Kalvenhorst Systeme GmbH &middot; Battery Reliability Lab, Bielefeld", H1S),
         Paragraph("QM-07 Release model RL-3 for Zelvora ZP-4820 cells", H1),
         Paragraph("Revision 4, 30 September 2026: refit on the twenty lots whose life tests have finished. Author: "
                   "%s, Head of Battery Reliability. Replaces revision 3 of 6 March 2026." % K.PEOPLE["lab"], H1S),
         Paragraph("1. Purpose", H2),
         Paragraph("RL-3 predicts a ZP-4820 cell's cycle life on QP-3 to 80 per cent of rated capacity (3,856 mAh) "
                   "from its first 100 cycles. It is the release model of record for Zelvora lots: the lab releases a "
                   "lot on its release test, and Product Finance books the lot's warranty reserve from the release "
                   "test (FIN-RS-04).", BODY),
         Paragraph("2. The release test", H2),
         Paragraph("At incoming inspection the lab draws 20 formation trays at random from the lot's A trays and puts "
                   "their 120 cells on QP-3 for 100 cycles. QP-3: 25 &deg;C chamber; charge at 1C (4.82 A), constant "
                   "current then constant voltage at 4.40 V to a 0.05C cut-off; rest 10 minutes; discharge at 1C to "
                   "3.00 V; rest 10 minutes. A 10-second 1C discharge pulse at half charge on every cycle gives the "
                   "cell's DC resistance. Cycle 1 is the protocol's first full cycle. After the release test the cells "
                   "stay on QP-3 until their discharge capacity falls below 3,856 mAh (life monitoring).", BODY),
         Paragraph("3. Features", H2),
         Paragraph("F1, the natural logarithm of the discharge capacity lost from the 10th to the 100th cycle, in mAh: "
                   "F1 = ln(Q10 &minus; Q100). F2, the rise in the 10-second DC resistance from the 10th to the 100th "
                   "cycle, in milliohm: F2 = R100 &minus; R10.", BODY),
         Paragraph("4. The model", H2),
         Paragraph("ln N80 = b0 + b1 F1 + b2 F2, N80 the cycles to 80 per cent of rated capacity. Fitted by ordinary "
                   "least squares on the %s qualification cells of the lots ZC2437 to ZC2614 that reached 80 per cent; "
                   "the %d cells whose tests stopped first are left out." % ("{:,}".format(n_cells), n_stopped), BODY),
         Paragraph("b0 = %.4f &nbsp;&nbsp; b1 = &minus;%.4f &nbsp;&nbsp; b2 = &minus;%.4f" % (b0, -b1, -b2), BODY),
         Paragraph("5. Validation", H2),
         Paragraph("Each of the twenty lots was predicted by the model fitted to the other nineteen. Over the %s cells "
                   "the prediction error of the log life has a root-mean-square error of %.3f. The errors are "
                   "normally distributed on the log scale (their normal probability plot is straight between the 0.5th "
                   "and the 99.5th percentiles), and each lot's mean error lies between %s and %s. Table 1 gives each "
                   "lot." % ("{:,}".format(n_cells), rmse, rng_err[0], rng_err[1]), BODY),
         _table([["Cell lot", "Released", "Cells", "Mean error", "RMSE"]] + table,
                [2.6 * cm, 2.8 * cm, 1.8 * cm, 2.4 * cm, 2.0 * cm]),
         Paragraph("Table 1. Leave-one-lot-out errors of the predicted log life, by lot.", SMALL),
         Paragraph("6. Release criterion", H2),
         Paragraph("A lot is released when the median predicted life of its 120 release-test cells is at least 750 "
                   "cycles and no more than six of them are predicted under 700 cycles.", BODY),
         Paragraph("7. Records", H2),
         Paragraph("The cyclers' exports of the first 100 cycles, the release test register and the life test results "
                   "are kept by the lab and pulled for Product Finance at each release.", BODY),
         ]
    d = _doc(path, "QM-07 Release model RL-3 for Zelvora ZP-4820 cells", K.PEOPLE["lab"])
    f = _footer("Kalvenhorst Systeme GmbH, Battery Reliability Lab", "QM-07 rev. 4")
    d.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- pack specification
def write_spec(path):
    s = [Paragraph("Kalvenhorst Systeme GmbH &middot; Battery Plant Bielefeld &middot; Product Engineering", H1S),
         Paragraph("Model K battery pack: specification, revision D", H1),
         Paragraph("Part 4100-2210. Released 14 March 2025; revision D adds the gauge firmware 4.2 cycle count and the "
                   "battery warranty wording of the K-series warranty terms.", H1S),
         Paragraph("1. Application", H2),
         Paragraph("The internal battery of the K14 and K15 notebooks.", BODY),
         Paragraph("2. Configuration", H2),
         _table([["Item", "Value"],
                 ["Cells", "3 x Zelvora ZP-4820 pouch cells in series (3S1P)"],
                 ["Rated capacity", "4,820 mAh (cell and pack)"],
                 ["Nominal voltage", "11.61 V"],
                 ["Energy", "56.0 Wh"],
                 ["Charge voltage", "13.20 V (4.40 V per cell)"],
                 ["Discharge cut-off", "9.00 V (3.00 V per cell)"],
                 ["Electronics", "Battery management with cell-level voltage monitoring, passive balancing, fuel gauge"]],
                [4.0 * cm, 11.5 * cm]),
         Paragraph("3. Cells", H2),
         Paragraph("ZP-4820 cells from formation trays graded A at incoming inspection (formation capacity and the "
                   "incoming limits on open-circuit voltage, AC impedance and self-discharge).", BODY),
         Paragraph("4. Capacity", H2),
         Paragraph("In the series string the pack's full charge capacity is that of its weakest cell: the battery "
                   "management stops the discharge when the first cell reaches 3.00 V and the charge when the first "
                   "reaches 4.40 V, and balancing does not move charge between cells.", BODY),
         Paragraph("5. Gauge", H2),
         Paragraph("The fuel gauge reports the full charge capacity it has learned and a cycle count; it adds one "
                   "cycle for each 4,820 mAh discharged.", BODY),
         Paragraph("6. End-of-line test", H2),
         Paragraph("Every pack is charged, discharged at 1C and recharged to 40 per cent before it leaves the line; a "
                   "pack outside the end-of-line limits is scrapped.", BODY),
         Paragraph("7. Battery warranty", H2),
         Paragraph("A Model K pack is replaced under the battery warranty when its full charge capacity, as its gauge "
                   "reports it, is below 80 per cent of rated capacity (3,856 mAh) within its first 600 cycles. A pack "
                   "below 80 per cent after 600 cycles may be replaced as goodwill at Service Operations' discretion, "
                   "or at the customer's cost.", BODY),
         ]
    d = _doc(path, "Model K battery pack specification rev. D", "Product Engineering")
    f = _footer("Kalvenhorst Systeme GmbH, Battery Plant", "4100-2210 rev. D")
    d.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- the distractor
def write_coa(path, W):
    import numpy as np
    cells = list(W.new.cells.values())
    cap = np.array([c.cap for c in cells])
    ocv = np.array([c.ocv for c in cells])
    acir = np.array([c.acir for c in cells])
    kv = np.array([c.kval for c in cells])
    rows = [["Characteristic", "Specification", "Mean", "Minimum", "Maximum", "Result"],
            ["Formation capacity, 0.2C (mAh)", "4,820 min.", "%.1f" % cap.mean(), "%.1f" % cap.min(),
             "%.1f" % cap.max(), "conforms"],
            ["Open-circuit voltage after aging (V)", "3.880 to 3.905", "%.4f" % ocv.mean(), "%.4f" % ocv.min(),
             "%.4f" % ocv.max(), "conforms *"],
            ["AC impedance, 1 kHz (mOhm)", "28.0 max.", "%.2f" % acir.mean(), "%.2f" % acir.min(), "%.2f" % acir.max(),
             "conforms *"],
            ["Self-discharge K value (mV/day)", "0.080 max.", "%.3f" % kv.mean(), "%.3f" % kv.min(), "%.3f" % kv.max(),
             "conforms *"]]
    s = [Paragraph("Zelvora Cell s.r.o. &middot; Ostrava &middot; Quality", H1S),
         Paragraph("Certificate of analysis, lot ZC2638", H1),
         Paragraph("Product ZP-4820, pouch cell 3.87 V 4,820 mAh. Formation 14 to 19 September 2026, %s cells in %s "
                   "formation trays. Issued 22 September 2026." % ("{:,}".format(len(cells)), "{:,}".format(len(W.new.trays))),
                   H1S),
         _table(rows, [5.2 * cm, 2.6 * cm, 1.9 * cm, 1.9 * cm, 1.9 * cm, 1.8 * cm]),
         Paragraph("* Every cell is measured; cells outside the limits are marked in the cell data package and may be "
                   "rejected at the customer's incoming inspection under the quality agreement.", SMALL),
         Paragraph("The lot conforms to ZP-4820 datasheet revision 6 and to the quality agreement with Kalvenhorst "
                   "Systeme GmbH. Cycle life is qualified by the customer.", BODY)]
    d = _doc(path, "Certificate of analysis ZC2638", "Zelvora Quality")
    f = _footer("Zelvora Cell s.r.o.", "CoA ZC2638")
    d.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- the extracts notes
def _write_note(path, head, files, notes):
    lines = list(head) + [""]
    for f, desc, src in files:
        lines.append(f)
        lines.append("    " + desc)
        lines.append("    Source: " + src)
        lines.append("")
    lines += ["Notes"] + notes
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write("\n".join(lines) + "\n")


def write_readme(path, files):
    head = ["Kalvenhorst Systeme GmbH: extracts for the release of Zelvora lot ZC2638",
            "Pulled for Product Finance on 12 October 2026 by the battery reliability lab and the battery plant."]
    notes = [
        "- Cell serials: Zelvora writes ZC2638-3111526; cycler fleet A writes 2638.3111526; fleet B and the pack line's",
        "  scanner write ZC26383111526.",
        "- Fleet A's export separates fields with semicolons, writes decimal commas and Bielefeld wall time, and numbers",
        "  a test's first cycle 0. Fleet B's export writes UTC (ISO 8601, ending Z) and numbers a test's first cycle 1;",
        "  it is assembled from weekly pulls.",
        "- The release test register has a row for each test. A test stopped by a channel fault and continued on another",
        "  channel is a new test on that channel; the register lists it under the same cell with a note.",
        "- Life test results: EOL gives the cycles to 80 per cent of rated capacity, the first QP-3 cycle whose",
        "  discharge capacity is below 3,856 mAh; STOPPED gives the cycle at which the test stopped first.",
        "- Zelvora's tray key, in the cell data package and the register: T and five digits before lot %s; FT, the" %
        K.TRAY_KEY_CHANGE,
        "  lot's four digits and the tray number from %s." % K.TRAY_KEY_CHANGE,
        "- The genealogy has one row for each cell in a Model K pack; position 1 to 3 is the cell's place in the series",
        "  string.",
    ]
    _write_note(path, head, files, notes)


def write_service_readme(path, files):
    head = ["Kalvenhorst Systeme GmbH: service and costing extracts, Model K batteries",
            "Pulled for Product Finance by Service Operations on 5 October 2026 (case system, depot orders) and on",
            "9 October 2026 (returns depot log, carrier statement, partner invoices, rates and cost sheet)."]
    notes = [
        "- Service case system: one row per case in its latest state, times in UTC. fault_code: CAP the gauge reported",
        "  full charge capacity below 80 per cent; SWL swollen battery; CON contact fault; BMS charging electronics or",
        "  gauge fault; NFF no fault found. warranty: WTY battery warranty, GW goodwill, OOW at the customer's cost.",
        "  action REPLACED: a battery was fitted. battery_sn: the battery in the notebook when the case closed.",
        "  legacy_ref: order number in the DACH depot's former system.",
        "- The DACH depot (Bielefeld) kept its service orders in SAP until 1 March 2026 and has recorded its repairs in",
        "  the service case system since 2 March 2026. SAP fields: Auftragsart ZS01 warranty repair, ZS02 goodwill,",
        "  ZS03 at the customer's cost; Schadenscode B10 capacity below 80 per cent, B20 swollen, B30 contact fault,",
        "  B40 charging electronics or gauge, B90 no fault found; Ausbau-SN battery removed, Einbau-SN battery fitted;",
        "  Techn. Abschluss the day the repair was completed.",
        "- Service regions: DACH (DE, AT, CH), the Bielefeld depot (KVD); FRB (FR, BE, NL, LU), Dauvergne Réparation",
        "  (DVG); UKI (GB, IE), Tolley Marsh Repair (TMR); NOR (SE, NO, DK, FI), Ljungqvist Service (LJQ); SOU (ES, IT,",
        "  PT), Ferrucci Assistenza (FRC).",
        "- Partner invoices: one workbook per partner, one sheet per invoice, a line per job in the invoice's service",
        "  period, in the partner's own layout and currency.",
        "- Returns depot log: one row for each battery received at the Bielefeld returns depot; Reference is the case or",
        "  order it came from.",
        "- Treasury rates are units of each currency per euro at each month end.",
    ]
    _write_note(path, head, files, notes)
