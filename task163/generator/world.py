"""task163 world: Aubrine's catalogue at Uphall, the current pick faces and the 2027 re-slot plan, a year and more of
picking, the mis-picks, what the check-weigh caught and what reached customers, the claims, Corsley's invoices and the
returns bench. Everything here is truth; pack.py writes what the organisation's systems would hold."""
from __future__ import annotations

import datetime as dt
import math
from collections import defaultdict

import numpy as np

import common as K

P_MISPICK = 1 / 800.0          # a picked line takes the item from the next face instead
P_REPORT = 0.88                # an escaped mis-pick that the customer reports as a wrong item
P_SHORT = 1 / 2600.0           # a line picked short (item left out)
P_EXTRA = 1 / 3400.0           # one unit too many
GROWTH_2027 = {"Make-up": 1.08, "other": 1.05}   # the demand plan: make-up grows fastest

# ------------------------------------------------------------------------------------------------- catalogue
# family, kind, product, prefix, lines, variants (lo, hi), weight g (lo, hi), size steps g, cost GBP (lo, hi)
TEMPLATES = [
    ("Make-up", "shades", "Lipstick", "LS", 22, (8, 13), (19.0, 24.0), None, (3.10, 4.90)),
    ("Make-up", "shades", "Lip balm", "LB", 6, (4, 6), (9.0, 12.0), None, (1.60, 2.40)),
    ("Make-up", "shades", "Eyeliner", "EL", 8, (3, 6), (11.0, 17.0), None, (2.20, 3.40)),
    ("Make-up", "shades", "Foundation", "FD", 10, (10, 15), (44.0, 57.0), None, (5.40, 8.10)),
    ("Make-up", "single", "Palette", "PL", 18, (1, 1), (72.0, 158.0), None, (6.90, 12.40)),
    ("Make-up", "shades", "Nail colour", "NC", 8, (8, 11), (30.0, 36.0), None, (1.90, 2.80)),
    ("Fragrance", "sizes", "Eau de parfum", "EP", 16, (3, 3), (182.0, 199.0), (74.0, 158.0), (9.80, 16.50)),
    ("Fragrance", "shades", "Body mist", "BM", 5, (4, 6), (141.0, 158.0), None, (3.40, 4.60)),
    ("Fragrance", "single", "Gift set", "GS", 12, (1, 1), (305.0, 640.0), None, (14.20, 26.80)),
    ("Skincare", "sizes", "Moisturiser", "MO", 18, (2, 2), (96.0, 118.0), (58.0,), (6.20, 10.40)),
    ("Skincare", "single", "Serum", "SR", 24, (1, 1), (61.0, 92.0), None, (7.10, 12.90)),
    ("Skincare", "shades", "Cleanser", "CL", 6, (3, 3), (161.0, 189.0), None, (3.60, 5.20)),
    ("Haircare", "sizes", "Shampoo", "SH", 16, (2, 2), (281.0, 299.0), (268.0,), (2.90, 4.80)),
    ("Haircare", "single", "Hair oil", "HO", 10, (1, 1), (118.0, 142.0), None, (5.20, 8.60)),
    ("Bath and body", "shades", "Body wash", "BW", 10, (4, 6), (262.0, 289.0), None, (2.40, 3.60)),
    ("Bath and body", "sizes", "Body lotion", "BL", 12, (2, 2), (231.0, 249.0), (207.0,), (3.10, 5.40)),
    ("Bath and body", "shades", "Hand cream", "HC", 6, (4, 5), (74.0, 86.0), None, (2.10, 3.10)),
]
FAMILIES = ["Make-up", "Skincare", "Fragrance", "Haircare", "Bath and body"]
NAMES_A = ["Velvet", "Satin", "Silk", "Cashmere", "Dew", "Glow", "Bloom", "Halo", "Pure", "Calm", "Lumen", "Rain",
           "Ember", "Aura", "Sable", "Petal", "Tide", "Moss", "Frost", "Opal", "Coral", "Linen", "Fern", "Amber"]
NAMES_B = ["Matte", "Sheer", "Cream", "Luxe", "Daily", "Rich", "Soft", "Bright", "Deep", "Fresh", "Gentle", "Clear"]
SHADES = ["Rose", "Coral", "Berry", "Nude", "Plum", "Mocha", "Ruby", "Blush", "Spice", "Cherry", "Taupe", "Mauve",
          "Ivory", "Sand", "Honey", "Caramel", "Almond", "Chestnut", "Espresso", "Porcelain", "Linen", "Beige",
          "Peony", "Fig", "Cocoa", "Wine", "Copper", "Slate", "Jade", "Pearl"]
