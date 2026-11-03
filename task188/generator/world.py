"""The world behind task188's pack: Harlow Reach Credit Union's cash-intensive business members in 2026.

Each member trades every day it is open. Its walk-in customers pay cash or card at the counter; card sales
settle into its account through its acquirer; delivery-platform orders are paid online and settle weekly.
Cash is banked as takings, less what the business keeps for floats and small purchases. Two members are
fronts: their owners pay criminal cash into the account with the takings, and the network behind them
pays the account and is paid from it as business customers and suppliers.

Everything here is the clean truth. pack.py writes the shipped files from it; golden.py recomputes every
graded figure from the shipped files alone.
"""
import datetime as dt
import math

import numpy as np

import common as C

# ---------------------------------------------------------------------------------------------------------
# Branches, ATMs and night depositories

BRANCHES = [
    # transit, name, municipality, street address, counts its own night deposits, opened, closed
    ("10342", "Newton", "Surrey", "7184 King George Blvd", False, dt.date(1987, 5, 4), None),
    ("10587", "Guildford", "Surrey", "15177 104 Ave", True, dt.date(1993, 9, 13), None),
    ("10611", "Richmond Centre", "Richmond", "6551 No. 3 Rd, Unit 1840", False, dt.date(1998, 3, 2), None),
    ("10729", "Metrotown", "Burnaby", "4720 Kingsway, Suite 210", True, dt.date(2001, 11, 19), None),
    ("10856", "Coquitlam Centre", "Coquitlam", "2929 Barnet Hwy, Unit 1020", False, dt.date(2004, 6, 7), None),
    ("10903", "Uptown New Westminster", "New Westminster", "601 Sixth St", False, dt.date(2006, 2, 20), None),
    ("11021", "Langley City", "Langley", "20475 Fraser Hwy", False, dt.date(2009, 8, 31), dt.date(2026, 6, 26)),
    ("11168", "Ladner Village", "Delta", "4857 Delta St", True, dt.date(2012, 4, 16), None),
    ("11204", "Willowbrook", "Langley", "19705 Fraser Hwy, Unit 108", False, dt.date(2026, 6, 29), None),
]
CASH_CENTRE = ("19004", "Regional Cash Services", "Delta", "1325 Cliveden Ave, Annacis Island")
BR = {b[0]: b for b in BRANCHES}
HOME_WEIGHTS = {"10342": 0.17, "10587": 0.13, "10611": 0.16, "10729": 0.14, "10856": 0.11,
                "10903": 0.09, "11021": 0.11, "11168": 0.09}
LANGLEY_OLD, LANGLEY_NEW = "11021", "11204"

TRADES = [
    # code, register text, members, walk-in cash share, sd, platform share, sd, median annual sales,
    # chance of business customers, chance of a second account
    ("RFS", "Restaurant - full service", 60, 0.160, 0.030, 0.10, 0.04, 1_100_000, 0.30, 0.25),
    ("RQS", "Restaurant - quick service / takeout", 56, 0.300, 0.040, 0.30, 0.07, 620_000, 0.12, 0.20),
    ("CAF", "Cafe / bakery", 44, 0.220, 0.035, 0.05, 0.03, 420_000, 0.25, 0.15),
    ("CNV", "Convenience store", 52, 0.330, 0.040, 0.00, 0.00, 840_000, 0.04, 0.20),
    ("GRO", "Grocery / specialty food", 48, 0.300, 0.040, 0.03, 0.02, 1_300_000, 0.40, 0.30),
    ("BAR", "Bar / pub", 28, 0.180, 0.030, 0.00, 0.00, 850_000, 0.15, 0.25),
    ("SAL", "Hair / nail / beauty salon", 48, 0.280, 0.040, 0.00, 0.00, 300_000, 0.04, 0.10),
    ("CWS", "Car wash", 22, 0.400, 0.045, 0.00, 0.00, 400_000, 0.45, 0.25),
    ("LDY", "Laundromat / dry cleaner", 20, 0.480, 0.045, 0.00, 0.00, 220_000, 0.30, 0.15),
    ("MFV", "Mobile food vendor", 18, 0.340, 0.040, 0.10, 0.04, 260_000, 0.40, 0.10),
]
TRADE = {t[0]: t for t in TRADES}

