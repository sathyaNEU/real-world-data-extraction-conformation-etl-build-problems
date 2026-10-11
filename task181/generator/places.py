"""Merchants and terminals the credit union's members use: eastern Ontario towns, Ottawa, travel
destinations, card-not-present merchants, and the places the counterfeit cards were cashed out.

Deterministic for world.SEED. Returns plain lists of dicts; sim.py indexes them.
"""
import datetime as dt

import numpy as np

import world as W

# category: mcc, median amount, sigma, open hour, close hour, terminals (lo, hi), tap capable
CATS = {
    "grocery": ("5411", 47.0, 0.78, 7, 21, (4, 8), True),
    "pharmacy": ("5912", 23.0, 0.80, 8, 21, (2, 4), True),
    "fuel": ("5542", 61.0, 0.28, 6, 22, (6, 10), True),
    "fuelshop": ("5541", 17.0, 0.80, 6, 22, (1, 2), True),
    "restaurant": ("5812", 46.0, 0.55, 11, 22, (1, 3), True),
    "fastfood": ("5814", 13.5, 0.55, 7, 22, (1, 3), True),
    "coffee": ("5814", 6.9, 0.45, 6, 18, (1, 2), True),
    "hardware": ("5251", 41.0, 0.90, 8, 20, (1, 3), True),
    "discount": ("5310", 57.0, 0.85, 8, 21, (3, 6), True),
    "liquor": ("5921", 37.0, 0.60, 10, 21, (2, 4), True),
    "clothing": ("5651", 66.0, 0.70, 10, 20, (1, 3), True),
    "convenience": ("5499", 14.5, 0.60, 6, 23, (1, 2), True),
    "bakery": ("5462", 12.0, 0.50, 7, 18, (1, 1), True),
    "homeimprove": ("5200", 88.0, 1.00, 7, 21, (3, 5), True),
    "auto": ("7538", 205.0, 0.80, 8, 18, (1, 1), True),
    "dental": ("8021", 160.0, 0.70, 8, 17, (1, 1), True),
    "salon": ("7230", 47.0, 0.50, 9, 19, (1, 1), True),
    "pet": ("5995", 41.0, 0.70, 9, 20, (1, 2), True),
    "sporting": ("5941", 74.0, 0.90, 10, 20, (1, 2), True),
    "electronics": ("5732", 118.0, 1.00, 10, 20, (1, 2), True),
    "books": ("5942", 25.0, 0.60, 10, 20, (1, 1), True),
    "florist": ("5992", 47.0, 0.50, 9, 18, (1, 1), True),
    "carwash": ("7542", 14.0, 0.30, 7, 21, (1, 1), False),
    "atm": ("6011", 0.0, 0.0, 0, 24, (1, 2), False),
    "hotel": ("7011", 175.0, 0.45, 14, 23, (1, 2), True),
    "attraction": ("7996", 58.0, 0.60, 9, 18, (1, 3), True),
    "parking": ("7523", 9.0, 0.50, 7, 20, (1, 2), True),
}

SURNAMES = ["Brennan", "Hollister", "MacLaren", "Keogh", "Lalonde", "Dufresne", "Whitcombe", "Pritchard",
            "Ashdown", "Barrowclough", "Corrigan", "Delisle", "Ellery", "Fennimore", "Gauthier", "Halloran",
            "Inkster", "Jardine", "Kilbride", "Lightbody", "Mulcahy", "Nesbitt", "Ostrander", "Pellerin",
            "Quigley", "Rutledge", "Sangster", "Thibodeau", "Upshall", "Vanstone", "Wardrope", "Yelland",
            "Abernethy", "Bickell", "Coutts", "Dorland", "Easson", "Fairbairn", "Goodfellow", "Hepburn",
            "Ireland", "Joynt", "Kerrigan", "Lavoie", "Mabee", "Nadon", "Ogilvie", "Purdy", "Ranger",
            "Sproule", "Tackaberry", "Usher", "Vroom", "Wemyss", "Archambault", "Belanger", "Cosgrove",
            "Dowdall", "Esmonde", "Foubert", "Gilchrist", "Hagerman", "Imrie", "Kavanagh", "Leduc", "Morrow",
            "Nolan", "O'Hare", "Pilon", "Rathwell", "Shouldice", "Truax", "Villeneuve", "Wylie", "Zufelt"]
LOCAL_WORDS = ["Tay River", "Otter Creek", "Beckwith", "Jock River", "Cataraqui", "Limerick", "Kilmarnock",
               "Burritts", "Bellamy", "Glen Tay", "Ashton", "Franktown", "Toledo", "Oxford Mills",
               "Bishops Mills", "Easton", "Rideau Ferry", "Port Elmsley", "Innisville", "Ferguson Falls"]
