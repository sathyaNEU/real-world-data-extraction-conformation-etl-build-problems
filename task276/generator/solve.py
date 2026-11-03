"""Every figure from the shipped bundle alone: the golden, each rung of the ladder, each ask's routes.

solve(target) reads only files under target/ and returns S."""
import bisect
import collections
import csv
import datetime as dt
import os
import re

import docx
import pdfplumber
from openpyxl import load_workbook

F = {
    "barrier": "rail/barrier_events_2025_26.csv", "orders": "rail/lx_work_orders_2025_26.csv",
    "occ": "rail/signaller_occurrences_2025_26.xlsx", "register": "rail/crossing_register_2025.pdf",
    "counts": "highways/approach_counts_2025_26.csv", "links": "highways/network_links.csv",
    "nodes": "highways/network_nodes.csv", "netreg": "highways/network_register_2026.xlsx",
    "brief": "programme/crossing_programme_2027.docx", "method": "programme/road_delay_appraisal_conventions.pdf",
    "survey": "programme/queue_survey_march_2026.xlsx", "terms": "schools/term_dates_2025_26.xlsx",
}
CLOSING = {"BFR", "ODF", "PWR"}
T7, T10 = 7 * 3600, 10 * 3600


def pdf_text(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join(p.extract_text() or "" for p in pdf.pages)


# ---------------------------------------------------------------- documents
def register(target):
    out = {}
    pat = re.compile(r"^([A-Z]{3}) (\d+)m (\d+)ch (.+?) (MCB-CCTV|MCB|AHB|AOCL\+B|UWC-T) (\w+shire) (\d{6}) (\d{6}) "
                     r"(LXB/\d+) (\d+) mph (\d+) ([\d,]+) ([A-Z]\d)$")
    for line in pdf_text(os.path.join(target, F["register"])).splitlines():
        m = pat.match(line.strip())
        if m:
            elr, mi, ch, name, typ, county, e, n, asset, spd, tr, veh, risk = m.groups()
            out[name] = dict(elr=elr, miles=int(mi), chains=int(ch), type=typ, county=county, grid=(int(e), int(n)),
                             asset=asset, trains=int(tr), vehicles=int(veh.replace(",", "")), risk=risk)
    return out


def shortlist(target):
    d = docx.Document(os.path.join(target, F["brief"]))
    names = [r.cells[0].text.strip() for r in d.tables[0].rows[1:]]
    text = "\n".join(p.text for p in d.paragraphs)
    return names, text


def method(target):
    text = pdf_text(os.path.join(target, F["method"]))
    flat = re.sub(r"\s+", " ", text)
    sat = int(re.search(r"discharges a standing queue at ([\d,]+) vehicles an hour", flat).group(1).replace(",", ""))
    vlen = float(re.search(r"A queued vehicle occupies ([\d.]+) metres", flat).group(1))
    return dict(sat=sat, vlen=vlen, text=flat)


def school_days(target):
    wb = load_workbook(os.path.join(target, F["terms"]), read_only=True)
    bh = set()
    for r in wb["Bank holidays"].iter_rows(min_row=2, values_only=True):
        if r and r[0]:
            bh.add(r[0].date() if hasattr(r[0], "date") else r[0])
    out = {}
    for county in ["Northshire", "Southshire", "Eastshire", "Westshire"]:
        days = set()
        for r in wb[county].iter_rows(min_row=4, values_only=True):
            if not r or not isinstance(r[1], dt.datetime):
                continue
            s, hs, he, e = (x.date() for x in r[1:5])
            d = s
            while d <= e:
                if d.weekday() < 5 and not (hs <= d <= he) and d not in bh:
                    days.add(d)
                d += dt.timedelta(days=1)
        out[county] = days
    return out, bh


# ---------------------------------------------------------------- the barrier log
def london_offset(u):
    """UK clock rule: summer time from 01:00 UTC on the last Sunday of March to 01:00 UTC on the last Sunday of October"""
    def last_sunday(y, m):
        d = dt.date(y, m, 31)
        return d - dt.timedelta(days=(d.weekday() + 1) % 7)
    y = u.year
    start = dt.datetime.combine(last_sunday(y, 3), dt.time(1))
    end = dt.datetime.combine(last_sunday(y, 10), dt.time(1))
    return 3600 if start <= u < end else 0


def closures(target, dedupe=True, convert=True):
    """crossing code -> date -> sorted [(down, up)] in local seconds; bounce repeats (the same event again within a few
    seconds) dropped"""
    ev = collections.defaultdict(list)
    with open(os.path.join(target, F["barrier"]), newline="") as fh:
        for r in csv.DictReader(fh):
            u = dt.datetime.strptime(r["event_time_utc"], "%Y-%m-%dT%H:%M:%SZ")
            ev[r["lx_ref"]].append((u, r["event_type"]))
    out = {}
    for code, rows in ev.items():
        rows.sort()
        kept, last = [], None
        for u, e in rows:
            if dedupe and last is not None and e == last[1] and (u - last[0]).total_seconds() <= 3:
                continue
            kept.append((u, e))
            last = (u, e)
        by = collections.defaultdict(list)
        down = None
        for u, e in kept:
            loc = u + dt.timedelta(seconds=london_offset(u) if convert else 0)
            if e == "LOWERED" and down is None:
                down = loc
            elif e == "RAISED" and down is not None:
                d = down.date()
                base = dt.datetime.combine(d, dt.time(0))
                by[d].append(((down - base).total_seconds(), (loc - base).total_seconds()))
                down = None
        out[code] = dict(by)
    return out


def code_of(reg):
    return "%s %03d.%02d" % (reg["elr"], reg["miles"], reg["chains"])


# ---------------------------------------------------------------- counts and the network
def counts(target):
    out = collections.defaultdict(dict)
    with open(os.path.join(target, F["counts"]), newline="") as fh:
        for r in csv.DictReader(fh):
            d = dt.date.fromisoformat(r["count_date"])
            hh, mm = r["interval_start"].split(":")
            q = (int(hh) - 6) * 4 + int(mm) // 15
            out[(r["site_ref"], d)][q] = (int(r["veh_total"]), int(r["veh_hgv"]))
    return out


def netreg(target):
    wb = load_workbook(os.path.join(target, F["netreg"]), read_only=True)
    sites = []
    for r in wb["Count sites"].iter_rows(min_row=2, values_only=True):
        if r and r[0]:
            inst = r[6].date() if hasattr(r[6], "date") else r[6]
            sites.append(dict(site=r[0], node=int(r[1]), road=r[2], location=r[3], direction=r[4], counter=r[5],
                              installed=inst))
    sig = []
    for r in wb["Signal sites"].iter_rows(min_row=2, values_only=True):
        if r and r[0]:
            sig.append(dict(site=r[0], node=int(r[1]), road=r[2], desc=r[3], control=r[4], cycle=r[5], s1=r[6],
                            g1=r[7], i1=r[8], s2=r[9], g2=r[10], i2=r[11], sat=str(r[12])))
    return sites, sig


def network(target):
    nodes = {}
    with open(os.path.join(target, F["nodes"]), newline="") as fh:
        for r in csv.DictReader(fh):
            nodes[int(r["node_ref"])] = (int(r["easting"]), int(r["northing"]))
    adj = collections.defaultdict(list)
    links = []
    with open(os.path.join(target, F["links"]), newline="") as fh:
        for r in csv.DictReader(fh):
            L = dict(a=int(r["from_node"]), b=int(r["to_node"]), road=r["road_name"], length=float(r["length_m"]),
                     carriage=r["carriageway"], lanes=int(r["lanes_each_direction"]))
            links.append(L)
            adj[L["a"]].append((L["b"], L))
            adj[L["b"]].append((L["a"], L))
    return nodes, adj, links


def path(adj, a, b):
    prev, q, seen = {a: None}, collections.deque([a]), {a}
    while q:
        x = q.popleft()
        if x == b:
            break
        for y, L in adj[x]:
            if y not in seen:
                seen.add(y)
                prev[y] = (x, L)
                q.append(y)
    out, x = [], b
    while prev[x] is not None:
        p, L = prev[x]
        out.append((p, x, L))
        x = p
    return out[::-1]


def layout(target, reg, names):
    """each shortlisted crossing's node, approach sites, lanes and the controls between its two count sites"""
    nodes, adj, links = network(target)
    sites, sig = netreg(target)
    sig_by_node = {s["node"]: s for s in sig}
    out = {}
    for name in names:
        g = reg[name]["grid"]
        node = min(nodes, key=lambda n: (nodes[n][0] - g[0]) ** 2 + (nodes[n][1] - g[1]) ** 2)
        mine = [s for s in sites if s["location"].split(",")[0].strip() == name]
        lanes = max(L["lanes"] for _, L in adj[node])
        p = path(adj, mine[0]["node"], mine[1]["node"])
        on = [x for _, x, _ in p[:-1]]
        ctrl = [sig_by_node[n] for n in on if n in sig_by_node]
        gate = None
        for s in ctrl:
            if s["desc"].startswith("Shuttle"):
                # the shuttle's own stop line is the site's node; the single-track link beyond it is the bridge
                near = [(x, L) for x, L in adj[s["node"]] if L["carriage"] != "single track"]
                far = [(x, L) for x, L in adj[s["node"]] if L["carriage"] == "single track"]
                storage_link = [L for x, L in near if x == node or L["a"] == node or L["b"] == node]
                gate = dict(site=s, storage_m=storage_link[0]["length"], bridge_m=far[0][1]["length"])
        out[name] = dict(node=node, sites=mine, lanes=lanes, controls=ctrl, gate=gate, path=p)
    return out


# ---------------------------------------------------------------- the replay
def arrivals(cnt, mode="even"):
    """count rows -> arrival seconds; vehicles in a quarter hour arrive evenly through it"""
    out, tag = [], []
    for q in range(16):                         # 06:00 to 10:00; later vehicles cannot delay earlier ones
        n = cnt[q][0]
        t0 = 6 * 3600 + 900 * q
        for j in range(n):
            out.append(t0 + (j + 0.5) * 900.0 / n if mode == "even" else t0 + j * 900.0 / n)
            tag.append(q >= 4)
    return out, tag


def pass_free(arr, cl, h):
    downs = [x[0] for x in cl]
    ups = [x[1] for x in cl]
    n, j, last, out = len(cl), 0, -1e18, []
    for a in arr:
        t = a if a > last + h else last + h
        while j < n and ups[j] <= t:
            j += 1
        if j < n and downs[j] <= t:
            t = ups[j]
        out.append(t)
        last = t
    return out


def green(s, off, cyc, g0, g1):
    ph = (s - off) % cyc
    return s if g0 <= ph < g1 else s + (g0 - ph) % cyc


def pass_down_gate(arr, cl, h, N, gp, hb, tau=0.0):
    """barrier first, then a fixed-time stop line N vehicles of storage downstream: exit times past the stop line"""
    downs = [x[0] for x in cl]
    ups = [x[1] for x in cl]
    n, j, lb, lc, b, c = len(cl), 0, -1e18, -1e18, [], []
    off, cyc, g0, g1 = gp
    for i, a in enumerate(arr):
        t = a if a > lb + h else lb + h
        while True:
            t0 = t
            if i >= N and c[i - N] > t:
                t = c[i - N]
            while j < n and ups[j] <= t:
                j += 1
            if j < n and downs[j] <= t:
                t = ups[j]
            if t == t0:
                break
        b.append(t)
        lb = t
        s = t + tau if t + tau > lc + hb else lc + hb
        s = green(s, off, cyc, g0, g1)
        c.append(s)
        lc = s
    return c


def pass_up_gate(arr, cl, h, N, gp, hb, tau=0.0):
    """a fixed-time stop line first, N vehicles of storage, then the barrier: exit times past the barrier"""
    downs = [x[0] for x in cl]
    ups = [x[1] for x in cl]
    n, j, lb, lc, b, c = len(cl), 0, -1e18, -1e18, [], []
    off, cyc, g0, g1 = gp
    for i, a in enumerate(arr):
        s = a if a > lc + hb else lc + hb
        while True:
            s0 = s
            if i >= N and b[i - N] > s:
                s = b[i - N]
            s = green(s, off, cyc, g0, g1)
            if s == s0:
                break
        c.append(s)
        lc = s
        t = s + tau if s + tau > lb + h else lb + h
        while j < n and ups[j] <= t:
            j += 1
        if j < n and downs[j] <= t:
            t = ups[j]
        b.append(t)
        lb = t
    return b


def gate_plans(gate):
    s = gate["site"]
    m = re.search(r"cycle zero (\d\d):(\d\d):(\d\d)", s["control"])
    off = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
    cyc = float(s["cycle"])
    plans = {}
    start = 0.0
    for stage, g, ig in ((s["s1"], s["g1"], s["i1"]), (s["s2"], s["g2"], s["i2"])):
        plans[stage] = (off, cyc, start, start + float(g))
        start += float(g) + float(ig)
    sat = [int(x) for x in re.findall(r"\d+", s["sat"])]
    return plans, sat


def crossing_delay(name, L, reg, cl_by_day, cnt, sdays, M, variant=None):
    """vehicle-hours over the school days; variant: None (golden replay through the section's controls), 'free' (the
    closure model, barrier only), 'wb_only' (the shuttle for the queue it meets downstream only), or a dict of
    convention changes"""
    v = variant if isinstance(variant, dict) else {}
    mode = v.get("mode", "even")
    h = 3600.0 / (M["sat"] * L["lanes"])
    total = 0.0
    code = code_of(reg[name])
    gate = L["gate"] if variant not in ("free",) else None
    if gate:
        plans, sat = gate_plans(gate)
        N = v.get("N", int(gate["storage_m"] // M["vlen"]))
        tau = v.get("tau", 0.0)
    for d in sdays:
        cl = cl_by_day[code].get(d, [])
        if v.get("start7"):
            cl = [x for x in cl if x[1] > T7]
        for s in L["sites"]:
            arr, tag = arrivals(cnt[(s["site"], d)], mode)
            if v.get("start7"):
                keep = [i for i, a in enumerate(arr) if a >= T7]
                arr, tag = [arr[i] for i in keep], [tag[i] for i in keep]
            if gate and s["direction"] in plans:
                own = plans[s["direction"]]
                hb = 3600.0 / sat[0]
                downstream = gate_is_downstream(L, s, gate)
                if variant == "wb_only" and not downstream:
                    w, w0 = pass_free(arr, cl, h), pass_free(arr, [], h)
                elif downstream:
                    w, w0 = pass_down_gate(arr, cl, h, N, own, hb, tau), pass_down_gate(arr, [], h, N, own, hb, tau)
                else:
                    w, w0 = pass_up_gate(arr, cl, h, N, own, hb, tau), pass_up_gate(arr, [], h, N, own, hb, tau)
            else:
                w, w0 = pass_free(arr, cl, h), pass_free(arr, [], h)
            total += sum(x - y for x, y, k in zip(w, w0, tag) if k)
    return total / 3600.0


def gate_is_downstream(L, s, gate):
    """the shuttle lies between the crossing and the far count site when the approach site is on the other side"""
    p = L["path"]
    seq = [p[0][0]] + [x for _, x, _ in p]
    i_site, i_x, i_g = seq.index(s["node"]), seq.index(L["node"]), seq.index(gate["site"]["node"])
    return (i_site < i_x < i_g) or (i_site > i_x > i_g)


# ---------------------------------------------------------------- the asks
def orders(target):
    out = []
    with open(os.path.join(target, F["orders"]), newline="") as fh:
        for r in csv.DictReader(fh):
            p = lambda s: dt.datetime.strptime(s, "%d/%m/%Y %H:%M")
            out.append(dict(wo=r["work_order"], asset=r["asset_no"], code=r["fault_code"], rep=p(r["reported_at"]),
                            att=p(r["attended_at"]), clr=p(r["cleared_at"])))
    return out


def occurrences(target):
    wb = load_workbook(os.path.join(target, F["occ"]), read_only=True)
    out = []
    for r in wb["Occurrences"].iter_rows(min_row=2, values_only=True):
        if r and r[0]:
            d = r[0].date() if hasattr(r[0], "date") else r[0]
            out.append(dict(date=d, time=r[1], box=r[2], text=r[3]))
    return out


def closure_at(cl_day, t):
    for x in cl_day:
        if x[0] <= t <= x[1]:
            return x
    return None


def fault_hours(target, reg, names, cl_by_day, route="golden"):
    """hours of barrier closure, 1 September 2025 to 31 August 2026, in closures a fault held down"""
    by_asset = {reg[n]["asset"]: n for n in reg}
    held = {n: set() for n in names}
    spans = {n: 0.0 for n in names}
    for o in orders(target):
        if o["code"] not in CLOSING:
            continue
        name = by_asset.get(o["asset"])
        d = o["rep"].date()
        t = (o["rep"] - dt.datetime.combine(d, dt.time(0))).total_seconds()
        if route == "lazy":
            if name in held:
                spans[name] += (o["clr"] - o["rep"]).total_seconds() / 3600.0
            continue
        if name is None and route == "golden":
            # a machine the register does not list: the crossing whose barriers were held down at that minute
            hits = [n for n in names if (x := closure_at(cl_by_day[code_of(reg[n])].get(d, []), t + 30)) and x[1] - x[0] > 600]
            name = hits[0] if len(hits) == 1 else None
        if name not in held:
            continue
        x = closure_at(cl_by_day[code_of(reg[name])].get(d, []), t + 30)
        if x:
            held[name].add((d, x))
    if route in ("full_short_f3", "golden"):
        pat = re.compile(r"^(.+?) LC: barriers failed to rise after \w+ passed at (\d\d):(\d\d)\. Crossing reset from "
                         r"panel (\d\d):(\d\d)")
        for e in occurrences(target):
            m = pat.match(e["text"])
            if not m or m.group(1) not in held:
                continue
            name = m.group(1)
            reset = int(m.group(4)) * 3600 + int(m.group(5)) * 60
            cands = [x for x in cl_by_day[code_of(reg[name])].get(e["date"], []) if reset <= x[1] < reset + 60]
            if len(cands) == 1:
                held[name].add((e["date"], cands[0]))
    if route == "lazy":
        return spans
    return {n: sum(x[1] - x[0] for _, x in held[n]) / 3600.0 for n in names}


def long_closure_hours(reg, names, cl_by_day, minutes=10):
    return {n: sum(x[1] - x[0] for d, cl in cl_by_day[code_of(reg[n])].items() for x in cl if x[1] - x[0] > minutes * 60)
            / 3600.0 for n in names}


def share_rows(cnt, site, before):
    """does a site's heavy column rise with its flow?  a share of the interval's vehicles does not"""
    lo, hi = [], []
    for (s, d), rows in cnt.items():
        if s != site or (before is not None and not (d < before)) or (before is None and False):
            continue
        for q, (v, h) in rows.items():
            if v < 45:
                lo.append(h / max(v, 1))
            elif v > 95:
                hi.append(h / v)
    if not lo or not hi:
        return False
    return (sum(lo) / len(lo)) > 2.0 * (sum(hi) / len(hi))


def hgv_share(L, names, cnt, sdays_by_name, route="golden"):
    out = {}
    for n in names:
        hv = tv = 0.0
        for s in L[n]["sites"]:
            older_all = s["counter"] == "QT-40"
            inst = s["installed"]
            switched = (not older_all) and share_rows(cnt, s["site"], inst)
            for d in sdays_by_name[n]:
                rows = cnt[(s["site"], d)]
                share = (route in ("f4", "golden") and older_all) or (route == "golden" and switched and d < inst)
                for q in range(4, 16):
                    v, h = rows[q]
                    hv += h * v / 100.0 if share else h
                    tv += v
        out[n] = 100.0 * hv / tv
    return out


# ---------------------------------------------------------------- everything
def solve(target, variants=False):
    reg = register(target)
    names, brief = shortlist(target)
    M = method(target)
    sd, bh = school_days(target)
    cl = closures(target)
    cnt = counts(target)
    L = layout(target, reg, names)
    sdays = {n: sorted(sd[reg[n]["county"]]) for n in names}
    S = dict(names=names, reg=reg, M=M, layout=L, sdays=sdays)
    S["delay"] = {n: crossing_delay(n, L[n], reg, cl, cnt, sdays[n], M) for n in names}
    S["free"] = {n: (S["delay"][n] if L[n]["gate"] is None else crossing_delay(n, L[n], reg, cl, cnt, sdays[n], M, "free"))
                 for n in names}
    S["wb_only"] = {n: (S["delay"][n] if L[n]["gate"] is None else crossing_delay(n, L[n], reg, cl, cnt, sdays[n], M,
                                                                                    "wb_only")) for n in names}
    per = {}
    for n in names:
        code = code_of(reg[n])
        k = mins = held_veh = 0.0
        for d in sdays[n]:
            day = cl[code].get(d, [])
            k += sum(1 for x in day if T7 <= x[0] < T10)
            mins += sum(max(0.0, min(x[1], T10) - max(x[0], T7)) for x in day) / 60.0
            for s in L[n]["sites"]:
                arr, tag = arrivals(cnt[(s["site"], d)])
                held_veh += sum(1 for a, t in zip(arr, tag) if t and closure_at(day, a))
        per[n] = dict(closures=k / len(sdays[n]), minutes=mins / len(sdays[n]), held=held_veh / len(sdays[n]))
    S["per"] = per
    S["fault"] = {r: fault_hours(target, reg, names, cl, r) for r in ("lazy", "careful", "full_short_f3", "golden")}
    S["fault"]["long10"] = long_closure_hours(reg, names, cl)
    S["hgv"] = {r: hgv_share(L, names, cnt, sdays, r) for r in ("lazy", "f4", "golden")}
    rank = sorted(names, key=lambda n: -S["delay"][n])
    S["call"], S["runner"] = rank[0], rank[1]
    S["gap"] = S["delay"][rank[0]] - S["delay"][rank[1]]
    if variants:
        S["variants"] = {}
        gated = [n for n in names if L[n]["gate"]]
        for key, v in (("start_mode", {"mode": "start"}), ("N6", {"N": 6}), ("N8", {"N": 8}), ("tau2", {"tau": 2.0}),
                       ("tau5", {"tau": 5.0}), ("start7", {"start7": True})):
            S["variants"][key] = {n: (crossing_delay(n, L[n], reg, cl, cnt, sdays[n], M, v) if (n in gated or key in
                                      ("start_mode", "start7")) else S["delay"][n]) for n in names}
        cl_raw = closures(target, dedupe=False)
        S["variants"]["no_dedupe"] = {n: crossing_delay(n, L[n], reg, cl_raw, cnt, sdays[n], M) for n in names}
        cl_utc = closures(target, convert=False)
        S["variants"]["utc_unconverted_free"] = {n: crossing_delay(n, L[n], reg, cl_utc, cnt, sdays[n], M, "free")
                                                 for n in names}
        S["fault"]["unconverted"] = fault_hours(target, reg, names, cl_utc, "golden")
    return S
