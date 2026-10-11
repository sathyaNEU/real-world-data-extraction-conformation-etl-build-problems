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
but there the decisive step is the unit the standard error is built over. task180 was re-rooted on 11 October to
architecture 3 (which of three spontaneous-report drug signals the national registries support, decided by a
within-patient comparison under channelling): another health signal one draw back, but its decisive step is a
comparison design against confounding, not a count read before its records have arrived.

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

## LADDER (shipped; every rung asserted by name in `generator/checks.py`)

Areas as built (2021 census usual residents): Wagga Wagga 67,609, Griffith 27,134, Leeton 11,391, Narrandera 5,847,
Murrumbidgee 3,902, Hay 2,896, Edward River 8,456, Junee 6,595, Cootamundra-Gundagai 11,292, Snowy Valleys 14,395.
Share of each area's cases through Inland Pathology: Griffith 0.94, Leeton 0.90, Murrumbidgee 0.18, Narrandera 0.12, Hay
0.10, Edward River 0.07, the rest 0.04 to 0.05 (adult serology goes to Inland Pathology from every area).

Route speeds as shipped (specimen collection to notification, local dates):

- Hospital laboratory (Wagga Wagga Hospital Laboratory; daily district courier, PCR runs Monday to Saturday, results
  authorised next morning): median 2 days, 95th percentile 5 (12-month history, 198 notifications); 100% within 14
  days and 98% within 7 for specimens collected August 2025 to July 2026 (196 notifications).
- Private route (Inland Pathology; courier Tuesday and Friday at 10:30 to Sydney, weekly Thursday screen, positives
  confirmed on the Tuesday run, keyed the next working day, a few urgent requests run on arrival): median 12 days, 95th
  percentile 21 over the 12-month history (96 notifications; 22 over the whole extract); 76% within 14 days and 8% within
  7 for specimens collected August 2025 to July 2026 (96 notifications).

| Rung | Construction | First (excess or score) | Next | Margin | Griffith | Killed by |
|---|---|---|---|---|---|---|
| 0 | Cases notified with specimens 21 Sep to 4 Oct | Wagga Wagga 9 | Griffith 7 (= Snowy Valleys) | 1.29 | 2nd, tied | PR-07 4.2 is an excess over the expected count |
| 1 | PR-07 excess on the cases notified so far | Wagga Wagga 7.6 | Griffith 5.6 (= Snowy Valleys) | 1.36 | 2nd, tied | the fortnight is not all notified: Inland Pathology notifies 8% of specimens within 7 days and 76% within 14 |
| 1b | The same on notification date, protocol's expected count | Wagga Wagga 10.6 | Griffith 6.6 | 1.61 | 2nd | PR-07 4.2 and 3.5 count specimens collected |
| 1b' | The same, expected count also on notification dates | Wagga Wagga 10.6 | Griffith 6.2 | 1.71 | 2nd | as 1b |
| 2 | Notified over expected | Wagga Wagga 6.43 | Griffith 5.00 (= Snowy Valleys) | 1.29 | 2nd, tied | PR-07 4.2 is a count excess |
| 3 | Nowcast on one delay pooled across the unit (aggregate inflation, 12 months, daily) | Wagga Wagga 13.43 | Griffith 10.13 (= Snowy Valleys) | 1.33 | 2nd, tied | the pooled delay is mostly the hospital route's; Inland Pathology's is several times slower |
| 4 (answer) | Nowcast each area on its own route's delay (aggregate inflation, 12 months, daily, by route) | **Griffith 30.97** | Wagga Wagga 9.74 | 3.18 | 1st | |

Expected counts (PR-07 4.3, mean of 21 September to 4 October in 2021 to 2025): Wagga Wagga, Griffith and Snowy Valleys
1.4; Leeton and Cootamundra-Gundagai 0.6; Narrandera and Edward River 0.4; Murrumbidgee, Hay and Junee 0.2. Notified in
the fortnight: Wagga Wagga 9, Griffith 7, Snowy Valleys 7, Cootamundra-Gundagai 2, Edward River, Leeton and Narrandera 1,
the rest 0. The rung 3 and 4 figures are the generator's internal estimates; no nowcast figure is stated in any shipped
or graded sentence.

