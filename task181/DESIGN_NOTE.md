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

**Layer 2 (the analytical shortcut).** Completing the fortnight on one delay pooled across the unit. The protocol's
excess is defined on the cases with specimens collected in the 14 days before the extract, as the count will stand once
all are notified (4.2); the line list holds only the specimens that have been notified, and how many have is a property
of each area's laboratory route. A careful analyst who sees the shortfall still pools the delay across the unit; an
expert estimates each route's own specimen-to-notification delay from the completed history in the file and nowcasts
each area on it.

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
  duplicate notifications, applies the case definition, maps every case to its area, computes the protocol's
  expected counts exactly and reads 4.2's count as the fortnight's cases once all are notified still completes the
  notified counts on one delay pooled across the unit and sends the team to Wagga Wagga; only a nowcast on each area's
  own route shows Griffith's fortnight several times above its expected count. Rule application (the expected-count
  arithmetic, the episode rule, the cluster rule, 4.2's definition of the count) and data semantics (UTC stamps, the
  probable class) sit on lower rungs and in the asks.

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

A competent solver reads PR-07 4.2's count as the fortnight's cases once all are notified, completes each area's
notified count on one specimen-to-notification delay pooled across the unit and sends the team to Wagga Wagga (excess
13.43 against Griffith and Snowy Valleys 10.13); the step that lands it there is pooling the delay, when the pooled history is
mostly the hospital laboratory's and Griffith's swabs go by courier to Sydney through Inland Pathology, so that,
completed on each route's own delay, Griffith's fortnight is several times what has been notified (excess 30.97 against
Wagga Wagga 9.74).

## ENTITY AND UNIT OF VALUE

One local government area, one team-week. PR-07's excess is a count of cases (confirmed and probable) with specimens
collected in the 14 days before the extract day, as the count will stand once all their notifications have been
received (4.2), less the area's expected count for the same 14 days.

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
| 0 | Cases notified with specimens 21 Sep to 4 Oct | Wagga Wagga 9 | Griffith 7 (= Snowy Valleys) | 1.29 | 2nd, tied | PR-07 4.2's definition: the count is the fortnight's cases once all are notified, set against the expected count |
| 1 | PR-07 excess on the cases notified so far | Wagga Wagga 7.6 | Griffith 5.6 (= Snowy Valleys) | 1.36 | 2nd, tied | PR-07 4.2's definition: the count is the fortnight's cases once all are notified, and Inland Pathology notifies 8% of specimens within 7 days and 76% within 14 |
| 1b | The same on notification date, protocol's expected count | Wagga Wagga 10.6 | Griffith 6.6 | 1.61 | 2nd | PR-07 4.2 and 3.5 count specimens collected, once all are notified |
| 1b' | The same, expected count also on notification dates | Wagga Wagga 10.6 | Griffith 6.2 | 1.71 | 2nd | as 1b |
| 2 | Notified over expected | Wagga Wagga 6.43 | Griffith 5.00 (= Snowy Valleys) | 1.29 | 2nd, tied | PR-07 4.2's definition: a count excess, on the fortnight's cases once all are notified |
| 3 | Nowcast on one delay pooled across the unit (aggregate inflation, 12 months, daily) | Wagga Wagga 13.43 | Griffith 10.13 (= Snowy Valleys) | 1.33 | 2nd, tied | the pooled delay is mostly the hospital route's; Inland Pathology's is several times slower |
| 4 (answer) | Nowcast each area on its own route's delay (aggregate inflation, 12 months, daily, by route) | **Griffith 30.97** | Wagga Wagga 9.74 | 3.18 | 1st | |

