"""The workplace returns of March 2026 and March 2027: every workplace line on every payroll account's return, adding up
to the Agency's municipality by sector cells for those months. Employers: the province-wide employers whose account
address is in Wickmoor or Saltmere (their workplaces elsewhere are the branch jobs), each region's school division
(teachers and support staff paid from two accounts, both listing every school), and the local businesses.

Between the two months workplaces close, open, grow and shrink; some change hands (the buyer's account reports the
same workplace under its own number), and some move from one of an employer's accounts to another."""
import collections

import numpy as np

import sim as S
import world as W

SIZE = {  # median and log-sd of a workplace's jobs by sector, local businesses
    "11": (5, 0.9), "21": (40, 0.9), "22": (12, 0.7), "23": (6, 1.0), "31-33": (18, 1.1), "41": (8, 0.9),
    "44-45": (9, 0.9), "48-49": (8, 1.0), "51": (6, 0.9), "52": (8, 0.7), "53": (3, 0.8), "54": (4, 1.0),
    "55": (10, 0.8), "56": (8, 1.1), "61": (12, 1.0), "62": (7, 1.1), "71": (6, 1.0), "72": (11, 0.8),
    "81": (4, 0.8), "91": (14, 0.9),
}
BRANCH_SIZE = {"62": (70, 0.8), "21": (120, 0.6), "31-33": (90, 0.6), "11": (25, 0.6), "44-45": (32, 0.5),
               "22": (18, 0.5), "48-49": (14, 0.6), "52": (12, 0.4), "91": (22, 0.6)}

ROOTS = """Acorn Alder Amber Anchor Arbour Arden Argent Ashcroft Aspen Bayview Beacon Bellmoor Birchwood Blackwater
Bluewater Bramble Briar Bridgewater Brightwater Broadleaf Brookside Cairn Castlegate Cedarline Clearwater
Cloverleaf Coastal Cobble Copperline Cornerstone Cove Crescent Crestview Crossroads Deepwater Driftwood
Eastgate Edgewater Elmwood Evergreen Fairhaven Falcon Fernhill Fieldstone Firside Flatrock Foxglove Gable
Garnet Gateway Glenview Goldleaf Granite Greystone Harbourside Harvest Hawthorn Heartland Heron Highland
Hillcrest Homestead Horizon Ironwood Juniper Keystone Lakeside Landmark Larch Laurel Ledgerock Lighthouse
Linden Lodgepole Longview Maple Marigold Meadowlark Millrace Milestone Moorland Northgate Northstar Oakridge
Orchard Outpost Pebble Pinecrest Plainview Prairie Quarry Quayside Ravine Redwood Ridgeline Riverbend Rockport
Rosewood Saddleback Sandpiper Sawmill Seabreeze Shoreline Silverleaf Skyline Spruce Steeple Stonebridge Summit
Sunrise Tamarack Thistle Timberline Topsail Trillium Upland Valleyview Vantage Waterford Westbrook Whitecap
Wildrose Willow Windward Woodland Yarrow""".split()
TRADES = {
    "11": ("Farms", "Fisheries", "Forestry Services", "Greenhouses", "Livestock"),
    "21": ("Drilling", "Exploration", "Quarry"),
    "22": ("Utilities", "Water Services"),
    "23": ("Construction", "Contracting", "Builders", "Excavating", "Roofing", "Electric", "Plumbing and Heating"),
    "31-33": ("Manufacturing", "Fabricating", "Bakery", "Woodworks", "Machining", "Printing", "Seafood Processors"),
    "41": ("Distributors", "Supply", "Wholesale", "Equipment Sales"),
    "44-45": ("Hardware", "Pharmacy", "Grocery", "Outfitters", "Auto Sales", "Home Centre", "Books and Gifts"),
    "48-49": ("Trucking", "Transport", "Courier", "Freight", "Bus Lines"),
    "51": ("Media", "Communications", "Printing House"),
    "52": ("Insurance Brokers", "Financial", "Investments"),
    "53": ("Properties", "Realty", "Rentals"),
    "54": ("Engineering", "Accounting", "Law Office", "Surveying", "Consulting", "Design"),
    "55": ("Holdings", "Management"),
    "56": ("Cleaning Services", "Security", "Staffing", "Landscaping", "Waste Services"),
    "61": ("Learning Centre", "Academy", "Tutoring", "Driving School"),
    "62": ("Dental Clinic", "Physiotherapy", "Home Care", "Medical Clinic", "Child Care Centre", "Seniors Residence"),
    "71": ("Golf Club", "Fitness", "Recreation", "Arena"),
    "72": ("Restaurant", "Inn", "Cafe", "Diner", "Lodge", "Pizza", "Motel"),
    "81": ("Auto Repair", "Hair Studio", "Laundry", "Repair Shop", "Pet Care"),
    "91": ("Services Board", "Library Board", "Housing Authority"),
}
SUFFIX = ("Ltd.", "Ltd.", "Ltd.", "Inc.", "Inc.", "Limited", "Corp.")
SURNAMES = """Abbott Andersen Arsenault Babcock Bergeron Bhatt Boucher Brar Cardinal Chan Chiasson Cormier Dhaliwal
Doucette Dube Fehr Friesen Gill Goertzen Hiebert Horvath Hutchinson Janzen Klassen Kowalchuk Lalonde Lam Leclerc
MacKay MacLeod Mahoney McAllister Mercier Nakamura Nguyen Olsen Ouellette Penner Petrenko Poirier Quinlan Rempel
Sandhu Schultz Sorensen Tanaka Thiessen Toews Vandermeer Wiebe Yakimchuk Zacharias""".split()
# trade names that several numbered companies operate under (franchisees and buying groups)
BRANDS = {"72": ("Tallgrass Coffee", "Pennant Pizza", "Kettlewick Bakery Cafe"),
          "44-45": ("Brightvale Pharmacy", "Larchmere Grocer", "Trailcraft Outfitters"),
          "81": ("Quickturn Auto Service", "Foldwell Laundry"),
          "62": ("Ridgeway Dental Centre", "Motionworks Physiotherapy"),
          "56": ("Steadfast Security",), "61": ("Brightpath Tutoring",)}
