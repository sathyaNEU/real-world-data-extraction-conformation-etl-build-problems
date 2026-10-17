"""The clean truth for task264: the basket's lines, each partner chain's weekly shelf prices and promotions, the panel's
stores (refits, refurbishments, openings and closures), what each store sold of each line each week, and each store's
weekly takings by department. Nothing here is messy; records.py writes the feeds as the firm's loader holds them."""
from __future__ import annotations

import numpy as np

import common as K

# per category: big sellers' and slow lines' rise over the window, extra rise in one format, share of the category's
# lines the July chain ranges, and the seasonal profile (Christmas lift, Easter lift, summer or winter swing)
CAT_PARAMS = {
    "Bread and bakery": dict(fast=0.045, slow=0.050, s5=0.70, xmas=0.10, easter=0.10, swing=0.00,
        extra={"supermarket": 0.0002, "neighbourhood": -0.0004, "convenience": -0.0001, "online": 0.0002}),
    "Breakfast cereals": dict(fast=0.020, slow=0.110, s5=0.15, xmas=0.00, easter=0.00, swing=-0.04,
        extra={"supermarket": 0.0018, "neighbourhood": -0.0046, "convenience": -0.0015, "online": -0.0075}),
    "Milk": dict(fast=0.050, slow=0.045, s5=0.70, xmas=0.05, easter=0.00, swing=0.00,
        extra={"supermarket": -0.0024, "neighbourhood": 0.0050, "convenience": 0.0342, "online": 0.0007}),
    "Cheese": dict(fast=0.030, slow=0.110, s5=0.20, xmas=0.35, easter=0.05, swing=0.00,
        extra={"supermarket": 0.0021, "neighbourhood": -0.0020, "convenience": -0.0056, "online": -0.0018}),
    "Yoghurt and desserts": dict(fast=0.030, slow=0.035, s5=0.25, xmas=0.15, easter=0.00, swing=0.04,
        extra={"supermarket": -0.0007, "neighbourhood": -0.0011, "convenience": -0.0007, "online": 0.0153}),
    "Butter and spreads": dict(fast=0.060, slow=0.065, s5=0.45, xmas=0.10, easter=0.00, swing=0.00,
        extra={"supermarket": 0.0008, "neighbourhood": 0.0006, "convenience": -0.0014, "online": -0.0339}),
    "Eggs": dict(fast=0.080, slow=0.080, s5=0.70, xmas=0.10, easter=0.15, swing=0.00,
        extra={"supermarket": 0.0003, "neighbourhood": -0.0008, "convenience": -0.0011}),
    "Fresh meat and poultry": dict(fast=0.040, slow=0.045, s5=0.50, xmas=0.20, easter=0.00, swing=0.00,
        extra={"supermarket": -0.0002, "neighbourhood": 0.0289, "convenience": 0.0027}),
    "Deli and cooked meats": dict(fast=0.025, slow=0.115, s5=0.20, xmas=0.45, easter=0.05, swing=0.00,
        extra={"supermarket": 0.0037, "neighbourhood": -0.0094, "convenience": 0.0038, "online": -0.0074}),
    "Seafood": dict(fast=0.050, slow=0.055, s5=0.10, xmas=0.60, easter=0.35, swing=0.00,
        extra={"supermarket": 0.0011, "neighbourhood": -0.0060, "convenience": -0.0350, "online": -0.0015}),
    "Fresh fruit": dict(fast=0.035, slow=0.040, s5=0.75, xmas=0.15, easter=0.00, swing=0.08,
        extra={"supermarket": -0.0013, "neighbourhood": 0.0005, "convenience": 0.0084, "online": 0.0015}),
    "Fresh vegetables": dict(fast=0.020, slow=0.025, s5=0.50, xmas=0.15, easter=0.00, swing=0.00,
        extra={"supermarket": 0.0430, "neighbourhood": 0.0191, "convenience": -0.0006, "online": 0.0009}),
    "Frozen foods": dict(fast=0.030, slow=0.035, s5=0.15, xmas=0.05, easter=0.00, swing=0.10,
        extra={"supermarket": 0.0003, "neighbourhood": -0.0006, "convenience": 0.0094, "online": 0.0087}),
    "Biscuits": dict(fast=0.025, slow=0.110, s5=0.10, xmas=0.30, easter=0.05, swing=-0.03,
        extra={"supermarket": 0.0014, "neighbourhood": -0.0044, "convenience": -0.0089, "online": 0.0007}),
    "Confectionery": dict(fast=0.060, slow=0.065, s5=0.30, xmas=0.40, easter=0.70, swing=0.00,
        extra={"supermarket": 0.0004, "neighbourhood": -0.0006, "convenience": -0.0006, "online": 0.0343}),
    "Chips and snacks": dict(fast=0.030, slow=0.035, s5=0.60, xmas=0.25, easter=0.05, swing=0.05,
        extra={"supermarket": 0.0006, "neighbourhood": -0.0006, "convenience": -0.0014, "online": -0.0034}),
    "Soft drinks": dict(fast=0.060, slow=0.025, s5=0.30, xmas=0.30, easter=0.05, swing=0.12,
        extra={"supermarket": -0.0004, "neighbourhood": 0.0002, "convenience": 0.0298, "online": 0.0025}),
    "Coffee and tea": dict(fast=0.030, slow=0.120, s5=0.20, xmas=0.10, easter=0.00, swing=-0.08,
        extra={"supermarket": -0.0008, "neighbourhood": 0.0001, "convenience": 0.0291, "online": 0.0015}),
}
PROMO_LIFT = 1.6
ROUND9 = {"S1", "S2", "N1", "C1", "C2", "O1", "O2"}      # chains whose shelf prices end in 9 cents
SHORT_LIFE = {"Bread and bakery", "Milk", "Yoghurt and desserts", "Deli and cooked meats", "Fresh fruit",
              "Fresh vegetables", "Fresh meat and poultry", "Seafood", "Cheese"}


