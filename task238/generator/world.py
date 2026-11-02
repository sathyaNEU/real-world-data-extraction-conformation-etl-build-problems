"""The clean truth of the task238 world: Saltmarsh Market's fourteen stores, their hourly scans, the fourteen Thursday
changeovers, every changeover label's print and hang time, the random audits, the Thursday changeover checks, the
Scanner Code claims and the flyer keying record. Nothing here reads target/; pack.py writes the files from it."""
import datetime as dt
from zoneinfo import ZoneInfo

import numpy as np

import params as P

TZ = ZoneInfo(P.TZ)
UTC = ZoneInfo("UTC")

DEPTS = ["GROCERY", "DAIRY", "FROZEN", "BAKERY", "MEAT", "DELI PACKAGED", "SNACKS", "BEVERAGES", "HOUSEHOLD",
         "HEALTH BEAUTY", "PET", "BABY"]
DEPT_W = np.array([0.24, 0.12, 0.09, 0.05, 0.07, 0.05, 0.10, 0.11, 0.07, 0.05, 0.03, 0.02])
BRANDS = ["Harvest Vale", "Northcove", "Ridgeway", "Maple Crest", "Bay Ridge", "Fundy Farms", "Clearwater",
          "Old Mill", "Brightfield", "Tidewell", "Sunnyhill", "Cobequid", "Lunenburg Kitchen", "Atlantic Pantry",
          "Driftwood", "Kingsport", "Seaside", "Valley Gold", "Peggy's Pick", "Highland Bake"]
NOUNS = {
    "GROCERY": ["Pasta", "Pasta Sauce", "Rice", "Cereal", "Peanut Butter", "Soup", "Canned Tomatoes", "Coffee",
                "Tea", "Flour", "Sugar", "Jam", "Crackers", "Oatmeal", "Salsa", "Olive Oil", "Ketchup", "Mustard"],
    "DAIRY": ["Yogurt", "Cheddar", "Butter", "Cream Cheese", "Milk 2%", "Sour Cream", "Mozzarella", "Eggs Large"],
    "FROZEN": ["Pizza", "Fries", "Ice Cream", "Mixed Vegetables", "Fish Fillets", "Waffles", "Perogies"],
    "BAKERY": ["Bagels", "Sliced Bread", "Muffins", "Tortillas", "Dinner Rolls"],
    "MEAT": ["Bacon", "Sausages", "Ground Beef", "Chicken Breasts", "Ham Sliced", "Pork Chops"],
    "DELI PACKAGED": ["Hummus", "Salami", "Turkey Breast", "Dip", "Coleslaw"],
    "SNACKS": ["Chips", "Cookies", "Granola Bars", "Popcorn", "Pretzels", "Chocolate Bar", "Nuts"],
    "BEVERAGES": ["Orange Juice", "Sparkling Water", "Cola", "Iced Tea", "Apple Juice", "Sports Drink"],
    "HOUSEHOLD": ["Paper Towels", "Bathroom Tissue", "Dish Soap", "Laundry Detergent", "Garbage Bags", "Foil"],
    "HEALTH BEAUTY": ["Shampoo", "Toothpaste", "Body Wash", "Deodorant", "Lotion"],
    "PET": ["Dog Food", "Cat Food", "Cat Litter", "Dog Treats"],
    "BABY": ["Diapers", "Baby Wipes", "Baby Food"],
}
SIZES = ["300 g", "400 g", "500 g", "650 g", "750 g", "900 g", "1 kg", "1.36 kg", "2 L", "1.89 L", "12 x 355 mL",
         "6 pk", "8 pk", "12 pk", "175 g", "250 g", "450 mL", "946 mL", "680 mL", "2.5 kg"]


def upc_check(d11):
    s = sum(int(c) * (3 if i % 2 == 0 else 1) for i, c in enumerate(d11))
    return str((10 - s % 10) % 10)


def days():
    d = P.Q_START
    while d <= P.Q_END:
        yield d
        d += dt.timedelta(days=1)


