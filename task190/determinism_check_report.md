# task190 determinism judge report (second pass, repaired pack)

**Order kept.** The full independent derivation was computed from the 17 shipped members alone and
written to `/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/task190_derivation.md`
before `task190_graded_blocks.md` was opened. Nothing in the repository was read except this brief's
pack. The derivation reached **Metal and metal-bearing wastes, 56.6 per cent against 59.5 per cent, a
2.9 point shortfall** independently, and reached every supplementary figure independently as well.

- **Verdict:** DETERMINISTIC
- **Disposition:** FIX_NOW. Three note-level pins (below); no graded figure moves and the main
  recommendation needs no rerun.
- **Gate G:** `mechanism: statistical_rigor`, `stumping_family: analytical_non_defect`,
  `surface_read_dependency: no`, `sole_data_defect: no`. No reported number in the pack is misleading:
  the register tonnages and the survey arisings are both correct and both used as they stand. The
  difficulty is judging a correctly computed rate against its target with the sampling uncertainty the
  design actually implies, which is a FINE-numbers shape (statistical rigor, with a
  method-selection face), so banned_stumping_type does not apply.
- **Gate H:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. The field's own analysis is
  the precision of a stratified survey estimate of national arisings, tested against a plan target: the
  denominator is a Business Waste Survey estimate for the whole frame, the numerator a movement-register
  census, and stratum E1 (250+ employees, 155 of 155, compulsory, full response, selection without
  replacement in the other three bands) is a complete enumeration that holds 95.8 per cent of metal's
  arisings and therefore contributes zero sampling variance. The easy route a strong analyst who read
  every field and rule correctly still takes: compute the same correct 56.6 per cent and test it with a
  variance that ignores the finite-population correction and the census stratum, which raises metal's CV
  from 1.12 to 5.38 per cent, puts the upper bound at 62.6 per cent, and files **"no stream is
  established below target at the 95 per cent level"**, a hold, or ranks on raw shortfall and files
  **Mixed commercial and industrial wastes, 4.9 points**.

## Gate table

| Gate | Result | The number or quotation that decides it |
|---|---|---|
| A, solution correct | PASS | Every graded figure reproduced from the files, independently and before the blocks were opened: metal 70,384 t recovered / 124,354 t arising / 56.5996 per cent / shortfall 2.9004 points / SE 0.6347 / 4.569 SEs; interval 55.355 to 57.845 -> 55.4 to 57.8; mixed_ci 4.900 points at 1.4523 SEs -> 1.45; all eight rows of the attainment sheet; all 32 stage-chain cells and all 24 pass-through rates (metal 77,384 despatched, 75,682 confirmed at a final operation, 62.2 / 97.8 / 93.0 per cent); the five field-day rows (32.54, 25.69, 29.80, 10.11, 7.66 and 16.53, 14.83, 14.43, 16.42, 15.01); all eight 2025 tonnages (metal 67,709); all five municipal rows (Norte gap 3,075 t, 2.6 per cent). Grain honoured: 6,130 onward legs excluded (their `producer_permit` is a facility permit, `APA-F...`), 1,630 usable returns counted once per case rather than 1,634 log rows, 133 field visits rather than 610 visit rows. Nothing failed to reproduce. |
| B, decisive facts shipped | PASS | The estimand is stated word for word in `collection_capacity_note_2027.pdf`: "the tonnage of that stream despatched by its producer during the 2026 calendar year and confirmed received at a recovery operation, counted once at the producer's despatch leg, over the total tonnage of that stream arising during 2026 at every enterprise in the Business Waste Survey frame whether sampled or not". Targets: `national_waste_management_plan_targets.pdf` Annex II Table 4. Design: `bws_2026_design_and_weighting.pdf` sections 2 and 3. Operation kinds and the interim rule: `treatment_operation_codes.xlsx`, Notes ("the later operation is confirmed on the consignment the holding site forwards"). The design PDF references an Annex A (frame activity classes) and the plan PDF an Annex I (stream definitions); neither ships and neither is needed, because the numerator is not restricted to frame members and the stream mapping ships as `waste_code_crosswalk.csv`. |
| C, uniquely forced | PASS, one thin closure | Eight forks enumerated and each closed, with what each computes to, in the derivation. The decisive two: variance with the FPC and the census stratum gives metal at 4.57 SEs and nothing else past 1.45, while ignoring the FPC gives no stream at all; one-sided (1.645) and two-sided (1.96) both give metal and only metal, so that unpinned choice is closed by the data. Including the onward legs gives metal 72.3 per cent and no shortfall anywhere; counting R13 as a recovery operation still gives metal but a 1.4 point shortfall, and is foreclosed by the operation list's own `operation_kind` of "interim". The margin is thin-but-clean: 2.9 points is 4.57 standard errors of the only estimated input. **Thin closure:** on supplementary ask A the design PDF's "with the field days attributed to the contact" reads, literally, as licensing a row sum, which gives Alentejo 55.57 days against only 13 dated visits of at most one day each. The row sum is arithmetically impossible, not merely worse, so the visit grain is forced, but it is forced by inference rather than by a stated sentence. Pin it. |
| D, hardness not semantics | PASS | The split between the committed answer and the easy answer is a variance estimator on a stated design (complete enumeration, simple random selection "without replacement", frame N per stratum), not a reading of a word. No prompt term carries the fork. |
| E, prompt unambiguous on the decision | PASS, two soft spots | The prompt commits to one stream, "by how many points", and fixes unit and rounding in the asking sentence. Soft spot 1: "the rate and its interval" with "at the 95 per cent level" leaves one-sided against two-sided unstated; the deliverable's whisker forces a two-sided interval and the blocks report it, and the call is the same either way. Soft spot 2: "a sheet of each stream's tonnage and pass through rate by chain stage" never names the stages, so a solver could decompose despatch / receipt / confirmation instead of the golden's arising / despatched / confirmed at a final operation / confirmed at a recovery operation, and lose 56 graded cells on a defensible alternative. Name the stages in the prompt. |
| F, stump power | STRONG | Three live traps, all on correct reported numbers: the no-FPC variance (files a hold), ranking on raw shortfall (files mixed_ci at 4.9 points), and counting the 6,130 onward facility despatch legs (files no shortfall at all). A capable solver that cleans h2's renamed columns, chases every R13 through its forwarded child and gets 56.6 per cent exactly right still fails on the variance step. No methodology checklist, no documented defect, no public dataset whose published finding is the answer. |
| G, stumping type | PASS | See the Gate G line above. The clean-data test: on perfectly clean data the census-stratum variance reasoning is untouched, so `sole_data_defect: no`. |
| H, three rules | PASS | See the Gate H line above. Layer 1: h2 renames all eleven columns (`consignment_ref`, `leg_kind`, `ewc_code`, `net_tonnes`, `treatment_op`, `parent_ref`), the 1 July 2026 reissue of both the operation list and the waste code list (`15 01 06` -> `15 01 06*`), two municipalities reporting in 100kg, 71 field-log rows in hours against 6,023 in days, a visit's days replicated on every case row, one exactly duplicated crosswalk row, five `Associacao de Municipios` bodies on the returns side with no counterpart on the receipts side, and a superseded preliminary release. Layer 2: the 95 per cent test on a ratio whose denominator is a stratified survey estimate with one completely enumerated stratum. |

