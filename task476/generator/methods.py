"""The routes from published estimates to each candidate 2020 tract's verdict: the Bureau's formulas for a derived
proportion and for a sum, the change test at 90 per cent, and the ways the 2014 to 2018 rate is carried to the 2020
tracts. Reads only Est objects, so the generator and the verifier share it through their own readers."""
import math

Z = 1.645


def rss(vals):
    return math.sqrt(sum(v * v for v in vals))


def proportion(x, mx, u, mu, ratio=False):
    """The Bureau's derived-proportion margin (the ratio formula when the radicand is negative, or when asked)."""
    p = x / u
    rad = mx ** 2 - p ** 2 * mu ** 2
    if ratio or rad < 0:
        rad = mx ** 2 + p ** 2 * mu ** 2
    return p, math.sqrt(rad) / u


def z(p1, m1, p2, m2):
    return (p2 - p1) / math.sqrt((m1 / Z) ** 2 + (m2 / Z) ** 2)


def summed(ests):
    """A sum of published estimates: counts added, margins as the root sum of squares."""
    return (sum(e.x for e in ests), rss([e.mx for e in ests]), sum(e.u for e in ests), rss([e.mu for e in ests]))


def earlier(route, tract20, parents, bg18, tr18, ratio=False):
    """The 2014-18 rate and margin carried to one 2020 tract.
    parents: [(2010 tract code, share of the parent's area or 2010 population in this 2020 tract)]
    bg18: the 2010 block groups whose ground lies in this 2020 tract (Est objects); tr18: {2010 code: Est}."""
    if route == "golden":
        return proportion(*summed(bg18), ratio=ratio)
    if route == "parent":
        # the counts scaled by each parent's share: the parent's rate, its margins scaled with it
        x = sum(tr18[c].x * s for c, s in parents)
        u = sum(tr18[c].u * s for c, s in parents)
        mx = rss([tr18[c].mx * s for c, s in parents])
        mu = rss([tr18[c].mu * s for c, s in parents])
        return proportion(x, mx, u, mu, ratio=ratio)
    raise ValueError(route)