# ---------------------------------------------------------------------------------------------- the lines
def gtin14(prefix, n, rs):
    """A GTIN-14 with a leading zero (a GTIN-13 packed to 14) and a valid check digit."""
    body = "0" + prefix + "%0*d" % (12 - len(prefix), n)
    body = body[:13]
    s = sum(int(d) * (3 if k % 2 == 0 else 1) for k, d in enumerate(body))
    return body + str((10 - s % 10) % 10)


def lines():
    items = []
    used = set()
    for ci, cat in enumerate(K.CATS):
        fr, sr, kgw, rows = K.LINES[cat]
        P = CAT_PARAMS[cat]
        r = K.rng("lines", cat)
        for j, (desc, kg) in enumerate(rows):
            fast = j < K.N_FAST
            lo, hi = fr if fast else sr
            if kg:
                code = gtin14("2", 100000 + 1000 * ci + j * 7 + int(r.integers(0, 6)), r)
            else:
                while True:
                    pre = ("93" if r.random() < 0.82 else "94") + "%05d" % int(r.integers(10000, 99999))
                    code = gtin14(pre, int(r.integers(0, 99999)), r)
                    if code not in used:
                        break
            used.add(code)
            rise = (P["fast"] if fast else P["slow"]) + r.normal(0, 0.004)
            items.append(dict(
                idx=len(items), code=code, desc=desc, cat=cat, kg=bool(kg), fast=fast,
                base=float(r.uniform(lo, hi)), rate=float(r.uniform(40, 80) if fast else r.uniform(3.0, 9.0)),
                wkg=float(kgw * r.uniform(0.8, 1.25)) if kg else 0.0,
                rise=float(rise), step=int(r.integers(6, 46)),
                in_s5=bool(r.random() < P["s5"]),
                in_conv=bool((not kg) and (fast or r.random() < 0.9))))
    return items


# ---------------------------------------------------------------------------------------------- prices
def price_point(p, chain):
    p10 = np.round(p * 10) / 10
    return np.round(p10 - 0.01, 2) if chain in K.CH and chain in ROUND9 else np.round(p10, 2)


def ranged_at(it, chain):
    fmt = K.CH[chain]["fmt"]
    if fmt == "convenience":
        return it["in_conv"]
    if chain == "S5":
        return it["in_s5"]
    return True


