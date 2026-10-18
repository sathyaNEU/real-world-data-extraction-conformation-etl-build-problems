"""task161 world: constants, accounts, rush episodes and calendars.

Pellerin Distribution Services is an import 3PL with four port-area buildings (40,000 rack positions).
Everything here is the generator's clean truth; nothing in this module ships.
"""
import datetime as dt

SEED = 161                      # fixed by rule: the task number, never searched
AS_OF = dt.date(2026, 12, 7)    # Monday; data runs to the close of Sunday 6 December 2026
LAST_CLOSE = dt.date(2026, 12, 6)
HIST_START = dt.date(2019, 4, 1)
OLD_WMS_END = dt.date(2022, 9, 30)      # legacy WMS authoritative through this close
NEW_WMS_START = dt.date(2022, 9, 12)    # new WMS parallel run from this close (overlap 12-30 Sep)
WINDOW = [(2027, m) for m in range(1, 7)]
RACK_CAP = 40000
BLOCK = 4000
N_BLOCKS = 6
BLOCK_PRICE = 1_100_000
HURDLE = 0.75

# buildings: code (new WMS), legacy code, name, city, rack positions
BUILDINGS = [
    ("CAR1", "W1", "Del Amo", "Carson", 13200),
    ("RDZ1", "W2", "Alondra", "Rancho Dominguez", 11600),
    ("WIL1", "W3", "Anaheim Street", "Wilmington", 8400),
    ("CMP1", "W4", "Artesia", "Compton", 6800),
]
assert sum(b[4] for b in BUILDINGS) == RACK_CAP

# Shipment seasonality by category, Jan..Dec (normalised in sim to mean 1).
PROFILE = {
    "furniture":   [0.86, 0.86, 0.96, 0.97, 0.98, 0.99, 1.01, 1.07, 1.10, 1.09, 1.07, 1.04],
    "housewares":  [0.70, 0.70, 0.78, 0.80, 0.84, 0.88, 0.96, 1.12, 1.30, 1.42, 1.40, 1.10],
    "toys":        [0.52, 0.56, 0.70, 0.74, 0.80, 0.86, 0.98, 1.22, 1.48, 1.58, 1.42, 1.14],
    "electronics": [0.74, 0.72, 0.80, 0.82, 0.86, 0.90, 0.96, 1.10, 1.24, 1.34, 1.40, 1.12],
    "apparel":     [0.84, 0.94, 1.03, 1.02, 0.97, 0.92, 0.96, 1.10, 1.12, 1.06, 1.01, 0.93],
    "footwear":    [0.84, 0.95, 1.07, 1.05, 0.98, 0.94, 1.06, 1.16, 1.06, 0.98, 0.98, 0.93],
    "textiles":    [0.88, 0.89, 0.96, 0.97, 0.98, 0.99, 1.02, 1.07, 1.09, 1.07, 1.05, 1.03],
    "outdoor":     [0.80, 0.98, 1.16, 1.24, 1.22, 1.12, 0.98, 0.88, 0.82, 0.82, 0.84, 0.86],
    "pet":         [0.97, 0.95, 1.00, 0.99, 1.00, 1.00, 1.01, 1.02, 1.02, 1.03, 1.01, 1.00],
    "auto":        [0.92, 0.94, 1.02, 1.05, 1.06, 1.04, 1.02, 1.02, 0.99, 0.98, 0.98, 0.98],
    "decor":       [0.22, 0.22, 0.32, 0.42, 0.55, 0.78, 1.12, 1.74, 2.12, 2.14, 1.68, 0.88],
    "appliances":  [0.70, 0.70, 0.78, 0.80, 0.84, 0.88, 0.95, 1.10, 1.30, 1.42, 1.44, 1.09],
    "fitness":     [1.28, 1.14, 1.08, 0.99, 0.92, 0.87, 0.87, 0.89, 0.91, 0.93, 0.99, 1.13],
    "office":      [0.88, 0.90, 0.94, 0.92, 0.96, 1.15, 1.30, 1.28, 1.00, 0.92, 0.88, 0.87],
}

