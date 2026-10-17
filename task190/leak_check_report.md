# leak check, task190

**Verdict: REVIEW.** 21 files read, 46 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: deposit, clause, nothing, asserted, excess, reporting, background, states, window, screen, customer, extract, sentence, profile, decisive, register, same-day, counter, ordinary, carries, closed, counted, shipped, construction, objective

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `aml_programme_handbook.pdf`: carries 10 of 12 distinctive words of the committed call: 'The annual report should state that 400 cash deposits were split below the prescribed transaction threshold in the year '
- **REVIEW** `annual_report_extract_2026.pdf`: carries 8 of 12 distinctive words of the committed call: 'The annual report should state that 400 cash deposits were split below the prescribed transaction threshold in the year '
- **REVIEW** `provenance.md`: carries 8 of 12 distinctive words of the committed call: 'The annual report should state that 400 cash deposits were split below the prescribed transaction threshold in the year '

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `aml_programme_handbook.pdf`: 9 of 25 stump-paragraph terms appear (deposit, reporting, states, customer, extract, register); read whether the document names the move
- **REVIEW** `annual_report_extract_2026.pdf`: 5 of 25 stump-paragraph terms appear (deposit, reporting, customer, extract, counter); read whether the document names the move
- **REVIEW** `provenance.md`: 9 of 25 stump-paragraph terms appear (deposit, nothing, reporting, customer, extract, register); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "How many cash deposits did Arahura Bank's business customers split below the prescribed transaction threshold in the year to 30 June 2027?"

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

# Reader answers, task190 (Arahura Bank structuring)

## 1. Decisive step
The only sentence that tells you how the headline is built is handbook para 7.4: "the number of physical cash deposits of nine thousand dollars or more and below ten thousand dollars that the segment's customers paid in during the reporting year and that were paid in below the prescribed transaction threshold when the amount would otherwise have been at or above it. The count is of deposits, one for one, and not of customers or of days; a deposit is counted in the reporting year in which it was paid in; every customer on the business register at the end of the reporting year is within its segment's count."
Read literally it is a band count. The phrase "when the amount would otherwise have been at or above it", the prompt's word "split", and the instruction "Split deposits to the nearest 10 per segment" point instead to an estimated excess (bunching). The pack does not say which one. The handbook also says (7.5) that the segment recodes do not change segments, and 3.1/7.6 define cash as counter plus smart machine.

## 2. File that ranks or scores candidates
None ranks segments on the structuring question. branch_cash_summary_2027.csv and the FY26 annual report ($539.4m business cash, which my FY26 total reproduces to 539.43m) only reconcile totals. The prescribed-transaction extracts hold only amounts at or above 10,000 and so show nothing about structuring.

## 3. Files that exist only to help
field_dictionary.csv, export_manifest.csv (its "omits" column tells you what is missing, for example AR11 after closure), provenance.md (lists the traps: 90 re-sent machine rows, 333 late-posted counter rows, AR11/AR12, recoding, UTC), rating_scale_map.csv (needed to bridge 1-5 and A-E), customer_number_crosswalk.csv.
Pure distractors as far as the main call goes: card_settlement_summary_2027.csv, branch_cash_summary_2027.csv, both prescribed_transaction extracts, annual_report_extract_2026.pdf (apart from a sanity total).

## 4. Figure that reads as the answer
Nothing states a segment figure. The giveaway is in the data: a visible spike in the 9,500 to 9,999 amounts and round values (9,800 / 9,900 / 9,950) piling up there. Also the prompt's "to the nearest 10" for a count tells you the intended figure is an estimate, not an exact tally of a band.

## 5. Sentence fixing the figure, and its literal result
Para 7.4 above. Literal execution (cash only, counter + machine, machine rows with pull_sequence 2 dropped, machine UTC converted to NZ local before assigning the year, the one reversed pair removed, deposit_date not posted_date, segment from crosswalk then register), amount 9,000.00 to 9,999.99, 1 Jul 2026 to 30 Jun 2027:

| Segment | band count | rounded to 10 |
|---|---|---|
| Clubs and community | 103 | 100 |
| Fuel and automotive | 298 | 300 |
| Grocery and convenience | 626 | 630 |
| Hospitality | 512 | 510 |
| Personal services | 111 | 110 |
| Rural supply and horticulture | 151 | 150 |
| Trades and construction | 216 | 220 |
| Transport and courier | 179 | 180 |
| Total | 2,196 | 2,200 |

Largest segment on this reading: Grocery and convenience. The result is insensitive to the UTC/local choice (969 machine deposits in band either way), to the DST handling, and to the recoding.

