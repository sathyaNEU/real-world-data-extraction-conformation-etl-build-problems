# determinism-check report, task445, 2026-10-12 (pass 3)

One isolated judge thread (Sonnet, medium) on a fresh unzip of `target.zip` under
`/tmp/determinism-check-task445-20261012T024423Z/`, with the judge system prompt inlined verbatim and the submission's
blocks; it read nothing outside that folder. The thread's verdict follows, then the spec gates and the Gate G and H
reconciliation done in the main session after it returned.

## Thread verdict

**Verdict:** NOT_DETERMINISTIC (failure type: competing_defensible_answer, on the bridge PNG's reconciling bars; the main recommendation itself is forced). The solution blocks also carry one SOLUTION_WRONG cell (GLI December ownership).

**Disposition:** SEND_BACK, ask layer only. The prompt has to say how the overlapping reconciling items are netted (put and call lines first, then reports replaced by a later amendment, or the reverse). The GLI cell needs regenerating at 84.5. The main call, the ladder and the 12 flags can stay frozen. A fresh solver round on the asks is required, because the prompt changes.

## Why
- **Main call: forced.** Run literally (cover-page period, OM-4 s.2 estimate by back-test, s.4 CUSIP rule, s.5 share counts, s.7 line at 80.0), WHII, GLI, OTF, JEMS and SAF are Y and the other seven are N. Every basis that back-tests within 0.1 point returns that same flag string (1,000 bases in the family I searched). The decisive back-test margin is clean: 0.04 points against 0.19 for the next distinct basis and 0.66 for the pooled-by-type basis. OTF (80.40) is the only name whose flag depends on the basis chosen.
- **Bridge, ask 1: not forced.** The put/call bar and the replaced-by-amendment bar overlap by 435,800 shares, which are put/call lines sitting inside the replaced reports. The prompt says only "one bar for each item between the two totals" and never fixes the netting order.
  - Golden order (put/call first, then replaced non-put/call lines): -8,193,500 and -50,329,283.
  - Equally natural reverse order (replaced reports first, then remaining put/call lines): -50,765,083 and -7,757,700.
  - Both orders tie out to 547,342,330, so a literal reader cannot choose between them. Each bar is graded to the whole share.
- **Bridge, ask 3: a second, smaller fork.** The "+6,508,236 matched back" bar can be split into three items by what the filer did wrong: zero-stripped CUSIPs (+3,931,423), lowercase CUSIPs (+1,000,187) and failed check digits matched on name (+1,576,626). "One bar for each item" admits 3 or 5 bars.
- **GLI December ownership.** The golden says 84.4%. The golden's own step 6 (index/ETF sponsors per name, every other type pooled) gives 84.4523, which rounds to 84.5. All 125 exact-argmin bases give 84.4529. Only the worse-backtesting carry-others variant (miss 0.0413 vs 0.0402) gives 84.43. The flag is unaffected.

## Evidence: recomputation ledger
| Figure | Claimed | Recomputed | Reproduced |
|---|---|---|---|
| Managers with a Sep holdings or combination report and no Dec filing by 3 Feb | 129 | 129 (395 Sep reporters, 272 Dec holdings filers, 0 overlap with the 8 Dec notices) | yes |
| Index/ETF sponsors' OTF change Sep to Dec (2 filed, 5 due) | +10.4% | +10.37% | yes |
| Pooled sponsor change across the 12 names | +4.5% | +4.46% | yes |
| Back-test miss: golden basis / pooled by type / carry at June | 0.04 / 0.66 / 1.38 | 0.041 / 0.661 / 1.379 (cut 3 Nov 2022; same for cuts 2 to 4 Nov) | yes |
| Dec ownership WHII, GLI, OTF, AMRB, TAAV, JEMS, FENN, ABBB, OLPD, SAF, HAMR, NOPR | 88.6, 84.4, 80.4, 76.2, 74.3, 84.8, 79.6, 62.3, 71.1, 91.4, 55.2, 67.2 | 88.607, **84.452**, 80.398, 76.192, 74.308, 84.808, 79.591, 62.310, 71.098, 91.403, 55.207, 67.193 | all yes except GLI (84.5) |
| Sep ownership (the prior column) | 85.1, 81.7, 78.8, 74.1, 75.4, 81.8, 81.6, 59.8, 69.7, 88.9, 52.5, 65.5 | 85.11, 81.69, 78.81, 74.09, 75.41, 81.79, 81.61, 59.79, 69.71, 88.91, 52.475, 65.49 | yes (under cover-page keying and AMENDMENTNO order) |
| OTF under comparison bases | 79.2 pooled by type; under the line carried | 79.16; 78.22 carried | yes |
| FENN over the line when every due manager moves with the name | over | 80.36 | yes |
| Bridge, as written | 599,356,877 | 599,356,877 | yes |
| Bridge, put and call | -8,193,500 | -8,193,500 (put/call first) | yes, order-dependent |
| Bridge, replaced by amendment | -50,329,283 | -50,329,283 (after put/call; 50,765,083 if taken first) | yes, order-dependent |
| Bridge, matched back | +6,508,236 | +6,508,236 | yes |
| Bridge end total | 547,342,330 | 547,342,330 | yes |
| Title gap | 52.0 million | 52,014,547 | yes |

Dec flags are identical under cover-page or header keying and under AMENDMENTNO or accession order. Only the Sep column and the bridge move: Sep WHII is 85.1 under the golden keying and 85.8 to 86.6 under the others.

**Fork table (Gate C):**
| Fork | Golden | Alternative | Moves a flag? | Moves a graded figure? |
|---|---|---|---|---|
| Bridge netting order | put/call first | replaced first | no | yes, 2 bars |
| Bridge matched-back split | one bar | three bars | no | yes, bar count |
| Period key for the amendment 0000950123-22-001007 | cover page (the readme's "quarter ended") | SUBMISSION header (June) | no | yes, Sep column and bridge totals |
| Same-day amendment order | AMENDMENTNO | accession | no | yes, Sep column |
| GLI December rounding | 84.4 | 84.5 | no | yes, one cell |

The last two forks are closed in the golden's favour by the files. The readme's "quarter ended" wording and the restatement's 183 lines (against 178 in June) fit the cover page. AMENDMENTNO is the only meaningful sequence. I count them as minor.

**Gate B:** every decisive fact is shipped. OM-4 s.2, s.4, s.5 and s.7 give the rules. COVERPAGE and SUBMISSION give the report types and dates. fsds supplies the share counts. manager_register.csv supplies the manager_type that makes the index-sponsor basis discoverable.

**Gate C on the main call:** the estimation basis is not enumerated in OM-4 ("the basis that comes closest"). Within every family I could back-test with the shipped June, September and December data, the closest basis is flag-unique. A solver who tries only carry, pooled or share-count bases (miss 0.66 or more) files OTF as N, which is the intended trap. No family I tested overturns the golden flags.

## Files/Hygiene: PASS
- 19 shipped files: 9 TSV in 3 data folders, 2 fsds txt, 2 csv, 1 xlsx, 1 pdf, 1 htm, 2 md, 1 txt.
- Formats: tsv, csv, xlsx, pdf, htm, md, txt (7).
- INFOTABLE files hold 37,870 lines (q3 drop), 39,440 (q4 drop) and 33,901 (daily build), above the 25,000-row floor.
- Distractors: short_interest_20221230.csv, 13flist2022q4.txt, the manager_register `family` column, and the OM-4 s.6 value basis.
- Provenance and fiction are coherent: an in-fiction research shop with fictional issuers and managers on the real 13F layout. No authoring leak found. Dates are coherent (flag file due 8 Feb, filings to 2 Feb, fsds 10-Ks accepted 1 and 2 Feb with as-of dates after year end correctly excluded).
- No public-data contamination: the issuers and managers are fictional. Not exclusion-level.
- Cross-batch fingerprint check was not run, because no corpus is shipped in the allowed universe.

## Stump power
Moderate to good. The easy routes are the December reports alone (OTF 54.0), June or September carry-forward (OTF 78.2), a pooled change per register type (OTF 79.2), or moving every due manager with the share count (FENN flips to Y). Each files four flags and drops OTF, or adds FENN. Only a back-test that stratifies sponsors by name wins, so a strong model that backtests only two or three bases is plausibly stumped.

## Stumping type
mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no.

The honest numbers are all correct. The difficulty is choosing the estimate basis by OM-4's own out-of-sample criterion. This is not a banned scaffold.

## Three rules
domain: pass, layers: pass (Layer 1: cover versus header period, amendments, off-format CUSIPs, put/call, 129 missing managers. Layer 2: back-tested nowcast of unreported holdings), decisive_step: analytical.

Swap test: put "hospital" in for "13F manager" and the OM-4 back-test no longer makes sense, so the domain is not a backdrop. The easy route, carrying or pooling by type, files OTF at 79.2 or lower and gives four flags.

## Fix
- **prompt:** state the bridge netting order ("take out put and call lines first, then lines in reports replaced by a later amendment, then add back off-format CUSIPs") and fix the bar list, either the three items as filed or the sub-split. The prompt is currently 934 characters.
- **solution:** regenerate crowded_flags GLI inst_own_pct to 84.5, and in the blocks change "GLI 84.4%" to 84.5%. State the argmin basis (index/ETF sponsors by name, other types pooled) exactly.
- No input file needs to change. The flags and the 129 stay frozen.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 19 | yes |
| Formats | 3 or more | 7 (csv, htm, md, pdf, tsv, txt, xlsx) | yes |
| Large file | 25,000 rows | `form13f_2022q4/INFOTABLE.tsv` 39,439 rows | yes |
| Distractors | 2 or more in `metadata.json`, none named in a file name | `short_interest_20221230.csv`, `13flist2022q4.txt` | yes |
| Deliverables | 1 to 3, all in the golden | `crowded_flags_2022q4.csv`, `sep_quarter_bridge.png` | yes |
| Asks | multi-dimensional, unit and rounding stated | September ownership per name (12), the bridge (5 bars); rounding at the close | yes |
| Shape and criteria | identifiable shape, 25 or more criteria | shape 03 inside a twelve-row flag file; about 40 criteria | yes |
| Realism | nothing LLM-generated | the reader's notes are the constructed world and the ask devices | yes |

## Gate G reconciliation

The thread's mechanism (`method_or_model_selection`), family (`analytical_non_defect`), `surface_read_dependency: no` and
`sole_data_defect: no` match the card (`gate_g: method_or_model_selection`) and the design note's Gate G section. It named
no distractor as carrying the task.

## Gate H reconciliation

domain pass, layers pass, decisive_step analytical: matches the card (`stump_class: analytical`, `analyst_test`,
`domain_test`).

## Disposition taken

The thread wrote SEND_BACK scoped to the ask layer: the main call forced (every basis it found within 0.1 point of the
best back-test files the golden's flags), and its fix list touches only the bridge wording and one golden cell. Treated as a
one-pass repair under build-pipeline stage 4, re-judged once:
- the prompt's bridge sentence names the three bars and their order (SF15);
- GLI's December target moved from 84.43 to 84.39 (HAMR's from 55.20 to 55.22 to hold its September slack mid-bin), so the
  near-argmin family under both peer readings files GLI 84.384 to 84.414 and every name in one bin (SF14, asserted);
- the main-call snapshot re-taken, every gate re-run green (27,281 checks, verifier, byte-identical rebuild, figures_check,
  precut, leak.py, surface).
