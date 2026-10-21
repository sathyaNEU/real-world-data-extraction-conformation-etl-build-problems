"""The three screens that refused architecture 1, run on the pack's own clean truth.

Screen 1 prices the estimator family clause 4.2 leaves open: every construction of "the shortfall
the network's own record shows the measurement produces without congestion" a competent analyst
would reach for, with the call each one files and the spread each one puts on the graded figures.

Screen 2 prices the cheapest licensed construction as algebra rather than as a correlation: the
designed max-over-the-eight-quarterly-worst-windows against one column maximum of the same rows.

Screen 3 prices the distortion the design can place against the effect the ladder needs.

Run it twice and require byte-identical output (stumping, the screening harness is evidence):

    python3 screen_estimator_family.py ../target
"""
import os
import sys

import numpy as np
import pandas as pd

import golden as G

Q = "2027Q1"
MARGIN = 1.06        # the margin checks.py asserts between the record and the decided figure


def truth(target):
    """every kept interconnect, evening and window of every quarter, as the goldens read them"""
    (_panel, rollup, register, maint, *_rest) = G.load(target)
    kept, every = G.shortfalls(rollup, register, maint)
    return kept, every


def family(kept):
    """every reference a competent analyst would build once clauses 4.2 and 4.4 are read

    Grouped by which record the reference is read off and at what reach, because that is the axis
    the architecture claims is decisive.
    """
    this = kept[kept["reporting_quarter"] == Q]
    prior = kept[kept["reporting_quarter"] != Q]
    dec = float(this["shortfall"].max())
    port = this.loc[this["shortfall"].idxmax(), "line"]
    qmax = prior.groupby("reporting_quarter")["shortfall"].max()
    pp = prior.groupby(["reporting_quarter", "line"])["shortfall"].max()
    pool = prior["shortfall"]
    own_prior = prior[prior["line"] == port]["shortfall"]
    own_this = this[this["line"] == port]["shortfall"]
    allk = kept["shortfall"]
    out = []

    def add(group, name, value):
        out.append((group, name, float(value)))

    g = "A record, quarter-max reach"
    add(g, "max of the 8 quarterly worst windows", qmax.max())
    add(g, "min of the 8 quarterly worst windows", qmax.min())
    add(g, "mean of the 8 quarterly worst windows", qmax.mean())
    add(g, "median of the 8 quarterly worst windows", qmax.median())
    add(g, "90th pctile of the quarterly worst windows", qmax.quantile(0.9))
    add(g, "10th pctile of the quarterly worst windows", qmax.quantile(0.1))
    add(g, "mean less 1sd of the quarterly worst windows", qmax.mean() - qmax.std(ddof=1))
    add(g, "the most recent quarter's worst window", qmax.loc["2026Q4"])
    add(g, "the same quarter a year ago", qmax.loc["2026Q1"])
    add(g, "mean of the last 4 quarterly worst windows",
        qmax.loc[["2026Q1", "2026Q2", "2026Q3", "2026Q4"]].mean())

    g = "B record, port-quarter reach"
    add(g, "per-port quarterly maxima, largest", pp.max())
    add(g, "per-port quarterly maxima, 90th pctile", pp.quantile(0.9))
    add(g, "per-port quarterly maxima, median", pp.median())
    add(g, "per-port quarterly maxima, mean", pp.mean())
    add(g, "per-port quarterly maxima, smallest", pp.min())
    add(g, "per-port quarterly maxima, mean plus 2sd", pp.mean() + 2 * pp.std(ddof=1))

    g = "C record, pooled windows"
    for p in (0.95, 0.98, 0.99, 0.995, 0.999, 0.9999):
        add(g, "pooled prior windows, %gth pctile" % (p * 100), pool.quantile(p))
    add(g, "pooled prior windows, maximum", pool.max())
    add(g, "pooled prior windows, mean plus 3sd", pool.mean() + 3 * pool.std(ddof=1))
    add(g, "pooled prior windows, mean plus 4sd", pool.mean() + 4 * pool.std(ddof=1))
    add(g, "pooled prior windows, median plus 3 IQR",
        pool.median() + 3 * (pool.quantile(0.75) - pool.quantile(0.25)))

    g = "D the port's own record"
    add(g, "%s own prior record, maximum" % port, own_prior.max())
    for p in (0.99, 0.995, 0.999):
        add(g, "%s own prior record, %gth pctile" % (port, p * 100), own_prior.quantile(p))
    add(g, "%s own prior record, mean plus 3sd" % port,
        own_prior.mean() + 3 * own_prior.std(ddof=1))
    add(g, "%s own prior record, mean plus 4sd" % port,
        own_prior.mean() + 4 * own_prior.std(ddof=1))
    opq = prior[prior["line"] == port].groupby("reporting_quarter")["shortfall"].max()
    add(g, "%s own prior quarterly maxima, mean" % port, opq.mean())
    add(g, "%s own prior quarterly maxima, smallest" % port, opq.min())

    g = "E this quarter, own-path and pooled"
    add(g, "%s own 2027Q1 99th pctile" % port, own_this.quantile(0.99))
    add(g, "%s own 2027Q1 mean plus 3sd" % port, own_this.mean() + 3 * own_this.std(ddof=1))
    add(g, "%s own 2027Q1 mean plus 4sd" % port, own_this.mean() + 4 * own_this.std(ddof=1))
    add(g, "%s own 2027Q1 second largest window" % port, own_this.nlargest(2).iloc[-1])
    add(g, "2027Q1 pooled kept windows, 99th pctile", this["shortfall"].quantile(0.99))
    add(g, "2027Q1 pooled kept windows, 99.9th pctile", this["shortfall"].quantile(0.999))
    add(g, "2027Q1 pooled kept windows, mean plus 3sd",
        this["shortfall"].mean() + 3 * this["shortfall"].std(ddof=1))
    add(g, "2027Q1 the other six ports' largest window",
        this[this["line"] != port]["shortfall"].max())
    add(g, "2027Q1 per-port worst windows, median", this.groupby("line")["shortfall"].max().median())
    add(g, "2027Q1 per-port-per-window maxima, median",
        this.groupby(["line", "window_from"])["shortfall"].max().median())

    g = "F the whole record, 9 quarters"
    add(g, "whole record pooled 99.9th pctile", allk.quantile(0.999))
    add(g, "whole record pooled 99.99th pctile", allk.quantile(0.9999))
    add(g, "whole record per-quarter maxima, mean",
        kept.groupby("reporting_quarter")["shortfall"].max().mean())
    add(g, "whole record pooled mean plus 3sd", allk.mean() + 3 * allk.std(ddof=1))
    return dec, port, out


