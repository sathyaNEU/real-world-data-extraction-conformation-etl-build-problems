# Determinism check report, task196 architecture 2, pass 1

**Verdict NOT_DETERMINISTIC, judge's disposition SEND_BACK, overridden by the author to FIX_NOW**, on the
19-member bundle whose zip md5 was 72c2b367aa54077806c3183825940d2b.

**The override and its reason.** An architecture is spent when the decisive step cannot be saved, and the
mark of that is when the only way to close the fork is to file the HOW. Every fork below closes by fixing
data or by making a wrong sentence right: the prompt's "our data stops at 31 March 2027" against extracts
running to 30 June, a designed cluster of registrations 1 to 5 days before the request that makes a second
attribution reading defensible, 33 pre-payment registrations, an overlap of 120 narrow enough that one
legitimate estimator form crosses the rounding boundary, and a golden ask-6 total that does not match its
own rows. None of them is the estimator or the attribution rule. Gate F is moderate with the trap working,
Gate G passes, Gate H passes with the decisive step analytical, and the isolated reader filed 23 against
the golden's 31 by the default path.

**The condition, and it is hard.** If the re-judge after this pass is not APPROVE, the architecture is
spent and the slot re-roots, with no second override.

# Task 196 determinism review

Note on method: the brief file inlines the graded blocks, so I had seen them when I opened it. The enumeration below was nonetheless built from the bundle only, and compared with the golden afterwards. Brief path says `target/`; the pack is actually the flat dir `task196_judge_pack/` (19 files, no `target/` subfolder). All recomputation is from those files.

## Pre-reading enumeration (answer the prompt and bundle lead to)

Index = scam cases arising from Castlegate customers' payments in scheme year to 31 Mar 2027 (standard v6 4.2), recorded or not, per million payments sent on the revised returns.
Denominator: revised 2026/27 sum, KM-104 = 22,301,200 (preliminary sheet differs by 6,258 in Q4 only, no rounding effect).
Numerator candidates for Castlegate (A = own register scam cases, payment date in 2026/27 = 400; 412 payments match the scheme register, 325 of them carry an own case ref; 87 do not):

| Reading | Cases | Index | Rounded |
|---|---|---|---|
| Plan on own register | 400 | 17.94 | 18 |
| Two-source (Lincoln-Petersen) on all 412 matches | 507.1 | 22.74 | 23 |
| Two-source with registrations a prior own fund-return request produced removed from the register list (205 out): 400 x 207/120 (golden) | 690.0 | 30.94 | 31 |
| Same, Chapman form | 688.3 | 30.86 | 31 |
| Capture probability taken only from own cases no request was sent on (34/109), non-register sightings 87 scaled by it | 678.9 | 30.44 | 30 |
| Golden rule but evidence cut at 31 Mar 2027 (A by notified date, matches by registered date, requests by sent date) | 581.7 | 26.08 | 26 |
| Golden but also drop sightings registered before the payment date (33, all in A) | 800 | 35.9 | 36 |
| Golden but request attribution allows registration 1-2 days before the request (cluster, see below) | 795.5 | 35.7 | 36 |

My own first answer from the bundle: 31 (the request-attribution adjustment is the evident analytic move). I could not stop at 31 as forced, see Gate C.

## Verdict: NOT_DETERMINISTIC

## Disposition: SEND_BACK
The estimand needs the evidence window, the attribution rule for own-request registrations and the estimator form filed in the prompt (what, not how), and ask 6 needs its population and totals pinned; that changes what solvers see, so a rerun is required.

## Gate table

| Gate | Result | Line |
|---|---|---|
| A | PASS for main figures, FAIL on ask 6 route totals | 400, 412, 205, 207, 120, 290, 690, 22,301,200 all reproduce; other members' 22 / 15 / 12 reproduce. Ask 6 "route totals" (7.9/5.4/2.3) are not the totals of the quarter rows (see below). |
| B | PASS | Every decisive fact is in the files (standard 4.2, returns, register, matches, requests). Method (two-source) is not in any file but method vagueness is permitted. |
| C | FAIL | Main call is not closed against several defensible conventions (30, 26, 36); ask 6 has unpinned population/source/totals. |
| D | PASS with risk | Splits would trace to unpinned conventions (window, attribution rule), not to the data, which is a Gate C/E issue rather than a semantic stump. |
| E | FAIL (partial) | Prompt says "our data stops at 31 March 2027" while files carry rows to 30 June 2027; ask 6 never says case-year, closing-date basis, ledger vs statement, cover, or what "route totals" total. |
| F | Moderate | The stump (own requests produce register entries, so the two lists are not independent) is not documented anywhere; naive routes give 18 or 23. Dictionary and manifest hand over the under-recording concept. |
| G | PASS | method_or_model_selection / statistical_rigor on honest reported numbers. |
| H | PASS | domain used, two layers, decisive step analytical. |
| Hygiene | PASS with notes | see below. |

## Figures I could not reproduce, or that I reproduce only under a convention the text does not file

