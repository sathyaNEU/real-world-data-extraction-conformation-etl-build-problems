# DS50 — Which hours next quarter's flexible batch runs in, when every schedule on the table fails one of the policy's conditions

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · carbon-aware compute scheduling |
| Mirrors | Placing flexible load in hours chosen on marginal rather than average emissions, under site and grid conditions that rule out the obvious windows (carbon-aware batch scheduling at cloud providers, EV fleet smart-charging windows, demand-flexibility commitments at industrial sites) |
| Decision shape | An allocation under a cap: next quarter's daily 40 MWh of flexible batch placed in hours of the day, under the site's 48 MW connection cap |
| Committed call | The hours the batch runs in each day, and the marginal emissions the schedule avoids over the quarter against the overnight status quo, in tonnes of CO2 to the nearest ten |
| Gap · Pattern | Gap 4 (rule) over Gap 3 (objective) · E13, the admissible option is off the slate (each of the three schedules proposed fails a stated condition; the policy admits any schedule of up to two blocks that meets them all, and exactly one does), with a suppressed cell bounded (E25) at rung 2 |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #9 picks from the offered options when none passes · #24 treats an unpublished figure as unknown · #10 notes a binding limit as a risk |
| Calibration form | Pilot log: the six-week pilot in which batch blocks were moved through trial hours at the site, with metered site load, IT load and chiller mode by hour |
| Driving force | The batch is meant to run where it causes the least extra emission, and the grid's average intensity, lowest at night, says nothing about that. Each schedule on the table fails something: the midday block breaches the connection cap once the chillers' response is metered, the split schedule misses the emissions target once a suppressed evening cell is bounded, and the night schedule cuts nothing. The policy does not allow choosing the least bad or keeping the status quo. One schedule the team never proposed passes every condition. |

## 1. Situation

A cloud provider runs 10 MW of flexible batch for four hours a day at its north-west site, overnight from 01:00, when the grid's average
carbon intensity is lowest. Its scheduling policy now requires next quarter's schedule to cut the batch's marginal emissions by at least
40% against that status quo, using the grid operator's published marginal factors, while keeping the site within its 48 MW connection
cap, clear of the 17:00–21:00 window it sold to the operator, and after the day's data lands at 08:30. The sustainability team has put
three schedules on the table, and it favours the overnight hours.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the operator's marginal and average factors, the site's metered load, the pilot log, the connection
  agreement, the flexibility contract and the data pipeline's landing time. No stakeholder read is overturned: the night is cleanest on
  average, and each proposed schedule is a reasonable idea. The difficulty is that none of them meets the policy.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the team's preference and every voice. The three proposals still each fail one condition, and an analyst who
  evaluates only them still ends on the closest or on the status quo.
* **Instrument repair.** Suspect file: the operator's marginal-factor table, which suppresses the 21:00 cell. Repaired with the cell itself,
  0.74 t/MWh, rung 0 still names S3 and rung 1 S1, and rung 2 can no longer pass S2, so it stops at the least bad of three failing
  proposals or the status quo. No other file is suspect: the pilot log, the site's metered load and the operator's other cells are
  complete. The schedule that passes is found only by searching every schedule the policy allows, which no repair supplies.
* **Lens swap.** The naive read and the answer differ in rule, not population or moment: the options on the table, against the set the
  policy admits.

## 3. The driving force

