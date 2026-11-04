# determinism-check report, task314, 2026-11-04

## Verdict
NOT_DETERMINISTIC (narrow: one supplementary column, the tank-fill counts in ask 2; the main call and every other graded figure are forced)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, sonnet, medium, scratch /tmp/determinism-check-task314-r1/ (verdict.md, derivation.md). The thread kept the order (derivation written before it opened the graded blocks) and matched every graded figure. The brief was written by the fallback path (no Agent tool in my runtime) and the thread was spawned by the main session.

## Why
The main call is analytical and forced by the data. The whole-bill price explains both past rate changes (elasticity -0.32 from the 2023 restructuring alone, -0.32 from the Fenwick USD 14.00 charge alone). The marginal block price explains neither well (-0.05 on the 2023 change, about zero once both prices are in one regression). So C > B > A, savings 30 / 20 / 10, gap 10, on 4,341 accounts and 772.1 AF of baseline. The failure is `underspecified_objective` on one column: no prompt sentence or shipped file defines a tank fill, so three counts compete (see the fork below).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Eligible accounts (W10, REBILL stands, billed all eight Jun-Sep months 2025-26) | 4,341 | 4,341 | yes (cis_water_bills, bill_date month; Plan 5.3) |
| Baseline | about 770 AF | 772.1 AF | yes |
| Elasticity, whole-bill price | -0.28 (-0.27 to -0.32) | -0.315 all data, -0.320 event 1 only, -0.322 Fenwick only; simple DiD -0.26 | yes within band; DiD sits 0.01 outside |
| Fenwick use change / price change | -4.6% / +18.5% | confirmed, ln ratio -0.28 | yes |
| Option C / B / A, AF | 30 / 20 / 10 | 32.5-33.0 / 21.4-21.7 / 8.9-9.0 (at -0.28: 28.8 / 19.0 / 7.9) | yes, same bins |
| Gap C-B | 10 | 11.3 (9.9 at -0.28) | yes, 10 under every log-form estimate -0.2 to -0.4 |
| Fill station water, kgal Jun-Sep | 678 / 717 / 630 / 682 | 677,943 / 717,127 / 629,773 / 682,170 gal | yes (bay meter span; raw row sums and the Corvane report double count 121 resumed Bay 2 records) |
| Tank fills Jun-Sep | 244 / 258 / 229 / 240 | same under "each tank, resumed session once" | only under that reading (fork below) |
| Facility use, AF Jun-Sep | 22.6 / 29.7 / 31.2 / 23.7 | 22.564 / 29.693 / 31.214 (31.225) / 23.711 (23.700) | yes |

## Competing answers that survived
1. **Tank fill (ask 2, 4 cells). The only surviving fork.** Jun / Jul / Aug / Sep:
   - one per record: 280 / 285 / 259 / 268;
   - the golden's count (one per tank, resumed session once): 244 / 258 / 229 / 240;
   - one per truck-and-trailer visit, resume merged: about 212 / 229 / 199 / 214.
   
   All 4 tank-fill cells move under either alternative. The 8 water and facility cells do not.
   - **Resumed session.** The data rule out counting it as two fills. The resumed record's meter_start equals the earlier record's meter_start and its gallons are cumulative (121 pairs, all Bay 2). So the record count is closed by the meter pattern, not by a sentence.
   - **Trailer.** Nothing rules out the visit count. The trailer pair is the same card, 1 to 6 minutes later, with continuous meter on the same bay (25 / 21 / 24 / 21) or overlapping on the other bay (7 / 8 / 6 / 5). Counting it as a second tank is an inference, not a filed rule.
   - **Would a pin close it?** A pin that names the trailer as its own tank (for example "one tank fill for each tank filled, a truck's and its trailer's each") closes the visit reading. It should leave the resumed session to the meter pattern, because a resumed record is the same tank, so a tank count does not add it. The record count is then already ruled out by the data. This closes the fork without stating the resumed-session device, and it files the WHAT (the unit) rather than the HOW. The residual risk is a literal reader who treats "fill" as an event rather than a tank. Naming "tank" in the pin and keeping the register pattern as the only evidence for the resume covers it. The pin must not mention registers or sessions.
