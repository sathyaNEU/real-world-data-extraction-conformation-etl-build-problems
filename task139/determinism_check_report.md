# Verdict, task139 (Haverline ERN placement, AY2027 credit)

**Verdict:** NOT_DETERMINISTIC on one committed answer only (supplementary 3, "intakes reported in 2025"); the main recommendation and supplementary 1, 2 and 4 are DETERMINISTIC and reproduce. Taxonomy for the failing item: solution_incorrect (golden not reproducible from the files; nearest literal readings differ), with an underspecified intake count rule behind it.

**Disposition:** FIX_NOW. The main call, stump, and every figure in the placement stay frozen. The author must identify the filter behind 1,537/822/939/708/1,356/770/1,109/666 and either pin it in claims_data_dictionary.xlsx (a definition of "intake" that fixes the count) or regenerate the block to the literal count. If the pin changes what solvers see in the claims extract, rerun. No model rerun is needed if only the dictionary line and golden block change.

## Why
The decision is forced: the memo (pick memo item 2, 4, 5) defines the credit per intake taken, the charter fixes team size, 7,300 place-days, the place-day count rule, the cap of 3 per unit and the fill rule, so the 17 teams land 3/3/3/3/3 in HC-SS, MF-SS, MF-OT, CN-OT, HC-OT, 2 in RW-SS, 0 in RW-OT and CN-SS, total about $4.1M, on every reasonable reading I tried. The one committed answer that fails is supplementary 3: the literal count (charter 4.1 and dictionary `time_off_at_report = Y`, report_date in 2025) gives 1,621/856/991/734/1,442/812/1,178/700, a second defensible rule (also requiring disability_began on or before report_date, which every pilot intake satisfies) gives 1,546/827/947/710/1,362/773/1,118/669, and the golden 1,537/822/939/708/1,356/770/1,109/666 matches neither.

## Evidence (recomputed from the shipped files)
| Item | Result | Source |
|---|---|---|
| Pilot intakes 5,227 (2,613 ERN, 2,614 usual), all matched to claims extract on legacy number, segments via crosswalk agree 100% | reproduced | assignments xlsx, claims extract, crosswalk |
| Paid indemnity (claim_type IND) 4,339 | reproduced | claims extract |
| Share paid ERN/UH: HC-SS 64.9/86.6, RW-SS 57.5/83.9, MF-SS 68.1/86.7 | reproduced | same |
| KPA workbook: 1,600 claims, 100 per stratum, total $9,747,283.11, claim number matches register once the control digit is dropped (100%) | reproduced | KPA xlsx, PDF 5.1 |
| Saving per assigned intake: HC-SS 857, RW-SS 741, MF-SS 889 (HC-OT 1,006; RW-OT 853; MF-OT 1,163; CN-SS 426; CN-OT 1,618) | reproduced | KPA means x paid shares |
| Place-days per ERN intake after normalising nurse-typed claim refs (all 2,647 rows map to ERN register), both days counted, reopenings added: HC-SS 21.40, RW-SS 18.85, MF-SS 23.03, HC-OT 38.31, RW-OT 47.64, MF-OT 40.05, CN-SS 26.12, CN-OT 59.31 | reproduced | case log, charter 5.3, 5.2 |
| Team-year savings (7,300 x saving / place-days): 292,364; 286,892; 281,996; 191,656; 130,715; 212,070; 118,890; 199,174, rounding to the golden 290/290/280/190/130/210/120/200 thousand | reproduced | |
| RW-SS fill: 944 intakes (Oct 2025 to Sep 2026) x 18.85 / 7,300 = 2.44 | reproduced (944 is the literal `Y` count) | claims extract |
| Placement and total: 4,105,564 unrounded, 4,090,000 from rounded team values, both round to $4.1M | reproduced | |
| Supp 4 payments: amount counted once per payment (it repeats on each weekly line), excluding VOID lines and EFT payments returned in the ACH file (they were reissued by check): 3,724,903; 4,652,050; 1,805,107; 3,992,890; 4,276,854; 5,232,875; 4,999,081; 7,281,913, all match the golden at $1,000 | reproduced exactly | payments csv, ACH returns, dictionary |
| Supp 3 intakes reported 2025 | NOT reproduced (see Why) | claims extract |

