# task122: which registered ranking policy takes the home carousel's Q1 2027 test slot (realises analytical_tasks note DS01)

Source note: `analytical_tasks/05_decision_support/DS01_carousel-slot-library-fill-off-slate.md` (DS01). This build is its first
realisation, redrawn at checkpoint A on 2026-10-09: the note's world and decision stand, its decisive move does not. Every departure
from the note is listed in `## Changes from the source note`.

## Draw

```
DRAW  (independent draws, checked with ../fingerprint/guard.py)
  Card filed: yes, registered 2026-10-09 after checkpoint A (go on the redraw) (scratchpad cards/task122.json, drawn 2026-10-09; the author registers approved redraws in draw order)
  Verdict: PASS on the filed corpus; WARN with no BLOCK in batch order, behind task119 and task121
  Shape: 07, grid of cells   Gate G mechanism: decomposition_attribution
  Gap: time (decisive), then rule, then population   Pattern: none at the decisive rung (G9), B for the estimator the archive pins
  Domain: Product Analytics   Subdomain (enumerated): experimentation-measurement   Objective: Experiment & Causal Analysis
  Pairing repeated from last build? no (task121 is product-analytics x root-cause, task119 policy-education x anomaly-detection,
         task123 nonprofit-grant-making x etl)
  Stakeholder role: head of marketplace science, recommending to the product leadership team (research_desk)
  Context-artifact type: register (the policy register, specifications only)
  Calibration form: pilot_log (nine archived carousel A/B tests with realised lifts, under a reproduction clause)
  Decision type: pick_one_of_n (one of six registered policies)
  Decisive mechanism: measured trap #13 carried by G9, the leader's in-session orders are mostly listings its buyers were already
         watching and would have bought within days anyway; behind #1 (the archive-pinned estimator, Pattern B, G16) at rung 1 and
         #14 (the eight-cell guardrail, G2) with the fresh-listing floor (G11, #10) at rung 2
  Repeats from prior builds: none on a banned axis, against the filed corpus or in batch order
As-of date: 2026-10-28 (the product leadership team's quarterly planning meeting, where the Q1 2027 test calendar is fixed)
```

Draw details, provisional until the design stage:

- **World.** Vouwlijn (invented), a Dutch peer-to-peer platform where private sellers list second-hand clothing and footwear and
  buyers pay the item price plus a buyer-protection fee; the platform holds no stock. EUR. The call is made on 2026-10-28 for the
  slot that runs 4 January to 28 March 2027 (twelve weeks). Logged carousel sessions run 22 June to 20 September 2026 (13 weeks)
  under a randomised logger that draws one ranking per session from the session's candidate pool and logs its propensity. The
  extract is dated 11 October 2026, so at least 21 days of each buyer's later orders and watch-list activity follow every logged
  session.
- **People** (`guard.py names --geo Netherlands --seed 122`, the same draw as the first draft, with Faye and Rosa still skipped for
  their WARNs). Saar Dries, head of marketplace science and the requester. Tygo Knoers, ranking engineering lead, who owns the logger
  and the policy register. Livia Verhaar, chief product officer, who chairs the planning meeting. Fabian Stoffel, owner of the
  velocity-boost policy. Kayleigh Zeemans, owner of the fresh-listing interleave ranker. Amélie Middelkoop, seller experience lead,
  who owns the fresh-listing commitment. None of them is a voice in the prompt, so there is no roll call to refute.
- **Furniture.** Forum executive_team: the product leadership team assigns the quarter's test calendar. Forcing event
  vote_or_meeting: the 28 October planning meeting. Organisation family software_or_platform.