SCENTS = ["Fig and Cedar", "Orange Blossom", "Wild Mint", "Sea Salt", "Rose and Oud", "Vanilla", "Pear", "Lavender",
          "Bergamot", "Jasmine"]


def catalogue():
    g = K.rng("catalogue")
    skus = []
    used_codes = set()
    for fam, kind, product, prefix, nlines, (vlo, vhi), (wlo, whi), steps, (clo, chi) in TEMPLATES:
        for li in range(nlines):
            nvar = int(g.integers(vlo, vhi + 1))
            base_w = float(g.uniform(wlo, whi))
            base_c = float(g.uniform(clo, chi))
            name = "%s %s %s" % (NAMES_A[int(g.integers(0, len(NAMES_A)))], NAMES_B[int(g.integers(0, len(NAMES_B)))], product)
            line_vel = float(g.lognormal(5.0, 0.85))
            if kind == "shades":
                shares = 1.0 / np.arange(1, nvar + 1) ** 0.9
            elif kind == "sizes":
                shares = np.array([0.30, 0.48, 0.22][:nvar]) if nvar == 3 else np.array([0.62, 0.38])
            else:
                shares = np.array([1.0])
            shares = shares / shares.sum()
            order = g.permutation(nvar) if kind == "shades" else np.arange(nvar)
            pool = SCENTS if product in ("Body mist", "Body wash", "Hand cream", "Cleanser") else SHADES
            picks = g.choice(len(pool), size=nvar, replace=nvar > len(pool))
            for v in range(nvar):
                if kind == "sizes":
                    w = base_w + (steps[0] * v if len(steps) == 1 else (0.0 if v == 0 else steps[v - 1]))
                    cost = base_c * (1.0 + 0.62 * v)
                    vname = ["30 ml", "50 ml", "100 ml"][v] if nvar == 3 else (
                        ["50 ml", "100 ml"][v] if product == "Moisturiser" else
                        ["250 ml", "500 ml"][v] if product == "Shampoo" else ["200 ml", "400 ml"][v])
                elif kind == "shades":
                    w = base_w + float(g.uniform(-1.4, 1.4))
                    cost = base_c
                    vname = "%02d %s" % (v + 1, pool[int(picks[v])])
                else:
                    w = base_w
                    cost = base_c
                    vname = ""
                code = "AUB-%s%02d%02d" % (prefix, li + 1, v + 1)
                assert code not in used_codes
                used_codes.add(code)
                skus.append(dict(
                    sku=len(skus), family=fam, kind=kind, product=product, line=prefix + "%02d" % (li + 1),
                    aub=code, desc=(name + (" " + vname if vname else "")).strip(), w=round(w, 0),
                    cost=round(cost, 2), vel=line_vel * float(shares[int(order[v])])))
    # WMS item codes: six digits, unrelated to Aubrine's codes
    perm = K.rng("itemcodes").permutation(900000)[:len(skus)] + 100000
    for s, c in zip(skus, perm):
        s["item"] = int(c)
        s["size_class"] = "S" if s["w"] < 150 else "L"
    return skus


# ------------------------------------------------------------------------------------------------- faces
RUN_LEN = 30                     # a shelf level along one aisle: ten bays of three faces
ZONES = {"A": (1, 1), "B": (11, 3), "C": (14, 3), "D": (17, 3)}   # zone: (first aisle, aisles); four levels each


def runs_of(zone):
    a0, na = ZONES[zone]
    return [(zone, a0 + a, lev) for a in range(na) for lev in (1, 2, 3, 4)]


def fill(zone, seq):
    """Place items along the zone's runs in order: run by run, face by face; spare faces stay at the run ends of the
    zone's last runs."""
    faces = {}
    rl = runs_of(zone)
    cap = len(rl) * RUN_LEN
    assert len(seq) <= cap, (zone, len(seq), cap)
    # spread the spare faces over the zone's runs: each run is filled to the same depth, the rest left spare at its end
    per = int(math.ceil(len(seq) / len(rl)))
    k = 0
    for r in rl:
        for p in range(per):
            if k >= len(seq):
                break
            faces[seq[k]["sku"]] = (r, p)
            k += 1
    assert k == len(seq)
    return faces


