"""The estimators of each endpoint's 99th-percentile response time at the forecast peak, run on the request rows and the
pause windows of a run of record (both in seconds from the run's start).

The golden: customers arrive independently of the platform's state, so a request customers send lands at any moment
of the measured window with equal chance, on any pod with equal chance (the balancer turns them in rotation), and
takes its own service time plus whatever pause time it meets. Each recorded request's own service time is its response
time less the pause time inside it; the distribution customers would see is those service times run against every
moment of the window on every pod."""
import numpy as np

import common as K

N_MC = 2_000_000


def overlap_rows(rows, P):
    """Pause time inside each recorded request (start to finish) on its own pod."""
    out = np.zeros(len(rows))
    A = [np.array([w[0] for w in p]) for p in P]
    B = [np.array([w[1] for w in p]) for p in P]
    for i, (pod, t, f) in enumerate(rows):
        a, b = A[pod], B[pod]
        j = np.searchsorted(b, t, side="right")
        tot = 0.0
        while j < len(a) and a[j] < f:
            tot += min(b[j], f) - max(a[j], t)
            j += 1
        out[i] = tot
    return out


def finish_vec(t, s, a, b):
    """Vectorised stop-the-world finish times on one pod (pauses a..b sorted, non-overlapping)."""
    cur = t.copy()
    left = s.copy()
    done = np.zeros(len(t), bool)
    i = np.searchsorted(b, cur, side="right")
    for _ in range(64):
        live = ~done
        if not live.any():
            break
        ii = i[live]
        past = ii >= len(a)
        idx = np.where(live)[0]
        # no pause left: finish
        fin = idx[past]
        cur[fin] = cur[fin] + left[fin]
        done[fin] = True
        idx = idx[~past]
        ii = ii[~past]
        if len(idx) == 0:
            break
        aa, bb = a[ii], b[ii]
        inside = cur[idx] >= aa
        # inside a pause: jump to its end
        j = idx[inside]
        cur[j] = bb[inside]
        i[j] = ii[inside] + 1
        k = idx[~inside]
        ak, bk, ik = aa[~inside], bb[~inside], ii[~inside]
        fits = cur[k] + left[k] <= ak
        f = k[fits]
        cur[f] = cur[f] + left[f]
        done[f] = True
        g = k[~fits]
        left[g] = left[g] - (ak[~fits] - cur[g])
        cur[g] = bk[~fits]
        i[g] = ik[~fits] + 1
    return cur


def golden_p99(svc_times, P, t0, t1, seed, n=N_MC):
    """Customers' 99th percentile (ms): arrivals uniform over [t0, t1), a pod at random, a recorded service time."""
    r = np.random.default_rng(seed)
    t = r.uniform(t0, t1, n)
    pod = r.integers(len(P), size=n)
    s = r.choice(svc_times, n)
    lat = np.empty(n)
    for p, w in enumerate(P):
        m = pod == p
        a = np.array([x[0] for x in w])
        b = np.array([x[1] for x in w])
        lat[m] = finish_vec(t[m], s[m], a, b) - t[m]
    return float(np.percentile(lat, K.PCT)) * 1000.0


def backfill_p99(lat, interval, mask=None):
    """HdrHistogram's correction for coordinated omission: every recorded response time longer than the expected
    interval adds the samples the client would have sent meanwhile (the response time less one interval, less two, and
    so on). mask limits it to the rows given."""
    parts = [lat]
    sel = lat if mask is None else lat[mask]
    sel = sel[sel > interval]
    k = 1
    while len(sel):
        x = sel - k * interval
        x = x[x > 0]
        if not len(x):
            break
        parts.append(x)
        sel = sel[sel - k * interval > 0]
        k += 1
    return float(np.percentile(np.concatenate(parts), K.PCT)) * 1000.0


def evaluate(run, eps, code, seed):
    """Every route's figure for one endpoint's run of record."""
    rows = run["rows"]
    P = run["pauses"]
    t0, t1 = K.WARMUP_S, K.RUN_S
    meas = [x for x in rows if t0 <= x[2] < t1]
    lat = np.array([x[3] - x[2] for x in meas])
    ov = overlap_rows([(x[1], x[2], x[3]) for x in meas], P)
    svc = lat - ov
    touched = ov > 0
    threads = eps[code]["threads"]
    rate = len(meas) / (t1 - t0)
    interval = threads / rate                      # the interval per client at the achieved rate
    pods = len(P)
    share = np.mean([sum(min(b, t1) - max(a, t0) for a, b, _ in w if b > t0 and a < t1) / (t1 - t0) for w in P])
    longest = max([b - a for w in P for a, b, _ in w if b > t0 and a < t1], default=0.0) * 1000.0
    Pw = [[(a, b) for a, b, _ in w] for w in P]
    R = dict(
        raw=float(np.percentile(lat, K.PCT)) * 1000.0,
        raw_warm=float(np.percentile([x[3] - x[2] for x in rows], K.PCT)) * 1000.0,
        drop=float(np.percentile(lat[~touched], K.PCT)) * 1000.0,
        hdr=backfill_p99(lat, interval),
        hdr_gc=backfill_p99(lat, interval, touched),
        hdr_gc_pods=backfill_p99(lat, interval * pods, touched),
        lw=float(np.percentile(np.repeat(lat, np.maximum(1, np.rint(lat / interval)).astype(int)), K.PCT)) * 1000.0,
        golden=golden_p99(svc, Pw, t0, t1, seed),
        golden_alt=golden_p99(svc, Pw, t0, t1, seed + 7919, n=1_000_000),
        golden_untouched=golden_p99(lat[~touched], Pw, t0, t1, seed),
        share=share * 100.0, longest=longest, n=len(meas), rate=rate, pods=pods, threads=threads,
    )
    return R
