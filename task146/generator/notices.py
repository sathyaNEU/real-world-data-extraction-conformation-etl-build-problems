"""Ask A's world: the layoff notices employers gave the board, as the clean truth and as the two channels and the case
notes record them.

An employer planning to lay off 20 or more workers gives the board notice at least 30 days before the first layoff,
stating each site's address and the workers to be laid off there and the date of the first layoff. Until 30 June 2026
Employer Services received notices by email and entered them in its register, one row per site, the region coded from
the site's address. From 1 July 2026 employers lodge them on the Employer Portal. The portal's first release takes the
notice header from the business register (name, business number and the employer's registered region) and prints it on
every site line of its notices report; it has no withdrawal function, so an employer withdrawing a notice emails
Employer Services, who note it in their case notes. Employer Services re-keyed the register's open notices onto the
portal in batches as their first layoffs approached, under new portal numbers. An amendment is lodged as a new notice
that replaces the old one, which the portal marks superseded."""
from __future__ import annotations

import datetime as dt
import re

import numpy as np

import common as K

# ---------------------------------------------------------------------------------------------------- places
# territorial authorities: (code, name, region, postcode from, postcode to, main towns)
TAS = [
    ("011", "Far North District", "Northern", 300, 399, ["Kelso Point", "Ardleigh"]),
    ("012", "Marrick District", "Northern", 400, 499, ["Marrick", "Fenwick Bay"]),
    ("013", "Tarrant City", "Northern", 500, 699, ["Tarrant"]),
    ("021", "Port Albany City", "Capital", 1000, 1299, ["Port Albany"]),
    ("022", "Westhaven City", "Capital", 1300, 1499, ["Westhaven"]),
    ("023", "Kingsmere District", "Capital", 1500, 1699, ["Kingsmere", "Larchfield"]),
    ("024", "Ellesmere District", "Capital", 1700, 1899, ["Ellesmere", "Dunmore"]),
    ("031", "Easterfield City", "Eastern", 2000, 2199, ["Easterfield"]),
    ("032", "Catlow District", "Eastern", 2200, 2399, ["Catlow", "Brisley"]),
    ("033", "Wharram District", "Eastern", 2400, 2599, ["Wharram", "Oxenhope"]),
    ("041", "Brackwell City", "Midlands", 3000, 3299, ["Brackwell"]),
    ("042", "Stanmore District", "Midlands", 3300, 3499, ["Stanmore", "Hollins Cross"]),
    ("043", "Renfield District", "Midlands", 3500, 3699, ["Renfield", "Coldbeck", "Oakridge"]),
    ("051", "Kerrigan City", "Western", 4000, 4199, ["Kerrigan"]),
    ("052", "Morven District", "Western", 4200, 4399, ["Morven", "Glenhallow"]),
    ("053", "Pikes Landing District", "Western", 4400, 4599, ["Pikes Landing", "Saltash"]),
    ("061", "Southby City", "Southern", 5000, 5199, ["Southby"]),
    ("062", "Carrow District", "Southern", 5200, 5399, ["Carrow", "Lindell", "Ferngate"]),
    ("071", "Seabrook District", "Coastal", 6000, 6199, ["Seabrook", "Gullhaven"]),
    ("072", "Port Rennie District", "Coastal", 6200, 6399, ["Port Rennie", "Ashby"]),
    ("073", "Linton District", "Coastal", 6400, 6599, ["Linton", "Driftwood"]),
    ("081", "Calder Islands District", "Island", 7000, 7199, ["St Bride's", "Calder"]),
    ("082", "Skerry District", "Island", 7200, 7299, ["Skerry", "Northwick"]),
]
TOWN = {}
for _code, _ta, _reg, _p0, _p1, _towns in TAS:
    for _k, _t in enumerate(_towns):
        TOWN[_t] = dict(ta=_code, ta_name=_ta, region=_reg, pc0=_p0 + 10 * _k, pc1=_p1)
REGION_TOWNS = {r: [t for t, v in TOWN.items() if v["region"] == r] for r in K.REGIONS}
STREETS = ["Main Road", "Station Street", "Wharf Road", "Industrial Drive", "Mill Lane", "High Street", "Quay Street",
           "Factory Road", "Harbour View Road", "Depot Road", "Albert Street", "Market Street", "Kiln Road",
           "Ferry Road", "Gully Road", "Racecourse Road", "Victoria Avenue", "Church Street", "Marina Parade",
           "Saddle Road", "Totara Street", "Rimu Place", "Matai Road", "Kowhai Drive", "Tannery Lane", "Smelter Road"]

GROUPS = ["Agriculture, forestry and fishing", "Mining, energy and utilities", "Manufacturing", "Construction",
          "Wholesale, transport and storage", "Retail trade", "Accommodation and food services",
          "Information and communication", "Financial, insurance and property services",
          "Professional, scientific and technical services", "Administrative and support services",
          "Public administration and safety", "Education and training",
          "Health care, social assistance and other services"]

SURNAMES = ["McAlister", "Fraser", "Paterson", "Kaur", "Ngata", "Wong", "Halloran", "Duncan", "Te Rangi", "Simmons",
            "Brody", "Ferreira", "Gallagher", "Iosefa", "Kingi", "Lindqvist", "Moana", "Nakamura", "O'Brien",
            "Petrovic", "Quinlan", "Rawiri", "Sutcliffe", "Tamatea", "Underwood", "Vaughan", "Whitlock", "Yeoman",
            "Ashdown", "Bellamy", "Crowther", "Dobbs", "Eyre", "Faleolo", "Grieve", "Huang", "Ingram", "Joyce",
            "Kerr", "Lomax", "Maitland", "Norris", "Ormsby", "Pritchard", "Rennie", "Sinclair", "Tuhoe", "Varga"]
PLACES = ["Highfield", "Ridgeway", "Riverbend", "Kauri", "Totara", "Southgate", "Bluewater", "Redcliff", "Greystone",
          "Pinehurst", "Harbourside", "Clearwater", "Northgate", "Summit", "Tasman", "Fernleaf", "Ironbark", "Waterlea"]


def _bn(g):
    """A business number: eight digits and a mod-11 check digit (weights 3,2,7,6,5,4,3,2)."""
    while True:
        d = [int(x) for x in g.integers(1, 10, 1)] + [int(x) for x in g.integers(0, 10, 7)]
        s = sum(a * b for a, b in zip(d, (3, 2, 7, 6, 5, 4, 3, 2)))
        c = (11 - s % 11) % 11
        if c < 10:
            return "%s%d" % ("".join(map(str, d)), c)


