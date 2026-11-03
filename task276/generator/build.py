"""Build task276's pack: the clean world first (closures, counts, faults, network), then each organisation's export.

run(target) writes every file under target/ and returns the clean truth W for checks.py."""
import csv
import datetime as dt
import functools
import hashlib
import io
import math
import os

import numpy as np

import params as P
import postprocess

FILES = {
    "barrier": "rail/barrier_events_2025_26.csv",
    "orders": "rail/lx_work_orders_2025_26.csv",
    "occ": "rail/signaller_occurrences_2025_26.xlsx",
    "register": "rail/crossing_register_2025.pdf",
    "plan": "rail/train_service_plan_2026.csv",
    "counts": "highways/approach_counts_2025_26.csv",
    "links": "highways/network_links.csv",
    "nodes": "highways/network_nodes.csv",
    "netreg": "highways/network_register_2026.xlsx",
    "collisions": "highways/road_collisions_2021_2025.csv",
    "brief": "programme/crossing_programme_2027.docx",
    "method": "programme/road_delay_appraisal_conventions.pdf",
    "survey": "programme/queue_survey_march_2026.xlsx",
    "terms": "schools/term_dates_2025_26.xlsx",
}
DISTRACTORS = ["plan", "collisions"]
BANDS = [(5, 7, "early"), (7, 10, "peak"), (10, 16, "day"), (16, 19, "pm"), (19, 21, "late")]
QH = 20                     # quarter hours from 06:00 to 11:00
PROFILE = {
    "school": [0.30, 0.36, 0.44, 0.52, 0.62, 0.75, 0.90, 1.00, 1.04, 1.00, 0.92, 0.82, 0.74, 0.70, 0.68, 0.66,
               0.66, 0.67, 0.68, 0.70],
    "holiday": [0.25, 0.30, 0.37, 0.45, 0.53, 0.62, 0.71, 0.78, 0.82, 0.83, 0.82, 0.80, 0.78, 0.77, 0.76, 0.75,
                0.75, 0.76, 0.77, 0.79],
    "sat": [0.12, 0.15, 0.19, 0.24, 0.29, 0.35, 0.41, 0.47, 0.53, 0.58, 0.62, 0.66, 0.69, 0.72, 0.74, 0.76,
            0.77, 0.78, 0.79, 0.80],
    "sun": [0.07, 0.08, 0.10, 0.13, 0.16, 0.20, 0.24, 0.28, 0.32, 0.37, 0.42, 0.47, 0.51, 0.55, 0.58, 0.61,
            0.63, 0.65, 0.67, 0.69],
}


def rng(*keys):
    h = hashlib.sha256("|".join([P.SEED] + [str(k) for k in keys]).encode()).hexdigest()
    return np.random.default_rng(int(h[:15], 16))


def days():
    d, out = P.D0, []
    while d <= P.D1:
        out.append(d)
        d += dt.timedelta(days=1)
    return out


@functools.lru_cache(maxsize=None)
def county_calendar(county):
    term, half = set(), set()
    for _, s, hs, he, e in P.TERMS[county]:
        s, hs, he, e = (dt.date.fromisoformat(x) for x in (s, hs, he, e))
        d = s
        while d <= e:
            if hs <= d <= he:
                half.add(d)
            else:
                term.add(d)
            d += dt.timedelta(days=1)
    return term, half


def day_type(d, county):
    term, _ = county_calendar(county)
    if d in P.BANK_HOLIDAYS or d.weekday() == 6:
        return "sun"
    if d.weekday() == 5:
        return "sat"
    return "school" if d in term else "holiday"


def school_days(county):
    return [d for d in days() if day_type(d, county) == "school"]


def bst(d):
    return d < P.BST_ENDS or d >= P.BST_STARTS


def in_main(c, d, t):
    """the main call's declared population window: the crossing's county's school day, 06:00 to 11:00 local"""
    return day_type(d, P.CROSSINGS[c]["county"]) == "school" and 6 * 3600 <= t < 11 * 3600


# ---------------------------------------------------------------- closures
def train_closures(c, d):
    """one closure per train, two trains close together sharing one closure; the odd extra path and cancellation"""
    X = P.CROSSINGS[c]
    g = rng("closures", c, d.isoformat(), P.SALTS[c]["cl"])
    dtp = day_type(d, X["county"])
    fac = {"school": 1.0, "holiday": 1.0, "sat": 0.85, "sun": 0.6}[dtp]
    trains = []
    for h0, h1, band in BANDS:
        if dtp == "sun" and band == "early":
            continue
        for h in range(h0, h1):
            r = X["rate"][band] * fac
            n = int(r) + (1 if g.uniform() < r - int(r) else 0)
            ts = [h * 3600 + (k + 0.5 + g.uniform(-0.32, 0.32)) * 3600.0 / n for k in range(n)]
            if g.uniform() < 0.09:
                ts.append(h * 3600 + g.uniform(0, 3600))
            trains += [t for t in ts if g.uniform() >= 0.025]
    trains.sort()
    out = []
    for t in trains:
        dur = max(0.45 * X["dm"], g.normal(X["dm"], X["ds"]))
        t, dur = round(t), round(dur)
        if out and t < out[-1][1] + 35:
            out[-1][1] = max(out[-1][1], t + round(0.55 * dur))
            continue
        out.append([t, t + dur, "train"])
    return out


def extend(closures, i, new_up, kind):
    """a closure held down past its train: later trains pass while the barriers stay down"""
    closures[i][1] = new_up
    closures[i][2] = kind
    j = i + 1
    while j < len(closures) and closures[j][0] < new_up + 30:
        del closures[j]


def pick_closure(c, g, closures_by_day, used, cutoff=None):
    """a closure outside the main population window, chosen at random"""
    ds = days()
    while True:
        d = ds[int(g.integers(0, len(ds)))]
        if cutoff and not cutoff(d):
            continue
        cl = closures_by_day[d]
        i = int(g.integers(0, len(cl)))
        down, up, kind = cl[i]
        school = day_type(d, P.CROSSINGS[c]["county"]) == "school"
        if kind != "train" or (d, i) in used or (school and down < 11 * 3600 + 600 and down + 6600 > 6 * 3600 - 600):
            continue
        if not (5 * 3600 + 600 < down < 19 * 3600):
            continue
        used.add((d, i))
        return d, i


