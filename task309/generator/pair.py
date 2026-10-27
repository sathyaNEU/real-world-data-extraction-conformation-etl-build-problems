"""The cracker and the mirror run on the cut pack, scored against the golden ask figures (supplemental-stumping
Part 0 weights: call and critical components 38, instruction-following 7, asks 55 spread over the ask figures).

The cracker lands the call, runs the hygiene battery and executes every filed rule: it normalises addresses and joins
certificates to homes on parcel and address as written, adds every carried new-system line to the legacy paid to date,
and raises roof years from the RE-ROOF permits at the address as written. The mirror stops at the most attractive
wrong rung of the call (one cut for all storms, Marlin Shoals) and takes the asks the plain way: certificates joined on
the policy they were issued under, the legacy valuations alone, the roof year on record.

    python3 task309/generator/pair.py <target dir>
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P  # noqa: E402
import solve as S  # noqa: E402

CRACKER = {"a": "parcel_address", "b": "legacy_plus_new", "c": "address_only"}
MIRROR = {"a": "by_policy", "b": "legacy_only", "c": "record"}
W_CALL, W_IF, W_ASK, R_MISS = 38.0, 7.0, 55.0, 5.0


def figures(target, routes):
    names = [P.COUNTY_NAME[c] for c in P.CANDIDATES]
    out = {}
    a = S.ask_a(target, routes["a"])
    for n in names:
        out["A homes %s" % n] = int(a.loc[n, "homes"])
        out["A cover %s" % n] = int(round(a.loc[n, "cov"] / 1e3))
    b = S.ask_b(target, routes["b"])
    for sid, (t, af) in b.items():
        out["B total %s" % sid] = int(round(t / 1e3))
        out["B after %s" % sid] = int(round(af / 1e3))
    c = S.ask_c(target, routes["c"])
    for n in names:
        out["C homes %s" % n] = int(c.loc[n, "homes"])
        out["C cover %s" % n] = int(round(c.loc[n, "cov"] / 1e3))
    return out


def main(target):
    gold = figures(target, {"a": "golden", "b": "golden", "c": "golden"})
    cr = figures(target, CRACKER)
    mi = figures(target, MIRROR)
    rows = []
    for k in gold:
        rows.append((k, gold[k], cr[k], mi[k], "hit" if cr[k] == gold[k] else "miss", "hit" if mi[k] == gold[k] else "miss"))
    n = len(rows)
    kc = sum(r[4] == "hit" for r in rows)
    km = sum(r[5] == "hit" for r in rows)
    sc = W_CALL + W_IF + W_ASK * kc / n
    sm = R_MISS + W_IF + W_ASK * km / n
    for r in rows:
        print("%-24s golden %-10s cracker %-10s %-4s mirror %-10s %s" % (r[0], r[1], r[2], r[4], r[3], r[5]))
    print("cracker keeps %d of %d ask figures, scores %.1f; mirror keeps %d, scores %.1f" % (kc, n, sc, km, sm))
    print("Pair ceiling: %.1f   Mirror leakage: %.1f per cent of ask weight" % ((sc + sm) / 2, 100.0 * km / n))
    return {"pair": (sc + sm) / 2, "mirror": 100.0 * km / n, "cracker_keeps": kc, "n": n}


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1])))
