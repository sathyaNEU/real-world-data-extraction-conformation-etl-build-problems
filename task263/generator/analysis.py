"""Every route through the pack, read from the shipped files alone: the wells' own water by the mass balance of the
entry-point samples (the golden) and the shortcuts below it (the ladder), the grants and the walk down the list, and
the asks. build.py writes the goldens from it and checks.py asserts on it."""
from __future__ import annotations

import collections
import csv
import datetime as dt
import os
import re
import subprocess

import numpy as np
from openpyxl import load_workbook
from scipy.optimize import nnls

import common as K

AN2 = ("PFOA", "PFOS")


def rd(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def plan_list(target):
    """Table 6-1 of the plan, read from the PDF's text: rank, PWS id, system, county, population."""
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(target, K.FILES["iup"]), "-"], capture_output=True,
                         text=True, check=True).stdout
    out = []
    for line in txt.splitlines():
        m = re.match(r"^\s*(\d{1,2})\s+(\d{7})\s+(.+?)\s{2,}(\w+)\s+([\d,]+)\s+(\d+)\s*$", line)
        if m:
            out.append(dict(rank=int(m.group(1)), pws=m.group(2), name=m.group(3).strip(), county=m.group(4),
                            pop=int(m.group(5).replace(",", "")), points=int(m.group(6))))
    assert [x["rank"] for x in out] == list(range(1, 21)), [x["rank"] for x in out]
    return out


def inventory(target):
    ws = load_workbook(os.path.join(target, K.FILES["inventory"]), read_only=True)["Facilities"]
    rows = list(ws.iter_rows(values_only=True))
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:]]


ALL = re.compile(r"^\s*(all|both)\b", re.I)


def parse_sources(text, ep_wells):
    """The well numbers a sampler wrote; 'all' and 'both' mean every active well at the entry point; 'Plant' is the
    surface plant. None when the sampler wrote nothing."""
    t = (text or "").strip()
    if not t:
        return None
    if t.lower() == "plant":
        return sorted(ep_wells)
    if ALL.match(t):
        return sorted(ep_wells)
    return sorted({int(n) for n in re.findall(r"\d+", t)})


def load(target):
    """The samples the golden reads: the listed systems' routine and confirmation samples of 2024 and 2025, each at its
    latest report revision, with its sources in service and the wells' rated capacities."""
    plan = plan_list(target)
    listed = {p["pws"]: p for p in plan}
    inv = inventory(target)
    wells = collections.defaultdict(dict)        # (pws, ep) -> {well no: gpm} for active wells
    allw = collections.defaultdict(dict)         # (pws, ep) -> every well that ever feeds it
    for f in inv:
        if f["facility_type"] in ("Well", "Surface water treatment plant") and f["entry_point"]:
            no = 1 if f["facility_type"] != "Well" else int(f["facility_name"].split()[-1])
            allw[(f["pws_id"], f["entry_point"])][no] = int(f["rated_capacity_gpm"])
            if f["status"] == "Active":
                wells[(f["pws_id"], f["entry_point"])][no] = int(f["rated_capacity_gpm"])
    rec = {r["state_sample_no"]: r for r in rd(target, K.FILES["records"])}
    res = collections.defaultdict(dict)
    meta = {}
    for r in rd(target, K.FILES["results"]):
        key = r["state_sample_no"]
        rev = int(r["report_revision"])
        cur = res[key].get(r["analyte"])
        if cur is None or rev > cur[0]:
            res[key][r["analyte"]] = (rev, None if r["result_sign"] == "<" else float(r["result"]),
                                      float(r["reporting_limit"]))
        meta[key] = r
    out = []
    for key, m in meta.items():
        a = res[key]
        rc = rec[key]
        ep = (m["pws_id"], m["sample_point"])
        on = parse_sources(rc["sources_in_service"], wells[ep])
        out.append(dict(no=key, pws=m["pws_id"], ep=m["sample_point"], kind=m["sample_type"],
                        date=dt.date.fromisoformat(m["collected_date"]), on=on,
                        flow=int(rc["ep_flow_gpm"]) if rc["ep_flow_gpm"] else None,
                        res={k: (v[1], v[2]) for k, v in a.items()}, listed=m["pws_id"] in listed))
    return dict(plan=plan, listed=listed, inv=inv, wells=wells, allw=allw, samples=out)


