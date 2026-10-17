# leak check, task190

**Verdict: REVIEW.** 21 files read, 51 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: deposit, clause, asserted, nothing, states, reporting, sentence, dictionary, decisive, window, screen, customer, surplus, background, excess, register, stated, extract, profile, carries, branch, reading, same-day, deficit, second

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `aml_programme_handbook.pdf`: carries 11 of 12 distinctive words of the committed call: 'The annual report should state that 450 cash deposits were split below the prescribed transaction threshold in the repor'
- **REVIEW** `annual_report_extract_2026.pdf`: carries 8 of 12 distinctive words of the committed call: 'The annual report should state that 450 cash deposits were split below the prescribed transaction threshold in the repor'
- **REVIEW** `provenance.md`: carries 8 of 12 distinctive words of the committed call: 'The annual report should state that 450 cash deposits were split below the prescribed transaction threshold in the repor'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `aml_programme_handbook.pdf`: 10 of 25 stump-paragraph terms appear (deposit, nothing, states, reporting, customer, register); read whether the document names the move
- **REVIEW** `annual_report_extract_2026.pdf`: 5 of 25 stump-paragraph terms appear (deposit, reporting, customer, stated, extract); read whether the document names the move
- **REVIEW** `provenance.md`: 8 of 25 stump-paragraph terms appear (deposit, nothing, reporting, customer, register, extract); read whether the document names the move
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

## Solver's-eye read (pass 3)

# Reader answers, task190 loop 3

## Headline
Decisive step: estimate the structuring figure as an excess-mass (bunching) estimate. Take each segment's deposit-amount distribution, build the counterfactual density for the 9,000 to 9,999.99 band from the segment's deposits outside the band, and subtract it from what the band holds. The band count itself is the wrong answer.
Committed answer: bank total 500 split deposits. Per segment, to the nearest 50: Transport and courier 150, Grocery and convenience 150, Fuel and automotive 50, Hospitality 50, Personal services 50, Trades and construction 50, Clubs and community 0, Rural supply and horticulture 0.
Largest segment: Transport and courier (unrounded about 155, against about 143 to 150 for Grocery). Confidence in the total: moderate. About 450 to 550 is defensible. Confidence in Transport as largest: about 65 percent. The rounded figures tie at 150, so the rounded table does not itself name the largest.

## Cleaned base (46,772 cash deposits in the year, 406,978,442.72 NZD)
- Counter: cash only, which drops 4,431 cheques and 3,461 credits. Drop the 2 reversing rows and the 2 deposits they reverse. Keep deposit_date in 2026-07-01 to 2027-06-30.
- Machine: keep one row per machine_deposit_ref (82 pull_sequence 2 resends dropped). Convert UTC to Pacific/Auckland. The UTC date equals the local date for every row (machine UTC hours are 0 to 7, local 13 to 20), so the conversion never moves a deposit across a date.
- Link: acct_customer_no to master_customer_no through the crosswalk (all link), then to the register segment (all match).
- Tie-out: branch_cash_summary_2027.csv sums to 46,772 deposits and 406,978,456.37 NZD. That is the same count and a $13.65 difference, so the cleaning reproduces the desk's total.
- Deposits per segment (cash deposits paid in): Clubs 2,718; Fuel 4,175; Grocery 15,131; Hospitality 4,758; Personal services 3,993; Rural 2,396; Trades 3,168; Transport 10,433.
- Dollar totals if wanted, in millions: Clubs 23.05, Fuel 35.14, Grocery 131.46, Hospitality 38.81, Personal 30.93, Rural 22.08, Trades 28.77, Transport 96.74.

## Part 2 answers

**1. What is asked, and does a column hold it?** The question asks for the number of deposits paid in below 10,000 that would otherwise have been at or above it. No column holds that. Handbook 7.4 says "The figure is a property of the year's deposits and is not a field." The prescribed extracts, and the near-threshold queue in 3.2, are not it.