2. **Functional form of the elasticity on Option C** (see Findings 3). It is open only in combination with the full-panel estimate. It is a risk on a main-call graded figure, not a fork the files settle.
3. Closed by the files: premise instead of account (4,800 / 856.5 AF gives C 36.5, which would bin to 40) is ruled out by Plan 5.3 "accounts". The pool meter (excluding it gives 22.6 / 29.7 / 31.2 / 23.7; including it gives 23.8 / 30.3 / 32.1 / 24.1) is forced by the read data, though no file states the plumbing. The marginal-price reading (A 6.7, B 3.3, C 0.0 at -0.05, so A first with the gap rounding to 0) is ruled out by the data, not by a sentence.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 4 (csv x8, xlsx x3, pdf x5, docx x1) | yes |
| Large file | 25,000 rows or more | cis_water_bills 276,883 rows (42 MB) | yes |
| Distractors named | 2 or more, no file name labels one | 3 in metadata.json (bvw03 weather, state_pws_water_use, conservation_rebates); `wrong_basis_distractors` empty; no file name labels one | yes |
| Distractor behaviour | unused by the solution, relevant enough to weigh, none answers a graded quantity | none enters a figure; the thread found the Fenwick and city rebates track each other with no confound; the state table's 5,213 Ardley connections against 6,698 SF accounts has no effect | yes (weather and rebates weigh; the state table is thin) |
| Deliverables | 1 to 3, all in the golden, no format family required | 3 (xlsx, docx, png), all present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | savings, gap, fill kgal, fills, facility AF, each with unit and rounding in the sentence; the fills have a unit gap (the fork) | partial: the tank-fill unit is unstated |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 07 grid of cells; the note estimates about 26 (not generated here) | yes, margin of 1 |
| Prompt form | under 1,000 characters, one paragraph | 906 characters | yes |
| Hygiene | nothing reads as LLM generated | thread found no authoring or benchmark language; dates consistent (agenda draft 2026-10-27, accounts 2026-11-02, bills to 2026-10-29) | yes |
| Golden realism | goldens read as real work products | the three files exist; I did not open them for realism | not checked here |

