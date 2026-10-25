"""The documents: the head of supply chain's planning note for the first category on automated store ordering, and
supply chain analytics' data dictionary for the folder."""
import datetime as dt

from docx import Document
from docx.shared import Pt

import params as P
import postprocess

AUTHOR = "Nikau Fletcher"
ANALYST = "Archie Eglinton"
VENDOR = "Kowhai Retail Systems"


def _doc(author, created, modified, revision):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    cp = d.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.created = created
    cp.modified = modified
    cp.revision = revision
    cp.title = ""
    cp.comments = ""
    return d


def plan(path):
    d = _doc(AUTHOR, dt.datetime(2026, 11, 9, 8, 40), dt.datetime(2026, 11, 16, 15, 12), 6)
    d.add_heading("Automated store ordering: the first category", 1)
    d.add_paragraph("Supply chain planning note, 16 November 2026. Nikau Fletcher, Head of Supply Chain.")
    d.add_heading("The change", 2)
    d.add_paragraph(
        "From 1 February 2027 the lines of one category in all 24 stores move onto %s' automated store "
        "ordering. The system reads each store's sales and opening stock every night and raises the next morning's "
        "order for every line, and the distribution centre's trailers deliver it before the store opens. The rest of "
        "the range follows over the next eighteen months, a category at a time." % VENDOR)
    d.add_paragraph(
        "The supply chain team has shortlisted four categories for the first move: bottled water, infant formula, dry "
        "pet food and gluten-free bakery. Infant formula comes to the stores direct from Arataki Nutrition on its "
        "weekly visit today; for the change it would be stocked at the distribution centre and come on the trailer "
        "with the other three.")
    d.add_heading("What going first is worth", 2)
    d.add_paragraph(
        "%s' contract commits the system to removing half of a category's out-of-stock line-days, and this plan "
        "takes that and no more. A line-day is out of stock when the store opened with none of the line on hand, as "
        "the stock system's opening position records it." % VENDOR)
    d.add_paragraph(
        "We value each category by what it would have sold in the 24 stores over the twelve months to 30 June 2026 "
        "had half of its out-of-stock line-days not happened, less what it did sell, at each line's 2025-26 shelf "
        "price, and we take that year as the guide to 2027. The category that adds the most goes first.")
    d.add_heading("The cereal trial", 2)
    d.add_paragraph(
        "%s ran the system for breakfast cereal in our Feilding, Levin and Carterton stores from 2 February 2026. "
        "Its export of the three stores' cereal stock for the thirteen weeks either side of that date is in the "
        "folder." % VENDOR)
    d.add_heading("Deliveries and suppliers", 2)
    d.add_paragraph(
        "The system's orders come on the next morning's trailer, so a trailer that reaches a store after it has "
        "opened puts the delivery on the shelf while customers are in the store. The category that goes first also "
        "changes what the distribution centre takes in from its suppliers each week.")
    d.add_heading("Decision", 2)
    d.add_paragraph(
        "The supply chain team will choose the first category on 25 November, from a short deck with the case and a "
        "workbook with the figures behind it.")
    d.save(path)
    postprocess.scrub(path, P.ORG, "2026-11-16")
    postprocess.finish_office(path, "2026-11-09T08:40:00Z", "2026-11-16T15:12:00Z", P.ORG, person=AUTHOR, revision=6)


