# Exemplars: Economics

> 10 accepted tasks in this domain, sorted by the current model's measured mean, lowest (hardest) first. Each is the client's own record. Index and the shared architecture: `index.md`.

## Report 11,667 Stalls traded at member markets in the year to 31 march 2026

**Retail Market Activity Measurement**, Batch 14, Economics, model mean **0.21** over 4 runs (0.26, 0.22, 0.26, 0.26).

### What makes it strong (the client's note)

The trap is the unit of count: one letting per stall gives 16,197, the licensing statement's traders give 8,614, and neither is a stall.
The unit is recovered from last year's paper: counted on the federation's convention (neighbouring trading lettings on one line of the market's own pitch numbering that share a day pattern, a goods class and the first word of the trading name form one stall), the 2024-25 extract gives 10,918 stalls and, at two collections a stall capped at 60 a market, reproduces all seventeen printed figures of Table 3, including the 79 markets at the cap. The licensed-trader basis reproduces two.
The computation chain: parse each market's numbering scheme (consecutive, odd and even, or block and number), drop 917 vacant and 927 casual lettings, join neighbours into stalls, then split, profile and compare with 2024-25.
Determinism pins: 11,667 stalls (8,211 of one letting, 3,456 of two to four); South East 2,324 the most and London 821 the fewest; General 7,557, Farmers 781, Specialist 1,531, Covered 1,798; up 749 (6.9 per cent) on 10,918; 8,062 collections a week with 87 markets at the cap.

### Stakeholder ask (the prompt, verbatim)

Subject: High street vitality paper - the stalls figure

The paper is the Council's one look a year at how the high streets our member markets stand on are faring, and the stalls figure is the measure it turns on: how much market trading those high streets carried in the year, and whether it grew on the year before. I need one determination for it: the number of stalls that traded across our member markets in the year to 31 March 2026, stated as a single figure on a stated basis. That figure is the answer, and the rest is its support: the same count by region and by market type, the profile of what is sold and on which days, the servicing load, and how the year compares with the one before. The pitch letting extract, the market list, the trader list, the goods class and day pattern lists, the waste round standard, the reporting standard, last year's vitality paper, the published licensing statement and my extract note are in the supplied files. Show the supporting calculations in a workbook the market managers can re-run the count from, with a short note to the federation's council stating the figure and how it was counted, and one chart by region.

### Deliverables

 (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer. Stalls trading 2025-26 (vitality paper).xlsx Stalls trading 2025-26 by region.png Stalls trading 2025-26 note to Council.pdf)

### Input files (A federation of markets must state, for its annual high street vitality paper, the number of stalls that traded across its 220 member markets in the year to 31 March 2026, as a single figure on a stated basis, with the same count by region and market type, the goods and day profile, the servicing load and the change on the year before. The analyst works from the 2025-26 and 2024-25 pitch letting extracts, the market and trader lists, goods class and day pattern lists, the waste round schedule, the reporting standard (RS-14), last year's vitality paper, the published licensing statement and the requester's extract note. RS-14 uses the word stall throughout without defining it. Deliverables are a re-runnable Excel workbook, a short note to the federation's council stating the figure and how it was counted, and one chart of stalls by region.)

`14 files, 3.7 MB`, `RE_vitality_paper.eml`, `day_patterns.csv`, `extract_note_2026-04.md`, `goods_classes.csv`, `licensing_statement_2026-03.pdf`, `markets.csv`, `pitch_lettings.csv`, `pitch_lettings_2024-25.csv`, `regions.csv`, `reporting_standard_2025-26.pdf`, `traders.csv`, `traders_2024-25.csv`, `vitality_paper_2024-25.pdf`, `waste_rounds.csv`

### Final recommendation

11,667 stalls traded at the federation's 220 member markets in the year to 31 March 2026, counted on the federation's stall convention, up 749 (6.9 per cent) on 10,918 in 2024-25 on the same basis.

### Step-by-step solution

1. Read RS-14, last year's vitality paper and the licensing statement: RS-14 does not define a stall, paragraph 27 allocates two collections a week a stall capped at 60 a market, and the paper's Table 3 prints markets by collection band with 79 at the cap.
2. Profile the 2025-26 extract: 18,041 rows, of which 917 vacant and 927 casual are not trading (paragraph 20), leaving 16,197 trading lettings (13,243 permanent, 2,954 seasonal).
3. Read each pitch label on its market's own numbering: 117 markets consecutive, 82 by odds and evens, 21 by block letter and number.
4. Join neighbouring trading lettings on one line that share a day pattern, goods class and first word of the trading name: 11,667 stalls.
5. Certify the convention on the 2024-25 extract: 10,918 stalls at 216 markets reproduce all seventeen Table 3 figures.
6. Split by region (North East 1,141, North West 1,713, Yorkshire and the Humber 1,128, East Midlands 1,002, West Midlands 1,152, East 1,373, London 821, South East 2,324, South West 1,013) and by market type (General 7,557, Farmers 781, Specialist 1,531, Covered 1,798).
7. Profile goods and days: fresh food the largest category at 4,098, fruit and vegetables the largest class at 1,498, Fri/Sat the largest pattern, 6,837 stalls on one day a week.
8. Compute the servicing load: 8,062 collections a week with 87 markets at the cap, set beside the 5,088 contracted collections, which are not the allocation (paragraph 28).
9. Compare with 2024-25: up 749 (6.9 per cent); the four new markets carry 178 and the 216 continuing markets rose 571 (5.2 per cent); 34 markets moved by more than a fifth.
10. Build the workbook with the convention as formulas, write the note and draw the regional chart.

### Key traps (what the model did)

- Counted one stall per Permanent/Seasonal letting row (16,197), so headline, regions, market types, servicing load and year-on-year change all inherited the wrong unit.
- Rebuilt 2024-25 on its own basis, found it did not reproduce printed Table 3 (91 vs 79 markets at cap), reported the discrepancy, and kept the basis anyway (one run hard-coded the published bands).

### Justification

The reporting standard never defines a stall, but last year's printed collection bands depend on the stall count, so they fix the unit. Only the federation's convention reproduces all seventeen printed figures from last year's lettings; one stall per letting and one stall per licensed trader both fail. On that unit, this year's lettings make 11,667 stalls, and the same unit applied to last year gives the comparable 10,918.

## Restate atchafalaya supply for 2024, The shipper furthest above the median correction position

**Pipeline Custody Transfer Measurement**, Batch 14, Energy & Environment, model mean **0.35** over 4 runs (0.41, 0.35, 0.35, 0.35).

### What makes it strong (the client's note)

The trap is the size of the correction: Port Arthur Distributing carries the largest correction in barrels (4,851,041), but GCS-9 s8 compares positions, the correction as a share of reported barrels, so its 15.40% sits below Atchafalaya Supply's 18.17%.
A second decoy is the Registrar's indicative schedule, which allocates by tickets lodged and puts Lafourche Distributing first at 2,063,359 barrels (47.75%); s6 bars allocation, and that figure is 50.0% of Lafourche's window, above the 35% ceiling.
The register publishes entry values, not barrels: the corrected volumes are recovered by finding the fixed step that separates sequence position from barrels, confirmed only when the result reproduces both prover controls (largest ticket 726,297 barrels; 158 tickets at 100,000 barrels or more).
The handbook's Annex A carries recalibration months that disagree with the station calibration record; the record governs under s4, the register's ticket months follow it, and the handbook months break the 35% cap.

### Stakeholder ask (the prompt, verbatim)

Product moves through the Gulf Coast Products Pipeline Council's system all year, metered at the station where each shipper injects it. Meters drift and when a prover run leads to a recalibration, everything the meter read before that point was taken on a basis the prover certificate supersedes.

At the close of the accounting year the Council works out which shipper's reported barrels have to be restated because of it. It restates one shipper. This review covers 2024.

Review the attached pack. GCS-9 governs. Work only from the supplied materials and carry out no external research. Name the single shipper whose reported figure GCS-9 requires the Council to restate for the 2024 accounting year. One shipper, no ties, no joint naming.

Also provide the following:

gcs9_restatement_review_2024.docx
State the shipper, its established correction in whole barrels and that correction as a percentage of the barrels it reported for the year, to 2 decimal places.
State the established correction in whole barrels for every other shipper whose meter station was recalibrated during the year.
State which shippers you weighed against your pick and what the supplied materials establish about each.
shipper_correction_table.csv
One row per shipper whose station was recalibrated, carrying the shipper code, shipper name, injection station, barrels reported for the year, barrels falling in the affected window, established correction in whole barrels and the correction as a percentage of barrels reported to 2 decimal places.
The shippers ranked by correction as a percentage of barrels reported, largest first.
The median of those percentages, computed on the unrounded values before rounding and each shipper's distance above or below it, both to 2 decimal places.
council_operations_review.html
Total barrels reported in 2024 by injection station, as whole numbers, with each station's share of the Council total in percent to 1 decimal place.
The 5 product grades with the largest reported barrels in 2024, giving the grade and the barrels as a whole number.

### Deliverables

`gcs9_restatement_review_2024.docx`, `shipper_correction_table.csv`, `council_operations_review.html` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A refined products pipeline council must close its 2024 accounting year by naming the one shipper whose reported barrels GCS-9 requires it to restate after meter recalibrations. Three of nine injection stations were recalibrated during the year, and every barrel metered before a recalibration took effect was read on a basis the prover certificate supersedes. From the reporting standard, the station calibration record, the meter ticket register, prover run controls, ticket counts, shipper and injection data, a registrar handbook and an indicative schedule, the analyst must establish each affected shipper's correction from the register, convert it into a position against the barrels the shipper reported, and name the shipper furthest above the median position. Deliverables are `gcs9_restatement_review_2024.docx` (the shipper, its correction and percentage, every other affected shipper's correction, and the shippers weighed against the pick), `shipper_correction_table.csv` (one ranked row per affected shipper with volumes, correction, percentage, the median and each distance from it) and `council_operations_review.html` (2024 barrels and share by injection station and the five largest product grades).)

