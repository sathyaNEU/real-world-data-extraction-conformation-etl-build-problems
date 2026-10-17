"""The pack's documents: Overton's offer, its two 2025 programme letters and its tank-wagon price sheet, the three card
programmes' pricing schedules, the marketers' group's file layout, the fleet manager's yard notes and the README. Their
text is kept here as data so checks.py can quote and execute it."""
from __future__ import annotations

import os
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("LibSerif", "liberation/LiberationSerif-Regular.ttf"), ("LibSerif-Bold", "liberation/LiberationSerif-Bold.ttf"),
               ("LibMono", "liberation/LiberationMono-Regular.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1f2329")
GREY = colors.HexColor("#5f6670")
OVERTON = colors.HexColor("#8a2a1c")
RIVERBEND = colors.HexColor("#1d4f7a")
CROSSROADS = colors.HexColor("#2d6a3e")
SMPM = colors.HexColor("#5a3d7a")
RULE = colors.HexColor("#a3abb5")
HEAD = colors.HexColor("#e7ebf0")


def styles(font, bold, accent, size=10.2):
    return dict(
        body=ParagraphStyle("b" + font + str(size), fontName=font, fontSize=size, leading=size * 1.36, textColor=INK,
                            spaceAfter=6),
        h1=ParagraphStyle("h1" + font + str(size), fontName=bold, fontSize=14.0, leading=18.0, textColor=accent,
                          spaceAfter=3),
        sub=ParagraphStyle("s" + font + str(size), fontName=font, fontSize=8.9, leading=11.8, textColor=GREY,
                           spaceAfter=9),
        h2=ParagraphStyle("h2" + font + str(size), fontName=bold, fontSize=10.6, leading=14.0, textColor=accent,
                          spaceBefore=7, spaceAfter=3),
        cell=ParagraphStyle("c" + font + str(size), fontName=font, fontSize=8.6, leading=10.8, textColor=INK),
        cellb=ParagraphStyle("cb" + font + str(size), fontName=bold, fontSize=8.6, leading=10.8, textColor=INK),
        small=ParagraphStyle("sm" + font + str(size), fontName=font, fontSize=8.2, leading=10.6, textColor=GREY,
                             spaceAfter=4))


def _doc(path, title, author, margins=1.0):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=margins * inch, rightMargin=margins * inch,
                             topMargin=0.8 * inch, bottomMargin=0.8 * inch, title=title, author=author, subject="",
                             creator="", producer="")


def _footer(left, font="Carlito", right="Page "):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(0.9 * inch, 0.5 * inch, left)
        canvas.drawRightString(letter[0] - 0.9 * inch, 0.5 * inch, "%s%d" % (right, doc.page))
        canvas.restoreState()
    return draw


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def grid(rows, widths, st, head=True):
    data = []
    for k, row in enumerate(rows):
        data.append([Paragraph(esc(str(c)), st["cellb"] if (head and k == 0) else st["cell"]) for c in row])
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1 if head else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 2.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4)]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), HEAD))
    t.setStyle(TableStyle(style))
    return t


def terms_table(rows, st, w=(1.35, 5.0)):
    data = [[Paragraph(esc(a), st["cellb"]), Paragraph(esc(b), st["cell"])] for a, b in rows]
    t = Table(data, colWidths=[x * inch for x in w])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 3.0), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.0),
                           ("BACKGROUND", (0, 0), (0, -1), HEAD)]))
    return t


def sentences(paras):
    return [s for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9(])", p)]


OVERTON_ADDR = "Overton Petroleum Co.  |  1420 South Jefferson Avenue, Cookeville, Tennessee 38506"
KEEBLE_ADDR = ["Gabriel Wyatt, Fleet Services Manager", "Keeble Supply Co.", "2650 Couchville Pike",
               "Nashville, Tennessee 37217"]