PATTERNS = {
    "grocery": ["{s} Market", "{s} Fresh", "{s} Grocery", "{w} Food Co-op", "{s} & Sons Grocers"],
    "pharmacy": ["{s} Pharmacy", "{w} Pharmacy", "{s} Drug Store", "{s} Apothecary"],
    "fuel": ["{s} Fuels", "{w} Gas Bar", "{s} Petroleum", "{w} Fuel Stop"],
    "fuelshop": ["{s} Fuels kiosk", "{w} Gas Bar store"],
    "restaurant": ["{s} Grill", "The {s} House", "{w} Kitchen", "{s} Tavern", "{s} Bistro", "{w} Diner"],
    "fastfood": ["{s} Burger", "{s} Pizza", "{w} Shawarma", "{s} Fish & Chips", "{s} Subs", "{w} Poutinerie"],
    "coffee": ["{s} Coffee", "{w} Cafe", "{s} Roasters", "{w} Coffee House"],
    "hardware": ["{s} Hardware", "{w} Building Supply", "{s} Lumber"],
    "discount": ["{s} Dollar Plus", "{w} Discount", "{s} General Store"],
    "liquor": ["{w} Wine & Spirits", "{s} Brewing retail", "{s} Wine Shop"],
    "clothing": ["{s} Outfitters", "{w} Clothing Co.", "{s} Apparel"],
    "convenience": ["{s} Variety", "{w} Mini Mart", "{s} Convenience"],
    "bakery": ["{s} Bakery", "{w} Bake Shop"],
    "homeimprove": ["{s} Home Centre", "{w} Home & Garden"],
    "auto": ["{s} Auto Service", "{w} Tire & Auto", "{s} Motors service"],
    "dental": ["{w} Dental", "{s} Family Dentistry", "Dr {s} Dental"],
    "salon": ["{s} Hair Studio", "{w} Salon", "Studio {s}"],
    "pet": ["{w} Pet Supply", "{s} Feed & Pet"],
    "sporting": ["{w} Sports", "{s} Outdoors"],
    "electronics": ["{s} Electronics", "{w} Computers"],
    "books": ["{w} Books", "{s} Booksellers"],
    "florist": ["{s} Flowers", "{w} Florist"],
    "carwash": ["{w} Car Wash", "{s} Auto Spa"],
    "atm": ["ATM {s} Variety", "ATM {w} Gas Bar", "ATM {s} Plaza"],
    "hotel": ["{w} Inn", "{s} Suites", "{s} Lodge", "{w} Motel"],
    "attraction": ["{w} Adventure Park", "{s} Marina", "{w} Golf Club", "{s} Museum shop"],
    "parking": ["{w} Parking", "{s} Lot parking"],
}
STREETS = ["Main St", "King St", "Queen St", "Church St", "William St", "Elgin St", "Bridge St", "Mill St",
           "Water St", "Market St", "Victoria Ave", "Brock St", "Wilson St", "Bay St", "Centre St",
           "Union St", "John St", "Russell St", "Herriott St", "Lansdowne Ave", "Rideau St", "Prescott St",
           "Gore St", "Foster St", "Beckwith St", "Colborne St", "Pearl St", "Wellington St"]

# town: province/state, country, size (merchant scale), currency, kind
TOWNS = [
    ("Smiths Falls", "ON", "CA", 1.00, "home"), ("Perth", "ON", "CA", 0.75, "home"),
    ("Carleton Place", "ON", "CA", 0.80, "home"), ("Kemptville", "ON", "CA", 0.75, "home"),
    ("Merrickville", "ON", "CA", 0.40, "home"), ("Brockville", "ON", "CA", 1.00, "home"),
    ("Kingston", "ON", "CA", 1.60, "home"), ("Ottawa", "ON", "CA", 3.20, "city"),
    ("Almonte", "ON", "CA", 0.30, "near"), ("Prescott", "ON", "CA", 0.30, "near"),
    ("Gananoque", "ON", "CA", 0.30, "near"), ("Westport", "ON", "CA", 0.20, "near"),
    ("Lanark", "ON", "CA", 0.15, "near"), ("Napanee", "ON", "CA", 0.30, "near"),
]
# travel destinations: (town, prov/state, country, merchants)
DESTINATIONS = [
    ("Montreal", "QC", "CA", 34), ("Quebec", "QC", "CA", 22), ("Mont-Tremblant", "QC", "CA", 18),
    ("Gatineau", "QC", "CA", 14), ("Halifax", "NS", "CA", 20), ("Moncton", "NB", "CA", 12),
    ("Charlottetown", "PE", "CA", 14), ("Toronto", "ON", "CA", 30), ("Niagara Falls", "ON", "CA", 18),
    ("Watertown", "NY", "US", 16), ("Ogdensburg", "NY", "US", 10), ("Lake Placid", "NY", "US", 18),
    ("Plattsburgh", "NY", "US", 14), ("Syracuse", "NY", "US", 16), ("Burlington", "VT", "US", 16),
    ("Old Orchard Beach", "ME", "US", 16), ("Kissimmee", "FL", "US", 20), ("Myrtle Beach", "SC", "US", 18),
    ("Cape May", "NJ", "US", 12), ("Erie", "PA", "US", 12),
]
TRAVEL_CATS = ["hotel", "restaurant", "fastfood", "fuel", "grocery", "attraction", "coffee", "pharmacy",
               "convenience", "parking", "clothing"]

