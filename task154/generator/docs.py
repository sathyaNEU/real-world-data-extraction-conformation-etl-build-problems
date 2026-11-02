"""The pack's documents: the licensing team's pre-application letter, the 2015 licence, the geological extract with
its map, section and borehole logs, the annual abstraction returns and the line 5 project brief. The text is held here
as data so checks.py can quote it and execute every filed sentence."""
from __future__ import annotations

import datetime as dt
import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import (Flowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,  # noqa: E402
                                TableStyle)

import common as K          # noqa: E402
import world as W           # noqa: E402

F_LETTER = "pre-application_advice_BH2_2026-09-22.pdf"
F_LICENCE = "abstraction_licence_MA-28-15-0042.pdf"
F_GEOLOGY = "brackenholt_geology_and_borehole_records.pdf"
F_RETURNS = "bh2_abstraction_returns_2015-2026.pdf"
F_BRIEF = "line5_project_brief.docx"

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("LibSerif", "liberation/LiberationSerif-Regular.ttf"), ("LibSerif-Bold", "liberation/LiberationSerif-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d2126")
GREY = colors.HexColor("#5e656e")
REG = colors.HexColor("#00594f")        # the licensing team's green
BGS = colors.HexColor("#3b3b6d")
RULE = colors.HexColor("#a6adb6")
HEAD = colors.HexColor("#e7ecef")


def styles(font, bold, accent, size=9.8):
    return dict(
        body=ParagraphStyle("b" + font + str(size), fontName=font, fontSize=size, leading=size * 1.36, textColor=INK,
                            spaceAfter=4),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=14, leading=18, textColor=accent, spaceAfter=3),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=8.6, leading=11.4, textColor=GREY, spaceAfter=8),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=10.6, leading=13.6, textColor=accent, spaceBefore=6,
                          spaceAfter=2),
        cell=ParagraphStyle("c" + font, fontName=font, fontSize=8.0, leading=9.8, textColor=INK),
        cellr=ParagraphStyle("cr" + font, fontName=font, fontSize=8.0, leading=9.8, textColor=INK, alignment=2),
        cellb=ParagraphStyle("cb" + font, fontName=bold, fontSize=8.0, leading=9.8, textColor=INK),
        cellbr=ParagraphStyle("cbr" + font, fontName=bold, fontSize=8.0, leading=9.8, textColor=INK, alignment=2),
        small=ParagraphStyle("sm" + font, fontName=font, fontSize=7.8, leading=10.0, textColor=GREY, spaceAfter=3))


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, subject="", creator="", producer="")


def _footer(left, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 10 * mm, left)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def grid(rows, widths, st, right_from=1, bold_rows=()):
    data = []
    for k, row in enumerate(rows):
        cells = []
        for j, c in enumerate(row):
            if k == 0 or k in bold_rows:
                sty = st["cellbr"] if j >= right_from else st["cellb"]
            else:
                sty = st["cellr"] if j >= right_from else st["cell"]
            cells.append(Paragraph(esc(str(c)), sty))
        data.append(cells)
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("BACKGROUND", (0, 0), (-1, 0), HEAD),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]))
    return t


def protected_rows():
    rows = []
    for name, lic, holder, xy, avail, rest, qd in K.PROTECTED:
        e, n = K.to_grid(xy)
        rows.append((name, lic, holder, K.grid_ref(e, n), rest, avail, qd))
    return rows


# ------------------------------------------------------------------------------------------------- the letter
LETTER_TEST = (
    "For each protected abstraction in the table below, predict the drawdown in the Sherwood Sandstone at the "
    "protected borehole on 31 March 2039, measured from its rest water level in April 2015, with Borehole 2 "
    "abstracting continuously at 1,200 cubic metres a day from 1 April 2015 to 31 March 2027 and at the daily quantity "
    "you apply for from 1 April 2027 to 31 March 2039.")
