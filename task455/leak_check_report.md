# leak check, task455

**Verdict: REVIEW.** 10 files read, 24 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: caldmere, eskwell, address, quarrin, register, closed, predecessor, workers, tolbeck, dunrath, worker, continuity, guideline, golden, records, transfer, decisive, take-overs, payroll, program, reports, experience, industry, asserted, reader

## 1 file names (REVIEW 1)
- **REVIEW** `ui_wage_records_2024q4_2026q4.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 3 answer figures in the pack (REVIEW 7)
- **REVIEW** `ui_wage_records_2024q4_2026q4.txt`: golden figure 118 appears: ...38740|2024|4|6261.33 9XPQBSAJBFK|307638740|2024|4|118.95 C24VPF25T7T|307638740|2024|4|11457.60 CD7QJ5GA...
- **REVIEW** `ui_wage_records_2024q4_2026q4.txt`: golden figure 104 appears: ...12329|2024|4|9564.35 UTEULC59CVU|497012329|2024|4|104.55 YGFTPV7DEGE|497012329|2024|4|9105.84 A7PBXHBAF...
- **REVIEW** `ui_wage_records_2024q4_2026q4.txt`: golden figure 110 appears: ...52193|2024|4|6284.63 VTAMFFRSPLY|195952193|2024|4|110.40 WSKEB2DAVD5|195952193|2024|4|4222.92 6AX5CVFHP...
- **REVIEW** `ui_wage_records_2024q4_2026q4.txt`: golden figure 121 appears: ...4005|2024|4|10603.10 E2M5CUV87BJ|225574005|2024|4|121.35 EDY5TQWMGMV|225574005|2024|4|7016.81 ERXH2AB8F...
- **REVIEW** `ui_wage_records_2024q4_2026q4.txt`: golden figure 113 appears: ...1497|2024|4|10975.17 NK89TS45GVN|321671497|2024|4|113.72 P9K2UEQW9AK|321671497|2024|4|7997.03 PSB373RCY...
- **REVIEW** `ui_wage_records_2024q4_2026q4.txt`: golden figure 702 appears: ...1890|2024|4|13306.51 LBTFH7UNJL5|148841890|2024|4|702.66 LGXMKHGJ2P9|148841890|2024|4|7358.94 LKZ9TP89F...
- **REVIEW** `formation_counties_program_guideline_2027.pdf`: carries 6 of 7 distinctive words of the committed call: 'Commerce should designate Eskwell, Dunrath and Quarrin as Formation Counties for 2027 to 2029.'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `formation_counties_program_guideline_2027.pdf`: 9 of 25 stump-paragraph terms appear (caldmere, eskwell, quarrin, tolbeck, dunrath, guideline); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 40% of 196 prompts (cap 30%); second-sentence opener 'put' at 39% of 196 prompts (cap 20%); rounding opener 'give' at 48% of 196 prompts (cap 20%); reword at the role level, not the verb

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)


## Solver's-eye read

Isolated reader (2026-11-01 re-check, medium effort), fresh copies of prompt.txt and target/ only; it computed nothing.

1. Decisive-step sentence: none. The guideline gives the birth definition (3.3), the base (3.4), the county (3.2) and
   the comparison (4.2), never how a continuation shows.
2. Ranking file: none. The grant disbursements name three FY2026 grantees; a prior-period payment record, a plausible
   distractor and not a ranking.
3. Helper-only file: none. The county codes and the NAICS crosswalk are reference tables a state agency keeps.
4. Answer-like figure or name: none.
5. Literal reading: the three counties highest on 2026 first-employment establishments net of continuing businesses,
   per 100 establishments reporting employment in 2025Q4, by worksite county, unrounded; population and window filed,
   detection of continuations left open.
6. What decides: an analytical choice (which new accounts continue a business), read through worker overlap in the
   wage records; nothing states the rule and nothing reads as planted.
7. Realism: nothing reads as generated or templated.
8. REVIEW lines: wage records harmless (the UI wage record extract; the digits are wage amounts); guideline harmless
   (the governing document must name the counties and the program's terms); prompt shell harmless.

Second read, after the guideline 3.3 sentence on first reported employment (fresh copies, medium effort): no
decisive-step sentence (3.3 defines a birth and names no evidence for continuity); no ranking or helper file; no
answer-like figure. On question 6 it leaned to rule application with a linkage step, while naming continuation across
accounts as the one judgement no sentence states; the determinism judge recomputed and rules the decisive step
analytical (Gate H, pass 4), which settles the split (build-pipeline). Realism: the disbursements' grant numbers carry
the county code, as such numbers do; nothing generated or templated.