def headcode(g):
    return "%d%s%02d" % (int(g.integers(1, 3)), "ABCDEFHKLNPSTWZ"[int(g.integers(0, 15))], int(g.integers(10, 99)))


def faults_and_long(c, closures_by_day):
    """long closures with no fault, fault-held closures (work orders and signaller resets), and non-closing faults"""
    X = P.CROSSINGS[c]
    g = rng("faults", c, P.SALTS[c]["flt"])
    used, orders, occ = set(), [], []
    n_long = {"A": 3, "B": 2, "C": 2, "D": 3, "E": 2, "F": 3}[c]
    for _ in range(n_long):
        d, i = pick_closure(c, g, closures_by_day, used)
        down = closures_by_day[d][i][0]
        extend(closures_by_day[d], i, down + int(g.integers(11 * 60, 27 * 60)), "long")
        occ.append(dict(date=d, t=down + int(g.integers(3 * 60, 8 * 60)), crossing=c, kind="held",
                        text="%s LC: barriers kept lowered for %s, held at signal on approach, crossing normal after "
                             "train cleared." % (X["name"], headcode(g))))
    n_wo = {"A": 3, "B": 3, "C": 4, "D": 3, "E": 3, "F": 2}[c]
    for k in range(n_wo):
        cutoff = None
        if c == "D":
            cutoff = (lambda d: d >= dt.date(2026, 2, 10)) if k < 2 else (lambda d: d < dt.date(2026, 2, 10))
        d, i = pick_closure(c, g, closures_by_day, used, cutoff)
        down = closures_by_day[d][i][0]
        code = ["BFR", "ODF", "PWR", "BFR"][k % 4]
        rep = down + int(g.integers(4 * 60, 9 * 60))
        att = rep + int(g.integers(22 * 60, 75 * 60))
        up = att + int(g.integers(2 * 60, 8 * 60))
        clr = up + int(g.integers(15 * 60, 95 * 60))
        extend(closures_by_day[d], i, up, "fault")
        asset = X["asset"]
        if c == "D" and d >= dt.date(2026, 2, 10):
            asset = X["renewed"][1]
        orders.append(dict(date=d, crossing=c, asset=asset, code=code, rep=rep, att=att, clr=clr, closing=True))
        if g.uniform() < 0.6:
            hc = headcode(g)
            occ.append(dict(date=d, t=rep + int(g.integers(0, 4 * 60)), crossing=c, kind="dup",
                            text="%s LC: barriers failed to rise after %s, fault reported to Fault Control, "
                                 "crossing attendant requested." % (X["name"], hc)))
    n_occ = {"A": 2, "B": 0, "C": 2, "D": 0, "E": 2, "F": 0}[c]
    for _ in range(n_occ):
        d, i = pick_closure(c, g, closures_by_day, used)
        down, up0, _ = closures_by_day[d][i]
        fail = up0 + int(g.integers(20, 90))
        reset = fail + int(g.integers(3 * 60, 17 * 60))
        extend(closures_by_day[d], i, reset, "reset")
        occ.append(dict(date=d, t=reset + int(g.integers(60, 6 * 60)), crossing=c, kind="reset", fail=fail,
                        reset=reset, text="%s LC: barriers failed to rise after %s passed at %s. Crossing reset from "
                        "panel %s, barriers raised, working normally." % (X["name"], headcode(g), hm(fail), hm(reset))))
    # faults that close nothing: lamps, audible warnings, a barrier that would not lower (crossing attended)
    for k in range(int(g.integers(3, 6))):
        while True:
            d = days()[int(g.integers(0, 365))]
            t = int(g.integers(5 * 3600 + 900, 20 * 3600))
            if not in_main(c, d, t) and not in_main(c, d, t + 7200):
                break
        code = ["LMP", "AUD", "BFL", "LMP", "CCT"][k % 5]
        if k == 0:      # a lamp fault reported while a train closure is down
            cl = closures_by_day[d]
            free = [x for x in cl if x[2] == "train" and not in_main(c, d, x[0]) and 5 * 3600 < x[0] < 20 * 3600]
            x = free[int(g.integers(0, len(free)))]
            t = x[0] + int(g.integers(20, max(30, x[1] - x[0] - 20)))
        att = t + int(g.integers(40 * 60, 240 * 60))
        orders.append(dict(date=d, crossing=c, asset=X["asset"] if not (c == "D" and d >= dt.date(2026, 2, 10))
                           else X["renewed"][1], code=code, rep=t, att=att,
                           clr=att + int(g.integers(20 * 60, 150 * 60)), closing=False))
    return orders, occ


