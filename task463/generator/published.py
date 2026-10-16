"""The field collection behind the published index: a collector prices a fixed sample of product lines at nine outlets on
the index day each month (the shelf price, offers included, member prices not), and the published item index is the
geometric mean of the quotes' price relatives within each year, linked in January. Quotes run from January 2024 so the
published series has its history; the transaction lines' prices before September 2025 are carried back from their
first month."""
import datetime as dt

import numpy as np

import sim as S
import world as W

# outlet code, name, retailer key or None for an independent, parish, collected from, collected to, replaces, in index
OUTLETS = [
    ("211", "Wrenfold Harbour Street", "W", "Port Kellan", "2019-01", None, None, "Y"),
    ("214", "Wrenfold Elskirk", "W", "Elskirk", "2019-01", "2026-02", None, "Y"),
    ("216", "Wrenfold Thornsay", "W", "Thornsay", "2019-01", None, None, "Y"),
    ("221", "Gorsedale Co-op Market Street", "G", "Port Kellan", "2019-01", None, None, "Y"),
    ("223", "Gorsedale Co-op Pier Road", "G", "Carrow", "2019-01", None, None, "Y"),
    ("231", "Calderby's Westgate", "C", "Port Kellan", "2019-01", None, None, "Y"),
    ("233", "Calderby's Ferry Lane", "C", "Lowender", "2019-01", None, None, "Y"),
    ("238", "Wrenfold Elskirk (Quay Road)", "W", "Elskirk", "2026-03", None, "214", "Y"),
    ("241", "Hollis Stores", None, "Hallow Cross", "2019-01", None, None, "Y"),
    ("243", "Lantern Lane Grocers", None, "Thornsay", "2019-01", None, None, "Y"),
    ("249", "Wrenfold online (collection trial)", "W", "Online", "2026-01", None, None, "N"),
]
# the published index's months: January 2024 to September 2026
PMONTHS = [(2024, m) for m in range(1, 13)] + [(2025, m) for m in range(1, 13)] + [(2026, m) for m in range(1, 10)]


def index_day(y, m):
    """The second Tuesday of the month."""
    d = dt.date(y, m, 1)
    first_tue = d + dt.timedelta(days=(1 - d.weekday()) % 7)
    return first_tue + dt.timedelta(days=7)


def _pm(y, m):
    """A published month's position against the parallel year (0 = September 2025)."""
    return (y - 2025) * 12 + (m - 9)


def line_price(L, y, m, rng_back):
    """A transaction line's shelf price in any published month: the parallel year's truth from September 2025, before it
    the line's September 2025 price taken back along its own trend with the retailers' offer calendar."""
    k = _pm(y, m)
    if 0 <= k < W.NM:
        if k < L["start"] or k >= L["end"]:
            return None
        return L["shelf"][k]
    if k >= W.NM:
        return None
    if L["start"] > 0:
        return None
    back = L["back"]
    return back.get((y, m))


def backcast(ls, seed):
    """Prices from January 2024 to August 2025 for lines on sale in September 2025."""
    for L in ls:
        rng = np.random.default_rng([seed, 31, "WGC".index(L["retailer"]), int(L["gtin"]) % 2147483647, W.NUDGE.get(L["item"], 0)])
        if L["start"] > 0:
            L["back"] = {}
            continue
        p_sep = L["reg"][0]
        tr = L["trend"]
        phase = int(L["gtin"]) % 6            # the line's own review months, two a year
        back = {}
        for (y, m) in PMONTHS:
            k = _pm(y, m)
            if k >= 0:
                break
            steps = sum(1 for r in range(k + 1, 1) if (r + phase) % 6 == 0)
            reg = S.price_point(p_sep / (1 + tr) ** (steps * 0.5))
            offer = m not in (8, 9, 10) and rng.random() < L["rate"] * 0.9
            back[(y, m)] = S.price_point(reg * (1 - rng.uniform(*L["depth"]))) if offer else reg
        L["back"] = back
    return ls


