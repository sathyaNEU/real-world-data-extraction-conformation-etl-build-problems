"""task161 documents: the space planning policy, the park's block offer, the customs broker's advisories
and the WMS export dictionary. The text is held here as data so checks.py can quote it and execute
every filed sentence, and verify.py reads the shipped PDFs back on its own extractor."""
from __future__ import annotations

import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import postprocess as PP    # noqa: E402
import world as W           # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("LibSerif", "liberation/LiberationSerif-Regular.ttf"), ("LibSerif-Bold", "liberation/LiberationSerif-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1f2328")
GREY = colors.HexColor("#5b626b")
PDS = colors.HexColor("#0f4c5c")        # Pellerin's teal
RA = colors.HexColor("#5a3d1e")         # Ridley-Ames brown
YV = colors.HexColor("#1d3a6e")         # Yamamoto & Vance navy
RULE = colors.HexColor("#a9b0b8")
HEAD = colors.HexColor("#e7ebef")


def styles(font, bold, accent, size=10.0):
    return dict(
        body=ParagraphStyle("b" + font + str(size), fontName=font, fontSize=size, leading=size * 1.36, textColor=INK,
                            spaceAfter=5),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=15, leading=19, textColor=accent, spaceAfter=2),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=8.8, leading=11.6, textColor=GREY, spaceAfter=8),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=10.8, leading=14, textColor=accent, spaceBefore=7,
                          spaceAfter=2),
        cell=ParagraphStyle("c" + font, fontName=font, fontSize=8.2, leading=10.0, textColor=INK),
        cellb=ParagraphStyle("cb" + font, fontName=bold, fontSize=8.2, leading=10.0, textColor=INK),
        small=ParagraphStyle("sm" + font, fontName=font, fontSize=8.0, leading=10.2, textColor=GREY, spaceAfter=3))


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                             topMargin=0.8 * inch, bottomMargin=0.8 * inch, title=title, author=author, subject="",
                             creator="", producer="")


def _footer(text, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(0.9 * inch, 0.5 * inch, text)
        canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.5 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def grid(rows, widths, st, head=True):
    data = [[Paragraph(esc(str(c)), st["cellb"] if (head and i == 0) else st["cell"]) for c in r]
            for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1 if head else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
             ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), HEAD))
    t.setStyle(TableStyle(style))
    return t


# ----------------------------------------------------------------------------------- the space policy

POLICY_TITLE = "Space planning policy"
POLICY_SUB = ("Pellerin Distribution Services, Inc. | Revision 4, effective 2 March 2026 | "
              "Owner: Mariah Norman, Vice President, Operations")
POLICY_CONTROL = [("Policy", "OPS-07 Space planning"), ("Revision", "4, effective 2 March 2026"),
                  ("Owner", "Mariah Norman, Vice President, Operations"),
                  ("Approved", "Executive team, 24 February 2026"), ("Next review", "March 2027"),
                  ("Distribution", "Operations managers, customer service, finance")]