def _name(g, group, town, used):
    """An employer's legal name, built the way company names in a register look: a family name, a place, a trade word,
    initials, sometimes an ampersand or a holdings company."""
    sn = SURNAMES[int(g.integers(len(SURNAMES)))]
    sn2 = SURNAMES[int(g.integers(len(SURNAMES)))]
    pl = PLACES[int(g.integers(len(PLACES)))]
    trades = {
        "Construction": ["Builders", "Construction", "Civil", "Scaffolding", "Concrete", "Roofing", "Drainage",
                         "Joinery", "Precast", "Earthworks"],
        "Accommodation and food services": ["Hotels", "Hospitality", "Lodge", "Resorts", "Catering", "Motor Inn",
                                            "Holiday Parks", "Function Centre"],
        "Manufacturing": ["Engineering", "Timber Processors", "Plastics", "Foods", "Packaging", "Metals",
                          "Joinery Manufacturing", "Dairy Products", "Print"],
        "Retail trade": ["Furniture", "Outdoor", "Hardware", "Fashion", "Home Centre", "Pharmacy Group", "Motors"],
        "Wholesale, transport and storage": ["Freight", "Logistics", "Distributors", "Couriers", "Cold Storage",
                                             "Transport"],
        "Agriculture, forestry and fishing": ["Orchards", "Forestry", "Fisheries", "Growers", "Contracting",
                                              "Seafoods"],
        "Mining, energy and utilities": ["Quarries", "Energy", "Minerals", "Drilling Services"],
        "Information and communication": ["Media", "Digital", "Communications", "Software"],
        "Financial, insurance and property services": ["Property Management", "Finance", "Realty", "Insurance Brokers"],
        "Professional, scientific and technical services": ["Consulting", "Surveyors", "Laboratories",
                                                            "Design Partners", "Engineers"],
        "Administrative and support services": ["Cleaning Services", "Security", "Recruitment", "Facilities",
                                                "Labour Hire"],
        "Public administration and safety": ["Services Trust", "Regional Council Enterprises"],
        "Education and training": ["Training Institute", "Learning Centre", "Academy"],
        "Health care, social assistance and other services": ["Healthcare", "Care Homes", "Medical Centre",
                                                              "Community Trust", "Laundry Services"],
    }[group]
    tr = trades[int(g.integers(len(trades)))]
    style = int(g.integers(9))
    if style == 0:
        n = "%s %s Ltd" % (sn, tr)
    elif style == 1:
        n = "%s & %s %s Ltd" % (sn, sn2, tr) if sn != sn2 else "%s Bros %s Ltd" % (sn, tr)
    elif style == 2:
        n = "%s %s Ltd" % (town, tr)
    elif style == 3:
        n = "%s %s Limited" % (pl, tr)
    elif style == 4:
        a, b = "ABCDEFGHJKLMNPRSTW"[int(g.integers(18))], "ABCDEFGHJKLMNPRSTW"[int(g.integers(18))]
        n = "%s%s %s Ltd" % (a, b, tr)
    elif style == 5:
        n = "%s %s (%s) Ltd" % (pl, tr, town)
    elif style == 6:
        n = "%s Group Holdings Ltd" % sn
    elif style == 7:
        n = "The %s %s Company Ltd" % (pl, tr)
    else:
        n = "%s %s %s Ltd" % (sn, pl, tr) if g.random() < 0.5 else "%s's %s Ltd" % (sn, tr)
    k = 2
    base = n
    while n in used:
        n = base.replace(" Ltd", " (%d) Ltd" % k) if " Ltd" in base else base + " (%d)" % k
        k += 1
    used.add(n)
    return n


COINED = ["Corvan", "Tarnex", "Pelora", "Avonmere", "Brackenridge", "Halvard", "Monterra", "Quayside", "Redstone",
          "Sandhurst", "Westmark", "Ashgrove", "Cobalt", "Granite Peak", "Kestrel", "Lakeview", "Marlowe", "Ironsand",
          "Silverfern", "Stonebridge", "Pacific Rim", "Alpine", "Seaview", "Coastline", "Fernbrook", "Northcote"]
NATIVE = ["Kowhai", "Totara", "Rimu", "Manuka", "Matai", "Kauri", "Pohutukawa", "Harakeke", "Rata", "Miro", "Tawa"]
TRADE = {
    "Construction": ["Builders", "Construction", "Civil", "Scaffolding", "Concrete", "Roofing", "Drainage", "Joinery",
                     "Precast", "Earthworks", "Plastering", "Formwork", "Building Services", "Developments", "Homes"],
    "Accommodation and food services": ["Hotels", "Hospitality", "Lodge", "Resorts", "Catering", "Motor Inn", "Holiday Park",
                                        "Function Centre", "Backpackers", "Hotel Group", "Kitchens", "Eateries", "Tavern"],
    "Manufacturing": ["Engineering", "Timber Processors", "Plastics", "Foods", "Packaging", "Metals", "Fabrication",
                      "Dairy Products", "Print", "Furniture", "Meats", "Bakeries", "Coatings"],
    "Retail trade": ["Furniture", "Outdoor", "Hardware", "Fashion", "Home Centre", "Pharmacy", "Motors", "Supplies",
                     "Trade Centre", "Garden Centre", "Books"],
    "Wholesale, transport and storage": ["Freight", "Logistics", "Distributors", "Couriers", "Cold Storage", "Transport",
                                         "Haulage", "Shipping", "Wholesale"],
    "Agriculture, forestry and fishing": ["Orchards", "Forestry", "Fisheries", "Growers", "Contracting", "Seafoods",
                                          "Vineyards", "Farms", "Horticulture"],
    "Mining, energy and utilities": ["Quarries", "Energy", "Minerals", "Drilling", "Aggregates", "Power"],
    "Information and communication": ["Media", "Digital", "Communications", "Software", "Networks", "Studios"],
    "Financial, insurance and property services": ["Property Management", "Finance", "Realty", "Insurance Brokers",
                                                   "Property Group", "Lending"],
    "Professional, scientific and technical services": ["Consulting", "Surveyors", "Laboratories", "Design", "Engineers",
                                                        "Architects", "Planning"],
    "Administrative and support services": ["Cleaning", "Security", "Recruitment", "Facilities", "Labour Hire",
                                            "Staffing", "Services"],
    "Public administration and safety": ["Services Trust", "Council Enterprises", "Community Services"],
    "Education and training": ["Training Institute", "Learning Centre", "Academy", "Education Trust", "Tutoring"],
    "Health care, social assistance and other services": ["Healthcare", "Care Homes", "Medical Centre", "Community Trust",
                                                          "Laundry Services", "Rest Home", "Home Support"],
}
INITIALS = "ABCDGHJKLMNPRSTW"


def _company_name(g, e, used):
    """The employer's legal name as the business register holds it, and the shorter way an Employer Services clerk
    typed it into the email register: family businesses, place names, coined brands and native tree and bird names,
    some re-registered with a year, a few holding companies."""
    pick = lambda xs: xs[int(g.integers(len(xs)))]
    sn, sn2 = pick(SURNAMES), pick(SURNAMES)
    trade = pick(TRADE[e.group])
    town = e.town
    u = g.random()
    if u < 0.20:
        core = "%s %s" % (sn, trade)
    elif u < 0.29:
        core = "%s & %s %s" % (sn, sn2, trade) if sn != sn2 else "%s Brothers %s" % (sn, trade)
    elif u < 0.42:
        core = "%s %s" % (town, trade)
    elif u < 0.52:
        a, b = pick(INITIALS), pick(INITIALS)
        core = pick(["%s & %s %s" % (a, b, sn), "%s.%s. %s %s" % (a, b, sn, trade), "%s %s %s" % (a, sn, trade)])
    elif u < 0.66:
        core = "%s %s" % (pick(COINED), trade)
    elif u < 0.76:
        core = "%s %s" % (pick(NATIVE), trade)
    elif u < 0.82:
        core = "%s Holdings" % pick([sn, pick(COINED), town])
    elif u < 0.88:
        core = "%s %s" % (pick(PLACES), trade)
    else:
        core = "%s Group" % pick([sn, pick(COINED), pick(NATIVE)])
    if g.random() < 0.13:
        core += " (%d)" % int(g.integers(1996, 2024))
    legal = core + " Limited"
    k = 2
    while legal in used:
        legal = "%s (No %d) Limited" % (core, k)
        k += 1
    used.add(legal)
    v = g.random()
    if v < 0.55:
        reg = legal.replace(" Limited", " Ltd")
    elif v < 0.80:
        reg = legal
    elif v < 0.92:
        reg = legal.replace(" Limited", "")
    else:
        reg = legal.replace(" Limited", " Ltd").upper()
    return legal, reg


