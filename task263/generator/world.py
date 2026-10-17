"""The state's community water systems as the program sees them: their wells and the entry points the wells feed,
each well's own water (the 25 PFAS the method reports), the operators' well rotation, and every 2024 to 2026
entry-point sample, the blend of the wells pumping at collection in proportion to their flows. The generator's
clean truth: nothing here is reported, rounded or mislaid."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

D, C = "D", "C"     # a well whose own water carries PFOA or PFOS over the line, and one whose water does not
L, G = "L", "G"     # a well the operators lead with in turn, and one they call on only beside the lead

# the twenty systems on the 2027 PFAS priority list, in the list's order: name, county, population served, and each
# entry point's wells as (number, rated capacity gpm, kind, PFOA, PFOS, role)
LISTED = [
    ("Tillerton", "Hedstrom", 6538, [[(1, 500, D, 19.0, 6.0, L), (2, 500, C, 1.4, 0.7, L), (3, 450, C, 2.2, 1.0, L),
                                     (4, 450, C, 0.8, 0.5, G)]]),
    ("Halloway", "Engvall", 8917, [[(1, 900, D, 18.5, 5.6, L), (2, 900, D, 6.4, 9.8, L), (3, 750, C, 1.9, 1.3, L)]]),
    ("Marsden Lake", "Granlund", 12764, [[(1, 1000, D, 24.0, 6.1, L), (2, 1000, C, 1.6, 0.8, L), (3, 800, C, 1.1, 0.6, G)],
                                       [(4, 700, C, 0.9, 0.5, L)]]),
    ("Westmere", "Sandholm", 3604, [[(1, 300, C, 0.9, 0.7, G), (2, 350, C, 1.5, 1.1, L), (3, 400, D, 13.2, 5.0, L)]]),
    ("Brennan Prairie", "Engvall", 8231, [[(1, 600, C, 2.1, 1.2, L), (2, 700, D, 9.4, 21.0, L)],
                                        [(3, 500, C, 0.7, 0.4, L), (4, 500, C, 1.2, 0.9, L)]]),
    ("Quenby", "Granlund", 5377, [[(1, 750, D, 9.0, 17.5, L), (2, 750, C, 1.8, 2.1, L)]]),
    ("Corrigan", "Hedstrom", 4906, [[(1, 800, D, 8.5, 13.8, L), (2, 650, C, 1.7, 1.5, L)]]),
    ("Lindell", "Engvall", 5843, [[(1, 550, D, 12.4, 7.0, L), (2, 550, C, 2.3, 1.6, L), (3, 500, C, 1.0, 0.6, G)]]),
    ("Ashgrove Falls", "Sandholm", 6612, [[(1, 400, C, 1.3, 1.0, L), (2, 600, D, 14.5, 5.2, L), (3, 600, C, 2.0, 1.4, L)],
                                         [(4, 350, D, 6.9, 9.5, L)]]),
    ("Paxton Creek", "Granlund", 4019, [[(1, 450, D, 11.6, 6.6, L), (2, 400, C, 1.9, 0.9, L)], [(3, 300, C, 0.6, 0.5, L)]]),
    ("Dalby", "Granlund", 3296, [[(1, 350, D, 8.9, 6.0, L), (2, 350, C, 1.4, 0.8, L), (3, 250, C, 2.4, 1.7, G)]]),
    ("Sedgwick", "Hedstrom", 3958, [[(1, 600, D, 10.2, 6.5, L), (2, 500, D, 6.8, 9.6, L)]]),
    ("Kettering Bluff", "Engvall", 2471, [[(1, 400, C, 1.6, 1.3, L), (2, 300, D, 7.0, 9.2, L)]]),
    ("Ivanhoe Ridge", "Hedstrom", 1683, [[(1, 250, D, 8.1, 5.5, L), (2, 250, C, 1.7, 1.0, L)]]),
    ("Fenwick", "Sandholm", 2207, [[(1, 300, C, 1.0, 0.9, L), (2, 300, D, 6.2, 8.4, L)]]),
    ("Vantage", "Hedstrom", 562, [[(1, 150, D, 7.1, 6.3, L)]]),
    ("Norrell", "Engvall", 1764, [[(1, 300, C, 1.3, 0.7, L), (2, 200, D, 6.0, 7.8, L)]]),
    ("Garvey", "Granlund", 1398, [[(1, 200, D, 7.6, 5.1, L), (2, 200, C, 1.1, 0.9, L)]]),
    ("Ellery", "Sandholm", 1094, [[(1, 150, C, 0.8, 0.6, L), (2, 150, D, 6.0, 7.3, L)]]),
    ("Orrin Falls", "Sandholm", 3511, [[(1, 350, C, 1.2, 0.9, L), (2, 350, D, 10.8, 7.4, L), (3, 300, C, 2.0, 1.2, L)]]),
]
LISTED_NAMES = [x[0] for x in LISTED]


def summer(d):
    return d.month in (6, 7, 8, 9)


def profile(r, kind, pfoa, pfos, source="afff"):
    """A well's own water: PFOA and PFOS as given, the other PFAS in the proportions a source of that kind leaves."""
    v = {a: 0.0 for a in K.AN}
    v["PFOA"], v["PFOS"] = pfoa, pfos
    if kind == D:
        v["PFHxS"] = pfos * r.uniform(0.35, 0.9)
        v["PFBS"] = pfos * r.uniform(0.08, 0.3)
        v["PFPeS"] = v["PFHxS"] * r.uniform(0.05, 0.15)
        v["PFHpS"] = pfos * r.uniform(0.02, 0.07)
        v["PFHxA"] = pfoa * r.uniform(0.25, 0.8)
        v["PFPeA"] = pfoa * r.uniform(0.15, 0.6)
        v["PFBA"] = pfoa * r.uniform(0.15, 0.5)
        v["PFHpA"] = pfoa * r.uniform(0.12, 0.4)
        v["PFNA"] = pfoa * r.uniform(0.01, 0.08)
        v["6:2 FTS"] = r.uniform(0.0, 4.0) if source == "afff" else 0.0
    else:
        v["PFHxS"] = pfos * r.uniform(0.2, 0.6)
        v["PFBS"] = pfos * r.uniform(0.2, 0.8)
        v["PFHxA"] = pfoa * r.uniform(0.3, 0.9)
        v["PFPeA"] = pfoa * r.uniform(0.2, 0.7)
        v["PFBA"] = pfoa * r.uniform(0.3, 1.2)
        v["PFHpA"] = pfoa * r.uniform(0.1, 0.4)
    return v


