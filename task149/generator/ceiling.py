"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden figures, and the pair priced on the planning weights
(38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task149/generator/ceiling.py

Rows. The cracker lands the call and runs the battery: the panel's UTC stamps to Irish time through the time-zone
database (the clock change of 31 October handled), ordinary weekdays from the calendar file, each station joined
to the code it replaced through the register, rows summed per station-day, and every gate asset joined to the
asset register on its asset number, keeping each asset's current station (the habitual one-row lookup); it times
each journey to work by the start of the long workplace stay it already built for the commuting days. The mirror
stops on the call's default rung and handles the asks the same way. The first-station row keeps each asset's first
station instead, and the fixed-offset row converts every stamp at UTC+1 (stress rows); the full includer places each
asset by its dated rows and times each journey by its first stay of the day in the workplace zone (the golden, a
check row)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402


def score(resp_a, resp_b, F):
    n = len(F["station_ratio"]) + len(F["arrival_share"])
    k = sum(int(round(100 * resp_a[s])) == v for s, v in F["station_ratio"].items() if resp_a.get(s))
    k += sum(int(round(100 * resp_b[z])) == v for z, v in F["arrival_share"].items() if z in resp_b)
    return k, n


def main(target=TARGET):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    D = A.load(target)
    W = A.workers(D)
    if not F["station_ratio"] or not F["arrival_share"]:
        raise SystemExit("ceiling: no ask figure to score; refusing to print a ceiling")
    last = {k: v[0] for k, v in A.station_ratios(D, mode="last").items()}
    first_st = {k: v[0] for k, v in A.station_ratios(D, mode="first").items()}
    gold_a = {k: v[0] for k, v in A.station_ratios(D).items()}
    long_arr = A.arrivals(D, W, mode="long")[0]
    zone_arr = A.arrivals(D, W)[0]
    ist = A.arrivals(D, W, clock="ist")[0]
    crack, n = score(last, long_arr, F)
    first_row, _ = score(first_st, long_arr, F)
    fixed, _ = score(last, ist, F)
    full, _ = score(gold_a, zone_arr, F)
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call; battery; each asset at its current station; long workplace stay as arrival): keeps "
          "%d of %d ask criteria, response %.1f" % (crack, n, c))
    print("mirror (default rung on the call, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("first-station cracker (each asset at its first station, stress row): keeps %d of %d" % (first_row, n))
    print("fixed-offset cracker (every stamp at UTC+1, stress row): keeps %d of %d" % (fixed, n))
    print("full includer (assets by their dated rows, first stay in the zone, check row): keeps %d of %d" % (full, n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc, crack, n, full


if __name__ == "__main__":
    main()
