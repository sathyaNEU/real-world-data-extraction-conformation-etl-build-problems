"""Simulate the eight counties' home-purchase mortgages closed from October 2023 to August 2026, how each one
reaches the county recorder, which recordings the vendor's purchase-money file holds, the vendor's other
purchase-flagged recordings, and the lenders' identifiers. Each lender and year draws from its own random stream,
so a lender's records depend on nothing but its own parameters."""
import datetime as dt
import zlib

import numpy as np
import pandas as pd
from faker import Faker

import world as W

HOLIDAYS = {dt.date(*d) for d in [
    (2023, 11, 10), (2023, 11, 23), (2023, 11, 24), (2023, 12, 25), (2024, 1, 1), (2024, 1, 15), (2024, 2, 19),
    (2024, 5, 27), (2024, 7, 4), (2024, 9, 2), (2024, 11, 11), (2024, 11, 28), (2024, 11, 29), (2024, 12, 25),
    (2025, 1, 1), (2025, 1, 20), (2025, 2, 17), (2025, 5, 26), (2025, 7, 4), (2025, 9, 1), (2025, 11, 11),
    (2025, 11, 27), (2025, 11, 28), (2025, 12, 25), (2026, 1, 1), (2026, 1, 19), (2026, 2, 16), (2026, 5, 25),
    (2026, 7, 3), (2026, 9, 7), (2026, 11, 11), (2026, 11, 26), (2026, 11, 27), (2026, 12, 25)]}
ADJ = {"Marion": ["McPherson", "Dickinson"], "Dickinson": ["Marion", "Saline"], "Ellsworth": ["Lincoln", "Rice"],
       "Rice": ["McPherson", "Ellsworth"], "Lincoln": ["Ottawa", "Ellsworth"], "Saline": ["Ottawa", "McPherson"],
       "McPherson": ["Rice", "Marion"], "Ottawa": ["Saline", "Lincoln"]}
GERMAN = ["Unruh", "Friesen", "Schmidt", "Janzen", "Penner", "Regier", "Koehn", "Goering", "Voth", "Dyck", "Entz",
          "Wiens", "Funk", "Klassen", "Ediger", "Nickel", "Thiessen", "Harms", "Bartel", "Kaufman", "Schrag",
          "Stucky", "Ratzlaff", "Loewen", "Jost", "Hiebert", "Esau", "Duerksen", "Flaming", "Wedel"]
SWEDISH = ["Johnson", "Peterson", "Anderson", "Nelson", "Carlson", "Lindholm", "Swenson", "Holmquist", "Engstrom",
           "Lundgren", "Berggren", "Sjogren"]
CZECH = ["Hlavaty", "Soukup", "Vopat", "Zajic", "Pfeifer", "Hrabe", "Kralik", "Mach", "Svoboda", "Brungardt"]
STREETS = ["ASH", "ELM", "OAK", "WALNUT", "CHERRY", "MAPLE", "HIGHLAND", "MARKET", "IRON", "PRESCOTT", "REPUBLIC",
           "CRAWFORD", "CLOUD", "SANTA FE", "OHIO", "COLUMBIA", "KENWOOD", "WAYNE", "BROADWAY", "SUNSET", "KANSAS",
           "LINCOLN", "PARK", "CEDAR", "SPRUCE", "GRAND", "EUCLID", "MAIN", "WASHINGTON", "JEFFERSON", "MADISON",
           "PINE", "FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH", "SEVENTH", "EIGHTH", "NINTH"]
SUFFIX = ["ST", "AVE", "DR", "ST", "AVE", "LN", "CT", "PL", "ST"]
ADDNS = ["MAYFAIR", "COUNTRY CLUB", "GLENDALE", "HIGHLAND PARK", "SUNSET HEIGHTS", "EASTBOROUGH", "WESTGATE",
         "PARKVIEW", "COLLEGE HILL", "ORIGINAL TOWN", "OAKDALE", "SOUTHGATE", "NORTH PARK", "FAIRVIEW", "LAKEWOOD"]
