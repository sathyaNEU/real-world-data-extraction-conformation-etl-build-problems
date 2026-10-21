# task249 design note (architecture 6)

## Draw

Card `cards/task249.json`, architecture 6, a fresh draw on 2026-10-21 at the author's standing instruction ("whatever
was retired do a fresh rebuild from scratch") after architecture 5 was spent at stage 4 on 2026-10-20. Architectures 1
to 5 are in the card's lineage with their fates and in `## Tried and rejected`; architecture 5's generator, pack and
goldens leave the folder with this draw (history holds them). Guard verdict WARN, no BLOCK. test.same_puzzle_older and
test.same_driver_older are NOTEs, differentiated on the card against task193 (v2) and task254 (v3). Each WARN, answered:
driver.near task83 at 0.12 (a randomized holdout's effect conditioned on each unit's prior trend under a cap): the cap
there limits an allocation; here it is a sitting's four hours, which couple a candidate's items, and nothing is
allocated. overuse.gate_g (method_or_model_selection): the mechanism carrying the stump is the counterfactual the gain
is estimated against, the direct excess on recognised items or the total with the time those items freed, and no other
key is true of it. repeat.decision and repeat.question_form (designation_set, which, after task252): the decision is a
designation of forms to flag and reassemble, so it is asked as which. The chart ships as a PDF page, so the deliverable
set is not task252's.

- **Pairing.** Psychology & Behavioral Science / psychometric-measurement-scale-validation, a task type serving
  Descriptive and Data Quality Monitoring. Not banned against the last three live builds (task482 SROS ETL, task177,
  task252 PES DQ). The object is the integrity of an examination's resit results, read form by form, and the call is
  the monitoring decision the regulations attach to it: which forms' 2027 resit results carry the exposure flag in the
  integrity report and are reassembled before the forms are used again.
- **Niche.** The Institute of Healthcare Coding Professionals (Chennai), a professional body of medical coders, runs the
  Certified Clinical Coder examination: four windows a year since February 2026 at six test centres, 170 items in a
  four-hour open-book sitting (code books on the desk), 150 scored and 20 trial, forms drawn at random among those a
  candidate has not sat, a results review that shows a failing candidate the scored items they got wrong with the
  keys, resits in any later window. Each bank item is written from an item model; 2027's ten forms reuse 2026 items and
  siblings written from the same models in different measure, and three of them (CC27-B, D and I) carry many case items
  (an operative or discharge note to code), so four in ten candidates run out of time on them.
- **The call.** Which of the ten 2027 forms gave their resit candidates more than one scored item per resit sitting
  from what an earlier sitting or results review had shown them (regulations 7.2 and 7.3), if any. Golden (prototype,
  seed 2496): CC27-A, B, C, D, G and H; E, F, I and J under the line.
- **Shape.** 10, a scorecard of ten forms against one line (10 verdicts), with a chart of every form's gain against the
  line, the flagged forms marked (5 to 7 parts), and the asks: about 10 + 6 + 18 + 2 = 36 criteria before
  instruction-following. Decision designation_set, answer set_of_items, question form which.
- **Strategy.** causal_design: forms are drawn at random among those a candidate has not sat, so which items a resit
  candidate had been shown before is an accident of the draw, and the comparison the design implies sits inside each
  resit candidate; the decisive step is that the candidate's other items share the four hours with the recognised
  ones. G7 decisive (the sitting's operating window: which items the four hours let a candidate answer), G16, G10 (one
  item model is one memorable unit across item numbers); gap objective; Gate G method_or_model_selection; calibration
  none; context artifact register (the Institute's register of sittings and results); Layer 2 family
  estimand_identification, pattern own:exposure-spillover-through-the-time-limit.
- **Forum, event, organisation.** committee_or_panel (the Examination Committee flags and orders reassembly),
  statutory_or_regulatory_filing (the annual integrity report the Institute files with its accreditation body),
  cooperative_or_member_body (a professional institute of its members). Role research_desk (the examinations
  psychometrician).
- **People** (`guard.py names --geo India --seed 249`): Abhiram Sarin, the Institute's examinations psychometrician, who
  asks; Yahvi Reddy, the examinations manager. Neither appears in the prompt.
- **Data-native sentence.** In an open-book coding examination the code lookups take the time, and a resit candidate
  who recognises an item from an earlier sitting answers it without the lookup; on the forms whose case items run four
  in ten candidates out of time, the minutes those recognised items free buy the resit candidate the end of the form,
  and the items answered there are most of the gain on the two such forms that reuse a moderate number of items.
- **As-of.** Monday 17 January 2028 (the request); the integrity report goes to the accreditation body on 31 January.
  The call is retrospective by design: the monitored product is the 2027 resit results, and the decision it drives
  (flag them, reassemble the forms before their next use) faces forward.
- **Probes before the draw.** Architecture 6's first form (the gain on recognised items and their item-model siblings,
  untimed) was landed by both call-only probes (sonnet and opus), each with a within-candidate Rasch or logistic
  baseline; with the four-hour limit and latencies in the pack, both probes (sonnet and opus) filed CC27-A, C, G and H on
  the same direct excess and neither read the time channel (`## Tried and rejected`).
