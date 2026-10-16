"""The supermarkets' product lines and their monthly truth over the parallel year: shelf prices (regular prices
reviewed in the retailers' price-review months, monthly offers from November to July), Wrenfold's member prices from
March 2026, own-label lines, range changes, and the units sold (an offer lifts a line's sales and, for goods that
keep, the month after falls below normal because shoppers stocked up)."""
import numpy as np

import world as W

REVIEW_MONTHS = list(range(1, 13))     # a line's regular price can be reviewed in any month after September 2025
OUT_OF_SCOPE = [("1109", "Cakes and pastries", 1.95), ("1191", "Crisps and snacks", 1.30),
                ("5612", "Dishwashing products", 3.20), ("6214", "Cosmetics", 6.50)]
SEASON = {  # a month's demand relative to the year (index 0 = September 2025)
    "1221": [1.10, 0.95, 0.85, 0.95, 0.80, 0.82, 0.90, 0.98, 1.06, 1.20, 1.28, 1.24, 1.10],
    "1222": [1.10, 0.92, 0.82, 0.86, 0.80, 0.82, 0.90, 1.00, 1.08, 1.24, 1.32, 1.28, 1.12],
    "1223": [1.02, 0.98, 0.96, 1.06, 1.04, 0.95, 0.96, 0.98, 1.00, 1.04, 1.06, 1.04, 1.02],
    "1182": [0.95, 1.02, 1.08, 1.45, 0.85, 0.98, 1.05, 1.10, 0.92, 0.90, 0.92, 0.94, 0.95],
    "1108": [0.98, 1.00, 1.04, 1.30, 0.92, 0.94, 0.98, 0.98, 0.96, 0.95, 0.96, 0.98, 0.98],
}
VISITORS = [1.06, 1.01, 0.97, 1.00, 0.94, 0.95, 0.97, 0.99, 1.02, 1.07, 1.12, 1.13, 1.06]
TRADE_DOWN = {"1211": (0.30, -0.10)}    # coffee buyers moving to own label: own-label units up 30 per cent over the year, branded down 10
STORABLE_BOOST, FRESH_BOOST = 2.6, 1.4

SYL = ["har", "vest", "mere", "lin", "ford", "bram", "well", "cor", "dale", "ash", "ton", "kel", "wyn", "tor", "sel",
       "bay", "rid", "ley", "mor", "stan", "oak", "brook", "fen", "wick", "glen", "row", "cal", "ver", "pen", "tal"]
VARIANTS = {
    "1101": [("Wholemeal loaf", "800g"), ("White sliced loaf", "800g"), ("Seeded batch", "800g"), ("Sourdough", "400g"),
             ("Rolls x6", "6pk"), ("Brown thick sliced", "800g"), ("Farmhouse white", "800g"), ("Bagels x5", "5pk")],
    "1103": [("Corn flakes", "500g"), ("Bran flakes", "750g"), ("Porridge oats", "1kg"), ("Granola", "500g"),
             ("Muesli", "750g"), ("Wheat biscuits x24", "430g"), ("Honey hoops", "375g"), ("Rice pops", "440g")],
    "1105": [("Spaghetti", "500g"), ("Penne", "500g"), ("Fusilli", "1kg"), ("Basmati rice", "1kg"),
             ("Long grain rice", "1kg"), ("Egg noodles", "250g"), ("Lasagne sheets", "375g"), ("Risotto rice", "500g")],
    "1108": [("Digestives", "400g"), ("Rich tea", "300g"), ("Chocolate digestives", "300g"), ("Shortbread", "200g"),
             ("Ginger nuts", "250g"), ("Custard creams", "400g"), ("Oat crunch", "300g"), ("Cookies", "200g")],
    "1145": [("Natural yoghurt", "500g"), ("Greek style yoghurt", "500g"), ("Fruit yoghurts 4x125g", "500g"),
             ("Strawberry yoghurt", "150g"), ("Kids yoghurts 6x45g", "270g"), ("Vanilla yoghurt", "450g")],
    "1146": [("Mature cheddar", "400g"), ("Mild cheddar", "400g"), ("Red Leicester", "350g"), ("Brie", "200g"),
             ("Mozzarella", "125g"), ("Grated cheddar", "250g"), ("Cheese slices", "200g"), ("Stilton", "220g")],
    "1151": [("Salted butter", "250g"), ("Unsalted butter", "250g"), ("Spreadable butter", "500g"),
             ("Sunflower spread", "500g"), ("Olive spread", "500g"), ("Light spread", "500g")],
    "1182": [("Milk chocolate bar", "100g"), ("Dark chocolate bar", "100g"), ("Chocolate buttons", "70g"),
             ("Fruit gums", "150g"), ("Mint chocolates", "200g"), ("Toffees", "150g"), ("Caramel bar", "45g"),
             ("Sharing bag", "160g")],
    "1211": [("Instant coffee", "200g"), ("Ground coffee", "227g"), ("Coffee beans", "500g"), ("Coffee pods x10", "55g"),
             ("Decaf instant", "100g"), ("Gold blend", "100g")],
    "1212": [("Tea bags x80", "250g"), ("Tea bags x160", "500g"), ("Green tea x40", "80g"), ("Fruit tea x20", "40g"),
             ("Earl grey x50", "125g"), ("Decaf tea x80", "250g")],
    "1221": [("Cola", "2L"), ("Diet cola 8x330ml", "2.64L"), ("Lemonade", "2L"), ("Orange crush", "1.5L"),
             ("Ginger beer 4x330ml", "1.32L"), ("Sparkling apple", "750ml"), ("Energy drink", "500ml"),
             ("Squash", "1L")],
    "1222": [("Still water", "2L"), ("Sparkling water", "1L"), ("Still water 6x500ml", "3L"),
             ("Spring water", "1.5L"), ("Flavoured water", "1L")],
    "1223": [("Orange juice", "1L"), ("Apple juice", "1L"), ("Smooth orange", "1.75L"), ("Cranberry juice", "1L"),
             ("Pineapple juice", "1L"), ("Tropical juice", "1L")],
    "5611": [("Bio liquid 40 washes", "1.2L"), ("Non-bio capsules x30", "30pk"), ("Powder 50 washes", "3kg"),
             ("Fabric conditioner", "1.4L"), ("Colour liquid 30 washes", "900ml"), ("Stain remover", "1L")],
    "5613": [("Toilet tissue 9 rolls", "9pk"), ("Toilet tissue 4 rolls", "4pk"), ("Kitchen roll 2 rolls", "2pk"),
             ("Toilet tissue 16 rolls", "16pk"), ("Kitchen roll 4 rolls", "4pk")],
    "6213": [("Shampoo", "400ml"), ("Conditioner", "400ml"), ("Shower gel", "250ml"), ("Toothpaste", "75ml"),
             ("Deodorant", "150ml"), ("Hand wash", "250ml"), ("Bar soap 4pk", "4pk"), ("Mouthwash", "500ml")],
    "1109": [("Victoria sponge", "350g"), ("Croissants x4", "4pk"), ("Muffins x4", "4pk"), ("Flapjacks x5", "5pk")],
    "1191": [("Ready salted crisps 6pk", "6pk"), ("Tortilla chips", "200g"), ("Salted peanuts", "200g"),
             ("Popcorn", "100g")],
    "5612": [("Washing up liquid", "450ml"), ("Dishwasher tablets x30", "30pk"), ("Rinse aid", "500ml")],
    "6214": [("Moisturiser", "50ml"), ("Lip balm", "4.8g"), ("Mascara", "8ml"), ("Foundation", "30ml")],
}
OWN_BRAND = {"W": "Wrenfold", "G": "Gorsedale", "C": "Calderby's"}


