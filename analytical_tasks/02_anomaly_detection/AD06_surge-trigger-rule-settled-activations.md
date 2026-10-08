# AD06 — Which surge trigger the network adopts when the authority stops publishing its own, and only one rebuilt rule settles every week the agency was paid for

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · healthcare surge staffing contracts |
| Mirrors | Rebuilding a retired third-party trigger so that a contract keyed to it keeps settling the same way (capacity-reservation triggers at cloud providers, surge-pricing triggers in ride-hailing marketplaces, peak-hiring triggers in Amazon-scale fulfilment networks) |
| Decision shape | A structure the body adopts: the surge-activation rule (signal grain, baseline weeks, threshold form), scored by the contract on reproducing every settled activation week |
| Committed call | The activation rule the surge committee adopts on 3 December 2026, and the 2026/27 threshold it sets, as a weighted ILI percentage to two decimals |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B with a reproduction gate (E01), whose decisive component is a run construction on a different file; two flawless grains at the lower rung (E07) |
| Gate G mechanism | method_or_model_selection, with signal_vs_noise_or_hold support |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #2 counts file rows instead of the real unit |
| Calibration form | Settled-transaction ledger: the agency contract's 64 settled activation weeks across seven seasons |
| Driving force | The authority's baseline is the mean plus two standard deviations of "non-epidemic weeks" over five seasons, and nothing defines those weeks. Cutting them out of the signal itself always keeps epidemic shoulders and lifts the baseline. The ledger is reproduced only when the weeks are built from a different file: runs of two or more weeks in which lab-confirmed respiratory admissions stayed below 15% of that season's peak. That construction sets the lowest threshold any rule can reach, and every rival under-activates. |

## 1. Situation

A hospital network staffs a surge unit with agency nurses whenever the regional respiratory signal crosses its baseline. For seven seasons
the regional health authority published the weekly trigger status and the agency was paid for every activation week, settled after
reconciliation. From this winter the authority stops publishing it. The contract lets the network substitute its own rule if, replayed on
the seven settled seasons, it reproduces every settled activation week and no other. The surge committee adopts the rule on 3 December.
The pack carries the sentinel providers' weekly visits and ILI visits for twelve seasons, the provider register with served populations,
the region's lab-confirmed admissions, the authority's method note and the settled ledger.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: visits, ILI counts, served populations, admissions and the settled ledger. The authority's method
  note is accurate as far as it goes. Nobody's number is overturned and no stakeholder read is corrected; the difficulty is building the
  undefined part of the rule so that the record reproduces.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the workforce director's memory of the old trigger and the agency's view. A careful replay still lands at 57 or
  59 of 64 with a cut on the signal itself, and a strong solver still ships it.
* **Instrument repair.** No file the ladder uses is suspect: sentinel visits, served populations, admissions (reported within three weeks,
  extracted ten weeks after the last closed season) and the settled ledger are complete and final, and no field claims to mark a week as
  epidemic. Perfect sentinel reporting leaves rung 0 at 4.71%, rung 1 at 3.86% and rung 2 at 2.71%, because each takes its baseline weeks
  from the signal it judges. The method note's silence on non-epidemic weeks is the rule the task recovers by reproduction from complete
  records, not a gap in a record, so the admissions-run construction is still needed for 2.38%.
* **Lens swap.** The naive baseline is built from weeks chosen by the signal it is meant to judge; the answer's baseline is built from a
  different population of weeks, chosen by admissions in another file, so rival rules disagree on which weeks enter, not on how one set is
  read.

## 3. The driving force