- **Sources.** The client's two-layer standard (estimand_identification: the control units touched by the treatment);
  published psychometric practice: repeat-examinee and item-exposure effects read on repeated against new items within
  candidates, item models and isomorphs as one memorable unit in automatic item generation, preknowledge read from fast
  correct responses, speededness read from not-reached items and response latencies. task230 (vigilance decay reset by
  task switches) and task144 (a spillover through followers) are the nearest shipped mechanisms; neither carries a
  treatment's effect through a shared time limit.

## Default path

1. Join the two releases of the results export (release 4's latencies in milliseconds), link candidates through the
   register's number changes, map the 2026 layouts' item numbers through the January 2027 renumbering and key every
   response from the bank snapshot; a 2027 sitting by a candidate who had sat before is a resit sitting.
2. Mark each resit sitting's delivered items an earlier sitting or held review had shown the candidate: the same item
   reached at an earlier sitting, scored or trial, or an item written from the same item model.
3. Fit each 2027 window's items on its first-time candidates (Rasch, or the share correct) and estimate each resit
   candidate's ability on the scored items nothing had shown them, blanks left out as not reached (scored wrong instead,
   the same forms).
4. Sum each resit sitting's correct answers on the recognised items less that ability's expectation, average over each
   form's 2027 resit sittings and flag above 1.0.

Ends on: CC27-A, C, G and H (the excess on recognised items alone).
Golden: CC27-A, B, C, D, G and H (the excess plus the items reached only in the time recognised items freed).

The lower rungs: the gain over the previous sitting flags nine forms, all but the speeded CC27-I (learning and the
rebound after a failed sitting carry it); resit against first-time candidates on the shared items flags none (ability
carries it); the same item alone flags A and G; the raw within-candidate excess flags A, C, D and G (CC27-D reuses easy
items). Both call-only probes on the timed pack (sonnet and opus) ended on the default path's four.

## Stump sentence

A competent analyst reads each resit candidate's gain as the excess on the items an earlier sitting or review had shown
them (or their siblings) over their own difficulty-adjusted performance on the other items, and flags CC27-A, C, G and
H; the other items share the four hours with the recognised ones, and on CC27-B and D, where four in ten candidates run
out of time, most of the gain is the items resit candidates reached at the end of the form only because the items they
recognised took them less time.

## Three rules

