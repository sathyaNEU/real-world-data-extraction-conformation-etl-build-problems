"""Pick balance adjustments on a few loans so every graded figure clears its rounding edge. A loan's ECL is
linear in its current balance, so each candidate updates the group sums arithmetically."""
import itertools
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W


def keys_of(prod, st, year):
    return ["total", "s%d" % st, "%s_s%d" % (prod, st), "band_%s_%s" % (prod, year)], ["%s_s%d_gca" % (prod, st)]


def margin(f):
    worst = 1.0
    for k, v in f.items():
        if k.endswith("_cov"):
            m = abs((v * 100) % 1 - 0.5) / 0.5
        else:
            m = abs((v / 1000.0) % 1 - 0.5) / 0.5
        worst = min(worst, m)
    return worst


def main():
    import build as B
    import estimators as E
    W.TUNE = {}
    tmp = tempfile.mkdtemp()
    lo, bk, hd = B.build(tmp)
    s = E.solve(tmp)
    L = s["loans"].reset_index(drop=True)
    keymap = dict(zip(bk["loan_no"], bk["loan_key"]))
    # base sums
    base = {"total": L["ecl"].sum()}
    for (st, p), g in L.groupby(["stage", "product"]):
        base["s%d" % st] = base.get("s%d" % st, 0.0) + g["ecl"].sum()
        base["%s_s%d" % (p, st)] = g["ecl"].sum()
        base["%s_s%d_gca" % (p, st)] = g["current_balance"].sum()
    for (p, y), g in L.groupby(["product", "band"]):
        base["band_%s_%s" % (p, y)] = g["ecl"].sum()

    def figures(adj):
        f = dict(base)
        for i, d in adj:
            r = L.iloc[i]
            de = r["ecl"] * d / r["current_balance"]
            ek, gk = keys_of(r["product"], int(r["stage"]), r["band"])
            for k in ek:
                f[k] += de
            for k in gk:
                f[k] += d
        for st in (1, 2):
            for p in ("PL36", "PL60"):
                f["%s_s%d_cov" % (p, st)] = 100 * f["%s_s%d" % (p, st)] / f["%s_s%d_gca" % (p, st)]
        return f

    print("base margin", round(margin(figures([])), 3), flush=True)

    def worst_key(f):
        best_k, best_m = None, 9
        for k, v in f.items():
            m = abs((v * 100) % 1 - 0.5) / 0.5 if k.endswith("_cov") else abs((v / 1000.0) % 1 - 0.5) / 0.5
            if m < best_m:
                best_k, best_m = k, m
        return best_k

    def group_rows(k):
        if k == "total":
            return L.index[L["ecl"] > 0]
        if k.startswith("s") and k[1:].isdigit():
            return L.index[(L["stage"] == int(k[1:])) & (L["ecl"] > 0)]
        if k.startswith("band_"):
            _, p, y = k.split("_", 2)
            return L.index[(L["product"] == p) & (L["band"] == y)]
        p, st = k.split("_")[0], int(k.split("_")[1][1])
        return L.index[(L["product"] == p) & (L["stage"] == st) & (L["ecl"] > 0)]

    adj = []
    deltas = [-2900, -2100, -1400, -900, -400, 400, 900, 1400, 2100, 2900]
    rng = np.random.default_rng(11)
    for step in range(8):
        f = figures(adj)
        cur = margin(f)
        print("step", step, "margin", round(cur, 3), "worst", worst_key(f), flush=True)
        if cur >= 0.25:
            break
        rows = group_rows(worst_key(f))
        rows = rng.choice(rows.to_numpy(), min(len(rows), 300), replace=False)
        cand = None
        for i in rows:
            if any(i == a for a, _ in adj):
                continue
            for d in deltas:
                m = margin(figures(adj + [(i, d)]))
                if cand is None or m > cand[0]:
                    cand = (m, i, d)
        if cand is None or cand[0] <= cur:
            break
        adj.append((cand[1], cand[2]))
    best = (margin(figures(adj)), adj)
    tune = {int(keymap[L.at[i, "loan_no"]]): float(d) for i, d in best[1]}
    print("best margin", round(best[0], 3))
    print("TUNE =", tune)


if __name__ == "__main__":
    main()