HOURLY = (" - Hourly", " - Seasonal", " - Part-time", "")
STREET_NAMES = """Main Mill Church Water King Queen Victoria Albert Railway Station Bridge Park River Lake Hill Pine Maple
Oak Elm Cedar Birch Spruce Willow Harbour Front Shore Bay Market Prince George Edward Union Centre School College
Industrial Commerce Airport Highland Ridge Valley Meadow Orchard Forest Granite Copper Iron Mineral Pioneer Prospect
Garrison Farm Field Dock Wharf Quarry Lighthouse Fisher Ferry Lodge Summit""".split()
STREET_TYPES = ("Street", "Street", "Road", "Road", "Avenue", "Drive", "Way", "Crescent", "Lane", "Boulevard")


def luhn_bn(g):
    """a nine-digit business number whose last digit checks the first eight"""
    d = [int(x) for x in str(g.integers(10 ** 7, 10 ** 8))]
    total = 0
    for k, x in enumerate(d):
        y = x * (2 if k % 2 == 1 else 1)
        total += y // 10 + y % 10
    return "".join(map(str, d)) + str((10 - total % 10) % 10)


RURAL = {"Dowrie", "Fallow Creek", "Ivory Crossing", "Cobbleford Flats", "Tarnbury", "Wexleigh-Dorran", "Wexleigh", "Dorran",
         "Brackenholt", "Corriemoor", "High Tolland", "Rushby", "Blackrill", "Sorrel Lake", "Coldmarsh Ridge",
         "Brockmere", "Rossmuir", "Wrayburn", "Lindmere Park"}
PUBLIC_BODIES = ("Public Library Board", "Housing Authority", "Recreation Commission", "Planning District Commission",
                 "Water Board")


