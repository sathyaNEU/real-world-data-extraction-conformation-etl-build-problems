"""Independent verifier for task501. Reads only the shipped bundle and figures.json, on its own code path (no generator
module is imported), and recomputes the call, every graded flow and both asks.

    python3 task501/generator/verify.py <target> <figures.json>"""
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import Counter, defaultdict
from zoneinfo import ZoneInfo

import numpy as np

LON = ZoneInfo("Europe/London")
UTC = dt.timezone.utc


def find(target, pattern):
    hits = [f for f in os.listdir(target) if re.search(pattern, f)]
    assert len(hits) == 1, (pattern, hits)
    return os.path.join(target, hits[0])


def pdf(target, pattern):
    from pypdf import PdfReader
    t = " ".join(p.extract_text() for p in PdfReader(find(target, pattern)).pages)
    return re.sub(r"\s+", " ", t)


def sheet(path, name):
    import openpyxl
    rows = list(openpyxl.load_workbook(path, data_only=True)[name].iter_rows(values_only=True))
    hdr = rows[2]
    return [dict(zip(hdr, r)) for r in rows[3:]]


def local_utc(naive, fold=0):
    return naive.replace(tzinfo=LON, fold=fold).astimezone(UTC).replace(tzinfo=None)


class Net:
    def __init__(self, reg):
        self.mains = {r["Main"]: (r["From"], r["To"]) for r in sheet(reg, "Mains")}
        self.valve_main = {}
        self.normal = {}
        for r in sheet(reg, "Valves"):
            self.valve_main[r["Valve"]] = r["Main"]
            self.normal[r["Valve"]] = r["Normal position"] == "Open"
        self.inlet = {r["DMA"]: r["Inlet junction"] for r in sheet(reg, "Districts")}
        self.root = "Copt Hill works outlet"

    def live(self, state):
        down = {self.valve_main[v] for v, o in state.items() if not o}
        return frozenset(m for m in self.mains if m not in down)

    def tree(self, live):
        """Junction -> list of mains from the works, or None when two routes run in parallel or a district is unfed."""
        nbr = defaultdict(list)
        for m in sorted(live):
            a, b = self.mains[m]
            nbr[a].append((m, b))
            nbr[b].append((m, a))
        seen = {self.root: []}
        stack = [self.root]
        edges = set()
        while stack:
            u = stack.pop()
            for m, v in nbr[u]:
                if m in edges:
                    continue
                edges.add(m)
                if v in seen:
                    return None
                seen[v] = seen[u] + [m]
                stack.append(v)
        if any(j not in seen for j in self.inlet.values()):
            return None
        return seen


