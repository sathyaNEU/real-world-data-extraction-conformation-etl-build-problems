"""The simulated world behind task268: every hour of 2026 for each service (the load balancer's request and 5xx
counts), and for December the traces the tracing store kept. The store's sampler sits at the edge: each edge service
keeps a share of its requests that it resets at the top of every hour from its previous hour's traffic, and a kept
request's whole trace is kept with it, the calls it made to the internal services included. The truth (every
request's latency) never ships; the pack carries the kept spans and the counts."""
import datetime as dt

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

import common as K

HOURS_YEAR = 365 * 24
DEC0 = (dt.datetime(2026, 12, 1) - dt.datetime(2026, 1, 1)).days * 24        # first December hour of the year
H = K.REVIEW_HOURS


def _diurnal(peaks):
    h = np.full(24, 0.22)
    for ph, w, a in peaks:
        x = np.arange(24)
        h += a * np.exp(-0.5 * (np.minimum(np.abs(x - ph), 24 - np.abs(x - ph)) / w) ** 2)
    return h / h.max()


MONTH = np.array([0.62, 0.60, 0.66, 0.72, 0.76, 0.86, 0.98, 1.0, 0.82, 0.74, 0.70, 1.0])


def _calendar():
    hrs = np.arange(HOURS_YEAR)
    doy = hrs // 24
    dates = [dt.date(2026, 1, 1) + dt.timedelta(days=int(d)) for d in range(365)]
    month = np.array([dates[d].month for d in doy])
    dow = np.array([dates[d].weekday() for d in doy])
    return hrs % 24, doy, month, dow


def edge_rate(svc):
    """Expected requests an hour for an edge service over 2026 (no draw)."""
    hod, doy, month, dow = _calendar()
    peak, peaks, camp, extra = K.TRAFFIC[svc]
    lam = peak * _diurnal(peaks)[hod] * MONTH[month - 1] * np.where(dow >= 5, 0.85, 1.0)
    dec_day = doy - DEC0 // 24
    dec = month == 12
    for d, f in K.SEASON.items():
        lam[dec & (dec_day == d)] *= f
    if camp:
        for d, h0, h1, f in K.CAMPAIGNS:
            lam[DEC0 + d * 24 + h0:DEC0 + d * 24 + h1] *= f
    for d, h0, h1, f in extra:
        lam[DEC0 + d * 24 + h0:DEC0 + d * 24 + h1] *= f
    return lam


def _load(n, svc):
    rho = np.minimum(n / K.CAP[svc], K.RHO_MAX)
    return rho


def _g(rho, a):
    return 1 + a * rho / (1 - rho)


def callers(svc):
    return [(e, op, p) for e, (_, calls) in K.GRAPH.items() for c, op, p in calls if c == svc]


def medians():
    """Each operation's latency median at zero load, set so its December slow share at the expected traffic sits at
    its target (internal operations analytically; an edge service's own work by simulation of the whole request)."""
    lam = {s: edge_rate(s)[DEC0:DEC0 + H] for s in K.EDGE}
    load = {}
    for s in K.EDGE:
        load[s] = _load(lam[s], s)
    n_int = {c: sum(lam[e] * p * (1 + (K.ERR[c] if c in K.RETRY else 0)) for e, op, p in callers(c))
             for c in K.INTERNAL}
    for c in K.INTERNAL:
        load[c] = _load(n_int[c], c)
    base = {}
    for (svc, op), (m, a, sig, tgt) in K.LAT.items():
        if svc in K.INTERNAL:
            if tgt is None:
                base[(svc, op)] = m
                continue
            g = _g(load[svc], a)
            w = sum(lam[e] * p for e, o, p in callers(svc) if o == op)
            thr = K.THRESHOLD[svc]

            def gap(lm):
                pslow = (1 - K.ERR[svc]) * (1 - norm.cdf((np.log(thr) - lm - np.log(g)) / sig))
                return 100 * (w * pslow).sum() / w.sum() - tgt
            base[(svc, op)] = float(np.exp(brentq(gap, np.log(thr) - 9, np.log(thr) + 3)))
    rng = np.random.default_rng(90210)
    R = 1500
    for s in K.EDGE:
        m, a, sig, tgt = K.LAT[(s, "own")]
        if tgt is None:
            base[(s, "own")] = m
            continue
        z = rng.standard_normal((H, R))
        extra = _call_time_mc(s, base, load, rng, R)

        def gap(lm):
            own = np.exp(lm + np.log(_g(load[s], a))[:, None] + sig * z)
            tot = _compose(s, own, extra)
            p = (tot > K.THRESHOLD[s]).mean(axis=1) * (1 - K.ERR[s])
            return 100 * (lam[s] * p).sum() / lam[s].sum() - tgt
        base[(s, "own")] = float(np.exp(brentq(gap, np.log(K.THRESHOLD[s]) - 9, np.log(K.THRESHOLD[s]) + 3)))
    return base