class Registry:
    """business numbers, legal names and addresses, each issued once"""

    def __init__(self):
        self.g = S.rng("registry")
        self.gn = S.rng("names")
        self.bns, self.names, self.addresses = set(), set(), set()
        self.street = {}

    def bn(self):
        while True:
            b = luhn_bn(self.g)
            if b not in self.bns:
                self.bns.add(b)
                return b

    def former_name(self, sector, trade):
        """the legal name a business carried before a rename: another name in the same trade"""
        g = self.gn
        for _ in range(400):
            u = g.random()
            stem = SURNAMES[g.integers(len(SURNAMES))] if u < 0.3 else ROOTS[g.integers(len(ROOTS))]
            nm = self._unique("%s %s %s" % (stem, trade, SUFFIX[g.integers(len(SUFFIX))]))
            if nm:
                return nm
        raise RuntimeError("names exhausted")

    def _unique(self, nm):
        if nm in self.names:
            return None
        self.names.add(nm)
        return nm

    def business(self, sector, place=None):
        """a business's legal name and the name it operates under: named for a feature or its town, for a family,
        for initials, or a numbered company trading under a name of its own or a franchise's"""
        g = self.gn
        for _ in range(400):
            trade = TRADES[sector][g.integers(len(TRADES[sector]))]
            self.last_trade = trade
            if sector == "91":                             # a local board or authority: no corporate suffix
                legal = self._unique("%s %s" % (place if (place and g.random() < 0.5) else ROOTS[g.integers(len(ROOTS))], trade))
                if legal is None:
                    continue
                return legal, legal
            suf = SUFFIX[g.integers(len(SUFFIX))]
            u = g.random()
            if u < 0.13:                                   # numbered company
                legal = self._unique("%d Canada Inc." % int(g.integers(1100000, 16400000)))
                if legal is None:
                    continue
                if sector in BRANDS and g.random() < 0.45:
                    op = BRANDS[sector][g.integers(len(BRANDS[sector]))]
                else:
                    op = "%s %s" % (ROOTS[g.integers(len(ROOTS))], trade)
                return legal, op
            if u < 0.33:                                   # a family's
                sn = SURNAMES[g.integers(len(SURNAMES))]
                form = g.random()
                if form < 0.2:
                    legal = "%s & Sons %s %s" % (sn, trade, suf)
                elif form < 0.35 and sector in ("54", "23", "62"):
                    legal = "%s and %s %s %s" % (sn, SURNAMES[g.integers(len(SURNAMES))], trade, suf)
                else:
                    legal = "%s %s %s" % (sn, trade, suf)
                legal = self._unique(legal)
                if legal is None:
                    continue
                op = legal.rsplit(" ", 1)[0]
                if sector in ("72", "44-45", "81") and g.random() < 0.35:
                    op = "%s's %s" % (sn, trade)
                return legal, op
            if u < 0.38:                                   # initials
                a, b = (chr(65 + int(x)) for x in g.integers(0, 26, 2))
                legal = self._unique(("%s & %s %s %s" if g.random() < 0.5 else "%s.%s. %s %s") % (a, b, trade, suf))
                if legal is None:
                    continue
                return legal, legal.rsplit(" ", 1)[0]
            root = place if (place and g.random() < 0.2) else ROOTS[g.integers(len(ROOTS))]
            if g.random() < 0.12:                          # a holding name, trading under another
                legal = self._unique("%s %s %s" % (root, ("Holdings", "Enterprises", "Ventures")[g.integers(3)], suf))
                if legal is None:
                    continue
                return legal, "%s %s" % (ROOTS[g.integers(len(ROOTS))], trade)
            legal = self._unique("%s %s %s" % (root, trade, suf))
            if legal is None:
                continue
            return legal, legal.rsplit(" ", 1)[0]
        raise RuntimeError("names exhausted")

    def public_body(self, muni):
        for body in PUBLIC_BODIES:
            nm = "%s %s" % (W.MUNI_NAME[muni], body)
            if nm not in self.names:
                self.names.add(nm)
                return nm
        return self.business("91", None)[0]

    def address(self, muni, suite=False):
        streets = self.street.setdefault(muni, [])
        if not streets:
            g = S.rng("streets", muni)
            names = list(STREET_NAMES)
            g.shuffle(names)
            k = 26 if muni in ("0101", "0301") else 9
            for nm in names[:k]:
                streets.append("%s %s" % (nm, STREET_TYPES[g.integers(len(STREET_TYPES))]))
        city = muni in ("0101", "0301")
        rural = W.MUNI_NAME[muni] in RURAL
        for _ in range(500):
            u = self.g.random()
            num = int(self.g.integers(1, 2400 if city else 900))
            if city and u < 0.3:
                st = "%d %s" % (int(self.g.integers(1, 60)), ("Street", "Avenue")[self.g.integers(2)])
                num = int(self.g.integers(100, 12000))
            elif rural and u < 0.35:
                st = ("Highway %d" % (2, 7, 13, 16, 21, 39)[self.g.integers(6)]) if u < 0.18 else \
                    "%s Road %d" % (("Range", "Township")[self.g.integers(2)], int(self.g.integers(10, 290)))
                num = int(self.g.integers(1000, 59000))
            else:
                st = streets[self.g.integers(len(streets))]
                if city and self.g.random() < 0.25:
                    st += " " + ("North", "South", "East", "West")[self.g.integers(4)]
            if suite and self.g.random() < 0.5:
                a = "Suite %d, %d %s" % (int(self.g.integers(1, 9)) * 100 + int(self.g.integers(0, 20)), num, st)
            elif not city and not rural and self.g.random() < 0.08:
                a = "Unit %d, %d %s" % (int(self.g.integers(1, 12)), num, st)
            else:
                a = "%d %s" % (num, st)
            if (muni, a) not in self.addresses:
                self.addresses.add((muni, a))
                return a
        raise RuntimeError("addresses exhausted")


