"""The Harrowmere world as it happened: the dwellings and their addresses, the ward boundary review, the true price
paths, every transfer 2015 to 2026 with its category and registration date, the building work done on each dwelling,
the developers' resales, the new homes, conversions and demolitions. Nothing here is read by solve.py."""
import datetime as dt
import hashlib
import math

import numpy as np

import params as P

D0 = dt.date(2015, 1, 1)


def rng(name):
    h = int(hashlib.sha256(("%d:%s" % (P.SEED, name)).encode()).hexdigest()[:16], 16)
    return np.random.default_rng(h)


def day(d):
    return (d - D0).days


def from_day(n):
    return D0 + dt.timedelta(days=int(n))


# ------------------------------------------------------------------------------------------------ the true index

def mean_levels():
    """log annual mean level of each ward, 2015 = 0"""
    out = {}
    for code, name, *_rest in P.WARDS:
        g = _rest[3]
        m = [0.0]
        for x in g:
            m.append(m[-1] + math.log1p(x / 100.0))
        out[name] = m
    return out


LEVELS = mean_levels()


def level(ward, d):
    """log level on a date: linear between mid-year points carrying each year's mean level"""
    m = LEVELS[ward]
    t = d.year + (d.timetuple().tm_yday - 0.5) / (366 if d.year % 4 == 0 else 365)
    x = t - 2015.5
    if x <= 0:
        return m[0] + x * (m[1] - m[0])
    i = int(math.floor(x))
    if i >= len(m) - 1:
        return m[-1] + (x - (len(m) - 1)) * (m[-1] - m[-2])
    f = x - i
    return m[i] * (1 - f) + m[i + 1] * f


# ------------------------------------------------------------------------------------------------ addresses

STREET_WORDS = ("Alder Ash Aspen Barley Beacon Beech Birch Bramble Brook Burdock Camden Cedar Chantry Chapel "
                "Cherry Clover Copper Coronation Cotton Cromwell Dale Dalton Elm Ferndale Field Flax Forge Foundry "
                "Garden Glebe Granby Grange Hawthorn Hazel Heather Holly Hope Ivy Juniper Kiln Laburnum Larch "
                "Laurel Lime Linden Locke Maple Market Meadow Mill Myrtle Nelson Newby Oak Orchard Osier Paddock "
                "Park Pear Pinfold Poplar Primrose Quarry Railway Raven Rectory Regent Rowan Rydal Saddler "
                "School Severn Shelley Sorrel Spencer Spring Station Stone Sycamore Tanner Teasel Thorn Tithe "
                "Trinity Union Vale Victoria Vine Walnut Warren Water Weaver Wellington Willow Windsor Wren "
                "Yew Albion Argyle Belmont Brunswick Clarence Derwent Eden Grafton Hanover Kendal Lonsdale "
                "Marlborough Melbourne Milton Newport Oxford Peel Portland Ripon Rutland Selby Stanley Sutton "
                "Talbot Tennyson Thornton Tudor Waverley Westbourne York Bede Hilda Aidan Cuthbert Oswald "
                "Keld Ure Swale Nidd Wharfe Calder Aire Don Rother Dearne Holme Colne Ryburn Hebble Spen Went "
                "Ewden Loxley Rivelin Porter Sheaf Moss Heron Kingfisher Lapwing Curlew Plover Merlin Kestrel "
                "Harrier Osprey Swallow Martin Linnet Finch Wagtail Bunting Thrush Dunnock Siskin Redwing "
                "Fieldfare Skylark Nightjar Corncrake Dotterel Whimbrel Godwit Knot Sanderling Turnstone").split()
SUFFIX = [("Road", 0.24), ("Street", 0.22), ("Avenue", 0.08), ("Grove", 0.07), ("Terrace", 0.08), ("Close", 0.06),
          ("Crescent", 0.05), ("Drive", 0.05), ("Lane", 0.06), ("Place", 0.03), ("Gardens", 0.03), ("Way", 0.03)]
HOUSE_NAMES = ("THE LINDENS|ROSE COTTAGE|THE GABLES|BRACKEN HOUSE|HILLCREST|THE ORCHARD|WILLOW HOUSE|"
               "FOXGLOVES|THE OLD SCHOOL|HAWTHORN LODGE|STONE COTTAGE|MEADOW VIEW|THE BARN|GLEBE HOUSE|"
               "HOLLY LODGE|THE STABLES|IVY HOUSE|BEECH HOUSE|WOODSIDE|FERN COTTAGE").split("|")
