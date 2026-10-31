"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task118/generator/ceiling.py

Rows. The cracker lands the call, runs the battery (UTC to MST, exact repeats dropped, the latest restatement of a
nomination kept) and executes every filed rule (schedule 2's three hours, USD 15 and USD 255 a premise, the event's
month; OP-7 section 6's ready thermostat, IDLE under the 6.0 firmware, and the utility's commercial meters), but
joins Cool Credit premises through the CIS's enrolled serial, tests each Brightwell record on its own, and keeps
the latest nomination per Arroyo reference. The mirror stops at the weather-model rung on the call and handles the
asks the same way, since they carry nothing from it. The full includer also links devices by address, combines a
battery's records for an event and keeps the latest nomination per meter (a stress row, not the gate)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import figs as F  # noqa: E402

BANKED = 1        # the note's chart, built by every response that draws one


def figures(target, a_link, a_idle, b_split, c_dedupe, c_territory):
    a = F.ask_a(target, a_link, a_idle)
    bm, bc = F.ask_b(target, split=b_split)
    c = F.ask_c(target, c_dedupe, c_territory)
    return ([a[d] for d in sorted(a)], [bm[m] for m in sorted(bm)] + [bc], [int(round(c[m])) for m in sorted(c)])


def kept(resp, gold):
    return sum(x == y for r, g in zip(resp, gold) for x, y in zip(r, g))


def main(target=TARGET):
    gold = figures(target, "address", "switch", "combine", "meter", "register")
    n = sum(len(g) for g in gold) + BANKED
    crack = kept(figures(target, "serial", "switch", "per_record", "ref", "register"), gold) + BANKED
    crack2 = kept(figures(target, "exact", "switch", "per_record", "ref", "register"), gold) + BANKED
    full = kept(figures(target, "address", "switch", "combine", "meter", "register"), gold) + BANKED
    worst = max(crack, crack2)
    lc = worst / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery, filed rules; CIS serials, records alone, the latest nomination per "
          "reference): keeps %d of %d ask criteria, response %.1f" % (crack, n, 38 + 7 + 55 * crack / n))
    print("cracker linking the registry by the address as written: keeps %d of %d" % (crack2, n))
    print("mirror (stops at the weather-model rung, same ask handling): keeps %d of %d, response %.1f" % (worst, n, s))
    print("full includer (address links, combined records, the latest nomination per meter; stress row): keeps %d of "
          "%d, response %.1f" % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
