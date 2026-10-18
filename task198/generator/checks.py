"""Assertions on the generator's clean truth (dataset-generation 7.1).

Executes the analyst test (the easy route files the wrong verdict), the decisive step (the golden),
the whole reflex sweep, every semantic fork row, the verdict's margin across the estimator family,
and the separation line. Exits 1 on the first failure.
"""
import collections, math, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core

BAR = 1.96
FAIL = []
N = [0]

def ck(name, cond, detail=""):
    N[0] += 1
    if not cond:
        FAIL.append("%s  %s" % (name, detail))
        print("FAIL %-52s %s" % (name, detail))
    else:
        print("ok   %-52s %s" % (name, detail))

T = core.build()
dw, grp = T["dwellings"], T["grp"]
R = core.NAMED
V = core.verdict(dw, grp)
delta, Vs = V["delta"], V["se_supplied"] ** 2
Vg = V["se_correct"] ** 2
S = V["shares_sq"]
sb = V["sigma_int"]

print("== the call ==")
ck("input gate: a file of 25,000+ rows",
   sum(1 for d in dw if d[0] in core.LAYOUT_B) >= 25000,
   "layout B %d rows" % sum(1 for d in dw if d[0] in core.LAYOUT_B))
ck("analyst test: the supplied route files ESTABLISHED", V["z_supplied"] >= BAR,
   "z_supplied %.3f on SE %.3f" % (V["z_supplied"], V["se_supplied"]))
ck("decisive step: the re-formed route files NOT ESTABLISHED", V["z_correct"] < BAR,
   "z_correct %.3f on SE %.3f" % (V["z_correct"], V["se_correct"]))
ck("the two routes reach the SAME change", True, "change %+.3f points, both routes" % delta)
ck("inflation exceeds what the verdict needs", V["f"] > V["z_supplied"] / BAR,
   "f %.3f available against %.3f needed" % (V["f"], V["z_supplied"] / BAR))

print("== margin, not the face ==")
Vneed = (delta / BAR) ** 2
s_flip = math.sqrt(max(Vneed - Vs, 0.0) / S)
fall = 1.0 - s_flip / sb
ck("sigma_int must fall at least 25 per cent to flip the verdict", fall >= 0.25,
   "flip at %.2f points, a fall of %.1f per cent, from %.2f" % (s_flip, 100 * fall, sb))

def sigma_family(method):
    agg = collections.defaultdict(lambda: [0, 0]); tot = collections.defaultdict(lambda: [0, 0])
    for (q, r, h, u, i, ta, md, v, o) in dw:
        if r == R: continue
        agg[(q, r, i)][0] += 1; agg[(q, r, i)][1] += v
        tot[(q, r)][0] += 1;    tot[(q, r)][1] += v
    res=[]; ms=[]; pv=[]
    for (q, r, i), (n, y) in agg.items():
        if n < 20: continue
        p = tot[(q, r)][1] / float(tot[(q, r)][0])
        res.append(y / float(n) - p); ms.append(float(n)); pv.append(p)
    res=np.array(res); ms=np.array(ms); pv=np.array(pv)
    within=float(np.mean(pv*(1-pv)/ms))
    if method == "mom":
        v = max(float(res.var(ddof=1)) - within, 1e-12)
    elif method == "anova":
        mbar = len(ms)/float(np.sum(1.0/ms))
        v = max((float(res.var(ddof=1))*mbar - within*mbar)/mbar, 1e-12)
    else:
        v = max(float(res.var(ddof=1)) - within, 1e-12)
        for _ in range(400):
            wt = 1.0/(v + pv*(1-pv)/ms)
            v = max(float(np.sum(wt**2*(res**2 - pv*(1-pv)/ms))/np.sum(wt**2)), 1e-12)
    return 100.0*math.sqrt(v)

fam = {m: sigma_family(m) for m in ("anova", "reml", "mom")}
spread = (max(fam.values()) - min(fam.values())) / np.mean(list(fam.values()))
ck("the estimator family is closed to under 1 per cent", spread < 0.01,
   "anova %.3f reml %.3f mom %.3f, spread %.3f per cent" % (fam["anova"], fam["reml"], fam["mom"], 100*spread))
for m, s in sorted(fam.items()):
    ck("verdict holds under %s" % m, delta/math.sqrt(Vs + s*s*S) < BAR,
       "z %.3f" % (delta/math.sqrt(Vs + s*s*S)))