`15 files, 1.7 MB`, `README.md`, `batch_movements.csv`, `council_overview.xlsx`, `council_reporting_standard.md`, `council_totals.csv`, `data_dictionary.json`, `gcs9_registrar_handbook.docx`, `meter_ticket_register.csv`, `monthly_injections.csv`, `prover_run_summary.csv`, `registrar_indicative_schedule.md`, `shipper_register.csv`, `station_calibration_record.csv`, `tank_gauge_daily.csv`, `ticket_counts.csv`

### Final recommendation

Restate Atchafalaya Supply (GCP-313, ST-8) for the 2024 accounting year: its established correction is 2,493,357 barrels, 18.17% of the 13,724,899 barrels it reported, 6.89 points above the 11.27% median position.

### Step-by-step solution

1. Read GCS-9: s4 defines the affected window as the months before a station's recalibration took effect with drift accumulating across it, s6 establishes corrections only from the meter ticket register and bars allocation or estimation, s7 lists the prover controls, s8 tests positions against the median, and s9 defers only inside half a point.
2. Take the recalibration months from the station calibration record: ST-2 from August, ST-8 from October, ST-5 from November. Six shippers injected at those stations before the recalibration took effect.
3. Sum each shipper's barrels in its window: Port Arthur 18,375,154; Atchafalaya 7,548,695; Grand Isle 7,880,012; Lafourche 4,123,114; Plaquemines 3,265,026; Matagorda 2,439,585.
4. Decode the register: each entry value combines a sequence position and the corrected barrels; the remainder against the one step that reproduces both prover controls (726,297 barrel maximum, 158 tickets at 100,000 or more) gives the corrected volumes.
5. Cut the register at the published ticket counts into one block per shipper and sum: Port Arthur 4,851,041; Atchafalaya 2,493,357; Plaquemines 962,390; Grand Isle 862,970; Matagorda 805,063; Lafourche 284,657. All sit inside the 35% ceiling.
6. Convert each to a position against reported barrels: Atchafalaya 18.17%, Port Arthur 15.40%, Plaquemines 12.65%, Matagorda 9.90%, Grand Isle 8.26%, Lafourche 6.59%.
7. Take the median on unrounded values, 11.27%: Atchafalaya stands 6.89 points above and Port Arthur 4.12, a 2.77 point margin, so s9 does not defer.
8. Record the rejected routes: ranking on barrels names Port Arthur, and the indicative schedule and every proportional split name Lafourche, all outside s6 and s8.
9. Build the HTML from reported barrels: 167,499,677 in total, ST-2 the largest at 47,240,044 (28.2%), and Transmix the largest grade at 34,384,059 barrels.

### Key traps (what the model did)

- Got the affected-window barrels right (they matched the calibration record) but recovered the wrong established correction per shipper. The decoding of register entry values into barrels (the fixed step that maps sequence position to barrels) was wrong and was never back-tested against the two prover controls. Every shipper's correction and percentage was wrong, which reshuffled the ranking so Grand Isle Supply came first (4/4).
- Did NOT fall for the designed decoys. Each run reasoned correctly that s8 compares positions, not barrels, and excluded the Registrar's indicative schedule.

### Justification

GCS-9 names the shipper standing furthest above the median position, not the one with the largest correction. Established from the register under s6, Atchafalaya Supply's correction is 18.17% of its reported year, the highest of the six, and its 6.89 point distance from the 11.27% median leads Port Arthur by 2.77 points, well clear of the half-point band. The indicative schedule and the handbook months would point elsewhere, but neither is an established figure under the standard.

## Publish the july 1, 2026 Withdrawal forecast from feed fr-26 At 24,247 Million

**Treasury Cash Flow Forecasting**, Batch 14, Finance & Accounting, model mean **0.41** over 4 runs (0.34, 0.97, 0.34, 0.31).

### What makes it strong (the client's note)

The trap is the supplied scorecard workpaper: every QA view there favors FR-18 (category MAE 416.5 against 420.6, statement-date MAE 25,976.4 against 28,703.6, calendar-day QA P75 13,393.2 against 15,272.1), but those measures score each date independently and are labeled QA, not certified loss.
The computation chain: filter DTS withdrawals to the eligible roster (excluding public debt cash redemptions), rebuild FR-18 from the eighth prior statement date and FR-26 from the sixth (25,750 rows), accumulate forecast minus observed withdrawals within each review period, apply the 0.75 underforecast and 0.25 overforecast loss to the running position, and weight by covered days.
Determinism pins: that method reproduces all six historical certified losses (for example 1,773,273.8 for August 2025), while independent-date and equal-date scoring reproduce none; final-test mean certified loss FR-26 34,106.7 and FR-18 35,446.0 million per covered day (totals 6,139,203.5 and 6,380,281.3); margin 1,339.3; July 1 forecasts FR-26 24,247 and FR-18 24,673.
The binding constraint is the publication request's decision rule, the lower mean certified forecast loss per covered day over the final-test period, with the certified method pinned by the historical controls rather than by the QA workpaper.

### Stakeholder ask (the prompt, verbatim)

The Federal Fiscal Outlook team must publish its July 1, 2026 forecast of eligible federal expenditure withdrawals for the near-term public-finance outlook. Two frozen candidate feeds were produced from Daily Treasury Statement history, but the supplied forecast records have not been closed out into one selection. Choose one feed and give one whole-million July 1 forecast. Use only the supplied files and do not browse.

Give me federal_withdrawal_forecast.svg.

State the selected feed, July 1 forecast, alternate feed, final-test margin, and the strongest evidence supporting the selection.
Compare the supplied feed-quality results and the full final-test loss results.
Show the selected feed's highest-loss final-test interval with the dates and figures that make it controlling.
Include a decision-bearing title, units, test window, legend, source note, and concise limitations.
Give me forecast_evaluation_audit.csv.

Include one row per final-test forecast date and feed, followed by the July 1 production rows, with source dates, forecast amount, eligible withdrawals, and every value needed to audit the comparison.
Include supplied review-period summaries and labeled rows for the selected feed, alternate feed, comparison losses, margin, July 1 forecast, and highest-loss interval.
Reconcile the supplied QA workpapers and historical certified losses without replacing their reported measures.
Append that interval's source and eligible row counts, signed deposit, withdrawal and net totals, and the top three deposit and withdrawal categories.
Give me reproduce_withdrawal_forecast.py.

Rebuild both frozen feeds from the supplied Treasury history and reproduce the final-test and July 1 forecast values.
Reconcile the supplied QA workpapers and historical certified losses.
Print the selected feed, alternate feed, comparison losses, margin, July 1 forecast, review-period results, and highest-loss-interval figures.
Run from the supplied folder without internet access and reproduce the values shown in the SVG and CSV.
Report forecast amounts as plain whole numbers of $ millions and final comparison losses to one decimal place. All three files must agree. Do not create extra files.

### Deliverables

`federal_withdrawal_forecast.svg`, `forecast_evaluation_audit.csv`, `reproduce_withdrawal_forecast.py` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A federal fiscal outlook team must publish its July 1, 2026 forecast of eligible federal expenditure withdrawals and has two frozen candidate feeds, FR-18 and FR-26, built from Daily Treasury Statement history. The supplied forecast records have not been closed out into one selection, so the analyst must choose one feed and give one whole-million July 1 forecast using only the supplied files: the 2025 and 2026 DTS cash flows, the candidate forecasts, the evaluation calendar, the loss schedule, the publication request, the historical certified losses and forecast rows, the feed register, and a feed-quality scorecard workpaper. The analyst must rebuild both feeds, settle which loss measure governs, compare the feeds over the January to June 2026 final test, and audit the selected feed's highest-loss interval. Deliverables are `federal_withdrawal_forecast.svg` (decision, margin, strongest evidence, QA versus final-test comparison, controlling interval), `forecast_evaluation_audit.csv` (248 final-test rows and two July 1 rows plus labeled summary, reconciliation and interval-context rows) and `reproduce_withdrawal_forecast.py` (an offline script that rebuilds the feeds and prints every figure).)

`12 files, 6.2 MB`, `candidate_feed_register.json`, `candidate_withdrawal_forecasts.csv`, `dts_cash_flow_metadata.json`, `dts_cash_flows_2025.csv`, `dts_cash_flows_2026.csv`, `forecast_evaluation_calendar.csv`, `forecast_loss_schedule.json`, `forecast_publication_request.json`, `historical_forecast_loss_summary.csv`, `historical_forecast_rows.csv`, `source_manifest.json`, `withdrawal_forecast_scorecard.xlsx`

### Final recommendation

Select FR-26 and publish a July 1, 2026 forecast of 24,247 million; its final-test mean certified loss of 34,106.7 million per covered day beats FR-18 (35,446.0, July 1 forecast 24,673) by 1,339.3.

### Step-by-step solution

