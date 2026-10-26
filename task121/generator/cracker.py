"""The cracker's path on the cut pack (supplemental-stumping 1.1), the path both round 1 readers took: a response that
lands the call, runs the hygiene battery (key uniqueness, exact and near-exact duplicate rows, unmatched joins,
fan-out) and executes every filed rule it points at. On Ask A it takes each CAD incident's processing time from the
answer to the earliest assignment in the unit history and the 90th percentile at QA 3.2's rank; on Ask B it takes each
primary review with compressions coached from the recording's start plus its seconds, less the CAD's answer, and the
month's median; on Ask C it takes the 911 trunk groups' answered calls by local month, every record a call. Every ask
figure is scored against figures.json: a hit is the figure at its rounding. The mirror (the response on R0, the
release) runs the asks the same way, since they consume nothing the call's construction produces. Prints the sheet and
the pair ceiling."""
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
    a = AK.processing(target, calls="incidents")
    b = AK.tcpr(target, keyed=None)
    c = AK.answering(target, passed="kept")
    rows = []
    for ym in K.MONTHS:
        k = "%d-%02d" % ym
        rows.append(("A", "P90 %s" % k, a[ym] == fig["asks"]["A"]["p90_processing_s"][k]))
        rows.append(("B", "median %s" % k, b[ym] == fig["asks"]["B"]["median_first_compression_s"][k]))
        rows.append(("C", "share %s" % k, abs(c[ym] - fig["asks"]["C"]["answered_within_15s_pct"][k]) < 0.05))
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
