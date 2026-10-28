"""The full population of Brindlecote's accounts, month by month, from the first launch to the end of 2027.

Every draw is a counter-based hash of (account, month, slot), so the run with the limit and the run without it share
every random number until the limit makes them differ. Only accounts still on the books are carried; an account that
leaves or cancels is dropped after its month is recorded.

simulate() runs the history to the extract and returns what the pack is cut from; truth() carries the state on to
December 2027 with and without the limit in every app and returns each app's 2027 revenue difference."""
import numpy as np

import params as P

MASK = (1 << 64) - 1
_C1 = np.uint64(0x9E3779B97F4A7C15)


def _mix(x):
    x = x ^ (x >> np.uint64(30))
    x = x * np.uint64(0xBF58476D1CE4E5B9)
    x = x ^ (x >> np.uint64(27))
    x = x * np.uint64(0x94D049BB133111EB)
    return x ^ (x >> np.uint64(31))


def uni(ids, m, slot):
    """a uniform in [0, 1) for each account id, fixed by (id, month, slot) and the world's seed"""
    off = np.uint64(((m * 1315423911 + slot * 2654435761 + P.SEED * 97) * 0x632BE59BD9B4E019) & MASK)
    x = ids.astype(np.uint64) * _C1 + off
    return (_mix(x) >> np.uint64(11)).astype(np.float64) * (1.0 / 9007199254740992.0)


def _normal(ids, m, s1, s2):
    u1 = np.maximum(uni(ids, m, s1), 1e-12)
    return np.sqrt(-2.0 * np.log(u1)) * np.cos(2.0 * np.pi * uni(ids, m, s2))


class State:
    """the accounts on the books, one entry each"""
    FIELDS = ("id", "app", "born", "a", "g", "eng", "k", "s", "st", "pe", "ad", "panel", "since", "ps", "plan_m",
              "plan_k")

    def __init__(self):
        self.id = np.zeros(0, np.int64)
        self.app = np.zeros(0, np.int8)
        self.born = np.zeros(0, np.int16)
        self.a = np.zeros(0)
        self.g = np.zeros(0)
        self.eng = np.zeros(0)
        self.k = np.zeros(0, np.int16)
        self.s = np.zeros(0)
        self.st = np.zeros(0, np.int8)        # 0 free, 1 Plus, 2 gone
        self.pe = np.zeros(0, np.int8)        # 1 stopped by storage, 2 stopped by the project limit
        self.ad = np.zeros(0, bool)           # archived down to three under the limit
        self.panel = np.zeros(0, bool)
        self.since = np.zeros(0, np.int16)    # month it moved to Plus
        self.ps = np.zeros(0, np.int16)       # a panel account's last storage-stop decision
        self.plan_m = np.zeros(0, np.int16)   # the month its post-stop year's own move falls
        self.plan_k = np.zeros(0, np.int8)    # that move: 1 upgrade, 2 leave, 3 cancel
        self.next_id = 1

    def copy(self):
        c = State()
        for f in self.FIELDS:
            setattr(c, f, getattr(self, f).copy())
        c.next_id = self.next_id
        return c

    def add(self, app, m, n):
        ids = np.arange(self.next_id, self.next_id + n, dtype=np.int64)
        self.next_id += n
        a = np.exp(np.log(P.PROJ_BIRTH[0]) + P.PROJ_BIRTH[1] * _normal(ids, -1, 1, 2))
        g = np.exp(np.log(P.STORE_GROW[0]) + P.STORE_GROW[1] * _normal(ids, -1, 3, 4)) * (P.PROJ_BIRTH[0] / a) ** P.STORE_TILT
        eng = 0.35 + 0.65 * uni(ids, -1, 5)
        cols = dict(id=ids, app=np.full(n, app, np.int8), born=np.full(n, m, np.int16), a=a, g=g, eng=eng,
                    k=np.ones(n, np.int16), s=5.0 + 35.0 * uni(ids, -1, 6), st=np.zeros(n, np.int8),
                    pe=np.zeros(n, np.int8), ad=np.zeros(n, bool), panel=uni(ids, -1, 7) < 1.0 / P.PANEL_RATE,
                    since=np.full(n, -1, np.int16), ps=np.full(n, -99, np.int16), plan_m=np.full(n, -1, np.int16),
                    plan_k=np.zeros(n, np.int8))
        for f in self.FIELDS:
            setattr(self, f, np.concatenate([getattr(self, f), cols[f]]))
        return ids

    def keep(self, mask):
        for f in self.FIELDS:
            setattr(self, f, getattr(self, f)[mask])


def signups(i, m):
    if m < P.LAUNCH[i]:
        return 0
    ramp = min(1.0, 0.3 + 0.7 * (m - P.LAUNCH[i]) / 24.0)
    trend = 1.0 + 0.004 * max(0, m - 240) / 12.0
    return int(round(P.SIGNUPS[i] * P.SEASON[m % 12] * ramp * trend))


