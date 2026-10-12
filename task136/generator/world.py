"""The Yarrabin world: properties on the council's rates roll, NMIs in the distributor's network model, the GIS
cross-reference between them, each dwelling's rooftop PV history (organic adoption, builder-installed systems at
handover, Solar Streets program systems, alterations, removals, withdrawn and pending applications) and the
national DER Register's record of each system. Everything is simulated forward from per-locality streams; the
campaign figures are targets the construction meets exactly, and every analysis figure is computed later from the
written files (calc.py)."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

# Organic adoption pace by calendar year (relative units per year): the Solar Bonus Scheme surge of 2010-2012, the
# lull after the feed-in tariff closed, and the steady rise with cheaper panels from 2017.
PACE = {2009: 0.40, 2010: 1.20, 2011: 2.15, 2012: 1.95, 2013: 0.90, 2014: 0.80, 2015: 0.85, 2016: 0.95, 2017: 1.20,
        2018: 1.40, 2019: 1.50, 2020: 1.55, 2021: 1.60, 2022: 1.50, 2023: 1.45, 2024: 1.40, 2025: 1.40, 2026: 1.40,
        2027: 1.40, 2028: 1.40, 2029: 1.40, 2030: 1.40}
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
    else:
        kw = float(r.choice([5.0, 6.0, 8.0, 8.2, 10.0], p=[0.42, 0.12, 0.20, 0.10, 0.16]))
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


def build_places(W):
    """Properties, NMIs and the cross-reference, locality by locality."""
    used_nmi, used_prop = set(), set()
    W.props, W.nmis = [], []
    r_streets = K.rng("streets")
    pool = list(STREETS)
    r_streets.shuffle(pool)
    sidx = 0
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
        lo, hi = loc["built"]
        infill = loc.get("infill", 0)
        # houses built in the estate's own years; infill houses (knock-down rebuilds and splits) 2019 to 2026
        house_idx = [i for i, k in enumerate(kinds) if k.startswith("house")]
        infill_set = set(int(x) for x in r.choice(house_idx, size=infill, replace=False)) if infill else set()
        unit_blocks = {}
        for i, kind in enumerate(kinds):
            street = streets[int(r.integers(0, len(streets)))]
            if i in infill_set:
                handover = K.add_days(dt.date(2019, 3, 1), int(r.integers(0, 2700)))
                built = handover.year
            elif loc["kind"] == "campaign27" and name == "Bindarra Waters":
                # stages handed over 2019 to June 2025
                handover = K.add_days(dt.date(2019, 4, 1), int(r.integers(0, 2245)))
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
                     infill=(i in infill_set) or (name == "Bindarra Waters"), feeder=feeder, loc=loc)
            W.props.append(p)
            nmi = make_nmi(r, used_nmi)
            n = dict(nmi=nmi, feeder=feeder, tariff="Residential", address=addr, locality=name,
                     postcode=postcode, status="Active", energised=handover, prop=p, temp=None,
                     transformer="%s-T%04d" % (feeder, int(r.integers(1, 420))))
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
                     feeder=feeder, loc=loc)
            W.props.append(p)
            nmi = make_nmi(r, used_nmi)
            n = dict(nmi=nmi, feeder=feeder, tariff="Business", address=addr, locality=name, postcode=postcode,
                     status="Active", energised=p["handover"], prop=p, temp=None,
                     transformer="%s-T%04d" % (feeder, int(r.integers(1, 420))))
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
                                built=None, handover=None, kind="vacant", infill=False, feeder=feeder, loc=loc, nmis=[]))
    # dual occupancy: a granny flat with its own NMI on a few rest-locality houses
    r = K.rng("dual")
    rest_houses = [p for p in W.props if p["kind"] == "house_oo" and p["loc"]["kind"] == "rest"]
    for p in [rest_houses[int(i)] for i in r.choice(len(rest_houses), size=41, replace=False)]:
        n0 = p["nmis"][0]
        nmi = make_nmi(r, used_nmi)
        n = dict(nmi=nmi, feeder=n0["feeder"], tariff="Residential", address="%s (secondary dwelling)" % p["address"],
                 locality=p["locality"], postcode=n0["postcode"], status="Active",
                 energised=K.add_days(max(p["handover"], dt.date(2012, 1, 1)), int(r.integers(200, 3000))),
                 prop=p, temp=None, transformer=n0["transformer"], secondary=True)
        if n["energised"] > K.BASE:
            n["energised"] = K.add_days(K.BASE, -int(r.integers(30, 400)))
        p["nmis"].append(n)
        W.nmis.append(n)
    # new builds since 2019 were first supplied on a builder's temporary NMI
    r = K.rng("temp")
    for p in W.props:
        if p["kind"] in ("house_oo", "house_rent") and p["infill"] and p["handover"] >= dt.date(2019, 1, 1):
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
        old = dict(nmi=make_nmi(r, used_nmi), feeder=n["feeder"], tariff="Residential", address=p["address"],
                   locality=p["locality"], postcode=n["postcode"], status="Abolished", energised=None, prop=p, temp=None,
                   transformer=n["transformer"], demolished=demolished, abolished=True)
        if demolished < dt.date(2022, 7, 1) and r.random() < 0.55:
            old["pv"] = True
        W.old_nmis.append(old)
    W.used_nmi = used_nmi
    W.nmi_by = {n["nmi"]: n for n in W.nmis}



# ----------------------------------------------------------------------------------------------------------------
# adoption

def solve_exact(E, H, n_target):
    """A propensity under which exactly n_target of the houses (latent exponentials E over exposures H) adopt."""
    ratio = np.where(H > 0, E / np.maximum(H, 1e-12), np.inf)
    order = np.sort(ratio)
    assert n_target < len(order) and np.isfinite(order[n_target - 1]), (n_target, len(order))
    lo, hi = order[n_target - 1], order[n_target]
    return float(lo + (hi - lo) * 0.5)


def application_dates(r, decided, program=False, close=None):
    """received, approved and connected dates for an application lodged on the decision date."""
    received = K.business_day(decided)
    approved = K.business_day(K.add_days(received, int(r.integers(2, 16))))
    if program:
        connected = K.business_day(K.add_days(max(approved, close), int(r.integers(14, 130))))
    else:
        connected = K.business_day(K.add_days(approved, int(r.integers(18, 95))))
    return received, approved, connected


def simulate(W):
    """Every NMI's applications: (nmi, dict(...)) in the order they were lodged."""
    W.apps = []
    W.camp_pool = {}
    loc_props = {}
    for p in W.props:
        loc_props.setdefault(p["locality"], []).append(p)
    targets_rest = {"Merindah Heights": 0.44, "Hollow Creek": 0.47, "Tanners Flat": 0.36, "Yarrabin North": 0.40,
                    "Myrtle Vale": 0.52, "Coachwood Park": 0.41, "Bloodwood": 0.49, "Jacaranda Gardens": 0.43,
                    "Ferndale Rise": 0.42}
    for loc in K.LOCALITIES:
        name = loc["name"]
        r = K.rng("adopt", loc.get("stream", name))
        props = loc_props[name]
        oo = [p for p in props if p["kind"] == "house_oo"]
        start = np.array([max(K.WORLD_START, p["handover"]) for p in oo])
        E = r.exponential(1.0, len(oo))
        builder = set()
        if name == "Bindarra Waters" or any(p["infill"] for p in oo):
            cands = [i for i, p in enumerate(oo) if p["infill"] and p["handover"] >= dt.date(2019, 1, 1)]
            if name == "Bindarra Waters":
                nb = 112
            else:
                nb = max(1, int(round(len(cands) * 0.42)))
            builder = set(int(i) for i in r.choice(cands, size=min(nb, len(cands)), replace=False))
        if loc["kind"] == "campaign":
            c = K.CAMP[loc["camp"]]
            when, target = c["open"], c["pv_open"]
        elif loc["kind"] == "campaign27":
            c = [x for x in K.CAMPAIGNS_2027 if x["suburb"] == name][0]
            when, target = K.BASE, c["pv_base"] - len(builder)
        else:
            when, target = K.BASE, None
        H = np.array([cum_pace(s, when) for s in start])
        H_eff = H.copy()
        for i in builder:
            H_eff[i] = 0.0          # builder systems are not organic decisions
        if target is None:
            share = targets_rest[name]
            target = int(round(share * len(oo))) - len(builder)
        prop = solve_exact(E, H_eff, target)
        decided = [None] * len(oo)
        for i, p in enumerate(oo):
            if i in builder:
                continue
            t = inv_pace(start[i], E[i] / prop)
            decided[i] = t
        W.loc_prop = getattr(W, "loc_prop", {})
        W.loc_prop[name] = prop
        # campaign conversions among the houses untapped at the opening
        program = {}
        if loc["kind"] == "campaign":
            c = K.CAMP[loc["camp"]]
            pool = [i for i in range(len(oo)) if i not in builder and
                    (decided[i] is None or K.business_day(decided[i]) >= c["open"])]
            # the pool as the generator sees it: untapped at the opening (no successful application before it)
            W.camp_pool[c["key"]] = len(pool)
            rc = K.rng("convert", c["key"])
            chosen = [pool[int(j)] for j in rc.choice(len(pool), size=c["systems"], replace=False)]
            span = (c["close"] - c["open"]).days
            for i in chosen:
                program[i] = K.add_days(c["open"], int(rc.integers(4, span + 40)))
                decided[i] = None
        # build the applications
        for i, p in enumerate(oo):
            n = p["nmis"][0]
            if i in builder:
                add_builder_system(W, r, n, p)
            elif i in program:
                add_program_system(W, r, n, p, loc["camp"], program[i])
            elif decided[i] is not None and decided[i] <= dt.date(2026, 12, 31):
                add_organic_system(W, r, n, decided[i])
            maybe_withdrawn(W, r, n, decided[i] if i not in program else program[i], p)
        # rented houses, townhouses, units
        for p in props:
            if p["kind"] == "house_rent":
                mult = 0.22
            elif p["kind"] == "town":
                mult = 0.08 if p["rating"] == "R1" else 0.03
            else:
                continue
            n = p["nmis"][0]
            p_builder = 0.02 if name == "Bindarra Waters" else 0.35
            if p["infill"] and p["handover"] >= dt.date(2019, 1, 1) and p["kind"] == "house_rent" and r.random() < p_builder:
                add_builder_system(W, r, n, p)
                continue
            s = max(K.WORLD_START, p["handover"])
            t = inv_pace(s, r.exponential(1.0) / (prop * mult))
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
            decided = K.add_days(lo_d, int(r.integers(0, (hi_d - lo_d).days)))
            app = add_organic_system(W, r, o, decided)
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


