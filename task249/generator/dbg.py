import numpy as np, params as P, sim, tune
exec(open("trial2.py").read().split("import sys")[0])
rng = np.random.default_rng(250)
true = sim.field(an + pts, rng)
i0, i1 = tune.window_idx()
A = true[:4, i0:i1]; N = true[4:, i0:i1]
print("analyser SDs", A.std(1).round(2), "pool", A.reshape(-1).std().round(2), "means", A.mean(1).round(1))
sd_true = N.std(1)
print("node true SD: min %.2f max %.2f mean %.2f" % (sd_true.min(), sd_true.max(), sd_true.mean()))
print("node true means: min %.1f max %.1f" % (N.mean(1).min(), N.mean(1).max()))
dev = sd_true / A.reshape(-1).std()
for j in np.argsort(np.abs(dev - 1))[-6:]:
    print(j, "dist %.1f" % dist[j], "trueSD ratio %.3f" % dev[j], "mean %.1f" % N[j].mean(), "min %.1f" % N[j].min())
