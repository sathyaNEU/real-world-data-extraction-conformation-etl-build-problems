"""The simulated world for task249: every browser of the twelve editions, simulated day by day from 1 January to
31 December 2028 (local days, Europe/Berlin).  A browser's visits follow its reader type.  On WebKit the analytics
identifier and the paywall meter live in script-written storage that is dropped once seven days pass without a page
view (elapsed time, so the clock change counts); the meter also restarts each calendar month; a reader past the free
count meets the registration wall and may register, signed in from the next session.  Print subscribers activated
their digital access before 2028 and are signed in throughout.  The fourth quarter is kept session by session."""
import datetime as dt
import numpy as np
import params as P

DAYS = [P.HIST_START + dt.timedelta(days=i) for i in range((P.END - P.HIST_START).days + 1)]
NDAY = len(DAYS)
MONTH = np.array([(d.year - 2028) * 12 + d.month - 1 for d in DAYS])
WALL_FIRST = DAYS.index(P.WALL_START)
Q4_FIRST = DAYS.index(P.Q4_START)
DST_ON, DST_OFF = DAYS.index(dt.date(2028, 3, 26)), DAYS.index(dt.date(2028, 10, 29))
OFF = np.array([2.0 if DST_ON <= k < DST_OFF else 1.0 for k in range(NDAY)])   # hours ahead of UTC


def tod(rng, n):
    """time of day in hours: morning, lunch and evening peaks"""
    c = rng.choice(3, n, p=[0.36, 0.22, 0.42])
    mu = np.array([7.4, 12.6, 20.3])[c]
    sd = np.array([1.1, 1.0, 1.6])[c]
    return np.clip(rng.normal(mu, sd), 5.0, 23.6)


class Edition:
    def __init__(self, idx, spec, rng):
        self.idx, self.spec = idx, spec
        n = spec["pop"]
        self.n = n
        self.dev = rng.choice(3, n, p=spec["dev"])
        mix = {}
        for d, key in enumerate(P.DEVICES):
            v = np.array(P.BASE_MIX[key], float)
            v[2] *= spec["tilt"]
            v[4] *= spec.get("xmult", 1.0)
            v[1] *= spec.get("rmult", 1.0)
            v /= v.sum()
            mix[d] = v
        self.type = np.zeros(n, int)
        for d in range(3):
            m = self.dev == d
            self.type[m] = rng.choice(5, m.sum(), p=mix[d])
        pp = np.array([min(0.9, P.PRINT_P[t] * spec["print_scale"]) for t in P.TYPES])
        self.printed = rng.random(n) < pp[self.type]
        wk = np.array(spec["wk"])[self.dev]
        wk_pr = np.minimum(0.95, wk * spec["skew"])
        self.webkit = rng.random(n) < np.where(self.printed, wk_pr, wk)
        self.family = np.empty(n, dtype=object)
        for d, key in enumerate(P.DEVICES):
            for w in (True, False):
                m = (self.dev == d) & (self.webkit == w)
                fams, ps = zip(*P.UA_FAMILIES[(key, w)])
                self.family[m] = rng.choice(np.array(fams, dtype=object), m.sum(), p=np.array(ps) / sum(ps))
        self.multi = rng.random(n) < P.MULTI_EDITION
        self.second = np.where(self.multi, (idx + 1 + rng.integers(0, 2, n) * 10) % 12, idx)
        # renewal processes for W, O and X: next visit (in days from history start)
        self.next = np.full(n, np.inf)
        self.gapmean = np.ones(n)
        for t, (shape, mean) in (("W", P.W_GAP), ("O", P.O_GAP), ("X", P.X_GAP)):
            m = self.type == P.TYPES.index(t)
            self.gapmean[m] = mean
            g = rng.gamma(shape, self.gapmean[m] / shape)
            self.next[m] = -rng.random(m.sum()) * g
        self.refuser = rng.random(n) < P.REFUSER
        self.walled_month = np.full(n, -999)
        self.reg = self.printed.copy()
        self.source = np.where(self.printed, "print", "").astype(object)
        self.reg_day = np.where(self.printed, -1, 10 ** 6)
        self.reg_time = np.full(n, np.nan)          # absolute hours of the registering wall session
        self.cookie = np.zeros(n, int)               # the identifier in use (counter per browser)
        self.cookie_born = np.full(n, np.nan)        # absolute hours the identifier in use was first written
        self.vcookie = np.zeros(n, int)              # the seven-day rule replayed on every browser
        self.last_end = np.full(n, -1e9)             # absolute days
        self.meter = np.zeros(n)
        self.meter_month = np.full(n, -999)
        self.meter_since = np.full(n, np.nan)        # absolute hours of the first read the meter in use counts


