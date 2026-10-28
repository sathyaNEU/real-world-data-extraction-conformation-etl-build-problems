# task488 design note

## Draw

**Status: DESIGN 2026-10-28, architecture 1 drawn in education at the user's request** (an education task with a
data-engineering feel and an analytical stump). The seed ET45 world (barcode catalog matching) was paused at stage 1
with no card; its resume line allows a redraw outside the seed's world, so the slot keeps its number and objective
(ETL) and moves to `education-learning-sciences / item-response-theory-test-equating`, the only education task type
that serves ETL. The ET45 screen is kept below as a record.

- **Card:** `.claude/skills/fingerprint/cards/task488.json`, v1, registered 2026-10-28; `guard.py check` PASS (one
  NOTE: `driver.near` 0.13 against task479's architecture 4, differentiated on the card: that build removed answers
  given too fast to read before scoring; this one removes nothing).
- **Pairing:** Education & Learning Sciences, item response theory and test equating, Data Extraction & Conformation.
  The deliverable is the conformed item bank in the new platform's import layout, and the decisive field is each
  item's difficulty on the consortium's reporting scale.
- **World:** the Quarrystone Regional Assessment Consortium, eleven Wisconsin school districts that own an adaptive
  mathematics interim for grades 3 to 8, delivered since 2021 on Tessaline Learning Systems' platform. Its bank holds
  the items calibrated in the 2021 launch field test and about 500 items the member districts' teachers wrote in the
  2024 to 2026 summer workshops to measure students far below grade level; Tessaline ran those items on the writing
  panel's provisional difficulty ratings. Tessaline's contract ends 30 June 2027 and the bank moves to Corvane
  Assessment, whose blueprint needs a floor of items below each grade's Approaching cut.
- **Decision:** how many new low-band items the consortium must commission from the summer 2027 item-writing
  workshop, grade by grade, so every grade's bank meets Corvane's floor at the July 2027 cutover. Forcing event: the
  cutover; forum: the consortium's board (member superintendents), which funds the workshop by the accepted item.
