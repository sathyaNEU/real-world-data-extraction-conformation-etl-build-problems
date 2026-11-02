# task487 determinism check, re-check under the new gates (2026-11-02)

Two isolated judge threads (sonnet, medium) on the repaired cuts; the shipped zip 3556c4e7 is unchanged on the portal and in the repo.

- Pass 1, zip 3568be1c: NOT_DETERMINISTIC, SEND_BACK, on Schedule B only (contract repair day; survey sessions). Main call forced, band C, CAD 171,000; Gate G method_or_model_selection; Gate H pass.
- Pass 2, zip 74e32011 (Reference values name the field ticket; directive 5.2 defines a survey; 3.1 files the per-event unit and clock): NOT_DETERMINISTIC, FIX_NOW, on Schedule B only (contract repair day; the July run change on R06 and R10 H2). Main call forced; survey sessions, Received in tracker, the clock, BT-0907 closed; Gate G statistical_rigor analytical; Gate H pass.

## Pass 2 verdict

# Determinism verdict, task487 (run r2)

**Verdict:** NOT_DETERMINISTIC (ask 2, Schedule B). The main recommendation (band C, levy CAD 171,000) is forced and the main figure reproduces within 0.3 t. Schedule B reproduces exactly (24 of 24 cells), but only under one reading of the repair day that no shipped file states. The literal reading gives a different Schedule B in all 24 cells.

**Disposition:** FIX_NOW. One filed sentence pins the repair day of a contract order (the WHAT, not the HOW). A second sentence pins the route attribution of the 12 batteries that changed route in early July. The data, the main call and every figure stay frozen, and the judge is re-run once.

## Why
Directive 5.2 vents a leak "until the start of the day it was repaired". The only repair date in the pack is `maintenance_work_orders_2026.csv` column `Completed`. The tracker's `Closed` column carries the same dates. Read word for word, a contract order is repaired on its `Completed` day.

The golden instead dates the 251 Brantham orders (`Vendor` filled, `Reference` = "Field ticket YYMMDD-NN") on the ticket day encoded in `Reference`. Nothing in the pack says that `Completed` is a foreman's approval date, or that the ticket number encodes the work date. The `Completed` dates of these orders fall on the 10th of the month after the ticket month, or the next working day (day-of-month counts 10: 311, 11: 8, 12: 30, 13: 14). That pattern, plus 8 re-check sessions that fall inside a ticket-to-Completed gap, supports the golden by inference only. The in-house orders ("EHS yymmdd-nn") are the opposite case, because their `Completed` is the repair day and their `Reference` date is not. A literal reader is not told which column to trust for which vendor.

Taxonomy label: answer_contradicts_files for ask 2 (underspecified_objective as the alternative label). Gates A, B, C and E fail on ask 2 only.

## Evidence

### Main figure (recomputed from the pack)
| Item | Result |
|---|---|
| Events | 1,660 = 1,425 hatch, 58 combustor, 177 relief. Reproduces. |
| Visit windows | Route app (27,082 rows) plus check-in app (28,615 rows) joined through `checkin_app_sites.csv`. 423 June double-logged visits taken once. 1,019 re-entries (gap 1 to 6 min; nothing between 6 and 30 min) merged. |
| Events matched to a visit | All 1,660 once BT-0907 is read as BT-0907A (`battery_register_20270108.csv` column `former_battery`). 2 events (the July BT-0907 ones) match no visit otherwise. |
| ALARM starts | 54 relief events at telemetered batteries (register `tank_pressure_telemetry` = Y). The last ALARM before the find, on the RTU clock embedded in the message, is always the lift that did not reseat (its NORMAL value is about 0 kPa, against 12 to 16 kPa for routine lifts). Using journal time instead of RTU time moves the total by 0.0002 t. Using the first alarm in the window instead moves it by 0.4 t. |
| Tank vapour methane | Oil production (`battery_daily_production`) times flash GOR times C1/100 times 0.6785, using the latest analysis on or before the day (`tank_vapour_analyses`, BT-0907 mapped). Reproduces. |

