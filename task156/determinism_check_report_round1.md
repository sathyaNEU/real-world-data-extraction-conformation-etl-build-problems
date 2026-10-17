# Verdict: task156 (paid moderator FTE request for 2027)

- **Verdict:** DETERMINISTIC for the main recommendation and supplementary answers 1 to 5. Supplementary answer 6 (2026 against 2022 questions) has an open fork, and slide 2 is under-specified, so the overall verdict is DETERMINISTIC with two reportable defects (below). No SOLUTION_WRONG: every graded figure I could recompute reproduced.
- **Disposition:** FIX_NOW. Pin the 2022 question-count semantics in the shipped notes (one sentence in moderation_ops_notes.md or posts_warehouse_notes.md, or the workbook footnote), and pin what "paid review hours" on slide 2 means (flags included or not, which close-vote standard prices 2024 to 2026). The main call and its inputs stay untouched, so no model rerun is needed for the main call.

## Why
The 35-FTE request is forced by the files. Volunteer reviewers cap at about 40 reviews a month (old workbook, saturated months of every site: about 40.0; platform export, saturated site-months of Security, Embedded and Scientific Computing: 39.4 pooled). Every pool loses about 2.05% a month with almost no new reviewers (roster). Carried through 2027 against plan questions times inbox per question, the pools fall below the inbox at Data & ML, Databases, Infrastructure & DevOps and Game Development. The easy route (trailing routed share, or last-12-months paid hours per question on the plan) gives 21 to 23 FTE, below the 26-FTE envelope, which is the wrong side of the call. Supplementary 6 is the weak point: it reproduces only under an unstated reading of how the old statistics job counted moved questions (gate C/E on a supplementary answer, label underspecified_objective).

## Evidence (recomputed from the bundle)
Literal reading: the charter fixes need = flag hours + routed-item hours at the year's standards, priced on UTC entry year, including future posts; the method for routed items is left open. Silent options: pace, attrition, the start pool, the floor of routing at covered sites.

