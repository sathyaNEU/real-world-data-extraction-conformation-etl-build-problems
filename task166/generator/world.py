"""The clean world: Marrowgate's catalogue, its trade accounts, and a weekly simulation of consumer sales, shop
stock, orders (invoices), returns authorisations, the distributor's receipts and the credits that quote invoices.
Everything shipped is cut from these event lists; nothing in the pack is authored apart from them.

The world's one decisive structure: a shop keeps a frontlist hardback on display until the paperback of the same
book is published, then sends what it has left back; a returned copy must quote an invoice 3 to 12 months old.
Marrowgate's hardbacks had their paperbacks about a year behind them until the autumn 2026 list, whose paperbacks
are scheduled four to five months after publication."""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

import numpy as np

import common as K

# ----------------------------------------------------------------------------------------------------------------
# Catalogue


IMPRINTS = {
    # imprint: (hardback-first works a year, trade-paperback-first a year, paperback originals a year, kind)
    "Marrowgate": (24, 6, 3, "literary"),
    "Larkhill": (21, 0, 12, "crime"),
    "Fernweather": (13, 0, 18, "commercial"),
    "Little Marrow": (6, 0, 16, "children"),
}

RRP = {  # (kind, format) -> list of list prices
    ("literary", "Hardback"): [16.99, 18.99, 20.00, 20.00, 22.00],
    ("crime", "Hardback"): [16.99, 18.99, 18.99, 20.00],
    ("commercial", "Hardback"): [16.99, 18.99, 20.00],
    ("children", "Hardback"): [12.99, 14.99, 14.99, 16.99],
    ("literary", "Trade paperback"): [14.99, 16.99],
    ("literary", "Paperback"): [9.99, 10.99, 10.99],
    ("crime", "Paperback"): [8.99, 9.99, 9.99],
    ("commercial", "Paperback"): [8.99, 9.99],
    ("children", "Paperback"): [6.99, 7.99, 7.99],
}

TITLE_A = ["Salt", "Glass", "Winter", "Harbour", "Lantern", "Orchard", "Ember", "Hollow", "River", "Stone", "Paper",
           "Iron", "Linen", "Ash", "Juniper", "Marsh", "Copper", "Tide", "Thorn", "Hawthorn", "Cinder", "Quiet",
           "Fallow", "Kestrel", "Ivory", "Bramble", "Saltwater", "Midnight", "Cobalt", "Heron", "Larch", "Slate"]
TITLE_B = ["Road", "House", "Year", "Garden", "Daughter", "Keeper", "Line", "Room", "Shore", "Field", "Season",
           "Bridge", "Hours", "Lights", "Hill", "Crossing", "Archive", "Fire", "Weather", "Song", "Inheritance",
           "Map", "Island", "Letters", "Mile", "Window", "Country", "Water", "Ground", "Silence", "Harvest"]
TITLE_C = ["The {a} {b}", "{a} {b}", "A {a} {b}", "The {b} of {a}", "{a} and {a2}", "The Last {b}", "Under the {a} {b}",
           "The {a}maker", "Small {b}s", "The {b} at {place}", "After the {b}", "{place}"]
PLACES = ["Holloway", "Ardwell", "Pentreath", "Caldmoor", "Ness", "Saltash Row", "Kirkby Fold", "Dunmere", "Eastry",
          "Wrayburn", "Corrigan Street", "Fenmouth", "Halsey", "Morrow Bay", "Ravelstone", "Tollan", "Brackwater"]
SUBTITLES = ["A Novel", "A Thriller", "A Memoir", "A Mystery", "An Inspector Vane Mystery", "Stories"]


@dataclass
class Work:
    wid: int
    imprint: str
    kind: str
    author_first: str
    author_last: str
    title: str
    first_format: str
    pub: dt.date
    strength: float                   # expected first-year UK consumer units of the first edition
    tier: str
    window_months: float | None = None  # hardback to paperback, where a paperback edition follows
    retitle: str = "same"             # how the paperback's title differs from the first edition's


@dataclass
class Edition:
    eid: int
    wid: int
    fmt: str
    pub: dt.date
    rrp: float
    isbn: str
    title: str
    contributor: str
    strength: float
    is_first: bool
    successor: int | None = None      # the edition whose publication ends this one's frontlist life
    succ_pub: dt.date | None = None


