# determinism-check report, task268, 2026-10-18

## Verdict
NOT_DETERMINISTIC (supplementary asks only: ask 1 people-present cells and ask 3 dark-store counts). SOLUTION_WRONG also applies to the ask-1 people-present cells, under the codebook-literal reading. The main recommendation (Tessavon), the densities, the dense-tract shares, the unit counts and the median rents are forced and reproduce.
**Disposition:** SEND_BACK. By the judge's table a NOT_DETERMINISTIC verdict that needs a fork closed in the prompt is SEND_BACK. The build is pre-ship, so the rerun cost is nil in practice, and the fix is confined to the asks.
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Tessavon (28,805 vs Corrisford 21,709 per km2) holds under every reading tried. Two graded cells are not forced by the shipped text.
1. The golden people-present figures (Tessavon 417,000, Quillmere 251,000, Ashcombe 371,000) reproduce only if a core resident whose workplace is in a micropolitan county, or in a county absent from the delineation list (8,755 flow rows in all), is typed HOMEREL 3. wls_puf_codebook_2025-26.pdf defines HOMEREL 4 as a usual workplace outside any MSA. Read literally, the figures are 416,000, 250,000 and 370,000. (answer_contradicts_files)
2. Ask 3 depends on a rule that no shipped file or prompt states: a shop listed by both brands at the same address and unit is neither brand's dark store. The prompt asks only for stores "delivering from". Counting those 18 pairs changes cells, for example Ashcombe 3/3, Corrisford 7/3, Tessavon 5/4. (underspecified_objective)
Gates C and E fail for asks 1 and 3.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| All other services share, HOMEREL 1/2/3 | 74.2 / 44.1 / 11.7 | 74.15 / 44.11 / 11.72 | yes |
| Trade-Transport-Utilities share, HOMEREL 3 | 34.9 | 34.90 | yes |
| Density Tessavon / Corrisford / Quillmere / Halberdine / Dunnaway / Ashcombe | 28,800 / 21,700 / 18,800 / 18,400 / 15,500 / 15,100 | 28,805 / 21,709 / 18,820 / 18,411 / 15,482 / 15,052 | yes |
| Dense-tract share, same order | 43 / 47 / 42 / 37 / 31 / 2 | 42.8 / 47.4 / 41.8 / 37.4 / 31.3 / 2.2 | yes |
| Lead over runner-up | 7,100 | 7,096 | yes |
| Wrong routes: Corrisford (one share per group), Halberdine (every job counts) | named in the recommendation | Corrisford 31,599 vs Tessavon 22,832; Halberdine 55,822 | yes |
| Units available 30 Sep (A, C, D, H, Q, T) | 7, 5, 5, 7, 9, 11 | identical | yes |
| Median rent per m2 per year | 361, 312, 236, 334, 296, 409 | 361.0, 312.0, 236.4, 334.1, 296.0, 409.0 | yes |
| Dark stores Tilldash; Hopcrate | A 2;2 C 5;1 D 2;0 H 4;2 Q 5;4 T 4;3 | identical, only if co-listed pairs are dropped | yes, with an unfiled rule |
| People present (A, C, D, H, Q, T), thousands | 371, 313, 330, 265, 251, 417 | codebook-literal HOMEREL 4: 370, 313, 330, 265, 250, 416 | no for A, Q, T |

