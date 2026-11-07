"""Prototype 1: does the payment-relevance footprint separate an upcoder from genuinely sicker hospitals,
and how stable is the honest clustering ratio across acuity levels?"""
import numpy as np

rng = np.random.default_rng(212)

MCC = {  # code: (base prevalence at z=0, loading)
    "J96.01": (0.08, 0.9), "N17.0": (0.02, 0.8), "I21.4": (0.04, 0.6), "E43": (0.03, 0.8),
    "G93.41": (0.04, 0.8), "J69.0": (0.02, 0.7), "I26.99": (0.01, 0.4), "A41.9": (0.03, 0.8),
}
CSTAR = "J96.01"


def logit(p):
    return np.log(p / (1 - p))


def sim(mu, n, u=0.0, sd=1.0):
    z = rng.normal(mu, sd, n)
    pres = {}
    for k, (p, b) in MCC.items():
        pr = 1 / (1 + np.exp(-(logit(p) + b * z)))
        pres[k] = rng.random(n) < pr
    other = np.zeros(n, bool)
    for k in MCC:
        if k != CSTAR:
            other |= pres[k]
    c = pres[CSTAR].copy()
    if u > 0:
        add = (~other) & (~c) & (rng.random(n) < u)
        c |= add
    else:
        add = np.zeros(n, bool)
    return dict(c=c, other=other, add=add, z=z)


print("honest clustering ratio by acuity")
for mu in [-0.6, -0.3, 0.0, 0.3, 0.6, 0.9]:
    d = sim(mu, 400000)
    p0 = d["c"][~d["other"]].mean()
    p1 = d["c"][d["other"]].mean()
    mcc_share = (d["c"] | d["other"]).mean()
    sole = (d["c"] & ~d["other"]).sum() / d["c"].sum()
    print(f"mu {mu:+.1f}: P(c*|none) {p0:.4f}  P(c*|other) {p1:.4f}  ratio {p0/p1:.3f}  MCC share {mcc_share:.3f}  sole share of c* {sole:.3f}")

print()
for u in [0.05, 0.08, 0.12]:
    d = sim(0.1, 400000, u=u)
    p0 = d["c"][~d["other"]].mean(); p1 = d["c"][d["other"]].mean()
    mcc_share = (d["c"] | d["other"]).mean()
    sole = (d["c"] & ~d["other"]).sum() / d["c"].sum()
    print(f"upcoder u {u}: P(c*|none) {p0:.4f}  P(c*|other) {p1:.4f}  ratio {p0/p1:.3f}  MCC share {mcc_share:.3f} sole {sole:.3f}")
