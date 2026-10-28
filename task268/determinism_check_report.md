# determinism-check report, task268, 2026-10-28

Re-judge after pass6's send-back. Pass6 (`determinism_check_report_pass6.md`) found the main call and the
cars-on-cover ask uniquely forced, and sent the build back on a second ask, the 2026 claims baseline. That ask
has been retired from `prompt.txt`, `submission.md` and the goldens; the ask layer is now the private cars on
cover on 30 September 2026 by region and by cover (COMP, TPFT, TPO). The main call and its figures are
unchanged. This pass judges the repaired bundle end to end, isolated thread spawned fresh on a clean unzip of
the current `target.zip`.

## Verdict
**DETERMINISTIC**
**Disposition:** APPROVE — every load-bearing figure reproduced exactly from the shipped files; no repair,
no rerun.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect,
surface_read_dependency: no, sole_data_defect: no

## Why
The judge thread reproduced the main call (Mersey + Pennine) and every cars-on-cover figure independently from
a fresh unzip, seeing only the prompt text and the shipped bundle. The deciding mechanism is the Motor
Reserving Standard's own mandated back-test (clause 3.3, within two per cent): the whole-book pooled
development, a by-head-of-claim split, and the literal `notified_by` field split each miss accident year 2022
in Wessex (8.54%, 7.85%, 6.78% respectively), so the Standard itself disqualifies them; only the development
split by notifying route (claims-management company, joined through `claimant_representatives.csv`'s
`firm_type`, versus everyone else) clears every region (max miss 1.09%, matching Critical Component 4's
"within 1.1 per cent" verbatim). That route split reproduces the stated 2025 frequencies (8.9 / 8.2 / 8.0 /
7.3 / 5.9) and the 0.2 Pennine–Severn gap to the digit, while every naive method the thread tried (pooled,
by-head, literal `notified_by`, binary representative/non-representative, by cover) ranks Severn above
Pennine — the Mersey + Severn pairing the golden explicitly names and rejects. The cars-on-cover ask (the
repaired ask layer) reproduced to the exact car for all five regions and all three cover types once the
vehicle-in-force snapshot was overlaid with each policy's latest mid-term ADDRESS/COVER change effective by
30 September 2026, and once the claims-notification timestamps were read as UTC and converted to UK local
time before dating. No gate A–E failure found.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Car-years earned 2025, private car (5 regions) | Mersey 61,924.81; Pennine 40,568.81; Severn 47,215.47; Wessex 38,108.96; Fenland 23,927.05 | same, from `earned_exposure_2019_2025.xlsx` | yes |
| Claims from 2025 accidents notified by 30 Sep 2026 (5 regions) | Mersey 5,297; Pennine 2,991; Severn 3,713; Wessex 2,681; Fenland 1,374 | same, `motor_claims_notified_2019_2026.csv` joined to region via `postcode_district_sales_regions.csv`, UTC→UK-local date | yes |
| AY2022 back-test miss, Wessex, by method | pooled/head/`notified_by` "miss ... by 6.8 to 8.5 per cent"; route split "within 1.1 per cent" | pooled 8.54%, by-head 7.85%, literal `notified_by` 6.78%, by-route 1.09% | yes |
| Route development factors | CMC 3.7, Solicitor 1.2 | CMC 3.687≈3.7, Solicitor 1.174≈1.2 | yes |
| AY2025 frequency per 100 car-years (5 regions) | 8.9 / 8.2 / 8.0 / 7.3 / 5.9 | 8.909 / 8.200 / 8.017 / 7.301 / 5.887 → same roundings | yes |
| Gap, Pennine to Severn | 0.2 | 0.184 → 0.2 | yes |
| Cars on cover 30 Sep 2026 by region × cover (15 cells) | as in Critical Component 3 / ask 4 | same to the exact car, vehicle-in-force rows overlaid with latest mid-term change ≤ cutoff | yes |

A second, independently-constructed valid route split (binary is_CMC vs. everyone else, collapsing the
solicitor category) also clears the 2% back-test (max 1.01%) and converges on materially the same rounded
answer (8.9/8.2/8.0/7.3/5.9, gap 0.2), which rules out a knife-edge dependency on one arbitrary partition of
the representative population.

