"""The Yarrabin world: properties on the council's rates roll, NMIs in the distributor's network model, the GIS
cross-reference between them, each dwelling's rooftop PV history (organic adoption, builder-installed systems at
handover, Solar Streets program systems, alterations, removals, withdrawn and pending applications) and the
national DER Register's record of each system. Everything is simulated forward from per-locality streams; the
campaign figures are targets the construction meets exactly, and every analysis figure is computed later from the
written files (calc.py)."""
from __future__ import annotations

import collections
import datetime as dt
import math

import numpy as np

import common as K

# Organic adoption pace by calendar year (relative units per year): the Solar Bonus Scheme surge of 2010-2012, the
# lull after the feed-in tariff closed, and the steady rise with cheaper panels from 2017.
PACE = {2009: 0.40, 2010: 1.20, 2011: 2.15, 2012: 1.95, 2013: 0.90, 2014: 0.95, 2015: 0.90, 2016: 0.95, 2017: 1.02,
        2018: 1.10, 2019: 1.19, 2020: 1.28, 2021: 1.37, 2022: 1.66, 2023: 2.00, 2024: 2.02, 2025: 2.20, 2026: 2.34,
        2027: 2.34, 2028: 2.34, 2029: 2.34, 2030: 2.34}
HORIZON = dt.date(2030, 12, 31)

STREETS = ["Banksia", "Kookaburra", "Wattle", "Grevillea", "Bottlebrush", "Lilly Pilly", "Mahogany", "Ironwood",
           "Silver Ash", "Blackbutt", "Spotted Gum", "Red Cedar", "Hoop Pine", "Brushbox", "Tuckeroo", "Callistemon",
           "Lomandra", "Melaleuca", "Firewheel", "Macadamia", "Plover", "Kingfisher", "Rosella", "Lorikeet", "Currawong",
           "Magpie", "Wren", "Pardalote", "Bellbird", "Whipbird", "Kestrel", "Brolga", "Jabiru", "Heron", "Egret",
           "Curlew", "Sandpiper", "Fairy", "Corella", "Galah", "Sunbird", "Honeyeater", "Fantail", "Robin", "Thornbill",
           "Swallow", "Martin", "Falcon", "Osprey", "Kite", "Harrier", "Goshawk", "Bushlark", "Pipit", "Finch",
           "Quail", "Dotterel", "Lapwing", "Ibis", "Spoonbill"]
SUFFIX = ["Street", "Street", "Street", "Court", "Crescent", "Place", "Drive", "Avenue", "Close", "Way", "Circuit",
          "Lane", "Parade", "Road"]
POSTCODE = {"YRB21": "4512", "YRB22": "4512", "YRB23": "4514", "YRB24": "4516", "YRB25": "4514", "YRB26": "4517",
            "YRB27": "4513", "YRB28": "4513"}

INSTALLERS = ["A%06d" % n for n in (101233, 104417, 107992, 110385, 112640, 115508, 118274, 120936, 123311, 126087,
                                     128745, 131402, 133968, 136650, 139271, 141893, 144520, 147106, 149788, 152433)]
PROGRAM_INSTALLER = {"SunCoast Solar Installations": "A118274", "Brightline Energy Solutions": "A126087",
                     "Greenhaven Electrical": "A133968", "Riverstone Solar": "A144520"}


# ----------------------------------------------------------------------------------------------------------------
# small helpers

def year_frac_start(d):
    return dt.date(d.year, 1, 1)


def cum_pace(start, end):
    """Integrated pace between two dates (pace-years)."""
    if end <= start:
        return 0.0
    tot, d = 0.0, start
    while d < end:
        ye = dt.date(d.year + 1, 1, 1)
        seg_end = min(ye, end)
        days_in_year = (ye - dt.date(d.year, 1, 1)).days
        tot += PACE[d.year] * (seg_end - d).days / days_in_year
        d = seg_end
    return tot


def inv_pace(start, amount):
    """The date at which the integrated pace from start reaches amount (or None past the horizon)."""
    d = start
    while d < HORIZON:
        ye = dt.date(d.year + 1, 1, 1)
        days_in_year = (ye - dt.date(d.year, 1, 1)).days
        seg = PACE[d.year] * (ye - d).days / days_in_year
        if amount <= seg:
            return d + dt.timedelta(days=int(amount / PACE[d.year] * days_in_year))
        amount -= seg
        d = ye
    return None


BOOM_END = dt.date(2013, 1, 1)
REFERENCE = dt.date(2015, 1, 1)


def adopt_date(start, e, lam_boom, lam):
    """The date a unit exponential e is reached by the cumulative hazard from start: lam_boom per unit of pace in the
    Solar Bonus Scheme years, lam from 2013."""
    if start < BOOM_END:
        h = lam_boom * cum_pace(start, BOOM_END)
        if e <= h:
            return inv_pace(start, e / lam_boom)
        return inv_pace(BOOM_END, (e - h) / lam)
    return inv_pace(start, e / lam)


def inverter_size(r, d, kind="res"):
    """Inverter rating (kW AC) and panel capacity (kWp) for a system connected on d."""
    y = d.year
    if kind == "biz":
        kw = float(r.choice([10.0, 15.0, 20.0, 25.0, 30.0], p=[0.30, 0.25, 0.20, 0.15, 0.10]))
        return kw, round(kw * float(r.uniform(1.05, 1.30)), 2)
    if y <= 2012:
        kw = float(r.choice([1.5, 2.0, 2.5, 3.0, 4.0, 5.0], p=[0.22, 0.20, 0.14, 0.20, 0.12, 0.12]))
    elif y <= 2016:
        kw = float(r.choice([3.0, 4.0, 4.6, 5.0], p=[0.18, 0.20, 0.12, 0.50]))
    elif y <= 2020:
        kw = float(r.choice([5.0, 6.0, 8.0, 8.2, 10.0], p=[0.58, 0.10, 0.14, 0.08, 0.10]))
    elif d < dt.date(2025, 7, 1):
        kw = float(r.choice([5.0, 6.0, 8.0, 8.2, 10.0], p=[0.42, 0.12, 0.20, 0.10, 0.16]))
    else:
        kw = float(r.choice([5.0, 6.0, 8.0, 10.0, 13.2], p=[0.10, 0.07, 0.15, 0.58, 0.10]))
    over = float(r.choice([1.0, 1.1, 1.2, 1.32], p=[0.20, 0.25, 0.30, 0.25]))
    return kw, round(kw * over + float(r.choice([0.0, 0.06, 0.12, -0.06])), 2)