Rungs 0 to 2 (1b and 1b' with them) read the cases notified so far, and 4.2's definition of the count kills them in
writing; they are the readings of a solver who skips the definition, not the stump. Rung 3 (the count completed on the
unit's pooled delay, Wagga Wagga) and rung 4 (each route on its own delay, Griffith) stand, and the step between them is
the stump.

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

The estimand (axis 12 with axis 4): pinned in PR-07 4.2, stated once in the highest-authority filed document. The count
is every case with a specimen in the 14 days as it will stand once all the notifications for those days have been
received, the quantity 4.3 counts in five complete years, and a case belongs to the 14 days of its first specimen
whenever its notification is received; the 07:00 extract is the day's data (4.1), not the count. Closure: the pin, which
defines what is counted and never how (the BANNED and METHOD sweeps in `checks.py`). The method stays open and is the
decisive step: completing the count on the unit's pooled delay gives Wagga Wagga in all 18 pooled cells, on each route's
own delay Griffith in all 36 route-specific cells.

As shipped: axis 9 (boundary): the nearest rung margin is 1.29 (rungs 0 and 2). Axis 10 (rounding):
expected counts are exact fifths and print at one decimal; the slide's route shares are whole per cents, 76.04 and 100.
Axis 12 (maturity): history ends 23 August 2026 and the longest gap in the extract is 36 days. Axis 4 (as-of): no
notification is received on 5 October before 07:00, so the extract day and its eve agree. Axis 5 (version basis): the
fortnight and the prior windows carry one notification per case.

## ASK SHEET (shipped)

| Ask | Figures | Shipped answer |
|---|---|---|
| A. 1 Jan to 31 Aug 2026 by area (CSV): confirmed, probable, infants under six months, of those admitted, of those born to a mother vaccinated 14 days or more before birth | 10 x 5 = 50 | Wagga Wagga 63, 2, 2, 1, 0; Griffith 25, 3, 1, 1, 0; Leeton 11, 0, 1, 0, 1; Narrandera 5, 0, 1, 0, 0; Murrumbidgee 0, 0, 0, 0, 0; Hay 2, 0, 0, 0, 0; Edward River 7, 1, 1, 1, 1; Junee 3, 1, 1, 0, 1; Cootamundra-Gundagai 15, 2, 1, 1, 1; Snowy Valleys 9, 1, 1, 1, 0 |
| B. School clusters in the area the team goes to (slide, PR-07 5.1): students, specimens 5 Sep to 4 Oct, two or more, at schools in that area | 2 schools x 2 | Banna Avenue Public School, 5; Kooyoo Street Public School, 2 (both Griffith schools on their rosters). Unit-wide, not graded: the same two with Wollundry Public School 3, Blowering Road Public School 2 and Bolton Park High School 2 |

Devices as built: two laboratories for one infant (I2, a GP swab to Inland Pathology then an admission swab); a Leeton
student notified by both laboratories; serology-only cases probable from 1 July 2024; infants placed clearly inside or
outside six months (no case in the ask period aged 5.7 to 6.3 months); admissions within 3 days of the specimen or 30 days or more
away (a newborn admission, a later bronchiolitis admission); maternal dTpa at 24 to 30 weeks, 8 to 11 days before birth,
or in an earlier pregnancy only (more than a year before), or influenza only; MRNs as eight-digit text in the line list
and births, numeric in the PAS extract; the mother's Medicare number as card plus IRN in the births, spaced card and a
separate IRN in the register; interview school names as written; a staff case, a parent case and a preschooler recorded
as a student; a Cootamundra student swabbed on 4 September and notified on 7 September; split postcodes 2652, 2655,
2665, 2706, 2722, 2727, 2729 (two of them allocate outside the unit).

**Ask stops** (each asserted to move its figures): episode rule ignored (A: Wagga Wagga confirmed 63 to 69, infants 2 to
3, admitted 1 to 2, Griffith 25 to 27, Edward River 7 to 10 and three more); probable cases not counted (A: every
probable figure to 0); admissions without the 14-day link (A: Wagga Wagga admitted 1 to 2, Leeton 0 to 1); antenatal
dTpa at any time before birth (A: Wagga Wagga vaccinated 0 to 2, Narrandera 0 to 1); any antenatal
vaccine (A: Griffith vaccinated 0 to 1); infants under twelve months (A: Wagga Wagga infants 2 to 6 and Griffith 1 to 3,
with their admitted and vaccinated figures); split postcodes by the first row (A: Wagga Wagga 63 to 61,
Cootamundra-Gundagai 15 to 18, Snowy Valleys 9 to 6) or to any unit area (A: Wagga Wagga 63 to 66); school names matched
exactly (B: no clusters at all); parents counted (B: Banna Avenue Public School 5 to 6). The call moves ask B too: a
solver who sends the team to Wagga Wagga lists Wollundry Public School 3 and Bolton Park High School 2, and one who sends
it to Snowy Valleys lists Blowering Road Public School 2 (asserted).

**Ask B devices that no longer touch the graded list** (each still asserted to move the unit-wide cluster set, and
recorded): staff counted (Bolton Park High School 2 to 3), the episode rule ignored (Canal Road Public School, Leeton,
becomes a cluster of 2), probable cases not counted (Bolton Park High School drops out), the window by notification date
(Hurley Street Public School, Cootamundra-Gundagai, becomes a cluster of 2) and the preschool merged into the school of
the same name (Wollundry Public School 3 to 4), all at schools outside Griffith. Every cluster window student lives in
the school's area, so reading "the clusters in the area" by residence gives the same list (asserted).

**Ask-only revision after portal round 1** (`supplemental-stumping` Part 12, 2026-10-11). Three devices, in the births,
the register and the admissions extract only; the line list and the other eight files keep their d6944e3 bytes and every
main-call figure on `golden.py` and `verify.py` hashes as shipped (the gate in `checks.py`). Draws from the `ask` streams.
Each cell is given as golden, then the natural read in brackets.

- **A1, a date of birth keyed month first.** The laboratory request's date of birth was keyed month first (11/02/2025
  read as 2 November), so the line list carries the swapped date; the birth record holds the date the baby was born and
  the mother's register due date sits on it. Rows: I1 (P7996616, Wagga Wagga, born 2025-02-11, request 2025-11-02) and
  I4 (P8102146, Griffith, born 2025-08-12, request 2025-12-08), their birth records and their mothers' doses. Cells:
  Wagga Wagga infants 2 (3), admitted 1 (2), vaccinated 0 (1); Griffith infants 1 (2), vaccinated 0 (1).
- **A2, a merged medical record number.** The presentation made a second MRN, recorded at follow-up and then merged in
  the PAS into the number issued at birth; the PAS and the birth record carry the surviving number and the line list's is
  in neither. Found on date of birth, sex and postcode, the baby the PAS holds where two fit (Griffith Hospital had two
  boys born 25 June). Rows: I5 (P9436908, Griffith, 01074380 to 00586193) and I10 (P6704032, Cootamundra-Gundagai,
  01846738 to 01007017), their birth records and admissions. Cells: Griffith admitted 1 (0); Cootamundra-Gundagai
  admitted 1 (0), vaccinated 1 (0).
- **A3, a reissued Medicare card.** The mother's card was reissued late in the pregnancy, so the tenth digit, the issue
  number, is one up on the birth record against the register's; the woman is the first nine digits and the IRN. About one
  mother in 25 across the births, and three infant mothers: I6 (Leeton, at 34 weeks), I8 (Junee, 34 weeks) and I9
  (Edward River, 35 weeks; her dTpa is now at 26 to 30 weeks, where the shipped design had it in the last fortnight).
  Cells: Leeton vaccinated 1 (0), Junee 1 (0), Edward River 1 (0).

The shipped method (d6944e3's `golden.py`) on the revised pack lands off the golden on 11 cells, 9 of them among round
1's 15 graded CSV cells (26 of their 42 points). The five confirmed and probable cells sit on the line list, which the
gate holds byte-identical, so they cannot move.

Use test: the huddle sees the area, the school visits it means and the year's infant picture every week. Decoupling
(asserted): ask A's rows share none with the fortnight and ask A does not move with any nowcast estimator; nor does the
unit-wide cluster set, but the slide's list is the clusters in the area the team goes to (PR-07 5.1, the team's school
visits under 4.4), so it follows the call and a wrong area carries a wrong list; the fortnight holds no ask device on
the main call's columns (no repeat notification, no probable status).

## PINS (shipped)

PR-07 v3.1 (`PR-07_pertussis_response_protocol.pdf`, effective 2 March 2026): 1.1 and 1.2 scope and the ten areas; 2.1
to 2.4 case definition, the 1 July 2024 revision and both statuses counted; 3.1 one row per laboratory notification, 3.2
onset imputation (specimen date less 10 days), 3.3 the 90-day episode rule, 3.4 residential postcode and the larger
population share for split postcodes, 3.5 every count dated by first specimen; 4.1 one area a week from the 07:00
Monday extract, 4.2 the deciding excess and the count it is taken on (below), 4.3 the expected count, 4.4 team leader
confirmations; 5.1 the cluster rule and
the slide's list (the clusters in the area the team goes to, its school visits under 4.4), 5.2 cluster follow-up; 6.1 infants, 6.2 the admission link, 6.3 the maternal vaccination link; 7.1 the
quarterly report. Line-list notes: field semantics, the school fields added to the interview on 1 September 2026, the
linked files. No shipped sentence mentions the time a notification takes, completeness, backfill or nowcasting
(asserted over every text-bearing file and the prompt, with the banned list in `checks.py`).

**PR-07 4.2 as shipped:** "The team goes to the area with the largest excess, over its expected count, of cases with
specimens collected in the 14 days before the extract day. The count is the number of such cases as it will stand once
all the notifications for those 14 days have been received, the same quantity 4.3 counts for each of the previous five
years. A case belongs to the 14 days in which its first specimen was collected, whenever its notification is
received." The author's wording, in the protocol's voice: a notification "is received" (`arriv\w*` is on the banned
list), "the 14 days in which its first specimen was collected" for "the fortnight of its specimen" (3.3, 3.5), and 4.3's
own "previous five years". No word on the banned list was needed, so no ban was narrowed, and `checks.py` adds a METHOD
sweep over the protocol (estimate, route, speed, model, adjust, forecast, predict, project, inflate, scale, weight,
complete). It also asserts that no other file restates the pin, and that built with d6944e3's 4.2 the protocol is
d6944e3's file to the byte. The version stays 3.1 with no history row (a history line invites the question of why;
Tried and rejected).

