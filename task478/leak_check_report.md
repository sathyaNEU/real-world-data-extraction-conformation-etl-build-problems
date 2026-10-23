# leak check, task478

**Verdict: REVIEW.** 14 files read, 26 golden figures and 17 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, reader, content, method, decisive, section, carried, pothole, window, landed, readers, loaded, source, monitored, carries, burner, district, standard, device, covers, golden, pattern, boiler, reading, meters

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `tbapcd_lowry_creek_cerp_2027.pdf`: carries 14 of 15 distinctive words of the committed call: 'Sign the 2027 NOx reduction agreements with Ashgrove Refining, Valmora Renewable Fuels, Sedge Hollow Creamery, Lindqvist'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `tbapcd_emission_inventory_guidance_2026.pdf`: 10 of 25 stump-paragraph terms appear (content, method, section, source, district, standard); read whether the document names the move
- **REVIEW** `tbapcd_lowry_creek_cerp_2027.pdf`: 8 of 25 stump-paragraph terms appear (content, section, source, carries, burner, district); read whether the document names the move

## 6 ranking artifacts (REVIEW 3)
- **REVIEW** `tbapcd_lowry_creek_cerp_2027.pdf`: names 13 of 17 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `tbapcd_permit_devices.csv`: names 14 of 17 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `tbapcd_rule4702_engine_logs_2026.xlsx`: names 14 of 17 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 8 column names (REVIEW 6)
- **REVIEW** `tbapcd_compliance_events_2018_2026.csv`: columns a generator names and an organisation does not: DEVICE_NO
- **REVIEW** `tbapcd_emission_statements_2018_2026.csv`: columns a generator names and an organisation does not: DEVICE_NO
- **REVIEW** `tbapcd_engine_inspections_2025_2027.csv`: columns a generator names and an organisation does not: DEVICE_NO
- **REVIEW** `tbapcd_permit_devices.csv`: columns a generator names and an organisation does not: DEVICE_NO
- **REVIEW** `tbapcd_rule4702_engine_logs_2026.xlsx`: columns a generator names and an organisation does not: Device
- **REVIEW** `tbapcd_source_tests_2018_2021.csv`: columns a generator names and an organisation does not: DEVICE_NO

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

- Architecture 5, round 1 (zip md5 feba8739), readers A and B: both missed the call on the default path (the gross as
  recorded); both kept all 24 ask figures. No decisive-step sentence, no helping file, no ranking artifact named.
- Architecture 5, round 2 (zip md5 98e0e301, asks re-sited), reader C: landed the call (score_reader exit 1, call 1 of
  1, ask figures 32 of 36 with the shares). Question 1: no sentence states the decisive step; the nearest is program 2.2
  ("Gross vehicle weight is the weight of the whole truck as the law measures it, on a certified static scale"). Its
  route: each station's gain measured on the classes other than 9 against the four stations that agree, class 9 divided
  by it. Reader D stopped at the spend. The architecture is spent (design note, Tried and rejected).

## Solver's-eye read

Two isolated readers (Sonnet, medium), each on a fresh copy of prompt.txt and target/ (zip md5 946c7506).

Reader A. Q1: none stated; nearest "the NOx emission rate it operated at over the year" (guidance section 3). Q2: none.
Q3: the guidance. Q4: none. Q5: plan 2.2 and guidance section 3, leaving how a year's rate comes from tests at
different catalyst ages open. Q6: an analytical choice, the year's rate from snapshot tests along catalyst operating
hours. It filed the golden five (score_reader: the five as a set; 14 of 14 tons, 14 of 14 gas, 7 of 14 engines).

Reader B. Q1: guidance sections 2 and 3 and plan 2.2. Q2: none. Q3: the guidance. Q4: none. Q5: guidance section 3,
read with each test's rate applied from its test date. Q6: mostly the stated procedure on messy data, with an
analytical choice in the year's rate. It filed the default five (10 of 14 tons, 3 of 14 gas, 14 of 14 engines) and
called the index meters' usage switching to therms in July "a reconciliation clue, not an answer-giving leak".