# Monthly trading profiles, January first.
SEASON = {
    "RFS": [0.86, 0.90, 0.96, 0.98, 1.00, 1.02, 1.06, 1.06, 0.98, 0.98, 0.98, 1.22],
    "RQS": [0.92, 0.93, 0.98, 1.00, 1.02, 1.03, 1.05, 1.04, 0.99, 0.99, 0.98, 1.07],
    "CAF": [0.92, 0.95, 1.00, 1.01, 1.03, 1.02, 1.00, 0.98, 1.02, 1.02, 0.98, 1.07],
    "CNV": [0.94, 0.93, 0.98, 1.00, 1.03, 1.05, 1.08, 1.07, 1.00, 0.98, 0.96, 0.98],
    "GRO": [0.95, 0.92, 0.98, 1.00, 1.01, 1.00, 1.02, 1.02, 0.99, 1.02, 1.00, 1.09],
    "BAR": [0.85, 0.90, 1.02, 0.96, 1.00, 1.06, 1.10, 1.08, 0.98, 0.97, 0.94, 1.14],
    "SAL": [0.88, 0.92, 0.98, 1.00, 1.04, 1.06, 1.00, 0.98, 1.00, 1.00, 1.02, 1.12],
    "CWS": [0.78, 0.82, 0.95, 1.04, 1.12, 1.16, 1.18, 1.14, 1.02, 0.94, 0.88, 0.97],
    "LDY": [1.05, 1.02, 1.00, 0.98, 0.98, 0.98, 0.97, 0.97, 0.99, 1.01, 1.02, 1.03],
    "MFV": [0.62, 0.66, 0.84, 1.00, 1.18, 1.32, 1.40, 1.36, 1.10, 0.92, 0.80, 0.80],
}
# Day-of-week profiles, Monday first; a zero is a day the business does not open.
DOW = {
    "RFS": [0.78, 0.84, 0.90, 0.98, 1.22, 1.34, 0.94],
    "RQS": [0.90, 0.92, 0.94, 1.00, 1.14, 1.12, 0.98],
    "CAF": [1.06, 1.04, 1.04, 1.04, 1.06, 0.96, 0.80],
    "CNV": [0.96, 0.95, 0.96, 0.98, 1.06, 1.06, 1.03],
    "GRO": [0.92, 0.90, 0.94, 0.98, 1.06, 1.16, 1.04],
    "BAR": [0.62, 0.70, 0.82, 1.00, 1.42, 1.52, 0.92],
    "SAL": [0.00, 0.90, 0.98, 1.08, 1.18, 1.34, 0.00],
    "CWS": [0.84, 0.86, 0.88, 0.92, 1.04, 1.34, 1.12],
    "LDY": [0.98, 0.94, 0.94, 0.96, 0.98, 1.10, 1.10],
    "MFV": [0.00, 0.84, 0.90, 0.98, 1.16, 1.34, 1.08],
}

ACQUIRERS = {
    # name, settlement lag in business days, blended discount fee
    "CASCADIA": ("Cascadia Merchant Services", 1, 0.0247),
    "NORTHGATE": ("Northgate Payments", 2, 0.0271),
}
PLATFORMS = {
    "DASHDROP": ("DashDrop Canada", 1, 0.270),   # pays on Tuesday for the Monday-Sunday week before
    "PLATEPASS": ("PlatePass Delivery", 3, 0.250),  # pays on Thursday
}

# ---------------------------------------------------------------------------------------------------------
# Names

