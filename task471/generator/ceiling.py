"""The pair ceiling, measured on the cut pack (supplemental-stumping Part 0). The cracker lands the call, runs the
hygiene battery (registration IDs unique and every one in the crosswalk, every completer list's IDs normalised and
duplicates dropped, the program year and the elementary pathways applied as Rule 8.4 files them, voided attempts left
out, every join checked for fan-out) and executes every handling the files document; for the ask it joins the 2024-25
completers in the register to the attempt history on the register's educator ID, and a completer whose record holds no
attempt reads as one who had not tested, which Rule 8.4.4 says is not counted. The mirror stops on the best-scoring
wrong rung of the ladder and builds the ask the same way. Weights 38 / 7 / 55: the main block's 38 as the call (the
set of programs) 8, the raw passing score 2 and, for each program, its rate 1, its passers 0.5 and its completers
counted 0.25; the 55 over the 32 ask figures (each program's 2024-25 completers tested and their rate).

    python3 task471/generator/ceiling.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B      # noqa: E402
import golden as G      # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)


def main(target):
    pk = B.Pack(target)
    comp = pk.completers()
    gcut = pk.cut("golden")[0]
    gold = pk.rates(gcut, comp)
    gset = {k for k, (n, p) in gold.items() if p / n < W.REVIEW_LINE}
    gprior = pk.prior_year()

    def main_score(cut):
        rt = pk.rates(cut, comp)
        st = {k for k, (n, p) in rt.items() if p / n < W.REVIEW_LINE}
        s = 8 * (st == gset) + 2 * (cut == gcut)
        hits = 0
        for k in rt:
            n, p = rt[k]
            n0, p0 = gold[k]
            s += 1.0 * (G.r1(p, n) == G.r1(p0, n0)) + 0.5 * (p == p0) + 0.25 * (n == n0)
            hits += int(G.r1(p, n) == G.r1(p0, n0))
        return s, st == gset, hits, len(st)

    def ask_score(prior):
        hits = 0
        for k in prior:
            n, p = prior[k]
            n0, p0 = gprior[k]
            hits += int(n == n0) + int(G.r1(p, n) == G.r1(p0, n0))
        return 55.0 * hits / 32, hits

    m, _, _, _ = main_score(gcut)
    a, ah = ask_score(pk.prior_year(match="id"))
    C = m + 7 + a
    print("cracker: call landed (raw %d), main %.1f + instructions 7 + ask %.1f (%d of 32 figures) = %.1f" % (
        gcut, m, a, ah, C))
    rungs = {}
    for route in ("no equating", "raters adjusted, no equating"):
        rungs["%s" % route] = [pk.cut(route)[0]]
    for route in ("as scored", "every assignment's papers", "multiple-choice anchor"):
        rungs[route] = sorted({v[0] for v in pk.cut(route, "all").values()})
    best = None
    for k, cuts in rungs.items():
        for c in cuts:
            mm, call, hits, size = main_score(c)
            S = mm + 7 + a
            print("mirror on %-34s raw %d: main %.1f (call %s, %d programs, %2d of 16 rates) + 7 + ask %.1f (%d of 32) "
                  "= %.1f" % (k, c, mm, call, size, hits, a, ah, S))
            if best is None or S > best[0]:
                best = (S, "%s at raw %d" % (k, c))
    pair = (C + best[0]) / 2
    print("Pair ceiling: %.1f (cracker %.1f, best mirror %.1f on %s)" % (pair, C, best[0], best[1]))
    print("Mirror leakage: %.1f per cent of ask weight (%d of 32 figures)" % (100.0 * ah / 32, ah))
    for k, match in (("the register's educator ID (the cracker)", "id"),
                     ("ID, then name and birth date where the ID has no attempts (golden)", "golden")):
        print("ask stop %-70s %d of 32" % (k, ask_score(pk.prior_year(match=match))[1]))
    print("The ask reads the register, which the call never reads, and the attempts it finds under a second record are "
          "first attempts on Form 25A under either record (checks.py S5), so the two responses' ask rows are scored on "
          "the same path by construction.")
    return pair


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