def shelf_prices(items):
    """regular[c][i, t], the week's price[c][i, t] (promotions included) and the promotion flags. Each chain runs a
    weekly catalogue: in each category one line comes on special each week, the lines taken in a fixed rotation of
    sixteen weeks, and chains with a heavier programme run a second rotation of eight weeks beside it. A line's
    special takes the same cut each time."""
    out = {}
    T = np.arange(K.W)
    for c in K.CHAIN_CODES:
        ch = K.CH[c]
        reg = np.zeros((len(items), K.W))
        pr = np.zeros((len(items), K.W))
        flag = np.zeros((len(items), K.W), bool)
        for cat in K.CATS:
            its = [it for it in items if it["cat"] == cat]
            rc = K.rng("catalogue", c, cat)
            order = rc.permutation(len(its))
            phase = int(rc.integers(0, 16))
            slot = (T + phase) % 16
            on = {int(order[k]): (slot == k) for k in range(len(its))}
            if ch["promo_rate"] >= 0.08:
                pool = [j for j, it in enumerate(its) if ranged_at(it, c)]
                order2 = [pool[k] for k in rc.permutation(len(pool))[:8]]
                slot2 = (T + int(rc.integers(0, 8))) % 8
                for k in range(len(order2)):
                    on[order2[k]] = on[order2[k]] | (slot2 == k)
            for j, it in enumerate(its):
                r = K.rng("price", c, it["code"])
                extra = CAT_PARAMS[it["cat"]]["extra"].get(ch["fmt"], 0.0)
                rise = it["rise"] + extra + r.normal(0, 0.003)
                step = int(np.clip(it["step"] + r.integers(-2, 3), 4, 47))
                raw = it["base"] * ch["lvl"] * (1 + rise * (T >= step))
                regular = price_point(raw, c)
                depth = 0.5 if (ch["fmt"] == "supermarket" and r.random() < 0.04) else float(r.uniform(0.12, 0.25))
                f = on[j] & ranged_at(it, c)
                promo = np.round(np.round(regular * (1 - depth) * 20) / 20, 2)
                reg[it["idx"]] = regular
                pr[it["idx"]] = np.where(f, promo, regular)
                flag[it["idx"]] = f
        out[c] = dict(reg=reg, price=pr, promo=flag)
    return out


# ---------------------------------------------------------------------------------------------- the panel's stores
SUBURBS = [
    ("Parramatta", "NSW", "2150"), ("Chatswood", "NSW", "2067"), ("Bondi Junction", "NSW", "2022"),
    ("Penrith", "NSW", "2750"), ("Hornsby", "NSW", "2077"), ("Liverpool", "NSW", "2170"), ("Blacktown", "NSW", "2148"),
    ("Castle Hill", "NSW", "2154"), ("Campbelltown", "NSW", "2560"), ("Hurstville", "NSW", "2220"),
    ("Newcastle", "NSW", "2300"), ("Wollongong", "NSW", "2500"), ("Gosford", "NSW", "2250"),
    ("Dee Why", "NSW", "2099"), ("Marrickville", "NSW", "2204"), ("Box Hill", "VIC", "3128"),
    ("Frankston", "VIC", "3199"), ("Dandenong", "VIC", "3175"), ("Ringwood", "VIC", "3134"), ("Footscray", "VIC", "3011"),
    ("Geelong", "VIC", "3220"), ("Glen Waverley", "VIC", "3150"), ("Werribee", "VIC", "3030"), ("Preston", "VIC", "3072"),
    ("Brunswick", "VIC", "3056"), ("St Kilda", "VIC", "3182"), ("Camberwell", "VIC", "3124"),
    ("Moonee Ponds", "VIC", "3039"), ("Cranbourne", "VIC", "3977"), ("Ballarat", "VIC", "3350"),
    ("Bendigo", "VIC", "3550"), ("Chermside", "QLD", "4032"), ("Carindale", "QLD", "4152"),
    ("Indooroopilly", "QLD", "4068"), ("Toowong", "QLD", "4066"), ("Southport", "QLD", "4215"),
    ("Robina", "QLD", "4226"), ("Ipswich", "QLD", "4305"), ("Toowoomba", "QLD", "4350"), ("Cairns", "QLD", "4870"),
    ("Townsville", "QLD", "4810"), ("Maroochydore", "QLD", "4558"), ("Glenelg", "SA", "5045"), ("Norwood", "SA", "5067"),
    ("Marion", "SA", "5043"), ("Elizabeth", "SA", "5112"), ("Modbury", "SA", "5092"), ("Unley", "SA", "5061"),
    ("Port Adelaide", "SA", "5015"), ("Joondalup", "WA", "6027"), ("Fremantle", "WA", "6160"), ("Morley", "WA", "6062"),
    ("Cannington", "WA", "6107"), ("Midland", "WA", "6056"), ("Rockingham", "WA", "6168"), ("Subiaco", "WA", "6008"),
    ("Mandurah", "WA", "6210"), ("Hobart", "TAS", "7000"), ("Launceston", "TAS", "7250"), ("Glenorchy", "TAS", "7010"),
    ("Belconnen", "ACT", "2617"), ("Gungahlin", "ACT", "2912"), ("Woden", "ACT", "2606"),
]
FULFILMENT = [("Moorebank", "NSW", "2170"), ("Truganina", "VIC", "3029"), ("Larapinta", "QLD", "4110"),
              ("Kewdale", "WA", "6105"), ("Wingfield", "SA", "5013"), ("Erskine Park", "NSW", "2759"),
              ("Derrimut", "VIC", "3026")]
