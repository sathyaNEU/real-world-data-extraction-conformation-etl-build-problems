"""The pack's documents: Penwick Pharmacy's Vaccine Storage and Handling Standard, the Tellvane pilot's project plan,
the Brannon service agreement and the refrigerator quotations for the 2027 program (all PDF)."""
import datetime as dt

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                     # noqa: E402
from reportlab.lib.pagesizes import letter                           # noqa: E402
from reportlab.lib.styles import ParagraphStyle                      # noqa: E402
from reportlab.lib.units import inch                                 # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import asks as A    # noqa: E402
import world as W   # noqa: E402

BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=6)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=4)
SUB = ParagraphStyle("s", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#444444"),
                     spaceAfter=10)
CELL = ParagraphStyle("c", fontName="Helvetica", fontSize=8, leading=9.6)
GRID = TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
                   ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.HexColor("#777777")),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4), ("TOPPADDING", (0, 0), (-1, -1), 2.0),
                   ("VALIGN", (0, 0), (-1, -1), "TOP")])
OPS = "Penwick Pharmacy, Pharmacy Operations"


def _doc(path, title, org):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.85 * inch,
                          bottomMargin=0.85 * inch, title=title, author=org, creator=org, producer=org, subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.9 * inch, 0.5 * inch, "%s  |  %s" % (org, title))
        c.drawRightString(letter[0] - 0.9 * inch, 0.5 * inch, "Page %d" % d_.page)
        c.restoreState()
    return d, frame


def _p(items):
    return [Paragraph(x, BODY) for x in items]


