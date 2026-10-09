# task122: which registered policy takes the home carousel's Q1 2027 test slot (realises analytical_tasks note DS01)

Source note: `analytical_tasks/05_decision_support/DS01_carousel-slot-library-fill-off-slate.md` (DS01). This build is its first
realisation. The decision, the ladder and the world are the note's except where `## Changes from the source note` says otherwise.

## Draw

```
DRAW  (independent draws, checked with ../fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? pending batch registration   Verdict: WARN
  Shape: 10, scorecard against thresholds   Gate G mechanism: binding_constraint with method_or_model_selection
         (the card declares method_or_model_selection, see Guard)
  Gap: objective (decisive), then rule, then population   Pattern: none at the decisive rung (G11), B for the estimator the archive pins
  Domain: Product Analytics   Subdomain (enumerated): experimentation-measurement   Objective: Experiment & Causal Analysis
  Pairing repeated from last build? no (task116 is product-analytics x opportunity-sizing-decision, the note's own tag)
  Stakeholder role: experimentation lead who runs the home page test calendar (product_manager)
  Context-artifact type: register (the policy registry the calendar owner fills slots from)
  Calibration form: closed_decision_corpus (nine archived carousel tests under a reproduction clause)
  Decision type: pick_one_of_n
  Decisive mechanism: measured trap #9, the one admissible policy sits off the slate (G11), behind the eight-cell
         guardrail (#14, G2) and the archive-pinned per-session estimator (#1, Pattern B, G16)
  Repeats from prior builds: none on a banned axis after the redraws; the structural signature (objective, G11,
         pick_one_of_n) repeats task37's retired wage-class ask and task50 v4, differentiated on the card
As-of date: 2026-10-28
```

Draw details, provisional until the design stage:

- **World.** Vouwlijn (invented), a Dutch online marketplace for third-party sellers' clothing and footwear, EUR. The call is
  made on 2026-10-28 for the slot that runs 4 January to 28 March 2027. Logged carousel sessions run 22 June to 20 September
  2026 (13 weeks); the extract is dated 11 October 2026, 21 days after the last session and 7 days after cart-source
  attribution closes on it, so no order is censored.
- **People** (`guard.py names --geo Netherlands --seed 122`). Saar Dries, experimentation lead and the requester. Tygo Knoers,
  personalisation lead, who holds that the two-tower model has earned the slot (the one belief the prompt may carry). Livia
  Verhaar, merchandising lead (the fresh-listing floor is a promise to sellers, not a ranking signal). Fabian Stoffel,
  data-science manager (replay is what the council has always been shown). Kayleigh Zeemans, lead of the trending-boost team.
  Amélie Middelkoop, chair of the growth council.
- **Furniture.** Forum committee_or_panel: the growth council reviews slot decisions, and its replay-among-the-proposals table is
  the licensed wrong basis. Forcing event launch_or_rollout: the Q1 2027 carousel test. Organisation family
  retailer_or_ecommerce.
- **Candidates.** Proposals A (two-tower personaliser), B (trending-boost ranker), C (session-sequence model). Library D, E (sequence
  ranker with a fresh-listing interleave), F, each filed as a scoring spec. Answer E.
- **Spine (planned).** `home_carousel_render_log_2026-06-22_2026-09-20.csv`, about 400,000 rows, one carousel render inside a
  logged session with the ranking the logger drew for that session and its propensity; synthetic.
- **Deliverables (provisional).** `carousel_slot_q1_2027.xlsx`: the test-calendar entry on its first sheet, every registered
  policy against the three launch conditions, the cell sheet, the estimator sheet and the device-carried ask sheets.
  `carousel_slot_q1_2027.png`: three panels, one per condition, the six registered policies as bars in two colours (proposals,
  library), each threshold as a labelled line at its value, the chosen policy annotated, the call in the title. Opening move
  question-first, provisional.
- **Shape arithmetic (shape 10).** 6 registered policies x 3 launch conditions = 18 threshold checks, plus the chosen policy's 8
  audience cells, the call with its lift to one decimal and its 90% lower bound (3), the condition each proposal fails (3), the
  archive hit count under each of the three estimators (3), 5 named chart parts and 2 files: 42 before the device-carried asks,
  which on the note's ask layer (checkout figures per cell, seller counts per category) add about 28 more.

