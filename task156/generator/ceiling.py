"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files (a hit is the same figure at the
asked rounding), and the pair priced on the planning weights (38 for the call and its components, 7 for
instruction-following, 55 for the asks).

    python3 task156/generator/ceiling.py

Rows: the cracker lands the call (the replay conditioned on the length of sewer below the water table), runs the
battery and executes every filed rule (the billing policy's spreading and its exclusion of estimates, the consent's
24-hour rule and its emergency definition, the monitors' own clock, each serial placed by the installation history),
but counts each rating unit's dwellings as the 31 October 2026 rating snapshot gives them in every quarter (Ask A) and
matches each station's outages through the ICP the asset register lists for it (Ask B); the mirror files the single
response's connect and handles the asks the same way, since they carry nothing from the call; the full includer also
dates the dwellings and reads every ICP the electricity site list gives a station's address (a stress row, not the
gate)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import asks as A   # noqa: E402


def rnd(x):
    return int(x + 0.5)


def kept(resp, gold):
    return sum(rnd(resp[k]) == rnd(gold[k]) for k in gold)


def main():
    ga, gb = A.ask_a(TARGET), A.ask_b(TARGET)
    n = len(ga) + len(gb)
    ca = kept(A.ask_a(TARGET, dwellings="snapshot"), ga)
    cb = kept(A.ask_b(TARGET, icps="current"), gb)
    crack = ca + cb
    full = kept(A.ask_a(TARGET), ga) + kept(A.ask_b(TARGET), gb)
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery, filed rules; snapshot dwellings, the register's current ICPs): keeps %d of "
          "%d ask figures (Ask A %d of %d, Ask B %d of %d), response %.1f" % (crack, n, ca, len(ga), cb, len(gb), c))
    print("mirror (the single response's connect, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (dated dwellings, every ICP at the address; stress row): keeps %d of %d, response %.1f"
          % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))


if __name__ == "__main__":
    main()