def add_organic_system(W, r, n, decided, kind="res"):
    received, approved, connected = application_dates(r, decided)
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
    new_apps = []
    for a in W.apps:
        if a["status"] != "Connected" or a.get("old"):
            continue
        c = a["connected"]
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
                if battery_retro:
                    kw = max(a["kw"], 5.0)
                    batt = float(r.choice([9.6, 10.2, 12.8, 13.5, 15.4], p=[0.18, 0.22, 0.20, 0.25, 0.15]))
                else:
                    kw = float(r.choice([5.0, 6.0, 8.0, 10.0], p=[0.35, 0.15, 0.30, 0.20]))
                    kw = min(max(kw, a["kw"] + 1.0), 30.0) if kw <= a["kw"] else kw
                    batt = 0.0
                new_apps.append(dict(nmi=a["nmi"], type="Alteration", received=received, approved=approved,
                                     connected=connected, kw=kw, kwp=round(kw * float(r.choice([1.1, 1.2, 1.32])), 2),
                                     battery=batt, program=None, builder=False, status="Connected", n=a["n"],
                                     removed=None, alters=a))
        # a new system installed with a battery
        if a["type"] == "New" and c.year >= 2020 and r.random() < (0.10 if c.year >= 2023 else 0.06):
            a["battery"] = float(r.choice([9.6, 10.2, 12.8, 13.5, 15.4], p=[0.18, 0.22, 0.20, 0.25, 0.15]))
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
    are in the legacy equipment table, keyed by the legacy application number."""
    r = K.rng("legacy")
    out = []
    for a in W.apps:
        if a["received"] < K.MIGRATION and a["status"] != "Withdrawn":
            a["legacy_no"] = "LG-%06d" % int(r.integers(10000, 999999))
            count = 1 if a["kw"] <= 5.0 or r.random() < 0.7 else 2
            out.append((a["legacy_no"], a["kw"], count))
    return out


# ----------------------------------------------------------------------------------------------------------------
# the national DER Register, as the distributor extracts it for one zone substation

BATTERIES = [("Tesla", "Powerwall 2", 13.5, 1), ("BYD", "Battery-Box Premium HVS", None, 0),
             ("Sungrow", "SBR HV battery", None, 0), ("Alpha ESS", "SMILE-G3 battery", 10.1, 1),
             ("LG Energy Solution", "RESU 10H Prime", 9.6, 1), ("GoodWe", "Lynx Home U", None, 0)]
MODULE_KWH = {"Battery-Box Premium HVS": 2.56, "SBR HV battery": 3.2, "Lynx Home U": 5.4}
BATTERY_SHARE = [0.25, 0.24, 0.17, 0.12, 0.08, 0.14]
INVERTERS = [("Fronius", "Primo"), ("SMA", "Sunny Boy"), ("Sungrow", "SG-RS"), ("Goodwe", "DNS"),
             ("Huawei", "SUN2000-L1"), ("Enphase", "IQ8 system"), ("SolarEdge", "Home Wave"), ("Growatt", "MIN TL-X")]


def battery_spec(r, kwh_target):
    """A battery product near the target size: single-unit products carry their own size; modular products are a
    module count times the module size."""
    brand, model, size, single = BATTERIES[int(r.choice(len(BATTERIES), p=BATTERY_SHARE))]
    if single:
        return brand, model, size, 1
    m = MODULE_KWH[model]
    count = int(min(5, max(2, round(kwh_target / m))))
    return brand, model, round(m * count, 2), count


def der_register(W):
    """Device rows: one per inverter and one per battery module; the AC connection's storage capacity is carried on
    each of its battery rows. Installers lodge within days of installation; a builder's system is lodged against the
    temporary supply NMI on the job sheet."""
    r = K.rng("der")
    rows = []
    ac_seq = [400000]

    def next_ac():
        ac_seq[0] += int(r.integers(3, 40))
        return "AC%07d" % ac_seq[0]

    by_nmi = {}
    for a in W.apps:
        by_nmi.setdefault(a["nmi"], []).append(a)
    W.der_systems = []
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
        if registered > K.DER_RUN:
            continue                      # not yet on the register at the extract
        if registered > K.BASE and a["status"] in ("Connected", "Removed") and a["connected"] <= K.BASE:
            registered = K.BASE           # lodged by the installer before the meter change was completed
        n = a["n"]
        use_temp = a["builder"] and n.get("temp") and installed < n["prop"]["handover"]
        nmi10 = n["temp"] if use_temp else n["nmi"]
        nmi_out = nmi10 + K.nmi_checksum(nmi10) if registered >= K.PORTAL_SWITCH else nmi10
        ac = next_ac()
        status, decom = "Active", None
        # an alteration's new connection: the old connection is decommissioned, or left active by the installer
        if a["type"] == "Alteration":
            old = [x for x in W.der_systems if x["app"] is a.get("alters")]
            for o in old:
                if r.random() < 0.72:
                    o["status"], o["decom"] = "Decommissioned", registered
        if a.get("removed"):
            if r.random() < 0.5:
                status, decom = "Decommissioned", K.add_days(a["removed"], int(r.integers(5, 60)))
                if decom > K.DER_RUN:
                    status, decom = "Active", None
        sysrec = dict(app=a, ac=ac, nmi=nmi_out, nmi10=nmi10, perm=n["nmi"], feeder=n["feeder"], registered=registered,
                      status=status, decom=decom, installer=a["installer"], kw=a["kw"], battery=a["battery"], devices=[])
        brand, model = INVERTERS[int(r.integers(0, len(INVERTERS)))]
        n_inv = 2 if (a["kw"] >= 15 and r.random() < 0.5) else 1
        for k in range(n_inv):
            sysrec["devices"].append(dict(type="Inverter", brand=brand, model=model,
                                          rated=round(a["kw"] / n_inv, 2), storage=None))
        if a["battery"] and a["battery"] > 0:
            bb, bm, size, count = battery_spec(r, a["battery"])
            for k in range(count):
                sysrec["devices"].append(dict(type="Battery", brand=bb, model=bm, rated=None, storage=size))
            sysrec["storage"] = size
        else:
            sysrec["storage"] = 0.0
        W.der_systems.append(sysrec)
    return W.der_systems


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