def _split(total, median, sd, g):
    """split total jobs into workplace sizes drawn around median"""
    if total <= 0:
        return []
    sizes = []
    while sum(sizes) < total:
        sizes.append(max(1.0, float(np.exp(np.log(median) + g.normal(0, sd)))))
    v = np.array(sizes)
    ints = S._largest_remainder(v, total)
    return [int(x) for x in ints if x > 0]


class Account:
    def __init__(self, bn, ref, legal, operating):
        self.bn, self.ref, self.legal, self.operating = bn, ref, legal, operating
        self.number = "%sRP%s" % (bn, ref)
        self.next_no = 1

    def workplace_no(self):
        k = self.next_no
        self.next_no += 1
        return "%03d" % k


def build(R, cells26, cells27):
    """the workplace lines of both months: {month: [dict]}, and the record of what happened to each workplace"""
    Sh = S.Shares(R)
    own, br = S.own_branch(R)
    reg = Registry()
    g = S.rng("firms")
    lines = {"2026-03": [], "2027-03": []}
    wp = []          # every workplace: dict(id, muni, sector, address, kind, account(s) per month, jobs per month)

    # the province-wide employers and their accounts
    emp = {}
    for hq, sector, legal, accts, weight in W.BRANCH_EMPLOYERS:
        bn = reg.bn()
        reg.names.add(legal)
        emp[legal] = dict(hq=hq, sector=sector, bn=bn, weight=weight,
                          accounts=[Account(bn, ref, legal, op) for ref, op in accts])
    # a second account's legal name as recorded before the employer's rename
    OLD_NAMES = {"Northline Health Authority": "Northern Regional Health Authority",
                 "Coastal Community Health Services": "Saltmere and District Health Services",
                 "Provincial Services Agency": "Provincial Government Services Branch"}
    for legal, old in OLD_NAMES.items():
        emp[legal]["accounts"][1].legal = old

    # school divisions: teachers on RP0001, support staff on RP0002, both listing every school
    divisions = {}
    for code, name, *_ in W.REGIONS:
        bn = reg.bn()
        legal = "%s School Division" % name
        reg.names.add(legal)
        old = "%s School District No. %d" % (name, 3 + W.RCODE.index(code) * 2)
        a1 = Account(bn, "0001", legal, legal)
        a2 = Account(bn, "0002", old if code in ("E03", "E05", "E08", "E09") else legal, legal + " - Support Staff")
        divisions[code] = dict(bn=bn, accounts=[a1, a2])

    towns = {}

    def municipal_government(mc):
        if mc not in towns:
            bn = reg.bn()
            nm = W.MUNI_NAME[mc]
            kind = "City of" if mc in ("0101", "0301") else ("Rural Municipality of" if W.MUNI_NAME[mc] in RURAL else "Town of")
            legal = "%s %s" % (kind, nm)
            reg.names.add(legal)
            towns[mc] = dict(bn=bn, sector="91", municipal=True,
                             accounts=[Account(bn, "0001", legal, legal), Account(bn, "0002", legal, legal + " - Council and Fire")])
        return towns[mc]

    i26, i27 = S.MAR26, S.MAR27
    p26 = S.parts(R, Sh, own, br, i26)
    HEALTH = {e["bn"] for e in emp.values() if e["sector"] == "62"}

    def split_lines(e_or_div, size, share=0.62):
        """a workplace's jobs on its employer's accounts: one account, or the first and second (salaried and hourly,
        teachers and support staff) when the employer pays from both"""
        a = e_or_div["accounts"]
        if len(a) > 1 and (e_or_div.get("sector") in ("62",) or "School Division" in a[0].legal):
            # most sites pay on both accounts; a few have no staff on the second
            if g.random() < (0.84 if e_or_div.get("sector") == "62" else 0.93):
                t = max(1, int(round(size * share)))
                return [(a[0], t), (a[1], size - t)] if size - t > 0 else [(a[0], t)]
            return [(a[0], size)]
        if len(a) > 1 and e_or_div.get("sector") == "44-45":
            return [(a[0] if g.random() < 0.7 else a[1], size)]
        if len(a) > 1 and e_or_div.get("municipal"):
            t = max(1, int(round(size * share)))
            return [(a[0], t), (a[1], size - t)] if size - t > 0 else [(a[0], t)]
        if len(a) > 1 and e_or_div.get("sector") == "91":
            t = max(1, int(round(size * 0.85)))
            return [(a[0], t), (a[1], size - t)] if (size - t > 0 and g.random() < 0.5) else [(a[0], size)]
        return [(a[0], size)]

    # ------------------------------------------------------------------ March 2026
    for code, d in R.items():
        keys = [(mc, s) for (r, mc, s, kind) in p26 if r == code]
        keys = list(collections.OrderedDict.fromkeys(keys))
        for (mc, s) in keys:
            total = cells26.get((mc, s), 0)
            if total <= 0:
                continue
            bparts = []
            for (r, m2, s2, kind), v in p26.items():
                if r == code and m2 == mc and s2 == s and kind != "own":
                    _, origin, hq = kind
                    es = [e for e in emp.values() if e["hq"] == hq and e["sector"] == s]
                    wsum = sum(e["weight"] for e in es)
                    for e in es:
                        bparts.append((e, v * e["weight"] / wsum))
            ownv = sum(v for (r, m2, s2, kind), v in p26.items() if r == code and m2 == mc and s2 == s and kind == "own")
            ints = S._largest_remainder([v for _, v in bparts] + [ownv], total)
            for (e, _), n in zip(bparts, ints[:-1]):
                for size in _split(int(n), *BRANCH_SIZE[s], g):
                    wp.append(dict(muni=mc, sector=s, address=reg.address(mc), kind="branch", emp=e["bn"], owner=e,
                                   l26=split_lines(e, size), region=code))
            n_own = int(ints[-1])
            if s == "61" and n_own > 0:
                school = int(round(n_own * 0.72))
                n_own -= school
                for size in _split(school, 45, 0.5, g):
                    dv = divisions[code]
                    wp.append(dict(muni=mc, sector=s, address=reg.address(mc), kind="school", emp=dv["bn"], owner=dv,
                                   l26=split_lines(dv, size, 0.68), region=code))
            if code in ("E01", "E02") and n_own > 0:
                es = [e for e in emp.values() if e["hq"] == code and e["sector"] == s]
                if es:
                    home = int(round(n_own * 0.35))
                    n_own -= home
                    wsum = sum(e["weight"] for e in es)
                    hs = S._largest_remainder([e["weight"] / wsum for e in es], home)
                    for e, n in zip(es, hs):
                        for size in _split(int(n), *BRANCH_SIZE[s], g):
                            wp.append(dict(muni=mc, sector=s, address=reg.address(mc, suite=True), kind="home",
                                           emp=e["bn"], owner=e, l26=split_lines(e, size), region=code))
            if s == "91" and n_own > 0:
                town = int(round(n_own * 0.8))
                n_own -= town
                mg = municipal_government(mc)
                for size in _split(town, 60, 0.4, g):
                    wp.append(dict(muni=mc, sector=s, address=reg.address(mc), kind="municipal", emp=mg["bn"],
                                   owner=mg, l26=split_lines(mg, size, 0.9), region=code))
            for size in _split(n_own, *SIZE[s], g):
                bn = reg.bn()
                legal, op = (reg.public_body(mc), None) if s == "91" else reg.business(s, W.MUNI_NAME[mc])
                trade = getattr(reg, "last_trade", None)
                accts = [Account(bn, "0001", legal, op or legal)]
                two = size >= 15 and s not in ("91",) and g.random() < 0.06
                if two:
                    second = legal
                    if g.random() < 0.4:
                        second = reg.former_name(s, trade)      # the legal name the business carried before a rename
                    accts.append(Account(bn, "0002", second, accts[0].operating + HOURLY[g.integers(len(HOURLY))]))
                own_e = dict(bn=bn, sector=s, accounts=accts)
                if two:
                    t = max(1, int(round(size * float(g.uniform(0.65, 0.85)))))
                    l = [(accts[0], t), (accts[1], size - t)]
                else:
                    l = [(accts[0], size)]
                wp.append(dict(muni=mc, sector=s, address=reg.address(mc, suite=mc in ("0101", "0301")), kind="local",
                               emp=bn, owner=own_e, l26=l, region=code))
    # seasonal workplaces closed in March (nil lines in both months)
    for code in ("E02", "E04", "E06", "E10", "E05"):
        ms = [mc for mc, *_ in W.MUNIS if W.MUNI_REGION[mc] == code and not (W.MUNIS[[m[0] for m in W.MUNIS].index(mc)][5])]
        for k in range(int(S.rng("nil", code).integers(14, 30))):
            mc = ms[k % len(ms)]
            s = ("72", "11", "71", "31-33")[k % 4]
            bn = reg.bn()
            legal, op = reg.business(s, W.MUNI_NAME[mc])
            own_e = dict(bn=bn, sector=s, accounts=[Account(bn, "0001", legal, op)])
            wp.append(dict(muni=mc, sector=s, address=reg.address(mc), kind="seasonal", emp=bn, owner=own_e,
                           l26=[(own_e["accounts"][0], 0)], region=code))
    for w in wp:
        w["l26"] = [(a, n, a.workplace_no()) for a, n in w["l26"]]
        # one workplace number per account: the same number is kept for the account's later months
    return _march27(R, cells27, wp, emp, divisions, reg, g)


