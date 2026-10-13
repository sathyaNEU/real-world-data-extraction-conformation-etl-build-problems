# leak check, task452

**Verdict: REVIEW.** 13 files read, 63 golden figures and 10 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: samples, discharge, concentration, record, decisive, laboratory, unsampled, estimator, watershed, method, contract, college, provisional, rating, overuse, golden, minute, agreement, tributaries, sentence, storms, reports, objective, closed, allocations

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `brannoch_lake_phosphorus_agreement.pdf`: golden figure 660 appears: ...Varrow Brook BLC-05 3,240 Hessick River BLC-06 5,660 Pellow Brook BLC-07 800 Ambrey River BLC-08 3,380...
- **REVIEW** `brannoch_lake_phosphorus_agreement.pdf`: golden figure 280 appears: ...lowmere Brook BLC-01 1,200 Kestle River BLC-02 14,280 Orrinwood Brook BLC-03 2,390 Tamsell River BLC-04...
- **REVIEW** `brannoch_lake_phosphorus_agreement.pdf`: carries 10 of 10 distinctive words of the committed call: 'Fund the 2027 tributary restoration projects in the Kestle River, the Hessick River and Varrow Brook.'
- **REVIEW** `merrifield_data_transmittal_2026-12-14.txt`: carries 7 of 10 distinctive words of the committed call: 'Fund the 2027 tributary restoration projects in the Kestle River, the Hessick River and Varrow Brook.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `blc_tributary_monitoring_program_2024-2026.docx`: 11 of 25 stump-paragraph terms appear (samples, discharge, record, laboratory, watershed, contract); read whether the document names the move
- **REVIEW** `brannoch_lake_phosphorus_agreement.pdf`: 13 of 25 stump-paragraph terms appear (samples, discharge, concentration, record, laboratory, watershed); read whether the document names the move
- **REVIEW** `merrifield_data_transmittal_2026-12-14.txt`: 5 of 25 stump-paragraph terms appear (discharge, record, provisional, rating, minute); read whether the document names the move

## 6 ranking artifacts (REVIEW 4, INFO 1)
- **REVIEW** `blc_station_register.xlsx`: names 10 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `brannoch_lake_phosphorus_agreement.pdf`: names 10 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `farm_practice_contracts_2024-2027.csv`: names 10 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `merrifield_data_transmittal_2026-12-14.txt`: names 10 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `practice_field_watershed_acres.csv`: names 10 of 10 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

### 1. Decisive step
none. The agreement 3.1 ("the three tributaries whose load for the water year just closed exceeds its allocation by the most kilograms") states the selection rule; 1.4 ("estimated from the tributary monitoring record: the Commission's samples, the storm samples the Ashgrove College Watershed Laboratory takes ... and the gage record") says what inputs feed load. No sentence says how to estimate load (no method named).

### 2. Ranking file
none. Schedule 1 lists allocations only; no file gives loads or excess.

### 3. Analyst-helper file
none clearly. The weather file, lake summer monitoring xlsx and the 2024-25 daily values read as ordinary organisational products (context/distractors). The 2026 provisional file is a legitimately superseded delivery.

### 4. Answer-like figures or names
none. Allocations (e.g. Kestle River 14,280) are context. The prompt's file names restoration_slate_2027.docx and tributary_loads_wy2026.csv are outputs, not shipped.

### 5. Sentences fixing the figure
- Agreement 1.1: "Water year means the twelve months from 1 October to 30 September" : Oct 2025 to Sep 2026.
- 1.3: "unfiltered sample ... expressed as P" : total phosphorus fraction, not dissolved.
- 1.4: load is "the mass of total phosphorus carried past a tributary's compliance station during a water year, in kilograms, estimated from ... the Commission's samples, the storm samples [from the college lab] ... and the gage record" : population is the whole water-year flux, not just sampled days; storm samples are included; method open.
- 2.2: "A tributary's load above its allocation is its load less its allocation. Comparisons ... are made on unrounded loads." : rank by unrounded excess kg.
- 3.1: top three by excess kg; fewer than three if fewer exceed.
- Transmittal: "Approved values above replace them" (provisional); "Unit values are stamped in ... UTC. Daily values are means over local calendar days"; ratings of 01-4420 and 01-4480 shifted from 1 August 2026. Consequence: use approved file, convert UTC to local/water-year bounds.
- Program doc: "Each compliance station has a gage at the station except Dunmarsh Brook, whose gage is 4.2 km upstream; the register gives both drainage areas." Consequence: Dunmarsh flow needs area scaling (61.4/52.8).
- Program doc: sampling "first and third Tuesdays ... whatever the weather" plus college storm samples "during high water". Consequence (as read literally): routine samples are fixed-schedule, storm samples are in the record; the file does not say how to combine.

