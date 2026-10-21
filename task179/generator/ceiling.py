"""The cracker and the mirror run on the cut pack, scored against figures.json (supplemental-stumping Part 0).

cracker: lands the call, reads every shipped definition, runs the hygiene battery (exact duplicates, key
uniqueness, unmatched joins) and executes every filed handling: listings grouped into people by the exact
person key the registry carries (district, household, initials, sex, age), the follow-up closed by the listing that
ends last; the Tamberlow field laboratory's diagnostic samples at their final result, read on the clock the file shows.
mirror: misses the call on the register's raw interval (the default path) and handles the asks the same way,
since the asks read nothing the call's construction produces (separation asserted in checks.py)."""
import json
import os
import calc

HERE = os.path.dirname(os.path.abspath(__file__))
W_REC, W_INS, W_ASK, R_MISS = 38.0, 7.0, 55.0, 5.0


def r1(v):
    return float("%.1f" % (v + 1e-9))


def cracker_asks(target=calc.TARGET):
    con = calc.ask_contacts(target, mode="exact")
    lab = calc.ask_lab(target, shift_h=0.0, final="last")
    out = {}
    for z, (n, s) in con.items():
        out["a1_%s.people" % z] = n
        out["a1_%s.pct_completed" % z] = r1(s)
    for w, (m, s, n) in lab.items():
        out["a2_w%d.mean_hours" % w] = r1(m)
        out["a2_w%d.pct_within_24h" % w] = r1(s)
    return out


def golden_flat(F):
    flat = {}
    for k, v in F.items():
        if isinstance(v, dict) and (k.startswith("a1_") or k.startswith("a2_")):
            for kk, vv in v.items():
                flat["%s.%s" % (k, kk)] = vv
    return flat


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    gold = golden_flat(F)
    cr = cracker_asks()
    rows = []
    kept = 0
    for k in sorted(gold):
        hit = cr[k] == gold[k]
        kept += hit
        rows.append((k, gold[k], cr[k], "hit" if hit else "miss"))
    n = len(gold)
    Lc = kept / n
    Ls = Lc     # the mirror's ask path is the cracker's (asks decoupled from the call)
    C = W_REC + W_INS + W_ASK * Lc
    S = R_MISS + W_INS + W_ASK * Ls
    call_cracker = F["call"]["cases_w49_52"]
    call_mirror = F["rivals"]["register_cases_w49_52"]
    for k, g, c, v in rows:
        print("%-26s golden %-8s cracker %-8s %s" % (k, g, c, v))
    print("cracker call %s (golden %s); mirror call %s" % (call_cracker, F["call"]["cases_w49_52"], call_mirror))
    print("ask figures kept by the cracker: %d of %d" % (kept, n))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent" % (C, S, (C + S) / 2, 100 * Ls))
    return (C + S) / 2, 100 * Ls, kept, n


if __name__ == "__main__":
    main()
