# task118 determinism check (wave-1 redesign)

Isolated judge on the shipped bundle (prompt.txt, target.zip unzipped, the submission's blocks). Pass 1 on the first rebuilt pack, 2026-10-12.

## Pass 1


- **Verdict:** DETERMINISTIC. The one wording defect in the solution blocks is that SOLUTION_STEPS step 2 says "within 2%". It reproduces only as within 0.2 percentage points, not as 2% relative.
- **Disposition:** FIX_NOW. Restate the back-test tolerance as 0.2 points. Tell graders that the 1,250,000 / 450,000 figures sit about 5,000 from a 50,000 rounding edge under some defensible estimators (see Evidence), and so should carry a tolerance of one rounding step. The shipped files and the prompt stay byte-identical, so no rerun is needed.
- **Why:** Every committed answer reproduces from the shipped files. Culture·national wins on shrunk lift (1.78%) times click exposure on its own surfaces that its desk has not already tested (70.31M clicks), which gives 1.25M. Local·metro follows at 0.81M. Every route to a different desk (raw lift, all-source clicks, no tested-article exclusion, readers) uses a number or convention that a shipped file contradicts. The desk and runner-up hold under every shrinkage estimator that survives the change-log back-test. Cross-batch check: I could not run it, because the sandbox lets me read nothing outside the review directory, so it is not done.

## Literal reading (before the gates)

| Open term | Literal readings | Answer each gives | Closed by |
|---|---|---|---|
| Lift per test | (a) dashboard raw: shipped CTR over control minus one, zero if kept (filed). (b) shrunk to a prior | (a) gives Sport·metro 2.76M on own-untested clicks. (b) gives Culture·national 1.25M | `headline_squad_change_log.xlsx`: raw average lift of 2.5 to 3.9 against realised holdback lift of 0.7 to 2.6. Back-test errors for the all-variant EB prior are at most 0.14 points. A zero-mean prior fails (up to 0.30 points). A prior that counts kept controls as zero fails (0.27 to 0.44). Raw lift misses by 0.72 to 1.83 points. |
| Which clicks the lift moves | All article clicks, or only surfaces that render the live headline. The sources that carry `canonical_headline` are partner_apps, search, social, discover, newsletter and alerts. | All clicks gives Business·national 3.59M untested, or 6.18M if tested articles are not excluded. Live-headline surfaces (home_web, section_web, feed_app, section_app, related_links) give Culture·national | `audience_warehouse_field_reference.md` (canonical_headline definition; test impressions are "test slot"). This is **inferential**: no file states outright that a shipped variant leaves the stored headline alone. |
| Articles already tested | Squad adds lift on every article, or only where the desk has not already shipped a winner | No exclusion gives Local·metro 2.79M, ahead of Culture·national 1.37M. With the exclusion, Culture·national leads | The archive has one test per article. The plan notes hold 2027 at the trailing level, so desk-test gains are already in the base. Reasonable but unfiled: nothing says a second round adds zero. |
| Readers (the leadership view) | Politics·national leads on readers, plan clicks and dashboard Politics lift | Politics·national | Rejected: the brief says the squad is judged on incremental clicks. |

## Recomputation ledger

| Figure | Claimed | Recomputed | Reproduced |
|---|---|---|---|
| Culture·national raw average lift | (dashboard 2.22%) | 2.219% (50 tests, 21 shipped) | yes |
| Prior (all 10,111 variant packages, ML, delta-method binomial variance) | not stated | mu = -1.04%, tau = 4.53% | n/a |
| Culture·national shrunk lift | 1.78% | 1.781% | yes |
| Culture·national own-surface share of clicks | 50.2% | 76.92M / 153.34M = 50.16% | yes |
| Desk-test coverage of own-surface clicks, Culture·national | 8.6% | 8.59% | yes |
| Desk-test coverage of own-surface clicks, Local·metro | 71.1% | 71.07% | yes |
| Culture·national own-surface clicks on untested articles | 70,300,000 | 70,314,857 | yes |
| Culture·national extra clicks | 1,250,000 | 1,252k, which rounds to 1,250,000 | yes |
| Local·metro extra clicks | 800,000 | 808k (31.45M x 2.57%), which rounds to 800,000 | yes |
| Gap | 450,000 | 444k, which rounds to 450,000 (also 1,250k - 800k) | yes |
| Back-test, shrunk vs holdback | "within 2%, 7 of 7; raw 0 of 7" | 7 of 7 within 0.14 points; raw 0 of 7 (min miss 0.72 points). As 2% relative only 3 of 7 pass. | **wording only** |
| Panel readers / visits, 6 desks | POL 3,180/13,041; SPT-M 470/1,550; BUS 1,760/6,642; SPT-N 2,931/11,626; LOC 617/2,359; CUL 1,412/5,052 (thousands) | identical, using the release-to-taxonomy map, latest release per month, and R26-08 April to June dropped as the R26-07B-replaced figures | yes (all 12 cells) |
| Median minutes to first headline correction | POL 86, SPT-M 55, BUS 89, SPT-N 47, LOC 102, CUL 119 | 86, 55, 89, 47, 102, 119 (n = 43, 17, 37, 39, 31, 13) | yes |
| Standards bulletin calibration (March 2026: 11 headline corrections, 22 text corrections) | not claimed | rule gives 11 headline events (10 articles) and 22 note-only events | consistent |
| Staff join, "every shortlisted-desk test was run by that desk's own staff" | yes | true, but trivially: all 12,171 web tests are desk-owned. The join adds no discrimination. | yes |
| Dashboard Politics 4.69% and "leads on readers / planned clicks" | yes | 4.69% = POL-N 205 + POL-M 210 tests pooled; POL-N leads readers and plan clicks | yes |

### Estimator sensitivity for the main figure

Shown for Culture·national and Local·metro on own-untested clicks.

| Estimator | Back-test max miss (points) | CUL | LOC | Rounded CUL / gap |
|---|---|---|---|---|
| ML, binomial variance (golden) | 0.14 | 1,252k | 808k | 1.25M / 450k |
| ML, Poisson variance | 0.13 | 1,239k | 793k | 1.25M / 450k |
| ML, prior on web only | 0.12 | 1,248k | 804k | 1.25M / 450k |
| Method of moments, precision-weighted mu | 0.16 | 1,259k | 814k | 1.25M / 450k |
| Method of moments, unweighted | 0.19 | 1,270k | 823k | 1.25M / 450k (5k from the 1.275M edge) |
| ML on log ratio, back-transformed | 0.27 | 1,280k | 833k | 1.30M / 450k |
| Per-desk priors | not backtestable on web desks | 1,199k | 807k | 1.20M / 400k |
| Zero-mean prior | 0.30 | 1,311k | 859k | 1.30M / 450k |
| Control counted as zero in the prior | 0.44 | 1,103k | 687k | 1.10M / 400k |

The desk and runner-up order never changes. The 50,000-rounded click figure can move one step under estimators that the unfiled tolerance cannot clearly exclude (log scale at 0.27 points, per-desk priors).

## Evidence (competing answers tried)

- Raw dashboard lift on own-untested clicks gives Sport·metro 2.76M. This is the easy route. Shrinkage takes Sport·metro to 0.1M because its 150 tests are small (about 2,200 impressions) and its raw lift is 10.8%.
- Shrunk lift on all clicks gives Business·national 6.18M, then Politics·national 4.81M. Culture·national falls to fifth. This is rejected only by the canonical-headline definition.
- Shrunk lift on own clicks without excluding tested articles gives Local·metro 2.79M, then Business·national 1.73M, then Culture·national 1.37M.
- Surface-set variants (drop related_links, add newsletter and alerts, home and feed only, under-24h only, new articles only) all keep Culture·national first and Local·metro second. Only adding search flips the order, to Business·national 1.58M, then Culture·national 1.53M. Search is a stored-headline surface by the field reference, so this is excluded.
- Panel mapping traps resolve as filed. R26-04H reruns BLN 101/102/105 on the 2026 list (Politics, Culture, Home), so mapping by period date would mislabel them. R26-08 re-carries April to June at the exact R26-05 values that the R26-07B note says are replaced. Taking R26-08 as the latest release gives Culture·national 1,386k and 4,870k, which is wrong.
- Correction timing needs five conventions, none of them stated outright as numbers in a single file:
  1. A published-headline change within 10 minutes of a new (not carried, not put-back) note, taken at the save that publishes the changed headline. The note-save time gives CUL 121 instead of 119.
  2. A live blog counts its own headline changes as well as its entries'. Without this, POL 89.5 and SPT-N 51 instead of 86 and 47.
  3. Restored copies are merged into their originals. Without this, LOC 87 instead of 102.
  4. Going live is publish_at for CMS-published scheduled articles. This needs `publish_at` to be Brisbane time (UTC+10). **That timezone is not stated in any file** (`cms_revisions_export_fields.txt` is silent). Only the data's structure shows it: with +10, no draft save precedes publish_at and the gaps have sharp edges at -10 and +2 minutes. Reading it as UTC gives 61/40/83/41/67/100. Reading it as +11 gives 113/55/98/82/131/126. Gate B/E exposure for the xlsx minutes column; the main call is unaffected.
  5. The median runs over corrected articles only, which is the natural reading.

## Gates

- **A (correct):** pass. All figures reproduce, except the "within 2%" unit.
- **B (facts present):** pass for the main call. The surface-to-headline mapping is in the field reference. It is inferential about shipped variants leaving the canonical headline alone. Weak spot: the `publish_at` timezone for the minutes column.
- **C (forced):** pass for the desk and runner-up. The 50,000-rounded figure is robust over the pass-the-back-test estimators, which give 1.24M to 1.27M. It is less robust at the margin (log scale, per-desk priors).
- **D:** pass. The split among good answers is analytical, not about the meaning of a word.
- **E (prompt):** pass. The prompt pins the desk, the figure, rounding and each xlsx column. It leaves method open (shrinkage, exposure), which is allowed.

## Files / Hygiene: PASS

19 files in 8 formats (csv, xlsx, parquet, pdf, docx, md, txt, eml); one file has 2.3M rows, one 266k. Distractors: the Newsfold syndication agreement, the newsletter performance file, and the dashboard export (right numbers, wrong basis). Dates are coherent: Friday 16 October 2026 email, Monday 12 October staff list, R26-10 published 11 October. Nothing declares the data as synthetic or generated. Minor noise: the field reference is "revised 2 October" while the email says it was updated on 16 October. Two LOC-M web tests are owned by staff whose HR dates do not cover the test start, which is harmless. No exclusion-level finding.

## Stump power

Four independent easy routes each give a wrong desk: raw dashboard lift (Sport·metro), reader share (Politics·national), all-source clicks (Business·national), and no tested-article exclusion (Local·metro). A strong model that shrinks correctly but forgets the exposure base still fails. I expect stumps, and for analytical reasons. The stacked inferences (surface class, coverage, rounding) make full agreement with the 1,250,000 figure uncertain even for a correct solver.

## Stumping type

`mechanism: method_or_model_selection` `stumping_family: analytical_non_defect` `surface_read_dependency: no` `sole_data_defect: no`

The reported dashboard lift is arithmetically right and is not a planted defect. The stump is choosing a validated shrinkage estimator (empirical Bayes, back-tested on the change log) and the exposure base. On clean data it still stumps, so Gate G passes.

## Three rules

`domain: pass` `layers: pass` `decisive_step: analytical`

The field's own analysis, A/B-test winner's-curse correction with empirical Bayes validated against holdbacks, decides Culture·national over Sport·metro. The easy route (dashboard lift times clicks) gives Sport·metro at about 2.8M. Layer 1 is the mixed taxonomies, restated panel months, restored and migrated CMS documents, and mixed timezones. Layer 2 is shrinkage plus the exposure base. Surface classification and the coverage join are rule-application steps below the decisive one.

## Fix

- **solution:** restate the back-test tolerance as 0.2 percentage points.
- **rubric:** allow one 50,000 step on the clicks figure.
- **Optional input_files lever (needs a rerun):** state the `publish_at` timezone in the CMS field notes, and state that shipped variants do not alter the stored canonical headline.

## Pass 2 (re-judge after the pass-1 fix and the leak reader's brief fix)


**Verdict:** DETERMINISTIC (SOLUTION_WRONG on wording only: CRITICAL_COMPONENTS 2 and SOLUTION_STEPS 3 call the 50.2% "platform-drawn", but 50.2% is the share on Bightline's OWN surfaces; the externally drawn share is 49.8%. The figure itself reproduces.)

**Disposition:** FIX_NOW. Reword that one label, and pin two facts the files only imply (see Fix). No model rerun needed: the analytic surface is unchanged.

**Why:** Executed literally, the shipped files give Culture·national 1,250,000 extra clicks, Local·metro 800,000, gap 450,000, and every xlsx row reproduces to the stated rounding. The call is forced by three things the files pin: (i) the per-test winning lift must be shrunk (an empirical-Bayes prior fitted on all 10,111 variant packages), and `headline_squad_change_log.xlsx` back-tests that estimator to within 1.2% of realised holdback lift on 7 of 7 embeddings while raw lift is 30% to 285% out; (ii) the squad can only move headlines on Bightline's own surfaces (`canonical_headline` in the field reference lists every external surface that shows the stored headline); (iii) the desks' own tests (every `owner_staff_id` is that desk's own staff) already cover 8.6% of Culture·national's own-surface clicks and 71.1% of Local·metro's, and the plan holds 2027 clicks at the trailing level, so only untested clicks are incremental. Culture·national wins under every reading I tried except dropping the coverage exclusion, which no reasonable reading supports. Runner-up and gap are less sturdy than the winner (see forks).

## Literal reading first

Executed word for word: desk = the shortlist desk with the largest (shrunk winning lift x own-surface clicks on articles with no test in the archive). The prompt is silent on lift basis, surface scope and coverage; the files supply them (field reference, plan notes, placement brief "tests that desk's headlines", change log notes). Where the files stay silent I listed every option below.

## Recomputation ledger

| Figure | Claimed | Recomputed | Reproduced |
|---|---|---|---|
| Raw avg winning lift vs dashboard (CUL/BUS/LOC) | 2.22 / 2.34 / 3.44 | 2.219 / 2.344 / 3.444 (kept control = 0) | yes |
| Test counts vs dashboard (Politics 415, Business 700, Sport 950, Local 1400, Culture 50) | as dashboard | POL-N 205 + POL-M 210, 700, SPT-N 800 + SPT-M 150, 1400, 50 | yes |
| Prior (ratio-minus-one scale, binomial delta variance, ML, all variant packages, both engines) | not stated | mu = -1.04%, tau = 4.53% | n/a |
| Culture·national shrunk lift | 1.78% | 1.781% | yes |
| Change-log selection | tests_run, avg lift | desk tests started in the embedding's calendar year: 72/3.008, 54/3.137, 60/2.889, 88/3.664, 66/2.678, 60/2.895, 58/3.217 vs 72/3.0, 54/3.1, 60/2.9, 88/3.7, 66/2.7, 60/2.9, 58/3.2. Window by started/ended dates does NOT reproduce (69, 52, 59, 80, 64, 56, 58). | yes (calendar year) |
| Back-test shrunk vs realised holdback | within 2%, 7 of 7 | shrunk 1.863/1.441/2.222/2.568/0.693/1.101/2.410 vs 1.842/1.426/2.218/2.554/0.695/1.108/2.431: errors +1.2/+1.0/+0.2/+0.5/-0.3/-0.7/-0.9% | yes |
| Back-test raw | 0 of 7 within 2% | raw 3.008 etc. vs realised: 0 of 7 | yes |
| Culture own-surface share | 50.2% | 76,918,315 / 153,340,236 = 50.16% | yes (label error, see Verdict) |
| Pageview file ties to plan | ties | all 11 desk totals equal `clicks_oct25_sep26` | yes |
| Desk-test coverage of own-surface clicks, Culture / Local | 8.6% / 71.1% | 8.59% / 71.07% | yes |
| Culture untested own-surface clicks | 70,300,000 | 70,314,857 | yes |
| Culture extra clicks | 1,250,000 | 1,252,299 (-> 1,250,000) | yes |
| Local·metro extra clicks | 800,000 | 808,110 (-> 800,000) | yes |
| Gap | 450,000 | 444,189 unrounded, 450,000 rounded either way | yes |
| Other desks (for ranking) | not stated | BUS-N 697,594; SPT-N 648,293; POL-N 552,392; SPT-M 100,400 | n/a |
| Panel readers / visits, POL-N | 3,180,000 / 13,041,000 | 3,180,260 / 13,041,230 | yes |
| SPT-M | 470,000 / 1,550,000 | 470,290 / 1,550,270 | yes |
| BUS-N | 1,760,000 / 6,642,000 | 1,760,310 / 6,641,840 | yes |
| SPT-N | 2,931,000 / 11,626,000 | 2,930,720 / 11,626,310 | yes |
| LOC-M | 617,000 / 2,359,000 | 616,760 / 2,358,790 | yes |
| CUL-N | 1,412,000 / 5,052,000 | 1,412,240 / 5,052,120 | yes |
| Median minutes to first headline correction: POL-N, SPT-M, BUS-N, SPT-N, LOC-M, CUL-N | 86, 55, 89, 47, 102, 119 | 86, 55, 89, 47, 102, 119 (n = 43, 17, 37, 39, 31, 13) | yes, under one stated rule set |
| Calibration: standards bulletin (11 headline + 22 text corrections in March 2026) | n/a | 11 headline-correction events and 33 new notes in March 2026 under the same rules | consistent |

Panel rule used: each month from its latest release by desk (earlier section list through R26-03, 2026 list from R26-04, R26-04H on the 2026 list, R26-04H rows replace only the sections it carries), R26-08's April to June rows set aside because they are byte-identical to the figures R26-07B restated. Correction rule used: live saves only; headline change = published headline hash differs from the previous live save; new note = first appearance of the text (carried and put-back excluded); pair within +/-10 min; time = the headline-changing live save; live blogs count their own headline and their entries' headlines; restored copies merged into originals; migrated documents and never-live documents dropped; go-live = min(publish_at - 10 h, first live save).

## Forks (literal readings, with the answers they give)

| Fork | Option A (golden) | Option B | Effect |
|---|---|---|---|
| related_links is an own surface (shows the live/tested headline) | in: CUL 1.25M, LOC 0.80M, gap 0.45M | out: CUL 1.05M, LOC 0.70M, gap 0.35M | figures change, winner and runner-up do not. The field reference lists every surface that carries `canonical_headline` and omits related links, so inclusion follows by exclusion only. |
| Coverage exclusion (only untested clicks are incremental) | applied | not applied: LOC-M 2.79M beats CUL-N 1.37M | flips the winner. Implied by plan notes ("no change assumed", "planned on top") plus the owner join, not stated in one sentence. Judged forced. |
| Lift basis | desk's own shrunk lift | squad's pooled realised lift 1.753%: CUL 1.23M still first (-> 1.25M), runner-up becomes SPT-N (~860k), gap ~400k | runner-up and gap change. Desk-specific evidence is the only basis that uses the web desks' data, so I treat it as the expert reading. |
| Estimator rounding band | binomial delta, global prior: CUL 1.781% -> 1.252M | web-only prior 1.775%, Poisson variance 1.762% -> still 1.25M. Log-ratio 1.820% -> 1.28M -> 1,300,000; per-desk prior 1.706% -> 1.20M | the 50,000 rounding makes the figure sensitive to +/-2% in lift. The back-test rejects log-ratio (max error 20.6%) and per-desk prior (15.4%); the filed "within 2%" criterion is the author's, not in the files, but the golden estimator is the best fit by a wide margin (1.2% vs next 1.9%). Thin but settled by the back-test. |
| Time zone of `publish_at` | AEST (+10 h) all desks | UTC: POL-N 64, SPT-M 40, BUS-N 83, SPT-N 42, LOC-M 67, CUL-N 100. AEDT for national desks Oct to Apr: POL-N 105.5, SPT-N 63, BUS-N 90, CUL-N 119 | affects the xlsx minutes column (every desk but SPT-M/LOC-M under DST). The files never state the zone. The data pin +10: first live save is never more than 120 min before publish_at on every desk in every month (no DST step), and the 15 to 716 min scheduling lead only fits +10. Inferable, not filed. |
| Live-blog own headline counts as headline | counts | entries only: POL-N 89.5, SPT-N 51 | two xlsx values change. "a live-blog entry's included" plus the bulletin calibration (11 March events) support the golden. |
| Drafts count as published versions | no (live saves only) | yes: POL-N 86, SPT-N 45, LOC-M 86 | LOC-M changes 102 to 86. Standards 7.4 ("the revision that publishes the corrected headline") supports live only. |
| Stale April to June rows in R26-08 | set aside (07B governs) | latest release: all readers and visits fall 1% to 4% (POL-N visits 12,557k) | the release log names 07B as replacing R26-05/06/07; R26-08's rows equal the replaced figures exactly. Resolvable from the files. |
| R26-04H partial coverage | replaces only the sections it carries (by desk) | replaces whole months (Business/Sport·national blank Nov to Feb) | the first is the only reading that yields 12 months for every desk. |
| Old articles in the 2027 base | all clicks | only articles published in the window | no effect: pre-October-2025 articles carry under 0.3% of own-surface clicks on every desk. |
| Timestamp of the correction (headline save, note save, later of the two) | headline save | note or later: CUL 121, BUS 91, POL-N 88, SPT-N 51 | Standards 7.4 favours the headline save. |

The ten-minute window is not a fork (any value from 9 to 20 gives the same medians; 8 and below change them).

## Gates

- **A:** passes. Every load-bearing figure reproduced. Grain checked: the panel and CMS files are not change-log feeds; the archive is one row per package; shipped = Y once per test. Dashboard "Politics 4.69%" is the 415-test pooled value across POL-N and POL-M (a declared-wrong-basis distractor), and does not misattribute.
- **B:** passes with two unfiled-but-inferable facts (`publish_at` zone, related links). Every decisive value was found in a shipped file or its data. Vocabulary check: "extra article clicks", "desk", "runner-up" appear in prompt and brief.
- **C:** passes for the winner. Strongest competitors built: Sport·metro on raw lift (raw 10.81% x 25.5M = 2.76M), Politics·national on the dashboard's 4.69% (43.2M x 4.69% = 2.0M), Local·metro without the coverage exclusion (2.79M), Politics/Sport·national on readers. Each is eliminated by the back-test, the desk-level join or the owner join. Runner-up and gap carry the related_links and pooled-lift forks above.
- **D, E:** pass. Difficulty comes from estimator choice and unit of analysis, not from a word. The prompt fixes the decision, the rounding and the window; method is open.
- **Contrasting models:** none supplied.
- **Cross-batch reference check:** not performed (no access outside this folder).

## Files / Hygiene: PASS

20 files; formats csv, parquet, xlsx, docx, pdf, md, txt, eml (8). Four distractors present and unused by the solution (newsletter file, syndication agreement, standards bulletin, experimentation dashboard) plus the stale panel releases. Real-looking operational noise (partial panel rerun, restored Brisbane copies, migration copies, mixed time zones). Dates cohere (12 Oct 2026 Monday, 16 Oct 2026 Friday, 11 Jan 2027 Monday, 18 Dec 2026 Friday; export log run times precede the 08:05 email). No README, generation disclosures or toolchain banners found in document properties. Minor: `audience_plan_2027.xlsx` creation date (18 Sep) precedes its stated version P2 date (9 Oct), harmless. Nothing exclusion-level.

## Stump power

The trap that does the work is the winner's curse: the dashboard-style raw lift makes Sport·metro (raw 10.8%, shrunk 0.39%) and Politics (4.69%) look best, and the change log's own tests_run/avg_winning_lift against realised holdback is the evidence to shrink. A second layer, tested coverage by owner, removes Local·metro (94.7% own-surface, 71.1% already tested). A strong model that skips shrinkage lands on Sport·metro or Politics; one that shrinks but skips the coverage join lands on Local·metro. Both are analytical errors, so the task should stump; whether it does is for the model runs.

## Stumping type

`mechanism: statistical_rigor` (empirical-Bayes shrinkage validated by back-test, with a coverage/unit-of-analysis join), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The dashboard and change-log averages are arithmetically right; the difficulty is selection bias in winning lifts and overlap with existing testing, and it persists on perfectly clean data, so it passes Gate G.

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1: panel taxonomy and release restatements, restored and migrated CMS documents, UTC and Brisbane clocks, partial extracts; Layer 2: empirical-Bayes lift estimation validated out of sample, then incremental reach net of existing testing. Easy route a strong analyst who read everything would take: average the winning lifts as the dashboard and change log do and multiply by all own-surface clicks, giving Local·metro (about 2.8M at shrunk lift, or Sport·metro at about 2.76M if lift is raw and coverage is applied), not Culture·national.

## Fix

- **solution:** relabel "platform-drawn" as "on Bightline's own surfaces" in CRITICAL_COMPONENTS 2 and SOLUTION_STEPS 3, and use "own-surface clicks" in step 5.
- **input_files (optional pins, no analytic change, no rerun):** one line in `audience_warehouse_field_reference.md` stating that related-story links show the live headline; one line in `cms_revisions_export_fields.txt` stating that `publish_at` is the editor's AEST (UTC+10) clock.

## Disposition of pass 2

- The label ("platform-drawn" for the 50.2% own-surface share) is fixed in submission.md: blocks 1 to 3 now say own-surface clicks.
- The related-links fork is closed in the pack: the field reference's `related_links` row now says the links show each linked article's current headline (SF7, asserted). The call, the runner-up and every graded figure are unchanged.
- The `publish_at` clock is left unfiled: it is the median ask's device, and this pass found the data pin it to +10 hours (no daylight-saving step, scheduling leads that fit only +10). The squad's pooled lift and the rounding band are settled by the change-log back-test, as this pass found.
- No third pass: the skill allows one re-judge, and neither fix moves a figure, a rung or the decisive path.
