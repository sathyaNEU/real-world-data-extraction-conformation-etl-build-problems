"""Every rung, reflex and ask stop computed from the pack's files, for checks.py: the default path (the filers'
five-year averages), the census year, the census year over the filers' reliability ratio, the golden, the reflexes
(a provincial transitory variance; the filers' averages with their own residual swing taken out, instrumented by the
census year, or reweighted to every family's chance of filing; the rank-rank slope), the convention variants of the
semantic fork table, and the asks' stops (young people counted by record, by transfer chain, with duplicate rows
dropped, with the CaseTrack rows left active dropped; spending with the central reversals shared out, with the
negative lines dropped, by calendar year, by office alone)."""
from __future__ import annotations

import collections
import datetime as dt

import numpy as np

import common as K
import deliver as G


class Pack:
    def __init__(self, folder):
        self.folder = folder
        self.D = G.load(folder)
        self.reg = G.family_region(self.D)
        self.kids = G.children(self.D)
        self.s2, self.nhist = G.transitory(self.D)

    def arrays(self, name, kids=None):
        sub = [k for k in (kids or self.kids) if k["region"] == name]
        y = np.array([k["y"] for k in sub])
        x = np.array([k["x"] for k in sub])
        fam = [k["family"] for k in sub]
        filer = np.array([f in self.D["hist"] for f in fam])
        xbar = np.array([np.log(np.mean([self.D["hist"][f][t] for t in K.TAX_YEARS])) if f in self.D["hist"] else np.nan
                         for f in fam])
        return y, x, filer, xbar, fam


def cov(a, b):
    return float(np.cov(a, b)[0, 1])


def var(a):
    return float(np.var(a, ddof=1))


def pooled_s2(pk):
    num = den = 0.0
    for f, h in pk.D["hist"].items():
        lx = np.log(np.array([h[t] for t in K.TAX_YEARS]))
        num += float(((lx - lx.mean()) ** 2).sum())
        den += 4
    return num / den


def _logit(x, t, iters=30):
    X = np.column_stack([np.ones_like(x), x])
    b = np.zeros(2)
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-(X @ b)))
        b = b + np.linalg.solve((X * (p * (1 - p))[:, None]).T @ X, X.T @ (t - p))
    return 1.0 / (1.0 + np.exp(-(X @ b)))


def rungs(pk):
    """Each region's value on every rung and reflex."""
    pool = pooled_s2(pk)
    out = {}
    # family-level filing model for the reweighting reflex, by region, on the census year
    fam_x = {}
    for r in pk.D["cohort"]:
        inc = float(r["parents_total_income_2000"])
        if inc > 0:
            fam_x[r["family_id"]] = np.log(inc * 100.0 / K.CPI[K.CENSUS_YEAR])
    for n in K.NAMES:
        y, x, filer, xbar, fam = pk.arrays(n)
        s2 = pk.s2[n]
        v = var(x)
        fams = sorted({f for f in fam_x if pk.reg[f] == n})
        fx = np.array([fam_x[f] for f in fams])
        p = dict(zip(fams, _logit(fx - fx.mean(), np.array([f in pk.D["hist"] for f in fams], float))))
        wt = np.array([1.0 / p[f] for f, fl in zip(fam, filer) if fl])
        yb, xb = y[filer], xbar[filer]
        my, mx = np.average(yb, weights=wt), np.average(xb, weights=wt)
        out[n] = dict(
            r0=cov(yb, xb) / var(xb),
            r1=cov(y, x) / v,
            r2=(cov(y, x) / v) / (cov(xb, x[filer]) / var(x[filer])),
            gold=cov(y, x) / (v - s2),
            pool=cov(y, x) / (v - pool),
            r1c=cov(yb, xb) / (var(xb) - s2 / 5),
            iv=cov(yb, x[filer]) / cov(xb, x[filer]),
            ipw=float(np.sum(wt * (yb - my) * (xb - mx)) / np.sum(wt * (xb - mx) ** 2)),
            n=len(y), filers=float(filer.mean()))
    # rank-rank: children's and parents' percentile ranks in the province, slope by region
    ally = np.array([k["y"] for k in pk.kids])
    allx = np.array([k["x"] for k in pk.kids])
    ry = (np.argsort(np.argsort(ally, kind="stable"), kind="stable") + 0.5) / len(ally)
    rx = (np.argsort(np.argsort(allx, kind="stable"), kind="stable") + 0.5) / len(allx)
    regs = np.array([k["region"] for k in pk.kids])
    for n in K.NAMES:
        m = regs == n
        out[n]["rank"] = cov(ry[m], rx[m]) / var(rx[m])
    return out, pool


