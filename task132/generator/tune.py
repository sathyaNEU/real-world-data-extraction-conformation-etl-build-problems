"""Pick legacy fitted-date shifts (one month, on modules that were already replacements at go-live) that leave
every graded figure clear of its rounding edge without moving the lot count. Scored in memory on the shipped
history with a vectorised forecast, then the chosen shifts go into world.TUNE."""
import datetime as dt
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W


def edge(v):
    return abs((v * 10) % 1 - 0.5)


def main(rounds=8, stop=0.09):
    import build as B
    import estimators as E
    import extracts as X
    W.TUNE = ()
    tmp = tempfile.mkdtemp()
    _, subs, fl, prog, extra, sp, f, _ = B.simulate()
    B.build(tmp, docs=False)
    reg, wo, hist, subs2, stock, plan = E.load(tmp)
    flt = E.fleet(reg)
    p26 = plan["Approved 2026"]
    avail = E.available(stock)
    nb = len(W.BANDS)
    # failures and the history row each one removed
    fr = E.failures(wo, flt, hist)
    row_of_wo = dict(zip(hist["removal_wo"], hist.index))
    fail_rows = [row_of_wo[w] for w in fr["wo_number"]]
    fail_month = list(fr["month"])

    def spell_expo(fitted, removed):
        e = np.zeros(nb)
        for m in E.spell_months(fitted, removed, W.MIGRATION):
            e[W.band_of(E.age_on(fitted, m))] += 1
        return e

    expo = {j: spell_expo(fi, re_) for j, fi, re_ in zip(hist.index, hist["fitted"], hist["removed"])}
    cnt_rows = {j: [] for j in hist.index}
    for j, m in zip(fail_rows, fail_month):
        cnt_rows[j].append(m)
    # forward: one row per supported relay, the band of its present module each month (-1 past support)
    region = dict(zip(subs2["sub_code"], subs2["region"]))
    cur = E.current_modules(flt, hist)
    cur_row = {a: j for j, a, r in zip(hist.index, hist["asset_id"], hist["removed"]) if r is None}
    H = E.months(W.HORIZON_START, E.month_add(W.PROGRAMME_END, 1))
    years = np.array([m.year for m in H])
    rows, regs, ends, fit_rows = [], [], [], []
    for aid, sub, bay, fitted in cur:
        end = E.support_end(sub, bay, p26)
        if end is None:
            continue
        n = len(E.months(W.HORIZON_START, end))
        rows.append([W.band_of(E.age_on(fitted, m)) for m in H[:n]] + [-1] * (len(H) - n))
        regs.append(region[sub])
        fit_rows.append(cur_row[aid])
    Bm = np.array(rows)
    regs = np.array(regs)
    pos_of_row = {j: i for i, j in enumerate(fit_rows)}

    def evaluate(Bmat, counts, ex):
        r = counts / ex * 12.0
        R = np.append(r, 0.0)
        q = R[Bmat] / 12.0
        live = Bmat >= 0
        surv = np.cumprod(np.where(live, 1 - q, 1.0), axis=1)
        surv = np.hstack([np.ones((surv.shape[0], 1)), surv[:, :-1]])
        e = np.where(live, surv * q + (1 - surv) * r[0] / 12.0, 0.0)
        lam = e.sum()
        by_year = [e[:, years == y].sum() for y in sorted(set(years))]
        by_reg = [e[regs == g].sum() for g in sorted(set(regs))]
        return lam, by_year, by_reg

    def totals(fitted_over):
        counts = np.zeros(nb)
        ex = np.zeros(nb)
        for j in hist.index:
            fi = fitted_over.get(j, hist.at[j, "fitted"])
            ex += expo[j] if j not in fitted_over else spell_expo(fi, hist.at[j, "removed"])
            for m in cnt_rows[j]:
                counts[W.band_of(E.age_on(fi, m))] += 1
        return counts, ex

    base_counts, base_ex = totals({})
    lam0, _, _ = evaluate(Bm, base_counts, base_ex)
    target = E.lots_needed(lam0, avail)
    print("target lots", target, "lam", round(lam0, 3), flush=True)

    def margins(lam):
        lo, hi = lam, lam
        while E.lots_needed(lo, avail) == target:
            lo -= 0.05
        while E.lots_needed(hi, avail) == target:
            hi += 0.05
        return (lam - lo) / lam, (hi - lam) / lam

    def score(Bmat, counts, ex):
        lam, by_year, by_reg = evaluate(Bmat, counts, ex)
        if E.lots_needed(lam, avail) != target or min(margins(lam)) < 0.03:
            return -1.0, lam
        covers = [100 * E.poisson_cdf(avail + n * W.LOT, lam) for n in W.SETTINGS]
        vals = [lam] + by_year + by_reg + [c for c in covers if 0.05 < c < 99.95]
        return min(edge(v) for v in vals), lam

    cand = B.candidates(sp)
    relay_mfg = {int(k): m for k, m in zip(fl["relay_key"], fl["mfg"])}
    _, key2aid, _, _ = X.register(np.random.default_rng(W.SEED + 1), subs, fl, prog, X.bay_plan(fl, prog), relay_mfg)
    moves = []
    for k, i in enumerate(cand):
        aid = key2aid[int(sp.at[i, "relay_key"])]
        hit = hist.index[(hist["asset_id"] == aid) & (hist["fitted"] == sp.at[i, "fitted"])].tolist()
        if hit:
            moves.append((k, hit[0]))
    over, chosen = {}, []
    Bcur, counts, ex = Bm.copy(), base_counts.copy(), base_ex.copy()
    best, _ = score(Bcur, counts, ex)
    print("base edge", round(best, 4), "candidates", len(moves), flush=True)
    for rnd in range(rounds):
        if best >= stop:
            break
        top = None
        for k, j in moves:
            if j in over:
                continue
            for sh in (1, -1):
                d = hist.at[j, "fitted"]
                m = E.month_add(dt.date(d.year, d.month, 1), sh)
                nd = dt.date(m.year, m.month, min(d.day, 28))
                if nd >= W.MIGRATION:
                    continue
                c2 = counts.copy()
                for fm in cnt_rows[j]:
                    c2[W.band_of(E.age_on(d, fm))] -= 1
                    c2[W.band_of(E.age_on(nd, fm))] += 1
                e2 = ex - expo[j] + spell_expo(nd, hist.at[j, "removed"])
                B2 = Bcur
                if j in pos_of_row:
                    B2 = Bcur.copy()
                    p = pos_of_row[j]
                    n = int((Bcur[p] >= 0).sum())
                    B2[p, :n] = [W.band_of(E.age_on(nd, mm)) for mm in H[:n]]
                s, _ = score(B2, c2, e2)
                if top is None or s > top[0]:
                    top = (s, k, j, sh, nd, c2, e2, B2)
        if top is None or top[0] <= best + 1e-9:
            break
        best = top[0]
        _, k, j, sh, nd, counts, ex, Bcur = top
        expo[j] = spell_expo(nd, hist.at[j, "removed"])
        hist.at[j, "fitted"] = nd
        over[j] = nd
        chosen.append((k, sh))
        print("round", rnd, "edge", round(best, 4), "move", (k, sh), flush=True)
    print("TUNE =", tuple(chosen))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8, float(sys.argv[2]) if len(sys.argv) > 2 else 0.09)