**The world behind the extract** (the simulation, never shipped): cases with specimens collected in the fortnight are
Griffith 41, Wagga Wagga 11, Snowy Valleys 8, against 7, 9 and 7 notified (asserted: Griffith at least four times its
notified count, the two hospital-route areas within 30 and 20 per cent).

**Twin pair (shipped).** Griffith and Snowy Valleys both have 7 notified and 1.4 expected, so rungs 0 to 2 and the pooled
rung 3 (10.13 each) cannot separate them. Snowy Valleys' 7 all came through the hospital laboratory; 6 of Griffith's 7
came through Inland Pathology (4 routine on 21 and 22 September, 2 urgent requests on 29 September and 1 October) and 1
through the hospital laboratory (an emergency department swab on 30 September). Every route-specific cell puts Griffith's
estimate at 2.51 or more times Snowy Valleys' (asserted per cell); Snowy Valleys' estimates run 7.1 to 11.8.

**Margins (shipped, all asserted).** Every route-specific cell: Griffith first, its excess at least 2.70 times the next
area's (target 2.5). Every rung 0 to 3: Wagga Wagga first and Griffith not, margins 1.29 to 1.71 (target 1.25). Wagga
Wagga's notified excess beats the next area by 36 per cent (7.6 against 5.6; target 25). Every pooled cell: Wagga Wagga
first by 1.25 to 1.37.

## GRID (shipped, asserted cell by cell)

Estimators: aggregate inflation (each route's or area's notified fortnight over the mean completeness of the fortnight's
days); per-day inflation (each specimen day over its own completeness, days below 5 per cent merged into the nearest
older day at or above it, a merged bin taking the mean completeness of its days); a reporting-triangle chain ladder
(development factors from every cohort in the window up to 4 October, recent partial cohorts included, the same merge
rule). History: specimens collected in the 6, 12 or 24 months to 23 August 2026 (six weeks before the extract day; no
notification in the extract took more than 36 days). Strata: by laboratory route or by area. Bins: daily, or weekly
(Monday-based specimen weeks and development weeks).

- **54 cells, 0 misses.** 36 route-specific cells (3 estimators x 3 windows x 2 strata x 2 bins) all give Griffith; 18
  pooled cells (3 x 3 x 2) all give Wagga Wagga.
- Minimum route-specific margins by family: by route, aggregate daily 2.98 and weekly 3.08, per-day daily 6.69 and
  weekly 3.78, chain ladder daily 6.96 and weekly 3.82; by area, aggregate daily 2.70 and weekly 2.97, per-day daily 5.56
  and weekly 3.45, chain ladder daily 3.82 and weekly 3.71. The thinnest cell is aggregate, 6 months, by area, daily:
  Griffith 28.1 against Wagga Wagga 10.4.
- Pooled cells: Wagga Wagga first in all 18, margins 1.25 (per-day and chain ladder, weekly) to 1.37.
- Variants, asserted: the 24-month window with the 2024 epidemic months (24 August to 31 December 2024) removed, and
  delays measured on each case's first notification instead of every notification, in every estimator, stratum and bin:
  every cell keeps its winner; route-specific minimum 2.56.
- Mess neutrality of the main call, asserted: the fortnight and the five prior-year windows hold no repeat notification,
  no probable case, no split postcode and no visitor, so the counts and expected counts are identical with the episode
  rule ignored, probable cases dropped, split postcodes taken by the first row or by any unit area.

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

As shipped: axis 9 (boundary): the nearest rung margin is 1.29 (rungs 0 and 2). Axis 10 (rounding):
expected counts are exact fifths and print at one decimal; the slide's route shares are whole per cents, 76.04 and 100.
Axis 12 (maturity): history ends 23 August 2026 and the longest gap in the extract is 36 days. Axis 4 (as-of): no
notification is received on 5 October before 07:00, so the extract day and its eve agree. Axis 5 (version basis): the
fortnight and the prior windows carry one notification per case.

## ASK SHEET (shipped)