1. Filter the DTS data to the 103-category eligible-withdrawal roster, excluding public debt cash redemptions, for a consistent observed-withdrawal series.
2. Rebuild FR-18 from the eighth prior statement date and FR-26 from the sixth: all 25,750 candidate rows reproduce exactly.
3. Reconcile the supplied scorecard: category MAE 416.5 (FR-18) against 420.6 (FR-26), statement-date MAE 25,976.4 against 28,703.6. These QA measures favor FR-18 and are kept as reported.
4. Test loss methods against the six historical certified periods: the cumulative within-period position, with the 0.75/0.25 asymmetric loss and covered-day weighting, matches 6 of 6; independent-date and equal-date scoring match 0 of 6.
5. Apply that method to the final test (2026-01-02 to 2026-06-30, 124 forecast dates, 180 covered days): FR-26 6,139,203.5 total, 34,106.7 per covered day; FR-18 6,380,281.3 total, 35,446.0 per covered day; margin 1,339.3.
6. Summarize by review period: FR-26 is lower in January, March and April (April 23,697.8 against 45,232.1); FR-18 is lower in February, May and June.
7. Aggregate FR-26's July 1 production rows to 24,247 million (FR-18 24,673).
8. Locate FR-26's highest-loss interval: forecast date June 5 (next forecast June 8, history cutoff June 4, reference statement date May 28), forecast 23,351, observed eligible withdrawals 20,219, opening position -134,107, closing -130,975, loss 294,693.8.
9. Profile June 5: 178 source rows, 99 eligible-withdrawal rows, deposits +15,580, withdrawals -34,564 and net -18,984 on all withdrawals (-20,219 and -4,639 on the eligible basis); top deposits Taxes Withheld Individual/FICA 9,151, Taxes Non-Withheld Ind/SECA Electronic 1,892, Public Debt Cash Issues 1,625; top eligible withdrawals Federal Salaries (EFT) 4,764, HHS Grants to States for Medicaid 3,930, Department of Defense miscellaneous 1,438.
10. Write the SVG, the audit CSV and the offline reproduction script so all three agree.

### Key traps (what the model did)

- Selected the feed on the supplied QA scorecard measures (category MAE, statement-date MAE, calendar-day P75) and reported those as the 'certified loss', never building the cumulative within-period asymmetric loss that the six historical certified-loss controls pin.

### Justification

The publication request decides on certified forecast loss, and the only loss method that reproduces every historical certified period is the cumulative within-period position weighted by covered days. The scorecard's measures reset the position on every date, so they describe a different loss process and contradict all six certified controls, even though they favor FR-18. Applied unchanged to the held-out January to June 2026 test, the certified method gives FR-26 a lower mean loss by 1,339.3 million per covered day, so FR-26 governs and its July 1 forecast of 24,247 million is the one to publish.

## Set the 2026 extended-hours calendar at 79 peak months with ten added centres and no northwest summer

**Labor Market Seasonality**, Batch 14, Economics, model mean **0.45** over 4 runs (0.95, 0.32, 0.35, 0.36).

### What makes it strong (the client's note)

The trap is the window: the terms do not state it, and a trailing window to August 2025 or a calendar-year window (2022 to 2024) looks natural but reproduces neither past calendar and gives 75 or 73 peak months with a different set of changes.
The construction is recovered by replaying the two calendars on file: only a 36-month window ending June of the year before the calendar, with each month's figure as the mean of its three observations and the norm as the mean of all 36, marked at 1.0 point above norm, reproduces 2024 and 2025 month for month.
The northwest summer is the decision the regions are waiting on: June 2025 ran at 6.9% in Pennington and 7.5% in Red Lake against norms of 4.3% and 4.7%, but the three-June figures sit only 0.5 and 0.9 points above norm and the Julys sit below it, so no summer month marks.
Determinism pins: 79 peak months at 28 centres; ten changed centres, all additions; Worthington June 4.1% against a 2.7% norm; Thief River Falls December 5.4% against 4.3%; January busiest with 25 centres; 2025 had 69 months at 24 centres.

### Stakeholder ask (the prompt, verbatim)

Ops meeting, 7 October , item 4, extended-hours calendar 2026

Action: analytics, back to Lennart by the 17th

Item 4 was deferred because the calendar wasn't ready, and it came back with a complication. Northwest region says Thief River Falls and Red Lake Falls have been swamped since June , worst summer anyone there remembers , and wants summer on their calendar for 2026. Southwest says the same thing happened at Worthington in 2023 and it never went on. Lennart's position: the calendar is for what a county does every year, not for what it did this year, and one hard summer is a regional problem, not a calendar entry , unless the figures say it's the county's pattern now. Regions need the calendar by the 20th to roster the second counsellors and book the Saturday cover, so this can't slip.

What's in the shared folder:

the LAUS pull from yesterday (Colorado, Oklahoma and Minnesota, everything BLS publishes, monthly through August)
centers.csv, our fifty centers with the county each one sits in
the 2024 and 2025 calendars as they were set
the terms page for the calendar
The question for item 4: what is the 2026 extended-hours calendar , how many peak months in total, and which centers change from 2025? That goes in the first line of extended_hours_2026.md, with the centers named. Whether the northwest summer is on it falls out of that.

Three things back, in this order of importance:

extended_hours_2026.xlsx

Sheet 1 , the calendar: one row per center, all fifty, an X in each peak month; the count of peak months and the list of changed centers at the top; a line at the bottom on what the marks rest on and which files they came from.

Sheet 2 , the figures: for every center, the twelve monthly figures the marks were judged on and the norm they were judged against.

extended_hours_2026.md

First line: the answer. Then half a page for the regional leads: each changed center with the month that comes on or off and the figure behind it; a plain answer on the northwest summer , this year's June and July at Thief River Falls and Red Lake Falls against their norms, and why those months are or are not on the 2026 calendar; the busiest month across the network; how 2026 sits against 2025 overall; and one plain-language line on what the figures are.

extended_hours_2026.png

The calendar as one picture: fifty centers down, twelve months across, colour for how far each month sits from the center's norm, the 2026 peak months outlined, and last year's peak months marked some other way so the changes stand out. Lennart puts this on the regional call.

Minutes taken by Ash. Lennart is out Thursday and Friday.

### Deliverables