**Similarity claim.** No prior build is a decision in which every candidate offered fails a different filed condition and the
answer is an earlier registered option off the offered list: no card on file carries measured trap #9's architecture, and the
nearest driver on file scores 0.06.

## Stump sentence

A competent solver who reads the guardrail at the charter's eight platform-by-tenure cells and adopts the one-weight-per-session
estimator that alone reproduces the nine archived tests finds that no proposal clears all three launch conditions and files the
session-sequence model (C), the largest reproduced lift on the slate, with its fresh-listing shortfall carried as a risk; the step
that lands it there is treating the three proposals as the whole choice set and never applying the test-calendar procedure, under
which an unqualified slot is filled from the policy library on the same conditions and only the fresh-listing interleave ranker
(E) clears all three.

Shallower stops, each a different name: the coarse new-versus-returning guardrail with replay files A; the eight cells with replay or
request-grain weights file B; a solver who opens the library but takes each entry's filed registration estimate files F, whose lift
on the current logs is negative.

## Decisive rung

**Measured trap #9, "Picks from the offered options when none passes": decided 4 of the client's 64 accepted tasks, 3 of them under
0.50 (established).** It sits behind #14, "Coarsens the segment it was asked about" (3 of 64, 1 under 0.50), at rung 1 and #1,
"Reports a failed back-test, ships anyway" (11 of 64, 9 under 0.50), at rung 2, with #10, "Notes a binding limit as a risk" (4 of
64, 3 under 0.50), as the stopping behaviour after rung 2. The nearest #9 exemplar alone measured 0.58, above the bar, which is why
the slate here empties only after two earlier corrections.