# Rush episodes: build window (first and last receipt day of bought-ahead stock) and the duty step date
# (first day the burn runs). Steps are real-shaped: 1 Sep 2019, 5 Apr 2025, 7 Aug 2025, 1 Jan 2027.
RUSHES = {
    "R2019":  (dt.date(2019, 6, 3),  dt.date(2019, 8, 31), dt.date(2019, 9, 1)),
    "R2025A": (dt.date(2025, 1, 6),  dt.date(2025, 4, 4),  dt.date(2025, 4, 5)),
    "R2025B": (dt.date(2025, 6, 2),  dt.date(2025, 8, 6),  dt.date(2025, 8, 7)),
    "R2026":  (dt.date(2026, 9, 1),  dt.date(2026, 12, 31), dt.date(2027, 1, 1)),
}

# Announcement dates (the build windows open on these; the broker's advisories carry them).
ANNOUNCED = {"R2019": dt.date(2019, 5, 13), "R2025A": dt.date(2025, 1, 2), "R2025B": dt.date(2025, 5, 28),
             "R2026": dt.date(2026, 8, 24)}

# Accounts. level = mean monthly pallets shipped over calendar 2026 (before noise); cover = months of
# forward shipments held as normal stock; s = share of shipments served from bought-ahead stock while
# any is left (the affected lines); g = growth a year; m = months of the affected lines' consumption
# bought ahead in each rush (0 = took no part); start/end = contract dates; ppc = pallets per 40ft box.
ACCOUNTS = {
    # code     category      level  cover  s      g      m by rush                                             start         end   ppc
    "A01": ("furniture",   3550, 1.78, 0.120, 0.030, {"R2019": 2.1, "R2025A": 2.6, "R2025B": 2.3, "R2026": 1.8},  "2019-04-01", None, 19.5),
    "A02": ("housewares",  2900, 1.25, 0.165, 0.040, {"R2019": 1.9, "R2025A": 2.4, "R2025B": 2.2, "R2026": 10.9}, "2019-04-01", None, 21.0),
    "A03": ("toys",        2350, 1.44, 0.180, 0.020, {"R2019": 2.0, "R2025A": 2.5, "R2025B": 2.4, "R2026": 11.4}, "2019-04-01", None, 23.5),
    "A04": ("electronics", 2200, 0.91, 0.145, 0.060, {"R2019": 1.8, "R2025A": 2.3, "R2025B": 2.1, "R2026": 10.4}, "2019-04-01", None, 24.0),
    "A05": ("apparel",     2650, 1.10, 0.090, 0.030, {"R2019": 2.0, "R2025A": 2.5, "R2025B": 2.2, "R2026": 1.0},  "2019-04-01", None, 22.0),
    "A06": ("footwear",    1700, 1.20, 0.110, 0.050, {"R2019": 1.9, "R2025A": 2.6, "R2025B": 2.1, "R2026": 1.2},  "2019-04-01", None, 20.5),
    "A07": ("textiles",    1900, 1.39, 0.110, 0.030, {"R2019": 2.2, "R2025A": 2.7, "R2025B": 2.4, "R2026": 1.5},  "2019-04-01", None, 21.5),
    "A08": ("outdoor",     1500, 1.63, 0.120, 0.040, {"R2019": 0.0, "R2025A": 2.6, "R2025B": 2.2, "R2026": 1.2},  "2020-03-02", None, 17.5),
    "A09": ("pet",         1800, 0.82, 0.070, 0.070, {"R2019": 1.8, "R2025A": 2.4, "R2025B": 2.0, "R2026": 0.8},  "2019-04-01", None, 22.5),
    "A10": ("auto",        1600, 1.30, 0.120, 0.030, {"R2019": 2.0, "R2025A": 2.5, "R2025B": 2.3, "R2026": 1.2},  "2019-04-01", None, 23.0),
    "A11": ("decor",        900, 2.02, 0.215, 0.020, {"R2019": 2.1, "R2025A": 2.6, "R2025B": 2.3, "R2026": 11.4}, "2019-04-01", None, 18.5),
    "A12": ("appliances",  1500, 1.10, 0.165, 0.050, {"R2019": 0.0, "R2025A": 2.4, "R2025B": 2.2, "R2026": 10.9}, "2021-05-03", None, 21.0),
    "A13": ("fitness",     1000, 1.49, 0.130, 0.040, {"R2019": 0.0, "R2025A": 2.5, "R2025B": 2.0, "R2026": 1.0},  "2023-02-06", None, 19.0),
    "A14": ("office",      1100, 1.01, 0.080, 0.020, {"R2019": 1.8, "R2025A": 2.3, "R2025B": 2.0, "R2026": 0.8},  "2019-04-01", None, 24.5),
    # former accounts (in the history, not in the book at the as-of)
    "F01": ("housewares",   950, 1.15, 0.110, 0.010, {"R2019": 1.9}, "2019-04-01", "2021-08-31", 21.0),
    "F02": ("apparel",     1250, 1.06, 0.090, 0.000, {"R2019": 2.0, "R2025A": 2.4}, "2019-04-01", "2025-10-31", 22.0),
}
CURRENT = [a for a, v in ACCOUNTS.items() if v[7] is None]

