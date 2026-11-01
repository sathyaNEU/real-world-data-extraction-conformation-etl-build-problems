"""The ladder and its neighbours, each a complete pipeline on target/: the median price change, the methodology's
index on every pair (the default path) with the usual repeat-sales filters, and the decisive route with each
defensible reading of its own step. checks.py asserts the sets and margins these return."""
import datetime as dt
import sys
from collections import defaultdict

import numpy as np

import solve as S

SIZE_KINDS = ("extension", "loft", "garage", "conversion", "two storey", "single storey", "dormer")


def is_size(w):
    t = (w["wtype"] + " " + w["desc"]).lower()
    return any(k in t for k in SIZE_KINDS)


def median_route(target, recs=None, ward_of=None):
    recs = recs or S.load_ppd(target)
    ward_of = ward_of or S.load_wards(target)
    by = defaultdict(lambda: defaultdict(list))
    for x in S.standard(recs):
        w = ward_of.get(S.norm_pc(x["postcode"]))
        by[w][x["date"].year].append(x["price"])
    return {w: 100 * (np.median(v[2026]) / np.median(v[2025]) - 1) for w, v in by.items() if w}


def trimmed(target, base, sd=3.0):
    """the default path with pairs whose residual is more than sd standard deviations out dropped, refitted"""
    ward_of = base["ward_of"]
    out = {}
    rows = defaultdict(list)
    for k, a, b in base["pairs"]:
        w = ward_of.get(S.norm_pc(b["postcode"]))
        rows[w].append((a["date"].year, b["date"].year, float(np.log(b["price"] / a["price"]))))
    for w, rr in rows.items():
        lev = S.bmn(rr)
        res = np.asarray([lr - (lev[y2] - lev[y1]) for y1, y2, lr in rr if y1 != y2])
        s = res.std()
        keep = [r for r in rr if r[0] != r[1] and abs(r[2] - (lev[r[1]] - lev[r[0]])) <= sd * s]
        out[w] = S.change(S.bmn(keep))
    return out


def no_newbuild_first(target, drop_works):
    """pairs whose first sale is a new dwelling's first sale left out"""
    R = S.solve(target, drop_works=drop_works)
    prs = [(k, a, b) for k, a, b in R["pairs"] if a["new"] != "Y"]
    idx = S.ward_index(prs, R["ward_of"])
    return {w: S.change(l) for w, l in idx.items()}


def recode_linked(target, drop_works):
    """pairs formed across a June 2021 postcode recode (the terminated postcode's street and number)"""
    import csv
    recs = S.load_ppd(target)
    term = {}
    with open(S.p(target, "pcs"), newline="") as f:
        rows = list(csv.DictReader(f))
    ended = {r["pcds"] for r in rows if r["doterm"]}
    st = S.standard(recs)
    # the successor of a terminated postcode: the postcode its street's later sales carry with the same number
    later = defaultdict(set)
    for x in st:
        later[(x["paon"], x["saon"], x["street"])].add(x["postcode"])
    def key(x):
        k = (x["paon"], x["saon"], x["street"])
        pcs = sorted(later[k])
        return S.addr_key(x["paon"], x["saon"], "+".join(pcs) if any(pc in ended for pc in pcs) else x["postcode"]) + (x["street"],)
    prs = S.pairs_of(st, key=key)
    if drop_works:
        widx = S.works_index(S.load_register(target))
        out = []
        for k, a, b in prs:
            ka = S.addr_key(a["paon"], a["saon"], a["postcode"])
            kb = S.addr_key(b["paon"], b["saon"], b["postcode"])
            ds = widx.get(ka, []) + widx.get(kb, [])
            if any(a["date"] < d < b["date"] for d in ds):
                continue
            out.append((k, a, b))
        prs = out
    idx = S.ward_index(prs, S.load_wards(target))
    return {w: S.change(l) for w, l in idx.items()}


def match_loose(target):
    """works matched on postcode and number alone, flats on the building"""
    R = S.solve(target, drop_works=False)
    reg = S.load_register(target)
    idx = defaultdict(list)
    for w in reg:
        idx[(w["paon"].upper().strip(), S.norm_pc(w["postcode"]))].append(w["completed"])
    prs = [(k, a, b) for k, a, b in R["pairs"]
           if not any(a["date"] < d < b["date"] for d in idx.get((a["paon"].upper(), S.norm_pc(a["postcode"])), []))]
    i2 = S.ward_index(prs, R["ward_of"])
    return {w: S.change(l) for w, l in i2.items()}


def routes(target):
    out = {}
    G = S.solve(target)
    D = S.solve(target, drop_works=False)
    out["R0 median"] = median_route(target, G["recs"], G["ward_of"])
    out["R1 every pair (default)"] = D["change"]
    out["R1 every pair, no update"] = S.solve(target, apply_update=False, drop_works=False)["change"]
    out["R2 every pair, six-month hold"] = S.solve(target, drop_works=False, min_hold=183)["change"]
    out["R2 every pair, WRS"] = S.solve(target, drop_works=False, wrs=True)["change"]
    out["R2 every pair, 3-sd trim"] = trimmed(target, D)
    out["R2 every pair, no new-build first"] = no_newbuild_first(target, False)
    out["R2 every pair, 2019 wards"] = S.solve(target, drop_works=False, wards="19")["change"]
    out["R3 golden"] = G["change"]
    out["R3 size works only"] = S.solve(target, works_kinds=is_size)["change"]
    out["R3 received date"] = S.solve(target, works_use="received")["change"]
    out["R3 loose match"] = match_loose(target)
    out["R3 WRS"] = S.solve(target, wrs=True)["change"]
    out["R3 six-month hold"] = S.solve(target, min_hold=183)["change"]
    out["R3 3-sd trim"] = trimmed(target, G)
    out["R3 no update"] = S.solve(target, apply_update=False)["change"]
    out["R3 no new-build first"] = no_newbuild_first(target, True)
    out["R3 recode linked"] = recode_linked(target, True)
    out["R3 A and B"] = S.solve(target, cats=("A", "B"))["change"]
    out["R3 2019 wards"] = S.solve(target, wards="19")["change"]
    return out


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else S.TARGET
    R = routes(t)
    wards = sorted(R["R3 golden"])
    print("%-36s %s" % ("route", " ".join("%7s" % w[:7] for w in wards)))
    for name, ch in R.items():
        print("%-36s %s  %s" % (name, " ".join("%7.2f" % ch.get(w, float("nan")) for w in wards),
                                ",".join(w[:4] for w in S.pressured(ch))))
