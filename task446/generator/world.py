"""task446 world (architecture 2).

Halstow Bank plc's corporate and commercial obligor groups from 2020 to 30 September 2026: the legal
entities in each group and their GLEIF records, the early-warning engine's month-end entity signals,
the watch-list history, and the facility book at 30 September 2026.

The four closed cohorts are built to fixed counts (monitored, reaching the watch list, flagged and
reaching, flagged and not reaching) and the 30 September 2026 book to a fixed size, flagged count and
exposure-band composition. Everything else is drawn from numpy default_rng(SEED). Nothing here reads
target/.
"""
import datetime as dt
import string
import numpy as np

SEED = 4462
D = dt.date
COHORTS = [D(2022, 9, 30), D(2023, 9, 30), D(2024, 9, 30), D(2025, 9, 30), D(2026, 9, 30)]
N_TARGET = [846, 871, 889, 902, 913]
P_REACH = [75, 43, 36, 47]
TP_FLAG = [58, 32, 28, 39]
FP_FLAG = [61, 66, 67, 65]
F_FWD = 165
EXTRACT_DATE = D(2026, 9, 30)
GAP = 8                       # no lifecycle date within this many days of a cohort date
BAND_EDGES = [5e6, 15e6, 40e6, 100e6]
BAND_LABELS = ["Under GBP 5m", "GBP 5m and under 15m", "GBP 15m and under 40m",
               "GBP 40m and under 100m", "GBP 100m and over"]
FX = {"GBP": 1.0, "EUR": 1.1534, "USD": 1.3487}     # units of currency per GBP 1 at 30 Sep 2026
ALNUM = string.ascii_uppercase + string.digits
LOUS = {"GB": "213800WAVVOPS85N2205", "IE": "635400AKJBGNS5WNQL34", "NL": "724500PMK2A2M1SQQ228",
        "DE": "529900T8BM49AURSDO55", "US": "5493001KJTIIGC8Y1R12", "LU": "222100T6ICDIY8V4VX70"}


def month_ends(start, end):
    out = []
    y, m = start.year, start.month
    while True:
        nxt = D(y + (m == 12), m % 12 + 1, 1)
        me = nxt - dt.timedelta(days=1)
        if me > end:
            break
        if me >= start:
            out.append(me)
        y, m = nxt.year, nxt.month
    return out


MONTHS = month_ends(D(2022, 9, 1), D(2026, 9, 30))       # 49 publications


def lei_check(body18):
    num = int("".join(str(int(c, 36)) for c in body18 + "00"))
    return "%02d" % (98 - num % 97)


def make_lei(rng, prefix, used):
    while True:
        body = prefix + "00" + "".join(rng.choice(list(ALNUM), 12))
        lei = body + lei_check(body)
        if lei not in used:
            used.add(lei)
            return lei


def near_cohort(d):
    return any(abs((d - c).days) <= GAP for c in COHORTS)


def window_of(d):
    """index c such that d lies in (COHORTS[c], COHORTS[c+1]]"""
    for c in range(4):
        if COHORTS[c] < d <= COHORTS[c + 1]:
            return c
    return None


# ------------------------------------------------------------------ names
PLACE = """Abberley Alston Arncliffe Askern Aynho Bainton Barlaston Beckley Bilsdale Blakeney Bolney Brackley
Brantham Brockhall Bulwick Burnside Calder Carlby Catterick Chalford Chesham Claydon Colwall Corbridge
Cowley Crantock Dalham Denby Dinton Dunsford Eastry Edgworth Elsham Epworth Exning Fairlie Felbrigg Finedon
Fordham Frampton Gainford Garstang Glenfield Goring Grayrigg Greystoke Hadlow Halsall Harbury Hartwith
Hawkshead Helmsley Heslington Hinton Holme Horton Hunmanby Ilmington Ingham Kelling Kemble Keswick Kilham
Kingsley Kirtling Lamport Langley Laxton Ledbury Leven Linton Litcham Lockton Lydden Malham Marden Melbury
Meriden Middleham Milton Moreton Mursley Nafferton Newholm Norley Oakley Ockham Orford Otterburn Overton
Painswick Pateley Pelton Pilling Polesden Preston Purley Quarndon Radwell Rampton Redbourn Ribston Ripley
Rodmell Roxby Rufford Ryedale Sandon Scalby Selside Shapwick Sherburn Shipton Sibford Skelton Snettisham
Sowerby Stainton Stanwick Stockley Studley Sutterton Swanton Tadmarton Tarporley Thoresby Thornton Tilney
Toddington Treswell Tunstall Upton Walcote Walsham Warcop Wathall Welford Westcott Whalton Whitwell
Wickham Willoughby Winster Wollaton Wragby Wykeham Yalding Yoxall""".split()
SECTORS = [  # code, description, name words
    ("RE", "Real estate and construction", ["Developments", "Estates", "Construction", "Homes", "Property"]),
    ("CL", "Consumer, retail and leisure", ["Retail", "Leisure", "Hotels", "Foods", "Brewing", "Stores"]),
    ("IN", "Industrials and manufacturing", ["Engineering", "Plastics", "Metals", "Packaging", "Fabrication"]),
    ("TL", "Transport, logistics and wholesale", ["Logistics", "Haulage", "Distribution", "Freight", "Wholesale"]),
    ("BS", "Business services and technology", ["Software", "Consulting", "Facilities", "Data", "Print"]),
    ("HC", "Healthcare and care", ["Care", "Healthcare", "Pharmacy", "Clinics", "Dental"]),
]
SECTOR_W = [0.21, 0.17, 0.19, 0.15, 0.18, 0.10]
SUB_SUFFIX = ["Ltd", "Ltd", "Ltd", "Limited", "Services Ltd", "Operations Ltd", "UK Ltd", "Trading Ltd"]


class Ent:
    __slots__ = ("eid", "gid", "lei", "crn", "name", "country", "category", "role", "parent", "borrower",
                 "cust", "reg", "reg_status", "successor", "merged_on", "joined", "lower_key", "repex",
                 "direct_only", "vendor_name", "inert", "hz", "cust_since")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


class Group:
    def __init__(self, gid, name, sector, active_from):
        self.gid = gid
        self.name = name
        self.sector = sector
        self.active_from = active_from
        self.active_to = None
        self.members = []          # Ent
        self.episodes = []         # dict(start, end, level, reason)
        self.flag = {}             # cohort index -> bool
        self.carriers = {}         # cohort index -> [eid]
        self.band = None
        self.exposure = None       # GBP target at 30 Sep 2026
        self.coverage = None
        self.officer = None