POLICY = [
    ("1. Purpose and scope", [
        "This policy sets how we forecast the space our accounts will need and when we commit to space beyond our "
        "own four buildings. It applies to every space forecast prepared for a commitment of temporary space and to "
        "every commitment to an overflow block. It does not cover the cross-dock lanes Avila Transload runs for our "
        "transload accounts at its own site.",
    ]),
    ("2. Our space", [
        "2.1 Our four buildings in Carson, Rancho Dominguez, Wilmington and Compton hold 40,000 rack positions between "
        "them; the site list gives each building's count. A rack position holds one pallet.",
        "2.2 When the racks are full we hold pallets in floor lanes and at dock staging inside the buildings, in "
        "storage trailers in the yards and, when one is let, in subleased space. Each of these costs us: floor and "
        "staging pallets slow putaway and picking, a storage trailer ties up a yard spot and a trailer rented from "
        "the pool, and a sublease needs its own crew and a shuttle run.",
        "2.3 Floor lanes are marked and hold no more than 12 pallets each, following the fire inspection at Del Amo "
        "in October 2025.",
    ]),
    ("3. Space forecasts", [
        "3.1 A space forecast covers the accounts under contract on the day it is made and counts every pallet they "
        "will hold with us, in our racks or outside them, as the mean of each day's closing stock in the month.",
        "3.2 Overflow is the part of a month's forecast above the 40,000 rack positions of the four buildings.",
        "3.3 Capacity planning prepares the forecast. It is approved with the commitment it supports and kept with "
        "the commitment's papers in the capacity log.",
        "3.4 An account's normal stock for a month is its cover times the mean of its shipments in that month and the "
        "month after; its cover is the months of those shipments it holds in its ordinary months.",
    ]),
    ("4. Overflow blocks", [
        "4.1 Space at a third-party facility is taken in the blocks the facility offers, whole, and for the whole "
        "term it offers.",
        "4.2 Blocks are counted in order. The first block would hold each month's overflow up to its positions, the "
        "second the overflow above the first block's positions up to its own, and so on. A block is taken when the "
        "overflow it would hold over the term is at least three quarters of its position-months, a block's "
        "position-months being its positions times the months of the term.",
        "4.3 Overflow that does not justify a block is held in floor lanes and storage trailers.",
        "4.4 Stock moved into a block comes out of floor lanes and storage trailers first; dock staging is kept "
        "clear for the day's work.",
    ]),
    ("5. Approval", [
        "The Vice President, Operations approves commitments to overflow blocks of up to $5,000,000 for a term. A "
        "larger commitment also needs the approval of the Chief Financial Officer.",
    ]),
]
POLICY_HISTORY = [("1", "March 2019", "First issue"), ("2", "August 2020", "Subleased space added to section 2"),
                  ("3", "June 2023", "Rack positions recounted after the Anaheim Street re-rack"),
                  ("4", "March 2026", "Section 4 on overflow blocks; normal stock defined in 3.4; floor lane limit "
                                      "in 2.3")]


def write_policy(path):
    st = styles("LibSans", "LibSans-Bold", PDS, 10.0)
    s = [Paragraph(esc("Pellerin Distribution Services, Inc."), st["sub"]), Paragraph(esc(POLICY_TITLE), st["h1"]),
         Spacer(1, 4), grid([(k, v) for k, v in POLICY_CONTROL], [1.3, 4.2], st, head=False), Spacer(1, 6)]
    for head, paras in POLICY:
        s.append(KeepTogether([Paragraph(esc(head), st["h2"])] + [Paragraph(esc(p), st["body"]) for p in paras]))
    s.append(Spacer(1, 8))
    s.append(Paragraph(esc("Revision history"), st["h2"]))
    s.append(grid([("Rev.", "Date", "Change")] + POLICY_HISTORY, [0.6, 1.2, 3.7], st))
    doc = _doc(path, "Space planning policy, revision 4", "Mariah Norman")
    f = _footer("Pellerin Distribution Services | OPS-07 Space planning | Rev. 4 | Internal", "LibSans")
    doc.build(s, onFirstPage=f, onLaterPages=f)
    PP.normalize_pdf(path, b"D:20260227161812-08'00'", b"D:20260302083405-08'00'")


# ----------------------------------------------------------------------------------- the block offer

OFFER_DATE = "19 November 2026"
OFFER_REF = "Ref. TAL-B/2027-1/PDS"
OFFER = [
    "Thank you for walking Building B with us last week. As discussed, the building will have six blocks of 4,000 "
    "rack positions each available for the term 1 January 2027 to 30 June 2027. Each block is a contiguous run of "
    "selective pallet racking on five beam levels with two dock doors of its own, and the racking takes standard "
    "48 by 40 inch pallets up to 60 inches high. The previous occupant left at the end of October and the racking "
    "was inspected on 12 November.",
    "The charge is $1,100,000 per block for the term, payable in six monthly instalments in advance. It covers the "
    "positions, dock access from 05:00 to 23:00 Monday to Saturday, yard space for four trailers per block, and the "
    "building's security, fire protection and property insurance. Handling is by your own staff and equipment, and "
    "we will need evidence of your warehouse legal liability cover before the term starts.",
    "Blocks are let whole and for the whole term; we are not able to let part of a block or part of the term. We are "
    "offering the blocks to several users and will allocate them in the order countersigned schedules are received. "
    "A commitment is made by countersigning the enclosed block schedule for the number of blocks you wish to take.",
    "Please call me on (310) 555-0182 with any questions about the building or the schedule.",
]