| Ask | Figures | Shipped answer |
|---|---|---|
| A. 1 Jan to 31 Aug 2026 by area (CSV): confirmed, probable, infants under six months, of those admitted, of those born to a mother vaccinated 14 days or more before birth | 10 x 5 = 50 | Wagga Wagga 63, 2, 3, 2, 1; Griffith 25, 3, 2, 1, 1; Leeton 11, 0, 1, 0, 1; Narrandera 5, 0, 1, 0, 0; Murrumbidgee 0, 0, 0, 0, 0; Hay 2, 0, 0, 0, 0; Edward River 7, 1, 1, 1, 0; Junee 3, 1, 1, 0, 1; Cootamundra-Gundagai 15, 2, 1, 1, 1; Snowy Valleys 9, 1, 1, 1, 0 |
| B. School clusters (slide): students, specimens 5 Sep to 4 Oct, two or more | 5 schools x 3 | Banna Avenue Public School, Griffith, 5; Wollundry Public School, Wagga Wagga, 3; Blowering Road Public School, Snowy Valleys, 2; Bolton Park High School, Wagga Wagga, 2; Kooyoo Street Public School, Griffith, 2 |

Devices as built: two laboratories for one infant (I2, a GP swab to Inland Pathology then an admission swab); a Leeton
student notified by both laboratories; serology-only cases probable from 1 July 2024; infants placed clearly inside or
outside six months (no case in the ask period aged 5.7 to 6.3 months); admissions within 3 days of the specimen or 30 days or more
away (a newborn admission, a later bronchiolitis admission); maternal dTpa at 24 to 30 weeks, 8 to 11 days before birth,
or in an earlier pregnancy only (more than a year before), or influenza only; MRNs as eight-digit text in the line list
and births, numeric in the PAS extract; the mother's Medicare number as card plus IRN in the births, spaced card and a
separate IRN in the register; interview school names as written; a staff case, a parent case and a preschooler recorded
as a student; a Cootamundra student swabbed on 4 September and notified on 7 September; split postcodes 2652, 2655,
2665, 2706, 2722, 2727, 2729 (two of them allocate outside the unit).

**Ask stops** (each asserted to move its figures): episode rule ignored (A: Wagga Wagga confirmed 63 to 69, infants 3 to
4, admitted 2 to 3, Griffith 25 to 27, Edward River 7 to 10 and three more; B: Canal Road Public School, Leeton, becomes
a cluster of 2); probable cases not counted (A: every probable figure to 0; B: Bolton Park High School drops out);
admissions without the 14-day link (A: Wagga Wagga admitted 2 to 3, Leeton 0 to 1); antenatal dTpa at any time before
birth (A: Wagga Wagga vaccinated 1 to 3, Narrandera 0 to 1, Edward River 0 to 1); any antenatal vaccine (A: Griffith
vaccinated 1 to 2); infants under twelve months (A: Wagga Wagga infants 3 to 6 and Griffith 2 to 3, with their admitted
and vaccinated figures); split postcodes by the first row (A: Wagga Wagga 63 to 61, Cootamundra-Gundagai 15 to 18, Snowy
Valleys 9 to 6) or to any unit area (A: Wagga Wagga 63 to 66); school names matched exactly (B: no clusters at all);
staff counted (B: Bolton Park High School 2 to 3); parents counted (B: Banna Avenue Public School 5 to 6); the window by
notification date (B: Hurley Street Public School, Cootamundra-Gundagai, becomes a cluster of 2); the preschool merged
into the school of the same name (B: Wollundry Public School 3 to 4).

Use test: the huddle sees the area, the clusters and the year's infant picture every week. Decoupling (asserted): ask
A's rows share none with the fortnight; neither ask moves with any nowcast estimator; the
fortnight holds no ask device on the main call's columns (no repeat notification, no probable status).

## PINS (shipped)

PR-07 v3.1 (`PR-07_pertussis_response_protocol.pdf`, effective 2 March 2026): 1.1 and 1.2 scope and the ten areas; 2.1
to 2.4 case definition, the 1 July 2024 revision and both statuses counted; 3.1 one row per laboratory notification, 3.2
onset imputation (specimen date less 10 days), 3.3 the 90-day episode rule, 3.4 residential postcode and the larger
population share for split postcodes, 3.5 every count dated by first specimen; 4.1 one area a week from the 07:00
Monday extract, 4.2 the deciding excess, 4.3 the expected count, 4.4 team leader confirmations; 5.1 the cluster rule and
the slide, 5.2 cluster follow-up; 6.1 infants, 6.2 the admission link, 6.3 the maternal vaccination link; 7.1 the
quarterly report. Line-list notes: field semantics, the school fields added to the interview on 1 September 2026, the
linked files. No shipped sentence mentions the time a notification takes, completeness, backfill or nowcasting
(asserted over every text-bearing file and the prompt, with the banned list in `checks.py`).

