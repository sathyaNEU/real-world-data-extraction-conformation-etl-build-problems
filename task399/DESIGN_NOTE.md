# task399 design note

Architecture 4, drawn 2026-11-03 (wave 7, Root-Cause lane, sathay3012), numbered from seed RC05 (a regional
electricity distributor choosing one reliability programme from five, where the costliest cause leaves no record of
its own). The seed's world collided at the draw; architecture 1 (Quantitative Finance) was spent at the draw in
task398's cell, architecture 2 (a bus operator's drivers' rest) at the draw as a template of shipped task121 v6, and
architecture 3 (a licensing agency's road-test booking journey) at stage 2 on the pricing harness (`## Tried and
rejected`, the card's lineage). Kept from the seed: the decision (one initiative funded from a shortlist), the
quantity in kind (what each initiative's cause did to the year's outcome) and the kernel, a cost that leaves no record
of its own: a defendant called while the duty lawyer is serving the list next door leaves no record that nobody spoke
for them.

The Halsey Coast region's District Courts hear defendants arrested and held in police custody at the next sitting's
custody list. In the twelve months to 30 September 2026 the gap in remands in custody at first appearance between
defendants without their own lawyer and defendants with one widened. The Ministry of Justice's regional manager for
criminal court operations puts one initiative into the region's Budget 2027 bid, from a shortlist of five: more
electronically monitored (EM) bail assessment capacity, a District Court judge on the Kestrel Bay custody list, a
second duty lawyer on the region's custody-list roster, supported bail accommodation, and court-date text reminders.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task399.json`, architecture v4, registered 2026-11-03 with architectures
  1 to 3 in its lineage. `guard.py check` on the draft: BLOCK test.same_driver_older against task253 v2 (gap, G5 and
  binding_constraint) and WARN driver.near against task141 v1 (0.14), both cleared by differentiation lines (task253 v2
  re-solves a congestible network's loading; task141 v1 prices a release rule from the gradient across rota'd
  decision-makers); first-name WARNs on Anthony, Nathan, Gavin, Nicole, Jessica and Alexander redrawn, and Casey Neal redrawn to
  Julie Smith on the merged tree (people.last against task480). Re-checked on
  the registered card as the last act of stage 1: WARN overuse.org_family only (a Ministry of Justice region is the
  honest label).
- **Pairing:** Criminology & Justice (client domain) / `sentencing-bail-disparity-analysis` / Root-Cause Analysis; the
  subdomain has never been drawn, lineage included.
- **Objective and call:** where in the region's first appearances the widening sits and which shortlisted initiative
  removes it. The call is retrospective on the closed twelve months, with its reason: a root cause is named for a year
  already closed, the initiative is funded from July 2027, and nothing is forecast.
- **Shape:** 12, a drill-down to one leaf (region, courthouse, list, judicial officer, and the leaf the drill lands
  on), each branch's piece of the widening graded at each level. Arithmetic in `## Ask sheet` at stage 2.
- **Strategy and Gate G:** `binding_constraint` for both. One rostered duty lawyer is the limit that two lists sitting
  at the same time share, and that limit moves the naive pick off the bench. Gap objective (the duty lawyer's daily
  presence and volume are correct and are not what decides); generator G5 (provision elsewhere: the provision was in
  the next courtroom when the matter was called).
- **Furniture:** forum `minister_or_cabinet` (the Budget 2027 bid goes to the Minister), forcing event
  `budget_or_appropriation`, org family `government_agency`, role family `operations_director`, context artifact
  `operations_log` (the duty lawyer service's own record), question form `where`. The ban window (task274, task277,
  task398) holds none of them.
- **Neighbour:** task274 (criminology, a US county's pre-plea diversion lottery on docket events) is three builds back.
  The domain repeats; the subdomain, objective, geography, spine (an appearance extract, not docket events), decision
  and mechanism do not (differentiation on the card).
- **People** (`guard.py names --geo "New Zealand" --seed 399`): Freya Herd (regional manager, criminal court
  operations), Julie Smith (manager of the region's duty lawyer service), Toby Conway (Corrections EM bail team
  leader). None is in the prompt.
- **Data-native sentence:** the court's appearance extract records a defendant's counsel of record (blank alike for a
  defendant the duty lawyer helped and for one nobody helped) and the minute each matter was called, the duty lawyer
  service records each defendant it assisted and when, and the sitting calendar records the audio-visual remand list
  sitting in the next courtroom, so a custody-list matter called while the one rostered duty lawyer was on the
  audio-visual list exists only as a time overlap across three records.
- **Abstraction sentence:** one advocate rostered to two lists that sit at the same time leaves the cases called
  while it serves the other list unassisted; its daily presence and output are flat, so the decision-maker who sits
  the overlapping hours carries the gap on a within-decision-maker comparison. Not writable against an approved build:
  task119 (a resource recorded full but held empty for planned work), task303 (a shared upstream loss every sibling
  logs in the same minute), task124 (the kind a group was laid in, read off its surviving members) and task121 v6 (the
  rest actually taken against the schedule) each spend another relation.
- **Semantic screen** (`guard.py mechanisms --objective root-cause`, one line per build on the insight it spends):
  task13 re-attributes outcomes from an exceptions-only log; task11 a threshold rebate seen on a rebuilt ledger; task36
  a filed rule excluding the largest candidate; task50 the share of exposure inside a funded window; task72 the owner
  whose agreement covered each piece; task84 identical concurrent units competing on an unkeyed target; task111 the
  cause still operating in the forward window; task500 a matched-reference method pinned by certified statements;
  task129 a rise scaling with each unit's surroundings; task121 the conditions each event was made under (v6 the rest
  before a shift); task202 the share of each input reaching the layer the response draws on; task398 an exposure rule
  driven by the whole's own path; task399 v3 a capacity stock rebuilt from releases and bookings. **Is the new
  decisive step any of them in other nouns?** No: it reads one advocate's presence at each case's call across two
  simultaneous lists behind a within-decision-maker disparity; no build on file reads a disparity against the absence
  of the person who speaks for the case.
- **Slots, run twice before any harness:** setting nouns (bail, remand, duty counsel, duty lawyer, magistrate,
  detention): task202 only, whose note set aside a binding hold read from the jail extract (the holds sit in a
  column) and a charging-cell sentencing disparity (readable); neither is this insight. Mechanism nouns
  (double-booked, simultaneous, overlap, same session, two places, adjourned): none.
- **Library test:** the golden is not a named correction; the field's own method for the deciding quantity
  (disparity within court and judicial officer, net of the legally relevant pre-decision factors, the rigor card's
  pattern 4) sits at rung 1 and files a judge on the custody list.

## Default path

1. Take every first appearance from police custody in the two twelve-month periods (October 2024 to September 2025,
   October 2025 to September 2026) from the court's appearance extract, flag a remand in custody, and split by counsel
   of record (own lawyer against none).
2. The gap in the remand-in-custody share between defendants with no lawyer of record and defendants with one widens
   between the periods.
3. Estimate the disparity the field's way: within court and judicial officer, with the legally relevant pre-decision
   factors (charge seriousness, criminal history, bail history, on bail at arrest) as controls, the counsel-by-period
   interaction carrying the widening.
4. Drill: courthouse, then list, then judicial officer. The widening sits in the Kestrel Bay custody list, under the
   community magistrate who took it over in March 2026.
5. Check the dated changes: EM bail assessments slowed from February 2026 (EM bail is sought at a later appearance,
   never decided at the first); the duty lawyer roster is unchanged (one duty lawyer at every Kestrel Bay sitting,
   clients a sitting flat); reminders and accommodation show nothing at first appearance.
6. Fund a District Court judge on the Kestrel Bay custody list.

Ends on: a District Court judge on the Kestrel Bay custody list (provisional figures at stage 2).

Golden: a second duty lawyer on the custody-list roster, the widening read against whether the duty lawyer was in the
custody courtroom when each matter was called (provisional).

## Stump sentence

A competent solver measures the first-appearance custody-remand gap within court and judicial officer with the
legally relevant factors as controls, finds the widening in the Kestrel Bay custody list under the community
magistrate who took it over in March 2026, and funds a judge on the custody list (Ends on: a District Court judge on
the Kestrel Bay custody list); the step that lands it there is reading a within-officer difference as the officer's,
when the duty lawyer service's record and the sitting calendar show the single rostered duty lawyer was serving the
new audio-visual remand list next door when most of the widening's matters were called, which puts the gap on the duty
lawyer roster.

## Three rules

- **Task type:** criminology-justice / sentencing-bail-disparity-analysis, which the taxonomy tags RC; the call names
  where a bail disparity's widening sits in the region's custody lists and the initiative that removes it.
- **Domain test:** the deciding quantity is the disparity in remands in custody at first appearance between defendants
  with no lawyer of record and defendants with one, estimated within court and presiding officer net of the legally
  relevant pre-decision factors (charge seriousness, criminal history, bail history, on bail at arrest), the way bail
  disparity analysis estimates it, then followed down the court's lists to the hearings that carry it.
- **Swap:** "where did the widening of the remand gap between defendants with no lawyer of record and defendants
  with one come from" read with a hospital's nouns ("the readmission gap between uninsured and insured patients")
  still parses, but the quantity stops existing: there is no first appearance, no presiding officer to compare
  within, no legally relevant factor set and no duty lawyer whose presence at the call decides whether anyone
  speaks for the defendant.
- **Layer 1:** the appearance extract stamps each call with its New Zealand offset (+13:00 in summer, +12:00 in
  winter) beside a local appearance date; the sitting calendar is a scheduling export with local times as text and a
  courtroom name where the extract has a courtroom code; the duty lawyer returns come as one workbook per financial
  year (July to June) whose column order changed with the 2025/26 claim form; the court is a code in the extract
  and a name in the calendar and returns; the EM bail register moved from a legacy tracker to a case system on 2
  February 2026 and the bail houses' provider from a spreadsheet to a case app on 1 June 2026. Each is produced by
  the system that holds it; nothing is placed to be caught, and none of it touches the decisive comparison.
- **Layer 2:** `estimand_identification`, the right comparison: the within-officer comparison the field makes is
  confounded by the duty lawyer's absence, which follows another list's sitting hours and not the officer; setting
  apart the calls made while that list sat is the comparison under which the officer carries no gap of their own.
- **Decisive step:** each Kestrel Bay custody-list call is read against the sitting calendar's audio-visual remand
  list in courtroom 2 on the same day and the duty lawyer returns' single rostered duty lawyer, so the calls made
  while that lawyer was on the other list are set apart: outside them the community magistrate's gap equals the
  judges', inside them every officer's gap is about 37 points (the magistrate 38.9, the judges 35.7).
- **Not semantics:** no field records the duty lawyer's presence at a call: the extract's counsel field is blank
  alike for a defendant the duty lawyer assisted and one nobody assisted, the returns are a daily total per court
  with no list or defendant, and the audio-visual list is an ordinary list in the calendar; reading every field,
  code and unit correctly leaves the easy route on the magistrate.
- **Not rule application:** no filed rule or procedure sets one list's calls against another list's hours, so
  executing every filed rule (the bid instructions' gap, its years, its counsel-of-record basis) still files a
  judge on the custody list. The enumerated family (pooled before and after against the dated changes; within court
  and officer with the legally relevant controls; the drill by court, list and officer; the weekday-session
  comparison) spreads across EM bail capacity and a judge on the custody list, the within-officer estimate putting
  +23.0 points (SE 2.2) on the magistrate; the standing family (every construction that sets the audio-visual-time
  calls apart, read from the calendar or from the audio-visual list's own appearances, with or without the
  controls) files the duty lawyer roster in 20 of 20 redraws and leaves nothing of the region's 5.9-point widening (-0.2); what
  rules the magistrate out is loud (his gap outside audio-visual time 3.5 against the judges' 2.7, and his own
  term 2.5 points, SE 2.8, once the audio-visual-time calls sit in the same model).
- **Analyst test:** a strong analyst who reads every field and filed rule correctly measures the gap within court and
  presiding officer with the legally relevant factors, finds the widening in the Kestrel Bay morning custody list
  under the community magistrate who took it over in December 2025, and funds a District Court judge on the Kestrel
  Bay custody list; read against the audio-visual list's sitting hours and the single rostered duty lawyer, the gap
  belongs to the calls made while the duty lawyer was in courtroom 2, under every officer.
- **Estimand:** filed once, in section 3 of the region's Budget 2027 bid instructions (Ministry of Justice, Halsey
  Coast region): the share of first appearances from police custody at the region's four District Courts that end
  with the defendant remanded in custody, for defendants with no lawyer of record at that appearance minus
  defendants with one, in percentage points, for the year to 30 September 2025 and the year to 30 September 2026,
  each first appearance counted once on its New Zealand date and every one in either year already decided; the
  initiative put forward is the one that removes the change between the two years.
- **No decoy:** nothing is planted: the EM bail slowdown and the community magistrate's arrival are ordinary
  operational changes with their own records, no memo, briefing or stakeholder figure argues for an initiative, and
  the shortlist states each initiative's scope and cost only.
- **No certified replay:** no certified or published figure in the pack carries the golden's method; the bid
  instructions file the WHAT, and nothing reports a gap by list, officer or hour for a solver to match.
- **Lesson:** a disparity within a decision-maker's list is the decision-maker's only when the conditions of the
  hearings are the same across the lists; when the advocate rostered to two lists sitting at once is absent from
  the hours one decision-maker sits, the decision-maker carries the gap. No build on file reads a disparity against
  the absence of the person who speaks for the case.

## Survivor anatomy

- **Actor:** the deciding property (the duty lawyer was on the audio-visual list when a custody-list matter was
  called) has no column in any file: the extract's counsel field is blank alike for assisted and unassisted
  defendants, the returns are daily totals with no list or defendant, and the calendar lists courtrooms and hours,
  so the property is a relation between a call time, another courtroom's sitting hours and a one-row-a-day roster.
- **Link:** each custody-list call is read against another list's sitting window in the same courthouse on the same
  day, a comparison across two lists bail disparity analysis never asks for; no key joins them (the extract's
  courtroom code KBY-1 against the calendar's "Courtroom 1") and no sentence names the pairing.
- **Reflex:** the field's own method (the disparity within court and presiding officer with the legally relevant
  factors, the rigor card's pattern 4) sits at rung 1 and files a District Court judge on the Kestrel Bay custody
  list.
- **Back-test:** the textbook route validates: the within-officer estimate is large and tight (+23.0, SE 2.2), the
  magistrate's first sitting matches the break in the monthly gap, and the duty lawyer returns show a duty lawyer
  claimed for every Kestrel Bay sitting with unrepresented matters per claimed hour level (4.3 before, 4.6 from
  December 2025), so the duty lawyer looks unchanged.
- **Second use:** every file the decisive step reads sits in the pack for its own reason: the appearance extract is
  the spine every main figure is read from, and the sitting calendar and the duty lawyer returns are the cost bases
  the bid instructions require for the judge line and the duty lawyer line.
- **Shock:** the audio-visual list's arrival is an ordinary list in the calendar and the duty lawyer's day is
  unchanged in its own record; the loud movements are the EM bail slowdown (turnaround more than doubled) and the
  magistrate's arrival, and the audio-visual-time calls are not an interval of any shipped statistic's sort (89 per
  cent sit under the magistrate and 11 per cent under judges, in morning and afternoon sittings, on windows that
  move day to day).
- **Pins:** the WHAT sits once in the bid instructions in the Ministry's own genre (population, outcome, comparison,
  years, unit), and no filed sentence names the duty lawyer's hours, the audio-visual list, a call time or an hour;
  deleting any filed sentence leaves the decisive comparison exactly as unforced as before, so none hands it over.

## Readability screen

| Rung | 1 filed | 2 schema | 3 reflex | 4 control | 5 hygiene | 6 linear | 7 organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 pooled before and after against the dated changes (EM bail capacity) | the EM register's dated switch and slowdown | a month column | the opponent's first group-by | none | no | one difference | no | readable |
| R1 within court and officer with the legally relevant controls, drilled (a judge on the Kestrel Bay custody list) | the instructions' gap definition | the officer column | the field's own method | none | no | one interaction term | no | readable |
| C1 the audio-visual list's first sitting against the month the gap widened (lands on the magistrate: the list and he share 1 December 2025, so the date names both and the within-officer comparison takes him) | the calendar | a list start date | a before-and-after | none | no | one date | no | readable |
| C2 unrepresented matters per duty lawyer hour (names nothing: 4.3 a claimed hour before and 4.6 from December 2025, level) | none | hours in the returns | a workload ratio | none | no | one ratio | no | readable |
| C3 unrepresented first appearances with no duty lawyer service entry, by month (not computable: the returns are sessions and hours, with no defendant) | none | no defendant in the returns | none | none | no | none | no | readable |
| R2 (decisive) the calls made while the audio-visual list sat set apart (the duty lawyer roster) | no clause names a call time, another list or the duty lawyer's hours | no column: counsel blank for assisted and unassisted, returns are daily totals | no named method sets one list's calls against another's hours | no control refutes the magistrate or names the overlap | no battery item reaches it | not one subtraction: a per-call window test across two files and a roster | no: every file it reads carries the spine or a cost base | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "first appearance from police custody" | the case's first appearance, appearing from police custody (extract type "First appearance (custody)") | every appearance from custody, later remand appearances included | same call: the audio-visual-time split carries the widening either way, asserted | the bid instructions' section 3 definition |
| SF2 | "remanded in custody" | every first-appearance outcome that leaves the defendant in custody | only remands after a contested bail hearing | C1: the extract has one custody outcome code, "Remanded in custody", with its next date | the extract's own outcome list and section 3 |
| SF3 | "no lawyer of record" | counsel field blank at that appearance | counsel as at the extract | C1: the extract carries counsel per appearance, asserted | section 3 ("at that appearance") |
| SF4 | the two years | by the appearance's New Zealand date | by the UTC date of the call timestamp | C1: the extract's local appearance date column, asserted against the timestamp | section 3 ("on its New Zealand date") |
| SF5 | "the gap" | share without minus share with, in points | a ratio of the two shares | same call, asserted | section 3 ("percentage points") |
| SF6 | "the widening" | the raw gap in the later year minus the earlier | the change net of the legally relevant factors | same call (5.9 raw, 5.8 adjusted, -0.6 beside the audio-visual-time term), asserted | section 3 ("the change between the two years") |
| SF7 | "courthouse" | where the first appearance was heard | the arresting police district | same call; the extract carries the hearing court only | section 3 ("at the region's four District Courts") |
| SF8 | "called while the audio-visual list sat" | call time inside the calendar's sitting window, start inclusive, end exclusive | the span from the audio-visual list's first to last call in the extract | C1: no custody call within five minutes of a window edge and the list fills its window, asserted | the calendar's times and the extract's calls agree |
| SF9 | "removes it" | the initiative whose cause the widening sits in | the initiative with the most remands avoided at full scale | same call (the duty lawyer roster under both), asserted | section 3 and the shortlist's scopes |
| SF10 | one first appearance per case | each case's first appearance once | one row per charge | C1: one row per case appearance, asserted | the extract's grain |

## Ladder

| Rung | Construction | Names | Figure (seed 3990) | Dies to |
|---|---|---|---|---|
| R0 | the region's gap before and after the dated changes | EM bail assessment capacity | widening 5.9 points (3.6 to 9.5), breaking December 2025 after the EM slowdown of November | no first appearance carries an EM order: EM bail is sought at a later appearance (every EM order in the register links to a second or later appearance) |
| R1 (Ends on) | within court and officer with the legally relevant controls, drilled court, list, officer | a District Court judge on the Kestrel Bay custody list | Kestrel Bay +10.3 against at most +3.3 elsewhere; morning +18.7 against afternoon -2.4; magistrate against judges +23.0 (SE 2.2) | the audio-visual-time split: the magistrate's gap outside audio-visual time 3.5 against the judges' 2.7 |
| R2 (decisive) | the calls made while the audio-visual list sat set apart | the duty lawyer roster | audio-visual-time gap 38.6 (2,714 calls) against 2.9 (6,096); the region's widening 5.9 falls to -0.2 | golden |

- **Position and margins:** the golden is extreme on the decisive split (all of the widening) and absent
  from R0 and R1; R1's within-officer estimate clears zero by 10.5 standard errors, so it is satisfying to stop at.
- **Dominance:** only the decisive move reverses the pick; every correction below it (controls, the drill, a
  weekday-session comparison) keeps the magistrate.
- **Redraws (20 seeds):** the drill lands on the magistrate 20 of 20 (+16 to +26 points); the audio-visual split
  carries at least 71.7 per cent of the widening 20 of 20; Kestrel Bay leads the court drill 19 of 20 (the one miss a
  tie at 10.0 against 10.0); measured on the final world (window settled, no Friday sitting).
- **Pricing sequence:** (1) the residue the filed WHAT leaves is which hearings carry the widening, a method; (2)
  the audio-visual-time calls can produce the move: their excess (38.6 less 2.9 points on 30.8 per cent of Kestrel
  Bay's unrepresented calls, Kestrel Bay 56.4 per cent of the region's) is about 6.2 points, the whole 5.9; (3) the
  one-group-by routes (officer, morning or afternoon, weekday) all name the magistrate, and hour of call names no
  hour because the window moves day to day; (4) the decisive estimate's sampling error is about 2.0 points on 38.6
  and 1.45 on 2.9; (5) the call is a verdict on one initiative far from its boundary (all of it against the half needed); (6)
  and (7) do not apply (no variance correction, no bound rows); (8) no visible attribute isolates the audio-visual
  calls (the officer column catches 89 per cent of them and 20 per cent of the other calls, whose gap is 3.5).
- **Worth in bins:** the decisive split moves Kestrel Bay's year-to-September-2026 gap figures by about 360 bins of
  0.1 point (38.6 against 2.9), and every graded figure sits at least 7 per cent of a bin from an edge (asserted;
  the tightest, May 2026's EM turnaround, at 0.097 of a bin).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | first appearances from police custody at the four courts, each year; filed in section 3, C1 one case a first appearance |
| 2 | Unit of account | the first appearance; filed |
| 3 | Attribution window | the appearance's New Zealand date; C1, the extract's local date column |
| 4 | As-of dating | counsel and outcome as at the appearance; C1, per-appearance fields |
| 5 | Version basis | one extract, no superseded rows in the main population; C1 asserted |
| 6 | Denominator | every first appearance from custody in each group, disposals on the day included; filed in section 3 |
| 7 | Weighting | each first appearance once, pooled within its group; filed ("the share of first appearances") |
| 8 | Window length | the two twelve-month years; filed |
| 9 | Boundary inclusivity | 1 October to 30 September inclusive; filed, C1 on local dates |
| 10 | Rounding path | shares unrounded, the gap rounded once to one decimal; the prompt's last sentence, mid-bin asserted |
| 11 | Tie-break | none needed; the call clears every rival by a wide margin, asserted |
| 12 | Maturity and censoring | every first appearance is decided on the day; C1 |
| 13 | Order of operations | share within each group, then the difference; filed |
| 14 | Row order | none; C1 |
| 15 | Duplicate resolution | one row per case appearance in the main population; C1 asserted |
| 16 | Identity normalisation | court codes, calendar names and return names map one to one; C1 asserted |
| 17 | Netting against gross | none; no offsetting quantities |
| 18 | Dimensional units | percentage points of shares; filed |
| 19 | Code and status semantics | one custody outcome code; the codes that leave a defendant in custody listed in section 3 |
| 20 | Integerisation | none |
| 21 | Clause scope | section 3 applies to every court and both years; filed |
| 22 | Forward window contents | none: the call is retrospective, nothing is forecast |

## Literal reader

Executed word for word, section 3 gives every graded gap (the region's 3.6 and 9.5, each courthouse's in each year,
and the Kestrel Bay gaps at each level below it), and no filed sentence reads to another initiative: the
shortlist states scope and cost only, and the question's "removes it" has one answer once the hearings carrying the
widening are found, the duty lawyer roster under the cause reading and under the remands-avoided reading alike
(SF9).

## Oracles

- The duty lawyer returns confirm on the wrong path that a duty lawyer sat at every Kestrel Bay sitting with a flat
  daily count; they tie under every reading and name no list, so they are no oracle for the golden.
- The sitting calendar confirms the magistrate's arrival on the wrong path and the audio-visual list's hours on the
  right one; it ranks nothing and carries no gap.
- No control, published figure or reconciliation column ties only under the golden.

## Ask sheet

Two asks, each a month-by-month block of twelve cells over the year to September 2026, each with two primaries from
different families on opposite sides of a dated system change, both on files and rows the main call never reads.

**Ask 1, EM bail assessment turnaround by month** (12 figures, average days to one decimal).
- **H18 home and use:** the EM line's cost base (bid instructions, section 5); the regional manager costs the EM line
  on the turnaround the Department's standard defines. Decoupled: EM orders sit on later appearances, never on a
  first appearance from custody.
- **Primary 1 (D8 with D7):** the legacy tracker's Referral date is the day the unit logged the registry's referral,
  0 to 3 working days after the court's order; the order is the extract's appearance whose outcome orders the
  assessment, reached by CRN or, where the tracker has none (15 per cent), by surname, first name and date of birth.
- **Primary 2 (D2):** the case system's ReportFiledDate holds the latest upload, so an order whose report was amended
  (16 per cent) carries the amendment's date; the first filing is the upload log's first report.
- **Hazards:** orders open on 2 February 2026 carried into the case system with that day as their OrderDate and still
  in the tracker as Migrated (joined by their addresses); one row per address (the standard counts an order once);
  the upload log in UTC.
- **Files and columns:** em_bail_tracker_2025-26.xlsx (12), em_case_system_assessments.csv (9),
  em_document_uploads.csv (4), cms_appearances_oct2024_sep2026.csv (the order appearances: CRN, names, date of birth,
  outcome, date), em_bail_service_standard_v3.pdf (the WHAT).
- **Stops (on the cut pack):** rows at face value (the mirror) 8.1 to 22.0 days; orders composed, carried-over rows
  dropped and each system's dates as given (the cracker) 7.8 to 21.2, 8.5 to 57 bins off in every month; the
  legacy lag fixed alone leaves February to September about a day high; the amendments fixed alone leave October
  to January about two days low; the golden 9.9 in October 2025, then 18.6 to 20.5.
- **Pin test:** the standard files the WHAT (order to filed report, calendar days, one assessment an order, the
  order's month, the case system from 2 February 2026); both devices sit in which day each system's date column
  carries, and no sentence states either column's meaning.
- **Realism:** a tracker the unit kept from the registry's emailed referrals, a case system that keeps a document's
  latest date, a migration that carried open records in with the go-live day.

**Ask 2, supported bail house occupied nights by month** (12 figures, whole nights).
- **H18 home and use:** the bail house line's cost base (section 5); the contract pays a rate for each occupied night
  above a house's base. Decoupled: placements and incidents are the provider's records.
- **Primary 1 (D8):** until 31 May 2026 the provider's spreadsheet recorded Left as the working day the exit was
  processed, up to three working days after the resident left; the departure is the incident log's exit (moved out,
  did not return, or taken into custody with no return).
- **Primary 2 (D8 and D3):** from 1 June 2026 the case app's start column carries the day the placement was
  approved, one to four days before the resident arrived; the first night is the incident log's arrival.
- **Hazards:** custody and hospital absences only in the incident log before June and in both the log and the app's
  Away sheet after (a union, never a sum); approved overnight leave only on the Away sheet; the log in UTC while the
  midnight rule is local; dates as text in the spreadsheet's rows and as dates in the app's.
- **Files and columns:** bail_house_register_2025-26.xlsx (Placements 8, Away 4), bail_house_incidents.csv (5),
  bail_support_contract_schedule2.pdf (clauses 2 and 4, the WHAT).
- **Stops (on the cut pack):** register nights as recorded (the mirror) 349 to 442, 22 to 54 nights off; the
  schedule's midnight rule executed on the log with the Away sheet joined (the cracker) 332 to 423, 6 to 28 nights
  off in every month; the golden 326 to 410.
- **Pin test:** clause 4 files the WHAT (a night dated by its evening, occupied when the resident is at the house at
  midnight, custody and hospital nights out) and clause 2 files a placement as the first night to the day the
  resident leaves; both devices sit in which day each system's start and end columns carry.
- **Realism:** an exit processed on the next working day in a small provider's spreadsheet; an app whose placement
  record starts when it is approved.

**Main population zero-counts:** no EM order and no bail-house row touches a first appearance from custody (asserted:
1,878 EM orders, every one on a later appearance); no main-call construction reads an ask file, and deleting both
asks leaves the call exactly as hard.

**Hazard table:** UTC (EM uploads, bail-house incidents; both asks); carried-over EM rows and per-address rows
(ask 1); two absence sources (ask 2). Each moves only its own ask.

**Referee:** the extract's order appearance for EM order dates and the incident log's arrival and exit events; each is
byte-clean and arbitrates without carrying a level of its own.

| Ask | Figures | Cracker kept | Mirror kept | Cracker |
|---|---|---|---|---|
| Ask 1, EM turnaround by month | 12 | 0 | 0 | miss |
| Ask 2, bail house nights by month | 12 | 0 | 0 | miss |

- **Mirror leakage:** 0.0 per cent of ask weight.
- **Pair ceiling:** 31.3 (cracker 45.0 on the call with no ask cell; mirror 17.6, off the call, keeping the default
  path's ten level-one figures of seventeen critical components and no ask cell).
- **Measured by:** generator/ceiling.py, run on the cut pack (target/ from build.py).

## Leak and duplicate review

`leak.py --asof 2026-11-03` on the cut pack: REVIEW, no LEAK. Each REVIEW line, harmless:
- Sweep 3, the bid instructions carry the call's words: the shortlist names all five initiatives on the same
  footing with scope and cost, ranks none and states no figure for any of them.
- Sweep 4, the bid instructions (sitting, appearance, region, Kestrel, calendar, returns), the EM standard (region,
  calendar, records) and the contract schedule (Kestrel, calendar, defendant): the words are each document's own
  genre (the measure's population, the cost bases' named records, calendar days and months); none names a call
  time, another list's hours or the duty lawyer's whereabouts.
- Sweep 9, 137 dates after 3 November 2026 in the appearance extract: the next dates of cases adjourned before the
  pull, which an extract pulled on 2 November 2026 carries.

`guard.py heart`: WARN (overuse.org_family only; task253 v2 and task141 v1 differentiated on the card).
`guard.py surface`: two pairs promoted at 0.101 (corpus top 1 per cent), task461 (a battery spread series conformed
for a cycling threshold) and task131 (a randomised tariff trial); both share only the pdf and xlsx deliverable
pair, answered on the card. Personas in the cut pack: Freya Herd only.

## Tried and rejected

- Seed RC05's own world (a regional distributor's five reliability programmes: animal guarding, recloser firmware,
  trunk vegetation, storm hardening, live-line crews; customer minutes by cause), screened at the draw on 2026-11-03
  before any harness: a screen card in that world ran `guard.py check` (axis BLOCKs only), `heart` (WARN 0.14 against
  task303's stump, the feeder breaker and recloser tickets by vegetation, wind and wildlife) and `slots` on its setting
  nouns (task303 five terms, task132, task183, task201 on outage, feeder, recloser). It collides on world with task129
  (grid-reliability outage root cause, the same subdomain and objective, vegetation and storms among its drivers) and
  task303 (customer-minutes, storm hardening): moved to another client domain, world and dataset (CLAUDE.md, a stuck
  build is unblocked). Its kernel (planned work for want of crews leaves no fault record) is a second register the
  estimand would have to name, which task445 v2 measured as rule application.
- Health equity decomposition of a life expectancy gap by cause (Epidemiology, `health-equity-disparity-decomposition`):
  the field's method (Arriaga by age and cause) is the golden on any honest data and every structural twist found
  (registration delay, denominators, residence at death) is maturity, Layer 1 or the population the estimand files.
- E-prescribing selection slips against look-alike name mistakes read from the search the prescriber typed (Human
  Factors, `safety-incident-error-analysis`): fresh mechanism, but crediting the programmes needs the error modes
  defined, and the sentence that defines a selection slip names what the decisive step recognises (the fork is the
  stump), while leaving it undefined forks on the reporter's contributing-factor tick.
- Sun glare behind signal heads reassigning red-light crashes to signal visibility (Human Factors): the glare set has
  no threshold the physics fixes, the count moves 10 to 40 per cent across defensible windows, and the excess that
  removes the threshold is task121 v3's comparison against the same unit's hours on other days.
- Teacher vacancies covered by long-term substitutes, invisible to the teacher of record (Education,
  `multilevel-classroom-school-research`): the vacancy is read off the substitute system's assignment type, a field
  reading, and the abstraction is the holder at the time.
- Vaccine doses from fridges that froze, read from logger records (Epidemiology): the freezes are the logger file's
  largest anomaly (Shock), and the vaccine incident guidance that invalidates frozen doses is a filed rule.
- A process plant's safety system bypassed during proof tests, turning leaks into large releases (Human Factors): the
  candidate that shortens bypasses tests its own mechanism straight off the bypass log, and every release's initiator
  and the bypass are both but-for causes, a fork on the split.
- The same pension world with the core manager as the naive winner and the currency hedge as the golden (no overlay on
  the list): the decisive step then only deflates the core manager and the golden's figure is the one every route
  computes, so a solver who doubts the core manager for any reason lands the call; the overlay was put on the list so
  the golden's own figure needs the step.
- Architecture 1 itself (Quantitative Finance, `factor-return-attribution`: a manufacturer's pension plan whose
  benefit money, raised by a quarterly pro-rata sale in the core manager's account, waits there as the manager's cash,
  so the core manager looks like the largest line and the cash overlay the smallest), spent at the draw on 2026-11-03
  with a calibrated clean truth (golden overlay USD 12.05 million against the hedge at 7.95; rung 0 the core manager at
  12.12): task398's draw in the same cell had been registered earlier on a branch this guard could not see, and with it
  visible `guard.py check` returned BLOCK on ban.pairing, ban.subdomain, ban.artifact and ban.strategy, and a reviewer
  reads the two as one decision. Its measured lessons carried here: the cost of short-held cash is dominated by the
  market's path on the held days (40 market paths spread the same balance's cost from minus 5 to plus 23 million), and a
  third ask on management fees was dead on supplemental rule 3 (the fee basis is the main call's account values).
- A 911 or ambulance call-taking centre whose breaks were eaten by callbacks (Human Factors): the setting matches
  task148's 911 call-takers and callback desk and task121 v6's call-takers' rest, so a reviewer holds the same room
  twice; moved to bus duties, where the rest is a terminus stand and the operation's own record is the trip log.
- A parcel sortation hub with the same missed-break mechanism: org family logistics_or_3pl is held by task277 (BLOCK
  ban.org_family), and pick and sort accuracy is task277's own quantity.
- Architecture 2 itself (Human Factors, `workload-fatigue-shift-analysis`: Morrowbank Regional Buses, whose drivers'
  terminus stands the duty schedule promised were driven through by late trips, rebuilt from the vehicle location
  records), spent at the draw on 2026-11-03 before any data was cut: the same cell and the same decisive insight as
  shipped task121 v6 (the rest each worker really had, rebuilt from the operator's own records, while the obvious
  candidate is wrong), with nine axes equal to task121 (domain, subdomain, objective, shape 18, Gate G, strategy,
  decision type, question form what, org family); the lexical guard scored it 0.06 and passed it, a template only the
  semantic read catches. No rest, fatigue or time on task may decide this slot again.
- Architecture 3 itself (Product Analytics, `funnel-journey-analysis`: Norland Driver Services' road-test booking
  journey, the search-to-booking fall read against the slot stock rebuilt from releases, bookings and cancellations),
  spent at stage 2 on 2026-11-03 before any data was cut. The pricing sequence's step 3 run as a daily queue harness
  over two years (scratch `a3/harness.py`) under three variants built to hide the binding (the busy centres losing 14
  per cent of slots; the province's releases held flat by rural top-ups; a quarter of slots released four days ahead):
  in every variant two one-group-by routes name the golden at rung 1, releases by centre down about 8 per cent at the
  busy centres and bookings over releases by centre at the ceiling there, while the decisive rebuild put 95 per cent
  of failed searches on an empty stock. The throughput identity (tests sat at a fully booked centre equal its releases)
  makes a binding capacity one subtraction (readability tests 3 and 6; Gate F's two cheap routes), so no honest booking
  world hides it.
- Duty counsel absent on some sitting days, read off the duty counsel log by day (Criminology, the same bail world as
  architecture 4): the initiative "restore full duty counsel coverage" invites the count of sitting days with no
  duty counsel entry, one group-by on the log, and the step is architecture 3's family (a resource's availability at
  the event against its aggregate).
- Video bail hearings recovered from the remand centre's court-escort movements: the initiative names the mode, so
  the solver looks for it and the escort movement type is one join from the hearing; and the dated switch to video is
  itself the before-and-after a solver runs first.
- A legal aid contract concentrating bail work in fewer lawyers, read as their double-booking across courtrooms: the
  per-lawyer caseload by year is one group-by and names the concentration.
- The binding matter across a person's open cases (released on the new charge, held on an old one): task202's note
  measured the holds as a column of every custody extract, and the rule that books a custody day to one matter would
  have to be filed (rule application).
- Failures to appear per scheduled appearance against the lead time each date was set at: a pooled rate over a mix
  that shifted, `composition_mix`, banned in the window by task277, and lead time is one lag a solver enumerates.
- Remand bed-days split into admissions and length of stay (exit-cohort stays shrink while stays lengthen):
  `maturity_censoring`, banned in the window by task274, and Little's law makes the split one division.
- Island ferry cancellations behind a visitor economy's turnover (Economics, panel data): the cancellations are the
  pack's largest anomaly (Shock) and the relief-ferry initiative invites its own check.
- An energy price shock absorbed by a panel's time effects, read through each town's energy-intensive employment
  (Economics, panel data): exposure times the shock is the energy rebate's natural check, and the hedged-contract
  second correction is a column one join away.
- A scoring model's inputs as scored against as stored after a late feed was backfilled (General Statistics,
  interpretability): the cause is a pipeline defect, so the step is Layer 1 carrying the call.
- Vaccine hesitancy measured after the missed dose in a parents' survey (Psychology, mediation): temporal precedence of
  the mediator is the rigor card's own pattern 3, a reflex.