ROADS = (["%d%s RD" % (k, "TH" if k % 10 > 3 or k % 10 == 0 or 10 < k < 14 else {1: "ST", 2: "ND", 3: "RD"}[k % 10])
          for k in range(1, 30)] + ["%s AVE" % ch for ch in "ABCDEFGHJKLMNP"] +
         ["OLD HWY 81", "SMOKY HILL RIVER RD", "K-4 HWY", "WATERWELL RD", "HEDVILLE RD"])
FK = Faker("en_US")


def stream(*keys):
    return np.random.default_rng([W.SEED] + [zlib.crc32(str(k).encode()) for k in keys])


def faker(*keys):
    FK.seed_instance(zlib.crc32("/".join(str(k) for k in keys).encode()))
    return FK


def is_bday(d):
    return d.weekday() < 5 and d not in HOLIDAYS


def next_bday(d):
    while not is_bday(d):
        d += dt.timedelta(days=1)
    return d


def bdays(y, m):
    d, out = dt.date(y, m, 1), []
    while d.month == m:
        if is_bday(d):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def all_bdays(y):
    d, out = dt.date(y, 1, 1), []
    while d.year == y:
        if is_bday(d):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def closing_days(rng, y, m, n):
    days = bdays(y, m)
    w = np.ones(len(days))
    w[-4:] *= 2.6                   # closings bunch at the end of the month
    w[-1] *= 1.4
    return [days[i] for i in rng.choice(len(days), size=n, p=w / w.sum())]


def systematic(n, c, u):
    """Systematic selection at rate c with random start u: within any run of consecutive items the number selected
    is the run's length times c, give or take one."""
    i = np.arange(n)
    return (np.floor(c * (i + 1) + u) - np.floor(c * i + u)).astype(bool)


# ---------------------------------------------------------------------------------------------------- lenders ----
def lenders():
    rng = np.random.default_rng(W.SEED * 7 + 1)
    out = [dict(x) for x in W.L]
    for k, t in enumerate(W.TAIL):
        name, ch, hq, county, n = t
        x = dict(id="T%02d" % (k + 1), name=name, kind="R", ch=ch, route="P", hq=hq, qc=0.004,
                 mers=0.92 if ch == "NB" else 0.5, off=0.0, rows=int(rng.integers(60, 520)))
        if county:
            x["home"] = {county: 1.0}
            x["years"] = {2023: 0, 2024: n[0], 2025: n[1], 2026: n[2]}
            x["total"] = n[0] + n[1]
        else:
            x["home"] = None
            x["total"] = n
        out.append(x)
    used = set()
    for x in out:
        x.setdefault("dup", 0)
        x.setdefault("pig", 0.0)
        x.setdefault("buy", 0)
        x.setdefault("short_list", False)
        x.setdefault("label", "")
        x.setdefault("rows", 0)
        while True:
            nm = int(rng.integers(400000, 900000)) if x["ch"] in ("CB", "CU", "RB") else int(rng.integers(3000, 2600000))
            if nm not in used:
                used.add(nm)
                break
        x["nmls"] = nm
        x["lei"] = W.lei(rng) if (x["kind"] == "R" or x["id"] in ("N1", "N2", "N3")) else ""
        x["rssd"] = int(rng.integers(100000, 5900000)) if x["ch"] in ("CB", "CU", "RB") else ""
    return out


# ------------------------------------------------------------------------------------------------- mortgages ----
def periods():
    """(year, months) blocks simulated, with each block's weight against a lender's two-year total."""
    q4 = W.MONTH_W[9:].sum() / W.MONTH_W.sum()
    jan_aug = W.MONTH_W[:8].sum() / W.MONTH_W.sum()
    return [(2023, list(range(10, 13)), 0.47 * 0.96 * q4), (2024, list(range(1, 13)), None),
            (2025, list(range(1, 13)), None), (2026, list(range(1, 9)), W.YEAR_W[2025] * W.GROWTH_2026 * jan_aug)]