TRY = {}


def _march27(R, cells27, wp, emp, divisions, reg, g):
    """what became of each workplace by March 2027, the openings, and the cells' March 2027 totals met exactly"""
    trend = {}
    for code in R:
        tot26 = sum(n for w in wp if w["region"] == code for _, n, _ in w["l26"])
        tot27 = sum(v for (mc, s), v in cells27.items() if W.MUNI_REGION[mc] == code)
        trend[code] = tot27 / tot26
    devices = collections.defaultdict(list)
    for w in wp:
        code = w["region"]
        mu = np.log(trend[code])
        size = sum(n for _, n, _ in w["l26"])
        w["l27"] = None
        if w["kind"] == "seasonal":
            w["l27"] = [(a, 0, no) for a, n, no in w["l26"]]
            continue
        if w["kind"] == "local":
            closing = 0.06 if w["sector"] in ("72", "44-45", "81", "23") else 0.035
            if g.random() < closing:
                w["l27"] = [] if g.random() < 0.8 else [(a, 0, no) for a, n, no in w["l26"]]
                w["fate"] = "closed"
                continue
        f = float(np.exp(mu + g.normal(0, 0.10 if w["kind"] == "local" else 0.05)))
        w["l27"] = [(a, max(1, int(round(n * f * float(np.exp(g.normal(0, 0.025)))))) if n > 0 else 0, no)
                    for a, n, no in w["l26"]]
        w["fate"] = "continuing"
    # changes of hands: five local workplaces in each region go to a new owner's account, the workplace unchanged
    for code in R:
        cand = [w for w in wp if w["region"] == code and w["kind"] == "local" and w.get("fate") == "continuing"
                and len(w["l26"]) == 1 and 28 <= sum(n for _, n, _ in w["l26"]) <= 95]
        cand.sort(key=lambda w: (w["muni"], w["sector"], w["address"]))
        pick = [cand[k] for k in S.rng("transfer", code, TRY.get(code, 0)).choice(len(cand), size=5, replace=False)]
        for k, w in enumerate(pick):
            size = sum(n for _, n, _ in w["l26"])
            f = float(S.rng("tf", code, k).uniform(0.50, 0.78)) if k < 4 else float(S.rng("tf", code, k).uniform(1.06, 1.22))
            bn = reg.bn()
            legal, op = reg.business(w["sector"], W.MUNI_NAME[w["muni"]])
            new = Account(bn, "0001", legal, op)
            w["l27"] = [(new, max(1, int(round(size * f))), new.workplace_no())]
            w["fate"] = "changed hands"
            w["fixed"] = True
            devices[code].append(("transfer", w))
    # Larkmoor Express stores taken into the Larkmoor Foods account
    harrow = emp["Larkmoor Foods Ltd."]
    for code in R:
        ws = [w for w in wp if w["region"] == code and w["owner"] is harrow and w.get("fate") == "continuing"
              and w["l26"][0][0] is harrow["accounts"][1]]
        for w in ws[:2]:
            a1 = harrow["accounts"][0]
            n27 = w["l27"][0][1]
            w["l27"] = [(a1, n27, a1.workplace_no())]
            w["fate"] = "account changed"
            w["fixed"] = True
            devices[code].append(("account", w))
    # openings
    for code in R:
        cl = [k for k in cells27 if W.MUNI_REGION[k[0]] == code]
        for (mc, s) in cl:
            have = sum(n for w in wp if w["muni"] == mc and w["sector"] == s for _, n, _ in (w["l27"] or []))
            target = cells27[(mc, s)]
            room = max(0, int(round(target * float(g.uniform(0.02, 0.06)))))
            if target - have > room:
                room = target - have
            for size in _split(room, *SIZE[s], g) if room > 0 else []:
                bn = reg.bn()
                legal, op = reg.business(s, W.MUNI_NAME[mc])
                a = Account(bn, "0001", legal, op)
                wp.append(dict(muni=mc, sector=s, address=reg.address(mc, suite=mc in ("0101", "0301")), kind="local",
                               emp=bn, owner=dict(bn=bn, sector=s, accounts=[a]), l26=[], region=code,
                               l27=[(a, size, a.workplace_no())], fate="opened"))
    # meet each cell exactly: spread the difference over the workplaces that simply carried on
    for (mc, s), target in sorted(cells27.items()):
        ws = [w for w in wp if w["muni"] == mc and w["sector"] == s and w["l27"]]
        have = sum(n for w in ws for _, n, _ in w["l27"])
        diff = target - have
        adj = [(w, k) for w in ws if not w.get("fixed") and w.get("fate") in ("continuing", "opened")
               for k, (_, n, _) in enumerate(w["l27"]) if n > 0]
        guard = 0
        while diff != 0 and adj and guard < 50:
            guard += 1
            sizes = np.array([w["l27"][k][1] for w, k in adj], dtype=float)
            step = S._largest_remainder(sizes, abs(diff))
            for (w, k), dlt in zip(adj, step):
                a, n, no = w["l27"][k]
                nn = n + int(dlt) if diff > 0 else max(1, n - int(dlt))
                w["l27"][k] = (a, nn, no)
            have = sum(n for w in ws for _, n, _ in w["l27"])
            diff = target - have
        if diff != 0:
            raise RuntimeError("cell %s %s off by %d" % (mc, s, diff))
    return dict(wp=wp, emp=emp, divisions=divisions, registry=reg, devices=devices)