class Employer:
    pass


class Notice:
    pass


def _local_dt(day, g, h0=8, h1=17):
    return dt.datetime.combine(day, dt.time(int(g.integers(h0, h1)), int(g.integers(0, 60)), int(g.integers(0, 60))))


def _workday(d, step=1):
    while d.weekday() >= 5 or d in K.HOLIDAYS:
        d += dt.timedelta(days=step)
    return d


# the industries whose notices the 2026 layoffs fill, and where
SURGE_GROUPS = {"Construction": 3.0, "Accommodation and food services": 2.6}
SURGE_REGIONS = {"Western": 2.1, "Coastal": 2.3, "Island": 1.9, "Midlands": 1.4}


def simulate():
    g = K.rng("notices")
    used = set()
    emps = []
    # employers: a national tier headquartered in the larger cities and a local tier everywhere
    hq_weights = {"Northern": 0.10, "Capital": 0.48, "Eastern": 0.06, "Midlands": 0.18, "Western": 0.06,
                  "Southern": 0.06, "Coastal": 0.04, "Island": 0.02}
    for k in range(214):
        e = Employer()
        e.national = k < 62
        if e.national:
            e.region = K.REGIONS[int(g.choice(8, p=[hq_weights[r] for r in K.REGIONS]))]
        else:
            e.region = K.REGIONS[int(g.choice(8, p=[0.12, 0.20, 0.10, 0.15, 0.13, 0.09, 0.13, 0.08]))]
        e.town = REGION_TOWNS[e.region][int(g.integers(len(REGION_TOWNS[e.region])))]
        gw = np.array([0.05, 0.03, 0.15, 0.16, 0.08, 0.10, 0.14, 0.02, 0.02, 0.03, 0.06, 0.02, 0.03, 0.11])
        e.group = GROUPS[int(g.choice(len(GROUPS), p=gw / gw.sum()))]
        e.name = _name(g, e.group, e.town, used)      # drawn as before so every later draw of the notice world holds
        e.bn = _bn(g)
        emps.append(e)
    gn = K.rng("employer-names")
    used_n = set()
    for e in emps:
        e.name, e.reg_name = _company_name(gn, e, used_n)
    # notices: dates given from 1 July 2025 to 7 October 2026
    notices = []
    day = dt.date(2025, 7, 1)
    seq_es = {2025: 300, 2026: 0}
    seq_ln = 0
    while day <= K.EXTRACT_PULL:
        if day.weekday() < 5 and day not in K.HOLIDAYS:
            rate = 1.2 + (1.5 if day >= dt.date(2026, 5, 15) else 0.0) + (1.4 if day >= dt.date(2026, 7, 10) else 0.0)
            for _ in range(int(g.poisson(rate))):
                n = Notice()
                n.given = day
                # who gives it: the 2026 layoffs lean on building and hotel employers in the surge regions
                w = np.ones(len(emps))
                if day >= dt.date(2026, 5, 15):
                    for i, e in enumerate(emps):
                        w[i] *= SURGE_GROUPS.get(e.group, 1.0) * (1.0 if e.national else SURGE_REGIONS.get(e.region, 1.0))
                n.emp = emps[int(g.choice(len(emps), p=w / w.sum()))]
                n.type = "Layoff" if g.random() < 0.88 else "Reduced hours"
                # most notices give a month or two; restructures planned well ahead give four to seven months
                if g.random() < (0.42 if n.emp.national else 0.24):
                    lead = int(g.integers(115, 225))
                else:
                    lead = int(np.clip(g.gamma(2.2, 24.0) + 30, 30, 160))
                n.first_layoff = n.given + dt.timedelta(days=lead)
                ns = 1
                if n.emp.national:
                    ns = int(g.choice([1, 2, 3, 4], p=[0.52, 0.26, 0.14, 0.08]))
                elif g.random() < 0.08:
                    ns = 2
                sites = []
                for s in range(ns):
                    if n.emp.national:
                        # national employers' sites fall where the work is, rarely at the head office's own region
                        sw = np.array([0.11, 0.13, 0.09, 0.15, 0.15, 0.09, 0.17, 0.11])
                        if day >= dt.date(2026, 5, 15):
                            sw = sw * np.array([SURGE_REGIONS.get(r, 1.0) for r in K.REGIONS])
                        reg = K.REGIONS[int(g.choice(8, p=sw / sw.sum()))]
                    else:
                        reg = n.emp.region if g.random() < 0.9 else K.REGIONS[int(g.integers(8))]
                    town = REGION_TOWNS[reg][int(g.integers(len(REGION_TOWNS[reg])))]
                    workers = int(np.clip(round(g.lognormal(3.45, 0.62)), 6, 420))
                    sites.append(dict(town=town, region=reg, workers=workers,
                                      street="%d %s" % (int(g.integers(1, 480)), STREETS[int(g.integers(len(STREETS)))]),
                                      postcode=TOWN[town]["pc0"] + int(g.integers(0, 9))))
                tot = sum(s["workers"] for s in sites)
                if tot < 20:
                    sites[0]["workers"] += 20 - tot
                n.sites = sites
                n.channel = "email" if day <= K.REGISTER_FROZEN else "portal"
                if n.channel == "email":
                    y = day.year
                    seq_es[y] = seq_es.get(y, 0) + int(g.integers(1, 3))
                    n.es_ref = "ES/%02d/%04d" % (y % 100, seq_es[y])
                    n.ln = None
                else:
                    n.ln = None
                    n.es_ref = None
                    n.lodged = _local_dt(day, g, 7, 20)
                n.withdrawn = None
                n.superseded_by = None
                n.replaces = None
                n.rekeyed = None
                notices.append(n)
        day += dt.timedelta(days=1)
    # amendments on the portal: a new notice replacing the old (dates moved or sites trimmed)
    portal = [n for n in notices if n.channel == "portal" and n.type == "Layoff"]
    for n in [portal[int(i)] for i in g.choice(len(portal), 11, replace=False)]:
        a = Notice()
        a.__dict__.update({k: v for k, v in n.__dict__.items()})
        a.given = _workday(n.given + dt.timedelta(days=int(g.integers(9, 40))))
        if a.given > K.EXTRACT_PULL:
            continue
        a.sites = [dict(s) for s in n.sites]
        if g.random() < 0.55:
            a.first_layoff = n.first_layoff + dt.timedelta(days=int(g.integers(10, 50)))
        else:
            for s in a.sites:
                s["workers"] = max(4, int(round(s["workers"] * float(g.uniform(0.55, 0.9)))))
        a.lodged = _local_dt(a.given, g, 7, 20)
        a.replaces = n
        a.superseded_by = None
        n.superseded_by = a
        notices.append(a)
    # withdrawals: by email to Employer Services, noted in the case notes (portal notices and open register ones)
    live = [n for n in notices if n.type == "Layoff" and n.superseded_by is None and n.first_layoff > dt.date(2026, 7, 15)]
    for n in [live[int(i)] for i in g.choice(len(live), 38, replace=False)]:
        start = max(n.given, K.PORTAL_LIVE + dt.timedelta(days=1)) + dt.timedelta(days=int(g.integers(5, 30)))
        wd = _workday(min(start, n.first_layoff - dt.timedelta(days=3)))
        if wd <= K.EXTRACT_PULL:
            n.withdrawn = wd
    # register statuses as frozen on 30 June 2026
    for n in notices:
        if n.channel == "email":
            if n.first_layoff <= K.REGISTER_FROZEN:
                n.reg_status = "Closed"
            elif g.random() < 0.035:
                n.reg_status = "Withdrawn"
                n.withdrawn = None   # withdrawn before the freeze: the register says so
                n.withdrawn_before_freeze = True
            else:
                n.reg_status = "Open"
    # re-keying: the open register notices whose first layoff fell before 1 October went onto the portal in the
    # go-live weeks; the later ones from mid-September, a working day's batch at a time, as their dates came near
    for n in notices:
        if n.channel == "email" and n.reg_status == "Open" and n.type == "Layoff":
            if n.first_layoff < dt.date(2026, 10, 1):
                kd = _workday(K.PORTAL_LIVE + dt.timedelta(days=int(g.integers(0, 12))))
            elif n.first_layoff <= dt.date(2026, 10, 31) and g.random() < 0.85:
                kd = _workday(dt.date(2026, 9, 14) + dt.timedelta(days=int(g.integers(0, 20))))
            elif n.first_layoff <= dt.date(2026, 11, 30) and g.random() < 0.38:
                kd = _workday(dt.date(2026, 9, 21) + dt.timedelta(days=int(g.integers(0, 14))))
            elif n.first_layoff <= dt.date(2026, 12, 31) and g.random() < 0.14:
                kd = _workday(dt.date(2026, 9, 28) + dt.timedelta(days=int(g.integers(0, 8))))
            else:
                kd = None
            if kd is not None and kd <= K.EXTRACT_PULL and (n.withdrawn is None or n.withdrawn > kd):
                n.rekeyed = dict(ln=None, at=_local_dt(kd, g, 9, 16))
    # every region has, in every month of the forward window, a site of an employer registered in another region
    nat = [e for e in emps if e.national]
    for reg in K.REGIONS:
        for pname, a0, a1 in PERIODS:
            def crosses(n):
                return valid(n) and period_of(n.first_layoff) == pname and \
                    any((s["region"] == reg) != (n.emp.region == reg) for s in n.sites)
            if any(crosses(n) for n in notices):
                continue
            e = [x for x in nat if x.region != reg][int(g.integers(len([x for x in nat if x.region != reg])))]
            n = Notice()
            n.emp = e
            n.type = "Layoff"
            n.first_layoff = a0 + dt.timedelta(days=int(g.integers(0, (a1 - a0).days + 1)))
            n.given = _workday(max(K.PORTAL_LIVE, n.first_layoff - dt.timedelta(days=int(g.integers(34, 110)))))
            if n.given > K.EXTRACT_PULL:
                n.given = _workday(dt.date(2026, 9, 1) + dt.timedelta(days=int(g.integers(0, 30))))
            town = REGION_TOWNS[reg][int(g.integers(len(REGION_TOWNS[reg])))]
            n.sites = [dict(town=town, region=reg, workers=int(np.clip(round(g.lognormal(3.5, 0.5)), 20, 300)),
                            street="%d %s" % (int(g.integers(1, 480)), STREETS[int(g.integers(len(STREETS)))]),
                            postcode=TOWN[town]["pc0"] + int(g.integers(0, 9)))]
            n.channel = "portal"
            n.ln = None
            n.es_ref = None
            n.lodged = _local_dt(n.given, g, 7, 20)
            n.withdrawn = None
            n.superseded_by = None
            n.replaces = None
            n.rekeyed = None
            notices.append(n)
    # the portal numbers its notices in the order they are entered, lodged by an employer or re-keyed by staff
    entries = [(n.lodged, 0, id(n), n, None) for n in notices if n.channel == "portal"]
    entries += [(n.rekeyed["at"], 1, id(n), n, "rekey") for n in notices if n.rekeyed]
    entries.sort(key=lambda x: (x[0], x[1]))
    seq = 412
    for at, _, _, n, kind in entries:
        seq += 1 if g.random() < 0.93 else int(g.integers(2, 4))
        if kind == "rekey":
            n.rekeyed["ln"] = "LN-2026-%05d" % seq
        else:
            n.ln = "LN-2026-%05d" % seq
    return dict(employers=emps, notices=notices)