def hm(t):
    t = int(t)
    return "%02d:%02d" % (t // 3600, (t % 3600) // 60)


def hms(t):
    t = int(round(t))
    return "%02d:%02d:%02d" % (t // 3600, (t % 3600) // 60, t % 60)


# ---------------------------------------------------------------- counts
def site_counts(c, k, d):
    X = P.CROSSINGS[c]
    dtp = day_type(d, X["county"])
    g = rng("counts", c, k, d.isoformat())
    level = X["q"][k] * math.exp(g.normal(0, 0.05)) * {"school": 1.0, "holiday": 0.82, "sat": 0.62, "sun": 0.47}[dtp]
    p = X["hgv"][k] + {"school": 0.0, "holiday": 0.008, "sat": -0.012, "sun": -0.025}[dtp]
    veh = g.poisson(level * np.array(PROFILE[dtp]) / 4.0)
    hgv = rng("hgv", c, k, d.isoformat(), P.SALTS[c]["hgv"]).binomial(veh, max(0.005, p))
    return [int(v) for v in veh], [int(h) for h in hgv]


def true_arrivals(c, k, d, veh):
    g = rng("arrivals", c, k, d.isoformat())
    out = []
    for q, n in enumerate(veh):
        t0 = 6 * 3600 + 900 * q
        out.extend(sorted(t0 + g.uniform(0, 900, n)))
    return out


# ---------------------------------------------------------------- network
def network():
    """nodes and links: each shortlisted crossing's road, and the rest of the four counties' A, B and C roads"""
    g = rng("network")
    nodes, links, sites = {}, [], {}
    ids = iter(sorted(set(int(x) for x in g.integers(20000, 79999, 3000)), key=lambda v: g.uniform())[:1800])

    def node(x, y):
        n = next(ids)
        nodes[n] = (int(round(x)), int(round(y)))
        return n

    lref = iter(sorted(set(int(x) for x in g.integers(100000, 999999, 4000)), key=lambda v: g.uniform())[:2500])

    def link(a, b, road, carriage, lanes, speed, length=None):
        ax, ay = nodes[a]
        bx, by = nodes[b]
        L = length if length is not None else int(round(math.hypot(ax - bx, ay - by)))
        links.append(dict(ref="L%d" % next(lref), a=a, b=b, road=road, length=L, carriage=carriage, lanes=lanes,
                          speed=speed))

    roads = {"A": "Station Road", "B": "Mill Lane", "C": "Common Road", "D": "Long Drove", "E": "Church Lane",
             "F": "Moor Road"}
    ends = []
    for c in P.ORDER:
        X = P.CROSSINGS[c]
        x0, y0 = X["grid"]
        x0 += int(g.integers(-4, 5))
        y0 += int(g.integers(-4, 5))
        ax = (1, 0) if X["axis"] == "EW" else (0, 1)
        offs = [-760, -520, -300, 0, 300, 545, 790]
        if c == "B":
            offs = [-760, -520, -300, -70, -42, 0, 300, 545, 790]
        chain = []
        for o in offs:
            wig = 0 if o in (-70, -42, 0) or c == "B" and -100 < o < 0 else int(g.integers(-9, 10))
            chain.append(node(x0 + ax[0] * o + ax[1] * wig, y0 + ax[1] * o + ax[0] * wig))
        lanes = X["lanes"]
        carriage = "dual" if lanes == 2 else "single"
        for i in range(len(chain) - 1):
            o1, o2 = offs[i], offs[i + 1]
            if c == "B" and (o1, o2) == (-70, -42):
                link(chain[i], chain[i + 1], roads[c], "single track", 1, X["speed"], length=28)
            elif c == "B" and (o1, o2) == (-42, 0):
                link(chain[i], chain[i + 1], roads[c], carriage, lanes, X["speed"], length=42)
            else:
                link(chain[i], chain[i + 1], roads[c], carriage, lanes, X["speed"])
        idx = {o: n for o, n in zip(offs, chain)}
        s0, s1 = (idx[300], idx[-300]) if X["axis"] == "EW" else (idx[-300], idx[300])
        sites[c] = dict(cross=idx[0], s0=s0, s1=s1, ends=(chain[0], chain[-1]))
        if c == "B":
            sites[c]["bridge"] = (idx[-42], idx[-70])
        ends += [chain[0], chain[-1]]
    # the rest of the network: county roads between towns, a share of them single track
    names = ["C201", "C208", "C219", "C233", "C240", "C259", "C273", "C214", "C227", "C236", "C251", "C268",
             "High Street", "Market Street", "Back Lane", "Green Lane", "Ings Lane", "Carr Road", "Hollow Lane",
             "Town Street", "Low Road", "Fen Road", "Sandy Lane", "Pinfold Lane", "Westgate", "Northgate"]
    bg = []
    for r, nm in enumerate(names):
        x, y = float(g.uniform(396000, 479000)), float(g.uniform(296000, 371000))
        th = float(g.uniform(0, 2 * math.pi))
        prev = ends[r] if r < len(ends) else node(x, y)
        x, y = nodes[prev]
        seg = []
        for k in range(int(g.integers(6, 15))):
            th += float(g.normal(0, 0.35))
            step = float(g.uniform(150, 650))
            x, y = x + step * math.cos(th), y + step * math.sin(th)
            n = node(x, y)
            if r < 3:
                carriage, lanes, sp = "single", 1, 60
            elif r < 7:
                carriage, lanes, sp = "single", 1, 50
            else:
                track = g.uniform() < 0.22
                carriage, lanes, sp = ("single track", 1, 40) if track else ("single", 1, 30 if g.uniform() < 0.5 else 40)
            link(prev, n, nm, carriage, lanes, sp)
            seg.append(n)
            prev = n
        bg.append((nm, seg))
    return nodes, links, sites, bg


def signal_sites(bg, sites, g):
    """the highway authority's signal timing register: junctions, pedestrian crossings and two shuttle sites"""
    out = []
    refs = iter(sorted(set(int(x) for x in g.integers(1100, 2999, 400)), key=lambda v: g.uniform())[:60])
    b = sites["B"]["bridge"]
    out.append(dict(site=P.BRIDGE["site"], node=b[0], road="Mill Lane", desc="Shuttle working, single-track river bridge",
                    control="Fixed time (AM plan %s, cycle zero %s)" % (P.BRIDGE["plan"], P.BRIDGE["plan_start"]),
                    cycle=P.BRIDGE["cycle"], s1="westbound", g1=P.BRIDGE["wb_green"], i1=P.BRIDGE["ig1"],
                    s2="eastbound", g2=P.BRIDGE["eb_green"], i2=P.BRIDGE["ig2"], sat="1800 / 1800"))
    pool = [(nm, n) for nm, seg in bg for n in seg[1:-1]]
    pick = sorted(set(int(x) for x in g.integers(0, len(pool), 40)))
    kinds = ["junction"] * 9 + ["puffin"] * 6 + ["shuttle"]
    order = [int(x) for x in g.permutation(len(kinds))]
    for j, k in enumerate(order):
        nm, n = pool[pick[j * 2 % len(pick)]]
        kind = kinds[k]
        site = "%s %d" % ({"junction": "SJ", "puffin": "SP", "shuttle": "SS"}[kind], next(refs))
        if kind == "junction":
            out.append(dict(site=site, node=n, road=nm, desc="Junction, %d arms" % int(g.integers(3, 5)),
                            control="MOVA" if g.uniform() < 0.5 else "VA", cycle=None, s1="main road",
                            g1=int(g.integers(28, 55)), i1=5, s2="side road", g2=int(g.integers(12, 30)), i2=5,
                            sat="%d / %d" % (int(g.integers(17, 20)) * 100, int(g.integers(16, 19)) * 100)))
        elif kind == "puffin":
            out.append(dict(site=site, node=n, road=nm, desc="Puffin crossing", control="VA", cycle=None, s1="traffic",
                            g1=int(g.integers(20, 40)), i1=3, s2="pedestrian", g2=int(g.integers(6, 9)), i2=8,
                            sat="1800"))
        else:
            out.append(dict(site=site, node=n, road=nm, desc="Shuttle working, single-track bridge",
                            control="Fixed time (all day, cycle zero 00:00:00)", cycle=90, s1="northbound", g1=30,
                            i1=12, s2="southbound", g2=36, i2=12, sat="1700 / 1700"))
    return out


# ---------------------------------------------------------------- world
def world():
    W = dict(closures={}, counts={}, orders=[], occ=[])
    for c in P.ORDER:
        cbd = {d: train_closures(c, d) for d in days()}
        o, oc = faults_and_long(c, cbd)
        W["closures"][c] = cbd
        W["orders"] += o
        W["occ"] += oc
        for k in (0, 1):
            for d in days():
                W["counts"][(c, k, d)] = site_counts(c, k, d)
    W["nodes"], W["links"], W["sites"], W["bg"] = network()
    W["signals"] = signal_sites(W["bg"], W["sites"], rng("signals"))
    return W


# ---------------------------------------------------------------- writers
def utc(d, t):
    off = 3600 if bst(d) else 0
    base = dt.datetime(d.year, d.month, d.day) + dt.timedelta(seconds=int(round(t)) - off)
    return base.strftime("%Y-%m-%dT%H:%M:%SZ")


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)


def elr_code(X):
    return "%s %03d.%02d" % (X["elr"], X["miles"], X["chains"])


def write_barrier(target, W):
    ev = []
    for c in P.ORDER:
        X = P.CROSSINGS[c]
        g = rng("bounce", c)
        for d in days():
            for down, up, kind in W["closures"][c][d]:
                for t, e in ((down, "LOWERED"), (up, "RAISED")):
                    ev.append((utc(d, t), elr_code(X), e, d, t))
                    if g.uniform() < 0.031:
                        ev.append((utc(d, t + float(g.uniform(0.6, 2.4))), elr_code(X), e, d, t + 1))
    ev.sort(key=lambda r: (r[0], r[1]))
    g = rng("eventids")
    eid = 418000000 + int(g.integers(0, 90000))
    rows = []
    for r in ev:
        eid += int(g.integers(1, 9))
        rows.append([eid, r[1], r[0], r[2]])
    write_csv(os.path.join(target, FILES["barrier"]), ["event_id", "lx_ref", "event_time_utc", "event_type"], rows)
    return len(rows)


def count_site_refs():
    g = rng("siterefs")
    refs = sorted(set(int(x) for x in g.integers(30100, 34999, 80)), key=lambda v: g.uniform())
    return refs


def write_counts(target, W):
    refs = count_site_refs()
    meta, rows = {}, []
    i = 0
    for c in P.ORDER:
        for k in (0, 1):
            meta[(c, k)] = "ATC %d" % refs[i]
            i += 1
    g = rng("dropouts")
    sw = dt.date.fromisoformat(P.SWITCH_DATE)
    for c in P.ORDER:
        X = P.CROSSINGS[c]
        for k in (0, 1):
            older_all = P.QT40_ALL_YEAR.get(c) == k
            older_switch = P.QT40_SWITCHED.get(c) == k
            for d in days():
                veh, hgv = W["counts"][(c, k, d)]
                drop = set()
                if day_type(d, X["county"]) != "school" and g.uniform() < 0.07:
                    s = int(g.integers(0, QH - 3))
                    drop = set(range(s, s + int(g.integers(1, 4))))
                for q in range(QH):
                    if q in drop:
                        continue
                    share = older_all or (older_switch and d < sw)
                    h = int(round(100.0 * hgv[q] / veh[q])) if share and veh[q] else (0 if share else hgv[q])
                    rows.append([meta[(c, k)], d.isoformat(), "%02d:%02d" % (6 + q // 4, 15 * (q % 4)), veh[q], h])
    write_csv(os.path.join(target, FILES["counts"]), ["site_ref", "count_date", "interval_start", "veh_total", "veh_hgv"], rows)
    return meta, len(rows)


def write_network(target, W):
    nodes = sorted(W["nodes"].items(), key=lambda kv: kv[0])
    write_csv(os.path.join(target, FILES["nodes"]), ["node_ref", "easting", "northing"], [[n, x, y] for n, (x, y) in nodes])
    rows = [[L["ref"], L["a"], L["b"], L["road"], L["length"], L["carriage"], L["lanes"], L["speed"]]
            for L in sorted(W["links"], key=lambda L: L["ref"])]
    write_csv(os.path.join(target, FILES["links"]),
              ["link_ref", "from_node", "to_node", "road_name", "length_m", "carriageway", "lanes_each_direction",
               "speed_limit_mph"], rows)


def xlsx_save(wb, path, created, modified, company):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb.save(path)
    postprocess.scrub(path, company, created[:10])
    postprocess.finish_office(path, created, modified, company)


def write_netreg(target, W, meta):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Count sites"
    ws.append(["Site ref", "Node ref", "Road name", "Location", "Direction counted", "Counter model", "Installed on"])
    for cell in ws[1]:
        cell.font = Font(bold=True)
    g = rng("netreg")
    rows = []
    for c in P.ORDER:
        X = P.CROSSINGS[c]
        s = W["sites"][c]
        side = {"EW": ("east of", "west of"), "NS": ("south of", "north of")}[X["axis"]]
        for k in (0, 1):
            node = s["s0"] if k == 0 else s["s1"]
            older_all = P.QT40_ALL_YEAR.get(c) == k
            older_switch = P.QT40_SWITCHED.get(c) == k
            if older_all:
                model, inst = "QT-40", "%d-%02d-%02d" % (2017 + int(g.integers(0, 3)), int(g.integers(1, 13)), int(g.integers(1, 28)))
            elif older_switch:
                model, inst = "RX-5", P.SWITCH_DATE
            else:
                model, inst = "RX-5", "%d-%02d-%02d" % (2022 + int(g.integers(0, 3)), int(g.integers(1, 13)), int(g.integers(1, 28)))
            rows.append([meta[(c, k)], node, X["name"],
                         "%s, %d m %s level crossing" % (X["name"], P.COUNT_SITE_M, side[k]), X["dirs"][k], model,
                         dt.date.fromisoformat(inst)])
    others = count_site_refs()[12:21]
    pool = [(nm, n) for nm, seg in W["bg"] for n in seg[1:-1]]
    for j, ref in enumerate(others):
        nm, n = pool[int(g.integers(0, len(pool)))]
        model = "QT-40" if g.uniform() < 0.35 else "RX-5"
        rows.append(["ATC %d" % ref, n, nm, "%s, at node %d" % (nm, n), "both", model,
                     dt.date(2016 + int(g.integers(0, 9)), int(g.integers(1, 13)), int(g.integers(1, 28)))])
    rows.sort(key=lambda r: r[0])
    for r in rows:
        ws.append(r)
        ws.cell(ws.max_row, 7).number_format = "dd/mm/yyyy"
    for col, w in zip("ABCDEFG", (11, 8, 20, 40, 17, 14, 11)):
        ws.column_dimensions[col].width = w
    ws2 = wb.create_sheet("Signal sites")
    ws2.append(["Site ref", "Node ref", "Road name", "Description", "Control", "Cycle (s)", "Stage 1", "Stage 1 green (s)",
                "Intergreen 1 (s)", "Stage 2", "Stage 2 green (s)", "Intergreen 2 (s)", "Saturation flow (veh/h)"])
    for cell in ws2[1]:
        cell.font = Font(bold=True)
    for s in sorted(W["signals"], key=lambda s: s["site"]):
        ws2.append([s["site"], s["node"], s["road"], s["desc"], s["control"], s["cycle"], s["s1"], s["g1"], s["i1"],
                    s["s2"], s["g2"], s["i2"], s["sat"]])
    for col, w in zip("ABCDEFGHIJKLM", (9, 8, 16, 40, 38, 9, 11, 9, 9, 11, 9, 9, 13)):
        ws2.column_dimensions[col].width = w
    wb.properties.creator = "Signals and Monitoring"
    xlsx_save(wb, os.path.join(target, FILES["netreg"]), "2026-07-28T09:14:00Z", "2026-09-07T15:41:00Z", P.HIGHWAYS)


def write_terms(target):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    first = True
    for county in ["Northshire", "Southshire", "Eastshire", "Westshire"]:
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = county
        ws.append(["%s County Council: school term and holiday dates 2025/26 (community and voluntary controlled "
                   "schools)" % county])
        ws["A1"].font = Font(bold=True)
        ws.append([])
        ws.append(["Term name", "Term starts", "Half term from", "Half term to", "Term ends"])
        for cell in ws[3]:
            cell.font = Font(bold=True)
        for t, s, hs, he, e in P.TERMS[county]:
            ws.append([t] + [dt.date.fromisoformat(x) for x in (s, hs, he, e)])
            for col in range(2, 6):
                ws.cell(ws.max_row, col).number_format = "ddd dd mmm yyyy"
        ws.append([])
        ws.append(["Schools are closed on bank holidays that fall in term."])
        for col, w in zip("ABCDE", (14, 17, 17, 17, 17)):
            ws.column_dimensions[col].width = w
    ws = wb.create_sheet("Bank holidays")
    ws.append(["Bank holidays in England, 2025/26"])
    ws["A1"].font = Font(bold=True)
    for d in P.BANK_HOLIDAYS:
        ws.append([d])
        ws.cell(ws.max_row, 1).number_format = "dddd dd mmmm yyyy"
    ws.column_dimensions["A"].width = 30
    wb.properties.creator = "School Admissions"
    xlsx_save(wb, os.path.join(target, FILES["terms"]), "2025-03-11T10:02:00Z", "2025-06-30T14:27:00Z", "Shires councils")


def write_orders(target, W):
    g = rng("woids")
    refs = sorted(set(int(x) for x in g.integers(7400000, 7999999, 600)), key=lambda v: g.uniform())
    desc = {"BFR": "Barriers failed to raise", "ODF": "Obstacle detection fault, barriers held lowered",
            "PWR": "Power supply failure, barriers lowered on failsafe", "LMP": "Road traffic light lamp failure",
            "AUD": "Audible warning device fault", "BFL": "Barriers failed to lower, crossing attended",
            "CCT": "CCTV picture degraded"}
    rows = []
    allo = list(W["orders"])
    # the maintainer's export also carries the four other crossings' equipment
    for elr, mi, ch, nm, typ, county, grid, asset, *_ in P.OTHER_CROSSINGS:
        for k in range(int(g.integers(2, 6))):
            d = days()[int(g.integers(0, 365))]
            t = int(g.integers(5 * 3600, 21 * 3600))
            att = t + int(g.integers(30 * 60, 200 * 60))
            allo.append(dict(date=d, crossing=None, asset=asset, code=["LMP", "BFR", "AUD", "ODF", "BFL"][k % 5], rep=t,
                             att=att, clr=att + int(g.integers(20 * 60, 120 * 60)), closing=False))
    allo.sort(key=lambda o: (o["date"], o["rep"]))
    for j, o in enumerate(allo):
        def stamp(t):
            base = dt.datetime(o["date"].year, o["date"].month, o["date"].day)
            return (base + dt.timedelta(seconds=int(t))).strftime("%d/%m/%Y %H:%M")
        o["wo"] = "WO%d" % refs[j]
        rows.append([o["wo"], o["asset"], o["code"], desc[o["code"]], stamp(o["rep"]), stamp(o["att"]), stamp(o["clr"]),
                     "Closed"])
    write_csv(os.path.join(target, FILES["orders"]), ["work_order", "asset_no", "fault_code", "fault_text", "reported_at",
                                                      "attended_at", "cleared_at", "wo_status"], rows)
    return allo


def write_occ(target, W):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment
    g = rng("occ")
    box = {"NSB": "Northshire branch panel", "WVL": "Westshire line panel", "EFL": "Eastshire line box",
           "SCL": "Southshire line panel"}
    entries = [dict(date=o["date"], t=o["t"], box=box[P.CROSSINGS[o["crossing"]]["elr"]], text=o["text"]) for o in W["occ"]]
    other = ["%s LC: CCTV picture lost, crossing worked on local monitor, restored %s.",
             "%s LC: vehicle reported stopped on crossing, driver moved on before the next train.",
             "%s LC: pedestrian crossed after the lights showed, reported to police.",
             "%s LC: road works on the approach, temporary lights in place, crossing working normally.",
             "%s LC: barrier skirt reported damaged, Fault Control informed, no effect on working."]
    for c in P.ORDER:
        X = P.CROSSINGS[c]
        for k in range(int(g.integers(6, 12))):
            while True:
                d = days()[int(g.integers(0, 365))]
                t = int(g.integers(5 * 3600, 21 * 3600))
                if not in_main(c, d, t):
                    break
            tx = other[int(g.integers(0, len(other)))]
            tx = tx % ((X["name"], hm(t + 1800)) if tx.count("%s") == 2 else (X["name"],))
            entries.append(dict(date=d, t=t, box=box[X["elr"]], text=tx))
    entries.sort(key=lambda e: (e["date"], e["t"]))
    wb = Workbook()
    ws = wb.active
    ws.title = "Occurrences"
    ws.append(["Occ date", "Occ time", "Signal box", "Entry"])
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for e in entries:
        ws.append([e["date"], hm(e["t"]), e["box"], e["text"]])
        ws.cell(ws.max_row, 1).number_format = "dd/mm/yyyy"
        ws.cell(ws.max_row, 4).alignment = Alignment(wrap_text=True)
    for col, w in zip("ABCD", (11, 7, 24, 96)):
        ws.column_dimensions[col].width = w
    wb.properties.creator = "Shires route control"
    xlsx_save(wb, os.path.join(target, FILES["occ"]), "2026-09-02T08:40:00Z", "2026-09-08T11:05:00Z", P.RAIL)


def write_survey(target, W):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    g = rng("survey")
    wb = Workbook()
    ws = wb.active
    ws.title = "Queue at rise"
    ws.append(["Level crossing", "Survey date", "Barriers down", "Barriers up", "Approach", "Vehicles queued at rise", "Surveyor"])
    for cell in ws[1]:
        cell.font = Font(bold=True)
    teams = ["JR", "MK", "SP", "TD"]
    rows = []
    for c in P.ORDER:
        X = P.CROSSINGS[c]
        sd = [d for d in school_days(X["county"]) if d.month == 3]
        pick = sorted(sd[i] for i in sorted(set(int(x) for x in g.choice(len(sd), 3, replace=False))))
        for d in pick:
            team = teams[int(g.integers(0, 4))]
            for down, up, kind in W["closures"][c][d]:
                if not (7 * 3600 <= down < 9 * 3600 + 1800):
                    continue
                for k in (0, 1):
                    veh, _ = W["counts"][(c, k, d)]
                    arr = true_arrivals(c, k, d, veh)
                    n = sum(1 for a in arr if down <= a < up)
                    n = max(0, n + int(round(g.normal(0, 1.1))))
                    rows.append([X["name"], d, hms(down + g.integers(-3, 4)), hms(up + g.integers(-3, 4)),
                                 X["dirs"][k], n, team])
    for r in rows:
        ws.append(r)
        ws.cell(ws.max_row, 2).number_format = "dd/mm/yyyy"
    for col, w in zip("ABCDEFG", (15, 11, 13, 12, 14, 22, 9)):
        ws.column_dimensions[col].width = w
    wb.properties.creator = "Traffic survey team"
    xlsx_save(wb, os.path.join(target, FILES["survey"]), "2026-03-02T07:55:00Z", "2026-03-20T16:12:00Z", P.BOARD)
    return len(rows)


def write_plan(target):
    g = rng("plan")
    rows = []
    for elr in ["NSB", "WVL", "EFL", "SCL"]:
        for dayset in ["Mon-Fri", "Sat", "Sun"]:
            for h in range(5, 23):
                base = {"NSB": 2, "WVL": 2, "EFL": 1, "SCL": 2}[elr]
                if dayset == "Sun" and h < 8:
                    continue
                up = base + (1 if 7 <= h < 10 or 16 <= h < 19 else 0) - (1 if dayset == "Sun" and g.uniform() < 0.4 else 0)
                rows.append([elr, dayset, "%02d:00" % h, max(0, up), max(0, up + int(g.integers(-1, 1))),
                             int(g.integers(0, 3)) if elr in ("WVL", "EFL") else int(g.integers(0, 2))])
    write_csv(os.path.join(target, FILES["plan"]), ["route_code", "day_set", "hour_starting", "passenger_up",
                                                     "passenger_down", "freight_paths"], rows)


def write_collisions(target, W):
    g = rng("collisions")
    rows = []
    refs = sorted(set(int(x) for x in g.integers(100000, 999999, 900)), key=lambda v: g.uniform())
    pool = list(W["nodes"].values())
    for j in range(347):
        y = 2021 + int(g.integers(0, 5))
        d = dt.date(y, 1, 1) + dt.timedelta(days=int(g.integers(0, 365)))
        x, yy = pool[int(g.integers(0, len(pool)))]
        sev = g.choice(["Slight", "Slight", "Slight", "Slight", "Serious", "Fatal"], p=[0.2, 0.2, 0.2, 0.22, 0.16, 0.02])
        rows.append(["%d%02d%06d" % (y, int(g.integers(30, 34)), refs[j]), d.isoformat(),
                     "%02d:%02d" % (int(g.integers(6, 23)), int(g.integers(0, 60))), x + int(g.integers(-60, 60)),
                     yy + int(g.integers(-60, 60)), str(sev), int(g.integers(1, 4)), int(g.integers(1, 3))])
    rows.sort(key=lambda r: (r[1], r[2]))
    write_csv(os.path.join(target, FILES["collisions"]), ["collision_ref", "acc_date", "acc_time", "easting", "northing",
                                                          "severity", "no_vehicles", "no_casualties"], rows)


def pdf_doc(path, title, author, flow, producer, stamp, landscape_page=False):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.platypus import SimpleDocTemplate
    os.makedirs(os.path.dirname(path), exist_ok=True)
    size = landscape(A4) if landscape_page else A4
    doc = SimpleDocTemplate(path, pagesize=size, title=title, author=author, creator=author,
                            leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    doc.build(flow)
    postprocess.scrub(path, producer, stamp)


def write_register(target):
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
    ss = getSampleStyleSheet()
    head = ["Ref", "Crossing", "Type", "County", "OS grid ref", "Barrier asset", "Line speed", "Trains/day",
            "Vehicles/day", "Risk"]
    rows = [head]
    census = {"A": (64, 3120, "C5"), "B": (58, 2460, "C6"), "C": (88, 9850, "B4"), "D": (41, 2980, "C4"),
              "E": (77, 5260, "C3"), "F": (60, 3540, "D4")}
    speeds = {"A": 40, "B": 70, "C": 75, "D": 60, "E": 75, "F": 60}
    allr = []
    for c in P.ORDER:
        X = P.CROSSINGS[c]
        allr.append((X["elr"], X["miles"], X["chains"], X["name"], X["type"], X["county"],
                     (X["grid"][0] // 10 * 10, X["grid"][1] // 10 * 10), X["asset"], speeds[c]) + census[c])
    for elr, mi, ch, nm, typ, county, grid, asset, spd, tr, veh, risk in P.OTHER_CROSSINGS:
        allr.append((elr, mi, ch, nm, typ, county, grid, asset, spd, tr, veh, risk))
    allr.sort(key=lambda r: (r[0], r[1], r[2]))
    for elr, mi, ch, nm, typ, county, grid, asset, spd, tr, veh, risk in allr:
        rows.append(["%s %dm %02dch" % (elr, mi, ch), nm, typ, county, "%d %d" % grid, asset, "%d mph" % spd,
                     str(tr), "{:,}".format(veh), risk])
    t = Table(rows, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    flow = [Paragraph("Level crossing register: extract for the Shires route", ss["Heading2"]),
            Paragraph("Route Asset Management. Extract taken 14 May 2025 for the Shires Transport Board. Census figures "
                      "from the last census at each crossing. Risk is the crossing's individual and collective risk "
                      "ranking from the crossing's most recent assessment.", ss["Normal"]),
            Spacer(1, 10), t,
            Spacer(1, 10),
            Paragraph("Types: MCB manually controlled barriers; MCB-CCTV manually controlled barriers with CCTV; AHB "
                      "automatic half barriers; AOCL+B automatic open crossing with barriers; UWC-T user worked crossing "
                      "with telephones.", ss["Normal"])]
    pdf_doc(os.path.join(target, FILES["register"]), "Level crossing register extract", "Route Asset Management", flow,
            "Microsoft: Print To PDF", "2025-05-14", landscape_page=True)


def write_method(target):
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, Spacer
    ss = getSampleStyleSheet()
    body = [
        ("Road user delay appraisal: conventions", "Heading1"),
        ("Shires Transport Board, Strategy and Appraisal. Version 3, March 2024, replacing version 2 of June 2021.",
         "Normal"),
        ("These conventions apply to every estimate of road user delay that the Board's programmes and business cases "
         "make, whatever the scheme. Where a programme defines its own measure, the programme's definition decides "
         "what is measured and these conventions decide the constants it is measured with.", "Normal"),
        ("1. Saturation flow", "Heading3"),
        ("Unless the signal timing register gives a surveyed figure for a stop line, a traffic lane discharges a "
         "standing queue at 1,800 vehicles an hour.", "Normal"),
        ("2. Queued vehicles", "Heading3"),
        ("A queued vehicle occupies 5.75 metres of lane. Queue lengths surveyed in metres are converted at that "
         "figure.", "Normal"),
        ("3. Traffic counts", "Heading3"),
        ("Vehicles recorded in a count interval are taken to arrive evenly through the interval.", "Normal"),
        ("4. Signal-controlled stop lines", "Heading3"),
        ("Effective green is taken as the displayed green of the controller's timing plan, at the saturation flow the "
         "timing register gives for the stage.", "Normal"),
        ("5. Values of time", "Heading3"),
        ("Per vehicle-hour, 2024 prices, occupancy included: car 16.30, light goods vehicle 19.90, heavy goods "
         "vehicle 27.40, bus 94.10 (pounds sterling).", "Normal"),
        ("6. Reporting", "Heading3"),
        ("Delay is reported in vehicle-hours over the days the measure covers. Values are applied only in the "
         "business case.", "Normal"),
    ]
    flow = []
    for text, style in body:
        flow.append(Paragraph(text, ss[style]))
        if style == "Normal":
            flow.append(Spacer(1, 4))
    pdf_doc(os.path.join(target, FILES["method"]), "Road user delay appraisal: conventions", "Strategy and Appraisal",
            flow, "Microsoft Word 2016", "2024-03-18")


def lean_docx(path):
    """keep only the styles the document uses, as Word saves a short paper"""
    import re
    import zipfile
    with zipfile.ZipFile(path) as z:
        order = [i.filename for i in z.infolist()]
        parts = {n: z.read(n) for n in order}
    doc = parts["word/document.xml"]
    used = set(re.findall(rb'<w:(?:pStyle|rStyle|tblStyle) w:val="([^"]+)"', doc))
    sx = parts["word/styles.xml"]
    blocks = re.findall(rb"<w:style\b.*?</w:style>", sx, flags=re.S)
    byid = {re.search(rb'w:styleId="([^"]+)"', b).group(1): b for b in blocks}
    keep = set(used) | {re.search(rb'w:styleId="([^"]+)"', b).group(1) for b in blocks if b'w:default="1"' in b}
    grow = True
    while grow:
        grow = False
        for sid in list(keep):
            for ref in re.findall(rb'<w:(?:basedOn|link|next) w:val="([^"]+)"', byid.get(sid, b"")):
                if ref in byid and ref not in keep:
                    keep.add(ref)
                    grow = True
    for b in blocks:
        if re.search(rb'w:styleId="([^"]+)"', b).group(1) not in keep:
            sx = sx.replace(b, b"")
    parts["word/styles.xml"] = sx
    with zipfile.ZipFile(path, "w") as z:
        for n in order:
            zi = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, parts[n])


def house_style(d):
    """the organisation's own heading style: Arial, dark grey, no theme font"""
    from docx.oxml.ns import qn
    from docx.shared import Pt, RGBColor
    for name, size in (("Heading 1", 14), ("Heading 2", 11.5)):
        st = d.styles[name]
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = RGBColor(0x26, 0x26, 0x26)
        rpr = st.element.get_or_add_rPr()
        rf = rpr.find(qn("w:rFonts"))
        if rf is None:
            rf = rpr.makeelement(qn("w:rFonts"), {})
            rpr.insert(0, rf)
        for k in list(rf.attrib):
            del rf.attrib[k]
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), "Arial")


def write_brief(target):
    import docx
    from docx.shared import Pt
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10.5)
    house_style(d)
    d.add_heading("Level Crossing Replacement Programme: selection of the 2027 scheme", level=1)
    d.add_paragraph("Programme Board paper LCRP/26/07, September 2026. Author: %s, Programme Manager." % P.PM)
    d.add_heading("1. Purpose", level=2)
    d.add_paragraph("The Board's capital programme for 2027/28 funds the replacement of one level crossing on the "
                    "programme shortlist by a road bridge or a realignment. This paper sets out the basis on which the "
                    "selection panel will choose it at its meeting on 12 November 2026.")
    d.add_heading("2. Shortlist", level=2)
    d.add_paragraph("The shortlist was agreed by the Programme Board in March 2025 from the crossings on the Board's "
                    "A, B and C roads where the railway runs more than forty trains a day.")
    t = d.add_table(rows=1, cols=3)
    t.style = "Table Grid"
    for i, h in enumerate(["Crossing", "Railway reference", "County"]):
        t.rows[0].cells[i].text = h
    for c in ["C", "D", "B", "F", "A", "E"]:
        X = P.CROSSINGS[c]
        r = t.add_row().cells
        r[0].text = X["name"]
        r[1].text = "%s %dm %02dch" % (X["elr"], X["miles"], X["chains"])
        r[2].text = X["county"]
    d.add_heading("3. Basis of selection", level=2)
    d.add_paragraph("3.1 The 2027 scheme goes to the shortlisted crossing whose barrier closures cost road users the "
                    "most delay on school-day mornings.")
    d.add_paragraph("3.2 The delay a crossing causes is the extra time that vehicles counted on its approaches between "
                    "07:00 and 10:00 take to reach the count site on the far side of the crossing because the barriers "
                    "were lowered, against the same morning with the barriers left raised. It is summed over the school "
                    "days of the 2025/26 school year and expressed in vehicle-hours, with the Board's appraisal "
                    "conventions.")
    d.add_paragraph("3.3 School days are the weekdays inside the published term dates of the county the crossing lies "
                    "in, outside half terms and bank holidays.")
    d.add_paragraph("3.4 The railway timetable and the road network at each shortlisted crossing are unchanged into "
                    "2027, so the 2025/26 school year is the record the choice is made on.")
    d.add_heading("4. Business case", level=2)
    d.add_paragraph("The panel paper also carries, for each crossing, how often its barriers close, how reliable they "
                    "have been and the heavy goods vehicle share of its morning traffic, which the business case uses "
                    "with the Board's values of time.")
    d.add_heading("5. Timetable and funding", level=2)
    d.add_paragraph("Analysis complete by 30 October 2026; selection panel 12 November 2026; design from April 2027. "
                    "The capital programme holds 14.6 million pounds for the scheme.")
    d.core_properties.author = P.PM
    d.core_properties.title = "Selection of the 2027 scheme"
    d.core_properties.revision = 4
    path = os.path.join(target, FILES["brief"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    d.save(path)
    lean_docx(path)
    postprocess.scrub(path, P.BOARD, "2026-09-03")
    postprocess.finish_office(path, "2026-08-27T13:20:00Z", "2026-09-03T10:46:00Z", P.BOARD)


def run(target):
    W = world()
    n_barrier = write_barrier(target, W)
    meta, n_counts = write_counts(target, W)
    W["site_refs"] = meta
    write_network(target, W)
    write_netreg(target, W, meta)
    write_terms(target)
    W["orders"] = write_orders(target, W)
    write_occ(target, W)
    W["survey_rows"] = write_survey(target, W)
    write_plan(target)
    write_collisions(target, W)
    write_register(target)
    write_method(target)
    write_brief(target)
    W["rows"] = dict(barrier=n_barrier, counts=n_counts)
    return W
