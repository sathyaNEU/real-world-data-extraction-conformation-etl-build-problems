"""The call from the pack: each hub's share of weekday evening peak quarter-hours in which a panel household's
connection delivered under 80 per cent of its plan, by the golden's construction and its family, and the rungs a
competent analyst stops at."""
from __future__ import annotations

import numpy as np

import common as K


def pava(y, wt, increasing=True):
    """weighted pool-adjacent-violators fit of y in the given order"""
    sign = 1.0 if increasing else -1.0
    vals, wts, lens = [], [], []
    for v, w in zip(sign * np.asarray(y, float), np.asarray(wt, float)):
        vals.append(v)
        wts.append(w)
        lens.append(1)
        while len(vals) > 1 and vals[-2] > vals[-1]:
            tw = wts[-2] + wts[-1]
            nv = (vals[-2] * wts[-2] + vals[-1] * wts[-1]) / tw
            nl = lens[-2] + lens[-1]
            vals.pop()
            wts.pop()
            lens.pop()
            vals[-1], wts[-1], lens[-1] = nv, tw, nl
    return sign * np.repeat(np.array(vals), lens)


def _groups(pk):
    order = np.argsort(pk.t_hh, kind="stable")
    sel = order[pk.t_peak[order]]
    hh = pk.t_hh[sel]
    st = np.searchsorted(hh, np.arange(len(pk.hh_list)))
    en = np.searchsorted(hh, np.arange(len(pk.hh_list)), side="right")
    return sel, st, en


def household_shares(pk):
    """every route's share for every panel household"""
    sel, st, en = _groups(pk)
    NH = len(pk.hh_list)
    keys = ("tests", "hour", "night", "skipfail", "thresh", "load20", "load10", "iso")
    out = {k: np.zeros(NH) for k in keys}
    sched = len(pk.peak_days) * (K.PEAK_TO - K.PEAK_FROM)
    for i in range(NH):
        ix = sel[st[i]:en[i]]
        b = pk.t_below[ix]
        l = pk.t_load[ix]
        rt = pk.t_ratio[ix]
        dd = pk.t_day[ix]
        hr = pk.t_localq[ix] // 4
        out["tests"][i] = b.mean()
        wt = 1.0 / np.bincount(hr, minlength=24)[hr]
        out["hour"][i] = (wt * b).sum() / wt.sum()
        wt = 1.0 / np.bincount(dd, minlength=K.DAYS)[dd]
        out["night"][i] = (wt * b).sum() / wt.sum()
        out["skipfail"][i] = (b.sum() + sched - len(ix)) / sched
        allu = pk.q_load[i]
        down_q = pk.down_day[i, pk.q_day]
        down_t = pk.down_day[i, dd]
        # load-bin re-weighting to the node's own peak loads, bin rates non-decreasing in load
        for nb, key in ((20, "load20"), (10, "load10")):
            edges = np.linspace(0, 1, nb + 1)
            tb = np.clip(np.digitize(l, edges), 1, nb) - 1
            ub = np.clip(np.digitize(allu, edges), 1, nb) - 1
            tgt = np.bincount(ub, minlength=nb) / ub.size
            have = np.bincount(tb, minlength=nb)
            hit = np.bincount(tb, weights=b.astype(float), minlength=nb)
            idx = np.where(have > 0)[0]
            fit = pava(hit[idx] / have[idx], have[idx])
            rate = np.interp(np.arange(nb), idx, fit)
            out[key][i] = (tgt * rate).sum()
        # per plan period: the load above which the connection falls under the standard, and an isotonic curve
        th, iso = 0.0, 0.0
        for dn in np.unique(down_q):
            qs = down_q == dn
            ts = down_t == dn
            lq = allu[qs]
            if not ts.any():
                continue
            o = np.argsort(l[ts], kind="stable")
            lt, bt, rtt = l[ts][o], b[ts][o].astype(int), rt[ts][o]
            c0 = np.concatenate([[0], np.cumsum(bt == 0)])
            c1 = np.concatenate([np.cumsum((bt == 1)[::-1])[::-1], [0]])
            j = int(np.argmax(c0 + c1))
            t = (lt[j - 1] + lt[j]) / 2 if 0 < j < len(lt) else (-1.0 if j == 0 else 2.0)
            th += (lq > t).sum()
            fit = pava(rtt, np.ones(len(rtt)), increasing=False)
            iso += (np.interp(lq, lt, fit) < K.STANDARD).sum()
        out["thresh"][i] = th / allu.size
        out["iso"][i] = iso / allu.size
    return out


GOLDEN = "thresh"
FAMILY = ("thresh", "load20", "load10", "iso")
RUNGS = ("tests", "hour", "night", "skipfail")


def hub_table(pk, shares):
    return {k: np.array([100.0 * v[pk.hub == h].mean() for h in K.HUB]) for k, v in shares.items()}


def designated(values):
    return tuple(h for h, v in zip(K.HUB, values) if v > K.LINE)


def call(pk):
    sh = household_shares(pk)
    tab = hub_table(pk, sh)
    return dict(shares=sh, table=tab, sets={k: designated(v) for k, v in tab.items()},
                n_households=np.array([(pk.hub == h).sum() for h in K.HUB]))
