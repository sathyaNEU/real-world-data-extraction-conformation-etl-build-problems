"""The world of task482 (architecture 4): the Brannagh Statistics Office's residential property price index for
sixteen local authority areas, read by the Minister for Housing against the 8 per cent line for designating rapid
price growth areas for 2027.

A dwelling's log price is its area's level on the sale day, its electoral division's premium, its type's, a floor
area elasticity and a new-dwelling premium, with noise. Each area's price level moves at one steady rate across the
two index years (October 2024 to September 2025, October 2025 to September 2026), so the change for an unchanged
dwelling is the same everywhere in the area. What moves between the years is which dwellings sell: in some areas the
second year sells far more second-hand homes in the cheaper or the dearer electoral divisions, or a run of large new
homes, or more apartments.

    x = build()    the truth: areas, electoral divisions, dwellings, sales"""
import datetime as dt

import numpy as np

SEED = 4824
LINE = 8.0
Y1 = (dt.date(2024, 10, 1), dt.date(2025, 9, 30))
Y2 = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))
EXTRACT = dt.date(2026, 10, 15)
VAT = 0.135
TYPES = ["detached", "semi-detached", "terraced", "apartment"]
TEFF = {"detached": 0.22, "semi-detached": 0.06, "terraced": 0.0, "apartment": -0.04}
TFLOOR = {"detached": 152.0, "semi-detached": 112.0, "terraced": 91.0, "apartment": 68.0}
TMIX = [0.27, 0.31, 0.22, 0.20]
ELAST = 0.80
NEWP = 0.10
NOISE = 0.14

# area code, name, second-hand sales a year, log level, annual growth (per cent), electoral divisions, place, knobs:
#   tilt  the second year's lean of second-hand sales toward the dearer (+) or cheaper (-) electoral divisions
#   new   the share of the second year's sales that are new dwellings (the first year's is 4 per cent), built in the
#         divisions at rank `where` (0 the cheapest)
#   apt   the second year's lean toward apartments (log odds)
# place: "o" over the line on the golden and on every summary of what sold; "u" under on all; "c" over on the golden,
# under on every summary (sales leaning cheap); "d" under on the golden, over on every summary (leaning dear); "n"
# under on the golden and on the regression without location, over on the summaries (new homes); "a" over on the
# golden, under on the median, over per square metre (apartments)
AREAS = [
    ("KB", "Kilbrannagh", 3100, 12.72, 11.6, 10, "o", dict(tilt=0.0, new=0.05, where=4, apt=0.0)),
    ("AC", "Ardcullen", 2400, 12.55, 10.3, 9, "c", dict(tilt=-0.26, new=0.04, where=3, apt=0.0)),
    ("LF", "Lisnafeen", 1900, 12.41, 4.2, 8, "u", dict(tilt=0.0, new=0.04, where=3, apt=0.0)),
    ("RG", "Rathgowan", 2700, 12.63, 5.9, 9, "d", dict(tilt=0.26, new=0.04, where=3, apt=0.0)),
    ("TV", "Tullyvane", 1600, 12.30, 3.1, 8, "u", dict(tilt=0.0, new=0.05, where=3, apt=0.0)),
    ("MR", "Moyrath", 2200, 12.48, 5.8, 9, "n", dict(tilt=0.0, new=0.21, where=6, apt=0.0)),
    ("GS", "Glenaskin", 1800, 12.37, 12.8, 8, "o", dict(tilt=0.0, new=0.05, where=3, apt=0.0)),
    ("DM", "Dunmarra", 2900, 12.69, 10.2, 10, "c", dict(tilt=-0.25, new=0.04, where=4, apt=0.0)),
    ("CT", "Clonteevan", 1500, 12.26, 6.1, 8, "u", dict(tilt=0.0, new=0.04, where=3, apt=0.0)),
    ("IR", "Innishrue", 2000, 12.44, 5.9, 9, "n", dict(tilt=0.0, new=0.20, where=6, apt=0.0)),
    ("CV", "Carrigvore", 2600, 12.60, 10.4, 9, "a", dict(tilt=0.0, new=0.04, where=4, apt=0.50)),
    ("KF", "Knockfeerin", 1700, 12.33, 2.4, 8, "u", dict(tilt=0.0, new=0.04, where=3, apt=0.0)),
    ("BM", "Ballymarne", 2300, 12.52, 6.0, 9, "d", dict(tilt=0.25, new=0.04, where=4, apt=0.0)),
    ("CL", "Corlespie", 1400, 12.22, 3.8, 8, "u", dict(tilt=0.0, new=0.04, where=3, apt=0.0)),
    ("AV", "Annaghvale", 2100, 12.46, 12.1, 9, "o", dict(tilt=0.0, new=0.05, where=4, apt=0.0)),
    ("DS", "Drumshallon", 1900, 12.39, 6.4, 8, "u", dict(tilt=0.0, new=0.05, where=3, apt=0.0)),
]
CODES = [a[0] for a in AREAS]
NAMES = {a[0]: a[1] for a in AREAS}
ED_WORDS = ["North", "South", "East", "West", "Urban", "Rural", "Upper", "Lower", "Central", "Bridge", "Mill", "Hill"]


