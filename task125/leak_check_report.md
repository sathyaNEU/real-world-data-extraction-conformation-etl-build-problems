# leak check, task125

**Verdict: REVIEW.** 12 files read, 48 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: decisive, population, controls, weights, households, instruction, asserted, carried, statistics, release, sentence, protocol, record, change, repeat, rotation, surface, person, carries, records, intakes, re-raking, address, template, section

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `hls_data_dictionary.md`: golden figure 110 appears: ...cal date and time the visit started | | outcome | 110 interview, 210 refusal, 310 no reply, 410 not eli...

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `extract_notes_2026-10-20.md`: 10 of 25 stump-paragraph terms appear (population, controls, statistics, release, record, change); read whether the document names the move
- **REVIEW** `field_instruction_FI-2024-03_call_pattern.pdf`: 4 of 25 stump-paragraph terms appear (instruction, statistics, record, address); read whether the document names the move
- **REVIEW** `field_instruction_FI-2026-07_first_interview_visits.pdf`: 5 of 25 stump-paragraph terms appear (instruction, statistics, record, change, address); read whether the document names the move
- **REVIEW** `hls_data_dictionary.md`: 6 of 25 stump-paragraph terms appear (statistics, record, person, intakes, address, section); read whether the document names the move
- **REVIEW** `hls_methods_note_2025.pdf`: 12 of 25 stump-paragraph terms appear (population, controls, weights, instruction, statistics, release); read whether the document names the move

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

## Solver's-eye read

Isolated reader (general-purpose, sonnet, medium) on prompt.txt and the rebuilt target.zip, 2026-10-12, after judge pass 1's repair.

# Reader report t125

Read prompt.txt and all 12 target files. Did not solve.

## 1. Decisive-step sentences
None names the move or warns an obvious approach is wrong. All are facts an office would file.
- methods_note §5: "its effect on the estimates is measured by applying the change to the last full quarter collected before it and re-running the estimation as in section 4." Closest candidate. General standard method; names the base quarter and re-raking, not the trap. Filed convention.
- methods_note §6: "unweighted... People not interviewed in the second quarter are left out." Definition for the flow ask.
- methods_note §7: "changes and differences are computed from unrounded estimates and rounded independently." Rounding convention.
- methods_note §1: "An address stays in the survey for five consecutive quarters... about a fifth of the sample is replaced each quarter." Design fact; implies phase-in/out but does not say so.
- FI-2026/07 item 2: "Addresses are not reissued." Item 5: "The visit pattern from January 2027 will be set with the 2027 field budget." Plain facts.
- FI-2024/03 item 3: "A visit at which you speak to a household member is a contact, whatever its outcome." Definition.
- extract_notes: "address serials carry a check digit as a tenth character." (join-key mess, Layer 1) and "July to September 2026 is the first quarter collected under FI-2026/07." (prompt already says it).
Prompt itself is not instructional.

## 2. Helping files
None. Release tables stop at April to June 2026 (no Q3, no cap effect). Nothing ranks regions or candidates. field_staffing and jobseeker_support files look like distractors. Call records are raw evidence, not a marker. No hidden sheets.

## 3. Literal execution
1. Compute Q2 and Q3 2026 unemployment rates from the parquet with raked weights (region, and seven age groups by sex, to that quarter's controls).
2. Cap effect per §5: apply a three-visit cap to Q2 2026 (last full pre-change quarter), drop wave-1 respondents needing visits 4 to 6 (call records joined on serial, handling 10-char serials), re-rake, take the difference in rates.
3. Labour-market part of the rise = rise minus cap effect.
4. Project the gap over five-wave composition: cap enters with the Q3 2026 intake, reverts with the Q1 2027 intake, so gap builds and decays by quarter.
5. Regional asks: visits from call records; employed share of Q2 unemployed as unweighted matched flow; employed hours from weights.
Forks:
- Cap-effect basis: §5 says apply to Q2 2026; prompt wording could mean Q3's own data. Mild.
- Rounded vs unrounded rise: §7 closes it; Q3 rate not published so computed.
- "Six visits all along" counterfactual for Q3 2026 cannot be observed; relies on pre-cap record.
- Controls rebase at 2026Q1: "published since 2023" series mixes bases. Presentation fork.
- Flow denominator closed by §6.
- Duplicate/late/misnumbered visit_no rows (semantics).

## 4. Main-call forks
- "the labour market": rise minus cap effect vs rise in a re-estimated six-visit series; agree if cap effect defined per §5.
- "published": rounded vs unrounded; §7 closes.
- Projected gap each quarter to Q3 2027: whether the Q2 2026 per-intake effect is held fixed or rescaled per quarter composition. Real fork; needs a filed sentence.
- Whether "labour market" is judged on unemployment alone; prompt asks both gaps.

## Best guess
Measure the cap effect directly: flag wave-1 respondents who needed visits 4 to 6 via the call records (fix the serial join), drop them from Q2 2026, re-rake to 2026Q2 controls, difference the rates. Wrong path: treat the whole rise as labour market, or use the capped Q3 sample as is. Difficulty: serial join, wave-weighted phasing of the gap over five intakes, and the matched flow denominator.

Session reading: no decisive-step sentence and no helping file. The reader's own approach drops the visit 4 to 6 households from wave 1 only (the default path), so the persistence rung stayed unseen. Its "projected gap" fork (hold the per-intake effect fixed or rescale it by the quarter's composition) is the method the stump turns on, not a reading of a term.