| Item | Result | Reproduced |
|---|---|---|
| Pace of reviewers | roster/inbox saturated site-months (34, >5% routed): pooled 39.40, median 39.36; old workbook saturated months about 40.0 | yes, "about 40" |
| Lapse rate | 2.04 to 2.09% a month on every site; new reviewers 0 to 0.67 a month | yes |
| Flags handled per question | stable 2024 to 2026 per site (web 0.156, data 0.140 ...) | yes |
| Need by site, my model (pace 40, 2% lapse, pool from Sep 2026 decayed to Jan 2027, 0.6% routed floor where covered) | Web 5.33, Mobile 1.85, Data 6.54, Databases 4.74, DevOps 4.61, Game 1.90, Security 3.74, Embedded 2.94, SciComp 1.86 = 5, 2, 7, 5, 5, 2, 4, 3, 2 = 35 | yes, matches the golden site by site |
| Robustness | total stays 35 for pace 39 to 40.4, lapse 2.0 to 2.05%, start pool by active-in-September or by roster status (3 decays), per-site pace. It moves to 32 at pace 41, 31 at 42, 37 at 38 | stable over the range the data supports |
| Covered sites | Web and Mobile peak utilisation 0.93 to 0.94 in Oct 2027, still covered; Data starts short in Jan 2027 (1.03) | yes |
| Easy routes | no shortfall: 21; trailing-12-month routed share: 23; the 2027 close-vote standard (2.0 against 5.0) does not change the rounded total (35 either way) | confirms the stump is the supply constraint |
| Envelope gap | 35 - 26 = 9; 26 x 1600 / 12 = 3,467 h a month | yes |
| Supp 4 (24-hour flag shares) | all 27 cells match: dedupe the 418 flag ids repeated across the two exports, take first action from flag_decision_reviews (the flag export's handled_at is overwritten by the final review time), drop closed_post_deleted | yes (naive handled_at gives about 4 points lower, so this is a real step) |
| Supp 5 (WFM hours) | all 27 cells match: approved lines only, site from moderator_site_assignments by shift date (WFM site is backfilled with the current assignment, 760 lines disagree), Ops & Cloud renamed, quarter by local start | yes |
| Supp 6 (2026 against 2022) | all 9 match only if each question moved out of a site (asked Jan to Sep 2022, per question_moves) is subtracted from that site's workbook count, Graphics & Shaders added to Game Dev | reproduces, but see the fork |

Fork on supp 6. Workbook footnote: "questions posted on the site in the month". The warehouse note says questions count once, on the site they are on today. No shipped file says the old job counted a moved question on both sites. The golden assumes it did (from the new_question_id column in the moves log). Three readings are licensed, one decimal apart or more:

| Reading | Web | Mobile | Data | Databases | DevOps | Game | Security | Embedded | SciComp |
|---|---|---|---|---|---|---|---|---|---|
| Golden: subtract moved-out | 39.7 | 42.1 | 55.5 | 58.4 | 60.2 | 53.8 | 72.0 | 76.0 | 76.8 |
| Net move (workbook counts once, on the posting site) | 39.5 | 41.8 | 55.2 | 58.0 | 59.9 | 53.5 | 71.5 | 75.5 | 76.3 |
| No restatement | 39.5 | 41.8 | 55.3 | 58.1 | 59.7 | 53.3 | 71.1 | 75.5 | 74.8 |

Every cell differs at one decimal, so a careful solver who reads the footnote literally files a different table. This is a data-semantics ask, which is allowed for asks, but it is not forced by the files.

Slide 2 (supp 8). The prompt says "monthly paid review hours". The files do not say whether that includes moderator-flag hours, which standard prices Jan 2024 to Dec 2026 (close vote 5.0 in force until 31 Dec 2026, 2.0 from 1 Jan 2027), or how Oct to Dec 2026 is projected. The golden describes the chart only qualitatively, so I could not recompute its plotted values. Treat as under-specified until the series is pinned.

## Files/Hygiene
PASS. 24 input files; formats csv, xlsx, pdf, md; files of 36,144 rows (inbox), 19,391 (roster), 49,530 (moves) and others above 25,000. Row counts in pool_request_files_2026-10-09.md match the files. Distractors present and unused by the solution: member_survey_2026_ai_assistants.pdf, pageviews_by_site_month, the 2 October September pull (stale: 1,764 open items, final export has none), plus the used-for-asks flag_service_standard.pdf. Temporal coherence holds (letters 30 Sep, pulls 8 Oct, listing 9 Oct). Mild tell: routed share by item type is near-identical within each site and period, and the 2021 to 2023 workbook is very regular, which reads synthetic. Not exclusion-level. No authoring or benchmark language found in the files I read. The brief forbids metadata.json, so licence and source records could not be checked.

## Stump power
Good. A strong model that builds a clean routed-share, trailing hours-per-question or trend forecast lands on 21 to 23 FTE and recommends staying within the 26 envelope, while the right answer is 35. Reaching 35 needs the reviewer-pool attrition model and a pace taken from saturated site-months (about 40), and it must not be taken from the covered sites (about 20 to 32 reviews a reviewer a month, which would imply no shortfall). I expect most capable runs to miss it. Margins are clean at every rounding boundary for the supported pace range (nearest: DevOps 4.61, flips only above pace about 40.5; Databases 4.74).

## Stumping type
`mechanism: binding_constraint`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported counts are all correct; the difficulty is a capacity-constrained forecast (shrinking volunteer supply against a stable inbox), and it would still stump on perfectly clean data. Passes Gate G.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: workforce capacity planning for a review operation (attrition, throughput ceiling, handle-time pricing); the deciding quantity is a supply-limited demand forecast, not a stated score. Swap test: "reviewers" and "inbox" cannot be swapped for another field's nouns without changing the analysis. Layer 1: renamed sites and a merged site, an old workbook against a new platform export, overlapping flag exports, a stale September pull, UTC against Toronto time, superseded WFM lines. Layer 2: modelling when the volunteer pool stops covering the inbox. Easy route a strong analyst would take after reading everything correctly: extend the routed share or paid hours per question (clean data, correct rules), which gives about 23 FTE and a recommendation under the envelope.

## Fix
- Supp 6: input_files (or solution). Add to moderation_ops_notes.md that the old statistics job counted a moved question on both sites (or restate the workbook footnote), so the subtract-moved-out reading is the only licensed one. Otherwise change the golden to the reading the files support.
- Slide 2: prompt/solution. State whether the series includes flag hours and which standard prices Jan 2024 to Dec 2026, and list the plotted monthly values in the deliverable answers so the slide is gradable.
- Main call, supp 1 to 5: none.
