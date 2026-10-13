# leak check, task122

**Verdict: REVIEW.** 16 files read, 8 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: chronic, decisive, recovery, change, decision, window, protocol, diuretics, pattern, fitted, record, clinical, client, graded, method, laboratory, carried, patient, repeat, reflex, readable, asserted, second, estimator, domain

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `VMK-4410-202_protocol_v3.0.pdf`: carries 5 of 7 distinctive words of the committed call: "Take VMK-4410 20 mg into the phase 3: after 36 months' treatment eGFR would be 3 mL/min/1.73 m2 higher on it than on pla"
- **REVIEW** `VMK-4410-301_synopsis_draft_v0.3.pdf`: carries 4 of 7 distinctive words of the committed call: "Take VMK-4410 20 mg into the phase 3: after 36 months' treatment eGFR would be 3 mL/min/1.73 m2 higher on it than on pla"

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `VMK-4410-202_SAP_v2.0.pdf`: 6 of 25 stump-paragraph terms appear (change, protocol, laboratory, patient, repeat, second); read whether the document names the move
- **REVIEW** `VMK-4410-202_protocol_v3.0.pdf`: 11 of 25 stump-paragraph terms appear (chronic, change, window, protocol, diuretics, record); read whether the document names the move
- **REVIEW** `VMK-4410-301_synopsis_draft_v0.3.pdf`: 9 of 25 stump-paragraph terms appear (chronic, change, window, diuretics, clinical, laboratory); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (second read, on the pack after the stage-4 fixes)

1. Decisive step: the 301 synopsis (VMK-4410-301_synopsis_draft_v0.3.pdf) says the dose is "the VMK-4410 dose from VMK-4410-202 expected to give the largest difference from placebo in this trial's primary end point, the change in eGFR from baseline to the month-36 visit". The estimand sentence adds "in all randomised patients as randomised, as if each patient had stayed on the assigned treatment: values from samples taken after a patient has stopped study drug permanently are set aside, and values during a temporary interruption are used." Nothing says how to get from a 52-week study to month 36. No sentence names the projection step.

2. No file ranks or scores the doses on eGFR at 36 months. The SAP only describes a week-52 MMRM, and the data are raw SDTM-style tables.

3. None. Everything is a plausible protocol, SAP, lab manual, data dictionary, sites list or draft synopsis. The manifest and data dictionary are normal data-handover items.

4. None. No figure or name reads as the answer.

5. Literal sentences:
- Synopsis estimand: "the difference between VMK-4410 and placebo in the mean change in eGFR from baseline to the month-36 visit (week 156), in all randomised patients as randomised, as if each patient had stayed on the assigned treatment". This gives all randomised patients (about 750) by randomised arm, outcome change in eGFR from baseline, at week 156, each dose against placebo, with post-permanent-stop values set aside and interruption values kept.
- "Baseline is the mean of the screening and day-1 values" (synopsis; also SAP section 2 and protocol section 9). "Values are analysed under the scheduled visit under which they were collected. If a scheduled visit has more than one central value for a test, the value from the first sample is used" (SAP section 2).
- eGFR is "the central laboratory's CKD-EPI 2021 values as reported" (SAP section 3).
- "The month-36 visit takes place while patients are taking study drug."
No filed sentence names a method, model, slope, knot or time window for the 36-month projection. The data stop at week 56, so the projection is open. The estimand is also hypothetical ("as if each patient had stayed on assigned treatment"), which is not the same as the on-treatment values observed.

6. In my judgement the decision turns on an analytical choice: how to project the dose differences from 52 weeks to 36 months. That includes the early acute eGFR dip versus the longer-term slope, the dose-response, and what to do about informative dropout and permanent stops. The synopsis and the protocol background ("lower eGFR in the first weeks ... a fall that reverses when treatment stops") hint at this, but the choice is not filed. Reading fields correctly is a necessary but separate layer: Madrid mg/dL versus Copenhagen umol/L, haemolysed potassium, local versus central labs, partial AE dates, visit relabelling and first-sample rules. Those clean-up steps do not decide the call alone. The asks (potassium, AEs, discontinuations, exposure) are mostly rule application of the SAP definitions.

7. Realism: nothing placeholder-like or impossible found. The one small oddity is the contact "vmk4410-202@tavlund-lab.example" (lab manual Cover, a deliberate .example domain). Other mild tells:
- Arm sizes are very even (149, 150, 150, 150, 151; 750 randomised), plausible for 1:1:1:1:1 blocks.
- dm.csv shows round-number site counts and a neat 50 sites.
- The 412 screen failures are tidy against 1,162 consented.
- dm.csv RANDDTC equals RFXSTDTC and the last dose falls in the planned week.
- The protocol and SAP are very short (2 to 3 pages) for a real phase 2b.

