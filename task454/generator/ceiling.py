"""The ask layer measured on the cut pack (target/ only): every route a careful solver could file through the two
asks, and the pair arithmetic.

The cracker lands the call, reads every field by its plain meaning (approved_aud as the claim's approved amount,
agreement_ref as the agreement a transfer quotes, the register's paid to 31 December 2025, status and final cost, a
receipt's payer and amount), executes the closure decision as worded and runs the hygiene battery: the 20 March
transfers that repeat the 19 March run line for line are dropped as duplicates; each transfer is paired to the claims
it pays where one claim, or claims of one agreement, equal it (the pairing of a header amount to its rows) and is
otherwise booked to the agreement it quotes; a receipt equal to a council's repeat is paired off with it as its return
and every other receipt is read as money the council returned unspent. The stops are the other complete pipelines a
careful solver could file: claims taken as paid (all of them, the ones a transfer equals one for one, the ones approved
in time for the year's last run), receipts net of every repeat the council was sent, and the register's paid amount
less final cost on closed agreements. The full includer splits each transfer into the claims it paid, across
agreements, and each receipt into the repeat and the unspent money it returns; it reproduces figures.json or this
script exits 1. Weights: 38 the call and its components, 7 instruction-following, 55 the asks (23 figures).
Run: python3 task454/generator/ceiling.py
"""
import os, sys, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reader


def main():
    T = os.path.join(os.path.dirname(HERE), "target")
    z = os.path.join(os.path.dirname(HERE), "target.zip")
    P = reader.load(T)
    f = json.load(open(os.path.join(HERE, "figures.json")))
    names = P["names"]
    regions = [r for r in names if r != "WST"]
    pop = reader.region_pop(P)
    months, days = reader.presence(P)

    def main_answers(is_visitor):
        q = reader.visitor_spend(P, is_visitor)
        pr = {r: sum(q[r]) / pop[r] for r in regions}
        o = sorted(regions, key=lambda r: (-pr[r], pop[r]))
        return {"set": set(o[:5]), "first": o[5], "gap": int(round(pr[o[4]])) - int(round(pr[o[5]])),
                "pr": {r: int(round(pr[r])) for r in regions}, "q": {r: [int(round(x / 1000.0)) * 1000 for x in q[r]] for r in regions}}

    def main_score(a):
        s = 12.0 * (a["set"] == set(f["call_codes"]))
        s += 3.0 * (names[a["first"]] == f["first_below"]) + 3.0 * (a["gap"] == f["gap_per_resident"])
        s += sum(1.0 for r in regions if abs(a["pr"][r] - f["per_resident_%s" % r]) <= 0.5)
        cells = sum(1 for r in regions for i in range(4) if abs(a["q"][r][i] - f["q_%s" % r][i]) <= 500)
        s += 9.0 * cells / (4 * len(regions))
        return s

    def kept(A, B):
        ka = sum(1 for r in regions if abs(A[names[r]] - f["remaining_%s" % r]) <= 0.5)
        kb = sum(1 for r in regions if abs(B[names[r]] - f["unspent_%s" % r]) <= 0.5)
        tot = 12_000_000 + sum(B.values()) - sum(A.values())
        kg = int(abs(tot / 5 - f["grant_each"]) <= 0.5)
        return ka, kb, kg

    routine = lambda cid, reg: len(months[(cid, reg)]) >= 6 and days[(cid, reg)] >= 30
    golden = main_answers(lambda row: not routine(row[0], row[1]))

    def home(sa2):
        if sa2 in P["shares"] and P["shares"][sa2]:
            return max(P["shares"][sa2], key=P["shares"][sa2].get)
        return P["sa2_region"].get(sa2, "IS")
    rung0 = main_answers(lambda row: home(row[3]) != row[1])

    n = 2 * len(regions) + 1
    R = reader.ask_routes(P)
    print("pack md5 %s" % hashlib.md5(open(z, "rb").read()).hexdigest() if os.path.exists(z) else "pack md5 (no zip)")
    print("ask figures: %d (11 remaining on open agreements, 11 unspent money returned, 1 grant each)" % n)
    print("routes through the asks (figures kept of 11, 11 and the grant):")
    res = {}
    for k, (A, B) in R.items():
        res[k] = kept(A, B)
        ka, kb, kg = res[k]
        print("  %-30s remaining %2d  unspent %2d  grant %d  total %2d of %d" % (k, ka, kb, kg, ka + kb + kg, n))
    kc = sum(res["cracker"])
    kg_full = sum(res["golden"])
    stops = [k for k in res if k not in ("golden", "cracker")]
    best_a = max(stops, key=lambda k: res[k][0])
    best_b = max(stops, key=lambda k: res[k][1])
    worst = res[best_a][0] + res[best_b][1]
    C = main_score(golden) + 7 + 55.0 * kc / n
    S = main_score(rung0) + 7 + 55.0 * kc / n
    print("cracker on the asks keeps %d of %d; full includer keeps %d of %d" % (kc, n, kg_full, n))
    print("cracker (on the call): main %.1f of 38, total %.1f" % (main_score(golden), C))
    print("mirror (rung 0, %s): main %.1f of 38, total %.1f" % (", ".join(sorted(rung0["set"])), main_score(rung0), S))
    print("two careful responses on the call: %.1f each" % C)
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * kc / n))
    print("best stop per ask: remaining by %r (%d), unspent by %r (%d); a response on the call taking both: %.1f"
          % (best_a, res[best_a][0], best_b, res[best_b][1], main_score(golden) + 7 + 55.0 * worst / n))
    Ac, Bc = R["cracker"]
    for r in regions:
        print("  %s remaining %d (cracker %d)  unspent %d (cracker %d)" % (r, f["remaining_%s" % r], round(Ac[names[r]]),
                                                                          f["unspent_%s" % r], round(Bc[names[r]])))
    if kg_full != n:
        print("FULL INCLUDER DOES NOT REPRODUCE figures.json")
        sys.exit(1)
    if (C + S) / 2 > 60 or kc > 0 or C >= 70:
        sys.exit(1)


if __name__ == "__main__":
    main()
