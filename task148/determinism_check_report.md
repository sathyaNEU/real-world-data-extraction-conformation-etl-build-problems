Judged pack: commit eb89e4a (the hardened pack, target.zip sha256 35bd97282bebbf5e88c44d37942afd46b3c690076c5205aeec4562a037fa0b03). After this verdict the README's callback-desk sentence was reworded to close finding (b), the April 2026 linkage; the round 1 verdict on the pre-hardening pack is determinism_check_report_round1.md.

# Verdict, task148 (re-judge, fresh)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed, no rerun. Optional note-level items under Evidence (rounding exposure on two asks).

**Why:** The shipped files force one answer: Jul 2027, Aug 2027 and Jun 2028 fall short of the 90 per cent standard with four call-takers (88.07, 88.91, 88.97 per cent); Sep 2027 and May 2028 (91.11, 91.04) and every other month clear it. I rebuilt the full chain from the raw files and every load-bearing figure reproduced. The decision survives every reasonable alternative I tried (patience anywhere in the 95 per cent interval, busy time, night weighting, a non-stationary simulation, a 2 per cent overlap correction of the forecast). It flips only on genuinely wrong methods (Erlang C, one pooled patience, patience read off hang-up waits, talk time instead of busy-until-Ready).

## Evidence (recomputed from target/ only)

| Value | Golden | Mine | Source |
|---|---|---|---|
| Calls, legacy + i3, tests out | 416,621 | 416,621 | acd csv (78,310 non-TST) + jsonl (338,311 non-test), local tz conversion, no overlap |
| Busy time (ready less answered, answered calls) | 226.9 s | 226.909 | both call files, SOP 4.2 |
| Late shift calls / hang-ups | 15,814 / 81 | 15,814 / 81 | Fri/Sat 22:00-02:00 dated by start day (SOP 5.2) |
| Patience (summed waits over hang-ups): late / other / all | 123.2 / 587.7 / 576.6 | 123.16 / 587.67 / 576.62 | same |
| Monthly compliance Jul27..Jun28 (Erlang A, c=4, SOP 3.3, forecast FY2028 Tavish rows, night-weighted, start-month) | 88 89 91 93 94 93 94 95 94 93 91 89 | 88.07 88.91 91.11 92.96 94.05 92.88 94.03 94.94 94.09 92.90 91.04 88.97 | forecast xlsx FY2028 sheet |
| Halvorsen reached / transferred Q1..Q4 | 1475/1326, 1243/1127, 1104/1003, 1253/1160 | identical | che records (joined on callId or incidentId, last device/gnss fix, polygon with its hole and exclave), i3, directory (Wexley primary + alt07) |
| Callback within 2 min, Jan..Jun 2026 | 55.2 45.1 56.8 52.6 50.3 51.4 | 55.2 45.1 56.8 51.5* 50.3 51.4 | callback desk tasks, i3 ended time |

*April: one hang-up (09EE50160AF9, 16:49:56) came a few seconds before the task opened by the same number's other abandon (task created 16:50:00, first dial 16:50:56). Joining it to that not-yet-dialled task (README rule) gives 51 of 97 = 52.6, matching the golden. A strict "task exists at hang-up" reading gives 51.5. README's "has not been dialled yet" supports the golden reading, so I treat it as reproduced, with a small wording exposure on that one ask.

Competing answers tested against the strongest honest case:

