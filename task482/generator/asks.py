"""The records behind the asks: each plant's 2026 stores issues of cleaning materials, the hauler's manifests and waste
profiles, the parts washer service tickets and the solvent vendors' payment lines (ask A, cleaning VOC away from the
presses); the two ink and coating suppliers' 2026 invoices and Haldane's renumbered catalog, and each plant's stock
counts (ask B, gallons received and unaccounted for). world.everything() calls build(e)."""
import datetime as dt

import numpy as np

import world as W

# cleaning: gal a year of HW-CS-210, HW-RC-240, HW-IK-260 issued away from the presses; press wash issued to the
# presses (gal); parts washers; share of the cleaning VOC shipped back out as spent solvent
CLEAN = {
    "ASH": (1400, 420, 760, 2, 900, 0.36), "BRI": (360, 90, 120, 1, 300, 0.315), "CAR": (1600, 980, 1100, 3, 1200, 0.42),
    "DUN": (320, 60, 90, 1, 200, 0.29), "ELS": (1150, 300, 640, 2, 700, 0.35), "GAR": (520, 180, 260, 1, 380, 0.33),
    "HAR": (600, 220, 330, 1, 420, 0.34), "IVE": (400, 150, 170, 1, 330, 0.30), "KEL": (1250, 140, 520, 2, 600, 0.38),
    "LAR": (820, 560, 480, 2, 560, 0.40), "MER": (1300, 380, 720, 2, 980, 0.37), "NOR": (460, 150, 240, 1, 330, 0.32),
    "PEL": (330, 50, 60, 1, 180, 0.27), "RAV": (2400, 1350, 1500, 3, 1700, 0.44),
}
STELLAR = ("ASH", "ELS", "HAR", "KEL", "MER", "RAV")      # parts washers moved to Ostrander from July
KG_PLANTS = ("CAR", "LAR")                   # the hauler's new manifest system from September
# unaccounted-for share of the inks, coatings and adhesives a plant used
LOSS = {"ASH": .031, "BRI": .024, "CAR": .036, "DUN": .022, "ELS": .028, "GAR": .026, "HAR": .029, "IVE": .025,
        "KEL": .033, "LAR": .034, "MER": .030, "NOR": .023, "PEL": .021, "RAV": .038}

# Haldane's catalog from 1 April 2026: item, product, pack (gal or lb), sold by, replaces (the item number it carried
# before 1 April, where it changed)
CATALOG = [
    ("2101", "HC-OPV-510", 5, "GAL", ""), ("2102", "HC-OPV-520", 5, "GAL", ""), ("2103", "HC-WOP-530", 5, "GAL", ""),
    ("2104", "HC-PRM-540", 5, "GAL", ""), ("2105", "HC-OPV-510", 55, "GAL", ""), ("2106", "HC-OPV-520", 55, "GAL", ""),
    ("2107", "HC-WOP-530", 55, "GAL", ""), ("2108", "HC-PRM-540", 55, "GAL", ""),
    ("2201", "HA-SB-610", 450, "LB", ""), ("2202", "HA-SB-620", 450, "LB", ""), ("2203", "HA-WB-650", 500, "LB", ""),
    ("2204", "HA-SL-680", 500, "LB", ""),
    ("2301", "HW-PW-710", 55, "GAL", "2102"), ("2302", "HW-PW-720", 55, "GAL", ""), ("2303", "HW-PW-710", 5, "GAL", ""),
    ("2304", "HW-PW-720", 5, "GAL", ""),
    ("2401", "HW-CS-210", 55, "GAL", "2101"), ("2402", "HW-RC-240", 55, "GAL", "2104"),
    ("2403", "HW-IK-260", 55, "GAL", "2103"), ("2404", "HW-CS-210", 5, "GAL", ""),
]
OLD_ITEM = {("HW-CS-210", 55): "2101", ("HW-PW-710", 55): "2102", ("HW-IK-260", 55): "2103",
            ("HW-RC-240", 55): "2104"}
PRICE = {"HC-OPV-510": 21.40, "HC-OPV-520": 24.85, "HC-WOP-530": 15.60, "HC-PRM-540": 19.95, "HA-SB-610": 3.62,
         "HA-SB-620": 3.98, "HA-WB-650": 2.71, "HA-SL-680": 4.46, "HW-PW-710": 12.30, "HW-PW-720": 13.75,
         "HW-CS-210": 11.90, "HW-RC-240": 16.20, "HW-IK-260": 10.45}
