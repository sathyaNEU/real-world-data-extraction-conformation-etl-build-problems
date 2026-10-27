# task464 design note: the 2027 outpatient capacity register (architecture 3)

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first: architecture 1
(the Wendlemere building emissions slate) was sent back by the determinism judge, architecture 2 (placing the
retiring reading test's scores on the new scale) was solved on the portal because its decisive step was
psychometrics' own named method for the deciding quantity, and architecture 3 is drawn afresh in the ETL
objective with the field's method moved into the default path.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task464.json` (architecture 3, architectures 1 and 2 in `lineage`),
  registered 2026-10-27, guard WARN only, 299 cards validated. The one WARN is `repeat.question_form`: how-many
  also opens task141's prompt, two builds back. Answered: the decision is a count of weekly treatment slots, so
  how-many is the form the decision gives (the guard's own fix line), and task141 counted re-arrests at a horizon.
- **Pairing:** healthcare-delivery-health-economics / payment-claims-health-plan-analytics, objective Data
  Extraction & Conformation (ETL), prompt shape 07 (grid of cells: each area cell).
- **Shape 07 against the two the taxonomy calls native for ETL.** Shapes 03 and 15 both announce the decisive
  step: a bridge between totals makes its own line items name the step from attested stations to deliverable
  positions, and fields-to-one-schema makes each field's transform a filed instruction. A grid of twelve area
  cells grades the same conformation without naming how any field is built.
- **Niche:** a nonprofit Medicaid managed care plan's network unit conforming one capacity dataset for its 2027
  outpatient dialysis and infusion contracts, out of the provider directory, the state licence file, the staffing
  rosters and four years of timed treatment encounters.
- **Strategy:** `binding_constraint`, gap `population`, Gate G `binding_constraint`, generators `G8`, decisive
  rule filed `false`, official decoy `false`, validated decoy `false`, `stump_class: analytical`.
- **Data-native sentence.** A treatment encounter is recorded with the clock time the chair was occupied, because
  infusion and dialysis are billed in timed units, so this pack carries four years of a site's own service
  intervals; the greatest number of them that have ever run together at a site is a measurement of how many of
  its positions can be worked at one time, and nothing else in the pack measures that, because a directory
  attestation and a licence both count the positions that exist rather than the positions that can run.
- **Sources, one line each.** `guard.py mechanisms --objective etl` was read before drawing. task487 (emissions
  inventory ETL) spends the insight that a reported total is assembled from sources at different vintages, which
  this build does not use. task485 (census register ETL) spends coverage of a register against an independent
  enumeration, which is a completeness question rather than a capacity one. task137, the nearest build in this
  client domain, spends demand censored by refusals at a capacity-bound service, which is the mirror of this
  build and is about demand, not about how much a site can deliver. task69 spends overlap between the
  contributions of a capped set's members, between units; this build's overlap is inside one unit, between its
  own positions. Nearest driver on file is 0.08 (task479, lineage).
- **Fiction.** An unnamed state of the United States, USD, a nonprofit Medicaid managed care plan contracting
  outpatient dialysis and infusion capacity, forum `operations_desk`, forcing event a purchase order or contract,
  org family `nonprofit_or_charity`. People drawn with `guard.py names`: Katherine Dalton, Nicholas Clay.
- **Deliverables:** `outpatient_capacity_2027.csv` (one row per contracted site) and `area_capacity_2027.xlsx`
  (the twelve service areas against the adequacy standard, with the chart).
- **The call faces forward:** the 2027 network year is not yet contracted at the as-of date.

## Default path

A competent analyst builds this without hesitating, from the prompt's words and the files' grain.

1. Read `provider_directory_*.csv` and keep the outpatient dialysis and infusion sites with a 2027 contract
   intent, resolving each site's identifier through the directory's own attestation cycles (a site appears once
   per cycle, the latest row current).
2. Join the state licence file on the service address to confirm each site is licensed and to carry its licensed
   station count, reconciling the corporate-entity rows against the service-address rows.
3. Read the staffing rosters and count each site's rostered treatment sessions a week by position.
4. Conform the two encounter layouts across the clearinghouse change and aggregate four years of encounters to
   each site's treatments a week, to measure realised volume.
5. Take each site's capacity as its attested stations times its rostered sessions a week, times the treatments a
   position runs in a session.
6. Reconcile the product against realised volume and against the adequacy contract's utilisation standard: the
   ratio sits in a plausible band at most sites, and the sites where it does not are the ones the plan already
   knows are growing.
7. Roll the sites up to the twelve service areas and compare each area against the standard.

Ends on: a 2027 network capacity 1.15 times the golden (1.129 to 1.150 over the eight stage-2 prototype seeds),
with three of the twelve service areas filed above the adequacy standard that are below it.

Golden: the same conformation with each site's deliverable positions set to the greatest number of its own
treatments that have ever run at one time, which at about a third of the sites is several short of the stations
it attests and the licence lists.

## Stump sentence

The default path multiplies each site's attested stations by its rostered sessions, ties the product to realised
volume and the adequacy standard, and files a 2027 network capacity 1.15 times the golden with three of the
twelve service areas wrongly above the standard, because the stations a site attests are the positions it has, not the positions
it can work at one time, and at about a third of the sites no hour in four years of its own timed encounters has
ever had more than a fixed number of treatments running together.

## Three rules

Task type: payment-claims-health-plan-analytics, in its provider network capacity and adequacy form: conforming
one capacity dataset for a contract year out of a provider directory, a state licence register, staffing rosters
and a timed encounter extract, which is the card's subdomain and serves Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each contracted site's deliverable treatment capacity for the 2027 network
year, which health plan analytics builds as the positions a site can work times its staffed sessions and tests
against the utilisation standard the adequacy contract sets; put a warehouse's nouns in and there is no staffed
session, no treatment interval and no position a patient occupies for a fixed span, so the quantity disappears.

Swap: "how many pallet positions the 2027 network holds, from the yard directory, the operating permit, the shift
rosters and four years of timed putaway records" keeps the sentence and loses the move: a pallet position is
occupied by a pallet and nothing stops every position being full at once, so there is no ceiling below the count
of positions and the conformation is a join.

Layer 1: a directory refreshed on each site's own attestation cycle; licence rows at both the corporate entity
and the service address; two encounter layouts across a clearinghouse change (one carries start and stop, the
other start and a duration in minutes); treatment start and stop times in local clock with no offset on one feed;
rosters by position rather than by named staff; sites that moved address and kept their identifier; a group
practice billing three sites under one tax identifier; cancelled and no-show encounters carried with no stop time.
Each is written by the system that produces it, none is placed to be caught, and each is asserted neutral on the
call.

Layer 2: allocation under a constraint (`own:the ceiling the overlaps fix`): the call flips on reading each site's
deliverable positions off the overlaps of its own service intervals rather than off the station count the
directory and the licence carry.

Decisive step: setting each site's deliverable positions to the greatest number of its own treatments ever running
concurrently, recovered by sweeping four years of its service intervals, rather than to the stations it attests or
is licensed for; in the field's words, measuring the site's effective chair capacity instead of taking its
attested chair count.

Not semantics: every field, code, unit and definition read correctly leaves the easy route on the wrong answer.
The attested station count is read correctly as the stations the site attests and is true of the site; the licence
count is read correctly as the stations the state licensed; no field, label, dictionary entry or definition in the
pack names deliverable positions, effective capacity or a ceiling, so there is no field whose correct reading
supplies the figure. The figure has to be constructed from the encounters' overlaps.

Not rule application: the adequacy contract files the population, the window, the unit and the standard, and no
rule or procedure in the pack says how a site's deliverable positions are determined; executing every filed rule
with the attested station count files the wrong total, so the step no rule performs is the reconstruction of the
positions.

Analyst test: a strong analyst who resolves the directory's attestation cycles, reconciles the licence file's two
grains, conforms both encounter layouts and counts the rostered sessions correctly takes attested stations times
rostered sessions, reconciles it against realised volume and the utilisation standard, and files a network
capacity 1.15 times the golden (1.129 to 1.150 over the eight stage-2 prototype seeds) with three of the twelve
service areas wrongly above the standard. Executed in `checks.py` on the generator's clean truth at stage 3.

Estimand: the adequacy contract's capacity section, filed in the contract document at authority: for each site
the plan intends to contract for the 2027 network year, the treatment slots a week the site can deliver, counted
as its deliverable treatment positions times the treatment sessions its roster staffs in a week times the
treatments a position runs in a session; and for each of the twelve service areas the sum over its sites against
the standard. It fixes the population, the window, the unit and the comparison, and says nothing about how a
site's deliverable positions are found.

No decoy: nothing is planted to be caught. The directory's attestation is a true attestation of the stations the
site has, the licence file is a true licence, no memo, briefing, draft or stakeholder figure argues for a method
or for a capacity number, and no file counts or ranks the areas against the standard.

No certified replay: no certified or published figure reproduces a method. The capacity report that ships as the
context artifact is the prior year's, states its own basis and is ruled out by the contract's window, and no table
of site capacities or area totals ships.

Lesson: capacity assembled from the positions a unit reports is an upper bound, not a measurement, and where the
unit's own service record is timed, the positions it can work at one time is measurable and smaller; no build on
file teaches a ceiling recovered from a unit's own overlaps (task69 overlaps the contributions of different
members of a capped set, task137 censors demand at a capacity bound).

## Readability screen
Seven tests per rung (`stumping` 2.1), verdict last. The decisive rung is the concurrency ceiling and it
comes out `silent`. Measured on the stage-2 prototype
(`generator/ladder_prototype.py`, eight seeds 464 to 7464).

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | 7 dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 attested stations | yes, the directory's attestation names the station count | yes, one column | yes, the first construction anyone builds | no control scores it | no sweep refutes it | yes, one product | no | readable |
| R1 the state licence's station count | yes, the licence names the licensed stations | yes, one column after one join | yes, the reflex of an analyst who distrusts a self-attestation | the 2026 state filing's station column ties to it | the licence's two grains are a battery finding | yes, one product | no | readable |
| R2 the revealed volume ceiling | no sentence names it | no, it is built from the encounter record | yes, revealed throughput is a capacity planner's second move | no control scores it | the battery's volume-against-capacity reconciliation points at it | close to it, one maximum over a group-by on site and week | no | readable |
| R3 the concurrency ceiling **(decisive)** | no: nothing in the pack names deliverable positions, effective capacity, a ceiling or an overlap, and the contract files the unit without saying how positions are found | no: the encounter record carries no session, chair, shift or position key, so there is no row predicate and no header-found join, and the plant reason ships nowhere | no (argued below) | no control, corpus or published figure scores any basis; the 2026 state filing constructs no capacity figure at all | no: the battery's five sweeps find the attestation cycles, the licence grains and the two layouts, and its volume-against-capacity tie passes on every basis, apparent utilisation on attested stations running 0.389 to 0.964 with no site over 1 | no: a maximum over about 1.1 million reconstructed intervals, and corr(the correction an area takes, the area's own size) is -0.34 to -0.56 so no rescaling of a shipped column reaches it | no: the timed encounter extract is the same file the standard's demand side needs | silent |

