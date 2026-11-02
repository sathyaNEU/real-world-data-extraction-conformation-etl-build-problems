# task475 determinism check (architecture 2)

2 isolated judge pass(es), each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | c316e563 | NOT_DETERMINISTIC on the main call (Gates C and E; order kept; F real; G PASS; H PASS) | SEND_BACK as labelled; a C/E repair by the gate table | regulation 14.1 files that the question and the average question are compared on the same candidates, whichever questions each chose (no method named); the May NGUYEN record's date of birth set apart so every cross-sitting link rests on a member number or full name and date of birth |
| 2 | 9a59084f | DETERMINISTIC (order kept; F moderate; G PASS; H PASS) | APPROVE | none (the optional refund-ask pin not taken: the golden is the better literal reading of regulation 19.4) |

The architecture 1 record is in the folder's archived reports.

---

# Determinism check, round 1 (2026-11-02): NOT_DETERMINISTIC on the main call (Gates C and E; order kept; F real; G PASS; H PASS), SEND_BACK as labelled; a C/E repair by the gate table

Isolated thread, Sonnet at medium effort, on target.zip c316e563.

# Verdict: task475 (Paper 2 Nov 2026 results), judge a2r1

ORDER kept: derivation.md was written to disk before graded_blocks.md was opened.

- **Verdict:** NOT_DETERMINISTIC (competing_defensible_answer on the main call; a second, smaller fork on one supplementary figure).
- **Disposition:** SEND_BACK. Pin the question-difficulty estimand in the filed text (the WHAT: difficulty compared on the same candidates, not on whoever chose the question) and close or remove the one unresolvable identity pair; solvers see different text, so a rerun is required.
- **Why:** Reg 14.1 files "how much harder ... the question proved than the average of the paper's optional questions, each counted once, for the candidates who sat the paper". Executed word for word with the data's only stated quantity (marks), difficulty is the question's mean mark among its answerers: moves Q1 -1, Q2 +1, Q3 0, Q4 +1, Q5 0, Q6 +1, Q7 -1, Q8 -1 and 422 of 714 pass (the pooled-mean variant gives the same eight moves). The golden (Q6 +3, Q8 -3, 401 pass) holds only under a candidate-plus-question fit that no shipped text names, and the May minutes cannot arbitrate (May moves are identical under both methods, I checked). The adjusted reading is defensible, even the better statistics, but the raw-mean reading is equally licensed by the sentence, so Gate C fails for the main recommendation and for the CSV, the pass count and the chart (all depend on the moves). Gates C and E; label competing_defensible_answer. Supplementary 4 (Melbourne May-sitter count) also carries an open identity fork, below.

## Evidence (recomputed from target/)
| Item | My value | Golden | Reproduced |
|---|---|---|---|
| Sitters | 714 (742 entered Paper 2 less 28 without marks; marks exist only for entered, validly unwithdrawn candidates) | 714 | yes |
| Raw-mean moves / pass | -1,+1,0,+1,0,+1,-1,-1 / 422 (unmoved 432) | not the golden | the competing answer |
| Two-way fit moves (candidate + question effects) | -1.04,+0.96,-0.08,+1.07,-0.03,+3.04,-0.97,-2.94 | -1,+1,0,+1,0,+3,-1,-3 | yes; 401 pass reproduces. A within-candidate "versus own other answers" estimator gives -1.16,+1.14,-0.10,+1.28,-0.01,+3.22,-1.09,-3.29, the same rounded moves, so the adjusted family is internally robust |
| Other-answer means | Q6 13.5 vs 10.1, Q8 8.9 vs 12.1 | same | yes |
| Withdrawals / absentees | 61 / 31 (3 portal withdrawals at 6 Nov 20:02 to 21:46 UTC = 7 Nov Sydney have no effect under 17.2 though cae_entries says Withdrawn; they have no marks, so absent) | 61 / 31 | yes. By centre SYD 11/4, WSY 4/3, MEL 23/8, BNE 8/9, PER 7/3, ADL 8/4 all match |
| Also sat Paper 2 in May | 150 (147 on family + given + DOB, +3 surname changes linked by identical member number, DOB, given) ; SYD 33, WSY 16, MEL 34, BNE 25, PER 20, ADL 22 | 150, same by centre | yes, but see fork |
| May results changed on review | 11, all fail to pass (3 request rows carry transposed candidate numbers, resolved by family name and the post-issue senior marks) | 11 | yes |
| Refund | 2045.125 for the 11 + 580 for 4 requests received 23 to 24 July after the 21 July closing = 2,625.125 | AUD 2,625 | yes (account lines repeat invoice totals; per-request fee at fee-in-force-on-receipt less agreement discount) |

