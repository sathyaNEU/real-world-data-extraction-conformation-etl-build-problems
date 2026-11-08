"""task197 pair ceiling, measured on the cut pack (weights 38 recommendation and critical components, 7 instruction
following, 55 asks; a response off the call keeps 5 of the 38).

Honest careful cracker: it landed the call, so it has every main-side figure. On the asks it reads every field by
its plain meaning (a preparation row is a bag; deferoxamine is the iron antidote, so every deferoxamine bag treats an
iron poisoning), runs the hygiene battery (exact and near duplicates: none; re-sent rows: none; no patient key to
join on), and groups bags into courses by every natural route, scored at its BEST route per ask (the worst case
for the build): rows over three, clusters of bags within 22, 24 or 26 hours (a course runs about 21) of a course's first bag, and chains
of one dose a few hours apart. Mirror: stopped at rung 0 (per pack sold), off the call, same ask routes.
Single-family responses: one repairs the acetylcysteine grouping only, one the deferoxamine scope only.
Full includer: both repaired; it must reproduce figures.json or the script exits 1.
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import askcalc as ac

TGT = os.path.join(os.path.dirname(HERE), "target")
W_REC, W_INSTR, W_ASK, R_WRONG = 38.0, 7.0, 55.0, 5.0


def ask_routes(bags):
    gold, _ = ac.figures_golden(bags)
    keys = sorted(gold)
    nac_routes = {"rows/3": ac.route_rows_over_three(bags)}
    for w in (22, 24, 26):
        nac_routes["clusters %dh" % w] = ac.route_time_clusters(bags, "NAC", w)
    dfo_plain = {"dose chains 10h": ac.route_dose_chains(bags, "DFO", 10),
                 "dose chains 30h": ac.route_dose_chains(bags, "DFO", 30),
                 "clusters 26h": ac.route_time_clusters(bags, "DFO", 26)}
    nac_gold = {k: gold[k]["nac"] for k in keys}
    dfo_gold = {k: gold[k]["dfo"] for k in keys}
    return gold, keys, nac_routes, dfo_plain, nac_gold, dfo_gold


def score(keys, nac, dfo, gold):
    hit_nac = sum(1 for k in keys if nac.get(k, 0) == gold[k]["nac"])
    hit_dfo = sum(1 for k in keys if dfo.get(k, 0) == gold[k]["dfo"])
    hit_tot = sum(1 for k in keys if nac.get(k, 0) + dfo.get(k, 0) == gold[k]["nac"] + gold[k]["dfo"])
    return hit_nac, hit_dfo, hit_tot


def main():
    bags = ac.load(TGT)
    gold, keys, nac_routes, dfo_plain, nac_gold, dfo_gold = ask_routes(bags)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    n = 3 * len(keys)
    best = None
    rows = []
    for nn, nr in nac_routes.items():
        for dn, dr in dfo_plain.items():
            s = score(keys, nr, dr, gold)
            rows.append((nn, dn, s))
            if best is None or sum(s) > sum(best[2]):
                best = (nn, dn, s)
    print("careful cracker routes (asks kept of %d: acetylcysteine, deferoxamine, together)" % n)
    for nn, dn, s in rows:
        print("  %-12s + %-16s %2d %2d %2d" % (nn, dn, *s))
    kept = sum(best[2])
    # single-family repairs: the best plain route for the other family
    f1 = max((score(keys, nac_gold, dr, gold) for dr in dfo_plain.values()), key=sum)
    f2 = max((score(keys, nr, dfo_gold, gold) for nr in nac_routes.values()), key=sum)
    full = score(keys, nac_gold, dfo_gold, gold)
    rec = {(a["hospital"], a["half"]): a for a in F["antidote"]}
    repro = all(rec[k]["acetylcysteine_courses"] == gold[k]["nac"] and rec[k]["deferoxamine_courses"] == gold[k]["dfo"]
                and rec[k]["antidote_courses"] == gold[k]["nac"] + gold[k]["dfo"] for k in keys)
    C = W_REC + W_INSTR + W_ASK * kept / n
    S = R_WRONG + W_INSTR + W_ASK * kept / n
    C1 = W_REC + W_INSTR + W_ASK * sum(f1) / n
    C2 = W_REC + W_INSTR + W_ASK * sum(f2) / n
    print("cracker on the call: keeps %d of %d ask figures (best route %s + %s) -> %.1f" % (kept, n, best[0], best[1], C))
    print("mirror off the call: keeps %d of %d -> %.1f" % (kept, n, S))
    print("acetylcysteine grouping repaired only: keeps %d of %d -> %.1f" % (sum(f1), n, C1))
    print("deferoxamine scope repaired only: keeps %d of %d -> %.1f" % (sum(f2), n, C2))
    print("full includer: keeps %d of %d, reproduces figures.json: %s" % (sum(full), n, repro))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    print("Mirror leakage: %.1f per cent of the ask weight" % (100.0 * kept / n))
    ok = kept == 0 and (C + S) / 2 <= 60 and C < 70 and C1 < 70 and C2 < 70 and sum(full) == n and repro
    print("VERDICT", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
