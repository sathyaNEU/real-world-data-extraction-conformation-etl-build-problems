"""The Region Lindholt world (architecture 3): practices, statin products, patients with their own daily dose and
refill behaviour, every dispensing, the personal-number replacements, and the 2026 pharmacy pilot. Clean truth only;
pack.py writes the files."""
import datetime as dt
import math
import random

import params as P

# products on the market in the region: (atc, strength mg, pack size tablets, names by supplier)
PRODUCT_LINES = [
    ("C10AA05", 10, (30, 98)), ("C10AA05", 20, (30, 98, 100)), ("C10AA05", 40, (30, 98, 100)), ("C10AA05", 80, (30, 98)),
    ("C10AA07", 5, (30, 98)), ("C10AA07", 10, (30, 98, 100)), ("C10AA07", 20, (30, 98, 100)),
    ("C10AA01", 20, (30, 100)), ("C10AA01", 40, (30, 100)),
    ("C10AA03", 20, (30, 100)), ("C10AA03", 40, (30, 100)),
]
SUPPLIERS = ["Nordfarm", "Medivest", "Pharmalux", "Viropa"]
BRAND = {"C10AA05": "Lipator", "C10AA07": "Rosuvex", "C10AA01": "Simvacor", "C10AA03": "Pravalin"}

# dose patterns: (tablets a day, strength in units of the DDD)
PATTERNS = {"N": (1.0, 1.0), "H": (1.0, 2.0), "H4": (1.0, 4.0), "T": (2.0, 1.0), "S": (0.5, 2.0), "L": (1.0, 0.5)}


class Product:
    def __init__(self, number, name, atc, strength, pack):
        self.number, self.name, self.atc, self.strength, self.pack = number, name, atc, strength, pack


class Patient:
    pass


def build_products(rng):
    prods = []
    used = set()
    for atc, strength, packs in PRODUCT_LINES:
        for pack in packs:
            for k, sup in enumerate([None] + rng.sample(SUPPLIERS, 2)):
                while True:
                    num = "%06d" % rng.randrange(100000, 599999)
                    if num not in used:
                        used.add(num)
                        break
                if sup is None:
                    name = "%s %d mg" % (BRAND[atc], strength)
                else:
                    name = "%s \"%s\" %d mg" % (P.ATC_NAME[atc].capitalize(), sup, strength)
                prods.append(Product(num, name, atc, strength, pack))
    return prods


def strength_for(atc, units):
    return int(round(P.DDD_MG[atc] * units))


def pick_product(rng, prods, pattern):
    """A product line whose strength is the pattern's multiple of the DDD (simvastatin and pravastatin carry no 2x
    or half strengths in the region, so those patterns fall on atorvastatin and rosuvastatin)."""
    tpd, units = PATTERNS[pattern]
    if pattern == "N":
        atc = rng.choices(["C10AA05", "C10AA07", "C10AA01", "C10AA03"], [0.55, 0.25, 0.12, 0.08])[0]
        strength = {"C10AA05": 20, "C10AA07": 10, "C10AA01": 40, "C10AA03": 40}[atc]
    else:
        atc = rng.choices(["C10AA05", "C10AA07"], [0.65, 0.35])[0] if pattern != "H4" else "C10AA05"
        strength = strength_for(atc, units)
    cands = [p for p in prods if p.atc == atc and p.strength == strength]
    return tpd, atc, strength, cands


def pick(rng, weights):
    keys = sorted(weights)
    return rng.choices(keys, [weights[k] for k in keys])[0]


def dispense_run(rng, start, tpd, pack_choices, stop_after, end_date, late_share=0.12):
    """Dispensings from start at tpd tablets a day: each refill when the stock is nearly out (0 to 7 days early, or
    now and then 5 to 18 days late), until the day stop_after (days after start) or the extract's end. Returns
    (date, packs, pack size) tuples."""
    out = []
    day = start
    stock_end = start
    while day <= end_date:
        pack = rng.choice(pack_choices)
        packs = 1 if pack < 90 or tpd < 1.0 or rng.random() < 0.85 else 2
        out.append((day, packs, pack))
        last = max(stock_end, day)
        stock_end = last + dt.timedelta(days=packs * pack / tpd)
        if (day - start).days >= stop_after:
            break
        if rng.random() < late_share:
            nxt = stock_end + dt.timedelta(days=rng.randint(5, 18))
        else:
            nxt = stock_end - dt.timedelta(days=rng.randint(0, 7))
        if (nxt - start).days > stop_after:
            break
        day = max(nxt, day + dt.timedelta(days=7))
    return out