def check_digit(body12):
    s = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(body12))
    return str((10 - s % 10) % 10)


def gtin(prefix, ref):
    body = (prefix + str(ref).zfill(12 - len(prefix)))[:12]
    return body + check_digit(body)


def price_point(x, lo=0.29):
    """A shelf price as the island's supermarkets set them: under a pound ending 5 or 9, above it ending 0, 5 or 9."""
    x = max(lo, x)
    pence = int(round(x * 100))
    ends = (5, 9) if pence < 100 else (0, 25, 29, 45, 49, 50, 69, 75, 79, 85, 89, 95, 99)
    mod = 10 if pence < 100 else 100
    cands = [p for p in range(pence - 12, pence + 13) if p % mod in ends and p > 0]
    return min(cands, key=lambda p: (abs(p - pence), p)) / 100.0


def brand_name(rng):
    return (rng.choice(SYL) + rng.choice(SYL)).capitalize()


def lines(seed):
    """Every product line (a GTIN at a retailer) with its fixed attributes."""
    rng = np.random.default_rng(seed)
    out = []
    makers = {}
    items = [(c, n, dip, rate, depth, tr, olg, lvl, counts) for c, n, dip, rate, depth, tr, olg, lvl, counts in W.ITEMS]
    items += [(c, n, 0.2, 0.18, (0.2, 0.3), 0.03, 0.0, lvl, (8, 6, 5)) for c, n, lvl in OUT_OF_SCOPE]
    ref = 1000
    for code, name, dip, rate, depth, trend, olgap, level, counts in items:
        # a pool of branded products per item, some stocked by two or three retailers under one GTIN
        nbrand = int(round(max(counts) * 0.95))
        pool = []
        for j in range(nbrand):
            v = VARIANTS[code][j % len(VARIANTS[code])]
            maker = makers.setdefault((code, j % 7), (brand_name(rng), "5" + str(int(rng.integers(0, 10))) +
                                                      str(int(rng.integers(10000, 99999)))))
            imported = rng.random() < 0.09
            ref += int(rng.integers(3, 40))
            g = gtin("00" + str(int(rng.integers(10000, 99999))), ref) if imported else gtin(maker[1], ref)
            pool.append({"gtin": g, "brand": maker[0], "variant": v[0], "size": v[1],
                         "rel": float(np.exp(rng.normal(0, 0.33))), "trend": float(trend - olgap * 0.3 + rng.normal(0, 0.010)),
                         "q": float(np.exp(rng.normal(0, 0.55))), "imported": imported})
        for r, n in zip(W.RETAILERS, counts):
            n_own = int(round(n * (0.36 if code == "1105" else 0.28)))
            stocked = list(rng.choice(len(pool), size=min(n - n_own, len(pool)), replace=False))
            for j in sorted(stocked):
                b = pool[j]
                out.append(dict(retailer=r, item=code, gtin=b["gtin"], own=False, imported=b["imported"],
                                desc="%s %s %s" % (b["brand"], b["variant"], b["size"]),
                                base=level * b["rel"] * float(np.exp(rng.normal(0, 0.05))),
                                trend=b["trend"] + float(rng.normal(0, 0.004)), q=b["q"] * float(np.exp(rng.normal(0, 0.2))),
                                dip=dip, rate=rate, depth=depth))
            for j in range(n_own):
                v = VARIANTS[code][int(rng.integers(0, len(VARIANTS[code])))]
                ref += int(rng.integers(3, 40))
                out.append(dict(retailer=r, item=code, gtin=gtin(W.OWN_PREFIX[r], ref), own=True, imported=False,
                                desc="%s %s %s" % (OWN_BRAND[r], v[0], v[1]),
                                base=level * 0.72 * float(np.exp(rng.normal(0, 0.25))),
                                trend=trend + olgap * 0.7 + float(rng.normal(0, 0.010)),
                                q=(3.4 if code == "1105" else 1.8) * float(np.exp(rng.normal(0, 0.5))), dip=dip,
                                rate=rate, depth=depth))
    return out


