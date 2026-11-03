"""The ask-layer ceiling on the cut pack: the cracker (lands the call, runs the hygiene battery, executes every
filed rule) and the mirror (stops at the procedure's per-area route), each ask figure scored against the golden."""
import csv
import datetime as dt
import hashlib
import json
import os

import openpyxl

import golden as G

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")


def lu_oct(meter_area, local_month=True, per_user_span=False):
    reads = G.amr(T)
    areas, _, _ = G.register(T)
    out = {c: 0.0 for c in areas}
    lo, hi = (dt.datetime(2026, 9, 30, 23), dt.datetime(2026, 11, 1)) if local_month else (dt.datetime(2026, 10, 1), dt.datetime(2026, 11, 1))
    for serial, area in meter_area.items():
        for t0, t1, d in G.advances(reads.get(serial, [])):
            if lo <= t0 and t1 <= hi:
                out[area] += d
    return {c: int(round(v)) for c, v in out.items()}


def account_meters():
    areas, _, _ = G.register(T)
    old = {a["prev"]: c for c, a in areas.items() if a["prev"]}
    return {a["serial"]: old.get(a["area"], a["area"]) for a in G.accounts(T)}


def occupied(order="effective", class_from="latest"):
    areas, _, _ = G.register(T)
    old = {a["prev"]: c for c, a in areas.items() if a["prev"]}
    ev = {}
    with open(os.path.join(T, G.F["billing"])) as f:
        for e in csv.DictReader(f):
            eff = dt.datetime.strptime(e["effective_date"], "%d/%m/%Y").date()
            if order == "effective" and eff > dt.date(2026, 10, 31):
                continue
            ev.setdefault(e["property_ref"], []).append((eff, e["posted"], e))
    out = {c: 0 for c in areas}
    for pref, lst in ev.items():
        lst.sort(key=(lambda x: (x[0], x[1])) if order == "effective" else (lambda x: x[1]))
        last = lst[-1][2]
        st = {}
        for _, _, e in lst:
            if e["event"] == "OCC":
                st[e["account_no"]] = True
            elif e["event"] == "VAC":
                st[e["account_no"]] = False
        cls = last["property_class"] if class_from == "latest" else lst[0][2]["property_class"]
        if any(st.values()) and cls == "HH":
            out[old.get(last["area_code"], last["area_code"])] += 1
    return out


def repairs(date_field="task"):
    amap = {}
    with open(os.path.join(T, G.F["assets"])) as f:
        for r in csv.DictReader(f):
            amap[r["asset_id"]] = r["dma"]
    wb = openpyxl.load_workbook(os.path.join(T, G.F["works"]), read_only=True)
    jobs = {}
    for job, task, ttype, asset, raised, done, closed in wb.active.iter_rows(min_row=2, values_only=True):
        if ttype != "REPAIR MAIN":
            continue
        d = done if date_field == "task" else closed
        if d is None or not (dt.datetime(2026, 8, 1) <= d < dt.datetime(2026, 11, 1)):
            continue
        a = str(asset)
        if a.startswith("W26-"):
            continue          # no asset on the row: the careful route cannot place it in an area
        jobs[job] = amap[a if a.startswith("WM-") else "WM-%06d" % int(a.split("/")[0])]
    areas, _, _ = G.register(T)
    out = {c: 0 for c in areas}
    for j, a in jobs.items():
        out[a] += 1
    return out


def score(resp, gold):
    hit = tot = 0
    for k in gold:
        for c in gold[k]:
            tot += 1
            hit += int(resp[k][c] == gold[k][c])
    return hit, tot


def main():
    res = G.compute(T)
    gold = {"lu": {c: int(round(v)) for c, v in res["lu_oct"].items()}, "occ": res["occupied"], "rep": res["repairs"]}
    cracker = {"lu": lu_oct(account_meters()), "occ": occupied("effective", "latest"), "rep": repairs("task")}
    mirror = {"lu": lu_oct(account_meters(), local_month=False), "occ": occupied("posted", "latest"), "rep": repairs("closed")}
    hc, tot = score(cracker, gold)
    hm, _ = score(mirror, gold)
    Lc, Lm = hc / tot, hm / tot
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Lm
    pair = (C + S) / 2
    per_ask = {k: (score({k: cracker[k]}, {k: gold[k]}), score({k: mirror[k]}, {k: gold[k]})) for k in gold}
    digest = hashlib.md5(open(os.path.join(os.path.dirname(HERE), "target", G.F["flows"]), "rb").read()).hexdigest()[:12]
    out = dict(cracker_keep=round(100 * Lc, 1), mirror_keep=round(100 * Lm, 1), cracker_score=round(C, 1),
               mirror_score=round(S, 1), pair=round(pair, 1), per_ask=per_ask, pack=digest)
    print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    main()