def winner(vals, key):
    order = sorted(K.NAMES, key=lambda n: -vals[n][key])
    return order, vals[order[0]][key] / vals[order[1]][key]


def estimators(pk):
    """The golden under every consistent estimate of each region's transitory variance: within-family deviations
    (the golden), half the squared year-to-year changes, within-family deviations with the census year (in 2005
    dollars) as a sixth year, each family weighted by its children in the sample, and only the families with a child
    in the sample."""
    cen = {}
    for r in pk.D["cohort"]:
        cen[r["family_id"]] = float(r["parents_total_income_2000"])
    kids = collections.Counter(k["family"] for k in pk.kids)
    acc = {n: dict(fd=[0.0, 0], w6=[0.0, 0], pc=[0.0, 0], wc=[0.0, 0]) for n in K.NAMES}
    for f, h in pk.D["hist"].items():
        lx = np.log(np.array([h[t] for t in K.TAX_YEARS]))
        n = pk.reg[f]
        ss = float(((lx - lx.mean()) ** 2).sum())
        a = acc[n]
        a["fd"][0] += float((np.diff(lx) ** 2).sum())
        a["fd"][1] += 8
        if cen[f] > 0:
            l6 = np.concatenate([[np.log(cen[f] * 100.0 / K.CPI[K.CENSUS_YEAR])], lx])
            a["w6"][0] += float(((l6 - l6.mean()) ** 2).sum())
            a["w6"][1] += 5
        if kids[f]:
            a["pc"][0] += ss * kids[f]
            a["pc"][1] += 4 * kids[f]
            a["wc"][0] += ss
            a["wc"][1] += 4
    out = {}
    for n in K.NAMES:
        y, x, _, _, _ = pk.arrays(n)
        c, v = cov(y, x), var(x)
        out[n] = [c / (v - pk.s2[n])] + [c / (v - acc[n][k][0] / acc[n][k][1]) for k in ("fd", "w6", "pc", "wc")]
    return out


def conventions(pk):
    """The golden under the semantic fork table's alternatives: SF2 (earnings in all five years), SF3 (the average
    over earning years only), SF7 (one child per family, the first child number), SF8 (census income left in 2000
    dollars and earnings in current dollars)."""
    D = pk.D
    alt = {"SF2": [], "SF3": [], "SF8": []}
    for r in D["cohort"]:
        inc = float(r["parents_total_income_2000"])
        if inc <= 0:
            continue
        b = int(r["birth_year"])
        e = D["earn"][r["child_id"]]
        real = [e[b + a] * 100.0 / D["cpi"][b + a] for a in K.AGES]
        nominal = [e[b + a] for a in K.AGES]
        region = D["recode"][r["census_region_2001"]]
        base = dict(child=r["child_id"], family=r["family_id"], region=region, x=np.log(inc * 100.0 / D["cpi"][K.CENSUS_YEAR]))
        if all(v > 0 for v in real):
            alt["SF2"].append(dict(base, y=np.log(sum(real) / 5.0)))
        pos = [v for v in real if v > 0]
        if pos:
            alt["SF3"].append(dict(base, y=np.log(sum(pos) / len(pos))))
        if sum(nominal) > 0:
            alt["SF8"].append(dict(base, y=np.log(sum(nominal) / 5.0), x=np.log(inc)))
    seen = set()
    alt["SF7"] = []
    for k in sorted(pk.kids, key=lambda k: k["child"]):
        if k["family"] in seen:
            continue
        seen.add(k["family"])
        alt["SF7"].append(k)
    out = {}
    for key, kids in alt.items():
        out[key] = {}
        for n in K.NAMES:
            sub = [k for k in kids if k["region"] == n]
            y = np.array([k["y"] for k in sub])
            x = np.array([k["x"] for k in sub])
            out[key][n] = cov(y, x) / (var(x) - pk.s2[n])
    return out


