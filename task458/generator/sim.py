"""task458 architecture 3: the generator's truth for Ashlund Home Group's FY2026 close.

The group's lines and what each subsidiary held at the year end, the 2025 and 2026 order books of the three trading
companies (customer shipments, returns, cancelled lines and the transfers of surplus to Valuehall), Valuehall's store
weeks since its first store opened, the trade-buyer lots, the group rate table and the facility's utilisation. Nothing
here is shipped directly: pack.py writes the files in each system's own layout.
"""
import datetime as dt
import math

import numpy as np

from world import *

WORDS = {
    "KD": (["Stainless Steel", "Enamel", "Ceramic", "Glass", "Bamboo", "Cast Iron", "Non-Stick", "Stoneware", "Acacia", "Copper Finish"],
           ["Saucepan", "Frying Pan", "Casserole", "Storage Jar", "Mixing Bowl", "Serving Platter", "Mug Set", "Utensil Set",
            "Chopping Board", "Teapot", "Dinner Set", "Baking Tray", "Colander", "Salad Bowl", "Spice Rack"]),
    "SL": (["Clear", "Grey", "White", "Wicker", "Fabric", "Stackable", "Folding", "Slimline", "Heavy Duty", "Bamboo"],
           ["Storage Box", "Laundry Basket", "Drying Rack", "Ironing Board", "Hanger Set", "Shoe Rack", "Under-Bed Box",
            "Peg Bag", "Airer", "Vacuum Bag Set", "Drawer Organiser", "Shelf Unit", "Hamper", "Clothes Rail"]),
    "LE": (["LED", "Brass", "Matt Black", "Chrome", "Rattan", "Smart", "Outdoor", "Dimmable", "Vintage", "Rechargeable"],
           ["Table Lamp", "Floor Lamp", "Ceiling Pendant", "Spotlight Bar", "Wall Light", "Extension Lead", "Night Light",
            "Desk Lamp", "Fairy Lights", "Plug Socket Timer", "Torch", "Bulb 4 Pack", "Strip Light", "Lantern"]),
    "TH": (["Steel", "Cordless", "Magnetic", "Soft Grip", "Folding", "Heavy Duty", "Compact", "Telescopic", "Brass", "Zinc"],
           ["Hammer", "Screwdriver Set", "Spirit Level", "Tape Measure", "Socket Set", "Step Ladder", "Toolbox", "Drill Bit Set",
            "Wall Plug Pack", "Padlock", "Hacksaw", "Workbench", "Hook Set", "Tool Bag", "Utility Knife"]),
    "GO": (["Rattan", "Steel", "Acacia", "Solar", "Folding", "Weatherproof", "Terracotta", "Galvanised", "Bamboo", "Resin"],
           ["Bistro Set", "Planter", "Watering Can", "Hose Reel", "Parasol", "Garden Bench", "BBQ Tool Set", "Lantern",
            "Bird Feeder", "Kneeler", "Seed Tray Set", "Compost Bin", "Fire Pit", "Garden Chair", "Pressure Sprayer"]),
}
DIV_COST = {"KD": 3.6, "SL": 4.2, "LE": 5.0, "TH": 4.6, "GO": 7.5}     # median landed unit cost, GBP
DIV_SHARE = {"KD": 0.24, "SL": 0.20, "LE": 0.20, "TH": 0.20, "GO": 0.16}
SCALE = {"AHL": 1.0, "AHI": 0.34, "AHB": 0.46}

