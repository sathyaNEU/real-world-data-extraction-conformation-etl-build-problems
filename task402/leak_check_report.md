# leak check, task402

**Verdict: REVIEW.** 16 files read, 45 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: minutes, overload, section, switching, outage, revision, pairing, device, re-trips, system, changes, decisive, golden, re-trip, comparison, record, sentence, category, redraws, architecture, nothing, generator, window, shipped, mechanism

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `board_policy_407_reliability_work_plan.docx`: 5 of 25 stump-paragraph terms appear (minutes, outage, system, changes, record); read whether the document names the move
- **REVIEW** `reliability_review_fy2026.docx`: 5 of 25 stump-paragraph terms appear (section, switching, system, changes, record); read whether the document names the move

## 8 column names (REVIEW 4)
- **REVIEW** `outage_events_fy2022-fy2026.csv`: columns a generator names and an organisation does not: device_id, device_type
- **REVIEW** `restoration_steps_fy2025-fy2026.csv`: columns a generator names and an organisation does not: device_id
- **REVIEW** `scada_reclosing_operations_fy2026.csv`: columns a generator names and an organisation does not: device_id
- **REVIEW** `system_register_2026-09-30.xlsx`: columns a generator names and an organisation does not: protective_device, device_type

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read (round 1, target.zip f2a3c845)

# Leak read answers (no figures computed, nothing solved)

1. Decisive step: no sentence announces it. The nearest is board_policy_407 s3.1, "the customer interruptions in the fiscal year that would not have occurred without the change, everything else as it was." That states the estimand (a counterfactual), not the method. Nothing in the pack says how to build the counterfactual (comparison group, timing, shared exposure across changes). The reliability review only lists the five changes with dates and scope ("They are listed for costing under Board Policy 407").

2. No file ranks or scores the candidates on the question. The review's indices table (SAIFI/SAIDI by year) is system-wide only. The daily_reliability xlsx is system-wide. No per-change tally exists in any file.

3. Files that exist only to help: none clearly. Distractors by relevance are wholesale_power_bills (not reliability), hq_substation_temperature_hourly.csv, ivr_calls_fy2026.csv (menu_choice FLICKER, OUTAGE), scada_reclosing_operations_fy2026.csv. The latter two are plausibly supports for the momentary-event ask. daily_reliability (two sheets, "Legacy OMS to Feb 2023" and "OMS daily") serves the major-event-day screen. gis_crosswalk (old_section_id to section_id) is a key helper but is a genuine conformation artifact, not an answer hint.

4. No figure or name reads as the answer. The five changes are listed neutrally in the review's s2 table, in no order that signals a winner. The indices table (FY2026 SAIFI 1.563, down from 1.988) is context.

5. Filed sentences that fix population/computation:
- Policy 3.1 (quoted above): fixes the quantity as customer interruptions attributable to each change, counterfactual, within the fiscal year.
- Policy 3.2: "each unplanned interruption record of five minutes or longer, with its customers interrupted. Interruptions on major event days are excluded, major event days being identified under IEEE Std 1366 from the daily SAIDI of the five fiscal years before the review year." Executed literally: count only planned=N records lasting five minutes or more, weigh by customers_interrupted, drop days flagged as major event days by the 2.5-beta method using the five prior fiscal years of daily SAIDI.
- Policy 3.3: "The fiscal year runs from 1 October to 30 September, on the Cooperative's local time." Fixes the window and clock.
- Policy 4: largest cost wins; the 10 percent shared-largest rule hands the choice to the Board (the prompt asks for a runner-up and gap).
- Review s2 "Applies to" column fixes each change's affected population (e.g. "Services connected under the rebate from that date").
- Labor agreement 14.1 to 14.4 and Schedule A fix callout pay (1.5x, 2-hour minimum per callout, 2x on listed holidays, corrections as new entries, rates by class). Review s1: "momentary interruption events per member (MAIFIe as IEEE Std 1366 defines it), all days included".

