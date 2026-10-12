# Verdict (task137 re-judge)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed and no model rerun. Optional note: the 57-hour gap between 5,568 and the 5,625 rounding line is the thinnest margin (see Evidence).

**Why:** Every committed answer reproduced from the shipped files. The main call turns on one analytical step: the retention-offer share of conversations is a function of the rate drop (held rate less the quarter's posted rate for the same term, brief PDFs), and the 2027 list has a very different drop mix (10,735 four-year deposits at 5.65% against 3.15%, drop 2.50). Past data show 92% at drops of 2.5 or more against 33% pooled. Hours are priced at SOW schedule 2 (1.5 / 8 / 22 minutes). Every plausible rigorous variant I built lands in the 5,500 bin (5,375 to 5,625), and the supplementary figures are rule-closed with no live fork.

## Evidence (recomputed from target/ files)

| Item | Result | Source |
|---|---|---|
| 460 listed deposits with no callable number | Reproduced. Normalising numbers to E.164 and washing against the register as at 2 Nov (recorded by then, not withdrawn by then) gives 460. | kbs_contact_points, kbs_do_not_call_register, kbs_td_retention_list_2027Q1 |
| 10,735 four-year deposits at 5.65%, drop 2.50 | Reproduced (10,735 at 48 months and 5.65%). The list has 18,400 unique members and unique accounts, all at or above 25k. | list, 2027Q1 brief |
| Past RT share | Reproduced. Pooled 32.7% over 45,044 conversations. At drops of 2.5 or more it is 92.25% (1,394 conversations); at exactly 2.50 it is 91.5% (874). Share depends on drop only: monotone, consistent across campaigns and terms. | case_release_log, closeouts, dial_log, past lists, 7 briefs |
| About 14,000 conversations, 67,400 non-reaching dials, 62% RT | Reproduced: 13,959, 67,354, 62.1%. | same, plus 95.46% release rate |
| Hours 5,568.0 (Jan 1,479.5, Feb 2,044.1, Mar 2,044.4) | Reproduced exactly with the golden method (by-mix averages, 0.25-point drop bands, release rate 55,369 / 58,002 = 95.46%). | SOW schedule 2 |
| Supp 3, counts and principal for 7 campaigns | Reproduced exactly: 6,520 / 486,794,035; 7,007 / 526,875,133; 6,902 / 504,703,802; 6,917 / 500,989,171; 6,860 / 503,624,114; 6,933 / 512,432,671; 7,001 / 521,206,617. | account_events, member_transfers, past lists |
| Supp 4, maturing and not on list | Reproduced exactly. Maturing 467,101,713 / 633,665,330 / 633,033,999.67; not on list 60,860,311 / 74,665,029 / 80,660,982. | term_holdings (deduped by account), KIC register, migration batches, list |

**Supp 3 closure.** The rule is cleanly closed. Every maturity-proceeds destination is either a savings or other-bank account, or a TD opened that day with a matching OPEN event. No transfer goes to a TD opened on another day, and none to a different customer_no. All BREAKs fall 3 to 24 days after opening, so any window from 24 to 60 days gives the same count of 37,537 kept own-account reinvestments. Partial proceeds are real (4,791 cases) and are handled by the prompt's "only the part that was". The rounding values sit nowhere near .5 thousand.

**Supp 4 closure.** The 579 KIC rows in the core holdings are exactly the migrated certificates, and principal matches. DEFERRED-then-MIGRATED certificates are covered by taking any MIGRATED row. Joint accounts appear twice in holdings (6,253 duplicated accounts) and are counted once. The treasury xlsx (870.4m January maturities, 82% reinvest) includes wholesale funding and is a distractor excluded by "across all our members".

**Hours: literal reading and forks.**
- The estimand is the forecast of agent-hours for the list. Procedure 6.1 says to draw on every closed campaign, and the SOW minutes and the 250 rounding are filed.
- Open method choices all land in the same bin:

| Variant | Hours |
|---|---|
| Golden (band shares, by-mix) | 5,568 |
| Exact-drop shares | 5,549 |
| Logistic in drop | 5,555 |
| No mix split (overall averages) | 5,569 |
| Mix by number count only | 5,574 |
| Release rate applied to the full list instead of removing 460 | 5,589 |

- Month figures sit mid-bin: Jan 1,479.5 (bin 1,375 to 1,625), Feb and Mar 2,044 (bin 1,875 to 2,125). The rounded months sum to the rounded total.
- Variants that give other answers are method errors, not fork readings:

| Variant | Hours | Rounded |
|---|---|---|
| Pooled share (33%) | 4,611 | 4,500 |
| Latest-campaign share | 4,694 | 4,750 |
| Share by term | 3,997 | 4,000 |
| Share by rate level | 5,307 | 5,250 |
| Ignoring the 4.5% released-to-instructed attrition (reason INSTRUCTED, flat 4.2 to 5.4% in every drop band) | 5,833 | 5,750 |

- The drop is separated empirically from the rivals. Log-likelihood by drop is -16,741, against -17,874 by rate level, -21,793 by term and -28,102 by campaign. Within the same 5.65% rate, share runs 41% to 88% as the drop varies.
- Reach and non-reaching dials do not depend on drop, principal, term or maturity month (residuals about 0 after the mix control), so the mix-based reach model is not biased by the shift.

**Weak points, none disqualifying:**
- The margin to 5,625 is 1.0%. All methods I could justify stay under it, and the 5,750 route needs ignoring a measured attrition rate.
- 460 depends on withdrawn register rows being excluded. Ignoring withdrawals gives 501 and moves hours by about 0.2%.
- The 2.50 drop is the top edge of observed support (874 conversations exactly at 2.50). This is supported by data, not extrapolated.

## Files/Hygiene: PASS
- 27 files in 6 formats (pdf x10, csv x13, eml, txt, docx, xlsx). The largest csv is 264,592 rows, with a 55k-row case file and a 59k-row release log.
- Distractors: treasury funding xlsx, 2027 staffing proposal (66.10 rate, capacity 9,000), block-order email (66.10 against SOW 64.80). None is needed for the answers.
- File-level realism is good: legacy and current core layouts (dd/mm/yyyy with commas against ISO, hyphenated accounts), mixed phone formats, joint holders, platform migration. File metadata is Word, Excel and plain-author PDF, with no tool banners and no authoring disclosures.
- Dates are coherent: 2 Nov 2026 is a Monday, the email is dated 4 Nov, and the SOW 20 Nov booking deadline matches.
- No exclusion-level finding. Not checked: public-data contamination (the data is a fictional NZ society) and the cross-batch fingerprint (other task folders are outside my permitted reads).

## Stump power
A natural lazy path is a pooled, latest-campaign or per-term retention share, which gives 4,500 / 4,750 / 4,000. All are wrong, and each is a plausible first move. Reaching 5,500 requires seeing that the 2027 list's drop mix is outside what the history averages over, and conditioning on the drop. Nothing in any file names the relationship. Strong models that segment by term will find a 3.7% four-year share and drift further wrong. Moderate to good stump; the supplementary asks (own-account reinvest versus new-account rollover with partial proceeds, joint-account dedupe, KIC migration) add independent chances of error.

## Stumping type
`mechanism: forecasting` (covariate-shift-aware forecast, close to method_or_model_selection), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported figure is wrong; the shortcut is a correct pooled number applied to a population it does not describe. On clean data the task still stumps. Gate G passes.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Layer 1: two core-banking layouts and account formats, phone normalisation against a dated register, joint holders, an investment-platform migration. None of it is planted or decisive.
- Layer 2: estimating how retention-offer take-up responds to the rate drop and forecasting call workload for a list whose drop distribution is outside the history's typical range. This is deposit-rate sensitivity, which is a retail-banking analysis; the swap test with hospital nouns breaks the "rate drop" mechanism.
- Easy route: pooled share of 33% with correct cleaning, giving 4,611 hours and a 4,500 booking against the golden 5,500.

## Fix
none.

## Disposition

Approved as judged (judge-task137b, the re-judge after the pass 1 FIX_NOW in `determinism_check_report.md`). No
graded figure, pack file, golden, write-up or prompt changed after the verdict.

1. **The thinnest margin (the optional note).** 5,568.0 hours sits 57.0 hours (1.0 per cent) under the 5,625 line.
   The generator's 32-member corridor runs 5,416.0 to 5,586.3 and files 5,500 and the three months in every member
   (asserted); the re-judge's variants run 5,549 to 5,589. The one cell over the line is the drop without the release
   share (5,832.8, booked 5,750), which procedure 4.2 refuses (SF11). Recorded in the design note under the Ladder
   (Margins after the re-judge). No change.
2. **The withdrawn registrations (weak point 2).** The 460 count reads the register as it stood at the cut, a number
   whose registration was withdrawn by 2 November being callable (SF5); the re-judge measured the reading that ignores
   withdrawals at 501 deposits and about 0.2 per cent of the hours, inside the bin. No change.
3. **The 2.50-point drop at the top of past support (weak point 3).** 874 past conversations sit at exactly 2.50 and
   1,394 at 2.5 or more, so the four-year deposits' share is read off observed conversations, not extrapolated. No
   change.
4. **The shipped bundle against the judged one.** The final rebuild's 27 files under `target/` are byte-identical to
   the judged copy, and the prompt and the write-up's blocks 1 to 4 are the ones the re-judge read. Free gates on it:
   `checks.py` 448 assertions; `verify.py` 32 checks from the bundle alone; two builds byte-identical (target, goldens,
   `metadata.json`, `figures.json`, `target.zip`); `figures_check.py` exit 0 (80 figures); `precut.py` exit 0 (38
   checks, `voice-check.py` PASS); `leak.py --asof 2026-11-04` REVIEW, the same 25 lines, no LEAK; container audit
   clean; `guard.py surface` exit 0, `heart` WARN (`repeat.gate_g`, answered at the draw), `validate` clean;
   `freeze.py check --mode determinism` PASS. `target.zip` is cut from that rebuild by the generator's `cut_zip` (27
   members, equal to `target/`; sha256 d5644068df2d6430b521a0830bcf4a5773841fa2da7cc31dad4f0bc4b5c985ca).
