# task445 design note (architecture 2, the Ellesmoor heat resilience grants)

Architecture 1 (the 13F holdings carry, quantitative finance) is spent and in the card's lineage; its measured
deaths are in the last section. It died on the determinism block (a literal reading of its governing section counted
only the reports on file) and on the survivor anatomy (its decisive basis was a filed criterion's selection). This
draw is held to two tests before anything else: the estimand, members not yet observed included, is filed so its
literal execution is the golden, and the easy route is the field's own completion of an unfinished count, which every
closed summer in the pack validates.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task445.json`, architecture v2, first registered 2026-10-31T22:45:01Z
  after `guard.py recent`, `coverage` and `mechanisms --objective etl`, and redrawn on its axes the same evening when
  task468 v5, registered eight minutes earlier on the same pairing, shape, forum and role, landed on main (the redraw
  is in the last section). `check` on the card as filed: WARN only (the objective's share of the last twelve builds,
  which the slot fixes; Gate G `etl_conformance` and the question form `which` against task468, answered in the
  pre-ship check). The bans against the last three builds (task172 v2, task125 v4, task468 v5: funder, executive and
  panel forums; meeting and budget events; university, local-government and government-agency organisations; the
  other, composition and population strategies; patterns G4, G5 and G11; shapes 01 and 05 against the last two) are
  clear, and task107 v3-etl, task181 and task485 are differentiated on the card.
- **Pairing:** General Statistics & Data Science, task type data-integration-record-linkage-entity-resolution,
  objective Data Extraction & Conformation: each place's residents' deaths from 1 June to 31 August 2026, which no
  one source holds (the register lacks the deaths a coroner holds for inquest, the medical examiner offices' logs lack
  residents who died outside their areas), integrated from the registrations and the two offices' referral logs, which
  share no key, decide which places of an integrated care board get its 2027 heat resilience grants.
- **Shape:** 10, a scorecard against a threshold: each place's deaths, its filed expected deaths, its excess and the
  fund's line of a tenth over the expected; the asks' place-by-period and coroner-area grids supply the rest of the
  criteria.
- **Strategy:** `maturity_censoring`; Gate G `etl_conformance`; gap time then population; generators G3 (the register
  records registrations and the fund counts deaths, so the record lags the event by the coroner's hold), G12 (a death
  missing from the register is an absence of record, not a record that no death occurred), G13 (the extract's horizon
  is not the summer's).
- **Data-native sentence:** in the July heat wave, older people living alone in Ashwold's terraces died at home and
  were found days later, the post-mortem could not give a cause, and a death whose cause a post-mortem cannot give
  waits for an inquest before it is registered, so in October Ashwold's summer is short on the register by exactly
  the deaths the medical examiners referred to the coroner and the coroner still holds.
- **World:** NHS Ellesmoor Integrated Care Board, a fictional board in the north of England serving six local
  authority places (Hollinsgate, the city; Ashwold; Brinmoor; Calderholt; Moorbridge; Thornley Vale); two coroner
  areas (North Ellesmoor: Hollinsgate, Ashwold, Thornley Vale; South Ellesmoor: Brinmoor, Calderholt, Moorbridge);
  two medical examiner offices hosted by the acute trusts, each with its own log. People from `guard.py names --geo uk
  --seed 445` (Lynn Davison and the Khan surname set aside, task468 v5 carrying Davison and Khan): Caroline Porter
  (Director of Population Health, who takes the grants to the board and asks for the scorecard), Jason Leach (Head of
  Population Health Intelligence, who owns the mortality extracts), Graeme Gould (Lead Medical Examiner, North
  Ellesmoor), Jayne Jackson (Medical Examiner Office Manager, South Ellesmoor).
- **Forum and forcing event:** the board of the integrated care board (board_of_directors) approves the 2027 heat
  resilience grants at its meeting of 26 November 2026, so that the designated places can commission cool spaces,
  check-in calls and home adaptations before summer 2027 (season_or_peak); the organisation is an NHS integrated care
  board (hospital_or_health_provider).
- **Why retrospective:** the fund pays for summer 2027 on summer 2026's toll, a window closed on 31 August whose
  count is not finished at the October extract; the forward element is the count's completion (the deaths not yet on
  the register), never a forecast of 2027.
- **Sources:** synthetic throughout, modelled on how English death registration works (registration within five
  days, after the medical examiner's scrutiny or the coroner's decision, and only after an inquest concludes where
  one is opened), on the medical examiner system in force from September 2024, and on how integrated care boards
  receive the primary care mortality extract; no real dataset, person or organisation.

## Default path

The pipeline a competent analyst builds from the prompt, the terms and the register, with the field's own
completion of a provisional series by date of occurrence in it:

1. Read `ellesmoor_death_registrations_2021-2026.csv` (81,590 rows) in both date formats, keep one row per entry
   (district and entry number, version 1), and take the residents' deaths with a date of death from 1 June to 31 August
   2026 by `usual_residence_code`: 831, 594, 330, 388, 575 and 350 for Hollinsgate, Ashwold, Thornley Vale, Brinmoor,
   Calderholt and Moorbridge.
2. The terms count every death whether or not it is registered, so complete the count for deaths not yet registered:
   for each summer from 2021 to 2025, the share of its deaths that were on the register by 9 October of that year,
   against the entries made by the extract (94.9 per cent pooled; 94.4 to 95.3 by place), and divide each place's
   registered count by it. Validate it on the earlier summers: carried from the summers before each, it reproduces the
   2023, 2024 and 2025 summers' counts within 2.0 per cent at every place.
3. Read Table 1 from the terms PDF, take each place's excess over its expected deaths as a percentage and qualify the
   places at 10 per cent or more: Hollinsgate 5.8, Ashwold 6.3, Thornley Vale 14.4, Brinmoor 6.8, Calderholt 14.8,
   Moorbridge 6.9.

- **Ends on:** Thornley Vale and Calderholt designated, Ashwold's excess at 6.3 per cent under the line.
- **Golden:** Ashwold, Thornley Vale and Calderholt designated, Ashwold's excess at 13.1 per cent over the line.

## Stump sentence

A competent analyst completes each place's registered summer deaths with the earlier summers' share registered by 9
October and designates Thornley Vale and Calderholt, leaving Ashwold at 6.3 per cent; the step that lands it there is
treating this summer's unregistered deaths as the usual twentieth, when the July heat wave's deaths of Ashwold's
residents found at home are held by the coroner for inquest and named one by one in the medical examiner offices'
logs (72 of its 666 summer deaths), which put Ashwold 13.1 per cent over its expected 589.

## Three rules

- **Task type:** data-integration-record-linkage-entity-resolution (General Statistics & Data Science), which serves
  Data Extraction & Conformation: the deaths that decide the call sit across three systems that share no key.
- **Domain test:** the deciding quantity is each place's deaths by date of occurrence, which no one source holds (the
  register lacks the deaths the coroner holds for inquest, the offices' logs lack the residents who died outside their
  areas), so it is built by integrating the sources on the person and the date of death; the field the call rests on is
  making one population out of systems that each hold part of it.
- **Swap:** put admissions or claims in for deaths and the task no longer reads the same: what keeps a death off the
  register is an inquest that has not concluded, and the logs that name the held deaths exist because every death in
  England now passes a medical examiner; the swap loses both.
- **Layer 1:** the register's two date formats and district codes either side of the 3 April 2023 system change; a
  correction as a second version of its entry; residents registered in Kexley; the north log's single SURNAME,
  Forenames field and Excel dates against the south export's nested JSON, family and given names and UTC stamps;
  postcodes placed through a lookup that keeps terminated postcodes; a returned referral reopened as a new case.
- **Layer 2:** completing a provisional series is the field's own step, and the data's real structure decides how: the
  earlier summers' completeness is right only while the coroner holds the usual twentieth, and this summer the heat
  wave's deaths at home were held for inquest, so the completion that every closed summer validates misplaces the
  place whose deaths they were.
- **Decisive step:** adding to each place's registered summer deaths the residents' deaths that the offices' logs hold
  and the register does not, matched on surname, forenames, date of birth and date of death, instead of scaling the
  register by the earlier summers' completeness.
- **Not semantics:** every field reads the same on every route; the terms say in one sentence that unregistered deaths
  count, and an analyst who reads it correctly still has to decide how to count them, where the completion that every
  earlier summer validates is the wrong way.
- **Not rule application:** the terms state what is counted (the window, the residence, the deaths not yet registered,
  each death once, the records at the close of 9 October, Table 1, the line) and never how the unregistered deaths are
  found; executing every stated rule on the completed register files Thornley Vale and Calderholt.
- **Analyst test:** a strong analyst who reads every field and the terms correctly counts each place's registered
  summer deaths and completes them with the earlier summers' share registered by 9 October (94.9 per cent), which
  reproduces every earlier summer within 2.0 per cent, and designates Thornley Vale and Calderholt with Ashwold at 6.3
  per cent; Ashwold's 72 deaths not yet registered are 11 per cent of its summer, where the completion assumes about 5.
- **Estimand:** each place's residents' deaths by date of death from 1 June to 31 August 2026, every death that
  occurred whether registered by 9 October or not and each counted once, from the mortality records held at the close
  of 9 October 2026; the excess over Table 1's expected deaths as a percentage; a place qualifies at 10 per cent or more.
- **No decoy:** nothing is planted: every register entry and log case is a correct record, Table 1 and the earlier
  summers' completeness are true statements, and no memo, briefing or figure in the pack argues for a set.
- **No certified replay:** the pack carries no provisional or published summer count, no completion factor and no
  ranking of the places; the completeness is computed by the solver from the register's own history, and nothing
  certified ties only under the completed register.
- **Lesson:** architecture 1 died on a literal reading that counted only what was on file; here the terms file the
  deaths not yet registered as part of the population, so the literal reading counts them, and the only open question is
  how, which the logs answer by name.

## Survivor anatomy

- **Actor:** a death the register lacks has no row on it at all, and no column in any file marks a summer death as
  unregistered; the property is a relation between files (a log's resident death with no entry under the same person
  and date of death).
- **Link:** the logs and the register share no key; the join is on surname, forenames, date of birth and date of death
  across three layouts (one name field in the north log, two in the south export, capitals on the register), which no
  key column, shared code or clause invites.
- **Reflex:** the field's named method for a provisional series by date of occurrence, completion by the earlier
  periods' share registered by the same point, sits at rung 1 and files Thornley Vale and Calderholt.
- **Back-test:** the textbook route validates: each earlier summer's completeness carried from the summers before it
  reproduces the 2023 to 2025 summers within 2.0 per cent at every place, and pooled, by place, by month of death or over
  the last three summers it files the same two places.
- **Second use:** the logs are in the pack for the medical examiner offices' quarterly activity (the second ask), which
  the board oversees as the offices' host; deleting the decisive step, the pack still carries both logs.
- **Shock:** Ashwold's completed excess (6.3 per cent) sits among the places that do not qualify (Moorbridge 6.9,
  Brinmoor 6.8, Hollinsgate 5.8) and reads as an ordinary hot summer; the golden set is not an interval of any sort
  (Ashwold is fifth of six on the completed register and on the register as extracted; asserted on four sorts).
- **Pins:** the terms file the WHAT in the board's own genre (the window, the usual address, the deaths not yet
  registered, each death once, the records at the close of 9 October 2026, Table 1, the line of 10 per cent); no
  sentence names the logs, the completion, the match or the coroner.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the register as extracted | the terms' "whether or not it has been registered" sends the solver past it | - | - | - | - | - | - | readable |
| R1 the earlier summers' completeness (pooled, by place, by month, last three) | - | - | the field's method for a provisional series | - | - | one ratio | - | readable |
| R2 every log death added beside the register | - | - | - | - | the battery finds the doubled deaths (every place over 100 per cent) | - | - | readable |
| R3 (decisive) the logs' residents' summer deaths that the register lacks, matched on surname, forenames, birth date and death date | no sentence names the logs, the coroner or the match; "the mortality records held" names a set the completion also reads | no column marks a death unregistered; the logs and the register share no key | the reflex is R1 | no count of 2026 summer deaths, published or provisional, is in the pack | no duplicate, re-sent batch or row after a close carries it | a four-field match across three layouts | the logs carry the second ask | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the place of a death | the usual address (register `usual_residence_code`; logs' usual postcode through the lookup, terminated postcodes included) | the place of death or the registration district | moves deaths between places | terms section 4, "the place of the deceased person's usual address" |
| SF2 | the window | date of death 1 June to 31 August 2026 inclusive | date of registration | not a reading: registration dates run to October | terms sections 3 and 4, "by the date of death" |
| SF3 | deaths not yet registered | counted | left out (R0) | no place qualifies | terms section 4, "whether or not it has been registered by the date of the count" |
| SF4 | a correction or a reopened case | one death | a second death | same call (corrections and reopened cases add under 1 per cent and move no place across the line) | terms section 4, "each death is counted once"; a version 2 row repeats its entry's district and number |
| SF5 | the records the count reads | the register and both offices' logs at the close of 9 October 2026 | the register alone | the R1 call | terms section 4, "the mortality records held by the population health intelligence team at the close of 9 October 2026"; the pack's three mortality extracts all run to the close of 9 October 2026 |
| SF6 | the excess | deaths less expected, as a percentage of expected | deaths over expected as a ratio | same call | terms section 3 |
| SF7 | the line | 10 per cent or more qualifies | strictly more than 10 | same call (no place within 2.4 points of the line) | terms section 3, "by 10 per cent or more" |
| SF8 | the expected deaths | Table 1 as filed | recomputed from the register | not guaranteed | terms section 5, "Table 1 is fixed for this allocation and is not recalculated" |
| SF9 | non-residents in the logs | outside the count | counted in the place of death | moves Hollinsgate and Calderholt up | their usual postcodes are outside the lookup of the six places |
| SF10 | residents who died outside Ellesmoor | counted (registered in Kexley) | left out | same call | terms section 4, the usual address; the Kexley rows carry Ellesmoor residence codes |
| SF11 | an office's deaths scrutinised in a quarter | distinct deaths, in the quarter the office completed its scrutiny | cases | the ask's figures | the asking sentence says deaths; a reopened case falls in its referral's quarter |
| SF12 | the quarters of 2025-26 | April to June 2025 through January to March 2026 | calendar 2025 | the ask's figures | the NHS year named in the asking sentence |
| SF13 | deaths with a medical certificate in a quarter of 2025 | certification beginning "Medical certificate", by date of death | by date of registration | the ask's figures | the asking sentence, "deaths ... in each quarter of 2025"; the register's certification values |
| SF14 | registered no more than five days after the date of death | the entry's registration date (version 1) at most five days after the date of death | the latest version's date | the ask's figures | a death is registered once: version 1 is its registration, and a version 2 row records the correction's own registration, weeks or months after the entry it repeats |
| SF15 | the place for the registration shares | the usual address's place as the entry now stands (a correction carries the corrected fields) | version 1's address, or the registration district | the ask's figures | the asking sentence, "its residents' deaths"; a version 2 row repeats its entry with the fields corrected |
| SF16 | the south export's UTC stamps | read as local dates | read as UTC dates | same call (every completion falls in the working day) | the stamps' own Z suffix |

## Ladder

Each rung a complete pipeline; excess over Table 1 in per cent for Hollinsgate, Ashwold, Thornley Vale, Brinmoor,
Calderholt and Moorbridge, and the set it files.

| Rung | Construction | Excess by place | Set |
|---|---|---|---|
| R0 | registered entries only | 0.4, 0.8, 8.6, 1.3, 8.9, 1.4 | none |
| R1 | completed by the earlier summers' share registered by 9 October, pooled (94.9 per cent) | 5.8, 6.3, 14.4, 6.8, 14.8, 6.9 | Thornley Vale, Calderholt |
| R1b | the same by place, by month of death, or over 2023 to 2025 only | Ashwold 6.1 to 6.8, every other place on the same side | Thornley Vale, Calderholt |
| R2 | every log death added beside the register, unmatched | 104.1 to 117.8 | all six |
| R3 | the logs' inquest and awaiting rows added, unmatched | 7.7, 13.1, 14.1, 7.3, 12.7, 6.4 | Ashwold, Thornley Vale, Calderholt |
| Golden | the register plus the logs' residents' summer deaths it lacks, matched on surname, forenames, birth date and death date | 7.6, 13.1, 13.5, 6.8, 12.7, 5.5 | Ashwold, Thornley Vale, Calderholt |

R3 lands the call by the decisive insight without the match; it is a route to the golden, not a rung below it, and the
asks carry the pair. The golden's deaths: 891, 666, 345, 409, 595 and 364 (3,270 against 2,977 expected); not yet
registered 60, 72, 15, 21, 20 and 14 (202).

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | residents' deaths by usual address, registered or not: terms section 4, asserted against the clean truth |
| 2 | Unit of account | a death, once: terms section 4; corrections and reopened cases collapse (SF4) |
| 3 | Attribution window | date of death 1 June to 31 August 2026 (SF2); the logs and the register carry the same date for every matched death |
| 4 | As-of dating | the records at the close of 9 October 2026 (SF5) |
| 5 | Version basis | version 1 of each entry for the call, where no correction in the window changes a date of death or residence; each 2025 entry as it now stands for the third ask (SF14, SF15) |
| 6 | Denominator | Table 1 as filed (SF8) |
| 7 | Weighting | none: a count per place |
| 8 | Window length | the summer is filed; the completion's history length is a rung choice and every length files the R1 set |
| 9 | Boundary inclusivity | 10 per cent or more (SF7); no place within 2.4 points |
| 10 | Rounding path | the excess to one decimal at the close; no place near a half |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | the decisive axis: the deaths not yet registered are in the population (SF3) and named in the logs |
| 13 | Order of operations | match then place; placing first changes nothing (the place comes from the log's own postcode) |
| 14 | Row order | asserted: the counts are set operations |
| 15 | Duplicate resolution | one death per person and date of death across the logs; a reopened case is the same death |
| 16 | Identity normalisation | case-folded surname and forenames, the north log's field split at its comma; asserted exact on every summer row |
| 17 | Netting against gross | none |
| 18 | Dimensional units | counts and percentages only |
| 19 | Code and status semantics | certification and coroner decision values are written out in full in the files; never the stump |
| 20 | Integerisation | none on the call; the grant follows the designation |
| 21 | Clause scope | section 4's counting rules govern the call only; the asks carry their own sentence |
| 22 | Forward window contents | none: the window closed on 31 August; its completion is in the logs |

## Literal reader

A literal reader of the terms counts every death of each place's residents with a date of death in the window, takes
section 4's "whether or not it has been registered" as part of the population, reads the count from the mortality
records the team held at the close of 9 October (the register and both offices' logs, each extracted to that close),
counts each death once and compares each place with Table 1: that execution is the golden, because the logs name the
deaths the register lacks. A completion factor is an estimate of the same deaths, which the records do not need.

## Oracles

- The clean truth: `checks.py` asserts the golden equals the generator's count of every resident death in the window at
  every place and month, and the analyst test (the earlier summers' completeness carried onto the clean truth's
  registered deaths) files Thornley Vale and Calderholt.
- The independent verifier (`verify.py`, its own readers) recomputes the counts, the set and both asks.
- No oracle ships: nothing in the pack ties only under the golden.

## Ask sheet

**Ask B, the offices' deaths scrutinised by quarter of 2025-26** (8 figures). H18: the board hosts both offices and its
quality committee takes their activity beside the grants paper. Primary device D1, one death under two case keys: when
the coroner sends a referral back (Form 100A), each office's system reopens the death as a new case with its own
reference, and in about a quarter of them the reopened case carries the registrar's corrected forename, so only the
coroner's reference ties it to the referral. Hazard: advice-only consultations carry a coroner's reference on a single
case (the benign twin: a reference alone marks no reopened case); the south export's UTC stamps (SF16, same call).
Path: the north workbook (11 columns) and the south JSON (14 fields). Stops (North April to June): cases 2,116; merged
on the person 1,940; golden 1,924. Pin test: the sentence pins deaths, the office and the NHS quarter; the device sits
in which records are one event, which no pin names. Realism: a reopened case is how a case system records a returned
referral.

**Ask C, registration within five days by place and quarter of 2025** (24 figures). H18: the registration lag is what
makes the board's provisional mortality counts short, and the panel reads it beside the scorecard. Primary device D2,
the one reflex-repair-wrong device the build carries: a correction is a second version of its entry whose
`date_of_registration` is the correction's date, so the battery's latest-version rule reads the correction's date as
the registration. Second device, D2 against D7 with its own figure block: in the districts' March 2026 review, care
home residents of Thornley Vale and Moorbridge whom the care home's manager had registered in 2025 at the family's
address in Hollinsgate or Calderholt were corrected to the care home, so the entry as it now stands takes its address
from version 2 and its registration date from version 1; reading version 1 for every field files those deaths in the
wrong place and moves the 16 cells of the four places. Path: the register (version, the two dates, certification,
residence code, postcode). Stops (Thornley Vale, January to March): latest version 55.8; version 1 for every field
61.1; golden 63.9. Pin test: the sentence pins the population (residents' deaths with a medical certificate), the
quarter of death and the boundary (no more than five days after); both devices sit in which version carries which
field, which the rows themselves show and the battery overrides. Realism: correction versions and a district
review of addresses are how a register extract carries amendments.

Separation: no reopened case with a corrected spelling has a date of death in or within 40 days after the window, the
address review touches 2025's deaths only, and no correction in the window changes a date of death or residence (each
asserted), so the main population carries no device row. Hazard table: the version rules move the third ask only;
reopened cases move the second ask only and are neutral on the call (both cases of a returned summer death match the
same entry). Referee: none needed.

| Ask | Cracker's route | Cracker keeps | Verdict |
|---|---|---|---|
| B North, four quarters | cases counted per quarter | 0 of 4 (over by 192 to 256) | miss |
| B South, four quarters | cases counted per quarter | 0 of 4 (over by 152 to 186) | miss |
| C, six places by four quarters | latest version per entry | 0 of 24 (0.6 to 12.1 points under) | miss |
| Full includer (stress row): cases merged on the person, version 1 for every field | the same pack | 8 of 32 (Ask B over by 14 to 25 in every quarter; Ask C off in the 16 cells of the four places the review moved) | miss |

- **Mirror leakage:** 0.0 per cent of the ask weight (the mirror handles the asks as the cracker does).
- **Pair ceiling:** 28.5 (cracker 45.0 on the call, mirror 12.0 off it; the full includer on the call 58.8).
- **Measured by:** generator/ceiling.py on the cut pack.

## Leak sweep

`leak.py --asof 2026-10-14` on the final cut (target.zip b103f21f): REVIEW, 0 LEAK, three lines, all on the fund's
terms, each ruled here.

- Sweep 3, Table 1's 589 (Ashwold's expected deaths): harmless. It is a filed input every response must read; the
  answer is the count against it, which no file states.
- Sweep 3, the terms carry most words of the committed call: harmless. The terms name every place and both kinds of
  grant because they are the allocation's own paper; they name no place as qualifying and rank nothing.
- Sweep 4, seven stump terms in the terms (register, summers, October, records, change): harmless. They are the WHAT
  (deaths counted whether or not registered, from the records held at the close of 9 October; Table 1 from the
  summers of 2021 to 2025, adjusted for population change); no sentence names a log, the coroner, an inquest, a
  completion or a match.
- An earlier cut carried a data-notes PDF describing every field of the three mortality extracts; sweep 12 called it
  a describing file (LEAK). It is gone, and every fork it closed is closed by the terms or by the rows themselves (the
  fork table's last column).

## Pre-ship check

- **The three rules:** answered in `## Three rules`; the decisive step is the completion's source, an analytical
  choice the literal estimand forces and the textbook route gets wrong.
- **Guard:** `check` and `heart` WARN on the final card, no BLOCK. overuse.objective is the slot's own objective (task445
  is numbered in the ETL range). repeat.gate_g (etl_conformance against task468 v5): the mechanisms differ (task468 v5
  rebuilds a ward price index across a boundary review; this build completes a provisional count from a second body's
  log). repeat.question_form (where against task125 v4): "which" would have repeated task468 v5 and sits over the
  corpus quota; "where" is the board's own question about where the grants go. Surface: exit 0; five pairs promoted
  for the author's adjudicated read on surface similarity at the corpus's top percentile (task146, task462, task447,
  task118, task273, each at about 0.10), task462 and task273 also sharing the decision type; none shares the driver,
  and the pack carries no other build's persona.