Gate G as the note argues it: surface_read_dependency no, stumping_family analytical_non_defect, sole_data_defect no. The one stale
field (the library's registration estimates) feeds no rung, and the library fill survives the instrument repair.

Checks `stumping` Part 6.1 asks of `proven-in-production.md`:

- **Dead shapes (its Part 4).** The lift is an estimator's output that the archive pins, not a filed formula. The launch
  conditions are quantities (a lower bound, a worst-cell change, a share), not status words. The nearest dead shape is
  "argmax under a stated rule over a filed candidate list" (task36): the defence is that the list the rule runs over is not the
  slate the prompt names, and every condition's value is a construction (the cells from the charter, the session weight from the
  archive, the library's rankings generated from its specs). The library-fill clause is filed on purpose, because a scope rule
  cannot be pinned by a corpus; its precondition, an empty slate, is reachable only through rungs 1 and 2.
- **Discriminators (its Parts 1 to 3).** S3 (a rule only a closed corpus settles) carries rung 2, and its known death, a menu the
  corpus scores end to end, is accepted because L1 wants the corpus to certify that shallow rung. The L1 sentence is writable: in
  every archived cycle at least one proposal cleared all three conditions, because the library-fill clause has never been
  exercised, so the archive holds nine proposal fills and no library fill. The twin pair (T3 and T7, identical on every archive
  column, realised +2.4 and +1.1, separated only by renders per session) is buildable in synthetic logs. L3 holds: the partial
  correction lands on F, further from the answer than C.

## Nearest exemplars

1. *Set the Flow Standard included allowance at 13,000 billable runs, the only allowance that meets all three conditions*
   (Product Analytics, usage-based pricing): **measured mean 0.58**. The same off-slate
   architecture: every slate candidate fails one of three conditions and the answer is found off the slate. Its model failure
   was the least-bad slate candidate, which is C's role here.
2. *Set the 2027 Team plan transcription allowance at 500 minutes per seat per month* (Product Analytics, SaaS usage allowance
   pricing): **measured mean 0.20**. A reproduction-gated series whose unit the standard defines and
   no file stores, which is the architecture DS01 puts at rung 2.

## Guard

`guard.py check` on the draft card (scratchpad `cards/task122.json`, not registered; the seven pilot cards register together in
draw order): **WARN, exit 0, no BLOCK.** Nearest driver similarity 0.06.

BLOCKs met and how they were cleared:

- **ban.pairing**, product-analytics x opportunity-sizing-decision against task116: the objective moved to Experiment & Causal
  Analysis, which is the honest tag anyway (Changes, item 1).
- **test.same_driver**, (objective, G11, binding_constraint) against task106 inside the batch, and **test.same_driver_older**, the
  same signature in 13 older builds: the card declares the note's own co-mechanism, method_or_model_selection, as its Gate G
  (Changes, item 2). The honest primary stays binding_constraint and the author can restore it with `register --force`.
- **test.same_puzzle_older**, (objective, G11, pick_one_of_n) against task37's retired wage-class ask and task50 v4: differentiated
  on the card in one line each. task37 removes a leader among four filed classes and task50 v4 demotes by exposure inside a funded
  window; here no offered candidate survives and the answer leaves the slate.
- Persona WARNs on the first draw: Faye (task27) and Rosa (task83) were swapped for Kayleigh and Amélie from the same seed-122 draw.

Bans avoided at the draw rather than met: calibration form pilot_log, context artifact monitoring_export (both against task116)
and shapes 07 and 01 (task115, task116).

WARN answered:

- **overuse.org_family** (retailer_or_ecommerce in 16 builds): the organisation is honestly an online marketplace, none of those
  builds turned on a ranking-experiment slot, and the nearest alternative family, software_or_platform, is banned against task116.

Batch note: DS17, DS33 and DS50 carry the same off-slate driver as DS01. If any of them is among the seven pilots, its card has to
be read against this one when the batch registers. The sibling drafts on 2026-10-08 (task117, task119, task120, task121) change
task122's recent three to task119, task120 and task121 at batch registration, and task116 drops out. A simulated check
(`FINGERPRINT_CARDS` pointed at a scratch copy of the corpus plus those four drafts) returns BLOCK on ban.forum
(committee_or_panel: task119, task120, task121), ban.calibration (closed_decision_corpus: task121), ban.role (product_manager:
task121) and ban.org_family (retailer_or_ecommerce: task121), with WARNs on repeat.gate_g (method_or_model_selection: task120) and
repeat.deliverables (png+xlsx: task120). Under that ordering the note's own pilot_log and monitoring_export become legal again,
and task106 leaves the twelve-build window, so a binding_constraint card would meet test.same_driver_older against task106 and 13
older builds (cleared only by fourteen differentiation lines, or by the method_or_model_selection key the card carries). Those
redraws belong to the batch step, because each of them is banned against the corpus as it stands today.

## Changes from the source note

1. **Objective: Opportunity Sizing & Decision Support to Experiment & Causal Analysis.** The note's committed figure, the chosen
   policy's expected offline lift in orders per 1,000 sessions, is not a sized opportunity built up from an addressable pool to
   what can be realised, so the note fails that objective's definition; and product-analytics x opportunity-sizing-decision
   repeats task116 (ban.pairing). The call rests on a causal claim estimated from logged data with known propensities and checked
   against archived A/B tests. No rung moves.
2. **Card Gate G: binding_constraint to method_or_model_selection.** Both are the note's own mechanisms; the guard blocks the
   first in this batch (task106) and finds it spent in 13 older builds. No rung, figure or file moves, and the design keeps both
   mechanisms.
3. **Calibration form keyed closed_decision_corpus.** The note calls the archive a published control set with a reproduction
   clause; its role is recovering the estimator, and pilot_log, which fits on form, is banned against task116. No design change.
4. **Context artifact: dashboard to policy registry.** The coarse new-versus-returning guardrail view moves from a dashboard export
   (monitoring_export, banned against task116) into the policy registry, the file the calendar owner fills slots from; rung 0 reads
   the coarse view there and no rung moves. Constraint for the design stage: the registry carries no figure that ranks the three
   proposals on replay, so rung 0 stays solver-built.
5. **Deliverables: three files to two.** `carousel_slot.xlsx`, `slot_conditions.png` and `slot_decision.pdf` become
   `carousel_slot_q1_2027.xlsx` and `carousel_slot_q1_2027.png`. A PDF, a chart and a workbook is the default the voice rule warns
   against, two files keep every shared figure to one agreement, and the committed sentence is a test-calendar entry, which sits
   on the workbook's first sheet.
6. **Shape 10 named.** The note's rubric arithmetic (about 60 criteria) is recast on shape 10, scorecard against thresholds; shape
   07, the grid that natively carries this objective, is banned against task115 and shape 01 against task116.
7. **World filled in where the note is silent.** The note names a fashion marketplace and three roles but no geography, no
   organisation name, no dates and no people by name. The fiction is a
   Dutch marketplace with invented names, guard-drawn personas and the dates above; none of the companies the note's Mirrors line
   lists appears anywhere in the build.

## Tried and rejected
