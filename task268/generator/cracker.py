"""The cracker's and the mirror's paths on the two asks, measured on the cut pack.

The cracker lands the call, runs the battery (exact duplicate rows, key uniqueness on listing_id, on city, address and suite
and on scrape date, brand and store code, every tract joined to the planning map) and executes the prompt's filters:
on the market on 30 September 2026 by date listed, status and status date, ground floor, retail or flex, 150 to
450 m2, every rent basis put on a yearly rate per m2; delivering on 30 September by that day's scrape and services.
The mirror stops at the share by industry group and takes the asks the same way. The over-cleaner keeps one unit per
address and drops every street both finders list.

    python3 task268/generator/cracker.py task268/target      exit 0 when the cracker keeps no ask figure"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import common as K     # noqa: E402


def battery(D):
    """What the hygiene sweeps find on the ask files: nothing."""
    L, S = D["listings"], D["locators"]
    found = []
    if len({x["listing_id"] for x in L}) != len(L):
        found.append("listing_id repeats")
    if len({tuple(sorted(x.items())) for x in L}) != len(L):
        found.append("exact duplicate listings")
    on = [x for x in L if A.on_market(x)]
    if len({(x["city"], x["address"], x["suite"]) for x in on}) != len(on):
        found.append("city, address and suite repeat among units on the market")
    if len({(x["scrape_date"], x["brand"], x["store_code"]) for x in S}) != len(S):
        found.append("store code repeats in a scrape")
    if len({tuple(sorted(x.items())) for x in S}) != len(S):
        found.append("exact duplicate scrape rows")
    return found


def score(D, a, b):
    ga, gb = A.ask_a(D), A.ask_b(D)
    keep_a = sum(a[m][0] == ga[m][0] for m in K.METRO_NAMES) + sum(
        a[m][1] is not None and int(a[m][1] + .5) == int(ga[m][1] + .5) for m in K.METRO_NAMES)
    keep_b = sum(b[k] == gb[k] for k in gb)
    return keep_a, keep_b


def main(pack):
    D = A.load(pack)
    found = battery(D)
    print("battery finds:", found or "nothing")
    crack = score(D, A.ask_a(D, "plain"), A.ask_b(D, "plain"))
    mirror = crack                     # the mirror takes the asks the same way: the asks read nothing the call reads
    over = score(D, A.ask_a(D, "per_address"), A.ask_b(D, "per_street"))
    status = score(D, A.ask_a(D, "status_as_exported"), A.ask_b(D, "plain"))
    n = 24
    print("cracker keeps A %d of 12, B %d of 12" % crack)
    print("mirror  keeps A %d of 12, B %d of 12 (the same reads)" % mirror)
    print("over-cleaner keeps A %d of 12, B %d of 12" % over)
    print("status read as exported keeps A %d of 12" % status[0])
    # Part 0's weights: a landed call banks 38 + 7; the best miss keeps about 5 of the recommendation side and the 7
    kc, km = sum(crack) / n, sum(mirror) / n
    pair = ((38 + 7 + 55 * kc) + (5 + 7 + 55 * km)) / 2
    print("pair ceiling %.1f, mirror leakage %.1f per cent of the ask weight" % (pair, 100 * km))
    return 0 if sum(crack) == 0 and not found else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