def main(argv):
    target, figpath = argv[0], argv[1]
    figs = json.load(open(figpath, encoding="utf-8"))
    ok = True

    def say(label, cond, detail=""):
        nonlocal ok
        ok &= bool(cond)
        print("%s  verify: %-54s %s" % ("PASS" if cond else "FAIL", label, detail))

    std = pdf(target, r"^nos12_.*\.pdf$")
    plan = pdf(target, r"outage_plan.*\.pdf$")
    say("standard read back (control: clause 4.2)", "highest hourly flow it carried in the twelve months" in std)
    say("plan read back (control: works dates)", "out of service from 15 March to 15 September 2027" in plan)
    net = Net(find(target, r"^trunk_mains_register.*\.xlsx$"))
    say("register read back (control: TM107 is the Ferrars Lane main)", "TM107" in net.mains and len(net.inlet) == 18)
    tab = plan[plan.index("Step Valve"):plan.index("are supplied from Coldharbour")]
    plan_ops = re.findall(r"(V\d{5})\b.*?\b(Open|Shut)\b", tab)
    say("plan valve table read", len(plan_ops) == 6, "%d operations" % len(plan_ops))

    # district inflows, UTC hours
    seen = set()
    flow = defaultdict(dict)
    with open(find(target, r"^dma_inlet_flows_.*\.csv$"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = tuple(r.values())
            if key in seen:
                continue
            seen.add(key)
            if r["flow_l_s"] != "":
                flow[r["reading_utc"]][r["dma"]] = float(r["flow_l_s"])
    hours = sorted(flow)
    dmas = sorted(net.inlet)
    full = [h for h in hours if len(flow[h]) == len(dmas)]
    say("district meters read back (control: 18 districts, a year of hours)", len(hours) == 8760, "%d hours" % len(hours))

    # valve state through the year from the log
    changes = []
    with open(find(target, r"valve_log.*\.csv$"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["valve_no"] in net.valve_main and r["action"] in ("OPEN", "CLOSE"):
                t = local_utc(dt.datetime.strptime(r["date"] + " " + r["time"], "%d/%m/%Y %H:%M"))
                changes.append((t, r["valve_no"], r["action"] == "OPEN"))
    changes.sort()
    state = dict(net.normal)
    normal_live = net.live(state)
    k = 0
    cur = normal_live
    live_at = {}
    for h in hours:
        t0 = dt.datetime.strptime(h, "%Y-%m-%d %H:%M")
        counts = Counter()
        for mnt in range(0, 60, 5):
            t = t0 + dt.timedelta(minutes=mnt + 2)
            while k < len(changes) and changes[k][0] <= t:
                state[changes[k][1]] = changes[k][2]
                k += 1
            lv = net.live(state)
            if net.tree(lv) is not None:
                cur = lv
            counts[cur] += 1
        live_at[h] = counts.most_common(1)[0][0]

    plan_state = dict(net.normal)
    for v, o in plan_ops:
        plan_state[v] = o == "Open"
    plan_live = net.live(plan_state)

    def carry(live, h):
        tr = net.tree(live)
        out = defaultdict(float)
        for d in dmas:
            for m in tr[net.inlet[d]]:
                out[m] += flow[h][d]
        return out

    ref = defaultdict(float)
    for h in full:
        for m, q in carry(live_at[h], h).items():
            ref[m] = max(ref[m], q)

    def local_date(h):
        return dt.datetime.strptime(h, "%Y-%m-%d %H:%M").replace(tzinfo=UTC).astimezone(LON).date()
    rep = [h for h in full if dt.date(2026, 3, 15) <= local_date(h) <= dt.date(2026, 9, 15)]
    peak, normal = defaultdict(float), defaultdict(float)
    rises = {m: True for m in net.mains}
    for h in rep:
        p, n0 = carry(plan_live, h), carry(normal_live, h)
        for m in net.mains:
            peak[m] = max(peak[m], p.get(m, 0.0))
            normal[m] = max(normal[m], n0.get(m, 0.0))
            if not p.get(m, 0.0) > n0.get(m, 0.0) + 1e-9:
                rises[m] = False
    listed = sorted(m for m, v in rises.items() if v)
    flush = sorted(m for m in listed if peak[m] > ref[m])
    say("the mains the relining loads", listed == sorted(figs["mains"]), ", ".join(listed))
    say("the call: mains to flush", flush == sorted(figs["flush"]), ", ".join(flush))
    for m in listed:
        f = figs["mains"][m]
        say("%s works peak and reference" % m, int(np.floor(peak[m] + 0.5)) == f["highest_hourly_flow_during_works_l_s"]
            and int(np.floor(ref[m] + 0.5)) == f["highest_hourly_flow_carried_nov2025_oct2026_l_s"],
            "%.2f / %.2f" % (peak[m], ref[m]))

    # ask A: the flushing job sheets
    rows, seen = [], set()
    with open(find(target, r"flushing_job_sheets.*\.csv$"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = tuple(r.values())
            if key not in seen:
                seen.add(key)
                rows.append(r)
    for r in rows:
        n = r["night_of"]
        r["night"] = dt.date.fromisoformat(n) if "-" in n else dt.datetime.strptime(n, "%d/%m/%Y").date()
        a, b = (dt.datetime.strptime(r[x], "%H:%M") for x in ("start", "finish"))
        mins = (b - a).total_seconds() / 60.0 % 1440
        r["cap"] = float(r["gauge_flow_l_s"]) * mins * 60 / 1000.0
        r["v"] = float(r["volume_m3"])
    groups = defaultdict(list)
    for r in rows:
        groups[(r["night_of"], r["crew"])].append(r)
    water = {}
    for g in groups.values():
        runs = any(r["v"] > 1.2 * r["cap"] for r in g[1:])
        prev = 0.0
        for r in g:
            water[id(r)] = r["v"] - prev if runs else r["v"]
            prev = r["v"]
    sec = {}
    for r in rows:
        key = (r["night_of"], r["section_ref"])
        w, L, dn, yr = sec.get(key, (0.0, float(r["section_length_m"]), int(r["main_dn_mm"]), r["night"].year))
        sec[key] = (w + water[id(r)], L, dn, yr)
    agg = defaultdict(lambda: [0.0, 0.0])
    for w, L, dn, yr in sec.values():
        agg[(dn, yr)][0] += w
        agg[(dn, yr)][1] += L
    for (dn, yr), (w, L) in sorted(agg.items()):
        v = "%.1f" % (np.floor(w / L * 1000 + 0.5) / 10.0)
        say("flushing water %d mm %d" % (dn, yr), v == figs["flushing_water_m3_per_100m"]["%d mm %d" % (dn, yr)], v)

    # ask B: non-household water by supplying district
    import openpyxl
    rows = list(openpyxl.load_workbook(find(target, r"^nonhousehold_supply_points.*\.xlsx$"), data_only=True)[
        "Supply points"].iter_rows(values_only=True))
    hdr = rows[2]
    sp = [dict(zip(hdr, r)) for r in rows[3:]]
    vol = defaultdict(float)
    with open(find(target, r"nonhousehold_monthly_consumption.*\.csv$"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if "2025-11" <= r["month"] <= "2026-10":
                vol[r["spid"]] += float(r["consumption_m3"])
    use = defaultdict(dict)
    last = {}
    with open(find(target, r"^amr_large_users.*\.csv$"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            t = dt.datetime.strptime(r["read_start_local"], "%d/%m/%Y %H:%M")
            fold = 1 if last.get(r["logger_id"]) == t else 0
            last[r["logger_id"]] = t
            use[r["logger_id"]][local_utc(t, fold).strftime("%Y-%m-%d %H:%M")] = float(r["volume_m3"]) / 3.6
    home = {}
    for s in sp:
        home[s["SPID"]] = s["DMA"]
        lg = s["AMR logger"]
        if not lg:
            continue
        rec = s["DMA"]
        over = sum(1 for h in full if use[lg].get(h, 0.0) > flow[h][rec] + 1e-9)
        if over:
            q = np.array([use[lg].get(h, np.nan) for h in hours])
            best, bc = None, -2
            for d in dmas:
                if d == rec:
                    continue
                x = np.array([flow[h].get(d, np.nan) for h in hours])
                dq, dx = np.diff(q), np.diff(x)
                m = ~(np.isnan(dq) | np.isnan(dx))
                cc = np.corrcoef(dq[m], dx[m])[0, 1]
                if cc > bc:
                    best, bc = d, cc
            home[s["SPID"]] = best
    tot = defaultdict(float)
    for s, v in vol.items():
        tot[home.get(s)] += v
    for key, want in figs["nonhousehold_water_ml"].items():
        d = key.split()[0]
        v = "%.1f" % (np.floor(tot[d] / 100.0 + 0.5) / 10.0)
        say("non-household water %s" % key, v == want, v)
    print("VERIFY   %s" % ("all figures reproduced from the bundle" if ok else "MISMATCH"))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
