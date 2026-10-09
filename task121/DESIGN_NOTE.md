# task121: the signed-out customers behind a checkout conversion fall, realising analytical_tasks note RC01

Source note: `analytical_tasks/06_root_cause/RC01_checkout-release-forward-cost-self-healing.md` (RC01). This is the slot's second draw, made at checkpoint A after the author rejected the first draft (its architecture is in `## Tried and rejected` and in the card's lineage). It keeps the note's world and decision, an online store whose quarter has one engineering sprint and must choose what it fixes after a checkout conversion fall, turns the call into a pick of the fix with the attribution left open, demotes the note's self-healing exposure to a lower rung, and draws a new decisive move.

```
DRAW  (independent draws, checked with ../fingerprint/guard.py)
  Card filed: yes, registered 2026-10-09 after checkpoint A (go on the redraw) (the coordinator registers approved redraws in draw order)   Verdict: WARN
  Shape: 18 hypotheses versus evidence   Gate G mechanism: decomposition_attribution
  Gap: population (decisive), then time   Pattern: none of A to E carries the decisive rung (G3 decisive); A behind it for the demoted self-healing rung
  Domain: Product Analytics   Subdomain (enumerated): onboarding-activation (the checkout funnel)   Objective: Root-Cause Analysis
  Pairing repeated from last build? no (task123 is nonprofit-grant-making x etl; product-analytics x root-cause was last built at task84)
  Stakeholder role: head of product at an online licensed-merchandise store, who assigns the quarter's one engineering sprint (product_manager)
  Context-artifact type: monitoring_export (the weekly trading dashboard: conversion by week, traffic source and checkout step, correct, ranking no fix)
  Calibration form: prior_period_close_out (the close-outs of the store's two closed partner campaigns)   Decision type: pick_one_of_n (one of five shortlisted fixes)
  Decisive mechanism: G3 record versus operation (a session the log files as a new, signed-out visitor belongs to an existing account, settled through
    the members'-price token on the session, the club's monthly redemption report and the member number on a store loyalty profile); G6 composition
    shift carries rung 1, G13 and G14 carry the demoted self-healing rung
  Repeats from prior builds: none against the last three; (population, G3, decomposition_attribution) repeats task101 (older), differentiated in one line on the card

  Committed call (planned): the one fix of the five on the sprint shortlist that gets the quarter's engineering sprint, named with the cause it removes
  Niche: an online licensed-merchandise store in Portugal choosing which of five shortlisted checkout fixes gets the quarter's one engineering sprint
    after a September conversion fall, where the club app's low-converting shop-tab sessions are mostly existing customers whom the app's own browser
    lands signed out, so only the parked one-time-code sign-in reaches the largest loss
  Forum: line_manager_or_team (the head of product assigns the sprint to her own squads, no board)   Forcing event: incident_or_complaint (the
    conversion-fall incident, which the review closes by naming its cause and the fix)   Org family: retailer_or_ecommerce
  World: Portugal, EUR; a store selling licensed football, music and gaming merchandise, linked since 31 August from a top-flight club's members app
    (a Shop tab whose links carry a members'-price token); the address check enforces the carrier's full-postcode label rule from 1 September
  People (guard.py names --geo Portugal --seed 121): Júlia Machado, head of product (the requester); Duarte Cunha, checkout product lead and owner of the
    address check; Luciana Castro, growth lead; Lia Neto, club partnership manager; Cristiano Soares, payments lead; Jaime Jesus, CRM lead and owner of
    the parked one-time-code sign-in; Noah Coelho, analytics engineer (session export, event dictionary); Raquel Pires, fulfilment lead
  Shortlist (the five fixes, one sprint each): F1 inline postcode lookup at the address step (Duarte); F2 a club landing page that routes fans to
    in-stock kits (Lia); F3 the card SDK upgrade with the in-page 3-D Secure challenge (Cristiano); F4 one-time-code sign-in at checkout, which works
    in any browser (parked in spring by Jaime when password resets were flat); F5 split dispatch for baskets mixing pre-order and in-stock lines (Raquel)
  Deliverables: q4_sprint_call.html (the call, the hypotheses-against-evidence grid, the weekly chart, for the incident review)
                checkout_fall_workings.xlsx (the workings: lost orders by cause by week, each population's baseline, the device-carried asks)
  Opening move: options-first (five fixes, room for one)
  Shape arithmetic: five shortlisted fixes against four lines of evidence = 20 cells, each a computed figure with its verdict: (1) orders lost over
    the four review weeks among the sessions the fix's cause touches, against that population's own baseline; (2) the same for the latest complete
    week; (3) the affected-against-unaffected conversion gap in points; (4) when the losses began against the fall's start. Then 6 decision figures
    (the call, the cause it removes, its latest-week lost orders, the runner-up, the gap to it, and the check that the five populations partition the
    fall's total) + 5 named chart parts (weekly lost orders by cause over the eight weeks, one series per cause, the latest week marked, the call
    annotated, the call in the title) + 2 files = 33. Each decoy is killed by a different line, so all twenty cells have to be worked.
  Spine: basket_sessions_2026.csv, one row per storefront session that put an item in the basket (account when signed in, traffic source,
    members'-price token, new-visitor flag, furthest checkout step), synthetic, 25,000 rows or more
  Decisive trap (measured): #5 takes the population a flag or filter suggests, reached through #18 joins only on the visible key
```

