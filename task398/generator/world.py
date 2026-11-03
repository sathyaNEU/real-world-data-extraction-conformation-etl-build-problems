"""The clean truth for task398: the Thornbury Managed Risk UK Equity Fund's accounting year to 30 September 2026.

Everything here is computed forward from seeded draws and hand-set market segments; nothing is fixed first and
reverse-engineered. The pack writer (pack.py) reads this state and applies the producing systems' own conventions.
"""
import datetime as dt
import math
import zlib

import numpy as np

SEED = 398
D = dt.date

YEAR_START = D(2025, 10, 1)      # first valuation point of the accounting year
YEAR_BASE = D(2025, 9, 30)       # the valuation point the year's return is measured from
YEAR_END = D(2026, 9, 30)
HIST_START = D(2025, 6, 2)       # the administrator's price history starts here (63-day window cover)
EXTRACT_END = D(2026, 10, 16)    # custody extracts run past the year end
CUSTODY_SWITCH = D(2026, 4, 1)   # Northcote takes custody from this valuation point
RECLASS_DATE = D(2026, 6, 22)    # Larkspur's annual industry review takes effect

DD_IN, DD_OUT, DEFENSIVE, WINDOW = 0.08, 0.04, 0.40, 63
TARGET_V, TARGET_G, TARGET_C = 0.47, 0.47, 0.06
FEE_B, FEE_C = 0.0085, 0.0060
SDRT = 0.005


def rng(stream):
    return np.random.default_rng([SEED, zlib.crc32(stream.encode())])


# ----------------------------------------------------------------------------------------------------------
# calendar
BANK_HOLIDAYS = {D(2025, 8, 25), D(2025, 12, 25), D(2025, 12, 26), D(2026, 1, 1), D(2026, 4, 3), D(2026, 4, 6),
                 D(2026, 5, 4), D(2026, 5, 25), D(2026, 8, 31), D(2026, 12, 25), D(2026, 12, 28)}


def dealing_days(a, b):
    out, d = [], a
    while d <= b:
        if d.weekday() < 5 and d not in BANK_HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


DAYS = dealing_days(HIST_START, EXTRACT_END)
IDX = {d: i for i, d in enumerate(DAYS)}


def add_bd(d, n):
    """n business days after d (n >= 0)."""
    i = IDX[d] + n
    return DAYS[i]


def quarter_of(d):
    if d <= D(2025, 12, 31):
        return "Q1"
    if d <= D(2026, 3, 31):
        return "Q2"
    if d <= D(2026, 6, 30):
        return "Q3"
    return "Q4"


QUARTER_ENDS = [D(2025, 12, 31), D(2026, 3, 31), D(2026, 6, 30), D(2026, 9, 30)]


def uk_offset_hours(d):
    """BST is UTC+1 from the last Sunday of March to the last Sunday of October."""
    def last_sunday(y, m):
        x = D(y, m, 31)
        while x.weekday() != 6:
            x -= dt.timedelta(days=1)
        return x
    return 1 if last_sunday(d.year, 3) <= d < last_sunday(d.year, 10) else 0


# ----------------------------------------------------------------------------------------------------------
# identifiers
def sedol_check(s6):
    w = [1, 3, 1, 7, 3, 9]
    tot = 0
    for ch, wt in zip(s6, w):
        v = int(ch) if ch.isdigit() else ord(ch) - 55
        tot += v * wt
    return str((10 - tot % 10) % 10)


def isin_check(body):
    digits = "".join(str(int(c)) if c.isdigit() else str(ord(c) - 55) for c in body)
    tot, dbl = 0, True
    for ch in reversed(digits):
        v = int(ch) * (2 if dbl else 1)
        tot += v // 10 + v % 10
        dbl = not dbl
    return str((10 - tot % 10) % 10)


def make_sedol(r):
    alpha = "BCDFGHJKLMNPQRSTVWXYZ"
    if r.random() < 0.6:
        s6 = "B" + "".join(r.choice(list("0123456789" + alpha)) for _ in range(5))
    else:
        s6 = "".join(r.choice(list("0123456789")) for _ in range(6))
    return s6 + sedol_check(s6)


def isin_of(sedol):
    body = "GB00" + sedol
    return body + isin_check(body)