Release-event methane for the other 1,606 events depends on the expected-start rule:

| Expected start rule | Total (t) | Band | Levy (CAD) |
|---|---|---|---|
| Previous departure | 87.5 | E | 360,000 |
| Midpoint of window | 45.1 | B | 115,200 |
| Per-kind fit with a share at departure plus an hourly rate (linear and exponential forms, window end at find or arrival, with or without December windows, H1-only or H2-only windows) | 53.2 to 54.9 (central 54.2 to 54.3) | C | 171,000 |

- **Fit evidence:** the hatch fit (share at departure 0.0087, rate 0.00063 per hour) is worth a log-likelihood of 47 over a constant-hazard fit. The hatch event rate per hour falls with window length, so the intercept is in the data. The combustor and relief shares are not significant, so those two kinds start mid-window.
- **Selection criterion:** the data separate the candidates, but the fit and its selection criterion are not filed. Directive 3.2 says only "expected value given those records". This is acceptable here because the data separate the candidates and the band is stable across every fit variant tried.
- **Residual:** my best fit gives 54.2 t, not the golden 54.5 t, a 0.3 t gap. The band and the CAD 171,000 levy hold. The event-level `start` and `methane` values for the 1,606 EXPECTED rows cannot be matched to the minute by independent fits.
- **Levy:** 180 batteries (the 2027 register lists 180 Active rows; BT-0907A is the former BT-0907). The levy is 950 x 180 = CAD 171,000. Reproduces.

### Schedule B
I rebuilt the leak list under the golden's conventions and got every one of the 24 route-by-half cells exactly (for example R01 8.8/7.8, R04 11.2/11.1, R10 12.3/7.8). Total 103.8 t in H1 and 61.8 t in H2. The conventions are:
- surveys are the 540 sessions with at least 100 points; the 318 sessions with 2 to 20 points are re-checks;
- a tag goes to the last survey on or before its `Received in tracker` date;
- a re-tag of a component that was not yet repaired is the same leak, at the first-found rate;
- the repair is the last work order naming the tag, with a contract order dated on its field-ticket day;
- the leak runs from the last survey before first found, clipped to 2026 and split at 1 July;
- each half is carried by that half's run, from the route app to 30 June and the check-in app from 1 July.

| Fork | Literal reading | Effect on the 24 cells | Forced by files? |
|---|---|---|---|
| Contract repair day: `Completed` vs ticket day in `Reference` | `Completed` | All 24 differ, up to 1.3 t (H1 108.6, H2 68.9) | **No. Open fork.** |
| Repair = tracker `Closed` (first repair) | tracker `Closed` | 23 of 24 differ, up to 1.1 t | Closed by the work orders' text "... did not hold" (36 tags), so last repair is forced. |
| First repair vs last repair | first repair | 9 of 24 differ, up to 0.6 t | Same as above. |
| Re-check sessions counted as surveys (for the start) | all sessions | All 24 differ, up to 4.7 t | Closed by directive 5.2 ("screens every component") and by `PointsScreened`: 2 to 20 vs 100 to 410, nothing between. |
| `Received in tracker` read as the survey date | survey date | start moves | Closed. The rule "last survey on or before Received" reproduces `LeaksTagged` for all 540 surveys (0 mismatches), with a lag of 0 to 4 days. |
| BT-0907 treated as a separate battery | separate | 1 cell, 0.3 t | Closed by `former_battery` in the register. |
| Route when 12 batteries move on 2 and 3 July | whole half to the new run (golden) vs split at the first new-run visit | 2 cells (R06 H2 4.0 vs 4.1, R10 H2 7.8 vs 7.9) | **Minor open fork.** R10 H2 raw is 7.8497 t, so 0.3 kg decides its rounding. |
| Register `route` (2027) instead of the 2026 logs | register | 12 batteries wrong | Closed. The register is dated 8 Jan 2027 and 12 batteries changed on 4 Jan 2027. |

