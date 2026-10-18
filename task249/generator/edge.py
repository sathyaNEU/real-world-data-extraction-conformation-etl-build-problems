import numpy as np, params as P, nodes as N
rows = np.load("/tmp/claude-0/-home-user/ae71c25a-4beb-538a-9fe7-971dc23fc641/scratchpad/t249/rows.npy", allow_pickle=True).item()
V = ["dm_pool", "dm_near", "iqr_pool", "q90_pool", "qq_pool", "dm_daily", "deming", "ols_m4", "ols_d", "ols_h", "rom"]
for c in N.CODES:
    vals = [rows[c][k] for k in V[:7]]
    m = min(min(abs(v - P.BAND[0]), abs(v - P.BAND[1])) for v in vals)
    if m < 0.06:
        print(c, "span %.2f" % N.SPAN[c], " ".join("%s %.3f" % (k.replace("_pool", ""), rows[c][k]) for k in V), "min %.3f" % m)
