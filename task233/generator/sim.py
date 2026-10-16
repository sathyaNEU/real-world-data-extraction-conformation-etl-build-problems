"""task233 world: three cohorts of school leavers (2024, 2025, 2026), their destinations, who returned the destinations
survey, the allocation of nonrespondents from the previous year's respondents, and the 2025 nonresponse follow-up.

Each leaver's destination is drawn once from uniforms fixed per leaver, so a district's nonresponse share moves only its
thresholds. Nonrespondents go to NEET more often and to higher education less often than respondents of the same
district and band: one odds ratio each, the departure the 2025 follow-up measures."""
import numpy as np
from scipy.special import expit, logit

import params as P


def mixf(t):
    return (1 - t) * P.AFF + t * P.DEP


class World:
    def __init__(self, seed=P.SEED, m26=None, m25=None):
        self.m26 = list(m26) if m26 is not None else [d[7] for d in P.DISTRICTS]
        self.m25 = list(m25) if m25 is not None else [d[6] for d in P.DISTRICTS]
        rng = np.random.default_rng(seed)
        self.U = {}
        for yr in (25, 26, 24):
            for d in range(P.ND):
                n = int(rng.integers(3300, 4500)); mix = mixf(P.DISTRICTS[d][4]); cnt = np.round(n * mix).astype(int)
                band = np.repeat(np.arange(P.B), cnt); n = len(band)
                self.U[(yr, d)] = dict(band=band, uu=rng.random(n), u1=rng.random(n), u2=rng.random(n), ut=rng.random(n))
        aux = np.random.default_rng(seed + 1)
        for k in sorted(self.U):
            n = len(self.U[k]["band"])
            self.U[k].update(u3=aux.random(n), u4=aux.random(n), us=aux.random(n), uc=aux.random(n), ua=aux.random(n),
                             ux=aux.random(n), sex=aux.random(n))
        self.aux = aux
        self.schools()

    # --------------------------------------------------------------- schools
    def schools(self):
        rng = np.random.default_rng(P.SEED + 2)
        self.school = []                                    # (code, district26, district25, weight)
        k = 0
        for d in range(P.ND):
            ns = int(rng.integers(9, 14))
            w = rng.gamma(4.0, 1.0, ns); w = w / w.sum()
            for j in range(ns):
                k += 1
                self.school.append([None, d, d, w[j]])
        # the two schools that moved district on the 2026 map: the smallest school of each receiving district
        for d26, d25 in P.MOVED:
            idx = [i for i, s in enumerate(self.school) if s[1] == d26]
            i = min(idx, key=lambda i: self.school[i][3])
            self.school[i][2] = d25
        order = rng.permutation(len(self.school))
        for r, i in enumerate(order):
            self.school[i][0] = "S%04d" % (1103 + 37 * r)
        self.school_idx = {d: [i for i, s in enumerate(self.school) if s[1] == d] for d in range(P.ND)}

    def assign_school(self, yr, d, n):
        rng = np.random.default_rng(P.SEED * 100 + yr * 13 + d)
        idx = self.school_idx[d]; w = np.array([self.school[i][3] for i in idx]); w = w / w.sum()
        return np.array(idx)[rng.choice(len(idx), n, p=w)]

    # --------------------------------------------------------------- cohorts
    def cohort(self, yr, d, m):
        aN, aH, t = P.DISTRICTS[d][2:5]
        U = self.U[(yr, d)]; band = U["band"]; mix = mixf(t); n = len(band)
        pu = m * P.UREL / (mix @ P.UREL); unk = np.zeros(n, bool)
        for b in range(P.B):
            idx = np.where(band == b)[0]; k = int(round(len(idx) * pu[b])); unk[idx[np.argsort(U["uu"][idx])[:k]]] = True
        pN = expit(aN + P.bN[band]); pH = expit(aH + P.bH[band])
        qN = np.where(unk, expit(logit(pN) + P.D_N), pN); qH = np.where(unk, expit(logit(pH) + P.D_H), pH)
        neet = U["u1"] < qN
        he = (~neet) & (U["u2"] < np.clip(qH / (1 - qN), 0, 1))
        rest = P.REST[band]; cum = np.cumsum(rest, axis=1)
        k3 = (U["u3"][:, None] > cum[:, :2]).sum(axis=1)       # 0 FE, 1 APP, 2 EMP
        cat = np.where(neet, 4, np.where(he, 0, 1 + k3))
        c = dict(band=band, unk=unk, cat=cat, d=np.full(n, d), yr=yr, n=n)
        c["school"] = self.assign_school(yr, d, n)
        c["d25map"] = np.array([self.school[i][2] for i in c["school"]])
        return c

    def build(self):
        self.y24 = [self.cohort(24, d, P.DISTRICTS[d][5]) for d in range(P.ND)]
        self.y25 = [self.cohort(25, d, self.m25[d]) for d in range(P.ND)]
        self.y26 = [self.cohort(26, d, self.m26[d]) for d in range(P.ND)]
        self.allocate()
        self.followup()
        self.odds_mid_bin()
        self.mid_bin()

    # --------------------------------------------------------------- allocation from the previous year's respondents
    @staticmethod
    def shares(cohorts, mapkey):
        tab = np.zeros((P.ND, P.B, 5)); cnt = np.zeros((P.ND, P.B))
        for c in cohorts:
            r = ~c["unk"]; dd = c[mapkey][r] if mapkey else c["d"][r]
            np.add.at(tab, (dd, c["band"][r], c["cat"][r]), 1)
            np.add.at(cnt, (dd, c["band"][r]), 1)
        return tab / cnt[:, :, None]

    def allocate(self):
        s24 = self.shares(self.y24, "d25map")          # 2024 respondents on the 2025 map, for the 2025 allocation
        s25 = self.shares(self.y25, None)              # 2025 respondents on the 2026 map, for the 2026 allocation
        self.s24, self.s25 = s24, s25
        for c in self.y25:
            c["alloc"] = np.zeros((c["n"], 5)); u = c["unk"]
            c["alloc"][u] = s24[c["d25map"][u], c["band"][u]]
        for c in self.y26:
            c["alloc"] = np.zeros((c["n"], 5)); u = c["unk"]
            c["alloc"][u] = s25[c["d"][u], c["band"][u]]

    # --------------------------------------------------------------- the 2025 follow-up (in the world: who was resolved)
    def followup(self):
        """the 2025 follow-up ran in five districts of the 2025 map: a school that moved district in 2026 was followed up, or
        not, with its 2025 district"""
        for c in self.y25:
            d = c["d"][0]; U = self.U[(25, d)]; n = c["n"]
            c["traced"] = np.zeros(n, bool); c["unresolved"] = np.zeros(n, bool)
            inside = np.array([bool(P.DISTRICTS[x][8]) for x in c["d25map"]])
            idx = np.where(c["unk"] & inside)[0]
            if len(idx):
                order = idx[np.argsort(U["ut"][idx])]
                k = int(round(len(idx) * P.TRACE_FRAC)); k2 = int(round(len(idx) * P.SAMPLE_EXTRA))
                c["traced"][order[:k]] = True; c["unresolved"][order[k:k + k2]] = True

    # --------------------------------------------------------------- the departure and the shifts (used for tuning)
    def calibration(self):
        rows = []
        for d in P.TRACED:
            c = self.y25[d]; t = c["traced"]
            rows.append(dict(d=c["d"][t], band=c["band"][t], cat=c["cat"][t], alloc=c["alloc"][t]))
        return {k: np.concatenate([r[k] for r in rows]) for k in rows[0]}

    # --------------------------------------------------------------- published rates kept clear of a rounding edge
    def mid_bin(self, floor=0.02):
        """move a published 2026 rate off a rounding edge by changing one respondent's recorded destination between a
        graded destination and an ungraded one (HE and FE, NEET and EMP); allocations, nonresponse and the follow-up are
        untouched, so no shift or flag moves"""
        pair = {0: 1, 4: 3}
        for it in range(400):
            worst = None
            for unit, members in self._units():
                for k in (4, 0):
                    num = sum(((c["cat"][m] == k) & ~c["unk"][m]).sum() + np.round(c["alloc"][m & c["unk"], k], 4).sum()
                              for c, m in members)
                    n = sum(m.sum() for c, m in members)
                    v = num / n * 100; fr = v * 10 - np.floor(v * 10); dist = abs(fr - 0.5) / 10
                    if dist < floor and (worst is None or dist < worst[0]):
                        worst = (dist, unit, members, k, fr)
            if worst is None:
                return it
            dist, unit, members, k, fr = worst
            up = fr > 0.5                     # above the edge: push up, else down
            src, dst = (pair[k], k) if up else (k, pair[k])
            for c, m in members:
                idx = np.where(m & ~c["unk"] & (c["cat"] == src))[0]
                if len(idx):
                    c["cat"][idx[(it * 7919) % len(idx)]] = dst
                    break
        raise RuntimeError("mid_bin did not settle")

    def _units(self):
        for d in range(P.ND):
            c = self.y26[d]
            yield ("d", d), [(c, np.ones(c["n"], bool))]
        for b in range(P.B):
            yield ("b", b), [(c, c["band"] == b) for c in self.y26]

    def odds_mid_bin(self, floor=0.002):
        """keep the follow-up's pooled odds ratios (two decimals) and points gaps (one decimal) clear of a rounding edge by
        changing the fewest resolved cases' found destination between a graded and an ungraded one (NEET and EMP, HE and FE);
        both figures depend on the cases only through the count found in the destination, so the count is chosen first"""
        from scipy.optimize import brentq
        pair = {4: 3, 0: 1}
        for k in (4, 0):
            p = np.concatenate([np.round(self.y25[d]["alloc"][self.y25[d]["traced"], k], 4) for d in range(P.ND)])
            a = np.concatenate([(self.y25[d]["cat"][self.y25[d]["traced"]] == k) for d in range(P.ND)]).astype(float)
            li = logit(np.clip(p, 1e-9, 1 - 1e-9))
            for n in (0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5):
                tot = a.sum() + n
                o = np.exp(brentq(lambda x: expit(li + x).sum() - tot, -10, 10))
                g = (tot / len(a) - p.mean()) * 100
                if abs(o * 100 - np.floor(o * 100) - 0.5) / 100 >= floor and abs(g * 10 - np.floor(g * 10) - 0.5) / 10 >= 0.012:
                    break
            else:
                raise RuntimeError("odds_mid_bin found no count")
            src, dst = (pair[k], k) if n > 0 else (k, pair[k])
            left = abs(n)
            for d in range(P.ND):
                c = self.y25[d]
                idx = np.where(c["traced"] & (c["cat"] == src))[0]
                take = idx[:left]
                c["cat"][take] = dst; left -= len(take)
                if left == 0:
                    break
        return True
