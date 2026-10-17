"""Projecting a monetary-unit sample, and the standard evaluation of one.

The projection is the only thing the graded figure needs. The evaluation's other terms are needed
only for the conclusion at plan 4.3, and the reliability factors they use are standard domain
knowledge: no shipped file carries them, and the crudest bound they support already decides.
"""
import bisect
import math

import sim
import world as W

# Poisson reliability factors, one-sided upper bound, 95 per cent, 0 to 20 overstatements.
RF = [3.00, 4.75, 6.30, 7.76, 9.16, 10.52, 11.85, 13.15, 14.44, 15.71, 16.97,
      18.21, 19.45, 20.67, 21.89, 23.10, 24.31, 25.50, 26.70, 27.88, 29.07]


def split(lines, hits, interval=W.INTERVAL):
    """The tested lines, divided into the ones certain of selection and the rest."""
    tested = [lines[i] for i, _ in hits]
    cert = [t for t in tested if t[1] >= interval]
    prop = [t for t in tested if t[1] < interval]
    return tested, cert, prop


def projection(lines, hits, interval=W.INTERVAL, by_programme=False):
    """Each tainting at the interval, each line certain of selection at its own error."""
    tested, cert, prop = split(lines, hits, interval)
    if by_programme:
        out = {c: 0.0 for c in W.PROG_CODES}
        for t in prop:
            out[t[0]] += t[3] * interval
        for t in cert:
            out[t[0]] += t[1] * t[3]
        return out
    return sum(t[3] for t in prop) * interval + sum(t[1] * t[3] for t in cert)


def found(lines, hits):
    """The misstatement the testing actually found, which projects nothing."""
    return sum(t[1] * t[3] for t in split(lines, hits)[0])


def recorded_ratio(lines, hits):
    """The default path: the errors found scaled on recorded value."""
    tested = split(lines, hits)[0]
    return found(lines, hits) * sum(x[1] for x in lines) / sum(t[1] for t in tested)


def stratum_ratio(lines, hits, interval=W.INTERVAL):
    """Certainty lines at their own error, the rest scaled on their stratum's recorded value."""
    tested, cert, prop = split(lines, hits, interval)
    Vp = sum(x[1] for x in lines if x[1] < interval)
    vp = sum(t[1] for t in prop)
    return sum(t[1] * t[3] for t in cert) + sum(t[1] * t[3] for t in prop) * Vp / vp


def evaluation(lines, hits, interval=W.INTERVAL):
    """Projected misstatement, basic precision, incremental allowance and the upper limit."""
    tested, cert, prop = split(lines, hits, interval)
    each = sorted((t[3] * interval for t in prop if t[3] > 0), reverse=True)
    pm = sum(each) + sum(t[1] * t[3] for t in cert)
    bp = interval * RF[0]
    ia = sum((RF[j] - RF[j - 1] - 1.0) * p for j, p in enumerate(each, 1) if j < len(RF))
    return dict(pm=pm, bp=bp, ia=ia, uml=bp + pm + ia, n_taint=len(each),
                crude=pm + bp)


# ---------------------------------------------------------------- recovering the interval
def lattice(lines, hits, interval):
    """Every start that reproduces exactly this selection pattern at this interval.

    Lines in the first and last partial interval of the sweep carry no information, because
    whether they hold a selection turns on where the lattice begins and ends.
    """
    cum = sim.cumulative(lines)
    total = cum[-1]
    sel = {i for i, _ in hits}
    lo_e, hi_e = float(interval), total - interval
    keep = [(0.0, float(interval))]
    for i in sorted(sel):
        a, b = cum[i], cum[i + 1]
        if a < lo_e or b > hi_e or (b - a) >= interval:
            continue
        lo = a % interval
        hi = lo + (b - a)
        ivs = [(lo, min(hi, interval))] + ([(0.0, hi - interval)] if hi > interval else [])
        out = []
        for p, q in keep:
            for u, v in ivs:
                s0, s1 = max(p, u), min(q, v)
                if s1 > s0:
                    out.append((s0, s1))
        keep = out
        if not keep:
            return []
    for i in range(len(lines)):
        if i in sel:
            continue
        a, b = cum[i], cum[i + 1]
        if a < lo_e or b > hi_e:
            continue
        if (b - a) >= interval:
            return []
        lo = a % interval
        hi = lo + (b - a)
        ivs = [(lo, min(hi, interval))] + ([(0.0, hi - interval)] if hi > interval else [])
        out = []
        for p, q in keep:
            segs = [(p, q)]
            for u, v in ivs:
                nxt = []
                for s0, s1 in segs:
                    if v <= s0 or u >= s1:
                        nxt.append((s0, s1))
                    else:
                        if u > s0:
                            nxt.append((s0, u))
                        if v < s1:
                            nxt.append((v, s1))
                segs = nxt
            out.extend(segs)
        keep = [(x, y) for x, y in out if y - x > 1e-9]
        if not keep:
            return []
    return keep


def gaps(lines, hits, interval=W.INTERVAL):
    """The cumulated value between consecutive proportional selections, three conventions."""
    cum = sim.cumulative(lines)
    sel = sorted(i for i, _ in hits)
    ends, starts, mids = [], [], []
    prev = None
    for i in sel:
        if lines[i][1] >= interval:
            continue
        a, b = cum[i], cum[i + 1]
        if prev:
            ends.append(b - prev[1])
            starts.append(a - prev[0])
            mids.append((a + b) / 2.0 - (prev[0] + prev[1]) / 2.0)
        prev = (a, b)
    return ends, starts, mids


def routes(lines, hits, interval=W.INTERVAL):
    """Every interval an analyst would plausibly recover, and the figure each files."""
    import statistics
    cum = sim.cumulative(lines)
    V = cum[-1]
    sel = {i for i, _ in hits}
    tested, cert, prop = split(lines, hits, interval)
    e, s, m = gaps(lines, hits, interval)
    cert_min = min(t[1] for t in cert)
    unt_max = max(lines[i][1] for i in range(len(lines)) if i not in sel)
    out = [("the lattice", interval),
           ("the median gap, line end to line end", statistics.median(e)),
           ("the median gap, line start to line start", statistics.median(s)),
           ("the median gap, midpoint to midpoint", statistics.median(m)),
           ("the mean gap, midpoint to midpoint", statistics.mean(m)),
           ("recorded value over the count of tested lines", V / len(sel)),
           ("recorded value over the count of proportional tested lines", V / len(prop)),
           ("the certainty threshold", cert_min),
           ("the certainty bracket's lower end", unt_max),
           ("the certainty bracket's midpoint", (cert_min + unt_max) / 2.0)]
    return [(nm, si, projection(lines, hits, si)) for nm, si in out]


def r_grain(x):
    return int(math.floor(x / float(W.GRAIN) + 0.5) * W.GRAIN)
