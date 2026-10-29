"""task464 architecture 10: the four documents of the pack.

  losses_programme_2027-28_brief.pdf      the losses strategy lead's paper to the investment review panel: the eight
                                          projects, the figure each is sized on (the estimand, at authority) and the
                                          decision. It says nothing about how a section's current is found.
  hv_conductor_data_EDS-02-0310.pdf       the engineering data sheet: every HV conductor's resistance and ratings.
  iis_reporting_definitions_2025-26.pdf   the network performance team's definitions for the 2025/26 interruptions
                                          return, with the exceptional event accepted for the year.
  line_loss_factors_2025-26.pdf           the published line loss factor statement for the licence area.

No document states a section's flow or loss, ranks the projects, or says which records restore a customer.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import world as W

S = getSampleStyleSheet()
H1 = ParagraphStyle("h1", parent=S["Heading1"], fontSize=13.5, spaceAfter=4)
H2 = ParagraphStyle("h2", parent=S["Heading2"], fontSize=10.5, spaceBefore=9, spaceAfter=3)
BODY = ParagraphStyle("body", parent=S["BodyText"], fontSize=9.2, leading=12.8, spaceAfter=5)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.2, leading=10.4, spaceAfter=0)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=7.8, leading=10, textColor=colors.HexColor("#555555"))

BRIEF = "losses_programme_2027-28_brief.pdf"
CATALOGUE = "hv_conductor_data_EDS-02-0310.pdf"
IIS = "iis_reporting_definitions_2025-26.pdf"
LLF = "line_loss_factors_2025-26.pdf"


def _doc(out, name, title, author, flow):
    d = SimpleDocTemplate(os.path.join(out, name), pagesize=A4,
                          leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
                          title=title, author=author, subject="", creator="")
    d.build(flow)
    return name


def _table(data, widths, size=8.2):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), size),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
        ("LINEBELOW", (0, 1), (-1, -2), 0.2, colors.HexColor("#bbbbbb")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def project_rows(w):
    """(feeder name, breaker, [section ids], old description, new code) for each project, in breaker order."""
    out = []
    for f in w["feeders"]:
        secs = [s for s in w["sections"] if s.feeder == f["code"] and s.project]
        olds = sorted(set(W.CONDUCTORS[s.code][0] for s in secs))
        out.append((f["name"], f["breaker"], [s.id for s in secs], olds, f["new"]))
    return out


def brief(w, out):
    P = W.PEOPLE
    f = [Paragraph("Losses programme 2027/28: reconductoring at Copsewell Cross", H1),
         Paragraph("%s, network losses strategy. Paper for the investment review panel, meeting of 9 December 2026. "
                   "Prepared by %s, losses strategy lead, 18 November 2026." % (W.DNO, P["losses_lead"]), SMALL),
         Paragraph("The programme", H2),
         Paragraph("The 2027/28 losses programme funds one 11 kV reconductoring project at Copsewell Cross 33/11 kV "
                   "primary substation. The 2026 asset condition review found runs of original conductor still in "
                   "service on each of the primary's eight 11 kV feeders, and each feeder's project replaces all of "
                   "that feeder's remaining runs in one scheme. The project the losses programme funds is built in 2027/28; the "
                   "other seven stay in the condition-led programme, where they are timed on condition alone.", BODY),
         Paragraph("The panel funds the project whose replacement conductor would have removed the most losses in "
                   "the last complete regulatory year, and the paper reports the runner-up and every project's "
                   "saving beside the pick.", BODY),
         Paragraph("The projects", H2)]
    data = [["Feeder", "Breaker", "Sections replaced (network model IDs)", "Existing conductor", "Replacement"]]
    for name, brk, ids, olds, new in project_rows(w):
        data.append([name, brk, Paragraph(", ".join(ids), CELL), Paragraph("; ".join(olds), CELL),
                     Paragraph(W.CONDUCTORS[new][0], CELL)])
    f.append(_table(data, [26 * mm, 15 * mm, 50 * mm, 45 * mm, 34 * mm]))
    f += [Paragraph("How each project is sized", H2),
          Paragraph("Each project is sized on the 2025/26 regulatory year, the half-hours from 00:00 on 1 April 2025 to "
                    "24:00 on 31 March 2026, UK time. For each half-hour and each section the project replaces, the "
                    "section's I<super>2</super>R loss is worked out at the current that section carried in that "
                    "half-hour, once on its existing conductor and once on the replacement conductor; the project's "
                    "saving is the difference, summed over its sections and over the half-hours.", BODY),
          Paragraph("The current is taken as balanced across the three phases at 11 kV nominal, resistances are the "
                    "conductor data sheet's values at 20&deg;C, and nothing is added to a section's current for the "
                    "network's own losses or for voltage drop. Each project's saving is reported in MWh for the year and "
                    "valued at the 2027/28 losses value of GBP %.2f per MWh." % W.LOSSES_VALUE_GBP_MWH, BODY),
          Paragraph("Interruptions", H2),
          Paragraph("The panel also sees each feeder's 2025/26 customer interruptions per 100 customers (CI) and "
                    "customer minutes lost per customer (CML), as the network reports them for the year under the "
                    "interruptions incentive scheme and the network performance team's reporting definitions for "
                    "2025/26.", BODY),
          Paragraph("Timetable", H2)]
    data = [["Date", "Step"],
            ["12 June 2026", Paragraph("2025/26 losses and interruptions extracts taken (%s, network data lead)." % P["data_lead"], CELL)],
            ["2 December 2026", Paragraph("Panel papers issued.", CELL)],
            ["9 December 2026", Paragraph("The panel funds the 2027/28 project.", CELL)],
            ["January to June 2027", Paragraph("Design, consents and procurement (%s, network planning)." % P["planning_engineer"], CELL)],
            ["From July 2027", Paragraph("Construction; the replaced runs are recovered as the new conductor is "
                                         "commissioned.", CELL)]]
    f.append(_table(data, [36 * mm, 134 * mm]))
    f += [Spacer(1, 6), Paragraph("%s, losses strategy lead, %s" % (P["losses_lead"], W.DNO), SMALL)]
    return _doc(out, BRIEF, "Losses programme 2027/28: reconductoring at Copsewell Cross", W.DNO, f)


# conductor data sheet: code -> (cross-section text, stranding/insulation, R20, R at max temperature, X ohm/km, summer A, winter A)
EXTRA = {
    "UG-PILC-0.1CU": ("0.1 sq in", "3-core belted, Cu", 1.239, 0.083, 255, 290),
    "UG-PILC-0.15CU": ("0.15 sq in", "3-core belted, Cu", 1.242, 0.080, 315, 355),
    "UG-PILC-0.2CU": ("0.2 sq in", "3-core belted, Cu", 1.244, 0.078, 365, 410),
    "UG-PILC-0.3CU": ("0.3 sq in", "3-core belted, Cu", 1.250, 0.076, 445, 500),
    "UG-XLPE-95AL": ("95 mm2", "triplex, Al", 1.282, 0.104, 230, 260),
    "UG-XLPE-185AL": ("185 mm2", "triplex, Al", 1.284, 0.094, 335, 375),
    "UG-XLPE-300AL": ("300 mm2", "triplex, Al", 1.288, 0.088, 430, 480),
    "OH-CU-0.04": ("0.04 sq in", "7/0.083 in hard-drawn Cu", 1.20, 0.383, 160, 185),
    "OH-CU-0.1": ("0.1 sq in", "7/0.136 in hard-drawn Cu", 1.20, 0.352, 300, 340),
    "OH-ACSR-50": ("50 mm2 (Rabbit)", "6/1/3.35 mm ACSR", 1.21, 0.370, 185, 210),
    "OH-ACSR-100": ("100 mm2 (Dog)", "6/4.72 + 7/1.57 mm ACSR", 1.21, 0.349, 300, 340),
    "OH-AAAC-100": ("100 mm2 (Oak)", "7/4.65 mm AAAC", 1.22, 0.344, 290, 330),
    "OH-AAAC-150": ("150 mm2 (Ash)", "19/3.48 mm AAAC", 1.22, 0.332, 375, 425),
    "OH-AAAC-200": ("200 mm2 (Elm)", "19/3.76 mm AAAC", 1.22, 0.325, 445, 505),
}


def catalogue(out):
    f = [Paragraph("Engineering data sheet EDS 02-0310: 11 kV conductor electrical data", H1),
         Paragraph("%s, asset policy. Issue 7, 3 September 2024. Supersedes issue 6 (2019); issue 7 adds the 300 mm2 "
                   "triplex cable and corrects the 0.04 sq in reactance." % W.DNO, SMALL),
         Paragraph("Scope", H2),
         Paragraph("Electrical data for the 11 kV overhead line conductors and three-core cables in service on the "
                   "network, including types no longer installed. The asset code is the code the network model and the "
                   "asset register carry. Resistances are per phase per kilometre of route; overhead line reactances "
                   "are at the standard 11 kV flat spacing. Ratings are distribution ratings for planning and are not "
                   "used for protection settings.", BODY),
         Paragraph("Conductors", H2)]
    data = [["Asset code", "Conductor", "Construction", "R at 20°C\n(ohm/km)", "R at max. temp.\n(ohm/km)",
             "X\n(ohm/km)", "Rating summer /\nwinter (A)"]]
    order = ["UG-PILC-0.1CU", "UG-PILC-0.15CU", "UG-PILC-0.2CU", "UG-PILC-0.3CU", "UG-XLPE-95AL", "UG-XLPE-185AL",
             "UG-XLPE-300AL", "OH-CU-0.04", "OH-CU-0.1", "OH-ACSR-50", "OH-ACSR-100", "OH-AAAC-100", "OH-AAAC-150",
             "OH-AAAC-200"]
    for code in order:
        desc, kind, r20, _ = W.CONDUCTORS[code][0], W.CONDUCTORS[code][1], W.CONDUCTORS[code][2], W.CONDUCTORS[code][3]
        cs, cons, kmax, x, sa, wa = EXTRA[code]
        rmax = r20 * kmax
        data.append([W.MODEL_CODE[code], Paragraph(desc, CELL), Paragraph(("Cable, " if kind == "UG" else "Overhead, ") + cons, CELL),
                     "%.4f" % r20 if r20 < 0.1 else "%.3f" % r20, "%.3f" % rmax, "%.3f" % x, "%d / %d" % (sa, wa)])
    f.append(_table(data, [27 * mm, 38 * mm, 37 * mm, 19 * mm, 21 * mm, 13 * mm, 20 * mm], size=7.8))
    f += [Paragraph("Notes", H2),
          Paragraph("Maximum conductor temperature is 65°C for paper-insulated cable, 90°C for XLPE and 75°C "
                    "for overhead conductors at the 2 km/h wind speed of the ratings. Imperial sizes are the original "
                    "manufacturers' nominal areas; they are not converted.", BODY),
          Paragraph("Asset policy, %s. Queries to the asset policy mailbox." % W.DNO, SMALL)]
    return _doc(out, CATALOGUE, "EDS 02-0310 11 kV conductor electrical data", W.DNO, f)


def iis(out, storm_circuits):
    f = [Paragraph("Interruptions reporting: definitions for the 2025/26 regulatory return", H1),
         Paragraph("%s, network performance. Issue 2, 14 May 2026. Issue 2 adds the accepted exceptional event." % W.DNO, SMALL),
         Paragraph("Scope", H2),
         Paragraph("These definitions govern the customer interruptions (CI) and customer minutes lost (CML) the network "
                   "reports for each 11 kV circuit and in total for the regulatory year 1 April 2025 to 31 March 2026. An "
                   "interruption belongs to the regulatory year in which it begins (UK time).", BODY),
         Paragraph("Interruptions and customers", H2),
         Paragraph("An interruption is a loss of supply to one or more customers lasting 3 minutes or longer. A loss of "
                   "supply shorter than 3 minutes is a short interruption; short interruptions are reported separately "
                   "and count in neither CI nor CML. A customer is a connection on the circuit with a registered "
                   "metering point, each LV customer and each HV-connected customer counting as one.", BODY),
         Paragraph("CI per 100 customers is the number of times customers on the circuit lost supply in interruptions "
                   "in the year, multiplied by 100 and divided by the customers connected to the circuit at 31 March "
                   "2026. CML per customer is the minutes from each such loss of supply to the restoration of that "
                   "customer's supply, summed over every customer interrupted, divided by the same customer count. "
                   "Where customers are restored in stages, each customer's minutes run to their own restoration.", BODY),
         Paragraph("Pre-arranged interruptions, given with notice for planned work, count at half weight in both CI and "
                   "CML. Unplanned interruptions count in full.", BODY),
         Paragraph("Exclusions", H2),
         Paragraph("Interruptions originating on the transmission system or at the grid supply point are excluded, as "
                   "are interruptions arising in an exceptional event accepted by the regulator, on the circuits the "
                   "acceptance names and for the period it covers.", BODY),
         Paragraph("Exceptional event accepted for 2025/26", H2)]
    data = [["Event", "Period (UK time)", "Circuits", "Accepted"],
            ["Storm (severe weather, wind)", "15:00 on 6 January 2026 to 23:59 on 7 January 2026",
             Paragraph(", ".join(storm_circuits), CELL), "28 April 2026"]]
    f.append(_table(data, [38 * mm, 46 * mm, 58 * mm, 26 * mm]))
    f += [Spacer(1, 6),
          Paragraph("Network performance, %s. These definitions are applied to the interruption log as extracted for the "
                    "return." % W.DNO, SMALL)]
    return _doc(out, IIS, "Interruptions reporting: definitions for the 2025/26 regulatory return", W.DNO, f)


def llf(out):
    f = [Paragraph("Line loss factors 2025/26", H1),
         Paragraph("%s. Statement of line loss factors for the regulatory year 1 April 2025 to 31 March 2026, as "
                   "published for settlement, 28 February 2025." % W.DNO, SMALL),
         Paragraph("Use of this statement", H2),
         Paragraph("Line loss factors scale metered consumption and generation to the grid supply point for settlement. "
                   "They are averages for each class of connection over the licence area and time band, set before the "
                   "year from the previous years' measured losses; they do not describe any individual circuit.", BODY),
         Paragraph("Factors", H2)]
    bands = ["Night (00:00-07:00)", "Weekday day (07:00-16:00, 19:00-24:00)", "Weekday peak (16:00-19:00)", "Weekend day"]
    rows = [("LV network", [1.071, 1.086, 1.104, 1.079]), ("LV substation", [1.052, 1.060, 1.071, 1.056]),
            ("HV network", [1.031, 1.037, 1.046, 1.034]), ("HV substation", [1.012, 1.015, 1.019, 1.013]),
            ("33 kV generation (export)", [0.991, 0.988, 0.985, 0.990]), ("HV generation (export)", [0.982, 0.977, 0.971, 0.980])]
    data = [["Class"] + bands]
    for name, v in rows:
        data.append([name] + ["%.3f" % x for x in v])
    f.append(_table(data, [44 * mm, 30 * mm, 38 * mm, 30 * mm, 28 * mm], size=7.8))
    f += [Spacer(1, 6),
          Paragraph("Published for the settlement year under the distribution connection and use of system agreement. "
                    "Factors for extra high voltage sites are calculated site by site and are not listed.", SMALL)]
    return _doc(out, LLF, "Line loss factors 2025/26", W.DNO, f)


def main(w, out, storm_circuits):
    return [brief(w, out), catalogue(out), iis(out, storm_circuits), llf(out)]