def _title(r):
    pat = TITLE_C[int(r.integers(len(TITLE_C)))]
    a, a2 = TITLE_A[int(r.integers(len(TITLE_A)))], TITLE_A[int(r.integers(len(TITLE_A)))]
    b = TITLE_B[int(r.integers(len(TITLE_B)))]
    place = PLACES[int(r.integers(len(PLACES)))]
    if a2 == a:
        a2 = TITLE_A[(TITLE_A.index(a) + 7) % len(TITLE_A)]
    t = pat.format(a=a, a2=a2, b=b, place=place)
    return t.replace("The Thewmaker", "The Tidemaker")


def _authors(n):
    from faker import Faker
    f = Faker("en_GB")
    Faker.seed(K.SEED * 31 + 4)
    out, seen = [], set()
    while len(out) < n:
        first, last = f.first_name(), f.last_name()
        if (first, last) in seen or len(last) < 3:
            continue
        seen.add((first, last))
        out.append((first, last))
    return out


def _pub_date(r, year, kind):
    """UK trade publishing: Thursdays, with the heaviest hardback months September and October."""
    if kind == "hb":
        w = np.array([3, 5, 7, 8, 7, 7, 5, 3, 14, 16, 4, 1], float)
    else:
        w = np.array([7, 7, 9, 9, 9, 10, 9, 8, 9, 8, 6, 2], float)
    m = int(r.choice(12, p=w / w.sum())) + 1
    d = dt.date(year, m, int(r.integers(1, 26)))
    return K.thursday_on_or_after(d)


def _core(t):
    import re
    t = t.lower().split(":")[0].replace("&", " and ")
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return re.sub(r"^(the|a|an) ", "", t)


