"""Shoppers, shelves and the days a line is off them.

Each store-line-day carries a first-choice demand. On a day the line is off the shelf its shoppers take another line of
the same category (r), come back for it after the restock (f) or buy nothing in the category (1 - r - f). Spells off
the shelf come from orders the stores' manual ordering missed (water, pet food, gluten-free bakery, one line at a time)
and from the formula supplier's missed weekly visits (every formula line at once). Refit days are closed days.
"""
import numpy as np

import params as P


def closed_mask():
    m = np.zeros((P.NS, P.ND), bool)
    for s, (a, b) in P.REFITS.items():
        ia = (np.datetime64(a) - np.datetime64(P.D0.date())).astype(int)
        ib = (np.datetime64(b) - np.datetime64(P.D0.date())).astype(int)
        m[s, ia:ib + 1] = True
    return m


def simulate(seed=P.SEED_WORLD):
    rng = np.random.default_rng(seed)
    size = np.exp(rng.normal(0, 0.28, P.NS))
    doy = P.DAYS.dayofyear.values
    dowf = np.array(P.DOW)[P.DAYS.dayofweek.values]
    closed = closed_mask()
    res = {}
    for c, C in P.CATS.items():
        lines = P.LINES[c]
        n = len(lines)
        share = np.array([x[1] for x in lines])
        group = np.array([x[2] for x in lines])
        seas = 1 + C["seas"] * np.cos(2 * np.pi * (doy - 15) / 365.25)      # southern summer peak in mid January
        lam = C["base"] * size[:, None, None] * share[None, :, None] * (dowf * seas)[None, None, :]
        oos = np.zeros((P.NS, n, P.ND), bool)
        if C.get("whole"):
            start = rng.uniform(size=(P.NS, P.ND)) < C["rho_whole"]
            for s, d in zip(*np.nonzero(start)):
                L = int(rng.integers(C["whole_dur"][0], C["whole_dur"][1] + 1))
                oos[s, :, d:d + L] = True
        else:
            start = rng.uniform(size=(P.NS, n, P.ND)) < C["rho"]
            for s, i, d in zip(*np.nonzero(start)):
                L = 1 + rng.poisson(C["dur"])
                oos[s, i, d:d + L] = True
        oos &= ~closed[:, None, :]
        first = rng.poisson(lam)
        first[np.broadcast_to(closed[:, None, :], first.shape)] = 0
        units = np.where(oos, 0, first).astype(np.int64)
        sub = np.zeros_like(units)
        defer = np.zeros_like(units)
        lost = np.zeros_like(units)
        lo, hi = C["lag"]
        S_, I_, D_ = np.nonzero(oos & (first > 0))
        for s, i, d in zip(S_, I_, D_):
            k = int(first[s, i, d])
            u = rng.uniform(size=k)
            ks = int((u < C["r"]).sum())
            kf = int(((u >= C["r"]) & (u < C["r"] + C["f"])).sum())
            inst = ~oos[s, :, d] & (group == group[i])
            if ks and inst.any():
                w = share * inst
                sub[s, :, d] += rng.multinomial(ks, w / w.sum())
            else:
                lost[s, i, d] += ks
            lost[s, i, d] += k - ks - kf
            for _ in range(kf):
                dd = d + int(rng.integers(lo, hi + 1))
                while dd < P.ND and (oos[s, i, dd] or closed[s, dd]):
                    dd += 1
                if dd < P.ND:
                    defer[s, i, dd] += 1
                else:
                    lost[s, i, d] += 1
        units = units + sub + defer
        res[c] = dict(lam=lam, oos=oos, first=first, sub=sub, defer=defer, lost=lost, units=units, share=share,
                      price=np.array([x[3] for x in lines]))
    return res, size, closed
