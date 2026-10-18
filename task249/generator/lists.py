import numpy as np, params as P, nodes as N
import subprocess, sys
rows = np.load("/tmp/claude-0/-home-user/ae71c25a-4beb-538a-9fe7-971dc23fc641/scratchpad/t249/rows.npy", allow_pickle=True).item()
gold = sorted(c for c in N.CODES if not P.BAND[0] <= rows[c]["dm_aft"] <= P.BAND[1])
print("golden (dm_aft):", gold, len(gold))
for k in [k for k in rows["OZ01"] if k not in ("d", "r")]:
    L = sorted(c for c in N.CODES if not P.BAND[0] <= rows[c][k] <= P.BAND[1])
    m = min(min(abs(rows[c][k] - P.BAND[0]), abs(rows[c][k] - P.BAND[1])) for c in N.CODES)
    print("%-9s n=%2d extra %-40s missed %-28s min edge %.3f" % (k, len(L), sorted(set(L) - set(gold)), sorted(set(gold) - set(L)), m))