PLACES = ["Fraser", "Kingsway", "Cedar", "Harbour", "Seaview", "Mountainview", "Riverside", "Parkway",
          "Westside", "Lakeview", "Hillcrest", "Brookside", "Meadow", "Pinecrest", "Bayside", "Sunset",
          "Highland", "Oakridge", "Willow", "Maple", "Granville", "Panorama", "Clayton", "Sullivan",
          "Steveston", "Brentwood", "Edmonds", "Sapperton", "Whalley", "Fleetwood", "Tsawwassen",
          "Murrayville", "Walnut Grove", "Queensborough", "Cloverdale", "Heritage", "Columbia", "Royal Oak",
          "Port Mann", "Annieville", "Boundary", "Lougheed", "Burquitlam", "Cariboo"]
ADJ = ["Golden", "Bright", "Lucky", "Happy", "Little", "Royal", "Fresh", "Silver", "Blue", "Green",
       "Red", "Urban", "Classic", "Modern", "Sunny", "Grand", "Prime", "True", "Wild", "Bold", "Gentle",
       "Northern", "Coastal", "Rustic", "Velvet", "Crystal", "Amber", "Jade", "Ivory", "Scarlet"]
SURN = ["Nguyen", "Singh", "Patel", "Chen", "Kim", "Sandhu", "Gill", "Wong", "Lee", "Park", "Tran",
        "Dhillon", "Grewal", "Lam", "Ho", "Romano", "Costa", "Murray", "Fraser", "Bains", "Sidhu",
        "Petrov", "Haddad", "Rahman", "Okafor", "Mendes", "Kowalski", "Novak", "Brar", "Johal",
        "Sahota", "Rossi", "Lindqvist", "Moreau", "Tanaka", "Yamada", "Ibrahim", "Karimi", "Duarte"]
CUISINE = ["Szechuan", "Punjabi", "Thai", "Greek", "Korean", "Vietnamese", "Lebanese", "Italian",
           "Mexican", "Filipino", "Persian", "Cantonese", "Japanese", "Ethiopian", "Portuguese",
           "Malaysian", "Peruvian", "Turkish", "Hakka", "Goan"]

TEMPLATES = {
    "RFS": ["{p} {c} Kitchen", "The {a} {n}", "{s}'s Bistro", "{c} House", "{p} Grill & Bar",
            "{a} Lotus Restaurant", "{s} Family Restaurant", "{c} Garden", "Taverna {s}", "{p} Dining Room"],
    "RQS": ["{p} Pizza & Donair", "{a} Pho", "{s}'s Burgers", "{p} Shawarma", "{c} Express",
            "{a} Wok", "{p} Fish & Chips", "{a} Taco Shop", "{s} Roti Hut", "{p} Sub Shop"],
    "CAF": ["{a} Bean Cafe", "{p} Bakehouse", "{s} Patisserie", "Cafe {p}", "{a} Cup Coffee",
            "{p} Bagel Co", "{s}'s Bakery", "{a} Crumb Bakery"],
    "CNV": ["{p} Convenience", "{a} Corner Store", "{p} Mini Mart", "{s} Convenience", "{a} 7 Days Market",
            "{p} Food Mart", "{a} Quick Stop"],
    "GRO": ["{p} Fresh Market", "{c} Grocery", "{a} Farm Market", "{s} Foods", "{p} Supermarket",
            "{c} Spice & Grocery", "{a} Harvest Produce"],
    "BAR": ["The {a} Fox Pub", "{p} Taphouse", "{s}'s Lounge", "The {p} Arms", "{a} Barrel Alehouse",
            "{p} Social House"],
    "SAL": ["{a} Nail Studio", "{s} Hair Design", "{p} Beauty Bar", "{a} Nails & Spa", "Studio {s}",
            "{p} Barbers", "{a} Lash & Brow", "{s} Salon"],
    "CWS": ["{a} Car Wash", "{p} Auto Spa", "{p} Wash & Detail", "{a} Touchless Wash", "{s} Auto Wash"],
    "LDY": ["{p} Coin Laundry", "{a} Cleaners", "{p} Laundromat", "{s} Dry Cleaning", "{a} Suds Laundry"],
    "MFV": ["{a} Wheels Food Truck", "{p} Street Eats", "{s}'s Kitchen on Wheels", "{a} Bowl Truck"],
}
LEGAL_SUFFIX = ["Ltd.", "Inc.", "Enterprises Ltd.", "Holdings Inc.", "Ventures Ltd.", "Corp."]

