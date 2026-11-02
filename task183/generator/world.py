"""task183 world: Lough Ree Bank, a fictional Irish regional bank, its branches, the post offices its customers lodge
at, and the cash-intensive business segment its Financial Crime Operations reviews each year under BCR-3.

Everything is seeded and deterministic. The designed parameters (each reviewed customer's own cash-to-card ratio,
its card trade, its lodgement habit, the two fronts' outside cash) are fixed here; sim.py turns them into days."""
from __future__ import annotations

import datetime as dt
import random

BANK = "Lough Ree Bank DAC"
BANK_SHORT = "Lough Ree Bank"
SEED = 183

# ---- calendar -------------------------------------------------------------------------------------------------
HISTORY_START = dt.date(2025, 1, 1)      # the account export and the merchant services file start here
REVIEW_START = dt.date(2025, 10, 1)
REVIEW_END = dt.date(2026, 9, 30)
EXPORT_END = dt.date(2026, 9, 30)
EXTRACT_DATE = dt.date(2026, 10, 14)     # the review's data pull
AS_OF = dt.date(2026, 11, 6)             # the committee paper is drafted
COMMITTEE = dt.date(2027, 1, 21)
LINE_EUR = 40000

# Irish public holidays (bank holidays) in the window
BANK_HOLIDAYS = {
    dt.date(2025, 1, 1), dt.date(2025, 2, 3), dt.date(2025, 3, 17), dt.date(2025, 4, 21), dt.date(2025, 5, 5),
    dt.date(2025, 6, 2), dt.date(2025, 8, 4), dt.date(2025, 10, 27), dt.date(2025, 12, 25), dt.date(2025, 12, 26),
    dt.date(2026, 1, 1), dt.date(2026, 2, 2), dt.date(2026, 3, 17), dt.date(2026, 4, 6), dt.date(2026, 5, 4),
    dt.date(2026, 6, 1), dt.date(2026, 8, 3),
}


def days(start, end):
    d = start
    while d <= end:
        yield d
        d += dt.timedelta(days=1)


def working(d):
    return d.weekday() < 5 and d not in BANK_HOLIDAYS


def next_working(d):
    d = d + dt.timedelta(days=1)
    while not working(d):
        d += dt.timedelta(days=1)
    return d


# ---- branches and post offices --------------------------------------------------------------------------------
BRANCHES = [  # code, town, county, sort code
    ("ATH", "Athlone", "Westmeath", "97-41-10"),
    ("RSC", "Roscommon", "Roscommon", "97-41-20"),
    ("LFD", "Longford", "Longford", "97-41-30"),
    ("MGR", "Mullingar", "Westmeath", "97-41-40"),
    ("BSL", "Ballinasloe", "Galway", "97-41-50"),
    ("TUM", "Tuam", "Galway", "97-41-60"),
    ("CBR", "Castlebar", "Mayo", "97-41-70"),
    ("COS", "Carrick-on-Shannon", "Leitrim", "97-41-80"),
]
BRANCH = {b[0]: b for b in BRANCHES}

# post offices near each branch town (office code, town, county); codes are An Post's four-digit office numbers
OFFICES = [
    ("4471", "Athlone", "Westmeath", "ATH"), ("4476", "Moate", "Westmeath", "ATH"),
    ("4512", "Roscommon", "Roscommon", "RSC"), ("4519", "Strokestown", "Roscommon", "RSC"),
    ("4521", "Castlerea", "Roscommon", "RSC"),
    ("4603", "Longford", "Longford", "LFD"), ("4608", "Edgeworthstown", "Longford", "LFD"),
    ("4611", "Ballymahon", "Longford", "LFD"),
    ("4705", "Mullingar", "Westmeath", "MGR"), ("4709", "Castlepollard", "Westmeath", "MGR"),
    ("4802", "Ballinasloe", "Galway", "BSL"), ("4806", "Mountbellew", "Galway", "BSL"),
    ("4911", "Tuam", "Galway", "TUM"), ("4914", "Headford", "Galway", "TUM"),
    ("5021", "Castlebar", "Mayo", "CBR"), ("5027", "Westport", "Mayo", "CBR"), ("5030", "Claremorris", "Mayo", "CBR"),
    ("5108", "Carrick-on-Shannon", "Leitrim", "COS"), ("5112", "Mohill", "Leitrim", "COS"),
    ("5115", "Drumshanbo", "Leitrim", "COS"),
]
OFFICE = {o[0]: o for o in OFFICES}

