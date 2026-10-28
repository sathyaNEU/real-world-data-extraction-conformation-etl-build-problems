# determinism-check report, task464, 2026-10-28 (architecture 8, pass 5 of the slot)

## Verdict
DETERMINISTIC (one residual reading fork on the terms of reference), no SOLUTION_WRONG
**Disposition:** SEND_BACK
**Stumping type:** mechanism: planted_defect_flip, stumping_family: surface_read_rejection, surface_read_dependency: yes, sole_data_defect: yes

## Why
Every graded figure reproduced from the shipped bundle (target.zip md5 251a8946). The judge classed the decisive step as the
retired scaffold: the coded shares are a misleading surface read and the call flips away from it, "on clean, correctly coded
data the task would not stump". Gate H3 decisive_step: planted. The residual fork: "does not re-read or re-code the exit
comments" read literally as filing the coded shares (work hours clash 24.4).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| files | 10 or more | 13 | yes |
| formats | 3 or more | 4 (csv, json, pdf, xlsx) | yes |
| large file | 25,000 rows | enrolments_2025_26.csv, 90,540 rows | yes |
| distractors | 2 named in metadata.json | satisfaction workbook, attendance return | yes |
| deliverables | 1 to 3 | 2, both in golden | yes |
| asks | unit and rounding stated | yes, rounding at the close | yes |

## Gate G reconciliation
The design note and card class the step analytical (classification_error, estimation_fit). The judge and, independently,
the leak reader's question 6 ("a planted-data component") both read the miscoding as a planted defect the solver catches.
Two isolated reads agree against the design: the mismatch is the finding, and it predicts the send-back.

## Stump power (Gate F)
Moderate by the judge: a strong model that reads the quality procedure reweights; the cutover re-keying is the likelier stump.

## Next action for the author
Re-root at stage 1 as architecture 9: the reported numbers must be right and the difficulty an estimand or method choice.

## The thread's verdict, verbatim

# Determinism verdict, task464 r1

- **Verdict:** DETERMINISTIC (one residual reading fork, below). No SOLUTION_WRONG: every figure reproduced.
- **Disposition:** SEND_BACK. Gate G (banned stumping type) and Gate H3 fail. The fix rebuilds the decisive step, so a rerun is required.

## Why
Every committed number reproduces from the shipped files. The adjusted-share answer is forced once the quality-assurance procedure is read as the governing estimand: it says the sample is drawn by code, with all OT comments and 400 per other code. That makes post-stratification the only coherent weighting. The task is still a banned scaffold. Its main stump is catching that the typed-code shares (work hours clash 24.4 per cent) are misleading and flipping to caring responsibilities. The hidden 25-course re-keying is a second planted defect.

One fork is not fully closed. The terms of reference say the review "does not reopen the coding manual and does not re-read or re-code the exit comments". A literal reader can take that to bar the moderation file and file the coded shares: work hours clash 24.4, caring 19.4, gap 5.0. I read it as barring a fresh recode of the 17,231 comments, not use of the moderating coder's categories already on file. The quality-assurance sentence "the service needs to know how its coding stands up before the figures are used" supports that reading. The answer is therefore forced, but only just. The prompt's "happened for that reason" supports the adjusted figure. KEY_ASSUMPTIONS is empty.

