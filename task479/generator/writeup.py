"""submission.md, drafted from generator/figures.json: every figure in blocks 1 to 4 is one the generator wrote."""
import json

ORDER_NOTE = "in rate order"


def money(v):
    return "${:,}".format(int(v))


def write(fig_path, out):
    f = json.load(open(fig_path))
    rates = f["components"]["rates"]
    order = f["rate_order"]
    five, nxt = f["call"]["five"], f["call"]["next"]
    five_o = [k for k in order if k in five]
    dp = f["default_path"]
    again = f["replayed_2016"]
    csvf = f["csv"]
    lines = []
    w = lines.append
    w("## Tags")
    w("")
    w("**Domain:** General Statistics & Data Science (data integration, record linkage and entity resolution).")
    w("**Analytical objective:** Data Extraction & Conformation (ETL).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**The 2027 private flood placement pilot should run in %s and %s, with %s next in line.**" % (
        ", ".join(five_o[:-1]), five_o[-1], nxt))
    w("The five have the lowest expected claim rates of the fourteen member counties, %s paid building claims per 1,000 "
      "building-years, against %s for %s. Not Kettlemoor or Dunholme, which fall to %s and %s only when every claim "
      "their buildings filed before they were elevated is dropped: the 2016 flood stood above the floors most of those "
      "buildings have now, and replayed on them the two counties stand at %s and %s. Not the record as filed, which "
      "keeps the coast's floods that its elevated floors now clear." % (
          ", ".join(rates[k] for k in five_o[:-1]) + " and " + rates[five_o[-1]], rates[nxt], nxt,
          dp["rates"]["Kettlemoor"], dp["rates"]["Dunholme"], rates["Kettlemoor"], rates["Dunholme"]))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Elevated insured buildings on 30 September 2026: **{:,}**".format(csvf["rows"]))
    w("2. Claims of 2016 that would come again on buildings elevated since: Dunholme **%d**, Kettlemoor **%d**" % (
        again["Dunholme"], again["Kettlemoor"]))
    w("3. Expected claim rates per 1,000 building-years: %s; %s **%s**; Kettlemoor **%s**, Dunholme **%s**" % (
        ", ".join("%s **%s**" % (k, rates[k]) for k in five_o), nxt, rates[nxt], rates["Kettlemoor"],
        rates["Dunholme"]))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. From nfip_dsa_policy_history_2026-10-02.csv took the building policies the guidelines define and the buildings whose "
      "policy in force on 30 September 2026 shows the lowest floor at or above the base flood elevation, NGVD29 "
      "elevations converted with tsrfa_vertical_datum_offsets.csv: {:,} buildings.".format(csvf["rows"]))
    w("2. Counted each building's days of building cover from 1 January 2001 to 31 December 2025 once across its "
      "policies, each policy covering to the day before its expiration or cancellation date, over 365.25.")
    w("3. Joined the claims of nfip_dsa_claims_2001-2019.csv and nfip_dsa_claims_2020-2026.csv (UTC dates taken to "
      "Central time) under those buildings' building policies for losses of 2001 to 2025.")
    w("4. Replayed each claim on the building as it stands on 30 September 2026: its water stood at the claim's lowest floor "
      "elevation plus its depth in inches over 12, and it counts where that is an inch or more above the present "
      "lowest floor, as every building-policy claim with an inch or more of water above its floor was paid: Dunholme "
      "%d and Kettlemoor %d claims of 2016 count again, the coast's none." % (again["Dunholme"], again["Kettlemoor"]))
    w("5. Divided each county's counted claims by its building-years per 1,000 and took the five lowest and the sixth "
      "as the guidelines direct: %s, then %s." % (", ".join(five_o), nxt))
    w("6. Ask A: among claims on 2026 losses with a building payment, merged each claim NFIP Direct entered under a "
      "policy not yet in force at the loss into the claim under the policy its prior_policy_number names for the same "
      "building and date of loss, counting it once at the later record's payments to date, unit owners' claims "
      "counted, as the guidelines direct.")
    w("7. Ask B: in tsrfa_hma_grants_export_2026-09-30.xlsx took the properties not withdrawn with no final inspection "
      "passed by 30 September 2026 in the Inspections sheet (the Properties status of projects approved before "
      "12 January 2026 predates their later inspections), each at its approved cost times the project's federal "
      "cost-share percentage, by the county of its community.")
    w("8. Recommended %s for the pilot, %s next in line." % (", ".join(five_o), nxt))
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### tsrfa_2027_private_flood_pilot.xlsx")
    w("")
    w("1. Expected claim rate per 1,000 building-years, the fourteen counties %s:" % ORDER_NOTE)
    for k in order:
        mark = ", pilot" if k in five else (", next in line" if k == nxt else "")
        w("   - %s: %s%s" % (k, rates[k], mark))
    w("2. The five marked: %s; next in line: %s." % (", ".join(five_o), nxt))
    w("3. Bar chart of the fourteen rates on the Pilot counties sheet, the five shaded dark.")
    w("4. Claims on losses in 2026 that carry a building payment, and the building payments made on them as of the "
      "extract, whole claims and whole dollars:")
    a = f["a_losses"]
    for k in sorted(a):
        w("   - %s: %s claims, %s" % (k, "{:,}".format(a[k]["claims"]), money(a[k]["payments"])))
    w("5. Buildings in elevation and acquisition projects not completed on 30 September 2026, and the federal share "
      "obligated to them, whole buildings and whole dollars:")
    b = f["b_pipeline"]
    for k in sorted(b):
        w("   - %s: %d buildings, %s" % (k, b[k]["buildings"], money(b[k]["federal_share"])))
    w("")
    w("### tsrfa_pilot_elevated_buildings_2026-09-30.csv")
    w("")
    w("1. {:,} rows, one per elevated insured building, with its county, its building-years to one decimal and its "
      "paid building claims as it stands: {:,} claims in all, on {:,} buildings.".format(
          csvf["rows"], csvf["claims"], csvf["buildings_with_a_claim"]))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
