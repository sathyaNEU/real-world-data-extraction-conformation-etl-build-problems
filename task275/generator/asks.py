"""The asks, read from the pack: each segment's first-sale value of its 2025 landings (Ask A) and its vessels' days at
sea in 2025 (Ask B), with the routes that stop short of each."""
from __future__ import annotations

import collections
import datetime as dt
import math

import common as K
import pack as PK


def _nm(a, b):
    la = math.radians((a[0] + b[0]) / 2)
    return math.hypot((b[1] - a[1]) * 60 * math.cos(la), (b[0] - a[0]) * 60)


def market_ports(target):
    return {r["port_name"] for r in PK.ports(target) if r["fish_market"] == "Y"}


def market_buyers(target):
    """the registered buyer that is the fish market of each market port: the buyer with the most notes there"""
    c = collections.Counter()
    mk = market_ports(target)
    for r in PK.sales(target):
        if r["port_of_landing"] in mk:
            c[(r["port_of_landing"], r["buyer_reg_no"])] += 1
    out = {}
    for (port, b), n in sorted(c.items(), key=lambda kv: -kv[1]):
        out.setdefault(port, b)
    return out


def _lot_key(r):
    return (r["vessel_pln"], r["landing_date"], r["port_of_landing"], r["species"], r["size_grade"])


def copy_rows(target, tol=0.03, weight=True, grade=True):
    """the lines another buyer filed for a lot a fish market sold: at a market port, a non-market line with the same
    vessel, landing, species and grade as a market lot, its weight within tol of the lot's (weight=False: any
    weight, the over-cleaning reading; grade=False: the lot keyed without its grade)"""
    rows = PK.sales(target)
    mkt = market_buyers(target)
    key = _lot_key if grade else (lambda r: _lot_key(r)[:4])
    lots = collections.defaultdict(list)
    for r in rows:
        p = r["port_of_landing"]
        if p in mkt and r["buyer_reg_no"] == mkt[p]:
            lots[key(r)].append(float(r["weight_kg"]))
    out = set()
    for i, r in enumerate(rows):
        p = r["port_of_landing"]
        if p in mkt and r["buyer_reg_no"] != mkt[p]:
            w = float(r["weight_kg"])
            ms = lots.get(key(r), [])
            if ms and (not weight or any(abs(w - m) <= tol * m for m in ms)):
                out.add(i)
    return out


def exact_repeats(target):
    """lines repeating another line's vessel, landing, species, grade, weight and price under another note"""
    rows = PK.sales(target)
    seen = {}
    out = set()
    for i, r in enumerate(rows):
        k = _lot_key(r) + (r["weight_kg"], r["price_gbp_per_kg"])
        if k in seen and rows[seen[k]]["sales_note_no"] != r["sales_note_no"]:
            out.add(i)
        else:
            seen.setdefault(k, i)
    return out


def first_sale(target, drop=None, by="landing"):
    """GBP thousands a segment: every sales note line for a landing of 2025 (by="landing"), or every line with a
    2025 sale date (by="sale"), or every line in the extract (by=None), leaving out the line indices in drop"""
    reg = PK.register(target)
    drop = drop or set()
    out = collections.Counter()
    for i, r in enumerate(PK.sales(target)):
        if i in drop:
            continue
        if by == "landing" and not r["landing_date"].startswith("2025"):
            continue
        if by == "sale" and not r["sale_date"].startswith("2025"):
            continue
        out[reg[r["vessel_pln"]]["segment"]] += float(r["value_gbp"])
    return {s: out[s] / 1000.0 for s in K.SEG}


def copies(target):
    """(the merchant's market lines identified, the lines the over-cleaning reading drops)"""
    return copy_rows(target), copy_rows(target, weight=False)


def _limits(target):
    return [((float(r["harbour_lat"]), float(r["harbour_lon"])), float(r["port_limit_radius_nm"]))
            for r in PK.ports(target)]


def holders(target):
    """{terminal: [(role, vessel_pln)]} from the PO's equipment record, role "cur" or "prev\""""
    out = collections.defaultdict(list)
    for r in PK.transponders(target):
        out[r["terminal_id"]].append(("cur", r["vessel_pln"]))
        if r["previous_terminal_id"]:
            out[r["previous_terminal_id"]].append(("prev", r["vessel_pln"]))
    return out