# ----------------------------------------------------------------------------------------------------------
# securities
INDUSTRIES = ["Financials", "Real Estate", "Energy", "Basic Materials", "Industrials", "Consumer Discretionary",
              "Consumer Staples", "Health Care", "Technology", "Telecommunications", "Utilities"]
LIC = {"Technology": "10", "Telecommunications": "15", "Health Care": "20", "Financials": "30",
       "Real Estate": "35", "Consumer Discretionary": "40", "Consumer Staples": "45", "Industrials": "50",
       "Basic Materials": "55", "Energy": "60", "Utilities": "65"}

ROOTS = ["Halworth", "Corbin", "Ashdale", "Brennock", "Carrick", "Dunmore", "Elstow", "Fenwick", "Garron",
         "Harlow", "Ingleby", "Kelso", "Lanyon", "Marston", "Netherby", "Orwell", "Pendle", "Quarry Hill",
         "Redmire", "Selby", "Tamar", "Ulverston", "Vallance", "Wenlock", "Yarrow", "Alderley", "Bramhope",
         "Calder", "Dalston", "Eskdale", "Fulbeck", "Glaisdale", "Hepworth", "Ilkley", "Kirkham", "Lindley",
         "Malham", "Norland", "Oakworth", "Pateley", "Rastrick", "Settle", "Thorner", "Upton", "Wetherby",
         "Arkholme", "Burnsall", "Cononley", "Dacre", "Embsay", "Farnhill", "Gargrave", "Hebden", "Kildwick",
         "Langbar", "Mickley", "Newsome", "Ovenden", "Pannal", "Ripley", "Scargill", "Tockwith", "Wath",
         "Addingham", "Bardsey", "Collingham", "Darley", "Eldwick", "Felliscliffe", "Grewelthorpe", "Hampsthwaite",
         "Kearby", "Leathley", "Menston", "Nidd", "Otley", "Pool", "Rufforth", "Spofforth", "Timble", "Weeton",
         "Aberford", "Barwick", "Clifford", "Drax", "Escrick", "Fangfoss", "Goole", "Hemingbrough", "Kexby",
         "Linton", "Moortown", "Naburn", "Osgodby", "Riccall", "Stillingfleet", "Thorganby", "Wheldrake", "Acaster",
         "Bilbrough", "Cawood", "Dunnington", "Elvington", "Fulford", "Heslington", "Kelfield", "Long Marston",
         "Murton", "Nether Poppleton", "Osbaldwick", "Rawcliffe", "Skelton", "Towthorpe", "Upper Poppleton",
         "Wigginton", "Askham", "Bishopthorpe", "Copmanthorpe", "Deighton", "Earswick", "Flaxton", "Haxby",
         "Huntington", "Knapton", "Langwith", "Moor Monkton", "Nunthorpe", "Overton", "Ryther", "Shipton",
         "Tadcaster", "Ulleskelf", "Walmgate", "Bolton Percy", "Crockey Hill", "Dringhouses", "Grimston",
         "Holtby", "Kirk Hammerton", "Lingcroft", "Middlethorpe", "Newton Kyme", "Poppleton", "Scagglethorpe",
         "Sutton", "Thornthwaite", "Warthill", "Appleton", "Bickerton", "Catterton", "Dunsforth", "Fewston",
         "Great Ouseburn", "Hunsingore", "Kirby Hill", "Lower Dunsforth", "Marton", "Nun Monkton", "Ouston",
         "Roecliffe", "Staveley", "Thorpe Underwood", "Whixley", "Allerton", "Boroughbridge", "Cattal", "Dishforth",
         "Ferrensby", "Goldsborough", "Hopperton", "Knaresborough", "Little Ribston", "Minskip", "Nidderdale",
         "Occaney", "Plompton", "Scotton", "Tentergate", "Walshford", "Arkendale", "Brearton", "Coneythorpe",
         "Farnham", "Flaxby", "Hilton", "Lofthouse", "Markington", "Ouseburn", "Rossett", "Starbeck", "Thruscross"]

