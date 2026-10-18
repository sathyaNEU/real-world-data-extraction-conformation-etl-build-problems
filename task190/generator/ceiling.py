"""Pair ceiling and mirror leakage for task190, on supplemental-stumping Part 0's weights.

Two responses are scored, from DIFFERENT readings, one row each:
  cracker  landed the call, ran the hygiene battery (key uniqueness, exact duplicates, unmatched
           joins, fan-out, count ties) and executed every filed rule the pack points at: the
           documented unit columns, the dated code revision, the re-sent operations batch, the
           permit supersessions a failing join exposes, the visit grain the collection
           documentation states, and the memo's municipal counting convention. Its permit join
           takes the crosswalk row marked current, which is what the battery's fan-out repair
           leaves, and it sums a municipality's twelve return months.
  mirror   stopped at the most attractive wrong rung on the call (rung 1, a bar built from the
           published national coefficient of variation) and takes each ask's lazy stop: the log's
           rows as contacts, every return as a return, the crosswalk's currently valid codes,
           every confirmed leg once.

No filed sentence resolves any of the three primaries, so neither response reaches one: each is an
inconsistency across grains or dates that no column description asks for and no sweep performs.
The readings differ on every ask (the re-sent batch on A1, the code revision on A2, the units and
the counting convention on A3), so the two rows are two measurements and not one counted twice.

Every ask figure is listed with the device and hazards that touch it, so a figure is scored a hit
only when no device touching it is resolved by that response; where ceiling_deltas.json exists the
measurement on the cut pack is read instead of that model. Part 0: C = 38 + 7 + 55*Lc,
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
    FIGURES.append(("A1", "contacts made %s" % region,
                    ["A1_permit_reissue"] + (["H3_resent_batch"] if region == "Norte" else [])))
    FIGURES.append(("A1", "contacts per usable return %s" % region,
                    ["A1_permit_reissue"] + (["H3_resent_batch"] if region == "Norte" else [])))
for stream in ("metal", "mixed_ci", "paper", "wood", "cd_rubble", "glass", "plastic", "textile"):
    FIGURES.append(("A2", "2025 confirmed recovery tonnage %s" % stream,
                    ["A2_renotification"] + (["H2_code_revision"] if stream in
                                             ("metal", "mixed_ci", "wood", "plastic") else [])))
for region in ("Norte", "Centro", "Lisboa", "Alentejo", "Algarve"):
    FIGURES.append(("A3", "municipal gap %s" % region,
                    ["A3_annual_in_december", "H5_authority_returns"] +
                    (["H1_units"] if region == "Centro" else [])))
    FIGURES.append(("A3", "gap as a share of collections %s" % region,
                    ["A3_annual_in_december", "H5_authority_returns"] +
                    (["H1_units"] if region == "Centro" else [])))

# What each response resolves. The cracker runs the battery and executes every filed rule, so it
# resolves every documented handling and everything the five sweeps find: the unit columns the
# files' own columns give (H1), the code revision the crosswalk dates (H2), the re-sent batch (H3),
# the permit supersessions the crosswalk lists where a join fails (H4), the municipal counting
# convention the memo files (H5) and the visit grain the collection documentation states. It
# resolves no primary: A1's reissued permit numbers are a valid current crosswalk row, A2's
# re-notified consignments are distinct consignment numbers, and A3's December row is a valid
# return month.
RESOLVES = {
    "cracker": {"H1_units", "H2_code_revision", "H3_resent_batch", "H4_permit_supersession",
                "H5_authority_returns", "A1_visit_grain"},
    "mirror": set(),
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


def total(lands, kept):
    return (W_REC if lands else R_WRONG_CALL) + W_IF + W_ASK * (kept / float(len(FIGURES)))


def main():
    rows, out = [], {}
    for name, lands in (("cracker", True), ("mirror", False)):
        hits = score(name)
        L = len(hits) / float(len(FIGURES))
        per_ask = {}
        for ask in ("A1", "A2", "A3"):
            n = sum(1 for f in FIGURES if f[0] == ask)
            k = sum(1 for f in hits if f[0] == ask)
            per_ask[ask] = "%d of %d" % (k, n)
        rows.append((name, lands, len(hits), L, total(lands, len(hits)), per_ask))
        out[name] = {"lands_call": lands, "ask_figures_kept": len(hits), "ask_weight_kept": round(L, 4),
                     "recommendation_weight": W_REC if lands else R_WRONG_CALL,
                     "total": round(total(lands, len(hits)), 2), "per_ask": per_ask}
    pair = sum(r[4] for r in rows) / 2.0
    leak = next(r[3] for r in rows if r[0] == "mirror") * 100.0
    src = "measured on the cut pack (ceiling_deltas.json)" if os.path.exists(DELTAS) else "designed stops, no pack cut yet"
    print("task190 pair ceiling, weights %g/%g/%g, %d ask figures, %s"
          % (W_REC, W_IF, W_ASK, len(FIGURES), src))
    for name, lands, k, L, tot, per_ask in rows:
        print("  %-8s call=%-5s asks %2d of %d (%.3f of ask weight)  rec=%.0f  total=%.2f   %s"
              % (name, "yes" if lands else "no", k, len(FIGURES), L,
                 W_REC if lands else R_WRONG_CALL, tot,
                 " ".join("%s %s" % (a, v) for a, v in per_ask.items())))
    print("  Pair ceiling:   %.1f  (gate %.0f) %s" % (pair, PAIR_GATE, "PASS" if pair <= PAIR_GATE else "FAIL"))
    print("  Mirror leakage: %.1f per cent of ask weight (gate under %.0f) %s"
          % (leak, LEAK_GATE, "PASS" if leak < LEAK_GATE else "FAIL"))
    # The premise the gate's figure rests on is that one of the top two responses lands the call.
    # The stage-4 cold reader and the judge's Gate F are what check it, so the alternative premise
    # is priced here rather than assumed away.
    kept = out["cracker"]["ask_figures_kept"]
    both = (total(True, kept) + total(True, kept)) / 2.0
    widest = max(sum(1 for f in FIGURES if f[0] == a) for a in ("A1", "A2", "A3"))
    both_one_ask = (total(True, kept) + total(True, kept + widest)) / 2.0
    print("  Sensitivity, one response on the call (the premise above): %.1f" % pair)
    print("  Sensitivity, both top responses on the call, each keeping its measured asks: %.1f" % both)
    print("  Sensitivity, both on the call and one resolving a whole ask (%d figures): %.1f"
          % (widest, both_one_ask))
    print("  No shipped sentence resolves a primary, so the third premise needs an inconsistency")
    print("  found rather than a section read; that is the difference this repair bought.")
    print("  The three asks consume nothing the call's construction produces (A1 the response log")
    print("  and the permit crosswalk, A2 the 2025 legs, A3 the municipal files), so a response's")
    print("  ask score does not depend on landing the call; checks.py asserts zero device and")
    print("  hazard rows inside the call's declared population.")
    out["pair_ceiling"] = round(pair, 2)
    out["mirror_leakage_pct"] = round(leak, 2)
    out["sensitivity"] = {"one_response_on_the_call": round(pair, 2),
                          "both_responses_on_the_call": round(both, 2),
                          "both_on_the_call_one_whole_ask_found": round(both_one_ask, 2)}
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "ceiling.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    return 0 if (pair <= PAIR_GATE and leak < LEAK_GATE) else 1


if __name__ == "__main__":
    sys.exit(main())
