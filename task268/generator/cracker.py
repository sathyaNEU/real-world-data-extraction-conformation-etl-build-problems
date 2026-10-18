"""The cracker's and the mirror's paths on the two asks, measured.

Stage 2 (design): run with no argument, it builds the design prototype of the two ask files in memory (the
listing platform's export and the competitors' locator scrapes, at the counts the ask sheet sets) and scores
every route against the golden handling. Stage 3 rewires `load()` to the cut pack and checks.py runs it.

    python3 task268/generator/cracker.py
"""
import statistics
import sys

import numpy as np

SQFT_PER_M2 = 10.7639104
CORES = ["Halberdine", "Quillmere", "Corrisford", "Tessavon", "Ashcombe", "Dunnaway"]
AS_OF = "2026-09-30"


# ----------------------------------------------------------------------------------------------- prototype
def prototype(seed=268):
    """Listings and locator rows at the ask sheet's design counts (stage 2 only)."""
    r = np.random.default_rng(seed)
    # buildings per core: suites on the market, and whether the broker also posted the floor as one listing
    # buildings per core: suites on the market, and whether the broker also posted the floor as one listing;
    # `after` units were leased on the day after the date (available on 30 September, not by the export's status)
    plan = {"Halberdine": ([(2, True), (1, False), (2, False), (1, False), (1, False)], 0),
            "Quillmere": ([(2, True), (3, False), (2, True), (1, False)], 1),
            "Corrisford": ([(2, True), (1, False)], 2),
            "Tessavon": ([(2, True), (3, False), (2, True), (1, False), (1, False), (1, False)], 1),
            "Ashcombe": ([(2, True), (1, False), (1, False), (2, False), (1, False)], 0),
            "Dunnaway": ([(2, True), (1, False)], 2)}
    base = {"Halberdine": 334.0, "Quillmere": 296.0, "Corrisford": 312.0, "Tessavon": 409.0, "Ashcombe": 361.0, "Dunnaway": 237.0}
    listings, lid = [], 4410000
    for m in CORES:
        blds, after = plan[m]
        n = sum(k for k, roll in blds) + after
        assert n % 2 == 1, m
        # n rents per square metre a year, at least 7 dollars apart, the highest going to the combined floors' suites
        steps = np.cumsum(r.uniform(7, 16, n)); vals = list(base[m] + steps - steps[n // 2])
        need_hi = 2 * sum(1 for k, roll in blds if roll)
        hi, lo = vals[n - need_hi:], vals[:n - need_hi]
        r.shuffle(lo)
        bld = 0
        for k, roll in blds:
            bld += 1
            addr = "%d %s St" % (100 + 20 * bld, m[:4])
            suites = []
            for s in range(k):
                m2 = float(r.uniform(160, 214 if roll else 300 if k > 1 else 430))
                rent = hi.pop() if roll else lo.pop()
                basis = r.choice(["/SF/YR"] * 6 + ["/SF/MO", "/MO"])
                lid += int(r.integers(3, 40))
                sf = round(m2 * SQFT_PER_M2)
                quote = (round(rent / SQFT_PER_M2, 2) if basis == "/SF/YR" else round(rent / SQFT_PER_M2 / 12, 2)
                         if basis == "/SF/MO" else round(rent * (sf / SQFT_PER_M2) / 12))
                row = dict(listing_id="LX-%d" % lid, core=m, address=addr, suite=("%d" % (101 + s)) if k > 1 or r.random() < .5 else "",
                           floor="1", type=r.choice(["Retail", "Retail", "Flex"]), sf=sf, rent=quote, basis=basis,
                           status="Available", status_date="", listed="2026-%02d-%02d" % (int(r.integers(1, 9)), int(r.integers(1, 28))))
                listings.append(row); suites.append(row)
            if roll:
                sf = sum(x["sf"] for x in suites)
                yr = sum(rate_m2(x) * x["sf"] for x in suites) / sf / SQFT_PER_M2
                lid += int(r.integers(3, 40))
                listings.append(dict(listing_id="LX-%d" % lid, core=m, address=addr, suite="", floor="1", type=suites[0]["type"],
                                     sf=sf, rent=round(yr, 2), basis="/SF/YR", status="Available", status_date="",
                                     listed=max(x["listed"] for x in suites), rollup=True))
        for i in range(after):   # leased the day after the date: available on 30 September
            lid += int(r.integers(3, 40)); bld += 1
            listings.append(dict(listing_id="LX-%d" % lid, core=m, address="%d %s Ave" % (100 + 20 * bld, m[:4]), suite="",
                                 floor="1", type="Retail", sf=round(float(r.uniform(170, 420)) * SQFT_PER_M2),
                                 rent=round(lo.pop() / SQFT_PER_M2, 2), basis="/SF/YR", status="Leased", status_date="2026-10-01",
                                 listed="2026-04-20"))
        assert not hi and not lo, m
        # texture: upper floors, office space, out-of-range sizes, leased before the date, listed after it
        for kind in ["floor2", "office", "small", "large", "leased", "listed_after"]:
            lid += int(r.integers(3, 40)); bld += 1
            m2 = {"small": 120.0, "large": 520.0}.get(kind, float(r.uniform(170, 420)))
            listings.append(dict(listing_id="LX-%d" % lid, core=m, address="%d %s Ave" % (100 + 20 * bld, m[:4]), suite="",
                                 floor="2" if kind == "floor2" else "1", type="Office" if kind == "office" else "Retail",
                                 sf=round(m2 * SQFT_PER_M2), rent=round(base[m] * float(r.lognormal(0, .12)) / SQFT_PER_M2, 2),
                                 basis="/SF/YR", status="Leased" if kind == "leased" else "Available",
                                 status_date="2026-08-14" if kind == "leased" else "",
                                 listed="2026-10-01" if kind == "listed_after" else "2026-03-02"))

    dark = {"A": {"Halberdine": 3, "Quillmere": 2, "Corrisford": 4, "Tessavon": 2, "Ashcombe": 1, "Dunnaway": 1},
            "B": {"Halberdine": 2, "Quillmere": 3, "Corrisford": 1, "Tessavon": 2, "Ashcombe": 2, "Dunnaway": 0}}
    partners = {"Halberdine": 1, "Quillmere": 1, "Corrisford": 2, "Tessavon": 1, "Ashcombe": 1, "Dunnaway": 1}
    coloc = {"Quillmere", "Tessavon"}
    stores = []
    for m in CORES:
        n = 0
        for b in "AB":
            for i in range(dark[b][m]):
                n += 1
                stores.append(dict(brand=b, core=m, street="%d %s Rd" % (500 + 10 * n, m[:4]), unit="Unit %d" % (n % 4 + 1),
                                   services="Delivery" if r.random() < .6 else "Delivery, Pickup", partner=False))
            stores.append(dict(brand=b, core=m, street="%d %s Rd" % (900, m[:4]), unit="", services="Pickup", partner=False))  # pickup point
        if m in coloc:   # one brand-A and one brand-B dark store in the same building, different units
            stores.append(dict(brand="A", core=m, street="77 %s Wharf" % m[:4], unit="Unit 2", services="Delivery", partner=False))
            stores.append(dict(brand="B", core=m, street="77 %s Wharf" % m[:4], unit="Unit 6", services="Delivery", partner=False))
        for i in range(partners[m]):
            for b in "AB":
                stores.append(dict(brand=b, core=m, street="%d %s Market" % (40 + i, m[:4]), unit="", services="Delivery, Pickup", partner=True))
    return listings, stores, dark, partners, coloc


def rate_m2(x):
    """Asking rent in dollars per square metre per year, from the quote and its basis."""
    if x["basis"] == "/SF/YR":
        return x["rent"] * SQFT_PER_M2
    if x["basis"] == "/SF/MO":
        return x["rent"] * 12 * SQFT_PER_M2
    return x["rent"] * 12 / (x["sf"] / SQFT_PER_M2)


def available(x):
    if x["listed"] > AS_OF or x["floor"] != "1" or x["type"] not in ("Retail", "Flex"):
        return False
    if not 150 <= x["sf"] / SQFT_PER_M2 <= 450:
        return False
    return x["status"] == "Available" or (x["status_date"] and x["status_date"] > AS_OF)


# ----------------------------------------------------------------------------------------------- the routes
def ask_a(listings, route):
    out = {}
    for m in CORES:
        rows = [x for x in listings if x["core"] == m and available(x)]
        if route == "golden":     # a listing whose suites are all listed at its address is the same space again
            rows = [x for x in rows if not rollup_of(x, rows)]
        elif route == "overclean":  # one space per address
            seen, keep = set(), []
            for x in rows:
                if x["address"] not in seen:
                    seen.add(x["address"]); keep.append(x)
            rows = keep
        elif route == "natural":  # the status column read as it stands at the export
            rows = [x for x in rows if x["status"] == "Available"]
        rents = [rate_m2(x) for x in rows]
        out[m] = (len(rows), statistics.median(rents) if rents else None)
    return out


def rollup_of(x, rows):
    parts = [y for y in rows if y is not x and y["address"] == x["address"] and y["suite"]]
    return not x["suite"] and len(parts) >= 2 and abs(sum(y["sf"] for y in parts) - x["sf"]) <= 1


def ask_b(stores, route):
    out = {}
    live = [s for s in stores if "Delivery" in s["services"]]
    key = lambda s: (s["street"], s["unit"])
    both = {key(s) for s in live if s["brand"] == "A"} & {key(s) for s in live if s["brand"] == "B"}
    streets = {s["street"] for s in live if s["brand"] == "A"} & {s["street"] for s in live if s["brand"] == "B"}
    for b in "AB":
        for m in CORES:
            rows = [s for s in live if s["brand"] == b and s["core"] == m]
            if route == "golden":
                rows = [s for s in rows if key(s) not in both]
            elif route == "overclean":
                rows = [s for s in rows if s["street"] not in streets]
            out[(b, m)] = len(rows)
    return out


def main():
    listings, stores, dark, partners, coloc = prototype()
    gold_a, gold_b = ask_a(listings, "golden"), ask_b(stores, "golden")
    for m in CORES:
        assert gold_a[m][0] % 2 == 1, "an even count makes the median a convention"
    assert all(gold_b[(b, m)] == dark[b][m] + (1 if m in coloc else 0) for b in "AB" for m in CORES)
    rows, keeps = [], {}
    for route in ("cracker", "natural", "overclean"):
        a = ask_a(listings, route if route != "cracker" else "plain")
        bb = ask_b(stores, route if route != "cracker" else "plain")
        hit_a = sum(a[m][0] == gold_a[m][0] for m in CORES) + sum(
            a[m][1] is not None and round(a[m][1]) == round(gold_a[m][1]) for m in CORES)
        hit_b = sum(bb[k] == gold_b[k] for k in gold_b)
        keeps[route] = (hit_a, hit_b)
        rows.append((route, hit_a, hit_b))
    print("golden  A:", {m: (gold_a[m][0], round(gold_a[m][1])) for m in CORES})
    print("golden  B:", {"%s %s" % k: v for k, v in gold_b.items()})
    plain_a, plain_b = ask_a(listings, "plain"), ask_b(stores, "plain")
    print("cracker A:", {m: (plain_a[m][0], round(plain_a[m][1])) for m in CORES})
    print("cracker B:", {"%s %s" % k: v for k, v in plain_b.items()})
    for route, ha, hb in rows:
        print("%-9s keeps A %2d of 12, B %2d of 12" % (route, ha, hb))
    # the pair on Part 0's weights: the cracker lands the call (38 + 7), the mirror keeps about 5 of the
    # recommendation side and the 7 of instruction-following; both take the asks the same way.
    ask_w = 55.0
    kept_c = (keeps["cracker"][0] + keeps["cracker"][1]) / 24.0
    pair = ((38 + 7 + ask_w * kept_c) + (5 + 7 + ask_w * kept_c)) / 2
    print("cracker keeps %d of 24 ask figures; mirror the same; pair ceiling %.1f" % (keeps["cracker"][0] + keeps["cracker"][1], pair))
    return 0 if keeps["cracker"] == (0, 0) else 1


if __name__ == "__main__":
    sys.exit(main())
