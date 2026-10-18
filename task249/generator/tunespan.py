"""Scratch: estimators per node on the window for the current SPAN and ZERO, from the realised field."""
import numpy as np, params as P, nodes as N, heads as H, sim, tune
true = sim.field(H.sites(), exposure=H.exposure())
w0, w1 = H.window()
A = true[:4, w0:w1]; pool = A.reshape(-1); m4 = A.mean(0)
an = [(a[2], a[3]) for a in P.ANALYSERS]
rows = {}
for c, m, x, y in N.NODES:
    if c in N.MOVES: x, y = N.MOVES[c][0], N.MOVES[c][1]
    k = int(np.argmin([np.hypot(x - ax, y - ay) for ax, ay in an]))
    node = H.readings(true, c)[w0:w1]
    e = tune.estimators(node, A[k], pool)
    hr = (np.arange(w0, w1) + 2) % 24                      # local hour (CEST) of each window hour
    aft = (hr >= 12) & (hr < 18)
    e["dm_aft"] = node[aft].std() / A[:, aft].reshape(-1).std()
    e["iqr_aft"] = np.subtract(*np.percentile(node[aft], [75, 25])) / np.subtract(*np.percentile(A[:, aft].reshape(-1), [75, 25]))
    e["q90_aft"] = np.subtract(*np.percentile(node[aft], [90, 10])) / np.subtract(*np.percentile(A[:, aft].reshape(-1), [90, 10]))
    for nm, (a0, a1) in {"aft1117": (11, 17), "aft1317": (13, 17), "aft1216": (12, 16)}.items():
        m = (hr >= a0) & (hr < a1)
        e[nm] = node[m].std() / A[:, m].reshape(-1).std()
    e["near_aft"] = node[aft].std() / A[k, aft].std()
    e["ols_m4"] = np.polyfit(m4, node, 1)[0]
    e["d"] = min(np.hypot(x - ax, y - ay) for ax, ay in an)
    rows[c] = e
np.save("/tmp/claude-0/-home-user/ae71c25a-4beb-538a-9fe7-971dc23fc641/scratchpad/t249/rows.npy", rows, allow_pickle=True)
for c, e in rows.items():
    print(c, "d=%4.1f" % e["d"], " ".join("%s %.3f" % (k, v) for k, v in e.items() if k not in ("d",)))