SHORT = {"HC-OPV-510": "OPV GLOSS 510", "HC-OPV-520": "HR LACQUER 520", "HC-WOP-530": "WB OPV 530",
         "HC-PRM-540": "FILM PRIMER 540", "HA-SB-610": "LAM ADH SB 610", "HA-SB-620": "LAM ADH SB HS 620",
         "HA-WB-650": "LAM ADH WB 650", "HA-SL-680": "LAM ADH SOLVENTLESS 680", "HW-PW-710": "AUTO PRESS WASH 710",
         "HW-PW-720": "PRESS WASH LV 720", "HW-CS-210": "EQUIP CLEANER 210", "HW-RC-240": "ANILOX/ROLL CLNR 240",
         "HW-IK-260": "INK KITCHEN WASH 260"}
INK_PRICE = {"SF": 18.70, "SG": 17.25, "WF": 14.10, "UV": 41.30}
ACCOUNT_A = {"ASH": "C-30417", "BRI": "C-30233", "CAR": "C-30288", "DUN": "C-30561", "ELS": "C-30302",
             "GAR": "C-30119", "HAR": "C-30476", "IVE": "C-30345", "LAR": "C-30390", "MER": "C-30258",
             "NOR": "C-30184", "PEL": "C-30602", "RAV": "C-30211", "KEL": "C-30674"}
ACCOUNT_B = {"ASH": "H-1213", "BRI": "H-1236", "CAR": "H-1327", "DUN": "H-1355", "ELS": "H-1388", "GAR": "H-1451",
             "HAR": "H-1476", "IVE": "H-1427", "KEL": "H-1142", "LAR": "H-1503", "MER": "H-1539", "NOR": "H-1562",
             "PEL": "H-1580", "RAV": "H-1604"}
THAMESIDE_B = "H-1117"


def _r(*k):
    return W.rng_for("asks", *k)


def kind(code):
    return W.PRODUCTS[code][2]


def ask_b_product(code):
    return kind(code) in ("INK", "COATING", "ADHESIVE")


def weekdays(rng, n, lo=W.FIRST_DAY, hi=W.LAST_DAY):
    out = []
    span = (hi - lo).days
    while len(out) < n:
        d = lo + dt.timedelta(days=int(rng.integers(0, span + 1)))
        if d.weekday() < 5 and d not in W.HOLIDAYS:
            out.append(d)
    return sorted(out)