def listed_systems():
    out = []
    for i, (name, county, pop, eps) in enumerate(LISTED):
        r = K.rng("listed", name)
        pws = "%07d" % (4600000 + int(r.integers(1000, 99999)))
        s = dict(name=name, county=county, pop=pop, pws=pws, listed=True, rank=i + 1, eps=[], wells=[])
        for e, wells in enumerate(eps):
            ep = dict(code="EP%02d" % (e + 1), wells=[], offset=int(r.integers(0, 12)),
                      route=int(r.integers(0, 3)))
            for (no, gpm, kind, pfoa, pfos, role) in wells:
                w = dict(no=no, gpm=gpm, kind=kind, role=role, ep=ep["code"], name="Well %d" % no,
                         own=profile(K.rng("profile", name, no), kind, pfoa, pfos), status="Active")
                ep["wells"].append(w)
                s["wells"].append(w)
            s["eps"].append(ep)
        out.append(s)
    return out


def in_service(r, ep, when):
    """The wells pumping at collection: the month's lead, taken in turn among the wells the operators lead with,
    and each other well when demand calls it on (more often in summer, the peak wells more than the rest)."""
    wells = ep["wells"]
    if len(wells) == 1:
        return [wells[0]["no"]]
    leads = [w for w in wells if w["role"] == L]
    lead = leads[(when.year * 12 + when.month + ep["offset"]) % len(leads)]
    on = {lead["no"]}
    for w in wells:
        if w is lead:
            continue
        p = (0.62 if summer(when) else 0.42) if w["role"] == G else (0.45 if summer(when) else 0.25)
        if r.random() < p:
            on.add(w["no"])
    return sorted(on)


