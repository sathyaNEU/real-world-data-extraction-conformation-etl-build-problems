"""The ladder on the world's own numbers (before any file is cut): the validation list, the bridge-only route, the
constant-loss route and the golden under every curve form, for picking the seed."""
import sys

import numpy as np
from scipy.optimize import curve_fit

import params as P
import sim


def vhours(W, x):
    return np.array([d == x["vday"] for d in W["C"]["date"]])


def bhat(W):
    """each station-direction's sensitivity from its validation day: loops over video, less one"""
    out = {}
    for x in W["st"]:
        k = vhours(W, x)
        for d in x["dirs"]:
            out[(x["code"], d)] = W["rec"][(x["code"], d)][k].sum() / W["true"][(x["code"], d)]["q"][k].sum() - 1
    return out


def validation_errors(W):
    out = {}
    for x in W["st"]:
        k = vhours(W, x)
        out[x["code"]] = (sum(W["rec"][(x["code"], d)][k].sum() for d in x["dirs"]) /
                          sum(W["true"][(x["code"], d)]["q"][k].sum() for d in x["dirs"]) - 1)
    return out


def pair_points(W, bh, occ_of=None):
    xs, ys = [], []
    for b in P.BRIDGES:
        for d, up, dn in (("NB", b["south"], b["north"]), ("SB", b["north"], b["south"])):
            ru, rd = W["rec"][(up, d)], W["rec"][(dn, d)]
            ou = W["true"][(up, d)]["occ"] if occ_of is None else occ_of(up, d)
            k = (ru > 50) & (rd > 50)
            xs.append(ou[k])
            ys.append(1 - ru[k] / rd[k] * (1 + bh[(dn, d)]) / (1 + bh[(up, d)]))
    return np.concatenate(xs), np.concatenate(ys)


def fit(x, y, form):
    if form == "pl":
        f = lambda o, a, k0: a * np.clip(o - k0, 0, None)
        par, _ = curve_fit(f, x, y, p0=[0.006, 20.0])
        return lambda o: f(np.asarray(o, float), *par)
    if form == "power":
        f = lambda o, a, k0, p: a * np.clip(o - k0, 0, None) ** p
        par, _ = curve_fit(f, x, y, p0=[0.006, 20.0, 1.0], maxfev=40000)
        return lambda o: f(np.asarray(o, float), *par)
    if form == "quad":
        k = x > 22
        c = np.polyfit(x[k], y[k], 2)
        return lambda o: np.where(np.asarray(o) > 22, np.clip(np.polyval(c, o), 0, None), 0.0)
    if form == "lin22":
        k = x > 22
        c = np.polyfit(x[k], y[k], 1)
        return lambda o: np.where(np.asarray(o) > 22, np.clip(np.polyval(c, o), 0, None), 0.0)
    if form == "bins":
        e = np.arange(0, 64, 2.0)
        idx = np.clip(np.digitize(x, e), 1, len(e))
        u = np.unique(idx)
        cen = np.array([e[i - 1] + 1 for i in u])
        val = np.array([np.mean(y[idx == i]) for i in u])
        val = np.where(cen < 21, 0, val)
        return lambda o: np.interp(o, cen, val)
    raise ValueError(form)


def errors(W, bh, mh, occ_of=None):
    out = {}
    for x in W["st"]:
        num = den = 0.0
        for d in x["dirs"]:
            r = W["rec"][(x["code"], d)]
            o = W["true"][(x["code"], d)]["occ"] if occ_of is None else occ_of(x["code"], d)
            num += r.sum()
            den += (r / ((1 + bh[(x["code"], d)]) * (1 - mh(o)))).sum()
        out[x["code"]] = num / den - 1
    return out


def bridge_only(W, bh):
    """each bridge approach's error with the far approach as its reference in the direction it queues; every other
    station at its validation error"""
    out = validation_errors(W)
    for b in P.BRIDGES:
        for code, other in ((b["south"], b["north"]), (b["north"], b["south"])):
            x = [s for s in W["st"] if s["code"] == code][0]
            num = den = 0.0
            for d in x["dirs"]:
                r = W["rec"][(code, d)]
                upstream = (code == b["south"] and d == "NB") or (code == b["north"] and d == "SB")
                num += r.sum()
                den += (W["rec"][(other, d)].sum() / (1 + bh[(other, d)])) if upstream else r.sum() / (1 + bh[(code, d)])
            out[code] = num / den - 1
    return out


def const_loss(W, bh, x, y, cut=25.0):
    lq = float(np.mean(y[x > cut]))
    return errors(W, bh, lambda o: np.where(np.asarray(o) > cut, lq, 0.0))


def listed(e):
    return tuple(sorted(k for k, v in e.items() if abs(v) > P.TOLERANCE))


def report(seed, verbose=False):
    W = sim.world(seed)
    T = sim.truth(W)
    bh = bhat(W)
    x, y = pair_points(W, bh)
    G = errors(W, bh, fit(x, y, "pl"))
    fam = {f: errors(W, bh, fit(x, y, f)) for f in ("power", "quad", "lin22", "bins")}
    D0 = listed(validation_errors(W))
    R1 = listed(bridge_only(W, bh))
    R2 = listed(const_loss(W, bh, x, y))
    gl = listed(G)
    famok = all(listed(v) == gl for v in fam.values())
    printed = all(round(100 * v[k]) == round(100 * G[k]) for v in fam.values() for k in gl)
    margin = min(abs(abs(v) - P.TOLERANCE) for v in G.values())
    vq = sum(int(W["true"][(s["code"], d)]["queued"][vhours(W, s)].sum()) for s in W["st"] for d in s["dirs"])
    V = validation_errors(W)
    crisp = min(abs(abs(v) - P.TOLERANCE) for v in V.values()) >= 0.003
    ok = gl == listed(T) and famok and printed and len(set(gl) - set(D0)) >= 2 and len(set(D0) - set(gl)) >= 1 \
        and vq == 0 and crisp and 3 <= len(gl) <= 6
    print(seed, "OK" if ok else "--", "gold", gl, "def", D0, "R1", R1, "R2=G" if R2 == gl else ("R2", R2),
          "fam" if famok else "FAM!", "printed" if printed else "PRINT!", "margin %.4f" % margin, "vq", vq,
          "adds", sorted(set(gl) - set(D0)), "drops", sorted(set(D0) - set(gl)),
          "R1dist" if (R1 != D0 and R1 != gl) else "")
    if verbose:
        for s in W["st"]:
            print("   %-7s %-6s L %.4f b %+.4f val %+.4f gold %+.4f true %+.4f" % (
                s["code"], s["kind"], s["L"], s["b"], validation_errors(W)[s["code"]], G[s["code"]], T[s["code"]]))
    return ok


if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for s in range(a, b):
        report(s, verbose="-v" in sys.argv)