def lines(F):
    """the workplace lines of each month as the Agency's extract lists them"""
    out = {"2026-03": [], "2027-03": []}
    for w in F["wp"]:
        for month, key in (("2026-03", "l26"), ("2027-03", "l27")):
            for a, n, no in (w.get(key) or []):
                out[month].append(dict(reference_month=month, payroll_account=a.number, legal_name=a.legal,
                                       operating_name=a.operating, workplace_no=no, street_address=w["address"],
                                       municipality_code=w["muni"], naics_sector=w["sector"], payroll_jobs=int(n)))
    return out


# ------------------------------------------------------------------------------------------- the asks' figures
def lost(F, key):
    """by region: (jobs lost at workplaces with none in March 2027, jobs lost at workplaces with fewer), the workplace
    identified by key(line, workplace)"""
    j = collections.defaultdict(lambda: [0, 0])
    for w in F["wp"]:
        for col, lst in ((0, w.get("l26") or []), (1, w.get("l27") or [])):
            for a, n, no in lst:
                j[(w["region"], key(a, no, w))][col] += n
    out = {c: [0, 0] for c in W.RCODE}
    for (code, k), (a, b) in j.items():
        if b < a:
            out[code][0 if b == 0 else 1] += a - b
    return out


LOST_KEYS = {
    "workplace": lambda a, no, w: (w["muni"], w["address"]),
    "account_number": lambda a, no, w: (a.number, no),
    "business_address": lambda a, no, w: (a.bn, w["muni"], w["address"]),
    "legal_address": lambda a, no, w: (a.legal, w["muni"], w["address"]),
}


