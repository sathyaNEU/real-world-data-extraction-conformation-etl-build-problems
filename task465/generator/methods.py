"""The expected loss of each county cover under each route a solver can take, from the current estimates.

The golden: each crop year's county yield as the service estimated it; in a year the service withheld the county's
dryland estimate, the county's harvested acres and production are the district's less the district's published
counties', and the yield is their ratio. Every year's yield is brought to 2027 by adding the term sheet's trend per
year times the years to 2027; the cover pays the share of its liability by which that yield falls short of the trigger
(90 per cent of the expected 2027 yield), and the expected loss is the average share over the 35 crop years.
"""
import numpy as np

import sim as S
import world as W

NI = "NON-IRRIGATED"


def county_series(cty, c):
    v = cty[(c, "SORGHUM", NI)]
    return v["harvested"], v["production"]


def published_yield(cty, pub, c):
    h, p = county_series(cty, c)
    m = pub[(c, "SORGHUM", NI)]
    return {int(y): round(float(p[i] / h[i]), 1) for i, y in enumerate(S.YEARS) if m[i]}


def district_yield(dist, d):
    v = dist[(d, "SORGHUM", NI)]
    return {int(y): round(float(v["production"][i] / v["harvested"][i]), 1) for i, y in enumerate(S.YEARS)}


def recovered(cty, dist, pub, c):
    """The withheld years from the district's totals less its published counties."""
    d = W.COUNTIES[c][1]
    dv = dist[(d, "SORGHUM", NI)]
    peers = [k for k, v in W.COUNTIES.items() if v[1] == d and k != c]
    out = {}
    for i, y in enumerate(S.YEARS):
        if pub[(c, "SORGHUM", NI)][i]:
            continue
        for k in peers:
            assert pub[(k, "SORGHUM", NI)][i], (k, y)
        h = dv["harvested"][i] - sum(cty[(k, "SORGHUM", NI)]["harvested"][i] for k in peers)
        p = dv["production"][i] - sum(cty[(k, "SORGHUM", NI)]["production"][i] for k in peers)
        out[int(y)] = dict(harvested=float(h), production=float(p), yld=round(float(p / h), 1))
    return out


def theil_sen(xs, ys):
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    sl = [(ys[j] - ys[i]) / (xs[j] - xs[i]) for i in range(len(xs)) for j in range(i + 1, len(xs))]
    m = float(np.median(sl))
    a = float(np.median(ys - m * xs))
    return a, m


def term_sheet(cty, pub):
    """Quillfield Re's expected 2027 yield and trend per county: a Theil-Sen line through the published years."""
    out = {}
    for c in W.MEMBERS:
        py = published_yield(cty, pub, c)
        a, m = theil_sen(list(py), list(py.values()))
        out[c] = dict(expected=round(a + m * 2027, 1), trend=round(m, 2))
    return out


def loss_share(c, y, v, ts):
    e, b = ts[c]["expected"], ts[c]["trend"]
    trig = W.COVERAGE * e
    return min(1.0, max(0.0, (trig - (v + b * (2027 - y))) / trig))


def routes(cty, dist, pub, ts):
    """{route: {county: {year: yield}}} for every route on the ladder."""
    out = {}
    for c in W.MEMBERS:
        d = W.COUNTIES[c][1]
        py = published_yield(cty, pub, c)
        dy = district_yield(dist, d)
        rec = recovered(cty, dist, pub, c)
        pubyears = sorted(py)
        ratio = float(np.mean([py[y] / dy[y] for y in pubyears]))
        bb, aa = np.polyfit([dy[y] for y in pubyears], [py[y] for y in pubyears], 1)
        worst = min(py.values())
        peers = [k for k, v in W.COUNTIES.items() if v[1] == d and k != c]

        def peer_yield(y):
            i = y - W.Y0
            h = sum(cty[(k, "SORGHUM", NI)]["harvested"][i] for k in peers)
            p = sum(cty[(k, "SORGHUM", NI)]["production"][i] for k in peers)
            return round(float(p / h), 1)
        fills = {
            "drop": None,
            "district": lambda y: dy[y],
            "peers": peer_yield,
            "ratio": lambda y: ratio * dy[y],
            "regress": lambda y: float(aa + bb * dy[y]),
            "worst": lambda y: worst,
            "zero": lambda y: 0.0,
            "golden": lambda y: rec[y]["yld"],
        }
        for name, f in fills.items():
            ser = dict(py)
            if f is not None:
                for y in rec:
                    ser[y] = f(y)
            out.setdefault(name, {})[c] = ser
    return out


def expected_loss(series, ts):
    return {c: 100.0 * float(np.mean([loss_share(c, y, v, ts) for y, v in sorted(s.items())]))
            for c, s in series.items()}


def calls(el, quotes):
    return {c: quotes[c] <= W.BUY_MULTIPLE * el[c] + 1e-12 for c in W.MEMBERS}
