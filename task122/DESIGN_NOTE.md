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

A competent solver scores all six registered policies with the session-weighted estimator that alone reproduces the nine archived
carousel tests, reads every guardrail at the charter's eight platform-by-tenure cells, checks the fresh-listing floor and commits the
Q1 2027 slot to B, the velocity-boost policy, as the largest lift that clears all three conditions; the step that lands it there is
taking the render log's in-session orders as the policy's effect, when most of B's in-session orders are listings already on the
buyer's watch list that the buyer buys within days anyway, so over the twelve-week test B keeps a fraction of its lift and E, fourth
on the natural estimate, is the largest lift that clears every condition.

Shallower stops, each a different name (five rungs, set at the design stage): replay over the render rows files D; one
propensity weight per render row files A; the session-weighted estimator with the guardrail read on the platform split
files C; the eight cells and the floor file B, which is the stump.

## Decisive rung

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
| 4 | `carousel_test_archive.xlsx` | calibration: tests sheet and logged-sessions sheet (99,000 rows) | main |
| 5 | `experimentation_charter_home_surfaces_v4.pdf` | governing: conditions, lift definition, clause, cell table | main |
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
| 17 | `test_capacity_and_release_gating.md` | organ, HZ3; cell-by-cell planning line; same weeks last year | ask |
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