def family_alternate(seq):
    """The carton-flow lanes take the fastest lines in velocity order, the slotting tool never putting two items of one
    family side by side where another family's item is next in line."""
    rest = list(seq)
    out = []
    while rest:
        k = 0
        if out:
            for i, s in enumerate(rest[:12]):
                if s["family"] != out[-1]["family"]:
                    k = i
                    break
        out.append(rest.pop(k))
    return out


def layouts(skus):
    by_vel = sorted(skus, key=lambda s: -s["vel"])
    nA = 4 * RUN_LEN - 8         # carton flow: one aisle of four levels, a few lanes spare
    A = by_vel[:nA]
    rest = by_vel[nA:]
    cur, plan = {}, {}
    A = family_alternate(A)
    fa = fill("A", A)
    cur.update(fa)
    plan.update(fa)
    # current: velocity bands, the slotting tool keeping a line's sizes side by side; shades are slotted one by one
    units = {}
    for s in rest:
        key = ("line", s["line"]) if s["kind"] == "sizes" else ("one", s["sku"])
        units.setdefault(key, []).append(s)
    ul = sorted(units.values(), key=lambda g: -max(x["vel"] for x in g))
    seq = [x for u in ul for x in sorted(u, key=lambda x: x["w"])]
    capz = {z: len(runs_of(z)) * RUN_LEN for z in "BCD"}
    nB = int(len(seq) * capz["B"] / (capz["B"] + capz["C"] + capz["D"]))
    nC = int(len(seq) * capz["C"] / (capz["B"] + capz["C"] + capz["D"]))
    cur.update(fill("B", seq[:nB]))
    cur.update(fill("C", seq[nB:nB + nC]))
    cur.update(fill("D", seq[nB + nC:]))
    # plan: the shelving by family, then line (best-selling line first), then each line's variants side by side
    lv = defaultdict(float)
    for s in rest:
        lv[s["line"]] += s["vel"]
    fam_rank = {f: i for i, f in enumerate(FAMILIES)}
    pseq = sorted(rest, key=lambda s: (fam_rank[s["family"]], -lv[s["line"]], s["line"],
                                       s["w"] if s["kind"] == "sizes" else -s["vel"]))
    plan.update(fill("B", pseq[:nB]))
    plan.update(fill("C", pseq[nB:nB + nC]))
    plan.update(fill("D", pseq[nB + nC:]))
    return cur, plan


def neighbours(faces):
    """Each item's left and right neighbours on its run (the faces either side that hold an item)."""
    at = {}
    for sku, (run, p) in faces.items():
        at[(run, p)] = sku
    nb = {}
    for sku, (run, p) in faces.items():
        nb[sku] = [at[(run, q)] for q in (p - 1, p + 1) if (run, q) in at]
    return nb


def separate_tolerance(skus, layouts_):
    """No neighbour pair, in either layout, weighs within 4 g of the tolerance: a pair is plainly inside it or plainly
    outside it, so neither the scale's resolution nor a carton's tare can carry a swap across."""
    by = {s["sku"]: s for s in skus}
    g = K.rng("separate")
    for _ in range(40):
        bad = 0
        for faces in layouts_:
            nb = neighbours(faces)
            for a, ns in nb.items():
                for b in ns:
                    d = abs(by[a]["w"] - by[b]["w"])
                    if K.TOL_G - 4 <= d <= K.TOL_G + 4:
                        bad += 1
                        x = by[a] if by[a]["kind"] != "shades" else by[b]
                        if x["kind"] == "shades":
                            # move a whole shade line together so its shades stay weight-alike
                            step = float(g.choice([-6.0, 6.0]))
                            for s in skus:
                                if s["line"] == x["line"]:
                                    s["w"] = max(8.0, s["w"] + step)
                        else:
                            x["w"] = max(8.0, x["w"] + float(g.choice([-6.0, 6.0])))
        if bad == 0:
            return
    raise AssertionError("tolerance band not cleared")


# ------------------------------------------------------------------------------------------------- picking
def season(d):
    m, wd = d.month, d.weekday()
    base = {1: 0.74, 2: 0.82, 3: 0.95, 4: 0.92, 5: 0.96, 6: 0.93, 7: 0.90, 8: 0.92, 9: 0.98, 10: 1.05, 11: 1.52,
            12: 1.46}[m]
    if dt.date(2025, 11, 24) <= d <= dt.date(2025, 12, 1):
        base *= 1.55            # Black Friday to Cyber Monday
    if dt.date(2025, 12, 19) <= d <= dt.date(2025, 12, 31):
        base *= 0.55
    dow = [1.18, 1.10, 1.04, 1.00, 0.98, 0.42, 0.28][wd]
    if d in K.UK_HOLIDAYS:
        return 0.0
    return base * dow


