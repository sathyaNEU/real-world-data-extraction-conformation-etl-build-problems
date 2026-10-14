# Verdict, task137 round 2

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed; no rerun.

**Why:** The booking is forced by the shipped procedure (6.1: forecast hours for the list, nearest 250), SOW schedule 2 (1.5 / 8 / 22 minutes) and the seven closed campaigns. Every rigorous variant of the forecast I built lands in 5,192 to 5,281 hours, so all round to 5,250. The monthly split is 1,250 / 2,000 / 2,000 under every rigorous variant. The deliverable figures (supplementary asks 3 and 4) each follow one reading of the filed text and all reproduce exactly.

## Evidence (recomputed from target/, all reproduced)

| Item | Result | Source |
|---|---|---|
| Listed deposits with no callable number | 464 (reproduced). If withdrawn DNC entries are ignored it is 514, a minor fork with about 15 hours of effect, no change to the rounding | kbs_contact_points, kbs_do_not_call_register, list2027Q1 |
| Release rate | 56,638 / (56,638 + 2,837 INSTRUCTED) = 95.2% | kbs_case_release_log |
| Non-reaching dials / conversations on the list | 66,714 / 13,962 (golden about 66,700 / 14,000) | release log + close-outs + dial log, mix by M/H/W counts |
| Past retention-offer share | 9,726 / 46,298 = 21.0% | dial log |
| Special class (rate at least 0.40 above the same list, term and quarter minimum; prem is 0.25 or less, or 0.50 and 0.60, so any cut in 0.25 to 0.50 gives the same class) | 4,093 conversations, 87.4% retention offer, flat 86 to 89% across drop bands | lists 2025/2026, briefs |
| List specials | 10,697 at 5.65% vs 5.15% base, drop 1.65 against the 4.00% 4-year rate in the 2027Q1 brief | list2027Q1 |
| Others at drop 1.50 to 1.75 | 27.7% | |
| Hours, golden method | 5,280.9 total; Jan 1,206.9, Feb 2,013.3, Mar 2,060.7 (exact match) | |
| Share of the list's conversations to the offer | 53.8% (golden "about 54") | |
| Retained principal / deposits per campaign | 497,825,279 / 6,700; 537,491,208 / 7,186; 532,430,083 / 7,226; 536,001,671 / 7,172; 562,095,944 / 7,591; 557,067,295 / 7,494; 573,831,183 / 7,765. All match the golden after rounding. | events + transfers |
| Quarter maturities | Jan 415,506,232; Feb 646,815,868; Mar 672,944,034; not on list 214,491,217. All match, with margin from rounding edges. | holdings (joint accounts deduplicated), KIP register, migration batches |

Retention logic checks: every listed deposit has a MATURE event on its maturity date; REINVEST amount equals MATURE amount in all 41,225 cases; BREAK events fall 3 to 24 days after maturity, so the 30-day window edge (inclusive or exclusive) is immaterial. Maturity-settlement transfers run only from settlement account 8604109000017099, and they land in accounts the events extract shows opened that day, or in other-bank accounts. Dial behaviour shows no January or close-down effect (nr per case about 3.9 to 4.1 in every month), so no calendar adjustment is needed.

**Competing answers and forks tested**

| Reading | Hours | Rounded |
|---|---|---|
| Golden: special class by drop band, others by band | 5,281 | 5,250 |
| Specials flat 87.4%, others by band | 5,264 | 5,250 |
| Specials flat, others by exact drop | 5,249 | 5,250 |
| Others set to zero | 5,192 | 5,250 |
| Pooled per-case dials, no number-type mix | 5,271 | 5,250 |
| Special / other class only (others pooled at 14.6%, which ignores that negative-drop deposits do not convert) | 5,389 | 5,500 |
| Skip the INSTRUCTED withdrawal haircut | 5,535 | 5,500 |
| Treat all 18,400 as callable | 5,406 | 5,500 |
| Pooled 21% | 4,214 | 4,250 |
| Latest campaign 22% | 4,247 | 4,250 |
| Drop band only | 4,267 | 4,250 |
| Locked rate band | 4,230 to 4,280 | 4,250 |
| By term | 3,822 | 3,750 |

The last four rows are the intended wrong paths. The two 5,500 rows that skip the haircut or treat all 18,400 as callable come from ignoring procedure 4.2 and 4.3, which is solver error and not a fork. The class-only 5,500 row is a weak model of the same insight. The margin to the 5,375 rounding edge is 94 hours (1.8%) and to 5,125 it is 156 hours. Sampling noise of the special share is about 10 hours.

Prompt and files closure: the estimand is pinned by procedure 6.1, SOW schedule 2 and the prompt ("hours for the deposits maturing in each of the three months", rounding to 250). The newsvendor argument for a lower or higher block is not licensed, because 6.1 says "forecast to need". Staffing proposal (66.10 rate, 9,000 hours capacity, 750 minimum block), the treasury workbook (maturities 870 / 892 / 787 million, all wholesale plus member funding; 82% reinvest) and the eml are non-decisive and appear in no committed answer. One open point: the filed text does not define a "special"; the class is recovered from the lists and its boundary sits in a clean gap (0.25 to 0.50), so the data separate it.

