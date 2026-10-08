# FC05 — Where twelve leased batteries go for next spring's midday oversupply, when a dry year will bring the irrigation pumps back

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · electricity distribution planning |
| Mirrors | Placing a capped pool of mitigation where the problem will be next period rather than where last period's alarms fired (cloud capacity buffers after a regional spike, Amazon fulfilment overflow capacity after a one-off surge, CDN capacity at Google or Meta after an event-driven traffic peak) |
| Decision shape | An allocation under a cap: twelve 5 MW battery units placed across eight substations for one spring |
| Committed call | The number of units at each of the eight substations, and the midday back-feed still left to curtail over March–May, in MWh to the nearest 100 |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · Pattern A (past exceedance against forward yield), with the moderator in how a period treats the unit (the water year) and a quiet second trap below it |
| Gate G mechanism | forecasting, with binding_constraint support |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Pilot log: two 5 MW units piloted at two suburban substations last spring, with hourly charge and the substation's back-feed |
| Driving force | Last spring was a full-allocation water year, so the groundwater pumps on three agricultural substations sat idle at midday and those substations back-fed hardest. Next year's surface allocation is 15%, and in both closed springs with an allocation under 40% the same pumps added 9–14 MW of midday load and erased most of the back-feed. The pumps are accounts in the customer register, two joins from a substation's SCADA, and no document links them to the water year. |

## 1. Situation

A distribution utility in an irrigated valley serves eight substations: three mostly agricultural (Ag1–Ag3) and five suburban (S1–S5).
Rooftop solar makes them back-feed toward the transmission system at spring middays, and whatever back-feed the batteries do not absorb
has to be curtailed. For next March–May the utility has leased twelve battery units (5 MW, 20 MWh each). The programme charter places
them one at a time where each adds the most absorbed energy over the season, at most three per substation. The siting plan goes to the
state commission on 15 November.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the back-feed alarm export, labelled as a description of last spring, the SCADA history, the
  interconnection queue, the pilot log, the customer register and the planning assumptions. No one's claim about their own numbers is
  overturned. The difficulty is that next spring will treat the agricultural substations differently from the spring the alarms measured.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the alarm export and both voices. Last spring's SCADA back-feed, grown by the queue, still puts five units on
  agricultural substations.
* **Instrument repair.** Suspect: the interconnection queue, whose capacity column is DC nameplate where the commission's additions are
  AC. Restate every system in AC. Rung 0 still returns 2 · 2 · 2 · 1 · 2 · 1 · 1 · 1, rung 1 becomes rung 2's 2 · 2 · 1 · 2 · 2 · 1 · 1 ·
  1, and the pumps' return in a 15% year is still a property of a spring that has not happened.
* **Lens swap.** The naive read and the answer differ in moment: a full-allocation spring against a 15% spring, at the same substations.

## 3. The driving force

A strong solver treats the alarm ranking as a statement about the past. It reconstitutes each substation's midday flow, adds the rooftop
solar the queue will energise and checks the queue's units against the commission's totals. Each step is right, and each still treats next
spring as last spring plus solar. The agricultural substations back-fed last spring because the surface allocation was 100% and growers
left their wells off. The SCADA history covers five springs. In the two whose allocation was under 40% (5% and 30%), the same substations
carried 9–14 MW of midday pumping and back-fed a small fraction of what they did last spring. The pumping accounts sit in the customer
register, joined to substations through feeders. Next year's allocation (15%) is one line among thirty in the planning assumptions sheet.
Next spring Ag1's back-feed falls from 5,700 to 400 MWh, and three units that every earlier rung sends to Ag1 and Ag2 belong in the
suburbs.

## 4. The ladder