Open forks:
1. **Main call (Gate C/E, governing).** Raw mean per answerers (Q6 +1, Q8 -1, 422 pass) versus candidate-adjusted difficulty (Q6 +3, Q8 -3, 401 pass). Nothing in regs, minutes, prompt or data dictionary says the moves must remove who chose the question; "for the candidates who sat the paper" is the only hook and is read either way. The wording does not force the stump.
2. **Supplementary 4, Melbourne May-sitters (Gate C).** Nov Pham, Quang Huy (member 153041, MEL) and May NGUYEN, Quang Huy (SYD, no member number) share DOB and full given name only. Not linked (golden, 150, MEL 34) versus linked (151, MEL 35). The three accepted surname changes are corroborated by member number; this pair is not, and no rule tells the solver which standard of identity to apply.
3. Borderline 48/49 (29 candidates): Reg 15 senior re-marks are not in the export, so the CSV result is on marks of record (fail). Closed enough by Reg 12 and the May minutes precedent ("subject to the borderline review"); not a finding.
4. "Number passing" is read as the paper total (pass is per paper); fine.

## Files/Hygiene: PASS
13 files, formats csv, xlsx, pdf (2), docx, json (5 formats); marking export 26,027 rows. Distractors present and unused by the call (venue_holds_2027, ar_invoices, results history, address/adjustment requests). Mess is Layer 1 realistic (UTC vs Sydney, PAR to WSY rename, mixed date formats, repeated invoice totals, transposed candidate numbers, last-mark-wins duplicates in May). Dates coherent (portal export 30 Nov, marks to 27 Nov). Minor: Regulations v3 approval date (28 July) postdates the May review window while stating the exam rules unchanged; harmless. No authoring leakage; no exclusion-level finding.

## Stump power (Gate F)
The trap is real: the easy route (mean mark per question) gives 422 and Q6 +1 / Q8 -1, and a strong model that computes simple means will file it; those who notice that stronger candidates chose Q6 and weaker ones Q8 get 401. No documentation hands out the correction (the minutes and regs say nothing about selection). Good stump power, but its validity depends on the fork above being closed.

## Stumping type (Gate G)
`mechanism: method_or_model_selection` (selection-adjusted question difficulty), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. All reported marks are correct; clean data would still stump. Passes Gate G.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: examination moderation, scaling optional-question choice for candidate self-selection, is what an assessment analyst does (swap test fails to read the same with "megawatt-hours"). Layer 1: UTC/Sydney timestamps, centre rename and transfers, duplicate May marks, transposed IDs, repeated invoice totals; Layer 2: question difficulty net of candidate ability. Easy route: unadjusted question means, giving 422 pass and Q6 +1/Q8 -1 instead of 401 and +3/-3. Analytical, not semantics or rule application, provided the estimand is filed.

## Fix
- **prompt / input_files (regulation text):** keep the stump but file the WHAT in Reg 14.1, e.g. that a question's difficulty is measured for the same candidates (as against the questions' own answerers), without naming a fit; add a fork-table closing sentence that the adjusted and unadjusted readings are not both licensed. Re-run the golden under that wording.
- **input_files:** resolve Pham/Nguyen (give the May row a member number or alter the DOB) so the also-sat-May count has one reading; alternatively file an identity rule (member number else family + given + DOB) in the pack.
- **solution:** none needed; golden figures reproduce under the intended estimand.

---

# Determinism check, round 2 (2026-11-02): DETERMINISTIC (order kept; F moderate; G PASS; H PASS), APPROVE

Isolated thread, Sonnet at medium effort, on target.zip 9a59084f.

# Verdict (task 475, a2r2)