BLOCK_WORDS = "Alder Beck Cedar Dale Elm Fell Gill Holme Ing Keld Lund Mere Nab Rigg Scar Thwaite Wath".split()
UNIT_LETTERS = "ABDEFGHJLNPQRSTUWXYZ"


class World:
    pass


def _postcode_units(r, used, district, n):
    """n fresh postcodes in a district: 'HW4 3QT'"""
    out = []
    while len(out) < n:
        pc = "%s %d%s%s" % (district, int(r.integers(1, 10)), UNIT_LETTERS[int(r.integers(0, 20))],
                            UNIT_LETTERS[int(r.integers(0, 20))])
        if pc not in used:
            used.add(pc)
            out.append(pc)
    return out


def build_stock(W):
    """every dwelling standing in 2015 (and the new ones added later by new_homes): address, ward, type, value"""
    r = rng("stock")
    used_pc, used_street = set(), set()
    words = list(STREET_WORDS)
    r.shuffle(words)
    wi = 0
    dw = []          # list of dicts
    streets = []     # (ward, street name, [postcodes])
    for code, name, n, mix, lev, growth, whaz, district in P.WARDS:
        types = r.choice(np.array(["D", "S", "T", "F"]), size=n, p=np.array(mix) / sum(mix))
        houses = [t for t in types if t != "F"]
        n_flats = int(sum(1 for t in types if t == "F"))
        # houses along streets of 60 to 140 numbers; flats in blocks of 6 to 24
        k = 0
        order = list(houses)
        order.sort(key=lambda t: "TSD".index(t))     # terraces together, then semis, then detached
        while k < len(order):
            m = int(r.integers(60, 141))
            seg = order[k:k + m]
            k += m
            while True:
                w = words[wi % len(words)]
                wi += 1
                sfx = SUFFIX[int(r.choice(len(SUFFIX), p=np.array([s for _, s in SUFFIX]) / sum(s for _, s in SUFFIX)))][0]
                st = ("%s %s" % (w, sfx)).upper()
                if st not in used_street:
                    used_street.add(st)
                    break
            # postcodes of about 14 addresses along the street
            n_pc = max(1, int(round(len(seg) / 14.0)))
            pcs = _postcode_units(r, used_pc, district, n_pc)
            streets.append((name, st, pcs))
            for j, t in enumerate(seg):
                num = j + 1
                paon = str(num)
                if t == "D" and r.random() < 0.18:
                    paon = HOUSE_NAMES[int(r.integers(0, len(HOUSE_NAMES)))]
                dw.append(dict(ward=name, street=st, postcode=pcs[min(n_pc - 1, j * n_pc // len(seg))],
                               paon=paon, saon="", ptype=t, duration="F" if r.random() > 0.02 else "L",
                               built=None, value=lev + P.TYPE_PREMIUM[t] + float(r.normal(0, 0.11)),
                               locality=""))
        # flats in blocks, each block a building on one of the ward's streets with its own postcode
        ward_streets = [x for x in streets if x[0] == name]
        left = n_flats
        nb = 0
        while left > 0:
            m = int(min(left, r.integers(6, 25)))
            left -= m
            nb += 1
            _, st, _pcs = ward_streets[int(r.integers(0, len(ward_streets)))]
            pcs = _postcode_units(r, used_pc, district, 1)
            streets.append((name, st, pcs))
            if r.random() < 0.55:
                block = "%s %s" % (BLOCK_WORDS[int(r.integers(0, len(BLOCK_WORDS)))].upper(),
                                   ["COURT", "HOUSE", "LODGE", "MILL"][int(r.integers(0, 4))])
            else:
                block = str(int(r.integers(150, 400)))
            for j in range(m):
                dw.append(dict(ward=name, street=st, postcode=pcs[0], paon=block, saon="FLAT %d" % (j + 1),
                               ptype="F", duration="L", built=None,
                               value=lev + P.TYPE_PREMIUM["F"] + float(r.normal(0, 0.09)), locality=""))
    # repeated house names inside one postcode would make two dwellings one address: number them instead
    seen = set()
    for d in dw:
        key = (d["postcode"], d["paon"], d["saon"])
        if key in seen:
            d["paon"] = str(len(seen) % 97 + 101)
            key = (d["postcode"], d["paon"], d["saon"])
        seen.add(key)
    W.dw = dw
    W.streets = streets
    W.stock_pcs = sorted({pc for _w, _s, pcs in streets for pc in pcs})
    W.used_pc = used_pc
    W.used_street = used_street


NEIGHBOURS = [("Eastholme", "Moss Brow"), ("Abbots Hollow", "Calder Bank"), ("Dunmore", "Gorsey Hill"),
              ("Brindley Moor", "Wexley"), ("Fennick", "Pellbury"), ("Hollin Edge", "Kestrel Rise")]


def boundary_review(W):
    """May 2023: a few edge streets move between neighbouring wards; the 2019 ward of a postcode is kept beside its
    May 2023 ward. Dwellings carry their May 2023 ward; ward19 is the earlier one."""
    r = rng("boundary")
    moved = {}
    for a, b in NEIGHBOURS:
        cand = [s for s in W.streets if s[0] == b]
        r.shuffle(cand)
        for s in cand[:3]:
            for pc in s[2]:
                moved[pc] = a        # in 2019 this postcode was in ward a, from May 2023 in ward b
    W.moved = moved
    for d in W.dw:
        d["ward19"] = moved.get(d["postcode"], d["ward"])


def new_homes(W):
    """new dwellings: estates and blocks completed plot by plot (the building control completions), each first sold
    as a new build; a few conversions and a demolition. Returns the register's new-dwelling events."""
    r = rng("newhomes")
    events = []
    sites = [  # ward, site, dwellings per year {year: n}, type mix, edge (2019 ward differs), developer
        ("Moss Brow", "HERON FIELDS", {2019: 34, 2020: 41, 2021: 38, 2022: 44, 2023: 40, 2024: 37, 2025: 39, 2026: 58},
         (0.20, 0.50, 0.30, 0.0), "Eastholme"),
        ("Eastholme", "KINGFISHER PARK", {2016: 28, 2017: 46, 2018: 51, 2019: 40, 2020: 22}, (0.25, 0.45, 0.30, 0.0), None),
        ("Wexley", "LAPWING MEADOWS", {2024: 22, 2025: 47, 2026: 41}, (0.30, 0.50, 0.20, 0.0), None),
        ("Calder Bank", "WHARF STREET", {2021: 0, 2022: 64, 2023: 0, 2025: 48, 2026: 36}, (0, 0, 0, 1.0), None),
        ("Kestrel Rise", "CURLEW GATE", {2023: 18, 2024: 33, 2025: 29, 2026: 27}, (0.10, 0.40, 0.50, 0.0), None),
        ("Dunmore", "DOTTEREL CLOSE", {2017: 12, 2018: 16, 2026: 14}, (0.70, 0.30, 0.0, 0.0), None),
        ("Abbots Hollow", "OSPREY VIEW", {2020: 20, 2021: 26, 2026: 19}, (0.05, 0.35, 0.40, 0.20), None),
        ("Brindley Moor", "SISKIN WAY", {2022: 15, 2023: 21, 2026: 23}, (0.30, 0.50, 0.20, 0.0), None),
        ("Eastholme", "TEAL WALK", {2026: 11}, (0.10, 0.50, 0.40, 0.0), "Moss Brow"),
        ("Fennick", "TEASEL MEWS", {2026: 9}, (0.0, 0.30, 0.70, 0.0), None),
        ("Hollin Edge", "WAGTAIL RISE", {2026: 16}, (0.20, 0.50, 0.30, 0.0), "Kestrel Rise"),
        ("Gorsey Hill", "PLOVER FIELD", {2026: 12}, (0.50, 0.50, 0.0, 0.0), "Dunmore"),
        ("Pellbury", "MILL YARD", {2026: 8}, (0.0, 0.0, 1.0, 0.0), None),
    ]
    lev = {w[1]: w[4] for w in P.WARDS}
    for ward, site, per_year, mix, edge, in sites:
        wcode = [w for w in P.WARDS if w[1] == ward][0]
        district = wcode[7]
        plot = 0
        st_names = []
        for y in sorted(per_year):
            n = per_year[y]
            if n == 0:
                continue
            # each year's phase is a new street on the site with its own postcodes
            if mix[3] == 1:
                st = site
                W.used_street.add(st)
            else:
                while True:
                    w = STREET_WORDS[int(r.integers(0, len(STREET_WORDS)))]
                    sfx = ["CLOSE", "WAY", "DRIVE", "GROVE", "MEWS"][int(r.integers(0, 5))]
                    st = "%s %s" % (w.upper(), sfx)
                    if st not in W.used_street:
                        W.used_street.add(st)
                        break
            st_names.append(st)
            n_pc = max(1, int(round(n / 14.0)))
            pcs = _postcode_units(r, W.used_pc, district, n_pc)
            W.streets.append((ward, st, pcs))
            if edge:
                for pc in pcs:
                    W.moved[pc] = edge
            types = r.choice(np.array(["D", "S", "T", "F"]), size=n, p=np.array(mix) / sum(mix))
            app_no = int(r.integers(100, 900))
            block = str(int(r.integers(1, 40)))
            # completions spread through the year, one certificate per plot (houses) or one per block (flats)
            days = sorted(int(x) for x in r.integers(day(dt.date(y, 1, 8)), day(dt.date(y, 12, 18)), size=n))
            if mix[3] == 1:      # a block of flats is certified complete as one building
                days = [max(days)] * n
            for j in range(n):
                plot += 1
                t = str(types[j])
                built = from_day(days[j])
                if mix[3] == 1:
                    paon, saon = str(int(block) + 2 * (y - 2020)), "FLAT %d" % (j + 1)
                else:
                    paon, saon = str(2 * j + 1 + (0 if y % 2 else 2)), ""
                d = dict(ward=ward, street=st, postcode=pcs[min(n_pc - 1, j * n_pc // n)], paon=paon, saon=saon,
                         ptype=t, duration="L" if t == "F" else "F", built=built,
                         value=lev[ward] + P.TYPE_PREMIUM[t] + 0.05 + float(r.normal(0, 0.08)), locality="",
                         ward19=edge or ward, site=site, plot=plot)
                W.dw.append(d)
                events.append(dict(kind="new", ward=ward, ward19=edge or ward, site=site, year=y, date=built,
                                   dwelling=len(W.dw) - 1, app="%02d/%05d/FP" % (y % 100 - 1 if y > 2015 else 15, app_no),
                                   street=st, postcode=d["postcode"], paon=paon, saon=saon, created=1, lost=0,
                                   block=mix[3] == 1))
    W.new_events = events


def works_and_sales(W):
    """every dwelling's history 2015 to 2026: owner building work (each a register completion) and transfers, with
    the developers' wave (purchase, works, resale) in the wards in P.FLIPS"""
    r = rng("history")
    end = day(dt.date(2026, 12, 31))
    W.sales = []      # dict(dw, date, price, cat, kind, new)
    W.works = []      # dict(dw, date, wtype, added, flip, received)
    ward_haz = {w[1]: w[6] for w in P.WARDS}
    # choose the dwellings the developers buy: terraced houses with an ordinary history
    flip_set = {}
    for ward, n in P.FLIPS.items():
        idx = [i for i, d in enumerate(W.dw) if d["ward"] == ward and d["ptype"] == "T" and d["built"] is None
               and not d.get("converted")]
        pick = r.choice(len(idx), size=n, replace=False)
        for k in pick:
            i = idx[int(k)]
            buy = day(dt.date(2024, 2, 1)) + int(r.integers(0, 600))         # Feb 2024 to Sep 2025
            done = buy + int(r.integers(110, 270))
            sell = done + int(r.integers(25, 150))
            if from_day(sell).year < 2026 and r.random() < 0.75:
                sell = day(dt.date(2026, 1, 10)) + int(r.integers(0, 300))
            sell = min(sell, end - 5)
            if done >= sell:
                done = sell - int(r.integers(20, 60))
            flip_set[i] = (buy, done, sell, r.random() < P.FLIP_COMPANY,
                           float(r.uniform(*P.FLIP_ADDED)), r.random() < 0.55)
    W.flip_set = flip_set
    wt_names = [w[0] for w in P.WORK_TYPES]
    wt_p = np.array([w[2] for w in P.WORK_TYPES])
    wt_p = wt_p / wt_p.sum()
    for i, d in enumerate(W.dw):
        start = day(d["built"]) if d["built"] else 0
        stop = day(d["converted"]) if d.get("converted") else end
        h = P.SALE_HAZARD[d["ptype"]]
        quality = P.FLIP_TIRED if i in flip_set else 0.0
        fb = flip_set.get(i)
        # ordinary transfers: a Poisson stream; owner building work on houses: another
        sale_days, work_days = [], []
        t = float(start)
        while True:
            t += float(r.exponential(365.25 / h))
            if t >= stop:
                break
            sale_days.append(int(t))
        if d["ptype"] != "F":
            wh = ward_haz[d["ward"]] * (0.35 if d["built"] else 1.0)
            t = float(start) + (700 if d["built"] else 0)
            while True:
                t += float(r.exponential(365.25 / wh))
                if t >= stop:
                    break
                work_days.append(int(t))
        lead = [int(r.integers(40, 200)) for _ in work_days]
        # an owner who has just built an extension stays a while: thin the sales in the two years after; and nobody
        # sells while the builders are in, between the application and the certificate
        keep = []
        for sd in sale_days:
            if any(-ld - 10 <= sd - wd <= 10 for wd, ld in zip(work_days, lead)):
                continue
            if any(0 < sd - wd < 730 for wd in work_days) and r.random() < 0.45:
                continue
            keep.append(sd)
        sale_days = keep
        lead_of = dict(zip(work_days, lead))
        if d.get("converted") and d["converted"].year == 2026 and not sale_days:
            # a house split into flats in 2026 last changed hands as a house within the record
            sale_days = [day(dt.date(2016, 3, 1)) + int(r.integers(0, 3000))]
        if fb:
            buy, done, sell, company, added, two_storey = fb
            sale_days = [x for x in sale_days if not (buy - 90 <= x <= sell + 60)]
            work_days = [x for x in work_days if not (buy - 90 <= x <= sell + 60)]
        hist = [(x, "sale", None) for x in sale_days] + [(x, "work", None) for x in work_days]
        if fb:
            hist += [(buy, "flipbuy", company), (done, "flipwork", (added, two_storey)), (sell, "flipsell", None)]
        if d["built"]:
            hist.append((start + int(r.integers(5, 40)), "newsale", None))
        hist.sort(key=lambda e: e[0])
        prev_sale = -999
        drift, last_t = 0.0, float(start)
        for tday, kind, extra in hist:
            if tday > end:
                continue
            if kind == "sale" and tday - prev_sale < 120:
                continue
            if kind == "work":
                wt = wt_names[int(r.choice(len(wt_names), p=wt_p))]
                lo, hi = [w[1] for w in P.WORK_TYPES if w[0] == wt][0]
                add = float(r.uniform(lo, hi))
                quality += add
                W.works.append(dict(dw=i, date=from_day(tday), wtype=wt, added=add, flip=False,
                                    received=from_day(tday - lead_of.get(tday, 60))))
                continue
            if kind == "flipwork":
                add, two = extra
                quality += add
                W.works.append(dict(dw=i, date=from_day(tday), wtype="Loft conversion", added=add, flip=True,
                                    two_storey=two, received=from_day(max(buy + 5, tday - int(r.integers(60, 150))))))
                continue
            dd = from_day(tday)
            new = "Y" if kind == "newsale" and d.get("conversion_of") is None else "N"
            if kind == "newsale":
                cat = "A"
            elif kind == "flipbuy":
                cat = "B" if extra else "A"
            else:
                cat = "B" if r.random() < P.COMPANY_BY_WARD.get(d["ward"], P.COMPANY_SHARE) + P.REPO_SHARE else "A"
            disc = float(r.normal(-0.03, 0.03)) if kind == "flipbuy" else 0.0
            # each dwelling's own drift about its ward's path, a random walk in time
            drift += float(r.normal(0, P.DRIFT_SD * math.sqrt(max(0.0, tday - last_t) / 365.25)))
            last_t = float(tday)
            price = math.exp(d["value"] + level(d["ward"], dd) + quality + drift + disc
                             + float(r.normal(0, P.NOISE_SD)))
            W.sales.append(dict(dw=i, date=dd, price=price, cat=cat, kind=kind, new=new))
            prev_sale = tday


def conversions_and_demolitions(W):
    """houses split into flats (the house's address ends, new flat addresses begin), office blocks changed to flats,
    and one demolition; each a register completion with dwellings created and lost"""
    r = rng("convert")
    out = []
    for y in range(2015, 2027):
        n = int(r.integers(4, 9))
        cands = [i for i, d in enumerate(W.dw) if d["ptype"] in ("T", "S") and d["built"] is None]
        picks = [cands[int(k)] for k in r.choice(len(cands), size=n, replace=False)]
        if y == 2026:
            # every ward had a house or two split into flats in 2026
            picks = []
            for _c, wname, *_r in P.WARDS:
                wc = [i for i in cands if W.dw[i]["ward"] == wname]
                for k in r.choice(len(wc), size=1 + int(r.random() < 0.5), replace=False):
                    picks.append(wc[int(k)])
        for i in picks:
            d = W.dw[i]
            if d.get("converted"):
                continue
            when = dt.date(y, 1, 1) + dt.timedelta(days=int(r.integers(20, 340)))
            m = int(r.choice([2, 2, 3, 3, 4]))
            d["converted"] = when
            new_ids = []
            for j in range(m):
                nd = dict(ward=d["ward"], ward19=d["ward19"], street=d["street"], postcode=d["postcode"],
                          paon=d["paon"], saon="FLAT %s" % "ABCD"[j], ptype="F", duration="L", built=when,
                          value=d["value"] - 0.55 + float(r.normal(0, 0.06)), locality="", conversion_of=i)
                W.dw.append(nd)
                new_ids.append(len(W.dw) - 1)
            out.append(dict(kind="conversion", ward=d["ward"], ward19=d["ward19"], date=when, dwelling=i,
                            created=m, lost=1, street=d["street"], postcode=d["postcode"], paon=d["paon"], saon="",
                            new=new_ids))
    # office to residential and demolitions: each on a postcode of its own street
    def site_pc(ward, moved_from=None):
        pool = [(st, pc) for (w, st, pcs) in W.streets if w == ward for pc in pcs
                if (W.moved.get(pc) == moved_from if moved_from else pc not in W.moved) and pc in W.stock_pcs]
        return pool[int(r.integers(0, len(pool)))]
    for kind, ward, moved_from, when, created, lost, paon in [
            ("change_of_use", "Calder Bank", None, dt.date(2026, 6, 19), 32, 0, "EXCHANGE HOUSE"),
            ("change_of_use", "Calder Bank", "Abbots Hollow", dt.date(2026, 10, 2), 14, 0, "FOUNDRY CHAMBERS"),
            ("demolition", "Calder Bank", None, dt.date(2026, 2, 27), 0, 24, "TANNERY HOUSE"),
            ("demolition", "Fennick", None, dt.date(2025, 11, 14), 0, 6, "1-6 KILN YARD"),
            ("change_of_use", "Wexley", None, dt.date(2026, 3, 6), 3, 0, "THE OLD BANK"),
            ("change_of_use", "Eastholme", None, dt.date(2026, 5, 22), 2, 0, "HOLME CHAMBERS"),
            ("change_of_use", "Dunmore", None, dt.date(2026, 8, 14), 4, 0, "ST JUDE'S HALL"),
            ("change_of_use", "Hollin Edge", None, dt.date(2026, 11, 20), 2, 0, "HOLLIN WORKS"),
            ("change_of_use", "Kestrel Rise", None, dt.date(2026, 7, 3), 6, 0, "STATION HOUSE")]:
        st, pc = site_pc(ward, moved_from)
        out.append(dict(kind=kind, ward=ward, ward19=moved_from or ward, date=when, dwelling=None, created=created,
                        lost=lost, street=st, postcode=pc, paon=paon, saon=""))
    W.conv = out


def simulate():
    W = World()
    build_stock(W)
    boundary_review(W)
    new_homes(W)
    conversions_and_demolitions(W)
    works_and_sales(W)
    return W


if __name__ == "__main__":
    W = simulate()
    print("dwellings", len(W.dw), "sales", len(W.sales), "works", len(W.works), "flips", len(W.flip_set))
    from collections import Counter
    print(Counter(s["date"].year for s in W.sales))
    print(Counter(s["cat"] for s in W.sales))
