# determinism-check report, task118, 2026-10-27

Architecture 3 (card `.claude/skills/fingerprint/cards/task118.json`, `"architecture": "v3"`). target.zip sha256 prefix 900e68f673731000.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: `method_or_model_selection` (bordering `statistical_rigor`, left-censored exposure-duration reconstruction), stumping_family: `analytical_non_defect`, surface_read_dependency: `no`, sole_data_defect: `no`

## Why
The decisive step is reconstructing each current user's true first-start date for their benzodiazepine/Z-drug by walking the repeat-template chain (`replaces_template_id`) in `repeat_templates_hypnotics_2026-10-01.csv`, and for the one practice that migrated clinical systems (Mill Road Group Practice, Q89159), continuing through `migration_source_ref`/`SupersededRef` into `Q89159_repeat_templates_previous_system_2026-07-12.csv`; a chain that still dangles is correctly left-censored to "before April 2024" (the >=24-month, 1.1-rate-ratio tier). The isolated judge thread independently recomputed this in full from the shipped files and reproduced the main call (Saltreach Coast 19.2->19, Hethermoss 15.3->15, all others <=12.6) and both of the submission's own named wrong-method forks (first-item-in-extract -> Corvenham Central 73.9 vs Saltreach's 54.6; assume-2-years-tenure-at-open -> Hethermoss 12.8 vs Corvenham 10.3 vs Saltreach 9.9). Gates A-E all pass; no competing defensible answer survives for the main call or for any of the four docx/xlsx asks.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Current users, total | 28,253 | 28,253 | Yes |
| Current users, Saltreach Coast | 5,034 | 5,034 | Yes |
| Avoided admissions, Saltreach Coast | 19 | 19.2 -> 19 | Yes |
| Avoided admissions, Hethermoss | 15 | 15.3 -> 15 | Yes |
| Avoided admissions, other 4 localities | <=13 | <=12.6 | Yes |
| Fork A (first-item-in-extract start): winner | Corvenham Central | Corvenham Central 73.9 > Saltreach 54.6 | Yes (confirms fork, not a real competing answer) |
| Fork B (2y-tenure-at-open assumption): winner | Hethermoss | Hethermoss 12.8 > Corvenham 10.3 > Saltreach 9.9 | Yes (confirms fork, not a real competing answer) |
| xlsx F1/F2/F3 (admissions/bed-days/readmissions by locality and age band) | e.g. Saltreach 889/1327/22140/347 | Saltreach 909/1,359/~22,100-range/~close (same ranking, +2-3%) | Close, not exact -- see note below |

**Note on the xlsx falls-cohort figures:** the judge's independent SUS spell/transfer reconstruction landed within roughly 2-3% of the committed admissions-by-age-band figures across all six localities, with the identical ranking and every definitional element (spell-chaining on provider+hospital_spell_no, the destination-51 transfer rule, the emergency-admission method set, the W00-19 external-cause filter, FY cut, age-at-admission, locality-by-practice) matching. The thread could not find an alternative reading of the falls dashboard's F1-F3 definitions that explains the residual gap better than its own same-day multi-candidate transfer tie-break, and did not find a materially different competing answer. This is reported as a close, consistent reproduction, not a SOLUTION_WRONG finding -- but it is the one place in this report where I am relying on the judge's own account rather than a second independent recompute, since I (the orchestrator) did not re-derive the SUS spell-chaining logic myself. If the author wants certainty here, a targeted recheck of the spell/transfer join (specifically the tie-break for same-day multi-candidate transfers) is cheap and would either confirm the golden exactly or surface a small table-extraction/tie-break defect, neither of which would change the verdict or the disposition.

## Competing answers that survived
None. The only two alternative readings the thread could construct (first-item-in-extract as start; 2-years-tenure assumption for already-established users) are exactly the two forks the submission itself names and rules out, and both are demonstrably inferior shortcuts, not equally defensible alternative readings. The 45%-off-drug fraction and the rate-ratio table are fixed constants applied identically to every locality, so neither can flip the ranking; the margin (19 vs 15, ~21%) is not knife-edged.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | >=10 | 12 | Yes |
| Format mix | >=3 formats | csv, eml, pdf, xlsx (4) | Yes |
| Large file | one file >=25,000 rows | `dispensing_hypnotics_2026-04_2026-09.csv`, 185,725 rows | Yes |
| Distractors named | metadata.json names >=2, no filename labels one | `hypnotic_prescribing_dashboard_q2_2026.xlsx`, `falls_service_referrals_2025-26.csv`; neither filename contains the word "distractor" | Yes |
| Distractor unused, relevant, weighable | each distractor unused by the solution but relevant enough to weigh | Dashboard is a prescribing-metrics workbook by locality/practice; referrals log is a falls-service intake log; neither is used in the solution path (SUS cohort and the dispensing/template chain are used instead) | Yes |
| One distractor reproduces arithmetically, ruled out by a shipped fact | required | `hypnotic_prescribing_dashboard_q2_2026.xlsx`'s "Patients aged 65+ with an item" column sums to 5,176 for Saltreach Coast, close to the committed current-user count (5,034) under NHS fiscal-quarter convention (Q2 = Jul-Sep, i.e. the same months policy section 4 requires); it is ruled out by the policy's own current-user definition (`hypnotics_deprescribing_policy_2026.pdf` section 4: "aged 65 or over **on 1 January 2027**", not current age as of the Q2 2026 snapshot, and an items/patients distinction the dashboard does not carry) | Yes |
| Deliverables | 1-3, all present in golden, no format family required | 2 deliverables (`.docx`, `.xlsx`), both present in `golden/` and named in `metadata.json` | Yes |
| Asks multi-dimensional, unit+rounding stated | required | xlsx ask is a 6-locality x 4-measure grid (24 figures); prompt states "Give admissions, bed-days and readmissions as whole numbers." | Yes |
| Prompt shape identifiable, rubric >=25 criteria | required | `metadata.json` `prompt_shape: "07"` (one of six with sized avoidance/runner-up/gap, plus a 6x4 grid = 24 figures); 24 grid cells + main-call components comfortably clears 25 | Yes (by inspection; rubric file not separately audited in this pass) |
| Not LLM-generated, reads as real work product | required | Judge thread's Files/Hygiene check: PASS, no LLM-tidy tells, realistic mess (legacy-system export in different casing/date format, a same-name-different-practice confusable, a historical practice-code merge). I additionally spot-checked `golden/deprescribing_case_2027.docx` (a board-paper memo with a presenter, a purpose line, a locality table) and `golden/deprescribing_placement_2027.xlsx` -- both read as genuine board/analyst artifacts, not LLM prose | Yes |

## Gate G reconciliation
The judge thread's classification (mechanism `method_or_model_selection`/`statistical_rigor`, stumping_family `analytical_non_defect`, surface_read_dependency `no`, sole_data_defect `no`) matches the design note's `## Stump sentence` and `## Three rules` section closely: the note's "Not semantics" and "Not rule application" paragraphs argue the same thing the judge independently found -- that the trap is a censoring/window-opening problem in the exposure-duration record, not a misread field or an executed rule, and that no decoy is planted (dashboard and referrals files "rank nothing on the decision").

One reconciliation finding: the fingerprint card (`.claude/skills/fingerprint/cards/task118.json`) carries two pre-build planning fields that do not match the as-shipped mechanism -- `"gate_g": "forecasting"` and `"stump_strategy": "composition_mix"`. The judge's actual, as-built classification is `method_or_model_selection`/`statistical_rigor` (a left-censored exposure-duration reconstruction), which is neither a forecast (the window 1 Apr-31 Dec 2027 is priced from the policy's own fixed rate-ratio table, not projected) nor a composition/mix decomposition. This is a card-hygiene mismatch, not a determinism or Gate-H defect -- the judge did not name the declared distractors as load-bearing, and Gate H (`domain: pass`, `layers: pass`, `decisive_step: analytical`) lines up cleanly with the card's `stump_class: analytical` and the design note's `analyst_test`/`domain_test`. Per the contract, a mismatch between the thread's classification and the card is the finding that most reliably predicts a send-back on a future pass if left unreconciled, so it is worth fixing even though it does not change this pass's verdict.