| Alternative | Result | Verdict |
|---|---|---|
| Erlang C (no hang-ups) | short: Jul, Aug, Sep, May, Jun (82.6, 84.1, 87.7, 87.6, 84.2) | wrong: predicts zero hang-ups, data shows 0.46 per cent on the late shift |
| One patience for all calls (576.6) | short May-Sep (89.0 to 85.0) | wrong: late-shift hazard is about 8.1e-3 per s against 1.7e-3 elsewhere (interval hazards constant in both, so exponential fits) |
| Patience as mean wait of hang-ups (37.6 s) | none short (90.8 minimum) | wrong: ignores the answered calls' time at risk (censoring) |
| Talk time (release less answer, 158.8 s) as busy time | none short (95.5 minimum) | wrong: SOP 4.2 pins busy until Ready |
| Patience 100 to 200 s (95 per cent interval for 81 events is about 96 to 158) | Jul, Aug, Jun short in every case; Sep, May stay above 90 (90.3 at 200 s) | set is robust |
| Late-shift-only busy time (225.5 s) | +0.1 to +0.2 points, same set | robust |
| Unweighted nights; Poisson simulation with queue carry-over between hours, empty start | within 0.3 points (Jul 88.4, Sep 91.35, May 91.3, Jun 89.2, Dec 93.06); same whole per cents | robust |
| Forecast Halvorsen move may double-count the 5,075 a year already reaching the queue (about 2.4 per cent of late-shift volume) | Jul 88.6, Aug 89.4, Jun 89.4: same set | robust (not a fork; SOP 5.1 also names the forecast as the planning basis) |
| Calendar-clock Fri/Sat 22-02 instead of shift-dated | patience 154.7, same set | robust |

Residual exposure (not a failure): (a) a patience calibrated to the observed 0.46 per cent hang-up rate (about 80 s, a method-of-moments choice) gives Aug 89.83 and Jun 89.88, still under 90 but printing as 90 to the whole per cent; the observed 41 against 32 expected hang-ups is within noise (z about 1.4) and the MLE is the principled estimate, so the golden stands, but those two graded cells carry a one-point rounding risk. (b) Q4 April wording noted above.

All decisive facts are present in the files: standard and measure (SOP 2.1, 3.2, 3.3), busy rule (4.2), shift and month assignment (5.2, 6.1), four funded call-takers (budget PDF table), forecast and Halvorsen move (xlsx), transfer destination mapping (directory), last-handset rule and callback join rule (README). Nothing relies on outside knowledge.

## Files/Hygiene
PASS. 14 files (13 inputs plus README), formats: csv x8, jsonl, xlsx, pdf x2, geojson, md. Large file present (339,676-line i3 log). Layout changes across systems (legacy local-time ACD vs UTC i3), cutover window, call vs incident keys, pseudonym keys, delta in hang-up timing are realistic. Distractors present and unused by the solution: admin_line_acd_fy2026.csv, cad_incidents_fy2026_fri_sat_late.csv, roster. The README is an in-fiction QA hand-off note with no authoring leakage. Temporal coherence holds (data to 30 Sep 2026, budget draft 2 Oct, README 6 Oct 2026, move on 1 Jul 2027). No public-data contamination. Mild synthetic tell: busy times and patience are near perfectly exponential (CV 1.00, constant hazards), which a real floor would not show; not exclusion-level. Cross-batch fingerprint check not run (isolation forbids other task folders).

## Stump power
Good. The easy routes are the industry-standard Erlang C and a single pooled patience, both of which are wrong in the same direction and put May to September short (a five-month answer against the true three), plus the hang-up-wait patience (none short). A strong model has to notice that abandonment is a segment property (late shift 123 s against 588 s), estimate it with the answered calls' time at risk, and use an abandonment-aware queue. One or two GPT runs taking Erlang C or the pooled patience is the expected failure; the task needs live testing to confirm, but the trap is genuine and clean.

## Stumping type
`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
No reported figure is wrong; the difficulty is choosing and parameterising the queue model on honest data (censoring-aware segment patience, validated against the observed 0.46 per cent hang-up rate). On perfectly clean data it would still stump.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
Domain: 911 answer-time staffing by queueing with abandonment (swap test fails: "megawatt-hours" or "visits" would not leave Erlang A, call-taker busy-until-Ready and caller patience intact). Layer 1: legacy vs i3 export, local vs UTC, CAMA/NG911 cutover, callId vs incidentId keys, pseudonymised numbers. Layer 2: segment patience with censoring and an abandonment-aware queue checked on observed hang-ups. Easy route a strong, correct-reading analyst takes: Erlang C (or one pooled patience) with the right busy time, giving May to September short (five months instead of three).

## Fix
none.
