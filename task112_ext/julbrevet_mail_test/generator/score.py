# Scores a reader's reported ask figures against figures.json: a hit is within half a unit of the stated rounding.
# Usage: python3 -I score.py <figures.json> <reader.json>   (reader.json uses the figures.json keys)
import json, sys
G = json.load(open(sys.argv[1], encoding="utf-8"))
R = json.load(open(sys.argv[2], encoding="utf-8"))
hits, rows = 0, []
for k, v in G.items():
    tol = 0.5 if k.startswith(("B|", "M|none|households")) else 0.05
    got = R.get(k)
    ok = got is not None and abs(float(got) - v) <= tol + 1e-9
    hits += ok
    rows.append(f"{'HIT ' if ok else 'miss'} {k:32s} golden {v:>10} reader {got}")
print("\n".join(rows))
print(f"ask figures kept: {hits} of {len(G)}")
