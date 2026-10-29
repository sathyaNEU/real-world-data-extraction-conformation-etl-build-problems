"""task273 architecture 5: the pack's documents. The Department's minimum-load framework (the assessment's
standard), Tallowbark Networks' notice of its new controlled-load switching times, and its summer demand outlook."""
from __future__ import annotations

import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import cm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import numpy as np   # noqa: E402

import params as P   # noqa: E402

FONT_DIR = next((d for d in ("/usr/share/fonts/truetype/liberation/", os.path.expanduser("~/Library/Fonts/"),
                              "/Library/Fonts/") if os.path.exists(d + "LiberationSerif-Regular.ttf")),
                "/usr/share/fonts/truetype/liberation/")
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1c2330"), colors.HexColor("#5a6470"), colors.HexColor("#bcc4cc")
DEPT_BLUE = colors.HexColor("#1f4e79")
NET_GREEN = colors.HexColor("#2e5e3e")


def styles(face, accent):
    b = face + "-B"
    body = ParagraphStyle("b", fontName=face, fontSize=10.0, leading=13.6, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=b, fontSize=15, leading=19, textColor=accent, spaceAfter=3),
        h2=ParagraphStyle("h2", fontName=b, fontSize=10.8, leading=14, textColor=INK, spaceBefore=9, spaceAfter=3,
                          keepWithNext=1),
        meta=ParagraphStyle("m", fontName=face, fontSize=8.6, leading=11.4, textColor=GREY, spaceAfter=10),
        cell=ParagraphStyle("c", fontName="Sans", fontSize=8.2, leading=10.2, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="Sans-B", fontSize=8.2, leading=10.2, textColor=INK),
        note=ParagraphStyle("n", fontName="Sans", fontSize=7.8, leading=10.0, textColor=GREY, spaceBefore=2,
                            spaceAfter=6),
        clause=ParagraphStyle("p", parent=body, leftIndent=30, firstLineIndent=-30))


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.6)
        canvas.drawString(2.2 * cm, A4[1] - 1.35 * cm, left)
        canvas.drawRightString(A4[0] - 2.2 * cm, A4[1] - 1.35 * cm, right)
        canvas.drawRightString(A4[0] - 2.2 * cm, 1.2 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.8),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2.1 * cm,
                             bottomMargin=1.9 * cm, title=title, author=author, subject=subject,
                             creator="Microsoft Word for Microsoft 365", producer="Microsoft Word for Microsoft 365")


