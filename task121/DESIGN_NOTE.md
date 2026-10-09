# task121: the checkout address check that heals itself, realising analytical_tasks note RC01

Source note: `analytical_tasks/06_root_cause/RC01_checkout-release-forward-cost-self-healing.md` (RC01). This build is its first realisation and keeps its decision, mechanism and world except where the changes below say otherwise.

```
DRAW  (independent draws, checked with ../fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? pending batch registration   Verdict: WARN
  Shape: 09 funnel or chain of stages   Gate G mechanism: decomposition_attribution (confirm_surface_read support)
  Gap: time (decisive), then population   Pattern: E (decisive), then A, then C
  Domain: Product Analytics   Subdomain (enumerated): onboarding-activation (the checkout funnel)   Objective: Root-Cause Analysis
  Pairing repeated from last build? no (task116 is product-analytics x opportunity-sizing-decision; this pairing was last built at task84)
  Stakeholder role: head of product at an online licensed-merchandise store (product_manager)   Context-artifact type: operations_log (the release and feature-flag rollout log)
  Calibration form: closed_decision_corpus (the release review board's two closed release-impact reviews)   Decision type: quantity_figure
  Decisive mechanism: G14 conditioned yield, with G13 horizon mismatch and G2 grain behind it; G6 composition shift carries rung 1, G16 method selection rung 2
  Repeats from prior builds: none against the last three; (time, E, quantity_figure) repeats task37, task44 and task97, differentiated in one line each on the card

  Committed call (planned): the release's lost orders a week, averaged over the 13 weeks from Monday 5 October 2026, if the address check stays, in whole orders
  Niche: an online licensed-merchandise store in Portugal choosing whether the quarter's one engineering sprint rolls back a checkout address check or builds a partner-referral traffic filter, on the check's forward cost; the check rejects only saved addresses holding a four-digit CP4 postcode, and an account fails it once before re-saving a full CP7 address
  Forum: committee_or_panel (the release review board)   Forcing event: incident_or_complaint (the regression incident logged against the release)   Org family: retailer_or_ecommerce
  World: Portugal, EUR; customers across mainland Portugal and the islands; the vendor's address rules, the partner contract and the growth traffic plan are filed documents
  People (guard.py names --geo Portugal --seed 121): Júlia Machado, head of product (the requester); Duarte Cunha, checkout product lead and owner of the check;
    Luciana Castro, growth lead; Jaime Jesus, chair of the release review board; Lia Neto, partnerships manager; Noah Coelho, analytics engineer (event dictionary, flag log);
    Cristiano Soares, payments operations lead
  Deliverables: address_check_sprint_call.html (the call, the funnel chart, the stage table, for the review board)
                address_check_sprint_call.xlsx (the workings: stage by channel, the twelve flag cohorts, authorisations by card network, the forward cost build)
  Opening move: options-first (one sprint: roll back the address check, or build the referral filter)
  Shape arithmetic: six checkout stages (basket, checkout started, delivery address accepted, delivery method chosen, payment authorised, order placed):
    6 volumes in the four exposed weeks + 5 pass-through rates + 5 changes in pass-through against the four weeks before, in points
    + 5 orders lost at each stage traced through to the order = 21; + 4 decision figures (the committed weekly figure, accounts still holding
    a failing address when the quarter opens, the referral filter's forward weekly figure, the sprint it implies) + 5 named chart parts
    (stages in order, both periods, the address and payment stages labelled with the orders lost there, the call in the title) + 2 files = 32.
    A channel split of the five pass-through rates (partner referral against the rest) adds 5 if margin is needed. No ask is a denser split of the committed figure.
  Spine: checkout_sessions_2026q3.csv, one row per session that put an item in the basket (account, channel, flag cohort, furthest step), synthetic, 25,000 rows or more
  Decisive trap (measured): #13 validates on one population, applies to another
```

As-of date: 2026-10-05

**Similarity claim.** No prior build is the forward cost of a correctly diagnosed cause whose exposed pool repairs itself through the window: the once-per-unit family on file (task83, a save offer moves a reader once; task76, a household that declines is never engaged again) grades a static reclassification of a pool at one moment, and the three builds sharing the (time, E, quantity_figure) signature (task37, task44, task97) turn on a linked entity's standing status, a moderator measured over the right window and a place's cumulative history, none of which the effect itself extinguishes.

