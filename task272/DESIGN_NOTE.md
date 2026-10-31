# task272 design note: a hospital pharmacy's batch-compounded doses against their volume tolerance (architecture 3)

Architecture 3, drawn 2026-10-31 after architecture 2 (the Vellacott Health Foundation's coaching grants) was spent at
stage 4 and retired again by the batch audit. Earlier architectures' sections are retired; their records and their
lessons stand below and in Tried and rejected.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task272.json`, architecture v3, registered 2026-10-31 after a
  fast-forward to main, guard WARN only: `people.first` (Cynthia, an older build's first name), `repeat.gate_g`
  and `repeat.deliverables` against task172. The structural signature (population, G7, method_or_model_selection)
  repeats three lineage architectures and is differentiated against each (task271 v2, task308 v1, task471 v1); the
  nearest ideas are differentiated too (task229 v2 at 0.08, task482 v8, task252, task274).
- **Pairing.** Client domain general-statistics-data-science, task type
  exploratory-data-analysis-distribution-assessment (which serves Descriptive & Distribution Analysis), objective
  Descriptive & Distribution Analysis: each product's distribution of delivered dose volumes over 2026 is assessed
  against its volume tolerance, and the tail beyond the tolerance decides the call.
- **Niche.** Ashcombe Valley Health, a regional hospital in Ontario, batch-compounds ready-to-administer syringes and
  bags for its wards and theatres in the pharmacy's sterile compounding unit, on peristaltic compounders. Each tubing
  set is calibrated gravimetrically at set-up; the unit's procedure weighs the first dose of each set and one dose in
  forty after it; a weighed dose outside tolerance stops the batch, every dose made since the last conforming check is
  weighed (a quarantine sort) and the set is replaced. The procedure lets a set carry consecutive batches of one
  product inside 24 hours. The IV workflow system goes live on 5 April 2027 and weighs every dose of the products
  configured for gravimetric verification at cutover.
- **Decision.** Which batch-compounded products are configured for 100 percent gravimetric verification at the
  cutover (a designation set). Forward facing: the configuration governs every dose from April 2027; the policy reads
  it on the last full calendar year, so the estimate is of 2026 and the reason is filed in the policy.
- **The quantity.** The pharmacy's quality policy files the WHAT: a product goes onto verification of every dose
  where its out-of-tolerance doses in the last full calendar year exceeded 10 in every 100,000 doses made, an
  out-of-tolerance dose being one whose delivered volume lay outside the product's volume tolerance, whether or not
  it was weighed or quarantined.
- **Data-native sentence.** Each set's delivered volume falls with the litres its tubing has pumped since the set-up
  calibration, and the procedure lets a set carry consecutive batches of one product, so the doses at the end of the
  sets that carried extra batches sit furthest below target, where one weighed dose in forty rarely lands before the
  set is changed; a capability study of the weighed doses reads them as one stationary spread.
- **Default path.** A capability study of each product's 2026 weighed doses: the overall mean and standard deviation
  of the delivered volume and the normal tails beyond the tolerance, the reflex of a process performance study.
- **Golden.** Each dose placed on its set: the set's start read from its weighed doses and the product's loss per
  litre pumped from every set's weighed doses, the dose's probability of lying outside the tolerance against the
  scatter about that line, summed over every dose made and stated per 100,000.
- **Shape.** 14, cuts of a distribution: each product's distribution of delivered volumes cut at its tolerance
  limits, the share outside per 100,000 doses made, charted against the line of 10.
- **Shell.** Question form which (the corpus quota WARN), deliverables pdf and csv (WARN against task172), forum the
  Director of Pharmacy (`line_manager_or_team`), forcing event the IV workflow cutover (`cutover_or_migration`),
  organisation family `hospital_or_health_provider`, context artifact the unit's gravimetric check register
  (`register`), all clear of the last three builds.
- **Personas** from `guard.py names --geo "Canada" --seed 272`: Cynthia Underwood (Director of Pharmacy), Erin
  Stewart (the unit's quality pharmacist), Jacob Burgess (the unit's lead technician), Spencer Frank (the IV
  workflow project lead).
- **Screen at the draw** (`raw/wip/screen.py`, in units of the dose-to-dose scatter, before any data is cut): with
  sets changed before the drift reaches the band the textbook normal fit files 1,450 to 2,970 per million against
  truths of 10 to 40, and the rare long runs carry truths far above anything the weighed share or the sorts see; the
  generator re-runs every rung on the built world and `generator/checks.py` asserts each rung's set.

## Architecture 2 record (spent 2026-10-21)

- Draw: the Vellacott Health Foundation's FY2027 Decision Coaching Grants, one per Fair Assistance Collaborative hospital where at least six percent of its counsellors' 2025 first reviews on households within the free-care limit, on their income over the twelve months before applying, left the household owing more than half of its balance. Golden: 16 grants ($1,024,000), H02, H08, H10, H11, H12, H14, H15, H17, H20, H22, H23, H24, H26, H28, H29 and H30, each application's three-month income put on a twelve-month basis through its region's calendar for its kind of work; the 2025 policy's quarter times four files 5, a calendar pooled across regions or across kinds of work 10.
- Build: stage 3 green on target.zip 66ca10c7 (checks 0 failed, the independent verifier PASS, two byte-identical builds, figures_check 85 of 85, precut 51, leak.py REVIEW answered, heart WARN), committed PAUSED at e59482a0 and 90d43a79.
- Stage 4, two isolated scored readers (`score_reader.py --call-key call.qualify --call-key call.count`): both landed the call with the golden set. Reader C (r272c) fitted a smoothed seasonal profile for each hospital and kind of work by month received and checked it on households seen twice (predicted and observed ratios correlating at about 0.98); reader D (r272d) estimated profiles by kind of work, hospital group and month and validated them on the households that applied more than once (their log spread fell from 0.58 to 0.10). Each quoted criteria 2.3's twelve months against the guide's three months times four as the decisive sentence. Asks: neither kept an Ask A figure (both summed every write-off line once exact duplicates were dropped, 602,632.9 thousand against 299,646.9); Ask B 1 of 31 each, the H20 tie (code 1 for the whole year).
- Judge (the isolated thread's verdict): DETERMINISTIC, APPROVE; the 16 reproduced with the calendars fitted on either year or both, per hospital, on medians or geometric means (the qualifiers at 7.04 or above, the others at 5.05 or below); the easy route files 5, one calendar per kind of work 10; Gate G method_or_model_selection and analytical_non_defect; Gate H pass; findings on the asks (the repeated write-off and its credit to the household's last approval, the renumbered reason list), watch items, and one on a rival clause: "one calendar for each region" files 10 only with the seasonal kinds pooled per region and the year-round kinds left flat, while pooling every kind files 4, so a rival construction is stated exactly or not at all.
- Fate: Gate F failed at both readers, so the architecture is spent. A three-month figure beside a filed twelve-month window is a gap the documents state outright, and seasonal work named on every application hands over the correction: a reader who sees the gap estimates the calendar at the finest cell the data supports, which is the golden family. Both ask devices held against both readers.

## Architecture 1 record (spent 2026-10-21)

- Draw: the Vellacott Health Foundation's FY2027 Decision Coaching Grants, one per Fair Assistance Collaborative hospital whose financial-assistance counsellors are at least six points less likely to approve right after an approval than right after a denial on the same working day, on 2025 determinations pooled from three billing hubs. Golden: 11 grants ($704,000), H03, H06, H09, H10, H17, H19, H20, H21, H22, H26 and H31, from the within-day contrast less its expectation with each counsellor-day's determinations in every order; the counsellor-day fixed-effects slope files 23 and the pooled contrast 2.
- Build: stage 3 green on target.zip 90774da6 (checks 0 failed, the independent verifier PASS, two byte-identical builds, figures_check 82 of 82, precut 51, leak.py REVIEW answered, heart WARN), committed PAUSED at a84ba0db and 24b56b9e.
- Stage 4, two isolated scored readers (`score_reader.py --call-key call.qualify`): both landed the call with the golden set. Reader 1 (r272a) corrected each within-day contrast by shuffling the day's determinations and kept no ask figure (every FAWO line summed, 816,026.2 thousand; code 1 read for the whole year). Reader 2 (r272b) fitted counsellor-day fixed effects, named their bias at about 19 determinations a day unprompted and subtracted the null of 150 within-day permutations per hospital; it kept every Ask A figure (31 of 31: the write-off once per application, the twice-loaded lines dropped on adjustment_id, reversals per account) and no Ask B figure (code 1 for the whole year).
- Judge (the isolated thread's verdict.md, `determinism_check_report.md`): DETERMINISTIC, FIX_NOW on documentation only: every figure reproduced (197,939 determinations, the 11, $704,000, all 62 ask figures); the one live main-call reading is the uncorrected within-day contrast (23), which is the stump itself; the two ask conventions (the write-off once per application, the 1 July 2025 renumbering) recoverable from the data and unstated. Gate G method_or_model_selection and analytical_non_defect; Gate H pass.
- Fate: Gate F failed at both readers, so the architecture is spent. The small-sample bias of conditioning on the previous outcome inside a short sequence (the Miller and Sanjurjo hot-hand correction) is a named reflex for these readers: criteria that compare "the chance" within the same working day, beside queues of about 19, hand over the within-day permutation null. Ask B's renumbering held against both readers; Ask A's repeated write-off held against one.

## Tried and rejected

- The seed's own quantity (the Medicaid gap on the "would recommend" top-box rate across a state report's hospitals), every route screened at the draw: composition and patient mix settle the comparison population (WHAT screen); shrinkage of small cells repeats task253; design weighting repeats task264's lesson and task268 v2's reflex; nonresponse either fails determinacy or repeats the inverse-probability weighting of task264, task267 and task268; survey mode effects belong to Experiment & Causal Analysis; misclassification is the spent sensitivity-and-specificity family; nowcasting the late returns repeats task181; telescoping sits next to task453.
- A race-probability (BISG) regression for the equity gap (prototype `p1.py`): a strong ladder, but the same linear unmixing of a mixed population as task263, a clone of its driver.
- Traffic count factor groups for an annual average (prototype `t1.py`): count differences of one or two units at tiny margins, and the ground overlaps task474.
- The sequence effect at queues of 4 to 14 determinations with effects of 2 to 13 points (`s1.py`, `s2.py`): the two corrected estimators (the excess over reordering by counts, the held-day slope less its reordering expectation) disagreed on 1 to 3 hospitals a seed, with the closest margins 0.01 to 0.3 points; the queues were lengthened and the effect hospitals separated from the line.
- Effects of 12 to 17 points (`s4.py`, `s5.py`): the family agreed, but the day's rate without the pair as a control landed 10 or 11 of the 11 hospitals, its bias of 3 to 5 points smaller than the gap to the line; the effects were lowered to 9.5 to 12.5 with a wider day mix (`s6.py`), where it lands 9.
- Ask B as presumptive approvals with nightly re-runs replayed under fresh application numbers (D1): dropped at stage 2, because no asking sentence makes the count determinate without naming the device (a replay is a fresh application record, so "each application once" counts it, and any wording that excludes it narrates the re-run); replaced by the reason list renumbered on 1 July 2025 (D2).
- Queues of 6 to 28 a day with counsellors sitting on 55 percent of working days: the held-day route filed 28 of 31, an answer a reader distrusts on sight; queues of 8 to 32 on 48 percent of days put it at 23 with the family still closed (1.81 points).
- Effects of 9.5 to 12.5 points with the day's rate over the other determinations as a reflex: it landed the golden set (the others' count is the day's sufficient statistic), so it was moved into the family and the construction made every member agree, rather than the world bent to break it.
- Architecture 1 (each counsellor's sequence effect measured against the reordering of each working day's own determinations): spent at stage 4, both scored readers corrected the within-day contrast for the short-queue bias by permuting each day's determinations and landed the 11; a decisive step that is a named small-sample bias correction falls to a reader who knows the bias by name, however the ladder below it is tuned.
- The outcome "did not get free care in full" (a denial or any discount below 100 percent): noise in the year-round households' calendars inflated the shares at the 200 percent line, where the 2025 policy's full-care boundary sits on the eligibility line; the outcome moved to owing more than half of the balance (a denial or a 25 percent discount), whose policy boundary at 300 percent no year-round household's pay crosses.
- Households timing their applications to a low quarter (selection on the quarter): dropped in the prototype, no separation the seasons did not already give.
- Every hospital's designed share at 7.5 or 4.5 percent (the first build of this architecture): under the golden calendars 13 hospitals landed between 7.50 and 7.56 percent and 8 between 4.50 and 4.54, a cluster that confirms the golden route to a reader trying several calendars and reads as made in the chart; the designed shares were spread to irregular values, and the three set below what misassessment alone gives them (H04, H07 and H27, which then denied almost no one for documents) were raised to 4.29 to 4.68.
- Flat pay for year-round households and a fixed seasonal shape (the first builds of this architecture): a household's repeat applications carried the same three-month total to the cent, which reads as made; pay now rises unevenly from year to year and varies month to month, a household reapplies when its work takes its pay down (the season it knows) rather than on a month's luck, and the fixed-effects member falls back to a cell's month means where the cell does not identify its own calendar (the Olympic Peninsula's resort households: left unadjusted there, it had read H28 at 6.31; the reapplication change did not move that figure, the missing cell did).
- Also weighed at the re-root draw and dropped before any prototype, no reasons written down at the time: CGM, cash fills, TTR, a hungry-judges time-of-day effect, and heaping (already on file as spent in this lane).
- Architecture 2 (each household's twelve-month income rebuilt from the 2025 policy's quarter through its region's calendar for its kind of work): spent at stage 4, both scored readers read criteria 2.3's twelve months against the guide's three months times four, fitted a seasonal profile per hospital or region and kind of work and landed the 16; a decisive step that answers a gap the documents state outright falls to a reader who reads both documents, however finely the calendar has to be cut.
- Screens run at the architecture 3 draw on 2026-10-21, each set aside with its record. None cleared, so the number retires.
  - Demand censored at a stock or a capacity: task18, task108, task147, task168, task133, task141, task120 and task179 record it as spent.
  - Event times known only between periodic inspections, or at a single inspection: task476's leak starts, and the onsets set aside at task270's draw.
  - A share past a line taken from model predictions with their error added back, as in poverty mapping or an exposure model's Berkson error: task123 records it as task253's insight, task185 measured the exceedance route dead on the lever against the plug-in, and task143 records a strong analyst adding the stated validation error by reflex.
  - Realised variance against microstructure noise: task270 and task271.
  - A hot deck whose donor cells leave out the grouping variable, pulling each group's imputed earnings toward the other groups': dropping the allocated values is the filter route the partial-coverage screen kills, and reweighting the respondents within cells is task253 v1's nonresponse adjustment within classes.
  - Immortal time, and the period-analysis estimate of current survival: both are delayed entry into the risk set, task265's lesson.
  - A point-in-time count's elapsed durations turned into a year's flow: length bias, task264's size-biased sampling.
  - Recall decay across a survey's recall period: the latest month is a filter route and the decay form forks; telescoping sits next to task453.
  - Persistence beyond a panel's span by a mover-stayer chain: mover-stayer, latent Markov and second-order chains extrapolate apart.
  - Bunching below the free-care line: the counterfactual density's degree, window and bin width are open.
  - The own-children estimate of fertility, and extinct-generation old-age death rates: named methods, each with an open adjustment; the second was set aside at task271's re-root.
  - A closing auction's own impact net of the liquidity its imbalance drew: task197's design, abandoned there on the taxonomy; here, which offsetting orders were responsive is a judgment no record settles.
  - Roll-call ideal points: task269 and task270.
  - The tail of a sum of correlated parts by simulation: each unit's recorded totals are a filter route.
  - Minimum-night-flow leakage through the night-day factor: no utility task type serves Descriptive & Distribution Analysis.
  - Medication persistence, pharmacology's one Descriptive task type, set aside at task270 and task271: the reverse waiting time forks, and the new-user washout is a WHAT.
  - The Fair Assistance world itself: its quantities are filed rules once its two estimation hooks (a counsellor's sequence effect, a season inside a quarter) are spent. Its presumptive-screen incomes are the Berkson case above, and take-up through verified applicants is the transported error-rate family (task192, task267).
- Architecture 2 retired by this session's batch audit (2026-10-31), short of the survivor anatomy the approved builds share: its actor had a column (every application named the main earner's kind of work) and its link was stated outright (the criteria's twelve months against the guide's three months times four), so only the field's-method rung held; it is re-rooted, not repaired, so the portal sees one strong build.
- 2026-10-31, at the architecture 3 draw: a clinic medication refrigerator's product temperature rebuilt from the
  building system's air probe through each model's thermal response, calibrated on pilot units carrying a buffered
  probe (the card first drafted): the same insight as task482 v8 (a slow quantity carried through a lag measured on a
  short overlap), spent there at stage 4 because two records of one unit side by side are compared on reflex.
- 2026-10-31, at the architecture 3 draw: the drift-between-resets stump in a precision machining plant (inserts
  wearing between tool changes, hand checks at intervals, containment sorts): the guard banned the organisation
  family (manufacturer, task482 v16 in the last three builds) with the context artifact and the forcing event; the
  hospital pharmacy's compounding unit carries the same structure honestly.
- 2026-10-31, at the architecture 3 draw, set aside before any prototype: an assay's drift between calibrations read
  from quality control (task274's calibration-specific bias on an immunoassay sits too close); hypochlorite decaying
  between deliveries at small water works (operators' grab samples land in most low spells, so the sampled share
  files nearly the golden); a dental milling centre's burs (every crown is seated on its die before release, so the
  checks are not sparse); medication adherence, roll-call ideal points and small-area opinion (rules, spent, or an
  open model specification); low-depth genotype calls (a named reflex).