def blend(ep, on, flows):
    """The water leaving the entry point: each well's own water in proportion to its flow."""
    tot = sum(flows[n] for n in on)
    own = {w["no"]: w["own"] for w in ep["wells"]}
    return {a: sum(flows[n] * own[n][a] for n in on) / tot for a in K.AN}


def lab_value(r, true, rl):
    """A laboratory result: the concentration with the method's scatter, three significant figures, and a result
    under the reporting limit reported as not detected (None)."""
    v = true * math.exp(r.normal(0, 0.07))
    if v < rl:
        return None
    return float("%.3g" % v)


def _visit_day(r, y, q, route):
    m = 3 * (q - 1) + 1 + route
    d = dt.date(y, m, 1) + dt.timedelta(int(r.integers(2, 26)))
    while d.weekday() >= 5:
        d += dt.timedelta(1)
    return d


def _time(r):
    return dt.time(int(r.integers(8, 15)), int(r.integers(0, 12)) * 5)


def samples(S):
    """Every routine, confirmation and quality-control sample at every entry point of the systems in S, in the
    order the program's samplers took them."""
    out = []
    for s in S:
        for ep in s["eps"]:
            r = K.rng("samples", s["pws"], ep["code"])
            for (y, q) in K.QUARTERS:
                day = _visit_day(r, y, q, ep["route"])
                if s.get("well_from") and day < s["well_from"]:
                    continue
                todo = [(day, "RT")]
                while todo:
                    when, kind = todo.pop(0)
                    t = dt.datetime.combine(when, _time(r))
                    on = in_service(r, ep, t)
                    rate = {w["no"]: w["gpm"] for w in ep["wells"]}
                    flows = {n: rate[n] * (1 + r.normal(0, 0.015)) for n in on}
                    true = blend(ep, on, flows)
                    lr = K.rng("lab", s["pws"], ep["code"], t.isoformat())
                    res = {a: lab_value(lr, true[a], K.RLS[a]) for a in K.AN}
                    x = dict(system=s["name"], pws=s["pws"], ep=ep["code"], when=t, kind=kind, on=on, flows=flows,
                             true=true, res=res, listed=s["listed"])
                    out.append(x)
                    if kind == "RT":
                        if r.random() < 0.06:          # a field duplicate, a second bottle of the same water
                            fr = K.rng("fd", s["pws"], ep["code"], t.isoformat())
                            out.append(dict(x, kind="FD", res={a: lab_value(fr, true[a], K.RLS[a]) for a in K.AN},
                                            when=t + dt.timedelta(minutes=5)))
                        if r.random() < 0.12:          # a field reagent blank, laboratory water opened at the tap
                            out.append(dict(x, kind="FRB", res={a: None for a in K.AN}, true={a: 0.0 for a in K.AN},
                                            when=t + dt.timedelta(minutes=10)))
                        if max(res["PFOA"] or 0, res["PFOS"] or 0) > K.LINE:
                            todo.append((when + dt.timedelta(int(r.integers(7, 15))), "CO"))
    return out


def own_level(w):
    return max(w["own"]["PFOA"], w["own"]["PFOS"])


def grant(capacity_gpm):
    return min(K.CAP, K.DOLLARS_PER_GPM * capacity_gpm)


def golden_grants(S):
    """Each listed system's grant from the wells' own water (the truth, before any sampling)."""
    return {s["name"]: grant(sum(w["gpm"] for w in s["wells"] if w["status"] == "Active" and own_level(w) > K.LINE))
            for s in S}


def walk(order, grants):
    """Down the list in order until the balance does not cover the next grant."""
    left, funded = K.FUND, []
    for name in order:
        g = grants[name]
        if g == 0:
            continue
        if g > left:
            return funded, name, left
        left -= g
        funded.append(name)
    return funded, None, left


