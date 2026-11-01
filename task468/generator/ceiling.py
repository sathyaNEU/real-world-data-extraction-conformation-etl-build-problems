"""The pair ceiling on the cut pack (supplemental-stumping Part 0 and Part 5): one row per response, each scored from
its own reading of every ask. The cracker lands the call, runs the hygiene battery (applies the update, drops a
certificate repeated under one application, counts one price on several same-day entries once, drops a claim that
repeats another's postcode, start and homes) and reads every helper document; the mirror stops at the default path
and takes every ask as the files print it. Scores on 38 (call and components), 7 (instruction following) and 55
(asks), with an off-call response banking 5 of the 38."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import askcheck as AC  # noqa: E402
import solve as S      # noqa: E402

WARDS = ["Abbots Hollow", "Brindley Moor", "Calder Bank", "Dunmore", "Eastholme", "Fennick", "Gorsey Hill",
         "Hollin Edge", "Kestrel Rise", "Moss Brow", "Pellbury", "Wexley"]


def kept(route, golden):
    return sum(1 for w in WARDS if route.get(w, 0) == golden.get(w, 0))


def main(target=S.TARGET):
    G = S.golden(target)
    A, B, C = AC.variants(target, G)
    n = 3 * len(WARDS)
    rows = {
        "cracker": dict(call=True, A=kept(A["blank lost as 0"], A["golden"]), B=kept(B["same-day pairs one"], B["golden"]),
                        C=kept(C["exact repeats only"], C["golden"])),
        "mirror": dict(call=False, A=kept(A["both"], A["golden"]), B=kept(B["every title"], B["golden"]),
                       C=kept(C["every claim"], C["golden"])),
        "full includer": dict(call=True, A=kept(A["golden"], A["golden"]), B=kept(B["golden"], B["golden"]),
                              C=kept(C["golden"], C["golden"])),
    }
    out = {}
    for k, r in rows.items():
        share = (r["A"] + r["B"] + r["C"]) / float(n)
        r["ask_share"] = round(share, 4)
        r["score"] = round((38 if r["call"] else 5) + 7 + 55 * share, 2)
        out[k] = r
    pair = round((out["cracker"]["score"] + out["mirror"]["score"]) / 2, 2)
    res = {"rows": out, "pair_ceiling": pair, "mirror_leakage_pct": round(100 * out["mirror"]["ask_share"], 1),
           "ask_figures": n}
    print(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else S.TARGET)