Task type: psychometric-measurement-scale-validation (Psychology & Behavioral Science), tagged in the taxonomy for Data Quality Monitoring: the integrity of a certification examination's resit results, read form by form as the score each form's resit candidates gained from earlier exposure, monitored against the regulations' one-item line.
Domain test: The deciding quantity is each form's repeat-examinee exposure gain, estimated the way psychometrics estimates it (item-level responses against first-time candidates' item difficulties within each resit candidate, an item model as one memorable unit, randomly drawn forms) and carried through the sitting's time limit the way speededness analysis reads latencies and not-reached items: an item recognised from an earlier sitting skips the code lookup, and on a speeded form the time it frees is spent on items at the end of the form that the candidate would otherwise not have reached.
Swap: "the forms whose resit candidates gained more than one scored item from what an earlier sitting or review showed them, counting the items reached in the time the recognised items freed" put into a hospital's readmissions has nothing to stand on: no form draws items at random, no item model makes two questions one memory, no four-hour limit couples one patient's items, and no latency or blank at the end of a sitting records what time bought; with megawatt-hours the sentence loses every noun.
Layer 1: the delivery vendor's results export (a response string and a latency string per sitting, blanks where no answer was recorded, the end reason), two export layouts across the year, the 2027 bank migration's new item numbers with a crosswalk, candidate numbers merged after re-registration, trial items interleaved at fixed slots, review bookings with cancellations. Nothing is placed to be caught.
Layer 2: estimand_identification: the within-candidate comparison of recognised with unrecognised items is the design's own, and the step is that the unrecognised items are not untouched controls, because the sitting's four hours are shared and the time recognised items free is spent on them; the gain is the direct excess on recognised items plus the correct answers on the items reached only in the freed time.
Decisive step: counting, in each resit sitting, the items the candidate reached only because the recognised items took less time than the candidate's own pace on unrecognised items says they would have (the time freed read from the latencies against first-time candidates' times on the same items, carried to where the four hours would have ended), and adding the correct answers among them to the excess on the recognised items.
Not semantics: every field reads as what it is (the response, the seconds on each delivered item, a blank as no answer recorded, the end reason, the item model, the review booking), and no field, code, unit or definition says that a recognised item frees time, that freed time reaches further items, or that an unrecognised item's answer can come from an earlier sitting.
Not rule application: regulation 7.2 files the gain as a counterfactual (the sitting's scored items answered correctly that would not have been had no earlier sitting or review shown the candidate any item) and says nothing on how it is estimated; no rule names latencies, speed, reach or time saved, so executing every filed rule leaves the estimate to the analyst, and the analyst's natural estimate counts only the items shown.
Analyst test: A strong analyst who reads every file correctly, links resits through the register, counts the same item, the trial item, the review and the item-model sibling as exposure and estimates each resit candidate's excess on them against first-time candidates' difficulties at the candidate's own ability flags CC27-A, C, G and H; the same analyst who also carries the time the recognised items freed to the end of the four hours files the golden (checks.py runs both on the clean world and on the pack).
Estimand: for each of the ten 2027 forms, the average over its 2027 resit sittings (sittings by a candidate who had sat before) of the number of the sitting's scored items the candidate answered correctly that they would not have answered correctly had no earlier sitting or results review shown them any item; flagged above 1.0 (CCC regulations 7.2 and 7.3).
No decoy: nothing is planted: the responses, latencies and blanks are what the delivery system recorded, the forms what the Institute assembled, the reviews what candidates booked; the speeded forms are speeded because their case items take time, as case items do; no memo, draft or figure argues for any list, and no file ranks the forms by gain or names time saved.
No certified replay: no certified or published figure sits in the pack; the regulations state the estimand and the line, the vendor's export records sittings, and no file states a form's gain or flag.
Lesson: a within-unit comparison of treated with untreated parts measures the treatment's total effect only when the parts do not share a budget; under a binding limit the treatment's savings are spent on the untreated parts, so the comparison misses the effect exactly where the limit binds; no shipped build carries a treatment's effect through a shared time limit.

## Readability screen

| Rung | Where a reader meets it | Verdict |
|---|---|---|
| 1. The gain over the previous sitting (nine forms, all but CC27-I) | the exports' scores, the first read of a resit | readable |
| 2. Resit against first-time candidates on the items both met (no form) | the layouts and the exports | readable |
| 3. The same item alone, within each resit candidate, difficulty-adjusted (CC27-A and G) | the renumbering and the layouts; the field's repeated-item comparison | readable |
| 4. Item-model siblings counted with the same item (CC27-A, C, G and H: the default path) | the bank's item_model column and regulation 3.4; both call-only probes took it | readable |
| 5. (decisive) The items reached only in the time recognised items freed (adds CC27-B and D: the golden) | nothing names a recognised item's time, the time it frees or where the four hours would have ended; the latencies, blanks and end reasons are recorded as what they are | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | what a results review shows | each scored item answered wrongly at that sitting, items left blank not shown | the blanks shown too | same call | regulation 4.2; asserted |
| SF2 | an item an earlier sitting showed | an item the candidate reached there | every item delivered there | same call | asserted |
| SF3 | a trial item met before | counts as shown (7.2: any item) | scored positions only | same call | asserted |
| SF4 | a resit sitting under a changed number | linked through the register (2.1) | numbers as given | same call (Layer 1 does not carry it) | regulations 2.1 and 7.2; asserted |
| SF5 | the year | the February to November 2027 windows | none | same call | regulation 7.2; asserted |
| SF6 | more than 1.0 scored item | strictly, unrounded | at or above | same call | every form at least 0.3 from the line (asserted) |
| SF7 | a recognised item's time had nothing shown it | the log-normal mean of the first-time candidates' log seconds, shifted by the candidate's pace | the median | same call | asserted (family lowest flagged 1.5, highest unflagged 0.6) |
| SF8 | the baseline on the unrecognised items | a logit shift on the first-time candidates' share correct | an additive shift | same call | asserted |
| SF9 | a booked review cancelled or not attended | showed nothing | counted as held | same call | the bookings' status; asserted |
| SF10 | the four hours | examination time: the latencies exclude the stops of 3.6 | wall time | same call | regulation 3.6; asserted (no stopped sitting's latencies exceed four hours) |
| SF11 | release 4's latencies | milliseconds | seconds | same call | the data notes; asserted (each release's medians agree once converted) |
| SF12 | a failure of the workstation or its power (ask A) | a WS_FAIL, or the Kochi power cut, after the clock started | the invigilators' pauses, the link losses | the asks only | regulations 3.6 and 7.4; asserted |
| SF13 | the sitting a failure interrupted (ask A) | the one whose clock was running on that workstation at that moment | the logged booking_ref | the asks only | the event times (asserted: the paths differ on six or more forms) |
| SF14 | ran in part without the link (ask B) | the clock ran while the workstation's link was down | any loss logged against the booking | the asks only | regulation 7.4 and the data notes (the client carries on); asserted |
| SF15 | a link loss with no NET_BACK (ask B) | down until the sitting's end | dropped | the asks only | asserted |

## Ladder

| Route | Flags | Count | Golden |
|---|---|---|---|
| The gain over the previous sitting | A, B, C, D, E, F, G, H, J | 9 | no |
| Resit against first-time candidates on the items both met | none | 0 | no |
| The same item alone, within each resit candidate | A, G | 2 | no |
| The raw within-candidate excess (no difficulty adjustment) | A, C, D, G | 4 | no |
| The excess on recognised items, siblings included, blanks not reached (the default path) | A, C, G, H | 4 | no |
| The same with blanks scored wrong | A, C, G, H | 4 | no |
| Golden: the excess plus the items reached only in the freed time (Rasch, log-normal mean) | A, B, C, D, G, H | 6 | yes |
| Golden with an additive baseline; with the median time | A, B, C, D, G, H | 6 | yes |

On the clean world the excess on recognised items alone files the default path's four and the reach added files the
golden (checks.py, dataset-generation 7.1). CC27-I is speeded like B and D and stays under the line, so speed alone
flags nothing.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the ten 2027 forms and the year's resit sittings of each | filed (regulation 7.2) |
| 2 | Unit of account | a form's gain per resit sitting, in scored items | filed (7.2) |
| 3 | Attribution window | the 2027 windows' resit sittings | filed (7.2) |
| 4 | As-of dating | the exports as delivered; the bank snapshot of 31 December 2027; the register to January 2028 | filed |
| 5 | Version basis | the regulations as amended in June 2027 | filed |
| 6 | Denominator | the form's 2027 resit sittings | filed (7.2) |
| 7 | Weighting | each resit sitting once | filed (7.2, an average over sittings) |
| 8 | Window length | the year's four windows | filed |
| 9 | Boundary inclusivity | exceeds 1.0 | C1 (0.3 clear, asserted) |
| 10 | Rounding path | no gain graded; counts whole | filed (the prompt) |
| 11 | Tie-break | none open | asserted |
| 12 | Maturity and censoring | every 2027 sitting in the exports; a review counts only before the resit | filed (4.2) |
| 13 | Order of operations | exposure marked, ability and pace from the unrecognised items, the clock rerun, the two parts summed per sitting, then averaged | C1 (asserted) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | none in the call's rows; on the asks a sitting counts once | filed |
| 16 | Identity normalisation | candidate numbers through the register, item numbers through the renumbering | filed (2.1; the data notes) |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | seconds (release 3) and milliseconds (release 4) | filed (the data notes) |
| 19 | Code and status semantics | blanks, end reasons, review status, event codes | filed (the data notes); never the stump |
| 20 | Integerisation | the sitting counts whole | filed (the prompt) |
| 21 | Clause scope | 7.2 and 7.3 for every 2027 form; 7.4 for every form | filed |
| 22 | Forward window contents | a flagged form is reassembled before it is used again | filed (7.3) |

## Literal reader

Executing the prompt and every filed sentence word for word (the regulations, the data notes, the request) leaves one
open move, how the counterfactual of regulation 7.2 is estimated, and the design and the data force it: forms drawn at
random among those not sat (3.5) make the comparison inside each resit candidate the design's own; an item recognised
from an earlier sitting is answered in about 70 per cent of the time the candidate's own pace on the other items gives;
and on the forms where four in ten candidates run out of the four hours (blank items at the end, time expired), the
time freed is spent on the items at the end, which a sitting with nothing shown would not have reached. The
counterfactual of 7.2 covers every scored item of the sitting, so those answers are in it. Every licensed estimate
files the same six (asserted: a logit or additive baseline, the mean or median counterfactual time; lowest flagged 1.5,
highest unflagged 0.6).

## Oracles

- No file ranks the forms or states a form's gain, flag, exposure count or reach.
- The exports state responses, latencies, end reasons and scores; the regulations state the estimand and the line.
- The bank snapshot states each item's model and format; no file states which items a candidate recognised.
- The event log states events and the incident reports describe incidents; no file states which sittings a failure
  interrupted or which ran without the link.
- The panel's decision log and minutes, the practice-test orders and the centres' capacity (the distractors) carry no
  figure any route needs.


## Ask sheet

**Ask A, each form's 2027 sittings a failure of the candidate's workstation or its power interrupted (10 figures,
whole numbers).** H18: regulation 7.4 puts the interrupted sittings in the integrity report beside the flags, the
record of each form's sittings delivered through a failure; the call reads the two exports, the layouts, the bank
snapshot, the renumbering, the register and the review bookings, and never the event log, the seat plan or the
invigilators' reports (asserted). Use: the report's 7.4 table, filed every year. Primary devices: D7, the true key
elsewhere: the server raises WS_FAIL when a workstation stops answering, and the log export fills the booking from the
seat plan as it stood at export, so a morning failure at a workstation repaired at lunch and used again in the
afternoon carries the afternoon's booking (61 of 2027's 119 failures), while the morning candidate resumes on a spare or,
with a few minutes of work left, has the sitting closed on the saved responses (17 with no resume); only the event times
place a failure in the sitting whose clock ran on that workstation (the logged booking moves 8 forms, -9 to +4). D4,
absence as the signal: the Kochi power cut of 19 August 2027 at 11:05 local took the centre's server down with the
workstations, so the log holds nothing for the sittings it stopped until they resumed, and the invigilators' report
records the cut (left out, 5 forms move, up to -9). Hazards: the invigilators' pauses (resumes with no failure), the
link losses, the reboots between sittings. Path: the event log, the seat plan, the invigilators' reports, the
regulations, the data notes and either export for each booking's form (6 files, 10 columns). Realism: a log export
that resolves the booking through the current seat plan; a power cut that takes the logging server down with the room.