**Why 4.2 reads as the eventual count, the main Gate C risk.** 4.1 names the 07:00 extract as the day's data and 4.2
names the quantity: cases with specimens collected in the 14 days before the extract day, the same quantity 4.3 counts
on the same 14 dates in five complete years. A case exists from its positive specimen (2.1, 3.5), not from its
notification, and the expected count is built on years in which every case has long since been notified, so setting
the cases notified so far against it is not like for like. The literal reading (count what the extract holds) is rung
1; the leak reader's pass 1 planned it in those words ("PR-07 has no lag adjustment") while noting Griffith's slow
route, so the judge is pointed at this sentence.

## PACK GATES (shipped)

| File | Format | Rows | Role |
|---|---|---|---|
| `pertussis_notifications_2019-2026.csv` | csv | 1,118 | the line-list extract (spine) |
| `pertussis_line_list_notes.md` | md | | field notes |
| `SIPHU_PERTUSSIS_LINELIST_job_20261005_0700.txt` | txt | | the state system's run report (checksum and row count of the extract) |
| `PR-07_pertussis_response_protocol.pdf` | pdf | | governing protocol |
| `postcode_lga_concordance.xlsx` | xlsx | | postcode lookup with ratios; area populations on a second sheet |
| `respiratory_admissions_2019-2026.csv` | csv | 29,036 | PAS respiratory admissions (ask A) |
| `birth_records_2024-2026.csv` | csv | 5,983 | maternity births (ask A) |
| `antenatal_vaccinations_2019-2026.parquet` | parquet | 35,724 | antenatal vaccination register (ask A; the volume gate) |
| `school_rosters_term3_2026.xlsx` | xlsx | | nine schools' rosters (ask B) |
| `influenza_notifications_2026.csv` | csv | 1,476 | distractor (named in `metadata.json`) |
| `cd_weekly_report_2026_wk35.pdf` | pdf | | distractor (named in `metadata.json`) |

11 files, 6 formats (csv, md, parquet, pdf, txt, xlsx); two files over 25,000 rows; two distractors named in
`metadata.json`, asserted unused (the golden recomputes unchanged with each removed). Goldens:
`golden/response_team_brief.pptx` (one slide) and `golden/pertussis_cases_by_lga.csv`. `checks.py`: 423 assertions
passed. `verify.py` (standard library, openpyxl and pyarrow, no code shared with `golden.py`): OK, Griffith, rungs 0 to
3 Wagga Wagga, 5 clusters, 50 ask A figures and both route speeds, each matched against the goldens. Two consecutive
builds byte-identical over `target/`, `golden/` and `metadata.json` (sha256).

## BUILD RECORD

- `generator/build.py` runs everything: the pack (`sim.py`, `records.py`, `docs.py`, `postprocess.py`), the goldens
  (`deliver.py` over `golden.py`), `metadata.py`, `checks.py`, `verify.py`, then a second full build into a scratch
  folder inside the task (gitignored, removed after) and the sha256 comparison.
- History: per-area Poisson draws on a district rate curve (near zero 2020 to 2022, the 2024 epidemic, a moderate 2025,
  an August 2026 rise in Wagga Wagga) with per-area multipliers, each area's stream the first seed whose prior-year
  windows hold the designed totals; September 2026 and the ask A infants are designed records with their notification
  times drawn from the route mechanisms, conditioned on being received by 07:00 on 5 October or not. The urgent-request
  stream seed (3) was chosen by search over 16 seeds for the margins (Tried and rejected).
- Containers: workbooks and the slide repacked with in-fiction owners and saved stamps and fixed entry stamps; PDFs
  issued on their in-fiction dates with the library banner blanked at equal length; the producer audit is clean.
