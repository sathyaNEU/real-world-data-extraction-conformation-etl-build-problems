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
  Pre-draw identity test: the allocation's arithmetic (offers = clamp(rate x fall), sum = pot) closes
    over falls the pack does not ship; every fall is constructed, and the decisive input (which quarters
    are admissible) is neither filed nor visibly forced. Passed.
```

## Stump sentence

A competent solver rebuilds the screen as held at the 30 September census, collapses the dual-grant returns, gives back every offer and every rate in Ledgerwood's six March-round packs and all but ten non-offered rows, which it writes off as noise, and strikes the offers at a rate at least 1.4 times the answer's (paper run: 52.19 cents against 28.26) on a set that differs by ten names, because it scores the 32 grantees whose 2025-26 annual return was not yet on the register on twelve months to June 2026 built with their management fourth quarter, when the standing method takes a year's fourth quarter only from the filed annual return and stops those grantees' twelve months at the quarter before that year-end (December 2025 for a 31 March balance date, March 2026 for 30 June).

(Refined at design from the draw's sentence, which named only the 31 March grantees; the draw's mechanism is unchanged.)

## Decisive rung

Measured trap: #3, stops at a close but inexact match (decided 8 of 64, 5 under 0.50), gated by #1's reproduction clause, reports a failed back-test and ships anyway (11 of 64, 9 under 0.50): the cutover standard makes the six published March-round packs the definition of the screen, and the obvious point-in-time rebuild gives back all of them but a handful. #11 (beats the headline trap, misses the quiet one; 4 of 64, 2 under 0.50) sets the order: look-ahead is the famous point-in-time trap, and a strong solver beats it first.

Why the corpus is nearly blind, for a computable reason: every earlier round was a March round, and a March census falls six months after the 30 September deadline for the prior year's annual return, so a year is unfiled at a census only for the handful of grantees that filed very late; the September 2026 census falls on the deadline itself, so about a fifth of grantees are unfiled. (Refined at design: the handful is three 31 December grantees, whose returns are not yet due at a March census, and two 30 June grantees three months late; no 31 March grantee is ever a corpus late filer. See "Calibration corpus".)

Corpus direction: under rung 2 the packs reproduce in every row but the handful of late-filer rows. That is the measured architecture's close-but-inexact gate rather than the corpus-direction test's "it reproduces"; the design stage sizes the handful and keeps each miss within about a point of fall so the residue reads as noise, the trade task110 shipped with its $375 a month.

**Corpus direction, settled at design.** Under the stump rung (R3 below, the draw's rung 2) the six packs reproduce 787 of 797 rows, all 71 offers and all six rates; the ten misses are non-offered rows. That is not "it reproduces", and it cannot be made so: those ten rows are the only thing that pins the decisive rule. Without them T is unpinned against R3, and also against the overdue rival (step back only where the annual return was overdue), which reproduces every late-filer row exactly and coincides with R3 at a census held on the 30 September deadline day itself; the corpus separates T from it only through grantees whose return was not yet due at a March census, and the only balance date that supplies them is 31 December. So the refutation is load-bearing for Gates C and D and stays; what is controlled is its loudness, five ways. (1) Size: 10 of 797 rows (1.25 per cent), each within 1.2 per cent of twelve-month income and 1.0 point of fall, none within 5 points of the line under either window, none offered, so no published decision moves. (2) No aggregate: the packs carry no total that a rebuild could tie or miss; the residue lives only at row level. (3) No equality signature: no 31 March grantee is a corpus late filer, because a full-year step-back makes a published twelve months equal the rebuilt prior twelve months on the same row; the residue comes from one-quarter (31 December) and three-quarter (30 June) step-backs, which match no rebuilt figure. (4) No column: the residue grantees share no portal column, and six of the ten carry no fourth-quarter amendment at all. (5) Disclosure framing: the prompt asks for the round-by-round count of rows given back, the measured trap 1 framing that models report and ship past. What this does not buy: a solver who investigates D1 (missing in all six rounds) finds T in about three steps. The trade is the measured top architecture (traps 1 and 3 decided 19 of 64 client tasks, 14 under 0.50) against the doctrine's two portal builds where an argumentative corpus was quoted back; those refuted the naive read in aggregate (task92 v2 by 18.45 per cent, task89 v5 through a workbook total), and this one refutes it on 1.25 per cent of rows, in no total and on no decision.

The residue must not point at the rule: the management fourth-quarter return is trued up to the filed annual return by an amendment once the return is filed, so no rung below the decisive one joins the register and the late filers share no column in the returns; the discriminator lives only in the register's date received.

Proven-in-production checks (Part 6.1): nothing drawn is on the dead list (no filed formula carries the decisive rung, the rule is not a scannable parameter, no shipped column announces it, the pack must not narrate it, there is no argmax under a stated rule, and the natural basis is not the correct one); the S3 discriminator is buildable (the rule is a construction over a join, not one parameter, and not a linear rule in a rate-times-exposure world); L1's sentence can be written (above); L7 holds (the stopping rung gives back all but a handful of published figures). Caution carried forward: once suspected, the step-back is one as-of join on a dated status (filed by the census), so its only defence is that no sentence and no column raises the question.

## Entity and unit of value

The Ashworth Pascoe Trust holds multi-year operating grants with about 150 Canterbury community organisations, and its Steady Ground Fund makes twelve-month stabilisation offers, scored on each grantee's twelve-month income at a census: an offer is the grantee's fall in twelve-month income at a common rate (cents per dollar of fall), raised to a floor of NZ$15,000 or held to a cap of NZ$150,000, the rate struck so the offers spend a fixed pot. Two things both read as the size of a grantee's trouble and rank grantees differently: the fall in dollars (what the offer is struck on) and the fall as a share of the prior twelve months (what the 10 per cent line tests). And two things both read as "twelve-month income": the latest filed financial year on the register (R0) and the trailing four portal quarters at the census (everything above R0), which disagree because the register runs on financial years and the screen on quarters ending at the census.

## Decision

Exactly one rate for the September 2026 round (census 30 September 2026), with the offer set and every offer it implies, committing the trustees' pot of NZ$820,000 (filed in the 2026-27 budget minute) for offers paid monthly from December 2026 to November 2027. Shape 05, allocation to a fixed total. The window is open (forward commitment); every input is a closed quarter or a filed date, so nothing is forecast and the tag stays ETL.

## Answer

```
ANSWER (targets; paper run in brackets)
  The rate: between 26.00 and 34.00 cents per dollar of fall, to the hundredth of a cent   [28.26]
    struck as the highest rate whose whole-dollar offers do not exceed NZ$820,000; the remainder
    left in the Fund sits at least NZ$25 from both step edges (so no per-offer rounding convention
    can move the struck rate by a hundredth of a cent)
  Offered: 14 grantees by name (7 filed 31 March grantees, one of them a dual-grant organisation;
    5 unfiled 31 March grantees; 2 30-June grantees)                                      [14]
  Scored: 146 (the 147 organisations in scope less one new 30-June grantee whose stepped-back
    windows reach before its first return)                                                  [146]
  Cap binds for exactly one offer (an unfiled grantee R3 does not offer); the floor binds for one
    or two (none floor-bound under R3)                                                      [1; 2]
  First grantee outside the line: an unfiled 31 March grantee at 7.0 to 8.5 per cent, which R3
    offers on a June-window fall of 15 per cent or more                                     [7.7; 17.1]
  Line clearance: no scored grantee's fall within 1.5 points of 10.0 per cent under T
  Natural-pipeline position (adapted, see the position table): the answer's rate is the lowest
    cell of the main grid, every lower rung sits at least 1.25 times above it, and the marker
    grantee (T's capped offer) ranks 76th or worse by fall on R1 to R3 and first on T
MARGIN: an allocation has no runner-up; the guard that binds is grid separation on the rate
  (nearest single-violation cell at least 8 per cent away) and on names (R3 differs from T by at
  least 8 names; paper run 10). Stated per the skill: the 1.20x rung-margin floor guards a ranking;
  this build guards a figure and a set, so the separation floor is the one asserted.
```

## Ladder

Five rungs. Candidates are offer sets with their rates; each rung's set differs from every other rung's by name, asserted after every parameter change. Paper run at the September census in brackets (rate, ratio to T, offers, symmetric difference with T's set).

- **R0, the filed-year basis (gap: rule, what "twelve-month income" is).** Twelve-month income is total gross income on the grantee's latest annual return in the register extract, the fall is against the return before. Candidate O0 [73.27 cents, 2.59x, 7 offered, 7 names differ]. Killed by: the six packs, whose twelve-month figures are sums of four portal quarters to the December before each census and match no filed financial year (a filed-year rebuild gives back under 5 per cent of the 797 rows). Why a careful analyst stops here: the annual return is the audited statutory figure, two filed years is how a funder reads a grantee's trend, and nothing in the register looks incomplete.
- **R1, the natural portal build (gap: population, the unit).** Today's portal (extract 7 October 2026), each return's latest accepted version, year to date differenced into quarters, twelve months to June 2026 against the twelve months to June 2025, one row per grant return. Candidate O1 [36.30, 1.28x, 14 offers on 154 rows, 12 differ]. Killed by: the packs carry one row per organisation, and the grants register maps the seven dual-grant organisations' two references to one charity number, so R1's row count exceeds every pack's (by 5 to 7 rows a round). Why stop: it is the textbook ETL build, each grant return is a separate filing under its own reference, and every figure ties to a return.
- **R2, one row per organisation (gap: time, the version basis).** The latest accepted version across each organisation's grants, today's portal. Candidate O2 [42.41, 1.50x, 13 offered, 11 differ]. Killed by: the twin pair and at least 40 corpus rows touched by amendments accepted after their census, which reproduce only on the versions accepted by each census (R2 also misses the offers and rate in at least four rounds). Why stop: dual grants are collapsed, every row now pairs one-for-one with a pack row, and "the latest accepted version is the record" is the warehouse's own convention.
- **R3, as held at the census: the stump (gap: time, knowledge time).** Versions accepted by the census (inclusive), the fourth quarter as held, which is the trued-up figure wherever the annual return was on the register and the management figure otherwise. Candidate O3 [52.19, 1.85x, 12 offered, 10 differ]. Killed by: the ten residue rows (D1 in all six rounds, D2 in two, two 30-June late filers), which reproduce only with the window stopped at the quarter before a year-end whose annual return had not reached the register by that census (register extract, date received). Why stop: it beats look-ahead, gives back every offer and every rate in all six rounds and 787 of 797 rows, every reconciliation the solver writes passes, and the ten misses are small non-offered rows that read as amendment noise.
- **R4, decisive (gap: time, then rule and population).** A year's final quarter exists only as the filed annual return's income less the nine-month year to date, admissible from the register's date received; the trailing window is the latest four consecutive admissible quarters and the prior window steps back with it. At 30 September 2026 the 14 unfiled 31 March grantees' twelve months stop at December 2025 and the 18 30-June grantees' at March 2026; one new 30-June grantee then lacks the eight quarters the round rules require and drops out. Candidate O*, the answer [28.26].

"A solver who does everything right up to rung 3 commits to O3": the stump sentence above.

```
Every rung names a different candidate? yes (asserted by name)
Which rung carries the stump: R4 (R3 is the stop)
Seven survival properties for R4:
  1 written in no shipped sentence ............ yes: no file states knowledge time, the Q4 source or the window; packs carry no window column or header
  2 no sweepable corpus nominates it .......... partial: blind on all 71 offers and 6 rates, sees it on 10 non-offered rows (the settled trade above)
  3 no arithmetic symptom ...................... partial: counts, offers, rates and joins tie; only a row-by-row replay shows ten small misses
  4 not a per-row predicate .................... yes: a construction over a join to another entity's record (the register, by charity number) and a year-end per balance date; once suspected it is one as-of join (the draw's caution)
  5 enumeration is arithmetic .................. construction, not selection: there is no menu of windows; the affected class is enumerable only once the construction is known
  6 no cutover date ............................ yes: the dated event (the March 2026 government cut) is the decoy's belief, and no series steps at the bureau cutover
  7 survives the deletion ...................... yes: no wrong number exists to delete
