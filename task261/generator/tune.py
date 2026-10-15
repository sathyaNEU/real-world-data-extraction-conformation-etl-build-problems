"""The design's tuning: every route's ratio of each neighbouring difference to its standard error, computed from the
survey arrays as the public files carry them, for a candidate set of net worth factors (common.TUNE)."""
from __future__ import annotations

import sys

import numpy as np

import common as K
import world as W


def wmed(x, W_):
    o = np.argsort(x, kind="stable")
    xs = x[o]
    c = np.cumsum(W_[:, o], axis=1)
    return xs[(c >= c[:, -1:] / 2).argmax(1)]


def routes(d, nboot=200):
    nw = d["nw"].astype(float)
    w = d["wgt"]
    R = d["repw"]
    older = np.minimum(d["older"], 85)
    out = {}
    for basis, age in (("older", d["older"]), ("ref", d["ref"])):
        b = K.band_of(age)
        est = np.array([[wmed(nw[m][b == g], w[None, b == g])[0] for g in range(6)] for m in range(5)])
        rep = np.stack([wmed(nw[0][b == g], R[:, b == g]) for g in range(6)], 1)
        th = est.mean(0)
        B = est.var(0, ddof=1)
        U = ((rep - est[0]) ** 2).mean(0)
        T = U + 1.2 * B
        zc, zq, zs = [], [], []
        srs = []
        for g in range(6):
            x = nw[0][b == g]
            ww = w[b == g]
            o = np.argsort(x)
            xs = x[o]
            c = np.cumsum(ww[o]) / ww.sum()
            vp = 0.25 * (ww ** 2).sum() / ww.sum() ** 2
            lo = np.interp(0.5 - 1.96 * np.sqrt(vp), c, xs)
            hi = np.interp(0.5 + 1.96 * np.sqrt(vp), c, xs)
            srs.append(((hi - lo) / (2 * 1.96)) ** 2 + 1.2 * B[g])
        for g in range(5):
            dd = th[g + 1] - th[g]
            Ud = (((rep[:, g + 1] - rep[:, g]) - (est[0, g + 1] - est[0, g])) ** 2).mean()
            Bd = (est[:, g + 1] - est[:, g]).var(ddof=1)
            zc.append(dd / np.sqrt(Ud + 1.2 * Bd))
            zq.append(dd / np.sqrt(T[g] + T[g + 1]))
            zs.append(dd / np.sqrt(srs[g] + srs[g + 1]))
        out[basis] = dict(med=th, zc=np.array(zc), zq=np.array(zq), zs=np.array(zs))
    # a bootstrap over households, ignoring the areas (200 resamples, implicate 1)
    b = K.band_of(d["older"])
    r = np.random.default_rng(5)
    n = len(w)
    bs = []
    for _ in range(nboot):
        i = r.integers(0, n, n)
        bs.append([wmed(nw[0][i][b[i] == g], w[None, i][:, b[i] == g])[0] for g in range(6)])
    bs = np.array(bs)
    est0 = np.array([wmed(nw[0][b == g], w[None, b == g])[0] for g in range(6)])
    estm = np.array([[wmed(nw[m][b == g], w[None, b == g])[0] for g in range(6)] for m in range(5)])
    th = estm.mean(0)
    zb = []
    for g in range(5):
        dd = th[g + 1] - th[g]
        Ud = (((bs[:, g + 1] - bs[:, g]) - (est0[g + 1] - est0[g])) ** 2).mean()
        zb.append(dd / np.sqrt(Ud + 1.2 * (estm[:, g + 1] - estm[:, g]).var(ddof=1)))
    out["older"]["zb"] = np.array(zb)
    return out


def segments(z):
    s = K.BAND_SHORT[0]
    for g in range(5):
        s += (" | " if abs(z[g]) > 1.96 else " + ") + K.BAND_SHORT[g + 1]
    return s


if __name__ == "__main__":
    k = [float(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else None
    d = W.survey(k)
    o = routes(d)
    print("medians (older):", np.round(o["older"]["med"] / 1000, 1))
    for basis in ("older", "ref"):
        for key in ("zc", "zq", "zs") + (("zb",) if basis == "older" else ()):
            print("%-5s %s %s  %s" % (basis, key, np.round(o[basis][key], 2), segments(o[basis][key])))
