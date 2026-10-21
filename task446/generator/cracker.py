"""task446 cracker: the ask layer's two measured responses on the cut pack, scored against the golden's figures.

    python3 task446/generator/cracker.py [<target>]

The cracker lands the call (each flag priced by where in the group it was raised) and executes every filed rule it
points at on the ask paths: each facility once per group (6.1), the limit as it stood at the end of 30 September
UK time read from the UTC history (1.3, 6.1, the field reference), customers not yet grouped placed through GLEIF
(2.2), every booked customer in the group the credit system books it to. That last is where it stops: a company
booked to one group and consolidated through GLEIF into another group's ultimate parent is a member of both under
2.2, and a one-group-per-customer map loses its facility from the consolidating group. The mirror stops on rung 0
of the call (one rate for every flagged group) and handles the asks the same way. Pair ceiling on
supplemental-stumping Part 0's weights (38 recommendation and components for a landed call, about 5 kept by a wrong
one, 7 instruction-following, 55 asks)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve    # noqa: E402
import deliver  # noqa: E402


def r1(x):
    return round(x + 1e-12, 1)


def graded(call, n1, bands, title):
    """the ask figures of block 4, in order: the heading, 25 band figures, the total row, the chart's three parts"""
    out = [("heading", call)]
    for r in bands:
        out += [(r["band"] + " groups", r["groups"]), (r["band"] + " committed", r1(r["committed"] / 1e6)),
                (r["band"] + " flagged", r["flagged"]), (r["band"] + " arrivals", r1(r["exp_arrivals"])),
                (r["band"] + " arriving", r1(r["exp_exposure"] / 1e6))]
    out += [("total groups", sum(r["groups"] for r in bands)),
            ("total committed", r1(sum(r["committed"] for r in bands) / 1e6)),
            ("total flagged", sum(r["flagged"] for r in bands)),
            ("total arrivals", r1(sum(r["exp_arrivals"] for r in bands))),
            ("total arriving", r1(sum(r["exp_exposure"] for r in bands) / 1e6)),
            ("chart bars", tuple(r1(r["exp_arrivals"]) for r in bands)), ("chart caseload", call),
            ("chart title", title % (call, n1))]
    return out


def response(G, model, **kw):
    fc = solve.forecast(G["tab"], model)
    exp = solve.exposures(G["pack"], **kw)
    bt = solve.band_table(G["tab"], fc, exp)
    return graded(round(fc["total"]), fc["N1"], bt, deliver.TITLE)


def main(target):
    G = solve.golden(target)
    gold = graded(G["call"], G["fc"]["N1"], G["bands"], deliver.TITLE)
    handling = dict(grain="group", clock="right", hz=True, member="booked")
    paths = [("cracker (on the call; 6.1, 1.3, the UTC history and 2.2's customers not yet grouped executed; one "
              "group per booked customer)", "split", handling),
             ("mirror (rung 0: one rate for every flagged group; the same handling of the asks)", "hit_and_miss",
              handling)]
    kept = []
    for name, model, kw in paths:
        got = response(G, model, **kw)
        hits = [g[0] for g, h in zip(gold, got) if g[1] == h[1]]
        kept.append(len(hits) / len(gold))
        print("%-118s keeps %2d of %d: %s" % (name, len(hits), len(gold), ", ".join(hits)))
    print("stops on the ask paths (the golden's handling, one reading changed at a time):")
    right = dict(handling, member="both")
    for label, kw in (("2.2 both ways (the golden)", right),
                      ("one group per booked customer", dict(right, member="booked")),
                      ("consolidating group only", dict(right, member="gleif")),
                      ("every extract row summed", dict(right, grain="rows")),
                      ("limit as extracted on 1 October", dict(right, clock="B1")),
                      ("history read on its UTC date", dict(right, clock="B2")),
                      ("latest version in the history", dict(right, clock="B3")),
                      ("customers not yet grouped dropped", dict(right, hz=False))):
        got = response(G, "split", **kw)
        print("   %-38s %2d of %d band and total figures right" %
              (label, sum(1 for g, h in zip(gold[1:31], got[1:31]) if g[1] == h[1]), 30))
    lc, ls = kept
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * ls
    print("Pair ceiling: %.1f (cracker %.1f, mirror %.1f)" % ((c + s) / 2, c, s))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    return (c + s) / 2, 100 * ls


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
