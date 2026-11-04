# determinism-check report, task210, 2026-11-04

Architecture 2 (Ashcombe Regional Transit's streetcar, the four January to February 2027 restricted-speed slots).

## Pass 1 (target.zip 1c38083e, judge thread run by the coordinator)

**Verdict:** NOT_DETERMINISTIC on two supplementary asks. **Disposition** as labelled by the thread: SEND_BACK. Read
against the gate table (determinism-check, a disposition is read against the gate table, not taken on its label): the
main call is forced and correct (the thread reproduced the four slots from sun geometry), Gate F high, Gate G
forecasting and analytical_non_defect, Gate H analytical. The failures are Gate C and E on the asks: the emergency-brake
ask's "in revenue service" read two ways (the yard sheet's block assignment, 707, against the AVL passes, 666), and the
defect-card ask counted cards on a re-dated day no file explained, with the weekday holidays and per month against the
period open. An ask-layer repair, no architecture spent. Closed in one generator pass in the world: every non-depot
application on a block-assigned car now falls inside its block's pull-out to pull-in window, SRM-07 6.2 files the WHAT
(in service from pull-out to pull-in, the post-release depot test excepted, a two-car train's two records one
application), the ask re-sited to seven monthly totals; no card's car runs its block on the day the card was entered,
the MMS export's date columns carry entry semantics, the run sheets carry each day's timetable, and the asking sentence
files the day written, the weekday timetable and the period as a whole. The main call did not move.

### The thread's verdict, verbatim

# Verdict, task210 (determinism judge)

Order kept: yes. derivation.md was written from prompt.txt and target/ alone (literal reading, forks, my own EB and card figures, my own slot ranking) before graded_blocks.md or graded/ was opened. Everything after that was recomputation against the bundle. Nothing outside the judge folder was read.

