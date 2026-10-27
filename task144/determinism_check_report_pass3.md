# determinism-check report (pass 3, narrow re-judge of Ask A and Ask B), task144, 2026-10-27

Pack judged: target.zip sha256 b370e2a4ca35f5fdac5c7319909765c6c4e8109f2855d3fcb33d4055eb057292. Scratch: /tmp/determinism-check-task144-r3/ (verdict.md, scripts/). The round 2 report (determinism_check_report.md) keeps the full main-call recomputation; this pass spot-checked the main call only.

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting / method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no (main call, carried from the round 2 read; the thread did not re-derive it)

## Why
All eleven Ask A and Ask B figures reproduce to the digit from the bundle by an independent implementation. Every variant that moves a figure is closed by the prompt wording ("delivered", "people", "when they did"), by a shipped file (the rename log, the account merges, the signed-in email hash), or by the data's own bimodal structure (gateway fetches). The main call's external star counts (kilnkit 1,523, slidewell 4,175, tracewire 4,534, and the other four) reproduce. The 12,000 / 9,000 and the other six totals were not re-derived.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Apr bryis | 6,699; 1.71% | 6,699 of 391,299 | yes |
| May awesome-home-automation | 7,031; 1.76% | 7,031 of 399,160 | yes |
| Jun zig-toml | 7,169; 1.76% | 7,169 of 406,891 | yes |
| Jul orvum | 7,395; 1.72% | 7,395 of 429,444 | yes |
| Aug minio-exporter | 7,090; 1.65% | 7,090 of 429,291 | yes |
| Sep rust-ratelimit | 7,317; 1.70% | 7,317 of 429,949 | yes |
| kilnkit outside nominators | 22; 81.48% | 22 / 27 | yes |
| tracewire | 43; 91.49% | 43 / 47 | yes |
| shiftgres | 28; 90.32% | 28 / 31 | yes |
| ferrolog | 30; 81.08% | 30 / 37 | yes |
| hullcheck | 23; 88.46% | 23 / 26 | yes |
| External stars by 27 Sep (ask 5 inputs) | 1,523 / 4,175 / 4,534, others 1,630 / 1,929 / 1,936 / 1,396 | same | yes |
| Ask 1/2 forecast totals | 12,000 / 9,000 etc. | not re-derived this pass | round 2 |

## Competing answers that survived
No fork survives that a shipped statement or the data fails to close. Residual readings, none blocking:
1. Thursday resend. Counting only the Tuesday batches gives April 5,450 / 391,299 = 1.39%, against the golden 1.71%. The literal reading "how many subscribers clicked through to its spotlighted repository" counts a Thursday clicker, who is a subscriber who clicked. All three sends share the campaign name, list and links, and Tuesday recipients already cover the list, so Thursday adds no denominator. No sentence states the resend rule. Moderate wording risk; the literal reading gives the golden.
2. Gateway plus real click by the same Postwerk subscriber (212 subscribers): excluding every all-links subscriber gives 6,595 / 6,923 (-104 / -108) for April and May. The golden removes only the one gateway click per link. The prompt wording "subscribers clicked" closes it. Low risk.
3. Owner role as member: moves kilnkit (23) and shiftgres (29) only. The membership file counts an owner as a member. Low risk.
4. Eight nominations naming a different owner for a shortlisted name (for example verhoevenr/tracewire) are not in the repository file and are not counted; literal full-name match closes it.
5. Seed and test sends add 4 to 5 per issue; they are on separately named seed lists outside the delivered counts. Low risk.

## Spec gates
Checked by me against the unzipped bundle and metadata.json. There is no rubric file in the task folder, so the 25-criteria gate is not countable here.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 5 (csv, json, parquet, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | relaymark_link_clicks 503,380 rows | yes |
| Distractors | 2 or more named in metadata.json, none in a file name | repository_traffic, trending_daily (the file names do not say "distractor") | yes |
| Distractor behaviour | unused by the solution, relevant enough to weigh | design note: they rank nothing, the call is unchanged with both deleted (asserted) | yes (by the note) |
| Deliverables | 1 to 3, each in the golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | prompt states thousands, two-decimal per cent, exact counts | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | shape recorded as "other" in metadata; criteria not countable | not checked |
| Reads as real, not LLM generated | | system-style noise (dialects, BOMs, offsets, rename log, merges); no authoring text in the bundle | yes |

## Gate G reconciliation
The thread's main-call line (mechanism forecasting / method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no) was carried from round 2 and was not re-derived in this pass. It matches the design note: Layer 2 is `forecast_uncertainty`, with the rate read from the 8th day public and validated on the closed lottery spotlights. The thread's own Gate H line is `domain: pass`, `layers: pass`, `decisive_step: analytical`, matching the note's Domain test, Layer 1 / Layer 2 and Decisive step. The declared distractors (repository traffic, trending lists) were not named by the thread as a surface read carrying the task. No mismatch. The card has `stump_class: analytical` and an `analyst_test` that files the slidewell whole-life route, consistent with the note and the thread.

## Stump power (Gate F)
Not re-derived this pass. On the asks only: gateway fetches, id-link resolution, the resend, and identity resolution (hash link, merge, rename) each move a casual path by 15% to 130%. They are data work and not the call's stump.

## Findings, ranked
1. Thursday resend is closed only by the literal reading of "subscribers clicked" and the "delivered" denominator, not by a shipped sentence. Moderate wording risk; not a fork under the literal reading.
2. Postwerk gateway-plus-real-click subscribers (212): the 104 / 108 effect is closed by the prompt wording. Low risk.
3. Owner-as-member and different-owner nominations: low risk, closed by the membership file and full-name matching.

## Next action for the author
None required. Optionally, file the WHAT in the prompt ("across all of the issue's sends, each subscriber once") to close finding 1; that would invalidate the freeze and need a rebuild, so it is not recommended. Otherwise proceed with stage 4 and ship.