STREETS = ["Station Street", "High Street", "Main Road", "Church Street", "Victoria Road", "Railway Parade",
           "King Street", "George Street", "Beach Road", "Park Road", "Bridge Road", "Market Street", "Albert Street",
           "Grand Junction Road", "Canning Highway", "Smith Street", "Pacific Highway", "Princes Highway"]
LOCAL_NAMES = {"supermarket": "", "neighbourhood": "", "convenience": "", "online": "Fulfilment "}

# designed panel events, by chain: (kind, week) with kind refit (re-coded, trading on), refurb (closed for some weeks,
# re-coded on reopening), open (a new store) or close (closed for good)
EVENTS = {
    "S1": [("refit", 22)], "S2": [("refit", 15), ("refurb", 33)], "S3": [("refit", 40)],
    "S4": [("refit", 11), ("open", 26)], "S5": [("refit", 41)],
    "N1": [("refit", 29), ("refurb", 9), ("open", 44)], "N2": [("refit", 36)], "N3": [("refit", 19)],
    "C1": [("refit", 13), ("refurb", 24), ("close", 40)], "C2": [("refit", 31), ("refurb", 42), ("open", 19), ("open", 37)],
    "C3": [("refit", 8), ("refurb", 27), ("close", 25)],
    "O1": [("refit", 34)], "O2": [("refit", 20), ("refurb", 12)], "O3": [("refit", 43)],
}


def sites_and_codes():
    """Sites (physical stores) and the codes they traded under. A code row: code, site, chain, first and last week
    (inclusive, window index), the week the site was closed between codes."""
    sites, codes = [], []
    taken = set()
    serial = {c: 0 for c in K.CHAIN_CODES}
    rs = K.rng("sites")
    sub_cycle = list(range(len(SUBURBS)))
    rs.shuffle(sub_cycle)
    pos = 0
    for c in K.CHAIN_CODES:
        ch = K.CH[c]
        r = K.rng("stores", c)
        n_extra = sum(1 for k, _ in EVENTS[c] if k == "open")
        for k in range(ch["n"] + n_extra):
            if ch["fmt"] == "online":
                sub = FULFILMENT[int(r.integers(0, len(FULFILMENT)))]
                while (c, sub[0]) in taken:
                    sub = FULFILMENT[int(r.integers(0, len(FULFILMENT)))]
            else:
                sub = SUBURBS[sub_cycle[pos % len(SUBURBS)]]
                pos += 1
                if (c, sub[0]) in taken:
                    sub = SUBURBS[sub_cycle[pos % len(SUBURBS)]]
                    pos += 1
            taken.add((c, sub[0]))
            size = float(r.uniform(*ch["size"]))
            num = int(r.integers(2, 240))
            street = STREETS[int(r.integers(0, len(STREETS)))]
            sites.append(dict(site=len(sites), k=k, chain=c, fmt=ch["fmt"], suburb=sub[0], state=sub[1],
                              postcode=sub[2], address="%d %s" % (num, street), size=size,
                              opened_year=int(r.integers(1996, 2024)), first=ch["start"], last=K.W - 1, segments=[]))
        mine = [s for s in sites if s["chain"] == c]
        order = list(range(len(mine)))
        r.shuffle(order)
        cursor = 0
        plan = {}
        for kind, wk in EVENTS[c]:
            plan.setdefault(kind, []).append((wk, mine[order[cursor]]))
            cursor += 1
        for wk, s in plan.get("open", []):
            s["first"] = wk
            s["opened_year"] = 2026
        for wk, s in plan.get("close", []):
            s["last"] = wk
        for s in mine:
            s["segments"] = [(s["first"], s["last"])]
        for wk, s in plan.get("refit", []):
            s["segments"] = [(s["first"], wk - 1), (wk, s["last"])]
            s["refit"] = wk
        for wk, s in plan.get("refurb", []):
            gap = int(r.integers(2, 5))
            s["segments"] = [(s["first"], wk - 1), (wk + gap, s["last"])]
            s["refurb"] = (wk, gap)
        for s in mine:
            for j, (a, b) in enumerate(s["segments"]):
                serial[c] += 1
                codes.append(dict(code=None, site=s["site"], k=s["k"], seg=j, chain=c, fmt=s["fmt"], first=a, last=b))
    # store codes: the firm's five-digit codes, a block per format, issued in order of first week
    base = {"supermarket": 21000, "neighbourhood": 34000, "convenience": 47000, "online": 68000}
    for fmt in K.FORMATS:
        rc = K.rng("codes", fmt)
        mine = sorted([x for x in codes if x["fmt"] == fmt], key=lambda x: (x["first"], x["chain"], x["site"]))
        n = base[fmt] + int(rc.integers(10, 90))
        for x in mine:
            n += int(rc.integers(3, 29))
            x["code"] = str(n)
    return sites, codes


