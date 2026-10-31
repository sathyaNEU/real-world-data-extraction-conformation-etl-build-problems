"""Constants for task268: Corcally's, its three stores and online shop, Corcally's Rewards, Faircourt Merchant Services,
the coffee range and its suppliers, the coffee counter, the 2026 multibuy deals, the people, the dates and the pack's
file names."""
import datetime as dt
import os

SEED = 263
ORG = "Corcally's"
ORG_LTD = "Corcally & Sons Limited"
YEAR = 2026

# store code, name, tills (the service desk is till 9), share of homes whose store it is, opening hours
STORES = [("DRM", "Drumsallagh", (1, 2, 3, 4, 5, 6, 7, 8, 9), 0.58, (8, 22)),
          ("LSG", "Lisgarvan", (1, 2, 3, 9), 0.23, (8, 21)),
          ("KBN", "Kilbrannagh", (1, 2, 3, 9), 0.19, (8, 21))]
STORE_NAME = {s[0]: s[1] for s in STORES}
DESK = 9

# Faircourt Merchant Services: merchant numbers and terminals (store, till, terminal, installed, removed)
MID = {"DRM": "4410231", "LSG": "4410232", "KBN": "4410233", "WEB": "4410239"}
TERMINALS = []
for code, name, tills, _, _ in STORES:
    base = {"DRM": "410231", "LSG": "410232", "KBN": "410233"}[code]
    for t in tills:
        TERMINALS.append((code, t, "%s%02d" % (base, t), dt.date(2023, 3, 6), None))
SWAP_DATE = dt.datetime(2026, 5, 12, 7, 40)            # Lisgarvan till 2's terminal replaced before opening
TERMINALS = [(s, t, tid, a, (SWAP_DATE.date() if (s, t) == ("LSG", 2) else b)) for s, t, tid, a, b in TERMINALS]
TERMINALS.append(("LSG", 2, "41023212", SWAP_DATE.date(), None))
COUNTER_TID = "41023121"
WEB_TID = "E4102390"

# the coffee brands: code, name as the brief writes it, supplier, multibuys run
BRANDS = [("OL", "Corcally's Roastery", "Corcally & Sons Limited"),
          ("HAL", "Halloran's", "Halloran & Sons Coffee Ltd"),
          ("BEL", "Bellvale", "Bellvale Foods Ireland Ltd"),
          ("NOR", "Nordhavn", "Nordhavn Coffee Ireland Ltd"),
          ("ROS", "Oro Rosso", "Oro Rosso Caffe Ireland Ltd"),
          ("CAF", "Cafetto", "Cafetto Brands Ireland Ltd"),
          ("WES", "Westquay", "Westquay Roasters Ltd"),
          ("KIN", "Kinvara Hills", "Kinvara Hills Coffee Ltd")]
B = [b[0] for b in BRANDS]
RIVALS = B[1:]
BRAND_NAME = {b[0]: b[1] for b in BRANDS}
SUPPLIER = {b[0]: b[2] for b in BRANDS}
FUNDED = ("HAL", "BEL", "NOR", "ROS", "CAF")            # the suppliers that ran multibuys in 2026