`extended_hours_2026.xlsx`, `extended_hours_2026.png` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A Minnesota workforce centre network must publish its 2026 extended-hours calendar so regions can roster second counsellors and Saturday cover. Northwest region wants summer added at Thief River Falls and Red Lake Falls after a hard 2025 summer, while the operations lead holds that the calendar records what a county does every year, not what it did this year. From a BLS LAUS county extract, the list of fifty centres and their counties, the 2024 and 2025 calendars as set, and the calendar terms page, the analyst must recover the construction that produced the two past calendars, apply it for 2026, and say how many peak months the calendar carries and which centres change. Deliverables are `extended_hours_2026.xlsx` (a fifty-row calendar sheet with the count and changed list at the top and a basis line at the bottom, and a figures sheet with each centre's norm and twelve monthly figures), `extended_hours_2026.md` (the answer on the first line, then a half-page brief on the changes, the northwest summer, the busiest month, the comparison with 2025 and what the figures are), and `extended_hours_2026.png` (a fifty by twelve heat map with the 2026 peaks outlined and the 2025 peaks marked differently).)

`14 files, 41.1 MB`, `centres.csv`, `checksums.txt`, `data_dictionary.json`, `dim_area.csv`, `dim_area_type.csv`, `dim_measure.csv`, `dim_state.csv`, `extended_hours_calendar_2024.csv`, `extended_hours_calendar_2025.csv`, `extended_hours_terms.md`, `fact_laus_levels.csv`, `fact_laus_rate.csv`, `overview.xlsx`, `provenance.txt`

### Final recommendation

The 2026 extended-hours calendar carries 79 peak months across 28 of the 50 centres, and 10 centres change from 2025, all by adding a month: Bemidji, Buffalo, Crookston, Foley, Hallock, Mora, Pine City, Preston, Thief River Falls and Worthington; the northwest summer is not on it.

### Step-by-step solution

1. Join centres.csv to the area dimension by LAUS area code and pull the fifty counties' monthly unemployment rate, not seasonally adjusted (measure 03), January 1990 to August 2025.
2. Read the two calendars on file as outcomes: 82 marks at 38 centres for 2024 and 69 marks at 24 centres for 2025.
3. Test candidate constructions against both: a month's figure is the mean of that calendar month over a 36-month window, the norm is the mean of the whole window, and a month marks at 1.0 point or more above norm; only the window July of Y-3 to June of Y-1 reproduces both calendars exactly.
4. Apply it on July 2022 to June 2025: 79 peak months at 28 centres.
5. Compare with 2025 centre by centre: 10 centres change, all additions, each added month between 1.1 and 1.4 points above its norm (for example Mora April 7.0% against 5.8%, Worthington June 4.1% against 2.7%, Thief River Falls December 5.4% against 4.3%).
6. Answer the northwest summer: Thief River Falls and Red Lake Falls have June figures 0.5 and 0.9 points above norm and July figures below it, so neither marks a summer month; Thief River Falls adds December and Red Lake Falls is unchanged. Crookston and Worthington are the only centres with a summer peak, each in June.
7. Count marks by month: January is busiest with 25 centres, and January to March hold 71 of the 79 marks. Against 2025, peak months rise from 69 to 79 and centres from 24 to 28.
8. Build the workbook, the brief and the heat map from the same table.

### Key traps (what the model did)

- Chose an arbitrary averaging window (calendar 2023-2025 with a 32-month norm; 2021-Aug 2025 56 observations; 2015-2024 excluding 2020-21) instead of recovering the window by replaying the 2024 and 2025 calendars, giving 66-67 peak months and spurious removals.
- Got the northwest-summer conclusion (off the calendar) for the wrong reasons: June gaps reported below norm or far below required, July sign wrong.

### Justification

The terms describe a month that runs seasonally high against the county's own norm, and the past calendars show exactly how that was measured. The construction that reproduces both of them, applied to the latest window, gives 79 peak months with ten additions and no removals. One hard summer in the northwest raises the 2025 actuals but not the three-year June and July figures enough to clear the 1.0 point line, so summer stays off the calendar at Thief River Falls and Red Lake Falls.

## Publish the corrected 2018 indicator at 0.126811 Net mwh per mmbtu for 21 review blocks and hold the other 455

**Electric Power Productivity Statistics**, Batch 14, Economics, model mean **0.53** over 4 runs (0.53, 0.53, 0.55, 0.52).

### What makes it strong (the client's note)

The trap is publishing on the historical generation basis, which gives 15 eligible blocks in the old queue and misses that signed negative Meramec generation becomes positive after the authorized correction; three Meramec blocks only become eligible on the restated basis.
A second trap is letting the generation amendment repair physical gaps: Mustang U:2953:T10 gets a resolved 962,780 MWh pool total but stays held because its required unit snapshot is missing.
The computation chain runs from 23 plant-code recodes and crosswalk plus boiler-generator edges, through distribution-pool closure, to a 2,225-block national ledger, a 476-block review population and 21 published blocks.
Determinism pins: published totals of 20,447,431 net MWh and 161,243,211 MMBtu give 0.126811 net MWh per MMBtu; unadjusted CO2 intensity is 1,004.865 lb per net MWh; the same population's historical generation is 15,035,146 MWh, so amendments add 5,412,285 MWh.

### Stakeholder ask (the prompt, verbatim)

We are revising a 2018 industry productivity indicator for the national economic brief. The electric-power source tables are its measurement base, and the decision is whether the corrected indicator is fit to publish,not how any plant should operate. Using the review population in publication_spec.md and its documented generation-correction scope, decide PUBLISH or HOLD. Put the decision in publication_decision.html and report the indicator as net MWh of output per MMBtu of heat input to six decimals, along with the supporting block calls, unadjusted CO2 intensity, annual quantities and coverage. Keep this selected-population figure separate from the whole sector.

Put the block-level working record in publication_exception_mart.json. For every reviewed block, show its membership, disposition, reasons and the source rows behind the call. I also need the population account to tie: published plus held blocks must equal the reviewed population, and reviewed plus outside-review blocks must equal the national block ledger. Keep the physical relationships and historical allocation pools behind those totals. Show how the authorized generation restatement changes the quantities and release membership while retaining the original observations and the separate all-source vintage bridge.

The research editor also needs a concise offline publication_decision.html. Put the decision first and use a visual for the publish-versus-hold account and coverage. We have been going back and forth on the held blocks, so make it easy to tell an unusual but publishable case from an incomplete one. Explain which differences come from source revisions and which come from the released population, and what the limited restatement can and cannot say about industry productivity.

Ship the rebuild as build_exception_mart.py. Another analyst should be able to run it against input_files, check the source keys and controls, and get the same substantive answer if the input rows arrive in a different order. Everything it needs is already in the folder. I need to reuse it when the source files are refreshed, so the figures have to come from those files rather than the script. If existing outputs differ, it should stop and leave them alone.

### Deliverables

`publication_decision.html`, `build_exception_mart.py` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (An economics research desk is revising a 2018 industry productivity indicator for a national economic brief, using eGRID2018 v2, EIA-923, EIA-860 and the EPA-EIA crosswalk as its measurement base. The decision is whether the corrected indicator is fit to publish. The analyst must build source-closed blocks from one relationship graph, form the historical three-characteristic review queue, add every block touching a plant named in an authorized 2018 generation correction, apply the restated generation at its supported grain, and re-test whole-block eligibility (reference snapshot, numeric quantities, physical support, uncovered boilers, positive output, confirmed non-CHP). The result must tie published plus held to the reviewed population and reviewed plus outside-review to the national ledger, and keep the all-source vintage bridge separate from the same-population amendment. Deliverables are `publication_decision.html` (offline, decision first, with a publish-versus-hold and coverage visual), `publication_exception_mart.json` (block-level case record with membership, disposition, reasons and source rows) and `build_exception_mart.py` (a rerunnable rebuild from the input files).)

`17 files, 38.1 MB`, `2___Plant_Y2018.xlsx`, `3_1_Generator_Y2018.xlsx`, `6_1_EnviroAssoc_Y2018.xlsx`, `Form EIA-860 Instruction (2018).pdf`, `LayoutY2018.xlsx`, `crosswalk_LICENSE.txt`, `egrid2018_GEN18.csv`, `egrid2018_PLNT18.csv`, `egrid2018_UNT18.csv`, `egrid2018_release_notes_2020-03-09.txt`, `egrid2018_technical_support_document.pdf`, `eia923_corrections.html`, `eia923_generation_fuel.csv`, `eia923_generator.csv`, `epa_eia_crosswalk.csv`, `publication_spec.md`, `source_index.json`

### Final recommendation

PUBLISH 0.126811 net MWh per MMBtu for the 21 qualifying 2018 review blocks and HOLD the remaining 455 review blocks.

### Step-by-step solution

1. Validate the supplied releases, source keys, record counts and controls. Keep the historical eGRID identities, unit heat input and CO2, and apply only the authorized 2018 generation corrections.
2. Resolve identities, the 23 documented plant recodes, physical relationships and historical allocation pools. This gives a national ledger of 2,225 blocks, 4,156 reference units, 4,231 unit endpoints and 4,718 participating generators.
3. Apply the three historical review triggers (470 blocks), then add every block touching a named correction plant. Six blocks join, giving 476 reviewed blocks and 1,749 outside-review blocks.
4. Apply the generation corrections at the supported grain: exact EIA-923 generator year-to-date values for non-pooled generators and one plant and prime-mover total for each historical pool. Recheck completeness, physical support, positive output and confirmed non-CHP status for each whole block, giving 21 published and 455 held blocks.
5. Aggregate the 21 published blocks on one common population: 20,447,431 net MWh, 161,243,211 MMBtu and 10,273,455.325 short tons of CO2. The same blocks had 15,035,146 MWh historically, so amendments add 5,412,285 MWh.
6. Compute the rates: 0.126811 net MWh per MMBtu, 7.886 MMBtu per net MWh and 1,004.865 lb CO2 per net MWh.
7. Compute coverage against the reviewed population: 4.412% of blocks, 4.587% of reference units, 3.709% of generators, 3.642% of known generation, 3.054% of known CO2 and 3.317% of known heat input.
8. Reconcile 21 published plus 455 held to 476 reviewed, and 476 reviewed plus 1,749 outside-review to 2,225 national blocks. Build the separate all-source bridge from 4,168,370,117.666 to 4,180,987,703.992 MWh, split into 6,387,623.005 MWh of documented named-plant change and 6,229,963.321 MWh of other change.
9. Record all 476 cases with evidence in publication_exception_mart.json, summarize the decision, coverage and amendment bridge in publication_decision.html, and ship build_exception_mart.py for deterministic rebuilding.

### Key traps (what the model did)

- Handled the intended traps (Meramec restatement 4/4, Mustang hold 3/4) but applied an over-broad physical-completeness blocker (holding blocks with any unit outside the reference snapshot rather than only missing required units), holding 4 qualifying blocks: 17 published vs 21, so every published total, ratio and coverage figure is off.

### Justification

The spec makes eligibility depend on the restated generation basis while keeping physical completeness requirements unchanged, so the right answer needs both halves. The Meramec correction turns three blocks with negative historical output into positive, fully supported blocks and lifts the published count from 18 to 21 in the expanded queue. The Mustang pool amendment changes output but cannot supply a missing unit snapshot, so that block stays held. With a complete, non-CHP, common population on both sides of the ratio, the indicator is 20,447,431 / 161,243,211 = 0.126811 net MWh per MMBtu. It describes only that selected population, and the all-source vintage bridge is a separate account of source revisions, not a change in the released population or evidence of growth.

## Certify cocke county, tennessee as the hurricane helene anchor county, with buncombe county as runner-up

**Disaster Labor Market Impact**, Batch 14, Economics, model mean **0.53** over 4 runs (0.70, 0.56, 0.44, 0.50).

### What makes it strong (the client's note)

The trap is the staff quick look, which ranks on raw change in private jobs and puts Buncombe County first at -10,313 jobs (-8.29 percent); on the terms' loss rate per hundred private jobs Buncombe is second at -5.15.
The computation chain runs from six Helene declarations (DR-4827 to DR-4832) and an October 2024 impact month, through a 5,000-job floor, state comparator pools (North Carolina 33, Tennessee 37, Virginia 81, Georgia 47, South Carolina 3, Florida 0), first-quarter exposed-line tests, a pre-storm comparator screen and a five-comparator minimum per line, to employment-weighted shortfalls on the exposed work.
The terms read more than one way: only the reading that drops the fifth of comparators (rounded down) farthest from the county on base-year half-over-half movement, measured on the county's exposed lines, with an adjacency ring that crosses state lines, returns all eight restated rates (Iowa County -4.13 and 362 jobs, Dauphin County -1.25 and 1,748, Henry County -4.97 and 450, Monroe County -6.47 and 536, runner-ups -3.40, -1.11, -3.61 and -2.31, Louisiana and Florida declined).
Determinism pins: Cocke -5.51 and 339 jobs on 6,149 base-year private jobs, six exposed lines carrying 4,138 jobs, 30 of 37 comparators kept; Buncombe -5.15 and 6,347 jobs with 16 exposed lines; unrounded gap 0.3587 points, about 22 jobs; 31 of 48 members certifiable.

### Stakeholder ask (the prompt, verbatim)

Our board meets in October, and the Helene certification is the one piece of the meeting that still needs to be completed.

Use the 2021 certification terms, the restated schedule Renata signed on the eighth, the membership roster, and the annual BLS and FEMA extracts. The extracts cover ten states because the earlier events on the schedule include Iowa, Pennsylvania, Louisiana, and Mississippi in addition to the six states affected by Helene.

Start by reconstructing the six certifications on the restated schedule. Those published results are the validation test for the method. Where the terms allow more than one reading, use the interpretation that reproduces the schedule and state that choice in the memo. Do not apply the method to Helene until all six prior certifications reproduce correctly.

An analyst also prepared an August first pass that ranks designated member counties by raw change in private employment and places Buncombe first. Treat that as a preliminary comparison, not the governing result, and explain why it does or does not agree with the certification method.

Return three files.

helene_anchor_county_certification.docx is the board memo. Open with the certified anchor county, its loss rate and attributed jobs, the runner-up, the gap between them, and how far the anchor county's rate could weaken before the runner-up takes its place, expressed both in rate points and jobs. Then explain where every member county stands and why the August first-pass leader is or is not the answer. Keep detailed tables in the workbook rather than the memo.

helene_loss_rate_chart.png should show the loss rate for every certifiable member county as horizontal bars in rank order, with the anchor county and runner-up clearly distinguished. Put the certification in the title.

helene_certification_workbook.xlsx should contain three sheets named Member counties, Restated schedule, and Exposed lines. Use one row per designated member county on the first sheet with its standing and supporting figures; reconcile the restated schedule against the reconstructed figures on the second; and list the exposed lines of work for the anchor county and runner-up on the third.

Report rates to two decimal places and jobs as whole jobs.

### Deliverables

`helene_anchor_county_certification.docx`, `helene_loss_rate_chart.png`, `helene_certification_workbook.xlsx` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A regional community-funding collaborative must certify the anchor county for Hurricane Helene at its October board meeting. The analyst has the collaborative's 2021 certification terms, a restated schedule of six earlier certifications, the membership roster, an August staff quick look, and raw BLS QCEW county extracts and FEMA declaration records for ten states. The terms read more than one way, and the analyst must first find the reading that reproduces all six restated certifications, then apply it to the 48 designated Helene member counties: fix the impact month and the two twelve-month years, build each state's comparator pool, identify each county's exposed lines of work, screen comparators on pre-storm movement, and compute loss rates and attributed jobs. Deliverables are `helene_anchor_county_certification.docx` (a board memo opening with the anchor, its rate and jobs, the runner-up, the gap and the flip margin in rate points and jobs, then where every member stands, the adopted reading, and why the quick look's leader is not the answer, with no tables), `helene_loss_rate_chart.png` (horizontal bars of every certifiable county's loss rate in rank order, anchor and runner-up picked out, certification in the title) and `helene_certification_workbook.xlsx` (sheets Member counties, Restated schedule and Exposed lines).)

`24 files, 80.0 MB`, `DisasterDeclarationsSummaries.csv`, `DisasterDeclarationsSummaries_fields.json`, `agglevel_titles.csv`, `area_titles.csv`, `certification_terms.pdf`, `county_adjacency.txt`, `csv_data_slices.htm`, `csv_quarterly_layout.htm`, `helene_quick_look.xlsx`, `industry_titles.csv`, `membership_roster.xlsx`, `national_county2020.txt`, `ownership_titles.csv`, `qcew_county_2018.csv`, `qcew_county_2019.csv`, `qcew_county_2020.csv`, `qcew_county_2021.csv`, `qcew_county_2022.csv`, `qcew_county_2023.csv`, `qcew_county_2024.csv`, `qcew_county_2025.csv`, `qcew_county_2026.csv`, `restated_schedule_2026.pdf`, `source_register.csv`

### Final recommendation

Certify Cocke County, Tennessee (FIPS 47029) as the Hurricane Helene anchor county at a loss rate of -5.51 per hundred private jobs (339 attributed jobs lost); Buncombe County, North Carolina is the runner-up at -5.15, a gap of 0.36 rate points or about 22 attributed jobs.

### Step-by-step solution

1. Take the six Hurricane Helene declarations (DR-4827 North Carolina, 4828 Florida, 4829 South Carolina, 4830 Georgia, 4831 Virginia, 4832 Tennessee); all begin in the last week of September 2024, so the impact month is October 2024, the base year October 2023 to September 2024 and the post-storm year October 2024 to September 2025.
2. Cut the roster to the 48 member counties designated under those declarations and compute base-year private jobs (aggregation level 71, ownership 5, industry 10); nine fall below the 5,000-job floor.
3. Build each state's comparator pool from same-state counties not designated under the event or under any other overlapping major disaster declaration (COVID-19, emergency and fire management declarations excluded) and not adjoining any county designated for Individuals and Households under the event, with the ring crossing state lines: North Carolina 33, Tennessee 37, Virginia 81, Georgia 47, South Carolina 3, Florida 0.
4. Keep a two-digit line for a county or comparator only where it is published in every month of both years, and treat 999 pseudo-county rows as non-counties.
5. Mark a county's exposed lines as those where its October to December 2024 average over its base-year average falls behind the pooled comparators' same ratio: Cocke has six lines (31-33, 42, 44-45, 71, 72, 81) carrying 4,138 of 6,149 base-year jobs; Buncombe has 16.
6. Screen comparators on pre-storm movement by dropping the fifth (rounded down) farthest from the county on the change between the first and second halves of the base year, measured on the county's exposed lines; Cocke keeps 30 of 37 and Buncombe 27 of 33. Drop any line with fewer than five comparators, which leaves the six South Carolina members with too few comparators and Hillsborough and Pinellas with none, so 31 counties are certifiable.
7. Run the same method on the six earlier events and confirm it returns the restated schedule row for row: Iowa County -4.13 and 362, Dauphin County -1.25 and 1,748, Henry County -4.97 and 450, Monroe County -6.47 and 536, with Louisiana and Florida declined.
8. Compute each loss rate as the county's exposed-work movement less the pooled comparators' movement, weighted by the county's own base-year line employment, times exposed jobs over base-year private jobs per hundred: Cocke -8.60 against -0.42, shortfall -8.18, giving -5.51 and 339 attributed jobs.
9. Rank: Cocke -5.51, Buncombe -5.15 (6,347 jobs), Decatur -5.03. The unrounded gap of 0.3587 points times 6,149.25 over 100 is about 22 attributed jobs.
10. Write the memo leading with the certification and stating the adopted reading, the ranked chart, and the three-sheet workbook.

### Key traps (what the model did)

- Applied the certification method without the pre-storm comparator screen (or with another relaxed reading), landing on the decoy figures Cocke -5.44/335 jobs and Buncombe -5.26 instead of -5.51/339 and -5.15; the winner usually held but the gap halved (0.17-0.18 vs 0.36) and weakening margin was ~11 jobs vs 22.
- One run's looser reconstruction moved Cocke to -4.48 and certified Buncombe; others named Decatur or Smyth as runner-up.

### Justification

The terms make the certification turn on the loss rate per hundred private jobs on a county's exposed work against unaffected comparators, and the collaborative requires any reading to reproduce its restated schedule before its Helene figures count. The one reading that returns all eight restated rates puts Cocke County first at -5.51, with Buncombe second at -5.15. The August quick look's Buncombe lead reflects Buncombe's size, since raw job change over a single quarter is not the terms' measure. The margin is thin, about 22 attributed jobs, but every certifiable county is ranked on the same reading and no rival comes closer.

## Print line 4 (Ohio state below local government) As the headline

**Occupational Safety Statistics**, Batch 14, Economics, model mean **0.56** over 4 runs (0.53, 0.48, 0.84, 0.46).

### What makes it strong (the client's note)

Three lines look settled by published figures but are contradicted by rates BLS does not publish: Kansas's state-and-local rate (5.5) sits above its local rate (4.0), forcing its state-government rate above 5.5 and past New York's 5.1; Texas's all-employer rate (2.2) above its private rate (1.7) forces its public-sector rate above 2.2.
The headline itself rests on an unpublished figure: Ohio's state-and-local rate (2.3) is below its local rate (2.5), so its state-government rate must be under 2.3. The bounding argument is supported by the data, with the combined rate between its parts in 367 of 367 fully published state-years.
Line 3's 2.8 versus 3.2 is a mix effect: 71.4% of state-government education-and-health hours are in education against 11.8% for private industry, and on a common mix state government is higher every way (5.47 vs 3.20 on the private mix, 2.79 vs 2.19 on the state mix, 5.20 vs 3.10 pooled), which requires reconstructing hours as cases divided by rate.
Line 5 fails on the stated rule: standard errors of 0.132 and 0.026 give a 95% margin on the difference of 0.264, larger than the 0.2 gap.

### Stakeholder ask (the prompt, verbatim)

I'm signing off a one-page fact sheet on workplace injuries in public-sector jobs, built on BLS's 2024 survey. Only one of these draft lines can be the headline, and it has to hold up:

Among the 34 states with a published state-and-local government rate, New York's state-government workers had the highest rate, at 5.1 cases per 100 full-time workers.
In Texas, state and local government workers were injured less often than private-industry workers.
Even after allowing for their different mix of services, state-government workers in education and health services were injured less often than private-industry workers in that sector, 2.8 versus 3.2.
In Ohio, state-government workers were injured less often than local-government workers.
Local-government hospital workers were injured less often than private hospital workers, 4.9 versus 5.1.
Which line goes to print as the headline? Where BLS gives a relative standard error, a gap only counts if it's bigger than the 95% margin of error on the difference; everywhere else, treat the published figures as exact.

Put the check behind every line in fact_sheet_check_2024.xlsx, including the full 34-state state-government ranking. Then write fact_sheet_corrections.docx from the workbook for the editor: the headline and why it holds, why each of the other lines fails with wording that would hold instead, and a chart they can check it all against.

### Deliverables

`fact_sheet_check_2024.xlsx`, `fact_sheet_corrections.docx` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (An editor is signing off a one-page fact sheet on public-sector workplace injuries built on the BLS 2024 Survey of Occupational Injuries and Illnesses, and must choose one of five draft lines as the headline: New York has the highest state-government rate of the 34 states with a state-and-local rate, Texas public-sector workers are injured less often than private workers, state education-and-health workers are safer than private ones even after allowing for service mix, Ohio state-government workers are injured less often than local-government workers, and local-government hospital workers are safer than private hospital workers. Gaps backed by a BLS relative standard error count only if they exceed the 95% margin of error on the difference; other published figures are exact. The analyst must join the BLS series, area and rate files, bound the unpublished Kansas, Ohio and Texas rates from the ownership hierarchy, rebuild hours from case counts to standardize the education-and-health mix, and test the hospital gap against its margin of error. Deliverables are `fact_sheet_check_2024.xlsx` (the check behind every line plus the full 34-state state-government ranking) and `fact_sheet_corrections.docx` (the headline and why it holds, why each other line fails with wording that would hold, and a chart).)

`12 files, 4.1 MB`, `area.csv`, `case_type.csv`, `data_dictionary.json`, `data_type.csv`, `fact_injury_rates.csv`, `industry.csv`, `overview.xlsx`, `ownership_counts_source.csv`, `ownership_rse_source.csv`, `series.csv`, `supersector.csv`, `supplementary_source_provenance.json`

### Final recommendation

Print line 4, "In Ohio, state-government workers were injured less often than local-government workers," as the headline. Ohio's state-and-local rate (2.3) is below its local rate (2.5), so its unpublished state-government rate must be below 2.3; lines 1, 2 and 3 are contradicted and line 5's gap is inside the margin of error.

### Step-by-step solution

1. Join fact_injury_rates.csv to series.csv and area.csv, keeping industry 000000 (all workers), total recordable case rates, 2024, annual period.
2. Decode ownership from the first digit of the area code (0 all employers, 1 private, 7 state, 8 local, 9 state-and-local) and the state from the last two digits.
3. Confirm the rates nest: state-and-local lies between state and local in 367 of 367 fully published state-years, and all-employer lies between private and state-and-local in 420 of 420.
4. Define the 34 states as those with a 2024 state-and-local rate, excluding the national total, Puerto Rico, the Virgin Islands and Guam. Pennsylvania has a state-government rate but no state-and-local rate, so it drops out.
5. Line 1: New York (5.1) has the highest published state-government rate, but Kansas's state-and-local rate (5.5) is above its local rate (4.0), so Kansas state government is above 5.5. Line 1 is contradicted.
6. Line 4: Ohio's state-and-local rate (2.3) is below its local rate (2.5), so Ohio state government is below 2.3. Line 4 holds.
7. Build the 34-state ranking: Kansas above 5.5 (derived), New York 5.1, California 4.5, Maine 4.0, Illinois 3.9, down to Vermont 0.9, with Ohio below 2.3 and not placed exactly.
8. Line 2: Texas's all-employer rate (2.2) is above its private rate (1.7), so its state-and-local rate is above 2.2. Line 2 is contradicted.
9. Line 3: compute full-time equivalents as cases divided by rate from ownership_counts_source.csv. Education is 71.4% of state-government hours and 11.8% of private hours. On a common mix state government is higher: 5.47 vs 3.20 (private mix), 2.79 vs 2.19 (state mix), 5.20 vs 3.10 (pooled). Line 3 is contradicted.
10. Line 5: standard errors are 4.9 x 2.7% = 0.132 and 5.1 x 0.5% = 0.026; the 95% margin on the difference is 1.96 x sqrt(0.132^2 + 0.026^2) = 0.264, above the 0.2 gap. Line 5 cannot be backed.
11. Draft replacement wording for lines 1, 2, 3 and 5, build the workbook (line checks, rates, bounds, ranking, mix adjustment, margin of error, chart) and write the editor memo from it with the chart embedded.

### Key traps (what the model did)

- Treated BLS-suppressed rates (Kansas and Ohio state government, Texas public sector) as missing and declared 'no comparison possible', instead of bounding them from the published combined rate vs its published component; this left line 1 (New York highest) standing and line 4 rejected.
- Even when the Kansas>5.5 bound was derived, read line 1 narrowly as 'highest published rate' and still printed it.

### Justification

Line 4 is the only draft that survives. BLS does not publish Ohio's state-government rate, but a combined rate is an hours-weighted average of its parts, and the data confirm it always sits between them, so Ohio's combined rate of 2.3 under its local rate of 2.5 puts state government below 2.3. The same reasoning overturns lines 1 and 2: Kansas's unpublished state-government rate has to exceed 5.5, ahead of New York, and Texas's public-sector rate has to exceed its all-employer 2.2, above private industry's 1.7. Line 3's lower headline rate comes from state government's heavy weighting toward colleges, and it reverses once both sectors are put on the same service mix. Line 5's 0.2 gap is smaller than the 0.264 margin of error the editor's own rule requires it to beat.

## Build the 2026 q1 seat plan on 51,220 Seats, adding the ma-4101 Seats that land on open lines

**Subscription Seat Billing**, Batch 14, Finance & Accounting, model mean **0.6** over 4 runs (0.68, 0.68, 0.68, 0.44).

### What makes it strong (the client's note)

The trap runs in two directions: the closing base looks inflated against the feed (re-subscribed accounts, a retired provisioning region, delegated-administrator seats) but each structure is billable under BP-4 and the December settlement ties line for line at 41,820 seats; on the other side, stopping at the closing base plus the contract book gives 43,960 and misses the MA-4101 expiry.
The binding constraint is where expiring channel seats land: clause 9.2 puts each account's seats on its own subscription line, BP-4 2.1 does not reopen a lapsed line, and BP-4 1.1 counts seats per line, so only the 7,260 seats on 152 accounts with an open line come direct and the 1,927 seats on 26 lapsed-line accounts stay out.
Two further readings overshoot: booking all 9,187 MA-4101 seats gives 53,147, and joining the December return to the crosswalk code by code also takes 2,150 seats on 14 codes whose spells closed on 14 December, giving 55,297.
Determinism pins: closing base 41,820; in-quarter commitments 2,140; out-of-quarter 1,193 on 28 notes; ENT 10,800; 1,060 open lines; 12,510 billing events; 9,560 invoices; USD 13,554,673 invoiced; reseller seats 15,682; net movement +3,747; receivables USD 1,097,040; 36 silent movers.

### Stakeholder ask (the prompt, verbatim)

Seat billing runs a quarter behind the revenue plan, and the 2026 Q1 plan closes on Friday. The December close is settled and the contract book is signed. Finance has been working from the seat count the provisioning feed reports and wants the plan built on that.

Tell us how many seats the 2026 Q1 plan should be built on. One committed number.

The materials Revenue Operations works from are in the supplied materials.

Write the commitment up in billing_base_commitment.pdf so the plan can be built on it as it stands.

Give the seat count the plan should be built on, as a whole number.

Give the closing billable base at 31 December 2025 as a whole number.

Give the seats the signed contract book adds inside the quarter as a whole number.

Give the closing billable base carried by the plan code holding the most seats, as a whole number, and name that plan code.

Give the seats committed by signed notes whose effective dates fall outside the quarter, as a whole number.

Close with the one change that would move the committed number, stated as a numeric threshold on seats.

Attach the supporting calculations in billing_base_workings.csv so Finance can audit them.

One row per subscription line open at the close, with its account, region, plan code, billable seats and delegated-administrator seats, each as a whole number, ordered by billable seats largest first with an integer rank from 1.

The number of subscription lines open at 31 December 2025, as a whole number.

The number of distinct billing events invoiced across 2025, as a whole number.

The number of invoices issued across 2025, as a whole number.

A total row carrying the closing base, the in-quarter commitments, the committed seat count and the settled seats, each as a whole number, so the audit ties to the commitment file.

Hand back seat_base_recomputation.py so the numbers can be rebuilt from the supplied materials.

Print the closing base, the in-quarter commitment total and the committed seat count, each as a whole number.

Print the amount invoiced across 2025, in whole USD.

Print the API calls recorded across 2025, as a whole number.

Print the API calls recorded on 31 December 2025, as a whole number.

Print the seats served through the reseller channel at 31 December 2025, as a whole number.

Print the net seat movement the event feed records for 2025, as a signed whole number.

Print the open receivables at 31 December 2025 held by accounts with more than one open subscription line, in whole USD.

Print the number of lines open at the close whose December billable seats differ from their July count with no seat movement recorded after 31 July 2025, as a whole number.

Print the settlement reconciliation: settled seats, closing base, and the difference as a whole number.

### Deliverables

`billing_base_commitment.pdf`, `billing_base_workings.csv`, `seat_base_recomputation.py` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A SaaS company's Revenue Operations team must give Finance one committed seat count for the 2026 Q1 revenue plan. The December close is settled and the contract book is signed, but Finance has been working from the provisioning feed's seat count and wants the plan built on it. From the seat ledger, subscription lines, seat event feed, invoice lines, settlement remittance, contract schedule, channel agreement register, partner seat feed and crosswalk, billing policy BP-4 and the partner master agreement terms, the analyst must establish the closing billable base, add every change taking effect inside the quarter, and decide which reseller channel seats come direct when a partner agreement expires. Deliverables are `billing_base_commitment.pdf` (the committed number, the closing base, in-quarter commitments, the largest plan code, out-of-quarter commitments, and a closing change stated as a seat threshold), `billing_base_workings.csv` (one ranked row per open line plus counts and a total row that ties to the PDF) and `seat_base_recomputation.py` (prints the headline figures and nine supporting checks from the inputs).)