6. What decides the main answer: an analytical choice. The policy files the estimand but no method, and the changes have different mechanisms (a rule change for connections, a template revision, suspended work lists, an ended programme, a supplier switch), each needing its own counterfactual from the data (list-year comparisons, supplier unit history, rebate load-study field, restoration steps). I found no sentence that tells the solver which route to use. Residual risk: some per-change tasks lean on field reading (rebates load_study blank after 1 Nov 2025; supplier by fitted date) and rule application (the 5-minute and MED screens). These sit inside costing each change and do not by themselves select the winner. Nothing looks planted. No sentence in the pack names the correct route.

7. Realism.
Genuine: board_policy_407 and the labor agreement extract (callout minimums, holiday table, Schedule A); crew_time_overtime (ORIGINAL/CORRECTION entries, APPROVED/REJECTED, a small negative correction hours of -0.23, foreman Monday entry timestamps); outage_events (cause codes EQUIP/TREE/WIND/ANML/UNKN/PLND, section ids F365-2 style legacy); the Legacy OMS vs OMS daily sheets with different units (Cust Hrs, hours vs minutes, "10/1/2020" text dates); rebate terms with a mid-term amendment.
Odd or machine-leaning: (a) outage_events customers_interrupted maxes at exactly 1000, which looks capped. (b) outage_events planned=Y rows carry cause PLND and an OW work order, plausible. (c) Entry ids and call ids are random UUIDs, where a real OMS or timekeeping system would typically hold sequential keys (crew entry_id, ivr call_id, restoration_steps event_id as UUID while outage_events uses LG2102207 style, so the key cannot be joined directly; that may be intended mess). (d) hq_substation_temperature_hourly values in a column "value" with point HQ-TMP-01 look like a historian export, genuine. (e) Review's "Prepared by Kayla Dean" and "Lawrence Reed" are fine. (f) Fixed 130,178 members in every daily row for six years looks static, slightly synthetic. (g) The ivr account numbers appear random 7-digit, fine.

8. Supplementary asks.
- Momentary interruption events per member by district and quarter: "momentary interruption events per member" is defined in the review (MAIFIe per IEEE 1366, all days included), so that settles inclusion of major event days. Residual two-way terms: "quarter of the year" could read as fiscal quarter (Oct to Dec first) or calendar quarter. The prompt says "each quarter of the year" with the year defined as the year to 30 September 2026 and policy 3.3 files the fiscal year, so fiscal is the likelier reading, but no sentence names fiscal quarters explicitly. Also "per member" denominator: district members could be from system_register sections.members (as at 30 Sep 2026) or the single 130,178 figure; the review says "on 130,178 members" for system indices only, and no sentence settles a district denominator (register sections "members" column is the nearest). "Event" could read as each reclosing operation or a sequence-of-operations event; nothing filed defines how SCADA TRIP/CLOSE rows collapse to events (IEEE 1366 convention is only invoked by name). Flag as possible fork.
- Crew callout hours and pay by month: "restoration work" could mean order_type OUTAGE only, or OUTAGE plus others; no filed sentence defines it (order_type has OUTAGE, CAPITAL, SERVICE). "Month" is calendar vs local-time boundary of the callout start/end (a callout spanning midnight or month end); art. 14.2 says a callout runs from start of work to release, travel included, but does not say which month a spanning callout falls in. "Callout hours" (paid hours with 2-hour minimum, vs worked hours in the hours column) is settled in part by 14.1 ("hours worked, with a minimum of two hours' pay"). Corrections (art. 14.4 "A correction is entered as a new entry") and REJECTED status are not settled by a sentence on whether rejected entries count.

## Solver's-eye read (round 2, target.zip af10a74f)

# Leak read, answers (no figures computed, nothing solved)

1. Decisive step. No sentence announces it. Closest is Board Policy 407 3.1: "Each change in the review is costed in sustained customer interruptions: the customer interruptions in the fiscal year that would not have occurred without the change, everything else as it was." That names the estimand (a counterfactual), not the method. The prompt's "Cost every change on the work plan policy's terms" points to it. Neither file says how to build the counterfactual, which comparison group to use, or which change matters. No file names a trap. No other sentence in the pack tells the solver what to do.

2. Ranking or scoring. None. The review's section 2 table only lists the five changes (in place date, scope, recorder), unranked and uncosted. Section 1 gives SAIFI/SAIDI/CAIDI by year, which is context, not a ranking of the changes. Policy section 4 states the choose-the-largest rule, which does not rank anything. No shipped file scores the candidates.

