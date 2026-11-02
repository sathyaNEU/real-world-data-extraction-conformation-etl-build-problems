"""The governing document: Saltmarsh Market's price integrity standard PI-2, revision 3, in the chain's own genre."""
import params as P
from pack import write_pdf


STANDARD_SENTENCES = {
    "accuracy": ("A store's price accuracy for a quarter is the share of the item scans at its registers in the "
                 "quarter that rang up at the price shown on the item's shelf-edge label at the moment of the scan."),
    "watch": ("A store whose price accuracy for a quarter is below 99.0 per cent goes on Price Watch for the "
              "following quarter."),
    "effect": ("Head office issues each week's price changes (flyer prices starting and ending, and regular price "
               "changes) in the weekly price change release, and they take effect at the registers at 00:00 on the "
               "Thursday that opens the flyer week."),
}


def standard(path):
    b = [
        ("title", "Price Integrity Standard PI-2"),
        ("small", "Saltmarsh Market Limited. Revision 3, approved 18 September 2026 by the Vice-President, Store "
                  "Operations; in force from 1 October 2026. Owner: Director of Price Integrity. Replaces revision 2 "
                  "(May 2024)."),
        ("h", "1. Purpose and scope"),
        ("p", "This standard governs price integrity at every Saltmarsh Market store: the agreement between the price a "
              "customer is charged at a register and the price the store shows the customer. It applies to every "
              "store in both price zones."),
        ("h", "2. Definitions"),
        ("p", "<b>2.1 Item scan.</b> One unit sold at a store register by scanning its barcode. Items sold by weight "
              "or by a keyed product code, voided lines and returns are not item scans."),
        ("p", "<b>2.2 Shelf-edge label.</b> The label on the shelf edge at the item's home location in the store "
              "planogram, showing the item's price."),
        ("p", "<b>2.3 Flyer week.</b> The seven days from the Thursday on which a weekly flyer starts to the Wednesday "
              "after it."),
        ("p", "<b>2.4 Price changes.</b> " + STANDARD_SENTENCES["effect"]),
        ("p", "<b>2.5 Quarter.</b> A calendar quarter, by the store's local date and time."),
        ("h", "3. Price accuracy"),
        ("p", "<b>3.1</b> " + STANDARD_SENTENCES["accuracy"] + " A scan that rang up above or below the label price "
              "was not accurate."),
        ("p", "<b>3.2</b> Price accuracy is reported in per cent for each store and each quarter."),
        ("h", "4. Price Watch"),
        ("p", "<b>4.1</b> " + STANDARD_SENTENCES["watch"]),
        ("p", "<b>4.2</b> A store on Price Watch has its store manager sign a daily price integrity sheet, and the "
              "Price Integrity team visits it every week. The Director of Price Integrity issues the Price Watch "
              "list by the 20th day of the quarter it covers."),
        ("h", "5. The Scanner Price Accuracy Code"),
        ("p", "<b>5.1</b> Saltmarsh Market follows the Retail Council of Canada's Scanner Price Accuracy Voluntary "
              "Code. When an item that carries no price sticker scans at a price higher than its shelf price, the "
              "customer receives the first item free if the correct price is $10.00 or less, or $10.00 off the "
              "correct price if it is more; further units of the item in the same purchase are sold at the correct "
              "price."),
        ("p", "<b>5.2</b> A payout under the Code is made at the register, as a price override, or at the customer "
              "service desk, as a refund."),
        ("h", "6. Advertised prices"),
        ("p", "<b>6.1</b> An item in the weekly flyer rings up at its flyer price for the whole flyer week at every "
              "store in both price zones."),
        ("small", "PI-2 rev. 3. Next review September 2027."),
    ]
    write_pdf(path, "Price Integrity Standard PI-2 rev. 3", "Saltmarsh Market Store Operations", b,
              stamp_date="D:20260918103000+00'00'")