SPECIAL = {
    # role: (trade, operating name, legal name, home transit)
    "front_a": ("RQS", "Pacifica Donair & Pizza", "1287446 B.C. Ltd.", "10342"),
    "front_b": ("GRO", "Seaview Specialty Foods", "1311908 B.C. Ltd.", "10611"),
    "stale_k": ("RFS", "Kingsway Pho House", "Kingsway Pho House Ltd.", "10729"),
    "stale_s": ("CWS", "Bright Spark Car Wash", "Bright Spark Auto Services Inc.", "10856"),
    "near_n": ("GRO", "Sunrise Fresh Market", "Sunrise Fresh Market (Guildford) Ltd.", "10587"),
}

BUSINESS_CUSTOMERS = ["Tidewater Logistics", "Cascade Film Services", "Northbank Property Management",
                      "Harbourline Events", "Summit Fleet Services", "Riverstone Construction",
                      "Pacific Gateway Seniors Living", "Westbay Medical Clinic", "Fraserview School District Catering",
                      "Ironwood Builders", "Crescent Hotel Group", "Coastal Rideshare Fleet", "Blue Heron Daycare",
                      "Lynnwood Office Park", "Granite Peak Developments", "Seastar Charters", "Kinross Community Centre",
                      "Arbutus Dental Group", "Orca Courier", "Milestone Sports Club", "Elgin Retirement Residence",
                      "Bridgeport Industrial", "Alder Creek Golf Club", "Pemberton Film Studios", "Coho Marine Supply"]
NETWORK_IN = {"front_a": ["Meridian Events Ltd", "Coastline Hospitality Grp"],
              "front_b": ["Aurelia Hospitality Group", "Brightwell Catering Co"]}
NETWORK_OUT = {"front_a": ["Westgate Trading Inc", "Harrow Imports Ltd", "Lionsgate Food Supply"],
               "front_b": ["Pinnacle Wholesale Ltd", "Eastport Commodities", "Kestrel Supply Co"]}
SUPPLIERS = {
    "RFS": ["Fraserfresh Foods", "Pacific Rim Produce", "Harbour Seafood Co", "Valley Meats", "Coastal Beverage Dist"],
    "RQS": ["Fraserfresh Foods", "Valley Meats", "Pacific Rim Produce", "Mainland Paper Supply", "Coastal Beverage Dist"],
    "CAF": ["Northwind Coffee Roasters", "Valley Dairy", "Fraserfresh Foods", "Mainland Paper Supply"],
    "CNV": ["Westcoast Tobacco & Confectionery", "Coastal Beverage Dist", "Valley Dairy", "Metro Snack Distributors"],
    "GRO": ["Pacific Rim Produce", "Orient Import Supply", "Valley Dairy", "Fraserfresh Foods", "Harbour Seafood Co"],
    "BAR": ["Coastal Beverage Dist", "Liquor Distribution Warehouse", "Fraserfresh Foods", "Mainland Paper Supply"],
    "SAL": ["Salonpro Supply", "Lumina Beauty Wholesale", "Mainland Paper Supply"],
    "CWS": ["Clearwater Chemicals", "Aquamatic Equipment Service", "Mainland Paper Supply"],
    "LDY": ["Clearwater Chemicals", "Dryline Equipment Service", "Mainland Paper Supply"],
    "MFV": ["Fraserfresh Foods", "Valley Meats", "Propane West", "Mainland Paper Supply"],
}
LANDLORDS = ["Kingsgate Properties Ltd", "Riverside Plaza Holdings", "Lansdowne Commercial Inc",
             "Metro Strata Leasing", "Fraserview Realty Corp", "Hillcrest Centre Ltd", "Oakridge Retail Holdings",
             "Brentwood Commercial REIT", "Panorama Plaza Inc", "Clayton Village Properties"]


class Member:
    pass


