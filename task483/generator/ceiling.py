"""The pair ceiling on the cut pack (supplemental-stumping Part 0, on its 38, 7 and 55 weights).

The cracker lands the call (every program's median rebuilt from its cells' pooled distributions, every grant
completer's day-180 status dated from each job's own pay) and every program's figure, runs the hygiene battery (keys
unique, amended wage reports superseding originals, every program joined through the inventory, both student systems'
ID formats, both loan-type code sets) and executes every filed rule it is pointed at: ask A as the board's payments to
the college in its 2025 fiscal year by payment date, each payment row under its program; ask B as each completer's
Direct Subsidized and Unsubsidized disbursements as exported, returns netted, parent PLUS loans left out. The mirror
stops at the default path (cell medians averaged, any pay in the quarter holding day 180) and reads every ask the same
way, since the asks consume nothing the call's construction produces (checks.py X1 and X2 assert the separation). A hit
is a figure inside half a unit of its stated rounding.

    python3 task483/generator/ceiling.py [target]
"""
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import bundle as B   # noqa: E402

W_REC, W_IF, W_ASK, R_WRONG = 38.0, 7.0, 55.0, 5.0


def figures(I, deg_route, short_route, a_basis, b_basis):
    c = B.call(I, deg_route, short_route)
    out = {"call": c["renews"], "share": B.hround(c["share"]),
           "fail": tuple(sorted(p for p, d in list(c["deg"].items()) + list(c["short"].items())
                                if d["tested"] and not d["passes"]))}
    for p, d in c["deg"].items():
        if d["tested"]:
            out["m|" + p] = B.hround(d["figure"] / 1000.0)
    for p, d in c["short"].items():
        if d["tested"]:
            out["m|" + p] = B.hround(d["figure"])
    for p, v in B.ask_a(I, a_basis).items():
        out["A|" + p] = v
    for p, v in B.ask_b(I, b_basis).items():
        out["B|" + p] = v[1]
    return out


def score(gold, resp):
    asks = [k for k in gold if k[:2] in ("A|", "B|")]
    main = [k for k in gold if k.startswith("m|")] + ["share", "fail"]
    kept = [k for k in asks if resp[k] == gold[k]]
    call = resp["call"] == gold["call"]
    mk = sum(1 for k in main if resp[k] == gold[k])
    rec = (W_REC * (0.4 + 0.6 * mk / len(main))) if call else R_WRONG
    return rec + W_IF + W_ASK * len(kept) / len(asks), kept, asks, call, mk, len(main)


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    I = B.Inputs(target)
    gold = figures(I, "golden", "golden", "golden", "golden")
    rows = {"cracker": figures(I, "golden", "golden", "ledger", "net"),
            "mirror": figures(I, "naive", "quarter", "ledger", "net"),
            "cracker who reconciles the payments to the invoice register": figures(I, "golden", "golden", "register",
                                                                                   "net"),
            "cracker who also carries each refund to its participant": figures(I, "golden", "golden", "golden", "net"),
            "cracker who grosses up the aid system's net amounts": figures(I, "golden", "golden", "ledger", "golden"),
            "cracker who does both asks": figures(I, "golden", "golden", "golden", "golden")}
    out = {}
    for name, resp in rows.items():
        sc, kept, asks, call, mk, nm = score(gold, resp)
        out[name] = (sc, kept, asks)
        ka = sum(1 for k in kept if k.startswith("A|"))
        kb = sum(1 for k in kept if k.startswith("B|"))
        print("%-62s call %-5s main %2d/%d  ask A %2d/11  ask B %2d/12  score %.1f" % (name, call, mk, nm, ka, kb, sc))
    sc, sm = out["cracker"][0], out["mirror"][0]
    print("Pair ceiling: %.1f" % ((sc + sm) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * len(out["mirror"][1]) / len(out["mirror"][2])))
    return (sc + sm) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