**Why 4.2 reads as the eventual count, the Gate C question.** It says so. The count is every case with a specimen in the
14 days as it will stand once all the notifications for those days have been received, the quantity 4.3 counts in five
complete years, and a late notification still counts in the 14 days of its first specimen. 4.1 still names the 07:00
extract as the day's data, so the count has to be reached from the extract, and no file says how. The earlier wording
("the largest excess of cases with specimens collected in the 14 days before the extract day over its expected count")
left the cases on the extract defensible: the portal's determinism QC on the re-test read 4.1's "from the line-list
extract" as favouring them, and the leak reader's three passes and solver rounds 2 and 3 all planned on them. The
definition closes that reading and names no method, so one delay pooled across the unit against each route's own is
still the analyst's choice, and it is the stump.

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
`golden/response_team_brief.pptx` (one slide) and `golden/pertussis_cases_by_lga.csv`. `checks.py`: 508 assertions
passed (after the 4.2 pin; the gate holds the prompt and eight files to d6944e3's bytes, the protocol to d6944e3's but
for 4.2, the quarterly table's three files and its golden to df378aa's, and the main-call fingerprint to
2e6c46341f359476). `verify.py` (standard library, openpyxl and pyarrow, no code shared with `golden.py`): OK, Griffith, rungs 0 to
3 Wagga Wagga, Griffith's 2 clusters (5 unit-wide), 50 ask A figures and both route speeds, each matched against the
goldens. Two consecutive
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
- Design-note vocabulary in PR-07 (12 terms), the bulletin (6), the run report (the scheduler job log, 4) and the notes (6): their own subject
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