def step(S, m, limit, seq, rec=None):
    """one month for every account on the books; returns the month's activity masks"""
    n = len(S.id)
    ids = S.id
    t = m - S.born
    r = [uni(ids, m, j) for j in range(9)]
    pu, pl = P.RESPONSE
    # decisions on last month's stops
    dec = (S.st == 0) & (S.pe > 0)
    up = dec & (r[0] < pu)
    lv = dec & (r[0] >= pu) & (r[0] < pu + pl)
    tr = dec & (r[0] >= pu + pl)
    pidx = np.nonzero(dec & (S.pe == 1) & S.panel)[0]
    def stratum(x):
        yrs = (m - int(S.born[x])) / 12.0
        return (int(S.app[x]), bool(S.k[x] >= 4), 0 if yrs < 3 else (1 if yrs < 6 else 2))
    for x in pidx:                     # the panel's storage stops take their responses in an even sequence, one for
        sq = seq.setdefault(stratum(x), [0, 0, 0, 0.0, 0, 0.0, 0, 0.0, 0])   # each app, project band and age
        sq[0] += 1
        if np.floor(sq[0] * pu + 0.5) > sq[1]:
            sq[1] += 1
            up[x], lv[x], tr[x] = True, False, False
        elif np.floor(sq[0] * (pu + pl) + 0.5) > sq[1] + sq[2]:
            sq[2] += 1
            up[x], lv[x], tr[x] = False, True, False
        else:
            up[x], lv[x], tr[x] = False, False, True
    S.st[up] = 1
    S.since[up] = m
    S.st[lv] = 2
    st_tr = tr & (S.pe == 1)
    pj_tr = tr & (S.pe == 2)
    S.s[st_tr] = P.CAP * (P.TRIM[0] + (P.TRIM[1] - P.TRIM[0]) * r[6][st_tr])
    S.g[st_tr] *= P.LEARN
    S.k[pj_tr] = np.minimum(S.k[pj_tr], 3)
    S.ad[pj_tr] = True
    # a panel account's year after a storage stop: its own move (an upgrade or a departure for an account that
    # trimmed, a cancellation for one that upgraded) is planned at the decision in an even sequence over the stops in
    # the order they fall, so every run of stops carries the year's rates
    S.ps[pidx] = m
    S.plan_m[pidx] = -1
    S.plan_k[pidx] = 0
    for x in pidx:
        sq = seq[stratum(x)]
        if up[x]:
            sq[5] += 1.0 - (1.0 - P.PAID_CHURN) ** 12
            if np.floor(sq[5] + 0.5) > sq[6]:
                sq[6] += 1
                S.plan_m[x], S.plan_k[x] = m + 1 + (sq[6] * 7) % 12, 3
        elif tr[x]:
            uu, ll = P.own_rates(np.array([m - S.born[x]]))
            sq[3] += 1.0 - (1.0 - float(uu[0])) ** 12
            sq[7] += 1.0 - (1.0 - float(ll[0])) ** 12
            if np.floor(sq[3] + 0.5) > sq[4]:
                sq[4] += 1
                S.plan_m[x], S.plan_k[x] = m + 1 + (sq[4] * 5) % 12, 1
            elif np.floor(sq[7] + 0.5) > sq[8]:
                sq[8] += 1
                S.plan_m[x], S.plan_k[x] = m + 1 + (sq[8] * 7) % 12, 2
    S.pe[dec] = 0
    # own-accord moves
    free = (S.st == 0) & ~dec
    u, l = P.own_rates(t)
    oup = free & (r[1] < u)
    olv = free & ~oup & (r[1] >= u) & (r[1] < u + l)
    post = S.panel & (m - S.ps >= 1) & (m - S.ps <= 12)
    planned = post & (S.plan_m == m)
    oup[post] = False
    olv[post] = False
    oup |= free & planned & (S.plan_k == 1)
    olv |= free & planned & (S.plan_k == 2)
    S.st[oup] = 1
    S.since[oup] = m
    S.st[olv] = 2
    pch = (S.st == 1) & ~up & ~oup & (r[2] < P.PAID_CHURN)
    pch[post] = False
    pch |= (S.st == 1) & planned & (S.plan_k == 3)
    S.st[pch] = 2
    # projects and storage
    on = (S.st == 0) | (S.st == 1)
    born = on & (r[3] < S.a)
    S.k[born] += 1
    free = S.st == 0
    died = free & (r[4] < P.PROJ_DEATH * S.k) & (S.k > 1)
    S.k[died] -= 1
    if limit and m >= P.M_LIMIT - 1:
        x = free & S.ad & (S.k > 3)
        S.k[x] = 3
    S.s[free] += S.g[free] * np.exp(1.73 * (r[7][free] - 0.5))
    paid = S.st == 1
    S.s[paid] += S.g[paid] * np.exp(1.73 * (r[7][paid] - 0.5))
    clean = free & (r[5] < P.CLEANUP[0])
    S.s[clean] *= P.CLEANUP[1] + (P.CLEANUP[2] - P.CLEANUP[1]) * r[6][clean]
    hit = free & (S.s >= P.STOP_AT)
    S.s[hit] = P.CAP - 0.02 - 0.95 * r[6][hit]
    S.pe[hit] = 1
    if limit and m >= P.M_LIMIT - 1:
        over = free & (S.k >= 4) & ~S.ad & (S.pe == 0)
        S.pe[over] = 2
    skip = free & (t >= 3) & (r[8] < P.SKIP)
    act_free = free & ~skip
    act_paid = S.st == 1
    days = np.where(act_free | act_paid, 1 + np.floor(27.0 * S.eng * r[8] ** 0.6 + 2.0 * r[5]).astype(int), 0)
    if rec is not None:
        rec(S, m, act_free, act_paid, days, up, oup, pch, lv, olv)
    return act_free, act_paid


