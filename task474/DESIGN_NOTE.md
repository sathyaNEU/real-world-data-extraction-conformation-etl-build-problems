# task474 design note: an awarding body's pass mark across a test-vendor change (architecture 7)

Architecture 7, drawn 2026-10-31 after architecture 6 (the port authority's air-corridor designations) was spent at
its repair. Earlier architectures' sections are retired; their lessons stand in Tried and rejected.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task474.json`, architecture v7, guard PASS (differentiated against
  task196, task202, task449, task466 and task480), registered 2026-10-31 after a fetch of main.
- **Pairing.** Client domain education-learning-sciences, task type item-response-theory-test-equating (which serves
  Data Extraction & Conformation), objective Data Extraction & Conformation (ETL): two test vendors' result exports
  and the awarding body's candidate register are conformed into one candidate-level record of every sitting, and the
  conformed record carries the old paper's standard onto the new paper.
- **Niche.** Heatwise Qualifications, an English awarding body owned by the installer trade associations, examines the
  theory paper of its Heat Pump Installer Certificate. Until 31 March 2026 Brindle Assessment ran the paper at test
  centres and reported a scaled score from 0 to 100, the pass standard 65. From 1 April 2026 Harrowgate Testing runs a
  new 60-question paper, online-proctored or at its test sites, scored by raw mark. Results for the new paper are held
  until the Board sets its pass mark at the 4 November 2026 meeting, from the sittings to 30 September.
- **Decision.** The raw pass mark on the new paper, applied to the held 2026 results and to every 2027 sitting.
  Forward facing: the mark governs the coming year's sittings.
- **The quantity.** The raw mark on the new paper that holds the old standard: Assessment Policy AP-3 files it as the
  lowest raw mark that no larger share of an equivalent group of candidates reaches than reaches 65 on Brindle's scale.
- **Data-native sentence.** The only candidates measured on both papers are the ones who failed the old paper and sat
  the new one, and every candidate who sits a second time gains on the first sitting, as the old paper's own retakes
  show; the first-time candidates on either side of the switch are not one cohort, since experienced gas engineers
  started coming through the standard route in autumn 2025 and the summer sittings always bring a stronger mix than
  the winter ones, so only the cross-switch candidates, read against the old paper's retakers matched on their first
  score, give an equivalent group.
- **Default path.** Hold the old paper's first-time pass rate of the same months a year earlier on the new paper's
  first-time candidates.
- **Golden.** The cross-switch candidates' pass rate on a second old sitting, read from the 2021 to 2025 retakers with
  the same first scores, set on their new-paper raw marks.
- **Shape.** 15, fields conformed to one schema: every 2026 sitting conformed to one record, plus the asks' figures,
  the pass mark and the paper's chart.
- **Shell.** Question form what; deliverables pdf and csv; forum the Board of Directors, forcing event its meeting,
  organisation family a member body, all clear of the last three builds.
- **Personas.** Laura Kay (Head of Qualifications), Alan Clayton (Chief Examiner), from `guard.py names --geo "United
  Kingdom" --seed 474`.

## Default path

1. Read AP-3: the new paper's pass mark is the lowest raw mark that no larger share of an equivalent group reaches
   than reaches 65 on Brindle's scale.
2. Conform the two exports through the register (Brindle's SAT rows, Harrowgate's cleared and released marks once per
   sitting, UK dates) and take each candidate's first sitting.
3. Take the first-time candidates of April to September 2025 on Brindle's paper as the equivalent group of the
   first-time candidates of April to September 2026 on Harrowgate's (the same months a year apart, the awarding
   body's way of holding a pass rate through a paper change), and set the mark where the 2026 share falls to the
   2025 share at 65.

Ends on: 40
Golden: 38

## Stump sentence

The default path gives Harrowgate's 2026 first-time candidates the pass rate Brindle's paper gave the 2025 first-time
candidates in the same months and files a pass mark of 40; the step that lands it there is reading a change in the
cohort as a change in the paper, when experienced gas engineers have come through the standard route since the autumn
of 2025 and the only candidates measured on both papers, the ones who failed Brindle's and sat Harrowgate's next, carry
a second-sitting gain that Brindle's own resits measure, so the mark that holds 65 is 38.

## Three rules

