# task123: Steady Ground Fund, September 2026 stabilisation offers (realises ET01, the point-in-time revenue screen, redesigned as a stump)

Source note: `analytical_tasks/07_data_extraction_conformation/ET01_sec-fsds-point-in-time-revenue-screen.md` (ET01). Stage 1, draw, 2026-10-08. This is the build's one design note; the design stage extends it.

```
DRAW  (independent draws, checked with ../fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? yes, registered 2026-10-09 after checkpoint A (go)   Verdict: PASS against the filed corpus; WARN against the corpus plus the six pilot cards in draw order
  Shape: 05 allocation to a fixed total   Gate G mechanism: method_or_model_selection
  Gap: time (decisive), then rule and population   Pattern: B
  Domain: Nonprofit & Grant-making   Subdomain (enumerated): grantee-financial-health   Objective: Data Extraction & Conformation (ETL)
  Pairing repeated from last build? no (task116 is product-analytics x opportunity-sizing-decision; task122, last in the batch, is product-analytics x experiment-causal)
  Stakeholder role: head of grants (programme_officer)   Context-artifact type: filed_standard (the fund's round rules and the cutover standard)
  Calibration form: parallel_run_overlap (the in-house screen replayed against the bureau's published runs on the same six March censuses)   Decision type: allocation_to_total
  Decisive mechanism: the trailing window a census may use, recovered from the published runs; a year's final quarter exists only as the filed annual return's income less the nine-month year-to-date, so a grantee whose return had not reached the register at the census has its twelve months stop at the quarter before that year-end (G12, G13, G16, G19)
  Repeats from prior builds: none on a banned axis; the (time, B, method_or_model_selection) signature repeats task62's tempo lineage and task85, differentiated on the card
As-of date: 2026-10-08
```

Fiction's calendar: census 30 September 2026 (the statutory annual return deadline for the 31 March balance date most grantees keep), portal and register extract 7 October 2026, trustees meet 11 November 2026, offers run December 2026 to November 2027.

**Similarity claim.** No prior build turns on which trailing window a cut-off may use when a year's final quarter exists only through a filed annual document, recovered from a bureau's published runs; the nearest driver on file scores 0.07 (task101).

**Pairing and shape.** The work is ETL: four years of versioned quarterly portal returns, dual-grant duplicates, a 2024 form revision and a charities register extract conformed into one screen table that gives back every figure the bureau published, with the offers falling out of that table. The call faces forward (the offers commit the fund for December 2026 to November 2027, a window not yet open); its inputs are closed quarters, so it is not a forecast and the tag stays ETL. Shape 05 arithmetic: about 12 offered grantees x 2 figures (offer in NZ$, twelve-month fall in NZ$) = 24, plus the common rate the offers are struck at, the count scored, the first grantee outside the line and its fall, six round-by-round replay counts, five named chart parts and three files, about 42 criteria.

