import numpy as np, params as P, heads as H, sim
w0, w1 = H.window()
res = []
for seed in range(249, 279):
    t = sim.field(H.sites(), seed=seed)
    A = t[:4, w0:w1]
    sd = A.std(1)
    nodes_sd = t[4:40, w0:w1].std(1) / A.reshape(-1).std()
    res.append((sd.max() / sd.min(), seed, np.abs(nodes_sd - 1).max()))
for r in sorted(res)[:8]:
    print("seed %d analyser sd spread %.3f  max node dev %.3f" % (r[1], r[0], r[2]))