Worth on the graded quantity (the rate, paper run): R1 to R2 +16.8 per cent, R2 to R3 +23.1, R3 to R4 -45.9
Sign direction: the corrections walk the rate up; the decisive rung reverses it to 22 per cent below R1, the lowest lower rung. R0 sits off the chain (a different measure).
```

## Position table (adapted to an allocation)

The skill's position rule is written for a ranking; here the answer is a rate and a set, so each row carries the rate's ratio to the answer, the names that differ, the share of the pot that goes to different grantees, and the rank by fall of the marker grantee (T's capped offer, an unfiled grantee that fell in 2025 and recovered in 2026).

| Rung | Rate vs T (target / paper run) | Names differing from T | Pot re-placed vs T | Marker's rank by fall |
|---|---|---|---|---|
| R0 | at least 1.25x / 2.59x | at least 4 / 7 | at least 30% / 41.5% | not offered / 10th |
| R1 | at least 1.25x / 1.28x | at least 8 / 12 | at least 40% / 54.4% | below 50th / 81st |
| R2 | at least 1.25x / 1.50x | at least 8 / 11 | at least 40% / 54.4% | below 50th / 76th |
| R3 | at least 1.40x / 1.85x | at least 8 / 10 | at least 40% / 54.4% | below 50th / 76th |
| R4 | 1.00x | 0 | 0 | 1st |

The marker leads no intermediate rung and is never second. No rung sits within 1.15x of the answer's rate (nearest 1.28x).

## Discriminator dominance (adapted)

- Decoy's carried advantage: R3's four decoy names (three cut-hit unfiled 31 March grantees and one with a soft 2025 then the cut) are eligible only on June-window falls of 15 to 22 per cent, carried by the January to June 2026 quarters the standing method does not yet admit for them; they hold at least a fifth of R3's eligible falls [paper run 26.8 per cent].
- Winner's edge on the decisive axis: T's six answer names (four unfiled 31 March grantees that fell in 2025 and recovered in 2026, one 30-June grantee likewise, one 30-June grantee with a mild 2025 fall) hold at least half of T's eligible falls [56.1 per cent].
- Product check: edge 0.561 against advantage 0.268 is 2.09, above 1.2 (target at least 1.5).
- Band check, both directions: every decoy name sits at least 2.0 points below the line under T [2.33]; every answer name sits at least 1.5 points below the line under R3 and at least 1.5 above it under T [1.55; 1.3 for the mild 30-June grantee in the paper run, which the generator lifts to 11.5 per cent or more].
- Disagreement constructed, not drawn: the generator builds each mover's quarterly path deterministically (the seed decides texture only) and asserts both windows' falls per name.

## Correction grid

Four independent toggles at the trailing-quarter measure (unit, version basis, decisive step-back, and the filed-year measure that overrides the other three), so 9 cells, plus seven partial applications of the decisive rule. Paper run, rate against T's 28.26 cents.

| Cell | Rate vs T | Rule it violates |
|---|---|---|
| per return, latest, no step-back (R1) | +28.5% | packs: one row per organisation |
| per return, as held, no step-back | +53.4% | packs: one row per organisation |
| per organisation, latest, no step-back (R2) | +50.1% | packs: versions accepted by each census (twin pair) |
| per organisation, as held, no step-back (R3) | +84.7% | packs: the ten residue rows |
| per return, latest, step-back | -18.0% | two violations, same direction |
| per return, as held, step-back | -10.2% | packs: one row per organisation |
| per organisation, latest, step-back | -11.3% | packs: versions accepted by each census |
| filed-year basis (R0) | +159% | packs: trailing quarters, not financial years |
| answer | 0 | |
| partial: 30-June grantees not stepped back | +13.1% | packs: the two 30-June residue rows |
| partial: only 30-June grantees stepped back | +53.1% | packs: the eight 31 December residue rows |
| partial: current window stepped back, prior window not | +49.3% | packs: prior and fall figures on all ten residue rows |
| partial: register read as at the extract, not the census | +20.7% | packs: all ten residue returns appear in the extract |
| partial: overdue only (V1) | +84.7% (equals R3) | packs: D1 and D2 rows, not yet due when stepped back |
| partial: register fallback, no step-back | +84.7% (equals R3, by construction) | packs: the ten residue rows |
| partial: census day exclusive | 0 on the rate and every offer; 14 CSV rows differ | packs: three census-day receipts counted as received |

Separation: the nearest single-violation cell sits 10.2 per cent from the answer (target at least 8). The only cells near the answer need two violations pointing opposite ways (for example 30-June grantees left unstepped, +13.1, together with dual returns counted twice, -10.2), which is task62's and task65's accepted argument. The census-day cell converges on the call by construction (no deadline-day filer is eligible or near the line under either window) and is separated on the CSV rows; asserted both ways.

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
```