# ---------------------------------------------------------------------------------------------- what each store sold
def season(cat, t):
    P = CAT_PARAMS[cat]
    s = np.ones(K.W)
    s[1] += 0.35 * P["xmas"]
    s[2] += 1.00 * P["xmas"] + 0.08
    s[3] += 0.30 * P["xmas"] - 0.04
    s[17] += P["easter"]
    phase = 2 * np.pi * (np.arange(K.W) - 7) / 52.0      # peaks in late January
    s *= 1 + P["swing"] * np.cos(phase)
    return s[t]


def traffic(chain, t):
    return 1 + K.CH[chain]["trend"] * t / (K.W - 1)


def sales(items, prices, sites, codes):
    """Per code: units[i, t] (kilograms for lines sold by weight), dollars[i, t], marked-down units, and the till code
    events. A line sells only where the code's chain ranges it and only in the code's weeks."""
    T = np.arange(K.W)
    seas = np.array([season(it["cat"], T) for it in items])                     # items x weeks
    rate = np.array([it["rate"] for it in items])
    kg = np.array([it["kg"] for it in items])
    wkg = np.array([it["wkg"] for it in items])
    short = np.array([it["cat"] in SHORT_LIFE for it in items])
    site_by = {s["site"]: s for s in sites}
    out = []
    for x in codes:
        s = site_by[x["site"]]
        c = x["chain"]
        ch = K.CH[c]
        ranged = np.array([ranged_at(it, c) for it in items])
        active = (T >= x["first"]) & (T <= x["last"])
        r = K.rng("sold", c, x["k"], x["seg"])
        P = prices[c]
        uplift = 1.0 + 0.05 * (x["first"] > s["first"])
        lam = (rate[:, None] * s["size"] * traffic(c, T)[None, :] * seas * np.where(P["promo"], PROMO_LIFT, 1.0) * uplift)
        lam = lam * ranged[:, None]
        n = r.poisson(lam) * active[None, :]
        units = n.astype(float)
        kgsum = r.gamma(np.maximum(4.0 * n, 1e-9), np.where(kg, wkg, 1.0)[:, None] / 4.0)
        units = np.where(kg[:, None], np.round(np.where(n > 0, kgsum, 0.0), 3), units)
        units = np.where(units > 0, units, 0.0)
        price = P["price"]
        md = np.zeros_like(units)
        mdcode = np.zeros(units.shape, bool)
        if ch["md_code"]:
            hit = (r.random(units.shape) < 0.035) & short[:, None] & ~P["promo"] & (units > 0) & ~kg[:, None] \
                  & (n >= 2)
            md = np.where(hit, np.maximum(1, np.floor(n * r.uniform(0.2, 0.5, units.shape))), 0.0)
            mdcode = hit
        dollars = np.where(kg[:, None], np.round(units * price, 2), (units - md) * price + md * np.round(price * 0.5, 2))
        dollars = np.round(dollars, 2)
        check = np.zeros(units.shape, bool)
        if c == K.UPGRADE_CHAIN:
            check = (r.random(units.shape) < 0.006) & (T[None, :] >= K.UPGRADE_T) & ~P["promo"] & (units > 0) & ~mdcode
        out.append(dict(code=x["code"], chain=c, fmt=ch["fmt"], site=x["site"], units=units, dollars=dollars,
                        md=md, mdflag=mdcode, check=check, promo=P["promo"] & (units > 0)))
    return out