def write_offer(path):
    st = styles("LibSerif", "LibSerif-Bold", RA, 10.6)
    s = [Paragraph(esc("Ridley-Ames Industrial Properties"), st["h1"]),
         Paragraph(esc("Tamarind Avenue Logistics Park | Leasing office | (310) 555-0182"), st["sub"]),
         Spacer(1, 6), Paragraph(esc(OFFER_DATE), st["body"]), Paragraph(esc(OFFER_REF), st["small"]),
         Spacer(1, 4), Paragraph(esc("Mariah Norman"), st["body"]),
         Paragraph(esc("Vice President, Operations, Pellerin Distribution Services, Inc."), st["body"]),
         Paragraph(esc("By email"), st["small"]), Spacer(1, 6),
         Paragraph(esc("Re: Overflow storage blocks, Building B, January to June 2027"), st["h2"]),
         Paragraph(esc("Dear Ms Norman,"), st["body"])]
    s += [Paragraph(esc(p), st["body"]) for p in OFFER]
    s += [Spacer(1, 4), Paragraph(esc("Yours sincerely,"), st["body"]), Spacer(1, 14),
          Paragraph(esc("Brandon Page"), st["body"]),
          Paragraph(esc("Leasing Manager, Ridley-Ames Industrial Properties"), st["body"]), Spacer(1, 8),
          Paragraph(esc("Enclosure: Building B block schedule, January to June 2027"), st["small"]),
          Paragraph(esc("cc: Property accounts, Ridley-Ames Industrial Properties"), st["small"])]
    s.append(Spacer(1, 6))
    sched = [("Block", "Positions", "Dock doors", "Term", "Charge for the term", "Taken (countersign)")]
    for k in range(1, 7):
        sched.append(("B-%d" % k, "4,000", "%d and %d" % (2 * k + 9, 2 * k + 10), "1 Jan 2027 to 30 Jun 2027",
                      "$1,100,000", ""))
    s.append(grid(sched, [0.6, 0.8, 0.9, 1.7, 1.3, 1.3], st))
    doc = _doc(path, "Overflow storage blocks, Building B, January to June 2027", "Ridley-Ames Industrial Properties")
    f = _footer("Ridley-Ames Industrial Properties | Tamarind Avenue Logistics Park", "LibSerif")
    doc.build(s, onFirstPage=f, onLaterPages=f)
    PP.normalize_pdf(path, b"D:20261119142207-08'00'", b"D:20261119142207-08'00'")


# ----------------------------------------------------------------------------------- the broker's advisories