## Competing answers that survived
None. Every naive AY2025 projection the thread tried (pooled, by-head-of-claim, literal `notified_by`, binary
representative/non-representative, by cover) ranks Severn above Pennine and files Mersey + Severn — the wrong
pair the golden names and rejects — but none of them survives the Standard's own clause 3.3 back-test, so none
is defensible. No fork on the cars-on-cover ask: vehicle rows are read literally (on/off/cancelled dates;
multiple concurrently-on-cover rows per policy are genuine multi-vehicle policies, not a join artifact), and
the ADDRESS/COVER overlay from `policy_changes_2025_2026.csv` is forced by the prompt's "as at 30 September
2026" and the vehicle file's own stale term-start snapshot.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | ≥10 | 11 shipped files | yes |
| Format mix | ≥3 formats | csv ×5, xlsx ×2, pdf ×3, txt ×1 = 4 formats | yes |
| Large file | ≥1 file ≥25,000 rows | `motor_claims_notified_2019_2026.csv` 137,580 rows; `policy_vehicles_in_force_20260930.csv` 248,648 rows; `policy_changes_2025_2026.csv` 32,264 rows | yes |
| Distractors named | `metadata.json` names ≥2, no filename labels one | `telematics_supplier_quote_2026.pdf`, `aggregator_quote_volumes_2025_26.xlsx`, neither filename says "distractor" | yes |
| Distractor relevance/unused | unused by solution, relevant enough to weigh; one reproduces a graded quantity and a shipped fact rules it out | both unused in the route-development or cars-on-cover computation; `aggregator_quote_volumes_2025_26.xlsx` tempts a naive "most demand" read (quotes/clicks/sales by region) toward a different region ranking, but it is new-business quote volume, not the in-force vehicle stock the cars-on-cover ask and the frequency's car-year denominator require, so the vehicle-in-force and exposure files rule it out structurally rather than by one coincident arithmetic match | partial — relevance and non-use confirmed; no distractor figure was found to reproduce a graded quantity arithmetically before being ruled out by a shipped fact |
| Deliverables | 1–3, all present in golden, no format family required | 2: `telematics_pilot_regions_2027.xlsx`, `telematics_pilot_regions_2027.pptx`, both in `golden/` | yes |
| Asks multi-dimensional | not stacked lookups; unit + rounding stated | frequency (5 regions + gap, one decimal) and cars-on-cover (5 regions × 3 covers, whole cars) stated in the prompt's closing sentence | yes |
| Prompt shape / rubric ≥25 criteria | identifiable shape, rubric ≥25 criteria | prompt shape (claims-frequency-severity, actuarial) is identifiable; no rubric artifact is present in the task folder for this pass to recount directly | not independently checked this pass — no rubric file in `task268/` to recompute against; flagging for the author to confirm at the regular rubric gate, not a determinism finding |
| Realism / not LLM-generated | nothing reads LLM-authored; goldens read as real work product | judge's hygiene pass: Reserving Standard's v3→v4 versioning note, informal email cross-talk in `telematics_pilot_thread.txt`, mixed legacy/new claims-system references read as genuine operational artifacts; no benchmark/authoring disclosure, no placeholder names | yes |

## Gate G reconciliation
Judge: `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`,
`surface_read_dependency: no`, `sole_data_defect: no`. Gate H: `domain: pass`, `layers: pass`,
`decisive_step: analytical`.

Design note's `## Three rules` (card `stump_class: analytical`): Layer 2 is named
`field_method, own:claim-count-development-by-notifying-route`, the basis chosen by the Standard's own
out-of-sample back-test, with "no decoy" and "no certified replay" both asserted — no shipped figure is itself
a frequency, ultimate count, or development factor that could be reproduced by replay. `analyst_test` names
the exact easy route (pooled, by-head, or by-`notified_by` development → Mersey and Severn) and `domain_test`
names the field's own completion-by-development-with-back-test method as the deciding quantity. This matches
the judge's classification point for point: the judge independently discovered the same three failing naive
splits (pooled, by-head, literal `notified_by`) and the same passing route split, with misses (8.54/7.85/6.78
vs. 1.09 per cent) that match the design note's own figures (8.54, 7.85, 6.78 vs. "within 1.1 per cent") to
two decimal places. No mismatch: the judge did not name either declared distractor as a surface read carrying
the task, and the design note likewise asserts no decoy and no certified replay. This is the library's own
textbook route (claims-development-by-report-lag-factor, validated by a governing standard's back-test) that
a strong analyst applying the field's standard method would still take the easy way and get wrong — a
landable call under `stumping` 1.3, not a planted trap. The main thread should weigh it as such against the
design note's ladder, but nothing here signals a send-back.

## Stump power (Gate F)
The judge's assessment: the pilot terms and the Reserving Standard both describe the general mechanics of
development and back-testing, but neither names "split by notifying route" or "claims-management company" as
the required grouping. A model has to run the mandated back-test itself, discover that the obvious whole-book,
by-head, or by-field development fails it, and then search for and find the one split (joined through
`claimant_representatives.csv`) that passes. A model that computes a pooled or by-head development factor and
stops — the natural "list the Standard's steps and apply them" route — files Mersey + Severn, the wrong pair.
This is a genuine out-of-sample-validated method-selection trap on honest, correctly-reported data, consistent
with the design note's `analyst_test`, and it is the field's own standard analytical move (claims development
completed by report-lag factor, validated against a closed year) rather than a reflex to distrust a stated
number. Two independently-constructed valid splits converge on the same rounded answer, which also rules out
the task collapsing to a knife-edge arbitrary partition.

## Findings, ranked
1. (informational, not a send-back) The spec-gate distractor check is partially unconfirmed: neither
   `telematics_supplier_quote_2026.pdf` nor `aggregator_quote_volumes_2025_26.xlsx` was found to reproduce a
   graded quantity arithmetically before being ruled out by a shipped fact; both are relevant-but-unused by
   file type and subject matter rather than by a near-miss number. Worth a author glance at the next regular
   hygiene pass, not a determinism defect.
2. (informational) No rubric artifact exists in `task268/` for this pass to recount against the "≥25
   criteria" gate; flag for the regular rubric check, not raised here as a determinism finding.
3. No Gate A–H finding. No competing answer survives for the main call or the cars-on-cover ask. No
   Gate G or Gate H mismatch between the judge and the design note.

## Next action for the author
None required for determinism. Ship: record the portal result in the ledger and mark the card's
`mechanism`/`stumping_family` fields (currently `None`) with the judge's values
(`method_or_model_selection` / `analytical_non_defect`) to keep the card current with this pass's verdict.