class World:
    def __init__(self):
        self.rng = np.random.default_rng(SEED)
        self.used_lei = set()
        self.used_crn = set()
        self.groups = {}
        self.ents = {}
        self.signals = []          # (date, ent, colour, score, triggers)
        self.facilities = []
        self._gseq = 104117
        self._cseq = 2203411
        self._eseq = 0
        self._case = 50311

    # ---------------------------------------------------------- dates
    def rand_date(self, lo, hi):
        """uniform date in [lo, hi] avoiding the cohort neighbourhoods"""
        span = (hi - lo).days
        for _ in range(500):
            d = lo + dt.timedelta(days=int(self.rng.integers(0, span + 1)))
            if not near_cohort(d):
                return d
        raise RuntimeError("no date")

    # ---------------------------------------------------------- entities
    def new_crn(self):
        while True:
            c = "%08d" % int(self.rng.integers(1500000, 14999999))
            if c not in self.used_crn:
                self.used_crn.add(c)
                return c

    def new_ent(self, g, name, role, country="GB", parent=None, with_lei=True, category="GENERAL", joined=None):
        self._eseq += 1
        rng = self.rng
        lei = make_lei(rng, LOUS[country][:4], self.used_lei) if with_lei else None
        crn = self.new_crn() if country == "GB" else None
        reg = D(2012, 6, 1) + dt.timedelta(days=int(rng.integers(0, 3300)))
        e = Ent(eid=self._eseq, gid=g.gid, lei=lei, crn=crn, name=name, country=country, category=category,
                role=role, parent=parent, borrower=False, cust=None, reg=reg, reg_status="ISSUED",
                successor=None, merged_on=None, joined=joined, lower_key=False, repex=None,
                direct_only=False, vendor_name=name, inert=False)
        self.ents[e.eid] = e
        g.members.append(e)
        return e

    def new_cust(self):
        self._cseq += int(self.rng.integers(3, 61))
        return "HB%07d" % self._cseq

    def new_group(self, active_from, sector=None):
        rng = self.rng
        self._gseq += int(rng.integers(2, 29))
        gid = "G%06d" % self._gseq
        if sector is None:
            sector = int(rng.choice(len(SECTORS), p=SECTOR_W))
        word = str(rng.choice(SECTORS[sector][2]))
        place = str(rng.choice(PLACE))
        top_name = f"{place} {word} Group plc" if rng.random() < 0.45 else f"{place} {word} Holdings Ltd"
        g = Group(gid, top_name, sector, active_from)
        self.groups[gid] = g
        top = self.new_ent(g, top_name, "top")
        n_sub = int(min(7, rng.poisson(1.6)))
        hold = None
        if n_sub >= 3 and rng.random() < 0.35:
            hold = self.new_ent(g, f"{place} {word} Holdings (UK) Ltd", "hold", parent=top.eid)
        for k in range(n_sub):
            country = "GB"
            if rng.random() < 0.10:
                country = "IE"
            elif rng.random() < 0.04:
                country = str(rng.choice(["NL", "DE"]))
            nm_place = place if rng.random() < 0.7 else str(rng.choice(PLACE))
            if country == "IE":
                nm = f"{nm_place} {word} Ireland {'DAC' if rng.random() < 0.6 else 'Limited'}"
            elif country == "NL":
                nm = f"{nm_place} {word} B.V."
            elif country == "DE":
                nm = f"{nm_place} {word} GmbH"
            else:
                nm = f"{nm_place} {rng.choice(SECTORS[sector][2])} {rng.choice(SUB_SUFFIX)}"
            par = hold.eid if (hold is not None and rng.random() < 0.6) else top.eid
            with_lei = True if country != "GB" else (rng.random() < 0.86)
            self.new_ent(g, nm, "sub", country=country, parent=par, with_lei=with_lei)
        # borrowers: the top with p 0.55, each other entity with p 0.5, at least one
        for e in g.members:
            if (e.role == "top" and rng.random() < 0.55) or (e.role != "top" and rng.random() < 0.5):
                e.borrower = True
        if not any(e.borrower for e in g.members):
            cand = [e for e in g.members if e.role != "hold"]
            cand[int(rng.integers(0, len(cand)))].borrower = True
        for e in g.members:
            if e.borrower:
                e.cust = self.new_cust()
        g.coverage = str(rng.choice(["Mid Corporate North", "Mid Corporate South", "Commercial Midlands",
                                     "Commercial London", "Large Corporate", "Commercial Scotland"]))
        g.officer = "".join(rng.choice(list(string.ascii_uppercase), 2))
        return g

    # ---------------------------------------------------------- state
    def active(self, g, d):
        return g.active_from <= d and (g.active_to is None or g.active_to > d)

    def on_list(self, g, d):
        return any(ep["start"] <= d and (ep["end"] is None or ep["end"] > d) for ep in g.episodes)

    def monitored(self, d):
        return [g for gid, g in sorted(self.groups.items()) if self.active(g, d) and not self.on_list(g, d)]

    def add_episode(self, g, start, reason=None, end=None):
        self._case += int(self.rng.integers(1, 9))
        g.episodes.append(dict(case="WL%06d" % self._case, start=start, end=end, reason=reason,
                               level=int(self.rng.choice([1, 2, 3], p=[0.55, 0.32, 0.13]))))
        return g.episodes[-1]


# ====================================================================== build
def resolve_episode(w, g, ep, horizon=EXTRACT_DATE):
    """Draw how a watch-list case ends. Ends after the extract date stay open."""
    rng = w.rng
    u = rng.random()
    start = ep["start"]
    if u < 0.45:
        reason, lo, hi = "CURED", 170, 640
    elif u < 0.65:
        reason, lo, hi = "REFINANCED_AWAY", 60, 420
    elif u < 0.85:
        reason, lo, hi = "TO_RECOVERY", 120, 520
    else:
        reason, lo, hi = None, None, None
    if reason is None:
        return
    end = start + dt.timedelta(days=int(rng.integers(lo, hi)))
    if end >= horizon - dt.timedelta(days=GAP):
        return
    if near_cohort(end):
        end = end + dt.timedelta(days=2 * GAP + 1)
        if end >= horizon - dt.timedelta(days=GAP):
            return
    ep["end"], ep["reason"] = end, reason
    if reason in ("REFINANCED_AWAY", "TO_RECOVERY"):
        g.active_to = end


def build_lifecycle(w):
    rng = w.rng
    c0 = COHORTS[0]
    # groups monitored at the first cohort date
    for _ in range(N_TARGET[0]):
        g = w.new_group(w.rand_date(D(2006, 1, 1), c0 - dt.timedelta(days=40)))
    # a few with an earlier, closed watch-list episode
    mon0 = [gid for gid in sorted(w.groups) if w.groups[gid].active_from < D(2021, 6, 1)]
    for gid in rng.choice(mon0, 58, replace=False):
        g = w.groups[str(gid)]
        st = w.rand_date(max(g.active_from, D(2020, 1, 15)), D(2021, 12, 31))
        en = st + dt.timedelta(days=int(rng.integers(160, 520)))
        if en >= c0 - dt.timedelta(days=GAP):
            en = c0 - dt.timedelta(days=int(rng.integers(20, 60)))
        if en <= st + dt.timedelta(days=60):
            continue
        ep = w.add_episode(g, st, reason="CURED", end=en)
    # groups on the watch list at the first cohort date
    for _ in range(33):
        g = w.new_group(w.rand_date(D(2006, 1, 1), D(2020, 6, 30)))
        st = w.rand_date(D(2021, 3, 1), c0 - dt.timedelta(days=20))
        ep = w.add_episode(g, st)
        resolve_episode(w, g, ep)
        if ep["end"] is not None and ep["end"] <= c0 + dt.timedelta(days=GAP):
            ep["end"] = w.rand_date(c0 + dt.timedelta(days=30), c0 + dt.timedelta(days=420))
            if ep["reason"] in ("REFINANCED_AWAY", "TO_RECOVERY"):
                g.active_to = ep["end"]
    # groups that left before the first cohort date (they appear in the register and the history)
    for _ in range(64):
        g = w.new_group(w.rand_date(D(2006, 1, 1), D(2019, 12, 31)))
        g.active_to = w.rand_date(D(2020, 2, 1), c0 - dt.timedelta(days=30))
        if rng.random() < 0.3 and g.active_to > D(2020, 6, 1):
            st = w.rand_date(D(2020, 1, 15), g.active_to - dt.timedelta(days=60))
            w.add_episode(g, st, reason="TO_RECOVERY", end=g.active_to)

    cohort = {}
    for c in range(4):
        d, nd = COHORTS[c], COHORTS[c + 1]
        M = w.monitored(d)
        assert len(M) == N_TARGET[c], (c, len(M))
        idx = rng.permutation(len(M))
        reach = [M[i] for i in sorted(idx[:P_REACH[c]])]
        rest = [M[i] for i in sorted(idx[P_REACH[c]:])]
        for g in reach:
            st = w.rand_date(d + dt.timedelta(days=GAP + 1), nd - dt.timedelta(days=GAP + 1))
            ep = w.add_episode(g, st)
            resolve_episode(w, g, ep)
        # leavers (repaid, refinanced, sold) without a watch-list case
        nleave = int(round(len(rest) * rng.uniform(0.047, 0.058)))
        for i in sorted(rng.choice(len(rest), nleave, replace=False)):
            rest[i].active_to = w.rand_date(d + dt.timedelta(days=GAP + 1), nd - dt.timedelta(days=GAP + 1))
        # flags at the cohort date
        tp = set(rng.choice([g.gid for g in reach], TP_FLAG[c], replace=False))
        fp = set(rng.choice([g.gid for g in rest], FP_FLAG[c], replace=False))
        for g in M:
            g.flag[c] = g.gid in tp or g.gid in fp
        cohort[c] = dict(M=[g.gid for g in M], reach=[g.gid for g in reach])
        # joiners during the window, to the next cohort's size
        prov = len(w.monitored(nd))
        need = N_TARGET[c + 1] - prov
        assert need > 0, (c, need)
        for _ in range(need):
            w.new_group(w.rand_date(d + dt.timedelta(days=GAP + 1), nd - dt.timedelta(days=40)))
    M4 = w.monitored(COHORTS[4])
    assert len(M4) == N_TARGET[4], len(M4)
    cohort[4] = dict(M=[g.gid for g in M4], reach=None)
    return cohort


