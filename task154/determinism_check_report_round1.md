# Verdict: task154 (June quarter 2026 GDP advance estimate)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed and no rerun. Two residual soft spots are listed under Evidence and Fix; neither changes a golden figure.

**Why:** Every committed answer reproduces from the shipped files. The main call is 0.691% on the quarter, which is 2.793% annualised, so 2.8%. Every inventory valuation that the out-of-sample back-test supports lands inside 2.75 to 2.85. The valuations are the stockholding-period deflation with fractional months, with rounded months, and a cost-of-sales FIFO version. The naive routes are worse on the back-test and give different calls: month-end index 2.2%, quarter-average index 3.3%, two months for every industry 3.1%. The revisions table and the coal/LNG table (supplementary questions 1 to 3) also reproduce exactly. The weakest link is the "shipped" timing basis in the coal/LNG table (see Evidence).

## Literal reading first
- Prompt as written: the call, an annualised GDP growth to 1 decimal, plus two tables.
- Annualisation is filed in so_gdp_user_guide_2026.pdf: ((1+q/100)^4-1)*100, with the headline taken from unrounded estimates.
- Contributions are each component's change over the previous quarter's GDP, with imports negative. This is filed in the user guide.
- Where the text is silent:
  1. How to value business stocks at 2025 prices. The guide says only "producer price indexes, inputs to each industry". The period of the index is silent.
  2. What "latest estimate" means. It could be the 25 June real-time database release or the 21 July annual accounts.
  3. Whether "shipped" means customs-entry month or loading month.
- Each silence is addressed below.

## Evidence (recomputed from the bundle)

| Item | Source | Recomputed | Reproduced |
|---|---|---|---|
| March-quarter GDP base | tarbert_gdp_tracker_2026q2.xlsx, so_annual_national_accounts_2025.xlsx Table 3 | 129,210; ten March-quarter lines plus the three TBS lines sum to it | yes |
| Ten non-TBS lines, change | tracker | +84 in total; the tracker's own contributions are correct | yes |
| Goods exports at 2025 prices | TBS PDF Table 1 (SA, Apr to Jun) / so_price_indexes Export prices rebased to 2025 | 30,881.1 against 30,021 (March quarter, which the Table 3 level matches exactly) | yes (+0.67 pp) |
| Goods imports at 2025 prices | TBS PDF Table 2 / Import prices | 27,116.3 against 27,618 (matches Table 3 exactly) | yes (+0.39 pp) |
| Inventory change, stockholding-period method | TBS PDF Tables 5 and 7, PPI inputs rebased to 2025 | -18.9 (fractional months), so -19; March quarter reproduces at 532.8 against 534 published | yes |
| Contribution of the inventory line | (-19 - 534) / 129,210 | -0.428, so -0.43 | yes |
| Quarterly growth | sum of 13 contributions | 0.691%, annualised 2.793%, so 2.8 | yes |
| Back-test RMS, 28 quarters 2019Q2 to 2026Q1, against CIPI_NF in so_realtime_gdp_database.csv release 2026Q1-T | portal stocks and ratios | fractional 9.86 (golden says 9.9); rounded months 9.39; FIFO on cost of sales 9.95; month-end 62.5; two months 61.4; quarter average 125.9; ceiling 37.9; output PPI about 88 | yes |

### Competing answers on the main call

| Valuation | Annualised call |
|---|---|
| Month-end index | 2.18 |
| Quarter-average index | 3.30 |
| Two months for every industry | 3.08 |
| Ceiling of ratio months | 3.05 |
| Floor of ratio months | 2.47 |
| Output PPI | about 3.28 |
| **Back-test-valid family (all round to 2.8)** | 2.761 (rounded months), 2.793 (fractional), 2.805 (FIFO) |

- Only the back-test-valid family is separated by the shipped history.
- The closest margin to a rounding line is 2.761 against 2.75 for the rounded-months variant. This variant is also valid and rounds to 2.8, so no live fork results.

### Supplementary answers

| Answer | Result | Reproduced |
|---|---|---|
| Revisions table: Sep 2025 / Dec 2025 / Mar 2026 | +0.50 / +0.575 / +1.22, so +0.5 / +0.6 / +1.2 | yes |
| Mean revision, mean absolute revision (12 quarters) | 0.3376 and 0.5807, so 0.34 and 0.58 | yes |
| Coal and LNG, 10 country cells plus totals | all reproduce to 0.1 under the shipped-basis reading (coal +325.5, LNG +1,466.8) | yes |

- Revisions method: advance growth uses the "-A" release's own levels, and latest growth uses the annual-accounts Table 3 series.
- "Latest estimate": the 21 July annual accounts postdate the 25 June database. They restate exactly the twelve quarters from June 2023 that the prompt names. Pinned.
  - Fork, for the record: using the 25 June database as "latest" gives Mar 2026 +0.58 and mean revision +0.08. It is an inferior reading because the annual accounts are later and cover the named window.
