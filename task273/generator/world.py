"""The world behind task273: each endpoint's November load test at its forecast peak volume, with the closed-loop test
clients (each sends its next request only after the last returns and the script's pacing sleep), the endpoint's service
pods behind a round-robin balancer, and every pod's stop-the-world garbage-collection pauses.

A request that reaches a pod at time t with an intrinsic service time s finishes once it has run for s outside the
pod's pauses: a pause that begins while it is in flight holds it, and one that is under way when it arrives holds it
until the pause ends. Nothing queues behind a pause beyond that (the pods run every request in its own thread).

Times inside a run are seconds from the run's start; the schedule puts each run on the wall clock (UTC)."""
import bisect
import datetime as dt

import numpy as np

import common as K

# per collector: pause families, each (events per minute per pod at the forecast load, median ms, log sd)
GC_FAMILIES = {
    "parallel": [("young", (14, 26), (22, 48), 0.35), ("full", (0.45, 1.5), (900, 2300), 0.30)],
    "g1": [("young", (12, 26), (18, 70), 0.40), ("mixed", (0.8, 2.5), (110, 260), 0.35)],
    "zgc": [("young", (4, 8), (0.05, 0.4), 0.30)],
}
WARMUP_TAU = 40.0                     # seconds: the JIT warm-up's decay at the start of each run


def service_gc(r):
    """Each service's pause families: the rates and median lengths drawn inside its collector's ranges."""
    out = {}
    for svc, (gc, pods) in K.SERVICES.items():
        fams = []
        for name, rate, med, sd in GC_FAMILIES[gc]:
            fams.append(dict(name=name, rate=r.uniform(*rate), med=r.uniform(*med), sd=sd))
        out[svc] = dict(gc=gc, pods=pods, fams=fams)
    return out


def endpoint_params(r):
    """Each endpoint's intrinsic service time (lognormal, ms) and, for the heavy endpoints, the share and size of the
    requests that are slow on their own (a large report, a wide search, a long document)."""
    out = {}
    for code in K.CODES:
        p = dict(med=r.uniform(60, 230), sd=r.uniform(0.32, 0.50), q=0.0, hmed=0.0, hsd=0.30)
        if K.KIND[code] == "heavy":
            p.update(q=r.uniform(0.004, 0.0085), hmed=r.uniform(900, 1500))
        p["threads"] = int(r.integers(2, 6))
        p["think"] = float(r.uniform(0.08, 0.35))   # the script's pacing sleep between a response and the next request
        out[code] = p
    return out


def pauses(r, gcs, svc, t0, t1):
    """Every pod's pauses between t0 and t1 (seconds from the run's start), each (start, end, family), sorted."""
    out = []
    for pod in range(gcs[svc]["pods"]):
        ev = []
        for f in gcs[svc]["fams"]:
            t = t0 + r.exponential(60.0 / f["rate"]) * r.uniform(0, 1)
            while t < t1:
                d = float(np.exp(np.log(f["med"]) + f["sd"] * r.standard_normal())) / 1000.0
                ev.append((t, d, f["name"]))
                t += r.exponential(60.0 / f["rate"])
        ev.sort()
        merged = []
        for a, d, n in ev:                      # a pause cannot start inside another on the same pod
            if merged and a < merged[-1][1]:
                a = merged[-1][1] + 0.001
            merged.append((a, a + d, n))
        out.append(merged)
    return out


def add_g1_cycles(r, P, t0, t1):
    """G1's concurrent marking cycles: each holds the pod twice, briefly (Remark, then Cleanup), around a concurrent
    phase that stops nothing. Returns the pauses with the two short holds added, and the cycles."""
    cycles = []
    out = []
    for pod, w in enumerate(P):
        rate = r.uniform(0.5, 1.4) / 60.0
        t = t0 + r.exponential(1 / rate) * r.uniform(0, 1)
        extra = []
        while t < t1:
            conc = r.uniform(0.12, 0.45)
            rem = float(np.exp(np.log(r.uniform(6, 22)) + 0.3 * r.standard_normal())) / 1000.0
            cln = float(np.exp(np.log(r.uniform(0.3, 1.6)) + 0.3 * r.standard_normal())) / 1000.0
            a1 = t + conc
            extra.append((a1, a1 + rem, "remark"))
            a2 = a1 + rem + r.uniform(0.002, 0.020)
            extra.append((a2, a2 + cln, "cleanup"))
            cycles.append((pod, t, conc, a2 + cln))
            t += r.exponential(1 / rate)
        ev = sorted(list(w) + extra)
        merged = []
        for a, b, n in ev:
            d = b - a
            if merged and a < merged[-1][1]:
                a = merged[-1][1] + 0.001
            merged.append((a, a + d, n))
        out.append(merged)
    return out, cycles


class PodClock:
    """Stop-the-world arithmetic for one pod's pauses."""

    def __init__(self, windows):
        self.a = [w[0] for w in windows]
        self.b = [w[1] for w in windows]

    def finish(self, t, s):
        """When a request arriving at t with service time s finishes."""
        i = bisect.bisect_right(self.b, t)      # first pause ending after t
        cur, left = t, s
        while True:
            if i >= len(self.a):
                return cur + left
            a, b = self.a[i], self.b[i]
            if cur >= a:                        # arrived inside the pause
                cur = b
                i += 1
                continue
            if cur + left <= a:
                return cur + left
            left -= a - cur
            cur = b
            i += 1