# ------------------------------------------------------------------ GLEIF texture
def gleif_texture(w, cohort):
    """Lapsed registrations, merged entities, branches, funds, reporting exceptions, LEIs keyed in
    lower case by one vendor feed. Every entity given texture is marked inert: it never carries a
    signal other than GREEN in a September publication."""
    rng = w.rng
    ents = [w.ents[k] for k in sorted(w.ents)]
    lei_ents = [e for e in ents if e.lei]
    # lapsed registrations
    for e in rng.choice(lei_ents, 260, replace=False):
        e.reg_status = "LAPSED"
        e.inert = True
    # entities that reported only their direct parent
    subs = [e for e in lei_ents if e.role == "sub"]
    for e in rng.choice(subs, 140, replace=False):
        e.direct_only = True
        e.inert = True
    # merged entities: a subsidiary merged into a sister during 2024 or 2025, still keyed by the vendor
    cand = [g for gid, g in sorted(w.groups.items()) if sum(1 for m in g.members if m.role == "sub" and m.lei) >= 2
            and w.active(g, D(2025, 12, 31))]
    for g in rng.choice(cand, 26, replace=False):
        subs_g = [m for m in g.members if m.role == "sub" and m.lei]
        a, b = subs_g[0], subs_g[1]
        a.reg_status = "RETIRED"
        a.successor = b.eid
        a.merged_on = w.rand_date(D(2024, 1, 15), D(2025, 11, 15))
        a.inert = True
        if a.borrower:
            # its facilities and customer move to the successor
            if not b.borrower:
                b.borrower = True
                b.cust = w.new_cust()
            a.borrower = False
    # international branches of the top entity (Ireland, the Netherlands)
    for g in rng.choice([g for gid, g in sorted(w.groups.items())], 30, replace=False):
        top = g.members[0]
        cc = "IE" if rng.random() < 0.7 else "NL"
        e = w.new_ent(g, f"{top.name} ({'Dublin' if cc == 'IE' else 'Amsterdam'} Branch)", "branch", country=cc,
                      parent=top.eid, category="BRANCH")
        e.inert = True
    # funds managed by an asset-management subsidiary (fund-management, not consolidation)
    for g in rng.choice([g for gid, g in sorted(w.groups.items()) if g.sector == 4], 12, replace=False):
        top = g.members[0]
        mgr = w.new_ent(g, top.name.split(" ")[0] + " Asset Management Ltd", "sub", parent=top.eid)
        mgr.inert = True
        for k in range(int(rng.integers(1, 4))):
            f = w.new_ent(g, f"{top.name.split(' ')[0]} {['Income', 'Growth', 'Property', 'Strategic'][k]} Fund",
                          "fund", parent=mgr.eid, category="FUND")
            f.inert = True
    # reporting exceptions on top entities owned by individuals or not consolidating
    tops = [g.members[0] for gid, g in sorted(w.groups.items())]
    for e in rng.choice(tops, 210, replace=False):
        e.repex = str(rng.choice(["NATURAL_PERSONS", "NON_CONSOLIDATING", "NO_KNOWN_PERSON"], p=[0.62, 0.28, 0.10]))
    # one vendor feed sends some LEIs in lower case
    for e in rng.choice(lei_ents, 90, replace=False):
        e.lower_key = True
        e.inert = True
    # vendor spellings
    for e in ents:
        r = rng.random()
        if r < 0.12:
            e.vendor_name = e.name.upper()
        elif r < 0.18:
            e.vendor_name = e.name.replace(" Ltd", " Limited") if " Ltd" in e.name else e.name.replace(" plc", " PLC")
        elif r < 0.21:
            e.vendor_name = e.name.replace(" & ", " and ")


# ------------------------------------------------------------------ signals
GREEN_TRIG = ""
AMBER_TRIG = ["PAY_DELAY", "FILING_LATE", "RATING_WATCH", "CCJ", "COVENANT_RISK", "ADVERSE_NEWS", "SECTOR_STRESS",
              "DIRECTOR_CHANGE"]
RED_TRIG = ["PAY_DEFAULT", "RATING_DOWN", "WINDING_UP_PETITION", "GOING_CONCERN", "COVENANT_BREACH"]


def pick_carriers(w, g, c):
    """Which members carry a flag at cohort c: an entity whose group the standard's rules reach however the
    GLEIF texture is read (a non-inert borrower, or a non-borrower with an LEI under a chain of ISSUED
    registrations), usually a borrower."""
    rng = w.rng
    top = g.members[0]

    def chain_issued(e):
        x = e
        for _ in range(6):
            if x.reg_status != "ISSUED" or x.direct_only:
                return False
            if x.parent is None:
                return True
            x = w.ents[x.parent]
        return False

    def ok_entity(e):
        if e.inert or e.role not in ("top", "sub", "hold"):
            return False
        if e.joined is not None and e.joined >= COHORTS[c] - dt.timedelta(days=GAP):
            return False
        if e.borrower:
            return True
        return bool(e.lei) and chain_issued(e)

    live = [e for e in g.members if ok_entity(e)]
    if not live:
        top.reg_status, top.lower_key, top.direct_only, top.inert = "ISSUED", False, False, False
        live = [e for e in g.members if ok_entity(e)]
    borrowers = [e for e in live if e.borrower]
    others = [e for e in live if not e.borrower]
    crn_only = [e for e in borrowers if not e.lei]
    u = rng.random()
    if others and u < 0.11:
        lead = others[int(rng.integers(0, len(others)))]
    elif crn_only and u < 0.20:
        lead = crn_only[int(rng.integers(0, len(crn_only)))]
    else:
        pool = borrowers or live
        lead = pool[int(rng.integers(0, len(pool)))]
    out = [lead]
    rest = [e for e in live if e is not lead]
    if rest and rng.random() < 0.3:
        out.append(rest[int(rng.integers(0, len(rest)))])
    return out


