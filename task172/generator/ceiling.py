"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task172/generator/ceiling.py

Rows: the cracker lands the call and executes every filed rule (the pharmacovigilance database as the SAP's record
of serious events, each case's latest report, nullified cases out, onset from randomisation to the cut; the SAP's
baseline and on-treatment rule; each laboratory's own upper limit; any dose of any study treatment), runs the
battery (UTC randomisation times converted, the cut applied, local units kept with their own limits, replaced and
withheld kits left out), and reads each file the way it presents itself: a case is linked to its patient by the
screening number the randomisation export carries, a central sample is dated by the transfer's COLLECTION_DATE, and
exposure is read from the EDC's administration pages. The mirror stops at the stratified Cox ratio on the call
(band A) and handles the asks the same way, since they carry nothing from it. The full includer also links the
re-screened patients' earlier numbers, dates every central sample from the EDC's sample tracking page and counts
the IRT's administrations (a stress row, not the gate)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402


def figures(P, cut, rescreen, collection, irt):
    out = {}
    for k, v in A.ask_sae(P, cut, rescreen=rescreen).items():
        out[("sae",) + k] = v
    for k, v in A.ask_liver(P, cut, collection=collection, irt=True).items():
        out[("liver",) + k] = v
    for k, v in A.ask_exposure(P, cut, irt=irt).items():
        out[("expo",) + k] = v
    return out


def main(target=TARGET):
    P = A.Pack(target)
    cut, _ = A.find_cut(P)
    gold = figures(P, cut, True, True, True)
    n = len(gold)
    crack = figures(P, cut, False, False, False)
    full = figures(P, cut, True, True, True)
    kc = sum(crack[k] == v for k, v in gold.items())
    kf = sum(full[k] == v for k, v in gold.items())
    lc = kc / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, filed rules, battery; cases by the export's screening numbers, central samples "
          "by the transfer's date, exposure from the EDC): keeps %d of %d ask criteria, response %.1f" % (kc, n, c))
    print("mirror (the stratified Cox ratio on the call, band A; same ask handling): keeps %d of %d, response %.1f"
          % (kc, n, s))
    print("full includer (re-screen links, sample-tracking dates, IRT administrations; stress row): keeps %d of %d, "
          "response %.1f" % (kf, n, 38 + 7 + 55 * kf / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    for k in sorted(gold):
        print("  %-48s golden %5d  cracker %5d  %s" % (" ".join(map(str, k)), gold[k], crack[k],
                                                      "miss" if crack[k] != gold[k] else "KEEP"))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