# ---------------------------------------------------------------------------------------------------- the offer
F_OFFER = "overton_offer_2026-08-26.pdf"
OFFER_OPEN = [
    "Gabriel,",
    "Thank you for the call on Monday. With the Gulf Coast rack down a little over 60 cents since the end of July and "
    "our allocation at the Memphis, Nashville and Knoxville terminals long into October, we can offer Keeble transport "
    "loads into its six yard tanks on the terms below.",
]
OFFER_TERMS = [
    ("Product", "Ultra-low sulfur diesel No. 2, clear."),
    ("Load", "8,000 net gallons (corrected to 60 degrees F), lifted for and delivered to one yard tank."),
    ("Loads offered", "Up to 32 in all, for any of the six yards."),
    ("Delivery period", "Monday, September 14 to Sunday, November 8, 2026. Deliveries Monday to Friday, 6:00 am to "
                        "2:00 pm, on 24 hours' call-off by the yard."),
    ("Price", "The TriState Rack Report contract average for ULSD No. 2 at the supplying terminal on the day of "
              "lifting, plus $0.019 per net gallon, delivered. Memphis supplies Memphis and Jackson, Nashville supplies "
              "Nashville and Cookeville, and Knoxville supplies Knoxville and Blountville. Federal and state taxes and "
              "fees are billed at cost."),
    ("Commitment", "Keeble confirms the number of loads for each yard in writing by Friday, September 4, 2026. Every "
                   "confirmed load is billed at the price above whether or not it has been called off by November 8."),
    ("Payment", "Net 10 days from invoice."),
]
OFFER_CLOSE = [
    "Against fleet card pricing off the same TriState average, every gallon taken on this offer saves the card "
    "programme's charge over the average less our 1.9 cents.",
    "The offer holds until 5:00 pm Central on September 4. I will need the name of a call-off contact at each yard "
    "with the confirmation.",
    "Regards,",
]


def write_offer(path):
    st = styles("LibSans", "LibSans-Bold", OVERTON, 10.0)
    s = [Paragraph("OVERTON PETROLEUM CO.", st["h1"]), Paragraph(esc(OVERTON_ADDR), st["sub"]),
         Paragraph("August 26, 2026", st["body"]), Paragraph("<br/>".join(esc(x) for x in KEEBLE_ADDR), st["body"]),
         Spacer(1, 4), Paragraph("Re: Transport loads for the yard tanks, September to November 2026", st["h2"])]
    s += [Paragraph(esc(p), st["body"]) for p in OFFER_OPEN]
    s += [terms_table(OFFER_TERMS, st), Spacer(1, 8)]
    s += [Paragraph(esc(p), st["body"]) for p in OFFER_CLOSE]
    s += [Spacer(1, 14), Paragraph("%s<br/>Commercial Account Manager<br/>Overton Petroleum Co." % K.PEOPLE["jobber"],
                                   st["body"])]
    doc = _doc(path, "Transport loads for the yard tanks, September to November 2026", K.PEOPLE["jobber"], 1.0)
    f = _footer("Overton Petroleum Co.", font="LibSans")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- 2025 letters