**Order kept:** yes. derivation.md was written to disk from the prompt and the 13 bundle files before graded_blocks.md was opened.

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE (one low-severity watch item on the refund ask, below; no rebuild, no rerun needed).
- **Why:** My independent derivation reproduces every golden figure: moves Q1 -1, Q2 +1, Q3 0, Q4 +1, Q5 0, Q6 +3, Q7 -1, Q8 -3, with 401 of 714 passing. The moves are forced by regulation 14.1 (the question against the unweighted average of the eight, "compared on the same candidates, whichever questions each candidate chose"). Candidate-plus-question fit and pairwise same-candidate comparison both round to the same eight integers, with the nearest rounding boundary 0.42 marks away (Q8 -2.94 and -2.97 against -2.5). The supplementary answers are closed by the regulations and the data. Goldens agree with my values on every item except the refund, where the two figures differ by one reading of the ask (see Evidence).
- **Evidence (recomputed from target/):**
  - Marking export, NOV26 (cae_marking_export_2026.csv): 714 sitters (696 with 5 questions, 18 with 4), one row per part, no duplicates, '-' = 0 with no all-dash question. Question-level fit: Q6 d=7.57, Q8 d=13.55 against a mean of about 10.5. Raw question means give moves -1,+1,0,+1,0,+1,-1,-1 and 422 passing (the easy-route wrong answer; unmoved gives 432). Additivity holds (residual by ability tertile under 0.4; per-tertile fits round the same). Pass count 401 reproduces. Only a "candidate's own five-answer mean including the question" variant gives Q8 -2.49 (-2), but that is not "the average of the paper's optional questions, each counted once", so it is not a licensed reading.
  - Withdrawals/absentees (cae_entries_nov2026.csv, portal_requests_nov2026.json, regs 17.1, 17.2, 17.3, 20): 61 effective withdrawals, 31 absent. Three requests (RQ-98058, RQ-98227, RQ-99194) are UTC 6 Nov but 7 Nov Sydney, so they do not withdraw. Per centre (W/A): SYD 11/4, WSY 4/3, MEL 23/8, BNE 8/9, PER 7/3, ADL 8/4. Reproduces. Reading the UTC date or the entries status would give 64/28 and MEL 26/5; reg 17.2 plus reg 20 close this.
  - Also sat May P2: candidate_no is re-issued each sitting, so it is not a key. Match on DOB + given name + family name (161) plus 3 surname changes via member_no (164); 14 of those were not marked present for May P2; 150 remain. By centre: SYD 33, WSY 16, MEL 34, BNE 25, PER 20, ADL 22. Reproduces. 53 bare-DOB coincidences are false matches and must be rejected (the data separates them by name/member no).
  - May review: closing 21 Jul (15 NSW working days from 30 Jun; matches the minutes). Request numbers 5503, 4708 and 3016 are keyed wrongly and resolve to 5053 FOSTER, 4078 SHAH and 3061 SCHMIDT by surname plus the re-marked question and completion date in the marking export. Result at issue (entries to 30 Jun, which include the 19 Jun senior-examiner borderline marks) against after review, both with the minutes' moves: 11 fail-to-pass; candidate 3023 (late courier script, 2 Jul) is not a review. Reproduces. Fees paid: 11 changed reviews = 2,045.13 (card fees at the rate in force on receipt; account fees from invoice totals split per request, e.g. 126.88, 54.25); the four declined requests (RR26-1278, 1281, 1284, 1287, 145 each) add 580 for 2,625.13. Golden says AUD 2,625, which is reg 19.4 applied in full (both sentences).
  - Surviving fork (low severity, supplementary ask 6 only): the ask "whether any May results changed on review and, if so, how many and the review fees to refund" can be read as fees of the changed reviews only (2,045) or all fees reg 19.4 refunds (2,625). The literal object "the review fees to refund" is unqualified and 19.4 states both refund cases, so 2,625 is the better literal answer, but the "if so" clause leaves a defensible 2,045 reading. It does not touch the main call and has no bearing on the stump. Optional tightening: "the review fees to refund under regulation 19.4" (a WHAT pin, not a method); doing so changes the prompt text solvers see, so it is the author's call.
- **Files/Hygiene:** PASS. 13 files, 5 formats (csv, xlsx, pdf, docx, json), one file of 26,027 rows plus a 1,438-row entries file. Unused-but-weighable distractors present (venue_holds_2027.xlsx, ar_invoices_2026.csv, cae_results_history_2019_2026.csv, centre_directory.csv, corporate_accounts.csv is used for discounts). Layer-1 mess reads as system output (two item-code layouts across series, UTC against Sydney, Parramatta renamed Western Sydney, per-sitting candidate numbers, invoice totals repeated per request, pre-assignment withdrawals with no candidate number, entries status_changed lagging the request). No authoring disclosure found, no answer in a filed document, timeline coherent (minutes 18 Jun, export 30 Nov). Nothing exclusion-level. Minor realism note: the minutes record only the May moves, which are consistent with the data (433 at first marks).
- **Stump power:** Moderate. Easy route: raw mean per question, giving Q6 +1 and Q8 -1 and 422 passing (stronger candidates choose Q6, weaker candidates choose Q8, which makes Q6 look easy and Q8 look hard); the right fit needs the candidate effect. Regulation 14.1's phrase "compared on the same candidates, whichever questions each candidate chose" signals the issue, so a strong solver may catch it; the hardness then shifts to the many Layer-1 and supplemental joins (re-issued numbers, UTC day-of rule, mis-keyed review ids, shared invoice totals), which are ask-weighted. To harden without breaking determinism: none needed.
- **Stumping type:** `mechanism: statistical_rigor / method_or_model_selection (confounded selection of questions)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Reported numbers are fine and no defect is planted. On clean data the choice-confounded raw means would still give the wrong moves. Passes Gate G.
- **Three rules:** `domain: pass`, `layers: pass` (Layer 1: UTC against Sydney, renamed centre, per-sitting candidate numbers, mis-keyed review ids, invoice totals; Layer 2: choice-adjusted question difficulty), `decisive_step: analytical`. This is exam equating (a core assessment/psychometrics task), and it fails the swap test cleanly ("megawatt-hours" for "marks" would not read the same). The strong analyst who cleaned the data and read every regulation correctly can still file raw per-question means, giving Q6 +1, Q8 -1 and 422 passing against the golden Q6 +3, Q8 -3 and 401. Gate H passes.
- **Fix:** none (optional: pin the refund ask to "under regulation 19.4"; prompt; low severity, author's call).

Gates: A pass (all load-bearing values reproduce; no overclaim). B pass (every decisive fact is in a shipped file; regulations, minutes, entries, portal export, marking export, May roster, review log). C pass for main call and asks 1-5; ask 6 residual fork as above (would fail Gate E only if the author treats it as open; assessed low severity). D pass. E pass for the main ask; the refund wording is the one soft spot. F moderate. G pass. H pass.