def simulate(until=P.M_EXTRACT, limit=False, state=None, start=None, collect=True):
    """the history from the first launch (or from a saved state) to the end of month `until`"""
    S = state.copy() if state is not None else State()
    seq = {}
    out = {"panel_rows": [], "panel_acc": {}, "kpi": {}, "spells": [], "paid_at": {}, "rev": {}}
    m0 = P.M_SIM0 if start is None else start
    for m in range(m0, until + 1):
        for i in range(5):
            c = signups(i, m)
            if c:
                ids = S.add(i, m, c)
                if collect:
                    pm = S.panel[-c:]
                    for x in ids[pm]:
                        out["panel_acc"][int(x)] = (i, m)
        rec = _recorder(out) if collect else None
        act_free, act_paid = step(S, m, limit, seq, rec)
        if m >= P.M_LIMIT:
            out["rev"][m] = np.array([[(act_paid & (S.app == i)).sum(), (act_free & (S.app == i)).sum()]
                                      for i in range(5)])
        if m in (P.M_EXTRACT, P.M_LIMIT - 1):
            out["heavy_%d" % m] = np.array([((S.st == 0) & (S.app == i) & (S.k >= 4)).sum() for i in range(5)])
        S.keep(S.st != 2)
    out["state"] = S
    out["seq"] = seq
    return out


def _recorder(out):
    def rec(S, m, act_free, act_paid, days, up, oup, pch, lv, olv):
        if P.M_PANEL0 <= m <= P.M_EXTRACT:
            pi = np.nonzero(S.panel & (act_free | act_paid))[0]
            out["panel_rows"].append((m, S.id[pi].copy(), S.app[pi].copy(), S.st[pi].copy(), S.k[pi].copy(),
                                      S.s[pi].copy(), days[pi].copy(), S.since[pi].copy()))
            band = np.minimum(S.k, 10)
            cnt = np.zeros((5, 11), np.int64)
            np.add.at(cnt, (S.app[act_free], band[act_free]), 1)
            out["kpi"][m] = cnt
        if P.M_EXTRACT - 11 <= m <= P.M_EXTRACT:
            # the paying population for the billing records: who moved to Plus, who cancelled, and when
            for x in np.nonzero(up | oup)[0]:
                out["spells"].append((int(S.id[x]), int(S.app[x]), m, "start"))
            for x in np.nonzero(pch)[0]:
                out["spells"].append((int(S.id[x]), int(S.app[x]), m, "end"))
        if m == P.M_EXTRACT - 12:
            pa = np.nonzero(S.st == 1)[0]
            out["paid_at"] = {int(S.id[x]): (int(S.app[x]), int(S.since[x])) for x in pa}
        if P.M_PANEL0 <= m <= P.M_EXTRACT:
            # panel leavers this month, for the account register's closures and merges
            pl_ = np.nonzero(S.panel & (lv | olv))[0]
            for x in pl_:
                out.setdefault("panel_left", {})[int(S.id[x])] = (m, bool(olv[x]))
    return rec


def truth(base):
    """each app's 2027 revenue with the limit less without it, carried on from the extract's state"""
    S0 = base["state"]
    pre = simulate(until=P.M_LIMIT - 2, state=S0, start=P.M_EXTRACT + 1, collect=False)
    out = {}
    for lim in (False, True):
        out[lim] = simulate(until=P.M_LAST, limit=lim, state=pre["state"], start=P.M_LIMIT - 1, collect=False)
    d = sum(out[True]["rev"][m] - out[False]["rev"][m] for m in range(P.M_LIMIT, P.M_LAST + 1))
    val = d[:, 0] * np.array(P.PLUS) + d[:, 1] * np.array(P.FREE_REV)
    return {"add": val, "paid_months": d[:, 0], "free_months": d[:, 1],
            "stock_dec": out[False]["heavy_%d" % (P.M_LIMIT - 1)]}


if __name__ == "__main__":
    import time
    t0 = time.time()
    b = simulate()
    print("history %.1fs, on the books %d, panel rows %d" % (time.time() - t0, len(b["state"].id),
                                                              sum(len(x[1]) for x in b["panel_rows"])))
    print("heavy free at the extract", dict(zip(P.APPS, b["heavy_%d" % P.M_EXTRACT])))
    t0 = time.time()
    tr = truth(b)
    print("truth %.1fs" % (time.time() - t0))
    for i, a in enumerate(P.APPS):
        print("%-11s 2027 add %10.0f  (paid months %+7.0f, free months %+8.0f)" % (a, tr["add"][i], tr["paid_months"][i],
                                                                                  tr["free_months"][i]))
