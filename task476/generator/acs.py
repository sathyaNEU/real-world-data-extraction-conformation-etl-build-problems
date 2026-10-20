"""The Bureau's five-year estimates as published: each block group's poverty universe and count below poverty with
margins of error, in 2014 to 2018 on the 2010 block groups and in 2019 to 2023 on the 2020 ones, and each tract's as
the sum of its block groups (detailed tables are additive across geographies; a tract's margin comes from the
replicate weights, a little under the root sum of its block groups')."""
import math

import geo as G
import world as W


def _se(n, p):
    f = W.SAMPLE_FRACTION
    return math.sqrt(W.DESIGN_EFFECT * n * p * (1 - p) * (1 - f) / f)


class Est:
    """One published estimate pair: universe and below poverty, with margins."""
    def __init__(self, u, mu, x, mx):
        self.u, self.mu, self.x, self.mx = u, mu, x, mx

    @property
    def rate(self):
        return self.x / self.u


def bg_estimates(ts):
    """{(period, geoid): Est} for every block group, 2014-18 on 2010 geoids and 2019-23 on 2020 geoids."""
    out = {}
    for t in ts:
        for b in t.bgs:
            for per, n, p, gid in ((1, b.u1, b.p1, b.geoid10), (2, b.u2, b.p2, b.geoid20)):
                rng = G.rng_for("est", gid, per)
                se = _se(n, p)
                k = W.CANDIDATE_NOISE if b.cand else 1.0
                x = int(round(n * p + k * se * float(rng.normal())))
                x = max(0, min(n, x))
                mu = int(round(n * float(rng.uniform(0.045, 0.085))))
                u = int(round(n + 0.3 * mu / W.Z90 * float(rng.normal())))
                mx = int(round(W.Z90 * _se(n, max(x, 1) / n) * float(rng.uniform(0.94, 1.06))))
                out[(per, gid)] = Est(u, mu, x, mx)
    return out


def tract_estimates(ts, bge):
    """{(period, tract code): Est}: 2014-18 on the 2010 tracts, 2019-23 on the 2020 tracts."""
    out = {}
    for t in ts:
        groups = [(1, t.code10, [b.geoid10 for b in t.bgs])] + \
                 [(2, code, [b.geoid20 for b in bgs]) for code, bgs in t.children]
        for per, code, gids in groups:
            es = [bge[(per, g)] for g in gids]
            rng = G.rng_for("tmoe", per, code)
            fu, fx = float(rng.uniform(0.80, 0.92)), float(rng.uniform(0.84, 0.95))
            u = sum(e.u for e in es)
            x = sum(e.x for e in es)
            mu = int(round(fu * math.sqrt(sum(e.mu ** 2 for e in es))))
            mx = int(round(fx * math.sqrt(sum(e.mx ** 2 for e in es))))
            out[(per, code)] = Est(u, mu, x, mx)
    return out