def screen1(kept):
    this = kept[kept["reporting_quarter"] == Q]
    prior = kept[kept["reporting_quarter"] != Q]
    dec, port, fam = family(kept)
    print("=" * 96)
    print("SCREEN 1  the estimator family clause 4.2 leaves open, priced on the clean truth")
    print("=" * 96)
    print("decided figure (the quarter's worst kept window) : %.0f kbps on %s" % (dec, port))
    print("kept windows this quarter %d, prior record windows %d" % (len(this), len(prior)))
    print()
    print("%-36s %-44s %9s  %s" % ("group", "construction", "ref kbps", "call"))
    for group, name, v in fam:
        print("%-36s %-44s %9.1f  %s"
              % (group, name, v, "none (hold)" if dec <= v else "fund %s" % port))
    vals = np.array([v for _g, _n, v in fam])
    hold = int((vals >= dec).sum())
    print()
    print("family size                : %d constructions" % len(fam))
    print("files the committed hold    : %d of %d (%.1f per cent)"
          % (hold, len(fam), 100.0 * hold / len(fam)))
    print("files a fund                : %d of %d" % (len(fam) - hold, len(fam)))
    print("reference spread            : %.1f to %.1f kbps, range %.1f"
          % (vals.min(), vals.max(), vals.max() - vals.min()))
    print("decision boundary           : %.1f kbps" % dec)
    print("nearest reference below it  : %.1f kbps" % max(v for v in vals if v < dec))
    print("nearest reference above it  : %.1f kbps" % min(v for v in vals if v >= dec))
    print()
    print("by group, which is the selection-breadth axis the architecture rests on:")
    print("%-36s %5s %6s %6s" % ("group", "n", "hold", "fund"))
    for group in sorted({g for g, _n, _v in fam}):
        vs = [v for g, _n, v in fam if g == group]
        h = sum(1 for v in vs if dec <= v)
        print("%-36s %5d %6d %6d" % (group, len(vs), h, len(vs) - h))
    rec = [v for g, _n, v in fam if g[0] in "ABCDF"]
    cur = [v for g, _n, v in fam if g[0] == "E"]
    print()
    print("read off the prior record, at ANY reach : hold %d of %d (%.1f per cent)"
          % (sum(1 for v in rec if dec <= v), len(rec),
             100.0 * sum(1 for v in rec if dec <= v) / len(rec)))
    print("read off this quarter, at ANY reach     : hold %d of %d (%.1f per cent)"
          % (sum(1 for v in cur if dec <= v), len(cur),
             100.0 * sum(1 for v in cur if dec <= v) / len(cur)))
    print()
    print("the spread the family puts on each graded figure of the call:")
    grid = this.groupby(["line", "window_from"])["shortfall"].max()
    print("  the decided shortfall %.0f kbps          : 0.0 kbps, it is a maximum and no reference enters it" % dec)
    print("  the closest interconnect %s           : 0 names, same reason" % port)
    print("  the %d grid worst-window figures        : 0.0 kbps, no reference enters them" % len(grid))
    print("  the evenings left out                  : 0, clause 4.4 fixes them")
    print("  the binary call                        : flips, %d of %d file a fund"
          % (len(fam) - hold, len(fam)))
    return dec, port