def _call_time_mc(s, base, load, rng, R):
    """Simulated client-side durations (ms) of the calls an edge request makes, hour by hour, R draws each."""
    if s not in K.GRAPH:
        return None
    mode, calls = K.GRAPH[s]
    out = []
    for c, op, p in calls:
        m, a, sig, _ = K.LAT[(c, op)]
        med = base[(c, op)] * _g(load[c], a)
        d = np.exp(np.log(med)[:, None] + sig * rng.standard_normal((H, R))) + 2.0
        made = rng.random((H, R)) < p
        out.append(np.where(made, d, 0.0))
    return mode, out


def _compose(s, own, extra):
    if extra is None:
        return own
    mode, calls = extra
    if mode == "par":
        return np.maximum(own, np.max(np.stack(calls), axis=0)) + 2.0
    return own + np.sum(np.stack(calls), axis=0) + 1.5


class World:
    def __init__(self, seed=K.SEED, base=None):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.base = base or medians()
        self.N = {}            # requests each service handled, every hour of 2026
        self.E = {}            # of which 5xx
        self.build_edge_counts()
        self.build_december()
        self.build_internal_counts()

    # ---------------------------------------------------------------- edge counts
    def build_edge_counts(self):
        r = self.rng
        for svc in K.EDGE:
            lam = edge_rate(svc)
            wob = np.repeat(r.normal(1.0, 0.04, 365), 24)          # day-to-day wobble outside December
            hod, doy, month, dow = _calendar()
            lam = lam * np.where(month == 12, 1.0, wob)
            self.N[svc] = r.poisson(lam).astype(np.int64)

    # ---------------------------------------------------------------- December: the sampler and the kept traces
    def build_december(self):
        """Kept traces for the last hour of 30 November (its spans that started in December are exported) and every
        December hour. Each kept span: trace, id, parent, service, operation, kind, start (s from 1 December 00:00
        UTC), duration (ms), HTTP status."""
        r = self.rng
        sp = {k: [] for k in ("trace", "sid", "parent", "svc", "op", "kind", "t0", "ms", "code")}
        self.sp = sp
        self.K_edge = {s: np.zeros(H, dtype=np.int64) for s in K.EDGE}       # kept edge requests by hour
        # December requests the internal services handled, built from every edge request's calls: kept + not kept
        self.Nint = {c: np.zeros(H, dtype=np.int64) for c in K.INTERNAL}
        self.Eint = {c: np.zeros(H, dtype=np.int64) for c in K.INTERNAL}
        self.Edec = {s: np.zeros(H, dtype=np.int64) for s in K.EDGE}
        self.slow_true = {s: 0.0 for s in K.SVC}                            # expected slow requests, all of them
        self.q = {}
        load_e = {s: _load(self.N[s][DEC0 - 1:DEC0 + H], s) for s in K.EDGE}   # index 0 is 30 November 23:00
        n_calls = {}
        for c in K.INTERNAL:
            n_calls[c] = sum(self.N[e][DEC0 - 1:DEC0 + H] * p for e, op, p in callers(c))
        load_i = {c: _load(n_calls[c], c) for c in K.INTERNAL}
        self.load = {**load_e, **load_i}
        tid = sid = 0
        for s in K.EDGE:
            n = self.N[s][DEC0 - 1:DEC0 + H]
            prev = self.N[s][DEC0 - 2:DEC0 + H - 1]
            q = np.minimum(1.0, K.TARGET_PER_HOUR / np.maximum(prev, 1))
            self.q[s] = q[1:]
            k = r.binomial(n, q)
            self.K_edge[s][:] = k[1:]
            m_own, a_own, sig_own, _ = K.LAT[(s, "own")]
            med_own = self.base[(s, "own")] * _g(load_e[s], a_own)
            mode, calls = K.GRAPH.get(s, (None, []))
            for hh in range(H + 1):
                h = hh - 1                                     # -1 is 30 November 23:00
                kk, nn = int(k[hh]), int(n[hh])
                # requests not kept still make their calls (the internal services' counts) and fail at the same rate
                if h >= 0:
                    self.Edec[s][h] += r.binomial(nn - kk, K.ERR[s])
                t_start = h * 3600 + np.sort(r.uniform(0.05, 3599.95, kk))
                own = np.exp(np.log(med_own[hh]) + sig_own * r.standard_normal(kk))
                err = r.random(kk) < K.ERR[s]
                own = np.where(err, r.uniform(4, 40, kk), own)
                end_calls = np.zeros(kk)
                cursor = t_start + own * 0.55 / 1000 if mode == "seq" else t_start + r.uniform(0.002, 0.006, kk)
                root_ids = np.arange(sid, sid + kk)
                sid += kk
                child = []                                      # (trace i, client start, client ms, server rows)
                for c, op, p in calls:
                    made = (r.random(kk) < p) & ~err
                    # the requests not kept make the call at the same share
                    if h >= 0:
                        mu = r.binomial(nn - kk, p * (1 - K.ERR[s])) if nn > kk else 0
                    m_c, a_c, sig_c, _ = K.LAT[(c, op)]
                    med_c = self.base[(c, op)] * _g(load_i[c][hh], a_c)
                    pslow = (1 - K.ERR[c]) * (1 - norm.cdf((np.log(K.THRESHOLD[c]) - np.log(med_c)) / sig_c))
                    retries_unkept = 0
                    if h >= 0 and mu:
                        e_un = r.binomial(mu, K.ERR[c])
                        self.Eint[c][h] += e_un
                        if c in K.RETRY:
                            retries_unkept = e_un
                            self.Eint[c][h] += r.binomial(e_un, K.ERR[c])
                        self.Nint[c][h] += mu + retries_unkept
                        self.slow_true[c] += (mu + retries_unkept) * pslow
                    idx = np.nonzero(made)[0]
                    for i in idx:
                        tries = 1
                        t_call = cursor[i] if mode == "seq" else t_start[i] + float(r.uniform(0.002, 0.006))
                        total = 0.0
                        while True:
                            code = 500 if r.random() < K.ERR[c] else 200
                            ms = float(r.uniform(6, 60)) if code == 500 else float(
                                np.exp(np.log(med_c) + sig_c * r.standard_normal()))
                            net = float(np.exp(np.log(1.8) + 0.4 * r.standard_normal()))
                            child.append((i, t_call, ms + net, c, op, code, ms))
                            if h >= 0 or t_call + 0.0005 >= 0:
                                ch = int((t_call + 0.0005) // 3600)
                                if 0 <= ch < H:
                                    self.Nint[c][ch] += 1
                                    self.Eint[c][ch] += code == 500
                            total += (ms + net) / 1000 + 0.0004
                            t_call += (ms + net) / 1000 + 0.0004
                            if code == 500 and c in K.RETRY and tries == 1:
                                tries += 1
                                continue
                            break
                        if mode == "seq":
                            cursor[i] = t_call + float(r.uniform(0.0003, 0.0015))
                        end_calls[i] = max(end_calls[i], t_call)
                # the edge request's own span covers its calls
                if mode == "seq":
                    end = np.where(end_calls > 0, np.maximum(end_calls, cursor) + own * 0.45 / 1000,
                                   t_start + own / 1000)
                elif mode == "par":
                    end = np.maximum(t_start + own / 1000, end_calls) + 0.002
                else:
                    end = t_start + own / 1000
                for j in range(kk):
                    code = 500 if err[j] else 200
                    sp["trace"].append(tid + j); sp["sid"].append(int(root_ids[j])); sp["parent"].append(-1)
                    sp["svc"].append(s); sp["op"].append("own"); sp["kind"].append("SERVER")
                    sp["t0"].append(float(t_start[j])); sp["ms"].append(float((end[j] - t_start[j]) * 1000))
                    sp["code"].append(code)
                    if h >= 0:
                        self.Edec[s][h] += code == 500
                for (i, t_call, cms, c, op, code, ms) in child:
                    cid, srv = sid, sid + 1
                    sid += 2
                    sp["trace"].append(tid + i); sp["sid"].append(cid); sp["parent"].append(int(root_ids[i]))
                    sp["svc"].append(s); sp["op"].append(c + ":" + op); sp["kind"].append("CLIENT")
                    sp["t0"].append(float(t_call)); sp["ms"].append(float(cms)); sp["code"].append(code)
                    sp["trace"].append(tid + i); sp["sid"].append(srv); sp["parent"].append(cid)
                    sp["svc"].append(c); sp["op"].append(op); sp["kind"].append("SERVER")
                    sp["t0"].append(float(t_call + 0.0005)); sp["ms"].append(float(ms)); sp["code"].append(code)
                tid += kk
                # the edge service's expected slow requests this hour (every request, kept or not)
                if h >= 0:
                    self._edge_truth(s, hh, nn, med_own[hh], sig_own)
        for k_ in sp:
            sp[k_] = np.array(sp[k_])
        # the internal services' realised kept calls enter their truth at their own operation's slow probability
        for c in K.INTERNAL:
            for e, op, p in callers(c):
                m_c, a_c, sig_c, _ = K.LAT[(c, op)]
                sel = (sp["svc"] == c) & (sp["op"] == op) & (sp["kind"] == "SERVER")
                t = sp["t0"][sel]
                hh = np.clip((t // 3600).astype(int) + 1, 0, H)
                med_c = self.base[(c, op)] * _g(load_i[c][hh], a_c)
                ps = (1 - K.ERR[c]) * (1 - norm.cdf((np.log(K.THRESHOLD[c]) - np.log(med_c)) / sig_c))
                inwin = (t >= 0) & (t < H * 3600)
                self.slow_true[c] += float(ps[inwin].sum())

    def _edge_truth(self, s, hh, nn, med_own, sig_own):
        """Expected slow requests of an edge service in one hour, by simulation of the whole request."""
        if not hasattr(self, "_mc"):
            self._mc = np.random.default_rng(self.seed + 999)
        R = 400
        own = np.exp(np.log(med_own) + sig_own * self._mc.standard_normal(R))
        mode, calls = K.GRAPH.get(s, (None, []))
        parts = []
        for c, op, p in calls:
            m_c, a_c, sig_c, _ = K.LAT[(c, op)]
            med_c = self.base[(c, op)] * _g(self.load[c][hh], a_c)
            d = np.exp(np.log(med_c) + sig_c * self._mc.standard_normal(R)) + 2.0
            parts.append(np.where(self._mc.random(R) < p, d, 0.0))
        if not parts:
            tot = own
        elif mode == "par":
            tot = np.maximum(own, np.max(np.stack(parts), axis=0)) + 2.0
        else:
            tot = own + np.sum(np.stack(parts), axis=0) + 1.5
        self.slow_true[s] += nn * (1 - K.ERR[s]) * float((tot > K.THRESHOLD[s]).mean())

    # ---------------------------------------------------------------- internal counts for the year
    def build_internal_counts(self):
        r = np.random.default_rng(self.seed + 17)
        for c in K.INTERNAL:
            n = np.zeros(HOURS_YEAR, dtype=np.int64)
            for e, op, p in callers(c):
                n += r.binomial(self.N[e], p)
            if c in K.RETRY:
                n += r.binomial(n, K.ERR[c])
            n[DEC0:DEC0 + H] = self.Nint[c]
            self.N[c] = n
            ev = r.binomial(n, K.ERR[c])
            ev[DEC0:DEC0 + H] = self.Eint[c]
            self.E[c] = ev
        for s in K.EDGE:
            ev = r.binomial(self.N[s], K.ERR[s])
            ev[DEC0:DEC0 + H] = self.Edec[s]
            self.E[s] = ev

    # ---------------------------------------------------------------- truths the pack cannot show
    def true_sli(self, svc):
        return 100 * self.slow_true[svc] / self.N[svc][DEC0:DEC0 + H].sum()