SUFFIX = {
    "Financials": ["Bank", "Building Society Holdings", "Insurance", "Capital", "Assurance", "Investment Trust",
                   "Asset Management", "Wealth", "Insurance Brokers", "Finance"],
    "Real Estate": ["Estates", "Property Trust", "Land", "REIT", "Housing REIT", "Properties"],
    "Energy": ["Energy", "Oil & Gas", "Petroleum", "Resources"],
    "Basic Materials": ["Mining", "Chemicals", "Metals", "Minerals", "Paper"],
    "Industrials": ["Engineering", "Group", "Industries", "Holdings", "Logistics", "Aerospace", "Payments",
                    "Support Services", "Construction"],
    "Consumer Discretionary": ["Retail", "Leisure", "Homes", "Hotels", "Brands", "Motor Group", "Media"],
    "Consumer Staples": ["Foods", "Brewery", "Distillers", "Grocers", "Tobacco"],
    "Health Care": ["Healthcare", "Pharmaceuticals", "Medical", "Diagnostics", "Life Sciences"],
    "Technology": ["Software", "Technology", "Systems", "Data", "Semiconductors", "Digital"],
    "Telecommunications": ["Telecom", "Networks", "Communications"],
    "Utilities": ["Water", "Power", "Utilities", "Energy Networks"],
}

# value sleeve industry mix (weights) and growth sleeve industry mix
VALUE_MIX = {"Financials": 0.30, "Energy": 0.12, "Basic Materials": 0.10, "Utilities": 0.08,
             "Consumer Staples": 0.08, "Industrials": 0.10, "Real Estate": 0.06, "Telecommunications": 0.06,
             "Health Care": 0.05, "Consumer Discretionary": 0.05}
GROWTH_MIX = {"Technology": 0.20, "Health Care": 0.16, "Industrials": 0.20, "Consumer Discretionary": 0.18,
              "Financials": 0.12, "Consumer Staples": 0.06, "Real Estate": 0.04, "Telecommunications": 0.04}


def securities():
    """The index universe (Main Market constituents) plus the growth sleeve's AIM holdings."""
    r = rng("securities")
    names_used, seds_used, tick_used = set(), set(), set()
    out = []

    def new_sec(industry, market="Main Market", suffix=None):
        while True:
            root = ROOTS[int(r.integers(len(ROOTS)))]
            suf = suffix or SUFFIX[industry][int(r.integers(len(SUFFIX[industry])))]
            style = r.random()
            if style < 0.08 and " " not in root:
                name = f"{root} & {ROOTS[int(r.integers(len(ROOTS)))].split()[0]} {suf}"
            else:
                name = f"{root} {suf}"
            name = name + (" plc" if r.random() < 0.93 else " Limited")
            if name not in names_used:
                break
        names_used.add(name)
        while True:
            sed = make_sedol(r)
            if sed not in seds_used:
                break
        seds_used.add(sed)
        while True:
            base = "".join(ch for ch in root.upper() if ch.isalpha())
            if r.random() < 0.5:
                t = base[:3]
            else:
                t = base[:2] + "ABCDEFGHJKLMNPRSTUVWXY"[int(r.integers(22))]
            if r.random() < 0.2:
                t = t + "ABCDEFGHJKLMNPRSTUVWXY"[int(r.integers(22))]
            if t not in tick_used:
                break
        tick_used.add(t)
        return dict(name=name, sedol=sed, isin=isin_of(sed), tidm=t, industry=industry, market=market)

    # index universe: 520 Main Market constituents
    ind_weights = {"Financials": 0.22, "Industrials": 0.17, "Consumer Discretionary": 0.13, "Real Estate": 0.07,
                   "Technology": 0.06, "Health Care": 0.06, "Consumer Staples": 0.07, "Basic Materials": 0.07,
                   "Energy": 0.05, "Telecommunications": 0.04, "Utilities": 0.06}
    keys = list(ind_weights)
    p = np.array([ind_weights[k] for k in keys]); p = p / p.sum()
    for _ in range(520):
        ind = keys[int(r.choice(len(keys), p=p))]
        out.append(new_sec(ind))
    # the bank that fails
    penrose = dict(name="Penrose Bank plc", sedol=None, isin=None, tidm="PNRB", industry="Financials",
                   market="Main Market")
    while True:
        s = make_sedol(r)
        if s not in seds_used:
            break
    seds_used.add(s)
    penrose["sedol"] = s; penrose["isin"] = isin_of(s)
    out.append(penrose)
    # AIM growth names (not index constituents)
    for ind in ["Technology"] * 4 + ["Health Care"] * 3 + ["Consumer Discretionary"] * 2 + ["Industrials"]:
        out.append(new_sec(ind, market="AIM"))
    for i, s in enumerate(out):
        s["sid"] = i
    return out


