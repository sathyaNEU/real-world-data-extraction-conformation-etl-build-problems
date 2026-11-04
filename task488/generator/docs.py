"""The pack's documents: the Operator's farm shift log, the supplier's recall notice, the corporation's QM-09 and
September's stock reconciliation."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import names as N    # noqa: E402
import sim           # noqa: E402
import world         # noqa: E402
from sim import DAY, H, M, T0, T1, T_RACK   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1c1f22")
GREY = colors.HexColor("#5d6369")
NAVY = colors.HexColor("#183a5a")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10, leading=13.4, textColor=INK, spaceAfter=5)
NUM = ParagraphStyle("num", parent=BODY, leftIndent=28, firstLineIndent=-28)
H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=13.5, leading=17, textColor=NAVY, spaceAfter=2)
SUB = ParagraphStyle("sub", fontName="LiberationSans", fontSize=9.2, leading=12, textColor=GREY, spaceAfter=8)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.2, leading=13.5, textColor=INK, spaceBefore=6,
                    spaceAfter=3)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.4, leading=10.4, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=7.8, leading=10, textColor=GREY)


def _doc(path, title, author, header, footer):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans-Bold", 8)
        canvas.setFillColor(NAVY)
        canvas.drawString(18 * mm, LETTER[1] - 12 * mm, header)
        canvas.setStrokeColor(colors.HexColor("#9aa3ab"))
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, LETTER[1] - 13.5 * mm, LETTER[0] - 18 * mm, LETTER[1] - 13.5 * mm)
        canvas.setFont("LiberationSans", 7.2)
        canvas.setFillColor(GREY)
        canvas.drawString(18 * mm, 11 * mm, footer)
        canvas.drawRightString(LETTER[0] - 18 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=19 * mm,
                          bottomMargin=18 * mm, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, head=True):
    data = [[Paragraph(str(c), CELLB if (i == 0 and head) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0, hAlign="LEFT")
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#a3abb2")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 3.5), ("RIGHTPADDING", (0, 0), (-1, -1), 3.5)]
    if head:
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e3e8ec")))
    t.setStyle(TableStyle(st))
    return t


def _hm(t):
    return N.local(t).strftime("%H:%M")


# ------------------------------------------------------------------------------------------------ the shift log
def shift_entries(W):
    rd = W["readings"]
    pcs = W["pcs"]
    lpd = [c for c in W["checks"] if c["kind"] == "lpd"]
    pc0 = rd[(pcs[0]["time"], pcs[0]["pit"])]
    pc1 = rd[(pcs[1]["time"], pcs[1]["pit"])]
    lpd0, lpd1 = lpd[0]["drain"].start, lpd[-1]["drain"].end
    import routes
    g2350 = 1286.4
    g0500 = g2350 - routes.pumped_between(W["hyd"], -10 * M, 5 * H) * 1.0018 / 1000.0
    shifts = [
        ("Monday 12 October 2026, day shift (05:00 to 17:00)", "R.M.", "K.T.", [
            (-DAY + 5 * H, "Handover from night shift. Hydrant pumps on Tank 2 (J-26-1171) since 08 Oct 09:40; rack "
                           "pump on Tank 2. Tank 1 settling J-26-1179; Tank 3 settling J-26-1187; Tank 4 empty, "
                           "inspected, ready to receive."),
            (-DAY + 5 * H + 40 * M, "Pump station: duty pumps P2 and P3, standby P1, P4 isolated for seal change."),
            (lpd0, "Weekly low point drain round started, branch end drains A, B, C, E, F and G."),
            (lpd1, "Low point drain round complete; samples recorded on the hydrant maintenance record."),
            (-DAY + 11 * H + 50 * M, "Filter vessel FV-2 differential pressure trending up, within limit; next check "
                                     "at 06:00 rounds."),
            (-DAY + 13 * H + 40 * M, "Laboratory certificate of quality received for J-26-1187 (Tank 3). Release "
                                     "planned for Tue 06:00 when Tank 2 runs down."),
            (-DAY + 15 * H + 5 * M, "Tank 1 J-26-1179 certificate received; held for release after Tank 3."),
        ]),
        ("Monday 12 October 2026, night shift (17:00 to 05:00)", "K.T.", "J.O.", [
            (-DAY + 17 * H, "Handover accepted. Hydrant and rack on Tank 2."),
            (-DAY + 21 * H + 15 * M, "Pump P4 seal change complete, returned to standby."),
            (-DAY + 23 * H + 50 * M, "Tank 2 gauge {:,.0f} m3; run-down to Tank 3 confirmed for 06:00.".format(g2350)),
            (2 * H + 30 * M, "Routine rounds, nothing to report."),
        ]),
        ("Tuesday 13 October 2026, day shift (05:00 to 17:00)", "J.O.", "P.S.", [
            (5 * H, "Handover accepted. Tank 2 gauge {:,.0f} m3.".format(g0500)),
            (T0, "Tank 3 (J-26-1187) lined up to the hydrant pumps and the rack pump; Tank 2 isolated."),
            (pcs[0]["time"], "Product change check at P-A01 (one hydrant line fill on the meter at %s): %.1f kg/m3 at "
                             "15 C, %d pS/m, clear and bright; matches J-26-1187." % (
                                 _hm(pcs[0]["metered_at"]), pc0["d15"], pc0["cond"])),
            (10 * H + 47 * M, "Pump station meter proved against the master meter, factor 1.0003 accepted; totaliser "
                              "restarted at zero."),
            (T_RACK, "Rack pump moved to Tank 1 (J-26-1179). Hydrant stays on Tank 3."),
            (13 * H + 30 * M, "Tank 4 receipt of J-26-1192 from the pipeline started."),
            (15 * H, "Airport Operations: stands 27 and 28 closed for apron resurfacing until Thu 15 Oct 06:00; pit "
                     "lids sealed."),
            (T1, "Hydrant pumps moved to Tank 1 (J-26-1179). Tank 3 isolated."),
        ]),
        ("Tuesday 13 October 2026, night shift (17:00 to 05:00)", "P.S.", "R.M.", [
            (17 * H, "Handover accepted. Hydrant on Tank 1, rack on Tank 1."),
            (pcs[1]["time"], "Product change check at P-A01 (one hydrant line fill on the meter at %s): %.1f kg/m3 at "
                             "15 C, %d pS/m, clear and bright; matches J-26-1179." % (
                                 _hm(pcs[1]["metered_at"]), pc1["d15"], pc1["cond"])),
            (22 * H + 40 * M, "Filter vessel FV-2 element change booked for Thursday."),
            (DAY + 1 * H + 15 * M, "Routine rounds, nothing to report."),
        ]),
        ("Wednesday 14 October 2026, day shift (05:00 to 17:00)", "R.M.", "", [
            (DAY + 5 * H, "Handover accepted. Hydrant and rack on Tank 1."),
            (DAY + 5 * H + 12 * M, "%s recall notice RN-2026-031 received for J-26-1187 (FAME above limit in the "
                                   "retained sample)." % N.SUPPLIER),
            (DAY + 5 * H + 30 * M, "Hydrant pumps stopped. All hydrant and refueller fuelling suspended; Corbel and "
                                   "Northgarth duty managers informed. Tank 3 quarantined."),
            (DAY + 5 * H + 55 * M, "N. Daugherty (fuel quality manager) informed. W. Hopkins calls the fuel quality "
                                   "committee for 08:00."),
            (DAY + 7 * H + 30 * M, "Records pulled for the committee: historian, register, maintenance record, "
                                   "agents' tickets and checks, rack log."),
        ]),
    ]
    return shifts


def write_shift_log(path, W):
    doc, frame = _doc(path, "Farm shift log", N.OPERATOR, "%s  |  Windrell fuel farm" % N.OPERATOR,
                      "FF-LOG-07 shift log  |  12 to 14 October 2026  |  controlled copy when printed")
    s = [Paragraph("Fuel farm shift log", H1),
         Paragraph("%s, operating the Windrell fuel farm, pump station, hydrant and truck rack for %s. "
                   "Times are local (PDT)." % (N.OPERATOR, N.CORP), SUB)]
    for title, sup, nxt, entries in shift_entries(W):
        rows = [["Time", "Entry", "By"]] + [[_hm(t), e, sup] for t, e in entries]
        block = [Paragraph(title, H2), _table(rows, [16 * mm, 140 * mm, 14 * mm])]
        if nxt:
            block.append(Paragraph("Shift supervisor %s. Handover accepted by %s." % (sup, nxt), SMALL))
        else:
            block.append(Paragraph("Shift supervisor %s. Shift in progress at the time of copying." % sup, SMALL))
        block.append(Spacer(1, 6))
        s.append(KeepTogether(block))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------ the recall notice
def write_recall(path):
    doc, frame = _doc(path, "Recall notice RN-2026-031", N.SUPPLIER, "%s  |  Product Quality" % N.SUPPLIER,
                      "RN-2026-031  |  issued 14 October 2026 05:05 PDT  |  supersedes none")
    s = [Paragraph("Product recall notice RN-2026-031", H1),
         Paragraph("To: %s; %s (Windrell fuel farm operator). Issued 14 October 2026, 05:05 PDT, by %s Product "
                   "Quality." % (N.CORP, N.OPERATOR, N.SUPPLIER), SUB)]
    s.append(_table([["Product", "Batch", "Delivered into", "Delivery", "Released at Windrell"],
                     ["Jet A-1", "J-26-1187", "Windrell Tank 3", "Pipeline, 10 to 11 October 2026", "13 October 2026, 06:00"]],
                    [22 * mm, 22 * mm, 30 * mm, 46 * mm, 44 * mm]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("1. Finding", H2))
    s.append(Paragraph("A retest of the retained sample of batch J-26-1187 at the Ostrey Point terminal laboratory on "
                       "13 October 2026 at 22:40 found fatty acid methyl ester (FAME) at 112 mg/kg against the "
                       "specification limit of 50 mg/kg. The batch's certificate of quality reported less than 5 "
                       "mg/kg. The likely source is a line flush at the terminal on 9 October; it is under "
                       "investigation.", BODY))
    s.append(Paragraph("2. Action required", H2))
    for n, t in (("2.1", "Stop issuing product from batch J-26-1187."),
                 ("2.2", "Quarantine all product from batch J-26-1187 wherever it is held, in storage tanks, in the "
                         "hydrant system and in vehicles, and hold it for collection or disposal as %s directs." % N.SUPPLIER),
                 ("2.3", "Identify every aircraft into which product from batch J-26-1187 has been delivered, in any "
                         "quantity, and advise the aircraft operator."),
                 ("2.4", "Return the recall return below within 24 hours of this notice.")):
        s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("3. Recall return", H2))
    s.append(Paragraph("One record for each uplift into which product from the batch was delivered:", BODY))
    s.append(_table([["Field", "Content"],
                     ["Ticket number", "the into-plane agent's delivery ticket"],
                     ["Into-plane agent", "the agent that delivered the fuel"],
                     ["Aircraft operator", "the operator of the aircraft fuelled"],
                     ["Flight", "the flight the uplift was for"],
                     ["Registration", "the aircraft registration"],
                     ["Uplift start (UTC)", "the start of the uplift"],
                     ["Location", "the hydrant pit or the refueller that delivered the fuel"],
                     ["Litres delivered (15 C)", "the uplift's litres at 15 C"],
                     ["Litres of J-26-1187 (15 C)", "the litres of the recalled batch in the uplift, at 15 C"]],
                    [48 * mm, 116 * mm]))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Questions on this notice to the terminal quality desk, 24 hours. Signed for %s Product "
                       "Quality: Terminal Quality Manager, Ostrey Point." % N.SUPPLIER, SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------ QM-09
def write_qm09(path):
    doc, frame = _doc(path, "QM-09 Product quarantine and recall", N.CORP,
                      "%s  |  Quality Manual" % N.CORP, "QM-09 revision 4  |  effective 1 March 2026  |  "
                      "approved by the Fuel Quality Committee")
    s = [Paragraph("QM-09 Product quarantine and recall", H1),
         Paragraph("Quality Manual of %s. Applies to the Operator (%s) and to each into-plane agent authorised at "
                   "%s." % (N.CORP, N.OPERATOR, N.AIRPORT), SUB)]
    p = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("1. Scope", H2))
    p("1.1", "Aviation fuel received, stored, issued and delivered through the Windrell facilities: the fuel farm "
             "tanks, the hydrant network, the truck rack and the refuellers.")
    s.append(Paragraph("2. Definitions", H2))
    p("2.1", "<b>Batch</b>: product received into one tank under one certificate of quality and identified by its "
             "batch number.")
    p("2.2", "<b>Hydrant section</b>: a part of the hydrant network isolated by its section valve, as listed in the "
             "hydrant network register.")
    p("2.3", "<b>Refueller</b>: a vehicle tank that carries product from the truck rack to aircraft, as listed in the "
             "into-plane equipment register.")
    p("2.4", "<b>Uplift</b>: one delivery of fuel into one aircraft, recorded on the into-plane agent's ticket.")
    s.append(Paragraph("3. Quarantine on recall", H2))
    p("3.1", "On notice that a released batch is recalled, the Operator's duty supervisor suspends hydrant and "
             "refueller fuelling at once and informs each into-plane agent and the Operator's fuel quality manager.")
    p("3.2", "Every storage tank, hydrant section and refueller holding product from the recalled batch when fuelling "
             "is suspended is quarantined, and is drained before it is used again; the drained product is held for "
             "the supplier.")
    p("3.3", "Quantities under this procedure are stated in litres at 15 C.")
    p("3.4", "Fuelling resumes from a hydrant section or a refueller only with the approval of the Fuel Quality "
             "Committee.")
    s.append(Paragraph("4. Notification", H2))
    p("4.1", "The Operator notifies the operator of every aircraft into which product from the recalled batch was "
             "delivered, in any quantity, from the batch's release to the suspension. Each notification lists every "
             "such uplift with the agent's ticket number, the registration, the flight, the start of the uplift in "
             "UTC, the pit or refueller, the litres delivered and the litres of the recalled batch among them.")
    p("4.2", "The recall return to the supplier lists the same uplifts in the supplier's format.")
    s.append(Paragraph("5. Records", H2))
    p("5.1", "The Operator keeps the hydrant network register, the farm shift log, the pump station historian and "
             "the hydrant maintenance record. Each into-plane agent keeps its tickets, its daily check records and "
             "its equipment records, and gives the Operator copies on request.")
    s.append(Spacer(1, 8))
    s.append(_table([["Revision", "Date", "Change"],
                     ["3", "12 May 2023", "Refuellers brought within section 3; notification by ticket."],
                     ["4", "1 March 2026", "Section 4.1 lists the uplift record; quantities at 15 C (3.3)."]],
                    [20 * mm, 28 * mm, 116 * mm]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Approved for the Fuel Quality Committee by the chair, 1 March 2026.", SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------ the distractor
def stock_rows(base):
    """September 2026's stock reconciliation by tank, in cubic metres at 15 C; every line and total adds."""
    out = []
    for tank, op, rec, hyd, rack, phys in base:
        book = round(op + rec - hyd - rack, 1)
        gl = round(phys - book, 1)
        out.append((tank, op, rec, hyd, rack, book, phys, gl, round(100 * gl / (hyd + rack), 3)))
    tot = [round(sum(r[i] for r in out), 1) for i in range(1, 8)]
    out.append(("All tanks", *tot, round(100 * tot[6] / (tot[2] + tot[3]), 3)))
    return out