- Invented names (H21): Southern Inland Public Health Unit and Local Health District, Inland Pathology, Wagga Wagga
  Hospital Laboratory, and the schools Banna Avenue, Kooyoo Street, Wollundry, Bolton Park High, Blowering Road, Canal
  Road, Hurley Street, Twynam Street and Fernleigh Road (street or place words with a school type, no saints); no check
  against a real school register was possible offline.

## LEAK CHECK (stage 4, mechanical half)

`leak.py task181 --asof 2026-10-05`: REVIEW, no LEAK (the first run was LEAK once, on the protocol's file name ending
`_v3.1`; fixed in the generator, the version is inside the document). Each REVIEW line:

- `cd_weekly_report_2026_wk35.pdf`, golden figure 100: the bulletin's "rate per 100,000"; the golden's 100 is the
  hospital laboratory's 14-day share, which the bulletin never states. Harmless.
- `PR-07_pertussis_response_protocol.pdf` carries 4 of 5 words of the committed call: response team, Griffith (only in
  the list of the ten areas), this week; the protocol names no area as the deployment. Harmless.
- Design-note vocabulary in PR-07 (12 terms), the bulletin (6), the run report (the scheduler job log, 4) and the notes (7): their own subject
  matter (specimens, expected, excess, notified, episode, public health, population); none mentions the time a notification takes,
  completeness, pooling or estimating unreported cases (asserted). Harmless.
- Ranking artifacts: PR-07 lists the ten areas without figures; the bulletin counts notifications received to 30 August
  by area (a past quantity, correct, on notification weeks, and not the decision fortnight); the line list is the data;
  the concordance lists postcodes and populations; the rosters carry each school's area. None ranks the areas on the
  decision question. Harmless.
- Dates after the setting in `antenatal_vaccinations_2019-2026.parquet`: `estimated_due_date` of pregnancies still in
  progress (allow-listed, H16; no dose or birth date is after the extract). Harmless.

**Solver's-eye read, pass 1 (isolated reader, 2026-10-11).** Question 1 quoted PR-07 4.2, the rule the prompt sends the
reader to ("no file says which data step tips the result"); questions 2 to 4 none. Its plan counted the extract's cases
against 4.3 and filed Wagga Wagga (7.6 against Griffith and Snowy Valleys 5.6), noting that Inland Pathology "reports
about 12 days after collection ... so Griffith's last fortnight is incomplete. Report that, but PR-07 has no lag
adjustment": rung 1, found from the data, with no sentence in the pack naming the move. One leak: the rosters
workbook's sheets ran the five schools that are clusters on 5 October first and the four near-misses last, an order no
one could have known when the file was saved on 1 October (ask B). Fixed in the generator: the sheets now run in the
order the rosters were received, and Twynam Street's roster, dated before its only case was notified, is now received
on 29 September. Rebuilt: checks 423, verifier OK, byte-identical, leak.py REVIEW (the same twelve lines).

**Solver's-eye read, pass 2 (rebuilt pack).** Clean: question 1 again PR-07 4.2 as the measure the prompt cites,
questions 2 to 4 none, every REVIEW line harmless, the rosters now in arrival order with the clusters at sheets 4, 5, 6, 8
and 9. Its plan again files Wagga Wagga at rung 1 with the caveat that "PR-07 4.1 fixes the count to the 07:00 extract":
two independent readers took the literal operational reading, which is the stump and the Gate C question PINS answers
(4.2's quantity is the cases collected, set against 4.3's complete years; the client's own pin for this pattern is a
question about the latest weeks on data whose report dates make the delay estimable).

## DUPLICATE CHECK (stage 5)

- **Adjudicated pre-flight (clone-auditor, pass 1 on architecture 2, `clone_check_report.md`): CLEAN.** No Exact, Same
  seed, Dataset or Template finding, no Shape echo; the screen promoted no pair of 124 (nearest task93, 0.100, layout and
  formats only). Readings of the nearest cards (task91, task31, task99, task59, task229, task122, task180 v3): each turns
  on something else. Batch-level note, not this build's: the certified-record decoy in 7 of the 12 builds before it;
  task181 adds to none of the capped counts.
