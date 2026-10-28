# determinism-check report, task275, 2026-10-28

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (also method_or_model_selection for the pooled-vs-stratified
raising choice), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge thread derived its own independent reading and recomputation from the shipped files before
opening the submission's graded blocks, and every committed figure reproduced exactly: 12,000 logbook trips,
856 observed, the segment discard shares (TR1 13%, TR2 12%, NEP 14%, BT 12%, SN 8%, GN 7%, LL 5%, POT 6%),
the four designated segments (TR1, TR2, NEP, BT), both supplementary asks (first-sale value to the tenth,
days-at-sea after the VMS terminal-handoff correction), and the three named wrong "easy routes" (DIS-only
raising naming NEP alone; pooled-ground raising dropping BT; counting every unobserved trip's own declared
BMS as discarded, which pushes GN over the line). `selectivity_programme_terms_2027.pdf` 2.1/3.1-3.4 pins
the estimand (catch = landed + returned, live weight, every 2025 trip, segment from vessel_register.csv),
and no decisive fact is missing (Gate B passes). The one methodological fork, ground-stratified vs
segment-pooled raising, is forced to the stratified reading by data the package itself ships (BT's observed
trips sit on WC14/WC15 for 39% of their hours against 69% for unobserved trips), so this is not an open
Gate C fork, it is the decisive analytical step.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Observed trips of 12,000 | 856 | 856 (855 clean + 1 in a DST-ambiguous UK clocks-back hour) | Yes |
| BMS/hr observed vs unobserved, TR1 | 25.28 / 2.10 | 25.28 / 2.10 | Yes |
| BMS/hr observed vs unobserved, TR2/NEP/BT/SN | 9.97/0.84, 1.44/0.11, 4.66/0.06, 6.82/0.05 | exact match | Yes |
| BT hours on WC14/WC15, observed vs unobserved | 39% / 69% | 39% / 69% | Yes |
| Discard shares, all 8 segments | 13,12,14,12,8,7,5,6 | 12.79→13, 11.94→12, 14.08→14, 11.89→12, 7.68→8, 7.30→7, 4.80→5, 6.35→6 | Yes |
| Designated segments | TR1, TR2, NEP, BT | same | Yes |
| First-sale value, all 8 segments (GBP 000s) | 12,062.3 / 7,174.4 / 8,053.4 / 9,649.8 / 3,561.4 / 1,719.9 / 693.8 / 2,332.9 | exact match, after excluding 700 Barlow & Hobbs duplicate market-lot lines | Yes |
| Days at sea, all 8 segments | 2,236 / 3,032 / 3,517 / 2,128 / 1,737 / 2,419 / 1,362 / 2,593 | exact match, after the 14-vessel / 1,718-hour VMS terminal-handoff reassignment | Yes |
| Pooled-raising alternative (wrong route) | BT drops below 10% | BT = 8.6% pooled | Yes, reproduces the claimed wrong answer |
| DIS-only raising alternative (wrong route) | NEP alone over 10% | NEP 11.9%, TR1 4.0%, TR2 4.1%, BT 2.9% | Yes, reproduces the claimed wrong answer |
| Unobserved-BMS-counted-whole alternative (wrong route) | GN pushed over 10% | GN = 10.5% (true share 7.3%) | Yes, reproduces the claimed wrong answer |

One non-blocking prose nit: FINAL_RECOMMENDATION states "TR2 nearest the line at 12 per cent," but the
judge's exact (unrounded) recomputation puts BT (11.886%) marginally nearer the 10% line than TR2 (11.936%);
both round to the same committed whole-percent figure, so no graded value is affected. Cosmetic only, no fix
required to ship.

## Competing answers that survived
None. No competing defensible answer survives for the main call or either supplementary ask; the one real
fork (pooled vs stratified raising) is closed by the data itself (the BT ground-share imbalance), not left
open.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | >= 10 | 17 | Pass |
| Format mix | >= 3 formats | 4 (csv, xlsx, pdf, txt) | Pass |
| Large file | >= 1 file of 25,000+ rows or large DB | elogbook_landings ~75k, observer_hauls ~65k, sales_notes ~99k, vms_positions ~197k rows | Pass |
| Distractors named | >= 2 in metadata.json, none in a file name | `quota_uptake_2025.xlsx`, `gear_specifications_2025.csv`; neither file name says "distractor" | Pass |
| Distractors relevant + unused | relevant enough to weigh, unused by the solution | quota_uptake is species-level EU/UK quota uptake (a real fisheries-management artifact, could tempt a solver toward a quota-pressure framing of "designation"); gear_specifications is per-vessel gear/mesh detail (could tempt a gear-type framing of discard risk); neither feeds the segment-level discard-raising computation | Pass |
| Deliverables | 1-3, present in golden, no required format family | 2 (`segment_discards_2025.xlsx`, `segment_discards_2025.png`), both present in `golden/` | Pass |
| Asks multi-dimensional | not stacked lookups, unit+rounding stated | 8 segments x 3 metrics (discard share, first-sale value, days at sea), each metric requiring its own reconciliation (raising, duplicate-note exclusion, VMS terminal handoff), not a plain lookup; prompt states "whole per cent," "thousands of pounds to one decimal place," "whole days" | Pass |
| Prompt shape / rubric criteria | identifiable shape, rubric >= 25 criteria | prompt shape present (one context paragraph, one main ask, one file+format request); no rubric artifact is shipped in the task folder (rubric is generated downstream at grading time) | Not independently verifiable from this folder |
| Not LLM-generated | files read as real work product | README_files.txt, observer_scheme_manual_2025.pdf and sales_notes_2025.csv read as genuine operational documents (dated memos, named staff, irregular formatting); no boilerplate or placeholder tells found in the sampled files | Pass |

