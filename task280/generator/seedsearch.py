"""Seed search for task280 on the latent world: the truth and the load-conditioned family must name one set of hubs
at a safe margin from the line, and the share of tests (overall, by hour, by night) and every skip counted as a
failure must each name another set."""
from __future__ import annotations

import sys

import numpy as np

import common as K
import world as W


def routes(w):
    """each household's share by route, computed on the latent tests (the pack's readers recompute them)"""
    h, d, r, m, q, mbps = w.tests()
    pkt = w.wkday[d] & np.isin(q, W.PEAK_Q)
    h, d, r, q, mbps = h[pkt], d[pkt], r[pkt], q[pkt], mbps[pkt]
    below = mbps < K.STANDARD * w.down[h, d]
    load = w.U[w.hh_node[h], d, q]
    NH = w.NH
    out = {k: np.zeros(NH) for k in ("tests", "hour", "night", "skipfail", "load20", "load10", "thresh")}
    order = np.argsort(h, kind="stable")
    st = np.searchsorted(h[order], np.arange(NH))
    en = np.searchsorted(h[order], np.arange(NH), side="right")
    wk = np.where(w.wkday)[0]
    for i in range(NH):
        ix = order[st[i]:en[i]]
        b, l, dd, rr = below[ix], load[ix], d[ix], r[ix]
        out["tests"][i] = b.mean()
        wt = 1.0 / np.bincount(rr, minlength=8)[rr]
        out["hour"][i] = (wt * b).sum() / wt.sum()
        wt = 1.0 / np.bincount(dd, minlength=K.DAYS)[dd]
        out["night"][i] = (wt * b).sum() / wt.sum()
        sched = len(wk) * (K.PEAK_TO - K.PEAK_FROM)
        out["skipfail"][i] = (b.sum() + sched - len(ix)) / sched
        allu = w.U[w.hh_node[i]][wk][:, W.PEAK_Q].ravel()
        for nb, key in ((20, "load20"), (10, "load10")):
            edges = np.linspace(0, 1, nb + 1)
            tb = np.clip(np.digitize(l, edges), 1, nb)
            ub = np.clip(np.digitize(allu, edges), 1, nb)
            tgt = np.bincount(ub, minlength=nb + 2) / ub.size
            have = np.bincount(tb, minlength=nb + 2)
            wv = np.where(have > 0, tgt / np.maximum(have, 1), 0.0)
            miss = tgt[have == 0].sum()
            top = b[l >= np.quantile(l, 0.9)].mean()
            out[key][i] = (wv[tb] * b).sum() / max(wv[tb].sum(), 1e-12) * (1 - miss) + miss * top
        o = np.argsort(l)
        vb = b[o].astype(int)
        c0 = np.concatenate([[0], np.cumsum(vb == 0)])
        c1 = np.concatenate([np.cumsum((vb == 1)[::-1])[::-1], [0]])
        j = int(np.argmax(c0 + c1))
        t = (l[o][j - 1] + l[o][j]) / 2 if 0 < j < len(o) else (-1.0 if j == 0 else 2.0)
        out["thresh"][i] = (allu > t).mean()
    return out


def hub_shares(w, per_hh):
    return np.array([100 * per_hh[w.hh_hub == a].mean() for a in range(len(K.HUB))])


def summary(seed, P=None, quiet=False):
    w = W.World(seed, P)
    R = routes(w)
    sh = {"truth": w.truth_hub}
    sh.update({k: hub_shares(w, v) for k, v in R.items()})
    sets = {k: tuple(np.where(v > K.LINE)[0]) for k, v in sh.items()}
    fam = np.vstack([sh[k] for k in ("truth", "load20", "load10", "thresh")])
    spread = (fam.max(0) - fam.min(0)).max()
    gold = sets["thresh"]
    margin = np.min(np.abs(fam - K.LINE))
    ok_family = all(sets[k] == gold for k in ("truth", "load20", "load10"))
    wrong = [k for k in ("tests", "hour", "night", "skipfail") if sets[k] != gold]
    # whole per cent agreement across the family on every hub
    rounds = np.all(np.round(fam + 1e-9).astype(int) == np.round(fam[0] + 1e-9).astype(int), axis=0).all()
    skipped = (w.k_ran[:, w.wkday][:, :, 2:6] < 0).mean()
    lab = lambda s: "".join(K.HUB[i][0] for i in s) or "-"
    if not quiet:
        print("seed %d skip %.1f%% gold %s m %.2f spread %.2f fam %s round %s | tests %s hour %s night %s skipfail %s"
              % (seed, 100 * skipped, ",".join(K.HUB[i] for i in gold), margin, spread, ok_family, rounds,
                 ",".join(K.HUB[i] for i in sets["tests"]), ",".join(K.HUB[i] for i in sets["hour"]),
                 ",".join(K.HUB[i] for i in sets["night"]), ",".join(K.HUB[i] for i in sets["skipfail"])))
        print("   gold  " + " ".join("%5.1f" % x for x in sh["thresh"]))
        print("   tests " + " ".join("%5.1f" % x for x in sh["tests"]))
    return dict(w=w, sh=sh, sets=sets, margin=margin, spread=spread, ok=ok_family, wrong=wrong, rounds=rounds)


if __name__ == "__main__":
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    b = int(sys.argv[2]) if len(sys.argv) > 2 else a + 1
    for s in range(a, b):
        summary(s)
