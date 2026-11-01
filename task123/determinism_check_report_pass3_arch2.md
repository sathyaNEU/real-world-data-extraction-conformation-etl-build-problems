# Determinism check, task123 (pass 3, the one re-judge after the /fix-determinism rebuild)

Isolated judge thread on a fresh unzip of target.zip (22 files, in /tmp/determinism-check-task123-1791847391/target/) and the graded blocks of submission.md; run 2026-10-12. The thread's verdict follows unchanged. The report was written from the verdict at the coordinator's request; the design note and metadata.json were not read for a Gate G reconciliation.

## Summary lines
- **Verdict:** DETERMINISTIC, SOLUTION_WRONG (minor, SOLUTION_STEPS step 2, Northbank move-out figures only)
- **Disposition:** FIX_NOW (edit step 2's Northbank figures to 545 reads, 0.27 against 3.57 points, shape closer at 517; no bundle, prompt or graded-figure change)
- **Gate G line:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no. The judge found no shipped artifact that ranks counties wrongly; the named decoys (KVG GS extract, HHAP premise snapshot, SERVICE_COUNTY field, stale IBPP rows, NNG ACT_DATE) are unused by the solution. Not reconciled against the design note or card by this pass.
- **Gate H line:** domain: pass, layers: pass, decisive_step: analytical
- Spec-gate counts from the judge's hygiene read: 22 files, 8 formats, a 1.06M-row parquet and a 139,768-row CSV (all pass). Distractor naming in metadata.json, deliverable count and the 25-criterion rubric were not independently checked by this pass.

# Determinism verdict, task 123 (NHAG 2026-27 county split)

- **Verdict:** DETERMINISTIC, SOLUTION_WRONG (minor, SOLUTION_STEPS step 2 only).
- **Disposition:** FIX_NOW. Restate the Northbank move-out check in step 2 (see Evidence). The bundle, prompt and every graded figure stay unchanged, and no model rerun is needed.

## Why
Every committed answer reproduces from the shipped files: the 12 awards, the 36 January indicator counts and the 12 therm values. They come out of a literal reading of Standard Ed. 3 (2.3 gas-day month, 2.4 service period, 2.5 therms as billed, 2.6 premise county, 3.3 unrounded allocation, 4.2 premise county, Appendix B). The one open method is how a bill spanning the month boundary is apportioned to gas days. Standard 2.3 requires "gas used on those gas days, whatever the dates of reads", and the only daily evidence in the package is the Pine Harbor AMI shape (cold snap 19 to 31 Jan, 2.4 times 1 to 18 Jan). That shape is validated on the move-out reads, so the even-by-days split is not defensible (the 2.3 definition and the data both reject it). Fork table: shape split gives Ashwell $1,710,000 and total 10,260,673 therms; even split gives Ashwell $1,755,000 and total 11,194,395 therms, so the awards differ.

## Evidence (recomputed from target/)
- January residential therms, shape proration, rounded to 10,000. All 12 match SUPPLEMENTARY_ANSWERS; region total 10,260,673 (golden 10,260,000).
  - Ashwell 940,754; Brennock 1,310,218; Farrish 928,121; Halvern 1,012,378; Keswin 619,138; Merrion 721,425.
  - Ottercreek 677,510; Pellow 1,048,469; Rennick 1,181,065; Sauvain 500,587; Tillery 839,753; Wynnell 481,255.
  - Tillery = Pine Harbor 762,512 + Kestrel Valley 77,240.
  - KVG: net of CNCL/RBIL by BILL_NO (666 of each), 21,325 premises, each January gas day in exactly one bill. January contains no E reads.
  - NNG: 37,199 detail records, CCF x HV-FACTOR = THERMS in every row, register rollover consistent, 13,373 premises with full January coverage.
  - PHE: CYCLE bills prorated by shape; CALENDAR bills wholly in the month and equal to MDMS x 1.034 within rounding.
  - GS and master-metered MFR (KVG GS extract) are not residential and are correctly excluded. All premises map to a county.
- Awards, unrounded county values times 18,640,000 over the total, rounded to $5,000. All 12 reproduce and sum to $18,640,000 (Brennock 2,380,201 to 2,380,000 ... Wynnell 874,270 to 875,000).
  - Margins to the $5,000 rounding boundary are about 1.4k to 2k dollars (about 0.1%) for Ashwell, Farrish, Tillery, Ottercreek, Sauvain and Wynnell. It is thin but clean.
  - Shape variants (exclude E reads, median, sum, non-zero mean) flip no award. Rounding the county values first would move 5 awards by $5,000, but 3.3 files the unrounded rule.
- Disconnections, all 12 reproduce.
  - KVG: completed NP OFF orders in January by COMPLETED_TS (41) union the Northline jobs by account and day (51; 38 overlap, so 54 in total). CERR and UNAB are excluded. Ashwell 13, Brennock 13, Rennick 12, Sauvain 8, Ottercreek 8.
  - NNG: DNP with RESULT C, by crew COMPLETED_AT in January (36). Halvern 14, Farrish 9, Wynnell 8, Keswin 5. ACT_DATE would give a different answer, but the standard says "completed in the month".
  - PHE: completed Collections Shutoff work orders (16 by Eastern completion date in January, 19 in all) plus NP VALVE_CLOSE events from HES (17 on their Eastern date, with no overlap). Pellow 13, Tillery 12, Merrion 11. VALVE_CLOSE_FAILED is excluded.
- Low-income plan accounts, all 12 reproduce.
  - KVG WCP at the account's billing-extract premise county (1,259 in force, versus enrollment SERVICE_COUNTY, which differs for roughly 150): Brennock 384, Rennick 282, Ashwell 217, Ottercreek 211, Sauvain 141, Tillery 24.
  - NNG HHAP from account history, 798 in force. The premise file's 821 includes 23 flags whose program ended before 31 January; both files are shipped, so the end dates rule them out.
  - PHE IBPP on accounts linked to a meter on 31 January, 787. 307 IBPP rows remain ACTIVE on accounts whose meter link ended in October and whose last bill was in October. Their premises hold new accounts, 292 of them with their own IBPP, so counting them double counts. Tillery = 228 + 24 = 252; Pellow 344; Merrion 215.
- Solution-block defect (SOLUTION_WRONG, minor). Step 2 says Northbank has 536 move-out reads, 0.3 against 3.3 points, shape closer at 517. Recomputed with the same definition: 545 reads (555 before the zero-therm drop), 0.27 against 3.57 points, shape closer at 517. The Kestrel figures (567, 0.3, 5.3, 530) reproduce exactly. The conclusion is unchanged. Fix the numbers.

## Files/Hygiene
PASS. 22 files in 8 formats (pdf, csv, txt fixed-width, xlsx, parquet, json, docx, eml); a 1.06M-row parquet, a 139,768-row CSV and a 37,199-record fixed-width file. Distractors present: KVG GS extract, HHAP premise snapshot, the 'SERVICE_COUNTY' field, the stale IBPP rows, the NNG ACT_DATE. The files read as system exports with a manifest. No authoring or benchmark language found, and dates are coherent with the April 2026 setting. One note: the data-notes docx explains column meanings in prose, which is acceptable. No exclusion-level finding.

## Stump power
The easy route, a bill-to-month split by days of service (the usual calendarization), is the stump. It gives 11.19M therms and a different split. Ashwell $1,755,000 against $1,710,000, and Keswin and Ottercreek swap ranks (9 and 10), with all 12 awards moving by $5,000 or more. A strong analyst who cleaned the data and read the standard right can still file this. It is plausible that a strong model falls for it, and the validation (move-out reads) is what separates the methods. Risk: the shape evidence comes only from the Pine Harbor AMI meters, and solvers who judge an even split "good enough" are the intended failures. The other layers (net cancels, dials, UTC) are cleared by competent runs.

## Stumping type
`mechanism: method_or_model_selection` (calendarization of bills with a validated daily load shape); `stumping_family: analytical_non_defect`; `surface_read_dependency: no`; `sole_data_defect: no`. No reported number is wrong; the difficulty is choosing and validating the proration method on honest data. Not banned.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1 is three utilities' conventions (cancel/rebill, fixed-width bimonthly reads, cycle versus calendar AMI bills, UTC events); Layer 2 is calendarization of non-calendar bills with a daily load shape validated at move-outs. Swap test: a utility-demand calendarization does not read the same with other nouns. Easy route: pro rata by days, giving the awards above.

## Fix
solution: edit step 2's Northbank figures only (545 reads, 0.27 against 3.57 points, shape closer at 517). Optional hardening is not needed; no input files or prompt change. Optional prompt reading note: none required.