# ---------------------------------------------------------------------------------------------- the rest of the state
FULL = {"Tillerton": "Torvik Water Utility", "Halloway": "City of Halvorsen Water Department",
        "Marsden Lake": "Lindvik Lake Municipal Water", "Westmere": "Village of Wikstrom",
        "Brennan Prairie": "Brekken Prairie Water Utility", "Quenby": "Fjelstad Water and Light",
        "Corrigan": "Kesselring Waterworks", "Lindell": "Village of Nesvold",
        "Ashgrove Falls": "Elvholm Falls Water Utility", "Paxton Creek": "Ackerholt Creek Sanitary District",
        "Dalby": "Village of Dalrud", "Sedgwick": "Skogen Municipal Water",
        "Kettering Bluff": "Kjelland Bluff Water Utility", "Ivanhoe Ridge": "Isaksen Ridge Sanitary District No. 1",
        "Fenwick": "Village of Felsbach", "Vantage": "Valdahl Sanitary District", "Norrell": "Village of Nordvold",
        "Garvey": "Glomstad Water Utility", "Ellery": "Town of Ekholm Sanitary District No. 2",
        "Orrin Falls": "Opsahl Falls Water Utility"}

FIRST = ("Oberring Millcombe Elvhaug Foxwick Unterburg Rygaard Pikemont Rognmo Duncott Ryquist Ottberg Wrenford Linhaug Sedgecott "
         "Ottlund Dorningen Fernholt Mjelholm Marlmore Lundnes Oberstedt Claycott Heselheim Bramwood Ottheim Oberwald Wickcott Pedvik "
         "Mosswell Lundhaug Rognby Goldcott Hochberg Mossbury Mollstad Aasland Mossdale Gjerbakk Meadcombe Hovheim Ottnes Kestreldale "
         "Mjelby Meadmere Ostheim Dornberg Wrenmere Wolfingen Redcott Sletrud Fjellberg Marlcombe Neuholt Sedgeton Nesgaard Isakby "
         "Coldcott Ramvang Mossham Strandgaard Voldvik Tealwood Aasstrom Fernmore Vesdahl Gjergaard Wrendale Sollund Clayley Svalvang "
         "Aasvik Ashcott Mjelberg Oakwick Weisswald Kirchberg Nettlewood Jorstad Harebury Ramlund Kesselingen Sorrelwick Strandvang Claywick "
         "Kjelberg Bergvang").split()
SECOND = ["", "", "", " Lake", " Falls", " Prairie", " Ridge", " Creek", " Hollow", " Heights", " Grove", " Valley",
          " Bluff", " Point", " Springs", " Crossing", " Mills", " Corners"]
KINDS = [("%s Water Utility", 0.30), ("Village of %s", 0.22), ("%s Sanitary District No. 1", 0.12),
         ("%s Municipal Water", 0.10), ("%s Mobile Home Park", 0.12), ("%s Estates", 0.08), ("%s Waterworks", 0.06)]

# systems that buy all their water: (name, county, population, seller); a seller named here is a listed system
# or another buyer, so some reach a listed system's wells through another buyer
BUYERS = [
    ("Northgate Sanitary District", "Granlund", 2215, "Marsden Lake"),
    ("Cedar Bend Mobile Home Park", "Engvall", 187, "Northgate Sanitary District"),
    ("Halloway Township Water Utility", "Engvall", 1436, "Halloway"),
    ("Pine Hollow Estates", "Engvall", 352, "Halloway Township Water Utility"),
    ("Corran Rural Water Cooperative", "Hedstrom", 1642, "Corrigan"),
    ("Village of Ridgeway", "Hedstrom", 611, "Corran Rural Water Cooperative"),
    ("Brookfield Estates", "Sandholm", 268, "Corran Rural Water Cooperative"),
    ("Quenby Junction Water Utility", "Granlund", 942, "Quenby"),
    ("Eastfork Mobile Home Park", "Granlund", 156, "Quenby Junction Water Utility"),
    ("Barrow Creek Sanitary District", "Hedstrom", 488, "Lindell"),
    ("Westmere Heights Association", "Sandholm", 318, "Westmere"),
    ("Prairie View Mobile Home Court", "Engvall", 241, "Brennan Prairie"),
    ("Tillerton East Sanitary District", "Hedstrom", 1130, "Tillerton"),
]
# connections that do not carry a listed system's water to anyone today: an emergency tie (the buyer has its own
# wells) and a purchase that ended when the buyer's own well came on
BUYER_FULL = {
    "Northgate Sanitary District": "Tamsholt Sanitary District",
    "Cedar Bend Mobile Home Park": "Oakmere Mobile Home Park",
    "Halloway Township Water Utility": "Halvorsen Township Water Utility",
    "Pine Hollow Estates": "Haldorsen Estates",
    "Corran Rural Water Cooperative": "Hedstrom Rural Water Cooperative",
    "Village of Ridgeway": "Village of Stensrud",
    "Brookfield Estates": "Gunderholm Estates",
    "Quenby Junction Water Utility": "Fjelstad Junction Water Utility",
    "Eastfork Mobile Home Park": "Lundquist Mobile Home Park",
    "Barrow Creek Sanitary District": "Arneberg Sanitary District",
    "Westmere Heights Association": "Wikstrom Heights Association",
    "Prairie View Mobile Home Court": "Kvisler Mobile Home Court",
    "Tillerton East Sanitary District": "Torvik East Sanitary District",
    "Sunrise Meadows Mobile Home Park": "Rodahl Mobile Home Park",
    "Village of Ostrem Lake": "Village of Solberg Lake",
    "Kilby Corners Water Utility": "Hagestad Corners Water Utility",
}
EMERGENCY = [("Village of Ostrem Lake", "Ashgrove Falls", dt.date(2009, 5, 1))]
ENDED = [("Kilby Corners Water Utility", "Paxton Creek", dt.date(2003, 7, 1), dt.date(2025, 6, 30))]


