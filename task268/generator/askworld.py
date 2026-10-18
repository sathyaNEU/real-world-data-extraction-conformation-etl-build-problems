"""The asks' records: the listing service's export of retail and flex space in the six central counties, and the
competitors' store locators as the market team scraped them each Wednesday of 2026. Neither touches a file the
call reads.

Ask A's device: where two ground-floor suites of a building are on the market, the broker posts each suite and, for
some buildings, the floor as one listing too, its suite blank, its size the suites' sum and its rent their
area-weighted mean. Ask B's device: both competitors list independent convenience shops that fill their delivery
orders beside their own dark stores, each such shop in both locators at the same address and unit."""
import datetime as dt
import math

import numpy as np

import common as K
import world as W

STREETS = ["Main", "Market", "Harbor", "Union", "Front", "Church", "Mill", "Water", "Locust", "Chestnut", "Walnut", "Spring",
           "Canal", "Commerce", "Depot", "Liberty", "Court", "Bridge", "Grove", "Prospect", "Summit", "Pearl", "Garden",
           "Franklin", "Jefferson", "Madison", "Monroe", "Jackson", "Adams", "Lincoln", "Ninth", "Fourth", "Second"]
SUFFIX = ["St", "Ave", "Blvd", "Way", "Rd", "Pl"]
ZIP3 = {"OH": 432, "IN": 469, "NC": 285, "CO": 801, "MO": 650, "TN": 371}
BROKERS = ["Orrmond Realty Partners", "Pike & Calloway Commercial", "Northgate Retail Advisors", "Larkfield Commercial",
           "Ambler Ross", "Keystone Tenant Services", "Bellweather Property Group", "Hartigan & Doyle"]
BASE_RENT = {"Halberdine": 334.0, "Quillmere": 296.0, "Corrisford": 312.0, "Tessavon": 409.0, "Ashcombe": 361.0,
             "Dunnaway": 237.0}       # asking rent, dollars per m2 a year, at the middle of each core's units
# Ask A design per core: buildings (suites on the market, and whether the floor is also listed whole), and units
# leased on 1 October (on the market on 30 September, Leased in the export)
PLAN_A = {"Halberdine": ([(2, True), (1, False), (2, False), (1, False), (1, False)], 0),
          "Quillmere": ([(2, True), (3, False), (2, True), (1, False)], 1),
          "Corrisford": ([(2, True), (1, False)], 2),
          "Tessavon": ([(2, True), (3, False), (2, True), (1, False), (1, False), (1, False)], 1),
          "Ashcombe": ([(2, True), (1, False), (1, False), (2, False), (1, False)], 0),
          "Dunnaway": ([(2, True), (1, False)], 2)}
# Ask B design per core: each brand's dark stores delivering on 30 September, the partner shops both list, and the
# cores where a Tilldash and a Hopcrate dark store share a building
PLAN_B = {"Halberdine": ((3, 2), 1), "Quillmere": ((3, 3), 1), "Corrisford": ((4, 1), 2), "Tessavon": ((2, 2), 1),
          "Ashcombe": ((1, 2), 1), "Dunnaway": ((1, 0), 1)}
COLOC = {"Quillmere", "Tessavon"}
SCRAPES = [dt.date(2026, 1, 7) + dt.timedelta(weeks=k) for k in range(39)]


def zipcode(M, t, r=None):
    h = int(t["geoid"][-6:]) // 100
    return "%03d%02d" % (ZIP3[M["metro"]["st"]], 1 + (h * 7 + int(t["geoid"][2:5])) % 38)


class Addr:
    def __init__(self, r):
        self.r, self.used = r, set()

    def new(self):
        while True:
            a = "%d %s %s" % (int(self.r.integers(1, 40)) * 20 + int(self.r.integers(0, 2)) * int(self.r.integers(1, 19)),
                              STREETS[int(self.r.integers(len(STREETS)))], SUFFIX[int(self.r.integers(len(SUFFIX)))])
            if a not in self.used:
                self.used.add(a)
                return a


def quote(r, rate_m2, sf):
    """The rent as the broker quotes it: per square foot a year (most), per square foot a month, or the monthly total."""
    u = r.random()
    if u < .80:
        return round(rate_m2 / K.SQFT_PER_M2, 2), "/SF/YR"
    if u < .91:
        return round(rate_m2 / K.SQFT_PER_M2 / 12, 2), "/SF/MO"
    return round(rate_m2 * sf / K.SQFT_PER_M2 / 12 / 5) * 5.0, "/MO"


def rate_m2(x):
    if x["rent_basis"] == "/SF/YR":
        return x["asking_rent"] * K.SQFT_PER_M2
    if x["rent_basis"] == "/SF/MO":
        return x["asking_rent"] * 12 * K.SQFT_PER_M2
    return x["asking_rent"] * 12 / (x["space_sf"] / K.SQFT_PER_M2)