**Test 3, the one to watch, argued.** A capacity planner handed timed service intervals may sweep them for
occupancy unsent, so this row is where the screen can be wrong. Three things keep it silent and all three are
properties of the pack rather than of the wording.

1. **There is no column whose maximum is the answer and no group-by on a shipped key that returns it.** The
   encounters arrive in two layouts across the clearinghouse change, 2023 and 2024 carrying a start and a stop
   and 2025 and 2026 carrying a start and a duration in minutes, and neither layout carries a session, chair,
   shift or position identifier. The intervals have to be reconstructed from both layouts before anything can
   be swept, and a count of treatments per site and day returns the site's daily throughput, which is two to
   three times its positions.
2. **The easy route's own output does not ask for a second measurement of positions.** The default path's
   step 6 ties the attested product to realised volume against the utilisation standard and reports a
   plausible band everywhere: apparent utilisation on attested stations is 0.389 to 0.964 across the forty
   sites with the plant-constrained sites at 0.41 to 0.74, so nothing reads as impossible and nothing points
   at a site whose stations cannot all run.
3. **The field's own method for this quantity sits at rung 0, not at the top** (`stumping` 1.1b). Health plan
   network analytics builds deliverable capacity as stations times staffed sessions; the decisive step is the
   recognition that this network violates that method's precondition at a third of its sites. The note's
   `Domain test:` and `Decisive step:` lines name no method in common, which is the gate `precut.py` runs on
   the same point.

**Test 7, answered by naming the other use.** Delete the decisive step from the design and the pack still
carries four years of timed treatment encounters, because the adequacy standard's demand side is the area's
2026 treatments a week and that is the only file that holds them, and because infusion and dialysis are
billed in timed units so a plan's encounter extract carries the service start and its stop or its duration
whatever anyone intends to do with them. The organ is multi-purpose: the same rows supply the 2026 realised
volume, the growth test's base and the out-of-network comparison in ask A. Its presence carries no
information about the decisive step.

## Semantic fork table
One row per term of the main ask and per convention the main computation needs. `Ruled out by` quotes a
shipped sentence, or names the construction that makes the readings converge (C1) with the assertion that
carries it. Every id is asserted in `generator/checks.py`. The critical row is SF1 and it is closed on the
data, never by a filed sentence saying how to compute a ceiling: a sentence filing the method would make the
decisive step rule application, which the client's rule 3 bans.

