"""The cracker and mirror sheets on the cut pack, scored figure by figure against generator/figures.json, a hit an
exact match at the asked rounding. The cracker lands the call, runs the hygiene battery and the two stage 4 readers'
measured routes (deeds read through the change log by their own dates and units combined after the sale set aside;
permits joined to the 2026 roll by their numbers as written; hearings taken at each case's last decision after the
2025 roll's certification) and executes every filed rule; the mirror stops on the default path. The asks consume
nothing the call produces, so the two read them alike (the separation assertions S1 to S4 in checks.py).

    python3 task269/generator/cracker.py"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AK     # noqa: E402
import common as K    # noqa: E402
import pack as PK     # noqa: E402

TASK = os.path.dirname(HERE)


def score(target, a_mode="rawperm", b_mode="case"):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    pk = PK.Pack(target)
    a = AK.ask_a(pk, a_mode)
    b = AK.ask_b(pk, b_mode)
    FA = fig["ask_a"]
    rows = [("A condominium sales", a["n"], FA["sales"]),
            ("A condominium level", round(a["level"], 2), FA["level"]),
            ("A condominium COD", round(a["cod"], 1), FA["cod"]),
            ("A condominium PRD", round(a["prd"], 3), FA["prd"]),
            ("A condominium aggregate", round(a["agg"], 3), FA["agg"])]
    for ar, nm in K.AREAS:
        rows.append(("B parcels area %d" % ar, b[ar]["parcels"], fig["ask_b"][str(ar)]["parcels"]))
        rows.append(("B value area %d" % ar, b[ar]["off"], fig["ask_b"][str(ar)]["value_off"]))
    rows = [(n, got, want, got == want) for n, got, want in rows]
    hits = sum(r[3] for r in rows)
    lc = hits / len(rows)
    crack = 38 + 7 + 55 * lc
    mirror = 5 + 7 + 55 * lc
    return rows, hits, (crack + mirror) / 2, lc


if __name__ == "__main__":
    target = os.path.join(TASK, "target")
    rows, hits, pair, lc = score(target)
    for name, got, want, hit in rows:
        print("%-22s cracker %-12s golden %-12s %s" % (name, got, want, "HIT" if hit else "miss"))
    print("cracker keeps %d of %d ask figures; mirror leakage %.1f per cent; pair ceiling %.1f"
          % (hits, len(rows), 100 * lc, pair))
    for am, bm in (("noperm", "case"), ("noperm", "allcase"), ("raw", "rows"), ("every", "first"),
                   ("rawperm", "all")):
        _, h, p, _ = score(target, am, bm)
        print("variant (A %s, B %s): keeps %d of %d, pair %.1f" % (am, bm, h, len(rows), p))