- **Verdict:** NOT_DETERMINISTIC (the main recommendation is forced and correct; supplementary answer 3, the emergency-brake counts, is not forced; supplementary answer 4 is correct but rests on an unstated re-dating and has two smaller forks).
- **Disposition:** SEND_BACK. The repair is a prompt pin on "in revenue service" (and a pin on which date a defect card is counted by); the shipped prompt changes, so prior solver runs are invalid and a rerun is required. Goldens for the main call and the chart stay as they are.
- **Why:** Gate C (and E) fail on supplementary answer 3. The prompt asks for EB "applications in revenue service" and no shipped file defines revenue service. Read against the AVL pass log (the dashboard labels AVL as "Revenue trips") the 14 figures are Juniper 40, 32, 44, 55, 48, 39, 43 and Foundry 54, 59, 49, 51, 53, 53, 46 (666 in all). The golden (Juniper 43, 34, 46, 60, 51, 42, 45; Foundry 56, 65, 53, 53, 54, 55, 50; 707 in all) counts every EB on a car assigned to a block by yard_block_sheets_2026.csv, which pulls in 41 EBs that sit 1 to 35 hours from any logged pass (for example 128-001659 on 23 May at 23:45, 5 hours after the car's last pass; 102-002489 on 20 Sept at 22:42, 31 hours before its next). Both readings are defensible and every one of the 14 cells differs between them. Taxonomy label: underspecified_objective.
- **Evidence:**

| Item | Golden | My recomputation | Status |
|---|---|---|---|
| Four slots | J4-O AM, J5-O AM, F5-O PM, F6-O PM | same four, independently, from sun geometry (my nonparametric elevation x relative-azimuth surface, pooled baseline): J4 36.3, J5 33.5, F6 31.9, F5 29.6, then J3-O AM 26.0 | reproduced |
| Bearings | J4 125, J5 131, F5 231, F6 237 outbound | same from geojson, inbound reversed | reproduced |
| Driver | low sun ahead of the operator on sun-visible passes | same: rate about 35 to 47 per 1,000 with sun under 20 degrees up and within about 15 degrees of heading, against 18 to 22 elsewhere; section baselines are homogeneous outside that zone (chi-square p = 0.33 over 52 cells); operator class, temperature, pedestrians, school days do not carry it | reproduced |
| Margin | not stated | using the golden's own kernel (cos squared, 25 degrees cut-off, 12 to 25 degree elevation fade, G 1.0 to 2.5, 68 per cent sunshine): 4th place 25.6 to 31.1 against 5th (J3-O AM) 23.9 to 26.7 | holds at every G tried |
| 52 rows, 4 yes, 38 weekdays, 68 per cent sunshine, 95 per cent of FB on a pass (11,298 of 11,955) | as stated | as stated | reproduced |
| EB by line and month | 707 total | reproduced exactly (all EB less 60 depot-release tests less 29 trailing-car duplicates, service-day or clock month give the same figures) | reproduces only under the block-assignment reading; pass-based reading gives 666 |
| Defect cards, Apr to Oct | J brakes 55, doors 56, other 153; F 37, 46, 139 | reproduced exactly by re-dating each Operator card to the latest earlier day (never the keyed day) on which its car pulled out on its block, keeping Monday to Friday days that are not the three Sunday-timetable holidays | reproduces only under that re-dating |

Forks I can show:
1. Ask 3, revenue service: AVL-pass reading 666 against block-assignment reading 707 (table above).
2. Ask 4, the date a card is counted by: the card's own `reported` date (equal to the keyed date) gives Juniper brakes 70, doors 72, other 183 and Foundry 50, 55, 177 (all weekdays Apr to Oct, one November card dropped). The golden's figures need a back-join from the card's block and car to the yard sheet; it exists in the data (the card block disagrees with the yard sheet on the reported date for 540 of 608 cards, and matches one to five days earlier for all 608, never on the keyed day among the 540 unambiguous ones), but the prompt never says cards are keyed late. The 68 cards with two candidate days (lag 0 and lag 1 and similar) are resolved only by inferring that no card is keyed the same day: latest-including-same-day gives Juniper 58, 58, 156 and Foundry 39, 48, 143.
3. Ask 4, "weekday service days": counting the three holidays that ran the Sunday timetable as weekdays moves Foundry other 139 to 141 and Juniper brakes 55 to 57.
4. Ask 4 reads "in those months" and the golden answers with Apr to Oct totals per line; a per-month table (as in the EB ask) is an equally natural reading.
5. Main call: a per-cell baseline fitted to Apr to Oct, or a crude glare box (sun under 25 to 30 degrees, within 25 to 30 degrees of heading), puts J3-O AM and J2-O AM into the four in place of F5/F6-O PM. The data reject both (homogeneous baselines, p = 0.33; the likelihood prefers a narrow window), so this is a method error, not a surviving answer.

- **Files/Hygiene:** PASS. 18 files; formats csv (12), parquet, pdf (3), geojson, xlsx; AVL parquet 623,550 rows, EDR 13,921 rows. Distractors present and unused (pedestrian counts, school calendar, arena events, maintenance log, the dashboard workbook, temperature). Realistic noise: UTC against local time, a reissued badge per operator, trailing-car duplicate EBs, depot brake tests, a seven-day AVL gap on F3 and F4, mm/dd/yyyy yard dates, cards keyed days late. No authoring or provenance leakage found; dates coherent (SRM effective 1 Oct, timetable issued 2 Nov, data to 31 Oct). The dashboard workbook shows a flat 19 per 1,000, so no file states the answer. No exclusion-level finding.
- **Stump power:** High on the main call. The easy routes all give a wrong slot set: rank by September to October rate (J3-O AM 45, J2-O PM 34, J5-I PM 32, in the chart's own data), carry the autumn pattern forward by month or hour, or blame the 26-3 operator class or pedestrians. Only the sun-geometry projection onto the January and February passes lands on J4/J5-O AM and F5/F6-O PM. The two ask groups add exposure, but Ask 3 would stump on its fork, not on analysis.
- **Stumping type:** `mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported rates and the dashboard are correct; the difficulty is a physical driver that must be found and extrapolated to an unobserved season, and it would still stump on clean data. Passes Gate G.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test: sun-glare exposure of a given section bearing at the timetabled minutes of a winter pick is a rail-safety hazard assessment and does not survive swapping the nouns. Layer 1: UTC/local, badge reissue, duplicate recorder records, depot tests, AVL gap, late-keyed cards. Layer 2: expected rate from the mechanism at out-of-sample sun positions. A strong analyst who cleaned everything and read SRM-07 correctly could still rank by the autumn rates (or fit the seasonal pattern) and file J3/J2-O instead of J4/J5-O AM and F5/F6-O PM.
- **Fix:** prompt. (a) Pin the EB population as what is meant, for example "on a car running a block at the time (not a depot release test), a two-car train's two records counted once", or equivalently "while a logged section pass was in progress", and rebuild the golden figures to whichever is chosen. (b) Pin the card date as the day the operator wrote the card (not the day it was keyed) or state the lag, name whether holidays on the Sunday timetable are weekday service days, and say whether the counts are per month or for the period. The main call, ladder, chart and slot plan need no change. File the WHAT (population and date), not the method.

## Pass 2 (target.zip 0d608249, judge thread run by the coordinator, round1_findings.md opened with the graded blocks)

**Verdict:** DETERMINISTIC. **Disposition:** APPROVE. Every committed answer reproduced by an independent route: the
four slots, the seven monthly applications and the six defect-card counts. Its optional wording fix (name the sun as
the driver that moves between rows and the newly qualified class as a transient, direction-neutral minor part; say the
rates are counted on logged passes) was applied to the write-up before the ship; target.zip did not change.

### The thread's verdict, verbatim

# Verdict, task210 (round 2)

Order kept: target.zip unzipped and read in full; derivation.md written from prompt.txt and target/ alone (literal reading, silent-text options, own figures and own top four); only then graded_blocks.md, graded/ and round1_findings.md opened. Round 1 findings treated as context only.

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. One optional wording fix in the solution blocks (see Evidence, attribution note); no input or prompt change, no rerun.
- **Why:** Every committed answer reproduced from the shipped files by an independent route: the four slots (AM J4 outbound, AM J5 outbound, PM F5 outbound, PM F6 outbound), the seven monthly EB counts and all six defect-card counts match the golden exactly. The decisive quantity (expected rate in the Jan/Feb peaks) is forced by a likelihood-selected sun-glare mechanism whose geometry (survey coordinates, timetable times, normals sunshine share) is fully in the package, and the fourth to fifth gap survives every reasonable glare specification the data does not reject.

## Evidence (recomputed from the bundle)
| Item | My value | Golden | Source |
|---|---|---|---|
| EB in service by Mountain month Apr..Oct | 99, 99, 99, 113, 105, 97, 95 (707) | same | edr export; yard_block_sheets (out/in, swap split by AVL vehicle); foundry_depot_releases; SRM-07 3.4 and 6.2 |
| Juniper brakes/doors/other | 46 / 55 / 171 | same | mms (Operator card, written day found from car+block run record), run_sheets schedule, block prefix |
| Foundry brakes/doors/other | 44 / 34 / 122 | same | same |
| Slots | AM J4 OB, AM J5 OB, PM F6 OB, PM F5 OB | same four | avl parquet, edr FB, geojson bearings, AWOS skyc, normals PDF, pick timetable PDF |
| Bearings | J4 125, J5 131, F5 231, F6 237 outbound | same | geojson |
| FB on a logged pass | 94.5 percent of 11,955 | 95 percent | edr + avl |
| Sep-Oct observed rows in the png | AM J3 OB 45.0, PM J2 OB 34.0, PM J5 IB 32.9 (AVL-only) | bars match (45, 34, about 32) | avl + edr |

EB path details: 943 EB rows; 736 fall inside in-service windows; 207 do not (60 post-release depot tests, each exactly one EB 12 to 45 minutes after release on a car already off the block, plus 147 stopped-car EBs at the termini at 3 to 7 mph); 29 two-car pairs (same badge, same block-day, other car, within 40 s) counted once. No EB lies in the 3 to 11 minute swap gap, so the swap boundary is not a fork. UTC month attribution would move cells; the prompt pins Mountain time. Dashboard EB column (for example 130 in April) counts depot tests, off-block events and pair duplicates and is ruled out by SRM-07 6.2.

Defect-card path: operator cards are keyed on the next weekday morning (06:35 to 09:40), so the car+block run record gives exactly one earlier day for all 558 cards; 472 fall on weekday-timetable days written 1 Apr to 31 Oct (25 May, 3 Jul, 7 Sep ran the Sunday timetable). Alternatives and what they give: entered_date basis Juniper 53/62/201, Foundry 50/38/149; no timetable filter Juniper 53/62/202, Foundry 52/38/151. The prompt says "the day it was written" and "only if the weekday timetable ran that day", which excludes both alternatives by its own wording, and the entry time of day proves the card cannot have been written that morning. No file states the keying habit, so the inference is the solver's, but it is unique and data-forced.

Main call model (own fit, weekday passes, Poisson): reserved track J6/F7 about 0.4x; peaks about +13 percent; new-operator weeks 0 to 10 about x1.2; glare x1.8 to 2.4 when the sun is within about 20 degrees of the heading and under about 20 degrees up (sunny), about x1.4 with cloud. No effect found from temperature, wind, visibility, two-car running, arena events, school days, pedestrian counts or track possessions (all distractors). Jan/Feb prediction (38 weekdays, MST sun, 68 percent sunny, rookie term zero): AM J4 OB 37.5, AM J5 OB 34.0, PM F6 OB 32.4, PM F5 OB 30.3, then AM J3 OB 28.0, PM F3 OB 26.3, AM F4 IB 24.8; golden chart shows about 42, 37, 41, 37 versus J3 OB about 27. Sensitivity: identical four across 7 binned-angle specifications and p(sunny) from 0.5 to 0.8; across a 36-cell grid of rectangular cone widths the best-fit cell (20 degrees azimuth, 20 degrees elevation, log-likelihood 45430) gives the four; wide cones (25 degrees azimuth or more) bring AM J3 OB level with or above PM F5/F6 but are rejected by the likelihood by 10 to 25 units. So the margin is thin only under mis-specified models the data refutes; under the data-selected model the gap is 8 percent in my weaker-effect fit and about 10 points in the golden. Competing answers: Sep-Oct top rows (AM J3 OB, PM J2 OB, PM J5 IB, AM F4 IB) or pooled Apr-Oct (AM J2 OB, AM F3 IB, AM J3 OB, PM F5 OB): both are the easy routes, not licensed answers.

Attribution note (minor, solution blocks only): the golden says the rise "was the low sun". My fit finds a smaller but significant second driver, the 26-3 cohort (qualified 31 Aug) at about x1.2 in its first 10 weeks, and the Sept peak is about 11 percent above even the sun-plus-rookie model (Sept non-glare passes +13 percent), so "rose because of the sun" slightly overclaims; the slot answer is unaffected because rookies fade by January and are direction-neutral. Suggest the blocks say the sun is the driver that moves between rows and add the cohort as the minor, transient part.
Also minor: the golden numerator and denominator use logged AVL passes only; AVL omits about 5 percent of scheduled trips (5,067 scheduled trips absent; most of the 5.5 percent of FB outside any logged pass fall in those windows). Rates barely move; ranking unchanged.

## Files/Hygiene: PASS
18 files; formats: csv (11), parquet, xlsx, geojson, pdf (3), five formats; one file of 623,550 rows plus a 14,068-row recorder export. Distractors: arena events, pedestrian counts, school calendar, maintenance log, dashboard workbook, roster-class labels (all weigh but decide nothing). No README, no benchmark or authoring language, no hidden sheets. Minor tooling signatures only: parquet created_by parquet-cpp-arrow; the pick-timetable PDF metadata date (27 Oct 2026) precedes its stated issue date (2 Nov 2026); SRM-07 and the timetable are plainly written for the task (prose defining terms) but read as procedure documents. Nothing exclusion-level, no public-data contamination.

## Stump power
Good. A strong solver can read every file correctly and still file Sep-Oct top rows or pooled rows, because the mechanism (sun versus heading, not stated anywhere) has to be found and extrapolated to a season never observed; the normals definition of possible sunshine and the AWOS sky field point to it without naming it. Asks add independent traps (swap-in cars, post-release tests, two-car pairs; reconstructing the written day, Sunday-timetable holidays). Risk of too hard rather than too easy; the sun term shows plainly in a residual-by-heading check.

## Stumping type
mechanism: forecasting (out-of-season expected-rate model, with method selected by fit); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no. The reported rates are correct; the difficulty is the structural driver and its seasonal shift, and clean data would still stump.

## Three rules
domain: pass, layers: pass, decisive_step: analytical.
Field analysis: expected-rate assessment for seasonal hazard control (glare as a human-factors exposure at the pick's own times and normal weather), which swap-tests badly (megawatt-hours or visits would not give a sun-heading structure). Layer 1: UTC against Mountain time, reissued badges, AVL dropouts, yard sheets listing only the pull-out car, mixed date formats. Layer 2: modelling the low-sun glare against heading and extrapolating to Jan/Feb. Easy route: take the highest Sep-Oct rows (AM J3 OB 45, PM J2 OB 34) or pooled rows, which gives J3/J2/F3 rows instead of J4, J5, F5, F6. No planted decoy decides it, the answer does not flip on a field reading, and no stated rule is executed.

## Fix
none (optional, solution): soften "the rise was the low sun" in FINAL_RECOMMENDATION and critical component 2 to name the sun as the row-moving driver and the 26-3 cohort as a transient minor contributor; state that FB and passes are counted on logged AVL passes.
