# determinism-check report, task445, 2026-10-12 (pass 4)

The one re-judge after pass 3's repair. One isolated judge thread (Sonnet, medium) on a fresh unzip of `target.zip` under
`/tmp/determinism-check-task445-20261012T032245Z/`, with the judge system prompt inlined verbatim and the repaired
submission's blocks; it read nothing outside that folder. The thread's verdict follows, then the spec gates and the Gate G and
H reconciliation done in the main session after it returned.

## Thread verdict

**Verdict:** DETERMINISTIC (SOLUTION_WRONG on one supplementary item: sep_quarter_bridge.png "ask 2" asks for a title the prompt never requests).

**Disposition:** FIX_NOW. The main call, the CSV and the three bridge bars reproduce exactly. The repair is solution-side: drop or re-word "ask 2" (the title) because the prompt never asks for one. Optionally align the SUBMISSION period of accession 0000950123-22-001007 with its cover page (see Evidence, fork 1). Neither repair moves a flag, so no solver rerun is needed.

**Why:** OM-4 s.2 files the estimate, and its basis rule: the basis that, applied to the previous period with only the reports filed the same number of days after period end, comes closest to the later complete period, measured by the largest difference across the 12 securities. Run on the September window (3 Nov 2022, 34 days, the same lag as 3 Feb 2023), that rule picks one basis uniquely: per-name peer change for Index and ETF sponsors, with the other types flat or pooled (largest miss 0.040 points). The next distinct flag pattern needs a basis scoring 0.30 or worse. The plain "one pooled change per register type" basis scores 0.66 and files OTF at 79.2, which is the wrong-but-natural answer. Every committed answer except the unpinned title reproduces from the shipped files.

## Evidence

Literal reading first. The flag file goes out 8 Feb 2023. The Form 13F readme says filings are due within 45 days of quarter end, which is 14 Feb. So it is issued before the deadline, and OM-4 s.2 requires estimating the reports not yet filed. Data in hand runs to 2 Feb filings and 3 Feb acceptances. I executed OM-4 as written:
- Report period comes from COVERPAGE.REPORTCALENDARORQUARTER (the readme calls it "Report for the calendar year or quarter ended").
- Amendments are applied in filing order, then AMENDMENTNO. A RESTATEMENT replaces the whole report. A NEW HOLDINGS amendment adds to it.
- Lines are SH only. PUTCALL is blank, and the title of class is not CALL or PUT.
- CUSIPs are upper-cased and leading zeros restored (8 lines).
- A failed check digit is matched on issuer name where exactly one covered security fits (8 lines, all unique against 13flist2022q4.txt).
- Shares outstanding are the latest EntityCommonStockSharesOutstanding as-of date on or before period end, across 10-Q, 10-Q/A and 10-K. This picks the 10-Q/A values for HAMR, TAAV and OLPD in September. The AMRB 10-K as-of date of 30 Jan 2023 is excluded.
- The managers who report December are the 272 December filers plus every September holdings or combination filer with no December filing or notice. There are 129 of them.

Recomputation ledger:

| Figure | Claimed | Recomputed | Reproduced |
|---|---|---|---|
| Managers with Sept holdings or combination report, no Dec filing by 3 Feb | 129 | 129 (no Dec notices among them) | yes |
| Index/ETF sponsors due | n/a | 5 of 7; 2 filed both periods | yes |
| Sponsor peers' OTF change Sept to Dec | 10.4% | 1.1040 | yes |
| Sponsor change pooled across the 12 names | 4.5% | 1.0446 | yes |
| Back-test, golden basis, Sept window | 0.04 | 0.0402 | yes |
| Back-test, one change per type pooled | 0.66 | 0.6606 | yes |
| Back-test, each due manager carried at June | 1.38 | 1.3785 | yes |
| Dec WHII / GLI / OTF / AMRB / TAAV / JEMS | 88.6 / 84.4 / 80.4 / 76.2 / 74.3 / 84.8 | 88.602 / 84.384 / 80.397 / 76.189 / 74.308 / 84.803 | yes |
| Dec FENN / ABBB / OLPD / SAF / HAMR / NOPR | 79.6 / 62.3 / 71.1 / 91.4 / 55.2 / 67.2 | 79.591 / 62.310 / 71.091 / 91.403 / 55.225 / 67.188 | yes |
| Flags | Y: WHII, GLI, OTF, JEMS, SAF | same | yes |
| Sept WHII / GLI / OTF / AMRB / TAAV / JEMS | 85.1 / 81.7 / 78.8 / 74.1 / 75.4 / 81.8 | 85.110 / 81.69 / 78.81 / 74.09 / 75.41 / 81.79 | yes |
| Sept FENN / ABBB / OLPD / SAF / HAMR / NOPR | 81.6 / 59.8 / 69.7 / 88.9 / 52.5 / 65.5 | 81.61 / 59.79 / 69.71 / 88.91 / 52.479 / 65.49 | yes |
| Bridge: lines as filed (exact CUSIP, all lines) | 599,363,366 | 599,363,366 | yes |
| Bridge: put and call lines | -8,193,500 | -8,193,500 | yes |
| Bridge: other lines in replaced reports | -50,329,359 | -50,329,359 | yes |
| Bridge: matched back | +6,508,236 | +6,508,236 (4,931,610 malformed, 1,576,626 check-digit failures) | yes |
| Bridge: Sept institutional shares | 547,348,743 | 547,348,743 (equals the Sept numerator behind the ownership column) | yes |
| Bridge title gap | 52.0 million | 52,014,623 | yes, but not asked by the prompt |
| OTF under pooled type change | 79.2% | 79.18 | yes |
| FENN over line under a share-count basis (mixed combo, back-test 0.30) | claimed over | FENN 80.32 | yes |