`20 files, 3.6 MB`, `account_register.csv`, `billing_policy_BP4.pdf`, `channel_agreements.csv`, `contract_schedule.csv`, `data_dictionary.md`, `invoice_lines_2025.csv`, `partner_account_crosswalk.csv`, `partner_master_agreement_terms.md`, `partner_seat_feed.json`, `plan_catalog.json`, `plan_rate_history.csv`, `provenance.md`, `receivables_summary_2025.csv`, `resubscription_ledger.csv`, `seat_events.csv`, `seat_ledger_2023_2025.csv`, `service_retirement_notice.md`, `settlement_remittance_2025_12.csv`, `subscription_lines.csv`, `usage_export_2025.tsv`

### Final recommendation

Build the 2026 Q1 plan on 51,220 seats: the 41,820-seat closing base, plus 2,140 seats the signed contract book adds inside the quarter, plus 7,260 MA-4101 channel seats that come onto their accounts' open lines when that agreement expires on 31 December 2025 with no successor recorded.

### Step-by-step solution

1. Sum billable seats in the seat ledger's December 2025 month across the 1,060 open lines: 41,820 seats.
2. Tie it to the December settlement remittance: 41,820 seats for USD 1,313,782.00, line for line, so the base is not adjusted.
3. Check the three structures that make the base look high against a feed-derived count: 7,530 seats on re-subscribed accounts (separate lines under BP-4 2.1), 5,460 seats in the retired provisioning region whose feed stopped on 1 August 2025, and 4,380 delegated-administrator seats billable since 1 April 2025 under BP-4 4.2. All stay in.
4. Apply BP-4 1.3: the plan carries the prior closing base plus every change taking effect inside the period.
5. Read the contract book on effective date (BP-4 5.1): 2,140 seats inside 2026 Q1, 1,193 seats on 28 notes outside it.
6. Read the channel register: MA-4101 ends on 31 December 2025 with no successor recorded; its schedule in force at the close serves 9,187 seats across 178 open crosswalk spells, excluding the 2,150 seats on 14 codes closed on 14 December that moved to another partner.
7. Apply clause 9.2 with BP-4 2.1 and 1.1: 152 accounts with one open line bring 7,260 seats direct on 1 January 2026; 26 accounts with only lapsed lines and no signed order bring none (1,927 seats). The crosswalk's exit history agrees: 16 of 16 exits with an open line stepped that line the next month, and none of 6 without one landed seats.
8. Commit 41,820 + 2,140 + 7,260 = 51,220 seats, and close on the change that would move it: a successor agreement recorded against MA-4101 would remove 7,260 seats and return the plan to 43,960.
9. Build the ranked workings CSV with its total row and the recomputation script that prints every requested figure, including USD 13,554,673 invoiced in 2025 and USD 1,097,040 open receivables on accounts with two or more open lines.