def assign_portfolios(secs):
    """Pick the value and growth sleeves' holdings and the reclassified names."""
    r = rng("portfolios")
    main = [s for s in secs if s["market"] == "Main Market" and s["name"] != "Penrose Bank plc"]
    aim = [s for s in secs if s["market"] == "AIM"]
    penrose = [s for s in secs if s["name"] == "Penrose Bank plc"][0]
    by_ind = {}
    for s in main:
        by_ind.setdefault(s["industry"], []).append(s)
    for k in by_ind:
        by_ind[k] = sorted(by_ind[k], key=lambda s: s["sid"])

    def pick(mix, n, exclude=()):
        chosen = []
        alloc = {k: max(1, int(round(v * n))) for k, v in mix.items()}
        for k, m in alloc.items():
            pool = [s for s in by_ind[k] if s["sid"] not in exclude and s not in chosen]
            idx = r.choice(len(pool), size=min(m, len(pool)), replace=False)
            chosen += [pool[int(i)] for i in sorted(idx)]
        return chosen

    value = pick(VALUE_MIX, 56)
    value.append(penrose)
    vsids = {s["sid"] for s in value}
    growth = pick(GROWTH_MIX, 50, exclude=vsids)
    # four names both managers hold
    overlap = [s for s in value if s["industry"] in ("Industrials", "Health Care", "Consumer Staples")][:4]
    growth += overlap
    growth += aim
    # Larkspur's June 2026 annual industry review: names that move into or out of Financials
    reclass = []
    v_fin = [s for s in value if s["industry"] == "Financials" and s["name"] != "Penrose Bank plc"]
    v_fin = sorted(v_fin, key=lambda s: s["sid"])
    # a housing REIT and an insurance broker in the value sleeve leave Financials
    for s, new in zip(v_fin[:2], ["Real Estate", "Industrials"]):
        reclass.append((s["sid"], s["industry"], new))
    # a payments business in the growth sleeve moves into Financials, a wealth platform leaves it
    g_ind = sorted([s for s in growth if s["industry"] == "Industrials" and s["market"] == "Main Market"
                    and s["sid"] not in vsids], key=lambda s: s["sid"])
    g_fin = sorted([s for s in growth if s["industry"] == "Financials" and s["sid"] not in vsids],
                   key=lambda s: s["sid"])
    reclass.append((g_ind[0]["sid"], "Industrials", "Financials"))
    reclass.append((g_fin[0]["sid"], "Financials", "Technology"))
    # index names outside the fund that also move
    others = [s for s in main if s["sid"] not in vsids and s["sid"] not in {x["sid"] for x in growth}]
    for s in sorted(others, key=lambda s: s["sid"])[3:40:6]:
        new = {"Financials": "Real Estate", "Real Estate": "Financials", "Industrials": "Technology",
               "Technology": "Industrials"}.get(s["industry"], "Industrials")
        if new != s["industry"]:
            reclass.append((s["sid"], s["industry"], new))
    return value, growth, reclass


# ----------------------------------------------------------------------------------------------------------
# market path (noon-to-noon total returns of the benchmark), style and industry factors
MARCH_PATH = {  # hand-set daily benchmark returns, per cent, the run-up and the stress window
    D(2026, 2, 16): 0.18, D(2026, 2, 17): 0.09, D(2026, 2, 18): 0.22, D(2026, 2, 19): -0.11, D(2026, 2, 20): 0.26,
    D(2026, 2, 23): 0.14, D(2026, 2, 24): -0.07, D(2026, 2, 25): 0.19, D(2026, 2, 26): 0.12, D(2026, 2, 27): 0.08,
    D(2026, 3, 2): 0.21, D(2026, 3, 3): 0.33, D(2026, 3, 4): 0.12, D(2026, 3, 5): -0.83, D(2026, 3, 6): -0.61,
    D(2026, 3, 9): -0.42, D(2026, 3, 10): -0.47, D(2026, 3, 11): -0.18, D(2026, 3, 12): 0.29,
    D(2026, 3, 13): -0.63, D(2026, 3, 16): -0.88, D(2026, 3, 17): -0.37, D(2026, 3, 18): 0.21,
    D(2026, 3, 19): -0.71, D(2026, 3, 20): -1.38, D(2026, 3, 23): -0.42, D(2026, 3, 24): -0.18,
    D(2026, 3, 25): 0.51, D(2026, 3, 26): -0.36, D(2026, 3, 27): -0.29, D(2026, 3, 30): 0.19,
    D(2026, 3, 31): 0.27, D(2026, 4, 1): -0.31, D(2026, 4, 2): -0.14, D(2026, 4, 7): 1.12, D(2026, 4, 8): 0.87,
    D(2026, 4, 9): 0.58, D(2026, 4, 10): 0.41}