CNP = [  # name, mcc, city, prov/state, country, kind
    ("Northwind Streaming", "4899", "Toronto", "ON", "CA", "sub"),
    ("Maplecell Wireless", "4814", "Toronto", "ON", "CA", "bill"),
    ("Eastern Ontario Hydro billing", "4900", "Smiths Falls", "ON", "CA", "bill"),
    ("Canuck Online Retail", "5999", "Vancouver", "BC", "CA", "shop"),
    ("Rideau Valley Internet", "4816", "Perth", "ON", "CA", "bill"),
    ("Brightline Home Insurance", "6300", "Toronto", "ON", "CA", "bill"),
    ("Parcelly Marketplace", "5399", "Montreal", "QC", "CA", "shop"),
    ("TrueNorth Air", "3000", "Toronto", "ON", "CA", "travel"),
    ("Laurentian Rail tickets", "4112", "Montreal", "QC", "CA", "travel"),
    ("Gridiron Sports Streaming", "4899", "Toronto", "ON", "CA", "sub"),
    ("Kitchenbox Meal Kits", "5499", "Toronto", "ON", "CA", "shop"),
    ("Sterling Pet Online", "5995", "Calgary", "AB", "CA", "shop"),
    ("Pinecrest Pharmacy online", "5912", "Toronto", "ON", "CA", "shop"),
    ("Harbourline Ferries", "4111", "Halifax", "NS", "CA", "travel"),
    ("Bookshelf Digital", "5815", "Toronto", "ON", "CA", "sub"),
    ("Quickcart Delivery", "5814", "Toronto", "ON", "CA", "shop"),
    ("Lakeshore Hotels online", "7011", "Toronto", "ON", "CA", "travel"),
    ("Trailhead Gear online", "5941", "Ottawa", "ON", "CA", "shop"),
    ("Cloudstack Software", "5734", "Seattle", "WA", "US", "sub"),
    ("Gamebox Online", "5816", "Redmond", "WA", "US", "shop"),
    ("Townsite Municipal payments", "9399", "Kemptville", "ON", "CA", "bill"),
    ("Ontario Lakes Camping reservations", "7033", "Peterborough", "ON", "CA", "travel"),
]

# counterfeit cash-out places: (name, category, street, town, prov/state, country)
CASHOUT = [
    ("ATM Depanneur Saint-Denis", "atm", "4120 Rue Saint-Denis", "Montreal", "QC", "CA"),
    ("ATM Marche Jean-Talon Express", "atm", "7015 Rue Saint-Dominique", "Montreal", "QC", "CA"),
    ("ATM Station Berri variety", "atm", "1580 Rue Berri", "Montreal", "QC", "CA"),
    ("Electro Plus Cote-des-Neiges", "electronics", "5745 Ch de la Cote-des-Neiges", "Montreal", "QC", "CA"),
    ("ATM Dundas West Convenience", "atm", "1312 Dundas St W", "Toronto", "ON", "CA"),
    ("ATM Yonge Street Variety", "atm", "2210 Yonge St", "Toronto", "ON", "CA"),
    ("Spadina Electronics Outlet", "electronics", "388 Spadina Ave", "Toronto", "ON", "CA"),
    ("ATM 8th Ave Deli", "atm", "512 8th Ave", "New York", "NY", "US"),
    ("ATM Broadway Food Mart", "atm", "2874 Broadway", "New York", "NY", "US"),
    ("ATM Canal St Smoke Shop", "atm", "301 Canal St", "New York", "NY", "US"),
    ("Midtown Wireless & Electronics", "electronics", "47 W 34th St", "New York", "NY", "US"),
    ("ATM Ferry St Liquors", "atm", "214 Ferry St", "Newark", "NJ", "US"),
    ("ATM Market St Grocery", "atm", "88 Market St", "Newark", "NJ", "US"),
    ("ATM Journal Square Deli", "atm", "2860 John F Kennedy Blvd", "Jersey City", "NJ", "US"),
    ("ATM Elizabeth Ave Mini Mart", "atm", "1150 Elizabeth Ave", "Elizabeth", "NJ", "US"),
    ("Route 1 Gift & Phone", "electronics", "605 US Route 1", "Elizabeth", "NJ", "US"),
    ("Newport Pharmacy & Gifts", "pharmacy", "30 Mall Dr W", "Jersey City", "NJ", "US"),
]