# ---- the cash-intensive segment ------------------------------------------------------------------------------
# trade key, the bank's trade label, count, the trade's typical cash-to-card ratio, the days it opens (Mon=0)
TRADES = [
    ("cafe", "Cafe / coffee shop", 8, 0.55, (0, 1, 2, 3, 4, 5, 6)),
    ("takeaway", "Takeaway / fast food", 8, 0.70, (0, 1, 2, 3, 4, 5, 6)),
    ("barber", "Barber / hairdresser", 7, 0.80, (1, 2, 3, 4, 5)),
    ("nails", "Nail and beauty salon", 6, 0.35, (1, 2, 3, 4, 5)),
    ("carwash", "Car wash / valeting", 5, 0.50, (0, 1, 2, 3, 4, 5, 6)),
    ("convenience", "Convenience store / newsagent", 8, 0.40, (0, 1, 2, 3, 4, 5, 6)),
    ("launderette", "Launderette / dry cleaner", 6, 0.90, (0, 1, 2, 3, 4, 5)),
]
TRADE = {t[0]: t for t in TRADES}

# day-of-week trade profile by trade (Mon..Sun), relative
DOW = {
    "cafe": (0.86, 0.88, 0.92, 0.97, 1.10, 1.30, 0.97),
    "takeaway": (0.78, 0.80, 0.86, 0.95, 1.30, 1.42, 0.89),
    "barber": (0.0, 0.85, 0.92, 1.00, 1.15, 1.30, 0.0),
    "nails": (0.0, 0.78, 0.86, 1.00, 1.20, 1.36, 0.0),
    "carwash": (0.80, 0.82, 0.86, 0.92, 1.08, 1.40, 1.12),
    "convenience": (0.95, 0.94, 0.95, 0.97, 1.05, 1.10, 1.04),
    "launderette": (1.10, 0.96, 0.95, 0.97, 1.00, 1.02, 0.0),
}

# name parts for trading names (fictional; towns are real)
NAME_STEMS = {
    "cafe": ["Riverbank Cafe", "Market Square Coffee", "The Abbey Tea Rooms", "Courthouse Lane Cafe",
             "Shannonside Coffee House", "The Corner Bakehouse", "Quayside Cafe", "Main Street Kitchen"],
    "takeaway": ["Golden Fry", "Bridge Street Chipper", "Lakeside Grill", "The Pizza Yard", "Supreme Fish Bar",
                 "Dragon Garden Takeaway", "Kebab Corner", "The Burger Loft"],
    "barber": ["Sharp Edge Barbers", "Old Town Barber Shop", "Cutting Room", "Fade and Shave", "Clipper House",
               "Mainline Barbers", "The Groom Room"],
    "nails": ["Polished Nail Studio", "Glow Beauty Rooms", "Nailed It Studio", "Luxe Nails and Brows",
              "Serenity Beauty", "Gloss Nail Bar"],
    "carwash": ["Sparkle Hand Car Wash", "Midland Valet Centre", "Showroom Shine Valeting", "Crystal Auto Spa",
                "Bubbles Hand Wash"],
    "convenience": ["Daybreak Stores", "Corner Shop Express", "Fairway Foodstore", "Kilbeg Newsagents",
                    "Value Stop", "Village Mart", "Quick Pick Convenience", "Station Road Stores"],
    "launderette": ["Clean Cycle Launderette", "Fresh Press Dry Cleaners", "Suds Laundry", "Whitewash Launderette",
                    "Pressed Dry Cleaning", "Spin City Launderette"],
}

# personas (guard.py names --geo Ireland --seed 183)
PEOPLE = {
    "head_fco": "Malachy Crohan",      # Head of Financial Crime Operations (the stakeholder; never in the prompt)
    "mlro": "Helen Culhane",           # Money Laundering Reporting Officer, owner of BCR-3
    "cash_ops": "Conall Mulgrew",      # cash operations manager
    "merchant": "Dearbhail Cashman",   # merchant services manager
}

