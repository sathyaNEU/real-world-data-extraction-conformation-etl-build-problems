"""Pair ceiling and mirror leakage for task190, on supplemental-stumping Part 0's weights.

Two responses are scored, from DIFFERENT readings, one row each:
  cracker  landed the call, ran the hygiene battery (key uniqueness, exact duplicates, unmatched
           joins, fan-out, count ties) and executed every filed rule the pack points at.
  mirror   stopped at the most attractive wrong rung on the call (rung 1, a bar built from the
           published national coefficient of variation), and takes each ask's lazy stop.

Every ask figure is listed with the device and hazards that touch it, so a figure is scored a hit
only when no device touching it is resolved by that response. Part 0: C = 38 + 7 + 55*Lc,
S = r + 7 + 55*Ls with r = 5, pair = (C + S) / 2, gate 40. Mirror leakage is Ls as a percentage.
"""
import json
import os
import sys

R_WRONG_CALL = 5.0          # recommendation weight a wrong call still keeps (generated rubric)
W_REC, W_IF, W_ASK = 38.0, 7.0, 55.0
PAIR_GATE, LEAK_GATE = 40.0, 35.0

# ask figures: (ask, figure, devices touching it). A figure is a hit only if the response
# resolves every device in its list.
FIGURES = []
for region in ("Norte", "Centro", "Lisboa", "Alentejo", "Algarve"):
    FIGURES.append(("A1", "field days consumed %s" % region, ["A1_visit_grain"]))
    FIGURES.append(("A1", "usable returns per field day %s" % region,
                    ["A1_visit_grain"] + (["H1_units"] if region == "Alentejo" else [])))
for stream in ("metal", "mixed_ci", "paper", "wood", "cd_rubble", "glass", "plastic", "textile"):
    FIGURES.append(("A2", "2025 confirmed recovery tonnage %s" % stream,
                    ["A2_renotification"] + (["H2_code_revision"] if stream in ("wood", "plastic") else [])))
for region in ("Norte", "Centro", "Lisboa", "Alentejo", "Algarve"):
    FIGURES.append(("A3", "municipal gap %s" % region, ["A3_authority_grain"]))
    FIGURES.append(("A3", "gap as a share of collections %s" % region,
                    ["A3_authority_grain"] + (["H1_units"] if region in ("Centro",) else [])))

# What each response resolves. The cracker runs the battery and executes every filed rule, so it
# resolves every documented handling and everything the five sweeps find: the unit column the
# dictionary describes (H1), the code revision the crosswalk dates (H2), the re-sent batch (H3) and
# the permit supersessions the crosswalk lists where a join fails (H4). It resolves no primary,
# because each primary is an inconsistency across grains that no column description asks for and no
# sweep performs: A1's response log is at case grain against an enterprise-grain frame and no count
# in the pack exceeds any published total, A2's re-notified consignments are distinct consignment
# numbers, and A3's authority return is a valid distinct return.
RESOLVES = {
    "cracker": {"H1_units", "H2_code_revision", "H3_resent_batch", "H4_permit_supersession"},
    "mirror": {"H2_code_revision"},
}

# When the generator has measured each figure under each response on the cut pack, read that
# instead of the model above: a figure is a hit only when the response's own reading is within half
# the stated rounding unit of the golden.
DELTAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ceiling_deltas.json")


def score(name):
    if os.path.exists(DELTAS):
        with open(DELTAS, encoding="utf-8") as fh:
            d = json.load(fh)
        if name in d:
            return [f for f in FIGURES if d[name].get(f[1], 1.0) == 0.0]
    resolved = RESOLVES[name]
    return [f for f in FIGURES if all(dv in resolved for dv in f[2])]


def main():
    rows, out = [], {}
    for name, lands in (("cracker", True), ("mirror", False)):
        hits = score(name)
        L = len(hits) / len(FIGURES)
        rec = W_REC if lands else R_WRONG_CALL
        total = rec + W_IF + W_ASK * L
        per_ask = {}
        for ask in ("A1", "A2", "A3"):
            n = sum(1 for f in FIGURES if f[0] == ask)
            k = sum(1 for f in hits if f[0] == ask)
            per_ask[ask] = "%d of %d" % (k, n)
        rows.append((name, lands, len(hits), L, rec, total, per_ask))
        out[name] = {"lands_call": lands, "ask_figures_kept": len(hits), "ask_weight_kept": round(L, 4),
                     "recommendation_weight": rec, "total": round(total, 2), "per_ask": per_ask}
    pair = sum(r[5] for r in rows) / 2.0
    leak = next(r[3] for r in rows if r[0] == "mirror") * 100.0
    src = "measured on the cut pack (ceiling_deltas.json)" if os.path.exists(DELTAS) else "designed stops, no pack cut yet"
    print("task190 pair ceiling, weights %g/%g/%g, %d ask figures, %s"
          % (W_REC, W_IF, W_ASK, len(FIGURES), src))
    for name, lands, k, L, rec, total, per_ask in rows:
        print("  %-8s call=%-5s asks %2d of %d (%.3f of ask weight)  rec=%.0f  total=%.2f   %s"
              % (name, "yes" if lands else "no", k, len(FIGURES), L, rec, total,
                 " ".join("%s %s" % (a, v) for a, v in per_ask.items())))
    print("  Pair ceiling:   %.1f  (gate %.0f) %s" % (pair, PAIR_GATE, "PASS" if pair <= PAIR_GATE else "FAIL"))
    print("  Mirror leakage: %.1f per cent of ask weight (gate under %.0f) %s"
          % (leak, LEAK_GATE, "PASS" if leak < LEAK_GATE else "FAIL"))
    print("  The three asks consume nothing the call's construction produces (A1 the response log, A2 the")
    print("  2025 legs, A3 the municipal returns), so the two rows differ only where a response resolves a")
    print("  device; checks.py asserts zero device and hazard rows inside the call's declared population.")
    out["pair_ceiling"] = round(pair, 2)
    out["mirror_leakage_pct"] = round(leak, 2)
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "ceiling.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    return 0 if (pair <= PAIR_GATE and leak < LEAK_GATE) else 1


if __name__ == "__main__":
    sys.exit(main())