## Stump sentence

A competent solver nets out the partner-referral mix, measures the release's per-session effect from the staggered flag cohorts balanced on channel and account age (the construction that reproduces both prior releases' reviewed effects), and applies that pooled effect to the quarter's planned sessions, filing a weekly cost about a quarter too high, because it never follows sessions through accounts to their saved addresses, where only four-digit-postcode addresses fail and an account that fails once re-saves and never fails again, so the share of checkouts still exposed falls week by week.

## Decisive rung

**#13 Validates on one population, applies to another** (`_measured.md`): decided 3 of 64 tasks, 2 of them under 0.50, status established. The cohort-measured effect fits the four exposed weeks and both prior releases' eight follow-on weeks exactly, and is then applied to forward weeks whose exposed checkouts are a different population: first attempts by accounts still holding a CP4-only address, a share that falls every week. The corpus is blind for a computable reason (proven-in-production L1): in every corpus case the exposing property never changes, because neither prior release touched saved customer data.

Behind it, from the same catalogue: #18 joins only on the visible key (2 of 64, 1 under 0.50, emerging) carries the session to account to saved address chain, and #11 beats the headline trap, misses the quiet one (4 of 64, 2 under 0.50) is the shape of the ladder, since the solver that correctly beats the referral-mix story is the one that stops at rung 2.

**Draw checks (stumping Part 6.1 against proven-in-production.md).**

- Strategies (the skill's Part A, the file's Part 3): S8 conditioned yield ("an average of a switch is not a price", task83) over S4 (a forward window generated under a regime the closed window never reached). Both discriminators are buildable here: the switch is absolute (no account fails the check twice, every failing account re-saves within two days), and the L1 sentence above is writable.
- Dead shapes (the skill's Part C, the file's Part 4): nothing is drawn on the list as it stands, but three entries are live risks the design has to close. A rung that changes the model of behaviour (task75, seen by a rolling-origin back-test): the staggered cohorts let a solver run an event study by weeks since exposure and watch the effect fade, which is an arithmetic symptom (survival property 3) unless every aggregate decay fit lands far off (the note prices one at +31 per cent). A forward population named by a filed clause (task100 v1): the vendor's published address rules name the failing postcode format and send a solver to the address book, which strains survival property 1. A device announced by its own shipped columns (task48): no address-book column may name a re-save or a validation outcome.
- Objective (guide-to-prompt step 2): the product team already names the cause correctly and the committed figure is that cause's forward cost, a predicted value the address book pins down, which stumping Part 6.1 warns reads as Forecasting to a reviewer. The Root-Cause tag holds only if the prompt leaves the attribution open (the release against the partner-referral mix, with payments as a third suspect), so naming the mechanism and sizing the rival are graded work; shape 09 supports that reading (it carries Root-Cause when the answer is the stage that caused the fall). Not retagged; the author decides.

## Nearest exemplars

1. *Fix the approval-gated connection stall in three scoped parts* (SaaS Trial Activation, Product Analytics): measured mean **0.52** over four runs (0.49, 0.68, 0.48, 0.49). Nearest on decision and mechanism: a fall dated to a release, a like-for-like composition correction, the broken segment found through a join to another entity, and a quarter landing projected forward. The model found the cause and the composition and lost on the scoped remedy (37.3 against 42.2 per cent).
2. *Merge the copied prospecting campaigns on 1 July instead of reverting the Anvil bid change* (Paid User Acquisition, Product Analytics): measured mean **0.58** over four runs (0.71, 0.72, 0.55, 0.45). Nearest on the organ: an intervention's effect priced from the account's own change-log natural experiments, with a loud dated change as the decoy. The model rejected the dated lure in all four runs and lost on pricing the premium ($160 against $150).

Both sit above 0.50 because the model names the cause and loses only on sizing. RC01 puts its stump on the sizing, which is where both misses landed, and the cause-naming half of this family has to be treated as free.

## Guard

Verdict against the existing corpus: **WARN** (exit 0), card at `<scratchpad>/cards/task121.json`, not registered.