def field_sample(ls, seed):
    """The field basket: for each item eight product lines chosen in 2019, mostly branded lines stocked by the chains,
    each priced at the chains' outlets that stock it, with an own-label line at each chain for two of the eight."""
    sample = []
    for code in W.ICODE:
        rng = np.random.default_rng([seed, 37, int(code), W.NUDGE.get(code, 0)])
        cands = [L for L in ls if L["item"] == code and not L["own"] and L["start"] == 0 and L["end"] == W.NM]
        by_gtin = {}
        for L in cands:
            by_gtin.setdefault(L["gtin"], []).append(L)
        shared = sorted(by_gtin, key=lambda g: (-len(by_gtin[g]), g))
        picks = shared[:6]
        for j, g in enumerate(picks):
            sample.append({"item": code, "pcode": "%s-%02d" % (code, j + 1), "gtin": g, "own": False,
                           "lines": {L["retailer"]: L for L in by_gtin[g]}, "desc": by_gtin[g][0]["desc"]})
        for j in range(2):
            own = {}
            for r in W.RETAILERS:
                c = [L for L in ls if L["item"] == code and L["own"] and L["retailer"] == r and L["start"] == 0
                     and L["end"] == W.NM]
                if c:
                    own[r] = c[int(rng.integers(0, len(c)))]
            sample.append({"item": code, "pcode": "%s-%02d" % (code, 7 + j), "gtin": None, "own": True, "lines": own,
                           "desc": "Own label " + own[W.RETAILERS[0]]["desc"].split(" ", 1)[1]})
    return sample


def independent_price(rng_state, base, tr, y, m, rate, depth, phase=0):
    k = _pm(y, m)
    reg = S.price_point(base * (1 + tr) ** (np.floor((k + 20 + phase) / 6) * 0.5))
    u = rng_state.random()
    return S.price_point(reg * (1 - rng_state.uniform(*depth))) if (m not in (8, 9, 10) and u < rate * 0.5) else reg


def quotes(ls, seed):
    """Every field quote, January 2024 to September 2026: outlet, product, month, price and status."""
    ls = backcast(ls, seed)
    sample = field_sample(ls, seed)
    rows = []
    for sp in sample:
        code = sp["item"]
        rng = np.random.default_rng([seed, 41, int(code), int(sp["pcode"][-2:]), W.NUDGE.get(code, 0)])
        any_line = next(iter(sp["lines"].values()))
        ind_base = any_line["reg"][0] * float(np.exp(rng.normal(0.12, 0.06)))
        ind_tr = any_line["trend"] + float(rng.normal(0, 0.008))
        for oc, oname, r, parish, o_from, o_to, repl, in_index in OUTLETS:
            if r is not None and r not in sp["lines"]:
                continue
            if r is None and (sp["own"] or rng.random() < 0.35):
                continue
            ind_rng = np.random.default_rng(seed + 43 + int(oc) * 97 + int(sp["pcode"][-2:]) * 7 + int(code))
            last = None
            for (y, m) in PMONTHS:
                ym = "%04d-%02d" % (y, m)
                if ym < o_from or (o_to and ym > o_to):
                    continue
                if r is not None:
                    p = line_price(sp["lines"][r], y, m, None)
                else:
                    p = independent_price(ind_rng, ind_base, ind_tr, y, m, any_line["rate"], any_line["depth"],
                                          (int(oc) + int(sp["pcode"][-2:])) % 6)
                if p is None:
                    continue
                status = "C"
                if last is not None and rng.random() < 0.025:
                    p, status = last, "T"
                last = p
                day = index_day(y, m) + dt.timedelta(days=int(rng.integers(0, 3)))
                rows.append({"month": ym, "item": code, "outlet": oc, "pcode": sp["pcode"], "desc": sp["desc"],
                             "price": p, "status": status, "collected": day.isoformat(), "in_index": in_index})
    return rows, sample


def published_index(qrows):
    """Each item's published index, January 2024 = the item's 2024 level, from the in-index quotes: the geometric mean of
    price relatives to January within each year, linked through December to January."""
    from collections import defaultdict
    px = defaultdict(dict)
    for q in qrows:
        if q["in_index"] != "Y":
            continue
        key = q["outlet"] if q["outlet"] != "238" else "214"     # the relocated outlet's quotes continue
        px[(q["item"], key, q["pcode"])][q["month"]] = q["price"]
    out = {}
    for code in W.ICODE:
        keys = [k for k in px if k[0] == code]
        lvl = {}
        level = 100.0
        months = ["%04d-%02d" % ym for ym in PMONTHS]
        for i, mo in enumerate(months):
            y = int(mo[:4])
            base = "%04d-01" % y
            if mo == base:
                if i > 0:
                    prev = months[i - 1]
                    rel = [np.log(px[k][mo] / px[k][prev]) for k in keys if mo in px[k] and prev in px[k]]
                    level = lvl[prev] * float(np.exp(np.mean(rel)))
                lvl[mo] = level
                jan_level = level
            else:
                rel = [np.log(px[k][mo] / px[k][base]) for k in keys if mo in px[k] and base in px[k]]
                lvl[mo] = jan_level * float(np.exp(np.mean(rel)))
        out[code] = lvl
    return out
