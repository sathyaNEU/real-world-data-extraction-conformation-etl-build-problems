"""Calibration: place each county's frame sizes, list overlap, nitrate medians and sample sizes so that the golden
(every dual-frame estimator) and each wrong route fall where the ladder needs them, with margins. Prints the placement
to paste into world.PLACED.

    python3 task471/generator/calibrate.py
"""
import sys

import numpy as np

import sim as S
import world as W

T = W.QUALIFY
GOLD = ("KA", "multiplicity", "domain means", "hartley 0", "hartley 1")
# target pattern per county: A robust qualifier, G a robust qualifier whose permit-only wells run high so that the
# parcel list alone leaves it out, B qualifies but pooling drops it, C below but adding the two lists' estimates (or
# weighting each tested well by the rate of the list it was drawn from, the same route in expectation) lifts it over,
# E below on every route
PATTERN = "GBECEBAECCBEAEEC"


def ok(e, kind):
    g = [e[x] for x in GOLD]
    lo, hi = min(g), max(g)
    if kind == "A":
        return lo >= 1.25 * T and e["pooled"] >= 1.08 * T
    if kind == "G":
        return (lo >= 1.25 * T and e["parcel list alone"] <= 0.88 * T and e["parcel share x wells"] <= 0.90 * T)
    if kind == "B":
        return lo >= 1.10 * T and hi <= 1.35 * T and e["pooled"] <= 0.92 * T
    if kind == "C":
        return (hi <= 0.90 * T and lo >= 0.60 * T and e["lists added"] >= 1.10 * T and e["drawn list's rate"] >= 1.08 * T
                and e["pooled"] <= 0.90 * T)
    if kind == "E":
        return hi <= 0.62 * T and e["lists added"] <= 0.86 * T and e["drawn list's rate"] <= 0.86 * T
    raise ValueError(kind)


def draw_params(r, kind):
    """shares and medians first, then the county's size from the golden total its type needs"""
    po, qo = {"A": ((0.10, 0.22), (0.22, 0.40)), "B": ((0.08, 0.16), (0.40, 0.52)), "C": ((0.05, 0.12), (0.08, 0.18)),
              "E": ((0.10, 0.22), (0.18, 0.40)), "G": ((0.34, 0.46), (0.10, 0.20))}[kind]
    po, qo = r.uniform(*po), r.uniform(*qo)
    sigma = r.uniform(0.85, 1.05)
    g = r.uniform(0.7, 1.5)
    qmul = {"A": 4.6, "B": 6.5, "C": 3.0, "E": 4.6, "G": 2.2}[kind]
    mPo, mQo, mB = (5.4 * g if kind == "G" else 1.6 * g), qmul * g, (1.5 * g if kind == "G" else 2.4 * g)
    share = (po * S.exceed_share(mPo, sigma) + qo * S.exceed_share(mQo, sigma)
             + (1 - po - qo) * S.exceed_share(mB, sigma))
    target = r.uniform(*{"A": (1.45, 2.6), "B": (1.16, 1.28), "C": (0.68, 0.84), "E": (0.20, 0.55),
                         "G": (1.40, 1.75)}[kind]) * T
    N = int(np.clip(target / share, 600, 14000))
    NP, NQ = N * (1 - qo), N * (1 - po)
    nP = int(round(NP * r.uniform(0.07, 0.10)))
    nQ = int(round(NQ * r.uniform(0.030, 0.045)))
    return dict(N=N, po=round(po, 3), qo=round(qo, 3), mPo=round(mPo, 2), mQo=round(mQo, 2), mB=round(mB, 2),
                sigma=round(sigma, 2), nP=nP, nQ=nQ, accept=round(r.uniform(0.55, 0.72), 2),
                retest=round(r.uniform(0.62, 0.80), 2), phone=round(r.uniform(0.18, 0.32), 2))


def place(seed=W.SEED, tries=4000):
    placed = []
    for k, kind in enumerate(PATTERN):
        r = np.random.default_rng([seed, 99, k])
        for t in range(tries):
            p = draw_params(r, kind)
            p["tries"] = t
            c = S.county(seed, k, p)
            e = S.estimates(c)
            phone_ok = int(c["phone"].sum()) >= 2 and int((c["retested"] & ~c["phone"]).sum()) >= 3
            if ok(e, kind) and phone_ok:
                placed.append(p)
                print("county %2d %s placed after %d tries: %s" % (k, kind, t,
                      "  ".join("%s %.0f" % (x, e[x]) for x in ("KA", "pooled", "lists added", "drawn list's rate",
                                                                "permit list alone"))), file=sys.stderr)
                break
        else:
            raise SystemExit("county %d (%s) not placed" % (k, kind))
    return placed


if __name__ == "__main__":
    for p in place():
        print("    %r," % p)
