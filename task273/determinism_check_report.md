# determinism-check report, task273, 2026-10-28

Re-judge of architecture 4 after the first pass's SEND_BACK (Gate H/stump-family rework). The prior pass
is kept separately as `determinism_check_report_a4_pass1.md`, which the judge thread run for this pass
never saw (isolated scratch unzip only, no task-folder access).

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call (14 conditions, +SACS/SLC26A2/TMEM216) is forced by a depth/detection-probability-corrected
("Horvitz-Thompson-style") carrier-frequency estimator, pinned by the methods report's own stated,
phase-specific calling thresholds (phase 1: >=5 alt reads and >=25%; phase 2: >=3 and >=20%) and the
member-level depth file. The judge thread independently rebuilt this estimator from
`ags_phase1_calls_grch37.tsv`, `ags_phase2_calls_grch38.tsv`, `ags_register_site_depth_2026-11-03.csv`
and `kgl_variant_register_2026-11-03.xlsx` and reproduced the full 30-condition table, including
SACS/SLC26A2/TMEM216 at 7/6/6 per 1,000 and the 14-vs-16 split at the panel's 5-per-1,000 line. It also
independently reproduced the four rejected-method numbers the narrative cites as wrong routes (naive
calls-over-cohort gives ~3.78/3.46/3.42, matching the stated 3.8/3.4/3.5), confirming the "easy route"
wrong answer (11 conditions, no joiners) is real, not a strawman. Cohort size (25,694) and the CFTR
half-year couple counts (88/98) both reproduce only once two documented, discoverable file behaviors are
read correctly (a consent-withdrawal effective date after the census, and a classification column that
silently carries a site's current rather than as-of-authorisation class from the August-2025 LIMS release)
-- both are facts stated or recoverable in the shipped files themselves, not external knowledge.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Reference cohort | 25,694 (7,945 + 17,749) | 25,694, only after correcting for in-force-on-census-date consent (22 members) | Yes |
| SACS carrier frequency | 7 /1,000 | 6.81 -> 7 (depth-weighted estimator) | Yes |
| SLC26A2 carrier frequency | 6 /1,000 | 6.13 -> 6 | Yes |
| TMEM216 carrier frequency | 6 /1,000 | 6.20 -> 6 | Yes |
| Full 30-condition table / 14-16 split | per submission | matches to rounded per-1,000 for all 30; HEXA=4.34 excluded, SLC26A2=6.13 included | Yes |
| Rejected "calls over cohort" (narrative) | 3.8/3.4/3.5 | 3.78/3.46/3.42 | Yes |
| CFTR couples told, H1/H2 2025/26 | 88 / 98 | 88 / 98, only after correcting the results export's classification field against the variant register's change history (naive export reading gives 87/86) | Yes |
| Narrative's depth-filtered (>=10/>=20 reads) and "pooled" rejected-method figures | stated in FINAL_RECOMMENDATION prose | not reproduced to the exact stated values after several attempts | Not independently confirmed (narrative only, not a graded Critical Component or Supplementary Answer) |

The one unreproduced item is explanatory narrative inside the main-call prose (the illustrative rejected
alternatives), not a Critical Component or a graded Supplementary Answer, so it does not affect the
verdict; worth a look only if the write-up prose is revisited for its own sake.

## Competing answers that survived
None. The 11-condition (no-join) answer only arises from not correcting for the documented depth-dependent
ascertainment bias, which the shipped methods report and depth file make a computation error, not a
licensed alternative reading of "carries." No fork in the main call or in either supplementary answer
survived the judge thread's stress test; the margin at the panel line is comfortable (sensitivity to
floor/ceil rounding in the binomial model moves every figure by <=0.003 per 1,000) and not a knife-edge.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | >=10 | 11 shipped files | Pass |
| Format mix | >=3 formats | csv, tsv, pdf, xlsx (4) | Pass |
| Large file | >=1 file with >=25,000 rows or large DB | `ags_member_register_2026-11-03.csv` (25,997 rows), `ags_register_site_depth_2026-11-03.csv` (25,864 rows) | Pass |
| Distractors named, not labelled | metadata.json names >=2, no filename labels one | `ccsp_referrals_2023-2026.csv`, `kgl_ccsp_turnaround_2025-26.csv` named in `metadata.json`; neither filename says "distractor" | Pass |
| Distractor relevance/arithmetic-coincidence check | each distractor unused yet relevant; one answering a graded quantity reproduces arithmetically and is ruled out by a shipped fact | Both named distractors (referral volumes, lab turnaround times) are thematically relevant to the programme but neither numerically coincides with a graded quantity (carrier frequency or couple count); the design note's own "No decoy" section separately names the national-reference-panel frequencies (a field-level distractor inside the review context, declared at stage 2) as the item ruled out by the shipped depth data, not either named distractor file | Partial -- the two file-level distractors pass the relevance/unused test but neither is the arithmetic-coincidence item; that role is carried by an in-file distractor the design note documents separately. Not a blocking finding, flagged for visibility |
| Deliverables | 1-3, all present in golden, no required format family | 2 (`carrier_panel_review_2027-28.xlsx`, `panel_recommendation_2027-28.docx`), both present under `golden/` | Pass |
| Asks multi-dimensional, unit+rounding stated | not stacked lookups | Ask 1 is condition x frequency x panel-status (30 rows), rounding to nearest whole stated in the prompt; ask 2 is condition x half-year couple counts, a count needing no rounding | Pass |
| Prompt shape + rubric >=25 criteria | shape identifiable | Card records shape `07`, decision_type `designation_set`; rubric itself is generated by the grading pipeline and is not shipped inside the task folder, so criterion count could not be directly verified here | Not independently verifiable from this folder; no finding raised |
| Not LLM-generated, goldens realistic | — | Judge thread hygiene check: PASS, no LLM-authorship tells, no provenance/benchmark disclosures, temporal coherence held (LIMS classification-field shift lands consistently at Aug 2025 across genes, reading as a real system artifact) | Pass |

