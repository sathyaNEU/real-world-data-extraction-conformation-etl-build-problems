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
TP_FLAG = [58, 33, 28, 39]
FP_FLAG = [60, 64, 66, 63]
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
                 "direct_only", "vendor_name", "inert")

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
                        (m == d and rng.random() < 0.28) else "AMBER"
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
                if m in sept_idx:
                    c = sept_idx[m]
                    if w.on_list(g, m):
                        mark(e0, m, "RED" if rng.random() < 0.7 else "AMBER")
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
            ms = [bin_margin(fl[i] * PPV1) for i in range(5)] + [bin_margin(u[i] * M1) for i in range(5)] + \
                 [bin_margin(fl[i] * PPV1 + u[i] * M1) for i in range(5)]
            m = min(ms)
            key = (round(m, 3), -sum(abs(x) for x in dn) - sum(abs(x) for x in df))
            if best is None or key > best[0]:
                best = (key, n, fl)
    return best[1], best[2]


BAND_N = [203, 294, 242, 122, 52]     # band_plan() result, fixed here; checks.py re-derives the margins
BAND_F = [36, 54, 44, 23, 8]


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
class Fac:
    __slots__ = ("fid", "cust", "eid", "booking", "product", "ccy", "limit", "drawn", "start", "maturity",
                 "status", "limit_r1", "device")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


def band_of(x):
    for i, e in enumerate(BAND_EDGES):
        if x < e:
            return i
    return 4


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


def build_facilities(w, cohort):
    rng = w.rng
    lo_hi = [(0.4e6, 4.6e6), (5.4e6, 14.6e6), (15.6e6, 39.2e6), (41e6, 98e6), (104e6, 260e6)]
    w._fseq = 3104227
    live_groups = [g for gid, g in sorted(w.groups.items()) if w.active(g, EXTRACT_DATE)]
    for g in live_groups:
        if g.band is None:   # on the watch list at 30 Sep 2026
            g.band_hint = int(rng.choice(5, p=[0.2, 0.35, 0.28, 0.13, 0.04]))
            b = g.band_hint
        else:
            b = g.band
        lo, hi = lo_hi[b]
        if b == 4:
            target = lo * np.exp(rng.uniform(0, np.log(hi / lo)))
        else:
            target = rng.uniform(lo, hi)
        borrowers = [e for e in g.members if e.borrower]
        # split the target into facilities
        k = int(min(6, 1 + rng.poisson(0.9 + 0.5 * b)))
        shares = rng.dirichlet(np.ones(k) * 1.6)
        amounts = [round_limit(target * s) for s in shares]
        # top up or trim to stay inside the band, away from the edges
        def total(a, ccys):
            return sum(x / FX[c] for x, c in zip(a, ccys))
        ccys = []
        bk = []
        owners = []
        for i in range(k):
            e = borrowers[int(rng.integers(0, len(borrowers)))]
            owners.append(e)
            if e.country == "IE":
                ccys.append("EUR")
                bk.append("HB-DAC")
            elif e.country in ("NL", "DE"):
                ccys.append("EUR")
                bk.append("HB-PLC")
            else:
                r = rng.random()
                ccys.append("USD" if r < 0.05 else ("EUR" if r < 0.10 else "GBP"))
                bk.append("HB-PLC")
        for _ in range(60):
            t = total(amounts, ccys)
            if lo + 0.25e6 <= t <= hi - 0.25e6:
                break
            j = int(np.argmax(amounts))
            amounts[j] = round_limit(amounts[j] * (lo + hi) / 2 / t)
        for i in range(k):
            e = owners[i]
            prod = str(rng.choice(["RCF", "TERM_LOAN", "OVERDRAFT", "TERM_LOAN", "ASSET_FINANCE", "RCF"]))
            start = w.rand_date(max(D(2016, 1, 1), g.active_from), D(2026, 8, 31))
            mat = start + dt.timedelta(days=int(rng.integers(400, 2600)))
            if mat <= EXTRACT_DATE + dt.timedelta(days=20):
                mat = EXTRACT_DATE + dt.timedelta(days=int(rng.integers(40, 1500)))
            drawn = amounts[i] * (rng.uniform(0.2, 0.95) if prod != "OVERDRAFT" else rng.uniform(0, 0.6))
            w._fseq += int(rng.integers(1, 40))
            w.facilities.append(Fac(fid="F%08d" % w._fseq, cust=e.cust, eid=e.eid, booking=bk[i], product=prod,
                                    ccy=ccys[i], limit=float(amounts[i]), drawn=round(drawn, 2), start=start,
                                    maturity=mat, status="ACTIVE", limit_r1=None, device=None))
        # cancelled and closed facilities kept in the extract with their last limit
        if rng.random() < 0.10:
            e = borrowers[0]
            w._fseq += int(rng.integers(1, 40))
            st = w.rand_date(D(2017, 1, 1), D(2024, 12, 31))
            w.facilities.append(Fac(fid="F%08d" % w._fseq, cust=e.cust, eid=e.eid, booking="HB-PLC",
                                    product="RCF", ccy="GBP", limit=float(round_limit(rng.uniform(1e6, 12e6))),
                                    drawn=0.0, start=st, maturity=st + dt.timedelta(days=1825),
                                    status=str(rng.choice(["CANCELLED", "CLOSED"])), limit_r1=None, device=None))


