"""Casting: which real trusts play which part, chosen deterministically and tuned to the ladder's targets."""
import datetime as dt

import numpy as np
import pandas as pd

import roles
from book import (central_rows, devolved_rows, group_row, net_of, avoid_window, rand_start, school_row, SCHOOL_ROLES,
                  OFFICER_ROLES)
from world import AS_AT, rng, term_for

D = dt.date
PURCHASES = [D(2021, 9, 1), D(2022, 9, 1), D(2023, 9, 1), D(2024, 9, 1), D(2025, 9, 1),
             D(2022, 1, 1), D(2023, 4, 1), D(2024, 1, 1), D(2025, 4, 1), D(2023, 11, 1), D(2024, 11, 1)]
PILOT_PURCHASES = [D(2022, 11, 1), D(2023, 1, 1), D(2023, 4, 1), D(2024, 1, 1), D(2024, 4, 1), D(2025, 1, 1),
                   D(2025, 4, 1), D(2023, 11, 1), D(2024, 11, 1)]

# Central answer pool, best first. Index 2 is the twin. 0-9 the answer, 10-14 the five behind it.
CENTRAL_TARGETS = [43000, 37000, None, 25500, 22200, "big1", 17300, "big2", 13600, 12600,
                   10600, 9900, 9200, 8400, 7700, 6400, 5900, 5400]
CENTRAL_PRE = [0, 2, 0, 0, 3, 0, 1, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0]
BIG = {"big1": dict(net=(17800, 21500), loss=8000, hidden_pupils=800),
       "big2": dict(net=(14500, 16600), loss=8000, hidden_pupils=800)}
# Devolved decoys, best first. Index 6 is the twin. Indices 1 and 4 carry hidden agreements (rung 1).
DECOY_TARGETS = [66000, 58500, 52500, 46000, 41500, 36000, None]
DECOY_K = [3, 3, 4, 3, 2, 3, 3]
DECOY_PRE = [0, 2, 0, 0, 1, 0, 0]
CONTENDER_TARGETS = [26200, 24100, 22000, 19900, 18000]


