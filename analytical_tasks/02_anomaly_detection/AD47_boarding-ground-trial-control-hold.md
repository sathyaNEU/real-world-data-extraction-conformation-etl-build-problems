# AD47 — Which approaches keep the outer pilot boarding grounds, or does the trial run on, when waiting fell on every approach

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · port pilotage |
| Mirrors | Geo and switchback experiments where a change rolled out to a few regions must beat what the untouched regions did by themselves (city-level dispatch and pricing tests at Uber and Lyft, delivery-station process trials at Amazon, geo experiments on ad spend at Google), where trip- or order-level precision hides region-level noise |
| Decision shape | A structure the body adopts, or a hold forced by a blocking quantity: the pilotage committee's boarding-ground plan (which of the three trial approaches keep their outer grounds for good) or another season of trial |
| Committed call | The approaches whose outer grounds become permanent, or that the trial runs another season, with South's lower 90% bound on its net cut in pilot-caused waiting, in percentage points to one decimal, against the 10 the plan requires |
| Gap · Pattern | Gap 4 (rule: what counts as a cut beyond what would have happened anyway) over Gap 2 (population: which waits are pilot-caused) · hold forced by a gap smaller than between-approach variation, a counterfactual baseline built from the untouched approaches and the ledger's own past seasons, with the population a flag suggests below it |
| Gate G mechanism | signal_vs_noise_or_hold, with decomposition_attribution support |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #4 never tests its reading against the control · #2 counts file rows instead of the real unit |
| Calibration form | Settled ledger: the pilotage service's settled invoices from 2022 to the trial's end, each job's approach, ordered and actual boarding times, the waiting charged and the cause settled with the ship's agent (pilot, berth, vessel or weather) |
| Driving force | Pilot-caused waiting fell on the trial approaches, 28% on South and 24% on West, and it also fell on the three untouched approaches, by 6% to 20%, as it does in these weeks every year by a different amount on each approach. The plan keeps an outer ground only where the cut beats what would have happened anyway by 10 points with 90% confidence. Net of the untouched approaches, South's excess is 15 points and West's 11, and the ledger's past seasons show an approach's net change swinging with a standard deviation of 7.0 points when nothing changed. At that spread South would need 19 points; its lower bound is 6.0, so no approach qualifies and the trial runs on. |

## 1. Situation

A port's pilotage service moved the pilot boarding grounds of three of its six approaches (South, West and Southeast) further out to sea
for a twelve-week trial, so that ships meet their pilot under way instead of waiting for the boat. The trial plan makes an outer ground
permanent on any approach where the trial cut pilot-caused waiting by at least 10% beyond what would have happened anyway, with 90%
confidence; otherwise the trial runs another season. The pilotage committee meets on the 20th. The service holds AIS tracks for every call,
the dispatch log, the settled invoices since 2022, the pilot roster, weather records, the tug log and the pilot order file. The harbour master
is sure the outer grounds work.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: AIS waiting, the dispatch log's flags, the settled causes and the falls on every approach. The harbour
  master is right that waiting fell where the grounds moved. Nothing is overturned; the difficulty is how much of the fall would have
  happened anyway, and how sure twelve weeks on one approach can make anyone.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the berth opening. Before and after on settled pilot-caused waiting is still the natural build
  and still adopts South and West.
* **Instrument repair.** Suspect file: the dispatch log's "pilot late" flag, which records late assignment of a pilot (a narrower meaning of
  pilot-caused waiting) and marks 61% of the waits the invoices settle as pilot-caused. Repaired to mark every pilot-caused wait, rung 1
  becomes rung 2 and adopts South and West; rung 0 still adopts South and Southeast on AIS waiting, and rung 2 is unchanged. The AIS tracks
  and the invoices are complete. The hold still needs the untouched approaches' baseline and the ledger's between-approach variation: a
  perfect record of every wait's cause says nothing about what would have happened anyway.
* **Lens swap.** The naive comparison is each trial approach before and after; the answer's is each trial approach against what the
  untouched approaches did in the same weeks, judged against how far that comparison swings when nothing changes: a different counterfactual
  and a different unit of evidence.

## 3. The driving force