def value(x, a, nd=0.5):
    v, rl = x["res"][a]
    return v if v is not None else nd * rl


def window(D, kinds=("RT", "CO"), years=K.WINDOW, missing="drop"):
    out = []
    for x in D["samples"]:
        if not x["listed"] or x["kind"] not in kinds or x["date"].year not in years:
            continue
        if x["on"] is None:
            if missing == "drop" or x["flow"] is None:
                continue
            x = dict(x, on=infer_on(D, x))
        out.append(x)
    return out


def infer_on(D, x):
    """The wells whose rated capacities add up to the entry-point flow at collection (a blank record)."""
    w = D["wells"][(x["pws"], x["ep"])]
    best = None
    nos = sorted(w)
    for k in range(1, len(nos) + 1):
        import itertools
        for combo in itertools.combinations(nos, k):
            d = abs(sum(w[n] for n in combo) - x["flow"])
            if best is None or d < best[0]:
                best = (d, list(combo))
    return best[1]


# ---------------------------------------------------------------------------------------------- the wells' own water
def unmix(D, rows, ep, a, nd=0.5, weights="rated", solver="ols"):
    w = D["wells"][ep]
    nos = sorted(w)
    A = np.zeros((len(rows), len(nos)))
    y = np.zeros(len(rows))
    for i, x in enumerate(rows):
        if weights == "rated":
            q = {n: w[n] for n in x["on"]}
        elif weights == "flow":
            q = {n: w[n] * x["flow"] / sum(w[k] for k in x["on"]) for n in x["on"]}
        else:
            q = {n: 1.0 for n in x["on"]}
        t = sum(q.values())
        for n in x["on"]:
            A[i, nos.index(n)] = q[n] / t
        y[i] = value(x, a, nd)
    if np.linalg.matrix_rank(A) < len(nos):
        return None
    sol = nnls(A, y)[0] if solver == "nnls" else np.linalg.lstsq(A, y, rcond=None)[0]
    return dict(zip(nos, (float(v) for v in sol)))


def chained(D, rows, ep, a, nd=0.5):
    """The same mass balance by subtraction: each well's level from the samples it ran alone, then each remaining
    well from the samples where every partner is already known, until none is left."""
    w = D["wells"][ep]
    known = {}
    for _ in range(len(w) + 1):
        for n in sorted(w):
            if n in known:
                continue
            ests = []
            for x in rows:
                if n not in x["on"] or any(k not in known for k in x["on"] if k != n):
                    continue
                t = sum(w[k] for k in x["on"])
                rest = sum(w[k] * known[k] for k in x["on"] if k != n)
                ests.append((value(x, a, nd) * t - rest) / w[n])
            if ests:
                known[n] = float(np.mean(ests))
    return known if len(known) == len(w) else None


def own_levels(D, nd=0.5, weights="rated", solver="ols", kinds=("RT", "CO"), years=K.WINDOW, missing="drop",
               method="lstsq", rows=None):
    """Each active well's own PFOA and PFOS, entry point by entry point."""
    rows = window(D, kinds, years, missing) if rows is None else rows
    by = collections.defaultdict(list)
    for x in rows:
        by[(x["pws"], x["ep"])].append(x)
    out = {}
    for ep, rr in by.items():
        ests = []
        for a in AN2:
            e = chained(D, rr, ep, a, nd) if method == "chained" else unmix(D, rr, ep, a, nd, weights, solver)
            ests.append(e)
        if any(e is None for e in ests):
            out[ep] = None
            continue
        out[ep] = {n: (ests[0][n], ests[1][n]) for n in ests[0]}
    return out


