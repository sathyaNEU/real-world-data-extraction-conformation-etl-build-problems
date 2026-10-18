# task194 - determinism judge report

Isolated review. File universe: the fresh unzip at
`/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/task194_judge_pack/`
(21 members) plus the graded blocks quoted in the judge brief. Nothing under the repo task folder
was opened: no design note, no generator, no pipeline.json, no earlier report, no skills or
guidelines. No git command was run and no agent was spawned.

**Procedural disclosure.** The brief is a single file and the graded blocks are inside it, so the
one read of the brief put the committed answers in front of me before I touched the bundle. I did
not use them as a starting point: the method was recovered from the register's own structure, and
the enumeration below was built by generating 12 estimator variants mechanically and comparing
afterwards, which is why two of the twelve committed figures came out contradicted rather than
confirmed. Read the Gate C enumeration as independent; read my claim to have been surprise-capable
with that caveat.

---

## Verdict

**NOT_DETERMINISTIC** (the main DECISION is forced and robust; the committed FIGURES are not)
**Disposition: SEND_BACK.** The repair pins the completion/development estimator in the shipped text
and re-cuts two graded cells off their rounding edges; that changes what solvers see, so a rerun is
required.
**Governing taxonomy: underspecified_objective** (with `margin_or_boundary_fragility` as the
mechanism on the 41240 and 41220-factor cells, and a separate `solution_incorrect` on 41320).
**Fix location: prompt** (plus one regenerated figure in the solution blocks).

### Why

Every graded number in `embed_placement_2027q4.xlsx` turns on a reporting-lag development factor
that **nothing in the prompt or in any shipped file pins**. The charter (part 4) and specification
4.0 (sections 2 and 3) say what avoidable complications are and over which period, and
`coding_close_out_register.csv` supplies the run-off triangle, but no shipped text chooses between
the standard estimators of that triangle. Volume-weighted age-to-ultimate on the cost centre's own
settled quarters gives the main figure 44.6; the same selection with simple-average link ratios
gives 44.7; all-rows chain ladder gives 45.1 and 45.2; carrying the register's own
`episodes_awaiting_coding` into the expected side gives 36.6; taking the rate per in-scope episode
rather than per separation gives 49.0. All are reasonable. The decision is the same under every one
of them (Alderbrook General Medicine, 41210, by 1.6x), so Gate C passes for the main *call* and
fails for the main *figure* and for deliverable item 1, which the prompt asks for to one decimal.
Separately, one committed cell (41320 at 14.9) reproduces under none of the twelve estimators I
built; I get 14.8.

---

## Gate table