## Evidence (recomputation ledger)
| Figure | Recomputed | Source | Reproduced |
|---|---|---|---|
| Total withdrawals | 17,231 (9,133 csv + 9,713 json - 1,615 shared winter refs) | both withdrawal files, deduplicated on ref | yes |
| Typed codes | 24 case variants, normalised by strip and upper | reason_code, exitReasonCode | yes |
| Overlap rows | 0 code, uln or date conflicts; 20 comment text differences, immaterial | | yes |
| Coded work hours clash | 4,199, 24.37 -> 24.4 | | yes |
| Coded caring | 3,337, 19.37 -> 19.4 | | yes |
| Coded others | 15.41, 14.02, 13.63, 13.20 (not in the golden) | | n/a |
| Moderation file | 4,416 rows: 2,416 OT (census) + 400 each of the other five; coded_reason matches the extracts on every row | coding_moderation_2025_26.csv | yes |
| Caring share of work hours clash | 59/400 = 14.75 -> 14.8 | moderation file | yes |
| Adjusted caring | 25.09 -> 25.1 | stratum split x coded share | yes |
| Adjusted work hours clash | 19.40 -> 19.4 | | yes |
| Adjusted others | 15.47 -> 15.5 (course too difficult); 14.70 -> 14.7 (travel); 13.53 -> 13.5 (health); 11.80 -> 11.8 (other) | | yes |
| Adjusted sum | 100.0 | | yes |
| Gap | 5.69 -> 5.7 | | yes |
| Pooled moderated sample, unweighted | OT 34.5, caring 19.0 (wrong estimand; the quality-assurance PDF rules it out) | | n/a |
| Catalogue vs enrolment terms | 277 courses; 58 span two terms in the enrolment rows, 25 T2 starters with terms_spanned=2 show only T2 rows | course_catalogue, enrolments | yes |
| Re-keyed pairs | exactly 25; each T3 course has all its learners (223 of 224 for the first pair) inside the T2 course's continuing set, same catalogue centre and area, no ambiguity | enrolments_2025_26.csv | yes |
| Learner-courses, five centres | 69,151, after excluding 4,127 first-row MDV (not in site_directory) | | yes |
| Started per centre | Cassgrove 11,468; Hollowdean Learning Hub 12,849; Northmarket Centre 17,228; The Lathe Street Building 15,857; Wyebrook Adult Learning Centre 11,749 | | yes |
| Completed share (any row completed) | 64.62 / 64.11 / 65.50 / 64.67 / 63.93 -> 64.6 / 64.1 / 65.5 / 64.7 / 63.9 | | yes |
| Completed, last-row alternative | identical to any-row | | n/a |
| Hours by area, once per learner-course | English and maths 832,566; Digital skills 734,640; ESOL 749,682; Health and social care 756,246; Business administration 726,420; Construction skills 687,663 | catalogue; enrolment first-row hours give the same totals | yes |
| Centre attribution | first-row centre equals catalogue centre in every case, so the attribution choice does not matter | | yes |
| Naive unlinked count | 74,464 started, double counting the 25 re-keyed courses | | n/a |

SOLUTION_STEPS and CRITICAL_COMPONENTS agree with the files. CRITICAL_COMPONENT 1 gives "caring 19.4" as a coded share, which is right. The recommendation text's phrase "every comment coded OT is moderated" matches the quality-assurance PDF.

## Gate checks
- **Gate A and B:** pass. Every decisive fact is shipped: the sampling design in the quality-assurance PDF, the code list, the manual and the catalogue.
- **Gate C:** the one fork above (coded versus adjusted) is the only surviving alternative. Sampling error on the winner's lead is about 0.5 points against a 5.7-point gap, so the margin is robust. The 25 links are unique.
- **Gate E:** the prompt asks one call and a fixed list of outputs. "Share that happened for that reason" is not an explicit instruction to adjust, which is the fork above.

## Files/Hygiene
**PASS.** 13 files; formats are csv, json, pdf and xlsx.
- Realistic noise is present: code case variants, a renamed centre, a stray site MDV, and the late-keyed winter rows in the spring export.
- Decoys (attendance, satisfaction, the budget workbook, the satisfaction workbook) are plausible operational files.
- The ToR is dated 2026-11-18 and the file mtimes are Nov 2026, later than the data; this is minor.
- No authoring or provenance leakage found. The data is fabricated, not public, so there is no contamination concern.

## Stump power
Moderate. The QA PDF spells out the by-code draw, so a strong model that reads it will reweight. The likely failures are the easy routes: the coded counts (work hours clash, 24.4), the pooled moderated sample (OT 34.5), and an unlinked learner-course count of 74,464. The 25-link re-keying is discoverable only through the catalogue-versus-rows mismatch and ULN overlap, and is the likelier stump.

## Stumping type
`mechanism: planted_defect_flip`, `stumping_family: surface_read_rejection`, `surface_read_dependency: yes`, `sole_data_defect: yes`.
Banned scaffold: the primary stumping strategy is catching that a misleading reported/surface read is wrong and flipping away from it, retired for tasks on/after 8/16 no matter how many corrections it takes. The misleading read is the typed-code share, plus the unlinked learner-course keys. On clean, correctly coded data the task would not stump. Rebuild around a FINE-numbers shape where the reported numbers are right.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: planted`.
Layer 1 is messy codes and re-keyed courses. Layer 2 is post-stratified estimation of the reasons. But the decisive flip (WH 24.4 -> caring 25.1) exists only because coding error is planted and moderation is supplied to catch it. The easy route (coded shares -> work hours clash by 5.0) is what a strong analyst who read everything would file if they honoured the ToR sentence.

## Fix
Fix location: input_files and prompt. Rebuild the decisive step so the reported shares are correct and the difficulty is a method or estimand choice (for example a forecast or a binding constraint). If the current design is kept, fix the prompt by stating that the shares are to be estimated from the moderation file, and reword or delete the ToR sentence "does not reopen the coding manual and does not re-read or re-code the exit comments".