F_JXN25 = "overton_jackson_tank_programme_2025-03-03.pdf"
F_KNX25 = "overton_knoxville_tank_programme_2025-06-02.pdf"
PROG_LETTERS = {
    "JXN": dict(file=F_JXN25, date="March 3, 2025", re="Jackson yard tank, spring 2025", terminal="Memphis",
                body=["Gabriel,",
                      "As agreed on Friday, Overton will keep the Jackson yard tank supplied from Monday, March 10 "
                      "through Thursday, May 29, 2025, so that the Jackson vehicles can fuel at the yard island."],
                terms=[("Product", "Ultra-low sulfur diesel No. 2, clear."),
                       ("Loads", "8,000 net gallons by transport from our Memphis terminal, scheduled by our dispatch "
                                 "from the tank reading the yard sends at 3:00 pm each working day. The first two "
                                 "loads will be delivered on March 10 and 11."),
                       ("Price", "Overton's posted rack for ULSD No. 2 at Memphis in effect at the time of lifting, "
                                 "plus $0.024 per net gallon, delivered. Taxes and fees at cost."),
                       ("Invoicing", "One invoice for each bill of lading, dated the day of delivery. Net 10 days.")],
                close=["Thank you for the chance to show what yard fueling can do for the Jackson fleet."]),
    "KNX": dict(file=F_KNX25, date="June 2, 2025", re="Knoxville yard tank, summer 2025", terminal="Knoxville",
                body=["Gabriel,",
                      "Following Jackson, Overton will keep the Knoxville yard tank supplied from Monday, June 9 "
                      "through Friday, August 22, 2025, so that the Knoxville vehicles can fuel at the yard island."],
                terms=[("Product", "Ultra-low sulfur diesel No. 2, clear."),
                       ("Loads", "8,000 net gallons by transport from our Knoxville terminal, scheduled by our "
                                 "dispatch from the tank reading the yard sends at 3:00 pm each working day. The first "
                                 "two loads will be delivered on June 9 and 10."),
                       ("Price", "Overton's posted rack for ULSD No. 2 at Knoxville in effect at the time of lifting, "
                                 "plus $0.016 per net gallon, delivered. Taxes and fees at cost."),
                       ("Invoicing", "One invoice for each bill of lading, dated the day of delivery. Net 10 days.")],
                close=["We will send the Knoxville tank's first reading sheet with the June 9 delivery."]),
}


def write_prog_letter(path, y):
    L = PROG_LETTERS[y]
    st = styles("LibSans", "LibSans-Bold", OVERTON, 10.0)
    s = [Paragraph("OVERTON PETROLEUM CO.", st["h1"]), Paragraph(esc(OVERTON_ADDR), st["sub"]),
         Paragraph(L["date"], st["body"]), Paragraph("<br/>".join(esc(x) for x in KEEBLE_ADDR), st["body"]),
         Spacer(1, 4), Paragraph("Re: %s" % esc(L["re"]), st["h2"])]
    s += [Paragraph(esc(p), st["body"]) for p in L["body"]]
    s += [terms_table(L["terms"], st), Spacer(1, 8)]
    s += [Paragraph(esc(p), st["body"]) for p in L["close"]]
    s += [Paragraph("Regards,", st["body"]), Spacer(1, 14),
          Paragraph("%s<br/>Commercial Account Manager<br/>Overton Petroleum Co." % K.PEOPLE["jobber"], st["body"])]
    doc = _doc(path, L["re"], K.PEOPLE["jobber"], 1.0)
    f = _footer("Overton Petroleum Co.", font="LibSans")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- card schedules