## Gate G reconciliation
Thread: `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
Card (`gate_g`, `stump_class`): `method_or_model_selection`, analytical. This matches, so it is not the finding that predicts a send-back.

Declared distractors (weather, state table, rebates) are not named by the thread as the surface read, and `wrong_basis_distractors` is empty, so nothing is too load-bearing.

**Gate G line:** mechanism method_or_model_selection = card; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no. Reconciled.

**Gate H line (thread):** domain pass, layers pass, decisive_step analytical.
Card: `stump_class: analytical`, `analyst_test` and `domain_test` consistent. Reconciled.

Two differences are worth recording; neither moves a verdict:
- **The default path's elasticity.** The card and note put the marginal-price elasticity from the 2023 restructuring at -0.12 (A 15.9, B 7.9, C 0). The thread estimates -0.05 (A 6.7, B 3.3). Both rank A first, so the default path still ends on the wrong answer. The easy-route figure (about 16 AF against about 7 AF) is estimator-dependent.
- **The back-test claim.** The note's readability row says the marginal-price model "fits" the 2023 restructuring and "nothing in the textbook route's own checks refutes it". The thread found the 2023 change alone prefers the whole-bill price (-0.32 against -0.05). See Gate F.

## Stump power (Gate F)
The thread rated stump power good on the main call: the standard block-tariff route, the marginal price from the 2023 restructuring, gives A and fails for an analytical reason (the choice and validation of the response variable). It reached the average-price reading by regression: it fitted the two prices against each other on the 2023 change and again on the Fenwick change, and got the same whole-bill answer from either event. It did not rely on the Fenwick comparison alone.

Weighing this against the builder's flag, without re-judging:
- A solver who applies an average-price response by reflex lands C with no test. This is already recorded in the note's ladder ("the whole-bill price assumed", checked in `checks.py`).
- The thread also shows a solver who runs one two-price regression on the 2023 change lands C without needing the Fenwick test.
- So the Fenwick comparison is confirmatory and not strictly needed. The stump rests on a solver adopting the marginal price untested. The note's claim that the restructuring's own fit supports the block price is not borne out by the thread's regression.
- The thread did not class the decisive step as landable by the field's standard method. It classed it analytical, because the textbook reflex is the marginal price.
- The main thread should weigh this against the ladder: the pair-on-the-call risk rises if capable solvers test both prices.

## Findings, ranked
1. **Tank-fill fork (ask 2, 4 cells).** FIX_NOW: pin the unit in the asking sentence (trailer a tank of its own; the resume left to the meter pattern). Data, figures and goldens stay unchanged.
2. **Elasticity mismatch (-0.28 submitted, -0.315 to -0.32 judge).**
   - The thread's point estimates (-0.315, -0.320, -0.322) sit inside the stated -0.27 to -0.32 band. Its simple DiD (-0.26) is 0.01 outside the band's low end.
   - The submission's own figures reproduce by the method each names:
     - Step 3: -4.6% use against +18.5% price gives ln ratio -0.28.
     - 4,341 accounts and about 770 AF (772.1) reproduce.
     - The savings 30 / 20 / 10 and the gap 10 reproduce, 28.8 / 19.0 / 7.9 at -0.28 and 32.5-33.0 / 21.4-21.7 / 8.9-9.0 at the full-panel estimate. All land in the same 10 AF bins.
   - **No written figure fails to reproduce.** The only item is the stated band, slightly narrower than the full set of estimates the thread tried (down to -0.26).
3. **Functional form on Option C (main-call graded figure).**
   - Constant-elasticity (log) form gives 32.95 AF at -0.32, 2.05 below the 35 edge (it flips at -0.340). The linear form q1 = q0(1 + e x %dP) gives 36.7 AF at -0.32, which rounds to 40. B (23.0), A (10.8) and the gap (13.7) stay in their bins.
   - At the golden's own -0.28 the linear form gives about 32 (scaled from the thread's 36.7), still 30. So the exposure is the full-panel estimate combined with the linear form: linear reaches 35 once e is about -0.305 or stronger.
   - **Is it an open fork?** Yes, as a risk on one main-call figure: no file filed says log or linear. The three savings and the gap can round differently for a solver who estimates -0.31 to -0.32 and applies it linearly. It does not move the ranking, the runner-up, or any other figure. It would not by itself make the file NOT_DETERMINISTIC if the golden's estimate is accepted, but it is a competing answer on a graded figure.
   - **Would converging it in the data close it without filing a method?** Yes in principle: tune the world so both forms land every saving and the gap in the same bin across the licensed estimate range, with no sentence about the form.
   - **Margin from the numbers (my arithmetic, not run on the data).** C must stay inside [25, 35) in both forms across the estimate range. The thread's licensed estimates run about -0.26 to -0.32 (a factor of about 1.23 on C), and the linear/log spread at -0.32 is 1.11. The product is about 1.37 against a window of 35/25 = 1.40. It fits, but only just, with nothing to spare for B (21.7 against the 25 edge) or the gap (11.3 against 15). Narrowing the estimator spread (a tighter, more homogeneous Fenwick response, so the simple DiD and the panel agree) or lowering the curvature (a smaller proportional price change on C) buys more room. The builder should recompute the fork table row for both forms in `checks.py`, which currently has no linear-form check (grep found none).
4. **Design-note back-test sentence** (see Gate G reconciliation, and the Stump power section for what it does to Gate F). Edit the Survivor anatomy "Back-test" row so it is true to the data, or accept that the 2023 change alone discriminates the two prices.
5. **Rubric count** is about 26 against the 25 minimum (estimated, not generated). Any criterion dropped for the tank-fill pin leaves no margin.
6. Rounding-line distances elsewhere are comfortable: the water-drawn figures are at least 0.2 kgal from a .5 edge, and the facility figures are at least 0.014 AF from a .x5 edge (22.564 is 0.014 from 22.55, the nearest).

## Next action for the author
Add the tank-fill unit to the ask 2 sentence in `prompt.txt`: "a tank fill is one tank filled, a truck's and its trailer's each", with no mention of registers, sessions or the fault. Then run the pin through `voice-check.py` and `precut.py`, and have the judge re-run once. In the same pass, add a linear-form row to `checks.py` and the fork table, and decide whether to tune the world so the form closes in the data (window check in Findings 3).