# ---------------------------------------------------------------------------------------------- weekly takings
DEPARTMENTS = {
    "supermarket": [("10", "Grocery", 0.31), ("20", "Dairy and chilled", 0.12), ("25", "Frozen", 0.06),
                    ("30", "Fruit and vegetables", 0.11), ("40", "Meat and seafood", 0.12),
                    ("45", "Deli and bakery", 0.09), ("60", "Liquor", 0.08), ("80", "General merchandise", 0.11)],
    "neighbourhood": [("10", "Grocery", 0.36), ("20", "Dairy and chilled", 0.15), ("30", "Fruit and vegetables", 0.13),
                      ("45", "Deli and bakery", 0.12), ("40", "Meat", 0.10), ("80", "General merchandise", 0.14)],
    "convenience": [("10", "Grocery", 0.38), ("20", "Chilled drinks and dairy", 0.27), ("70", "Tobacco", 0.25),
                    ("90", "Services and cards", 0.10)],
    "online": [("10", "Grocery", 0.38), ("20", "Dairy and chilled", 0.15), ("30", "Fresh", 0.24),
               ("80", "Household", 0.19), ("95", "Delivery fees", 0.04)],
}
# chains whose store sales come as two department groups (one till vendor's export, and two chains' own)
TWO_GROUP_CHAINS = set(K.VENDOR_CHAINS) | {"S4", "C1"}
TWO_GROUP = {"supermarket": [("01", "Food", 0.84), ("02", "Non-food", 0.16)],
             "neighbourhood": [("01", "Food", 0.87), ("02", "Non-food", 0.13)],
             "convenience": [("01", "Food", 0.58), ("02", "Non-food", 0.42)],
             "online": [("01", "Food", 0.81), ("02", "Non-food", 0.19)]}
WEEKLY_TAKINGS = {"supermarket": 912_000, "neighbourhood": 1_046_000, "convenience": 548_000, "online": 1_103_000}


def takings(sites, codes):
    """Per code and week: the store's takings by department (dollars). The July chain's stores also carry their
    takings from the week ending 3 January 2026 (its onboarding backfill), outside the panel."""
    T = np.arange(K.W)
    site_by = {s["site"]: s for s in sites}
    out = []
    for x in codes:
        s = site_by[x["site"]]
        c = x["chain"]
        r = K.rng("takings", c, x["k"], x["seg"])
        base = WEEKLY_TAKINGS[x["fmt"]] * s["size"] * K.CH[c]["lvl"] ** 0.4
        depts = TWO_GROUP[x["fmt"]] if c in TWO_GROUP_CHAINS else DEPARTMENTS[x["fmt"]]
        shares = np.array([d[2] for d in depts]) * r.uniform(0.85, 1.15, len(depts))
        shares = shares / shares.sum()
        first = BACKFILL_FIRST if c == "S5" else x["first"]
        weeks = T[(T >= first) & (T <= x["last"])]
        gen = 1 + 0.18 * np.exp(-((weeks - 2) ** 2) / 1.5) + 0.04 * np.cos(2 * np.pi * (weeks - 7) / 52)
        tot = base * traffic(c, weeks) * gen * r.normal(1, 0.035, len(weeks))
        dep = tot[:, None] * shares[None, :] * r.normal(1, 0.03, (len(weeks), len(depts)))
        dep = np.round(dep, 2)
        out.append(dict(code=x["code"], chain=c, fmt=x["fmt"], weeks=weeks, depts=depts, values=dep))
    return out


BACKFILL_FIRST = K.BACKFILL_FROM


def world():
    items = lines()
    prices = shelf_prices(items)
    sites, codes = sites_and_codes()
    sold = sales(items, prices, sites, codes)
    tk = takings(sites, codes)
    return dict(items=items, prices=prices, sites=sites, codes=codes, sold=sold, takings=tk)
