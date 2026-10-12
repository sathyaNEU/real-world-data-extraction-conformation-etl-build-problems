# task130: Corvane Health, the first-year contribution to its professional liability trust (architecture 4)

Private, never ships. Architecture 4, drawn 2026-10-12 as the author's fourth root for a number retired with three
architectures spent (wave 1, "re-root: retired"). v1 (a 2027 large-holder designation) and v2 (the Tenter House
replacement-unit call-off) failed on the portal; v2's hardening loop was a Template of task73 world ten at the clone
pre-flight; v3 (Red Cedar Valley's care-management baseline, regression to the mean against an untreated analog
cohort) was landed by the in-house solver in round 1 because its default construction, the analog, was the golden.
Their records are under `## Retired` and `## Tried and rejected`; the card keeps all four dead identities in
`lineage`. v3's generator, pack, goldens, write-up, metadata, prompt and its leak and clone reports were removed from
this folder at the re-root (in history at 15fab18); `solver_rounds/` stays as its evidence. Nothing of v3's world,
pack, prompt or asks is reused: v4 moves from a health plan's claims baseline to professional liability pricing, from
a selected cohort to a claims-made window, and from a school district to a health system.

Carried forward from v3's death, as design rules: the default path is written first and must end wrong on the data in
hand; no pin may point at the method; no figure in the pack confirms the solver's construction for free.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task130.json`, architecture v4, registered 2026-10-12; `guard.py check` WARN on one finding (`repeat.gate_g`, answered below); `guard.py validate` clean |
| Domain / task type | actuarial-science-insurance / pricing-ratemaking-credibility (a client domain): funding a self-insured professional liability programme is pricing its cover |
| Objective | Forecasting & Predictive Modeling: the expected cost of the claims that will first be made against a new trust in 2027, its first year, from the system's claims experience to 30 September 2026 |
| Shape | 02, forecast across periods: the expected cost (and number) of claims first made in each quarter of 2027, entity by entity from the quarter it joins (Ashgrove four quarters, Tolliver Falls three, the medical group two, Brennick one: ten cells, each with a cost and a count), each entity's 2027 total, and the contribution |
| Decision | `quantity_figure`, answer unit `currency`: the 2027 contribution the trustees put into the trust |
| Mechanism | gap time (decisive: the trust pays only for claims made inside its own opening window), then population (the claims a short window can catch are a cheap subset); pattern none; generators G13 (decisive: the horizon, the claims-made window against an annual incurred cost) then G14 (the cost of a claim conditioned on how soon it is made); Gate G `forecasting`; strategy `maturity_censoring` (the window truncates the report lag: only the claims made soon after their incident arrive in time) |
| Layer 2 family / pattern | `field_method` (exposure windows and report-lag development, the professional liability actuary's claims-made method); `own:claims-made-opening-window-cost-by-report-lag` |
| Furniture | forum `trustees_or_governors` (the trust's board of trustees sets its annual contribution), forcing event `purchase_order_or_contract` (each entity's expiring occurrence policy, renewed no further, moves it into the trust on its own anniversary date), organisation family `hospital_or_health_provider`, role family `compliance_or_audit` (the system's risk management and insurance lead), context artifact `register` (the risk management claims register the stakeholder works from), calibration `none` (the system's own claims experience is the evidence, no organ), opening `question-first`, question form `how-much` |
| Spine | payroll FTE by clinician and month, January 2016 to September 2026, about 1,100 clinicians, over 100,000 rows: one clinician's paid FTE in one month with the entity, cost centre, specialty and employment status payroll held that month; synthetic |
| Deliverables (draft) | `trust_funding_2027.xlsx` (the contribution, the quarterly emergence by entity, the asks), `trustees_paper_2027.pptx` (the call and the emergence chart); final at the build |
| People | drawn with `guard.py names --geo "United States" --seed 130 --n 40`, skipping every name v3 used: Nancy Holland (vice president, risk management and insurance; the requester), Derek White (chief financial officer), Lori Williams (director of claims and litigation), Jerome Warren (consulting actuary), Elizabeth Nelson (director of the early resolution program), Walter Butler (chair of the trust's board of trustees); none appears in the prompt |

**Guard.** `guard.py check` on the scratch card: WARN, one finding. `repeat.gate_g` (forecasting repeats task124, one
of the last two builds in draw order): forecasting is the honest mechanism, because the contribution is a bet on the
claims that will be made in 2027 and the correctly read past (every claim's cost, every year's FTEs) pins it only
through the window the trust's cover defines. Bans run against task120, task121 and task124, the three builds drawn
before this one; a first draft blocked on `ban.artifact` (operations_log, task120), `ban.forum` (board_of_directors,
task124) and the structural tests against task102 and task501 v3. The artifact and forum were redrawn (`register`,
`trustees_or_governors`); the forcing event was moved off `cutover_or_migration` so that this card adds no block to
task180, drawn later today with that event; the structural tests are answered by the card's differentiation lines
(task102 moves payments across a period boundary by a release rule; task501 v3 sized a buffer on a cumulative path's
furthest overrun; neither costs a lag-truncated window claim by claim). Gap time with pattern E was tried and blocked
against four older builds (task117, task37, task44, task97); gap population with pattern E against task124's lineage.
Nearest driver on file 0.07 (task121 v3); task50 v4 at 0.06 (a slow-surfacing failure projected with a run-out law) is
the opposite move: there the unsurfaced part has to be added, here only the part surfaced inside the window counts.

**Abstraction and same-puzzle tests.** Stripped of nouns, the driver is: a cover that pays only for events that both
occur and are first reported inside its own window is costed from a full period's cost per unit of exposure, when
inside a short window only the events reported soon after they occur can count, and here those are the cheap ones;
the expected cost is the exposure at each point of the window times the cost of past events reported within the time
then left. The three nearest drivers (task121 v3, events set against the same unit's exposure at the same clock hours;
task93 v3, what raising a floor obliges a flat-rate unit to pay; task88, displaced full-rate demand on nights capacity
fills) share no latent structure, default path or correction with it. On the maturity family's record (task181: a
pooled reporting delay against each route's own, where the forecast needs the complete count), the move here runs the
other way: the decision is the truncated count, and its cost, never the complete one.

**Data-native sentence.** Corvane's early resolution program meets most patients harmed by care within weeks, with an
apology and a modest offer, and turns their requests into quick, small settlements, while the lawsuits that carry
most of the money are filed a year or more after the incident; so a trust that each hospital and the medical group
joins on its own policy's anniversary sees, in its first months, mostly the cheap early claims from a few months of
incidents, and almost none of the suits.

**World (targets; the generator asserts or replaces each with its built value).** Corvane Health, a nonprofit health
system in western Oregon: three hospitals and an employed medical group, about 1,000 FTE of employed physicians and
advanced practice clinicians. Each entity has insured its employed clinicians' professional liability with a
commercial occurrence policy on its own anniversary; the board resolved in June 2026 to let each policy run to expiry
and move the entity into the new Corvane Professional Liability Trust, claims-made, with a retroactive date equal to
its transition date (incidents before it stay with the occurrence policy that was in force):

- Ashgrove Medical Center, the flagship (hospitalists, emergency, anesthesia, surgery, OB laborists, intensivists,
  hospital APCs and CRNAs, about 205 FTE): trust from 1 January 2027.
- Tolliver Falls Hospital (about 90 FTE): trust from 1 April 2027.
- Corvane Medical Group, the clinics (primary care, OB/GYN, surgical and medical specialties, APCs, about 640 FTE):
  trust from 1 July 2027.
- Brennick Community Hospital (about 35 FTE): trust from 1 October 2027.

Seven specialty classes as the trust's funding policy rates them (obstetrics, surgery, emergency medicine,
anesthesiology, hospital and medical specialties, primary care, advanced practice). About 33 claims a year across the
system (about 3.4 per 100 FTE, from about 11 in obstetrics to about 1.4 in advanced practice), about half of them made
through the early resolution program: requests made a median of about six weeks after the incident and settled for
tens of thousands; the rest are demand letters and suits, made a median of about fourteen months after the incident
(obstetrics about two years), most closed without indemnity but carrying defence costs, the paid ones in the hundreds
of thousands. The trust's actuarial basis (the funding policy) uses the system's own claims from incidents since
1 January 2017, valued on 30 September 2026 at paid plus case reserve, one claim per incident, trended at a stated rate.
Targets on the built pack: the default path about $2.9 million, the golden about $0.3 million; the count-share rung
about 3.5 times the golden, the prorated full-year cost share about 1.45 times; every figure re-centred off round
values at the build.

As-of date: the claims register extract runs Friday 2 October 2026, valued at 30 September 2026; payroll FTE runs
through September 2026; the trustees set the 2027 contribution at their meeting on Tuesday 10 November 2026.

## Default path

1. Read the claims register extract (one row per named defendant) and keep the rows for employed clinicians;
   collapse them to one claim per incident, summing each claim's paid indemnity, paid defence and case reserves.
2. Take incidents from 2017 onward, value each claim at paid plus reserve and trend it to 2027 at the funding
   policy's rate.
3. Sum the trended cost by specialty class and incident year, take each class's FTE-years of employed clinicians from
   the payroll file, and form each class's annual cost per FTE over the mature years.
4. Multiply by each entity's 2027 FTE by class for the months it is in the trust (twelve, nine, six, three) and add
   the four entities; spread each entity's cost evenly over its quarters for the emergence schedule.

Ends on: about $2.9 million, the annual claims cost of a mature year prorated to each entity's months in the trust.
Golden: about $0.3 million, the cost of the claims made before 31 December 2027 from incidents after each entity's
transition, each past claim's trended cost counted for the share of the window's exposure from which it would have
been made in time.

## Stump sentence

A competent solver collapses the register's defendant rows to one claim per incident, values and trends every claim
from 2017, takes the system's annual claims cost per clinician FTE by specialty class, prorates it to each entity's
months in the trust and files a contribution of about $2.9 million (Ends on); the step that lands it there is costing
the trust's opening months as a mature year, when only the claims made before 31 December 2027 from incidents after
each entity's transition count, and those are the early resolution program's quick, cheap settlements: the golden is
about $0.3 million.

## Three rules

- **Domain test:** the deciding quantity is the expected cost of the claims first made inside a claims-made trust's
  opening window, built from each entity's covered clinician exposure through the system's own report-lag and
  cost-by-lag experience, which is how a professional liability actuary funds a first claims-made year; with another
  field's nouns the retroactive dates, report lags, early resolution settlements and specialty classes have nothing
  to attach to.
- **Analyst test:** a strong analyst who dedupes the register and reads the trust agreement and the funding policy
  correctly still multiplies a mature year's cost per FTE by each entity's months of cover (about $2.9 million), or,
  having seen that the cover is claims-made, applies the share of claims made within the window at the average claim
  cost (about $1.1 million) or a full year's cost share prorated to a part year (about $0.45 million); each is wrong,
  because inside a first claims-made window only the claims made quickly count, they cost a fraction of the average,
  and the share a part year catches falls faster than its length.
- **Layer 1:** a claims register with one row per named defendant and claim stages that move (a program request that
  later becomes a suit keeps its first claim-made date); employed and contracted clinicians and institutional
  defendants in one register; two expiring carriers' loss runs in their own layouts overlapping the register (one
  carrier changed systems in 2021 and renumbered its claims); paid indemnity and defence on a transaction ledger with
  case reserves at the valuation date; payroll FTE by clinician and month with cost-centre and specialty codes
  re-mapped in 2020 and clinicians moving between entities; the early resolution program's own case log keyed on its
  case number, linked to claim numbers only once a request for compensation exists. Each is something these systems
  produce; none decides the call.
