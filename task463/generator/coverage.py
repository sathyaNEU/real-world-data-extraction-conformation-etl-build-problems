"""The coverage files: the supermarkets' 2025 returns of retail sales by their own categories, the office's map of the
retailers' categories to RPI items built from the 2024 returns, and the office's estimate of households' 2025 spending
on each item.

Each supermarket's 2025 sales come from its own lines' months, so the returns agree with the feeds: September to
December 2025 as the lines sold them, January to August 2025 from the same lines' offer months (the campaign calendar
runs November to July) and offer-free months at the prices of the time. Wrenfold's return is a half-year report from its
sales system with units beside value: from 1 July 2025 its product hierarchy numbered the packaged categories in store
order, so nearly every one took the number another had held in 2024, and the report labels each number with the
category that holds it now: the first half's sales, recorded under the numbers of the time, sit beside the names of the
categories that took those numbers over (the second half's names are right). Gorsedale's return carries its trade sales to cafes and
guest houses beside its retail sales; Calderby's is net of GST."""
import numpy as np

import sim as S
import world as W

# Wrenfold's categories in its 2024 hierarchy, the one the office's map was built from: category number, category,
# RPI item
WREN_2024 = [
    ("110", "Bread and rolls", "1101"), ("115", "Breakfast cereals and porridge", "1103"),
    ("120", "Pasta, rice and noodles", "1105"), ("125", "Biscuits", "1108"), ("130", "Yoghurts", "1145"),
    ("135", "Cheese", "1146"), ("140", "Butter and spreads", "1151"), ("145", "Confectionery", "1182"),
    ("150", "Coffee", "1211"), ("155", "Tea", "1212"), ("160", "Soft drinks", "1221"), ("165", "Water", "1222"),
    ("170", "Juices", "1223"), ("175", "Cakes and bakery snacks", "1109"), ("180", "Crisps and snacks", "1191"),
    ("210", "Laundry", "5611"), ("215", "Toilet and kitchen rolls", "5613"), ("220", "Dishwashing", "5612"),
    ("310", "Toiletries", "6213"), ("320", "Cosmetics", "6214"),
    ("410", "Fresh fruit and vegetables", "1171"), ("420", "Fresh meat and fish", "1121"),
]
# Wrenfold's 2025 hierarchy, from 1 July 2025, numbers the packaged categories in store order: each category below
# carries the 2024 number of the category set against it; cosmetics and the fresh departments keep theirs
TAKES = {"1101": "1182", "1103": "1105", "1105": "1151", "1108": "1145", "1145": "5613", "1146": "5611",
         "1151": "1212", "1182": "1101", "1211": "1221", "1212": "1223", "1221": "1211", "1222": "5612",
         "1223": "1108", "5611": "1146", "5613": "6213", "6213": "1103", "1109": "1191", "1191": "1109",
         "5612": "1222"}
GORS = [("BAK", "Bakery", "1101"), ("CER", "Cereals", "1103"), ("DRY", "Pasta and rice", "1105"),
        ("BIS", "Biscuits", "1108"), ("CAK", "Cakes", "1109"), ("YOG", "Yoghurt", "1145"), ("CHE", "Cheese", "1146"),
        ("BUT", "Butter and fats", "1151"), ("CON", "Confectionery", "1182"), ("SNK", "Snacks", "1191"),
        ("COF", "Coffee", "1211"), ("TEA", "Tea", "1212"), ("SDR", "Soft drinks", "1221"), ("WAT", "Water", "1222"),
        ("JUI", "Juice", "1223"), ("LAU", "Laundry", "5611"), ("DSH", "Dishwashing", "5612"),
        ("PAP", "Paper", "5613"), ("TOI", "Toiletries", "6213"), ("COS", "Cosmetics", "6214"),
        ("FRE", "Fresh produce", "1171"), ("MEA", "Butchery", "1121")]
