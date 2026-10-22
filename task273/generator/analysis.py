"""Every route's figures, computed from the cut pack: the call (each endpoint's 99th percentile at the forecast peak, by
the golden and by every route a competent analyst might take) and the two supplementary questions."""
import datetime as dt
import math

import numpy as np

import common as K
import models as M
import pack as P

N_MC = 2_000_000
EST = dt.timedelta(hours=-5)


def half_up(x):
    return int(math.floor(x + 0.5))


# ------------------------------------------------------------------------------------------------ the call
def call_inputs(target):
    """Each endpoint's run of record, measurement window and its service's pods with their pauses."""
    ep, svc = P.register(target)
    rs = P.runs(P.requests(target))
    pauses = P.gc_pauses(target)
    out = {}
    for c in K.CODES:
        run = P.run_of_record(rs[c])
        t0, t1 = run["t0"] + K.WARMUP_S, run["t0"] + K.RUN_S
        pods = sorted(set(run["pod"]))
        assert len(pods) == svc[ep[c]["service"]]["pods"], c
        win = [[(a, b) for a, b in pauses.get(p, []) if b > t0 - 60.0 and a < t1 + 60.0] for p in pods]
        out[c] = dict(run=run, t0=t0, t1=t1, pods=pods, pauses=win, n_runs=len(rs[c]))
    return out


