"""The co-operative's book with the mutual: members, their blocks and varieties, the co-operative's 2025 redraw of its
four sub-districts, the cover's schedule season by season, and what the cover paid.

The mutual's policy system copies a block's sub-district when the block first comes on cover and rewrites it only when
the block is endorsed, so a block not endorsed since the 2025 redraw keeps the old one. The schedule mirrors the
co-operative's variety lines and repeats the block's insured area on each. Claims are one per member a season,
assessed on the member's insured area at the season's payout a hectare; the claims report repeats the claim's amount
on each insured block line. Brokers and members both lodge after a hot season, so some claims are lodged twice and
assessed twice; only one is ever paid. Each season is paid in an interim run in March and a final run once the
Service approves the season's readings."""
import collections
import datetime as dt

import numpy as np

import world as W

VARIETIES = ["Shiraz", "Cabernet Sauvignon", "Chardonnay", "Grenache", "Merlot", "Sauvignon Blanc", "Mataro",
             "Durif", "Pinot Gris", "Riesling"]
SURNAMES = ["Ainslie", "Baxter", "Calloway", "Delaney", "Eastwood", "Fenwick", "Gallagher", "Hartigan", "Ingram",
            "Jessup", "Kilroy", "Lindqvist", "Marchetti", "Nolan", "Oakes", "Pemberton", "Quilty", "Rasmussen",
            "Sinclair", "Tedesco", "Underwood", "Vickers", "Whitlock", "Yardley", "Zammit", "Abernethy", "Brennock",
            "Costigan", "Dunphy", "Elsworth", "Faraday", "Gorman", "Holloway", "Iverson", "Jardine", "Kearney",
            "Lockhart", "Mulcahy", "Norrie", "Ormsby", "Pritchard", "Rowntree", "Stavros", "Tremayne", "Ulrich",
            "Varga", "Wilmot", "Xuereb", "Yeoman", "Zielinski", "Ashcroft", "Bramwell", "Cardillo", "Doolan",
            "Esposito", "Finnegan", "Goldsworthy", "Huxtable"]
ENTITY = ["Vineyards", "Estate", "Family Vineyards", "& Sons", "Wines", "Growers", "Partners", "Farming Co"]


def rng(*key):
    return np.random.default_rng([W.SEED, 900] + [int(k) for k in key])


class Block:
    def __init__(self, member, no, area, district_old, district_new, varieties, planted, first_cover, cancel):
        self.member, self.no, self.area = member, no, area
        self.district_old, self.district_new = district_old, district_new
        self.varieties = varieties          # [(variety, ha)], ha summing to area
        self.planted = planted
        self.first_cover = first_cover      # first season the block was on cover, or None (never insured)
        self.cancel = cancel                # date its cover ended (grubbed or withdrawn), or None
        self.endorsed = None                # date of the block's last endorsement on the policy system


def members():
    g = rng(1)
    out = []
    for i in range(58):
        surname = SURNAMES[i]
        kind = ENTITY[int(g.integers(0, len(ENTITY)))]
        name = "%s %s" % (surname, kind) if kind[0] != "&" else "%s %s" % (surname, kind)
        out.append({"coop_no": 300 + int(g.integers(1, 9)) * 0 + 100 + i * 7 + int(g.integers(0, 6)),
                    "name": name, "policy_no": "HC%06d" % (104000 + i * 13 + int(g.integers(0, 9)))})
    return out


def blocks(mem):
    g = rng(2)
    out = []
    for m in mem:
        nb = int(g.choice([1, 1, 2, 2, 2, 3, 3, 4, 5, 6]))
        home_new = W.SUB_DISTRICTS[int(g.integers(0, 4))]
        for no in range(1, nb + 1):
            area = float(np.round(g.lognormal(1.7, 0.55), 1))
            area = max(1.2, min(area, 38.0))
            nv = int(g.choice([1, 1, 1, 2, 2, 3]))
            vs = list(g.choice(VARIETIES, size=nv, replace=False))
            cuts = np.sort(g.uniform(0.15, 0.85, nv - 1))
            shares = np.diff(np.concatenate([[0.0], cuts, [1.0]]))
            ha = [float(np.round(area * s, 2)) for s in shares]
            ha[-1] = float(np.round(area - sum(ha[:-1]), 2))
            new = home_new if g.random() < 0.8 else W.SUB_DISTRICTS[int(g.integers(0, 4))]
            # the 2025 redraw moved about one block in five between the same four names
            old = new if g.random() < 0.78 else W.SUB_DISTRICTS[(W.SUB_DISTRICTS.index(new) + 1 + int(g.integers(0, 3))) % 4]
            insured = g.random() < 0.72
            first = int(g.choice([2019, 2019, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027])) if insured else None
            cancel = None
            if insured and g.random() < 0.06:
                cancel = dt.date(int(g.choice([2023, 2024, 2025, 2026, 2027])), int(g.integers(3, 10)), int(g.integers(1, 28)))
                if first is not None and cancel.year <= first:
                    cancel = dt.date(first + 1, 6, 15)
            b = Block(m["coop_no"], no, area, old, new, list(zip(vs, ha)), int(g.integers(1968, 2021)), first, cancel)
            if insured and g.random() < 0.38:
                b.endorsed = dt.date(int(g.choice([2025, 2026, 2027])), int(g.integers(1, 13)), int(g.integers(1, 28)))
                if b.endorsed < W.REDRAW and b.endorsed.year == 2025:
                    b.endorsed = dt.date(2025, int(g.integers(7, 13)), int(g.integers(1, 28)))
                if b.endorsed > W.AS_OF:
                    b.endorsed = dt.date(2027, int(g.integers(1, 8)), int(g.integers(1, 28)))
            out.append(b)
    return out


def stored_district(b):
    """the policy system's sub-district: written when the block came on cover, rewritten at an endorsement"""
    if b.endorsed is not None and b.endorsed >= W.REDRAW:
        return b.district_new
    if b.first_cover is not None and b.first_cover >= 2025:
        return b.district_new
    return b.district_old


def in_force(b, on):
    if b.first_cover is None:
        return False
    start = dt.date(b.first_cover, 11, 1)
    return start <= on and (b.cancel is None or b.cancel > on)


def schedule_2027(bl):
    return [b for b in bl if in_force(b, W.COVER_START)]