def build_signals(w, cohort):
    """Month-end signals per entity. September publications follow the cohort design exactly; other
    months follow episodes around it."""
    rng = w.rng
    state = {}   # (eid, month) -> (colour, triggers)

    def mark(e, m, colour):
        key = (e.eid, m)
        cur = state.get(key)
        if cur is not None and cur == "RED":
            return
        state[key] = colour

    def months_between(a, b):
        return [m for m in MONTHS if a <= m <= b]

    sept_idx = {COHORTS[c]: c for c in range(5)}
    for gid, g in sorted(w.groups.items()):
        for c in range(5):
            d = COHORTS[c]
            if c < 4 and gid not in cohort[c]["reach"] and not g.flag.get(c, False):
                continue
            if c == 4 and not g.flag.get(4, False):
                continue
            if not w.active(g, d):
                continue
            car = pick_carriers(w, g, c)
            g.carriers[c] = [e.eid for e in car]
            entry = None
            if c < 4 and gid in cohort[c]["reach"]:
                entry = [ep for ep in g.episodes if COHORTS[c] < ep["start"] <= COHORTS[c + 1]][0]["start"]
            flagged = g.flag.get(c, False)
            if flagged:
                k0 = int(rng.integers(0, 5))
                start = MONTHS[max(0, MONTHS.index(d) - k0)]
                if entry is not None:
                    stop = entry + dt.timedelta(days=int(rng.integers(20, 75)))
                else:
                    stop = d + dt.timedelta(days=31 * int(rng.integers(0, 6)))
                    if c < 4:
                        stop = min(stop, COHORTS[c + 1] - dt.timedelta(days=40))
                for m in months_between(start, stop):
                    if m in sept_idx and m != d:
                        continue
                    colour = "RED" if (entry is not None and m >= entry - dt.timedelta(days=75)) or \
                        rng.random() < 0.28 else "AMBER"
                    mark(car[0], m, colour)
                    if len(car) > 1 and m >= d - dt.timedelta(days=40):
                        mark(car[1], m, "AMBER")
            else:
                # reaches the list but was green at the cohort date: the signal comes after
                first = d + dt.timedelta(days=31 * int(rng.integers(1, 4)))
                for m in months_between(first, entry + dt.timedelta(days=40)):
                    if m in sept_idx:
                        continue
                    if m <= d:
                        continue
                    mark(car[0], m, "RED" if m >= entry - dt.timedelta(days=60) else "AMBER")
        # watch-list episodes: red or amber while on the list, outside cohort Septembers handled below
        for ep in g.episodes:
            lead = [e for e in g.members if not e.inert and e.role in ("top", "sub", "hold")]
            if not lead:
                continue
            e0 = lead[0]
            stop = ep["end"] or EXTRACT_DATE
            for m in months_between(ep["start"], stop):
                if m in sept_idx and not w.on_list(g, m):
                    continue
                if rng.random() < 0.85:
                    mark(e0, m, "RED" if ep["level"] >= 2 else "AMBER")
        # occasional amber blips in non-September months
        if rng.random() < 0.16:
            live = [e for e in g.members if e.role in ("top", "sub", "hold")]
            e = live[int(rng.integers(0, len(live)))]
            m0 = int(rng.integers(0, len(MONTHS)))
            for m in MONTHS[m0:m0 + int(rng.integers(1, 3))]:
                if m in sept_idx:
                    continue
                mark(e, m, "AMBER")

    # emit rows
    rows = []
    for gid, g in sorted(w.groups.items()):
        cov_from = max(g.active_from, D(2022, 9, 1))
        cov_to = EXTRACT_DATE if g.active_to is None else min(EXTRACT_DATE, g.active_to + dt.timedelta(days=45))
        for e in g.members:
            for m in MONTHS:
                if m < cov_from - dt.timedelta(days=31) or m > cov_to:
                    continue
                if e.joined is not None and m < e.joined:
                    continue
                if e.merged_on is not None and m > e.merged_on + dt.timedelta(days=70):
                    continue
                colour = state.get((e.eid, m), "GREEN")
                if m in sept_idx and e.inert:
                    colour = "GREEN"
                rows.append((m, e, colour))
    # September publications for groups outside their September role are green unless on the list
    out = []
    for m, e, colour in rows:
        g = w.groups[e.gid]
        if m in sept_idx:
            c = sept_idx[m]
            if w.active(g, m) and not w.on_list(g, m):
                want = g.flag.get(c, False)
                if not want:
                    colour = "GREEN"
                else:
                    if e.eid not in g.carriers.get(c, []):
                        colour = "GREEN"
                    elif colour == "GREEN":
                        colour = "AMBER"
        if colour == "GREEN":
            score = int(rng.integers(6, 40))
            trig = ""
        elif colour == "AMBER":
            score = int(rng.integers(40, 70))
            k = int(rng.integers(1, 3))
            pool = AMBER_TRIG
            p = None
            if m >= D(2026, 4, 1):
                p = np.array([0.30, 0.08, 0.20, 0.08, 0.12, 0.06, 0.12, 0.04])
                p = p / p.sum()
            trig = ";".join(sorted(rng.choice(pool, k, replace=False, p=p)))
        else:
            score = int(rng.integers(70, 98))
            k = int(rng.integers(1, 3))
            trig = ";".join(sorted(set(list(rng.choice(RED_TRIG, k, replace=False)) +
                                       ([str(rng.choice(AMBER_TRIG))] if rng.random() < 0.5 else []))))
        out.append((m, e, colour, score, trig))
    w.signals = out


# ------------------------------------------------------------------ bands and the forward flags
def ppv_m1():
    P, TP, FP = map(np.array, (P_REACH, TP_FLAG, FP_FLAG))
    Ns = np.array(N_TARGET[:4])
    se = TP.sum() / P.sum()
    f = FP.sum() / (Ns - P).sum()
    a1 = F_FWD / N_TARGET[4]
    p1 = (a1 - f) / (se - f)
    return se * p1 / a1, (1 - se) * p1 / (1 - a1)


def bin_margin(x, step=0.1):
    y = x / step
    return 0.5 - abs(y - round(y))


def band_plan():
    """Band composition of the 30 Sep 2026 book: groups and flagged groups per band, chosen so every
    expected-arrival figure sits well inside its one-decimal bin."""
    PPV1, M1 = ppv_m1()
    base_n = [205, 300, 248, 118, 42]
    base_f = [34, 54, 46, 22, 9]
    best = None
    for dn in [(a, b, c, d) for a in range(-6, 7, 2) for b in range(-6, 7, 2) for c in range(-6, 7, 2)
               for d in range(-4, 5, 2)]:
        n = [base_n[0] + dn[0], base_n[1] + dn[1], base_n[2] + dn[2], base_n[3] + dn[3]]
        n.append(N_TARGET[4] - sum(n))
        for df in [(a, b, c, d) for a in range(-2, 3) for b in range(-2, 3) for c in range(-2, 3) for d in range(-2, 3)]:
            fl = [base_f[i] + df[i] for i in range(4)]
            fl.append(F_FWD - sum(fl))
            if fl[4] < 6 or fl[4] > 12:
                continue
            u = [n[i] - fl[i] for i in range(5)]
            ms = [bin_margin(fl[i] * PPV1) for i in range(5)] + [bin_margin(u[i] * M1) for i in range(5)]
            m = min(ms)
            key = (round(m, 3), -sum(abs(x) for x in dn) - sum(abs(x) for x in df))
            if best is None or key > best[0]:
                best = (key, n, fl)
    return best[1], best[2]


BAND_N = [201, 306, 250, 120, 36]     # band_plan() result, fixed here; checks.py re-derives the margins
BAND_F = [34, 54, 47, 20, 10]


def assign_bands_and_flags(w, cohort):
    rng = w.rng
    n, fl = list(BAND_N), list(BAND_F)
    M4 = [w.groups[g] for g in cohort[4]["M"]]
    order = rng.permutation(len(M4))
    pos = 0
    for b in range(5):
        chosen = [M4[i] for i in order[pos:pos + n[b]]]
        pos += n[b]
        fset = set(rng.choice(len(chosen), fl[b], replace=False))
        for i, g in enumerate(chosen):
            g.band = b
            g.flag[4] = i in fset
    w.band_n, w.band_f = n, fl




# ------------------------------------------------------------------ facilities at 30 Sep 2026
# The loan platforms stamp limit versions in UTC. The start-of-day batch runs at 00:30 UK time, so in BST it
# stamps 23:30Z on the previous date. The end of 30 September 2026 UK time is 23:00Z.
T_END = dt.datetime(2026, 9, 30, 23, 0, 0)
SOD_1OCT = dt.datetime(2026, 9, 30, 23, 30, 0)
EXTRACT_RUN = dt.datetime(2026, 10, 1, 0, 15, 0)       # 01:15 BST on 1 October
USERS = ["mryan", "jpage", "jali", "rhussain", "ewilliams", "vpratt", "banderson", "dbishop", "dfoster"]


def last_sunday(y, m):
    d = D(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else D(y, 12, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def is_bst(d):
    return last_sunday(d.year, 3) <= d < last_sunday(d.year, 10)


def sod_stamp(d):
    """the start-of-day batch for UK date d, in UTC"""
    t = dt.datetime(d.year, d.month, d.day, 0, 30, 0)
    return t - dt.timedelta(hours=1) if is_bst(d) else t


def user_stamp(rng, d):
    """a limit keyed by a user during the UK working day of d, in UTC"""
    t = dt.datetime(d.year, d.month, d.day, int(rng.integers(8, 18)), int(rng.integers(0, 60)), int(rng.integers(0, 60)))
    return t - dt.timedelta(hours=1) if is_bst(d) else t


class Fac:
    __slots__ = ("fid", "booking", "product", "ccy", "limit", "obligors", "start", "maturity", "status", "drawn",
                 "booked", "oct1", "sep30", "later", "dev", "closed_on", "history")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))
        if self.obligors is None:
            self.obligors = []
        if self.dev is None:
            self.dev = set()
        if self.later is None:
            self.later = []
        self.oct1 = self.oct1 or 0.0
        self.sep30 = self.sep30 or 0.0


def band_of(x):
    for i, e in enumerate(BAND_EDGES):
        if x < e:
            return i
    return 4


def edge_dist(x):
    return min(abs(x - e) for e in BAND_EDGES)


def round_limit(x):
    """committed limits are set in round amounts"""
    if x >= 20e6:
        step = 500000
    elif x >= 5e6:
        step = 250000
    elif x >= 1e6:
        step = 50000
    else:
        step = 25000
    return max(step, round(x / step) * step)


def in_force(f):
    return f.start <= EXTRACT_DATE < f.maturity


def fac_value(f, clock="right"):
    """the facility's committed limit under a reading of the limit clock, in its currency"""
    if clock == "right":
        v = f.limit
    elif clock in ("B1", "B2"):
        v = f.limit + f.oct1
    elif clock == "B3":
        v = f.later[-1][1] if f.later else f.limit + f.oct1
    elif clock == "B0":
        v = f.limit - f.sep30
    else:
        raise ValueError(clock)
    return v