### 6. What decides the main answer
An analytical choice. Nothing filed names the estimator. I would build a flow-paired concentration model (rating curve or composite/regression style load estimate, e.g. log concentration vs log flow with season terms) using accepted total-P results (unit-harmonised ug/L vs mg/L, drop Rejected, handle Not Detected at the limit, exclude blanks, treat replicates sensibly), apply it to the 15-minute approved flow for the water year, sum to kg, subtract allocation. The naive path (mean of routine concentrations times total flow) is visible and the pack leaves the choice open; the data (sampling by calendar, storms sampled by the college) is what separates the methods. Semantics (units, codes, UTC) are mess, not the decider.

### 7. Realism
Mostly authentic: WQX-style column names, DMR layout with lb/d and resubmissions, USGS-style header comments, transmittal letter. Minor: the program document and register are very tidy; allocations that sum to round numbers per tributary; the transmittal's row counts exactly 350400 (365 days x 96 x 10) is plausible. Nothing glaring. The register note "Sampling station 4.2 km downstream of gage 01-4490" is consistent with the program doc.

### 8. Supporting figures
Facilities: register "Facilities" sheet (receiving water, outfall river km, in-service dates), "Streams" sheet (tributary junction river km, for which tributary a side stream joins) and the station river km above lake (Station river km above lake) decide upstream status. Outfall 001 of Ambrey Village ends 2026-03-31 and outfall 002 begins 2026-04-01 (two outfalls, one permit, split year). Agreement 4.1(a) fixes the calc: "each month's average daily discharge (the monthly average concentration times the monthly average flow, or the monthly average mass) times the days in the month". DMR file: MO AVG concentration in mg/L, flow in MGD, some lb/d, 21 Resubmissions (use the latest). Possible ambiguity: the register's "Outfall river km" is measured on the receiving water (e.g. Hollin Brook 2.1) while a tributary join is "Joins at river km" on the main stem; comparing outfall to the compliance station requires the join km vs station km, which is implied rather than stated (station km above lake vs outfall km measured in what direction is not defined in any sentence). That is the one two-way reading, at the edge of the register. Acres: farm_practice_contracts (practice Cover Crop, first_crop_year/last_crop_year, amendment_no/amended_on, contracted_acres, watershed) and practice_field_watershed_acres.csv (share_of_field per watershed, which sums to 1 per field and overrides the contract's single watershed). Agreement 4.1(b): "the acres of cover crop under ... contracts in its watershed for the crop year in which the water year ends" : crop year 2026. Amended contracts (18) likely supersede rows; the filed text does not say whether an amended row replaces the original. No other sentence reads two ways.

### Sweep lines
- Golden figure 490 (agreement): harmless, a substring of the Schedule 1 allocations (3,490), context data.
- Golden figure 660 (agreement): harmless, substring of 5,660 Hessick allocation.
- Golden figure 240 (agreement): harmless, substring of 3,240 Varrow allocation.
- Agreement carries 10 of 10 words of the committed call: harmless, 3.1 is the stated selection rule (top three by excess); it names no tributary, the sweep matched generic words (fund, projects, tributary, river, brook).
- Transmittal 7 of 10 call words: harmless, matches only generic words (tributary, river, brook, etc.); no call or ranking.
- Monitoring program docx 8 of 25 stump terms: harmless, it describes sampling, labs and units as ordinary program documentation; it does not name any estimation move (no mention of bias, flow weighting or regression).
- Agreement 10 of 25 stump terms: harmless, 1.4 lists the inputs (samples, storm samples, gage record) without naming a method.
- Transmittal 3 of 25 stump terms: harmless, discharge/record/provisional are data-delivery vocabulary.
- Register names 10 of 10 candidates beside numbers: harmless, it holds drainage areas, river km and coordinates; no loads, no ranking.
- Agreement names 10 of 10 beside numbers: harmless, allocations only, no loads or excess; the 3.1 rule names no outcome.
- Transmittal names 10 of 10 beside numbers: harmless, drainage areas only.