def service_time(r, p):
    if p["q"] > 0 and r.random() < p["q"]:
        return float(np.exp(np.log(p["hmed"]) + p["hsd"] * r.standard_normal())) / 1000.0
    return float(np.exp(np.log(p["med"]) + p["sd"] * r.standard_normal())) / 1000.0


def warm(t):
    """The JIT's warm-up: service times run slow at the start of a run and settle within the warm-up."""
    return 1.0 + 0.8 * np.exp(-max(t, 0.0) / WARMUP_TAU)


def closed_loop(r, p, clocks, run_s):
    """The test clients: each thread sends, waits for the response and the script's pacing sleep, sends again; the
    balancer hands each new request to the next pod in turn. Returns rows (thread, pod, start, finish, service time)."""
    n_pods = len(clocks)
    nxt = [r.uniform(0, 0.25) for _ in range(p["threads"])]
    rr = int(r.integers(n_pods))
    rows = []
    while True:
        th = int(np.argmin(nxt))
        t = nxt[th]
        if t >= run_s:
            break
        pod = rr % n_pods
        rr += 1
        s = service_time(r, p) * warm(t)
        f = clocks[pod].finish(t, s)
        rows.append((th, pod, t, f, s))
        nxt[th] = f + p["think"] + r.uniform(0.0005, 0.004)  # the pacing sleep and the client's own turnaround
    return rows


# the campaign: JMeter until Thursday 12 November, k6 from Monday 16 November
JMETER_DAYS = [dt.date(2026, 11, 10), dt.date(2026, 11, 11), dt.date(2026, 11, 12)]
K6_DAYS = [dt.date(2026, 11, 16), dt.date(2026, 11, 17), dt.date(2026, 11, 18), dt.date(2026, 11, 19)]
ABORTED = {"EP05": 342.0, "EP13": 97.0, "EP20": 251.0}     # endpoints with an aborted first run: seconds it ran
UPTIME_SERVICES = {"tax-forms", "banking", "accounting-sync"}  # older base image: GC log decorated with uptime


def schedule(seed):
    """Each endpoint's run of record (and its aborted run, where there was one) on the wall clock, and the tool."""
    r = np.random.default_rng([seed, 0, 7])
    order = list(K.CODES)
    r.shuffle(order)
    n_j = 10
    days = [(d, "jmeter") for d in JMETER_DAYS] + [(d, "k6") for d in K6_DAYS]
    slots = {d: [] for d, _ in days}
    for i, code in enumerate(order):
        d, tool = days[i % 3] if i < n_j else days[3 + (i - n_j) % 4]
        slots[d].append((code, tool))
    sched = {}
    for d, lst in slots.items():
        t = dt.datetime.combine(d, dt.time(14, 0)) + dt.timedelta(minutes=int(r.integers(5, 40)))
        for code, tool in lst:
            item = dict(tool=tool)
            if code in ABORTED:
                item["aborted_start"] = t
                t += dt.timedelta(seconds=ABORTED[code] + int(r.integers(600, 1500)))
            item["start"] = t + dt.timedelta(milliseconds=int(r.integers(0, 1000)))
            sched[code] = item
            t = item["start"] + dt.timedelta(seconds=K.RUN_S + int(r.integers(900, 3000)))
    return sched


def pod_names(seed):
    r = np.random.default_rng([seed, 0, 11])
    al = list("bcdfghjklmnpqrstvwxz2456789")
    hx = list("0123456789abcdef")
    out = {}
    for svc, (gc, n) in K.SERVICES.items():
        rs = "".join(r.choice(hx, 10 if svc in UPTIME_SERVICES else 9))
        out[svc] = ["%s-%s-%s" % (svc, rs, "".join(r.choice(al, 5))) for _ in range(n)]
    return out


def world(seed=K.SEED):
    r = np.random.default_rng(seed)
    gcs = service_gc(r)
    eps = endpoint_params(r)
    sched = schedule(seed)
    runs = {}
    for code in K.CODES:
        rr = np.random.default_rng([seed, int(code[2:]), 1])
        svc = K.SERVICE[code]
        P = pauses(rr, gcs, svc, -30.0, K.RUN_S + 30.0)
        cycles = []
        if gcs[svc]["gc"] == "g1":
            P, cycles = add_g1_cycles(np.random.default_rng([seed, int(code[2:]), 2]), P, -30.0, K.RUN_S + 30.0)
        rows = closed_loop(rr, eps[code], [PodClock(w) for w in P], K.RUN_S)
        run = dict(pauses=P, cycles=cycles, rows=rows)
        if code in ABORTED:
            ra = np.random.default_rng([seed, int(code[2:]), 3])
            Pa = pauses(ra, gcs, svc, -30.0, ABORTED[code] + 30.0)
            ca = []
            if gcs[svc]["gc"] == "g1":
                Pa, ca = add_g1_cycles(np.random.default_rng([seed, int(code[2:]), 4]), Pa, -30.0, ABORTED[code] + 30.0)
            run["aborted"] = dict(pauses=Pa, cycles=ca,
                                  rows=closed_loop(ra, eps[code], [PodClock(w) for w in Pa], ABORTED[code]))
        runs[code] = run
    return dict(seed=seed, gcs=gcs, eps=eps, runs=runs, sched=sched, pods=pod_names(seed))