def fac_groups(w, f, grain="group", hz=True):
    cnt = {}
    for eid in f.obligors:
        e = w.ents[eid]
        if e.hz and not hz:
            continue
        cnt[e.gid] = cnt.get(e.gid, 0) + 1
    if grain != "rows":
        cnt = {k: 1 for k in cnt}
    return cnt


def gexp(w, g, clock="right", grain="group", hz=True):
    tot = 0.0
    for f in w.gfacs.get(g.gid, []):
        if not in_force(f):
            continue
        k = fac_groups(w, f, grain, hz).get(g.gid, 0)
        tot += k * fac_value(f, clock) / FX[f.ccy]
    return tot


def exposure(w, clock="right", grain="group", hz=True):
    out = {}
    for f in w.facilities:
        if not in_force(f):
            continue
        v = fac_value(f, clock) / FX[f.ccy]
        for gid, k in fac_groups(w, f, grain, hz).items():
            out[gid] = out.get(gid, 0.0) + k * v
    return out


def add_fac(w, f):
    w.facilities.append(f)
    for gid in {w.ents[e].gid for e in f.obligors}:
        w.gfacs.setdefault(gid, [])
        if f not in w.gfacs[gid]:
            w.gfacs[gid].append(f)


def drop_fac(w, f):
    w.facilities.remove(f)
    for lst in w.gfacs.values():
        if f in lst:
            lst.remove(f)


def booking_of(e):
    return "HB-DAC" if e.country == "IE" else "HB-PLC"


def ccy_of(rng, e):
    if e.country == "IE" or e.country in ("NL", "DE"):
        return "EUR"
    r = rng.random()
    return "USD" if r < 0.05 else ("EUR" if r < 0.10 else "GBP")


def build_facilities(w, cohort):
    rng = w.rng
    lo_hi = [(0.4e6, 4.6e6), (5.4e6, 14.6e6), (15.6e6, 39.2e6), (41e6, 98e6), (104e6, 260e6)]
    w.gfacs = {}
    live_groups = [g for gid, g in sorted(w.groups.items()) if w.active(g, EXTRACT_DATE)]
    for g in live_groups:
        if g.band is None:   # on the watch list at 30 Sep 2026
            g.band_hint = int(rng.choice(5, p=[0.2, 0.35, 0.28, 0.13, 0.04]))
            b = g.band_hint
        else:
            b = g.band
        lo, hi = lo_hi[b]
        target = lo * np.exp(rng.uniform(0, np.log(hi / lo))) if b == 4 else rng.uniform(lo, hi)
        borrowers = [e for e in g.members if e.borrower]
        k = int(min(6, 1 + rng.poisson(0.9 + 0.5 * b)))
        shares = rng.dirichlet(np.ones(k) * 1.6)
        owners = [borrowers[int(rng.integers(0, len(borrowers)))] for _ in range(k)]
        ccys = [ccy_of(rng, e) for e in owners]
        amounts = [round_limit(target * s * FX[c]) for s, c in zip(shares, ccys)]
        for _ in range(60):
            t = sum(x / FX[c] for x, c in zip(amounts, ccys))
            if lo + 0.25e6 <= t <= hi - 0.25e6:
                break
            j = int(np.argmax(amounts))
            amounts[j] = round_limit(amounts[j] * (lo + hi) / 2 / t)
        for i in range(k):
            e = owners[i]
            prod = str(rng.choice(["RCF", "TERM_LOAN", "OVERDRAFT", "TERM_LOAN", "ASSET_FINANCE", "RCF"]))
            if rng.random() < (0.25 if booking_of(e) == "HB-DAC" else 0.03):
                start = D(2026, 9, int(rng.integers(1, 22)))
            else:
                start = w.rand_date(max(D(2016, 1, 1), g.active_from), D(2026, 8, 31))
            mat = start + dt.timedelta(days=int(rng.integers(400, 2600)))
            if mat <= EXTRACT_DATE + dt.timedelta(days=20):
                mat = EXTRACT_DATE + dt.timedelta(days=int(rng.integers(40, 1500)))
            add_fac(w, Fac(booking=booking_of(e), product=prod, ccy=ccys[i], limit=float(amounts[i]), obligors=[e.eid],
                           start=start, maturity=mat, status="ACTIVE",
                           booked=start - dt.timedelta(days=int(rng.integers(0, 45 if start.year < 2026 or
                                                                              start.month < 9 else 7)))))
        # cancelled and closed facilities stay on the ledger with a nil limit
        if rng.random() < 0.10:
            e = borrowers[0]
            st = w.rand_date(D(2017, 1, 1), D(2024, 12, 31))
            status = str(rng.choice(["CANCELLED", "CLOSED"]))
            mat = st + dt.timedelta(days=1825)
            closed_on = mat if (status == "CLOSED" and mat <= D(2026, 8, 31)) else \
                w.rand_date(st + dt.timedelta(days=200), min(mat, D(2026, 8, 31)))
            if closed_on < st + dt.timedelta(days=60):
                closed_on = st + dt.timedelta(days=60)
            add_fac(w, Fac(booking="HB-PLC", product="RCF", ccy="GBP", limit=0.0, obligors=[e.eid], start=st,
                           maturity=mat, status=status, booked=st - dt.timedelta(days=int(rng.integers(0, 30))),
                           closed_on=closed_on, history=float(round_limit(rng.uniform(1e6, 12e6)))))
    w.live_groups = live_groups


# ------------------------------------------------------------------ ask devices
class Undo:
    def __init__(self):
        self.ops = []

    def set(self, obj, attr, val):
        self.ops.append(("set", obj, attr, getattr(obj, attr)))
        setattr(obj, attr, val)

    def add(self, w, f):
        add_fac(w, f)
        self.ops.append(("fac", f))

    def oblig(self, w, f, eid):
        f.obligors.append(eid)
        gid = w.ents[eid].gid
        new = f not in w.gfacs.setdefault(gid, [])
        if new:
            w.gfacs[gid].append(f)
        self.ops.append(("obl", f, eid, gid, new))

    def member(self, g, e, w):
        g.members.append(e)
        w.ents[e.eid] = e
        self.ops.append(("mem", g, e, w))

    def rollback(self, w):
        for op in reversed(self.ops):
            if op[0] == "set":
                setattr(op[1], op[2], op[3])
            elif op[0] == "fac":
                drop_fac(w, op[1])
            elif op[0] == "obl":
                _, f, eid, gid, new = op
                f.obligors.remove(eid)
                if new:
                    w.gfacs[gid].remove(f)
            elif op[0] == "mem":
                op[1].members.remove(op[2])
                del op[3].ents[op[2].eid]
        self.ops = []


def plain_facs(w, g):
    """facilities of g that carry nothing else: one obligor, in force, no device"""
    return [f for f in w.gfacs.get(g.gid, []) if in_force(f) and len(f.obligors) == 1 and not f.dev
            and f.status == "ACTIVE"]


def reduce_by(w, g, amount, u):
    """take about `amount` (GBP) off the group's plain facilities, largest first, keeping each above GBP 0.25m"""
    left = amount
    for f in sorted(plain_facs(w, g), key=lambda f: -f.limit / FX[f.ccy]):
        if left <= 0.05e6:
            break
        v = f.limit / FX[f.ccy]
        take = min(left, v - 0.3e6)
        if take <= 0.05e6:
            continue
        new = round((v - take) * FX[f.ccy] / 50000) * 50000
        u.set(f, "limit", float(new))
        left -= v - new / FX[f.ccy]
    return amount - left


def right_ok(w, g, clear=0.3e6):
    if g.band is None:
        return True
    e = gexp(w, g)
    return band_of(e) == g.band and edge_dist(e) >= clear and any(in_force(f) and fac_value(f) > 0
                                                                   for f in w.gfacs.get(g.gid, []))