**2. Defensible answers.**
- Naive: count deposits in [9000, 10000). Total 2,583 pooled, with Grocery 808 the largest and Transport 632. This is wrong, because 7.4 says "no part of it evidences what the band would have held".
- Bunching estimate: Poisson GLM of 100-dollar bin counts on a polynomial, band excluded, excess = observed minus predicted in the band.
  - Fitting outside the band only, pooled, gives about 590 (degree 5).
  - Also excluding the notch [10000, 11000) gives about 468 to 508. Excluding to 11,000 or beyond makes the band excess equal the missing mass above 10,000: excess 483 against missing 448 to 491 (U 11,000 to 13,000, degree 4 and 6).
  - A grid of 60 specifications (notch bound 10,000 to 12,000, degree 3 to 6, three fit windows), summed over the 8 segments: median about 500, range 443 to 728.
- Per segment, notch to 11,500, degree 5: Clubs -9, Fuel 56, Grocery 153, Hospitality 50, Personal 62, Rural -8, Trades 47, Transport 153. The sum is about 500, and these round to 0, 50, 150, 50, 50, 0, 50, 150.
- Across the grid, Transport exceeds Grocery in 95 percent of specifications. Medians are Transport 155, Grocery 141, Personal 66, Hospitality 57, Trades 55, Fuel 55.
- Mass conservation, segment by segment, would shrink Grocery. Its missing mass above 10,000 is only 9 to 64 against an excess of about 150, whereas Transport balances (157 against 155). A solver who forces per-segment balance would get a lower Grocery and a total near 430, and Transport would be clearly largest.
- Settled by: the 7.4 sentence "that has to come from the segment's trade outside the band" and the data shape. Nothing fixes the functional form, the bin width or the notch width, and the tolerance is not filed.

**3. Planted or generated tells.** Yes, several.
- Cents alphabet. Only 72 distinct cent values occur. Last digit of the cents: 0 = 32,127; 1 = 2,078; 2 = 351; 3 = 2,232; 4 = 174; 5 = 5,116; 6 = 353; 7 = 1,991; 8 = 195; 9 = 2,155. Even digits other than 0 are nearly absent. Cents values 28, 64, 82, 94, 96 and 98 appear 1 to 2 times, while neighbouring odd values appear 150 to 200 times. Cents of 25, 50, 75 and every multiple of 5 are inflated (50: 1,740; 25: 943; 75: 866). A real 1,000 to 10,000 dollar cash count would not have this. It looks like a generator that draws a cents list.
- Whole-dollar share is 56.6 percent and multiples of 50 are 46.6 percent of all deposits. That is a plausible habit, but the share is high for amounts counted by machine.
- Round-value spikes in the band: 9,500 (96), 9,750 (76), 9,800 (113), 9,900 (118) and 9,950 (107), against 55 to 60 at neighbouring multiples of 50. 9,500 is concentrated in Fuel, Hospitality and Transport. The excess sits only on round values: non-round amounts show no bump at 9,800 to 9,999 (229 against about 255 base). That is the mark of an inserted behaviour and not of an organic one.
- Hard bounds. Floor exactly 50.00 (one deposit, then 95.25 and 100.00 x3). Ceiling 53,471.19. Both look like truncations of a continuous curve, not tails.
- Dispersion. Counts per 100-dollar bin outside the band, non-round amounts, against a smooth degree 4 to 8 polynomial: Pearson chi2/df = 0.94 to 0.95. This is slightly under-dispersed relative to Poisson. Real deposit amounts from 9,600 customers would be over-dispersed (a campaign, a payday, large single customers). The scatter is a Poisson draw on a smooth curve.
- Machine hours. All machine deposits fall at local 13:00 to 20:59 (UTC 00 to 07 only), and machine collection sessions are at UTC 00 to 01 only. No machine deposits in the morning or at night. Counter hours are 09 to 18 with a dip at 13. Weekend counter volumes are exactly about half of weekdays (5,212 and 5,167 against about 10,200).
- Vendor ratio. Vendor minutes for AR15 and AR19 are a constant multiple of the log: 590/441, 805/601, 443/331 and 757/565 all give 1.338 to 1.340. A real sign-off lag would add minutes per visit, not scale by 1.34 uniformly. The other 9 sites tie to the minute, in every month.
- Reconciliations. The summary ties to the feed count exactly and to within $13.65 on $407m. Vendor report ties to the log to the minute for 9 of 11 sites in all months. Both are too clean for independent systems.
- Annual report 2026: 385.3 million against 407.0 million this year (+5.6 percent) is plausible.