def over_from_levels(levels, rule="either"):
    over = collections.defaultdict(set)
    for (pws, ep), lv in levels.items():
        for n, (pfoa, pfos) in (lv or {}).items():
            hit = (pfoa > K.LINE or pfos > K.LINE) if rule == "either" else (pfoa + pfos > K.LINE)
            if hit:
                over[pws].add((ep, n))
    return over


# ---------------------------------------------------------------------------------------------- the shortcuts
def presence(D, agg=np.mean, weight=False):
    rows = window(D)
    num = collections.defaultdict(lambda: [0.0, 0.0])
    den = collections.defaultdict(float)
    vals = collections.defaultdict(list)
    for x in rows:
        w = D["wells"][(x["pws"], x["ep"])]
        t = sum(w[n] for n in x["on"])
        for n in x["on"]:
            sh = w[n] / t if weight else 1.0
            den[(x["pws"], x["ep"], n)] += sh
            for i, a in enumerate(AN2):
                num[(x["pws"], x["ep"], n)][i] += sh * value(x, a)
            vals[(x["pws"], x["ep"], n)].append([value(x, a) for a in AN2])
    over = collections.defaultdict(set)
    for k in den:
        lv = ([v / den[k] for v in num[k]] if agg is np.mean else
              [float(agg([v[i] for v in vals[k]])) for i in range(2)])
        if max(lv) > K.LINE:
            over[k[0]].add((k[1], k[2]))
    return over


def solo(D, fallback=True):
    rows = window(D)
    so = collections.defaultdict(list)
    pr = collections.defaultdict(list)
    for x in rows:
        for n in x["on"]:
            pr[(x["pws"], x["ep"], n)].append(x)
        if len(x["on"]) == 1:
            so[(x["pws"], x["ep"], x["on"][0])].append(x)
    over = collections.defaultdict(set)
    for (pws, ep), w in D["wells"].items():
        if pws not in D["listed"]:
            continue
        for n in w:
            xs = so[(pws, ep, n)] or (pr[(pws, ep, n)] if fallback else [])
            if xs and max(np.mean([value(x, a) for x in xs]) for a in AN2) > K.LINE:
                over[pws].add((ep, n))
    return over


def ep_route(D):
    rows = window(D)
    hit = {(x["pws"], x["ep"]) for x in rows if max(value(x, a, 0.0) for a in AN2) > K.LINE}
    over = collections.defaultdict(set)
    for (pws, ep), w in D["wells"].items():
        if (pws, ep) in hit:
            over[pws] |= {(ep, n) for n in w}
    return over


def pumping_at_exceedance(D):
    over = collections.defaultdict(set)
    for x in window(D):
        if max(value(x, a, 0.0) for a in AN2) > K.LINE:
            over[x["pws"]] |= {(x["ep"], n) for n in x["on"]}
    return over


def top_sample(D):
    best = {}
    for x in window(D):
        k = (x["pws"], x["ep"])
        v = max(value(x, a, 0.0) for a in AN2)
        if k not in best or v > best[k][0]:
            best[k] = (v, x)
    over = collections.defaultdict(set)
    for (pws, ep), (v, x) in best.items():
        if v > K.LINE:
            over[pws] |= {(ep, n) for n in x["on"]}
    return over


# ---------------------------------------------------------------------------------------------- grants and the walk
def grants(D, over):
    out = {}
    for p in D["plan"]:
        gpm = sum(D["wells"][(p["pws"], ep)][n] for ep, n in over.get(p["pws"], set()))
        out[p["pws"]] = min(K.CAP, K.DOLLARS_PER_GPM * gpm)
    return out


def walk(D, g, skip=False):
    left, funded, stop = K.FUND, [], None
    for p in D["plan"]:
        x = g[p["pws"]]
        if x == 0:
            continue
        if x > left:
            if stop is None:
                stop = p["pws"]
            if not skip:
                break
            continue
        left -= x
        funded.append(p["pws"])
    return dict(funded=funded, stop=stop, left=left)


def route(D, over):
    g = grants(D, over)
    return dict(grants=g, **walk(D, g))