### Key traps (what the model did)

- Resisted the provisioning-feed lure and stated the MA-4101 expiry with no successor (4/4), but treated expiring channel seats as simply leaving the base rather than following clause 9.2 that moves them onto the account's own open line; committed closing base + contract book = 43,960.

### Justification

The settlement proves the 41,820-seat closing base is what was actually billed, so none of the downward corrections the feed invites is allowed. The plan must then carry every change inside the quarter. The signed book adds 2,140 seats on effective date, and the MA-4101 expiry moves channel seats onto direct lines, but only where an open line exists for them to land on. That gives 7,260 seats, not the full 9,187, and a committed plan of 51,220 seats.

## Attribute hungary's q3 2024 contraction to net trade, not investment

**Quarterly National Accounts**, Batch 14, Economics, model mean **0.66** over 4 runs (0.60, 0.71, 0.76, 0.66).

### What makes it strong (the client's note)

The trap is reading component growth rates at face value: Hungary's gross capital formation fell 2.0 percent, which looks like the culprit, but it carries only about -0.44 pp once weighted, while imports rising 1.1 percent take about -0.99 pp off GDP.
A second trap is Iceland, which has the deepest real contraction (-0.7 percent) and a large investment fall, but its weighted bridge confirms the investment reading, so it shows no headline versus expenditure mismatch.
The computation chain joins observations to the dimensions, screens 40-plus geographies on the real and nominal Q3 changes, converts Q2 to Q3 chain-linked volume moves into GDP contributions using Q2 GDP as the scale, and signs imports negatively.
Determinism pins: the screen returns exactly Iceland, Malta, Hungary and Poland; Hungary real GDP -0.3 percent with current-price GDP up EUR 531m; Hungary domestic demand about +0.66 pp against net trade about -0.92 pp.