## Gate G reconciliation
The judge thread's classification (`mechanism: method_or_model_selection`, `stumping_family:
analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`) matches the card's own
`gate_g: "method_or_model_selection"` exactly, and matches the design note's "Not semantics" / "Not rule
application" / "No decoy" lines: the three rejected-method readings are real, computable constructions on
clean data (not a planted defect), no file ranks or pre-states the conditions' frequencies for the solver
to catch-and-reject, and the policy files only the population, outcome, unit and threshold line, leaving
the estimator choice open and data-settled. There is no mismatch between the thread's surface-read
reading and the design note's declared distractor: the thread correctly did not name either declared
distractor file (referrals, turnaround) as carrying the main call, and the national-reference-panel
frequencies the design note calls out as the actual declared decoy are refuted by the depth data rather
than treated as the surface read the solver must reject -- consistent with a FINE-numbers,
method-selection stump, not surface-read-rejection.

## Gate H reconciliation
Thread: `domain: pass`, `layers: pass`, `decisive_step: analytical`. Card: `stump_class: analytical`, with
`analyst_test` describing the exact easy route (counting calls among members read >=10 times, filing the
current 11 conditions unchanged and missing SACS/TMEM216/SLC26A2 at ~2.3/2.4/2.1 per 1,000) and
`domain_test` naming the binomial detection-probability structure as the field-specific quantity that a
domain swap would destroy. These align point for point: the thread's named "easy route" (naive calls over
cohort, giving 3.8/3.4/3.5 and the 11-condition answer) is a different but equally valid naive route from
the card's depth-filter route, and both are explicitly enumerated and rejected in the design note's "Not
semantics" paragraph (both naive families, among others, are itemized with their numbers). No instance of
the thread naming the declared distractor as the surface read carrying the task; the decisive step is
squarely the choice of detection-probability-weighted estimator, which both the card and the thread treat
as analysis rather than rule application or data semantics. No reconciliation mismatch found.

## Findings, ranked
1. (Informational, non-blocking) The spec-gate's arithmetic-coincidence distractor requirement is
   satisfied by an in-file distractor (national reference panel frequencies inside the review context)
   documented in the design note, not by either file named in `metadata.json`'s `distractor_files`.
   Visible for the author's awareness; does not affect the determinism verdict, disposition, or either
   gate classification.
2. (Informational, non-blocking) Two of FINAL_RECOMMENDATION's illustrative rejected-method figures (the
   depth-filtered >=10/>=20-read numbers and the "pooled" numbers) were not independently reproduced to
   their exact stated values by the judge thread after several attempts. These are explanatory narrative,
   not a Critical Component or a graded Supplementary Answer, so this is not a SOLUTION_WRONG finding;
   worth a look only if the write-up prose is revisited.

## Next action for the author
None required for shipping; the task is DETERMINISTIC, APPROVE. If the write-up is touched again for any
other reason, re-verify the two narrative-only rejected-method figures in finding 2 against the generator's
exact construction.
