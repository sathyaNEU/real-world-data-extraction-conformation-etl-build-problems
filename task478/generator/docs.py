"""The pack's documents: the Freight Compliance Program 2027 (PDF), the data exports dictionary (PDF) and the 2025 toll
schedule (PDF)."""
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                     # noqa: E402
from reportlab.lib.pagesizes import letter                           # noqa: E402
from reportlab.lib.styles import ParagraphStyle                      # noqa: E402
from reportlab.lib.units import inch                                 # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P    # noqa: E402
import world as W   # noqa: E402

BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=6)
SMALL = ParagraphStyle("sm", fontName="Times-Roman", fontSize=9.5, leading=12, spaceAfter=4)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=15, leading=19, spaceAfter=4)
SUB = ParagraphStyle("s", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#444444"),
                     spaceAfter=10)
CELL = ParagraphStyle("c", fontName="Helvetica", fontSize=8.4, leading=10.2)
ORG = W.AUTHORITY
GRID = TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.6), ("FONT", (0, 1), (-1, -1), "Helvetica", 8.6),
                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                   ("TOPPADDING", (0, 0), (-1, -1), 2), ("VALIGN", (0, 0), (-1, -1), "TOP")])


def _doc(path, title):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                          topMargin=0.9 * inch, bottomMargin=0.9 * inch, title=title, author=ORG,
                          creator=ORG, producer=ORG, subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.95 * inch, 0.55 * inch, "%s  |  %s" % (ORG, title))
        c.drawRightString(letter[0] - 0.95 * inch, 0.55 * inch, "Page %d" % d_.page)
        c.restoreState()
    return d, frame


