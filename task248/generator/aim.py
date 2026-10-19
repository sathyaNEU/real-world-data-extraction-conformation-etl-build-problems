"""task248 aim: hand-run tuning of each plant's wave amplitudes so every plant's winter 2027 episode count stands
clear of the High and Low lines on the published basis and on the shed load."""
import numpy as np

import estim as E
import params as P
import sim


def bases(W, Hh, comps, k20=P.K20, theta=P.THETA):
    dates = [c["d"] for c in comps]
    out = {}
    for s in range(P.NPLANT):
        pub = [c["load"][s] for c in comps]
        shed = [c["load"][s] + E.LOG10E * sim.k(c["Tw"][s], k20, theta) * W["tt"][s] for c in comps]
        out[s] = (E.levels(dates, pub), E.levels(dates, shed))
    return out


def margins(lev, step=0.0025, span=0.4):
    """the smallest shift, added to every week's level, that moves the plant's winter episode count"""
    n0 = E.episodes(lev)[0]
    for i in range(1, int(span / step) + 1):
        for sgn in (1, -1):
            d = sgn * i * step
            if E.episodes({w: v + d for w, v in lev.items()})[0] != n0:
                return i * step
    return span


def series(lev):
    return " ".join("%.2f" % lev[w] for w in sorted(lev) if P.REF[1] < w <= P.WINTER[1])


def table(W, Hh, comps):
    B = bases(W, Hh, comps)
    tp = ts = 0
    for s in range(P.NPLANT):
        (lp, bp), (ls, bs) = B[s]
        np_, _ = E.episodes(lp)
        ns, _ = E.episodes(ls)
        tp += np_
        ts += ns
        print("%s %5.0f min  pub %d  shed %d   margin pub %.3f shed %.3f" % (P.PLANTS[s][0], W["tt"][s] * 60, np_, ns,
                                                                          margins(lp), margins(ls)))
    print("total published %d, shed %d" % (tp, ts))


if __name__ == "__main__":
    W = sim.make()
    Hh = sim.hourly(W)
    comps = sim.composites(W, Hh)
    table(W, Hh, comps)


def counts(W, comps, corr):
    """per plant episode count and margin on loads restored by corr(s, comp) (log10 added to each composite's load)"""
    dates = [c["d"] for c in comps]
    out = []
    for s in range(P.NPLANT):
        vals = [c["load"][s] + corr(s, c) for c in comps]
        lev, base = E.levels(dates, vals)
        out.append((E.episodes(lev)[0], margins(lev)))
    return out


def variants(W, Hh, comps, rows):
    import fit
    tt = W["tt"]
    V = {}
    V["published"] = lambda s, c: 0.0
    for name, f in (("linear", fit.linear), ("arrhenius", fit.arrhenius), ("per_plant", fit.per_plant)):
        for temp in ("Tin", "Tup"):
            g = f(rows, temp)
            V["%s/%s" % (name, temp)] = (lambda g: lambda s, c: E.LOG10E * float(g(c["Tw"][s])) * tt[s])(g)
    V["truth"] = lambda s, c: E.LOG10E * float(sim.k(c["Tw"][s])) * tt[s]
    gc = fit.constant(rows)
    V["constant"] = lambda s, c: E.LOG10E * float(gc(c["Tw"][s])) * tt[s]
    ca = fit.additive(rows)
    V["additive"] = lambda s, c: -E.LOG10E * (ca[1] * tt[s] + ca[2] * c["Tw"][s])
    ga = fit.arrhenius(rows)
    study_idx = {i for i, p in enumerate(P.PLANTS) if p[0] in sim.STUDY_PLANTS}
    V["study plants only"] = lambda s, c: E.LOG10E * float(ga(c["Tw"][s])) * tt[s] if s in study_idx else 0.0
    out = {k: counts(W, comps, f) for k, f in V.items()}
    # PMMoV normalisation: log10 N1 over PMMoV, no decay correction
    dates = [c["d"] for c in comps]
    pm = []
    for s in range(P.NPLANT):
        vals = [np.log10(c["conc"][s] / c["pconc"][s]) for c in comps]
        lev, base = E.levels(dates, vals)
        pm.append((E.episodes(lev)[0], margins(lev)))
    out["pmmov"] = pm
    return out