| id | Term or convention | Golden reading | Alternatives, and the call under each | Ruled out by |
|---|---|---|---|---|
| SF1 | a site's deliverable positions | the greatest number of the site's own treatments running at one time over the record | the record maximum; each year's maximum; each month's maximum; a high percentile (90th, 95th, 99th) of concurrency over treating hours. Same call under all four | C1 on the data, a hard plateau: at 40 of 40 sites the record maximum, all 4 yearly maxima and all 48 monthly maxima equal the same integer, and one more than that integer never runs. The site's treating hours sit at exactly that integer for 0.155 to 0.324 of their length, so the smallest quantile returning it is at most 0.845 and the 90th, 95th and 99th percentiles all return it. A full session holds every position occupied for at least 94 minutes. Asserted per site as `SF1`: the four readings equal, and zero time above |
| SF2 | the interval convention | half-open, start inclusive and stop exclusive | closed, or stop inclusive and start exclusive. Same call | C1: every position carries a strictly positive turnover between its successive treatments and no start time at a site coincides with any stop time at that site, so the overlap count is identical under every endpoint convention. Asserted as `SF2`: the minimum turnover in minutes is above zero and the count of coincident endpoints per site is zero |
| SF3 | cancelled and no-show encounters | no interval, because the record carries no stop time and no duration for them | treat them as instantaneous, or drop them. Same call | C1: no interval is constructible under any reading, and `SF3` asserts the ceiling and all twelve area verdicts unchanged whether they are dropped or read as instantaneous |
| SF4 | the local clock with no offset on one feed | the site's own local clock | a site-level offset applied, or the feed read as coordinated time | C1: an offset cancels inside a site because concurrency is a within-site overlap count, and `SF4` asserts the ceiling unchanged under any site-level offset and across the autumn fall-back hour, no site holding an interval that spans the repeated hour |
| SF5 | a treatment session | the contract's capacity section: a scheduled block in which each staffed position runs its treatments for that block | a shift, a day, a chair-day | the contract's sentence, and the roster reports sessions staffed a week as an integer per site, so no derivation of the count is needed. Asserted as `SF5`: the roster's weekly session count is one value per site at the as-of date |
| SF6 | a week | the contract: one 52nd of the contract year | 52.143 weeks, or the weeks in which the site treated | the contract's sentence; `SF6` asserts the twelve area verdicts identical under 52 and under 52.143, the 0.3 per cent difference sitting inside every margin (worst 6.04 per cent) |
| SF7 | the attestation cycle current at the as-of date | the site's latest cycle row at or before the as-of date | the latest row in the file, the latest row of the current calendar year | C1: every site's latest cycle row precedes the as-of date by 30 days or more and no site carries two rows in one cycle, so every reading selects the same row. Asserted as `SF7` on the row counts and the figure |
| SF8 | the licence file's two grains | the service-address rows | the corporate-entity rows | C1: a corporate row's station count equals the sum of its service-address rows, so either grain returns the same count per site. Asserted as `SF8` by equality and by row counts |
| SF9 | the population | the sites the plan intends to contract for the 2027 network year, from the directory's recorded intent | every site in the directory, every licensed site in the twelve areas, the 2026 contracted set | the contract's capacity section files the population; C1, the intent is recorded once per site and no site changes it inside the window. Asserted as `SF9` on the site count |
| SF10 | the treatments a position runs in a session | the contract's per-modality figure | a site-level figure read off the encounters | the contract's sentence; `SF10` asserts no site carries both modalities, so the figure is unambiguous per site |
| SF11 | projected 2027 demand | the area's 2026 contract-year treatments a week grown by the area's enrolment growth factor | the 2026 calendar year, the last four quarters, a four-year trend | the contract files the base, the window and the factor's source; `SF11` asserts the 2026 contract year and calendar 2026 select the same encounters |
| SF12 | the standard's direction and inclusivity | capacity at or above the required figure | strictly above | C1: no area's capacity lies within 6 per cent of its required figure on any of the four bases (worst measured 6.04 per cent of required over eight seeds), so strict and non-strict readings agree. Asserted as `SF12` |
| SF13 | the rounding path | the required figure to a whole treatment slot, once, at the end | per site then summed, or to the nearest ten | the asking sentence states whole numbers; `SF13` asserts no required figure lies within 0.05 of a half treatment (measured 0.010 to 0.133, the generator redrawing under 0.05) and that capacities are counts |
| SF14 | a site's service area | the directory's recorded area for the site at the as-of date | the area of the address the site held earlier | C1: no site crosses an area boundary inside the window, including the sites that moved address and kept their identifier. Asserted as `SF14` |
| SF15 | the look-back for the ceiling | the whole four-year record | the most recent 24 months, the most recent 12 months | C1 through SF1's plateau: every month's maximum equals the site's positions, so any sub-window returns the same integer. Asserted as `SF15` |
| SF16 | the key that identifies a site | the directory's own site identifier, carried on every encounter as the service facility | the tax identifier, which three sites of one group practice share; the service address | the contract files the unit as the site, and the tax-identifier reading merges those three sites into one and lifts their joint ceiling, a named wrong cell. Asserted as `SF16`: the tax-identifier reading changes the network total, and the directory's site identifier is one to one with a site |
| SF17 | weekly treatment slots | deliverable positions times sessions staffed a week times the treatments a position runs in a session | realised treatments a week; the slots the 2027 roster offers | the contract's capacity section files the unit and its inputs and says nothing about how positions are found, which is the WHAT and not the HOW (`determinism-check` section 1). Asserted as `SF17` |

## Ladder
Four rungs, measured on the stage-2 prototype over eight seeds (464, 1464, 2464, 3464, 4464, 5464, 6464,
7464); `generator/ladder_prototype.py` builds every rung by construction and lets the seed decide texture
only. The area codes below are the prototype's; the cut pack names them.

| Rung | What it does | Network total over the golden | Areas short of 12 | Its own short set (prototype seed 464) | Worth on the graded quantity |
|---|---|---|---|---|---|
| R0 | the default path: attested stations times sessions staffed a week times the modality figure | 1.1286 to 1.1500 | 3 | A04 A09 A12 | 0.000, by definition |
| R1 | the state licence's station count in place of the directory's attestation, for an analyst who distrusts a self-attestation | 1.2098 to 1.2286 | 2 | A04 A09 | -0.49 to -0.69, it walks away from the golden |
| R2 | the revealed volume ceiling: each site's positions taken as its busiest week's treatments over its sessions staffed a week, which carries through to the busiest week's treatments as the site's weekly slots | 0.8855 to 0.9209 | 8 | A01 A03 A04 A06 A09 A10 A11 A12 | +1.55 to +1.89, it overshoots the correction |
| R3 | the concurrency ceiling, the golden: positions set to the greatest number of the site's own treatments ever running at one time | 1.0000 | 6 | A02 A04 A07 A09 A11 A12 | +1.000 |

**Position and dominance.** The golden is bracketed, which is the shape `stumping` Part 3 asks for: R1 and R0
overshoot it, R2 undershoots it, and the decisive move reverses R2 upward. The four totals are strictly
ordered R1 > R0 > R3 > R2 on every seed and the closest pair sits 7.34 to 8.92 per cent of the golden apart,
clear of the 6 per cent floor. Every rung names its own total and its own short set on every seed.