ADVISORIES = [
    ("13 May 2019", "Proposed additional duties on a further list of goods from China",
     "The U.S. Trade Representative has published a proposed list of further goods from China that would carry "
     "additional duties of up to 25 per cent, with public hearings from 17 June. The list covers most consumer goods "
     "not on the earlier lists. Clients with flexible orders may wish to bring shipments forward."),
    ("16 August 2019", "List 4A duties apply to entries from 1 September 2019",
     "Additional duties on the goods in List 4A apply to goods entered for consumption on or after 1 September 2019. "
     "Goods entered before 1 September are not affected."),
    ("2 January 2025", "Expected duty increases in 2025",
     "We expect new duties on imports to be announced in the first months of the year. Several clients have asked us "
     "to bring entries forward; we can advise on the timing of entries for goods already in transit."),
    ("3 April 2025", "Additional 10 per cent duty on most imports from 5 April 2025",
     "An additional ad valorem duty of 10 per cent applies to most imported goods entered for consumption on or after "
     "12:01 a.m. EDT on 5 April 2025. Higher rates for some countries are scheduled from 9 April."),
    ("28 May 2025", "Country rates paused until 9 July",
     "The higher country rates paused on 9 April remain scheduled to apply after 9 July, and litigation over the "
     "duties continues. Clients are again bringing shipments forward ahead of the end of the pause."),
    ("1 August 2025", "Revised country rates from 7 August 2025",
     "Revised additional duties by country of origin apply to goods entered for consumption on or after 12:01 a.m. "
     "EDT on 7 August 2025. Please send us the bills of lading for any shipment you expect to enter in the week of "
     "the change so we can confirm its rate."),
    ("24 August 2026", "Duty increase from 1 January 2027",
     "Increases in the additional duties on a wide range of consumer goods take effect for goods entered for "
     "consumption on or after 12:01 a.m. EST on 1 January 2027. Goods entered before that date are not affected. We "
     "expect heavy front-loading through the autumn and will publish entry cut-off guidance in November."),
]


def write_advisories(path):
    st = styles("LibSans", "LibSans-Bold", YV, 9.8)
    s = [Paragraph(esc("Yamamoto & Vance Customs Brokers"), st["h1"]),
         Paragraph(esc("Client advisories: duty changes, archive extract for Pellerin Distribution Services, Inc. "
                       "(advisories of 2019 to 2026 on additional duties)"), st["sub"])]
    for date, title, text in ADVISORIES:
        s.append(KeepTogether([Paragraph(esc("%s | %s" % (date, title)), st["h2"]), Paragraph(esc(text), st["body"])]))
    s.append(Spacer(1, 8))
    s.append(Paragraph(esc("These advisories are general information for our clients and are not legal advice. "
                           "Duty treatment depends on the classification and origin of each entry."), st["small"]))
    doc = _doc(path, "Client advisories: duty changes, archive extract", "Yamamoto & Vance Customs Brokers")
    f = _footer("Yamamoto & Vance Customs Brokers | Client advisories", "LibSans")
    doc.build(s, onFirstPage=f, onLaterPages=f)
    PP.normalize_pdf(path, b"D:20261203101544-08'00'", b"D:20261203101544-08'00'")


# ----------------------------------------------------------------------------------- the export dictionary