### Other probes
- **Clock:** directive 1 states UTC-7 to 02:00 on 8 March 2026, UTC-6 after, no fall-back. Check-in and register times carry -06:00. The effect on the relief starts is below 0.001 t.
- **Distractors:** `hauler_load_tickets_2026.csv`, `sales_gas_meter_statements_2026.xml` (sales-gas methane mol% is not the tank-vapour fraction) and the register's `Entered` column are unused and consistent with that.

## Files/Hygiene
**PASS.** There are 14 files in 6 formats: 1 PDF, 3 XLSX, 8 CSV, 1 JSONL and 1 XML. One file is above 25,000 rows (production 68,760 rows; also route visits 27,082 and hauler tickets 26,496). The other files read as system exports (mixed ISO and local timestamps, a renamed battery, backfilled SCADA alarms, re-entries). There is no README or authoring text. Dates are coherent with a 31 March 2027 filing. No public-data contamination and nothing exclusion-level. Real-world facts are absent from the pack, as the brief intends.

## Stump power
Strong. The easy routes are the window midpoint (band B, CAD 115,200) and "every hatch starts at the previous departure" (band E, CAD 360,000). Only a fit over all windows, including those with no event, shows the share starting at departure and lands band C. A strong model reading everything correctly still lands B by taking the midpoint, so the stump does not rest on cleaning or on a rule.

