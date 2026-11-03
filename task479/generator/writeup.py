"""submission.md from generator/figures.json: every figure in it is one the generator wrote."""
import json

import pack as P

SOLVENTS = ["Methanol", "Toluene", "Isopropanol", "Ethyl acetate", "n-Heptane", "Isohexane", "Tetrahydrofuran"]


def write(fig_path, out):
    f = json.load(open(fig_path))
    c, q = f["call"], f["quarters"]
    qs = ", ".join("Q%d **%s**" % (k, q["Q%d" % k]["tons"]) for k in range(1, 5))
    L = []
    L += ["## Tags", "",
          "**Domain:** Physical & Environmental Sciences (emissions inventory).",
          "**Analytical objective:** Data Extraction & Conformation (ETL).", ""]
    L += ["## 1. Final Recommendation", "",
          "**EU-P1 did not keep within its 2026 VOC limit: it emitted %s tons against the %s-ton calendar-year limit, "
          "over by %s tons.**" % (c["total_tons"], c["limit_tons"], c["margin_tons"]),
          "The vents' summed flow went above RTO-1's %s scfm fan in short coincidences, and the VOC above the fan's "
          "draw left untreated through PSV-31. Not the controlled figure of %s tons, which applies the tested %s per "
          "cent destruction to every vented pound as if the closed-vent system captured all of it. Not the hourly "
          "capacity check at %s tons, which averages away coincidences that last minutes."
          % (c["fan_scfm"], f["default_path"]["tons"], c["dre_pct"], f["hourly_check"]["tons"]), ""]
    L += ["## 2. Critical Components", "",
          "1. VOC emitted from EU-P1 in each quarter of 2026 (tons): %s" % qs,
          "2. Calendar 2026 total **%s tons** against the **%s-ton** limit, over by **%s tons**"
          % (c["total_tons"], c["limit_tons"], c["margin_tons"]),
          "3. VOC released untreated at PSV-31 in 2026, the share of each minute's header VOC above RTO-1's %s scfm "
          "draw: about **%s lb**" % (c["fan_scfm"], f["capture"]["psv31_lb"]), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Put %s (plant local time) and %s (UTC) on one clock with each step once, the in-flight batches' migrated "
          "history in Orbitas taken in place of their Batchwise rows, and keyed every step to %s by product and step "
          "number, the PX line's Nm3/h and kg/h converted to scfm at %s F and to lb/hr."
          % (P.FILES["bw"], P.FILES["orb"], P.FILES["basis"], c["std_temp_f"]),
          "2. Summed every vent's flow and VOC rate minute by minute over 2026, with RTO-1's mode from %s (Eastern "
          "Standard Time all year)." % P.FILES["dahs"],
          "3. In each minute RTO-1 was in RUN, took the share of the header's VOC above the fan's %s scfm (%s) as "
          "released at PSV-31 and applied %s per cent destruction (%s) to the rest; minutes not in RUN were "
          "uncontrolled." % (c["fan_scfm"], P.FILES["reg"], c["dre_pct"], P.FILES["test"]),
          "4. Summed by local calendar quarter under permit B.5 and D.1: %s tons, %s tons for 2026, over the %s-ton "
          "limit by %s tons." % (", ".join(q["Q%d" % k]["tons"] for k in range(1, 5)), c["total_tons"],
                                 c["limit_tons"], c["margin_tons"]),
          "5. Ask: took each delivery once by its bill of lading, its solvent from the supplier's invoice line in %s "
          "(material SOL-07 was n-heptane drums before June 2026), its date the invoice's delivery date (the warehouse "
          "posts after its stock counts), its quantity from %s, gallons at %s's density and kilograms at %s lb/kg."
          % (P.FILES["ap"], P.FILES["wms"], P.FILES["mm"], c["lb_per_kg"]),
          "6. EU-P1 was over its limit in 2026: %s tons, %s tons over." % (c["total_tons"], c["margin_tons"]), ""]
    L += ["## 4. Deliverable Answers", "", "### eu_p1_2026_aq117.xlsx", "",
          "1. AQ-117, VOC emitted from EU-P1 in each quarter of 2026 and calendar year to date (tons):"]
    for k, lab in enumerate(["Jan-Mar", "Apr-Jun", "Jul-Sep", "Oct-Dec"], 1):
        L.append("   - Q%d (%s): %s this quarter, %s year to date" % (k, lab, q["Q%d" % k]["tons"],
                                                                     q["Q%d" % k]["ytd_tons"]))
    L.append("2. Pounds of each solvent delivered to the plant in 2026 (nearest 100 lb):")
    for s in SOLVENTS:
        L.append("   - %s: %s" % (s, f["ask_b"][s]))
    L.append("3. Pounds of all solvents delivered in each quarter of 2026 (nearest 100 lb):")
    for k in range(1, 5):
        L.append("   - Q%d: %s" % (k, f["ask_a"]["Q%d" % k]))
    L += ["", "### eu_p1_2026_determination.docx", "",
          "1. EU-P1 was over its limit: %s tons of VOC in calendar 2026 against the %s-ton limit, over by %s tons."
          % (c["total_tons"], c["limit_tons"], c["margin_tons"]), ""]
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
