# OS16 — Which workforce intervention a $2M fund should buy, when the best-measured one runs into seats that are already taken

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · workforce development programmes |
| Mirrors | Funding the growth lever whose measured lift cannot be delivered because downstream capacity binds (marketing spend into a sold-out onboarding queue, acquisition campaigns into a support team at capacity, demand generation for a hardware line whose supplier slots are full) |
| Decision shape | Which of N gets one scarce thing, with the sizing kept as the graded figure |
| Committed call | The one intervention funded for next programme year, and the additional participants employed in the second quarter after exit that it buys |
| Gap · Pattern | Gap 3 (objective) into Gap 2 (population) · Pattern C (serviceable share behind a join), with S5 (a per-provider minimum that does not commute) |
| Gate G mechanism | binding_constraint, with decomposition_attribution |
| Measured traps engaged | #10 notes a binding limit as a risk · #13 validates on one population, applies to another · #20 leaves the deciding comparison unstated |
| Calibration form | Pilot log: four randomised pilots from last programme year, with outcomes |
| Driving force | Outreach's randomised lift is real and the largest per dollar. Its enrolees can only be served where a training provider has a free seat. Free seats are a per-provider stock computed from continuing enrolment, nowhere stated, and full where outreach recruits. |

## 1. Situation

A state workforce board has $2M for one intervention next programme year: outreach to raise enrolment, credential-exam vouchers, job-placement
coaching, or childcare stipends during training. Last year the board's evaluation office ran a randomised pilot of each, and each pilot's
lift is on file. Staff favour vouchers, because the published credential indicator looks weakest. The board scores interventions on
additional participants employed in the second quarter after exit.

## 2. Gate G: why this is legal

* **Litmus.** Every reported figure is correct: the published indicators, the pilots' lifts, the provider seat register and the enrolment
  records. Nothing is overturned. The difficulty is that one intervention's lift can only be realised through seats that the forward year
  has already filled.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete staff's preference and the published indicators. The pilots still rank outreach first per dollar, and the seat
  arithmetic still reverses it.
* **Instrument repair.** No file is suspect: the seat register, the participant records and the pilot files are complete and current. Make every
  pilot larger and every outcome perfectly measured and rung 2 still names outreach. Seat binding is a forward stock condition that
  still has to be computed per provider.
* **Lens swap.** The pilot counties' spare seats in a closed year and next year's provider stock are different populations at different
  moments.

## 3. The driving force

A strong solver distrusts the published indicators, uses the randomised pilots and ranks per dollar. That makes outreach the clear winner, and
the pilot is genuinely randomised and genuinely right. But every extra enrolee needs a seat at an eligible training provider. The seat
register files each provider's capacity, and free seats are what remains after continuing participants, whose enrolment carries over from
this year. Outreach recruits through community partners clustered in five counties whose providers are near full. The realised lift is a sum
of per-provider minimums of extra enrolees and free seats. That sum is far below the pilot's lift scaled by spend, and nobody states it.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Gap between each stage's published indicator and target, × reach | A, vouchers | The board's own indicators, and staff's reading | The indicators use different denominators and exit cohorts; conditioned on reaching each stage, the voucher gap shrinks |
| 1 | Conditional stage rates, × cost per participant from the vendor contracts | B, coaching | The textbook funnel correction, per dollar | The randomised pilots measure causal lift directly, and coaching's pilot lift is a third of its conditional-rate estimate |
| 2 | Randomised pilot lifts, × participants the $2M reaches at contract cost | D, outreach (1.6× the runner-up) | Causal evidence, cleanly randomised and correctly costed | The seat register and continuing enrolment leave too few free seats where outreach recruits |
| 3 | **Decisive:** each intervention's lift, realised through per-provider free seats in the forward year: the sum over providers of the smaller of extra enrolees and free seats, × conversion | **E, childcare stipends** (4th of 4 on rung 0) | — | — |

* **Position table.** Childcare ranks 4th on rung 0, 3rd on rung 1 and 2nd on rung 2 (1.6× behind outreach), and leads only rung 3.
* **Discriminator dominance.** Outreach carries a 1.6× per-dollar advantage into rung 3. Its seat-realised share is 0.31 against
  childcare's 1.00, an edge of 3.2×, more than 1.2 × 1.6.
* **Partial correction priced (L3).** A solver who applies seat binding at county level (all free seats in a county against all extra
  enrolees) still names outreach. Free seats in unrelated programmes absorb the county totals, so outreach's realised share reads 0.83, not
  0.31.
* **Grid.** Indicators or conditional rates × pilot lifts (on/off) × seat binding (none, county, provider-programme) gives 8 feasible cells.
  Every cell without provider-programme binding names A, B or D.