def _advance_renewal(rng, E, k, tmask):
    """W, O and X: visit today if the next renewal falls on day k; draw the following gap"""
    hit = tmask & (np.floor(E.next) <= k)
    idx = np.where(hit)[0]
    if len(idx):
        tt = E.type[idx]
        shapes = np.select([tt == 2, tt == 3], [P.W_GAP[0], P.O_GAP[0]], P.X_GAP[0])
        g = rng.gamma(shapes, E.gapmean[idx] / shapes)
        E.next[idx] = np.maximum(E.next[idx] + g, k + 1)
    return hit


def simulate(seed=P.SEED):
    rng = np.random.default_rng(seed)
    eds = [Edition(i, s, rng) for i, s in enumerate(P.EDITIONS)]
    q4, monthly, walls = [], [], []
    for E in eds:
        recs, tally = [], {}
        isD, isR = (E.type == 0), (E.type == 1)
        isRen = E.type >= 2
        cur_m = None
        st_ = {}

        def flush(m):
            if m is None or m < 0:
                return
            tally[m] = {k2: v.copy() for k2, v in st_.items()}
        for k in range(NDAY):
            m = MONTH[k]
            if m != cur_m:
                flush(cur_m)
                cur_m = m
                st_ = dict(act=np.zeros((E.n, 2), bool), c0=np.full((E.n, 2), -1), c1=np.full((E.n, 2), -1),
                           v0=np.full((E.n, 2), -1), v1=np.full((E.n, 2), -1), sg=np.zeros((E.n, 2), bool),
                           sess=np.zeros((E.n, 2), int), pages=np.zeros((E.n, 2), int))
            visit = np.zeros(E.n, bool)
            visit |= isD & (rng.random(E.n) < P.DAY_P["D"])
            visit |= isR & (rng.random(E.n) < P.DAY_P["R"])
            visit |= _advance_renewal(rng, E, k, isRen)
            idx = np.where(visit)[0]
            if not len(idx):
                continue
            tp = E.type[idx]
            ns = 1 + rng.poisson(np.array([P.SESS_PER_DAY[t] - 1 for t in P.TYPES])[tp])
            ns = np.minimum(ns, 6)
            maxs = ns.max()
            valid = np.arange(maxs)[None, :] < ns[:, None]
            st = np.sort(np.where(valid, tod(rng, len(idx) * maxs).reshape(len(idx), maxs), np.inf), axis=1)
            dur = rng.gamma(2.0, 3.2, (len(idx), maxs)) / 60.0          # hours
            en = np.minimum(st + dur, 23.99)
            abs0 = 24.0 * k - OFF[k]                                     # absolute hours (UTC) of local midnight
            first = (abs0 + st[:, 0]) / 24.0
            last = (abs0 + np.max(np.where(valid, en, -np.inf), axis=1)) / 24.0
            # the seven-day rule, in elapsed time
            gap = first - E.last_end[idx]
            reset = gap > P.CAP_DAYS
            E.vcookie[idx] += reset
            wk = E.webkit[idx]
            E.cookie[idx] += reset & wk
            newborn = np.isnan(E.cookie_born[idx]) | (reset & wk)
            E.cookie_born[idx] = np.where(newborn, abs0 + st[:, 0], E.cookie_born[idx])
            mreset = (E.meter_month[idx] != m) | (reset & wk)
            E.meter[idx] = np.where(mreset, 0, E.meter[idx]); E.meter_month[idx] = m
            E.meter_since[idx] = np.where(mreset, np.nan, E.meter_since[idx])
            reads = rng.poisson(np.array([P.METERED[t] for t in P.TYPES])[tp][:, None] * np.ones((1, maxs)))
            reads = np.where(valid, reads, 0)
            pv = 1 + rng.poisson(np.array([P.PAGES[t] - 1 for t in P.TYPES])[tp][:, None] * np.ones((1, maxs)))
            pv = np.where(valid, np.maximum(pv, reads), 0)
            free = ~E.reg[idx]
            refd = E.refuser[idx] & (E.walled_month[idx] == m)
            reads = np.where(refd[:, None], 0, reads)
            cum = E.meter[idx][:, None] + np.cumsum(reads, axis=1)
            first_read = np.argmax(reads > 0, axis=1)
            has_read = (reads > 0).any(axis=1)
            start_meter = free & has_read & np.isnan(E.meter_since[idx])
            E.meter_since[idx] = np.where(start_meter, abs0 + st[np.arange(len(idx)), first_read], E.meter_since[idx])
            wall_s = free[:, None] & (cum > P.FREE) & (reads > 0) & (k >= WALL_FIRST) & valid
            nwall = wall_s.sum(axis=1)
            E.meter[idx] = np.where(free, cum[:, -1], E.meter[idx])
            u = rng.random(len(idx))
            p_any = 1 - (1 - P.P_REG - P.P_SUB) ** nwall
            newreg = (nwall > 0) & (u < p_any) & ~E.refuser[idx]
            E.walled_month[idx[(nwall > 0) & E.refuser[idx]]] = m
            sub = newreg & (rng.random(len(idx)) < P.P_SUB / (P.P_REG + P.P_SUB))
            first_wall = np.argmax(wall_s, axis=1)
            signed_before = E.reg[idx] & (E.reg_day[idx] < k)
            sig = valid & (signed_before[:, None] | (newreg[:, None] & (np.arange(maxs)[None, :] > first_wall[:, None])))
            ridx = idx[newreg]
            E.reg[ridx] = True; E.reg_day[ridx] = k
            E.reg_time[ridx] = abs0 + st[np.where(newreg)[0], first_wall[newreg]]
            E.source[idx[newreg & ~sub]] = "registration"; E.source[idx[sub]] = "subscription"
            E.last_end[idx] = last
            ed2 = E.multi[idx] & (rng.random(len(idx)) < P.MULTI_SHARE)
            slot = ed2.astype(int)
            S = st_
            S["act"][idx, slot] = True
            cc = E.cookie[idx]; vv = E.vcookie[idx]
            S["c0"][idx, slot] = np.where(S["c0"][idx, slot] < 0, cc, S["c0"][idx, slot]); S["c1"][idx, slot] = cc
            S["v0"][idx, slot] = np.where(S["v0"][idx, slot] < 0, vv, S["v0"][idx, slot]); S["v1"][idx, slot] = vv
            S["sg"][idx, slot] |= sig.any(axis=1)
            S["sess"][idx, slot] += ns; S["pages"][idx, slot] += pv.sum(axis=1)
            if k >= Q4_FIRST:
                ws = np.where(nwall > 0)[0]
                for j in ws:
                    for s_ in np.where(wall_s[j])[0]:
                        out = ("subscription" if sub[j] else "registration") if (newreg[j] and s_ == first_wall[j]) else "closed"
                        walls.append((E.idx, int(idx[j]), int(E.second[idx[j]] if slot[j] else E.idx), abs0 + st[j, s_],
                                      int(cc[j]), out, E.meter_since[idx[j]]))
                recs.append(dict(day=k, b=idx, ns=ns, st=abs0 + st, en=abs0 + en, pv=pv, reads=reads, sig=sig,
                                 cookie=cc, born=E.cookie_born[idx].copy(), ed=np.where(slot == 1, E.second[idx], E.idx)))
        flush(cur_m)
        q4.append(recs)
        monthly.append(tally)
    return eds, q4, monthly, walls


def sessions(eds, q4):
    """the fourth quarter as one table of sessions: one row per session of a regular browser"""
    import pandas as pd
    parts = []
    for E, recs in zip(eds, q4):
        for r in recs:
            ns = r["ns"]
            maxs = r["st"].shape[1]
            valid = np.arange(maxs)[None, :] < ns[:, None]
            rows, cols = np.where(valid)
            parts.append(pd.DataFrame({
                "home": np.full(len(rows), E.idx, np.int8), "b": r["b"][rows].astype(np.int32),
                "ed": r["ed"][rows].astype(np.int8), "day": np.full(len(rows), r["day"], np.int16),
                "start": r["st"][rows, cols], "end": r["en"][rows, cols], "pv": r["pv"][rows, cols].astype(np.int16),
                "reads": r["reads"][rows, cols].astype(np.int16), "sig": r["sig"][rows, cols],
                "cookie": r["cookie"][rows].astype(np.int32), "born": r["born"][rows]}))
    return pd.concat(parts, ignore_index=True)
