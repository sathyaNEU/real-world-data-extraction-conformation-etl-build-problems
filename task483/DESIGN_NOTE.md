# task483 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 1, drawn 2026-10-23 from seed ET40 (the
world, the decision and the quantity kept, the pitfall found again from the data under the 10/10 rules): a state
workforce board deciding whether a multi-campus community college system keeps its workforce-value designation for the
2027-28 grant year, which needs at least 75 per cent of the system's completers in programs that pass the board's
tests.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task483.json` (architecture v1), registered 2026-10-23 after a pull,
  `check` re-run on the filed card: WARN only (strategy risk answered under `## Three rules`; government_agency
  overused across the corpus, the honest organisation here). `test.same_driver_older` against task39 (objective, G19,
  etl_conformance) is answered by the card's differentiation: task39 recovers a stop rule from a corpus of settled
  disputes; nothing here is recovered from a corpus.
- **Redrawn at the draw, and why the labels are the honest ones.** The window moved twice while the card was written.
  First government_agency, programme_officer and shape 10 were in it (task171 v4, task176 v2, task274 v2), so the
  first form had the system's own institutional research office as the analyst (university_or_school, research_desk,
  shape 07). The pull before registration brought task275 and put university_or_school, research_desk, shape 07, G2
  and G3 in the window (task179 v3, task173 v3, task275) while government_agency and programme_officer left it. The
  board's grant programs office is the honest analyst in any case: it holds its grant completers' wage records under
  the grant's participant agreement and has only the state's public outcomes release for degree programs, which is
  exactly the data reality the decisive step lives in. Shape 16: each program's test is one indicator of the system's
  share. Generator G19 (the board's standard reads a program's median and a completer's work on one day; the records
  hold cells' percentiles and quarters' pay), G16 second.
- **Pairing:** Survey Research & Official Statistics, task type `census-register-administrative-data-quality`, which
  serves ETL: two administrative sources, the state outcomes release (each campus's program by completion cohort:
  completers with earnings and five earnings percentiles, cells under 10 suppressed) and the employer-quarter wage
  records of the board's short-term grant completers, conformed with the system's campus completer extracts into the
  board's designation file, one row per program with its test figure and whether it passes.
- **The decision and the quantity:** the board's Career Training Grant pays tuition only at designated providers. The
  designation for 2027-28 renews when at least 75 per cent of the provider's 2024-25 completers are in programs that
  pass: a degree or long-certificate program passes when its completers' median earnings in the third calendar year
  after completion (award years 2020-21 and 2021-22, every campus that offers it, pooled) are at or above the board's
  benchmark; a short-term program (under 600 clock hours) passes when at least 70 per cent of its July 2024 to June 2025
  grant completers were working for an employer on the 180th day after the day they completed. The quantity is the
  system's share; the call is whether the designation renews or lapses, with each program's figure and result.
  Forward facing: the designation decides which programs the grant pays for through 2027-28.
- **Shape:** `16`, indicators into one score: about ten degree programs' pooled medians and about ten short-term
  programs' day-180 shares, each passing or not, the system's share against 75 per cent, the program nearest each line
  and its shortfall; asks on records the call never reads (fixed at stage 2), a chart's named parts and the files.
