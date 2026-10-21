"""The v5 ladder on the world's own numbers: the validation list, the queue loss alone, the cold miss alone, both, and
the truth, for picking the seed."""
import sys

import numpy as np
from scipy.optimize import curve_fit

import ladder as L
import params as P
import sim


def tcx2_days(W, code):
    return np.array([not sim.tcx4_on(code, day) for day in W["C"]["date"]])


def cold_points(W, bh, free_occ=18.0):
    """each mixed bridge pair's free-flow days: the TCX-2 side's count against the TCX-4 side's, each on its validated
    sensitivity, by the day's mean temperature"""
    C = W["C"]
    days = np.array(C["date"])
    xs, ys = [], []
    for b in P.BRIDGES:
        for d, up, dn in (("NB", b["south"], b["north"]), ("SB", b["north"], b["south"])):
            ru, rd = W["rec"][(up, d)], W["rec"][(dn, d)]
            ou, od = W["true"][(up, d)]["occ"], W["true"][(dn, d)]["occ"]
            t2u, t2d = tcx2_days(W, up), tcx2_days(W, dn)
            k = (ou < free_occ) & (od < free_occ) & (ru > 0) & (rd > 0) & (t2u != t2d)
            if not k.any():
                continue
            for day in sorted(set(days[k])):
                kk = k & (days == day)
                if kk.sum() < 6:
                    continue
                r = (ru[kk].sum() / (1 + bh[(up, d)])) / (rd[kk].sum() / (1 + bh[(dn, d)]))
                c = 1 - r if t2u[kk][0] else 1 - 1 / r
                xs.append(W["tmean"][day])
                ys.append(c)
    return np.array(xs), np.array(ys)


def cold_fit(x, y, form="knee"):
    if form == "knee":
        f = lambda t, a, k: np.clip(a * (k - t), 0, None)
        par, _ = curve_fit(f, x, y, p0=[0.004, 0.0])
        return lambda t: f(np.asarray(t, float), *par)
    if form == "knee0":
        f = lambda t, a: np.clip(a * (0.0 - t), 0, None) + 0 * t
        par, _ = curve_fit(lambda t, a: np.clip(a * (2.0 - t), 0, None), x, y, p0=[0.004])
        return lambda t: np.clip(par[0] * (2.0 - np.asarray(t, float)), 0, None)
    if form == "bins":
        e = np.arange(-20, 36, 2.0)
        idx = np.clip(np.digitize(x, e), 1, len(e))
        u = np.unique(idx)
        cen = np.array([e[i - 1] + 1 for i in u])
        val = np.array([np.mean(y[idx == i]) for i in u])
        val = np.where(cen > 6, 0.0, np.clip(val, 0, None))
        return lambda t: np.interp(t, cen, val)
    raise ValueError(form)


def chour(W, code, cf):
    """the cold miss each hour of a station, by the controller in force and the day's mean temperature"""
    C = W["C"]
    tm = np.array([W["tmean"][day] for day in C["date"]])
    t2 = tcx2_days(W, code)
    return np.where(t2, cf(tm), 0.0)


def pair_points(W, bh, cf):
    xs, ys = [], []
    for b in P.BRIDGES:
        for d, up, dn in (("NB", b["south"], b["north"]), ("SB", b["north"], b["south"])):
            ru, rd = W["rec"][(up, d)], W["rec"][(dn, d)]
            ou = W["true"][(up, d)]["occ"]
            cu, cd = chour(W, up, cf), chour(W, dn, cf)
            k = (ru > 50) & (rd > 50)
            xs.append(ou[k])
            ys.append(1 - (ru[k] / ((1 + bh[(up, d)]) * (1 - cu[k]))) / (rd[k] / ((1 + bh[(dn, d)]) * (1 - cd[k]))))
    return np.concatenate(xs), np.concatenate(ys)


def errors(W, bh, mh, cf):
    out = {}
    for x in W["st"]:
        num = den = 0.0
        c = chour(W, x["code"], cf)
        for d in x["dirs"]:
            r = W["rec"][(x["code"], d)]
            o = W["true"][(x["code"], d)]["occ"]
            num += r.sum()
            den += (r / ((1 + bh[(x["code"], d)]) * (1 - mh(o)) * (1 - c))).sum()
        out[x["code"]] = num / den - 1
    return out


ZERO = lambda t: np.zeros_like(np.asarray(t, float))


def routes(W, mform="pl", cform="knee"):
    bh = L.bhat(W)
    xc, yc = cold_points(W, bh)
    cf = cold_fit(xc, yc, cform)
    x, y = pair_points(W, bh, cf)
    G = errors(W, bh, L.fit(x, y, mform), cf)
    xa, ya = pair_points(W, bh, ZERO)
    A = errors(W, bh, L.fit(xa, ya, mform), ZERO)
    B = errors(W, bh, ZERO, cf)
    return dict(G=G, A=A, B=B, D=L.validation_errors(W), cf=cf)


def report(seed, verbose=False):
    W = sim.world(seed)
    T = sim.truth(W)
    R = routes(W)
    gl = L.listed(R["G"])
    fam = {}
    for mf in ("pl", "power", "quad", "lin22", "bins"):
        for cf in ("knee", "knee0", "bins"):
            if (mf, cf) != ("pl", "knee"):
                fam[(mf, cf)] = L.listed(routes(W, mf, cf)["G"])
    famok = all(v == gl for v in fam.values())
    lists = {k: L.listed(R[k]) for k in ("D", "A", "B")}
    margin = min(abs(abs(v) - P.TOLERANCE) for v in R["G"].values())
    tmargin = min(abs(abs(v) - P.TOLERANCE) for v in T.values())
    distinct = len({gl, lists["D"], lists["A"], lists["B"]}) == 4
    ok = gl == L.listed(T) and famok and distinct and margin >= 0.008 and tmargin >= 0.006 and 3 <= len(gl) <= 7
    print(seed, "OK" if ok else "--", "gold", gl, "D", lists["D"], "A", lists["A"], "B", lists["B"],
          "fam" if famok else "FAM!" + str([k for k, v in fam.items() if v != gl][:3]), "margin %.4f tmargin %.4f"
          % (margin, tmargin), "truth" if gl == L.listed(T) else "TRUTH!" + str(L.listed(T)))
    if verbose:
        for x in W["st"]:
            s = x["code"]
            print("   %-7s %-6s %s L %.4f b %+.4f D %+.4f A %+.4f B %+.4f G %+.4f T %+.4f" % (
                s, x["kind"], "T4" if s in P.NEW_CONTROLLERS else "T2", x["L"], x["b"], R["D"][s], R["A"][s], R["B"][s],
                R["G"][s], T[s]))
        print("   cold fit at -10, -5, 0, 2:", [round(float(R["cf"](np.array([t]))[0]), 4) for t in (-10, -5, 0, 2)])
    return ok


if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for s in range(a, b):
        report(s, verbose="-v" in sys.argv)
