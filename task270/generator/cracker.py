"""The cracker and the mirror, run on the cut pack (supplemental-stumping Part 1.1): the cracker lands the call and
takes each ask the careful way, executing every filed rule it points at; the mirror stops at the most attractive
wrong rung of the call and takes the asks the same way. Each ask figure is scored as a hit within half a unit of its
stated rounding; the pair ceiling is computed on the rubric weights 38, 7 and 55.

    python3 task270/generator/cracker.py [target]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import common as K     # noqa: E402
import pack as PK      # noqa: E402

TASK = os.path.dirname(HERE)
COMP = K.COMPONENTS
ADMS = [a["name"] for a in K.ADMIN]

# the careful paths: Ask A pairs each year-end accrual with its invoice (same purchase order) and takes every accrual
# out with the 1 July 2024 reversal, the rule the 2024 pairs show; Ask B joins records on name and date of birth or on
# email, takes the window in Eastern time and the lateral applicants out by the screening question
PATHS = {
    "cost": "accruals_out",
    "keys": ("name_dob", "email"),
}
ALT = {
    "cost": "every_line",
    "keys": ("name_dob", "name_phone"),
}


def asks(target, paths):
    cost = A.cost(target, paths["cost"])[0]
    appl = A.applicants(target, keys=paths["keys"])
    comp = A.completion(target, appl)
    out = {}
    for c in COMP:
        out["A %s" % K.LABEL[c]] = (round(cost[c], 2), 0.005)
    for a in ADMS:
        out["B applicants %s" % a] = (appl[a], 0.5)
    for c in COMP:
        out["B completion %s" % K.LABEL[c]] = (round(comp[c], 2), 0.005)
    return out


def golden(fig):
    out = {}
    for c in COMP:
        out["A %s" % K.LABEL[c]] = fig["ask_a"][K.LABEL[c]]
    for a in ADMS:
        out["B applicants %s" % a] = fig["ask_b"]["applicants"][a]
    for c in COMP:
        out["B completion %s" % K.LABEL[c]] = fig["ask_b"]["completion"][K.LABEL[c]]
    return out


def score(target, fig, paths):
    got = asks(target, paths)
    gold = golden(fig)
    rows = []
    for k, g in gold.items():
        v, half = got[k]
        rows.append((k, g, v, abs(v - g) < half - 1e-9))
    return rows


def run(target=None, quiet=False):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    smp = PK.sample(target)
    ro = A.routes(smp)
    cr_call = A.call(ro["golden"])["keep"] == A.call(ro["golden"])["keep"]
    mi_call = A.call(ro["appointees"])["keep"] == A.call(ro["golden"])["keep"]
    res = {}
    for name, paths in (("cracker", PATHS), ("cracker, other path", ALT)):
        rows = score(target, fig, paths)
        res[name] = rows
        if not quiet:
            print("%s: keeps %d of %d ask figures" % (name, sum(r[3] for r in rows), len(rows)))
            for k, g, v, hit in rows:
                print("   %-40s golden %-10s %-10s %s" % (k, g, v, "HIT" if hit else "miss"))
    n = len(res["cracker"])
    kept_c = max(sum(r[3] for r in rows) for rows in res.values())
    kept_m = kept_c                       # the mirror takes the asks the same way: they read nothing the call produces
    cr = 38 + 7 + 55.0 * kept_c / n if cr_call else 5 + 7 + 55.0 * kept_c / n
    mi = (38 + 7 if mi_call else 5 + 7) + 55.0 * kept_m / n
    pair = (cr + mi) / 2
    if not quiet:
        print("call: cracker %s, mirror (appointees' correlations) %s" % ("landed" if cr_call else "missed",
                                                                          "landed" if mi_call else "missed"))
        print("asks read nothing the call's construction produces (the separation assertions in checks.py), so the "
              "mirror's ask row equals the cracker's")
        print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight"
              % (cr, mi, pair, 100.0 * kept_m / n))
    return dict(rows=res, pair=pair, cracker=cr, mirror=mi, kept=kept_c, n=n, leakage=100.0 * kept_m / n)


if __name__ == "__main__":
    r = run(sys.argv[1] if len(sys.argv) > 1 else None)
    sys.exit(0 if r["kept"] == 0 else 1)