# ----------------------------------------------------------------------------------- names
COMPANY = "Pellerin Distribution Services, Inc."
COMPANY_SHORT = "Pellerin Distribution"
PARK = "Tamarind Avenue Logistics Park"
PARK_BUILDING = "Building B"
LANDLORD = "Ridley-Ames Industrial Properties"
BROKER = "Yamamoto & Vance Customs Brokers"
TRANSLOAD = "Avila Transload Services, LLC"
SUBLEASE_SITE = ("DHS1", "Dominguez sublease", "Rancho Dominguez")
PEOPLE = {
    "vp_ops": ("Mariah Norman", "Vice President, Operations"),
    "wms": ("Jerome Lam", "WMS Systems Lead"),
    "cs": ("Nicole Freeman", "Customer Service Manager"),
    "landlord": ("Brandon Page", "Leasing Manager"),
}

# account names; new WMS id; legacy mnemonic(s) (with the date a legacy code stopped, for merges)
ACCOUNT_NAMES = {
    "A01": ("Quillan Furniture Group", "PD2041", ["QUILLAN"]),
    "A02": ("Avendano Housewares Corp.", "PD2047", ["AVENDANO"]),
    "A03": ("Fanshaw Toy Co.", "PD2052", ["FANSHAW"]),
    "A04": ("KDT Mobile Accessories, Inc.", "PD2058", ["KDTMOBILE"]),
    "A05": ("Rosales Apparel Group", "PD2063", ["ROSALESB", "ROSALESK"]),
    "A06": ("Ostrander Footwear LLC", "PD2071", ["OSTRANDER"]),
    "A07": ("Ashby Linens Inc.", "PD2076", ["ASHBY"]),
    "A08": ("Coronado Patio & Garden", "PD2083", ["CORONADO"]),
    "A09": ("Bramwell Pet Supply Co.", "PD2089", ["BRAMWELL"]),
    "A10": ("Garza Auto Parts Imports", "PD2094", ["GARZAAUTO"]),
    "A11": ("Halloran Holiday Decor Co.", "PD2102", ["HALLORAN"]),
    "A12": ("Kitano Appliance USA", "PD2108", ["KITANO"]),
    "A13": ("Lockhart Fitness Imports", "PD2115", []),
    "A14": ("Penrose Office Products", "PD2121", ["PENROSE"]),
    "F01": ("Bellamy Kitchen Co.", None, ["BELLAMY"]),
    "F02": ("Hollins Apparel", "PD2066", ["HOLLINS"]),
}
# Rosales ran two legacy accounts (basics and kids) until the 2022 migration merged them into one.
ROSALES_SPLIT = 0.62   # share of the account's volume under ROSALESB in the legacy system

# home building of each account (most of its racked stock sits there)
HOME = {"A01": "CAR1", "A02": "RDZ1", "A03": "CAR1", "A04": "WIL1", "A05": "RDZ1", "A06": "CMP1",
        "A07": "CAR1", "A08": "RDZ1", "A09": "CMP1", "A10": "WIL1", "A11": "CAR1", "A12": "RDZ1",
        "A13": "WIL1", "A14": "CMP1", "F01": "RDZ1", "F02": "CMP1"}

# accounts that send part of their freight through the transload partner (53ft trailers) in 2026,
# and the share of their receipts that arrives that way
TRANSLOAD_SHARE = {"A05": 0.34, "A06": 0.28, "A09": 0.31, "A10": 0.22, "A14": 0.26}
# accounts that also bring domestic transfers in 53ft trailers from their own inland DCs (share of receipts)
DOMESTIC_SHARE = {"A01": 0.045, "A07": 0.035, "A12": 0.03}
