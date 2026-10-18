"""Every figure from the shipped pack alone: each core tract's people present on an average weekday, each core's
delivery-weighted density and the share of its people present in tracts of 20,000 or more per km2, the pick, and
both asks. Routes other than the golden are here too, so checks.py can assert every rung and fork."""
import csv
import os
import statistics

import numpy as np
import openpyxl

import common as K

RINGS = ("C", "O", "X")


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def load(pack):
    p = lambda k: os.path.join(pack, K.FILES[k])
    D = {}
    D["od"] = read_csv(p("od_main")) + [dict(x, part="aux") for x in read_csv(p("od_aux"))]
    D["survey"] = read_csv(p("survey"))
    with open(p("population"), newline="") as f:
        rows = list(csv.reader(f))
    D["pop"] = {r[0].replace("1400000US", ""): int(r[2]) for r in rows[2:]}
    with open(p("gazetteer")) as f:
        lines = [l.rstrip("\n").split("\t") for l in f]
    head = [h.strip() for h in lines[0]]
    D["gaz"] = {r[head.index("GEOID")]: dict(zip(head, r)) for r in lines[1:]}
    wb = openpyxl.load_workbook(p("delineation"), read_only=True)
    ws = wb["List 1"]
    rows = list(ws.iter_rows(values_only=True))
    hi = [i for i, r in enumerate(rows) if r and r[0] == "CBSA Code"][0]
    head = rows[hi]
    D["delin"] = []
    for r in rows[hi + 1:]:
        if not r or not r[0] or not str(r[0]).strip().isdigit():
            continue
        d = dict(zip(head, r))
        D["delin"].append(d)
    wb = openpyxl.load_workbook(p("cores"), read_only=True)
    rows = list(wb["Core tracts"].iter_rows(values_only=True))
    D["cores"] = {}
    for r in rows[1:]:
        if r and r[0]:
            D["cores"].setdefault(r[0], []).append(str(r[3]))
    D["listings"] = read_csv(p("listings"))
    D["locators"] = read_csv(p("locators"))
    D["acs_commute"] = read_csv(p("acs_commute"))
    return D


# ------------------------------------------------------------------------------------------------- the survey
def shares(D, cells="gr", weighted=True, per="weekday", waves=None, months_equal=False):
    """Share of weekdays on the employer's premises, by industry group (g) and residence relation (r)."""
    num, den = {}, {}
    wave_tot = {}
    if months_equal:
        for x in D["survey"]:
            wave_tot[x["WAVE"]] = wave_tot.get(x["WAVE"], 0.0) + float(x["FINALWT"])
    for x in D["survey"]:
        if x["HOMEREL"] not in ("1", "2", "3"):
            continue
        if waves and x["WAVE"] not in waves:
            continue
        g = K.SECTOR_GROUP[x["NAICS_SECTOR"]]
        rr = {"1": "C", "2": "O", "3": "X"}[x["HOMEREL"]]
        key = (g if "g" in cells else "*", rr if "r" in cells else "*")
        w = float(x["FINALWT"]) if weighted else 1.0
        if months_equal:
            w = w / wave_tot[x["WAVE"]]
        d = 5 if per == "weekday" else 5 - int(x["DAYS_NOTWORK"])
        if d == 0:
            continue
        num[key] = num.get(key, 0.0) + w * int(x["DAYS_PREM"])
        den[key] = den.get(key, 0.0) + w * d
    return {k: num[k] / den[k] for k in num}


def route_rate(route, D):
    """The share each route carries onto a flow, as a function (group, ring) -> share."""
    if route == "cadp":
        return lambda g, r: 1.0
    if route == "acs":
        return None
    spec = {"one": dict(cells=""), "pool": dict(cells="g"), "ring": dict(cells="r"), "golden": dict(cells="gr"),
            "unweighted": dict(cells="gr", weighted=False), "per_workday": dict(cells="gr", per="workday"),
            "sep_wave": dict(cells="gr", waves=("202609",)), "months_equal": dict(cells="gr", months_equal=True),
            "pool_unweighted": dict(cells="g", weighted=False)}[route]
    tab = shares(D, **spec)
    c = spec["cells"]
    return lambda g, r: tab[(g if "g" in c else "*", r if "r" in c else "*")]


# ------------------------------------------------------------------------------------------------- the geography
def geography(D):
    """For each metro: its CBSA's counties by type, from the delineation file, keyed by the central county."""
    by_cbsa = {}
    for d in D["delin"]:
        fips = str(d["FIPS State Code"]).zfill(2) + str(d["FIPS County Code"]).zfill(3)
        by_cbsa.setdefault(str(d["CBSA Code"]), {})[fips] = d["Central/Outlying County"]
    county_cbsa = {}
    for cb, cs in by_cbsa.items():
        for c in cs:
            county_cbsa[c] = cb
    return by_cbsa, county_cbsa


def ring_of(home, work, by_cbsa, county_cbsa):
    """Where the worker lives relative to the metropolitan area of the workplace: its central county (C), an outlying
    county of it (O) or outside it (X)."""
    cb = county_cbsa.get(work[:5])
    if cb is None:
        return "X"
    t = by_cbsa[cb].get(home[:5])
    if t is None:
        return "X"
    return "C" if t == "Central" else "O"


def land_km2(D, g, sqmi=False):
    z = D["gaz"][g]
    return float(z["ALAND_SQMI"]) * 2.589988110336 if sqmi else int(z["ALAND"]) / 1e6


