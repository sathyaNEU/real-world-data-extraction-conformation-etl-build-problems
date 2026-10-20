"""submission.md, drafted from figures.json's own values: tags, the recommendation, the critical components, at most
eight steps and the deliverable answers."""
import world as W

TAGS = ("> **Domain:** Survey Research & Official Statistics (census, register and administrative data quality).\n"
        "> **Analytical objective:** Data Extraction & Conformation (ETL).")


def write(path, x):
    import golden as GD
    g = GD.figures(x)
    rows, nb = g["rows"], {n["nbhd"]: n for n in g["nb"]}
    rec = g["call"]
    t = {r["tract"]: r for r in rows}
    e = x["tre"][(1, "0403.00")]
    e3 = x["tre"][(1, "0303.00")]
    p403, p303 = GD.pct(e.x / e.u), GD.pct(e3.x / e3.u)
    others = [n for n in W.NEIGHBOURHOODS if n not in rec]
    L = ["## Tags", "", TAGS, "",
         "## 1. Final Recommendation", "",
         "**Recommend %s of the five candidates, %s, for the 2027 round of the Neighborhood Stabilization Fund.**" % (
             GD.WORDS[len(rec)], " and ".join(rec)),
         "Each has three listed 2020 tracts at 20 per cent or more in 2019 to 2023 with a rise from 2014 to 2018 "
         "significant at 90 per cent; %s. Not Linden Row, whose tract 303.01 rises only against its old tract's %s "
         "per cent and stood at %s on its own block groups; Kestrel Park qualifies because tract 403.02 stood at %s, "
         "not the old tract's %s." % ("; ".join("%s has %s" % (n, GD.WORDS[nb[n]["count"]]) for n in others),
                                       p303, t["303.01"]["r18"], t["403.02"]["r18"], p403),
         "",
         "## 2. Critical Components", "",
         "1. Tract 403.02's 2014 to 2018 poverty rate on its own block groups is **%s%%** (z **%s**)." % (
             t["403.02"]["r18"], t["403.02"]["z"]),
         "2. Tract 303.01's 2014 to 2018 poverty rate on its own block groups is **%s%%** (z **%s**)." % (
             t["303.01"]["r18"], t["303.01"]["z"]),
         "3. Qualifying tracts: %s." % ", ".join("%s **%d**" % (n, nb[n]["count"]) for n in W.NEIGHBOURHOODS),
         "",
         "## 3. Step-by-Step Solution", "",
         "1. Read the guidelines (%s) and the candidate list in %s: 28 listed 2020 tracts in five neighborhoods." % (
             W.FILES["guidelines"], W.FILES["neighbourhoods"]),
         "2. Took each listed tract's 2019 to 2023 rate from %s (B17001_002 over B17001_001) and its margin by the "
         "proportion formula (guidelines %s)." % (W.FILES["tract23"], g["sections"]["rate"]),
         "3. For a tract keeping its 2010 code, took its 2014 to 2018 rate and margin from %s the same way." % (
             W.FILES["tract18"]),
         "4. For each tract the 2020 census split, found the 2010 block groups its blocks come from in %s (the first "
         "digit of each 2010 block) and summed their 2014 to 2018 estimates in %s, margins as the root sum of "
         "squares: tract 403.02 %s%%, 303.01 %s%%." % (W.FILES["blockrel"], W.FILES["bg18"], t["403.02"]["r18"],
                                                     t["303.01"]["r18"]),
         "5. Tested each tract (guidelines %s): 2019 to 2023 rate of 20 per cent or more and z over 1.645; counted the "
         "qualifying tracts per neighborhood: %s." % (g["sections"]["tests"], ", ".join(
             "%s %d" % (n, nb[n]["count"]) for n in W.NEIGHBOURHOODS)),
         "6. From %s and %s, took each housing case's status on 31 December 2026 from its event history (a case "
         "closed in 2026 and reopened in 2027 was closed that day), residential land uses from %s through the prior "
         "parcel number for older cases, and days from each case's opening: the open properties and average days "
         "below." % (W.FILES["cases"], W.FILES["events"], W.FILES["parcels"]),
         "7. From both fiscal-year sheets of %s, took checks dated in 2026 that were not reversed, whenever the "
         "reversal was posted, so a reissue dated in 2026 counts and a 2026 check voided in 2027 does not: the dollars "
         "and properties below." % W.FILES["payments"],
         "8. Recommended the neighborhoods with three or more qualifying tracts: %s." % " and ".join(rec),
         "",
         "## 4. Deliverable Answers", "",
         "### %s" % W.GOLDEN["workbook"], "",
         "1. Each listed tract, 2014 to 2018 rate and margin, 2019 to 2023 rate and margin, in per cent, and whether "
         "it meets both tests:"]
    for r in rows:
        L.append("   - %s %s: %s ± %s; %s ± %s; %s" % (r["nbhd"], r["tract"], r["r18"], r["m18"], r["r23"], r["m23"],
                                                     "qualifies" if r["qual"] else "does not qualify"))
    L.append("2. Each neighborhood, qualifying tracts, residential properties with a housing case open on 31 December "
             "2026, average days open, grant dollars paid in 2026, properties paid:")
    for n in g["nb"]:
        L.append("   - %s: %d; %d; %d; $%s; %d" % (n["nbhd"], n["count"], n["open_props"], n["days"],
                                                 "{:,}".format(n["dollars"]), n["paid_props"]))
    L += ["", "### %s" % W.GOLDEN["memo"], "",
          "1. Recommends %s of five: %s." % (GD.WORDS[len(rec)], " and ".join(rec)),
          "2. Chart of each listed tract's change with its 90 per cent interval, qualifying tracts highlighted, on "
          "pages 1 and 2; the neighborhood table beside it.", ""]
    open(path, "w", encoding="utf-8").write("\n".join(L))