class Catalog:
    """merchants: list of dict; terminals: list of dict (one per physical terminal position).
    A terminal position can carry several terminal IDs over time (tid_history)."""

    def __init__(self):
        self.merchants = []
        self.terminals = []
        self.by_town_cat = {}
        self._mid = set()
        self._tid = set()
        self.rng = np.random.default_rng(W.SEED + 101)
        self._used_names = set()

    # identifiers ---------------------------------------------------------------------------------
    def new_mid(self, acq):
        pre = {"A": "4450", "B": "5301", "C": "8820", "U": "7311"}[acq]
        while True:
            m = pre + "%011d" % int(self.rng.integers(0, 10 ** 11))
            if m not in self._mid:
                self._mid.add(m)
                return m

    def new_tid(self, acq):
        while True:
            if acq == "A":
                t = "%08d" % int(self.rng.integers(20_000_000, 29_999_999))
            elif acq == "B":
                t = "LT%06d" % int(self.rng.integers(100_000, 999_999))
            elif acq == "C":
                t = "%08d" % int(self.rng.integers(0, 2_999_999))       # leading zeros
            else:
                t = "%08d" % int(self.rng.integers(60_000_000, 89_999_999))
            if t not in self._tid:
                self._tid.add(t)
                return t

    def name_for(self, cat):
        for _ in range(200):
            pat = PATTERNS[cat][int(self.rng.integers(0, len(PATTERNS[cat])))]
            nm = pat.format(s=SURNAMES[int(self.rng.integers(0, len(SURNAMES)))],
                            w=LOCAL_WORDS[int(self.rng.integers(0, len(LOCAL_WORDS)))])
            if nm not in self._used_names:
                self._used_names.add(nm)
                return nm
        raise RuntimeError("names exhausted for " + cat)

    def address(self):
        return "%d %s" % (int(self.rng.integers(2, 1400)), STREETS[int(self.rng.integers(0, len(STREETS)))])

    # building ------------------------------------------------------------------------------------
    def add_merchant(self, name, cat, town, prov, country, address=None, mcc=None, acq=None,
                     n_term=None, tap=None, role=None, insert_only=()):
        spec = CATS.get(cat)
        acq = acq or ("U" if country == "US" else ["A", "B", "C"][int(self.rng.integers(0, 3))])
        m = {"idx": len(self.merchants), "merchant_id": self.new_mid(acq), "name": name, "cat": cat,
             "mcc": mcc or spec[0], "address": address or self.address(), "town": town, "prov": prov,
             "country": country, "currency": "840" if country == "US" else "124", "acq": acq,
             "role": role or "ordinary", "terminals": []}
        if n_term is None:
            lo, hi = spec[5]
            n_term = int(self.rng.integers(lo, hi + 1))
        tap_ok = (spec[6] if spec else False) if tap is None else tap
        for k in range(n_term):
            t = {"idx": len(self.terminals), "merchant": m["idx"], "pos": k + 1,
                 "tap": tap_ok and (k + 1) not in insert_only, "tid_history": [(None, self.new_tid(acq))]}
            self.terminals.append(t)
            m["terminals"].append(t["idx"])
        if cat == "atm":
            m["surcharge"] = 0.0 if role == "branch_atm" else round(float(self.rng.choice([2.5, 2.75, 3.0, 3.25, 3.5])), 2)
        self.merchants.append(m)
        self.by_town_cat.setdefault((town, cat), []).append(m["idx"])
        return m

    def retid(self, term_idx, from_date):
        t = self.terminals[term_idx]
        acq = self.merchants[t["merchant"]]["acq"]
        t["tid_history"].append((from_date, self.new_tid(acq)))