def screen2(kept, dec, port):
    prior = kept[kept["reporting_quarter"] != Q]
    print()
    print("=" * 96)
    print("SCREEN 2  the cheapest licensed construction, run as algebra")
    print("=" * 96)
    by_q = prior.groupby("reporting_quarter")["shortfall"].max()
    designed = float(by_q.max())
    cheapest = float(prior["shortfall"].max())
    print("designed   max over the 8 quarterly worst windows   = %.12f" % designed)
    print("cheapest   one column maximum over the same rows    = %.12f" % cheapest)
    print("difference                                          = %.3e" % abs(designed - cheapest))
    print("            an identity, because the maximum of a partition's maxima is the maximum.")
    print("            designed = 1.0 x cheapest + 0.0, slope 1, intercept 0.")
    print()
    row = kept.loc[kept["shortfall"].idxmax()]
    print("the one-group-by route to the call, in one line:")
    print("  subtract the rollup's two median columns, drop clause 4.4's evenings, take one idxmax")
    print("  over all %d kept rows: it lands in %s on %s %s at %.0f kbps, not in %s, so fund nothing."
          % (len(kept), row["reporting_quarter"], row["line"], row["window_from"],
             row["shortfall"], Q))
    print("  one-liner call %-5s   designed call %-5s   agree %s"
          % ("none" if row["reporting_quarter"] != Q else "fund",
             "none" if dec <= designed else "fund",
             (row["reporting_quarter"] != Q) == (dec <= designed)))
    print()
    at = int((prior["shortfall"] >= dec).sum())
    print("and a filter and a count file the same call: %d of %d prior record windows already sit"
          % (at, len(prior)))
    print("at or above %.0f kbps (%.2f per cent of the record)." % (dec, 100.0 * at / len(prior)))
    print()
    print("seven of the eight draws of the statistic enter no graded figure: golden.compute reads")
    print("the eight quarterly maxima only through their maximum.")


def screen3(kept, dec, port):
    this = kept[kept["reporting_quarter"] == Q]
    easy = float(this[this["line"] == port]["shortfall"].quantile(0.99))
    _d, _p, fam = family(kept)
    vals = np.array([v for _g, _n, v in fam])
    print()
    print("=" * 96)
    print("SCREEN 3  the distortion available against the effect the ladder needs")
    print("=" * 96)
    print("the ladder needs : decided above the easy route's reference, the port's own 2027Q1")
    print("                   99th pctile, %.1f kbps" % easy)
    print("Gate C needs     : decided at or below EVERY licensed reference, whose smallest member")
    print("                   is that same %.1f kbps, because the easy route is itself licensed" % easy)
    print("admissible window: [%.1f x %.2f, %.1f / %.2f] = [%.1f, %.1f], EMPTY by %.1f kbps"
          % (easy, MARGIN, easy, MARGIN, easy * MARGIN, easy / MARGIN,
             easy * MARGIN - easy / MARGIN))
    print()
    print("as shipped       : decided %.0f kbps, %.1f per cent above the easy reference, which is"
          % (dec, 100 * (dec / easy - 1)))
    print("                   the same %.1f per cent above the smallest licensed reference"
          % (100 * (dec / vals.min() - 1)))
    print("family spread    : %.1f kbps on a graded quantity of %.0f kbps, %.0f per cent of its own"
          % (vals.max() - vals.min(), dec, 100 * (vals.max() - vals.min()) / dec))
    print("                   level, and %.0f printed units wide at the prompt's nearest kbps"
          % (vals.max() - vals.min()))
    print("boundary sits    : %.1f kbps above the nearest licensed reference below it and %.1f kbps"
          % (dec - max(v for v in vals if v < dec), min(v for v in vals if v >= dec) - dec))
    print("                   below the nearest above it, so inside the family's own spread")
    print()
    print("one dial, both ends the same end: raising the decided figure to clear the easy route is")
    print("what carries it past the licensed references that hold, and lowering it to sit under")
    print("every licensed reference is what puts the easy route on the hold as well.")


def main(target):
    kept, _every = truth(target)
    dec, port = screen1(kept)
    screen2(kept, dec, port)
    screen3(kept, dec, port)
    print()
    print("VERDICT: the decisive step has no estimator content. Architecture 1 is refused.")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(here), "target"))