def build(seed=P.SEED):
    rng = random.Random(seed * 10 + 1)
    W = type("World", (), {})()
    W.products = build_products(rng)
    W.practices = P.PRACTICES
    ids = set()

    def pseudonym():
        while True:
            x = "%08X" % rng.randrange(0x10000000, 0xFFFFFFFF)
            if x not in ids:
                ids.add(x)
                return x
    patients = []
    for code, name, town, *mix, keep in P.PRACTICES:
        weights = dict(zip(["N", "H", "H4", "T", "S", "L"], mix))
        # the new users of the second half of 2025
        for _ in range(rng.randint(*P.COHORT_SIZE)):
            pt = Patient()
            pt.id = pseudonym()
            pt.practice = code
            pt.sex = rng.choice("MK")
            pt.born = dt.date(rng.randint(1938, 1982), rng.randint(1, 12), rng.randint(1, 28))
            pt.pattern = pick(rng, weights)
            pt.tpd, pt.atc, pt.strength, cands = pick_product(rng, W.products, pt.pattern)
            pt.cohort = True
            start = P.COHORT_START + dt.timedelta(days=rng.randrange(0, (P.COHORT_END - P.COHORT_START).days + 1))
            pt.start = start
            pt.persistent = rng.random() < keep
            fav = rng.choice(cands)
            pack_choices = [p.pack for p in cands if p.pack >= 90] or [fav.pack]
            if pt.persistent:
                runs = dispense_run(rng, start, pt.tpd, pack_choices, 10 ** 6, P.EXTRACT_END, late_share=0.10)
            else:
                # stops for good: the last tablets run out well before day 335 of the year under any rate estimate
                single = rng.random() < 0.38
                if single:
                    pack_choices = [p.pack for p in cands if p.pack <= 100 and p.pack >= 90] or [30]
                    if pt.pattern == "H4":
                        pt.pattern, pt.tpd, pt.atc, pt.strength = "H", 1.0, "C10AA05", 40
                        cands = [p for p in W.products if p.atc == "C10AA05" and p.strength == 40]
                        pack_choices = [98, 100]
                    runs = [(start, 1, rng.choice(pack_choices))]
                else:
                    horizon = rng.randint(80, 230)
                    runs = dispense_run(rng, start, pt.tpd, pack_choices, horizon, P.EXTRACT_END, late_share=0.0)
                    # make sure the last tablets are out by day 300
                    while runs:
                        stock = start
                        for d, k, pk in runs:
                            stock = max(stock, d) + dt.timedelta(days=k * pk / pt.tpd)
                        if (stock - start).days <= 300:
                            break
                        runs = runs[:-1]
                    if len(runs) < 2:
                        runs = [(start, 1, min(pack_choices))]
            pt.runs = runs
            pt.cands = cands
            patients.append(pt)
        # patients already on a statin (started before the cohort window), for the register's volume and the asks
        for _ in range(rng.randint(*P.PREVALENT_PER_PRACTICE)):
            pt = Patient()
            pt.id = pseudonym()
            pt.practice = code
            pt.sex = rng.choice("MK")
            pt.born = dt.date(rng.randint(1932, 1980), rng.randint(1, 12), rng.randint(1, 28))
            pt.pattern = pick(rng, weights)
            pt.tpd, pt.atc, pt.strength, cands = pick_product(rng, W.products, pt.pattern)
            pt.cohort = False
            pack_choices = [p.pack for p in cands if p.pack >= 90] or [cands[0].pack]
            first = P.EXTRACT_START + dt.timedelta(days=rng.randrange(0, 100))
            pt.start = first
            stop = 10 ** 6 if rng.random() < 0.86 else rng.randint(150, 800)
            pt.persistent = stop > 10 ** 5
            pt.runs = dispense_run(rng, first, pt.tpd, pack_choices, stop, P.EXTRACT_END, late_share=0.12)
            pt.cands = cands
            patients.append(pt)
    W.patients = patients
    backfill(W, seed)
    add_background(W, seed, ids)
    separate_birthdays(W, seed)
    return W