- **Idiom, acted on.** The run report was named on the corpus's `extract` stem (`pertussis_extract_run_20261005.txt`,
  as seven of the twelve builds before it name their provenance file); it is now the scheduler's own job log name,
  `SIPHU_PERTUSSIS_LINELIST_job_20261005_0700.txt`. No content or figure moved; rebuilt (checks 423, verifier OK,
  byte-identical), leak.py REVIEW with the file-name sweep clean. The two reader passes read the same content under the
  old name; no third pass for a rename.

## SURFACE (guard.py surface task181)

0 promoted pairs across 124 in scope; nearest neighbours task93 (surface 0.100, percentile 98), task90 (0.094), task72,
task51, task65 and task89 (0.093), none promoted. Personas in the cut pack: Cassandra Dawson, Janice Barker, Nathan Olson,
Tiffany Peters, all on the card (Colleen Brown is in the rosters workbook, which the scan does not read).

## DEVIATIONS FROM THE DESIGN (as built)

- **Private route speed.** The ladder's killing line said about a quarter of Griffith's completed cases are notified
  within 14 days; the build brief fixes Inland Pathology at a median of about 12 days and a 95th percentile of about 24,
  which puts 76% within 14 days (8% within 7). The slide states the 14-day shares as the brief asks and says in words
  that few specimens are notified in the first week.
- **Counts.** Expected counts are 1.4 for Wagga Wagga and the twin pair (targets 2.0 and 0.8) and the twin pair sits at 7
  notified (target 6): rung 2 (notified over expected) needs Wagga Wagga's ratio 25 per cent clear of the twin's while
  the twin's count carries the route-specific margin.
- **Position.** Griffith sits second, tied with its twin, on rungs 0 to 3, not fourth or fifth as `dataset-generation`
  6.2's position table prefers; the twin pair forces the tie and every rung margin is 1.29 or more.
- **Grid.** Three estimators as the build brief lists them; the design's negative-binomial delay model was not built.
  Rung 1b is asserted on both expected-count bases.
- **Files.** Population by area ships as the second sheet of the postcode workbook, not as its own file (no step reads
  it, so as a file it would have been a third, unnamed distractor). 11 files, not 12.
- **Volume.** The line list holds 1,118 notifications, not a few thousand: realistic pertussis rates for 160,000 people
  give this many, and the volume gate is carried by the admissions extract and the register.
- **Hospital route.** 100% of its notifications within 14 days; no artificial outlier was added.

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
- **Build, private route at a 09:30 courier pickup (median 13 days).** Kept 10:30, which gives the brief's median of 12
  and a 95th percentile of 21 to 23.
- **Build, every Sunday illness swabbed in an emergency department.** That sent about a fifth of Griffith's history
  through the hospital laboratory, so the by-area cells fell to 1.95 to 2.5 times the next area. Most Sunday illnesses
  are now swabbed by a GP the next working day (85 per cent), as general practice works.
- **Build, Griffith's notified fortnight as 5 routine Inland Pathology results, 1 urgent and 1 emergency department
  swab, with Griffith quieter in 2026 than the district.** The per-day and chain-ladder cells by area sat at 1.5 to 2.4
  times, because Griffith's six-month history held about 13 notifications. Griffith now runs a moderate 2026 background
  and its notified fortnight is 4 routine results from 21 and 22 September, 2 urgent requests and 1 emergency
  department swab, which is what a school outbreak's general practices and emergency department produce.
- **Build, a merged low-completeness bin divided by the completeness of the day it joins.** Read literally, one urgent
  result could swing a cell by a factor of three depending on whether a day sat just above or below 5 per cent; a merged
  bin now takes the mean completeness of its days, which is what pooling days means. It did not move any winner.
- **Build, urgent-request stream seeds 0 to 15.** All 16 give Griffith in every route-specific cell and Wagga Wagga in
  every pooled cell; only seeds 3 and 7 clear 2.5 times everywhere, and 7's pooled minimum is 1.24. Seed 3 ships.
- **Build, "Griffith Southside Public School".** The persona scan reads Griffith as a first name; renamed Kooyoo Street
  Public School.
- **Build, a PR-07 history line saying the deployment rule had been restated on the specimen collection date.** Dropped:
  it invites the question of why, and the answer is the time a notification takes.
- **Build, "(preliminary)" on the population sheet.** Dropped with the rest of that vocabulary (asserted by the banned
  word sweep in `checks.py`).