**Robustness of the main call.** RW-SS needs 1,162 intakes a year for a third team; every window I tried (calendar 2025 literal 991, golden 939, Oct-Sep 944, annualised 2026 about 907, historical max 1,028) fills 2.3 to 2.56 teams, so 2 is forced. All other units clear three teams by a wide margin (fill 4.1 to 5.7). Greedy order by team-year saving with the cap and fill rule gives the stated 17. Without the plus-one-day rule team values shift (HC-SS about $307k), but the charter 5.3 fixes it, so not a fork. The superseded draft v3 charter (16 to 18 teams, two nurses a team, 1 February start) is overruled by the signed charter and is a declared-style distractor, not a fork.

**Remaining forks (non-fatal).**
- Supp 4: summing lines (6.73M HC-SS) against payment amount (3.72M). The dictionary calls `amount` the "Payment amount", and the ACH return amounts equal the single repeated amount, so the payment-level reading is supported by two shipped facts, but a solver who treats each line as a week's benefit gets a different, unflagged answer. Accept, with the dictionary line for `amount` worth tightening ("amount repeats on each line of a payment").
- Supp 3 internal inconsistency: the main call uses the plain `Y` count for Oct 2025 to Sep 2026 (944), the supplement uses some stricter, undocumented filter for 2025. The extra filter (disability_began after report_date on `Y` rows) bites only on pre-upgrade rows, which looks like a legacy-flag mess but nothing in the files says to drop those rows.
- The golden-to-literal gap of about 45 intakes beyond the dates rule I could not explain with any filter I tested (weekends, holidays, lag caps, status, office/legacy letter, injury year).

## Files/Hygiene
PASS, no exclusion-level finding. 15 files, formats csv, xlsx, pdf, docx. Two files above 25,000 rows (claims extract 59,789; payments 63,135). Distractors available: draft charter v3 (docx), staffing plan, worker survey, ACH returns, KPA PDF restatements. Provenance and dates are coherent (extract 30 Sep 2026, charter signed 19 Oct 2026, memo 28 Oct 2026, staffing plan 30 Oct 2026; pilot files as of 2025). Real mess is authentic Layer 1: legacy against 2025 segment codes, control digit on KPA claim numbers, nurse-typed claim refs (case, spacing, missing zeros), MM/DD/YYYY dates, void and reissued checks, returned EFTs. Minor: memo cites plan Exhibits 3 and 4 that are not shipped (not decisive). Cross-batch fingerprint: I cannot compare to other tasks (isolated); no near-duplicate observed internally.

## Stump power (Gate F)
Moderate to good. The trap that does the work is the estimand: the KPA sample is drawn only from claims that paid indemnity, so differencing the sampled group means (the per-verified-claim saving) discards the nurses' effect on whether an intake pays at all, shrinking HC-SS, RW-SS and MF-SS savings (means differ only 133, 109, 229 dollars) and dropping them down the ranking. A second layer is capacity (place-days per intake, fill cap on RW-SS). Risk of being too easy: pick memo item 2 states the estimand nearly literally ("what those intakes would pay"), so a solver who reads it closely lands on the per-intake route; the rubric weight rests on the asks (payment-level amount, ACH reissue, intake rule), which are semantics-heavy.