**Ask B, each form's 2027 sittings that ran in part without the centre's link (10 figures, whole numbers).** H18:
regulation 7.4's third item, the sittings whose responses were held on the workstation while the link was down; the
call never reads the event log. Use: the same table. Primary device: D6, a log read as a roster: every seated
workstation logs the centre's link losses against its booking, a candidate who had finished and one still in the
tutorial alike, so only a loss overlapping the sitting's clock (SESSION_START to SESSION_END) counts (every loss row
counted moves all 10 forms, +17 to +41). D4: a loss still running when the session closed has no NET_BACK (67 began
inside a sitting's clock; dropped, all 10 forms move, -2 to -12). D8: a loss that began in the tutorial and ran into the
examination counts (a loss timed inside the clock only moves all 10, -4 to -23). Hazards: a flapping link (several
losses in one sitting count once), losses inside the tutorial alone. Path: the event log, the data notes, the
regulations and either export for each booking's form (4 files, 6 columns). Realism: a centre's link loss is logged on
every workstation in the room, and a workstation that closes its session before the link returns logs no NET_BACK.

Main population zero-counts: the event log, the seat plan and the invigilators' reports are read by the asks alone,
and no file the call reads carries a device row (asserted: separation).

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| the seat plan's afternoon booking on a morning failure (D7, primary) | A | -9 sittings |
| the power cut's missing events (D4, primary) | A | -9 sittings |
| the invigilators' pauses read as failures | A | +16 sittings |
| every seated workstation's loss rows (D6, primary) | B | +41 sittings |
| a loss with no NET_BACK dropped (D4) | B | -12 sittings |
| a loss counted only when it began inside the clock (D8) | B | -23 sittings |

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed on the fields it names) | Verdict |
|---|---|---|
| Ask A, sittings, all ten forms | each WS_FAIL's logged booking, the power cut's sittings from the invigilators' report, the pauses and link losses left out | miss |
| Ask B, sittings, all ten forms | each NET_LOST paired with the workstation's next NET_BACK and overlapped with the sitting's clock, a loss with no NET_BACK left out | miss |