A strong solver drops AIS waiting (Southeast's fall is berth waiting after its new container berth opened), rebuilds pilot-caused waiting from
the settled invoices rather than the dispatch flag, and finds South down 28% and West 24%. It then notices that the untouched approaches fell
too, nets out their mean of 13%, and finds South 15 points clear and West 11, both over the bar. With twelve weeks of jobs on each approach, a
job-level interval on South's net is ±3.1 points, and South clears 10 comfortably. Every step is correct, and the interval treats jobs as the
unit of evidence. The boarding ground was moved for whole approaches, so the trial has three treated approaches and three untouched ones, and
the counterfactual for an approach is uncertain by how much approaches differ from each other in a season with no change. The ledger shows it:
in 17 past approach-seasons with nothing changed, an approach's twelve-week change net of the others swung with a standard deviation of 7.0
points. At that spread South's lower bound is 6.0 and West's 2.0, and the plan's standard is not met.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | AIS waiting at the boarding area, all causes, twelve weeks before against twelve during: S −19%, W −9%, SE −40% | Adopt South and Southeast | The trial's outcome on the cleanest record of every call | The settled invoices: Southeast's fall is berth waiting after its new container berth opened in week 3, and the plan measures pilot-caused waiting |
| 1 | Pilot-caused waits as the dispatch log flags them, before and after: S −31%, W −6%, SE −4% | Adopt South | The service's own record of a pilot being late | The settled invoices: the flag marks 61% of the waits settled as pilot-caused, missing every wait where the boat reached the ground late, most of West's |
| 2 | Invoice-settled pilot-caused waiting, before and after: S −28%, W −24%, SE −8% | Adopt South and West | The plan's measure, on the settled record | The untouched approaches: their settled pilot-caused waiting fell 6%, 13% and 20% over the same twelve weeks |
| 3 | **Decisive:** each trial approach's fall net of the untouched approaches' mean (13%), judged at the between-approach variation of the ledger's past seasons (standard deviation 7.0 points): S +15, W +11, SE −5; lower 90% bounds 6.0, 2.0 and −14.0 against the 10 required | **Hold: no outer ground is made permanent, and the trial runs another season** | — | — |

* **The blocking quantity.** South's lower 90% bound on its net cut is 6.0 points against the 10 required: at the ledger's spread a net cut
  must reach 10 + 1.282 × 7.0 = 19.0 points to qualify, and South's is 15. West's bound is 2.0 and Southeast's −14.0. Every approach fails the
  same standard.
* **Partial correction priced (L3).** A solver who nets out the untouched approaches but stops at the point estimates adopts South and West,
  15 and 11 points against 10. A solver who puts a job-level interval on the net (±3.1 points) adopts South alone, its bound 11.9 against 10.
  A solver who uses approach-level variation on the flagged waits adopts South, whose flagged net cut is 23 points (bound 14.0). Each commits
  to a structure, and none holds.
* **Grid.** Waiting population (AIS, flagged, settled) × standard (before and after; net point estimate; net with a job-level interval; net
  with approach-level variation) = 12 cells. AIS cells adopt South and Southeast, and Southeast alone at approach level (its berth-driven net
  is 35 points); flagged cells adopt South in every column; settled cells adopt South and West before and after and on the point estimate,
  South with a job-level interval, and hold only with approach-level variation. The nearest wrong cell is the job-level interval, which needs
  only the unit of evidence changed to reach the answer.
* **Falsifiable.** South would have been adopted with a net cut of 19.0 points or more, or had the ledger's past seasons swung with a
  standard deviation of 3.9 points or less.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The plan says "beyond what would have happened anyway" and "with 90% confidence"; no document says which approaches
   stand in for "anyway", or that the approach, not the job, is the unit of evidence.
2. **Pinned by the ledger's past seasons, a construction from complete records.** In the 17 approach-seasons of 2022–2024 with no change to
   any boarding ground or boat station, an approach's twelve-week change net of the other five's mean ranged from −12 to +13 points (standard
   deviation 7.0), and a job-level interval would have called 11 of the 17 real. The counterfactual is built per approach and season from the
   invoices, and every approach-level standard (the past-season spread, a prediction interval on the three untouched approaches, the 90th
   percentile of the past net changes) puts South's bound between −0.2 and 6.0.
3. **No arithmetic symptom.** Every wait carries one settled cause, AIS boarding times tie to the invoices, and every fall reproduces from
   the records.
4. **Not a row predicate.** The baseline needs each untouched approach's twelve-week change, and the variation needs every past
   approach-season's change net of the others: aggregates of aggregates over three years of invoices.
5. **The enumeration is arithmetic.** Each approach's net cut and bound are computed; no column holds either.
6. **No cutover date.** The berth opening in week 3 is decoy material on Southeast's AIS waiting; the hold rests on a spread with no date
   in it.
7. **Survives deletion.** Remove both voices and the berth opening, and before and after on settled waits still adopts South and West.

## 6. The calibration corpus

* **Form.** The settled ledger: every pilotage job from January 2022 to the trial's end, with its approach, ordered and actual boarding
  times, the waiting charged and the cause settled with the agent.
* **What it pins.** The pilot-caused population (the flag covers 61% of it, and under a third of West's) and the between-approach variation
  (above).
* **Twin pair.** In the same twelve weeks of 2024, North and Northeast were identical on every visible column (calls, ship-size mix, roster
  cover, weather days and ordered-time profile), and neither changed anything. North's settled pilot-caused waiting fell 26% and Northeast's
  12%, 2.2× apart. A job-level test calls the gap real many times over; only the approach-level spread reads it as an ordinary season.
* **Resemblance points at the decoy.** The ledger's one past change, the 2023 move of West's boat station, cut West's pilot-caused waiting
  by 27% and it stayed down; on every column South's trial weeks resemble it.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The trial plan: an outer ground becomes permanent on an approach where the trial cut its pilot-caused waiting by at least
  10% beyond what would have happened anyway, with 90% confidence; otherwise the trial runs another season. The invoice terms: waiting is
  charged with a cause settled with the agent. The dispatch log's field guide: "pilot late" is set when a pilot is assigned after the ordered
  time. One sentence each.
* **Empirical pins.** The between-approach variation, from the ledger's past seasons; the pilot-caused population, from the invoices.
* **Voices.** The harbour master: "Ships are getting their pilots sooner on the outer grounds; I see it every morning." The pilots'
  association chair: "The new grounds work, and the numbers will show it."
* **Licensed wrong basis.** The plan records that the ship agents' association measures the trial by AIS waiting before and after and will
  publish its own figures.

## 8. Determinism by construction

* **Windows.** Twelve weeks before and twelve during, the same calendar weeks in every past season; no job straddles a window edge.
* **Causes.** Every wait carries exactly one settled cause, and no trial-week invoice was disputed after settlement.
* **Variation.** The past-season spread is 7.0 points whether each approach is netted against the other five or against the untouched three
  only. Every approach-level standard puts South's bound under 10 (−0.2 to 6.0), and every job-level standard puts it over (11.1 to 11.9).
* **Rounding.** Changes are reported to whole percentage points and bounds to one decimal.

## 9. Prompt sketch and deliverables

> The boarding-ground trial ends on Friday and the committee meets on the 20th. Our harbour master says ships are getting their pilots
> sooner on the outer grounds. Tell me which approaches keep their outer grounds for good, or that the trial has to run another season, in
> a line for the committee, with the figure that decides it in percentage points to one decimal. Send `trial_case.xlsx`, a chart
> `net_cut_by_approach.png`, and a one-page `committee_note.pdf`.

* `trial_case.xlsx` — the three trial approaches under each rung's basis (ask C), the tug sheet (ask A) and the order sheet (ask B).
* `net_cut_by_approach.png` — the twelve-week change in settled pilot-caused waiting on all six approaches as bars, the untouched mean as a
  line, each trial approach's net cut with its job-level and approach-level 90% intervals, the 10-point bar drawn and labelled, and the verdict
  in the title.
* `committee_note.pdf` — the committed verdict, the blocking quantity and what would have adopted an approach.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each approach, tug jobs in the trial weeks and median tug hours per job. *Device:* a tug job
  that runs through a shift change is booked as two rows under one job number, one per crew, and the tug log guide counts one job per job
  number; counting rows inflates jobs and shortens hours on four approaches. The verdict never reads the tug log.
* **Ask B (device-carried).** For each approach, pilot orders in the trial weeks and the share amended at least once. *Device:* an amended
  order is re-filed under its number with a revision suffix (P-30215-R2), and the order guide treats the latest revision as the order;
  counting rows inflates orders and amendments on every approach. The invoices carry each job's final ordered time, so the verdict never
  reads the order file.
* **Ask C (validity).** For each trial approach, the change and the verdict under each of the four rung bases.
* **Decoupling.** Clearing the settled-cause population and the approach-level variation changes no figure in asks A or B.

## 11. Rubric arithmetic

6 approaches × 2 (ask A) + 6 × 2 (ask B) + 3 trial approaches × 4 bases × 2 (ask C) + the committed verdict, the blocking quantity, West's
bound and the falsifiability margin + 5 named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* Twelve weeks before and twelve during. Trial approaches South, West and Southeast; untouched North, Northeast and East.
* AIS waiting, all causes: S −19%, W −9%, SE −40%, untouched −4%, −5% and −6%. Southeast's new berth opens in week 3 of the trial.
* Flagged waits: S −31%, W −6%, SE −4%, untouched −7%, −8% and −9%. The flag covers 61% of settled pilot-caused waits overall and under a
  third of West's.
* Settled pilot-caused waiting: S −28%, W −24%, SE −8%, untouched −6%, −13% and −20% (mean 13).
* Past seasons: 17 approach-seasons with no change (2022–2024, excluding West in 2023), net changes from −12 to +13 points, standard
  deviation 7.0 on settled and on flagged waits and 8.0 on AIS waiting. Job-level standard errors of a net change: S 2.4, W 2.6, SE 2.2 points.
* North and Northeast in 2024 are identical on every visible column and fell 26% and 12%.
* Tug jobs and pilot orders never touch the invoices' waiting, causes or ordered times.
