"""Writes task255/submission.md from generator/figures.json, so every figure in it is one the generator computed.

    python3 task255/generator/writeup.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)

ORDER = ["Overstappunten", "Zuidtak", "Oosttak", "Eindhaltes", "Binnenstad", "Centraal", "Ringlijn", "Noordtak",
         "Westtak"]
CODES = {"Centraal": "CEN", "Binnenstad": "BNS", "Overstappunten": "OVP", "Noordtak": "NRD", "Oosttak": "OST",
         "Westtak": "WST", "Zuidtak": "ZDT", "Ringlijn": "RNG", "Eindhaltes": "EIN"}


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    reach, lm = f["reach"], f["reach_linemap"]
    tier = sorted(f["call"], key=lambda k: -f["reach_exact"][k])
    rest = sorted((k for k in reach if k not in tier), key=lambda k: -f["reach_exact"][k])
    near = rest[0]
    names = ", ".join(tier[:-1]) + " and " + tier[-1]
    rates = f["agency_rates_pct"]
    pkg_order = sorted(reach, key=lambda k: list(CODES).index(k))
    L = []
    L += ["## Tags", "",
          "**Domain:** Marketing & Consumer Research (media reach, frequency and audience measurement: a metro "
          "advertising concessionaire's screen packages, effective reach over its autumn audience window).",
          "**Analytical objective:** Descriptive & Distribution Analysis.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Sell %s in Tier G in 2027, at %d, %d and %d per cent effective reach against the 40 per cent line; every "
          "other package stays in the standard tier.** The nearest package below the line is %s at %d per cent. Not "
          "Centraal and Binnenstad: with every change of trains put where the line map puts it they reach %d and %d "
          "per cent, but on weekday peaks the north and east branches run through Centraal into each other, as do the "
          "west and south, so the riders who change there are others than the line map shows and both packages "
          "reach %d per cent."
          % (names, reach[tier[0]], reach[tier[1]], reach[tier[2]], near, reach[near], lm["Centraal"],
             lm["Binnenstad"], reach["Centraal"]), ""]
    L += ["## 2. Critical Components", "",
          "1. The audience window holds **%s** regular riders (passenger cards with a metro journey in each of its "
          "calendar weeks)." % format(f["regular_riders"], ","),
          "2. On weekdays the trains passing Centraal from 07:00 to 09:30 and from 16:00 to 18:30 run north with "
          "east and west with south; at every other time riders change trains where the line map shows.",
          "3. Effective reach is **%d per cent** for %s, **%d per cent** for %s and **%d per cent** for %s, and "
          "**%d per cent** for Centraal and for Binnenstad." % (reach[tier[0]], tier[0], reach[tier[1]], tier[1],
                                                                reach[tier[2]], tier[2], reach["Centraal"]), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Kept the passenger cards (card class reiziger in RVB_productcodes.csv) of "
          "RVB_metro_ritten_20261001_20261104.csv with a journey checked in during each calendar week from 5 October "
          "to 1 November 2026 (rate card 3.2 and 3.3): %s regular riders." % format(f["regular_riders"], ","),
          "2. Gave each of their journeys its check-in and check-out halls through the Gates sheet of "
          "RVB_metronet_planningsmodel_2026.xlsx, old and new gate codes alike, and routed it over the network's lines "
          "by the fewest changes, crediting the interchange passage wherever the route changes line.",
          "3. Read each journey through Centraal from its own duration against the network's walking and run times in "
          "the hours trains run every %d minutes (a change adds the passage walk and a second wait): on weekdays from "
          "07:00 to 09:30 and 16:00 to 18:30 north-south and west-east riders change there and north-east and "
          "west-south riders ride through, and at every other hour the line map holds." % f["headway_min"],
          "4. Counted for each package in Annex A of Spoorbeeld_tariefkaart_2027.pdf the regular riders whose "
          "journeys passed its halls and passages %d times or more (rate card 3.4 and 3.5): %s %d, %s %d and %s %d per "
          "cent, every other package under 40." % (f["effective_frequency"], tier[0], reach[tier[0]], tier[1],
                                                   reach[tier[1]], tier[2], reach[tier[2]]),
          "5. For make-good, took each booked screen's dark hours within the opening hours of terms 6.1 from "
          "cms_player_status_20261001_20261104.csv (UTC to Ravelmond time), on the player its Bekabeling rows in "
          "schermregister_2026-11-12.xlsx give, except that a move off a player that never came back dates from the "
          "receiving player's report of its displays rising by the moved screens, plus Wilgenhof's screens from their "
          "take-down; then the dark hours above %s per cent of booked screen-hours, rounded up (terms 6.3)."
          % f["make_good_allowance_pct"],
          "6. For the 2027 screens, took each asset tag's latest Schermen row hung by 1 January 2027 and not taken "
          "down by then, kept one screen to a location and position (the replacement units of 3 to 5 November came in "
          "under new tags beside rows left open), left out package \"-\" and counted by package.",
          "7. For net revenue, split the VAT out of facturen_oud_systeem_2026.csv, added the invoices and netted every "
          "credit note through its invoice number in billing_export_2026-10-15_2026-11-12.xlsx, and charged each "
          "agency's contract rate (its statement in bureaucommissie_najaar_2026.pdf over the value net of the credit "
          "notes issued by 31 October: Kompasmedia %s, Noordlicht Mediaplanning %s and Bureau Lindeman %s per cent) on "
          "each booking's value net of all its credit notes (terms 8.2 and 8.3)."
          % (rates["Kompasmedia"], rates["Noordlicht Mediaplanning"], rates["Bureau Lindeman"]),
          "8. Recommended Tier G for %s." % names, ""]
    L += ["## 4. Deliverable Answers", "", "### tier_g_2027.xlsx", "",
          "1. Tier G in 2027: %s; every other package in the standard tier." % names,
          "2. Effective reach, whole per cent, and 2027 tier:"]
    for k in ORDER:
        L.append("   - %s (%s): %d, %s" % (k, CODES[k], reach[k], "Tier G" if k in tier else "standard tier"))
    L.append("3. Make-good owed per autumn booking, whole hours:")
    for ref, h in f["make_good_hours"].items():
        L.append("   - %s (%s): %d" % (ref, f["booking_package"][ref], h))
    L.append("4. Screens on sale on 1 January 2027 by package:")
    for k in pkg_order:
        L.append("   - %s: %d" % (k, f["screens_on_sale_2027"][k]))
    L.append("5. Net revenue from the autumn bookings by package, nearest 10 euros:")
    for k in pkg_order:
        L.append("   - %s: EUR %s" % (k, format(f["net_revenue_eur"][k], ",")))
    L += ["", "### tier_g_2027.pdf", "",
          "1. One-page bar chart of every package's effective reach, highest first, with the Tier G line at 40 per "
          "cent drawn across it and %s shaded as Tier G." % names, ""]
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    main()
