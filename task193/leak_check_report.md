# leak check, task193

**Verdict: REVIEW.** 20 files read, 120 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: asserted, expected, section, standard, decisive, sentence, package, nothing, inside, patient, re-sent, clearance, period, comparison, shipped, counterfactual, agency, release, reissued, manifest, detection, method, arithmetic, first-receipt, distribution

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `screen_standard_7_2024.pdf`: golden figure 1.25 appears: ...fter the first receipt of the product is at least 1.25 times the number that would be expected if receiv...
- **REVIEW** `screen_standard_7_2024.pdf`: carries 23 of 27 distinctive words of the committed call: 'Refer 7 of the 20 candidate pairs to formal signal assessment in the quarter beginning 1 January 2027: Dalvextin and loo'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `screen_standard_7_2024.pdf`: 7 of 25 stump-paragraph terms appear (expected, standard, package, inside, patient, clearance); read whether the document names the move

## 6 ranking artifacts (INFO 1)
- **INFO** `holder_register.csv`: names 7 of 7 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read (pass 3)

# Reader answers (bundle only)

## Headline
**Decisive step:** no sentence names it. The nearest is standard 1.1 ("where the marker treatment is started after the product more often than the register's own dispensing pattern would give") and 3.2(b) ("at least 1.25 times the number that would be expected if receiving the product had no bearing on when the marker treatment is first received"). Standard 3.5 then withholds the construction: "The construction of the expected number in 3.2(b) is the division's own epidemiological work and is recorded with each run." No file documents it. The move is a null-adjusted sequence symmetry analysis (Hallas style), where the expected "after" share comes from the timing distributions of the two first-receipts, not a flat 50%.