- **Layer 2:** the shortcut is to cost the trust's first year as a mature year, or as a share of a mature year's
  claims at the average cost; the expert costs the claims-made window claim by claim, each past claim's trended cost
  counted for the share of the window's exposure from which it would have been made before the year ends, entity by
  entity from its own transition date.

## Retired

task130 was retired on 2026-10-11 with its third architecture spent (`build-pipeline`, Retirement), and put back in
the author's wave 1 on 2026-10-12 as a fourth root ("re-root: retired"). Every card stays filed so none of the earlier
architectures is drawn again.

- v1 failed on the portal on 2026-10-10: both top models filed the golden.
- v2 failed on the portal on 2026-10-11, and its hardening loop 1 was a Template of task73's world ten at the clone
  pre-flight.
- v3, the regression-to-the-mean baseline (an untreated cohort selected the same way a year earlier, trended), was
  cracked by the in-house solver in round 1: it filed the golden $4,060 PMPM and every tier figure in about four
  minutes (proxy 100). The pins that closed v3's forks (the any-list Risk Tier, the cancelled RFP, the bid list's
  programme year) pointed at the method, and the renewal letter's plan totals verified the solver's claims netting.
- Hardening loop 1 measured every candidate deeper rung on the shipped pack and found none forced, fork-free and
  moving the call; the only levers left were planting a rung or deleting the pins that close forks.