def town_counts(size, kind):
    base = {"grocery": 4, "pharmacy": 3, "fuel": 3, "fuelshop": 2, "restaurant": 9, "fastfood": 8, "coffee": 5,
            "hardware": 2, "discount": 2, "liquor": 2, "clothing": 4, "convenience": 4, "bakery": 2,
            "homeimprove": 1, "auto": 3, "dental": 3, "salon": 4, "pet": 1, "sporting": 1, "electronics": 1,
            "books": 1, "florist": 1, "carwash": 1, "atm": 3}
    out = {}
    for c, n in base.items():
        k = n * size
        if kind == "near":
            k = n * size * 0.9
        if kind == "city" and c in ("restaurant", "fastfood", "coffee", "clothing", "parking"):
            k = n * size * 1.6
        out[c] = max(1, int(round(k)))
    if kind == "city":
        out["parking"] = 8
        out["hotel"] = 4
    if kind == "home" and size >= 1.0:
        out["parking"] = 1
    return out


def build_catalog():
    cat = Catalog()
    rng = cat.rng
    # the credit union's own branch ATMs
    for town, _, addr in W.BRANCHES:
        cat.add_merchant("Larchmere Credit Union ATM " + town, "atm", town, "ON", "CA", address=addr,
                         acq="A", n_term=2 if town in ("Smiths Falls", "Kingston", "Brockville") else 1,
                         role="branch_atm")
    for town, prov, country, size, kind in TOWNS:
        for c, n in town_counts(size, kind).items():
            for _ in range(n):
                cat.add_merchant(cat.name_for(c), c, town, prov, country)
    # the plaza at Highway 416 exit 34 (one address, three merchant IDs)
    plaza_addr = "1845 County Road 43"
    fuel = cat.add_merchant("Ferrier Creek Travel Plaza fuel", "fuel", "Kemptville", "ON", "CA",
                            address=plaza_addr, acq="B", n_term=8, insert_only=(6,), role="plaza_fuel")
    coffee = cat.add_merchant("Ferrier Creek Travel Plaza coffee counter", "coffee", "Kemptville", "ON", "CA",
                              address=plaza_addr, acq="B", n_term=1, role="plaza_coffee")
    wash = cat.add_merchant("Ferrier Creek Travel Plaza car wash", "carwash", "Kemptville", "ON", "CA",
                            address=plaza_addr, acq="B", n_term=1, role="plaza_wash")
    # Lombard Market, Smiths Falls: staffed lanes 1-4, self-checkout 1-6 (terminal positions 5..10)
    lombard = cat.add_merchant("Lombard Market", "grocery", "Smiths Falls", "ON", "CA", address="210 Lombard St",
                               acq="C", n_term=10, role="lombard")
    # travel destinations
    for town, prov, country, n in DESTINATIONS:
        for k in range(n):
            c = TRAVEL_CATS[k % len(TRAVEL_CATS)] if k < len(TRAVEL_CATS) else \
                TRAVEL_CATS[int(rng.integers(0, len(TRAVEL_CATS)))]
            cat.add_merchant(cat.name_for(c), c, town, prov, country)
        cat.add_merchant(cat.name_for("atm"), "atm", town, prov, country)
    # card-not-present merchants
    for name, mcc, town, prov, country, kind in CNP:
        m = cat.add_merchant(name, "cnp", town, prov, country, mcc=mcc, n_term=0,
                             acq="U" if country == "US" else "A", role="cnp_" + kind)
        m["cnp_kind"] = kind
    # cash-out places
    for name, c, street, town, prov, country in CASHOUT:
        cat.add_merchant(name, c, town, prov, country, address=street, n_term=1 if c == "atm" else 2,
                         role="cashout")
    # routine terminal replacements across the period (about 3 per cent of positions)
    for t in cat.terminals:
        m = cat.merchants[t["merchant"]]
        if m["role"] in ("plaza_fuel", "lombard", "cashout", "branch_atm") or m["country"] != "CA":
            continue
        if rng.random() < 0.03:
            d = dt.date(2026, 6, 8) + dt.timedelta(int(rng.integers(0, 110)))
            cat.retid(t["idx"], d)
    # the plaza's OPT 6 is re-terminalled after its reader is replaced; Lombard's self-checkout pads
    cat.retid(fuel["terminals"][5], W.PUMP_OUT_OF_SERVICE + dt.timedelta(1))
    for pos in range(4, 10):
        cat.retid(lombard["terminals"][pos], W.SCO_NEW_TIDS)
    cat.fuel, cat.coffee, cat.wash, cat.lombard = fuel, coffee, wash, lombard
    return cat

