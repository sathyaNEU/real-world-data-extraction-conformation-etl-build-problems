# Verdict, task156 (re-judge)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed and no model rerun. Two optional hardening notes are in Fix.

**Why:** Every committed answer reproduced from the shipped files. The main call (35 FTE, 9 above the 26-FTE envelope) follows from the filed estimand: charter section 4 need, the 2027 standards, the 2027 question plan and the finance envelope. The method is not filed. The data forces it: sites that already ran short of reviewers show a volunteer ceiling of about 40 reviews a reviewer a month, every site's pool loses about 2.05% a month with almost no new arrivals, and the 2027 inbox outruns the pool at Data & ML, Databases, Infrastructure & DevOps and Game Development. Doing it the easy way (last-twelve-months routed hours per question carried onto the plan) gives about 23 FTE, so the golden is not what the easy route files.

## Evidence (recomputed from target/)

Main call model (inbox, roster, flags, plan):

| Item | Recomputed | Source |
|---|---|---|
| Volunteer pace in site-months with routed share >5% (Jan 2024 to Sep 2026) | pooled 40.2, mean 40.4, sd 1.2 (34 site-months: Security 39.9, Embedded 39.9, Scientific Computing 41.4) | review_inbox_daily (complete 8 Oct pull) over roster-derived active reviewers |
| Same pace in the 2021 to 2023 workbook, routed share >5% | mean 39.9, sd 1.1 (55 site-months, 7 sites) | review_queues_monthly xlsx, Volunteer reviews / Active reviewers |
| Monthly lapse rate | 2.03% to 2.09% on all nine sites, same for either window | reviewer_roster (last review month vs active reviewer-months) |
| New reviewers a month, last 12 months | 0 to 0.75 per site | reviewer_roster |
| Sep 2026 active reviewers | 10,131 = rows with status active; per site web 3,246, mobile 1,230, data 1,679, databases 1,419, devops 1,202, gamedev 449, security 446, embedded 266, scicomp 194 | reviewer_roster |
| Inbox items per question | stable over time (e.g. data 2.78 all windows, web 2.85); window choice changes nothing | review_inbox_daily / posts_questions |
| Handled flags per question | stable 2024 to 2026 (data 0.139 to 0.141) | modtool_flag_summary_daily / posts_questions |

Model: pool carried from September 2026 at the lapse rate plus new reviewers, capacity 40 a reviewer, routed items = inbox beyond capacity (floor 0.6% of the inbox), priced at 9.0/5.0 minutes through 2026 and 2.0 for close votes in 2027, flags at 9.0, divided by 1,600. Result, unrounded FTE: web 5.33, mobile 1.85, data 7.15, databases 5.17, devops 4.93, gamedev 2.08, security 3.90, embedded 3.04, scicomp 1.95. Rounded: 5, 2, 7, 5, 5, 2, 4, 3, 2 = **35**, matching the golden site by site. 35 - 26 = 9. Reproduced. Network hours 56,641 (35.4 FTE) before rounding.

Which sites are short in 2027: Data & ML, Databases, Infrastructure & DevOps and Game Development exceed capacity in 2027 months (peak routed share 30%, 28%, 28%, 31% in November 2027); Frontend & Web and Mobile Apps stay at the 0.6% floor all 15 months (web Oct 2027 inbox about 94.7k against capacity about 98.7k, a thin but real margin). Critical component 3 reproduced. Backtest of the capacity rule on saturated sites in 2026 is within a few percent of actual routed items.

Supplementary answers:
- Table 4 (24-hour flag response): reproduced exactly for all 27 cells (web 97.9/97.0/97.1 through scicomp 85.6/90.0/81.4). Method: both flag exports de-duplicated on flag_id (418 overlap rows identical), first action taken from flag_decision_reviews where present (2,103 flags, where handled_at in the export is the later review close), closed_post_deleted excluded, UTC month. Using handled_at naively gives 82 to 94%, different.
- Table 5 (hours by quarter): reproduced exactly for all 27 cells only when approved lines are attributed to the site in moderator_site_assignments.csv on the shift date (WFM site labels are the current site, 760 approved lines differ), Ops & Cloud mapped to Infrastructure & DevOps, quarter by Toronto start time. By WFM label web Q1 is 2,053, not 2,475. Forced by the ops notes ("the site the moderator worked for on that shift").
- Table 6 (Jan to Sep 2026 against 2022): reproduced exactly (39.7, 42.1, 55.5, 58.4, 60.2, 53.8, 72.0, 76.0, 76.8). Method: May to August 2022 restated questions replace the original, Graphics & Shaders counted at Game Development, moves log used to move the first-site count to the destination site in the asked month and to remove the duplicate counted in the move month (warehouse basis, posts_warehouse_notes). Without these steps the figures differ by 0.1 to 2 points.
- Chart (item 8): definition is filed in moderation_ops_notes (flag and routed-item hours at the standard of the year, UTC month, October to December 2026 on the outlook, 2027 on the plan); envelope 26 x 1,600 / 12 = 3,466.7, shown as 3,467. Plotted values were not rebuilt in full; the definition computes and the 2027 total is consistent with the 35-FTE model.

