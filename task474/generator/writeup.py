"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W

TAGS = ("**Domain:** Physical & Environmental Sciences (emissions inventory: an ozone-season NOx inventory from "
        "continuous emissions monitor records whose gaps include hours without NOx control).\n"
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
         "Each emitted %s lb of NOx per gross MWh or more over the 2026 ozone season once the hours its analyzers "
         "were out are filled by the emission state the unit was in. In the hours a plant lost its instrument air "
         "(most of them at Cutler Bend and Ashfork), the first measured hour after each loss reads about twenty times "
         "the unit's usual NOx per MMBtu and falls back over the next hour or two, so the SCR was not removing NOx "
         "while the air was out; those hours are filled at that first-hour NOx per MMBtu, times the hour's heat input; every other hour without a measurement is filled from the unit's measured hours at the "
         "same hour after a start or, later in a run, at the same load. Not a fill of every gap from the unit's "
         "measured hours in the same start state and load, nor the average of the hours either side of each gap: "
         "both put controlled NOx into uncontrolled hours and designate %s, leaving CB-2 and AF-1 under the target." %
         (f["target"], _join(f["state_route"])),
         "",
         "## 2. Critical Components", "",
         "1. Units at or above %s lb per MWh: **%d** of %d." % (f["target"], f["n_call"], f["n_units"]),
         "2. Season operating hours without a NOx measurement: **%s**, of which **%s** inside an instrument air "
         "ticket." % (fmt(f["gaps"]["all"]), fmt(f["gaps"]["air"])),
         "",
         "## 3. Step-by-Step Solution", "",
         "1. Took the combined-cycle units from %s (rule %s) and their operating hours (OP_TIME above zero) from 1 May "
         "to 30 September 2026 in %s, standard time (rule %s), counting each unit's hours since its start along the "
         "whole year's record." % (F["units"], sec["units"], F["dahs"], sec["rate"]),
         "2. Marked as air-loss hours the operating hours with a blank NOX_MASS_LB inside a %s ticket whose "
         "description names the plant instrument air or its compressor, the ticket's local times moved back an hour "
         "to standard time." % F["tickets"],
         "3. Filled every air-loss hour, its own run measured on its return or not, with its HEAT_INPUT_MMBTU times "
         "the unit's mean NOX_MASS_LB over HEAT_INPUT_MMBTU across the clock hours right after its runs of air-loss "
         "hours in which the unit was still operating and measured (a unit with none takes the same mean over its "
         "plant's units).",
         "4. Filled every other blank hour: in hours 1 to 3 after a start with the mean NOX_MASS_LB of the unit's "
         "measured hours at the same hour after a start; later, from the unit's quadratic fit of NOX_MASS_LB on "
         "GLOAD_MW over its measured hours more than 3 hours after a start.",
         "5. Divided each unit's measured and filled NOx by its GLOAD_MW summed over the same hours and designated "
         "every unit at or above %s (rule %s): %s." % (f["target"], sec["designation"], _join(des)),
         "6. Priced each operating hour's HEAT_INPUT_MMBTU at the %s price for the gas day it falls in, the hour "
         "moved from standard time to Central clock time and then back 9 hours (%s, Section 1; rule %s); a gas day "
         "with no invoice line of its own at the delivery point takes the price on the point's next line, which "
         "bills the gas days since the point's previous line together (weekend and holiday gas, traded the business "
         "day before), its quantity the plant's metered burn over those days: $%s in all." % (
             F["invoices"], F["terms"], sec["fuel"], fmt(f["asks"]["fuel_total"])),
         "7. For each unit's equivalent forced outage rate (rule %s), on local time from 1 May to 30 September 2026: "
         "forced outage hours, the hours inside a U1, U2 or U3 event in %s, a later-filed report replacing an earlier "
         "one it overlaps on the same unit; service hours, OP_TIME summed; equivalent forced derated hours, each D1 or "
         "D2 hour at derate_mw over the register's nameplate MW times OP_TIME; the reserve shutdown derated hours, "
         "each D1 or D2 hour outside a full outage at derate_mw over nameplate times one less OP_TIME; the rate, in per cent, is "
         "forced outage hours plus equivalent forced derated hours, over forced outage hours plus service hours plus "
         "the reserve shutdown derated hours." % (sec["outages"], F["events"]),
         "",
         "## 4. Deliverable Answers", "",
         "### %s" % W.GOLDEN["workbook"], "",
         "1. Every combined-cycle unit: designated or not, 2026 ozone-season fuel cost (nearest hundred dollars), "
         "equivalent forced outage rate (per cent, one decimal):"]
    for u in f["units"]:
        r = rows[u]
        L.append("   - %s: %s; $%s; equivalent forced outage rate %.1f%%" % (
            u, "designated" if r["designated"] else "not designated", fmt(r["fuel"]), r["efor"]))
    L += ["", "### %s" % W.GOLDEN["memo"], "",
          "1. The designated units for the Board: %s." % _join(des),
          "2. Bar chart of every combined-cycle unit's 2026 ozone-season NOx rate (lb per gross MWh) against the %s "
          "target line, the designated units' bars in orange." % f["target"]]
    open(out_path, "w", encoding="utf-8").write("\n".join(L) + "\n")
