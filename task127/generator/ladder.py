"""task127: prints every measured figure the design note states (ladder, standing family, grains, book rates, the
ask C organ), read from the cut pack, so no figure in the note rests on a scratch script."""
import math
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as GD  # noqa: E402
import world as W  # noqa: E402

T = os.path.join(os.path.dirname(HERE), "target")
w = W.build()
lines = {c["cid"]: c["line"] for c in w.watch.values()}
name = {c["cid"]: c["name"].replace(" Limited", "") for c in w.watch.values()}
key = {c["key"]: c["cid"] for c in w.watch.values()}
P = GD.Pack(T, lines)
KIN, RID, MAT = key["KIN"], key["RID"], key["MAT"]


def rn(x, u=50_000):
    return int(math.floor(x / u + 0.5)) * u


p1, k1, n1, _ = P.p1(0.30)
p0, k0, n0 = P.p0(0.30)
up = p1 - p0
own = {c: P.own(c) for c in lines}
val = P.values(up)
book = lambda s: sum(val[c] for c in s)
print("p1 %d/%d = %.4f, p0 %d/%d = %.4f, uplift %.4f" % (k1, n1, p1, k0, n0, p0, up))

# ---- the ladder ----
U = P.borrower_universe()
pk = pn = 0
for a, eps in P.episodes.items():
    for s, _ in eps:
        if not (GD.D(2022, 1, 1) <= s <= GD.D(2025, 12, 31)):
            continue
        for p in U:
            if p == a or a not in P.payers_of[p] or P.in_default(p, s):
                continue
            if P.share(p, a, GD.add_months(GD.D(s.year, s.month, 1), -12), GD.D(s.year, s.month, 1)) <= 0:
                continue
            pn += 1
            pk += any(s < t <= GD.add_months(s, 12) for t in P.starts(p))
pooled = pk / pn
rungs = [
    ("R0 largest exposure", {c: sum(float(f["ead_nzd"]) for f in P.borrowers26()[c]) for c in lines}),
    ("R1 own twelve-month", own),
    ("R2 own lifetime", {c: P.own(c, "pd_lifetime") for c in lines}),
    ("R3 own plus payees' own EL", {c: own[c] + sum(P.pd(s) * P.lgd_ead(s) for s in P.dependents(c)) for c in lines}),
    ("R4a assumed uplift 0.25", P.values(0.25)),
    ("R4b pooled over every payee (%d of %d, %.3f)" % (pk, pn, pooled),
     {c: own[c] + P.pd(c) * max(0.0, pooled - p0) * sum(P.lgd_ead(s) for s in P.dependents(c, T=0.0001)) for c in lines}),
    ("golden", val),
]
for lab, v in rungs:
    best, tot, _, _ = P.best_set(v)
    print("%-44s KIN %10.0f RID %10.0f MAT %10.0f | %-40s rung total %10.0f book %10.0f" % (
        lab, v[KIN], v[RID], v[MAT], " and ".join(sorted(name[c] for c in best)), tot, book(best)))
gbest, gtot, runner, rtot = P.best_set(val)
dbest = P.best_set(own)[0]
print("golden %.0f, default set on the book %.0f (step worth %.0f, %.1f per cent), runner-up %s %.0f (%.0f behind)" % (
    gtot, book(dbest), gtot - book(dbest), 100 * (gtot / book(dbest) - 1), " and ".join(sorted(name[c] for c in runner)),
    rtot, gtot - rtot))
print("assumed uplift needed to move the set: %.4f" % ((own[RID] - own[MAT]) / (
    P.pd(MAT) * sum(P.lgd_ead(s) for s in P.dependents(MAT)) - P.pd(RID) * sum(P.lgd_ead(s) for s in P.dependents(RID)))))


# ---- the standing family ----
def p0_never(t):
    nn = kk = 0
    for Y in (2022, 2023, 2024, 2025):
        y0, y1 = GD.D(Y, 1, 1), GD.D(Y + 1, 1, 1)
        for p in sorted(U):
            for a in P.payers_of[p]:
                if P.share(p, a, GD.D(Y - 1, 1, 1), y0) < t or P.starts(a):
                    continue
                if P.in_default(p, y0) or not P._active(p, Y):
                    continue
                nn += 1
                kk += any(y0 <= x < y1 for x in P.starts(p))
    return kk / nn


fm, ft, fr, sets = [], [], [], set()
for t in (0.10, 0.30, 0.45, 0.50):
    for win in (9, 12, 15, 18):
        q1 = P.p1(t, window=win)[0]
        q0 = P.p0(t)[0]
        for v in (P.values(q1 - q0, T=t), P.values(q1 - p0_never(t), T=t), P.values(None, T=t, baseline=q1)):
            fm.append(v[MAT])
            ft.append(v[KIN] + v[MAT])
            fr.append(v[MAT] + v[RID])
            sets.add(tuple(sorted(P.best_set(v)[0])))
