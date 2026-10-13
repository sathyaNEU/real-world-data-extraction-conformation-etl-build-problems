# determinism-check report, task129, 2026-10-13 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Executed literally, the shipped text gives one call: fix the Bolge front end (about 1,460,000 mobile views a month at August's traffic) ahead of the header-bidding ad stack (about 610,000). Each effect is read where only its own change acts, standardised within phone class and first or later view since the latest deploy, then valued on the August scored views each fix acts on. The easy routes give the opposite call (phone class only: ad stack 1.23M against front end 0.80M; no stratification: 1.14M against 0.74M). Extra strata leave the rounded figures unchanged and the ranking never moves. The title asks and the six monthly image figures all reproduce. One judge thread, one pass; no retry. This is the single re-judge licensed after the pass 1 FIX_NOW.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Front end, August | 1,460,000 | 1,459,976 | yes |
| Ad stack, August | 610,000 | 609,889 | yes |
| First-view share, ad-supported views of six groups | about 75% | 74.6% | yes |
| First-view share, windows read | about 25% | 23.5% / 23.2% | yes |
| Banner ST/LA/KD | 180/140/110k | 177.7/141.0/108.8k | yes |
| Image pipeline ST/LA/KD | 130/110/90k | 129.0/109.7/88.4k | yes |
| Fonts ST/LA/KD | 110/80/80k | 109.7/80.7/80.4k | yes |
| Banner/image/fonts totals | 430/330/270k | 427.6/327.2/270.8k | yes |
| Image req and KB per view, Mar to Aug | 11.4/530, 12.2/710, 12.4/750, 12.5/770, 12.3/760, 12.6/790 | identical | yes |

Frame checks: 2,814,292 rows; 2,693,585 after pv_id dedup, phone filter and repeat-beacon drop; July and August counts match the Q3 close-out exactly.

## Competing answers that survived
Forks tested, none moves the call:
- Subscription must match the view's title: front end 1,473,510 (rounds 1,470,000), ad stack 613,064 (610,000). Terms say "signed-in subscribers" with no title condition; golden is the literal reading. Shifts one graded figure by 10k. 1.05% of subscriber views.
- Calendar-day windows instead of the deploy moment: 604,909 / 1,464,097. Service level section 3 says "the moment ... deployed", so the exact moment governs.
- Ad stack valued per view after each wave's switch-on: 600,140. Section 4 "the change now reaches" favours the golden reading.
- Image pipeline from title-wide share: 111/96/77k. The register line names hero templates and the data separates them.
- Repeat-beacon drop not stated in the field guide: without it March to May image figures become 10.8/503 or 11.0/513 against 11.4/530. Repeats are unmistakable (same device, page, timings, 3 to 19 s apart), "page view" is the unit asked; touches ask 2 March to May only.
Optional, non-blocking closes: a prompt sentence "a subscription counts whatever title it is for"; the "now reaches" wording. Neither is required.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | 6 (csv, xlsx, pdf, md, parquet, txt) | yes |
| Large file | 25,000 rows or more | parquet, 2,814,292 rows | yes |
| Distractors in metadata.json, none in a file name | 2 or more | 3: desktop_field_summary, amp_landing_views, newsletter_sends | yes |
| Distractors unused yet weighable; fact rules out | yes | desktop outside mobile scope, AMP outside release train, newsletter log; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (pptx, xlsx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per title by change, six months by two measures; rounding in the prompt | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 11, 28 criteria per design note | yes |
| Reads as real, not LLM generated | yes | judge found in-fiction provenance, no authoring language | yes |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g decomposition_attribution, stump_class analytical, stump_strategy composition_mix. Match. The declared distractors are not the surface read carrying the task; none is load-bearing. Gate H line from the thread: domain: pass, layers: pass, decisive_step: analytical. Card analyst_test and domain_test agree: the decisive step is estimating each change's effect on its clean population by device class and first or later view, then valuing it on the population the fix acts on; the easy route files the ad stack.

## Stump power (Gate F)
Plausible stump. A model standardising on phone class alone, which the registry presents as the reporting class, files the ad stack at 1.23M against 0.80M. Reaching the front end requires noticing that effects concentrate on a device's first view after a deploy and that the read windows are about 25% first views against about 75% in the populations the fixes act on. The release log's bundle hashes make the mechanism discoverable from the files. Measured stump power remains the portal's.

## Findings, ranked
1. None blocking.
2. Title-matching reading of "subscriber" shifts the front end by 10k at rounding (call unchanged).
3. Repeat-beacon drop is unfiled in the field guide but unambiguous in the data (ask 2, March to May only).
4. "now reaches" wording: 600k against 610k under the weaker reading.

## Next action for the author
Proceed to stage 5 SHIP with the current bundle; optionally add the one-sentence subscription-title close to the prompt only if you accept a rebuild.