def valid(n):
    """The notice lays workers off: a layoff notice, not superseded and not withdrawn."""
    return n.type == "Layoff" and n.superseded_by is None and n.withdrawn is None and \
        not getattr(n, "withdrawn_before_freeze", False)


PERIODS = [("11-31 Oct", dt.date(2026, 10, 11), dt.date(2026, 10, 31)),
           ("Nov", dt.date(2026, 11, 1), dt.date(2026, 11, 30)),
           ("Dec", dt.date(2026, 12, 1), dt.date(2026, 12, 31))]


def period_of(d):
    for name, a, b in PERIODS:
        if a <= d <= b:
            return name
    return None


def truth_table(W):
    out = {(r, p[0]): 0 for r in K.REGIONS for p in PERIODS}
    for n in W["notices"]:
        if not valid(n):
            continue
        p = period_of(n.first_layoff)
        if p:
            for s in n.sites:
                out[(s["region"], p)] += s["workers"]
    return out


# ---------------------------------------------------------------------------------------------------- shipped rows
PORTAL_COLS = ["notice_no", "lodged_utc", "business_no", "employer", "region", "notice_type", "first_layoff", "site_no",
               "site_address", "site_town", "site_postcode", "workers", "status", "replaces"]
REGISTER_COLS = ["ES ref", "Received", "Employer", "Business no.", "Site address", "Town", "Region", "Workers",
                 "First layoff", "Type", "Status", "Entered by", "Comments"]
CASE_COLS = ["note_id", "note_date", "officer", "reference", "note"]
OFFICERS = ["JW", "CH", "RB", "SB", "DL", "TL"]


def portal_notices(W):
    """Every notice the portal holds at the export: lodged there, an amendment, or re-keyed from the register."""
    out = []
    for n in W["notices"]:
        if n.channel == "portal":
            out.append((n.ln, n.lodged, n))
        elif n.rekeyed:
            out.append((n.rekeyed["ln"], n.rekeyed["at"], n))
    return sorted(out, key=lambda x: x[0])


def portal_rows(W):
    rows = []
    for ln, at, n in portal_notices(W):
        status = "Superseded" if n.superseded_by else "Lodged"
        for k, s in enumerate(n.sites, 1):
            rows.append(dict(notice_no=ln, lodged_utc=K.utc_stamp(at), business_no=n.emp.bn, employer=n.emp.name,
                             region=n.emp.region, notice_type=n.type, first_layoff=n.first_layoff.isoformat(),
                             site_no=k, site_address=s["street"], site_town=s["town"], site_postcode="%04d" % s["postcode"],
                             workers=s["workers"], status=status, replaces=n.replaces.ln if n.replaces else ""))
    return rows


def _typed_date(d, g):
    """A date as the register's clerks typed it: mostly entered as a date, some as day-first text."""
    if g.random() < 0.18:
        return "%d/%02d/%d" % (d.day, d.month, d.year) if g.random() < 0.6 else "%02d.%02d.%d" % (d.day, d.month, d.year)
    return d


def register_rows(W):
    g = K.rng("register-typing")
    rows = []
    for n in W["notices"]:
        if n.channel != "email":
            continue
        who = OFFICERS[int(g.integers(5))]
        for k, s in enumerate(n.sites):
            com = ""
            if len(n.sites) > 1 and k == 0:
                com = "%d sites" % len(n.sites)
            elif n.type == "Reduced hours" and g.random() < 0.3:
                com = "hours cut to %d per week" % int(g.choice([20, 24, 28, 30, 32]))
            rows.append({"ES ref": n.es_ref, "Received": n.given, "Employer": n.emp.reg_name, "Business no.": n.emp.bn,
                         "Site address": s["street"], "Town": s["town"], "Region": K.LEGACY_CODE[s["region"]],
                         "Workers": s["workers"], "First layoff": _typed_date(n.first_layoff, g), "Type": n.type,
                         "Status": n.reg_status, "Entered by": who, "Comments": com})
    return rows


