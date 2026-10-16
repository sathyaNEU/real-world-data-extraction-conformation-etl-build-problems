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


def _month_after(d, k):
    """The name of the month k months after d's month."""
    return MONTH_NAMES[(d.month - 1 + k) % 12]


class _Cycle:
    """Draws one phrasing per call, using every phrasing of a kind before any repeats (as officers vary their wording)."""

    def __init__(self, g):
        self.g = g
        self.left = {}

    def pick(self, key, forms):
        left = self.left.get(key)
        if not left:
            left = list(range(len(forms)))
        i = left.pop(int(self.g.integers(len(left))))
        self.left[key] = left
        return forms[i]


def _why(g, n, d):
    """The reason an employer gave for withdrawing a notice, in the words the officer took down; every month it names is
    after the note's date when it is a plan and before it when it is past."""
    pick = lambda xs: xs[int(g.integers(len(xs)))]
    w = sum(s_["workers"] for s_ in n.sites)
    other = pick([t for t in TOWN if t != n.sites[0]["town"]])
    since = pick((["the start of %s" % MONTH_NAMES[d.month - 1]] if d.day >= 8 else []) +
                 [_month_after(d, -1), _month_after(d, -2)])
    forms = [
        lambda: pick(["new contract won", "picked up a new contract", "won the %s contract after all" % other]),
        lambda: pick(["sale of the business fell through", "the sale fell over", "buyer pulled out, staying open"]),
        lambda: pick(["restructure deferred", "restructure put back to %s" % _month_after(d, int(g.integers(4, 8))),
                      "restructure shelved for now"]),
        lambda: pick(["staff redeployed", "staff redeployed to other sites", "all %d placed elsewhere in the group" % w]),
        lambda: pick(["workers taken on by the buyer", "buyer keeping the whole team"]),
        lambda: pick(["council consent came through", "resource consent granted", "consent approved on appeal"]),
        lambda: pick(["funding extended to %s %d" % (pick(["March", "June", "December"]), int(g.integers(2027, 2029))),
                      "funding renewed for another year", "programme funding confirmed to %d" % int(g.integers(2027, 2029))]),
        lambda: pick(["the receiver found a buyer", "receivers sold it as a going concern"]),
        lambda: pick(["work picked up after the stand-down", "orders back up", "busy again since %s" % since]),
        lambda: "main client renewed for %s years" % pick(["two", "three", "five"]),
        lambda: "staff moving to the %s plant instead" % other,
        lambda: pick(["the merger was called off", "merger off"]),
        lambda: pick(["insurer approved the rebuild", "insurance came through for the repairs"]),
        lambda: "season extended into %s" % _month_after(d, int(g.integers(2, 4))),
        lambda: pick(["parent company put in more capital", "owners injected funds"]),
        lambda: pick(["tender won on the second round", "won the retender"]),
        lambda: pick(["hours cut instead of jobs", "going to a four-day week instead",
                      "reduced hours for %d staff instead" % max(3, w // 2), "short time instead, nobody let go"]),
        lambda: "closure on hold until %s" % _month_after(d, int(g.integers(3, 8)))]
    return forms[int(g.integers(len(forms)))]()


MODES = ["by email", "by phone", "in an email", "on the phone", "by letter", "in a call"]


def _cap(t):
    return t[:1].upper() + t[1:]


def _fl(d):
    return "%d %s" % (d.day, d.strftime("%B"))


def _hm(g):
    return "%d:%02d" % (int(g.integers(8, 17)), int(g.integers(0, 60)))


def _note_withdraw(g, who, n, d, cyc):
    """A withdrawal as each officer writes one up: the contact, how it came in, the reason the employer gave."""
    pick = lambda xs: xs[int(g.integers(len(xs)))]
    town = n.sites[0]["town"]
    why = _why(g, n, d)
    c = pick(CONTACTS)
    w = sum(s_["workers"] for s_ in n.sites)
    mode = pick(MODES)
    dm = "%d/%d" % (d.day, d.month)
    forms = {
        "JW": ["Notice withdrawn. The %s confirmed %s (%s), so none of the %d layoffs will go ahead." % (c, mode, why, w),
               "The %s has withdrawn the notice (%s). Confirmation saved to the file." % (c, why),
               "Withdrawal received %s from the %s: %s. Closed." % (mode, c, why),
               "Employer has withdrawn the notice; %s. The %s site keeps all %d staff." % (why, town, w),
               "Notice withdrawn at the employer's request %s. Reason given: %s." % (mode, why),
               "Spoke to the %s at %s. %s, so the notice is withdrawn and written confirmation is on its way." % (
                   c, _hm(g), _cap(why)),
               "%s: the employer has withdrawn its notice for the %s staff." % (_cap(why), town),
               "Withdrawal in writing from the %s today. %s." % (c, _cap(why))],
        "CH": ["w/drawn - %s. email on file" % why, "ph %s - notice withdrawn, %s" % (c, why),
               "WITHDRAWN per email %s (%s)" % (dm, why), "notice withdrawn by emp, %s" % why,
               "w/drawn. %s rang, %s" % (c, why), "withdrawal recvd from %s. %s" % (c, why),
               "emp w/drawn notice %s, %s. nothing further" % (dm, why), "withdrawn (%s) - confirmed w %s" % (why, c)],
        "RB": ["employer emailed - notice withdrawn, %s" % why, "notice withdrawn, %s at %s" % (why, town),
               "withdrawn by the %s, %s" % (c, why), "%s confirmed withdrawal - %s" % (c, why),
               "withdrawal email in from %s. %s" % (c, why), "got the withdrawal through from the %s, %s" % (c, why),
               "%s notice withdrawn - %s, all %d staying" % (town, why, w)],
        "SB": ["Notice withdrawn. The %s advised: %s." % (c, why),
               "Received written withdrawal of the notice from the %s. %s." % (c, _cap(why)),
               "Withdrawal confirmed with the %s %s. %s staff staying on." % (c, mode, town),
               "Notice withdrawn by the employer; %s. File closed." % why,
               "Formal withdrawal received from the %s on %s. %s. No layoffs to proceed." % (c, _fl(d), _cap(why)),
               "The employer has withdrawn its notice covering %d workers at %s. Reason: %s." % (w, town, why)],
        "DL": ["%s/%d withdrawal email from %s - %s." % (dm, d.year, c, why), "Withdrawn %s. %s." % (_fl(d), _cap(why)),
               "%s notice withdrawn (%s)." % (dm, why), "Withdrawal of notice received %s from %s. %s." % (dm, c, _cap(why)),
               "%s %s rang: notice withdrawn, %s." % (dm, c, why), "%s withdrawal confirmed in writing. %s." % (dm, _cap(why))],
        "TL": ["Withdrawn - %s." % why, "Spoke to %s. Notice withdrawn, %s." % (c, why), "Notice withdrawn; %s." % why,
               "Withdrawn by employer (%s)." % why, "W/drawn %s, %s." % (mode, why),
               "Emp has withdrawn notice. %s. %d jobs kept." % (_cap(why), w),
               "%s confirmed withdrawal %s - %s." % (_cap(c), mode, why)],
    }
    return cyc.pick(("withdraw", who), forms[who])


def _ordinal(k):
    return "%d%s" % (k, "th" if 10 <= k % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(k % 10, "th"))


def _note_other(g, who, n, d, cyc):
    """Everything else Employer Services records on a notice, in the officer's own style; a date it schedules falls
    after the note, a date it reports does not."""
    pick = lambda xs: xs[int(g.integers(len(xs)))]
    town = n.sites[0]["town"]
    c = pick(CONTACTS)
    C = _cap(c)
    w = sum(s_["workers"] for s_ in n.sites)
    k = len(n.sites)
    fl = n.first_layoff
    hm = _hm(g)
    reg = TOWN[town]["region"]
    ev = _workday(d + dt.timedelta(days=int(g.integers(3, 24))))       # a date the note schedules, after the note
    evs = pick(["%d %s" % (ev.day, ev.strftime("%B")), "%s %d/%d" % (ev.strftime("%a"), ev.day, ev.month),
                "%s %d %s" % (ev.strftime("%A"), ev.day, ev.strftime("%B"))] +
               (["the %s" % _ordinal(ev.day)] if ev.month == d.month else []))
    x = max(2, w // 5)
    v = max(2, w // 7)
    ahead = fl > d
    kinds = [
        ["Called the %s to confirm the site addresses, all correct." % c, "Site addresses checked with the %s." % c,
         "Went through the %d site%s with the %s, no changes." % (k, "" if k == 1 else "s", c),
         "Confirmed the %s address with the %s; matches the notice." % (town, c),
         "%s confirmed every site on the notice is still trading." % C],
        ["Union delegate asked for a copy of the notice. Sent with names removed.",
         "%s organiser asked for the notice, redacted copy sent." % town, "Copy to the union as requested.",
         "Union rep rang for the numbers by site. Sent the summary, no names.",
         "Delegate at the %s site wants the notice; sent a copy without staff names." % town],
        ["Employer asked whether the 30 days run from lodgement. They do.",
         "Query from the %s about when the 30 days start. Explained." % c,
         "%s unsure if the notice period counts weekends. It does." % C,
         "%s wanted to know if the 30 days can be shortened. Not without an exemption." % C,
         "Explained to the %s that the 30 days count from the day the notice was lodged." % c],
        (["%s says the layoffs go ahead as notified." % C, "Layoffs going ahead on %s per the %s." % (_fl(fl), c),
          "No change, proceeding %d/%d." % (fl.day, fl.month), "%s confirmed %d finishing as planned from %s." % (C, w, _fl(fl)),
          "Checked in with the %s; still %d affected, dates unchanged." % (c, w)] if ahead else
         ["%s confirmed the layoffs went ahead on %s as notified." % (C, _fl(fl)),
          "First finishes went through on %d/%d, no change to the numbers." % (fl.day, fl.month),
          "%s says the %d left as planned." % (C, w)]),
        ["Postcode missing for the %s site, now supplied." % town, "Blank postcode on site %d fixed." % k,
         "Site %d had no postcode. %s supplied it." % (k, C), "Corrected the %s site's postcode." % town,
         "Wrong postcode on the %s site line; the %s sent the right one." % (town, c)],
        ["Referred to the %s regional office for redeployment help." % reg,
         "Employer wants help placing staff. Passed to %s regional office." % reg,
         "%s asked about redeployment support; put them onto the %s office." % (C, reg),
         "%s regional office to contact the %s about placing the %d staff." % (reg, c, w)],
        ["Media enquiry about the %s job losses, sent to communications." % town,
         "Reporter rang about the %s numbers at %s, referred to comms." % (town, hm),
         "Local paper asking about %s. Passed to comms." % town,
         "Comms team asked for the %s figures, sent the notice summary." % town],
        ["%s thinks %d of the %d may be kept on. Will amend if so." % (C, x, w),
         "Numbers may come down. Employer will lodge an amendment if they do.",
         "Possibly fewer than %d will go; the %s will amend the notice once they know." % (w, c),
         "%s hopes to keep %d on. Told them to lodge an amended notice if that happens." % (C, x)],
        (["Payroll confirms the first finishing date is %s." % _fl(fl), "First layoff date checked with payroll, unchanged.",
          "Payroll contact confirmed the last day of work as %s." % _fl(fl), "%s still the first finishing date, per payroll." %
          _cap(_fl(fl))] if ahead else
         ["Payroll confirms the first staff finished on %s." % _fl(fl), "First layoff date checked with payroll, it held."]),
        ["Staff briefing booked at the %s office for %s." % (town, evs),
         "Information session for affected staff %s at %s." % (evs, town),
         "%s has a briefing for the affected staff on %s; we will attend." % (C, evs),
         "Booked a room at %s for the staff session %s." % (town, evs)],
        ["New contact for this notice: the %s." % c, "Contact details updated, now the %s." % c,
         "%s takes over as contact for the notice." % C, "Changed the contact on file to the %s." % c],
        ["%d staff left early on voluntary terms, notice stands." % v,
         "Some voluntary redundancies taken early. Notice unchanged at %d." % w,
         "%s says %d took voluntary redundancy already; the notice still covers all %d." % (C, v, w)],
        ["Info pack for affected workers emailed to the %s." % c, "Sent the information sheet for affected workers.",
         "Posted copies of the worker information sheet to the %s site." % town,
         "%s asked for the information sheets in bulk; sent." % C],
        ["Asked whether casual staff count towards the 20. Explained.",
         "Question on fixed-term staff and the notice. Answered by email.",
         "%s unsure whether contractors count. They don't; explained." % C,
         "Query about part-timers in the count. Explained they count."],
        ["Jobs expo in %s for the affected workers, employer releasing staff to attend." % town,
         "Regional office running a jobs expo at %s on %s." % (town, evs),
         "Expo for the %s workers set for %s; the %s is letting staff go along." % (town, evs, c)],
        ["Second copy of the notice by email, nothing new.", "Same notice sent again by the %s, no action." % c,
         "Duplicate email %d/%d, nothing changed." % (d.day, d.month),
         "%s resent the notice; identical to the one on file." % C],
        (["%s rang at %s, still on track for %s." % (C, hm, _fl(fl)), "Rang the %s, on track." % c,
          "Spoke to the %s; %s is still the date." % (c, _fl(fl)),
          "%s called to say nothing has changed for %s." % (C, _fl(fl))] if ahead else
         ["Rang the %s, all went as notified." % c, "%s rang at %s, the layoffs are done." % (C, hm)]),
        ["Got a mobile number for the %s site lead." % town, "Asked for the site manager's number for the briefing.",
         "Need a site contact at %s; the %s to send one." % (town, c)],
        ["%s wanted wording for the staff letter, example sent." % C, "Template letter to staff sent to the %s." % c,
         "Sent the %s our sample letter for affected staff." % c],
        ["Left a message for the %s, no reply yet." % c, "Tried the %s twice, voicemail." % c,
         "No answer from the %s, will try again Monday." % c, "Emailed the %s again; nothing back." % c],
        ["Checked the notice against the business register, details match.",
         "Business number on the notice confirmed with the register.",
         "Register entry for the employer checked, nothing out of line."],
        ["Employer asked to move the first layoff date. Advised an amended notice is needed.",
         "Wants to push the first layoff back a fortnight. Told them to amend the notice.",
         "%s asked how to change the dates. Sent the amendment steps." % C],
        ["Regional employment office told about the %d workers at %s." % (w, town),
         "Passed the numbers to the local benefits office for %s." % town,
         "Let the %s regional office know %d at %s are affected." % (reg, w, town)],
        ["%s asked if the notice is public. Explained what we publish." % C,
         "Query about who sees the notice. Explained.", "%s worried about the notice being published; explained." % C],
        ["Site visit to %s arranged for %s." % (town, evs), "Visited the %s site, met the %s." % (town, c),
         "Going out to %s on %s to meet the %s." % (town, evs, c)],
        ["Emailed the %s for the full site list, received the same day." % c,
         "Requested the breakdown by site, the %s sent it through." % c,
         "%s sent the site-by-site numbers on request." % C],
    ]
    kind = cyc.pick("kind", list(range(len(kinds))))
    t = cyc.pick(("other", kind, ahead), kinds[kind])
    if who == "CH":
        t = t.replace("Employer", "emp").replace("employer", "emp").replace(" the ", " ").replace("phone", "ph")
        t = t.replace("received", "recvd").replace(" with ", " w ")
    elif who == "RB":
        t = (t if t[:2].isupper() else t[0].lower() + t[1:]).rstrip(".")
    elif who == "DL":
        t = "%d/%d %s" % (d.day, d.month, t)
    elif who == "TL" and g.random() < 0.4:
        t = t.rstrip(".").replace(" the ", " ")
    return t


def case_note_rows(W):
    g = K.rng("case-notes")
    gt = K.rng("case-note-text")
    cyc = _Cycle(K.rng("case-note-wording"))
    notes = []
    for n in W["notices"]:
        if n.withdrawn:
            ref = n.rekeyed["ln"] if (n.rekeyed and n.withdrawn >= n.rekeyed["at"].date()) else (n.ln or n.es_ref)
            who = OFFICERS[int(g.integers(6))]
            notes.append((n.withdrawn, who, _typed_ref(ref, g), _note_withdraw(gt, who, n, n.withdrawn, cyc)))
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
        who = OFFICERS[int(g.integers(6))]
        notes.append((d, who, _typed_ref(ref, g), _note_other(gt, who, n, d, cyc)))
    cons = [n for n in pool if n.withdrawn is None and valid(n) and n.first_layoff >= dt.date(2026, 10, 20)]
    for n in [cons[int(i)] for i in g.choice(len(cons), 2, replace=False)]:
        start = n.lodged.date() if n.channel == "portal" else n.rekeyed["at"].date()
        d = _workday(start + dt.timedelta(days=12))
        ref = n.ln if n.channel == "portal" else n.rekeyed["ln"]
        txt = ["Employer is considering withdrawing the notice if a tender comes through. Will advise.",
               "the %s thinks they may withdraw, waiting on their directors" % CONTACTS[int(g.integers(len(CONTACTS)))]][len(notes) % 2]
        notes.append((d, "JW" if "Employer" in txt else "RB", _typed_ref(ref, g), txt))
    notes.sort(key=lambda x: (x[0], x[1]))
    rows = []
    k0 = 51120
    for k, (d, who, ref, txt) in enumerate(notes):
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
