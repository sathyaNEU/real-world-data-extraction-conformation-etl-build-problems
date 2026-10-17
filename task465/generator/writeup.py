"""Write task465/submission.md from generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402


def _and(names):
    return ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]


def n(v):
    return "{:,}".format(int(v))


def write(fig_path, out_path):
    F = json.load(open(fig_path))
    st = F["call"]["by_division"]
    pr = F["pilot_rates"]
    F_ = W.FILES
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** General Statistics & Data Science (data integration: two state surveys that each measured one "
             "of a programme's two eligibility traits, fused through the county and income band they share with a "
             "utility's screening pilot that asked both).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Staff %d Home Energy Medical Assistance caseworkers for 2027: %s.**" % (
        F["call"]["total"], _and(["%s %d" % (d, st[d]) for d in W.DIV_NAMES])))
    L.append("Each division's 2025 eligible households fuse the energy survey's high-burden share and the health survey's "
             "equipment share in each income band with the screening pilot's odds ratio between the two traits inside the "
             "band (%s under $25,000, %s from $25,000 to $49,999). Not the %d caseworkers that multiplying the two "
             "surveys' shares staffs: inside each band the pilot's high-burden homes report the equipment about three "
             "times as often as the rest (%s against %s per cent under $25,000, %s against %s per cent from $25,000 to "
             "$49,999), so treating the traits as independent undercounts every division.\n" % (
                 "%.2f" % F["psi"]["0"], "%.2f" % F["psi"]["1"], F["rivals"]["independence"]["total"],
                 pr["0"]["equip_high"], pr["0"]["equip_rest"], pr["1"]["equip_high"], pr["1"]["equip_rest"]))
    L.append("## 2. Critical Components\n")
    L.append("1. In the pilot's complete screens the equipment is reported in **%s** per cent of high-burden homes against "
             "**%s** per cent of the rest under $25,000, and in **%s** against **%s** per cent from $25,000 to $49,999." % (
                 pr["0"]["equip_high"], pr["0"]["equip_rest"], pr["1"]["equip_high"], pr["1"]["equip_rest"]))
    L.append("2. The pilot's odds ratio between high energy burden and the equipment inside each band: **%.2f** under "
             "$25,000 and **%.2f** from $25,000 to $49,999." % (F["psi"]["0"], F["psi"]["1"]))
    L.append("3. Caseworkers in total: **%d**." % F["call"]["total"])
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Took each division's counties from %s and each county's households in the two eligible bands from %s "
             "(county rows, not the region and state rows)." % (F_["divisions"], F_["estimates"]))
    L.append("2. From %s, computed each household's annual home energy cost (ELEC_AMT times 12 where ELEC_BASIS is M, "
             "plus GAS_AMT and OTHER_AMT) and its band from HHINC, and took each division and band's WT_FINAL-weighted "
             "share with costs above 6 per cent of income." % F_["heas"])
    L.append("3. From %s, nested INCCAT 1 to 3 and 4 to 5 into the two bands, matched CNTYFIPS to the register's "
             "three-digit codes, and took each division and band's HH_WT-weighted share with MEDEQUIP 1 among answers 1 "
             "and 2." % F_["shs"])
    L.append("4. From %s, kept each address's latest complete screen, computed its burden from HH_INCOME, ELEC_12M and "
             "OTHER_FUELS_12M, and tabulated burden against MED_EQUIPMENT (Yes or No) in each band: odds ratios %.2f and "
             "%.2f." % (F_["pilot"], F["psi"]["0"], F["psi"]["1"]))
    L.append("5. Raked each band's pilot table to each division and band's two survey shares and multiplied the share "
             "with both traits by the households; a Mantel-Haenszel odds ratio, each pilot division's own odds ratio or "
             "the pilot's equipment rate ratio puts every cell on the same hundred. Multiplying the two shares, as if independent inside the "
             "cell, was not used: the pilot rejects independence in both bands, and it staffs %d." % (
                 F["rivals"]["independence"]["total"]))
    L.append("6. Staffed each division at one caseworker for every 400 eligible households or part of that number, from "
             "the unrounded counts: %d in all." % F["call"]["total"])
    L.append("7. Joined accounts into households through PRIOR_ACCOUNT_NO in %s and counted the households with a spell "
             "open on October 31, 2026 (START_DATE on or before it, END_DATE blank or on or after it), each in its "
             "premise county's division." % F_["baseline"])
    L.append("8. Counted the households (accounts joined the same way) with a Completed order in %s whose COMPLETED_UTC "
             "falls from January 1 to October 31, 2026 on Central Time, each in its premise county's division." % (
                 F_["batteries"]))
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % W.GOLDEN["workbook"])
    L.append("1. Each division's eligible households in 2025 (nearest hundred) and caseworkers for 2027:")
    for d in W.DIV_NAMES:
        L.append("   - %s: %s eligible households, %d caseworkers" % (d, n(F["eligible"][d]), st[d]))
    L.append("   - Total caseworkers: %d" % F["call"]["total"])
    L.append("2. Each division's households on the medical baseline rate at the end of October 2026:")
    for d in W.DIV_NAMES:
        L.append("   - %s: %s" % (d, n(F["baseline"][d])))
    L.append("3. Each division's households given a backup battery from January to October 2026:")
    for d in W.DIV_NAMES:
        L.append("   - %s: %s" % (d, n(F["battery"][d])))
    L.append("4. A horizontal bar chart of eligible households by division, each bar labelled with its caseworkers, on the "
             "Caseworkers 2027 sheet.")
    L.append("")
    L.append("### %s\n" % W.GOLDEN["table"])
    L.append("1. Eligible households in 2025 by division and income band (nearest hundred):")
    for d in W.DIV_NAMES:
        for b in W.ELIGIBLE_BANDS:
            L.append("   - %s, %s: %s" % (d, W.BANDS[b].replace("Under", "under"), n(F["cells"]["%s|%d" % (d, b)])))
    txt = "\n".join(L) + "\n"
    assert "\u2014" not in txt and "\u2013" not in txt
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(txt)
    return txt