def _typed_ref(ref, g):
    if ref.startswith("LN"):
        num = ref.split("-")[-1]
        forms = [ref, "LN 2026 %s" % num, "LN2026-%d" % int(num), "ln-2026-%s" % num, "LN-2026-%d" % int(num),
                 "notice LN-2026-%s" % num]
    else:
        y, num = ref.split("/")[1], ref.split("/")[2]
        forms = [ref, "ES %s/%d" % (y, int(num)), ref.lower(), "ES%s/%s" % (y, num), "register %s" % ref]
    return forms[int(g.integers(len(forms)))]


CONTACTS = ["HR manager", "payroll contact", "site manager", "general manager", "operations manager", "owner",
            "HR advisor", "company accountant", "employment lawyer", "office manager"]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]
# who writes the notes: the team's workload is uneven, the senior officer and the intake officer carrying most of it
OFFICER_LOAD = {"JW": 0.31, "CH": 0.25, "SB": 0.16, "RB": 0.13, "DL": 0.09, "TL": 0.06}


def _month_after(d, k):
    """The name of the month k months after d's month."""
    return MONTH_NAMES[(d.month - 1 + k) % 12]


def _year_of(d, k):
    return d.year + (d.month - 1 + k) // 12


def _fl(d):
    return "%d %s" % (d.day, d.strftime("%B"))


def _dm(d):
    return "%d/%d" % (d.day, d.month)


def _cap(t):
    return t[:1].upper() + t[1:]


def _hm(g):
    return "%d:%02d" % (int(g.integers(8, 17)), int(g.integers(0, 60)))


def _ordinal(k):
    return "%d%s" % (k, "th" if 10 <= k % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(k % 10, "th"))


class _Spread:
    """Chooses among options the one used least so far (ties broken on the wording stream), so an officer's phrasing
    and an employer's reasons spread across the log instead of repeating."""

    def __init__(self, g):
        self.g = g
        self.used = {}

    def pick(self, key, options, ident=None):
        ids = [ident(o) if ident else i for i, o in enumerate(options)]
        counts = [self.used.get((key, x), 0) for x in ids]
        low = min(counts)
        idx = [i for i, c_ in enumerate(counts) if c_ == low]
        i = idx[int(self.g.integers(len(idx)))]
        self.used[(key, ids[i])] = low + 1
        return options[i]


def note_clauses(text):
    """A note's clauses (split at stops, commas, semicolons, colons, brackets and spaced dashes), lower case."""
    return [" ".join(c.split()).lower() for c in re.split(r"[.,;:()!?]| - ", text) if c.strip()]


def note_skeleton(text):
    """A note with its particulars set aside (date stamps, contacts, towns, numbers, months and weekdays, the bracketed
    reason, case and closing stops): the sentence template an officer wrote."""
    s = text.lower()
    s = re.sub(r"^\d{1,2}/\d{1,2}(/\d{4})?\s*", "", s)
    for c in sorted(CONTACTS, key=len, reverse=True):
        s = s.replace(c.lower(), "<c>")
    for t in sorted(TOWN, key=len, reverse=True):
        s = s.replace(t.lower(), "<t>")
    s = re.sub(r"\b(%s|monday|tuesday|wednesday|thursday|friday|mon|tue|wed|thu|fri)\b" % "|".join(
        m.lower() for m in MONTH_NAMES), "<m>", s)
    s = re.sub(r"\d+(st|nd|rd|th)?", "#", s)
    s = re.sub(r"\(([^)]*)\)", "(<r>)", s)
    return s.strip(" .")


def _why(g, n, d, spread=None):
    """The reason an employer gave for withdrawing a notice, in its own particulars: the counterparty, the project,
    the place and the month. A month it names as past is before the note; one it names as a plan is after it."""
    pick = lambda xs: xs[int(g.integers(len(xs)))]
    town = n.sites[0]["town"]
    other = pick([t for t in TOWN if t != town])
    sn, pl, co = pick(SURNAMES), pick(PLACES), pick(COINED)
    w = sum(s_["workers"] for s_ in n.sites)
    past = _workday(d - dt.timedelta(days=int(g.integers(3, 20))), step=-1)
    m_plan = int(g.integers(3, 8))
    plan = "%s %d" % (_month_after(d, m_plan), _year_of(d, m_plan))
    yrs = pick(["two", "three", "five"])
    by_group = {
        "Construction": [
            "consent for the %s Road stage came through on %s" % (pl, _fl(past)),
            "%s Developments put the %s apartments back on" % (sn, town),
            "won the %s school rebuild" % other,
            "%s Civil kept them on for stage %d of the %s job" % (co, int(g.integers(2, 5)), pl),
            "council signed off the %s subdivision variation" % town,
            "the %s motorway package came back to them" % other],
        "Accommodation and food services": [
            "bookings for %s picked up once the %s festival was confirmed" % (_month_after(d, 1), town),
            "%s Hospitality bought the business and is keeping everyone" % sn,
            "the %s conference contract was renewed to %d" % (co, _year_of(d, 18)),
            "sale of the %s lodge fell through, staying open" % pl,
            "the cruise schedule for %s was confirmed for the summer" % town,
            "the %s owners decided to stay open over winter" % town],
        "Manufacturing": [
            "the %s order for %s confirmed" % (co, plan),
            "signed an export contract with %s Trading" % sn,
            "the %s line is staying after %s Group put money in" % (town, co),
            "%s took the plant on with the staff" % (sn + " Industries"),
            "the %s tender came through on %s" % (pl, _fl(past))],
        "Retail trade": [
            "the %s lease renewed for %s years" % (town, yrs),
            "%s Holdings bought the store as a going concern" % sn,
            "the %s landlord cut the rent, store staying open" % pl,
            "trading at %s since %s better than budgeted" % (town, _month_after(d, -1))],
        "Health care, social assistance and other services": [
            "the %s health board renewed the contract to %s" % (TOWN[town]["region"], plan),
            "funding for the %s clinic extended to %s" % (town, plan),
            "%s Trust took the service over with all staff" % sn],
        "Wholesale, transport and storage": [
            "%s Freight renewed the %s depot contract" % (co, town),
            "won back the %s distribution work" % sn,
            "the depot merger with %s Logistics is off" % co],
        "Agriculture, forestry and fishing": [
            "the %s harvest ran late, season extended into %s" % (town, _month_after(d, int(g.integers(2, 4)))),
            "%s Orchards bought the %s block with the staff" % (sn, pl)],
        "Administrative and support services": [
            "%s renewed the %s cleaning contract for %s years" % (co, town, yrs)],
    }
    client = sn + " " + pick(["Freight", "Group", "Partners", "Trading", "Foods", "Health"])
    generic = [
        pick(["restructure put back to %s" % plan, "the %s restructure deferred to %s" % (town, plan)]),
        pick(["the sale to %s Holdings fell over, staying open" % sn, "%s Holdings pulled out of the purchase" % sn]),
        pick(["receivers sold it to %s Group as a going concern" % co,
              "%s Group bought it out of receivership with the staff" % co]),
        pick(["parent company put in capital to %s" % plan, "the %s parent topped up funding to %s" % (co, plan)]),
        pick(["main client %s renewed for %s years" % (client, yrs), "the %s contract extended to %d" % (client, _year_of(d, 24))]),
        pick(["%s staff going onto shorter weeks instead" % town, "rostering the %s crew down to four days instead" % town]),
        pick(["closure on hold until %s" % plan, "the %s closure deferred to %s" % (town, plan)]),
        "won %s work that covers the %s roles" % (client, town),
        "insurer approved the %s rebuild" % town,
        "merger with %s called off" % co,
        "new owner %s keeping the %s team" % (sn, town),
        "orders at %s up since %s" % (town, _month_after(d, -1)),
        "redeploying the %s staff to %s instead" % (town, other)]
    fams = [("g", n.emp.group, i) for i in range(len(by_group.get(n.emp.group, [])))] + [("x", i) for i in range(len(generic))]
    texts = {f: (by_group[n.emp.group][f[2]] if f[0] == "g" else generic[f[1]]) for f in fams}
    return texts[spread.pick("why", fams, ident=lambda f: f)] if spread else texts[fams[int(g.integers(len(fams)))]]