**Files/Hygiene:** PASS. 27 files; formats pdf, csv, docx, xlsx, eml, txt; main files are 269k, 157k, 61k, 57k rows. The files read like system artifacts: mixed phone formats, DD/MM/YYYY vs ISO core layouts, dashed vs 16-digit accounts, UTC dial times, joint-account duplicate rows, DEFERRED then MIGRATED batches. No authoring or benchmark language found in the extract notes, eml, SOW, procedure or briefs. Dates cohere (2 Nov 2026 is a Monday; 17 and 20 Nov 2026 weekdays correct; events end 31 Oct, enough for 30 days after the 30 Sept maturities). No public-data contamination (fictional society and contractor). Minor, not exclusion-level: the 2027Q1 brief is labelled "(draft)" while the rates are "approved by ALCO", which does not alter the answer. I did not review the shipped goldens for realism, and I did not run the cross-batch reference check (outside the readable directory).

**Stump power:** HIGH on the main call. The pooled / latest / trend / drop-only / locked-rate / term paths all give 3,750 to 4,500 hours against 5,250, because 58% of the list is one low-drop special tranche (4-year, 5.65%) that behaves at 87% and not at the drop-curve share (35%). Careful solvers must also keep the release-rate haircut and the DNC wash right (misses push to 5,500). The asks add independent multi-row stumps: retention via transfers into new same-day TD accounts with the BREAK/CLOSE rule (REINVEST-only gives lower figures), joint-account dedup in holdings and KIP-core key matching (naive sums overstate by about 277 million).

**Stumping type:** `mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The numbers are fine; the difficulty is a composition shift in the forecast population whose past behaviour is separable by class, not a flipped reported number. On perfectly clean data it still stumps pooled or drop-only fits. It passes Gate G.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. The field's own analysis is forecasting of rate-shock retention conversion (drop from locked rate to reinvestment rate, promotional money) turned into contact-centre workload. Layer 1 is the phone and DNC conformance, 2025 and 2026 core layouts, account formats and batch dedup. Layer 2 is the heterogeneous-segment forecast. The easy route is to pool or fit a drop curve, giving 4,250 hours instead of 5,250.

**Fix:** none. Optional editorial: none required to the prompt, solution or files.

## Disposition

Approved as judged (judge-task137r2, the round 2 pack). No pack file, golden, write-up, prompt or graded figure
changed after the verdict; the final rebuild's 27 files under `target/` are byte-identical to the copy the judge read,
and `target.zip` is unchanged (sha256 e9d6e93637fe658acbc03425898c8a8d79a6b3e4c47d36238c0cb3c4c655d5c9). Round 1's
reports (`determinism_check_report.md`, `determinism_check_report_pass2.md`) stay as history of the round 1 pack.

1. **The draft label (the judge's minor point).** Left as it stands. The 2027Q1 brief is the society's working document
   to Harbourline for a quarter not yet released (issued 3 November 2026, cases released from 11 December), so it
   stays in draft while its other sections can still move; its rate table is the society's card "as approved by ALCO"
   in its own words. Both phrases are asserted under SF6, every route reads the same card, and no answer turns on the
   label. Recorded in the design note's Build record.
2. **The withdrawn registrations.** 464 listed deposits with no callable number reads the register as it stood at the
   cut (SF5); the reading that ignores withdrawals gives 514 and about 15 hours, inside the 5,250 bin. No change.
3. **The about-5,500 routes.** Skipping the instructed withdrawals (5,535) or treating all 18,400 as callable (5,406)
   ignores procedure 4.2 and 4.3 (SF10, SF11), solver error and not a fork, as the judge rules; the class-only route
   that pools member money across drops (5,389) is a weaker model of the same step. Margins 94 hours to 5,375 and 156
   to 5,125. No change.
4. **The leak reader's readings**, each with its fork row: per-month against total rounding SF13; Ask A's reinvestment
   into a new account SF20; a partial renewal and the part-retained count SF18; a transfer to a joint or related
   member's account SF20; Ask B's migrated-certificate double count SF23; "not on the list" SF24. Two of them were
   closed by text and data but not asserted; two assertions were added to `generator/checks.py` (every REINVEST equals
   its MATURE amount, so no part is renewed on the deposit's own account; every payment of a listed deposit's principal
   into a term deposit goes to the deposit's own holder). The judge's reproducing rule for Ask A (transfers into term
   deposits opened that day, with the BREAK or CLOSE check over 30 days) is the golden's.
5. **Free gates on the final rebuild:** `checks.py` 606 assertions; `verify.py` 34 checks from the bundle alone; two
   builds byte-identical (target, goldens, `metadata.json`, `figures.json`, `target.zip`); `figures_check.py` exit 0
   (111 figures); `precut.py` exit 0 (49 checks); `voice-check.py` PASS; `leak.py --asof 2026-11-04` REVIEW, no LEAK,
   every line answered in the design note; container audit clean on target and golden; `guard.py surface` exit 0,
   `heart` WARN (`repeat.gate_g` only, answered under Guard), `validate` clean.