def owners(target):
    """the vessel that carried each report's terminal, as a function of (terminal, utc): a terminal the record holds
    for one vessel is that vessel's; a terminal one vessel carried before and another carries now is the first
    vessel's until the first vessel's own terminal began reporting and the second's once the second vessel's previous
    terminal stopped; (None, n) with n the reports that fall between"""
    hold = holders(target)
    cur = {r["vessel_pln"]: r["terminal_id"] for r in PK.transponders(target)}
    prev = {r["vessel_pln"]: r["previous_terminal_id"] for r in PK.transponders(target)}
    first, last = {}, {}
    for r in PK.vms(target):
        u, t = r["terminal_id"], PK.parse(r["position_utc"])
        first[u] = min(first.get(u, t), t)
        last[u] = max(last.get(u, t), t)
    between = [0]

    def who(u, t):
        hs = hold.get(u, [])
        if len(hs) == 1:
            return hs[0][1]
        if len(hs) != 2:
            return None
        P = next(p for role, p in hs if role == "prev")
        Q = next(p for role, p in hs if role == "cur")
        if cur[P] in first and t < first[cur[P]]:
            return P
        if prev[Q] in last and t > last[prev[Q]]:
            return Q
        between[0] += 1
        return None
    return who, between


def vessel_days(target, attribution="record", clock="uk", where="limits"):
    """{vessel_pln: set of dates at sea}: attribution "record" (the vessel that carried the terminal, from the PO's
    equipment record), "label" (the vessel the extract names), "current" (the vessel whose current terminal it is,
    other terminals' reports left out) or "first" (a terminal on two vessels given to the one that had it first);
    clock "uk" or "utc"; where "limits" (outside every port limit), "speed" (reported speed of 1 knot or more) or
    "any" (every report)"""
    lim = _limits(target)
    who, _ = owners(target)
    hold = holders(target)
    days = collections.defaultdict(set)
    for r in PK.vms(target):
        t = PK.parse(r["position_utc"])
        la, lo = float(r["latitude"]), float(r["longitude"])
        if where == "limits" and any(_nm((la, lo), c) <= rad for c, rad in lim):
            continue
        if where == "speed" and float(r["speed_kn"]) < 1.0:
            continue
        u = r["terminal_id"]
        if attribution == "label":
            pln = r["vessel_pln"]
        elif attribution == "current":
            pln = next((p for role, p in hold.get(u, []) if role == "cur"), None)
        elif attribution == "first":
            hs = hold.get(u, [])
            pln = next((p for role, p in hs if role == "prev"), None) if len(hs) == 2 else (hs[0][1] if hs else None)
        else:
            pln = who(u, t)
        if pln is None:
            continue
        day = (K.to_local(t) if clock == "uk" else t).date()
        if day.year == K.YEAR:
            days[pln].add(day)
    return days


def days_at_sea(target, **kw):
    reg = PK.register(target)
    out = collections.Counter()
    for pln, ds in vessel_days(target, **kw).items():
        out[reg[pln]["segment"]] += len(ds)
    return {s: out[s] for s in K.SEG}


def logbook_days(target):
    """the calendar days (UK) from each logbook trip's departure to its return"""
    reg = PK.register(target)
    days = collections.defaultdict(set)
    for r in PK.rows(target, "trips"):
        a = K.to_local(PK.parse(r["departure_utc"])).date()
        b = K.to_local(PK.parse(r["return_utc"])).date()
        while a <= b:
            days[r["vessel_pln"]].add(a)
            a += dt.timedelta(days=1)
    out = collections.Counter()
    for pln, ds in days.items():
        out[reg[pln]["segment"]] += len(ds)
    return {s: out[s] for s in K.SEG}


def ask_a(target):
    return {s: round(v, 1) for s, v in first_sale(target, drop=copy_rows(target)).items()}


def ask_b(target):
    return days_at_sea(target)


def ask_a_routes(target):
    cp, over = copies(target)
    return {"A1 the merchant's lines kept": first_sale(target),
            "A2 sale dates in 2025": first_sale(target, drop=cp, by="sale"),
            "A3 both": first_sale(target, by="sale"),
            "A4 every line of the extract": first_sale(target, drop=cp, by=None),
            "A5 every other buyer's line on a market lot dropped": first_sale(target, drop=over),
            "A6 exact repeats dropped": first_sale(target, drop=exact_repeats(target))}


def ask_b_routes(target):
    return {"B1 the vessel the extract names": days_at_sea(target, attribution="label"),
            "B2 UTC days": days_at_sea(target, clock="utc"),
            "B3 the vessel the extract names, UTC days": days_at_sea(target, attribution="label", clock="utc"),
            "B4 moving reports, not the port limits": days_at_sea(target, where="speed"),
            "B5 the logbook's trips": logbook_days(target),
            "B6 the record's current terminals only": days_at_sea(target, attribution="current"),
            "B7 a terminal on two vessels given to the first": days_at_sea(target, attribution="first")}