A strong solver discards average intensity, prices each proposal at the operator's marginal factors, and checks the conditions. S1, the
midday block 12:00–16:00, cuts emissions by half on the batch's IT energy and fits under the cap at 10 MW. But the pilot log shows each MW
of batch adds 1.18 MW at the meter on summer afternoons, when the chillers work hardest, and at 13:00 the site would draw 48.8 MW. S2 splits
the batch into 15:00–17:00 and 21:00–23:00 and cuts 48% if the suppressed 21:00 cell is filled from its neighbours. The operator
publishes the season's daily average to three decimals alongside every other hour, and the identity puts 21:00 at 0.72 to 0.74, when an
oil-fired unit sets the margin: S2 cuts only 30%. S3, 23:00–03:00, cuts nothing. A careful analyst now recommends the least bad, or the
status quo. The policy allows neither: the schedule must meet every condition, and any schedule of up to two blocks of at least two hours
is admissible. Searching them, exactly one passes: 09:00–11:00 and 15:00–17:00, a 42.6% cut.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The team's ranking of its three proposals on the grid's average intensity | S3, 23:00–03:00 (0.046 t/MWh, the slate's lowest) | The published intensity everyone quotes, and the team's own view | The scheduling policy: the batch is judged on the operator's marginal factors, the emissions an added load causes |
| 1 | Marginal factors on the batch's IT energy, the cap checked at 10 MW | S1, the midday block, cutting 50% and drawing 47 MW at 13:00 | The right factors, and every condition checked | The pilot log: each MW of batch adds 1.18 MW at the meter on summer afternoons, so S1 draws 48.8 MW at 13:00 against the 48 MW cap |
| 2 | Metered energy and load; S1 out; the suppressed 21:00 factor filled from its neighbours | S2, 15:00–17:00 and 21:00–23:00, cutting 48% | Every condition passed by the one proposal left | The operator's published daily average: with the other 23 hours it bounds 21:00 at 0.72 to 0.74, and S2's cut falls to 30% |
| 3 | **Decisive:** the policy's admissible set, every schedule of up to two blocks of at least two hours after 08:30, searched against all four conditions; exactly one passes | **09:00–11:00 and 15:00–17:00, avoiding 860 t a quarter** | — | — |

* **Figure shape.** Rungs 1 and 2 book 970 and 980 t a quarter on schedules that cannot run; the answer, 860 t, sits 11% below the
  nearest of them, and no other cell commits the answer's hours.
* **Position table.** The answer is never on the slate, so no intermediate rung names it. On rung 0's reading it is the 5th of the five
  schedules a reader would rank (S3, the status quo, S1, S2, then the answer, at 0.061 t/MWh). Rung leaders are S3, S1, S2, then the
  answer.
* **Discriminator dominance.** S2 carries a 1.11× emissions advantage over the answer into rung 3 under the neighbours' fill (11.3 t a day
  against 12.6). The bound turns it into a gate: S2's cut is 30%, ten points short, at either end of the bound, so its eligible value is
  nil and no ratio carries it back. Among schedules that do not touch 21:00, the nearest to passing, 15:00–17:00 and 22:00–24:00, cuts
  39.1%.
* **Partial correction priced (L3).** No half-applied search lands on the answer. Searching with the 21:00 cell filled, from its
  neighbours or from the daily average, finds S2 best, 3.6% to 10% below the answer, and commits it at 900 to 980 t. Searching single
  blocks only finds nothing that passes (the best, 09:00–13:00, cuts 36%) and falls back to the least bad proposal. Searching with the cap
  checked at IT load commits 13:00–17:00, which breaches it, at 900 to 980 t.
* **Grid.** Energy basis (IT, metered) × the 21:00 cell (filled, bounded) × candidate set (the slate, single blocks, the policy's two
  blocks) = 12 cells. The slate cells name S1, S2 or nothing; single blocks pass nothing; the two-block search names 13:00–17:00 on IT
  energy, S2 with the cell filled, and the answer only on metered energy with the cell bounded.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy lists the conditions and says any schedule of up to two blocks is admissible. No document lists a
   schedule that meets them, or says the slate fails.
2. **The conditions pin it, and the pilot pins the meter.** Exactly one of the 190 schedules the policy's block rules admit passes all
   four conditions; the next best cut 39.1% and 38.8%. The pilot log reproduces the site's metered load from IT load and chiller mode in 1,008
   of 1,008 pilot hours within 0.2 MW, which is what rules S1 out.
3. **No arithmetic symptom.** Every proposal's figures are positive and plausible, the factors reconcile to the operator's daily average,
   and the status quo's emissions match the site's metered nights.
4. **Not a row predicate.** Admissibility is a search over block pairs, each tested hour by hour against the metered cap and as a whole
   against the emissions floor.
5. **The enumeration is arithmetic.** No file lists admissible schedules or marks a proposal as failing.
6. **No cutover date.** The policy's conditions apply to next quarter as a whole; nothing in the factor tables or the pilot steps.
7. **Survives deletion.** No wrong number exists to delete. Without the team's preference, the slate still fails and the search is still
   the only way to a passing schedule.

## 6. The calibration corpus

* **Form.** The six-week pilot: batch blocks moved through trial hours at the site, with metered site load, IT load, chiller mode and
  outdoor conditions by hour, 1,008 hours in all.
* **What it certifies.** The metered response: 1.05 MW per MW of batch at night, 1.08 in the morning and 1.18 on summer afternoons, with
  the chillers off economiser mode.
* **What it does not show.** Emissions, which come from the operator's factors, and any schedule's admissibility, which the search
  supplies.
* **Twin pair.** Two pilot days are identical on every column the pilot log's main table shows: the same 40 MWh of batch in the same
  15:00–17:00 block, the same IT load and the same dry-bulb temperature. Each MW of batch raised metered load by 1.09 MW on one and 1.18
  on the other, a cooling increment of 0.09 against 0.18 (2.0×): humid air took the chillers off economiser mode on the second, as the
  building system's mode log records. Only the mode log separates them.
