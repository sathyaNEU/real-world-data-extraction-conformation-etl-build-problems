# FC33 — How many triagers the browser needs in its first quarter on the new tracker, when the parallel run that certified the switch never saw a release week

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Product Analytics · software quality operations |
| Mirrors | Support or triage capacity planned through a tool migration that changes the unit of work (bug-tracker moves at browser and OS vendors, Apple Feedback Assistant intake, Zendesk-to-Service-Cloud cutovers), where the parallel run happened in a quiet period |
| Decision shape | One figure committed at a date: the triage headcount in the quarterly staffing plan, filed before the holidays |
| Committed call | Triagers for the first quarter on the new tracker, as a whole number (the busiest forecast week's triage items ÷ 120, rounded up) |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · L1 with S4 (the parallel run certifies the shallow rungs and is blind to the decisive one), with a suppressed cell bounded (measured #24) at rung 2 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #24 treats an unpublished figure as unknown · #13 validates on one population, applies to another · #2 counts file rows instead of the real unit |
| Calibration form | Parallel-run overlap: four November weeks in which every report was filed in both the old and the new tracker |
| Driving force | The old tracker merged duplicate reports into their bug at filing; the new one files every report as its own triage item. Duplicates are not a constant share of bugs: the old tracker merged 0.67 per bug in the first week after each release and 0.08 in quiet weeks. The parallel run measured 1.08 items per bug and reproduced it in all four weeks, because it ran in the year-end release hold and no week of it followed a release. The quarter's busiest week is a post-release week. |

## 1. Situation

A browser's triage team staffs to its busiest week each quarter, at 120 triage items per triager-week. On 4 January the old tracker is
retired and every report goes to the new one. In November both trackers ran side by side for four weeks. The browser ships on a four-week
train, with releases on 12 January, 9 February and 9 March. Security-restricted bugs are hidden from the public statistics; the internal
triage dashboard publishes weekly totals per product area. The pack holds the old tracker's history, including its merge records, the
public statistics, the dashboard totals, the parallel-run export and the release calendar.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the old tracker's bug and merge records, the public statistics, the dashboard totals and both
  trackers' parallel-run counts. No stakeholder's reading of their own numbers is overturned; the parallel run did show 1.08 items per bug.
  The difficulty is that the parallel run describes weeks unlike the quarter's busiest one.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the tools team's view and every voice. The parallel run still reproduces its own four weeks exactly, and the
  release-aligned bug forecast times that ratio is still the natural build.
* **Instrument repair.** Clean-data test. One file is suspect: the public bug statistics leave out security bugs. Filled from the
  dashboard's totals, rung 0 returns 14, rung 1 16 (rung 2 merges into it) and rung 3 17, none of them 26. The old tracker's bug records
  and merge records are complete, and the rebuild of triage items by release phase is still needed, because no file counts post-release
  triage items: the old tracker merged them at filing and the new tracker has not yet met a release week.
* **Lens swap.** The naive read and the answer count different things at different moments: merged bugs in a release hold, against
  separate reports in the week after a release.

## 3. The driving force

A strong solver aligns the old tracker's bug inflow to the release train, adds the security bugs the public statistics hide by
differencing the dashboard totals, and converts to the new tracker's items with the ratio the parallel run measured. The ratio reproduces
all four overlap weeks to the item. But the old tracker absorbed duplicates at filing: every report of an already-known crash was merged
into its bug, and the merge records keep each one. The new tracker files every report as a triage item. How many duplicates there are
depends on where a week sits on the train. In the week after a release, when a new crash reaches millions of users at once, the old
tracker merged two duplicate reports for every three bugs; in a quiet week, one for every twelve. The parallel run ran in the year-end
release hold, so it measured the quiet ratio four times over. The quarter's busiest week is the week after 12 January's release.

## 4. The ladder

| Rung | Construction | Lands on (triagers) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Same calendar week last year × 1.03, public bugs | 12 (−54%) | The planning model the team has always used | The release calendar: the train moved from six-week to four-week cycles, so last year's weeks sit at different release phases |
| 1 | Release-aligned profile from the last ten cycles, public bugs | 14 (−46%) | Event-time seasonality, the textbook fix for a release-driven series | The dashboard's weekly totals per product area exceed public bugs every week: security bugs are in the queue but not in the statistics |
| 2 | Plus security bugs, recovered as dashboard total minus public count | 16 (−38%) | Every bug the triagers will see, reconciled to the dashboard | The new tracker files reports, not bugs, and the parallel run measured 1.08 items per bug |
| 3 | Bugs × the parallel run's 1.08 items per bug | 17 (−35%) | The switch's own measured conversion, reproduced in all four overlap weeks | The old tracker's merge records: duplicates per bug run 0.67 in the first week after each release and 0.08 in quiet weeks |
| 4 | **Decisive:** triage items rebuilt as bugs plus the duplicates the old tracker merged, by days since release, from its merge records | **26** | — | — |

* **Figure shape.** Every correction walks the figure up and the decisive rung is the largest step, so the answer is the maximum cell
  and every partial build under-staffs the release weeks. Rungs 0–3 sit 54%, 46%, 38% and 35% below it.
* **Partial correction priced (L3).** A solver who finds the merge records but applies the old tracker's average duplicates per bug
  (0.22) flatly gets 19 triagers (−27%). One who applies the release-phase duplicates to public bugs only, leaving the security reports out,
  gets 23 (−11.5%).
* **Grid.** Seasonality (calendar, release-aligned) × security (omitted, recovered) × conversion (none, parallel-run ratio, average
  duplicates, release-phase duplicates) = 16 cells. Every wrong cell sits at least 11.5% below 26; the nearest is release-phase
  duplicates without the security reports, which treats a figure the dashboard determines as unknown.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The new tracker's intake guide says each report is filed as its own issue and triagers link duplicates. No
   document says how many duplicates a week holds or that the number depends on the release phase.
2. **Corpus blind to the decisive quantity.** *In every week of the parallel run the old tracker merged 0.08 duplicates per bug, because
   the overlap ran inside the year-end release hold and no week of it followed a release.* It reproduces the 1.08 conversion in all four
   weeks and cannot see the 1.67 that a post-release week carries.
3. **No arithmetic symptom.** New-tracker items equal old-tracker bugs plus merged duplicates in every overlap week; dashboard totals equal
   public plus security bugs in every week; nothing fails to tie.
4. **Not a row predicate.** Duplicates per bug have to be grouped by days since the most recent release across ten cycles and laid onto
   the Q1 calendar, then added to a release-aligned bug forecast.
5. **The enumeration is arithmetic.** No column says how many items a bug will become in the new tracker; the forward count is computed.
6. **No cutover date in the decisive cause.** The switch on 4 January is dated and filed, and it is the decoy the parallel run answers.
   Duplicate surges recur every release and step nothing at the switch.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The parallel-run export: four November weeks, 1,412 old-tracker bugs and 1,525 new-tracker items, every new item mapped to
  the old bug it was merged into.
* **What it certifies.** Rung 3: items = bugs × 1.08 in every overlap week, and every new item maps to exactly one old bug, so the unit
  change is confirmed and measured.
* **What it is blind to.** The release-phase dependence (above).
* **Twin pair.** Old-tracker weeks 2025-W38 and 2025-W46 each hold 412 bugs with the same component mix and security share. Their merged
  duplicates are 276 and 33 (8.4× apart), so their reports are 688 and 445, because W38 followed a release and W46 sat in a freeze. Only the release-phase rule reproduces both.
* **Resemblance points at the decoy.** By component mix and bug count, the quarter's average week most resembles the parallel-run weeks.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The triage standard: a quarter is staffed to its busiest week at 120 triage items per triager-week, rounded up. The new
  tracker's intake guide: every report is filed as its own issue. The release calendar. The old tracker is retired on 4 January.
* **Empirical pins.** Duplicates per bug by days since release, from the old tracker's merge records over the last ten cycles. The
  release-aligned bug profile, from the same cycles. Security bugs, from dashboard totals minus public counts.
* **Voices.** The tools team lead: "The parallel run told us everything we need to know about the new tracker." The triage lead:
  "Duplicates take seconds; nobody staffs for them." The release manager: "Q1 is a normal quarter on the train."
* **Licensed wrong basis.** The triage standard records that engineering finance funds triage from the public statistics page's bug
  counts and will compare the plan against them.

## 8. Determinism by construction

* **Release profile.** Duplicates per bug in the first week after a release lie between 0.66 and 0.68 in each of the last ten cycles,
  and at 0.08 in every freeze week, so six- or ten-cycle averages agree.
* **Busiest week.** The first full week after each release is the busiest under every construction, and the week after 12 January leads
  the other two by more than 5%.
* **Week definition.** Releases ship on Tuesdays and weeks run Monday to Sunday, so the release week's partial days fall in the same week
  under either alignment.
* **Security.** Dashboard minus public is exact for every week and product area; no week rounds.
* **Rounding.** The busiest week's 3,060 items give 25.5 triager-weeks, mid-way between whole triagers under the standard's round-up.

## 9. Prompt sketch and deliverables

> We switch fully to the new tracker on 4 January, and I have to set triage staffing for the quarter before the holidays. The tools team
> is confident the November parallel run told us everything about the new tracker. Tell me how many triagers we need, as a whole number,
> in one sentence I can put in the staffing plan, and send `triage_plan.xlsx` with the build and the sheets below, a chart
> `q1_triage_items.png`, and a one-page `staffing_note.pdf`.

* `triage_plan.xlsx` — the weekly Q1 forecast, the response-time sheet (ask A) and the fixes sheet (ask B).
* `q1_triage_items.png` — thirteen weekly stacked bars for Q1: public bugs, security bugs, quiet-week duplicates and post-release
  duplicates, with release dates marked, capacity lines for 17 and 26 triagers, and the busiest week annotated.
* `staffing_note.pdf` — the committed headcount and why the parallel run's ratio does not carry to release weeks.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of ten components, the median time from filing to first human triage decision in each
  month of the last quarter. *Device:* crash-signature bots set a triage decision automatically and are logged as triage events under bot
  accounts, which the tracker guide excludes from human triage; counting them understates the time at six components. Response times enter
  no part of the item forecast.
* **Ask B (device-carried).** For each component, the bugs fixed in each of the last three releases. *Device:* a fix uplifted to the beta
  channel carries the beta's milestone, with its original target in the tracking-flag table, as the release guide documents; counting by
  milestone misattributes uplifts at five components.
* **Ask C (validity).** The headcount under each of the five rung constructions, and how many of the four parallel-run weeks each
  construction's conversion reproduces.
* **Decoupling.** Clearing the release-phase duplicate rule changes no figure in asks A or B.

## 11. Rubric arithmetic

10 components × 3 months (ask A) + 10 × 3 releases (ask B) + 5 constructions × 2 (ask C) + the committed headcount, the busiest week and its
item count + 5 named chart parts + 3 files ≈ 81 criteria.

## 12. World-building constraints

* Busiest week (after 12 January): 1,620 public bugs, 216 security bugs, 1,224 merged-equivalent duplicates; 3,060 items.
* Headcounts by rung: 12 / 14 / 16 / 17 / 26; flat average duplicates 19; release-phase duplicates without security 23.
* Duplicates per bug: 0.66–0.68 in each first post-release week over ten cycles, 0.08 in every freeze week; parallel run 0.08 in all
  four weeks.
* The twin weeks are identical on bug count, component mix and security share.
* Bot triage events and uplift milestones touch no bug, duplicate or security count.
