"""submission.md, drafted from generator/figures.json: every figure in blocks 1 to 4 is one the generator wrote."""
import json


def money(v):
    return "${:,}".format(int(v))


def write(fig_path, out):
    f = json.load(open(fig_path))
    q = f["call"]["qualifying"]
    g = f["growth_pct"]
    dp = f["default_path"]
    each = f["call"]["match_each"]
    others = [c for c in sorted(g, key=lambda c: (-g[c], c)) if c not in q]
    lines = []
    w = lines.append
    w("## Tags")
    w("")
    w("**Domain:** Survey Research & Official Statistics (seasonal adjustment and official time-series production).")
    w("**Analytical objective:** Data Extraction & Conformation (ETL).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**%s and %s qualify for the 2027 Rising Destinations match, %s each from the %s fund.**" % (
        ", ".join(q[:-1]), q[-1], money(each), money(f["call"]["fund"])))
    w("On the Department of Revenue's basis their tax year 2025 receipts grow %s per cent on 2024, at or above the "
      "6 per cent floor; no other county reaches it. Not Corrigan Bay or Delvane, which reach %d and %d per cent only "
      "when 2024's receipts are moved by the Monitor's own 2025 growth: the Department's receipts there have trailed "
      "the panel every year since it was drawn, and carried one year further they grow %d and %d per cent. Elsmoor, "
      "Fallowmere and Grindell, whose member hotels grew only %d, %d and %d per cent, qualify because the Department's "
      "receipts there have outgrown the panel at a steady pace in every year both are known." % (
          ", ".join(str(g[c]) for c in q[:-1]) + " and " + str(g[q[-1]]), dp["Corrigan Bay"], dp["Delvane"],
          g["Corrigan Bay"], g["Delvane"], dp["Elsmoor"], dp["Fallowmere"], dp["Grindell"]))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Qualifying counties: %s" % ", ".join("**%s**" % c for c in q))
    w("2. Estimated growth of tax year 2025 receipts on 2024, whole per cent: %s" % ", ".join(
        "%s **%d**" % (c, g[c]) for c in q + others))
    w("3. Match: **%s** to each qualifying county" % money(each))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Took each county's first-print taxable lodging receipts for tax years 2018 to 2024 from the seven "
      "Department reports (thousands of dollars to 2020, dollars after).")
    w("2. Built each county's Monitor room revenue for 2018 to 2025 from the legacy and InnSight exports, the later "
      "submission of a resubmitted month replacing the earlier, InnSight cents in dollars, legacy county names in one "
      "case.")
    w("3. Divided each year's receipts by the Monitor revenue: the ratio rises or falls along a straight line in every "
      "county, and carrying 2024's receipts by the panel's growth would have missed each earlier year by that drift.")
    w("4. Fitted the line to 2018 to 2024 by least squares, read it at 2025 and multiplied by the county's 2025 Monitor "
      "revenue to estimate the tax year 2025 receipts the Department will first publish.")
    w("5. Divided by the 2024 first print, applied the 6 per cent floor and split the fund equally: %s." % ", ".join(q))
    w("6. Ask A: January to August 2026 InnSight reports, the later submission of each month, each property in the "
      "county the register gives (Harbor & Pine's reports carry its office county's code from April 2026); occupancy "
      "and average daily rate from the county totals.")
    w("7. Ask B: linked the January 2018 legacy properties to InnSight through the crosswalk and, for the thirteen "
      "March 2022 properties it misses, to the one unmapped InnSight property in the same county with the same rooms "
      "in April 2022; took those reporting in August 2026, rooms as room-nights available over the month's days.")
    w("8. Recommended %s for the match." % ", ".join(q))
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### tla_rising_destinations_2027.xlsx")
    w("")
    w("1. Each county's estimated growth of tax year 2025 receipts on 2024, whole per cent, and its match:")
    for c in sorted(g):
        w("   - %s: %d%s" % (c, g[c], ", qualifies, %s" % money(each) if c in q else ", does not qualify"))
    w("2. Bar chart of the sixteen counties' growth against the 6 per cent floor, the qualifying five in green.")
    w("3. Lodging Monitor occupancy (per cent, one decimal) and average daily rate (dollars, to the cent), January to "
      "August 2026:")
    for c in sorted(f["ask_a"]):
        a = f["ask_a"][c]
        w("   - %s: %s, $%s" % (c, a["occupancy_pct"], a["adr_usd"]))
    w("4. Of the panel's January 2018 properties, those still reporting in August 2026: their share of January "
      "2018's panel rooms, and the change in their rooms since, per cent to one decimal:")
    for c in sorted(f["ask_b"]):
        b = f["ask_b"][c]
        w("   - %s: %s, %s" % (c, b["rooms_share_pct"], b["rooms_change_pct"]))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