## Stumping type (Gate G)
`mechanism: binding_constraint` (with estimand/unit-of-analysis choice), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The KPA workbook and register numbers are fine; the difficulty is choosing the intention-to-treat per-intake estimand over the post-selection per-claim difference and then applying the unit fill cap. On clean data the task would still stump.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical` (borderline toward rule_application because memo item 2 states the estimand).
Layer 1 is the legacy/2025 coding, control-digit and typed-reference joins, void/returned payments. Layer 2 is the actuarial estimate of the programme credit from a randomised pilot with a stratified-on-outcome verification sample (post-treatment selection) and capacity-constrained placement. Swap test: replacing indemnity and claims with another field's nouns breaks it (the credit is an ultimate-loss estimate from a randomised trial), so it passes. Easy route a strong analyst who cleaned everything would take: rank segments on the difference of KPA mean verified indemnity per sampled claim (ERN against usual), giving HC-SS, RW-SS and MF-SS much smaller team values and a different placement (not recomputed in full here); the golden, placing three teams in the strain units, defeats it.

## Fix
- Location: solution plus a dictionary pin (input_files only for a one-line definition, no data changes). Supplementary 3: state exactly which rule produces the 2025 intake counts and pin it, or regenerate the numbers as 1,621/856/991/734/1,442/812/1,178/700 if the literal rule is intended; make the main call's step 6 and supplement 3 use the same intake definition.
- Optional: tighten the `amount` field note in claims_data_dictionary.xlsx for supplement 4 so the payment-level count is not left to inference.
- Main recommendation, placement, savings and total need no change.

## Disposition

FIX_NOW applied on 2026-10-15 in one generator pass, `freeze.py` snapshot taken first; the call (the placement and the
$4,100,000 credit), the stump and the ladder are frozen and `freeze.py check` passes in rubric and in determinism mode:
no graded figure moved.

- **Supplementary 3, the intake rule.** The filter behind 1,537/822/939/708/1,356/770/1,109/666 is charter 4.1's intake
  (a first report recording time lost) with the parallel run's second listings counted once. It is the organisation's
  own definition, and the converted claims' flag is the legacy LOST_TIME indicator, so it is filed as a WHAT in
  `claims_data_dictionary.xlsx`: `time_off_at_report` is "Y when the first report of injury records time lost from work
  (disability_began on or before report_date). On claims converted at the 2 June 2025 upgrade the field holds the legacy
  LOST_TIME indicator, which the legacy system set to Y for any claim with time lost on record."; the extract's file row
  adds "A first report received in the parallel run of 29 May to 1 June 2025 and keyed in both systems is listed twice,
  converted under its legacy number and again under its new number, the two rows carrying the same office, segment,
  class_code, injury_date, report_date and disability_began." The counts do not move. `checks.py` and `verify.py`
  execute the dictionary literally on their own code paths and land on them (62 pairs one to one, the four converted
  claims of those days with no new-number twin counted as listed); the rival readings each miss: the flag as filed
  (1,621/856/991/734/1,442/812/1,178/700), both listings kept (1,546/827/947/710/1,362/773/1,118/669), the strict dates
  (37 to 124 low), every converted claim of the parallel run dropped (HC-SS, MF-SS, CN-SS low) and a dedup on the six
  fields across the year (3 to 34 low). The call and supplementary 3 now read one definition: every row reported October
  2025 to September 2026 is a new-system row whose flag equals its dates, so the fill check's 944 for RW-SS is the
  filed definition's count (asserted).
- **Supplementary 4.** `amount` is "Amount of the payment, US dollars, repeated on each line of the payment."; the line
  sum misses every segment (1.66 to 1.86 times), asserted. VOID reads "voided before it was cashed", each of the 85
  replaced by a new check for the same claim, benefit, payee, period and amount. The returned EFTs are closed by the
  bank's return file: each return item sits on one register EFT by trace number, 271 of the 275 paid again by such a
  check and the other four returned on 29 September 2026; kept, a benefit period is paid twice.
- **The decisive step's borderline.** Pick memo paragraph 2 named no estimator, sample, reweighting or zero handling, but
  restated the credit as "what those intakes would pay with their adjusters alone, less what they pay with a team". It
  now states the credit once: "The credit is the ultimate indemnity that the accident year 2027 intakes the teams take
  will not pay because the teams took them." The counterfactual is charter 4.2's (an intake no team takes stays with its
  adjuster); no method is named.
- **Realism, figure-neutral.** The review workbook's references are workpaper sections B1 to B8 with item numbers in the
  blind order the files were worked (no group signal, asserted), its remarks vary in form, date style and rate by sheet;
  the memo carries the reference PR-2026-041. The control digit stays: it sits on the call's join of the review to the
  register.
- **Changed under `target/`:** `claims_data_dictionary.xlsx`, `ay2027_indemnity_pick_ern_credit.pdf`,
  `kpa_ern_indemnity_verification_2026-06-30.xlsx` (the targeted re-read); every other file byte-identical. Outside it,
  the golden workbook's Notes line on 2025 intakes and the write-up's steps 3 and 6 follow the filed text.
- **Owed.** The one re-judge. The filing makes Ask 1's two devices seen, so `precut.py` is red on the ask sheet (pair
  ceiling 58.2, mirror leakage 54 per cent, the cracker lands Ask 1); an Ask 1 rework is owed before ship.