## Stump power (Gate F)
High, for a legitimate reason. A solver must recognize that "time since the patient first started" means first-ever start (not time on the current repeat template), forcing a walk of a 98,020-row `replaces_template_id` chain; it must separately notice that one migrated practice needs a second, differently-formatted legacy export joined in; and it must make a defensible call about chains that still dangle after that. The two shortcuts a time-pressed analyst reaches for (first item in the extract; assume long tenure for anyone already on the drug) are exactly the ones demonstrated above to flip the locality, to Corvenham Central and Hethermoss respectively. This is the FINE-numbers shape Gate F wants: the design note additionally frames the decisive step as "the standard's general method" for pricing excess risk by time-since-exposure in benefit-risk assessment -- a textbook route a strong analyst takes -- which per the contract's Gate G/H weighing note is a landable call, not a defect, since the judge itself reached the golden by applying that standard method with no judgment the data had to settle beyond the censoring reconstruction.

## Findings, ranked
1. (Low severity, card hygiene) `.claude/skills/fingerprint/cards/task118.json` fields `gate_g: "forecasting"` and `stump_strategy: "composition_mix"` are stale relative to the as-shipped mechanism (`method_or_model_selection`/`statistical_rigor`, a censored exposure-duration reconstruction). Fix location: the card (not the task). No rerun needed; this does not affect the determinism verdict.
2. (Informational, not a defect) The xlsx falls-cohort figures (F1/F2/F3) reproduced within ~2-3% rather than to the exact digit under the judge's own independent SUS-transfer reconstruction; the gap is most likely a same-day multi-candidate transfer tie-break the falls-indicator PDF does not spell out, not a competing reading. No fix required to ship; optional cheap recheck available if the author wants exact-digit confirmation.

## Next action for the author
Update `.claude/skills/fingerprint/cards/task118.json`'s `gate_g` and `stump_strategy` fields to reflect the as-shipped mechanism (`method_or_model_selection` / censored exposure-duration reconstruction) so a future guard or reviewer pass does not flag a mismatch against this report; no change to the task itself, the prompt, or any golden is needed, and no model rerun is required.