def surname(fk, rng, county):
    u = rng.random()
    if county in ("Marion", "McPherson") and u < 0.30:
        return GERMAN[int(rng.integers(len(GERMAN)))]
    if county == "McPherson" and u < 0.38:
        return SWEDISH[int(rng.integers(len(SWEDISH)))]
    if county in ("Ellsworth", "Rice", "Lincoln") and u < 0.18:
        return CZECH[int(rng.integers(len(CZECH)))]
    return fk.last_name()


# surnames that read as a reviewer's vocabulary are written as a neighbouring surname (no draw is spent on it)
RENAME = {"GOLDEN": "GOLDING", "STUMP": "STUMPF", "TRUTH": "TRUITT", "SECRET": "SECREST", "LADDER": "LADD",
          "HIDDEN": "HIDDLE", "TRAP": "TRAPP", "DECOY": "DECKER", "RUNG": "RUNGE", "SEED": "SEEDS"}


def person(fk, rng, county):
    last = surname(fk, rng, county).upper()
    last = RENAME.get(last, last)
    a = "%s %s" % (fk.first_name().upper(), rng.choice(list("ABCDEFGHJKLMRST")))
    if rng.random() < 0.58:
        return "%s %s & %s %s" % (last, a, fk.first_name().upper(), rng.choice(list("ABCDEJKLMR")))
    return "%s %s" % (last, a)


# in a sale between unrelated parties the seller and buyer do not share a surname; a draw that pairs two is given
# another surname for the seller, chosen from the record itself so no draw is spent on it
UNRELATED = ["ANDERSON", "BAKER", "COLLINS", "DAVIS", "ELLIS", "FOSTER", "GRAHAM", "HARRIS", "JENSEN", "KELLER",
             "LARSON", "MILLER", "NELSON", "OWENS", "PARKER", "REYNOLDS", "SCHMIDT", "THOMPSON", "WALKER", "YOUNG"]


def unrelated(seller, buyer, county, close):
    a, b = seller.split()[0], buyer.split()[0]
    if a != b:
        return seller
    k = zlib.crc32(("%s|%s|%s" % (seller, county, close)).encode())
    alt = [x for x in UNRELATED if x != b]
    return " ".join([alt[k % len(alt)]] + seller.split()[1:])


def place(rng, c, across=True):
    """Where a home in county c stands and how it is addressed and described."""
    ax = W.MAIL_ACROSS.get(c)
    if across and ax and rng.random() < ax[1]:
        t, r = ax[0], True
    else:
        t = W.TOWNS[c][rng.choice(len(W.TOWNS[c]), p=np.array(W.TOWN_W[c]) / sum(W.TOWN_W[c]))]
        r = rng.random() < W.RURAL[c] * (0.5 if t == W.TOWNS[c][0] else 1.2)
    if r:
        addr = "%d %s %s" % (int(rng.integers(100, 3999)), rng.choice(["N", "S", "E", "W"]), rng.choice(ROADS))
        legal = "%s%s %d-%d-%dW" % (rng.choice(["N2", "S2", "E2", "W2", "NE4", "NW4", "SE4", "SW4"]),
                                    "" if rng.random() < 0.6 else " " + str(rng.choice(["NE4", "SE4", "NW4"])),
                                    int(rng.integers(1, 37)), int(rng.integers(12, 21)), int(rng.integers(1, 11)))
    else:
        addr = "%d %s%s %s" % (int(rng.integers(100, 2999)), rng.choice(["", "N ", "S ", "E ", "W "]),
                               rng.choice(STREETS), rng.choice(SUFFIX))
        legal = "LOT %d BLK %d %s ADD" % (int(rng.integers(1, 30)), int(rng.integers(1, 15)), rng.choice(ADDNS))
    apn = "%03d-%03d-%02d-0-%02d-%02d-%03d.%02d-0" % (
        W.KSNO[c], int(rng.integers(1, 200)), int(rng.integers(1, 37)), int(rng.choice([10, 20, 30, 40])),
        int(rng.integers(1, 9)), int(rng.integers(1, 60)), int(rng.choice([0, 0, 0, 1, 2])))
    return dict(city=t, rural=r, addr=addr, zip=W.ZIP[t], apn=apn, legal=legal, hmda_county=W.CITY_COUNTY[t])


