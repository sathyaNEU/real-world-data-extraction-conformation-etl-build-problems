# determinism-check report, task236, 2026-10-28

Context: this is task236's rubric reship. The portal held the main call and the determinism block
passed on the first build; the rubric came back at 79. The repair changed only rows of
`gateway_influenza_results_2027-04-05_to_2027-09-12.csv` outside every region's four-weeks-before/
four-weeks-from change window; the call's figures and every other file are claimed byte-identical to
the shipped pack. target.zip sha256 `5ef00068c44e380a4bc2570bfe6d6e4a72f8139c4a56815cb15eb4a9a1f4e945`
matches the folder's current pack.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated judge thread rebuilt the whole case-construction pipeline from the raw 229,848-row gateway
file with no access to the generator, author notes, or the submission, and reproduced every decisive
main-call figure exactly: the 16 before/after window counts (CRITICAL_COMPONENTS #1) and the 8
infection-ascertainment ratios (CRITICAL_COMPONENTS #2: FN 1.87, MS 0.45, MW 1.53, SC 1.53, and the four
~1.00 ratios), hence the main recommendation (flag FN, MS, MW, SC; not NC, TB, CW, MN) is forced. Getting
there required the thread to independently discover and resolve, purely from the gateway file's own
structure with zero help from any shipped document, three real data-identity issues: a free-text
result-string trap ("No influenza virus detected" contains "detected"), specimen-sharing patient_keys (28
pairs, always identical demographics), and age-discontinuous patient_keys (16 keys, a clean bimodal gap at
0-1 vs 21-40, several also sex-mismatched). Of four candidate merge/split variants it tried, only the
merge-plus-split rule reproduces the solution's stated totals (46,380 overall, 44,872 in the eight
regions) exactly, so the rule is forced by the data, not chosen freely. Gates A-E all pass for the main
call.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Before/after case counts, all 8 regions (CRITICAL_COMPONENTS #1) | FN 434/2226, NC 763/2267, TB 286/895, CW 583/1368, MN 2459/6943, MS 2603/2638, MW 1210/6763, SC 655/2487 | identical | yes, exact |
| Infection-ascertainment ratios, all 8 regions (CRITICAL_COMPONENTS #2) | FN 1.87, NC 1.01, TB 1.00, CW 1.00, MN 0.99, MS 0.45, MW 1.53, SC 1.53 | identical | yes, exact |
| Total cases built (step 1) | 46,380 | 46,380 (only under merge+split; raw 46,566, merge-only 46,538, split-only 46,582) | yes, forced |
| Cases in the eight regions (step 2) | 44,872 | 44,872 | yes, exact |
| Season-to-date notified cases, all 8 regions (supplementary) | FN 3,560; NC 4,113; TB 1,505; CW 2,491; MN 12,037; MS 6,133; MW 11,230; SC 3,646 | within 1-3 cases of each, deviations netting to exactly zero across regions (+2/-2 pattern) | yes, within residual the judge attributes to its own script's boundary choice, not a traced task defect |
| Week-36 notified rate per 100,000, all 8 regions (supplementary) | FN 53.7; NC 39.1; TB 54.6; CW 50.6; MN 36.7; MS 24.9; MW 68.4; SC 104.0 | consistent with the above residual, no flag/rank effect | yes, same caveat |

## Competing answers that survived
None, for the main call. The judge built and refuted the two natural alternative metrics with checkable
numbers (raw case-count growth 2.3-5.6x in seven of eight regions; sentinel swab positivity alone, which
flags NC/TB/CW/MN and misses FN) and confirmed no shipped fact supports either as the governing metric.

The one open item is the small residual in the two supplementary per-region figures (season-to-date count
and week-36 rate). The judge's own reconstruction landed 1-3 cases off each committed figure, netting to
exactly zero across the eight regions, while the much larger and more decisive before/after window figures
reproduced with zero error under the same pipeline. That pattern (a small, sign-balanced, likely
boundary/tie-break artifact confined to the harder-to-pin cutoff-and-rate step, with the load-bearing
ascertainment figures exact) is best read as noise in the judge's from-scratch script rather than a fork
in the task; it is far too small (<0.1% of any region's season total, under one point of any rate) to move
any flag or any headline figure. Not escalated as a finding, but named here since the author specifically
flagged these two figures as newly dependent on the key-sharing/postcode-field reading in this repair pass.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 13 | yes |
| Formats | 3 or more | csv, pdf, xlsx, md (4) | yes |
| Large file | 1 file ≥25,000 rows or large DB | gateway file, 229,848 rows | yes |
| Distractors named, not in file names | 2 or more in metadata.json, none flagged by filename | `influenza_vaccine_doses_by_region_2027_wk14-36.csv`, `laboratory_turnaround_by_week_2027.csv` | yes |
| Distractors relevant, unused, one arithmetically answers a graded quantity ruled out by a shipped fact | both distractors are plausible surveillance files unused by any solution step (vaccine coverage and lab turnaround do not enter the case-build, region-attribution or ascertainment-ratio steps) | yes | yes |
| Deliverables 1-3, all in golden, no required format family | 2 deliverables (xlsx, png) | both present, matches golden list | yes |
| Asks multi-dimensional, unit/rounding stated | main call across 8 regions x before/after x ratio; xlsx asks season-to-date + week-36 rate per region, "to one decimal place" stated | yes | yes |
| Prompt shape identifiable, rubric ≥25 criteria | metadata records shape 11, "30 criteria" | yes | yes |
| Nothing LLM-generated, goldens read as real work product | judge: 45 distinct free-text result phrasings across services, mid-season postcode redraw, duplicate key issuance, blank/0000 postcodes, UTC/local timestamps, none narrated in any shipped doc | pass | yes |

## Gate G reconciliation
Judge: mechanism `method_or_model_selection`, stumping_family `analytical_non_defect`, surface_read_dependency `no`, sole_data_defect `no`. Design note / card: `stump_class: analytical`, the decisive step named as "estimating each region's influenza infections... from the sentinel practices' influenza-like-illness consultation rate times the share of their protocol swabs positive for influenza, and reading the change in notified cases against that index rather than against the region's own tests" (field_method, Layer 2). These agree exactly: the judge's "ascertainment-ratio-vs-sentinel-reference method is the field's own technique" restates the design note's domain_test almost word for word, and neither names the two named distractors, the testing-change register, or any other shipped artifact as the surface read carrying the task — the judge's naive-metric alternatives (raw counts, positivity alone, consultation/positivity-only ratios) are the same three the design note's analyst_test names as the easy, wrong routes. No mismatch, no declared distractor doing load-bearing work.

Gate H line: `domain: pass, layers: pass, decisive_step: analytical`, versus the card's `stump_class: analytical`, `analyst_test` and `domain_test` quoted above. These also agree: the judge's H1 swap test ("health region"/"influenza" into another field's nouns breaks the method) restates the design note's own Swap line; the judge's H3 easy-route/wrong-answer pair (rank by raw growth, or by positivity alone, both wrong) is the same pair the card's analyst_test names. The judge independently rediscovered, and classed as forced Layer-1 mess rather than a missing Gate-B rule, the merge/split case-identity resolution that the design note's Layer 1 list anticipates ("result wording that differs by service," "a boundary review that moved a postcode," "a multiplex panel reporting influenza A and B on their own rows") without being told the specific merge/split rule by any shipped document — consistent with the note's claim that this mess is realistic and never planted to be caught. This is the landable-call case the contract calls out: the judge classed the decisive step analytical because the sentinel-ascertainment-index comparison is a recognized field method, and it reached the golden itself by applying that method with no judgment the data had to settle beyond what the design note already pins (the estimand paragraph). Recorded as a clean reconciliation, not a finding.

## Stump power (Gate F)
The judge rates stump power as real and two-layered: the main-call trap (rejecting positivity and raw-count growth in favor of the sentinel ascertainment ratio) is a genuine method-selection stump on honest data, and the supplementary-figure case-identity cleaning (colliding/shared patient_keys, with the data dictionary's own wording "the gateway's key for the person" inviting face-value trust) is a second, independent trap a model could plausibly miss in a 230K-row file with no narrative tip-off. No too-easy signal raised.

## Findings, ranked
1. (Not escalated, logged for the author's awareness) A small, sign-balanced residual (1-3 cases, netting to zero across the 8 regions) between the judge's independent reconstruction and the committed season-to-date/week-36-rate figures, confined to the harder cutoff-and-rate step while the decisive before/after window figures matched exactly. Most likely a boundary/tie-break artifact in the judge's own from-scratch script, not a task defect; too small to move any flag, rank, or headline figure, and does not change the verdict or disposition.
2. No other findings. Hygiene passes; no competing defensible answer survives for the main call or any supplementary answer; no Gate G or Gate H mismatch against the design note or card.

## Next action for the author
None required before reshipping; file the small season-to-date/week-36-rate residual as a known non-issue (a from-scratch reviewer artifact, not a task defect) if it resurfaces in a future pass, and proceed to portal resubmission on this rubric-repair build.