def build_catalogue():
    r = K.rng("catalogue")
    authors = _authors(900)
    works, ai = [], 0
    cores = {}
    wid = 1000
    # the backlist: paperbacks of works first published 2009 to 2017 (their hardbacks long out of print)
    for year in range(2009, 2018):
        for imp, (n_hb, n_tpb, n_pbo, kind) in IMPRINTS.items():
            n = int(round((n_hb + n_tpb + n_pbo) * 0.55))
            for _ in range(n):
                first, last = authors[ai % len(authors)]
                ai += 1
                s = float(np.exp(r.normal(np.log(1600 if kind != "children" else 1800), 0.8)))
                t = _title(r)
                while _core(t) in cores.setdefault((first, last), set()):
                    t = _title(r)
                cores[(first, last)].add(_core(t))
                works.append(Work(wid, imp, kind, first, last, t, "Paperback", _pub_date(r, year, "pb"), s, "D"))
                wid += 1
    # the frontlist years the ledger and its run-up cover, and the forthcoming season
    for year in range(2018, 2028):
        for imp, (n_hb, n_tpb, n_pbo, kind) in IMPRINTS.items():
            if year == 2027:
                n_hb, n_tpb, n_pbo = n_hb // 2, n_tpb // 2, n_pbo // 2
            for fmt, n in (("Hardback", n_hb), ("Trade paperback", n_tpb), ("Paperback", n_pbo)):
                for _ in range(n + int(r.integers(-1, 2))):
                    # a third of the list comes from authors already on it
                    if works and r.random() < 0.33:
                        prev = works[int(r.integers(max(0, len(works) - 400), len(works)))]
                        first, last = prev.author_first, prev.author_last
                    else:
                        first, last = authors[ai % len(authors)]
                        ai += 1
                    pub = _pub_date(r, year, "hb" if fmt == "Hardback" else "pb")
                    med = {"Hardback": 6200, "Trade paperback": 4200, "Paperback": 8800}[fmt]
                    if kind == "children":
                        med = {"Hardback": 4200, "Paperback": 6400}.get(fmt, 4200)
                    s = float(np.exp(r.normal(np.log(med), 0.50)))
                    t = _title(r)
                    while _core(t) in cores.setdefault((first, last), set()):
                        t = _title(r)
                    cores[(first, last)].add(_core(t))
                    works.append(Work(wid, imp, kind, first, last, t, fmt, pub, s, ""))
                    wid += 1
    # tiers by first-edition strength within format
    for fmt in ("Hardback", "Trade paperback", "Paperback"):
        ss = np.array([w.strength for w in works if w.first_format == fmt and w.tier != "D"])
        q = np.quantile(ss, [0.55, 0.85, 0.96])
        for w in works:
            if w.first_format == fmt and w.tier != "D":
                w.tier = "D" if w.strength < q[0] else "C" if w.strength < q[1] else "B" if w.strength < q[2] else "A"
    # hardback to paperback windows: about a year, except a fifth of each autumn list brought out for the spring
    # market, until the autumn 2026 list, four in five of which have their paperbacks four to five months on
    rw = K.rng("windows")
    autumn_flag = lambda w: (w.pub.month, w.pub.day) >= (8, 20) and w.pub.month <= 10
    a26 = [w for w in works if w.first_format == "Hardback" and w.kind != "children" and w.pub.year == 2026 and autumn_flag(w)]
    order = rw.permutation(len(a26))
    quick26 = {a26[i].wid for i in order[: int(round(0.92 * len(a26)))]}
    # earlier autumn lists: a fifth of each list, drawn within tier bands so big and small books both appear
    quick_hist = set()
    for year in range(2017, 2026):
        lst = [w for w in works if w.first_format == "Hardback" and w.kind != "children" and w.pub.year == year and autumn_flag(w)]
        for band in (("A", "B"), ("C",), ("D",)):
            grp = sorted([w for w in lst if w.tier in band], key=lambda w: w.wid)
            k = int(np.floor(0.15 * len(grp) + rw.random()))
            if band == ("A", "B") and grp:
                k = max(k, 1)
            for i in rw.permutation(len(grp))[:k]:
                quick_hist.add(grp[i].wid)
    for w in works:
        if w.first_format == "Hardback" and w.kind != "children":
            if w.wid in quick26:
                w.window_months = float(rw.uniform(4.0, 5.3))
            elif w.wid in quick_hist:
                w.window_months = float(rw.uniform(4.0, 5.3))
            else:
                w.window_months = float(np.clip(rw.normal(12.5, 0.7), 11.4, 14.0))
        elif w.first_format == "Trade paperback":
            w.window_months = float(np.clip(rw.normal(12.0, 0.8), 10.8, 13.8))
        if w.window_months is not None:
            u = rw.random()
            w.retitle = "same" if u < 0.62 else "subtitle" if u < 0.80 else "drop_article" if u < 0.90 else "colon"
    return works


def build_editions(works):
    r = K.rng("editions")
    eds, eid = [], 1
    stems = r.permutation(np.arange(0, 10000))
    si = 0

    def new_isbn(prefix):
        nonlocal si
        stem = "%s%04d" % (prefix, int(stems[si]))      # 978-1-8469-nnnn: one registrant block, 10,000 numbers
        si += 1
        return K.isbn13(stem)

    for w in works:
        kind = w.kind
        price = RRP.get((kind, w.first_format), RRP[(kind, "Paperback")] if (kind, "Paperback") in RRP else [9.99])
        first = Edition(eid, w.wid, w.first_format, w.pub, float(r.choice(price)), new_isbn("97818469"),
                        w.title, "%s %s" % (w.author_first, w.author_last), w.strength, True)
        eds.append(first)
        eid += 1
        if w.window_months is not None:
            pub2 = K.thursday_on_or_after(w.pub + dt.timedelta(days=int(round(w.window_months * 30.44))))
            t2 = w.title
            if w.retitle == "subtitle":
                t2 = "%s: %s" % (w.title, SUBTITLES[int(r.integers(len(SUBTITLES) - (0 if kind == "crime" else 2)))])
            elif w.retitle == "drop_article" and w.title.startswith("The "):
                t2 = w.title[4:]
            elif w.retitle == "colon":
                t2 = w.title.replace(" and ", " & ") if " and " in w.title else w.title
            pb_price = RRP.get((kind, "Paperback"), [9.99])
            mult = float(r.uniform(1.3, 2.1))
            pb = Edition(eid, w.wid, "Paperback", pub2, float(r.choice(pb_price)), new_isbn("97818469"),
                         t2, "%s %s" % (w.author_first, w.author_last), w.strength * mult, False)
            eds.append(pb)
            first.successor, first.succ_pub = pb.eid, pub2
            eid += 1
    return eds


