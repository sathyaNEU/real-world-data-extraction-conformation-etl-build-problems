"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task146/generator/ceiling.py

The cracker lands the call and executes every filed rule (baseline by date on or before the first dose, study day
1 from the dosing log, the composite, the rescue classes, the diary day in local time with after-midnight entries to
the evening before, four of seven days), runs the battery (units, dd.mm.yyyy dates, pounds) and reads each file the
way it presents itself: a rescue phototherapy is a row that says phototherapy, and a diary entry belongs to the
patient whose subject listing carries its handheld. The mirror files 100 mg on the arm rates and handles the asks the
same way, since they carry nothing from the call. The full includer also reads NB-UVB and PUVA as phototherapy and
links every handheld through the device log (a stress row, not the gate)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402


def figures(target, light, link):
    P = A.Pack(target)
    P.light, P.link = light, link
    out = {}
    for k, v in A.ask_pasi(P).items():
        out[("pasi",) + k] = v
    for k, v in A.ask_itch(P).items():
        out[("itch",) + k] = v
    return out


def main(target=TARGET):
    gold = figures(target, True, "log")
    n = len(gold)
    crack = figures(target, False, "listing")
    kc = sum(crack[k] == v for k, v in gold.items())
    lc = kc / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, filed rules, battery; rescue read where a row says phototherapy, handhelds linked "
          "through the subject listing): keeps %d of %d ask criteria, response %.1f" % (kc, n, c))
    print("mirror (100 mg on the arm rates; same ask handling): keeps %d of %d, response %.1f" % (kc, n, s))
    print("full includer (NB-UVB and PUVA as phototherapy, the device log): keeps %d of %d, response %.1f" % (n, n, 100.0))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    for ask in ("pasi", "itch"):
        ks = [k for k in gold if k[0] == ask]
        miss = sum(crack[k] != gold[k] for k in ks)
        print("  ask %s: the cracker misses %d of %d" % (ask, miss, len(ks)))
    for k in sorted(gold):
        print("  %-30s golden %6.1f  cracker %6.1f  %s" % (" ".join(map(str, k)), gold[k], crack[k],
                                                        "miss" if crack[k] != gold[k] else "KEEP"))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
