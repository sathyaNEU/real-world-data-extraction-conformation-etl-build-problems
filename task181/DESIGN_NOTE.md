# task181 design note (architecture 2)

Architecture 1 (a credit union's counterfeit wave traced to two skimmed terminals) was spent at in-house round 1; its
note is `DESIGN_NOTE_arch1.md` and its reports carry the `_arch1` suffix. This note is the build plan for architecture
2 and the record of it.

## DRAW

```
Card filed with guard.py register before the ladder was written? yes (PASS)
Shape: 17 periods around a change point (each area's fortnight against its expected count; the curve around the surge)
Gate G mechanism: forecasting (a nowcast: the eventual count of recent specimens from each route's delay)
Gap: time (decisive), population        Pattern: none (own); generators G12 (absence of record versus record of absence), G13
Domain: epidemiology-public-health / disease-surveillance-outbreak-anomaly-detection   Objective: anomaly-detection
Pairing repeated from a recent build? no (epidemiology x anomaly detection never built)
Stakeholder role: director of a regional public health unit (operations_director)   Context artifact: filed_standard
Calibration form: censored_or_lagged_release (the line list's own history of how each area's counts fill in)
Decision type: pick_one_of_n   Answer unit: named_option   Opening move: evidence-first
Stump strategy: maturity_censoring   Decisive rule filed? yes (PR-07 4.2 defines the excess; it says nothing about delay)
Official decoy filed? no   Validated decoy? no   stump_class: analytical
Forum: operations_desk (the Monday huddle)   Forcing event: shift_or_daily_cycle (the weekly deployment)
Org family: hospital_or_health_provider (a public health unit inside a local health district)
Layer 2: field_method, epidemiology-public-health/disease-surveillance-outbreak-anomaly-detection/2 (nowcast the
recent, incomplete period)
People (guard.py names, en_AU, seeds 1814 and 1816): Nathan Olson (director, the requester), Tiffany Peters
(surveillance epidemiologist, owner of the line list notes), Janice Barker (response team leader), Darryl Morales
(immunisation coordinator), Colleen Brown (public health nurse), Cassandra Dawson (data officer who runs the extract).
```

**Data-native sentence.** A pertussis case reaches the public health unit only when a laboratory notifies it, and the
laboratory a case goes through depends on where the patient was swabbed: the regional hospital laboratory runs the PCR
on site and notifies within a couple of days, while the private collection network that serves most Griffith general
practices sends its swabs by courier to Sydney and notifies a week and a half or more after collection, so the
specimens of the last fortnight are almost all on file for one area and mostly still in transit for another.

**Layer 1 (realistic mess and the system that produces it).** A notifiable-conditions line list with one row per
laboratory notification (a person tested by two laboratories, or re-tested, appears twice, and the protocol's episode
rule decides when that is one case); confirmed and probable status under a case definition revised on 1 July 2024
(serology-only cases moved from confirmed to probable); onset dates missing on many rows and imputed under the
protocol's stated rule; specimen dates as local dates and notification times as UTC stamps from the state system;
residential postcodes mapped to local government areas through the ABS-style concordance, where a few postcodes are
split between two areas with population ratios and the protocol's allocation rule applies; a hospital admissions
extract keyed by medical record number; an antenatal vaccination register keyed by the mother's Medicare number, linked
to infants through the birth record file; school enrolment rosters with school names spelled as each school spells
them.

**Layer 2 (the analytical shortcut).** Reading the cases notified so far for the last fortnight as the fortnight's
cases. The protocol's excess is defined on specimens collected in the 14 days before the extract; the line list holds
only the specimens that have been notified, and how many have is a property of each area's laboratory route. A careful
analyst who sees the shortfall still pools the delay across the unit; an expert estimates each route's own
specimen-to-notification delay from the completed history in the file and nowcasts each area on it.

**Similarity claim.** No prior build turns on right-truncated counts read across reporting routes of different speed.
task229 (a release-health alert on interval meter reads) has days the MDM held nothing for until its estimation run,
but there the decisive step is the unit the standard error is built over; task180's decisive step is a gas source
attribution. Differentiation lines are written at stage 5.

## THREE RULES (client, 2026-10-10)

- **Rule 1, the domain is used.** What decides the call is an epidemiological nowcast, the eventual count of recent
  specimens estimated from each reporting route's own delay distribution, which is how outbreak surveillance reads
  right-truncated case data. Swap test: with another field's nouns in there is no specimen-to-notification delay, no
  laboratory route and no truncated epidemic curve; the task does not survive the swap.
- **Rule 2, two layers.** Layer 1 above (episodes from duplicate notifications, the case-definition revision, onset
  imputation, UTC stamps, split postcodes, record linkage across three registers, school spellings). Layer 2: the
  nowcast on each route's own delay.
- **Rule 3, the decisive step is analytical.** Class `analytical`. Analyst test: a strong analyst who removes the
  duplicate notifications, applies the case definition, maps every case to its area and computes the protocol's
  expected counts exactly still compares the cases notified so far for the fortnight (or a nowcast on one pooled delay)
  with the expected counts and sends the team to Wagga Wagga; only a nowcast on each area's own route shows Griffith's
  fortnight several times above its expected count. Rule application (the expected-count arithmetic, the episode rule,
  the cluster rule) and data semantics (UTC stamps, the probable class) sit on lower rungs and in the asks.

## GATE G

- **Litmus.** Nothing reported is overturned: every notification is correct, every date is right, the expected counts
  are the protocol's own. The difficulty is that the recent fortnight is incomplete by different amounts in different
  areas.
- **Primary mechanism:** forecasting (nowcasting the eventual count of specimens already collected).
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`
- **Deletion test.** Delete the line-list notes and the protocol's background section: the notified counts still put
  Wagga Wagga first and the route-specific nowcast still puts Griffith first.
- **Clean-data and instrument test.** No file is incomplete or stale: the line list is the state system's complete
  extract of everything notified up to 07:00 on Monday 5 October 2026. A perfect notification system would still hold
  only the specimens notified so far; the decision needs the specimens collected, which is an estimate from the delay
  each route shows in the completed history. Nothing is repaired.
- **Lens swap.** Not one population under two lenses: the answer's quantity is the estimated count of specimens
  collected, built from the delay history; the naive quantity is the count notified.

## STUMP SENTENCE

A competent solver counts the cases notified with specimens collected in the 14 days to Sunday 4 October in each area
against PR-07's expected count and sends the team to Wagga Wagga, the largest excess on file (or nowcasts with the
unit's pooled delay and still lands there); the step that lands it there is reading the specimens notified so far as
the specimens collected, when Griffith's swabs go by courier to Sydney and, at Griffith's own specimen-to-notification
delay, its fortnight is several times what has arrived.

## ENTITY AND UNIT OF VALUE

One local government area, one team-week. PR-07's excess is a count of cases (confirmed and probable) with specimens
collected in the 14 days before the extract day, less the area's expected count for the same 14 days.

## LADDER (targets for the build; the shipped values replace these)

Areas (ten local government areas served by the unit; populations from the 2021 census, rounded): Wagga Wagga 67,600
(hospital route), Griffith 27,100 (private route since before 2019), Leeton 11,400 (private route), Narrandera 5,800,
Murrumbidgee 3,900, Hay 2,900, Edward River 8,500, Junee 6,600, Cootamundra-Gundagai 11,300, Snowy Valleys 14,400 (all
hospital route unless named). Route delays (specimen collection to notification): hospital route median 2 days, 95th
percentile 5; private route median about 12 days (courier runs Tuesday and Friday, a Sydney batch PCR, results keyed
next working day), 95th percentile about 24.

| Rung | Construction | Area | Why a careful analyst stops | Killed by |
|---|---|---|---|---|
| 0 | Most cases notified with specimens in the fortnight | Wagga Wagga (about 9) | the biggest number | PR-07 4.2 is an excess over the expected count |
| 1 | PR-07 excess on the cases notified so far | Wagga Wagga (about 9 against 2.0, +7) | the protocol applied exactly | the fortnight is incomplete: in the completed history only about a quarter of Griffith's cases are notified within 14 days of collection |
| 1b | The same on notification date instead of specimen date | Wagga Wagga | a complete window | PR-07 4.2 counts specimens collected; Griffith's surge is mostly not yet notified on either date |
| 2 | Relative excess (notified over expected) | Wagga Wagga or a tie | a rate reads fairer than a count | PR-07 4.2 is a count excess |
| 3 | Nowcast on one delay pooled across the unit | Wagga Wagga | the truncation handled | the pooled delay is the hospital route's (most cases go through it); Griffith's route is several times slower |
| 4 (answer) | Nowcast each area on its own route's delay | **Griffith** (about 40 estimated against 0.8 expected) | | |

**Twin pair.** Griffith and Snowy Valleys carry the same notified count for the fortnight and the same expected count
(both about 6 against 0.8), so rungs 0 to 2 cannot separate them; Snowy Valleys' cases go through the hospital route and
its fortnight is nearly complete (nowcast about 6.5), Griffith's go through the private route (nowcast about 25 or more
under every estimator in the grid).

**Margins (targets).** Under every route-specific estimator in the grid, Griffith's estimated excess is at least 2.5
times the next area's; under every rung 0 to 3 construction, Wagga Wagga is first and Griffith is not; Wagga Wagga's
notified excess beats the next area by at least 25 per cent.

## GRID (to be asserted in checks.py, cell by cell)

Rows (estimators): aggregate inflation (notified in the fortnight divided by the route's completeness averaged over the
fortnight's days), per-day inflation (each specimen day divided by its own completeness, with days below 5 per cent
completeness pooled into the nearest day above it), reporting-triangle chain ladder on weekly specimen cohorts, and a
negative-binomial delay model by route. Columns: delay history over the last 6, 12 and 24 months of completed
specimens; stratified by laboratory route or by area; daily or weekly delay bins. Every route-specific cell returns
Griffith. Every pooled cell and every rung 0 to 2 construction returns Wagga Wagga. The 2024 epidemic months may be in
or out of the history window without moving a cell (asserted).

## CLOSURE (the 22 axes)

1 Population: residents of the ten areas (PR-07 1.2); visitors notified to the unit are excluded by residential
postcode. 2 Unit: local government area. 3 Window: specimens collected Monday 21 September to Sunday 4 October 2026
(the 14 days before the extract day, PR-07 4.2). 4 As-of: the extract at 07:00 AEDT on Monday 5 October 2026 (daylight
saving began Sunday 4 October; the window's dates are local). 5 Version basis: one row per notification; the episode
rule (PR-07 3.3) makes one case of a person's notifications within 90 days. 6 Divisor: none (a count excess). 7
Weighting: none. 8 Window length: 14 days. 9 Boundary: no area within 25 per cent of the winner at any rung. 10
Rounding: expected counts to one decimal in the brief. 11 Tie-break: the twin tie sits below the naive winner. 12
Maturity: the decisive axis; the nowcast. 13 Order of operations: episodes, case status, area, window, then expected
count and nowcast. 14 Row order: irrelevant. 15 Duplicates: the episode rule. 16 Identity: person ID across
laboratories; the mother's Medicare number for the antenatal link. 17 Netting: none. 18 Units: cases. 19 Code
semantics: case status confirmed or probable under the definition in force at the specimen date; PR-07 counts both. 20
Integerisation: none in the call. 21 Scope: pertussis only. 22 Forward window: none.

## ASK SHEET (devices off the main call's row population)

| Ask | Figures | Primary devices (silent) | Shared hazard |
|---|---|---|---|
| A. The year to 31 August by area (CSV): confirmed cases, probable cases, infants under six months at specimen, of those admitted to hospital, of those whose mother was vaccinated at least 14 days before the birth | 10 x 5 = 50 | the episode rule across two laboratories (a second laboratory's notification within 90 days is the same case); serology-only cases before 1 July 2024 recoded probable by the revised definition (none in 2026, but the extract's status column carries the status at notification); age at specimen from date of birth; hospital admission linked by medical record number with an admission date within 14 days of the specimen; antenatal vaccine linked to the infant through the birth record (mother's Medicare number), counted only at least 14 days before birth | split postcodes (PR-07 3.4: the area holding the larger population share) |
| B. School clusters (slide): schools with two or more cases among students with specimens in the 30 days to 4 October, each with school, area and case count | about 4 schools | school names spelled as each school spells them on its roster against the case interview's free-text school; students against staff (the interview's role field); the 30-day window by specimen date | the episode rule |

Stops (each moving its figures, to be asserted): ignoring the episode rule; counting probable cases as not cases;
admissions without the 14-day link; antenatal vaccine at any time before birth; school names matched exactly; the
window by notification date.

Use test: the huddle sees the area, the clusters and the year's infant picture every week. Decoupling: the ask figures
do not move with the nowcast (asserted).

## PINS

Filed: PR-07 Pertussis response protocol (governing): scope (1.1, 1.2), case definition and status (2.1, 2.2, revision
of 1 July 2024), episodes and notifications (3.1 to 3.4: the episode rule, onset imputation as specimen date less 10
days where onset is missing, residential postcode, split postcodes to the area with the larger population share),
deployment (4.1 the team works one area a week; 4.2 the area is the one with the largest excess of cases with
specimens collected in the 14 days before the extract day over its expected count; 4.3 the expected count is the mean
count for the same 14 days in the previous five years), clusters (5.1 two or more cases among a school's students with
specimens in 30 days), infants (6.1 maternal vaccination counts at least 14 days before birth). Line-list notes (field
semantics only). No sentence anywhere mentions notification delay, completeness, backfill or nowcasting (to be
asserted on the protocol, the notes and the extract report).

## PACK GATES (targets)

10 to 13 files, at least 5 formats: the line list (csv, 2019 to 2026, a few thousand notifications), the postcode
concordance (xlsx), population by area (xlsx, census and estimated resident population), hospital admissions extract
(csv), birth records (csv), antenatal vaccination register (parquet, large: every pregnancy dose for the district since
2019, or a daily immunisation register at 25,000 rows or more), school rosters (xlsx, one sheet per school), PR-07 (pdf),
line-list notes (md), extract run report (txt), and two distractors named in metadata.json (an influenza notifications
extract and the unit's weekly bulletin PDF for August, both from the same world, neither read by the golden). Two
consecutive builds byte-identical.

## PRE-SHIP CHECK (client, eight points; answered at ship)

## STOPPING RULE

Two rounds in which the solver nowcasts each route unprompted file this architecture as at-ceiling; a miss that lands
anywhere other than rungs 0 to 3 is read for a fork before any hardening.

## Tried and rejected

- **Architecture 1 spent at round 1 (2026-10-11).** See `DESIGN_NOTE_arch1.md`, Tried and rejected: the solver's
  explain-away and residual re-screen landed the reissue count, and any further rung was either dismissed by its subset
  check or opened a fork.
- **Draws weighed for architecture 2 and not taken.** A competing-risks registry outlier (one minus Kaplan-Meier against
  cumulative incidence for implants in frail patients): registries report Kaplan-Meier, so the expert estimand would
  read as a second defensible answer. Overdispersed funnel limits for hospital mortality: multiplicative and additive
  adjustments rank the extreme hospitals differently, a fork. A disproportionality signal masked by indication: the
  pinned comparator would have to be filed, which makes it rule application.
