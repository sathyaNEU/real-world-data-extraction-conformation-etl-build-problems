"""The 2025 world: six station networks of a docked bike-share, simulated event by event in whole seconds.

Requests arrive at each station as a Poisson process whose rate is constant within each (month, day type, local hour).
A request that finds a bike becomes a ride; one that finds the station empty leaves no row anywhere. Every ride, van
move, false start and the 03:00 count is kept, with bike identities, e-bike batteries and charging sessions, and the
workshop jobs of bikes the night crew swaps out. At one second, requests are served before arrivals and van drops, so
a bike docked at second s rides from s + 1. The request stream is drawn first from SEED_WORLD in the order of the scratch
scan; vans, false starts and the workshop draw from their own streams, so tuning them never moves a request.
"""
import datetime as dt
import heapq
import itertools
from collections import deque

import numpy as np

import params as P

WK, WE = 0, 1


def _prof(pairs, night=0.15):
    p = np.full(24, night)
    for h, v in pairs.items():
        p[h] = v
    return p


ROLES = {
    ("CEN", "edge"): {WK: _prof({6: 2.5, 7: 6, 8: 7, 9: 3, 10: 2, 11: 2, 12: 2.5, 13: 2, 14: 2, 15: 2, 16: 2, 17: 2.5, 18: 2.5, 19: 2, 20: 1.5, 21: 1, 22: 0.6, 23: 0.4}),
                      WE: _prof({8: 1, 9: 1.5, 10: 2, 11: 2.5, 12: 2.5, 13: 2.5, 14: 2.5, 15: 2.5, 16: 2, 17: 2, 18: 1.5, 19: 1.5, 20: 1, 21: 0.8, 22: 0.5})},
    ("CEN", "core"): {WK: _prof({7: 1.5, 8: 2, 9: 2, 10: 2, 11: 2.5, 12: 3.5, 13: 3, 14: 2, 15: 2, 16: 3, 17: 6.5, 18: 5.5, 19: 2.5, 20: 1.5, 21: 1, 22: 0.6, 23: 0.4}),
                      WE: _prof({9: 1, 10: 1.5, 11: 2, 12: 2.5, 13: 2.5, 14: 2.5, 15: 2.5, 16: 2.5, 17: 2, 18: 2, 19: 1.5, 20: 1.2, 21: 0.8, 22: 0.5})},
    ("UNI", "dorm", "term"): {WK: _prof({7: 2, 8: 9, 9: 2, 10: 2, 11: 2.5, 12: 8, 13: 2, 14: 2, 15: 2, 16: 2.5, 17: 3, 18: 2.5, 19: 2, 20: 2, 21: 1.5, 22: 1, 23: 0.5}, 0.1),
                              WE: _prof({9: 0.6, 10: 1, 11: 1.5, 12: 1.5, 13: 1.5, 14: 1.5, 15: 1.5, 16: 1.5, 17: 1.2, 18: 1, 19: 1, 20: 1, 21: 0.8, 22: 0.6}, 0.1)},
    ("UNI", "class", "term"): {WK: _prof({8: 1, 9: 2, 10: 2.5, 11: 2.5, 12: 2.5, 13: 2.5, 14: 2.5, 15: 3, 16: 3.5, 17: 7, 18: 3, 19: 2, 20: 2, 21: 3, 22: 1.5, 23: 0.5}, 0.1),
                               WE: _prof({10: 0.8, 11: 1, 12: 1.2, 13: 1.2, 14: 1.2, 15: 1.2, 16: 1.2, 17: 1.2, 18: 1, 19: 1, 20: 0.8, 21: 0.8}, 0.1)},
    ("UNI", "dorm", "break"): {WK: _prof({8: 0.8, 9: 1, 10: 1.2, 11: 1.2, 12: 1.4, 13: 1.2, 14: 1.2, 15: 1.2, 16: 1.2, 17: 1.2, 18: 1, 19: 1, 20: 0.8, 21: 0.6}, 0.08),
                               WE: _prof({10: 0.6, 11: 0.8, 12: 1, 13: 1, 14: 1, 15: 1, 16: 0.8, 17: 0.8, 18: 0.6, 19: 0.6, 20: 0.5}, 0.08)},
    ("UNI", "class", "break"): {WK: _prof({9: 0.6, 10: 0.8, 11: 0.8, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1.2, 17: 1.2, 18: 0.8, 19: 0.6, 20: 0.5}, 0.08),
                                WE: _prof({11: 0.5, 12: 0.6, 13: 0.6, 14: 0.6, 15: 0.6, 16: 0.6, 17: 0.5, 18: 0.5}, 0.08)},
    ("RIV", "water"): {WK: _prof({7: 0.5, 8: 0.8, 9: 0.8, 10: 1, 11: 1.2, 12: 1.4, 13: 1.4, 14: 1.4, 15: 1.4, 16: 1.5, 17: 1.6, 18: 1.6, 19: 1.4, 20: 1, 21: 0.6, 22: 0.3}, 0.06),
                       WE: _prof({8: 0.6, 9: 1.2, 10: 2, 11: 2.6, 12: 3, 13: 3, 14: 3, 15: 3, 16: 2.8, 17: 2.4, 18: 2, 19: 1.6, 20: 1.1, 21: 0.6, 22: 0.3}, 0.06)},
    ("OLD", "town"): {WK: _prof({7: 0.6, 8: 1, 9: 1, 10: 1, 11: 1.2, 12: 1.6, 13: 1.4, 14: 1.2, 15: 1.2, 16: 1.3, 17: 1.6, 18: 1.8, 19: 1.6, 20: 1.4, 21: 1, 22: 0.6}, 0.1),
                      WE: _prof({9: 0.8, 10: 1.2, 11: 1.6, 12: 2, 13: 2, 14: 1.8, 15: 1.6, 16: 1.6, 17: 1.6, 18: 1.8, 19: 1.8, 20: 1.4, 21: 1, 22: 0.7}, 0.1)},
    ("HIL", "top"): {WK: _prof({6: 1, 7: 3, 8: 3.5, 9: 1.5, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 0.8, 20: 0.6, 21: 0.4}, 0.08),
                     WE: _prof({9: 0.8, 10: 1.2, 11: 1.4, 12: 1.4, 13: 1.4, 14: 1.2, 15: 1, 16: 1, 17: 0.8, 18: 0.6, 19: 0.5}, 0.08)},
    ("HIL", "bottom"): {WK: _prof({7: 0.6, 8: 0.8, 9: 0.8, 10: 0.8, 11: 0.8, 12: 0.8, 13: 0.8, 14: 0.8, 15: 1, 16: 1.5, 17: 2.6, 18: 2.4, 19: 1, 20: 0.6, 21: 0.4}, 0.08),
                        WE: _prof({9: 0.6, 10: 0.8, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 0.8, 18: 0.6, 19: 0.5}, 0.08)},
    ("HBR", "quay"): {WK: _prof({7: 0.8, 8: 1.2, 9: 1, 10: 0.9, 11: 1, 12: 1.3, 13: 1.2, 14: 1, 15: 1, 16: 1.1, 17: 1.4, 18: 1.4, 19: 1.1, 20: 0.8, 21: 0.5, 22: 0.3}, 0.06),
                      WE: _prof({8: 0.5, 9: 0.9, 10: 1.4, 11: 1.8, 12: 2, 13: 2, 14: 2, 15: 1.9, 16: 1.8, 17: 1.6, 18: 1.4, 19: 1.1, 20: 0.8, 21: 0.5, 22: 0.3}, 0.06)},
}
DEST = {("CEN", "edge"): {"core": 0.8, "edge": 0.2}, ("CEN", "core"): {"edge": 0.8, "core": 0.2},
        ("UNI", "dorm"): {"class": 0.85, "dorm": 0.15}, ("UNI", "class"): {"dorm": 0.7, "class": 0.3},
        ("RIV", "water"): {"water": 1.0}, ("OLD", "town"): {"town": 1.0},
        ("HIL", "top"): {"bottom": 0.75, "top": 0.25}, ("HIL", "bottom"): {"top": 0.35, "bottom": 0.65},
        ("HBR", "quay"): {"quay": 1.0}}
