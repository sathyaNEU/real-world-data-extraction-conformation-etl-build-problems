# determinism-check report, task260, 2026-10-15

## Verdict
NOT_DETERMINISTIC (competing_defensible_answer on supplementary ask 4, the Lumidra Detect first-year cost only). The main recommendation (license Halvic Breast) is forced and reproduces.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call reproduces and is robust: only Halvic's interval, with readers and examinations both random, lies wholly above zero, and the ranking holds under OR, DBM and a two-way bootstrap. The Lumidra figure of £101,565 rests on a 28-day episode rule that no shipped file states; the Lumidra quote says only "one woman's screening, including any technical repeat". The golden also silently leaves out 14 women whose only window study is an early-October 2025 technical repeat (MAMT). Three readings are licensed by the files and the prompt asks for whole pounds, so they give different answers.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Gain, Lumidra (reader_study exports, last submission) | 0.047 | 0.04722 | yes |
| Gain, Ondrix | 0.042 | 0.04201 | yes |
| Gain, Halvic | 0.026 | 0.02593 | yes |
| Halvic interval (OR/DBM, Hillis df) | wholly above 0 | 0.0136 to 0.0383 | yes |
| Ondrix interval | crosses 0 | -0.0129 to 0.0969 | yes |
| Lumidra interval | crosses 0 | -0.0148 to 0.1092 | yes |
| Screening studies, 4 sites (RIS + mobile visits) | 11,569 / 7,298 / 13,253 / 13,758 (45,878) | same | yes |
| Film readers 1 Apr 2027 | 27 | 27 | yes |
| Ondrix cost | £89,122 | £89,122 | yes |
| Halvic cost | £101,750 | £101,750 | yes |
| Lumidra episodes / cost | 44,262 / £101,565 | 44,262 / £101,565 under the golden reading only | partly (fork) |

## Competing answers that survived
| Fork | Answers | Closing rule shipped |
|---|---|---|
| Lumidra episode population and window | distinct women with any screening study (44,276, £101,594); 28 days by timestamp (44,263, £101,567); golden, episodes opened by a routine study in the calendar-day window (44,262, £101,565) | none: the quote gives no 28-day rule and no window rule for a technical repeat |
| Mobile-unit host (ask 2, residual) | dated visits file (golden: 11,569 / 7,298 / ...) against the static `host_site` in screening_locations.json (WDL 12,450, CRB 6,417) | the dated visits file is the better source but no "as at" qualifier is shipped on the json field |

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | 4 (PDF, XLSX, CSV, JSON) | yes |
| Large file | 25,000 rows or more | RIS 55,920 raw rows | yes |
| Distractors in metadata.json, none named in a file | 2 or more | 3 (vendor summaries, KPIs, self-assessment) | yes |
| Distractors unused yet weighable, ruled out by a shipped fact | yes | vendor AUCs ruled out by protocol 3.1 and 3.2 | yes |
| Deliverables | 1 to 3, all in golden | 3 present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | yes (three decimals, whole pounds) | yes |
| Rubric 25 or more criteria, prompt shape identifiable | yes | not generated at this stage; per-tool, per-site and per-cost items give well over 25 | not checked |
| Reads as real, not LLM generated | yes | judge found no authoring or provenance leakage | yes |

## Gate G reconciliation
Judge: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The stump is the choice of unit of analysis (readers and examinations both random); a reader-level paired test makes Lumidra qualify and win. The declared distractor (vendor summaries) is inert and does not carry the call. Gate H: domain pass, layers pass, decisive_step analytical. The design note's Three rules lines (No decoy, Not semantics, Not rule application) are present and consistent with this read: the protocol files the estimand and leaves the interval construction to the analyst. The design note's own fork table (row B, D1) lists the 28-day episode rule as a closed fork, but the judge found no shipped text that closes it. The card carries stump_class analytical with an analyst_test and domain_test naming the OR/DBM interval, matching the judge. No mismatch on Gate G or H.

## Stump power (Gate F)
Good. Only the two-source analysis licenses Halvic; one-factor intervals file Lumidra or Ondrix. Halvic's lower bound is 0.0136 and the other two cross zero under every method tried, so the margins are not knife-edge.

## Findings, ranked
1. Ask 4 Lumidra cost is open (44,262 / 44,263 / 44,276 episodes, £101,565 / £101,567 / £101,594). FIX_NOW.
2. Ask 2 mobile-unit host basis has a residual semantic risk (static `host_site` against dated visits). Optional pin.
3. Minor: MBS-AI-02 unaided-to-aided gap is about 27 days for at least one reader against the protocol's "at least four weeks". It does not touch the decision.

## Next action for the author
Pin the episode count basis in the Lumidra quote wording or the prompt (for example "screening episodes whose routine study falls in the 12 months to 30 September 2026; a technical repeat belongs to the routine study it repeats") so that 44,262 and £101,565 are forced, optionally pin the host-by-date basis for mobile units, assert both in `checks.py`, rebuild, and re-judge once. Do not touch the reader-study files or the main call.