**Committed answer (confidence about 80% on the set, 70% that the grader's expected counts match mine):** 7 pairs are referred.
P01 Dalvextin x M4 loop diuretic, P02 Pirenoxol x M2 acid-suppressant, P03 Ternivast x M3 gout, P04 Oxelumab x M5 antidepressant, P06 Hestroban x M1 antiemetic, P07 Kirunelle x M6 hypnotic, P09 Sovraxil x M7 topical corticosteroid.

## Pair results (my filed construction)
Patients in a pair: first receipt of both treatments inside 1 Oct 2025 to 30 Sep 2026, same-day patients dropped, earliest receipt taken over the whole extract with person keys mapped through the crosswalk. Expected = N x P(marker after), where P is taken with the product and marker first-receipt dates treated as independent draws from their own observed distributions among the pair's patients, ties excluded.

| pair | N | after | before | expected | multiple | referred |
|---|---|---|---|---|---|---|
| P01 M4 | 375 | 277 | 98 | 188.1 | 1.47 | yes |
| P01 M2 | 195 | 99 | 96 | 96.1 | 1.03 | no |
| P01 M3 | 204 | 110 | 94 | 113.2 | 0.97 | no |
| P02 M2 | 363 | 273 | 90 | 188.7 | 1.45 | yes |
| P02 M6 | 172 | 91 | 81 | 92.9 | 0.98 | no |
| P02 M5 | 169 | 94 | 75 | 94.5 | 0.99 | no |
| P03 M3 | 546 | 268 | 278 | 197.2 | 1.36 | yes |
| P03 M6 | 324 | 63 | 261 | 67.9 | 0.93 | no |
| P03 M1 | 346 | 71 | 275 | 73.7 | 0.96 | no (tracker also under assessment) |
| P04 M5 | 694 | 383 | 311 | 281.7 | 1.36 | yes |
| P04 M7 | 502 | 143 | 359 | 141.1 | 1.01 | no (tracker also under assessment) |
| P04 M4 | 423 | 147 | 276 | 147.8 | 0.99 | no |
| P05 M6 | 269 | 208 | 61 | 210.1 | 0.99 | no |
| P05 M1 | 279 | 227 | 52 | 230.2 | 0.99 | no |
| P05 M2 | 301 | 229 | 72 | 235.5 | 0.97 | no |
| P06 M1 | 480 | 346 | 134 | 233.0 | 1.48 | yes |
| P06 M8 | 7 | 3 | 4 | | | no (under 25) |
| P07 M6 | 339 | 252 | 87 | 180.8 | 1.39 | yes |
| P07 M8 | 13 | 7 | 6 | | | no (under 25) |
| P08 M4 | 210 | 159 | 51 | 160.0 | 0.99 | no |
| P08 M5 | 268 | 215 | 53 | 211.7 | 1.02 | no (tracker: closed, so not a bar) |
| P09 M7 | 631 | 496 | 135 | 332.0 | 1.49 | yes |
| P09 M8 | 17 | 11 | 6 | | | no (under 25) |

Patient counts, after and before are forced by the documents (given the hygiene steps below). Expected and multiple are not filed (see Q5).

## Six questions

**1. Decisive-step sentence/file.** Nothing names it. 1.1 ("the register's own dispensing pattern") and 3.2(b) ("would be expected if receiving the product had no bearing on when the marker treatment is first received") point at a null model; 3.5 says the construction is the division's own work. No worked example. The selection of files is not a hint here: the documentation covers key replacement, duplicate transmission, package re-use, DD-MM-YYYY layout, so it teaches Layer 1 hygiene only. The only structural hint is the data itself (P03/P04 launch ramps, P05/P08 wind-downs, visible by month in the dispensings).

**2. File that already ranks/scores the candidates.** None. signal_tracker_export.csv lists pairs under assessment, but only P03 M1 and P04 M7 are "under assessment" and neither would be referred under any null I tried, so it is a non-event. spontaneous_reports_summary.csv has reports by product and quarter (P03 and P04 rising: 27 and 38 in 2026 Q3), but it is by product, not pair, and unused.

**3. File that exists only to help.** None obviously. Candidates for "helper": register_variable_documentation.csv and register_release_notes.json (they exist to explain the layout change, retransmission ids, package re-use, key replacement; a real register would carry a lot more variables than the ones this task needs, and every row here documents exactly a mess the data contains). That selectivity is a tell, but it hints at hygiene, not the decisive step. screen_annexes.csv duplicates Annex A/B of the PDF in machine form (a convenience). Unused/distractors: literature_screening_log.csv, spontaneous_reports_summary.csv, atc_text.csv (marker texts only), signal_tracker_export.csv (moot), atc entries for non-screened drugs.

**4. Figure/name reading as the answer.** The tracker rows P03-M1 and P04-M7 (the two fastest-rising launches), plus spontaneous reports for Ternivast and Oxelumab, read as "the" signal; they are context. The crude share (P05 about 80% after) reads as the answer but is a trend artefact.

**5. Filed sentence that fixes the computation.** Population: 2.5 ("patients whose first receipt of the product and whose first receipt of the marker treatment both fall inside the screen window... same day is not one of the pair's patients"). Window/unit: 2.1, 2.3, 2.4. Ordering: 3.1. Threshold: 3.2(a)-(c). What the measure is taken against: **nothing is filed**. 3.5 withholds it. Under each comparator I consider defensible:
- Flat 50% (symmetry, expected = N/2), which is the literal "no bearing" reading with stationary rates: multiples P01M4 1.48, P02M2 1.50, P05M6 1.55, P05M1 1.63, P05M2 1.52, P06M1 1.44, P07M6 1.49, P08M4 1.51, P08M5 1.60, P09M7 1.57; P04M5 1.10, P03M3 0.98. Referred set (10): P01M4, P02M2, P05 x3, P06M1, P07M6, P08M4, P08M5, P09M7.
- Null-adjusted on the pair's own timing marginals (table above): 7 referred.
- Null-adjusted on all window initiators of each treatment: same 7 (multiples P03M3 2.10, P04M5 1.70, P01M4 1.48, P02M2 1.44, P06M1 1.58, P07M6 1.52, P09M7 1.48); everything else under 1.25 (largest non-referred 1.12).
- Null-adjusted on calendar-month buckets: same 7 (1.39 to 1.49).
So the set is invariant across null-adjusted forms but flips on 5 pairs against the flat 50%. Literal execution is not possible. A strict "expected = half" reader would file 10 pairs including all of P05 and P08.

**6. What decides it.** An analytical choice: whether the expected number allows for the rising/falling timing of first receipts (launch ramps for P03/P04, wind-down for P05/P08). It is not a field/code reading, not a stated rule (the rule is deliberately withheld), not a planted item. The sentence that carries it, weakly, is 1.1 "the register's own dispensing pattern would give".

## Other asks

**Hygiene battery.** Union of the two layouts (rename + DD-MM-YYYY), drop retransmissions (2,103 duplicate rows, all APK, all dispensed Oct 2025, new record ids, same everything else), crosswalk 420 retired keys to current, package to ATC at the date (the Sovraxil codes re-issue on 2026-02-27, same ATC either way, nothing outside validity in the extract), age 18+ (all are), deaths/emigrations (no dispensing after death). Effect on selection: none. Not deduping or not applying the crosswalk changes counts only (e.g. P01 M4 377 vs 375, P09 M7 635 vs 631, P03 M3 547 vs 546; no-dedupe leaves pair counts unchanged because duplicates are in the same person-date). Folding in the 2,420 rejected lines as first receipts also leaves the 7. So cleaning changes counts, not the referred set. Pair counts for the sheet (patients, after, before) do depend on dedupe/crosswalk by 1 to 4 patients in some pairs, which the documents force.

**Chain x quarter table (dispensing quarter, window).** Rejected = rows in submission_exceptions.csv by date_of_dispensing quarter and pharmacy chain (811 in window). Accepted = deduplicated lines (retransmissions counted once, as the variable documentation says), median = submission_date minus date_of_dispensing. Forced: yes, given the documentation (the submission log is by submission month and is a decoy for this). Values (accepted / median days / rejected):
APK 2025Q4 5985/1.0/66; 2026Q1 5476/2.0/67; Q2 5554/2.0/42; Q3 5732/2.0/58.
DSA 4673/3.0/66; 4119/3.0/71; 4082/4.0/39; 4344/4.0/62.
NOR 3386/4.0/73; 3064/5.0/64; 2875/6.0/82; 3203/6.0/35.
VST 2260/6.0/28; 2002/7.0/18; 1933/6.0/22; 1997/8.0/18.
Not forced only if retransmissions are counted: APK 2025Q4 accepted would be 8,088 (5,985 + 2,103 duplicate rows); medians are unchanged. The documentation settles it (count once).

**Holder DDD and fee.** Payer by product on the date (P09 H5 to H6 from 2026-02-27; P07 H7 to H2 from 2026-04-01; lapsed P05/P08 still charged), band settled on the whole-window total, old rates before 1 Apr 2026 and amended after. Doses (DDD) pre/post and fee: H1 255,520.5 DDD, band 2, DKK 329,175; H2 231,565.7, band 1, 361,748; H3 407,656.0, band 2, 542,791; H4 159,767.0, band 1, 237,117; H5 80,973.6, band 1, 121,540; H6 316,685.3, band 2, 401,744; H7 113,515.5, band 1, 168,003 (total 2,162,118). Forced, but fragile to hygiene: H1 sits at 255.5k thousand-DDD against a 250 break, so omitting the dedupe (adds retransmitted APK Oct 2025 doses to P01/P04? it raises totals by about 54k DDD overall) or mis-assigning Oxelumab could move bands; H2 (231.6k) also sits near 250 if the merger is read differently (H7 pre-merger stays with H7, which I did). ddd_per_pack is used as printed (rounded to 2 dp). Blank DDD for topicals does not touch Annex A products.

**Region x age band.** Patients with a first Annex A product receipt in window: 9,895, of whom 7,492 (75.7%) have a first receipt of at least one Annex B marker in window. Region taken at the start of the window = previous_region where region_recorded_from falls after 1 Oct 2025 (all 345 changes do), else region; blank = "Not stated"; age = 2025 minus year of birth in the four bands. Cell shares (n, share%): Hovedstaden 18-39 868/68.5, 40-59 788/77.5, 60-74 552/81.9, 75+ 709/79.5; Midtjylland 667/68.1, 626/76.7, 457/79.6, 529/77.3; Nordjylland 303/67.0, 285/75.1, 204/80.9, 222/80.6; Sjaelland 391/73.4, 422/73.9, 303/80.2, 338/81.1; Syddanmark 621/69.9, 550/75.6, 403/79.2, 420/80.2; Not stated 74/74.3, 64/75.0, 53/75.5, 46/80.4. Forced by 4.2. The one open choice: "at least one marker treatment in Annex B" read as any of the eight markers (what I filed) vs only the patient's own product's screened markers, which would give lower shares. Using current region instead moves 146 cells' worth of patients.

## Does the pack read as recorded or generated?
Mixed; the structure is plausible but several things read generated:
- Reconciliation too exact. pharmacy_submission_log.csv matches the extract's raw row count (including retransmitted duplicates) and the exceptions file to the unit in all 148 chain-month cells, and submitted = accepted + turned back in every cell. Real chain totals do not tie to a row-level export in every cell.
- All 2,103 retransmissions are APK, all Oct 2025 dispensings, confined to one burst (APK 2025-10 has 4,054 submitted vs about 2,000 a month), record ids 16,227 to 179,399. A single clean planted event rather than scattered failed transfers.
- Submission dates are weekday-flat: Sunday submissions (24,683) equal the weekday level while Sunday dispensings are 1% of lines (1,782), Saturday 18,781. Lag is drawn independently of weekday, capped at 20 days, unimodal per chain with chain-level means exactly ordered APK 2.0, DSA 3.6, NOR 5.5, VST 6.9 and a median that rises monotonically with quarter in most chains.
- Rates flat across strata that should differ: marker share by region within age band varies little, while the age gradient is smooth (68 to 81). Rejection reasons are spread uniformly across dates and chains (e.g. "package code not valid on the date of dispensing" for 568 lines, of which 547 involve codes with no validity dates in package_index.csv, so the reason cannot be reproduced from the files; "pharmacy identifier closed" has no closing date anywhere in pharmacy_register.csv).
- Launch curves are too smooth: P03/P04 ramp monthly 18, 84, 158, 256, 370, 493, 554, 703; P05/P08 decay symmetrically; P05 and P08 stop on exactly the authorisation end dates (2026-04-18, 2026-07-07) with first dispensings the day after first_marketed.
- Person data: 16,991 persons, all with at least 1 dispensing, mean 10.3 lines each, none with zero; every person in the register is in the extract (the extract scope makes this partly natural). Person keys run PK3100003 to PK3319xxx with replacement keys PK84xxxxx (a clean separate range, 420 pairs on 4 replacement dates per file). The person register holds only current keys, contradicting its own documentation ("appears once under each"). region_recorded_from falls only between 2025-10-21 and 2026-09-05, none earlier, though the documentation says it covers the extract period. Region blank 433 (2.5%), no previous_region without a date.
- Names: pharmacies "Koebenhavn Oesterbro Apotek", "Svanen Apotek", brands invented but plausible; prescriber ids uniformly L10000 to L19999 style (7,400 ids, 24 lines each on average, narrow 4 to 57). Holder names are obviously invented ("Soegaard Medica", "Ellevang Biosciences").
- Dispensing volume per patient is high and homogeneous: a patient's lines are mostly of Annex A/B drugs only, so 76% of new users of a monitored product also start a marker in the same year, which no real register would show.
- Literature log: titles are template strings ("A signal evaluation of X and sleep disturbance", "Hospital admissions in the first year of X"), 96 rows, the four rows with read_against filled are exactly the tracker rows.
- A seemingly planted contradiction: P05 and P08 marker shares of 76 to 81% look like the clearest signals unless the null is trend-adjusted.

## Unused / helper files
Unused for the solution: literature_screening_log.csv, spontaneous_reports_summary.csv, atc_text.csv, signal_tracker_export.csv (moot, as the tracker rows are not referred anyway), pharmacy_submission_log.csv (trap: counts by submission month, not dispensing quarter), the age/death fields (deaths and emigrations touch nothing), holder_register.csv only matters via H7 to H2. Helper-like: register_variable_documentation.csv, register_release_notes.json, screen_annexes.csv. A real documentation file would list the full register variable set, codelists, and caveats unrelated to this task; this one lists only the variables the mess touches. Nothing in the package supplies the expected-number construction, which a real run would record "with each run".
