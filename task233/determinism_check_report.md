# task233 determinism check (architecture 3)

1 isolated judge pass(es), each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | edd35bde | DETERMINISTIC (order kept; F moderate to good; G PASS, statistical_rigor / analytical_non_defect; H PASS) | APPROVE | solution step 8 names the de-duplication of the three replacement rows exported twice (write-up only; target.zip unchanged); the optional WHAT pin on the lag correction not taken, since standard 3.1 already files the price at the time the collector recorded it |

The architecture 2 record is in the folder's archived reports. The leak reader read 62987245 first; its realism finding was fixed before the judge read edd35bde.

---

# Determinism check, round 1 (2026-11-02): DETERMINISTIC (order kept; F moderate to good; G PASS, statistical_rigor / analytical_non_defect; H PASS), APPROVE

Isolated thread, Sonnet at medium effort, on target.zip edd35bde.

# Verdict, task233 (a3r2)

**Order kept:** yes. derivation.md was written to disk before graded_blocks.md was opened.

- **Verdict:** DETERMINISTIC (all five gates A-E pass). One residual fork risk is recorded below (R1). The solution blocks have one minor wording gap (R2).
- **Disposition:** APPROVE. R1 can be left as is, or closed by a pin of the WHAT only (see Fix). R2 is a solution-block rewording that needs no model rerun.
- **Why:** The standard files the estimand in 3.1: the share of recorded prices that were the offered price at the time the collector recorded it. The register's Re-collected on column gives the lag to each re-collection: about 1 day in Halbrook Central, North and South, and about 5 days elsewhere. The price-change frequencies in cpi_field_quotes then give the exposure to a shelf change over that lag. Every band outcome, the credit and all 42 asked per-region figures reproduce from the files. The band outcomes hold across every reasonable variant of the lag correction, and the credit is a single region's fee, so there is no rounding fork.

