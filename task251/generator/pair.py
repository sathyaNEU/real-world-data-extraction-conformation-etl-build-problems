"""The ask layer measured on the cut pack: each path a response could take through the data manager's export, the
figures it keeps against the golden, the cracker (on the call: the hygiene battery, the export's own ward and
hospital, the meters' clock read as Italian civil time) and the mirror (off the call, the same care), and the pair
ceiling.
    python3 pair.py [target]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import solve as S

TASK = os.path.dirname(HERE)

# each path: its arguments and the silent devices it has found (c: the solar clock, h: the location history,
# d: the re-sent copies by memory number)
PATHS = {
    "golden": ({}, "chd"),
    "the export as delivered, every row a result": (dict(dedupe="none", clock="civil", where="current"), ""),
    "the same, the copies removed by memory number": (dict(clock="civil", where="current"), "d"),
    "the same, the clock read as UTC": (dict(clock="utc", where="current"), "d"),
    "the copies removed keeping the last reception": (dict(dedupe="last", clock="civil", where="current"), ""),
    "solar clock found": (dict(where="current"), "cd"),
    "location history found": (dict(clock="civil"), "hd"),
    "solar clock and history, copies kept": (dict(dedupe="none"), "ch"),
}


def main(target):
    D = S.load(target, B.FILES)
    res = {k: S.asks(D, **v[0]) for k, v in PATHS.items()}
    g1, g2 = res["golden"]
    n = len(g1) + len(g2)
    sc = {}
    for k, (a1, a2) in res.items():
        k1 = sum(int(round(a1.get(q, -1), 1) == round(v, 1)) for q, v in g1.items())
        k2 = sum(int(a2.get(w, -1) == v) for w, v in g2.items())
        sc[k] = k1 + k2
        print("  %-52s ask 1 %2d/12  ask 2 %2d/13   %2d/%d" % (k, k1, k2, k1 + k2, n))
    natural = [k for k in PATHS if len(PATHS[k][1]) <= 1]
    kc = max(sc[k] for k in natural)
    lc = kc / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (the battery, the copies even removed by memory number, the export's ward, the clock as civil "
          "time) keeps at most %d of %d; the mirror the same" % (kc, n))
    print("pair ceiling %.1f ((%.1f + %.1f) / 2); mirror leakage %.0f per cent of ask weight" % ((c + s) / 2, c, s,
                                                                                                100 * lc))
    one = max(sc[k] for k in PATHS if PATHS[k][1] in ("cd", "hd"))
    print("a reader who finds one of the two silent devices keeps at most %d of %d (%.1f with the call)"
          % (one, n, 38 + 7 + 55 * one / n))
    return sc


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args[0] if args else os.path.join(TASK, "target"))