LETTER_RULE = (
    "We will not grant a daily quantity for which the predicted drawdown at any protected borehole exceeds the "
    "available drawdown shown for it in the table.")


def letter_paragraphs():
    officer = K.PEOPLE["officer"]
    return [
        ("p", "Our ref: WR/MA/28/15/0042/PA1. Your ref: BSW/LIC/2026."),
        ("p", K.long_date(K.LETTER_DATE)),
        ("p", "Mr Francis Mason, Water Resources Lead, %s, Brackenholt Bottling Plant, Coldharbour Lane, Brackenholt." % K.COMPANY),
        ("h", "Pre-application advice: renewal and variation of abstraction licence MA/28/15/0042 (Borehole 2, Brackenholt)"),
        ("p", "Thank you for your request of 2 September 2026. Licence MA/28/15/0042 authorises abstraction from "
              "Borehole 2 of 1,200 cubic metres a day and 400,000 cubic metres a year and expires on 31 March 2027. "
              "You intend to apply to renew it to 31 March 2039, the common end date for the Sherwood Sandstone in this "
              "catchment, and to vary the daily quantity to supply a fifth bottling line."),
        ("h", "Protected rights"),
        ("p", "Three licensed abstractions draw on the same aquifer close enough to Borehole 2 for a change in its "
              "abstraction to reach them. Each is a protected right, and the renewed licence must not derogate from "
              "it."),
        ("p", LETTER_TEST),
        ("p", LETTER_RULE),
        ("table", None),
        ("p", "The available drawdown is the fall in water level the holder's borehole can take before its pump "
              "intake is uncovered, less a 1 metre allowance, from the borehole records we hold."),
        ("h", "What to send with the application"),
        ("p", "Please send, by 18 December 2026: the predicted drawdown at each protected borehole and the largest "
              "daily quantity that meets the test; the observation borehole record that condition 9 of the licence "
              "requires, from April 2015; your abstraction returns from April 2015; and the water used per litre of "
              "product on each bottling line in the 2025-26 licence year, with the new line's expected use. Our "
              "observation borehole record at Windle Cross is enclosed for the regional level, and the 2014 "
              "pumping test data you supplied for the original application remain on our file."),
        ("p", "This advice is given without prejudice to our determination of the application."),
        ("p", "Yours sincerely,"),
        ("p", "%s, Senior Permitting Officer, %s" % (officer, K.REGULATOR)),
    ]


def write_letter(out):
    st = styles("LibSans", "LibSans-Bold", REG, 9.6)
    path = os.path.join(out, F_LETTER)
    doc = _doc(path, "Pre-application advice MA/28/15/0042", K.REGULATOR)
    flow = [Paragraph(esc(K.REGULATOR), st["h1"]),
            Paragraph("Water resources permitting", st["sub"])]
    for kind, text in letter_paragraphs():
        if kind == "h":
            flow.append(Paragraph(esc(text), st["h2"]))
        elif kind == "table":
            rows = [["Protected abstraction", "Licence", "Holder", "Borehole", "Rest water level April 2015 (m AOD)",
                     "Available drawdown (m)"]]
            for name, lic, holder, gr, rest, avail, qd in protected_rows():
                rows.append([name, lic, holder, gr, "%.2f" % rest, "%.2f" % avail])
            flow.append(grid(rows, [33 * mm, 25 * mm, 32 * mm, 30 * mm, 26 * mm, 22 * mm], st, right_from=4))
            flow.append(Spacer(1, 4))
        else:
            flow.append(Paragraph(esc(text), st["body"]))
    doc.build(flow, onFirstPage=_footer(K.REGULATOR, "LibSans"), onLaterPages=_footer(K.REGULATOR, "LibSans"))


