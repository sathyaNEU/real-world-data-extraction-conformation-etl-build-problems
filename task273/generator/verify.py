"""The independent verifier: every graded figure recomputed from the cut pack by code that shares nothing with the
analysis (its own readers, its own stop-the-world arithmetic on a work clock, its own seed), then compared with
generator/figures.json.

    python3 task273/generator/verify.py [task folder]"""
import bisect
import csv
import datetime as dt
import json
import math
import os
import re
import sys

import numpy as np

FILES = {
    "jmeter": "loadtest_jmeter_results_2026-11-10_to_12.jtl", "k6": "loadtest_k6_results_2026-11-16_to_19.csv",
    "gc": "perf_gc_log_export_2026-11-10_to_19.log", "events": "perf_cluster_pod_events_2026-11.csv",
    "register": "public_api_endpoint_register.xlsx", "edge": "edge_requests_hourly_2026-01.csv",
    "synthetic": "edge_uptime_monitors.yaml", "changelog": "developer_portal_changelog_2026.html",
    "employers": "crm_employer_accounts_2026-11-01.csv", "subs": "billing_subscription_events_2026.csv",
    "legacy": "legacy_billing_credits_2026-01_to_04.csv", "credits": "billing_credits_2026-05-01_to_11-19.json",
    "incidents": "status_page_incidents_2025-12_to_2026-11.xlsx",
}
E0 = dt.datetime(1970, 1, 1)


def ts(s):
    s = s.rstrip("Z")
    base, _, frac = s.partition(".")
    return (dt.datetime.fromisoformat(base) - E0).total_seconds() + (float("0." + frac) if frac else 0.0)


def rnd(x):
    return int(math.floor(x + 0.5))


def endpoints(T):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(T, FILES["register"]), read_only=True)
    ep = {}
    for r in list(wb["Endpoints"].iter_rows(values_only=True))[1:]:
        ep[r[0]] = (r[1] + " " + r[2], r[3], set(x.strip() for x in r[4].split(",")))
    pods = {r[0]: int(r[4]) for r in list(wb["Services"].iter_rows(values_only=True))[1:]}
    return ep, pods


def load_requests(T):
    req = {}
    for r in csv.DictReader(open(os.path.join(T, FILES["jmeter"]), encoding="utf-8")):
        s = int(r["timeStamp"]) / 1000.0
        req.setdefault(r["label"][:4], []).append((s, s + int(r["elapsed"]) / 1000.0, r["servedBy"]))
    for r in csv.DictReader(open(os.path.join(T, FILES["k6"]), encoding="utf-8")):
        tg = dict(kv.split("=") for kv in r["extra_tags"].split("&"))
        e = ts(r["timestamp"])
        req.setdefault(tg["endpoint"], []).append((e - float(r["metric_value"]) / 1000.0, e, tg["served_by"]))
    out = {}
    for code, lst in req.items():
        lst.sort()
        cut = [0] + [i for i in range(1, len(lst)) if lst[i][0] - lst[i - 1][0] > 600] + [len(lst)]
        runs = [lst[cut[i]:cut[i + 1]] for i in range(len(cut) - 1)]
        full = [x for x in runs if x[-1][0] - x[0][0] > 770]
        out[code] = (full[-1], len(runs))
    return out


def load_pauses(T):
    js = {}
    for r in csv.DictReader(open(os.path.join(T, FILES["events"]), encoding="utf-8")):
        m = re.search(r"process running for ([0-9.]+)\)", r["message"])
        if m:
            js.setdefault(r["pod"], []).append(ts(r["time"]) - float(m.group(1)))
    out = {}
    for line in open(os.path.join(T, FILES["gc"]), encoding="utf-8"):
        f = line.split(" ", 3)
        if len(f) < 4 or "Pause " not in f[3]:
            continue
        deco = f[2][1:f[2].index("]")]
        dur = float(re.search(r"([0-9.]+)ms\s*$", f[3]).group(1)) / 1000.0
        if re.fullmatch(r"[0-9.]+s", deco):
            starts = sorted(x for x in js[f[1]] if x <= ts(f[0]))
            end = starts[-1] + float(deco[:-1])
        else:
            end = ts(deco[:23]) + 5 * 3600.0
        out.setdefault(f[1], []).append((end - dur, end))
    return {p: sorted(v) for p, v in out.items()}