# customers: (account, name, weight, discount off the list price). Corrib is served from Leicester until the handover.
CUSTOMERS = {
    "AHL": [("C1003", "Marlow Home Retail", 14, 0.32), ("C1011", "Brightwell Stores", 11, 0.30),
            ("C1017", "Hartley Hardware Group", 8, 0.28), ("C1024", "Greystone Home Ltd", 7, 0.27),
            ("C1032", "Medway Garden Centres", 5, 0.25), ("C1038", "Pennine Hardware", 6, 0.26),
            ("C1046", "Sutton Lane Online", 9, 0.22), ("C1051", "Brook & Vale", 4, 0.24),
            ("C1059", "Calder Homeware", 5, 0.25), ("C1064", "Ashby Value Stores", 8, 0.34),
            ("C1072", "Larkspur Interiors", 3, 0.20), ("C1080", "Holloway & Pratt", 4, 0.23),
            ("C1093", "Shannonside Hardware", 3, 0.26), ("C1105", "Corrib Home & Garden", 11, 0.27)],
    "AHI": [("IE2001", "Liffey Stores", 12, 0.30), ("IE2004", "Barrow DIY", 7, 0.27), ("IE2009", "Slaney Homewares", 6, 0.25),
            ("IE2013", "Errigal Garden World", 4, 0.24), ("IE2018", "Boyne Value", 8, 0.33),
            ("IE2022", "Atlantic Hardware", 5, 0.26), ("IE2031", "Corrib Home & Garden", 9, 0.27)],
    "AHB": [("200114", "Waalhuis Wonen", 12, 0.31), ("200127", "Kempen Bouwmarkt", 8, 0.28),
            ("200133", "Dommel Tuincentrum", 5, 0.24), ("200148", "Brabant Huishoud", 7, 0.29),
            ("200152", "Veluwe Wonen", 6, 0.27), ("200167", "Zeeland Doe-het-zelf", 5, 0.26),
            ("200171", "Utrechtse Woonwarenhuis", 4, 0.23), ("200189", "Kanaal Online B.V.", 7, 0.21)],
}
KESTREL = ("C1118", "Kestrel DIY Ltd")             # the customer programme that ended with 2025
PRICE_RISE = dt.date(2025, 4, 1)                    # AHL's list prices rose on this date
PRICE_RISE_FACTOR = {"KD": 1.02, "SL": 1.12, "LE": 1.11, "TH": 1.03, "GO": 1.13}   # by division
PROTECT_END = dt.date(2025, 6, 30)                  # five key accounts held at their old prices to this date
NONSTOCK = "NS001"                                  # AHL's non-stock code for price-only credit lines
PROTECTED = ("Marlow Home Retail", "Brightwell Stores", "Hartley Hardware Group", "Greystone Home Ltd",
             "Ashby Value Stores")
VALUEHALL_ACCT = {"AHL": "C9001", "AHI": "IE9001", "AHB": "209001"}

HOLIDAYS = {
    "AHL": ["2025-01-01", "2025-04-18", "2025-04-21", "2025-05-05", "2025-05-26", "2025-08-25", "2025-12-25", "2025-12-26",
            "2026-01-01", "2026-04-03", "2026-04-06", "2026-05-04", "2026-05-25", "2026-08-31", "2026-12-25", "2026-12-28"],
    "AHI": ["2025-01-01", "2025-02-03", "2025-03-17", "2025-04-21", "2025-05-05", "2025-06-02", "2025-08-04", "2025-10-27",
            "2025-12-25", "2025-12-26", "2026-01-01", "2026-02-02", "2026-03-17", "2026-04-06", "2026-05-04", "2026-06-01",
            "2026-08-03", "2026-10-26", "2026-12-25", "2026-12-28"],
    "AHB": ["2025-01-01", "2025-04-18", "2025-04-21", "2025-04-26", "2025-05-05", "2025-05-29", "2025-06-09", "2025-12-25",
            "2025-12-26", "2026-01-01", "2026-04-03", "2026-04-06", "2026-04-27", "2026-05-14", "2026-05-25", "2026-12-25",
            "2026-12-26"],
}


def mondays(start, end):
    d = start - dt.timedelta(days=start.weekday())
    out = []
    while d <= end:
        out.append(d)
        d += dt.timedelta(days=7)
    return out