**Rerun after the slide's cluster list was tied to the call (2026-10-11).** PR-07 5.1's slide sentence and the
prompt's slide sentence changed; `leak.py task181 --asof 2026-10-05`: REVIEW, the same twelve lines, no new one, each
answered as above. Two counts moved: block 4 of the submission now lists Griffith's two clusters, so the candidate
names fell from 9 to 6 (the line list and the rosters now name 4 of 6, not 7 of 9); and the swept design-note terms
swap "written" for "pattern" (from the pass 2 paragraph above, added after the last run), so the notes carry 6 terms,
not 7. The two reader passes read the earlier slide sentence; a reader re-read follows.

**Solver's-eye read, pass 3 (after the slide's cluster list was tied to the call).** Clean: question 1 PR-07 4.2 as the
rule the prompt cites, questions 2 to 4 none, every REVIEW line harmless. The rosters' arrival order ends with the two
Griffith schools (30 September and 1 October), which the reader called "at most a weak sign of recent activity": it is
the slow route showing (Griffith's first school cases were notified late), the order is honest, and it names no area or
cluster. Its plan files Wagga Wagga at rung 1, stable under every 14-day variant it tried, without a word on delay.

**Rerun after the 4.2 pin (2026-10-11).** Only PR-07's text changed (PINS); every other file under `target/` is
byte-identical. `leak.py task181 --asof 2026-10-05 --quiet`: REVIEW, the same twelve lines, no LEAK and no new line. The
design-note counts moved because the paragraphs the sweep draws its 25 terms from were rewritten (`complete`, `pooled`
and `eventual` are among the terms now), not because a document did. Each line:

- The bulletin's 100 and PR-07's 4 of 5 call words: as above; the pin names no area.
- PR-07, 11 terms (notifications, definition, notified, expected, health, griffith, specimen, received, excess,
  specimens, record): the d6944e3 protocol carries the same 11 against this vocabulary, so the pin adds none. Its words
  are the protocol's own, and it names no method (no nowcast, pooled, complete, eventual, fortnight or method). Harmless.
- The run report, 5 (health, specimen, received, record, and complete through the job's `COMPLETED` status), the
  bulletin, 6, and the notes, 5: byte-identical, each on its own subject. Harmless.
- Ranking artifacts (PR-07, the bulletin, the line list, the concordance, the rosters) and the parquet's 1,177 due
  dates: as above. Harmless.

The reader has not read the pack since the pin; a document under `target/` changed, so a re-read is due before the next
round.

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

- **Heart (`guard.py heart task181`, refreshed 2026-10-11 with task180 v3, task134 and task135 on file): BLOCK on one
  axis, `ban.strategy`.** maturity_censoring repeats task134, another author's forecasting build drawn the same day.
  - No other ban fired, and neither `test.same_puzzle` nor `test.same_driver` did.
  - The nearest drivers are task98 (0.08) and task91 (0.06); task134 is not among them.
- **Author override, 2026-10-11.** The card is registered with `--force` on the author's explicit instruction. The card's
  notes carry the reason; its `differentiation` carries one line each against task134 and task135. The label is kept
  honest: the stump is late arrival, which maturity_censoring names.
- **WARNs, one line each:**
  - `repeat.gate_g` (task135): task135's forecasting is a creek rating curve applied to daily flow; this one is a
    right-truncation nowcast inside an anomaly call.
  - `overuse.gate_g` (5 of the last 12): three of the five are the Forecasting lane's own builds (task132, task133,
    task135), where forecasting is the objective. task181 is the Anomaly lane's only one, and task182 draws away from it.
  - `repeat.decision` (task180 v3): both are this lane's builds, one area of ten against one signal of three; task182
    takes another answer type.
  - `repeat.opening` (task180 v3): task182's prompt opens on another move (prompt-voice.md section 3).

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
- **Personas.** Darryl Morales (immunisation coordinator) is named in no shipped file; he is off the card's people at
  ship. Colleen Brown signs the roster receipts in the rosters workbook and stays on the card.

## PRE-SHIP CHECK (client, eight points; answered at ship)

1. **Domain.** Surveillance epidemiology's own task: excess cases over a five-year seasonal baseline on a right-truncated
   epidemic curve, read by reporting route. The swap test breaks it: another field's nouns have no specimen-to-notification
   delay, no laboratory route and no truncated curve.
2. **Real data work, no plant.**
   - The notification-grain line list has to be built into 90-day episodes.
   - Receipt stamps are UTC across the daylight-saving change.
   - Split postcodes go by population share, under the 2024 case-definition revision.
   - Records link on MRN and on Medicare number plus IRN across three registers, and free-text school names have to be
     matched to rosters.

   Every record is correct.
3. **The flip is a method.** The flip is completing each area's fortnight from its own laboratory route's delay history.
   PR-07 4.2 defines the count (the fortnight's cases once all are notified) and is silent on delay, so the solver has
   to choose how to reach it from the extract. Nothing is planted to catch, and no field, code or stated rule decides it.
4. **Analyst test.** It holds. Cleaned and read correctly, 4.2's count completed on one delay pooled across the unit
   sends the team to Wagga Wagga (13.43 against 10.13). In-house solver rounds 2 and 3 stopped a rung lower, at the cases
   notified so far (7.6 against 5.6), a reading 4.2's definition now rules out in writing.
5. **The estimand is defined.** PR-07 4.2 to 4.3 define the quantity: cases (3.3) dated by first specimen (3.5), collected
   in the 14 days before the extract day, counted as they will stand once all their notifications have been received,
   set against the mean of the same dates in five complete years. Judge pass 2 found Griffith first under all 33 nowcast
   variants; the portal's determinism QC on the re-test read the earlier 4.2 as open between the on-file count and the
   eventual count, and 4.2 now states the eventual count.
6. **No decoy.** No memo, draft or briefing argues for Wagga Wagga. The two declared distractors carry no recommendation:
   the week-35 report counts notifications by week received, and the influenza file holds another condition's
   notifications.
7. **The method isn't recovered from certified figures.** No shipped figure is reproduced only by the right method. The
   week-35 report reconciles to the line list on received dates and pins nothing about the nowcast.
8. **A new lesson.** The lesson is that a right-truncated count has to be completed with each reporting route's own delay
   before it meets a complete baseline. The nearest earlier lessons teach censoring in durations or follow-up: task31's
   open approval clocks, and task134's immature recidivism follow-up with competing risks (same strategy family,
   differentiation on the card). Neither nowcasts an outbreak curve by route, and the nearest driver on file is 0.08.

## STOPPING RULE

Two rounds in which the solver nowcasts each route unprompted file this architecture as at-ceiling; a miss that lands
anywhere other than rungs 0 to 3 is read for a fork before any hardening.

## DETERMINISM RETURN (portal QC, Response 2, 2026-10-11)

**The finding** (`oviya-notes/portal-task181-determinism-response2.md`). Read literally, PR-07 4.1 to 4.3 count the
cases on the 07:00 extract, so the committed Griffith contradicts the files (Wagga Wagga 9 against Griffith and Snowy
Valleys 7, excess 7.6 against 5.6); even granting a completion, its variants (history, estimator) were left open.
Required: a PR-07 clause that makes the completion mandatory and single-valued. A second open axis: the CSV infant
columns rest on a birth-link judgement (the request's month-first date of birth, the mother's reissued card).

**The clause, designed and measured, not built.** PR-07 4.2a in the protocol's voice: "The count is completed laboratory
by laboratory before the excess is taken. Each laboratory's cases with first specimens in the 14 days are divided by
that laboratory's share of the cases a Monday extract holds: of its cases with first specimens in the 14 days before
each Monday from 1 September 2025 to 31 August 2026, as they now stand, the share whose first notification had been
received by 07:00 that Monday. A case belongs to the laboratory whose notification of it was received first." A share
taken on Monday extracts and not a per-day share, because Inland Pathology keys its routine results in a Wednesday batch
(91 of its 96 receipts, specimens August 2025 to July 2026): a per-day share then turns on how the empty days after the
Tuesday courier are read, and one urgent result can carry a weight of twenty.

**Measured** (scratch `oviya-notes/t181-det/proto/sweepA.py`, the shipped world on urgent-stream seeds 0 to 11). The
clause names Griffith on all 12 seeds at 2.87 to 4.44 times Wagga Wagga (Inland's share 0.140 to 0.217, the hospital
laboratory's about 0.82). Every variant names Griffith on every seed: Mondays over 6 months (2.55 to 4.18) or 3 years
(3.10 to 3.99), Mondays run to the extract (2.88 to 4.62), a case's laboratory by its first specimen (2.49 to 4.21), the
same 14 dates of 2023 to 2025 at 07:00 on 5 October (1.95 to 3.93, Inland's share from 6 cases), and each case over its
laboratory's per-day share (2.95 to 7.43). Only a share pooled across the laboratories names Wagga Wagga (1.33 on every
seed), and "laboratory by laboratory" rules it out.

**Infant columns.** Three readings to close before any rebuild: the infant's age from the request's date of birth or the
birth record's (6.1); the link when a case's medical record number is in neither file (6.2); the mother's register key
with or without the card's issue digit (6.3). Filed in PR-07, each is single-valued but becomes a filed rule the cracker
executes, so the ask layer would need new devices; closed by convergence (a second record that contradicts the
request's date, such as an earlier admission on the same medical record number), the device stays silent.

**Status.** With 4.2a filed, a solver who executes PR-07 lands Griffith (round 4 already completed by laboratory
unprompted), and on the portal's rubric a response that lands the call banks about 58 before it answers an ask (the
call and its dependent figures about 48, format about 10), so the build cannot pass the bar. No stump survives with the
method filed (Tried and rejected, 2026-10-11 entries). Nothing under `target/` or `golden/`, no
prompt and no write-up has changed; the author decides what comes next.

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
- Solver round 2 (architecture 2) missed the call at rung 1 but answered every ask, proxy 65.2; the slide's cluster list now follows the call (the team's school visits), so a wrong area carries a wrong list.
- **Portal round 1 (2026-10-11): ask A's devices as shipped did not bite.** The response filed all 15 graded CSV figures (42 points, 52 with the format points against the bar of 50), because each device was a stated rule or a step the hygiene battery runs: the 90-day episode, probable status, the 14-day admission link, the pregnancy window, the six-month boundary, split postcodes, eight-digit MRNs and the Medicare format. Revised on ask-path data alone (A1 to A3 under ASK SHEET). Not taken: any line-list device (the run report carries the line list's sha256, so one changed byte changes the job file the gate holds), and a `dTpa-IPV` antigen label (a value count shows it).
- Portal determinism QC (2026-10-11): the unpinned 4.2 left the observed-count reading defensible; pinned the estimand (the eventual count), not the method. Not taken: the QC's proposal to write the delay completion into 4.2, which would make the decisive step rule application and hand every solver Griffith.
- **Round 4 after the 4.2 pin (2026-10-11): landed, proxy 96.8.**
  - **What it did:** with 4.2 now defining the count, it completed each case by its own laboratory's historical delay
    ("Allowed for reporting delay using each lab's historical delay from first specimen to first receipt (cases before
    Jul 2026)"). That gave Griffith 60.6 against Wagga Wagga 9.3, and it never visited the pooled rung.
  - **Why the stump went:** before the pin, the stump rested on not completing the fortnight at all (rung 1), which
    was the portal's fork. Once the count is defined, the two laboratories' delays (median 12 days against 2) make the
    per-laboratory completion the obvious first move.
  - **Decision:** hardening loop on architecture 2.