- **Input gates:** 10 files in four formats (csv, json, pdf, xlsx); the register extract has 81,590 rows; four context
  files named as distractors in `metadata.json` (population estimates, temperatures, heat-health alerts, the care home
  list), none read by the golden.
- **Free gates on the final cut:** 103,082 generator checks green; the verifier recomputes the counts, the set and both
  asks; two builds byte-identical; `figures_check.py` 103 figures, none absent; `precut.py` 61 checks with no FAIL or
  WARN; `voice-check.py` PASS; pair ceiling 28.5 by `generator/ceiling.py`.
- **Open for stage 4:** the leak reader's solver's-eye read (brief in the scratchpad) and the determinism judge, run
  together from the main thread.

## Tried and rejected

- Seed ET02 as written (amendment-type supersession and filing-date value units deciding the flag):
  rule application and data semantics as the decisive step, banned; kept as Layer 1 on the asks.
- A top-holder ask with every manager in contention, including index sponsors still to file: the top
  holder would be unknowable at the extract; the large early complexes are made the top holders and every
  pending manager's carried value is asserted under 80 per cent of the top.
- The issuer-level completion factor as a rigorous variant: once the September window carried one-off
  lateness (January reports, a 10 November original) it stopped converging, so it is a wrong rung (R4),
  refuted by the June-to-September back-test.