Measured by: generator/pair.py on the cut pack (target.zip ff5b5f5b): the cracker keeps 3 of the 20 ask figures (CC27-A,
B and J of ask A, where neither the afternoon bookings nor the power cut move the count), the mirror (off the call, each
log's first reading: the failure's logged booking, every loss row) 2; a response that places each failure by its time,
reads the power cut from the report and overlaps each loss with the clock keeps all 20.

Pair ceiling: 35.4 ((38 + 7 + 55 x 3/20) and (5 + 7 + 55 x 2/20), averaged)

Mirror leakage: 10.0 per cent of ask weight

## Tried and rejected

- Drift forecast from the cumulative particle load through an optical PM sensor (drift accrues with dose, not calendar
  time): the lesson is task46's (a rate law stationary only in cumulative service exposure), so the driver is spent.
- Seasonal confounding of a PM sensor's gain by humidity growth or aerosol type: the shape of task248's driver (a
  covariate moving over the year against a level comparison), one build earlier.
- An analyser ask (each analyser's 2027 days over 120 micrograms on the EU maximum daily 8-hour mean): every device it
  carried (span-check hours flagged N, the old analyser's parallel rows) is adjudicated by the station sheet, so the call-landing
  response executes it and keeps every figure; dropped for the node quarter's single silent device.
- Architecture 1 (each node's span read from its spread against the four distant analysers, the paired slope
  attenuated by the sites' partial hourly agreement): the stage 4 reader (medium effort, about two minutes) landed the
  call with an errors-in-variables slope instrumented by the other stations' mean, cued by plan 4's "true ozone
  concentration at its inlet", and kept all 36 ask figures after reading the vendor's firmware note. Regression dilution
  is textbook statistics, so the decisive step is readable to a strong model; and an ask one device deep falls to one
  document read. Realism tells it named: firmware dates cycling in ten-day steps, installation dates on a fixed
  five-week pattern, visit slots on a fixed cadence, the ES4104A analyser's model against its serial (T400 and API400E),
  head serials stepping by 37. The judge's pass on the same bundle: DETERMINISTIC (write-up wording only); its residual
  reading F1, the spread of the four stations' averaged series, gives 10 nodes, so architecture 2's write-up says the
  analysers' hours are pooled.
- Ask A on firmware 4.2's renumbered codes alone, the release note carrying a table of the codes up to 3.7 and from
  4.2: architecture 1's stage 4 reader read the note and kept 36 of 36. The note now gives 4.2's codes only (the records
  show the old meaning: before each node's update its status-1 records are the two warm-up hours after a restart), and
  the restart clocks stand beside it as a second primary, each moving all 36 figures alone.
- The firmware table without a date for OZ19 read as OZ19 never reaching 4.2: the spare's records after the 25 January
  rename lost their humid hours (OZ19 +89 against +18 to +24 elsewhere); OZ19 runs 4.2 from the spare's start at 11:00
  on 9 January, in the solver, the verifier and A1.
- Architecture 2 (each node's span read on the mixed afternoon hours, the hill villages above the night's surface
  layer): the stage 4 reader (Sonnet, medium, about four minutes) landed the call with a regression on the four
  analysers, the 900 m sites' night-time intercepts and the register's altitudes pointing it to the midday hours;
  the judge's pass on the same bundle was DETERMINISTIC, APPROVE, and Ask A held (0 of 36). A site's night-time
  decoupling shows in any residual by hour of day, so the decisive step is readable to a strong model.
- Architecture 3 draw, 2026-10-19, candidates that died before the card was filed: register coverage by dual-system
  estimation within post-strata after erroneous enumerations (task448 already runs capture estimated within route
  strata in the same task type); an adaptive item bank's drift under compromise read with purified anchors (filed as
  drift on the bank's scale, its literal reading is the contaminated thetas, so the estimand forks unless it names
  the purification, which files the method); rapid guessing read from item-specific response-time thresholds (the
  decisive step is a threshold choice, a coin flip in the client's measured runs); this world's forward referral rate
  under the SE-scaled rule (1.645 times the standard error of the difference: the rule's own scaling compresses every
  account into 2 to 9 per cent, too thin for a cap) and a fixed eight-point band (elite accounts at 40 to 60 per cent,
  no firm would adopt it, and a 2028 verification record would let a solver carry each account's empirical shortfall
  forward). The confidence-band rule on the verification score, with the check new in 2029, keeps the spread
  realistic and leaves no per-account history to carry.
- Ask A's highest weekly exposure of any item (four figures): any response that checks the attempts against the
  register keeps it whole, so the ask's weight sat on the one device a careful response can find; replaced by the
  count of items rested for 2029, which the suite moves as well, and the ask cut to five figures.
- Appeal outcomes recorded as later rows of the original case: each case's latest row, the habitual read of a decision
  log, filed the golden, so the impersonation ask carried no device. The desk now logs an appeal as a case of its own,
  as its own sheet would, and a sitting's standing is the latest decision across the candidate's cases.
- The synthetic suite's sittings labelled release 5.3.2 in the week of 3 July, before the release went live: a marker
  isolating the device rows in one week. They now carry the release in service, as the platform stamps every attempt.
- Shrinkage of each pool's top share with each candidate's reported error (Kelley's formula at the estimate) taken as a
  competing reading: it adds NVK, UJB and OJS, but the study's own top tenth of MAT-R scorers refutes it (it predicts
  their MAT-V a tenth of a logit lower than scored) while the shrinkage at the ability, the full posterior and the
  world's own truth all file the 15. Kept as a rung and stated in the write-up's critical components, so a judge sees
  the refutation in the shipped data.
- Architecture 3 (each account's 2029 referral share read through its shortlist's regression to the mean, MAT-R's
  error at the ability and the retest gain at the interval): the stage 4 reader (Sonnet, medium, about eleven
  minutes) landed the call with a latent-ability model (a tier prior deconvolved from the 2028 pool, Table 4.3's
  errors, the study's fitted gain), checked against the study's referral rates by interval and by MAT-R level, and
  kept all 19 ask figures, finding the 6,400 Monday-night identities outside the register, each candidate's latest
  case decision and the fresh booking references from release 5.3.2; the judge's pass on the same bundle was
  DETERMINISTIC, APPROVE. Selection on a noisy score is the textbook regression to the mean, a shrink the author file
  names as a reflex, so the decisive step is readable to a strong model, and three devices one cross-file check deep
  each fall to the hygiene battery. Realism tells it named: round plan counts and shortlist ratios, the suite's
  identical early-Monday timing and short sittings, uniform selection-day spreads, the study's fixed interval grid.
- Candidate 1 as offered to the author (signed-out visitors on other browsers as the comparison for signed-out WebKit identifiers): in a world without a meter it is the golden, and holding every visible status fixed is the careful opponent's reflex, so it would be landed by the first thorough reader; prototyped at the draw (proto3 and proto4 in the session scratchpad), the decisive step moved to what that reflex gets wrong, the sign-in the capped meter produces. A first cut of the print-subscriber skew modelled print readers as daily readers and moved nothing (the skew shifted the device-only route by 0.5 points): daily readers never reset, so print subscribers are drawn as the weekly and occasional online readers a print household is.
- The sign-in trap at the draw's weekly gaps (eight to nine days, two to three registration chances in ten on WebKit):
  the sign-in split fell only 2.6 points short of the golden on the meter editions, inside a reader's variant of it;
  weekly readers now come every eight to twelve days, so WebKit's meter almost never reaches the wall, and the gap is
  5.5 to 6.6 points.
- The hybrid (signed-in browsers from the register, signed-out identifiers by every other browser) at the draw's
  reader mix: within 1.5 points of the golden everywhere, because removing the few signed-in WebKit readers barely
  moves the pool's revisits; it lands the call unless the signed-in pool is large and frequent. A local edition's
  loyal core (daily and regular readers about a third of the month's browsers, registered on every engine) makes it
  fall 4.4 to 5.7 points short on the meter editions.
- Print-heavy editions under the line to catch the signed-in ratio: the ratio over-corrected them by only 2.5 points
  at a realistic print share; with the loyal core the ratio falls 10 points short on every non-print edition, so it
  needs no print-below rung, and those editions became ordinary unnoted ones.
- Ask B's primary as return slips dated by collection (weekly points covering the week before): the quarter starts on
  a Monday and ends on a Saturday, so a slip never straddles it and shifting every slip one publication day gives the
  exact answer; dropped for the COMBI's e-paper on the e-paper platform.
- Ask A's primary as contacts archived after the year's end and missing from the export: their groups at archiving
  would have to ship somewhere, which marks them; dropped for the export's current groups after the new year's mailing.
- A 0.6 scale world with 5.3 million sessions at full scale: the export reached 75 MB; the populations were scaled by
  0.6, daily readers' sessions a day trimmed, and the export sorted by identifier (3.0 million rows, 34 MB).

- Architecture 4, stage 4 round 1 (2026-10-19): reader 1 (Sonnet, medium, about thirteen minutes) landed the call without
  the decisive step. Every browser had carried one user-agent string and one address all quarter (3,048 prefixes,
  about 65 identifiers each), so chaining the anonymous WebKit identifiers within user agent, address and edition, each
  new one at least seven days after the chain's last session, matched the register's devices within 0.04 per cent and
  filed the golden's eight. Reader 2 fell on the trap (three editions, the signed-in ratio bridged by state). The judge's
  pass on the same bundle was DETERMINISTIC, APPROVE. The landing came through a construction defect, the browsers
  observable through a fingerprint no real export carries, not through the decisive step. Repaired in the generator:
  - Addresses now vary by session: household lines that reconnect (daily, weekly, monthly or fixed) inside each
    edition's region's provider blocks, mobile networks' shared pools, and office lines on weekday daytimes.
  - User agents are shared by version and move with each release at the browser's own lag; Safari's system token is the
    one Safari has reported since version 26.

  After the repair, reader 1's chain misses the register's devices by 24 to 64 per cent. Every chaining key fails its
  own check on the registered identifiers by 12 to 43 per cent and files 0, 4 or 9 editions (chain_test.py in the
  session scratchpad). The route table is byte for byte the same.
- Ask A's primary as the export's current groups after the new year's mailing, with the mailing's additions in the
  group-change log: both stage 4 readers reversed the log and kept all twelve figures (a change file over a base list,
  which the hygiene battery executes). The mailing's additions now come through the newsletters' one-click links,
  recorded only as clicks in the activity log among the article clicks; the preference centre's log does not hold them.
- Ask B's primary as the COMBI's e-paper counted again: both readers matched order_ref Kombi to the COMBI and kept every
  figure (one dictionary line and the reference settle it). It stays a hazard. The primary is now the circulation
  system's release of 6 November, which wrote the date of a saved change into the start date until the fix of
  4 December; only the numbers' entry order finds it.
- Realism tells the readers named:
  - Fixed: e-paper accesses starting in 1974, before the e-paper existed (each plan now starts no earlier than its
    launch); one order reference on two accesses (now unique); start dates spread evenly back to 1974 (now a tenure
    curve, with subscriptions older than the system carrying its go-live date).
  - Kept: 88 per cent of sessions signed in, which a registration wall after five free articles produces in frequent
    readers; Rhineland-Palatinate's editions print-heavy and Hesse's digital, a rural against commuter-belt geography.
- Stage 4 round 2 (2026-10-19, target.zip d00ed7b6): both readers missed the call. Reader 3 filed the default path's
  four (the signed-out replay with edition weights); reader 4 filed nine, Bergstetten marginal (signed-in readers
  reweighted by session count). The newsletter device held for both: each noticed 49 contacts whose groups the
  preference centre's log does not explain and left them as exported. Reader 4 kept all twelve sold-copies figures (12
  of 24, exit 1). It was cued by twelve subscriptions the release had re-dated past their own end date, an impossible
  record that a start-before-end check finds, then the numbers' entry order and the COMBI accesses' earlier starts. The
  judge: DETERMINISTIC, APPROVE. Repaired: the release re-dates only a subscription still delivered when the change is
  saved; customer numbers are unique (reader 3 found trials sharing a daily subscriber's number); retail points keep
  a weekly rest day or a holiday closure (reader 4: exactly 378 rows on every issue).
- Stage 4 round 3 (2026-10-19, target.zip 31ad0d1e, the final pack). Reader 6 missed the call: the sign-in split's
  four, with 0 of 24 ask figures. Reader 5 landed the call with 0 of 24 ask figures (exit 1). It calibrated each
  anonymous WebKit identifier's share of a browser on the signed-in WebKit browsers, stratified by edition, by whether
  the cookie predates the quarter, and by the identifier's sessions in the month (1, 2, 3, 4 or more), and filed the
  eight with Bergstetten at 24.2. Round 2's reader 4 took the same calibration with the strata pooled over editions and
  filed nine (Bergstetten 25.8). The light strata of the signed-in WebKit pool are mostly print subscribers, the
  readers whose sign-in the meter does not select, so the stratified calibration leans on the very population the
  golden validates on, without the reader naming it. The judge's pass on this pack: DETERMINISTIC, APPROVE (the 24 ask
  figures exact). The cap's selection runs through visit spacing, which an identifier's own session count partly
  shows, so any calibration stratified on activity recovers most of it. Four of five clean readers across rounds 1 to
  3 missed the call (one landing, one more within one marginal edition); round 1's other landing came through the
  repaired fingerprint. Under the two-reader rule a call any reader lands is spent. Hardening the ladder against one
  estimator is not a repair, so shipping as measured, a fifth architecture or retirement is the author's call.
- Architecture 4 as a whole (WebKit's seven-day cookie cap, the meter's selection of who signs in, the transport within
  edition, month and device class): spent at stage 4 round 3 when reader 5 landed the call. The cap selects through
  visit spacing, which an identifier's own session count records, so a calibration stratified on activity recovers the
  selection. The number was retired on 2026-10-20 at the author's choice.
- Retired on 2026-10-20 at the author's choice when architecture 4 was spent (four architectures: 1 and 2 a PES
  low-cost sensor network's drift pull list, 3 a psychology verification check's genuine referral rate, 4 Product
  Analytics' WebKit cookie cap), and un-retired the same day at the author's request for a fresh rebuild. The lesson
  the four paid for: a transport or selection a unit's own trace can reconstruct is spent; architecture 5 puts the
  regime in a second continuous record and the selection in when the field team could reach the river.
- Architecture 5 draw, candidates set aside before the card was filed: a stage-discharge rating's hysteresis on the
  rising limb (task229's hydrometry world, the subdomain's spent neighbour); a seismic network's station leverage (the
  golden's and the easy route's ranges overlapped, 72 to 89 against 84 to 93 per cent); a solar array's soiling
  (task152's ground); a fixed sampling clock aliasing the tide; light traps under the lunar cycle; sensor warm-up after
  restarts. The turbidity surrogate conditioned on the hydrograph limb was the one whose decisive step the samples
  themselves force and no file names.
- The prototype's routine rounds drew fractional days, so rounds fell at any hour and the glacier stations' summer
  rounds missed the melt's rise; fixed before any tuning was trusted.
- MKE as a sand-rich glacier station sampled on evening rounds with early callouts (a trap for the trip type): the
  linear and positive rate-of-rise relations read it at +12 to +20 against the rising indicator's near nought, a fork
  on the main call; MKE is now a silty station below a proglacial lake, inside 8 per cent on every specification.
- JVB with one round a month: some rising-water specifications fell to +5 to +9 (rising turbidity, positive rate of
  rise), too close to the tolerance; two rounds a month in the melt season and a sandier bed put every specification
  above +18.
- Stations drawn on shared random seeds had identical discharge histories (four glacier rivers, three rain rivers,
  three lake outlets); every river now runs its own hydrology under one regional storm calendar.
- The field app's wall-clock time without its offset: in the prototype, read as UTC, it moved several stations inside
  the tolerance past 15 per cent on the golden method, so Layer 1 carried the call (R2); every sample time now carries
  its offset, and the wall clock read as UTC fails to reproduce the report (SF9).
- Every station's bottle count a multiple of six (no round ever missed, every callout two bottles): rounds are now
  missed at a realistic rate and callouts bring back one to three bottles (44 to 101 per station).
- A field remark "rising, brown water" on callout bottles named the decisive regime; the remarks say "high water" and
  "brown water" only.
- Ask B per month (12 figures of nought to three): the template's nominal moves only the second half's months, so the
  cracker kept the first half's; per station, the stale lot moves 13 of 14 figures.
- A laboratory re-run of a failed batch as an Ask B device: suspended sediment by whole-sample filtration cannot be
  re-run; dropped as unrealistic.
- Architecture 5 (turbidity surrogate conditioned on rising water), spent 2026-10-20 at stage 4: both scored readers
  landed the call and all 28 ask figures. Sediment hysteresis is the field's textbook effect, so a reader who knows the
  field tests the rising limb first, and the simulated relation's scatter (0.025 in log10) made the residuals
  two-valued at a glance; the ask devices (old flag letters decodable from the maintenance log, the lot's concentration
  in the quality statement) were found by both. A decisive step that is the domain's named reflex is no stump against
  a reader who knows the domain.
- Architecture 6 draw, candidates set aside before the card was filed (2026-10-21): a cancer registry's completeness at
  the publication cut-off (the never-registered share is model-bound: flow method, Ajiki and chain ladder all licensed,
  and task194 died on a chain-ladder family); web page views under prerender and the back-forward cache (the
  classification overlaps, and release notes announce both mechanisms); a business survey's dead units imputed as live
  (identification needs a follow-up subsample or a continuity extrapolation); remote cognitive testing's device latency
  (person fixed effects are the reflex, and the staggered switch is task230 v1's driver); maternal mortality's
  pregnancy checkbox (the error's age gradient is a fitted extrapolation and the coding rules make the call semantic);
  a test form's speededness on its own (the share running out of time is nearly observed in the time used at the
  limit, and the cost needs an absolute reference only forms far apart in time demand supply).
- Architecture 6's first form, untimed (the resit gain on items an earlier sitting or review had shown the candidate
  and on their item-model siblings, the sibling the decisive rung): both call-only probes landed the golden. The sonnet
  probe fitted a logistic model with a shift per exposure category, siblings their own categories; the opus probe
  fitted Rasch difficulties on first sittings, took each resit's ability from its unexposed items, summed the residuals
  on the exposed ones (same item, review, trial slot, sibling) and checked item misfit against unexposed resitters. With
  forms drawn at random the within-candidate comparison is the design's own, and a strong reader marks every exposure
  channel a column shows, so a retrospective gain on the items shown leaves the analysis nothing to get wrong. The
  sibling stays as a lower rung; the decisive step moved to the four-hour limit the items share.
- Ask B as each content area's 2027 trial items standing accepted at the year end, read from the panel's decision log
  (withdrawals, revisions and entries under the earlier item numbers): the log's latest decision per item, the lazy
  path, kept most figures, so the ask carried no device a careful response misses; replaced by the sittings that ran
  in part without the centre's link, and the log ships as a distractor.