def loan(rng, x, c, r, yr):
    base = W.PRICE[c] * (1.0 + 0.045 * (yr - 2024)) * (1.12 if r else 1.0)
    p = float(np.exp(rng.normal(np.log(base), 0.42)))
    p = max(38000.0, min(p, 1150000.0))
    ch = x["ch"]
    u = rng.random()
    if ch in ("CB", "CU") or (ch == "RB" and u < 0.4):
        t = "CONV" if u < 0.86 else ("USDA" if u < 0.95 else "FHA")
    else:
        t = "CONV" if u < 0.55 else ("FHA" if u < 0.74 else ("VA" if u < 0.85 else "USDA"))
    ltv = float(rng.choice([0.80, 0.80, 0.90, 0.95, 0.97, 0.85, 0.75, 0.70])) if t == "CONV" else (
        0.965 if t == "FHA" else 1.0)
    a = round(p * ltv * (1.0175 if t == "FHA" else 1.0) / 50) * 50
    o = 1 if rng.random() < 0.89 else (3 if rng.random() < 0.8 else 2)
    units = 1 if rng.random() < 0.975 else int(rng.choice([2, 2, 3, 4]))
    cons = 1 if not r or rng.random() < 0.9 else 2
    return dict(price=round(p / 100) * 100, amount=int(a), ltype=t, occ=o, units=units, cons=cons)


def recording(rng, x, d):
    """The closing's route to the recorder and its recording dates. P: the deed and the mortgage go in one
    package; S: the deed is recorded, then the lender records its own mortgage."""
    r = x["route"]
    if r == "S" and d >= W.SWITCH:
        r = "P"
    k = int(rng.choice([0, 1, 2, 3, 4], p=[0.30, 0.38, 0.18, 0.09, 0.05]))
    dr = next_bday(d + dt.timedelta(days=k))
    if r == "P":
        mr = dr
    else:
        mr = next_bday(dr + dt.timedelta(days=1 + int(min(43, rng.gamma(1.6, 7.0)))))
    return dict(route=r, deed_rec=dr, mtg_rec=mr)


def lender_records(x):
    """Every closing of one lender from October 2023 to August 2026, from the lender's own streams."""
    rows = []
    N = x["total"]
    home = x["home"] or W.COUNTY_W
    cs = list(home)
    p = np.array([home[c] for c in cs], float)
    p /= p.sum()
    n24 = int(round(N * W.YEAR_W[2024] + stream("split", x["id"]).normal(0, 0.03 * N ** 0.5)))
    for y, months, wt in periods():
        rng = stream("close", x["id"], y)
        fk = faker("people", x["id"], y)
        if "years" in x:
            n = x["years"][y]
            months = months if y != 2026 else list(range(1, 7))
        elif wt is None:
            n = n24 if y == 2024 else N - n24
        else:
            n = int(rng.poisson(N * wt))
        mw = W.MONTH_W[[m - 1 for m in months]]
        per = rng.multinomial(n, mw / mw.sum())
        for m, k in zip(months, per):
            for d in closing_days(rng, y, m, k):
                c = cs[rng.choice(len(cs), p=p)]
                rec = dict(lender=x["id"], close=d, county=c)
                rec.update(place(rng, c))
                rec.update(loan(rng, x, c, rec["rural"], y))
                rec["buyer"] = person(fk, rng, c)
                rec["seller"] = person(fk, rng, c)
                if rec["occ"] == 3 and rng.random() < 0.45:
                    rec["buyer"] = "%s %s LLC" % (rec["buyer"].split()[0],
                                                   rng.choice(["PROPERTIES", "RENTALS", "HOLDINGS", "INVESTMENTS"]))
                rec["seller"] = unrelated(rec["seller"], rec["buyer"], c, d)
                rec.update(recording(rng, x, d))
                rows.append(rec)
    D = pd.DataFrame(rows)
    return capture_lender(D, x)