def listings(Wd, seed=W.SEED):
    out = []
    lid = [5130000]

    def nid(r):
        lid[0] += int(r.integers(4, 260))
        return "L%d" % lid[0]

    for i, M in enumerate(Wd["metros"]):
        name = M["metro"]["name"]
        r = np.random.default_rng([seed, 71, i])
        ad = Addr(r)
        core = [t for t in M["tracts"] if t["core"] and t["kind"] != "water"]
        cbd = [t for t in core if t["kind"] == "cbd"]
        noncore = [t for t in M["tracts"] if t["county"] == M["central"] and not t["core"]]
        city, st = name, M["metro"]["st"]

        def row(t, addr, suite, ptype, floor, m2, rate, status, sdate, listed, broker, rollup=False):
            sf = int(round(m2 * K.SQFT_PER_M2 / 5) * 5)
            rent, basis = quote(r, rate, sf)
            return dict(listing_id=nid(r), address=addr, suite=suite, city=city, state=st, zip=zipcode(M, t),
                        census_tract=t["geoid"], property_type=ptype, floor=floor, space_sf=sf, asking_rent=rent,
                        rent_basis=basis, lease_type="NNN" if ptype in ("Retail", "Flex") else "FSG", status=status,
                        status_date=sdate, date_listed=listed, broker=broker, metro=name, core=t["core"], rollup=rollup)

        def listed_date():
            d = dt.date(2025, 10, 1) + dt.timedelta(days=int(r.integers(0, 350)))
            return d.isoformat()

        blds, after = PLAN_A[name]
        n = sum(k for k, roll in blds) + after
        assert n % 2 == 1
        steps = np.cumsum(r.uniform(9, 19, n))
        vals = list(BASE_RENT[name] + steps - steps[n // 2])
        need_hi = 2 * sum(1 for k, roll in blds if roll)
        hi, lo = vals[n - need_hi:], vals[:n - need_hi]
        r.shuffle(lo)
        for k, roll in blds:
            t = cbd[int(r.integers(len(cbd)))] if r.random() < .5 else core[int(r.integers(len(core)))]
            addr = ad.new()
            broker = BROKERS[int(r.integers(len(BROKERS)))]
            ptype = "Retail" if r.random() < .7 else "Flex"
            listed = listed_date()
            suites = []
            for s in range(k):
                m2 = float(r.uniform(161, 212)) if roll else float(r.uniform(165, 290 if k > 1 else 430))
                rate = hi.pop() if roll else lo.pop()
                suite = ("%d" % (100 + 2 * s + 1) if r.random() < .6 else chr(65 + s)) if k > 1 else ("" if r.random() < .55 else "1A")
                x = row(t, addr, suite, ptype, "1", m2, rate, "Available", "", listed, broker)
                suites.append(x)
                out.append(x)
            if roll:
                sf = sum(x["space_sf"] for x in suites)
                yr = sum(rate_m2(x) * x["space_sf"] for x in suites) / sf / K.SQFT_PER_M2
                x = dict(suites[0])
                x.update(listing_id=nid(r), suite="", space_sf=sf, asking_rent=round(yr, 2), rent_basis="/SF/YR",
                         date_listed=max(s["date_listed"] for s in suites), rollup=True)
                out.append(x)
        for j in range(after):
            t = core[int(r.integers(len(core)))]
            out.append(row(t, ad.new(), "", "Retail", "1", float(r.uniform(180, 410)), lo.pop(), "Leased", "2026-10-01",
                           listed_date(), BROKERS[int(r.integers(len(BROKERS)))]))
        assert not hi and not lo
        # texture inside the core: upper floors, offices, units outside the size band, leased or withdrawn before the
        # date, listed after it, and a combined floor too large for the band
        for kind in ["floor2", "office", "small", "large", "leased", "withdrawn", "listed_after", "lower", "big_roll"]:
            t = core[int(r.integers(len(core)))]
            m2 = {"small": float(r.uniform(70, 138)), "large": float(r.uniform(470, 900))}.get(kind, float(r.uniform(170, 420)))
            rate = BASE_RENT[name] * float(r.lognormal(0, .14))
            if kind == "big_roll":
                addr, broker, listed = ad.new(), BROKERS[int(r.integers(len(BROKERS)))], listed_date()
                parts = []
                for s in range(3):
                    x = row(t, addr, chr(65 + s), "Retail", "1", float(r.uniform(205, 260)), rate * float(r.lognormal(0, .05)),
                            "Leased", "2026-0%d-%02d" % (int(r.integers(4, 9)), int(r.integers(1, 28))), listed, broker)
                    parts.append(x)
                    out.append(x)
                sf = sum(x["space_sf"] for x in parts)
                x = dict(parts[0])
                x.update(listing_id=nid(r), suite="", space_sf=sf, asking_rent=round(rate / K.SQFT_PER_M2, 2), rent_basis="/SF/YR")
                out.append(x)
                continue
            out.append(row(t, ad.new(), "" if r.random() < .5 else "2B", "Office" if kind == "office" else "Retail",
                           {"floor2": "2", "lower": "LL"}.get(kind, "1"), m2, rate,
                           {"leased": "Leased", "withdrawn": "Withdrawn"}.get(kind, "Available"),
                           {"leased": "2026-08-%02d" % int(r.integers(1, 28)), "withdrawn": "2026-07-%02d" % int(r.integers(1, 28))}.get(kind, ""),
                           "2026-10-01" if kind == "listed_after" else listed_date(), BROKERS[int(r.integers(len(BROKERS)))]))
        # the rest of the central county: everything the export holds outside the core
        for j in range(int(r.integers(70, 120))):
            t = noncore[int(r.integers(len(noncore)))]
            k = 1 if r.random() < .75 else int(r.integers(2, 4))
            addr, broker, listed = ad.new(), BROKERS[int(r.integers(len(BROKERS)))], listed_date()
            ptype = ["Retail", "Retail", "Flex", "Office", "Industrial"][int(r.integers(5))]
            u = r.random()
            status, sdate = (("Available", "") if u < .62 else ("Leased", "2026-%02d-%02d" % (int(r.integers(1, 10)), int(r.integers(1, 28))))
                             if u < .9 else ("Withdrawn", "2026-%02d-%02d" % (int(r.integers(1, 10)), int(r.integers(1, 28)))))
            parts = []
            for s in range(k):
                m2 = float(r.lognormal(math.log(260), .6))
                x = row(t, addr, ("%d" % (100 + 2 * s + 1)) if k > 1 else "", ptype, "1" if r.random() < .82 else "2", m2,
                        BASE_RENT[name] * .85 * float(r.lognormal(0, .2)), status, sdate, listed, broker)
                parts.append(x)
                out.append(x)
            if k > 1 and r.random() < .4:
                sf = sum(x["space_sf"] for x in parts)
                x = dict(parts[0])
                x.update(listing_id=nid(r), suite="", space_sf=sf,
                         asking_rent=round(sum(rate_m2(p) * p["space_sf"] for p in parts) / sf / K.SQFT_PER_M2, 2),
                         rent_basis="/SF/YR", rollup=True)
                out.append(x)
    order = np.random.default_rng([seed, 72]).permutation(len(out))
    return [out[i] for i in order]


def locators(Wd, seed=W.SEED):
    """One row per store per brand per weekly scrape. Returns the rows and the design truth per core."""
    rows = []
    code = {"Tilldash": [1040], "Hopcrate": [301]}
    hours = {"Tilldash": ["07:00-23:00", "07:00-24:00", "08:00-23:00"], "Hopcrate": ["08:00-22:00", "08:00-23:00", "07:00-23:00"]}
    stores = []   # dict: brand, code, name, addr, unit, tract, lat, lon, services, hours, first, last, partner, core, metro

    def new_code(b, r):
        code[b][0] += int(r.integers(1, 9))
        return ("TD-%04d" if b == "Tilldash" else "HC%05d") % code[b][0]

    for i, M in enumerate(Wd["metros"]):
        name = M["metro"]["name"]
        r = np.random.default_rng([seed, 81, i])
        ad = Addr(r)
        core = [t for t in M["tracts"] if t["core"] and t["kind"] != "water"]
        noncore = [t for t in M["tracts"] if t["county"] == M["central"] and not t["core"]]
        zones = ["Downtown", "Midtown", "Riverside", "Old Town", "Northside", "Westgate", "Eastside", "Southbank",
                 "Mill District", "Union Square", "Hillcrest", "Parkview", "Lakeside", "Harbor Point", "College Hill"]

        def site(t):
            """A building's own point, inside its tract."""
            return t["lat"] + float(r.normal(0, .002)), t["lon"] + float(r.normal(0, .002))

        def place(t, addr, unit, b, kind, first, last, hrs=None, at=None):
            la, lo = at or site(t)
            s = dict(brand=b, code=new_code(b, r), name="%s %s" % (b, zones[int(r.integers(len(zones)))]),
                     addr=addr, unit=unit, tract=t["geoid"], lat=la + float(r.normal(0, .00012)),
                     lon=lo + float(r.normal(0, .00012)), city=name, st=M["metro"]["st"], zip=zipcode(M, t),
                     services={"dark": "Delivery" if r.random() < .55 else "Delivery, Pickup", "pickup": "Pickup",
                               "partner": "Delivery, Pickup"}[kind],
                     hours=hrs or hours[b][int(r.integers(3))], first=first, last=last, partner=kind == "partner",
                     core=t["core"], metro=name, kind=kind)
            stores.append(s)
            return s

        (n_td, n_hc), n_partner = PLAN_B[name]
        for b, n in (("Tilldash", n_td), ("Hopcrate", n_hc)):
            for k in range(n):
                t = core[int(r.integers(len(core)))]
                first = SCRAPES[0] if r.random() < .7 else SCRAPES[int(r.integers(4, 30))]
                place(t, ad.new(), "Unit %d" % int(r.integers(1, 9)) if r.random() < .5 else "", b, "dark", first, SCRAPES[-1])
            # a pickup point in the core, and a dark store that closed in the summer
            t = core[int(r.integers(len(core)))]
            place(t, ad.new(), "", b, "pickup", SCRAPES[int(r.integers(0, 10))], SCRAPES[-1])
            t = core[int(r.integers(len(core)))]
            place(t, ad.new(), "", b, "dark", SCRAPES[0], SCRAPES[int(r.integers(18, 30))])
        if name in COLOC:   # one building, a Tilldash and a Hopcrate dark store in different units
            t = core[int(r.integers(len(core)))]
            addr, at = ad.new(), site(t)
            place(t, addr, "Unit 2", "Tilldash", "dark", SCRAPES[0], SCRAPES[-1], at=at)
            place(t, addr, "Unit 6", "Hopcrate", "dark", SCRAPES[int(r.integers(2, 12))], SCRAPES[-1], at=at)
        for k in range(n_partner):
            t = core[int(r.integers(len(core)))]
            addr, unit = ad.new(), "" if r.random() < .6 else "Suite %d" % int(r.integers(1, 5))
            hrs = ["06:00-23:00", "06:00-24:00", "07:00-22:00", "00:00-24:00"][int(r.integers(4))]
            at = site(t)
            for b in ("Tilldash", "Hopcrate"):
                place(t, addr, unit, b, "partner", SCRAPES[int(r.integers(0, 14))], SCRAPES[-1], hrs, at=at)
        # stores outside the core: dark stores, pickup points and partner shops across the rest of the county
        for b in ("Tilldash", "Hopcrate"):
            for k in range(int(r.integers(4, 9))):
                t = noncore[int(r.integers(len(noncore)))]
                place(t, ad.new(), "", b, "dark" if r.random() < .8 else "pickup", SCRAPES[int(r.integers(0, 20))],
                      SCRAPES[-1] if r.random() < .85 else SCRAPES[int(r.integers(22, 36))])
        for k in range(int(r.integers(1, 4))):
            t = noncore[int(r.integers(len(noncore)))]
            addr = ad.new()
            hrs = ["06:00-23:00", "07:00-23:00", "00:00-24:00"][int(r.integers(3))]
            at = site(t)
            for b in ("Tilldash", "Hopcrate"):
                place(t, addr, "", b, "partner", SCRAPES[int(r.integers(0, 20))], SCRAPES[-1], hrs, at=at)
        # a dark store that moved during the year, under its code, from outside the core into it (Tilldash) or out
        t_old, t_new = noncore[int(r.integers(len(noncore)))], core[int(r.integers(len(core)))]
        s = place(t_old, ad.new(), "", "Tilldash", "dark", SCRAPES[0], SCRAPES[-1])
        s["moved"] = (SCRAPES[int(r.integers(20, 30))], t_new["geoid"], ad.new(), t_new)
    out = []
    r = np.random.default_rng([seed, 82])
    for d in SCRAPES:
        for s in stores:
            if not (s["first"] <= d <= s["last"]):
                continue
            if d != SCRAPES[-1] and r.random() < .015:     # the locator's paging dropped the store that week
                continue
            tract, addr, lat, lon, zp = s["tract"], s["addr"], s["lat"], s["lon"], s["zip"]
            if s.get("moved") and d >= s["moved"][0]:
                tn = s["moved"][3]
                tract, addr, lat, lon = s["moved"][1], s["moved"][2], tn["lat"] + .0011, tn["lon"] - .0007
            out.append(dict(scrape_date=d.isoformat(), brand=s["brand"], store_code=s["code"], store_name=s["name"],
                            address=addr, unit=s["unit"], city=s["city"], state=s["st"], zip=zp,
                            latitude=round(lat, 6), longitude=round(lon, 6), census_tract=tract, services=s["services"],
                            hours=s["hours"]))
    out.sort(key=lambda x: (x["scrape_date"], x["brand"], x["store_code"]))
    return out, stores