## Stumping type
`mechanism: statistical_rigor (interval-censored onset estimation from inspection windows)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported number is wrong, and on clean data the task still stumps (the estimand choice remains).

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- **Domain:** swap test fails to read the same, because OGI and PVRV surveys, flash vapour and the board's levy bands are the field's own work.
- **Layer 1:** two apps with a June overlap and re-entries, BT-0907 renamed to BT-0907A, SCADA alarms backfilled after comm failure, UTC against local time, route reassignments.
- **Layer 2:** the expected onset of an event known only to a visit interval.
- **Easy route:** midpoint start gives 45.1 t, band B.

## Fix
`prompt` or a filed pin, with no change to the data:
1. File the repair day of a contract order: "a contract order's repair day is its field ticket's day, not the day it was marked completed" (pins the WHAT).
2. File the route attribution: "a battery counts to the run that visited it in the half" or "to the run on the day". Either one closes the 2-cell fork. The R10 H2 cell sits 0.0003 t from a rounding edge, so pin the convention and re-assert the cell.
3. Optionally record the fit family (share at departure plus hourly rate) as a filed selection criterion. The band is already stable across fits, and the event-level `start` and `methane` columns are only gradable in aggregate.

## Pass 1 verdict

# Determinism verdict: task487 (run r1)

Method: only the 14 shipped files were read. Everything below was recomputed from them (pandas, scipy, pdftotext, openpyxl). Scratch code is in /tmp/determinism-check-task487-r1/work/.

- **Verdict:** NOT_DETERMINISTIC (the main recommendation is forced by the data; supplementary answer ask 2, Schedule B, is not)
- **Disposition:** SEND_BACK. The repair is small and freezes the main call, the stump and the ladder. Close the Schedule B forks (below) with a sentence in the prompt or a restored exports-notes file, then re-ship; a model rerun is required because solvers see the change.
- **Why:** The golden's Schedule B (all 24 route-half cells reproduce exactly) holds only under two readings that no shipped sentence, header or file states:
  1. A contract (Brantham, `FT yymmdd-nn`) leak repair is dated by the yymmdd inside `Reference`, not by `Completed`.
  2. The 318 survey-log rows with 2 to 20 points screened are not surveys, so they do not set a leak's venting start.
  Read literally (`Completed` is the repair date; every row of ldar_surveys is a survey of the battery), every one of the 24 cells moves. Gates B and C fail for ask 2. Governing label: **answer_contradicts_files**.

  The main recommendation (band C, 54.5 t, CAD 171,000) is data-forced, not text-forced (Gate C below), and survives every reasonable variant I ran.

## Literal reading first (what the text says, where it is silent, what each reading gives)

| Item | Text | Silent on | Literal readings and result |
|---|---|---|---|
| Event start, undated (s.3.2) | "the return takes the start at its expected value given those records" | the start distribution | (a) midpoint of window: 44.8 t, plus 0.3 t for alarm starts, about 45.1 t, band B, CAD 115,200. (b) previous departure: 88.8 t, band E. (c) found time: 0.6 t, band A. (d) estimated from all 2026 windows (a share starting as the previous visit left plus a rate per hour): 54.2 to 54.5 t, band C. Only (d) uses "those records". Hatch intercept LR test = 108 (p about 1e-25), so the data separate (d) from (a). |
| Relief valve start where telemetered | "starts at the tank pressure alarm at which it lifted" | which of several alarms; journal or RTU stamp | Last ALARM before the find, with the post-lift NORMAL near 0 kPa (stuck open) versus about 15 kPa (reseated). Chatter inside the lift spans seconds to minutes. Journal versus RTU stamp differ by at most 209 s on the 54 events. Effect on tonnes under 0.01 t. |
| Hourly flow (s.3.3) | oil × latest analysis GOR × C1 × 0.6785, "spread evenly over the day's 24 hours" | nothing material | C1 sums to 100 on every analysis, so no normalisation fork. HoursOn is explicitly not used. |
| Clock (s.1) | UTC-7 until 02:00 on 8 March 2026, UTC-6 after, no fall-back | nothing | Applying fall-back on 1 November moves the total by +0.009 t. Constant UTC-6 moves it by -0.009 t. Immaterial to the band. |
| Levy base (s.4) | "each oil battery the licensee holds at the start of the year" | BT-0907 and BT-0907A | battery_register_20270108 lists 180 Active batteries and shows `former_battery` BT-0907 on BT-0907A (renamed 17 Aug 2026 in the production file). 180 × 950 = CAD 171,000. Counting the old id as a battery gives 181 and CAD 171,950, but the register itself excludes it. |
| Leak (s.5.2) | found by an "OGI survey of the battery"; "a later survey that finds it again before it is repaired has found the same leak"; vents from "the start of the day of the battery's last survey before it was first found" until "the start of the day it was repaired" | what counts as a survey; what the repair date is; how the tracker date relates to the survey | See Schedule B forks. |

## Recomputation ledger

| Value | Source | Result | Reproduced |
|---|---|---|---|
| 1,660 events (1,425 hatch, 58 combustor, 177 relief) | release_event_register_2026.xlsx, kind from the Event text | 1,660 / 1,425 / 58 / 177 | yes |
| Each event matches exactly one visit (1,646 inside the visit; 14 a few minutes before arrival; BT-0907A mapped to BT-0907; no visit holds two events) | route_app_visits csv and checkin_app_visits jsonl, after taking the 430 June visits logged in both apps once and collapsing check-in re-entries under 10 min | 1,660 of 1,660 | yes |
| 54 ALARM-started relief events | the 64 telemetered batteries in battery_register; scada_alarm_journal (UTC, RTU stamp in the Message) | 54 relief events at telemetered batteries, each with a stuck-open lift in its window | yes |
| Release-event methane | linear MLE fit p = a + b·w per kind over all 2026 windows (51,981 windows); expected start = previous departure + (b·w/(a+b·w))·w/2; alarm starts for the 54; production, GOR and C1 as s.3.3 | HATCH 47.07, COMBUSTOR 2.39, RELIEF 5.02, total **54.47 t = 54.5 t, band C** | yes |
| Levy | 950 × 180 | CAD 171,000 | yes |
| Fitted parameters | same fit | hatch a = 0.00862, b = 0.000608/h; combustor a = 1.4e-4, b = 3.1e-5; relief a = 2.2e-4, b = 1.0e-4 | n/a |
| Schedule B, 24 cells | tracker tags placed on the last full survey on or before the Received date; same leak merged; repair = last WO naming the tag, contract orders on the FT date; start = start of the day of the previous full survey; clipped to 2026; split at 1 July; route per half from the route app (to 30 June) and the check-in app (from 1 July) | all 24 cells equal the golden to one decimal (R01 8.8/7.8 through R12 5.7/4.8); totals 103.8 and 61.8 t | yes, under the golden's readings |
| Tag placement check | 802 tags placed on survey sessions, compared with `LeaksTagged` | all 540 full sessions match their tag counts exactly; the 318 short sessions tag 0 | yes (this closes the "Received in tracker" fork) |

## Fork resolution

**Main call.**
- Midpoint starts give band B and previous-departure starts give band E. The data prefer the golden's share-plus-rate form, so band C is forced by the data.
- Band C survives every variant I ran: linear 54.47, exponential-hazard form 54.25, pooled fit 54.24, H1-only 53.3, H2-only 55.4, daily-visit batteries only 53.3, windows over 100 h dropped 54.09, combustor-only windows 54.4. All sit inside [48, 60), which is the Gate C "thin-but-clean" case.
- Residual risk is solver competence, not ambiguity: a solver who never tests event rate against window length files 45.1 t, band B. That is the analytical stump.

**Fork: "Received in tracker".** It trails the survey by 0 to 4 days (562 tags same day, then weekends). Placing each tag on the last full survey on or before that date reproduces `LeaksTagged` on all 540 full surveys. Forced.

**Fork: survey-log sessions.**
- 540 sessions screen 118 to 410 points. Every battery has exactly three, with a consistent point count per battery, one in 2025 and two in 2026.
- 318 sessions screen 2 to 20 points and tag nothing.
- Nothing in the pack labels the short sessions as re-checks of repaired fittings.
- Counting them as surveys moves all 24 cells, up to 4.7 t (totals 87.5 and 50.0).
- The data separate the groups cleanly, but nothing says the 318 short rows are not "surveys". Open for ask 2.

**Fork: work orders' Reference and Vendor.**
- All 712 Brantham orders carry `Reference` "FT yymmdd-nn", and all complete on the 10th of a month or the next working day (a batch-approval pattern). The embedded date precedes `Completed` by 10 to 42 days.
- The tracker's `Closed` equals `WO.Completed` for 363 of 363 contract-tag links, so every record says repaired on `Completed`.
- No file says "FT" means a field ticket, that the ticket date is the work day, or that `Completed` is an approval date. The FT reading is a real-world inference.
- Using `Completed`: 24 of 24 cells change, up to 1.3 t (totals 108.6 and 68.9).
- Rechecks fall between the FT date and `Completed` only 8 times for 251 contract repairs (about 31 expected by chance). The little evidence there is points weakly toward `Completed`.
- **Open fork, material for ask 2.**

**Fork: BT-0907 versus BT-0907A.** Closed by the register's `former_battery`. Production, tank analyses, surveys and visits all bridge on it.

**Fork: Schedule B routes.** The 2027 register routes differ from the visit routes for 24 batteries, and using them moves all 24 cells by up to 4.9 t. The prompt says "the batteries it ran" in each half. The visits give one route per battery per half, and the check-in rows from 4 January 2027 are outside the year. Closed enough by the prompt wording. The merge rule (s.5.2) is filed and is forced.

**Schedule A row-level figures.**
- Ask 1's "Board's schema" column set (battery, kind, start, closure, methane) comes from s.3.1 only.
- The golden also carries find, active hours and start basis. Time zone, time format, kind labels and the methane unit per row (kg or t) are not pinned.
- The headline 54.5 t depends on the estimator form: linear 54.47 gives 54.5, the exponential form gives 54.25 (54.3). The band and levy do not move.
- Per-row starts for the 1,606 expected-value events differ by tens of minutes between estimators.
- A tolerance-based grade is needed; a cell-exact match on `start` is not determinate.

## Gates
- **A:** Pass for the main call. Pass for Schedule B under the golden's readings (all 24 cells reproduce). Ask 2's figures and the solution steps are consistent. SOLUTION_STEPS cites "the foreman approved tickets", a fact found in no shipped file.
- **B:** Fail for ask 2. The FT semantics, and the status of the 318 short sessions as non-surveys, are absent from the pack. The pdf, xml, tracker and register carry no such statement (docProps checked).
- **C:** Fail for ask 2 (forks above). The main call is uniquely forced by the data.
- **D:** Pass. Difficulty is analytical for the main call. Ask 2's split would be from interpretation, which is a defect for that ask.
- **E:** Main ask is unambiguous. Ask 2 is pinned on units and rounding. Ask 1's file schema is under-specified (above).

## Files/Hygiene
**PASS.**
- 14 files in 5 formats: csv ×8, xlsx ×3, pdf, jsonl, xml.
- The largest file has 68,760 rows (battery_daily_production).
- Two distractors are visible: sales_gas_meter_statements_2026.xml (sales-gas methane mol%) and hauler_load_tickets_2026.csv (event hazard per hour is the same with or without a hauler ticket in the window).
- Realistic noise is present: mixed time formats in the register (naive local, then ISO with -06:00 from July), two visit apps overlapping in late June, geofence re-entries, a renamed battery, buffered alarms after comm failures (journal lag up to 25,000 s), two labs, contractor batch dates.
- No README, authoring language or tool banners. xlsx docProps creators read EHS Office, Quellmark Laboratories and Production Engineering.
- Temporal coherence is fine: the tracker is dated 12 Jan 2027, the register 8 Jan 2027, the meter statements issued 11 Jan 2027.
- Provenance is not exclusion-level. The field-definition notes are absent by design; that absence causes the Gate B/C findings for ask 2.

## Stump power
Strong for the main call, for an analytical reason. A strong analyst who cleans the data and reads every rule will take the midpoint of each window and file 45.1 t, band B, CAD 115,200 (previous-departure starts give 88.8 t, band E). The data show a hatch intercept (event rate 0.7 to 1.2% in windows under 8 h, against 0.2 to 0.5% under uniform starts), which the midpoint approach misses. Ask 2 also bites hard (every cell sensitive to the contractor-date, short-session and merge readings), but for interpretation reasons, not analysis.

## Stumping type
`mechanism: method_or_model_selection` (interval-censored start estimation), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported numbers are correct, and the difficulty is estimating the undated starts from the windows, where the easy midpoint gives band B. Gate G passes.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Swap test: passes. Estimating vent-start timing for open thief hatches from visit-interval data is emissions-inventory work and does not read the same with another field's nouns.
- Layer 1: UTC against local time with no fall-back, two visit apps, a battery rename, contractor batch dates, a tracker lagging surveys.
- Layer 2: estimating the undated start distribution from all windows, with a share starting at departure.
- Easy route: the midpoint start, giving band B and CAD 115,200.

## Fix
- **Location:** prompt, or input_files if the notes file is restored.
- **Change:**
  1. State, for contract work orders, which date is the repair day: "a contract order's repair is on the day on its field ticket". This files the WHAT. Alternatively restore the exports' notes defining `Reference` and `Completed`.
  2. State that only sessions that screen a battery's points count as surveys (or label the short rows as re-checks).
  3. Pin the CSV column names, time zone and per-row methane unit, plus a tolerance for the expected-start estimator.
- The main call, ladder, stump and graded 54.5 t / band C / CAD 171,000 stay frozen.
- Re-judge once after the fix.