class WorkClock:
    """A pod's time with its pauses taken out: work done by wall time x, and the wall time work w is done."""

    def __init__(self, pauses):
        merged = []
        for a, b in pauses:
            if merged and a <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], b)
            else:
                merged.append([a, b])
        self.a = np.array([x[0] for x in merged])
        self.b = np.array([x[1] for x in merged])
        d = self.b - self.a
        self.before = np.concatenate([[0.0], np.cumsum(d)])          # paused time before pause k
        self.wa = self.a - self.before[:-1]                            # work clock at pause k's start
        self.d = d

    def work(self, x):
        k = np.searchsorted(self.a, x, side="right")                   # pauses started by x
        inside = (k > 0) & (x < self.b[np.maximum(k - 1, 0)])
        w = x - self.before[k]
        w[inside] = self.wa[k[inside] - 1]
        return w

    def wall(self, w):
        k = np.searchsorted(self.wa, w, side="left")                  # pauses whose start work precedes w
        return w + self.before[k]


def call(T, n=600_000, seed=91827):
    ep, podn = endpoints(T)
    req = load_requests(T)
    pauses = load_pauses(T)
    p99, recorded, stopped = {}, {}, []
    for code in sorted(ep):
        run, nruns = req[code]
        if nruns > 1:
            stopped.append(code)
        t0 = run[0][0] + 180.0
        t1 = run[0][0] + 780.0
        meas = [x for x in run if t0 <= x[0] < t1]
        pods = sorted({x[2] for x in run})
        assert len(pods) == podn[ep[code][1]]
        clocks = {p: WorkClock([q for q in pauses.get(p, []) if q[1] > t0 - 60 and q[0] < t1 + 60]) for p in pods}
        lat = np.array([x[1] - x[0] for x in meas])
        recorded[code] = float(np.percentile(lat, 99)) * 1000.0
        svc = np.empty(len(meas))
        for p in pods:
            k = np.array([x[2] == p for x in meas])
            st = np.array([x[0] for x in meas])[k]
            en = np.array([x[1] for x in meas])[k]
            svc[k] = clocks[p].work(en) - clocks[p].work(st)
        svc = np.maximum(svc, 0.0005)
        r = np.random.default_rng([seed, int(code[2:])])
        t = r.uniform(t0, t1, n)
        pod = r.integers(len(pods), size=n)
        s = r.choice(svc, n)
        resp = np.empty(n)
        for i, p in enumerate(pods):
            k = pod == i
            resp[k] = clocks[p].wall(clocks[p].work(t[k]) + s[k]) - t[k]
        p99[code] = float(np.percentile(resp, 99)) * 1000.0
    return p99, recorded, stopped


def ask_a(T):
    import yaml
    ep, _ = endpoints(T)
    by_route = {v[0]: k for k, v in ep.items()}
    page = open(os.path.join(T, FILES["changelog"]), encoding="utf-8").read()
    ren = {}
    for m in re.finditer(r"GET (\S+) is now GET (\S+?),? [^<]*?From 10:00 ET on (\d+) January 2026", page):
        ren["GET " + m.group(2).rstrip(".,")] = ("GET " + m.group(1), (dt.datetime(2026, 1, int(m.group(3)), 15) -
                                                                         E0).total_seconds())
    y = yaml.safe_load(open(os.path.join(T, FILES["synthetic"]), encoding="utf-8"))
    syn = {k: 0 for k in ep}
    for c in y["monitors"]:
        if c["created"] > dt.date(2026, 1, 1):
            continue
        every = c.get("frequency_seconds", y["defaults"]["frequency_seconds"])
        locs = c.get("locations", y["defaults"]["locations"])
        for st in c["steps"]:
            syn[by_route[st.split("#")[0].strip()]] += 3600 // every * len(locs)
    counts = {}
    for r in csv.DictReader(open(os.path.join(T, FILES["edge"]), encoding="utf-8")):
        counts.setdefault(r["route"], {})[ts(r["hour_start_utc"])] = int(r["requests"])
    peak = {}
    for code, (route, svc, plans) in ep.items():
        series = dict(counts[route])
        if route in ren:
            old, sw = ren[route]
            series = {h: v for h, v in series.items() if h >= sw}
            series.update({h: v for h, v in counts[old].items() if h < sw})
        peak[code] = max(v - syn[code] for v in series.values())
    # the accounts on 1 January: walk every 2026 event back from the CRM's 1 November state
    state = {}
    for r in csv.DictReader(open(os.path.join(T, FILES["employers"]), encoding="utf-8")):
        state[r["employer_id"]] = r["plan"]
    nov = dict(state)
    evs = list(csv.DictReader(open(os.path.join(T, FILES["subs"]), encoding="utf-8")))
    evs.sort(key=lambda e: (e["effective_date"], e["event_id"]))
    for e in reversed(evs):
        i = e["employer_id"]
        if e["event"] == "new_subscription":
            state.pop(i, None)
        elif e["event"] == "cancellation":
            state[i] = e["plan_before"]
        elif e["event"] == "plan_change" and i in state:
            state[i] = e["plan_before"]
    out = {}
    for code, (route, svc, plans) in ep.items():
        num = sum(1 for p in nov.values() if p in plans)
        den = sum(1 for p in state.values() if p in plans)
        out[code] = rnd(peak[code] * num / den)
    return out