def dictionary(path):
    d = _doc(ANALYST, dt.datetime(2026, 10, 28, 10, 5), dt.datetime(2026, 11, 13, 11, 50), 5)
    d.add_heading("Store ordering folder: data dictionary", 1)
    d.add_paragraph("Supply chain analytics, 13 November 2026. The four shortlisted categories' sales and stock for "
                    "the two years to 30 June 2026, the cereal trial, and the distribution centre's transport and "
                    "purchasing for the twelve months to 30 June 2026.")

    def table(rows):
        t = d.add_table(rows=1, cols=2)
        t.style = "Table Grid"
        t.rows[0].cells[0].text, t.rows[0].cells[1].text = "Field", "Meaning"
        for a, b in rows:
            r = t.add_row().cells
            r[0].text, r[1].text = a, b

    d.add_heading("pos_daily_sales_2024-07_2026-06.parquet", 2)
    d.add_paragraph("From the tills: one row per store, trading day and till code with sales or returns that day.")
    table([("store_no", "Ridgeway's store number."),
           ("trade_date", "The trading day."),
           ("item_code", "The code the tills sold the line under: our article number until 2 March 2025, the "
                         "supplier's GTIN from 3 March 2025, when the tills moved to scanning GTINs. "
                         "till_item_codes.csv gives each code's article."),
           ("units", "Units sold less units returned at the till that day."),
           ("net_sales_nzd", "The value at the till, including GST.")])
    d.add_heading("stock_positions_2024-07_2026-06.csv", 2)
    d.add_paragraph("From the stock system: one row per store, line and day.")
    table([("store_no, article", "Store number and Ridgeway's article number."),
           ("date", "The day."),
           ("on_hand_open", "Units on hand in the stock system when the store opened, after that morning's delivery."),
           ("delivered", "Units received that morning before the store opened."),
           ("adjustment", "Units the store added or removed in the stock system that day: write-offs for damage or "
                          "date, and count corrections where a count found a different number on the shelf.")])
    d.add_heading("lines.csv", 2)
    table([("article, gtin", "Ridgeway's article number and the line's current GTIN."),
           ("description, category, supplier", "As in the range."),
           ("case_size", "Units in the supplier's case."),
           ("shelf_price_fy2025, shelf_price_fy2026", "Shelf price in NZD including GST, 1 July 2024 to 30 June 2025 "
                                                       "and 1 July 2025 to 30 June 2026."),
           ("supply", "Distribution centre, or Supplier direct for lines the supplier delivers to the stores.")])
    d.add_heading("till_item_codes.csv", 2)
    d.add_paragraph("Every code the tills have sold each line under, with the dates it was in use; a supplier that "
                    "changes a line's pack gives it a new GTIN.")
    table([("item_code, code_type", "The code and whether it is an article number or a GTIN."),
           ("article", "Ridgeway's article number."),
           ("valid_from, valid_to", "The first and last day the tills used the code; valid_to is blank while in "
                                    "use.")])
    d.add_heading("stores.csv", 2)
    table([("store_no, store_name, town, region, island", "As in the store list."),
           ("opens, closes", "Trading hours.")])
    d.add_heading("cereal_trial_stock_2025-11_2026-05.csv", 2)
    d.add_paragraph("%s' export for the breakfast cereal lines in the three trial stores, 3 November 2025 to "
                    "3 May 2026; the system went live in the three stores on 2 February 2026." % VENDOR)
    table([("store_no, date, article, description", "As above; the cereal lines' article numbers."),
           ("on_hand", "Units on hand."),
           ("delivered", "Units delivered that morning before the store opened."),
           ("units_sold", "Units sold that day.")])
    d.add_heading("dc_trailer_stops_2025-26.csv", 2)
    d.add_paragraph("From the distribution centre's transport system: one row per store a trailer run reached, "
                    "1 July 2025 to 30 June 2026.")
    table([("run_no, trailer", "The run and the trailer on it."),
           ("store_no", "The store reached."),
           ("departed", "When the run left the distribution centre."),
           ("arrived", "When the trailer reached the store."),
           ("cases", "Cases unloaded.")])
    d.add_heading("store_trading_days_2025-26.csv", 2)
    d.add_paragraph("From the tills: each store's first and last sale and its transactions on each trading day, 1 July "
                    "2025 to 30 June 2026.")
    d.add_heading("dc_purchase_orders_2025-26.csv", 2)
    d.add_paragraph("The distribution centre's purchase orders for the shortlisted categories' lines it stocks, one "
                    "row per order line.")
    table([("po_no, supplier", "The order and the supplier."),
           ("issued", "The date the order was issued."),
           ("article, cases", "The line and the cases ordered."),
           ("due", "The delivery date on the order.")])
    d.add_heading("supplier_edi_messages_2025-26.csv", 2)
    d.add_paragraph("The EDI messages the distribution centre sent its suppliers: ORDERS for an order, ORDCHG for a "
                    "change to one.")
    d.add_heading("dc_goods_received_2025-26.csv", 2)
    d.add_paragraph("Goods received at the distribution centre against purchase orders, 1 July 2025 to 30 June 2026.")
    table([("grn_no, po_no", "The goods received note and its order."),
           ("delivery_ref", "The supplier's dispatch advice number for the order."),
           ("received", "The day the goods were received."),
           ("article, cases", "The line and the cases received."),
           ("pallets", "Pallets received.")])
    d.add_heading("dc_dock_appointments_2025-26.csv", 2)
    d.add_paragraph("From the distribution centre's dock booking system: the dispatch advices unloaded at each "
                    "appointment, 1 July 2025 to 30 June 2026.")
    table([("appointment_no", "The dock appointment."),
           ("supplier", "The supplier."),
           ("arrived", "When the truck reached the door."),
           ("door", "The receiving door."),
           ("delivery_ref", "A dispatch advice unloaded at the appointment.")])
    d.add_heading("Other files", 2)
    d.add_paragraph("shelf_space_2026.xlsx holds the March 2026 planogram's shelf metres and facings for each "
                    "shortlisted category in each store. store_ordering_hours_2025-26.csv holds the hours store staff "
                    "booked to counting and ordering each category each week.")
    d.save(path)
    postprocess.scrub(path, P.ORG, "2026-11-13")
    postprocess.finish_office(path, "2026-10-28T10:05:00Z", "2026-11-13T11:50:00Z", P.ORG, person=ANALYST, revision=5)