As-of date: 2026-10-05 (the Monday after the fourth review week closes).

**Similarity claim.** No prior build turns a correctly reported shortfall that every closed case books as harmless dilution into the largest loss by re-attaching signed-out sessions to the established accounts a channel stripped of their stored state: the record-versus-operation builds on file re-attribute a component filed under another party's name (task101, the decision's own payments published under intermediaries' names; task82 v2, purchases under one-off keys credited to holders) or trace a conduct-coded delay to off-schedule work (task111 v1, lineage), and none of them changes which remedy is named by restoring the state the channel removed.

## Stump sentence

A competent solver gives the sprint to the card-authentication upgrade: it measures the address check on its flag cohorts and watches its losses drain as accounts re-save, books the club app's low-converting sessions as new-fan dilution because they carry no account and a new-visitor cookie and both closed partner close-outs book partner traffic that way, and is left with the rise in 3-D Secure challenges as the largest real loss, because it joins sessions to accounts on the account key alone and never follows each club-app session's members'-price token through the club's redemption report to a member number on a store loyalty profile, which shows most of those sessions are existing customers landing signed out, whose lost orders are the largest current loss and which only the one-time-code sign-in reaches.

## Decisive rung

**#5 Takes the population a flag or filter suggests** (`_measured.md`): decided 5 of 64 tasks, 3 of them under 0.50, status established. It is reached through **#18 Joins only on the visible key** (2 of 64, 1 under 0.50, emerging), and **#13 Validates on one population, applies to another** (3 of 64, 2 under 0.50) holds the corpus blind.

The session log files every club-app session as a new, signed-out visitor, and it is right at its meaning: the club app opens the store in its own browser, where nobody is signed in and no store cookie exists. Joined to accounts on the account key, which is empty on every one of those sessions, they are the population the new-visitor flag suggests, new fans whose lower conversion is dilution. The population the decision is about comes from a three-file chain that nothing signposts: the members'-price token on each session, the club's monthly redemption report (token to member number, a billing file) and the store's loyalty profiles (member number to account). Two independent signatures agree on the same sessions (the typed delivery address matches a saved one, the typed card matches a saved card fingerprint). Signed out, those customers lose their saved address, saved card and card-on-file exemptions, so their losses surface downstream as typed-postcode failures at the address check and 3-D Secure challenges at payment, and the members' price exists only in the club-app session, so a customer who gives up there does not buy the same kit later at the full price.

**Corpus blind for a computable reason (L1).** Both closed partner campaigns linked to the open web, so a returning customer arrived in their own browser already signed in and the signed-out share of partner traffic matched the store's base; booking partner traffic as incremental dilution reproduces both close-outs exactly (L7), and every attribution partitions the same lost orders, so every total ties (L8).