def picking(skus):
    """Order lines picked per item per day, 1 September 2025 to 25 October 2026, about 1.25 million in the baseline."""
    g = K.rng("picking")
    dd = K.days(K.EXPORT_FROM, K.EXPORT_TO)
    tot = sum(s["vel"] for s in skus)
    share = np.array([s["vel"] / tot for s in skus])
    daily = {}
    per_day_total = 31000.0
    lines = np.zeros((len(skus), len(dd)), dtype=np.int64)
    for j, d in enumerate(dd):
        lam = per_day_total * season(d) * float(g.uniform(0.93, 1.07))
        lines[:, j] = g.poisson(share * lam)
    units = lines + g.binomial(lines, 0.14)
    return dd, lines, units


def forecast_2027(skus, dd, lines):
    """The demand plan's 2027 order lines per item, as the slotting plan carries them."""
    g = K.rng("forecast")
    base = [i for i, d in enumerate(dd) if K.BASE_FROM <= d <= K.BASE_TO]
    out = {}
    for s in skus:
        b = float(lines[s["sku"], base].sum())
        grow = GROWTH_2027["Make-up"] if s["family"] == "Make-up" else GROWTH_2027["other"]
        out[s["sku"]] = int(round(b * grow * float(g.uniform(0.92, 1.08)) / 10.0) * 10)
    return out


# ------------------------------------------------------------------------------------------------- mis-picks
def mispicks(skus, cur, dd, lines):
    """Each picked line errs with one probability whatever sits beside it; the wrong item comes from the left or the
    right face with equal chance; the check-weigh holds the parcel when the swap moves it by more than the tolerance."""
    g = K.rng("mispicks")
    nb = neighbours(cur)
    by = {s["sku"]: s for s in skus}
    events = []
    for s in skus:
        i = s["sku"]
        ns = nb[i]
        n_err = g.binomial(lines[i], P_MISPICK)
        for j in np.nonzero(n_err)[0]:
            for _ in range(int(n_err[j])):
                wrong = ns[int(g.integers(0, len(ns)))]
                gap = abs(by[wrong]["w"] - s["w"])
                caught = gap > K.TOL_G
                reported = (not caught) and (g.random() < P_REPORT)
                events.append(dict(sku=i, wrong=wrong, day=dd[j], caught=caught, reported=reported, gap=gap,
                                   minute=int(g.integers(6 * 60, 22 * 60))))
    return events


def other_errors(skus, dd, lines):
    """Short and extra units: a short escapes the check-weigh only when the missing item weighs no more than the
    tolerance; an extra unit likewise."""
    g = K.rng("others")
    out = []
    for s in skus:
        i = s["sku"]
        for kind, p in (("SHORT", P_SHORT), ("EXTRA", P_EXTRA)):
            n = g.binomial(lines[i], p)
            for j in np.nonzero(n)[0]:
                for _ in range(int(n[j])):
                    out.append(dict(kind=kind, sku=i, day=dd[j], caught=s["w"] > K.TOL_G,
                                    reported=(s["w"] <= K.TOL_G) and kind == "SHORT" and g.random() < 0.9,
                                    minute=int(g.integers(6 * 60, 22 * 60))))
    return out


# ------------------------------------------------------------------------------------------------- the agency
RATES = {"Picker": (15.62, 16.31), "Team leader": (17.44, 18.20)}
RATE_CHANGE = dt.date(2026, 4, 6)
U_NIGHT, U_SUNDAY = 1.47, 2.36
SHIFTS = {"Early": (8.0, 0.0), "Late": (8.0, 0.5), "Night": (8.0, 8.0), "Sunday": (8.0, 0.0)}