## Competing answers that survived
1. Non-MSA workplace typing (ask 1 people present). HOMEREL 3, the golden: Tessavon 417,000, Quillmere 251,000, Ashcombe 371,000. HOMEREL 4, the codebook-literal reading: 416,000, 250,000, 370,000. A mixed reading (micropolitan as 4, unlisted as 3) gives Tessavon 416,000. The delineation file lists only "candidate areas and neighbours", so for unlisted counties the files cannot show whether they sit in another MSA. No shipped rule closes the fork, and the design note's SF16 covers survey respondents, not flows.
2. Co-listed shops (ask 3). The golden drops the 18 same-address, same-unit pairs for both brands. Counting them gives Ashcombe 3/3, Corrisford 7/3 and Tessavon 5/4. The rule meant to close it is in the design note only; no shipped file closes it.
3. Minor, not graded. The recommendation prose calls the Trade, Transportation and Utilities group "port and logistics", although the group also holds retail trade (NAICS 44-45). DAYS_PREM/5 against excluding not-working days moves the lead (7,096 vs 7,647); the five-weekday denominator is the literal reading and is treated as closed.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, xlsx, pdf, txt (4) | yes |
| Large file | one of 25,000 or more rows | commuting main part, 129,954 rows | yes |
| Distractors | two or more in metadata.json, none labelled by file name | acs5_2022_b08301_counties, cbp_2022_county_sectors, trenstead_expansion_log; the names do not label them | yes |
| Distractor behaviour | unused by the solution, relevant enough to weigh, ruled out by a shipped fact | not stress-tested by the thread beyond its note that nothing answers a graded quantity; the design note says none does | yes, not tested further |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, pptx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 6 cores by several measures, rounding in the prompt | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | shape 14 (cuts of a distribution); the generated rubric is not in the folder, so the criterion count is not verified (about 30 figures plus the call) | unverified |
| Not LLM-reading, goldens realistic | required | thread found no authoring language; golden realism not re-read | yes, thread-level |
| Determinism of asks | Gates C and E | asks 1 and 3 fail | NO |

## Gate G reconciliation
The thread classified the stump as mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no and sole_data_defect no.
- Design note (read after the thread returned): Gate G is `method_or_model_selection` (strata of a synthetic estimator), decisive generator G14, strategy `composition_mix`.
- Reconciliation: consistent. The method-selection family is a FINE-numbers shape and passes. The declared distractors (b08301 work-from-home, CBP, Trenstead log) are not named by the thread as the surface read carrying the task. The easy routes it names, the pooled industry share (Corrisford) and every job present (Halberdine), come from the design's own ladder rather than from a shipped wrong ranking.
- Gate G classification: pass, nothing banned. No shipped artifact ranks the candidates wrongly.

## Gate H
domain: pass, layers: pass, decisive_step: analytical.
- The deciding quantity is a small-area synthetic estimate carrying a survey attendance rate onto commuting flows within industry-by-residence strata.
- Layer 1 is the split main and auxiliary commuting files, GEO_ID and GEOID prefixes, delineation typing, listings in mixed rent bases and locator scrapes. Layer 2 is the choice of strata.
- The swap test fails to preserve the task, so the domain is used.
- The analyst test holds: a strong analyst who reads every field correctly still lands on Corrisford by carrying one share per group.
- Caveat on "not rule application": the typing of non-MSA workplaces is a convention that decides ask-1 cells. That is an ask, which is free of rule 3, but it is still an unclosed fork.

## Stump power (Gate F)
Moderate. The pooled-share route to Corrisford is natural, but the HOMEREL variable and the delineation file point to the stratified one, and the data separate them, so many strong runs will find it. The asks add real difficulty: the 30 Sep date edge with 1 Oct leases and listings, whole-floor rollups, /MO to per-m2-year conversion, delivery versus pickup, and co-listed units. The leak reader's cold run (context from the coordinator, not a verdict input) committed the golden call and every core density, which fits "many strong runs will find it". The asks, not the call, carry the stump against that reader, so closing forks 1 and 2 by filing the WHAT is the right lever and should not file the HOW.

## Findings, ranked
1. Ask 3 (12 cells): the co-listed-shop exclusion is unfiled. underspecified_objective.
2. Ask 1 people present (the A, Q and T cells): non-MSA workplace typing contradicts the codebook, or is unfiled. answer_contradicts_files.
3. Minor: "port and logistics" prose in the recommendation overstates the Trade-Transport-Utilities group.
4. Rubric criterion count is unverified in the folder.
Files and hygiene: PASS, nothing exclusion-level.

## Next action for the author
In the generator, either restate the ask-1 people-present golden to the codebook-literal reading (Tessavon 416,000, Quillmere 250,000, Ashcombe 370,000) or file in the prompt or the codebook how a workplace outside the six MSAs is typed. File the ask-3 population as WHAT, for example "not counting a unit both finders list", without filing the method. Keep the call, densities, shares, rents and unit counts frozen. Then rebuild twice byte-identically and re-judge once.
