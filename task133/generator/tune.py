"""Pick extra repayments of irregular amounts on a few up-to-date loans, paid a few days after their September 2026
instalment, so every graded figure clears its rounding edge, read with past-maturity loans carrying their one month or
nothing. The repayment comes off the balance at the reporting date in full (no interest is charged on it before then)
and a loan's ECL is linear in its current balance, so each candidate updates the group sums arithmetically. Paste the
printed TUNE into world.py and rebuild."""
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W


def keys_of(prod, st, year):
    return ["total", "s%d" % st, "%s_s%d" % (prod, st), "band_%s_%s" % (prod, year)], ["%s_s%d_gca" % (prod, st)]


def margin_of(k, v):
    return abs((v * 100) % 1 - 0.5) / 0.5 if k.endswith("_cov") else abs((v / 1000.0) % 1 - 0.5) / 0.5


def main():
    import build as B
    import estimators as E
    W.TUNE = {}
    tmp = tempfile.mkdtemp()
    _, bk, _ = B.build(tmp)
    s = E.solve(tmp)
    L = s["loans"].reset_index(drop=True)
    info = bk.set_index("loan_no")
    L["key"] = info.loc[L["loan_no"], "loan_key"].values
    L["dpd"] = info.loc[L["loan_no"], "days_past_due"].values
    base = {"total": L["ecl"].sum()}
    for (st, p), g in L.groupby(["stage", "product"]):
        base["s%d" % st] = base.get("s%d" % st, 0.0) + g["ecl"].sum()
        base["%s_s%d" % (p, st)] = g["ecl"].sum()
        base["%s_s%d_gca" % (p, st)] = g["current_balance"].sum()
    for (p, y), g in L.groupby(["product", "band"]):
        base["band_%s_%s" % (p, y)] = g["ecl"].sum()
    # the same figures read with past-maturity loans carrying nothing: every graded figure must round alike both ways
    z = E.solve(tmp, pm_zero=True)
    Z = z["loans"].reset_index(drop=True)
    alt = {"total": Z["ecl"].sum()}
    for (st, p), g in Z.groupby(["stage", "product"]):
        alt["s%d" % st] = alt.get("s%d" % st, 0.0) + g["ecl"].sum()
        alt["%s_s%d" % (p, st)] = g["ecl"].sum()
        alt["%s_s%d_gca" % (p, st)] = g["current_balance"].sum()
    for (p, y), g in Z.groupby(["product", "band"]):
        alt["band_%s_%s" % (p, y)] = g["ecl"].sum()
    shift = {k: alt[k] - base[k] for k in base}

    def figures(adj, zero=False):
        f = dict(base)
        if zero:
            for k in f:
                f[k] += shift[k]
        for i, amt in adj:
            r = L.iloc[i]
            d = -amt
            ek, gk = keys_of(r["product"], int(r["stage"]), r["band"])
            for k in ek:
                f[k] += r["ecl"] * d / r["current_balance"]
            for k in gk:
                f[k] += d
        for st in (1, 2):
            for p in ("PL36", "PL60"):
                f["%s_s%d_cov" % (p, st)] = 100 * f["%s_s%d" % (p, st)] / f["%s_s%d_gca" % (p, st)]
        return f

    def bin_of(k, v):
        return round(v, 2) if k.endswith("_cov") else round(v / 1000.0)

    def pair(f, f0, k):
        return min(margin_of(k, f[k]), margin_of(k, f0[k])) if bin_of(k, f[k]) == bin_of(k, f0[k]) else 0.0

    def margin(f, adj=None):
        f0 = figures(adj if adj is not None else [], zero=True)
        return min(pair(f, f0, k) for k in f)

    def score(f, adj):
        """the worst figure's margin, then the margins short of the target, so one straddling figure can be fixed
        while another still straddles"""
        f0 = figures(adj, zero=True)
        v = [pair(f, f0, k) for k in f]
        return (min(v), sum(min(x, 0.3) for x in v))

    def worst_key(f, adj=None):
        f0 = figures(adj if adj is not None else [], zero=True)
        return min(f, key=lambda k: pair(f, f0, k))

    def group_rows(k):
        ok = (L["ecl"] > 0) & (L["dpd"] == 0) & (L["current_balance"] > 4000)
        if k == "total":
            return L.index[ok]
        if k.startswith("s") and k[1:].isdigit():
            return L.index[ok & (L["stage"] == int(k[1:]))]
        if k.startswith("band_"):
            _, p, y = k.split("_", 2)
            return L.index[ok & (L["product"] == p) & (L["band"] == y)]
        p, st = k.split("_")[0], int(k.split("_")[1][1])
        return L.index[ok & (L["product"] == p) & (L["stage"] == st)]

    rng = np.random.default_rng(11)
    adj = []
    print("base margin", round(margin(figures([]), []), 3), flush=True)
    for step in range(10):
        f = figures(adj)
        cur = score(f, adj)
        print("step", step, "margin", round(cur[0], 3), "worst", worst_key(f, adj), flush=True)
        if cur[0] >= 0.25:
            break
        rows = group_rows(worst_key(f, adj))
        rows = rng.choice(rows.to_numpy(), min(len(rows), 300), replace=False)
        cand = None
        for i in rows:
            if any(i == a for a, _ in adj):
                continue
            cap = min(6000.0, 0.3 * float(L.at[i, "current_balance"]))
            for amt in np.round(rng.uniform(250, cap, 12), 2):
                m = score(figures(adj + [(i, float(amt))]), adj + [(i, float(amt))])
                if cand is None or m > cand[0]:
                    cand = (m, i, float(amt))
        if cand is None or cand[0] <= cur:
            break
        adj.append((cand[1], cand[2]))
    tune = {int(L.at[i, "key"]): amt for i, amt in sorted(adj, key=lambda x: int(L.at[x[0], "key"]))}
    print("best margin", round(margin(figures(adj), adj), 3))
    print("TUNE =", tune)


if __name__ == "__main__":
    main()