A strong solver reconstructs the signal from the sentinel file, reads "mean plus two standard deviations of non-epidemic weeks over five
seasons", replays it, finds too few activations, and fixes the obvious problem: epidemic weeks are inflating the baseline. It cuts them
out with each season's own upper quartile, or with the textbook laboratory rule it knows, and the replay climbs to 57 or 59 of 64. Every
miss is a settled week the rule leaves below threshold, so the residue reads like a slightly conservative baseline, and #1 and #3 are
where it stops. Any cut defined on the signal keeps the epidemic shoulders in the baseline, because shoulders are not extreme in the
signal. The weeks that reproduce the ledger come from admissions: a week enters the baseline when it sits in a run of two or more weeks
whose lab-confirmed respiratory admissions are below 15% of that season's peak. That needs a season-level maximum, a run construction and
a join from the admissions file to the signal weeks, and it is the only rule that settles all 64 weeks.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Signal pooled across sentinel visits, baseline on all weeks of the five preceding seasons, mean plus two SD | 4.71%, +97.9% (21 of 64 settled weeks) | The method note read literally on the signal the sentinel file builds | The contract defines the regional signal as each provider's ILI share weighted by the population it serves, and four large urgent-treatment centres dominate pooled visits |
| 1 | The contract's population-weighted signal, same baseline | 3.86%, +62.2% (33 of 64) | The right grain, each figure checked against the provider register | The ledger: all 31 misses are settled weeks the rule leaves unactivated, the signature of epidemic weeks inside the baseline |
| 2 | Weighted signal, baseline excluding each season's weeks above its own 75th percentile | 2.71%, +13.9% (57 of 64) | The natural repair, close to the record, every miss a borderline shoulder week | The ledger: seven settled weeks, all in seasons that follow a long epidemic, stay unactivated |
| 3 | **Decisive:** weighted signal, baseline on weeks in runs of two or more whose lab-confirmed respiratory admissions are below 15% of that season's peak | **2.38%** (64 of 64, no unsettled week) | — | — |

* **Figure shape.** The answer is the minimum cell: every correction walks the threshold down, and every rival rule sets a higher
  threshold and under-activates. Per-rung offsets are +97.9%, +62.2% and +13.9%.
* **Partial correction priced (L3).** A solver who finds the admissions construction but keeps the pooled signal reproduces 46 of 64 and
  sets 2.90% (+21.8%), further than rung 2. The textbook laboratory rule on the weighted signal, the nearest construction a knowledgeable
  solver tries, reproduces 59 of 64 and sets 2.62% (+10.1%).
* **Grid.** Grain (pooled or weighted) × baseline weeks (all, upper-quartile cut, calendar summer, textbook laboratory rule, admissions runs)
  gives ten cells. Only weighted × admissions runs reproduces 64 of 64; every other cell sets a higher threshold, the nearest at +10.1%
  (59 of 64), and every pooled cell sits at least 21.8% above.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The method note names "non-epidemic weeks" and never defines them. No document links the admissions file to the
   baseline.
2. **The corpus pins a construction, not a menu.** The admissions-run rule reproduces 64 of 64 settled weeks with no false activation; the
   best rival, the textbook laboratory rule, 59 of 64, and every rival's misses are settled weeks left unactivated, so each fails on the
   season totals too. The reproducing rule is a construction: its weeks come from a season maximum, a run of consecutive weeks and a join
   to another file, and no cut on the signal can produce them.
3. **No arithmetic symptom.** The weighted signal ties to the authority's published annual summaries, admissions tie to the hospital returns,
   and every replay runs cleanly; the rivals simply activate fewer weeks.
4. **Not a row predicate.** It needs each season's peak, a share of it per week, runs of at least two consecutive qualifying weeks, and a
   baseline recomputed for every replayed season from the five before it.
5. **The enumeration is arithmetic.** Which weeks enter each baseline is computed; no field marks a week as epidemic.
6. **No cutover date.** The rule is stationary over all twelve seasons; no series steps.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The agency contract's settled ledger: 64 activation weeks across seven seasons, each invoiced, reconciled and settled, with the
  weeks of the seven seasons that were not activated implicit in their absence.
* **What it pins.** The admissions-run rule on the weighted signal reproduces all 64 settled weeks and activates no other; the rivals reach
  21, 33, 49 (calendar summer), 57 and 59, every miss in the same direction.
* **Twin pair.** Seasons 2017/18 and 2023/24 are identical on peak weighted signal (6.84%), onset week, weeks above 4%, epidemic length and
  total ILI visits. The ledger settled 14 activation weeks in 2017/18 and 7 in 2023/24, because the admissions runs of their preceding
  seasons set baselines of 2.21% and 3.05%; no rule built from the signal alone separates them.
* **Every rule exercised.** One season's admissions dip below 15% for a single week mid-epidemic, so the run length is tested. One summer
  carries a back-to-school respiratory wave in the signal with no lab-confirmed admissions, so a calendar rule and a signal cut disagree.
