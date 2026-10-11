# task446 design note

Seed ET03 (GLEIF LEI-hierarchy issuer-group concentration over N-PORT holdings, Data Extraction &
Conformation). Re-rooted at the draw: the seed's stump (relationship types, LAPSED status, successor
LEIs, ISIN fallback) is rule application and data semantics, and its asset-management pairing
(Quantitative Finance with ETL) was taken by task445, registered first the same day. The objective and
the number stay; the domain moves to Banking, Credit & Financial Risk and the LEI-hierarchy mechanics
stay as Layer 1 on the ask paths.

## DRAW

| Axis | Draw |
|---|---|
| Card | `cards/task446.json`, registered 2026-10-11 with `guard.py register` before the ladder; verdict WARN (answered below) |
| Domain / task type | banking-credit-financial-risk / other: obligor-group credit concentration and house-limit monitoring (client domain Banking, Credit & Financial Risk) |
| Objective | Data Extraction & Conformation (ETL): five quarter-ends of loan, securities and derivative exposure from three booking systems conformed to obligor groups on the GLEIF consolidation hierarchy, then projected under the bank's filed standard |
| Shape | 01 ranked list under a cap: every agenda group ranked on projected utilisation of its house limit, the in-or-out on its request, the approvable amount |
| Gate G mechanism | etl_conformance (the history conformed to the estimand the standard defines) |
| Gap / pattern | population then time / none; generators G4 (attribution at transition, decisive), G2, G19, G13 |
| Decision type | quantity_figure (GBP, the approvable commitment for the requesting group) |
| Stump strategy | time_semantics (which membership a history describes); decisive rule filed: yes (estimand), official decoy: no, validated decoy: no |
| Calibration | none, because nothing has to be recovered: the projection formula and the group definition are filed, and the difficulty is the history the formula runs on |
| Context artifact | other: the credit committee's pending-request agenda |
| Role | head of credit portfolio analytics (portfolio_manager family); forum committee_or_panel; forcing event vote_or_meeting; org financial_institution |
| World | United Kingdom, GBP, a UK commercial bank; personas Lesley Miller, Russell Hussain (`guard.py names --geo 'United Kingdom' --seed 446`) |
| Layer 2 | estimand_identification, own:history-rebuilt-on-the-projected-membership |
| Layer 1 | GLEIF merger events with retired predecessors still keyed in the loan system; lapsed relationship records; international branches; fund-management links; blank issuer LEIs resolvable through the ISIN map; three booking systems with their own keys, currencies and units; quarterly archived reference-data snapshots |

**Guard WARN answered.** `three_rules.strategy_risk` (time_semantics). The decisive step is not
reading a date field: every date in the pack is read the same way on the wrong path and the right
one. The step is choosing which membership a five-quarter history describes when the standard
projects the group as it stands now. The analyst test below names the route that fails after every
field and rule is read correctly: point-in-time joins, the discipline a careful analyst applies to any
history by habit.

**Similarity claim.** No prior build turns on rebuilding a history on the membership of the date the
projection is for. Nearest drivers on file sit at 0.07 and below (task33 forward yield, task65 filed
grouping rule, task87 per-entity cap, task14 entitlement resolved point in time). task14 resolves
membership point in time as the right answer; here point in time is the trap.

## The three rules

- **Domain test.** The call turns on credit-exposure aggregation to obligor groups under
  accounting-consolidation control (drawn loans, undrawn commitments under a credit conversion
  factor, investment securities, derivative replacement cost net of cash collateral per netting set)
  checked against house limits through a limit-monitoring projection; put another field's nouns in
  and the consolidation hierarchy, the commitment exposure measure and the limit framework have
  nothing to attach to.
- **Two layers.** Layer 1: the bank's three booking systems (loans, investment securities, derivatives
  with CSA collateral), each with its own keys, currency and units, and the GLEIF golden copy
  archived at each quarter-end, with its real behaviour (merged LEIs still keyed in the customer
  master, lapsed relationship records, branches, fund-management links, blank issuer LEIs on
  custodian feeds). Layer 2: a five-quarter history built for a projection of the group as it stands
  on the projection date has to be rebuilt on that membership; the point-in-time build books
  acquisitions and disposals as growth and shrinkage.
- **Decisive step class: analytical.** Analyst test: a strong analyst who conforms every quarter's
  three books correctly and reads the standard correctly builds each past quarter on the hierarchy
  archived for that quarter, because point-in-time joins are the default discipline for history, and
  so books membership changes as exposure change and files the wrong approvable amount, too low for a
  group that grew by acquisition and too high for one that sold a borrower.

## Stump sentence

