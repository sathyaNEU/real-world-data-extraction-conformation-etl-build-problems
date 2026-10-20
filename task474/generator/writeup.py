"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W

TAGS = ("**Domain:** Physical & Environmental Sciences (emissions inventory: an ozone-season NOx inventory from "
        "continuous emissions monitor records with gaps).\n"
        "**Analytical objective:** Data Extraction & Conformation (ETL).")
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def fmt(n):
    return "{:,}".format(int(n))


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    F = W.FILES
    des, rows, sec = f["call"], f["rows"], f["sections"]
    L = ["## Tags", "", TAGS, "",
         "## 1. Final Recommendation", "",
         "**Designate %s of the %s combined-cycle units for the 2027 SCR Upgrade Program: %s.**" % (
             WORDS[f["n_call"]], WORDS[f["n_units"]], _join(des)),
         "Each emitted %s lb of NOx per gross MWh or more over the 2026 ozone season once every hour without a NOx "
         "measurement is filled from the same unit's measured hours at the same number of hours after its start. Not a "
         "fill from each unit's NOx at the same load, nor the measured hours alone: the analyzers were out mostly in "
         "the first hours after a start, when the cold catalyst lets NOx run several times its steady level, so those "
         "routes put steady-state NOx into start-up hours and leave the units that cycle hardest under the target." %
         f["target"],
         "",
         "## 2. Critical Components", "",
         "1. Units at or above %s lb per MWh: **%d** of %d." % (f["target"], f["n_call"], f["n_units"]),
         "2. Season operating hours without a NOx measurement: **%s**, of which **%s** in the first three hours after "
         "a start." % (fmt(f["gaps"]["all"]), fmt(f["gaps"]["start"])),
         "",
         "## 3. Step-by-Step Solution", "",
         "1. Took the combined-cycle units from %s (rule %s) and their operating hours (OP_TIME above zero) from 1 May "
         "to 30 September 2026 in %s, standard time (rule %s)." % (F["units"], sec["units"], F["dahs"], sec["rate"]),
         "2. Counted each unit's hours since its start along the whole year's record (the first operating hour after "
         "an offline hour is hour 1).",
         "3. Filled each operating hour with a blank NOX_MASS_LB: in hours 1 to 3 after a start, with the mean "
         "NOX_MASS_LB of the unit's measured hours at the same hour after a start; later, from the unit's quadratic "
         "fit of NOX_MASS_LB on GLOAD_MW over its measured hours more than 3 hours after a start.",
         "4. Divided each unit's measured and filled NOx by its GLOAD_MW summed over the same hours and designated "
         "every unit at or above %s (rule %s): %s." % (f["target"], sec["designation"], _join(des)),
         "5. Priced each operating hour's HEAT_INPUT_MMBTU at the %s price for the gas day it falls in, the hour "
         "moved from standard time to Central clock time and then back 9 hours (%s, Section 1; rule %s); a gas day "
         "with no invoice line at a delivery point (one month at each) priced at another point's price that day plus "
         "the constant difference between the two points' prices (Section 6, a common Daily Index plus each point's "
         "adder): $%s in all." % (F["invoices"], F["terms"], sec["fuel"], fmt(f["asks"]["fuel_total"])),
         "6. Counted the hours from 1 May to 30 September 2026 in which %s shows the unit in a U1, U2 or U3 event, "
         "where two full outages on one unit overlap keeping the later-reported one (rule %s): %s hours in all." % (
             F["events"], sec["outages"], fmt(f["asks"]["forced_total"])),
         "",
         "## 4. Deliverable Answers", "",
         "### %s" % W.GOLDEN["workbook"], "",
         "1. Every combined-cycle unit: designated or not, 2026 ozone-season fuel cost (nearest dollar), forced outage "
         "hours:"]
    for u in f["units"]:
        r = rows[u]
        L.append("   - %s: %s; $%s; %s forced outage hours" % (
            u, "designated" if r["designated"] else "not designated", fmt(r["fuel"]), fmt(r["forced"])))
    L += ["", "### %s" % W.GOLDEN["memo"], "",
          "1. The designated units for the Board: %s." % _join(des),
          "2. Bar chart of every combined-cycle unit's 2026 ozone-season NOx rate (lb per gross MWh) against the %s "
          "target line, the designated units' bars in orange." % f["target"]]
    open(out_path, "w", encoding="utf-8").write("\n".join(L) + "\n")
