import sys, collections, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import p2


def estimators(rows, U=2, f="HF", k="E43"):
    rs = [r for r in rows if r[1] == f]

    def strata(sub):
        n0 = sum(1 for r in sub if not any(c != k for c in r[2]))
        c0 = sum(1 for r in sub if k in r[2] and not any(c != k for c in r[2]))
        n1 = sum(1 for r in sub if any(c != k for c in r[2]))
        c1 = sum(1 for r in sub if k in r[2] and any(c != k for c in r[2]))
        return n0, c0, n1, c1
    hs = sorted(set(r[0] for r in rs))
    st = {h: strata([r for r in rs if r[0] == h]) for h in hs}
    oth = [st[h] for h in hs if h != U]
    N0 = sum(o[0] for o in oth); C0 = sum(o[1] for o in oth); N1 = sum(o[2] for o in oth); C1 = sum(o[3] for o in oth)
    n0, c0, n1, c1 = st[U]
    a = c0 - n0 * (C0 / N0) / (C1 / N1) * (c1 / n1)
    b = c0 - n0 * (C0 / N0)
    ratios = [(o[1] / o[0]) / (o[3] / o[2]) for o in oth if o[3] > 0 and o[0] > 0 and o[1] > 0]
    med = np.median(ratios)
    c = c0 - n0 * med * (c1 / n1)
    import statsmodels.api as sm
    X = []; y = []
    hidx = {h: i for i, h in enumerate(hs)}
    for r in rs:
        oth_m = any(cc != k for cc in r[2])
        row = [1.0, float(oth_m)] + [1.0 if hidx[r[0]] == j else 0.0 for j in range(1, len(hs))]
        row.append(1.0 if (r[0] == U and not oth_m) else 0.0)
        X.append(row); y.append(1.0 if k in r[2] else 0.0)
    X = np.array(X); y = np.array(y)
    m = sm.Logit(y, X).fit(disp=0)
    Xc = X.copy(); Xc[:, -1] = 0
    sel = np.array([(r[0] == U and not any(cc != k for cc in r[2])) for r in rs])
    d = y[sel].sum() - m.predict(Xc[sel]).sum()
    return a, b, c, d, (n0, c0, n1, c1)


if __name__ == "__main__":
    n = int(sys.argv[1]); u1 = float(sys.argv[2]); u2 = float(sys.argv[3])
    tally = collections.defaultdict(collections.Counter)
    for s in range(n):
        hosp, rows = p2.world(2000 + s, u_main=u1, u_second=u2)
        res, r0, r1, r3 = p2.analyse(rows)
        truth = sum(r[9] for r in rows if r[0] == 2 and r[1] == "HF")
        a, b, c, d, st = estimators(rows)
        print(s, "R0", res["R0"], "R1", res["R1"], "R1b", res["R1b"], "R3", res["R3"], "2nd", res["R3_second"],
              "margin %.2f" % res["R3_margin"], "truth", truth, "est a %.1f b %.1f c %.1f d %.1f" % (a, b, c, d), st)
        for kk in ("R0", "R1", "R1b", "R2", "R2b", "R3"):
            tally[kk][str(res[kk][:2])] += 1
    for kk, cc in tally.items():
        print(kk, dict(cc))