# ---------------------------------------------------------------------------------------------- the framework
def write_framework(path, thresholds):
    S = styles("Serif", DEPT_BLUE)
    doc = _doc(path, "Minimum-load framework for distribution zone substations", P.DEPT, "Version 2")
    fr = _frame(P.DEPT + ", Energy Security Division", "Minimum-load framework, version 2 (3 March 2026)")
    s = []
    s.append(Paragraph("Minimum-load framework for distribution zone substations", S["h1"]))
    s.append(Paragraph("Version 2. Approved by the Deputy Secretary, Energy, on 3 March 2026; replaces version 1 "
                       "(February 2025). Owner: Director, Energy Security. Next review: March 2027.", S["meta"]))
    s.append(Paragraph("1. Purpose", S["h2"]))
    s.append(Paragraph(
        "Rooftop solar on the %s now exceeds daytime load across much of the distribution network on clear spring "
        "days, and the power flows back into the subtransmission network through the zone substations. Below a "
        "certain level a zone substation's protection and voltage control are no longer secure. Each year the "
        "Department assesses the coming spring and the Minister designates the zone substations at risk, so that "
        "the network has emergency backstop arrangements in place for them before 1 September." % P.REGION, S["body"]))
    s.append(Paragraph("2. Designation", S["h2"]))
    s.append(_clause(S, "2.1", "A zone substation is designated for a spring when its forecast demand on that "
                     "spring's reference day falls below its minimum-load threshold (section 4) in any of the ten "
                     "half-hours from 10.00 am to 3.00 pm local time."))
    s.append(_clause(S, "2.2", "The reference day for an assessment is the Sunday of the preceding spring (1 September "
                     "to 30 November) on which the total demand of the network's zone substations was lowest in a "
                     "half-hour between 10.00 am and 3.00 pm local time."))
    s.append(_clause(S, "2.3", "Demand is the net flow of active power into a zone substation from the subtransmission "
                     "network, in megawatts; a flow back into the subtransmission network is negative demand."))
    s.append(Paragraph("3. The forecast", S["h2"]))
    s.append(_clause(S, "3.1", "A zone substation's forecast demand for each half-hour of the coming spring's "
                     "reference day is its demand in the same half-hour of the reference day, with two changes and no "
                     "others: (a) the rooftop solar the network forecasts will be connected behind it after the "
                     "reference day and by 1 October of the assessment year is subtracted, at the reference day's "
                     "output per kW of inverter capacity for that half-hour in the Department's monitored sample; and "
                     "(b) load the network has notified will be switched at different times from 1 September of the "
                     "assessment year is placed in the half-hours in which it will draw."))
    s.append(_clause(S, "3.2", "A storage water heater on a controlled-load circuit draws its element rating from the "
                     "time its circuit is switched on until it has taken its daily energy. A heater's daily energy is "
                     "the controlled-load consumption recorded for it over the preceding spring's meter reads divided "
                     "by the number of days those reads cover."))
    s.append(_clause(S, "3.3", "Customer numbers, other load and the solar connected at the reference day are taken "
                     "as they were on the reference day."))
    s.append(Paragraph("4. Minimum-load thresholds", S["h2"]))
    s.append(Paragraph(
        "The threshold is the lowest demand at which the zone substation's transformer protection and voltage "
        "regulation remain secure, set with the network from its reverse-power settings and tap range. The "
        "thresholds below were reviewed with %s in February 2026." % P.NETWORK, S["body"]))
    rows = [["Code", "Zone substation", "Threshold (MW)", "Limiting element"]]
    basis = ["Transformer reverse-power protection", "Voltage regulation at minimum tap",
             "Subtransmission line protection setting"]
    r = np.random.default_rng(7351)
    for c, nm in sorted(((c, n) for c, n, *_ in P.SUBS), key=lambda x: x[1]):
        rows.append([c, nm, "%.1f" % thresholds[c], basis[int(r.choice(3, p=[0.55, 0.27, 0.18]))]])
    s.append(_table(S, rows, [1.6, 4.2, 3.0, 7.2], right=(2,)))
    s.append(Paragraph("5. Emergency backstop", S["h2"]))
    s.append(_clause(S, "5.1", "For a designated zone substation the network prepares arrangements to curtail rooftop "
                     "solar behind it remotely in a minimum-load event, and tests them before 1 September."))
    s.append(_clause(S, "5.2", "Under the State's emergency backstop requirement, a rooftop solar inverter installed on "
                     "or after 1 July 2025 accepts the network's remote curtailment; an inverter installed before that "
                     "date does not."))
    s.append(Paragraph("6. Timetable", S["h2"]))
    s.append(Paragraph(
        "By 31 January the network gives the Department its forecast of rooftop solar connections and notice of any "
        "change to the times at which it switches load. The Department reports its assessment to the Minister by 31 "
        "March, and the Minister's designations are published by 30 April.", S["body"]))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Contact: %s, %s." % (P.PEOPLE["director"], P.ROLES["director"]), S["note"]))
    doc.build(s, onFirstPage=fr, onLaterPages=fr)


