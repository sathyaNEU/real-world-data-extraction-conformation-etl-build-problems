"""Seed search for the simulation (development only; the shipped seed is params.SEED): each seed's pack is built in a
scratch folder and scored on the call's margins, the clean truth's agreement and the asks' separation from the cracker's
routes."""
import os
import sys
import tempfile

import numpy as np

import build as B
import docs
import estim as E
import params as P
import sim
import solve


def score(seed):
    T = tempfile.mkdtemp()
    out = B.run(T, documents=False, seed=seed)
    W, R = out["W"], out["R"]
    docs.flows_workbook(os.path.join(T, B.FILES["flows"]), R)
    A = solve.call(T, B.FILES)
    clean = {}
    for d in P.DCODES:
        Ot = W.M.T @ sim.clean_flows(W, d) @ W.M
        for a, b in E.CELLS:
            clean[(d, a + b)] = E.not_real(Ot, W.M, a, b)
    ppvd = max(E.not_real_ppv(A["C"], a, b) for a, b in E.CELLS)
    df = solve.persons(T, B.FILES)
    g, c = solve.ask_match(T, B.FILES, df), solve.ask_match(T, B.FILES, df, key="line")
    gd, cd = solve.ask_days(T, B.FILES, df), solve.ask_days(T, B.FILES, df, date="attempt_date")
    hitsA = sum((g[d][0] == c[d][0]) + (round(g[d][1], 1) == round(c[d][1], 1)) for d in P.DCODES)
    hitsB = sum(round(gd[d][1], 1) == round(cd[d][1], 1) for d in P.DCODES)
    return dict(seed=seed, margin=min(abs(v - P.WARN_SHARE) for v in A["shares"].values()),
                clean_margin=min(abs(v - P.WARN_SHARE) for v in clean.values()),
                same=A["warned"] == E.warned(clean), n=len(A["warned"]), ppv=ppvd, hitsA=int(hitsA), hitsB=int(hitsB))


if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(244, 252))
    for s in seeds:
        r = score(s)
        print("seed %(seed)d margin %(margin).3f clean %(clean_margin).3f same %(same)s n %(n)d ppv %(ppv).3f "
              "cracker hits A %(hitsA)d B %(hitsB)d" % r, flush=True)