**Each rung's own grid of wrong area cells**, against the golden's twelve verdicts:

| Rung | Golden-short areas it clears | Golden-clear areas it calls short | Area cells wrong of 12 |
|---|---|---|---|
| R0 | 3 (A02 A07 A11, the flip set) | 0 | 3 |
| R1 | 4 (A02 A07 A11 A12) | 0 | 4 |
| R2 | 2 (A02 A07) | 4 (A01 A03 A06 A10) | 6 |
| R3 | - | - | 0 |

This is the defect the first prototype of the arithmetic carried, and the repair. There the volume ceiling sat uniformly below the
concurrency ceiling, so R2 named exactly the golden's six short areas and a solver stopped at R2 got the
whole area grid right and only the network total wrong. Here the busiest week over four years can sit above
the current roster's product as well as below it, because six to nine sites of forty closed a third shift or
a sixth day between 2023 and 2026 and their busiest week came from the larger roster, so R2 now misses two of
the golden's short areas and calls four of its clear areas short: six of twelve cells wrong on every seed,
and the same six-of-twelve headline count as the golden under a different set, so stopping at R2 is
satisfying and wrong.

**Margins.** All 48 area-rung cells clear 6 per cent of their area's required figure on every seed, the worst
measured at 6.04 to 6.13 per cent (the flip areas on the golden reading, which is where the floor is meant to
bind). The flip set is three of twelve on every seed.

**The grid of partial applications.** The decisive step applies site by site, so the grid is the power set of
the plant-constrained sites inside each area: 39 to 47 cells across the twelve areas. Two properties are
measured on every seed. No partial application reproduces a golden-short area's verdict, because each
constrained site inside a flip area is sized to carry at least a seventh of its area's positions, so leaving
any one of them on attested stations puts the area back above the standard. And the nearest partial cell to
its area's line sits 6.03 to 6.11 per cent away, so every cell of the grid is a named wrong answer outside
the floor rather than a near miss. The network total falls strictly as more sites take the ceiling, so no
proper subset reproduces the golden's total either.

**The arithmetic of `dataset-generation` section 6, on paper.** One live degree of freedom would hold no
ladder, so the graded quantity carries three: which station count a site's positions come from, whether the
demand side is realised or projected, and which of the twelve areas the comparison is made in. The fork grid
is the cross product of the four station bases and the two demand bases, eight cells; the realised-demand
column cannot fail any area at all (realised volume is bounded by true capacity, so 1.15 times realised is
always under the ceiling capacity) and is the first death recorded in `## Tried and rejected`. Each of the
remaining cells is mapped in `## Closure table` and in `generator/checks.py` to the shipped sentence it
violates. Three further partial-path cells are named rather than swept: sweeping only the start-and-stop
layout returns a ceiling below the site's positions at the sites whose later years sit in the duration
layout, so it files a total below the golden and extra short areas; reading the duration column as hours
makes every one of a site's intervals overlap and files a ceiling above the site's attested stations, which
the file itself refutes; and ignoring the modality figure scales the infusion sites by a half.

**Stacking.** Three mechanisms from different gaps sit under this call: the population gap carries the
decisive rung (which positions a site can work), the time gap carries rung 1 and the demand side (a licence
cycle and an enrolment projection against a contract year), and the objective gap carries rung 2 (a revealed
throughput read as a capacity). The decisive gap is not rung 1's.

## Closure table
The 22 axes of `determinism-check/references/forcing-the-answer.md` Part 1, one row per axis number, axes
that cannot move the answer today included.

| # | Axis | The reading this build takes | Closure move |
|---|---|---|---|
| 1 | Population | the sites with a recorded 2027 contract intent at the as-of date, the 2027 network year not yet contracted | filed in the contract's capacity section, which states that the set is the sites the plan intends to contract and not the sites it contracted for 2026; C1 through SF9 and SF7 |
| 2 | Unit of account | the site, not the corporate entity and not the tax identifier | filed by the contract's "for each site"; C4, the tax-identifier reading merges the group practice's three sites and files a named wrong total (SF16) |
| 3 | Attribution window | the 2026 contract year for demand, the four-year record for the ceiling | the contract files the demand window; C1 for the ceiling through SF1's plateau and SF15, every sub-window returning the same integer |
| 4 | As-of dating | one filed as-of date; the roster current at it, static across the window | filed as-of date in the contract; SF7 puts every latest attestation row 30 days or more before it |
| 5 | Version basis | the latest accepted licence amendment per site | filed in the licence register's own status column as plain words; C1, no site carries two amendments inside the window |
| 6 | Denominator | capacity against 1.15 times projected demand, demand being the area's 2026 treatments a week | filed in the contract in the standard's own words (SF11, SF17) |
| 7 | Weighting | none: an area's figure is the sum over its sites | cannot move the answer; no weighting choice exists, asserted as a sum identity per area |
| 8 | Window length | the ceiling's four-year look-back | C1, measured: 12, 24 and 48 months return the same integer at all 40 sites (SF15) |
| 9 | Boundary inclusivity | at or above the required figure | C1, no area within 6 per cent of its line on any of the four bases, worst 6.04 per cent (SF12) |
| 10 | Rounding path | the required figure to a whole treatment slot, once, at the end | the asking sentence; SF13 keeps every required figure 0.05 or more from a half treatment, the generator redrawing otherwise |
| 11 | Tie-break | none: the call is a count and a grid, not a ranking | cannot move the answer; asserted that no two areas share a required figure and no area's capacity equals its required figure |
| 12 | Maturity and censoring | the 2026 contract year complete at the as-of date, the extract pulled after the filing run-out | filed run-out in the contract's reporting section; asserted that no 2026 encounter carries a receipt date after the extract date |
| 13 | Order of operations | positions, then sessions, then the modality figure, then the area sum, then the standard | the steps commute (multiplication and summation), asserted; the only non-commuting step is rounding, closed at axis 10 |
| 14 | Row order | the ceiling is a maximum over a set and the totals are sums | C1, asserted invariant over permutations of the encounter tables |
| 15 | Duplicate resolution | the latest accepted claim per encounter, the superseded line carrying its replacement reference | C1 on the main path: asserted zero resubmission pairs inside the 2027 contract-intent sites' own encounters, the pairs sitting on non-contract sites where ask A reads them |
| 16 | Identity normalisation | the directory's site identifier, joined to the licence register on the service address and to the encounters on the service facility | C4, the raw tax-identifier join merges three sites and is mapped to the contract's unit sentence (SF16); the crosswalk is the directory's own |
| 17 | Netting against gross | none: capacity and demand are gross counts | cannot move the answer; nothing nets, asserted |
| 18 | Dimensional units | treatments, positions, sessions, minutes; the duration layout is minutes | C4, reading the duration as hours makes every one of a site's intervals overlap and files a ceiling above its attested stations, which the file refutes; asserted as a named wrong cell |
| 19 | Code and status semantics | the encounter status (completed, cancelled, no show) and the directory's contract intent, both plain words, no dictionary shipping | the governing contract defines the intent; SF3 makes the status unable to move the ceiling under any reading; never the stump |
| 20 | Integerisation | positions are whole by construction, a count of concurrent treatments; slots are counts | C1 by construction: no floor, round or remainder choice exists on the graded quantity, and the one rounded figure is closed at axis 10 |
| 21 | Clause scope | the contract's capacity section governs the 2027 network year and the 2027 contract-intent sites | filed scope in the section's own first sentence; the 2026 state filing states its own year and site set, differing by six sites or more |
| 22 | Forward window contents | the 2027 network year is not yet contracted | the plan's 2027 enrolment projection by service area ships as the driver file for the uncovered span; nothing else about 2027 is needed, and no 2027 treatment is in the pack |

