"""submission.md, drafted from generator/figures.json so every figure it states is one the generator computed.

    python3 task275/generator/writeup.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ORDER = ["TR1", "TR2", "NEP", "BT", "SN", "GN", "LL", "POT"]
NAME = {"TR1": "TR1 (demersal otter trawl, 18 m and over)", "TR2": "TR2 (demersal otter trawl, 12 m to under 18 m)",
        "NEP": "NEP (Nephrops trawl)", "BT": "BT (beam trawl)", "SN": "SN (seine)", "GN": "GN (set gillnet)",
        "LL": "LL (set longline)", "POT": "POT (pots and creels)"}
WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}


def joined(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def thousands(x, nd=1):
    return format(x, ",.%df" % nd)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    sg = f["segments"]
    des = f["call"]["designated"]
    notd = f["call"]["not_designated"]
    dp = f["default_path"]
    near_under = f["call"]["nearest_under"]
    near_over = f["call"]["nearest_over"]
    ins = f["inshore_hours_share"]["BT"]
    tot = f["totals"]
    out = ["## Tags", "",
           "**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement error).",
           "**Analytical objective:** Descriptive & Distribution Analysis.", "",
           "## 1. Final Recommendation", "",
           "**Designate %s of the eight segments for the 2027 Selectivity Programme: %s.**"
           % (WORD[len(des)], joined(des)),
           "They discarded %d to %d per cent of their 2025 catch by weight, %s nearest the line at %d per cent, and "
           "%s, the highest of the rest, discarded %d per cent. Not %s alone, which the observers' discards raised to "
           "every trip give (%s %.1f per cent, %s %.1f, %s %.1f, %s %.1f): an observed trip lands the undersized quota "
           "fish (BMS) that an unobserved trip throws back, so the observers record as kept what the rest of the "
           "fleet discards. %s's observed trips declared %.2f kg of BMS an hour fished and its unobserved trips "
           "%.2f. Not the observed trips' unwanted catch with the grounds pooled, which leaves BT under the line "
           "because observed beam trawl trips fish the inshore grounds less; and not every unobserved trip's BMS "
           "counted as discarded, which puts GN over it although most gillnetters land their BMS every trip."
           % (min(sg[s]["share"] for s in des), max(sg[s]["share"] for s in des),
              joined([s for s in des if sg[s]["share"] == sg[near_over]["share"]]), sg[near_over]["share"],
              near_under, sg[near_under]["share"], "NEP", "NEP", dp["NEP"], "TR1", dp["TR1"], "TR2", dp["TR2"],
              "BT", dp["BT"], "TR1", sg["TR1"]["bms_kg_per_hour_observed"], sg["TR1"]["bms_kg_per_hour_unobserved"]),
           "",
           "## 2. Critical Components", "",
           "1. Discard shares of 2025 catch by weight: %s." % "; ".join(
               "%s **%d** per cent" % (s, sg[s]["share"]) for s in ORDER),
           "2. BMS declared an hour fished, observed against unobserved trips: %s." % "; ".join(
               "%s **%.2f** against **%.2f** kg" % (s, sg[s]["bms_kg_per_hour_observed"],
                                                    sg[s]["bms_kg_per_hour_unobserved"])
               for s in ("TR1", "TR2", "NEP", "BT", "SN")),
           "3. Of the **%s** trips begun in 2025, **%d** were observed; the others' discards are the unwanted catch "
           "(BMS and lawful discards) an hour fished that the same segment's observed trips show on the same "
           "ground, times their hours there, less the BMS they declared." % (format(tot["trips"], ","),
                                                                            tot["observed_trips"]),
           "4. Observed beam trawl trips spent **%d** per cent of their hours on WC14 and WC15 and unobserved ones "
           "**%d** per cent, so the raising is done ground by ground." % (ins["observed"], ins["unobserved"]),
           "",
           "## 3. Step-by-Step Solution", "",
           "1. Took the terms in selectivity_programme_terms_2027.pdf: a segment is designated above 10 per cent of "
           "its 2025 catch by weight, catch being everything landed or returned on every trip begun in 2025, in live "
           "weight.",
           "2. Built each trip from elogbook_trips_2025.csv (ground, hours fished) and elogbook_landings_2025.csv "
           "(live weight above MCRS and BMS), with its segment from vessel_register.csv: %s trips."
           % format(tot["trips"], ","),
           "3. Matched the %d observed trips in observer_deployments_2025.csv to the logbook by vessel (port letters "
           "and number written alike) and notified departure in UK time, and summed observer_hauls_2025.csv by "
           "fraction, each trip's sampled hauls raised to its hours fished (the haul records hold the hauls sampled)."
           % tot["observed_trips"],
           "4. Compared observed with unobserved trips on the same grounds: BMS declared an hour fished (TR1 %.2f "
           "against %.2f kg) against the marketable catch landed an hour, which matched (TR1 %.1f against %.1f kg), "
           "so an observer aboard changes what a vessel lands, not what its hauls bring aboard; and hours on WC14 "
           "and WC15 (BT %d against %d per cent)."
           % (sg["TR1"]["bms_kg_per_hour_observed"], sg["TR1"]["bms_kg_per_hour_unobserved"],
              sg["TR1"]["marketable_kg_per_hour_observed"], sg["TR1"]["marketable_kg_per_hour_unobserved"],
              ins["observed"], ins["unobserved"]),
           "5. For each segment and ground, raised the observed trips' unwanted catch (BMS and DIS) an hour fished "
           "to the unobserved trips' hours there, which is what those trips' hauls brought aboard below size or "
           "unwanted; the BMS they declared was landed and the rest went back to the sea, since the terms' catch is "
           "what was landed and what was returned, so took off the BMS they declared, and added the observed trips' "
           "DIS. Raised by the marketable catch landed instead of hours (BMS left out, being what an observer "
           "changes), the same construction gives every segment the same whole per cent; the observers' discards "
           "alone name %s alone, raised by hours or by landed weight."
           % joined(f["default_path_by_landed_weight_designated"]),
           "6. Divided each segment's discards by its catch (every trip's declared landings plus those discards) and "
           "designated the segments above 10 per cent: %s." % joined(des),
           "7. For first-sale value, summed sales_notes_2025.csv over 2025 landing dates, leaving out the lines Barlow "
           "& Hobbs filed at Kestlemouth and Brindlesea for lots the market sold (the vessel, landing date, species "
           "and grade of a market lot, the weight within 3 per cent of the lot's).",
           "8. For days at sea, counted UK calendar days with a report outside port_limits.csv in "
           "vms_positions_2025.csv, each report given to the vessel that carried its terminal (the terms count a "
           "vessel's own reports). Under the vessel the extract names, %d vessels report from two terminals in the "
           "same UTC hour, in %s hours, most of them more than %d nautical miles apart, and one of each vessel's two is "
           "a terminal vms_transponders.csv holds as one vessel's previous (the terminal it carried before) and "
           "another's current; so such a terminal was the first vessel's until that vessel's own terminal began "
           "reporting, the second's after its previous terminal stopped."
           % (f["vms_two_terminals"]["vessels"], format(f["vms_two_terminals"]["vessel_hours"], ","),
              f["vms_two_terminals"]["apart_nm"]),
           "",
           "## 4. Deliverable Answers", "",
           "### segment_discards_2025.xlsx", "",
           "1. Discard share of 2025 catch (whole per cent) and designation, every segment:"]
    for s in ORDER:
        out.append("   - %s: %d per cent, %s" % (NAME[s], sg[s]["share"],
                                                "designated" if sg[s]["designated"] else "not designated"))
    out.append("2. First-sale value of 2025 landings (thousands of pounds, one decimal):")
    for s in ORDER:
        out.append("   - %s: %s" % (s, thousands(sg[s]["first_sale_gbp_thousands"])))
    out.append("3. Vessels' total days at sea in 2025 (whole days):")
    for s in ORDER:
        out.append("   - %s: %s" % (s, format(sg[s]["days_at_sea"], ",")))
    out += ["", "### segment_discards_2025.png", "",
            "1. One bar chart of the eight segments' discard shares against the 10 per cent line, the %s designated "
            "segments (%s) highlighted." % (WORD[len(des)], joined(des))]
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