# SKUs: plu, brand, master spelling, till description, full description, format, grams, price, listed online
SKUS = [
    ("5391002110018", "OL", "Corcally's Roastery", "ROASTERY HOUSE GRD 227", "Corcally's Roastery House Blend ground coffee 227g", "Ground", 227, 4.29, "Y"),
    ("5391002110025", "OL", "Corcally's Roastery", "ROASTERY BREAKFAST 454", "Corcally's Roastery Breakfast Blend ground coffee 454g", "Ground", 454, 7.79, "Y"),
    ("5391002110032", "OL", "Corcally's Roastery", "ROASTERY ESPRESSO BN500", "Corcally's Roastery Espresso beans 500g", "Beans", 500, 8.49, "Y"),
    ("5391002110049", "OL", "Corcally's Roastery", "ROASTERY COLOMBIA BN 1K", "Corcally's Roastery Colombia beans 1kg", "Beans", 1000, 15.99, "Y"),
    ("5391002110056", "OL", "Corcally's Roastery", "ROASTERY DECAF GRD 227", "Corcally's Roastery Decaf ground coffee 227g", "Ground", 227, 4.49, "Y"),
    ("5391127400016", "HAL", "Halloran's", "HALLORANS GOLD GRD227", "Halloran's Gold Blend ground coffee 227g", "Ground", 227, 4.59, "Y"),
    ("5391127400023", "HAL", "HALLORANS", "HALLORANS ORIG GRD454", "Halloran's Original ground coffee 454g", "Ground", 454, 8.29, "Y"),
    ("5391127400030", "HAL", "Hallorans Coffee", "HALLORANS ITAL BN 1KG", "Halloran's Italian Roast beans 1kg", "Beans", 1000, 15.49, "Y"),
    ("5391127400047", "HAL", "Halloran's", "HALLORANS MILD GRD227", "Halloran's Mild Roast ground coffee 227g", "Ground", 227, 4.59, "Y"),
    ("5391488600014", "BEL", "Bellvale", "BELLVALE CLASSIC 227", "Bellvale Classic ground coffee 227g", "Ground", 227, 3.69, "Y"),
    ("5391488600021", "BEL", "Bellvale", "BELLVALE STRONG 340", "Bellvale Strong ground coffee 340g", "Ground", 340, 4.99, "Y"),
    ("5391488600038", "BEL", "Bellvale", "BELLVALE FILTER 500", "Bellvale Filter ground coffee 500g", "Ground", 500, 6.49, "Y"),
    ("5701923300017", "NOR", "Nordhavn", "NORDHAVN LUNGO 10CAP", "Nordhavn Lungo capsules x10", "Capsules", 55, 3.99, "Y"),
    ("5701923300024", "NOR", "Nordhavn", "NORDHAVN FORTE 10CAP", "Nordhavn Espresso Forte capsules x10", "Capsules", 55, 3.99, "Y"),
    ("5701923300031", "NOR", "Nordhavn", "NORDHAVN DECAF 10CAP", "Nordhavn Decaffeinato capsules x10", "Capsules", 55, 4.19, "Y"),
    ("5701923300048", "NOR", "Nordhavn", "NORDHAVN LUNGO 30CAP", "Nordhavn Lungo capsules x30", "Capsules", 165, 10.49, "Y"),
    ("5701923300055", "NOR", "Nordhavn", "NORDHAVN RISTR 20CAP", "Nordhavn Ristretto capsules x20", "Capsules", 110, 7.49, "Y"),
    ("8001477200011", "ROS", "Oro Rosso", "ORO ROSSO CREMA BN1K", "Oro Rosso Crema beans 1kg", "Beans", 1000, 17.99, "Y"),
    ("8001477200028", "ROS", "Oro Rosso", "ORO ROSSO ESPR GR250", "Oro Rosso Espresso ground coffee 250g", "Ground", 250, 4.99, "Y"),
    ("8001477200035", "ROS", "Oro Rosso", "ORO ROSSO INTEN BN500", "Oro Rosso Intenso beans 500g", "Beans", 500, 9.49, "Y"),
    ("5391733500012", "CAF", "Cafetto", "CAFETTO GOLD INST 100", "Cafetto Gold instant coffee 100g", "Instant", 100, 5.49, "Y"),
    ("5391733500029", "CAF", "Cafetto", "CAFETTO GOLD INST 200", "Cafetto Gold instant coffee 200g", "Instant", 200, 9.99, "Y"),
    ("5391733500036", "CAF", "CAFETTO", "CAFETTO ORIG INST 200", "Cafetto Original instant coffee 200g", "Instant", 200, 7.49, "Y"),
    ("5391733500043", "CAF", "Cafetto", "CAFETTO CAPPUCC 8SACH", "Cafetto Cappuccino sachets x8", "Instant", 144, 3.29, "Y"),
    ("5391870200017", "WES", "Westquay", "WESTQUAY HARBOUR G250", "Westquay Harbour Blend ground coffee 250g", "Ground", 250, 6.95, "N"),
    ("5391870200024", "WES", "Westquay", "WESTQUAY ORIGIN BN250", "Westquay Single Origin beans 250g", "Beans", 250, 8.50, "N"),
    ("5391905100015", "KIN", "Kinvara Hills", "KINVARA BURREN GR227", "Kinvara Hills Burren Blend ground coffee 227g", "Ground", 227, 5.49, "Y"),
    ("5391905100022", "KIN", "KINVARA HILLS ROASTERS", "KINVARA ATLANT BN454", "Kinvara Hills Atlantic beans 454g", "Beans", 454, 9.99, "Y"),
]
SKU = {s[0]: s for s in SKUS}
SKUS_OF = {b: [s[0] for s in SKUS if s[1] == b] for b in B}
COUNTER_PLU = "2400011"
ACCESSORY_PLU = "2400028"
ADJ_PLU = "9000101"

