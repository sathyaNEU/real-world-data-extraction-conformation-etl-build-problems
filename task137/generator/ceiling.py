"""The ask layer measured against the careful solver on the cut pack, and the pair ceiling.

The honest cracker lands the call (350), reads every field by its plain meaning (the receipt's own reference, the fault
column, the net and gross columns, both telematics clocks), executes every filed rule (the fund terms' claim, quarter,
VAT and recovery sentences) and runs the hygiene battery: exact duplicates and re-sent lines dropped, receipts without
our claim number anti-joined and placed by payer and amount, payer names normalised, the overlap week deduplicated.
The mirror stops on the most attractive wrong rung of each ask. Routes beyond the battery (an import-by-import resend
rule, liability shares inferred from amounts) are printed for the record. The full includer must reproduce
figures.json or the script exits 1.

    python3 task137/generator/ceiling.py [target folder]
"""
import collections
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S

TARGET = os.path.join(os.path.dirname(HERE), "target")
SH = [0.75, 2 / 3, 0.5, 1 / 3, 0.25]


def r100(x):
    return int(100 * round(x / 100 + 1e-9))


def score(target=TARGET):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    REG = S.register(target)
    L = S.listing(target)
    CI = S.claim_index(L, REG)
    J = S.jobs(target)
    AP = S.ap(target)
    B = S.bank(target)
    own = {x["Claim no."]: x for x in L}
    xw = S.insurer_crosswalk(L)
    key = lambda x: (x["Supplier Ref"], x["Invoice Date"], x["Description"], x["Net"])
    post = lambda x: dt.datetime.strptime(x["Posting Date"], "%d/%m/%Y").date()

    # B handlings
    def keep_all():
        return list(AP)

    def exact_dedup():
        seen, out = set(), []
        for x in sorted(AP, key=lambda x: (post(x), x["Doc No"])):
            if key(x) in seen:
                continue
            seen.add(key(x))
            out.append(x)
        return out

    def week_twin():
        have = collections.defaultdict(set)
        for x in AP:
            have[key(x)].add(post(x))
        return [x for x in AP if (post(x) - dt.timedelta(days=7)) not in have[key(x)]]

    def week_twin_paired():
        """one-for-one: a line is a resend when an identical line was posted one import earlier and not yet used"""
        pool, out = collections.Counter(), []
        for x in sorted(AP, key=lambda x: (post(x), x["Doc No"])):
            prev = (key(x), post(x) - dt.timedelta(days=7))
            if pool[prev] > 0:
                pool[prev] -= 1
                continue
            pool[(key(x), post(x))] += 1
            out.append(x)
        return out

    def golden_lines():
        return S.genuine_lines(AP, J, CI, REG)

    def b1(lines):
        return {"%s %s" % k: v for k, v in S.repair_costs(lines, J, CI, REG).items()}

    # A handlings: quoted receipts by our number; the rest by the given rule
    def a1(rule, outl):
        t = {q: 0.0 for q in S.QS}
        for x in B:
            if x["Type"] != "BAC" or not x["Paid in"]:
                continue
            payer = xw.get(x["Description"].split()[0])
            if payer is None:
                continue
            d = dt.datetime.strptime(x["Date"], "%d/%m/%Y").date()
            amt = round(float(x["Paid in"]), 2)
            m = re.search(r"\b(RVM\d{6})\b", x["Description"])
            q = S.quarter(CI[m.group(1)]["Incident date"]) if m else rule(d, amt, payer, outl)
            if q in t:
                t[q] += amt
        return t

    def cands(d, amt, payer, outl, shares_split, tol=0.005):
        out = []
        for no, c in own.items():
            if c["Third-party insurer"] != payer or c["Fault"] not in ("Non-fault", "Split") or no not in outl:
                continue
            if c["Incident date"] >= d:
                continue
            sh = [1.0] if c["Fault"] == "Non-fault" else shares_split
            if any(abs(round(outl[no] * s + 1e-9, 2) - amt) < tol for s in sh):
                out.append(no)
        return out

    def by_outlay(fallback):
        def f(d, amt, payer, outl):
            m = cands(d, amt, payer, outl, [])
            return S.quarter(own[m[0]]["Incident date"]) if len(m) == 1 else fallback(d, amt, payer, outl)
        return f

    def shares_exact(d, amt, payer, outl):
        m = cands(d, amt, payer, outl, SH)
        return S.quarter(own[m[0]]["Incident date"]) if len(m) == 1 else None

    def shares_nearest(d, amt, payer, outl):
        best = None
        for no, c in own.items():
            if c["Third-party insurer"] != payer or c["Fault"] not in ("Non-fault", "Split") or no not in outl:
                continue
            if c["Incident date"] >= d:
                continue
            for s in ([1.0] if c["Fault"] == "Non-fault" else SH):
                e = abs(outl[no] * s - amt)
                if best is None or e < best[0]:
                    best = (e, no)
        return S.quarter(own[best[1]]["Incident date"]) if best else None

    drop = lambda d, amt, payer, outl: None
    receipt_q = lambda d, amt, payer, outl: S.quarter(d)

    def kept(a, b):
        ka = sum(r100(a[q]) == F["recoveries_by_collision_quarter"][q] for q in S.QS)
        kb = sum(r100(b[k]) == F["repair_cost_by_depot"][k] for k in F["repair_cost_by_depot"])
        return ka, kb

    rows = []
    lines = {"keep every line": keep_all(), "exact duplicates dropped": exact_dedup(),
             "a line with a twin one import earlier dropped": week_twin(),
             "twins one import earlier paired one for one": week_twin_paired(), "golden": golden_lines()}
    outl = {k: S.outlays(v, J, CI) for k, v in lines.items()}
    routes = [
        ("honest cracker", "exact duplicates dropped", "payer and amount equal to the outlay, else the receipt's quarter",
         by_outlay(receipt_q)),
        ("honest cracker", "exact duplicates dropped", "payer and amount equal to the outlay, else left out", by_outlay(drop)),
        ("honest cracker", "exact duplicates dropped", "left out (no claim number)", drop),
        ("honest cracker", "exact duplicates dropped", "the receipt's quarter", receipt_q),
        ("mirror", "keep every line", "left out (no claim number)", drop),
        ("beyond the battery", "a line with a twin one import earlier dropped", "shares inferred from amounts, exact",
         shares_exact),
        ("beyond the battery", "twins one import earlier paired one for one", "shares inferred from amounts, exact",
         shares_exact),
        ("beyond the battery", "exact duplicates dropped", "shares inferred from amounts, nearest", shares_nearest),
        ("beyond the battery", "twins one import earlier paired one for one", "shares inferred from amounts, nearest",
         shares_nearest),
        ("full includer", "golden", "shares inferred from amounts, exact", shares_exact),
    ]
    print("route | B handling | A orphans | A1 kept of %d | B1 kept of %d" % (len(S.QS), len(F["repair_cost_by_depot"])))
    res = {}
    for who, bh, ah, rule in routes:
        a = a1(rule, outl[bh])
        b = b1(lines[bh])
        ka, kb = kept(a, b)
        res.setdefault(who, []).append((ka, kb))
        print("%s | %s | %s | %d | %d" % (who, bh, ah, ka, kb))
    full = res["full includer"][0]
    if full != (len(S.QS), len(F["repair_cost_by_depot"])):
        print("FULL INCLUDER DOES NOT REPRODUCE figures.json")
        sys.exit(1)
    n = float(len(S.QS) + len(F["repair_cost_by_depot"]))
    lc = max((ka + kb) / n for ka, kb in res["honest cracker"])
    ls = max((ka + kb) / n for ka, kb in res["mirror"])
    lb = max((ka + kb) / n for ka, kb in res["beyond the battery"])
    C = 38 + 7 + 55 * lc
    Sx = 5 + 7 + 55 * ls
    print("ask weight kept: honest cracker %.2f, mirror %.2f, best route beyond the battery %.2f" % (lc, ls, lb))
    print("pair ceiling (cracker on the call, mirror off it): C %.1f, S %.1f, pair %.1f" % (C, Sx, (C + Sx) / 2))
    print("two careful responses on the call: %.1f each" % C)
    print("cracker on the call with the best route beyond the battery: %.1f; pair with the mirror %.1f" % (
        45 + 55 * lb, (45 + 55 * lb + Sx) / 2))
    return {"lc": lc, "ls": ls, "lb": lb, "pair": (C + Sx) / 2}


if __name__ == "__main__":
    score(sys.argv[1] if len(sys.argv) > 1 else TARGET)
