# Verdict, task137 (Kaimai BS / Harbourline Q1 2027 block order)

**Verdict:** DETERMINISTIC (SOLUTION_WRONG on wording only; no committed figure fails to reproduce).

**Disposition:** FIX_NOW. Regenerate the solution blocks (garbled last two sentences of the Final Recommendation; "about 60 per cent" and "about 67,500 dials" should read about 62 per cent and about 67,400). Optional one-clause prompt pin on ask 3 (see Evidence, fork F1); if the author takes that option only ask 3 needs a rerun, the booking and ask 4 are untouched.

**Why:** The booking is forced by the files. Procedure v4 6.1 makes the booking the forecast need drawn from all seven closed campaigns. SOW schedule 2.1 prices the dials and conversations. The closed-campaign data show that the share of conversations that go to the 22-minute retention offer (RTK/RTW) is a smooth function of the rate drop (locked rate less the posted rate for that term in that quarter's brief). The 2027Q1 list is dominated by 10,735 four-year deposits at 5.65 per cent against a 3.15 per cent posted rate, a drop of 2.50 points. That puts the list's share near 62 per cent, against 33 per cent pooled. Every reasonable way of estimating that share lands at 5,550 to 5,590 hours, which is 5,500 at the nearest 250. Every share-blind method lands at 4,600 to 4,750.

## Evidence (recomputed from target/ only)

Reproduced exactly:

| Item | Result | Source |
|---|---|---|
| DNC wash | 460 of 18,400 deposits with no callable number. Contact numbers normalised to E.164 (leading 0 becomes +64); register rows recorded by 2 Nov 2026 and not withdrawn. | kbs_contact_points, kbs_do_not_call_register |
| Release rate | 95.46% of listed deposits with a callable number were released across the seven campaigns (55,369 of 59,265 listed; 3,896 not released: 2,633 INSTRUCTED, 1,263 NO CALLABLE NUMBER). Stable across campaigns. | kbs_case_release_log |
| Conversations | 45,044 across the seven campaigns; 32.7% went to RTK/RTW. | closeouts, dial log |
| 10,735 four-year deposits | 5.65% locked against 3.15% posted, a drop of 2.50 points. | retention_list_2027Q1, 2027Q1 brief |
| Share at large drops | Share of conversations to the retention offer: 0.9225 in the 2.50 band (0.915 at exactly 2.50, n=874). | closeouts joined to the 2025/2026 lists and the briefs |
| Booking | 5,568.0 h total; Jan 1,479.5, Feb 2,044.1, Mar 2,044.4. This is the golden's own model, rebuilt. Booking 5,500: 1,500 / 2,000 / 2,000. | dial log, closeouts, lists, briefs |
| List's retention-offer share | 62.1% (golden text says "about 60"). | recomputed |
| Expected conversations | 13,959 (golden "14,000"). | recomputed |
| Non-reaching dials | 67,354 (golden "about 67,500"; wording only). | recomputed |

**Ask 3.** The golden rule (REINVEST on own account at maturity, or maturity-proceeds transfer into a Society account opened that day, with no BREAK/CLOSE within 30 days, principal = list principal or amount transferred) reproduces all seven rows exactly:

| Campaign | Deposits | Principal (NZ$) |
|---|---|---|
| 2025Q1 | 6,520 | 486,794,035 |
| 2025Q2 | 7,007 | 526,875,133 |
| 2025Q3 | 6,902 | 504,703,802 |
| 2025Q4 | 6,917 | 500,989,171 |
| 2026Q1 | 6,860 | 503,624,114 |
| 2026Q2 | 6,933 | 512,432,671 |
| 2026Q3 | 7,001 | 521,206,617 |

All exits (BREAK/CLOSE) fall 3 to 24 days after maturity, so there is no edge case at day 30.

**Ask 4.** Reproduced exactly; joint-holder rows deduplicated by account; migrated certificates counted once, using the latest migration status.

| Month | Maturing (NZ$) | Not on list (NZ$) |
|---|---|---|
| Jan 2027 | 467,101,713 | 60,860,311 |
| Feb 2027 | 633,665,330 | 74,665,029 |
| Mar 2027 | 633,033,999.7 | 80,660,982 |

Ask 4 inputs:
- Holdings has 6,253 duplicate account rows (joint holders). Each account is counted once.
- KICs migrated to the core appear in holdings as product KIC; the 150 DEFERRED rows include 65 certificates that were later MIGRATED. Only certificates whose final status is not MIGRATED are added from the register.
- List principal equals holdings principal for all 18,400 accounts.

**Literal-reading forks (silent points) and their answers:**
- **F1 (moderate, ask 3). Partial retention.** 4,890 maturing deposits sent part of the proceeds into a new Society TD and part elsewhere. The prompt does not say whether such a deposit is "still on term deposit". The golden counts it, with principal equal to the amount transferred, which fits "how much of their principal". A count of fully retained deposits only gives 5,889 / 6,338 / 6,170 / 6,218 / 6,142 / 6,252 / 6,340 and principal of about 456 / 495 / 469 / 467 / 468 / 478 / 489 M. Counting the same deposits with full list principal gives about 503 / 543 / 524 / 520 / 522 / 531 / 538 M. I judge the golden reading the better licensed one because the ask says "how much of their principal", but it is a real risk of a split on this ask.
- **F2 (closed). Release share.** The listed deposits that are never released are 2.1% no-callable and 4.4% INSTRUCTED. A solver who ignores the INSTRUCTED share gets 5,833 h, which is 5,750; one who ignores both gets about 6,000. Procedure 4.2, 4.3 and the release log pin both effects, so these are errors, not forks.
- **F3 (closed). Booking rule.** The procedure fixes the booking at the forecast need, so the +35% overage asymmetry, the $66.10 rate, the 9,000-hour capacity and the 750 minimum are distractors. Rounding per month or in total gives the same 5,500.
- **F4 (closed). Statistical form of the retention-offer share.** Share by 0.25-point band, by 0.5-point band, by exact drop, and logit (linear, quadratic, cubic) give 5,549 to 5,560 h. The 5,625 rounding line is 1% above the golden; the nearest rival (pooled released/listed with no wash and no mix model) gives 5,589, still 5,500.
- **F5 (closed). Competing wrong answers:**

| Method | Hours | Booking |
|---|---|---|
| Pooled 33% share | 4,611 | 4,500 |
| Latest campaign (35%) | 4,694 | 4,750 |
| Pooled hours per listed deposit | 4,637 | 4,750 |
| By term | none (no past four-year data) | n/a |
| By locked rate | none (past 5.65% rate rows are rare and the share is explained by the drop) | n/a |

No other driver tested: at fixed drop the share does not vary with term, campaign, principal or month, and conversation rate and dial count do not vary with the drop.

**Other checks:**
- No January close-down effect in the closed Januaries.
- Mix of mobile/home/work numbers is immaterial.
- Dial log: no duplicates; dials per case match closeouts.

## Files/Hygiene
**PASS.** 27 files; formats: pdf (9), csv (13), docx, xlsx, eml, txt. Metadata is in-fiction (authors Hazel Johnstone, Harbourline, Sienna Stewart; creation dates inside the fiction timeline). Dates and weekdays are coherent: 2 Nov 2026 is a Monday, and 20 Nov per SOW 2.2. The events extract runs to 31 Oct 2026, so every 30-day window closes inside the data. Layer 1 mess is realistic: five phone formats, 16-digit versus dashed accounts, DD/MM/YYYY and comma principal in the 2025 list versus decimal rates in the 2026 lists, joint-holder duplicates, a KIC register that predates the migrations. No authoring or benchmark language found. The 2027Q1 brief is marked "draft" while its rates are stated as ALCO-approved; harmless. Distractors: the treasury outlook (82% reinvestment, maturities 870/892/787 M that do not equal core maturities), the proposal's $66.10 rate and 9,000 capacity, talk_sec in the dial log (SOW bills fixed minutes). Synthetic NZ data, no public-data contamination. Nothing exclusion-level.

## Stump power
Moderate to good. The main trap is the pooled or latest-campaign share of retention-offer conversations (33 to 35 per cent), which is correctly read from the past; the list's rate-drop mix is a regime change the trailing share does not pin, and finding it needs the posted rates read from eight PDFs and joined to the lists and the dial outcomes. Share-blind answers (4,500 / 4,750) are a visible wrong land, and the supplementary asks carry independent traps (partial transfers, split exits, joint-holder duplicates, deferred then migrated certificates, dashed 2025 account IDs). Risk to the bar: a strong run may test conversation codes against the rate gap and get the call; the asks must then do the work, and F1 is the one place a "wrong" ask answer may be a defensible reading rather than a stump.

## Stumping type
`mechanism: forecasting` (with etl_conformance in the asks), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported figures are correct (the 33% is real); the difficulty is a forward projection under a changed drop mix, which the clean data would still stump on.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. The deciding quantity is a propensity-to-withdraw forecast as a function of the rate gap, which is what a deposits or contact-centre planning team would estimate; with another field's nouns the task stops making sense. Layer 1 is the multi-format, multi-era data conformation; Layer 2 is the conditional-share forecast. The easy route, a pooled or latest share of retention-offer conversations applied to a cleaned list, gives 4,500 to 4,750 hours.

## Fix
Where: solution (wording) plus an optional prompt clause. Solution: correct "about 60 per cent" to about 62 per cent and "about 67,500" to about 67,400 non-reaching dials; rewrite the garbled closing sentences of the Final Recommendation. Prompt, optional: in ask 3 add a clause that a deposit counts if any of its maturity proceeds were in a Society term deposit 30 days after maturity, and that principal is the amount in term deposit (this closes F1 without moving any figure).

**Disposition (author, 2026-10-12):** FIX_NOW applied in one generator pass; re-judge next. Solution: the list's share of conversations to the retention offer reads about 62 per cent and the non-reaching dials about 67,400 in the write-up and the note; the Final Recommendation's last two sentences rewritten; the incidental 0.1 per cent dropped from step 3. F1 closed in the prompt with one clause on ask 3, "counting a deposit if any of its principal was, and only the part that was" (923 characters), fork row SF18, the reader's readings SF19 to SF21; no Deliverable Answer, booking or month moved, and target/ is unchanged.