def write_standard(path):
    title = "Vaccine Storage and Handling Standard (PO-114)"
    d, frame = _doc(path, title, OPS)
    s = [Paragraph("Vaccine Storage and Handling Standard", TITLE),
         Paragraph("Penwick Pharmacy, Pharmacy Operations. Standard PO-114, revision 6, effective 1 January 2026. "
                   "Owner: %s, Director of Pharmacy Operations." % W.PEOPLE["director"], SUB),
         Paragraph("1 Scope", HEAD)]
    s += _p(["This standard applies at every Penwick Pharmacy store that stocks vaccine, including the stores that "
                "joined Penwick from Vollmer Drug and Lindqvist Apothecary. It covers the storage units, temperature "
                "monitoring, the vaccine stock records and the service of the vaccine refrigerators."])
    s += [Paragraph("2 Storage units", HEAD)]
    s += _p(["2.1 Each store keeps its refrigerated vaccine in one vaccine refrigerator. Pharmaceutical-grade units "
                "are the standard. The household-style units in service at stores that joined from other chains stay in "
                "service until they are replaced under section 7.3.",
                "2.2 The refrigerator is set to hold 5.0 degrees C, within the range 2.0 to 8.0 degrees C.",
                "2.3 Vaccine is kept in its original cartons on the center shelves, away from the walls, the floor and "
                "the cooling vents, and never in the door. The door is kept closed except to put stock away or take a "
                "dose out."])
    s += [Paragraph("3 Receiving and stock rotation", HEAD)]
    s += _p(["3.1 Meridale Pharmaceutical Distribution delivers on Tuesdays all year and, from September to November, "
                "on Fridays as well; the busiest stores receive twice a week all year. A delivery is put away in the "
                "vaccine refrigerator as soon as it is checked in.",
                "3.2 Stock is rotated so the earliest expiry is used first. Multi-dose vials are dated when first "
                "punctured and discarded 28 days after."])
    s += [Paragraph("4 Daily checks and excursions", HEAD)]
    s += _p(["4.1 At opening the pharmacist on duty checks the refrigerator's display and the device of record and "
                "initials the daily check sheet.",
                "4.2 If the device of record alarms or shows a reading outside 2.0 to 8.0 degrees C, staff check the "
                "door and the power, keep the vaccine in the refrigerator unless it cannot hold temperature, and call "
                "the Brannon service line if the unit does not recover. Vaccine that may have been affected is marked "
                "do not use until the pharmacy operations office has consulted its manufacturers."])
    s += [Paragraph("5 Power and service interruptions", HEAD)]
    s += _p(["5.1 In an outage the door stays shut. If power is not restored within four hours the store's "
                "emergency plan applies."])
    s += [Paragraph("6 Temperature monitoring", HEAD)]
    s += _p(["6.1 Every store's vaccine refrigerator has a digital data logger with a buffered probe, the probe "
                "sealed in a 5 mL bottle of glycol and placed among the vaccine on a center shelf. The loggers are the "
                "models each chain used before it joined Penwick: Frostline at the Penwick stores, Kelvra at the "
                "former Vollmer Drug stores and Brumal at the former Lindqvist Apothecary stores.",
                "6.2 Loggers are downloaded or synchronized at least monthly and their records kept for three years.",
                "6.3 Every logger is set to a ten-minute recording interval. Each record stands for the ten minutes "
                "that follow its time stamp.",
                "6.4 At a store with a Tellvane in-carton sensor, the sensor is the store's device of record from its "
                "installation; before it, the store's data logger."])
    s += [Paragraph("7 Temperature records and the refrigerator program", HEAD)]
    s += _p(["7.1 The pharmacy operations office collects every store's temperature records for a year by 15 January "
             "of the next year and keeps them for three years.",
                "7.2 The vaccine's temperature is the temperature of the vaccine itself as it sits in storage.",
                "7.3 A store whose vaccine spent a cumulative 24 hours or more above 8.0 degrees C in calendar year "
                "2026, local time at the store, has its vaccine refrigerator replaced with a new pharmaceutical-grade "
                "refrigerator, installed and qualified before 1 September 2027. The hours are counted record by "
                "record: a record counts its ten minutes when the vaccine's temperature at its time stamp was above "
                "8.0 degrees C. The capital committee approves the list in February 2027."])
    s += [Paragraph("8 Vaccine stock records", HEAD)]
    s += _p(["8.1 A store's vaccine stock records are its deliveries from Meridale, its transfers to and from other "
                "Penwick stores, the doses it administers, the doses it writes off, and the physical inventory of its "
                "vaccine, counted in doses after closing on the last day of each year.",
                "8.2 A store's doses unaccounted for in a year are the doses in its stock at the start of the year and "
                "the doses it received during the year, less the doses that left its stock during the year and the "
                "doses in its stock at the year's end."])
    s += [Paragraph("9 Refrigerator service", HEAD)]
    s += _p(["9.1 Brannon Refrigeration Service maintains every store's vaccine refrigerator under the service "
                "agreement: two preventive maintenance visits a year and service calls as needed.",
                "9.2 A store's refrigerator service spend for a year is what Brannon invoiced for work completed on the "
                "store's vaccine refrigerator in that year, sales tax included."])
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_pilot(path, roster):
    title = "Tellvane in-carton monitoring pilot, 2026: project plan"
    d, frame = _doc(path, title, OPS)
    s = [Paragraph(title, TITLE),
         Paragraph("Pharmacy Operations. Prepared by %s, pilot lead; approved by %s, Director of Pharmacy Operations, "
                   "14 April 2026." % (W.PEOPLE["pilot"], W.PEOPLE["director"]), SUB),
         Paragraph("1 Purpose", HEAD)]
    s += _p(["The pilot runs Tamberlane Sensing's Tellvane wireless monitoring at ten stores through the rest of 2026 "
                "so that the chain can decide in 2027 whether to move every store to it. Tellvane sends each reading "
                "to Tamberlane's cloud as it is taken and alerts the store and the on-call pharmacist by text and "
                "email, which the stores' data loggers cannot do between downloads."])
    s += [Paragraph("2 Stores", HEAD)]
    s += _p(["Ten stores, chosen to include each logger make, both unit types and a range of store volumes:"])
    rows = [["Store", "Town", "Data logger", "Unit", "Planned installation"]]
    for (no, inst) in roster:
        st = W.BY_NO[no]
        rows.append([str(no), st["town"], W.MAKES[st["make"]][0],
                     "Pharmaceutical-grade" if st["unit"] == "pharma" else "Household-style",
                     "Week of %s" % (inst - dt.timedelta(days=inst.weekday())).strftime("%d %B")
                     .lstrip("0")])
    t = Table(rows, colWidths=[0.6 * inch, 1.3 * inch, 1.2 * inch, 1.5 * inch, 1.6 * inch])
    t.setStyle(GRID)
    s += [t, Spacer(1, 8)]
    s += [Paragraph("3 The sensor", HEAD)]
    s += _p(["The Tellvane TV-4 is a wireless temperature sensor on a short lead. Its probe is placed inside an "
                "opened carton of vaccine on the refrigerator's middle shelf, among the doses, so that it reads the "
                "temperature of the vaccine itself. It takes a reading every ten minutes and sends it to Tellvane's "
                "cloud, which keeps every reading with its time in UTC. Each sensor has a printed sensor id, which the "
                "monitoring roster records against its store."])
    s += [Paragraph("4 Installation", HEAD)]
    s += _p(["One store a week from the week of 4 May, in the order above. Tamberlane's installer and the store's "
                "pharmacist place the sensor together and confirm the first readings in the Tellvane app. From "
                "installation the sensor is the store's device of record (Standard PO-114, section 6.4)."])
    s += [Paragraph("5 Check-in visit", HEAD)]
    s += _p(["About two weeks after installation the pilot lead visits each store to confirm the readings are "
                "arriving without gaps, test the alert contacts and the on-call escalation, take the pharmacists' "
                "first comments and collect the store's data logger, which goes back to the pharmacy operations "
                "office."])
    s += [Paragraph("6 Records", HEAD)]
    s += _p(["Tellvane exports each sensor's readings as a CSV file. The pharmacy operations office downloads the "
                "pilot stores' readings each month with the other stores' logger downloads and keeps them for three "
                "years with the stores' temperature records."])
    s += [Paragraph("7 Evaluation", HEAD)]
    s += _p(["In January 2027 the pilot lead reports to the Director on the alerts raised and how quickly stores "
                "answered them, the gaps in the readings, the pharmacists' views, and the cost of moving every store to "
                "Tellvane against keeping the data loggers."])
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_agreement(path):
    title = "Refrigeration Service Agreement, Brannon Refrigeration Service and Penwick Pharmacy"
    org = "Brannon Refrigeration Service, LLC"
    d, frame = _doc(path, title, org)
    s = [Paragraph("Refrigeration Service Agreement", TITLE),
         Paragraph("Between Brannon Refrigeration Service, LLC (Brannon) and Penwick Pharmacy, Inc. (Penwick). Effective "
                   "1 January 2025 for two years, renewing for one year at a time unless either party gives 90 days' "
                   "notice.", SUB),
         Paragraph("1 Equipment", HEAD)]
    s += _p(["This agreement covers the vaccine refrigerator at each Penwick store listed in Schedule A, as it "
                "stands at the date of each visit. Penwick adds or removes a store by notice to Brannon."])
    s += [Paragraph("2 Preventive maintenance", HEAD)]
    s += _p(["2.1 Brannon maintains each unit twice a year, at visits scheduled before the store opens: cleaning the "
                "condenser coil, checking the door gasket, hinges and closer, checking the thermostat against a "
                "reference thermometer and checking the alarm.",
                "2.2 Each visit is charged at the price for the unit's model in Schedule B and includes up to 0.75 "
                "hours on site. Further work found at a visit is charged at the business-hours labor rate in quarter "
                "hours, with parts, on the same work order."])
    s += [Paragraph("3 Service calls", HEAD)]
    s += _p(["3.1 Brannon answers a call about a unit out of range within four hours, at any time.",
                "3.2 Each visit on a service call is charged a trip charge of 65.00 dollars and labor at 118.00 dollars "
                "an hour from 8:00 to 18:00 Monday to Friday and 177.00 dollars an hour at other times, in quarter "
                "hours with a minimum of one hour a visit. Parts are charged at Brannon's list price less 10 per cent."])
    s += [Paragraph("4 Invoices and payment", HEAD)]
    s += _p(["4.1 Brannon invoices each work order on its completion. Invoices are payable 30 days from their date.",
                "4.2 Brannon adds sales tax to each invoice at the rate in force at the store, which is 6.0 per cent in "
                "2025 and 2026.",
                "4.3 Brannon keeps each store's service history, with every visit and invoice, in its customer portal, "
                "where Penwick may export it at any time."])
    s += [Paragraph("5 Term and prices", HEAD)]
    s += _p(["The prices in section 3 and Schedule B hold for the first two years. Either party may propose new "
                "prices for a renewal year by 1 October before it."])
    s += [Paragraph("Schedule A. Stores and units", HEAD)]
    rows = [["Store", "Brannon site", "Unit"]]
    for st in W.STORES:
        mk, md, _ = A.model_of(st["no"])
        rows.append([str(st["no"]), A.BRANNON_SITE[st["no"]], "%s %s" % (mk, md)])
    t = Table(rows, colWidths=[0.8 * inch, 1.2 * inch, 2.0 * inch], repeatRows=1)
    t.setStyle(GRID)
    s += [t, Spacer(1, 8), Paragraph("Schedule B. Preventive maintenance price per visit", HEAD)]
    rows = [["Model", "Type", "Price per visit (dollars)"]]
    for kind, lst in A.MODELS.items():
        for (mk, md, price) in lst:
            rows.append(["%s %s" % (mk, md), "Pharmaceutical-grade" if kind == "pharma" else "Household-style",
                         "%.2f" % price])
    t = Table(rows, colWidths=[1.6 * inch, 1.6 * inch, 1.8 * inch])
    t.setStyle(GRID)
    s += [t]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_quotes(path):
    title = "Pharmaceutical refrigerator quotations for the 2027 program"
    d, frame = _doc(path, title, "Penwick Pharmacy, Procurement")
    s = [Paragraph(title, TITLE),
         Paragraph("Penwick Pharmacy, Procurement. Quotations received 8 to 15 January 2027 for the capital committee's "
                   "February meeting. Prices are per unit, delivered, and hold for orders placed by 31 March 2027.",
                   SUB)]
    rows = [["Supplier", "Model", "Capacity (cu ft)", "Unit price", "Delivery and installation", "Qualification",
             "Lead time"],
            ["Northcold Scientific", "PG-23", "23", "6,840.00", "420.00", "380.00", "8 to 10 weeks"],
            ["Northcold Scientific", "PG-12 (undercounter)", "12", "5,215.00", "380.00", "380.00", "8 to 10 weeks"],
            ["Stellane Cold Chain", "V-26", "26", "7,390.00", "395.00", "450.00", "6 to 8 weeks"],
            ["Stellane Cold Chain", "V-15 (undercounter)", "15", "5,880.00", "395.00", "450.00", "6 to 8 weeks"],
            ["Pendry Medical", "GM-20P", "20", "6,120.00", "510.00", "340.00", "12 weeks"]]
    t = Table([[Paragraph(x, CELL) for x in r] for r in rows],
              colWidths=[1.2 * inch, 1.2 * inch, 0.7 * inch, 0.75 * inch, 0.9 * inch, 0.8 * inch, 0.9 * inch])
    t.setStyle(GRID)
    s += [t, Spacer(1, 10)]
    s += _p(["Qualification is a 24-hour temperature mapping of the installed unit, empty and loaded, with a report "
                "the store keeps with its temperature records. Every quoted model is a pharmaceutical-grade unit with "
                "a microprocessor controller, forced-air circulation, a self-closing glass door and a probe port for "
                "a data logger. Removal of the old unit is 85.00 dollars a store with any supplier.",
                "Prices exclude sales tax. Northcold offers 4 per cent off its unit prices on an order of ten or more "
                "units placed at once; Stellane offers the first year's preventive maintenance free."])
    d.build(s, onFirstPage=frame, onLaterPages=frame)
