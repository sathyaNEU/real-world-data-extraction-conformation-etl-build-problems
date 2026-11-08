import sys, numpy as np, pandas as pd
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from world4 import make, LIMIT
P = {}
for kv in sys.argv[2:]:
    k, v = kv.split("="); P[k] = float(v)
S, Lv, meta = make(int(sys.argv[1]), P)
wy = Lv.index.year
for w in ("C", "D", "D2", "D3", "F2", "R", "N3"):
    pk = Lv[w].groupby(wy).max()
    print(f"{w:3s} peaks 2018-27:", " ".join(f"{pk[y]:.2f}" for y in range(2018, 2028)),
          f"| zc/floor {meta.get('zc') if w=='C' else meta.get(w, float('nan')):.2f}")
    g = S[(S.well == w) & (S.boron > LIMIT)]
    print("     exc:", " ".join(f"{d:%Y-%m}:{int(b)}" for d, b in zip(g.date, g.boron)))
