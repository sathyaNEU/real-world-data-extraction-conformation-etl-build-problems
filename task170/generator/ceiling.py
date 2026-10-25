"""task170 ask layer against the careful solver's routes, on the cut pack.

    python3 task170/generator/ceiling.py [target]

Every route a careful reader takes on the two asks, figure by figure, against figures.json. Ask A (Class 461 units
accepted by each Phase 4 go-live): the works records carry the fitment programme's own unit numbers, so vehicles the
fleet team reformed into other units after their works visit sit under the unit they arrived in; every unit still
shows two driving vehicles, and only the formation list says which vehicles a unit now has. Ask C (each Phase 1 to 3
depot's level transition errors and brake interventions in 2026): the recorder downloads' reports carry the
recorder's time (UTC) and are never linked to the driver's or signaller's report of the same event, and some drivers
meet the same transition or speed board again on the return working the same day. The cracker lands the call, runs
the hygiene battery and executes every filed rule (both driving vehicles, the renumbering register, linked and
withdrawn reports); the mirror is the best response off the call. Pair ceiling on the generated rubric's weights (38
recommendation and components, 7 instruction following, 55 asks; a wrong call keeps about 5)."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc     # noqa: E402
import common as C     # noqa: E402

A_ROUTES = {
    "works records by programme unit, renumbering mapped (the cracker)": "programme",
    "works records by programme unit, renumbering not mapped": "raw_unit",
    "either driving vehicle accepted, by the formation list": "any",
    "accepted vehicles only, planned dates ignored": "accepted_only",
    "golden: the formation list's two vehicles, actual or planned dates": "formations",
}
C_ROUTES = {
    "recorder downloads folded within 30 minutes, read as local time (the cracker)": "fold_as_local",
    "one event per driver, unit, category and day": "fold_day",
    "every report, linked ones once (the mirror)": "all_rows",
    "recorder downloads only": "obr_only",
    "drivers' and signallers' reports only": "manual_only",
    "golden: downloads read as UTC and folded within 30 minutes": "golden",
}


def keyed_a(out):
    r = {}
    for c, (a, n) in out.items():
        r["ask_units_accepted_by_golive_%s" % c.lower()] = a
        r["ask_units_not_accepted_by_golive_%s" % c.lower()] = n
    return r


def keyed_c(out):
    r = {}
    for c, (lt, bk) in out.items():
        r["ask_level_transition_errors_2026_%s" % c.lower()] = lt
        r["ask_brake_interventions_2026_%s" % c.lower()] = bk
    return r


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    d = calc.load(target)
    ka = sorted(k for k in figs if k.startswith("ask_units_"))
    kc = sorted(k for k in figs if k.startswith(("ask_level_", "ask_brake_")))
    nA, nC = len(ka), len(kc)
    chart = 3                                    # the chart's bars, labels and segments, right only when ask A is
    total = nA + nC + chart
    print("ask A: %d figures, ask C: %d figures, chart %d criteria tied to ask A" % (nA, nC, chart))
    hits = {}
    for nm, how in A_ROUTES.items():
        out = keyed_a(calc.fleet(d, how))
        h = sum(out[k] == figs[k] for k in ka)
        hits[("A", how)] = h
        print("  A  %-74s %2d of %d" % (nm, h, nA))
    for nm, how in C_ROUTES.items():
        out = keyed_c(calc.events(d, how))
        h = sum(out[k] == figs[k] for k in kc)
        hits[("C", how)] = h
        print("  C  %-74s %2d of %d" % (nm, h, nC))

    def score(on_call, a_how, c_how):
        ha = hits[("A", a_how)]
        kept = ha + hits[("C", c_how)] + (chart if ha == nA else 0)
        L = kept / float(total)
        return (38 + 7 + 55 * L) if on_call else (5 + 7 + 55 * L), kept
    cr, crk = score(True, "programme", "fold_as_local")
    mi, mik = score(False, "programme", "all_rows")
    print("cracker (on the call, programme units, downloads folded as local): %d of %d ask criteria, %.1f" % (crk, total, cr))
    print("mirror (default path 750, programme units, every report): %d of %d ask criteria, %.1f" % (mik, total, mi))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * mik / total))
    print("Pair ceiling: %.1f" % ((cr + mi) / 2))
    for nm, (a, c_) in (("cracker reading the formation list", ("formations", "fold_as_local")),
                        ("cracker converting the downloads' UTC", ("programme", "golden")),
                        ("cracker cracking both", ("formations", "golden"))):
        v, k = score(True, a, c_)
        print("  if the %s: %d of %d, pair %.1f" % (nm, k, total, (v + mi) / 2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