def _name(r, used):
    while True:
        base = FIRST[int(r.integers(0, len(FIRST)))] + SECOND[int(r.integers(0, len(SECOND)))]
        if base in used:
            continue
        used.add(base)
        u, acc = r.random(), 0.0
        for fmt, p in KINDS:
            acc += p
            if u < acc:
                return base, fmt % base
        return base, KINDS[0][0] % base


def other_systems(n=88):
    """The state's other community water systems drawing on wells: names, counties, populations, entry points and
    wells, each well's own water mostly under the reporting limit, some with traces, two over the line."""
    r = K.rng("others")
    used = set(LISTED_NAMES) | {b[0] for b in BUYERS}
    out = []
    for i in range(n):
        base, full = _name(r, used)
        county = K.COUNTIES[int(r.choice(len(K.COUNTIES), p=K.COUNTY_WEIGHTS))]
        mhp = "Mobile Home Park" in full or "Estates" in full
        pop = int(round(math.exp(r.normal(4.6, 0.6)))) if mhp else int(round(math.exp(r.normal(7.4, 1.1))))
        pop = max(pop, 31)
        s = dict(name=base, full=full, county=county, pop=pop, listed=False, eps=[], wells=[])
        n_ep = 1 if pop < 8000 else (2 if r.random() < 0.6 else 1)
        no = 0
        for e in range(n_ep):
            k = 1 if pop < 300 else int(r.choice([1, 2, 3, 4], p=[0.25, 0.4, 0.25, 0.1]))
            ep = dict(code="EP%02d" % (e + 1), wells=[], offset=int(r.integers(0, 12)), route=int(r.integers(0, 3)))
            for j in range(k):
                no += 1
                gpm = int(25 * round(max(30, pop * 0.076 / r.uniform(0.22, 0.4) / k / max(1, n_ep) * 1.1) / 25)) or 25
                trace = r.random() < 0.35
                pfoa = r.uniform(0.6, 2.8) if trace else r.uniform(0.0, 0.7)
                pfos = r.uniform(0.5, 3.0) if trace else r.uniform(0.0, 0.7)
                w = dict(no=no, gpm=gpm, kind=C, role=L, ep=ep["code"], name="Well %d" % no, status="Active",
                         own=profile(K.rng("profile", base, no), C, pfoa, pfos))
                ep["wells"].append(w)
                s["wells"].append(w)
            s["eps"].append(ep)
        out.append(s)
    # two systems with a well over the line that did not apply for a 2027 grant
    for s, (pfoa, pfos) in zip((out[7], out[41]), ((7.4, 3.1), (2.2, 9.8))):
        w = s["wells"][0]
        w["kind"] = D
        w["own"] = profile(K.rng("profile", s["name"], w["no"]), D, pfoa, pfos)
    return out