CALD = [("101", "Bread", "1101"), ("102", "Cereal", "1103"), ("103", "Pasta & rice", "1105"), ("104", "Biscuits", "1108"),
        ("105", "Cakes", "1109"), ("111", "Yogurt", "1145"), ("112", "Cheese", "1146"), ("113", "Butter & spreads", "1151"),
        ("121", "Sweets & chocolate", "1182"), ("122", "Snacks", "1191"), ("131", "Coffee", "1211"), ("132", "Tea", "1212"),
        ("133", "Soft drinks", "1221"), ("134", "Water", "1222"), ("135", "Juice", "1223"), ("141", "Fresh produce", "1171"),
        ("142", "Meat & fish", "1121"), ("201", "Laundry", "5611"), ("202", "Paper products", "5613"),
        ("203", "Dishwashing", "5612"), ("301", "Health & beauty", "6213"), ("302", "Cosmetics", "6214")]
# fresh food, which the feeds do not carry: its monthly sales against the retailer's packaged items, and its unit price
FRESH = {"1171": (0.62, 1.18), "1121": (0.54, 4.85)}
TRADE_ITEMS = ("1101", "1146", "1151", "1211", "1212", "1221", "1222", "1223", "5613")
PACKAGED = W.ICODE + [c for c, n, p in S.OUT_OF_SCOPE]
TREND = dict({i[0]: i[5] for i in W.ITEMS}, **{c: 0.03 for c, n, p in S.OUT_OF_SCOPE})
OFFER_2025 = {1, 2, 3, 4, 5, 6, 7, 11, 12}     # January to July and November to December carry the monthly offers


def _season(item):
    s = S.SEASON.get(item, [1.0] * W.NM)
    return [s[k] * S.VISITORS[k] for k in range(W.NM)]


def _k(month):
    """The parallel year's month with the same calendar name (September 2025 = 0; January 2026 = 4)."""
    return month - 9 if month >= 9 else month + 3


def months_2025(ls, rng):
    """{(retailer, item): (value with GST, units)} for each calendar month of 2025, from the lines' own months."""
    V, U = {}, {}
    for L in ls:
        key = (L["retailer"], L["item"])
        v, u = V.setdefault(key, np.zeros(W.NM)), U.setdefault(key, np.zeros(W.NM))
        for m in range(W.NM):
            q = L["units"][m]
            if q <= 0:
                continue
            mu = L["member_share"][m] if L["member_price"][m] is not None else 0.0
            v[m] += q * (L["shelf"][m] * (1 - mu) + (L["member_price"][m] or 0) * mu)
            u[m] += q
    out = {}
    for r in W.RETAILERS:
        for it in PACKAGED:
            v, u, s = V[(r, it)], U[(r, it)], _season(it)
            u_free, p_free = u[0:2].sum() / sum(s[0:2]), v[0:2].sum() / u[0:2].sum()
            u_off, p_off = u[2:6].sum() / sum(s[2:6]), v[2:6].sum() / u[2:6].sum()
            val, uni = np.zeros(12), np.zeros(12)
            for mo in range(1, 13):
                if mo >= 9:
                    k = _k(mo)
                    e = float(np.exp(rng.normal(0, 0.01)))
                    val[mo - 1], uni[mo - 1] = v[k] * e, u[k] * e
                    continue
                k = _k(mo)
                if mo in OFFER_2025:
                    q, p = u_off * s[k], p_off * (1 + TREND[it]) ** ((mo - 12.5) / 12)
                else:
                    q, p = u_free * s[k], p_free * (1 + TREND[it]) ** ((mo - 9.5) / 12)
                q *= float(np.exp(rng.normal(0, 0.03)))
                p *= float(np.exp(rng.normal(0, 0.006)))
                uni[mo - 1], val[mo - 1] = q, q * p
            out[(r, it)] = (val, uni)
        pk = sum(out[(r, it)][0] for it in W.ICODE)
        for it, (frac, price) in FRESH.items():
            val = pk * frac * np.exp(rng.normal(0, 0.04, 12)) * float(np.exp(rng.normal(0, 0.08)))
            out[(r, it)] = (val, val / (price * float(np.exp(rng.normal(0, 0.03)))))
    return out