# the four designed customers: trade, slot within the trade, own cash ratio, weekly card trade (EUR),
# outside cash put in each lodgement (EUR, 0 for a legitimate customer)
FOCAL = {
    "cafe_heavy": dict(trade="cafe", slot=2, k=1.40, card_week=2600.0, inj=0.0),
    "barber_heavy": dict(trade="barber", slot=1, k=1.50, card_week=2000.0, inj=0.0),
    "front_carwash": dict(trade="carwash", slot=3, k=0.10, card_week=6500.0, inj=958.0),
    "front_nails": dict(trade="nails", slot=0, k=0.07, card_week=4200.0, inj=493.0),
}


def customers():
    """The reviewed customers with their designed parameters. Each legitimate customer's own ratio sits near its
    trade's typical ratio (within the band that keeps it under the referral line against its peers), and nobody but
    the two fronts carries outside cash."""
    r = random.Random(SEED)
    out = []
    serial = 10411
    till_slots = {"cafe": (4, 6), "takeaway": (2, 5), "barber": (3,), "nails": (2, 4), "carwash": (0, 4),
                  "convenience": (1, 6), "launderette": (2,)}
    focal_at = {(v["trade"], v["slot"]): k for k, v in FOCAL.items()}
    # trade-specific ratio multipliers for the legitimate customers (designed spread, not random draws)
    spread = [0.80, 0.88, 0.94, 1.00, 1.06, 1.12, 1.18, 0.84]
    branch_codes = [b[0] for b in BRANCHES]
    for tkey, tlabel, n, kmed, open_days in TRADES:
        stems = NAME_STEMS[tkey]
        for i in range(n):
            serial += r.choice((7, 11, 13, 17, 19, 23))
            home = branch_codes[(i * 3 + len(tkey)) % len(branch_codes)]
            town = BRANCH[home][1]
            focal = focal_at.get((tkey, i))
            c = dict(cid="BC-%05d" % serial, trade=tkey, trade_label=tlabel, slot=i, home=home,
                     name="%s, %s" % (stems[i], town), focal=focal or "",
                     open_days=open_days,
                     legal="Limited company" if r.random() < 0.55 else "Sole trader",
                     till=(i in till_slots.get(tkey, ())),
                     inj=0.0)
            if focal:
                f = FOCAL[focal]
                c.update(k=f["k"], card_week=f["card_week"], inj=f["inj"], till=False)
            else:
                c["k"] = round(kmed * spread[(i + len(tkey)) % len(spread)] * (1 + r.uniform(-0.03, 0.03)), 4)
                c["card_week"] = round(r.uniform(2600, 7600), 2)
            # lodgement habit: fixed weekdays or every few days; channel: branch counter or post office
            habit = r.random()
            if focal == "front_carwash":
                c["habit"] = ("days", (0, 3))          # Monday and Thursday
            elif focal == "front_nails":
                c["habit"] = ("days", (1, 4))          # Tuesday and Friday
            elif habit < 0.45:
                c["habit"] = ("days", r.choice([(0, 3), (1, 4), (0, 2, 4), (1, 3), (2, 5)]))
            else:
                c["habit"] = ("every", r.choice([(2, 4), (3, 5), (2, 5), (3, 6)]))
            po_offices = [o for o in OFFICES if o[3] == home]
            c["channel"] = "branch" if (focal or r.random() < 0.6) else "post"
            c["office"] = po_offices[i % len(po_offices)][0]
            c["mids"] = 2 if r.random() < 0.25 else 1
            c["acct"] = "%08d" % r.randint(30000000, 89999999)
            c["second_acct"] = ("%08d" % r.randint(30000000, 89999999)) if r.random() < 0.15 else ""
            c["onboarded"] = dt.date(r.randint(2009, 2023), r.randint(1, 12), r.randint(1, 28))
            out.append(c)
    return out


CUSTOMERS = customers()
BY_CID = {c["cid"]: c for c in CUSTOMERS}
FOCAL_CID = {c["focal"]: c["cid"] for c in CUSTOMERS if c["focal"]}
