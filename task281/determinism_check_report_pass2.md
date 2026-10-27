# determinism-check report, task281, 2026-10-27

## Verdict
DETERMINISTIC

**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
This is the re-judge licensed by `/fix-determinism` after the rebuild that closed the portal's SF16/SF17/SF18 finding (the unit an overtime piece was worked at, and the aides' comp-time credit). One isolated judge thread (sonnet, medium, single pass, run `pass2`) worked from a fresh unzip of `target.zip`, `prompt.txt`, and the submission's five graded blocks only. It wrote its own full derivation (`/tmp/determinism-check-task281-pass2/my_derivation.md`) **before** opening the committed-answer block, confirmed as "Order kept: yes" at the top of its verdict.

It independently rebuilt the decisive chain from the raw files, not the solution text: Budget Instruction 2024-07 2.4 drops FY2026's own 11,968 vacant-line-shift hours (separations) from the FY2028 need; 2.3(b) adds the position control's 14 lines vacant on 1 July 2027 by each one's `first_shift_on_post` date; and 3.3's "hours its holder will work" is forced onto the July 2025 entry classes' own first-year absence rate (the memo's named recruiting source for the new positions), not the unit's blended incumbent. That chain reproduced the committed complement bit-for-bit (ACF 8, FFH 7, HRC 9, KPG 6, OXG 10, PCN 6, PCS 6, TWC 7 = 59 of 60) and reproduced all eight FY2026 overtime-hours figures (ask 2) exactly, including the SL-0410/Thornmere cost-center resolution the prior portal round flagged. Ask 3 (headcount) landed within 1 in 7 of 8 units, fully explained by the one rehire-dedup join named in solution step 6 that the thread did not implement; no contradiction. Ask 4 was traced to specific files but not independently re-derived at person-level granularity given scale; nothing contradicts it.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Complement by unit (ask 1) | 9,8,7,6,6,7,10,6 = 59 of 60 | identical | yes |
| FY2026 OT hours by unit (ask 2) | 7,984 / 8,144 / 6,824 / 7,616 / 5,320 / 9,216 / 5,502 / 5,019 | identical, all 8 | yes |
| People with OT by unit (ask 3) | 66/66/62/44/44/23/38/39 | within 1 in 7 of 8 (one rehire-dedup join not implemented); ACF exact (66=66) | yes, with named gap explained |
| People over 600h by title (ask 4) | CO 13, PCO 6, FSA 7, HMW 2 | traced to files (title_effective_from/to), not independently re-derived at person level | not re-derived; no contradiction found |
| Entry-class off-post rate (critical component 3) | 7.8% (classes) vs 14.5% (units' holders) | reproduced (≈7–8% by unit vs ≈12–19% blended, averaging to the filed figures) | yes |
| Fifth-heaviest week hours by unit | HRC 304 / ACF 280 / TWC 232 / PCN 192 / PCS 200 / FFH 232 / OXG 344 / KPG 208 | consistent with the thread's independent weekly rebuild | yes |

## Competing answers that survived
None. The thread built and rejected the full ladder on the files themselves: 38 (annual-mean relief factor, superseded by the standard), 62 (FY2026's own vacant lines kept in, contradicted by 2.4), 63/64 (relief rated at the unit's or title's blended incumbent, contradicted by the memo's named recruiting cohort plus 3.3). Every fork the thread could construct closed on a shipped fact (2.4, 3.3, 3.4, the memo's sentence); none survived as a defensible alternative for the main call or for asks 1–2. Ask 3's small per-unit gap is explained, not an open fork (it is the thread's own incomplete implementation of a named join, not an ambiguity in the task).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 15 | yes |
| Format mix | 3 or more formats | csv, pdf, xlsx (3) | yes |
| Large file | one file 25,000+ rows or large DB | `merrimont_shift_rosters_fy2026.csv`, 44,115 rows | yes |
| Distractors named | metadata.json names 2+, no filename labels one | 4 named (`doc_average_daily_population_fy2026.csv`, `msp_communications_call_volume_fy2026.csv`, `sha_winter_operations_log_fy2026.csv`, `overtime_expenditure_by_program_fy2026.xlsx`); none of the four filenames announces itself as a distractor | yes |
| Distractor relevance / arithmetic lure | each distractor unused yet relevant; at least one reproduces a graded quantity arithmetically before a shipped fact rules it out | design note states the Comptroller's overtime-by-program table (and the other three) "ties to nothing in the pack" and is "none read by the placement or the asks"; plausible and on-topic, but none of the four is shown to arithmetically coincide with a graded figure before being ruled out | partial |
| Deliverables | 1–3, all present in golden, no format family forced | 2 (`fy2028_relief_positions_by_unit.xlsx`, `fy2028_weekly_backfill_need.png`), both present under `golden/` | yes |
| Asks multi-dimensional, unit/rounding stated | yes | prompt states "hours to the nearest hour"; asks run over 8 units x 4 sub-questions plus a 4-way title breakdown, each multi-dimensional | yes |
| Prompt shape identifiable, rubric ≥25 criteria | yes | design note names Shape 14 (cuts of a distribution); the rubric itself is portal-generated and not shipped in the task folder, so the ≥25-criteria count could not be verified from local files (not locally verifiable) | n/a (not locally checkable) |
| Not LLM-generated; goldens read as real work product | yes | judge found two timekeeping systems, split pay periods, retro pay, a rehire split across employee IDs, mismatched cost-center codes (genuine operational mess, not planted); no provenance/LLM-authorship tells | yes |

## Gate G reconciliation
The thread classifies `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`. The design note's draw step (§`## Draw`, point 1) logged the intended Gate G label at draw time as `forecasting` ("Gate G `forecasting`: the correctly read FY2026 does not pin FY2028's need"), while the note's own Layer 2 line names the mechanism `estimand_identification` / `own:forward-week-distribution-cut`, picking the right comparison cohort to estimate a not-yet-observed population's availability. This is a label mismatch at the edges (forecasting vs. method/model selection), not a substantive one: both are FINE-numbers, non-rejection shapes under Gate G, and the card's own mechanism description (choosing which cohort's empirical rate stands in for a relief holder's hours) reads as a comparison-cohort/estimand choice at least as much as a trend extrapolation. The thread did not name either of the card's two declared distractor-adjacent artifacts (the Comptroller's overtime table, the superseded annual relief factor) as the surface read carrying the task, and did not treat any reported figure as something to catch-and-reject; `surface_read_dependency: no` is consistent with the design note's "No decoy" and "No certified replay" lines (no planted figure states the need, availability or complement). No finding here predicts a send-back; the terminology gap between "forecasting" and "method_or_model_selection" is noted for the card but does not change the Gate G disposition.

## Gate H reconciliation
Thread: `domain: pass`, `layers: pass`, `decisive_step: analytical`. It names H1 via the swap test (a real civil-service relief-complement sizing method that cannot be renamed into another field's nouns without destroying the mechanics), H2 via the two timekeeping systems/comp-time/retro-pay/rehire mess (Layer 1) against the comparison-cohort choice (Layer 2), and H3 via the easy-route test: a strong analyst who executes every clause correctly but models "the holder" as the unit's typical/blended incumbent (the natural default, since that is who appears in the FY2026 roster) still lands on 62–63, not 59.

This matches the design note's `## Three rules` block point for point: the same domain test (an order statistic of a rebuilt weekly distribution set against a cohort-specific capacity), the same Layer 1/Layer 2 split, and the same analyst test ("a strong analyst who reads every rule... and rates a relief position by title at the title's officers... files 63 positions, three short of the 60"). The design note's "Not semantics" and "Not rule application" lines independently argue the same H3 = analytical conclusion the thread reached from the files alone, with no exposure to the note. No mismatch; no send-back signal from Gate H.

## Stump power (Gate F)
The thread found real stump power: the decisive fork (which absence-rate cohort stands in for "the holder") is not advertised anywhere in the files, and the natural first read of "its holder" (the unit's blended average incumbent, who is who actually appears in the FY2026 roster) is a specific, provably wrong landing (63, three short of 60), not a coin flip. This agrees with the design note's ladder (R2/R2t at 63–64) and the Analyst test's own characterization of the default path. Per the client's library note on textbook domain methods (`stumping` 1.3), the task's own field (civil-service relief-complement sizing) genuinely uses this cohort-substitution method as a standard move, and the thread reached the golden by applying that method with no judgment call the data had to settle beyond picking the right comparison population from a memo sentence, joined against an HR column (`academy_class`) that describes a person, not a relief position. That is a landable analytical call, consistent with a textbook route a strong solver takes in this domain, not a coin-flip or a planted trap.

## Findings, ranked
1. (Low, informational) Design-note terminology drift: the card's draw-time Gate G label is `forecasting`; the final mechanism reads closer to `method_or_model_selection` / comparison-cohort estimand selection. Both are non-banned, FINE-numbers shapes, so this does not affect the verdict or disposition. Recommend updating the card's mechanism label for consistency at the next touch, not urgent.
2. (Low, informational) Spec gate "distractor arithmetic lure" is only partially met: the design note states none of the four named distractors arithmetically ties to a graded quantity before being ruled out ("ties to nothing in the pack"); they are topically plausible but not a live arithmetic trap. This was true before this fix-determinism round as well (not something the rebuild touched) and does not bear on the determinism verdict; noted for completeness only.
3. (None) No Gate A–E, F, G or H finding from this pass. The judge thread kept the required order (own derivation before the committed answers) and reproduced every load-bearing figure it attempted.

## Next action for the author
None required to ship this pass: verdict is DETERMINISTIC, disposition APPROVE, Gate G and Gate H both pass and reconcile cleanly with the design note. If desired, update the card's Gate G mechanism label from `forecasting` to `method_or_model_selection` for internal consistency; this is cosmetic and not a blocking item.