def backfill(W, seed):
    """The patients already on a statin when the main window opens carry their dispensings back to January 2024 (the
    old register system's months), drawn on their own stream."""
    rng = random.Random(seed * 10 + 6)
    for pt in W.patients:
        if pt.cohort:
            continue
        d0, k0, pk0 = pt.runs[0]
        days = k0 * pk0 / pt.tpd
        prev = []
        d = d0
        while True:
            d = d - dt.timedelta(days=int(round(days)) + rng.randint(-7, 2))
            if d < P.EXTRACT_FIRST:
                break
            prev.insert(0, (d, k0, pk0))
        pt.runs = prev + pt.runs


def add_background(W, seed, ids):
    """Patients who started a statin outside the cohort window (November 2024 to June 2025, and during 2026), drawn on
    their own stream so the cohort and the patients already on a statin never move."""
    rng = random.Random(seed * 10 + 2)

    def pseudonym():
        while True:
            x = "%08X" % rng.randrange(0x10000000, 0xFFFFFFFF)
            if x not in ids:
                ids.add(x)
                return x
    spans = [(dt.date(2024, 11, 1), dt.date(2025, 6, 30)), (dt.date(2026, 1, 2), dt.date(2026, 11, 30))]
    for code, name, town, *mix, keep in P.PRACTICES:
        weights = dict(zip(["N", "H", "H4", "T", "S", "L"], mix))
        for lo, hi in spans:
            for _ in range(rng.randint(*P.BACKGROUND_PER_SPAN)):
                pt = Patient()
                pt.id = pseudonym()
                pt.practice = code
                pt.sex = rng.choice("MK")
                pt.born = dt.date(rng.randint(1938, 1984), rng.randint(1, 12), rng.randint(1, 28))
                pt.pattern = pick(rng, weights)
                pt.tpd, pt.atc, pt.strength, cands = pick_product(rng, W.products, pt.pattern)
                pt.cohort = False
                pt.start = lo + dt.timedelta(days=rng.randrange(0, (hi - lo).days + 1))
                pt.persistent = rng.random() < keep
                pack_choices = [p.pack for p in cands if p.pack >= 90] or [cands[0].pack]
                stop = 10 ** 6 if pt.persistent else rng.randint(40, 260)
                pt.runs = dispense_run(rng, pt.start, pt.tpd, pack_choices, stop, P.EXTRACT_END, late_share=0.10)
                pt.cands = cands
                W.patients.append(pt)


def separate_birthdays(W, seed):
    """Two people sharing a birth date and sex whose dispensings never overlap would read as one person under two
    personal numbers; redraw the later one's birth date (birth dates move nothing on the call)."""
    rng = random.Random(seed * 10 + 3)

    def span(pt):
        return pt.runs[0][0], pt.runs[-1][0]
    while True:
        groups = {}
        for pt in W.patients:
            groups.setdefault((pt.born, pt.sex), []).append(pt)
        moved = 0
        for key, pts in sorted(groups.items()):
            if len(pts) < 2:
                continue
            pts = sorted(pts, key=lambda x: (span(x)[0], x.id))
            for i, a in enumerate(pts):
                for b in pts[i + 1:]:
                    if span(a)[1] < span(b)[0] or span(b)[1] < span(a)[0]:
                        b.born = dt.date(rng.randint(1938, 1984), rng.randint(1, 12), rng.randint(1, 28))
                        moved += 1
                        break
                if moved:
                    break
        if not moved:
            return


def truth_persistent(pt):
    """Each patient's persistence at the dose they take (the clean truth)."""
    stock_end = 0.0
    for d, packs, pack in pt.runs:
        x = (d - pt.start).days
        if x >= P.HORIZON_DAYS:
            break
        if x - stock_end > P.GRACE_DAYS:
            return False
        stock_end = max(stock_end, x) + packs * pack / pt.tpd
    return P.HORIZON_DAYS - stock_end <= P.GRACE_DAYS
