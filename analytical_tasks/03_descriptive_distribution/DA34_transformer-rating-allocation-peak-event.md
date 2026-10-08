# DA34 — How a distribution transformer's 300 kVA rating is split across customer groups, when the peak that loads it is an event, not a half-hour

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · utility network capacity allocation |
| Mirrors | Splitting a shared asset's capacity across tenant groups at the peak that actually loads it (cloud region capacity across tenants, CDN egress commitments, warehouse dock capacity), where the sustained window, not the busiest minute, sets the limit |
| Decision shape | An allocation under a cap: the 300 kVA rating divided across three customer groups as their connection allowances |
| Committed call | Each group's allowance in kVA to one decimal, summing to 300.0 |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · S1 (the unit the decision funds is not the unit the pack records), with a flag-suggested population corrected at rung 1 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #2 counts file rows instead of the real unit · #5 takes the population a flag suggests · #4 never tests its reading against the control |
| Calibration form | Prior-period close-out: last summer's substation close-out, publishing the maximum-demand event loading of each of its 12 transformers |
| Driving force | The planning standard allocates the rating by contribution to the transformer's maximum-demand event, the sustained loading its thermal rating is assessed on. No file stores that event; it is the run of consecutive half-hours at or above 95% of the annual maximum, and only that construction returns the close-out's 12 published loadings. Solar homes' net load climbs through the event as generation fades, so their share of the event is far below their share of its last half-hour. |

## 1. Situation

A distribution network operator is offering connection allowances to a new estate served by one 300 kVA transformer, and must split the
rating across three customer groups: homes with neither solar nor controlled load, homes with controlled load, and homes with at least
3 kWp of solar. Allowances are set from half-hourly data for comparable homes, scaled to the estate. The pack holds the half-hourly net
load of 300 comparable homes, the customer register, the generation-meter register, the planning standard and memo, and last summer's
substation close-out.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each home's half-hourly load, each register entry and each published loading. Nobody files an
  allocation and nothing reported is overturned. The difficulty is which stretch of time the peak is.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the consultant's basis and both voices. The coincident half-hour, built from the data, still gives the solar
  group 117.0 kVA.
* **Instrument repair.** Suspect: the customer register's solar flag, stale for 16 homes. Repaired from the generation-meter register,
  rung 0 returns rung 1's 118.0 / 78.0 / 104.0 and rung 2 stays 123.0 / 60.0 / 117.0. The half-hourly loads are complete, and the
  maximum-demand event is a unit no row claims to record, so the answer stays 136.0 / 70.0 / 94.0 and still needs the event built from
  runs of half-hours.
* **Lens swap.** The half-hour reading weights one moment; the answer weights seven half-hours across which solar homes change from
  near-zero to full import. Different moments, different contributions.

## 3. The driving force

A strong solver discards the sum of individual peaks, takes each group's load in the half-hour of the estate's annual maximum (18:30 on the
hottest day), and splits the rating in proportion. That half-hour comes after sunset, when solar homes import fully for air conditioning,
and it gives them 117.0 kVA. The standard allocates on the maximum-demand event, though, and the close-out shows what that is. Its 12
published loadings are each transformer's average over the consecutive half-hours at or above 95% of its annual maximum, here 15:30 to
19:00. Through that run, solar homes start near 40 kVA behind their panels and only reach full import in the last half-hour. Averaged over
the event, they carry 94.0 kVA, and the homes without solar carry 136.0.

## 4. The ladder

| Rung | Construction | Allocates (A / B / C, kVA) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Sum of each group's individual annual peaks, groups from the register's solar flag | 112.0 / 78.0 / 110.0 | Conservative, and every home's peak is in the data | The planning memo: solar homes are those with generation commissioned before the reference summer |
| 1 | The same sum, solar group rebuilt from the generation-meter register (12 flagged homes have no commissioned generation; 4 unflagged homes do) | 118.0 / 78.0 / 104.0 | The population now matches the memo's definition | The close-out: diversified loadings run 25% below summed peaks |
| 2 | Each group's load in the estate's maximum half-hour (coincident peak) | 123.0 / 60.0 / 117.0 | The textbook coincident-peak allocation | The close-out: single maximum half-hours reproduce none of the 12 published loadings |
| 3 | **Decisive:** each group's average over the maximum-demand event (consecutive half-hours at or above 95% of the annual maximum) | **136.0 / 70.0 / 94.0** | — | — |

* **Figure shape.** The solar allowance is the graded component and the answer is its minimum cell. Rungs put it 17.0%, 10.6% and 24.5% above
  94.0, and no rung lands on the answer's vector.
* **Partial correction priced (L3).** A solver who builds an event but at 90% of the maximum (14:30 to 19:30) catches more generation and
  lands the solar group at 84.0 (−10.6%). Its event loadings reproduce 3 of 12 close-out figures.
* **Grid.** Peak construction (summed peaks, maximum half-hour, three-hour rolling maximum, 95% event) × membership (flag or register) = 8
  cells. The nearest wrong cell is the 95% event on flag membership, solar at 103.0 (+9.6%), where 12 flagged homes with no generation
  carry full load through the event.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard defines the event as "the period of sustained loading from which the thermal rating is assessed". No
   document states the 95% threshold or the consecutive-run rule.