def agency():
    """Corsley's workers on the Aubrine account: who worked which shift on which day, at what base rate."""
    g = K.rng("agency")
    dd = K.days(K.AGENCY_FROM, K.AGENCY_TO)
    workers = []
    for k in range(118):
        start = K.AGENCY_FROM + dt.timedelta(int(g.integers(-200, 400)))
        stay = int(g.integers(40, 420))
        workers.append(dict(no="C%05d" % (10412 + 13 * k + int(g.integers(0, 12))),
                            grade="Team leader" if k % 11 == 0 else "Picker",
                            start=max(start, K.AGENCY_FROM - dt.timedelta(30)), end=start + dt.timedelta(stay),
                            nights=bool(g.random() < 0.22)))
    seen = set()
    for w in workers:
        while w["no"] in seen:
            w["no"] = "C%05d" % (int(w["no"][1:]) + 1)
        seen.add(w["no"])
    lines = []
    for d in dd:
        if d in K.UK_HOLIDAYS:
            continue
        vol = season(d) / [1.18, 1.10, 1.04, 1.00, 0.98, 0.42, 0.28][d.weekday()]
        wd = d.weekday()
        if wd == 5:
            continue                                   # Saturdays are worked by Lathmor's own pickers
        need = {}
        if wd == 6:
            need["Sunday"] = int(round(9 * vol * float(g.uniform(0.85, 1.15))))
        else:
            need["Early"] = int(round(17 * vol * float(g.uniform(0.85, 1.15))))
            need["Late"] = int(round(15 * vol * float(g.uniform(0.85, 1.15))))
            need["Night"] = int(round(7 * vol * float(g.uniform(0.80, 1.20))))
        avail = [w for w in workers if w["start"] <= d <= w["end"]]
        order = [avail[i] for i in g.permutation(len(avail))]
        used = set()
        for shift in ("Night", "Sunday", "Early", "Late"):
            if shift not in need:
                continue
            pool = [w for w in order if w["no"] not in used and (w["nights"] == (shift == "Night"))]
            for w in pool[:need[shift]]:
                used.add(w["no"])
                hrs, nh = SHIFTS[shift]
                if g.random() < 0.06:
                    hrs = float(g.choice([4.0, 6.0, 6.5]))
                    nh = min(nh, hrs) if shift == "Night" else (0.0 if shift != "Late" or hrs < 8.0 else 0.5)
                rate = RATES[w["grade"]][1 if d >= RATE_CHANGE else 0]
                lines.append(dict(worker=w["no"], grade=w["grade"], date=d, shift=shift, hours=hrs, night=nh,
                                  sunday=hrs if shift == "Sunday" else 0.0, rate=rate))
    return lines


def pay_periods():
    out, k = [], 0
    while True:
        a = K.PAY_P0 + dt.timedelta(28 * k)
        b = a + dt.timedelta(27)
        if b > K.AGENCY_TO:
            break
        out.append((a, b))
        k += 1
    return out


# ------------------------------------------------------------------------------------------------- returns
FATES = {"Make-up": (0.58, 0.21, 0.21), "Skincare": (0.55, 0.16, 0.29), "Fragrance": (0.50, 0.27, 0.23),
         "Haircare": (0.52, 0.28, 0.20), "Bath and body": (0.57, 0.18, 0.25)}
REPACK_PRICE = {"S": 0.84, "L": 1.31}


def returns(skus):
    """Units graded at the returns bench: their fate, and the code each era's sheet or handheld gave it."""
    g = K.rng("returns")
    dd = K.days(K.RET_FROM, K.RET_TO)
    tot = sum(s["vel"] for s in skus)
    p = np.array([s["vel"] for s in skus]) / tot
    out = []
    for d in dd:
        if d.weekday() == 6 or d in K.UK_HOLIDAYS:
            continue
        lam = 172.0 * (1.35 if d.month in (1, 12) else 1.0) * (0.55 if d.weekday() == 5 else 1.0)
        n = int(g.poisson(lam))
        idx = g.choice(len(skus), size=n, p=p)
        for i in idx:
            s = skus[int(i)]
            r = g.random()
            f = FATES[s["family"]]
            fate = "resell" if r < f[0] else ("repack" if r < f[0] + f[1] else "scrap")
            if d < K.APP_LIVE:
                code = {"resell": 1, "repack": 2, "scrap": 3}[fate]
            else:
                code = {"resell": 1, "scrap": 2, "repack": 3}[fate]
            out.append(dict(sku=s["sku"], day=d, fate=fate, code=code, minute=int(g.integers(7 * 60 + 30, 17 * 60)),
                            station="R%d" % int(g.integers(1, 4))))
    return out


def build():
    skus = catalogue()
    cur, plan = layouts(skus)
    separate_tolerance(skus, [cur, plan])
    dd, lines, units = picking(skus)
    fc = forecast_2027(skus, dd, lines)
    ev = mispicks(skus, cur, dd, lines)
    oth = other_errors(skus, dd, lines)
    ag = agency()
    rt = returns(skus)
    return dict(skus=skus, cur=cur, plan=plan, dd=dd, lines=lines, units=units, fc=fc, events=ev, others=oth,
                agency=ag, periods=pay_periods(), returns=rt)