Disposition of pass 1 (main thread): Q1 to Q6 clean; the two Q8 readings (the river-km datum, an amendment against the contract) closed in the generator before pass 2.

## Solver's-eye read, pass 2

### 1. Decisive step for the main question
none that announces it. The only filed statement of the rule is the agreement, "3.1 ... one in each of the three tributaries whose load for the water year just closed exceeds its allocation by the most kilograms" (brannoch_lake_phosphorus_agreement.pdf). That is the selection rule, not the estimation step. The load method is only bounded by "1.4 ... estimated from the tributary monitoring record: the Commission's samples, the storm samples the Ashgrove College Watershed Laboratory takes ... and the gage record" and "2.2 Comparisons under this agreement are made on unrounded loads."

### 2. Files that rank or score tributaries
none. Schedule 1 lists allocations only. No file holds loads, exceedances or a ranking.

### 3. File that exists only to help the analyst
none clearly. The closest are the register's "Streams" and "Facilities" sheets (outfall river km, joining river km), which the Commission could plausibly keep for the report in 4.1(a); lake_brannoch_summer_monitoring and the weather file read as distractors the organisation would hold anyway.

### 4. Figure or name that reads as the answer
none. The Schedule 1 allocations and the register carry no result. The only answer-like text is the sweep's own match to the prompt's wording, not a filed sentence.

### 5. Filed sentences that fix the main figure
- "Water year means the twelve months from 1 October to 30 September, named for the calendar year in which it ends" (1.1): window 1 Oct 2025 to 30 Sep 2026.
- "Load means the mass of total phosphorus carried past a tributary's compliance station during a water year, in kilograms" (1.3, 1.4): total P, unfiltered, as P, at the station, kg.
- "estimated from the tributary monitoring record: the Commission's samples, the storm samples the Ashgrove College Watershed Laboratory takes ... and the gage record" (1.4): both sample sets count, gage record supplies flow; the estimator is not named.
- "A tributary's load above its allocation is its load less its allocation. Comparisons ... on unrounded loads." (2.2): rank on kg exceedance, unrounded.
- "the three tributaries whose load ... exceeds its allocation by the most kilograms" (3.1): top three by kg over, not by percentage.
- Transmittal: "Unit values are stamped in Coordinated Universal Time"; "The approved values above replace them"; "Two gages' ratings were shifted ... 01-4420 ... and 01-4480 ... from 1 August 2026": use the approved file, UTC stamps converted for the local-day and water-year edges; provisional file is out.
- Register note on Dunmarsh: "Sampling station 4.2 km downstream of gage 01-4490" with areas 61.4 vs 52.8: gage flow must be scaled to the station for BLC-09.
- Monitoring program: "Commission staff sample every station on the first and third Tuesdays ... whatever the weather"; "the college samples stations during high water": routine samples are fixed-schedule, storm samples are event-biased. Result status "Accepted ... or Rejected"; the unit and name changes at 1 July 2025 (ug/L, "Total Phosphorus, mixed forms").

### 6. What decides the main answer
An analytical choice: how to estimate each station's annual load from about two samples a month plus event samples against a 15-minute flow record. Nothing filed names the estimator. The nearest sentences are 1.4 and the two program sentences on sampling ("whatever the weather", "during high water"), which describe the data, not the move. The easy route (mean concentration times total volume, or Commission samples only, or a plain average of all samples including storm-biased ones) is available and the file set does not say it is wrong. Cleaning items (units, rejected results, UTC, approved vs provisional, Dunmarsh area) are mess, not decisive. My own estimate: per station, build a concentration against discharge relation from accepted total P results (both sets, units harmonised, non-detects handled at the limit or half), predict it on every 15-minute flow value in the approved record converted to the water year window, sum to kg, scale Dunmarsh by area, compare with Schedule 1.

### 7. Realism
Mostly reads real: WQX-style column names, ECHO-style DMR columns, USGS-style comment headers, a consolidated agreement with amended date. Possible tells: register has a Dunmarsh area (61.4) that differs from the transmittal's own 52.8 only for the gage, which is explained; the farm contracts file repeats the contract-total acres on every field row of a contract (an odd export, but it matches "Contracts enrol whole fields"); a clean 12-gage-by-3-figure rating shift story. Station names all follow one pattern (X Brook or X River, one treatment plant each), which is a little tidy. Nothing dated after the setting beyond the exports (January 2027 file dates; the water quality file is dated 2027-01-08, consistent).