1. Ask 6 route totals: golden 7.9 / 5.4 / 2.3. Over the cases the quarter rows cover (2025/26 scheme-year scam cases closed 1 Apr 2025 to 31 Mar 2026, denominator 6,548,215) the totals are 8.33 / 5.74 / 2.22 (8.3 / 5.7 / 2.2). Golden totals only reproduce on all 2025/26 scheme-year scam cases including the 921 closed after 31 Mar 2026 (denominator 10,468,750: 7.91 / 5.44 / 2.25). The quarter rows themselves reproduce (Q1 5.7/4.4/2.3, Q2 12.9/3.8/2.0, Q3 5.8/7.4/0.9, Q4 8.7/5.1/3.7) only with: scam cover only; case belongs to scheme year 2025/26; grouped by closing quarter; numerator all ledger credits ever posted (to July 2026). Reading "cases closed in each 2025/26 quarter" literally (any case year) gives Q1 9.7/6.5/1.7, Q2 10.8/3.8/3.2, Q3 5.7/7.3/0.9, Q4 8.7/5.1/3.7; adding unauthorised fraud gives yet another set (Q1 8.5/6.0/2.2 ...). The shipped recovery_statement_2025_26.csv (same population as the golden denominators, but credits "as credited", repatriation net of agent charges) gives Q1 0.6/0.0/0.1 ... Q4 9.3/4.5/2.2; its basis is not tied to the ledger anywhere.
2. Ask 4 quarter totals: reproduce from advice-detail indemnity_paid_gbp (Q1 665,483.62 etc.). Rounded parts do not sum to the rounded total in Q1 (311,088+272,896+81,499 = 665,483 vs 665,484) and Q3 (613,154 vs 613,153); a one-pound fork depending on summing before or after rounding. Not filed.
3. Ask 4 source: the advice header advice_total_gbp disagrees with the sum of the detail lines in 49 of 144 unauthorised advices (header higher, +15% to +740%, e.g. ADV-202604-101-U 59,472.82 vs lines 32,097.45; every scam advice ties). Header-based quarter totals are Q1 921,924, Q2 793,015, Q3 836,252, Q4 764,257. The golden (lines) is supported by the column name indemnity_paid_gbp and by exact tie of every line to the register's reimbursed_amount_gbp, so I treat the golden as the better reading, but no shipped text says the header is wrong or what the excess is.
4. Ask 5 reproduces (957 rows over main plus supplement, all notified 1 Apr to 30 Jun 2027; counts equal the revised returns). Five rows share a case_reference with a different case (different dates and amounts): a solver who deduplicates on reference loses them (e.g. KM-101 191 / 458,875 instead of 193 / 460,362). Golden keeps them, correctly, but nothing says references can collide.
5. Index per member: Saltmarch 139.3 (21.88 -> 22), Trentmoor 301.4 (15.07 -> 15), Brindlemere 517.4 (12.11 -> 12) reproduce under the golden convention. Recorded 109 / 246 / 443 reproduce.

## Gate C detail: main call forks

Standard 4.2/4.4 fix the definition, the denominator and the rounding; they do not fix how the two sources are combined, what window the evidence runs to, or how to treat registrations an own request produced. The shipped text is silent, and each of these is defensible:

