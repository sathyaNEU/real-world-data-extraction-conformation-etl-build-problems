"""The pack's documents: the plot register (XLSX), the company's field manual with its volume table, the board's
salvage policy, the burn boss's 2024 unit reports and the 2025 fire report (PDF). Each is written in its own form."""
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                    # noqa: E402
from reportlab.lib.pagesizes import letter                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                     # noqa: E402
from reportlab.lib.units import inch                                # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402
from openpyxl import Workbook                                       # noqa: E402
from openpyxl.styles import Alignment, Font                         # noqa: E402

import numpy as np   # noqa: E402

import world as W   # noqa: E402

BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=6)
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8.2, leading=10.4, spaceAfter=3)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5, leading=13.5, spaceBefore=8, spaceAfter=3)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=3)
SUB = ParagraphStyle("u", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#444444"), spaceAfter=10)
FORM = ParagraphStyle("f", fontName="Courier", fontSize=9, leading=11.5, spaceAfter=2)


def _doc(path, title, owner, footer):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.8 * inch, title=title, author=owner, creator=owner, producer=owner, subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 7.4)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.9 * inch, 0.5 * inch, footer)
        c.drawRightString(letter[0] - 0.9 * inch, 0.5 * inch, "Page %d" % d_.page)
        c.restoreState()
    return d, frame


def _table(rows, widths, font=8.4, head_font="Helvetica-Bold"):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", font), ("FONT", (0, 0), (-1, 0), head_font, font),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6), ("TOPPADDING", (0, 0), (-1, -1), 1.6)]))
    return t