def halves(mo):
    val, uni = mo
    return float(val[:6].sum()), float(val[6:].sum()), float(uni[:6].sum()), float(uni[6:].sum())


def wren_rows(mo):
    """Wrenfold's report: one row per code, labelled with the category holding the code since July 2025, its first half
    the sales recorded under the code (by the 2024 hierarchy) and its second half the sales of the category holding it."""
    code24 = {it: c for c, n, it in WREN_2024}
    name = {it: n for c, n, it in WREN_2024}
    holder = {code24[TAKES.get(it, it)]: it for c, n, it in WREN_2024}      # 2025 code -> category holding it
    rows = []
    for c, n, it24 in WREN_2024:
        it25 = holder[c]
        a = halves(mo[("W", it24)])
        b = halves(mo[("W", it25)])
        rows.append([c, name[it25], int(round(a[2])), round(a[0], 2), int(round(b[3])), round(b[1], 2)])
    rows.sort(key=lambda r: r[0])
    return rows


def build(seed, ls, offset=None):
    """The returns' rows, the category map, the households' spending by item, and the coverage each implies."""
    rng = np.random.default_rng([seed, 201, W.COVER_OFFSET if offset is None else offset])
    cov = {}
    for code in W.ICODE:
        rng.normal(np.log(9500), 0.30)
        cov[code] = float(rng.uniform(0.55, 0.80))
        rng.normal(0, [0.35, 0.15, 0.15])
    for code in ("1109", "1191", "5612", "6214", "1171", "1121"):
        for r in W.RETAILERS:
            rng.normal(np.log(2.2e6), 0.5)
    trade_f = {code: float(rng.uniform(0.10, 0.22)) for code in TRADE_ITEMS}
    mo = months_2025(ls, rng)
    annual = {k: float(v[0].sum()) for k, v in mo.items()}
    wren = wren_rows(mo)
    gors = []
    for code, nm, it in GORS:
        gors.append(["Retail", code, nm, round(annual[("G", it)], 2)])
        if it in trade_f:
            gors.append(["Trade", code, nm, round(annual[("G", it)] * trade_f[it], 2)])
    cald = [[code, nm, round(annual[("C", it)] / (1 + W.GST), 2)] for code, nm, it in CALD]
    cmap = [["Wrenfold Stores", c, n, it] for c, n, it in WREN_2024]
    cmap += [["Gorsedale Co-operative", c, n, it] for c, n, it in GORS]
    cmap += [["Calderby's", c, n, it] for c, n, it in CALD]
    # each item's sales as the returns state them, read the right way (Wrenfold's first half by its codes in the map,
    # its second half by its names; Gorsedale's retail rows; Calderby's with GST): the households' spending is set
    # against them at the item's coverage, in whole thousands of pounds kept clear of a whole-per-cent edge
    num = {it: 0.0 for it in W.ICODE}
    by_code = {c: it for c, n, it in WREN_2024}
    by_name = {n: it for c, n, it in WREN_2024}
    for c, nm, u1, v1, u2, v2 in wren:
        for it, v in ((by_code[c], v1), (by_name[nm], v2)):
            if it in num:
                num[it] += v
    for ch, c, nm, v in gors:
        it = dict((cc, i) for cc, n, i in GORS)[c]
        if ch == "Retail" and it in num:
            num[it] += v
    for c, nm, v in cald:
        it = dict((cc, i) for cc, n, i in CALD)[c]
        if it in num:
            num[it] += v * (1 + W.GST)
    spend, coverage = {}, {}
    for it in W.ICODE:
        target = num[it] / cov[it] / 1000.0
        base = int(round(target))
        for step in (0, 1, -1, 2, -2, 3, -3):
            s_ = base + step
            c_ = 100.0 * num[it] / 1000.0 / s_
            if abs(c_ % 1 - 0.5) >= 0.15:
                break
        spend[it], coverage[it] = s_, c_
    return {"spend": spend, "wren": wren, "gors": gors, "cald": cald, "map": cmap, "coverage": coverage,
            "months": mo, "trade_f": trade_f, "target_cov": cov}