def working_days(sub, start, end):
    hol = {dt.date.fromisoformat(h) for h in HOLIDAYS[sub]}
    d, out = start, []
    while d <= end:
        if d.weekday() < 5 and d not in hol:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def items(rng):
    """The group item master: about 1,360 lines plus the Lumio smart-lighting range launched in March 2026."""
    out = []
    used = set()
    code = 10400
    for div in DIVISIONS:
        n = int(round(1360 * DIV_SHARE[div]))
        adj, noun = WORDS[div]
        for k in range(n):
            code += int(rng.integers(3, 17))
            for _ in range(20):
                name = "%s %s" % (adj[int(rng.integers(len(adj)))], noun[int(rng.integers(len(noun)))])
                size = ["", " Small", " Medium", " Large", " 2 Pack", " Set of 4", " 30cm", " 45cm"][int(rng.integers(8))]
                if (name + size) not in used:
                    break
            used.add(name + size)
            cost = float(np.round(DIV_COST[div] * math.exp(rng.normal(0, 0.62)), 2))
            cost = max(0.62, min(cost, 68.0))
            case = int(rng.choice([1, 4, 6, 6, 12, 12, 24]))
            launch = dt.date(int(rng.integers(2014, 2026)), int(rng.integers(1, 13)), 1)
            out.append(dict(code="AH%05d" % code, desc=name + size, div=div, cost=cost, case=case,
                            launch=launch, lumio=False))
    lumio = ["Lumio Smart Bulb E27", "Lumio Smart Bulb B22", "Lumio Smart Bulb GU10", "Lumio Colour Strip 2m",
             "Lumio Colour Strip 5m", "Lumio Smart Table Lamp", "Lumio Smart Floor Lamp", "Lumio Smart Plug",
             "Lumio Hub", "Lumio Motion Sensor", "Lumio Smart Bulb E14", "Lumio Starter Kit", "Lumio Outdoor Strip",
             "Lumio Filament Bulb E27", "Lumio Smart Spot 3 Pack", "Lumio Ceiling Panel"]
    for j, nm in enumerate(lumio):
        for var in ["", " Twin Pack"]:
            code += int(rng.integers(3, 9))
            cost = float(np.round(6.4 * math.exp(rng.normal(0, 0.45)), 2))
            out.append(dict(code="AH%05d" % code, desc=nm + var, div="LE", cost=cost,
                            case=int(rng.choice([6, 12, 12, 24])), launch=dt.date(2026, 3, 2), lumio=True))
    for it in out:
        lp = it["cost"] * math.exp(rng.normal(math.log(1.72), 0.09))
        it["list_gbp"] = float(np.round(lp, 2))
        it["list_eur"] = float(np.round(lp / 0.86, 2))
    return out


def ranges(rng, its):
    """Which subsidiary stocks which line, each line's weekly demand in 2026 and 2025 (units) and its year-end stock."""
    rows = []
    for it in its:
        if it["lumio"]:
            subs = ["AHL", "AHB"] if rng.random() < 0.75 else ["AHL"]
        else:
            subs = ["AHL"] if rng.random() < 0.88 else []
            if rng.random() < 0.36:
                subs.append("AHI")
            if rng.random() < 0.52:
                subs.append("AHB")
            if not subs:
                subs = ["AHL"]
        for s in subs:
            scale = SCALE[s]
            if it["lumio"]:
                wk = float(np.round(scale * 34.0 * math.exp(rng.normal(0, 0.5)), 3))
                bought = scale * 11600 * math.exp(rng.normal(0, 0.3))
                stock = int(round(bought - 43 * wk))
                kind = "lumio"
                wk25 = 0.0
            else:
                wk = float(np.round(scale * 880 / max(it["cost"], 0.8) * math.exp(rng.normal(0, 0.9)), 3))
                r = rng.random()
                if r < 0.02:
                    kind, cover = "dead", None
                elif r < 0.064:
                    kind, cover = "over", 52 * math.exp(rng.normal(0.42, 0.30))
                else:
                    kind, cover = "normal", 13.506 * math.exp(rng.normal(0, 0.36))
                if kind == "dead":
                    stock = int(round(scale * 5200 / max(it["cost"], 0.8) * math.exp(rng.normal(0, 0.6))))
                    wk25 = 6.0 * scale * math.exp(rng.normal(0, 0.5))
                    wk = 0.0
                else:
                    stock = int(round(wk * cover))
                    wk25 = wk * math.exp(rng.normal(0.05, 0.25))
                    if kind == "over":
                        wk25 = wk25 * math.exp(rng.normal(0.85, 0.25))   # the lines a customer programme took in 2025
            stock = max(stock, 0)
            if s == "AHL":
                ucost = it["cost"]
            elif s == "AHI":
                ucost = float(np.round(it["cost"] / FX_CLOSE * math.exp(rng.normal(0.03, 0.02)), 4))
            else:
                ucost = float(np.round(it["cost"] / FX_CLOSE * math.exp(rng.normal(0.0, 0.02)), 4))
            rows.append(dict(sub=s, code=it["code"], div=it["div"], cost=it["cost"], ucost=ucost, case=it["case"],
                             wk=wk, wk25=wk25, stock=stock, kind=kind, lumio=it["lumio"], desc=it["desc"]))
    return rows


