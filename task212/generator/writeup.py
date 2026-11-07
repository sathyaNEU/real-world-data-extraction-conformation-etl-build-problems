"""Emit task212/submission.md from generator/figures.json (every figure read from the file, none typed)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
HUBS = [("ZAZ", "Zaragoza Plaza"), ("VLC", "Ribarroja"), ("SVQ", "Dos Hermanas"), ("MAD", "San Fernando"),
        ("BCN", "El Prat"), ("BIO", "Basauri")]


def n(v):
    return "{:,}".format(v)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    L = []
    L += ["## Tags", "",
          "**Domain:** General Statistics & Data Science, exploratory data analysis and distribution assessment (a Spanish "
          "parcel carrier's outbound cage audits and the one sortation engineering survey slot before the 2026 peak).  ",
          "**Analytical objective:** Anomaly Detection & Diagnostics (whose sorter causes the audited damage excess, and "
          "what its repairs stop over the peak).", ""]
    L += ["## 1. Final Recommendation", "",
          "**Send the sortation engineering survey to %s; its repairs would stop about %s damaged parcels a week over "
          "peak weeks %s.** At equal load in the cage its sorter damages about %d parcels per 10,000 inspected more than "
          "the network does, and no other hub comes within 30 of it. Not Zaragoza Plaza, which leads on audited "
          "damage because cartons loaded on top of its cages crush the parcels beneath, and sits below the network at "
          "equal load. Not Dos Hermanas, whose excess is the same crush under cases loaded part way through the cage."
          % (F["call"], n(F["parcels_week_stopped"]), F["peak_weeks"], F["vlc_own_damage_per_10k"]), ""]
    L += ["## 2. Critical Components", "",
          "1. Each audited parcel's load is the DWS weight of the parcels scanned into its cage after it, read from the "
          "cage build log; at equal load Zaragoza Plaza sits below the network and Dos Hermanas close to it.",
          "2. Ribarroja's own sorter damage is **%d per 10,000 parcels inspected** above the network at equal load."
          % F["vlc_own_damage_per_10k"],
          "3. Ribarroja's planned parcels a week over peak weeks %s average **%s**." % (F["peak_weeks"],
                                                                                    n(F["vlc_planned_parcels_week"])),
          "4. The survey's repairs stop **%s damaged parcels a week** over the peak." % n(F["parcels_week_stopped"]), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Took the routine audits in audit_headers_q3_2026.csv and their OK and DAMAGED lines in "
          "audit_findings_q3_2026.parquet (any damage code, old or new list), per the audit procedure.",
          "2. Joined each parcel's first DWS weighing (dws_induction_q3_2026.parquet, grams), shape and size, and its "
          "service and fragile flag from shipment_lines_q3_2026.parquet, by barcode.",
          "3. Ordered each cage's LOAD scans in cage_build_log_q3_2026.parquet and summed the DWS weights of the parcels "
          "scanned after each parcel: its load on top.",
          "4. Fitted the six-hub logistic expectation on shape, log weight, fragility, service and the heavy-carton "
          "flag with the load in each form tried (steps at several weights, linear, log, cartons above, heaviest "
          "parcel above, with and without packaging terms, with the position and cage-weight terms added) and kept "
          "the lowest BIC, per the programme: 60 kg or more on top, by packaging; Ribarroja %d per 10,000 above, no "
          "other hub within 30 of it."
          % F["vlc_own_damage_per_10k"],
          "5. Applied that rate to Ribarroja's mean planned parcels over weeks %s in peak_plan_2026.xlsx (%s): %s damaged "
          "parcels a week." % (F["peak_weeks"], n(F["vlc_planned_parcels_week"]), n(F["parcels_week_stopped"])),
          "6. Claims: charged each parcel's first approved case to its first hub sort in "
          "tracking_events_claimed_parcels.parquet, counted a flat-rate account's case as its approved amount over the "
          "account's rate in flat_rate_damage_terms.xlsx, and added to the transfers in claims_transfers_2026.xlsx the "
          "card refunds in card_refunds_settlement_2026-07-01_2026-10-22.csv of each private sender's approved amount "
          "made on or after its decision.",
          "7. Stoppages: took the PLC's STOP to RUN spells in sorter_event_log_q3_2026.csv, read the safety system's "
          "STOPs on the PLC's clock through the offset of the stops both record, started each PLC RUN no STOP precedes "
          "at its safety STOP, and added each corrective order in sorter_work_orders_q3_2026.xlsx that matches no "
          "logged spell.",
          "8. Recommended the survey for %s." % F["call"], ""]
    L += ["## 4. Deliverable Answers", "", "### survey_case_note.pdf", "",
          "1. Survey hub: %s." % F["call"],
          "2. Damaged parcels a week its repairs stop over the peak: %s." % n(F["parcels_week_stopped"]),
          "3. Bar chart of each hub's audited damage per 10,000 parcels inspected beside the part its own sorter "
          "accounts for (%d at Ribarroja, none at the other hubs) on page 1." % F["vlc_own_damage_per_10k"], "",
          "### hub_damage_q3_2026.xlsx", "",
          "1. Damaged parcels with an approved claim, by hub:"]
    L += ["   - %s: %s" % (nm, n(F["claims_%s" % k])) for k, nm in HUBS]
    L += ["2. Euros paid on them, by hub:"]
    L += ["   - %s: EUR %s" % (nm, n(F["claims_eur_%s" % k])) for k, nm in HUBS]
    L += ["3. Sorter stoppages, by hub:"]
    L += ["   - %s: %s" % (nm, n(F["stoppages_%s" % k])) for k, nm in HUBS]
    L += ["4. Hours stood, by hub:"]
    L += ["   - %s: %.1f" % (nm, F["hours_%s" % k]) for k, nm in HUBS]
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