| Rung | Construction | Lands on (Ag1 · Ag2 · Ag3 · S1 · S2 · S3 · S4 · S5 units; MWh left to curtail) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Last spring's SCADA back-feed per substation (the alarm export's basis), placed by the charter's rule | 2 · 2 · 2 · 1 · 2 · 1 · 1 · 1; 6,780, +12% | The utility's own measure of where back-feed happens, placed exactly as the charter says | The interconnection queue: systems approved since last spring add back-feed, mostly in the suburbs |
| 1 | Last spring's flow plus each substation's queued capacity × the spring PV profile | 2 · 1 · 1 · 2 · 3 · 1 · 1 · 1; 17,370, +188% | The forward correction for solar growth: the loud trap beaten | **E15 (the quiet trap):** the queue's capacity column is DC nameplate; its listed AC ratings reproduce the commission's published additions, and DC does not |
| 2 | The same with each system's AC rating | 2 · 2 · 1 · 2 · 2 · 1 · 1 · 1; 14,650, +143% | Forward solar in the right units, every reconciliation tied, and the pilot's absorption reproduced day by day | The planning assumptions' 15% allocation, read against five springs of SCADA joined to the register's pumping accounts |
| 3 | **Decisive:** midday flow rebuilt with each agricultural substation's pumping at its level in the closed springs under 40%, plus queued AC solar, then placed | **0 · 0 · 1 · 3 · 3 · 2 · 2 · 1; 6,030 → 6,000 MWh** | — | — |

* **Figure shape.** Every rung over-places agricultural units (6, 4 and 5 against 1) and overstates the curtailment left (+12%, +188%,
  +143%). The only grid cells below the answer drop the queue's growth, which the loud trap has already forced every solver to add.
* **Partial correction priced (L3).** The natural way to use five springs is to regress each substation's back-feed on its installed
  rooftop capacity. At the agricultural substations the two dry springs were also the two with the least rooftop, so the fit charges the
  missing back-feed to capacity and projects Ag1 and Ag2 higher still: 6 agricultural units and 15,900 MWh left (+164%), further away
  than rung 2.
* **Grid.** Solar growth (none, DC, AC) × pumping (as last spring, five-spring average, allocation-matched) gives 9 cells, each with a
  different placement. The nearest wrong figures are rung 0 (+12%, five extra agricultural units) and DC with matched pumping (+34%, one
  unit moved from S1 to S5). The five-spring average places 3 agricultural units at +79%. The cells without solar growth sit 35% and 69%
  low.
* **Separation at the margin.** Under every rung the twelfth unit's absorption beats the best thirteenth by at least 5%, so the greedy
  placement never turns on a near-tie.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter, the queue dictionary and the planning assumptions never connect irrigation to back-feed, and the
   allocation is one planning line with no stated use.
2. **Corpus blind for a computable reason.** *On every pilot day pumping load at the pilot substations was zero, because neither serves a
   groundwater pumping account.* The pilot log reproduces the absorption arithmetic on 92 of 92 days and says nothing about pumps.
3. **No arithmetic symptom.** SCADA flows tie to feeder meters, AC additions tie to the commission, and the units sum to twelve under
   every rung.
4. **Not a row predicate.** Pumping load is a substation-level sum over accounts reached through feeders, conditioned on a property of
   the period (the allocation band) and recovered by matching springs, not read from a column.
5. **The enumeration is arithmetic.** Which substations stop back-feeding is computed by rebuilding flows. No field marks them.
6. **No cutover date.** Water years recur. Wet and dry springs alternate through the history, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete. Without the alarm export the same ladder starts at last spring's SCADA.

## 6. The calibration corpus

* **Form.** The pilot log: units at S1 and S2 for 92 spring days, with hourly charge and the substation's hourly back-feed.
* **What it certifies.** The absorption arithmetic: each hour the k-th unit at a substation takes the back-feed between 5(k−1) and 5k MW,
  and a unit's day stops at 20 MWh. That reproduces 92 of 92 days. An hourly cap without the daily limit misses 31 days, and the alarm
  export's exceedance energy misses all 92. A back-tester is confirmed at rung 2.
* **What it is blind to.** Pumping (above).
* **Twin pair.** Feeders F-31 (on Ag3) and F-52 (on S3) are identical on every column the alarm export and the queue carry: rooftop
  capacity, customers, peak load and last spring's back-feed. In the 30% spring they back-fed 260 and 540 MWh (2.1×), because F-31 serves
  eleven groundwater pumping accounts. Only conditioning on the allocation band through the register reproduces both.
* **Resemblance points at the decoy.** Last spring's agricultural back-feed has the same daily shape as the pilot substations', which the
  absorption arithmetic fits exactly.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The charter: twelve 5 MW, 20 MWh units leased for March–May, placed one at a time where each adds the most absorbed
  energy over the season, at most three per substation. The queue dictionary: capacity_kw is DC nameplate, and each system's inverter AC
  rating is listed. The planning assumptions: next year's surface-water allocation is 15%.
