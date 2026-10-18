"""task247 pair measurement on the cut pack. The cracker lands the call and handles the ask files the way the
dictionary and the protocol say: the survey's S sheets at the survey depth, annex genera of 10 cm or more, every slate
line a colony; the loggers trimmed to the log's deployment times read as the loggers' local time. The mirror stops at a
wrong rung on the call and takes each ask by the path that keeps it the most figures among the cracker's and the
lazier ones. Every ask figure is scored against the golden at its rounding (prevalence to one decimal, colonies and
hours whole). The mirror's share of the call's per-site criteria is measured too (expected maximum, level and verdict).
Prints the cracker sheet, the mirror's leakage and the pair ceiling; --ladder prints the design note's ladder figures.

    python3 task247/generator/pair.py [target]
    python3 task247/generator/pair.py --ladder [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import solve

TARGET = os.path.join(os.path.dirname(HERE), "target")


def ask_paths(pk):
    return {
        # the cracker: every filed rule executed, every slate line a colony, the log's times as local time
        "cracker": (pk.survey(collapse=False), pk.logger_hours(gps=False)),
        # lazier: nothing filtered (QA sheets, wrong depth, fire corals, small colonies in); no trimming
        "unfiltered": (pk.survey(collapse=False, filters=False), pk.logger_hours(gps=False)),
        "untrimmed": (pk.survey(collapse=False), pk.logger_hours(gps=False, trim=False)),
    }


def score(pk, paths):
    g, h = pk.survey(), pk.logger_hours()
    n = 3 * len(pk.codes)
    keep = {}
    for k, (sv, hr) in paths.items():
        hits = ["prev " + c for c in pk.codes if round(sv[c][0], 1) == round(g[c][0], 1)] + \
               ["col " + c for c in pk.codes if sv[c][1] == g[c][1]] + \
               ["hours " + c for c in pk.codes if hr[c] == h[c]]
        keep[k] = len(hits) / n
        print("%-11s keeps %2d of %d ask figures %s" % (k, len(hits), n, hits))
    return keep


def mirror_on_call(pk, b, rows):
    ru, c = pk.rungs()
    best = (None, 0.0)
    for k in ["as issued", "pooled", "flag", "regression", "refill, no difference"]:
        v = ru[k]
        right = 0
        for i, r in enumerate(rows):
            lv = solve.level(v[i])
            right += (round(v[i]) == r["dhw_round"]) + (lv == r["level"]) + (solve.verdict(lv, r["declared"]) == r["verdict"])
        on = [pk.codes[i] for i in range(16) if v[i] >= 8]
        share = right / 48.0
        lands = on == [r["site"] for r in rows if r["level"] == "Alert Level 2"]
        print("mirror at %-22s lists %s; %2d of 48 per-site criteria right%s" % (k, on, right,
                                                                                 " (lands the call)" if lands else ""))
        if not lands and share > best[1]:
            best = (k, share)
    return best


def main(target=TARGET):
    pk, b, rows = solve.solve(target, B.FILES)
    keep = score(pk, ask_paths(pk))
    rung, share = mirror_on_call(pk, b, rows)
    r_miss = round(38 * 0.75 * share, 1)
    print("the best wrong rung on the call: %s, keeping %.1f of the 38 recommendation points" % (rung, r_miss))
    lc = keep["cracker"]
    ls = max(keep.values())
    c, s = 38 + 7 + 55 * lc, r_miss + 7 + 55 * ls
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    return (c + s) / 2, 100 * ls


def ladder(target=TARGET):
    pk, b, rows = solve.solve(target, B.FILES)
    ru, c = pk.rungs()
    var = pk.variants(b)
    print("constants", {k: round(v, 4) for k, v in c.items()}, "clear-sky", round(b, 4))
    print("%-22s %s" % ("", " ".join("%5s" % x for x in pk.codes)))
    for k, v in ru.items():
        print("%-22s %s  %s" % (k, " ".join("%5.2f" % x for x in v), [pk.codes[i] for i in range(16) if v[i] >= 8]))
    print("%-22s %s" % ("golden", " ".join("%5.2f" % r["dhw"] for r in rows)))
    for k, v in var.items():
        print("%-22s %s" % (k, " ".join("%5.2f" % x for x in v)))
    for k, v in pk.backtest(b).items():
        print("back-test %-10s rmse %.3f hot mean %+.3f (%d days, %d hot)" % ((k,) + v))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    t = args[0] if args else TARGET
    if "--ladder" in sys.argv:
        ladder(t)
    else:
        main(t)