def plant_devices(w, cohort):
    rng = w.drng
    M4 = [w.groups[g] for g in cohort[4]["M"]]
    used = set()                       # groups carrying a crosser for some device
    w.movers = {}
    width = [BAND_EDGES[i + 1] - BAND_EDGES[i] for i in range(3)] + [None]

    def up(g):
        return BAND_EDGES[g.band] - gexp(w, g) if g.band < 4 else None

    def down(g):
        return gexp(w, g) - BAND_EDGES[g.band - 1] if g.band > 0 else gexp(w, g)

    def pool(band, flag, key):
        c = [g for g in M4 if g.band == band and g.flag[4] == flag and g.gid not in used]
        c.sort(key=key)
        return c

    # ---------------------------------------------------------- HZ-C: customers not yet grouped
    hz_plan = [(1, True, 1), (1, False, 4), (2, True, 1), (2, False, 2)]      # (edge, flagged, count), down
    w.movers["HZ"] = []
    nseq = [0]

    def hz_entity(g, u):
        top = g.members[0]
        place, word = g.name.split(" ")[0], SECTORS[g.sector][2][0]
        nm = f"{place} {word} Ireland {'DAC' if rng.random() < 0.6 else 'Limited'}"
        joined = D(2026, int(rng.integers(2, 9)), int(rng.integers(1, 28)))
        w._eseq += 1
        e = Ent(eid=w._eseq, gid=g.gid, lei=make_lei(rng, LOUS["IE"][:4], w.used_lei), crn=None, name=nm, country="IE",
                category="GENERAL", role="sub", parent=top.eid, borrower=True, cust=None, reg=joined,
                reg_status="ISSUED", successor=None, merged_on=None, joined=joined, lower_key=False, repex=None,
                direct_only=False, vendor_name=nm, inert=True, hz=True,
                cust_since=D(2026, 9, int(rng.integers(1, 20))))
        w._hzseq += int(rng.integers(3, 25))
        e.cust = "HB%07d" % w._hzseq
        u.member(g, e, w)
        start = e.cust_since + dt.timedelta(days=int(rng.integers(0, 5)))
        return e, start

    def hz_ok_group(g):
        top = g.members[0]
        return top.lei and top.reg_status == "ISSUED" and not top.lower_key

    for edge, flag, cnt in hz_plan:
        got = 0
        for g in pool(edge + 1, flag, key=lambda g: down(g)):
            if got >= cnt:
                break
            if not hz_ok_group(g):
                continue
            u = Undo()
            L = down(g) + rng.uniform(0.4e6, 1.0e6)
            if L > 0.8 * gexp(w, g):
                continue
            e, start = hz_entity(g, u)
            eur = round(L * FX["EUR"] / 50000) * 50000
            red = reduce_by(w, g, eur / FX["EUR"], u)
            f = Fac(booking="HB-DAC", product=str(rng.choice(["RCF", "TERM_LOAN"])), ccy="EUR", limit=float(eur),
                    obligors=[e.eid], start=start, maturity=start + dt.timedelta(days=int(rng.integers(1095, 1826))),
                    status="ACTIVE", booked=max(e.cust_since, start - dt.timedelta(days=int(rng.integers(0, 4)))),
                    dev={"HZ"})
            u.add(w, f)
            if not right_ok(w, g) or band_of(gexp(w, g, hz=False)) != edge or \
                    edge_dist(gexp(w, g, hz=False)) < 0.2e6:
                u.rollback(w)
                continue
            used.add(g.gid)
            w.movers["HZ"].append(g.gid)
            got += 1
        assert got == cnt, ("HZ", edge, flag, got)
    # non-crossers, two in each outer band and two elsewhere
    for band, cnt in ((0, 2), (4, 2), (1, 1), (3, 1)):
        got = 0
        cands = [g for g in M4 if g.band == band and g.gid not in used and hz_ok_group(g)]
        for i in rng.permutation(len(cands)):
            if got >= cnt:
                break
            g = cands[int(i)]
            u = Undo()
            d0 = down(g)
            L = min(rng.uniform(0.3, 0.6) * gexp(w, g), d0 - 0.5e6, 9e6)
            if L < 0.3e6:
                continue
            e, start = hz_entity(g, u)
            eur = round(L * FX["EUR"] / 50000) * 50000
            reduce_by(w, g, eur / FX["EUR"], u)
            u.add(w, Fac(booking="HB-DAC", product=str(rng.choice(["RCF", "TERM_LOAN"])), ccy="EUR", limit=float(eur),
                         obligors=[e.eid], start=start,
                         maturity=start + dt.timedelta(days=int(rng.integers(1095, 1826))), status="ACTIVE",
                         booked=max(e.cust_since, start - dt.timedelta(days=int(rng.integers(0, 4)))), dev={"HZ"}))
            if not right_ok(w, g) or band_of(gexp(w, g, hz=False)) != band:
                u.rollback(w)
                continue
            used.add(g.gid)
            got += 1
        assert got == cnt, ("HZ nc", band, got)

    # ---------------------------------------------------------- DV-A: joint property facilities
    w.movers["A3"] = []
    re_live = [g for g in w.live_groups if g.sector == 0]

    def joint(gB, eB, L, u, want_cross, prefer_band=None):
        partners = [g for g in re_live if g.gid not in used and g is not gB]
        order_ = [partners[int(i)] for i in rng.permutation(len(partners))]

        def cross_last(g):
            # the partner drops a band when the extract is de-duplicated keeping the last row
            if g.band is None or g.band == 0:
                return False
            d = down(g)
            return 0.35e6 <= L - d and (g.band == 1 or L - d <= BAND_EDGES[g.band - 1] - BAND_EDGES[g.band - 2] - 0.35e6)
        if want_cross:
            order_ = [g for g in order_ if cross_last(g)] + [g for g in order_ if not cross_last(g)]
        elif prefer_band is not None:
            order_ = [g for g in order_ if g.band == prefer_band] + [g for g in order_ if g.band != prefer_band]
        for gA in order_:
            ea = [m for m in gA.members if m.borrower and not m.hz and m.cust < eB.cust]
            if not ea:
                continue
            eA = ea[0]
            if g_total := gexp(w, gA):
                if g_total < L + 1.0e6:
                    continue
            mark = len(u.ops)
            reduce_by(w, gA, L, u)
            reduce_by(w, gB, L, u)
            st = w.rand_date(D(2019, 1, 1), D(2026, 6, 30))
            f = Fac(booking="HB-PLC", product="TERM_LOAN", ccy="GBP", limit=float(L), obligors=[eA.eid, eB.eid],
                    start=st, maturity=st + dt.timedelta(days=int(rng.integers(1400, 2600))), status="ACTIVE",
                    booked=st - dt.timedelta(days=int(rng.integers(0, 30))), dev={"JOINT"})
            if f.maturity <= EXTRACT_DATE + dt.timedelta(days=60):
                f.maturity = EXTRACT_DATE + dt.timedelta(days=int(rng.integers(200, 900)))
            u.add(w, f)
            eB_loss = gexp(w, gB) - L
            okB = right_ok(w, gB) and (band_of(eB_loss) == gB.band - 1 if want_cross else
                                       band_of(eB_loss) == gB.band)
            if want_cross:
                okB = okB and edge_dist(eB_loss) >= 0.2e6
            if okB and right_ok(w, gA):
                return gA
            # undo this partner's part only
            tail = Undo()
            tail.ops = u.ops[mark:]
            tail.rollback(w)
            u.ops = u.ops[:mark]
        return None

    a3_plan = [(0, True, 1), (0, False, 2), (1, False, 1), (2, True, 1), (2, False, 2), (3, False, 1)]
    for edge, flag, cnt in a3_plan:
        got = 0
        for gB in pool(edge + 1, flag, key=lambda g: down(g)):
            if got >= cnt:
                break
            if gB.sector != 0:
                continue
            eb = [m for m in gB.members if m.borrower and not m.hz]
            eB = max(eb, key=lambda m: m.cust)
            u = Undo()
            L = float(round_limit(down(gB) + rng.uniform(0.5e6, 1.5e6)))
            gA = joint(gB, eB, L, u, True)
            if gA is None:
                continue
            used.update([gA.gid, gB.gid])
            w.movers["A3"].append(gB.gid)
            got += 1
        assert got == cnt, ("A3", edge, flag, got)
    n_joint_nc = 0
    cands = [g for g in M4 if g.sector == 0 and g.gid not in used and g.band > 0]
    for i in rng.permutation(len(cands)):
        if n_joint_nc >= 10:
            break
        gB = cands[int(i)]
        if gB.gid in used:
            continue
        d0 = down(gB)
        if d0 < 2.0e6:
            continue
        eb = [m for m in gB.members if m.borrower and not m.hz]
        eB = max(eb, key=lambda m: m.cust)
        u = Undo()
        L = float(round_limit(rng.uniform(0.25, 0.7) * min(d0 - 0.5e6, 20e6)))
        gA = joint(gB, eB, L, u, False, prefer_band=(0, 4)[n_joint_nc % 2])
        if gA is None:
            continue
        used.update([gA.gid, gB.gid])
        n_joint_nc += 1

    # ---------------------------------------------------------- DV-A: several obligors in one group
    w.movers["A1"] = []
    a1_plan = [(0, True, 1), (1, True, 3), (2, True, 1), (3, True, 3),
               (0, False, 3), (1, False, 7), (2, False, 3), (3, False, 7)]

    def borrowers_of(g):
        return [m for m in g.members if m.borrower and not m.hz and m.cust]

    for edge, flag, cnt in a1_plan:
        got = 0
        cands = pool(edge, flag, key=lambda g: up(g))
        for g in cands:
            if got >= cnt:
                break
            bs = borrowers_of(g)
            if len(bs) < 2:
                continue
            u0 = up(g)
            done = False
            for f in sorted(plain_facs(w, g), key=lambda f: -f.limit / FX[f.ccy]):
                v = f.limit / FX[f.ccy]
                others = [m for m in bs if m.eid != f.obligors[0]]
                for k in range(1, min(3, len(others)) + 1):
                    if k * v < u0 + 0.35e6:
                        continue
                    if edge < 3 and k * v > u0 + width[edge] - 0.35e6:
                        break
                    u = Undo()
                    for m in others[:k]:
                        u.oblig(w, f, m.eid)
                    f.dev.add("A1")
                    e1 = gexp(w, g, grain="rows")
                    if right_ok(w, g) and band_of(e1) == edge + 1 and edge_dist(e1) >= 0.2e6:
                        done = True
                        break
                    f.dev.discard("A1")
                    u.rollback(w)
                if done:
                    break
            if done:
                used.add(g.gid)
                w.movers["A1"].append(g.gid)
                got += 1
        assert got == cnt, ("A1", edge, flag, got)
    # blending: about 12 per cent of facilities carry two to four obligors from one group
    target = int(0.12 * sum(1 for f in w.facilities if f.status == "ACTIVE"))
    have = sum(1 for f in w.facilities if "A1" in f.dev)
    cands = [f for f in w.facilities if f.status == "ACTIVE" and len(f.obligors) == 1 and not f.dev]
    for i in rng.permutation(len(cands)):
        if have >= target:
            break
        f = cands[int(i)]
        g = w.groups[w.ents[f.obligors[0]].gid]
        if g.gid in used:
            continue
        others = [m for m in borrowers_of(g) if m.eid != f.obligors[0]]
        if not others:
            continue
        k = int(min(len(others), 1 + rng.choice(3, p=[0.7, 0.22, 0.08])))
        u = Undo()
        for j in rng.choice(len(others), k, replace=False):
            u.oblig(w, f, others[int(j)].eid)
        f.dev.add("A1")
        if g.band is not None and band_of(gexp(w, g, grain="rows")) != g.band:
            f.dev.discard("A1")
            u.rollback(w)
            continue
        have += 1

    # ---------------------------------------------------------- DV-B: limit increases from 1 October
    w.movers["B2"] = []
    b2_plan = [(0, True, 1), (1, True, 3), (2, True, 1), (3, True, 3),
               (0, False, 3), (1, False, 7), (2, False, 3), (3, False, 7)]
    for edge, flag, cnt in b2_plan:
        got = 0
        for g in pool(edge, flag, key=lambda g: up(g)):
            if got >= cnt:
                break
            u0 = up(g)
            fs = sorted([f for f in plain_facs(w, g) if f.start < D(2026, 8, 1)], key=lambda f: -f.limit / FX[f.ccy])
            if not fs:
                continue
            f = fs[0]
            d_gbp = u0 + rng.uniform(0.4e6, 1.2e6)
            d = round(d_gbp * FX[f.ccy] / 50000) * 50000
            if d > 1.5 * f.limit:
                continue
            u = Undo()
            u.set(f, "oct1", float(d))
            f.dev.add("B")
            e2 = gexp(w, g, clock="B2")
            if band_of(e2) == edge + 1 and edge_dist(e2) >= 0.2e6:
                used.add(g.gid)
                w.movers["B2"].append(g.gid)
                got += 1
            else:
                f.dev.discard("B")
                u.rollback(w)
        assert got == cnt, ("B2", edge, flag, got)
    n = len(w.movers["B2"])
    cands = [f for f in w.facilities if f.status == "ACTIVE" and in_force(f) and not f.dev and f.limit >= 0.5e6
             and f.start < D(2026, 8, 1)]
    for i in rng.permutation(len(cands)):
        if n >= 70:
            break
        f = cands[int(i)]
        gids = fac_groups(w, f)
        if any(x in used for x in gids):
            continue
        d = round(rng.uniform(0.08, 0.35) * f.limit / 50000) * 50000
        if d <= 0:
            continue
        u = Undo()
        u.set(f, "oct1", float(d))
        f.dev.add("B")
        if any(w.groups[x].band is not None and band_of(gexp(w, w.groups[x], clock="B2")) != w.groups[x].band
               for x in gids):
            f.dev.discard("B")
            u.rollback(w)
            continue
        n += 1
    # facilities available from 1 October, activated by the same batch
    for g in [w.live_groups[int(i)] for i in rng.choice(len(w.live_groups), 12, replace=False)]:
        e = [m for m in g.members if m.borrower and not m.hz][0]
        ccy = ccy_of(rng, e)
        add_fac(w, Fac(booking=booking_of(e), product=str(rng.choice(["RCF", "TERM_LOAN", "ASSET_FINANCE"])), ccy=ccy,
                       limit=0.0, oct1=float(round_limit(rng.uniform(0.5e6, 6e6) * FX[ccy])), obligors=[e.eid],
                       start=D(2026, 10, 1), maturity=D(2026, 10, 1) + dt.timedelta(days=int(rng.integers(900, 1830))),
                       status="ACTIVE", booked=D(2026, 8, 1) + dt.timedelta(days=int(rng.integers(0, 56))),
                       dev={"ACT"}))
    # facilities reaching final maturity on 30 September, closed by the 1 October batch
    cands = [f for f in w.facilities if f.status == "ACTIVE" and in_force(f) and not f.dev and
             f.start < D(2024, 6, 1)]
    for i in rng.choice(len(cands), 22, replace=False):
        f = cands[int(i)]
        g = w.groups[w.ents[f.obligors[0]].gid]
        if g.gid in used:
            continue
        u = Undo()
        u.set(f, "maturity", EXTRACT_DATE)
        # the facility's own limit no longer counts; the group keeps its band through a new facility
        e = w.ents[f.obligors[0]]
        st = w.rand_date(D(2026, 3, 1), D(2026, 8, 31))
        nf = Fac(booking=f.booking, product=f.product, ccy=f.ccy, limit=f.limit, obligors=[e.eid], start=st,
                 maturity=st + dt.timedelta(days=int(rng.integers(1000, 1830))), status="ACTIVE",
                 booked=st - dt.timedelta(days=int(rng.integers(0, 30))))
        u.add(w, nf)
        u.set(f, "status", "CLOSED")
        f.dev.add("MAT")
        if not right_ok(w, g):
            f.dev.discard("MAT")
            u.rollback(w)

    # ---------------------------------------------------------- DV-B: increases keyed in the day on 30 September
    w.movers["B0"] = []
    b0_plan = [(0, True, 1), (2, True, 1), (0, False, 2), (1, False, 4), (2, False, 2), (3, False, 4)]
    for edge, flag, cnt in b0_plan:
        got = 0
        for g in pool(edge + 1, flag, key=lambda g: down(g)):
            if got >= cnt:
                break
            d0 = down(g)
            fs = sorted([f for f in plain_facs(w, g) if f.start < D(2026, 8, 1)], key=lambda f: -f.limit / FX[f.ccy])
            if not fs:
                continue
            f = fs[0]
            d_gbp = d0 + rng.uniform(0.4e6, 1.2e6)
            d = round(d_gbp * FX[f.ccy] / 50000) * 50000
            if f.limit - d < 0.4 * f.limit:
                continue
            u = Undo()
            u.set(f, "sep30", float(d))
            f.dev.add("B")
            e0 = gexp(w, g, clock="B0")
            if band_of(e0) == edge and edge_dist(e0) >= 0.2e6:
                used.add(g.gid)
                w.movers["B0"].append(g.gid)
                got += 1
            else:
                f.dev.discard("B")
                u.rollback(w)
        assert got == cnt, ("B0", edge, flag, got)
    n = len(w.movers["B0"])
    cands = [f for f in w.facilities if f.status == "ACTIVE" and in_force(f) and not f.dev and f.limit >= 0.5e6
             and f.start < D(2026, 8, 1)]
    for i in rng.permutation(len(cands)):
        if n >= 34:
            break
        f = cands[int(i)]
        gids = fac_groups(w, f)
        if any(x in used for x in gids):
            continue
        d = round(rng.uniform(0.1, 0.3) * f.limit / 50000) * 50000
        if d <= 0:
            continue
        u = Undo()
        u.set(f, "sep30", float(d))
        f.dev.add("B")
        if any(w.groups[x].band is not None and band_of(gexp(w, w.groups[x], clock="B0")) != w.groups[x].band
               for x in gids):
            f.dev.discard("B")
            u.rollback(w)
            continue
        n += 1

    # ---------------------------------------------------------- later limit changes, 2 to 7 October
    cands = [f for f in w.facilities if f.status == "ACTIVE" and in_force(f) and f.limit >= 0.5e6 and
             not (f.dev & {"MAT"})]
    for i in rng.choice(len(cands), 26, replace=False):
        f = cands[int(i)]
        base = f.limit + f.oct1
        val = float(round(base * rng.uniform(0.7, 1.35) / 50000) * 50000)
        d = D(2026, 10, int(rng.integers(2, 8)))
        stamp = sod_stamp(d) if rng.random() < 0.4 else user_stamp(rng, d)
        if stamp.date() < D(2026, 10, 1):
            stamp = user_stamp(rng, d)
        f.later = [(stamp, val)]
        f.dev.add("LATER")
    w.used_groups = used