- **Candidates.** Six registered policies, all eligible from the start: A two-tower personaliser, B velocity boost (two fast-selling
  listings in the buyer's sizes pinned to tiles 1 and 2), C session-sequence model, D local-pickup boost, E sequence ranker with a
  fresh-listing interleave, F seller-diversity re-ranker. Answer E.
- **Spine (planned).** `home_carousel_render_log_2026-06-22_2026-09-20.csv`, about 400,000 rows, one carousel render inside a
  logged session with its candidate-pool id, the ranking the logger drew, its propensity and the in-session orders by tile;
  synthetic.
- **Deliverables (provisional).** `carousel_slot_q1_2027.ipynb`, an executed notebook the requester can rerun: the archive
  reproduction, the six-by-eight grid, the three launch conditions and the call. `carousel_slot_q1_2027_cells.png`, the heatmap for
  the planning deck: six policies by eight cells, the guardrail as the colour break, the chosen policy's column marked, the call in
  the title. Opening move deliverable-first, provisional.
- **Shape arithmetic (shape 07, grid of cells, the native shape for measured effects).** 6 policies x 8 platform-by-tenure cells =
  48 cell values (each policy's 90% lower bound on the change in orders per 1,000 carousel sessions), plus the call with its lift to
  one decimal and its lower bound (3), the condition each of the other five policies fails (5), the archive hit count under the
  adopted estimator (1) and the heatmap's four named parts (4): 61 before the ask layer. The two-gate rule is the lift floor and the
  worst-cell guardrail in the charter, with the fresh-listing floor in the seller commitment, a third file.

**Similarity claim.** No card on file turns on gains a candidate brings forward from what its units would have done anyway inside
the judged window. The nearest driver on file scores 0.09: task118, where a specialist team's effect is restricted to volume a unit
does not already treat, which is a stock the unit already holds rather than orders borrowed from the buyer's own next days. The next
score 0.07 (task60 v2's filed netting of outcomes units already hold, task44 v2's transport of a pooled effect), and no card carries
(time, G9, pick_one_of_n) or (time, G9, decomposition_attribution).

## Stump sentence

A competent solver scores all six registered policies with the session-weighted estimator that alone reproduces the nine
archived carousel tests, takes the charter's lift as the orders the arm's buyers place over the test (which nets the velocity
boost's brought-forward watch-list orders), reads condition (b) in the eight platform-by-tenure cells on the render log's
ordered_tiles and commits the Q1 2027 slot to C, the session-sequence model, at 9.8 extra orders per 1,000 carousel sessions;
the step that lands it there is taking the logger's in-session tile orders as the charter's carousel order rate, when the
charter counts every order placed from the tiles an arm served and buyers under every other ranker come back to order from a
tile left on screen after the session closes (credited to the new session, so only the listing ties the order to its tile),
which puts C's rate in app 0-29 3.8 per cent below the incumbent's, so C fails (b) and E, at 5.7, is the largest lift that
clears every condition.

Shallower stops, each a different name (harden loop 1's ladder): replay over the render rows files D; one propensity weight per
render row files A; session weights with the guardrail on ordered_tiles file C, on in-session orders and on the lift over the
test alike (the second is the stump); the tile count on in-session orders files B. The draw's sentence (B on in-session orders)
was cracked in round 1; it is in `## Tried and rejected`.

## Decisive rung

**Harden loop 1: the decisive rung is now the guardrail count** (measured trap #7 inside #11, generator G13; see
`## Harden loop 1: design`). The text below describes the borrowed-order netting the draw made decisive, which round 1
executed as a default and which is now the ladder's last rung.

**Measured trap #13, "Validates on one population, applies to another": decided 3 of the client's 64 accepted tasks, 2 of them
under 0.50 (established; Halls and Meeting Places Fund 0.34, Rapid Response Program 0.39).** The in-session order measure fits all
nine archived tests because no archived policy surfaced listings its buyers were already watching, and B differs on exactly that
axis. The evidence of the difference sits in reference records (the watch-list events and each buyer's later orders), never in a
sentence. Its companion is #7, "Uses the ready-made measure" (5 of 64, 2 under 0.50): the render log's in-session order column passes
the archive and answers a nearby question. It sits behind #1, "Reports a failed back-test, ships anyway" (11 of 64, 9 under 0.50),
at rung 1 and #14, "Coarsens the segment it was asked about" (3 of 64, 1 under 0.50), at rung 2, which is the architecture of #11,
"Beats the headline trap, misses the quiet one" (4 of 64, 2 under 0.50).

Gate G. Litmus: no reported number or stakeholder conclusion is overturned. The register carries specifications and no lift; the
archive's realised lifts, the logger's propensities and the in-session orders are all correct; the miss is the solver's own correct
in-session estimate taken as the effect over a window it does not cover. surface_read_dependency no, stumping_family
analytical_non_defect, sole_data_defect no. Delete every wrong number: there are none, and the task stays hard because the
counterfactual (what each buyer would have ordered anyway) has to be constructed. Instrument repair: no file the decisive rung
touches is incomplete, stale, superseded, delta-shaped or filtered; the later orders and the watch-list events ship whole, so the
borrowed share is computed from shipped records rather than recovered from something no file observed. Lens swap: the naive read
and the answer are not the same moment (the session against the days after it).

Why it survives the opponent (`stumping` Part 1):

1. Written in no sentence: nothing in the charter, the register or the dictionary says an order can be brought forward.
2. The archive is blind, for a computable reason (L1): in every archived test the in-session lift and the lift over the test
   coincide, because no archived policy surfaced listings from its buyers' own watch lists (the watch-list signal entered ranking only
   with B's 2026 build), so the archive reproduces 9 of 9 under in-session orders and cannot see the borrowed ones.
3. No arithmetic symptom: in-session orders tie to the orders file by session, each buyer's orders total the same under either
   basis, and the dip shows only in a within-buyer window after the session.
4. Not a per-row predicate: it needs each buyer's orders ordered in time after each session, or the watch list joined to the listing
   B pinned, a property of a different entity.
5. Its enumeration is a construction, not a scan over a menu.
6. No cutover date.
7. It survives the deletion.

Checks `stumping` Part 6.1 asks of `proven-in-production.md`:

- **Dead shapes (its Part 4).** The call is still the best qualifying registered policy, which keeps the form "argmax under a stated
  rule over a filed candidate list" (task36) that the author named against the first draft. The defence has changed: the stump
  applies the rule exactly and is wrong about the value it applies it to, and no clause carries the decisive step. "A recovery of what
  an instrument could not observe" (89 v6) does not apply, because every record the netting needs ships. "A device announced by its
  own shipped columns" is a design constraint: no column marks an order as borrowed, and the watch list needs a legitimate role
  elsewhere in the pack so that its presence does not ask the question.
- **Strategy (its Part 3).** S10, the governing verb is causal so the baseline has to be constructed (task51's "brings forward",
  task43's waitlist). The discriminator is that the counterfactual is computable from shipped records: the watched listings the
  logger did not push, and what their watchers did next. L7 holds: the in-session measure is excellent on the closed record (9 of 9),
  which is why it is trusted.

## Ladder sketch

| Rung | What the solver does | Leader | Killed by |
|---|---|---|---|
| 0 | Replay or one weight per render on in-session orders; guardrail read on the platform split; floor on rendered tiles | A, two-tower personaliser | The charter's reproduction clause: replay and per-render weights miss archived tests |
| 1 | The session-weighted estimator, the only one that reproduces 9 of 9 archived tests (#1; twin pair T3 and T7, identical on every archive column and separated only by renders per session) | C, session-sequence model | The guardrail read at the charter's eight platform-by-tenure cells: C fails the app under-30-day cell |
| 2 | Eight cells (#14) and the fresh-listing floor (#10, G11): D misses the floor, F the lift floor | B, velocity boost | Most of its in-session orders are listings already on the buyer's watch list |
| 3, decisive | Split each policy's in-session orders into borrowed and new, by following each buyer's orders over the days after the session or by setting watched-listing orders against what watched listings convert to without a carousel push (#13, G9) | **E, sequence ranker with a fresh-listing interleave** (fourth of six at rung 0) | |

Every rung names a different candidate (A, C, B, E), and E leads no rung before the decisive one. Provisional, every item asserted at
the design stage: E fourth at rung 0; every rung margin at least 1.15x; B's carried in-session advantage over E beaten by E's edge on
the kept share by at least 1.2x (discriminator dominance); the borrowed share convergent across every window from the end of the dip
to the extract; and the partial corrections (one flat haircut on every policy, a one-day window) priced so each lands on a named
wrong policy rather than on E. The asks are the decisive construction by segment (each policy's kept share by cell), built under
`supplemental-stumping` at the design stage.

## Nearest exemplars

1. *Budget on the Halls and Meeting Places Fund balance running out in 2029-30, with 7,283,135 pounds not covered* (Nonprofit &
   Grant-making, Capital Grant Drawdown Forecasting): **measured mean 0.34**. The decisive rung's architecture: a stage schedule that
   passes every backtest only because the office realigns an award's schedule once it starts drawing, applied to awards that have
   not drawn. Here the in-session measure passes every archived test only because no archived policy surfaced watched listings, and
   it is applied to the one policy that does.
2. *Set the 2027 Team plan transcription allowance at 500 minutes per seat per month* (Product Analytics, SaaS Usage Allowance
   Pricing): **measured mean 0.20**. A reproduction-gated series in this domain, the architecture rung 1 uses: a method may be used
   only if it reproduces the published controls, and the obvious construction matches most of them.

## Guard

`guard.py check` on the redraw card (scratchpad `cards/task122.json`, drawn 2026-10-09, not registered): **PASS, exit 0, on the
filed corpus.** Nearest driver similarity 0.09 (task118).

In batch order (a scratch corpus with task119's current card and task121's redraw, both drawn 2026-10-09 and so ahead of this card,
read through `FINGERPRINT_CARDS`): **WARN, exit 0, no BLOCK.** The recent three become task123, task119 and task121.

WARNs answered:

- **repeat.gate_g** (decomposition_attribution against task119 and task121): it is the honest label for netting borrowed orders out
  of a measured lift; task121 decomposes a checkout loss across populations and task119 an excess of deaths across transfer paths,
  and the alternatives (method_or_model_selection, forecasting) would misname the move.
- **repeat.decision** (pick_one_of_n against task121): the note's decision is one policy for one slot, which the author asked to
  keep; task121 picks a sprint fix for a cause, a different decision on a different evidence chain.

How the redraw met the bans without a BLOCK to clear:

- task121's redraw holds product_manager, retailer_or_ecommerce, line_manager_or_team, incident_or_complaint,
  prior_period_close_out, monitoring_export, shape 18 and G3; task123 holds programme_officer, trustees_or_governors,
  budget_or_appropriation, parallel_run_overlap, filed_standard and Pattern B; task120 holds G2 and certified_matrix; task119's
  current card holds committee_or_panel, audit_or_inspection, compliance_or_audit, published_series and Pattern B. The card draws
  none of them. The requester moved from an experimentation lead to the head of marketplace science (research_desk), the world from a
  retail marketplace to a peer-to-peer resale platform (software_or_platform, honest because the platform holds no stock and earns a
  fee), the forum from a growth council to the product leadership team, and the calibration form back to the note's own pilot_log.
- No relabel. The decisive signature (time, G9, decomposition_attribution) is the name a reviewer would give the move, and it
  collides with no card, lineage included.
- The redraw's first carded decisive, (population, G15, method_or_model_selection), also passed the guard and was dropped for Gate G
  rather than for the guard (see Tried and rejected).

Batch note: task119's redraw is still in flight. If it lands on research_desk, software_or_platform, executive_team,
vote_or_meeting, pilot_log, register, shape 07 or a G9 decisive, this card BLOCKs at registration on that axis, and the axis is
redrawn.

## Changes from the source note

1. **Objective: Opportunity Sizing & Decision Support to Experiment & Causal Analysis**, the first draft's honest retag kept. The
   call rests on each policy's causal lift, estimated off-policy from randomised logs and netted against a constructed
   counterfactual; it is not a sized opportunity built from an addressable pool to what can be realised.
2. **Decisive move replaced.** The note's library fill (#9, filed in the test-calendar procedure) is a written rule a strong solver
   follows once no proposal qualifies, so it is gone. The decisive move is now the borrowed-order decomposition (#13 with G9), which no
   sentence states.
3. **The off-slate idea is dropped, not demoted.** All six registered policies are the choice set from the start. Keeping the
   proposals-versus-library split as a lower rung would put a written fallback back on the path to the answer.
4. **Ladder reordered.** The note ran the eight cells at rung 1 and the archive-pinned estimator at rung 2. Here the estimator is
   rung 1 (it hands the lead from A to C) and the cells with the floor are rung 2 (they hand it from C to B), because the decisive move
   has to meet B.
5. **Candidates.** B is now a velocity boost that pins two fast-selling listings in the buyer's sizes (the note's trending boost);
   E keeps the fresh-listing interleave; D and F are new registered policies in place of the note's unscored library entries.
6. **World.** A Dutch peer-to-peer resale platform instead of a fashion marketplace selling through third-party sellers, so the
   organisation family is honestly software_or_platform; the fresh-listing floor is a commitment to private sellers; the watch list
   and its price-drop alerts are the platform's own features. The note's checkout and seller-merge material is left to the ask layer.
7. **Requester, forum and forcing event.** The head of marketplace science recommends to the product leadership team at its quarterly
   planning meeting. The note's growth council and its licensed wrong basis (replay among the proposals) are dropped.
8. **Calibration and context artifact.** The archive is keyed pilot_log, the note's own form (the first draft keyed
   closed_decision_corpus while pilot_log was banned). The context artifact is the policy register, carrying specifications and no
   lift figure.
9. **Shape and deliverables.** Shape 07, the grid that natively carries this objective, replaces the first draft's shape 10. The
   note's three files become an executed notebook and a cell heatmap.
10. **People and dates.** Guard-drawn names and the dates above; none of the companies in the note's Mirrors line appears anywhere in
    the build.
## Stage 2: design (2026-10-09)

Harden loop 1 supersedes this section's ladder, position table, dominance, correction grid, guardrail figures and
ask ledger (`## Harden loop 1: design`); the rest stands.

Skills run in order: build-pipeline (stage 2 row), stumping (Parts 1 to 5 and 13), determinism-check (section A),
supplemental-stumping, guide-to-prompt (shape 07, prompt-voice, prompt-economy). Every number below is a target the
generator asserts (stage 3); unrounded targets are given where a graded figure depends on them.

### What the design stage settled

1. **The graded grid is no longer the guardrail read.** The draw's 48 cells were each policy's guardrail value by cell.
   That read is on the main call's path and every response that reaches rung 3 computes it; on the kept basis only B's
   row differs from the in-session row by more than a rounding bin, so 48 graded guardrail cells would hand the
   response that lands E all of them and hand the best response that stops at B about 40 of them, and the pair could
   not reach 40 (supplemental-stumping Part 0). The shape stays 07: the graded grid is each policy's change in
   buyer-protection fee income per 1,000 carousel sessions in each of the charter's eight cells during the slot.
   Its construction layer is the kept orders by cell (the decisive move), its device layer sits on the price and
   fee path the main call never reads. The guardrail stays on the heatmap as hatching on the breaching cells, not as
   the colour.
2. **No graded lower bound, and no variance method in any pass or fail.** The draw graded 90 per cent lower bounds.
   A delta-method bound and a bootstrap bound differ in the first decimal, so the charter's conditions are written
   as point-estimate rules: the lift at least 2.0 extra orders per 1,000 carousel sessions, no cell more than 1.5 per
   cent below the incumbent, at least 12 of every 100 tiles in positions 1 to 6 on listings under 48 hours old.
   Every condition passes or fails on a point figure with a stated margin.
3. **The basis is pinned once, as the observable.** The charter defines lift as the change in orders the arm's buyers
   place over the test, per 1,000 carousel sessions. Without that clause in-session against over-the-test is an open
   fork (Gate C); with it the basis is fixed and the answer still needs the construction. The archive's realised
   lifts are measured on that definition, which is why the in-session estimate matching them is L7 excellence on the
   closed record rather than a refutation.
4. **The stump sentence's "most of B's in-session orders" reads as the orders B adds.** 7.58 of B's 8.03 extra
   in-session orders per 1,000 are listings on the buyer's watch list at session start; 4.73 of them would have been
   bought by the same buyer within six days anyway. The card's sentence is unchanged; this is its arithmetic.
5. **The borrowing is over by day 6.** Every borrowed purchase in the data falls 1 to 6 days after the session, so any
   follow-up window from 7 days to the 21 days the extract allows returns the same kept lift for every policy (C1).
   Windows of 1 to 3 days still name B; 4 to 6 days name E with a wrong runner-up figure (priced in the grid below).
6. **The corpus-direction test, in one sentence.** Under the naive path (session-weighted, in-session orders) the
   archive reproduces 9 of 9: it reproduces, it never refutes, so it cannot be quoted back as evidence for the
   decisive rung.
7. **The pre-draw identity test.** The governing arithmetic is kept lift = in-session lift minus the orders the
   buyer would have placed anyway inside the test; the last term is neither filed nor visibly forced, it is a
   counterfactual built from the orders record and the watch list, so the identity does not close over shipped
   quantities.
8. **Instrument repair (the concern the draw raised), settled.** The record that observes the decision's own
   quantity, every buyer's orders by date across all channels with the watch list beside it, ships complete through
   11 October. The render log's in-session order column is a correct convenience measure of in-session orders, the
   one the archive certifies. No instrument can observe what a buyer would have ordered without the push; that is a
   counterfactual, and the randomised logger plus the complete orders record make it computable. The residual risk
   (a judge reading the in-session column as the instrument and a window count as its repair, which would make the
   move a lens swap) is carried in Realism debts and in the stopping rule, and it is why the decisive rung is built
   as a decomposition with a window that has to be found, not as an outcome column to swap.
9. **The source note's checkout-retry and seller-merge asks are not used.** The ask layer is rebuilt below on the fee
   path and the traffic path, both off the main call's rows.
10. **Deliverables, personas and furniture stay as drawn**: `carousel_slot_q1_2027.ipynb` and
    `carousel_slot_q1_2027_cells.png`, the six guard-drawn names, executive_team, vote_or_meeting,
    software_or_platform, deliverable-first opening.
11. **The ladder has five rungs, not the draw's four.** The pipeline asks for five to six. The fifth distinct
    leader comes from splitting the shallow estimators: replay over the render rows, unweighted, leans on the cells
    where the logger served D most and names D; propensity weights per render row then name A (measured trap #2,
    the file's rows taken as the unit). Both are refused by the archive on different tests, the session estimator
    names C, the eight cells name B, the decomposition names E.

### Gate G

**Gate G line.** decomposition_attribution (each policy's measured in-session gain split into orders it adds and
orders it brings forward from the buyer's own next days), with method_or_model_selection at rungs 1 and 2 ·
surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no · deletion test passes ·
not a lens swap.

- **Litmus, as a sentence.** No reported number or stakeholder conclusion is overturned: the register carries
  specifications and no lift, the archive's realised lifts, the logger's propensities, the render log's in-session
  orders and the orders record are all correct, and no shipped artifact ranks the six policies on any basis; the
  miss is the solver's own correct in-session estimate taken as the effect over a test it does not cover.
- **Primary mechanism.** decomposition_attribution. Removing it collapses the difficulty to rung 3 (B).
- **Deletion test.** Delete Fabian Stoffel's belief, Tygo Knoers's note and every other voice: the archive still
  certifies the session-weighted in-session estimate 9 of 9, the eight cells still remove A and C, the floor D and
  the lift bar F, and nothing says an order can be brought forward. Still hard.
- **Clean-data test, per suspect file.** The only file the decisive rung touches that is limited by design is the
  archive (in-session orders only). Repair it in the generator by adding each archived session's follow-up orders:
  the kept construction then also reproduces 9 of 9 (no archived policy surfaced watched listings ahead of others),
  so answer(repaired) = E, naive(repaired) = B, answer != naive. Asserted.
- **Lens-swap test.** The naive read is the session; the answer is the session plus the days after it, and it is
  reached by splitting the gain (route 2) or by following each buyer (route 1) over a window the solver has to find.
  Not the same moment.

### Entity, unit of value and decision

Vouwlijn runs a peer-to-peer marketplace for second-hand clothing and footwear in the Netherlands, holds no stock, and
earns a buyer-protection fee on every item bought; its home carousel is scored on orders. The two quantities that
both read as a policy's size: the extra **in-session carousel orders** per 1,000 carousel sessions (what the logger
records and the archive certifies) and the extra **orders the buyers place over the test** per 1,000 carousel
sessions (what the charter defines). They rank the candidates differently because one policy, B, gets most of its
in-session gain from listings its buyers were already watching and would have bought within days.

**Decision.** Exactly one policy from {A two-tower personaliser, B velocity boost, C session-sequence model, D
local-pickup boost, E sequence ranker with a fresh-listing interleave, F seller-diversity re-ranker} for the home
carousel's single A/B slot, 4 January to 28 March 2027, filed at the 28 October 2026 planning meeting. Forward
facing: the call commits the coming quarter.

### The answer

**E**, kept lift **5.7** extra orders per 1,000 carousel sessions (unrounded target 5.698). Rank on the natural
pipeline: **4th of 6** (session-weighted in-session: C, B, A, E, D, F), 4th under render weights and 5th under
replay over the render rows. Runner-up on the correct basis: **B at 3.3** (3.302); gap **2.4** (2.396). Margin **1.726x**.

### The world in numbers (generator targets)

- **Logger.** 22 June to 20 September 2026. The logger enrols one home-carousel session per buyer from a 6 per cent
  buyer slice, draws one of seven rankers for it (the incumbent R0 or a registered policy A to F) with a logged
  propensity, and re-renders that ranking on every carousel render in the session. 150,400 logged sessions,
  405,000 renders (2.69 a session). The extract is dated 11 October 2026, 21 days after the last session.
- **Cells (charter table).** app and web, by buyer tenure under 30 days, 30 to 179, 180 to 729, 730 and over.
  Session shares: app 7.4 / 13.8 / 19.6 / 23.9, web 4.1 / 8.2 / 10.9 / 12.1 per cent. Renders a session by tenure
  band: 4.1, 3.0, 2.3, 1.9 (new buyers browse the carousel most).
- **Base.** Incumbent in-session carousel orders 62.0 per 1,000 carousel sessions, session-weighted.
- **The slot's planned traffic (asks only).** The same ISO weeks of 2026 (weeks 2 to 13): 31.4 million logged-in
  home-carousel sessions, 64.7 per cent on the app. The arm takes 10 per cent on each platform, app cells for the 10
  weeks from the 18 January release: about 2.80 million arm sessions (web 1.11, app 1.69).
- **Allocation levers** (what makes the estimators disagree; the generator solves the per-cell system): sellers who
  offer pickup sit mostly in the four big cities, so the logger served D at 0.18 in the app's established cells and
  at 0.06 elsewhere, which puts D's replay sample in the high-base cells; render weights lean on long sessions, A's
  gain is largest in long sessions within each cell, and the long sessions are the new buyers', where B pins listings
  nobody was watching; the logger's E traffic leans to the new-buyer cells.
- **Watch list.** Mean watched listings at session start by tenure band 0.6, 4.2, 11.8, 17.5. A watched listing the
  session did not show is bought by its watcher within 6 days at 62.0 per cent, uniformly across categories, sizes,
  price bands and cells; shown or not, the watcher's purchases after day 6 run at the same background rate, so the
  difference is complete by day 6.
- **B's decomposition.** B's extra in-session orders 8.03 = 0.45 new-listing + 7.58 watched-listing; borrowed 4.73
  (7.58 x 0.62 = 4.70, plus 0.03 of organic watched exposure); kept 3.30. Borrowed share of B's gain 58.9 per cent,
  concentrated in the 180-day-plus cells.
- **Fresh-listing share** (tiles in positions 1 to 6 on listings under 48 hours old, per 100 tiles, each served
  ranking counted once as the commitment states): D 8.9; A 13.6, B 14.1, C 13.9, F 15.2, E 21.4. Floor 12. Counted
  over rendered tiles instead (every render row), D reads 12.4, because its fresh local listings surface in long
  sessions; every other policy moves by less than 0.4 and stays above 13.2.
- **Guardrail** (kept basis, change against the incumbent in the cell): A web 730+ at -2.7 per cent, C app under 30
  at -2.3 per cent, threshold -1.5; every other policy-cell at -0.9 or better; on every coarse cut (platform only,
  tenure only, pooled) no policy below -0.8. The same pass and fail on the in-session basis.

| Policy | Replay over render rows, unweighted | Render-weighted | Session-weighted, in-session | Kept (session-weighted, 7 to 21 days) |
|---|---|---|---|---|
| A two-tower personaliser | 8.50 | 10.38 | 6.58 | 6.47 |
| B velocity boost | 8.20 | 8.31 | 8.03 | 3.30 |
| C session-sequence model | 7.90 | 8.04 | 9.71 | 9.41 |
| D local-pickup boost | 10.40 | 5.58 | 5.12 | 5.03 |
| E sequence ranker, fresh-listing interleave | 6.60 | 6.43 | 5.79 | 5.70 |
| F seller-diversity re-ranker | 2.50 | 1.92 | 1.37 | 1.31 |

Extra orders per 1,000 carousel sessions against the incumbent. Kept is 5.698 for E and 3.302 for B unrounded.

### The ladder (five rungs; supersedes the draw's four-rung sketch)

| Rung | Construction | Leader | Margin | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Replay over the render rows (every render whose logged ranking is the policy's, unweighted) on in-session orders; floor counted over rendered tiles; guardrail on the platform split; the 2.0 bar | **D** | 1.224 over A | The reproduction clause with the archive's cell-allocated tests: replay misses six of the nine, each a test whose logger allocation varied by cell |
| 1 | Propensity weights, one per render row: the file's rows taken as the units | **A** | 1.249 over B | The twins T3 and T7, identical on every archive column and realised 2.24x apart: render weights put T7 at 5.12 against 2.5 (6 of 9 overall) |
| 2 | One self-normalised weight per session, the only estimator that reproduces 9 of 9; the floor recounted per served ranking | **C** | 1.209 over B | The charter's cell table: C loses 2.3 per cent in app, under 30 days |
| 3 | The eight cells, the floor and the bar: A out (web 730+), C out (app under 30), D out (floor 8.9), F out (bar, 1.37) | **B** | 1.387 over E | The orders record with the watch list: 7.58 of B's 8.03 extra in-session orders are watched listings, 62 per cent of which their watchers buy within 6 days unprompted, so B adds 3.30 over the test |
| 4, decisive | Split every policy's in-session gain into orders added and orders brought forward (route 2: watched-listing orders netted at the anyway rate measured on watched listings the session did not show; route 1: each buyer's orders, all channels, over the 7 to 21 days after the session, under the same session weights) and re-apply the three conditions | **E** | 1.726 over B | |

Gaps: rungs 0 to 2 are the rule gap (the estimator the archive pins, Pattern B, with the population gap of render
rows against sessions inside it, measured trap #2); rung 3 is the population gap (the eight cells, #14) with the
floor (#10, G11); rung 4 is the time gap (G9, #13 with #7).

**Why each rung is a place to stop.** Rung 0: it is the offline replay a ranking team runs first, and D leads it by
more than a fifth with every condition met. Rung 1: the logged propensities are now applied, the sampling skew replay
carried is gone, and A leads by a quarter. Rung 2: every figure is citable under the charter's clause, the estimator
is the one the archive certifies 9 of 9, and C leads by a fifth. Rung 3: every condition the charter states has been
applied at the grain it states with the only admissible estimator, and B is the largest lift that clears all three,
by 1.39x. A solver who does everything right up to rung 3 commits to **B**.

Every rung names a different candidate (D, A, C, B, E). The stump is carried by rung 4, and it clears the seven
survival properties as the draw set them out (1 written nowhere, 2 the archive blind for a computable reason, 3 no
arithmetic symptom, 4 not a row predicate, 5 enumeration is a construction, 6 no cutover date, 7 survives the
deletion).

**Worth on the graded quantity** (the call's lift): 10.40 (D) to 10.38 (A) to 9.71 (C) to 8.03 (B, -17 per cent) to
5.70 (E, -29 per cent). Every correction walks the committed figure down, the decisive rung moves it most, and the
answer's 5.70 is the smallest committed lift of the twelve grid cells below (L5, the extreme cell).

### Position table (asserted row by row)

| Rung | E's rank | Behind the leader by | Leader |
|---|---|---|---|
| 0 replay over render rows | 5 of 6 | 1.576x | D |
| 1 render weights | 4 of 6 | 1.614x | A |
| 2 session weights | 4 of 6 | 1.677x | C |
| 3 | 2 of the 2 that clear all three | 1.387x | B |
| 4 | 1 | leads by 1.726x | E |

E leads no intermediate rung, is second on one (rung 3, at 1.387x, above the 1.20 floor), and no rung margin is under
1.15 (the thinnest is C over B at rung 2, 1.209).

### Discriminator dominance

B's carried advantage into rung 4, in-session: 8.03 / 5.79 = **1.387x**. E's edge on the share of its gain it keeps:
0.984 (5.698 / 5.79) against B's 0.411 (3.302 / 8.03) = **2.393x**. Required: 1.2 x 1.387 = 1.664; held, and the
product 2.393 / 1.387 = 1.726 is the kept ratio.

### Correction grid (three independent toggles, 12 cells, each asserted by name)

The floor is counted at the estimator's grain (rendered tiles for the two render-row estimators, served rankings for
session weights).

| Estimator | Guardrail read | Outcome | Names | Its committed lift |
|---|---|---|---|---|
| replay over render rows | platform split | in-session | D | 10.40 |
| replay over render rows | platform split | kept | D | 10.31 |
| replay over render rows | eight cells | in-session | D | 10.40 |
| replay over render rows | eight cells | kept | D | 10.31 |
| render weights | platform split | in-session | A | 10.38 |
| render weights | platform split | kept | A | 10.24 |
| render weights | eight cells | in-session | B | 8.31 |
| render weights | eight cells | kept | B | 7.70 (E 6.36) |
| session weights | platform split | in-session | C | 9.71 |
| session weights | platform split | kept | C | 9.41 |
| session weights | eight cells | in-session | B | 8.03 |
| session weights | eight cells | kept | **E** | **5.70** |

Every non-decisive cell names D, A, B or C; E is reachable only through the decisive combination. The render-weights
kept cell names B by 1.211x because render weights lean on the new-buyer cells, where B borrows nothing; asserted at
1.15x or more. With the floor counted per served ranking, the replay cells name A (coarse, 8.50 over 8.20) or B
(eight cells), still wrong.

**Partial applications, swept and asserted.**

| Partial reading | Names | Figure |
|---|---|---|
| Flat haircut at B's own borrowed share (58.9 per cent) on every policy | B | 3.30 against E 2.38 |
| Flat haircut at the pooled watched-and-borrowed share of all carousel orders (7.6 per cent) | B | 7.42 |
| Follow-up window of 1 day / 2 days / 3 days | B | 7.79 / 6.94 / 6.19 |
| Follow-up window of 4 / 5 / 6 days | E | 5.70, with B at 4.62 / 3.98 / 3.49 (runner-up gap wrong) |
| Window of 7, 10, 14 or 21 days | E | 5.70, B 3.30 (C1) |
| The decomposition applied to B alone | E | 5.79 (a cracker one decimal off) |
| Route 2 netting with replay over render rows | D | the replay kept cell |

A solver who half-sees the borrowing and prices it flat lands on B, the stump, rather than drifting toward E (L3).

### Calibration corpus (the archive, pilot_log)

- **Form.** Nine archived home-carousel A/B tests, T1 to T9 (March 2023 to May 2026): each test's policy family and
  inputs, logging window, test window, traffic share, duration, cells in scope, logger version, the offline estimate
  published at the time (replay, the method then in use), and the realised lift with its interval, measured as the
  charter defines lift. Beside it, every pre-test logging window at session grain (test, session, ranker drawn,
  propensity, cell, renders, in-session orders), about 99,000 rows, so every estimator can be rerun from the bundle.
- **The clause.** The charter lets an offline estimator be cited against the lift condition only if, run on each
  archived test's logged sessions, it returns that test's realised lift within 0.25 extra orders per 1,000.
- **Back-test.** Session grain reproduces **9 of 9** (worst miss 0.21). Render weights **6 of 9** (T2 +0.84, T7
  +2.62, T9 +1.07). Replay **3 of 9** (six misses, 0.61 to 3.81). Every rival miss overstates, so the rivals also
  fail on the total: render weights by 11.4 per cent, replay by 27.2 per cent (L2, scored row by row and on the
  total). Swept family of six: replay, render weights, and four session-grain estimators (self-normalised,
  unnormalised, clipped at 0.05, cell-stratified difference). The four session-grain readings return identical
  figures by construction (arms are drawn by quota within each cell and propensity stratum, every propensity is at
  least 0.07), so the survivor is one class, never a choice among four.
- **Twin pair.** T3 and T7, both sequence-model family, identical on every archive column: inputs, traffic 10 per
  cent, 28 days, all cells, logger v3, published offline estimate +6.3. Realised +5.6 and +2.5 (2.24x apart).
  T7's logging window ran 16 to 29 November 2025, sessions averaging 6.8 renders against 1.9 for T3, with the gain
  concentrated in the long sessions. Session weights return 5.52 and 2.61; render weights 5.75 (a hit) and 5.12 (a
  miss); replay 6.3 and 6.3. Only session weights reproduce both, and no transferred rate can.
- **Resemblance points at the decoy.** The three largest realised lifts (T1 +7.9, T4 +7.1, T8 +6.8) were two-tower
  personalisers like A. E's family resembles T7, the smallest. The 2024 trending boost (T6, +4.4) resembles B and
  reproduces exactly, because it ranked on category velocity and never on a buyer's saves.
- **What it is blind to, and why (L1).** In every archived test the in-session estimate and the realised lift agree
  within 0.21 per 1,000, because no archived policy put listings from a buyer's own watch list ahead of other
  listings: buyer-listing saves enter carousel ranking for the first time in B's 2026 build (the register's inputs
  line), so in no archived test do the arms' watched-listing order rates differ by more than 0.1 per 1,000. Asserted
  twice: on that structural property, and by rerunning the nine tests with each archived session's hidden follow-up
  orders, where the kept construction also reproduces 9 of 9.
- **Every rule the golden composes has a case.** Session against render weighting: T2, T7, T9. Propensity weighting
  against replay: the six tests whose logger allocation varied by cell. The cell grain, the floor and the bar are
  filed rules, not estimator rules. The decomposition is the stated blind spot.

### Pins and counter-pins

- **Filed, level 2, the experimentation charter (home surfaces).** The three launch conditions as point rules; the
  lift definition, one sentence naming the observable: the change in orders placed by the arm's buyers during the
  test, per 1,000 carousel sessions, against the incumbent; the reproduction clause; the cell table; policies are
  scored on the most recent logged window; a slot test takes 10 per cent of logged-in carousel sessions on each
  platform for twelve weeks.
- **Filed, level 2, the fresh-listing commitment to private sellers.** At least 12 of every 100 tiles in carousel
  positions 1 to 6 go to listings under 48 hours old.
- **Filed, level 4, the logger dictionary.** The session is the draw unit; one propensity per session; every render
  repeats its session's ranking; in-session orders are carousel-tile orders placed before the session ends; the
  orders extract carries every order by enrolled buyers from 22 June to 11 October in every channel.
- **Empirical.** The estimator (session grain), the unique surviving class of the archive back-test.
- **Not pinned, and closed instead.** The follow-up window (C1 over 7 to 21 days); the anyway-rate comparison set
  (C1, the rate is uniform).
- **Counter-pins: none.** The archive's published-estimate column records what was published and is refuted by the
  clause it sits under. No voice endorses in-session orders as a policy's effect. The policy register carries
  inputs and no lift. No licensed wrong basis (the draw dropped the note's growth council).

### Fork grid: the 22-axis closure table (determinism-check A.5)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | the sessions the logger enrolled (logged-in buyers; internal accounts are never enrolled) | C1: nothing in the render log to exclude, asserted no internal account in it |
| 2 | Unit of account | one session for weights; one order is one listing bought | filed (dictionary, charter); C1: one row per order, no bundle rows |
| 3 | Attribution window | in-session for the naive read; 7 to 21 days after the session for the kept read | C1: every window from 7 to 21 days returns the same kept lift for all six (borrowing complete by day 6); 1 to 6 days violate "during the test" (C4, priced above) |
| 4 | As-of dating | tenure band at session start, stamped by the logger | C1: one stamp per session |
| 5 | Version basis | one release of every main-path file; each policy at its registered build | C1 |
| 6 | Divisor | per 1,000 carousel sessions of the enrolled population | filed; C1: self-normalised and unnormalised weights identical by quota draws |
| 7 | Weighting | one weight per session | C2: 9 of 9 against 6 and 3 of 9 |
| 8 | Window length | the whole 13 logged weeks | C1: each policy's first-half and second-half lifts within 0.10, asserted |
| 9 | Boundary inclusivity | "more than 1.5 per cent below", "at least 12", "at least 2.0" | C4: failing cells at -2.7 and -2.3, passing at -0.9 or better; floor 8.9 against 13.6; bar 1.37 against 3.30 |
| 10 | Rounding path | lifts unrounded, rounded once at the end | bin: every graded figure at least 0.03 inside its bin; rounding per cell before pooling moves none across, asserted |
| 11 | Tie-break | none needed | C4: E over B 1.726x; every grid cell's winner at least 1.15x clear |
| 12 | Maturity | every session followed for at least 21 days | C1: nothing censored inside any window up to 21 days |
| 13 | Order of operations | decomposition then conditions | C1: every policy passes or fails the same conditions on both bases; netting then weighting equals weighting then netting (linear) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | render rows are repeats of the session's ranking, not sessions | filed (dictionary); C2 (render weights refuted) |
| 16 | Identity normalisation | buyer and listing ids share one format across log, orders and watch list | C1: every key resolves, asserted |
| 17 | Netting against gross | borrowed orders netted in every arm, the incumbent's organic watched exposure included | C1: netting each arm then differencing equals differencing then netting |
| 18 | Dimensional units | orders per 1,000 sessions; guardrail in per cent of the incumbent's cell rate | filed (charter) |
| 19 | Code semantics | channel codes in the orders extract (carousel, search, favourites, alerts, other) | C1: route 1 counts every channel and route 2 every channel of a watched purchase, and both converge |
| 20 | Integerisation | none in the main call | C1 |
| 21 | Scope of a stated clause | the reproduction clause governs the lift estimator only | C1: the guardrail cells and the floor pass and fail identically under every estimator in the family, asserted |
| 22 | Forward window contents | the slot is scored on the latest logged window | filed (charter) |
| + | Variance method | none graded; every condition a point rule | filed; asserted that a 90 per cent bound above zero would also pass B, D and E and fail F |
| + | Anyway-rate comparison set | any set of watched listings the session did not show | C1: 62.0 per cent in every category, size, price band and cell |
| + | Route 1 against route 2 | either | C1: within 0.03 per 1,000 for every policy, asserted |
| + | Floor counting unit | each served ranking once, as the commitment states | filed; C4: over rendered tiles only D moves (8.9 to 12.4) and only at the render-row rungs, where it leads; every other policy above 13.2 either way |

### Deliverables and the criteria arithmetic

Shape 07, grid of cells, two files (both fixed at the draw):

1. **`carousel_slot_q1_2027.ipynb`**, executed, rerunnable by the requester. Opens on the call (E, 5.7 extra orders
   per 1,000 carousel sessions), then the runner-up and the gap, then the six-by-eight grid of each policy's change
   in buyer-protection fee income per 1,000 carousel sessions during the slot (euros, one decimal), then each
   policy's totals over the twelve weeks (extra orders and extra fee income, nearest hundred). The archive
   reproduction, the three conditions per policy and the guardrail cells sit in it as the working, not as asks.
2. **`carousel_slot_q1_2027_cells.png`**, the planning-deck heatmap: policies down, the eight cells across, colour
   on the fee figure, the two breaching cells hatched (A web 730+, C app under 30), E's row outlined, the call in
   the title.

**Arithmetic.** The call (1), its lift (1), the runner-up (1), the gap (1) = 4; the grid 6 x 8 = 48; the totals
6 x 2 = 12; the heatmap's parts beyond its layout (euro scale, hatching, outlined row, title) = 4; the files and the
heatmap's layout = 4. **72 criteria**, three distinct findings (the call, what each option is worth where, what the
quarter buys), a named-parts visual, a breakdown at an explicit grain (the charter's cells). The robustness check
(the archive) is in the notebook's working and is not asked for, because both top responses reach it (rung 2).

### Ask ledger (supplemental-stumping)

**Main call's declared row population.** Files: the render log (every column), the orders extract (order id, buyer,
listing, ordered at, channel; never the price column), the watch-list events, the archive register and archive
sessions, the charter, the fresh-listing commitment, the policy register, the logger dictionary. Window: sessions 22
June to 20 September 2026, orders to 11 October. Entities: the 150,400 enrolled sessions, their buyers and the
listings on their tiles and orders. **Zero device rows and zero hazard rows inside it**: every device below lives
in a file the main call never opens, and the one shared file (the orders extract) carries no device row; asserted
by file and by column.

| Ask | Figures, unit, rounding | Construction layer | Device layer: primary; hazards | Causal file path | Use (H18) |
|---|---|---|---|---|---|
| 1 Grid | 48: each policy's change in fee income per 1,000 carousel sessions in each cell during the slot, euros to one decimal | kept orders by cell (rung 4) | **P1 pickup orders paid in person** (D4); HZ1 tariff of record (D2); HZ2 price paid on accepted offers (D3) | render log, orders extract, watch list, logger dictionary, charter (cells), payments export, buyer-protection terms, tariff register, pricing committee minutes, offers export: 10 files, 14 columns | a component of the case: what each option is worth in each buyer cell, the measure the call does not turn on; finance books the chosen test's fee value from it |
| 2 Totals | 12: each policy's extra orders over the twelve weeks (nearest hundred) and extra fee income (nearest hundred euros) | kept lift by cell on the test arm's planned cell traffic | **P2 tenure restatement with invariant totals** (D2); HZ3 app arm starts at the first app release (forward window); on the fee half also P1, HZ1, HZ2 | ask 1's ten files plus the weekly sessions history, restatement R2, analytics release log, test capacity note, app release calendar: 15 files, 21 columns | a component of the case: what the quarter's slot buys, which the planning meeting puts beside the call |

**Primaries.**
- **P1, pickup orders paid in person (absent channel, silent on the natural path).** Buyer protection and its fee
  apply only to items paid through Vouwlijn; an order collected at a pickup and paid in person never reaches the
  payments export, while the orders extract lists it like any other order. 11 per cent of carousel orders overall,
  46 per cent of D's. Wrong path (every order priced by the formula) overstates every cell, D's row most. Over-
  cleaning half: pickup orders paid in the app carry the fee (they are in the payments export), so dropping every
  pickup order understates. Organs split: the terms (documentary) and the payments export's coverage (structural).
- **P2, the tenure restatement (a vintage whose totals are invariant).** The weekly sessions history (first release)
  bands January to June 2026 by each account's own creation date; restatement R2 (14 August 2026) re-bands those weeks
  after tenure was recomputed from the oldest merged account, moving 6.2 per cent of sessions from the two younger
  bands to the two older ones with every platform-week total unchanged. R2 ships as its own export and the release
  log says it replaces the first release for those weeks. Wrong path (first release) misallocates every cell's
  traffic; every policy's totals move because the lifts differ by cell (at least 100 orders on every policy's
  total, asserted).

**Hazards** (each on at least two asks' figures).

| Hazard | Family | Moves | Per-figure delta |
|---|---|---|---|
| HZ1, tariff of record: the register lists the 1 September 2026 revision (EUR 0.80 + 5 per cent) and a revision entered for 4 January 2027 (EUR 0.95 + 5 per cent); the October minutes defer the January revision to the Q2 review, and the terms' change clause makes a revision apply once approved; the register has no status column | D2 | ask 1 (48), ask 2 fee half (6) | +9.0 per cent on the January row; -4.6 per cent on the charged-fee mix of the logged window (EUR 0.70 until 31 August) |
| HZ2, price paid: the percentage part runs on the price paid; 38 per cent of carousel orders were bought on an accepted offer, 21 per cent below asking on average, and 22 per cent of accepted offers lapsed before checkout (asking paid); the orders extract carries the asking price, the offers export the accepted price, the payments export the total charged | D3 | ask 1 (48), ask 2 fee half (6) | +4.5 per cent on the asking price (mean asking EUR 19.00 against EUR 17.48 paid); taking every accepted offer, live or lapsed, undershoots by 1.2 points |
| HZ3, app arm start: an app arm begins with the first app release on or after the test's start (capacity note); the release calendar puts it on 18 January 2027, so app cells run 10 of the 12 weeks | forward window | ask 2 (12) | +12.1 per cent on the arm's sessions if all 12 weeks are counted on app (10 to 14 per cent on a policy's totals) |

Every graded figure sits under at least two independent devices: ask 1's cells under P1, HZ1 and HZ2; ask 2's orders
under P2 and HZ3, its fees under all five. No primary family repeats (D4, D2). The fee path's routes converge: the
price paid from the offers export and from the payments total less fee and shipping agree to the cent (C1).

**Referee (exactly one, byte-clean).** Finance's monthly buyer-protection fee income statement, July to September
2026, by platform: it ties to the payments export's charged fees and not to orders priced by the formula (which
overstate it by 17.5 per cent: P1's 12.4 compounded with HZ2's 4.5), so it arbitrates P1 and HZ2 for the logged window without giving any policy or cell
a level, and it says nothing about January.

**Per-ask stops** (asserted outside the golden bin on every figure unless a count is given).
- Ask 1: natural read (in-session orders, every order priced, asking price, January row); P1 alone handled; the
  over-cleaner (every pickup order dropped); the right fee set on the charged mix; everything right on in-session
  orders (moves B's eight cells and at least 24 of the other 40); golden.
- Ask 2: natural read (pooled in-session lift x 12 weeks x first release); cell by cell on the first release; all 12
  weeks on app; pooled lift on the planned total (violates the capacity note's cell-by-cell planning line); golden.
- Device magnitude floor: P1 or HZ1 moves every cell whose golden value is at least EUR 0.6 outside its bin;
  at most 4 of the 48 cells sit under that and are carried by the construction layer alone.

**Pair arithmetic (Part 0, planning weights 38 / 7 / 55).** Recommendation block 4 criteria; instruction 4; asks 64
at 0.86 points each (48 cells, 12 totals, 4 heatmap parts).
- Cracker (lands E): 38 + 7 + leakage. It keeps the 4 heatmap parts; a grid cell only when it handles P1, HZ1 and
  HZ2 together (planned at 0.15, so 7.2 cells) plus the at most 4 small cells (planned 2); a total only with P2 and
  HZ3 (planned 0.10, 1.2 figures). 14.4 criteria, 12.4 points, Lc = 0.225, score 57.4.
- Mirror (stops at B): r = 3 (all four call criteria need rung 4; 3 allows one generated criterion such as the
  guardrail exclusions). It keeps the hatching and the euro scale (2), at most 16 grid cells the construction
  layer leaves level, at 0.15 (2.4) plus 1 small cell, and no total (every policy's kept and in-session totals sit
  at least 160 orders apart). 5.4 criteria, 4.6 points, Ls = 0.084, score 14.6.
- **Pair 36.0**, under 40: 55 x (0.225 + 0.084) = 17.0, inside 28 - r = 25.
- Reachability: the share of ask weight reachable from the landed call is 4 of 64 (the heatmap parts), so a cracker
  banks 0.30 + 0.60 x 0.06 before any device.
- The exposure, stated: a cracker that handles all three fee devices keeps the grid and the pair reaches 52.6. The
  layer rests on P1 staying silent on the natural fee path and on HZ1 having two wrong sides; the leak sweep and the
  pair simulation (stage 3) are run against the pack as cut, and the over-determination sweep confirms no ask figure
  solves back for the anyway rate or the borrowed share.

### Assertion plan (46; generator first, then an independent verifier on the shipped bytes)

Main ladder
1. Rung 0, replay over render rows: D leads, margin at least 1.20 (1.224).
2. Rung 1, render weights: A leads, margin at least 1.20 (1.249).
3. Rung 2: C leads, margin at least 1.15 (1.209).
4. Rung 3: B leads, margin at least 1.20 (1.387).
5. Rung 4: E leads, margin at least 1.50 (1.726).
6. E is 5th of 6 at rung 0 and 4th of 6 at rungs 1 and 2.
7. E is 2nd at rung 3 only and leads no intermediate rung.
8. Dominance: E's kept-share edge (2.393) at least 1.2 x B's carried advantage (1.664).
9. All twelve correction-grid cells by name, each winner at least 1.15x clear of the next qualifier.
10. Partial readings by name: both flat haircuts and windows of 1 to 3 days name B; 4 to 6 days name E with B's
    figure outside its bin.
11. Route 1 and route 2 within 0.03 per 1,000 for all six policies.
12. Windows of 7, 10, 14 and 21 days return identical kept lifts for all six.
13. Every comparison set for the anyway rate returns 61.6 to 62.4 per cent and files the same kept figures.
14. Guardrail: A web 730+ at -2.7 and C app under 30 at -2.3; every other policy-cell at -0.9 or better; every coarse
    cut at -0.8 or better; identical pass and fail on the kept and in-session bases.
15. Guardrail and floor pass and fail identically under all six estimators in the swept family.
16. Floor: per served ranking D 8.9 and every other policy at least 13.6; over rendered tiles D 12.4 and every
    other policy at least 13.2.
17. Bar: F at least 0.6 under 2.0 on every session-grain estimator; B's kept lift at least 1.3 over 2.0.
18. A 90 per cent bound above zero would pass B, D and E and fail F (no condition depends on the variance method).

Archive
19. Session grain reproduces 9 of 9 within 0.25 (worst 0.21).
20. Render weights 6 of 9, replay 3 of 9, every miss overstating; totals +11.4 and +27.2 per cent.
21. The four session-grain readings agree to 0.001 on all nine tests and on the logged window (quota draws,
    propensities at least 0.07).
22. T3 and T7 identical on every archive column, realised 2.24x apart; session weights reproduce both, render weights
    and replay miss T7.
23. Blindness: no archived specification lists buyer saves; archived arms' watched-listing order rates within 0.1 per
    1,000 of control.
24. Clean-data test: with each archived session's hidden follow-up orders added, the kept construction reproduces 9
    of 9, answer(repaired) = E, naive(repaired) = B.
25. Resemblance: the three largest realised lifts are two-tower tests; the sequence family's nearest test is T7.

Bins and rounding
26. Every graded figure at least 0.03 inside a one-decimal bin and at least 20 inside a hundred bin (E 5.698, B
    3.302, gap 2.396).
27. Rounding per cell before pooling moves no graded figure across a bin.
28. Each policy's first-half and second-half lifts within 0.10.

Asks
29. Ask 1: all 48 golden cells; every stop; P1, HZ1 and HZ2 each move at least 44 cells out of the bin; at most 4
    cells under EUR 0.6.
30. Ask 1: the in-session basis moves B's eight cells and at least 24 of the other 40 out of the bin.
31. Ask 1: the price paid from the offers export and from the payments total agree to the cent on every order.
32. Ask 2: all 12 golden figures; the first-release, all-weeks-on-app and pooled-lift stops each out of the bin on
    every figure.
33. Ask 2: R2 keeps every platform-week total equal to the first release and moves 6.2 per cent of sessions.
34. Ask 2: every policy's kept and in-session totals at least 160 orders apart.
35. Every subset of mishandled devices per ask lands outside the bin (ask 1: 7 subsets; ask 2: 31).
36. Over-cleaners land on their stops: every pickup order dropped, every accepted offer taken, the pre-September
    tariff.
37. Separation: zero device and hazard rows in the main call's declared files and columns.
38. Necessity matrix: each device moves exactly the asks in its ledger row and none of the call's four figures.
39. Over-determination: the asks are unchanged along the line of (watched share, anyway rate) pairs that hold each
    policy's kept lift by cell fixed, so neither constant can be solved back from them.
40. Pair simulation, cracker and mirror sheets with the hygiene battery applied: at most 40.
41. The hygiene battery on each wrong path comes back clean (no duplicate key, no unmatched join on that path, every
    count ties).

Pack
42. Input gates: at least 10 files, at least 3 formats, the render log at least 25,000 rows (405,000), at least two
    distractors named in metadata.json.
43. No shipped table carries a per-policy lift, guardrail or ranking on any basis.
44. Each load-bearing fact in exactly one file: the lift definition, the reproduction clause, the cell table, the
    floor, the tariff deferral, the app-release gating line, the R2 replacement line.
45. Two consecutive builds byte-identical.
46. The notebook's printed figures equal the generator's, and the heatmap's cells equal the grid.

### Pack plan (names provisional, in the organisation's own idiom; dataset-generation builds against it)

| # | File | Role | Path |
|---|---|---|---|
| 1 | `home_carousel_render_log_2026-06-22_2026-09-20.csv` | spine, 405,000 renders | main |
| 2 | `orders_enrolled_buyers_2026-06-22_2026-10-11.parquet` | operating extract, every channel | main (price column ask only) |
| 3 | `watchlist_events_2026-05-01_2026-10-11.csv` | operating extract | main |
| 4 | `carousel_experiment_archive.xlsx` | calibration: tests sheet and logged-sessions sheet (99,000 rows) | main |
| 5 | `experimentation_charter_home_surfaces.pdf` | governing: conditions, lift definition, clause, cell table | main |
| 6 | `fresh_listing_commitment_2026.docx` | governing: the floor | main |
| 7 | `ranking_policy_register.json` | context artifact: specifications and inputs, no lift | main |
| 8 | `carousel_logger_data_dictionary.md` | dictionary | main |
| 9 | `payments_buyer_protection_2026-06-22_2026-10-11.csv` | ask 1 and 2 | ask |
| 10 | `offers_2026-06-15_2026-10-11.csv` | ask 1 and 2 | ask |
| 11 | `buyer_protection_terms_2026-09.pdf` | organ, P1 and HZ2 | ask |
| 12 | `kopersbescherming_tarieven.csv` | tariff register, HZ1 | ask |
| 13 | `pricing_committee_minutes_2026-10-06.docx` | organ, HZ1 | ask |
| 14 | `home_carousel_sessions_weekly_2025W01_2026W39.csv` | traffic, first release | ask |
| 15 | `home_carousel_sessions_weekly_R2_2026W01_2026W26.csv` | restatement | ask |
| 16 | `analytics_release_log.md` | organ, P2 | ask |
| 17 | `slot_capacity_and_release_gating.md` | organ, HZ3; cell-by-cell planning line; same weeks last year | ask |
| 18 | `app_release_calendar_2026-2027.ics` | HZ3 dates | ask |
| 19 | `finance_buyer_protection_fee_income_2026Q3.xlsx` | the referee | ask |
| 20 | `planning_thread_carousel_slot.txt` | social layer: Fabian Stoffel (the pinned tiles convert better than any tiles the carousel has had, which the log bears out), Tygo Knoers (the archive has never missed with session weights), Kayleigh Zeemans (the interleave costs a tile and she would not put it against the velocity boost) | neither |
| 21 | `search_ranking_tests_2026H1.xlsx` | distractor: search-page tests, same metric family, another surface | none |
| 22 | `seller_survey_fresh_listings_2026Q2.csv` | distractor: sellers on exposure, beside the floor | none |
| 23 | `provenance.md` | provenance record | none |

Nine formats (CSV, Parquet, XLSX, PDF, DOCX, JSON, MD, ICS, TXT). Every voice holds a belief and none quotes a lift;
the owner of the answer argues against it. No sentence anywhere says an order can be brought forward.

### Realism debts (stated)

- **Point-estimate guardrail on per-cell differences of 2 to 3 per cent.** Real per-cell sampling error on a
  405,000-render log is several times that. Forced because a cell guardrail has to be determinate on the spine the
  gate allows; mitigated by the charter stating it as an offline screen ahead of the online test, and by no graded
  figure being a bound.
- **Quota-balanced arm draws** (self-normalised and unnormalised weights identical). Tidier than a live logger;
  forced by C1 on axis 6; mitigated by the dictionary's line that arms are assigned in fixed proportions within each
  cell's daily block.
- **A uniform anyway rate and borrowing complete by day 6.** Real rates vary and tail off; forced by C1 on route
  2's comparison set and on the window; mitigated by sampling spread of 61.6 to 62.4 across segments and a
  background purchase rate after day 6 that is the same shown or not.
- **One enrolled session per buyer.** Forced so route 1's windows never overlap; stated in the dictionary.
- **B's 59 per cent borrowed share and replay sitting 5.3 above the session estimate for D.** Forced by dominance
  (an edge of at least 1.664) and by a 1.2x leader at rung 0; mitigated by B's inputs line (buyer-listing saves) and
  by the logger's documented cell allocations (D served where pickup sellers are).
- **23 files**, above the 13-file median, forced by the eight-file span on both asks with split organs; every file
  has a causal role or is a named distractor.
- **Gate G residual.** A judge who takes the render log's in-session column as the instrument and a window count as
  its repair would call the move a lens swap. Mitigated by the decomposition being the graded construction (route 2
  needs the watch list and the anyway rate, route 1 a window that has to be found), by no artifact ranking the
  policies, and by the clean-data repair holding. It is the first thing to read in a judge report.

### Stopping rule (written before any round)

- **At ceiling:** two responses, in-house or portal, that file E at 5.7 by different routes (route 1 and route 2),
  or a landed call in two consecutive rounds. The main ladder is then measured out and the move is re-rooting the
  ask, not hardening the mechanism.
- **One more repair licensed:** a response that misses E but scores near 40 on the asks (the fee or traffic devices
  leaking: a Part 4/5 repair), or two responses splitting on a figure (determinism first). A response that lands E
  with the decomposition applied to B alone is a cracker, not a defect.
- Three hardening loops on this architecture, then a re-root at stage 1.

### Portal log

None yet.

### Determinism check

Invoked at the ladder (section A): litmus, mechanism and flags written; 22 axes and three additions closed; no
graded figure on a variance method; every pass and fail a point rule with a stated margin. Open for stage 3 (the
generator, section B): solve the per-cell system so the twelve grid cells hold by name; route 1 against route 2;
the fee devices' reach on the small cells; the bin distances.

### The prompt (stage 2)

`prompt.md`, 224 words. Deliverable-first opening (unused in the batch window), role in the last paragraph, the call
as a question at the seam carrying its unit and rounding, one block convention for the rest (rates to one decimal,
totals to the nearest hundred). No voice, no input file, no basis, window or method clause; "while the slot runs"
and "over the twelve weeks" carry the forcing event's period only. voice-check: 18.7 words a sentence, context 29
per cent, longest paragraph 81 words, one rounding tag, no carrier flagged, no shared six-word run; hierarchy read
passes (the call closes the context, the notebook opens on that answer, each later paragraph ties back to it).

## Build record

The stage 3 build's record; `## Harden loop 1: build record` supersedes every figure in it.

Stage 3, 2026-10-09. `python3 task122/generator/build.py` (seeded throughout) writes `target/` and `metadata.json`,
asserts every check in `checks.py` on the files as written, normalises container metadata and mtimes, and fails
loudly at the first assertion that does not hold. `task122/generator/verify_pack.py` is the independent verifier: it
reads only the bytes under `target/` (and `metadata.json` for the distractor list), imports nothing from the
generator, and reads every constant it needs (lift bar, guardrail, reproduction clause, cell bands, floor, slot
share and dates, app gating, tariff in force, R2 replacement) from the shipped documents.

### Gates

- **Generator green:** 240 assertions, all pass, on the task-folder build.
- **Independent verifier green:** 70 of 70 checks pass on the task folder, including agreement with the
  build record on the call (to 0.0006), all 48 fee cells (to 0.0006), all 12 slot totals (to 0.06) and every rung's leader.
- **Byte-identical:** two consecutive builds into separate scratch roots and every build into the task folder (the last
  on the final generator) produce the same SHA-256 for all 24 files (23 under `target/` plus `metadata.json`); every
  `target/` mtime is 2026-10-14 17:30.
- **Input gates:** 23 files; 9 formats (csv, docx, ics, json, md, parquet, pdf, txt, xlsx); the render log carries
  404,100 rows; two distractors named in `metadata.json` only (search_ranking_tests_2026H1.xlsx, seller_survey_fresh_listings_2026Q2.csv),
  and the word appears nowhere under `target/` (asserted).
- **Containers:** `scrub_producer_metadata.py` repaired the two PDFs (writer's name, invariant 2000-01-01 date) to
  Vouwlijn and 2026-10-14; the audit then reads the whole folder clean (asserted, H1). The OOXML containers are rewritten
  with fixed entry dates and order.
- **metadata.json:** task, title (no policy named), domain, subdomain, objective, shape, as-of 2026-10-28, the two
  deliverables, the distractor list, the input gates, and source, date and licence for every file. No answer, no rung,
  no device name.

### The answer

E, HC-37 (Sequence ranker with fresh-listing interleave): kept lift 5.697 extra orders per 1,000 carousel
sessions, filed 5.7. Runner-up B, HC-33 (Velocity boost): 3.303, filed 3.3. Gap 2.394, filed 2.4;
E over B 1.725x. Bin clearances: E 0.047 (from 5.65), B 0.053 (from 3.25), gap 0.044 (from 2.35).

### The ladder as built (asserted leader and margin per rung)

| Rung | Estimator | Guardrail read | Basis | A | B | C | D | E | F | Leader | Next | Margin | E's place of six |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | replay_rows | platform | in-session | 6.956 | 7.676 | 7.200 | 9.661 | 3.323 | 0.318 | D | B | 1.259 | 5 |
| 1 | render_weights | platform | in-session | 11.018 | 9.087 | 7.975 | 5.552 | 5.780 | 1.910 | A | B | 1.212 | 4 |
| 2 | session_ipw | platform | in-session | 6.563 | 7.957 | 9.784 | 5.074 | 5.697 | 1.389 | C | B | 1.230 | 4 |
| 3 | session_ipw | eight | in-session | 6.563 | 7.957 | 9.784 | 5.074 | 5.697 | 1.389 | B | E | 1.397 | 4 |
| 4 | session_ipw | eight | kept | 6.563 | 3.303 | 9.784 | 5.074 | 5.697 | 1.389 | E | B | 1.725 | 3 |

Qualifiers: rungs 0 and 1 A, B, C, D, E (F under the bar); rung 2 A, B, C, E (D fails the floor per served ranking);
rungs 3 and 4 B and E (A fails web 730+, C fails app under 30). At rung 4 E is third of six by value and first of the
two qualifiers. Position: E 5th, 4th, 4th, then second behind B at rung 3 only, then the leader. Dominance: B's carried
advantage at rung 3 1.397, E's kept-share edge 2.409, product 1.725 (at least 1.2 asserted).

### Correction grid (12 cells, each asserted by name at 1.15x or better)

| Estimator | Guardrail | Basis | Leader | Value | Next qualifier | Margin |
|---|---|---|---|---|---|---|
| replay_rows | platform | in | D | 9.661 | B | 1.259 |
| replay_rows | platform | kept | D | 77.933 | none | only qualifier |
| replay_rows | eight | in | D | 9.661 | B | 1.259 |
| replay_rows | eight | kept | D | 77.933 | none | only qualifier |
| render_weights | platform | in | A | 11.018 | B | 1.212 |
| render_weights | platform | kept | A | 11.018 | C | 1.382 |
| render_weights | eight | in | B | 9.087 | E | 1.572 |
| render_weights | eight | kept | B | 7.355 | E | 1.272 |
| session_ipw | platform | in | C | 9.784 | B | 1.230 |
| session_ipw | platform | kept | C | 9.784 | A | 1.491 |
| session_ipw | eight | in | B | 7.957 | E | 1.397 |
| session_ipw | eight | kept | E | 5.697 | B | 1.725 |

Replay over render rows on the kept basis returns 77.9 for D because replay carries no propensity weights and three
weeks of every buyer's other orders differ by cell; it is the unweighted estimator failing visibly, not a figure any
filed rule licenses.

### Partial readings and the windows

- Flat haircut of every policy at B's borrowed share (58.5 per cent): B 3.303 against E
  2.365, names B. Flat haircut at the pooled share of all in-session orders (0.75 per cent): names B.
- Follow-up windows of 1, 2 and 3 days name B (B 7.647, 6.960, 6.206 against E 5.697); 4 and 5 days
  name E with B at 5.031 and 4.023, outside B's bin; every window from 6 to 21 days returns E 5.697 and
  B 3.303 for all six policies, and calendar-day windows of 7, 10, 14 and 21 days match to 1e-9.

### Route 2, the anyway rate and its comparison sets

- Watched listings the session did not show are bought by their watcher within the window at exactly 62.5 per cent
  (five in eight) in every cell, every arm, every cell by arm, both platforms and every tenure band; route 2 equals
  route 1 for every policy (within 0.005) and every cell (1e-6).
- Other segments (renders, watch-list size, weekday, ISO week, half) run 61.79 to 63.26 per cent. Netting each
  segmentation stratum by stratum files E 5.697 and B 3.3011 to 3.3028; each natural sub-population's rate
  applied to every session (incumbent arm, velocity arm, each platform, each half, one-render and up-to-two-render
  sessions) runs 62.45 to 62.55 per cent and files B 3.2990 to 3.3065; E never moves.
- Thinnest boundary in the pack, recorded rather than asserted: the most extreme single segment applied to every
  session moves B to 3.2462 (four-render sessions, 63.26 per cent), across the 3.25 edge, or 3.3556 (61.79
  per cent). No reading applies one segment's rate to everyone; every stratified and sub-population reading files 3.3.

### Conditions

- Guardrail breaches exactly A web 730+ (-2.736 per cent) and C app under 30 (-2.392); every other
  policy-cell at +1.20 per cent or better; the same pass and fail on in-session and kept bases, session and render
  weighting, and every coarse cut (platform, tenure, pooled) at -0.8 or better, asserted.
- Floor, per served ranking: D 8.84 (fails), incumbent 13.00, every other policy 13.60 to
  21.40. Over rendered tiles D reads 15.59 (17.01 render-weighted) and passes, which is why the
  render-row rungs keep D.
- Bar: F 1.389 on every session-grain estimator (fails); B's kept 3.303 clears it by 1.30.
- Halves: each policy's first-half and second-half lifts agree within 0.085 (in-session) and 0.050 (kept).

### The archive (calibration corpus)

| Test | Realised | Session weights | Render weights | Replay rows | Published |
|---|---|---|---|---|---|
| T1 | 7.9 | 7.727 | 7.993 | 7.993 | 8.0 |
| T2 | 4.1 | 4.185 | 4.993 | 5.253 | 5.3 |
| T3 | 5.6 | 5.522 | 5.779 | 6.333 | 6.3 |
| T4 | 7.1 | 7.010 | 7.179 | 7.776 | 7.8 |
| T5 | 3.6 | 3.643 | 3.667 | 3.667 | 3.7 |
| T6 | 4.4 | 4.394 | 4.441 | 4.441 | 4.4 |
| T7 | 2.5 | 2.621 | 5.153 | 6.294 | 6.3 |
| T8 | 6.8 | 6.713 | 6.998 | 8.149 | 8.1 |
| T9 | 3.2 | 3.352 | 4.282 | 5.141 | 5.1 |

Session weights reproduce 9 of 9 within the charter's 0.25 (worst 0.173, T1), and the three other session-grain
readings agree to 0.001. Render weights 6 of 9 (T2, T7, T9 miss), replay 3 of 9 (T1, T5, T6 hit); every miss overstates;
summed over the nine tests render weights overstate by 11.7 per cent and replay by 21.8 per cent. The published
column is replay to one decimal on all nine. Twins T3 and T7 are identical on every archive column (published 6.3 both)
and realised 5.6 and 2.5 (2.24x); session weights reproduce both, render weights and replay miss T7. Lookup transfer by
policy family names A (7.27, the two-tower personaliser), a decoy. Blindness and the clean-data test are asserted
per test on the hidden layers: no archived arm moves watched-listing orders by more than 0.1 per 1,000, and with each
archived session's follow-up orders added the kept construction reproduces all nine.

### Ask 1: change in buyer-protection fee income per 1,000 carousel sessions (EUR, filed to one decimal)

| Cell | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| app <30 | 11.004 | 5.593 | 1.392 | -8.687 | 8.896 | 5.994 |
| app 30-179 | 10.810 | 11.605 | 16.500 | -14.906 | 10.995 | 1.893 |
| app 180-729 | 9.792 | 4.501 | 17.005 | -14.388 | 9.798 | 1.813 |
| app 730+ | 8.510 | 3.709 | 17.914 | -17.688 | 6.097 | 1.112 |
| web <30 | 12.709 | 1.902 | 8.989 | -9.810 | 7.615 | 1.489 |
| web 30-179 | 8.297 | 6.814 | 15.698 | -13.100 | 12.085 | -2.799 |
| web 180-729 | 11.900 | 0.991 | 11.294 | -15.614 | 9.108 | 0.701 |
| web 730+ | -2.215 | 2.410 | 16.691 | -19.209 | 5.409 | 1.686 |

Every cell sits at least 0.035 inside its bin. Every one of the seven combinations of the three fee devices (pickups
paid in person priced, the asking price for the price paid, the deferred January tariff row) and the natural read (all
three, in-session orders only) moves all 48 cells out of their bins, the nearest by 0.051; two cells sit under
EUR 1.00 (B|web 180-729, F|web 180-729) and move under every reading too. Over-cleaners move
43 (fee as charged), 45 (every pickup dropped), 44 (any accepted offer as the price) and
48 (the pre-September tariff) cells. The in-session basis moves the four cells where B's figures carry
borrowed orders (app and web, 180-729 and 730+); in the four younger cells B buys no watched listing in the session
and its two bases agree. The price paid read from the offers export and from the payments ledger agree on every paid
order.

### Ask 2: the twelve-week slot totals (filed to the nearest hundred)

| Policy | Extra orders | Filed | Extra fee income (EUR) | Filed | First release | All 12 weeks on app | Pooled lift | Natural read |
|---|---|---|---|---|---|---|---|---|
| A | 17,107.6 | 17,100 | 22,592.5 | 22,600 | 17,380.4 | 19,718.2 | 17,321.7 | 19,530.8 |
| B | 8,910.8 | 8,900 | 12,709.7 | 12,700 | 9,411.3 | 10,113.1 | 8,716.7 | 23,678.6 |
| C | 25,326.4 | 25,300 | 38,272.8 | 38,300 | 24,789.3 | 28,250.3 | 25,823.4 | 29,116.8 |
| D | 13,227.7 | 13,200 | -39,578.3 | -39,600 | 13,426.2 | 15,287.7 | 13,392.3 | 15,100.2 |
| E | 15,286.4 | 15,300 | 22,778.2 | 22,800 | 15,622.0 | 17,296.4 | 15,034.6 | 16,952.0 |
| F | 3,807.3 | 3,800 | 3,726.4 | 3,700 | 4,010.7 | 4,350.9 | 3,664.6 | 4,132.0 |

Planned arm sessions by cell (10 per cent of the R2-current 2026 weeks; web W01 to W12, app W03 to W12 from the
18 January 2027 release): 216,093, 370,206, 475,592, 514,023, 155,100, 256,384, 320,701, 331,120 (2,639,219 in all). Every golden total sits
22.35 or more from its bin's edges; every wrong reading of every total (the first release, all twelve
weeks on the app, both, the pooled lift, the natural read, and on the fee every one of the 31 subsets of the five
devices) lands outside its hundred, the nearest by 5.67 (F's fee total on the first release alone; the nearest order
stop is F's pooled-lift total, 85.4 outside). R2 keeps every platform-week total and moves
6.19 per cent of sessions; the in-session basis moves only B's total (20,286.3).

### Referee, pair and separation

- The Q3 finance statement ties to the payments ledger by month and platform to the cent; pricing every Q3 order by
  the formula on its asking price overstates it by 20.7 per cent.
- Pair simulation (planning weights 38 / 7 / 55, hygiene battery applied): cracker 48.4, mirror 11.7, pair
  30.1 (at most 40 asserted); a cracker that handles every fee device would bring the pair to
  50.7, the stated exposure.
- Zero device rows in the main call's declared population; scrambling the device columns of the orders extract moves
  neither E nor B (1e-12). Hygiene battery clean: unique keys, every payment and every offer has its order, no
  duplicate purchase.
- Each load-bearing fact stands in exactly one file: lift definition (experimentation_charter_home_surfaces.pdf); reproduction clause (experimentation_charter_home_surfaces.pdf); cell table (experimentation_charter_home_surfaces.pdf); floor (fresh_listing_commitment_2026.docx); slot share (experimentation_charter_home_surfaces.pdf); tariff deferral (pricing_committee_minutes_2026-10-06.docx); app gating (slot_capacity_and_release_gating.md); r2 replaces (analytics_release_log.md); cell by cell planning (slot_capacity_and_release_gating.md); fee basis (buyer_protection_terms_2026-09.pdf); change clause (buyer_protection_terms_2026-09.pdf).

### Placement, for the record

- Fee cells: whole-euro moves on the cell's own in-session orders, plain-order prices -10 to +2, accepted-offer
  asking prices -13 to +7, in-person prices -1 to +5 per cell.
- Slot traffic: per-cell factors 0.9850 to 1.0091 on 2026-W01 to W12, inside the 1.5 per cent box.
- Halves: per-group option search; the largest gap between a policy's half difference and the incumbent's is
  0.086 per 1,000.

### Assertion plan against what was built

The design planned 46 assertions; the build carries 240 in `checks.py` and 70 in `verify_pack.py`. Where the build
departs from the plan:
- #13 (every comparison set files the same figures) is replaced by stratified netting on ten segmentations and eight
  natural sub-population rates, all filing E 5.7 and B 3.3; see Tried and rejected.
- #18 (a 90 per cent bound check) is dropped; see Tried and rejected.
- #29 is stronger than planned: every device combination moves all 48 cells, not 44, and no cell is carried by the
  construction layer alone.
- #30 and #34 narrow to B: since only the velocity boost shows watched listings, the other five policies' kept and
  in-session figures are equal, and the in-session basis moves B's four borrowing cells and B's total only
  (asserted).
- #38 is asserted for the call (no device column moves E or B); each device's reach on the asks is covered by the
  subset assertions (7 on ask 1 plus the natural read, 31 fee subsets and 5 order stops on ask 2).
- #39 (over-determination) is not built as a sweep: the ask figures are computed from the window orders and carry
  neither the anyway rate nor the watched share, and no shipped file states either constant.
- #46 belongs to the golden stage.
- Figures that moved from the design's targets: rung margins 1.259, 1.212, 1.230, 1.397, 1.725 (design 1.224, 1.249,
  1.209, 1.387, 1.726); E 5.697 and B 3.303 (design 5.698 and 3.302); guardrail breaches -2.74 and -2.39 (design
  -2.7 and -2.3); D's floor 8.84 per served ranking and 15.59 over rendered tiles (design 8.9 and 12.4); archive
  overstatement +11.7 and +21.8 per cent (design +11.4 and +27.2); borrowing complete by day 6, so the E-named partial
  windows are 4 and 5 days (design 4 to 6); F's lift 1.389 against the bar (design 1.37); the anyway rate 62.5 per
  cent (design 62.0). The design's comparison sets by category and price band cannot be formed, because a watched
  listing nobody bought carries no category or price in the pack; the sets a reader can form are the session's own
  cuts, listed above.

### Realism debts added at build

- The two halves of the logged window agree to 0.09 per 1,000 for every policy, closer than a randomised window would;
  forced by the stability axis (#8), stated.
- The anyway rate is exactly five in eight in every cell, arm and charter cut; segments outside the charter's cuts
  scatter 61.8 to 63.3 per cent.
- Prices of a few in-session orders per cell are moved by whole euros to place the fee cells; every move keeps asking,
  paid, offer and payment records consistent.
- Q1 tenure mix: a January new-buyer surge in the weekly table (both years), which is what separates the pooled and
  cell-by-cell slot totals.

### Files

| File | Format | Rows | Bytes |
|---|---|---|---|
| analytics_release_log.md | md |  | 1,503 |
| app_release_calendar_2026-2027.ics | ics |  | 11,403 |
| buyer_protection_terms_2026-09.pdf | pdf |  | 2,731 |
| carousel_logger_field_reference.md | md |  | 4,065 |
| carousel_experiment_archive.xlsx | xlsx | 99,200 | 3,617,682 |
| experimentation_charter_home_surfaces.pdf | pdf |  | 3,856 |
| extract_register_slot_review.md | md |  | 3,653 |
| finance_buyer_protection_fee_income_2026Q3.xlsx | xlsx |  | 6,018 |
| fresh_listing_commitment_2026.docx | docx |  | 37,365 |
| home_carousel_render_log_2026-06-22_2026-09-20.csv | csv | 404,100 | 26,227,263 |
| home_carousel_served_rankings_2026-06-22_2026-09-20.parquet | parquet | 150,400 | 10,212,573 |
| home_carousel_sessions_weekly_2025W01_2026W39.csv | csv | 728 | 27,165 |
| home_carousel_sessions_weekly_R2_2026W01_2026W26.csv | csv | 208 | 7,790 |
| kopersbescherming_tarieven.csv | csv | 3 | 318 |
| offers_accepted_2026-05-25_2026-10-11.csv | csv | 96,904 | 9,074,235 |
| orders_enrolled_buyers_2026-06-01_2026-10-11.parquet | parquet | 366,052 | 6,751,197 |
| payments_buyer_protection_2026-06-01_2026-10-11.parquet | parquet | 325,156 | 5,503,229 |
| planning_thread_carousel_slot.txt | txt |  | 2,254 |
| pricing_committee_minutes_2026-10-06.docx | docx |  | 37,351 |
| ranking_policy_register.json | json |  | 3,488 |
| search_ranking_tests_2026H1.xlsx | xlsx |  | 6,541 |
| seller_survey_fresh_listings_2026Q2.csv | csv | 1,612 | 86,853 |
| slot_capacity_and_release_gating.md | md |  | 1,249 |


## Stage 3: write-up and ship checks (2026-10-09)

Skills run in order: submission-writeup, golden-realism, reduce-house-fixes, leak-check, fingerprint (dataviz loaded
before the chart code).

- **Golden.** `generator/golden.py` reads only `target/`. It defines the notebook's code cells once, runs them
  in-process so the opening sentence carries the computed call, writes `carousel_slot_q1_2027.ipynb`, executes it
  top to bottom with a Jupyter kernel in `golden/` (the last cell saves `carousel_slot_q1_2027_cells.png`), refuses
  any error or stderr output, checks the executed outputs show the same call line, fee grid and totals table, and
  asserts every graded figure against this note's build record (call 5.697, runner-up 3.303, gap 2.394; all 48
  fee cells to 0.001 and the same tenth; all 12 totals to 0.06; the two breaches; archive 9, 6 and 3 of 9; the two
  qualifiers). Two runs, one into the scratchpad, are byte-identical on both files.
- **The notebook's path.** Per-session weights certified on the archive, then each buyer's orders over the 21
  days after the session (a 1 to 21 day sweep shows every lift flat from day 6), the watched-listing netting as a
  cross-check (anyway rate 62.5 per cent, route 2 within 0.01 of route 1 for all six), the three conditions as point
  rules, the fee grid at KB-2026-02 on the price paid with no fee on items paid in person, and the totals on the
  R2-current 2026-W01 to W12 cells with the app arm from W03.
- **submission.md**: five blocks; block 4 carries the call, runner-up and gap, all 48 cells (one point per policy,
  every cell named) and all 12 totals, plus the heatmap's four parts. Every block 4 figure was diffed against
  `verify_pack.py --out` (48 of 48 cells, 12 of 12 totals).
- **golden-realism.** The chart: deliberate diverging red to blue palette with a grey zero (dataviz palette, poles
  validated), cells labelled to one decimal, app and web column groups, hatching with a backed label so the value
  stays legible, the chosen row outlined above the group gap, a status column, a finding title, a source line.
  First render clipped the title and HC-37's label and ran two tenure headers together; fixed in the chart cell and
  re-rendered. The notebook opens on the call in Saar Dries's voice, carries the argument in short markdown cells,
  keeps constants at the top with their charter and commitment sections, and leaves control assertions in (session
  tie to the orders extract, archive 9 of 9, windows flat from day 7, price paid on two routes).
- **reduce-house-fixes.** H1: `scrub_producer_metadata.py` audit of `golden/` clean; the PNG carries only its dpi
  chunk. H4: `golden/` holds exactly the two files the prompt names (asserted in golden.py). H6: the fee rule the
  notebook states (fixed amount plus a percentage of the price paid, none on items paid in person) is back-tested in
  the notebook on every payment in the ledger, each at the register row in force on its capture date (325,156 of
  325,156), and every order without a payment is a pickup (asserted). H8: the three renamed files are updated in
  this note, the submission and the verifier, and nothing cites an old name. H11: one `submission.md` and one
  `prompt.md` under the task tree. Figures re-run after the realism pass: unchanged.
- **Leak fix.** `leak.py` returned LEAK on three file names (`test_` twice, `_v4`). Renamed in `generator/docs.py`:
  `carousel_experiment_archive.xlsx`, `slot_capacity_and_release_gating.md`,
  `experimentation_charter_home_surfaces.pdf`. The rebuild (240 assertions) left every other file byte-identical
  and changed only the three names inside `extract_register_slot_review.md`; `verify_pack.py` 62 of 62 after it.
  Re-run verdict REVIEW.
- **Surface:** 0 promoted pairs (nearest task109 at 0.092). **Heart:** WARN, no BLOCK (repeat.gate_g against
  task119 and task121, repeat.decision against task121, both answered under Guard); nearest heart text 0.06
  (task118's stump). Card updated (answer, answer_source, spine rows 404,100, deliverables, opening move) and
  `guard.py validate` clean.

## Leak review

Answers to `leak.py --asof 2026-10-28` as re-run at stage 3 after harden loop 2 (REVIEW, no LEAK, 16 REVIEW lines;
stump terms from the current stump sentence).

- Charter, golden figures 179, 180, 729, 730: the cell table's tenure band edges, which the golden uses as cell labels, not as answers.
- Charter, golden figure 2.1: the section number of definition 2.1 (a carousel session), which only coincides with the B web 730+ fee cell.
- Charter, golden figure 2.4: the section number of definition 2.4, which only coincides with the gap.
- Charter, golden figure 5.2: the section number of the reproduction clause, which only coincides with the E web 730+ fee cell.
- Extract register, 11 of 17 words of the call: the folder's own subject line (Q1 2027 home carousel test slot and its dates); it names no policy.
- Planning thread, 12 of 17 words of the call: the slot's vocabulary; the one voice on the interleave argues against it, so nothing points at the answer.
- Field reference, 7 stump terms: the logger's field definitions; "in the session" and the seven-day rule are its scope statement and a serving rule (realism debts on file), and no sentence says a tile can be ordered from after its session.
- Charter, 7 stump terms: the reproduction clause, definitions 2.2 and 2.4 and the cell table, pins the design requires; no sentence on orders after a session or on borrowed orders.
- Extract register, 5 stump terms: file titles only.
- Fresh-listing commitment, 3 stump terms: the counting rule per served ranking, a pin.
- Planning thread, 6 stump terms: the voices hold beliefs (the pinned tiles convert, the archive never misses with session weights, fee income by cell) and none names the tile count or the guardrail basis.
- Prompt, two stump terms in the question: the question itself (registered policies, carousel sessions), no method or basis.
- Tariff register, 2027-01-04: the deferred January row, a forward-dated entry by design (HZ1); the minutes defer it.
- Capacity note (no REVIEW line, read anyway as loop 2's carrier): the 1 March 2027 sentence carries the date and no cover or fee word, and terms 2 carries the cover and no date, so no single shipped sentence ties the checkout change to the fee.

## Harden loop 1: design (2026-10-09)

Skills run in order: build-pipeline (the hardening loop), stumping (Parts 1, 6.1, 10 and 13), supplemental-stumping (Parts
0 to 6, the device book and the pair arithmetic), dataset-generation (section 12), determinism-check (sections A and B).
This section is the build's current design. In `## Stage 2: design` the ladder, the position table, the dominance line,
the correction grid, the guardrail figures and the ask ledger are superseded by the ones below; the world, the
archive, the pins and the rest of the fork grid stand.

### What round 1 showed, and the repair

Round 1's solver never had to see borrowing: charter 2.2 defines lift as the orders the arm's buyers place over the test,
the orders extract holds every order by buyer, so "all orders by the buyer (any channel) within 7 days of session start"
was the default and the netting of B fell out of it. What its trace held fixed without checking was that the logger's
in-session columns measure the charter's other quantities: "Carousel order rate (from ordered_tiles) by cell vs HC-24".
The repair attacks that assumption with a rung after which the solver's own step (lift over the test, guardrail off the
logger) still completes and still files a wrong name.

**The physics change.** A buyer can leave the home screen open, let the session close (30 minutes without activity) and
come back to order straight from a tile still on screen. The order is placed in the new home session the return opens,
so the orders extract credits it there, and the render log's `ordered_tiles` (orders placed in the session) never sees
it. Under the incumbent and five policies these come-back orders run at 1.2 to 1.7 per 1,000 sessions by cell; under the
session-sequence model (C) they almost never happen (rate scaled to 0.15: 3 orders in 16,544 sessions, none in app
0-29). They are background orders the block template already places on the session's evening or next morning, moved to
2 minutes to 4 hours after the session closed and onto a tile listing, so no order enters or leaves any window and no
lift, half, fee or total moves.

**What the pack says.** Charter 2.4 now reads "the number of orders placed from the carousel tiles it served, per 1,000 of
its carousel sessions in that cell" (it read "its orders placed from a home carousel tile", which also admits every
carousel order by the arm's buyers). The field reference says `ordered_tiles` counts the tiles ordered from in the
session, `home_session_id` is the home session the order was placed in, and a listing shown on a buyer's carousel is
kept off it in their later sessions for seven days. The archive's notes say the same of `in_session_orders`. Nothing
says an order can be placed from a tile after its session.

**What it does to the call.** C, the largest lift over the test (9.8), clears the eight cells on `ordered_tiles` (app
0-29 at -0.96 per cent against Blend v7) and fails them once the rate counts every order placed from its tiles (-3.77
per cent). C's in-session lift in app 0-29 moved from -1.30 to -0.20 per 1,000 so that the logger count passes it;
nothing else in the world moved.

### Gate G

**Gate G line.** decomposition_attribution (each order attributed to the tiles and the test that produced it: the orders
a session's tiles take after the session closes, and the orders a session brings forward from the buyer's own next
days), with method_or_model_selection at rungs 1 and 2 · surface_read_dependency: no · stumping_family:
analytical_non_defect · sole_data_defect: no · deletion test passes · not a lens swap.

- **Litmus.** No reported number or stakeholder conclusion is overturned. `ordered_tiles` is right for what it says
  (orders placed in the session), the orders extract credits every order to the session it was placed in, and no
  shipped artifact computes a guardrail, a lift or a ranking of the six policies. The miss is the solver taking a
  correct in-session count as the charter's rate.
- **Instrument repair.** A logger that counted every order placed from a session's tiles would observe the charter's
  rate directly and close rung 3. No such instrument is withheld: the orders extract (every order, channel and listing)
  and the served tiles ship complete, so the rate is computed from shipped records. The render log is not a suspect
  file in the clean-data sense (it is complete for its stated scope).
- **Lens swap.** The two counts are different populations: the tile count adds 205 orders placed in other sessions,
  which `ordered_tiles` and the session credit both leave out. Not two lenses on the same rows.
- **Deletion.** Delete every voice: nothing in the thread touches the guardrail or C, and the task stays hard.

### The decisive rung

**Measured trap #7, "Uses the ready-made measure"** (5 of the client's 64, 2 under 0.50): the render log's
`ordered_tiles` is the prominent ready-made count, it ties to the orders extract session by session, and it answers a
nearby question. **Inside measured trap #11, "Beats the headline trap, misses the quiet one"** (4 of 64, 2 under 0.50): the
headline fight is the velocity boost's watch-list orders, which the thread argues over and the charter's lift settles;
the quiet one is the guardrail count. Generator G13 (horizon mismatch, gap 1: the logger's count ends with the session,
the charter's rate does not), so the card's decisive generator moved from G9 to G13; G9 stays on the ladder as the
borrowed-order netting.

The seven survival properties (`stumping` Part 1):

1. Written in no sentence: no document says a tile can be ordered from after its session. The seven-day rule is a
   serving rule about impressions, and "in the session" is the logger's scope statement (both carried as realism debts).
2. No corpus nominates it: the archive is a lift corpus on in-session orders and carries no guardrail count.
3. No arithmetic symptom: `ordered_tiles` equals the carousel orders credited to each session in all 150,400 sessions;
   the 205 come-back orders are carousel orders credited to unlogged home sessions, among 56,068 such orders.
4. Not a per-row predicate: it needs each buyer's later orders joined to a different entity (the logged session's six
   tiles) by listing, with the seven-day rule to attribute them.
5. Its enumeration is a construction, not a menu.
6. No cutover date.
7. It survives the deletion.

Dead shapes checked: the call is still argmax under the charter over the six registered policies, and the stump still
applies the rule exactly to a wrong count (the defence the draw recorded). The first crediting (orders credited to the
tile's session) carried an arithmetic symptom on the wrong path and died (Tried and rejected).

### The ladder (five rungs)

| Rung | Construction | Leader | Margin | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Replay over the render rows, unweighted; in-session orders; guardrail on the platform split; floor over rendered tiles | **D** | 1.259 over B | The reproduction clause: replay returns 3 of the 9 archived lifts |
| 1 | One propensity weight per render row | **A** | 1.212 over B | The twins T3 and T7 and the clause: render weights 6 of 9 |
| 2 | One weight per session (9 of 9); the eight cells read on the render log's `ordered_tiles`; floor per served ranking | **C** | 1.237 over B | Charter 2.4 with the orders extract and the served tiles: counting every order placed from C's tiles puts app 0-29 at -3.77 per cent |
| 3 | The guardrail on every order placed from the tiles each arm served (the listing join; A out in web 730+, C out in app 0-29, D out on the floor, F under the bar) | **B** | 1.397 over E | Charter 2.2 with the orders extract and the watch list: 58.5 per cent of B's in-session gain is watch-list purchases its buyers would have made within six days anyway |
| 4 | Lift over the test (orders by the buyer in every channel, 7 to 21 days, or route 2's netting) | **E** | 1.725 over B | |

Every rung names a different candidate (D, A, C, B, E). Gaps: rungs 0 to 2 are the rule gap (the archive-pinned
estimator, Pattern B, #1, with #2 at rung 1); rung 3 is the time gap at the guardrail (G13, #7 inside #11); rung 4 is
the time gap at the lift (G9, #13). The stump is carried by rung 3. A solver who takes rung 4's construction first, as
round 1 did, stands at rung 2 with C (9.845 over E 5.697, 1.728x) until the tile count; a solver who counts the tiles
but stays on in-session orders files B.

**Worth on the committed lift:** 9.661 (D) to 11.018 (A) to 9.845 (C) to 7.957 (B) to 5.697 (E).

### Position table (asserted)

| Rung | E's rank of six | Leader | Runner-up |
|---|---|---|---|
| 0 | 5 | D | B |
| 1 | 4 | A | B |
| 2 | 4 | C | B |
| 3 | 4 (second of the two that clear) | B | E, 1.397x behind |
| 4 | first of the two that clear | E | B |

E leads no intermediate rung and is runner-up only at rung 3.

### Discriminator dominance

At rung 4: B's carried in-session advantage 7.957 / 5.697 = **1.397**; E's edge on the share of its gain it keeps,
(5.697 / 5.697) / (3.303 / 7.957) = **2.409**; required 1.2 x 1.397 = 1.676, held; product 1.725. At rung 3 the move is a
pass or fail: C sits 0.54 points inside the threshold on the logger count and 2.27 points outside it on the tile count.

### Correction grid (24 cells, each asserted by name at 1.15x or better)

Three estimators x four guardrail counts (platform split on `ordered_tiles`; the eight cells on `ordered_tiles`, on the
orders placed from the tiles, and on the buyer's carousel orders within 7 days) x two outcomes (in-session, lift over
the test).

| Estimator | Guardrail count | In-session | Over the test |
|---|---|---|---|
| replay over render rows | any of the four | D (1.259 over B; 1.389 over A on the buyer window) | D, the only policy clearing all three |
| render weights | platform split | A, 1.212 over B | A, 1.359 over C |
| render weights | eight cells, `ordered_tiles` | B, 1.572 over E | B, 1.272 over E |
| render weights | eight cells, orders from the tiles | B, 1.572 over E | B, 1.272 over E |
| render weights | eight cells, buyer's carousel orders 7 days | A, 1.906 over E | A, 1.906 over E |
| session weights | platform split | C, 1.237 over B | C, 1.500 over A |
| session weights | eight cells, `ordered_tiles` | C, 1.237 over B | **C, 1.728 over E (the stump)** |
| session weights | eight cells, orders from the tiles | B, 1.397 over E | **E, 1.725 over B (the answer)** |
| session weights | eight cells, buyer's carousel orders 7 days | C, 1.500 over A | C, 1.500 over A |

E leads one cell of 24. Each wrong cell violates one filed rule: replay and render weights the reproduction clause
(5.2); the platform split the cell table (3); `ordered_tiles` and the buyer window charter 2.4 (orders placed in the
session only; carousel orders from tiles the arm never served); in-session orders charter 2.2.

### Partial readings (asserted where named)

- **Time limits on the tile count.** Any limit of 4 hours or more after the session files exactly the tile count (C1);
  limits under 1.5 hours pass C (-0.96), 1.5 to 3 hours fail it at -2.10, 3 hours or more at -3.77. A limit has no
  footing in 2.4.
- **Buyer windows** (every carousel order by the arm's buyers within 1, 7 or 21 days): C passes in all three (-0.83,
  -0.54, -0.42), so they file C with the lift over the test.
- **Follow-up windows on the lift** (tile count): 1 to 3 days name B (7.6, 7.0, 6.2); 4 and 5 days name E with B at 5.0
  and 4.0 (a wrong runner-up figure); from day 6 every policy is flat (C1 over 7 to 21 days and calendar days).
- **Flat haircuts on in-session lifts** at B's borrowed share (58.5 per cent) or the pooled share (0.75 per cent) name B.
- **The headline on the slot's planned cell mix** (R2, app from W03): E 5.716, B 3.314, gap 2.402, the same bins as the
  logged window's 5.697, 3.303 and 2.394 (C1; round 1's 5.8 came from the January surge, now cut, see Tried and
  rejected). On the first release's mix (P2 mishandled) E reads 5.844: the device reaches the headline only through a
  reading that is wrong twice (reweighting the charter's offline score, 5.1, and the superseded release).

### Fork grid: the axes this loop changed (the Stage 2 table stands for the rest)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population (guardrail) | orders placed from the tiles the arm served | C4: the buyer windows add tiles the arm never served and file C; violate 2.4 |
| 3 | Attribution window (guardrail) | no limit after the session | C1 from 4 hours; shorter limits violate 2.4 (priced above) |
| 9 | Boundary inclusivity | "more than 1.5 per cent below" | C4: failing cells A web 730+ -2.51, C app 0-29 -3.77; every other policy-cell at +1.2 or better on either count; coarse cuts +1.3 or better |
| 13 | Order of operations | the guardrail count is independent of the lift basis | C1: the breaches are the same under in-session and over-the-test lifts |
| 16 | Identity normalisation | listing ids shared by orders and served tiles | C1: every come-back resolves to one tile of one logged session |
| 19 | Code semantics | channel carousel = ordered from a home carousel tile; `home_session_id` = the session placed in | filed (field reference); C1: `ordered_tiles` equals the carousel orders credited to each session |
| 21 | Scope of a stated clause | the seven-day rule governs carousel serving across sessions | filed; asserted in the data (no shown listing reaches its buyer through a carousel tile more than 4 hours after the session) |
| + | Headline cell mix | the logged window (5.1) | C1 with the slot's planned mix |
| + | VAT (F1) | fee income excluding the 21 per cent VAT, as Finance books it | filed (statement); C1: VAT taken off order by order to the cent files every cell in the same bin (min 0.015 inside); C4: VAT kept in moves all 48 cells, 21 per cent taken off the gross 44 |
| + | Balance purchases (F2) | covered and charged | filed (terms 1, 2 and 5; field reference: the payments file is card and iDEAL captures); C4 |
| + | Fee totals, pooled | refused (capacity note: cell by cell) | placed at least 5 from the golden hundred's edges either side, recorded |

### Ask ledger (supersedes Stage 2's; asks unchanged in wording)

**Main call's declared row population.** The render log, the served rankings (now including the six tile listing ids,
which the tile count joins on), the orders extract (order id, buyer, listing, ordered at, channel, home session; never
price, delivery, platform or category), the archive, the charter, the commitment, the register, the field reference.
Zero device rows in it: the fee devices live in the price, delivery and payment columns and in files the main call
never opens, and the call and the guardrail breaches are asserted unchanged with every price scrambled and every
delivery set to shipped.

| Ask | Figures | Construction layer | Device layer: primaries; hazards | Use (H18) |
|---|---|---|---|---|
| 1 Grid | 48: each policy's change in buyer-protection fee income per 1,000 carousel sessions by cell, EUR, one decimal | orders over the test by cell (rung 4) | **F1 fee income net of VAT; F2 purchases paid from a balance**; P1 pickups paid in person, HZ1 the January tariff row, HZ2 the price paid | what each option is worth in each cell beside the call |
| 2 Totals | 12: extra orders and extra fee income over the twelve weeks, nearest hundred | the lift over the test by cell on the slot's planned cell traffic | fee half: F1, F2, P1, HZ1, HZ2; both halves: P2 the R2 restatement, HZ3 the app release gate | what the quarter buys beside the call |

**Primaries, fresh this loop (both silent: nothing on the ask path states that they matter).**
- **F1, fee income net of VAT (D3, units set by agreement).** The tariff is what buyers pay, VAT included; Finance books
  fee income excluding the 21 per cent (statement header, account 1630). The careless path (tariff fee per order) files
  gross figures 21 per cent high in every cell. Organs split: the statement's header (documentary) and its figures, which
  tie only under the division (structural).
- **F2, purchases paid from a Vouwlijn balance (D4, an absent channel).** 7 per cent of shipped purchases are paid from a
  balance, covered and charged, and absent from the payments file, which is the provider's card and iDEAL captures. The
  careless path (no capture, no fee) drops them. The over-cleaning half is P1: charging every order without a capture
  also charges pickups paid in person. Organs: terms 1, 2 and 5 (documentary), the field reference's payments line and
  the statement's covered-purchase count (structural).

**Hazards** (P1, HZ1, HZ2 on both asks' fee figures; P2 and HZ3 on both totals) keep their Stage 2 definitions.

**Referee (exactly one, byte-clean).** Finance's July to September fee-income statement by month and platform. It ties
to the cent only when every covered purchase is charged (captures at the capture-date tariff, balance purchases at the
order date), in-person pickups are left out and the VAT is taken out: the six rows sum to EUR 320,877.16 against EUR
360,097.35 for the provider's captured fees as charged and EUR 297,601.12 for those net of VAT. It gives no policy or
cell a level and says nothing about January.

**Per-ask stops** (asserted). Ask 1: all 31 subsets of the five fee devices and the natural read (every order priced on
the formula, VAT in, asking price, January row, in-session orders) carry every cell out of its bin by at least 0.0456;
the over-cleaners move 43 to 47 cells (fees as charged 47, every pickup dropped 43, every accepted offer 43, the old
tariff 46, VAT taken off the gross 44); the in-session basis moves B's four older cells and nothing else. Ask 2: the
first release, all twelve weeks on the app, both, and the natural read sit at least 5 outside the golden hundred on
every order total; 760 of the 762 fee readings (127 per policy) do, and B with only P1 mishandled and F on the first
release alone sit inside it (single devices whose effect on that total is under 30, placed at least 5 from the edges); the pooled readings sit at
least 5 from the edges, five of twelve inside (B, E and F orders, D and E fees).

**Pair arithmetic (planning weights 38 / 7 / 55; 4 call, 4 file, 64 ask criteria at 0.86).**
- Cracker (lands E): the call block, the files, the heatmap's four parts and the six order totals (it handles P2 and HZ3,
  as round 1 did); on round 1's fee path (captures re-priced at the slot tariff, price paid, in-person pickups free, VAT
  kept in) it keeps 0 cells and 0 fee totals, and 0 if it also drops balance purchases or drops only those. **53.6**.
- Mirror (files C on the logger count): 3 call criteria (the exclusions it names), the files, the euro scale, the six
  order totals, the same fee path. **16.0**.
- **Pair 34.8**, under 40: 55 x (Lc + Ls) = 55 x (10 + 7) / 64 = 14.6, inside 28 - r = 25.
- **Exposure, stated:** a cracker that reads Finance's statement and handles F1 and F2 keeps the grid and the fee totals:
  pair 58.0. The ask layer rests on the referee going unread, which round 1's trace supports (its path never opened it).
- The order half (6 criteria) keeps its Stage 2 devices only; no fresh silent device fits the traffic path without a new
  organ (Tried and rejected), so it leaks to both sheets and the arithmetic above counts it.

### Realism debts added

- C's buyers hardly ever come back to a stale tile; the register says C re-ranks after every render, which a reader may
  take as the reason, and no document says so.
- "In the session" (field reference, archive notes) and the seven-day rule are true, needed sentences that a sharp
  reader could turn into the question.
- The statement's header states the VAT and "every payment method": the referee is the organ for F1 and F2.
- The first-release slot-mix headline (5.8) is a compound wrong path that reaches a graded figure through P2.

### Stopping rule

Loop 1 of 3 on this architecture. Round 1 is re-run on this build. A landed main call through the tile count, or a
proxy at or over 40 with the call missed, is loop 2's brief; a loop that has to move the guardrail count's physics again
is the signal to re-root at stage 1 with this architecture moved to the card's lineage rather than to spend loop 3.

## Harden loop 1: build record (2026-10-09)

Supersedes `## Build record` for every figure below; Stage 3's write-up section is superseded by `submission.md` as
rewritten in this loop.

### Gates

- **Generator:** 306 assertions passed (`checks.py`), on the files as written.
- **Independent verifier:** `verify_pack.py` 102 of 102 on the task folder, on its own code path, every figure agreeing
  with the build record.
- **Determinism of the build:** two builds into different roots, 23 target files and `metadata.json` byte-identical (the
  records differ only in the scrub log's output path).
- **Input gates:** 23 files, 9 formats, the render log at 404,100 rows, two distractors named in `metadata.json` only.
- **Metadata:** containers clean (`scrub_producer_metadata.py`, target and golden), forward dates on the allow-list only.
- **Golden:** `golden.py` executes the notebook top to bottom, writes the PNG, and every figure agrees with the record;
  realism pass done (footer split onto two lines, colour bar and legend lifted, VAT read from the statement).
- **Leak sweep:** `leak.py` REVIEW, no LEAK (the cell table's figures in the charter, the call's ordinary words in the
  index and the thread, the deferred January tariff row's date, generic stump vocabulary). No shipped text names the
  come-back orders or says a tile can be ordered from after its session.
- **Fingerprint:** card updated (stump, driver, decisive generator G13 first); `guard.py validate` clean, `check` and
  `heart` WARN with no BLOCK (repeat.gate_g, repeat.decision, as answered at the draw), `surface` 0 pairs promoted.

### The answer and the stump, as built

E, lift over the test **5.697** (5.7); runner-up B **3.303** (3.3); gap **2.394** (2.4). The stump path (session weights,
eight cells on `ordered_tiles`, lift over the test) files C at **9.845** with E runner-up at 5.697, gap 4.148.

### Guardrail by count (per cent against Blend v7)

| Count | C app 0-29 | A web 730+ | Breaches |
|---|---|---|---|
| `ordered_tiles`, and the orders credited to the session | -0.957 | -2.736 | A |
| every order placed from the tiles (no limit, or any limit of 4 hours or more) | -3.771 | -2.512 | A, C |
| tiles within 1 hour | -0.957 | -2.679 | A |
| tiles within 1.5 or 2 hours | -2.102 | -2.623, -2.914 | A, C |
| buyer's carousel orders within 1 day | -0.826 | -2.111 | A |
| buyer's carousel orders within 7 or 21 days | -0.535, -0.423 | -1.229, -0.927 | B in every cell (its shown listings never come back through a carousel), C passes |

Come-back orders: 205, 2 minutes to 4.0 hours after the session (incumbent 72, A 23, B 26, C 3, D 29, E 23, F 29).

### Asks, as built

Fee grid (EUR per 1,000 carousel sessions; cells app 0-29 to web 730+): as `submission.md` block 4, item 3, recomputed
by the verifier to the cent. Every cell at least 0.035 inside its bin and at least 0.005 off the round value; four cells
under EUR 1.00 (C app 0-29, F app 730+, B web 180-729, F web 180-729).

| Policy | Extra orders | Extra fee income, EUR |
|---|---|---|
| A two-tower personaliser | 16,876.4 | 18,318.0 |
| B velocity boost | 8,818.7 | 10,376.5 |
| C session-sequence model | 26,123.6 | 32,114.4 |
| D local pickup boost | 13,223.6 | -33,520.5 |
| E sequence ranker, fresh-listing interleave | 15,212.9 | 18,788.4 |
| F seller-diversity re-ranker | 3,720.5 | 3,076.7 |

Every total 20 to 45 from the edges of its hundred, on 2,661,486 arm sessions (app cells from W03).

### Files changed

Generator: `params.py` (come-back rates, the C scale, VAT, the wallet share, the January surge cut to 2 and 1 points, C's
app 0-29 lift), `world.py` (balance-paid flags), `records.py` (come-back orders, balance purchases, the shown-listing
channel rule, protected purchases for Finance), `place.py` (five fee devices, off-round placement, either-side traffic
readings), `traffic.py`, `analysis.py` (the tile count), `asks.py`, `docs.py` (charter 2.4, field reference, archive
notes, terms 5, the statement), `build.py`, `checks.py`, `verify_pack.py`, `golden.py`. Pack: every data file
regenerated. Write-up: `submission.md` blocks 1 to 4. Card: `cards/task122.json`.

## Stage 3 after harden loop 1: write-up and ship checks (2026-10-09)

Skills run in order: submission-writeup, golden-realism (dataviz loaded first), reduce-house-fixes, leak-check,
fingerprint. Nothing in the generator, the pack, the goldens or `submission.md` needed to change; every check was re-run.

- **Rebuild.** `build.py` into the scratchpad: 306 assertions passed; all 23 target files and `metadata.json`
  byte-identical to the shipped ones. `verify_pack.py` 102 of 102 against that build record.
- **Golden.** `golden.py` re-run: both files byte-identical to the previous run, every figure agreeing with the
  harden loop 1 record (E 5.697, B 3.303, gap 2.394; 48 fee cells; 12 totals; breaches A web 730+ and C app 0-29;
  archive 9, 6 and 3 of 9).
- **submission.md.** Five blocks kept as rewritten in loop 1; block 4's 48 cells and 12 totals diffed against
  `verify_pack.py --out`, 60 of 60 equal at the filed rounding. No em dashes.
- **golden-realism.** Chart and notebook read cold; the loop 1 pass holds (finding title, diverging palette with a
  grey zero, labelled hatching, outlined row, status column, source footer; the notebook's argument in markdown,
  control assertions left in, the figure displayed inline). Texture claims checked against the pack: Finance's
  account 8120 and the 21 per cent VAT (statement header), extracts pulled 12 October (extract register), the
  statement total EUR 320,877.15 (its own total row; the six rows sum to 320,877.16 by rounding path), T7 as the
  per-render weight's widest miss (2.65 against 1.08 next). No edit, so figures unchanged.
- **reduce-house-fixes.** H1 audit clean on `target/` and `golden/` (band 2026-01-01 to 2026-10-28). H4: `golden/`
  holds exactly the two named files; the manifest in `metadata.json` equals the 23 shipped files. H6: the seven-day
  serving rule the notebook states holds on all 902,400 served tiles (no listing shown twice to a buyer), and the
  fee rule is back-tested in the notebook on every capture. H8: every citation resolves (charter 2.2, 2.4, 3, 4(a)
  to (c), 5.2, 6; terms 2 and 3; release log 14 August; capacity note). H11: one `submission.md`, one `prompt.md`.
- **Leak.** `leak.py --asof 2026-10-28`: REVIEW, no LEAK; every line answered under `## Leak review`.
- **Fingerprint.** `surface`: 0 promoted pairs (nearest task121 at 0.096). `heart`: WARN, no BLOCK; nearest heart
  text 0.05 (task121's stump). WARNs: repeat.gate_g and repeat.decision as answered under Guard; driver.near 0.13
  against this slot's own first draft (lineage v1), whose move was a written library-fill rule over failing
  proposals, not a count that ends with the session. Card `notes` corrected to name G13 as the decisive after
  loop 1 (answer, answer_source, spine rows 404,100, deliverables and opening move already current);
  `guard.py validate` clean.

## Harden loop 2: design (2026-10-09)

Skills run in order: build-pipeline (the hardening loop), stumping (Part 10), supplemental-stumping (the device book,
the nine laws, the pair arithmetic), dataset-generation (section 12), determinism-check (sections A and B). This
section is the build's current design of the ask layer. Round 2 missed the call where the stump sentence says it would,
so the main ladder, the position table, the dominance line and the correction grid of `## Harden loop 1: design`
stand as built; they are restated under the build record below with the figures re-asserted.

### What round 2 showed, and the repair

Round 2 (plain, proxy 48.7) stopped at rung 2 on C and kept the asks at its step 7 by reconciling its fee basis to
Finance's Q3 statement. Under loop 1 the slot's fee basis and the logged window's were one basis, so a statement that
ties the logged window to the cent was a manifest total equal to the repaired truth: law 8's oracle, not a referee.
Every fee device was either settled by it (VAT out, balance purchases charged) or filed on the fee path (terms 2 and
3, the minutes), so no device the statement can see can carry the grid. The repair moves the graded basis off the
statement: the slot's cover differs from the logged window's for a reason filed off the fee path, so the statement
still ties to the cent, still arbitrates the logged window's basis, and now certifies the wrong basis for the slot.

**FX, the checkout change of 1 March 2027 (fresh primary on all 48 cells and the six fee totals).** One sentence in
the capacity note's overlaps section: the checkout change of 1 March 2027 is server side, a launch rather than a
test, and runs alongside the Q1 slot on both platforms; from that day a pickup order is paid at checkout when it is
placed and sellers no longer take payment at the handover. Read with terms 2 (pickup orders paid through checkout are
covered), the slot's weeks before 1 March run on the logged window's cover, where a pickup paid to the seller in
person carries no fee, and its last four weeks on full cover. The change in fee income per 1,000 carousel sessions
while the slot runs is therefore each cell's blend: the arm's planned sessions before 1 March (web 2027-W01 to W08,
app W03 to W08, so 2/3 and 0.6 of each cell) at the logged window's rate and the rest at full cover.

- Wrong paths: the reconciled basis carried through the slot (round 2's step 7, which the statement confirms to the
  cent); full cover for the whole slot (the line found, its date not); the app blend counted from 4 January (HZ3
  inside the blend, recorded as a partial reading).
- Silent: nothing on the fee path names it (terms, register, minutes, statement); the logged window's records are
  complete and consistent under the old cover, and the referee ties under it. The sentence sits in a note the solver
  opens for traffic, and says the launch runs alongside the slot, which reads as touching both arms alike; it does
  not, because the arms' shares of pickups paid in person differ (the local pickup boost's most of all).
- Two antidotes in two files: the capacity note's sentence carries the date and no cover or fee word; terms 2
  carries the cover and no date.
- Forced, not argued: days, weeks and planned sessions give the same shares, because the 2026 slot weeks are level
  within each cell (no January bump; each cell's last four weeks set to half of its first eight on the web and two
  thirds of its six on the app, asserted); and no in-person order changes regime between a session and its follow-up,
  because a watched listing is never paid at the handover, so none of the velocity boost's brought-forward orders
  crosses 1 March on a different cover from the purchase it replaces.
- Family: the version of the cover in force while the slot runs (D2 in the forward window, D4's absent channel
  closing): what the operation commits to next, not a correction of anything filed.

**Referee (exactly one, byte-clean, unchanged).** Finance's July to September statement. It arbitrates the logged
window's basis (VAT out, balance purchases charged, pickups paid in person uncharged, the tariff in force on the
capture date) and hands over no slot level: on the slot's basis the logged window's fees miss it by the in-person
pickups, so a solver who reconciles to it is confirmed in the basis that is wrong for the slot.

**Hazards kept.** F1 (VAT), F2 (balance purchases), HZ1 (the January row) and HZ2 (the price paid) on every fee figure,
each now crossed with FX's three states; P2 (R2) and HZ3 (the app release gate) on the totals. Each is settled by a
filed rule or by the referee, so each prices careless paths, not the top two.

### Ask ledger (supersedes harden loop 1's; asks unchanged in wording)

Main call's declared row population: unchanged (render log, served rankings, the orders extract's order, buyer,
listing, time, channel and home session, the archive, charter, commitment, register, field reference). Zero device
rows in it: the cover, the prices, deliveries and payments live in columns and files the call never reads, and the
capacity note is on the traffic path only.

| Ask | Figures | Construction layer | Device layer | Use (H18) |
|---|---|---|---|---|
| 1 Grid | 48: change in buyer-protection fee income per 1,000 carousel sessions by policy and cell, EUR, one decimal | orders over the test by cell (rung 4) and the planned traffic's weeks either side of 1 March | **FX**; F1, F2, HZ1, HZ2 | what each option is worth in each cell beside the call |
| 2 Totals | 12: extra orders and extra fee income over the twelve weeks, nearest hundred | the lift over the test by cell on the planned cell traffic | fee half: FX, F1, F2, HZ1, HZ2; both halves: P2, HZ3 | what the quarter buys beside the call |

**Per-ask stops (asserted).** Ask 1: each of the 47 combinations of FX (blend, logged cover throughout, full cover
throughout) with the four hazards, and the natural read, carries every cell out of its bin; the blends by days, by
weeks and by planned sessions file the same grid (C1); VAT taken off order by order to the cent files the same grid
(C1); the over-cleaners (fees as charged, every pickup dropped, every accepted offer, the pre-September tariff, VAT
off the gross) each move most cells. Ask 2: the order readings as in loop 1; the fee readings are FX's three states
by the four hazards by the four traffic readings (191), each at least 5 outside the golden hundred unless recorded
as an either-side reading.

**Pair arithmetic (planning weights 38 / 7 / 55; 4 call, 4 file and 64 ask criteria at 0.86).**
- Cracker (lands E), on round 2's fee path (the reconciled basis carried through the slot): the call block, the files,
  the heatmap's four parts and the six order totals, no fee cell and no fee total. **53.6**.
- Mirror (files C on the logger count), the same fee path: three call criteria, the files, the euro scale, the six
  order totals. **16.0**.
- **Pair 34.8**, under 40. Each top response that both finds the 1 March line and blends by the planned weeks keeps the
  54 fee criteria and adds 23.2 to the pair; one that finds the line and applies full cover to the whole slot keeps
  no cell (asserted).
- **Exposure, stated:** the layer no longer rests on the referee going unread. Reading it confirms the wrong basis.
  It rests on the 1 March line staying one uninvited question away from the fee step, and on the blend: a solver who
  asks what changes for fees while the slot runs, as round 2 did for the tariff, and reads the overlaps line with
  terms 2, keeps the grid.

### Fork grid: the axes this loop changed (harden loop 1's table stands for the rest)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 3 | Attribution window (fee cover) | a session's fees take the cover in force on its date | C1: no brought-forward order changes cover between a session and its follow-up (watched listings never paid at the handover); background orders are the same in every arm |
| 5 | Version basis (cover) | logged window's cover to 28 February, full cover from 1 March | filed (capacity note with terms 2); C4: carrying either cover through the slot moves every cell |
| 6 | Divisor (blend weights) | the arm's planned sessions either side of 1 March, per cell | C1: by days, weeks and sessions the shares are 2/3 (web) and 0.6 (app) to within 0.0005, asserted per cell |
| 22 | Forward window contents | the logged window's orders at the slot's rules | filed (charter 5.1 for orders; capacity note, terms, minutes and register for the rules) |
| + | Fee cover in the logged window | pickups paid in person uncharged | filed (terms 2); the referee ties only under it |

### Realism debts added

- The 2026 slot weeks carry no January bump and are level within each cell to the share the blend needs (a step of
  under one per cent at 2026-W09 in some cells, inside the week-to-week noise).
- Watched listings are never collected and paid at the handover; a buyer who watches a listing pays for it through
  checkout, pickup or not.
- A cover change dated inside the slot is a coincidence of the calendar a reader may notice; the note dates it to the
  start of a month, server side, with the slot named only as something it runs alongside.

### Stopping rule

Loop 2 of 3 on this architecture. Round 1 is re-run on this build. A landed call through the tile count, or a proxy at
or over 40 with the call missed because a response found the 1 March line and blended, is loop 3's brief; a loop that
has to move the fee cover again, or the guardrail count's physics, is the signal to re-root at stage 1 with this
architecture moved to the card's lineage rather than to spend loop 3 on a third device.

## Harden loop 2: build record (2026-10-09)

Supersedes `## Harden loop 1: build record` for every figure below. `submission.md` blocks 3 and 4 are rewritten in this
loop (the traffic split at 1 March as step 5, the blended fee as step 6, the 48 cells and 12 totals); blocks 1 and 2
stand.

### Gates

- **Generator:** 349 assertions passed (`checks.py`), on the files as written.
- **Independent verifier:** `verify_pack.py` 122 of 122 on the task folder, on its own code path, every figure agreeing
  with the build record; it reads the 1 March date from the capacity note and the cover from terms 2.
- **Determinism of the build:** two builds (the task folder and a scratch root), 23 target files and `metadata.json`
  byte-identical; the records differ only in the scrub log's output path.
- **Input gates:** 23 files, 9 formats, the render log at 404,100 rows, two distractors named in `metadata.json` only.
- **Metadata:** containers clean (`scrub_producer_metadata.py` on `target/` and `golden/`); the one forward ISO date is
  the deferred January tariff row, as before.
- **Golden:** `golden.py` executes the notebook top to bottom, writes the PNG, and every figure agrees with the record.
  Realism pass: the chart footer split onto three lines (the cover line had run off the canvas), colour bar and legend
  lifted to make room, and the summary's fee paragraph reworded to say what the statement covers and what changes on
  1 March. New notebook sections: the slot's traffic and the cover change (the plan table with each cell's share before
  1 March), then the fee on both covers, blended.
- **Leak sweep:** `leak.py --asof 2026-10-28` REVIEW, no LEAK. Two new REVIEW lines are clause numbers: the fee cells 2.1
  (B web 730+) and 5.2 (E web 730+) match the charter's sections 2.1 and 5.2. No shipped text ties the checkout change to
  the fee: the capacity note's sentence carries no cover or fee word, and terms 2 carries no date.
- **Fingerprint:** `surface` 0 promoted pairs (nearest task121 at 0.096); `heart` WARN, no BLOCK (driver.near 0.13
  against this slot's own first draft; repeat.gate_g and repeat.decision as answered at the draw). Card unchanged: the
  call, the stump, the driver and the deliverables did not move.
- **House fixes:** H4 (`golden/` holds the two named files), H8 (terms 2 and 3, charter 2.2, 2.4 and 5.2, the capacity
  note all resolve), H11 (one `submission.md`, one `prompt.md`); every block 4 figure diffed against the record, 60 of
  60 equal at the filed rounding. No em dashes.

### The answer and the stump, as built (unchanged)

E 5.697 (5.7), runner-up B 3.303 (3.3), gap 2.394 (2.4); the stump path files C at 9.845 with E at 5.697, gap 4.148. The
ladder re-asserted: rung 0 D (margin 1.259), rung 1 A (1.212), rung 2 C (1.237), rung 3 B over E (1.397), rung 4 E over
B (1.725); E ranks 5th, 4th, 4th and 4th, then leads. Dominance: carried 1.397, edge 2.409, product 1.725. The guardrail
by count as in loop 1 (C app 0-29 -0.957 on `ordered_tiles`, -3.771 on every order placed from the tiles; A web 730+
-2.736 and -2.512); 205 come-back orders. The archive: the per-session weight 9 of 9, per render 6, replay 3.

The headline on the slot's planned cell mix, now on the levelled traffic: E 5.689, B 3.293, gap 2.396, the same bins as
the logged window's and at least 0.039 from every edge (C1). C reads 9.872 there, so a stump filed on the slot mix
carries 9.9 rather than 9.8. On the first release's mix (P2 mishandled) E reads 5.817.

### The traffic plan, as built

- 2026 slot weeks level within each cell (no January bump), so each cell's share before 1 March is 0.600 on the app
  (W03 to W08 of W03 to W12) and 0.667 on the web (W01 to W08 of W01 to W12), the same by weeks, days and planned
  sessions to within 0.0005 (asserted per cell).
- Placement factors 0.986 to 1.015 per cell; R2 moves 6.19 per cent of sessions and keeps every platform-week total.
- No watched listing is paid at the handover (asserted), so no brought-forward order changes cover between a session
  and its follow-up.

### Ask 1, the fee grid, as built

As `submission.md` block 4 item 3, recomputed by the verifier. Every cell 0.036 to 0.044 from its bin's edges and at
least 0.006 off the round value; three cells under EUR 1.00 (C app 0-29, F app 730+, F web 0-29).

- All 47 device readings (FX's three states by the four hazards, less the golden) and the natural read carry every
  cell out of its bin. The nearest is D app 0-29 with only the January row applied, 0.0246 outside; the floor is
  asserted at 0.02.
- FX alone: the logged window's cover carried through the slot (round 2's path, the one the statement confirms) moves
  all 48 cells, the nearest 0.0582 outside; full cover through the slot moves all 48, the nearest 0.0819 outside; the
  app blend counted from 4 January moves 17 cells (partial, recorded).
- C1: VAT taken off order by order to the cent files every cell in the golden bin (at least 0.0227 inside; the pair
  lever needed no pairs on this placement); the blend by days, weeks or planned sessions files the same grid.
- Over-cleaners: fees as charged move 45 cells, every pickup dropped 46, every accepted offer 41, the pre-September
  tariff 46, VAT off the gross 43; the in-session basis moves B's four cells over 180 days and no other.

### Ask 2, the twelve-week totals, as built

| Policy | Extra orders | Extra fee income, EUR |
|---|---|---|
| A two-tower personaliser | 16,576.1 | 19,808.7 |
| B velocity boost | 8,608.7 | 10,326.2 |
| C session-sequence model | 25,809.9 | 33,222.5 |
| D local pickup boost | 12,980.6 | -14,012.0 |
| E sequence ranker, fresh-listing interleave | 14,873.9 | 19,217.0 |
| F seller-diversity re-ranker | 3,612.2 | 3,516.7 |

Every total at least 23.8 from the edges of its hundred (B's fee and E's orders the nearest). Per policy, 198 readings
(five order readings, the pooled and natural fee reads, and the 191 fee device readings: FX's three states by the four
hazards by the four traffic readings, less the golden), each at least 5 from the golden hundred's edges. Inside the
hundred, recorded: B's fee with only FX mishandled (the logged cover carried, 10,300; the one fee total round 2's path
keeps), F's fee on the first release alone, and three compound readings (D with both traffic devices, F2, HZ1 and HZ2
wrong; F with the app gate missed and the logged cover carried; F with both traffic devices missed and the logged cover
carried). The pooled reads, refused by the capacity note, sit inside for B's, E's and F's orders and C's fee, as in
loop 1. No order reading sits inside.

### Referee, pair and the proxy, as built

- **Referee.** Finance's statement, EUR 333,347.23, reproduced to the cent only on the logged window's cover with VAT
  out and balance purchases charged (the captures alone are 375,204.30 gross, 310,086.20 net of VAT; balance-paid
  purchases are 6.8 per cent of protected ones). Full cover overshoots it by 8.71 per cent, so the statement certifies
  the logged window's basis and no other, and the slot's basis is the one it does not tie.
- **Device rows in the main call's population:** 0 (asserted).
- **Pair arithmetic (as built):** cracker 54.5, mirror 16.9, pair 35.7 on round 2's fee path, under 40. It is 0.9 above
  the design's 34.8 because B's fee total stays inside its hundred under FX alone, one total kept on both sheets. A
  response that finds the 1 March line and applies full cover to the whole slot keeps no cell and no fee total.
  Exposure: one top response that lands the call and blends by the planned weeks puts the pair at 58.4.
- **Token proxy (`grade.py`), simulated on this pack.** Round 2's own answer sheet rewritten with this pack's figures on
  its own path (C at 9.8, the logged cover carried, the order totals right) scores 45.0, call missed, 1 of 8 items over
  the bar; full cover through the slot scores 46.5. Every fee value is wrong on both, but 86 of the grid item's 134
  tokens are policy and cell labels that any grid in the asked shape matches, notebook item 1 matches on the runner-up
  answer's HC-37 and 5.7, and the six order totals match because P2 and HZ3 are settled by filed rules. The pair
  arithmetic above counts criteria, not tokens; the stage 4 proxy gate reads tokens.

## Stage 3 after harden loop 2: write-up and ship checks (2026-10-09)

Skills run in order: submission-writeup, golden-realism (dataviz loaded first), reduce-house-fixes, leak-check,
fingerprint. Nothing in the generator, the pack, the goldens or `submission.md` needed to change; every check was re-run.

- **Rebuild.** `build.py` into the scratchpad: 349 assertions passed; all 23 target files and `metadata.json`
  byte-identical to the shipped ones. `verify_pack.py` 122 of 122 on the task folder against that build record (call
  HC-37 5.6966, runner-up HC-33 3.3028, gap 2.3938).
- **Golden.** `golden.py` re-run into the scratchpad: both files byte-identical to `golden/` (sha256 2b2d1d04 notebook,
  7c4d9049 PNG); it executes the notebook top to bottom and reports every figure agreeing with the loop 2 record (E 5.7,
  B 3.3, gap 2.4; 48 fee cells; 12 totals; breaches A web 730+ -2.5% and C app 0-29 -3.8%; archive 9, 6 and 3 of 9;
  D 8.8 fresh tiles per 100; F 1.4).
- **submission.md.** Five blocks as rewritten in loop 2. Block 4's 48 cells and 12 totals diffed mechanically against
  `verify_pack.py --out`, 60 of 60 equal at the filed rounding; blocks 2 and 3 figures (9 of 9, 3.8%, 2.5%, 8.8, 1.4,
  8.0 and 3.3, 5.7, six of ten and eight of twelve weeks before 1 March) agree with the golden's printout. No em dashes.
- **golden-realism.** PNG and notebook read cold: finding title, diverging red to blue with a grey zero, labelled
  hatching, outlined chosen row, status column, three-line source footer that fits the canvas; the notebook opens on the
  call, carries the argument in markdown, keeps control assertions in, and has no hedge words. No edit, figures unchanged.
- **reduce-house-fixes.** H1 audit clean on `target/` and `golden/` (band 2026-01-01 to 2026-10-28). H4: `golden/` holds
  exactly the two named files; the `metadata.json` manifest equals the 23 shipped files. H6: the seven-day rule the
  notebook states holds on all 902,400 served tiles (no listing shown twice to a buyer; the 205 come-back orders all
  within 4.0 hours, none later than seven days), and the fee rule is back-tested in the notebook on every capture. H8:
  charter 2.1, 2.2, 2.4, 4(a) to (c), 5.2; terms 2 and 3; the release log's 14 August entry; the capacity note's 1 March
  sentence all resolve. H11: one `submission.md`, one `prompt.md`, no backup or snapshot in the task tree.
- **Leak.** `leak.py --asof 2026-10-28`: REVIEW, no LEAK, 16 REVIEW lines, each answered under `## Leak review`.
- **Fingerprint.** `surface`: 0 promoted pairs (nearest task121 at 0.096). `heart`: WARN, no BLOCK; nearest heart text
  0.05 (task121's stump); WARNs driver.near 0.13 against this slot's own first draft, repeat.gate_g and repeat.decision,
  as answered at the draw and at loop 1. Card already current (answer, answer_source, spine rows 404,100, deliverables,
  opening move deliverable-first); `guard.py validate` 119 cards, 0 invalid.

## Harden loop 3: design (2026-10-09)

Skills run in order: build-pipeline (the hardening loop), stumping (Part 10, Part 1's survival properties),
supplemental-stumping (the device book, the nine laws, the pair arithmetic, the top-two reading of leakage),
dataset-generation (section 12), determinism-check (sections A and B). This section is the build's current design of the
ask layer. Round 3 missed the call where the stump sentence says it would, at the tile count, so the main ladder, the
position table, the dominance line and the correction grid of `## Harden loop 1: design` stand; they are re-asserted
under the build record below. Loop 3 of 3 on this architecture.

### What round 3 showed, and the repair

Round 3 (plain, token proxy 51.1, about 23 to 31 read by hand) filed C at rung 2 for the second round running and kept
all 48 fee cells and all twelve totals. Two habits carried every device. Its fee model was reconciled to Finance's Q3
statement, which ties to the cent only on the logged window's own fee basis, so the VAT, the balance purchases and the
pickups paid at the handover were settled in one pass; and every other device was a dated, named sentence in a note the
ask path opens (the January deferral in the minutes, R2 in the release log, the app gate in the capacity note, the 1 March
checkout change in the capacity note's overlaps). The brief: the statement must stop tying under the golden fee basis,
and the traffic and tariff rules must leave the documents the ask path opens.

The repair is a rung on the fee path after which the solver's own step 8 still completes and still returns the wrong
answer: reconcile the fee model to Finance's statement and carry it into the slot. The statement still ties to the cent,
on the logged window's checkout. The slot runs on a different checkout, and no note on the ask path says so.

**FC, the checkout in force (fresh primary on all 48 cells and the six fee totals; measured trap #13, validates on one
population and applies to another, with #5, the population a flag suggests).** Checkout 3 went live on 21 September 2026,
the day after the logger window closed, with app release 26.19 and on the website the same day: every order is paid when
it is placed, pickups included, so a seller no longer takes payment at the handover. The slot runs from January to March
2027 under Checkout 3, so every pickup in it is paid through checkout and covered (terms 2), and every logged order
carries the fee in the slot. The golden prices every order in each logged session's 21 days at the tariff in force on the
slot's dates, on the price paid, VAT out, the pickups the logged window saw paid at the handover included.

- **Wrong path** (round 3's step 8 carried into the slot): a pickup with no capture left uncharged. It reproduces
  Finance's July to September statement to the cent, because every pickup from 21 September carries a capture, so the
  rule ties September as well as July and August. The statement certifies the logged window's checkout, which is wrong
  for the slot; charging every pickup, the golden's basis, overshoots it (asserted), so the statement no longer ties
  under the golden fee basis.
- **Silent.** No document on the ask path names the change. The terms (September 2026) are unchanged and true under
  both checkouts; the capacity note, the minutes, the release log, the field reference and the statement say nothing of
  it; the release calendar shows 26.19 on 21 September with its standard release line. The thread names Checkout 3 once,
  in Amélie Middelkoop's message about sellers' autumn, without saying what it changed. The records show it: from 21
  September every pickup order carries a card or iDEAL capture, none paid at the handover, against about half paid at
  the handover before.
- **Seven properties.** 1 Written nowhere as a rule: no sentence ties Checkout 3 to payment, cover or the fee. 2 No
  corpus nominates it: the one control on the fee path, the statement, reproduces the wrong basis. 3 No arithmetic
  symptom: every join, key and count ties on both sides of 21 September, and so does the statement. 4 Not a row
  predicate the battery runs: the switch shows only when pickup captures are tabulated by date across the logged
  window's end. 5 The solver's own step completes and is wrong: reconciled, carried, every cell out of its bin. 6 Its
  date is a launch outside the graded window, so an event study on any graded series finds nothing. 7 It survives
  deleting the thread line: the records still date and show the switch.
- **Determinacy.** The slot runs after Checkout 3 (the thread names it; the records date it and show its effect); terms
  2 covers pickups paid through checkout; so in the slot every pickup carries the fee. The rival prices the slot on a
  checkout that no longer exists, while itself re-pricing July and August at the September tariff, the rule in force,
  which is the principle the golden applies to the checkout.
- **Interior handling, stated as an exposure (law 5).** On the cover dimension the golden equals the credulous reading
  (charge every order). That reading stays wrong through F1, because the VAT is taken off only by reading Finance's
  statement, and a reader of the statement reconciles to it, which leads to the old checkout; and through HZ2.

**FX retired.** The capacity note's 1 March 2027 sentence is deleted. No cover change falls inside the slot, so there is
no blend, and the 2026 slot weeks are no longer levelled for one.

**HZ1 moved into the record.** The tariff register's KB-2027-01 row (EUR 0.95 plus 5 per cent) becomes a Finance
proposal entered on 22 September for 5 April 2027, with no committee decision in its decision column. The minutes of 6
October no longer carry it; they keep the Q3 review, listing promotions and bundle shipping and become a third
distractor (pricing committee business none of the asks needs). The tariff in force on every day of the slot is
KB-2026-02, read off the register's dates alone; the hazard is taking the register's newest row (plus 9 per cent on every
fee figure).

**The holdout sentence deleted.** "The 1 per cent long-term holdout on recommendations stays out of every test" admitted
an arm of 10 per cent of 99 per cent, a reading no loop asserted and one that moves totals across their hundreds. With
it gone the arm is 10 per cent of the table's sessions, as charter 6 states.

**P2 and HZ3 stay where they are, as hazards on the totals.** No silent device fits the traffic path (harden loop 1's
finding stands): moving the R2 line or the app gate into another document the solver opens changes nothing, and a
records-only app gate leaves charter 6's "for twelve weeks" as a counter-pin. The pair arithmetic has always counted the
six order totals as kept by both sheets.

### Gate G (unchanged)

decomposition_attribution, with method_or_model_selection at rungs 1 and 2 · surface_read_dependency: no ·
stumping_family: analytical_non_defect · sole_data_defect: no · deletion test passes · not a lens swap. No device or
document change in this loop touches a file or column the main call reads; the thread line names no figure and no
policy.

### Ask ledger (supersedes harden loop 2's; asks unchanged in wording)

Main call's declared row population: unchanged (render log, served rankings, the orders extract's order, buyer,
listing, time, channel and home session, the archive, charter, commitment, register, field reference). Zero device rows
in it: the checkout, prices, deliveries and payments live in columns and files the call never reads.

| Ask | Figures | Construction layer | Device layer | Use (H18) |
|---|---|---|---|---|
| 1 Grid | 48: change in buyer-protection fee income per 1,000 carousel sessions by policy and cell, EUR, one decimal | orders over the test by cell (rung 4) | **FC**; F1, F2, HZ2, HZ1 | what each option is worth in each cell beside the call |
| 2 Totals | 12: extra orders and extra fee income over the twelve weeks, nearest hundred | the lift over the test by cell on the planned cell traffic | fee half: FC, F1, F2, HZ2, HZ1; both halves: P2, HZ3 | what the quarter buys beside the call |

**Per-ask stops (asserted).** Ask 1: the 31 readings (FC's two states by the four hazards, less the golden) and the
natural read (every order priced on the formula, VAT in, the asking price, the register's newest row, in-session orders
only) carry every cell out of its bin by at least 0.02; the logged checkout alone moves every cell; VAT taken off order by
order files the golden grid (C1); the over-cleaners (fees as charged, every pickup dropped, every accepted offer, the
pre-September tariff, VAT off the gross) each move most cells; the in-session basis moves the velocity boost's four older
cells and nothing else. Ask 2: the order readings as in loop 2 (first release, all twelve weeks on the app, both, the
natural read, the pooled lift); 127 fee readings per policy (FC's two states by the four hazards by the four traffic
readings, less the golden), each at least 5 outside the golden hundred unless recorded as an either-side reading.

**Pair arithmetic (planning weights 38 / 7 / 55; 4 call, 4 file and 64 ask criteria at 0.86).**
- Cracker (lands E) on round 3's fee path, the reconciled basis carried into the slot: the call block, the files, the
  heatmap's four parts and the six order totals, no fee cell and no fee total (asserted). **53.6.**
- Mirror (files C on the logger count), the same fee path: three call criteria, the files, the euro scale, the six order
  totals. **16.0.**
- **Pair 34.8**, under 40.
- **Exposure, stated.** A response that finds Checkout 3 keeps 48 cells and six fee totals (plus 46.4): with a cracker
  that misses it, 58.0; as one of two mirrors, 39.2; both, 62.4. Because the bar averages the top two of about twelve
  responses, a device found by one response in ten already puts two finders in the top two about a third of the time,
  so FC is built to be found by almost none: no document on the ask path, no control that confirms it, one named
  launch on the social layer.

### Fork grid: the axes this loop changed (harden loop 1's table stands for the rest)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 22 | Forward window contents (cover) | the checkout in force when the slot runs, Checkout 3: every order paid at checkout | records (no pickup paid at the handover from 21 September) with the thread's Checkout 3 and terms 2; C4: the logged checkout moves every cell |
| 3 | Attribution window (fee cover) | one checkout for the whole slot | C1: no blend; every order in the slot on Checkout 3 |
| 5 | Version basis (tariff) | the register row in force on the slot's dates, KB-2026-02 | C1: KB-2027-01 is dated after the slot, so every reading by date returns KB-2026-02; the newest row is the hazard |
| 6 | Divisor (traffic) | 10 per cent of the table's sessions in each cell | charter 6; the holdout sentence deleted |
| + | Fee cover in the logged window | pickups paid at the handover uncharged until 20 September | terms 2; the referee ties only under it |

### Realism debts added

- Checkout 3 is described nowhere in the folder beyond one passing mention and its trace in the records; the folder is a
  slot review folder assembled for the planning meeting, not a product changelog, and the minutes record pricing
  decisions, not launches.
- The logger window closed the day before a checkout change; no document links the two.
- Pickups are never paid from a Vouwlijn balance, so every pickup from 21 September carries a provider capture.

### Stopping rule

Loop 3 of 3 on this architecture, the last before a re-root. Round 1 is re-run on this build. A landed call, or a proxy
at or over 40 with the call missed (a response that finds Checkout 3, or a fee path no loop has seen), sends the build to
stage 1 with this architecture moved into the card's lineage.

## Tried and rejected

- First draft (v1, drafted 2026-10-08, never registered): every proposal failed a different launch condition and the test-calendar
  library-fill clause widened the choice to the registered library, where only E cleared all three. Died at checkpoint A because the
  decisive step was a written rule a strong solver follows once no proposal qualifies (measured trap #9 alone scored 0.58 in its
  nearest exemplar, so the stump leaned on lower rungs firing first, and the nearest dead shape is argmax under a stated rule over a
  filed candidate list, task36), and because its honest Gate G, binding_constraint, collided on (objective, G11, binding_constraint)
  with task106 and 13 older builds and passed only after the card relabelled it method_or_model_selection.
- Redraw candidate, 2026-10-09, the leader outside the logger's reach: B's pinned listings fall outside the logger's per-session
  candidate pool on most new-buyer sessions, so its new-buyer guardrails are not identified and B cannot be certified (#13, G15,
  guard PASS). Dropped before registration: it fails Gate G's instrument repair (a logger able to draw B's rankings observes the
  decision's quantity directly and the task collapses, the 89 v6 dead shape), and it carries an arithmetic symptom, B's
  self-normalising weight sum at a fraction of the session count, visible to any solver who prints the normaliser or the
  unnormalised estimate beside the normalised one.
- Other decisive moves screened at the redraw and rejected on paper: carrying a correct pooled lift onto the Q1 traffic mix (the
  transport driver of task43 iteration A, task44 v2 and task83); habituation measured from each buyer's prior exposure count (task83's
  conditioning on each unit's own treatment history); shared unique listings depleted across buyers (task106's shared-pool driver);
  the Q1 control being a retrained incumbent (a dated release-calendar line that asks the question for the solver); and a test-power
  or clustering argument (G2 is banned against task120 and G17 is supporting only).
- Design stage, 2026-10-09, grading the draw's 48 guardrail cells as the shape's grid: rejected on the pair
  arithmetic. The guardrail read is on the main call's path and on the kept basis only B's row moves out of its
  bins, so the response that lands E keeps all 48 and the best response that stops at B keeps about 40; the pair
  sits above 50 on paper. The grid became each policy's fee income by cell, and the guardrail moved to hatching.
- Design stage, 90 per cent lower bounds as graded figures and as the lift condition: rejected. A delta-method bound
  and a bootstrap bound differ in the first decimal, and B's kept bound sat at +0.4 against a zero bar, a knife
  edge on the runner-up. All three conditions became point rules with stated margins.
- Design stage, a fee charged once per checkout and repeated on every order line (D6) as the grid's primary:
  rejected. Splitting a bundle's fixed fee between the carousel order and the other items in the same checkout is an
  allocation fork on every bundled cell.
- Design stage, refunds on cancelled orders as a fee-path device: rejected. Cancellations visible on the ask path
  invite taking cancelled orders out of the main call's lift, a fork on a graded figure.
- Design stage, the offers clock (UTC acceptance against local checkout at a 24-hour expiry) as a hazard: rejected on
  magnitude, about 0.4 per cent on a cell, inside the one-decimal bin.
- Design stage, shipping each archived session's follow-up orders so the archive is blind by construction in the
  pack: rejected. The column names the other outcome and hands route 1 over; the archive ships in-session orders
  only and the blindness is asserted in the generator with the hidden follow-ups.
- Design stage, a first-time-seller ask on a prior-account chain (D7): dropped for this pack. Its construction layer
  is level (B's brought-forward orders rarely go to first-time sellers) and its two files take the pack past 24;
  kept in reserve as an ask device for a hardening loop.
- Design stage, the draw's four-rung sketch (A, C, B, E) carried as the ladder: below the pipeline's five-rung floor,
  because replay and per-render weights both named A, so the two refused estimators were one rung. Split by giving
  the logger's D allocation to the pickup cities (replay over the render rows names D) and A its gain in long
  sessions (render weights name A); every leader is still a different policy.
- Build stage, 2026-10-09, the design's render-weights figures for B (8.31 in-session, 7.70 kept): infeasible.
  With B's session-weighted borrowing at 4.73, the render-weighted borrowing cannot fall below 4.73 x 150,400 /
  404,990 = 1.76 even with every borrowed order in a single-render session, so B's render-weighted kept could
  not exceed 6.55 and the render/eight-cells/kept grid cell would not name B by 1.15x over E. Repaired in the
  data rather than the ladder: B's added new-listing orders rise with session length in the new-buyer cells, so
  B's render-weighted in-session figure is about 9.0 and its render-weighted kept about 7.0 (1.20x over E), and
  A's render-weighted figure rises to about 11.0 to keep rung 1's margin at 1.22x over B.
- Build stage, 2026-10-09, the design's 90 per cent bound check (a bound above zero passes B, D and E and fails F):
  dropped. On the kept basis every policy's per-session outcome includes three weeks of orders, so a delta-method
  bound straddles zero for every policy and the sentence would be false; the charter's conditions are point rules
  and the charter says so, which is the closure, and no assertion claims a variance result.
- Build stage, 2026-10-09, organic watched-listing exposure for the five rankers that do not read saves (the design's
  "plus 0.03 of organic watched exposure" and borrowed 0.06 to 0.30 for A, C, D, E, F): dropped. Route 1 and route 2
  agree to the order and to the cent only if each (cell, ranker) group's in-session watched purchases are a
  multiple of eight with five in eight bought anyway; at an organic purchase rate of 0.1 to 2.3 per 1,000 a group
  of 400 to 3,000 sessions can only hold 0 or 8, so one octet put 3 borrowed orders per 1,000 into a single cell
  (F, web 30-179) and erased F's young-to-old spread that the restatement device needs. Now only the velocity
  boost's build shows a buyer's watched listings (every other ranker, archived ones included, draws from a pool
  that leaves them out, which is also why no archived test could see the borrowing); the other five policies' kept
  and in-session figures are equal, and the decomposition applied to B alone files E at 5.7, a cracker.

- Build stage, 2026-10-09, the design's assertion 13 as written (any segment's anyway rate, applied to every
  session, files the same kept figures): infeasible. B's kept lift moves about 7.5 per 1,000 per unit of the rate, so
  a segment 0.008 off the pooled 62.5 per cent (four-render sessions, 63.3) nets B to 3.25, across its bin edge, and
  no position of B inside its bin survives a spread of 0.01 either way. Replaced by the readings a solver actually
  runs: every segmentation netted stratum by stratum (cell, ranker, cell by ranker, platform, tenure band, renders,
  watch-list size, weekday, ISO week, half) and each natural sub-population's rate (incumbent arm, velocity arm,
  each platform, each half, one-render and up-to-two-render sessions) applied to every session, all filing E 5.7
  and B 3.3; the most extreme single segment applied everywhere is recorded as the thinnest boundary, not asserted.
- Build stage, 2026-10-09, the two halves of the logged window stratified on in-session outcomes only: each
  policy's kept lift differed between the halves by up to 12 per 1,000 (B 9.4 against -2.8), because three weeks of
  background orders per session fell at random between the halves, which hands a solver who checks stability a
  reason to distrust route 1. Equal half sums of in-session and 21-day orders per (cell, ranker) then still left C
  and D 0.4 to 0.5 apart on the kept basis, because a group with an odd session count puts one more session in one
  half and a kept base of about 1.8 orders a session moves that half's mean. Now each group's halves hold the same
  mean of both counts to within one order, the odd orders and sessions placed by a search that matches each
  ranker's half gap to the incumbent's; every policy's halves agree within 0.09 on either basis.
- Build stage, 2026-10-09, placing the fee cells by whole-euro price moves on plain orders alone: could not carry
  the price-paid device out of the bin where the arm's accepted-offer discount per session matched the
  incumbent's (shifts of -0.008 to 0.034 in five cells), and in two cells the January row and the asking price
  cancelled. Replaced by three levers on the cell's own in-session orders, searched together: a plain order's price
  moves the figure and every reading alike, the asking price of an order bought on an accepted offer moves only the
  asking-price readings, and the price of an order paid in person moves only the readings that charge it; every
  one of the seven device combinations and the natural read now clears all 48 cells, the two under EUR 1.00 included.
- Build stage, 2026-10-09, the slot-total placement as first written scored distance from the round hundred, which
  pushed the totals toward the bin edges (A's orders sat 14 from one). Now scored on distance to the edges, 20 to
  45, with every wrong reading of every total at least 5 outside its hundred.
- Build stage, 2026-10-09, the pooled-lift stop on ask 2 (one pooled kept lift times the planned total) against a
  planned Q1 cell mix that matched the logged summer mix: it filed the same hundred as the cell-by-cell total for
  B, C, E and F (4 to 23 orders apart). The weekly table now carries a January new-buyer surge in both years (the
  0-29 band peaks 8 points above its base share in early January, the 30-179 band 4 points), which puts the pooled
  and cell-by-cell totals at least 138 orders apart for every policy before placement.
- Solver round 1 (plain, 2026-10-09), the five-rung build as shipped: LANDED, proxy 89.8, asks 6 of 8. The solver walked every
  rung without friction and executed the decisive one at its step 6 as a work order: "Lift outcome: all orders by the buyer (any
  channel) within 7 days of session start, from orders_enrolled_buyers. The result is identical at 14 days. HC-33 pins watch-list
  listings in tiles 1-2, which cannibalises favourites/alerts orders in the 180+ tenure cells, so its net log-mix lift is 3.30
  against a gross carousel lift of 7.96." The charter's lift definition (orders during the test, every channel) plus a shipped
  all-channel order file keyed by buyer makes the any-channel window the default outcome, so the netting is never a construction.
  It also kept every ask figure (48 fee cells, 12 totals), and it weighted the headline to 5.8 on the slot mix against the
  golden's 5.7 on the logged mix while using the slot mix for the totals, a determinism finding on the headline basis.
- Harden loop 1, diagnosis of round 1 (the borrowed-order netting as the decisive rung; P1 in-person pickups, P2 the R2
  restatement, HZ1 the deferred tariff, HZ2 the price paid and HZ3 the app gating as the ask devices): the decisive quantity
  was the charter's own observable, so the solver never had to think of borrowing at all. Its "Lift outcome: all orders by
  the buyer (any channel) within 7 days of session start, from orders_enrolled_buyers. The result is identical at 14 days"
  is charter 2.2 executed on the one extract that already holds every order by buyer, and the netting of B fell out of it as
  a by-product ("which cannibalises favourites/alerts orders in the 180+ tenure cells"). Every ask device died the same way:
  each organ sits in a file the ask's own path opens with its rule beside it ("recomputed at the 1 Sep 2026 tariff ...
  because KB-2027-01 was deferred", "Pickup orders paid directly carry no fee", "R2 restatement 2026-W01..W12 (it matches the
  account-service tenure), app only from W03 because of the release 27.1 gate"). Dead: a decisive rung whose correct basis
  is the definition's own observable on a shipped extract, and an ask device whose rule is filed in a document the ask path
  reads anyway. What the trace holds fixed without checking is that the logger's in-session columns measure the charter's
  quantities whenever the charter is not about orders over the test (its guardrail is read "from ordered_tiles"), which is
  where loop 1 goes. Harden loop 1 of 3 on this architecture.
- Harden loop 1, the come-back orders credited to the session the tile was in (home_session_id = the logged session): the
  habitual tie between ordered_tiles and the carousel orders credited to each session then failed in 202 sessions, every one
  outside C, an arithmetic symptom on the wrong path that points straight at the device. Now each come-back is credited to
  the session it was placed in, the tie holds in all 150,400 sessions, and the field reference's seven-day rule lets the
  listing alone attribute the order to its tile.
- Harden loop 1, no come-back orders at all under C: one zero in a by-arm count reads as a marker; C now comes back at 0.15
  of the others' rate (3 orders, none in app 0-29).
- Harden loop 1, charter 2.4 as written ("its orders placed from a home carousel tile"): it also admits every carousel order
  by the arm's buyers in a window, a reading under which C passes and is filed; 2.4 now counts the orders placed from the
  carousel tiles the arm served.
- Harden loop 1, the January new-buyer surge at 8 and 4 points (built for the pooled stop on ask 2): it put the slot-mix
  headline at 5.8 against the logged window's 5.7, round 1's determinism finding. Cut to 2 and 1 points, the headline
  converges (5.716 against 5.697) and the pooled totals fall 14 to 41 orders from the cell-by-cell ones for B and E, which
  no placement can carry out of the hundred, so the pooled stop is retired: pooled readings are placed at least 5 from the
  edges on either side and recorded.
- Harden loop 1, every fee reading as a stop on ask 2: B with only P1 mishandled and F on the first release alone sit 25
  and 14 euros from their golden totals, under the 25 a stop needs with the golden 20 from its edges; both are carried as
  either-side readings at least 5 from the edges (both inside) and the placement reached 6.4 of slack.
- Harden loop 1, fee cells placed anywhere from 0.35 to 0.65 of the bin: 7 of 48 landed within 0.003 of the round
  one-decimal value (7.0001, -14.5997 and so on), a receipt; the window now leaves out the middle tenth.
- Harden loop 1, a fresh silent device for the order totals (the logger slice held out of slot arms, a weekly table
  counting home sessions rather than carousel sessions, Easter falling in the slot's last week, staff and monitor
  accounts in the weekly table): each needs a new organ on the traffic path or a rate the pack cannot pin, or reads as
  sabotage; the order half keeps P2 and HZ3 and the pair arithmetic counts it as leaking to both sheets.
- Harden loop 1 as built, graded in the re-run of round 1 (labelled "round 2, plain", 48.7, call missed, 3 of 8 items):
  the tile count held the call (the solver filed C at 9.8 with E as runner-up, its step "Guardrail on the in-session
  carousel order rate: the only breach is HC-31 in web 730+" never sees rung 3), but the ask layer leaked exactly as the
  stated exposure said: "This reconciles exactly to the Finance Q3 sheet (the 6,147 July shipped orders missing from
  payments supply EUR 8,205.17)". Reading the referee settled F1 (VAT out) and F2 (balance purchases charged), so all 48
  fee cells and all twelve totals landed. A referee that ties to the cent only under the golden fee basis is a recipe
  the solver reconciles to, not a silent organ; the fee devices cannot rest on the referee going unread.
- Harden loop 2, diagnosis of round 2 (loop 1's ask layer: F1 fee income net of VAT and F2 balance purchases charged as the
  silent primaries, P1, HZ1 and HZ2 stacked on every fee figure, P2 and HZ3 on the totals, and Finance's Q3 statement as the one
  referee, tying to the cent only under the golden fee basis): the tile count held the call, and every fee figure fell to one
  reconciliation, in the solver's words at its step 7, "Fee income is taken excl. 21% VAT. This reconciles exactly to the Finance
  Q3 sheet (the 6,147 July shipped orders missing from payments supply EUR 8,205.17)". A statement scoped to the extract's own
  buyers that ties to the cent under exactly one fee basis arbitrates all five fee devices at once and hands over the level,
  which is the oracle law 8 bans, not a referee; every device it did not settle was a filed rule the path reads ("KB-2027-01 was
  deferred by the 6 Oct pricing committee", "uncaptured pickups were paid directly and carry no fee", "app uses W03 to W12
  because the first app release on or after 4 Jan 2027 is 27.1"). Dead: a fee device whose correct handling is also the only
  basis on which the logged window's statement ties. Harden loop 2 of 3.
- Harden loop 2 build, the in-person price lever as single-euro moves within plus or minus 30: it moves only the full-cover
  half of a cell, and F app 730+ (23 in-person orders) could then clear its bin by no more than 0.0035; the lever now moves
  up to 3 euros an order over plus or minus 60 units, applied round robin across the cell's orders.
- Harden loop 2 build, traffic readings within 30 of a hundred's edge treated as stops: B's fee total with only the cover
  change mishandled sits 6.3 inside its hundred and no set of traffic factors carried every stop out (the placement score
  stayed negative); the near band is 40 and the readings in it are either-side readings, B's FX-alone total among them
  (recorded as kept by round 2's path).
- Harden loop 2 build, every fee reading at least 0.03 outside its bin: D app 0-29 with only the January row applied can
  sit no further than 0.0246 outside, because the two tariffs differ too little on that cell's orders for the price
  levers to widen it; the floor is 0.02.
- Harden loop 2 build, VAT taken off order by order converging without a lever: on an early placement one B web cell's
  per-order rounding fell 0.0031 outside the golden bin; a pair lever (plus and minus one euro on two plain orders, which
  moves only the per-order rounding) was added, and on the final placement it needed no pairs (0.0227 inside at the
  nearest).
- Harden loop 2 as built, graded in the re-run of round 1 (labelled "round 3, plain", token proxy 51.1, call missed, 4 of 8
  items by token; read-corrected about 23 to 31, because notebook items 1 and 2 and image items 2 to 4 were credited on HC-37,
  5.7, HC-33 and HC-34 named in the solver's screen-out and negation sentences): the tile count held the call for the second
  round running (C filed at 9.8, E runner-up at a gap of 4.1, at the same step, "Condition (b), each cell's carousel order rate
  against HC-24: HC-31 web 730+ is -2.74% and fails. All other policies' cells are within -1.5% (HC-34 app 0-29 -0.96%)"), but
  loop 2's ask layer leaked whole again: all 48 fee cells and all six policies' twelve-week totals landed, at its step 8, "covered
  orders are shipped orders plus pickup orders captured by card or iDEAL, which reproduces Finance's protected orders and fee
  excl. VAT exactly ... Tariff for 2027 stays 0.80 + 5%, because the pricing committee minutes of 6 Oct defer KB-2027-01", and at
  step 9 it read P2, HZ3 and the 1 March cover change straight off the filed notes. Dead: a fee basis that still ties Finance's
  Q3 statement to the cent (the referee survived loop 2 as an oracle under a new cover rule) and traffic and tariff devices whose
  rule sits in a document the ask path opens. Harden loop 3 of 3 on this architecture is the last before a re-root.
- Harden loop 3, diagnosis of round 3 (loop 2's ask layer: FX, the 1 March 2027 checkout change in the capacity note's
  overlaps section, as the fresh primary on all 48 cells and the six fee totals; F1 VAT, F2 balance purchases, HZ1 the
  deferred January row and HZ2 the price paid stacked on every fee figure; P2 the R2 restatement and HZ3 the app release
  gate on the totals; Finance's Q3 statement as the one referee, still tying to the cent on the logged window's cover): the
  call held at the tile count, and the whole ask layer fell to two habits the solver runs by default. It reconciled its fee
  model to the referee, which still ties the logged window under the golden's own per-purchase basis and so settles VAT,
  balance purchases and in-person pickups in one pass, in its words at step 8, "covered orders are shipped orders plus
  pickup orders captured by card or iDEAL, which reproduces Finance's protected orders and fee excl. VAT exactly ... Tariff
  for 2027 stays 0.80 + 5%, because the pricing committee minutes of 6 Oct defer KB-2027-01 even though the tariff register
  lists it"; and it executed every rule filed on the traffic path as a work order, at step 9, "The app arm starts 18 Jan
  2027 (release 27.1 after the code freeze), so app runs W03-W12 and web W01-W12 ... From 1 Mar 2027 (W09-W12) every
  pickup order is paid at checkout and carries the fee", so FX, built to sit off the fee path, was read in the same pass as
  HZ3 because both sit in the capacity note. Dead: a referee whose figure the golden's fee basis reproduces on the logged
  window (whatever changes for the slot, the statement hands over every logged-window device at once), and any device whose
  rule is a dated, named sentence in a document the ask path opens (the minutes, the release log, the capacity note), because
  the solver reads every note on its path and carries out what it says. Harden loop 3 of 3.