### Stakeholder ask (the prompt, verbatim)

I need to go through the Eurostat numbers for Q3 2024 and find the individual countries where real GDP dropped even though GDP at current prices still went up. Leave out the EU and euro-area totals. From there, figure out which country has the biggest mismatch between what the headline numbers suggest and what the spending breakdown actually shows. Work out what really drove the decline and which other country looks most similar once the details are lined up.

Put the answer in three files. Use q3_contraction_rca.pdf for a short memo with the final call and the key figures, q3_contraction_dashboard.html for a simple side-by-side comparison, and q3_contraction_audit.xlsx for the calculations and source rows so someone else can trace the work back. Use one decimal place for percentages and round euro changes to the nearest million. Stick to the supplied files and make sure the three outputs agree.

The headline story may not hold up once the expenditure side is checked, so I want the components looked at together rather than taking the first obvious explanation at face value. A couple of countries may look close at first, but the final choice should come from the underlying numbers.

### Deliverables

`q3_contraction_rca.pdf`, `q3_contraction_dashboard.html`, `q3_contraction_audit.xlsx` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A macro analyst working from a Eurostat quarterly national accounts extract (namq_10_gdp, seasonally and calendar adjusted, with country, item, unit and time dimensions) must find the individual countries whose real GDP fell in Q3 2024 while current-price GDP still rose, leaving out the EU and euro-area aggregates. From that screen the analyst picks the country where the headline reading and the expenditure breakdown diverge most, works out what actually drove its decline by weighting each component's volume change by its size (imports entering with a negative sign), and names the other country that looks most similar once components are lined up. Deliverables are `q3_contraction_rca.pdf` (a short memo with the call and key figures), `q3_contraction_dashboard.html` (a simple side-by-side comparison) and `q3_contraction_audit.xlsx` (calculations and source rows), with percentages to one decimal place, euro changes to the nearest million, and all three files agreeing.)

`10 files, 12.0 MB`, `KS-01-13-429-3A-C-EN.PDF.pdf`, `KS-GQ-13-004-EN.PDF`, `KS-GQ-14-005-EN-N.pdf`, `data_dictionary.json`, `dim_geo.csv`, `dim_na_item.csv`, `dim_time.csv`, `dim_unit.csv`, `observations.csv`, `overview.xlsx`

### Final recommendation

Hungary shows the biggest mismatch: real GDP fell 0.3% while current-price GDP rose EUR 531m, and its contraction was driven by net trade (imports up 1.1%, about -0.9 pp) rather than by the 2.0% fall in gross capital formation (about -0.4 pp), with domestic demand still positive.

### Step-by-step solution

1. Join the Eurostat observations to the country, item, unit and time dimensions, keep the seasonally and calendar adjusted series for 2024 Q2 and Q3, and drop the EU and euro-area aggregates.
2. Screen for countries whose Q3 real GDP change is negative while current-price GDP rose. This leaves Iceland (-0.7 percent, EUR 41m), Malta (-0.4 percent, EUR 39m), Hungary (-0.3 percent, EUR 531m) and Poland (-0.1 percent, EUR 5,252m).
3. For each candidate, turn the Q2 to Q3 chain-linked volume change of final consumption, gross capital formation, exports and imports into a GDP contribution scaled by Q2 real GDP, with imports entering negatively and parent lines used without double counting subcomponents.
4. Hungary shows the strongest mismatch: the raw rates point to gross capital formation (-2.0 percent), but its contribution is only about -0.44 pp.
5. Final consumption contributes about +1.09 pp, so Hungary's domestic demand is still positive at about +0.66 pp.
6. Net trade contributes about -0.92 pp, driven by imports at about -0.99 pp against exports at about +0.07 pp, making external trade the root cause.
7. Check Iceland: gross capital formation fell 2.8 percent and contributes about -0.71 pp while net trade is a small positive offset (about +0.09 pp), so the first-pass investment reading holds there and there is no reversal.
8. Line up the remaining candidates: Malta also combines positive domestic demand with a net trade drag (imports about -2.0 pp), so it has the driver profile closest to Hungary's.
9. Report the same figures in the PDF, the dashboard and the audit workbook, keeping source rows, flags and the contribution bridge in the workbook.

### Key traps (what the model did)

- Selected Poland as the biggest headline-versus-expenditure mismatch (and Austria / Hungary / Iceland as the closest match) using its own loosely defined mismatch metric, even though its own tables showed Hungary's import-led drag; Malta never named as Hungary's peer.
- Reported component contributions separately but never aggregated them into the decision quantities (domestic demand total, net trade total), so the key comparison is never stated.

### Justification