## Pins and counter-pins

- **Filed pins, by authority.** Level 1, the cutover standard (the reproduction clause: the in-house screen may be used only once it gives back every grantee row, every offer and each round's rate in all six published March runs). Level 1, the round rules (scope: organisations holding a current operating grant at the census with returns covering both twelve-month periods the screen compares; one row per organisation; the 10 per cent line on the prior twelve months; offers at the common rate on the fall in dollars, floor NZ$15,000, cap NZ$150,000, whole dollars; the rate struck to the hundredth of a cent as the highest that keeps offers within the pot, any remainder staying in the Fund; offers paid in twelve monthly instalments from the December after the census). Level 3, the trustees' 2026-27 budget minute (September pot NZ$820,000). Level 4, the warehouse field guide (field semantics only: version status values, accepted_at in New Zealand time, line codes on both forms, the register extract's date_received). Level 5, the portal's November 2024 form-change notice, effective from the December 2024 return (ask layer only: line moves, the Trust-money memo, payments counted in the quarter received, comparatives shown for information). Above all of them, since stage 3, the prompt states the pot (NZ$820,000), the floor (NZ$15,000) and the cap (NZ$150,000), the same values the budget minute and rule 5.2 file; nothing in the pack states another, so the top of the hierarchy and the filed pin agree and no counter-pin exists.
- **Empirical pins (corpus, C2).** Trailing four quarters; one row per organisation; as held at the census; T (Q4 only from a received annual return; the window steps back; the prior window with it); census day inclusive; fall per cent on the prior twelve months; rounding and integerisation paths.
- **No pin, deliberately.** Nothing states knowledge time, the fourth-quarter source, the window or that a management return is provisional.
- **Counter-pin sweep (asserted by grep over the cut pack).** No header or cell says "twelve months to"; no document defines twelve-month income as "the four quarters to the census"; no field-guide line calls the management Q4 "final"; no social-layer line endorses a basis or quotes a figure; the round rules' "twelve-month income at the census" is the only definitional phrase and it is neutral between R3 and T. Andrew Knox's handover note says the six packs are the record and that Ledgerwood will not run September; nothing about method.
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
| Register as at | census; extract | extract violates the residue rows |
| Fall per cent denominator | prior twelve months; current | current violates every published fall per cent |
| Line test | unrounded at least 10.0; rounded to a decimal | converge: no September fall within 1.5 points of the line under T (C1) |
| Rate precision | hundredth of a cent, within the pot | the round rules and every round sheet |
| Offer rounding | whole dollars half up, then floor and cap | converge: floor and cap are whole dollars, so the order is immaterial (C1); the remainder sits at least NZ$25 from each step edge |
| Maturity | quarters due by the census | converge: no July to September 2026 return exists in the extract (C1) |

## Convention axes (determinism-check A.5, one line per axis)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | organisations holding a current operating grant at 30 Sep 2026 with returns covering both compared windows (147 in scope, 146 scored under T) | filed (round rules) + C2 (each pack lists exactly its in-scope organisations) + C1 (no operating grant starts or ends within 20 days of any census) |
| 2 | Unit of account | the organisation (charity registration number), not the grant return | C2 (packs one row per organisation; R1 fails every round's count) + grants register mapping |
| 3 | Attribution window | a quarter is the calendar quarter its period ends in; asks: Trust money in the quarter it reaches the grantee's account | C2 (main); filed form-change clause (asks K2) |
| 4 | As-of dating | portal versions accepted by the census, register returns received by the census, both inclusive, New Zealand time | C2 (twin pair, 40+ amended rows, three census-day receipts) + C1 (no portal version accepted within a day either side of any census, so the time zone cannot move a version) |
| 5 | Version basis | the latest accepted version as held at the census | C2 (twin pair 1.97x; R2 misses 40+ rows) |
| 6 | Divisor | fall per cent = fall over the prior twelve months | C2 (every published fall per cent) |
| 7 | Weighting | none: the rate applies per dollar of fall | filed (round rules); nothing to weight |
| 8 | Window length | four quarters | filed ("twelve-month income") + C2 |
| 9 | Boundary inclusivity | census day inclusive; the line at "at least 10 per cent" | C2 (three census-day receipts); C1 (no September fall within 1.5 points of the line) |
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
| 21 | Scope of a stated clause | the reproduction clause governs every published figure (rows, offers, rates), not only the offers | filed (cutover standard wording) |
| 22 | Forward window contents | the offers commit the pot for December 2026 to November 2027; no forward quantity enters the figure | C1 (the call depends on no forecast) |

## Pack plan and gates

Nineteen files, six formats (csv, xlsx, pdf, docx, md, txt). Names in the Trust's and the bureau's own idiom; final names are set when the pack is cut.

| # | File (working name) | Role | Main call | Asks |
|---|---|---|---|---|
| 1 | `portal_return_lines_2018q3_2026q2.csv` | spine: one row per return version, income line and column (year to date, prior-year comparative), quarters ending Sep 2018 to Jun 2026; at least 60,000 rows | total-income rows | line and memo rows |
| 2 | `grants_register.xlsx` | dimension: grant reference, programme, charity number, organisation, dates, amounts, variations | scope, unit | dual mapping |
| 3 | `charities_register_returns_extract_20261007.csv` | operating extract: the warehouse's register match, one row per annual return, date received, total gross income, revenue lines | date received, total gross income | referee (revenue lines) |
| 4 to 9 | six `SGF_screen_run_20YY-03.xlsx` | calibration corpus | method | method |
| 10 | round rules (pdf) | governing: scope, line, offer rule, floor, cap, rate precision | yes | population |
| 11 | screen cutover standard (docx) | governing: the reproduction clause | yes | method |
| 12 | 2026-27 budget minute extract (pdf) | governing: the September pot | yes | no |
| 13 | portal form-change notice, November 2024 (pdf) | organ for K1 and K2 | no | yes |
| 14 | `trust_payment_run_2018-07_to_2026-09.csv` | operating extract: the Trust's own payments to grantees | no | K2 |
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
Criteria arithmetic: 14 offered grantees x 3 figures (offer, government part, own-money part) = 42
  + the rate 1 + first outside the line and its fall 2 + count scored 1 + six rounds' rows given back 6
  + chart parts 5 + CSV row count, columns, order and device columns 4 + three files 3 = 64
  (the generated rubric compresses; expected 35 to 45, comfortably over 25)
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

**Pools.** Pool A (coupled to the main call, sitting in the recommendation and critical-components block): the rate, the 14 offers, the first outside the line and its fall, the count scored, the six rounds' rows given back, the CSV's screen columns and the chart. Pool B (device-carried asks): K1 and K2. No inheriting ask is built in the ask block.

| | K1, government money inside each fall | K2, the Trust's own money inside each fall |
|---|---|---|
| Asked as | for every grantee offered, the part of the fall it is struck on that was government grants and contracts, whole dollars; the same column for every scored grantee in the CSV (left empty for short-form filers) | for every grantee offered, the part of its fall that was money from the Trust itself (operating grant and earlier Steady Ground instalments), whole dollars, negative where the Trust's money rose; the same CSV column, taken from the payment run alone for short-form filers |
| Construction layer | T's windows per organisation as held: a response on R3's windows is wrong on all seven unfiled offerees and lists ten different names | same windows |
| Primary device | D3 meaning: on the old form (returns to September 2024) government service contracts sit inside "fees, sales and service contracts", visible only as a memo line under it; from the December 2024 return they are reported in "government grants and contracts". Label mapping leaves them in trading. Silent: every line maps, totals are identical, and each financial year's government total ties to the register under both mappings (the errors cancel over a year), so the reconciliation a careful solver runs is a false clean; the screen's windows cut the year, so the error survives in every window that holds an old-form quarter | D8 clock: the new form carries a memo "of which received from Ashworth Pascoe Trust"; for old-form quarters the Trust's money comes only from the Trust's payment run. The Trust pays each monthly instalment on the 20th of the month before the month it is for, and grantees book Trust money in the quarter it reaches their account (form-change notice), so attributing payments to the month they are for moves one instalment across every quarter boundary; it bites wherever instalments changed near a boundary (a grant renewed at a new level, a Steady Ground offer starting or ending). Silent: totals by grant tie to the grants register under either attribution |
| Organ pair | structural: the old-form memo rows (spine); documentary: the form-change notice | structural: the run's `value_date` beside `instalment_for`; documentary: the notice's "count Trust money in the quarter it reaches your account" |
| Hazards stacked | H1, H2, H4; H3 on the CSV column | H1, H2, H5; H3 on the CSV column |
| Aim (lazy delta) | at least 10 of the 14 offered grantees move by at least 8 per cent of their government part or NZ$2,000, whichever is larger | at least 10 of the 14 move by at least one instalment |
| Stops (each asserted outside the bin) | S1 label mapping · S2 re-presented comparatives used for old-form quarters · S3 over-corrected: the whole old fees line moved to government · S4 right mapping on R3's windows · golden | S1 by the month the instalment is for · S2 rejected payments summed with their reissues · S3 over-corrected: payments within ten days of a quarter end dropped as in transit · S4 one grant reference only for the dual organisation · S5 right attribution on R3's windows · golden |
| Files on the causal path | spine, form-change notice, field guide, grants register, register extract, round rules, cutover standard, the six packs (counted once: only the set pins the window) = 8 | spine, payment run, form-change notice, field guide, grants register, register extract, round rules, cutover standard, the packs = 9 |
| Columns | line_code, form_version, ytd_amount, prior_year_ytd_amount, version_status, accepted_at, period_end, grant_ref, charity_number, year_end, date_received, register government revenue = 12 | memo ytd_amount, value_date, instalment_for, payment_status, amount, grant_ref, programme, charity_number, accepted_at, period_end, date_received, version_status = 12 |
| Separation line | no K1 device or hazard row is a total-income row; the old-form memo and line rows never enter the main computation (count 0) | the payment run is never read by the main computation (count 0); memo rows are not total-income rows |
| Use, and how it enters the call (H18) | Wiremu Roberts and the trustees, deciding whether the round is backfilling government: a component of each offer's case | the trustees, seeing where a fall is their own grant or an earlier offer stepping down: a component of each offer's case |
| Reused device | task74 and task65 shape (a vintage with invariant totals, a false clean), re-skinned | task80 and task83 shape (a clock against a filed cutoff), re-skinned |

**Hazard table.**

| Hazard | What it is | Asks it moves | Per-ask delta target |
|---|---|---|---|
| H1 | dual-grant organisations file line detail and receive payments under both references; the project-grant return's lines lag one amendment behind | K1, K2 (the offered dual organisation; the seven dual CSV rows) | at least NZ$1,500 on the offered dual organisation |
| H2 | new-form returns re-present the prior year under the new lines (comparative column), and the re-presentation differs from the old-form returns as held; the field guide says a quarter's record is its own return | K1, K2 (every offered grantee whose windows hold an old-form quarter) | at least 8 of 14 offered move by 5 per cent or more |
| H3 | short-form filers (small grantees) report total income and two lines only; government lines and the Trust memo are absent, meaning not reported, not zero | K1 and K2 CSV columns (about 25 rows, no offered grantee) | K1 empty, never zero; K2 from the payment run by value date, never zero |
| H4 | three returns whose latest delivered version was rejected for line coding (same total); only accepted versions count | K1, K2 (two offered grantees) | at least NZ$1,000 each |
| H5 | two Trust payments rejected by the bank and reissued; the rejected lines stay in the run with a status | K2 (one offered grantee, one CSV row) | one instalment |

Composed deltas: every subset of {primary, hazards} mishandled on a K1 or K2 figure lands outside the whole-dollar bin and at least NZ$500 from the golden (asserted per figure). Referee (one per pack): the register extract's revenue lines, filed financial-year totals by category, byte-clean; it arbitrates H2 (re-presented comparatives against the figures as filed) and hands over no window's split. Off path in prose too: the form-change notice and the payment run are read by no step of the main call, and no document the main call reads mentions government contracts, memo lines or payment dates.

**Pair arithmetic (Part 0), at the planning weights 38 / 7 / 55.**

```
r (recommendation criteria that survive R3): about 3 (method credit for as-held versions and the
  dual collapse); R3 misses the rate, every offer (rate 1.85x; the floor- and cap-bound offers differ
  by name or amount), the first outside the line, the count scored and all six replay counts.
Cracker (lands T): K1 leakage 0.25, K2 leakage 0.25  ->  Lc = 0.25  ->  C = 38 + 7 + 13.75 = 58.75
Mirror (stops at R3): 7 of 14 offered names share its construction; devices then hold it to about a
  quarter of those  ->  Ls = 0.125  ->  S = 3 + 7 + 6.9 = 16.9
Pair average 37.8, under the 40 target; check 55 x (Lc + Ls) = 20.6 <= 28 - r = 25.
Sensitivity: if the generated rubric files the CSV screen columns and the chart labels (about 12
  points) under the asks, where the cracker holds 0.9 of them and the mirror 0.45, the pair rises to
  about 44; the repair is the denominator (more K1 and K2 criteria, e.g. each part as a share of the
  prior twelve months) or trimming the CSV's device-free columns, decided when the rubric generates.
Reachability: c (ask weight reachable from the landed call alone) is 0 for K1 and K2.
The two sheets differ in pool A and in K1/K2's construction layer only: K1 and K2 are keyed to the
  offered set, so the seven unfiled offerees (six the mirror does not offer, one it offers on the
  wrong window) move with the decisive construction (the layer the skill builds on purpose); on the
  seven filed offerees the sheets agree and only the devices decide (asserted by the mirror sweep,
  name by name). Neither ask is keyed to the rate.
```

## Prompt (stage 2)

`prompt.md`, number-first (the move on the card), 288 words (276 at stage 2), 19.2 words a sentence, context 29 per cent of the prompt, longest paragraph 84 words, two rounding tags under a block convention, no "because"; `voice-check.py 123` flags nothing and the opening move is unique in the batch so far (task117 calendar-first, task118 stakes-first, task120 evidence-first). Hierarchy reads: the call stands alone at the seam ("What I need is the rate the September offers are struck at, in cents per dollar of fall to two decimal places."); the docx clause names one quantity ("That rate opens ..."); the CSV and PNG paragraphs open on the rate. One belief clause (Tony Hughes's view, unattributed by name). The constraint sentence, second in the context since stage 3 (the author's decision at the leak review, below): "The pot is $820,000, with a $15,000 floor and a $150,000 cap on each offer." It states the filed constants as the round's furniture, closes no fork (no reading of the pack uses another pot, floor or cap), agrees with the round rules and the budget minute, which keep them as the filed pin, and gives the chart's "the floor and the cap" its antecedent; "It is the first round" became "This is the first round" so the pronoun cannot read as the pot. Deliberately absent: the line, any window, any input file, the register, the management returns, the word "census". Figure walk: the rate (cents, two decimals), 14 offers and 28 parts (whole dollars, block), the first outside the line and its fall (one decimal, block), the count scored, six replay counts, the CSV's seven figure columns and order, five chart parts; unchanged by the stage 3 sentence, which adds constants and no ask, so the criteria arithmetic stands.

## Assertion plan

Every line is an assertion in the generator and a recomputation in an independent verifier that reads only the shipped bytes (pyarrow and plain dictionaries where the generator uses pandas). Fifty-three assertions.

```
September census (the call)
  A1  T's rate in [26.00, 34.00] cents, struck as the highest hundredth of a cent within NZ$820,000
  A2  the remainder sits at least NZ$25 from both step edges (no per-offer rounding convention moves the rate)
  A3  T offers exactly 14 named grantees; the offered set equals the round rules applied to T's falls
  A4  T scores 146; R2 and R3 score 147; R1 produces 154 rows
  A5  R0, R1, R2 rates at least 1.25x T's; R3's at least 1.40x
  A6  every rung's offered set differs from every other rung's, by name (rung-collision guard)
  A7  R3 and T differ by at least 8 names; pot re-placed at least 40 per cent
  A8  partial cells (30-June unstepped, only 30-June stepped, prior window unstepped, register as at
      the extract) each at least 1.10x T's rate
  A9  single-violation cells with the step-back (dual returns twice; latest versions) at least 8 per
      cent below T's rate
  A10 census-day-exclusive cell: identical rate and offers to T; exactly 14 CSV rows differ
  A11 register-fallback cell equals R3 on every row; overdue cell equals R3 at September
  A12 no scored grantee's T fall within 1.5 points of 10.0 per cent
  A13 the first outside the line under T is the designed grantee, 7.0 to 8.5 per cent, at least 0.3
      points clear of the next; its R3 fall at least 15 per cent
  A14 the cap binds under T for exactly one grantee, one R3 does not offer; the floor for one or two,
      none floor-bound under R3; R3's cap-bound grantee sits at least NZ$8,000 under the cap on T
  A15 no two scored grantees share a dollar fall
  A16 every graded fall per cent at least 0.02 from a x.x5 edge
  A17 unfiled at the census: 14 (31 March) + 18 (30 June) = 32; deadline-day receipts 14; receipts
      1 to 7 October 6
  A18 dominance: decoy names hold at least a fifth of R3's eligible falls, answer names at least half
      of T's; edge over advantage at least 1.5
  A19 each mover's fall on both windows, by name (decoys at least 2.0 points under the line on T;
      answer names at least 1.5 under on R3 and at least 11.5 per cent on T)
Corpus
  A20 T gives back 797 of 797 rows, 71 of 71 offers, 6 of 6 rates
  A21 R3 gives back 787 of 797 rows, 71 of 71 offers, 6 of 6 rates; the ten misses by name
  A22 each residue miss within 1.2 per cent of income and 1.0 point of fall; none offered; none within
      5 points of the line on either window
  A23 R2 misses at least 40 rows and the offers and rate of at least 4 rounds
  A24 R1's row count fails every round; R0 gives back under 5 per cent of rows
  A25 twin pair identical on every grants-register column and on latest-version figures; published
      falls 1.8x to 2.2x apart; both reproduce only as held
  A26 rival family: each of the 12 rivals' misses asserted by name and count; none under 3
  A27 blindness, structural: every year-end quarter inside a March window has its return received by
      the census except the ten residue rows
  A28 blindness, case by case: T and R3 identical on the other 787 rows, every offer and rate
  A29 three census-day receipts, each reproduced only inclusive; none dated 31 March 2024
  A30 every rule the golden composes breaks at least one corpus case when flipped (list above)
Convergence and Gate G
  A31 every return received by a census has its trued-up fourth quarter accepted by that census or an
      exact management fourth quarter
  A32 no portal version accepted within one day either side of any census
  A33 no operating grant starts or ends within 20 days of any census
  A34 comparatives on total-income rows equal the prior year's own totals as held at every census
  A35 rejected versions carry their accepted version's total income
  A36 six row orders of every input give identical outputs
  A37 no July to September 2026 return in the extract
  A38 the six 1-to-7-October filers carry exact management fourth quarters
  A39 no pack header, cell or document line states a window end (grep over the cut pack)
  A40 no shipped artifact ranks September's grantees; the two distractors change no golden figure
      when deleted (recompute with each removed)
  A41 clean-data test, portal: as-held snapshot gives R3 and T unchanged, T != R3
  A42 clean-data test, register: completed with the eventual returns, T and R3 unchanged, T != R3
  A43 clean-data test, management quarters: audited replacements leave R3 and T unchanged, T != R3
Ask layer
  A44 zero device rows and zero hazard rows inside the main call's declared population (counts written)
  A45 K1 and K2: every stop's value per offered grantee, each outside the whole-dollar bin and at
      least NZ$500 from the golden; lazy deltas as targeted
  A46 necessity matrix: each device and hazard mishandled alone moves exactly the asks in its row
  A47 composed mishandlings: every subset lands at least NZ$500 from the golden on every figure
  A48 over-cleaner: each blanket rule lands on its designed over-corrected stop
  A49 the referee ties to the golden's financial-year totals and to neither S2 window split
  A50 pair simulation: cracker and mirror sheets scored with the habitual battery; pair at or under 40
Pack and generator
  A51 input gates: 19 files, 6 formats, spine at least 60,000 rows, 2 distractors in metadata.json
  A52 two consecutive builds byte-identical; generator and golden agree on every graded figure
  A53 the new-form Trust memo equals the payment run by value date for every grantee and quarter, so
      K2's two sources agree wherever both exist
```

## Realism debts

- **A constructed register extract.** The Charities Register is real; this extract is the Trust's warehouse match of fictional organisations, built for the fiction. Mitigation: the provenance record says so in one line (constructed in the warehouse, not downloaded), and the extract carries the warehouse's own column names, never the public register's export layout (H22).
- **Unfiled grantees carry over half of T's eligible falls.** Forced by the ladder: the decisive rung has to re-place at least 40 per cent of the pot, and only 32 of 147 grantees step back. Motivated: organisations under strain file late, and a 30 June year-end is not due until December. Stated, not hidden.
- **The residue grantees are all steady.** Forced: every residue row must miss by under 1.2 per cent and move no offer. Mitigation: they are three 31 December grantees (one files every May, as many church-linked trusts do) and two 30-June grantees, each three months late once.
- **Fourteen grantees file on the deadline day and none is near the line.** Forced by A10 (the census-day cell converges on the call). Realistic: deadline-day filing is common; their stability is a design choice the generator asserts.
- **A round pot of NZ$820,000.** A filed appropriation, round by nature; no computed total is round (asserted).
- **Six bureau workbooks with one layout.** One bureau, one template, six years.

## Stopping rule

Written before any round or portal result.

- **At ceiling, re-root at stage 1 with this architecture moved to the card's lineage:** two in-house solver rounds in which a plain solver files T's rate (or two portal responses land the call), or two consecutive solves reaching T by different routes.
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
- The September pot is fixed at NZ$820,000 in the budget minute; the line at 10 per cent, the floor at NZ$15,000 and the cap at NZ$150,000 in the round rules.
- The spine starts at the quarter ending September 2018, not 2020, because D1's stepped-back windows at the March 2021 census reach October 2018; the card's planned spine name changes with it when the pack is cut.
- The ask layer is K1 (government money inside each fall) and K2 (the Trust's own money inside each fall), both keyed to the offered set and carried into the CSV; the docx asks for no fall figure. The draw's two figures per offered grantee (offer, fall) become three (offer, government part, own-money part), and the fall lives in the CSV only, so the arithmetic moves from about 42 to 64 before compression.

## Build record

Stage 3, build, 2026-10-09. Generator `generator/build.py` (seeded, deterministic; modules roster, identity, movers, world, plan, screen, lines, asks, tune, design, writers_data, writers_docs, asserts_world, asserts_asks), independent verifier `generator/verify.py` (reads only `target/` and `metadata.json`, parses the xlsx bytes itself, shares no code with the generator), ship script `generator/ship.py` (two scratch builds, the task-folder build, the verifier, the generator against verifier comparison). Rebuild: `python3 task123/generator/ship.py --task task123 --scratch <scratch dir>` from the repo root.

```
GATES
  generator: 314 assertions green across 55 assertion ids (A1 to A53 as planned, plus SS single-statement,
    TELL generation tells including the extract record's row counts against every graded figure, H1 container
    audit); verifier: 124 checks green from the shipped bytes (six read the extract record: its four stated
    row counts equal their files and none equals a figure of the screen)
  two consecutive scratch builds byte-identical (20 files: target/ and metadata.json); the task-folder pack
    byte-identical to both; generator and verifier agree on 1,050 figures (every scored row's income, prior,
    fall, fall per cent, offer, K1 and K2; every corpus round; every rival's miss count; every rung's rate)
  input gates: 19 files, 6 formats (csv, xlsx, pdf, docx, md, txt), spine portal_return_lines_2018q3_2026q2.csv
    83,450 rows (card still carries the planned 2020q3_2026q3 name and 140,000 rows; /approve updates it),
    register match 1,098 rows (financial years ending on or after 1 July 2018), payment run 15,358 rows;
    distractors canterbury_community_income_survey_2025.xlsx
    and grantee_capacity_ratings_2026.csv named in metadata.json only; deleting both leaves the call unchanged
  containers: house scrub audit clean (no writer signature, no out-of-band date); zip entries at a fixed time;
    mtimes 7 October 2026 09:00; leak.py --asof 2026-10-08: REVIEW, no LEAK, after the stage 3 leak fix (see
    Leak review; generic register vocabulary in five documents; forward dates are the grants register's
    current-term end dates and the portal's year_end column, both forward by design)
```

**The answer.** 27.47 cents per dollar of fall (2,747 hundredths of a cent); 14 offers totalling NZ$819,939, NZ$61 left in the Fund, the next hundredth NZ$178 over the pot; 146 scored. First outside the line: Pegasus Community Transport Trust (Y4), 7.7 per cent (7.72; next 6.39). Replay: every round's published rows given back, 118, 124, 131, 137, 142 and 145.

| Key | Grantee | Offer | Fall | Fall % | K1 government part | K2 Trust part |
|---|---|---|---|---|---|---|
| M | Geraldine Carer Respite Network | 150,000 (cap) | 660,409 | 20.3 | 302,510 | -10,800 |
| A2 | Heathcote Adult Literacy Project | 106,458 | 387,542 | 22.1 | 125,528 | 13,877 |
| F1 | Mayfield Kai Share Cooperative | 105,414 | 383,743 | 13.2 | 258,337 | -19,966 |
| A5 | Woolston Sports Education Trust | 70,813 | 257,783 | 18.3 | 103,487 | 36,866 |
| A3 | Burwood Environmental Restoration Trust | 68,195 | 248,253 | 21.0 | 89,049 | 15,122 |
| C1 | Beckenham Carer Respite Network | 63,848 | 232,427 | 14.9 | 138,951 | -61,032 |
| A4 | Beckenham Music School Trust | 58,277 | 212,147 | 18.5 | 115,965 | -36,728 |
| F3 | Tai Tapu Kai Share Cooperative (dual) | 42,461 | 154,572 | 13.2 | 94,431 | -71,516 |
| F2 | Waikari After School Care Society | 38,365 | 139,661 | 13.3 | 73,145 | -8,408 |
| F4 | Papanui Neighbourhood Hub Trust | 33,440 | 121,733 | 14.1 | 41,328 | -6,402 |
| F5 | St Albans Newcomers Network | 26,794 | 97,539 | 14.2 | 54,616 | -6,718 |
| A6 | Sydenham Play Resource Library Society | 24,005 | 87,387 | 14.2 | 34,351 | 2,078 |
| F6 | Shirley Kai Share Cooperative | 16,869 | 61,407 | 13.5 | 28,381 | -4,300 |
| F7 | Kaiapoi Newcomers Network | 15,000 (floor) | 43,416 | 13.6 | 22,709 | -2,500 |

The CSV's K1 column is empty for the 25 short-form scored grantees; K2 for them comes from the payment run. Every scored row's figures are in the verifier's JSON output (`verify.py --json`), which the submission stage reads rather than this note.

**Rungs (September, rate against the answer's).** R0 filed year 58.85 cents (2.142x, 10 offers, 6 names differ, 51.2% of the pot re-placed); R1 per grant return, latest 35.35 (1.287x, 154 rows, 15 offers on 14 names, 12 differ, 58.3%); R2 one row per organisation, latest 39.08 (1.423x, 13 offers, 11 differ, 58.3%); R3 as held, the stop 45.03 (1.639x, 12 offers, 10 differ, 58.3%); R4 the answer 27.47. Marker (M) ranks 153rd, 146th and 146th by dollar fall on R1 to R3 and first on T; offered on no lower rung. R3 offers C1, F1 to F7 and the decoys Y1 Bryndwr Household Budgeting Trust, Y2 Aranui Heritage Society, Y3 Shirley After School Care Society and Y4; R2 adds G_R2 Diamond Harbour Whanau Support Services (June 2026 return restated on 5 October); R1 adds L_dual Amberley Tenancy Advocacy Service (project-grant copy of the June 2026 return left low) and F3's second row. R3's cap-bound offer (F1) is NZ$44,586 under the cap on T.

**Dominance.** Decoys hold 28.9% of R3's eligible falls, the six answer names 60.0% of T's, ratio 2.07. Movers: decoys on T -1.41, -1.18, -1.58 and 7.72 per cent, on R3 15.86 to 18.43; answer names on T 14.21 to 22.08, on R3 -9.09 to -2.92.

**Grid (rate against the answer's).** Per return, as held, no step-back +42.7%; per return, latest, step-back -15.9%; per return, as held, step-back -8.5% (nearest single-violation cell); per organisation, latest, step-back -8.7%; 30-June grantees not stepped back +16.9%; only 30-June grantees stepped back +34.7%; current window stepped back, prior not +58.6%; register read at the extract +33.4%; overdue only and register fallback both equal R3 (+63.9%); census day exclusive: identical rate and offers, 14 CSV rows differ.

**Corpus.** 797 rows (118, 124, 131, 137, 142, 145), 71 offers (9, 10, 11, 12, 13, 16), rates 29.77, 38.40, 33.83, 26.54, 30.81 and 20.16 cents, totals offered NZ$539,966, 574,924, 609,983, 649,960, 689,979 and 719,997; floor or cap offers in 2021, 2022, 2024 and 2026. Rival misses: R3 10 (787 given back, every offer and rate); V1 overdue only 8; V2 December balance dates 12; V3 Q4 amended after the census 10; V4 current window only 10; V5 unfiled unscored 10; T-strict 3; T-extract 10; register fallback 10; R2 94 rows with offers and rates failing in 4 rounds; R1 119 rows, count failing all 6 rounds; R0 787 (10 given back, 1.25%). Residue rows: D1 Rangiora Family Support Trust in all six rounds, D2 Diamond Harbour After School Care Society in 2022 and 2024, J1 Papanui Environmental Restoration Trust 2023, J2 Rakaia Community Rooms Trust 2024; each within 0.79% of income and 0.69 points of fall, none offered, all falls between -1.17 and 0.31 per cent. Census-day receipts: J3 Prebbleton Arts Trust (31 March 2023), D2 (31 March 2025), J4 Oxford Community Transport Trust (31 March 2026). Twin pair: Amberley Mental Wellbeing Collective (TA) and Waikari Mental Wellbeing Collective (TB), identical on every grants-register column and at 11.60 per cent each on today's versions, published 5.9 and 11.6 (1.97x). Dual organisation whose two returns differed as held: St Albans Heritage Society (DU2), March 2023. Rule flips: 14 composed rules each break at least one corpus case (the latest-across-grants rule breaks exactly one, DU2 2023).

**Ask layer.** Lazy paths: K1 by label mapping moves 14 of 14 offered figures by 8% or NZ$2,000; K2 by the month the instalment is for moves 14 of 14 by 8% or NZ$1,000. Every stop (K1: label mapping, comparatives, whole fees line; K2: instalment month, returned payments, ten-day transit, one grant reference) leaves each offered figure either untouched or at least NZ$500 away; R3's windows miss all seven unfiled offerees on both asks. Necessity: D3 moves K1 only, D8 K2 only; H1 moves K1 (NZ$23,270) and K2 for F3 only; H4 moves K1 and K2 for A4 and F2 (each by NZ$1,000 or more); H5 moves K2 for A3 only; H2 moves 12 of 14 K1 figures by 5% or more; H3 covers 25 short-form scored rows, none offered. Composed mishandlings: 112 subset checks, nearest NZ$942 (F7, K2, comparatives). Referee: 30 offered-grantee years tie to the register, all 14 re-presented comparative years do not. Pair simulation (habitual battery, D3 and D8 missed): cracker 45.0, mirror 10.0, average 27.5. Separation: 0 device or hazard rows in the main call's 5,725 total-income YTD rows of accepted, rejected and withdrawn versions; the payment run is read by no step of the main call.

**Cast (design keys, never shipped).** Unfiled at the census and filed 1 to 7 October: A2, A4 and four steady grantees; not in the extract: M, A3, C1, Y1 to Y4 and one steady grantee; 14 steady 31 March grantees filed on 30 September 2026. New 30-June grantee dropped by T: Bryndwr Community Transport Trust (N). 31 December grantees: D1, D2, D3 St Albans Neighbourhood Hub Trust. Dual grantees: F3, L_dual, DU1 Governors Bay Community Rooms Trust (offered March 2023), DU2 and three steady.

**Built against the plan, where it moved.** Paper run to build: T 28.26 to 27.47 cents; R3 1.85x to 1.64x, R2 1.50x to 1.42x, R1 1.28x to 1.29x, R0 2.59x to 2.14x; nearest single-violation cell 10.2% to 8.5%; A9's 8% floor held on both cells. The K2 lazy aim is asserted as 8% of the figure or NZ$1,000; most offered grantees move by exactly one Steady Ground instalment (the March 2026 offers paid from 20 May 2026 sit inside the filed grantees' windows), M by one operating-grant renewal step (NZ$1,200). The pair simulation is a proxy on the planning weights 38/7/55 with r = 3; rerun it on the generated rubric.

**Write-up and ship checks (stage 3, 2026-10-09).** `python3 task123/generator/golden.py` reads only `target/` (shares no code with the generator or the verifier) and writes `golden/steady_ground_sep2026_offers.docx` (the trustees' paper from Marie Griffin: recommendation, the rate, the step-back in prose, the offers table with both parts, the first outside the line, the replay table, the purpose answer to the decoy belief, two notes), `golden/steady_ground_sep2026_screen.csv` (146 rows, nine columns, largest fall first, K1 empty for the 25 short-form rows) and `golden/steady_ground_sep2026_offers.png` (matplotlib, one series, floor and cap labelled at their values, rate in the title). It asserts the replay (797 of 797 rows, 71 of 71 offers, 6 of 6 rates), the struck rate against the next hundredth, distinct falls, every stepped-back window ending December 2025 (31 March) or March 2026 (30 June) with that year's return not received by the census (H6, the stated rule back-tested row by row), every unscored organisation a grantee from mid-2024 or later, and the Trust memo against the payment run on 884 QFR-24 returns. It prints 27.47 cents, 14 offers, $819,939 of $820,000 with $61 left, 146 scored, Pegasus Community Transport Trust 7.7 per cent and the 14 offers with both parts; all 146 CSV rows agree with the generator record and `verify.py --json` on all seven figures. Two counts are stated more exactly than the plan above: 150 organisations hold a current operating grant at the census (rule 3.1), 146 are scored and the four not scored are newer grantees (N, dropped by the step-back, and three too new under any window; the plan's "147 in scope" counted organisations with eight natural quarters), and 31 scored grantees step back (14 at 31 March, 17 at 30 June; the plan's 32 includes N). The golden-realism pass ran after the figures froze (title block and threshold labels on the chart, table grid widths, the header block and keep-with-next headings in the paper, the cap and floor sentence and the unscored count derived from the data); the printed figures were re-diffed unchanged after every edit and two golden builds are byte-identical. Container: docProps carry Marie Griffin and 28 October 2026, the zip entries a fixed time, the PNG no Software chunk; the house audit is clean on `target/` and `golden/`. Register pass: H1 clean, H4 the golden folder holds exactly the three declared files and every visual was opened, H6 as above, H8 every cited file, field, line code and rule number resolves, H11 one submission.md and one prompt.md, no em dash in the write-up or the paper. The persona rename (below) moved exactly three pack files (the thread, the cutover standard, the budget minute); ship.py green after it (313 assertions, 118 verifier checks, two scratch builds byte-identical, generator and verifier agree on 1,050 figures). `guard.py heart task123`: WARN, no BLOCK (people.first Marie against task67, an older build; repeat.gate_g against task120, answered under Guard; nearest stump 0.06, nearest driver 0.07 task101). `guard.py validate`: 116 cards, 0 invalid.

**Leak fix (stage 3, 2026-10-09, the author's decision).** Two changes and nothing else. The prompt gained its constraint sentence (Prompt, above), and `voice-check.py 123` re-ran clean (288 words, 19.2 a sentence, context 29.2 per cent, longest paragraph 84, opening move and hierarchy read unchanged). The generator's `write_register` drops annual returns for financial years ending before 1 July 2018, and the extract record's coverage cell says so (1,213 to 1,098 rows); `build.py` asserts the record's four row counts clear of every graded figure, and `verify.py` checks the same from the shipped bytes, each stated count against its own file. `ship.py` green: 314 assertions, 124 verifier checks, two scratch builds and the task-folder pack byte-identical, generator and verifier agree on 1,050 figures. Against a scratch snapshot taken before the edit (deleted after): 17 of 19 target files and `metadata.json` byte-identical; the register's 1,098 surviving rows identical in every column but the warehouse `match_id`, and the 115 rows gone all end before 1 July 2018; the verifier's corpus, golden, rivals and September sections identical. `golden.py` rebuilds all three goldens byte-identical from the new pack, so the goldens and `submission.md` are unchanged and the golden-realism pass stands. `leak.py`: REVIEW, no LEAK (Leak review).

**Write-up and ship checks re-run on the rebuilt pack (stage 3, 2026-10-09).** `ship.py` green (314 assertions across 55 ids, 124 verifier checks, two scratch builds and the task-folder pack byte-identical, generator and verifier agree on 1,050 figures); the 19 target files and `metadata.json` are byte-identical to the pack before the run. `golden.py` rebuilt all three goldens byte-identical and printed the same figures (27.47 cents, 14 offers, $819,939 of $820,000 with $61 left, 146 scored, Pegasus Community Transport Trust 7.7 per cent, replay 797 of 797 rows, 71 offers, 6 rates). `submission.md` re-checked against the rebuilt pack and kept as written: five blocks, block 4 in the prompt's order, all 146 CSV points and all 14 offer points equal to the golden CSV and to `verify.py --json` on every figure, the replay counts equal to the verifier's, the card's answer verbatim in block 1, no em or en dash in the write-up, the paper or the CSV. Golden-realism pass re-read on the frozen figures with no edit warranted (the chart and the paper were opened; every rule, clause, file, field, line code and form cited in the paper and the submission resolves in the pack). Register pass: H1 audit clean on `target/` (band 2018-01-01 to 2026-10-08) and `golden/` (October 2026), H4 the golden folder holds exactly the three declared files, H6 the stated step-back back-tested row by row in `golden.py`, H8 citations resolve, H11 one `submission.md` and one `prompt.md` and no snapshot, H16 forward dates confined to the two allow-listed columns, H22 the extract record declares the register match constructed. `leak.py`: REVIEW, no LEAK, the same 21 REVIEW lines answered below. `guard.py surface`: the same two promoted pairs and people lines, answered below. `guard.py heart`: WARN, no BLOCK (people.first Marie against task67, an older build; the same-driver signature differentiated against task62 and task85; nearest stump 0.06, nearest driver 0.07 task101). Card fields already true of the submission and the pack (answer, answer_source, spine.rows 83,450, the three deliverables, number-first); `guard.py validate`: 119 cards, 0 invalid.

## Leak review

`leak.py task123 --asof 2026-10-08`, stage 3, after the leak fix and again on the rebuilt pack: **REVIEW, no LEAK** both times, with the same 21 REVIEW lines (19 files read, 703 golden figures and 147 candidate names from submission.md, 25 stump terms). The run after the goldens, the write-up and the persona rename returned **LEAK** on four lines and was held for the author, because no honest pack edit cleared the first three. The author's decision (2026-10-09) cleared all four:

- `SGF_round_rules_rev2026-06.pdf` 150,000 and 15,000 (the cap and floor of rule 5.2) and `trustees_budget_minute_2026-27_extract.pdf` 820,000 (the September pot): filed pins the screen cannot run without, equal to graded figures only because the offers fill the pot and one offer is capped and one floored by construction (A14). Cleared by stating the pot, the floor and the cap in the prompt, where the leak-check skill exempts a budget or cap the prompt itself states (the script skips every figure the prompt carries). The round rules and the budget minute keep them as the filed pin, each still stated once in the pack (SS).
- `warehouse_extract_record_2026-10-07.md` 1,213: the register match's true row count, colliding by chance with one non-offered grantee's government part (Darfield Men's Workshop Collective, $1,213, a CSV figure). Cleared in the generator on the count's side, so no graded figure moved: the register match now covers financial years ending on or after 1 July 2018, the horizon of the warehouse's other extracts, which drops the 105 returns for 31 March 2018 year-ends and the 10 for 30 June 2018 (1,213 to 1,098 rows). Those years end before the portal's first quarter, so no window, rung, rival or ask reads them, and the filter acts in `write_register` only, after `W["annual"]` and every random stream drawn over it are fixed. A TELL assertion in the generator and a verifier check now hold every row count the record states clear of every graded figure.

The remaining lines, each answered:

- REVIEW, round rules 5.4 and 3.3: clause numbers matching two fall percentages in the CSV block; harmless.
- REVIEW, payment run 10,800: the regex joins "2018-10" and an instalment of 800 across a comma; harmless.
- REVIEW, extract record 4.0: the CC BY 4.0 licence; harmless.
- REVIEW, round rules carry 8 of 10 words of the call: the fund's own vocabulary (Steady Ground, offers, cents per dollar of fall); no rate, no count.
- REVIEW, round rules (return, census, annual, december): rule 2's census dates and rule 7's December first instalment; nothing about windows or filing.
- REVIEW, grants team thread (return, register, extract): Liam Bryant listing what the extract holds; no method.
- REVIEW, portal form-change notice (return, quarter, received, december): the K1 and K2 organ (lines from the December 2024 return, Trust money in the quarter it reaches the account); read by no step of the main call.
- REVIEW, extract record and field guide (register, annual, quarter, version, accepted): field and coverage definitions; neither states knowledge time, the fourth-quarter source or a window end (counter-pin sweep, A39).
- REVIEW, the six screen packs: the calibration corpus, ranking March rounds' grantees on March windows; none ranks September's (A40).
- REVIEW, register match, grants register, payment run, capacity ratings: organisation-keyed data and a declared distractor; none ranks grantees on the September question.
- REVIEW, dates after the setting: the grants register's current-term end dates and the portal's year_end column, forward by design (recorded at the build stage).

`guard.py surface task123`, re-run after the leak fix with the same result: two promoted pairs and people lines, each answered. The prompt sentence moved no pair axis: track_a against task81 is 1.000 (layout, formats and the shared New Zealand) and against task85 0.085 (layout, formats) with the stage 2 prompt and the stage 3 prompt alike, and no prompt-wording axis fires for either. task81: the shared "invented name" is New Zealand, the real geography, and the shared calibration form is outside the three-build ban window. task85: the same-driver signature, differentiated on the card at the draw. people.last Anderson against task118 was real and is fixed by the rename. people.inside (Geraldine, Linwood, Shirley, Carer, Mental) and "not on the card" (Shirley Kai, Tai Tapu and the like): fragments of organisation names (Canterbury places plus "Carer Respite Network", "Mental Wellbeing Collective", "Kai Share Cooperative"), not personas; renaming organisations to satisfy the name parser would game the screen.

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