def pick_customer(rng, sub, date, wts):
    cust = CUSTOMERS[sub]
    while True:
        c = cust[int(rng.choice(len(cust), p=wts))]
        if c[1] == "Corrib Home & Garden":
            if sub == "AHL" and date >= CORRIB_HANDOVER:
                continue
            if sub == "AHI" and date < CORRIB_HANDOVER:
                continue
        return c


def shipments(rng, its, rows):
    """Customer order lines for 2025 and 2026: shipped lines, returns and cancelled lines, quantities in eaches."""
    by_code = {it["code"]: it for it in its}
    wts = {s: np.array([c[2] for c in CUSTOMERS[s]], float) / sum(c[2] for c in CUSTOMERS[s]) for s in CUSTOMERS}
    wdays = {(s, y): working_days(s, dt.date(y, 1, 1), dt.date(y, 12, 31)) for s in SUBS for y in (2025, 2026)}
    lumio_days = {s: [d for d in wdays[(s, 2026)] if d >= dt.date(2026, 3, 2)] for s in SUBS}
    lines = []
    for r in rows:
        s, code = r["sub"], r["code"]
        it = by_code[code]
        case = it["case"]
        for yr in (2025, 2026):
            if it["lumio"] and yr == 2025:
                continue
            if r["kind"] == "dead" and yr == 2026:
                continue
            level = r["wk"] if yr == 2026 else r["wk25"]
            units = level * (43 if it["lumio"] else 52)
            cases = int(round(units / case))
            if cases <= 0:
                continue
            mean_cases = max(1.0, cases / (8 + 22 * rng.random()))
            n = int(max(1, min(cases, round(cases / mean_cases))))
            qs = rng.multinomial(cases, np.ones(n) / n)
            days = lumio_days[s] if it["lumio"] else wdays[(s, yr)]
            kestrel_share = 0.0
            if s == "AHL" and yr == 2025 and r["kind"] == "over":
                kestrel_share = max(0.0, 1.0 - r["wk"] / max(r["wk25"], 1e-9))
            for q in qs:
                if q <= 0:
                    continue
                d = days[int(rng.integers(len(days)))]
                if kestrel_share and rng.random() < kestrel_share:
                    acct, name, disc = KESTREL[0], KESTREL[1], 0.35
                else:
                    acct, name, _, disc = pick_customer(rng, s, d, wts[s])
                lines.append(dict(sub=s, code=code, date=d, qty=int(q) * case, acct=acct, cust=name, disc=disc,
                                  kind="ship"))
    # AHL's list prices rose on 1 April 2025; five key accounts were held at their old prices to 30 June, but the
    # hold was missing on some of their lines, which were invoiced at the new price and credited in July
    rd = np.random.default_rng(SEED + 23)
    q1 = sorted({(ln["cust"], ln["code"]) for ln in lines
                 if ln["sub"] == "AHL" and ln["cust"] in PROTECTED and ln["date"] < PRICE_RISE})
    unheld = {k for k in q1 if rd.random() < 0.7}

    def over(ln):
        return (ln["sub"] == "AHL" and ln["kind"] == "ship" and ln["cust"] in PROTECTED and
                PRICE_RISE <= ln["date"] <= PROTECT_END and (ln["cust"], ln["code"]) in unheld)

    rets = []
    for ln in lines:
        if rng.random() < 0.03:
            case = by_code[ln["code"]]["case"]
            q = max(1, int(round(ln["qty"] / case * rng.uniform(0.15, 1.0)))) * case
            d = ln["date"] + dt.timedelta(days=int(rng.integers(3, 41)))
            while d.weekday() >= 5:
                d += dt.timedelta(days=1)
            if d.year > 2026:
                continue
            if over(ln):
                continue
            rets.append(dict(ln, date=d, qty=-q, kind="return", ship_date=ln["date"]))
    canc = []
    for ln in lines:
        if rng.random() < 0.015:
            canc.append(dict(ln, kind="cancelled"))
    allr = lines + rets + canc
    for ln in allr:
        it = by_code[ln["code"]]
        if ln["sub"] == "AHL":
            cur = "GBP"
            d0 = ln.get("ship_date", ln["date"])
            new_list = it["list_gbp"]
            old_list = float(np.round(new_list / PRICE_RISE_FACTOR[it["div"]], 2))
            held = (ln["cust"] in PROTECTED and PRICE_RISE <= d0 <= PROTECT_END and
                    (ln["cust"], ln["code"]) not in unheld)
            lst = old_list if (d0 < PRICE_RISE or held) else new_list
            ln["contract"] = float(np.round(old_list * (1 - ln["disc"]), 2))
        else:
            cur = "EUR"
            lst = it["list_eur"]
        ln["unit_price"] = float(np.round(lst * (1 - ln["disc"]), 2))
        ln["cur"] = cur
        ln["value"] = float(np.round(ln["qty"] * ln["unit_price"], 2))
    by_order = {}
    for ln in lines:
        if ln["sub"] == "AHL":
            by_order.setdefault((ln["date"], ln["acct"]), []).append(ln)
    july = working_days("AHL", dt.date(2025, 7, 1), dt.date(2025, 7, 31))
    # AHL's system takes a price-only credit on its non-stock code (a stock item on a credit line would book goods
    # back in), so each corrected line becomes one credit line on NS001 under the original order
    credits = []
    for key in sorted(by_order):
        ols = sorted(by_order[key], key=lambda a: (a["code"], a["qty"]))
        hit = [ln for ln in ols if over(ln)]
        if not hit:
            continue
        d = july[int(rd.integers(len(july)))]
        for ln in hit:
            amt = float(np.round(ln["qty"] * (ln["unit_price"] - ln["contract"]), 2))
            credits.append(dict(sub="AHL", code=NONSTOCK, date=d, qty=0, acct=ln["acct"], cust=ln["cust"],
                                disc=ln["disc"], kind="price", unit_price=0.0, cur="GBP", value=-amt, orig=key,
                                corrects=ln["code"]))
    allr += credits
    allr.sort(key=lambda x: (x["sub"], x["date"], x["acct"], x["code"], x["kind"], x["qty"]))
    return allr