**Planned deliverables.** `steady_ground_sep2026_offers.docx` (the trustees' paper that commits the offers), `steady_ground_sep2026_screen.csv` (every scored grantee on the conformed screen), `steady_ground_sep2026_offers.png` (the offers read at a glance).

**World.** Ashworth Pascoe Trust (Canterbury, New Zealand, NZD), its Steady Ground Fund, and Ledgerwood Analytics, the bureau whose contract ended after the March 2026 round. Personas drawn with `guard.py names --geo "New Zealand, Canterbury" --seed 123`: Rebecca Anderson (head of grants, the requester), Liam Bryant (data lead, built the warehouse), Andrew Knox (Ledgerwood's lead analyst), Wiremu Roberts (chair of trustees), Mia Hart (finance manager), Tony Hughes (grants adviser, holds the decoy belief that the round exists for the March 2026 funding cut).

**Gate G.** Litmus: no. Every figure the task overturns is correct: today's portal holds each grantee's quarters as now known, the management fourth-quarter returns are what the grantees reported, and the bureau's packs are what the bureau computed; the difficulty is constructing a window rule no document states, not catching a wrong number. Mechanism method_or_model_selection, with etl_conformance as the frame. surface_read_dependency: no. stumping_family: analytical_non_defect. sole_data_defect: no (repair every file and the rule still has to be recovered; the naive read and the answer are different windows, not one window under two lenses).

## Stump sentence

A competent solver rebuilds the screen as held at the 30 September census, collapses the dual-grant returns, gives back every figure in Ledgerwood's six March-round packs except a handful of late-filer rows it writes off as noise, and files offers that score the grantees whose 2025-26 annual return was not yet on the register on twelve months to June 2026 built with their management fourth quarter, when the standing method takes a year's fourth quarter only from the filed annual return and stops those grantees' twelve months at December 2025.

## Decisive rung

Measured trap: #3, stops at a close but inexact match (decided 8 of 64, 5 under 0.50), gated by #1's reproduction clause, reports a failed back-test and ships anyway (11 of 64, 9 under 0.50): the cutover standard makes the six published March-round packs the definition of the screen, and the obvious point-in-time rebuild gives back all of them but a handful. #11 (beats the headline trap, misses the quiet one; 4 of 64, 2 under 0.50) sets the order: look-ahead is the famous point-in-time trap, and a strong solver beats it first.

Why the corpus is nearly blind, for a computable reason: every earlier round was a March round, and a March census falls six months after the 30 September deadline for the prior year's annual return, so a year is unfiled at a census only for the handful of grantees that filed very late; the September 2026 census falls on the deadline itself, so about a fifth of grantees are unfiled.

Corpus direction: under rung 2 the packs reproduce in every row but the handful of late-filer rows. That is the measured architecture's close-but-inexact gate rather than the corpus-direction test's "it reproduces"; the design stage sizes the handful and keeps each miss within about a point of fall so the residue reads as noise, the trade task110 shipped with its $375 a month.

The residue must not point at the rule: the management fourth-quarter return is trued up to the filed annual return by an amendment once the return is filed, so no rung below the decisive one joins the register and the late filers share no column in the returns; the discriminator lives only in the register's date received.

Proven-in-production checks (Part 6.1): nothing drawn is on the dead list (no filed formula carries the decisive rung, the rule is not a scannable parameter, no shipped column announces it, the pack must not narrate it, there is no argmax under a stated rule, and the natural basis is not the correct one); the S3 discriminator is buildable (the rule is a construction over a join, not one parameter, and not a linear rule in a rate-times-exposure world); L1's sentence can be written (above); L7 holds (the stopping rung gives back all but a handful of published figures). Caution carried forward: once suspected, the step-back is one as-of join on a dated status (filed by the census), so its only defence is that no sentence and no column raises the question.

## Ladder sketch

Candidates are offer sets; the design stage names them and asserts that every rung's set differs.

- Rung 0, the natural pipeline: today's portal (extract 7 October 2026), each return's latest version, discrete quarters by year-to-date differences, twelve months to the latest quarter held, one row per return. Candidate O0. Killed by: the packs score one row per grantee while the grants register maps a dual-grant grantee's two grant references to one organisation, so O0 scores those grantees twice.
- Rung 1, hygiene: one return per grantee-quarter (the latest accepted version across its grants), lines mapped across the 2024 form revision. Candidate O1. Killed by: the twin pair, two grantees identical in today's portal whose published falls sit about twice apart, which reproduce only on the versions accepted by each census.
- Rung 2, as held at each census: only versions accepted by the census, the management fourth quarter as held (trued up wherever the annual return was filed). Candidate O2, the stump: it beats look-ahead, gives back every published pack figure but a handful, and every reconciliation the solver writes passes. Killed by: the handful of late-filer pack rows, which reproduce only with the twelve months ended at the quarter before a year whose annual return had not reached the register at that census (the register extract's date received).
- Rung 3, decisive: a year's final quarter exists only as the filed annual return's income less the nine-month year-to-date, admissible from the register's date received; at 30 September 2026 the unfiled grantees' twelve months stop at December 2025. Candidate O*, the answer.

A solver who does everything right up to rung 2 commits to O2.

## Nearest exemplars

- Capacity Watch (Nonprofit & Grant-making, Agricultural Research Grant Allocation), measured mean 0.36 over four runs: a designation below a line and shares of a fixed reserve by shortfall, from an index rebuilt against 200 filed register cells; the model computed a words-only reading and never tested it against the register. Nearest on decision shape and on the published-results gate.
- Jurupa fiscal diagnostic review (Policy & Education, School District Finance Review), measured mean 0.41 over one run: a growth screen on filed finance data rebuilt after the consultancy closed, with a paragraph making its transmitted results the definition and a data-vintage fork; the model kept the winner and missed the runner-up and counts on an incomplete rule set. Nearest on scenario and on the vintage fork. This build's decisive rung moves the committed set itself, which Jurupa's did not.

## Guard

- Filed corpus (112 cards): PASS. NOTE test.same_driver_older, (time, B, method_or_model_selection) repeats task62's tempo lineage and task85, differentiated on the card. Nearest driver 0.07 (task101).
- Corpus plus the six pilot cards in draw order (simulated with FINGERPRINT_CARDS, nothing registered): WARN repeat.gate_g against task122. Answer: task122 selects an off-policy estimator by a corpus of past outcomes, here the corpus selects a window rule for a conformed income series, and etl_conformance, the other honest label, is blocked by task98 v5's (time, B, etl_conformance) lineage in the window.
- BLOCKs cleared at the draw: shape 01 (the note's own) is held by task116, so 05; patterns A, C and D are held by task114 to task116, so B; (rule, B, etl_conformance) is blocked by task98 v4 in the window and (rule, B, method_or_model_selection) is spent in 14 builds, so gap time leads, which is honest because the hidden rule is a window rule; closed_decision_corpus is held by task121 and task122 in the batch, so parallel_run_overlap, the cutover's replay; register is held by task122, so filed_standard; the furniture (trustees_or_governors, foundation_or_funder) is clear of task114 to task116 and of task120 to task122; the forcing event moved from cutover_or_migration to budget_or_appropriation at batch registration, because ban.forcing_event blocked cutover_or_migration against task117: the September 2026 stabilisation round is itself the allocation round that forces the call, and the in-house cutover stays in the world as background.
- People WARNs cleared by redrawing from the same seed: Patrick Mitchell (task103) and David Eaton (task104) out, Wiremu Roberts in; Benjamin Thompson, Andrea Brown and Jason Smith skipped against task118 and task119.
- WARN repeat.gate_g at batch registration (method_or_model_selection, against task120): answered as before, etl_conformance is the only other honest label and it is blocked by task98 v5 lineage; the two builds share the label, not the mechanism (task120 recovers a filing unit, this build recovers a window rule).

## Changes from the source note

- Domain: capital-markets quant research becomes Nonprofit & Grant-making, grantee financial health, because Economics excludes markets trading and a funder owns this call.
- Data: the SEC Financial Statement Data Sets (their hosts are blocked here) become a fully constructed pack with declared provenance: a New Zealand trust's grants-portal returns, its grants register and a charities register extract.
- The stated methodology memo goes: no shipped sentence states knowledge time, the fourth-quarter source or the window, and the cutover standard's reproduction clause on the bureau's six published March-round packs is the only pin.
- Decisive move: ET01's latest-value look-ahead becomes the headline lower rung, and the decisive rule is new: a year's final quarter only from the filed annual return, with the window stepping back where that return was not on the register at the census.
- Call: a retrospective top ten at a past rebalance becomes a forward-facing allocation of the September 2026 stabilisation pot (offers running December 2026 to November 2027).
- Shape 01 becomes 05, and the CSV, PNG and PDF deliverables become DOCX, CSV and PNG.
- Raw material kept: year-to-date to discrete quarters is rung-0 machinery; restated comparatives and the 2024 form revision (the tag-priority analogue) go to the ask layer as devices; fiscal-label alignment drops to texture.

## Tried and rejected

- The blueprint's stated-memo architecture (a methodology memo fixing knowledge time, the latest visible submission, tag priority and the year-to-date derivation): rejected because a strong solver implements every stated clause, so the screen becomes a computation; the decisive rule now lives in no shipped sentence.
- Bitemporal look-ahead as the decisive rung: rejected because in a forward round the census and the extract sit a week apart, so latest-value and as-held barely differ live, and point-in-time is a strong solver's reflex; kept as the headline rung-2 move.
- Like-for-like restated comparatives as the decisive rung: rejected because a latest-value build already pairs a quarter with its re-presented comparative, so the natural pipeline lands on the rule.
- The analyst's LTM identity (last annual plus year-to-date less prior year-to-date) as the decisive rung: rejected as a two-item menu that any sweep of the packs scores end to end.
- Merger pro-forma (organic income) and successor-registration linking as the decisive rung: rejected, the first is ET04's mechanism and the second is task81's driver (a unit persisting across identifier changes).
- Excluding the fund's own earlier offers from grantee income: rejected because it needs a filed sentence, and a filed exclusion is read and executed.
- First cut of rung 2 replaced the management fourth quarter with the filed annual return wherever it was on file: rejected because the residual misses would then be exactly the solver's own fallback branch, which points straight at the rule; the trued-up fourth-quarter amendment keeps the register out of every rung below the decisive one.
- Australia as the setting (30 June year-ends, lodgement by 31 December): dropped because task118 in this batch is already Australian; New Zealand's six-month annual return deadline gives the same structural reason.