# ---------------------------------------------------------------------------------------------------------------------
def cleaning(e):
    issues, manifests, profiles, tickets, payments = [], [], [], [], []
    truth = {}
    ino, mno, tno = 410000, 88000, 52000
    for p in W.PLANTS:
        c = p["code"]
        r = _r("clean", c)
        cs, rc, ik, nwash, pw, ship = CLEAN[c]
        fac = p["fac"]
        # stores issues
        issued_voc = 0.0
        plan = [("HW-CS-210", cs, ("PARTS CLEANING", "INK KITCHEN")), ("HW-RC-240", rc, ("ROLL CLEANING",)),
                ("HW-IK-260", ik, ("INK KITCHEN",))]
        pwcode = "HW-PW-710" if any(m[0] == "HW-PW-710" for mx in p["mix"].values() for m in mx) else "HW-PW-720"
        plan.append((pwcode, pw, tuple("PRESS " + x for x in p["presses"])))
        for code, total, places in plan:
            nis = max(6, int(total / 25))
            ds = weekdays(r, nis)
            w = r.dirichlet([3.0] * nis) * total
            for d, q in zip(ds, w):
                qty = max(5, int(round(q / 5.0)) * 5)
                ino += int(r.integers(1, 9))
                fac_d = p.get("old_fac") if (p.get("old_fac") and d < W.ACQUIRED) else fac
                issues.append(dict(fac=fac_d, no="SI-%d" % ino, date=d, material=code, qty=qty, uom="GAL",
                                   to=places[int(r.integers(0, len(places)))]))
                if not code.startswith("HW-PW"):
                    issued_voc += qty * W.voc_per_gal(code, d)
        # waste: the cleaning profile and the press waste profile
        pc = "CB-%s-01" % fac
        pp = "CB-%s-02" % fac
        voc_c = round(float(r.uniform(68, 81)), 1)
        voc_p = round(float(r.uniform(24, 36)), 1)
        profiles.append(dict(profile=pc, fac=fac, plant=p["name"], waste="Spent cleaning solvent and solvent-laden "
                             "rinse from ink kitchen, parts and roll cleaning", source="Cleaning", voc=voc_c,
                             code="D001 F003 F005", form="Liquid, drums"))
        profiles.append(dict(profile=pp, fac=fac, plant=p["name"], waste="Waste ink, coating and adhesive from press "
                             "make-ready and wash-up", source="Press operations", voc=voc_p, code="D001 F005",
                             form="Liquid and sludge, drums"))
        want = issued_voc * ship
        nman = int(r.integers(8, 14))
        ds = weekdays(r, nman)
        wc = r.dirichlet([4.0] * nman) * want / (voc_c / 100.0)
        credit = 0.0
        for d, lbs in zip(ds, wc):
            for prof, w_lb, vp in ((pc, lbs, voc_c), (pp, lbs * float(r.uniform(0.25, 0.6)), voc_p)):
                mno += int(r.integers(1, 40))
                drums = max(1, int(round(w_lb / 420.0)))
                kg = c in KG_PLANTS and d >= W.KG_FROM
                net = round(w_lb / 2.20462) if kg else round(w_lb)
                manifests.append(dict(no="%09dCBE" % (100000000 + mno), date=d, fac=fac if not (p.get("old_fac") and
                                      d < W.ACQUIRED) else p["old_fac"], profile=prof, containers=drums,
                                      ctype="DM", net=net, unit="KG" if kg else "LB"))
                if prof == pc:
                    credit += (net * 2.20462 if kg else net) * voc_c / 100.0
        # parts washers: Wexcombe every four weeks; Ostrander from July at six plants
        washer_voc = 0.0
        for wn in range(nwash):
            wid = "W%d" % (wn + 1)
            d = dt.date(2026, 1, 6) + dt.timedelta(days=int(r.integers(0, 20)))
            while d <= W.LAST_DAY:
                stell = c in STELLAR and d >= W.WASHER_SWITCH
                add = round(float(r.uniform(24, 36)), 1)
                spent = round(add * float(r.uniform(0.70, 0.84)), 1)
                prod = "OS-MS-7" if stell else "WX-MS-100"
                washer_voc += (add - spent) * W.voc_per_gal(prod, d)
                if stell:
                    payments.append(dict(fac=fac, vendor=W.WASHERS["SS"], inv="OSR-%05d" % (31000 + len(payments)),
                                         date=d + dt.timedelta(days=int(r.integers(2, 9))),
                                         amount=round(145 + 3.85 * add, 2), gl="6420 Solvent services",
                                         desc="Washer %s service %s: fresh %.1f gal OS-MS-7, spent %.1f gal recovered"
                                         % (wid, d.strftime("%m/%d/%y"), add, spent)))
                else:
                    tno += 1
                    fac_d = p.get("old_fac") if (p.get("old_fac") and d < W.ACQUIRED) else fac
                    tickets.append(dict(ticket="KL%06d" % tno, date=d, fac=fac_d, washer=wid, product=prod, added=add,
                                        removed=spent))
                d += dt.timedelta(days=28 + int(r.integers(-2, 3)))
        truth[c] = dict(issued=issued_voc, credit=credit, washers=washer_voc,
                        tons=(issued_voc - credit + washer_voc) / 2000.0)
    # the solvent vendors' other payment lines
    for p in W.PLANTS:
        r = _r("pay", p["code"])
        for m in range(1, 13):
            if p["code"] not in STELLAR or m < 7:
                payments.append(dict(fac=p["fac"], vendor=W.WASHERS["KL"], inv="WPW-%d-%02d" % (int(p["fac"]), m),
                                     date=dt.date(2026, m, 1) + dt.timedelta(days=int(r.integers(26, 30)) if m < 12
                                                                           else 20),
                                     amount=round(float(r.uniform(320, 980)), 2), gl="6420 Solvent services",
                                     desc="Parts washer service, %s 2026" % dt.date(2026, m, 1).strftime("%B")))
            for _ in range(int(r.integers(1, 3))):
                payments.append(dict(fac=p["fac"], vendor=W.HAULER, inv="CBE-%06d" % int(r.integers(200000, 299999)),
                                     date=dt.date(2026, m, int(r.integers(3, 27))),
                                     amount=round(float(r.uniform(900, 4200)), 2), gl="6450 Waste disposal",
                                     desc="Hazardous waste transportation and disposal"))
            if r.random() < 0.5:
                payments.append(dict(fac=p["fac"], vendor="Bellridge Safety Supply",
                                     inv="BSS-%05d" % int(r.integers(10000, 99999)),
                                     date=dt.date(2026, m, int(r.integers(2, 28))),
                                     amount=round(float(r.uniform(80, 640)), 2), gl="6310 Shop supplies",
                                     desc="Absorbent pads, safety cans, nitrile gloves"))
    for i, pmt in enumerate(sorted(payments, key=lambda x: (x["date"], x["fac"], x["inv"]))):
        pmt["line"] = i + 1
    e["ask_a"] = dict(issues=sorted(issues, key=lambda x: (x["date"], x["fac"], x["no"])),
                      manifests=sorted(manifests, key=lambda x: (x["date"], x["no"])),
                      profiles=profiles, tickets=sorted(tickets, key=lambda x: (x["date"], x["ticket"])),
                      payments=sorted(payments, key=lambda x: x["line"]), truth=truth)