def presence(D, rate, drop_aux=False, acs_wfh=None, sqmi=False):
    """People present on an average weekday in every core tract: residents, less residents at a workplace in
    another tract, plus people from other tracts at a workplace in it."""
    by_cbsa, county_cbsa = geography(D)
    core_set = {g for gs in D["cores"].values() for g in gs}
    P = {g: float(D["pop"].get(g, 0)) for g in core_set}
    for x in D["od"]:
        if drop_aux and x.get("part") == "aux":
            continue
        w, h = x["w_tract"], x["h_tract"]
        if w == h:
            continue
        gs = {g: int(x[g]) for g in K.GROUPS}
        if h in core_set:
            rr = ring_of(h, w, by_cbsa, county_cbsa)
            P[h] -= sum(n * (acs_wfh(h) if acs_wfh else rate(g, rr)) for g, n in gs.items())
        if w in core_set:
            rr = ring_of(h, w, by_cbsa, county_cbsa)
            P[w] += sum(n * (acs_wfh(h) if acs_wfh else rate(g, rr)) for g, n in gs.items())
    return P


def core_figures(D, P, sqmi=False):
    out = {}
    for m, gs in D["cores"].items():
        rows = []
        for g in gs:
            a = land_km2(D, g, sqmi)
            if a <= 0:
                continue
            rows.append((g, P[g], a, P[g] / a))
        tot = sum(p for _, p, _, _ in rows)
        pwd = sum(p * d for _, p, _, d in rows) / tot
        dense = sum(p for _, p, _, d in rows if d >= K.DENSE) / tot
        out[m] = dict(present=tot, pwd=pwd, dense=dense, tracts=rows)
    return out


def acs_route(D):
    """The working-from-home share of each home county from the ACS table, taken off every worker living there
    (out-of-state homes keep every worker)."""
    wfh = {}
    for x in D["acs_commute"][1:]:
        c = x["GEO_ID"].replace("0500000US", "")
        wfh[c] = int(x["B08301_021E"]) / int(x["B08301_001E"])
    return lambda h: 1 - wfh.get(h[:5], 0.0)


def run(D, route="golden", **kw):
    if route == "acs":
        P = presence(D, None, acs_wfh=acs_route(D), **{k: v for k, v in kw.items() if k == "drop_aux"})
    else:
        P = presence(D, route_rate(route, D), **{k: v for k, v in kw.items() if k == "drop_aux"})
    F = core_figures(D, P, sqmi=kw.get("sqmi", False))
    order = sorted(F, key=lambda m: -F[m]["pwd"])
    return dict(P=P, F=F, order=order, pick=order[0], margin=F[order[0]]["pwd"] / F[order[1]]["pwd"])


# ------------------------------------------------------------------------------------------------- the asks
def rate_m2(x):
    rent, sf = float(x["asking_rent"]), int(x["space_sf"])
    if x["rent_basis"] == "/SF/YR":
        return rent * K.SQFT_PER_M2
    if x["rent_basis"] == "/SF/MO":
        return rent * 12 * K.SQFT_PER_M2
    return rent * 12 / (sf / K.SQFT_PER_M2)


def on_market(x, day="2026-09-30"):
    if x["date_listed"] > day or x["floor"] != "1" or x["property_type"] not in ("Retail", "Flex"):
        return False
    m2 = int(x["space_sf"]) / K.SQFT_PER_M2
    if not 150 <= m2 <= 450:
        return False
    return x["status"] == "Available" or (x["status_date"] > day)


def ask_a(D, handling="golden"):
    """Each core's ground-floor retail or flex units of 150 to 450 m2 on the market on 30 September 2026 and their
    median asking rent per m2 a year. A listing with no suite at an address whose suites are all listed, its size
    their sum, is that floor listed whole: the same units again."""
    out = {}
    for m, gs in D["cores"].items():
        tracts = set(gs)
        rows = [x for x in D["listings"] if x["census_tract"] in tracts and on_market(x)]
        if handling == "golden":
            keep = []
            for x in rows:
                parts = [y for y in rows if y is not x and y["address"] == x["address"] and y["suite"]]
                whole = (not x["suite"] and len(parts) >= 2 and abs(sum(int(y["space_sf"]) for y in parts) - int(x["space_sf"])) <= 5)
                if not whole:
                    keep.append(x)
            rows = keep
        elif handling == "per_address":
            seen, keep = set(), []
            for x in rows:
                if x["address"] not in seen:
                    seen.add(x["address"])
                    keep.append(x)
            rows = keep
        elif handling == "status_as_exported":
            rows = [x for x in rows if x["status"] == "Available"]
        rents = [rate_m2(x) for x in rows]
        out[m] = (len(rows), statistics.median(rents) if rents else None)
    return out


def ask_b(D, handling="golden", day="2026-09-30"):
    """How many dark stores each competitor was delivering from in each core on 30 September 2026: the stores in that
    day's scrape with Delivery among their services, less any shop both competitors list at the same address and unit
    (a shop neither runs)."""
    rows = [x for x in D["locators"] if x["scrape_date"] == day and "Delivery" in x["services"]]
    key = lambda x: (x["address"], x["unit"])
    both = {key(x) for x in rows if x["brand"] == K.BRANDS[0]} & {key(x) for x in rows if x["brand"] == K.BRANDS[1]}
    streets = {x["address"] for x in rows if x["brand"] == K.BRANDS[0]} & {x["address"] for x in rows if x["brand"] == K.BRANDS[1]}
    out = {}
    for m, gs in D["cores"].items():
        tracts = set(gs)
        for b in K.BRANDS:
            sel = [x for x in rows if x["brand"] == b and x["census_tract"] in tracts]
            if handling == "golden":
                sel = [x for x in sel if key(x) not in both]
            elif handling == "per_street":
                sel = [x for x in sel if x["address"] not in streets]
            out[(m, b)] = len(sel)
    return out