* **Empirical pins.** Absorption arithmetic, from the pilot log. Pumping by allocation band, from five springs of SCADA joined to the
  register's pumping accounts and the allocation history.
* **Voices.** The planning manager: "The alarms tell you where the back-feed is. Put the batteries there." The customer-programmes lead:
  "In spring, rooftop solar is the whole story."
* **Licensed wrong basis.** The charter records that the commission's staff review siting against the alarm export's last-spring
  exceedances and will see that ranking in the filing.

## 8. Determinism by construction

* **Window.** Spring is March–May and midday is 09:00–16:00 local, as the charter states.
* **Allocation match.** Pumping at each agricultural substation in the 5% and 30% springs agrees within 1 MW in every midday hour, and a
  regression of pumping on allocation also returns full pumping at 15%, so the matched spring, the mean of the two and the fitted line
  all give the same placement.
* **Queue maturity.** Every system approved before the extract reaches permission to operate within 60 days under the interconnection
  standard, and the extract is five months before March. No application is pending.
* **Placement.** The twelfth unit beats the thirteenth by at least 5% under every rung, and a unit's absorption is computed on the hourly
  basis the pilot certifies.
* **Rounding.** The unrounded 6,030 MWh lies inside its 100 MWh bin under the certified arithmetic.

## 9. Prompt sketch and deliverables

> We have twelve leased battery units for next spring's midday oversupply, and I file the siting plan with the commission on 15
> November. Our planning manager is sure the batteries belong where the reverse-power alarms fired last spring. Tell me how many units go
> to each of our eight substations and how much back-feed we will still have to curtail over the spring, to the nearest 100 MWh. Send
> `battery_siting.xlsx`, a chart `spring_backfeed_forward.png`, and a one-page `siting_filing_note.pdf`.

* `battery_siting.xlsx` — the placement build, the protection sheet (ask A) and the reliability sheet (ask B).
* `spring_backfeed_forward.png` — each substation's forward spring back-feed under rung 2 and under the answer as paired bars, the units
  placed as markers, the agricultural substations' dry-year pumping shaded, and the curtailment left as a labelled line.
* `siting_filing_note.pdf` — the committed placement, the curtailment left, and the bases the commission's staff will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each substation, the number of reverse-power relay operations last spring and the mean
  minutes per operation. *Device:* the protection log records an operation and its reset as two events, and a reclosing sequence logs up
  to three operations within 60 seconds, which the protection manual counts as one. Counting raw events triples the count at three
  substations and halves the mean duration.
* **Ask B (device-carried).** For each substation, last year's customer-minutes of interruption and the number of sustained
  interruptions, with and without major event days. *Device:* the reliability manual excludes major event days by the 2.5-beta threshold
  it states, computed on the daily log of the past five years. Treating the January storm as ordinary inflates four substations' figures
  by more than half.
* **Ask C (validity).** The placement and curtailment left under each of the four rung constructions, and each construction's fit to the
  92 pilot days.
* **Decoupling.** Setting the pumping adjustment to zero changes no figure in asks A or B.

## 11. Rubric arithmetic

8 substations × 2 (ask A) + 8 substations × 2 (ask B) + 4 constructions × 2 (ask C) + the eight committed unit counts and the
curtailment left + 5 named chart parts + 3 files ≈ 57 criteria.

## 12. World-building constraints

* Spring back-feed (MWh), last spring → next spring under the answer: Ag1 5,500 → 400; Ag2 4,000 → 450; Ag3 3,400 → 1,600; S1 3,200 →
  5,400; S2 3,900 → 6,700; S3 3,000 → 4,000; S4 1,900 → 3,700; S5 1,400 → 2,700. DC/AC is 1.25 everywhere except S4 (1.15) and S5 (1.70,
  commercial roofs).
* Placements and curtailment per rung as in the ladder; the answer absorbs 18,920 of 24,950 MWh.
* Water allocations: 5%, 30%, 100%, 75%, 100% in the five closed springs; 15% next year. Pumping is 9–14 MW per agricultural substation in
  the two dry springs and near zero in the others.
* Neither pilot substation serves a pumping account. F-31 and F-52 are identical on every alarm-export and queue column.
* Relay events and major event days never touch SCADA flows, the queue or the pumping accounts.