def group_exposure(w, g, facs=None, fx_wrong=False, dac=True, rerun=True, matured=False, status=True):
    """Committed exposure of a group at 30 Sep 2026 under a reading of the facility files."""
    eids = {e.eid for e in g.members}
    tot = 0.0
    for f in (facs if facs is not None else w.facilities):
        if f.eid not in eids:
            continue
        if not dac and f.booking == "HB-DAC":
            continue
        if status and f.status != "ACTIVE":
            continue
        if not matured and f.maturity <= EXTRACT_DATE:
            continue
        lim = f.limit if (rerun or f.limit_r1 is None) else f.limit_r1
        tot += lim * FX[f.ccy] if fx_wrong else lim / FX[f.ccy]
    return tot


def plant_devices(w, cohort):
    """Ledgered exposure devices, each moving flagged and unflagged groups across band edges."""
    rng = w.rng
    M4 = [w.groups[g] for g in cohort[4]["M"]]

    def facs_of(g):
        eids = {e.eid for e in g.members}
        return [f for f in w.facilities if f.eid in eids and f.status == "ACTIVE"]

    def margin_up(g):
        t = group_exposure(w, g)
        return BAND_EDGES[g.band] - t if g.band < 4 else None

    def margin_down(g):
        t = group_exposure(w, g)
        return t - BAND_EDGES[g.band - 1] if g.band > 0 else None

    used = set()
    # D3: euro facilities large enough that multiplying by the rate instead of dividing crosses up
    fx_movers = []
    k_fx = FX["EUR"] * (FX["EUR"] - 1 / FX["EUR"]) + 1.0
    for b in (0, 1, 2, 3):
        for want_flag, k in ((True, 2), (False, 2)):
            cands = [g for g in M4 if g.band == b and g.flag[4] == want_flag and g.gid not in used]
            n_ok = 0
            for g in cands:
                if n_ok >= k:
                    break
                up = margin_up(g)
                if up is None or up < 2.4e6:
                    continue
                e = [m for m in g.members if m.borrower]
                if not e:
                    continue
                e = e[0]
                x = (up + 0.45e6 + rng.uniform(0, 0.3e6)) / k_fx       # sterling value of the new euro limit
                if x > up - 0.3e6:
                    continue
                eur = round_limit(x * FX["EUR"])
                f = new_fac(w, e, "EUR", eur, "HB-DAC" if e.country == "IE" else "HB-PLC", "D3")
                t = group_exposure(w, g)
                if band_of(t) != b or min(abs(t - xx) for xx in BAND_EDGES) < 0.25e6 or \
                        band_of(group_exposure(w, g, fx_wrong=True)) == b:
                    w.facilities.remove(f)
                    continue
                fx_movers.append(g.gid)
                used.add(g.gid)
                n_ok += 1
    # D4: Dublin facilities; dropping them moves groups down a band
    dac_movers = []
    for b in (1, 2, 3, 4):
        for want_flag, k in ((True, 2), (False, 2)):
            cands = [g for g in M4 if g.band == b and g.flag[4] == want_flag and g.gid not in used]
            n_ok = 0
            for g in cands:
                if n_ok >= k:
                    break
                down = margin_down(g)
                gbp = [f for f in facs_of(g) if f.ccy == "GBP"]
                if not gbp:
                    continue
                big = max(gbp, key=lambda f: f.limit)
                shift = down + 0.6e6 + rng.uniform(0, 1.2e6)
                if shift >= 0.8 * big.limit:
                    continue
                ie = [m for m in g.members if m.country == "IE" and not m.inert and m.role == "sub"]
                e = ie[0] if ie else None
                eur = round_limit(shift * FX["EUR"])
                old_limit = big.limit
                big.limit = float(round_limit(big.limit - eur / FX["EUR"]))
                if e is None:
                    top = g.members[0]
                    e = w.new_ent(g, top.name.split(" ")[0] + " " + SECTORS[g.sector][2][0] + " Ireland DAC",
                                  "sub", country="IE", parent=top.eid)
                    e.inert = True
                if not e.borrower:
                    e.borrower = True
                    e.cust = w.new_cust()
                f = new_fac(w, e, "EUR", eur, "HB-DAC", "D4")
                t2 = group_exposure(w, g)
                if band_of(t2) != b or min(abs(t2 - x) for x in BAND_EDGES) < 0.25e6 or \
                        band_of(group_exposure(w, g, dac=False)) == b:
                    w.facilities.remove(f)
                    big.limit = old_limit
                    continue
                dac_movers.append(g.gid)
                used.add(g.gid)
                n_ok += 1
    # D2: limits amended on 30 Sep, posted after the scheduled run
    rerun_movers = []
    for b in (1, 2, 3, 4):
        for want_flag, k in ((True, 2), (False, 2)):
            cands = [g for g in M4 if g.band == b and g.flag[4] == want_flag and g.gid not in used]
            cands.sort(key=lambda g: margin_down(g))
            n_ok = 0
            for g in cands:
                if n_ok >= k:
                    break
                plc = [f for f in facs_of(g) if f.booking == "HB-PLC" and f.ccy == "GBP"]
                if not plc:
                    continue
                f = max(plc, key=lambda x: x.limit)
                down = margin_down(g)
                # the amendment raised the limit; the scheduled run still shows the old one
                old = round_limit(f.limit - (down + 0.6e6 + rng.uniform(0, 1.0e6)))
                if old <= 0.2e6:
                    continue
                f.limit_r1 = float(old)
                f.device = "D2"
                if band_of(group_exposure(w, g, rerun=False)) == b:
                    f.limit_r1 = None
                    f.device = None
                    continue
                rerun_movers.append(g.gid)
                used.add(g.gid)
                n_ok += 1
    # amendments that do not cross an edge (most of them), so the rerun is not a list of movers
    others = [f for f in w.facilities if f.booking == "HB-PLC" and f.status == "ACTIVE" and f.limit_r1 is None
              and f.ccy == "GBP" and w.groups[w.ents[f.eid].gid].gid not in used and f.limit >= 1e6]
    for f in rng.choice(others, 32, replace=False):
        g = w.groups[w.ents[f.eid].gid]
        delta = round_limit(rng.uniform(0.1, 0.35) * f.limit) * (1 if rng.random() < 0.6 else -1)
        old = f.limit - delta
        if old <= 0.25e6:
            continue
        f.limit_r1 = float(old)
        if g.band is not None and band_of(group_exposure(w, g, rerun=False)) != g.band:
            f.limit_r1 = None
    # D8: facilities reaching final maturity on 30 Sep 2026, still ACTIVE in the plc runs
    mat_movers = []
    for b in (0, 1, 2, 3):
        for want_flag, k in ((True, 2), (False, 2)):
            cands = [g for g in M4 if g.band == b and g.flag[4] == want_flag and g.gid not in used]
            for g in cands[:k]:
                up = margin_up(g)
                e = [m for m in g.members if m.borrower and m.country == "GB"]
                if not e:
                    continue
                amt = round_limit(up + 0.7e6 + rng.uniform(0, 1.2e6))
                f = new_fac(w, e[0], "GBP", amt, "HB-PLC", "D8")
                f.maturity = EXTRACT_DATE
                f.start = EXTRACT_DATE - dt.timedelta(days=int(rng.integers(700, 1800)))
                f.product = str(rng.choice(["TERM_LOAN", "RCF"]))
                if band_of(group_exposure(w, g, matured=True)) == b:
                    w.facilities.remove(f)
                    continue
                mat_movers.append(g.gid)
                used.add(g.gid)
    # matured facilities that do not cross an edge
    for g in rng.choice([g for g in M4 if g.gid not in used], 14, replace=False):
        e = [m for m in g.members if m.borrower and m.country == "GB"]
        if not e:
            continue
        up = margin_up(g)
        if up is None or up < 1.2e6:
            continue
        amt = round_limit(rng.uniform(0.2, 0.6) * up)
        f = new_fac(w, e[0], "GBP", amt, "HB-PLC", None)
        f.maturity = EXTRACT_DATE
        f.start = EXTRACT_DATE - dt.timedelta(days=int(rng.integers(700, 1800)))
    w.movers = dict(D3=fx_movers, D4=dac_movers, D2=rerun_movers, D8=mat_movers)