## Tried and rejected

v1 (large-holder designation, failed on the portal), carried over:

- The blueprint's stated-memo architecture (a methodology memo fixing the holdings rows, the amendment semantics, the unit-by-filing-date rule, CUSIP repair and the denominator source): rejected because a strong solver implements every stated clause, so the bridge becomes a computation; its traps are kept only as lower rungs.
- Capital-markets ownership kept literally (13F holders, issuers, shares outstanding) under an accepted domain label: rejected, markets trading is outside Economics and none of the nine owns a vendor's crowding flag without a relabel a reviewer would not accept.
- Confidentially omitted holdings recovered from another public disclosure as the decisive rung: rejected on the clean-data test, the public returns are a filtered file whose repair hands the natural pipeline the answer (sole_data_defect yes).
- Denominator timing (dwellings or shares outstanding taken at a later date than the holdings) as the decisive rung: rejected on the clean-data test (a stale file whose repair collapses the task) and as a single-fact flip.
- Holders whose returns are not yet due completed from the title register: rejected, the incomplete feed is a suspect file under the clean-data test, and the register-to-titles route is a schema-visible two-hop join a strong solver takes.
- Double reporting under a non-exclusive holding definition: rejected, the regime text that makes both returns correct concedes the overlap, and dwelling-level returns are deduplicated by reference by default.
- Agent-filed returns and nominee title holders as the decisive rung: rejected as a lens swap, registrant against owner of the same dwellings on the same date.
- Employer concentration with PEO look-through as the re-skin: rejected, it drops the ownership scenario and co-employment look-through is textbook.
- Passive holders re-derived at a forward date around an index change: rejected, out-of-scope domain and textbook.
- The agency's takeovers evidenced by preventive annotations in the deed extract: rejected, the evidence would sit in the forward roll's own source.
- Settled large-holder takeovers as the clock's evidence: rejected, a back-test mismatch sends the solver to the ledger.
- The programme order naming the first-offer programme: rejected, a sentence in the document that defines the quantity sends every solver looking.
- A bridge from the raw lodged rows to the conformed total, and a bridge with one bar per kind of movement: rejected, free weight and a taxonomy fork.
- Round 1 (plain) landed v1's six-section answer: the agency's first-offer takeovers in a budget ledger with a 120-day clock recovered from settled deeds died because the solver audited the ledger for transfers unprompted.
- Hardening loop 1's pre-registered repair (re-key the ledger by expedient in a second file): rejected before building, it only hides a step the solver completed.
- Portal 2026-10-10, the hardened v1 (holders inscribed after 30 June rung): failed, both top models filed the golden seven sections. Any rung that is a record a diligent solver can find and join is solved; the certified-bulletin reproduction blessed the path instead of hiding it.