Basis search. Per manager type, I tested six modes: carry, share-count move, type change pooled, type change per name, every filer's change pooled, every filer's change per name. That is 6^5 = 7,776 combinations, with peers read as "filed both periods" and as "every filer of the current period" (the Dec-side readings are identical on every flag).
- The best score is 0.0402. All six combinations at that score, and all 30 best-ranked bases up to 0.041, give YYYNNYNNNYNN (WHII, GLI, OTF, JEMS, SAF), with OTF 80.40 and FENN 79.59. They differ only in how the Long-only, Pension and RIA types are treated, which does not move the flags.
- Other flag patterns first appear at 0.30 (YYNNNYYNNYNN: OTF 79.3, FENN 80.3), 0.41 (YYYNNYYNNYNN) and 0.59 (YYNNNYNNNYNN).
- Moving the September window from 2 Nov to 14 Nov keeps the same winning pattern. The gap to the next pattern is wide.

Residual forks, none of which moves a flag:
1. Accession 0000950123-22-001007 (Selwood Savings, restatement) carries cover period 30-SEP-2022 but SUBMISSION.PERIODOFREPORT 30-JUN-2022. Its figures also look like June numbers. The prompt wording ("reports for the quarter ended 30 September") and the readme's COVERPAGE definition favour the cover page, which the golden uses. A solver who keys on SUBMISSION would file Sept ownership 0.3 to 0.6 points higher (WHII 85.8, OTF 79.4, FENN 82.2) and a different bridge. The Dec flags are unchanged under that reading (best basis still 0.040, same flags). This is a supplementary-column and bridge risk only.
2. The 129 includes 3 managers whose holdings reports have no information-table lines (CIKs 1396742, 1589543 and 1273775). The literal rule counts them, and it does not affect any ownership figure.
3. The Elmstead NEW HOLDINGS amendment filed 17 Jan 2023 changes no watchlist figure.
4. Percentages are not near a rounding edge. OTF at 80.397 against the 80.0 line is a clean gap that holds across every basis scoring under 0.2.

Defect, bridge "ask 2": the SUPPLEMENTARY_ANSWERS list a title ("our September institutional shares sit 52.0 million shares below the straight sum of the SEC lines"), and the prompt asks for no title. Under Gate E this is an answer the prompt does not pin. The figure itself is derivable, so the repair is solution-side.

## Files/Hygiene

**PASS.** 19 files in 7 formats (tsv, csv, txt, htm, md, xlsx, pdf). The largest information table has 39,440 rows and the three drops hold about 111,000 lines.
- Two distractors: short_interest_20221230.csv and the manager_register family and inactive fields.
- Realistic mess: leading zeros dropped, lower-case and malformed CUSIPs, a 10-Q/A, restatements and a mis-dated amendment, the dollar and thousand basis change at 3 Jan 2023, and a trimmed 13(f) list.
- The company names are fictional, but the SEC layouts are faithful. data_sources.md is a habit-style file but contains no authoring disclosure.
- Mild tell: accession sequence numbers such as -22-000748 are too small for real filer-agent numbers.
- No exclusion-level finding.

## Stump power

Adequate. The tempting route is a single pooled change per register type, which a careful solver arrives at (back-test miss 0.66). It files OTF at 79.2 and gives 4 flags where the golden has 5. The in-hand-only route (OTF 54.0) and carry-forward route (OTF 78.2, miss 1.38) are visibly worse. A strong solver must run the OM-4 criterion and let sponsors take a name-specific change from only two filed peers. The stump is not decoded from an annotated rule. It comes from running the stated closeness criterion.

## Stumping type

`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`

The reported 13F figures are all fine. The difficulty is choosing the estimator by out-of-sample back-test. Clean data would still stump. Passes Gate G.

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`

Layer 1 is mixed-vintage SEC drops, amendments, malformed CUSIPs and a share-count vintage. Layer 2 is back-test selection of the estimation basis for managers not yet filed. The swap test passes: 13F filing rules, register types and a back-tested estimation basis for unfiled managers do not survive another field's nouns. The easy route is one pooled change per type: OTF 79.2, 4 flags (misses OTF). Gate H passes.

## Fix

solution: remove or re-word "ask 2" (the title), since the prompt asks for no title. Optional input_files: in SUBMISSION.tsv set PERIODOFREPORT for 0000950123-22-001007 to 30-SEP-2022 so the cover and submission tables agree. That edit touches the prior column and the bridge only, not the call.

## Spec gates

Unchanged from pass 3 and all pass: 19 files, 7 formats, `form13f_2022q4/INFOTABLE.tsv` 39,439 rows, two distractors named
only in `metadata.json`, two deliverables both in the golden, asks multi-dimensional with rounding stated, shape 03, about 40
criteria, no LLM-shaped file.

## Gate G and Gate H reconciliation

The thread's mechanism (`method_or_model_selection`), family (`analytical_non_defect`), `surface_read_dependency: no`,
`sole_data_defect: no` and its Three rules line (domain pass, layers pass, decisive_step analytical) match the card and the design
note. It named no distractor as carrying the task.

## Disposition taken

FIX_NOW, write-up only: block 4's bridge title line removed (the prompt asks for no title; the chart keeps its title as
presentation). The optional input change (the restatement's SUBMISSION period set to 30 September) is declined: the header and
cover-page disagreement is Ask A and Ask B's designed device DV-2, which the thread itself finds closed in the golden's favour by
the prompt's wording and the readme. Its mild tell (low accession sequence numbers) is recorded as a realism debt. No figure, file
or flag moved, so no further pass runs.