DICT_TITLE = "WMS exports: field dictionary"
DICT_SUB = "Version 3, 2 November 2026 | Jerome Lam, WMS Systems Lead"
DICT_GENERAL = [
    "Stamps ending in Z are UTC. Business dates are Pacific dates. Pallet counts are whole pallets (one license "
    "plate number, LPN, per pallet).",
    "Each nightly inventory run starts at midnight Pacific and holds the balances at the close of the business day "
    "just ended; snapshot_utc is the run's start in UTC (07:00Z under daylight time, 08:00Z otherwise).",
    "The legacy WMS1 system was retired at the close of 30 September 2022. Both systems ran from the close of "
    "12 September 2022 to the close of 30 September 2022, and the legacy client codes map to client ids in the "
    "client master.",
    "A site is one of the four buildings (CAR1, RDZ1, WIL1, CMP1) with its docks and its yard, or the Dominguez "
    "sublease (DHS1) while it is let. A pallet on a site is either in a warehouse location (a rack position, a floor "
    "lane or a dock staging lane) or in a storage trailer parked in the site's yard.",
    "Ocean containers reach us by dray from the container terminals of the Port of Los Angeles and the Port of Long "
    "Beach.",
]
DICT = [
    ("wms1_inv_daily_20190401-20220930.txt (legacy WMS1, pipe-delimited)", [
        ("BUS_DT", "business date, MM/DD/YYYY; one row per client per business day, Monday to Saturday"),
        ("CLIENT", "legacy client code"),
        ("OPEN_PLT, RCVD_PLT, SHIP_PLT, CLOSE_PLT", "pallets at the opening, received, shipped and at the close"),
    ]),
    ("wms_inventory_nightly_20220913_20261207.csv", [
        ("snapshot_utc", "the run's start, UTC"),
        ("site_id", "CAR1, RDZ1, WIL1, CMP1 (the four buildings) and DHS1 (the Dominguez sublease, while let)"),
        ("client_id", "client id"),
        ("on_hand_pallets", "pallets on hand for the client at the site at the close, in its warehouse locations and "
                            "in storage trailers in its yard"),
    ]),
    ("wms_outbound_daily_20220912_20261206.csv", [
        ("ship_date", "business date the loads shipped"),
        ("client_id", "client id"),
        ("loads", "outbound loads (bills of lading)"),
        ("pallets_shipped", "pallets shipped"),
    ]),
    ("wms_inbound_receipts_20220912_20261206.csv", [
        ("receipt_no", "receipt number"),
        ("received_at_utc", "time the receipt was confirmed, UTC"),
        ("site_id, client_id", "receiving building and client"),
        ("equipment_id", "container number (ISO 6346) or trailer number"),
        ("equipment_type", "ISO 6346 size-type code for a container (22G1 20ft, 42G1 40ft, 45G1 40ft high cube, L5G1 "
                           "45ft high cube) or 53DV for a 53ft dry van trailer. TEU: 22G1 1, 42G1 and 45G1 2, L5G1 2.25. "
                           "A container received in several pieces is counted once, in the month of its first receipt "
                           "(WMS) or delivery (Avila)."),
        ("pallets", "pallets received on the receipt"),
    ]),
    ("wms_lpn_inventory_20261207T0800Z.csv", [
        ("coverage", "one row per pallet in a warehouse location; pallets in yard storage trailers are held in the "
                     "yard system and are not in this extract"),
        ("snapshot_utc", "the run's start, UTC"),
        ("site_id, location_id", "site and warehouse location"),
        ("location_type", "RACK (rack position), FLOOR (floor lane), STAGE (dock staging lane)"),
        ("client_id, lpn", "client id; the pallet's SSCC-18 label"),
        ("item, cases, received_date", "item number, cases on the pallet, business date the pallet was received"),
    ]),
]


def write_dictionary(path):
    st = styles("Carlito", "Carlito-Bold", PDS, 10.2)
    s = [Paragraph(esc("Pellerin Distribution Services, Inc. | Information Systems"), st["sub"]),
         Paragraph(esc(DICT_TITLE), st["h1"]), Paragraph(esc(DICT_SUB), st["sub"]),
         Paragraph(esc("General"), st["h2"])]
    s += [Paragraph(esc(p), st["body"]) for p in DICT_GENERAL]
    for title, fields in DICT:
        s.append(KeepTogether([Paragraph(esc(title), st["h2"]),
                               grid([("Field", "Meaning")] + list(fields), [1.9, 4.8], st)]))
    s.append(Spacer(1, 8))
    s.append(Paragraph(esc("Questions about the exports: WMS support desk, extension 4410."), st["small"]))
    doc = _doc(path, "WMS exports: field dictionary, version 3", "Jerome Lam")
    f = _footer("Pellerin Distribution Services | WMS exports: field dictionary | v3", "Carlito")
    doc.build(s, onFirstPage=f, onLaterPages=f)
    PP.normalize_pdf(path, b"D:20261102113029-08'00'", b"D:20261102113029-08'00'")


# ----------------------------------------------------------------------------------- helpers for checks

def all_text():
    """Every sentence the four documents ship, for the counter-pin and leak sweeps."""
    out = [POLICY_TITLE, POLICY_SUB] + [p for _, ps in POLICY for p in ps]
    out += OFFER + [t for _, _, t in ADVISORIES] + [h for _, h, _ in ADVISORIES]
    out += DICT_GENERAL + [m for _, fs in DICT for _, m in fs]
    return out


def sentences(paras):
    out = []
    for p in paras:
        out += [x.strip() for x in re.split(r"(?<=[.;])\s+(?=[A-Z0-9])", p) if x.strip()]
    return out