Component growth rates do not show how much each component moved GDP, because each one has to be weighted by its size and imports subtract from output. On that basis Hungary's 2.0 percent investment fall costs well under half a point, consumption more than offsets it, and a 1.1 percent rise in imports, applied to an import base close to GDP itself, removes nearly a full point. That is the largest gap between the obvious headline story and the expenditure evidence among the four screened countries. Iceland's investment-led reading survives the same check, so it is not the mismatch case.

## Hold the 2027 opening allocation and do not weight openings toward indiana

**Restaurant Labor Market Policy**, Batch 14, Economics, model mean **0.68** over 4 runs (0.81, 0.60, 0.68, 0.69).

### What makes it strong (the client's note)

The trap is the comparison window: opening it at the first Illinois wage step (2020Q1) yields -10.8% with an interval that excludes zero (p = 0.016) and reads as a decisive case for Indiana, but Illinois kept capacity limits until 2021-06-11 while Indiana lifted them on 2020-09-26, so those quarters measure reopening timing alongside wages.
On the comparable window from 2021Q3 the eating-and-drinking gap is -10.7% with a 95% interval of about -22% to +3% (p near 0.11 to 0.14 depending on the clustered-error approximation); the point estimate barely moves but the interval now spans zero, and retail (-6.9%) and all industries (-2.9%) are smaller and not significant.
Illinois was never one treatment group: the Chicago and Cook County ordinances took the binding floor to $13.00 by 2019 while downstate stayed at $8.25, and Cook food-service employment indexed to 2016Q4 finished 2019 at 105.1 against Lake County's 104.5, so the corpus's own large early increase shows no employment loss.
Determinism pins: 30 comparisons with 3 nominally significant (1.5 expected by chance), new hires -15.7% to -17.2% (all accessions or new hires only) and separations -15.2% (a hiring slowdown, not layoffs), and Indiana counties holding 8.2% of combined food-service employment (21,658 against 243,014 in 2024Q4).

### Stakeholder ask (the prompt, verbatim)

Bit of a long one, sorry , I need a second pair of eyes before the partners meet.

We run restaurants and taverns on both sides of the Illinois-Indiana line. Chicago and Gary up north, Danville and Clinton in the middle, a couple of places down around Mount Carmel. Our Illinois payroll has climbed every year since 2020 and the Indiana side hasn't moved, and the room is split about what that means. Ray wants two thirds of the 2027 openings on the Indiana side. Denise thinks we'd be managing to a payroll line and walking away from the better markets, and that if Illinois were really killing operators we'd have seen it in the numbers by now rather than just in our own P&L.

I don't want a survey of both views. I want you to work the public data and come back with the call: do we weight 2027 openings toward Indiana, or hold the allocation where it is? Say which, in a sentence I can read out loud without hedging it for them.

What I've attached is the public employment record for the counties we're in, plus the wage rules and the state policy records that cover the same stretch. That's what I could get. Work with it and tell me what it genuinely supports rather than what our payroll line feels like.

Some things I'll want to see addressed, because they're what Ray and Denise will argue about the moment you're done.

Ray's case is that the Illinois shortfall is obvious in the data. If that's right I want the number, for eating-and-drinking places specifically, and I want to know how firm it is , not just the estimate but the range you'd actually defend, and whether it holds up when you look at retail and at total employment instead. Denise will say you went looking until you found something. If you ran the comparison several ways, tell me how many ways you ran it and how many came back looking meaningful, because she'll ask and I'd rather hear it from you first.

Denise's case is that our own history already answers this. We've been operating in Cook County a long time and our labor costs there ran ahead of the rest of Illinois well before Springfield did anything. I want to know whether all our Illinois locations have actually been under the same wage floor across this period, and if not, what happened to employment in the places that got there first. If that's not the picture I have in my head, say so plainly.

Then two things neither of them will raise. First: I need to know whether what we're seeing is Illinois operators cutting staff or just not hiring, because those point at different things for us , one says the market's shrinking, the other says it's tight and we'd struggle to staff a new opening either way. Second, and this is the one I actually care about: whatever gap you land on, tell me whether it's big enough to matter for a decision like this one. A number can be real and still be too small to move where we put eight million dollars, and I'd rather you told me that than let me read something into it.

Send me three things. A short memo with the call up front and the two or three findings it rests on, each one a number I can check rather than a description. Whatever working file you built the estimates in, so I can hand it to our accountant , every comparison you ran, not just the ones that survived, with the counties named. And a chart of the two sides over the whole period that lets me see the thing you're describing, marked up wherever the wage rules changed, because I'll be putting it on the screen and I'd rather it made the point without me narrating it.

If part of this comes down to a judgment call rather than the data, I'd rather know which part. But I still need the call.

### Deliverables

`employment_chart.png`, `memo.docx`, `working_estimates.xlsx` (Every file is prescribed by name. Nothing is optional, and no single file carries the whole answer.)

### Input files (A restaurant and tavern operator with locations on both sides of the Illinois and Indiana line has to decide whether to put two thirds of its 2027 openings on the Indiana side, as one partner argues because Illinois payroll keeps rising, or hold the current allocation. Working only from public Census QWI county-quarter employment for six border counties (Cook, Vermilion and Wabash in Illinois; Lake, Vermillion and Gibson in Indiana, 2015 to 2024), the state and local minimum wage schedules, and the two states' COVID reopening timelines, the analyst must estimate the Illinois shortfall in eating-and-drinking employment with an interval, test it against retail and total employment, report how many comparisons were run and how many were significant, establish that Illinois locations were not under one wage floor and what happened where the floor rose first, separate reduced hiring from staff cuts, and judge whether the gap is large enough to move the allocation. Deliverables are a short memo with the call in its first sentence and two or three numeric findings, a working estimates file listing every comparison with counties named, and a chart of the two sides across the whole period marked at the wage changes.)

`8 files, 4.8 MB`, `Indiana2009MinimumWage.pdf`, `file_manifest.csv`, `il_in_minimum_wage_history.csv`, `local_minimum_wage_ordinances.csv`, `local_ordinance_coverage_notes.md`, `minimumwagehistoricrates.pdf`, `qwi_six_counties_2015q1_2024q4.csv`, `state_reopening_policy_timeline.json`

### Final recommendation

Hold the 2027 opening allocation where it is and do not weight openings toward Indiana. The Illinois food-service gap on the comparable window is -10.7% with an interval that includes zero, and the Indiana side holds only 8.2% of the combined food-service labor market.

### Step-by-step solution

1. Load the QWI county-quarter records for the six counties, 2015Q1 to 2024Q4, keeping eating-and-drinking places (NAICS 72), retail and all-industries employment, plus new hires and separations.
2. Build the binding wage floor for each county-quarter from the federal, state, county and municipal schedules. Cook County reached $13.00 by 2019Q4 under the Chicago ordinance while downstate Illinois stayed at $8.25 and Indiana at $7.25, so Illinois is not one treatment group.
3. Read the reopening records: Illinois lifted all capacity limits on 2021-06-11 and Indiana on 2020-09-26, an 8.5-month gap. The first fully comparable quarter is 2021Q3.
4. Check pre-trends: an Illinois-specific trend over 2015 to 2019 is flat (+0.00022 per quarter, p = 0.973), so the design holds.
5. Estimate the Illinois-versus-Indiana food-service gap with county and seasonal effects, a pre-2020 baseline and errors clustered by county: -10.7%, 95% interval about -22% to +3% (upper bound above zero), p about 0.11 to 0.14.
6. Re-estimate from 2020Q1: -10.8%, interval -18.7% to -2.1%, p = 0.016. The estimate is unchanged; only the interval tightens, borrowed from the capacity-rule quarters.
7. Repeat for retail (-6.9%, p = 0.142) and all industries (-2.9%, p = 0.335).
8. Drop Cook and run the downstate pairs alone: -9.7%, interval -20.8% to +2.9%. Drop each county in turn: estimates run -14.9% to -6.1% and never change sign, but p runs 0.010 to 0.313.
9. Count the comparisons: 30 across three sectors, three windows, two county groupings and three measures, 3 nominally significant against 1.5 expected by chance, in unrelated cells.
10. Compare Cook and Lake food-service employment while Cook's floor rose 58%: 105.1 against 104.5 at 2019Q4 on a 2016Q4 base, no detectable effect.
11. Estimate flows: new hires -15.7% on all accessions or -17.2% on new hires only and separations -15.2% (p = 0.138), falling together, which points to reduced hiring rather than staff cuts.
12. Size the decision: Indiana counties hold 21,658 food-service jobs against 243,014 in Illinois, 8.2% of the combined total.
13. Conclude: hold the allocation, and deliver the memo, the 36-row estimates file and the annotated chart.

### Key traps (what the model did)

- Got the hold call right 4/4 but used an ad hoc pre/post window (2019 vs 2022-24 averages, or 2022Q1 start) not aligned to the policy confounder (Illinois capacity limits until 2021-06-11), producing a wholly negative interval that reads as a decisive effect.
- Never quantified materiality (Indiana = 8.2% of combined food-service employment) or set the significant count against chance (3 of 30 vs 1.5 expected).

### Justification

The only window in which the two states operated under the same restaurant rules starts in 2021Q3, and on that window the Illinois food-service shortfall is -10.7% with a range running from about -22% to about +3%, so no effect at all is inside the range. The alternative reaches a significant result only by starting in 2020, which adds the quarters when Indiana could seat customers and Illinois could not, or by dropping a county without a reason to. The corpus also contains its own test of the wage story: Cook's floor rose 58% before 2020 and its food-service employment kept pace with Lake County. Hires and separations fell together, which describes a tight market rather than a shrinking one. And even taking the gap at face value, the Indiana counties are 8.2% of the combined food-service market, too small for this number to justify moving two thirds of the openings there.
