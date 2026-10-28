# determinism-check report, task268, 2026-10-28

Architecture 4 (first judge pass on this architecture). Isolated judge thread ran against a fresh unzip of
`target.zip` at `/tmp/determinism-check-task268-1793229113/target/` plus the extracted `submission.md`
blocks only; it never saw `DESIGN_NOTE.md`, `metadata.json`, the generator or any prior report.

## Verdict
**NOT_DETERMINISTIC**
**Disposition:** SEND_BACK
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main recommendation (Mersey and Pennine, the five AY2025 frequencies, the 0.2 gap) and the Ask A
supplementary answer (cars on cover, COMP vs TPFT+TPO) both reproduce exactly and are uniquely forced: the
judge recomputed the back-test on accident year 2022 and confirmed only the notifying-route split (CMC vs
solicitor, via `claimant_representatives.csv`) clears the Standard's stated bound, while pooled, by-head and
by-notified-by all miss Wessex by 6.8-8.6%, well outside it. This is a clean, honest-data method-selection
stump (Gate G passes), and Gate H passes on the main call.

The block is Ask B, the 2026 claims baseline (injury vs. all-other). Solution step 6 silently dedupes an
"online journey opened and closed nil the day after" placeholder record against a later phoned-in claim for
the same policy/car/accident date/head of claim. No shipped file states this convention (not the Reserving
Standard, not the pilot thread, no data dictionary for the claims extract exists), and the judge could not
recover it exactly: after testing roughly eight reasonable dedup variants it got within 0-4 claims per cell
of the committed figures but never matched all twenty exactly. Worse, the Standard's own 2.1 states the
general rule literally as "every claim notified counts once, including claims closed without payment," which
argues for counting the abandoned record too, not dropping it, and produces a materially different, equally
defensible raw count (reported below). This fails Gate B (missing input data: the decisive dedup criterion
is not in any file) and Gate C/E (a textually-licensed alternative survives) for Ask B specifically. Per the
judge's global rule, a disqualifying defect on any one committed answer sinks the overall DETERMINISTIC
verdict even though the main call and Ask A are clean. Governing taxonomy label: `missing_input_data`
(with a secondary `competing_defensible_answer` on the Standard 2.1 reading).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Car-years 2025, private car, by region (Mersey/Pennine/Severn/Wessex/Fenland) | 61,924.81 / 40,568.81 / 47,215.47 / 38,108.96 / 23,927.05 | same, from `earned_exposure_2019_2025.xlsx` sheet "2025", product PC | yes |
| 2025 AY claims notified by 30 Sep 2026, by region | 5,297 / 2,991 / 3,713 / 2,681 / 1,374 | same, 16,056 total | yes |
| AY2022 back-test miss, pooled / head-of-claim / notified-by / by cover, Wessex | n/a (solution asserts "outside 2") | -8.5% / -7.8% / -6.8% / -8.6% | yes, and each fails the stated bound |
| AY2022 back-test miss, notifying-route split | within 1.1% | within 1.09% every region | yes |
| 2025 frequencies / pilot call | 8.9 / 8.2 / 8.0 / 7.3 / 5.9, gap 0.2 | 8.91 / 8.20 / 8.02 / 7.30 / 5.89, gap 0.2; naive pooled reading instead gives Mersey 8.85 / Severn 8.14 / Pennine 7.63 | yes (route split); naive reading confirmed as the real non-golden output, not an invented foil |
| Cars on cover 30 Sep 2026, COMP/TPFT+TPO, by region (Ask A) | Mersey 44,743/16,359; Pennine 30,213/9,882; Wessex 30,001/7,783; Fenland 19,421/4,246; Severn 36,590/10,367 | same, to the car, replaying `policy_changes_2025_2026.csv` onto `policy_vehicles_in_force_20260930.csv` | yes |
| Claims baseline 2026 accidents, injury/other, by region (Ask B) | Mersey 371/3,392; Pennine 164/1,889; Wessex 133/1,679; Fenland 61/901; Severn 205/2,339 | raw (no dedup, per Standard 2.1 literal): Mersey 398/3,541; Pennine 175/1,981; Wessex 147/1,763; Fenland 64/939; Severn 217/2,462. Closest dedup reconstruction: within 0-1 (injury), -4 to +3 (other) | no, not exact under any of ~8 tested rule variants; a defensible literal alternative (the raw count) also survives |

