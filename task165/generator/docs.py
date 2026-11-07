"""task165 architecture 2: the pack's documents. The consent decree's Appendix C (the authority's conformed copy),
Ostrem Calder's TM-7 and section 4 of the Northside tank's O&M manual, each written as a Word document and exported
to PDF by LibreOffice Writer (officepdf), with the issuing office as author and the document's own dates."""
import datetime as dt

import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle

import officepdf as O
import params as P
import world as W

reportlab.rl_config.invariant = 1
ET_STD = dt.timezone(dt.timedelta(hours=-5))
ET_DST = dt.timezone(dt.timedelta(hours=-4))
SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["Normal"], fontName="Helvetica", fontSize=9.6, leading=12.8, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10.6, leading=13.5,
                    spaceBefore=6, spaceAfter=3)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8.0, leading=10.2, textColor=colors.HexColor("#444444"))
CELL = ParagraphStyle("c", parent=BODY, fontSize=8.4, leading=10.4, spaceAfter=0)
CELLB = ParagraphStyle("cb", parent=CELL, fontName="Helvetica-Bold")
AUTH = "Quessling Sewer Authority"


def _esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _table(rows, widths):
    data = [[Paragraph(_esc(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#333333")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def appendix_c(path):
    s = [Paragraph("Appendix C: Combined Sewer Overflow Control Performance", H1),
         Paragraph("Consent Decree, United States and Commonwealth of Pennsylvania v. Quessling Sewer Authority. "
                   "Conformed copy incorporating the 2021 modification; the Authority's file copy.", SMALL),
         Spacer(1, 4),
         Paragraph("1. The system", H2),
         Paragraph("1.1 The Authority owns and operates the combined sewer system serving the City of Quessling, the "
                   "Southside Water Reclamation Plant and the Northside Water Reclamation Plant, and the fourteen "
                   "combined sewer outfalls listed in Table C-1, each of which discharges to the Wennick River.", BODY),
         Paragraph("1.2 The Northside Water Reclamation Plant is rated at 45 MGD average daily flow and 125 MGD peak "
                   "hydraulic capacity. The Northside storage tank at Outfall 006 (8.0 million gallons) was placed in "
                   "service on 1 May 2020 under Phase 1 of this Decree.", BODY),
         Paragraph("1.3 The Southside Water Reclamation Plant is rated at 78 MGD average daily flow and 140 MGD peak "
                   "hydraulic capacity at the headworks.", BODY),
         Paragraph("2. Performance criterion", H2),
         Paragraph("2.1 The criterion in 2.4 applies to each combined sewer outfall in Table C-1 and to the discharges "
                   "from that outfall to the Wennick River.", BODY),
         Paragraph("2.2 An untreated overflow event is any discharge from a combined sewer outfall to the receiving "
                   "water. Discharges from the same outfall that are separated by less than 24 hours without discharge "
                   "are a single event.", BODY),
         Paragraph("2.3 The average year is the period of record of the Authority's outfall flow monitoring from 1 "
                   "January 2014 through 31 December 2025, Eastern time. The number of untreated overflow events in an "
                   "average year is the number of events in that period divided by twelve. The performance of a "
                   "control measure not yet constructed is determined against the same period of record.", BODY),
         Paragraph("2.4 Each outfall shall have no more than four untreated overflow events in an average year once "
                   "its control measures are in service.", BODY),
         Paragraph("3. Remaining control measure: Outfall 014 (Clay Street)", H2),
         Paragraph("3.1 The Authority shall select a storage control measure for Outfall 014 from the alternatives "
                   "evaluated in its facilities planning, issue the design task order by 1 March 2026, submit the "
                   "Facility Plan for Outfall 014 to EPA and the Department by 30 June 2026, and place the control "
                   "measure in service by 31 December 2029.", BODY),
         Paragraph("4. Annual report", H2),
         Paragraph("4.1 The Authority's annual report for each calendar year shall include the rainfall recorded at "
                   "each of the Authority's rain gauges in each calendar month, in inches, months taken in Eastern "
                   "time; the volume each storage facility returned to the interceptor in the year, in million "
                   "gallons; and the untreated overflow events at each outfall.", BODY),
         Spacer(1, 4),
         Paragraph("Table C-1. Combined sewer outfalls", H2),
         _table([["Outfall", "Location", "Regulator", "Tributary plant"]] +
                [[o, loc, r, pl] for o, loc, r, pl in OUTFALLS], [22, 62, 24, 50])]
    O.build(path, s, "Appendix C: Combined Sewer Overflow Control Performance", AUTH,
            "Consent decree Appendix C, CSO control performance, conformed copy (2021 modification)",
            "Consent Decree, Appendix C (conformed copy)",
            dt.datetime(2021, 9, 27, 15, 12, tzinfo=ET_DST), dt.datetime(2021, 9, 27, 15, 40, tzinfo=ET_DST))


OUTFALLS = [("001", "Front Street at Mill Race", "R-01", "Northside WRP"),
            ("002", "Cannery Lane", "R-02", "Northside WRP"),
            ("003", "Bridge Street east abutment", "R-03", "Northside WRP"),
            ("004", "Water Street", "R-04", "Northside WRP"),
            ("005", "Locust Avenue", "R-05", "Northside WRP"),
            ("006", "Northside tank, Pike Street", "R-06", "Northside WRP"),
            ("007", "Tanner Street", "R-07", "Northside WRP"),
            ("008", "Market Street", "R-08", "Southside WRP"),
            ("009", "Ferry Street", "R-09A, R-09B", "Southside WRP"),
            ("010", "Orchard Avenue", "R-10", "Southside WRP"),
            ("011", "Depot Street", "R-11", "Southside WRP"),
            ("012", "Riverside Park", "R-12", "Southside WRP"),
            ("013", "Wennick Avenue", "R-13", "Southside WRP"),
            ("014", "Clay Street", "R-14", "Southside WRP")]


def tm7(path):
    rows = [["Alternative", "Storage (MG)", "Dewatering pump station, firm capacity (MGD)", "Site",
             "Estimated capital cost (USD million, 2025)"]]
    sites = {"A": "Clay Street lot, single cell", "B": "Clay Street lot, two cells",
             "C": "Clay Street lot and former rail yard, two cells", "D": "Former rail yard, three cells"}
    for lab, v, p, c in P.ALTERNATIVES:
        rows.append([lab, "%.0f" % v, "%.0f" % p, sites[lab], "%.1f" % c])
    s = [Paragraph("Technical Memorandum 7: Clay Street Storage Alternatives", H1),
         Paragraph("Quessling Sewer Authority, Outfall 014 Facility Planning. Prepared by Ostrem Calder Engineers "
                   "(Jesus Thompson, P.E., project engineer). Final, 18 December 2025.", SMALL),
         Spacer(1, 4),
         Paragraph("1. Purpose", H2),
         Paragraph("This memorandum sets out the storage alternatives for Outfall 014 at Clay Street that the Authority "
                   "will choose among for the design task order required by Appendix C, Section 3 of the Consent "
                   "Decree. It describes each alternative's storage, dewatering and site; it does not select one.", BODY),
         Paragraph("2. Background", H2),
         Paragraph("Outfall 014 drains about 1,900 acres of combined sewershed in the Clay Street, Orchard Hill and "
                   "lower Midtown neighborhoods. Regulator R-14 at Clay Street diverts dry weather flow and the first "
                   "of the wet weather flow to the Southside Interceptor, which carries it to the Southside Water "
                   "Reclamation Plant; flow above the regulator's diversion discharges through Outfall 014 to the "
                   "Wennick River. The outfall's overflow pipe has carried a flow meter since January 2014; the "
                   "original area-velocity meter was replaced in June 2019. The Southside plant's influent record "
                   "for the same period was provided from the plant historian by Tammy Williams, Superintendent, "
                   "Southside WRP, for the baseline flows chapter of the Facility Plan.", BODY),
         Paragraph("3. Alternatives", H2),
         Paragraph("3.1 Four covered concrete storage tanks are carried forward from the screening in TM-5. Each is "
                   "fed from a new diversion chamber on the Outfall 014 overflow pipe downstream of R-14, so that every "
                   "flow that would have discharged through the outfall enters the tank until the tank is full; flow "
                   "arriving at a full tank discharges through the outfall as today.", BODY),
         _table(rows, [22, 22, 40, 52, 34]),
         Spacer(1, 4),
         Paragraph("3.2 Each tank holds its contents until the overflow to it has stopped. Its dewatering pump station "
                   "then returns the stored flow through a new force main to the Southside Interceptor at manhole SI-1, "
                   "at the Southside WRP headworks, where it is treated with the plant's influent.", BODY),
         Paragraph("3.3 Each pump station's firm capacity, with its largest pump out of service, is sized to return a "
                   "full tank in about 20 hours.", BODY),
         Paragraph("4. Selection", H2),
         Paragraph("The Authority will carry forward to design the least-cost alternative that meets the Appendix C "
                   "criterion at Outfall 014. Costs are planning-level estimates (AACE Class 4) in 2025 dollars and "
                   "include the diversion chamber, force main and site work.", BODY),
         Paragraph("5. Next steps", H2),
         Paragraph("Following the Authority's selection, Ostrem Calder will prepare the design task order scope and "
                   "the Facility Plan chapters for the selected alternative.", BODY)]
    O.build(path, s, "TM-7 Clay Street Storage Alternatives", "Ostrem Calder Engineers",
            "Outfall 014 facility planning, technical memorandum 7: Clay Street storage alternatives",
            "Ostrem Calder Engineers  |  Quessling Sewer Authority Outfall 014 Facility Planning  |  TM-7 Final",
            dt.datetime(2025, 12, 18, 10, 5, tzinfo=ET_STD), dt.datetime(2025, 12, 18, 16, 48, tzinfo=ET_STD))


def om_section4(path):
    rows = [["Level (ft)", "Volume (MG)"]]
    h = 0.0
    while h <= P.NT_CREST_FT + 1e-9:
        rows.append(["%.2f" % h, "%.4f" % W.nt_volume_of_depth(h)])
        h = round(h + (0.1 if h < P.NT_HOPPER_FT - 1e-9 else 1.0), 2)
    s = [Paragraph("Section 4. Northside Storage Tank and Dewatering Pump Station", H1),
         Paragraph("Operation and Maintenance Manual, Northside Storage Tank (Outfall 006). Quessling Sewer Authority, "
                   "Operations. Issued at commissioning, April 2020.", SMALL),
         Spacer(1, 4),
         Paragraph("4.1 Tank", H2),
         Paragraph("The tank is a covered cast-in-place concrete tank of 8.0 million gallons at the overflow crest, "
                   "22.0 ft above the floor sump. The floor slopes to the sump over the lowest 3.0 ft. Levels in this "
                   "section are measured from the floor sump. Table 4-1 gives the stored volume by level.", BODY),
         Paragraph("4.2 Dewatering pump station", H2),
         Paragraph("Three submersible pumps (P-1, P-2 and P-3), each rated 4.0 MGD at the design head, discharge "
                   "through a common force main to the Northside Interceptor. The station curve tested at "
                   "commissioning: one pump 4.0 MGD, two pumps 7.4 MGD, three pumps 10.2 MGD.", BODY),
         Paragraph("4.3 Control", H2),
         Paragraph("The station is held off while storm flow enters the tank (FIT-600 at or above 1.0 MGD). Otherwise "
                   "the lead pump starts at 1.0 ft; the lag pump runs above 5.0 ft and the second lag above 12.0 ft. The "
                   "lead pump rotates each week. Pumps stop when the tank is empty.", BODY),
         Paragraph("4.4 Instrumentation", H2),
         _table([["Tag", "Instrument"],
                 ["LIT-601", "tank level transducer, ft"],
                 ["FIT-600", "tank inflow, diversion chamber, MGD"],
                 ["P-1, P-2, P-3", "pump run status"],
                 ["LSH-006", "Outfall 006 overflow detector, downstream of the tank"]], [40, 110]),
         PageBreak(),
         Paragraph("Table 4-1. Tank stage-storage", H2),
         _table(rows, [40, 40])]
    O.build(path, s, "O&M Manual Section 4, Northside Storage Tank", AUTH,
            "Northside storage tank O&M manual, section 4: tank, dewatering pump station, control and instruments",
            "Northside Storage Tank O&M Manual  |  Section 4",
            dt.datetime(2020, 4, 22, 9, 30, tzinfo=ET_DST), dt.datetime(2020, 4, 24, 14, 2, tzinfo=ET_DST))