* **Resemblance points at the decoy.** S1's midday block most resembles the schedule a sister site in a cooler zone runs within its cap.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The scheduling policy: the batch runs four hours a day at 10 MW, in at most two blocks of at least two hours, after the
  day's data lands at 08:30 and before 07:00; it must cut marginal emissions by at least 40% against the 01:00–05:00 status quo, at the
  operator's published summer factors, on metered energy; the site must stay within its 48 MW connection cap in every hour, and add no
  load from 17:00 to 21:00 under the flexibility contract; the committed schedule must meet every condition, and neither the status quo
  nor deferring the commitment is admissible. The team's three proposals.
* **Empirical pins.** The metered response, from the pilot; the 21:00 factor, bounded from the operator's published figures; the site's
  base load by hour, from last summer's meter.
* **Voices.** The sustainability lead: "The overnight hours are the cleanest on the grid." The site manager: "The connection has headroom
  for ten more megawatts." The batch platform lead: "Splitting the batch is fine as long as each block runs two hours."
* **Licensed wrong basis.** The policy records that the regional sustainability report presents the site's schedule against the grid's
  average intensity.

## 8. Determinism by construction

* **Factors.** The operator's summer weekday table applies to every day of the quarter, as the policy specifies; the bound on 21:00 comes
  from the daily average published to three decimals.
* **Meter.** The pilot's response by hour band is filed with its range; moving any band by 0.02 changes no schedule's standing against
  the cap or the floor.
* **Search.** Blocks start on the hour; every admissible schedule's cut is at least 0.9 points from 40%, and S2's at least ten.
* **Rounding.** The answer avoids 9.34 t a day, 859.2 t over the quarter's 92 days, clear of the nearest-ten edges.

## 9. Prompt sketch and deliverables

> Our flexible batch at the north-west site needs next quarter's daily schedule, and the sustainability team has three options on the
> table. They favour the overnight hours, when the grid is cleanest. Tell me which hours we commit the batch to and the emissions it
> avoids over the quarter, in tonnes of CO2 to the nearest ten, as the line for the quarterly plan. Send `batch_schedule.xlsx`, a chart
> `marginal_factors_by_hour.png`, and a one-page `quarterly_plan_note.pdf`.

* `batch_schedule.xlsx` — each proposal and the committed schedule against every condition, the search's passing schedule and its nearest
  rivals (ask C), the PUE sheet (ask A) and the job sheet (ask B).
* `marginal_factors_by_hour.png` — marginal and average factors by hour as two lines, the cap-bound hours, the contract window and the
  data landing shaded, the 21:00 bound drawn as a range, and the three proposals and the committed blocks marked.
* `quarterly_plan_note.pdf` — the committed hours, the avoided emissions, and why none of the three proposals can run.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each month of last year, the site's power usage effectiveness. *Device:* two of the 48
  power-distribution feeds were relabelled in June and report under new IDs, which the feed register cross-references. Summing the old IDs
  drops those feeds from IT energy from June on and overstates the ratio.
* **Ask B (device-carried).** For each of the 13 weeks of last quarter, batch jobs completed and their median runtime. *Device:* a job
  resumed from a checkpoint keeps its job ID and logs a second start, as the scheduler's guide documents. Counting starts as jobs
  overstates completions and halves the median for checkpointed jobs.
* **Ask C (validity).** For each of the three proposals, its standing on each of the five conditions; the bound on the 21:00 factor; and
  the passing schedule's daily emissions with the two nearest rivals'.
* **Decoupling.** Clearing the search changes no figure in asks A or B. Feed IDs and job restarts touch no factor, load, contract or
  schedule record.

## 11. Rubric arithmetic

12 months (ask A) + 13 weeks × 2 (ask B) + 3 proposals × 5 conditions + 2 bound ends + 3 schedule figures (ask C) + the committed hours,
the avoided emissions and the margin to the floor + 5 named chart parts + 3 files ≈ 69 criteria.

## 12. World-building constraints

* Marginal factors (t/MWh), summer weekday: 01–04 0.53, 0.53, 0.52, 0.51; 09 0.30, 10 0.31, 11 0.38, 12 0.28, 13 and 14 0.26, 15 0.24,
  16 0.27, 20 0.53, 21 0.74 (suppressed; bounded 0.72–0.74), 22 0.16, 23 0.54; daily average 0.425. Average intensity 0.046 to 0.050
  at night, 0.058 to 0.062 by day. Metered response 1.05 / 1.08 / 1.18.
* Base load 37.0 MW at 13:00 and 14:00, 36.0 at 15:00 and 16:00, 35.8–36.4 in the morning; the cap binds only at 13:00 and 14:00.
* Daily emissions: status quo 21.95 t; S1 12.27 t (cap breach); S2 15.47 t (29.5%), 11.32 t with the neighbours' fill; S3 22.26 t;
  answer 12.61 t (42.6%); next best 13.37 t (39.1%) and 13.43 t (38.8%).
* Feed relabelling and job restarts are independent of every main-call record.
