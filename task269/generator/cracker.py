"""The cracker's path on the cut pack (supplemental-stumping 1.1): a response that lands the call, runs the hygiene
battery (key uniqueness, exact and near-exact duplicate rows, unmatched joins, fan-out) and executes every filed rule
it points at, as the stage 4 readers did. On Ask A it links every culture to its admission (a retired record number by
date of birth and sex, the battery's unmatched join), rebuilds the ward at collection from the admitting ward and the
transfers, keeps each patient's episodes across admissions and applies the onset rule from each admission's own start;
on Ask B it sums the bottles the store issued to each ward less returns, reads each carton as 24 personal bottles, and
counts every dispenser refill record (no two rows are alike, so the battery drops nothing); on Ask C it sums the soap
bottles to each ward and the quantity on every cartridge record at 0.8 litres. Every ask figure is scored against figures.json: a hit
is within half a unit of the stated rounding. The mirror (the response on R1, 9B alone) runs the asks the same way,
since they consume nothing the call's construction produces; the separation rows in checks.py prove it. Prints the
sheet and the pair ceiling."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AK      # noqa: E402
import common as K     # noqa: E402


def score(task):
    target = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    a = AK.hobsi(target, stay_gap=None)
    b = AK.hand_rub(target, drop_copies=False)
    s = AK.hand_soap(target, drop_copies=False, sum_quantity=True)
    ga, gb, gs = fig["asks"]["A"], fig["asks"]["B"], fig["asks"]["C"]
    rows = []
    for c in K.WARD:
        rows.append(("A", "HOBSI %s" % c, a["n"][c] == ga["hobsi"][c]))
        rows.append(("A", "rate %s" % c, abs(a["rate"][c] - ga["rate_per_10000_obd"][c]) < 0.05))
        rows.append(("B", "litres %s" % c, abs(b["litres"][c] - gb["litres"][c]) < 0.05))
        rows.append(("B", "rate %s" % c, abs(b["rate"][c] - gb["litres_per_1000_obd"][c]) < 0.05))
        rows.append(("C", "litres %s" % c, abs(s["litres"][c] - gs["litres"][c]) < 0.05))
        rows.append(("C", "rate %s" % c, abs(s["rate"][c] - gs["litres_per_1000_obd"][c]) < 0.05))
    return rows


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
    rows = score(task)
    for ask in ("A", "B", "C"):
        r = [x for x in rows if x[0] == ask]
        print("Ask %s: cracker keeps %d of %d figures%s" % (ask, sum(x[2] for x in r), len(r),
                                                              "" if not any(x[2] for x in r) else
                                                              " (" + ", ".join(x[1] for x in r if x[2]) + ")"))
    kept = sum(x[2] for x in rows)
    n = len(rows)
    lc = kept / n
    pair = ((38 + 7 + 55 * lc) + (5 + 7 + 55 * lc)) / 2
    print("cracker %d of %d ask figures; mirror %d of %d (decoupled asks); pair ceiling %.1f" % (kept, n, kept, n, pair))
    sys.exit(0 if kept == 0 else 1)
