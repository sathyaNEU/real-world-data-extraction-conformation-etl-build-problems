import numpy as np, params as P, design
an = [(a[2], a[3]) for a in P.ANALYSERS]
r2 = np.random.default_rng(21)
pts = []
# town nodes: 2 to 7 km from an analyser; village nodes: 9 to 24 km from the nearest
for k in range(20):
    ax, ay = an[k % 4][0], an[k % 4][1]
    while True:
        a, r = r2.uniform(0, 2 * np.pi), r2.uniform(1.5, 7.0)
        x, y = ax + r * np.cos(a), ay + r * np.sin(a)
        if min(np.hypot(x - bx, y - by) for bx, by in an) > 1.2: break
    pts.append((round(x, 1), round(y, 1)))
while len(pts) < 36:
    x, y = r2.uniform(-32, 30), r2.uniform(-28, 26)
    dd = min(np.hypot(x - bx, y - by) for bx, by in an)
    if 9 <= dd <= 24: pts.append((round(x, 1), round(y, 1)))
dist = np.array([min(np.hypot(x - bx, y - by) for bx, by in an) for x, y in pts])
rs = np.random.default_rng(8)
spans = rs.uniform(0.94, 1.06, 36); offs = rs.normal(0, 1.8, 36)
town = [j for j in range(36) if dist[j] < 8]; vill = [j for j in range(36) if dist[j] >= 8]
low = [town[2], town[9], town[15], vill[3], vill[10]]
high = [vill[1], vill[7], vill[13]]
for j, s in zip(low, [0.76, 0.73, 0.78, 0.75, 0.77]): spans[j] = s
for j, s in zip(high, [1.205, 1.21, 1.20]): spans[j] = s
edge_lo = [vill[0], vill[5], vill[12]]; edge_hi = [vill[4], vill[14]]
for j in edge_lo: spans[j] = 0.905
for j in edge_hi: spans[j] = 1.09
offs[low[0]] = 5.5; offs[low[3]] = 6.0; offs[high[0]] = -5.0
offs[town[4]] = -5.5; spans[town[4]] = 0.94; offs[town[11]] = -5.0; spans[town[11]] = 0.95
import sys
seed = int(sys.argv[1]) if len(sys.argv) > 1 else P.SEED
rows = design.run(spans, offs, pts, seed=seed)
gold = set(low + high)
L = design.lists(rows)
for k, v in L.items():
    print("%-9s n=%2d  extra %s  missed %s" % (k, len(v), sorted(set(v) - gold), sorted(gold - set(v))))
for k in ["dm_pool", "dm_near", "iqr_pool", "q90_pool", "qq_pool", "dm_daily"]:
    m = min(min(abs(e[k] - P.BAND[0]), abs(e[k] - P.BAND[1])) for e in rows)
    dev = max(abs(e[k] - s) for e, s in zip(rows, spans))
    print("%-9s min edge distance %.3f  max |est - span| %.3f" % (k, m, dev))
