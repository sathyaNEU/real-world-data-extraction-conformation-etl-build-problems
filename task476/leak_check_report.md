# leak check, task476

**Verdict: REVIEW.** 45 files read, 62 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: emissions-inventory, interval, payment-claims, method, architecture, application, vapour, golden, driver, efficiency, volume, silent, family, sentence, previous, decisive, conversion, register, acre-foot, reflex, readable, session, production, census-register, window

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `power/vrp_usage_export_2025-09-01_2026-03-31.csv`: golden figure 59,205 appears: ...Wh, 4452923461,Electric usage,2026-02-22,11:00,11:59,205.20,kWh, 4452923461,Electric usage,2026-02-22,12:0...
- **REVIEW** `pump_tests/GPT-23-0611.pdf`: golden figure 339 appears: ...Value Measurement Value Standing water level (ft) 339.9 Flow rate (gpm) 1488 Pumping water level (ft) 3...
- **REVIEW** `agency/sallow_plains_gsa_wy2026_allocation_notice.pdf`: carries 11 of 11 distinctive words of the committed call: 'Ochre Flats should buy 250 acre-feet of transfer water and have it recorded with the Sallow Plains GSA before the Decemb'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `agency/sallow_plains_gsa_wy2026_allocation_notice.pdf`: 5 of 25 stump-paragraph terms appear (interval, method, volume, acre-foot, window); read whether the document names the move

