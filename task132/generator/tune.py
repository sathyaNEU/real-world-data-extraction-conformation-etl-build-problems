"""Pick recorded-failure date shifts (one month) that leave every graded figure clear of its rounding
edge. Exposure is untouched by a failure's date, so each candidate is scored on band counts alone."""
import datetime as dt
import itertools
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W


def main():
    import build as B
    import estimators as E
    W.TUNE = ()
    tmp = tempfile.mkdtemp()
    _, subs, fl, prog, fails = B.simulate()
    B.build(tmp)
    reg, wo, subs2, stock, plan = E.load(tmp)
    flt = E.fleet(reg)
    expW = E.exposure(flt, W.MIGRATION)
    tot, by_year, by_region = E.forward(flt, plan["Approved 2026"], subs2)
    avail = E.available(stock)
    post = fails[fails["month"] >= W.MIGRATION].reset_index(drop=True)
    inst = dict(zip(fl["relay_key"], fl["install"]))
    ret = dict(zip(prog["sub_code"], prog["retired_on"]))
    sub_of = dict(zip(fl["relay_key"], fl["sub_code"]))
    base = np.bincount([W.band_of(a) for a in post["age"]], minlength=6).astype(float)

    r0 = base / expW * 12.0
    target_lots = E.lots_needed((r0 * tot).sum() / 12.0, avail)
    print("target lots", target_lots, "lam", round((r0 * tot).sum() / 12.0, 2))

    def score(cnt):
        r = cnt / expW * 12.0
        lam = (r * tot).sum() / 12.0
        if E.lots_needed(lam, avail) != target_lots:
            return -1
        vals = [(r * v).sum() / 12.0 for v in by_year.values()] + [(r * v).sum() / 12.0 for v in by_region.values()] + [lam]
        vals += [100 * E.poisson_cdf(avail + n * W.LOT, lam) for n in W.SETTINGS]
        vals = [v for v in vals if v < 99.95]
        return min(abs((v * 10) % 1 - 0.5) for v in vals)

    moves = []
    for k, f in post.iterrows():
        if ret.get(sub_of[f.relay_key]):
            continue
        for sh in (1, -1):
            m = E.month_add(f["month"], sh)
            if not (W.MIGRATION <= m <= dt.date(2026, 9, 1)):
                continue
            nb = W.band_of(E.age_on(inst[f.relay_key], m))
            ob = W.band_of(f["age"])
            if nb != ob:
                moves.append((k, sh, ob, nb))
    print("base", score(base), "candidate moves", len(moves))
    best = None
    for mv in moves:
        c = base.copy(); c[mv[2]] -= 1; c[mv[3]] += 1
        s = score(c)
        if best is None or s > best[0]:
            best = (s, [mv])
    for a, b in itertools.combinations(moves, 2):
        if a[0] == b[0]:
            continue
        c = base.copy()
        for mv in (a, b):
            c[mv[2]] -= 1; c[mv[3]] += 1
        s = score(c)
        if s > best[0]:
            best = (s, [a, b])
        if best[0] >= 0.15:
            break
    print("best", best)
    print("TUNE =", tuple((mv[0], mv[1]) for mv in best[1]))


if __name__ == "__main__":
    main()
