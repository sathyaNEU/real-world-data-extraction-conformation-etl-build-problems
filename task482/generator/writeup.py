"""submission.md, drafted from generator/figures.json: every figure in blocks 1 to 4 is one the generator wrote."""
import json

NAMES = {"KB": "Kilbrannagh", "AC": "Ardcullen", "LF": "Lisnafeen", "RG": "Rathgowan", "TV": "Tullyvane",
         "MR": "Moyrath", "GS": "Glenaskin", "DM": "Dunmarra", "CT": "Clonteevan", "IR": "Innishrue",
         "CV": "Carrigvore", "KF": "Knockfeerin", "BM": "Ballymarne", "CL": "Corlespie", "AV": "Annaghvale",
         "DS": "Drumshallon"}


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def write(fig_path, out):
    f = json.load(open(fig_path))
    d = f["call"]["designated"]
    dp = f["default_path"]["designated"]
    ch = f["change"]
    codes = sorted(f["ask"], key=lambda k: NAMES[k])
    nm = lambda ks: [NAMES[k] for k in sorted(ks, key=lambda k: NAMES[k])]
    lines = []
    w = lines.append
    w("## Tags")
    w("")
    w("**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).")
    w("**Analytical objective:** Data Extraction & Conformation (ETL).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**Designate %s as rapid price growth areas for 2027.**" % _and(nm(d)))
    w("The market value of each one's dwelling stock rose by more than 8 per cent in the year to September 2026 on the "
      "year before; no other area's did. Each dwelling type's change is held to constant quality by a hedonic "
      "regression with location, and the four are weighted by the census stock's value, because apartments sell far "
      "more often than the stock holds them and in some areas rose differently from houses: one year effect for all "
      "sales would designate %s." % _and(nm(dp)))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Areas designated: %s" % ", ".join("**%s**" % x for x in nm(d)))
    w("2. Areas not designated: %s" % ", ".join(nm([k for k in codes if k not in d])))
    w("3. Price change, year to September 2026 (per cent): %s" % "; ".join(
        "%s %.1f" % (NAMES[k], ch[k]) for k in sorted(codes, key=lambda k: -ch[k])))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Read both price register extracts: the old layout's day-first dates and euro text prices, its new-dwelling "
      "prices grossed up by 13.5 per cent VAT, and the new system's consideration including VAT.")
    w("2. Joined each old-layout sale to the valuation register by its normalised eircode, or by its address where "
      "no eircode was keyed, and each new-system sale by property number; counted the filings made in both systems "
      "from 1 to 10 October 2025 once.")
    w("3. Took each dwelling's type, floor area and newness from the valuation register and its electoral division "
      "from the address point file through the eircode.")
    w("4. Kept sales at full market price dated 1 October 2024 to 30 September 2026 by date of sale.")
    w("5. For each area regressed log price on a year-to-September-2026 indicator for each dwelling type, dwelling "
      "type, log floor area, new dwelling and electoral division.")
    w("6. Weighted each type's exp(year effect) by the census count of that type times its mean first-year price "
      "(the stock's value) and took the weighted mean less one as the area's change.")
    w("7. Designated the areas over 8 per cent: %s." % ", ".join(nm(d)))
    w("8. Ask: every residential sale dated 1 October 2025 to 30 September 2026, any market basis; the apartments of a "
      "housing body's block share one building, date and consideration (the block's total on each line), so each "
      "block is one purchase paid once.")
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### bso_area_property_price_change_2026.xlsx")
    w("")
    w("1. Areas designated: %s." % ", ".join(nm(d)))
    w("2. Chart of every area's price change against the 8 per cent line, the designated areas marked.")
    w("3. Price change, year to September 2026 on the year before (per cent, one decimal):")
    for k in codes:
        w("   - %s: %.1f" % (NAMES[k], ch[k]))
    w("4. Residential purchases in the year to September 2026, number and total paid including VAT (whole euros):")
    for k in codes:
        w("   - %s: %s purchases, EUR %s" % (NAMES[k], "{:,}".format(f["ask"][k]["purchases"]),
                                            "{:,}".format(f["ask"][k]["paid"])))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