- Whole-percent December ownership to absorb estimator spread: dropped; the back-test selects the
  holder-level construction and every graded figure is held at one decimal.
- Portal round 1 (author's report 2026-10-11): rubric average 52 (top responses passed the bridge end
  557,031,720 and the restated-reports bar -16,011,685; in-house round 1 had every September figure, every
  December count and every top holder); Determinism QC failed (A pass, B C D fail, E pass, F plausible, G
  unsure; answer_contradicts_files, golden_wrong): OM-4 s.2 counted the managers that "file" for the period
  and filed no completion, so the literal reading flags WHII and JEMS from the reports on file, and the
  count of managers to carry (128 against 125) and the carry basis were unpinned. Filing the completion
  method itself would make the decisive step rule application and hand the call over; loop 1 files the
  estimand and a basis-selection criterion instead and moves the stump to the basis.
- task181 collision (task446's pre-flight, 2026-10-11): the shipped driver ("complete reporter by reporter
  from each one's last report, not one aggregate completion share") shared the decisive gap, G12, the
  calibration form and the stump strategy with task181 ("the complete count each unit's own arrival history
  implies, not an arrival speed pooled across units"); replaced by a different claim (the last report is
  stale for the filer class that drifts), stump strategy `forecast_method_backtest`, decisive pattern E.
- Flat carry as the golden: with the estimand filed literally it is the natural method and every solver
  reaches it; it is the stump rung now.
- Ask devices on hosts whose September filings fall after 3 November (the brief's placement): a
  mishandling that removes September lines (a failed CUSIP dropped, latest-accession-wins on a new-holdings
  host) then lowers only the back-test's final figure, shifts every basis's miss upward and can hand the
  selection to flat carry; every September device host files all its September reports by 3 November
  instead, so every mishandling cancels between the day-34 estimate and the final figure.
- The three September reports filed in January and NH's 10 November original: any mishandling that drops
  them (one data set only, latest accession wins) lowers only the back-test's final figure by 2 to 3 points
  and hands the selection to flat carry; removed, NH re-homed and re-timed.
- Optional A4 as proposed (a market maker's December option lines worth more than the largest holder's
  stock): counting them in ownership moves on-file December by several points on those names, so the main
  call's own option filter becomes load-bearing on a device, and the option family repeats A2; replaced by
  the top holder's rename on its December cover page.
- Active types left to drift (scratch prototype): per-type changes of -9 to +26 per cent on the twelve
  names, and the type-change completion then sits up to 1.5 points from the index-only version; fixed by
  holding every active type flat in aggregate.
- OTF as the only name near the line (prototype): one rate for every manager still due (3.3 per cent or
  more) then lands the golden set; FENN is placed at 79.6 with multi-strategy funds still due, so no single
  rate gives both.
- Attrition (four advisers that file September and never December): under the literal estimand they are
  still due and estimated, and in a back-test window a June filer that never files September has no final
  figure; removed, the register's inactive rows are managers absent from all three drops.
- Mean of per-manager ratios with position turnover alone (builder, 2026-10-11): the per-manager ratios
  average back to the pooled change and the basis missed the September window by only 0.30 to 0.38, under
  the 0.6 target; fixed with manager-level book flows (1.171).
- FENN's multi-strategy holdings still due at 14 per cent (builder): one rate crosses the line on FENN at 3.02
  per cent and on OTF at 3.24, 0.22 apart against the 0.3 the design asserts; moved to 16 per cent (2.66
  against 3.24).
- Late active filers moving 1.0 per cent a position (builder): own-trend carry put GLI at 84.33 against the
  golden's 84.39, across the bin edge; 0.7 per cent and GLI's target at 84.43 keep both in 84.4.
- Device sizes drawn freely inside the design's ranges (builder): SAF's COM-only drop (-0.36) and its October
  count (+0.36) cancelled to 0.005, and A2 kept with COM-only and keyed dropped left the bridge end 21,178
  shares from the golden; sizes now come from a search asserting every combination clears 0.06 points and
  100,000 shares.
- Loop 1 asks as device-carried lookups (September counts and ownership, top holders, the September bridge, devices A1 to A5), round 2, 2026-10-11: the solver missed the call at the designed rung but landed every one of these figures; each device was a work order an OM-4 rule points at (s.3, s.4, s.5, the cover-page amendment fields, the December cover-page name). Proxy 45.1 with the call missed. The ask layer is rebuilt on the decisive construction's outputs.
- Round 2's leak in the spec's terms (2026-10-11): every ask device was adjudicated by a filed rule on its own path (OM-4 s.3 options, s.4 check digit, s.5 latest count, the readme's amendment types, Wexley's cover note, the layout's cover-page name pin), so the careful path executed each as a work order; and the plan recorded with round 2, rebuilding the asks on the decisive construction's outputs, is rejected too (keyed to the construction, ban 4: the cracker banks it). The December share counts and the top holder are dropped as graded asks because no silent device fits them (December twelve-name lines stay clean, VALUE is fixed by the readme's filing-date rule and s.6, the holder's name needs a pin); the layer moves to the September figures the criterion runs against, on two devices no filed sentence speaks to (same-day amendments ordered by number, a restatement's header period).
- Ordinary same-day pairs as June restatements filed with the September original (builder, ask layer, 2026-10-11): an identical June restatement dated in October moves the department's June lines past the June window's day 34, so the issuer-level rival's back-test miss moved from 2.894 to 3.127 and the main-call identity assertion failed; replaced by three September re-filings in full on the original's day, which move no share, no date and no main-call figure.
- The ask sheet's full-grid floor of 3.0 million shares on the bridge end (builder): unreachable, since A2 kept alone moves the end 2.1 million and the negative hazards sum to 3.4 million; asserted on the stops instead, with every grid cell's end different from the golden (closest 12,431 shares).
- Loop 1 main call (completion by register-type change pooled across names), round 3, 2026-10-11: the solver tested five bases in OM-4 s.2's back-test (none, carry, per-security ratio, pooled ratio, type-pooled ratio) and landed the call on the type-pooled ratio (0.042 pp); round 2's solver had stopped at carry. The ask layer held (ask share 18 per cent, 0 of 4 items). Loop 2 deepens the decisive step past the type-pooled basis.
- Loop 2 with the sponsors' stakes held constant (no creations) and only each name's share count moving, the first
  form considered (prototype, 2026-10-12): the sponsors' change pooled across the names then sits at the
  share-weighted mean count move (about 1.00), so the type-pooled basis collapses onto flat carry, the register-type
  signal that drew round 3 to it disappears, and the default path no longer ends on the type-pooled answer; the
  creations stay at 5.5 per cent, so the golden's stake formulation grows the September stake by the filed sponsors'
  stake change.
- The type by name change for every type as the golden's second formulation beside the stake carry: the active
  types' per-name changes are noisy by construction and the grid misses the back-test by 11.0, and making them converge
  would turn the decisive step into the reflex "condition on every visible attribute" (readability test 3); the
  per-name change is the golden for the sponsors only, and the full grid is an R4c rival.
- Creations at 3.5 per cent to retire the realism debt (prototype): the sponsors' stake without growth becomes the
  closest rival (0.77, ahead of the type-pooled change at 0.82) with OTF 0.39 under the line; kept at 5.5.
- Share-count moves on OTF, FENN, GLI and SAF only (prototype): the type-pooled rung then kept the golden's one-decimal
  December figure on eight of twelve names, so a response stopping there banks most of the December figures; buybacks
  and at-the-market issuance spread across the watchlist in both windows cut that to three (GLI, FENN, HAMR) without
  moving the back-test (the type-pooled change 0.66, the golden 0.04).
- An accelerated repurchase on HAMR in the December window: HAMR's August offering (A5) makes a buyback in the next
  quarter implausible; the December-window buybacks sit on WHII, AMRB, JEMS and NOPR.
- GLI's December target at 84.43 (loop 2 build): the golden sat at 84.424, 0.026 under the 84.45 edge, and the judge's pass 3 (2026-10-12) found the near-argmin family (peers read as every December filer, other types mixed carry and pool, best miss 0.0402 against the golden's 0.0408) at 84.452, which rounds to 84.5; the target moved to 84.39 (family 84.384 to 84.414) with HAMR's December target at 55.22 to hold its September slack at 52.479, and SF14 asserts the family.
- The bridge asked as "one bar for each item between the two totals" (judge pass 3): 435,800 option shares sit inside replaced reports, so replaced-first and options-first both tie to the end total with different first two bars, and the matched-back bar could be split three ways by kind of mis-keying; the prompt now names the three bars and their order (SF15), and the stakes clause about never reissuing a file came out to keep it under 1,000 characters.
- Architecture 1 itself (the 13F holdings carry, quantitative finance): the portal's determinism block failed it
  (answer_contradicts_files: OM-4 section 2 named the filers for the period and filed no completion, so a literal
  reading flagged WHII and JEMS, and the 128 against 125 managers to carry was unpinned), and this session's batch
  audit found it short of the survivor anatomy (its decisive basis was a filed criterion's selection, not a link no
  key invites); re-rooted rather than repaired, so the portal sees one strong build.
- Architecture 2's first draw, coroner-held registrations completing a provisional count in
  census-register-administrative-data-quality as a designation set for a statistics office with a funder as the
  forum (2026-10-31, at the draw, never registered): its card axes sat on task485's (the same subdomain, objective,
  strategy, decision type and organisation family, a provisional register count completed for a period still
  maturing), and by the time it was ready to register its forum (funder_or_donor) and shape (01) repeated the last
  three builds; the world and the decisive step kept, the build moved to official time series production, an
  allocation, an NHS board and its panel.
- A repeat-homelessness draw (2026-10-31, at the draw, never registered): eight councils' case records linked
  across councils on the applicant's name and birth date, where households housed out of district come back on the
  host council's file. It died on the analyst test: once the grant letter files that a duty owed by any housing
  authority counts, which determinism needs, a strong analyst who reads it correctly links the councils' records and
  lands the golden, so the decisive step was reading the scope, with no textbook estimate a careful reader would
  prefer to the link.
- The draw as first registered (2026-10-31T22:45:01Z, pushed in 9b6e0799): survey-research-official-statistics with
  seasonal-adjustment-official-time-series-production, shape 05 (an allocation of GBP 2.4 million on each place's
  excess), the board's Heat Resilience Panel as forum and a programme officer as the role. task468 v5 had registered
  the same pairing, subdomain, shape, forum, role and decision type eight minutes earlier on another branch, so on
  main the card took six bans; the same world and decisive step were redrawn onto data integration, a scorecard
  designation, the board itself and a policy adviser, with gap time and pattern G3, because every honest (population,
  G12) and (population, G3) signature with a designation was already spent five or more times.
- A data-notes PDF in the pack (2026-10-31, at the leak sweep): a page describing every field of the three mortality
  extracts, written to close the version, timestamp and certification forks; sweep 12 found 49 of the extracts'
  column names in it verbatim (a describing file, LEAK). Removed; each fork it closed is closed by the terms or by the
  rows themselves, and the board's care home list joined the pack as its tenth file.
- Ask C with one device (the correction's date read as the registration's): the full includer, reading version 1 for
  every field, kept all 24 figures (pair stress row 86.2); the districts' 2026 review of care home residents
  registered at a family address in another place was added as a second device, so the entry as it now stands takes
  its address from version 2 and its date from version 1, and the full includer keeps 8 of 32.
- Ashwold with 34 heat-wave deaths held for inquest (build, 2026-10-31): its completed excess, 7.4 per cent, made the
  golden set the top three of the completed register's sort, an interval; at 40 held deaths it is fifth of six (6.3).
