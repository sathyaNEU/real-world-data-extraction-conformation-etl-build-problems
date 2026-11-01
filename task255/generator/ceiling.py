"""The ask sheet's pair ceiling and mirror leakage, measured on the cut pack: the cracker (lands the call, runs the
hygiene battery, executes every filed rule) and the mirror (the best response off the call, the WHO-DDD rung, with
the same ask handling), each ask figure kept only when it equals the golden. Also prints each ask's ladder stops."""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import analysis as AN  # noqa: E402

T = os.path.join(TASK_DIR, "target")


def kept(path, gold):
    return sum(1 for k in gold if path.get(k) is not None and round(path[k]) == round(gold[k]))


def ask_stops():
    pay = AN.pilot_payments(T)
    gold_a = {(ph[:4], q): v for ph in pay if ph.endswith(":q") for q, v in pay[ph].items()}
    a_paths = {}
    for name, mode in (("statement as the quarter's figure", "statements"),
                       ("rate off each statement over conversations standing now", "held_now")):
        r = AN.pilot_payments(T, mode)
        a_paths[name] = {(ph[:4], q): v for ph in r if ph.endswith(":q") for q, v in r[ph].items()}
    cu = AN.continuing_users(T)
    b_paths = {"pseudonyms counted": AN.continuing_users(T, "pseudonyms"),
               "birth date and sex joined": AN.continuing_users(T, "birth_sex"),
               "CPR previous number joined (programme 3.3 executed)": cu}
    return gold_a, a_paths, cu, b_paths


def main():
    gold_a, a_paths, gold_b, b_paths = ask_stops()
    n_ask = len(gold_a) + len(gold_b)
    print("Ask A ladder (8 pharmacies x 4 quarters, whole kroner):")
    for name, path in a_paths.items():
        print("  %-56s keeps %d of %d" % (name, kept(path, gold_a), len(gold_a)))
    print("Ask B ladder (16 practices, persons):")
    for name, path in b_paths.items():
        print("  %-56s keeps %d of %d  total %d" % (name, kept(path, gold_b), len(gold_b), sum(path.values())))
    # the cracker takes, per ask, whichever of its paths keeps the most figures; on ask B the filed rule (3.3) and the
    # CPR person table's previous number are its path, so it keeps the ask
    crack = max(kept(p, gold_a) for p in a_paths.values()) + max(kept(p, gold_b) for p in b_paths.values())
    lc = crack / float(n_ask)
    G = AN.main_call(T)
    M = AN.main_call(T, "ddd")
    lm = lc
    landed = G.joins
    print("cracker: the call %s, asks kept %d of %d (L = %.3f)" % (landed, crack, n_ask, lc))
    print("mirror: the call %s (off), the same ask handling (L = %.3f)" % (M.joins, lm))
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lm
    print("Pair ceiling: %.1f ((38 + 7 + 55 x %.3f) and (5 + 7 + 55 x %.3f), averaged)" % ((c + s) / 2, lc, lm))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * lm))
    print("Full includer (the statements' scope handled too): L = 1.000, landed 100.0, off the call 67.0")


if __name__ == "__main__":
    main()