def new_fac(w, e, ccy, amount, booking, device):
    rng = w.rng
    w._fseq += int(rng.integers(1, 40))
    start = w.rand_date(D(2019, 1, 1), D(2026, 8, 31))
    f = Fac(fid="F%08d" % w._fseq, cust=e.cust, eid=e.eid, booking=booking,
            product=str(rng.choice(["TERM_LOAN", "RCF", "TERM_LOAN"])), ccy=ccy, limit=float(amount),
            drawn=round(float(amount) * rng.uniform(0.3, 0.9), 2), start=start,
            maturity=EXTRACT_DATE + dt.timedelta(days=int(rng.integers(60, 1600))), status="ACTIVE",
            limit_r1=None, device=device)
    w.facilities.append(f)
    return f


def band_exposure_figures(w, cohort, **kw):
    """World-side expected arriving exposure by band and in total (GBP m), and per-band flagged and
    unflagged expected arrivals, on the right reading unless told otherwise."""
    PPV1, M1 = ppv_m1()
    out = [0.0] * 5
    for gid in cohort[4]["M"]:
        g = w.groups[gid]
        e = group_exposure(w, g, **kw)
        b = band_of(e)
        out[b] += (PPV1 if g.flag[4] else M1) * e
    return [x / 1e6 for x in out] + [sum(out) / 1e6]