def hours_of(d):
    if d in P.CLOSED:
        return []
    if d.weekday() == 6:
        return list(range(P.SUN_OPEN, P.SUN_CLOSE))
    return list(range(P.OPEN_H, P.SHORT_CLOSE.get(d, P.CLOSE_H)))


def local(d, hour_float):
    base = dt.datetime(d.year, d.month, d.day, tzinfo=TZ)
    naive = dt.datetime(d.year, d.month, d.day) + dt.timedelta(hours=hour_float)
    return naive.replace(tzinfo=TZ)


class World:
    def __init__(self):
        self.r = np.random.default_rng(P.SEED)
        self.items()
        self.scans()
        self.changeovers()
        self.labels_and_hanging()
        self.thursday_scans()
        self.audits()
        self.checks()
        self.claims()
        self.flyer_keying()

    # ------------------------------------------------------------------ assortment
    def items(self):
        r = self.r
        varieties = ["Original", "Vanilla", "Strawberry", "Low Fat", "Garlic", "BBQ", "Sea Salt", "Unsalted",
                     "Spicy", "Honey", "Lemon", "Mint", "Whole Wheat", "Light", "Classic", "Extra Sharp", "Medium",
                     "Mild", "Peach", "Mixed Berry", "Dark Roast", "Decaf", "Chicken", "Beef", "Unscented"]
        seen = set()
        rows = []
        fam = []
        mfr = [str(x) for x in r.choice(np.arange(55000, 79000), size=180, replace=False)]
        fid = 0
        while len(rows) < 12600:
            dep = DEPTS[r.choice(len(DEPTS), p=DEPT_W / DEPT_W.sum())]
            m = mfr[r.integers(len(mfr))]
            brand = BRANDS[r.integers(len(BRANDS))]
            noun = NOUNS[dep][r.integers(len(NOUNS[dep]))]
            size = SIZES[r.integers(len(SIZES))]
            nv = int(r.choice([1, 2, 3, 4, 5], p=[0.46, 0.2, 0.16, 0.1, 0.08]))
            base = float(np.round(np.exp(r.normal(1.35, 0.55)), 2))
            price = max(0.99, round(np.floor(base) + [0.49, 0.79, 0.99, 0.29, 0.69][r.integers(5)], 2))
            vs = list(r.choice(varieties, size=nv, replace=False)) if nv > 1 else [""]
            fid += 1
            for v in vs:
                body = ("0" + m + "%05d" % r.integers(0, 100000))[:11]
                if body in seen:
                    continue
                seen.add(body)
                upc = body + upc_check(body)
                desc = " ".join(x for x in (brand, noun, v, size) if x)
                rows.append((upc, dep, desc, price, float(np.exp(r.normal(0, 1.1))), fid, "%s %s %s" % (brand, noun, size)))
        self.upc = np.array([x[0] for x in rows])
        self.dept = np.array([x[1] for x in rows])
        self.desc = np.array([x[2] for x in rows])
        self.reg = np.array([x[3] for x in rows])
        self.pop = np.array([x[4] for x in rows])
        self.fam = np.array([x[5] for x in rows])
        self.famname = {x[5]: x[6] for x in rows}
        n = len(rows)
        self.stocked = {}
        big = max(s[6] for s in P.STORES)
        for s in P.STORES:
            frac = 0.80 + 0.20 * (s[6] / big)
            keep = r.random(n) < np.clip(frac + 0.15 * np.tanh(np.log(self.pop)), 0.05, 1.0)
            self.stocked[s[0]] = keep

    # ------------------------------------------------------------------ hourly scans, every store, every day
    def profile(self, d, morning):
        hrs = hours_of(d)
        if not hrs:
            return hrs, np.array([])
        base = {8: 3.0, 9: 4.4, 10: 5.6, 11: 6.2, 12: 6.6, 13: 6.1, 14: 5.9, 15: 6.4, 16: 7.6, 17: 8.9, 18: 8.4,
                19: 6.6, 20: 4.6, 21: 2.9}
        w = np.array([base[h] for h in hrs])
        if d.weekday() == 3:   # Thursday, flyer day: a morning crowd at the stores whose shoppers chase the flyer
            bump = {8: 4.2, 9: 5.0, 10: 3.8, 11: 2.0, 12: 0.8}
            w = w + morning * np.array([bump.get(h, 0.0) for h in hrs])
        if d.weekday() == 6:
            w = w * np.array([1.2 if 11 <= h <= 15 else 0.9 for h in hrs])
        return hrs, w / w.sum()

    def scans(self):
        dow = [0.86, 0.84, 0.93, 1.12, 1.16, 1.27, 0.88]
        self.hourly = {}     # (store, date) -> (hours, counts)
        self.daytot = {}
        for s in P.STORES:
            no, size, morning = s[0], s[6], s[8]
            r = np.random.default_rng([P.SEED, no, 5])
            for d in days():
                hrs, prof = self.profile(d, morning)
                if not hrs:
                    continue
                season = 1.0 + 0.02 * ((d - P.Q_START).days / 30.0)
                if dt.date(2026, 12, 14) <= d <= dt.date(2026, 12, 24):
                    season += 0.22
                if d in P.SHORT_CLOSE:
                    season *= 0.85
                mean = size * dow[d.weekday()] * season * np.exp(r.normal(0, 0.05))
                counts = r.poisson(mean * prof)
                self.hourly[(no, d)] = (hrs, counts)
                self.daytot[(no, d)] = int(counts.sum())

    # ------------------------------------------------------------------ the weekly price change lists
    def changeovers(self):
        r = self.r
        n = len(self.upc)
        self.reg0 = self.reg.copy()
        regular = self.reg.copy()        # the standing regular price
        cur = self.reg.copy()            # the register price in force
        self.week_price = []             # register price of every item through flyer week k
        self.co = []
        prev_ad = np.array([], dtype=int)
        w = self.pop / self.pop.sum()
        for k, d in enumerate(P.CHANGEOVERS):
            big = d in P.HOLIDAY_WEEKS
            n_ad = int(r.integers(150, 185) if big else r.integers(96, 122))
            n_reg = int(r.integers(38, 70))
            prev = set(int(x) for x in prev_ad)
            fams = []
            got = 0
            famw = {}
            for i in range(n):
                famw[self.fam[i]] = famw.get(self.fam[i], 0.0) + w[i]
            fkeys = np.array(sorted(famw))
            fw = np.array([famw[f] for f in fkeys])
            for f in r.choice(fkeys, size=len(fkeys), replace=False, p=fw / fw.sum()):
                mem = [int(i) for i in np.where(self.fam == f)[0]]
                if any(i in prev for i in mem):
                    continue
                fams.append(mem)
                got += len(mem)
                if got >= n_ad:
                    break
            ad = np.array([i for mem in fams for i in mem])
            self.co_families = getattr(self, "co_families", []) + [fams]
            ended = prev_ad.copy()
            rest = np.setdiff1d(np.arange(n), np.concatenate([ad, ended]).astype(int))
            regs = r.choice(rest, size=n_reg, replace=False)
            items = np.concatenate([ad, ended, regs]).astype(int)
            kinds = np.array(["AD START"] * len(ad) + ["AD END"] * len(ended) + ["REG"] * len(regs))
            old = cur[items].copy()
            new = np.empty(len(items))
            famcut = {}
            for j, i in enumerate(items):
                if kinds[j] == "AD START":
                    cut = famcut.setdefault(self.fam[i], float(r.choice([0.15, 0.2, 0.25, 0.3, 0.33, 0.4])))
                    target = regular[i] * (1 - cut)
                    p = np.floor(target) + 0.99 - (1.0 if target - np.floor(target) < 0.99 else 0.0)
                    p = round(max(0.79, p if p > 0.5 else round(target, 2)), 2)
                    if p >= regular[i] - 0.20:
                        p = round(regular[i] - 0.50, 2)
                    new[j] = max(0.49, p)
                elif kinds[j] == "AD END":
                    new[j] = regular[i]
                else:
                    step = float(r.choice([-0.30, -0.20, 0.20, 0.30, 0.40, 0.50]))
                    regular[i] = round(max(0.99, regular[i] + step), 2)
                    new[j] = regular[i]
            cur[items] = new
            self.week_price.append(cur.copy())
            self.co.append({"date": d, "items": items, "kind": kinds, "old": old, "new": new, "big": big,
                            "ad_items": ad, "ad_price": new[:len(ad)].copy()})
            prev_ad = ad
        self.reg = regular

    # ------------------------------------------------------------------ print time and every label's hang time
    def labels_and_hanging(self):
        self.batch = {}     # (store, k) -> dict(print=datetime, labels=int, rate=float, hang=array per item)
        for s in P.STORES:
            no, crew, phour, sd, hol = s[0], s[5], s[9], s[10], s[11]
            r = np.random.default_rng([P.SEED, no, 7])
            for k, c in enumerate(self.co):
                d = c["date"]
                keep = self.stocked[no][c["items"]]
                idx = np.where(keep)[0]
                L = len(idx)
                if crew == "night":
                    hstart = 24.0 + phour + r.normal(0, sd)          # the Wednesday evening before
                    pt = local(d - dt.timedelta(days=1), max(22.08, min(hstart, 23.9)))
                    rate = P.NIGHT_RATE * np.exp(r.normal(0, 0.08))
                else:
                    h = phour + r.normal(0, sd) + (hol if c["big"] else 0.0)
                    close = P.SHORT_CLOSE.get(d, P.CLOSE_H)
                    h = min(max(h, 6.6), close - 3.2)
                    pt = local(d, h)
                    rate = P.HANG_RATE * np.exp(r.normal(0, P.HANG_RATE_SD / P.HANG_RATE))
                dur = L / rate                                      # minutes
                order = r.permutation(L)
                hang = np.empty(len(c["items"]))
                hang[:] = np.nan
                hang[idx[order]] = (np.arange(L) + r.random(L)) / L * dur   # minutes after print
                jam = r.random() < 0.09
                self.batch[(no, k)] = {"print": pt, "labels": L, "rate": rate, "dur": dur, "hang_min": hang,
                                       "jam": jam, "jam_lead": float(r.uniform(4, 13)) if jam else 0.0}

    # ------------------------------------------------------------------ changed items' Thursday scans
    def thursday_scans(self):
        self.thu = {}       # (store, k) -> dict(units per item, prior units per item, stale count, overcharge rows)
        self.truth_stale = {s[0]: 0 for s in P.STORES}
        self.overcharge_scans = []    # (store, datetime, item index, scanned price, shelf price)
        for s in P.STORES:
            no, share = s[0], s[7]
            for k, c in enumerate(self.co):
                r = np.random.default_rng([P.SEED, no, 11, k])
                d = c["date"]
                hrs, counts = self.hourly[(no, d)]
                big = 1.18 if c["big"] else 1.0
                U = int(round(share * big * counts.sum() * np.exp(r.normal(0, 0.04))))
                keep = self.stocked[no][c["items"]]
                w = self.pop[c["items"]] * keep * np.where(c["kind"] == "AD START", 2.6,
                                                           np.where(c["kind"] == "AD END", 0.9, 1.0))
                w = w / w.sum()
                units = r.multinomial(U, w)
                prior = r.multinomial(int(round(U * np.exp(r.normal(-0.12, 0.05)))), w)
                b = self.batch[(no, k)]
                # each scan's moment: the store's own hour mix that day, uniform within the hour
                hshare = counts / counts.sum()
                stale = 0
                item_of = np.repeat(np.arange(len(units)), units)
                hr_of = r.choice(len(hrs), size=len(item_of), p=hshare)
                frac = r.random(len(item_of))
                t_scan = np.array([local(d, hrs[h] + f) for h, f in zip(hr_of, frac)])
                pt = b["print"]
                mins = np.array([(ts - pt).total_seconds() / 60.0 for ts in t_scan])
                hang = b["hang_min"][item_of]
                is_stale = mins < hang
                stale = int(is_stale.sum())
                for j in np.where(is_stale)[0]:
                    i = c["items"][item_of[j]]
                    sc, sh = c["new"][item_of[j]], c["old"][item_of[j]]
                    if sc > sh:
                        self.overcharge_scans.append((no, t_scan[j], int(i), float(sc), float(sh)))
                self.truth_stale[no] += stale
                self.thu[(no, k)] = {"units": units, "prior": prior, "stale": stale, "U": U}

    # ------------------------------------------------------------------ the weekly random price audit
    def audits(self):
        self.audit_rows = []
        for s in P.STORES:
            no = s[0]
            r = np.random.default_rng([P.SEED, no, 13])
            for k, c in enumerate(self.co[:13]):
                d0 = c["date"]
                cands = [d0 + dt.timedelta(days=j) for j in range(7) if hours_of(d0 + dt.timedelta(days=j))]
                d = cands[r.integers(len(cands))]
                hrs = hours_of(d)
                start = r.uniform(hrs[0] + 0.25, hrs[-1] + 0.5)
                t0 = local(d, start)
                pool = np.where(self.stocked[no])[0]
                pick = r.choice(pool, size=P.AUDIT_LABELS, replace=False)
                pos = {int(i): j for j, i in enumerate(c["items"])}
                b = self.batch[(no, k)]
                for m, i in enumerate(pick):
                    t = t0 + dt.timedelta(seconds=int(m * r.uniform(14, 40)))
                    reg_price = self.price_at(int(i), k, t)
                    j = pos.get(int(i))
                    label = reg_price
                    if j is not None:
                        mins = (t - b["print"]).total_seconds() / 60.0
                        if mins < b["hang_min"][j]:
                            label = c["old"][j]
                    if label == reg_price and r.random() < P.BASE_ERR:
                        label = round(reg_price + r.choice([-0.50, -0.30, -0.20, 0.20, 0.40, 1.00]), 2)
                    self.audit_rows.append((no, t, int(i), float(label), float(reg_price)))

    def price_at(self, i, k, t):
        """the register price of item i at moment t inside flyer week k (changes take effect at 00:00 Thursday)"""
        return float(self.week_price[k][i])

    # ------------------------------------------------------------------ Thursday changeover checks
    def checks(self):
        self.check_rows = []
        for s in P.STORES:
            no = s[0]
            r = np.random.default_rng([P.SEED, no, 17])
            for k, c in enumerate(self.co):
                d = c["date"]
                close = P.SHORT_CLOSE.get(d, P.CLOSE_H)
                h = r.uniform(P.CHECK_FROM, min(P.CHECK_TO, close - 1.0))
                t0 = local(d, h)
                keep = np.where(self.stocked[no][c["items"]])[0]
                pick = r.choice(keep, size=P.CHECK_LABELS, replace=False)
                b = self.batch[(no, k)]
                for m, j in enumerate(pick):
                    t = t0 + dt.timedelta(seconds=int(m * r.uniform(25, 70)))
                    mins = (t - b["print"]).total_seconds() / 60.0
                    reg_price = float(c["new"][j])
                    label = float(c["old"][j]) if mins < b["hang_min"][j] else reg_price
                    if label == reg_price and r.random() < P.BASE_ERR:
                        label = round(reg_price + r.choice([-0.30, 0.20, 0.40]), 2)
                    self.check_rows.append((no, t, int(c["items"][j]), label, reg_price))

    # ------------------------------------------------------------------ Scanner Code claims (ask A)
    def claims(self):
        r = self.r
        self.claim_rows = []   # (store, moment, item, scanned, shelf, channel, register, txn, dup_logged)
        txn = {s[0]: 4000 + int(r.integers(0, 900)) for s in P.STORES}
        # overcharges from stray labels on any day, beside the changeover ones the scans produced
        extra = []
        for s in P.STORES:
            no = s[0]
            tot = sum(v for (st, d), v in self.daytot.items() if st == no)
            n_stray = int(r.poisson(tot * P.BASE_ERR * 0.5 * 0.022))
            keys = [d for (st, d) in self.daytot if st == no]
            for _ in range(n_stray):
                d = keys[r.integers(len(keys))]
                hrs = hours_of(d)
                t = local(d, r.uniform(hrs[0], hrs[-1] + 1))
                i = int(r.integers(len(self.upc)))
                sh = float(self.reg[i])
                sc = round(sh + float(r.choice([0.20, 0.30, 0.40, 0.50, 1.00])), 2)
                extra.append((no, t, i, sc, sh))
        pool = [x for x in self.overcharge_scans if r.random() < 0.030] + extra
        # a few claims made on the evening of 30 September, inside the UTC export window but outside the quarter
        for s in P.STORES[:9]:
            no = s[0]
            if r.random() < 0.8:
                t = local(dt.date(2026, 9, 30), r.uniform(20.1, 21.9))
                i = int(r.integers(len(self.upc)))
                sh = float(self.reg[i])
                pool.append((no, t, i, round(sh + 0.40, 2), sh))
        pool.sort(key=lambda x: (x[0], x[1]))
        zone = {s[0]: s[4] for s in P.STORES}
        for (no, t, i, sc, sh) in pool:
            at_till = r.random() < 0.66
            reg_no = int(r.integers(1, 9))
            txn[no] += int(r.integers(3, 40))
            if at_till:
                # Halifax stores: a supervisor approves the Code payout and logs it in the desk app as well.
                # Zone 2 stores: the cashier often takes the line back to the shelf price only, and the desk
                # pays the free item (or the 10.00) when the customer asks for the Code's remedy.
                if zone[no] == 1:
                    kind = "dup" if r.random() < 0.55 else "plain"
                else:
                    kind = "partial" if r.random() < 0.45 else "plain"
                later = t + dt.timedelta(minutes=float(r.uniform(2, 35)))
                self.claim_rows.append((no, t, i, sc, sh, "till", reg_no, txn[no], (kind, later)))
            else:
                later = t + dt.timedelta(hours=float(r.uniform(2, 70)))
                if later.date() in P.CLOSED or not hours_of(later.date()):
                    later = later + dt.timedelta(days=1)
                self.claim_rows.append((no, t, i, sc, sh, "desk", reg_no, txn[no], ("desk", later)))

    # ------------------------------------------------------------------ flyer keying (ask B)
    def flyer_keying(self):
        r = self.r
        self.ad_lines = []    # (k, line_no, [item indexes], qty, ad_price_for_qty, lead item)
        self.keyed = {}       # (k, item, zone, release) -> (qty, price_for_qty)
        self.ad_units = {}    # (k, item, zone) -> units in the flyer week
        for k, c in enumerate(self.co):
            fams = list(self.co_families[k])
            order = r.permutation(len(fams))
            for line, fi in enumerate(order, start=1):
                members = fams[fi]
                unit = float(np.max([c["ad_price"][int(np.where(c["ad_items"] == i)[0][0])] for i in members]))
                qty = int(r.choice([1, 2, 3], p=[0.72, 0.18, 0.10]))
                if qty == 2:
                    unit = max(1.00, round(np.floor(unit) + 0.50, 2))
                    price_q = round(unit * 2, 2)
                elif qty == 3:
                    price_q = float(max(3, int(np.round(unit * 3))))
                else:
                    price_q = unit
                lead = int(members[int(np.argmax(self.pop[members]))])
                self.ad_lines.append((k, line, [int(i) for i in members], qty, round(price_q, 2), lead))
                for i in members:
                    for zone in (1, 2):
                        good = (qty, round(price_q, 2))
                        prelim = good
                        u = r.random()
                        if u < 0.030:
                            prelim = (qty, round(price_q + float(r.choice([0.50, 1.00, 0.30])), 2))
                        elif u < 0.040 and qty > 1:
                            prelim = (1, round(price_q, 2))
                        revised = good if r.random() < 0.62 else prelim
                        if prelim == good and r.random() < 0.006:
                            revised = (qty, round(price_q + 0.20, 2))
                        self.keyed[(k, int(i), zone, "PRELIM")] = prelim
                        self.keyed[(k, int(i), zone, "REVISED")] = revised
                        zw = 0.6 if zone == 1 else 0.4
                        self.ad_units[(k, int(i), zone)] = int(r.poisson(self.pop[i] * 180 * zw) + 3)


def build_world():
    return World()
