# DS26 — Whether this cycle's one backbone upgrade goes ahead, when the room it frees is claimed by circuits already waiting for it

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · research and education networking |
| Mirrors | Capacity upgrades whose new headroom is claimed by demand queued behind the constraint (cloud regions whose new racks are consumed by reservations waiting for them, hyperscaler WAN links whose reserved-bandwidth tiers refill on upgrade, fulfilment-centre expansions absorbed by held inbound) |
| Decision shape | Hold, forced by a blocking quantity: commit the cycle's single 400G upgrade to one of six shortlisted links, or carry the allocation into next cycle's programme |
| Committed call | Upgrade one named link or hold the allocation, with the deciding figure: the backbone's worst-case single-failure utilisation with the best candidate in service |
| Gap · Pattern | Gap 1 (time) into Gap 3 (objective) · S5, a ceiling that binds only after a self-referencing solve (admission consumes the headroom it is computed from), with a saturated tie (E21) at rung 1 |
| Gate G mechanism | binding_constraint, with signal_vs_noise_or_hold |
| Measured traps engaged | #22 solves a self-referencing rule in one pass · #19 breaks a big tie instead of questioning it · #10 notes a binding limit as a risk |
| Calibration form | Existing-book actuals: the link book of 38 backbone links with three years of loads, 14 single-link incidents and five past upgrades |
| Driving force | The upgrade that clears the one breach also lifts that link's guaranteed-circuit ceiling, which is 40% of capacity, and fourteen requests already wait for exactly that room. Admitting them is a sequential, path-by-path solve whose ceiling binds again on the links beyond, and their reserved rates are planning load. With them in service the second link breaches the standard. In no past upgrade was anything queued on the upgraded link. |

## 1. Situation

A national research and education network can fund one 400G upgrade this cycle, among six backbone links on engineering's shortlist
(A–F). Its resilience standard caps every backbone link at 90% of capacity at planning load when any one backbone link is lost. An upgrade
is committed only where it brings the backbone within the standard; otherwise the allocation carries into next cycle's programme. The NOC
manager trusts the incidents the network has actually lived through. Separately, the network sells guaranteed point-to-point circuits to
member universities, administered by a service desk.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: link counters, incident logs, traffic matrices, the circuit register and the request queue. No
  stakeholder read is overturned: the counters really did read 100%, the shortlisted science-corridor link really is the worst under
  failure, and its upgrade really does clear its own breach. The difficulty is that the upgrade changes the load it is tested against.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the NOC manager's view and the technical committee's basis. The textbook single-failure simulation still names
  the science-corridor link, and its one-pass check with the upgrade in service still passes.
* **Instrument repair.** Suspect file: the link counters, which stop at line rate, so four incident readings sit at 100%. Repaired with
  unsaturating flow telemetry, rung 1 reads offered loads (C 146%, B 104%, A 101%) and names C; rung 0 still names A and rung 2 still names
  C. No instrument of today's traffic records the circuits the upgrade will admit, so the admission solve is still needed and the hold
  stands.
* **Lens swap.** The naive read and the answer are different populations at different moments: today's traffic against the traffic the
  network will carry once the requests the upgrade admits are in service.

## 3. The driving force