## The five repairs, tested

1. **Can any shipped number still verify the variance method, in either direction?** No, and the repair
   holds. The only precision figure in the pack is `waste_statistics_2025_release.pdf`'s "the coefficient
   of variation of that estimated national total in the 2025 round is 3.4 per cent": a different round,
   whose micro-data does not ship, so it cannot be recomputed either way. Residual soft hint only: the
   2026 round's national CV is 3.91 per cent with the FPC and 4.48 per cent without, so a solver who
   treats 3.4 per cent as a continuity check is nudged, weakly, toward the correct method. That nudges
   nobody to the wrong answer and it verifies nothing. If the author wants it airtight, quote the CV for
   the activity-class publication domain instead of the national total.
2. **Does the published table's stated reason hold, and can an adjustment be read out of it?**
   **The reason does NOT hold.** Table 1 of `waste_statistics_2025_release.pdf` publishes 308,695 t
   recovered in 2025 "as extracted on 30 June 2026", and explains the gap with "The register goes on
   receiving treatment confirmations for consignments despatched in earlier reference years, and the
   published series is not revised for them." The shipped `waste_movement_legs_2025.csv` holds **no leg
   of any kind after 2026-03-09** and its maximum receipt-to-confirmation lag is **48 days** (median 3),
   so a 30 June 2026 extract would have contained every confirmation in the file and the published
   column should equal the recomputation. It does not: the register gives 320,991 t, 3.37 to 5.22 per
   cent higher stream by stream. No adjustment can be read out of it, which is the one consolation: the
   per-stream gaps carry no constant ratio, and no basis reproduces the published column (direct-recovery
   only 224,801 t; all despatch legs 316,539 t; receipt-year basis 223,793 t; a 2025-12-31 confirmation
   cut 309,456 t, the nearest, still off by -317 to +531 t per stream). So it is not a leak and it does
   not fork ask B, which the memo pins ("we take that out of the register on the same basis as 2026"),
   but the artifact misstates its own provenance and a diligent solver who notices will doubt a correct
   basis. **This is the one repair that did not land.**