**4. Does any file rank segments on the question?** No file states a structuring figure or ranking. The 2026 annual report extract says "the cash-intensive segments carry the bank's highest residual risk", which points toward volume-heavy segments (Grocery, Fuel, Hospitality) and would mislead. The prescribed-transaction extracts could be joined to segments, but they hold only deposits at or above 10,000. Their union equals the 15,555 feed deposits of 10,000 or more exactly (preliminary 13,664 + revised 3,651, 1,760 overlap). They carry no band information.

**5. Did a sentence hand over the method?** Yes.
- Handbook 7.4: "The whole of that band is what the figure estimates, so no part of it evidences what the band would have held absent the practice; that has to come from the segment's trade outside the band." This is the decisive step, stated almost outright.
- 7.4 also says "Each such deposit counts one for one: the figure is of deposits and not of their value, and not of customers and not of days."
- 3.2 says the queue and alert "decide nothing" and that most of what they raise is "ordinary trade".
- The word "estimates" tells the solver this is an estimation problem. What the handbook leaves open is the functional form, the band edges for the fit, and whether the notch above 10,000 should be excluded.
- Literal reading: the figure is the count of deposits paid in below 10,000 "when the amount would otherwise have been at or above it". That is a count of shifted deposits, not of band deposits. Its literal numeric result cannot be computed from a stated sentence. It equals the missing mass above the threshold, which my fit puts at about 450 to 490, and the excess below, about 480 to 500.

**What decides the main answer.** An analytical choice: the counterfactual, not reading a field. Only reading rules of the cleaning (cash only, reversal pairs, resends, crosswalk) are semantics, and they do not decide the segment ranking.

**6. Side questions.**
- Cash count sessions by quarter (all forced). Quarters of the reporting year (Jul to Sep is Q1). Tolerance 25 to 31 Dec 2026, then 15 from 1 Jan 2027. Pass when absolute variance is at or under the tolerance. All 9,151 sessions are "complete", and machine sessions are UTC but their date never differs from the local date.

| Quarter | Sessions | Over tolerance | Net variance (NZD) |
|---|---|---|---|
| Jul to Sep 2026 | 1,145 | 117 | 17.00 |
| Oct to Dec 2026 | 1,126 | 119 | 100.28 |
| Jan to Mar 2027 | 1,081 | 223 | -798.74 |
| Apr to Jun 2027 | 1,101 | 238 | 944.81 |

  Total 4,453. Five sessions sit exactly at 15.00, and counting them as over would add 5. The register sentence settles that. The handbook asks per branch and quarter but the prompt asks per quarter, so I filed totals.
