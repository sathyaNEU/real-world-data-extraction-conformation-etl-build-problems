"""The pair ceiling, measured on the cut pack: each response's figures recomputed from target/ with the handling that
response applies, scored against the golden on the planning weights (38 for the call and its components, 7 for
instruction-following, 55 for the asks).

    python3 task475/generator/ceiling.py

Rows. The cracker lands the call (the fit of candidate and question) and runs the battery: it converts the portal's
UTC stamps, reads every filed rule (regulation 17's withdrawal timing, 19.4's refunds of changed and declined
reviews, Schedule 1's fees by the day received), normalises names across the two registers and links the November
sitters to the May register on name and date of birth; it dates each withdrawal by the register's status_changed,
counts as May sitters the May entrants the register shows as entered, joins each review request to the May marks on
the number the candidate keyed, and takes an account-paid fee at the schedule rate. The mirror stops at the means rung
on the call (its moves agree with the golden on six questions; its pass count and results file do not) and handles
the asks the same way, since nothing in them comes from the call. The full includer (stress row) handles every ask
the golden way."""
import os
import sys
import warnings

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import params as P  # noqa: E402

W_CALL, W_IF, W_ASK = 38.0, 7.0, 55.0
W_PASS, W_MOVE, W_FILE = 10.0, 3.0, 4.0     # inside the call's 38: the pass count, each move, the results file


def ask_figures(Pk, route):
    C = A.ask_centres(Pk, route)
    R = A.ask_reviews(Pk, route)
    f = {}
    for c in P.CODES:
        for k in ("withdrawals", "absentees", "may_sitters"):
            f["%s %s" % (c, k)] = C[c][k]
    f["reviews changed"] = R["changed"]
    f["refund"] = int(round(R["refund"]))
    return f


def main(target=TARGET):
    Pk = A.Pack(target)
    M = A.main_call(Pk)
    gold = ask_figures(Pk, "golden")
    crack = ask_figures(Pk, "cracker")
    n = len(gold)
    kept_c = sum(crack[k] == v for k, v in gold.items())
    lc = kept_c / float(n)
    moves_ok = sum(int(a == b) for a, b in zip(M["rungs"]["R1 facility"], M["golden"]))
    mirror_call = W_MOVE * moves_ok + (W_PASS if M["passes"]["R1 facility"] == M["n_pass"] else 0.0)
    c = W_CALL + W_IF + W_ASK * lc
    s = mirror_call + W_IF + W_ASK * lc
    print("ask criteria: %d (18 centre figures, results changed on review, refund)" % n)
    print("cracker (lands the call, battery, register dates and entrants, keyed numbers, schedule fees): keeps %d of "
          "%d ask criteria, response %.1f" % (kept_c, n, c))
    print("mirror (the means rung: %d of 8 moves, pass count %d against %d): keeps %d of %d, response %.1f" %
          (moves_ok, M["passes"]["R1 facility"], M["n_pass"], kept_c, n, s))
    print("full includer (every device handled, stress row): keeps %d of %d, response %.1f" % (n, n, c + W_ASK * (1 - lc)))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