def assign_ids(S):
    """PWS ids, facility ids and the sample points as the state's inventory numbers them."""
    r = K.rng("ids")
    pws_used, fac = set(), 20017
    for s in S:
        if not s.get("pws"):
            while True:
                p = "%07d" % int(r.integers(4600000, 4699999))
                if p not in pws_used:
                    break
            s["pws"] = p
        pws_used.add(s["pws"])
    for s in sorted(S, key=lambda x: x["pws"]):
        for w in s["wells"]:
            fac += int(r.integers(1, 9))
            w["fid"] = "%d" % fac
    return S


def statewide():
    S = listed_systems() + other_systems()
    for s in S:
        s.setdefault("full", FULL.get(s["name"], s["name"]))
    return assign_ids(S)


SURFACE = [("Port Allard", "Port Ellefsen Water Utility", "Brunnfeld", 21890, 4200, 1.4, 2.1),
           ("Mittelfeld", "City of Myrvold Water Department", "Mittelfeld", 27315, 5500, 1.7, 1.9)]
FROM_SURFACE = [("Sunrise Meadows Mobile Home Park", "Mittelfeld", 214, "Mittelfeld")]


def add_surface(S):
    """Two systems on surface water: one entry point after the treatment plant, its water the lake or river's."""
    for name, full, county, pop, gpm, pfoa, pfos in SURFACE:
        r = K.rng("surface", name)
        ep = dict(code="EP01", wells=[], offset=0, route=int(r.integers(0, 3)))
        w = dict(no=1, gpm=gpm, kind=C, role=L, ep="EP01", name="Treatment Plant", status="Active", plant=True,
                 own=profile(K.rng("profile", name, 1), C, pfoa, pfos))
        ep["wells"].append(w)
        S.append(dict(name=name, full=full, county=county, pop=pop, listed=False, eps=[ep], wells=[w], surface=True))
    return S


def add_buyers(S):
    """The systems that buy all their water, and the connections the register keeps."""
    by_name = {s["name"]: s for s in S}
    conns = []
    for name, county, pop, seller in BUYERS + FROM_SURFACE:
        s = dict(name=name, full=BUYER_FULL.get(name, name), county=county, pop=pop, listed=False, eps=[], wells=[],
                 buyer=True)
        S.append(s)
        by_name[name] = s
    r = K.rng("connections")
    for name, county, pop, seller in BUYERS + FROM_SURFACE:
        start = dt.date(int(r.integers(1972, 2016)), int(r.integers(1, 13)), 1)
        start += dt.timedelta(days=int(K.rng("connection day", name).integers(0, 27)))
        conns.append(dict(buyer=name, seller=seller, kind="Full purchase", start=start, end=None))
    for name, seller, start in EMERGENCY:
        conns.append(dict(buyer=name, seller=seller, kind="Emergency", start=start, end=None))
    for name, seller, start, end in ENDED:
        conns.append(dict(buyer=name, seller=seller, kind="Full purchase", start=start, end=end))
    # the emergency tie's and the ended purchase's buyers draw on their own wells today
    for nm, cty in (("Village of Ostrem Lake", "Sandholm"), ("Kilby Corners Water Utility", "Granlund")):
        s = next(x for x in S if x["full"] == nm or x["name"] == nm.split(" Water")[0]) if any(
            x["full"] == nm for x in S) else None
        if s is None:
            s = dict(name=nm.replace("Village of ", "").replace(" Water Utility", ""), full=BUYER_FULL[nm], county=cty,
                     pop={"Sandholm": 1271, "Granlund": 846}[cty], listed=False, eps=[], wells=[])
            ep = dict(code="EP01", wells=[], offset=int(K.rng("tie", nm).integers(0, 12)), route=1)
            for no, gpm in ((1, 250), (2, 200)) if cty == "Sandholm" else ((1, 200),):
                w = dict(no=no, gpm=gpm, kind=C, role=L, ep="EP01", name="Well %d" % no, status="Active",
                         own=profile(K.rng("profile", nm, no), C, 0.4, 0.6))
                ep["wells"].append(w)
                s["wells"].append(w)
            s["eps"].append(ep)
            if cty == "Granlund":
                s["well_from"] = dt.date(2025, 7, 1)     # its well came on when the purchase ended
            S.append(s)
    return S, conns