# ----------------------------------------------------------------------------------------------------------------
# Accounts


@dataclass
class Account:
    aid: int
    code: str                 # the ERP's account code since February 2023
    legacy: str               # the six-digit code it had in the old system
    name: str
    channel: str
    share: float              # share of UK consumer demand (or of export demand) through this account
    cover: float              # weeks of expected demand it reorders to
    reorder_at: float         # weeks of expected demand below which it reorders
    max_cover: float          # weeks it keeps at a returns review
    review: int               # weeks between returns reviews
    order_every: int          # weeks between orders
    display: float            # copies on display per frontlist title, by tier A (scaled for B, C, D)
    frac: float               # share of the excess sent back at a review
    ship_lag: tuple           # weeks from authorisation to receipt (low, high)
    damage: float             # share of returned copies scrapped
    terms: str                # SOR or FIRM
    discount: dict = field(default_factory=dict)
    ranges: float = 1.0       # share of the list it carries


def build_accounts():
    r = K.rng("accounts")
    A = []
    aid = 1

    def code(prefix):
        return "%s%05d" % (prefix, int(r.integers(10000, 99999)))

    def legacy():
        return "%06d" % int(r.integers(200000, 299999))

    disc = lambda hb, pb: {"Hardback": hb, "Trade paperback": hb, "Paperback": pb}
    A.append(Account(aid, code("C"), legacy(), "Ravensworth Books Ltd", "Chain", 0.30, 6.0, 3.0, 9.0, 4, 1, 6800.0, 0.85,
                     (2, 4), 0.035, "SOR", disc(0.52, 0.55)))
    aid += 1
    A.append(Account(aid, code("C"), legacy(), "Pagewell Online UK Ltd", "Online", 0.26, 3.0, 1.5, 6.0, 8, 1, 0.0, 0.90,
                     (1, 2), 0.085, "SOR", disc(0.55, 0.57)))
    aid += 1
    A.append(Account(aid, code("C"), legacy(), "Bookstack Retail Ltd", "Online", 0.06, 5.0, 2.0, 9.0, 8, 3, 0.0, 0.85,
                     (1, 3), 0.07, "SOR", disc(0.50, 0.52)))
    aid += 1
    A.append(Account(aid, code("C"), legacy(), "Calder & Pryce Wholesale Ltd", "Wholesale", 0.10, 6.0, 3.0, 10.0, 4, 2,
                     650.0, 0.75, (1, 3), 0.05, "SOR", disc(0.55, 0.57)))
    aid += 1
    A.append(Account(aid, code("C"), legacy(), "Northgate Books Distribution", "Wholesale", 0.06, 6.0, 3.0, 10.0, 4, 2,
                     400.0, 0.75, (1, 3), 0.05, "SOR", disc(0.54, 0.56)))
    aid += 1
    A.append(Account(aid, code("C"), legacy(), "Brannock Retail Services Ltd", "Supermarket", 0.10, 12.0, 4.0, 12.0, 4, 2,
                     0.0, 1.0, (2, 4), 0.11, "SOR", disc(0.58, 0.62)))
    aid += 1
    towns = ["Hexham", "Ludlow", "Frome", "Totnes", "Hay-on-Wye", "Stamford", "Whitstable", "Kendal", "Malvern",
             "Saffron Walden", "Bridport", "Wimborne", "Alnwick", "Lewes", "Tewkesbury", "Oakham", "Sherborne", "Ilkley",
             "Hebden Bridge", "Marlborough", "Southwold", "Wells", "Faversham", "Shrewsbury", "Ross-on-Wye", "Barnard Castle",
             "Bakewell", "Woodbridge"]
    styles = ["Pellow's Bookshop ({t})", "Gethin & Lowe, {t}", "Quayle Books, {t}", "Tindall Marsh Books ({t})",
              "The Lantern Bookroom, {t}", "Fennick's Booksellers ({t})", "Ink & Page ({t})", "Hollis Lane Books, {t}"]
    ish = r.dirichlet(np.full(len(towns), 1.6)) * 0.10
    for i, t in enumerate(towns):
        nm = styles[int(r.integers(len(styles)))].format(t=t)
        A.append(Account(aid, code("C"), legacy(), nm, "Independent", float(ish[i]), 8.0, 3.0, 12.0, 8, 4,
                         float(r.choice([9.0, 12.0, 15.0, 18.0])), 0.6, (1, 3), 0.03, "SOR",
                         disc(0.38 + 0.02 * float(r.integers(0, 4)), 0.40 + 0.02 * float(r.integers(0, 4))),
                         ranges=float(r.uniform(0.12, 0.30))))
        aid += 1
    exports = [("Liffey Books Wholesale", 0.30, "SOR"), ("Kerrigan's Bookshops", 0.14, "SOR"), ("Abbey Street Books", 0.06, "SOR"),
               ("Skeppsbro Bokimport AB", 0.08, "FIRM"), ("Grachtenhuis Books BV", 0.10, "SOR"), ("Buchhaus am Kanal GmbH", 0.06, "FIRM"),
               ("Librairie du Quai SARL", 0.05, "SOR"), ("Bayside Book Distributors Pty", 0.09, "SOR"),
               ("Southern Cross Books Ltd", 0.05, "SOR"), ("Totara Bay Books NZ", 0.03, "FIRM"), ("Marina Books Malta", 0.02, "SOR"),
               ("Gulf English Books LLC", 0.02, "FIRM")]
    for nm, sh, terms in exports:
        A.append(Account(aid, code("E"), legacy(), nm, "Export", 0.09 * sh, 12.0, 5.0, 16.0, 13, 4, 0.0, 0.7, (4, 8), 0.06,
                         terms, disc(0.55, 0.58), ranges=float(r.uniform(0.25, 0.6))))
        aid += 1
    return A