## Literal reader
A reader who executes `prompt.txt`, the adequacy contract's capacity section and the licence register's own
status words word for word, inferring nothing the files do not say, reaches the golden: the contract fixes the
population, the unit, the window and the standard and says nothing about how a site's deliverable positions
are found, so the only step left open is the measurement of those positions, and every reading of a site's
own record returns the same integer (SF1's plateau, 40 of 40 sites). Where the text is silent the options were
enumerated in `## Semantic fork table`, all 17 rows, and each either returns the golden or violates a quotable
shipped sentence; no row is closed by this note or by the write-up, and the easy answer comes from an easy
method on the same literal estimand (attested stations in place of a measurement) rather than from another
reading.

## Oracles
Every control, published figure, reconciliation column and corpus, with what it confirms on the wrong path.
Nothing ties only under the golden, and nothing ranks the twelve areas against the standard.

| Control | What it confirms | Its wrong-path reading | Screen |
|---|---|---|---|
| the 2026 state network adequacy filing (the context artifact, ask C's source) | per area, the 2026 contracted sites, their licensed stations and the treatments delivered in 2026 | a solver reconciling its station column against the licence register for the 2026 cycle ties exactly, on R1's input, and learns nothing about any basis | it constructs no capacity figure, states no method, carries no utilisation figure and no adequacy verdict, and its site set differs from the 2027 contract-intent set by six sites or more, so it is out of window for the call. Asserted on all five points |
| the plan's 2027 enrolment projection by service area | the growth factor the standard's demand side uses | identical under all four rungs, because it multiplies the demand side and every rung shares it | ties on every basis; cannot score a station basis |
| the adequacy contract's capacity section | the population, the unit, the window, the standard and the as-of date | quotable against no station basis, because it names none | the pin sits at authority level 2 and once only; the counter-pin sweep is owed at stage 3 |
| the encounter extract's transmittal (control totals by quarter) | the extract's row count and treatment count per quarter | ties on every basis, because it counts encounters and not capacity | asserted to tie under all four rungs; it carries no capacity or position figure |
| the 2026 out-of-network payment register and its 2027 run-out supplement (ask A) | the treatments paid for at sites under no contract | the register's own reconciliation tab ties on its adjudication basis and not on the service-date basis the ask needs, which is ask A's primary device | it reads no contracted site's capacity and reaches no station basis; asserted zero device rows in the main population |
| the non-emergency transport trip file by area (distractor, named in `metadata.json`) | 2026 trips by area, which looks relevant to access | a solver ranking areas by trips ranks them by volume | asserted that its area ordering does not reproduce the golden's short set, so no shipped artifact ranks the candidates on the decision question (Gate G) |
| the state facility licence fee schedule by station count (distractor, named in `metadata.json`) | the fee a station attracts | a solver could read the fee schedule as a capacity authority | it states fees only and no station count for any site; never read by the solution |

**No calibration corpus and no confirming back-test ships.** The method is forced by the design (the data's
own structure), which is `determinism-check` Part 5 case 1 and the case it ranks first, so no filed selection
criterion and no closed-data confirmation is needed, and none is built. **No voice argues a method:** no memo,
briefing, draft or stakeholder figure in the pack carries a capacity number or a method for one.

## Ask sheet
Three asks, each a reconciliation or an audit trail of an input the call consumes (H18), each computed on rows
the call never reads. The main call's declared row population is the 2027 contract-intent sites' own
treatment encounters, and every device and hazard row sits outside it.

**Ask A, out-of-network treatment volume.** By area and half of 2026, the treatments the plan paid for at
sites it holds no contract with, and their share of the area's 2026 treatments. 24 counts and 24 shares, 48
graded figures, whole treatments and shares to one decimal, both stated in the asking sentence.
- H18 home: the audit trail of the demand side, from the payment register through rows the call never reads to the area's own 2026 total.
- Use: the network unit sizes the leakage it is contracting to pull back in.
- Primary device (D5 scope with D2 vintage, silent): the register's own quarterly reconciliation tab is true on the adjudication basis while the ask needs the service-date basis, and the 2026 service-date population needs the lines adjudicated in 2027, which arrive in a separate run-out supplement. A solver that ties to the tab files half-year counts that cannot be reproduced from the service dates. The inconsistency is internal and arithmetic: the register's service dates spill outside its adjudication quarters, so the tab's totals and the service-date totals differ by a figure the generator asserts. Nothing narrates it, the tab says only "adjudicated", and the battery's count-tie check passes against the tab, which is the tie that passes wrong.
- Remedy: a reconstruction, the half-year counts rebuilt on service date from the register and its supplement, with one correct answer.
- Hazards: the member-residence against site-service area assignment in the register (h3), and the run-out supplement's own vintage (h1).
- Files on the path: the payment register, the run-out supplement, the register's reconciliation tab, the provider directory, the licence register, the encounter database, the extract transmittal and the 2026 state filing. Column count on the golden's path is confirmed at stage 3 against the cut pack.
- Realism: a plan's out-of-network register is extracted on the adjudication cycle and supplemented after run-out, because that is when the money moves.

**Ask B, the licensed supply by area.** By area, the licensed outpatient dialysis and infusion sites the state
register holds at the as-of date and their licensed stations, counting a site once. 24 graded figures, whole
sites and whole stations.
- H18 home: a component of the call's case, the supply the plan could contract against the supply it does.
- Use: the network unit states the supply it has left to approach in a short area.
- Primary device (D7 keys with D2 version, silent): the register carries the amendment history as well as the current state, and licence numbers lapse and are reissued to other operators at other addresses, so grouping on the licence number merges two distinct sites and the current state has to be rebuilt per number from its amendment chain. The inconsistency is a licence number carrying two service addresses, some with non-overlapping spans and some overlapping because an amendment row and a current row both sit in the file.
- Remedy: a reconstruction, the state of each licence number rebuilt over its own chain at the as-of date, with one correct answer; noticing the duplicate addresses does not settle which rows are current.
- Hazards: the licence register's two grains on non-contract rows (h2), and the reissued numbers (h2).
- Files on the path: the licence register, its amendment rows, the provider directory, the 2026 state filing, the licence fee schedule's area list, the payment register (for the operators it names), the encounter database and the transmittal.
- Realism: a state licensing file is an event log with a current view, because licences are amended rather than reissued.

**Ask C, the sites the 2026 filing counted that carry no 2027 contract intent.** By area, how many and the
stations they were licensed for then. 24 graded figures, whole sites and whole stations.
- H18 home: a reconciliation of the context artifact to the population the call declares.
- Use: the network unit explains to the state what moved between the two filings.
- Primary device (D9 self-validation, silent): the plan redrew two service-area boundaries for 2027, so the 2026 filing's per-area totals are true only under the 2026 boundaries while the ask is by the 2027 areas, and both files are internally consistent and tie area by area on their own basis. The sites have to be re-assigned to the 2027 areas from the directory's own recorded area before the two are compared. The battery's unmatched-join check passes, every site matching.
- Remedy: a reconstruction, each 2026 site placed in its 2027 area, with one correct answer.
- Hazards: the run-out supplement's vintage (h1) and the licence register's two grains (h2).
- Files on the path: the 2026 state filing, the provider directory, the licence register, the enrolment projection's area list, the transmittal, the payment register, the fee schedule's area list and the encounter database.
- Realism: a plan redraws service areas with its own network, and files against the areas in force in the filing year.

**The main population's zero counts.** Asserted by count in `generator/checks.py`: zero device rows, zero
hazard rows and zero resubmission pairs inside the 2027 contract-intent sites' own treatment encounters; no
document the call reads carries an ask's organ; deleting every device leaves the call's figures and all twelve
area verdicts byte-identical.

| Hazard | Asks it moves | Per-ask delta |
|---|---|---|
| h1 the run-out supplement's vintage | A, C | owed at stage 3 against the cut pack |
| h2 the licence register's two grains and its reissued numbers, on non-contract rows | B, C | owed at stage 3 against the cut pack |
| h3 the register's member-residence against site-service area assignment | A | owed at stage 3 against the cut pack |

**The referee.** One byte-clean referee arbitrates the designed disagreement in ask A without handing over a
level: the extract transmittal's treatment count by quarter, which ties under both the adjudication and the
service-date readings for the contracted sites and so settles nothing about the non-contract rows. Every other
control ties under every handling.

| Ask | Cracker's path (lands the call, runs the hygiene battery, executes every filed rule, matches every control) | Figures it reaches | Verdict |
|---|---|---|---|
| A out-of-network volume by area and half | ties the half-year counts to the register's own reconciliation tab, which passes its count-tie check, and never cross-tabs service date against adjudication quarter, so every half-year count and every share is on the adjudication basis | 0 of 48 | miss |
| B licensed supply by area | groups the register on the licence number, which is unique in the current view, so the reissued numbers merge two sites and the amendment rows are read as current | 0 of 24 | miss |
| C the dropped sites by area | compares the 2026 filing's per-area totals against the directory on the filing's own area labels, which tie area by area, and never re-assigns the sites to the 2027 areas | 0 of 24 | miss |

**Mirror leakage:** 29.2 per cent of the ask weight, the best response off the call keeping no ask whole
(it reaches 18 of ask A's 48 figures through the run-out supplement and 10 of ask B's 24 through the
amendment chain, and misses ask C's boundary redraw entirely).

**Pair ceiling:** 36.5, on Part 0's weights of 38 for the recommendation and critical components, 7 for
instruction following and 55 for the asks: the response that lands the call keeps 45.0 and the best response
off it keeps 28.0, both under the build target of 60 and under the brief's 40.

**Measured by:** generator/ceiling.py, which prints one row per response with the two scored from different
readings; at stage 2 it runs on this sheet's own figure counts and stop model, and it is re-run on the cut
pack at stage 3 before the pair is believed (`supplemental-stumping` Part 1.1d), the gated fields taking the
worst honest measurement.

**Sensitivity**, printed by the same script. If the cut pack lets the cracker keep a tenth, a fifth, three
tenths or two fifths of the ask weight rather than nothing, the pair reads 39.3, 42.0, 44.8 or 47.5, all under
60; the ladder, not the asks, is what keeps one of the top two off the call.

## Layer 1 inventory

Owed at stage 3 for architecture 3, one row per item in `## Three rules`'s `Layer 1:` line with the system that
produces it and its asserted neutrality on the call.

## Pre-ship check

Owed at stage 5 for architecture 3.

## Leak check

Owed at stage 3 for architecture 3. The pack ships no file whose job is to describe the data: no dictionary, field
notes, readme or manifest (`dataset-generation` section 3), so every convention the call leans on sits in the
adequacy contract at authority.

## Tried and rejected

- Architecture 2, placing the 2025 retiring reading test's scores on the new scale by a concordance from the
  single-group bridge study (2026-10-27): solved on the portal. Both responses landed the call and one filed the
  runner-up and the gap exactly. The diagnosis is in `## Portal result and the diagnosis, 2026-10-27` below, and
  the world was then measured closed in `## The world is exhausted for this decision, measured 2026-10-27`: the
  repeater population moves counts 1 to 22 and leaves the slate intact, and the count-day rolls and the crosswalk
  are exactly clean, so no harder call survives in that world. The root cause is the client's rule 3 read the
  other way round: the decisive step was psychometrics' own named method for the deciding quantity, so a response
  that knows the field reaches it by reflex (the stage-4 leak reader had already named a symmetric equating at 241
  or below). Architecture 3 keeps the number and the ETL objective, takes a fresh world, and moves the field's own
  method into the default path, so the decisive step is a reconstruction of a capacity input that no field holds
  rather than a choice between two named methods.

- Weather normalization alone, with oil fills and estimated reads as the interval structure: in a prototype of 150
  buildings, a degree-day regression on calendar-month bills with oil deliveries summed by month landed within 2 per
  cent of the fill-to-fill fit for most oil buildings (6 at most) and on the golden's slate, so a strong analyst's
  regression lands the call; the estimated reads and fills are Layer 1 (cleaning them makes the call easy) and stay
  there. The decisive structure is each building's change in how it runs.
- A first keying of the card on the time gap with pattern A and Gate G forecasting: the signature is spent in seven
  older builds; keyed on the population gap with G4 first, which also reads truer (the bills before a change are not
  the decided building).
- The 2025 benchmarking year scaled by degree days as the default path: the cycle rules name the bills, statements and
  tickets as the records, so a competent analyst fits them; the filings route stays below rung 0 and the default path
  is the whole-record fit.
- Ask B on the gap between the filings and the bills for 2025: its golden sat near zero for most types; Ask B now
  carries the filings' own emissions and site energy by type on the export's lot rows.
- A six-day sensor outage in April 2024 in the weather record: leaving missing days out of the degree days moved 808
  Thornwick Avenue and 686 Fenwright Avenue across their $5,000 bins; the outage now sits in April 2019, outside the
  billing years.
- Partial oil deliveries at random on every building: taking them as fills hid one building's boiler change from the
  search and put it in the slate; partials now fall in the 2022 to 2023 season, on no building near the cut, and every
  building away from the cut is held under $55,000 on a whole-record fit.
- The law's billing sentence ("bills it to the property's tax lot and posts any deduction ... against the same
  notice"): an ask organ in a document the call reads, and wrong against the ledger (a reassessment opens a new
  notice); cut.
- Round floor areas on the twenty buildings placed around the cut (each a multiple of 1,000, against none of the other
  138): a giveaway; each now carries an ordinary area and the calibration re-aims.
- Keeping estimated reads and partial deliveries off the buildings around the cut, to hold those items neutral: a second
  giveaway. Every building now carries the same processes: the utility's estimates land within a few per cent, as a
  weather-adjusted routine does (estimates missing by 20 to 40 per cent, read as actual, hid two slate properties'
  changes from the search), none after the advanced meters of October 2025 or the steam company's January 2025 system,
  and partial deliveries stop a few hundred gallons short, in the 2022 to 2023 season only.
- A window started one span after the found break as a variant the golden must hold under: no reader would choose it
  (the first span after a change is wholly post-change), and 62 Merrow Street moves 2 per cent under it; the variant
  asserted is the generator's own change dates.
- Architecture 1, the degree-day fit on each fuel's spans after its last change found in the property's own bills
  (2026-10-17): judged NOT_DETERMINISTIC, SEND_BACK (margin_or_boundary_fragility, underspecified_objective). The post-
  change window's first span and whether electricity is refit with the heating fuel are open (461 Tallman Street's
  electricity rises 1.35 times when its gas falls; refit, it is the first left out at $70,990 against 633 Lattermore
  Place's $68,577), a step search run as written flags dozens of series and moves four $5,000 amounts, and a $7,000
  12th-to-13th margin sits inside a $40,000 to $57,000 window freedom. Filing the window or a dated change log would make
  the step rule application; an undated change cannot be pinned without it. The architecture is spent and re-rooted.
- A first redraw (architecture 2 on paper, 2026-10-17): each district's claim under a state challenge judged by the
  upper end of its inventory's 95 per cent interval, the decisive move carrying each shared emission factor's error on
  the district's fuel total instead of building by building. The correlated-error lesson is already task228's,
  task229 v1's, task260's and task261's (an error shared by the units does not average away); dropped before
  registration.
- The retiring test on a continuous scale (every integer a possible score): the concordance conventions disagreed at
  the Level 1 boundary unless the bridge's share sat within a student of a cumulative step (an exact count match tied
  the at-or-below conventions, a gap of one to three students split the quantile cut's "below" and "at or below"); the
  retiring test is now a 30-item paper form whose raw-to-scale table leaves six to eleven points between scale scores
  near the cut, and all 30 conventions agree with 41 bridge students to spare.
- A bracket of the slate, the overcounting routes (inverse regression, the range match) also wrong: it needed grade 9
  cohorts two to three times the grade 10 ones in two districts; those routes land the golden six with every count
  wrong, and the ladder rests on the prediction and cohort routes.
- Equal cohorts statewide: matching the two cohorts' statewide percentiles or z-scores landed the golden; the 2025 grade
  8 cohort now reads 0.20 standard deviations below the 2026 one, which the bridge sample's retiring-test mean shows,
  and every cohort match places 231.
- Bridge draw 0: 53 per cent of its students with a retiring score of 241 sat at Level 1, so a per-score majority rule
  placed 241 at Level 1 and filed the golden; the bridge's schools are drawn again (draw 11: 43.5 per cent, all 30
  conventions still agreeing at every cut).
- A school realignment between two districts as an ask hazard, the vendor's file keeping the old district: the date of
  the move could not be read from the folder without a filed sentence, a fork; dropped.
- Asks on the students the count leaves out (no grade 8 result) or on the movers: the complement or a split of the main
  population, so a device on them moves the call's rows; dropped.

- The adequacy standard written as a cushion over REALISED demand (2026-10-27, measured on the stage-2
  prototype): the true ceiling can never fail it. Realised volume is bounded by the true capacity, so 1.15
  times realised volume always sits under the concurrency-ceiling capacity and no area ever flips, which
  would have left the decisive step moving the network total and not one of the twelve area verdicts, with
  the grid the prompt shape supplies graded on a constant column. The standard is now the growth test the
  2027 contract actually turns on: projected 2027 demand is the area's 2026 contract-year treatments a week
  grown by its enrolment growth factor (1.040 to 1.120 across the twelve areas), and an area meets the
  standard when its capacity is at or above 1.15 times that. An area then fails on the golden when its 2026
  true utilisation is above 1 over 1.15g, about 0.80, and clears on attested stations when its apparent
  utilisation is below that line, which is what the flip set of three areas is built from.

- The volume ceiling filled as a fixed fraction of each site's concurrency ceiling (the first prototype of the
  arithmetic, 2026-10-27): R2 then sat uniformly below R3 at every site, so R2's short set was exactly the
  golden's six areas and a solver stopped at R2 got all twelve area verdicts right and only the network
  total wrong, which cost the area grid its whole discrimination. R2 is now the site's busiest week over the
  four-year record, which sits above the current roster's product at the six to nine sites of forty that
  closed a third shift or a sixth day between 2023 and 2026 and well below it where the site's own demand
  never approached its slots: measured over eight seeds R2 misses two of the golden's six short areas and
  calls four of its clear areas short, six of twelve cells wrong, with the same six-of-twelve headline count
  as the golden under a different set.