PENROSE_PATH = {D(2026, 3, 9): -0.24, D(2026, 3, 10): -0.33, D(2026, 3, 11): -0.38, D(2026, 3, 12): -0.28,
                D(2026, 3, 13): -0.22}
PENROSE_SUSPENDED = D(2026, 3, 16)


def segment_drift(d):
    """mean daily benchmark return (per cent) and daily volatility by stretch of the record."""
    if d < D(2025, 10, 1):
        return 0, 0.030, 0.55
    if d < D(2025, 12, 15):
        return 1, 0.040, 0.55
    if d < D(2026, 2, 16):
        return 7, 0.085, 0.40
    if d <= D(2026, 4, 10):
        return 2, 0.0, 0.0
    if d <= D(2026, 6, 30):
        return 3, 0.130, 0.78
    if d <= D(2026, 8, 31):
        return 4, 0.032, 0.62
    if d <= D(2026, 9, 30):
        return 5, -0.020, 0.70
    return 6, 0.02, 0.65


def demeaned(z, seg):
    """noise with its mean removed inside each stretch, so a stretch's drift is the stretch's return"""
    z = z.copy()
    for s in set(seg):
        m = seg == s
        z[m] = z[m] - z[m].mean()
    return z


SEG = np.array([segment_drift(d)[0] for d in DAYS])


def market():
    r = rng("market")
    n = len(DAYS)
    bench = np.zeros(n)
    z = demeaned(r.standard_normal(n), SEG)
    for i, d in enumerate(DAYS):
        if d in MARCH_PATH:
            bench[i] = MARCH_PATH[d] / 100
        else:
            _, m, v = segment_drift(d)
            bench[i] = (m + v * z[i]) / 100
    # value-minus-growth style factor: value lags in the March stress
    rs = rng("style")
    style = 0.0018 * demeaned(rs.standard_normal(n), SEG)
    for i, d in enumerate(DAYS):
        if D(2026, 3, 2) <= d <= D(2026, 3, 31):
            style[i] -= 0.0010
    # financials factor: bank stress in March
    rf = rng("finfactor")
    fin = 0.0035 * demeaned(rf.standard_normal(n), SEG)
    for i, d in enumerate(DAYS):
        if D(2026, 3, 5) <= d <= D(2026, 3, 27):
            fin[i] -= 0.0030
        if D(2026, 4, 7) <= d <= D(2026, 5, 29):
            fin[i] += 0.0006
    # the Larkspur 100 (large caps): close to the benchmark with its own wobble
    r100 = rng("l100")
    l100 = bench + 0.0011 * demeaned(r100.standard_normal(n), SEG)
    # noon-to-close drift within the day for the close series
    rc = rng("closewobble")
    close_extra = 0.0018 * rc.standard_normal(n)
    return dict(bench=bench, style=style, fin=fin, l100=l100, close_extra=close_extra)


ALPHA_V = 0.0000445     # Ashcombe's stock selection outside Penrose, per dealing day
ALPHA_G = -0.00010    # Fennick's stock selection, per dealing day


def opening_weights(value, growth):
    """each sleeve's weights at the start of the record, Penrose five per cent of the value sleeve"""
    out = {}
    for tag, members in (("V", value), ("G", growth)):
        rr = rng("weights" + tag)
        w = rr.dirichlet(np.full(len(members), 3.0))
        sids = [s["sid"] for s in members]
        if tag == "V":
            k = [j for j, s in enumerate(members) if s["name"] == "Penrose Bank plc"][0]
            w = w * (1 - 0.054) / (1 - w[k])
            w[k] = 0.054
        out[tag] = dict(zip(sids, w))
    return out


