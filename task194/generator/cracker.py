"""The cracker and the mirror, run on the cut pack.

The cracker is the response that lands the call and then takes every ask the way the pack's own hygiene
battery leads it: it joins the unit register for a hospital, counts the extract's rows for the units
outside the indicator, and groups the complication detail on the code as recorded. The mirror is the best
response that does not land the call, which is rung 2's: the standing taken correctly and the programme
priced as the average drop in the standardised ratio.

Prints the ask-by-ask verdicts, the pair ceiling and the mirror's leakage, and `build.py` asserts the two
figures against the design note.
"""
import collections
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import golden as G

REC, ASKS, INSTR = 38.0, 55.0, 7.0          # the rubric's three blocks
ASK_CRITERIA = 60                            # gradable ask figures


def run(target):
    g = G.compute(target)
    b = g["bundle"]
    reg = {c: u["hospital_code"] for c, u in b["units"].items()}
    out = []

    # A2: the cracker joins the register, which is the master at the export date
    wrong = collections.defaultdict(int)
    for eid, (unit, sep, fy) in b["inscope_episode"].items():
        if dt.date(2026, 1, 1) <= sep <= dt.date(2026, 12, 31):
            wrong[reg[unit]] += 1
    for h in g["hospitals"]:
        out.append(("A2 %s episodes" % h["hospital"], wrong[h["hospital"]] == h["episodes"]))

    # A3: the cracker counts the extract's rows for the units outside the indicator
    acute = {c for c, u in b["units"].items() if u["service_type"] == "Acute inpatient"}
    raw = collections.defaultdict(int)
    with open(os.path.join(target, "episode_outcomes_extract.csv"), encoding="utf-8") as fh:
        import csv
        for r in csv.DictReader(fh):
            if r["unit_code"] in acute:
                continue
            raw[G.fiscal(dt.date.fromisoformat(r["separation_date"]))[1]] += 1
    for o in g["outside"]:
        out.append(("A3 %s separations" % o["quarter"], raw[o["quarter"]] == o["separations"]))

    # A4: the cracker groups the detail extract on the code as recorded, against the current revision
    cat26 = {r["complication_code"]: r["group_id"] for r in G._read(target, "hac_category_list.csv")
             if r["list_revision"] == "2026"}
    seen = collections.defaultdict(lambda: collections.defaultdict(set))
    for r in G._read(target, "hac_detail_extract.csv"):
        eid = r["episode_id"]
        if eid not in b["inscope_episode"]:
            continue
        unit, sep, fy = b["inscope_episode"][eid]
        if fy in ("2025-26", "2026-27") and r["complication_code"] in cat26:
            seen[fy][cat26[r["complication_code"]]].add(eid)
    for x in g["groups"]:
        out.append(("A4 %s 2025-26" % x["group"], len(seen["2025-26"][x["group"]]) == x["fy2025"]))
        out.append(("A4 %s 2026-27" % x["group"], len(seen["2026-27"][x["group"]]) == x["fy2026"]))

    hits = sum(1 for _, ok in out if ok)
    construction = 12                         # the twelve avoided counts, which the cracker lands
    landed = REC + INSTR + ASKS * (construction + hits) / ASK_CRITERIA

    # the mirror: rung 2's response, which lands none of the twelve and carries the same devices
    models = g["models"]
    drop = models["a constant drop in the standardised ratio"]["parameter"]
    mirror_vec = {d["unit"]: round(drop * d["expected_plan"]) for d in g["units"]}
    mirror_hits = sum(1 for d in g["units"] if mirror_vec[d["unit"]] == round(d["avoided"]))
    mirror = 5.0 + INSTR + ASKS * (mirror_hits + hits) / ASK_CRITERIA
    leakage = 100.0 * (mirror_hits + hits) / ASK_CRITERIA
    return out, landed, mirror, (landed + mirror) / 2.0, leakage


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    rows, landed, mirror, ceiling, leakage = run(tgt)
    for label, ok in rows:
        print("  %-28s %s" % (label, "hit" if ok else "miss"))
    print("landed call %.1f, best response off the call %.1f, pair ceiling %.1f" % (landed, mirror, ceiling))
    print("mirror leakage %.1f per cent of ask weight" % leakage)
