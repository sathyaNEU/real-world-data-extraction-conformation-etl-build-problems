"""submission.md, drafted from figures.json: the tags, the call, the components, eight steps and the answers by file."""
import figs as FG
import golden as GD


def write(path, fig):
    c = fig["call"]
    order = sorted(c["pressured"], key=lambda w: -c["shares"][w])
    ch = fig["change"]
    pb = fig["pellbury"]
    a, b, d = order
    L = []
    L.append("## Tags\n")
    L.append("> **Domain:** Survey Research & Official Statistics (seasonal adjustment and official time series "
             "production: a ward house price index compiled from the price paid record and the council's building "
             "control register).")
    L.append("> **Analytical objective:** Data Extraction & Conformation (ETL).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Give the 2027-28 pressured-ward uplift to %s (%s), %s (%s) and %s (%s).** Their Ward House Price "
             "Index rose %.1f, %.1f and %.1f per cent from 2025 to 2026, over the 5.0 per cent line, and no other "
             "ward's did. Not Pellbury, whose index rises %.1f per cent on every pair of its sales but %.1f per cent "
             "once the pairs whose dwelling had building work completed between its two sales are set aside.\n"
             % (a, c["shares_text"][a], b, c["shares_text"][b], d, c["shares_text"][d], ch[a], ch[b], ch[d],
                pb["every_pair"], pb["golden"]))
    L.append("## 2. Critical Components\n")
    L.append("1. %s's, %s's and %s's index rose **%.1f%%**, **%.1f%%** and **%.1f%%** from 2025 to 2026."
             % (a, b, d, ch[a], ch[b], ch[d]))
    L.append("2. Pellbury's index rose **%.1f%%** with the pairs spanning completed building work set aside, against "
             "**%.1f%%** on every pair." % (pb["golden"], pb["every_pair"]))
    L.append("3. The pressured wards have **%d**, **%d** and **%d** homes due to start on site in 2027-28, **%d** in all.\n"
             % (c["homes"][a], c["homes"][b], c["homes"][d], c["homes_total"]))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Read pp-harrowmere-2015-2025.csv and pp-harrowmere-2026.csv and applied pp-monthly-update-2027-01.csv "
             "by transaction identifier: A and C rows stand as published, D rows withdraw the entry.")
    L.append("2. Kept standard (category A) entries for property types D, S, T and F and paired each address's "
             "consecutive sales (PAON, SAON, street and postcode), per section 3 of "
             "hvha_ward_house_price_index_methodology.pdf.")
    L.append("3. Read both sheets of hcc_building_control_completions_2015-2026.xlsx to house number or name, flat and "
             "postcode, and set aside every pair whose dwelling has a completion certificate dated between its two "
             "sales, the dwelling being of a different quality at the second sale: Pellbury keeps %d of its %d pairs "
             "ending in 2026." % (pb["pairs_2026_kept"], pb["pairs_2026_every"]))
    L.append("4. Placed each pair in its May 2023 ward by postcode (wd23cd in harrowmere_postcode_directory_2026-11.csv), "
             "fitted each ward's index by ordinary least squares on the year indicators and took the 2025 to 2026 "
             "change: %s %.1f, %s %.1f, %s %.1f, every other ward under 5.0 (Pellbury %.1f)."
             % (a, ch[a], b, ch[b], d, ch[d], pb["golden"]))
    L.append("5. Ask A: register rows certified in 2026, dwellings created less dwellings lost, each application once "
             "(a partial completion and its completion certificate carry the same dwellings), in the ward of the "
             "site postcode's wd23cd, since the register's Ward column holds the 2019 wards: %d in all."
             % fig["ask_a_total"])
    L.append("6. Ask B: category B entries for dwellings transferred in 2026, after the update; a portfolio "
             "transfer's price stands on each of its titles, so a price on three or more entries of one day is "
             "counted once: %d entries, GBP {:,} in all.".format(fig["ask_b_money_total"]) % fig["ask_b_count_total"])
    L.append("7. Ask C: start-on-site claims in hvha_start_on_site_claims_2025-2027.csv dated 2026 and Paid or Approved, "
             "each start once (Calderstone's claims for the starts Brackwell Homes was paid for before the merger "
             "repeat the postcode, start date and homes): %d homes in all." % fig["ask_c_total"])
    L.append("8. Shared the GBP 12,000,000 among the three in proportion to homes in Approved or In contract schemes "
             "due to start from 1 April 2027 to 31 March 2028 in hvha_affordable_pipeline_2027-28.xlsx, per section 3 "
             "of the programme rules: %s %s, %s %s and %s %s.\n"
             % (a, c["shares_text"][a], b, c["shares_text"][b], d, c["shares_text"][d]))
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % GD.PDF)
    L.append("1. Pressured wards for 2027-28: %s, %s and %s." % (a, b, d))
    L.append("2. Shares of the GBP 12,000,000 uplift: %s %s; %s %s; %s %s."
             % (a, c["shares_text"][a], b, c["shares_text"][b], d, c["shares_text"][d]))
    L.append("3. Chart on page 1: every ward's 2025 to 2026 index change as a bar, the 5.0 per cent line marked and "
             "the three pressured wards highlighted.\n")
    L.append("### %s\n" % GD.XLSX)
    L.append("1. Index change 2025 to 2026, per cent to one decimal:")
    for w in FG.WARDS:
        L.append("   - %s: %.1f" % (w, ch[w]))
    L.append("2. Share of the uplift, nearest pound:")
    for w in FG.WARDS:
        L.append("   - %s: %s" % (w, c["shares_text"][w] if w in c["pressured"] else "GBP 0"))
    L.append("3. Net additional dwellings from building work completed in 2026 (May 2023 wards):")
    for w in FG.WARDS:
        L.append("   - %s: %d" % (w, fig["ask_a"][w]))
    L.append("4. Additional price paid entries for dwellings transferred in 2026, count and money paid to the nearest pound:")
    for w in FG.WARDS:
        L.append("   - %s: %d entries, %s" % (w, fig["ask_b_count"][w], fig["ask_b_money_text"][w]))
    L.append("5. Affordable homes started on site in 2026:")
    for w in FG.WARDS:
        L.append("   - %s: %d" % (w, fig["ask_c"][w]))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
