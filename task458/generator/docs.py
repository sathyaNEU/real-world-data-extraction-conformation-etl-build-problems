"""The pack's three documents, each in its owner's voice: the group's stock provisioning policy (FIN-07), the
facility agreement's borrowing base clauses, and Valuehall's 2027 store plan. No document describes a data file,
states a recovery, a rate, a provision or an outlet budget, or proposes an answer."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

from world import *    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1d1d1f")
GREY = colors.HexColor("#5b5f66")
NAVY = colors.HexColor("#1f3a5f")
BODY = ParagraphStyle("body", fontName="LiberationSans", fontSize=9.6, leading=13.4, textColor=INK, spaceAfter=6)
SERIF = ParagraphStyle("serif", fontName="LiberationSerif", fontSize=10.4, leading=14.2, textColor=INK, spaceAfter=7)
H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=13.5, leading=17, textColor=NAVY, spaceAfter=4)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.2, leading=13.5, textColor=NAVY, spaceBefore=6,
                    spaceAfter=3)
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8, leading=10.4, textColor=GREY)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.6, leading=10.8, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
NUM = ParagraphStyle("num", parent=SERIF, leftIndent=9 * mm, firstLineIndent=-9 * mm)

PROVENANCE = [
    # key, source, as-of date, description (for metadata.json only)
    ("ahl_stock", "Ashlund Home Ltd ERP, stock valuation report by bin", "2027-01-04",
     "Ashlund Home Ltd stock on hand at 31 December 2026 at unit cost, by bin"),
    ("ahi_stock", "Ashlund Home Ireland Ltd ERP, inventory valuation (cost specification)", "2027-01-05",
     "Ashlund Home Ireland Ltd inventory at 31 December 2026 in euro"),
    ("ahb_stock", "Ashlund Home B.V. ERP, voorraadwaardering", "2027-01-05",
     "Ashlund Home B.V. stock at 31 December 2026 in euro, by article"),
    ("ahb_xref", "Ashlund Home B.V. ERP, article to group code table", "2027-01-05",
     "Ashlund Home B.V. article numbers and the group item codes they carry"),
    ("master", "Group item master (product data team)", "2027-01-11", "Group item codes, divisions and case quantities"),
    ("ahl_orders", "Ashlund Home Ltd ERP, sales order line report", "2027-01-04",
     "Ashlund Home Ltd order lines despatched and returned, 2025 and 2026"),
    ("ahi_ship26", "Ashlund Home Ireland Ltd ERP (from 1 January 2026), posted shipment and return receipt lines",
     "2027-01-05", "Ashlund Home Ireland Ltd posted shipment and return lines, 2026"),
    ("ahi_arch25", "Ashlund Home Ireland Ltd previous ERP, read-only archive, invoice and credit note lines", "2026-12-18",
     "Ashlund Home Ireland Ltd invoice and credit note lines, 2025"),
    ("ahb_orders", "Ashlund Home B.V. ERP, verkooporderregels", "2027-01-05",
     "Ashlund Home B.V. order lines, 2025 and 2026"),
    ("vh_weeks", "Valuehall Stores Ltd stock system, weekly store trading summary", "2027-01-06",
     "Valuehall store weeks since March 2021"),
    ("lots", "Group finance, trade lot register", "2027-01-08", "Lots of surplus stock sold to trade buyers, 2021 to 2026"),
    ("fx", "Group finance, rate table", "2027-01-04", "EUR to GBP average and month-end rates, 2025 and 2026"),
    ("rcf", "Group treasury system, facility utilisation", "2027-01-04", "Daily drawn balance on the revolving facility, 2026"),
    ("policy", "Group finance policy manual, FIN-07 (version 4)", "2025-03-14", "Stock provisioning policy"),
    ("facility", "Revolving credit facility agreement, extract of clauses 1 and 21", "2024-06-28",
     "Borrowing base definitions and financial covenant"),
    ("vhplan", "Valuehall Stores Ltd, 2027 store plan", "2026-11-20", "Valuehall stores, trading days and closures in 2027"),
    ("open_po", "Ashlund Home Ltd ERP, open purchase order lines", "2027-01-04",
     "Purchase order lines due for delivery in 2027"),
    ("pallets", "Group logistics, warehouse management system", "2027-01-04", "Weekly pallet positions occupied at each DC, 2026"),
]


def _doc(path, story, title, author):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=17 * mm,
                            bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")
    doc.build(story)


def write_policy(path):
    s = [Paragraph("Ashlund Home Group plc", SMALL),
         Paragraph("FIN-07 Stock provisioning", H1),
         Paragraph("Group finance policy manual. Version 4, approved by the audit committee on 12 March 2025. "
                   "Owner: group financial controller. Applies to every trading company of the group.", SMALL),
         Spacer(1, 4 * mm),
         Paragraph("1. Scope", H2),
         Paragraph("This policy sets how the group measures its inventories at each half-year and year end under IAS 2. "
                   "It applies to finished goods held by Ashlund Home Ltd, Ashlund Home Ireland Ltd, Ashlund Home B.V. and "
                   "Valuehall Stores Ltd, wherever the stock is held.", SERIF),
         Paragraph("2. Measurement", H2),
         Paragraph("2.1 Inventories are carried at the lower of cost and net realisable value, line by line. Cost is the "
                   "landed cost each trading company records in its own system.", NUM),
         Paragraph("2.2 In Ashlund Home Ltd, Ashlund Home Ireland Ltd and Ashlund Home B.V., excess stock is the "
                   "quantity of a line held at the balance sheet date beyond that line's net shipments to customers in the "
                   "twelve months to that date, in the same company. Net shipments are despatches less customer returns. "
                   "Transfers to Valuehall Stores Ltd and to other group companies are not shipments to customers.", NUM),
         Paragraph("2.3 Stock that is not excess is carried at cost.", NUM),
         Paragraph("2.4 Excess stock is carried at the net proceeds, excluding VAT, the group expects to receive for it "
                   "from its disposal in the year after the balance sheet date, where those proceeds are below cost. The "
                   "group disposes of surplus stock through Valuehall Stores Ltd and through trade buyers. Stock held by "
                   "Valuehall Stores Ltd at the balance sheet date is surplus stock awaiting disposal and is measured "
                   "with the excess.", NUM),
         Paragraph("2.5 Net realisable value is assessed on the stock held at the balance sheet date. The group's own "
                   "selling, store, warehouse and transport costs are period costs and are not deducted.", NUM),
         Paragraph("2.6 Stock held in euro is translated into sterling at the group's year-end rate.", NUM),
         Paragraph("3. Reporting", H2),
         Paragraph("3.1 The provision, the excess stock on which it rests and the stock carried after it are reported to "
                   "the audit committee for each trading company and each division before the accounts are approved.", NUM),
         Paragraph("3.2 The group's divisions are Kitchen and Dining (KD), Storage and Laundry (SL), Lighting and "
                   "Electrical (LE), Tools and Hardware (TH) and Garden and Outdoor (GO).", NUM),
         Spacer(1, 6 * mm),
         Paragraph("Superseded: version 3 (March 2022). Next review: March 2027.", SMALL)]
    _doc(path, s, "FIN-07 Stock provisioning", "Group Finance")


def write_facility(path):
    s = [Paragraph("EXECUTION VERSION", SMALL),
         Paragraph("GBP 32,000,000 Revolving Credit Facility Agreement", H1),
         Paragraph("between Ashlund Home Group plc as Parent, the Borrowers listed in Schedule 1 and Northgate "
                   "Commercial Bank plc as Lender. Dated 28 June 2024. Extract: clause 1.1 (selected definitions) and "
                   "clause 21 (financial covenant).", SMALL),
         Spacer(1, 4 * mm),
         Paragraph("1.1 Definitions", H2),
         Paragraph("<b>Audited Accounts</b> means the audited consolidated financial statements of the Group for a "
                   "Financial Year delivered under clause 19.1.", SERIF),
         Paragraph("<b>Borrowing Base</b> means, at any Test Date, 62.5 per cent. of Eligible Inventory at that Test "
                   "Date.", SERIF),
         Paragraph("<b>Eligible Inventory</b> means the inventories of the Group, at the lower of cost and net realisable "
                   "value, as stated in the consolidated balance sheet contained in the Audited Accounts for the Financial "
                   "Year ending on that Test Date.", SERIF),
         Paragraph("<b>Outstandings</b> means the aggregate principal amount of all Loans outstanding at the close of "
                   "business on a Test Date.", SERIF),
         Paragraph("<b>Test Date</b> means 31 December in each year.", SERIF),
         Paragraph("21. Financial covenant", H2),
         Paragraph("21.1 The Parent shall ensure that on each Test Date the Outstandings do not exceed the Borrowing "
                   "Base.", NUM),
         Paragraph("21.2 Compliance with clause 21.1 is tested on the Audited Accounts and shown in a Compliance "
                   "Certificate delivered with them, signed by two directors of the Parent.", NUM),
         Paragraph("21.3 A breach of clause 21.1 is an Event of Default under clause 23 unless, before the Audited "
                   "Accounts are delivered, the Lender has waived it in writing.", NUM),
         Spacer(1, 6 * mm),
         Paragraph("Clauses 2 to 20 and 22 onwards are not reproduced in this extract.", SMALL)]
    _doc(path, s, "RCF Facility Agreement extract", "Northgate Commercial Bank plc")


def write_vhplan(path):
    rows = [[Paragraph(h, CELLB) for h in ("Store", "Opened", "2027 closures", "Trading days 2027")]]
    days = {"VH01": 349, "VH02": 363, "VH03": 363, "VH04": 363, "VH05": 363}
    clos = {"VH01": "1 to 14 February (refit); 25 and 26 December"}
    for code, nm, op in STORES:
        rows.append([Paragraph("%s %s" % (code, nm), CELL), Paragraph(op.strftime("%d %B %Y").lstrip("0"), CELL),
                     Paragraph(clos.get(code, "25 and 26 December"), CELL), Paragraph("%d" % days[code], CELL)])
    rows.append([Paragraph("Total", CELLB), "", "", Paragraph("%d" % sum(days.values()), CELLB)])
    t = Table(rows, colWidths=[52 * mm, 30 * mm, 62 * mm, 26 * mm])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, NAVY), ("LINEABOVE", (0, -1), (-1, -1), 0.4, GREY),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    s = [Paragraph("Valuehall Stores Ltd", SMALL),
         Paragraph("2027 store plan", H1),
         Paragraph("Prepared by Valuehall operations for the group property committee, 20 November 2026.", SMALL),
         Spacer(1, 4 * mm),
         Paragraph("Valuehall will trade from its five existing stores throughout 2027. The Kettering site reviewed in "
                   "September is deferred: the landlord's works will not finish before the spring, and the committee "
                   "agreed to look at it again for a 2028 opening. No store closes in 2027.", SERIF),
         Paragraph("Leicester Fosse Park will close for its refit from Monday 1 February to Sunday 14 February 2027: new "
                   "lighting, a second till bank and the stockroom racking moved to the rear dock. All stores close on "
                   "Christmas Day and Boxing Day and trade on every other day of the year, including bank holidays.",
                   SERIF),
         Spacer(1, 2 * mm), t, Spacer(1, 5 * mm),
         Paragraph("Opening hours are unchanged: 9am to 8pm Monday to Saturday and 10am to 4pm on Sunday (Leicester and "
                   "Nottingham 10.30am to 4.30pm). Deliveries from the group's distribution centres continue on the "
                   "current fortnightly rota for each store.", SERIF)]
    _doc(path, s, "Valuehall 2027 store plan", "Valuehall Operations")