def monthly(seed, ls, nudge=None):
    """Each line's month-by-month truth: active, regular price, offer, shelf price, member share, units. Every line draws
    from its own stream, keyed by the world stream, its position and its item's nudge, so an item's lines can be re-drawn
    alone."""
    nudge = nudge if nudge is not None else W.NUDGE
    for idx, L in enumerate(ls):
        rng = np.random.default_rng([seed, idx, nudge.get(L["item"], 0)])
        nm = W.NM
        # range changes: a few lines arrive or leave inside the year, never at an offer
        s, e = 0, nm
        u = rng.random()
        if u < 0.07:
            s = int(rng.integers(2, 10))
        elif u < 0.13:
            e = int(rng.integers(5, 12))
        churn_q = 0.3 if (s > 0 or e < nm) else 1.0       # new lines start small, delisted lines were slow sellers
        L["start"], L["end"] = s, e
        # regular price: one or two reviews in the review months, the year's change about the line's trend
        steps = sorted(rng.choice(REVIEW_MONTHS, size=int(rng.integers(1, 3)), replace=False))
        p0 = price_point(L["base"])
        target = p0 * (1 + L["trend"])
        reg, cur = [], p0
        for m in range(nm):
            if m in steps:
                k = steps.index(m) + 1
                cur = price_point(p0 + (target - p0) * k / len(steps))
            reg.append(cur)
        L["reg"] = reg
        # offers: whole months, November to July, never in a line's first or last month
        offer = [False] * nm
        depth = [0.0] * nm
        for m in range(nm):
            if m in W.OFFER_FREE or m < s or m >= e or m == s or m == e - 1:
                continue
            if rng.random() < L["rate"] * float(np.exp(rng.normal(0, 0.25))):
                offer[m] = True
                depth[m] = float(rng.uniform(*L["depth"]))
        L["offer"] = offer
        L["shelf"] = [price_point(reg[m] * (1 - depth[m])) if offer[m] else reg[m] for m in range(nm)]
        # Wrenfold Rewards member prices on branded cheese and chocolate lines from March 2026
        L["member"] = (L["retailer"] == "W" and L["item"] in W.MEMBER_ITEMS and not L["own"] and rng.random() < 0.82)
        L["member_price"] = [price_point(L["shelf"][m] * 0.82) if (L["member"] and m >= W.MEMBER_START) else None
                             for m in range(nm)]
        L["member_share"] = [float(np.clip(rng.normal(0.60, 0.04), 0.45, 0.75)) if (L["member"] and m >= W.MEMBER_START)
                             else 0.0 for m in range(nm)]
        # units: a stocked-up month after an offer for goods that keep
        storable = L["dip"] >= 0.25
        boost = STORABLE_BOOST if storable else FRESH_BOOST
        season = SEASON.get(L["item"], [1.0] * nm)
        base_q = 160.0 * L["q"] * churn_q
        units = []
        for m in range(nm):
            if m < s or m >= e:
                units.append(0.0)
                continue
            q = base_q * season[m] * VISITORS[m]
            if L["item"] in TRADE_DOWN:
                q *= 1 + TRADE_DOWN[L["item"]][0 if L["own"] else 1] * m / (nm - 1)
            if offer[m]:
                q *= 1 + boost * depth[m] / 0.3
            elif m > 0 and offer[m - 1]:
                q *= 1 - L["dip"]
            units.append(q * float(np.exp(rng.normal(0, 0.06))))
        L["units"] = units
    return ls


def world(seed=None, nudge=None):
    seed = W.STREAM if seed is None else seed
    return monthly(seed, lines(seed), nudge)