def segments(yr):
    """The stock system's trading weeks in a year: Monday to Sunday, the first and last cut at the year end."""
    out = []
    d = dt.date(yr, 1, 1)
    while d.year == yr:
        e = d + dt.timedelta(days=6 - d.weekday())
        e = min(e, dt.date(yr, 12, 31))
        out.append((d, e))
        d = e + dt.timedelta(days=1)
    return out


def outlet(rng, pool_by_year):
    """Valuehall's store weeks, 2021 to 2026: trading days, goods in, sales at cost and ex VAT, closing stock.

    pool_by_year: the cost value of surplus the group sends the outlet over each year (the generator's choice).
    Returns (weeks, jobbed): jobbed lists the outlet's own sales of aged stock to trade buyers.
    """
    weeks = []
    stock = {s[0]: 0.0 for s in STORES}
    opened = {s[0]: s[2] for s in STORES}
    jobbed = []
    pending = {}
    ix = {s[0]: 0 for s in STORES}
    for yr in range(2021, 2027):
        segs = segments(yr)
        open_stores = [s[0] for s in STORES if s[2].year <= yr]
        sw = {s: sum(1 for a, b in segs if a >= opened[s]) for s in open_stores}
        tot_sw = sum(sw.values())
        intake = pool_by_year[yr]
        for a, b in segs:
            for s in open_stores:
                if a < opened[s]:
                    continue
                span = [a + dt.timedelta(days=k) for k in range((b - a).days + 1)]
                shut = {d for d in span if (d.month, d.day) in ((12, 25), (12, 26))}
                if s == "VH02" and dt.date(2025, 2, 10) <= a <= dt.date(2025, 2, 17):
                    shut |= set(span)    # refit
                if s == "VH01" and a == dt.date(2023, 9, 4):
                    shut |= set(span)    # flood repair
                days = len(span) - len(shut)
                gi = 0.0
                wk_ix = ix[s]
                ix[s] += 1
                if wk_ix == 0:
                    gi = THROUGHPUT * 3.2
                elif (wk_ix % 2 == 0) and days > 0:
                    gi = intake / tot_sw * 2.0 * math.exp(rng.normal(0, 0.18))
                out_lot = 0.0
                if s in pending and a >= pending[s][0]:
                    out_lot = min(pending[s][1], stock[s])
                    jobbed.append(dict(store=s, date=a + dt.timedelta(days=2), cost=out_lot))
                    stock[s] -= out_lot
                    del pending[s]
                avail = stock[s] + gi
                potential = THROUGHPUT * days / 7.0 * math.exp(rng.normal(0, THROUGHPUT_SD))
                sales = min(potential, avail / COVER_FULL) if days > 0 else 0.0
                if a.month == 1 and a.day <= 28:
                    band, rec = "January sale", OUTLET_RECOVERY - 0.085
                elif rng.random() < 0.12:
                    band, rec = "Multibuy", OUTLET_RECOVERY - 0.035
                else:
                    band, rec = "", OUTLET_RECOVERY + 0.012
                rec = rec + rng.normal(0, 0.006)
                shrink = sales * 0.004 * math.exp(rng.normal(0, 0.3))
                stock[s] = avail - sales - shrink
                weeks.append(dict(store=s, week=a, end=b, days=days, goods_in=gi, sales_cost=sales,
                                  sales_exvat=sales * rec, close=stock[s], band=band, jobbed=out_lot))
        if yr == 2023:
            for j, s in enumerate(open_stores):
                excess = stock[s] - THROUGHPUT * 5.0
                if excess > 0:
                    pending[s] = (dt.date(2024, 2, 5) + dt.timedelta(days=7 * j), excess * 0.74)
    return weeks, jobbed