# ------------------------------------------------------------------------------------------------- the licence
LICENCE_CONDITIONS = [
    ("1", "Source of supply", "Sherwood Sandstone, groundwater."),
    ("2", "Point of abstraction", "Borehole 2 at %s." % K.grid_ref(K.BH2_E, K.BH2_N)),
    ("3", "Means of abstraction", "One borehole pump."),
    ("4", "Purpose", "Bottling of spring water, supply of water in bulk, and associated process and cleaning uses."),
    ("5", "Maximum quantities", "1,200 cubic metres a day; 400,000 cubic metres a year."),
    ("6", "Day and year", "In this licence a day is a period of 24 hours beginning at midnight, local time, and a "
                          "year is the period of twelve months beginning on 1 April."),
    ("7", "Metering", "The licence holder shall install, maintain and keep in good working order a meter to measure "
                      "the water abstracted, read it at least weekly and keep the readings for six years."),
    ("8", "Returns", "By 28 April each year the licence holder shall send a return of the volume abstracted in each "
                     "month of the year ending on the previous 31 March."),
    ("9", "Monitoring", "The licence holder shall record the water level in observation boreholes OB1, OB2 and OB3 "
                        "at least monthly and keep the record for the life of the licence."),
    ("10", "Expiry", "This licence expires on 31 March 2027."),
]


def write_licence(out):
    st = styles("LibSerif", "LibSerif-Bold", REG, 9.8)
    path = os.path.join(out, F_LICENCE)
    doc = _doc(path, "Licence to abstract water MA/28/15/0042", K.REGULATOR)
    flow = [Paragraph(esc(K.REGULATOR), st["h1"]),
            Paragraph("Licence to abstract water. Licence number MA/28/15/0042", st["h2"]),
            Paragraph(esc("Licence holder: %s, Brackenholt Bottling Plant, Coldharbour Lane, Brackenholt. Issued "
                          "26 March 2015; effective from 1 April 2015." % K.COMPANY), st["body"]),
            Spacer(1, 4)]
    rows = [["No.", "Condition", "Terms"]] + [list(c) for c in LICENCE_CONDITIONS]
    flow.append(grid(rows, [12 * mm, 38 * mm, 118 * mm], st, right_from=9))
    flow.append(Spacer(1, 8))
    flow.append(Paragraph(esc("Signed for the licensing authority, 26 March 2015."), st["body"]))
    doc.build(flow, onFirstPage=_footer("MA/28/15/0042", "LibSerif"), onLaterPages=_footer("MA/28/15/0042", "LibSerif"))


# ------------------------------------------------------------------------------------------------- geology
def fault_points():
    """Two points on the fault trace the memoir names (where it crosses the Windle Cross road and the old mineral
    railway), to the nearest 10 metres."""
    p0 = K.FAULT_DIST * W.np.array(K.normal())
    s_hat = W.np.array([W.np.sin(W.np.deg2rad(K.STRIKE_DEG)), W.np.cos(W.np.deg2rad(K.STRIKE_DEG))])
    pts = []
    for lam in (-1300.0, 1700.0):
        xy = p0 + lam * s_hat
        e, n = K.to_grid(xy)
        pts.append((round(e, -1), round(n, -1)))
    return pts