def ask_b(T):
    import openpyxl
    ep, _ = endpoints(T)
    by_route = {v[0]: k for k, v in ep.items()}
    page = open(os.path.join(T, FILES["changelog"]), encoding="utf-8").read()
    for m in re.finditer(r"GET (/\S+) is now GET (/\S+?)[,.]? ", page):
        by_route["GET " + m.group(1)] = by_route["GET " + m.group(2)]
    wb = openpyxl.load_workbook(os.path.join(T, FILES["incidents"]), read_only=True)
    inc = {}
    for r in list(wb["Incidents"].iter_rows(values_only=True))[1:]:
        day = (r[1] - dt.timedelta(hours=5)).date()
        inc[r[0]] = by_route.get(r[4]) if dt.date(2026, 1, 1) <= day <= dt.date(2026, 10, 31) else None
    cents = {k: 0 for k in ep}
    legacy = set()
    for r in csv.DictReader(open(os.path.join(T, FILES["legacy"]), encoding="utf-8")):
        if r["status"] == "void":
            continue
        legacy.add((r["account"], r["incident"]))
        if inc[r["incident"]]:
            cents[inc[r["incident"]]] += int(r["amount"])
    for x in json.load(open(os.path.join(T, FILES["credits"]), encoding="utf-8"))["credits"]:
        if x["type"] == "credit" and (x["account"], x["incident"]) in legacy:
            continue
        if inc[x["incident"]]:
            cents[inc[x["incident"]]] += int(round(float(x["amount"]) * 100))
    out = {k: rnd(v / 100.0) for k, v in cents.items()}
    return out, sum(out.values())


def run(task):
    T = os.path.join(task, "target")
    fig = json.load(open(os.path.join(task, "generator", "figures.json")))
    bad = []
    p99, recorded, stopped = call(T)
    fix = sorted(c for c, v in p99.items() if v > 800.0)
    if fix != fig["call"]["fix"]:
        bad.append(("call", fix, fig["call"]["fix"]))
    near = min(abs(v - 800.0) for v in p99.values())
    if near < 60:
        bad.append(("margin", near))
    for c, v in recorded.items():
        if int(round(v)) != fig["recorded_ms"][c]:
            bad.append(("recorded", c, v, fig["recorded_ms"][c]))
    if stopped != fig["runs"]["stopped_early"]:
        bad.append(("stopped", stopped))
    a = ask_a(T)
    for c, v in a.items():
        if v != fig["ask_a"][c]:
            bad.append(("ask_a", c, v, fig["ask_a"][c]))
    b, total = ask_b(T)
    for c, v in b.items():
        if v != fig["ask_b"][c]:
            bad.append(("ask_b", c, v, fig["ask_b"][c]))
    if total != fig["ask_b_total"]:
        bad.append(("ask_b_total", total, fig["ask_b_total"]))
    print("verify: call %s (nearest the line %.0f ms), Ask A 24 figures, Ask B 24 figures and the total: %s" % (
        ", ".join(fix), near, "PASS" if not bad else "FAIL %s" % bad[:6]))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