* **Resemblance points at the decoy.** The last closed season most resembles 2018/19, a season the upper-quartile rule reproduces exactly.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The contract: the network may substitute a rule that, replayed on the seven settled seasons, reproduces every settled
  activation week and no other. The contract's definition: the regional signal is each sentinel provider's ILI share weighted by the
  population it serves. The method note: the baseline is the mean plus two standard deviations of non-epidemic weeks over the five
  preceding seasons, seasons running from week 40 to week 39.
* **Empirical pins.** The admissions-run definition of non-epidemic weeks, from the ledger.
* **Voices.** The workforce director: "The old trigger was a line through every week of the last five winters, nothing cleverer." The
  agency's account manager: "The big urgent-care sites see the flu first; their visits are the signal."
* **Licensed wrong basis.** The contract records that the agency's account team replays activations on the visit-pooled signal and will
  present that replay to the committee.

## 8. Determinism by construction

* **Share of peak.** At every onset and offset, admissions move from below 10% to above 25% of the season's peak within one week, so any
  cut from 10% to 25% qualifies the same weeks.
* **Run length.** Outside summer no qualifying week stands alone except the one mid-epidemic dip, which runs of two or three both exclude.
* **Standard deviation.** Sample and population SD move every threshold by under 0.004 points, and no replayed week sits within 0.01 of
  its threshold.
* **Maturity.** Lab-confirmed admissions report within three weeks and the extract is taken ten weeks after the last closed season.
* **Rounding.** 2.38% sits mid-bin at two decimals.

## 9. Prompt sketch and deliverables

> From this winter the authority stops publishing its surge trigger, and our agency contract pays on activations, so on 3 December the
> committee has to adopt a trigger rule of its own. Our workforce director remembers the old trigger as a simple line through the last
> five winters. Tell me the rule we adopt and the threshold it sets for 2026/27, to two decimals, in two sentences for the committee
> paper, with `trigger_rule.xlsx` holding the sheets below, a chart `trigger_replay.svg`, and `committee_paper.docx`.

* `trigger_rule.xlsx` — the rule build and replay, the bed sheet (ask A), the absence sheet (ask B) and the rule comparison (ask C).
* `trigger_replay.svg` — the weighted signal for the seven settled seasons, the adopted rule's replayed threshold as a step line, settled
  activation weeks shaded, the upper-quartile rule's misses marked, and the twin seasons labelled.
* `committee_paper.docx` — the adopted rule, its threshold, and why the agency's replay and the textbook rule are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight hospitals, occupied general and acute beds in the peak week of each of the
  last three seasons. *Device:* the daily bed return reports core and escalation beds in separate fields, and the return guidance counts
  both as occupied. Reading core beds alone understates every hospital that opened escalation wards, five of the eight in the latest
  season. The trigger never reads bed returns.
* **Ask B (device-carried).** For each hospital, nursing sickness-absence days and the absence rate in the last season's eight peak weeks.
  *Device:* an absence episode is recorded once, at its start date with a duration, per the HR guide. Counting by start date puts every
  day of an episode spanning the window's edge in the wrong place and misstates three hospitals.
* **Ask C (validity).** For each of the five candidate rules (rungs 0–3 and the textbook laboratory rule), the settled weeks it reproduces
  out of 64 and the 2026/27 threshold it sets.
* **Decoupling.** Clearing the admissions construction changes no figure in asks A or B.

## 11. Rubric arithmetic

8 hospitals × 3 seasons (ask A) + 8 hospitals × 2 (ask B) + 5 rules × 2 (ask C) + the adopted rule's grain, baseline weeks and form, its
threshold and its last-season activation weeks + 5 named chart parts + 3 files ≈ 63 criteria.

## 12. World-building constraints

* Thresholds: 4.71 / 3.86 / 2.71 / 2.38; textbook rule 2.62; calendar summer 2.96; pooled cells are 1.22× their weighted twins. Every
  rival sets a higher threshold than 2.38 and activates fewer weeks.
* Reproduction: 21, 33, 57, 59 and 64 of 64; the calendar-summer rule 49; no rule activates an unsettled week.
* The four urgent-treatment centres hold 41% of sentinel visits and 9% of the served population, with ILI shares above the regional mean.
* Seasons 2017/18 and 2023/24 are identical on every signal-level column; their baselines are 2.21% and 3.05%.
* Admissions jump across the 10–25% band within one week at every onset and offset; one summer wave appears in the signal only.
* Escalation beds and absence episodes never touch the sentinel file or the admissions runs.