def days(a, b):
    return [a + dt.timedelta(days=k) for k in range((b - a).days + 1)]


def _level(area, d, g):
    """The area's log price level on day d: a steady rate through the two years, centred on 1 October 2025."""
    t = (d - Y2[0]).days / 365.25
    return area + np.log1p(g / 100.0) * t


def _sales(rng, code, n, lvl, g, eds, kn, year):
    """One year's sales in one area: second-hand dwellings drawn from the stock (with the year's lean) and new ones."""
    lo, hi = Y1 if year == 1 else Y2
    dd = [d for d in days(lo, hi) if d.weekday() < 5]
    ne = len(eds)
    order = np.argsort([e["eff"] for e in eds])
    rank = np.empty(ne)
    rank[order] = np.linspace(-1, 1, ne)
    tilt = kn["tilt"] if year == 2 else 0.0
    w_ed = np.exp(tilt * 1.6 * rank) * np.array([e["size"] for e in eds])
    w_ed = w_ed / w_ed.sum()
    apt = kn["apt"] if year == 2 else 0.0
    w_t = np.array(TMIX) * np.exp([0, 0, 0, apt])
    w_t = w_t / w_t.sum()
    share_new = kn["new"] if year == 2 else 0.04
    n_new = int(round(n * share_new / (1 - share_new)))
    out = []
    for i in range(n + n_new):
        new = i >= n
        if new:
            e = int(order[min(ne - 1, kn["where"] + int(rng.integers(0, 2)))])
            t = TYPES[int(rng.choice(4, p=[0.38, 0.44, 0.12, 0.06]))]
            fl = TFLOOR[t] * 1.18 * float(np.exp(rng.normal(0, 0.10)))
            built = (2025 if year == 1 else 2026) - int(rng.integers(0, 2))
        else:
            e = int(rng.choice(ne, p=w_ed))
            t = TYPES[int(rng.choice(4, p=w_t))]
            fl = TFLOOR[t] * float(np.exp(rng.normal(0, 0.17)))
            built = int(rng.choice([1965, 1975, 1985, 1995, 2002, 2006, 2012, 2018])) + int(rng.integers(0, 6))
        d = dd[int(rng.integers(0, len(dd)))]
        lp = (_level(lvl, d, g) + eds[e]["eff"] + TEFF[t] + ELAST * np.log(fl / 100.0) + (NEWP if new else 0.0)
              + float(rng.normal(0, NOISE)))
        price = float(np.exp(lp))
        price = round(price / 500.0) * 500.0 if price < 1e6 else round(price / 5000.0) * 5000.0
        out.append({"area": code, "ed": eds[e]["code"], "type": t, "floor": round(fl, 1), "new": new,
                    "built": built, "date": d, "price": price, "market": True, "bulk": None})
    return out


def _estimates(sales):
    """The routes on the truth (VAT-inclusive prices, market sales): the median change, the median per square metre,
    the type change weighted by the first year's mix, the regression without location, and the full regression."""
    y = np.array([s["date"] >= Y2[0] for s in sales])
    p = np.array([s["price"] for s in sales])
    fl = np.array([s["floor"] for s in sales])
    lp = np.log(p)
    out = {"median": 100 * (np.median(p[y]) / np.median(p[~y]) - 1),
           "per_m2": 100 * (np.median((p / fl)[y]) / np.median((p / fl)[~y]) - 1)}
    tt = np.array([s["type"] for s in sales])
    acc = 0.0
    for t in TYPES:
        m = tt == t
        acc += (m & ~y).sum() / (~y).sum() * (np.median(p[m & y]) / np.median(p[m & ~y]) - 1)
    out["type_weighted"] = 100 * acc

    def reg(location):
        cols = [np.ones(len(sales)), y.astype(float), np.log(fl / 100.0), np.array([s["new"] for s in sales], float)]
        cols += [(tt == t).astype(float) for t in TYPES[1:]]
        if location:
            eds = sorted(set(s["ed"] for s in sales))
            ee = np.array([s["ed"] for s in sales])
            cols += [(ee == e).astype(float) for e in eds[1:]]
        b = np.linalg.lstsq(np.column_stack(cols), lp, rcond=None)[0]
        return 100 * (np.exp(b[1]) - 1)
    out["hedonic_no_location"] = reg(False)
    out["hedonic"] = reg(True)
    return out


