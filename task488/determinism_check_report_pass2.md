# determinism-check report, task488, 2026-10-28

## Verdict
DETERMINISTIC

**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why

The judge thread independently re-implemented the Rasch marginal-maximum-likelihood calibration (anchors fixed at
the 2021 launch values, per-window population mean/sd by EM) from scratch against `tessaline_item_bank_export_20270331.csv`,
`tessaline_sessions_2025-26.csv`, and the 3,894,963-row operational slice of `tessaline_item_responses_2025-26.parquet`,
and reproduced the main recommendation (199 items, grade split 27/39/31/33/49/20) and both CRITICAL_COMPONENTS rows
(total-below-cut 123/111/119/117/101/130; workshop-below-cut 60/49/62/61/46/60) exactly. It also reproduced the
bank_import row count (2,538) and all 30 grade-by-domain cells and all 6 grades' enemy-set counts in
`pool_summary_2027-28.xlsx` by reconstructing the catalog's version-overlay logic (v1 full record, later versions
overwrite only `changed_fields` columns) from `qrac_item_authoring_catalog_20270315.xlsx` and
`qrac_framework_crosswalk_2010_to_2026.csv`. No committed/graded figure failed to reproduce. The one unreproduced
number is 138, a rejected-alternative figure quoted only in the FINAL_RECOMMENDATION narrative ("not the 138 that
reading each workshop item against the reported scale scores gives"), which is not itself a graded deliverable value
(see Findings).

## Recomputation ledger

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Operational responses after dropping unscored re-deliveries | 3,894,963 | 3,894,963 | yes |
| Total items below Approaching cut, grades 3-8 | 123,111,119,117,101,130 | identical | yes |
| Workshop items below cut, grades 3-8 | 60,49,62,61,46,60 | identical | yes |
| Shortfall vs. floor 150 / total commission | 27,39,31,33,49,20 / 199 | identical | yes |
| "Not the 93" (panel ratings as-is, no recalibration) | 93 | 93 | yes |
| "Not the 138" (calibrate against reported scale scores) | 138 | 191 and 125 under two reasonable re-implementations | no (non-graded narrative figure only) |
| bank_import_2027-28.csv row count | 2,538 | 2,538 | yes |
| Imported items by grade x 2026 framework domain (30 cells) | per submission | all 30 cells identical | yes |
| Enemy sets and items by grade (6 grades) | per submission | all 6 pairs identical | yes |

## Competing answers that survived

None for any graded/committed figure. The two natural shortcuts an analyst might take (trust the panel's existing
provisional rating verbatim -> 93; or calibrate against the circularly-dependent reported scale score -> a figure in
the 125-191 range depending on exact implementation, versus the design note's claimed 138) both produce clearly
different, wrong totals, and the Corvane specification's instruction to estimate difficulty "from the 2025-26
operational responses" (not from the panel rating, not from the reported score) rules both out on a shipped fact.
The imprecision in exactly which number the "read against reported scores" shortcut lands on (191 vs. 125 vs. the
claimed 138) does not open a competing *committed* answer -- it is friction in the narrative aside only.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | >= 10 | 12 | Yes |
| Format mix | >= 3 formats | csv, xlsx, pdf, parquet (4) | Yes |
| Large file | 1 file >= 25,000 rows or large DB | `tessaline_item_responses_2025-26.parquet`, 3,925,625 rows | Yes |
| Distractors named, 2+ | >= 2 in metadata.json, none labelled in a file name | 3 named (`qrac_workshop_payments_2024_2025.csv`, `tessaline_platform_incidents_2025-26.csv`, `qrac_writing_panel_ratings_2024_2025.csv`); no file name says "distractor" | Yes |
| One distractor reproduces arithmetically and a shipped fact rules it out | 1 | `qrac_writing_panel_ratings_2024_2025.csv`: trusting its mean as the operational difficulty gives exactly 93, ruled out by the bank export's `difficulty_basis` column | Yes |
| Deliverables | 1-3, all present in golden | 3 (`bank_import_2027-28.csv`, `pool_summary_2027-28.xlsx`, `low_band_commission_memo.docx`), all present under `golden/` | Yes |
| Asks multi-dimensional, unit/rounding stated | yes | prompt states "every count as whole items and every difficulty to one decimal of a scale point"; asks are per-grade x per-domain / per-grade enemy sets, not stacked lookups | Yes |
| Prompt shape identifiable, rubric >= 25 criteria | yes | prompt shape (count x 6 grades, domain breakdown 6 grades x 5 domains = 30 cells, enemy sets x 6 grades, memo+chart) easily supports 25+ gradable criteria; no rubric file is shipped in the task folder to count directly, so this is inferred from prompt shape, not independently verified against a rubric artifact | Likely pass (unverified directly) |
| Not LLM-generated, goldens read as real work product | yes | thread reports PASS: operational exports, versioned catalog, incident log, payment records; no README/benchmark-disclosure language seen | Pass (per thread; not independently re-sampled by me) |

## Gate G reconciliation

Thread: `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`,
`sole_data_defect: no`. Design note's `## Three rules`: `Layer 2: field_method`, decisive step is "estimate each
workshop item's difficulty jointly with the students' abilities ... holding the launch items at their 2021 values,"
labelled `Not semantics`, `Not rule application`, `No decoy`. Card (`.claude/skills/fingerprint/cards/task488.json`):
`stump_class: analytical`, with `analyst_test` describing the same 138-vs-199 split and `domain_test` grounding the
quantity in IRT jointly estimated with examinee ability in an adaptive test. These all agree: the decisive step is
classed analytical by the thread, the design note, and the card alike, with the same named easy route (calibrate
against the reported/circular scale score) producing the same named wrong answer family (near 138, empirically 125-191).
No mismatch. The one named distractor that is load-bearing for the main call (`qrac_writing_panel_ratings_2024_2025.csv`,
giving 93) is correctly the declared distractor in metadata.json, not an undeclared surface read the thread had to
discover on its own, and the thread did not name it as "the surface read carrying the task" -- it named the reported
scale score path as the decisive fork, consistent with the design note's own framing. This is the library's standard
item-calibration method (fixed-anchor MMLE recovers anchor values when the panel-rating or reported-score shortcuts
do not), which is a landable call per `stumping` 1.3: the main thread should weigh it against the design note's ladder,
but nothing here indicates the stump is disguised rule application or a planted defect.

## Stump power (Gate F)

Good, per the thread: a strong model must (a) recognize that provisionally panel-rated workshop items need a real
IRT recalibration rather than a readout of the panel value or the circularly-dependent reported scale score, (b)
handle the within-year growth structure (fall/winter/spring ability populations) correctly, and (c) reconstruct the
catalog's version-overlay semantics for the import and domain crosswalk. The gap between 199 and the two naive
shortcuts (93, and roughly 125-191) is large and non-fragile on most grades. The design note's "Standing family" /
"Ruling-out loudness" analysis (checking that the launch items re-estimate within 1.0 point only under the joint
calibration) is the kind of check the client's ladder wants: a strong analyst who skips it has no way to tell the 199
answer from the alternatives analytically, which is the intended trap.

## Findings, ranked

1. **Minor, non-blocking.** The FINAL_RECOMMENDATION narrative's rejected-alternative figure "the 138 that reading
   each workshop item against the reported scale scores gives" did not reproduce for the judge thread under either of
   two reasonable re-implementations of "read against reported scale scores" (it got 191 and 125 instead). This number
   is not a graded deliverable value (it appears only inside the main recommendation's own prose, as the value being
   rejected, not the committed figure), and it does not change any CRITICAL_COMPONENTS figure, any SOLUTION_STEPS
   figure, or any of the three deliverables' committed answers -- all of which reproduce exactly. It is worth the
   author double-checking the exact procedure the design note and the card's `analyst_test` intend for that one
   sentence (the card gives a specific per-grade breakdown for 138: 19, 31, 19, 18, 42, 9), since a mismatch there
   would weaken the stated analyst test's precision even though it does not touch determinism.
2. No other findings. All committed answers, all critical components, and the bank_import/pool_summary/memo figures
   reproduced exactly on independent recomputation from the shipped files, Gate G and Gate H classifications are
   mutually consistent across the thread, the design note, and the card, and the spec gates pass.

## Next action for the author

Optional only: re-derive the exact "reading each workshop item against the reported scale scores" procedure used to
get the design note's stated 138 (and the card's per-grade 19/31/19/18/42/9 breakdown) and confirm it against the
shipped files, or soften/remove the specific "138" figure from the FINAL_RECOMMENDATION narrative sentence if it
cannot be pinned exactly -- no rerun is required and no graded figure needs to change.
