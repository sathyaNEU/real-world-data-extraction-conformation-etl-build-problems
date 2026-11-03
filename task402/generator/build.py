"""Build task402: world, pack under target/, goldens, figures.json, metadata.json, target.zip. Deterministic."""
import json, os, shutil, sys, zipfile
import numpy as np
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world, asks, pack, golden, deliver
from normal import normalise

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def nudge(W, F, O, R, seed=4026):
    """Move ask figures off their rounding edges with ordinary rows: a recloser's lone sequence dropped, a crew's last
    job ending a few minutes later. Neither touches a device row or the main call's population."""
    rng = np.random.default_rng(seed)
    S = W["S"]
    for _ in range(400):
        A = asks.maifi(O, S, "golden")
        bad = [(d, q) for d in range(4) for q in range(4) if edge(A[d, q], 0.01) < 0.0007 * 1.5]
        if not bad:
            break
        d, q = bad[0]
        tr = O[(O.kind == "R") & (~O.lockout) & (O.op == "TRIP")]
        tr = tr[[S.district.values[int(i)] == d for i in tr.id.values]]
        tr = tr[asks.quarter(asks.local_ts(tr.t.values)) == q + 1]
        lone = [s for s in tr.seq.unique() if not ((O.kind == "B") & (abs(O.t - tr.t[tr.seq == s].min()) < 5)).any()]
        if not lone:
            break
        O = O[O.seq != lone[int(rng.integers(len(lone)))]]
    for _ in range(600):
        h, p = asks.callout_figures(R, "golden")
        bad = [m for m in range(12) if edge(h[m], 1) < 0.07 * 1.5 or edge(p[m], 1) < 0.07 * 1.5]
        if not bad:
            break
        m = bad[0]
        mon = [(world.D0 + pd.Timedelta(days=int(s // 1440))).month for s in R.s.values]
        want = (m + 10 - 1) % 12 + 1
        last = R.sort_values("e").groupby(["emp", "chain"]).tail(1)
        cand = [i for i in last.index if mon[R.index.get_loc(i)] == want and R.wo_type[i] == "OUTAGE"]
        i = cand[int(rng.integers(len(cand)))]
        e2 = R.e[i] + int(rng.integers(1, 6))
        if (e2 // 1440) != (R.s[i] // 1440):
            continue
        R.loc[i, "e"] = e2
    return O, R


def truth():
    """The world and the asks' worlds after the nudge, rebuilt in process (checks.py reads the same)."""
    W = world.run(world.P)
    F = normalise(W, world.P["seed"] + 7)
    O = asks.scada(W, F, 4024)
    R, EMP, chains = asks.crew(W, F, 4025)
    O, R = nudge(W, F, O, R)
    return W, F, O, R, EMP


def main():
    W = world.run(world.P)
    F = normalise(W, world.P["seed"] + 7)
    O = asks.scada(W, F, 4024)
    R, EMP, chains = asks.crew(W, F, 4025)
    O, R = nudge(W, F, O, R)
    if os.path.isdir(T):
        shutil.rmtree(T)
    os.makedirs(T)
    meta = pack.build(T, W, F, O, R, EMP)
    P, m, a, h, p = golden.all_figures(T)
    figs = deliver.write(TASK, P, m, a, h, p)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    deliver.metadata(TASK)
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(T)):
            zi = zipfile.ZipInfo("target/" + f, date_time=(2026, 10, 27, 9, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(T, f), "rb").read())
    print(json.dumps({k: figs[k] for k in ("call", "costs")}, indent=1))


if __name__ == "__main__":
    main()