- Placing the extra dropped shifts (the ones outside the two flip areas, which keep that structure from
  being a marker) as a closed third shift (2026-10-27): at an unconstrained site that lifts the busiest week
  to 1.27 to 1.49 times the site's current attested weekly capacity, a visible impossibility that a solver's
  own capacity check flags at exactly the sites the ladder leans on. Those sites now lost a sixth day
  instead, and the busiest week over the current attested capacity is asserted at or under 1.05 (measured
  maximum 0.992 to 1.032 over eight seeds, which reads as the roster having shrunk and argues the attested
  count is too low, away from the golden).

- Giving every flip area three plant-constrained sites of unequal size (2026-10-27): the partial
  applications of the ceiling then filled the interval between the attested and the concurrency readings
  densely enough that one cell sat 3.6 to 5.6 per cent from the area's line, under the floor. Each flip
  area's shortfall vector is now searched so every one of its constrained sites carries at least a seventh
  of the area's positions, and the nearest partial cell is measured at 6.03 to 6.11 per cent on every seed.

- A staffing roster carrying clinical headcount per session (2026-10-27): a nurse ratio across the extra
  chairs is one of the three physical reasons a site's stations cannot all run, and a per-session headcount
  would let a solver compute positions straight off the roster, which is readability test 2 and hands the
  decisive quantity over. The roster ships the sessions it staffs a week and the clinical hours it staffs a
  month, from which no position count is derivable, and every plant constraint in the pack is a shared water
  treatment loop or a shared compounding hood.