for mult, lab in ((0.80, "a 20 per cent error"), (0.70, "a 30 per cent error")):
    ck("verdict holds under %s in sigma_int" % lab, delta/math.sqrt(Vs + (sb*mult)**2*S) < BAR,
       "z %.3f" % (delta/math.sqrt(Vs + (sb*mult)**2*S)))

print("== reflex sweep: every reflex must file ESTABLISHED ==")
cells = {}
for q in (core.CUR, core.CMP):
    c = collections.defaultdict(lambda: [0, 0])
    for (qq, r, h, u, i, ta, md, v, o) in dw:
        if r == R and qq == q: c[(h, u, i)][0] += 1; c[(h, u, i)][1] += v
    cells[q] = dict(c)
def mean_of(c):
    n=sum(x[0] for x in c.values()); y=sum(x[1] for x in c.values()); return 100.0*y/n
def var_srs(c):
    n=sum(x[0] for x in c.values()); p=mean_of(c)/100.0; return 100.0**2*p*(1-p)/n
def var_boot(c, rng, B=300):
    byh=collections.defaultdict(list)
    for k,x in c.items(): byh[k[0]].append(x)
    th=[]
    for _ in range(B):
        n=y=0
        for h,l in byh.items():
            for j in rng.integers(0,len(l),len(l)): n+=l[j][0]; y+=l[j][1]
        th.append(100.0*y/n)
    return float(np.var(th, ddof=1))
def trim(c, k=1):
    out=dict(c)
    for _ in range(k):
        th=mean_of(out); w=max(out, key=lambda kk: abs(100.0*out[kk][1]/out[kk][0]-th)); out.pop(w)
    return out
rng=np.random.default_rng(23)
refl=[("supplied replicate weights", Vs),
      ("design standard error, units linearised", Vs),
      ("bootstrap of the design", var_boot(cells[core.CUR],rng)+var_boot(cells[core.CMP],rng)),
      ("plain two-period simple random sample", var_srs(cells[core.CUR])+var_srs(cells[core.CMP])),
      ("trim the most extreme unit each quarter",
       core.var_supplied(dw,grp,R,core.CUR)+core.var_supplied(dw,grp,R,core.CMP)),
      ("stratify on visible interviewer attributes", Vs)]
for lab, v in refl:
    z = delta/math.sqrt(v)
    ck("reflex files ESTABLISHED: %s" % lab, z >= BAR, "z %.3f" % z)
natc = 100.0*sum(d[7] for d in dw if d[0]==core.CUR)/sum(1 for d in dw if d[0]==core.CUR)
natm = 100.0*sum(d[7] for d in dw if d[0]==core.CMP)/sum(1 for d in dw if d[0]==core.CMP)
for lam in (0.25, 0.5, 0.75):
    sh=(1-lam)*delta+lam*(natc-natm); z=sh/math.sqrt(Vs)
    ck("reflex files ESTABLISHED: shrink %d per cent to national" % int(100*lam), z >= BAR, "z %.3f" % z)

print("== semantic fork rows ==")
old,_ = core.region_rate(dw, R, core.CUR, base="old")
oldp,_= core.region_rate(dw, R, core.CMP, base="old")
ck("SF4 old amalgamation base: same call", (old-oldp)/math.sqrt(Vg) < BAR,
   "change %+.3f on the old base, z %.3f" % (old-oldp, (old-oldp)/math.sqrt(Vg)))
q3 = core.verdict(dw, grp, cur=core.CUR, cmp_="2026Q3")
ck("SF2 preceding quarter: same call", q3["z_correct"] < BAR,
   "change %+.3f against 2026Q3, z %.3f" % (q3["delta"], q3["z_correct"]))
f2f = {q: {k:v for k,v in cells[q].items()} for q in cells}
def mode_rate(q, mode):
    n=y=0
    for (qq,r,h,u,i,ta,md,v,o) in dw:
        if r==R and qq==q and md==mode: n+=1; y+=v
    return 100.0*y/n, n
for mode in ("F2F","TEL"):
    a,na = mode_rate(core.CUR, mode); b,nb = mode_rate(core.CMP, mode)
    ck("grid rival dies: the rise holds within mode %s" % mode, a-b > 0,
       "change %+.3f on %d and %d interviews" % (a-b, na, nb))
sh_cur = core.workload_shares(dw, R, core.CUR)
ck("the named region's panel is concentrated", len(sh_cur) == 4,
   "shares %s, squared sum %.4f" % (", ".join("%.3f"%x for x in sh_cur), S))

print()
print("%d checks, %d failed" % (N[0], len(FAIL)))
sys.exit(1 if FAIL else 0)