# the coffee counter at Drumsallagh: guest roasters, their coffees, price per kg (first half, from 1 July)
ROASTERS = [("GLN", "Glenmore Roasters", [("Kiambu AA", 42.0, 44.0), ("Colombia Huila", 38.0, 39.5)]),
            ("ARD", "Ardcath Coffee Co.", [("House Espresso", 34.0, 35.0), ("Brazil Cerrado", 36.0, 36.0)]),
            ("INB", "Inish Bean", [("Ethiopia Guji", 46.0, 48.0), ("Sumatra Mandheling", 40.0, 42.0)])]
ROASTER_NAME = {r[0]: r[1] for r in ROASTERS}
PRICE_CHANGE = dt.date(2026, 7, 1)
ACCESSORIES = [("Filter papers, 100", 4.20), ("Cone dripper", 14.50), ("Reusable cup", 12.00),
               ("Cafetiere, 3 cup", 24.50), ("Hand grinder", 39.95), ("Gift box", 6.00)]
SCALE_RESET = dt.datetime(2026, 6, 22, 7, 12)           # scale 2's clock reset to 1 January 00:00 after a power cut
SCALE_FIXED = dt.datetime(2026, 7, 14, 8, 31)           # set right at the service visit, before opening
COUNTER_HOURS = (9, 18)

# the 2026 multibuy deals: id, brand, listed PLUs, mechanic price for two, start, end, funding per multibuy,
# [(effective from, funding)] revisions
DEALS = [
    ("P26-003", "HAL", ("5391127400016", "5391127400047"), 8.00, dt.date(2026, 1, 12), dt.date(2026, 2, 22), 0.57, []),
    ("P26-006", "NOR", ("5701923300017", "5701923300024", "5701923300031"), 7.00, dt.date(2026, 2, 16), dt.date(2026, 3, 29), 0.66, []),
    ("P26-009", "CAF", ("5391733500012",), 9.50, dt.date(2026, 3, 16), dt.date(2026, 4, 26), 0.71, []),
    ("P26-011", "BEL", ("5391488600014", "5391488600021"), 6.50, dt.date(2026, 2, 23), dt.date(2026, 3, 29), 0.54, []),
    ("P26-013", "ROS", ("8001477200028",), 9.00, dt.date(2026, 3, 23), dt.date(2026, 4, 26), 0.62, []),
    ("P26-017", "HAL", ("5391127400023",), 15.00, dt.date(2026, 4, 13), dt.date(2026, 5, 24), 1.13, [(dt.date(2026, 5, 4), 1.38)]),
    ("P26-019", "NOR", ("5701923300048",), 19.00, dt.date(2026, 6, 15), dt.date(2026, 7, 26), 1.24, []),
    ("P26-022", "CAF", ("5391733500036",), 13.00, dt.date(2026, 5, 18), dt.date(2026, 6, 28), 1.07, []),
    ("P26-024", "BEL", ("5391488600038",), 11.50, dt.date(2026, 6, 15), dt.date(2026, 7, 26), 0.76, []),
    ("P26-026", "ROS", ("8001477200035",), 17.00, dt.date(2026, 5, 25), dt.date(2026, 7, 5), 0.86, []),
    ("P26-031", "HAL", ("5391127400016", "5391127400047"), 8.00, dt.date(2026, 9, 14), dt.date(2026, 10, 25), 0.91, []),
    ("P26-034", "NOR", ("5701923300017", "5701923300024"), 7.00, dt.date(2026, 8, 3), dt.date(2026, 9, 13), 0.67, [(dt.date(2026, 8, 24), 0.83)]),
    ("P26-036", "CAF", ("5391733500043",), 5.50, dt.date(2026, 9, 14), dt.date(2026, 10, 25), 0.61, []),
    ("P26-038", "BEL", ("5391488600014", "5391488600021"), 6.50, dt.date(2026, 8, 24), dt.date(2026, 10, 4), 0.58, []),
    ("P26-040", "ROS", ("8001477200028",), 9.00, dt.date(2026, 9, 7), dt.date(2026, 10, 18), 0.63, []),
    ("P26-043", "HAL", ("5391127400023",), 15.00, dt.date(2026, 11, 2), dt.date(2026, 12, 13), 1.12, []),
    ("P26-045", "NOR", ("5701923300055",), 13.00, dt.date(2026, 11, 9), dt.date(2026, 12, 20), 0.96, []),
    ("P26-047", "CAF", ("5391733500029",), 18.00, dt.date(2026, 11, 16), dt.date(2026, 12, 27), 1.16, [(dt.date(2026, 11, 30), 1.31)]),
    ("P26-049", "BEL", ("5391488600038",), 11.50, dt.date(2026, 11, 23), dt.date(2026, 12, 31), 0.77, []),
    ("P26-051", "ROS", ("8001477200011",), 32.00, dt.date(2026, 11, 30), dt.date(2026, 12, 31), 1.63, []),
]