- First pass with the note's own labels (gap time, pattern A with C second, G13 decisive) was BLOCK on four rules: ban.pattern (A against task114); test.same_puzzle inside the window ((time, A, quantity_figure) against task107's v4-forecast lineage); test.same_puzzle_older (the same signature in nine earlier builds, task35, task46, task47, task57, task62, task77, task89 and task95 among them); test.same_driver_older ((time, A, decomposition_attribution) against task51's v1 to v3 lineage). Cleared by moving the decisive pattern to E (see Changes).
- Variants checked at the draw and not taken: population as the decisive gap collides inside the window with task107's v1 lineage on (population, E, decomposition_attribution); a pick_one_of_n decision clears every rule but turns the graded figure into a two-way pick.
- NOTE test.same_puzzle_older: (time, E, quantity_figure) repeats task37, task44 and task97, each differentiated on the card: task37 is a static coupling to a linked entity's status, task44 a moderator measured over the right window with membership moving both ways, task97 a recurrence rate that rises with a place's history; here the effect ends its own exposure and the pool only drains.
- WARN overuse.org_family (retailer_or_ecommerce in 16 builds): an online merchandise store is a retailer and no other family is honest; none of the last three builds is a retailer, and the furniture around it (a release review board, a regression incident) is fresh.
- Furniture: committee_or_panel, incident_or_complaint and retailer_or_ecommerce are each clear of task114 to task116; the honest alternative forum (the head of product's own call, line_manager_or_team) is banned against task116. People: no findings on the seven drawn names.
- Nearest drivers: task43 iteration A at 0.11 (under the 0.12 WARN line), task83 at 0.07.
- Batch preview, not binding: against the sibling pilot drafts in the scratch folder, if task117, task119 and task120 register first, this card BLOCKs on ban.pattern E, ban.artifact and test.same_puzzle against task117 (the same (time, E, quantity_figure) signature) and on ban.forum against task119 and task120. A variant tested in that order clears them: C first (the note's own join label, the rollback's recoverable share), monitoring_export, line_manager_or_team, plus one differentiation line against task98's v2 lineage. In the current corpus order those three choices are each banned by task116.

## Changes from the source note

1. **Decisive pattern A to E, with A and C kept behind it; decisive generator G14 with G13 second.** Forced by the guard (ban.pattern against task114, and the (time, A, quantity_figure) signature spent nine times, once inside the window). No rung moves: the decisive rung is framed as conditioning the cohort-measured per-checkout effect on the account's address state at the checkout (a CP4-only saved address not yet failed), an absolute split behind a two-hop join, applied to a forward mix that drains. It is a relabel of the same rung, so the author may veto it (see the guard section for what restoring A costs).
2. **Calibration form mapped to closed_decision_corpus.** The note's "change-log natural experiments" has no vocabulary key; the organ certifies a measurement method on closed reviews rather than piloting the decision's own intervention, so pilot_log (task116's form) is the weaker fit.
3. **World fixed where the note left it open.** Portugal, EUR; the "legacy-format saved address" becomes a CP4-only postcode (the four-digit code without its three-digit extension), which the vendor's address rules reject. The 13-week window from 5 October 2026 takes in the Black Friday and Christmas weeks, so the growth traffic plan that pins forward sessions carries a peak.
4. **Shape 09 and two deliverables instead of three.** The note's `regression_case.xlsx`, `forward_cost.png` and `sprint_decision.pdf` become `address_check_sprint_call.html` (call, funnel chart, stage table) and `address_check_sprint_call.xlsx` (workings). The note's chart asked for the forward cost "under the constant and draining bases", and its ask C asked for the forward cost under each of the four rung bases; both name the ladder in the prompt and are dropped. A per-forward-week split of the committed figure would be an inheriting ask, which supplemental-stumping does not build. Asks A (the twelve cohorts, with the bot-session device) and B (authorisations by card network, with the retry device) survive as funnel-stage asks on the session and payment stages.
5. **Furniture added** (the note names none): the forum is the note's own platform review board, renamed the release review board, which holds the licensed wrong basis (regressions sized as the measured weekly loss carried forward); the forcing event is the regression incident logged against the release; seven personas drawn.
6. **Realism debt to settle at design:** rolling back a flag-gated release is normally a flag flip, so the world needs a reason the rollback costs a sprint (for example the flag retired at full rollout and the vendor call wired into the carrier booking step).

## Tried and rejected
