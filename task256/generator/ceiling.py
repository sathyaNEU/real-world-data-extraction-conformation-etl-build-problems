"""The ask sheet's cracker and mirror, run on the cut pack.

The cracker lands the call (its accommodation table and chart are the golden's), runs the hygiene battery and executes
every filed rule (standard ES-12; procedure FM-07: parts and labor on work orders billed to TVRTA, in the month the work
order closed; a bus-month for each month a bus is in the fleet on the first day, an option's for each month the bus
carries it then). It reads the work-order export as delivered, so the job's labour printed on every part line is summed
over the lines, and it counts bus-months on the fleet roster's buses with the options they carry today. The mirror stops
at the call's most attractive wrong rung (the conditional carry on the published survey, Configuration G) and takes the
same ask paths. Each keeps a figure when it lands on the golden's rounding (the dollar, one decimal).

    python3 task256/generator/ceiling.py [target_dir]
"""
import csv
import datetime as dt
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import records as R   # noqa: E402
import world as W     # noqa: E402

TASK = os.path.dirname(HERE)
FIRST, LAST = dt.date(2021, 1, 1), dt.date(2025, 12, 1)
COMP_OF = {c: v[1] for c, v in W.COMPONENTS.items() if v[1]}          # option component -> option letter
LETTER_OF = {code: letter for letter, code in R.OPT_CODE.items()}      # PDL -> P


def months():
    d = FIRST
    while d <= LAST:
        yield d
        d = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)


def cracker_asks(target):
    cost = {o: 0.0 for o in W.OPTION_ORDER}
    with open(os.path.join(target, R.WORK_ORDERS)) as fh:
        for r in csv.DictReader(fh):
            o = COMP_OF.get(r["component"])
            if o and r["bill_to"] == "TVRTA" and "2021-01-01" <= r["closed"] <= "2025-12-31":
                cost[o] += float(r["part_cost"]) + float(r["labor_cost"])       # labour taken on every line
    bm = {o: 0 for o in W.OPTION_ORDER}
    with open(os.path.join(target, R.FLEET)) as fh:
        for r in csv.DictReader(fh):
            acc = dt.date.fromisoformat(r["accepted"])
            opts = {LETTER_OF[c] for c in r["operator_area_options"].split() if c in LETTER_OF}
            n = sum(1 for m in months() if acc <= m)
            for o in opts:
                bm[o] += n
    maint = {o: {"cost": round(cost[o]), "bus_years": round(bm[o] / 12.0, 1),
                 "rate": round(cost[o] / (bm[o] / 12.0)) if bm[o] else 0} for o in W.OPTION_ORDER}
    twelve = {c: p + 12 * sum(cost[o] / (bm[o] / 12.0) for o in opts if bm[o]) for c, opts, p in W.CONFIGS}
    return maint, {c: round(v) for c, v in twelve.items()}


def run(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    gm, gt = fig["maint"], fig["twelve"]
    cm, ct = cracker_asks(target)
    keep_a = sum((cm[o]["cost"] == gm[o]["cost_dollars"]) + (cm[o]["bus_years"] == gm[o]["bus_years"]) +
                 (cm[o]["rate"] == gm[o]["rate"]) for o in W.OPTION_ORDER)
    keep_b = sum(ct[c] == gt[c] for c in gt)
    gold_c = fig["acc_pct"]
    mirror_c = fig["rung_pct"]["R4"]
    keep_c_mirror = sum(abs(mirror_c[c] - gold_c[c]) < 0.05 for c in gold_c)
    # the accommodation table and the chart (C) are the call's own construction and sit in the main block with the
    # call: the cracker, on the call, keeps them; the mirror, on G, keeps none of the shares
    total = 3 * len(W.OPTION_ORDER) + len(gt)
    lc = (keep_a + keep_b) / total
    ls = (keep_a + keep_b) / total
    cr, mi = 38 + 7 + 55 * lc, 5 + 7 + 55 * ls
    return dict(cracker_kept={"A": keep_a, "B": keep_b}, mirror_kept={"A": keep_a, "B": keep_b},
                mirror_c_shares_kept=keep_c_mirror, ask_criteria=total, cracker=round(cr, 1), mirror=round(mi, 1),
                pair_ceiling=round((cr + mi) / 2, 1), mirror_leakage_pct=round(100 * ls, 1),
                cracker_ask_a=cm, cracker_twelve=ct)


def main():
    if len(sys.argv) > 1:
        print(json.dumps(run(sys.argv[1]), indent=1))
        return
    tmp = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as z:
            z.extractall(tmp)
        print(json.dumps(run(tmp), indent=1))
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
