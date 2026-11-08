# determinism-check report, task156 (architecture 4), 2026-11-08

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (no FIX_NOW; three optional wording and note touches below, no rebuild)
**Stumping type:** mechanism: forecasting, stumping_family: method_selection (time scale and out-of-regime hazard), surface_read_dependency: no, sole_data_defect: no

Thread: one judge thread (sonnet, medium), scratch /tmp/determinism-check-task156-r1/. Order kept: derivation.md written from the bundle alone, then graded_blocks.md opened. target.zip sha256 4bf9959c...2a23.

## Why
The 12-hub list is forced once the outage is read on the days-since-power-up scale. HX150 hangs occur only 76 to 120 days after the last power-up. The RC50's monthly service powers down the HX150s at 25 hubs (1,114 of 1,116 visits) but at only the five chronic hubs (3 of 218). The renewal programme removes that service at 12 hubs. The seven two-visit programme hubs then run 139 to 201 days between power-ups. The six-visit hubs (gaps 70 to 74 days) and the supply-interruption hubs NM125 and NM162 stay above 99. Schedule 4.6 and the programme file the asset base and the "any unit" test. The judge's own derivation (before it saw the graded blocks) reached the same 12 hubs under the uptime-clock reading.

Caveat on the derivation: the judge's derivation said it "could not force the exact set from the files with certainty" because of three thin-margin hubs (below). Its verdict then ruled the competing readings out. I accept that only on the evidence argument in the attendance section, not on the judge's phrase "unreasonable choice".

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Hangs before day 76 | none | min uptime 76.4 d | yes |
| Hang count | 84 | 90 total, 83 with a prior power-up on record (7 fall in Jan to Mar 2023) | within one; wording touch |
| Five chronic hubs | NM119 NM131 NM144 NM155 NM166 | same, pooled availability 97.3 to 98.6 | yes |
| 2027 list | 12 hubs | 12 under the uptime-clock reading | yes |
| Seven programme hubs forecast | below 99 | 97.9 to 98.6 (hub attendance) | yes |
| 30 hub charge counts | 87,070 total | all 30 reproduce under the stated join rule | yes (rule not filed in a file) |
| 30 hub energies (MWh, 1 dp) | 2,807.9 total | all 30 reproduce from first opening to last closing register | yes |
| Nearest rounding line | none | every hub at least 0.0013 MWh away on register span | yes |

## Competing answers that survived
- **Own-rate and pooled-rate readings (a, b):** list the five hubs only. Ruled out by the data: they cannot produce the sharp 76-day onset or explain why exactly the five hubs lack the RC50 power-down. This is the intended wrong answer, not a fork.
- **Jan to Oct 2026 carried (d):** 8 hubs (five plus NM106, NM109, NM152, all single long hardware faults). Ruled out: it ignores the programme asset base that the prompt names.
- **Attendance pooled across hubs, my view:** the judge calls this a fork surviving "only an unreasonable choice". From its table:
  - by-group attendance (1,906 min) puts the seven programme hubs at 98.87 to 98.96 (still below 99);
  - fleet attendance puts them at 98.5 to 98.6;
  - hub attendance puts them at 97.65 to 98.76.
  
  So pooled attendance alone does not move a hub across 99. The set holds under every attendance reading. The nearest margin is 0.04 to 0.1 points.
- **Pooled supply-interruption rate combined with by-group attendance, the real residual fork:** NM150 reaches 99.03 (leaves the list) while NM125 (98.94) and NM162 (98.86) enter it, so the list changes. I rate it ruled out, not competing. NM125 and NM162 carry about 26 logged interruptions each over 3.8 years (about 6.8 a year) against a few at the other hubs, so a pooled rate overwrites a plainly hub-specific, shipped record. The design note's SF12 closes the last-twelve-months rate, not a pooled one.
- **Risk to record:** three hubs sit within 0.1 point of 99 under the softer attendance reading. A reviewer who pools both inputs would get a different list.
- **Register-jump join (asks):** not written in any file. It follows from Schedules 6.2 and 6.3 (1,924 records open above the prior closing register, all HX150, blank id tag, 6 to 20 minute gaps). A solver who counts rows gets 88,994 charges and about 2,781.7 MWh. The judge's cold derivation missed it before it saw the blocks. This is the asks' device, a wrong answer rather than a licensed alternative, but it is a filed-rule gap. See finding 2.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 10 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 or more rows | sessions csv 106,918 rows | yes |
| Distractors in metadata.json | 2 or more, none labelled in a file name | customer_survey_2026.xlsx, tariff_schedule_2026.pdf, neither named as a distractor | yes |
| Distractors weigh but are unused | relevant, no graded answer | survey and tariff carry no availability figure (design note and judge) | yes |
| Deliverables | 1 to 3, all in the golden | 2 (CSV, PDF), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 30 hubs x side, charges (whole), energy (MWh, 1 dp); stated in the prompt | yes |
| Prompt shape and criteria | identifiable, 25 or more | 578 characters, one paragraph, question first, no count the data hold; 30 hubs x 3 fields plus the list gives well over 25 criteria (the generated rubric was not inspected) | yes |
| Reads as real, no LLM tell | none | judge found no authoring or provenance leak; goldens not otherwise audited here | yes |

## Gate G reconciliation
The thread says mechanism forecasting, stumping_family method_selection, surface_read_dependency no, sole_data_defect no. The design note's stump sentence and the card (stump_class analytical) say the hang clock and the removed power-down regime, estimation_fit. These match. The declared distractors (survey, tariff) are not named as the surface read, so they are not too load-bearing. The easy route, own or pooled rate, files 5 hubs and misses 7.

Gate H: the thread gives domain pass, layers pass, decisive_step analytical. The design note's `## Three rules` has no decoy, not semantics and not rule application, all present and consistent. The decisive step (the restart clock, then the programme regime) is not filed anywhere and the data separate the candidates. Not a textbook-method landing: the judge's route needed the RC50 work orders linked to the HX150 Offline rows.

## Stump power (Gate F)
Strong, with the caveat that the stumping is on the main call and the asks bank the rest. Design note rungs 0 to 0g reach the golden at 0 of 7 and the standing family at 6 of 6. The judge recomputed that rates, pooled rates and the 2026 carry give 5, 5 and 8 hubs. A strong solver must find the 76-day onset from the status history. The prompt's "asset base" phrase hints at the RC50 but names no mechanism. The design note's ladder and the judge agree.

## Findings, ranked
1. Margin claim in the design note does not match the recompute. SF4 and the closure table say "no forecast sits within 0.3 of 99", and checks.py reports 0.21 at the closest. The judge's own table has hub-attendance forecasts at 98.74 to 98.76 (0.24 to 0.26) and group-attendance forecasts at 98.89 to 98.96. SF13 asserts the fleet attendance gives the same set, true for 2,374/3,024 (98.5 to 98.6), but the 1,906 by-group variant was not asserted. Add the group-attendance and pooled-interruption variants as asserted forks (the first holds the set, the second is ruled out by the 26-versus-few interruption record) and correct the 0.3 wording to the measured 0.21.
2. The register-jump join and its basis (Schedules 6.2 and 6.3) is not in the solution steps in a form a grader can accept. State it in step 6.
3. CRITICAL_COMPONENTS 1 says 84 hangs; the data give 83 with a prior power-up on record (90 in all). Restate.
4. No file or filing problem found; the judge's hygiene check passed.

## Next action for the author
Edit the design note's SF4 and SF13 rows to the measured margins and add the two variants; state the register-jump join in the solution steps and correct the hang count to 83 (90 including 2023 Q1). No rebuild and no re-judge. Then proceed to ship.