# ---------------------------------------------------------------------------------------------------------------------
def gallons(code, qty, uom):
    return qty / W.density(code) if uom == "LB" else qty


def receipts(e):
    """Deliveries, returns, stock counts and the truth of each plant's unaccounted gallons."""
    inv_a, stmt_b, counts = [], [], []
    truth = {}
    na, nb = 718000, 560000
    for p in W.PLANTS:
        c = p["code"]
        r = _r("recv", c)
        rec = e["plants"][c]
        use = {}
        for row in rec["rows"]:
            use[row["material"]] = use.get(row["material"], 0.0) + gallons(row["material"], row["qty"], row["uom"])
        # press wash and cleaning bought from Haldane too
        extra = {}
        cs, rc, ik, _, pw, _ = CLEAN[c]
        for code, g in (("HW-CS-210", cs), ("HW-RC-240", rc), ("HW-IK-260", ik)):
            extra[code] = g
        pwcode = [m for m in use if m.startswith("HW-PW")]
        for m in pwcode:
            extra[m] = use[m]
        tot_used = sum(g for m, g in use.items() if ask_b_product(m))
        loss_total = LOSS[c] * tot_used
        lw = {m: g / tot_used for m, g in use.items() if ask_b_product(m)}
        un = 0.0
        for code in sorted(set(use) | set(extra)):
            used_g = use.get(code, 0.0) if ask_b_product(code) else extra.get(code, 0.0)
            sup = W.PRODUCTS[code][1]
            lb = W.PRODUCTS[code][9] == "LB"
            weekly = used_g / 50.0
            open_g = weekly * float(r.uniform(1.5, 3.5))
            loss = loss_total * lw.get(code, 0.0)
            ret_g = used_g * float(r.uniform(0.004, 0.012)) if ask_b_product(code) and used_g > 400 else 0.0
            pack = 450 if code in ("HA-SB-610", "HA-SB-620") else 500 if lb else 55 if (used_g > 900 or not
                                                                                            ask_b_product(code)) else 5
            pack_g = pack / W.density(code) if lb else float(pack)
            need = used_g + loss + ret_g + weekly * float(r.uniform(1.2, 3.0)) - open_g
            ndel = int(np.clip(round(need / pack_g / max(1.0, need / pack_g / 26.0)), 1, 60))
            packs_total = max(1, int(np.ceil(need / pack_g)))
            per = np.maximum(1, np.round(r.dirichlet([2.5] * ndel) * packs_total)).astype(int)
            ds = weekdays(r, ndel, W.FIRST_DAY - dt.timedelta(days=3), dt.date(2026, 12, 30))
            got = 0.0
            for d, k in zip(ds, per):
                qty = int(k) * pack
                got += gallons(code, qty, "LB" if lb else "GAL")
                inv_d = d + dt.timedelta(days=int(r.integers(0, 5)))
                while inv_d.weekday() > 4:
                    inv_d += dt.timedelta(days=1)
                if sup == "A":
                    na += int(r.integers(1, 30))
                    item = "%s-%02d" % (code[3:], pack)
                    inv_a.append(dict(doc="INV", no="CV%07d" % na, inv_date=inv_d, ship=d, acct=ACCOUNT_A[c],
                                      name=p["name"].upper(), item=item, desc=W.PRODUCTS[code][0], qty=qty, uom="GAL",
                                      price=INK_PRICE[code[3:5]], fac=c))
                else:
                    nb += int(r.integers(1, 30))
                    old = inv_d < W.RENUMBERED and (code, pack) in OLD_ITEM
                    item = OLD_ITEM[(code, pack)] if old else [x[0] for x in CATALOG if x[1] == code and x[2] == pack][0]
                    acct, name = ACCOUNT_B[c], p["name"].upper()
                    if p.get("old_fac") and d < W.ACQUIRED:
                        acct, name = THAMESIDE_B, p["old_name"].upper()
                    stmt_b.append(dict(doc="INV", no="HCA-%06d" % nb, date=inv_d, ship=d, acct=acct, name=name,
                                       item=item, desc="%s %s" % (SHORT[code], ("%dG" % pack) if not lb else
                                                                  ("%dLB DR" % pack)), qty=qty,
                                       price=PRICE[code], fac=c, code=code))
            if r.random() < 0.35 and used_g > 200:
                d = dt.date(2025, 12, int(r.choice([29, 30])))
                k = max(1, int(round(weekly * float(r.uniform(0.6, 1.4)) / pack_g)))
                qty = k * pack
                open_g += gallons(code, qty, "LB" if lb else "GAL")
                inv_d = dt.date(2026, 1, int(r.choice([5, 6, 7])))
                if sup == "A":
                    na += int(r.integers(1, 30))
                    inv_a.append(dict(doc="INV", no="CV%07d" % na, inv_date=inv_d, ship=d, acct=ACCOUNT_A[c],
                                      name=p["name"].upper(), item="%s-%02d" % (code[3:], pack),
                                      desc=W.PRODUCTS[code][0], qty=qty, uom="GAL", price=INK_PRICE[code[3:5]], fac=c))
                else:
                    nb += int(r.integers(1, 30))
                    item = OLD_ITEM.get((code, pack)) or [x[0] for x in CATALOG if x[1] == code and x[2] == pack][0]
                    acct, name = (THAMESIDE_B, p["old_name"].upper()) if p.get("old_fac") else (ACCOUNT_B[c],
                                                                                                p["name"].upper())
                    stmt_b.append(dict(doc="INV", no="HCA-%06d" % nb, date=inv_d, ship=d, acct=acct, name=name,
                                       item=item, desc="%s %s" % (SHORT[code], ("%dG" % pack) if not lb else
                                                                  ("%dLB DR" % pack)), qty=qty, price=PRICE[code],
                                       fac=c, code=code))
            ret = 0.0
            if ret_g > 0:
                d = weekdays(r, 1, dt.date(2026, 2, 1), dt.date(2026, 11, 30))[0]
                qty = max(pack, int(round(ret_g / pack_g)) * pack) if pack <= 5 else pack
                ret = gallons(code, qty, "LB" if lb else "GAL")
                if sup == "A":
                    na += int(r.integers(1, 30))
                    inv_a.append(dict(doc="RMA", no="CR%07d" % na, inv_date=d + dt.timedelta(days=6), ship=d,
                                      acct=ACCOUNT_A[c], name=p["name"].upper(), item="%s-%02d" % (code[3:], pack),
                                      desc="RETURN " + W.PRODUCTS[code][0], qty=-qty, uom="GAL",
                                      price=INK_PRICE[code[3:5]], fac=c))
                else:
                    nb += int(r.integers(1, 30))
                    item = [x[0] for x in CATALOG if x[1] == code and x[2] == pack][0]
                    if d + dt.timedelta(days=5) < W.RENUMBERED and (code, pack) in OLD_ITEM:
                        item = OLD_ITEM[(code, pack)]
                    stmt_b.append(dict(doc="CM", no="HCM-%06d" % nb, date=d + dt.timedelta(days=5), ship=d,
                                       acct=ACCOUNT_B[c], name=p["name"].upper(), item=item,
                                       desc="RETURN %s" % SHORT[code], qty=-qty, price=PRICE[code], fac=c, code=code))
            # the counts: opening, and closing as what is left after the year's use and loss
            in2026 = sum(gallons(code, x["qty"], "LB" if lb else "GAL") for x in (inv_a if sup == "A" else stmt_b)
                         if x["fac"] == c and (x.get("code") == code or x.get("item", "").startswith(code[3:]))
                         and x["ship"].year == 2026 and x["doc"] in ("INV",))
            close_g = open_g + in2026 - ret - used_g - loss
            if close_g < 0:
                close_g = float(r.uniform(0.2, 0.6)) * weekly
            uom = "LB" if lb else "GAL"
            f = W.density(code) if lb else 1.0
            o_q, c_q = round(open_g * f), round(close_g * f)
            counts.append(dict(fac=p["fac"], date=dt.date(2026, 1, 1), material=code, qty=o_q, uom=uom, plant=c))
            counts.append(dict(fac=p["fac"], date=dt.date(2026, 12, 31), material=code, qty=c_q, uom=uom, plant=c))
            if ask_b_product(code):
                un += gallons(code, o_q, uom) + in2026 - ret - gallons(code, c_q, uom) - used_g
        truth[c] = dict(gallons=un, used=tot_used)
    e["ask_b"] = dict(inv_a=sorted(inv_a, key=lambda x: (x["inv_date"], x["no"])),
                      stmt_b=sorted(stmt_b, key=lambda x: (x["date"], x["no"])), counts=counts, truth=truth)


def build(e):
    cleaning(e)
    receipts(e)