**Gate G at the draw.** Litmus: no. Every reported figure is correct (weekly conversion, step counts, approval and challenge rates, the close-outs' booked figures) and every voice's claim about its own numbers is true; the difficulty is attributing a correctly reported fall to the population it happened to. surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no (a session in the club app's browser is signed out by fact, and the identity link exists only through the redemption report and the loyalty profiles). Deletion: no wrong number exists to delete.

**Draw checks (stumping Part 6.1 against proven-in-production.md).**

- Strategy (Part 3): S7, every screen is right and the answer is a population the screen's grain cannot express (task48's discriminator): the session log's grain is sign-in state, and the decision needs the customer behind it. Laws L1, L7 and L8 above are writable in this world.
- Dead shapes (Part 4), live risks the design has to close. Argmax under a stated rule over a filed candidate list (task36): the pick is over a filed shortlist under a filed sizing line, so it survives only if the ranking quantity needs the token chain and no row the natural pipeline reads carries it. A device announced by its own columns (task48) and a device whose only defence is silence in a pack that breaks it (task76 v1): no column may say existing customer or in-app browser, and neither the partnership agreement nor the event dictionary may say the club app opens its own browser. A recovery of what an instrument could not observe (89 v6): the answer here is a remedy named by the attribution, not a repaired reported figure, but the judge's instrument repair (a session log that resolved every token to its account) narrows the decisive step to a join, so the design keeps the stripped state (no saved address, no saved card, no exemption) carrying the attribution and prices each population against its own signed-in baseline. The self-healing rung that task75's dead shape killed as a decisive move is now meant to be seen.
- Objective (guide-to-prompt step 2): the committed answer is the fix for the cause that carries the fall, with rivals ruled out on evidence (the address check drained, the club traffic's dilution, the issuers' challenges, the pre-order mix), and the prompt leaves the attribution open. The sprint is forward; the basis is the attribution of the closed review weeks and their latest week, and no forecast enters the call.

## Ladder sketch

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Lost orders by the checkout step each session ended on, review weeks against baseline weeks (the stage table) | F1 postcode lookup | The address step carries the largest rise, it lines up with the check's rollout, and the checkout lead says so | The check's flag cohorts: its losses are first failures that stop once an account re-saves its address, so by the latest week they are small |
| 1 | The check measured on its cohorts and drained (the note's self-healing pool), the rest of the fall read off the traffic sources | F2 club landing page | Club-app sessions are about a fifth of September's and convert at about a third of the rest, the largest shortfall left | The two closed partner close-outs: partner traffic converts lower and costs no orders, and booking it as incremental reproduces both exactly |
| 2 | Club traffic booked as dilution; the largest real loss left is the rise in 3-D Secure challenges at payment | F3 card SDK upgrade | Challenges rose, approvals are flat, and the SDK upgrade is the standard remedy | The affected-against-unaffected split: the challenge rise sits in signed-out sessions, and the token chain shows most signed-out club-app sessions are existing customers |
| 3 | **Decisive:** each club-app session re-attached to its account through the token chain; signed out, those customers lose saved address, saved card and exemptions, and their orders lost against their own signed-in baseline are the largest in the latest week | **F4 one-time-code sign-in** | | |

- **F5** (split dispatch) never leads: baskets mixing pre-order and in-stock lines were as common and as lossy in the baseline weeks.
- **Position.** F4 is fifth of five on the natural pipeline (no checkout step carries a sign-in loss) and leads no intermediate rung; the rung margins and the dominance ratio (F4's latest-week loss against F3's carried advantage) are settled at design.
- **Grid.** Three toggles (the drain, the dilution reading, the token chain) give eight cells; every cell without the token chain names F1, F2 or F3, asserted at design.
- **Asks.** The device layer is designed with `supplemental-stumping`; the note's bot-session device (cohort table) and authorisation-retry device (card networks) are the first candidates.

## Nearest exemplars

1. *Fund LC-12 Time-Deposit Rescue for the Q1 lifecycle budget, not the win-back list* (Lifecycle Campaign Prioritization): measured mean **0.50** over four runs (0.54, 0.58, 0.54, 0.55). Nearest on decision and failure: a pick of one option for a budget where the model beat the loud decoy (the win-back list) and lost the name in all four runs, funding LC-16 or LC-14, because it never resolved session-token actors through the device-session log. It still scored about 0.55, because its asks were reads it got right, so the ask layer, not the ladder, decides whether the pair gets under 40.
2. *Order 1,298 Top Dog kits split 749 dog, 353 cat, 196 other* (Loyalty Program Operations): measured mean **0.58** over four runs (0.62, 0.59, 0.58, 0.62). Nearest on mechanism: the model joined the archive to members by account only in all four runs and missed 970 storefront orders credited to members who checked out without signing in. The trap fired every time; the score stayed above 0.50 because the graded call was a count.

The redraw puts the same miss on the name, which is where the first draft's exemplars did not lose. The root-cause record for a #5 miss on a named leaf is *Name Education and Learning in Tessel* (Community Foundation Grants Reporting), measured mean 0.36 (0.57, 0.13, 0.09, 0.68).

## Guard

Verdict against the registered corpus (task117, task118, task120 and task123 included): **WARN** (exit 0), card at `<scratchpad>/cards/task121.json`, not registered.

- First pass: one BLOCK, test.same_driver_older against task101 on (population, G3, decomposition_attribution). Cleared by one line on the card: task101 takes the decision's own earlier payments out of a published distribution they entered under intermediaries' names, a component removed so a threshold can be cut; here a channel files established customers as signed-out newcomers and strips the state that makes them buy, so re-attaching them turns a shortfall every closed case books as dilution into the largest loss and changes which fix is named, with nothing removed from any total.
- No relabel: G3 is the generator list's own name and gap for a record-versus-operation move (gap 2), and no A to E pattern carries the decisive rung, so the pattern reads none first; A sits behind it only for the demoted self-healing rung.
- WARN overuse.org_family (retailer_or_ecommerce in 16 builds): an online store is a retailer and no other family is honest; none of the last three builds is a retailer.
- Furniture: line_manager_or_team, incident_or_complaint and retailer_or_ecommerce are each clear of task118, task120 and task123. People: eight drawn names, no findings.
- Nearest drivers: the slot's own v1 at 0.09 and task82 v2 at 0.07, both under the 0.12 WARN line. task82 shares the device class (records filed without the holder's key, attributed to the holder through a second identifier) and not the insight: it lifts a tier count, while here the re-attached population changes which remedy is named.
- Variants checked and not taken: the note's own move (time, A) is blocked inside the window by task107's v4 lineage on both structural tests; relabelled E it collides with task117 on (time, E, quantity_figure); a population E rung is blocked inside the window by task107's v1 lineage with decomposition_attribution and spent in six older builds with method_or_model_selection; a grain move (D or G2) would repeat task120's decisive move; B is banned against task123 and G5 against task118.
- Batch preview, not binding: the unregistered scratch cards for task119 and task122 are drawn 2026-10-08. If task122 registers before this card as it stands (product-analytics, product_manager, retailer_or_ecommerce), this card BLOCKs on ban.role and ban.org_family against it, and task118 leaves the window of three. The honest variant then is a head of e-commerce who runs the online store (operations_director, free once task118 leaves the three); no honest family replaces retailer_or_ecommerce for an online store, so two retail product builds side by side needs the author's call.

## Changes from the source note

1. **The call is a pick of the fix, not a forward cost.** The note's committed figure (the release's lost orders a week over 13 weeks) becomes one of five shortlisted fixes for the quarter's sprint, named with its cause, with the attribution left open in the prompt. The stump sits on the name, the Root-Cause tag rests on attributing the fall, and no forecast enters the call.
2. **A new decisive move.** The note's own (time, A: the self-healing pool) collides inside the window with task107's v4 lineage and, relabelled E, with task117, so the decisive rung is drawn fresh: G3, signed-out club-app sessions re-attached to existing accounts. The self-healing pool survives as rung 1 (the address check's losses drain as accounts re-save), where an event study by weeks since exposure is meant to find it.
3. **The partner.** The note's marketing partnership becomes a top-flight club's members app whose Shop tab (from 31 August) opens the store in its own browser with a members'-price token; the growth team's referral-quality fix becomes the club landing page (rung 1's pick).
4. **Payments.** The note's third suspect becomes the 3-D Secure challenge rise at payment (rung 2's pick), real for the issuers and mostly a symptom of signed-out checkouts.
5. **Realism.** The address check enforces the carrier's full-postcode label rule from 1 September, so rolling it back is not on the table and no flag flip settles anything; the address-step candidate is an inline postcode lookup, and each of the five shortlisted fixes takes a sprint.
6. **Calibration.** The note's two prior flagged releases stay in the pack and certify the cohort method on rung 1; the decisive rung's organ is new, the close-outs of two closed partner campaigns, which reproduce under the dilution reading and cannot see signed-out arrivals.
7. **Shape 18 and two deliverables.** The note's `regression_case.xlsx`, `forward_cost.png` and `sprint_decision.pdf` become `q4_sprint_call.html` and `checkout_fall_workings.xlsx`; the note's ask C (the forward cost under each rung basis) is dropped because it names the ladder, and its asks A and B are candidates for the device layer.
8. **Furniture.** The note's platform review board is dropped: the head of product assigns the sprint herself (line_manager_or_team), the forcing event is the conversion-fall incident, and eight personas are drawn (the first draft's seven, with the review board chair's role removed, plus Raquel Pires).

## Tried and rejected

- v1 (first draft, 2026-10-08, never registered): the address check's forward weekly cost, decisive on the self-healing pool (an account holding a CP4-only saved address fails once, re-saves and never fails again). Rejected at checkpoint A on 2026-10-09: it cleared the guard only by relabelling the note's pattern A to E, as E it still collides with task117 on (time, E, quantity_figure) while A stays blocked by task107's v4 lineage; its forward-cost figure read as Forecasting; the staggered flag cohorts let an event study by weeks since exposure show the fade (an arithmetic symptom, task75's dead shape) and the vendor's published address rules pointed at the address book; both nearest exemplars sat above 0.50 because the model names the cause and loses only on sizing; and rolling back a flag-gated release is a flag flip, not a sprint. The self-healing pool survives in v2 as rung 1.
