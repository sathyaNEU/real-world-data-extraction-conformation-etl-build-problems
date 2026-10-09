# task123: Steady Ground Fund, September 2026 stabilisation offers (realises ET01, the point-in-time revenue screen, redesigned as a stump)

Source note: `analytical_tasks/07_data_extraction_conformation/ET01_sec-fsds-point-in-time-revenue-screen.md` (ET01). Stage 1, draw, 2026-10-08; stage 2, design, 2026-10-09. This is the build's one design note. Every number from "Entity and unit of value" down is a target the generator asserts; figures marked "paper run" come from a scratch prototype of the ladder arithmetic (not the pack) and only show the targets are reachable.

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
  Decisive mechanism after hardening loop 1: rule 4.1's recency clause (twelve-month income ends on or after
    the census before) composed with rule 2's census list and applied to the stepped-back windows; it never
    binds in a March round and removes the 14 stepped-back 31 March grantees at the first September census
    (measured traps #13 and #11); the step-back above is now the stop (R4)
  Repeats from prior builds: none on a banned axis; the (time, B, method_or_model_selection) signature repeats task62's tempo lineage and task85, differentiated on the card
As-of date: 2026-10-08
```

Fiction's calendar: census 30 September 2026 (the statutory annual return deadline for the 31 March balance date most grantees keep), portal and register extract 7 October 2026, trustees meet 11 November 2026, offers run December 2026 to November 2027.

**Similarity claim.** No prior build turns on which trailing window a cut-off may use when a year's final quarter exists only through a filed annual document, recovered from a bureau's published runs; the nearest driver on file scores 0.07 (task101).

**Pairing and shape.** The work is ETL: four years of versioned quarterly portal returns, dual-grant duplicates, a 2024 form revision and a charities register extract conformed into one screen table that gives back every figure the bureau published, with the offers falling out of that table. The call faces forward (the offers commit the fund for December 2026 to November 2027, a window not yet open); its inputs are closed quarters, so it is not a forecast and the tag stays ETL. Shape 05 arithmetic: about 12 offered grantees x 2 figures (offer in NZ$, twelve-month fall in NZ$) = 24, plus the common rate the offers are struck at, the count scored, the first grantee outside the line and its fall, six round-by-round replay counts, five named chart parts and three files, about 42 criteria.

**Planned deliverables.** `steady_ground_sep2026_offers.docx` (the trustees' paper that commits the offers), `steady_ground_sep2026_screen.csv` (every scored grantee on the conformed screen), `steady_ground_sep2026_offers.png` (the offers read at a glance).

**World.** Ashworth Pascoe Trust (Canterbury, New Zealand, NZD), its Steady Ground Fund, and Ledgerwood Analytics, the bureau whose contract ended after the March 2026 round. Personas drawn with `guard.py names --geo "New Zealand, Canterbury" --seed 123`: Marie Griffin (head of grants, the requester; redrawn at stage 3, see Tried and rejected), Liam Bryant (data lead, built the warehouse), Andrew Knox (Ledgerwood's lead analyst), Wiremu Roberts (chair of trustees), Mia Hart (finance manager), Tony Hughes (grants adviser, holds the decoy belief that the round exists for the March 2026 funding cut).

**Gate G.** Litmus: no. Every figure the task overturns is correct: today's portal holds each grantee's quarters as now known, the management fourth-quarter returns are what the grantees reported, and the bureau's packs are what the bureau computed; the difficulty is constructing a window rule no document states, not catching a wrong number. Mechanism method_or_model_selection, with etl_conformance as the frame. surface_read_dependency: no. stumping_family: analytical_non_defect. sole_data_defect: no (repair every file and the rule still has to be recovered; the naive read and the answer are different windows, not one window under two lenses).

```
GATE G  (design stage)
  Litmus, in a sentence: no reported number or stated read is overturned; the management returns, the
    register dates and Ledgerwood's packs are all correct, no voice or file states the stump's basis or
    its figures, and the model loses by building the screen on a window construction the packs refute
    on ten non-offered rows and every other check confirms.
  Framing limb: nobody in the pack reads a correct number the wrong way. Tony Hughes holds a belief
    about the round's purpose (relief for the March 2026 government cut), never a basis for the screen
    and never a figure; delete him and the stump is unchanged.
  Primary mechanism label: method_or_model_selection (G16 over a Pattern B corpus); frame etl_conformance
  surface_read_dependency: no   stumping_family: analytical_non_defect   sole_data_defect: no
  Delete every wrong number from the pack. Still hard because: there are none to delete; the step-back
    is a construction (a year's final quarter exists only as filed annual income less the nine-month
    year to date, admissible from the register's date received), recovered from six packs that confirm
    the natural construction on every offer and every rate.
  Clean-data test, per suspect file (asserted in the generator, section "Assertion plan" A41 to A43):
    portal (version history, delta-shaped): repair = hand the solver the portal as held at the census
      (drop every version accepted after 30 Sep 2026). R3 unchanged, T unchanged, T != R3.
    register extract (returns not yet filed): repair = complete it with every outstanding FY2025-26
      return at its eventual received date (all after the census). T unchanged (dates after the census
      are inadmissible), R3 unchanged (R3 never reads the register), T != R3.
    management fourth quarters (semantics): repair = replace every management Q4 with the audited Q4
      where the extract holds the return. The six grantees who filed 1 to 7 October carry exact
      management fourth quarters by construction, so R3 and T are unchanged, T != R3.
    instrument: the decision's own quantity is twelve-month income on the standing method at the
      census; no better instrument exists short of backdating 32 grantees' filings, which changes the
      world rather than repairing a file. The difficulty is which quarters the method admits.
  Lens-swap test: R3 and T are not one number read two ways. For the 32 grantees unfiled at the
    census they are different periods (twelve months to June 2026 against twelve months to December
    2025 or March 2026), for the other 115 they are identical, and the choice between them is settled
    only by reproduction of the corpus, which is selection among constructions, not a relabelling.
  Hardening loop 1 (R5, rule 4.1's recency clause): no suspect file carries it (the clause and the census
    list are filed); A41 to A43 re-run on the trio (the answer, R3, R4): each repair leaves all three
    unchanged and all three different. Lens-swap: R4 and the answer agree on all 132 rows the answer
    scores; the 14 rows R4 adds are twelve months to December 2025 that the March 2026 round already
    scored, so the difference is which windows rule 4.1 admits at this census, not one figure read two
    ways. Exposure on file: the step from R4 to the answer removes a class of honest rows under a filed
    clause and re-places 55.2 per cent of the pot, the shape stumping Part 1 flags for a binding
    constraint (task58 v3, v4). The answer on file: the clause defines the measure at this census and
    is composed with the corpus-recovered window rather than inferred; the excluded windows are correct
    figures that the March 2026 round scored, and no voice or file reads them as wrong.
  Pre-draw identity test: the allocation's arithmetic (offers = clamp(rate x fall), sum = pot) closes
    over falls the pack does not ship; every fall is constructed, and the decisive input (which quarters
    are admissible) is neither filed nor visibly forced. Passed.
```

## Stump sentence

A competent solver rebuilds the screen as held at the 30 September census, collapses the dual-grant returns, recovers the step-back from Ledgerwood's ten residue rows (or reaches it directly through the twelve-month identity on the register as held), gives back all 797 published rows, every offer and every rate, and strikes the offers at 17.76 cents on 14 names (R4), because it scores the 14 grantees balancing at 31 March whose 2025-26 annual return was not on the register on twelve months to December 2025, reading rule 4.1's "census before it" as a year back, which is what it meant in every March round the corpus shows, when rule 2 makes 31 March 2026 the census before the first September census, those twelve months end before it, and the answer scores 132 grantees and strikes 42.55 cents on nine.

(Hardening loop 1. The stage 2 sentence had the solver stop at R3, scoring the 32 unfiled grantees on twelve months to June 2026 with their management fourth quarters; solver round 1 climbed past it, see Tried and rejected.)

## Decisive rung

**Hardening loop 1: the decisive rung is R5.** Measured trap #13, validates on one population and applies to another (3 of 64, 2 under 0.50), behind #11 (beats the headline trap, misses the quiet one; 4 of 64, 2 under 0.50): the stepped-back window is the construction that fits all 797 published rows, and the population it is applied to in September differs on one axis, the distance to the census before. Rule 4.1 says twelve-month income at a census is for twelve months ending on or after the census before it; rule 2, amended 16 June 2026, adds 30 September to the census dates from 2026. In every March round the census before was a year back and every window, stepped back or not, ended on or after it: no published window ends before it, two end exactly on it (J1 2023 and J2 2024, the 30-June residue rows), which pins the inclusive reading, and the screen with the clause switched off, or read against the census a year back, gives back all six packs (A54). So the clause has never bound and no back-test can see it. At the first September census the census before is 31 March 2026: the 17 scored 30-June grantees end exactly on it and the 14 unfiled 31 March grantees, whose twelve months stop at December 2025, fall before it and are not scored (rule 3.2). The forward rows' difference is filed (rules 2 and 4.1), not left to inference, and it changes the decision: R4 strikes 17.76 cents on 14 names, the answer 42.55 on nine.

Why this rung and not another: the stage 2 rung (the step-back, now R4) is the analyst's own twelve-month identity evaluated on the register as held, so any rung that turns on which quarters the register admits is free (Tried and rejected); the next rung had to sit after the window and move a figure that identity cannot see, and the recency clause acts only on the identity's output. Its exposure is stated, not hidden: it is a filed sentence, and a solver who reads every clause and composes rule 2 with it lands the answer (opponent property 1); its defence is that it is quiet at every natural window and in every corpus case, bites only on the step-back's output, and its right-hand side needs rule 2's new calendar.

The stage 2 description of the rung that is now the stop follows, as designed.

Measured trap: #3, stops at a close but inexact match (decided 8 of 64, 5 under 0.50), gated by #1's reproduction clause, reports a failed back-test and ships anyway (11 of 64, 9 under 0.50): the cutover standard makes the six published March-round packs the definition of the screen, and the obvious point-in-time rebuild gives back all of them but a handful. #11 (beats the headline trap, misses the quiet one; 4 of 64, 2 under 0.50) sets the order: look-ahead is the famous point-in-time trap, and a strong solver beats it first.

Why the corpus is nearly blind, for a computable reason: every earlier round was a March round, and a March census falls six months after the 30 September deadline for the prior year's annual return, so a year is unfiled at a census only for the handful of grantees that filed very late; the September 2026 census falls on the deadline itself, so about a fifth of grantees are unfiled. (Refined at design: the handful is three 31 December grantees, whose returns are not yet due at a March census, and two 30 June grantees three months late; no 31 March grantee is ever a corpus late filer. See "Calibration corpus".)

Corpus direction: under rung 2 the packs reproduce in every row but the handful of late-filer rows. That is the measured architecture's close-but-inexact gate rather than the corpus-direction test's "it reproduces"; the design stage sizes the handful and keeps each miss within about a point of fall so the residue reads as noise, the trade task110 shipped with its $375 a month.

**Corpus direction, settled at design.** Under the stump rung (R3 below, the draw's rung 2) the six packs reproduce 787 of 797 rows, all 71 offers and all six rates; the ten misses are non-offered rows. That is not "it reproduces", and it cannot be made so: those ten rows are the only thing that pins the decisive rule. Without them T is unpinned against R3, and also against the overdue rival (step back only where the annual return was overdue), which reproduces every late-filer row exactly and coincides with R3 at a census held on the 30 September deadline day itself; the corpus separates T from it only through grantees whose return was not yet due at a March census, and the only balance date that supplies them is 31 December. So the refutation is load-bearing for Gates C and D and stays; what is controlled is its loudness, five ways. (1) Size: 10 of 797 rows (1.25 per cent), each within 1.2 per cent of twelve-month income and 1.0 point of fall, none within 5 points of the line under either window, none offered, so no published decision moves. (2) No aggregate: the packs carry no total that a rebuild could tie or miss; the residue lives only at row level. (3) No equality signature: no 31 March grantee is a corpus late filer, because a full-year step-back makes a published twelve months equal the rebuilt prior twelve months on the same row; the residue comes from one-quarter (31 December) and three-quarter (30 June) step-backs, which match no rebuilt figure. (4) No column: the residue grantees share no portal column, and six of the ten carry no fourth-quarter amendment at all. (5) Disclosure framing: the prompt asks for the round-by-round count of rows given back, the measured trap 1 framing that models report and ship past. What this does not buy: a solver who investigates D1 (missing in all six rounds) finds T in about three steps. The trade is the measured top architecture (traps 1 and 3 decided 19 of 64 client tasks, 14 under 0.50) against the doctrine's two portal builds where an argumentative corpus was quoted back; those refuted the naive read in aggregate (task92 v2 by 18.45 per cent, task89 v5 through a workbook total), and this one refutes it on 1.25 per cent of rows, in no total and on no decision.

The residue must not point at the rule: the management fourth-quarter return is trued up to the filed annual return by an amendment once the return is filed, so no rung below the decisive one joins the register and the late filers share no column in the returns; the discriminator lives only in the register's date received.

Proven-in-production checks (Part 6.1): nothing drawn is on the dead list (no filed formula carries the decisive rung, the rule is not a scannable parameter, no shipped column announces it, the pack must not narrate it, there is no argmax under a stated rule, and the natural basis is not the correct one); the S3 discriminator is buildable (the rule is a construction over a join, not one parameter, and not a linear rule in a rate-times-exposure world); L1's sentence can be written (above); L7 holds (the stopping rung gives back all but a handful of published figures). Caution carried forward: once suspected, the step-back is one as-of join on a dated status (filed by the census), so its only defence is that no sentence and no column raises the question.

## Entity and unit of value

The Ashworth Pascoe Trust holds multi-year operating grants with about 150 Canterbury community organisations, and its Steady Ground Fund makes twelve-month stabilisation offers, scored on each grantee's twelve-month income at a census: an offer is the grantee's fall in twelve-month income at a common rate (cents per dollar of fall), raised to a floor of NZ$15,000 or held to a cap of NZ$150,000, the rate struck so the offers spend a fixed pot. Two things both read as the size of a grantee's trouble and rank grantees differently: the fall in dollars (what the offer is struck on) and the fall as a share of the prior twelve months (what the 10 per cent line tests). And two things both read as "twelve-month income": the latest filed financial year on the register (R0) and the trailing four portal quarters at the census (everything above R0), which disagree because the register runs on financial years and the screen on quarters ending at the census.

## Decision

Exactly one rate for the September 2026 round (census 30 September 2026), with the offer set and every offer it implies, committing the trustees' pot of NZ$560,000 (filed in the 2026-27 budget minute; NZ$820,000 until hardening loop 1, see Tried and rejected) for offers paid monthly from December 2026 to November 2027. Shape 05, allocation to a fixed total. The window is open (forward commitment); every input is a closed quarter or a filed date, so nothing is forecast and the tag stays ETL.

## Answer

```
ANSWER (built, hardening loop 1)
  The rate: 42.55 cents per dollar of fall (target band 36.00 to 48.00, asserted), struck as the
    highest hundredth of a cent whose whole-dollar offers do not exceed NZ$560,000: NZ$559,969
    offered, NZ$31 left in the Fund, the next hundredth NZ$66 over (both at least NZ$25 from the
    step edges, so no per-offer rounding convention moves the struck rate)
  Offered: 9 grantees by name: F1 to F7 (filed 31 March grantees, F3 the dual-grant organisation)
    and A5 and A6 (30-June grantees scored on twelve months to March 2026)
  Scored: 132 of the 150 organisations holding an operating grant at the census; the 14 unfiled
    31 March grantees are out under rule 4.1 and four newer grantees under rule 3.2
  Cap binds for exactly one offer (F1); no offer sits at the floor; neither R3 nor R4 caps an offer
  First grantee outside the line: L_dual, Amberley Tenancy Advocacy Service, 6.4 per cent (6.39;
    the next 5.40); R4's first outside is Y4 at 7.72
  Line clearance: no scored grantee's fall within 1.5 points of 10.0 per cent
MARGIN: an allocation has no runner-up; the guard that binds is grid separation on the rate (every
  rung and single-violation cell at least 14.5 per cent below the answer, R0 nearest) and on names
  (R4 differs by five names and 55.2 per cent of the pot, R3 by seven and 46.2 per cent)
```

## Ladder

Six rungs since hardening loop 1. Candidates are offer sets with their rates; each rung's set differs from every other rung's by name, asserted after every parameter change (A6). Built values at the September census in brackets: rate; the answer's rate as a multiple of the rung's; offers; names differing from the answer; share of the pot re-placed.

- **R0, the filed-year basis (gap: rule, what "twelve-month income" is).** Twelve-month income is total gross income on the grantee's latest annual return in the register extract, the fall is against the return before. Candidate O0 [36.37 cents, 1.170x, 10 offered, 5 differ, 31.4 per cent]. Killed by: the six packs, whose twelve-month figures are sums of four portal quarters and match no filed financial year (a filed-year rebuild gives back 10 of the 797 rows). Why a careful analyst stops here: the annual return is the audited statutory figure, two filed years is how a funder reads a grantee's trend, and nothing in the register looks incomplete.
- **R1, the natural portal build (gap: population, the unit).** Today's portal (extract 7 October 2026), each return's latest accepted version, year to date differenced into quarters, twelve months to June 2026 against the twelve months before, one row per grant return. Candidate O1 [23.94, 1.777x, 14 offers on 154 rows, 9 differ, 51.1 per cent]. Killed by: the packs carry one row per organisation, and the grants register maps the seven dual-grant organisations' two references to one charity number, so R1's row count exceeds every pack's. Why stop: it is the textbook ETL build, each grant return is a separate filing under its own reference, and every figure ties to a return.
- **R2, one row per organisation (gap: time, the version basis).** The latest accepted version across each organisation's grants, today's portal. Candidate O2 [26.54, 1.603x, 13 offered, 8 differ, 51.9 per cent]. Killed by: the twin pair and 94 corpus rows touched by amendments accepted after their census, which reproduce only on the versions accepted by each census (R2 also misses the offers and rate in four rounds). Why stop: dual grants are collapsed, every row pairs one-for-one with a pack row, and "the latest accepted version is the record" is the warehouse's own convention.
- **R3, as held at the census (gap: time, knowledge time; the stage 2 stump).** Versions accepted by the census (inclusive), the fourth quarter as held, which is the trued-up figure wherever the annual return was on the register and the management figure otherwise. Candidate O3 [29.83, 1.426x, 12 offered, 7 differ, 46.2 per cent]. Killed by: the ten residue rows (D1 in all six rounds, D2 in two, two 30-June late filers), which reproduce only with the window stopped at the quarter before a year-end whose annual return had not reached the register by that census. Why stop: it beats look-ahead, gives back every offer and every rate in all six rounds and 787 of 797 rows, and the ten misses are small non-offered rows that read as amendment noise.
- **R4, the step-back (gap: time, then rule; the stage 2 decisive rung, now the stop).** A year's final quarter exists only as the filed annual return's income less the nine-month year to date, admissible from the register's date received; the trailing window is the latest four consecutive admissible quarters and the prior window steps back with it. At 30 September 2026 the 14 unfiled 31 March grantees' twelve months stop at December 2025 and the 17 scored 30-June grantees' at March 2026. Candidate O4 [17.76, 2.396x, 14 offered, 5 differ, 55.2 per cent]. Killed by: rule 4.1's recency clause with rule 2's census list (R5). Why stop: it gives back all 797 published rows, every offer and every rate; it is the analyst's own twelve-month identity on the register as held (solver round 1 reached it that way, Tried and rejected); and the clause it breaks has never bound in a round the corpus shows, because every March census before had its previous census a year back.
- **R5, decisive (gap: population, through time).** Twelve-month income at a census must end on or after the census before it (rule 4.1), and the census before 30 September 2026 is 31 March 2026 (rule 2). The 14 unfiled 31 March grantees (twelve months to December 2025) are not scored; the 17 30-June grantees (twelve months to March 2026, ending on that census) are; one new 30-June grantee still lacks the quarters rule 3.2 requires. Candidate O*, the answer [42.55, 9 offered, 132 scored].

"A solver who does everything right up to rung 4 commits to O4": the stump sentence above.

```
Every rung names a different candidate? yes (asserted by name, A6)
Which rung carries the stump: R5 (R4 is the stop; R3 was the stage 2 stop)
Seven survival properties for R5:
  1 written in no shipped sentence ............ no: rule 4.1's second sentence files it, and rule 2 files the
                                                calendar it is read against; the exposure, stated under Decisive rung
  2 no sweepable corpus nominates it .......... yes: blind by construction, every March window ends on or after the
                                                census a year back (A54, structurally and case by case)
  3 no arithmetic symptom ...................... yes: R4 gives back every published figure; counts, offers, rates
                                                and joins all tie on the wrong path
  4 not a per-row predicate .................... partial: once suspected it is one date comparison per row, but its
                                                right-hand side (the census before) needs rule 2's new calendar
  5 enumeration is arithmetic .................. yes: the affected class is the step-back's own output
  6 no cutover date ............................ partial: rule 2's June 2026 amendment is a dated event, but no
                                                series steps at it
  7 survives the deletion ...................... yes: no wrong number exists to delete
Worth on the graded quantity (the rate, built): R1 to R2 +10.9 per cent, R2 to R3 +12.4, R3 to R4 -40.5,
  R4 to R5 +139.6
Sign direction: the corrections walk the rate up through R3, the step-back cuts it by two fifths, and the
  decisive rung more than doubles it, past every lower rung: the answer is the highest rate on the grid.
  R0 sits off the chain (a different measure).
```

## Position table (adapted to an allocation)

The skill's position rule is written for a ranking; here the answer is a rate and a set, so each row carries the answer's rate as a multiple of the rung's, the names that differ, the share of the pot that goes to different grantees, and the rank by dollar fall of two markers: A5 (Woolston Sports Education Trust, the answer's largest uncapped offer, a 30-June grantee scored on twelve months to March 2026) and M (Geraldine Carer Respite Network, R4's largest offer, an unfiled 31 March grantee the answer does not score).

| Rung | Answer's rate as a multiple | Names differing from the answer | Pot re-placed | A5 by fall | M by fall |
|---|---|---|---|---|---|
| R0 | 1.170x | 5 | 31.4% | 14th, not offered | 7th, not offered |
| R1 | 1.777x | 9 | 51.1% | 145th | 153rd |
| R2 | 1.603x | 8 | 51.9% | 138th | 146th |
| R3 | 1.426x | 7 | 46.2% | 138th | 146th |
| R4 | 2.396x | 5 | 55.2% | 4th, offered | 1st, offered |
| R5 | 1.00x | 0 | 0 | 2nd, offered | not scored |

No rung sits within 1.15x of the answer's rate (nearest R0 at 1.170x; A5 asserts the floors 1.15, 1.40, 1.40, 1.30 and 2.00). The answer's offers are R4's less the five R4 makes to grantees the answer does not score (M, A2, A3, A4, C1; A7).

## Discriminator dominance (adapted)

- R4 against the answer (hardening loop 1): R4's five own offers (M, A2, A3, A4 and C1, 31 March grantees that fell in 2025 and recovered in 2026, scored by R4 on twelve months to December 2025) hold 56.4 per cent of R4's eligible falls (A18, floor 45). The answer's edge is the removal itself: no answer name changes window between R4 and the answer (A45 holds every offered grantee on the answer's windows under R4), so the rate moves only through the five removed falls, which is why the move is 2.40x.
- R3 against the answer: R3's own names (the four decoys and C1) hold 46.4 per cent of R3's eligible falls; the answer's own names against R3 (A5 and A6) hold 25.6 per cent of the answer's (A18, floors 20 each).
- Band check, both directions: every decoy is unscored by the answer and sits on R4 at -1.45, -1.27, -1.58 and 7.72 per cent, on R3 at 15.81 to 18.43; every step-back mover sits at 14.21 to 22.08 per cent on R4 or the answer and at -9.09 to -2.92 on R3 (A19).
- Disagreement constructed, not drawn: the generator builds each mover's quarterly path deterministically (the seed decides texture only) and asserts both windows' falls per name.

## Correction grid

Built values at the September census, rate against the answer's 42.55 cents. Every cell runs with rule 4.1 unless the row says otherwise.

| Cell | Rate vs the answer | Rule it violates |
|---|---|---|
| per return, latest, no step-back (R1) | -43.7% | packs: one row per organisation |
| per return, as held, no step-back | -37.5% | packs: one row per organisation |
| per organisation, latest, no step-back (R2) | -37.6% | packs: versions accepted by each census (twin pair) |
| per organisation, as held, no step-back (R3) | -29.9% | packs: the ten residue rows |
| per return, latest, step-back | -26.9% | two violations, same direction |
| per return, as held, step-back | -16.1% | packs: one row per organisation |
| per organisation, latest, step-back | -16.4% | packs: versions accepted by each census |
| filed-year basis (R0) | -14.5% | packs: trailing quarters, not financial years |
| step-back without rule 4.1's clause (R4) | -58.3% | rules 2 and 4.1 |
| R4 per return, as held | -61.5% | rules 2 and 4.1; one row per organisation |
| R4 latest versions | -61.2% | rules 2 and 4.1; versions accepted by each census |
| answer | 0 | |
| partial: 30-June grantees not stepped back | +55.8% | packs: the two 30-June residue rows |
| partial: only 30-June grantees stepped back | -41.0% | packs: the eight 31 December residue rows |
| partial: current window stepped back, prior window not | +55.8% | packs: prior and fall figures on all ten residue rows |
| partial: overdue only (V1) | -29.9% (equals R3) | packs: D1 and D2 rows, not yet due when stepped back |
| partial: register fallback, no step-back | -29.9% (equals R3, by construction) | packs: the ten residue rows |
| rule 4.1 read strictly (after the census before, not on it) | +55.8% | packs: J1 2023 and J2 2024 end on the census before |
| rule 4.1 against the census a year back | -58.3% (equals R4) | rule 2: the census before is the previous date in its list |
| partial: register read as at the extract | 0 on the rate and every offer; 138 scored, not 132 | packs: all ten residue returns appear in the extract |
| partial: census day exclusive | 0 on the rate and every offer; 118 scored, not 132 | packs: three census-day receipts counted as received |

Separation: the nearest single-violation cell sits 14.5 per cent from the answer (R0, a different measure), the nearest on the main chain 16.1 per cent (per return, as held, step-back); target at least 8. The three +55.8 cells coincide because each takes A5 and A6 out of the offered set (their June-window falls are under the line, or they are not scored), leaving F1 to F7. The two converging cells (register at the extract, census day exclusive) leave the rate and every offer unchanged by construction and move only the count scored, which the corpus pins (T-extract misses 10 rows, T-strict 3).

## Calibration corpus

```
Form: parallel_run_overlap. Ledgerwood's six published March-round runs (census 31 March 2021 to 2026),
  one workbook per round, each a screen sheet (one row per scored organisation: reference, name,
  twelve-month income, the twelve months before, fall in dollars, fall per cent to one decimal, offer)
  and a round sheet (census date, pot, rate, offers made, total offered). No window column, no window
  in any header, no method text. The cutover standard makes giving back every figure in all six the
  condition of using the in-house screen.
Cases: 797 rows (118, 124, 131, 137, 142, 145); 71 offers (9, 10, 11, 12, 13, 16); six rates;
  pots NZ$540,000, 575,000, 610,000, 650,000, 690,000, 720,000.
Correct rule (T) reproduces 797 of 797 rows to the dollar (fall per cent to the decimal), 71 of 71
  offers to the dollar and 6 of 6 rates to the hundredth of a cent. Zero tolerance.
Rival family, 12 rules, each scored row by row (misses asserted by name, worst stated):
  R0 filed-year basis ..................... misses at least 760 rows
  R1 per grant return ...................... row counts fail all six rounds (5 to 7 extra rows each);
                                             offers and rate fail where a dual organisation was offered (2023, 2025)
  R2 latest versions ....................... misses at least 40 rows, offers and rate in at least 4 rounds
  R3 as held, management Q4 (the stump) .... misses 10 rows; 0 offers; 0 rates
  V1 step back only where overdue .......... misses 8 (D1 x6, D2 x2: returns not yet due)
  V2 December balance dates step back ...... misses 12 (D2 x4 and D3 x6 filed early, the two 30-June rows)
  V3 step back where the Q4 return was
     amended after the census .............. misses at least 10 (six residue rows never amended; four
                                             on-time filers re-amended a Q4 line split after a census)
  V4 current window only ................... misses 10 (prior and fall figures)
  V5 leave unfiled grantees unscored ....... misses 10 (rows absent)
  T-strict (census day exclusive) .......... misses 3 (the three census-day receipts)
  T-extract (register as at 7 Oct 2026) .... misses 10 (every residue return is in the extract)
  fallback (register Q4 where received,
     management Q4 otherwise) .............. misses 10 (identical to R3 by construction)
  Worst rival miss among the T variants: 3 rows (T-strict); no rival misses fewer than 3.
Twin pair: two 31 March grantees in the March 2025 round, identical on every grants-register column
  (sector, region, programme, grant amount, start date, balance date) and identical to the dollar on
  twelve-month income, prior twelve months and fall under today's latest versions (both 11.6 per cent);
  published falls 5.9 and 11.6 per cent (1.97x), because one restated its October to December 2024
  quarter after the census. Only the versions accepted by 31 March 2025 reproduce both; under R2
  both are offered and the round's offers and rate fail.
Every rule the golden composes has a case that breaks if it is flipped:
  trailing four quarters (all rows) · one row per organisation (dual rows) · as held (twin pair and
  amended rows) · latest accepted version across an organisation's grants (one dual organisation
  whose two returns differed as held, March 2023) · Q4 admissible only from a received annual
  return (ten residue rows) · not yet due still steps back (D1, D2) · step back to the quarter
  before the inadmissible year-end, prior window with it (residue figures) · census day inclusive
  (three receipts) · eight quarters required (new grantees appear only from their ninth quarter) ·
  floor and cap (offers at NZ$15,000 and NZ$150,000 in four rounds) · rate struck to the hundredth
  of a cent with the remainder kept (every round sheet) · fall per cent on the prior twelve months.
  One composition has no corpus case: T together with the eight-quarter rule removing a grantee
  (September only); both halves are separately pinned, the first by the residue rows, the second by
  the filed round rules.
Ordinal agreement defeated: R3 orders the six rounds' offers and rates exactly like T, which is the
  point; the residue rows are where its order breaks, and none is near the line.
Resemblance: the residue grantees resemble nobody in September's decision (steady, never offered);
  the corpus nominates the decoy's method on every decision it shows.
What the corpus is blind to, and why (asserted twice, structurally and case by case): in every March
  pack the year-end quarter inside each window belongs to a year whose annual return was due six
  months (31 March balance dates) or three months (30 June) before the census, so it was on the
  register except for two 30-June grantees that filed very late; the only balance date whose return
  is not yet due at a March census is 31 December (three grantees, two filing after March in some
  years). So T and R3 agree on 787 of 797 rows, every offer and every rate. At the September census
  the census falls on the filing deadline itself for 31 March balance dates and three months before
  it for 30 June, so 32 grantees step back.
Residue rows, named for the generator: D1 (31 December balance date, files each May) in all six
  rounds; D2 (31 December) in 2022 and 2024, early in 2021, 2023 and 2026 and on the census day in
  2025; D3 (31 December, files each February) in none; two 30-June grantees received in April 2023
  and May 2024. Census-day receipts: 31 March 2023 (a 30-June grantee), 31 March 2025 (D2) and
  31 March 2026 (a 30-June grantee); none on 31 March 2024, which was Easter Sunday.
Rule 4.1's recency clause (hardening loop 1), blind by construction: at every March census the census
  before is a year back; no published window ends before it and exactly two end on it (J1 2023 and J2
  2024, the 30-June residue rows, stepped back to the March a year earlier), which pins "on or after"
  against "strictly after" (the strict flip breaks 4 corpus cases, A30). The screen with the clause
  switched off, or read against the census a year back, gives back all six packs (A54, asserted per
  round in the generator and in the verifier). So the corpus scores the window construction and is
  arithmetically incapable of scoring the clause, which binds for the first time at 30 September 2026.
```

## Pins and counter-pins

- **Filed pins, by authority.** Level 1, the cutover standard (the reproduction clause: the in-house screen may be used only once it gives back every grantee row, every offer and each round's rate in all six published March runs). Level 1, the round rules (the census dates in rule 2: 31 March each year and, from 2026, 30 September; rule 4.1's second sentence: twelve-month income at a census is for twelve months ending on or after the census before it; rule 7's pay day: the 20th of the month before the month an instalment is for, or the Friday before; scope: organisations holding a current operating grant at the census with returns covering both twelve-month periods the screen compares; one row per organisation; the 10 per cent line on the prior twelve months; offers at the common rate on the fall in dollars, floor NZ$15,000, cap NZ$150,000, whole dollars; the rate struck to the hundredth of a cent as the highest that keeps offers within the pot, any remainder staying in the Fund; offers paid in twelve monthly instalments from the December after the census). Level 3, the trustees' 2026-27 budget minute (September pot NZ$560,000). Level 4, the warehouse field guide (field semantics only: version status values, accepted_at in New Zealand time, line codes on both forms, the register extract's date_received). Level 5, the portal's November 2024 form-change notice, effective from the December 2024 return (ask layer only: "Government grants" becomes "Government grants and contracts" and keeps its code, fees and sales lose the contracts, the Trust-money memo, comparatives shown for information). Above all of them, since stage 3, the prompt states the pot (NZ$560,000 since hardening loop 1), the floor (NZ$15,000) and the cap (NZ$150,000), the same values the budget minute and rule 5.2 file; nothing in the pack states another, so the top of the hierarchy and the filed pin agree and no counter-pin exists.
- **Empirical pins (corpus, C2).** Trailing four quarters; one row per organisation; as held at the census; T (Q4 only from a received annual return; the window steps back; the prior window with it); census day inclusive; fall per cent on the prior twelve months; rounding and integerisation paths.
- **No pin, deliberately.** Nothing states knowledge time, the fourth-quarter source, the window or that a management return is provisional. Rule 4.1's recency clause is a pin of a different kind: it is filed, it is quiet at every natural window, and nothing points at the step-back's output it acts on.
- **Counter-pin sweep (asserted by grep over the cut pack).** No header or cell says "twelve months to"; no document defines twelve-month income as "the four quarters to the census"; no field-guide line calls the management Q4 "final"; no social-layer line endorses a basis or quotes a figure; the round rules' "twelve-month income at the census" is neutral between R3 and R4, and rule 4.1's second sentence ("for twelve months ending on or after the census before it") decides R4 against the answer; by admitting that twelve-month income can end before the latest quarter it points toward the step-back (R4, the stop), never past it. Andrew Knox's handover note says the six packs are the record and that Ledgerwood will not run September; nothing about method.
- **Licensed wrong belief.** Tony Hughes (grants adviser), in the team thread and once in the prompt: the round is for the groups the March 2026 government cut hit. A belief about purpose, not a basis and not a figure; it points at the June window (R3), which is where the decoy's four names come from.

## Fork grid, cell by cell

| Axis | Cells | Losing cells and the rule each violates |
|---|---|---|
| Window measure | filed year; trailing quarters | filed year violates the packs (no published figure is a financial year) |
| Unit | grant return; organisation | grant return violates the packs and the round rules (one row per organisation) |
| Version basis | latest; accepted by the census; first filed | latest violates the packs (twin pair, 40+ rows); first filed violates the packs (amendments accepted before a census are used) |
| Q4 source | management as held; register less nine months; T | management as held and register-fallback violate the ten residue rows |
| Window end for an unfiled year | natural; step back | natural violates the residue rows |
| Prior window under step-back | stepped; unstepped | unstepped violates the residue rows' prior and fall figures |
| Census day | inclusive; exclusive | exclusive violates three census-day receipts |
| Rule 4.1, the census before | the previous date in rule 2's list; a year back; clause ignored | a year back and ignored violate rule 2's list (both equal R4); the corpus is blind to all three (A54) |
| Rule 4.1, the boundary | on or after; strictly after | strictly after violates J1 2023 and J2 2024 |
| Register as at | census; extract | extract violates the residue rows |
| Fall per cent denominator | prior twelve months; current | current violates every published fall per cent |
| Line test | unrounded at least 10.0; rounded to a decimal | converge: no September fall within 1.5 points of the line under T (C1) |
| Rate precision | hundredth of a cent, within the pot | the round rules and every round sheet |
| Offer rounding | whole dollars half up, then floor and cap | converge: floor and cap are whole dollars, so the order is immaterial (C1); the remainder sits at least NZ$25 from each step edge |
| Maturity | quarters due by the census | converge: no July to September 2026 return exists in the extract (C1) |

## Convention axes (determinism-check A.5, one line per axis)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | organisations holding a current operating grant at 30 Sep 2026 with an admissible window under rule 4.1 and returns covering both compared windows (150 in scope, 132 scored) | filed (round rules) + C2 (each pack lists exactly its in-scope organisations) + C1 (no operating grant starts or ends within 20 days of any census) |
| 2 | Unit of account | the organisation (charity registration number), not the grant return | C2 (packs one row per organisation; R1 fails every round's count) + grants register mapping |
| 3 | Attribution window | a quarter is the calendar quarter its period ends in; asks: Trust money in the quarter it reaches the grantee's account, Steady Ground instalments on rule 7's pay day | C2 (main); for K2, the QFR-24 memo "received from" the Trust ties to the payment run by value date on all 884 new-form returns and to no other attribution (A53), and rule 7 files the pay day the rebuilt instalments take |
| 4 | As-of dating | portal versions accepted by the census, register returns received by the census, both inclusive, New Zealand time | C2 (twin pair, 40+ amended rows, three census-day receipts) + C1 (no portal version accepted within a day either side of any census, so the time zone cannot move a version) |
| 5 | Version basis | the latest accepted version as held at the census | C2 (twin pair 1.97x; R2 misses 40+ rows) |
| 6 | Divisor | fall per cent = fall over the prior twelve months | C2 (every published fall per cent) |
| 7 | Weighting | none: the rate applies per dollar of fall | filed (round rules); nothing to weight |
| 8 | Window length | four quarters | filed ("twelve-month income") + C2 |
| 9 | Boundary inclusivity | census day inclusive; the line at "at least 10 per cent"; rule 4.1's "on or after" | C2 (three census-day receipts; J1 2023 and J2 2024 for 4.1); C1 (no September fall within 1.5 points of the line) |
| 10 | Rounding path | sums of whole-dollar quarters, fall per cent unrounded for the line and shown to one decimal, offers rounded per grantee to whole dollars, rate to the hundredth of a cent | filed + C2 (every pack); graded fall percentages at least 0.02 from a x.x5 edge |
| 11 | Tie-break | the CSV sorts by fall in dollars; the first outside the line is the largest fall per cent under 10 | C1 (no two scored grantees share a dollar fall; the first outside clears the next by at least 0.3 points) |
| 12 | Maturity and censoring | quarters due by the census only; a year whose annual return is not received is censored at its last admissible quarter | C1 (no July to September 2026 return in the extract) + C2 (T) |
| 13 | Order of operations | rate times fall, rounded, then floor and cap; the rate struck after clamping | filed + C2 (floor and cap offers in four rounds); C1 for round-then-clamp against clamp-then-round |
| 14 | Row order | irrelevant | C1 (six file orders give identical outputs, asserted) |
| 15 | Duplicate resolution | dual-grant returns collapse to the latest accepted version across the organisation's grants; rejected versions never count | C2 (March 2023 dual case) + C1 (rejected versions carry the accepted version's total income) |
| 16 | Identity normalisation | charity numbers matched after trimming and upper-casing | C1 (every grants-register number joins after normalisation; no collision) |
| 17 | Netting | none across grantees or across a dual organisation's two returns; a rise is a negative fall and not eligible | filed (round rules) |
| 18 | Dimensional units | NZ dollars throughout; year to date differenced into quarters | C2 (summing year-to-date figures misses every row) |
| 19 | Code and status semantics | version status accepted, rejected, withdrawn (only accepted counts); form line codes on both forms; the register's date_received | filed (field guide) + C2 |
| 20 | Integerisation | whole-dollar offers, rate to the hundredth of a cent, remainder kept in the Fund | filed + C2; flip condition: the struck rate moves only if the pot moved by more than the remainder to the next step (at least NZ$25 either way) |
| 21 | Scope of a stated clause | the reproduction clause governs every published figure (rows, offers, rates), not only the offers; rule 4.1's census before is the previous date in rule 2's list (31 March 2026 at this census) | filed (cutover standard wording; rules 2 and 4.1); the year-back reading equals R4 and is refuted by rule 2's list, not by the corpus, which is blind to it |
| 22 | Forward window contents | the offers commit the pot for December 2026 to November 2027; no forward quantity enters the figure | C1 (the call depends on no forecast) |

## Pack plan and gates

Nineteen files, six formats (csv, xlsx, pdf, docx, md, txt). Names in the Trust's and the bureau's own idiom; final names are set when the pack is cut.

| # | File (working name) | Role | Main call | Asks |
|---|---|---|---|---|
| 1 | `portal_return_lines_2018q3_2026q2.csv` | spine: one row per return version, income line and column (year to date, prior-year comparative), quarters ending Sep 2018 to Jun 2026; at least 60,000 rows | total-income rows | line and memo rows |
| 2 | `grants_register.xlsx` | dimension: grant reference, programme, charity number, organisation, dates, amounts, variations, and the Steady Ground offers sheet (offer, first instalment month, monthly instalment) | scope, unit | dual mapping; K2's rebuilt instalments |
| 3 | `charities_register_returns_extract_20261007.csv` | operating extract: the warehouse's register match, one row per annual return, date received, total gross income, revenue lines | date received, total gross income | referee (revenue lines) |
| 4 to 9 | six `SGF_screen_run_20YY-03.xlsx` | calibration corpus | method | method |
| 10 | round rules (pdf) | governing: scope, line, offer rule, floor, cap, rate precision | yes | population |
| 11 | screen cutover standard (docx) | governing: the reproduction clause | yes | method |
| 12 | 2026-27 budget minute extract (pdf) | governing: the September pot | yes | no |
| 13 | portal form-change notice, November 2024 (pdf) | organ for K1 and K2 | no | yes |
| 14 | `trust_payment_run_2018-07_to_2026-09.csv` | operating extract: the grants payment run (operating and project grants; Steady Ground instalments are paid from the Fund and are not in it) | no | K2 |
| 15 | warehouse field guide (md) | dictionary: field semantics, codes, statuses, the register match | yes | yes |
| 16 | pack provenance record (md) | provenance for every constructed file | no | no |
| 17 | grants team thread, October 2026 (txt) | social layer: Marie Griffin, Liam Bryant, Tony Hughes, Mia Hart, Wiremu Roberts, Andrew Knox | no | no |
| 18 | `canterbury_community_income_survey_2025.xlsx` | distractor: a regional survey of community-sector income by sector | no | no |
| 19 | `grantee_capacity_ratings_2026.csv` | distractor: the grants team's governance and capacity ratings (no filing fields) | no | no |

Gates, asserted: 19 files; 6 formats; the spine at least 60,000 rows (well over 25,000); 2 distractors named in `metadata.json` and nowhere in the pack; 3 deliverables. The spine starts at the quarter ending September 2018 because D1's stepped-back windows at the March 2021 census reach October 2018 (the card's planned spine name, 2020q3 to 2026q3, changes with it; recorded below).

## Deliverables and criteria arithmetic

Prompt shape 05, allocation to a fixed total: each bucket's amount and what it is made of.

1. `steady_ground_sep2026_offers.docx`, the trustees' paper that commits the rate: the rate first; one row per grantee offered with its offer, the part of its fall that was government money and the part that was the Trust's own money; the first grantee outside the line and its fall; how many grantees were scored; and, round by round, how many of Ledgerwood's published rows the screen gives back exactly.
2. `steady_ground_sep2026_screen.csv`, the conformed screen: one row per scored grantee, largest fall in dollars first, with twelve-month income, the twelve months before, the fall in dollars and per cent, the offer, and the government and own-money parts of the fall. Script-written.
3. `steady_ground_sep2026_offers.png`, the offers at a glance: one bar per offer, largest first, each labelled with its amount, the floor and the cap drawn at their values, the rate in the title. Script-rendered.

```
Criteria arithmetic (hardening loop 1): 9 offered grantees x 3 figures (offer, government part,
  own-money part) = 27 + the rate 1 + first outside the line and its fall 2 + count scored 1 + six
  rounds' rows given back 6 + chart parts 5 + CSV row count, columns, order and device columns 4
  + three files 3 = 49 (the generated rubric compresses; expected 30 to 40, over 25; the CSV's 132
  rows carry K1 and K2 for every scored grantee if the rubric grades below the offered set)
Distinct findings: the allocation (rate and offers); the cutover certification (rows given back);
  the government money inside the falls; the Trust's own money inside the falls; the edge of the line.
Named-parts visual: yes. Breakdown at an explicit grain: yes (per grantee). Validity check: yes (the replay).
Over-determination sweep: no ask names, requests or implies a window, and no requested figure can be
  inverted to recover which grantees step back without building the windows (the docx carries no
  fall; the CSV's falls are outputs, never inputs). Asserted by listing every requested figure with
  its inputs and checking none is a window or a received date.
```

## Ask ledger (supplemental-stumping)

**The main call's declared row population.** Portal rows whose line code is total income (old form `TOT_INC`, new form `TOT_REV`), year-to-date column only, for the 147 in-scope organisations, quarters ending September 2018 to June 2026, every version and status; the register extract's `date_received` and `total_gross_income` for those organisations' year-ends in that span; the grants register's scope columns; the six packs; the round rules; the cutover standard; the budget minute; the field guide's definitions of those fields. **Zero device rows and zero hazard rows inside it** (asserted counts: 0 and 0). Texture allowed inside it, asserted inert: a rejected version's total-income row equals its accepted version's; the comparative column on total-income rows equals the prior year's own total as held at every census.

**Pools.** Pool A (coupled to the main call, sitting in the recommendation and critical-components block): the rate, the nine offers (14 at stage 2), the first outside the line and its fall, the count scored, the six rounds' rows given back, the CSV's screen columns and the chart. Pool B (device-carried asks): K1 and K2. No inheriting ask is built in the ask block.

| | K1, government money inside each fall | K2, the Trust's own money inside each fall |
|---|---|---|
| Asked as | for every grantee offered, the part of the fall it is struck on that was government grants and contracts, whole dollars; the same column for every scored grantee in the CSV (left empty for short-form filers) | for every grantee offered, the part of its fall that was money from the Trust itself (operating and project grants and Steady Ground instalments from earlier rounds), whole dollars, negative where the Trust's money rose; the same CSV column, from the payment run and the rebuilt instalments for short-form filers |
| Construction layer | the answer's windows per organisation as held; R3's June windows miss both 30-June offerees, and R4 holds every offeree on the answer's windows, so against the stop only the devices decide | same windows |
| Primary device | D7, a code reissued with a new meaning (hardening loop 1): on the old form (returns to September 2024) `GOV_GRT` is government grants only, with government service contracts inside `FEE_SVC` and visible only as the memo `FEE_SVC_GOV`; from the December 2024 return the same code carries grants and contracts (the notice: the line "keeps its code"). Reading `GOV_GRT` as one series across both forms leaves the old-form contracts out. Silent: the code joins across the forms with no mapping step at all, every total ties, and each financial year's government total ties to the register under either reading (a year's final quarter is the register's figure less the nine-month year to date, so the misread cancels over the year); the screen's windows cut the year, so the error survives in every window holding an old-form quarter | D4, an absent channel (hardening loop 1): Steady Ground instalments are the Trust's own money and stay in reported income (rule 5.4), but they are in neither the grants payment run (operating and project grants only) nor the QFR-24 memo "of which received from Ashworth Pascoe Trust", which ties to that run; they are rebuilt from the grants register's Steady Ground offers sheet (first instalment month, monthly instalment, the twelfth carrying the balance) and rule 7. Silent: the memo equals the run to the dollar on all 884 new-form returns, so the reconciliation a careful solver runs passes on the wrong path; the absence shows only at a cross-file cut, offers sheet against run. Stacked with D8, the clock: each rebuilt instalment falls in the quarter of its pay day (the 20th of the month before the month it is for, or the Friday before), the basis the memo ties to; by the month it is for, one instalment crosses each window boundary |
| Organ pair | structural: the old-form `FEE_SVC_GOV` memo rows and the form column (spine); documentary: the notice ("keeps its code", contracts reported on it, fees and sales lose them) and the field guide's line codes for both forms | structural: the offers sheet (offer, first instalment month, instalment) beside the run's programme column, and the run's `value_date` beside `instalment_for`; documentary: rules 5.4 and 7 and the field guide's description of the run (operating or project grant payments) |
| Hazards stacked | H1, H2, H4; H3 on the CSV column | H1, H5; H3 on the CSV column |
| Aim (lazy delta) | the lazy path (`GOV_GRT` as one series) moves all 9 offered figures by at least 8 per cent or NZ$2,000 (A45) | the lazy path (the payment run alone, which the memo confirms) moves all 9 by at least 8 per cent or NZ$1,000 (A45) |
| Stops (each asserted outside the bin) | S1 `GOV_GRT` on both forms (D7) · S2 re-presented comparatives for old-form quarters (H2) · S3 over-corrected: the whole old fees line moved to government · S4 the right reading on R3's windows (both 30-June offerees) · golden | S0 the payment run alone (D4) · S1 by the month the instalment is for (D8) · S2 rejected payments summed with their reissues (H5) · S3 over-corrected: payments within ten days of a quarter end dropped as in transit · S4 one grant reference for the dual organisation (H1) · S5 R3's windows · golden |
| Files on the causal path | spine, form-change notice, field guide, grants register, register extract, round rules, cutover standard, the six packs (counted once: only the set pins the window) = 8 | spine (the memo), payment run, grants register (the offers sheet), round rules (rules 5.4 and 7), field guide, register extract, cutover standard, the packs, form-change notice = 9 |
| Columns | line_code, form, column, amount, version_status, accepted_at, period_end, grant_ref, charity_no, year_end, date_received, govt_grants_contracts = 12 | the memo amount, value_date, instalment_for, payment_status, reissue_of, amount, programme, grant_ref, offer_amount, first_instalment_for, instalment, charity_no = 12 |
| Separation line | no K1 device or hazard row is a total-income row; the old-form memo and line rows never enter the main computation (count 0) | the payment run and the offers sheet are read by no step of the main call (count 0); memo rows are not total-income rows |
| Use, and how it enters the call (H18) | Wiremu Roberts and the trustees, deciding whether the round is backfilling government: a component of each offer's case | the trustees, seeing where a fall is their own grant or an earlier offer stepping down: a component of each offer's case |
| Reused device | task65's codes reissued (D7 on the silent list), re-skinned as a form code that keeps its name and changes its meaning | task65's and task80's absent channel (D4) with task80 and task83's clock against a filed cutoff (D8), re-skinned |

**Hazard table.**

| Hazard | What it is | Asks it moves | Per-ask delta target |
|---|---|---|---|
| H1 | dual-grant organisations file line detail and receive payments under both references; the project-grant return's lines lag one amendment behind | K1, K2 (the offered dual organisation; the seven dual CSV rows) | at least NZ$1,500 on the offered dual organisation |
| H2 | new-form returns re-present the prior year under the new lines (comparative column), and the re-presentation differs from the old-form returns as held; the field guide says a quarter's record is its own return | K1 (every offered grantee whose windows hold an old-form quarter) | 7 of 9 offered move by 5 per cent or more (asserted at least 6) |
| H3 | short-form filers (small grantees) report total income and two lines only; government lines and the Trust memo are absent, meaning not reported, not zero | K1 and K2 CSV columns (25 scored rows, no offered grantee) | K1 empty, never zero; K2 from the payment run and the rebuilt instalments by pay day, never zero |
| H4 | three returns whose latest delivered version was rejected for line coding (same total); only accepted versions count | K1 (F2 on the June 2025 quarter, F4 on the June 2024 quarter, both offered) | at least NZ$1,000 each (built: NZ$21,866 and NZ$13,004) |
| H5 | two Trust payments rejected by the bank and reissued; the rejected lines stay in the run with a status | K2 (F5, offered, one CSV row) | one instalment (NZ$6,200) |

Composed deltas: every subset of {primary, hazards} mishandled on a K1 or K2 figure lands outside the whole-dollar bin and at least NZ$500 from the golden (asserted per figure). Referee (one per pack): the register extract's revenue lines, filed financial-year totals by category, byte-clean; it arbitrates H2 (re-presented comparatives against the figures as filed) and hands over no window's split. Off path in prose too: the form-change notice, the payment run and the offers sheet are read by no step of the main call, and no document the main call reads mentions government contracts or memo lines. Rule 7's pay day sits in the round rules, which the main call reads; it is the rules' own payment clause, says nothing about income or windows, and acts only on the K2 rebuild.

**Pair arithmetic (Part 0), at the planning weights 38 / 7 / 55.**

```
Hardening loop 1. r (recommendation criteria that survive R4): about 3 (method credit for as-held
  versions, the dual collapse and the full replay); R4 misses the rate (2.40x), five of 14 names and
  every offer amount, the first outside the line and the count scored.
Cracker (lands the answer, habitual battery, D7 and D4 missed): every offered K1 and K2 figure moves
  (A45, A46)  ->  Lc = 0.00  ->  C = 38 + 7 + 0 = 45.0
Mirror (stops at R4): the same windows on all nine answer offerees (A45), so only the devices decide;
  with D7 and D4 missed  ->  Ls = 0.00  ->  S = 3 + 7 + 0 = 10.0
Pair average 27.5 (A50, the generator's simulation); check 55 x (Lc + Ls) = 0 <= 28 - r = 25.
Sensitivity: a cracker that also catches D7 keeps K1 (about half the ask weight): Lc = 0.5, C = 72.5,
  pair 41.3; one that catches both devices keeps the asks and the pair reaches about 55, which is the
  case the main ladder has to prevent (one response on the call, the other off it). If the generated
  rubric files the CSV screen columns and the chart labels (about 12 points) under the asks, where
  the cracker holds 0.9 of them and the mirror 0.45, the pair rises by about 7; the repair is the
  denominator (more K1 and K2 criteria) or trimming the CSV's device-free columns, decided when the
  rubric generates.
Reachability: c (ask weight reachable from the landed call alone) is 0 for K1 and K2.
The two sheets differ in pool A only: against R4 the asks' construction layer is identical (R4 holds
  every answer offeree on the same windows), so the devices carry K1 and K2 alone; against R3 the two
  30-June offerees also miss on both asks (A45). Neither ask is keyed to the rate.
```

## Prompt (stage 2)

`prompt.md`, number-first (the move on the card), 288 words (276 at stage 2), 19.2 words a sentence, context 29 per cent of the prompt, longest paragraph 84 words, two rounding tags under a block convention, no "because"; `voice-check.py 123` flags nothing and the opening move is unique in the batch so far (task117 calendar-first, task118 stakes-first, task120 evidence-first). Hierarchy reads: the call stands alone at the seam ("What I need is the rate the September offers are struck at, in cents per dollar of fall to two decimal places."); the docx clause names one quantity ("That rate opens ..."); the CSV and PNG paragraphs open on the rate. One belief clause (Tony Hughes's view, unattributed by name). The constraint sentence, second in the context since stage 3 (the author's decision at the leak review, below): "The pot is $560,000, with a $15,000 floor and a $150,000 cap on each offer." (NZ$820,000 until hardening loop 1; the figure is the only prompt edit of the loop, and `voice-check.py 123` re-ran clean.) It states the filed constants as the round's furniture, closes no fork (no reading of the pack uses another pot, floor or cap), agrees with the round rules and the budget minute, which keep them as the filed pin, and gives the chart's "the floor and the cap" its antecedent; "It is the first round" became "This is the first round" so the pronoun cannot read as the pot. Deliberately absent: the line, any window, any input file, the register, the management returns, the word "census". Figure walk: the rate (cents, two decimals), 9 offers and 18 parts since hardening loop 1 (whole dollars, block), the first outside the line and its fall (one decimal, block), the count scored, six replay counts, the CSV's seven figure columns and order, five chart parts; unchanged by the stage 3 sentence, which adds constants and no ask, so the criteria arithmetic stands.

## Assertion plan

Every line is an assertion in the generator and a recomputation in an independent verifier that reads only the shipped bytes (its own xlsx parser and plain dictionaries). As built after hardening loop 1: 299 generator assertions across 57 ids (A1 to A51, A53 to A55, SS, TELL, H1), A52 in `ship.py`, 163 verifier checks.

```
September census (the call)
  A1  the answer's rate in [36.00, 48.00] cents, struck as the highest hundredth of a cent within NZ$560,000
  A2  the remainder and the next-step overshoot each at least NZ$25 (built 31 and 66)
  A3  the answer offers exactly the 9 designed grantees, the offered set equals the round rules applied to
      its falls, and the stop (R4) offers its designed 14
  A4  scored: the answer 132, R4 146, R2 and R3 147; R1 produces 154 rows
  A5  the answer's rate at least 1.15x R0's, 1.40x R1's and R2's, 1.30x R3's, 2.00x R4's
  A6  every rung's offered set differs from every other rung's, by name (rung-collision guard)
  A7  names differing and pot re-placed per rung (R0 4 and 25%, R1 and R2 3 and 25%, R3 6 and 35%,
      R4 5 and 45%); the answer's offers are R4's less the five it does not score
  A8  partial cells (30-June unstepped, prior window unstepped, rule 4.1 read strictly) at least 1.10x
      the answer's rate; only 30-June stepped at most 0.80x
  A9  single-violation cells with the step-back (dual returns twice; latest versions; both) and R4's
      two variants at least 8 per cent below the answer's rate
  A10 census day exclusive and register read at the extract: identical rate and offers, 14 fewer and
      6 more scored
  A11 register fallback and overdue-only equal R3 on every row; rule 4.1 read against the census a year
      back equals R4
  A12 no scored grantee's fall within 1.5 points of 10.0 per cent
  A13 the first outside the line is the designed grantee (L_dual) at 6.0 to 8.5 per cent, at least 0.3
      points clear of the next, and R4's first outside is a different grantee
  A14 the cap binds for F1 only and no offer sits at the floor; neither R3 nor R4 caps an offer
  A15 no two scored grantees share a dollar fall
  A16 every graded fall per cent at least 0.02 from a x.x5 edge
  A17 unfiled at the census: 14 (31 March) + 18 (30 June); deadline-day receipts 14; receipts 1 to 7
      October 6
  A55 the answer leaves out exactly the 14 unfiled 31 March grantees, each scored by R4 on the twelve
      months to December 2025 that the March 2026 round published for it; every scored window ends on
      or after 31 March 2026 and the 17 scored 30-June grantees end on it
  A18 dominance: R4's five own offers hold at least 45 per cent of R4's eligible falls; R3's own names
      and the answer's own names against R3 at least 20 per cent each
  A19 each mover's fall by name (decoys unscored by the answer, at most 8.0 per cent on R4 and at least
      15.0 on R3; step-back movers at least 11.5 per cent on R4 or the answer and at most 8.5 on R3)
Corpus
  A20 the six packs written as computed: 797 rows, 71 offers, six rates; T gives back all of them
  A21 R3 gives back 787 of 797 rows, every offer and every rate; the ten misses by name
  A22 each residue miss within 1.2 per cent of income and 1.0 point of fall; none offered; none near the line
  A23 R2 misses at least 40 rows and the offers and rate of at least 4 rounds (built 94 and 4)
  A24 R1's row count fails every round; R0 gives back under 5 per cent of rows (built 10 of 797)
  A25 twin pair identical on every grants-register column and on today's versions; published falls
      1.8x to 2.2x apart; both reproduce only as held
  A26 rival family: twelve rules scored, each one's misses asserted by count, none under 3
  A27 blindness, structural: every year-end quarter inside a March window on the register except the
      ten residue rows
  A28 blindness, case by case: T and R3 identical on the other 787 rows, every offer and rate
  A29 three census-day receipts, each reproduced only inclusive
  A30 every rule the golden composes breaks at least one corpus case when flipped (15 flips, rule 4.1's
      "on or after" among them, 4 cases)
  A54 rule 4.1's clause is blind on the corpus: no published window ends before the census before, J1
      2023 and J2 2024 end on it, and the screen without the clause gives back every pack
Convergence and Gate G
  A31 every return on the register by a census has a trued-up or exact fourth quarter held
  A32 accepted after submitted; version numbers in submission order; no version accepted within a day
      of any census
  A33 no operating grant starts or ends within 20 days of any census
  A34 comparatives on total-income rows equal the prior year's own totals as held at every census
  A35 rejected and withdrawn versions carry their accepted version's total income
  A36 six row orders of every input give identical outputs
  A37 no July to September 2026 return in the extract
  A38 the six 1-to-7-October filers carry exact management fourth quarters
  A39 no pack header, cell or document line states a window end, a fourth-quarter source or knowledge
      time (grep over the cut pack)
  A40 no shipped artifact scores September's grantees; only the six March packs carry offers
  A41 clean-data test, portal cut to the census: the answer, R3 and R4 unchanged, all three different
  A42 clean-data test, register completed with every outstanding return: all three unchanged; lens-swap:
      the 115 filed grantees identical under the answer and R3, the 17 scored 30-June grantees on
      different periods, R4 adds 14 rows on twelve months already scored
  A43 clean-data test, management fourth quarters replaced by audited ones: all three unchanged
Ask layer
  A44 zero device rows and zero hazard rows inside the main call's 5,725 total-income rows; the payment
      run and the offers sheet read by no step of the main call
  A45 every stop's value per offered grantee untouched or at least NZ$500 from the golden; R4 holds
      every offered grantee on the answer's windows; R3's windows miss both 30-June offerees on both
      asks; the lazy paths move at least 8 of 9
  A46 necessity: D7 moves at least 8 of 9 K1 figures, D4 all 9 K2 figures, D8 at least 7; H1 F3 only
      (K1 by NZ$23,270); H4 F2 and F4 only, each by NZ$1,000 or more; H5 F5 only; H2 at least 6 of 9 by
      5 per cent or more; H3 25 short-form rows, K1 empty, none offered
  A47 composed mishandlings: every subset of the devices touching a figure lands at least NZ$500 away
      (74 checks, nearest NZ$1,050)
  A48 over-cleaner: the whole fees line and the ten-day transit rule fail every offered figure
  A49 the referee ties to the golden's financial-year totals (18 offered-grantee years) and to no
      re-presented comparative (9)
  A50 pair simulation: cracker and mirror scored with the habitual battery; pair at or under 40
  A53 the QFR-24 Trust memo equals the payment run by value date on every new-form return (884), and
      Steady Ground money sits outside both on at least 100 (159)
Pack and generator
  A51 input gates: 19 files, 6 formats, spine at least 60,000 rows, 2 distractors in metadata.json only
  A52 two consecutive builds byte-identical; generator and verifier agree on every graded figure, rung
      and grid cell (ship.py)
  SS  the pot, the floor, the cap, the line, the reproduction clause, rule 7's pay day, rule 4.1's
      recency clause, a quarter's own return and accepted versions only: each stated once in the pack;
      no figure in the thread; no em dash
  TELL no round-thousand offer total; pack row counts all differ; no offer on a half dollar; no row count
      in the extract record equals a graded figure
  H1  the house scrub audit is clean on the cut pack
```

## Realism debts

- **A constructed register extract.** The Charities Register is real; this extract is the Trust's warehouse match of fictional organisations, built for the fiction. Mitigation: the provenance record says so in one line (constructed in the warehouse, not downloaded), and the extract carries the warehouse's own column names, never the public register's export layout (H22).
- **Unfiled 31 March grantees carry over half of the stop's eligible falls (56.4 per cent of R4's).** Forced by the ladder: the decisive rung has to re-place at least 45 per cent of the pot, and only the 14 unfiled 31 March grantees fall to rule 4.1. Motivated: organisations under strain file late, the census falls on their filing deadline, and a fall in 2025 followed by a 2026 recovery is what a stabilisation round sees. Stated, not hidden.
- **The residue grantees are all steady.** Forced: every residue row must miss by under 1.2 per cent and move no offer. Mitigation: they are three 31 December grantees (one files every May, as many church-linked trusts do) and two 30-June grantees, each three months late once.
- **Fourteen grantees file on the deadline day and none is near the line.** Forced by A10 (the census-day cell converges on the call). Realistic: deadline-day filing is common; their stability is a design choice the generator asserts.
- **A round pot of NZ$560,000.** A filed appropriation, round by nature; no computed total is round (asserted). It sits inside the range of the six March pots (NZ$540,000 to NZ$720,000), which suits a half-year round.
- **A rule amended three months before the round.** Rule 2 gained the September census on 16 June 2026; rule 4.1's recency sentence is part of the adopted rules and bound for the first time at that census. Realistic: a fund that moves to two rounds a year amends its calendar and nothing else.
- **Six bureau workbooks with one layout.** One bureau, one template, six years.

## Stopping rule

Written before any round or portal result.

- **At ceiling, re-root at stage 1 with this architecture moved to the card's lineage:** two in-house solver rounds in which a plain solver files T's rate (or two portal responses land the call), or two consecutive solves reaching T by different routes. Hardening loop 1 spent one: solver round 1 filed the stage 2 answer through the twelve-month identity. One more plain solve that files 42.55 re-roots; three hardening loops on this architecture is build-pipeline's limit, and a fourth is a re-root.
- **One more repair licensed, at stage 3:** solvers stop at R3 but the pair clears 40 on the asks (a K1/K2 repair or the denominator lever, never a ladder change); or a solver lands T through a route that never touches the corpus residue (find that route, close it, re-run); or a solver files R3 without ever running the replay (the trap fired by omission: keep it, and check the replay ask still reads as a disclosure item).
- **Not a repair:** making the residue louder or quieter after a result. Its size is fixed by Gates C and D, not by difficulty.

## Nearest exemplars

- Capacity Watch (Nonprofit & Grant-making, Agricultural Research Grant Allocation), measured mean 0.36 over four runs: a designation below a line and shares of a fixed reserve by shortfall, from an index rebuilt against 200 filed register cells; the model computed a words-only reading and never tested it against the register. Nearest on decision shape and on the published-results gate.
- Jurupa fiscal diagnostic review (Policy & Education, School District Finance Review), measured mean 0.41 over one run: a growth screen on filed finance data rebuilt after the consultancy closed, with a paragraph making its transmitted results the definition and a data-vintage fork; the model kept the winner and missed the runner-up and counts on an incomplete rule set. Nearest on scenario and on the vintage fork. This build's decisive rung moves the committed set itself, which Jurupa's did not.

## Guard

- Filed corpus (112 cards): PASS. NOTE test.same_driver_older, (time, B, method_or_model_selection) repeats task62's tempo lineage and task85, differentiated on the card. Nearest driver 0.07 (task101).
- Corpus plus the six pilot cards in draw order (simulated with FINGERPRINT_CARDS, nothing registered): WARN repeat.gate_g against task122. Answer: task122 selects an off-policy estimator by a corpus of past outcomes, here the corpus selects a window rule for a conformed income series, and etl_conformance, the other honest label, is blocked by task98 v5's (time, B, etl_conformance) lineage in the window.
- BLOCKs cleared at the draw: shape 01 (the note's own) is held by task116, so 05; patterns A, C and D are held by task114 to task116, so B; (rule, B, etl_conformance) is blocked by task98 v4 in the window and (rule, B, method_or_model_selection) is spent in 14 builds, so gap time leads, which is honest because the hidden rule is a window rule; closed_decision_corpus is held by task121 and task122 in the batch, so parallel_run_overlap, the cutover's replay; register is held by task122, so filed_standard; the furniture (trustees_or_governors, foundation_or_funder) is clear of task114 to task116 and of task120 to task122; the forcing event moved from cutover_or_migration to budget_or_appropriation at batch registration, because ban.forcing_event blocked cutover_or_migration against task117: the September 2026 stabilisation round is itself the allocation round that forces the call, and the in-house cutover stays in the world as background.
- People WARNs cleared by redrawing from the same seed: Patrick Mitchell (task103) and David Eaton (task104) out, Wiremu Roberts in; Benjamin Thompson, Andrea Brown and Jason Smith skipped against task118 and task119.
- WARN repeat.gate_g at batch registration (method_or_model_selection, against task120): answered as before, etl_conformance is the only other honest label and it is blocked by task98 v5 lineage; the two builds share the label, not the mechanism (task120 recovers a filing unit, this build recovers a window rule).
- Hardening loop 1 (2026-10-09): the card's answer, answer_source, driver, driver_concrete and stump rewritten for R5 (no other field moved); `guard.py heart task123`: WARN, no BLOCK (people.first Marie against task67, an older build; the same-driver signature differentiated against task62 and task85; nearest driver 0.08, task70 v2 and task101; nearest stump 0.07, task107); `guard.py validate`: 119 cards, 0 invalid.

## Changes from the source note

- Domain: capital-markets quant research becomes Nonprofit & Grant-making, grantee financial health, because Economics excludes markets trading and a funder owns this call.
- Data: the SEC Financial Statement Data Sets (their hosts are blocked here) become a fully constructed pack with declared provenance: a New Zealand trust's grants-portal returns, its grants register and a charities register extract.
- The stated methodology memo goes: no shipped sentence states knowledge time, the fourth-quarter source or the window, and the cutover standard's reproduction clause on the bureau's six published March-round packs is the only pin.
- Decisive move: ET01's latest-value look-ahead becomes the headline lower rung, and the decisive rule is new: a year's final quarter only from the filed annual return, with the window stepping back where that return was not on the register at the census.
- Call: a retrospective top ten at a past rebalance becomes a forward-facing allocation of the September 2026 stabilisation pot (offers running December 2026 to November 2027).
- Shape 01 becomes 05, and the CSV, PNG and PDF deliverables become DOCX, CSV and PNG.
- Raw material kept: year-to-date to discrete quarters is rung-0 machinery; restated comparatives and the 2024 form revision (the tag-priority analogue) go to the ask layer as devices; fiscal-label alignment drops to texture.

Stage 2 (design) changes, every draw decision kept (pairing, shape 05, the three deliverables, the Trust, the Fund, Ledgerwood, the six personas, the forum and the forcing event):

- The ladder grows from the draw's four rungs to five: the filed-year register basis goes in at the bottom (R0), the draw's rungs 0 to 3 become R1 to R4. The draw's rung 1 carried "lines mapped across the 2024 form revision"; on the main path that is now inert texture (the total-income line is invariant across the forms), and the line mapping is K1's device.
- The world gains 30 June and 31 December balance dates beside 31 March. The 30 June grantees are structurally unfiled at a September census and give the decisive rung weight without an implausible number of deadline-day non-filers; the 31 December grantees supply the only corpus cases that separate T from the overdue rival. The stump sentence is refined to name both stepped-back quarter ends.
- Corpus late filers are 31 December and 30 June grantees only, never 31 March (the equality signature, above).
- The September pot is fixed at NZ$820,000 in the budget minute (NZ$560,000 since hardening loop 1); the line at 10 per cent, the floor at NZ$15,000 and the cap at NZ$150,000 in the round rules.
- The spine starts at the quarter ending September 2018, not 2020, because D1's stepped-back windows at the March 2021 census reach October 2018; the card's planned spine name changes with it when the pack is cut.
- The ask layer is K1 (government money inside each fall) and K2 (the Trust's own money inside each fall), both keyed to the offered set and carried into the CSV; the docx asks for no fall figure. The draw's two figures per offered grantee (offer, fall) become three (offer, government part, own-money part), and the fall lives in the CSV only, so the arithmetic moves from about 42 to 64 before compression.

## Build record

Stage 3, build, 2026-10-09; rebuilt for hardening loop 1 the same day. Generator `generator/build.py` (seeded, deterministic; modules roster, identity, movers, world, plan, screen, lines, asks, tune, design, writers_data, writers_docs, asserts_world, asserts_asks), independent verifier `generator/verify.py` (reads only `target/` and `metadata.json`, parses the xlsx bytes itself, shares no code with the generator), golden script `generator/golden.py` (reads only `target/`, shares no code with either), ship script `generator/ship.py` (two scratch builds, the task-folder build, the verifier, the generator against verifier comparison). Rebuild: `python3 task123/generator/ship.py --task task123 --scratch <scratch dir>` from the repo root, then `python3 task123/generator/golden.py task123/target task123/golden`.

```
GATES (hardening loop 1)
  generator: 299 assertions green across 57 assertion ids (A1 to A51, A53 to A55, SS single-statement,
    TELL generation tells, H1 container audit); verifier: 163 checks green from the shipped bytes (rule
    4.1's blindness per round, the 14 removed grantees against the March 2026 pack, the Steady Ground
    instalments rebuilt from the offers sheet and rule 7, the memo against the run)
  two consecutive scratch builds byte-identical (20 files: target/ and metadata.json); the task-folder pack
    byte-identical to both; generator and verifier agree on 967 figures (every scored row's income, prior,
    fall, fall per cent, offer, K1 and K2; every corpus round; every rival's miss count; every rung's rate;
    every grid cell)
  input gates: 19 files, 6 formats (csv, xlsx, pdf, docx, md, txt), spine portal_return_lines_2018q3_2026q2.csv
    83,450 rows, register match 1,098 rows, payment run 14,618 rows (operating and project grants only);
    distractors canterbury_community_income_survey_2025.xlsx and grantee_capacity_ratings_2026.csv named in
    metadata.json only; deleting both leaves the call unchanged
  containers: house scrub audit clean on target/ and golden/; zip entries at a fixed time; mtimes 7 October
    2026 09:00; leak.py --asof 2026-10-08: REVIEW, no LEAK (Leak review)
```

**The answer.** 42.55 cents per dollar of fall (4,255 hundredths of a cent); 9 offers totalling NZ$559,969, NZ$31 left in the Fund, the next hundredth NZ$66 over the pot; 132 scored of 150 in scope. First outside the line: Amberley Tenancy Advocacy Service (L_dual), 6.4 per cent (6.39; next 5.40). Replay: every round's published rows given back, 118, 124, 131, 137, 142 and 145.

| Key | Grantee | Offer | Fall | Fall % | K1 government part | K2 Trust part |
|---|---|---|---|---|---|---|
| F1 | Mayfield Kai Share Cooperative | 150,000 (cap) | 383,743 | 13.2 | 258,337 | -19,966 |
| A5 | Woolston Sports Education Trust | 109,687 | 257,783 | 18.3 | 103,487 | 36,866 |
| F3 | Tai Tapu Kai Share Cooperative (dual) | 65,770 | 154,572 | 13.2 | 94,431 | -71,516 |
| F2 | Waikari After School Care Society | 59,426 | 139,661 | 13.3 | 73,145 | -8,408 |
| F4 | Papanui Neighbourhood Hub Trust | 51,797 | 121,733 | 14.1 | 41,328 | -6,402 |
| F5 | St Albans Newcomers Network | 41,503 | 97,539 | 14.2 | 54,616 | -6,718 |
| A6 | Sydenham Play Resource Library Society | 37,183 | 87,387 | 14.2 | 34,351 | 2,078 |
| F6 | Shirley Kai Share Cooperative | 26,129 | 61,407 | 13.5 | 28,381 | -4,300 |
| F7 | Kaiapoi Newcomers Network | 18,474 | 43,416 | 13.6 | 22,709 | -2,500 |

The CSV's K1 column is empty for the 25 short-form scored grantees; K2 for them comes from the payment run and the rebuilt instalments. Every scored row's figures are in the verifier's JSON output (`verify.py --json`), which the submission stage reads rather than this note.

**Rungs (September; the answer's rate as a multiple of each).** R0 filed year 36.37 cents (1.170x, 10 offers, 5 names differ, 31.4% of the pot re-placed); R1 per grant return, latest 23.94 (1.777x, 154 rows, 14 offers, 9 differ, 51.1%); R2 one row per organisation, latest 26.54 (1.603x, 13 offers, 8 differ, 51.9%); R3 as held 29.83 (1.426x, 12 offers, 7 differ, 46.2%); R4 the step-back, the stop, 17.76 (2.396x, 146 scored, 14 offers, 5 differ, 55.2%); R5 the answer 42.55. R4 offers the answer's nine plus M Geraldine Carer Respite Network (its largest, NZ$117,289), A2 Heathcote Adult Literacy Project, A3 Burwood Environmental Restoration Trust, A4 Beckenham Music School Trust and C1 Beckenham Carer Respite Network, all on the twelve months to December 2025 the March 2026 pack published for them. R3 offers C1, F1 to F7 and the decoys Y1 Bryndwr Household Budgeting Trust, Y2 Aranui Heritage Society, Y3 Shirley After School Care Society and Y4 Pegasus Community Transport Trust; R2 adds G_R2 Diamond Harbour Whanau Support Services (June 2026 return restated on 5 October); R1 adds L_dual Amberley Tenancy Advocacy Service (project-grant copy left low). R3 floors F7 and R4 floors F6 and F7; only the answer caps an offer.

**Dominance.** R4's five own offers hold 56.4% of R4's eligible falls; R3's own names 46.4% of R3's; the answer's own names against R3 (A5, A6) 25.6% of the answer's. Movers: decoys on R4 -1.45, -1.27, -1.58 and 7.72 per cent, on R3 15.81 to 18.43; step-back movers on R4 or the answer 14.21 to 22.08, on R3 -9.09 to -2.92.

**Grid.** See Correction grid (built values). Nearest single-violation cell R0 at -14.5%, nearest on the main chain -16.1% (per return, as held, step-back); census day exclusive and register at the extract leave the rate and offers unchanged and score 118 and 138.

**Corpus.** 797 rows (118, 124, 131, 137, 142, 145), 71 offers (9, 10, 11, 12, 13, 16), rates 29.77, 38.40, 33.83, 26.54, 30.81 and 20.16 cents, totals offered NZ$539,966, 574,924, 609,983, 649,960, 689,979 and 719,890. Rival misses: R3 10 (787 given back, every offer and rate); V1 overdue only 8; V2 December balance dates 12; V3 Q4 amended after the census 10; V4 current window only 10; V5 unfiled unscored 10; T-strict 3; T-extract 10; register fallback 10; R2 94 rows with offers and rates failing in 4 rounds; R1 119 rows, count failing all 6 rounds; R0 787 (10 given back). Rule 4.1: no published window ends before the census before; J1 Papanui Environmental Restoration Trust 2023 and J2 Rakaia Community Rooms Trust 2024 end on it; the screen without the clause gives back all six packs. Residue rows: D1 Rangiora Family Support Trust in all six rounds, D2 Diamond Harbour After School Care Society in 2022 and 2024, J1 2023, J2 2024; each within 0.79% of income and 0.69 points of fall, none offered. Census-day receipts: J3 Prebbleton Arts Trust (31 March 2023), D2 (31 March 2025), J4 Oxford Community Transport Trust (31 March 2026). Twin pair: Amberley Mental Wellbeing Collective (TA) and Waikari Mental Wellbeing Collective (TB), 11.60 per cent each on today's versions, published 5.9 and 11.6 (1.97x). Rule flips: 15, each breaking at least one corpus case (the latest-across-grants rule exactly one, DU2 St Albans Heritage Society 2023; rule 4.1 read strictly four).

**Ask layer.** Lazy paths: K1 by `GOV_GRT` as one series moves 9 of 9 offered figures by 8% or NZ$2,000; K2 by the payment run alone moves 9 of 9 by 8% or NZ$1,000. Every stop (K1: `GOV_GRT` on both forms, comparatives, whole fees line, project copy, latest delivered; K2: the run alone, instalment month, returned payments, ten-day transit, one grant reference) leaves each offered figure untouched or at least NZ$500 away; R4 holds all nine offerees on the answer's windows; R3's windows miss both 30-June offerees on both asks (K1 by NZ$159,670 and NZ$33,665, K2 by NZ$7,564 and NZ$4,646). Necessity: D7 moves 9 K1 figures, D4 9 K2 figures (F3 by NZ$50,816, A5 by NZ$36,866), D8 9 K2 figures; H1 moves F3 only (K1 NZ$23,270, K2 NZ$20,700); H4 F2 and F4 only (NZ$21,866 and NZ$13,004); H5 F5 only (NZ$6,200); H2 7 of 9 K1 figures by 5% or more; H3 25 short-form scored rows, none offered. Composed mishandlings: 74 subset checks, nearest NZ$1,050 (F6, K2, instalment month). Referee: 18 offered-grantee years tie to the register, 9 re-presented comparative years do not. Memo against run: equal on 884 new-form returns; Steady Ground money outside both on 159. Pair simulation (habitual battery, D7 and D4 missed): cracker 45.0, mirror 10.0, average 27.5. Separation: 0 device or hazard rows in the main call's 5,725 total-income YTD rows of accepted, rejected and withdrawn versions; the payment run and the offers sheet are read by no step of the main call.

**Cast (design keys, never shipped).** Unfiled at the census and filed 1 to 7 October: A2, A4 and four steady grantees; not in the extract: M, A3, C1, Y1 to Y4 and one steady grantee; 14 steady 31 March grantees filed on 30 September 2026. New 30-June grantee not scored: N Bryndwr Community Transport Trust. 31 December grantees: D1, D2, D3 St Albans Neighbourhood Hub Trust. Dual grantees: F3, L_dual, DU1 Governors Bay Community Rooms Trust, DU2 and three steady.

**Hardening loop 1, what moved and what held.** Main call: rule 4.1 gained its second sentence and rule 7 its pay day in `writers_docs.py`; `common.py` gained the census calendar (`prev_census`); `screen.py` reads the clause (on, off for R4, strict and year-back for the grid). The budget minute's September pot moved from NZ$820,000 to NZ$560,000 with the prompt's constraint sentence (Tried and rejected). Ask layer: the QFR-24 government line keeps the code `GOV_GRT` (it was `GOV_GRC`), the notice's sentence on counting Trust money by receipt is gone, the payment run carries operating and project grants only, the offers sheet gained the monthly instalment, the field guide describes both, and H4 and H5 moved onto offered grantees (F2 and F4; F5). Assertions moved with the design: A14 keeps the cap to the answer alone (at NZ$560,000 R3 floors F7 and R4 floors F6 and F7, so the stage 2 "no floor on R3" clause was dropped); A18 keeps both 20 per cent floors and drops the ratio between them (25.6 against 46.4 per cent is 0.55, under the stage 2 ratio of 0.6, and the decisive rung's dominance is R4's 56.4 per cent); A54 and A55 are new. Held: the pack's 19 files and formats, the corpus (rates, rows and offers; the March 2026 total moved from NZ$719,997 to NZ$719,890 with the tuned falls), the twin pair, the residue rows, every rival's miss count, the persona set and the register match's 1 July 2018 horizon.

**Write-up and ship checks (hardening loop 1).** `golden.py` reads only `target/` and writes the paper (recommendation; the rate; the step-back and rule 4.1 in prose, the 14 31 March grantees named as a count and the March 2026 round that scored them; the nine offers with both parts; the first outside the line; the replay table; the purpose answer to the decoy belief; two notes), the 132-row CSV and the chart. It asserts the replay (797 of 797 rows, 71 of 71 offers, 6 of 6 rates), the struck rate against the next hundredth, distinct falls, every stepped-back scored window a 30-June grantee's to March 2026, the 14 not scored under rule 4.1 each equal to its March 2026 pack row on income and the twelve months before (H6, the stated rule back-tested), the rest of the not-scored grantees from mid-2024 or later, and the Trust memo against the run on 884 QFR-24 returns. All 132 CSV rows agree with the generator record and `verify.py --json` on all seven figures; every figure in `submission.md` recomputes from `verify.py --json`. Golden-realism pass after the figures froze: counts under ten in words in the paper's prose, the floor sentence derived from the data (no offer at the floor), the chart opened; no other edit warranted; two golden builds byte-identical. Register pass: H1 audit clean on `target/` and `golden/`, H4 the golden folder holds exactly the three declared files, H6 as above, H8 every rule, clause, file, field and line code cited in the paper and the submission resolves, H11 one `submission.md` and one `prompt.md` and no snapshot, H16 forward dates confined to the two allow-listed columns, H22 the extract record declares the register match constructed.

**Earlier stage 3 changes that still stand.** The author's leak-review decision put the pot, the floor and the cap in the prompt's constraint sentence; the register match covers financial years ending on or after 1 July 2018 (1,213 to 1,098 rows), so no row count in the extract record collides with a graded figure (TELL and a verifier check); the head of grants was redrawn as Marie Griffin after the surface screen (Tried and rejected).

## Leak review

`leak.py task123 --asof 2026-10-08` after hardening loop 1 (the rebuilt pack, the new goldens and write-up, and this note's new stump paragraph): **REVIEW, no LEAK**, 20 REVIEW lines (19 files read, 631 golden figures and 133 candidate names from submission.md, 25 stump terms). At stage 3 the run after the goldens, the write-up and the persona rename returned **LEAK** on four lines and was held for the author, because no honest pack edit cleared the first three. The author's decision (2026-10-09) cleared all four:

- `SGF_round_rules_rev2026-06.pdf` 150,000 and 15,000 (the cap and floor of rule 5.2) and `trustees_budget_minute_2026-27_extract.pdf` 820,000 (the September pot, NZ$560,000 since hardening loop 1): filed pins the screen cannot run without, equal to graded figures only because the offers fill the pot and one offer is capped and one floored by construction (A14). Cleared by stating the pot, the floor and the cap in the prompt, where the leak-check skill exempts a budget or cap the prompt itself states (the script skips every figure the prompt carries). The round rules and the budget minute keep them as the filed pin, each still stated once in the pack (SS).
- `warehouse_extract_record_2026-10-07.md` 1,213: the register match's true row count, colliding by chance with one non-offered grantee's government part (Darfield Men's Workshop Collective, $1,213, a CSV figure). Cleared in the generator on the count's side, so no graded figure moved: the register match now covers financial years ending on or after 1 July 2018, the horizon of the warehouse's other extracts, which drops the 105 returns for 31 March 2018 year-ends and the 10 for 30 June 2018 (1,213 to 1,098 rows). Those years end before the portal's first quarter, so no window, rung, rival or ask reads them, and the filter acts in `write_register` only, after `W["annual"]` and every random stream drawn over it are fixed. A TELL assertion in the generator and a verifier check now hold every row count the record states clear of every graded figure.

The lines of the hardening loop 1 run, each answered:

- REVIEW, round rules 3.3, 4.1 and 5.4: clause numbers the submission cites (rule 3.3, rule 4.1, rule 5.4), read as figures by the sweep; harmless.
- REVIEW, extract record 4.0: the CC BY 4.0 licence; harmless.
- REVIEW, round rules carry 8 of 10 words of the call: the fund's own vocabulary (Steady Ground, offers, cents per dollar of fall); no rate, no count.
- REVIEW, round rules (census, return, annual, december): rule 2's census dates and rule 7's December first instalment; rule 4.1's recency sentence is the filed pin of the decisive rung and is stated once (SS), in the rules' own voice, with no class named and no pointer to the step-back it acts on.
- REVIEW, portal form-change notice (return, quarter, december): the K1 organ (the December 2024 return's line changes); read by no step of the main call.
- REVIEW, extract record and field guide (register, annual, quarter, accepted, december): field and coverage definitions; "December" is the December 2024 form change; neither states knowledge time, the fourth-quarter source or a window end (counter-pin sweep, A39).
- REVIEW, the six screen packs: the calibration corpus, ranking March rounds' grantees on March windows; none ranks September's (A40).
- REVIEW, register match, grants register, payment run, capacity ratings: organisation-keyed data and a declared distractor; none ranks grantees on the September question. The grants register's offers sheet lists earlier rounds' offers, never September's.
- REVIEW, dates after the setting: the grants register's current-term end dates and the portal's year_end column, forward by design.

`guard.py surface task123`, re-run after the leak fix and again after hardening loop 1 with the same result: two promoted pairs and people lines, each answered (the loop added no file, no persona and no organisation name; "Geraldine Mental" is one more organisation-name fragment of the same kind). The prompt sentence moved no pair axis: track_a against task81 is 1.000 (layout, formats and the shared New Zealand) and against task85 0.085 (layout, formats) with the stage 2 prompt and the stage 3 prompt alike, and no prompt-wording axis fires for either. task81: the shared "invented name" is New Zealand, the real geography, and the shared calibration form is outside the three-build ban window. task85: the same-driver signature, differentiated on the card at the draw. people.last Anderson against task118 was real and is fixed by the rename. people.inside (Geraldine, Linwood, Shirley, Carer, Mental) and "not on the card" (Shirley Kai, Tai Tapu and the like): fragments of organisation names (Canterbury places plus "Carer Respite Network", "Mental Wellbeing Collective", "Kai Share Cooperative"), not personas; renaming organisations to satisfy the name parser would game the screen.

## Tried and rejected

- The blueprint's stated-memo architecture (a methodology memo fixing knowledge time, the latest visible submission, tag priority and the year-to-date derivation): rejected because a strong solver implements every stated clause, so the screen becomes a computation; the decisive rule now lives in no shipped sentence.
- Bitemporal look-ahead as the decisive rung: rejected because in a forward round the census and the extract sit a week apart, so latest-value and as-held barely differ live, and point-in-time is a strong solver's reflex; kept as the headline rung-2 move.
- Like-for-like restated comparatives as the decisive rung: rejected because a latest-value build already pairs a quarter with its re-presented comparative, so the natural pipeline lands on the rule.
- The analyst's LTM identity (last annual plus year-to-date less prior year-to-date) as the decisive rung: rejected as a two-item menu that any sweep of the packs scores end to end.
- Merger pro-forma (organic income) and successor-registration linking as the decisive rung: rejected, the first is ET04's mechanism and the second is task81's driver (a unit persisting across identifier changes).
- Excluding the fund's own earlier offers from grantee income: rejected because it needs a filed sentence, and a filed exclusion is read and executed.
- First cut of rung 2 replaced the management fourth quarter with the filed annual return wherever it was on file: rejected because the residual misses would then be exactly the solver's own fallback branch, which points straight at the rule; the trued-up fourth-quarter amendment keeps the register out of every rung below the decisive one.
- Australia as the setting (30 June year-ends, lodgement by 31 December): dropped because task118 in this batch is already Australian; New Zealand's six-month annual return deadline gives the same structural reason.
- Four-rung ladder kept from the draw: extended to five because the stage-2 gate asks five to six; the added rung is the filed-year register basis, a real first read for a funder that the packs refute on every row.
- The overdue rule as a ladder rung (step back only where the annual return was overdue at the census): rejected as a rung because with the 31 December rows in the corpus it leaves residue a solver at that stop can see, and without them the corpus cannot tell it from T, which at a census on the deadline day is a Gate C fork on 32 grantees; kept as a refuted rival.
- 31 March very-late filers as corpus residue: rejected because a full-year step-back makes the published twelve months equal the rebuilt prior twelve months on the same row, an exact signature a row-by-row replay finds.
- A corpus with no residue at all (blind on every row): rejected because the window rule is then pinned by nothing, a Gate C failure on the whole decisive move.
- Paper prototype, first population: the 30 June movers netted to zero, so the "30 June grantees unstepped" partial cell landed 0.7 per cent from T; the 30 June movers must push the rate the same way as the 31 March movers (all toward T).
- Paper prototype: with a small decisive move, the per-return natural build (R1) landed within 1 per cent of T's rate; fixed by having the unfiled grantees carry over half of T's eligible falls, so the decisive rung reverses the chain past every lower rung.
- Paper prototype: two post-census restatements pushing opposite ways left the "T with latest versions" cell 5.5 per cent from T; both now push the same way and are resized (target at least 8 per cent).
- Reserves cover as an ask: rejected because every silent device on a register row (units in thousands, an amended return) also moves total gross income, which T reads, so it cannot stay off the main path.
- The March 2026 instalments still to be paid in the offer window as an ask: rejected on the already-known test (the Trust's finance team holds its own payment schedule).
- A window-end column in the CSV ("twelve months to"): rejected as a leak; asking for each grantee's window end raises exactly the question the decisive rung depends on nobody asking.
- Pack headers reading "twelve months to 31 December": rejected as a counter-pin against every stepped-back row.
- Any device or hold tied to annual-return filing status in the ask layer (for example instalments withheld from late filers): rejected because it would send a solver to the register's dates, the decisive rung's own evidence.
- Build, first population: R1 at 1.222x and the dual-returns cell at -7.8% at once, because both turn on the same dual additions (the offered dual grantee's second row and the lagging project-grant row); repaired by shrinking the common filed decliners and the decoys and lifting two answer names, which widens the gap between T's falls and R2's before the duals are added (R1 1.29x, dual cell -8.5%).
- Build: the offered dual grantee's line lag first ran the same way as the re-presented comparatives and the two cancelled on its K1 (NZ$67 apart composed); the lag now runs the other way, so every subset of mishandlings lands at least NZ$942 off.
- Build: project grants at a flat level made the one-grant-reference stop inert on K2 (a constant flow cancels in a fall); project grants now renew three-yearly at a new level, F3's in May 2025.
- Build: government income spread evenly across quarters left the re-presented comparatives NZ$436 from the answer on one grantee's K1; government grants now arrive lumpily (two strong quarters a year), every comparative stop at least NZ$500 off.
- Rebecca Anderson as head of grants: the surface screen blocked the surname against task118's Jason Anderson (people.last, both in the last twelve builds, drawn concurrently); redrawn from the same seed as Marie Griffin, the first draw not already rejected at the draw stage, renamed in the generator and the golden script.
- The pot, the floor and the cap kept out of the prompt (stage 2, so the solver had to find the filed pin): rejected at stage 3 by the author's decision, because leak.py reads a filed figure as LEAK whenever it equals a graded figure (the offers fill the pot, one is capped and one floored by construction) and exempts only figures the prompt states; they are now in the prompt and stay in the round rules and the budget minute as the filed pin.
- Clearing the 1,213 collision by moving Darfield Men's Workshop Collective's government part: rejected because it moves a graded CSV figure and the line split under it; the register match's row count moved instead.
- Filtering the pre-July-2018 annual returns inside `build_annual`: rejected because `received_date` and `q4_plan` draw from per-organisation sequential streams over the annual returns, so dropping a year there shifts every later true-up date and management fourth quarter in the portal; the filter acts in `write_register` only.
- Solver round 1 (plain, 2026-10-09, proxy 93.8, main call landed, 8 of 9 asks): the R3 stop with ten non-offered residue rows as the only pin of R4 is rejected, because a plain solver replaying the six packs row by row did not write the residue off but reverse-engineered the window from it, in its own words "an annual return in the charities register counts only if date_received is on or before the census ... if the needed annual return has not been received, the screen steps back a quarter", reproduced 797 of 797 rows and struck 27.47 on the answer's 14 names; the trade the corpus-direction section accepted (a solver who investigates D1 finds T in about three steps) is the one a plain solver takes, so the next rung has to sit after that step-back and still return a wrong rate.
- Hardening loop 1 (2026-10-09), the route that made R4 free: the step-back as the decisive rung died to the analyst's LTM identity evaluated on the register as held, which this note had filed only as a rejected rung; the plain solver's own step 4 reads "Twelve-month income at quarter Q is YTD(Q) plus the prior full financial year from the register annual return, less YTD(Q-4). When Q is the organisation's year end, the annual return total is used directly. Q is the latest quarter on or before the census at which both periods can be built; if the needed annual return has not been received, the screen steps back a quarter", and because a trued-up fourth quarter is the annual return less the nine-month year to date, that identity is T by construction: the step-back is the identity's own availability check rather than a second discovery, so no rung that turns on which quarters the register admits can carry the stump, and the next rung has to sit after the window and move a figure the identity cannot see.
- Hardening loop 1, a rung on the management fourth quarter as held (the screen takes the management Q4 only where the trued-up amendment was not yet accepted, as a rung above the step-back): rejected, it fails the clean-data test (replace the management quarters with the audited ones and the answer moves), so sole_data_defect would turn yes.
- Hardening loop 1, a rung on combined group returns (scoring an organisation that files one return for a group differently from its members): rejected, it fails the clean-data test the same way, and it would have needed a new file class in the pack.
- Hardening loop 1, a filed "no repeat window" sentence (an organisation scored in March on twelve months is not scored again on the same twelve months): rejected as phrasing, because it names the class and turns the rung into an exclusion executed on reading; rule 4.1's recency sentence reaches the same rows as a consequence of the window definition and names no class.
- Hardening loop 1, keeping the September pot at NZ$820,000 under R5: rejected, nine offers would strike 73.68 cents, an implausible replacement rate for a stabilisation fund with a cap-bound list; the budget minute and the prompt moved together to NZ$560,000, which strikes 42.55.
- Hardening loop 1, the stage 2 ask devices: rejected after solver round 1 cracked 8 of 9 ask items, because each was narrated in prose a solver reads for the asks (the notice's "count Trust money in the quarter it reaches your bank account" handed over D8; the new code `GOV_GRC` announced the line move and made D3 a mapping; Steady Ground lines in the payment run made the memo check a confirmation); the solver's own step 7 reads "Government money is GOV_GRT + FEE_SVC_GOV on QFR-16, GOV_GRC on QFR-24 ... The Trust's own money is the paid lines in trust_payment_run, by value_date, ... which matches the QFR-24 GRT_NGO_APT memo exactly". Replaced by D7 (`GOV_GRT` keeps its code with a new meaning), D4 (Steady Ground instalments in no run and no memo, rebuilt from the offers sheet and rule 7) and D8 on those instalments.
- Hardening loop 1, H4 on A4's December 2024 quarter and H5 on A3: rejected at the rebuild, because rule 4.1 leaves neither grantee scored; H4 moved to F2 (June 2025 quarter) and F4, first on F4's December 2024 quarter, which sits in neither of F4's windows (31 March balance date, windows ending June) and moved nothing, then on its June 2024 quarter, which the prior window reads; H5 moved to F5.