# the online shop
ONLINE_FROM = dt.date(2025, 12, 1)       # the export covers orders placed from this day

EXTRACT = dt.datetime(2027, 1, 8, 6, 30)     # the warehouse extracts pulled
BRIEF_DATE = dt.date(2027, 1, 11)
ASSEMBLED = dt.datetime(2027, 1, 13, 16, 20)
DECISION = dt.date(2027, 2, 3)

PEOPLE = {"insight": "Cal Monaghan",       # customer insight lead, the requester
          "brand": "Alix Fennell",          # Roastery brand manager, owns the sampling
          "buyer": "Katy Kinnegan"}         # coffee buyer, keeps the deal log

FILES = {
    "till": "coffee_till_lines_2026.csv",
    "online": "online_orders_2026.json",
    "register": "rewards_cards_2026.csv",
    "settle": "faircourt_settlement_2026.parquet",
    "agreement": "faircourt_merchant_agreement_2026.pdf",
    "master": "product_master_coffee.xlsx",
    "terms": "corcallys_rewards_terms_2026.pdf",
    "brief": "roastery_sampling_brief_2027.docx",
    "labels": "counter_scale_labels_2026.csv",
    "board": "coffee_counter_price_board_2026.pdf",
    "deals": "multibuy_deals_2026.xlsx",
    "census": "catchment_households_census2022.csv",
    "tracker": "coffee_brand_tracker_2026.xlsx",
}
DISTRACTORS = ("census", "tracker")
DECK = "roastery_sampling_2027.pptx"
CSV_OUT = "rival_home_overlap_2026.csv"
DELIVERABLES = (DECK, CSV_OUT)


def ist(t_utc):
    """True when a UTC datetime falls in Irish Standard Time (summer time: last Sunday of March to last Sunday of
    October, from 01:00 UTC)."""
    def last_sunday(y, m):
        d = dt.date(y, m, 31)
        return d - dt.timedelta(days=(d.weekday() + 1) % 7)
    a = dt.datetime.combine(last_sunday(t_utc.year, 3), dt.time(1))
    b = dt.datetime.combine(last_sunday(t_utc.year, 10), dt.time(1))
    return a <= t_utc < b


def to_utc(t_local):
    u = t_local - dt.timedelta(hours=1)
    return u if ist(u) else t_local


def to_local(t_utc):
    return t_utc + dt.timedelta(hours=1) if ist(t_utc) else t_utc


def quarter(d):
    return (d.month - 1) // 3 + 1


def ean13(body12):
    s = sum(int(c) * (3 if i % 2 else 1) for i, c in enumerate(body12))
    return body12 + str((10 - s % 10) % 10)


def r2(x):
    return float("%.2f" % (x + (1e-9 if x >= 0 else -1e-9)))


def _font_dir():
    for d in ("/usr/share/fonts/truetype/liberation/", os.path.expanduser("~/Library/Fonts/"), "/Library/Fonts/"):
        if os.path.exists(os.path.join(d, "LiberationSans-Regular.ttf")):
            return d
    raise FileNotFoundError("LiberationSans-Regular.ttf")


FONT_DIR = _font_dir()


def _fix_eans():
    """Every pack PLU carries a valid EAN-13 check digit."""
    global SKUS, SKU, SKUS_OF, DEALS
    fix = {s[0]: ean13(s[0][:12]) for s in SKUS}
    SKUS = [(fix[s[0]],) + tuple(s[1:]) for s in SKUS]
    SKU = {s[0]: s for s in SKUS}
    SKUS_OF = {b: [s[0] for s in SKUS if s[1] == b] for b in B}
    DEALS = [(d[0], d[1], tuple(fix[p] for p in d[2])) + tuple(d[3:]) for d in DEALS]


_fix_eans()
DEAL = {d[0]: d for d in DEALS}
