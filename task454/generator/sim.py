"""The simulation: the drug catalog (products, NDCs, labelers, packages), each NDC's acquisition cost by month, the
survey's AAC rates for the NDCs it priced, the WAC, the pharmacies and members, the claims of the window and the
administrator's FY2026 utilization summary. One RNG stream per purpose, keyed by name."""
import datetime as dt
import hashlib

import numpy as np

import world as W


def rng(*keys):
    h = hashlib.sha256(("%d|" % W.SEED + "|".join(map(str, keys))).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def months(start, end):
    out, y, m = [], start.year, start.month
    while (y, m) <= (end.year, end.month):
        out.append(dt.date(y, m, 1))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


WMONTHS = months(*W.WINDOW)
PMONTHS = months(*W.PRIOR)
LAB = {code: (name, kind, cfg) for name, code, kind, cfg in W.LABELERS}
BY_KIND = {k: [c for _, c, kk, _ in W.LABELERS if kk == k] for k in "MUN"}


# ------------------------------------------------------------------ NDCs
def ndc_codes(labeler, product, package, cfg):
    """the ten-digit hyphenated code in the labeler's configuration and the eleven-digit 5-4-2 code"""
    if cfg == "442":
        p, k = "%04d" % (product % 10000), "%02d" % (package % 100)
        ten = "%s-%s-%s" % (labeler, p, k)
        eleven = "0" + labeler + p + k
    elif cfg == "532":
        p, k = "%03d" % (product % 1000), "%02d" % (package % 100)
        ten = "%s-%s-%s" % (labeler, p, k)
        eleven = labeler + "0" + p + k
    else:
        p, k = "%04d" % (product % 10000), "%d" % (package % 10)
        ten = "%s-%s-%s" % (labeler, p, k)
        eleven = labeler + p + "0" + k
    assert len(eleven) == 11 and len(ten.replace("-", "")) == 10
    return ten, eleven


class Product:
    def __init__(self, cls, name, strength, form, unit, base, kunits, ltc, newshare, drift, shortlisted=True):
        self.cls, self.name, self.strength, self.form, self.unit = cls, name, strength, form, unit
        self.base, self.kunits, self.ltc, self.newshare, self.drift = base, kunits, ltc, newshare, drift
        self.shortlisted = shortlisted
        self.key = (name, strength)
        self.old_cls = W.MOVES.get(self.key, (cls, cls))[0]
        g = rng("premium", name, strength)
        self.premium = W.UD_PREMIUM * float(np.exp(g.normal(0, 0.025)))
        self.ndcs = []
        self.gpc = None

    @property
    def liquid(self):
        return self.unit == "ML"

    def label(self):
        return "%s %s %s" % (self.name, self.strength, self.form)


def acquisition(n, month):
    """what a pharmacy paid its supplier per unit of NDC n in the month (the truth the survey estimates)"""
    p = n["product"]
    t = (month.year - 2026) * 12 + month.month - 4          # months from April 2026
    trend = 1.0 + p.drift * t / 12.0
    pkg = p.premium if n["pkg"] == "U" else 1.0
    return p.base * trend * pkg * n["labeler_factor"]


def catalog():
    """every product and NDC: the shortlisted classes', the products moved by the revision, and others"""
    prods = []
    for cls, items in W.SHORTLIST:
        for it in items:
            prods.append(Product(cls, *it))
    for cls, items in W.OTHERS:
        for name, strength, form, unit, base, kunits, ltc in items:
            prods.append(Product(cls, name, strength, form, unit, base, kunits, ltc, 0.02, -0.02, shortlisted=False))
    gpcs = set()
    for p in prods:
        g = rng("gpc", p.name, p.strength)
        while True:
            code = "%05d" % int(g.integers(10000, 99999))
            if code not in gpcs:
                gpcs.add(code)
                p.gpc = code
                break
    used, pnums, ndc_seen = {}, set(), set()
    for p in prods:
        g = rng("ndcs", p.name, p.strength)
        mans = list(g.choice(BY_KIND["M"], size=int(g.integers(3, 6)), replace=False))
        uds = list(g.choice(BY_KIND["U"], size=int(g.integers(2, 4)), replace=False))
        news = []
        if p.newshare >= 0.3:
            news = list(g.choice(BY_KIND["N"], size=3, replace=False))
        elif p.newshare > 0:
            news = list(g.choice(BY_KIND["N"], size=1, replace=False))

        def add(lab, pkg, size, desc_count, share):
            cfg = LAB[lab][2]
            if (lab, p.key) not in used:
                gp = rng("pnum", lab, *p.key)
                while True:
                    cand = int(gp.integers(1, 999))
                    if (lab, cand) not in pnums:
                        pnums.add((lab, cand))
                        used[(lab, p.key)] = cand
                        break
            pnum = used[(lab, p.key)]
            gk = rng("pk", lab, *p.key, pkg, size)
            while True:
                pk = int(gk.integers(1, 99 if cfg != "541" else 9))
                ten, eleven = ndc_codes(lab, pnum, pk, cfg)
                if eleven not in ndc_seen:
                    ndc_seen.add(eleven)
                    break
            p.ndcs.append(dict(product=p, labeler=lab, pkg=pkg, size=size, desc=desc_count, ndc10=ten, ndc11=eleven,
                               share=share, labeler_factor=float(np.exp(rng("lf", lab, *p.key).normal(0, 0.02)))))

        form = p.form.upper()
        for i, lab in enumerate(mans):
            if p.liquid:
                for size in ((473,) if i % 2 == 0 else (118, 473)):
                    add(lab, "B", size, "%d mL in 1 BOTTLE" % size, 1.0)
            else:
                sizes = (30, 90) if i % 3 == 0 else ((100, 500) if i % 3 == 1 else (100,))
                for size in sizes:
                    add(lab, "B", size, "%d %s in 1 BOTTLE" % (size, form), 1.0)
        for lab in uds:
            if p.liquid:
                add(lab, "U", 50, "10 CUP, UNIT-DOSE in 1 TRAY > 5 mL in 1 CUP", 1.0)
            else:
                add(lab, "U", 100, "10 BLISTER PACK in 1 CARTON > 10 %s in 1 BLISTER PACK" % form, 1.0)
        for lab in news:
            add(lab, "B", 100 if not p.liquid else 473,
                ("100 %s in 1 BOTTLE" % form) if not p.liquid else "473 mL in 1 BOTTLE", 1.0)
            p.ndcs[-1]["new"] = True
        # market shares within each package kind
        g2 = rng("shares", *p.key)
        for kind in ("B", "U"):
            xs = [n for n in p.ndcs if n["pkg"] == kind and not n.get("new")]
            w = g2.dirichlet(np.ones(len(xs)) * 2.0) if xs else []
            for n, s in zip(xs, w):
                n["share"] = float(s)
        xs = [n for n in p.ndcs if n.get("new")]
        w = g2.dirichlet(np.ones(len(xs)) * 3.0) if xs else []
        for n, s in zip(xs, w):
            n["share"] = float(s)
    return prods


def coverage(prods):
    """which NDCs the survey priced in which months: the retail bottles of established labelers nearly always, a new
    entrant's bottles from some months after launch, and about one carton NDC in four"""
    for p in prods:
        g = rng("coverage", *p.key)
        cartons = [n for n in p.ndcs if n["pkg"] == "U"]
        k = len(cartons)
        priced_cartons = set()
        for i, n in enumerate(cartons):
            if g.random() < 0.26:
                priced_cartons.add(n["ndc11"])
        # most products with cartons have one priced
        if not priced_cartons and g.random() < 0.62 and cartons:
            priced_cartons.add(cartons[int(g.integers(0, k))]["ndc11"])
        for n in p.ndcs:
            if n["pkg"] == "U":
                n["priced"] = {m: (n["ndc11"] in priced_cartons) for m in WMONTHS + PMONTHS}
            elif n.get("new"):
                launch = dt.date(2025, 9, 1) if p.newshare < 0.3 else WMONTHS[int(g.integers(0, 7))]
                n["launch"] = launch
                lag = int(g.integers(5, 9)) if p.newshare >= 0.3 else int(g.integers(3, 7))
                first = months(launch, dt.date(2028, 12, 1))[lag] if True else None
                n["priced"] = {m: (m >= first) for m in WMONTHS + PMONTHS}
            else:
                gap = g.random() < 0.04
                gm = set(g.choice(WMONTHS, size=2, replace=False)) if gap else set()
                n["priced"] = {m: (m not in gm) for m in WMONTHS + PMONTHS}
        # WAC per unit
        for n in p.ndcs:
            gw = rng("wac", n["ndc11"])
            a0 = acquisition(n, dt.date(2026, 4, 1))
            if n["pkg"] == "U":
                n["wac"] = a0 * float(gw.uniform(*W.W_UD))
            elif n.get("new"):
                n["wac"] = a0 * float(gw.uniform(*W.W_NEW))
            else:
                n["wac"] = a0 * float(gw.uniform(3.5, 7.0))
    return prods


def aac_rates(prods):
    """the survey's rates for the NDCs it priced: each month's invoice average per unit, published as a new rate only
    when it moves more than 2 per cent from the rate in effect; a rate stays in effect until replaced or until the
    NDC drops out of the month's survey"""
    rows = []
    for p in prods:
        for n in p.ndcs:
            g = rng("aac", n["ndc11"])
            cur = None
            for m in WMONTHS:
                est = acquisition(n, m) * float(np.exp(g.normal(0, 0.012)))
                if not n["priced"][m]:
                    if cur is not None:
                        rows.append(cur)
                        cur = None
                    continue
                if cur is not None and abs(est / cur["rate"] - 1) <= 0.02:
                    cur["end"] = month_end(m)
                    continue
                if cur is not None:
                    rows.append(cur)
                cur = dict(ndc11=n["ndc11"], rate=round(est, 5), unit=p.unit, effective=m, end=month_end(m), product=p,
                           ndc=n)
            if cur is not None:
                rows.append(cur)
    return rows


def month_end(m):
    nxt = dt.date(m.year + (m.month == 12), 1 if m.month == 12 else m.month + 1, 1)
    return nxt - dt.timedelta(days=1)


def rate_on(spans, day):
    for r in spans:
        if r["effective"] <= day <= r["end"]:
            return r["rate"]
    return None


def index_rates(rows):
    by = {}
    for r in rows:
        by.setdefault(r["ndc11"], []).append(r)
    return by


# ------------------------------------------------------------------ pharmacies and members
def npi(g):
    """a ten-digit NPI whose last digit checks the first nine with the 80840 prefix"""
    d = [int(x) for x in "1" + "".join(str(int(v)) for v in g.integers(0, 10, 8))]
    total = 24
    for i, x in enumerate(reversed(d)):
        y = x * 2 if i % 2 == 0 else x
        total += y // 10 + y % 10
    return "".join(map(str, d)) + str((10 - total % 10) % 10)


def pharmacies():
    g = rng("pharmacies")
    out = {"retail": [], "discount": [], "ltc": []}
    seen = set()
    for kind, k in (("retail", 330), ("discount", 48), ("ltc", 21)):
        while len(out[kind]) < k:
            x = npi(g)
            if x not in seen:
                seen.add(x)
                out[kind].append(x)
    return out


def members():
    g = rng("members")
    ids = set()
    while len(ids) < 52000:
        ids.add("%09d" % int(g.integers(100000000, 999999999)))
    ids = sorted(ids)
    return {"ltc": ids[:7400], "retail": ids[7400:]}


QTY_EA = ((30, 0.55), (60, 0.15), (90, 0.30))
QTY_ML = ((118, 0.25), (150, 0.2), (237, 0.25), (300, 0.15), (473, 0.15))
QTY_LTC_ML = ((150, 0.3), (240, 0.3), (300, 0.25), (450, 0.15))


def mean_qty(p, ltc):
    if p.liquid:
        tab = QTY_LTC_ML if ltc else QTY_ML
    else:
        return 30.4 if ltc else sum(q * w for q, w in QTY_EA)
    return sum(q * w for q, w in tab)


def claims(prods, rate_idx, scale):
    """the window's claims: each a fill of one NDC at one pharmacy for one member, priced the way the State prices
    it (the lesser of U&C and the AAC rate in effect on the fill date, or the WAC where none is), with reversals"""
    ph, mb = pharmacies(), members()
    out = []
    cid = [0]
    for p in prods:
        if not p.shortlisted:
            continue
        g = rng("claims", *p.key)
        units = p.kunits * 1000 * scale[p.cls]
        for ltc in (False, True):
            u = units * (p.ltc if ltc else 1 - p.ltc)
            n = int(round(u / mean_qty(p, ltc)))
            mo = g.integers(0, 12, n)
            day = g.random(n)
            pick = g.random(n)
            pick2 = g.random(n)
            for i in range(n):
                m = WMONTHS[int(mo[i])]
                fill = m + dt.timedelta(days=int(day[i] * (month_end(m).day)))
                if ltc and p.liquid:
                    qty = _draw(QTY_LTC_ML, pick2[i])
                elif ltc:
                    qty = 31 if pick2[i] < 0.42 else 30
                else:
                    qty = _draw(QTY_ML if p.liquid else QTY_EA, pick2[i])
                nd = _ndc(p, ltc, fill, pick[i], g)
                pool = ph["ltc"] if ltc else (ph["discount"] if g.random() < 0.12 else ph["retail"])
                pharm = pool[int(g.integers(0, len(pool)))]
                mem = mb["ltc" if ltc else "retail"][int(g.integers(0, len(mb["ltc" if ltc else "retail"])))]
                spans = rate_idx.get(nd["ndc11"], [])
                r = rate_on(spans, fill)
                basis = "AAC" if r is not None else "WAC"
                amount = round((r if r is not None else nd["wac"]) * qty, 2)
                if pool is ph["discount"] and p.base <= 0.15 and not p.liquid:
                    uc = 4.00 if qty <= 30 else (10.00 if qty <= 90 else 15.00)
                    if uc < amount:
                        amount, basis = uc, "UC"
                fee = W.FEE["ltc" if ltc else "retail"]
                lag = int(g.integers(1, 20)) if ltc else int(_draw(((0, .5), (1, .3), (2, .2)), g.random()))
                paid = min(fill + dt.timedelta(days=lag), W.PAID_THROUGH)
                cid[0] += 1
                row = dict(claim_id=cid[0], fill=fill, paid=paid, pharmacy=pharm, member=mem, ndc=nd, product=p,
                           qty=qty, ingredient=amount, fee=fee, basis=basis, ltc=ltc, txn="B1", original=None)
                out.append(row)
                if g.random() < 0.032:
                    rev = min(paid + dt.timedelta(days=int(g.integers(1, 25))), W.PAID_THROUGH)
                    cid[0] += 1
                    out.append(dict(row, claim_id=cid[0], paid=rev, qty=-qty, ingredient=-amount, fee=-fee,
                                    txn="B2", original=row["claim_id"]))
                    if g.random() < 0.4:
                        cid[0] += 1
                        out.append(dict(row, claim_id=cid[0], paid=min(rev + dt.timedelta(days=1), W.PAID_THROUGH)))
    return out


def _draw(tab, u):
    c = 0.0
    for v, w in tab:
        c += w
        if u < c:
            return v
    return tab[-1][0]


def _ndc(p, ltc, fill, u, g):
    m = dt.date(fill.year, fill.month, 1)
    if ltc and g.random() < 0.86:
        xs = [n for n in p.ndcs if n["pkg"] == "U"]
    else:
        xs = None
        news = [n for n in p.ndcs if n.get("new") and n.get("launch", dt.date(2000, 1, 1)) <= m]
        if news and not ltc and u < p.newshare:
            xs = news
            u = u / p.newshare
        elif not ltc and p.newshare > 0:
            u = (u - p.newshare) / (1 - p.newshare) if u >= p.newshare else u
        if xs is None:
            xs = [n for n in p.ndcs if n["pkg"] == "B" and not n.get("new")]
    w = np.array([n["share"] for n in xs], dtype=float)
    w = w / w.sum()
    k = int(np.searchsorted(np.cumsum(w), min(max(u, 0.0), 0.999999)))
    return xs[min(k, len(xs) - 1)]


# ------------------------------------------------------------------ the administrator's FY2026 summary
def prior_year(prods):
    """the FY2026 utilization summary: for each NDC and fill month from April 2025 to March 2026, the claims (net of
    reversals), units and ingredient cost paid, with the drug class the class list in force at the time gave the
    product (the list revised on 1 January 2027 moved some products between classes)"""
    out = []
    for p in prods:
        g = rng("prior", *p.key)
        growth = float(g.uniform(-0.08, 0.12))           # FY2027 against FY2026
        scale = W.SCALE.get(p.cls, W.OTHER_SCALE)
        units_y = p.kunits * 1000 * scale / (1 + growth)
        for ltc in (False, True):
            u = units_y * (p.ltc if ltc else 1 - p.ltc)
            mq = mean_qty(p, ltc)
            if ltc:
                kinds = [n for n in p.ndcs if n["pkg"] == "U"]
                kshare = 0.86
                rest = [n for n in p.ndcs if n["pkg"] == "B" and not n.get("new")]
            else:
                kinds = [n for n in p.ndcs if n["pkg"] == "B" and not n.get("new")]
                kshare = 1.0
                rest = []
            for m in PMONTHS:
                season = 1.0 + 0.04 * np.cos(2 * np.pi * (m.month - 1) / 12)
                um = u / 12 * season * float(np.exp(g.normal(0, 0.05)))
                for group, gs in ((kinds, kshare), (rest, 1 - kshare)):
                    if not group or gs <= 0:
                        continue
                    w = np.array([n["share"] for n in group], dtype=float)
                    w = w / w.sum()
                    for n, wi in zip(group, w):
                        units = um * gs * wi * float(np.exp(g.normal(0, 0.08)))
                        claims_n = int(round(units / mq))
                        if claims_n <= 0:
                            continue
                        units = round(claims_n * mq * float(np.exp(g.normal(0, 0.03))), 0 if not p.liquid else 1)
                        price = acquisition(n, m) * (float(np.exp(g.normal(0, 0.012))) if n["priced"][m]
                                                     else n["wac"] / acquisition(n, dt.date(2026, 4, 1)))
                        out.append(dict(month=m, ndc=n, product=p, label=p.old_cls, claims=claims_n, units=units,
                                        ingredient=round(price * units, 2)))
    return out