- Coal/LNG sources: SITC divisions 32 and 34 exports by country from the bulk CSV, in $000, for April and May 2026 and June 2025 to July 2025. June 2026 comes from TBS PDF Table 4, because the CSV ends in May.
- **Soft spot (supplementary question 3):** the golden holds only on a loading-month basis. The TBS entry month trails the Harbours Board loadings by exactly one month through December 2025.
  - Evidence: ratio of TBS tonnes to previous-month loadings is about 1.00 every month to December 2025, and about 1.00 against same-month loadings from January 2026. TBS December 2025 is doubled (LNG 4.13 Mt, coal 15.0 Mt).
  - The PDF adds only "From the January 2026 month the statistics are compiled on TBS's new processing system". No shipped text states the lag.
  - So the Q2 2025 comparison is May to July 2025 entries, and Q2 2026 is April to June.
  - Entry-month reading: April to June 2025 gives Japan coal +205.7, coal total +393.0, LNG total +902.3.
  - The prompt's word "shipped" together with the Harbours Board loadings file separates the two readings. The ask is also outside the main call's decisive step. I treat it as pinned but the weakest link.
- No other column, unit or key trap was found. The June 2026 coal and LNG kt in Table 4 agree with Harbours Board loadings. Unit prices are identical across countries within a month.

### Decisive facts located
- Stock-to-sales ratios, stocks and the revised April and May figures are in TBS PDF Tables 5 and 7.
- The industry input price index is in so_price_indexes_2026-06.xlsx, sheet "PPI inputs".
- The 2025 prices rebasing rule is in the user guide ("quarters of 2026 are at 2025 prices"; "Sources and price measures").
- The Office's own history of non-farm inventories for validating the method is in so_realtime_gdp_database.csv.
- The stockholding-period method itself is not filed. It is found by back-test, which the shipped history allows. This is a method-selection step, and the data separate the candidates by a factor of at least 3.7 in RMS.

## Files/Hygiene
**PASS.**
- 15 files in 5 formats: csv (9), xlsx (3), pdf (2), json (1), txt (1).
- Largest file: 72,129 rows (partner SITC CSV), above the 25,000-row floor.
- Provenance is clean: no authoring or benchmark language, no tool banners, and PDF and xlsx metadata name the fictional agencies. Dates are temporally coherent: poll 23 July, notice 24 July, tracker 08:00 28 July before the 28 July bulletin, annual accounts 21 July, price indexes 16 July.
- Distractors: Harbourline poll (median 2.4), industry_federation_business_conditions (not used in the solution); tarbert_econ_data_index.csv is a desk catalogue and is not an answer source.
- Layer 1 mess is authentic: PDF-only June bulletin, revised April and May, the Dec 2025 doubled period and system change, reference-year rebasing, 2019-based NSA indexes against SA values, $000 against $m.
- Minor note: tarbert_econ_data_index.csv reads slightly like a manifest because it carries terms and received columns, and some "covers" cells are blank. Cosmetic and non-stump.
- Nothing is exclusion-level.

## Stump power (Gate F)
- The trap is how business stocks are deflated, so the inventory line swings from -214 to +141 million dollars and the call from 2.2 to 3.3.
- Easy routes a strong model might file: month-end PPI (2.2), quarter-average PPI (3.3), or the poll median (2.4).
- Winning requires proposing that each industry's stock be priced over its own stock-to-sales months, then confirming it against the Office's non-farm inventory history, where RMS falls from 62 to under 10.
- Strong models that never back-test the deflator will miss. I judge stump power moderate to good. It is not too easy: the guide says only "input prices" and no shipped text mentions stockholding periods.
- The ten tracker lines and the poll are honest, with no wrong reported number to catch.

## Stumping type (Gate G)
`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.

The difficulty is choosing the valuation of stocks by out-of-sample validation. No reported figure is wrong. On perfectly clean data the task still stumps, because the deflator remains to be chosen.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.

- **Domain:** national-accounts nowcasting of expenditure GDP, with chain volumes, inventory valuation and contribution to growth. The swap test fails to transplant it, because nothing in the decisive quantity survives swapping in another field's nouns.
- **Layer 1:** TBS PDF outage and revised months, the January 2026 system change, SA stocks against NSA indexes, and rebasing from 2019 to 2025.
- **Layer 2:** value stocks over their holding period and validate against the Office's own inventory history.
- **Easy route and its answer:** a strong analyst who cleaned everything and read every rule would still deflate with a month-end or quarter index and file 2.2% or 3.3%.

## Fix
none. Two optional notes for the author, neither required:
- The shipped-basis timing for supplementary question 3 rests on the Harbours Board comparison and the word "shipped". If a prior run split on entry-month against loading-month, that is where.
- Keep the rounded-months variant in mind for the determinism record: it gives 2.761, which still rounds to 2.8.
