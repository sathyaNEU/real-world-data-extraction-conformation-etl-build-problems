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
    gold_a = {k: v for k, v in pay.items() if ":" not in k}
    stm = AN.pilot_payments(T, "statements")
    convs = AN.load_conversations(T)
    statements = AN.load_statements(T)
    # half-handled: each pharmacy's rate read off its first statement over the quarter's conversations held now
    half = {}
    for ph in gold_a:
        s = sorted((x for x in statements if x["pharmacy"] == ph), key=lambda x: x["date"])[0]
        q0 = AN.quarter_start(s["date"])
        held_now = sum(1 for c in convs if c["pharmacy"] == ph and q0 <= c["date"] <= s["date"] and c["cancelled"] is None)
        rate = s["amount"] / held_now
        half[ph] = rate * sum(1 for c in convs if c["pharmacy"] == ph and c["cancelled"] is None)
    cu = AN.continuing_users(T)
    pseud = AN.continuing_users(T, "pseudonyms")
    # over-joined: every pseudonym sharing a birth date and sex taken for one person
    D = AN.load(T)
    by_key = collections.defaultdict(list)
    for pid in D["disp"]:
        by_key[D["meta"][pid]].append(pid)
    out = collections.Counter()
    for key, pids in by_key.items():
        ds = sorted((d for p in pids for d in D["disp"][p] if d["date"].year == 2026), key=lambda d: (d["date"], d["product"]))
        if {(d["date"].month - 1) // 3 for d in ds} == {0, 1, 2, 3} and ds[-1]["prescriber"] in D["practices"]:
            out[ds[-1]["prescriber"]] += 1
    over = {c: out.get(c, 0) for c in D["practices"]}
    return gold_a, {"statements summed": stm, "rate off the first statement": half}, cu, {
        "pseudonyms counted": pseud, "birth date and sex joined": over}


def main():
    gold_a, a_paths, gold_b, b_paths = ask_stops()
    n_ask = len(gold_a) + len(gold_b)
    print("Ask A ladder (8 pharmacies, whole kroner):")
    for name, path in a_paths.items():
        print("  %-32s keeps %d of %d  %s" % (name, kept(path, gold_a), len(gold_a),
                                             {k: int(round(path[k] - gold_a[k])) for k in sorted(gold_a)}))
    print("Ask B ladder (16 practices, persons):")
    for name, path in b_paths.items():
        print("  %-32s keeps %d of %d  %s" % (name, kept(path, gold_b), len(gold_b),
                                             {k: path[k] - gold_b[k] for k in sorted(gold_b)}))
    # the cracker takes, per ask, whichever path short of the device keeps the most figures
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
    print("Full includer (both devices handled): L = 1.000, landed 100.0, off the call 67.0")


if __name__ == "__main__":
    main()