def write_stock(path, base):
    doc, frame = _doc(path, "Stock reconciliation September 2026", N.OPERATOR, "%s  |  Windrell fuel farm" % N.OPERATOR,
                      "FF-STK-09  |  September 2026 monthly reconciliation  |  for %s" % N.CORP)
    s = [Paragraph("Monthly stock reconciliation, September 2026", H1),
         Paragraph("Jet A-1, cubic metres at 15 C, 1 September 00:00 to 30 September 24:00. Book stock from receipts "
                   "and metered issues; physical stock from the automatic tank gauges at month end.", SUB)]
    rows = [["Tank", "Opening", "Receipts", "Hydrant issues", "Rack issues", "Closing book", "Closing physical",
             "Gain (loss)", "Per cent of issues"]]
    table = stock_rows(base)
    for r in table:
        rows.append([r[0]] + ["{:,.1f}".format(v) for v in r[1:8]] + ["%.3f" % r[8]])
    s.append(_table(rows, [20 * mm, 18 * mm, 18 * mm, 20 * mm, 17 * mm, 19 * mm, 20 * mm, 17 * mm, 17 * mm]))
    s.append(Spacer(1, 6))
    tot = table[-1]
    big = max(table[:-1], key=lambda r: r[3])
    s.append(Paragraph("The month's net loss, %s m3 or %.3f per cent of issues, is inside the 0.10 per cent the supply "
                       "agreement allows. %s carried the largest hydrant issues; each tank took one receipt except "
                       "Tank 1, which took two." % ("{:,.1f}".format(-tot[7]), -tot[8], big[0]), BODY))
    s.append(Spacer(1, 10))
    s.append(Paragraph("Prepared by the Operator's farm accountant, 5 October 2026. Reviewed for %s." % N.CORP, SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)
