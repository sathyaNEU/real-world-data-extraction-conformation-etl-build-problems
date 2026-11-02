"""The pair ceiling measured on the cut pack: the cracker (takes the decisive step and lands the call, runs the hygiene
battery, executes every filed rule; deduplicates the imaging records on woman, day, location and code, hosts the mobile
units by the location table and counts film readers by employee number) and the two mirrors (the strong analyst's
one-factor intervals: the examinations resampled with the panel fixed, filing Ondrix, and a paired test across the
readers, filing Lumidra), each priced against generator/figures.json.

    python3 task260/generator/ceiling.py [target]

Weights 35 / 7 / 58. The call side 35: the pick 10, each tool's gain 3, each tool's verdict 3, the reason for each tool
the protocol excludes 3.5 (kept only where the response excludes that tool too). Instructions 7. The ask layer 58 over
ten units: the four site counts, the three first-year costs, the film readers in post, and the chart's two parts (the
gains on their axis, kept by every route, and the intervals, kept when every bound prints as the golden's to three
decimals). A figure is kept when it prints in the golden's cell at the ask's rounding."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import common as K    # noqa: E402
import deliver as G   # noqa: E402
import load as L      # noqa: E402

TASK = os.path.dirname(HERE)
PICK, GAIN, VERDICT, REASON, INSTR, ASKS, UNITS = 10.0, 3.0, 3.0, 3.5, 7.0, 58.0, 10


def main(target=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    T = L.read(target)
    mats = {S["sid"]: G.study_matrix(T, S["sid"]) for S in K.STUDIES}
    tools = [S["tool"] for S in K.STUDIES]
    gold_res, gold_pick = G.evaluate(T, "or_jk", mats=mats)
    assert gold_pick == fig["call"]
    r3 = lambda x: round(float(x), 3)
    gold_iv = {k: (r3(gold_res[k]["lo"]), r3(gold_res[k]["hi"])) for k in tools}

    # the ask figures the cracker files (every route shares them: the asks are decoupled from the call)
    s = G.screening_studies(T, dedupe="same_day", hosts="directory")
    sites = G.per_site(s)
    seats = G.readers_in_post(T, "employee")[0]
    cost = {k: G.pounds(v) for k, v in G.costs(sum(sites.values()), G.episodes(s), seats).items()}
    kept_ab = sum(sites[c] == fig["studies_per_site"][c] for c in K.SITE_ORDER) + \
        sum(cost[k] == fig["cost"][k] for k in tools) + int(seats == fig["readers_in_post"])

    scores = {}
    for label, method in (("cracker (both random)", "or_jk"), ("mirror (panel fixed)", "fixed_dl"),
                          ("mirror (readers only)", "paired_t")):
        res, pick = G.evaluate(T, method, mats=mats)
        qual = {k: res[k]["lo"] > 0 for k in tools}
        call = PICK * (pick == gold_pick)
        call += GAIN * sum("%.3f" % res[k]["gain"] == fig["gain_3dp"][k] for k in tools)
        call += VERDICT * sum(qual[k] == fig["qualifies"][k] for k in tools)
        call += REASON * sum((not qual[k]) and (not fig["qualifies"][k]) for k in tools)
        chart = 1 + int(all((r3(res[k]["lo"]), r3(res[k]["hi"])) == gold_iv[k] for k in tools))
        units = kept_ab + chart
        sc = call + INSTR + ASKS * units / UNITS
        scores[label] = (sc, units)
        print("%-24s pick %-15s call side %4.1f  ask units kept %d of %d (%4.1f%% of ask weight)  score %5.1f"
              % (label, pick, call, units, UNITS, 100.0 * units / UNITS, sc))
    print("ask figures the cracker keeps: %d of 8 (sites %s, costs %s, film readers %d)" % (kept_ab, sites, cost, seats))
    pair = (scores["cracker (both random)"][0] + max(scores["mirror (panel fixed)"][0],
                                                      scores["mirror (readers only)"][0])) / 2
    leak = 100.0 * max(scores["mirror (panel fixed)"][1], scores["mirror (readers only)"][1]) / UNITS
    print("pair ceiling %.1f; mirror leakage %.1f per cent of ask weight" % (pair, leak))
    return pair, leak


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