def band_exposure_figures(w, cohort, **kw):
    """World-side committed exposure and expected arriving exposure by band and in total (GBP m)."""
    PPV1, M1 = ppv_m1()
    E = exposure(w, **kw)
    com, arr = [0.0] * 5, [0.0] * 5
    for gid in cohort[4]["M"]:
        g = w.groups[gid]
        e = E.get(gid, 0.0)
        b = band_of(e)
        com[b] += e
        arr[b] += (PPV1 if g.flag[4] else M1) * e
    return [x / 1e6 for x in com] + [sum(com) / 1e6], [x / 1e6 for x in arr] + [sum(arr) / 1e6]


def tune_exposures(w, cohort):
    """Nudge one ordinary sterling limit at a time until every committed and arriving exposure figure (five
    bands and the total, GBP m to one decimal) sits at least 0.25 of its bin from an edge."""
    rng = w.drng
    cand = []
    for gid in cohort[4]["M"]:
        g = w.groups[gid]
        if gid in w.used_groups:
            continue
        if any(f.dev for f in w.gfacs.get(gid, [])):
            continue
        if edge_dist(gexp(w, g)) < 1.5e6:
            continue
        for f in plain_facs(w, g):
            if f.ccy == "GBP" and f.booking == "HB-PLC" and 1e6 <= f.limit <= 5e6:
                cand.append((g.band, gid, f))
    for it in range(3000):
        com, arr = band_exposure_figures(w, cohort)
        bad = [("c", i) for i, x in enumerate(com) if bin_margin(x) < 0.25] + \
              [("a", i) for i, x in enumerate(arr) if bin_margin(x) < 0.25]
        for v in (com, arr):     # the rounded rows tie to the rounded total
            if abs(sum(round(x, 1) for x in v[:5]) - round(v[5], 1)) > 1e-6:
                bad.append(("t", 5))
        if not bad:
            return it
        _, i = bad[0]
        b = i if i < 5 else int(rng.integers(0, 5))
        pl = [x for x in cand if x[0] == b]
        _, gid, f = pl[int(rng.integers(0, len(pl)))]
        f.limit = float(f.limit + 25000 * int(rng.choice([-3, -2, -1, 1, 2, 3])))
    raise RuntimeError("exposure tuning did not settle")


