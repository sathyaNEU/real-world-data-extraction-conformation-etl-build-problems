"""Class spreads from the simulated claims under each way of costing the claims no AAC rate covers (generator side;
calc.py reads the pack)."""
import collections
import statistics

import numpy as np

import sim as S
import world as W


def rates_in_effect(prods, rate_idx):
    """{(product key, package, month): [rates of the priced NDCs in effect on the month's first day... any day]}"""
    out = collections.defaultdict(list)
    for p in prods:
        for n in p.ndcs:
            for r in rate_idx.get(n["ndc11"], []):
                for m in S.WMONTHS:
                    if r["effective"] <= m <= r["end"]:
                        out[(p.key, n["pkg"], m)].append(r["rate"])
    return out


def premium_by_class(prods, rie):
    """the carton-to-bottle rate ratio over products where both are priced, by class"""
    out = {}
    for cls in W.SHORTLIST_NAMES:
        rs = []
        for p in prods:
            if p.cls != cls:
                continue
            for m in S.WMONTHS:
                u, b = rie.get((p.key, "U", m)), rie.get((p.key, "B", m))
                if u and b:
                    rs.append(statistics.median(u) / statistics.median(b))
        out[cls] = statistics.median(rs) if rs else W.UD_PREMIUM
    allr = []
    for p in prods:
        for m in S.WMONTHS:
            u, b = rie.get((p.key, "U", m)), rie.get((p.key, "B", m))
            if u and b:
                allr.append(statistics.median(u) / statistics.median(b))
    out["_pooled"] = statistics.median(allr)
    return out


def est(c, rie, prem, how):
    p, n = c["product"], c["ndc"]
    m = S.dt.date(c["fill"].year, c["fill"].month, 1)
    if how == "truth":
        return S.acquisition(n, m)
    if how == "golden":
        xs = rie.get((p.key, n["pkg"], m))
        if xs:
            return statistics.median(xs)
        b = rie.get((p.key, "B", m))
        if b and n["pkg"] == "U":
            return statistics.median(b) * prem[p.cls]
        return None
    if how in ("golden_mean", "golden_class", "golden_pooled", "golden_nofallback"):
        xs = rie.get((p.key, n["pkg"], m))
        b = rie.get((p.key, "B", m))
        if how == "golden_mean" and xs:
            return float(np.mean(xs))
        if how in ("golden_class", "golden_pooled") and n["pkg"] == "U" and b:
            return statistics.median(b) * (prem[p.cls] if how == "golden_class" else prem["_pooled"])
        if how in ("golden_class", "golden_pooled") and xs:
            return statistics.median(xs)
        if how == "golden_nofallback":
            return statistics.median(xs) if xs else None
        if b and n["pkg"] == "U":
            return statistics.median(b) * prem[p.cls]
        return statistics.median(xs) if xs else None
    allx = rie.get((p.key, "B", m), []) + rie.get((p.key, "U", m), [])
    if not allx:
        return None
    if how == "default":
        return statistics.median(allx)
    if how == "default_mean":
        return float(np.mean(allx))
    if how == "lowest":
        return min(allx)
    if how == "highest":
        return max(allx)
    raise ValueError(how)


def spreads(cl, prods, rate_idx, how):
    rie = rates_in_effect(prods, rate_idx)
    prem = premium_by_class(prods, rie)
    out = collections.Counter()
    miss = 0
    for c in cl:
        r = None if how == "truth" else S.rate_on(rate_idx.get(c["ndc"]["ndc11"], []), c["fill"])
        e = r if r is not None else est(c, rie, prem, how)
        if e is None:
            miss += 1
            if how == "golden_nofallback":
                continue
            continue
        out[c["product"].cls] += c["ingredient"] - e * c["qty"]
    return out, miss
