"""The coverage files: each supermarket's 2025 annual return of retail sales by its own product categories (Wrenfold's
in the category codes of its 2025 hierarchy, Gorsedale's with its trade sales to cafes and guest houses alongside its
retail sales, Calderby's net of GST), the office's map of the retailers' categories to RPI items built from the 2024
returns, and the office's estimate of households' 2025 spending on each item."""
import numpy as np

import world as W

# Wrenfold's categories: (2024 code, 2025 code, name, RPI item); its 2025 hierarchy put the grocery categories in a new
# order and moved toiletries to a personal care department, so every code the 2024 map holds now names another category
WREN_CATS = [
    ("G110", "G135", "Bread and rolls", "1101"), ("G115", "G140", "Breakfast cereals and porridge", "1103"),
    ("G120", "G145", "Pasta, rice and noodles", "1105"), ("G125", "G150", "Biscuits", "1108"),
    ("G130", "G155", "Yoghurts", "1145"), ("G135", "G160", "Cheese", "1146"), ("G140", "G165", "Butter and spreads", "1151"),
    ("G145", "G170", "Confectionery", "1182"), ("G150", "G110", "Coffee", "1211"), ("G155", "G115", "Tea", "1212"),
    ("G160", "G120", "Soft drinks", "1221"), ("G165", "G125", "Water", "1222"), ("G170", "G130", "Juices", "1223"),
    ("H210", "H215", "Laundry", "5611"), ("H215", "H210", "Toilet and kitchen rolls", "5613"),
    ("H310", "P310", "Toiletries", "6213"),
]
WREN_OTHER = [("G175", "G175", "Cakes and bakery snacks", "1109"), ("G180", "G180", "Crisps and snacks", "1191"),
              ("H220", "H220", "Dishwashing", "5612"), ("H320", "H320", "Cosmetics", "6214"),
              ("F410", "F410", "Fresh fruit and vegetables", "1171"), ("F420", "F420", "Fresh meat and fish", "1121")]
GORS_CATS = [("BAK", "Bakery", "1101"), ("CER", "Cereals", "1103"), ("DRY", "Pasta and rice", "1105"),
             ("BIS", "Biscuits", "1108"), ("YOG", "Yoghurt", "1145"), ("CHE", "Cheese", "1146"), ("BUT", "Butter and fats", "1151"),
             ("CON", "Confectionery", "1182"), ("COF", "Coffee", "1211"), ("TEA", "Tea", "1212"), ("SDR", "Soft drinks", "1221"),
             ("WAT", "Water", "1222"), ("JUI", "Juice", "1223"), ("LAU", "Laundry", "5611"), ("PAP", "Paper", "5613"),
             ("TOI", "Toiletries", "6213"), ("FRE", "Fresh produce", "1171"), ("SNK", "Snacks", "1191")]
CALD_CATS = [("101", "Bread", "1101"), ("102", "Cereal", "1103"), ("103", "Pasta & rice", "1105"), ("104", "Biscuits", "1108"),
             ("111", "Yogurt", "1145"), ("112", "Cheese", "1146"), ("113", "Butter & spreads", "1151"),
             ("121", "Sweets & chocolate", "1182"), ("131", "Coffee", "1211"), ("132", "Tea", "1212"),
             ("133", "Soft drinks", "1221"), ("134", "Water", "1222"), ("135", "Juice", "1223"), ("201", "Laundry", "5611"),
             ("202", "Paper products", "5613"), ("301", "Health & beauty", "6213"), ("141", "Fresh produce", "1171"),
             ("142", "Snacks", "1191")]
SHARE = {"W": 0.44, "G": 0.31, "C": 0.25}       # the supermarkets' shares of their combined grocery sales


def build(seed, offset=None):
    """The 2025 sales by retailer and item (with GST), the households' spending by item, and each return's rows."""
    rng = np.random.default_rng([seed, 201, W.COVER_OFFSET if offset is None else offset])
    spend, sales, true_cov = {}, {}, {}
    for code, name, *_ in W.ITEMS:
        hh = float(np.exp(rng.normal(np.log(9500), 0.30)))           # thousand pounds a year
        cov = float(rng.uniform(0.55, 0.80))
        tot = hh * cov
        mix = np.array([SHARE[r] for r in W.RETAILERS]) * np.exp(rng.normal(0, [0.35, 0.15, 0.15]))
        mix /= mix.sum()
        for r, s in zip(W.RETAILERS, mix):
            sales[(r, code)] = tot * s * 1000.0                         # pounds with GST
        spend[code] = round(hh, 0)
        true_cov[code] = None
    other = {}
    for code in ("1109", "1191", "5612", "6214", "1171", "1121"):
        for r in W.RETAILERS:
            other[(r, code)] = float(np.exp(rng.normal(np.log(2.2e6), 0.5))) * (3.6 if code in ("1171", "1121") else 1.0)
    # Gorsedale's trade sales (cafes, guest houses) in a few categories, beside its retail sales
    trade = {}
    for code in ("1101", "1146", "1151", "1211", "1212", "1221", "1222", "1223", "5613"):
        trade[code] = float(sales[("G", code)] * rng.uniform(0.10, 0.22))
    wren = [[c25, nm, round(sales[("W", it)], 2)] for c24, c25, nm, it in WREN_CATS]
    wren += [[c25, nm, round(other[("W", it)], 2)] for c24, c25, nm, it in WREN_OTHER]
    wren.sort(key=lambda r: r[0])
    gors = []
    for code, nm, it in GORS_CATS:
        val = sales[("G", it)] if it in W.INAME else other[("G", it)]
        gors.append(["Retail", code, nm, round(val, 2)])
        if it in trade:
            gors.append(["Trade", code, nm, round(trade[it], 2)])
    cald = []
    for code, nm, it in CALD_CATS:
        val = sales[("C", it)] if it in W.INAME else other[("C", it)]
        cald.append([code, nm, round(val / (1 + W.GST), 2)])
    cmap = [["Wrenfold Stores", c24, nm, it] for c24, c25, nm, it in WREN_CATS + WREN_OTHER]
    cmap += [["Gorsedale Co-operative", c, nm, it] for c, nm, it in GORS_CATS]
    cmap += [["Calderby's", c, nm, it] for c, nm, it in CALD_CATS]
    for code in W.ICODE:
        true_cov[code] = sum(sales[(r, code)] for r in W.RETAILERS) / 1000.0 / spend[code]
    return {"spend": spend, "sales": sales, "trade": trade, "wren": wren, "gors": gors, "cald": cald, "map": cmap,
            "coverage": true_cov}
