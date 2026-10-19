"""task249 pair measurement on the cut pack: the ask figures each modelled response keeps, and the pair ceiling.

The cracker lands the call (spans from the spreads) and takes the ask the way a careful analyst who has not met the
device would: the dictionary's status codes for the whole quarter (firmware 4.2's), OZ19B joined to OZ19 from the log,
distinct local hours, every record at the time it is stamped. The mirror stops at the paired
slope and takes the asks by the path that keeps it the most figures. The careful alternatives (every device met) are
printed too.

    python3 task249/generator/pair.py [target]
"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import solve

TARGET = os.path.join(os.path.dirname(HERE), "target")


def main(target=TARGET):
    pk, sp, pull = solve.solve(target, B.FILES)
    ga = pk.ask_a()
    paths = {}
    for name, kw in [("cracker (dictionary codes, stamps as written)", dict(fw_aware=False, retime=False)),
                     ("the firmware met, stamps as written", dict(retime=False)),
                     ("stamps re-timed, dictionary codes", dict(fw_aware=False)),
                     ("dictionary codes, stamps as written, orphan dropped", dict(fw_aware=False, retime=False,
                                                                                  merge_spare=False)),
                     ("every device met", {})]:
        pk._nodes(**kw)
        paths[name] = pk.ask_a()
    pk._nodes(fw_aware=False, retime=False)
    paths["dictionary codes, stamps as written, rows counted"] = pk.ask_a(count="rows")
    pk._nodes()
    n = len(ga)
    keep = {}
    for k, a in paths.items():
        hits = sum(a[c] == ga[c] for c in ga)
        keep[k] = hits / n
        print("%-42s keeps %2d of %d ask figures" % (k, hits, n))
    mirror = max(v for k, v in keep.items() if k != "every device met")
    lc = keep["cracker (dictionary codes, stamps as written)"]
    r_miss = 38 * 0.12
    c, s = 38 + 7 + 55 * lc, r_miss + 7 + 55 * mirror
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * mirror))
    full = keep["every device met"]
    print("If the cracker meets every device: %.1f; if both miss the call and meet every device: %.1f" % (
        (38 + 7 + 55 * full + s) / 2, r_miss + 7 + 55 * full))
    return (c + s) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else TARGET)
