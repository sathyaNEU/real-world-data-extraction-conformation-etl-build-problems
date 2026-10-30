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
  below: a partial fix files the same wrong call as no fix. Measured on the cut pack: the default 83.83 per cent (1,208
  of 1,441 completers), the degree half alone 76.89 (1,108), the short-term half alone 77.79 (1,121), the golden 70.85
  (1,021). Medical Assisting (100 completers) carries the degree half and the Commercial Driver License program (87)
  the short-term half.
- **World:** an unnamed U.S. Mountain West state; its State Workforce Development Board and the board's grant programs
  office; Larkspur Basin Community College, four campuses (Fennimore and Ridgefield on the older student system, Copper
  Flats and Antelope Springs on the newer one); the State Education and Workforce Data Center, which publishes the
  outcomes release. People from `guard.py names --geo
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

1. Read the board's Workforce Value Designation Standard: a credit program passes on its completers' median earnings
   in the third full calendar year after the award year, every campus and both award years taken as one group, at or
   above USD 34,200 in 2025 dollars; a short-term program passes when at least 70 per cent of its grant completers were
   working for an employer on the 180th day after completing; the designation renews at 75 per cent of the 2024-25
   completers of tested programs in passing programs.
2. Conformed the two completion extracts (two student systems, two layouts, two ID formats), the outcomes release's
   two editions (a wide workbook coded by the awards' CIP codes, a long file coded by current CIP 2020 codes, other
   colleges and other years-after rows, Paralegal Studies' cells suppressed), the roster and the wage records (amended
   reports superseding originals, other providers' participants) to one program list through the inventory.
3. Took each credit program's median as its campus-by-cohort cells' medians averaged by completers with earnings, the
   2024 medians in 2025 dollars.
4. Counted a grant completer as working on day 180 when the wage records show pay from any employer in the calendar
   quarter that holds day 180.
5. Applied the tests and summed the 2024-25 completers in passing programs.

Ends on: the designation renews, 84 per cent of the system's 2024-25 completers in passing programs (1,208 of 1,441),
Medical Assisting passing at 36 thousand dollars and the Commercial Driver License program at 91 per cent.

Golden: the designation lapses, 71 per cent (1,021 of 1,441): Medical Assisting's pooled median is 33 thousand dollars,
under the benchmark, and the Commercial Driver License program's day-180 share is 63 per cent, under 70; each
correction alone leaves the share at 77 or 78 per cent.

## Stump sentence

The default path averages each credit program's campus-by-cohort medians by completers and counts a short-term
completer as working on day 180 whenever any employer paid them in the quarter holding that day, and keeps the
designation at 84 per cent; but Medical Assisting's rural campus pays its completers a tight 30 thousand dollars while
its two metro campuses' completers, many of them part-year, spread from 13 to 66, so the program's pooled median (33
thousand) sits under the line its averaged median (36) clears, and 22 of the CDL program's 79 grant completers left their
first carrier weeks before day 180 and started at the next weeks after it, still drawing that quarter's partial pay,
so the jobs dated from their own pay put the CDL share at 63 per cent; with both the designation lapses at 71 per cent,
and either correction alone leaves it at 77 or 78.

## Three rules

Task type: census-register-administrative-data-quality (Survey Research & Official Statistics), a task type serving
Data Extraction & Conformation (ETL): an outcomes release of campus-by-cohort cells and a set of employer-quarter wage
records, conformed with two campus completion extracts, the grant roster and the program inventory into the board's
designation file.

Domain test: the call turns on two quantities administrative employment statistics estimate from outcome releases and
employer wage records, a program's median earnings as the half point of its cells' released distributions pooled by
completers, and a completer's work status on the 180th day dated from a job's pay in its first or last quarter against
its pay in a full quarter (the job-flow reading of quarterly wage records).

Swap: "which wards keep their accreditation because their patients' median stay is under four days and 70 per cent
were at home on the 180th day" reads differently at once, because a hospital's records are dated claims and unit
stays: no released cell hides the ward's pooled stay and no quarter hides the day a patient went home.

Layer 1: the two completion extracts in two student systems' layouts (a workbook with seven-digit IDs and SIS program
codes, a CSV with LB numbers, dashed state IDs and numeric program IDs); the outcomes release in two editions whose
layout and coding changed (a wide workbook under a two-line title coded by the awards' own CIP codes, Information
Technology and Criminal Justice under their pre-2022 codes, and a long CSV coded by current CIP 2020 codes), other
colleges' and other years-after rows in both, Paralegal Studies' cells suppressed; employer-quarter wage rows in which
an amended report supersedes the original, other providers' participants and pre-program jobs; the roster's withdrawals
and the cohorts before and after the window. Each is how the producing system writes its records; nothing is placed to
be caught, and none moves the call when handled the obvious way (asserted: the CIP recodes missed, the CPI factor
missed, amended reports summed or ignored, untested programs counted or grant completers used as weights all leave the
call where it is).

Layer 2: estimation that fits the data's structure, twice: a median of a pooled population from its parts' released
distributions rather than their medians, and an event date inside a reporting period from the period's partial amount
against a full period's.

Decisive step: rebuilding each credit program's earnings distribution from its cells' five percentiles and taking the
pooled half point, and dating each short-term completer's job starts and exits inside the quarter that holds day 180
from that job's pay there against its pay in a full quarter; the share crosses 75 per cent only when both are done.

Not semantics: a solver who reads every field right (the release's cells are campus by cohort, percentiles are of
earnings among completers with earnings, wage rows are pay per employer per quarter, the completion date is the
section's last day) still averages the cells' medians and still reads pay in the quarter as work on the day, because
no field holds a pooled median or a start date.

Not rule application: no filed rule says how a group's median is computed from released cells or how a day's status is
read from quarterly pay. Measured on the cut pack. The degree half's enumerated family (cells' medians averaged,
unweighted or their median, the percentile points pooled as a sample, a log-normal through each cell's five points,
and the interpolations) spreads the graded figures 1,919 to 4,789 dollars, Medical Assisting 32,411 to 37,100; the
standing family (every interpolation through the released percentiles: straight in dollars, straight in log dollars,
monotone cubic, any tail anchors) spreads 69 to 149 dollars and files one whole-thousand cell for every program. The
short-term half's enumerated family (pay in the quarter, the second quarter after exit, earnings floors of 500, 1,000
and 2,500 dollars, beginning-, end- and full-quarter employment, the position-chosen point-in-time measure, a
day-proportional share, a half-quarter pay threshold, a person-level pay ratio) spreads the CDL figure 59 to 91 per
cent, 31.6 points; the standing family (the job-level pay ratio against the adjacent full quarter, the full quarters'
mean, the two beside the partial one or the job's median quarter, a pay-lag correction of 0, 7 or 14 days, a calendar
or a 91-day quarter: twenty-four variants) spreads it by zero on every program.
What rules out the rest is the data, never a clause: the log-normal misses a released percentile by up to 57.7 per
cent (a median 7.7 at each cell's worst point), the percentile points pooled as a sample do not pass through the cells'
own percentiles, and the 31 jobs that put 22 CDL completers in the quarter route's count paid a median 20 per cent of
their own full quarter there (8 to 67), the mark of a job that ended or began inside the quarter.

Analyst test: with every field read and the board's standard applied, the easy route averages the cells' medians and
counts pay in the day-180 quarter as work on day 180, and files the designation as renewed at 84 per cent; the golden
lapses it at 71 (asserted by `checks.py` on the generator's clean truth and on the cut pack).

Estimand: the board's Workforce Value Designation Standard (in the pack, sections 3 to 5) fixes the population (the
program's completers in award years 2020-21 and 2021-22 across every campus, as the release counts them with
earnings; the grant participants who completed a section ending from 1 July 2024 to 30 June 2025), the outcomes
(median earnings in the third full calendar year after the award year, every campus and both award years taken as one
group, in 2025 dollars; working for an employer on the 180th day after the section's last day), the units, the windows
and the comparisons (USD 34,200, 70 per cent, 75 per cent of the 2024-25 completers of tested programs).

No decoy: nothing is planted to be caught; no memo, draft, briefing, dashboard or stakeholder figure argues for the
averaged medians or for pay in the quarter, and no shipped artifact ranks the programs on the tests.

No certified replay: no certified or published figure is reproduced to recover a method; the release's percentiles are
the data the pooled median is built from, not controls for a hidden rule.

Lesson: a median of a pooled population comes from its parts' distributions, not their medians, and a status on one
day inside a reporting period is read from a record's partial amount against a full one; no build on file teaches the
first (no pooled-median screen in any slot note), and the nearest teach allocating a period's total by an indicator
(task123) or starting an onset from a seasonal profile (task476), not dating a job from its own partial pay.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the cells' medians averaged by completers; any pay in the quarter holding day 180 (the default path: renews at 84) | standard 3.1's "median annual earnings" beside a release of medians; 4.2's wage records: fires | the release's Median column; the wage rows' year and quarter: fires | dashboards weight cell medians; the federal performance measure counts wages in a quarter: fires | none | none | one weighted mean; one join and a filter | readable |
| R1, the cells' medians unweighted or their median; the second quarter after exit; an earnings floor in the quarter | none | the same columns | the federal second-quarter measure; substantial-earnings floors: fires | none | none | one group-by | readable |
| R2, beginning-, end- or full-quarter employment (same employer in the adjacent quarters), or the one nearer day 180 | none | the wage rows by employer and quarter | the job-flow statistics' point-in-time measures: fires | none | none | one self-join on employer | readable |
| R3, the percentile points pooled as a sample, or a log-normal through each cell's points | none | five percentile columns invite a distribution | fit a distribution to quantiles: fires | none | none | one sort, or one regression per cell | readable |
| R4, a day-proportional share of a partial quarter, a half-quarter pay threshold, or a person-level pay ratio | none | the wage amounts | interpolate by position: fires | none | none | one formula per completer | readable |
| R5, each cell's distribution rebuilt through its five released percentiles and the pooled half point solved (decisive) | none: the standard files the group's median, not how a release of cells yields it | none: no column holds a program's median or a pooled count at a value | none: the field's habit is to weight the cells' medians | none: the release publishes no program-level figure to reconcile to | none | a root of a weighted sum of piecewise functions | silent |
| R6, each job paid in the quarter holding day 180 dated from its pay there against its own full quarter, start or exit (decisive) | none: the standard files the day, and a wage record as a quarter's pay | none: no start or end date anywhere in the grant's records | none: the field's habit is to read employment from wages in a quarter | none: no file dates any job | none | a per-job ratio no column suggests | silent |

R5 is silent: averaging the cells' medians by completers is what published dashboards do and the averaged figure is a
plausible median for every program; nothing in the pack computes a pooled distribution or names one. R6 is silent: the
grant's records date nothing but sections, every wage row is a well-formed quarter's pay, and the default path's
counts reconcile (every completer with pay in the quarter is counted once).

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a credit program's earnings figure | the median of the group's earnings, every campus's published cells and both award years taken as one group | the cells' medians averaged, unweighted or their median | renews (the default) | standard 3.1, "taken as one group": a group's median is a point of the group's distribution, which a mean of its parts' medians is not; asserted |
| SF2 | the third full calendar year after the award year | 2024 for 2020-21, 2025 for 2021-22, the release's three-years-after rows | the release's one- or five-years-after rows | not a live reading | standard 3.1's parenthesis and the technical notes' earnings year; asserted |
| SF3 | 2025 dollars | 2024 earnings times 1.0294, 2025 earnings as published | no adjustment | same call; six figures move | standard 3.2; asserted |
| SF4 | a suppressed cell | left out; Paralegal Studies has no published cell and is not tested | imputed | same call | standard 3.4; asserted |
| SF5 | a program's CIP code across editions | the 2024 edition's pre-2022 codes for Information Technology and Criminal Justice joined through the inventory | those two programs' 2020-21 cells missed | same call | the inventory's earlier-CIP column and the technical notes' coding; asserted |
| SF6 | the 180th day after the day they completed | the section's last day plus 180 days | plus 179 (the completion day counted as day 1) | same call, same figures | asserted: no completer's job starts or ends within 24 days before or 14 days after day 180 |
| SF7 | the day a participant completes | the roster's section end for the participant's section | the campus extract's completion date | same call, same figures | standard 4.1; the two agree for every grant completer; asserted |
| SF8 | working for an employer on the 180th day | a job covered by unemployment insurance running on that day | any wages reported in the quarter holding it | renews (the default) | standard 4.1, "on the 180th day", and 4.2, "a wage record is the wages ... in one calendar quarter": a quarter's pay is not a day's work; asserted |
| SF9 | an amended wage report | replaces the original for the same participant, employer and quarter | the original kept; both summed | same call, same figures | standard 4.2; asserted |
| SF10 | grant completers | the roster's participants with exit reason Completed in sections ending 1 July 2024 to 30 June 2025 | the campus extracts' short-term completers | same call | standard 4.1 ("Career Training Grant participants"); asserted |
| SF11 | at least 20 grant completers | Forklift and Material Handling (18) not tested | tested on its 20 completers in the extracts | same call | standard 4.4; asserted |
| SF12 | a program's 2024-25 completers | the completion extracts' completers at every campus, grant participants or not | the grant completers for short-term programs | same call (70.68 and 83.73) | standard 5.2; asserted |
| SF13 | programs not tested | in neither the numerator nor the denominator | in the denominator as not passing | same call (69.31 and 82.01) | standard 5.2; asserted |
| SF14 | comparing a figure with its line | as computed, before rounding | the rounded figure | same call | standard 5.3; asserted: the nearest figures are 1,143 dollars and 6.7 points from their lines |
| SF15 | which test a program takes | credit programs (Medical Assisting and Paralegal Studies certificates of 34 and 32 credits included) the earnings test; clock-hour programs the placement test | a certificate read as short-term | not a live reading | standard 2.2 ("of one academic year (30 credits) or more") and the inventory's lengths; asserted |
| SF16 | ask A's year | the sessions dated 1 July 2024 to 30 June 2025 | the sessions of the sections that ended in the year | ask figures only | the asking sentence ("attended from July 2024 to June 2025"); asserted |
| SF17 | ask A's hours | each session's time read as hours and minutes after the point, the repeated rows once | decimal hours; the repeated week kept | ask figures only | C4 separate: every program's full sessions are whole hours, and of the entries a late arrival or early departure cut short none runs past 59 after the point and every one is a whole five minutes; the repeated rows are the same participant, section, date and time twice; asserted |
| SF18 | ask B's principal | every subsidized and unsubsidized dollar the completer borrowed at the college in any award year: each disbursement before July 2024, returns netted, and each 2024-25 loan's amount once; the median and the total over the program's completers who borrowed | the rows summed as exported; one amount per loan in every year; the 2024-25 award year alone; the parent PLUS loans | ask figures only | the asking sentence ("all the Direct Subsidized and Unsubsidized Loan principal they borrowed at the college") and the cost of attendance's annual limits and installments: two rows of a 2024-25 subsidized loan summed run past the subsidized annual limit for over a thousand borrowers, one row never does; asserted |
| SF19 | rounding | each figure from its unrounded value, rounded once, halves up | per line or per cell | same call, same figures | asserted: no graded figure within a tenth of a rounding unit of an edge |

## Ladder

Measured on the cut pack and asserted in `checks.py` (the share of the 1,441 completers of tested programs in passing
programs; the line is 75).

| Rung | Credit programs | Short-term programs | Share | Call |
|---|---|---|---|---|
| R0 (default) | cells' medians averaged | any pay in the day-180 quarter | 83.83 | renews |
| R1 | unweighted or median of medians | second quarter after exit; floors of 500 to 2,500 | 83.83 | renews |
| R2 | averaged | beginning-, end-, position-chosen or full-quarter employment; prorated; half-quarter; person ratio | 75.85 to 83.83 | renews |
| R3 (one half) | pooled through the percentiles | any pay in the quarter, and every R1, R2 and R4 reading but full-quarter | 76.89 | renews |
| R4 (other half) | averaged, unweighted or median of medians | each job dated from its own pay | 77.79 | renews |
| R5 (golden) | pooled through the percentiles (straight, log or monotone cubic) | each job dated from its own pay (twenty-four variants) | 70.85 | lapses |

Two routes off the ladder also lapse, and neither files the golden: full-quarter employment with pooled medians
(68.91, Phlebotomy failing at 64 per cent and every short-term figure moved), and the crude poolings (the percentile
points as a sample, a log-normal) with dated jobs (70.85, six to ten of the eleven credit figures moved).
The default path's error is one-sided: it passes two programs the records fail (Medical Assisting, 100 completers, and
the CDL program, 87). Margins: the golden 4.15 points under the line, each one-half fix 1.89 and 2.79 over it, the
default 8.83 over; every rung's share is fixed by whole-program pass and fail sets, so no rung sits within a completer
of the line.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | credit programs: the release's published cells for award years 2020-21 and 2021-22 at every campus; short-term: the roster's completers of sections ending in the window | filed (standard 3.1, 3.4, 4.1); C1 |
| 2 Unit of account | a program; a completer within it | the question names the program; SF15 |
| 3 Attribution window | award years 2020-21 and 2021-22; sections ending 1 July 2024 to 30 June 2025; 2024-25 completers | filed (3.1, 4.1, 5.2); C1, no section ends on a boundary |
| 4 As-of dating | the editions and records as shipped (October 2026) | the files' own ranges; C1 |
| 5 Version basis | an amended wage report replaces the original | filed (4.2); SF9 asserted |
| 6 Denominator | the share: completers of tested programs; the placement figure: grant completers | filed (5.1, 5.2, 4.1); SF12, SF13 asserted |
| 7 Weighting | the cells pooled by completers with earnings; programs weighted by 2024-25 completers | filed ("taken as one group"; 5.1); SF1, SF12 |
| 8 Window length | the third full calendar year after the award year; the 180th day | filed (3.1, 4.1); SF2, SF6 |
| 9 Boundary inclusivity | at or above the benchmark; 70 and 75 per cent or more | filed; C1, nothing within 1,143 dollars or 1.89 points of a line |
| 10 Rounding path | lines compared unrounded; figures rounded once | filed (5.3); SF14, SF19 asserted |
| 11 Tie-break | none: no figure on its line | C1, asserted margins |
| 12 Maturity and censoring | every completer's day 180 and the next two quarters inside the wage records (to 2026 Q2) | C1, asserted |
| 13 Order of operations | 2024 earnings into 2025 dollars before pooling; supersede amended reports before dating | filed (3.2, 4.2); C1 (pooling is invariant to the order once each cell is converted) |
| 14 Row order | none: every figure is a set computation | asserted over shuffled rows |
| 15 Duplicate resolution | amended over original wage reports; a person once per program in the release | filed (4.2; technical notes); SF9 |
| 16 Identity normalisation | programs through the inventory (SIS codes, numeric IDs, CIP before and after 2022, grant program IDs); students by state ID with or without dashes | the inventory; C1, every row joins; SF5 |
| 17 Netting against gross | none on the main path; ask B's returns net against their loan | SF18 |
| 18 Dimensional units | dollars of 2024 and 2025; per cent | filed (3.2); SF3 |
| 19 Code and status semantics | exit reason Completed; suppression S; loan types old and new | dictionary and file semantics; never the stump; SF10, SF4 |
| 20 Integerisation | completer counts whole; shares of whole counts | C1 by construction |
| 21 Clause scope | the earnings test for credit programs, the placement test for clock-hour programs | filed (2.2); SF15 |
| 22 Forward window contents | the designation governs 2027-28; the call rests on closed records | not live: the standard's tests read closed records |

## Literal reader

Executed word for word, the prompt and standard sections 3 to 5 ask for each credit program's median earnings with
every campus and both award years taken as one group, among completers the release counts with earnings, and for each
short-term program's share of grant completers working on the 180th day after their section's last day, then the
share of 2024-25 completers of tested programs in passing programs. Neither the group's median nor anyone's status on
a day is published: the release carries campus-by-cohort cells and the wage records carry quarters' pay, so the
literal estimand is unobserved on both halves and is estimated from the records. The standing estimators agree on the
graded figures (every interpolation through the released percentiles files one whole-thousand cell per program; the
24 job-level pay-ratio variants file one count per program), and every reading of every term in the fork table
files the same call or is ruled out by a quoted sentence. The golden is the literal estimand's estimate, not a reading
of a term.

## Oracles

None ties only under the golden. No file publishes a program's pooled median, a pooled share at the benchmark or any
completer's start or exit date; the release's percentiles and the wage amounts are the data the golden is built from,
and every route reads them. No file ranks the programs on their tests or reports the system's share. For the asks: the
attendance export is not summarised by program anywhere and states no session's length, the inventory's clock hours
are one participant's schedule (the referee that separates the readings of a session's time without handing over any
program's total); the loan export carries no column of a loan's amount beside its disbursements' amounts, and no file
states a completer's principal.

## Ask sheet

Two asks, both on files the call never reads: the college's attendance export for the grant's participants (ask A);
the college's Direct Loan disbursements and its cost-of-attendance statement (ask B). Zero device rows sit in the
call's population: the attendance and the loans are read by no step of the call, and the roster and completion
extracts they join to are read by the call only for counts the devices do not touch (asserted, X1 and X2).

- **Ask A, each short-term program's clock hours its grant participants attended from July 2024 to June 2025, whole
  hours (11 figures).** H18 home: the instruction the grant bought, program by program, beside the outcomes it is
  judged on. User: the board's grant office, reporting training hours delivered under the grant. Primary device: D3
  units set per source, hours and minutes in a decimal column (the attendance system writes a session's time as hours
  and minutes after a point; nothing in the export or the documents says so). Every program meets in whole-hour
  sessions, so a full session reads the same either way and a completer at every session totals the inventory's clock
  hours under both readings; the device lives in the sessions a late arrival or early departure cut short (a tenth of
  them, each cut by a whole five minutes), whose entries never run past 59 after the point: read as decimal hours the
  figures fall 2 to 45 hours short. Hazards: the export appends the week of 3 March 2025 a second time at its end
  (exact duplicates), late enrollees and leavers attend only part of a section, the sessions of sections that
  straddle the year's ends. Files and columns: the attendance export (participant, course reference number, session
  date, hours), the roster (participant, program, course reference number, section dates, enrolled on, exit date),
  the inventory (clock hours). Stops: the times as decimal hours (0 of 11), the repeated week kept (3), both (0), the
  sections that ended in the year (4 or fewer), the completers' sessions alone (0), the golden.
- **Ask B, each credit program's median and total, over its 2024-25 completers who borrowed, of all the Direct
  Subsidized and Unsubsidized Loan principal they borrowed at the college, nearest 10 dollars (24 figures).** H18 home: the debt side
  of the same completers' workforce value, a measure every credit program carries that the call does not turn on.
  User: the board's grant office and the college's consumer information. Primary device: D6 an event's quantity on
  every line it covers (the aid system that went live on 1 July 2024 writes the loan's gross amount for its award year
  on each of the loan's disbursements, in the GROSS_AMT column the old system filled with each disbursement's gross
  amount; the cost of attendance's annual limits and "disbursed in installments, normally one each semester" are the
  evidence: two rows of a 2024-25 subsidized loan summed run past the 4,500-dollar subsidized limit for 1,136 borrowers,
  one row never does), with its over-cleaning half (one amount per loan, or alike rows kept once, in every year halves
  the old system's two-installment loans). Hazards: returned disbursements as negative rows under status Returned,
  parent PLUS loans under two code sets, two ID formats for the state student ID, the cost of attendance's origination
  fee (the export's amounts are gross). Stops: the rows summed as exported (0 of 12 medians, 0 of 12 totals), one
  amount per loan in every year (0, 0), alike rows kept once (0, 0), the 2024-25 award year alone (0, 0), every amount
  read as net (0, 0), returned rows dropped (5 medians, 0 totals), parent loans kept (2 medians, 2 totals), the golden. Every program's borrower count is odd and every completer's principal a whole
  10 dollars, so each median is one completer's principal at the centre of its bin.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | the attendance export's sessions dated in fiscal 2025, exact duplicates dropped, each time read as decimal hours | miss |
| B | each completer's Subsidized and Unsubsidized rows as exported, returns netted, parent loans left out | miss |

Measured partial handlings on the cut pack: ask A keeps 11 of 11 once the session times are read as hours and minutes
and 3 of 11 if the repeated week is then kept; ask B keeps 24 of 24 once each 2024-25 loan counts once and 0 of 24 when
every loan counts once. A response that finds both devices scores 100; one that finds neither scores 45 on the call; one
that finds only ask A's keeps under a third of the 35 ask figures.

Pair ceiling: 28.5 (the cracker 38 + 7 with none of 35 ask figures, the mirror 5 + 7 with none).

Mirror leakage: 0.0 per cent of ask weight.

Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

1. Domain: administrative employment statistics' own estimates from an outcomes release and employer-quarter wage
   records, a program's median earnings as the half point of its cells' released distributions pooled by completers
   and a completer's status on the 180th day dated from a job's pay inside its first or last quarter; with a hospital's
   nouns no released cell hides a pooled median and no quarter hides the day a job began or ended.
2. Real work, nothing planted: every Layer 1 item is what the producing system writes (two student systems' extracts,
   two release editions with the CIP recodes and Paralegal Studies' suppression, amended wage reports, the roster's
   withdrawals and the cohorts outside the window, the attendance export's minutes after the point and its re-sent
   week, the new aid system's annual amount on each disbursement); none is on the decisive step, and no ask device row
   sits in the call's population (X1 and X2).
3. The step that flips the call is analytical: pooling the released distributions and dating each job from its own
   partial pay; no clause makes either choice (standard 3.1 files the group taken as one and 4.1 the 180th day, not how
   a released cell becomes a median or a quarter's pay a day's status).
4. Analyst test: every field and rule read correctly, the averaged medians and any pay in the day-180 quarter file the
   designation as renewed at 84 per cent (asserted on the clean truth and on the pack); either correction alone files
   78 or 77, both together 71, lapsed.
5. The standard files the estimand (population, outcomes, windows, units and comparisons in sections 3 to 5) and no
   estimator; the standing family (every interpolation through the released percentiles with any tails, and the 24
   job-level pay-ratio variants) files one whole-thousand cell per credit program and one count per short-term program
   (G1, G3), and the asks' conventions are filed in their asking sentences or closed by the data (SF16 to SF18).
6. No decoy, no withheld rule against a stated one, no certified replay.
7. The lesson is on no other card: nearest task266's stump at 0.07, task477's ledger row at 0.05 and task229 v3's driver
   at 0.07; task39 differentiated on the card.
8. Re-read against the built pack at stage 4: eight isolated readers over four rounds filed the designation as renewed
   at 77 per cent (the pooled medians with any pay in the quarter), and none dated a job from its own pay; the round 4
   readers on the shipped cut (zip 7d3d1845) kept 0 and 11 of the 35 ask figures (0 and 31.4 per cent).
9. Judge pass 1 DETERMINISTIC, FIX_NOW (ask A's counting and ask B's window not literally filed, the credit programs'
   year undefined, the CDL figure moved under two further dating references: ask A re-sited, ask B's window put in its
   asking sentence, standard 2.2's 30 credits filed, the dating family widened to 24 variants with every completer
   dated alike); passes 2 to 4 DETERMINISTIC, APPROVE, Gate G method_or_model_selection and analytical_non_defect,
   Gate H domain pass, layers pass, decisive step analytical. Pass 4, on the shipped cut, kept no competing answer and
   left two minor notes: the attendance export does not label its hours (the data forces hours and minutes, SF17), and
   the dating step sits near data semantics (it is the unit-of-analysis choice between a day inside the quarter and the
   quarter itself).

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
- A late calendar for one of the CDL campuses (sections ending the last Friday of a quarter, day 180 late in the next
  quarter but one), so a half-quarter threshold would count the early leavers: their first jobs began the week after
  completing and so never had a full quarter before the quarter holding day 180, and no record dates them; dropped for
  a calendar putting day 180 on the quarter's first days.
- Phlebotomy and Pharmacy Technician as the traps for the strict readings (completers leaving shortly after day 180 and
  starting shortly before it inside the quarter): every strict reading then failed them, so full-quarter employment
  with the averaged medians filed the golden share to the decimal (71.3) and the golden call; rebuilt so only
  full-quarter employment fails Phlebotomy, at 64 per cent, and Medical Assisting's 100 completers keep that reading
  with the averaged medians on renews (75.85).
- An ask on each credit program's release coverage (completers with earnings over completers in the college's own
  2020-21 and 2021-22 records), its device the older student system dating awards by their posting: the extract's only
  date column would then be literally the award date, so a literal reader files the device's wrong answer.
- An ask on the grant's completion rates with a case-management migration closing open records as withdrawals: the
  record shape is the migration duplicates both top responses removed on the portal (16 rev 3).
- Borrower counts beside ask B's medians: every handling that leaves out parent loans and nets returns lands all 12,
  so the counts were free to the cracker; cut.
- Ask A's device a section's fee on every participant line of the board's line export from January 2025: the judge read
  the export's amounts summed as what the board paid (a fork, not a device), and reader A kept all 11 figures through
  the inventory's fee per section and the register; replaced by the invoice header's program on every old line and the
  hand-keyed invoices outside the register.
- Ask B's device the aid system writing disbursements net of the origination fee from July 2023: both readers grossed
  the amounts up from the cost of attendance's fee sentence and the cents the net amounts carried (12 of 12 each);
  replaced by the loan's amount on each of its disbursements from July 2024.
- Day-180 status accepted when the golden's job dating agreed with the simulation: the judge's two other references
  (the adjacent and far quarters averaged, the job's median quarter) moved the CDL figure 50 to 54 of 79 through exits
  whose far quarter was a few weeks' pay. Requiring every dating reading to agree and redrawing in the shared stream
  moved every later path and put the half-quarter threshold under the line for the CDL program (53 of 79, landing the
  call); kept with the four disagreeing completers redrawn from their own streams.
- Ask A's second devices, the old billing system writing the invoice header's program on every register line and the
  hand-keyed supplementary invoices outside the register: both round 2 readers compared each register line's program
  with its participant's program in the roster (507 and 434 lines flagged) and kept the CE invoices by their program
  ID, 11 of 11 each, while the call (77 per cent, renews) and ask B (0 of 12) held; the tuition reconciliation runs on
  three files that check one another line by line, so no device on its path stays silent. Replaced by each short-term
  program's clock hours attended, read from an attendance export that writes hours and minutes.
- Ask A's clock hours from sessions scheduled to the half hour (7.30 on every full session of six programs): both
  round 3 readers read the hours as hours and minutes, one from the 7.30 entries and one because only that reading
  gave the inventory's clock hours, 11 of 11 each; reader F also caught ask B (two subsidized rows of 4,500 over the
  4,500 limit), 23 of 23, while every reader of three rounds missed the call. Kept with whole-hour sessions, the
  minutes only in the sessions cut short, and ask B doubled to each program's median and total.
- The prompt without the standard's name: the portal's prompt check failed P6 on 2026-10-28 (no pass line, no renewal share and no renewal rule cited, and the reviewer saw no input files); the question now cites the State Workforce Development Board's Workforce Value Designation Standard by its title, the thresholds left in the standard and no ask, file, unit or rounding moved.
- Closing the portal's day-180 fork (determinism block of 2026-10-28, Gates C, D and E: the CDL program's day-180 status read from quarterly wage records as 47, 50, 65 or 72 of 79 grant completers, the last two passing and renewing the designation at 76.9 per cent) with a filed sentence: every closure spends the stump. The eight in-house readers and the portal's judge all pooled Medical Assisting's cells and missed only the dating (77 per cent, renews), so the judge's both-neighbours rule (which also moves CDL to 59 per cent), the golden's dating filed in standard 4.2, or a definition ruling out the quarter's pay each let that path land the call. The fork was the stump; back to design rather than shipped as a determinism fix.