def tune_exposures(w, cohort):
    """Nudge one ordinary sterling limit at a time, in GBP 50,000 steps, until every expected-exposure
    figure (five bands and the total, GBP m to one decimal) sits at least 0.2 of its bin from an edge."""
    rng = w.rng
    movers = set(sum(w.movers.values(), []))
    cand = []
    for gid in cohort[4]["M"]:
        g = w.groups[gid]
        if gid in movers:
            continue
        e = group_exposure(w, g)
        if min(abs(e - x) for x in BAND_EDGES) < 1.5e6:
            continue
        eids = {m.eid for m in g.members}
        for f in w.facilities:
            if f.eid in eids and f.ccy == "GBP" and f.booking == "HB-PLC" and f.status == "ACTIVE" and \
                    f.limit_r1 is None and f.device is None and 1e6 <= f.limit <= 5e6 and f.maturity > EXTRACT_DATE:
                cand.append((g.band, gid, f))
    for it in range(400):
        figs = band_exposure_figures(w, cohort)
        bad = [i for i, x in enumerate(figs) if bin_margin(x) < 0.2]
        if not bad:
            return it
        i = bad[0]
        b = i if i < 5 else int(rng.integers(0, 5))
        pool = [x for x in cand if x[0] == b]
        _, gid, f = pool[int(rng.integers(0, len(pool)))]
        f.limit = float(f.limit + 50000 * int(rng.choice([-2, -1, 1, 2])))
    raise RuntimeError("exposure tuning did not settle")


def build():
    w = World()
    cohort = build_lifecycle(w)
    w.cohort = cohort
    gleif_texture(w, cohort)
    assign_bands_and_flags(w, cohort)
    build_signals(w, cohort)
    build_facilities(w, cohort)
    plant_devices(w, cohort)
    w.tune_steps = tune_exposures(w, cohort)
    return w


if __name__ == "__main__":
    w = build()
    print(len(w.groups), len(w.ents), len(w.signals), len(w.facilities))
    print({k: len(v) for k, v in w.movers.items()})
    print(w.band_n, w.band_f)