F_CARDS = "card_programmes_pricing_schedules.pdf"
CARD_SCHEDULES = [
    dict(acct="West", accent=RIVERBEND, issuer="Riverbend Travel Plazas, Fleet Services",
         title="Fleet Direct Bill Agreement, Schedule A: Pricing",
         party="Account 30418, Delta Paper & Chemical LLC (a Keeble Supply Co. company). Schedule A as amended "
               "March 1, 2023.",
         clauses=[
             "A1. Diesel fuel dispensed on the account is priced per gallon at the TriState Rack Report contract "
             "average for ULSD No. 2 at the terminal serving the site, for the day the fuel is dispensed, plus $0.119.",
             "A2. The serving terminal is Memphis for sites in Arkansas, Mississippi and Tennessee west of the "
             "Tennessee River, and Nashville for all other sites.",
             "A3. Federal excise tax and state fuel taxes are billed at the rates in effect at the site.",
             "A4. Diesel exhaust fluid and all other products are billed at the site's posted price.",
             "A5. Riverbend invoices the account weekly, Monday through Sunday. Each transaction appears in the "
             "fleet portal the day after the fill, and the account's full history may be downloaded there."],
         signed="For Riverbend Travel Plazas: Director, Fleet Accounts. For Delta Paper & Chemical LLC: %s, "
                "Controller, Keeble Supply Co." % K.PEOPLE["controller"]),
    dict(acct="Central", accent=CROSSROADS, issuer="Crossroads Fleet Card",
         title="Customer Agreement, Pricing Addendum 4",
         party="Customer: Keeble Supply Co., account KS-20117. Effective January 1, 2025; replaces Pricing Addendum 3.",
         clauses=[
             "1. Diesel purchased with Crossroads cards at participating merchants is billed per gallon at the "
             "TriState Rack Report contract average for ULSD No. 2 at the merchant's serving terminal, for the day "
             "of the purchase, plus $0.084.",
             "2. A network fee of $0.015 per gallon applies to every diesel gallon billed.",
             "3. Taxes are billed as charged by the merchant.",
             "4. Diesel exhaust fluid and other products are billed at the merchant's price, with no network fee.",
             "5. Crossroads issues one statement a month. Transactions are available in the Crossroads portal, "
             "where the customer may export them in any date range."],
         signed="For Crossroads Fleet Card: Vice President, Commercial Fleet. For Keeble Supply Co.: %s, "
                "Controller." % K.PEOPLE["controller"]),
    dict(acct="East", accent=SMPM, issuer="Smoky Mountain Petroleum Marketers",
         title="Fleet Program, Schedule 1: Pricing",
         party="Member account HSS0417, Holston Sanitary Supply Inc. (a Keeble Supply Co. company). Schedule 1 as "
               "amended July 1, 2022.",
         clauses=[
             "1.1 Diesel fuel purchased on program cards at member sites is priced per gallon at the TriState Rack "
             "Report contract average for ULSD No. 2 at the terminal serving the member site, for the day of the "
             "purchase, plus $0.127.",
             "1.2 Federal and state fuel taxes are billed at the rates in effect at the member site.",
             "1.3 Diesel exhaust fluid is billed at the member site's posted price.",
             "1.4 Transactions are reported in the program's member transaction file, sent weekly; the layout is "
             "issued separately."],
         signed="For Smoky Mountain Petroleum Marketers: Program Manager. For Holston Sanitary Supply Inc.: %s, "
                "Controller, Keeble Supply Co." % K.PEOPLE["controller"]),
]