# ----------------------------------------------------------------------------------------------------------------
# Demand


def season_mult(weeks):
    """Weekly consumer demand multiplier by calendar week (UK trade: the Christmas run-up, a quiet January)."""
    d = np.array([K.date_of(w, 3) for w in weeks])
    doy = np.array([x.timetuple().tm_yday for x in d], float)
    m = np.ones(len(weeks))
    # the run-up to Christmas: from early November to 24 December
    m += 2.6 * np.exp(-0.5 * ((doy - 354) / 11.0) ** 2) + 0.9 * np.exp(-0.5 * ((doy - 330) / 14.0) ** 2)
    m -= 0.28 * np.exp(-0.5 * ((doy - 20) / 12.0) ** 2)            # January
    m += 0.10 * np.exp(-0.5 * ((doy - 205) / 20.0) ** 2)           # summer reading
    m[(doy > 358)] *= 0.55                                          # the week after Christmas
    return m


def edition_curves(eds, works_by_id):
    """Expected weekly UK consumer demand per edition, before the season multiplier."""
    weeks = np.arange(K.WEEKS)
    E = np.zeros((len(eds), K.WEEKS))
    for i, e in enumerate(eds):
        w0 = K.week_of(e.pub)
        a = weeks - w0
        live = a >= 0
        aa = np.where(live, a, 0).astype(float)
        if e.pub < dt.date(2018, 1, 1):
            f = np.where(live, 1.0 / 52.0 * 0.22, 0.0)            # backlist: a slow steady seller
        else:
            f = 0.62 * np.exp(-aa / 5.0) / 5.0 + 0.30 * np.exp(-aa / 26.0) / 26.0 + 0.08 / 52.0
            f = np.where(live, f, 0.0)
        E[i] = e.strength * f
        if e.successor is not None:
            ws = K.week_of(e.succ_pub)
            E[i, ws:] *= 0.06                                      # the paperback takes the hardback's sales
    return E


# ----------------------------------------------------------------------------------------------------------------
# The weekly simulation


@dataclass
class World:
    works: list
    eds: list
    accounts: list
    invoices: list            # (inv_no, week, weekday, aid, eid, qty, net_price)
    returns: list             # (ra_no, ra_day, aid, eid, qty_authorised, lapsed)
    receipts: list            # (rc_no, delivery_no, ra_no, aid, eid, day, qty, saleable, hurt, unsaleable)
    credits: list             # (cr_no, day, aid, eid, qty, inv_no, net_price, ra_no, reason)
    panel: np.ndarray         # (edition, week) UK consumer units sold
    exp_sales: np.ndarray     # (edition, week) export units sold
    params: dict