# ---------------------------------------------------------------------------------------------- the network notice
def write_notice(path):
    S = styles("Sans", NET_GREEN)
    doc = _doc(path, "New load-control signal times from 1 September 2027", P.NETWORK,
               "Network notice NN-2027-02")
    fr = _frame(P.NETWORK, "Network notice NN-2027-02, issued 19 January 2027")
    s = []
    s.append(Paragraph("New load-control signal times from 1 September 2027", S["h1"]))
    s.append(Paragraph("Network notice NN-2027-02. Issued 19 January 2027 to retailers with customers on Tallowbark "
                       "controlled-load tariffs, and to the %s." % P.DEPT, S["meta"]))
    s.append(Paragraph("What is changing", S["h2"]))
    s.append(Paragraph(
        "From 1 September 2027 %s will move the switching signals its audio-frequency load-control system sends "
        "from the night into the middle of the day, when rooftop solar output across the %s is highest. From that "
        "date the system will send the switch-on signal to each load-control group at the time below and the "
        "switch-off signal to every group at 4.00 pm. It will no longer send the overnight signals (switch-on from "
        "10.00 pm, switch-off at 7.00 am)." % (P.NETWORK, P.REGION), S["body"]))
    rows = [["Load-control group", "Switch-on signal from 1 September 2027", "Switch-off signal"]]
    for g, t in enumerate(("10.00 am", "10.30 am", "11.00 am", "11.30 am", "12.00 noon")):
        rows.append(["Group %d" % (g + 1), t, "4.00 pm"])
    s.append(_table(S, rows, [4.0, 6.6, 4.4]))
    s.append(Paragraph("Times are local time. Daylight saving time applies from the first Sunday in October.",
                       S["note"]))
    s.append(Paragraph("Why", S["h2"]))
    s.append(Paragraph(
        "Demand at several zone substations already falls below zero in the middle of clear spring days. Heating "
        "water while the sun is up uses energy that would otherwise flow back into the subtransmission network, and "
        "it lets more customers connect rooftop solar without export limits.", S["body"]))
    s.append(Paragraph("Tariffs and customers", S["h2"]))
    s.append(Paragraph(
        "Controlled-load network tariffs and their prices do not change. A customer's load-control group is "
        "recorded in Tallowbark's load-control register; retailers can request a customer's group through the "
        "usual service order process. Customers who would like a boost element switched outside these times should "
        "contact their retailer.", S["body"]))
    s.append(Spacer(1, 8))
    s.append(Paragraph("%s, %s, %s." % (P.PEOPLE["ops"], P.ROLES["ops"], P.NETWORK), S["note"]))
    doc.build(s, onFirstPage=fr, onLaterPages=fr)


# ---------------------------------------------------------------------------------------------- distractor
def write_summer(path, w):
    S = styles("Sans", NET_GREEN)
    doc = _doc(path, "Summer 2027-28 zone substation demand outlook", P.NETWORK, "Planning report PR-26-14")
    fr = _frame(P.NETWORK + ", Network Planning", "Summer 2027-28 demand outlook, 6 November 2026")
    r = np.random.default_rng(w.seed + 1601)
    s = []
    s.append(Paragraph("Summer 2027-28 zone substation demand outlook", S["h1"]))
    s.append(Paragraph("Planning report PR-26-14, 6 November 2026. Network Planning, %s." % P.NETWORK, S["meta"]))
    s.append(Paragraph(
        "This outlook sets out the maximum demand each zone substation is forecast to reach in summer 2027-28 at "
        "50 per cent and 10 per cent probability of exceedance, against its firm rating (the rating with the largest "
        "transformer out of service). It informs the 2027 augmentation programme and the summer contingency plans. "
        "Maximum demand on the %s falls on hot weekday evenings, after rooftop solar has dropped away, and is driven "
        "by air conditioning." % P.REGION, S["body"]))
    rows = [["Code", "Zone substation", "Firm rating (MVA)", "2025-26 actual (MW)", "2027-28 POE50 (MW)",
             "2027-28 POE10 (MW)"]]
    for c, nm in sorted(((c, n) for c, n, *_ in P.SUBS), key=lambda x: x[1]):
        sb = w.sub[c]
        peak = sb["n"] * float(r.uniform(2.05, 2.6)) / 1000.0
        firm = round(peak * float(r.uniform(1.05, 1.42)) / 5) * 5
        p50 = peak * float(r.uniform(1.01, 1.05))
        p10 = p50 * float(r.uniform(1.08, 1.14))
        rows.append([c, nm, "%d" % firm, "%.1f" % peak, "%.1f" % p50, "%.1f" % p10])
    s.append(_table(S, rows, [1.4, 3.4, 2.6, 2.9, 2.9, 2.9], right=(2, 3, 4, 5)))
    s.append(Paragraph("Actual demand is the highest half-hour of summer 2025-26 from the zone substation's SCADA, "
                       "corrected for abnormal switching.", S["note"]))
    s.append(Paragraph("Zone substations above firm rating at POE10", S["h2"]))
    s.append(Paragraph(
        "Where the POE10 forecast exceeds firm rating the network relies on load transfers to neighbouring zone "
        "substations and on its demand response contracts. No zone substation is forecast above its full (N) "
        "rating.", S["body"]))
    doc.build(s, onFirstPage=fr, onLaterPages=fr)