def number_facilities(w):
    """Each ledger numbers its facilities in the order they were booked."""
    rng = w.drng
    plc = sorted([f for f in w.facilities if f.booking == "HB-PLC"], key=lambda f: (f.booked, f.start, f.limit))
    dac = sorted([f for f in w.facilities if f.booking == "HB-DAC"], key=lambda f: (f.booked, f.start, f.limit))
    n = 20418226
    for f in plc:
        n += int(rng.integers(1, 6))
        f.fid = "%08d" % n
    span = n - 20418226
    step = max(2, span // max(1, len(dac)))
    n = 20418226 + int(rng.integers(0, 20))
    for f in dac:
        n += int(rng.integers(1, 2 * step))
        f.fid = "%08d" % n


def build_histories(w):
    """Every committed limit each facility has carried, with the platform's UTC stamps."""
    rng = w.drng
    for f in w.facilities:
        h = []
        if "ACT" in f.dev:
            h.append((SOD_1OCT, f.oct1, "SOD_BATCH"))
            f.history = h
            continue
        pre = f.history if f.status in ("CANCELLED", "CLOSED") and "MAT" not in f.dev else (f.limit - f.sep30)
        # earlier amendments, walked backwards from the limit in force before 30 September
        n_am = 0
        if f.start < D(2025, 9, 1):
            n_am = int(min(3, rng.poisson(0.9)))
        last_day = min(D(2026, 9, 25), f.closed_on - dt.timedelta(days=5) if f.closed_on else D(2026, 9, 25))
        days = sorted({f.start + dt.timedelta(days=int(rng.integers(30, max(31, (last_day - f.start).days))))
                       for _ in range(n_am)} - {None})
        days = [d for d in days if d <= last_day]
        vals = [float(pre)]
        for _ in days:
            vals.insert(0, float(round_limit(vals[0] * rng.uniform(0.7, 1.15))))
        # initial version: keyed when the facility was booked, or set by the batch on the start date
        if rng.random() < 0.6:
            h.append((user_stamp(rng, f.booked), vals[0], str(rng.choice(USERS))))
        else:
            h.append((sod_stamp(f.start), vals[0], "SOD_BATCH"))
        for d, v in zip(days, vals[1:]):
            if rng.random() < 0.5:
                h.append((sod_stamp(d), v, "SOD_BATCH"))
            else:
                h.append((user_stamp(rng, d), v, str(rng.choice(USERS))))
        if f.status in ("CANCELLED", "CLOSED") and "MAT" not in f.dev:
            h.append((user_stamp(rng, f.closed_on) if rng.random() < 0.5 else sod_stamp(f.closed_on), 0.0,
                      "SOD_BATCH" if rng.random() < 0.5 else str(rng.choice(USERS))))
        if f.sep30:
            t = dt.datetime(2026, 9, 30, int(rng.integers(7, 16)), int(rng.integers(0, 60)), int(rng.integers(0, 60)))
            h.append((t, f.limit, str(rng.choice(USERS))))
        if f.oct1:
            h.append((SOD_1OCT, f.limit + f.oct1, "SOD_BATCH"))
        if "MAT" in f.dev:
            h.append((SOD_1OCT, 0.0, "SOD_BATCH"))
        for t, v in f.later:
            h.append((t, v, "SOD_BATCH" if t.minute == 30 and t.second == 0 else str(rng.choice(USERS))))
        h.sort(key=lambda x: x[0])
        # the stamps are strictly increasing, and the value in force at each reading is the designed one
        for a, b in zip(h, h[1:]):
            assert a[0] < b[0], (f.fid, h)
        f.history = h


def version_at(f, t):
    v = None
    for s, val, _ in f.history:
        if s <= t:
            v = val
    return v


def build(devices=True):
    w = World()
    w.drng = np.random.default_rng(SEED + 101)
    w._hzseq = 2290000
    cohort = build_lifecycle(w)
    w.cohort = cohort
    gleif_texture(w, cohort)
    assign_bands_and_flags(w, cohort)
    build_signals(w, cohort)
    build_facilities(w, cohort)
    w.used_groups = set()
    w.movers = {}
    if devices:
        plant_devices(w, cohort)
        w.tune_steps = tune_exposures(w, cohort)
    number_facilities(w)
    build_histories(w)
    for f in w.facilities:
        if f.status in ("CANCELLED", "CLOSED") and "MAT" not in f.dev:
            f.limit = 0.0
        assert version_at(f, T_END) == (f.limit if (f.start <= EXTRACT_DATE or "ACT" not in f.dev) else None) or \
            "ACT" in f.dev, f.fid
    return w


if __name__ == "__main__":
    w = build()
    print(len(w.groups), len(w.ents), len(w.signals), len(w.facilities))
    print({k: len(v) for k, v in w.movers.items()}, "tuning", w.tune_steps)
    print(w.band_n, w.band_f)