def _scope(g, n, spread=None):
    """How the officer says the whole notice is withdrawn, never one site of it: an adverb for the notice, and a
    count of everyone on it."""
    pick = lambda xs: xs[int(g.integers(len(xs)))]
    w = sum(s_["workers"] for s_ in n.sites)
    k = len(n.sites)
    choose = (lambda key, xs: spread.pick(key, xs)) if spread else (lambda key, xs: pick(xs))
    if k == 1:
        adv = choose("adv1", ["in full", "as a whole", "entirely", "outright", "altogether"])
    elif k == 2:
        adv = choose("adv2", ["for both sites", "in full, both sites", "at both sites"])
    else:
        adv = choose("advk", ["for all %d sites" % k, "in full, all %d sites" % k, "across all %d sites" % k])
    count = pick(["all %d staying" % w, "none of the %d will go" % w, "%d jobs kept" % w])
    return adv, count


def _note_withdraw(g, who, n, d, spread=None):
    """A withdrawal as each officer writes one up: the contact, how it came in, that the whole notice is withdrawn,
    and the employer's reason in its own particulars."""
    pick = lambda xs: xs[int(g.integers(len(xs)))]
    c = pick(CONTACTS)
    mode = pick(["by email", "by phone", "in an email", "on the phone", "by letter", "in a call"])
    why = _why(g, n, d, spread)
    adv, count = _scope(g, n, spread)
    w = sum(s_["workers"] for s_ in n.sites)
    hm = _hm(g)
    forms = {
        "JW": ["%s rang at %s: notice withdrawn %s, %s. %s." % (_cap(c), hm, adv, count, _cap(why)),
               "Withdrawal received %s from the %s, notice withdrawn %s. %s." % (mode, c, adv, _cap(why)),
               "Written withdrawal from the %s on file, notice withdrawn %s, %s. %s." % (c, adv, count, _cap(why)),
               "%s, per the %s. Notice withdrawn %s." % (_cap(why), c, adv),
               "Spoke to the %s at %s, notice withdrawn %s (%s)." % (c, hm, adv, why),
               "%s has withdrawn the notice %s: %s." % (_cap(c), adv, why)],
        "CH": ["w/drawn %s - %s. %s %s" % (adv, why, c, mode.replace("by ", "").replace("on the ", "").replace("in an ", "")
                                            .replace("in a ", "")),
               "ph %s %s, notice w/drawn %s. %s" % (c, hm, adv, why),
               "WITHDRAWN %s per email %s, %s. %s" % (adv, _dm(d), count, why),
               "notice w/drawn %s %s: %s" % (adv, _dm(d), why), "%s - withdrawal on file, w/drawn %s, %s" % (c, adv, count)],
        "RB": ["%s emailed, notice withdrawn %s - %s" % (c, adv, why),
               "withdrawal in from the %s, withdrawn %s, %s, %s" % (c, adv, count, why),
               "%s. withdrawn %s" % (why, adv), "%s confirmed withdrawal %s %s, %s, %s" % (c, adv, mode, count, why)],
        "SB": ["Formal withdrawal of the whole notice received from the %s on %s. %s." % (c, _fl(d), _cap(why)),
               "The %s advised: %s. Notice withdrawn %s." % (c, why, adv),
               "Withdrawal confirmed with the %s %s, notice withdrawn %s, %s. %s." % (c, mode, adv, count, _cap(why)),
               "%s. Letter of withdrawal from the %s, notice withdrawn %s." % (_cap(why), c, adv)],
        "DL": ["%s notice withdrawn %s, %s. %s." % (_dm(d), adv, c, _cap(why)),
               "%s withdrawal email from %s: %s. Whole notice, all %d staying." % (_dm(d), c, why, w),
               "%s notice withdrawn %s (%s)." % (_dm(d), adv, why)],
        "TL": ["W/drawn %s - %s." % (adv, why), "Spoke to %s, notice withdrawn %s: %s." % (c, adv, why),
               "Withdrawal by phone, notice withdrawn %s, %s. %s." % (adv, count, _cap(why))],
    }
    return spread.pick(("w", who), forms[who]) if spread else pick(forms[who])