## Gate G reconciliation
Judge thread: mechanism `statistical_rigor` / `method_or_model_selection`, `surface_read_dependency: no`,
`sole_data_defect: no`. Card (`.claude/skills/fingerprint/cards/task275.json`): `stump_class: analytical`,
with `analyst_test` naming the same mechanism the judge found independently -- "raising the observer
scheme's discard share of catch, area by area, to each segment's hours fished names only the Nephrops
trawlers" (the easy route) -- and `domain_test` naming the observer effect and the fishery's catch structure
as what a swapped domain would destroy. These agree with the judge's own account; no mismatch. The judge did
not name either shipped distractor (`quota_uptake_2025.xlsx`, `gear_specifications_2025.csv`) as load-bearing
or as the surface read carrying the task, so neither distractor is over-load-bearing. No finding here.

## Gate H reconciliation
Judge thread: `domain: pass`, `layers: pass`, `decisive_step: analytical`. DESIGN_NOTE.md `## Three rules`
(lines 32-46): task type is Survey Research & Official Statistics'
`nonresponse-calibration-measurement-error-adjustment`; `No decoy:` nothing is planted to be caught, no
memo/report/stakeholder figure states a segment's discards, and no shipped file ranks the segments; `Not
semantics:` every field read correctly still names NEP alone, because no definition says BMS is landed only
when observed; `Not rule application:` the terms file the outcome but nothing on estimating it for
unwatched trips, and the decisive comparison (observed-vs-unobserved BMS per hour on the same ground) is
reached only by a join no document invites. The judge's independent account matches this almost exactly: it
named the same two confounds (the observer-presence effect on BMS, and BT's non-representative ground
coverage) as the decisive analytical step, and verified the same named wrong routes (DIS-only raising names
NEP alone; pooled-ground raising drops BT) that the design note's `Not rule application:` line enumerates as
the "easy route" family. The judge classed the decisive step `analytical` because the golden applies the
field's own standard discard-raising method (observer-coverage raising under measurement-affecting
sampling, core DCF/ICES methodology) and the judge itself reached the golden by applying that method, with
the ground-stratification choice forced by data the package ships (the BT ground-split imbalance), not by
unexplained judgment. Per the skill's guidance this is a landable call, not a mismatch: a library method
applied to honest, self-revealing data is a textbook stump route, and stump power is weighed, not
disqualified, for using it. No Gate G/H mismatch found.

## Stump power (Gate F)
Two independent analytical traps stack on honest data: (1) the observer effect -- raising discards from the
observed trips' DIS field alone (the "obvious" discard record) misses that BMS flips from discarded
(unobserved) to landed (observed), landing on NEP alone instead of the four true designations; (2) ground
stratification -- raising per segment without checking the ground mix misses that BT's observed trips are
concentrated away from its highest-discard grounds, understating BT's true share below the 10% line. Neither
trap is a planted decoy or a misleading reported figure to reject (`sole_data_defect: no`); both require
constructing an unbiased raising estimator from honest microdata, a genuine fisheries-discard-estimation
method. This is the kind of library-method application the client wants rewarded (`stumping` 1.3), weighed
against the design note's own ladder evidence (20 constructions, spread at most 0.68 points once the BMS and
ground corrections are both applied, versus six distinct designated sets across the enumerated wrong-route
family) rather than disqualified for being "just the standard method."

## Findings, ranked
1. (Non-blocking, cosmetic) FINAL_RECOMMENDATION's prose, "TR2 nearest the line at 12 per cent," is contradicted
   by exact arithmetic (BT 11.886% vs TR2 11.936%), though both round to the same committed whole-percent
   figure and no graded value is affected. Optional wording fix, no rerun needed.
2. (Informational, not a defect) The prompt shape's rubric is not shipped in this task folder as an artifact,
   so the 25+ criteria spec gate could not be independently verified from the files available to this review;
   this is generated downstream and outside this pass's scope.

## Next action for the author
No repair is required to ship. If desired, make the one-sentence cosmetic edit in `submission.md`'s Final
Recommendation, from "TR2 nearest the line at 12 per cent" to "BT and TR2 both nearest the line at 12 per
cent" (or similar), since BT is marginally closer on exact arithmetic; this changes no committed/graded
figure and needs no rerun.
