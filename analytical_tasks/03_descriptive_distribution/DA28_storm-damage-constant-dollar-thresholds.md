# DA28 — "More billion-dollar storms than ever": a nominal threshold rises with prices and with what is built

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Any count of events above a fixed money threshold (deals over $1M, incidents costing over $100k, "enterprise" customers by contract size) tracked across years of inflation and growth |
| Domain | Catastrophe risk / insurance |
| Task shape | 03 · Bridge between two totals (count of large-loss episodes in 2014–2023 versus 1996–2005 → bridged by inflation, exposure growth and residual change) |
| Core method | Aggregate events to episodes; convert property damage to constant dollars (CPI-U); normalise for exposure growth (housing units in affected counties); count episodes above the threshold under each adjustment; sequential bridge |
| Analytical stump | Counting episodes above a fixed nominal dollar threshold mechanically increases with inflation and with growth in the value of exposed property. Without constant-dollar conversion and exposure normalisation, trends in counts are mostly price and growth effects. The episode, not the per-county event row, is the loss unit |
| Primary sources | NOAA NCEI Storm Events Database (details files); BLS CPI-U; Census county housing unit estimates |

## 1. The real-world situation

A reinsurer's research team reported that the number of convective storm episodes causing over $250 million in property damage had tripled
between 1996–2005 and 2014–2023 and recommended raising the loading for that peril. The chief risk officer asked how much of the increase
survives adjustment for inflation and for the growth of property in harm's way.

## 2. The decision (one deterministic recommendation)

**The exposure-and-inflation-adjusted change in the count of large-loss convective episodes between the two decades, and whether it exceeds
the memo's +25% threshold for raising the loading.**

Rules (research memo):

* Events: Storm Events details files 1996–2023; event types in the convective group (thunderstorm wind, hail, tornado, flash flood per memo).
* Damage: `DAMAGE_PROPERTY` parsed from strings with K/M/B suffixes; sum across all event rows in an `EPISODE_ID` → episode damage.
* Constant dollars: episode damage × CPI-U(2023) ÷ CPI-U(episode year).
* Exposure normalisation: × (housing units in 2023 ÷ housing units in episode year), summed over the episode's counties, weights per memo (the
  share of the episode's damage in each county).
* Threshold: $250 million.
* Counts per decade: nominal, constant-dollar, constant-dollar + exposure-normalised.
* Bridge: nominal change → inflation effect → exposure effect → residual (adjusted change).
* Raise loading if the adjusted change > +25%.

## 3. Why capable analysts get it wrong

* Nominal counts above a threshold are simple and widely quoted.
* The threshold's real value falls each year; more events cross it with no change in hazard.
* Growing exposure raises damages from the same hazard.
* Event rows split one storm system across counties; episodes are the loss unit.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–28 | `StormEvents_details-ftp_v1.0_d<yyyy>_c<date>.csv.gz` (1996–2023) | CSV | ~50–70k each | NOAA NCEI Storm Events | U.S. Gov public domain | Events, episodes, damage |
| 29 | `Storm-Data-Export-Format.pdf` | PDF | — | NOAA NCEI | Public domain | Field definitions |
| 30 | `cpi_u_annual.csv` | CSV | ~30 | BLS | Public domain | Deflator |
| 31 | `county_housing_units_1996_2023.csv` | CSV | ~90k | Census Bureau intercensal and postcensal estimates | Public domain | Exposure proxy |
| 32 | `convective_event_types.json` | JSON | ~6 | Task author | — | Peril definition |
| 33 | `research_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 34 | `research_team_nominal_counts.xlsx` | XLSX | 2 | Task author | — | Original claim |
| 35 | `damage_string_parsing_tests.json` | JSON | ~20 | Task author | — | Parsing checks |
| 36 | `noaa_billion_dollar_methodology_citation.pdf` | PDF | — | NOAA (cite) | Public domain | Inflation adjustment context |

## 5. Deterministic solution path

1. Parse damage strings; filter event types; aggregate to episodes with county damage shares.
2. Convert to constant dollars; compute exposure factors.
3. Count episodes above threshold under each adjustment per decade.
4. Bridge; loading decision.

## 6. Wrong paths (method errors, not misreadings)

**A — nominal counts.** Inflation and growth counted as hazard.

**B — event rows instead of episodes.** Large storms split and undercounted.

**C — CPI only.** Exposure growth remains.

**D — exposure factor from national totals.** Ignores where storms hit.

## 7. Why the stump is analytical, not semantic

Parsing, aggregation and adjustments are specified. The trap is a moving threshold and exposure in event counts.

## 8. Draft task prompt (prose)

> Has the frequency of large convective loss episodes really tripled? Follow the research memo: aggregate to episodes, adjust for inflation and
> exposure, and bridge the change. Provide `episode_counts.csv` (decade × basis: count), `count_bridge.png` (waterfall from nominal to adjusted
> change), and a one-page `loading_decision.pdf`.

## 9. Deliverables

* `episode_counts.csv`, `count_bridge.png`, `loading_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 2 decades × 3 bases = 6 counts; 3 bridge steps; annual adjusted counts for 10 years; parsing checks; decision.

## 11. Golden-output checklist

* Damage parsing; episode aggregation; CPI conversion; exposure weighting; threshold; bridge; decision.

## 12. Build notes (scope tuning)

* Freeze file creation dates (Storm Events files are revised).
* Confirm the adjusted change is below +25% while the nominal change exceeds +100%.
