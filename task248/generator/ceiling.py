"""The pair ceiling, measured on the cut pack: the cracker lands the call and runs the hygiene battery on every ask
(out-of-range clock rows dropped, near-duplicate test rows collapsed on their test number, UTC converted, the console
setup applied by its dates, the shadow week matched pair by pair, stamps read as written, the grade table as
published); the mirror stops at the delivery check and at each ask's most attractive handling. Scored on
38 + 7 + 55 x (ask weight kept) for a response on the call and 5 + 7 + 55 x (kept) off it."""
import sys, os, json
import analysis as A


def kept(golden, got, tol=0.5):
    keys = list(golden)
    return sum(1 for k in keys if k in got and abs(got[k] - golden[k]) < tol) / len(keys)


def run(target, verbose=True):
    res, pk = A.analyse(target)
    G1, G2, G3 = res["A1"], res["A2"], {k: round(v) for k, v in res["A3"].items()}
    r3 = lambda d: {("%s|%s" % k): round(v) for k, v in d.items()}
    crk = {
        "A1": A.ask_days(pk, redate=False),
        "A2": A.ask_tests(pk, redate=False, dedupe=True),
        "A3": r3(A.ask_gallons(pk, shadow="match", grade_basis="table", settle=False)),
    }
    mir = {
        "A1": A.ask_days(pk, redate=False, by_current=True),
        "A2": A.ask_tests(pk, redate=False, dedupe=False),
        "A3": r3(A.ask_gallons(pk, shadow="both", grade_basis="table", settle=False)),
    }
    full = {   # the full includer: finds the resets, reprints and shadow week, but keys tanks by the current
               # console numbering and reads the settlement stamps as sale times
        "A1": A.ask_days(pk, redate=True, by_current=True),
        "A2": A.ask_tests(pk),
        "A3": r3(A.ask_gallons(pk, shadow="match", grade_basis="price", settle=False)),
    }
    gold = {"A1": G1, "A2": G2, "A3": G3}
    out = {}
    for name, resp, on_call in (("cracker", crk, True), ("mirror", mir, False), ("full_includer", full, True)):
        per = {a: kept(gold[a], resp[a]) for a in gold}
        L = sum(per.values()) / len(per)
        score = (38 + 7 + 55 * L) if on_call else (5 + 7 + 55 * L)
        out[name] = {"per_ask_kept": per, "L": L, "score": score}
    out["pair_ceiling"] = (out["cracker"]["score"] + out["mirror"]["score"]) / 2
    out["mirror_leakage_pct"] = 100 * out["mirror"]["L"]
    out["cracker_misses_every_ask"] = all(v < 1.0 for v in out["cracker"]["per_ask_kept"].values())
    if verbose:
        print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "target"))