def write_register(path, x):
    rng = np.random.default_rng(W.SEED + 41)
    wb = Workbook()
    ws = wb.active
    ws.title = "Plots"
    ws.append(["Plot", "Stand", "Cond 1 share", "Cond 2 stand", "Cond 2 share", "UTM E (m)", "UTM N (m)",
               "Elev (ft)", "Slope (%)", "Aspect (deg)", "Installed", "Notes"])
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True)
    notes = ["centre stake replaced 2016", "witness tree blown down, new witness DF", "skid trail crosses NE quarter",
             "spring on W edge", "access from spur 4N12", "steep, rope needed", "cap missing, rebar found 2021"]
    for p in x["plots"]:
        note = None
        if p["nb"]:
            note = "boundary mapped 2021"
        elif rng.random() < 0.08:
            note = notes[int(rng.integers(0, len(notes)))]
        ws.append([p["plot"], p["stand"], p["share"], p["nb"], round(1 - p["share"], 2) if p["nb"] else None,
                   round(p["x"]), round(p["y"]), p["elev"], p["slope"], p["aspect"], p["est"], note])
    for col, wd in zip("ABCDEFGHIJKL", (6, 8, 8, 9, 8, 10, 11, 8, 8, 8, 8, 30)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A2"
    wb.save(path)


def write_manual(path):
    d, frame = _doc(path, "Continuous Forest Inventory Field Manual", W.COMPANY,
                    "%s, Forestry Department. CFI Field Manual, revision 2026" % W.COMPANY)
    vol = [["DBH"] + ["%g" % L for L in W.VOL_LOGS]]
    for c in W.VOL_DBH:
        vol.append(["%d" % c] + ["%d" % W.scribner_c(c, L) for L in W.VOL_LOGS])
    story = [Paragraph("%s" % W.COMPANY, TITLE),
             Paragraph("Continuous Forest Inventory Field Manual. Revision 2026, for the 2026 remeasurement and the "
                       "new data collector; replaces the 2015 manual.", SUB),
             Paragraph("1. Plots", HEAD),
             Paragraph("Permanent plots are fixed-area circles of one fifth acre (radius 52.7 feet, horizontal "
                       "distance), remeasured every five years in summer. Plot centres are monumented and located from "
                       "the plot register. Plots that straddle a stand boundary were mapped by condition in 2021: the "
                       "register gives each condition's stand and its share of the plot, and each tree record carries "
                       "its condition. A stand's per-acre figures are taken over the plot conditions mapped to it.", BODY),
             Paragraph("2. Trees", HEAD),
             Paragraph("Every live tree 5.0 inches DBH and larger is tallied. Trees carry numbered aluminium tags "
                       "nailed on the uphill side at breast height, and are located by azimuth from true north and "
                       "horizontal distance from plot centre to the face of the tree. DBH is taken to the tenth of an "
                       "inch with a diameter tape. Basal area in square feet is 0.005454 times the square of DBH in "
                       "inches.", BODY),
             Paragraph("Status codes at remeasurement: L live, D dead, C cut, M not found, N added (tag from the "
                       "crew's series). Damage codes: FIRE bole char, BB bark beetle, BTOP broken top, FORK, LEAN.", BODY),
             Paragraph("3. Sawtimber and volume", HEAD),
             Paragraph("Conifers 11.0 inches DBH and larger are sawtimber. Record merchantable height in feet to a "
                       "6-inch top. For volume, merchantable height is converted to 16-foot logs by dividing by 16.5 "
                       "and rounding down to the half log, at most six logs, and gross volume is read from Table 1 at "
                       "the tree's 2-inch DBH class (11.0 to 12.9 inches is class 12). Net volume is gross volume less "
                       "the recorded cull per cent. Black oak is not sawtimber.", BODY),
             Paragraph("Table 1. Scribner Decimal C volume in tens of board feet, by 2-inch DBH class (rows) and "
                       "number of 16-foot logs (columns)", SMALL),
             _table(vol, [0.55 * inch] + [0.52 * inch] * len(W.VOL_LOGS), font=7.4)]
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def write_policy(path):
    d, frame = _doc(path, "Board Policy %s Salvage Marking" % W.POLICY_NO, W.COMPANY, "Adopted by the Board of Directors, August 13, 2026")
    story = [Paragraph(W.COMPANY.upper(), TITLE), Paragraph("Board Policy %s: Salvage Marking" % W.POLICY_NO, SUB),
             Paragraph("1. Purpose", HEAD),
             Paragraph("The company recovers timber killed by fire, insects and disease while it is still "
                       "merchantable. This policy sets which stands the forestry department marks for salvage in the "
                       "operating season after each remeasurement of the permanent plots.", BODY),
             Paragraph("2. Marking rule", HEAD),
             Paragraph("A stand is marked when the basal area of the trees tallied live at its previous measurement "
                       "that are not tallied live at the remeasurement, other than trees recorded as cut, is 15 per cent "
                       "or more of the basal area of the trees tallied live at its previous measurement. Basal area is "
                       "taken at each tree's diameter at the previous measurement, over the trees on the plot "
                       "conditions mapped to the stand.", BODY),
             Paragraph("For the 2027 operating season the previous measurement is 2021 and the remeasurement 2026.", BODY),
             Paragraph("3. Reporting", HEAD),
             Paragraph("The forestry manager brings the marking list to the board's December meeting with every "
                       "stand's share under section 2, its live basal area per acre and its net sawtimber volume per "
                       "acre at the remeasurement.", BODY),
             Paragraph("4. Review", HEAD),
             Paragraph("The board reviews this policy after the 2031 remeasurement.", BODY)]
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def write_burns(path):
    d, frame = _doc(path, "Prescribed Burn Unit Reports, Fall 2024", W.COMPANY, "Burn unit reports, fall 2024")
    rng = np.random.default_rng(W.SEED + 31)
    story = [Paragraph("Prescribed Burn Unit Reports", TITLE),
             Paragraph("Fall 2024 season. One report per unit, filed by the burn boss after mop-up.", SUB)]
    ac = {s: a for s, a, _ in W.STANDS}
    for sid, date in W.BURN_DATES.items():
        fl = "%.0f-%.0f" % (rng.uniform(0.5, 1.5), rng.uniform(2.0, 4.0))
        ch = "%.0f-%.0f" % (rng.uniform(1.5, 3.0), rng.uniform(6.0, 10.0))
        story += [Paragraph("Unit %s. Ignition %s" % (sid, date), HEAD),
                  _table([["Acres", "Ignition", "Flame length (ft)", "Bole char ht (ft)", "Min RH (%)", "Max wind (mph)"],
                          [str(ac[sid]), "strip head fire", fl, ch, "%d" % rng.integers(22, 38), "%d" % rng.integers(4, 11)]],
                         [0.55 * inch, 1.05 * inch, 1.1 * inch, 1.15 * inch, 0.85 * inch, 1.0 * inch]),
                  Paragraph("Holding: no spots or slopovers. Mop-up complete %s. Smoke dispersed by afternoon on "
                            "ignition day." % ["two days after ignition", "three days after ignition",
                                               "four days after ignition"][int(rng.integers(0, 3))], BODY)]
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def write_fire(path):
    d, frame = _doc(path, "Juniper Saddle Fire Report", W.COMPANY, "Fire report, %s" % W.WILDFIRE[2])
    story = [Paragraph("%s" % W.WILDFIRE[2], TITLE),
             Paragraph("Fire report to the board, October 2025. Lightning start, August 14, 2025.", SUB),
             Paragraph("A lightning start on the ridge above Juniper Saddle on August 14, 2025 burned 241 acres before "
                       "containment on August 19, nearly all of it in stand %s. Burn severity was high across most of the "
                       "stand: crowns were consumed on the upper slopes and the overstory below the ridge was largely "
                       "killed. Suppression lines were rehabilitated in September. Salvage of the stand is under "
                       "review." % W.WILDFIRE[0], BODY)]
    d.build(story, onFirstPage=frame, onLaterPages=frame)
