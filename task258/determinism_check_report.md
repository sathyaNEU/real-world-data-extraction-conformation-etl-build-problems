# determinism-check report, task258, 2026-10-13

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (two optional one-sentence pins, supplementary asks 3 and 4 only)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated thread (sonnet, medium) recomputed the main call and all 24 supplementary figures from a fresh unzip of target.zip (sha256 588bea8c70a22a27...) and reproduced every one. Pantry 6.28 million leads Tideline 4.61 million (1.36x) under every variant run (delay 232 to 247 ms, load-time ratio 0.45 to 0.51, last-rate weighting). Only the two ratio-carrying readings put Ledger first (7.4 and 8.4 million). The charter fixes the estimand and the engagement beacons plus change log show the delay settling at about 240 ms and the load time at about 0.48. Thread hygiene verdict: PASS.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Delay after playbook (median of 11 engagements) | 240 ms | 240 ms (232 to 247) | yes |
| Load-time ratio | 0.48 | 0.480 (0.451 to 0.510) | yes |
| Pantry / Tideline / Matchday / Hearth / Ledger / Trailhead moved (M) | 6.3 / 4.6 / 4.4 / 4.2 / 3.3 / 2.3 | 6.28 / 4.61 / 4.39 / 4.19 / 3.29 / 2.30 | yes |
| Ledger at ratios on both parts / no delay (M) | 7.4 / 8.4 | 7.40 / 8.41 | yes |
| Tideline all slow loads; Hearth own-image slow loads (M) | 26.9; 20.0 | 26.9; 20.0 | yes |
| Egress GB, AUD (Pa/Ti/Ma/He/Le/Tr) | 616,$44 / 1,971,$140 / 1,208,$86 / 2,102,$149 / 1,056,$75 / 667,$47 | 616.0,43.74 / 1,970.9,139.93 / 1,208.2,85.78 / 2,101.9,149.24 / 1,055.8,74.96 / 666.9,47.35 | yes |
| Live hero images (Pa/Ti/Ma/He/Le/Tr) | 3,543 / 6,362 / 4,210 / 2,777 / 2,044 / 2,444 | same | yes |

## Competing answers that survived
- Supplementary 4: DAM `property` column instead of the last_used_page host gives Pantry 3,055, Tideline 6,709, Hearth 3,062, Ledger 1,759, Trailhead 2,097, Matchday 4,698. The runbook and charter 2.4 favour the host reading but no sentence states it. Residual semantic fork, ask 4 only.
- Supplementary 3: status 304 counted as hero requests gives Tideline 2,593 GB and so on. The contract's "bytes delivered" excludes it but no file defines 200 versus 304. Residual semantic fork, ask 3 only.
- Closed forks: reload navigations (charter 2.2 includes them), last-rate weighting (field notes: rate in force at load start), delay at min(own, 240) (call unchanged; the engagement data forces the fixed level), live cutoff (nightly crawl date).
- Neither open fork touches the main call. Asks are exempt from the semantics rule.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 4 (csv, md, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | 157,066 beacons; 118,869 DAM rows; 65,694 engagement beacons | yes |
| Distractors | 2 or more in metadata.json, not labelled by file name | crux_lcp_origins_2026-11.csv, analytics_pageviews_2026-11.csv; names neutral | yes |
| Distractors unused yet weighable | yes | unused by golden; CrUX is the public view, charter names the group's own RUM; neither answers the graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (md, png), both in golden | yes |
| Asks multi-dimensional, unit and rounding stated | yes | six properties across moved loads, GB, AUD, images; rounding stated in prompt | yes |
| Prompt shape and 25 or more criteria | yes | shape 14; 6 properties x 4 figures + call + chart gives 26 or more | yes |
| Reads as real, not LLM generated | yes | thread found operational artifacts, nothing exclusion-level; I did not independently re-read the PNG | yes (thread) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical; stump is the effect model of the image delay (level-reset to 240 ms against proportional or zero). These match. The declared distractors (CrUX, analytics) are not named by the thread as carrying the task; the thread names the ratio carry (Ledger 7.4) as the stump route and the all-slow (Tideline) and own-image (Hearth) routes as easy to avoid. No shipped file ranks the candidates wrongly on the decision question. No mismatch.

Gate H line: domain pass, layers pass, decisive_step analytical. This matches the card's analyst_test and domain_test and the note's Three rules. Layer 2 is transferring a before/after effect from eleven engagements to a different population. Layer 1 is the UTC/Sydney month, effective-dated sampling rates, duplicate beacons, legacy aliases and DAM legacy ids.

## Stump power (Gate F)
Good. Three wrong routes give three different wrong winners: Tideline 26.9 (all slow loads), Hearth 20.0 (own-image slow loads), Ledger 7.4 or 8.4 (ratio or preload). Only the Ledger route is a trap for a careful analyst. The thread notes the first two fall to a reading of charter 2.4, so the stump rests on the third. The asks add independent layers.

## Findings, ranked
1. Ask 4 attribution fork (DAM property column against page host). Low, ask only.
2. Ask 3 status 200 versus 304 fork. Low, ask only.
3. Stump rests on one route (the ratio carry). Observation, no action.

## Next action for the author
Optional: add one sentence to the prompt or deliverable asks that egress counts requests answered with the image (status 200) and that a moved image belongs to the property whose page now uses it. File the WHAT, not the method. Then proceed to ship. If you edit the prompt, the target.zip hash does not change, but re-run the voice check.
