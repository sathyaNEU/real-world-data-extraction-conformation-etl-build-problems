"""Design-time prototype: each segment's pilot economics at large N (the expected rates, severities, place-days and
team-year values) behind world.DESIGN, and the allocations every rung would file. Usage: design.py [N] [out.json]."""
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402

import common as K  # noqa: E402
import world as W  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 60000
out = {}
for seg in K.PROG:
    rg = np.random.default_rng(7)
    cs = []
    days = (K.PILOT_END - K.PILOT_START).days
    for i in range(2 * N):
        d = K.PILOT_START + dt.timedelta(days=int(rg.integers(0, days)))
        u = rg.random()
        lag = 0 if u < 0.12 else (int(rg.integers(1, 4)) if u < 0.72 else (int(rg.integers(4, 15)) if u < 0.94 else int(rg.integers(15, 91))))
        inj = d - dt.timedelta(days=lag)
        db = inj + dt.timedelta(days=0 if rg.random() < 0.7 else 1)
        if db > d: db = d
        c = W.Claim(cid=i, seg=seg, office="STL", klass="0", injury=inj, report=d, intake=True, dis_began=db)
        c.triage = K.next_working(d)
        c.arm = "E" if i % 2 == 0 else "U"
        cs.append(c)
    L = W._lat(np.random.default_rng(11), len(cs))
    f = W._course(seg, cs, L, [c.arm for c in cs])
    E = [i for i, c in enumerate(cs) if c.arm == "E"]; U = [i for i, c in enumerate(cs) if c.arm == "U"]
    pu = np.mean([cs[i].ind for i in U]); pe = np.mean([cs[i].ind for i in E])
    mu = np.mean([cs[i].indemnity for i in U if cs[i].ind]); me = np.mean([cs[i].indemnity for i in E if cs[i].ind])
    fl = np.array([f[i] * (1 + 0.012 * 8.0 / max(f[i], 1)) for i in E])  # reopen allowance approx
    Lall = float(np.mean([f[i] for i in E])) + 0.012 * 8.0
    Lcl = float(np.mean([f[i] for i in E if cs[i].ind])) + 0.012 * 8.0
    D = pu * mu - pe * me; d = mu - me
    out[seg] = dict(pU=pu, pE=pe, mU=mu, mE=me, Lall=Lall, Lcl=Lcl, D=D, d=d, V=7300 * D / Lall, Vd=7300 * d / Lcl, Vic=7300 * D / Lcl,
                    kept=float(np.mean([cs[i].kept for i in E])))
    o = out[seg]
    print(f"{seg}: pU {pu:.3f} pE {pe:.3f} kept {o['kept']:.3f} mU {mu:7.0f} mE {me:7.0f} d% {100*d/mu:5.1f} Lall {Lall:5.1f} Lcl {Lcl:5.1f} D {D:6.0f} V {o['V']/1e3:6.1f}k Vd {o['Vd']/1e3:6.1f}k Vic {o['Vic']/1e3:6.1f}k", flush=True)
if len(sys.argv) > 2:
    json.dump(out, open(sys.argv[2], "w"), indent=1)
VOL = {s: W.VOLUME[s] * (1 + W.GROWTH[s[:2]]) ** 3.5 for s in K.PROG}
def alloc(vals, Lcap=None):
    order = sorted(K.PROG, key=lambda s: -vals[s]); a = {s: 0 for s in K.PROG}; left = 17
    for s in order:
        cap = 3 if Lcap is None else min(3, int(VOL[s] * Lcap[s] / 7300))
        t = min(cap, left); a[s] = t; left -= t
    return a, order
for key, val, cap in [("V", "V", "Lall"), ("V", "V", None), ("Vd", "Vd", "Lcl"), ("Vic", "Vic", "Lcl"), ("D", "V", "Lall")]:
    a, o = alloc({s: out[s][key] for s in K.PROG}, None if cap is None else {s: out[s][cap] for s in K.PROG})
    tot = sum(a[s] * out[s][val] for s in K.PROG)
    print(f"{key:4s} cap={cap}", " ".join(f"{s}:{a[s]}" for s in K.PROG), f"{tot/1e6:.3f}M", ">".join(o))
print({s: round(VOL[s] * out[s]["Lall"] / 7300, 2) for s in K.PROG})
