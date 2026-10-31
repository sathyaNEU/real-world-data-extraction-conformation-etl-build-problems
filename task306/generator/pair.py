"""task306 pair measurement on the cut pack. The cracker lands the call and runs the hygiene battery: on the 2026 claims
it sees the web form's notified-date loss dates and re-dates every line from the adjusters' instructions, joined on
the claim number with the reopened line's suffix and the portal's spaces removed, one date a claim (the join's fan-out
collapsed to the claim's first instruction), and executes the wording's 72-hour clause; on the farm book it applies
the register's shares on the policies' main holding CPH, dropping the register's unmatched rows as lapsed
arrangements. The mirror stops at the default path on the call (one ratio for every storm) and does the asks as the
cracker does. Every ask figure is scored against the golden at its rounding; prints the cracker sheet, the mirror's
leakage and the pair ceiling.

    python3 task306/generator/pair.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A
import world as W

TARGET = os.path.join(os.path.dirname(HERE), "target")
REC, IF, ASK = 38.0, 7.0, 55.0


def ask_figures(a, b):
    out = {}
    for i, o in enumerate(a["occurrences"]):
        out["A occ%d home" % i] = (o["start"], round(o["home"], -3))
        out["A occ%d farm" % i] = (o["start"], round(o["farm"], -3))
    out["A recovery"] = round(a["recovery"], -3)
    out["A reinstatement"] = round(a["reinstatement"], -3)
    for c in W.COUNTIES:
        out["B %s buildings" % c] = round(b[c][0] / 1e6, 1)
        out["B %s contents" % c] = round(b[c][1] / 1e6, 1)
    return out


def main_figures(o):
    return {"call": o["value"] > 0, "release": round(o["release_sec"] / 1e6), "margin": round(o["margin_sec"] / 1e6, 1),
            "value": round(o["value"] / 1e6, 1), "gross": round(o["gross"] / 1e6), "net_base": round(o["net_base"] / 1e6),
            "net_both": round(o["net_both"] / 1e6)}


def score(fig, gold):
    hits = [k for k in gold if fig.get(k) == gold[k]]
    return hits, len(hits) / len(gold)


def main(target=TARGET):
    gold_a, gold_b = A.ask_a(target), A.ask_b(target)
    gold = ask_figures(gold_a, gold_b)
    gm = main_figures(A.programme(target, "golden"))
    paths = {
        "cracker": (A.ask_a(target, "first"), A.ask_b(target, "main")),
        "cracker, the fan-out kept at the last instruction": (A.ask_a(target, "last"), A.ask_b(target, "main")),
        "cracker, the instructions joined on the full claim number": (A.ask_a(target, "full"), A.ask_b(target, "main")),
        "cracker, the shares joined holding by holding": (A.ask_a(target, "first"), A.ask_b(target, "holding")),
        "cracker, the recorded loss dates kept": (A.ask_a(target, "recorded"), A.ask_b(target, "main")),
    }
    print("Ask figures: %d (A %d, B %d)" % (len(gold), sum(1 for k in gold if k.startswith("A")),
                                           sum(1 for k in gold if k.startswith("B"))))
    keep = {}
    for name, (a, b) in paths.items():
        hits, share = score(ask_figures(a, b), gold)
        keep[name] = share
        print("%-58s keeps %2d of %d ask figures (%.1f per cent)%s" % (name, len(hits), len(gold), 100 * share,
                                                                         ": " + ", ".join(hits) if hits else ""))
    mm = main_figures(A.programme(target, "pooled"))
    mirror_main = sum(1 for k in gm if mm[k] == gm[k]) / len(gm)
    lc = max(keep.values())
    ls = keep["cracker"]
    c = REC + IF + ASK * lc
    s = REC * mirror_main + IF + ASK * ls
    print("mirror (one ratio for every storm) keeps %d of %d main figures: %s" % (
        round(mirror_main * len(gm)), len(gm), ", ".join(k for k in gm if mm[k] == gm[k]) or "none"))
    print("Pair ceiling: %.1f ((%.0f + %.0f + %.0f x %.2f) and (%.1f + %.0f + %.0f x %.2f), averaged)" % (
        (c + s) / 2, REC, IF, ASK, lc, REC * mirror_main, IF, ASK, ls))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    return (c + s) / 2, 100 * ls


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else TARGET)