def simulate():
    works = build_catalogue()
    eds = build_editions(works)
    wbi = {w.wid: w for w in works}
    A = build_accounts()
    E = edition_curves(eds, wbi)
    S = season_mult(np.arange(K.WEEKS + 30))
    n_e = len(eds)
    tier = np.array([wbi[e.wid].tier for e in eds])
    kind = np.array([wbi[e.wid].kind for e in eds])
    fmt = np.array([e.fmt for e in eds])
    pubw = np.array([K.week_of(e.pub) for e in eds])
    succw = np.array([K.week_of(e.succ_pub) if e.succ_pub else 10 ** 6 for e in eds])
    rrp = np.array([e.rrp for e in eds])
    frontfmt = np.isin(fmt, ["Hardback", "Trade paperback"])
    tier_disp = {"A": 1.0, "B": 0.6, "C": 0.32, "D": 0.14}
    front_disp = np.array([tier_disp[t] for t in tier])
    Epad = np.concatenate([E, np.zeros((n_e, 30))], axis=1)
    cum = np.concatenate([np.zeros((n_e, 1)), np.cumsum(Epad * S[None, :], axis=1)], axis=1)

    invoices, returns, pending = [], [], []
    panel = np.zeros((n_e, K.WEEKS), np.int32)
    exp_sales = np.zeros((n_e, K.WEEKS), np.int32)
    inv_no, ra_no = [26000000], [400000]
    moq = {"Chain": 5, "Online": 6, "Wholesale": 5, "Supermarket": 10, "Independent": 2, "Export": 4}

    for acc in A:
        ra_ = K.rng("acct", acc.aid)
        carry = np.ones(n_e, bool)
        if acc.channel == "Supermarket":
            carry = ((tier == "A") & (kind != "literary")) | ((fmt == "Paperback") & np.isin(kind, ["commercial", "crime"]) & np.isin(tier, ["A", "B"])) \
                | ((kind == "children") & (tier == "A"))
        elif acc.channel in ("Independent", "Export"):
            p = acc.ranges * np.where(np.isin(tier, ["A", "B"]), 1.7, np.where(tier == "C", 1.0, 0.4))
            carry = ra_.random(n_e) < np.clip(p, 0, 1)
        elif acc.channel == "Online" and acc.share < 0.1:
            carry = ra_.random(n_e) < 0.8
        idx = np.where(carry)[0]
        m = len(idx)
        if m == 0:
            continue
        Ex = Epad[idx] * acc.share
        cumx = cum[idx] * acc.share
        # the buyer's view of each title: optimistic at subscription, then drifting toward what it sells
        opt = np.where(frontfmt[idx], 0.47, 0.36) + (0.12 if acc.channel == "Supermarket" else 0.0)
        belief = np.exp(ra_.normal(opt, 0.12, m))
        stock = np.zeros(m)
        ledgers = [[] for _ in range(m)]
        disc = np.array([acc.discount.get(f, 0.5) for f in fmt[idx]])
        price = np.round(rrp[idx] * (1 - disc), 2)
        pbfront = (fmt[idx] == "Paperback") & (pubw[idx] >= K.week_of(dt.date(2019, 1, 1)))
        disp_full = np.where(frontfmt[idx], acc.display * front_disp[idx], np.where(pbfront, 0.45 * acc.display * front_disp[idx], 0.0))
        mq = moq[acc.channel]
        for wk in range(K.WEEKS):
            exp_now = Ex[:, wk] * S[wk]
            lam = exp_now * np.exp(ra_.normal(0, 0.15, m))
            dem = ra_.poisson(np.maximum(lam, 0))
            sales = np.minimum(dem, stock)
            stock -= sales
            if acc.channel == "Export":
                exp_sales[idx, wk] += sales.astype(np.int32)
            else:
                panel[idx, wk] += sales.astype(np.int32)
            ok = exp_now > 0.3
            ratio = (dem + 0.3) / (exp_now * belief + 0.3)
            belief = np.where(ok, belief * np.exp(0.15 * np.log(np.clip(ratio, 0.25, 4.0))), belief)
            age = wk - pubw[idx]
            frontlist = (age >= -1) & (age < 52) & (wk < succw[idx]) & (frontfmt[idx] | (age < 26))
            disp = np.where(frontlist, disp_full, 0.0)

            def ahead(n):
                return cumx[:, min(wk + 1 + n, K.WEEKS + 30)] - cumx[:, wk + 1]

            order = np.zeros(m)
            subs = pubw[idx] == wk + 1
            if subs.any():
                n_ahead = int(acc.cover + (10 if acc.channel in ("Chain", "Independent", "Wholesale") else 4))
                order = np.where(subs, np.ceil(belief * ahead(n_ahead) + disp_full), 0)
            if wk % acc.order_every == acc.aid % acc.order_every:
                target = belief * ahead(int(acc.cover)) + disp
                trigger = belief * ahead(max(1, int(acc.reorder_at))) + 0.7 * disp
                q = np.ceil(target - stock)
                live = (age >= 1) & (stock < trigger) & (q >= mq)
                if acc.channel == "Supermarket":
                    live &= (age < 12) & (tier[idx] == "A")
                order = np.where(live & (order == 0), q, order)
            order = np.where(order >= 1, np.maximum(order, mq), 0)
            for j in np.nonzero(order)[0]:
                inv_no[0] += int(ra_.integers(1, 4))
                q = int(order[j])
                stock[j] += q
                iwd = int(ra_.integers(0, 5))
                ledgers[j].append([inv_no[0], 7 * wk + iwd, q, float(price[j])])
                invoices.append((inv_no[0], wk, iwd, acc.aid, int(idx[j]), q, float(price[j])))
            if acc.terms == "FIRM":
                continue
            d = K.date_of(wk)
            jan = d.month == 1 and 8 <= d.day <= 14
            review = (wk % acc.review == (acc.aid * 3) % acc.review) or jan
            shed = (wk >= succw[idx]) & (wk < succw[idx] + 12) & (wk % 2 == acc.aid % 2)
            slot = np.zeros(m, bool)
            if acc.channel == "Supermarket":
                slot = (age >= 13) & ((age - 13) % 6 == 0) & (stock > 0)
            if not (review or shed.any() or slot.any()):
                continue
            keep = belief * ahead(int(acc.max_cover if not jan else max(3, acc.max_cover // 2))) + disp
            want = np.zeros(m)
            if review:
                want = np.floor(acc.frac * np.maximum(stock - keep, 0))
            want = np.where(shed, np.maximum(want, np.floor(0.93 * stock)), want)
            want = np.where(slot, np.maximum(want, np.floor(0.95 * stock)), want)
            cand = np.nonzero(want >= 2)[0]
            if len(cand) == 0:
                continue
            ra_no[0] += 1 + int(ra_.integers(0, 3))
            this_ra = ra_no[0]
            ra_day = 7 * wk + int(ra_.integers(0, 5))
            lapsed = ra_.random() < 0.025          # the account never sends the parcel; the authorisation lapses
            used = False
            for j in cand:
                elig = [l for l in ledgers[j] if K.ELIG_MIN_D <= ra_day - l[1] <= K.ELIG_MAX_D and l[2] > 0]
                cap = sum(l[2] for l in elig)
                q = int(min(want[j], cap, stock[j]))
                if q < 1:
                    continue
                used = True
                returns.append((this_ra, ra_day, acc.aid, int(idx[j]), q, lapsed))
                if lapsed:
                    continue
                stock[j] -= q
                left, match = q, []
                for l in elig:
                    take = min(left, l[2])
                    l[2] -= take
                    left -= take
                    match.append((l[0], take, l[3]))
                    if left == 0:
                        break
                pending.append((this_ra, ra_day, acc.aid, int(idx[j]), q, match))
            if not used:
                ra_no[0] -= 1
            if wk % 13 == 0:
                for j in range(m):
                    if ledgers[j] and ra_day - ledgers[j][0][1] > K.ELIG_MAX_D + 60:
                        ledgers[j] = [l for l in ledgers[j] if ra_day - l[1] <= K.ELIG_MAX_D + 60]

    # the distributor receives what was sent; Marrowgate credits each delivered line against the invoices matched
    rp = K.rng("receipts")
    acc_by = {a.aid: a for a in A}
    grades = {"Chain": (0.915, 0.062), "Online": (0.86, 0.085), "Wholesale": (0.90, 0.07), "Supermarket": (0.84, 0.10),
              "Independent": (0.93, 0.05), "Export": (0.88, 0.075)}
    by_ra = {}
    for ra, ra_day, aid, eid, q, match in pending:
        by_ra.setdefault((ra, aid, ra_day), []).append((eid, q, match))
    receipts, credits, deliveries = [], [], []
    rc_no, cr_no, dl_no = 7100000, 5500000, 880000
    for (ra, aid, ra_day), lines in sorted(by_ra.items()):
        acc = acc_by[aid]
        lag = 7 * int(rp.integers(acc.ship_lag[0], acc.ship_lag[1] + 1)) + int(rp.integers(-2, 3))
        d1 = ra_day + max(4, lag)
        p_split = {"Chain": 0.55, "Supermarket": 0.5, "Wholesale": 0.35, "Online": 0.3, "Export": 0.25, "Independent": 0.12}[acc.channel]
        split = len(lines) > 1 and rp.random() < p_split
        d2 = d1 + int(rp.integers(3, 13))
        days = {}

        def wkday(day):
            while (K.DAY0 + dt.timedelta(days=day)).weekday() >= 5:
                day += 1
            return day
        for k, (eid, q, match) in enumerate(lines):
            if split and q >= 8 and rp.random() < 0.45:
                # the copies of one line come in two parcels
                q1 = int(rp.integers(max(1, q // 4), q - max(1, q // 4) + 1))
                days.setdefault(wkday(d1), []).append((eid, q1, match, 0))
                days.setdefault(wkday(d2), []).append((eid, q - q1, match, q1))
            else:
                day = d2 if (split and rp.random() < 0.4) else d1
                days.setdefault(wkday(day), []).append((eid, q, match, 0))
        for day in sorted(days):
            dl_no += 1 + int(rp.integers(0, 3))
            deliveries.append((dl_no, ra, aid, day))
            for eid, q, match, offset in days[day]:
                rec = q
                if q >= 10 and rp.random() < 0.02:
                    rec = q - int(rp.integers(1, 4))
                s_p, h_p = grades[acc.channel]
                g = rp.multinomial(rec, [s_p, h_p, 1 - s_p - h_p])
                rc_no += 1
                receipts.append((rc_no, dl_no, ra, aid, eid, day, rec, int(g[0]), int(g[1]), int(g[2])))
                cday = day + int(rp.integers(1, 8))
                while (K.DAY0 + dt.timedelta(days=cday)).weekday() >= 5:
                    cday += 1
                cr_no += 1 + int(rp.integers(0, 2))
                # the copies of this parcel take the matched invoices in order, after any earlier parcel of the line
                skip, left = offset, rec
                for inv, take, pr in match:
                    avail = take - min(skip, take)
                    skip = max(0, skip - take)
                    t = min(left, avail)
                    if t <= 0:
                        continue
                    credits.append((cr_no, cday, aid, eid, t, inv, pr, ra, "RET"))
                    left -= t
                    if left == 0:
                        break
    # claims for copies damaged in transit: credited against the invoice, never a return
    rd = K.rng("transit")
    for (inv, wk, wd, aid, eid, q, pr) in invoices:
        if rd.random() < 0.004 and acc_by[aid].terms == "SOR":
            cday = 7 * wk + wd + int(rd.integers(5, 22))
            while (K.DAY0 + dt.timedelta(days=cday)).weekday() >= 5:
                cday += 1
            cr_no += 1 + int(rd.integers(0, 2))
            credits.append((cr_no, cday, aid, eid, int(min(q, rd.integers(1, 5))), inv, pr, None, "DIT"))
    credits.sort(key=lambda c: (c[1], c[0]))
    W_ = World(works, eds, A, invoices, returns, receipts, credits, panel, exp_sales, {})
    W_.deliveries = deliveries
    W_.params = dict(n_editions=n_e, n_accounts=len(A))
    return W_