Task type: item-response-theory-test-equating (Education & Learning Sciences), which serves Data Extraction & Conformation: two vendors' results conformed to one record and the old scale's standard carried onto the new paper.
Domain test: the quantity that decides is the raw mark on the new paper equivalent to 65 on the old scale, an equating function the field estimates from a linking design, here the candidates measured on both papers once the gain every second sitting carries is removed; swap the nouns for a hospital's or a utility's and there is no instrument change, no pass standard and no retest gain, and the task stops reading the same.
Swap: "What dose on the new infusion pump matches the old pump's 65?" has no candidates who sat twice and no second-sitting gain to remove, and "which tariff holds the old bill" has no measured proficiency, so the task does not read the same with another field's nouns.
Layer 1: two vendors' exports keyed by their own candidate numbers and tied to board numbers only through the register, candidates who re-registered after a lapse under a second board number, Brindle's ABS and VOID bookings beside SAT rows, Harrowgate's held records beside their releases and its no-show and voided records, UTC timestamps against UK dates, day-month-year against ISO dates and Brindle's rotating forms on one scale; each is what the systems that hold it produce and none is placed to be caught.
Layer 2: estimation_fit, the linking design: an equivalent group has to be found, the first-time cohorts on either side of the switch are not one (the gas engineers since autumn 2025, the stronger summer mix), and the candidates measured on both carry the retest gain, so their second-sitting pass rate on the old paper has to be estimated from Brindle's own resits matched on the first score.
Decisive step: estimating, from Brindle's resits of first-sitting fails in 2021 to 2025 matched on the first score, the share of the cross-switch candidates who would have reached 65 on a second Brindle sitting, and setting the mark where their Harrowgate marks give that share.
Not semantics: reading every field and AP-3 correctly still leaves the equivalent group to choose, and no column marks a gas engineer, a retest gain or a cohort; the first-time cohorts, the side-by-side pairs and the unmatched resits all read every field right and file 40, 41 and 37.
Not rule application: AP-3 files the estimand (an equivalent group's share at 65) and no clause says which group is equivalent or how its old-paper share is found; executing the filed rule on any group files whatever that group gives, and only the resit record matched on the first score rules the other groups out.
Analyst test: a strong analyst conforms both exports through the register, reads AP-3 correctly, holds the 2025 first-time pass rate on the 2026 first-time candidates and files 40; every field is read and every rule executed, and the mark is wrong because the 2026 cohort is stronger than the 2025 one and the candidates measured on both papers carry a second-sitting gain.
Estimand: ap3_pass_marks_and_standards.pdf section 2: the lowest raw mark on Harrowgate's paper that no larger share of an equivalent group of candidates reaches than reaches 65 on Brindle's scale, an equivalent group being one whose proficiency would be the same whichever paper it sat; population, the paper's candidates; window, Harrowgate's sittings from 1 April to 30 September 2026; unit, the raw mark; comparison, the share at 65.
No decoy: nothing is planted to be caught; no memo, draft, provisional mark or vendor recommendation argues any group or any mark, the held results carry no result, and the item statistics and the survey decide nothing.
No certified replay: no certified or published figure reproduces any linking route; no file carries a pass rate, an equating table or a recommended mark.
Lesson: an equivalent group for a paper change is the one whose proficiency is the same on both papers, which first-time cohorts a year apart are not when the intake moves, and which candidates measured twice are only after the retest gain the old paper's own resits measure is removed; no build on file teaches the retest gain in a linking sample.

## Survivor anatomy

Actor: the deciding property, how much a second sitting reads above a first, has no column; it shows only as the difference between a resitter's two Brindle scores, and the cohort's change shows only as Brindle's first-time pass rate rising on an unchanged paper from the autumn of 2025.
Link: the comparison that finds the mark sets the cross-switch candidates beside Brindle's own resitters of 2021 to 2025 with the same first score, different people tied by no key, and no sentence invites it; the register's keys invite only the side-by-side pairs.
Reflex: the field's way of holding a standard through a paper change at an awarding body, the pass rate of the same months a year earlier carried onto the new paper's first-time candidates, is rung 0 and files 40.
Back-test: the textbook route validates on the record: Brindle's first-time pass rate held between 45.9 and 47.3 per cent in every year from 2021 to 2025, so any year-apart comparison on the old paper would have held the standard until the scheme's intake arrived.
Second use: every file the decisive step reads has its own reason to be in the pack: Brindle's export is the results record, Harrowgate's the new paper's, the register ties the candidates, AP-3 files the standard and the resit rules, and the notice dates the switch.
Shock: the golden sits below every first-time route, 38 against 40 on both the year-apart and the adjacent halves and 40 on their difference, and the obvious repair, the resits without matching, overshoots to 37; no route the cohorts allow lands on it.
Pins: the WHAT sits in AP-3 (the estimand, the group's definition, the window of held results) and no filed sentence names a retest gain, matching, the gas engineers or a cohort (asserted, L1); deleting AP-3 section 2 unforces the call and that section names no step.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 first-time pass rate a year earlier | AP-3 section 2 is the estimand | first sittings by date | the awarding body's reflex | none refutes it | the battery runs it | one share and one cut | none | readable |
| 1 the half before the switch | none | first sittings by date | a careful variant | none | yes | one share and one cut | none | readable |
| 2 the cross-switch candidates side by side | none | the register's keys | the common-candidate link | none | yes | one linear link | none | readable |
| 3 the resits unmatched | none | resits by date | a psychometrician's repair | none | yes | one share | none | readable |
| 4 (decisive) the resits matched on the first score | none names a gain, matching or a cohort | no column holds a gain | not the reflex | Brindle's resits are the bench, matched by first score | no battery item | not affine in a shipped column | the resit record is the results export itself | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | an equivalent group | a group whose proficiency is the same whichever paper it sat | any group of candidates | the routes differ (40, 41, 37) | AP-3 section 2's definition; asserted |
| SF2 | reaches 65 | at or above 65 | above 65 | not the filed reading | AP-3 section 2 ("reaches 65"); asserted |
| SF3 | the lowest raw mark no larger share reaches | the lowest mark whose share is at or under the group's share at 65 | the mark whose share is nearest | same call (asserted) | AP-3 section 2 |
| SF4 | the resit history | first-sitting fails from 2021 to 2025 | from 2020, from 2023, or to March 2026 | same call (asserted under each) | none needed |
| SF5 | matching on the first score | each first score | bands of two or five points | same call (asserted) | none needed |
| SF6 | the resits read | the resit of a first sitting | every resit | same call (asserted) | none needed |
| SF7 | a sitting | a SAT row or a cleared or released mark, once per sitting | ABS, VOID, held, no-show or voided records, or a held record and its release twice | moves the asks, not the call | AP-3 section 4; asserted |
| SF8 | the date of a remote sitting | the UK local date | the UTC date | same call (asserted) | the export's Z suffix |
| SF9 | a candidate | a person: board numbers sharing surname, initials and date of birth | each board number | same call (asserted); moves the asks | the register (one person, two numbers) |
| SF10 | first sitting and resitting in the asks | a person's first sat sitting on either paper | a board number's first | moves 18 of 18 and 10 of 10 figures (asserted) | the register and AP-3 section 4 |
| SF11 | the months and years | UK calendar months of 2026 to September; calendar years by the sitting's date | other calendars | not the filed reading | the prompt; asserted |

## Ladder

| Rung | Construction | Files | Dies to |
|---|---|---|---|
| 0 | the 2025 first-time pass rate of April to September carried onto the 2026 first-time candidates | 40 | Brindle's first-time pass rate for October 2025 to March 2026 sat 5 points above the same half a year earlier on the unchanged paper, as the gas engineers came through the standard route |
| 1 | the half before the switch (October 2025 to March 2026) carried onto April to September 2026 | 40 | the summer sittings draw a stronger mix every year (Brindle's first-time pass rate in April to September sat 4 to 6 points above the October to March before it in every year from 2020 to 2024) |
| 1b | the year-apart route corrected by the winter halves' shift | 40 | the gas engineers' share kept rising through 2026, so the winter shift understates the summer's |
| 2 | the cross-switch candidates' two results side by side (a linear link) | 41 | every second sitting reads higher, as Brindle's resitters show |
| 3 | Brindle's resits of first-sitting fails, unmatched, carried onto the cross-switch candidates | 37 | the 2025 resit rules (a free resit for 55 to 64 within six weeks, six months' wait under 55) changed which first scores reach the new paper |
| 4 (decisive) | the resits matched on the first score, their share at 65 carried onto the cross-switch candidates | 38 | the golden |

- **Margins on the cut pack** (asserted in checks.py): the equivalent share sits 0.027 above the share reaching 38 and
  0.042 below the share reaching 37; every standing member (first scores exact or in bands, histories from 2020, 2021
  or 2023, every resit) files 38, and the latent model's equivalence for any equivalent group is 38 (T1).
- **Separation.** The default path is wrong on the clean truth (T3) and the matched route on the world's own sittings
  is the golden (T2).

## Closure table

| Axis | Reading in this build | Move |
|---|---|---|
| 1 Population | the theory paper's candidates; for the call, the group AP-3 calls equivalent | filed (AP-3 section 2) |
| 2 Unit of account | the person, board numbers sharing surname, initials and date of birth | C1 (SF9) |
| 3 Attribution window | Harrowgate's sittings 1 April to 30 September 2026, Brindle's to 31 March 2026 | filed (AP-3 section 2, the notice) |
| 4 As-of dating | the register extract of 12 October 2026 | the file's date |
| 5 Version basis | one record per sitting; a held record and its release are one sitting | SF7 |
| 6 Denominator | the equivalent group's candidates | filed (AP-3 section 2) |
| 7 Weighting | the cross-switch candidates' own first scores | C1 (SF5) |
| 8 Window length | the resit history 2021 to 2025 | C1 (SF4) |
| 9 Boundary inclusivity | reaches 65 is at or above 65; no larger share is at or under | filed (SF2, SF3) |
| 10 Rounding path | marks are whole; shares compared unrounded | C1 by construction |
| 11 Tie-break | the lowest mark meeting the share | filed (AP-3 section 2) |
| 12 Maturity and censoring | results held, so no new-paper resit; the window closed on 30 September | filed (AP-3 section 2) |
| 13 Order of operations | conform, tie people, take sittings, match, set | C1 |
| 14 Row order | none: set operations by person and date | C1 |
| 15 Duplicate resolution | a held record beside its release: the release | SF7 |
| 16 Identity normalisation | provider numbers to board numbers by the register, board numbers to persons by name and date of birth | SF9 |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | scaled scores 0 to 100 on Brindle's paper, raw marks out of 60 on Harrowgate's | the files' own fields |
| 19 Code and status semantics | SAT, ABS, VOID; cleared, released, held, no_show, voided | AP-3 section 4; SF7 |
| 20 Integerisation | whole marks and whole candidates | C1 by construction |
| 21 Clause scope | AP-3's resit rules decide who resits when, not the estimand | filed scope |
| 22 Forward window contents | the mark applies to the held 2026 results and every 2027 sitting | filed (AP-3 section 2) |

## Literal reader

Executed word for word, AP-3 section 2 asks for the lowest raw mark that no larger share of an equivalent group
reaches than reaches 65 on Brindle's scale, the group being one whose proficiency would be the same whichever paper it
sat. Read literally, no group of first-time candidates a year apart, or the halves either side of the switch, has the
same proficiency (Brindle's own first-time pass rates move between them on an unchanged paper), and the cross-switch
candidates at their second sitting are equivalent only to themselves at a second sitting, whose Brindle share at 65
Brindle's resits matched on the first score give: 38. The asks' months and years, first sittings and resits read
literally on persons give the figures in figures.json.

## Oracles

None on the main call: no file carries a pass rate on Harrowgate's paper, an equating table, a provisional mark or a
recommendation; the Harrowgate records carry no result. The asks have no oracle either: no file states a monthly or
yearly count.

## Ask sheet

Two asks on the conformed record, each on persons the register ties by surname, initials and date of birth, a link no
key invites.

**Ask A, first-time and resitting candidates in each month of 2026 to September (18 figures).**
- Files: the register, Brindle's export, Harrowgate's export.
- Primary (D9, the true key elsewhere): a candidate who comes back after a year away re-registers under a second board
  number and new provider numbers, so taking each board number as a candidate makes the returner a first-time
  candidate; the person is the board numbers sharing surname, initials and date of birth.
- Hazards: ABS and VOID bookings; Harrowgate's held records beside their releases; no-show and voided records; UTC
  timestamps.

**Ask B, candidates who first sat Brindle's paper in each year 2021 to 2025, and how many passed at it (10 figures).**
- Files: the register and Brindle's export.
- Primary (D9 again, a second grain): the returner's later first sitting under the second board number is counted
  as another first sitting in its year, and its result as another first-sitting pass or fail.
- Hazard: ABS and VOID bookings are not sittings (AP-3 section 4).

| Ask figures | Cracker (lands the call, runs the battery, executes every filed rule) | Mirror (stops at rung 0) | Verdict |
|---|---|---|---|
| A, 18 monthly figures | takes each board number as a candidate | the same | miss |
| B, 10 yearly figures | takes each board number as a candidate | the same | miss |

Pair ceiling: 30.4 (the cracker on the call at 46.9, the mirror off it at 13.9, each keeping 1 of 29 ask criteria,
the paper's chart).
Mirror leakage: 3.4 per cent of the ask weight.
Measured by: generator/ceiling.py (run on the cut pack, target.zip 1fc4d13f)

## Leak sweep

`leak.py task474 --asof 2026-10-13` on target.zip 1fc4d13f: REVIEW, no LEAK; each line ruled.
- Sweep 3 on `ap3_pass_marks_and_standards.pdf` and `theory_paper_change_notice_2026.pdf` (pass mark, Harrowgate,
  theory paper): harmless; they are the awarding body's own nouns for the paper and its provider, and neither document
  carries a mark, a share or a group.
- Sweep 4 on `ap3_pass_marks_and_standards.pdf` (resits, equivalent, carries, register, sittings): harmless; the policy
  files the estimand (an equivalent group) and its own resit rules, and says nothing of a second sitting's reading,
  matching or a cohort (asserted, L1).
- Fixed before this run: the venues file's name (an author word), the item note column's name, and the workbooks'
  application stamp (now the office suite's, each workbook with its own save history).

## Pre-ship check

1. Three rules: the decisive step (the resits matched on the first score) is analytical; nothing planted, read or
   executed decides (the Three rules lines).
2. Determinism: AP-3 section 2 files the WHAT; the standing family converges on 38 across first-score bands, resit
   histories and resit orders, the latent model gives 38 for every equivalent group, and the forks are closed
   (SF1 to SF11, asserted).
3. Gates on the final cut (target.zip 1fc4d13f): generator checks 42 of 42, the independent verifier on every graded
   figure, two byte-identical builds, figures_check.py 52 of 52, precut.py 61 of 61, voice-check.py PASS, leak.py
   REVIEW with no LEAK; the leak reader and the determinism judge run from the main thread.

## Tried and rejected

- 2026-10-20, at the draw: the seed's own move (rebuild from towns rather than an area crosswalk): a careful analyst
  rebuilds from towns unprompted; kept as Layer 1.
- 2026-10-20, at the draw: re-basing the 2020 to 2021 estimates onto the population the 2020 census revised (the silent
  break behind the loud geography break): the population base is the series' version basis, an axis that must be
  filed, and filing it makes the step rule application while leaving it open forks the call against the published
  figures; dead by the WHAT screen.
- 2026-10-20, at the draw: the auxiliary for splitting the former counties (SNAP recipients over each region's take-up,
  measured where both are published): the same insight as task470 and task448 (the ratio the target actually scales
  with, measured where both are observed); a clone in the lane.
- 2026-10-20, at the draw: the five-year window centred on each year picked from a full run of overlapping releases: a
  lookup once the idea is there, and the one-window routes (2018-2022 or 2019-2023 for both years) sit within half a
  year of the golden, about $5,000 a region; replaced by two non-overlapping releases, where every route but the
  interpolation at the middle years misses by a year of drift or more.
- 2026-10-20, at the draw: a region formed by differencing overlapping published geographies (the pieces pinned by two
  partitions' margins): exact arithmetic with no field in it; the swap test reads it the same for sales territories.
- 2026-10-20, at stage 2: two non-overlapping five-year releases (2015-2019, 2020-2024) placed at their middle years
  and a year's town shares interpolated between them: its forcing evidence (the native years 2023 and 2024 on the line
  through the middle years) sat inside the regions' survey noise of 5 to 12 per cent, and the drift between the two
  releases' middle years, five years apart, was smaller than that noise; replaced by an annual indicator benchmarked to the one release.
- 2026-10-20, at stage 2: a growth component (each town's drift estimated from the two releases and carried by year):
  the difference of two town releases carries both sampling errors and swamped the drift; dropped.
- 2026-10-20, at stage 2: shipping the 2015-2019 release beside the 2020-2024 one under the benchmarked indicator: with
  two benchmarks a proportional Denton spreads the ratio across the years and moves amounts by up to $12,000 against
  the pro-rata golden, an open method; only the 2020-2024 release ships, where Denton and pro-rata coincide.
- 2026-10-20, at stage 2: SNAP benefits in dollars in the DSS file: a dollar indicator for a person count carries the
  emergency allotments of April 2020 to February 2023 and moves two amounts; the file ships recipients and households.
- 2026-10-20, at stage 2: the client address changes as their own file: a file named for address changes announces
  that the extract's town is not the town when served, and with it a reader keeps 14 of the 18 figures in asks A and B;
  the moves ship as address edits inside the grants data system's profile audit trail.
- 2026-10-20, at stage 3: the two relocations dated July 2023 to June 2024: the State Data Center's own planning region
  series then showed the drift outright (Greater Ormsby down 10.6 per cent from 2023 to 2024, Mill River Valley up
  8.1), so the record displayed the step; both relocations now run from April 2021 to February 2022, inside a former
  county each, where no published estimate shows them (the planning region estimates begin in 2023, and every region
  moves under 1.3 per cent from 2023 to 2024).
- 2026-10-20, at stage 4 (architecture 1 spent): two isolated scored readers. Reader 1 benchmarked each town's SNAP
  recipients to its own five-year survey count unprompted ("SNAP levels are not proportional to poverty across towns,
  but SNAP's year-to-year movement is usable") and landed all nine amounts (score_reader.py exit 1); reader 2 took SNAP
  shares (missed the call) but, like reader 1, rebuilt the town at service date from the audit trail, mapped Corbin's
  numbers and counted one energy payment per household, keeping 27 of 27 ask figures. Rule 2.2's "in that year" beside
  a single five-year release and a monthly town series displays the decisive step, and the ask devices are work orders
  a careful reader executes; the architecture is spent and the draw is re-rooted at stage 1.
- 2026-10-20, stage 4 judge on architecture 1: DETERMINISTIC, APPROVE, Gate H analytical; it named two pins worth
  carrying into the re-root (an effective date is the first day the new value applies; a household payment repeats on
  each member's row), and that the release-shares route is defensible enough that a miss there can read interpretive.
- 2026-10-20, re-root screen: keep the world and add a second correction to the benchmark (relocated households keep
  the origin city's SNAP take-up, so a constant town ratio misplaces the move): every route, the benchmark included,
  misses a split on the true poor by six or more amounts through the survey's sampling error, and a movers-aware
  estimator (backing the moves out of the conserved recipients) has no form the data close to one; dead as a decisive
  step.
- 2026-10-20, re-root screen: a second, independent correction from students (off-campus students counted poor by the
  survey and the estimates but absent from SNAP, away for remote teaching April 2020 to August 2021, timed by a
  university's residence counts): with campuses of 6,200 to 9,800 students in three towns of split counties, the
  SNAP-only benchmark still lands all nine amounts (largest gap $3,959), because the absence is two partial years of
  a five-year average and moves people only between pieces of one county; dead without implausible enrolments.
- 2026-10-20, re-root screens also run against the corpus: item-response test equating is spent in the lane
  (task450's anchor equating with a drift screen, task464's concordance, task123's and task249's drift screens), and
  census-register coverage carries nine cards and repeated screens (task123, task228, task243); neither is redrawn.

- Re-root screen, gas-network methane with undetected leaks scaled from quality-assurance re-surveys: dead on paper, the re-survey file displays its own miss rate so readers scale by it, it repeats task470's sensor-completion insight, and emissions-inventory is now held by task476 v2 inside the last-three window.
- Re-root screen, survey employment benchmarked to an annual census count with post-benchmark bias estimated from past benchmark revisions: dead on paper, the bias is displayed by the past revisions themselves and the bias forms (mean, recent, growth-scaled) fork the graded level with no design closing the family; task477 drawn first while task474 waits for a fresh world.
- Architecture 1 (the planning-region poverty split, each town's SNAP recipients benchmarked to its five-year survey
  level) as a whole: spent at stage 4 on 2026-10-20 (reader 1 landed the call, reader 2 kept every ask); re-rooted to
  architecture 2 in a fresh world after six screens on the old one died.
- Asks of the first cut (fuel priced on the gas day across the clock change; outages re-reported with a corrected end
  only; generation and operating hours graded): stage 4 readers 1 and 2 both missed the call (two and four units) and
  both kept all nine fuel costs, three forced-outage figures and every generation and hours figure; the judge read the
  re-report as a fork (union against the later report). Generation and hours left the deliverables, rule 3.2 files
  that the later report stands, re-reports correct the start as well, and one invoice month per delivery point is
  missing; a generation total that sat on a half MWh is gone with the two-decimal load.
- Architecture 2 (combined-cycle NOx with monitor gaps filled by hours since start): spent at stage 4 on 2026-10-20.
  The judge returned DETERMINISTIC and APPROVE and readers 1 and 2 missed the call (two and four units), but round-2
  reader 3 filled the start hours by position after a start unprompted, designated the golden seven and kept all 18
  ask figures (score_reader exit 1); the judge had already named the start-state fill the field's standard handling of
  missing monitor hours. A gap filled by the condition that causes it is a repair a careful analyst reaches; the next
  architecture needs a decisive step no standard repair performs.
- Architecture 3 screens at the draw (2026-10-20): hot-afternoon duct firing behind shelter-overheat outages (the heat
  input in every gap carries it, so a fill on load and heat input is a standard repair that lands it); start class
  (cold, warm, hot starts) behind longer start-up outages (hardens the spent start-state design and its thresholds are
  a knob); an analyzer over-range censoring (the tail above the span is unidentified without a second measurement).
  Kept: the shared instrument air outage, whose uncontrolled level shows only in the first hour back.
- Architecture 3, ask A first cut: the transporters' fuel retention as a fixed share (a straight-line fit of one
  point's price on another's rebuilds a missing month exactly, the agreement's formula pointing at it); the retention
  now resets monthly, so only a point on the same transporter rebuilds it. Ask B's first device, a month and day
  exchanged, found a qualifying outage on one unit only; replaced by an entry dated a day late.
- 2026-10-20, stage 4 round 1 on architecture 3: both readers missed the call (the start-state fill, five units:
  the architecture holds) but kept 17 of 18 ask figures each (score_reader exit 1 on the asks): the meters on one
  transporter differ by exactly the same amount every day, so the missing invoice month was rebuilt exactly, and the
  day-late outage entries started 24 hours from their true reports, inside the readers' 30-hour pairing window. Ask A
  re-sited to strip billing (weekend and holiday gas on one line dated on the strip's last gas day, no missing month);
  ask B to entries a month early. The round-1 briefs quoted the leak sweep's line carrying the committed call; later
  briefs paraphrase it.
- 2026-10-20, stage 4 round 2 on architecture 3: readers 3 and 4 missed the call again (five units; four of four
  readers now) and kept 18 of 18 ask figures each: the strip lines reconciled exactly on the gas day, and rule 3.2's
  definition of a later report (overlapping, or repeating type, cause, length and hours under other dates) was a
  procedure they executed. Both flagged the regular start-up shape, OP_TIME 1.00 in every operating hour and the
  repeated outage pairs as looking generated. The month-early entries and the definition are gone; ask B is now
  IEEE 762's EFOR; the meter quantities run midnight to midnight on standard time; start and shutdown hours are part
  hours; each unit has its own start shape and each start its own size. The round-2 re-judge returned DETERMINISTIC,
  FIX_NOW on wording (the write-up now states the air-loss fill by what the record shows, the fill of air-loss hours
  without a measured hour after them, and the strip rule with its quantity tie).
- 2026-10-20, stage 4 round 3 on architecture 3: readers 5 and 6 missed the call (six of six now) and kept 10 and 1
  of 18 ask figures: reader 5 priced the strip days at the next line from the quantity tie and kept the contract's
  gas day despite the calendar-day tie; both left IEEE 762's reserve-shutdown term out of the outage rate. The
  round-3 judge returned NOT_DETERMINISTIC: no file tied the SCR to instrument air (the first hour back fitted a
  restart transient as well as an uncontrolled loss), the pooled start-up profile moved DF-1, and the asks' strip
  pricing, meter clock and EFOR terms were unfiled. The register now describes the SCR's ammonia flow control
  valves as air-to-open, rule 2.2 files that the NOx emitted counts in every operating hour, the pooled profile is
  ruled out by the record (asserted), and the asks' conventions are filed. Lowering DF-1's start-up outage share to
  cut its pooled sensitivity reshuffled every unit's draws and pulled CB-2 and AF-1 to within 0.005 of the target
  under interpolation; reverted.
- 2026-10-20, stage 4 round 4 on architecture 3: readers 7 and 8 missed the call (eight of eight; reader 7 at four
  units with a pooled start-up profile) and kept 18 and 12 of 18 ask figures: with the strip line, the meter clock
  and the EFOR formula filed, both asks were procedures executed. The fuel ask is dropped (the gas invoices and the
  agreement are now declared distractors) and both asks are IEEE 762 rates by the standard's own definitions, the
  formulas left to the standard and only the events, overlap rule, capacity basis and operating time filed; the
  golden EFOR now counts reserve-shutdown derates in EFDH as the standard does. Round-4 judge: DETERMINISTIC,
  FIX_NOW on the later-report rule (now: the earlier report counts for none of its hours).
- 2026-10-20, stage 4 round 5 on architecture 3: readers 9 and 10 missed the call (ten of ten) and kept 18 and 16 of
  18 IEEE 762 figures by reconstructing the standard; judge DETERMINISTIC, APPROVE. A failed-start device for EFORd
  (fuel burned with no operation) died on paper: Part 75 makes any hour with fuel combusted an operating hour, which
  would put device rows in the call's population. Taken instead, on the coordinator's measured list: revisions under
  the same event number (D2, latest revision, not latest delivered). An event spanning a month written once per month
  (D6) was screened and dropped: rule 3.2's overlap rule already resolves it.
- Architecture 3 (combined-cycle NOx with instrument-air gaps filled at the uncontrolled level) as a whole: spent at
  stage 4 on 2026-10-20 by the coordinator's ruling under the author's rule that both scored readers must miss the
  call. Eleven of twelve readers missed it, but reader 12 in round 6 landed it from the register's "air-to-open flow
  control valves", the grounding the round-3 judge required (1 of 6 readers since that line went in). A premise the
  judge needs filed becomes readable once filed, so the next decisive step must rest on a structure only a
  cross-record or cross-period cut shows, which no filed line describes. Carried forward: the event-revision ask
  device (a forced outage revised to MO or D4 under one event number with a later report date, no adjudicating
  sentence), which held at 0 of 18 for both round-6 readers; the realism fixes (part-hour loads under nameplate,
  start profiles that differ by unit). Dropping "air-to-open" was ruled out: it reopens the round-3 judge's finding.

- 2026-10-20, at stage 4 (architecture 4 spent): isolated reader 1 (sonnet, medium, fresh unzip) landed the call and
  all 24 ask figures (score_reader.py exit 1). It saw that the remittance's bulk lines tie to the roster's counts each
  month, read the member-level lines as retroactive adjustments, netted them per member and month (3,009 added, 923
  removed, rate cell pairs to zero) and noted the result equals the remittance total: the 820 is self-describing, an
  adjustment layer over a tied roster, and reconciling a roster to capitation is the reflex of any health plan ETL
  analyst, so the exposure rebuild is a work order, not a stump. The pharmacy latest-line device fell to the same
  reflex (5,646 claim numbers with two lines, each taken at its later line). Lesson for the re-root: a decisive step
  whose evidence is a second source that ties to the first and carries signed corrections is found by the first
  reconciliation; and the latest-line-per-key device is spent in this lane. Reader 2 and the judge were stopped.
- 2026-10-20, at stage 4 (architecture 5 spent): isolated reader 1 (sonnet, medium, fresh unzip) landed the call
  (L01, L03, L05, L14) and 12 of 24 ask figures (score_reader.py exit 1). It scaled each count to the year class by
  class with the four classifying stations unprompted: the traffic monitoring guide itself recommends class-specific
  factors where classifying stations exist, so with classifying stations in the pack the decisive step is the field's
  reflex, not a skipped step (readability test 3 misjudged as silent). On the asks it keyed visits on terminal, tag
  and gate_out, which defeats Berth 20's standard-time in-gate for visit counts, and stitched Berth 40's rail ramp
  legs by their RG1 lanes; it missed only the Berth 20 turn times and Pacific Gateway's voided keyings. Lessons: a
  decisive step the field's own guidance names is a reflex for a model that knows the guidance; a shared gate_out is
  a key the reader will find; a lane code that names a gate is read. Reader 2 and the judge were stopped.
- 2026-10-20, at stage 4 (architecture 6, round 1): both isolated readers missed the call (reader 1 L03, L04, L06,
  L07, L11, L12; reader 2 the class-factor default L01, L03, L05, L06), but reader 2 kept 20 of 24 ask figures: it
  deduplicated trucks by VIN and read blank model years from the certification list, so neither device sat on its
  path. Re-sited: the open carrier moves' VINs keyed with O or I, and gliders whose model_year is the chassis's.
- 2026-10-31, the repair of architecture 6 (the port authority's air-corridor designations): the repair's determinism judge returned SEND_BACK; no shipped text said how a two-weekday count becomes a year's vehicle-miles, the golden's carrying rule (follow the vessel calls through the terminal's gate record) was filed nowhere, so the standard classifying-station factoring filed another designation, and the fleet answers needed an unfiled VIN rule. Lesson: an expansion or carrying rule the golden needs is the estimand's WHAT and is filed, or the design forces it; architecture 6 spent, re-rooted as architecture 7 in a new domain.
- 2026-10-31, architecture 7 at design: a world without the 2025 resit rules let the unmatched resits file the golden (38, the cross-switch candidates' first scores mixed like the history's); the free near-miss resit within six weeks and the six-month wait under 55, the awarding body's own rules from 1 October 2025, make the candidates reaching the new paper low first-scorers, so the unmatched route files 37 and matching decides.
- 2026-10-31, architecture 7 at design: a provider-count ask (each training provider's candidates on the new paper) was executable from the provider list's merger note, so the cracker kept it whole; replaced by the yearly first sittings and passes, which turn on the re-registered candidates as the monthly ask does.
- 2026-10-31, architecture 7 at design: the remote sittings' UTC stamps as a month-boundary device: remote sittings run 07:00 to 23:59 UK time, so in British Summer Time no UTC stamp crosses a UK date and the device moved nothing; kept as Layer 1 only.