def golden(D):
    lv = own_levels(D)
    over = over_from_levels(lv)
    return dict(levels=lv, over=over, **route(D, over))


# ---------------------------------------------------------------------------------------------- the asks
def meters_by_month(target, month):
    """Meter groups in service in a month: each meter's facilities."""
    groups = []
    for m in rd(target, K.FILES["meters"]):
        start = dt.date.fromisoformat(m["installed"])
        end = dt.date.fromisoformat(m["removed"]) if m["removed"] else None
        first = dt.date(2025, month, 1)
        last = dt.date(2025 + month // 12, month % 12 + 1, 1) - dt.timedelta(days=1)
        if start <= last and (end is None or end >= first):
            groups.append(set(m["facility_ids"].split(";")))
    return groups


def ask_a(D, target, mode="golden"):
    """2025 water pumped by the listed systems' wells, by county. mode: golden (each meter once), every_row,
    active_only (each meter once, active wells only), readings (each meter once, from the readings)."""
    county = {p["pws"]: p["county"] for p in D["plan"]}
    ftype = {f["facility_id"]: (f["facility_type"], f["status"]) for f in D["inv"]}
    rows = [r for r in rd(target, K.FILES["mor"]) if r["pws_id"] in county]
    out = collections.defaultdict(float)
    by_month = collections.defaultdict(list)
    for r in rows:
        if mode != "every_row_all" and ftype[r["facility_id"]][0] != "Well":
            continue
        if mode == "active_only" and ftype[r["facility_id"]][1] != "Active":
            continue
        by_month[(r["pws_id"], int(r["report_month"][5:]))].append(r)
    for (pws, mth), rr in by_month.items():
        if mode in ("every_row", "every_row_all"):
            for r in rr:
                out[county[pws]] += int(r["volume_gal"])
            continue
        groups = meters_by_month(target, mth)
        done = set()
        for r in rr:
            g = next((g for g in groups if r["facility_id"] in g and len(g) > 1), {r["facility_id"]})
            key = frozenset(g)
            if key in done:
                continue
            done.add(key)
            out[county[pws]] += (int(r["meter_end"]) - int(r["meter_start"])) if mode == "readings" else int(r["volume_gal"])
    return {c: round(v / 1e6, 1) for c, v in out.items()}


def ask_b(D, target, mode="golden"):
    """People who get their water from the listed systems' wells, by the county they live in. mode: golden (chains
    of full purchases in service, an id the register holds as inactive taken to the active system of that name and
    county), as_found (the chains, each id's register row as found), active_only (the chains, inactive ids left out),
    listed (the listed systems alone), one_step (buyers of a listed system), every_tie (chains through every
    connection)."""
    reg = {r["pws_id"]: r for r in rd(target, K.FILES["register"])}
    live = {(r["system_name"], r["county"]): r["pws_id"] for r in reg.values() if r["status"] == "Active"}
    con = rd(target, K.FILES["connections"])
    base = set(D["listed"])
    if mode == "listed":
        reach = base
    elif mode == "one_step":
        reach = base | {c["buyer_pws_id"] for c in con if c["seller_pws_id"] in base and
                        c["connection_type"] == "Full purchase" and not c["in_service_to"]}
    else:
        reach = set(base)
        while True:
            nxt = reach | {c["buyer_pws_id"] for c in con if c["seller_pws_id"] in reach and
                           (mode == "every_tie" or (c["connection_type"] == "Full purchase" and not c["in_service_to"]))}
            if nxt == reach:
                break
            reach = nxt
    if mode in ("golden", "every_tie"):
        reach = {live.get((reg[p]["system_name"], reg[p]["county"]), p) if reg[p]["status"] == "Inactive" else p
                 for p in reach}
    elif mode == "active_only":
        reach = {p for p in reach if reg[p]["status"] == "Active"}
    out = collections.defaultdict(int)
    for p in reach:
        out[reg[p]["county"]] += int(reg[p]["population_served"])
    return dict(out)