def stock_returns(secs, value, growth, mk):
    """Daily noon-to-noon price returns (before dividends)."""
    r = rng("stocks")
    wts = opening_weights(value, growth)
    n = len(DAYS)
    vs = {s["sid"] for s in value}
    gs = {s["sid"] for s in growth}
    out = {}
    group = {}
    for s in secs:
        sid = s["sid"]
        group[sid] = "V" if (sid in vs and sid not in gs) else ("G" if (sid in gs and sid not in vs) else "O")
        s["beta"] = float(r.uniform(0.82, 1.18))
        s["tilt"] = float({"V": r.uniform(0.4, 1.2), "G": r.uniform(-1.2, -0.4), "O": r.uniform(-0.8, 0.8)}[group[sid]])
        s["idio"] = float(r.uniform(0.009, 0.018)) * (1.4 if s["market"] == "AIM" else 1.0)
        s["e"] = s["idio"] * r.standard_normal(n)
        if s["name"] == "Penrose Bank plc":
            # a large bank: market-like before its fall, its own noise without drift up to the run on it
            s["beta"], s["tilt"], s["idio"] = 1.06, 0.9, 0.0105
            e = s["idio"] * r.standard_normal(n)
            pre = np.array([d < D(2026, 3, 6) for d in DAYS])
            e[pre] -= e[pre].mean()
            s["e"] = e
    # each sleeve carries a market beta of one at its opening weights and no common idiosyncratic drift
    bysid = {s["sid"]: s for s in secs}
    for gname in ("V", "G"):
        w = {sid: x for sid, x in wts[gname].items() if bysid[sid]["name"] != "Penrose Bank plc"}
        own = [sid for sid in w if group[sid] == gname]
        wo = sum(w[sid] for sid in own)
        mb = sum(w[sid] * bysid[sid]["beta"] for sid in w) / sum(w.values())
        common = sum(w[sid] * bysid[sid]["e"] for sid in own) / wo
        for sid in own:
            bysid[sid]["beta"] += (1.0 - mb) * sum(w.values()) / wo
            bysid[sid]["e"] = bysid[sid]["e"] - common
    for s in secs:
        sid = s["sid"]
        finl = 1.0 if s["industry"] == "Financials" else (0.35 if s["industry"] == "Real Estate" else 0.0)
        alpha = {"V": ALPHA_V, "G": ALPHA_G, "O": 0.0}[group[sid]]
        out[sid] = s["beta"] * mk["bench"] + 0.5 * s["tilt"] * mk["style"] + finl * mk["fin"] + s.pop("e") + alpha
    return out


def dividends(secs):
    """Two dividends a year per payer: ex-dates and pay dates, amounts in pence per share set later from price."""
    r = rng("dividends")
    sched = {}
    for s in secs:
        if s["name"] == "Penrose Bank plc":
            yield_ = 0.045
        else:
            yield_ = {"Financials": 0.045, "Energy": 0.055, "Utilities": 0.050, "Real Estate": 0.042,
                      "Basic Materials": 0.040, "Telecommunications": 0.048, "Consumer Staples": 0.036,
                      "Industrials": 0.024, "Health Care": 0.020, "Consumer Discretionary": 0.022,
                      "Technology": 0.010}[s["industry"]]
            if s["market"] == "AIM":
                yield_ = 0.0 if r.random() < 0.6 else 0.008
        if yield_ == 0:
            sched[s["sid"]] = []
            continue
        yield_ *= float(r.uniform(0.7, 1.3))
        # interim and final ex-dates: spread across the year, many near quarter-ends
        m1 = int(r.choice([2, 3, 5, 6, 8, 9, 10, 11]))
        m2 = (m1 + 6 - 1) % 12 + 1
        evs = []
        for m in (m1, m2):
            for y in (2025, 2026):
                day = int(r.integers(1, 27))
                exd = D(y, m, day)
                while exd.weekday() != 3 or exd in BANK_HOLIDAYS:     # UK ex-dates fall on Thursdays
                    exd += dt.timedelta(days=1)
                if D(2026, 3, 26) <= exd <= D(2026, 4, 10):
                    exd = D(2026, 4, 16)          # registrars avoid the Easter settlement week
                if not (HIST_START <= exd <= EXTRACT_END):
                    continue
                payd = exd + dt.timedelta(days=int(r.integers(22, 48)))
                while payd.weekday() >= 5 or payd in BANK_HOLIDAYS:
                    payd += dt.timedelta(days=1)
                frac = 0.38 if m == m1 else 0.62
                evs.append(dict(ex=exd, pay=payd, frac=frac))
        if s["name"] == "Penrose Bank plc":
            evs = [dict(ex=D(2025, 8, 21), pay=D(2025, 9, 26), frac=0.4),
                   dict(ex=D(2025, 11, 13), pay=D(2025, 12, 19), frac=0.6),
                   dict(ex=D(2026, 3, 12), pay=D(2026, 4, 24), frac=0.6)]   # declared 26 February, never paid
        sched[s["sid"]] = [dict(e, yld=yield_) for e in sorted(evs, key=lambda e: e["ex"])]
    return sched


