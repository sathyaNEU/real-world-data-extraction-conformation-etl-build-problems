"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task138/generator/ceiling.py

Rows: the cracker lands the call and runs the battery (the 2016 shots and the ORF2 gauge datum put on NAVD 88 with
the benchmark pairs; the ORF2 export's stamps step back where the new logger's records start, so it lines the two
loggers up and moves the old one's records 6 h), joins the two surveys on station number and reads OP-04's 21.0 ft
on the Coyle Bridge gauge as printed; the mirror stops on the published-record rung of the call and handles the asks the same way,
since nothing in them comes from the call; the re-stationer also re-stations the 2016 survey from the structures
both surveys shot; the full includer also puts the warning elevation on the gauge datum in force at each flood (stress
rows, not the gate)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402


def figures(AF, restation, coy_mode, clock_fix=True, hb_convert=True, datum=True):
    st = A.settlement(AF, offset=None if restation else 0, shift=None if datum else 0.0)
    lt = A.lead_times(AF, coy_mode=coy_mode, clock_fix=clock_fix, hb_convert=hb_convert)
    return ({k: round(v, 2) for k, v in st.items()}, [int(round(h)) for _, h in lt])


def kept(resp, gold):
    a = sum(resp[0].get(k) == v for k, v in gold[0].items())
    b = sum(x == y for x, y in zip(resp[1], gold[1])) if len(resp[1]) == len(gold[1]) else 0
    return a + b


def main(target=TARGET):
    AF = A.AskFiles(target)
    gold = figures(AF, True, "per_datum")
    n = len(gold[0]) + len(gold[1])
    crack = kept(figures(AF, False, "old_stage", clock_fix=True), gold)
    full = kept(figures(AF, True, "per_datum"), gold)
    half = kept(figures(AF, True, "old_stage", clock_fix=True), gold)
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery: datums, the ORF2 clock; surveys joined by station; 21.0 ft as printed): "
          "keeps %d of %d ask criteria, response %.1f" % (crack, n, c))
    print("mirror (published-record rung, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("re-stationer (also re-stations the 2016 survey; 21.0 ft as printed): keeps %d of %d, "
          "response %.1f"
          % (half, n, 38 + 7 + 55 * half / n))
    print("full includer (both reconstructions, stress row): keeps %d of %d, response %.1f"
          % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