* **The deciding comparison (#20).** Realised outreach employed (≈ 210) against childcare employed (≈ 340) is what the memo has to state.
  Pilot lifts alone never compute it.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The seat register lists capacities. No document says an outreach enrolee needs a free seat or that seats bind.
2. **Corpus blind for a computable reason.** *In both outreach pilot counties every provider had at least 300 free seats, because the pilot
   was sited where the state had just funded new provider capacity.* The pilot reproduces its lift uncapped.
3. **No arithmetic symptom.** Enrolment, seats and pilot counts reconcile on every rung.
4. **Not a row predicate.** Free seats per provider are capacity minus a carried-over stock (continuing participants whose planned end
   dates fall after the year starts). They are matched to outreach's recruiting partners by county and programme, then a per-provider
   minimum is taken.
5. **The enumeration is arithmetic.** No column says "free seats".
6. **No cutover date.** No series steps; the binding is a forward stock condition.
7. **Survives deletion.** Removing every voice changes nothing.

## 6. The calibration corpus

* **Form.** Four randomised pilots (outreach, vouchers, coaching, childcare), each with its assignment, cost and second-quarter employment
  outcomes.
* **What it certifies.** Each intervention's causal lift (rung 2), so a solver who back-tests is confirmed at rung 2.
* **What it is blind to.** Seat binding (above).
* **Twin pair.** Providers Halden Technical and Marrow Valley Skills are identical on programme mix, seat capacity and last year's completers.
  Halden carries 410 continuing participants and Marrow 40, so the same outreach push realises 2.4× more enrolees at Marrow.
* **Resemblance points at the decoy.** The forward recruiting counties resemble the pilot counties on every demographic column.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The board's charter scores interventions on additional participants employed in the second quarter after exit, in the
  programme year funded. The seat register is the provider list's official capacity, at authority level 2.
* **Empirical pins.** The lifts come from the pilots, and continuing enrolment from planned end dates in the participant records.
* **Voices.** Staff lead: "The credential indicator is our weakest number; vouchers fix it directly." The evaluation office: "Our pilots are
  randomised. Use the lifts and you can't go wrong" (true, for the pilot years).
* **Licensed wrong basis.** The charter records that the governor's office will present the published-indicator ranking at the board meeting.

## 8. Determinism by construction

* **Continuing participants.** Planned end dates fall well clear of the year boundary (none within 30 days), so whether to count "planned
  end" or "expected end" makes no difference.
* **Recruiting geography.** Outreach partners map to counties one-to-one, and each county's eligible providers are listed in the register.
  Assignment by county or by partner gives the same seats.
* **Conversion.** Employed-per-enrolee conversion is pinned by the outreach pilot itself. Childcare's lift needs no seats (it acts on
  enrolled trainees), so no conversion fork touches it.
* **Integer seats.** The world is built so floor and rounding of seats give the same totals.

## 9. Prompt sketch and deliverables

> I have $2M for one intervention next programme year, and staff want vouchers because our credential number looks worst. Tell me which one
> we fund and how many additional people it gets into work by the second quarter after exit. Send `intervention_case.xlsx`, a chart
> `realised_lift.png`, and a one-page `funding_memo.pdf` I can take to the board.

* `intervention_case.xlsx` — the sizing for all four interventions, the provider sheet (ask A) and the cost reconciliation (ask B).
* `realised_lift.png` — pilot lift against seat-realised lift per intervention, per $100k, with the funded choice marked and outreach's
  capped share annotated.
* `funding_memo.pdf` — the committed intervention, its employed figure, and the deciding comparison.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 18 eligible providers, last programme year's completion rate and median days to
  credential, worst first. *Device:* provider IDs changed when four providers merged mid-year, and the crosswalk is in the provider register.
  A solver without it splits four providers' records and misstates their rates.
* **Ask B (device-carried).** Each intervention's cost per participant reached, from the vendor invoices. *Device:* one vendor bills
  coaching in session blocks of four hours, as its contract schedule documents. Reading invoice lines as sessions overstates coaching's
  cost by a factor of four.
* **Ask C (validity).** Realised employed per $100k for each intervention under each of the four rung bases.
* **Decoupling.** Clearing seat binding changes no figure in asks A or B.

## 11. Rubric arithmetic

18 providers × 2 (ask A) + 4 costs (ask B) + 4 interventions × 4 bases (ask C) + the committed choice, its employed figure and the deciding
comparison + 5 named chart parts + 3 files ≈ 65 criteria.

## 12. World-building constraints

* Outreach's pilot lift is the largest per dollar (1.6× the runner-up). Its forward recruiting counties' providers hold 31% of the needed
  free seats. Childcare's lift needs no seats.
* Rung leaders are A, B, D, E, with margins of at least 1.25× at each rung.
* Halden and Marrow are identical on every provider-level column except continuing enrolment.
* Every pilot county had at least 300 free seats. Every planned end date is at least 30 days from the year boundary.
* Provider merges and invoice blocks never touch seat capacity or pilot outcomes.