def _rid(rng, used, lo, hi):
    while True:
        v = int(rng.integers(lo, hi))
        if v not in used:
            used.add(v)
            return v


def _name(rng, trade, used):
    for _ in range(200):
        t = TEMPLATES[trade][int(rng.integers(len(TEMPLATES[trade])))]
        s = t.format(p=PLACES[int(rng.integers(len(PLACES)))], a=ADJ[int(rng.integers(len(ADJ)))],
                     s=SURN[int(rng.integers(len(SURN)))], c=CUISINE[int(rng.integers(len(CUISINE)))],
                     n=["Table", "Spoon", "Olive", "Hearth", "Plate", "Copper Pot", "Fig"][int(rng.integers(7))])
        if s not in used:
            used.add(s)
            return s
    raise RuntimeError("names exhausted")


def _legal(rng, op, used_nums):
    if rng.random() < 0.38:
        return "%d B.C. Ltd." % _rid(rng, used_nums, 1_040_000, 1_399_999)
    core = op.replace("'s", "s").replace("&", "and")
    return "%s %s" % (core, LEGAL_SUFFIX[int(rng.integers(len(LEGAL_SUFFIX)))])


def build(seed=C.SEED):
    rng = np.random.default_rng(seed)
    used_ids, used_names, used_nums, used_acct = set(), set(), set(), set()
    for v in SPECIAL.values():
        used_names.add(v[1])
    members = []
    homes = list(HOME_WEIGHTS)
    hw = np.array([HOME_WEIGHTS[h] for h in homes])
    hw = hw / hw.sum()
    # the specials take one slot in their trade's count
    special_by_trade = {}
    for role, v in SPECIAL.items():
        special_by_trade.setdefault(v[0], []).append(role)
    for code, text, n, s_mu, s_sd, p_mu, p_sd, med, p_b2b, p_two in TRADES:
        roles = special_by_trade.get(code, [])
        for j in range(n):
            m = Member()
            m.role = roles[j] if j < len(roles) else "honest"
            m.trade = code
            m.number = _rid(rng, used_ids, 2_100_000, 6_899_999)
            if m.role != "honest":
                _, m.op_name, m.legal_name, m.home = SPECIAL[m.role]
            else:
                m.op_name = _name(rng, code, used_names)
                m.legal_name = _legal(rng, m.op_name, used_nums)
                m.home = homes[int(rng.choice(len(homes), p=hw))]
            m.sales = med * math.exp(rng.normal(0, 0.50))
            m.s = float(np.clip(s_mu + rng.normal(0, s_sd), 0.05, 0.80))
            m.p = float(np.clip(p_mu + rng.normal(0, p_sd), 0.0, 0.65)) if p_mu > 0 else 0.0
            m.retain = float(rng.beta(3, 30))
            m.growth = float(np.clip(math.exp(rng.normal(0.22, 0.30)), 0.75, 2.40))
            m.since = dt.date(2008, 1, 1) + dt.timedelta(days=int(rng.integers(0, 6200)))
            m.acquirer = "CASCADIA" if rng.random() < 0.58 else "NORTHGATE"
            m.mid = ("%04d-%03d-%03d" % (rng.integers(1000, 9999), rng.integers(0, 999), rng.integers(0, 999))
                     if m.acquirer == "CASCADIA" else "MID%08d" % rng.integers(1_000_000, 99_999_999))
            m.platforms = []
            if m.p > 0:
                m.platforms = ["DASHDROP"] if rng.random() < 0.45 else (
                    ["PLATEPASS"] if rng.random() < 0.4 else ["DASHDROP", "PLATEPASS"])
            m.dep_freq = str(rng.choice(["daily", "mwf", "twice", "weekly"], p=[0.30, 0.30, 0.22, 0.18]))
            m.ch_counter = float(rng.uniform(0.15, 0.75))
            m.ch_night = float(rng.uniform(0.0, 0.5)) * (1 - m.ch_counter)
            m.ch_atm = 1 - m.ch_counter - m.ch_night
            m.drop_elsewhere = float(rng.uniform(0.0, 0.25))
            m.b2b = []
            if rng.random() < p_b2b:
                k = int(rng.integers(1, 4))
                names = list(rng.choice(BUSINESS_CUSTOMERS, size=k, replace=False))
                share = float(rng.uniform(0.04, 0.45))
                if code == "GRO" and rng.random() < 0.40:
                    share = float(rng.uniform(0.8, 2.2))   # importers that sell mostly to restaurants
                for nm in names:
                    m.b2b.append((str(nm), share / k, "cheque" if rng.random() < 0.35 else "eft",
                                  int(rng.integers(1, 28))))
            m.loan = None
            if rng.random() < 0.18:
                m.loan = (dt.date(2026, 1, 1) + dt.timedelta(days=int(rng.integers(20, 330))),
                          round(float(m.sales * rng.uniform(0.05, 0.35)), -2))
            m.owner_inj = float(m.sales * rng.choice([0, 0, 0.01, 0.03, 0.08], p=[0.45, 0.2, 0.15, 0.12, 0.08]))
            m.two_accounts = rng.random() < p_two
            m.second_cash_share = float(rng.uniform(0.15, 0.45)) if m.two_accounts else 0.0
            m.launder = 0.0
            m.network_in = 0.0
            members.append(m)
    by_role = {m.role: m for m in members if m.role != "honest"}
    _shape_specials(by_role)
    # accounts and products
    for m in members:
        m.accounts = [_acct(rng, used_acct, m.home)]
        if m.two_accounts:
            m.accounts.append(_acct(rng, used_acct, m.home))
        if m.home == LANGLEY_OLD:
            m.acct_transit = LANGLEY_OLD
    return members, by_role, rng


