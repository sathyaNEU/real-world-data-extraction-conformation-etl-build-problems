# task464 design note: the 2027 outpatient capacity register (architecture 3, spent)

Status lives in `pipeline.json`; this note holds the design. **Read `## Architecture 4: the cell screened and
refused, measured 2026-10-27` at the foot of this file before anything else, then `## Tried and rejected`.**
Architecture 1 (the Wendlemere building emissions slate) was sent back by the determinism judge, architecture 2
(placing the retiring reading test's scores on the new scale) was solved on the portal because its decisive step
was psychometrics' own named method for the deciding quantity, architecture 3 (below) was sent back at the stage
4 re-judge on Gate C and its world then measured closed, and architecture 4's screen of the author's fixed
education and ETL pairing refused all four candidate decisive steps on measured arithmetic. The body of this
note from `## Draw` to `## Leak check` describes architecture 3 and is kept as the record of a spent design.

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

Ends on: a 2027 network capacity 1.2012 times the golden (4,668 weekly treatment slots against 3,886 on the cut
pack), with three of the twelve service areas filed above the adequacy standard that are below it.

Golden: the same conformation with each site's deliverable positions set to the greatest number of its own
treatments that have ever run at one time, which at about a third of the sites is several short of the stations
it attests and the licence lists.

## Stump sentence

The default path multiplies each site's attested stations by its rostered sessions, ties the product to realised
volume and the adequacy standard, and files a 2027 network capacity 1.2012 times the golden with three of
the twelve service areas wrongly above the standard, because the stations a site attests are the positions it has, not the positions
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
capacity 1.2012 times the golden (4,668 weekly treatment slots against 3,886) with three of the twelve service areas
wrongly above the standard. Executed in `generator/checks.py` on the clean truth as the R3a assertion.

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
comes out `silent`. Every figure below is measured on the cut pack and written from
`generator/measurements.json`.

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | 7 dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 attested stations | yes, the directory's `attested_stations` names the count | yes, one column | yes, the first construction anyone builds | no control scores it | no sweep refutes it | yes, one product | no | readable |
| R1 the state licence's station count | yes, the register names the licensed stations | yes, one column after one join | yes, the reflex of an analyst who distrusts a self-attestation | the 2026 filing's station column ties to it | the register's two grains are a battery finding | yes, one product | no | readable |
| R2 the revealed volume ceiling | no sentence names it | no, it is built from the encounter record | yes, revealed throughput is a capacity planner's second move | no control scores it | the battery's volume-against-capacity reconciliation points at it | close to it, one maximum over a group-by on site and week | no | readable |
| R3 the concurrency ceiling **(decisive)** | the agreement defines the unit's term and nothing else (argued below) | no: the encounter record carries no session, chair, shift or position key, so there is no row predicate and no header-found join, asserted over every shipped column name | no (argued below) | no control, corpus or published figure scores any station basis; the 2026 filing constructs no capacity figure at all, asserted | no: the five sweeps find the attestation cycles, the register's grains and the two layouts, and the volume-against-capacity tie passes on every basis, apparent utilisation on attested stations running 0.419 to 0.951 with no site at or over 1 | no: a maximum over 639,009 reconstructed intervals, and corr(the correction an area takes, the area's own size) is far from one | no: the timed extract is the file the standard's own demand side needs | silent |

**Test 1, answered as it stands rather than as stage 2 wrote it.** Stage 2's cell said nothing in the pack
names deliverable positions. That is not true of the cut pack and could not be: `determinism-check` section 1
requires the estimand's unit filed literally, so Schedule 4 clause 4.2 carries one sentence, "Deliverable
treatment positions means the treatment positions a Site is able to operate simultaneously". What the clause
does not carry is a route: it names no file, no column, no statistic and no window, and the obvious
operationalisation of it is the directory's own `attested_stations` column, which is what the default path
takes. The sweep for the words a route would need is asserted: the agreement does not contain `concurrent`,
`overlap`, `greatest number`, `at one time`, `effective capacity`, `water loop`, `compounding hood` or
`busiest week`, each checked through the same extractor the positive controls run through. **This is the
build's largest Gate F risk and it is named here rather than argued away:** a reader who tests the clause
against the column finds the gap, and the design rests on the claim that a competent analyst maps the clause
onto the column without testing it.

**The stage-4 leak reader measured that exposure in the pack's own words, and both answers are on the
record.** Asked whether anything makes it obvious that a station count is not the runnable positions, it
answered "yes, it is fairly obvious", citing clause 4.2 and the "where used" hedge on the licensed count in
the same clause. Asked whether a solver would reach the concurrency sweep, it answered "yes, by data shape
and by the word simultaneously in 4.2". The build ships with that risk recorded rather than redesigned, on
the author's ruling of 2026-10-27: section 1 requires the unit filed, leaving it open is the fork that
killed task157's first architecture twice, and this is the Gate C against Gate F dial this lane keeps
hitting. What makes it tolerable is measured above and not argued: no window width returns the ceiling
everywhere, the cheap statistics return at least 1.38 times the positions, and the two readings a solver
might actually take file 3,013 and 3,825 weekly slots against the golden's 3,886 and are named cells in the
fork grid.

**Test 3, the one the brief asked to be guarded hardest.** A capacity planner handed timed service intervals
may sweep them for occupancy unsent. Four properties of the cut pack bear on it and all four are measured.

1. **The plateau is in the month without being the day's signature.** The ceiling is reached in every one of
   the 48 months at all 40 sites, and the hour of the day at which a site runs fullest sits at that site's
   own modal hour on a median of 0.29 of its site-days (worst 0.48) across a median of 10
   distinct hours. The round that saturates is drawn per day, so there is no fixed clock window at which a
   site is always full.
2. **The statistics a solver runs for another reason do not return the position count.** The most treatments
   a site takes in one day is at least 1.38 times its positions, and the most distinct members in one
   day at least 1.38 times, so neither a per-day count nor a per-member count lands on it.
3. **The statistics that do return it are the decisive step in other clothes, and none works at a width a
   solver could validate.** The most treatments starting inside a sliding window equals the position count
   at 18 of 40 sites at one hour, 36 at two and 25 at three; on a fixed clock block the
   counts are 15, 30, 24 and 16 of 40 at one, two, three and four hours. No width
   returns it everywhere, the count is a lower bound that is slack at the rest, and arriving at the right
   width means already knowing the quantity is positions and that the width is a treatment's own length,
   which is the stop or the length column. Read as a basis rather than as a check, the clock-hour reading
   files 3,013 weekly slots and the two-hour reading 3,825, neither the golden's 3,886, so each is a
   named wrong cell in `## Ladder`'s grid rather than a route to the answer.
4. **A solver who does sweep occupancy finds the ceiling at once, and that is determinism rather than a
   leak.** SF1 is closed on a hard plateau, so every maximum-based reading returns the same integer at all
   40 sites. **Verdict: the plateau is legible to the sweep and to nothing else, and the sweep is the
   decisive step.** Nothing in the pack gives a reason to sweep occupancy: the demand side needs weekly
   counts, the hygiene battery compares volumes against capacity and passes, and no shipped column, filed
   sentence or control compares a site's concurrent treatments with its station count.

**Test 7, answered by naming the other use.** Delete the decisive step and the pack still carries four
contract years of timed encounters, because the standard's own demand side is the area's 2026 treatments a
week and this is the only file that holds them, and because dialysis and infusion are billed in timed units.
The same rows supply the demand base, the growth test and ask A's denominator, so the organ's presence
carries no information about the decisive step.

## Semantic fork table
One row per term of the main ask and per convention the main computation needs. Every id is asserted in
`generator/checks.py` and recomputed from the bundle by `generator/verify.py`. SF1 is closed on the data,
never by a sentence saying how to compute a ceiling: a filed method would make the decisive step rule
application, which the client's rule 3 bans.

| id | Term or convention | Golden reading | Alternatives, and the call under each | Ruled out by |
|---|---|---|---|---|
| SF1 | a site's deliverable positions | the greatest number of the site's own treatments running at one time | the record maximum; each of the 4 yearly maxima; each of the 48 monthly maxima; the 12 and 24 month look-backs; a high percentile of concurrency over treating time | C1 on the data, a hard plateau, measured at 40 of 40 sites: the record maximum, all 4 yearly maxima, all 48 monthly maxima and the 12 and 24 month look-backs are one integer, and one more than it never runs. A site holds every position occupied for 0.062 to 0.213 of its treating minutes, so the 95th and 99th percentiles return the same integer at 40 and 40 of 40 sites. The 90th returns it at 27 of 40, and where it does not it returns a number the record itself refutes, since the record shows that many treatments running together; a percentile under 1 is not a reading of a maximum. Asserted per site as `SF1` |
| SF2 | the interval convention | half-open, start inclusive and stop exclusive | closed, or stop inclusive and start exclusive. Same call | C1: no treatment at a site starts on the minute another stops, measured at 0 coincident endpoints over all 40 sites, and every position's turnover is strictly positive. Asserted as `SF2` |
| SF3 | cancelled and no-show encounters | no interval: the record carries no stop time and no length for them | read as instantaneous, or dropped. Same call | C1: 7,576 such rows ship, each placed where the site was running at least two positions short, so the ceiling and all twelve verdicts are unchanged under either reading. Asserted as `SF3` |
| SF4 | the local clock with no offset on the 2023 and 2024 feed | the site's own local clock | a site-level offset applied, or the feed read as coordinated time | C1: an overlap count inside a site is invariant under any site-level offset, asserted by recomputing every site's maximum under a shifted clock, and no interval spans the repeated hour of the autumn fall-back (0 of 639,009). Asserted as `SF4` |
| SF5 | a treatment session | Schedule 4 clause 4.2: a staffed block in which each position delivers its treatments for that block | a shift, a day, a chair-day | the clause, and the roster reports `treatment_sessions_week` as one integer per site current at the position date, asserted one row per site |
| SF6 | a week | clause 4.3: one fifty-second of the contract year | 52.143 weeks, or the weeks in which the site treated | the clause; `SF6` asserts the twelve verdicts identical under 52 and under 52.143 |
| SF7 | the attestation cycle current at the position date | the site's latest cycle row at or before it | the latest row in the file, the latest of the current calendar year | C1: every site's latest cycle row precedes the position date by 30 days or more and no site carries two rows in a cycle. Asserted as `SF7` |
| SF8 | the register's two grains | the facility row at the service address | the corporate umbrella row | clause 4.2 files the facility row as the basis, and a corporate row equals the sum of its own facility rows in its area. Asserted as `SF8` |
| SF9 | the population | the sites carrying a 2027 contract intent on the current cycle | every site in the directory, every licensed site in the twelve areas, the 2026 contracted set | clause 4.1 files it, and the intent is recorded once per site and only on the current cycle, asserted at 40 sites |
| SF10 | the treatments a position delivers in a session | clause 4.2's per-category figure, one and two | a site-level figure read off the encounters | the clause; `SF10` asserts no site carries both service categories |
| SF11 | projected 2027 demand | clause 4.3: the area's 2026 contract year treatments a week grown by its projected factor | the 2026 calendar year, the last four quarters, a four-year trend | the clause files the base, the window and the factor's source, and the contract year is the calendar year, asserted by selecting the same encounters both ways |
| SF12 | the standard's direction and inclusivity | at or above the required figure | strictly above | C1: no area sits within 6 per cent of its line on any of the four bases, worst measured 6.02 per cent of required. Asserted as `SF12` |
| SF13 | the rounding path, and which area comes nearest the standard | clause 4.4: the required figure is rounded once, at the area level, up to the next whole treatment slot, because it is a minimum; the area nearest the standard is the one with the smallest shortfall in slots | round to nearest, round down, or the unrounded figure; nearest read as the smallest shortfall as a share of required | the direction is filed at authority, asserted present in the shipped document. No area's verdict depends on the rounding, asserted per area against the unrounded figure, the floor and the ceiling, and no required figure sits within 0.06 of a whole slot or of a half. C1 on the data for the nearest: Hesper Vale's shortfall is 19.62 unrounded, 20 to nearest, 20 up and 19 down, and the runner-up Lowenbrook's is 22.07, 22, 23 and 22, so one area is nearest under every rounding with 2 slots of daylight on the tightest reading, asserted. The per cent reading is not a reading of nearest the standard, which is a figure in slots |
| SF14 | a site's service area | the area recorded against the site on the current cycle | the area of the address the site held earlier | clause 4.6 files it, and no site sits in two areas inside the window, asserted; the three sites that changed address kept one area |
| SF15 | the look-back for the ceiling | the whole four-year record | the most recent 24 or 12 months | C1 through SF1's plateau, asserted per site at 12, 24 and 48 months |
| SF16 | the key that identifies a site | the plan site identifier, carried on every encounter as the service facility | the tax identifier, which three sites of one group practice share; the service address | clause 4.1 files the unit as the Site and says that sites sharing a tax identifier remain separate Sites. The tax-identifier reading merges those three and files 4,512 weekly slots against the golden's 3,886, a named wrong cell; the plan site identifier is one to one with a site, asserted |
| SF17 | weekly treatment slots | clause 4.2: positions times sessions a week times the category figure | realised treatments a week; the slots the 2027 roster offers | the clause files the unit and its inputs and says nothing about how positions are found, which is the WHAT and not the HOW. Asserted per site and against the shipped deliverable |

## Ladder
Four rungs, measured on the cut pack and written from `generator/measurements.json`. Stage 2's figures were
a prototype's and are replaced here.

| Rung | What it does | Network slots | Over the golden | Areas short of 12 | Its own short set | Worth on the graded quantity |
|---|---|---|---|---|---|---|
| R0 | the default path: attested stations times sessions a week times the category figure | 4,668 | 1.2012 | 3 | Hesper Vale, Eastmoor Reach, Fallowbray | 0.000, by definition |
| R1 | the state licence's station count in place of the directory's attestation | 5,006 | 1.2882 | 2 | Hesper Vale, Eastmoor Reach | -0.432, it walks away from the golden |
| R2 | the revealed volume ceiling: each site's busiest week in the record | 3,590 | 0.9238 | 8 | Granleigh, Ammerly, Hesper Vale, Innsmere, Eastmoor Reach, Durnsfield, Jarrowmead, Fallowbray | +1.379, it overshoots the correction |
| R3 | the concurrency ceiling, the golden | 3,886 | 1.0000 | 6 | Lowenbrook, Hesper Vale, Bexhollow, Eastmoor Reach, Jarrowmead, Fallowbray | +1.000 |

**Position and dominance.** The golden is bracketed: R1 and R0 overshoot it, R2 undershoots it, and the
decisive move reverses R2 upward. The four totals are strictly ordered R1 > R0 > R3 > R2 and the closest
pair sits 7.62 per cent of the golden apart, clear of the 6 per cent floor. Each rung names its own total
and its own short set.

**Each rung's own grid of wrong area cells**, against the golden's twelve verdicts:

| Rung | Golden-short areas it clears | Golden-clear areas it calls short | Area cells wrong of 12 |
|---|---|---|---|
| R0 | 3 (Lowenbrook, Bexhollow, Jarrowmead, the flip set) | 0 | 3 |
| R1 | 4 (Lowenbrook, Bexhollow, Jarrowmead, Fallowbray) | 0 | 4 |
| R2 | 2 (Lowenbrook, Bexhollow) | 4 (Granleigh, Ammerly, Innsmere, Durnsfield) | 6 |
| R3 | none | none | 0 |

This is the defect the first prototype of the arithmetic carried, and the repair. There the volume ceiling
sat uniformly below the concurrency ceiling, so R2's short set was exactly the golden's and a solver stopped
at R2 got the whole grid right and only the total wrong. Here the busiest week can sit above the current
roster's product as well as below it, because 6 sites of 40 closed a shift between 2023 and 2026
and their busiest week came from the larger roster, so R2 now misses two of the golden's short areas and
calls four of its clear areas short: six of twelve cells wrong, under a short count of 8 against the
golden's 6.

**Margins.** All 48 area-rung cells clear 6 per cent of their area's required figure, the worst measured
6.02 per cent, which is where the floor is meant to bind (the flip areas on the golden reading). The flip
set is three of twelve.

**The grid of partial applications.** The decisive step applies site by site, so the grid is the power set of
the plant-constrained sites inside each area: 41 cells over the twelve areas, with 16 constrained
sites. No partial application reproduces a golden-short area's verdict, because each constrained site inside
a flip area carries at least a seventh of its area's positions, so leaving any one of them on attested
stations puts the area back above the standard. The nearest partial cell sits 6.02 per cent from its
area's line, so every cell is a named wrong answer outside the floor. The network total falls strictly as
more sites take the ceiling, so no proper subset reproduces it either.

**The fork grid's own cells, each measured and mapped.** The station basis crossed with the demand basis is
eight cells. The realised-demand column is the first death in `## Tried and rejected` and is asserted inert:
on 1.15 times realised 2026 volume, 3 areas are short and the decisive step changes **no** area's
verdict, which is why the standard turns on projected demand. The four station bases are the four rungs
above. Four further cells are named rather than swept, each asserted against the fact that refutes it:
reading the 2025 and 2026 length column as hours makes every one of a site's intervals overlap and files a
ceiling above the site's attested stations at 40 of 40 sites, which the file itself refutes; taking the
most treatments starting inside a clock hour as the position count files 3,013 slots; taking the most
inside two hours files 3,825; and the 75th percentile of occupancy files 2,911. None is the golden's
3,886.

**Stacking.** Three mechanisms from different gaps: the population gap carries the decisive rung (which
positions a site can work), the time gap carries rung 1 and the demand side (a licence cycle and an enrolment
projection against a contract year), and the objective gap carries rung 2 (a revealed throughput read as a
capacity). The decisive gap is not rung 1's.

## Closure table
The 22 axes of `determinism-check/references/forcing-the-answer.md` Part 1, one row per axis number, axes
that cannot move the answer today included.

| # | Axis | The reading this build takes | Closure move |
|---|---|---|---|
| 1 | Population | the 40 sites with a recorded 2027 contract intent on the current attestation cycle, the 2027 network year not yet contracted | clause 4.1 files it and states that sites contracted for an earlier network year are not in scope unless they carry that intent; C1 through SF9 and SF7 |
| 2 | Unit of account | the site, not the corporate holder and not the tax identifier | filed by clause 4.1, which adds that sites sharing a tax identifier or a licence holder remain separate Sites; C4, the tax-identifier reading merges the group practice's three sites and files a named wrong total (SF16) |
| 3 | Attribution window | the 2026 contract year for demand, the four-year record for the ceiling | the contract files the demand window; C1 for the ceiling through SF1's plateau and SF15, every sub-window returning the same integer |
| 4 | As-of dating | one filed as-of date; the roster current at it, static across the window | filed as-of date in the contract; SF7 puts every latest attestation row 30 days or more before it |
| 5 | Version basis | the licence row covering the date in question, per licence number | the register ships the amendment history beside the current state with its own effective span; C1, exactly one facility row per licence number covers the position date, asserted. The golden never reads the register; ask B does |
| 6 | Denominator | capacity against 1.15 times projected 2027 weekly demand, the base being the area's 2026 contract year treatments a week | filed in clause 4.3 in the standard's own words, asserted present in the shipped document (SF11, SF17) |
| 7 | Weighting | none: an area's figure is the sum over its sites | cannot move the answer; no weighting choice exists, asserted as a sum identity per area |
| 8 | Window length | the ceiling's four-year look-back | C1, measured: 12, 24 and 48 months return the same integer at all 40 sites (SF15) |
| 9 | Boundary inclusivity | at or above the required figure | C1, no area within 6 per cent of its line on any of the four bases, worst 6.02 per cent of required (SF12) |
| 10 | Rounding path | the required figure rounded once, at the area level, **up** to the next whole treatment slot | clause 4.4 files the direction and the asking sentence states whole numbers; SF13 asserts the direction present in the shipped document, every area's verdict identical under the unrounded figure, the floor and the ceiling, and every required figure 0.06 or more from a whole slot and from a half |
| 11 | Tie-break | which of the short areas comes nearest the standard | C1 on the data: the nearest area is nearest under the unrounded figure and under all three roundings, with 2 slots of daylight to the runner-up on the tightest reading, asserted; no area's capacity equals its required figure |
| 12 | Maturity and censoring | the 2026 contract year complete at the as-of date, the extract pulled after the filing run-out | clause 4.4 files the ninety day run-out and the transmittal carries the pull date; asserted that no encounter in the pack carries a service date after 31 December 2026, so the contract year is complete on the extract |
| 13 | Order of operations | positions, then sessions a week, then the category figure, then the area sum, then the standard | the steps commute (multiplication and summation), asserted; the only non-commuting step is rounding, closed at axis 10 |
| 14 | Row order | the ceiling is a maximum over a set and the totals are sums | C1, asserted invariant over permutations of the encounter tables |
| 15 | Duplicate resolution | one row per distinct facility where a file holds two | C1 on the main path: no claim line in the register names a contracted site and no claim line repeats, asserted; the duplicates that exist are the 2026 filing's five rows under a corporate licence number and the register's amendment rows, both outside the main population, where asks C and B read them |
| 16 | Identity normalisation | the directory's site identifier, joined to the licence register on the service address and to the encounters on the service facility | C4, the raw tax-identifier join merges three sites and is mapped to the contract's unit sentence (SF16); the crosswalk is the directory's own |
| 17 | Netting against gross | none: capacity and demand are gross counts | cannot move the answer; nothing nets, asserted |
| 18 | Dimensional units | treatments, positions, sessions, minutes; `service_minutes` is minutes | C4, reading `service_minutes` as hours makes every one of a site's intervals overlap and files a ceiling above the site's attested stations at 40 of 40 sites, which the file itself refutes; asserted as a named wrong cell |
| 19 | Code and status semantics | the encounter status (completed, cancelled, no show) and the directory's contract intent, both plain words, no dictionary shipping | the governing contract defines the intent; SF3 makes the status unable to move the ceiling under any reading; never the stump |
| 20 | Integerisation | positions are whole by construction, a count of concurrent treatments; slots are counts | C1 by construction: no floor, round or remainder choice exists on the graded quantity, and the one rounded figure is closed at axis 10 |
| 21 | Clause scope | Schedule 4 governs the 2027 network year and the sites in scope for it | filed in clause 4.1's own first sentence, asserted present; the 2026 filing states its own network year and position date, and its site set differs from the 2027 population by six sites or more |
| 22 | Forward window contents | the 2027 network year is not yet contracted | the plan's 2027 enrolment projection by service area ships as the driver file for the uncovered span; nothing else about 2027 is needed, and no 2027 treatment is in the pack |

## Literal reader
A reader who executes `prompt.txt`, Schedule 4 of the network agreement and the licence register's own
status words word for word, inferring nothing the files do not say, reaches the golden: clause 4.1 fixes the
population at the 40 sites carrying a 2027 contract intent on the current attestation cycle, 4.2 fixes
the unit and defines deliverable treatment positions as the positions a site can operate simultaneously
without naming a route to them, 4.3 fixes the comparison and the standard, and 4.4 fixes the rounding. The
only step the text leaves open is the measurement of those positions, and every reading of a site's own
record returns the same integer: 40 of 40 sites on the record maximum, all 4 yearly maxima, all 48 monthly
maxima and the 12 and 24 month look-backs, with one more than that integer never running. The 17 rows of
`## Semantic fork table` enumerate every other silence and each returns the golden or violates a quotable
shipped sentence; no row is closed by this note or by the write-up. The easy answer comes from an easy method
on the same literal estimand, the directory's own attested station count in place of a measurement, which
files 4,668 weekly slots against the golden's 3,886.

## Oracles
Every control, published figure, reconciliation column and corpus, with what it confirms on the wrong path.
Nothing ties only under the golden and nothing ranks the twelve areas against the standard. Each line is
asserted in `generator/checks.py`.

| Control | What it confirms | Its wrong-path reading | Screen |
|---|---|---|---|
| `state_adequacy_filing_2026.xlsx` (the context artifact, ask C's source) | per area, the 2026 contracted sites, their licensed stations then and the treatments delivered in 2025 | a solver reconciling its station column against the licence register ties on every facility-numbered row, on R1's input, and learns nothing about any station basis | asserted: it carries no weekly-slot figure, no utilisation figure and no adequacy verdict; its position date is 1 January 2026 and its site set differs from the 2027 population by six sites or more; it also carries rows under a corporate licence number, which is ask C's own device |
| `enrolment_projection_2027.csv` | the growth factor the standard's demand side uses | identical under all four rungs, because every rung shares the demand side | ties on every basis; cannot score a station basis |
| `network_agreement_2027_capacity_terms.pdf`, Schedule 4 | the population, the unit, the window, the comparison, the standard and the rounding | quotable against no station basis, because it names none | the pin sits once, at authority level 2; the counter-pin sweep over both documents for the constraint's nouns beside a licensing verb returns nothing |
| `encounter_extract_transmittal.json` | the extract's pull date, its two tables and its row counts by service quarter | ties under every rung, because it counts encounters and not capacity | asserted: its quarter counts sum to the shipped rows, 639,009, and it carries no capacity or position figure |
| `out_of_network_payments_reconciliation_2026.xlsx` | the register's own control totals by adjudication quarter | it ties exactly to the rows the register holds, claim header lines included, so a count-tie check passes on a unit total that counts a sixth of the claims twice, which is ask A's primary device | it reads no contracted site and reaches no station basis; asserted zero device rows in the main population |
| `nemt_trips_2026.csv` (distractor) | 2026 transport trips by area and month | a solver ranking areas by trips ranks them by volume | asserted: the six areas with the most trips are not the golden's six short areas, so no shipped artifact ranks the candidates on the decision question |
| `licence_fee_schedule_2026.pdf` (distractor) | the annual fee a station band attracts | a solver could read the fee bands as a capacity authority | asserted: it carries no station count for any named site and no plan or licence identifier |

**No calibration corpus and no confirming back-test ships.** The method is forced by the design, which is
`determinism-check` Part 5 case 1, so no filed selection criterion and no closed-data confirmation is needed
and none is built. **No voice argues a method:** no memo, briefing, draft or stakeholder figure carries a
capacity number or a method for one, asserted over every document in the pack.

## Ask sheet
Three asks, each a reconciliation or an audit trail of an input the call consumes (H18), each computed on
rows the call never reads. The main call's declared row population is the 2027 contract-intent sites' own
treatment encounters, and the encounter database holds those sites and no others, asserted. Every figure
below is measured on the cut pack.

**Ask A, out-of-network treatment volume.** By half of 2026 and the area of the site treated, the
treatments the plan paid for at sites it holds no contract with, and their share of all the area's
treatments that half. 24 counts and 24 shares, 48 graded figures, whole treatments and shares to one
decimal, both in the asking sentence.
- H18 home: the audit trail of the demand side, from the payment register through rows the call never reads to the area's own total.
- Use: the network unit sizes the leakage it is contracting to pull back in.
- Two bases are closed rather than left open, because the determinism judge named both: clause 4.4 files that a treatment is counted in the period of the contract year in which it was delivered, and the asking sentence names the area of the site treated. Both are conventions, and neither names a method.
- Primary device (D1 duplication with D9 self-validation, silent): the register writes a claim header line, `line_no` 0, for about a sixth of its claims, carrying that claim's own treatment count beside the service lines that make it up, as a claims extract does. Summing `treatment_units` over every row counts those claims twice, and the file's own reconciliation workbook reports the same doubled unit total by adjudication quarter, so the count-tie check passes on a figure the ask cannot use. Nothing names a header line and the key `claim_id` with `line_no` is unique, so key uniqueness and the unmatched-join sweep both pass.
- Remedy: a reconstruction, one treatment count per claim, the header line where the register writes one and the service lines where it does not, one correct answer.
- Measured: summing every unit row moves **24 of the 48** figures; leaving the run-out supplement out moves **12**; grouping on the register's own `member_residence_area` instead of the area of the site treated moves **24**.
- Path: 6 files and 13 columns.

**Ask B, the licensed supply by area.** By area, the licensed dialysis and infusion sites the state register
holds at the position date and their stations. 24 graded figures, whole sites and stations.
- H18 home: a component of the call's case, the supply the plan could contract against the supply it does.
- Use: the network unit states the supply left to approach in a short area.
- Primary device (D2 version with D7 keys, silent): the register ships the amendment history beside the current state, so a row whose `effective_to` has passed still reads `active` in its own words, and a licence number that lapsed in 2026 was reissued to another facility at another address. The current state has to be rebuilt per licence number from its own span. The register's summary sheet counts licence numbers, so it ties on its own basis and not on the ask's.
- Remedy: a reconstruction, the row covering the position date per licence number, corporate umbrella rows excluded, one correct answer; spotting the duplicate addresses does not settle which rows are current.
- Measured: filtering on `licence_status` alone moves 12 of the 24 figures; counting corporate umbrella rows as sites moves 24.
- Path: 1 file and 8 columns.

**Ask C, the sites the 2026 filing counted that carry no 2027 contract intent.** By current service area,
how many and the stations they were licensed for then. 24 graded figures.
- H18 home: a reconciliation of the context artifact to the population the call declares.
- Use: the network unit explains to the state what moved between the two filings.
- Primary device (D9 self-validation with D1 duplication, silent): the filing's per-area totals are true only under the service areas in force for the 2026 network year, four of which the plan redrew for 2027, and five of its site rows are filed twice, once under the operator's corporate licence number, so the filing's own area summary ties to its own rows while the ask's answer does not. The battery's unmatched-join and key-uniqueness checks both pass, because the duplicate rows carry a different licence number.
- Remedy: a reconstruction, one row per distinct facility resolved through the register row covering the filing's own position date, then placed in the area the directory records now, one correct answer.
- Measured: counting filing rows on the filing's own area labels moves 20 of the 24 figures; resolving the licence numbers at the position date of the as-of extract instead of the filing moves 6.
- Path: 3 files and 10 columns.

**The main population's zero counts.** Asserted by count in `generator/checks.py`: no out-of-network claim
line names a contracted site; the encounter database holds the 40 contract-intent sites and no others; no
duplicate claim line in the main population; and the call's network total is unchanged with every ask device
in place.

| Hazard | Asks it moves | Figures it moves |
|---|---|---|
| the claim header line summed beside its own service lines (ask A's primary) | A | 24 of 48 |
| h1 the run-out supplement's vintage | A | 12 of 48 |
| h2 the register's two grains and its reissued numbers | B, C | 24 of 24 and 6 of 24 |
| h3 the register's member-residence area against the area of the site treated, now a stated basis | A | 24 of 48 |

**The referee.** The extract transmittal's treatment count by quarter arbitrates ask A's designed
disagreement without handing over a level: it ties under both the adjudication and the service-date readings
for the contracted sites and so settles nothing about the non-contract rows.

| Ask | Cracker's path (lands the call, runs the hygiene battery, executes every filed rule, matches every control) | Figures it reaches | Verdict |
|---|---|---|---|
| A out-of-network volume | takes the filed service-date basis and the asked area of the site treated, then ties its totals to the reconciliation workbook, so it sums every unit row and reads the main file alone | 0 of 48 | miss |
| B licensed supply | filters on `licence_status` and counts every active row in the area, corporate rows included | 0 of 24 | miss |
| C the dropped sites | counts filing rows on the filing's own area labels | 4 of 24 | miss |

**Mirror leakage:** 4.2 per cent of the ask weight, measured on the cut pack: the response off the call
reaches 4 of the 96 ask figures, all of them in ask C, and keeps no ask whole.

**Pair ceiling:** 30.8, on Part 0's weights of 38 for the recommendation and critical components, 7 for
instruction following and 55 for the asks: the response that lands the call keeps 47.3 and the best
response off it 14.3.

**Measured by:** generator/ceiling.py, which walks the cracker's path and the mirror's path over the shipped
bundle in code and scores every ask figure each produces against the golden at the golden's own rounding.
Stump power is argued on paper and measured by the portal alone (`CLAUDE.md`, the STOP block of 2026-10-27);
no reader measurement is run, waited on or owed, and the sensitivity band below is the paper measurement's
own.

**Sensitivity**, printed by the same script: if the cut pack let the cracker keep nothing, a tenth, a fifth,
three tenths or two fifths of the ask weight, the pair would read 29.6, 32.4, 35.1, 37.9 or
40.6. The ladder, not the asks, is what keeps a response off the call.

**The span floor, a stated exception.** `supplemental-stumping` Part 4 asks for eight or more files on each
ask's own path and ten to fifteen columns; the measured spans are 6 files and 13 columns for ask A, 1 file
and 8 columns for ask B, and 3 files and 10 columns for ask C. The exception is taken deliberately and
ruled on 2026-10-27: the evidence these three reconciliations need genuinely sits in those files, and
routing an ask through files it does not read is the idle complication `dataset-generation` section 12 sends
back. The floor is a proxy for device strength, and the thing it proxies for is measured directly here and
came out strong: the cracker reaches 0 of ask A's 48 figures, 0 of ask B's 24 and 4 of ask C's 24, the pair
ceiling is 30.8 and the mirror leakage 4.2 per cent of the ask weight.

## Layer 1 inventory

One row per item in `## Three rules`'s `Layer 1:` line, with the system that writes it, the file it sits in
and its asserted neutrality on the call. Each is the R2 block of `generator/checks.py`.

| Item | The system that writes it | Where it sits | Asserted neutral because |
|---|---|---|---|
| a directory refreshed on each site's own attestation cycle | provider data management, one cycle a year | `provider_directory_2027.csv`, three cycles | every cycle agrees on every site's service area, and the 2027 contract intent is recorded on the current cycle only, so the cycle choice moves the attested station count (rung 0's input) and nothing the golden reads |
| licence rows at both the corporate entity and the service address | the state licensing authority's register | `state_licence_register.xlsx`, `holder_type` | the golden never reads the register; a corporate row equals the sum of its own facility rows in its area (SF8) |
| two encounter layouts across a clearinghouse change | the encounter data warehouse, 2025 cutover | `treatment_encounters.db`, two tables | either layout alone returns every site's positions, asserted at 40 of 40 sites on each |
| treatment start and stop in local clock with no offset on the 2023 and 2024 feed | the same warehouse before the cutover | `encounters_2023_2024.service_start` | an overlap count inside a site is invariant under any site-level offset, and no interval spans the autumn fall-back hour (SF4) |
| rosters by position rather than by named staff | clinical operations | `staffing_roster_2026q4.csv` | the roster carries sessions a week and clinical hours a month, from which no position count is derivable; one row per site at the position date (SF5) |
| sites that moved address and kept their identifier | provider data management | `provider_directory_2027.csv`, three sites | the golden joins on `plan_site_id`, which is one to one with a site; an address join would lose those three, a named wrong cell |
| a group practice billing three sites under one tax identifier | claims operations | `provider_directory_2027.csv`, `tax_id` | clause 4.1 files the unit as the Site; the tax-identifier reading merges the three and files 4,512 slots, a named wrong cell (SF16) |
| cancelled and no-show encounters carried with no stop time | the warehouse, scheduled slots nobody attended | both encounter tables, 7,576 rows | no interval is constructible under any reading, and each sits where the site was running at least two positions short, so the ceiling and all twelve verdicts hold either way (SF3) |

## Pre-ship check

The build stage's gates, each re-run on the pack as it now stands, after the second leak read's four
procedural fingerprints were fixed. The pre-ship block proper is stage 5's. The main call itself does not
ship: the re-judge's Gate C finding sent architecture 3 back and the entry under "## Tried and rejected"
and `determinism_check_report_pass4.md` carry the ruling.

| Gate | Result |
|---|---|
| `generator/checks.py` | 682 assertions passed: the three-rules block (R1, R2 per mess item, R3a, R3b, R3c), SF1 to SF17, the ladder, the named wrong cells, the legibility block, the ask separation line, the oracles, the input gates, the realism sweep, the 22 closure axes, the documents, the write-up, the five owed figures and the five procedural shapes (no id column stepping by a constant and each by at least six distinct amounts, the area names in code order not in alphabetical order, more than two site-name shapes, no two sites sharing a name or an address, no workbook stating a position or pull later than its own file date) |
| `generator/verify.py` | PASS, reading only the bundle on its own code path: 40 sites, 12 areas, 96 ask figures, every graded figure recomputed, the rounding direction and the delivery-period convention read out of the agreement's own text |
| two consecutive rebuilds | byte-identical `target/` across all 13 files and byte-identical `target.zip`, md5 `c0e0dfcfcc8ecf0bc864f9e4b9eb8d7a` |
| `figures_check.py` | PASS, 146 figures in blocks 1 to 4, 0 absent from `generator/figures.json` |
| the realism sweep | in `checks.py`: no round headline, the required figures not all alike, no repeated yearly count, personas from the card, every container's application and version pair consistent with a title and an author, each document's producer the body that issued it, the operator column in no fixed order with uneven site counts and no name against its own service category, dates coherent per document with each PDF carrying its own issue date, no em dash in the bundle |
| `golden-realism` | run after the figures froze: named sheets, frozen header, per-column number formats and alignment, a chart whose title states the finding, a basis and position line, print area set |
| `reduce-house-fixes` | H1 containers scrubbed and asserted, H2 every figure emitted, H4 the archive's 13 members equal the declared list, H7 the archive cut last from the final tree, H8 every citation resolves, H9 no describing file, H16 dates coherent, H21 invented names clear of real ones, H29 the bound figures read against the quantity they bound, H33 one entry point writes `figures.json` |
| `leak.py --asof 2027-02-19` | REVIEW, no LEAK, every REVIEW line answered in `## Leak check` |
| `guard.py surface` and `heart` | surface clean with only the card's own personas, heart WARN at a nearest driver of 0.05 (task181, lineage), no BLOCK |
| `precut.py` | exit 0, 52 checks, 0 FAIL, 0 WARN |
| `voice-check.py` | PASS, 998 characters |
## Leak check

`leak.py --asof 2027-02-19`: **REVIEW**, no LEAK, 13 files read. The pack ships no file whose job is to
describe the data, asserted by name and by content over every file and every workbook sheet, so every
convention the call leans on sits in Schedule 4 at authority. Architecture 2's solver's-eye read was removed
from `leak_check_report.md`: it was taken on a pack that no longer exists. The isolated leak reader is stage
4's and the author's to spawn; no scored or solving reader is run on any build (`CLAUDE.md`, the STOP block
of 2026-10-27).

The five REVIEW lines, answered:

- **sweep 3, `licence_fee_schedule_2026.pdf`, "golden figure 105 appears".** 105 is ask C's station total for
  one area and the sweep found it inside the fee `USD 2,105`. A substring of a currency amount in a fee band;
  the fee schedule carries no station count for any named site, asserted.
- **sweep 3, the agreement, "golden figure 4.5 appears".** The clause number of 4.5 Corrective action. It is
  filed in `figures.json` as a constant read from `docs.py`, so the write-up's citation and the document
  cannot drift apart (H2).
- **sweep 3, the agreement, "carries 12 of 13 distinctive words of the committed call".** The call's own
  nouns are network, weekly treatment slots and service areas, which Schedule 4 must use because it files
  the unit and the standard. It carries none of the call's figures, asserted: no weekly-slot figure, no
  utilisation figure and no adequacy verdict anywhere in the pack.
- **sweep 4, `licence_fee_schedule_2026.pdf`, "3 of 25 stump-paragraph terms appear".** The terms are
  station, carries and licence, which is what a facility licensing fee schedule is about. It carries no
  station count for any named site, asserted.
- **sweep 4, the agreement, "6 of 25 stump-paragraph terms appear".** The terms are positions, deliverable,
  directory, licence, encounter and demand. Five of the six are the estimand's own parts, which section 1
  requires filed; the sixth, deliverable, is the unit's term. The route words are swept for and absent:
  `concurrent`, `overlap`, `greatest number`, `at one time`, `effective capacity`, `water loop`,
  `compounding hood`, `busiest week`, each asserted through the same extractor as a positive control that
  finds a sentence known to be there.

**The single-use test, run by hand on every file.** The encounter database is the standard's own demand
source as well as the ceiling's evidence; the licence register is ask B's population and rung 1's input; the
2026 filing is ask C's source and the state's own record; the reconciliation workbook is the register's own
control total; the transmittal is the extract's own receipt. No file has one use, and no sentence exists only
to make a solver notice a structure.

## Tried and rejected

- **Architecture 3's decisive step is spent: the stump lived in the fork, measured 2026-10-27.** The stage 4
  re-judge returned NOT_DETERMINISTIC, `competing_defensible_answer` on the MAIN CALL via
  `underspecified_objective`, and the finding is not repairable. Schedule 4 clause 4.2 defines deliverable
  positions as "the treatment positions a Site is able to operate simultaneously" and nothing files what
  evidence fixes that, so three readings are reachable and each changes the call: the golden's concurrency
  sweep gives 274 positions, 3,886 slots and 6 areas below the standard; the directory's attested stations
  give 327, 4,668 slots and 3 areas below; the register's licensed stations give 351, 5,006 slots and 2 areas
  below. Only inference, or the write-up's own "Not the stations the directory attests", picks the golden.
  Every golden figure reproduces, so there is no `solution_incorrect`: the defect is that the estimand's unit
  is not forced.
  The judge's own suggested fix is the thing rule 3 bans. It asks for a sentence in 4.2 filing that positions
  are evidenced by "the site's own treatments running at the same time in the encounter extract", and
  "running at the same time" IS the concurrency sweep, so taking it would make the decisive step rule
  application whatever the determinism verdict (`CLAUDE.md` first section, `/fix-determinism` step 3).
  Then the stump test, and it fires. The default path's entire error is taking the attested 327. Any closure
  that forces the golden reading tells the analyst not to take it, and the construction is then the only
  route left, so closing the fork in either direction makes the default path land on the golden. That is the
  stop condition verbatim and eight builds have died on it. Leaving it open to keep the stump is explicitly
  banned.
  Two escapes were weighed and both fail. A selection criterion naming the evidence source in general terms
  (the Site's own delivered service record, and not a count it attests or is licensed for) is section 1's
  named escape and files WHAT rather than HOW, but its second half is the stump itself: "not the attested
  count" is the whole insight. And deleting the attested and licensed counts from the pack closes Gate C and
  kills Gate F at once, because the construction becomes the only available route and nothing is skipped.
  So Gate C and Gate F ride one dial here with no middle, which is the finding task184 and task188 each
  recorded from their own slots.
  This supersedes my ruling earlier the same day that the build ships with the Gate F risk recorded. That
  ruling answered the leak reader's observation that clause 4.2 makes the exposure visible, which is a Gate F
  weakness. The judge has since shown a Gate C failure on the main call, which is a different and worse
  thing, and the evidence beats the ruling.
  **What survives for the redesign.** The world, the pack and the ask layer are sound and measured: 652
  generator assertions, verify recomputing every graded figure on its own code path, two byte-identical
  rebuilds, 146 figures with none absent, precut at 52 checks with 0 FAIL and 0 WARN, cracker 0 of 48, 0 of
  24 and 4 of 24 with a pair ceiling of 30.8 and mirror leakage 4.2 per cent, and the nearest-area ask now
  forced under all four roundings (Durnsfield 19.625, 20, 20, 19 against a runner-up pair at 22, 22, 23, 22),
  which the judge confirmed independently. The ceiling's own convergence also holds: the record, yearly and
  monthly maxima, the 99th and 99.9th percentiles, either table alone, a UTC clock and both interval
  conventions all give the same 274. The next architecture keeps this world and moves the decisive step off
  the unit of the estimand.

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

- Stage 3, the ceiling's first construction: the first session of every day running every position
  (2026-10-27). It gives the hard plateau SF1 needs and it also gives the day a signature, a flat top at the
  same clock hour every day, and it put the most treatments starting inside a two-hour window at exactly the
  position count at 40 of 40 sites. The saturating round is now drawn per day and the opening ramp is as wide
  as each site's own plateau can carry, measured per site: the busiest hour of the day sits at a site's modal
  hour on a median of 0.29 of its site-days over a median of 10 distinct hours, and no window width
  returns the position count everywhere (18, 36 and 25 of 40 at one, two and three hours).
  The trade is visible and taken deliberately: widening the ramp shortens the plateau, so a site now holds
  every position occupied for 0.062 to 0.213 of its treating minutes, which leaves the 95th and 99th
  percentiles of occupancy on the position count at 40 of 40 sites and the 90th at 27 of 40. SF1 is
  closed on the maxima, and a percentile under 1 is refuted by the record itself.
- The extra closed shifts placed at sites whose stations all run (2026-10-27): the busiest week then reached
  1.27 to 1.49 times the site's current attested weekly capacity, a visible impossibility at exactly the
  sites the ladder leans on. The extra closures are now searched among plant-constrained sites in clear
  areas, accepted only while every ladder condition holds, and the busiest week over the current attested
  capacity is asserted at or under 1.05, measured 0.988.
- Member identifiers rotated by position and round (2026-10-27): a patient could then take two treatments at
  a site on one day, and the most distinct members in a day equalled the position count at one site, which is
  a one-group-by route to the decisive quantity. The panel now splits into cohorts, haemodialysis on the odd
  and even weekdays and infusion one weekday in a few, nobody takes two treatments at a site in a day, and
  the most distinct members in a day is at least 1.38 times the position count at every site.
- The 2026 filing's area labels as ask C's primary, closed in the asking sentence (2026-10-27): with the ask
  reading "by current service area" the redraw alone is a join, so the primary moved to the filing's
  duplicate rows under a corporate licence number and the redraw became the hazard that punishes a reflex
  group-by on the filing's own area column. Measured: counting filing rows on the filing's labels moves
  20 of ask C's 24 figures.
- `score_reader.py` and any reader measurement of the ask layer (2026-10-27, from `CLAUDE.md`): the STOP
  block retires the solver flow, so the pair ceiling and the mirror leakage are the paper measurement made
  exact in `generator/ceiling.py` on the cut pack, plus the portal. Where stage 2's ask sheet said the
  isolated reader is the measurement, that sentence described the retired practice and is corrected.

- Stage 3 containers and naming, four defects the stage-4 leak reader found and the author verified
  (2026-10-27), each fixed in the generator with no graded figure moving (`figures.json` byte-identical
  before and after): the three workbooks read `<Application>Microsoft Excel</Application>` beside
  `<AppVersion>3.1</AppVersion>`, which is openpyxl's own version and an impossible pair, now 16.0300 with
  the issuing body as the Company; `licence_fee_schedule_2026.pdf` carried the health plan as its Producer
  and Creator although it is the state licensing authority's own fee schedule, so each document now carries
  the body that issued it and the register's workbook already did; both PDFs shipped an empty Title and
  Author, now filled from each document's own masthead; and the operator column cycled eight names in fixed
  order through all 40 sites, which anyone sorting by site identifier sees, and produced systematic
  mismatches such as an infusion-named operator running a haemodialysis centre. Operators are now drawn per
  site from the operators that serve the site's own category, on weights that give one group 8 sites and
  three operators 1 each, and the realism sweep asserts all four: a consistent application and version pair
  with a title and an author on every container, no fixed-order period of 1 to 12 in the operator column,
  uneven site counts, and no operator whose name names one service category while its sites deliver
  another.

- The absolute-shortfall reading of "nearest the standard", left to a rounding (2026-10-27, the
  determinism judge, NOT_DETERMINISTIC on Gate C `competing_defensible_answer`): with the required figure
  rounded to nearest, Bexhollow and Durnsfield were both 20 slots short, so the golden's Bexhollow held
  under one of five readings and the weakest one, the shortfall as a per cent of required. Closed in the
  order the judge and `determinism-check` both rank: the golden moved to the absolute shortfall in slots,
  which is what "nearest the standard" plainly means; the data was then moved so one area is nearest under
  the unrounded figure and under every rounding, Durnsfield at 19.62, 20, 20 and 19 against Bexhollow's
  22.07, 22, 23 and 22, which is 2 slots of daylight on the tightest reading, built by adding one treatment
  at a time to a non-nearest short area's largest site; and clause 4.4 now files the direction, up to the
  next whole slot, because a required figure is a minimum. No pin was spent on a tie-break.
- Ask A's adjudication-basis primary (2026-10-27, in the same pass): the judge named the date basis and the
  member's residence area as unstated alternatives on ask 4, and closing both, one at authority and one in
  the asking sentence, would have left the ask with no primary. The primary moved to the register's own
  claim header lines, a rollup above its own parts whose unit total the reconciliation workbook reports as
  the file holds it, so the count-tie check still passes wrong: measured at 24 of the 48 figures, with the
  run-out supplement at 12 and the residence-area column, now a stated basis, at 24. The cracker still
  reaches 0 of ask A's 48 figures and the pair ceiling is unchanged at 30.8.
- The projected-demand component computed back out of the rounded required total (2026-10-27, the judge):
  `cc3` read 3,092 where the quantity is 3,095, because the generator divided the summed, rounded required
  figure by the cushion instead of summing each area's own growth times its own weekly base. It is now
  computed forward and the verifier recomputes it from the bundle.

- **Architecture 4 candidate C1, the conversion certified on a conditioned entry: refused on its own
  arithmetic, 2026-10-27, measured over 24 seeds at two settings.** A licensure written paper, twelve closed
  windows, no item carried between any two papers, the standard certified at a base window and carried forward
  by equating each paper's mark distribution to the preceding paper's; the decisive step is that each window's
  entry is part returning candidates whose marks are conditioned on having fallen below the preceding cut, at a
  share that swings with the preceding paper's severity, so the conversion is certified on the first-attempt
  distributions. Graded on the open window's carried cut in marks: the decisive step is worth a mean of 3.21
  marks (re-entry 0.55, gain 0.35) and 4.04 marks (re-entry 0.30, gain 0.25), the licensed family spreads the
  same cut a mean of 2.38 and 2.79 marks (maximum 6 and 7), and the golden estimator's own bootstrap standard
  deviation is 1.09 and 1.10 marks, so the step exceeds the spread plus the interval in only 10 of 24 and 12 of
  24 seeds, with the means at 3.21 against 3.46 and 4.04 against 3.90. The rung beneath kills it outright: first
  attempts equated straight to the base window, which is one equating instead of eleven and therefore the
  cheapest licensed construction, names the golden's bin in 12 of 24 and 7 of 24 seeds. Graded on the
  carry-forward count instead the estimator is worse, a bootstrap standard deviation of 845 counts on a mean of
  11,390, with the common-mix rung within 6 counts of the golden on one of 8 seeds. The discretising rescue
  fails too: against a filed tolerance of 2 marks, 8.04 of 11 per-window verdict cells sit inside one bootstrap
  standard deviation of the line and the direct-to-base rung reproduces the whole 11-cell verdict set in 9 of 24
  seeds. Card drafted and cleared (guard WARN, exit 0, nearest driver 0.06 against task450) and deliberately not
  registered.
- **Architecture 4 candidate C2, the path through a chain of administrations: refused, measured inside C1's
  family spread.** Chaining the cut window by window and equating each window straight to the base are both
  standard equating practice and neither is refutable by a shipped fact, and they spread the graded cut 1 to 7
  marks against a decisive step worth 2 to 7 marks, which is 0.59 to 1.75 times the step's own worth. Filing the
  path makes the carry the literal execution of a filed clause; leaving it free is Gate C on the main call,
  which is architecture 3's death restated in another world.
- **Architecture 4 candidate C3, marker severity conformed from an incomplete double-marked overlap: refused,
  measured over 12 seeds (28 markers, 2,400 scripts, 12 per cent double-marked, allocation by centre batch).**
  The joint severity solve and the one-line regression of the recorded mark on marker and script indicators are
  one object, maximum absolute difference 0.000e+00 across all 12 seeds, so what closes the estimator family is
  what makes the construction one line. The overlap graph is connected in only 3 of 12 seeds and splits into 2
  or 3 components with 1 or 2 isolated markers in the other 9, where severity is not identified at all, which is
  Gate B rather than Gate C. In the 3 connected seeds the decisive step moves the graded cut 0.03, 0.42 and 0.48
  marks while the licensed severity family (the joint solve, two spanning-tree chainings of the pairwise mean
  differences, and each marker's own mean) spreads the same cut 1.40, 1.49 and 0.75 marks, which is 1.6 to 46
  times the step's worth. The dial is one-ended: raising the double-marking share until the graph connects is
  exactly what makes each marker's severity readable off their own overlap, which is one group-by.
- **Architecture 4 candidate C4, item-bank exposure moving observed difficulty: refused without a prototype.**
  It is anchor drift under another name, which the author banned as the gravest clone finding against task450,
  and the mechanism is already spent in the corpus at task249, whose deciding quantity is each form's
  repeat-examinee exposure gain in a certification examination with resits in any later window.

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

- Identifiers, area names and site names generated by arithmetic (2026-10-27, the second leak read's four
  procedural fingerprints): abandoned and replaced. Plan site ids stepped by 37, licence numbers by 23, street
  numbers by 53, tax ids and claim, member and encounter keys by their own constants; the twelve area names ran
  A to L in service-area-code order; every site was named "<Locality> Dialysis Center" or "<Locality> Infusion
  Center"; and the licence register reported a position date three days after its own file date. Each is now
  drawn from its own stream, off the world's: ids and street numbers rise with uneven gaps, the code to name
  mapping is shuffled, a site is named from fifteen templates with fourteen distinct shapes appearing over the pack's 72 sites, one carrying an operator's brand, and every
  document carries its own date and states nothing later than it (the register the evening of the position date
  it reports, the two plan exports the next morning, the agreement the week its board approved it, the fee
  schedule the week before it took effect), so the three workbooks no longer share one timestamp either. `checks.py` asserts all five shapes (30 assertions):
  twelve id-bearing columns each step by at least six distinct amounts and none by a constant, the names in
  code order differ from the names in alphabetical order, more than two name shapes appear, no two sites share
  a name or an address, and no workbook states a position or pull later than its own file date. No numeric
  figure moved: `figures.json` differs only in the 40 site-id labels, whose slot values are identical in order,
  and in the name of the nearest short area, which is the same area (SA-04) under the name the shuffle gave it.
- The area names in the live sections of this note (2026-10-27): remapped with the shuffle, so every table above
  "## Tried and rejected" names the area the pack now names. The short set, the flip set and every figure are
  per service area code and unchanged. Entries below this heading keep the names they were written with, since
  the section is append-only: SA-04 is Durnsfield in the history above and Hesper Vale in the pack.
- A synthesised `sharedStrings.xml` (2026-10-27): refused. The three workbooks are system exports, a register
  extract, a state filing and a claims reconciliation, and an exporter that writes cell text inline is in
  character for all three; rewriting every cell's XML to add the part risks the files for no realism gain. The
  empty `<workbookProtection/>` element the writer emits was stripped instead, because a book with no
  protection set carries no such element.

- Architecture 4 candidate 1, the area's 2027 weekly demand projected off the standing treatment panel
  (prevalent members times each member's own regimen times projected enrolment) instead of off 2026
  delivered throughput (2026-10-27, measured on the pack as cut): refused, 0 of 12 verdict cells. The
  panel route raises the required total 222 slots (8 to 38 per area) and every short area gets shorter
  while every clear area stays clear (SA-02's gap -23 to -31, SA-05's +63 to +25), so the correction walks
  one way and never reverses and a response on the filed base lands the whole call. The bin arithmetic
  fails twice over: the nine defensible panel readings spread the required total 1,686 slots (3,633 to
  5,319) and the standing-panel readings alone 92, against a decisive worth of 222, which is also under
  architecture 3's smallest rung gap of 296 slots; the regimen construction (modal, maximum or mean
  attended week) moves it another 53.
- Architecture 4 candidate 2, the demand base read as the level the record has reached rather than the
  contract year's mean, because six of forty sites stepped their panel down in April 2025 (2026-10-27,
  measured): refused on the fit interval. Every parameter-free level construction moves 0 of 12 verdict
  cells (tail completion +45 slots, trailing 13 weeks +62, trailing 26 weeks -14), and the only
  construction that moves the call at all is a four-year extrapolation, which clears SA-02 and SA-07 for a
  worth of 118 slots while its own prediction standard error on exactly those two cells is 45.6 and 45.8
  slots against a 23-slot capacity gap, twice the margin it has to clear. It also extrapolates a one-off
  shift closure as a continuing decline (SA-02 predicted 11,142 against 2026's 13,609), and a fitted base
  is a model of the measurement, which the skills bar as the decisive step.
- Architecture 4 candidate 3, each site's staffed sessions a week reconstructed from the record's own
  treatment rounds instead of read off the roster's `treatment_sessions_week` (2026-10-27, measured):
  refused, no arithmetic-closed piece exists. The encounter record carries no session, shift or chair key,
  so a per-position session count needs a round window, and the four defensible widths put the network
  between 2,408 and 9,380 weekly slots with the short count at 10, 6, 2 and 0 of 12, a spread of 6,972
  slots against a decisive worth of 222 to 616; the three parameter-free turn readings still spread 873.
  The second file that might have closed it carries nothing: `clinical_hours_month` takes exactly one
  distinct value in each of the six (sessions, category) cells across all 40 sites, so it is a function of
  two columns already inside clause 4.2's own formula. Clause 4.2 also files the roster as the source of
  the session count, so the reconstruction contradicts a shipped sentence and is an official decoy besides.


## Architecture 4: the cell screened and refused, measured 2026-10-27

The author fixed the pairing (education-learning-sciences, the item-response-theory-test-equating task type,
objective etl, verified as the only task type in that domain the taxonomy tags for ETL) and barred task450's
anchor-drift cell, its campus designation, shape 14, the etl_conformance with causal_design pair and its spine
grain, and barred `org_family: university_or_school` against task204. None of that is what refused the draw. The
pairing is legal, the cell holds exactly one card (task450), and the candidate driver taken furthest sat at 0.06
against task450 on the text screen with the abstraction test separating them as well, since no item is carried
between any two papers and no item is ever compared. What refused the draw is arithmetic, and it is one
structure rather than four accidents.

**The wall.** Every decisive step that carries a reported number across administrations runs through a
conversion, and a conversion is an estimated object rather than a records-fixed one. There are three ways to
make it determinate and all three fail in this cell. File the population the conversion is certified on and the
path it is carried along, and the carry becomes the literal execution of filed text, which rule 3 bars as the
decisive step. Leave either free, and two standard constructions each file another figure, which is Gate C on
the main call, and that is architecture 3's death in this slot written in another world. Make the records force
it, and the forcing is exactly what a strong analyst reads: measured, the cheapest licensed neighbour names the
golden's bin in 7 to 12 of 24 seeds. On top of all three, the conversion's own sampling error compounds along
the chain, 1.09 to 1.10 marks over eleven links against a decisive step worth 3.21 to 4.04 marks, so the graded
figure is seed hostage before any method choice is made, and the discretising rescue cannot reach it because
8.04 of 11 verdict cells sit inside one standard deviation of a 2-mark tolerance line.

**The spec says the same thing in its own words, and it says it as a design-time rule rather than as a
measurement, which is why no repair of C1 was attempted.** `determinism-check` section 1: the comparison is
WHAT, and every lever below it, the pool and the denominator, is part of the estimand too, so a decisive step
that is a comparison or a pool choice has to be filed and the stump has to live somewhere else; and the second
of the three bin quantities is the WHAT screen read as a number, so a candidate whose defensible-subgroup
spread is closed by filing the population has not been repaired, it has been converted into a banned decisive
step. The population a conversion is certified on is the pool. The same section prices C2 as an enumeration
over the four closure moves: two corrections of one graded quantity cannot be separated by the record without
either naming the separating property, which hands over the step, or making them agree, which lets a solver
reach the golden by either route. And it names the escape this screen converged on independently: a correction
with no fitted parameter at all, its rate read off a shipped record rather than estimated, so there is no
corridor and every figure is determinate.

**What ground is left, stated as a shape to price rather than a mechanism to draw.** One shape survives the
measurements: a build whose conversion is **filed and certified in the pack**, so the conformation sits at rung
0 or rung 1 as a lookup and no estimator noise reaches the graded figure, and whose decisive step recovers an
exact **input** to that filed conversion from a second file at a finer grain than the results extract carries,
the records supplying it exactly and the easy route omitting it. Two things are priced first, in this order.
Whether the recovery is a lookup: an awarding body's component and item records usually sum to the total the
results extract already holds, and then the step is arithmetic on shipped columns, which is rule application,
so the finer file has to pin something the coarser one does not state at all. And readability test 7: the finer
file must ship for a reason the organisation independently has (component marks exist because components are
separately examined, carried forward and billed; a marker allocation exists because markers are paid per script;
a custody log exists because the board must evidence the chain), or its presence announces the step.

**What is now spent on this cell and should not be re-screened.** Anchor or common-item drift and
non-equivalent-groups common-item linking (task450, and barred). Any external anchor both groups took, which is
task450's driver with other nouns. The population a conversion is certified on (C1 above). The path through a
chain of administrations (C2). Marker severity from a double-marked overlap, in every form, by the
design-matrix identity (C3). Item-bank exposure (C4, and task249). Placing a retiring instrument's scores on a
new scale by a single-group bridge concordance, which is this slot's own architecture 2 and was solved on the
portal.

**The organisation to draw into, if the shape above is taken.** An awarding body rather than a school: a
chartered professional institute, an examination board, a licensure or certification board, a testing contractor
or a national assessment agency. Measured, that clears `org_family: university_or_school` against task204 and
also moves the world off task450's district. `cooperative_or_member_body`, `committee_or_panel` and
`vote_or_meeting` all measured free at the moment of this screen, and `filed_standard`,
`monitoring_export` and `capacity_report` measured BLOCKed on `ban.artifact`, with `register` free.