A strong solver routes the planning matrix under every single-link failure and finds one breach: the science-corridor link C runs at 118%
when link K fails. Upgrading C to 400G clears it, and re-running the check with C in service leaves the backbone's worst case at 88.0%.
Every step is correct. But C is also the link that has held back fourteen guaranteed-circuit requests from member universities, 188 Gbps
in all. Guaranteed circuits may take at most 40% of any link, and C's 40 Gbps of reservations already fill its share. The upgrade lifts that
share to 160 Gbps. The service desk then provisions waiting requests in order, each only where every link on its path still has room, so
admission is a sequential solve in which each circuit consumes headroom that later circuits are tested against. Seven circuits fit, 82 Gbps,
and the ceiling binds again on G and H, the two links beyond the corridor hub, long before it binds on C. At their reserved rate the
circuits are planning load, and with them G reaches 110.0% when link K′ fails. No document connects the upgrade to the queue.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Normal-state 95th-percentile utilisation per link, the NOC dashboard view; upgrade the hottest | A, the north–south trunk (84%) | The view everyone watches daily, and A leads by 1.20× | The resilience standard tests the loss of one link at planning load, not normal operation |
| 1 | Hygiene, then the incident record: bundle members summed to their link, peak utilisation on surviving links across the 14 single-link incidents; A, B and C tie at 100%, settled by the planning guide's tie-break (most incidents at peak) | B, the eastern ring link (at peak in 4 incidents, against A's 2 and C's 1) | Real failure evidence rather than a model, cleaned, with the guide's own rule settling the tie | The monitoring guide: counters cannot read above line rate. Routing each saturated incident's traffic matrix gives offered loads of 146% (C), 104% (B) and 101% (A) |
| 2 | Textbook N−1: planning matrix plus provisioned circuits routed under every single-link failure; upgrade the worst link and re-run the check with it in service | C, the science-corridor link (118% under loss of K, against B's 88%); with C at 400G the backbone's worst case is 88.0%, inside the line | Complete, reconciled, certified by all 14 incidents, and the post-upgrade check passes | The request queue: fourteen requests (188 Gbps) wait on paths through C, whose 40% guaranteed ceiling rises from 40 to 160 Gbps with the upgrade |
| 3 | **Decisive:** with C at 400G, admit the queued requests in order against every path link's 40% ceiling, add the admitted circuits at reserved rate, and re-run N−1 | **Hold**: 82 Gbps admitted, the ceiling binds on G and H, and G reaches 110.0% under loss of K′. The other five candidates leave C's 118% in place | — | — |

* **Position table.** Rung leaders are A, B, C, then the hold, and no leader repeats. A leads rung 0 by 1.20× (84% against B's 70%). B wins
  rung 1's three-way tie on incident count, 4 against 2 (2.0×). C leads rung 2 by 1.34× (118% against 88%). C sits 4th of six on rung 0
  (58%, level with D) and 3rd on rung 1's tie-break.
* **Blocking quantity.** With C in service and the queue admitted, the backbone's worst case is 110.0% (G, loss of K′), 20.0 points over
  the line. Every other candidate leaves C at 118%. The hold is falsifiable: had the requests that fit through G come to 14 Gbps or less, G
  would end at or under 90.0% and C would be the pick.
* **Discriminator dominance.** C carries a one-pass clearance on G of 1.08× into rung 3 (90 / 83). Admission multiplies G's planning load
  by 1.33× (220 / 166), so G lands 1.22× over the line (110.0 / 90): 1.08 × 1.22 = 1.33.
* **Partial correction priced (L3).** Every half-applied admission names C. A solver who tests each request against C's own ceiling alone
  admits 120 Gbps, but 110 of it is queued through H, so only 10 Gbps reaches G, which ends at 88.0%: the backbone's worst case stays
  88.0% (B and G), inside the line, and C is the pick. A solver who reads the queue as strictly first-come stops at the third request,
  which H cannot take, admits 28 Gbps through H and nothing through G, and names C at 88.0%. A solver who admits path-wise but adds the
  circuits to C's load alone, forgetting they cross G and H, sees C at 50.0% and the backbone still at 88.0%, and names C.
* **Grid.** Basis (normal p95, incident peaks, planning N−1) × upgrade check (none, one-pass, strict order, C's ceiling only, path-wise
  admission with load on C only, path-wise admission) = 18 cells. The first two bases name A or B under every check, since nothing waits on
  either. Planning N−1 names C under the first five checks, at 88.0%, and holds, at 110.0%, only under full path-wise admission. Admitting
  every queued request is not a cell: it puts 228 Gbps of reservations on C against the 160 Gbps ceiling that made the requests wait.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The service terms describe how circuits are provisioned, and the standard describes the failure test. No document
   says an upgrade releases queued requests, or that admitted circuits count against the upgrade that admitted them.
2. **Corpus blind for a computable reason.** *In every one of the five past upgrades the upgraded link's guaranteed reservations sat below
   its 40% ceiling, so no request was waiting on it, and its next-quarter load equals the one-pass figure (5 of 5 within 1%).*
3. **No arithmetic symptom.** Counters, matrices, circuits and incidents reconcile on every rung, and the queue is a legitimate backlog
   that no hygiene check flags.
4. **Not a row predicate.** Admission walks the queue in order, tests each request's whole path against per-link headroom that earlier
   admissions have already consumed, and feeds the result back into a full failure simulation.
5. **The enumeration is arithmetic.** Which requests are admitted is computed. No column says admissible, and filtering the queue on its
   status ("waiting") returns all fourteen, which overfill C's own ceiling by 68 Gbps.
6. **No cutover date.** Admission happens after a forward in-service date, and no series in the pack steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice the one-pass check still passes.

## 6. The calibration corpus

* **Form.** The link book: three years of monthly loads per link and direction, capacity history, 14 single-link incidents with
  five-minute readings on every surviving link, and five past upgrades with the loads before and after.
* **What it certifies.** Rung 2's routing: shortest path on the fixed metrics with even ECMP splitting, applied to each incident's traffic
  matrix, reproduces every unsaturated surviving-link reading within 1.5% in 14 of 14 incidents; the one rival split, weighting by
  capacity, reproduces 9 of 14. It also refutes rung 1, because four incidents read 100% on links whose routed offered load is 101% to
  146%.
* **What it is blind to.** Admission (above). The one-pass upgrade model reproduces 5 of 5 past upgrades.
* **Twin pair.** C and D are identical on every link-book column: 100G, normal p95 58%, 40 Gbps of reservations at the ceiling, 188 Gbps
  queued on paths through each, same corridor class and number of members served. Upgraded, C admits 82 Gbps and D 41 Gbps (2.0×),
  because the ceilings on the links beyond them bind at different points. No lookup on the link book separates them.
* **Resemblance points at the decoy.** C's capacity step and corridor class most resemble the third past upgrade, whose next-quarter load
  matched the one-pass figure to 0.4%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The resilience standard: no backbone link above 90% of capacity at planning load on the loss of any one backbone link.
  The planning manual: planning load is the IP planning matrix (each pair's 95th percentile over four months × 1.3) plus guaranteed circuits
  at reserved rate. The upgrade rule: an upgrade is committed only where it brings the backbone within the standard; otherwise the
  allocation carries forward. The service terms: guaranteed circuits may take at most 40% of any link; requests are provisioned in order
  within 30 days once every link on the path has room, and a request that does not fit does not hold back later ones. The routing policy:
  metrics are set in the policy table and do not change with capacity.
* **Empirical pins.** Routing and ECMP splitting, from the 14 incidents.
* **Voices.** The NOC manager: "We size for the failures we've actually had, and the counters don't lie." The head of engineering: "The
  draft has always gone to the hottest links." The service-desk lead: "Circuit requests are a provisioning matter, not a planning one."
* **Licensed wrong basis.** The standard records that the board's technical committee reviews upgrades on normal-state 95th-percentile
  utilisation against the 70% alert line and will present that view.

## 8. Determinism by construction

* **Planning window.** Three-, four- and six-month matrices give the same breach, the same rung-2 ordering and, since admission depends
  only on reserved rates, the same admitted set. The manual pins four months and the 1.3 factor.
* **Queue order.** Request timestamps are unique, and the service terms pin skip-ahead: a request that does not fit does not hold back
  later ones. Under skip-ahead the six requests through H after the second, and the last request (24 Gbps through G), are blocked; the five
  requests through G before it exactly fill G's 54 Gbps of headroom, so no tie or rounding convention changes the admitted set.
* **Paths.** Every request carries its computed path in the queue record, and metrics do not move with capacity, so no routing fork opens.
* **Reserved against measured.** The manual counts circuits at reserved rate. Admitted circuits have no measured usage to substitute.
* **Rounding.** The blocking quantity is 220 / 200 exactly, and every candidate's figure sits at least 2 points from 90%.

## 9. Prompt sketch and deliverables

> I have one 400G upgrade to place this cycle, and engineering's shortlist has six links on it. Our NOC manager is sure the incidents we've
> actually had tell us all we need. Tell me which link gets it, or that the money should wait for next year's programme, in one sentence I
> can minute, with the utilisation figure that decides it to one decimal. Send `upgrade_case.xlsx`, a chart `failure_headroom.svg`, and a
> one-page `board_minute.docx`.

* `upgrade_case.xlsx` — each candidate under the four rung bases, the admission table, the alert sheet (ask A) and the maintenance sheet
  (ask B).
* `failure_headroom.svg` — for each of the six candidates, the backbone's worst-case single-failure utilisation with that upgrade in
  service, one-pass and with the queue admitted, as paired bars, with the 90% line labelled, G's 110.0% annotated and the two links left
  at the guaranteed ceiling named.
* `board_minute.docx` — the committed call, the blocking quantity, and what would have made it a pick.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 38 backbone links, the hours in the last four months its busier direction spent
  above the 70% alert line. *Device:* nine links are bundles whose members report as separate interfaces, and three of them gained a member
  mid-window, effective-dated in the bundle register. Treating members as links splits nine links into 22 rows; dividing by today's bundle
  capacity overstates the three in their early months.
* **Ask B (device-carried).** For each of the 24 PoPs, the hours of planned maintenance last year and the share of them inside the daily
  peak window (14:00–20:00 UTC). *Device:* the change calendar records each window in the PoP's local time, and the PoP register gives the
  zone, with nine PoPs one hour ahead of UTC and on summer time. Reading the calendar as UTC misplaces every window at those nine.
* **Ask C (validity).** For each of the six candidates, the backbone's worst-case single-failure utilisation with that upgrade in service
  under the one-pass check and with the queue admitted, and the links that end at the 40% guaranteed ceiling.
* **Decoupling.** Clearing the admission solve changes no figure in asks A or B. Bundle counters and the change calendar never enter the
  planning matrix, the circuit register or the queue.

## 11. Rubric arithmetic

38 links (ask A) + 24 PoPs × 2 (ask B) + 6 candidates × 2 + 2 ceiling links (ask C) + the hold, the blocking quantity, its distance from
the line and the falsifier + 5 named chart parts + 3 files ≈ 112 criteria.

## 12. World-building constraints

* Normal p95: A 84%, B 70%, F 66%, C 58%, D 58%, E 49%. Four of the 14 incidents read 100% on surviving links, B in all four, A in two and C
  in one; routed offered loads at those readings are C 146%, B 104%, A 101%. All four fall in data-challenge weeks, when corridor traffic
  runs above the planning matrix, so A and B sit under 90% at planning load.
* Planning N−1: C 118% (loss of K), B 88% (loss of L), A 86%, every other link at most 84%, G 83% of 200G (loss of K′), H 52% of 400G.
  With C at 400G under one pass: C 29.5%, backbone worst 88.0% (B).
* The queue: fourteen requests, 188 Gbps, in this order: through H 16, 12, 14, 12, 12, 12, 12, 20; through G 12, 12, 12, 10, 8, 24. C holds
  40 Gbps of reservations, G 26 of its 80 Gbps ceiling, H 132 of its 160. Admission takes seven requests (82 Gbps) and leaves G and H at
  their ceilings; G ends at 220 of 200 Gbps (110.0%), H at 59.0%, C at 50.0%. C's ceiling alone admits 120 Gbps, 10 of it through G (88.0%).
* D matches C on every link-book column and would admit 41 Gbps. The five past upgrades had nothing queued on the upgraded link.
* Rung leaders A, B, C, hold. Bundle membership and the change calendar touch no planning, circuit or queue record.