def _acct(rng, used, transit):
    while True:
        v = "%s-%07d" % (transit, int(rng.integers(1_000_000, 9_999_999)))
        if v not in used:
            used.add(v)
            return v


def _shape_specials(r):
    """The five members the design note names, set on the quantities their rungs turn on."""
    a = r["front_a"]
    a.sales = 640_000.0
    a.s, a.p, a.retain = 0.300, 0.580, 0.080
    a.platforms = ["DASHDROP", "PLATEPASS"]
    a.acquirer, a.mid = "CASCADIA", "4458-221-907"
    a.growth, a.since = 1.05, dt.date(2023, 2, 14)
    a.dep_freq, a.ch_counter, a.ch_night, a.ch_atm = "daily", 0.40, 0.35, 0.25
    a.drop_elsewhere = 0.06
    a.b2b = []
    a.two_accounts, a.second_cash_share = True, 0.30
    a.loan, a.owner_inj = None, 0.0
    a.launder = 225_700.0
    a.network_in = 610_000.0
    b = r["front_b"]
    b.sales = 475_000.0
    b.s, b.p, b.retain = 0.300, 0.0, 0.080
    b.platforms = []
    b.acquirer, b.mid = "NORTHGATE", "MID00982214"
    b.growth, b.since = 1.10, dt.date(2022, 8, 30)
    b.dep_freq, b.ch_counter, b.ch_night, b.ch_atm = "daily", 0.45, 0.30, 0.25
    b.drop_elsewhere = 0.04
    b.b2b = []
    b.two_accounts, b.second_cash_share = False, 0.0
    b.loan, b.owner_inj = None, 0.0
    b.launder = 346_000.0
    b.network_in = 790_000.0
    k = r["stale_k"]
    k.sales, k.s, k.p, k.retain = 1_760_000.0, 0.165, 0.09, 0.085
    k.growth, k.since = 2.95, dt.date(2017, 4, 3)
    k.platforms = ["DASHDROP"]
    s = r["stale_s"]
    s.sales, s.s, s.retain = 470_000.0, 0.405, 0.080
    s.growth, s.since = 2.90, dt.date(2019, 7, 22)
    n = r["near_n"]
    n.sales, n.s, n.p, n.retain = 2_900_000.0, 0.410, 0.0, 0.070
    n.growth, n.since = 1.30, dt.date(2011, 10, 5)
    n.platforms = []
