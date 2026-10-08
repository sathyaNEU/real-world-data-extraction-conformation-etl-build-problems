# DA13 — How far $36 million of PFAS design grants reaches, when six systems' worst results are their wholesaler's wellfield water

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · public water-infrastructure grant administration |
| Mirrors | Funding remediation where the symptom is measured downstream of a shared upstream source (an upstream API or CDN whose errors surface in many client services at cloud platforms, a component lot whose defect shows up on several assembly lines in hardware supply chains, one ingredient lot contaminating several products in food supply chains) |
| Decision shape | An allocation under a cap: grants in priority order until $36 million is spent, each at $2.4 million per MGD of source capacity whose own water exceeds 4.0 ng/L, capped at $6 million a system |
| Committed call | The funded systems with each grant in dollars, and the number of systems the fund reaches |
| Gap · Pattern | Gap 4 (rule) over Gap 3 (objective) · E31, a mixture rather than a constant (purchased water blended into six purchasers' entry points by monthly meter fractions), with E21 (a saturated priority score broken by the lowest-consistent rule) below it and a close-out blind to purchases (L1) |
| Gate G mechanism | method_or_model_selection, with binding_constraint |
| Measured traps engaged | #17 guesses an attribution the data can settle · #19 breaks a big tie instead of questioning it · #13 validates on one population, applies to another · #10 notes a binding limit as a risk |
| Calibration form | Prior-period close-out: the 2026 grant cycle's close-out, each funded system's confirmed maximum, eligible capacity and grant |
| Driving force | Six systems buy unblended wellfield water from the Harmon Valley Water Authority through summer interconnects. Their entry-point results therefore mix their own wells with the purchased water, by fractions the monthly purchase meters record. No per-system constant reproduces their records. One assignment does, at reporting precision: the wellfield at 21.0 ng/L for all six, and their own wells clean except one at 5.0. The treatment the grants fund belongs at Harmon Valley's wellfield, which its own blended entry points (9 ng/L) never put near the top of the list. |

## 1. Situation

A state revolving fund has $36 million for PFAS treatment-design grants in 2027. The fund's rule scores each system on its confirmed
maximum PFOA or PFOS as a multiple of 4.0 ng/L, capped at 4, with ties broken by population served, larger first. Grants go down the list
until the money runs out, each at $2.4 million per MGD of the capacity of the system's sources whose own water exceeds 4.0 ng/L, up to $6
million. Thirty systems have scored detections. The pack holds the national monitoring results by entry point and sampling event, the
state's confirmation resamples, each system's source and entry-point inventory with pumping logs, the consecutive-system register with
monthly purchase meter readings, and the 2026 cycle's close-out. The board approves the list on 18 February.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each monitoring result, each confirmation sample, the pumping logs, the purchase meters and the 2026
  close-out. The six purchasers' summer results really are above 16 ng/L, and nobody's reading of their own numbers is overturned. The
  difficulty is whose source the contamination belongs to.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the grants manager's and the purchasers' views and the federal partner's licensed basis. The monitoring
  results still put six purchasers at the score cap, and entry-point attribution still gives each of them its own grant.
* **Instrument repair.** Sample the purchasers' taps perfectly and they read the same, because their water is a blend. A source is known
  only by unmixing entry points with the meter fractions. Even a direct wellfield sample would need the register to say whose interconnect
  carries it.
* **Lens swap.** The two reads fund different systems. Six purchasers (and their own clean wells) against the Harmon Valley wellfield,
  whose own entry points are blended down to 9 ng/L.

## 3. The driving force

A strong solver scores each system on confirmed maxima. It sees that seven systems tie at the cap, applies the fund's lowest-consistent
rule against the confirmation resamples (which breaks most of the tie, as last year's close-out confirms), and sizes each grant on the
sources feeding its exceeding entry point. Each step reconciles. But six of the capped systems are consecutive systems. In June to
September they draw unblended wellfield water from Harmon Valley through interconnects, metered monthly. Their entry-point results swing
from non-detect in winter to 18–21 ng/L in summer, and the swing tracks the purchase fraction exactly. Solved across every sampling event,
the six records admit one assignment at reporting precision: purchased water at 21.0 ng/L in all six, and their own wells at 0.0, except
Cedar Bluff's second well at 5.0. The fund pays for treatment at a source. Five purchasers fall away, Cedar Bluff keeps a small grant, and
Harmon Valley's 12 MGD wellfield takes $6 million. The fund reaches fourteen systems.

## 4. The ladder

| Rung | Construction | Lands on (systems funded) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Monitoring maxima, capped score, population tie-break, grant on the whole system's capacity | 8 (−42.9%) | The fund's score and tie-break applied as written to the national results | The 2026 close-out: its grants reproduce only on the capacity of the sources feeding the exceeding entry point |
| 1 | Same score, grant on the sources feeding the exceeding entry point | 10 (−28.6%) | Grant sizes now match the close-out's formula | The 2026 close-out: its scores reproduce only when each maximum is the lower of the monitoring result and the confirmation resample |
| 2 | Confirmed maxima by the lowest-consistent rule (E21), tie broken by score before population | 11 (−21.4%) | Every 2026 close-out cell reproduces: scores, capacities and grants | The purchase meters: in every purchaser the summer results track the purchased fraction, and only a purchased concentration of 21.0 ng/L reproduces all six records |
| 3 | **Decisive:** purchasers' entry points unmixed by the meter fractions, contamination assigned to the source it comes from, Harmon Valley's wellfield scored and sized | **14** | — | — |

* **Figure shape.** The answer is bracketed. Every rung below funds purchasers' clean wells and reaches 8 to 11 systems. A solver who
  unmixes but never re-attributes the purchased water reaches 17 (+21.4%) by leaving Harmon Valley unfunded. The full list carries Harmon
  Valley at $6.0 million and Cedar Bluff at $2.16 million.
* **Partial correction priced (L3).** The unmixing half-step (purchasers cleared, nothing assigned upstream) lands on the far side of the
  answer, funding three small systems instead of the source that contaminates six.
* **Grid.** Capacity basis (system or entry point) × score (monitoring or lowest consistent) × attribution (entry point or unmixed to
  source) gives 8 cells. Only all three corrections fund 14 systems with Harmon Valley among them. The other cells fund 8 to 12 systems,
  or 17.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rule funds treatment "at each source whose own water exceeds 4.0 ng/L". The register lists interconnects and
   meters for supply planning. No document says a purchaser's results are a blend, or that a supplier's water is anyone's source.
2. **Corpus blind for a computable reason.** *In every 2026 close-out case the system drew only its own water in the months it was
   sampled, because consecutive systems' 2026 sampling events fell in January to March, when nothing was purchased.* The close-out
   certifies rungs 1 and 2 exactly and contains no blend.
3. **No arithmetic symptom.** Results, confirmations, pumping and meter volumes all reconcile, entry-point maxima tie to the national
   release, and grant arithmetic closes to the dollar under every rung.
4. **Not a row predicate.** The source concentrations are the unique solution of each purchaser's results against its monthly purchased
   fraction, one shared value for the wellfield across six systems. No row holds a source's water.
5. **The enumeration is arithmetic.** Seven source concentrations (one wellfield, six sets of own wells) come out of 48 sampling events by
   solving, not by lookup.
6. **No cutover date.** Purchases recur every summer, and the results swing seasonally without a step. Harmon Valley's blend has been
   stable for a decade.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the six purchasers still sit at the score cap.

## 6. The calibration corpus

* **Form.** The 2026 cycle's close-out: each funded system's monitoring maximum, confirmation result, confirmed score, eligible sources
  and capacity, and grant.
* **What it certifies (E21).** The lowest-consistent rule: the 2026 scores reproduce only on the lower of monitoring and confirmation (11
  of 11 systems, against 6 of 11 on monitoring maxima). It also certifies entry-point capacity and the grant formula.
* **What it is blind to.** Blending (above).
* **Twin pair.** Pine Hollow and Cedar Bluff are identical on every monitoring and confirmation column: entry points, results by event
  (summer 19.4 and 20.1, winter non-detect), population and capacity. Pine Hollow runs its own contaminated well in summer, while Cedar
  Bluff buys Harmon Valley water and keeps a well at 5.0 ng/L. Their eligible capacities are 1.8 and 0.9 MGD, and their grants $4.32
  million and $2.16 million (2.0×). Only the pumping log and purchase meter separate them.
* **Resemblance points at the decoy.** The purchasers' results most resemble Pine Hollow's, a system whose summer maximum really is its
  own source.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fund's rule: "A system's priority score is its confirmed maximum PFOA or PFOS as a multiple of 4.0 ng/L, capped
  at 4; ties are broken by population served, larger first; a confirmed maximum is the lowest value consistent with every result on
  file." The rule: "Grants fund treatment at each source whose own water exceeds 4.0 ng/L, at $2.4 million per MGD of that source's
  capacity, up to $6 million a system, in priority order until the fund is spent; a grant is made in full or not at all."
* **Empirical pins.** The lowest-consistent rule's application, from the close-out.
* **Voices.** The grants manager: "The score cap and the population tie-break settle the order. That's why we wrote them." The
  operator association for the six purchasers: "Our members' tap results are the worst in the state, and they should be first in line."
* **Licensed wrong basis.** The rule records that the federal partner ranks systems on monitoring maxima at the entry point and will
  publish its own priority list.

## 8. Determinism by construction

* **Precision.** Results are reported to 0.1 ng/L. Under the unique assignment every purchaser result reproduces within rounding, and the
  next-best constant fails by at least 3 ng/L on some event.
* **Meter months.** Each sampling event falls inside one meter month, and no event straddles a reading.
* **Funding edge.** The money runs out between the 14th and 15th systems with $1.1 million left. The 15th needs $2.9 million, and no
  system further down needs less than $1.2 million, so stopping and skipping to the next system that fits give the same list.
* **Tie-break.** After the lowest-consistent rule, three systems remain at the cap, with populations distinct to the person.

## 9. Prompt sketch and deliverables

> The fund's 2027 PFAS design grants go to the board on 18 February, and $36 million will not reach every system on the list. Our grants
> manager believes the score cap and the population tie-break settle the order. Give me the funded systems with each grant in dollars,
> and how many systems the fund reaches, as the table the board approves, and send `pfas_grants.xlsx` with the build and the sheets
> below, plus `source_attribution.png`.

* `pfas_grants.xlsx` — scores, sources and grants, each of the four rung constructions' funded lists (ask C), the bill sheet (ask A) and
  the service-line sheet (ask B).
* `source_attribution.png` — each purchaser's results by sampling event plotted against its purchased fraction, the single 21.0 ng/L line
  through all six, the funded list as a bar of cumulative dollars against the $36 million line, and Pine Hollow and Cedar Bluff
  annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Monthly residential bill at 5,000 gallons for each of the twelve largest systems in the state.
  *Device:* five of them bill fixed charges every two months while charging usage monthly, as their rate schedules state. Treating the
  fixed charge as monthly overstates those five bills by $9 to $22.
* **Ask B (device-carried).** Lead service lines fully replaced in each of the eight regional offices' areas in 2023, 2024 and 2025.
  *Device:* the inventory records a partial replacement (utility side only) with status "replaced-partial", which the state's guidance
  does not count as a replacement. Counting it overstates 17 of the 24 cells.
* **Ask C (validity).** For Harmon Valley and its six purchasers, the grant under each of the four rung constructions, with the unmixed
  source concentrations.
* **Decoupling.** Rate schedules and the service-line inventory share no row with the monitoring, confirmation or meter data. Clearing
  the unmixing changes no figure in asks A or B.

## 11. Rubric arithmetic

12 systems (ask A) + 8 offices × 3 years (ask B) + 7 systems × 4 constructions and 7 source concentrations (ask C) + the funded count,
Harmon Valley's and Cedar Bluff's grants and the funding edge + 4 named chart parts + 2 files ≈ 82 criteria.

## 12. World-building constraints

* Harmon Valley's wellfield is 21.0 ng/L and 12 MGD. Its entry points blend to about 9 ng/L with surface water. Six purchasers draw 25%
  to 70% of their summer water through metered interconnects and none in winter.
* Systems funded by rung: 8 / 10 / 11 / 14. Unmixing without upstream attribution funds 17. The other grid cells fund 8 to 12.
* The 2026 close-out holds 11 systems, none a purchaser in its sampled months. The lowest-consistent rule reproduces all 11 scores.
* Pine Hollow and Cedar Bluff are identical on every monitoring column, and their source logs differ.
* Rate schedules and the service-line inventory touch no monitoring row.