Literal-reading forks tested (each reasonable alternative recomputed):

| Fork | FTE by site, total | Effect |
|---|---|---|
| Pace 39.5 to 41.0 | 5,2,7,5,5,2,4,3,2 = 35 | none |
| Pace 39.0 | 5,2,8,6,5,2,4,3,2 = 37 | outside measured range (39.9 to 40.4) |
| Pace 41.5 / 42 | 33 / 32 | outside measured range |
| Routed = max(inbox - capacity, 0.6% floor) vs inbox - capacity + 0.6% on the covered part | 35 both | none |
| New reviewers 0 vs 0.17 to 0.75 | 35 | none |
| Lapse 1.8% / 2.3% (measured 2.05%) | 35 / 37 | outside measured range |
| Items per question and flags per question window (full, 12 months, 2026) | 35 | none |
| Decay starting in Oct 2026 vs one month later (pace 40.0) | 35 (data 6.74 vs 7.15) | none; with pace 40.5 and the late start it is 34, a double departure from the natural reading |
| Close-vote standard left at 5.0 | 38 | the filed standard says 2.0 from 2027 |
| Easy route: last 12 months routed hours per question times plan | 5,2,4,3,3,1,2,2,1 = 23 | the wrong answer the easy route files, 3 below the envelope |
| Easy route: trend of routed share or paid hours | below 35, for the same reason (covered sites route 0.6% in history) | wrong |

Nearest round-half boundaries: devops 4.93 against 4.5 (0.43 FTE, pace would have to be above about 41.3); data 7.15 against 6.5; the nearest of the nine is the devops boundary. The pace is a well-measured parameter (sd 1.2 over 34 site-months, 1.1 over 55 more in the old workbook, SE about 0.2), so the margin is thin on one parameter but clean, not contested.

Other checks: the 2 October September pull (open_at_pull) is superseded by the 8 October pull and is a named-by-note distractor; the plan's "2026 actual" sheet equals the warehouse Jan to Aug; the plan's 2027 year column equals its months; the survey and page views are unused (distractors).

## Files/Hygiene
PASS. 24 files; formats pdf (5), csv (13), xlsx (2), md (4), so four formats; largest file question_moves has 49,530 rows, inbox 36,144 rows. Distractors: member_survey_2026_ai_assistants.pdf, pageviews_by_site_month, the 2 October inbox pull, flag_decision_reviews partly (used only for table 4). Layer 1 mess is operational: superseded WFM lines, a stale WFM site label, old site names, a restated workbook block, a merged site, overlapping flag exports. No authoring language found in the memos or notes. Dates are coherent with an October 2026 setting. Minor: pool_request_files_2026-10-09.md reads as a manifest with row counts; plausible as an ops handoff note, not a finding. No exclusion-level finding. Cross-batch check: other task folders are outside this judge's readable set, so no clone comparison was run.

## Stump power
Medium to good. A strong model that cleans everything and reads every rule will still price the routed items it sees in the last twelve months (about 23 FTE, below the envelope) unless it notices that the sites with no routing are sitting at the same pace as the saturated sites and that the reviewer pool is shrinking at 2% a month. Both are discoverable in the roster and the workbook, but nothing in the prompt names them, so the trap should catch routes that extrapolate the history or the share.

## Stumping type
`mechanism: binding_constraint` (forecast with a measured volunteer ceiling), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported figures are correct; the difficulty is projecting the routed items from a capacity ceiling the history only shows at three sites. On clean data it would still stump. Passes Gate G.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1: stale WFM labels and superseded lines, restated workbook months, overlapping flag exports, old site names, a merged site, two inbox pulls. Layer 2: workforce capacity planning, with attrition of the reviewer pool and a measured throughput ceiling deciding which sites overflow to paid staff. Swap test: with another field's nouns the capacity and attrition quantity would not read the same; it is a staffing and queue-capacity estimate. Easy route a strong analyst takes after reading everything correctly: price last twelve months' routed items per question onto the plan, giving about 23 FTE, 3 below the envelope, instead of 35, 9 above.

## Fix
none. Optional, no rerun needed: (1) keep "about 40" in the solution as is; do not state a more precise pace in any deliverable, since 41.3 or above would move devops. (2) Note in the solution that supplementary tables 4 to 6 each depend on a named method step (first action from the decision reviews, assignment history by shift date, warehouse-basis restatement), which the data supports and the ops notes file.
