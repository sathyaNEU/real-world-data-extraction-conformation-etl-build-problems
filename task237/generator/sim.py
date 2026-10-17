"""The world behind task237's pack: each translated version's pilot respondents, their connectedness and their answers
to the twelve BCS-12 items. A respondent's answer to an item comes from their connectedness through the item's loading
in that translation; in six translations the negatively worded items also share a wording factor (how a respondent
answers the translation's negation, whatever their connectedness). The valid completes are the respondents who
finished the interview and those who reached the end of the module and left in the background questions, and, for
the interviewer-administered pilots, the interviews at reissued and revisited cases. Besides them the vendors' files
carry retakes (some from a second account the panel merged afterwards), respondents who switched to English, partials,
screen-outs and soft-launch entries (online), and pretest, unconfirmed and broken-off interviews
(interviewer-administered). The clean truth (each version's answers before any file is written, and the trait's share
of each version's score in the generating model) stays here for the checks."""

VALID = ("valid", "past", "replacement", "revisit")
import numpy as np
import pandas as pd

import params as P

KINDS = ("valid", "past", "replacement", "revisit", "retake", "merged", "switch", "partial", "screenout", "soft",
         "pretest", "unconfirmed", "inside")


def keyed(rng, n, lam, dlt, shift, eta=None, W=None):
    """five-point answers in the keyed direction (higher, more connected) from the continuous responses"""
    p = len(lam)
    eta = rng.standard_normal(n) if eta is None else eta
    W = rng.standard_normal(n) if W is None else W
    th = 1 - lam ** 2 - dlt ** 2
    Y = np.outer(eta, lam) + np.outer(W, dlt) + rng.standard_normal((n, p)) * np.sqrt(th)
    X = np.zeros((n, p), dtype=int)
    cuts = np.array(P.CUTS)
    for i in range(p):
        X[:, i] = 1 + np.searchsorted(cuts + shift[i], Y[:, i])
    return X, eta, W


def loadings(pos, neg, wording):
    lam = np.zeros(12); lam[P.POS] = pos; lam[P.NEG] = neg
    dlt = np.zeros(12); dlt[P.NEG] = wording
    return lam, dlt


def model_trait_share(lam, dlt):
    """the trait's share of the continuous total score's variance in the generating model (the keyed sum)"""
    th = 1 - lam ** 2 - dlt ** 2
    return lam.sum() ** 2 / (lam.sum() ** 2 + dlt.sum() ** 2 + th.sum())