### 8. Supporting figures
Facilities: agreement 4.1(a) fixes the measure: "phosphorus discharged during the water year by permitted facilities whose outfalls are upstream of its compliance station ... each month's average daily discharge (the monthly average concentration times the monthly average flow, or the monthly average mass) times the days in the month". Deciding files: blc_station_register.xlsx (Facilities sheet outfall, receiving water, river km, in-service dates; Streams sheet join km; Stations sheet station river km) and npdes_dmr_phosphorus_wy2026.csv (MO AVG phosphorus and flow, units mg/L, MGD and lb/d; Original vs Resubmission; period start and end). Upstream is decided by receiving water either being the tributary or joining it, and the outfall km being above the station km (for example Ambrey 002 at km 0.8 and Dunmarsh at 0.8 are below stations at 2.2 and 1.5; Ambrey 001 stops 2026-03-31, 002 starts 2026-04-01). Days per report: the report's period; most are monthly (30 days max span) but about half the facilities file quarterly periods (span up to 91 days), so a report stands for the days from start to end inclusive, not one month. Resubmission rows exist for 21 rows and the register does not say they replace the Original, but a literal reader will take the later one. Reading two ways: 4.1(a) says "times the days in the month" while quarterly rows span several months, and the Original and Resubmission rows both appear without a filed supersession sentence. No file narrates a pitfall.
Acres: 4.1(b) "acres of cover crop lying in its watershed on fields under the ... Program's contracts for the crop year in which the water year ends" (crop year 2026). Deciding files: farm_practice_contracts_2024-2027.csv (header comment: "Contracts enrol whole fields. Amendment 0 is the contract as signed; an amendment restates the contract, and the latest amendment is the contract in force for every crop year it covers.") with first_crop_year and last_crop_year, and practice_field_watershed_acres.csv (field_acres and share_of_field by watershed, so a field straddling two watersheds is split). Contracted_acres is a contract total repeated on every field row, so it is not an acres figure per watershed; field acres times share is. Reading two ways: the contracts' watershed column versus the split file, and contracted acres versus field acres, are not reconciled by a filed sentence beyond "lying in its watershed". No file narrates a pitfall.

### Sweep lines
- golden figure 280 in agreement (Fallowmere 1,200 / Kestle 14,280 ...): harmless, "280" is the tail of the printed allocation 14,280 in Schedule 1, an input.
- golden figure 660 in agreement (5,660): harmless, tail of allocation 5,660, an input.
- 10 of 10 words of the committed call in agreement: harmless, the words are tributary names, "Fund", "projects" and "2027" that occur in Section 3 and Schedule 1; no sentence names the three chosen tributaries as a decision.
- 7 of 10 words of the call in transmittal: harmless, tributary names and gage names listed in a gage table; no selection stated.
- 10 of 25 stump terms in monitoring program docx: harmless, it describes sampling and lab reporting as an operator would; it does not say loads must be modelled from flow or that storm samples bias a mean. (The "whatever the weather" and "during high water" sentences are the nearest and still describe the data only.)
- 12 of 25 stump terms in agreement: harmless, definitions of load and sample sources in 1.4; does not name a method.
- 5 of 25 stump terms in transmittal: harmless, discharge, provisional, rating shift are delivery notes; they point to using approved data (Layer 1 mess), not the load estimator.
- station register names 10 of 10 candidates beside numbers: harmless, areas and river km only, no ranking.
- agreement names 10 of 10 candidates beside numbers: harmless, allocations are an input to the comparison, not a ranking.
- farm contracts names 10 of 10 candidates beside numbers: harmless, acres by watershed, no ranking on the decision question.
- transmittal names 10 of 10 candidates beside numbers: harmless, drainage areas only.

Disposition of pass 2 (main thread): Q1 to Q6 clean, every sweep line harmless. Q8's two readings (4.1(a)'s days in the month against quarterly reports; an original against its resubmission) left as filed: the re-judge executed both to the golden (each report stands for the days of its period; the latest received submission replaces the original) and found no fork.