3. **Is the new unit convention a convention, and is it load-bearing?** A convention, and load-bearing
   for one ask only. `bws_2026_design_and_weighting.pdf` section 5: "The division books field work in
   field days of eight hours, and a team records the time a contact took in the unit shown in the log's
   time_unit column." That fixes a unit, not a method. It bites on the 71 hour-unit rows, all Alentejo
   field visits; unconverted, Alentejo reads 80.88 field days against 13 dated visits, which is
   self-refuting. It touches nothing on the main call.
4. **Does the recomputed supplementary figure reproduce and tie to the stated counts?** Yes. The 2025
   column (metal 67,709; mixed_ci 89,749; paper 30,516; wood 19,243; cd_rubble 91,788; glass 12,868;
   plastic 7,368; textile 1,750; total 320,991 t) reproduces exactly on the memo's stated basis, from
   20,898 root 2025 despatches resolving 16,895 recovery / 3,302 disposal / 701 unconfirmed, the same
   root-only chain-resolved basis as 2026.
5. **Does any shipped sentence, read literally, make the easy answer correct?** None on the main call.
   The design PDF states the complete enumeration, the compulsory full response and the selection
   "without replacement" as facts about the design, and never states a variance formula, so it files the
   WHAT and not the HOW. The memo's "counted once at the producer's despatch leg" forecloses the onward
   legs, and "No calibration or post-stratification is applied" forecloses a weighting fork. The single
   sentence that points literally at a wrong figure is the design PDF's "with the field days attributed
   to the contact", and it governs ask A, not the call.
6. **Dates and pile-ups.** Clean. No negative leg lag anywhere; the last leg in the 2026 files is
   2027-01-30 with 13 legs, against a stated register extract of 31 January 2027, so nothing piles onto
   the extract date; h1 despatches end 2026-09-22 and h2 begin 2026-07-01 with no duplicated
   consignment-leg pair; all 20,622 municipal receipt dates and all 384 return months sit inside 2026;
   PDF and workbook metadata carry in-fiction dates and authors only. One realism miss, not a date
   error: the 730 never-confirmed 2026 roots are spread evenly over all twelve months (51 to 72 a month)
   while the confirmation lag is at most 48 days, so they read as random missingness rather than the
   censoring a 31 January 2027 extract would produce.

## Files and hygiene

FAIL, not exclusion-level. 17 files, 3 formats (12 csv, 4 pdf, 1 xlsx), largest
`waste_movement_legs_2025.csv` at 80,104 rows. Distractors present and genuinely weighable:
`hazardous_export_notifications_2026.csv` (131,240 t notified under R1/R4/R5, absent from the register),
`carrier_permit_vehicle_log_2026.csv`, `enterprise_permit_crosswalk.csv`, and the five
`Associacao de Municipios` returns. No README, no authoring or benchmark disclosure, no tool banner, no
synthetic self-description; metadata is in-fiction and temporally coherent. Three findings:

1. `waste_statistics_2025_release.pdf` against `waste_movement_legs_2025.csv`: the stated extract date
   and the stated reason for the gap are contradicted by the register (repair 2 above). Temporal and
   internal coherence.
2. **Generator tidiness.** Five of the eight 2026 rates land on an exact tenth with zeros beyond
   (56.5996, 59.5999, 49.8999, 43.7000, 60.2000), seven of the eight pass-through rates do the same
   (97.001, 92.999, 55.004), and all 24 root tonnage cells are exact integers although individual
   despatch legs carry two decimals. That reads as solved-backwards rather than extracted, and it is an
   LLM-generation tell under the hygiene check. Named files: `bws_2026_microdata.csv`,
   `waste_movement_legs_2026_h1.csv` and `_h2.csv`.
3. The uniform month profile of the 730 unconfirmed roots, above.

None of the three gives away the answer or changes what a trap does, so none is a send-back.

## Fix

`input_files` and `prompt`, three pins, none of which moves a graded figure on the main call:

1. **`waste_statistics_2025_release.pdf` / `waste_movement_legs_2025.csv`.** Make the stated reason true.
   Preferred: give the 2025 register a realistic long tail so that confirmations after 30 June 2026
   account for the 12,296 t gap (which also fixes finding 3's cousin in the 2026 files). Do not instead
   regenerate the published column to equal the register at a stated cut: that would reconcile the table
   and thereby confirm the roots-only chain basis to any solver who checks.
2. **`bws_2026_design_and_weighting.pdf` section 5.** Add one clause stating that a field visit's days
   are recorded on each case the visit covered, so the visit grain is pinned by a sentence instead of by
   the arithmetic impossibility of the row sum. This closes the only literal reading in the pack that
   points at a wrong number.
3. **`prompt.txt`.** Name the chain stages in the sheet request (arising, despatched, confirmed at a
   final operation, confirmed at a recovery operation), so a defensible alternative decomposition cannot
   cost a solver 56 graded cells.

If fix 2 or 3 is made, the ask-A and stage-sheet cells change what solvers see, so make both before any
testing round. Neither touches the main recommendation, its interval, its shortfall or the stump.