DECLARED = {("Wath Energy plc", D(2025, 11, 20)): 15.80}   # rates a board declared in round tenths of a penny


def price_paths(secs, rets, divs):
    """Noon prices in pence, with the ex-dividend drop and Penrose's collapse; dividends in pence per share."""
    r = rng("pricelevels")
    n = len(DAYS)
    prices = {}
    for s in secs:
        sid = s["sid"]
        p0 = float(np.exp(r.uniform(np.log(80), np.log(4200))))
        path = np.zeros(n)
        path[0] = p0
        ex_map = {}
        for ev in divs[sid]:
            if ev["ex"] in IDX:
                ex_map[IDX[ev["ex"]]] = ev
        for i in range(1, n):
            d = DAYS[i]
            ret = rets[sid][i]
            if s["name"] == "Penrose Bank plc":
                if d in PENROSE_PATH:
                    ret = PENROSE_PATH[d]
                elif d >= PENROSE_SUSPENDED:
                    path[i] = path[i - 1]
                    continue
            new = path[i - 1] * (1 + ret)
            if i in ex_map:
                ev = ex_map[i]
                amt = DECLARED.get((s["name"], DAYS[i]), round(path[i - 1] * ev["yld"] * ev["frac"], 2))
                ev["pence"] = amt
                new -= amt
            path[i] = max(new, 1.0)
        for ev in divs[sid]:
            if "pence" not in ev:
                i = IDX.get(ev["ex"])
                ev["pence"] = round(path[i - 1] * ev["yld"] * ev["frac"], 2) if i else 0.0
        prices[sid] = np.round(path, 2 if path.mean() > 20 else 3)
    return prices


def settle_date(d, n=2):
    """UK equities settle two dealing days after the trade"""
    k = 0
    while k < n:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in BANK_HOLIDAYS:
            k += 1
    return d


def listing_moves(secs, growth):
    """growth holdings that move from AIM to the Main Market during the year (effective date, new, old)"""
    aim = sorted([s for s in growth if s["market"] == "AIM"], key=lambda s: s["sid"])
    tech = [s for s in aim if s["industry"] == "Technology"]
    health = [s for s in aim if s["industry"] == "Health Care"]
    return {tech[1]["sid"]: (D(2026, 5, 18), "Main Market", "AIM"),
            health[0]["sid"]: (D(2026, 9, 7), "Main Market", "AIM")}


def market_on(sec, d, moves):
    m = moves.get(sec["sid"])
    if not m:
        return sec["market"]
    eff, new, old = m
    return new if d >= eff else old


def close_prices(secs, prices, mk):
    """Close-of-business prices in pence: the noon price carried through the afternoon's move."""
    r = rng("closeprices")
    n = len(DAYS)
    out = {}
    for s in secs:
        sid = s["sid"]
        z = r.standard_normal(n)
        aft = s["beta"] * mk["close_extra"] + 0.0035 * z
        c = prices[sid] * (1 + aft)
        if s["name"] == "Penrose Bank plc":
            for i, d in enumerate(DAYS):
                if d >= PENROSE_SUSPENDED:
                    c[i] = c[IDX[D(2026, 3, 13)]]
        out[sid] = np.round(c, 2 if prices[sid].mean() > 20 else 3)
    return out


# ----------------------------------------------------------------------------------------------------------
# the index provider's series
PEN_W_BENCH = 0.0080   # Penrose's weight in the benchmark before its fall
PEN_W_VALUE = 0.0310   # and in the value index