class Cast:
    def __init__(self, reg):
        self.reg = reg
        self.g, self.op = roles.profiles(reg)
        self.used = set()
        self.rows = []
        self.role = {}
        self.mode = {}
        self.net = {}
        self.pilot = []
        self.cluster = []
        self.sell_urns = set(int(u) for u in reg.open_state()["URN"])

    def acads(self, uid):
        return roles.academy_frame(self.reg, self.op, uid)

    def clean_pool(self, cond):
        g = self.g
        c = g[g["clean"] & cond(g)]
        return [int(u) for u in c.index if int(u) not in self.used]

    def commit(self, uid, rows, tag, mode, net):
        self.used.add(uid)
        self.rows.extend(rows)
        self.role[uid] = tag
        self.mode[uid] = mode
        self.net[uid] = net

    # ------------------------------------------------------------------ helpers
    def try_central(self, uid, target, pre_k, tag, tol=0.025, purchases=PURCHASES, subset=None):
        a = self.acads(uid)
        r = rng("central", uid)
        best = None
        opts = [(p, s) for p in purchases for s in ("all", "primary")] if subset is None else [(purchases[0], "all")]
        for p, s in opts:
            rows, left = central_rows(self.reg, uid, a, p, s, pre_k, tag, r, subset=subset)
            if left or len(rows) < 2:
                continue
            if sum(1 for x in rows if x["annual_value_gbp"] > 900.0) < 1:
                continue
            n = net_of(a, rows)
            err = abs(n - target) / target
            if best is None or err < best[0]:
                best = (err, rows, n, p, s)
        if best is None or best[0] > tol:
            return None
        return best

    def try_big(self, uid, tag, which):
        """A large trust the office bought for most of: a big repricing, several academies under old URNs."""
        a = self.acads(uid)
        best = None
        for p in PURCHASES:
            for s in ("all", "primary"):
                for pre_k in (8, 7, 6, 5, 4, 3):
                    rows, left = central_rows(self.reg, uid, a, p, s, pre_k, tag, rng("big", uid, pre_k))
                    if left or len(rows) < 6:
                        continue
                    n = net_of(a, rows)
                    covered = sum(x["pupils_billed"] for x in rows)
                    loss = sum(x["annual_value_gbp"] for x in rows) - 4.05 * sum(x["pupils_current"] for x in rows)
                    hidden = sum(x["pupils_current"] for x in rows if x["urn"] != x["urn_current"])
                    b = BIG[which]
                    if not (b["net"][0] <= n <= b["net"][1] and loss >= b["loss"] and hidden >= b["hidden_pupils"]):
                        continue
                    key = (-loss, n)
                    if best is None or key < best[0]:
                        best = (key, rows, n)
                    break
        return best

    def try_devolved(self, uid, target, k, pre_k, tag, tol=0.03):
        a = self.acads(uid)
        best = None
        for trial in range(6):
            r = rng("devolved", uid, trial)
            for smallest in (True, False):
                rows, left = devolved_rows(self.reg, uid, a, k, pre_k, tag, r, smallest=smallest)
                if left or len(rows) < k:
                    continue
                n = net_of(a, rows)
                err = abs(n - target) / target if target else 0
                if best is None or err < best[0]:
                    best = (err, rows, n)
        if best is None or (target and best[0] > tol):
            return None
        return best

    # ------------------------------------------------------------------ the twin pair
    def twin(self):
        c = self.g[self.g["clean"] & (self.g["n_open"] >= 12)]
        best = None
        idx = sorted(int(u) for u in c.index)
        for i, u in enumerate(idx):
            for v in idx[i + 1:]:
                a, b = c.loc[u], c.loc[v]
                if a["n_open"] != b["n_open"] or a["region"] != b["region"]:
                    continue
                gap = abs(a["P_all"] - b["P_all"]) / max(a["P_all"], b["P_all"])
                if gap > 0.02 or a["P_all"] < 8000:
                    continue
                if best is None or gap < best[0]:
                    best = (gap, u, v)
        if best is None:
            raise AssertionError("no twin pair")
        _, u, v = best
        # the central one is the one the hash puts first
        cu, dv = (u, v) if rng("twin", u).random() < rng("twin", v).random() else (v, u)
        ad, ac = self.acads(dv), self.acads(cu)
        dres = None
        for trial in range(20):
            r = rng("twin-d", trial)
            rows, left = devolved_rows(self.reg, dv, ad, 3, 0, "decoy", r, smallest=True)
            if len(rows) == 3:
                dres = rows
                break
        ndv = net_of(ad, dres)
        # the central twin bought centrally for three academies of the same sizes
        sizes = sorted(x["pupils_current"] for x in dres)
        cand = ac.sort_values(["NumberOfPupils", "URN"])
        pick = []
        for s in sizes:
            rest = cand[~cand["URN"].isin(pick)]
            j = (rest["NumberOfPupils"] - s).abs().idxmin()
            pick.append(int(rest.loc[j, "URN"]))
        r = rng("twin-c")
        crows, _ = central_rows(self.reg, cu, ac, D(2024, 9, 1), "all", 0, "answer", r, subset=pick)
        ncu = net_of(ac, crows)
        self.commit(dv, dres, "decoy", "devolved", ndv)
        self.commit(cu, crows, "answer", "central", ncu)
        self.twin_pair = (cu, dv)
        return cu, dv

    def run(self):
        cu, dv = self.twin()
        # devolved decoys
        self.decoys = []
        for i, t in enumerate(DECOY_TARGETS):
            if t is None:
                self.decoys.append(dv)
                continue
            for u in self.clean_pool(lambda g: (g["n_open"] >= 15)):
                res = self.try_devolved(u, t, DECOY_K[i], DECOY_PRE[i], "decoy")
                if res:
                    self.commit(u, res[1], "decoy", "devolved", res[2])
                    self.decoys.append(u)
                    break
            else:
                raise AssertionError("no decoy for target %s" % t)
        # central answer pool
        self.central = []
        for i, t in enumerate(CENTRAL_TARGETS):
            if t is None:
                self.central.append(cu)
                continue
            if isinstance(t, str):
                for u in self.clean_pool(lambda g: g["n_open"].between(18, 70) & g["P_all"].between(12000, 34000)):
                    res = self.try_big(u, "answer", t)
                    if res:
                        self.commit(u, res[1], "answer", "central", res[2])
                        self.central.append(u)
                        break
                else:
                    raise AssertionError("no big central trust")
                continue
            for u in self.clean_pool(lambda g: g["n_open"].between(5, 30)):
                res = self.try_central(u, t, CENTRAL_PRE[i], "answer" if i < 10 else "behind")
                if res:
                    self.commit(u, res[1], "answer" if i < 10 else "behind", "central", res[2])
                    self.central.append(u)
                    break
            else:
                raise AssertionError("no central trust for target %s" % t)
        # devolved contenders just under the twin
        self.contenders = []
        for t in CONTENDER_TARGETS:
            for u in self.clean_pool(lambda g: g["n_open"].between(8, 30)):
                res = self.try_devolved(u, t, 2, 0, "contender")
                if res:
                    self.commit(u, res[1], "contender", "devolved", res[2])
                    self.contenders.append(u)
                    break
            else:
                raise AssertionError("no contender for %s" % t)
        self.cast_pilot()
        self.cast_filler()
        self.cast_cluster()
        self.cast_multi()
        self.cast_singles()
        self.mark_identity()
        self.cast_offcycle()
        return self

    def cast_offcycle(self):
        """A trust that asked for trust pricing after the pilot, was offered the licence in September and declined.
        Its academies' agreements were signed by their own heads, so the round plan cannot offer it the licence."""
        cluster = set(u for u, _ in self.cluster)
        pool = [u for u in self.filler_devolved if u not in cluster and u not in self.mixed
                and sum(1 for x in self.rows if x["uid"] == u) >= 2]
        self.offcycle = pool[int(rng("offcycle").integers(0, min(10, len(pool))))]

    # ------------------------------------------------------------------ one agreement for several academies
    MULTI_TARGETS = [47400, 32300, 6900, 5600]   # two that lead the round, two well out of contention

    def cast_multi(self):
        """Trusts whose office already buys for several primary academies under one agreement, recorded on the lead
        school's account; the agreements export keys it to that school and the invoices name the schools it covers."""
        self.multi = []
        for t in self.MULTI_TARGETS:
            for u in self.clean_pool(lambda g: g["n_open"].between(6, 60) & (g["n_prim"] >= 4)):
                res = self.try_multi(u, t)
                if res:
                    self.commit(u, [res[1]], "multi", "central", res[2])
                    self.multi.append(u)
                    break
            else:
                raise AssertionError("no multi-school trust for %s" % t)

    def try_multi(self, uid, target, tol=0.08):
        a = self.acads(uid)
        names = a["EstablishmentName"]
        unique = set(names[~names.duplicated(keep=False) & ~names.str.contains(";")])
        r = rng("multi", uid)
        best = None
        for start in (D(2023, 9, 1), D(2024, 4, 1), D(2023, 4, 1), D(2024, 9, 1)):
            prim = a[(a["band"] == "Primary") & (a["joined"].dt.date < start) & (a["open_d"].dt.date < start)
                     & a["TypeOfEstablishment (name)"].isin(["Academy converter", "Academy sponsor led"])
                     & a["EstablishmentName"].isin(unique)]
            if len(prim) < 3:
                continue
            order = sorted(prim["URN"].astype(int), key=lambda u: rng("multi-order", uid, u).random())
            for k in (3, 4):
                if len(order) < k:
                    continue
                role = OFFICER_ROLES[int(r.integers(0, len(OFFICER_ROLES)))]
                row = group_row(self.reg, uid, order[:k], start, role, "multi")
                n = net_of(a, [row])
                err = abs(n - target) / target
                if best is None or err < best[0]:
                    best = (err, row, n)
        if best is None or best[0] > tol:
            return None
        return best

    # ------------------------------------------------------------------ how the signatures are recorded
    def mark_identity(self):
        """Some trust officers' names are typed two ways across their academies' agreements (one CRM contact), and
        in some trusts whose academies buy for themselves one business manager signed for two academies."""
        cluster = set(u for u, _ in self.cluster) | set(self.cluster_won)

        def rows_of(u):
            return sorted([x for x in self.rows if x["uid"] == u], key=lambda z: (z["urn"], z["agreement_start"]))

        fc = [u for u in self.filler_central if u not in cluster and len(rows_of(u)) >= 3]
        self.variant = [self.central[0], self.central[6], self.central[8]] + fc[:3]
        for u in self.variant:
            rs = rows_of(u)
            r = rng("variant", u)
            for i in sorted(r.choice(len(rs), 1 if len(rs) <= 3 else 2, replace=False)):
                rs[int(i)]["name_variant"] = True
        fd = [u for u in self.filler_devolved if u not in cluster and len(rows_of(u)) >= 3]
        self.mixed = [self.decoys[0], self.decoys[1], self.decoys[3], self.decoys[5]] + fd[:3]
        for u in self.mixed:
            for x in rows_of(u)[:2]:
                x["signer_key"] = ("shared", u)
                x["signed_by_role"] = "Business Manager"
        # in one of them the business manager and the head of the third academy share a surname
        rs = rows_of(self.decoys[5])
        for x in rs[:2]:
            x["surname_from"] = rs[2]["signer_key"]
        rs[2]["signed_by_role"] = "Headteacher"
        self.same_surname = self.decoys[5]

    # ------------------------------------------------------------------ the 2026 pilot
    def cast_pilot(self):
        """Twelve trusts whose offices asked for trust pricing in spring 2026: all buy centrally, stable since June."""
        pool = self.clean_pool(lambda g: g["n_open"].between(4, 12) & g["stable"] & (g["n_pred"] >= 3))
        targets = [9800, 8700, 7900, 7300, 6800, 6200, 5700, 5200, 4800, 4300, 3900, 3500]
        pre = [1, 2, 0, 1, 0, 1, 0, 2, 0, 1, 0, 0]
        self.pilot = []
        mayjun = [D(2023, 5, 1), D(2024, 5, 1), D(2025, 5, 1), D(2024, 6, 1), D(2025, 6, 1), D(2023, 6, 1)]
        for i, t in enumerate(targets):
            for u in pool:
                if u in self.used:
                    continue
                purchases = mayjun if i in (2, 4) else PILOT_PURCHASES
                res = self.try_central(u, t, pre[i], "pilot", tol=0.08, purchases=purchases)
                if res:
                    self.commit(u, res[1], "pilot", "central", res[2])
                    self.pilot.append(u)
                    break
            else:
                raise AssertionError("no pilot trust for %s" % t)

    # ------------------------------------------------------------------ the rest of the eligible trusts
    def cast_filler(self):
        """The rest of the eligible trusts, all well out of contention. The first six central ones are the
        cluster licence winners: their academies went back onto school agreements from 1 September 2024."""
        self.filler_central, self.filler_devolved, self.cluster_won = [], [], []
        pool = self.clean_pool(lambda g: g["n_open"].between(3, 14))
        r = rng("filler")
        for u in pool:
            if len(self.filler_central) >= 46 and len(self.filler_devolved) >= 66:
                break
            a = self.acads(u)
            want_central = len(self.filler_central) < 46 and (len(self.filler_devolved) >= 66 or r.random() < 0.42)
            if want_central:
                winner = len(self.cluster_won) < 6
                purchases = [D(2024, 9, 1)] if winner else PURCHASES
                best = None
                for p in purchases:
                    for sc in ("all", "primary"):
                        rows, left = central_rows(self.reg, u, a, p, sc, 0, "filler", rng("fc", u))
                        if len(rows) < (3 if winner else 2):
                            continue
                        n = net_of(a, rows)
                        if n < 4800 and (best is None or abs(n - 1500) < abs(best[2] - 1500)):
                            best = (None, rows, n)
                if best:
                    self.commit(u, best[1], "filler", "central", best[2])
                    self.filler_central.append(u)
                    if winner:
                        self.cluster_won.append(u)
            else:
                if self.g.loc[u, "P_all"] > 3600:
                    continue
                k = 2 if r.random() < 0.6 else 3
                pre = 1 if r.random() < 0.18 else 0
                rows, left = devolved_rows(self.reg, u, a, k, pre, "filler", rng("fd", u))
                if left or len(rows) < k:
                    continue
                n = net_of(a, rows)
                if n >= 16000:
                    continue
                self.commit(u, rows, "filler", "devolved", n)
                self.filler_devolved.append(u)
        if len(self.filler_central) < 46 or len(self.filler_devolved) < 66:
            raise AssertionError("filler short: %d central, %d devolved" % (len(self.filler_central),
                                                                             len(self.filler_devolved)))

    # ------------------------------------------------------------------ the 2023-24 cluster licence offers
    def cast_cluster(self):
        """Thirty trusts offered the cluster licence in 2023-24: thirteen central (six won), seventeen devolved
        (none won). Every one held at least two agreements before the offer."""
        def held_two(u):
            return sum(1 for x in self.rows if x["uid"] == u and x["agreement_start"] < D(2023, 9, 1)) >= 2
        r = rng("cluster")
        rest_c = [u for u in self.filler_central if u not in self.cluster_won and held_two(u)]
        rest_d = [u for u in self.filler_devolved if held_two(u)]
        r.shuffle(rest_c)
        r.shuffle(rest_d)
        if len(rest_c) < 7 or len(rest_d) < 17:
            raise AssertionError("cluster pools short: %d central, %d devolved" % (len(rest_c), len(rest_d)))
        self.cluster = ([(u, "won") for u in self.cluster_won] + [(u, "lost") for u in rest_c[:7]]
                        + [(u, "lost") for u in rest_d[:17]])

    # ------------------------------------------------------------------ one academy in a trust
    def cast_singles(self):
        """Academies whose head bought for their own school, the only one in their trust holding an agreement."""
        e = self.op
        uids = sorted(set(int(u) for u in e["uid"].unique()) - self.used)
        r = rng("singles")
        r.shuffle(uids)
        self.singles = []
        for u in uids[:300]:
            a = self.acads(u)
            a = a[a["URN"].isin(self.sell_urns)]
            if len(a) == 0:
                continue
            pre = 1 if r.random() < 0.15 else 0
            rows, left = devolved_rows(self.reg, u, a, 1, pre, "single", rng("sg", u))
            if left or not rows:
                rows, left = devolved_rows(self.reg, u, a, 1, 0, "single", rng("sg2", u))
            if rows:
                self.commit(u, rows, "single", "single", None)
                self.singles.append(u)