def routes(target, n_mc=N_MC, inputs=None):
    """code -> every route's figure (milliseconds, unless named otherwise)."""
    X = call_inputs(target) if inputs is None else inputs
    out = {}
    for c in K.CODES:
        x = X[c]
        run, t0, t1, pods, Pw = x["run"], x["t0"], x["t1"], x["pods"], x["pauses"]
        idx = {p: i for i, p in enumerate(pods)}
        m = (run["start"] >= t0) & (run["start"] < t1)
        st, en = run["start"][m], run["end"][m]
        lat = en - st
        pod_i = np.array([idx[p] for p in run["pod"][m]])
        ov = M.overlap_rows(list(zip(pod_i, st, en)), [[(a, b, "") for a, b in w] for w in Pw])
        svc_t = np.maximum(lat - ov, 0.0005)
        touched = ov > 0
        threads = len(set(run["thread"]))
        rate = len(st) / (t1 - t0)
        interval = threads / rate
        share = np.mean([sum(min(b, t1) - max(a, t0) for a, b in w if b > t0 and a < t1) / (t1 - t0) for w in Pw])
        longest = max([b - a for w in Pw for a, b in w if b > t0 and a < t1], default=0.0) * 1000.0
        pooled = [sorted({ab for w in Pw for ab in w})]
        merged = []
        for a, b in pooled[0]:
            if merged and a <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], b))
            else:
                merged.append((a, b))
        seed = K.SEED * 100 + int(c[2:])
        out[c] = dict(
            raw=float(np.percentile(lat, K.PCT)) * 1000.0,
            raw_warm=float(np.percentile(run["end"] - run["start"], K.PCT)) * 1000.0,
            drop=float(np.percentile(lat[~touched], K.PCT)) * 1000.0,
            hdr=M.backfill_p99(lat, interval),
            hdr_gc=M.backfill_p99(lat, interval, touched),
            hdr_gc_pods=M.backfill_p99(lat, interval * len(pods), touched),
            lw=float(np.percentile(np.repeat(lat, np.maximum(1, np.rint(lat / interval)).astype(int)), K.PCT)) * 1000.0,
            golden=M.golden_p99(svc_t, Pw, t0, t1, seed, n=n_mc),
            golden_alt=M.golden_p99(svc_t, Pw, t0, t1, seed + 7919, n=max(n_mc // 2, 1)),
            golden_untouched=M.golden_p99(lat[~touched], Pw, t0, t1, seed + 31, n=n_mc),
            golden_rawsvc=M.golden_p99(lat, Pw, t0, t1, seed + 57, n=max(n_mc // 2, 1)),
            pooled=M.golden_p99(svc_t, [merged], t0, t1, seed + 73, n=max(n_mc // 2, 1)),
            share=share * 100.0, longest=longest, n=int(len(st)), rate=rate, pods=len(pods), threads=threads,
            touched=int(touched.sum()), runs=x["n_runs"])
    return out


GOLDEN_FAMILY = ("golden", "golden_alt", "golden_untouched")


def verdicts(R, key="golden"):
    return [c for c in K.CODES if R[c][key] > K.SLA_MS]


# ------------------------------------------------------------------------------------------------ Ask A
def route_codes(target, old_names=True):
    ep, _ = P.register(target)
    rc = {v["route"]: c for c, v in ep.items()}
    if old_names:
        for new, (old, ts) in P.renames(target).items():
            rc[old] = rc[new]
    return rc


def synthetic_per_hour(target, before=dt.date(2026, 1, 1)):
    rc = route_codes(target, old_names=False)
    out = {c: 0 for c in K.CODES}
    for ck in P.synthetic(target):
        if ck["created"] <= before:
            for s in ck["steps"]:
                out[rc[s]] += (3600 // ck["every"]) * len(ck["locations"])
    return out


def january_series(target, ep=None, mode="golden"):
    """Each endpoint's requests by clock hour of January as the edge counted them on the route that served it:
    mode golden, the old path before the rename and the new path from it; current, the current path only; merged,
    both paths in every hour."""
    if ep is None:
        ep, _ = P.register(target)
    E = P.edge(target)
    ren = P.renames(target)
    out = {}
    for c in K.CODES:
        route = ep[c]["route"]
        cur = dict(E.get(route, {}))
        if route in ren and mode != "current":
            old, ts = ren[route]
            if mode == "golden":
                s = {h: v for h, v in E[old].items() if h < ts}
                s.update({h: v for h, v in cur.items() if h >= ts})
            else:
                s = dict(cur)
                for h, v in E[old].items():
                    s[h] = s.get(h, 0) + v
            cur = s
        out[c] = cur
    return out


def busiest(series, minus=None):
    """(requests, hour) of the busiest clock hour, after taking each hour's synthetic requests off."""
    out = {}
    for c, s in series.items():
        k = 0 if minus is None else minus[c]
        h = max(s, key=lambda t: (s[t] - k, -t))
        out[c] = (s[h] - k, h)
    return out


def january_states(target, events_only=False):
    """Each account's (active, plan) on 1 January 2026: its state on 1 November with every 2026 event undone, latest
    first."""
    emp = P.employers(target)
    state = {e: (True, r["plan"]) for e, r in emp.items()}
    ev = P.subscription_events(target)
    for e in sorted(ev, key=lambda x: (x["effective_date"], x["event_id"]), reverse=True):
        eid = e["employer_id"]
        act, plan = state.get(eid, (False, None))
        if e["event"] == "new_subscription":
            state[eid] = (False, None)
        elif e["event"] == "cancellation":
            state[eid] = (True, e["plan_before"])
        elif e["event"] == "plan_change":
            state[eid] = (act, e["plan_before"])
    return state


def growth(target, ep=None):
    if ep is None:
        ep, _ = P.register(target)
    emp = P.employers(target)
    jan = january_states(target)
    out = {}
    for c in K.CODES:
        pl = set(ep[c]["plans"])
        num = sum(1 for r in emp.values() if r["plan"] in pl)
        den = sum(1 for act, p in jan.values() if act and p in pl)
        out[c] = (num, den)
    return out


def ask_a(target):
    ep, _ = P.register(target)
    syn = synthetic_per_hour(target)
    peaks = busiest(january_series(target, ep), syn)
    g = growth(target, ep)
    out = {}
    for c in K.CODES:
        n, h = peaks[c]
        num, den = g[c]
        x = n * num / den
        out[c] = dict(peak=n, hour=h, num=num, den=den, synthetic=syn[c], forecast=half_up(x), exact=x)
    return out


# ------------------------------------------------------------------------------------------------ Ask B
def ask_b(target):
    rc = route_codes(target)
    inc = P.incidents(target)
    leg = P.legacy_credits(target)
    new = P.new_credits(target)

    def code_in_window(key):
        i = inc[key]
        d = (i["start"] + EST).date()
        return rc.get(i["comp"]) if K.WINDOW_FROM <= d <= K.WINDOW_TO else None

    cents = {c: 0 for c in K.CODES}
    issued = {(x["account"], x["incident"]) for x in leg if x["status"] == "issued"}
    for x in leg:
        c = code_in_window(x["incident"])
        if c and x["status"] == "issued":
            cents[c] += int(x["amount"])
    carried = 0
    for x in new:
        if x["type"] == "credit" and (x["account"], x["incident"]) in issued:
            carried += 1
            continue
        c = code_in_window(x["incident"])
        if c:
            cents[c] += int(round(float(x["amount"]) * 100))
    return {c: dict(cents=v, dollars=half_up(v / 100.0)) for c, v in cents.items()}, carried


def golden_only(inputs, n=400_000, seed_off=0, svc_from="golden"):
    """Each endpoint's rebuilt 99th percentile alone (for the fork and separation checks), and the share of arrivals
    answered within 800 ms."""
    out = {}
    for c in K.CODES:
        x = inputs[c]
        run, t0, t1, pods, Pw = x["run"], x["t0"], x["t1"], x["pods"], x["pauses"]
        idx = {p: i for i, p in enumerate(pods)}
        m = (run["start"] >= t0) & (run["start"] < t1)
        st, en = run["start"][m], run["end"][m]
        lat = en - st
        pod_i = np.array([idx[p] for p in run["pod"][m]])
        ov = M.overlap_rows(list(zip(pod_i, st, en)), [[(a, b, "") for a, b in w] for w in Pw])
        svc_t = np.maximum(lat - ov, 0.0005)
        r = np.random.default_rng(K.SEED * 100 + int(c[2:]) + seed_off)
        t = r.uniform(t0, t1, n)
        pod = r.integers(len(Pw), size=n)
        s = r.choice(svc_t, n)
        resp = np.empty(n)
        for p, w in enumerate(Pw):
            k = pod == p
            a = np.array([q[0] for q in w])
            b = np.array([q[1] for q in w])
            resp[k] = M.finish_vec(t[k], s[k], a, b) - t[k]
        out[c] = dict(p99=float(np.percentile(resp, K.PCT)) * 1000.0, within=float(np.mean(resp <= K.SLA_MS / 1000.0)))
    return out