def statewide():
    S = listed_systems() + other_systems()
    for s in S:
        s.setdefault("full", FULL.get(s["name"], s["name"]))
    S = add_surface(S)
    S, conns = add_buyers(S)
    for s in S:
        s.setdefault("full", s["name"])
    return add_purchase(assign_ids(add_facilities(S))), conns


def people_reached(S, conns):
    """The people who get their water from the listed systems' wells, by the county they live in: each listed
    system's own customers, and the customers of every system that buys all its water from one, directly or
    through another buyer, while the purchase is in service."""
    seller = {c["buyer"]: c["seller"] for c in conns if c["kind"] == "Full purchase" and c["end"] is None}
    by = {s["name"]: s for s in S}
    root = lambda n: n if n not in seller else root(seller[n])
    out = {}
    for s in S:
        if s["listed"] or (s["name"] in seller and by.get(root(s["name"]), {}).get("listed")):
            out[s["county"]] = out.get(s["county"], 0) + s["pop"]
    return out


# ---------------------------------------------------------------------------------------------- 2025 operations
SEASON = [0.86, 0.87, 0.90, 0.95, 1.05, 1.18, 1.30, 1.26, 1.10, 0.97, 0.90, 0.88]
# wells measured by one meter on a common discharge (listed systems, one in each county, and three elsewhere)
SHARED = [("Marsden Lake", (2, 3)), ("Halloway", (1, 2)), ("Sedgwick", (1, 2)), ("Ashgrove Falls", (1, 3))]
SHARED_OTHER = 3
REPLACED = [("Quenby", 2, dt.date(2025, 6, 12))]          # a meter changed out in the month
EMERGENCY_WELL = ("Corrigan", 3, 400, (dt.date(2025, 7, 22), dt.date(2025, 7, 23), dt.date(2025, 7, 24)))
INACTIVE = [("Marsden Lake", 5, 600, dt.date(2018, 10, 1)), ("Halloway", 4, 450, dt.date(2021, 4, 1))]
PURCHASE = ("Paxton Creek", dt.date(2025, 9, 8), dt.date(2025, 9, 21))   # an emergency tie while a well was rehabbed


def add_facilities(S):
    """The wells the inventory keeps beside the active ones: an emergency well that ran during a main break and two
    wells taken out of service years ago."""
    by = {s["name"]: s for s in S}
    name, no, gpm, days = EMERGENCY_WELL
    s = by[name]
    w = dict(no=no, gpm=gpm, kind=C, role=L, ep="EP01", name="Well %d" % no, status="Emergency", ran=days,
             own=profile(K.rng("profile", name, no), C, 1.2, 0.8))
    s["wells"].append(w)
    s["eps"][0]["standby"] = [w]
    for name, no, gpm, since in INACTIVE:
        w = dict(no=no, gpm=gpm, kind=C, role=L, ep=None, name="Well %d" % no, status="Inactive", since=since,
                 own=None)
        by[name]["wells"].append(w)
    return S


def served(S, conns):
    """Each producing system's customers plus those of every system that takes its water."""
    seller = {c["buyer"]: c["seller"] for c in conns if c["kind"] == "Full purchase" and c["end"] is None}
    by = {s["name"]: s for s in S}
    root = lambda n: n if n not in seller else root(seller[n])
    out = {s["name"]: s["pop"] for s in S if s["wells"]}
    for s in S:
        if s["name"] in seller:
            out[root(s["name"])] += s["pop"]
    return out