def index_series(mk, pen_ret):
    """Total return levels of the benchmark (noon and close), its price index (close), the Larkspur 100 (noon and
    close, price), and the value and growth style indices (close, total return)."""
    n = len(DAYS)
    bench = mk["bench"]
    div_yield = 0.0352
    tr_noon = np.zeros(n); tr_noon[0] = 9_412.37
    pr_close = np.zeros(n)
    for i in range(1, n):
        tr_noon[i] = tr_noon[i - 1] * (1 + bench[i])
    tr_close = tr_noon * (1 + mk["close_extra"])
    # the price index runs below the total return index by the dividends the index reinvests
    cal = np.array([(d - DAYS[0]).days for d in DAYS])
    pr_close = tr_close * np.exp(-div_yield * cal / 365.0) * (4_391.88 / tr_close[0])
    l100_noon = np.zeros(n); l100_noon[0] = 8_806.4
    for i in range(1, n):
        l100_noon[i] = l100_noon[i - 1] * (1 + mk["l100"][i] - div_yield / 252)
    rl = rng("l100close")
    l100_close = l100_noon * (1 + mk["close_extra"] + 0.0004 * rl.standard_normal(n))
    # style indices: the value index carries more of Penrose and of the value factor
    v_ex = 0.42 * mk["style"] + 0.08 * mk["fin"] + (PEN_W_VALUE - PEN_W_BENCH) * (pen_ret - bench)
    v_ret = bench + v_ex
    g_ret = bench - (0.44 / 0.56) * v_ex
    rv = rng("styleclose")
    val = np.zeros(n); gro = np.zeros(n); val[0] = 5_206.14; gro[0] = 6_877.52
    for i in range(1, n):
        val[i] = val[i - 1] * (1 + v_ret[i]); gro[i] = gro[i - 1] * (1 + g_ret[i])
    val_close = val * (1 + mk["close_extra"] + 0.0006 * rv.standard_normal(n))
    gro_close = gro * (1 + mk["close_extra"] + 0.0006 * rv.standard_normal(n))
    return dict(tr_noon=np.round(tr_noon, 2), tr_close=np.round(tr_close, 2), pr_close=np.round(pr_close, 2),
                l100_noon=np.round(l100_noon, 1), l100_close=np.round(l100_close, 1),
                val_close=np.round(val_close, 2), gro_close=np.round(gro_close, 2))


# ----------------------------------------------------------------------------------------------------------
# futures on the Larkspur 100: quarterly contracts, third Friday expiry, ten pounds a point
def third_friday(y, m):
    d = D(y, m, 1)
    while d.weekday() != 4:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(days=14)


CONTRACTS = []
for _y in (2025, 2026, 2027):
    for _m, _c in ((3, "H"), (6, "M"), (9, "U"), (12, "Z")):
        CONTRACTS.append((f"LKX{_c}{str(_y)[-1]}", third_friday(_y, _m)))
CONTRACTS = [c for c in CONTRACTS if c[1] >= D(2025, 6, 1)]


def front_contract(d, roll_days=5):
    """the contract an overlay holds on day d: the nearest expiry more than roll_days dealing days away"""
    for code, exp in CONTRACTS:
        if exp in IDX and IDX[exp] - IDX.get(d, 0) > roll_days:
            return code, exp
        if exp not in IDX and exp > d:
            return code, exp
    raise ValueError(d)


def futures_marks(ix):
    """noon marks for every listed contract on every dealing day: the index level carried to expiry at the
    financing rate less the dividend yield, with a little basis noise"""
    r = rng("basis")
    out = {}
    for code, exp in CONTRACTS:
        row = {}
        for i, d in enumerate(DAYS):
            if d > exp:
                continue
            t = (exp - d).days / 365.0
            carry = (mmf_rate(d) - 0.0006 - 0.0352) * t
            row[d] = round(2 * float(ix["l100_noon"][i] * (1 + carry + 0.00018 * r.standard_normal()))) / 2
        out[code] = row
    return out


def mmf_rate(d):
    """the liquidity sleeve's money market fund, annual yield (actual/365)"""
    if d < D(2025, 8, 8):
        return 0.0421
    if d < D(2025, 11, 7):
        return 0.0402
    if d < D(2026, 2, 6):
        return 0.0385
    if d < D(2026, 5, 8):
        return 0.0371
    return 0.0360