## 5 announcements (REVIEW 1)
- **REVIEW** `pump_tests/BHS-1874.pdf`: Note: original bowls, 1998 installation; rebuild recommended.

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `agency/sallow_plains_gsa_wy2026_allocation_notice.pdf`: names 5 column(s) of the data files verbatim (Agency well ID, Aquifer, Upper, method, month): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 2 author vocabulary (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Read on the previous cut (target.zip 7e8bf4aa). Since then the FIX_NOW pass changed two pack files only: the agency notice (its allocation total row now sums its rows and prints the two column totals, and section 5's sentence adds "counted from the end of the last interval in which the utility's data for the well's service record energy") and the technician's download log (each well-logger visit's note records the clock, "clock set from field laptop, PST (UTC-08:00), no daylight saving"); the reader is to be run again on the new cut.

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), architecture 3, on a fresh copy of prompt.txt and target/ (target.zip sha256 7e8bf4aa718d934980021ecab4934c68a1dbc0df434918f3de4b1ec402f5ae7c). Sweep 4's line and the answer-figure numbers were kept out of the brief and ruled in the main thread.

# Leak read, task476 (read and quote only; nothing solved)

1. Decisive step: none announces it. Closest context: agency notice s4 "Extraction above the water available must be covered by a transfer ... in whole blocks of 50 acre-feet, the smallest transfer the Agency records." and s2 "The water available to you for water year 2026 is the allocation plus the carryover." These are the agency's standing rules, not a pointer to a step.
2. No file ranks or scores candidates on the question. The agency notice lists allocation per APN (total 14879.0 AF) and carryover 480 AF, but no extraction total or shortfall.
3. Files existing only to help the analyst: the blank agency/wy2026_extraction_return_template.csv (the requested form, legitimate). Nothing else. ranch/ochre_flats_well_register.xlsx is a crosswalk but reads as the ranch's own register.
4. Figures reading as the answer: none. The 480 AF carryover and USD 1,185 / 1,500 per AF are stated context; no extraction, shortfall or purchase figure appears.
5. Filed sentences fixing computation/population:
 - Notice s3: "Water year 2026 runs from October 1, 2025 through September 30, 2026, local time." and "A well with a flow meter reports the difference between its meter readings taken nearest the start and the end of each month and of the water year, allowing for any meter exchange. A well without a meter reports the volume it pumped, calculated from the well's own records." Fixes: window Oct 1 2025 to Sep 30 2026 local; metered wells by meter-read differences; unmetered wells by calculated volume, whole AF per well, agency sums the wells' reported WY volumes (so rounding is per well).
 - Notice s5: "the depth to water below ground surface at the well at the first reading in the window at which the well's pump has been off for at least the preceding 24 hours" with windows Feb 1 to Mar 31 2026 and Oct 1 to Oct 31 2026, local. Fixes the static-DTW definition.
 - Notice s4: transfers in whole blocks of 50 AF.
 - Prompt: "ranch's water-year total against the water it had available", charges "under its time-of-use schedule".
 Note: s3 does not state how the unmetered volume is calculated (method open); the pack supplies power, pump tests and level data for that.
6. What decides the main answer: mostly data conformation and following the stated agency procedure (meter differences, unit conversions, meter exchange, power to acre-feet through kWh/AF for unmetered wells, 50 AF block rounding), with an analytical component in estimating unmetered pumping from energy and test efficiency (using the right test per pump and the pumping lift). Deciding text: notice s3 "A well without a meter reports the volume it pumped, calculated from the well's own records". Nothing is announced as planted.

a. power/vrp_usage_export_2025-09-01_2026-03-31.csv: harmless, because it is an hourly utility export (header Name/Address/Account Number, columns SERVICE AGREEMENT, TYPE, DATE, START TIME, END TIME, USAGE, UNITS, NOTES); NOTES empty in sampled rows; no value reads as an answer. pump_tests/GPT-23-0611.pdf: harmless, because it is an ordinary test sheet (SWL 339.9, kWh/AF 871, 6.58 AF/24h) with printed formulas of the standard test form.
b. agency notice vocabulary (transfer, true-up, allocation, carryover, available): harmless, because it is the agency's standing WY2026 notice stating allocation/carryover/rules with no extraction total, shortfall or purchase.
c. agency notice naming column names: harmless, because the names (state well no., APN, aquifer, method METER/CALCULATED, monthly AF, static DTW) are the agency's own return format, reproduced in the blank template; it is addressed to Melinda Walter, issued October 15, 2026, signed to Tamara Larson, and reads as the agency's notice, not an analyst note.
d. BHS-1874 note "original bowls, 1998 installation; rebuild recommended.": harmless-to-borderline. It is an ordinary tester's remark, and the same line appears on Gutierrez GPT-23-0611 and GPT-23-0629 (2023 tests of Deep 2, Deep 7, Deep 5), so it is a consistent house remark. Mild observation: those 2023 tests pre-date the register's pump install dates for those wells (Deep 2 2024-02-21, Deep 5 2024-03-06, Deep 7 2024-02-28), and the "original bowls" remark is consistent with a superseded pump. That is derivable from the register and test dates; the note does not say which test to use. Not a leak.
e. pump_tests: read as real test reports (two contractor templates, BHS and Gutierrez; printed definitions TDH/OPE/kWh-per-AF are standard formulas on real test sheets; fields like Utility SA differ slightly from the register's SA to Mar 31 (e.g., BHS-1874 4410847946 vs register 4410847963), consistent with an imperfect key). No steering line.
f. levels/logger_download_log.csv and logger files: ordinary technician log (J. Cox visits, pump running/off at sounding, "logger moved to Pump 5; 2081044 installed from Pump 5 ... relaunched at new site, location field not changed", "barologger clock synced to office PC (UTC)"). The swap note is the kind of record a technician leaves; it is a fact about the data rather than a hint at a method, though it does openly state the location-field mismatch. Logger headers state time zone "daylight saving not applied" and reference "set 2025-03-12 from manual sounding", normal instrument metadata. Nothing placed to be caught beyond ordinary records.
g. ranch/ochre_flats_well_register.xlsx: reads as the ranch's own register (well, ranch name, state well no., agency ID, APN, pump installed, motor hp, bowl setting, SAs before/after Apr 1 2026, rate schedule, meter model, logger S/N, sensor depth, MP height). Notes are brief ("Totalizer on old meter read in gal x 100", "Booster on separate service, not this SA", "Sounding tube 1.25 in."). Mildly dense with exactly the conversion facts (units, MP height, SA change dates), but plausible for a water manager's register; no column points at a single step. The "Rate schedule" column lists the schedule after the change; the utility letter dates it June 1, 2026.

Realism: none strongly; mild tells: power/vrp_usage_export hourly values for a pump are near-constant with tiny noise (e.g., 75.84, 75.37, 76.13 kWh every hour), and the register, notice and tests all carry unusually clean, complete data. Not disqualifying.