## Solver's-eye read (first read, before the stage-4 fixes)

1. None. No file or sentence says how to get from a 52-week trial to a 36-month dose difference. The nearest text is the synopsis estimand: "the difference between VMK-4410 and placebo in the mean change in eGFR from baseline to the month-36 visit (week 156), in all randomised patients as randomised, as if each patient had stayed on the assigned treatment: values from samples taken after a patient has stopped study drug permanently are set aside, and values during a temporary interruption are used." That fixes the target quantity. It says nothing about how to project to 36 months.

2. None. No file ranks or scores the doses on the eGFR difference at 36 months. The data are raw SDTM-style tables (lb, dm, ex, ds). The SAP only describes a week-52 MMRM.

3. None. Every file is something a sponsor would hold: protocol, SAP, lab manual, data dictionary, sites list, manifest, a phase 3 synopsis draft and the raw tables. The synopsis and the lab manual's eGFR sheet are context, not hints.

4. None. The prompt's "four doses" and "36 months" are context. The only dose-specific text is the synopsis line that the dose is "expected to give the largest difference from placebo in the primary end point", and it names no dose. The synopsis's primary end point is eGFR, while the protocol and SAP primary is UACR. The sponsor's two documents do not agree on what "primary" means.

5. Sentences that fix population, outcome, window and comparison:
- Synopsis estimand (quoted above). Literal execution gives the population (all randomised, analysed as randomised), the outcome (change in eGFR from baseline), the time point (week 156 and a projected one), the comparison (each dose against placebo), and the handling (post-permanent-stop values excluded, interruption values kept).
- SAP: "Baseline eGFR is the mean of the screening and day-1 central values; when one is missing, the other is used." and "If a scheduled visit has more than one central value for a test, the value from the first sample is used." and "eGFR analyses use the central laboratory's CKD-EPI 2021 values as reported."
- SAP: "values from samples taken after a patient has stopped study drug permanently are not used".
- SAP: "the day-1 sample is taken before the first dose and is a baseline value".
No filed sentence names a method, model, slope, knot or time window for the 36-month projection. The data stop at week 52, with a week-56 follow-up. The synopsis says the month-36 visit is on treatment. The protocol notes an early eGFR fall that reverses on stopping. So the projection method is left entirely to the analyst. The definitions behind the four spreadsheet asks (potassium above 5.5, treatment-emergent AEs, exposure) are fully stated in SAP sections 4 to 6.

6. An analytical choice decides it. Nothing is a field reading or a rule to follow on the main call. The solver has to choose how to extrapolate from 52-week data to 36 months. That means separating an early haemodynamic dip from the chronic slope, deciding how to use the off-treatment week-56 values, and handling informative dropouts after permanent stop. No file decides it. The closest framing sentence is the synopsis estimand and its remark that the month-36 visit is on treatment. The asks (potassium, AE, stops, exposure) turn on SAP definitions and on data semantics, not on analysis. Examples are the Madrid mg/dL creatinine, local labs mixed into lb.csv, mEq/L potassium, and partial AE dates.

7. Little looks generated. Arm sizes are 149 to 151 (near-equal, but consistent with 1:1:1:1:1 block randomisation, so plausible). Every one of the 50 sites is CLOSED, with an activation date, and site size ranges from 0 to 47. Laboratory row counts are identical across CREAT, GLUC, K and SODIUM (10,553 each). That is plausible for a panel, but a real export would show a few missing tests. Hub units are mixed (umol/L against mg/dL), as in the lab manual. The lab contact address uses the ".example" domain and the sponsor, drug and lab names are fictional. The "VMK-4410-301_synopsis_draft_v0.3" is dated 5 October 2026, a plausible date. Overall nothing is placeholder-like.

## Rulings

- Sweep 3 and sweep 4 REVIEW lines: harmless (the study's own nouns, the disease's name, the visit windows and the twelve-week background-therapy clause); answered in the design note.
- First read, question 4: the synopsis's 'primary end point' could be read as the phase 2b's UACR end point; fixed, the sentence now names this trial's primary end point, the change in eGFR from baseline to the month-36 visit.
- First read, question 7: identical test counts across the chemistry panel; fixed, potassium rechecks are requested as a renal panel or a full panel.
- Second read, question 7: even arm sizes, fifty sites, short protocol and SAP: harmless (block randomisation gives near-equal arms; the protocol says about 50 sites; the documents are the sponsor's handover copies of the sections the extract relies on).