Every REVIEW line: harmless to both readers (the plan's roster, Method 19 and source test wording, the DEVICE_NO
columns as the district's own field names).

## Solver's-eye read

Round 1, architecture 7 (zip md5 2936a1ef, 2026-10-23), two isolated readers (Sonnet, medium) on fresh copies of prompt.txt and target/.

### Reader v7a

```
# Part 2

1. none. The closest is guidance section 3: "Rule 4306 section 6.3 requires each unit without a monitoring system to be source tested for NOx every 12 months, or every 24 months where the permit allows a reduced frequency" (tbapcd_emission_inventory_guidance_2026.pdf), which does not say which test governs.
2. none. No file ranks facilities by NOx.
3. tbapcd_emission_inventory_guidance_2026.pdf (its section 7 file list and the formulas); also the Appendix A of tbapcd_lowry_creek_cerp_2027.pdf for facility numbers and BTU areas.
4. none. No figure or name reads as the answer; the CERP lists all fourteen facilities alphabetically-unordered with no emissions.
5. tbapcd_lowry_creek_cerp_2027.pdf 2.1-2.2: "the five facilities in the corridor whose units subject to Rule 4306 emitted the most oxides of nitrogen ... in calendar year 2026, in tons" and "A facility's emissions are the sum over its Rule 4306 units". Literal result: the five above. For the gas, 4.2: "each billing period's therms spread evenly over the days of its read period, from the day of its prior read to the day before its current read", which gives the gas figures above. The guidance does not file which source test applies to a year.
6. Mostly an analytical choice plus reconciling sources: deciding that each uncontrolled unit's year is measured by the test taken in that year (Sedge Hollow's 2026 tests show the drift; using the prior test would swap Sedge Hollow for Merriwell), and judging the engine logs against the compliance-log outage durations and hour meters. Much of the remaining work is following stated procedures (guidance sections 2-6). No sentence announces it; the deciding material is the 2026 versus 2025 source test rows in tbapcd_source_tests_2022_2026.xlsx.

# Part 3

- tbapcd_lowry_creek_cerp_2027.pdf, 14 of 15 call words: harmless, the names and the phrase are the prompt's own wording and Appendix A's roster; no emissions beside them.
- tbapcd_emission_inventory_guidance_2026.pdf, 10 of 25 stump terms: harmless, generic method vocabulary; it does not say which test governs or that logs may double-count.
- tbapcd_lowry_creek_cerp_2027.pdf, 9 of 25 terms: harmless, ordinary plan text (burner replacement, district, section).
- tbapcd_lowry_creek_cerp_2027.pdf, 13 of 17 candidates beside numbers: harmless, the numbers are facility numbers and addresses, no ranking.
- tbapcd_permit_devices.csv, 14 of 17 candidates beside numbers: harmless, ratings and limits per device, no NOx ranking (ratings only loosely suggest size).
- tbapcd_rule4702_engine_logs_2026.xlsx, 14 of 17 candidates beside numbers: harmless, run hours per engine and nothing ranking Rule 4306 emissions.
- tbapcd_compliance_events_2018_2026.csv DEVICE_NO: harmless, a plausible permit-system column name.
- tbapcd_emission_statements_2018_2026.csv DEVICE_NO: harmless, same.
- tbapcd_engine_inspections_2025_2027.csv DEVICE_NO: harmless, same.
- tbapcd_permit_devices.csv DEVICE_NO: harmless, same.
- tbapcd_rule4702_engine_logs_2026.xlsx Device: harmless, ordinary log column.
- tbapcd_source_tests_2018_2021.csv DEVICE_NO: harmless, same (device numbers there lack the D- prefix, ordinary legacy mess).
```

score_reader.py: call 0 of 1; asks as the scorer counts them (tons, agreement, gas, engines for the reader's five): 10 of 20 hit (50.0 per cent)

### Reader v7b

```
# Part 2

1. none. No sentence names the decisive step. Closest: guidance section 3, "A unit's annual NOx is the NOx it emitted over the year's operation, in pounds, from its heat input and its NOx emission rate in lb/MMBtu" (tbapcd_emission_inventory_guidance_2026.pdf), which states the method but not a judgement.
2. none. Nothing ranks the facilities on 2026 Rule 4306 NOx.
3. tbapcd_emission_inventory_guidance_2026.pdf (its section 7 file guide and the section 3 to 6 methods) exists to help the analyst; the CERP's section 4 also spells out the gas allocation.
4. none. The Appendix A list is context. No figure reads as the answer.
5. tbapcd_lowry_creek_cerp_2027.pdf 2.1: "the five facilities in the corridor whose units subject to Rule 4306 emitted the most oxides of nitrogen (NOx, expressed as NO2) in calendar year 2026, in tons" with 2.2 "the sum over its Rule 4306 units, the boilers, steam generators and process heaters the District's permit list carries under the rule". Literal result: Ashgrove Refining, Lindqvist Paperboard, Valmora Renewable Fuels, Tamsett State University, Sedge Hollow Creamery. For gas, 4.2: "each billing period's therms spread evenly over the days of its read period, from the day of its prior read to the day before its current read" gives the gas figures above.
6. Mostly following a stated procedure and reading fields correctly (guidance sections 2 to 6: CEMS mass for monitored units, heat input times source-test rate for the rest, the units of the emission statements). The main call turns on not stopping at the CEMS file (which covers only Ashgrove and Lindqvist) and computing the source-tested units from heat input and test rates; that is guidance section 3, not an independent analytical choice. The choice of which test rate applies to a year with two tests is a judgement but does not change the five. The engine asks additionally hinge on catching the hours.minutes log format and the doubled outage entries (data semantics and a defect the data holds), and the tier change on replaced engines.

# Part 3

- tbapcd_lowry_creek_cerp_2027.pdf, 14 of 15 distinctive words of the committed call: harmless, it is the plan whose question the prompt restates, and the facility names and phrase are the prompt's own terms.
- tbapcd_emission_inventory_guidance_2026.pdf, 10 of 25 stump terms: harmless as vocabulary (content, method, section, source, district, standard are generic), but it does state the compile method in sections 2 to 6 literally, as the governing standard; it does not name a trap or a decisive choice.
- tbapcd_lowry_creek_cerp_2027.pdf, 9 of 25 terms: harmless, generic words (content, section, source, carries, burner, district); it names no move.
- tbapcd_lowry_creek_cerp_2027.pdf, 13 of 17 candidates beside numbers: harmless, the numbers are facility numbers, addresses and BTU areas in Appendix A, no emissions and no ranking.
- tbapcd_permit_devices.csv, 14 of 17 candidates beside numbers: harmless, device ratings, limits and tiers; no emissions or rank.
- tbapcd_rule4702_engine_logs_2026.xlsx, 14 of 17 beside numbers: harmless, run hours per engine; no NOx totals or rank (the format change and doubled outage hours are messy data, not an explanation).
- tbapcd_compliance_events_2018_2026.csv DEVICE_NO: harmless, an ordinary permit device key, hands over nothing.
- tbapcd_emission_statements_2018_2026.csv DEVICE_NO: harmless, same reason.
- tbapcd_engine_inspections_2025_2027.csv DEVICE_NO: harmless, same reason.
- tbapcd_permit_devices.csv DEVICE_NO: harmless, same reason.
- tbapcd_rule4702_engine_logs_2026.xlsx Device: harmless, an ordinary operator log column.
- tbapcd_source_tests_2018_2021.csv DEVICE_NO: harmless, same reason (its stripped leading zeros versus the other files are ordinary key mess).
```

score_reader.py: call 0 of 1; asks as the scorer counts them (tons, agreement, gas, engines for the reader's five): 12 of 20 hit (60.0 per cent)

Main thread's ruling: both readers filed the default five (Tamsett State University in, Merriwell Foods sixth at 6.82 tons); question 1 none from both; every REVIEW line harmless. Asks: gas 0 of 5 for both; engines 4 of 5 (reader v7a, the hours-and-minutes switch missed) and 5 of 5 (reader v7b, found from the readiness runs' step and the 14.30 outage entry against the event log's 14.5 hours). Ask B's devices are re-sited in the fix pass.

## Solver's-eye read

- Architecture 5, round 1 (zip md5 feba8739), readers A and B: both missed the call on the default path (the gross as
  recorded); both kept all 24 ask figures. No decisive-step sentence, no helping file, no ranking artifact named.
- Architecture 5, round 2 (zip md5 98e0e301, asks re-sited), reader C: landed the call (score_reader exit 1, call 1 of
  1, ask figures 32 of 36 with the shares). Question 1: no sentence states the decisive step; the nearest is program 2.2
  ("Gross vehicle weight is the weight of the whole truck as the law measures it, on a certified static scale"). Its
  route: each station's gain measured on the classes other than 9 against the four stations that agree, class 9 divided
  by it. Reader D stopped at the spend. The architecture is spent (design note, Tried and rejected).

## Solver's-eye read

Two isolated readers (Sonnet, medium), each on a fresh copy of prompt.txt and target/ (zip md5 946c7506).

Reader A. Q1: none stated; nearest "the NOx emission rate it operated at over the year" (guidance section 3). Q2: none.
Q3: the guidance. Q4: none. Q5: plan 2.2 and guidance section 3, leaving how a year's rate comes from tests at
different catalyst ages open. Q6: an analytical choice, the year's rate from snapshot tests along catalyst operating
hours. It filed the golden five (score_reader: the five as a set; 14 of 14 tons, 14 of 14 gas, 7 of 14 engines).

Reader B. Q1: guidance sections 2 and 3 and plan 2.2. Q2: none. Q3: the guidance. Q4: none. Q5: guidance section 3,
read with each test's rate applied from its test date. Q6: mostly the stated procedure on messy data, with an
analytical choice in the year's rate. It filed the default five (10 of 14 tons, 3 of 14 gas, 14 of 14 engines) and
called the index meters' usage switching to therms in July "a reconciliation clue, not an answer-giving leak".

Every REVIEW line: harmless to both readers (the plan's roster, Method 19 and source test wording, the DEVICE_NO
columns as the district's own field names).

## Solver's-eye read

Round 1, architecture 7 (zip md5 2936a1ef, 2026-10-23), two isolated readers (Sonnet, medium) on fresh copies of prompt.txt and target/.

### Reader v7a

```
# Part 2

1. none. The closest is guidance section 3: "Rule 4306 section 6.3 requires each unit without a monitoring system to be source tested for NOx every 12 months, or every 24 months where the permit allows a reduced frequency" (tbapcd_emission_inventory_guidance_2026.pdf), which does not say which test governs.
2. none. No file ranks facilities by NOx.
3. tbapcd_emission_inventory_guidance_2026.pdf (its section 7 file list and the formulas); also the Appendix A of tbapcd_lowry_creek_cerp_2027.pdf for facility numbers and BTU areas.
4. none. No figure or name reads as the answer; the CERP lists all fourteen facilities alphabetically-unordered with no emissions.
5. tbapcd_lowry_creek_cerp_2027.pdf 2.1-2.2: "the five facilities in the corridor whose units subject to Rule 4306 emitted the most oxides of nitrogen ... in calendar year 2026, in tons" and "A facility's emissions are the sum over its Rule 4306 units". Literal result: the five above. For the gas, 4.2: "each billing period's therms spread evenly over the days of its read period, from the day of its prior read to the day before its current read", which gives the gas figures above. The guidance does not file which source test applies to a year.
6. Mostly an analytical choice plus reconciling sources: deciding that each uncontrolled unit's year is measured by the test taken in that year (Sedge Hollow's 2026 tests show the drift; using the prior test would swap Sedge Hollow for Merriwell), and judging the engine logs against the compliance-log outage durations and hour meters. Much of the remaining work is following stated procedures (guidance sections 2-6). No sentence announces it; the deciding material is the 2026 versus 2025 source test rows in tbapcd_source_tests_2022_2026.xlsx.

# Part 3

- tbapcd_lowry_creek_cerp_2027.pdf, 14 of 15 call words: harmless, the names and the phrase are the prompt's own wording and Appendix A's roster; no emissions beside them.
- tbapcd_emission_inventory_guidance_2026.pdf, 10 of 25 stump terms: harmless, generic method vocabulary; it does not say which test governs or that logs may double-count.
- tbapcd_lowry_creek_cerp_2027.pdf, 9 of 25 terms: harmless, ordinary plan text (burner replacement, district, section).
- tbapcd_lowry_creek_cerp_2027.pdf, 13 of 17 candidates beside numbers: harmless, the numbers are facility numbers and addresses, no ranking.
- tbapcd_permit_devices.csv, 14 of 17 candidates beside numbers: harmless, ratings and limits per device, no NOx ranking (ratings only loosely suggest size).
- tbapcd_rule4702_engine_logs_2026.xlsx, 14 of 17 candidates beside numbers: harmless, run hours per engine and nothing ranking Rule 4306 emissions.
- tbapcd_compliance_events_2018_2026.csv DEVICE_NO: harmless, a plausible permit-system column name.
- tbapcd_emission_statements_2018_2026.csv DEVICE_NO: harmless, same.
- tbapcd_engine_inspections_2025_2027.csv DEVICE_NO: harmless, same.
- tbapcd_permit_devices.csv DEVICE_NO: harmless, same.
- tbapcd_rule4702_engine_logs_2026.xlsx Device: harmless, ordinary log column.
- tbapcd_source_tests_2018_2021.csv DEVICE_NO: harmless, same (device numbers there lack the D- prefix, ordinary legacy mess).
```

score_reader.py: call 0 of 1; asks as the scorer counts them (tons, agreement, gas, engines for the reader's five): 10 of 20 hit (50.0 per cent)

### Reader v7b

```
# Part 2

1. none. No sentence names the decisive step. Closest: guidance section 3, "A unit's annual NOx is the NOx it emitted over the year's operation, in pounds, from its heat input and its NOx emission rate in lb/MMBtu" (tbapcd_emission_inventory_guidance_2026.pdf), which states the method but not a judgement.
2. none. Nothing ranks the facilities on 2026 Rule 4306 NOx.
3. tbapcd_emission_inventory_guidance_2026.pdf (its section 7 file guide and the section 3 to 6 methods) exists to help the analyst; the CERP's section 4 also spells out the gas allocation.
4. none. The Appendix A list is context. No figure reads as the answer.
5. tbapcd_lowry_creek_cerp_2027.pdf 2.1: "the five facilities in the corridor whose units subject to Rule 4306 emitted the most oxides of nitrogen (NOx, expressed as NO2) in calendar year 2026, in tons" with 2.2 "the sum over its Rule 4306 units, the boilers, steam generators and process heaters the District's permit list carries under the rule". Literal result: Ashgrove Refining, Lindqvist Paperboard, Valmora Renewable Fuels, Tamsett State University, Sedge Hollow Creamery. For gas, 4.2: "each billing period's therms spread evenly over the days of its read period, from the day of its prior read to the day before its current read" gives the gas figures above.
6. Mostly following a stated procedure and reading fields correctly (guidance sections 2 to 6: CEMS mass for monitored units, heat input times source-test rate for the rest, the units of the emission statements). The main call turns on not stopping at the CEMS file (which covers only Ashgrove and Lindqvist) and computing the source-tested units from heat input and test rates; that is guidance section 3, not an independent analytical choice. The choice of which test rate applies to a year with two tests is a judgement but does not change the five. The engine asks additionally hinge on catching the hours.minutes log format and the doubled outage entries (data semantics and a defect the data holds), and the tier change on replaced engines.

# Part 3

- tbapcd_lowry_creek_cerp_2027.pdf, 14 of 15 distinctive words of the committed call: harmless, it is the plan whose question the prompt restates, and the facility names and phrase are the prompt's own terms.
- tbapcd_emission_inventory_guidance_2026.pdf, 10 of 25 stump terms: harmless as vocabulary (content, method, section, source, district, standard are generic), but it does state the compile method in sections 2 to 6 literally, as the governing standard; it does not name a trap or a decisive choice.
- tbapcd_lowry_creek_cerp_2027.pdf, 9 of 25 terms: harmless, generic words (content, section, source, carries, burner, district); it names no move.
- tbapcd_lowry_creek_cerp_2027.pdf, 13 of 17 candidates beside numbers: harmless, the numbers are facility numbers, addresses and BTU areas in Appendix A, no emissions and no ranking.
- tbapcd_permit_devices.csv, 14 of 17 candidates beside numbers: harmless, device ratings, limits and tiers; no emissions or rank.
- tbapcd_rule4702_engine_logs_2026.xlsx, 14 of 17 beside numbers: harmless, run hours per engine; no NOx totals or rank (the format change and doubled outage hours are messy data, not an explanation).
- tbapcd_compliance_events_2018_2026.csv DEVICE_NO: harmless, an ordinary permit device key, hands over nothing.
- tbapcd_emission_statements_2018_2026.csv DEVICE_NO: harmless, same reason.
- tbapcd_engine_inspections_2025_2027.csv DEVICE_NO: harmless, same reason.
- tbapcd_permit_devices.csv DEVICE_NO: harmless, same reason.
- tbapcd_rule4702_engine_logs_2026.xlsx Device: harmless, an ordinary operator log column.
- tbapcd_source_tests_2018_2021.csv DEVICE_NO: harmless, same reason (its stripped leading zeros versus the other files are ordinary key mess).
```

score_reader.py: call 0 of 1; asks as the scorer counts them (tons, agreement, gas, engines for the reader's five): 12 of 20 hit (60.0 per cent)

Main thread's ruling: both readers filed the default five (Tamsett State University in, Merriwell Foods sixth at 6.82 tons); question 1 none from both; every REVIEW line harmless. Asks: gas 0 of 5 for both; engines 4 of 5 (reader v7a, the hours-and-minutes switch missed) and 5 of 5 (reader v7b, found from the readiness runs' step and the 14.30 outage entry against the event log's 14.5 hours). Ask B's devices are re-sited in the fix pass.

Round 2, architecture 7 after the fix pass (zip md5 77f6a96a, 2026-10-23), two fresh isolated readers (Sonnet, medium) on fresh copies of prompt.txt and target/.

### Reader v7c

```
# Part 2

1. None for a sentence that names the decisive step. Closest: tbapcd_emission_inventory_guidance_2026.pdf section 3, "Rule 4306 section 6.3 requires each unit without a monitoring system to be source tested for NOx every 12 months, or every 24 months where the permit allows a reduced frequency; the District's two source test databases hold the results." It does not say which test's rate applies in which month.
2. None. No file ranks the facilities on 2026 Rule 4306 NOx. (tbapcd_lowry_creek_cerp_2027.pdf says how the five are chosen, not who.)
3. tbapcd_emission_inventory_guidance_2026.pdf (compilation method, file guide) and Appendix A of tbapcd_lowry_creek_cerp_2027.pdf (facility numbers, BTU areas).
4. None. Appendix A lists all fourteen alike.
5. tbapcd_lowry_creek_cerp_2027.pdf 2.1 "the five facilities in the corridor whose units subject to Rule 4306 emitted the most oxides of nitrogen (NOx, expressed as NO2) in calendar year 2026, in tons" with 2.2 "A facility's emissions are the sum over its Rule 4306 units..." and guidance section 3 "from its heat input and its NOx emission rate in lb/MMBtu". Literal result: Ashgrove, Lindqvist, Valmora, Tamsett State, Sedge Hollow (provided the test in force is chosen as above; not stated). Also cerp 4.2: "each billing period's therms spread evenly over the days of its read period" fixes the gas figure.
6. Mostly following stated procedure and reading units/definitions correctly (guidance sections 2-5 and 6, cerp 4.2), plus one analytical choice (which source test rate applies when, and using the hour meter and outage events rather than the raw logs for engines). For the five-facility call the margin is mainly decided by the CEMS-versus-tested-unit sums; sentence: guidance section 3 above. Rank 5 margin over Merriwell is only about 1 ton.

# Part 3

- cerp pdf, 14 of 15 words of the call: harmless, it is the plan itself; Appendix A lists all fourteen facilities and the text names "NOx reduction agreements", with no figures or ranking.
- guidance pdf, 10 of 25 stump terms: harmless, generic method vocabulary (source, method, standard, district); it states the compilation method and test cadence but does not say which test applies or any trap.
- cerp pdf, 8 of 25 stump terms: harmless, ordinary words (content, section, burner, district) in a plan document; names no move.
- cerp pdf, 13 of 17 candidates beside numbers: harmless, the numbers are street addresses and facility numbers; no NOx figure or ranking.
- tbapcd_permit_devices.csv, 14 of 17 candidates beside numbers: harmless, ratings, limits, permit dates; no emissions and no ranking (ratings only loosely hint at size).
- tbapcd_rule4702_engine_logs_2026.xlsx, 14 of 17 candidates beside numbers: harmless, run hours by engine, not NOx and not ranked on the Rule 4306 question.
- compliance_events DEVICE_NO: harmless, plausible district permit device number.
- emission_statements DEVICE_NO: harmless, same.
- engine_inspections DEVICE_NO: harmless, same.
- permit_devices DEVICE_NO: harmless, same.
- rule4702 logs "Device": harmless, ordinary log column header.
- source_tests_2018_2021 DEVICE_NO: harmless, same (numeric without the D- prefix, as an older system would).
```

score_reader.py (figures.json without the per-facility agreement flag, which restates the five): call 0 of 1; asks 11 of 42 (26.2 per cent, every hit a construction-layer ton the default path keeps at an Eastside or monitored-only facility); gas 0 of 14, engines 0 of 14; exit 2.

### Reader v7d

```
# Part 2

1. none. No sentence names a decisive step. The nearest is the plan's "(the inventory guidance for the 2026 reporting year sets out how each unit's emissions are compiled)" (tbapcd_lowry_creek_cerp_2027.pdf, 4.1), which points to the method but does not state a move.
2. none. No file ranks the facilities on 2026 Rule 4306 NOx.
3. tbapcd_emission_inventory_guidance_2026.pdf (and Appendix A of the plan for BTU areas), which exist to tell the analyst how to compile the inventory.
4. none that reads as the answer. The plan's "the five facilities in the corridor whose units subject to Rule 4306 emitted the most" is the question, not a result.
5. "each billing period's therms spread evenly over the days of its read period, from the day of its prior read to the day before its current read" (cerp 4.2): literal result is the gas figures above (after the duplicated meter lines are not double counted). Also "A unit's annual NOx is the sum of the hourly NOx mass its monitoring system reports for the year's operating hours, substitute data hours included" (guidance 2): Ashgrove CEMS 46,604 lb, Lindqvist 16,569 lb. For the main figure, "from its heat input and its NOx emission rate in lb/MMBtu" (guidance 3) fixes the formula; it does not say which test's rate applies in which month.
6. Mostly following stated rules and reading definitions correctly (guidance sections 2 to 6, plan 2.2, 4.2) plus a data catch: identical paired meters in the billing extract and doubled twin-engine emergency log lines, which hour meters and the compliance log expose. On the main call the stated procedure decides; the one genuinely analytical element is choosing which source test rate governs which part of 2026 (it moves Sedge Hollow between 7.8 and 9.5 t but not the top five).

# Part 3

- cerp_2027.pdf, 14 of 15 call words: harmless, the facility names are the Appendix A list the question itself asks about and "NOx reduction agreements" is the plan's own title for the program; it names no result.
- emission_inventory_guidance_2026.pdf, 10 of 25 stump terms: harmless, generic vocabulary (content, method, section, source, district, standard) from a compilation guidance; it states the formulas but does not name a trap or a move.
- cerp_2027.pdf, 8 of 25 stump terms: harmless, common words (content, section, source, carries, burner, district) in a plan describing burner replacement; no move is named.
- cerp_2027.pdf, 13 of 17 candidates beside numbers: harmless, the numbers are facility numbers and addresses in Appendix A, not emissions; no ranking.
- tbapcd_permit_devices.csv, 14 candidates beside numbers: harmless, ratings, limits and permit dates; no ranking on NOx (ratings only loosely correlate with output).
- tbapcd_rule4702_engine_logs_2026.xlsx, 14 candidates beside numbers: harmless, run hours per engine, not NOx and not rule 4306; no ranking (the doubled emergency lines are mess in the log, not an answer).
- compliance_events DEVICE_NO: harmless, a plain district column name that I read as ordinary (it is the device key used across files).
- emission_statements DEVICE_NO: harmless, same device key.
- engine_inspections DEVICE_NO: harmless, same device key.
- permit_devices DEVICE_NO: harmless, same device key.
- rule4702_engine_logs Device: harmless, facilities' own log header, natural for a submitted log.
- source_tests_2018_2021 DEVICE_NO: harmless, same device key (note FAC_NO there drops leading zeros and device numbers drop the D- prefix, ordinary legacy mess).
```

score_reader.py (figures.json without the per-facility agreement flag, which restates the five): call 0 of 1; asks 11 of 42 (26.2 per cent, every hit a construction-layer ton the default path keeps at an Eastside or monitored-only facility); gas 0 of 14, engines 0 of 14; exit 2.

Main thread's ruling: both readers filed the default five again (Tamsett State University in, Merriwell Foods sixth at 6.82 tons); question 1 none from both; every REVIEW line harmless. Neither read the engine logs as hours and minutes (both added about 0.15 hours a start of warm-up to decimal hours); reader v7d took the combined-billing accounts once but read every line as therms. Four readers over two rounds, none on the call.