def write_cards(path):
    out = []
    for k, c in enumerate(CARD_SCHEDULES):
        st = styles("LibSerif", "LibSerif-Bold", c["accent"], 10.4)
        if k:
            out.append(PageBreak())
        out += [Paragraph(esc(c["issuer"]), st["sub"]), Paragraph(esc(c["title"]), st["h1"]),
                Paragraph(esc(c["party"]), st["sub"])]
        out += [Paragraph(esc(p), st["body"]) for p in c["clauses"]]
        out += [Spacer(1, 10), Paragraph(esc(c["signed"]), st["small"])]
    doc = _doc(path, "Card programmes, pricing schedules", K.PEOPLE["controller"], 1.0)
    f = _footer("Keeble Supply Co.  |  Card programmes, pricing schedules (copies)", font="Carlito")
    doc.build(out, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- SMPM layout
F_LAYOUT = "smpm_member_transaction_file_layout_v3.pdf"
LAYOUT = {
    "H": [("1", "1", "Record type", "H"), ("2-8", "7", "Batch number", "numeric"),
          ("9-16", "8", "Batch week start", "CCYYMMDD"), ("17-26", "10", "Member account", "alphanumeric"),
          ("27-56", "30", "Member name", "alphanumeric")],
    "D": [("1", "1", "Record type", "D"), ("2-8", "7", "Batch number", "numeric"),
          ("9-14", "6", "Sequence in batch", "numeric"), ("15-22", "8", "Transaction date", "CCYYMMDD"),
          ("23-26", "4", "Transaction time", "HHMM"), ("27-32", "6", "Site number", "alphanumeric"),
          ("33-40", "8", "Unit (as entered at the pump)", "alphanumeric"),
          ("41-48", "8", "Card number (last digits)", "alphanumeric"),
          ("49-55", "7", "Odometer (as entered)", "numeric"), ("56-59", "4", "Product code", "DSL2, DEF"),
          ("60-68", "9", "Quantity, gallons", "numeric, 3 implied decimals"),
          ("69-75", "7", "Price per gallon before tax", "numeric, 4 implied decimals"),
          ("76-82", "7", "Tax per gallon", "numeric, 4 implied decimals"),
          ("83-106", "24", "Site name", "alphanumeric"), ("107-108", "2", "Site state", "alphanumeric")],
    "T": [("1", "1", "Record type", "T"), ("2-8", "7", "Batch number", "numeric"),
          ("9-14", "6", "Detail records in batch", "numeric"),
          ("15-26", "12", "Total quantity, gallons", "numeric, 3 implied decimals")],
}
LAYOUT_NOTES = [
    "Numeric fields are right-justified and zero-filled; alphanumeric fields are left-justified and space-filled.",
    "Each weekly batch carries the transactions dated Monday through Sunday of its batch week and is transmitted on "
    "the following Monday.",
    "Product codes: DSL2 diesel No. 2; DEF diesel exhaust fluid.",
]


def write_layout(path):
    st = styles("LibSans", "LibSans-Bold", SMPM, 9.6)
    s = [Paragraph("Smoky Mountain Petroleum Marketers &middot; Fleet Program", st["sub"]),
         Paragraph("Member transaction file: record layout, version 3", st["h1"]),
         Paragraph("Effective with the batch of October 2, 2023. Fixed-width text, one record per line.", st["sub"])]
    names = {"H": "Batch header (H)", "D": "Transaction detail (D)", "T": "Batch trailer (T)"}
    for k in ("H", "D", "T"):
        s.append(Paragraph(names[k], st["h2"]))
        s.append(grid([["Positions", "Length", "Field", "Format"]] + [list(r) for r in LAYOUT[k]],
                      [0.85, 0.65, 2.75, 2.15], st))
    s.append(Paragraph("Notes", st["h2"]))
    s += [Paragraph(esc(p), st["body"]) for p in LAYOUT_NOTES]
    doc = _doc(path, "Member transaction file record layout v3", "SMPM Fleet Program", 0.95)
    f = _footer("SMPM Fleet Program  |  Member transaction file layout v3", font="LibSans")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- tank wagon
F_TW = "overton_tank_wagon_prices_2026-08-24.pdf"
TW_ROWS = [["Zone", "Counties served", "ULSD clear, over posted rack", "ULSD dyed, over posted rack", "Minimum drop"],
           ["1", "Putnam, White, Jackson, Overton", "$0.142", "$0.131", "300 gal"],
           ["2", "Cumberland, DeKalb, Smith, Warren, Fentress", "$0.168", "$0.157", "300 gal"],
           ["3", "Davidson, Rutherford, Wilson, Knox, Sullivan, Madison, Shelby", "$0.196", "$0.185", "500 gal"]]
TW_NOTES = [
    "Tank wagon deliveries of 300 to 2,999 gallons from our bobtail fleet, priced per gross gallon over Overton's posted "
    "rack at the supplying terminal on the day of delivery. Fuel surcharge: 3.5 per cent of the adder.",
    "Deliveries of 3,000 gallons or more are quoted as transport loads.",
]


def write_tankwagon(path):
    st = styles("LibSans", "LibSans-Bold", OVERTON, 9.8)
    s = [Paragraph("OVERTON PETROLEUM CO.", st["h1"]), Paragraph(esc(OVERTON_ADDR), st["sub"]),
         Paragraph("Tank wagon prices, week of August 24, 2026", st["h2"]),
         grid(TW_ROWS, [0.5, 2.6, 1.3, 1.3, 0.8], st), Spacer(1, 8)]
    s += [Paragraph(esc(p), st["body"]) for p in TW_NOTES]
    doc = _doc(path, "Tank wagon prices, week of August 24, 2026", "Overton Petroleum Co.", 0.95)
    f = _footer("Overton Petroleum Co.  |  Tank wagon prices", font="LibSans")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- yard notes
F_NOTES = "yard_notes_2026-08.md"


def count_units(W, y, body=None, status="Active"):
    return sum(1 for u in W.units if u.yard == y and u.status == status and (body is None or u.body in body))


def notes_text(W):
    c = lambda y, b=None: count_units(W, y, b)
    L = ["# Yard notes, August 2026", "",
         "Gabriel Wyatt, Fleet Services. For the fuel review; the unit list is the maintenance system's as of today.", "",
         "Every yard runs Monday to Friday and is closed on weekends and company holidays (Labor Day, September 7; "
         "Thanksgiving, November 26 and 27). No route, fleet or yard changes are planned before December.", "",
         "Each yard has one 20,000-gallon above-ground diesel tank and a self-serve island on the fuel management "
         "system. The islands have been on standby since the fleet moved to fuel cards in 2023, apart from the Jackson "
         "and Knoxville programmes in 2025. The fobs issued for those programmes still work at every island, and new "
         "units get a fob at delivery.", "",
         "## West (Delta's direct-bill account)", "",
         "- Memphis, branch 21, 4410 Getwell Road: %d Sprinter vans and %d straight trucks on metro routes." % (
             c("MEM", ("van",)), c("MEM", ("box",))),
         "- Jackson, branch 24, 117 Industrial Park Drive: %d straight trucks on metro routes, %d day cabs on the "
         "regional day runs and %d sleepers on the Mississippi, Arkansas and Kentucky routes." % (
             c("JXN", ("box",)), c("JXN", ("daycab",)), c("JXN", ("sleeper",))), "",
         "## Central (Keeble's Crossroads account)", "",
         "- Nashville, branch 31, 2650 Couchville Pike: %d straight trucks on metro routes and %d sleepers on the "
         "Kentucky, Alabama and Georgia routes. Two spare M2s are kept at the yard for breakdowns." % (
             c("NSH", ("box",)), c("NSH", ("sleeper",))),
         "- Cookeville, branch 35, 1290 Interstate Drive: %d straight trucks at the yard; %d Sprinter vans based at "
         "the Sparta and Crossville lots (leased spaces since 2024), stocked by shuttle from the yard." % (
             c("CKV", ("box",)), c("CKV", ("van",))), "",
         "## East (Holston's SMPM account)", "",
         "- Knoxville, branch 41, 5320 Middlebrook Pike: %d Sprinter vans on metro routes and %d sleepers on the "
         "Kentucky, Carolina and Virginia routes." % (c("KNX", ("van",)), c("KNX", ("sleeper",))),
         "- Blountville, branch 46, 1915 Highway 75: %d straight trucks on metro routes and %d sleepers on the "
         "Virginia, West Virginia and Kentucky routes." % (c("TRI", ("box",)), c("TRI", ("sleeper",))), "",
         "## Fuel", "",
         "Each account's vehicles carry that account's cards and buy wherever the route takes them.", ""]
    return "\n".join(L)


# ---------------------------------------------------------------------------------------------------- README
F_README = "fuel_review_files_2026-08-28.md"


def readme_text(W):
    L = ["# Fuel review: the files pulled on August 28", "",
         "Pulled by Gabriel Wyatt (Fleet Services) on Friday, August 28, 2026. The telematics files and the "
         "Riverbend and Crossroads downloads run through Thursday, August 27; the last SMPM batch received covers "
         "the week to Sunday, August 23.", "",
         "## Fleet and telematics", "",
         "- `%s`: the telematics service's vehicle-day export, one row for each day a vehicle's engine ran, September "
         "1, 2024 to August 27, 2026." % R.F_DAYS,
         "- `%s`: the telematics service's geofence entries and exits, March 1 to August 27, 2026 (the service keeps "
         "180 days of geofence history)." % R.F_GEO,
         "- `%s`: which telematics device was fitted to which vehicle, and when." % R.F_DEV,
         "- `%s`: the maintenance system's unit list and model specifications." % R.F_UNITS,
         "- `%s`: the fleet manager's yard notes." % F_NOTES, "",
         "## Yard tanks and islands", "",
         "- `%s`: the six yard tanks." % R.F_TANKS,
         "- `%s`: the fuel management system's island transactions for 2025, the Jackson and Knoxville "
         "programmes." % R.F_FMS, "",
         "## Card accounts", "",
         "- `%s`: Delta's direct-bill transactions, downloaded from the Riverbend fleet portal." % R.F_WEST,
         "- `%s`: Keeble's Crossroads Fleet Card transactions, exported from the Crossroads portal." % R.F_CENTRAL,
         "- `%s`: Holston's SMPM member transaction files, as received, one weekly batch after another; layout in "
         "`%s`." % (R.F_EAST, F_LAYOUT),
         "- `%s`: the pricing schedules of the three card programmes." % F_CARDS,
         "- `%s`: the IFTA returns filed for the three licences, third quarter 2025 to second quarter 2026." % R.F_IFTA,
         "", "## Overton", "",
         "- `%s`: Overton's offer of August 26." % F_OFFER,
         "- `%s` and `%s`: Overton's letters for the 2025 Jackson and Knoxville programmes." % (F_JXN25, F_KNX25),
         "- `%s`, `%s` and `%s`: Overton's 2025 delivery tickets, invoices and credit memos for the two programmes, "
         "from Overton's customer portal." % (R.F_DELIV, R.F_INV, R.F_CRED),
         "- `%s`: Overton's daily posted rack and the TriState contract average for ULSD No. 2 at Memphis, Nashville "
         "and Knoxville, by effective date." % R.F_RACK,
         "- `%s`: Overton's tank wagon prices for the week of August 24." % F_TW, ""]
    return "\n".join(L)


# ---------------------------------------------------------------------------------------------------- writing
PDF_STAMPS = {
    F_OFFER: (b"D:20260826151204-05'00'", b"D:20260826151204-05'00'"),
    F_JXN25: (b"D:20250303104512-06'00'", b"D:20250303104512-06'00'"),
    F_KNX25: (b"D:20250602093847-05'00'", b"D:20250602093847-05'00'"),
    F_CARDS: (b"D:20250106142219-06'00'", b"D:20250106142219-06'00'"),
    F_LAYOUT: (b"D:20230925111530-04'00'", b"D:20230925111530-04'00'"),
    F_TW: (b"D:20260824074102-05'00'", b"D:20260824074102-05'00'"),
}
DOCS = [F_OFFER, F_JXN25, F_KNX25, F_CARDS, F_LAYOUT, F_TW, F_NOTES, F_README]


def write_all(out, W):
    p = lambda f: os.path.join(out, f)
    write_offer(p(F_OFFER))
    write_prog_letter(p(F_JXN25), "JXN")
    write_prog_letter(p(F_KNX25), "KNX")
    write_cards(p(F_CARDS))
    write_layout(p(F_LAYOUT))
    write_tankwagon(p(F_TW))
    for f, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(p(f), c, m)
    with open(p(F_NOTES), "w", encoding="utf-8", newline="") as fh:
        fh.write(notes_text(W))
    with open(p(F_README), "w", encoding="utf-8", newline="") as fh:
        fh.write(readme_text(W))