Re-root (v2):

- Staying in the large-holder world with a property-against-dwelling grain stump (undivided buildings counted as one return row but holding several flats): rejected, the judge's lens-swap example (rank by logo count when the decision needs seats) is this move, and a dwelling-grain return collapses it.
- Staying in the large-holder world with any further hidden record (a licence register for new blocks, an inheritance date, a section split): rejected, the portal solvers join every record they can reach.
- The tensioned-zone rent burden from a deposit register (stock against flow, rents indexed on each anniversary): rejected, the update rules would have to be filed and a filed rule is a computation; the stock-and-flow reading is also close to a semantic fork on "rent".
- A survival-curve stump on the whole TA population (length-biased stock, pooled leaving rate as the decoy): rejected after simulation, in near steady state the pooled rate and the duration-conditional forecast agree within 4 per cent on the TA total because the stock's slow leavers and the new entrants' fast leavers offset; and "last year's stock survival" lands within 3 per cent.
- The same survival stump on a closed cohort: rejected, the gap opens (12 per cent against a rate) but a survival curve is the textbook answer to a closed-cohort question and a strong solver fits one; it is kept as a wrong rung (R3) because the departures are rationed, not hazards.
- Tenter House filled in order of each household's first move out of emergency accommodation: rejected after simulation, the block's positions in the lists were left to chance and swung from front-heavy to back-heavy between seeds, so the call was an accident of the history; the 2023 longest-in-nightly-paid lettings rule makes the positions a property of the world.
- v2 as first shipped: the move-on order left unfiled and recoverable only from the lets log; replaced by a filed allocations scheme extract under the client's two-layer standard, which caps a method hidden and recovered from records. A scheme clause letting main-duty households also bid through HomeChoice was drafted and cut, because it opens a second exit route the plan does not count.