- **Hardening loop 1 after round 4 (2026-10-11): a dated change in Inland Pathology's pertussis process, measured on
  prototypes and not built.** Pertussis PCR on Inland's regional bench before the change (daily van, a run every working
  day: median 2 days, 95th percentile 4 over the 12 months to July, the hospital's speed) and on the Sydney route as
  shipped after it, so each laboratory's 12-month history is the old fast one.
  - **Trap side:** on histories that end before the change, the per-laboratory completion names Wagga Wagga in every
    cell, but at 1.05 to 1.35 over the route-specific cells (round 4's per-case method on the 12 months to 30 June:
    Wagga Wagga 7.91 against Griffith 5.90). With both laboratories fast it cannot sit further apart than the notified
    excesses (7.6 against 5.6). A reporting triangle that runs to 4 October takes in the post-change cohorts and falls
    to 1.01 to 1.24.
  - **Answer side:** Inland Pathology notifies about 8 pertussis specimens a month (96 in the 12 months to July 2026).
    A change on 1 August leaves 18 post-change notifications on the extract, 5 of them in cohorts complete by then; on
    1 July, 25 and 12. The route cells name Griffith (1.30 to 15.9 at 1 August, 1.42 to 6.55 at 1 July), but the
    by-area cells have no post-change history to run on (undefined, and Leeton infinite on one row).
  - **Rescue tried:** ten designed early-September Inland cases (no school, so neither ask moves) lift the truncated
    route cells to 1.83 and leave the by-area cells undefined. They also put September cohorts into every triangle
    that runs to 4 October, which flips old-history cells to Griffith: one on round 4's history to 30 June, seven on
    the 12 months to the extract. The trap and the answer pull on the same few notifications.
  - **Literal rule (main, PR #39):** the window would need a filed criterion. "The experience that applies to the
    fortnight's own specimens" (or "that has held steady") closes the 12-month reading only by naming the step a
    clause-reading solver then runs, and the natural wording needs words `checks.py` bans (turnaround, completed). A
    back-test on the last closed fortnight cannot separate the candidates: 10 to 23 August, as at 07:00 on 24 August,
    holds one Griffith case (Inland, not yet on that extract) and 2 (1 August change) or 9 (1 July) post-change Inland
    notifications.
  - **Decision:** nothing under `target/` or `golden/`, no prompt and no write-up changed. Once the literal rule files
    which delay experience completes the fortnight, that choice is the route round 4 already ran, so the
    recommendation is a re-root rather than loops 2 and 3. The shipped pack also leaves pooled against per-route
    with no filed criterion; judge pass 3 closed that on the data alone, which the literal rule no longer accepts.
- **Determinism return, Response 2 (2026-10-11): the completion filed single-valued leaves no stump on the call.** The
  clause and its measurement are under DETERMINISM RETURN: filed by laboratory, every variant names Griffith on 12 of 12
  seeds, so the step that carried this architecture becomes a work order. Each new direction below was tried with the
  method filed and died.
  - **The Wednesday batch (measured, the nearest miss).** Inland Pathology keys routine results on Wednesdays, so at a
    Monday extract only the specimens on the Tuesday courier can be on file. With Griffith's two urgent window results
    made routine (scratch `sweepB.py`, `sweepB2.py`, seeds 0 to 11), every per-day completion names Wagga Wagga
    (weekday-pooled 1.14 to 1.31, weekday-stratified 1.15 to 1.38; Griffith completed to 7.4 to 8.5, because a per-day
    completion has nothing to inflate on the empty days), while the fortnight's share names Griffith (calendar 1.72 to
    2.47, Monday extracts 1.90 to 2.95; Griffith 18 to 30, truth 41). It lives only while the estimator is open: filed per
    day, the protocol's own method gives the wrong area (a decoy); filed per fortnight, it is a work order; left open, it
    is the variant fork this return rejected. Nor is the per-day answer wrong in itself: an urgent request (7 per cent of
    Inland PCRs) is keyed within days, so a per-day completion is unbiased and fails only on the draw where none of the
    35 Griffith specimens that missed the Tuesday courier went urgent (0.93 to the 35th, about 1 in 13), which the data
    would have to be cut to show; on the shipped draw (2 urgent) every per-day completion names Griffith. Round 4 also
    ran a per-day and a fortnight completion side by side, so a solver sees the threefold disagreement.
  - **A filed back-test choosing the estimator (measured).** Run at each Monday from March to August 2026 (world B,
    seeds 0, 3, 7, `backtestB.py`): mean absolute miss 0.48 to 0.53 for per-day, fortnight and Monday-extract alike (area
    fortnights of 0 to 2 cases cannot separate them); largest miss per-day 16.0 to 19.3 (one urgent result weighted
    about twenty), fortnight 5.75 to 6.27, Monday extract 5.86 to 7.31. A largest-miss criterion drops per-day and both
    survivors name Griffith, so the filed criterion hands over the call (a control bench); the organ is task446's, and
    architecture 3 measured that closed records this thin do not pin a method.
  - **Right truncation inside the delay history.** With the history ending before the 14 days, its unfinished cohorts
    are 15 days old or more: running the Mondays to the extract moves Inland's share by under 0.01 (0.140 to 0.217
    against 0.132 to 0.212), and solvers take complete cohorts by reflex (round 4).
  - **Case-level against notification-level delays (the unit).** A case's laboratory by first specimen instead of first
    receipt moves the margin under 10 per cent on every seed; 7 per cent of non-infant cases have a second laboratory, and
    round 4 measured first specimen to first receipt unprompted.
  - **The expected count as the decisive step.** 4.3 files the five-year mean (rule application); worded as the area's
    usual count, mean, median and leaving out 2024 all stand (a fork); and expected counts of 0.2 to 1.4 cannot move a
    completed excess of 20 or more.
  - **A second truncation or a missing route.** A case re-dated out of the 14 days once a slower earlier specimen is
    keyed is rare and has no single completion; a laboratory with nothing on file for an area completes to zero under any
    per-laboratory clause; a window on onset dates needs specimens not yet collected (a forecast, a fork).
  - **The ratio against the difference.** Setting the notified count against prior years as they stood at the same hour
    (`samelag.py`) keeps the ratio (Griffith 11.7 against Wagga Wagga 7.5) but shrinks the difference by the completeness
    (Griffith 6.4 against Wagga Wagga 7.8); with the completion mandatory no solver takes that route, and filing it would
    make the protocol the decoy.
  - **Redesigns that keep "which area".** Excess per resident, the excess over the district-wide rise, growth, infant
    exposure, school clusters, a reliability hold on the completion, test positivity: each is a filed formula (rule
    application) or an open model (a fork). Once the completion is filed, PR-07's quantity is a function of the records
    and its rules, and none of these adds an estimand the data alone settles.