- **Strategy:** `grain_or_unit` (the records sit at a coarser grain than the standard reads, twice); Gate G
  `etl_conformance`; gap `objective` (a cell's median and a quarter's pay are correct for what they record and are
  not the program median and the day's work status the designation is scored on); pattern none; generators G19, G16.
  Layer 2 family `estimation_fit`, pattern `own:a program median rebuilt from its cells' released percentiles, and a
  day's work status dated from a job's pay inside its first or last quarter`. No calibration organ.
- **The conjunction, sized at the build.** Each half moves a different set of programs: the degree half moves programs
  whose campuses or cohorts earn very differently (a completer-weighted mean of cell medians sits above the pooled half
  point when the cells are far apart and skewed by part-year earners); the short-term half moves programs whose
  completers often leave a first job in the months before day 180 or start one after it inside the same quarter. The
  generator sizes the halves so that the default path, the degree half corrected alone and the short-term half
  corrected alone each leave the system's share at or above 75 per cent, and only both corrections together put it
  below: a partial fix files the same wrong call as no fix. Target: default near 80, either half alone 76 to 78, golden
  near 71 (set at the build from `generator/figures.json`).
- **World:** an unnamed U.S. Mountain West state; its State Workforce Development Board and the board's grant programs
  office; a community college system of four campuses (names set at the build and screened by `guard.py surface`);
  the state's education research center, which publishes the outcomes release. People from `guard.py names --geo
  "United States" --seed 483`: Kathryn Petersen (the board's grant programs manager) and Rodney Randall (the research
  center's release lead).
- **Forcing fact:** the board votes the 2027-28 designations in March 2027 and the grant's 2027-28 appropriation is
  committed to designated providers' programs from July 2027.
- **Forum and forcing event:** funder_or_donor, budget_or_appropriation. Organisation government_agency; role
  programme_officer.
- **Data-native sentences:** (1) the outcomes release publishes each campus's program by cohort as its completers with
  earnings and their 10th, 25th, 50th, 75th and 90th percentile earnings, because the research center releases cells
  and never the program's pooled record; a program offered at a metro campus and a rural campus, or by a large cohort
  and a small one, has cells whose medians lie far apart, and its completers' median is the half point of the cells'
  pooled distribution, which the cells' medians averaged by completers overstate. (2) a wage record is one employer's
  pay to one person in one calendar quarter, so the day a job began or ended inside a quarter is written nowhere; a job
  that began or ended in the quarter holding a completer's 180th day shows only part of a quarter's pay there, and that
  pay against the same job's pay in a full quarter dates the start or the exit.
- **Default path and golden, by name:** degree programs' cell medians averaged by completers, and short-term
  completers counted as working on day 180 on any pay in the quarter holding it, keep the designation; the pooled half
  points and the dated jobs let it lapse. Names and figures are set at the build.
- **The WHAT screen.** Population: the system's programs, their 2020-21 and 2021-22 degree completers with earnings
  and their 2024-25 short-term grant completers. Outcome: median earnings in the third calendar year after the award
  year; working for an employer on the 180th day after completion. Unit: dollars; a completer. Window: the stated award
  years and days. Comparison: the benchmark, 70 per cent, 75 per cent. The decisive step settles none of them: it is
  how a program's median is computed from released cells and how a day's work status is read from quarterly pay, which
  no filed rule or procedure states.
- **Sources, one line each:**
  - published postsecondary earnings outcomes (the Census Bureau's Post-Secondary Employment Outcomes and state
    longitudinal data system dashboards) release cells as counts and percentiles, never pooled records;
  - the medians of parts do not combine into the median of the whole; a grouped or percentile release is pooled through
    each part's distribution (the median of a mixture);
  - administrative job-flow statistics (the Quarterly Workforce Indicators) read job starts and exits from employer
    quarter wage records by whether the same employer paid the person in the adjacent quarters, and a partial quarter's
    pay against a full quarter's measures the share of the quarter worked.
- **Same-puzzle and same-driver tests:** (objective, G19, renew_replace_lapse) and (objective, G19, etl_conformance)
  against the last twelve builds, lineage included: no match in the last twelve; task39 differentiated on the card.
- **Abstraction test:** the nearest drivers stripped of nouns: task229 v3 passes a day's mean through a convex
  conversion; task457 reads a period's amount from a report covering only part of it; task177 v2 times an intervention
  against a unit's recurring decision; task476 starts an interval-censored onset from a seasonal profile carried from
  another record; task477 re-dates a total by its payment schedules' weekdays; task123 allocates a billing period's
  total to months by an activity indicator. Here no total is allocated or re-dated: one half pools released
  distributions where the default averages their half points, the other dates a job's start or exit from that job's own
  pay in the quarter that holds the day the standard reads.

## Default path

1. Read the board's Workforce Value Designation Standard: a degree program passes on its completers' median third-year
   earnings at or above the benchmark, pooled over every campus offering it and the two award years; a short-term
   program passes when at least 70 per cent of its completers were working for an employer on the 180th day after
   completing; the designation renews at 75 per cent of the 2024-25 completers in passing programs.
2. Conformed the system's four campus extracts (two student-system layouts), the outcomes release's two editions
   (wide in 2024, long in 2025, suppressed cells) and the grant wage records (amended rows superseding filed ones,
   several employers per completer) to one program list through the CIP crosswalk.
3. Took each degree program's median as its campus-by-cohort cells' medians averaged by completers with earnings.
4. Counted a short-term completer as working on day 180 when the wage records show pay from any employer in the
   calendar quarter that holds day 180.
5. Applied the tests and summed the 2024-25 completers in passing programs.

Ends on: the designation renews, about 80 per cent of the system's completers in passing programs (programs and
figures set at the build).

Golden: the designation lapses, about 71 per cent (set at the build): each degree program's median is the half point
of its cells' distributions rebuilt from the five released percentiles and pooled by completers, and a short-term
completer works on day 180 only when a job paid in that quarter was running on that day, its start or exit there
dated from its pay that quarter against its pay in a full quarter.

## Stump sentence

The default path averages each degree program's campus-by-cohort medians by completers and counts a short-term
completer as working on day 180 whenever any employer paid them in the quarter holding that day, and keeps the
system's designation at about 80 per cent; but a program whose campuses or cohorts earn far apart has a pooled median
below its cells' averaged median, and a completer who left a job weeks before day 180, or started one weeks after it,
still shows that quarter's partial pay, so the pooled half points and the jobs dated from their own pay put the share
near 71 per cent, and either correction alone still leaves it above 75.

## Three rules

Task type: census-register-administrative-data-quality (Survey Research & Official Statistics), a task type serving
Data Extraction & Conformation (ETL): an outcomes release of campus-by-cohort cells and a set of employer-quarter wage
records, conformed with four campus extracts into the board's designation file.

Domain test: the call turns on two quantities administrative employment statistics estimate from outcome releases and
employer wage records, a program's median earnings as the half point of its cells' released distributions pooled by
completers, and a completer's work status on the 180th day dated from a job's pay in its first or last quarter against
its pay in a full quarter (the job-flow reading of quarterly wage records).

Swap: "which wards keep their accreditation because their patients' median stay is under four days and 70 per cent
were at home on the 180th day" reads differently at once, because a hospital's records are dated claims and unit
stays: no released cell hides the ward's pooled stay and no quarter hides the day a patient went home.

Layer 1: the four campus extracts in two student-system layouts (the two older campuses' system dates completions by
the award posting, the two newer by the section's last day); the outcomes release in two editions whose layout
changed (wide to long) with cells under 10 completers suppressed; employer-quarter wage rows in which an amended row
supersedes the filed one; several employers per completer in a quarter; CIP 2010 codes in the 2020-21 cohort against
CIP 2020 in the program list. Each is how the producing system writes its records; nothing is placed to be caught, and
none moves the call when handled the obvious way.

Layer 2: estimation that fits the data's structure, twice: a median of a pooled population from its parts' released
distributions rather than their medians, and an event date inside a reporting period from the period's partial amount
against a full period's.

Decisive step: rebuilding each degree program's earnings distribution from its cells' five percentiles and taking the
pooled half point, and dating each short-term completer's job starts and exits inside the quarter that holds day 180
from that job's pay there against its pay in a full quarter; the share crosses 75 per cent only when both are done.

Not semantics: a solver who reads every field right (the release's cells are campus by cohort, percentiles are of
earnings among completers with earnings, wage rows are pay per employer per quarter, the completion date is the
section's last day) still averages the cells' medians and still reads pay in the quarter as work on the day, because
no field holds a pooled median or a start date.

Not rule application: no filed rule says how a pooled median is computed from released cells or how a day's status is
read from quarterly pay. The enumerated family on the draw's prototypes: for the degree half, the completer-weighted
mean of cell medians sits 2.7 per cent below to 7.5 per cent above the pooled median on cells of 30 to 160 completers,
a log-normal fitted through the five points 2 to 11 per cent below, and the interpolation family (linear in dollars,
linear in log dollars, monotone spline) within 155 to 634 dollars of each other; for the short-term half, pay in the
quarter overstates the day-180 share by 0 to 24 points, continuous pay across three quarters understates it by 4 to 29,
day-proportional shares of the partial quarter miss by 1 to 10 either way, and the job-level pay ratio matched the
simulated truth for every one of 583 completers once no deciding start or exit sat within 28 days of day 180. The
standing family is the interpolations that pass through every released percentile and the job-level ratio's variants
(reference quarter, day count, cut), measured at the build to name one set at the graded rounding. What rules out the
rest is the data, never a clause: the log-normal misses the released 10th percentile by a fifth, and pay of a few per
cent of a full quarter cannot be work on a day six weeks into it.

Analyst test: with every field read and the board's standard applied, the easy route averages the cells' medians and
counts pay in the day-180 quarter as work on day 180, and files the designation as renewed at about 80 per cent; the
golden lapses it at about 71 (figures set at the build and asserted by `checks.py` on the generator's clean truth).

Estimand: the board's Workforce Value Designation Standard (in the pack, its sections on the degree test, the
short-term test and the designation) fixes the population (the program's completers in the named award years across
every campus; the short-term grant completers of July 2024 to June 2025), the outcomes (median third-year earnings;
working for an employer on the 180th day after the section's last day), the units, the windows and the comparisons
(the benchmark, 70 per cent, 75 per cent of the 2024-25 completers).

No decoy: nothing is planted to be caught; no memo, draft, briefing, dashboard or stakeholder figure argues for the
averaged medians or for pay in the quarter, and no shipped artifact ranks the programs on the tests.

No certified replay: no certified or published figure is reproduced to recover a method; the release's percentiles are
the data the pooled median is built from, not controls for a hidden rule.

Lesson: a median of a pooled population comes from its parts' distributions, not their medians, and a status on one
day inside a reporting period is read from a record's partial amount against a full one; no build on file teaches the
first (no pooled-median screen in any slot note), and the nearest teach allocating a period's total by an indicator
(task123) or starting an onset from a seasonal profile (task476), not dating a job from its own partial pay.

## Tried and rejected

- The seed's earnings-premium test alone, the pooled median rebuilt from each cell's quartiles (P25, P50, P75): on
  realistic skewed cells of 10 to 70 completers eight licensed reconstructions (log-normal and log-logistic through the
  quartiles, split log-normal, linear in dollars or log dollars, monotone spline, normal) spread 500 to 1,650 dollars
  on the pooled median, as wide as the naive error (0.4 to 5.8 per cent), so Gate C and Gate F could not both hold.
- The same with five released percentiles: the family tightens to 155 to 634 dollars, but the decisive step is then one
  choice a solver enumerates (average the cells' medians or rebuild them), the coin-flip shape of the client's measured
  tasks; kept only as one half of a conjunction.
- The release's count of completers at or above the benchmark per cell: the test becomes exact (a median clears the
  line when half the pooled completers do, and counts add), but the column hands the step to any solver who reads it,
  and the graded medians stop being computable.
- Earnings known only for aided (or SSN-linked) completers, reweighted to all completers: the reweighting is a reflex
  (task482 v2 and v5 readers weighted by reflex) and missing at random is untestable, so a literal judge can read the
  linked completers' median as the measure.
- Earnings released only above a full-time floor: recognising the floor is a field reading, and once recognised the
  quantile shift pushes the solver into distributions, so the pooling follows.
- Out-of-state work estimated for completers who moved to states outside the wage exchange: assumption-bound, no
  determinate golden.
- The day-180 placement test alone: once no deciding start or exit sits within 28 days of day 180 the job ratio is exact,
  but pay in the quarter then lands within 0 to 4 points of the golden unless exits fall early in the quarter and
  starts late in it, and day-proportional shares land near the golden whenever day 180 sits near a quarter's edge; kept
  only as the other half of the conjunction, with each program's completion calendar and job flows set so the halves
  carry the share.