2. **Pattern B, pinned by a published figure on the true unit.** The 95% consecutive-run average reproduces 12 of 12 published loadings
   within 0.2 kVA. The single maximum half-hour reproduces 0, a three-hour rolling maximum 7, and the top ten half-hours 5, all reading
   high. The event is a construction: a threshold recovered from the close-out, then a run of half-hours per transformer.
3. **No arithmetic symptom.** Group loads sum to the estate's load in every half-hour, and allocations sum to 300.0 under every rung.
4. **Not a row predicate.** It needs the annual maximum, a run of consecutive qualifying half-hours around it, and an average per group
   over that run.
5. **The enumeration is arithmetic.** No column marks a half-hour as part of the event.
6. **No cutover date.** The event is one afternoon, and nothing steps across days.
7. **Survives deletion.** With every voice removed, the coincident half-hour still allocates the solar group 117.0.

## 6. The calibration corpus

* **Form.** Last summer's close-out for the substation: the published maximum-demand event loading of each of its 12 transformers, with
  their half-hourly loads.
* **What it certifies.** That loadings are diversified, which kills summed peaks.
* **What pins the unit.** The 95% consecutive-run average (above), unique among the constructions a solver would try.
* **Twin pair.** Homes H-1142 and H-2207 share group, tariff, annual energy, individual peak (9.8 kW) and load in the maximum half-hour
  (5.2 kW). Their event averages are 4.8 kW and 2.4 kW (2.0×): one runs air conditioning all afternoon and the other only after 18:00.
* **Resemblance points at the decoy.** The estate's comparable homes resemble the transformer whose rolling three-hour maximum happens to
  match its published loading.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The planning standard: the rating is allocated in proportion to each group's contribution to the transformer's
  maximum-demand event. The planning memo: the three groups, with solar homes defined by generation commissioned before the reference
  summer, the estate scale factors and a 0.95 power factor.
* **Empirical pins.** The event construction, from the close-out.
* **Voices.** The planning engineer: "Sizing to each home's own peak is conservative, and conservative is how distribution gets built."
  The control-room lead: "The busiest half-hour is what trips the fuse; allocate on that."
* **Licensed wrong basis.** The standard records that the developer's consultant allocates on the sum of each group's individual peaks
  and will present it at the connection-offer meeting.

## 8. Determinism by construction

* **Threshold.** No half-hour on the peak day lies within 0.5% of the 95% line, so inclusive and exclusive conventions agree.
* **Run.** The qualifying half-hours form one unbroken run on the peak day; no other day reaches 95%.
* **Rounding.** Allocations round to 0.1 kVA by largest remainder and sum to 300.0.
* **Scaling.** The memo's scale factors map comparable homes to estate counts, the same under every rung.

## 9. Prompt sketch and deliverables

> We are issuing connection allowances on the new estate's 300 kVA transformer, and the planning engineer wants each group sized to its
> own peaks. Give me each group's allowance in kVA to one decimal, summing to 300.0, as the table for the offer letter. Send
> `allowance_build.xlsx`, a chart `peak_event.png`, and a one-page `allowance_note.pdf`.

* `allowance_build.xlsx` — the allocation build, the consumption sheet (ask A), the reliability sheet (ask B) and the construction table
  (ask C).
* `peak_event.png` — the estate's net load on the peak day as stacked group areas by half-hour, with the 95% line, the event shaded, the
  maximum half-hour marked, and each construction's solar allowance in the margin.
* `allowance_note.pdf` — the committed allowances and why each rival construction fails the close-out.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each group, the median monthly consumption per home in each of the 12 months. *Device:* the
  meter-exchange log records register resets when meters were replaced; summing raw register deltas double counts or drops a month for
  23 homes. No exchange falls on the peak day.
* **Ask B (device-carried).** For each of the 12 close-out transformers, customer interruption minutes last year. *Device:* the
  reliability standard excludes interruptions under three minutes, which the outage log records with their own type code; counting them
  overstates four transformers.
* **Ask C (validity).** The allocation under each of the four rung constructions, and each peak construction's reproduction count against
  the close-out.
* **Decoupling.** Clearing the event construction changes no figure in asks A or B.

## 11. Rubric arithmetic

3 groups × 12 months (ask A) + 12 transformers (ask B) + 4 allocations × 3 groups and 4 reproduction counts (ask C) + the three committed
allowances and the event loading + 5 named chart parts + 3 files ≈ 76 criteria.

## 12. World-building constraints

* Allocations (A / B / C): 112.0 / 78.0 / 110.0; 118.0 / 78.0 / 104.0; 123.0 / 60.0 / 117.0; 136.0 / 70.0 / 94.0. Flag-membership event
  cell gives the solar group 103.0; the 90% event gives 84.0.
* The event runs 15:30 to 19:00; the solar group's net load climbs from about 40 to 122 kVA across it.
* Close-out: 95% event 12 of 12, rolling three-hour 7, top ten half-hours 5, maximum half-hour 0. H-1142 and H-2207 match on every
  register and maximum-half-hour column.
* Meter exchanges and short interruptions never touch the peak day or the event.
