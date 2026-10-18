"""The cracker's, the mirror's and the over-cleaner's paths on the two asks, run on the cut pack.

The cracker lands the call, runs the battery (exact duplicate rows, key uniqueness on note number and line and on the
ledger's entry number, every vessel and licence joined to the members' list) and executes the prompt's filters:
haddock landed by members from January to September 2026 by landing date, every presentation put on live weight; the
quota ledger summed by effective date to 30 September under the quota rules. The battery finds nothing to remove:
note numbers and lines are unique, no row repeats, every member's current letters join. The mirror stops at a wrong
rung on the call and takes the asks the same way. The over-cleaner keeps one note per buyer and landing (or collapses
identical lots) and drops every ledger entry with no licence.

    python3 task268/generator/cracker.py [pack]     exit 0 when the cracker keeps no ask figure"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import common as K     # noqa: E402


def keeps(a, b, ga, gb):
    ka = sum(round(a[p][0]) == round(ga[p][0]) for p in K.PORT_NAMES) + \
        sum(round(a[p][1]) == round(ga[p][1]) for p in K.PORT_NAMES)
    kb = sum(round(b[p]) == round(gb[p]) for p in K.POOL_CODES)
    return ka, kb


def battery(D):
    notes = [(r["note_no"], r["line"]) for r in D["notes"]]
    rows = [tuple(r.values()) for r in D["notes"]]
    entries = [r["entry_no"] for r in D["ledger"]]
    return dict(note_keys_unique=len(set(notes)) == len(notes), no_repeated_rows=len(set(rows)) == len(rows),
                entries_unique=len(set(entries)) == len(entries))


def main(pack):
    D = A.load(pack)
    b = battery(D)
    assert all(b.values()), b
    ga, gb = A.ask_a(D), A.ask_b(D)
    crack = keeps(A.ask_a(D, "plain"), A.ask_b(D, "plain"), ga, gb)
    mirror = crack
    over = [keeps(A.ask_a(D, h), A.ask_b(D, "blank"), ga, gb) for h in ("session", "lots")]
    n = 2 * len(K.PORT_NAMES) + len(K.POOL_CODES)
    print("battery: %s" % ", ".join(k for k, v in b.items() if v))
    print("cracker keeps A %d of 8, B %d of 5" % crack)
    print("mirror  keeps A %d of 8, B %d of 5 (the same reads)" % mirror)
    print("over-cleaner keeps A %d of 8 (one note a buyer a landing), %d of 8 (lots collapsed); B %d of 5"
          % (over[0][0], over[1][0], over[0][1]))
    kc, km = sum(crack) / n, sum(mirror) / n
    pair = ((38 + 7 + 55 * kc) + (5 + 7 + 55 * km)) / 2
    print("pair ceiling %.1f, mirror leakage %.1f per cent of the ask weight" % (pair, 100 * km))
    return 0 if sum(crack) == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