- **Architecture 3 (designed on its own branch and spent 2026-10-11; its record folded in here when the repo moved to one branch).** Its design note is not kept; what died, verbatim:
  - **Draws weighed for architecture 3 and not taken.**
    - Electricity theft against technical losses that scale with the square of the load: task180 v1's revenue-protection
      territory, task229's smart-meter surface, and a strong solver squares the half-hourly load by reflex.
    - The variance of a month-to-month change between overlapping survey panels: the same insight as task229 (an error built
      on the wrong independence), in the other direction.
    - A registry outlier on cumulative incidence against one minus Kaplan-Meier: spent by task134 and task133 (competing
      exits).
    - Overdispersed funnel limits for provider outliers: architecture 2's own rejected fork, and the limits widen on reflex
      once a criterion files their coverage.
    - Fabricated interviews found as inliers (too little variance): the only literal pin is a closed reinterview corpus
      that selects the indicator, which is a corpus-fit rule.
    - Warranty returns read against an age-specific failure curve (a sales surge's echo against a defect): age-specific
      rates are the warranty analyst's first move.
    - The seed's own zone-D vibration split by operating point: the same insight as task180 v2 (a monitored signal carried in
      from ordinary operation, attributed to its source).
    - A self-exciting fit with one background rate over five years as the golden's method: it misses the recent rise in
      Heathfold's background and its forward figures depend on the kernel; the golden projects each estate's recent
      background instead, and the constant-background fit sits in the grid as a wrong cell.
    - The same draw labelled time and A: collides with ten older builds, task33's forward-yield signal pick among them.
  - **Build, stage 3 (2026-10-11): CS-04 2.3's back-test does not select the background projection on honest data, so
    the closure in LADDER, GRID and CLOSURE axis 22 cannot be built.** Prototyped before any pack was cut (scratch
    `oviya-notes/t181-a3/proto2.py`, `sweep2.py`, `backtest_feasibility.log`): the eight Appendix B quarters (29 July 2024
    to 26 July 2026, cut at the end of the Sunday 15 days before each), twelve estates at the planned usual counts and
    seasonal ratios, Poisson background, four persistent steps of 40 to 60 per cent in the closed period, 25 to 30 runs
    of 4 to 11 over the quarters and their bases at the same rate before, true run labels standing in for the proximity
    separation, total absolute miss over the 96 estate-quarters. Over 300 seeds the best count projection misses
    0.85 times the golden cell's total at the median and 1.03 at most (25 per cent better is required; no seed reaches
    1.0 by a margin), the usual winter itself (every estate's excess zero) wins the whole back-test in 81 per cent of
    seeds and shrinkage toward it at 0.75 in most of the rest, and the golden cell (13 weeks, seasonal ratio of all
    break-ins) is the best background cell in 8 per cent (flat 13 weeks or a background-only ratio win). Twelve steps
    of 60 to 150 per cent and larger, more frequent runs (6 to 14, 30 to 36 in the closed period) lift the best count
    cell's ratio to the golden cell to 1.22 at most over 400 seeds and never make the golden cell the background
    minimum. Why: a 13-week window holds about 10 break-ins, so a 13-week projection carries Poisson noise as large as
    anything the count projections lose to runs; runs in the target quarters are a miss every projection shares; and the
    five-winter usual, which needs no recent data, is the most accurate 13-week forecast in this world. Read literally,
    2.3 would then select the usual (no estate exceeds it), a fork as well as a lost stump. A seed search cannot find the
    planned margins and a smoother background would be the planted fix the brief rules out, so nothing was cut; the
    closure goes back to a designer (the criterion, the window, or the volume it runs on).
  - **Design pass 2, stage 3 (2026-10-11): no criterion, window or volume closes CS-04 2.3 on honest data; architecture
    3 is spent.** Prototyped across seeds before any design was written (scratch `oviya-notes/t181-a3/proto3.py` to
    `proto14.py` and their logs). (1) Accuracy criteria, total absolute or squared miss: with shrinkage toward the usual and
    trailing windows open to both families (the builder's run gave background cells none) the usual rarely wins outright
    (2 per cent of seeds in the base world), but in all 96 configurations swept (10 to 35 background break-ins an
    estate-quarter, estate levels changing 0.6 to 1.5 times a year with log SD 0.30 to 0.45, runs started by 3 to 8 per
    cent of break-ins with 3 to 10 or 8 to 19 follow-ons) the best count projection sits at 0.95 to 1.11 times the best
    background projection at the median and at most 1.04 at the 10th percentile, because shrinking a count projection
    toward the usual sheds its runs without changing its estate order, and the target quarter's noise is a floor both
    families share. Sprees of 15 to 30 under absolute loss reach 1.10; 100 break-ins an estate-quarter (no estate of this
    size) gives 1.00, since runs started by break-ins scale with the background and average out. Confining the projection
    to the 13 weeks before the cut opens the count gap to 1.14 but leaves the usual (0.98) and count shrinkage (0.95) ahead
    of every 13-week background cell, and count shrinkage stays within 1.11 at the median (10th percentile 0.97 to 1.0)
    even when estate levels jump by a factor of 1.8 a year. (2) Decision-scored criteria (the estate each projection would
    have funded, or its top three, recorded excess totalled): shrinkage cannot help a count projection and the usual makes
    no call, but the background family wins only 59 to 88 per cent of seeds (top three, 76 to 95) over 8 or 20 quarters.
    (3) Rank criteria, the correlation between projected and recorded excess over the usual (pooled over estates and
    quarters, or by rank within each quarter), over 20 quarters (log from April 2016), the projection confined to the 13
    weeks to the cut, homes placed in space at 30 to 45 dwellings a hectare and runs separated by proximity rules rather
    than true labels: the families separate (pooled, at least 1.10 in 87 per cent of 90 seeds, median 1.27; the usual has
    no spread to score and constant shrinkage leaves the score unchanged), but nothing pins the method inside the
    background family. At estate densities a 200 m and 14 day rule links 45 to 50 per cent of background break-ins (11 of
    Heathfold's 17 in a median world) and names another estate while scoring within 6 per cent of the tight rules' best
    in 44 to 52 per cent of seeds (ahead of them at the 90th percentile); the weekly-median background form ranks on
    medians of 0 to 2 and topped the per-quarter rank criterion in that median world, for Rookcliffe. With each live
    autumn sized to its seed's own usual counts, the closure (families at least 1.10 apart, the criterion's best
    background cell on Heathfold, every cell on another estate at least 9 per cent behind) held in 2 of 12 typical worlds.
    The planned empty band cannot exist on an honest background either: a 200 m radius covers a fifth of a 2,400-home
    estate and half its background break-ins have a chance neighbour within 200 m and 14 days, so the band was a planted
    background, and without it the run set depends on a scale no filed sentence may name. Root cause: about 10 break-ins
    per estate per 13 weeks, so every choice made after the runs are separated (window, seasonal treatment, robust form,
    proximity scale) moves the call by more than any closed record of this size discriminates. Filing the scale names the
    step, an under-dispersed background is planted, and at volumes where noise stops deciding (35 or more a quarter,
    estates of about 6,000 homes at 25 per 1,000) runs started by break-ins average out and the families stop
    disagreeing (1.02). Retiring task181 is the author's decision.