def separation(F):
    """each region's smallest gap between the golden figure and every other key's, on both figures"""
    g = lost(F, LOST_KEYS["workplace"])
    gap = {c: 10 ** 9 for c in W.RCODE}
    for k in ("account_number", "business_address", "legal_address"):
        o = lost(F, LOST_KEYS[k])
        for c in W.RCODE:
            gap[c] = min(gap[c], abs(o[c][0] - g[c][0]), abs(o[c][1] - g[c][1]))
    return gap, g


def _target(v, other, taken=()):
    """the nearest unrounded value to v whose tens are not round (a multiple of 50), not the row's other figure nor
    another region's figure in the column, and sit mid-bin (the units 8, 9, 0, 1 or 2)"""
    r10 = lambda x: int(round(x / 10.0)) * 10
    best = None
    for d in sorted(range(-22, 23), key=lambda d: (abs(d), d)):
        x = v + d
        if x % 10 in (8, 9, 0, 1, 2) and r10(x) % 50 != 0 and r10(x) != r10(other) and r10(x) not in taken and x > 0:
            best = x
            break
    return best


def polish(F, cells26, cells27):
    """bring each region's two golden figures to the middle of their tens, off round values and apart, moving jobs
    between workplaces of the same municipality and sector in one month so no cell changes (one pair or several)"""
    g = lost(F, LOST_KEYS["workplace"])
    taken = ({}, {})
    r10 = lambda x: int(round(x / 10.0)) * 10
    for code in W.RCODE:
        for fig in (0, 1):
            v = g[code][fig]
            rem = _target(v, g[code][1 - fig], set(taken[fig].values())) - v
            taken[fig][code] = r10(v + rem)
            if not rem:
                continue
            ws = [w for w in F["wp"] if w["region"] == code and not w.get("fixed") and w["kind"] == "local"
                  and len(w.get("l26") or []) <= 1 and len(w.get("l27") or []) <= 1]
            ws.sort(key=lambda w: (w["muni"], w["sector"], w["address"]))
            for w in ws:
                if not rem:
                    break
                if fig == 0 and not (w.get("fate") == "closed" and w.get("l26")):
                    continue
                if fig == 1 and not (w.get("fate") == "continuing" and w.get("l26") and w.get("l27")
                                     and 0 < w["l27"][0][1] < w["l26"][0][1]):
                    continue
                for o in ws:
                    if not rem:
                        break
                    if o is w or o["muni"] != w["muni"] or o["sector"] != w["sector"] or o.get("fate") != "continuing":
                        continue
                    a26, a27 = o["l26"][0][1], o["l27"][0][1]
                    if a27 <= a26:
                        continue                                    # o is a workplace that grew, and stays one
                    if fig == 0:
                        n26 = w["l26"][0][1]
                        cap = min(a26 - 1, rem) if rem > 0 else min(n26 - 1, a27 - a26 - 1, -rem)
                        if cap <= 0:
                            continue
                        k = cap if rem > 0 else -cap
                        w["l26"] = [(w["l26"][0][0], n26 + k, w["l26"][0][2])]
                        o["l26"] = [(o["l26"][0][0], a26 - k, o["l26"][0][2])]
                    else:
                        n26, n27 = w["l26"][0][1], w["l27"][0][1]
                        cap = min(n27 - 1, rem) if rem > 0 else min(n26 - n27 - 1, a27 - a26 - 1, -rem)
                        if cap <= 0:
                            continue
                        k = cap if rem > 0 else -cap
                        w["l27"] = [(w["l27"][0][0], n27 - k, w["l27"][0][2])]
                        o["l27"] = [(o["l27"][0][0], a27 + k, o["l27"][0][2])]
                    rem -= k
            if rem:
                raise RuntimeError("no pair to polish %s figure %d" % (code, fig))
            g = lost(F, LOST_KEYS["workplace"])
    return g
