"""The pair ceiling on the cut pack (supplemental-stumping Part 0, on its 38, 7 and 55 weights).

The cracker lands the call (every docked bike that broke on a ride counted out of working order from that ride until
a van took it in, so the four priority stations and every station's lowest month) and runs the hygiene battery (the
trips' repeated week dropped, voided sales netted, every feed ID joined through the station list, times put on
Eastern time) and executes every filed rule it is pointed at: ask A as the sales export's own pay_station column, ask
B as each card-stopping alarm (the register's codes) paired with its code's next clear. The mirror stops at the
default path (the feed's available count as the bikes in working order) and reads every ask the same way, since the
asks consume nothing the call's construction produces (checks.py X1 and X2 assert the separation). The other rows give
the cracker one more repair at a time. A hit is a figure inside half a unit of its stated rounding.

    python3 task482/generator/ceiling.py [target]
"""
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import bundle as B   # noqa: E402

W_REC, W_IF, W_ASK, R_WRONG = 38.0, 7.0, 55.0, 5.0


def figures(I, call, a_basis, b_basis):
    av = B.golden(I) if call == "golden" else B.default(I)
    pr = tuple(B.designated(av))
    nb, margin = B.nearest_clear(av)
    out = {"call": pr, "nearest": nb, "margin": B.hround(margin)}
    for no in I.nos:
        out["m|%02d" % no] = int(B.hround(min(av[no].values()), 0))
    sa = B.sales(I, attribution=a_basis) if a_basis in ("history", "column") else B.sales(I, tz="utc")
    for no, v in sa.items():
        out["A|%02d" % no] = round(v, 2)
    for no, v in B.downtime(I, pairing=b_basis).items():
        out["B|%02d" % no] = int(B.hround(v, 0))
    return out


def score(gold, resp):
    asks = [k for k in gold if k.split("|")[0] in ("A", "B")]
    main = [k for k in gold if k.startswith("m|")] + ["nearest", "margin"]
    kept = [k for k in asks if resp[k] == gold[k]]
    call = resp["call"] == gold["call"]
    mk = sum(1 for k in main if resp[k] == gold[k])
    rec = (W_REC * (0.4 + 0.6 * mk / len(main))) if call else R_WRONG
    return rec + W_IF + W_ASK * len(kept) / len(asks), kept, asks, call, mk, len(main)


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    I = B.Inputs(target)
    gold = figures(I, "golden", "history", "restart")
    rows = {"cracker": figures(I, "golden", "column", "clear"),
            "mirror": figures(I, "default", "column", "clear"),
            "cracker who drops the alarms with no clear": figures(I, "golden", "column", "drop"),
            "cracker who ends an open alarm at the next event of any kind": figures(I, "golden", "column", "next_any"),
            "cracker who places each sale by its terminal's history": figures(I, "golden", "history", "clear"),
            "cracker who ends each alarm at a restart": figures(I, "golden", "column", "restart"),
            "mirror who ends an open alarm at the next event of any kind": figures(I, "default", "column", "next_any"),
            "cracker who does both asks": figures(I, "golden", "history", "restart")}
    out = {}
    for name, resp in rows.items():
        sc, kept, asks, call, mk, nm = score(gold, resp)
        out[name] = (sc, kept, asks)
        ka = sum(1 for k in kept if k.startswith("A|"))
        kb = sum(1 for k in kept if k.startswith("B|"))
        print("%-62s call %-5s main %2d/%d  ask A %2d/24  ask B %2d/24  score %.1f" % (name, call, mk, nm, ka, kb, sc))
    sc, sm = out["cracker"][0], out["mirror"][0]
    worst = max((out[c][0] + out[m][0]) / 2 for c in ("cracker", "cracker who ends an open alarm at the next event of any kind")
                for m in ("mirror", "mirror who ends an open alarm at the next event of any kind"))
    print("Pair ceiling: %.1f (with the next-event repair on both: %.1f)" % ((sc + sm) / 2, worst))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * len(out["mirror"][1]) / len(out["mirror"][2])))
    return (sc + sm) / 2, worst


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