POOL = {2021: 420e3, 2022: 860e3, 2023: 2300e3, 2024: 1250e3, 2025: 2340e3, 2026: 2460e3}


def transfers(rng, rows, weeks):
    """Each Valuehall goods-in of 2025 and 2026 as the order lines the sending companies raised (at cost)."""
    split = {"AHL": 0.72, "AHB": 0.18, "AHI": 0.10}
    pools = {s: [r for r in rows if r["sub"] == s and not r["lumio"]] for s in SUBS}
    slow = {s: [r for r in pools[s] if r["kind"] != "normal"] or pools[s] for s in SUBS}
    out = []
    for w in weeks:
        if w["week"].year < 2025 or w["goods_in"] <= 0:
            continue
        sh = {s: split[s] * math.exp(rng.normal(0, 0.25)) for s in SUBS}
        tot = sum(sh.values())
        for s in SUBS:
            val = w["goods_in"] * sh[s] / tot
            k = int(rng.integers(2, 5))
            parts = rng.dirichlet(np.ones(k)) * val
            for p in parts:
                src = slow[s] if rng.random() < 0.7 else pools[s]
                r = src[int(rng.integers(len(src)))]
                q = max(1, int(round(p / r["cost"] / r["case"]))) * r["case"]
                lag = {"AHL": 3, "AHI": 6, "AHB": 5}[s]
                d = w["week"] - dt.timedelta(days=lag)
                while d.weekday() >= 5:
                    d -= dt.timedelta(days=1)
                cur = "GBP" if s == "AHL" else "EUR"
                unit = r["ucost"] if s != "AHL" else r["cost"]
                out.append(dict(sub=s, code=r["code"], date=d, qty=q, acct=VALUEHALL_ACCT[s], cust="Valuehall Stores Ltd",
                                disc=0.0, kind="transfer", unit_price=float(np.round(unit, 2)), cur=cur,
                                value=float(np.round(q * unit, 2)), store=w["store"]))
    return out