## Portal result and the diagnosis, 2026-10-27

**Both responses landed the call.** Each funded the golden six (Kessick, Varlow City, Brenmoor County, Calderidge
Unified, Garnet Hills, Elmorrow), and the second also filed the runner-up and the gap exactly: "Harlenbrook is first
left out with 353 eligible students, 15 fewer than Elmorrow's 368", which are the golden's own figures. So the second
response executed the concordance, not a route that lands the slate by accident. Architecture 2 is spent, and the
reason is in this note rather than in the portal.

**Cause 1, and it is the root: the decisive step is the field's standard practice, so it is a reflex.** The
`Domain test:` line says it outright: "psychometrics places one test's scores on another's scale by a concordance that
matches the two score distributions (equipercentile or linear linking ...), while a regression of one score on the
other is a prediction that pulls every converted score toward the sample's mean." The golden is that concordance. The
`## Readability screen` then rated the same move `silent` on test 3 with "no: the prediction reflexes and the cohort
match land on 231". Both cannot be true. If the field's own method for the deciding quantity is the golden, a
competent analyst applies it; what the screen measured was that the *wrong* routes are also reflexes, which is not
what test 3 asks. Test 3 asks whether the decisive move is an opponent default, and for anyone who has linked two
tests it is the first thing they reach for.