# ----------------------------------------------------------------------------------------------------------------
# properties and NMIs

class World:
    pass


def make_nmi(r, used):
    while True:
        n = "3119%06d" % int(r.integers(0, 10 ** 6))
        if n not in used:
            used.add(n)
            return n


def feeder_on(n, d):
    """The feeder an NMI was on at date d (the network model's history of load transfers)."""
    f = n["hist"][0][1]
    for start, fd in n["hist"][1:]:
        if d is not None and d >= start:
            f = fd
    return f


def build_places(W):
    """Properties, NMIs and the cross-reference, locality by locality."""
    used_nmi, used_prop = set(), set()
    W.props, W.nmis = [], []
    r_streets = K.rng("streets")
    pool = list(STREETS)
    r_streets.shuffle(pool)
    sidx = 0
    transfers = {t[0]: t[1:] for t in K.TRANSFERS}
    for loc in K.LOCALITIES:
        r = K.rng("place", loc.get("stream", loc["name"]))
        name, feeder = loc["name"], loc["feeder"]
        postcode = loc.get("postcode", POSTCODE[feeder])
        n_units = loc["res"] - loc["oo"] - loc["rent"] - loc["town"]
        assert n_units >= 0, name
        kinds = (["house_oo"] * loc["oo"] + ["house_rent"] * loc["rent"] + ["town"] * loc["town"] +
                 ["unit"] * n_units)
        kinds = list(np.array(kinds)[r.permutation(len(kinds))])
        n_streets = max(4, len(kinds) // 55)
        streets = []
        for _ in range(n_streets):
            base = pool[sidx % len(pool)]
            sidx += 1
            streets.append("%s %s" % (base, SUFFIX[int(r.integers(0, len(SUFFIX)))]))
        # a load transfer moves the whole locality, or the streets of one section of it
        moved, hist_of = set(), None
        if name in transfers:
            share, frm, to, when = transfers[name]
            rt = K.rng("transfer", name)
            k = len(streets) if share >= 1.0 else int(round(share * len(streets)))
            moved = set(streets) if share >= 1.0 else set(rt.choice(streets, size=k, replace=False))

            def hist_of(st, frm=frm, to=to, when=when):
                return [(None, frm), (when, to)] if st in moved else [(None, frm)]
        else:
            def hist_of(st, feeder=feeder):
                return [(None, feeder)]
        lo, hi = loc["built"]
        infill = loc.get("infill", 0)
        # houses built in the locality's own years; infill houses (knock-down rebuilds and splits) 2019 to 2026
        house_idx = [i for i, k in enumerate(kinds) if k.startswith("house")]
        infill_set = set(int(x) for x in r.choice(house_idx, size=infill, replace=False)) if infill else set()
        unit_blocks = {}
        for i, kind in enumerate(kinds):
            street = streets[int(r.integers(0, len(streets)))]
            if i in infill_set:
                handover = K.add_days(dt.date(2019, 3, 1), int(r.integers(0, 2700)))
                built = handover.year
            else:
                built = int(r.integers(lo, hi + 1))
                handover = dt.date(built, int(r.integers(1, 13)), int(r.integers(1, 28)))
            prop_no = "%07d" % int(r.integers(1000000, 9999999))
            while prop_no in used_prop:
                prop_no = "%07d" % int(r.integers(1000000, 9999999))
            used_prop.add(prop_no)
            if kind in ("house_oo", "house_rent"):
                lu, plan = "02", "RP" if built < 2000 else "SP"
                lot = "%d%s%06d" % (int(r.integers(1, 400)), plan, int(r.integers(100000, 399999)))
                addr = "%d %s" % (int(r.integers(1, 260)), street)
                area = int(r.integers(420, 900)) if name not in ("Myrtle Vale", "Bloodwood") else int(
                    r.integers(4000, 20000))
            elif kind == "town":
                lu = "09"
                lot = "%dGTP%06d" % (int(r.integers(1, 40)), int(r.integers(100000, 120000)))
                addr = "%d/%d %s" % (int(r.integers(1, 30)), int(r.integers(1, 200)), street)
                area = int(r.integers(140, 320))
            else:
                lu = "08"
                blk = unit_blocks.setdefault(street, int(r.integers(1, 200)))
                lot = "%dBUP%06d" % (int(r.integers(1, 60)), int(r.integers(100000, 110000)))
                addr = "%d/%d %s" % (int(r.integers(1, 48)), blk, street)
                area = 0
            occ = "R1" if kind == "house_oo" else ("R2" if kind == "house_rent" else
                                                    ("R1" if r.random() < 0.45 else "R2"))
            p = dict(property_no=prop_no, lot=lot, address=addr, locality=name, postcode=postcode,
                     land_use=lu, rating=occ, area=area, built=built, handover=handover, kind=kind,
                     infill=i in infill_set, feeder=feeder, loc=loc, street=street)
            W.props.append(p)
            nmi = make_nmi(r, used_nmi)
            hist = hist_of(street)
            n = dict(nmi=nmi, feeder=hist[-1][1], hist=hist, tariff="Residential", address=addr, locality=name,
                     postcode=postcode, status="Active", energised=handover, prop=p, temp=None,
                     transformer="%s-T%04d" % (hist[-1][1], int(r.integers(1, 420))))
            p["nmis"] = [n]
            W.nmis.append(n)
        # business NMIs on their own commercial properties
        for b in range(loc["biz"]):
            prop_no = "%07d" % int(r.integers(1000000, 9999999))
            while prop_no in used_prop:
                prop_no = "%07d" % int(r.integers(1000000, 9999999))
            used_prop.add(prop_no)
            street = streets[int(r.integers(0, len(streets)))]
            built = int(r.integers(lo, max(lo, hi) + 1))
            addr = "%d %s" % (int(r.integers(1, 260)), street)
            p = dict(property_no=prop_no, lot="%dSP%06d" % (int(r.integers(1, 90)), int(r.integers(100000, 399999))),
                     address=addr, locality=name, postcode=postcode, land_use=str(r.choice(["11", "17", "27", "41"])),
                     rating="C1", area=int(r.integers(400, 3000)), built=built,
                     handover=dt.date(built, int(r.integers(1, 13)), int(r.integers(1, 28))), kind="biz", infill=False,
                     feeder=feeder, loc=loc, street=street)
            W.props.append(p)
            nmi = make_nmi(r, used_nmi)
            hist = hist_of(street)
            n = dict(nmi=nmi, feeder=hist[-1][1], hist=hist, tariff="Business", address=addr, locality=name,
                     postcode=postcode, status="Active", energised=p["handover"], prop=p, temp=None,
                     transformer="%s-T%04d" % (hist[-1][1], int(r.integers(1, 420))))
            p["nmis"] = [n]
            W.nmis.append(n)
        # vacant lots on the roll (no NMI)
        for v in range(int(loc["res"] * 0.03)):
            prop_no = "%07d" % int(r.integers(1000000, 9999999))
            while prop_no in used_prop:
                prop_no = "%07d" % int(r.integers(1000000, 9999999))
            used_prop.add(prop_no)
            street = streets[int(r.integers(0, len(streets)))]
            W.props.append(dict(property_no=prop_no, lot="%dSP%06d" % (int(r.integers(1, 400)), int(r.integers(100000, 399999))),
                                address="%d %s" % (int(r.integers(1, 260)), street), locality=name,
                                postcode=postcode, land_use="01", rating="V1", area=int(r.integers(380, 900)),
                                built=None, handover=None, kind="vacant", infill=False, feeder=feeder, loc=loc, nmis=[],
                                street=street))
    # dual occupancy: a granny flat with its own NMI on a few rest-locality houses
    r = K.rng("dual")
    rest_houses = [p for p in W.props if p["kind"] == "house_oo" and p["loc"]["kind"] == "rest"]
    for p in [rest_houses[int(i)] for i in r.choice(len(rest_houses), size=41, replace=False)]:
        n0 = p["nmis"][0]
        nmi = make_nmi(r, used_nmi)
        n = dict(nmi=nmi, feeder=n0["feeder"], hist=n0["hist"], tariff="Residential",
                 address="%s (secondary dwelling)" % p["address"],
                 locality=p["locality"], postcode=n0["postcode"], status="Active",
                 energised=K.add_days(max(p["handover"], dt.date(2012, 1, 1)), int(r.integers(200, 3000))),
                 prop=p, temp=None, transformer=n0["transformer"], secondary=True)
        if n["energised"] > K.BASE:
            n["energised"] = K.add_days(K.BASE, -int(r.integers(30, 400)))
        p["nmis"].append(n)
        W.nmis.append(n)
    # new builds handed over since 1 July 2019 were first supplied on a builder's temporary NMI
    r = K.rng("temp")
    for p in W.props:
        if p["kind"] in ("house_oo", "house_rent") and p["infill"] and p["handover"] >= dt.date(2019, 7, 1):
            n = p["nmis"][0]
            n["temp"] = make_nmi(r, used_nmi)
            n["temp_from"] = K.add_days(p["handover"], -int(r.integers(120, 300)))
    # a knock-down rebuild abolished the old house's NMI at demolition; some old houses had PV
    r = K.rng("old-houses")
    W.old_nmis = []
    for p in W.props:
        n = p["nmis"][0] if p["nmis"] else None
        if n is None or not n.get("temp") or p["loc"]["kind"] not in ("rest", "transfer"):
            continue
        demolished = K.add_days(n["temp_from"], -int(r.integers(7, 60)))
        old = dict(nmi=make_nmi(r, used_nmi), feeder=n["feeder"], hist=n["hist"], tariff="Residential",
                   address=p["address"], locality=p["locality"], postcode=n["postcode"], status="Abolished",
                   energised=None, prop=p, temp=None, transformer=n["transformer"], demolished=demolished, abolished=True)
        if demolished < dt.date(2022, 7, 1) and r.random() < 0.55:
            old["pv"] = True
        W.old_nmis.append(old)
    W.used_nmi = used_nmi
    W.nmi_by = {n["nmi"]: n for n in W.nmis}


# ----------------------------------------------------------------------------------------------------------------
# adoption

def stratified_exponentials(r, starts):
    """Unit exponentials for houses listed with their start dates: quantiles laid out along a low-discrepancy sequence
    in order of start, so every cohort of handovers spans the whole distribution and the houses taking up PV in any
    stretch of time number close to their expectation instead of wandering with sampling noise."""
    n = len(starts)
    order = sorted(range(n), key=lambda i: (starts[i], i))
    q = np.empty(n)
    off = float(r.uniform(0.0, 1.0))
    for rank, i in enumerate(order):
        q[i] = (off + rank * 0.6180339887498949) % 1.0
    q = np.clip(q, 0.5 / n, 1.0 - 0.5 / n)
    return -np.log1p(-q)


def application_dates(r, decided, program=False, close=None, lags=None):
    """received, approved and connected dates for an application lodged on the decision date (lags, when given, are
    the days to approval and from approval to connection)."""
    received = K.business_day(decided)
    a_lag = lags[0] if lags else int(r.integers(2, 16))
    approved = K.business_day(K.add_days(received, a_lag))
    if program:
        connected = K.business_day(K.add_days(max(approved, close), int(r.integers(14, 130))))
    else:
        c_lag = lags[1] if lags else int(r.integers(18, 95))
        connected = K.business_day(K.add_days(approved, c_lag))
    return received, approved, connected


def simulate(W):
    """Every NMI's applications: (nmi, dict(...)) in the order they were lodged."""
    W.apps = []
    W.camp_pool, W.camp_n12, W.camp_systems = {}, {}, {}
    W.camp_new, W.camp_harvest, W.camp_pipeline = {}, {}, {}
    loc_props = {}
    for p in W.props:
        loc_props.setdefault(p["locality"], []).append(p)
    for loc in K.LOCALITIES:
        name, lam = loc["name"], loc["lam"]
        lam_boom = loc.get("lam_boom", lam)
        r = K.rng("adopt", loc.get("stream", name))
        props = loc_props[name]
        oo = [p for p in props if p["kind"] == "house_oo"]
        start = [max(K.WORLD_START, p["handover"]) for p in oo]
        builder = set()
        cands = [i for i, p in enumerate(oo) if p["infill"] and p["handover"] >= dt.date(2019, 7, 1)]
        if cands:
            nb = max(1, int(round(len(cands) * 0.42)))
            builder = set(int(i) for i in r.choice(cands, size=min(nb, len(cands)), replace=False))
        organic = [i for i in range(len(oo)) if i not in builder]
        E = stratified_exponentials(r, [start[i] for i in organic])
        decided = [None] * len(oo)
        for e, i in zip(E, organic):
            decided[i] = adopt_date(start[i], float(e), lam_boom, lam)
        # from the reference date every house still without PV faces the same hazard (the boom long over), so their
        # remaining waits are laid on one even grid: the houses taking up PV in any stretch after it number their
        # expectation to within one
        rs = K.rng("adopt-after", loc.get("stream", name))
        later = [i for i in organic if start[i] < REFERENCE and (decided[i] is None or decided[i] >= REFERENCE)]
        if later:
            u = float(rs.uniform(0.0, 1.0))
            qs = (np.arange(len(later)) + u) / len(later)
            rs.shuffle(qs)
            for qv, i in zip(qs, later):
                decided[i] = adopt_date(REFERENCE, float(-np.log1p(-qv)), lam, lam)
        # a campaign takes most of the households about to buy anyway (those whose own application would have come in
        # the next two years, the nearest most likely) and brings in a few from outside the market
        program = {}
        if loc["kind"] == "campaign":
            c = K.CAMP[loc["camp"]]
            op = c["open"]

            def recv(i):
                return K.business_day(decided[i]) if decided[i] is not None else None
            pool = [i for i in organic if decided[i] is None or recv(i) >= op]
            win_end = K.add_days(op, K.HARVEST_DAYS)
            pipeline = sorted((i for i in pool if decided[i] is not None and recv(i) < win_end),
                              key=lambda i: (decided[i], i))
            clear = K.add_days(op, K.CLEAR_DAYS)
            outside = [i for i in pool if decided[i] is None or recv(i) >= clear]
            rc = K.rng("convert", c["key"])
            off = float(rc.uniform(0, 1))
            harvested = []
            for rank, i in enumerate(pipeline):
                tau = (recv(i) - op).days / float(K.HARVEST_DAYS)
                q = K.HARVEST_Q0 + (K.HARVEST_Q1 - K.HARVEST_Q0) * tau
                if (off + rank * 0.6180339887498949) % 1.0 < q:
                    harvested.append(i)
            n_new = int(round(K.NEW_B * (1.0 + c["eps"]) * len(pool)))
            new = [outside[int(j)] for j in rc.choice(len(outside), size=n_new, replace=False)]
            n12 = sum(1 for i in organic if decided[i] is not None and op - dt.timedelta(days=365) <= recv(i) < op)
            W.camp_pool[c["key"]], W.camp_n12[c["key"]] = len(pool), n12
            W.camp_systems[c["key"]] = len(harvested) + len(new)
            W.camp_new[c["key"]], W.camp_harvest[c["key"]], W.camp_pipeline[c["key"]] = len(new), len(harvested), len(pipeline)
            span = (c["close"] - c["open"]).days
            for i in harvested + new:
                program[i] = K.add_days(c["open"], int(rc.integers(4, span + 40)))
                decided[i] = None
        # the days to approval and connection, spread evenly along the order in which the houses applied
        lag_of, rl = {}, K.rng("lags", loc.get("stream", name))
        o1, o2 = float(rl.uniform(0, 1)), float(rl.uniform(0, 1))
        for rank, i in enumerate(sorted((i for i in organic if decided[i] is not None and i not in program),
                                        key=lambda i: (decided[i], i))):
            lag_of[i] = (2 + int(((o1 + rank * 0.6180339887498949) % 1.0) * 6),
                         8 + int(((o2 + rank * 0.7548776662466927) % 1.0) * 17))
        # build the applications
        for i, p in enumerate(oo):
            n = p["nmis"][0]
            if i in builder:
                add_builder_system(W, r, n, p)
            elif i in program:
                add_program_system(W, r, n, p, loc["camp"], program[i])
            elif decided[i] is not None and decided[i] <= dt.date(2026, 12, 31):
                add_organic_system(W, r, n, decided[i], lags=lag_of[i])
            maybe_withdrawn(W, r, n, decided[i] if i not in program else program[i], p)
        # rented houses, townhouses, units
        for p in props:
            if p["kind"] == "house_rent":
                mult = 0.05
            elif p["kind"] == "town":
                mult = 0.02 if p["rating"] == "R1" else 0.01
            else:
                continue
            n = p["nmis"][0]
            if p["infill"] and p["handover"] >= dt.date(2019, 7, 1) and p["kind"] == "house_rent" and r.random() < 0.35:
                add_builder_system(W, r, n, p)
                continue
            s = max(K.WORLD_START, p["handover"])
            t = adopt_date(s, float(r.exponential(1.0)), lam_boom * mult, lam * mult)
            if t is not None and t <= dt.date(2026, 12, 31):
                add_organic_system(W, r, n, t)
        # secondary dwellings (granny flats) rarely carry their own PV
        for p in props:
            for n in p["nmis"][1:]:
                if r.random() < 0.12:
                    add_organic_system(W, r, n, K.add_days(max(n["energised"], dt.date(2014, 1, 1)), int(r.integers(30, 2500))))
        # the old houses' systems, removed at demolition
        for o in [x for x in W.old_nmis if x["locality"] == name and x.get("pv")]:
            lo_d = dt.date(2010, 3, 1)
            hi_d = K.add_days(o["demolished"], -400)
            if hi_d <= lo_d:
                continue
            dd = K.add_days(lo_d, int(r.integers(0, (hi_d - lo_d).days)))
            app = add_organic_system(W, r, o, dd)
            app["removed"] = o["demolished"]
            app["old"] = True
        # business NMIs
        for p in props:
            if p["kind"] != "biz":
                continue
            s = max(dt.date(2011, 1, 1), p["handover"])
            t = K.add_days(s, int(r.exponential(4200)))
            if t <= dt.date(2026, 12, 31):
                add_organic_system(W, r, p["nmis"][0], t, kind="biz")
    finish(W)


def add_system(W, r, n, received, approved, connected, kind="res", program=None, builder=False):
    kw, kwp = inverter_size(r, connected, kind)
    app = dict(nmi=n["nmi"], type="New", received=received, approved=approved, connected=connected, kw=kw, kwp=kwp,
               battery=0.0, program=program, builder=builder, status="Connected", n=n, removed=None)
    W.apps.append(app)
    return app


def add_organic_system(W, r, n, decided, kind="res", lags=None):
    received, approved, connected = application_dates(r, decided, lags=lags)
    return add_system(W, r, n, received, approved, connected, kind=kind)


def add_builder_system(W, r, n, p):
    """Installed by the builder before handover on the temporary supply; the distributor connects it at handover
    and moves the record to the permanent NMI."""
    handover = p["handover"]
    received = K.business_day(K.add_days(handover, -int(r.integers(40, 110))))
    approved = K.business_day(K.add_days(received, int(r.integers(3, 15))))
    connected = K.business_day(K.add_days(handover, int(r.integers(0, 12))))
    app = add_system(W, r, n, received, approved, connected, builder=True)
    app["installed"] = K.business_day(K.add_days(handover, -int(r.integers(10, 45))))
    return app


def add_program_system(W, r, n, p, camp, decided):
    c = K.CAMP[camp]
    received, approved, connected = application_dates(r, decided, program=True, close=c["close"])
    app = add_system(W, r, n, received, approved, connected, program="SS-%s-%s" % (camp[-2:], camp[:3]))
    # the appointed installer's standard packages
    kw = float(r.choice([5.0, 6.0, 8.0, 8.2, 10.0], p=[0.46, 0.12, 0.20, 0.08, 0.14]))
    app["kw"], app["kwp"] = kw, round(kw * float(r.choice([1.1, 1.2, 1.32])), 2)
    app["installer"] = PROGRAM_INSTALLER[c["installer"]]
    return app


def maybe_withdrawn(W, r, n, decided, p):
    """Some households lodge an application and withdraw it (a quote declined, a roof that needed replacing first)."""
    if r.random() >= 0.035:
        return
    base = decided if decided is not None else K.add_days(dt.date(2013, 1, 1), int(r.integers(0, 4800)))
    when = K.add_days(base, -int(r.integers(120, 900)))
    if when < max(K.WORLD_START, p["handover"]) or when > dt.date(2026, 7, 31):
        return
    received = K.business_day(when)
    W.apps.append(dict(nmi=n["nmi"], type="New", received=received,
                       approved=K.business_day(K.add_days(received, int(r.integers(2, 14)))) if r.random() < 0.6 else None,
                       connected=None, kw=None, kwp=None, battery=0.0, program=None, builder=False, status="Withdrawn",
                       n=n, removed=None, withdrawn=K.business_day(K.add_days(received, int(r.integers(10, 120))))))


def finish(W):
    """Alterations, removals, the base-date statuses, program withdrawals, battery retrofits."""
    r = K.rng("finish")
    rb = K.rng("battery-product")
    new_apps = []
    for a in W.apps:
        if a["status"] != "Connected" or a.get("old"):
            continue
        c = a["connected"]
        # a new system installed with a battery
        if a["type"] == "New" and c.year >= 2020 and r.random() < (0.10 if c.year >= 2023 else 0.06):
            a["bat"] = battery_product(rb)
            a["battery"] = a["bat"]["total"]
        if a["builder"] or a["program"]:
            p_alt = 0.05
        elif c.year <= 2012:
            p_alt = 0.36
        elif c.year <= 2016:
            p_alt = 0.16
        elif c.year <= 2020:
            p_alt = 0.07
        else:
            p_alt = 0.035
        if r.random() < p_alt:
            lo = max(dt.date(2016, 1, 1), K.add_days(c, 900))
            if lo < dt.date(2026, 8, 1):
                when = K.add_days(lo, int(r.integers(0, max(1, (dt.date(2026, 8, 20) - lo).days))))
                received = K.business_day(when)
                approved = K.business_day(K.add_days(received, int(r.integers(2, 14))))
                connected = K.business_day(K.add_days(approved, int(r.integers(14, 70))))
                battery_retro = connected.year >= 2021 and r.random() < 0.45
                bat = None
                if battery_retro:
                    kw = max(a["kw"], 5.0)
                    bat = battery_product(rb)
                    batt = bat["total"]
                else:
                    kw = float(r.choice([5.0, 6.0, 8.0, 10.0], p=[0.35, 0.15, 0.30, 0.20]))
                    kw = min(max(kw, a["kw"] + 1.0), 30.0) if kw <= a["kw"] else kw
                    batt, bat = a["battery"], a.get("bat")
                new_apps.append(dict(nmi=a["nmi"], type="Alteration", received=received, approved=approved,
                                     connected=connected, kw=kw, kwp=round(kw * float(r.choice([1.1, 1.2, 1.32])), 2),
                                     battery=batt, bat=bat, program=None, builder=False, status="Connected",
                                     n=a["n"], removed=None, alters=a))
    W.apps.extend(new_apps)
    # removals (house demolished for a rebuild, or panels taken off at a re-roof and not reinstated)
    altered = set(id(x["alters"]) for x in new_apps)
    for a in W.apps:
        if a["status"] == "Connected" and a["type"] == "New" and not a["builder"] and id(a) not in altered and \
                not a.get("old") and r.random() < 0.004:
            a["removed"] = K.add_days(a["connected"], int(r.integers(700, 3500)))
            if a["removed"] > dt.date(2026, 8, 25):
                a["removed"] = None
    # statuses at the base date: applications received but not yet connected are Approved or Under assessment
    for a in W.apps:
        if a["status"] == "Withdrawn":
            a["withdrawn"] = min(a["withdrawn"], K.BASE)      # withdrawn by the customer before the extract
            continue
        if a["received"] > K.BASE:
            a["status"] = "future"
        elif a["connected"] > K.BASE:
            a["status"] = "Approved" if a.get("approved") and a["approved"] <= K.BASE else "Under assessment"
            if a["status"] == "Under assessment":
                a["approved"] = None
            a["connected_actual"] = a["connected"]
            a["connected"] = None
        elif a.get("removed"):
            a["status"] = "Removed"
    W.apps = [a for a in W.apps if a["status"] != "future"]
    # program contracts cancelled after the installer lodged the application
    for c in K.CAMPAIGNS:
        rc = K.rng("cancel", c["key"])
        locp = [p for p in W.props if p["locality"] == c["suburb"] and p["kind"] == "house_oo"]
        n_cancel = int(rc.integers(2, 6))
        for p in [locp[int(j)] for j in rc.choice(len(locp), size=n_cancel, replace=False)]:
            n = p["nmis"][0]
            received = K.business_day(K.add_days(c["open"], int(rc.integers(10, 70))))
            W.apps.append(dict(nmi=n["nmi"], type="New", received=received, approved=None, connected=None, kw=None,
                               kwp=None, battery=0.0, program="SS-%s-%s" % (c["key"][-2:], c["key"][:3]), builder=False,
                               status="Withdrawn", n=n, removed=None,
                               withdrawn=K.business_day(K.add_days(received, int(rc.integers(10, 60)))),
                               installer=PROGRAM_INSTALLER[c["installer"]]))
    # installers on organic applications
    for a in W.apps:
        if "installer" not in a:
            a["installer"] = INSTALLERS[int(r.integers(0, len(INSTALLERS)))]
    W.apps.sort(key=lambda a: (a["received"], a["nmi"], a["type"]))
    for k, a in enumerate(W.apps):
        a["app_id"] = "EG%07d" % (2100000 + k * 7 + int(r.integers(0, 6)))


def legacy_rows(W):
    """Applications lodged before the July 2019 migration carry panel capacity only in the register; their inverters
    are in the legacy equipment table, keyed by the legacy application number. The legacy system never reissued a
    number: a draw that repeats one already issued is replaced from a second stream, so the first stream (and every
    inverter count drawn from it) is unchanged and the join is one to one."""
    r = K.rng("legacy")
    spare = K.rng("legacy", "renumber")
    issued = set()
    out = []
    for a in W.apps:
        if a["received"] < K.MIGRATION and a["status"] != "Withdrawn":
            no = int(r.integers(10000, 999999))
            while no in issued:
                no = int(spare.integers(10000, 999999))
            issued.add(no)
            a["legacy_no"] = "LG-%06d" % no
            count = 1 if a["kw"] <= 5.0 or r.random() < 0.7 else 2
            out.append((a["legacy_no"], a["kw"], count))
    return out


# ----------------------------------------------------------------------------------------------------------------
# the national DER Register, as the distributor extracts it for one zone substation

# Home battery products: brand, model, module size (kWh), whether the product is modular, its market share, and how
# the installer's commissioning app lodges a modular product's devices with the DER Register: one device per module
# carrying the module's size ("module"), or one device per module each carrying the system's total ("system").
BATTERIES = [
    dict(brand="Tesla", model="Powerwall 2", kwh=13.5, modular=False, share=0.25, lodged="module"),
    dict(brand="BYD", model="Battery-Box Premium HVS", kwh=2.56, modular=True, share=0.24, lodged="module", n=(3, 5)),
    dict(brand="Sungrow", model="SBR HV battery", kwh=3.2, modular=True, share=0.17, lodged="system", n=(3, 5)),
    dict(brand="Alpha ESS", model="SMILE-G3 battery", kwh=10.1, modular=False, share=0.12, lodged="module"),
    dict(brand="LG Energy Solution", model="RESU 10H Prime", kwh=9.6, modular=False, share=0.08, lodged="module"),
    dict(brand="GoodWe", model="Lynx Home U", kwh=5.4, modular=True, share=0.14, lodged="module", n=(2, 3)),
]
INVERTERS = [("Fronius", "Primo"), ("SMA", "Sunny Boy"), ("Sungrow", "SG-RS"), ("Goodwe", "DNS"),
             ("Huawei", "SUN2000-L1"), ("Enphase", "IQ8 system"), ("SolarEdge", "Home Wave"), ("Growatt", "MIN TL-X")]


def battery_product(r):
    """The battery a household buys: a single unit, or a modular product of two to five modules. The connection
    application states the system's total storage."""
    b = BATTERIES[int(r.choice(len(BATTERIES), p=[x["share"] for x in BATTERIES]))]
    count = int(r.integers(b["n"][0], b["n"][1] + 1)) if b["modular"] else 1
    return dict(brand=b["brand"], model=b["model"], module=b["kwh"], count=count, lodged=b["lodged"],
                total=round(b["kwh"] * count, 2))


def der_register(W):
    """Device rows: one per inverter and one per battery device. Installers lodge within days of installation; a
    builder's system is lodged against the temporary supply NMI on the job sheet. The extract is as at 31 August
    2026, and Mirrabee's extraction stamps each AC connection with the feeder its NMI was on when it was lodged."""
    r = K.rng("der")
    ac_seq = [400000]

    def next_ac():
        ac_seq[0] += int(r.integers(3, 40))
        return "AC%07d" % ac_seq[0]

    W.der_systems = []
    by_app = {}
    for a in sorted(W.apps, key=lambda x: (x.get("connected") or x.get("connected_actual") or x["received"], x["nmi"])):
        if a["status"] == "Withdrawn":
            continue
        if a["status"] in ("Approved", "Under assessment"):
            # installed and awaiting the meter change, or not yet installed
            done = a["received"] + dt.timedelta(days=35)
            if a["status"] == "Under assessment" or done > K.BASE or r.random() < 0.5:
                continue
            installed = K.add_days(K.BASE, -int(r.integers(5, 30)))
        elif a["builder"]:
            installed = a["installed"]
        else:
            installed = K.add_days(a["connected"], -int(r.integers(0, 12)))
        if r.random() < 0.006:
            continue                      # never lodged by the installer
        lag = int(r.choice([1, 2, 3, 5, 8, 12, 18, 26, 35], p=[0.10, 0.12, 0.14, 0.16, 0.16, 0.12, 0.10, 0.06, 0.04]))
        registered = K.business_day(K.add_days(installed, lag))
        if registered > K.BASE:
            continue                      # not yet on the register at the extract
        n = a["n"]
        use_temp = a["builder"] and n.get("temp") and installed < n["prop"]["handover"]
        nmi10 = n["temp"] if use_temp else n["nmi"]
        nmi_out = nmi10 + K.nmi_checksum(nmi10) if registered >= K.PORTAL_SWITCH else nmi10
        ac = next_ac()
        status, decom = "Active", None
        # an alteration's new connection: the old connection is decommissioned, or left active by the installer
        # (never one that carries a battery, which the new connection lists again)
        if a["type"] == "Alteration":
            old = by_app.get(id(a.get("alters")), [])
            for o in old:
                if r.random() < 0.72 or o["storage"] > 0:
                    o["status"], o["decom"] = "Decommissioned", registered
                else:
                    o["left_active"] = registered
        if a.get("removed"):
            if r.random() < 0.5:
                status, decom = "Decommissioned", K.add_days(a["removed"], int(r.integers(5, 60)))
                if decom > K.BASE:
                    status, decom = "Active", None
        sysrec = dict(app=a, ac=ac, nmi=nmi_out, nmi10=nmi10, perm=n["nmi"], feeder=feeder_on(n, registered),
                      registered=registered, status=status, decom=decom, installer=a["installer"], kw=a["kw"],
                      battery=a["battery"], devices=[])
        brand, family = INVERTERS[int(r.integers(0, len(INVERTERS)))]
        # a larger system often runs two inverters (an east and a west string, or a business roof)
        n_inv = 2 if (a["kw"] >= 10 and r.random() < (0.5 if a["kw"] >= 15 else 0.22)) else 1
        if brand == "Enphase":
            n_inv = 1                     # a microinverter system is lodged as one device
        each = round(a["kw"] / n_inv, 2)
        model = family if brand == "Enphase" else "%s %.1f" % (family, each)
        # the older installer portal asked for one rating per inverter and installers entered the connection's
        # total there, so an older two-inverter lodgement carries the total on both inverter rows
        rated = a["kw"] if (n_inv > 1 and registered < K.PORTAL_SWITCH) else each
        for k in range(n_inv):
            sysrec["devices"].append(dict(type="Inverter", brand=brand, model=model, rated=rated, storage=None))
        if a["battery"] and a["battery"] > 0:
            bt = a["bat"]
            sysrec["devices"].extend(battery_devices(bt))
            sysrec["storage"] = bt["total"]
        else:
            sysrec["storage"] = 0.0
        W.der_systems.append(sysrec)
        by_app.setdefault(id(a), []).append(sysrec)
    return W.der_systems


def battery_devices(bt):
    return [dict(type="Battery", brand=bt["brand"], model=bt["model"], rated=None,
                 storage=bt["total"] if bt["lodged"] == "system" else bt["module"]) for _ in range(bt["count"])]


def settle_ask_bins(W):
    """Keep each feeder's DER Register inverter capacity and battery storage clear of a rounding edge (the asks are
    graded to the nearest 10 kW and 10 kWh): where a feeder's total sits within a kilowatt of one, an old connection
    an installer left active after an alteration is recorded as decommissioned on the day its replacement was lodged,
    or a household's modular battery carries one module more or fewer. Neither touches the connection register's
    capacity, so the call is unchanged."""
    nmi_by = {n["nmi"]: n for n in W.nmis}
    BAT = {b["model"]: b for b in BATTERIES}

    def totals():
        inv, bat = collections.defaultdict(float), collections.defaultdict(float)
        for s in W.der_systems:
            if s["status"] == "Active" and s["perm"] in nmi_by:
                f = nmi_by[s["perm"]]["feeder"]
                inv[f] += s["kw"]
                bat[f] += s["storage"]
        return inv, bat

    def room(x):
        k = x / 10.0
        return abs((k - math.floor(k)) - 0.5)

    for _ in range(60):
        inv, bat = totals()
        bad_c = [f for f in K.FEEDERS if room(inv[f]) < 0.1]
        bad_b = [f for f in K.FEEDERS if room(bat[f]) < 0.1]
        if not bad_c and not bad_b:
            return
        for f in bad_c:
            cand = [s for s in W.der_systems if s.get("left_active") and s["status"] == "Active" and s["perm"] in nmi_by
                    and nmi_by[s["perm"]]["feeder"] == f]
            s = cand[0]
            s["status"], s["decom"] = "Decommissioned", s.pop("left_active")
        for f in bad_b:
            cand = [s for s in W.der_systems if s["status"] == "Active" and s["perm"] in nmi_by and s["storage"] > 0
                    and nmi_by[s["perm"]]["feeder"] == f and BAT[s["app"]["bat"]["model"]]["modular"]]
            bt = cand[0]["app"]["bat"]
            lo, hi = BAT[bt["model"]]["n"]
            bt["count"] += 1 if bt["count"] < hi else -1
            bt["total"] = round(bt["module"] * bt["count"], 2)
            for a in W.apps:
                if a.get("bat") is bt:
                    a["battery"] = bt["total"]
            for s in W.der_systems:
                if s["app"].get("bat") is bt:
                    s["devices"] = [d for d in s["devices"] if d["type"] != "Battery"] + battery_devices(bt)
                    s["storage"] = bt["total"]
    raise AssertionError("ask bins did not settle")


def reallocations(W):
    """The distributor's NMI re-allocation log: every new build's temporary supply abolished at handover, and a few
    NMIs re-keyed for other reasons."""
    r = K.rng("realloc")
    out = []
    for n in W.nmis:
        if n.get("temp"):
            out.append((n["temp"], n["nmi"], n["prop"]["handover"], "Builder's temporary supply abolished; permanent supply connected"))
    others = [n for n in W.nmis if not n.get("temp") and n["tariff"] == "Residential"]
    for n in [others[int(i)] for i in r.choice(len(others), size=29, replace=False)]:
        old = make_nmi(r, W.used_nmi)
        when = K.add_days(dt.date(2019, 8, 1), int(r.integers(0, 2500)))
        reason = str(r.choice(["NMI created in error; replaced by the existing NMI for the premises",
                               "Duplicate NMI raised by retailer; merged"]))
        out.append((old, n["nmi"], when, reason))
    out.sort(key=lambda t: (t[2], t[0]))
    return out


def never_applied(W):
    """Houses and units on the rates roll whose owners have never applied for PV (a shaded or heritage roof, a strata
    roof the body corporate has not opened up). Drawn last, each locality on its own stream, so nothing drawn before
    moves; every one sits on a street of its locality, on the feeder and transformer of a neighbour."""
    used_prop = {p["property_no"] for p in W.props}
    W.no_pv = {}
    for loc in K.LOCALITIES:
        name = loc["name"]
        r = K.rng("no-pv", loc.get("stream", name))
        mine = [p for p in W.props if p["locality"] == name and p["kind"] in ("house_oo", "house_rent", "town", "unit")]
        streets = sorted({p["street"] for p in mine})
        by_street = {}
        for p in mine:
            by_street.setdefault(p["street"], p)
        n_units = loc["res"] - loc["oo"] - loc["rent"] - loc["town"]
        k = {"house_oo": int(r.integers(6, 39)), "house_rent": int(r.integers(2, 20)), "unit": int(r.integers(3, 28))}
        while k["house_oo"] % 10 == 0:
            k["house_oo"] += 1
        while k["house_rent"] % 10 == 0:
            k["house_rent"] += 1
        while (n_units + k["unit"]) % 10 == 0 or (k["house_oo"] + k["house_rent"] + k["unit"]) % 10 == 0:
            k["unit"] += 1
        lo, hi = loc["built"]
        W.no_pv[name] = dict(k)
        for kind in ("house_oo", "house_rent", "unit"):
            for _ in range(k[kind]):
                street = streets[int(r.integers(0, len(streets)))]
                nb = by_street[street]
                n0 = nb["nmis"][0]
                built = int(r.integers(lo, hi + 1))
                handover = dt.date(built, int(r.integers(1, 13)), int(r.integers(1, 28)))
                prop_no = "%07d" % int(r.integers(1000000, 9999999))
                while prop_no in used_prop:
                    prop_no = "%07d" % int(r.integers(1000000, 9999999))
                used_prop.add(prop_no)
                if kind == "unit":
                    lu, rating = "08", ("R1" if r.random() < 0.45 else "R2")
                    lot = "%dBUP%06d" % (int(r.integers(1, 60)), int(r.integers(100000, 110000)))
                    addr = "%d/%d %s" % (int(r.integers(1, 48)), int(r.integers(1, 200)), street)
                    area = 0
                else:
                    lu, rating = "02", ("R1" if kind == "house_oo" else "R2")
                    plan = "RP" if built < 2000 else "SP"
                    lot = "%d%s%06d" % (int(r.integers(1, 400)), plan, int(r.integers(100000, 399999)))
                    addr = "%d %s" % (int(r.integers(1, 260)), street)
                    area = int(r.integers(420, 900)) if name not in ("Myrtle Vale", "Bloodwood") else int(
                        r.integers(4000, 20000))
                p = dict(property_no=prop_no, lot=lot, address=addr, locality=name, postcode=nb["postcode"],
                         land_use=lu, rating=rating, area=area, built=built, handover=handover, kind=kind,
                         infill=False, feeder=nb["feeder"], loc=loc, street=street, no_pv=True)
                W.props.append(p)
                n = dict(nmi=make_nmi(r, W.used_nmi), feeder=n0["feeder"], hist=list(n0["hist"]), tariff="Residential",
                         address=addr, locality=name, postcode=n0["postcode"], status="Active", energised=handover,
                         prop=p, temp=None, transformer=n0["transformer"])
                p["nmis"] = [n]
                W.nmis.append(n)
                W.nmi_by[n["nmi"]] = n
        camp = loc.get("camp")
        if camp in W.camp_pool:
            W.camp_pool[camp] += k["house_oo"]