Hardening loop 1 (after the v2 portal failure, 2026-10-11):

- Portal 2026-10-11, v2 as shipped: failed; the reported model built the filed duty-date queue on the case record's need against the revised plan, took the accepted October lets out once and filed the golden 46 (0 / 7 / 20 / 19) at GBP 21,615. Once the order was filed, the queue was a computation.
- Ageing alone (the members' birthdays inside the window moving households between lists) as the decisive device: rejected after measurement on seeds 130 to 166, it moves two to four Tenter House households in six months and leaves a solver who freezes need on 30 September within one unit, often on the same total; kept as the second-level rung R6.
- Exact-size lists for households needing five or more as the decisive device: rejected, it is one filed sentence and a plan row away and moves only the four-bed count; kept as R8.
- Tenter House flats let on the case record's need (the record then stale for 27 per cent of the block): rejected, it fills the block with families in flats too small for them, which reads as a data defect; flats go on the need checked on the day, as a TA move would.
- Reassessing the record for every household near the front of a list before each round, so that a replay on the record reproduces every let: rejected before building, the lets log would then bless the record until the forward rounds broke it, the validated-record shape the client bans; the record is reassessed only for the household offered.
- Hardening loop 1 as built (the move-on lists on Part 3 need worked out from the household members on each round day, against a case record that lags it; 52 units against the record's 66): rejected at the clone pre-flight, reject tier (Template, Track B) against task73 world ten, whose stump is the same move (carry the class the household's record holds, when a filed rule re-derives it from the circumstances on file); task86's v2 first cut carried the same move (the bedroom standard applied with ages on the offer date) and both platform responses solved it on 2026-09-12. Its realism read (birth histories, working-day dates, the 56-day relief period, TA sizing and voids, procedure dating) was not repaired, since the device is spent. With rate-against-queue (v2) and record-against-re-derived-class (loop 1) both gone, the Tenter House queue world has no honest decisive device left that a filed rule does not turn into a computation; v2 is spent and task130 is re-rooted as architecture v3 in the same objective.

v3 build (2026-10-11):

- The first acuity score (claims dollars with pharmacy at full weight): rejected after measurement, specialty-drug members dominated every list and persistence came out only 1.1 to 1.5 times the golden, because a specialty regimen persists; the score now weights pharmacy at 0.2 of medical and the world carries the one-off medical episodes a top-of-plan list really holds (major surgery, stroke, post-acute stays, readmissions, longer cancer courses).
- Model noise keyed by a member's position on the list: rejected, the draft and the final list scored the same member differently; noise is keyed by member and year.
- Tiers from a rank on the rounded score: rejected, it tied at place 140; ranks use the unrounded score and the lists show one decimal, as the cover sheets say.
- Scores on nominal dollars: rejected, the 2024 and 2026 scores drifted apart with prices and the bid and final tiers stopped meaning the same acuity; dollars are restated to a 2023 base.
- Model noise salted with the world seed: rejected, the seed sweep and the build drew different lists; the salt is fixed (41730).
- Seeds 100000 and 102002: passed every gate but their tier baselines fell out of order (a lower tier costing more than a higher one in total), which a board reads as a broken model; seed 101005 kept.
- A tier total column in the workbook: rejected, Schedule C.2 forbids intermediate rounding and tier 4's unrounded total rounds to 2,630 against 2,629 from its rounded parts; the medical and pharmacy figures stand alone and Note 1 says why.
- R3b, R5b and R6c land within 5 per cent of the golden total: accepted rather than forced apart, they are the arithmetic of 18 against 24 months of trend, weights only, and two offsetting errors; each still misses the whole-dollar tier cells it touches.
- R4b equal to the golden in tier 3: accepted as structural, no tier-3 bid member left the plan during the year; checks.py reports it.
- The renewal letter restating Schedule C's member-month and incurred-date rules: cut, each convention is stated once, in Schedule C.
- Procedure lines carrying diagnoses drawn at random: replaced by procedure-appropriate diagnosis maps for outpatient surgery and hospital services.
- context_artifact register, asked for at the card update to clear filed_model's collision with task133: BLOCK ban.artifact against task131; redrawn to operations_log, the plan's claims and eligibility feeds the baseline is built on.

Repair 1 (2026-10-11):

- Seed 101005 under the rebuilt claims engine: bid tier 1 fell to 8 members and the tier baselines fell out of order at every acuity base from 2,200 to 2,500; a sweep of seeds 101000 to 101053 at four bases kept 101050 at 2,500, which passes every gate at all four.
- A simulation that started in January 2024: the 2024 selection year had a shallower history than 2026, so the bid's tier 1 shrank against the final's; the simulation starts in January 2023 as burn-in.
- A plan-wide medical PMPM near $425 under the first fee schedule: low for a school district plan; facility charges, consults and the commercial multiple (1.14 of the reference schedule) bring it to $468.
- Home health priced as a case rate: allowed ran above billed; it is priced per visit at a share of charges.
- A wrong-member claim drawn from any family member: it put PSA tests on women and deliveries on men; the wrong member is drawn from the same sex and age band.
- Birth-date corrections drawn freely: five-year changes no conversion produces; one digit of the year, on two-child families.
- Pharmacy pickups on the day a fill fell due: a Monday spike; pickups spread over five days on a weekday profile.
- A hepatitis C first visit dated the first of the month: a Sunday office visit; moved to the next business day, no graded figure moved.
- The duplicate assertion counting a wrong-member claim that was later voided as a second payment: the assertion reads only live claims.
- The first rebuild's programme pharmacy ($1,689.88) rounded with the persistence rung's ($1,690.46): centring now holds the programme figures a dollar clear of persistence's, and checks.py asserts no rung lands on either programme figure.
- Centring that let one pharmacy fill move 7 per cent: a fill now moves at most 2.5 per cent and a facility claim 4 per cent.
- The memo's "a transplant, a premature baby, a cancer course or an accident" and the chart title "pharmacy moves much less": false on this seed (no enrolled member had a transplant in 2026; tier pharmacy baselines run 0.29 to 3.18 times 2026); rewritten to the enrolled members' own 2026 and to "pharmacy moves both ways", both asserted.
- Implementation plan tables that opened with the role and the milestone: the guard's name reader joined cells into "Ellery Final", "Ellery Welcome", "Kelley Enrolment" and "Santiago Direct" (a BLOCK on two Ellerys); the tables open with the name and the date.
- Jessica Petty from the draw as outreach supervisor: a first-name WARN against task104; Edward Miller from the same draw.
- LibreOffice's /DocChecksum left as exported: it hashes the run clock and broke byte identity between rebuilds; it is recomputed over the pinned file.

Repair 2 (2026-10-11, the second reader's forks and signposts):

- Seed 101050 with pharmacy at 0.2 of medical in the score: pharmacy persisted (0.99 of its selection-year level in real terms), so carrying the enrolled members' own 2026 pharmacy forward landed a dollar from the golden programme pharmacy; the score now counts pharmacy at 0.4 of medical and the world carries one-off pharmacy (hepatitis C cures, G-CSF and capecitabine with chemotherapy, fixed-length venetoclax and adjuvant oral oncology, CMV prophylaxis after a transplant, teriparatide after a hip fracture, biologic starts with a loading dose, stops and switches, weight-loss GLP-1s started and stopped).
- Recital C's "no agreement was executed and Northcourt provided no services": read as certifying the untreated control; the recitals are now procurement history, and the untreated status follows from the cancelled RFP, the second RFP and the implementation plan's dates.
- One member carrying 26 to 31 per cent of each bid tier's medical, and one or two specialty-drug members 63 to 89 per cent of its pharmacy: a credibility argument for pooling; the new seed and score hold the largest member to 25 and 22 per cent.
- r2's first seed choice, 102002 with pharmacy at 0.75 of medical: chosen on a world before the sim's last incidence fixes and never rebuilt; superseded by a 160-seed sweep of score weights, pharmacy weights and tier splits on the final simulation.
- Seed 102016 (the sweep's first pick: pharmacy at 0.4, persistence 2.44 times the golden): its world let a spouse dropped at open enrolment come back after the employee had remarried, two spouses on person code 02 at once, and the PBM join refused it. The re-add now waits for no other spouse on the plan; that changes the random stream of any world where it bites, so 102016's world was redrawn and dropped, and 102037, whose world the guard leaves unchanged, was taken.
- Centring blind to the full-year-only rung: tier 4's pharmacy baseline and R4c rounded to the same $2,114; baseline cells are now centred off R4c's whole dollar on a part-year member's claim, which leaves R4c in place.

Repair 3 (2026-10-11, the third reader's forks on the main call):

- Repair 2's eligibility churn under lists drawn on the simulation's own coverage: RCV8692544 left on 31 October 2026 and was rehired from 1 March 2027, so he scored onto the final list at rank 18, Tier 1, while the eligibility file, cut at 28 February, ends his coverage in October and Tier 1 read 35 or 34; the model now scores only members the eligibility file of the run carries on the list's date (the administrator's file of the first of the month, through the day before), which leaves the RFP and draft lists as they were and takes RCV9058604 (Tier 4, an RFP list member) onto the final list in his place.
- Schedule C.1(e) as repair 2 left it ("a member's Risk Tier is the tier assigned to the member on the Final Enrolment List"): it gave the members on both lists their final tier for the RFP cohort's year too, a reading that moves every tier cell and the programme total by 3.3 per cent; C.1(e) now defines a Risk Tier as the tier the model places a member in when it draws a list.

Repair 4 (2026-10-11, the tuner's round targets):

- The tuner's round-value targets (each tier baseline aimed at a two-decimal value such as 3,017.30 and landing within 0.00002 of it, each 2026 PMPM moved onto a quarter-dollar such as 4,335.25): a confirming bell, since a solver printing full precision saw a figure come out exact only under the intended method; each graded figure now lands at an offset drawn for it from a seeded generator, clear of the cent grid, and a draw is kept only once it is built and every rung's and fork's programme total sits off that grid too (taking the cheapest tier combination in every draw left R2 within 0.0005 of $4,427.31 in both draws tried, so a draw now takes one of the thirty cheapest).

Hardening loop 1 (after v3 round 1, 2026-10-11):

- v3 round 1: the analog cohort's tier PMPM, trended and count-weighted, landed in four minutes. The in-house solver read the selection on 2026 claims as regression to the mean, took the cancelled RFP 2025-07 cohort as the untreated comparison (Schedule C.1(e)'s Risk Tier "when it draws a list", Recital B's cancellation before an award, the bid cover's proposed programme year), measured its April 2025 to March 2026 allowed PMPM in its RFP tiers (41, 30, 23, 46), trended it 24 months, weighted by the final list's 34, 37, 38 and 31 and filed $4,060 ($1,438 medical, $2,622 pharmacy) with every ask figure; its netting tied to the renewal letter's Exhibit 1 to the dollar on claims paid through 31 January 2027, which confirmed it for free.
- Exposure weighting as the next rung (C.1(i) rewritten so the Programme Baseline is expected claims over expected Member Months, each tier weighted by its members times their expected months): rejected after measurement. The analog's Member Months per member enrolled at its start (1 April 2025) run 11.28, 11.48, 11.00 and 11.48 by tier and move the total 0.05 per cent ($4,058.14); per listed member (10.73, 11.10, 11.00, 11.48) they move it 0.59 per cent ($4,036.04). The effect is two dollars on the estimator a careful reader takes (every Enrolled Member is enrolled on 1 April 2027), the two estimators are a fork 0.54 per cent apart with no closure, and the count weighting it would replace is filed.
- Case-mix normalisation by age and sex (each analog tier indirectly standardised to the enrolled tier's ages in the Programme Year, the score being claims-only): rejected after measurement. Nothing in the pack forces it (C.1(h) takes a tier's experience from the members in that tier, and no clause or standard makes the unadjusted reading a violation), a consulting actuary's funding-rate letter carries no age and sex rating table, so the table is the solver's choice, and four defensible tables from the plan's own 2025 and 2026 experience move the total -3.56, -2.03, -1.20 and +0.18 per cent ($3,915.75, $3,977.78, $4,011.55, $4,067.64; raw and smoothed, by benefit and combined). The adjustment's size is the table, it is under 5 per cent in every reading, and the raw tables move the baseline away from the simulated truth ($4,348.19), not towards it.
- The analog's selection rule against the final list's (the top 140 of a different pool, cut into fixed score bands): rejected after measurement. The bid list's lowest score is 33.0 and the final list's 34.1, so tier 4 spans different bands; restricting the analog's tier 4 to the final list's floor (24 of 46 members) moves the total +1.39 per cent ($4,116.55), contradicts C.1(e) (a Risk Tier is the tier the model places a member in when it draws a list), and the gradient inside the band is noise (the analog's April 2025 to March 2026 allowed PMPM for tier-4 scores below 34.0, 34.0 to 34.4, 34.5 to 34.9 and 35.0 to 35.6: $2,056, $4,829, $2,143 and $2,840).
- Part of the analog treated by another programme: nothing in the world treats the bid cohort (no administrator or PBM programme reaches it in 2025-26), and adding one to make a rung bite would be a planted defect; not built.
- A bridge from the first two months after each selection year (the analog's January and February 2025 against the enrolled members' January and February 2027, as a ratio on the analog's year): rejected after measurement. It moves the total +8.98 per cent ($4,424.87) on tier ratios of 0.17 to 2.70, two months of a heavy-tailed cohort; nothing files it, and its medical half needs a completion factor for February 2027 that the renewal letter does not derive. The enrolled members' own January and February 2027 pharmacy, trended to the Programme Year's midpoint, runs 12.8 per cent above the golden programme pharmacy: a reading of C.1(h)'s "experience of members in that Risk Tier" the pack does not rule out, which any architecture that keeps this world has to close.
- Weakening the three pins that announce the analog as the hardening on its own: rejected, hardening by deletion. Each pin closes a fork (the comparator tier for the 20 members on both lists, the cohort's untreated status, the analog window), and the bid list in the folder still announces the analog to any solver who knows regression to the mean.
- Verdict: v3 is spent. With the analog construction forced and found, every deeper adjustment measured is optional with no shipped sentence the unadjusted reading violates (case mix, the bridge), contrary to a filed clause (the score floor) or worth two dollars (exposure); none moves the call by 5 per cent on a forced, fork-free path, and a plant is the only fix left. v3 is the number's third architecture, so the pipeline's cap retires task130 unless the author grants a fourth root.

Architecture 4 draw (2026-10-12):

- Draws weighed and not taken. A zone substation's peak after rooftop solar moves it into the evening: with
  half-hourly load and a solar profile in the pack, netting the two half-hour by half-hour is the solver's first move,
  so the default lands. A drought outlook whose evaporation scales with a shrinking lake's surface area: the planning
  scenario has to file evaporation as a depth to be deterministic, and a depth sends every solver to the area table.
  Bowel screening demand by prevalent and incident rounds: "first screen or repeat" is the first cut any screening
  analyst makes, and the colonoscopy yields of first-time and repeat attenders nearly cancel per invitation. Mortality
  after the end of a level term: the analog cohorts' post-level experience lands when it transfers, and a model is a
  fork when it does not. Fiscal drag under frozen thresholds: with taxpayer records in the pack the microsimulation is
  the first move. Increased limits factors after a minimum-limits change and leveraged trend in an excess layer:
  per-claim trending under the new limit or retention is the actuarial reflex. Override bias against a random
  low-side test: the decision reason code and the test's own description name the unbiased sample. Real-time data
  vintages and mixed flood populations: neither method is forced by the estimand, so both are forks. Group quarters
  in a cohort-change projection: the error moves only with the local cohort's size and stays a few per cent.
- Claims-made funding with one entity joining on 1 January: the decisive step collapses to one filter (the claims
  made in the same calendar year as their incident, costed on their own), which the coverage clause prompts and a
  careful solver writes in one line; the draw keeps the claims-made window but staggers the transitions on each
  entity's policy anniversary, so a part-year window catches a share of claims that falls faster than its length,
  and keeps the cost of each claim tied to how soon it is made.
- Card variants blocked at check: gap time with pattern E (test.same_puzzle and test.same_driver against task117,
  task37, task44, task97); gap population with pattern E (test.same_driver inside the window against task124's
  lineage); forcing event cutover_or_migration (it would have banned task180, drawn later today with that event).
