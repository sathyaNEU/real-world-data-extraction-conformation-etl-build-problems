"""World model for task484 architecture 2 (stage 2 screen): device-level stock, worst-first changeout by heat status,
a stratified 2024 survey with weights, applications recording status. Prints the ladder and the standing family."""
import numpy as np
SEED = 48431
r = np.random.default_rng(SEED)
CL = ["UNC", "CNC", "CAT", "PEL", "FPL", "HYD"]
EF = dict(UNC=34.0, CNC=17.0, CAT=15.0, PEL=4.0, FPL=27.0, HYD=26.0)
PRIM = dict(UNC=0.45, CNC=0.40, CAT=0.40, PEL=0.50, FPL=0.03, HYD=0.80)
CORD = {1: dict(UNC=4.2, CNC=3.8, CAT=3.8, PEL=3.2, FPL=1.0, HYD=7.5), 0: dict(UNC=1.1, CNC=1.0, CAT=1.0, PEL=0.9, FPL=0.3, HYD=3.0)}
DEFAULT = dict(UNC=2.1, CNC=2.1, CAT=2.1, PEL=2.0, FPL=0.4, HYD=5.0)
AREAS = [  # name, scale, changeout intensity, survey rate, commitment, valley burning factor
    ("A1", 1.00, 0.50, 0.10, 25, 1.00), ("A2", 0.70, 0.42, 0.14, 22, 1.05), ("A3", 1.30, 0.18, 0.08, 20, 0.95),
    ("A4", 0.50, 0.30, 0.18, 15, 1.10), ("A5", 0.90, 0.08, 0.11, 15, 1.00), ("A6", 0.60, 0.55, 0.15, 25, 0.92)]
res = []
for name, scale, prog, srate, T, vf in AREAS:
    n = {c: int(scale * x) for c, x in zip(CL, (5200, 3000, 600, 1100, 2400, 220))}
    st = {c: (r.random(n[c]) < PRIM[c]).astype(int) for c in CL}
    use = {c: np.array([CORD[s][c] for s in st[c]]) * vf * r.lognormal(-0.08, 0.4, n[c]) for c in CL}
    co, other = {}, {}
    for c in ("UNC", "HYD"):
        p = np.where(st[c] == 1, min(0.95, prog * 1.8), prog * 0.25)
        co[c] = r.random(n[c]) < p
        other[c] = (~co[c]) & (r.random(n[c]) < 0.03)                 # removals outside the programme, at random
    for c in ("CNC", "CAT", "PEL", "FPL"):
        co[c] = np.zeros(n[c], bool); other[c] = r.random(n[c]) < 0.04
    # the current stock: survivors, programme replacements (60 per cent certified, 40 per cent pellet), new construction
    cur = {c: [use[c][~(co[c] | other[c])], st[c][~(co[c] | other[c])], np.zeros((~(co[c] | other[c])).sum(), bool)] for c in CL}
    for c in ("UNC", "HYD"):
        u, s = use[c][co[c]] * 0.9, st[c][co[c]]
        k = int(len(u) * (0.6 if c == "UNC" else 1.0))
        for tgt, sl in (("CNC", slice(0, k)), ("PEL", slice(k, None))):
            cur[tgt][0] = np.concatenate([cur[tgt][0], u[sl]]); cur[tgt][1] = np.concatenate([cur[tgt][1], s[sl]])
            cur[tgt][2] = np.concatenate([cur[tgt][2], np.ones(len(u[sl]), bool)])
    nb = int(380 * scale); nbs = (r.random(nb) < 0.35).astype(int)
    nbu = np.array([CORD[s]["CNC"] for s in nbs]) * vf * r.lognormal(-0.08, 0.4, nb)
    cur["CNC"] = [np.concatenate([cur["CNC"][0], nbu]), np.concatenate([cur["CNC"][1], nbs]), np.concatenate([cur["CNC"][2], np.ones(nb, bool)])]
    sv = {}
    for c in CL:
        u, s, new = cur[c]; m = max(12, int(srate * len(u))); i = r.choice(len(u), m, replace=False)
        sv[c] = (u[i], s[i], new[i], len(u) / m)
    def cell(c, s, src=None):
        u, ss, new, w = (src or sv)[c]; k = ss == s
        return u[k].mean() if k.sum() else u.mean()
    E26 = sum(len(cur[c][0]) * sv[c][0].mean() * EF[c] for c in CL)
    truth = sum(use[c].sum() * EF[c] for c in CL)
    def base(kind):
        tot = 0.0
        for c in CL:
            u, s, new, w = sv[c]
            if kind == "classmean":
                a = n[c] * u.mean()
            elif kind == "surveymix":
                a = n[c] * sum((s == q).mean() * cell(c, q) for q in (0, 1))
            elif kind == "default":
                a = n[c] * DEFAULT[c]
            elif kind == "survivors_only":
                a = (n[c] - co[c].sum()) * u.mean()
            elif kind in ("golden", "allprimary", "unweighted", "pooled"):
                old = ~new                                              # units in place by 2014
                mix1 = s[old].mean() if old.sum() else s.mean()
                nco = co[c].sum(); nco1 = st[c][co[c]].sum()
                rest = n[c] - nco
                if kind == "allprimary":
                    a = rest * (mix1 * cell(c, 1) + (1 - mix1) * cell(c, 0)) + nco * cell(c, 1)
                else:
                    a = rest * (mix1 * cell(c, 1) + (1 - mix1) * cell(c, 0)) + nco1 * cell(c, 1) + (nco - nco1) * cell(c, 0)
            tot += a * EF[c]
        return tot
    red = {k: 100 * (base(k) - E26) / base(k) for k in ("golden", "classmean", "surveymix", "default", "survivors_only", "allprimary")}
    red["truth"] = 100 * (truth - E26) / truth
    res.append((name, T, red, co["UNC"].mean(), st["UNC"][co["UNC"]].mean(), st["UNC"][~co["UNC"]].mean(), len(cur["UNC"][0])))
keys = ["truth", "golden", "allprimary", "classmean", "surveymix", "default", "survivors_only"]
print("area T  | " + "  ".join("%-14s" % k for k in keys))
for name, T, red, a, b, c_, nu in res:
    print("%s  %2d | " % (name, T) + "  ".join("%5.1f %-8s" % (red[k], "TRIGGER" if red[k] < T else "") for k in keys) + " | co %.2f prim co %.2f surv %.2f" % (a, b, c_))
for k in keys:
    s = sorted(n for n, T, red, *_ in res if red[k] < T)
    print("%-15s triggers %s" % (k, ",".join(s) or "none"))
g = [red["golden"] - T for n, T, red, *_ in res]
print("golden margin to commitment, smallest %.1f points" % min(abs(x) for x in g))