## 6. What decides the main answer
Mixed. A solver who follows 7.4 as written gets 2,196/2,200 by executing a rule (rule application and semantics: the dedupe, UTC, crosswalk, instrument filter). A solver who takes "split ... would otherwise have been at or above" seriously needs an analytical choice: estimate how many of those 2,196 deposits are excess over a counterfactual density. The text that decides is 7.4's "when the amount would otherwise have been at or above it" against its own first clause "of nine thousand dollars or more and below ten thousand". I could not tell from the documents which is meant. Nothing looks like a planted decoy. The ranking of segments differs sharply: the literal count makes Grocery the largest by far, the excess makes Transport (about 90) the largest. That fork is the real stump and is not closed in the pack.

## 7. Doing the work

Cleaning (all deterministic): counter 56,080 rows, cash only 48,873; 2 reversal pairs (both outside the band); machine 38,605 rows, drop 90 pull_sequence 2; machine local date = UTC+12/+13 (Pacific/Auckland); crosswalk 1:1 with all 9,601 register customers, no unmapped deposit customer; FY27 = 44,964 cash deposits, $571.37m.

Excess (bunching) estimate. Density of deposits (non round amounts) is flat to gently declining from 5,000 to 13,000, with no hole above 10,000 and a clear surplus from about 9,500 up. Fitting a line or quadratic to 100-dollar bins outside 9,000 to 10,000 (and skipping the 10,900/10,950 round-number bump) and subtracting from the band gives, per segment, about:
Clubs 30, Fuel 30, Grocery 58, Hospitality 58, Personal services 30, Rural 29, Trades 70, Transport 90; total about 395 (range 354 to 411 depending on where the excess window starts). Rounded to 10: 30, 30, 60, 60, 30, 30, 70, 90, sum 400. Largest segment: Transport and courier. Confidence: about 70 percent that the structuring figure that was meant is this 400 (the clean multiples of 10 are very telling), 30 percent that it is the literal 2,200. Bank's figure: 400 or 2,200.

Choices the documents did not make for me: (a) band count versus excess; (b) the counterfactual (linear, quadratic, other-year baseline; FY26 itself has smaller bunching so it is not clean); (c) where the excess window starts (9,000, 9,300, 9,500) which moves Grocery by about 8 and Transport by about 20; (d) "cash deposits it paid in" is a count or dollars (I give both: Clubs 1,836 / $23.27m; Fuel 6,658 / $84.73m; Grocery 14,111 / $179.51m; Hospitality 11,297 / $143.64m; Personal 2,036 / $25.84m; Rural 3,042 / $38.67m; Trades 3,684 / $46.70m; Transport 2,300 / $29.02m); (e) fiscal quarters for the quarterly asks; (f) sessions of both sources (counter and machine) are counted.

## 8. Realism
Reads as generated, strongly, on the amounts:
- Dispersion. Non-round deposit amounts in 100-dollar bins from 5,000 to 9,000 have variance/mean of 0.11 (a real count process is at least 1.0, usually well above). 250-wide bins: 292, 287, 293, 288, 288, 284, 282, 280, 279, 276, 275, 273, 269, 267, 273, 266, a smooth ramp with scatter of 1 to 3. Between 8,000 and 8,900 the whole bank shows 182, 185, 184, 184, 182, 182, 182, 182, 182, 181 per 100-dollar bin; between 10,000 and 10,800: 177, 178, 177, 177, 177, 176, 175, 176, 175. Per segment variance/mean is 0.02 to 0.08 (Clubs 15, 14, 15, 14, 15, 14, 14, 14). A bank's record bunches at 5,000, 9,000, 9,500, 10,000 with day-to-day noise; this is a deterministic quantile grid.
- Round values: every multiple of 50 away from the threshold has the same count (about 43 each for 500, 550, 650 ... 3,300 across the bank), and within a segment the baseline count at 8,500, 8,600 ... 8,950 is identical (Transport 2,2,2,...; Grocery 12 each; Fuel 6 each). Real round amounts spike unevenly (1,000, 5,000 dominate).
- Cents: non-round amounts end only in 0 or 5 in the last digit and only 20 distinct cents values; a cash count with notes and coin would not.
- Hard floor of 500.00 and ceiling of 32,222.20; no deposits below 500 at all across 45,000 business cash deposits.
- Threshold effect: excess is exactly in multiples of 10 per segment (30, 30, 60, 60, 30, 30, 70, 90) and the round-value surplus sits at 9,800 to 9,950 with matching small bumps at 10,900/10,950 (35 each) and 10,000/10,050 (35 each). No hole above the threshold, which is unlike real structuring.
- Tellers/time: deposit_time_local concentrated at 09:xx (11,375 deposits in the 09 hour), machines show deposits only 09:00 to 20:59 although they are smart machines; till sessions at exact minutes at 16:xx/17:xx counter and 18:xx/19:xx UTC machine only. Branch summary reconciles to the dollar with the feeds, which a real reconciliation pack rarely does.
- Other: service log restored_ts minus reported_ts equals minutes exactly with identical seconds; variance_nzd is symmetric with a hard cap about +/-48 and no variance exactly at 15 or 25; deposits are almost never on the exact tolerance boundary; risk events chain perfectly (no gaps) for 1,964 customers; all 234 service incidents are reported between 08:00 and 16:59.
Realistic touches: the PDFs read as exported (vendor table with page break), the register title block, the provenance notes, the vendor and log agreement for 9 of 11 sites down to the minute.
How a working analyst would notice: a histogram of deposit amounts, a Poisson dispersion test on the bins, or just counting how many times each round amount occurs. The excess then jumps out and the flatness too.