- Evidence window. Prompt: "our data stops at 31 March 2027". Trustee pack: reviews "prepared from the mutual's evidence base at 31 March 2027". Standard 4.2: "as it stands when the review is prepared". Files: register notified dates to 27 Jun 2027 (51 of Castlegate's 400 notified after 31 Mar), matches registered to 30 Jun 2027 (55 of 412), requests to 25 Apr 2027. Golden uses everything (31). Cutting at 31 March gives Castlegate 26, Saltmarch 18, Trentmoor 14, Brindlemere 10. Closed only by inferring that 4.2 outranks the prompt and pack.
- Attribution rule for own-request registrations. Golden rule: request_sent_date <= registered_date (205). The reglag distribution (registered minus request, all members) is: induced registrations sit at fixed lags by firm type (clearing bank +1/+2, e-money +14/+15, building society/overseas +38 to +40), and there is a sharp cluster the other side of the request (-1: 275, -2: 248, -3: 163, -4: 99, -5: 48 against a flat tail of about 12 a day at -8 to -12, and no same-day rows). Those near-miss registrations are scored as independent by the golden rule. Treating registration within two days before the request as request-linked gives Castlegate 795.5 cases, 35.7 (36), Saltmarch 23, Trentmoor 16, Brindlemere 12 or 13. The golden's own sentence ("not a rule on the registration date") sits uneasily with a step that is itself a registration-date rule. The text does not say which is right.
- Pre-payment registrations. 33 of Castlegate's matches (all in its own register) were registered before the payment date (as early as 94 days before across members). Dropping them from the register list as non-attributable gives 800 cases, 35.9 (36).
- Estimator form. Chapman 688 gives 31, but conditioning capture probability on own cases never requested (34/109) gives 679, 30.44, which rounds to 30. Nothing in the pack pins Lincoln-Petersen on the independent register list over this. With only 120 overlaps the sampling band on 690 is about plus or minus 8 percent (index about 28.5 to 33.5), so "nearest whole case" is not a quantity the data forces; the golden is the one point estimator, not the only licensed one. The all-members ranking is unaffected by any of these (Castlegate first, then Saltmarch, Trentmoor, Brindlemere), so the chart order and the "highest" call survive; the stated index figures do not.

Competing answers that do survive on the shipped files: 30 (stratified estimator), 26 (31 March cut), 36 (near-miss or pre-payment treatment). 18 and 23 are the easy-route answers and are properly ruled out by the own-request dependence.

## Gate G (full)
mechanism: statistical_rigor / method_or_model_selection (dependence-aware two-source estimate, with a data-driven choice of which sightings are independent)
stumping_family: analytical_non_defect
surface_read_dependency: no
sole_data_defect: no
Every reported number (400 recorded, 412 matches, 22,301,200 payments) is correct; nothing reported is overturned. The difficulty is that a two-source estimate on all matches is biased because Castlegate's own fund-return requests create register entries, which is a method failure on honest figures, not a rejection of a misleading surface read. On a version of the data without the request effect the all-matches estimate would simply be right, so the dependence is part of the structure being tested; borderline only in that the dependence exists solely in a file whose job is to expose it.

## Gate H (full)
domain: pass. The deciding quantity is an actuarial incidence estimate for unrecorded claims (cases a member's own record did not hold) per exposure, which an underwriting and pricing function would estimate with a two-source model; swapping nouns to hospitals or schools would not leave the task unchanged since the beneficiary-account register, fund-return requests and the member's own record are specific to scheme claims.
layers: pass. Layer 1: 2023/24 layout with pence, dd/mm/yyyy and thousands against whole payments later; preliminary against revised returns for 2026/27; sort-code hyphen and leading-zero mismatch between the match run and the register; scheme-year quarters starting in April; a notifications feed with a supplement and colliding case references. Layer 2: the own-request dependence between the register and the case list and the two-source estimate built around it.
decisive_step: analytical. A strong analyst who cleaned everything and read every field correctly would run a two-source estimate on all 412 matches (507, index 23) or plan on the register (400, index 18), so the easy route files a wrong answer. The qualifier is that the repair itself is not unique (Gate C), which is a determinism problem and not a Gate H failure.

## Files / Hygiene: PASS with notes
19 files; formats csv, xlsx, pdf, txt (4). Largest: mule_account_register.csv 29,989 rows (meets the 25,000 floor). Distractors present (national_scam_statistics_calendar_year.csv, aml_alert_summary.csv, recovery_statement_2025_26.csv as a conflicting basis, notifications feed in the other direction). No README or benchmark disclosure found; no public-data contamination (synthetic fiction). Notes, not exclusion-level: register_feed_notes.txt reads as an explained how-to ("Pad the account number back to eight digits ... or the match loses every account") rather than a log entry; export_manifest.csv "what_it_omits" and data_dictionary.csv ("A case appears in the register only when the member's own controls or its customer brought it to it") spell out the under-recording concept; trustee_pack_2027_07.pdf refers to "the register feed change of February 2027" and to papers 1 to 3, and nothing in the pack describes a Feb 2027 change (I checked register volumes, request-induced share and lags by month: no discontinuity); recovery_statement_2025_26.csv bases (as credited, net of agent charges) are unreconciled with the ledger. Trustee pack and prompt say data stops at 31 March 2027 while the extracts run to 30 June 2027 (temporal coherence finding, and the source of the window fork above).

## Stump power (Gate F)
The own-request dependence is the working trap: the easy two-source estimate and the register count both land on a wrong index (23, 18), and nothing in the pack names the dependence. Too-easy signals are limited to the dictionary/manifest explaining under-recording. Because the correct repair is not uniquely forced (30 / 31 / 36), a solver who finds the trap can still miss the golden for a convention reason, which is not credit as a valid stump.

## Fix (prompt, then input_files)
- prompt: file the estimand, not the method: state the evidence cut-off ("register and matching run as received to 30 June 2027" or "to 31 March 2027"), and that sightings produced by the member's own fund-return requests are not independent sightings (or name the population: payments whose registration did not follow an own request). Remove or reword "our data stops at 31 March 2027".
- input_files: decide the near-miss cluster and the 33 pre-payment registrations (either remove the near-miss cluster so the date rule is clean, or give a shipped fact that classifies them), and widen the overlap so the rounded index is not inside the sampling noise; reconcile or explain the 49 unauthorised advice headers and the recovery statement basis, or state the ledger as source in the ask.
- prompt, ask 6: state case population (scheme-year-2025/26 scam cases, by closing quarter), the credit basis (all ledger credits to date), and that the route total covers the same cases as the quarter rows (or what it covers); state that ask 4 totals are summed before rounding.
- solution: if ask 6 is kept as is, the route totals line must be changed to 8.3 / 5.7 / 2.2 to agree with the quarter rows.