def _note_other(g, who, n, d, spread=None):
    """Everything else Employer Services records on a notice, as an officer's terse record of the call or the job
    done; a date it schedules falls after the note, a date it reports does not."""
    pick = lambda xs: xs[int(g.integers(len(xs)))]
    town = n.sites[0]["town"]
    c = pick(CONTACTS)
    c2 = pick([x for x in CONTACTS if x != c])
    C = _cap(c)
    w = sum(s_["workers"] for s_ in n.sites)
    k = len(n.sites)
    fl = n.first_layoff
    hm = _hm(g)
    reg = TOWN[town]["region"]
    emp = re.sub(r"\s*\((?:No \d+|\d{4})\)|\s+Limited$", "", n.emp.name)
    ev = _workday(d + dt.timedelta(days=int(g.integers(3, 24))))
    evs = pick(["%d %s" % (ev.day, ev.strftime("%B")), "%s %d/%d" % (ev.strftime("%a"), ev.day, ev.month),
                "%s %d %s" % (ev.strftime("%A"), ev.day, ev.strftime("%B"))] +
               (["the %s" % _ordinal(ev.day)] if ev.month == d.month else []))
    x = max(2, w // 5)
    v = max(2, w // 7)
    ahead = fl > d
    kinds = [
        ["Went through %s with the %s (%s)." % ("the site details" if k == 1 else "the %d sites" % k, c, emp),
         "%s address confirmed with the %s." % (town, c),
         "Site %s checked w %s." % ("details" if k == 1 else "list (%d)" % k, c),
         ("Rang %s re the site address." % emp if k == 1 else "Rang %s re site addresses, %s first." % (emp, town))],
        ["Union delegate rang %s for a copy of the %s notice, sent redacted." % (hm, emp),
         "%s organiser wants the notice; copy sent, names out." % town, "Copy to union (%s delegate)." % town,
         ("Union rep after the %s numbers, summary sent." % emp if k == 1 else
          "Union rep after the %s numbers by site, summary sent." % emp)],
        ["Rang re notice period, went through it with the %s." % c, "%s rang %s re the 30 days for %s." % (C, hm, emp),
         "Query from %s %s on timing, rang back %s." % (emp, c, hm),
         "%s asked about the notice period for the %s staff, covered it on the phone." % (C, town)],
        (["Layoffs at %s going ahead %s per %s." % (town, _fl(fl), c), "No change, proceeding %s." % _dm(fl),
          "%s: %d finishing from %s as notified." % (C, w, _fl(fl)), "Checked in w %s %s, %s still the date." % (c, hm, _fl(fl))]
         if ahead else
         ["%s confirmed the %s finishes went through %s." % (C, town, _fl(fl)),
          "%s: first finishes done %s." % (emp, _dm(fl)), "%s says the %d left as planned." % (C, w)]),
        ["Postcode for the %s site added." % town,
         ("%s postcode missing, %s supplied." % (town, c) if k == 1 else "Site %d postcode missing, %s supplied." % (k, c)),
         "Fixed the %s postcode (%s)." % (town, emp), "%s site line had the wrong postcode, corrected from the %s's email." %
         (town, c)],
        ["Passed to %s regional office re redeployment (%s)." % (reg, emp),
         "%s after help placing %d staff, referred to %s office." % (C, w, reg),
         "%s office to call the %s re placements at %s." % (reg, c, town)],
        ["%s reporter rang %s, sent to comms." % (town, hm), "Media query re %s numbers, comms handling." % emp,
         "Comms asked for the %s figures, summary sent." % town],
        ["%s thinks %d of the %d may be kept on, will confirm." % (C, x, w),
         "Numbers at %s may come down, %s to let us know." % (town, c),
         "%s hoping to keep %d on at %s, nothing firm." % (C, x, town)],
        (["Payroll: first finish %s." % _fl(fl), "Payroll contact confirmed last day %s (%s)." % (_fl(fl), emp),
          "%s confirmed as first finishing date, per payroll." % _fl(fl)] if ahead else
         ["Payroll: first staff finished %s." % _fl(fl), "%s payroll confirmed the %s finish went through." % (emp, _dm(fl))]),
        ["Staff briefing at the %s office %s." % (town, evs), "Info session for %s staff %s." % (town, evs),
         "%s running a staff briefing %s, we will attend." % (C, evs), "Room booked at %s for the session %s." % (town, evs)],
        ["Now dealing with the %s." % c, "New contact for %s: %s." % (emp, c), "%s taking over the notice from the %s." % (C, c2)],
        ["%s: %d gone early on voluntary terms." % (C, v), "%d left on VR at %s per the %s." % (v, town, c)],
        ["Info pack emailed to %s (%s)." % (c, emp), "Worker info sheets posted to %s." % town,
         "%s asked for %d info sheets, sent." % (C, w)],
        ["Query re casuals on the %s roster, rang back %s." % (town, hm), "%s asked about fixed-term staff, went through it." % C,
         "Contractor question from the %s, covered on the phone." % c, "Part-time staff query (%s), answered." % emp],
        ["Jobs expo %s %s, %s releasing staff." % (town, evs, c), "%s office expo at %s %s." % (reg, town, evs),
         "Expo for the %s workers %s." % (emp, evs)],
        ["Same notice emailed again by the %s." % c, "Duplicate email %s, filed." % _dm(d),
         "%s resent the notice, filed with the original." % C],
        (["%s rang %s, still on for %s." % (C, hm, _fl(fl)), "Rang %s, on track." % c,
          "%s still the date per %s." % (_fl(fl), c), "%s called, no change for %s." % (C, _fl(fl))] if ahead else
         ["Rang %s, all went as notified." % c, "%s rang %s, layoffs done." % (C, hm)]),
        ["Got a mobile for the %s site lead." % town, "Need site contact at %s, %s to send." % (town, c),
         "Asked the %s for the site lead's number." % (c if c != "site manager" else c2)],
        ["%s wanted staff letter wording, sample sent." % C, "Sample staff letter to the %s." % c,
         "Sent our letter template to %s for the %s staff." % (emp, town)],
        ["Left msg for %s." % c, "Tried %s twice, voicemail." % c, "No answer from %s, try Monday." % c,
         "Emailed %s again, nothing back." % c],
        ["%s wants to move the first layoff, sent the amendment form." % C,
         "Asked about pushing the %s dates back a fortnight, sent the amendment steps." % town,
         "%s rang %s re changing dates, amendment form emailed." % (C, hm)],
        ["Regional employment office told re %d at %s." % (w, town), "%s numbers to the local benefits office." % town,
         "Let %s office know: %d at %s." % (reg, w, town)],
        ["%s rang %s worried the notice is public, went through it." % (C, hm),
         "Query re who sees the %s notice, rang back." % emp, "%s asked about publication, covered it." % C],
        ["Site visit %s %s." % (town, evs), "Visited the %s site, met the %s." % (town, c),
         "Out to %s %s to see the %s." % (town, evs, c)],
        (["Full site list requested from %s, in same day." % c, "%s sent site breakdown on request." % C,
          "Asked %s for numbers by site, received %s." % (emp, _dm(d))] if k > 1 else
         ["%s headcount requested from %s, in same day." % (town, c), "%s sent the staff numbers on request." % C,
          "Asked %s for the %s staff list, received %s." % (emp, town, _dm(d))]),
    ]
    if spread:
        ki = spread.pick("kind", list(range(len(kinds))))
        t = spread.pick(("other", ki, ahead), kinds[ki])
    else:
        t = pick(pick(kinds))
    if who == "CH":
        t = t.replace("Employer", "emp").replace("employer", "emp").replace(" the ", " ").replace("phone", "ph")
        t = t.replace("received", "recvd").replace(" with ", " w ")
    elif who == "RB":
        first = re.split(r"[ ,:;(]", t, 1)[0]
        proper = t[:2].isupper() or first in TOWN or first in K.REGIONS or first in MONTH_NAMES or \
            first == emp.split()[0] or any(first == x.split()[0] for x in TOWN)
        t = (t if proper else t[0].lower() + t[1:]).rstrip(".")
    elif who == "DL":
        t = "%s %s" % (_dm(d), t)
    elif who == "TL" and g.random() < 0.4:
        t = t.rstrip(".").replace(" the ", " ")
    return t


def _unique(make, used_clauses, used_texts, skel, who="", tries=60):
    """Draw a note until no clause of six words or more repeats an earlier note's, the text is new, its template has
    not been used twice already and never twice by the same officer."""
    t = None
    for _ in range(tries):
        t = make()
        long_ = [cl for cl in note_clauses(t) if len(cl.split()) >= 6]
        sk = note_skeleton(t)
        if t not in used_texts and not any(cl in used_clauses for cl in long_) and skel.get(sk, 0) < 2 and \
                (sk, who) not in skel:
            break
    used_texts.add(t)
    used_clauses.update(cl for cl in note_clauses(t) if len(cl.split()) >= 6)
    sk = note_skeleton(t)
    skel[sk] = skel.get(sk, 0) + 1
    skel[(sk, who)] = 1
    return t


def case_note_rows(W):
    g = K.rng("case-notes")
    gt = K.rng("case-note-text")
    go = K.rng("case-note-officer")
    load = [OFFICER_LOAD[o] for o in OFFICERS]
    officer = lambda: OFFICERS[int(go.choice(len(OFFICERS), p=np.array(load) / sum(load)))]
    used_clauses, used_texts, skel = set(), set(), {}
    spread = _Spread(K.rng("case-note-wording"))
    notes = []
    for n in W["notices"]:
        if n.withdrawn:
            ref = n.rekeyed["ln"] if (n.rekeyed and n.withdrawn >= n.rekeyed["at"].date()) else (n.ln or n.es_ref)
            slot = int(g.integers(6))                       # the structure stream keeps its draws and the log its order
            who = officer()
            txt = _unique(lambda: _note_withdraw(gt, who, n, n.withdrawn, spread), used_clauses, used_texts, skel, who)
            notes.append((n.withdrawn, slot, who, _typed_ref(ref, g), txt))
    pool = [n for n in W["notices"] if (n.channel == "portal" or n.rekeyed) and n.given >= dt.date(2026, 4, 1)]
    for _ in range(152):
        n = pool[int(g.integers(len(pool)))]
        start = n.lodged.date() if n.channel == "portal" else n.rekeyed["at"].date()
        if start > K.EXTRACT_PULL:
            continue
        d = _workday(start + dt.timedelta(days=int(g.integers(0, max(1, (K.EXTRACT_PULL - start).days + 1)))))
        if d > K.EXTRACT_PULL or (n.withdrawn and d >= n.withdrawn):
            continue
        ref = n.ln if n.channel == "portal" else n.rekeyed["ln"]
        slot = int(g.integers(6))
        who = officer()
        txt = _unique(lambda: _note_other(gt, who, n, d, spread), used_clauses, used_texts, skel, who)
        notes.append((d, slot, who, _typed_ref(ref, g), txt))
    cons = [n for n in pool if n.withdrawn is None and valid(n) and n.first_layoff >= dt.date(2026, 10, 20)]
    for n in [cons[int(i)] for i in g.choice(len(cons), 2, replace=False)]:
        start = n.lodged.date() if n.channel == "portal" else n.rekeyed["at"].date()
        d = _workday(start + dt.timedelta(days=12))
        ref = n.ln if n.channel == "portal" else n.rekeyed["ln"]
        txt = ["Employer is considering withdrawing the notice if the %s tender comes through. Will advise." %
               n.sites[0]["town"],
               "the %s thinks they may withdraw, waiting on their directors" % CONTACTS[int(g.integers(len(CONTACTS)))]][
            len(notes) % 2]
        who = "JW" if "Employer" in txt else "RB"
        notes.append((d, OFFICERS.index(who), who, _typed_ref(ref, g), txt))
    notes.sort(key=lambda x: (x[0], OFFICERS[x[1]]))
    rows = []
    k0 = 51120
    for k, (d, _, who, ref, txt) in enumerate(notes):
        k0 += int(g.integers(1, 4))
        rows.append(dict(note_id="CN%06d" % k0, note_date=d.isoformat(), officer=who, reference=ref, note=txt))
    return rows


# ---------------------------------------------------------------------------------------------------- the ask from rows
import re as _re

LN_RE = _re.compile(r"ln[\s-]*2026[\s-]*0*(\d+)", _re.I)
ES_RE = _re.compile(r"es\s*/?\s*(\d{2})\s*/\s*0*(\d+)", _re.I)
WD_RE = _re.compile(r"\b(withdrawn|withdrawal|withdraws|withdrawing it|w/drawn|withdraw -|withdraw the notice)\b|"
                    r"emailed to withdraw|to withdraw\b(?! the notice if)", _re.I)


def norm_ref(s):
    m = LN_RE.search(s)
    if m:
        return "LN-2026-%05d" % int(m.group(1))
    m = ES_RE.search(s)
    if m:
        return "ES/%s/%04d" % (m.group(1), int(m.group(2)))
    return None


def is_withdrawal(text):
    t = text.lower()
    if "considering" in t or "may withdraw" in t or "thinks they may" in t:
        return False
    return bool(_re.search(r"withdrawn|withdrawal|w/drawn|withdrawing notice|emailed to withdraw|withdraws notice|"
                           r"withdraws this|has withdrawn|withdrawing it", t))


def parse_day(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    s = str(v).strip()
    m = _re.fullmatch(r"(\d{1,2})[/.](\d{1,2})[/.](\d{4})", s)
    if m:
        return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    return dt.date.fromisoformat(s[:10])


def ask_a(portal, register, notes, town_region, region_of_code, site_region=True, dedupe="match",
          withdrawals="notes", superseded=True, layoff_only=True):
    """The workers to be laid off by region and period. portal, register and notes are row dicts as read from the
    files; town_region maps a town to its region, region_of_code a legacy code to its region name.
    site_region False takes the portal's own region column; dedupe 'match' counts a re-keyed notice once, 'stack'
    keeps both copies, 'portal' drops the register, 'drop_bn' drops every portal notice whose business number is on
    an open register notice; withdrawals 'notes' applies the case notes' withdrawals, 'none' ignores them, 'word'
    takes every note mentioning a withdrawal."""
    wd = set()
    if withdrawals != "none":
        for r in notes:
            txt = r["note"]
            hit = is_withdrawal(txt) if withdrawals == "notes" else ("withdr" in txt.lower() or "w/drawn" in txt.lower())
            if hit:
                ref = norm_ref(r["reference"])
                if ref:
                    wd.add(ref)
    pn = {}
    for r in portal:
        pn.setdefault(r["notice_no"], []).append(r)
    rn = {}
    for r in register:
        rn.setdefault(r["ES ref"], []).append(r)
    items = []   # (key, business_no, first_layoff, [(region, workers)], refs)
    for no, rows in pn.items():
        h = rows[0]
        if superseded and h["status"] == "Superseded":
            continue
        if layoff_only and h["notice_type"] != "Layoff":
            continue
        fl = parse_day(h["first_layoff"])
        sites = [((town_region[r["site_town"]] if site_region else h["region"]), int(r["workers"]), r["site_town"])
                 for r in rows]
        items.append(dict(src="portal", ref=no, bn=h["business_no"], fl=fl, sites=sites))
    reg_items = []
    for ref, rows in rn.items():
        h = rows[0]
        if h["Status"] != "Open":
            continue
        if layoff_only and h["Type"] != "Layoff":
            continue
        fl = parse_day(h["First layoff"])
        sites = [(region_of_code[r["Region"]], int(r["Workers"]), r["Town"]) for r in rows]
        reg_items.append(dict(src="register", ref=ref, bn=str(h["Business no."]), fl=fl, sites=sites))
    sig = lambda it: (it["bn"], it["fl"], tuple(sorted((t, w) for _, w, t in it["sites"])))
    matched = {}
    if dedupe == "match":
        by = {}
        for it in items:
            by.setdefault(sig(it), []).append(it)
        keep = []
        for it in reg_items:
            hits = by.get(sig(it), [])
            if hits:
                matched[it["ref"]] = hits[0]["ref"]
                continue
            keep.append(it)
        reg_items = keep
    elif dedupe == "portal":
        reg_items = []
    elif dedupe == "drop_bn":
        bns = {it["bn"] for it in reg_items}
        items = [it for it in items if it["bn"] not in bns]
    out = {(r, p[0]): 0 for r in K.REGIONS for p in PERIODS}
    for it in items + reg_items:
        refs = {it["ref"]} | ({matched_r for matched_r, p in matched.items() if p == it["ref"]})
        if refs & wd:
            continue
        p = period_of(it["fl"])
        if not p:
            continue
        for reg, w, _ in it["sites"]:
            out[(reg, p)] += w
    return out, dict(matched=matched, withdrawn=wd)


if __name__ == "__main__":
    W = simulate()
    ns = W["notices"]
    print("notices", len(ns), "email", sum(n.channel == "email" for n in ns), "portal", sum(n.channel == "portal" for n in ns))
    print("rekeyed", sum(1 for n in ns if n.rekeyed), "withdrawn", sum(1 for n in ns if n.withdrawn),
          "amended", sum(1 for n in ns if n.replaces))
    T = truth_table(W)
    for r in K.REGIONS:
        print("%-9s" % r, [T[(r, p[0])] for p in PERIODS])