## Competing answers that survived
- **Ask B, claims-baseline dedup (SF16 in the design note's own fork table).** Golden reading: drop an
  abandoned-online-journey placeholder closed nil the day after a phoned-in claim for the same
  policy/car/accident date/head. Alternative, textually licensed by Standard 2.1 ("every claim notified
  counts once, including claims closed without payment"): count every notified row, no dedup. The two give
  materially different figures (raw count 7-10% above the committed figures region by region) and no shipped
  file states the specific supersession/dedup criterion that would close the fork. This fork is open.
- No other fork survived: the main call's SF1-SF15 forks (reproduced by the judge from the design note's own
  closure table, though the judge did not see that note) all converged, and Ask A's attribute-vintage fork
  closed cleanly on the change log.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / formats / large file | 10+ files, 3+ formats, one file 25,000+ rows | 11 files; csv/xlsx/pdf/txt (4 formats); `motor_claims_notified_2019_2026.csv` 138,245 rows, `policy_vehicles_in_force_20260930.csv` 248,648 rows | Pass |
| Distractors named, unlabeled | metadata.json names 2+, no filename labels one | `telematics_supplier_quote_2026.pdf`, `aggregator_quote_volumes_2025_26.xlsx`; neither filename says "distractor" | Pass |
| Distractor relevance / one reproduces arithmetically, ruled out by a shipped fact | each distractor used-but-ruled-out, relevant enough to weigh | Supplier quote (device pricing, volume tiers, take-up rates) and aggregator report (monthly quotes/sales/premium by region) are both genuinely relevant to a 2027 telematics pilot decision and plausibly temptingly load-bearing, but neither reproduces a graded figure arithmetically (aggregator's monthly sales counts, e.g. Pennine 1,517-1,891/month, do not coincide with any committed quantity); design note confirms deleting both leaves every golden figure unchanged (`checks.py` GATE) | Partial — relevance and non-use confirmed; the stronger "reproduces arithmetically, ruled out by a shipped fact" sub-clause is not demonstrated by either distractor |
| 1-3 deliverables, all present in golden, no format family required | required | 2 deliverables (`telematics_pilot_regions_2027.xlsx`, `.pptx`), both present under `golden/` | Pass |
| Asks multi-dimensional, unit+rounding stated | required | pilot-regions ask (5 regions + gap, 1 decimal), cars-on-cover ask (5x2, whole cars), claims-baseline ask (5x2, whole claims); units and rounding stated in the prompt's last sentence | Pass on shape; Ask B's grain is the open fork above |
| Prompt shape identifiable, rubric 25+ criteria | required | prompt shape identifiable (ranked-slate-under-cap, two regions capped from five); no rubric file is shipped inside `target.zip` or the task folder for this pass to inspect, so this half is not independently verifiable here | Not verifiable from the bundle |
| Nothing LLM-generated, goldens read as real work product | required | judge's hygiene check: PASS, no LLM tells, realistic warehouse-export texture (mixed UTC/local timestamps, legacy CL references, a long-tail closed-nil duplicate pattern) | Pass |

## Gate G reconciliation
Thread: `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`,
`surface_read_dependency: no`, `sole_data_defect: no`. Thread's Gate H line: `domain: pass`, `layers: pass`,
`decisive_step: analytical` (scoped to the main call only, correctly, per the judge system prompt's binding
rule that H3 is about the main call).

Design note / card: Gate G label `method_or_model_selection` (drawn and relabeled explicitly in the design
note's Draw section, replacing a withdrawn `forecasting` label); card `stump_class: analytical`;
`analyst_test` names the same default-path failure (region's own/pooled/head-of-claim/notified-by
developments all land Mersey and Severn) and the same decisive split (firm type via the representatives
register) that the thread independently derived; `domain_test` names the same field mechanism (report-lag
development on claim-count triangles, validated against closed accident years, the lag carried by notifying
route) that the thread's H1/H3 lines name.

**No mismatch.** The thread's classification of the main call lines up point for point with the design
note's own ladder and pre-ship check: same mechanism, same stump_class, same decisive step, same easy route
and its wrong answer (Mersey and Severn). This is a clean, landable Gate G/H call on the main recommendation;
the method-selection-on-honest-data shape is the library's textbook route here and not a surface-read
rejection. The only finding is Ask B's data-completeness gap (above), which sits outside the main call's
Gate H scope but still sinks the overall DETERMINISTIC verdict via Gates B/C/E on a committed answer.

## Stump power (Gate F)
The judge rates the main-call trap as strong: a model that applies the Reserving Standard's literal §3.2
instruction (the whole book's factors) without running the mandatory §3.3 back-test will confidently file
Mersey and Severn; only a model that notices the CMC-vs-solicitor notification-lag confound and back-tests
per §3.3 lands on Mersey and Pennine. No lever needed on the main call. Design note corroborates: six
candidate groupings (pooled, by head, by notified-by, by representative, region-level) all converge on
Mersey and Severn and all fail the 2022 back-test by 6.8-8.6%; only route-by-firm-type and its variants pass
within 1.1% and all print the same golden figures.

## Findings, ranked
1. **Ask B dedup rule is unshipped and not uniquely recoverable (Gate B/C/E, `missing_input_data`).** The
   "online journey opened and closed nil the day after" supersession convention that step 6 depends on
   appears in no shipped file; Standard 2.1's literal text argues for the opposite (count every notified
   row). This is the blocking finding and drives SEND_BACK.
2. **Distractor arithmetic-reproduction sub-clause not demonstrated.** Both distractors are relevant and
   confirmed unused, but neither visibly reproduces a graded quantity that a shipped fact then rules out;
   this is a minor spec-gate gap, not a determinism defect, and does not by itself block shipping.
3. **Rubric not inspectable from this bundle.** No rubric artifact ships inside `target.zip` or the visible
   task folder for this pass to check against the 25-criteria floor; flagged as unverified, not failing.

## Next action for the author
Close Ask B's open fork at the WHAT, not the HOW: either ship the operative online-claims-journey
counting/supersession convention as an input file (e.g., a short claims-ops note, or a flag column on the
claims extract distinguishing a superseded online placeholder from a genuine closed-nil claim) so the dedup
is forced rather than inferred, or drop the claims-baseline ask's grain to the raw Standard-2.1 notified
count (no dedup), leaving the main recommendation, its stump, and the Ask A cars-on-cover figures frozen.
Either repair changes what solvers see on Ask B and requires a rerun; re-judge once in `/fix-determinism`.