def operations_2025(S, conns, X=()):
    """Each active or emergency facility's days in service and gallons in each month of 2025: the month's lead well
    every day, the others when demand calls them (the same rotation the samplers saw, and on a sampling day the wells
    the sampler found running), and the emergency well on the days it ran."""
    pop = served(S, conns)
    seen_on = {}
    for x in X:
        if x["when"].year == 2025:
            seen_on.setdefault((x["system"], x["ep"], x["when"].date()), set()).update(x["on"])
    ops = {}
    for s in S:
        if not s["wells"] or s.get("buyer"):
            continue
        r = K.rng("ops", s["name"])
        gpcd = r.uniform(96, 132)
        cap = sum(w["gpm"] for w in s["wells"] if w["status"] == "Active")
        start_well = s.get("well_from")
        for ep in s["eps"]:
            share = sum(w["gpm"] for w in ep["wells"]) / cap
            for m in range(1, 13):
                days = (dt.date(2025 + m // 12, m % 12 + 1, 1) - dt.date(2025, m, 1)).days
                for w in ep["wells"]:
                    ops.setdefault((s["name"], w["no"], m), [0, 0.0])
                for d in range(1, days + 1):
                    day = dt.date(2025, m, d)
                    if start_well and day < start_well:
                        continue
                    want = pop[s["name"]] * gpcd * share * SEASON[m - 1] * math.exp(r.normal(0, 0.07))
                    if len(ep["wells"]) == 1:
                        w = ep["wells"][0]
                        h = min(r.uniform(21.0, 23.8), want / (60 * w["gpm"]))
                        o = ops[(s["name"], w["no"], m)]
                        o[0] += 1
                        o[1] += 60 * w["gpm"] * h * (1 + r.normal(0, 0.015))
                        continue
                    t = dt.datetime(2025, m, d, 11)
                    on = sorted(set(in_service(r, ep, t)) | seen_on.get((s["name"], ep["code"], day), set()))
                    lead = on[0] if len(on) == 1 else [w["no"] for w in ep["wells"] if w["role"] == L][
                        (t.year * 12 + t.month + ep["offset"]) % len([w for w in ep["wells"] if w["role"] == L])]
                    rate = {w["no"]: w["gpm"] for w in ep["wells"]}
                    h_lead = min(r.uniform(19.0, 22.5), want / (60 * rate[lead]))
                    rest = max(0.0, want - 60 * rate[lead] * h_lead)
                    lags = [n for n in on if n != lead]
                    hours = {lead: h_lead}
                    for n in lags:
                        hours[n] = (rest / (60 * sum(rate[k] for k in lags))) if rest > 0 else r.uniform(1.5, 4.5)
                        hours[n] = min(hours[n], 20.0)
                    for n, h in hours.items():
                        o = ops[(s["name"], n, m)]
                        o[0] += 1
                        o[1] += 60 * rate[n] * h * (1 + r.normal(0, 0.015))
        for w in s["wells"]:
            if w.get("ran"):
                for day in w["ran"]:
                    o = ops.setdefault((s["name"], w["no"], day.month), [0, 0.0])
                    o[0] += 1
                    o[1] += 60 * w["gpm"] * r.uniform(9.0, 13.0)
                for m in range(1, 13):
                    ops.setdefault((s["name"], w["no"], m), [0, 0.0])
    return ops


def pumped_by_county(S, ops):
    """The listed systems' wells' 2025 gallons, by county (the truth, each well once)."""
    by = {s["name"]: s for s in S}
    out = {}
    for (name, no, m), (days, gal) in ops.items():
        s = by[name]
        if s["listed"] and not any(w.get("plant") for w in s["wells"]):
            out[s["county"]] = out.get(s["county"], 0.0) + gal
    return out


def add_purchase(S):
    """The emergency tie of the listed system keyed Paxton Creek (Ackerholt Creek) to a larger system in its county,
    opened while one of its wells was rehabilitated in September 2025 (the water entered the mains, not an entry
    point)."""
    by = {s["name"]: s for s in S}
    hr = next(s for s in S if not s["listed"] and s["county"] == "Granlund" and s["pop"] > 4000 and s["eps"]
              and not s.get("buyer"))
    hr["is_regional"] = True
    pax = by[PURCHASE[0]]
    r = K.rng("purchase")
    days = (PURCHASE[2] - PURCHASE[1]).days + 1
    gal = int(round(sum(r.uniform(150_000, 230_000) for _ in range(days))))
    pax["purchase"] = {PURCHASE[1].month: gal}
    pax["purchase_days"] = {PURCHASE[1].month: days}
    pax["ic_fid"] = "%d" % (int(max(w["fid"] for w in pax["wells"])) + 3)
    pax["ic_name"] = "Emergency interconnect (%s)" % hr["full"].replace(" Water Utility", "").replace("Village of ", "")
    return S