def capture_lender(D, x):
    """Which of a lender's mortgages the vendor pairs with their deed: systematic at the lender's capture within each
    route and year."""
    cap = np.zeros(len(D), bool)
    if len(D):
        yr = D.close.map(lambda d: d.year)
        for (r, y), g in D.groupby(["route", yr], sort=True):
            g = g.sort_values(["county", "close", "addr"], kind="mergesort")
            c = W.CAPTURE[r] + (x["off"] if r == x["route"] else 0.0)
            cap[D.index.get_indexer(g.index)] = systematic(len(g), c, stream("cap", x["id"], r, y).random())
    D["captured"] = cap
    return D


def true_mortgages(LX, cache=None):
    parts = []
    for x in LX:
        key = (x["id"], x["total"], tuple(sorted(x.get("years", {}).items())))
        if cache is not None and key in cache:
            parts.append(cache[key])
            continue
        D = lender_records(x)
        if cache is not None:
            cache[key] = D
        parts.append(D)
    M = pd.concat(parts, ignore_index=True)
    M = M.sort_values(["close", "lender", "county", "addr"], kind="mergesort").reset_index(drop=True)
    M["rid"] = ["M%05d" % i for i in range(len(M))]
    return M


def two_county(M, LX):
    """Farmstead mortgages on land in two counties are recorded in both; the house stands in the first."""
    M["land_county"] = ""
    for x in LX:
        if not x["dup"]:
            continue
        rng = stream("dup", x["id"])
        pool = M[(M.lender == x["id"]) & M.rural & M.close.map(lambda d: 2024 <= d.year <= 2025) & M.captured]
        main = max(x["home"], key=x["home"].get) if x["home"] else None
        if main:
            pool = pool[pool.county == main]
        pick = pool.index.values[rng.choice(len(pool), size=x["dup"], replace=False)]
        for i in sorted(pick):
            M.at[i, "land_county"] = str(rng.choice(ADJ[M.at[i, "county"]]))
    pool = M[(M.lender == "N3") & M.rural & (M.close >= dt.date(2026, 1, 1)) & M.captured & (M.county == "Marion")]
    if len(pool):
        M.at[pool.index.values[0], "land_county"] = "McPherson"
    # the farmsteads whose land runs across the Saline, Marion and McPherson lines: Eisenbrandt's Dickinson county
    # farms reaching into Saline and Marion, Stueckemann's Rice county farms reaching into McPherson
    for lid, house, land, k in (("N5", "Dickinson", "Saline", 5), ("N5", "Dickinson", "Marion", 3),
                                ("N7", "Rice", "McPherson", 3), ("N3", "Marion", "Dickinson", 2)):
        rng = stream("dup2", lid, land)
        pool = M[(M.lender == lid) & M.rural & M.close.map(lambda d: 2024 <= d.year <= 2025) & M.captured &
                 (M.county == house) & (M.land_county == "")]
        pick = pool.index.values[rng.choice(len(pool), size=min(k, len(pool)), replace=False)]
        for i in sorted(pick):
            M.at[i, "land_county"] = land
    return M


def piggyback(M, LX):
    M["second_amt"] = 0
    for x in LX:
        if not x["pig"]:
            continue
        g = M[(M.lender == x["id"]) & (M.route == "P")].sort_values(["close", "rid"])
        sel = systematic(len(g), x["pig"], stream("pig", x["id"]).random())
        for i in g.index.values[sel]:
            M.at[i, "second_amt"] = int(round(M.at[i, "price"] * 0.10 / 50) * 50)
            M.at[i, "amount"] = int(round(M.at[i, "price"] * 0.80 / 50) * 50)
    return M