| Gate | Result | One line |
|---|---|---|
| A - solution correct on the shipped files | **FAIL (narrow)** | 41210's whole chain reproduces to the cent (3097 -> 3408.55, uplift 311.55, factors 1.763 / 1.0368, expected 3023.647, 44.607); 41320's committed 14.9 does not reproduce under any estimator (I get 14.785 or 14.826, both 14.8); Critical Component 1 mislabels four of the five open quarters' publication counts. |
| B - every decisive fact in the shipped files | **PASS** | Eligibility (charter 4.2), period (spec 3.3), expected rates (Appendix A / `hac_stratum_rates.csv`), planned separations (`activity_plan_2027q4.csv`), the restatement history (`coding_close_out_register.csv`) and the two list revisions (Appendix B / `hac_category_list.csv`) are all shipped. Action vocabulary grounded: "avoidable" and "carries" both occur in `improvement_partnership_charter_v3.pdf`. |
| C - uniquely forced, no defensible alternative | **FAIL on the figures, PASS on the decision** | 41210 wins under all 12 development variants and even against the nine ineligible units (44.61 vs 36.24 for 41440); but the asked-for number is one of {36.6, 44.6, 44.7, 45.1, 45.2, 49.0} and row 41240 straddles its printed bin (11.5414 vs 11.5646). |
| D - difficulty is analytical, not semantic | **PASS** | The split between the right and wrong answer is right-censored coding, not the reading of a word: the naive path is a method error, not an interpretation. |
| E - prompt unambiguous on the decision | **FAIL (minor)** | The decision is pinned; the deliverable figures are not, because the completion method they turn on is unstated while the rounding unit is stated. Supplementaries 3 and 4 also admit a second source (see below). |
| F - stump power | **STRONG** | The default path files a specific wrong unit; 41210 sits 5th of 12 on the undeveloped record. |
| G - no surface-read-rejection | **PASS** | `mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. |
| H - the three rules | **PASS** | `domain: pass`, `layers: pass`, `decisive_step: analytical`. |

---

## Gate C - the enumeration (built before the blocks were used)

The shipped text fixes the estimand: eligible acute inpatient units at 2027-03-24 (charter 4.2),
the period being every closed quarter from 1 July 2024 (spec 3.3, which also forbids any other
period for a unit), avoidable = own patients' complications less expected under Appendix A
(charter 4.3), carried onto the quarter's planned separations (charter 4.4, spec 3.4). It is silent
on how an unfinished quarter is carried to what it settles at. Options, each computed:

| Option | What it is | Winner | 41210's figure |
|---|---|---|---|
| 1 | No development: the record as it stands over ten quarters | **41220 at 26.1** | 8.5 (41210 ranks 5th of 12) |
| 2 | The four most recent closed quarters, as recorded | **41320 at 27.59** | -15.1 |
| 3 | The five quarters that have fully settled, only | **41220 at 50.63** | 24.27 (3rd) |
| 4 | Unit's own settled quarters, volume-weighted, direct age-to-ultimate | 41210 | **44.607 -> 44.6** |
| 5 | Unit's own settled quarters, volume-weighted, product of link ratios | 41210 | 44.607 -> 44.6 |
| 6 | Unit's own settled quarters, simple-average ratios | 41210 | 44.73 -> **44.7** |
| 7 | All rows chain ladder, volume-weighted link ratios | 41210 | 45.12 -> **45.1** |
| 8 | All rows chain ladder, simple-average link ratios | 41210 | 45.22 -> **45.2** |
| 9 | Network-wide settled basis (the first five quarters for every unit) | 41210 | 44.61 -> 44.6 |
| 10 | Option 4, rate taken per in-scope episode instead of per separation | 41210 | 48.97 -> **49.0** |
| 11 | Option 4 with expected also carried for the register's `episodes_awaiting_coding` | 41210 | 36.59 -> **36.6** |
| 12 | Option 4 with each developed quarter rounded to whole separations | 41210 | 44.55 -> 44.6 |

**Closed forks.** Options 1, 2 and 3 are ruled out by shipped text, and this is the design's real
strength. Option 1 contradicts charter 4.3 ("the complications its own patients had", the actual
count) and spec 3.7 ("a quarter is reported once the coding of its separations is complete"), with
the register showing the coding of five quarters demonstrably incomplete. Options 2 and 3 are shut
by one sentence of spec 3.3: "No other period is reported for a unit." The per-separation
denominator (option 10) is shut by spec 3.4's own words, "expected complications per separation",
against a file whose column is defined as separations.

**Open forks, which is the finding.** Options 4 to 9 are all textbook readings of the same triangle
and nothing in the pack selects among them. They agree on the decision and disagree on the printed
answer: 44.6, 44.7, 45.1, 45.2. Option 11 is the sharpest of them, because it is invited by a column
the author shipped: `episodes_awaiting_coding` never reaches zero (41210's 2024-25 Q1 still shows 4
awaiting at the last publication while its complication count has been flat at 334 for six
publications), 766 of 41210's episodes across the ten quarters are still awaiting coding at
2027-02-25, and a solver who carries the numerator to ultimate but leaves the expected side on the
coded episodes only is mixing two grains. Carrying both gives 36.6 and the same winner.

---

## The three things the brief asked me to be deliberate about

**1. The count and identity of the still-filling periods, and each one's contribution.**
Reproduced and correct. Applying "a quarter whose last two publications agree has settled" across
all 23 cost centres in the register: 2024-25 Q1 to 2025-26 Q1 have settled for every unit (22 of
22 present), and five quarters are still filling for at least one unit - **2025-26 Q2** (12 of 21
settled), **2025-26 Q3** (5 of 21), **2025-26 Q4** (1 of 21), **2026-27 Q1** (0 of 21) and
**2026-27 Q2** (0 of 21, one publication only). "5 of the ten closed quarters" is right and the
identities are right; no period is included or omitted wrongly.

Each one's separate contribution to 41210's uplift, recomputed from the triangle:

| Quarter | Publications held | Latest count | Age-to-ultimate | Developed | Contribution | Write-up |
|---|---|---|---|---|---|---|
| 2025-26 Q2 | 5 | 305 | 1.0000 | 305.00 | **0.00** | 0.0 (ok) |
| 2025-26 Q3 | 4 | 310 | 1.037580 | 321.65 | **11.65** | 11.65 (ok) |
| 2025-26 Q4 | 3 | 348 | 1.124224 | 391.23 | **43.23** | 43.23 (ok) |
| 2026-27 Q1 | 2 | 287 | 1.314770 | 377.34 | **90.34** | 90.34 (ok) |
| 2026-27 Q2 | 1 | 218 | 1.762987 | 384.33 | **166.33** | 166.33 (ok) |
| | | 3097 total | | 3408.55 | **311.55** | 311.55 (ok) |

**The one mismatch is the "publication held at" label.** Critical Component 1 says 2025-26 Q2 is
held "at its 4th publication", Q3 at its 3rd, Q4 at its 2nd and 2026-27 Q1 at its 1st, then says
2026-27 Q2 is "at its own close alone". The register shows 5, 4, 3, 2 and 1 publications
respectively (coding close for the December 2026 quarter being 2027-02-25, eight weeks after
quarter end per spec 3.7, which is that quarter's first publication). So four of the five labels
are one short, and they are one short on a different convention from the fifth, which is counted as
publications. Read literally the block is wrong: 2025-26 Q2 is at its 5th publication, its 4th
restatement. Repairable in the block.

**2. Every numeric range or interval the write-up asserts.** This version asserts no interval or
range. The one set-valued claim is step 7's "all 8 readings of the growth the register leaves open
name the same unit". I cannot enumerate the author's eight, because nothing shipped defines the
candidate set; what I can report is that all 12 readings I built (options 4 to 12 above, plus the
three rejected period variants) name 41210 except options 1, 2 and 3, which are the ones shipped
text excludes. So the claim is directionally confirmed on every reading that survives the rules,
but it is not checkable as stated. Two near-tie claims sit inside it: the second-place figure is
27.8 under options 4, 5 and 6 and 28.0 under option 9, so "27.8 at the closest unit" and "gap 16.8"
are themselves estimator-dependent.

**3. The direction of every ratio, factor and movement.** All correct, none inverted.

| Statement | Check | Direction |
|---|---|---|
| "a margin of 1.604x" | 44.607125 / 27.813044 = 1.60382 | multiplier, correct way up |
| "still to be multiplied by 1.763 at 41210" | 1629 ult / 924 at first close = 1.762987 | >1, applied to the early figure to reach ultimate: correct |
| "against 1.0368 at 41220" | 1.036765 on the unit's own settled set | correct, and correctly the smaller of the two |
| 41220 "at 26.1 and rises only to 27.8" | 26.14 undeveloped -> 27.81 developed | does rise, by the stated amounts |
| "loses the lead on rank and not on value" | 41220's value rises, 41210's rises further (8.50 -> 44.61) | correct |
| 41320 "leads on the four most recent closed quarters at 27.59" | option 2: 41320 first at 27.59 | correct, and it is a lead |
| "3097 to 3408.55, an uplift of 311.55" | 3408.5496 - 3097 = 311.5496 | correct |
| "gap 16.8" | 44.607125 - 27.813044 = 16.794 | correct |
| "the record as it stands reads 41210 5 of 12" | option 1 order: 41220, 41230, 41320, 41240, **41210** | correct |

---

## Gate A - what reproduced and what did not

Independent reconstruction from `episode_outcomes_extract.csv` (465,882 rows) under spec 2.1 to 2.4
(care type Acute, length of stay >= 1, acute inpatient unit per `unit_register.csv`, DRG mapped to a
band with a published rate) reproduces **all 215 rows of `unit_indicator_series.csv` exactly**:
in-scope episodes and observed complications to the unit, expected complications to within 0.0005.
Eligibility reproduces at 12 units (23 acute cost centres, less 41511 and 41512 closed 2025-09-30,
less the nine units placed with in the last twelve closed quarters including the in-progress 41460).

### Figures that did not reproduce

| Figure | Committed | Recomputed | Gap |
|---|---|---|---|
| 41320 Stonecreek General Surgery, avoidable complications | **14.9** | **14.785** (direct) / **14.826** (link-ratio product); 14.79 to 14.83 across all unit-own-record estimators | both round to **14.8**. Only a network-wide settled basis gives 14.92, and that basis breaks seven other rows of the same table (41220 28.0, 41240 11.4, 41310 4.7, 41420 4.4, 41510 1.2, 41230 18.6, 41410 13.0). No single estimator reproduces the committed table. |
| 41240 Alderbrook Respiratory Medicine | **11.6** | **11.5414** (direct) / **11.5646** (link-ratio product) | the two standard estimators straddle the 11.55 bin edge: the committed 11.6 is right under one and wrong under the other |
| Critical Component 1, publication held at | 4th / 3rd / 2nd / 1st / own close | 5th / 4th / 3rd / 2nd / 1st | four labels one short, and inconsistent with the fifth |

Everything else in the blocks reproduced: 44.6, 27.8, 18.5, 12.9, 6.9, 6.4, 4.9, 4.3, 3.2, 1.9,
the 4,261 and every other planned-separations figure, 3023.6 expected, 3097, 3408.55, 311.55, the
five per-quarter contributions, 1.763, 1.0368, the gap 16.8, the 1.604x margin and "5 of 12".

### Bin-edge distances, graded figures (rounding unit as stated in the asking sentence)

Deliverable item 1, one decimal, so the bin half-width is 0.05. Distance is to the nearest printed
bin edge; the brief's flag is 0.3 of the rounding unit, i.e. 0.03.

| Unit | Computed (direct) | Distance | Computed (link ratios) | Distance | Flag |
|---|---|---|---|---|---|
| 41210 | 44.607125 | 0.0429 | 44.607125 | 0.0429 | |
| 41220 | 27.813044 | 0.0370 | 27.813044 | 0.0370 | |
| 41230 | 18.505328 | 0.0447 | 18.505328 | 0.0447 | |
| 41320 | 14.785495 | 0.0645 | 14.826409 | **0.0236** | **FLAG** (and does not match the committed 14.9 either way) |
| 41410 | 12.908606 | 0.0414 | 12.908606 | 0.0414 | |
| 41240 | 11.541408 | **0.0086** | 11.564631 | **0.0146** | **FLAG** (and the two estimators print different answers) |
| 41520 | 6.898537 | 0.0485 | 6.898537 | 0.0485 | |
| 41330 | 6.387147 | 0.0371 | 6.387147 | 0.0371 | |
| 41310 | 4.868832 | **0.0188** | 4.875400 | **0.0254** | **FLAG** (both still print 4.9) |
| 41420 | 4.319066 | 0.0309 | 4.319066 | 0.0309 | borderline |
| 41430 | 3.188212 | 0.0382 | 3.188212 | 0.0382 | |
| 41510 | 1.885045 | 0.0350 | 1.885045 | 0.0350 | |
| gap | 16.794081 | 0.0441 | | | |

Narrative figures in the recommendation and critical-components blocks, at the precision printed:

| Figure | Value | Unit | Distance | Flag |
|---|---|---|---|---|
| 41220 development factor 1.0368 | 1.03676471 | 0.0001 | **0.0000147** | **FLAG**, 0.15 of the unit: the figure sits essentially on its bin edge, so any reweighting prints 1.0367 or 1.0369 |
| margin 1.604x | 1.60382032 | 0.001 | 0.000320 | borderline, 0.32 of the unit |
| 41210 development factor 1.763 | 1.76298701 | 0.001 | 0.000487 | |
| 3408.55 | 3408.549647 | 0.01 | 0.004647 | |
| 311.55 | 311.549647 | 0.01 | 0.004647 | |
| 27.59 (four-quarter reading) | 27.5878 | 0.01 | 0.0030 | borderline |

All supplementary figures are whole counts, so no rounding fragility there.

---

## Gate A/C - the supplementary answers

| Ask | Committed | Recomputed | Verdict |
|---|---|---|---|
| 3. Separations the indicator does not measure in calendar 2026, by site, and how many recorded a complication | 7198/383, 6108/369, 6715/421, 1914/145 | **7198/383, 6108/369, 6715/421, 1914/145** | reproduces exactly from `activity_summary_monthly.csv` totals (site taken from its own monthly `facility`, which moves: 41270 to H2, 41430 to H2 and 41520 to H3 from July 2026) less the in-scope episodes reconstructed from the extract. **Second defensible source**: computing the whole thing from the extract instead gives 7101/379, 6161/373, 6813/428, 2014/152. Mitigated by the manifest ("omits uncoded episodes") and by the prompt's site attribution needing the monthly facility, not closed. |
| 4. Sub-acute and mental health separations and complications by quarter | 1443/107 ... 1295/116 | **all 20 figures reproduce** from `activity_summary_monthly.csv` for 41610, 41620, 41630 | **Second defensible source**: the extract gives 1526/112 ... 1357/121 after deduplicating on the dictionary's stated separation key, or 1691/129 ... raw. The 1,422 duplicate-key groups in the extract are confined to exactly these three units. Mitigated by the word "reported" and by the dictionary's "distinct separations the unit reported in the month", not closed. |
| 5. In-scope episodes recording a complication by group, 2025-26 and 2026-27 to date | 3563/1618, 4281/2104, 1827/837, 1598/704, 4236/1892, 2613/1264, 861/425, 1661/757 | **all 16 figures reproduce exactly** | the only route that reproduces is the right one: `hac_detail_extract.csv` distinct in-scope episodes per group, with the 2022 list revision applied to separations before 2026-07-01 and the 2026 revision after (which moves HAC03 from pressure injury to catheter infection and folds the old HAC13), plus a fallback to the episode-level `hac_category_code` for the 1,026 in-scope episodes of the Carrowdean campus units (41520, 41510, 41511, 41512) whose detail the manifest declares omitted. Detail alone gives 3503/1584 etc.; the episode-level first-complication field alone gives 2766/1251 etc. Well forced by the manifest's declared omission. |

---

## Files / Hygiene: PASS, with notes

21 files; four formats (17 csv, 2 pdf, 1 xlsx, 1 txt); largest file 465,882 rows / 34 MB.
Distractors present and relevant but unused: `patient_experience_unit_quarterly.csv`,
`nursing_hours_by_unit_monthly.csv`, `hand_hygiene_audit_2026.csv`. No README or how-generated
artifact, no synthetic/benchmark/authoring disclosure, no tool banner; a grep for the authoring and
method vocabulary (synthetic, generated, benchmark, golden, chain ladder, development factor,
run-off, solver, prompt) returns nothing across all 21 files. `quality_dashboard_2026q2.xlsx`
carries a realistic author (Joseph Hunter, matching `placement_cycle_notes.txt`) and a created date
of 2027-03-05 matching the manifest's export date. Layer 1 mess is authentic: two national list
revisions across a mid-year boundary, fiscal quarters against a calendar-year ask, a campus whose
complication detail lives in another module, month-by-month facility reassignment, two amalgamated
predecessor cost centres, duplicate episode rows in the sub-acute units, a comorbidity score keyed
on about six episodes in seven and never used, and an extract that omits uncoded episodes against a
complete activity cube.

Notes, none exclusion-level:
- **Format lean**: 17 of 21 files are csv (81 per cent). Above the three-format floor, but a
  monoculture-ish archive; in-house padding item at most.
- **Temporal slip**: `placement_cycle_notes.txt` says "Coding for the December quarter closed on
  28 February", while spec 3.7 (eight weeks after quarter end) and the register's own last
  publication both put it at 25 February 2027. Three days, non-decisive, in-house fix.
- **Near-Gate-G artefact, passes**: `quality_dashboard_2026q2.xlsx` shows 41210 with the best
  standardised ratio in its hospital (0.738) for the December quarter. It is literally correct
  (observed 218, expected 295.6, both reproduce), it carries its own disclaimer ("Quarter-end
  position; not a projection of any later quarter"), and it ranks units on a different quantity
  over a different period from the decision question, so it does not rank the candidates on the
  decision question and get it wrong. It is a legitimate default-path artefact rather than a decoy.

---

## Stump power (Gate F)

Strong, and empirically so on the shipped data. The default path - taking the ten closed quarters as
the extract and the indicator series record them - produces a specific, confident wrong answer,
Alderbrook General Surgery at 26.1, and puts the right unit fifth of twelve at 8.5. Two further
plausible shortcuts each name a different wrong unit: the four most recent closed quarters name
Stonecreek General Surgery at 27.59 (those being the quarters the pull date cuts shortest), and the
quality dashboard's latest standardised ratio makes 41210 look like the best medical unit in the
network. Nothing in the pack announces that the counts are still filling; the register has to be
read as a run-off triangle and the per-cost-centre spread discovered (1.763 against 1.0368, a factor
the pack ties loosely to `cis_registered_date`), which also defeats a single network-wide factor.
No lever is needed to make this harder.

## Stumping type (Gate G)

`mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`,
`sole_data_defect: no`.

The difficulty is a right-censoring and development problem on numbers that are all correct: every
published count in `coding_close_out_register.csv` is correct as at its publication date, the
register exists precisely to restate them, `unit_indicator_series.csv` is a correct as-at snapshot,
and the dashboard labels itself a quarter-end position. Nothing has to be caught as wrong; a
not-yet-observed quantity has to be estimated from the history that pins it. That is the
FINE-numbers forecasting shape, and it would survive perfectly clean data because the coding lag is
real structure rather than a defect. Not banned.

## Three rules (Gate H)

`domain: pass`, `layers: pass`, `decisive_step: analytical`.

The deciding quantity is risk-standardised excess complications - observed less expected over
published stratum rates, carried to ultimate against a coding run-off and scaled onto planned
activity - which is the core work of a health-service indicator analyst, not a stated score or a
list check; the swap test fails to survive it, because putting school or substation nouns in loses
both the stratum risk model and the coding close-out that the quantity is built from. Layer 1 is
the two national list revisions across a mid-year boundary, a fiscal-against-calendar ask, a campus
whose complication detail sits in another module, monthly facility reassignment and duplicate
sub-acute rows; Layer 2 is estimating the complications the quarters will settle at, per cost
centre, before computing the excess. The easy route a strong analyst who cleaned everything and
read every rule correctly still takes: compute avoidable complications on the ten closed quarters
as the extract and the series record them, and file Alderbrook General Surgery (41220) at 26.1.

---

## Fix

**prompt** (one clause), plus **solution** (one regenerated figure).

1. Pin the completion method in the asking sentence or, better, in the charter extract so it governs
   for every solver: carry each unfinished quarter to the count it settles at on the cost centre's
   own settled quarters, weighting each development step by the complications published at it. One
   sentence closes options 4 to 9 onto a single printed answer. Also say explicitly whether the
   expected side is taken on the coded episodes or carried for the episodes still awaiting coding,
   because the register ships `episodes_awaiting_coding` and that choice moves the headline from
   44.6 to 36.6 while leaving the winner alone.
2. Re-cut so no graded cell sits within 0.03 of its printed bin edge. 41240 at 11.5414 / 11.5646
   straddles 11.55, and the stated factor 1.0368 sits 0.000015 from its edge.
3. Regenerate 41320's cell: on the method the blocks describe it is **14.8**, not 14.9.
4. Fix Critical Component 1's publication labels to 5th, 4th, 3rd, 2nd and own close, and the notes'
   "28 February" to 25 February.

The main recommendation, the ladder and the stump need no change: Alderbrook General Medicine, cost
centre 41210, is the answer under every reading the shipped rules leave open, by 1.6x.