FAULTS = {"classic": [("BRK", 0.24), ("CHN", 0.18), ("TYR", 0.2), ("LCK", 0.12), ("SAD", 0.1), ("LGT", 0.1), ("FRM", 0.06)],
          "ebike": [("BAT", 0.22), ("MOT", 0.14), ("BRK", 0.18), ("TYR", 0.16), ("LCK", 0.1), ("DSP", 0.1), ("CON", 0.1)]}


def calendar():
    T0 = int(dt.datetime(P.YEAR, 1, 1, tzinfo=P.TZ).timestamp())
    T1 = int(dt.datetime(P.YEAR + 1, 1, 1, tzinfo=P.TZ).timestamp())
    hours = np.arange(T0, T1, 3600)
    loc = [dt.datetime.fromtimestamp(int(h), P.TZ) for h in hours]
    return (T0, T1, hours, np.array([d.hour for d in loc]), np.array([d.month for d in loc]),
            np.array([int(d.weekday() >= 5) for d in loc]))


def local_ts(day, hh, mm, ss=0):
    return int(dt.datetime(day.year, day.month, day.day, hh, mm, ss, tzinfo=P.TZ).timestamp())


class World:
    def __init__(self, seed=P.SEED_WORLD, eworld=None, eb_e=1000):
        self.rs = np.random.default_rng(seed)
        self.rv = np.random.default_rng(P.SEED_VANS)
        self.rf = np.random.default_rng(P.SEED_FALSE)
        self.rw = np.random.default_rng(P.SEED_SHOP)
        self.rc = np.random.default_rng([P.SEED_VANS, 5])    # the crews' pace, the opening plug-ins, the point a rider picks
        self.eworld, self.eb_e = eworld, eb_e
        self.T0, self.T1, self.hours, self.H_hour, self.H_mon, self.H_we = calendar()
        self.docks = [(a, r) for a, (_, rl) in P.NETWORKS.items() for r, n in rl for _ in range(n)]
        self.ND = len(self.docks)
        self.area = np.array([a for a, r in self.docks]); self.role = np.array([r for a, r in self.docks])
        hbr = np.where(self.area == "HBR")[0]; perm = self.rs.permutation(hbr)
        self.pilot = np.zeros(self.ND, bool); self.matched = np.zeros(self.ND, bool)
        self.pilot[perm[:P.PILOT_N]] = True; self.matched[perm[P.PILOT_N:P.PILOT_N + P.MATCHED_N]] = True
        self.wkrate = {k: float(self._roles(k)[WK].sum()) for k in range(self.ND)}
        self.turned = np.zeros((self.ND, 12, 2, 24)); self.requests = np.zeros((self.ND, 12, 2, 24))
        self.rides, self.moves, self.counts, self.sessions, self.jobs = [], [], [], [], []
        self.seq = itertools.count()
        # identities
        self.cl_next = itertools.count(1); self.eb_next = itertools.count(1)
        self.pool = {}
        self.batt = {}; self.flag = {}; self.rides_since = {}; self.intermit = {}
        self.cl, self.points, self.overflow = {}, {}, {}
        self.maxstock = np.zeros(self.ND, int); self.maxeb = np.zeros(self.ND, int)


    def _roles(self, k):
        a, r = self.docks[k]
        return P_ROLES_TERM(a, r)

    def rate_vec(self, k):
        a, r = self.docks[k]
        if a == "UNI":
            term = np.isin(self.H_mon, list(P.TERM)); pt = ROLES[(a, r, "term")]; pb = ROLES[(a, r, "break")]
            out = np.where(self.H_we == 1, np.where(term, pt[WE][self.H_hour], pb[WE][self.H_hour]),
                           np.where(term, pt[WK][self.H_hour], pb[WK][self.H_hour]))
        else:
            p = ROLES[(a, r)]
            out = np.where(self.H_we == 1, p[WE][self.H_hour], p[WK][self.H_hour]) * np.array(P.MONTH)[self.H_mon - 1]
        out = out * P.SCALE.get((a, r), P.SCALE.get(a))
        return out * (1 + P.INDUCE) if (self.pilot[k] or a == self.eworld) else out

    # ------------------------------------------------------------------ e-bike helpers
    def _eb_level(self, e, t):
        lv, tp, k = self.batt[e]["lv"], self.batt[e]["tp"], self.batt[e]["pt"]
        if k is None:
            return lv
        return min(P.BATTERY_WH, lv + P.CHARGE_WH_MIN * (t - tp) / 60.0)

    def _plug(self, k, e, t):
        pts = self.points[k]
        free = [p for p in range(1, P.POINTS + 1) if p not in pts]
        b = self.batt[e]
        if free and self.pilot[k]:
            p = free[int(self.rc.integers(len(free)))]; pts[p] = e; b["pt"] = (k, p); b["tp"] = t
        else:
            self.overflow[k].append(e); b["pt"] = None; b["tp"] = t

    def _unplug(self, k, e, t):
        b = self.batt[e]
        if b["pt"] is not None:
            kk, p = b["pt"]
            gained = min(P.BATTERY_WH - b["lv"], P.CHARGE_WH_MIN * (t - b["tp"]) / 60.0)
            self.sessions.append((kk, p, e, b["tp"], t, gained / P.CHARGE_EFF))
            b["lv"] += gained
            del self.points[kk][p]
        else:
            self.overflow[k].remove(e)
        b["pt"] = None

    def _ebikes_at(self, k):
        return list(self.points[k].values()) + list(self.overflow[k])

    # ------------------------------------------------------------------ the simulation
    def run(self):
        for a in P.NETWORKS:
            if self.eworld and a != self.eworld:
                continue
            self._area(a)
        return self

    def _area(self, a):
        rs, rv, rf = self.rs, self.rv, self.rf
        self.cur = a                      # each network has its own depot and spares
        ix = [int(k) for k in np.where(self.area == a)[0]]
        roles = {r: [k for k in ix if self.role[k] == r] for r in dict.fromkeys(self.role[ix])}
        if a == self.eworld:
            for k in ix:
                self.pilot[k] = True
        pil = [k for k in ix if self.pilot[k]]
        ev = []
        push = lambda t, pr, e: heapq.heappush(ev, (int(t), pr, next(self.seq), e))
        for k in ix:
            n = rs.poisson(self.rate_vec(k)); tot = int(n.sum())
            t = np.repeat(self.hours, n) + rs.integers(0, 3600, tot); hi = np.repeat(np.arange(len(self.hours)), n)
            u = rs.random(tot); dur = np.maximum(120, np.round(rs.gamma(3.0, 5.5, tot) * 60)).astype(int)
            dd = rs.random(tot); rd = rs.random(tot)
            for j in range(tot):
                push(t[j], 1, ("req", k, int(hi[j]), u[j], int(dur[j]), dd[j], rd[j]))
            # false starts: an undock put straight back, about one in eighty requests
            nf = rf.poisson(self.rate_vec(k) * 0.0125); tf = np.repeat(self.hours, nf) + rf.integers(0, 3600, int(nf.sum()))
            for j, tt in enumerate(tf):
                push(tt, 1, ("false", k, int(rf.integers(5, 56)), rf.random()))
        day = dt.date(P.YEAR, 1, 1)
        while day <= dt.date(P.YEAR, 12, 31):
            for hh in P.VANRUNS[a]:
                push(local_ts(day, hh, 0) + int(rv.integers(0, 900)), 0, ("run", "van"))
            rst = local_ts(day, 1, 30) if day == dt.date(P.YEAR, 3, 9) else local_ts(day, 2, 30)
            push(rst + int(rv.integers(0, 240)), 0, ("run", "reset"))
            if pil:
                push(local_ts(day, 2, 40) + int(self.rc.integers(0, 300)), 0, ("ebike_restock",))
            push(local_ts(day, 3, 0), 3, ("count", day))
            day += dt.timedelta(days=1)
        # the opening fleet
        target = P.TARGET[a]
        for k in ix:
            self.cl[k] = deque(next(self.cl_next) for _ in range(target))
            self.points[k] = {}; self.overflow[k] = []
            for b in self.cl[k]:
                self._newbike(b, "classic")
        for _ in range(max(6, round(0.06 * target * len(ix)))):
            b = next(self.cl_next); self._newbike(b, "classic"); self._pool_in("classic", b, self.T0)
        ebn = self.eb_e if a == self.eworld else P.EB_PILOT
        for k in pil:
            for _ in range(ebn):
                e = "E%d" % next(self.eb_next); self.batt[e] = {"lv": P.BATTERY_WH, "tp": self.T0, "pt": None}
                self._newbike(e, "ebike"); self._plug(k, e, self.T0 - int(self.rc.integers(300, 7 * 3600)))
        if pil:
            for _ in range(P.EB_SPARES):
                e = "E%d" % next(self.eb_next); self.batt[e] = {"lv": P.BATTERY_WH, "tp": self.T0, "pt": None}
                self._newbike(e, "ebike"); self._pool_in("ebike", e, self.T0)
        while ev:
            t, pr, _, e = heapq.heappop(ev)
            kind = e[0]
            if kind == "req":
                self._request(a, roles, pil, t, e, push)
            elif kind == "false":
                _, k, d, u = e
                ebs = self._ebikes_at(k)
                if ebs and u < P.SWITCH:
                    b = max(ebs, key=lambda q: (self._eb_level(q, t), q)); self._unplug(k, b, t); typ = "ebike"
                elif self.cl[k]:
                    b = self.cl[k].popleft(); typ = "classic"
                else:
                    continue
                self.rides.append((t, t + d, k, k, typ, b, 1))
                push(t + d, 2, ("arr", k, typ, b))
            elif kind == "arr":
                _, k, typ, b = e
                if typ == "classic":
                    self.cl[k].append(b)
                else:
                    self._plug(k, b, t)
                self._peak(k)
            elif kind == "mv":
                _, f, to, n = e
                n = min(n, len(self.cl[f]))
                if n > 0:
                    for _ in range(n):
                        self.cl[to].append(self.cl[f].popleft())
                    self.moves.append((t, f, to, n, "classic"))
                    self._peak(to)
            elif kind == "run":
                self._run(a, ix, t, e[1], push)
            elif kind == "ebike_restock":
                self._restock(pil, t)
            elif kind == "count":
                for k in ix:
                    self.counts.append(((e[1] - dt.date(P.YEAR, 1, 1)).days, k, len(self.cl[k]), len(self._ebikes_at(k))))

    def _peak(self, k):
        self.maxstock[k] = max(self.maxstock[k], len(self.cl[k]) + len(self._ebikes_at(k)))
        self.maxeb[k] = max(self.maxeb[k], len(self._ebikes_at(k)))

    def _pool_in(self, typ, b, ready):
        heapq.heappush(self.pool.setdefault((self.cur, typ), []), (int(ready), next(self.seq), b))

    def _pool_out(self, typ, t):
        """the workshop sends out the bike it finished last: repaired bikes go back on the next run"""
        q = self.pool.setdefault((self.cur, typ), [])
        ready = [x for x in q if x[0] <= t]
        if not ready:
            return None
        x = max(ready)
        q.remove(x); heapq.heapify(q)
        return x[2]

    def _newbike(self, b, typ):
        self.flag[b] = None; self.rides_since[b] = 0; self.intermit[b] = None

    def _request(self, a, roles, pil, t, e, push):
        _, k, hi, u, dur, dd, rd = e
        m = self.H_mon[hi] - 1; w = self.H_we[hi]; h = self.H_hour[hi]
        self.requests[k, m, w, h] += 1
        ebs = self._ebikes_at(k)
        if ebs and u < P.SWITCH:
            typ = "ebike"
        elif self.cl[k]:
            typ = "classic"
        elif ebs:
            typ = "ebike"
        else:
            self.turned[k, m, w, h] += 1
            return
        acc = 0.0; pool = None
        for r, wgt in DEST[self.docks[k]].items():
            acc += wgt
            if dd <= acc:
                pool = roles[r]; break
        pool = pool or roles[list(DEST[self.docks[k]])[-1]]
        if typ == "ebike":
            cand = [p for p in pool if self.pilot[p]] or pil
            dst = cand[int(rd * len(cand)) % len(cand)]; d_s = int(round(dur * P.SPEED))
            b = max(ebs, key=lambda q: (self._eb_level(q, t), q)); self._unplug(k, b, t)
            self.batt[b]["lv"] = max(0.0, self.batt[b]["lv"] - P.USE_WH_MIN * d_s / 60.0)
        else:
            dst = pool[int(rd * len(pool)) % len(pool)]; d_s = dur
            b = self.cl[k].popleft()
        self.rides.append((t, t + d_s, k, dst, typ, b, 0))
        self._wear(b, typ, t)
        push(t + d_s, 2, ("arr", dst, typ, b))

    def _wear(self, b, typ, t):
        """a ride may leave the bike with a fault, flagged until the night crew swaps it out"""
        self.rides_since[b] += 1
        im = self.intermit[b]
        if im is not None and self.flag[b] is None:
            code, left = im
            if left <= 1:
                self.flag[b] = (code, t); self.intermit[b] = None
            else:
                self.intermit[b] = (code, left - 1)
            return
        if self.flag[b] is None and self.rw.random() < P.FAULT[typ]:
            codes, wts = zip(*FAULTS[typ])
            self.flag[b] = (codes[int(self.rw.choice(len(codes), p=np.array(wts) / sum(wts)))], t)

    def _shop(self, b, typ, t_in):
        """the workshop: a job from arrival to the repair, a second job when the road test fails, then spare"""
        code, _ = self.flag[b]
        op = t_in + int(self.rw.integers(35 * 60, 75 * 60))
        rep = int(min(6 * 86400, max(3600, self.rw.lognormal(np.log(20 * 3600), 0.9))))
        cl = op + rep
        if self.rw.random() < 0.02:
            self.jobs.append((b, typ, op, cl, code, "scrapped", False)); self.flag[b] = None
            return None
        self.jobs.append((b, typ, op, cl, code, "repaired", False))
        while self.rw.random() < P.RETEST:
            # the road test is ridden the same shift or, when the bench closes late, the next day
            op = cl + (int(self.rw.integers(10 * 60, 90 * 60)) if self.rw.random() < 0.6 else int(self.rw.integers(14 * 3600, 40 * 3600)))
            cl = op + int(min(3 * 86400, max(1800, self.rw.lognormal(np.log(6 * 3600), 0.8))))
            self.jobs.append((b, typ, op, cl, code, "repaired", True))
        self.flag[b] = None; self.rides_since[b] = 0
        if self.rw.random() < P.INTERMITTENT:
            # an intermittent fault usually shows again within a ride or two of the repair
            self.intermit[b] = (code, int(self.rw.geometric(0.45)))
        return cl

    def _run(self, a, ix, t, kind, push):
        rv = self.rv
        tot = sum(len(self.cl[k]) for k in ix); order = sorted(ix, key=lambda q: -self.wkrate[q])
        if kind == "van":
            goal = {k: tot // len(ix) for k in ix}
            for q in order[:tot - (tot // len(ix)) * len(ix)]:
                goal[q] += 1
        else:
            # the night crew works each station to its par; when the van runs short of time a station is left a
            # bike or two off it, and a spare bike or two is left where the morning is busiest
            goal = {k: P.TARGET[a] + int(self.rc.choice((-2, -1, 0, 1), p=(0.05, 0.17, 0.64, 0.14))) for k in ix}
            diff = tot - sum(goal.values())
            for q in (order[:diff] if diff > 0 else order[::-1][:-diff]):
                goal[q] += 1 if diff > 0 else -1
        sur = [[k, len(self.cl[k]) - goal[k]] for k in ix if len(self.cl[k]) > goal[k]]
        dfc = [[k, goal[k] - len(self.cl[k])] for k in ix if len(self.cl[k]) < goal[k]]
        plan = []
        i = j = 0
        while i < len(sur) and j < len(dfc):
            n = min(sur[i][1], dfc[j][1])
            if n > 0:
                plan.append((sur[i][0], dfc[j][0], n))
            sur[i][1] -= n; dfc[j][1] -= n
            if sur[i][1] == 0:
                i += 1
            if dfc[j][1] == 0:
                j += 1
        tt = t
        if kind == "reset":
            gap = max(15, min(50, (26 * 60) // max(1, len(plan) + 4)))
            for f, to, n in plan:
                push(tt, 2, ("mv", f, to, n)); tt += gap + int(rv.integers(0, 12))
            # the crew swaps flagged classic bikes for spares while it is out
            for k in ix:
                for b in [b for b in self.cl[k] if self.flag[b] is not None]:
                    s = self._pool_out("classic", tt)
                    if s is None:
                        break
                    self.cl[k].remove(b); self.cl[k].append(s)
                    dl = int(self.rc.integers(3, 9))
                    self.moves.append((tt, k, -1, 1, "classic")); self.moves.append((tt + dl, -1, k, 1, "classic"))
                    tt += int(self.rc.integers(12, 29))
                    back = self._shop(b, "classic", tt)
                    if back is not None:
                        self._pool_in("classic", b, back)
        else:
            for f, to, n in plan:
                push(tt, 2, ("mv", f, to, n)); tt += int(rv.integers(180, 480))

    def _restock(self, pil, t):
        """about 02:40: every pilot station back to its e-bikes; flagged e-bikes swapped for charged spares"""
        tt = t
        for k in pil:
            for e in [e for e in self._ebikes_at(k) if self.flag[e] is not None]:
                s = self._pool_out("ebike", tt)
                if s is None:
                    break
                self._unplug(k, e, tt); self.moves.append((tt, k, -1, 1, "ebike"))
                dl = int(self.rc.integers(3, 15))
                self.batt[s]["lv"] = P.BATTERY_WH; self._plug(k, s, tt + dl)
                self.moves.append((tt + dl, -1, k, 1, "ebike")); tt += int(self.rc.integers(9, 26))
                back = self._shop(e, "ebike", tt)
                if back is not None:
                    self._pool_in("ebike", e, back)
        want = self.eb_e if self.eworld else P.EB_PILOT
        for k in pil:
            have = self._ebikes_at(k)
            if len(have) > want:
                out = sorted(have, key=lambda q: (self._eb_level(q, tt), q))[: len(have) - want]
                for e in out:
                    self._unplug(k, e, tt); self._pool_in("ebike", e, tt)
                self.moves.append((tt, k, -1, len(out), "ebike")); tt += int(self.rc.integers(9, 26))
        for k in pil:
            need = want - len(self._ebikes_at(k))
            if need > 0:
                got = 0
                for _ in range(need):
                    s = self._pool_out("ebike", tt)
                    if s is None:
                        break
                    self.batt[s]["lv"] = P.BATTERY_WH; self._plug(k, s, tt); got += 1
                if got:
                    self.moves.append((tt, -1, k, got, "ebike")); tt += int(self.rc.integers(9, 26))


def P_ROLES_TERM(a, r):
    return ROLES[(a, r, "term")] if a == "UNI" else ROLES[(a, r)]


def world(seed=P.SEED_WORLD, eworld=None, eb_e=1000):
    return World(seed, eworld, eb_e).run()


if __name__ == "__main__":
    import sys, time
    t0 = time.time()
    W = world(int(sys.argv[1]) if len(sys.argv) > 1 else P.SEED_WORLD)
    for a in P.NETWORKS:
        ix = W.area == a; R = W.requests[ix].sum(); U = W.turned[ix].sum()
        print(f"{a} stations {ix.sum():3d} requests {R:9.0f} turned away {U:8.0f} ({U / max(R, 1) * 100:4.1f}%)")
    fs = sum(r[6] for r in W.rides)
    print("rides", len(W.rides) - fs, "false starts", fs, "moves", len(W.moves), "sessions", len(W.sessions), "jobs", len(W.jobs),
          "seconds", round(time.time() - t0, 1))
