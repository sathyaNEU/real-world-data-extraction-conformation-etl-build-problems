"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task457/generator/ceiling.py

Rows: the cracker lands the docket, runs the battery (the Eastern deadline converted from UTC, the first submission
from the history, owed on 31 December) and executes every filed rule, but joins the disclosures by the employee
number as it stands (A), ties register records through the profiles' NPIs (B) and checks the list's companies by
their present names (C); the mirror files the whole-year docket and handles the asks the same way, since they carry
nothing from the call; the full includer also resolves the three devices (a stress row, not the gate). The conformed
file's row count and the chart's structure are banked by every response that builds them."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import asks as A          # noqa: E402
import conform as C       # noqa: E402
import golden as GD       # noqa: E402

BANKED = 2       # the conformed file's row count and the chart's structure


def figures(data, link, attribution, listed):
    a = A.ask_a(data, link=link)
    b = A.ask_b(data, attribution=attribution)
    c = A.ask_c(data, listed=listed)
    return list(a), [GD.thousand(b[k]) for k in sorted(b)], [GD.thousand(c[k]) for k in sorted(c)]


def kept(resp, gold):
    return sum(x == y for r, g in zip(resp, gold) for x, y in zip(r, g))


def main():
    data = C.load(TARGET)
    gold = figures(data, "npi", "profile", "resolve")
    n = sum(len(g) for g in gold) + BANKED
    crack = kept(figures(data, "emp", "profile_npi", "present"), gold) + BANKED
    full = kept(figures(data, "npi", "profile", "resolve"), gold) + BANKED
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc          # the mirror's ask handling is the cracker's: the asks carry nothing from the call
    print("cracker (lands the docket, battery, filed rules; employee numbers as they stand, the profiles' NPIs, the "
          "list's present names): keeps %d of %d ask criteria, response %.1f" % (crack, n, c))
    print("mirror (the whole-year docket, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (resolves all three devices, stress row): keeps %d of %d, response %.1f"
          % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))


if __name__ == "__main__":
    main()