class World:
    def __init__(self, seed=P.WORLD_SEED):
        self.seed = seed
        self.base_shift = np.random.default_rng(seed).normal(0, 0.25, 12)

    def _rng(self, k, j):
        return np.random.default_rng(self.seed * 1000 + k * 37 + j)

    def missing(self, rng, eta, n):
        """items left unanswered, commoner among the less connected"""
        pr = np.clip(P.ITEM_MISSING * np.exp(-P.MISSING_SLOPE * eta), 0, 0.2)
        return rng.random((n, 12)) < pr[:, None]

    def version(self, k):
        code, lang, vendor, n, pos, neg, wording = P.VERSIONS[k]
        rng = self._rng(k, 0)
        lam, dlt = loadings(pos, neg, wording)
        shift = self.base_shift + rng.normal(0, 0.12, 12) + P.LEVEL.get(code, 0.0) + P.NUDGE.get(code, 0.0)
        X, eta, W = keyed(rng, n, lam, dlt, shift)
        rows = [dict(kind="valid", X=X[i], miss=m, eta=eta[i]) for i, m in enumerate(self.missing(rng, eta, n))]
        if vendor == "NCP":
            # retakes: the same person a second time, the same connectedness and wording tendency
            r = rng.choice(n, size=int(round(n * P.RETAKE)), replace=False)
            X2, _, _ = keyed(rng, len(r), lam, dlt, shift, eta[r], W[r])
            for j, i in enumerate(r):
                rows.append(dict(kind="retake", X=X2[j], miss=self.missing(rng, eta[[i]], 1)[0], eta=eta[i], of=int(i)))
            # respondents who switched the questionnaire to English: the source version's items and loadings; people
            # at ease in English are a little more connected
            ns = int(round(n * P.SWITCH))
            le, de = loadings(*P.ENGLISH, 0.0)
            X3, e3, _ = keyed(rng, ns, le, de, self.base_shift, eta=rng.standard_normal(ns) + 0.5)
            rows += [dict(kind="switch", X=X3[i], miss=self.missing(rng, e3[[i]], 1)[0], eta=e3[i]) for i in range(ns)]
            # partials: broke off before the end of the module
            npart = int(round(n * P.PARTIAL))
            X4, e4, _ = keyed(rng, npart, lam, dlt, shift, eta=rng.standard_normal(npart) - 0.4)
            for i in range(npart):
                stop = int(rng.integers(2, 11))
                m = np.zeros(12, bool); m[stop:] = True
                rows.append(dict(kind="partial", X=X4[i], miss=m, eta=e4[i], stop=stop))
            rows += [dict(kind="screenout", X=np.zeros(12, int), miss=np.ones(12, bool), eta=np.nan)
                     for _ in range(int(round(n * P.SCREENOUT)))]
            # reached the end of the module and left in the background questions (a little less connected)
            npast = int(round(n * P.PAST_MODULE["NCP"]))
            X6, e6, _ = keyed(rng, npast, lam, dlt, shift, eta=rng.standard_normal(npast) - 0.3)
            for i in range(npast):
                rows.append(dict(kind="past", X=X6[i], miss=self.missing(rng, e6[[i]], 1)[0], eta=e6[i],
                                 leave=int(rng.integers(0, 3))))
            # a second completion from a second account of the same member, which the panel merges afterwards
            nm = int(round(n * P.MERGED))
            r2 = rng.choice(np.setdiff1d(np.arange(n), r), size=nm, replace=False)
            X7, _, _ = keyed(rng, nm, lam, dlt, shift, eta[r2], W[r2])
            for j, i in enumerate(r2):
                rows.append(dict(kind="merged", X=X7[j], miss=self.missing(rng, eta[[i]], 1)[0], eta=eta[i], of=int(i)))
            # entries on the soft-launch evening before the pilot's first day
            nsoft = int(round(n * P.SOFT))
            X8, e8, _ = keyed(rng, nsoft, lam, dlt, shift)
            rows += [dict(kind="soft", X=X8[i], miss=self.missing(rng, e8[[i]], 1)[0], eta=e8[i]) for i in range(nsoft)]
        else:
            # the draft translation's pretest, recruited through community organisations
            npre = int(rng.integers(*P.PRETEST_N))
            X5, e5, _ = keyed(rng, npre, lam, dlt, shift, eta=rng.standard_normal(npre) + 0.35)
            rows += [dict(kind="pretest", X=X5[i], miss=self.missing(rng, e5[[i]], 1)[0], eta=e5[i]) for i in range(npre)]
            # interviews the back-check could not confirm: another interview's answers copied with a few changed
            nun = int(round(n * P.NOT_CONFIRMED / (1 - P.NOT_CONFIRMED)))
            for i in range(nun):
                src = int(rng.integers(n))
                x = X[src].copy()
                for j in rng.choice(12, size=int(rng.integers(1, 4)), replace=False):
                    x[j] = int(np.clip(x[j] + rng.choice([-1, 1]), 1, 5))
                rows.append(dict(kind="unconfirmed", X=x, miss=np.zeros(12, bool), eta=eta[src], of=src))
            # interviews broken off in the background questions (the module finished) and inside the module
            npast = int(round(n * P.PAST_MODULE["FLR"]))
            X6, e6, _ = keyed(rng, npast, lam, dlt, shift, eta=rng.standard_normal(npast) - 0.3)
            for i in range(npast):
                rows.append(dict(kind="past", X=X6[i], miss=self.missing(rng, e6[[i]], 1)[0], eta=e6[i],
                                 leave=int(rng.integers(0, 3))))
            nin = int(round(n * P.INSIDE_FLR))
            X9, e9, _ = keyed(rng, nin, lam, dlt, shift, eta=rng.standard_normal(nin) - 0.4)
            for i in range(nin):
                rows.append(dict(kind="inside", X=X9[i], miss=self.missing(rng, e9[[i]], 1)[0], eta=e9[i],
                                 stop=int(rng.integers(3, 12))))
            # cases of unconfirmed interviews reissued to another interviewer: a new interview at the same case
            unc = [i for i, rw in enumerate(rows) if rw["kind"] == "unconfirmed"]
            rep = [u for u, p in zip(unc, rng.random(len(unc))) if p < P.REISSUE]
            X10, e10, _ = keyed(rng, len(rep), lam, dlt, shift)
            for j, u in enumerate(rep):
                rows.append(dict(kind="replacement", X=X10[j], miss=self.missing(rng, e10[[j]], 1)[0], eta=e10[j], case=u))
            # cases whose interview broke off inside the module, revisited by another interviewer for a full interview
            ins = [i for i, rw in enumerate(rows) if rw["kind"] == "inside"]
            rev = [u for u, p in zip(ins, rng.random(len(ins))) if p < P.REVISIT]
            X11, e11, _ = keyed(rng, len(rev), lam, dlt, shift)
            for j, u in enumerate(rev):
                rows.append(dict(kind="revisit", X=X11[j], miss=self.missing(rng, e11[[j]], 1)[0], eta=e11[j], case=u))
        out = pd.DataFrame(rows)
        out["version"] = code
        out["vendor"] = vendor
        self.truth[code] = dict(trait_share=model_trait_share(lam, dlt), lam=lam, dlt=dlt, shift=shift)
        return out

    def build(self):
        self.truth = {}
        self.respondents = pd.concat([self.version(k) for k in range(len(P.VERSIONS))], ignore_index=True)
        return self.respondents

    def english(self, n=2416):
        """the source version's validation sample, for the technical manual's figures"""
        rng = self._rng(99, 0)
        le, de = loadings(*P.ENGLISH, 0.0)
        X, _, _ = keyed(rng, n, le, de, self.base_shift)
        return X


def make(seed=P.WORLD_SEED):
    W = World(seed)
    W.build()
    return W