- Risk bands (forced, with one residual judgement). Use accepted events only. Map letters to numbers (A=1 and so on) so the April 2027 relabel does not split a band. Customers 1,969, with 1,445 having one event, 495 two, 29 three. Rating moves are plus or minus 1, with 8 plus-2 and 3 minus-2 jumps. Raised into band: 2 = 392, 3 = 402, 4 = 320, 5 = 230, band 1 = 0. Lowered into band: 1 = 240, 2 = 241, 3 = 306, 4 = 391, band 5 = 0. Raised in then out again (raised into the band, later left it by being raised on): band 2 = 153, 3 = 115, 4 = 3, bands 1 and 5 = 0. Two defensible variants: counting the superseded rows gives 398 and 404 for raised into 2 and 3, which the dictionary rules out. A band jumped over by a two-step move is not counted as entered, which I took as the natural reading. "Out again" by being lowered gives zero for every band, because nobody reverses.
- Machine hours by month, with the month of an incident not forced. By reported month in hours: Jul 75.9, Aug 91.7, Sep 94.0, Oct 78.9, Nov 56.9, Dec 82.5, Jan 95.4, Feb 134.9, Mar 54.2, Apr 98.2, May 72.9, Jun 63.2 (sum 998.6). Four incidents cross a month end (SI000515, SI000583, SI000397, SI000216). By restored month: Aug 85.3, Sep 94.2, Oct 85.0, Nov 49.5, Dec 89.8, Apr 92.4, May 78.7. Pro-rata: Aug 89.5, Sep 92.2, Oct 82.9, Nov 54.2, Dec 85.2, Apr 94.2, May 76.9. The vendor report ties to the log by reported month, which I take as the convention, but no sentence files it. The minutes column wins over the timestamps in 5 incidents, and the dictionary says so.
- Machines with no service record (forced): yes, 3 of the 20 in the register (SDM-1455 at AR25, SDM-1509 at AR28, SDM-1562 at AR31), each in service during the year. The vendor report also omits those three sites.
- Site hours differing from the vendor by over two (forced): yes, AR15 (log 62.3 h against vendor 83.5 h, -21.1) and AR19 (log 102.1 h against vendor 136.8 h, -34.6). The other nine sites tie exactly. This holds whether the test is per site-month (AR15 has five months over two, AR19 seven) or per site-year. Note SDM-0907 and AR11: the log holds nothing after the 27 Nov 2026 withdrawal and the vendor report omits it, which is consistent.

**7. Inconsistencies.**
- The prompt says the split deposits are to the nearest 50 per segment, while handbook 7.4 says the nearest ten. The prompt governs, but the two differ.
- The prompt asks for cash count sessions per quarter, while handbook 7.6 asks per branch and quarter. Machine availability is also stated differently ("availability" against the prompt's hours).
- The manifest lists the handbook as "Version 9.2, approved 14 May 2026". The PDF says version 9.4 approved 11 June 2027.
- The annual report 2026 extract says paragraph 7.4 was approved May 2026 but the figure was first stated for FY2027. That is consistent, but it also means no prior-year figure exists to calibrate against.
- The vendor report is 34 percent higher than the log at two sites and exact at the other nine.
- provenance.md says teller feed 61,568 and machine feed 37,275 rows, and both match.

## Helper and unused files
- Helpers: `field_dictionary.csv` (it states the reversal pair, resend and superseded rules, which would be in a data-management dictionary but are very pointed here); `vendor_service_report_2027.pdf` (serves only the site comparison, and a real one would carry per-incident dispatch references and machine ids, not a clean site-month table); `rating_scale_map.csv`; `cash_tolerance_register.xlsx`. The handbook 7.4 text is the biggest helper. A real handbook paragraph would not tell the analyst the estimation logic ("has to come from the segment's trade outside the band") nor say that the reporting officer "satisfies himself" the figure rests on the year's records.
- Unused for the answers: `card_settlement_summary_2027.csv` (48,304 rows, customer-month card totals; a real file would have merchant ids, batch dates and chargebacks); `annual_report_extract_2026.pdf` (prior-year figures, not needed); both `prescribed_transaction_extract_*.csv` (tie-out only, and a real one would carry report status, reviewer and filing dates); `branch_cash_summary_2027.csv` (tie-out only); `branch_register.csv` (the 9.3 branch merge changes nothing asked, since the prompt asks for totals); `anzsic_code`, `trading_name` and `relationship_opened` in the customer register.
