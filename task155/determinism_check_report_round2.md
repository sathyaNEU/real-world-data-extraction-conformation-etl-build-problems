# Determinism verdict, task155 (re-judge after repair, judged fresh)

**Verdict:** DETERMINISTIC (main call forced; two supplementary tables rest on unstated counting conventions, see Fork S1 and S2).

**Disposition:** FIX_NOW. The main call, the stump and the data stay byte-identical. The repair is one pin in the call-in module notes (or the prompt's asking sentence) on how a shift is counted once and when a fill counts as cover, plus softening the two magnitudes in solution step 4. No model rerun on the main call.

## Why
The literal reading of the standard (sections 3, 4, 5) is: forecast, per store, the paid hours of its open shifts that call-ins leave unfilled, with all eight stores posting at 09:00 on 16 Nov, then place the crew at the largest and report that store's open paid hours. The package contains every input to do this (open lines in christmas_roster_2026_published.xlsx, module rules in kws_callin_module_notes.pdf, availability JSON, rosters, payroll history, 142k historical offers). Executing the module over the Christmas rosters with an acceptance model fitted to the offer history puts Camberwell first by a wide margin (about 580 to 640 hours against 230 or less for any other store) in every adjacency-aware model I tried. Camberwell's new weekday 10:00 to 16:00 shift (M10, 127 shifts, trading plan note "online picking 10:00 to 16:00 weekdays") has a median of 7 and a mean of 5.2 available, non-overlapping casuals per shift, and 4% of shifts have a casual rostered to carry on from. The only way to get another answer is to leave out the carry-on effect, which the history shows is large (34% against 4%). No taxonomy label applies to the main call.

## Evidence (recomputed from the bundle)
| Item | Result | Source |
|---|---|---|
| Open paid hours by store | Werribee 3,254.0; Box Hill 2,602.0; Altona 1,770.0; Camberwell 1,092.5; Ringwood 1,140.0; Sunshine 1,378.0; Ballarat 876.0; Williamstown 641.5. Reproduced. | christmas_roster_2026_published.xlsx, Status=OPEN, "Paid hrs" |
| Crew hours at Camberwell | 1,092.5, which is 1,090 to the nearest 10. Reproduced. Paid hours already net the 30 minute break (M10 is 5.5). | roster xlsx; EA pdf |
| Critical component 1 | Reproduced exactly: 2,152 offers continue the casual's own same-store shift; 33.6% accepted against 4.2% of the other 139,847. Join is roster lines, less lines vacated by ABS/LVE, plus call-ins already accepted before the offer, by person code to payroll number through previous_employee_no. | callin_offers, both roster exports, register, people, payroll |
| Critical component 2 | Reproduced in direction. Share of open shifts with at least one available, non-overlapping casual who is continuing from a same-store shift: Werribee 100%, Box Hill 100%, Altona 85%, Camberwell 2%. The golden says 100, 96, 79 and 2; my version leaves out the hours caps. | availability JSON, roster xlsx |
| Critical component 3 | 215 open shifts, 1,090 hours. Reproduced. | roster xlsx |
| Expected unworked hours, my own simulation (12 runs each, offer order, eligibility, 60/20 minute response, 07:00 to 21:00 window, daily re-raise, shared West and East clusters, decline final) | Fitted logit with carry-on, other-shift-same-day and the other terms: Camberwell 580 against at most 228 for any other store. Logit with the filed terms: Camberwell 638, next Williamstown 234. Two-rate model (31.7% / 4.2%): Camberwell 580, Sunshine 335. Constant 4.66%: Werribee 686, Camberwell 572. No carry-on term (4.2%): Werribee 783, Camberwell 597. | work scripts in this scratch directory |
| Solution step 4 magnitudes | Not reproduced. The golden says Camberwell about 670 and Ringwood about 400. Mine gives about 580 to 640 for Camberwell and 175 to 225 for Ringwood. The ranking and the top store agree; the second-place store and the 400 do not. The shipped asks do not commit chart values. | simulation |

**Competing answers tested.**
- Werribee, the most open hours and the largest forecast under a constant or carry-on-blind acceptance rate. The history separates the candidates: acceptance depends strongly on carry-on (about 8 times), so a model without it misstates every store. Not defensible once the history is read.
- Werribee or Box Hill from last year's fill rate by store: Werribee had only 299 hours put out last year (RELIEF lines in the legacy export show a crew was there), and its Christmas 2026 N18 and A14 patterns are new, so history by store is not an estimate for it.
- Ranking by unfilled share instead of hours: Camberwell is also first on share.
- Crew capacity binding (25 x 38 x 4 = 3,800 h): not binding at any store, so it changes nothing.
- No hours-between-stores alternative reading of "crew hours": section 5 states paid hours of the placed store's open shifts. Forced.

**Supplementary tables (xlsx), recomputed.**
- Table 1 uncovered hours: all eight stores reproduce exactly (776.0, 1,221.5, 875.5, 672.0, 732.0, 944.0, 187.5, 754.5).
- Table 1 put-out and covered: seven stores reproduce exactly; Sunshine comes to 2,028.5 / 1,084.5 against the golden 2,023.0 / 1,079.0, one 5.5 hour shift I could not account for.
- Table 2: reproduces exactly for all fourteen figures once the duplicate pair of ABS call-ins described below is collapsed to one shift (four 5.5 hour cells: Box Hill, Williamstown, Ringwood and Werribee).

**Fork S1 (supplementary 1): what counts as "a shift put out" and as "covered".**
The golden counts a shift once even if a casual who took it then reports an absence and the store raises it again as an ABS call-in. The final state decides covered or uncovered. The module notes say the original call-in "keeps its FILLED outcome", and a literal reader can count the ABS call-in as a second shift put out. Altona gives put out 1,636.5, covered 860.5, uncovered 776.0 on the call-in-by-call-in reading, against the golden 1,615.0 / 839.0 / 776.0. Uncovered hours do not move; put-out and covered do. Nothing shipped states the golden's convention.

**Fork S2 (supplementary 2): what counts as "covered by".**
The golden excludes fills whose casual later reported the absence, and collapses two ABS call-ins that name the same absent payroll number on the same shift (callin_ids 2214166 and 2214167; 2217720 and 2217722; both filled by the same person at the same close time). Counting FILLED call-ins as written gives Altona 33.5 / 5.5 against the golden 29.5 / 0.0, Werribee 5.5 / 49.0 against 0.0 / 43.5, and so on. The sentence "hours of its call-ins covered" does not say that a fill that was then vacated is not cover.

## Files/Hygiene
**PASS.** 15 files; formats txt, csv, xlsx, json, pdf (five). Largest: callin_offers 141,999 rows, plus register 42,180 and rosters 79,643 / 108,481. Row counts in the transmittal match every file. Distractors: vic_school_terms_public_holidays csv, ea pdf rates table, christmas_trading_plan sales and customer columns, legacy "Hrs" as shift length. Layer 1 mess is authentic (UTC against store time, 12-hour clock legacy export against 24-hour KWS, re-engaged casuals with new employee numbers, cost-centre history for home store, VACANT/RELIEF/OPEN status words, ABS duplicates). Document properties are plausible (named authors and offices), no generator banners, no hidden sheets, no comments. Dates are consistent with the 12 Nov 2026 extract. No answer-bearing text: the trading-plan notes (online picking, to midnight) describe the new shift patterns only. Cross-batch fingerprint against delivered tasks not assessable from this isolated folder; nothing in the package shows a clone. No exclusion-level finding.

## Stump power (Gate F)
Strong, from analysis, not a defect. The carry-on structure has to be found by joining 142k offers to two roster exports, call-in bookings, vacated lines and payroll cost-centre history, and then used inside a simulation of the module. The easy route (store-level fill rates, or a simulation with one overall acceptance rate) is natural for a capable analyst who cleaned everything and read every rule, and it files Werribee (or Box Hill). The asks add work (shift identity, final status, home store by date). Risk to watch: a pool-size count (Camberwell's M10 has about 5 available casuals per shift) also lands on Camberwell without the carry-on finding, so the decisive step can be reached by a shorter path, but not by the fill-rate route.

## Stumping type (Gate G)
`mechanism: method_or_model_selection` (forecasting by simulation), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
No reported figure is wrong; on perfectly clean data the task still needs the fitted acceptance model and the simulation. The data separates the candidate models (a back-test against the historic open-line fill rates, or the 34% / 4% split itself, is available to the solver).

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: workforce supply and fill-rate forecasting, the field's own estimate (probability a call-in is accepted, expected unfilled hours); swap test fails to read the same with other nouns because the quantity is acceptance behaviour of casuals under a staffing system.
- Layer 1: UTC against store time, legacy against KWS export semantics (Hrs as length against paid hours), re-engaged employee numbers, cost-centre moves, duplicate ABS rows. Layer 2: estimating acceptance from history with the carry-on effect and simulating the module over the new Christmas shift patterns.
- Easy route: apply last year's or an overall acceptance rate and rank stores on expected unfilled hours, which gives Werribee (about 690 to 780 hours against Camberwell about 570 to 600).

## Fix
Location: input_files (data-dictionary pin) and solution. Specific changes:
1. In kws_callin_module_notes.pdf add one sentence: a shift is counted once however many call-ins it generates, and a fill that the casual later vacated by an absence is not cover (so a shift filled and then vacated counts as left uncovered unless the re-raise is filled), and two call-ins naming the same absent payroll number on the same shift are one shift. This closes Fork S1 and S2 with the golden's convention and moves no graded number.
2. In SOLUTION_STEPS step 4, replace "about 670" and "about 400 (Ringwood next)" with figures that reproduce, or say only that Camberwell is the largest; the golden's second-place store is not corroborated by an independent run.
3. Re-check Sunshine's put-out (2,023.0) and covered (1,079.0): an independent count gives 2,028.5 and 1,084.5 and the 5.5 hour difference is unexplained.