- **Gap, pattern, generators:** gap objective (the panel's ratings, the percent correct and the reported scale scores
  are each correct as recorded and none is an item's difficulty on the scale); pattern none, generators G14 (an
  item's difficulty is its success rate conditioned on the takers' ability), G16 (two calibrations, the right one
  confirmed by the calibrated items' own values), G19 (the import contract). Labels population / G16 /
  method_or_model_selection were tried first and refused by `test.same_puzzle` and `test.same_driver` (task177's
  lineage and eight older builds).
- **Context artifact:** monitoring_export (Tessaline's item-statistics report: each item's administrations and
  percent correct among the students who met it, correct for that question). Redrawn in place from close_out_summary
  after the DRAWN push, when task162's ship commit relabelled its own card close_out_summary inside the window.
- **Strategy:** other (contaminated conditioning: the variable each estimate would condition on, the reported scale
  score, was computed from the quantities being estimated). Gate G etl_conformance. Calibration form
  gold_standard_subsample (the calibrated items' bank values, which only the right calibration reproduces).
- **Personas:** `guard.py names --geo us --seed 488`; Sheri Brady and Timothy Fitzgerald on the card (Natasha Fox and
  Kevin Thornton, drawn first, warned on first names used in older builds).
- **Data-native sentence:** an adaptive engine serves each item to the students its recorded difficulty matches and
  scores them with the recorded difficulties, so an item whose recorded difficulty is wrong is met by the wrong
  students and corrupts their scores in the same direction.

## Screen

- **Prototype (scratchpad t488/proto, cat4 to cat7):** six grades, about 340 calibrated items and 45 to 95 provisional
  items a grade, 7,000 to 8,000 students, a 35 to 45 item adaptive test selecting the item nearest the running
  estimate among a randomised few, scored by EAP with the bank's operational values. Writers rated single-step items
  about right and multi-step word problems about 2 logits too easy.
- **Routes on the prototype (low-band totals over six grades, cut at -0.75):** truth 618; marginal likelihood with the
  calibrated items fixed 620; alternating EAP 620; re-scoring on the calibrated items only, EAP 620; calibration
  against the reported scale scores (the default path) 644; joint maximum likelihood 662; maximum-likelihood
  re-scoring on calibrated items only 654; the panel's ratings 740; percent correct mapped to difficulty through the
  calibrated items 397 (every provisional item out of the band).
- **Multi-step word problems (true mean about -0.05):** marginal likelihood -0.06 to -0.11; reported-score calibration
  -0.42 to -0.66; joint maximum likelihood -0.49 to -0.66.
- **The separating check:** the calibrated items re-estimated from the same responses. Mean error on items below
  -1.2: marginal likelihood +0.015, reported-score calibration -0.160, joint maximum likelihood -0.282 (and +0.168
  above 1.2). Only the marginal calibration reproduces the bank, so the data refute both wrong calibrations without
  any filed method.
- **Determinism risk carried into the generator:** items near the band edge. Under the right calibration the two item
  types sit on either side of the edge with a gap (single-step at or below -1.35, word problems at or above -0.4
  true), and the generator must keep every principled estimate at least 0.2 from the edge with enough takers per
  word problem (about 600) to hold its standard error near 0.1.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain, every field read correctly:

1. Take each grade's operational items from Tessaline's bank export: the 2021 launch items carry their calibrated
   values (`difficulty_basis` launch calibration 2021), the 2024 and 2025 workshop items carry the writing panel's
   ratings (`difficulty_basis` writing panel rating), and Corvane cannot load a rating as a difficulty.
2. Recognise that in an adaptive test an item's percent correct says little about its difficulty, because the
   engine served every item to the students it matched, so the item statistics workbook cannot calibrate anything.
3. Calibrate each workshop item the field's standard online way: the Rasch model fitted to the students who met it in
   the 2025-26 complete and incomplete events (unscored re-delivery rows dropped), each student's ability fixed at the
   event's reported scale score, theta = (QSS - 500) / 40.
4. Count each grade's items below its Approaching cut (launch values and the new estimates).
5. Commission each grade's shortfall against Corvane's floor of 150.

Ends on: 138 items to commission (19, 31, 19, 18, 42 and 9 for grades 3 to 8).
Golden: 199 items to commission (27, 39, 31, 33, 49 and 20 for grades 3 to 8).

## Stump sentence

The default path files 138 items to commission against 199, because it calibrates each workshop item against the
students' reported scale scores, which Tessaline computed with the writing panel's ratings: the panel rated a run of
multi-step word problems far too easy, the engine served them to students they were too hard for, those students'
scores fell with every miss, and read against the fallen scores 61 workshop items land back below the Approaching
cut, so the pools look 61 items deeper than the students' answers make them.

## Three rules

- Task type: education-learning-sciences / item-response-theory-test-equating, which serves Data Extraction &
  Conformation; the deciding quantity is each workshop item's difficulty on the consortium's Rasch reporting scale,
  the field that the conformed import carries and that Corvane's floor is counted on.
- Domain test: the deciding quantity is each new item's Rasch difficulty on the launch scale, which item response
  theory estimates jointly with the examinees' abilities while the anchor items hold their known values (a fixed-anchor
  calibration by marginal maximum likelihood); the swap fails because only an adaptive test serves each item to the
  examinees its recorded difficulty matches and scores those examinees from the same recorded difficulties.
- Swap: "how many new low-acuity beds must each ward commission so that every ward meets the state's floor when it
  moves to a new bed-management system" keeps a floor and a count and loses the object: no bed's level is estimated
  from occupants admitted because of the level recorded for it, and no occupant's record was computed from the beds'
  recorded levels.
- Layer 1: Tessaline's vendor item keys against the consortium's authoring ids (one row per authored version, a
  revision's version 2 sometimes under a new key while the old key stays operational in the export); event times in
  UTC across a daylight-saving change; an interrupted session's unscored re-delivery row; invalidated and incomplete
  events; retired items in the export; district-scoped student keys that change when a student moves; the item
  statistics workbook by window. Every item is what Tessaline's platform or the consortium's authoring system writes.
- Layer 2: field_method (the field's own calibration done right); the methodological choice is what each workshop
  item is read against: the students' reported scores, or abilities estimated jointly from every response with the
  launch items fixed.
- Decisive step: estimate each workshop item's difficulty jointly with the students' abilities from every 2025-26
  operational response, holding the launch items at their 2021 values, because the reported scores were computed from
  the workshop items' own provisional ratings and the engine served each item to the students those ratings matched,
  so any reading against the reported scores returns the ratings.
- Not semantics: reading every field correctly (`difficulty_basis` marks the panel's ratings, the scale note gives
  QSS = 500 + 40 theta, the unscored rows are re-deliveries, invalidated events are not operational) still files 138
  on the reported-score calibration, 116 on a joint calibration that scores the students by maximum likelihood and 93
  on the ratings as they stand.
- Not rule application: no filed rule says how to estimate a workshop item's difficulty; Corvane's specification
  says only that it must be on the scale and estimated from the 2025-26 operational responses. Enumerated family
  (abilities fixed at the reported scores; joint maximum likelihood; re-scoring on the launch items by maximum
  likelihood or by posterior mean and then fixing; marginal maximum likelihood with a population per window or a
  fixed one, on grids of 41 to 161 points; alternating posterior means): commissions 116 to 214, an enumerated spread
  of 98 items. Standing family, the members whose re-estimates of the launch items return the launch values: 199 in
  every grade, a spread of 0. Ruling-out loudness: the check that rules the rest out, re-estimating the launch items
  below 452 the same way, is one nobody runs without asking whether the method recovers what is already known, and
  nothing filed points at it (within 1.0 point for the standing family; 3.4 to 7.6 points too easy against the
  reported scores; 11.8 to 16.7 too easy under joint or maximum-likelihood re-scoring; 1.6 to 6.0 too hard under
  posterior-mean re-scoring).
- Analyst test: a strong analyst who conforms the export, sees that percent correct in an adaptive test says nothing
  about difficulty and calibrates each workshop item with the Rasch model against the students' reported scale scores
  files 138 items to commission (19, 31, 19, 18, 42 and 9 for grades 3 to 8), the default path's Ends on.
- Estimand: Corvane's import specification 3.2: the pool is each grade's operational items (section 1); an item's
  difficulty is on the customer's scale, a calibrated item keeps its value (section 2), and an item not yet calibrated
  takes a difficulty estimated from the 2025-26 operational responses of complete and incomplete events (section 3);
  a grade's pool needs at least 150 items below its Approaching cut and the shortfall is commissioned (section 5); the
  cuts and the scale are in the consortium's scale note (sections 1 and 3).
- No decoy: nothing is planted to be caught: the panel's ratings are the operational values Tessaline really ran,
  labelled as ratings; the reported scores are Tessaline's real scores; the item statistics workbook reports percent
  correct correctly; no memo, briefing or stakeholder figure argues a count.
- No certified replay: no certified or published figure exists for a workshop item's calibration or a pool's
  low-band count; the launch values anchor the scale and are not a figure the golden reproduces to choose a method.
- Lesson: in an adaptive test the students an item meets and the scores they carry were both set by the item's
  recorded difficulty, so a new item can only be calibrated jointly with the abilities, anchored on items whose values
  are known; no build on file teaches calibration under adaptive administration (task450 linked two forms through
  common items that drifted; task479's architecture 4 removed rapid guesses before scoring).

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | 7 dedicated organ | verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the panel's ratings as they stand (93) | silent | the bank's difficulty column holds them | the read-the-file reflex | silent | silent | silent | silent | readable |
| R1 percent correct mapped through the launch items (333) | silent | the item statistics workbook invites it | a generalist's calibration | silent | silent | silent | silent | readable |
| R2 Rasch against the reported scale scores (138) | silent | the event file's scale score is the obvious ability | the field's online-calibration reflex | silent | silent | silent | silent | readable |
| R3 joint maximum likelihood (116) | silent | silent | the concurrent-calibration reflex | silent | silent | silent | silent | readable |
| R4 (decisive) joint marginal calibration with the launch items fixed | silent: the specification names the scale and the data, never a method, and the scale note names no method | silent: no column carries an ability except the reported score, and no column carries a calibration for a workshop item | silent: the reflexes are the reported score and joint maximum likelihood, both wrong | silent: no control or published figure scores a calibration; the launch values check a method only for an analyst who thinks to re-estimate them | silent: no sweep re-estimates known items | silent: an estimation over abilities and difficulties together, with each window's population | silent: the response file is Tessaline's delivery log, which the migration needs anyway for exposure and history, and the launch values are the bank's own | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternatives | Call under each | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "new items to commission" | the floor less the pool's count below the cut, never negative | items to write so that enough are accepted | another quantity | Corvane specification section 5 (the customer commissions the difference as new items) |
| SF2 | "below the Approaching cut" | strictly below | at or below | same call (no workshop item within 3 points of a cut; the nearest 6.7) | asserted |
| SF3 | a launch item at the cut | none sits there | n/a | same call (no launch item within 3.6 points of a cut) | asserted |
| SF4 | "the pool" | one record per authored item, a re-keyed revision once under its current key | every operational row of the bank export | same call (every re-keyed revision sits 8 or more points above its cut) | specification sections 1 and 2; asserted |
| SF5 | "operational responses" | complete and incomplete events, re-delivery rows unscored | invalidated events kept, re-delivery rows read as wrong | same call (asserted) | specification section 3 |
| SF6 | the students' population in the estimation | a normal population per window | one fixed normal population | same call (asserted) | converges |
| SF7 | the estimation grid | 81 points | 41 or 161 points | same call (asserted) | converges |
| SF8 | the marginal estimation | marginal maximum likelihood | alternating posterior means | same call (asserted) | converges |
| SF9 | the launch items' difficulties | their 2021 values | re-estimated from 2025-26 | another quantity | specification section 2 (a calibrated item keeps its value) |
| SF10 | the band test's precision | the difficulty to one decimal | unrounded | same call (asserted) | converges |
| SF11 | the floor's reach | each grade's pool on its own | the six pools pooled | another quantity | specification section 5 (a grade's pool) |
| SF12 | rounding | whole items | none other | same call | the prompt's last sentence |
| SF13 | an item in the import (the asks' population) | each authored item once, under its current version's key | every operational row of the bank export, a re-keyed revision under both keys | other ask figures; the call is the same (every re-keyed revision sits 8 or more points above its cut) | specification section 1 (each item is loaded once, under the key of its current version) |
| SF14 | a later version's blank field in the catalog | unchanged from the version before, unless changed_fields lists it (then cleared) | the field is empty; or the union of every version's value | other ask figures; the call does not read the catalog | the catalog's own form: every version 1 is a full record and a later version populates only the fields its changed_fields lists (asserted) |

## Ladder

| Rung | Construction | Items to commission | Against the golden |
|---|---|---|---|
| 0 | the panel's ratings as they stand | 93 | 106 under |
| 1 | joint maximum likelihood | 116 | 83 under |
| 2 | re-scored on the launch items by maximum likelihood, then fixed | 137 | 62 under |
| 3 (default path) | Rasch against the reported scale scores | 138 | 61 under |
| golden | joint marginal calibration, the launch items fixed | 199 | |
| over-correction | re-scored on the launch items by posterior mean, then fixed | 214 | 15 over |
| heuristic | items under 30 per cent correct taken out of the band | 271 | 72 over |
| heuristic | multi-step word problems taken out of the band | 320 | 121 over |
| generalist | percent correct mapped through the launch items | 345 | 146 over |

- Position and dominance: the golden is bracketed, four wrong routes under it and four over it; the default path
  differs from the golden in every grade (8 to 15 items a grade), and the nearest wrong route on the near side is 61
  items away, 31 per cent of the call.
- Family: the standing family (marginal likelihood with a population per window or fixed, grids of 41 and 161,
  alternating posterior means) files 199 in every grade, its nearest workshop item 3.5 to 16.4 points from a cut.
- Worth: the decisive step moves 61 workshop items across the cut and the call by 61 items; no route in the standing
  family moves a single item.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | each grade's operational items, one record per authored item | specification sections 1 and 2; SF4 |
| 2 | Unit of account | items | the prompt and specification section 5 count items |
| 3 | Attribution window | the pools as they open in July 2027 | the prompt; specification section 5 |
| 4 | As-of dating | the close-out export of 31 March 2027 | the export's own date; no item changes status after it |
| 5 | Version basis | an item's current authored version | the catalog's versions; SF4 |
| 6 | Denominator | none (counts) | the call is a count |
| 7 | Weighting | each item once | the specification counts items |
| 8 | Window length | the 2025-26 school year | specification section 3 |
| 9 | Boundary inclusivity | strictly below the cut | SF2, no item within 3 points |
| 10 | Rounding path | the difficulty to one decimal, counts whole | SF10, SF12 |
| 11 | Tie-break | none needed | no item at a cut |
| 12 | Maturity and censoring | none (the year is closed) | the export is after the spring window |
| 13 | Order of operations | estimate, then count, then the shortfall | the specification's sections in order |
| 14 | Row order | none | the estimation is order-free, asserted by the rebuild |
| 15 | Duplicate resolution | an interrupted session's unscored re-delivery row carries no score | SF5 |
| 16 | Identity normalisation | vendor keys to authored items through the catalog | SF4 |
| 17 | Netting against gross | none | counts only |
| 18 | Dimensional units | scale points, theta = (QSS - 500) / 40 | scale note section 1 |
| 19 | Code and status semantics | operational, retired; complete, incomplete, invalidated | specification sections 1 and 3 |
| 20 | Integerisation | counts are whole | SF12 |
| 21 | Clause scope | the floor per grade | SF11 |
| 22 | Forward window contents | the pools as loaded; the commission is written after the count | specification section 5 |

## Literal reader

Executed word for word, the prompt asks for each grade's shortfall against Corvane's floor of items below the
Approaching cut, and the specification fixes the pool, the scale, the data the workshop items are estimated from and
the floor; every reading of those terms (SF1 to SF12) gives the same call or is ruled out by a quoted section; the easy
answer (138) comes from an easy method on the same estimand, the Rasch fit against the reported scores, never from
another reading.

## Oracles

none: no control, published figure, reconciliation column or corpus scores a workshop item's calibration or a pool's
count. The item statistics workbook reproduces from the responses under every route (it is percent correct) and favours
no rung; the launch values are the scale's anchors, readable as a check only by an analyst who re-estimates them.

## Layer 1 inventory

| Mess | System that produces it | Files | Handled by | Moves the call |
|---|---|---|---|---|
| Vendor item keys against authored ids, versions in the catalog | Tessaline's bank and the consortium's authoring system keep their own keys | bank export, catalog | the catalog's item_key per version | no (re-keyed items sit above every cut) |
| A revision re-keyed with its old key still operational | Tessaline issued a new key for a 2024 revision and never retired the old one | bank export, responses, catalog | one record per authored item | no (asserted) |
| A catalog whose later versions record only what they changed | the authoring system's version history: the 2024 alignment and accessibility review made version 2 of every revised launch item, a 2025 accessibility pass made a version 3 of 100 and a version 2 of 117 workshop 2024 items | catalog | each item's versions read in order (SF14) | no (the call does not read the catalog) |
| Event times in UTC across the November daylight-saving change | Tessaline logs UTC | events | not needed by the call | no |
| An interrupted session's unscored re-delivery row | the platform re-delivers the item on screen | responses | rows without a score carry none | no (SF5) |
| Invalidated and incomplete events | test administration | events | specification section 3 | no (SF5) |
| Retired items | the 2024 review | bank export, catalog | specification section 1 | no |
| District-scoped student keys that change on a move | Tessaline keys students by district | events, roster | not needed by the call | no |

## Ask sheet

**Ask A: the imported items by grade and 2026 framework domain** (30 figures: grades 3 to 5 in NSO, ALG, FRA, MDA and
GEO; grades 6 to 8 in PRR, NUM, ALG, GMS and DAP).

- H18 home: the domain columns of the conformed import that Corvane's specification requires (section 2), the
  measure every imported item carries that the commission does not turn on.
- Path: the bank export's operational rows, the catalog's versions (key, status, framework code, skill tag), the
  crosswalk's 2010-to-2026 rows with their skill-tag condition.
- Pin: specification section 1 files the population (each item loaded once, under the key of its current version),
  so the 98 revisions Tessaline re-keyed in 2024, operational in the export under both keys, are a hazard the
  battery's cross-system match repairs, not the device.
- Primary device (silent): the catalog is a version history whose later versions record only the fields they
  changed. The 2024 review set each revised item's 2026 framework code on version 2, and a 2025 accessibility pass
  that changed only art, alt text or text-to-speech markup made a version 3 of 100 of them and a version 2 of 117
  workshop 2024 items, so the active row's code and enemy group are blank. Read as the item's whole record, the active row sends a re-aligned item back through the crosswalk to its
  2010 domain; the join is one to one, the crosswalk absorbs the blank without a gap, and nothing errors. Benign twins:
  a 2025 version of an item whose code is its 2010 domain moves nothing, and blank fields fill every later row; the
  pass is drawn so that the active-row reading moves every domain count of every grade (A6).
  Secondary: workshop items carry 2026 codes that are not their 2010 domain; the crosswalk's measurement codes in
  grades 3 to 5 split by the skill tag.

**Ask B: enemy sets by grade and the items they hold** (12 figures).

- H18 home: the enemy_set column of the conformed import (specification section 4).
- Primary device (silent, two-sided): a group set on a revised item's version 1 stands on the versions after it
  that leave the field blank, while the 2024 review cleared 11 items' groups on version 2 (changed_fields lists the
  field, left blank). The active row alone drops the inherited members; the union of every version keeps the cleared
  ones; only the versions read in order give the sets. Hazards: the re-keyed revisions' version 1 rows carry the old
  key, so a group mapped by key loses the member; cross-grade members; retired members; a group that falls to one item.
- Separation: the call never reads the catalog or the crosswalk, so no ask device row sits in the call's files or
  columns; the only bank rows the asks turn on are the 98 old keys of the re-keyed revisions, each 8 or more points
  above its cut (SF4, A4), so loading them or not leaves every pool's count below the cut.
- Referee: the catalog's version history settles which keys are one item and which fields stand; nothing ties only
  under the golden, and a grader confirms each inherited or cleared field from changed_fields.

| Ask figures | The cracker's route | Against the golden | Verdict |
|---|---|---|---|
| A, imported items by grade and domain | each authored item once under its active version's key (section 1), the active row read as the item's record: its 2026 code, else the crosswalk with its skill tag | an item whose 2026 code is not its 2010 domain sent back to the 2010 domain wherever a 2025 version stands on it, every count of every grade moved | miss |
| B, enemy sets and their items by grade | the active rows' groups by authoring id, one grade at a time, two or more to a set (section 4) | under wherever a group stands on version 1 behind a blank later version, in every grade | miss |

Measured by: generator/ceiling.py
Pair ceiling: 29.8 (cracker 45.0 on the call and none of 42 ask figures; mirror 14.6)
Mirror leakage: 4.8 per cent of ask weight (the mirror keeps 2 of 42: grade 8 GMS and NUM)

## Pre-ship check

- **The decisive step is still analytical, on the built pack.** A strong analyst who conforms the export, reads every
  field and calibrates each workshop item with the Rasch model against the reported scale scores files 138 (R3a); only
  estimating the workshop items jointly with the students' abilities, the launch items fixed, files 199, and every
  member of that family agrees in every grade (R3b). No filed sentence names a calibration method: the scale note
  says only that the launch calibration set the scale, the specification only that the estimate is on the scale and
  from the 2025-26 operational responses. Not semantics, not rule application, nothing planted.
- **The mess is still only Layer 1.** Keeping the invalidated events and reading every unscored re-delivery row as a
  wrong answer leaves the call (SF5); counting a re-keyed revision under both keys leaves it, every one sitting 8 or
  more points above its cut (SF4).
- **The domain still decides.** The deciding quantity is each workshop item's Rasch difficulty on the launch scale,
  and the separating check is the field's own: the launch items re-estimated the same way return their values only
  under the joint calibration (R3d).
- **Determinacy on the built pack.** The standing family (marginal likelihood per window or fixed, grids 41 and 161,
  alternating posterior means) files 199 in every grade; the nearest workshop item sits 3.5 points from a cut under
  the alternating member and at least 6.7 under every marginal member; no launch item within 3.6 points of a cut.
- **Gate G.** No shipped artifact ranks or counts the pools: the item statistics workbook reports percent correct by
  window, correct for that question, and the panel's ratings are labelled as ratings.
- **The ask layer after the judge's pass 1.** Specification section 1 now files the import's population (each item
  once, under its current version's key) and the catalog's own form files how a version's fields stand
  (changed_fields); the silent primary under those pins is the 2025 accessibility version whose blank fields the
  active-row reading takes as empty; the cracker misses all 42 ask figures. Rebuilt with every file the call reads byte-identical (bank export, sessions, responses,
  scale note, item statistics, panel ratings, roster) and the call at 199 in every grade.
- **House fixes run.** H1: the PDFs' writer comments blanked, every container stamped by its fictional owner; H8:
  every cited section resolves (specification 1, 2, 3, 4, 5; scale note 1 and 3); H9: no file describes the pack; H16:
  no event after the close-out export; H21: the three organisation names checked against real companies, none found.

## Leak sweep

- `leak.py --asof 2027-04-02`, 2026-10-28: REVIEW, four lines, no LEAK, after two fixes in the generator: the session
  file renamed from `tessaline_test_events` (the author's word test in the name) to `tessaline_sessions_2025-26.csv`,
  and the item statistics workbook given a report's headers.
- Answer-figure sweep, Corvane's specification (9 of 9 distinctive words of the call) and the scale note (7 of 9):
  harmless; the words are the estimand's own (items, the Approaching cut, grade, commission), which the specification
  files as section 5 and the scale note as section 3; no figure of the answer is in either.
- Stump-vocabulary sweep, the specification (consortium, operational, adaptive, calibrated, window, estimated) and the
  scale note (scores, launch, calibration, reported, consortium, correct): harmless; each is the document's own
  vocabulary for the pools, the data and the scale, and neither says how a workshop item is calibrated, that the
  reported scores were computed from the panel's ratings, or that the engine served items by their ratings.

- Reader round 1 (2026-10-28, general-purpose at medium, fresh copy of the pack and the prompt only): questions 1 to
  4 none (no sentence names the decisive step, no file counts the answer or helps the analyst, no figure reads as the
  answer); question 5 quotes specification sections 1, 2, 3 and 5 and the scale note's QSS = 500 + 40 theta, each
  executing to the golden's population and data with the estimation left open; question 6 analytical; both review
  lines harmless. Realism: the workshop payments file paid every writer exactly 600 + 85 per accepted item across both
  years. Fixed in the generator: a stipend schedule by year (a day rate and an item rate), days attended, mileage to the
  consortium office at the year's federal rate, payroll or invoice dates, on its own random stream so the incidents
  file is byte-identical.
- Specification section 1 gained a sentence at the judge's pass 1, so the reader ran a second round on the rebuilt
  pack (2026-10-28, fresh copy): questions 2 to 4 none; question 5 quotes sections 1 (the new sentence read as one row
  per item at its current version), 2, 3, 4 and 5 and the scale note's boundary sentence, each executing to the
  golden; question 6 analytical, the estimation of the panel-rated items left open by the files; both review lines
  harmless; realism none (it checked the new stipend schedule and the whole-point ratings, which the panel file
  explains). Its question 1 quotes sections 2 and 3 with the bank's difficulty_basis as the step that sends about 500
  items to re-estimation: harmless, that is the population every route re-estimates (the default path takes the same
  step and files 138), and the reader's own question 6 places the decision in the estimation method, which no sentence
  names.
- The rebuild reused the stored rival, family and anchor figures; an in-memory full recompute on the same tables
  matched figures.json on all 328 keys.

## Determinism judge

- Pass 1, 2026-10-28: DETERMINISTIC, FIX_NOW. The judge reproduced the call (199: 27, 39, 31, 33, 49 and 20), each
  grade's count below the cut and the workshop items below it, both wrong routes (93 on the ratings, 138 on the
  reported scores), and the single-population sensitivity (the same call). Gate G: method_or_model_selection,
  analytical_non_defect, surface_read_dependency no. Gate H: domain pass, layers pass, decisive step analytical.
  Finding (Gate A on the asks only): it loaded both keys of the 98 re-keyed revisions as items (2,636 rows against
  2,538), because section 1 read pool membership off the export's status and nothing filed said an item is loaded
  once. A fork, not a device: closed by section 1's "each item is loaded once, under the key of its current version",
  with the enemy groups' version reading closed in the catalog's own form (SF13, SF14) and the silent primary re-sited
  onto the 2025 accessibility versions (the ask sheet). Ask-layer repair under the gate table: G and H pass, no architecture spent.
- Pass 2, 2026-10-28: DETERMINISTIC, APPROVE. The judge reproduced the call, both component rows, the import's 2,538
  rows, all 30 domain cells and every grade's enemy sets (reading the catalog's versions with changed_fields), and
  the 93. Gate G and Gate H as pass 1, matching the card and the note. Non-blocking note: block 1's rejected 138 did
  not reproduce under the thread's two readings of "against the reported scale scores" (191 and 125); block 1 now
  names the construction that gives 138 (a Rasch fit of each workshop item with every student's ability fixed at the
  event's reported scale score), no pack file or graded figure moved, and the zip digest is unchanged.

## ET45 screen record (paused 2026-10-26, superseded by the redraw)

Stage 1, not yet drawn. Seed ET45 (a nutrition app's product master merged from USDA FoodData Central
Branded Foods and Open Food Facts on barcodes), header and situation only. Objective ETL. The only client
task type that serves ETL in this world is `general-statistics-data-science/data-integration-record-linkage-entity-resolution`,
so the deciding quantity has to be record linkage's own statistical object (match and non-match agreement
rates, a key's evidence, linkage error, entity counts), and the seed's barcode normalization (leading zeros,
UPC-E, GTIN-14 indicator digits, check digits, restricted circulation codes) can only be Layer 1 or an ask
device, because the answer flipping on it is data semantics.

Banned against the last three builds at the screen (task304, task271, task270): strategies composition_mix,
forecast_method_backtest and maturity_censoring; forums committee_or_panel, board_of_directors and
executive_team; forcing events launch_or_rollout and period_close; org families financial_institution and
retailer_or_ecommerce. Personas drawn with `guard.py names --geo us --seed 488`: Natasha Fox, Kevin Thornton,
Mary Adams (unused until the draw is fixed).

Live candidates when the screen stopped, both unspent in the corpus (no driver mentions value-specific
agreement or matcher calibration):

1. The weight of an agreement depends on how common the agreeing value is (Fellegi-Sunter value-specific
   u-probabilities, the client's rigor pattern 2 for this task type taken to the value level). Its open
   problem is determinism: the probability that a unique exact agreement is the record's own product needs
   the share of records whose product is in the target file at all, and every route to it is a model.
   The cleanest determinate form found is the birthday-problem one, coincidences counted from pairs whose
   quasi-random field differs by a step (birth dates a few days apart), which lives in person linkage and
   would leave the seed's world.
2. A matcher's stated probabilities are overconfident where its fields record one fact (independence
   assumption broken), measured in the reviewed band and carried on the log-odds scale to the unreviewed
   auto-link band; a coarse dial of offered cut-offs keeps it determinate. Open problem: stump power, since
   the review band shows the miscalibration to anyone who bins it.

## Tried and rejected

- Precision of an attribute matcher carried from a small-block pilot to the full build, rebuilt from the
  per-comparison false-acceptance rate times the comparisons each block makes: the lesson is task192's
  (an instrument's error rates carry, its predictive values do not when the base rate moves) and task446
  v2's, in record-linkage nouns, so it is a repeated driver whatever the guard's lexical score (0.07).
- Resolving pairwise links into entities under a one-record-per-source constraint, chains cut at the
  weakest link: task486 architecture 2's driver, landed by its scored reader A.
- Correcting a noisy disagreement flag for its own error rates measured on known true and false links to
  estimate a barcode join's false-match share: task468's heart (linker misses and false links measured on
  control groups) and close to task456's latent class.
- Self-null coincidence rate (how often FDC's own distinct products agree on brand, serving and panel)
  applied to label-snap stubs: a paper simulation on seeds 488, 7 and 11 showed pair-level precision
  dominated by visible ties, so the tie rung lands the golden, and the per-link form needs the
  counterpart share, which no file pins.
- Clustered audit errors read with a design effect at the company prefix: task228's and task261's lesson
  (variance built at the unit the errors cluster within).
- The ET45 world's two live record-linkage candidates (value-specific agreement weights; a matcher's overconfidence carried to the auto-link band) were left unbuilt at the 2026-10-28 redraw into education at the user's request; the first had no determinate form inside the seed's world and the second's miscalibration shows to anyone who bins the review band.
- Ask layer, first form: the import's population left to the export's operational status with nothing filed on a
  revised item's keys, and enemy groups read from every version's row; the judge's pass 1 loaded both keys of the 98
  re-keyed revisions and called the one-per-item golden wrong, a fork sold as a device. Replaced by the section 1 pin
  and a version-history catalog whose 2025 accessibility versions carry the silent primary.