**Cause 2: the stage-4 reader had already solved it, and its answer was read for its taxonomy rather than its
content.** Round 2's question 6 says the easy routes "swap Elmorrow and Harlenbrook; a symmetric equating (less than
or equal to 241) does not". That is the decisive step, the correct cut and the correct consequence, in the reader's
own words, before the build shipped. It was recorded as a pass because question 6's answer was "an analytical
choice", which it is: the step's KIND was never the problem. Gate F was, and the evidence for failing it was sitting
in the same paragraph.

**Cause 3: the slate is landable without the decisive step.** The `## Ladder` records it: R2 (inverse regression) and
R2b (the two scales' ranges matched) both file "the golden six, every count high". Three of the seven rungs land the
call, so a response that links the scales wrongly in the other direction still banks the recommendation. Only the
counts separate them, and the counts are ask weight, not the call.

**What this does not need.** The determinism is sound (two judge passes on file), the pack and its Layer 1 inventory
measured sound, the asks are decoupled and the conformed-file deliverable is good. The world, the fourteen applicants,
the two vendors and the count-day machinery can all be kept. What has to move is the decisive step.

**What a re-root needs here.** A decisive step that is not the field's named method for the deciding quantity, that no
competent reflex reaches, and that the records force to one execution. The test to apply at the draw, from this
failure: if the `Domain test:` line and the `Decisive step:` line name the same method, the screen's test 3 fails and
the draw is not ready.


- Architecture 2's decisive step, the concordance against the regression prediction (2026-10-27, on the portal
  result): spent. Both responses landed the call and one filed the golden's runner-up and gap exactly. The step is the
  field's own standard practice, which the note's `Domain test:` line states and the readability screen then rated
  silent on test 3; a reflex reaching the golden spends the stump whatever the step's kind. The stage-4 reader had
  already named the symmetric equating and the 241 cut in its own words, which was Gate F evidence recorded as a pass
  because its question-6 answer was "analytical choice". Compounding it, R2 and R2b land the slate too, so three of
  seven rungs reach the call and only the counts separate them.
- Defending the concordance better, or adding a rung above it: refused before it was tried, on task184's measured
  precedent in this repo. There, deleting the three clauses that licensed the textbook weight left the same answer
  reachable, because the reader had reached it unprompted; the note's conclusion was that the golden has to move off
  the textbook move rather than be better defended. The same holds here: the equating is reachable from the bridge
  file alone.

## The world is exhausted for this decision, measured 2026-10-27

Before drawing architecture 3 I looked for a decisive step in this world that is not the test placement, because the
placement is the reflex that spent architecture 2. The pack was re-measured from `target.zip` directly, and the
reconstruction reproduces the golden exactly (sixth 368, seventh 353, gap 15), so the measurements below are against
the shipped truth and not against a re-derivation.

**What the pack still holds that architecture 2 never used.** The grade in 2026-27 does not determine which
instrument carries a student's grade 8 result, because students repeat grades:

| Population | Students |
|---|---|
| Grade 9 with a new-test grade 8 result (the expected path) | 22,513 |
| Grade 9 with a retiring-test grade 8 result only, so grade 9 repeaters | 610 |
| Grade 9 with both, so grade 8 repeaters whose latest result is the newer one | 326 |
| Grade 10 with a retiring-test result (the expected path) | 22,351 |
| Grade 9 or 10 with no grade 8 reading result at all | 1,063 |

That is 936 grade 9 students whom a pipeline keyed on grade either drops or places on the wrong instrument, and the
spent default path's own step 4 ("Grade 9 on the new test") does exactly that.

**And it does not move the call.** Measured per district against the golden: the by-grade pipeline moves every count
down, by 1 to 22 students, and leaves the slate and the boundary where they were (sixth 1220 at 363 against 368,
seventh 1240 at 349 against 353, the gap 14 against 15). The ordering is untouched.

**So the only lever in this world that moves the funding boundary is the placement of the retiring test's scores on
the new scale**, which is the field's named method and the reflex that failed. Everything else is measured flat: the
count-day roll has no ambiguity at all (88,329 covering spells, zero students with two, zero on two districts'
rolls), the examinee crosswalk is exactly one to one in both directions (71,949 ids each way, no fan-out), the
students with no result cannot be counted at Level 1 under any reading, and the ladder already measured the retiring
test's own performance levels as a rung rather than a lever.

**Conclusion: architecture 3 cannot be drawn in this world.** Any call this pack can ask routes its analytical content
back through test linking, because linking two scales is what this world is about. The re-root keeps the number and
the ETL objective and takes a fresh world, which is a full stage-1 draw and a new pack rather than a repair.


- A decisive step built on the repeater and off-instrument populations, in this world (2026-10-27, measured before
  the draw): refused on magnitude. The structure is real, 610 grade 9 students carrying only a retiring-test grade 8
  result and 326 carrying both, and the spent default path mishandles all 936. But it moves each district's count by
  only 1 to 22 students and leaves the slate, the sixth and seventh places and the gap intact, so it cannot carry a
  call. It also sits on the hygiene battery's own unmatched-join check, which the opponent runs.
- Keeping this world for architecture 3 at all (2026-10-27): refused on the same measurement. The placement of the
  retiring scores on the new scale is the only lever that moves the funding boundary, and it is the field's named
  method, so every call this pack can ask routes back through the reflex that spent architecture 2. The count-day
  roll, the crosswalk and the unresulted students are each measured flat. The re-root takes a fresh world in the same
  objective and number.