## 9. Supplementary asks

Cash count sessions per quarter (all 9,151 sessions complete; all FY27 sessions both sources; machine sessions converted from UTC; tolerance 25 to 31 Dec 2026, 15 from 1 Jan 2027; "over" = absolute variance strictly greater; no variance sits exactly on a tolerance):

| Quarter | sessions | over tolerance | net variance |
|---|---|---|---|
| Jul to Sep 2026 | 1,145 | 117 | 17.00 |
| Oct to Dec 2026 | 1,126 | 119 | 100.28 |
| Jan to Mar 2027 | 1,081 | 223 | -784.53 |
| Apr to Jun 2027 | 1,101 | 240 | 869.81 |

Determinate once the choice is made, but two things split careful analysts: counter-only versus counter + machine (counter alone: 795/80/-205.95, 777/81/-242.05, 706/154/-574.70, 737/159/766.87), and using UTC dates for machine sessions (changes 1,144 / 1,128 / 1,078 / 1,096 and the nets). Also "per quarter" in the prompt, "branch and quarter" in the handbook. Calendar versus fiscal quarters would also change the answer.

Risk bands (accepted events only, effective date in the year, 1/A = Low ... 5/E = High; no multi-step moves; the 11 superseded events dropped):

| Band | raised into | lowered into | raised in then out again |
|---|---|---|---|
| 1 Low | 0 | 278 | 0 |
| 2 | 478 | 244 | 73 |
| 3 | 339 | 272 | 43 |
| 4 | 291 | 496 | 43 |
| 5 High | 370 | 0 | 96 |

Events and customers differ slightly (band 2 raised: 478 events, 470 customers; band 3 338; lowered 276 / 243 / 270 / 492). Including superseded events gives 480/342/293 raised and 278/245/274/497 lowered. "Out again" is the same under immediate and any-later readings. Forced by the records once accepted events and the relabel are handled; the event-versus-customer count and the "out again" wording are the defensible splits.

Machine service, per month (hours from the log, sum of machine minutes, reported_ts month; log timestamps are local-looking, 08:00 to 16:59, no month crossing): Jul 58.6, Aug 87.1, Sep 74.0, Oct 75.3, Nov 64.7, Dec 116.4, Jan 54.1, Feb 103.0, Mar 64.8, Apr 92.8, May 53.2, Jun 66.3. Differences: SDM-0907 (withdrawn 27 Nov 2026) has 10 rows including Jul to Nov; the dictionary says a decommissioned machine has no rows; if it is dropped the figures become Jul 53.4, Aug 76.3, Sep 66.9, Oct 65.3, Nov 61.9 (Dec onward unchanged). Four same-machine overlapping incidents mean "estate out of service" could also be taken as union time (Oct 74.8, Nov 57.8, Dec 115.9). So the monthly hours are not fully forced: include or exclude the withdrawn machine, sum versus union.

Any machine with no service record: yes, 3 (SDM-1455 at AR25, SDM-1509 at AR28, SDM-1562 at AR31, installed 2025-06, 2025-11, 2026-09, none withdrawn). Forced at 3 (whole-year silence), though a reader might want to ask whether SDM-1562, installed Sept 2026, should count. Note the vendor report omits AR25, AR28 and AR31 entirely.

Any site differing from the vendor by over two hours: yes, AR15 and AR19. At month level the vendor is exactly 4/3 times the log for every AR15 and AR19 month; months over 2.0 hours: AR15 Aug 4.03, Oct 4.08, Nov 2.48, Dec 3.40, May 2.63, Jun 6.37 (Feb 1.87 and Apr 1.78 under); AR19 Sep 3.20, Feb 6.00. All other 78 site-months match to the minute. Answer: AR15 and AR19 (8 site-months). A careful analyst could instead compare annual totals (still the same two sites) or count differences in absolute terms; the two sites are the same either way. The vendor's AR11 rows include the withdrawn machine, against its own footnote, and match the log only if SDM-0907 is included.
