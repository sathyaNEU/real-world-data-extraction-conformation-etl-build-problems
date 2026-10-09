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

Shallower stops, each a different name: replay or one weight per render with the guardrail read on the platform split files A; the
session-weighted estimator with the same coarse guardrail files C; the eight cells and the floor file B, which is the stump.

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