print("standing family: %d members, sets %s; Matai %.0f to %.0f (spread %.0f, bins %s); total %.0f to %.0f (bins %s); "
      "runner-up %.0f to %.0f" % (len(fm), [" and ".join(name[c] for c in s) for s in sets], min(fm), max(fm),
                                  max(fm) - min(fm), sorted(set(rn(x) for x in fm)), min(ft), max(ft),
                                  sorted(set(rn(x) for x in ft)), min(fr), max(fr)))

# ---- grains and rates ----
obs = []
for a in sorted(P.episodes):
    for s, _ in P.episodes[a]:
        if not (GD.D(2022, 1, 1) <= s <= GD.D(2025, 12, 31)):
            continue
        for p in sorted(U):
            if p == a or a not in P.payers_of[p] or P.in_default(p, s):
                continue
            sh = P.share(p, a, GD.add_months(GD.D(s.year, s.month, 1), -12), GD.D(s.year, s.month, 1))
            if sh > 0:
                obs.append((sh, s.year, P.cust[a]["sector"], any(s < t <= GD.add_months(s, 12) for t in P.starts(p))))
hi = [o for o in obs if o[0] >= 0.30]
lo = [o for o in obs if o[0] < 0.30]
print("payees above the threshold %d of %d; below it %d of %d" % (sum(o[3] for o in hi), len(hi), sum(o[3] for o in lo), len(lo)))
for lab, f in (("payer-default year", lambda o: o[1]), ("payer division", lambda o: o[2]),
               ("share band", lambda o: "<0.60" if o[0] < 0.6 else ("0.60-0.75" if o[0] < 0.75 else ">=0.75"))):
    g = defaultdict(lambda: [0, 0])
    for o in hi:
        g[f(o)][0] += o[3]
        g[f(o)][1] += 1
    print("by %s: %s" % (lab, {k: "%d/%d" % tuple(v) for k, v in sorted(g.items())}))


def vals_rate(rate):
    out = {}
    for c in lines:
        v = P.own(c)
        for d in P.dependents(c):
            v += P.pd(c) * max(0.0, rate(P.share(d, c, GD.D(2026, 1, 1), GD.D(2027, 1, 1))) - p0) * P.lgd_ead(d)
        out[c] = v
    return out


for cut in (0.55, 0.60, 0.65, 0.70, 0.75):
    a_ = [o for o in hi if o[0] < cut]
    b_ = [o for o in hi if o[0] >= cut]
    ra, rb = sum(o[3] for o in a_) / len(a_), sum(o[3] for o in b_) / len(b_)
    v = vals_rate(lambda x: ra if x < cut else rb)
    print("two bands at %.2f: %d/%d and %d/%d, Matai %.0f (%d), total %.0f (%d), set %s" % (
        cut, sum(o[3] for o in a_), len(a_), sum(o[3] for o in b_), len(b_), v[MAT], rn(v[MAT]), v[KIN] + v[MAT],
        rn(v[KIN] + v[MAT]), " and ".join(sorted(name[c] for c in P.best_set(v)[0]))))
for Y in (2022, 2023, 2024, 2025):
    y0, y1 = GD.D(Y, 1, 1), GD.D(Y + 1, 1, 1)
    base = [c for c in U if not P.in_default(c, y0) and P._active(c, Y)]
    k = sum(1 for c in base if any(y0 <= t < y1 for t in P.starts(c)))
    print("%d book default rate %d/%d = %.3f" % (Y, k, len(base), k / len(base)))
print("Matai's dependants:", sorted((round(P.share(d, MAT, GD.D(2026, 1, 1), GD.D(2027, 1, 1)), 3), P.cust[d]["trading"],
                                     P.cust[d]["sector"]) for d in P.dependents(MAT)))

# ---- ask C's organ ----
import csv  # noqa: E402
import re  # noqa: E402
acct = set(P.acct)
c_yr = Counter()
for r in csv.DictReader(open(os.path.join(T, "default_register_2021-2026.csv"))):
    if not r["reference"].startswith("C") and re.sub(r"\D", "", r["reference"]) not in acct:
        c_yr[r["trigger_date"][:4]] += 1
print("register rows keyed to a loan account by year:", dict(sorted(c_yr.items())))
g = P.sector_table()
n = P.sector_table(keys="noloan")
print("2025 defaults: %d with loan rows resolved, %d without" % (sum(v[3] for v in g.values()), sum(v[3] for v in n.values())))
print("ask C drop when loan rows are left unkeyed: min %.2f points" % min(g[s][0] - n[s][0] for s in g))
