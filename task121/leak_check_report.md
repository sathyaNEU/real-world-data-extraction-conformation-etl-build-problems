# leak check, task121

**Verdict: REVIEW.** 13 files read, 18 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: household, rendering, landfill, comparison, sessions, address, decisive, compost, valley, orders, procedure, complaint, member, accounts, kestrel, carries, golden, device, harden, identity, schema, second, asserted, report, same-hours

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `cp14_odor_complaint_procedure_rev4.pdf`: carries 11 of 17 distinctive words of the committed call: "Ridgeway Organics' composting facility is behind the 2026 surge in odor complaints in Harlow Falls, and the district sho"

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `complaint_export_fields.txt`: 5 of 25 stump-paragraph terms appear (address, valley, complaint, member, kestrel); read whether the document names the move
- **REVIEW** `cp14_odor_complaint_procedure_rev4.pdf`: 7 of 25 stump-paragraph terms appear (household, address, valley, procedure, complaint, kestrel); read whether the document names the move
- **REVIEW** `hfs_station_readme.txt`: 3 of 25 stump-paragraph terms appear (valley, kestrel, second); read whether the document names the move

## 6 ranking artifacts (REVIEW 1)
- **REVIEW** `odor_source_list_2026.xlsx`: names 6 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `odor_source_list_2026.xlsx`: 5 ISO dates after 2026-10-12, e.g. 2027-01-31, 2027-07-31, 2027-11-30, 2028-02-29, 2030-03-31

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

One isolated Sonnet reader at medium effort per pass, each on a fresh copy of `prompt.txt` and the unzipped `target.zip`, never the design note, generator, submission or this report.

### Pass 1 (the stage 3 pack)

1. Decisive step: none stated. The nearest is the procedure's caution, "An upwind check shows that a source could have reached the household in that hour. On its own it does not show which source did.", which warns that raw upwind counts may not decide and gives no method.
2. Ranking file: none. The operators' reports and the source list each showed one 2026 change per facility and scored nothing.
3. Analyst-only file: the 2019 to 2025 annual totals (a bare year, complaints and households table) and, mildly, the source list's notes. Both are the district's own summaries (the totals are the history the word "surge" is measured against) and state no method; they stay.
4. Answer-like figure: none. The complaint text leans on "dump" and "garbage" (the procedure says a description is not a finding of source) and the rendering plant's July intake jump pulls toward another facility; both are context.
5. Filed sentences: the event, household, time noticed, boundary, hourly wind, calm and upwind check sentences, the station's clock and direction convention and the airport exclusion all execute to the golden's construction; executed literally they give each facility's upwind count, the largest being the landfill, which is the default path the stump rests on (the procedure files no baseline).

Ruling: harmless on 1 to 5. Its forks were closed in the procedure (a usable wind measurement is the wind as the monitor measured it; the hourly wind is the speed and direction of the average vector; calm is an hour with a usable wind below 0.5 m/s; a report that reaches the District more than once is one complaint, which also answers the judge's FIX_NOW) or by convergence (household keys, the two-hour edge and the 30-degree edge, all asserted). Its realism tells were fixed in the generator: descriptions in each complainant's own words, contacts per phone number, e-mail address and app registration in one sequence, eight occasional complainers, the June audit moved off the outage, drying beds at month end, part-month changes in the operators' reports, a permit actions log with administrative actions, a creek-following boundary at six decimals, service gaps in the PM2.5 record and dropped hours and specials in the airport feed. The held-vane zeros under the flag V stay: they are what a logger writes with the vane held or the cable unplugged, and the maintenance log dates them.

### REVIEW lines (leak.py after the repair)

- The procedure carries the call's words because it governs odor complaints and abatement before the hearing board. Harmless.
- The field reference, the procedure and the station readme share the stump paragraph's nouns (address, household, valley, Kestrel) as their subject and name no comparison. Harmless.
- The odor source list names the five facilities beside coordinates, throughputs, expiry dates and permit actions; it ranks nothing on the question. Harmless.
- Dates after the setting: the five permits' expiry dates (2027 to 2030), which lie in the future by nature. Harmless.

### Pass 2 (the repaired pack)

1 to 3: none (the procedure's caution is again the nearest hint; the annual totals read as a supplied baseline). 4: the source list's notes line on Ridgeway Organics' food-waste contracts, the only facility note there, read as pointing at a story. 5: every quoted sentence executes to the golden's construction except the new complaint sentence, which the reader took as one person's reports keyed on the contact (nine duplicates rather than the resends under new app registrations). Its realism tells: the held-vane zeros under the flag V, the audits' monthly cadence and four phrasings, the operators' annotated change months.

Ruling: not repaired. The judge's re-run returned SEND_BACK on the main call the same day, which spends the third architecture, and the number was retired (`DESIGN_NOTE.md`, `## Retired`).