# ------------------------------------------------------------------------------- other purchase-flagged rows ----
def quitclaim_refis(M, LX):
    """Owners deed the home to their own trust by quitclaim and refinance in the trust's name; the vendor pairs the
    refinance with the quitclaim and flags it purchase money."""
    rows = []
    yr = M.close.map(lambda d: d.year)
    for x in LX:
        if not x["qc"]:
            continue
        home = x["home"] or W.COUNTY_W
        cs = list(home)
        p = np.array([home[c] for c in cs], float)
        p /= p.sum()
        for y, months, _ in periods():
            rng = stream("qc", x["id"], y)
            fk = faker("owners", x["id"], y)
            n_p = int(((M.lender == x["id"]) & (yr == y)).sum())
            n = int(rng.poisson(x["qc"] * n_p)) if x["qc"] < 0.2 else int(round(x["qc"] * n_p))
            mw = W.MONTH_W[[m - 1 for m in months]] * 0.5 + 0.5 / 12
            per = rng.multinomial(n, mw / mw.sum())
            for m, k in zip(months, per):
                for d in closing_days(rng, y, m, k):
                    c = cs[rng.choice(len(cs), p=p)]
                    rec = dict(lender=x["id"], close=d, county=c)
                    rec.update(place(rng, c, across=False))
                    owner = person(fk, rng, c)
                    last = owner.split()[0]
                    rec["seller"] = owner
                    rec["buyer"] = str(rng.choice(["%s FAMILY TRUST" % last, "%s REVOCABLE TRUST" % last,
                                                   "%s %s TRUSTEE" % (last, " ".join(owner.split()[1:3])),
                                                   "%s LIVING TRUST" % last]))
                    rec["amount"] = int(round(float(np.exp(rng.normal(np.log(W.PRICE[c] * 0.55), 0.5))) / 50) * 50)
                    rows.append(rec)
    Q = pd.DataFrame(rows).sort_values(["close", "lender", "county", "addr"], kind="mergesort").reset_index(drop=True)
    Q["rid"] = ["Q%05d" % i for i in range(len(Q))]
    return Q


def seller_notes(LX):
    """Sales the seller finances: the buyer gives the seller a note and mortgage, recorded with the deed."""
    market = sum(x["total"] for x in LX) / 2.0
    rows = []
    for y, months, wt in periods():
        rng = stream("seller", y)
        fk = faker("seller", y)
        vol = market * (2.0 * W.YEAR_W[y] if wt is None else 2.0 * wt)
        n = int(round(W.SELLER_FIN * vol))
        mw = W.MONTH_W[[m - 1 for m in months]]
        per = rng.multinomial(n, mw / mw.sum())
        cw = np.array([W.COUNTY_W[c] * (1.0 + 2.5 * W.RURAL[c]) for c in W.REGION])
        for m, k in zip(months, per):
            for d in closing_days(rng, y, m, k):
                c = W.REGION[rng.choice(8, p=cw / cw.sum())]
                rec = dict(close=d, county=c)
                rec.update(place(rng, c, across=False))
                rec["seller"] = person(fk, rng, c)
                rec["buyer"] = person(fk, rng, c)
                rec["seller"] = unrelated(rec["seller"], rec["buyer"], c, d)
                rec["price"] = round(float(np.exp(rng.normal(np.log(W.PRICE[c] * 0.8), 0.45))) / 100) * 100
                rec["amount"] = int(round(rec["price"] * float(rng.choice([0.7, 0.8, 0.85, 0.9])) / 50) * 50)
                rows.append(rec)
    S = pd.DataFrame(rows).sort_values(["close", "county", "addr"], kind="mergesort").reset_index(drop=True)
    S["rid"] = ["S%05d" % i for i in range(len(S))]
    return S


def simulate():
    LX = lenders()
    M = true_mortgages(LX)
    M = two_county(M, LX)
    M = piggyback(M, LX)
    Q = quitclaim_refis(M, LX)
    S = seller_notes(LX)
    return dict(LX=LX, M=M, Q=Q, S=S)
