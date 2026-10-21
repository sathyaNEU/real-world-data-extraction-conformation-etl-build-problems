"""submission.md from generator/figures.json: every figure the write-up states is emitted from the figures the golden
computed on the shipped pack, never typed."""
import json

TAGS = ("**Domain:** General Statistics & Data Science (data integration, record linkage and entity resolution: an area "
        "agency on aging's provider-area counts of older residents fused from a formally private census release's block "
        "group tables and its exact census-day housing counts, with each provider's FY2026 home-delivered meals and "
        "active clients conformed from the route tablets' log, the agency's case records and the state's death match).  \n"
        "**Analytical objective:** Data Extraction & Conformation (ETL).")


def c(n):
    return "{:,}".format(n)


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    areas = f["areas"]
    a60, a75 = f["age_cuts"]
    k60, k75 = f["counts"]["60"], f["counts"]["75"]
    rt = f["routes"]
    north = "North Kelvane"
    pairs = ", ".join("%s %s and %s" % (a, c(k60[a]), c(k75[a])) for a in areas)
    rural = areas[2:]
    towns = areas[:2]
    above = all(rt["block_sum"][w][a] > f["counts"][w][a] for w in ("60", "75") for a in rural)
    below = all(rt["block_sum"][w][a] < f["counts"][w][a] for w in ("60", "75") for a in towns)
    assert above and below
    lines = ["## Tags", "", TAGS, "",
             "## 1. Final Recommendation", "",
             "**On census day 2020 Kelvane County's provider areas held, aged %d and over and aged %d and over: %s.**  " % (
                 a60, a75, pairs),
             ("Each area takes its block groups' published counts, with the %d block groups the 2023 boundaries cut split "
              "by their blocks' census-day housing units. Not the sum of each area's published block counts, which gives "
              "%s %s aged %d and over and puts all eight rural counts above these and all four town counts below them, because "
              "the "
              "release forced its noise-infused block counts to be non-negative and to add up to their block group, which "
              "moves residents from the dense town blocks into the sparse rural blocks of the cut groups. Not the cut "
              "groups split by the county's 2026 address points or by the blocks' published population, which carry the "
              "same drift (%s %s and %s), nor whole tracts split by housing units, which overrides the block groups' own "
              "counts (%s %s)." % (
                  f["n_cut"], north, c(rt["block_sum"]["60"][north]), a60, north, c(rt["bg_points"]["60"][north]),
                  c(rt["bg_pop"]["60"][north]), north, c(rt["tract_hu"]["60"][north]))),
             "",
             "## 2. Critical Components", "",
             "1. The provider areas as drawn since 1 July 2023 cut **%d** of the county's **%d** block groups; the other "
             "**%d** lie wholly inside one area." % (f["n_cut"], f["n_bg"], f["n_whole"]),
             "2. The %d cut block groups publish **%s** residents aged %d and over and **%s** aged %d and over; split by "
             "their blocks' census-day housing units, about **%s** and **%s** fall on the rural areas' side of the "
             "boundaries, where the published blocks hold **%s** and **%s**." % (
                 f["n_cut"], c(f["cut_60"]), a60, c(f["cut_75"]), a75, c(f["cut_rural_60"]),
                 c(f["cut_rural_75"]), c(f["cut_rural_blocks_60"]), c(f["cut_rural_blocks_75"])),
             "",
             "## 3. Step-by-Step Solution", "",
             "1. Took each block's provider area from provider_area_blocks.csv, the row with no EFFECTIVE_TO, reading "
             "TRACT_BLOCK as the block's ten-digit tract and block code: %d block groups have blocks in two areas." % f["n_cut"],
             "2. Summed each block group's residents aged %d and over (P12_018N to P12_025N and P12_042N to P12_049N) and "
             "aged %d and over (P12_023N to P12_025N and P12_047N to P12_049N) in dhc2020_kelvane_block_groups_p12.csv." % (
                 a60, a75),
             "3. Gave each of the %d whole block groups' counts to its area." % f["n_whole"],
             "4. Split each cut block group's counts between its two areas in proportion to its blocks' H1_001N in "
             "dhc2020_kelvane_blocks_h1.csv: about %s aged %d and over and %s aged %d and over to the rural sides, to "
             "the nearest ten." % (c(f["cut_rural_60"]), a60, c(f["cut_rural_75"]), a75),
             "5. Added each area's parts, which together equal the county's %s and %s in "
             "dhc2020_kelvane_county_tracts_p12.csv, and rounded each area's count once to the nearest ten (%s %s aged "
             "%d and over)." % (c(f["county"]["60"]), c(f["county"]["75"]), north, c(k60[north]), a60),
             "6. Meals: counted each client's rows in hdm_route_delivery_log_fy2026.csv once per delivery_date and "
             "item_code, a HOT code up to the client's meals_per_day in hdm_client_roster_2026-10-09.csv, valued each "
             "at its meals in hdm_item_codes.csv and placed it under the provider of the area of the client's "
             "home_block, whichever route carried it: %s meals." % c(f["meals_total"]),
             "7. Active clients: kept the clients with an episode in hdm_service_episodes_2026-10-09.csv open on 30 "
             "September 2026, dropped those state_death_match_runs_2025-07_to_2026-10.csv shows died on or before that "
             "day under their state_participant_id or a prior_participant_id that state_registry_number_links.csv "
             "links to it, and counted the rest under the provider of their home_block's area: %s clients." % c(
                 f["active_total"]),
             "8. Wrote kelvane_provider_area_counts.xlsx.",
             "",
             "## 4. Deliverable Answers", "",
             "### kelvane_provider_area_counts.xlsx", "",
             "1. Residents aged %d and over on census day 2020, to the nearest ten:" % a60]
    lines += ["   - %s: %s" % (a, c(k60[a])) for a in areas]
    lines += ["2. Residents aged %d and over on census day 2020, to the nearest ten:" % a75]
    lines += ["   - %s: %s" % (a, c(k75[a])) for a in areas]
    lines += ["3. Home-delivered meals served from October 2025 through September 2026, by provider:"]
    lines += ["   - %s (%s): %s" % (f["providers"][a][1], a, c(f["meals"][a])) for a in areas]
    lines += ["4. Active home-delivered meal clients on 30 September 2026, by provider:"]
    lines += ["   - %s (%s): %s" % (f["providers"][a][1], a, c(f["active"][a])) for a in areas]
    text = "\n".join(lines) + "\n"
    assert "—" not in text and "–" not in text
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)