def write_program(path):
    title = W.PROGRAM
    d, frame = _doc(path, title)
    rows = [["Section", "Name", "From milepost", "To milepost"]]
    for s in W.SECTIONS:
        rows.append([s[0], s[1], "%.1f" % s[2], "%.1f" % s[3]])
    t = Table(rows, hAlign="LEFT", colWidths=[0.8 * inch, 1.5 * inch, 1.1 * inch, 1.1 * inch])
    t.setStyle(GRID)
    dr = W.PEOPLE["director"]
    s = [Paragraph(title, TITLE),
         Paragraph("%s, Office of Freight Operations. Issued 12 February 2027 by %s, Director of Freight Operations."
                   % (ORG, dr), SUB),
         Paragraph("1. Purpose", HEAD),
         Paragraph("The Authority's enforcement unit weighs trucks at its two scale houses, at the West Barrier and the "
                   "East Barrier. In 2027 the Authority lets a contract for virtual weigh stations: screening sites on "
                   "the mainline that photograph every truck, weigh it in motion and send the trucks most likely to be "
                   "overweight on to a scale house. The contract equips five of the turnpike's twelve sections, each "
                   "site at the section's weigh-in-motion station. The sections, from west to east:", BODY),
         t, Spacer(1, 4),
         Paragraph("2. The gross weight limit", HEAD),
         Paragraph("2.1 A five-axle tractor-semitrailer may not run on the turnpike with a gross vehicle weight above "
                   "80,000 lb (State Vehicle Code, section 32-4-611; the Authority's toll tariff, rule 9).", BODY),
         Paragraph("2.2 Gross vehicle weight is the weight of the whole truck as the law measures it, on a certified "
                   "static scale. The scale houses weigh each axle at rest and add the axles.", BODY),
         Paragraph("3. Where the sites go", HEAD),
         Paragraph("3.1 The five sites go to the five sections with the highest share of their five-axle "
                   "tractor-semitrailers (FHWA vehicle class 9) running over the gross weight limit.", BODY),
         Paragraph("3.2 A section's share is taken over the class 9 trucks its weigh-in-motion station weighed in "
                   "calendar 2026, in every lane and in both directions: it is the share of those trucks whose gross "
                   "vehicle weight exceeded 80,000 lb.", BODY),
         Paragraph("3.3 The sites are fixed by 1 March 2027, for the contract's notice to proceed.", BODY),
         Paragraph("4. The weigh-in-motion network", HEAD),
         Paragraph("Each section has one weigh-in-motion station, listed with its milepost in the station list. Seven "
                   "stations have quartz piezoelectric sensors and five have bending plates. Each station's controller "
                   "classifies every vehicle by the FHWA scheme from its axles and their spacings and records the "
                   "weight of each axle and the gross. The stations count and weigh traffic at highway speed for the "
                   "Authority's traffic and pavement programs; the WIM program engineer, %s, maintains them."
                   % W.PEOPLE["engineer"], BODY),
         Paragraph("5. Screening volume", HEAD),
         Paragraph("5.1 The contract prices each site on its screening volume: the average number of five-axle trucks "
                   "a weekday that entered the turnpike at the section's interchanges in 2026. A section's "
                   "interchanges are its toll plazas, the barrier plazas included.", BODY),
         Paragraph("5.2 Every entry by a five-axle truck at one of the section's toll plazas counts, a truck entering "
                   "twice counting twice. A weekday is Monday to Friday, holidays included, by the local date of the "
                   "entry: there were 261 in 2026.", BODY),
         Paragraph("6. Enforcement baseline", HEAD),
         Paragraph("6.1 The contract measures each site against the citations for gross overweight (violation code "
                   "G) the scale houses issued in 2026 to five-axle trucks that had entered the turnpike at the "
                   "section's toll plazas.", BODY),
         Paragraph("6.2 A citation counts once, in the section where the truck entered the turnpike on the trip on "
                   "which the scale house weighed it.", BODY),
         Paragraph("7. Data", HEAD),
         Paragraph("The exports and lists this program uses are described in the data exports dictionary of 9 "
                   "February 2027.", BODY),
         Spacer(1, 10),
         Paragraph("%s<br/>Director of Freight Operations, %s" % (dr, ORG), BODY)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_dictionary(path, n):
    title = "Data exports dictionary"
    d, frame = _doc(path, title)
    F = P.FILES
    piezo = [["Columns", "Field"],
             ["1-4", "station id, as the sensor vendor numbers it (the station list gives its milepost)"],
             ["5", "direction of travel, E or W"],
             ["6", "lane, as the controller numbers it"],
             ["7-14", "date, YYYYMMDD"],
             ["15-22", "time, HHMMSScc (hundredths of a second)"],
             ["23-26", "speed, tenths of a mile an hour"],
             ["27-28", "vehicle class, FHWA scheme"],
             ["29-30", "number of axles"],
             ["31-35", "gross weight, tens of pounds"],
             ["36-71", "axle weights 1 to 9, four columns each, tens of pounds (blank past the vehicle's last axle)"],
             ["72-95", "axle spacings 1 to 8, three columns each, tenths of a foot"],
             ["96", "validity: 0 valid, 1 rejected by the controller"]]
    t = Table([[Paragraph(a, CELL), Paragraph(b, CELL)] for a, b in piezo], hAlign="LEFT",
              colWidths=[0.8 * inch, 5.2 * inch])
    t.setStyle(GRID)
    items = [
        (F["bending"], n["bending"],
         "One row per vehicle weighed by the bending-plate stations, as their vendor's software writes it. site is the "
         "station id; dir is EB or WB; lane is the controller's lane number. local_time is the controller's clock. "
         "speed_kph is kilometres an hour; gvw_kg and ax1_kg to ax9_kg are kilograms; sp1_m to sp8_m are axle spacings "
         "in metres. fhwa_class is the FHWA vehicle class. status is OK, or REJ where the controller rejected the "
         "weighing."),
        (F["stations"], n["stations"],
         "The weigh-in-motion stations: station id, milepost, sensor technology, lanes weighed and in-service date. A "
         "station that has been moved carries its previous milepost and the date it moved."),
        (F["tickets"], n["tickets"],
         "One row per five-axle tractor-semitrailer weighed at a scale house in 2026: ticket number, scale house, "
         "local date and time, the truck's toll tag, trailer body, the five axle weights in pounds from the certified "
         "static scale, the gross as the scale operator keyed it, and the result."),
        (F["citations"], n["citations"],
         "The enforcement unit's citation log for 2026, one row per violation cited. citation_no: paper citations are "
         "numbered C and were keyed into the log from the officer's book; e-citations, numbered EC, were written in the "
         "log from 1 July 2026. issued and keyed are local times. ticket_no is the scale house ticket. violation is G "
         "(gross weight) or T (tandem axle weight); a truck cited for both has two rows. entry_plaza is the truck's "
         "entry plaza, looked up in the toll system."),
        (F["entries"], n["entries"],
         "Every five-axle entry to the turnpike in 2026 from the toll back office: transaction id, plaza code, entry "
         "time stamp, axle class and toll tag. The back office's current host stamps the entries it records in UTC. "
         "Exported 4 February 2027."),
        (F["plazas"], n["plazas"],
         "The toll plazas in service: code, name, milepost and, for a plaza opened since 1 January 2026, the date it "
         "came into service. Plaza codes are those the toll back office records."),
        (F["schedule"], None,
         "The toll schedule in force from 1 January 2025, with the plaza codes then in use."),
        (F["pavement"], n["pavement"],
         "The 2026 pavement condition survey by section and direction: roughness, rut depth and cracking."),
        (F["bridges"], n["bridges"],
         "Bridges on the roads crossing the turnpike near its interchanges that carry a posted weight limit."),
    ]
    s = [Paragraph("%s: data exports dictionary" % ORG, TITLE),
         Paragraph("Office of Freight Operations. Compiled 9 February 2027 by %s, WIM program engineer, for the Freight "
                   "Compliance Program 2027." % W.PEOPLE["engineer"], SUB),
         Paragraph("<b>%s</b> (%s rows)" % (F["piezo"], "{:,}".format(n["piezo"])), BODY),
         Paragraph("Fixed-width records, one per vehicle weighed by the piezoelectric stations, as their controllers "
                   "write them; times are the controller's clock.", SMALL),
         t, Spacer(1, 6)]
    for name, rows, text in items:
        s.append(Paragraph("<b>%s</b>%s" % (name, "" if rows is None else " (%s rows)" % "{:,}".format(rows)), BODY))
        s.append(Paragraph(text, SMALL))
    s.append(Paragraph("Clocks: the weigh-in-motion controllers keep Eastern Standard Time all year and take no daylight "
                       "saving time; the toll back office's current host stamps UTC; the scale houses and the citation "
                       "log keep local time (Eastern Time).", BODY))
    d.build(s, onFirstPage=frame, onLaterPages=frame)


INTERCHANGE = {"P01": "Mainline barrier (western terminus)", "P03": "Route 14", "P05": "Wendell Road",
               "P23": "Brannock Road (County Road 610)", "P07": "Route 22", "P09": "Pellam Junction (Interstate 71)",
               "P10": "Route 30", "P11": "Route 41", "P13": "Foxbriar Pike", "P14": "Route 47", "P15": "Route 52",
               "P17": "Route 58", "P19": "Route 63", "P20": "Route 9 Connector", "P25": "Route 77",
               "P27": "Route 81", "P28": "Marsh Lane", "P30": "Route 90", "P32": "Mainline barrier (eastern terminus)"}


def write_schedule(path):
    title = "Toll Schedule 2025"
    d, frame = _doc(path, title)
    rows = [["Plaza", "Name", "Milepost", "Interchange with", "Class 5 tag", "Class 5 cash"]]
    for p in W.PLAZAS:
        if p[5] is not None:            # opened in 2026
            continue
        miles = max(p[3], 0.6)
        tag = 0.392 * min(miles, 283.4 - miles) + 6.50
        rows.append([p[0], p[1], "%.1f" % p[3], INTERCHANGE[p[0]], "%.2f" % tag, "%.2f" % (tag * 1.25)])
    t = Table(rows, hAlign="LEFT", colWidths=[0.55 * inch, 1.35 * inch, 0.7 * inch, 2.25 * inch, 0.8 * inch, 0.8 * inch])
    t.setStyle(GRID)
    s = [Paragraph("Calderwick Turnpike Toll Schedule 2025", TITLE),
         Paragraph("%s. Adopted by the Board on 14 November 2024; in force from 1 January 2025." % ORG, SUB),
         Paragraph("Tolls are charged by class and by the plaza of entry to the nearer barrier. The class 5 toll "
                   "applies to five-axle vehicles. The plaza code is the code printed on the toll receipt and recorded "
                   "by the toll system.", BODY),
         t, Spacer(1, 8),
         Paragraph("Tag tolls are charged to a valid transponder account; cash and plate tolls carry the 25 per cent "
                   "surcharge of tariff rule 4.", SMALL)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)