def trade_lots(rng, jobbed):
    """Lots sold to trade buyers 2021 to 2026: the subsidiaries' dead lines each year and the outlet's 2024 clear-out."""
    buyers = ["Kirkby Surplus Ltd", "Midland Clearance Co", "J & M Bulk Buyers", "Tamworth Trade Lots",
              "Stockline Liquidations", "Ferrybridge Wholesale"]
    out = []
    for yr in range(2021, 2027):
        for k in range(int(rng.integers(5, 10))):
            seller = ["Ashlund Home Ltd", "Ashlund Home Ltd", "Ashlund Home Ltd", "Ashlund Home Ireland Ltd",
                      "Ashlund Home B.V."][int(rng.integers(5))]
            cost = float(np.round(rng.uniform(14e3, 85e3), 2))
            d = dt.date(yr, int(rng.integers(1, 13)), int(rng.integers(1, 28)))
            out.append(dict(date=d, seller=seller, cost=cost))
    for yr, mo, cost in ((2022, 3, 236412.37), (2025, 10, 318764.91)):   # range clear-outs sold as single lots
        out.append(dict(date=dt.date(yr, mo, int(rng.integers(3, 25))), seller="Ashlund Home Ltd", cost=cost))
    for j in jobbed:
        out.append(dict(date=j["date"] - dt.timedelta(days=9), seller="Valuehall Stores Ltd",
                        cost=float(np.round(j["cost"], 2)), store=j["store"]))
    out.sort(key=lambda x: (x["date"], x["seller"]))
    for n, o in enumerate(out):
        o["lot"] = "TL%03d" % (101 + n)
        o["buyer"] = buyers[int(rng.integers(len(buyers)))]
        o["price"] = float(np.round(o["cost"] * JOBBER_RECOVERY * math.exp(rng.normal(0, 0.04)), -1))
        o["pallets"] = max(2, int(round(o["cost"] / 1450 * math.exp(rng.normal(0, 0.15)))))
        o["collected"] = o["date"] + dt.timedelta(days=int(rng.integers(5, 22)))
    for o in out:   # no lot is signed on a bank holiday: one dated Christmas or Boxing Day moves to the next working day
        while (o["date"].month, o["date"].day) in ((12, 25), (12, 26)) or o["date"].weekday() >= 5 and \
                (o["date"].month, o["date"].day) >= (12, 25):
            o["date"] += dt.timedelta(days=1) if o["date"].day < 31 else -dt.timedelta(days=3)
    return out


def fx_table(rng):
    """Monthly average and month-end EUR to GBP rates, 2025 and 2026, matching the group's year averages and close."""
    out = []
    for yr, avg in ((2025, FX_AVG_2025), (2026, FX_AVG_2026)):
        dev = rng.normal(0, 0.0045, 12)
        dev = dev - dev.mean()
        for m in range(12):
            a = float(np.round(avg + dev[m], 4))
            c = float(np.round(a + rng.normal(0, 0.0022), 4))
            out.append(dict(year=yr, month=m + 1, avg=a, close=c))
    out[-1]["close"] = FX_CLOSE
    return out


def utilisation(rng):
    """Daily drawn balance on the revolving facility through 2026 (drawings and repayments in 250,000s)."""
    out = []
    bal = 21_500_000
    d = dt.date(2026, 1, 1)
    while d <= dt.date(2026, 12, 31):
        if d.weekday() < 5 and rng.random() < 0.55:
            bal += int(rng.choice([-6, -4, -3, -2, -1, 1, 2, 3, 4, 6])) * 50_000
            bal = int(min(max(bal, 15_000_000), 29_500_000))
        out.append(dict(date=d, drawn=bal))
        d += dt.timedelta(days=1)
    gap = DRAWN - out[-1]["drawn"]
    for o in out:
        if o["date"] >= dt.date(2026, 12, 14):
            o["drawn"] += gap
    return out


def everything():
    rng = np.random.default_rng(SEED)
    its = items(rng)
    rows = ranges(rng, its)
    ship = shipments(rng, its, rows)
    weeks, jobbed = outlet(np.random.default_rng(SEED + 5), POOL)
    tr = transfers(np.random.default_rng(SEED + 7), rows, weeks)
    lots = trade_lots(np.random.default_rng(SEED + 11), jobbed)
    fx = fx_table(np.random.default_rng(SEED + 13))
    util = utilisation(np.random.default_rng(SEED + 17))
    return dict(items=its, rows=rows, ship=ship, weeks=weeks, jobbed=jobbed, transfers=tr, lots=lots, fx=fx, util=util)