## Evidence (recomputed from target/)
- **Back-checks.** 6,125 found prices (80 Not found, left out); 199 raw mismatches. CR01 raw mismatch 1.1 per cent, CR05 7.2 per cent. Both reproduce.
- **Raw agreement.** CR01 98.92, CR02 97.18, CR03 98.78, CR04 97.52, CR05 92.84, CR06 97.14, CR07 95.09, CR08 97.37, CR09 97.35, CR10 94.90, CR11 97.32, CR12 94.95, CR13 97.49, CR14 97.23. Band outcomes: 2 compliant (CR01, CR03), 8 corrective action and 4 service credit (CR05, CR07, CR10, CR12), credit USD 7,049. This matches the "would put seven compliant regions under corrective action and three corrective regions on credits ($7,049)" sentence in the recommendation.
- **Lag-adjusted accuracy (the golden's method).** Agreeing back-checks divided by the sum of (1 minus the monthly price-change frequency) to the power lag/30.4, with the frequency taken by COICOP class and outlet type from 47,209 consecutive same-variety quote pairs (frequency 9.95 per cent). Results: CR01 99.18, CR02 97.39, CR03 99.18, CR04 99.29, CR05 94.33, CR06 99.28, CR07 96.68, CR08 99.49, CR09 99.11, CR10 96.56, CR11 99.39, CR12 96.49, CR13 99.18, CR14 99.33. Outcome: only CR05 is a service credit, CR02, CR07, CR10 and CR12 are corrective action, the other nine are compliant. This matches the golden exactly.
- **Robustness of the bands.** All of these gave identical bands for all 14 regions: frequency by class only, type only, item x type, kind, class x kind; month base 30, 30.4 or 31; lag from the first or the last visit date; frequency from Oct-Mar only or Jun-Sep only; including variety changes as changes; an additive form; a linear form. The smallest margin to a band is CR02 at 97.39 against 98.0, and CR02 has almost no lag, so the correction barely moves it.
- **Credit.** CR05 fee 44,380 x 4 per cent = 1,775.2, so USD 1,775. One region only, so no round-each versus round-the-total fork.
- **Data supports the correction.** Observed mismatches (199) exceed the drift expected from the lag exposure (93). The excess concentrates in CR02, CR05, CR07, CR10 and CR12 and is about 3 or fewer in the other nine. 61 per cent of mismatches show an FQT price equal to the next month's collector price, against a 5.8 per cent price change in the following month among agreeing prices. Eleven regions have no back-check with a lag under 3 days, so a short-lag-only estimate is not available. The correction is the only workable route to the filed estimand.
- **Timeliness and missed visits.** Window by the calendar: Jul 14-17 and 20, Aug 11-14 and 18 (17 Aug is a holiday), Sep 8-11 and 14. 963 scheduled rows; 16 Lifeline branches closed 31 July and were taken over by CareMed at the same address from 1 August, so the schedule keeps the Lifeline numbers while the visit log uses the CareMed numbers; mapped by address in the outlet register. 9 missed, 38 late. All 14 regions agree with the golden on timeliness and missed visits (for example CR03 95.1 with 2 missed, CR07 95.5, CR12 98.4).
- **Duplicate quote rows.** 109 duplicate quote rows (same quote_id and price, later load_batch). Unique quotes equal prices_entered in the visit log for all 954 outlet-months, so the duplicates are re-uploads and every price is recorded at its visit.
- **Replacement acceptance.** 198 replacement events after deduplication (201 raw rows). Status R before 3 Aug and 30 after (handheld_status_codes.csv). Each decision is assigned to the latest replacement of its quote collected on or before the decision date. All 14 regions match the golden (CR01 68.4, CR09 42.9, CR07 88.9, and so on).
- **Silent options listed.**
  - Replacement counted as the event (golden and literal) or as the distinct quote with its latest decision overall: the second gives CR01 63.2, CR03 70.0, CR07 77.8 and CR09 28.6, so most regions differ. The text says "replacements its collectors made" and "latest decision" for each, which favours the event reading. It does not touch the outcomes or the credit.
  - Duplicate re-uploads read as late recording would move 5 outlet-months to late (T4496, T5280, T6431, T9801 in July; T3846 in August). The visit log's prices_entered equal the unique quote counts, which settles it.
- **Cross-batch check.** No access to prior batches inside the allowed folder. Not assessed.

## Residual risks
- **R1 (Gate C/E, not failed).** No shipped sentence says the re-collection lag must be corrected, or how. A literal reader who takes 3.2 and 3.3 as "compare the back-check price with the collector price" gets the raw column above: 4 service credits and USD 7,049. The estimand in 3.1 ("at the time the collector recorded it"), the Re-collected on column and the lag-dependent excess in the data force the correction, and the golden's bands are robust to every estimator variant I tried. I judge it forced, but it is the single point where a weaker-minded reader could split on method rather than on analysis. If the author wants it nailed, the pin must file the WHAT, for example that accuracy is of the price at collection, never the HOW.
- **R2 (solution blocks).** SOLUTION_STEPS step 8 does not mention removing the 3 duplicate replacement rows (201 raw rows against 198 events). A solver who skips this changes some replacement percentages. The golden figures are correct. Add the dedupe to the step. FIX_NOW class, no rerun.

## Files/Hygiene
PASS. 14 files in 3 formats (csv x 7, xlsx x 5, pdf x 2; the quotes csv has 56,578 rows). Roster, indices, item list, return and the outlet register act as distractors; the Tallis return is a contractor self-report that does not feed the answer. The register layouts change across the three back-check sheets (date text against date type, column order differs in September) and the status codes change on 3 August. These are Layer 1 mess and are real-system looking. No authoring or benchmark language found. Temporal coherence holds (register dated 2026-10, return submitted 9 Oct, decisions to 1 Oct). Licence and source records are not in the folder I could read, so I did not assess them. No exclusion-level finding.

## Stump power (Gate F)
Moderate to good. The easy route is raw agreement (seven compliant regions pushed to corrective action, three corrective ones to credits, USD 7,049). A strong model must see that Halbrook re-collections are about 1 day after the visit and the rest about 5, so raw agreement penalises the remote regions, and then build the exposure from the quote series. The asks add several multi-source reconstructions (takeover mapping, calendar window with the holiday, status code switch, deduplication, decision-to-replacement dating). The exact timeliness and replacement figures should fail many runs by themselves. No too-easy signal: nothing in the files documents the drift.

## Stumping type (Gate G)
`mechanism: statistical_rigor` (measurement-bias correction, with etl_conformance in the asks), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported accuracy is shipped to be rejected; the stump is estimating the filed estimand from back-checks taken at different lags. The lag is a feature of the back-check procedure, not a corrupted value. Gate G passes.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: official-statistics field quality assurance, estimating measurement error from re-collection back-checks; the swap test fails to change the reading, because the deciding quantity is a drift-corrected accuracy estimate. Layer 1: takeover outlet numbering, status-code change on 3 August, duplicate uploads, sheet layout changes, holiday-shifted window. Layer 2: lag-exposure correction of back-check agreement. Decisive step: a strong analyst who cleans everything and reads every rule right still files the raw agreement (4 service credits, USD 7,049), the wrong answer; so H3 passes as analytical, though see R1.

## Fix
none required. Optional: (a) solution, add the duplicate-row removal to step 8 (R2); (b) a WHAT-only pin for R1 if the author wants to close it.