A competent solver conforms all three books, groups each quarter-end on the hierarchy the bank archived
at that quarter-end (or on the customer master's group code as it stood then), and so the requesting
group's April acquisition of a borrower the bank already lends to enters its history as
quarter-on-quarter growth; the least-squares trend it projects with is inflated, the projected
year-end exposure is overstated and it approves a commitment well short of what the limit allows
(figures fixed at build, recorded in the ladder below).

## Data-native sentence

Obligor groups change shape between quarter-ends (a parent buys a borrower the bank already lends to,
sells another to a group the bank also lends to), and the bank's own records of those quarter-ends,
the archived golden copy and the customer master's group code, are both correctly point-in-time, so
the history a projection naturally reads describes groups that no longer exist in that form, while
the standard projects the group as it stands on the projection date.

## Gate G

- **Litmus.** No reported number in the pack is wrong and nothing is overturned. The archived golden
  copies, the customer master's group codes and every extract are correct for the date they describe;
  the difficulty is that the projection is for the group as it stands on 30 September 2026, and a
  history built point in time describes other groups.
- **Mechanism:** etl_conformance (the five-quarter history conformed to the estimand the standard
  defines), with forecasting support (the filed least-squares projection runs on that history).
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Delete every wrong number:** there are none to delete; repair every file at source (successors
  keyed, late extract merged, one derivatives run, both parent relationships reported) and the main
  call and the point-in-time figure do not move (asserted: every ask device mishandled at once leaves
  B1 at 21.8 restated and 15.0 point in time).
- **Lens swap:** no. The naive history and the answer's history are different borrower populations
  (asserted), and the difference runs both ways: Tarrant Hydraulics enters Kelderby's restated history
  for all five quarters, Norbeck Coatings leaves it for all five.
- **No artifact ranks the requests.** No concentration report, limit-utilisation report or past limit
  check ships; the house limit register gives limits only.

## Entity and decision

Calder & Wey Bank plc's credit portfolio analytics team runs the LMS-03 limit check on the six Part B
requests for the 4 November 2026 credit committee. The committed call: **how much of Kelderby
Facilities Ltd's GBP 30.0m term loan the committee can approve: GBP 21.8m.** Forward facing: the
projection is to 31 December 2026, a quarter that has not closed, and the commitment is signed against
it. The tag stays ETL: the work is conforming three booking systems and five archived hierarchies
into one group-by-quarter exposure history; the projection is a filed one-line formula.

## Ladder (asserted in `generator/checks.py`; B1 Kelderby, approvable GBP m)

| Rung | Reading | Projected | Approvable | Killed by |
|---|---|---|---|---|
| R0 | point in time, drawn balances only (the loan book's balance column) | 139.3 | 30.0 | Policy 3.1(b): undrawn committed balances at 50% |
| R1 | point in time, policy measure: each quarter on the archive of that quarter-end, or on the customer master's group code as it stood (both land here) | 154.9 | **15.0** | LMS-03 2.3: the projection is for the group as constituted at the projection date, from that group's exposure at each quarter-end |
| R1c | the 30 Sep archive read with relationship periods at each quarter-end, active records only | 159.7 | 10.2 | same; ended relationships are INACTIVE records the reading drops, so the disposal leaves and the acquisition never enters |
| R2 | acquisition restated, disposal left in (pro forma for the purchase only) | 143.4 | 26.6 | LMS-03 2.3: Norbeck is not in the group at the projection date |
| Answer | every quarter on the 30 September 2026 membership | **148.1** | **21.8** | |

- **Rule-violation cells (not rungs, asserted distinct):** no projection 23.5 (+7.8 per cent); drawn
  balances only on the restated history 30.0; the request at the revolver weight 30.0. The average
  quarterly change instead of the least-squares slope converges on the answer for B1 (148.2, 21.8):
  C1 on that axis.
- **Satisfying to stop at.** R0 is the balance column a loan extract offers; R1 is the disciplined
  history (no look-ahead, the bank's own archive, the customer master agreeing with it); R2 is the
  pro forma a credit analyst does for an acquisition.
- **Direction.** Point in time under-approves where a group bought a borrower (Kelderby, Meridale,
  Brauneck, Pellow) and over-approves where it sold one (Corrin: 25.0 against 16.7).
- **Thinnest margin:** the no-projection cell, 23.5 against 21.8 (1.7m). Rungs proper sit 30 per cent
  or more away.
- **The decisive move against the seven properties.** 1 no sentence states it (2.3 defines the group,
  not the history); 2 no corpus; 3 no arithmetic symptom: every point-in-time history reconciles to
  its own archive and to the customer master's codes; 4 not a row predicate: it needs each borrower's
  group at another date, behind a join; 5 enumeration is a resolution of the whole hierarchy twice;
  6 the membership changes are dated, but the dates move membership, not the outcome series, and the
  event-study reflex finds a jump it reads as growth; 7 survives deletion (nothing is wrong).

## Stump or fork

LMS-03 2.2 and 2.3 file the estimand: the group as constituted at the projection date, its exposure at
each of the five quarter-ends, the least-squares slope. The point-in-time history is not that group's
exposure at those dates, it is a different group's, so the reading is named by a shipped sentence
without the sentence naming the construction. The alternatives are ruled out by the data's own
structure: a history that mixes membership with exposure books an acquisition as quarter-on-quarter
growth that no borrower drew.

## Layers

- **Layer 1:** three booking systems (core lending with two booking entities and a late Dublin
  delivery, the custodian's positions with gaps in issuer LEIs, the trading risk system's netting sets
  in thousands with a rerun close and CSA collateral in units), Treasury FX in units per pound, and the
  GLEIF golden copy archived quarterly with its real behaviour (merged LEIs still keyed in the customer
  master, lapsed entity registrations, subsidiaries reporting only a direct parent, international
  branches, fund-management links, reporting exceptions).
- **Layer 2:** the history behind a projection must describe the population the projection is for;
  the point-in-time build, the right discipline for most histories, is wrong here.

## Closure table (22 axes)

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | committed and uncommitted facilities on the extracts, investment positions, netting sets; pinned by Policy 3.1 |
| 2 | Unit | obligor group by accounting consolidation, branches to head office, funds alone; Policy 2.1 to 2.6 |
| 3 | Attribution window | quarter-end extracts; Policy 3.3 |
| 4 | As-of dating | membership at the projection date for every quarter: LMS-03 2.3, the decisive axis (C4: R1, R1c, R2 are named wrong cells) |
| 5 | Version basis | one extract per quarter-end plus the late Dublin file (extract log); the R2 rerun for the 30 Sep close (field reference); the 30 Sep archive for membership |
| 6 | Denominator | house limit from the register, keyed by ultimate parent LEI |
| 7 | Weighting | sums; none |
| 8 | Window length | five quarter-ends, LMS-03 2.2 |
| 9 | Inclusivity | "does not exceed": no group lands on its limit (room at least 0.15 of a GBP 0.1m step from the edge, asserted) |
| 10 | Rounding path | unrounded pounds, rounding only on report (LMS-03 2.4); approvals floor to GBP 0.1m steps (3.2); every graded figure at least GBP 10,000 inside its bin (asserted) |
| 11 | Tie-break | utilisation order gaps at least 0.3 points (asserted) |
| 12 | Maturity | none; every quarter is closed |
| 13 | Order of operations | per netting set: MTM less cash collateral, floored at nil (Policy 3.1(d)); FX before summing (linear) |
| 14 | Row order | irrelevant (sums) |
| 15 | Duplicate resolution | migration overlap: receiving facility is the record (field reference); twin tranches are two facilities (distinct refs) |
| 16 | Identity | LEI; merged LEI to successor (Policy 2.5); blank issuer LEI through the ISIN file |
| 17 | Netting | netting sets not offset (Policy 3.1(d)) |
| 18 | Units | derivatives in GBP thousands, collateral in units (field reference) |
| 19 | Code semantics | committed flag, facility types, relationship types and statuses (Policy, field reference) |
| 20 | Integerisation | floor to GBP 0.1m, capped at the request (LMS-03 3.2) |
| 21 | Clause scope | the 50% weight applies to undrawn committed balances and to new revolvers (Policy 3.1(b), LMS-03 3.1) |
| 22 | Forward window | one quarter, the least-squares slope; C1 with the average-change reading on B1 |

## Ask sheet (supplemental-stumping)

Main call row population: the five facilities of Kelderby Group plc, Kelderby Facilities Ltd, Kelderby
Engineering Ltd and Tarrant Hydraulics Ltd across five quarter-ends (25 rows), their GLEIF records.
Zero Dublin, migration, non-sterling, uncommitted, late-file, securities or derivative rows inside it,
and every main entity ISSUED with PUBLISHED relationship records in every archive (asserted).

| Row (ask) | In the decision | Primary device | Hazards | Stops (projected / approvable, asserted) | Use |
|---|---|---|---|---|---|
| B2 Meridale | the check beside the call | June booking migration London to Dublin: both rows on the 30 Jun extract, receiving row carries migrated_from (D1) | twin tranches a lazy dedup collapses (over-clean); EUR in units per pound (D3); construction (bought Norbeck) | migration twice 75.0/9.9; twins collapsed 68.5/12.0; FX multiplied 78.2/6.8; no FX 75.8/9.2; point in time 78.5/6.5; **golden 73.7/11.2** | committee sizes the Meridale loan |
| B3 Brauneck | same | Dublin 31 Dec 2025 extract delivered late, in its own file (D4 absent channel) | London branch reached only through IS_INTERNATIONAL_BRANCH_OF; EUR rate; construction (bought Hollins Gear) | late file out 87.6/12.3; branch alone 56.6/20.0; FX multiplied 96.1/3.9; point in time 88.7/11.3; **golden 83.7/16.2** | same |
| B4 Corrin | same | merged Corrin Warehousing still keyed in the customer master (D7) | derivatives in GBP thousands (D3); cash CSA only, gilts ignored; construction (sold Corrin Cold Chain) | merged alone 63.6/25.0; MTM as pounds 80.1/19.7; collateral ignored 83.7/12.6; gilts deducted 80.7/18.6; point in time 77.5/25.0; **golden 81.6/16.7** | same |
| B5 Pellow | same | the bakery reports only its direct parent, a lapsed holding company (D7) | lapsed holdco dropped; blank issuer LEI on a 2031 bond (ISIN file); construction (bought Fenwick) | ultimate join only 34.0/14.0; lapsed dropped 34.0/14.0; blank LEI dropped 70.6/14.0; point in time 77.4/7.6; **golden 74.4/10.5** | same |
| B6 Stannard | same | the 30 Sep close rerun (R2 sheet is the record) (D2) | derivatives in thousands; funds grouped under the manager on the customer master; revolver request at 50% | first run 20.5/18.9; MTM as pounds 19.9/20.0; funds under manager 77.9/0.0; revolver at full weight 21.5/8.5; **golden 21.5/17.0** | same |
| Book split at 30 Sep | the exposure the check stands on | carries every device above that lives at 30 Sep | | moves with each device | committee reads what the exposure is made of |
| Chart | the call at a glance | the construction (order and bars) | | point in time reorders the bars | committee pack |

**Pair arithmetic, stated plainly.** The point-in-time history moves 26 of the 72 row figures (the
earlier quarter-ends, projections, utilisations and approvals of the five groups that changed shape);
the other 46 (the 30 September book splits and totals and the Stannard row) rest on the devices alone
(counted by script). A response that misses the call but handles every device keeps those 46; one
that lands the call keeps whatever devices it handles. The design therefore leans on the main ladder
keeping both top responses off the call, with the devices as margin, and the device layer is the
first place a hardening goes if a round shows high ask leakage. The solver round measures it.

## Shape and criteria

Shape 01 (ranked list under a cap): six requests ranked by projected utilisation against the 100 per
cent line, each with 12 figures (four book parts, five quarter-ends, projected, utilisation,
approvable) = 72, plus the order, the call, and the chart's five named parts (bars in order, the
limit line at its value, the annotation, the title, the file) and two files: well past 25.

## Prompt

`prompt.md`, 987 characters, 160 words, question-first, voice-check clean (no calcified carrier, no
roll call, no input file name, no method or trap word). Deliverables `limit_check_2026-11-04.xlsx` and
`projected_utilisation_2026Q4.png`.

## Realism debts

- Every agenda group but Stannard changed shape inside the year. Acquisitive groups are the ones
  that come for term loans, and the background book carries 26 more ownership changes and 18 legal
  mergers, so the agenda is not marked out.
- The least-squares projection is a simple early-warning metric; it is the bank's filed standard.

## Stopping rule

Two consecutive solver rounds that land 21.8 by restating the history file the architecture as
spent at the decisive rung (re-root, not harden). A round that lands on 15.0, 10.2 or 26.6 and keeps
most ask figures licenses one hardening of the device layer only.

## Tried and rejected

- Seed as written (5/10/40 group test on N-PORT holdings, relationship types, LAPSED, successors,
  ISIN fallback decide): rule application and data semantics as the decisive step; pairing taken by
  task445 (quantitative-finance with etl).
- Pro forma borrowing base for a fund-finance revolver (concentration caps re-struck on the pool the
  advance buys): the borrowing base is a filed formula; a coding solver re-runs its base function on
  the pro forma pool and bisects the advance, so the decisive step is executing stated definitions
  (dead shape: a committed figure that is the output of a filed formula).
- Self-referencing allocation cap for an allocator funding a new fund mandate (the cap's denominator
  grows with the allocation): honest domain is Quantitative Finance (blocked pairing), and a solver
  who writes the post-funding inequality solves it.
- Quarter-end window dressing of money-fund repo with foreign banks: the only exact construction lowers
  a bank group's exposure at quarter-ends, so every decision it can carry either games a quarter-end
  test or needs a seasonal estimator with open forks.
- Default dependence within obligor groups for a pool tail loss (members default together): the same
  insight as task229 (the independent unit sits behind a shared parent node).
- Linkage-error propagation for holdings without LEIs (gold-standard review sample): calibration form
  banned against task228, estimator forks.