# ---------------------------------------------------------------------------------------------- the asks' stops
def ask_a_stops(folder):
    rows = G.read(folder, K.PART)
    reg = G.offices(folder)
    byref = {x["participant_ref"]: x for x in rows}
    par = {x["participant_ref"]: x["transfer_from"] for x in rows if x["transfer_from"]}

    def roots(rs, parent):
        out = set()
        for x in rs:
            ref = x["participant_ref"]
            while ref in parent:
                ref = parent[ref]
            out.add(ref)
        return out

    def count(refs):
        c = collections.Counter(reg[byref[r]["office"]] for r in refs)
        return {n: c.get(n, 0) for n in K.NAMES}

    natural = count([x["participant_ref"] for x in rows])
    chain_roots = roots(rows, par)
    chain = count(chain_roots)
    seen, keep = set(), []
    for rt in sorted(chain_roots):
        x = byref[rt]
        k = (x["office"], x["intake_date"], x["date_of_birth"])
        if k not in seen:
            seen.add(k)
            keep.append(rt)
    dedup = count(keep)
    left = [x for x in rows if not (x["source_system"] == "CaseTrack" and x["status"] == "Active")]
    dropped = count(roots(left, par))
    final = count([x["participant_ref"] for x in rows if x["status"] != "Transferred out"
                   and not (x["source_system"] == "CaseTrack" and x["status"] == "Active")])
    return dict(natural=natural, chain=chain, dedup=dedup, dropped=dropped, final=final)


def ask_b_stops(folder, starts):
    lines = G.read(folder, K.LEDGER)
    reg = G.offices(folder)
    off_all = {o: 0.0 for o in reg}
    acc = {o: 0.0 for o in reg}
    off_2024 = {o: 0.0 for o in reg}
    cen = rev = cen_2024 = 0.0
    for l in lines:
        a = float(l["amount"])
        y = int(l["posting_date"][:4])
        if l["cost_centre"] in reg:
            off_all[l["cost_centre"]] += a
            if l["description"] == "Year-end accrual, mentor fees":
                acc[l["cost_centre"]] += a
            if y >= 2024:
                off_2024[l["cost_centre"]] += a
        elif l["description"].startswith("Reversal of"):
            rev += a
        else:
            cen += a
            if y >= 2024:
                cen_2024 += a

    def share(st, office, central):
        tot = sum(st.values())
        return {name: office[o] + central * st[name] / tot for o, name in reg.items()}

    net = {o: off_all[o] - acc[o] for o in reg}
    out = {}
    for label, st in starts.items():
        out["shared reversal, starts %s" % label] = share(st, off_all, cen + rev)
        out["accruals taken back, starts %s" % label] = share(st, net, cen)
    out["negative lines dropped"] = share(starts["golden"], off_all, cen)
    out["2019 to 2023 postings"] = share(starts["golden"], {o: net[o] - off_2024[o] for o in reg}, cen - cen_2024)
    out["office lines alone"] = {name: off_all[o] for o, name in reg.items()}
    return out, dict(accruals={reg[o]: acc[o] for o in reg}, reversals=rev, central=cen)