3. Files that exist only to help. Mostly none. Context documents: `heat_pump_rebate_terms_2025-26.docx` ("From 1 November 2025, heat pumps connected under this rebate are connected without a load study.") restates the change's scope and is the one that helps the most, but it also reads as the normal origin of the change. The review's "Applies to" column is helpful scoping. `asset_programme_lists_2022-2026.xlsx` and `transformer_units.parquet` hold the exposed populations (needed). The review's table also tells the solver that the 2026 list was "not fitted", which is a scope statement and not a hint. Likely distractors: `wholesale_power_bills_fy2022-fy2026.xlsx`, `hq_substation_temperature_hourly.csv`, `ivr_calls_fy2026.csv`, `scada_reclosing_operations_fy2026.csv` (the last is probably needed for the momentary ask).

4. Answer-like figures or names. No figure or name reads as the answer. Nothing is flagged, no change is called "the cause", and the review draws no conclusion. The review's wording "to shorten restoration times" for SO-7 and "suspended; the 2025 list not worked" are neutral descriptions. The one thing to check: the review's indices table (SAIFI falling to 1.569 in FY2026, one major event day) is context only and does not point at any change.

5. Filed sentences that fix the figure or population.
- Policy 3.1 (quoted above): the quantity is the customer interruptions that would not have occurred without the change, everything else as it was. Executed literally: for each change, take the fiscal-year interruptions attributable to the change versus the world without it, counted in customer interruptions.
- Policy 3.2: "each unplanned interruption record of five minutes or longer, with its customers interrupted. Interruptions on major event days are excluded, major event days being identified under IEEE Std 1366 from the daily SAIDI of the five fiscal years before the review year." Fixes the unit (OMS record, unplanned, 5 minutes or longer), the exclusion (major event days under the 2.5-beta method on the five prior fiscal years' daily SAIDI), and so the population.
- Policy 3.3: "The fiscal year runs from 1 October to 30 September, on the Cooperative's local time." Fixes the window (local time, so UTC files need conversion).
- Policy section 4: largest cost wins; a tie within 10 per cent goes to the Board. Fixes the selection.
- Review section 1: "Indices are for unplanned sustained interruptions with major event days excluded (IEEE Std 1366), per member on the average number of members served in each fiscal year." and "MAIFIe as IEEE Std 1366 defines it), all days included" fixes the ask-side conventions (momentary events per member, all days, so major days stay in). Review also states "130,325 members at 30 September 2026".
- Labor agreement 14.1 to 14.4: callout is time and a half for hours worked, minimum two hours per callout, a callout runs from start of work to release from the last job including travel between jobs, double time on listed holidays, corrections replace the earlier entry once approved, only approved entries are paid, rejected not paid. Executed literally, these fix the callout hours and pay (approved entries, corrections replacing originals, minimum of two hours per callout, holiday double time, rates from Schedule A).

6. What decides the main answer. An analytical choice: costing each change against a counterfactual (the right comparison population or control for each change, handling of the exposed set, the major event day exclusion and the OMS split at March 2023, etc.). Policy 3.1 supplies the question, not the method. Nothing I can see makes it a single field reading, a stated rule to execute, or a planted item. The pieces that could read as rule execution (major event days, 5 minute cutoff, local time) are all stated in 3.2 and 3.3 and are inputs, not the stump. Nothing reads as planted. One caution: the review's "Applies to" column plus the rebate terms and the programme lists make the exposed sets easy to find, so the difficulty has to sit in the counterfactual, and no file gives a ready-made control.

7. Realism.
Reads as genuine: `daily_reliability_fy2021-fy2026.xlsx` (legacy hours-based sheet to Feb 2023, then OMS minutes sheet, different column names and units, text-formatted dates in the legacy sheet), `crew_time_overtime_fy2026.csv` (GUID entry ids, ORIGINAL and CORRECTION entries, APPROVED/REJECTED, same job times for the crew), `labor_agreement` extract (Article 14 wording, Schedule A rates), `outage_events` (device types FUSE/SECT/RCLR/XFMR, cause codes including UNKN, planned flag), the review docx and Policy 407 (short, plausible), `scada_reclosing_operations` (TRIP/CLOSE pairs with ms timestamps in UTC), the IVR CSV.
Reads as machine-made or odd:
- `heat_pump_rebates_fy2024-fy2026.xlsx`: accounts are plain 7 digit numbers and meters random 8 digit ids (`'M60780459'`, account `3248875`); transformer keyed `'T-823117'` with a hyphen while other files use `T823117` (imperfect-key mess, plausible but uniform). rebate_id jumps (HPR-03346 then HPR-03348) is fine.
- `system_register`: section ids `S58880` and transformers `T304667` are random five and six digit numbers with no feeder structure (the old IDs `F011-1` do have it); `transformers.members_served` values 6 to 10 per transformer look uniformly random; a section of 198 members with 124 electric heat reads as constructed (electric_heat_members is a flat share per district).
- `outage_events`: event ids `LG2103543`, `LG2103545` step by 2, suspiciously regular; planned flag Y for 577 rows against 567 PLND cause codes (small mismatch, could be genuine mess). 
- `legacy` sheet: Cust Served constant (122557) for a long stretch with no daily change, unlike the OMS sheet that moves daily.
- `asset_programme_lists`: fitted/replaced dates look like uniformly spread dates (all January 2022 for the 2022 guards, all October for risers), plausible for a programme.
- `crew_time_overtime`: three crew members of different classes share identical start and end times to the minute on a work order; plausible for a crew.
- `transformer_units.parquet`: supplier prefixes `HE`/`DT` serials, plausible; the parquet format itself is unusual for a coop's records but fine as an export.

8. Supplementary asks, ambiguity.
- "momentary interruption events per member in each district for each quarter of the year": terms are settled by the review ("MAIFIe as IEEE Std 1366 defines it), all days included"), except "per member" has two denominators: average members served (the review uses "the average number of members served in each fiscal year") versus the register's members at 30 September 2026 ("The system register counted 130,325 members at 30 September 2026"), and the district denominator, where the register carries section-level `members` by district, is the only district-level source (quarter-level members are not filed). The review's sentence for indices is written about sustained indices and the district scorecard sentence says "per member" without naming average or year end members. Also "quarter of the year" could be a fiscal quarter or a calendar quarter; the prompt says "each quarter of the year" and "the year to 30 September 2026", and policy 3.3 gives the fiscal year, which settles it for a fiscal reading, though no sentence defines a quarter. A "momentary event" (reclose sequence versus each operation, and one event per TRIP/CLOSE pair or per circuit-breaker or recloser operation) is not defined in a filed sentence I can find; the IEEE reference is the only settler, and the SCADA file carries TRIP/CLOSE rows only, so grouping TRIP/CLOSE operations into events could be read two ways. I flag this as the weakest term.
- "crew callout hours worked and the callout pay for restoration work in each month": "hours worked" versus hours paid (the two hour minimum, 14.1) is settled by 14.1 ("for the hours worked, with a minimum of two hours' pay"), and 14.2 settles what a callout runs. "Restoration work" is the open term: the order_type column holds OUTAGE, CAPITAL, SERVICE, and pay_code CALLOUT vs OT-SCHED. No filed sentence says restoration work equals OUTAGE orders; a reader may take it as order_type OUTAGE with pay_code CALLOUT. "Each month" is local calendar month (time in the file is local without zone). Corrections and rejected entries are settled by 14.4 ("replaces the earlier entry", "an entry the foreman rejects is not paid"). Holiday pay is settled by 14.3 and Article 18. The pay for which hours (minimum applied to a callout of several jobs) is settled by 14.2, though the unit of a callout across several entries is only implied.

## Coordinator's ruling on round 2

- Questions 1 to 6 clean: no decisive-step sentence, no ranking or helper file, nothing reads as the answer, the deciding
  step analytical.
- Realism tells measured on the cut and not found: members per transformer run 1 to 23 with the mode at 8 and 9; the
  electric-heat share runs from 0.02 to 0.85 inside every district; outage event ids step by 0 to 5.
- Ask readings settled by the round 2 judge's recompute (all 40 ask figures reproduced): restoration work is the OUTAGE
  orders at face value (no SERVICE or CAPITAL order carries an outage record); MAIFIe events are reclosing sequences
  under IEEE Std 1366; the register's district members are the only district-grain count; fiscal and calendar quarters
  are the same four blocks of the year.