def placed(place, e):
    over = {k: v > LINE + 1.0 for k, v in e.items()}
    under = {k: v < LINE - 1.0 for k, v in e.items()}
    clear = abs(e["hedonic"] - LINE) >= 1.5
    summ = ("median", "per_m2", "type_weighted")
    return clear and {
        "o": all(over.values()),
        "u": all(under.values()),
        "c": over["hedonic"] and all(under[k] for k in summ) and under["hedonic_no_location"],
        "d": under["hedonic"] and all(over[k] for k in summ) and over["hedonic_no_location"],
        "n": under["hedonic"] and under["hedonic_no_location"] and all(over[k] for k in summ),
        "a": over["hedonic"] and under["median"] and over["per_m2"] and over["hedonic_no_location"],
    }[place]


def build():
    rng = np.random.default_rng(SEED)
    x = {"areas": [], "eds": [], "sales": [], "est": {}}
    for code, name, n, lvl, g, ne, place, kn in AREAS:
        for tries in range(200):
            words = list(rng.permutation(ED_WORDS))[:ne]
            eff = rng.normal(0, 0.24, ne)
            eff -= eff.mean()
            eds = [{"code": "%s%03d" % (code, 11 + 7 * k), "name": "%s %s" % (name, words[k]), "area": code,
                    "eff": float(eff[k]), "size": float(rng.uniform(0.6, 1.6))} for k in range(ne)]
            sub = _sales(rng, code, n, lvl, g, eds, kn, 1) + _sales(rng, code, n, lvl, g, eds, kn, 2)
            e = _estimates(sub)
            if placed(place, e):
                break
        else:
            raise SystemExit("area %s not placed" % code)
        x["areas"].append({"code": code, "name": name, "growth": g, "place": place, "n": n, "level": lvl})
        x["eds"] += eds
        x["sales"] += sub
        x["est"][code] = e
    _non_market(rng, x)
    return x


def _non_market(rng, x):
    """Sales not at full market price (family transfers, part-interest sales) in every area, and housing bodies'
    purchases of whole blocks of new apartments, the block's one consideration on each apartment's line."""
    eds_by_area = {}
    for e in x["eds"]:
        eds_by_area.setdefault(e["area"], []).append(e)
    extra = []
    for a in x["areas"]:
        eds = eds_by_area[a["code"]]
        for year, (lo, hi) in ((1, Y1), (2, Y2)):
            dd = [d for d in days(lo, hi) if d.weekday() < 5]
            for _ in range(int(a["n"] * 0.035)):
                e = eds[int(rng.integers(0, len(eds)))]
                t = TYPES[int(rng.choice(4, p=TMIX))]
                fl = TFLOOR[t] * float(np.exp(rng.normal(0, 0.17)))
                d = dd[int(rng.integers(0, len(dd)))]
                lp = _level(a["level"], d, a["growth"]) + e["eff"] + TEFF[t] + ELAST * np.log(fl / 100.0)
                price = round(float(np.exp(lp)) * float(rng.uniform(0.35, 0.8)) / 500.0) * 500.0
                extra.append({"area": a["code"], "ed": e["code"], "type": t, "floor": round(fl, 1), "new": False,
                              "built": 1990, "date": d, "price": price, "market": False, "bulk": None})
    # housing bodies' purchases of whole blocks of new apartments, one consideration for each block
    k = 0
    for a in x["areas"]:
        eds = sorted(eds_by_area[a["code"]], key=lambda e: e["eff"])
        for j, (year, (lo, hi)) in enumerate(((1, Y1), (2, Y2), (2, Y2), (2, Y2))):
            if j > 1 and rng.random() < 0.5:
                continue
            if year == 1 and rng.random() < 0.6:
                continue
            units = int(rng.integers(4, 21))
            e = eds[int(rng.integers(1, len(eds) - 1))]
            dd = [d for d in days(lo, hi) if d.weekday() < 5]
            d = dd[int(rng.integers(0, len(dd) - 30))]
            unit = []
            for u in range(units):
                fl = round(TFLOOR["apartment"] * float(np.exp(rng.normal(0, 0.08))), 1)
                lp = _level(a["level"], d, a["growth"]) + e["eff"] + TEFF["apartment"] + ELAST * np.log(fl / 100.0) + NEWP
                unit.append((fl, float(np.exp(lp)) * 0.88))
            total = round(sum(v for _, v in unit) / 1000.0) * 1000.0
            for fl, _ in unit:
                extra.append({"area": a["code"], "ed": e["code"], "type": "apartment", "floor": fl, "new": True,
                              "built": d.year, "date": d, "price": total, "market": False, "bulk": (k, units)})
            k += 1
    x["sales"] += extra