class MapFlowable(Flowable):
    """The geological map extract: national grid lines every kilometre, the fault trace with its downthrow tick, the
    boreholes, the brook and the road. Solid geology: Mercia Mudstone at rockhead over the whole sheet."""

    def __init__(self, width, height):
        super().__init__()
        self.width, self.height = width, height
        self.e0, self.e1 = 382500.0, 388500.0
        self.n0, self.n1 = 338500.0, 344500.0

    def xy(self, e, n):
        return ((e - self.e0) / (self.e1 - self.e0) * self.width, (n - self.n0) / (self.n1 - self.n0) * self.height)

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(colors.HexColor("#efe2d0"))
        c.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        c.setStrokeColor(colors.HexColor("#b9b2a6"))
        c.setLineWidth(0.3)
        c.setFont("LibSans", 6.2)
        c.setFillColor(GREY)
        for e in range(383000, 388001, 1000):
            x, _ = self.xy(e, self.n0)
            c.line(x, 0, x, self.height)
            c.drawCentredString(x, -7, "%d" % (e // 1000 % 100))
        for n in range(339000, 344001, 1000):
            _, y = self.xy(self.e0, n)
            c.line(0, y, self.width, y)
            c.drawRightString(-2, y - 2, "%d" % (n // 1000 % 100))
        # Brackenholt Brook and the Windle Cross road
        c.setStrokeColor(colors.HexColor("#5b8db8"))
        c.setLineWidth(0.9)
        brook = [(382500, 343700), (383600, 343100), (384500, 342600), (385300, 341900), (386100, 341400),
                 (387000, 340200), (388500, 339500)]
        pts = [self.xy(*p) for p in brook]
        for a, b in zip(pts, pts[1:]):
            c.line(a[0], a[1], b[0], b[1])
        c.setStrokeColor(colors.HexColor("#8a6d3b"))
        c.setLineWidth(0.6)
        road = [(382500, 340600), (384200, 340950), (385600, 341100), (386900, 340800), (388500, 340300)]
        pts = [self.xy(*p) for p in road]
        for a, b in zip(pts, pts[1:]):
            c.line(a[0], a[1], b[0], b[1])
        # the fault, drawn through the memoir's two points and continued across the sheet
        (e_a, n_a), (e_b, n_b) = fault_points()
        de, dn = e_b - e_a, n_b - n_a
        t0 = (self.n0 - n_a) / dn
        t1 = (self.n1 - n_a) / dn
        fa = self.xy(e_a + t0 * de, n_a + t0 * dn)
        fb = self.xy(e_a + t1 * de, n_a + t1 * dn)
        c.setStrokeColor(colors.HexColor("#b0182b"))
        c.setLineWidth(1.4)
        c.line(fa[0], fa[1], fb[0], fb[1])
        mid = self.xy((e_a + e_b) / 2, (n_a + n_b) / 2)
        c.setLineWidth(1.0)
        c.line(mid[0], mid[1], mid[0] + 6, mid[1] - 1.6)
        c.setFillColor(colors.HexColor("#b0182b"))
        c.setFont("LibSans-Bold", 6.6)
        c.drawString(fb[0] - 66, fb[1] - 14, "Coldharbour Fault")
        # boreholes
        c.setFont("LibSans", 6.0)
        pts = [("BH2", K.BH2["xy"]), ("OB1", K.OBS["OB1"]["xy"]), ("OB2", K.OBS["OB2"]["xy"]),
               ("OB3", K.OBS["OB3"]["xy"]), ("Windle Cross OBH", K.RMB["xy"])]
        pts += [(p[0], p[3]) for p in K.PROTECTED]
        for name, xy in pts:
            e, n = K.to_grid(xy)
            x, y = self.xy(e, n)
            c.setFillColor(INK)
            c.circle(x, y, 1.6, stroke=0, fill=1)
            dx, dy = 3, 2
            if name == "OB1":
                dx, dy = -14, 3
            if name == "OB2":
                dx, dy = 3, -6
            c.drawString(x + dx, y + dy, name)
        c.setStrokeColor(INK)
        c.setLineWidth(0.5)
        c.rect(0, 0, self.width, self.height, stroke=1, fill=0)
        c.restoreState()


SECTION_LAYERS = [
    # (from, to) metres below ground at BH2's side and at Windle Cross's side of the fault
    ("BH2 side", [("Made ground and boulder clay", 0, 7), ("Mercia Mudstone Group", 7, 72),
                  ("Sherwood Sandstone Group", 72, 214), ("Permian mudstones (Manchester Marl equivalent)", 214, 240)]),
    ("Windle Cross side", [("Alluvium", 0, 4), ("Mercia Mudstone Group", 4, 333), ("Sherwood Sandstone Group", 333, 471)]),
]


def logs():
    """Drillers' and geologists' logs held for the boreholes on the sheet."""
    out = []
    out.append(("BH2 (production)", K.grid_ref(K.BH2_E, K.BH2_N), "%.2f" % K.BH2["gl"], [
        ("0.0", "6.5", "Brown silty sandy clay with gravel (boulder clay)"),
        ("6.5", "71.8", "Red-brown mudstone with grey-green bands, occasional gypsum; firm to hard"),
        ("71.8", "160.0", "Red medium-grained sandstone, weakly cemented, pebbly in part; water struck 74.2 m, rose to 8.1 m bgl"),
    ], "Plain casing 0-84 m (300 mm), screen 84-160 m (250 mm). Test pumped June 2014."))
    for ob, info in K.OBS.items():
        e, n = K.to_grid(info["xy"])
        top_ss = {"OB1": 72.6, "OB2": 71.1, "OB3": 76.4}[ob]
        out.append(("%s (observation)" % ob, K.grid_ref(e, n), "%.2f" % info["gl"], [
            ("0.0", "%.1f" % (5.5 + 0.8 * len(ob) % 3), "Boulder clay"),
            ("%.1f" % (5.5 + 0.8 * len(ob) % 3), "%.1f" % top_ss, "Red-brown mudstone, gypsiferous"),
            ("%.1f" % top_ss, "%.1f" % info["depth"], "Red sandstone, fine to medium grained"),
        ], "Casing 0-%d m, slotted below. Drilled May 2014." % int(top_ss + 6)))
    e, n = K.to_grid(K.RMB["xy"])
    out.append(("Windle Cross OBH (regional monitoring)", K.grid_ref(e, n), "%.2f" % K.RMB["gl"], [
        ("0.0", "3.8", "Alluvium: grey silty clay and gravel"),
        ("3.8", "332.6", "Red-brown and grey-green mudstone with siltstone bands and gypsum veins"),
        ("332.6", "410.0", "Red sandstone, medium grained, well sorted"),
    ], "Casing to 338 m, open hole below. Drilled 2008 for the regional observation network."))
    pumps = {"Lower Hay Farm": (95.0, 21.0), "Kilnbrook Nurseries": (110.0, 24.0), "Hollin Bank Golf Club": (118.0, 23.5)}
    for name, lic, holder, xy, avail, rest, qd in K.PROTECTED:
        e, n = K.to_grid(xy)
        dep, pump = pumps[name]
        out.append(("%s borehole" % name, K.grid_ref(e, n), "", [
            ("0.0", "%.0f" % (68 + (len(name) % 7)), "Clay and marl (driller)"),
            ("%.0f" % (68 + (len(name) % 7)), "%.0f" % dep, "Red rock, water bearing (driller)"),
        ], "Licence %s. Pump intake %.1f m below ground." % (lic, pump)))
    return out


MEMOIR = [
    ("Stratigraphy", "The Sherwood Sandstone Group comprises red, medium-grained, weakly to moderately cemented "
                     "sandstones about 140 m thick in this district. It is overlain by the Mercia Mudstone Group, red-"
                     "brown mudstones with gypsum, which crops out over the whole of the sheet extract and thickens "
                     "eastwards. Glacial till and alluvium cover the rockhead in places."),
    ("Structure", None),
    ("Boreholes", "Logs for the boreholes on the extract are reproduced below from the records held by the survey "
                  "and the licensing authority. Levels are in metres above Ordnance Datum and depths in metres below "
                  "ground level unless stated."),
]


def structure_text():
    (e_a, n_a), (e_b, n_b) = fault_points()
    return ("The district lies on the eastern margin of a gently westward-dipping block. The Coldharbour Fault, "
            "which trends about north-north-east across the extract, crosses the Windle Cross road at %s and the "
            "disused mineral railway at %s. It is downthrown to the east by about 260 m, so that east of the fault "
            "the top of the Sherwood Sandstone lies at about 240 m below Ordnance Datum and the Mercia Mudstone is "
            "correspondingly thicker; west of the fault the top of the sandstone lies between 20 and 25 m above "
            "Ordnance Datum. No other faults with a throw greater than 10 m are known within 5 km of Brackenholt."
            % (K.grid_ref(e_a, n_a), K.grid_ref(e_b, n_b)))


def write_geology(out):
    st = styles("Carlito", "Carlito-Bold", BGS, 9.6)
    path = os.path.join(out, F_GEOLOGY)
    doc = _doc(path, "Brackenholt: geology and borehole records", "Geological records extract")
    flow = [Paragraph("Brackenholt district: solid geology and borehole records", st["h1"]),
            Paragraph("Extract compiled for the licensing file MA/28/15/0042. National grid square SJ; "
                      "kilometre numbers shown on the margins.", st["sub"])]
    for head, text in MEMOIR:
        flow.append(Paragraph(head, st["h2"]))
        flow.append(Paragraph(esc(text if text is not None else structure_text()), st["body"]))
    flow.append(Spacer(1, 10))
    flow.append(MapFlowable(150 * mm, 150 * mm))
    flow.append(Spacer(1, 10))
    flow.append(Paragraph("Map extract: solid geology, Mercia Mudstone Group at rockhead throughout. Red line: "
                          "Coldharbour Fault, tick on the downthrown side. Blue: Brackenholt Brook. Brown: Windle "
                          "Cross road.", st["small"]))
    flow.append(PageBreak())
    flow.append(Paragraph("Section through Borehole 2 and Windle Cross", st["h2"]))
    rows = [["Unit", "BH2 side, depth (m)", "Windle Cross side, depth (m)"]]
    names = ["Made ground, till or alluvium", "Mercia Mudstone Group", "Sherwood Sandstone Group",
             "Permian mudstones"]
    left = SECTION_LAYERS[0][1]
    right = SECTION_LAYERS[1][1]
    for i, nm in enumerate(names):
        l = left[i] if i < len(left) else None
        r = right[i] if i < len(right) else None
        rows.append([nm, "%d to %d" % (l[1], l[2]) if l else "-", "%d to %d" % (r[1], r[2]) if r else "not reached"])
    flow.append(grid(rows, [62 * mm, 50 * mm, 54 * mm], st, right_from=1))
    flow.append(Spacer(1, 8))
    flow.append(Paragraph("Borehole logs", st["h2"]))
    for name, gr, gl, layers, note in logs():
        flow.append(Paragraph(esc("%s. %s%s" % (name, gr, (", ground level %s m AOD" % gl) if gl else "")), st["cellb"]))
        rows = [["From (m)", "To (m)", "Description"]] + [list(x) for x in layers]
        flow.append(grid(rows, [18 * mm, 18 * mm, 130 * mm], st, right_from=9))
        flow.append(Paragraph(esc(note), st["small"]))
        flow.append(Spacer(1, 4))
    doc.build(flow, onFirstPage=_footer("Geological records extract", "Carlito"),
              onLaterPages=_footer("Geological records extract", "Carlito"))


# ------------------------------------------------------------------------------------------------- the returns
def returns_table(O):
    """Each licence year's monthly volumes as the returns gave them: the plant meter's readings (FM-1)."""
    am = W.abstraction_monthly(O)
    years = {}
    for (y, m), (true_q, fm1_q) in sorted(am.items()):
        ly = y if m >= 4 else y - 1
        if ly > 2025:
            continue
        vol = int(round(fm1_q * W.month_days(y, m)))
        years.setdefault(ly, []).append(((y, m), vol))
    return years


# who signed each licence year's return, and the day in April it went
RETURN_SIGNED = {ly: ("%s, operations manager" % K.PEOPLE["previous"], day)
                 for ly, day in ((2015, 19), (2016, 25), (2017, 12), (2018, 26))}
RETURN_SIGNED.update({2019: (K.PEOPLE["lead"], 21), 2020: (K.PEOPLE["lead"], 14),
                      2021: ("%s for %s" % (K.PEOPLE["site"], K.PEOPLE["lead"]), 27), 2022: (K.PEOPLE["lead"], 20),
                      2023: (K.PEOPLE["lead"], 24), 2024: (K.PEOPLE["lead"], 17), 2025: (K.PEOPLE["lead"], 22)})


def write_returns(out, O):
    st = styles("LibSans", "LibSans-Bold", REG, 9.2)
    path = os.path.join(out, F_RETURNS)
    doc = _doc(path, "Abstraction returns MA/28/15/0042", K.COMPANY)
    flow = []
    serials = {2015: "EM-15-4471", 2019: "EM-15-4471", 2025: "EM-25-0937"}
    for ly, months in sorted(returns_table(O).items()):
        flow.append(Paragraph("Return of water abstracted. Licence MA/28/15/0042", st["h1"]))
        flow.append(Paragraph(esc("Licence holder: %s. Year 1 April %d to 31 March %d." % (K.COMPANY, ly, ly + 1)),
                              st["sub"]))
        rows = [["Month", "Volume abstracted (m3)"]]
        for (y, m), v in months:
            rows.append([dt.date(y, m, 1).strftime("%B %Y"), "{:,}".format(v)])
        rows.append(["Total for the year", "{:,}".format(sum(v for _, v in months))])
        flow.append(grid(rows, [60 * mm, 50 * mm], st, right_from=1, bold_rows=(len(rows) - 1,)))
        meter = "EM-15-4471" if ly < 2025 else "EM-15-4471 to 14 October 2025, EM-25-0937 from that date"
        flow.append(Spacer(1, 6))
        who, day = RETURN_SIGNED[ly]
        flow.append(Paragraph(esc("Meter: %s, read weekly. Signed %s, %s." % (meter, who,
                                                                                    K.long_date(dt.date(ly + 1, 4, day)))),
                              st["body"]))
        flow.append(PageBreak())
    doc.build(flow[:-1], onFirstPage=_footer(K.COMPANY, "LibSans"), onLaterPages=_footer(K.COMPANY, "LibSans"))


# ------------------------------------------------------------------------------------------------- the brief
BRIEF = [
    ("h", "Line 5: project brief"),
    ("p", "Line 5 is a second returnable-glass line for the hospitality trade, a copy of line 3 in format and "
          "filler, planned to start in May 2027 on the two-shift pattern. Its supply comes off the plant's treated "
          "water ring main like the other lines'."),
    ("h", "Water"),
    ("p", "The site's peak day is close to the licensed 1,200 cubic metres. With line 5 running, the plant's peak "
          "day rises to about 1,800 cubic metres, which is the daily quantity the licence variation needs."),
    ("p", "Line 5's water is sized on line 3's: the litres through line 3's meter in a month, cleans included, per "
          "litre it packed (good bottles times the bottle's size)."),
    ("p", "The bulk supply to %s began in April 2026 on a two-year contract, about forty tanker loads a month "
          "from the bulk bay." % K.BULK_CUSTOMER),
    ("h", "Programme"),
    ("p", "Board approval of the capital in December 2026, subject to the licence. Filler order January 2027, "
          "installation March and April 2027, commissioning May 2027."),
]


def write_brief(out):
    import docx
    from docx.shared import Pt
    d = docx.Document()
    sty = d.styles["Normal"]
    sty.font.name = "Calibri"
    sty.font.size = Pt(10.5)
    for kind, text in BRIEF:
        if kind == "h":
            d.add_heading(text, level=1 if text.startswith("Line 5") else 2)
        else:
            d.add_paragraph(text)
    d.save(os.path.join(out, F_BRIEF))


def write_all(out, O):
    write_letter(out)
    write_licence(out)
    write_geology(out)
    write_returns(out, O)
    write_brief(out)
