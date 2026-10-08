# DA33 — How many hogweed treatments an environment agency commissions for next season, when part of next season's work is in no queue yet

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · environmental programme administration |
| Mirrors | Sizing next period's work when part of it never passes intake (re-opened support tickets suppressed as duplicates, repeat failures of units already repaired, re-uploads of content a platform already took down) |
| Decision shape | One figure committed at a date: the treatment call-off under the regional framework contract, issued on 1 February |
| Committed call | Site treatments commissioned for next season, to the nearest 10 |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · S2 (a residual population between two correct records), with a per-district binding limit at rung 2 (S5) |
| Gate G mechanism | forecasting, with binding_constraint |
| Measured traps engaged | #10 notes a binding limit as a risk · #5 takes the population a flag suggests · #4 never tests its reading against the control |
| Calibration form | Counterparty acknowledgement file: the contractor's acknowledgement of every work order over four seasons, with completion and the infestation stage found at first visit |
| Driving force | A site treated while flowering regrows from its seed bank in the season after, without exception. Those sites are closed in the agency's register, and nobody reports regrowth before it spreads. Next season's regrowth sites therefore sit in neither the report stream nor the open queue. Only the contractor's acknowledgements of last season's flowering first treatments recover them, and they fall in districts where crew capacity is spare. |

## 1. Situation

A regional environment agency controls an invasive hogweed under a framework contract with a treatment contractor. Each February it issues
a call-off fixing next season's site treatments by district. Citizen reports through a recording app have tripled in three years, and the
programme manager wants the call-off sized to them. The pack holds the app's records and checklists, the agency's site register, the
contractor's acknowledgement file, the framework's registered crew capacity by district, the programme plan and the species fact sheet.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each report, each checklist, each register status, each acknowledgement and each capacity line.
  Nobody files a sized call-off and nothing reported is overturned. The difficulty is the work that will exist next season and is in no
  record yet.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the manager's view and the committee's basis. The effort-corrected projection and the district caps still
  give a clean 2,050 with nothing missing from any reconciliation.
* **Instrument repair.** Suspect: the app's report stream, which misses infestations observers do not revisit. Repaired so that every
  infestation is reported in the season it appears, rungs 0 and 1 project 2,370 and rung 2 caps at 2,110: the stream would then carry
  earlier seasons' regrowth, about 60 a season, not last season's 590 flowering first treatments. The register's statuses are correct
  work-order states. The answer stays 2,640, and carrying those treatments into next season is still needed.
* **Lens swap.** The naive figure is sites already reported or projected from reports; the answer adds sites that will exist in the
  coming season from treatments already done, a different population at a different moment.

## 3. The driving force

A strong solver sees that raw reports track app adoption, projects new sites from the share of complete checklists recording the species,
carries forward the open sites, and caps each district at its registered crew capacity, deferring the excess as the plan requires. It
reaches 2,050, and every number ties. But a hogweed stand that flowered before treatment leaves seed that germinates the next summer.
The contractor's acknowledgements show every flowering first treatment in a closed season followed by a regrowth treatment the season
after, 180 of 180, and no vegetative first treatment ever regrowing. The register closes a site once it is treated, and observers do
not revisit fenced sites, so regrowth is reported a season late, after it spreads. Last season's 590 flowering first treatments are next
season's regrowth. They sit in districts where crews have room, and the call-off is 2,640.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Open sites plus new sites projected from the trend in raw reports | 4,860, +84% | The reports are the programme's early warning, and they tripled | The app's participation series: complete checklists rose 3.4× while the share recording hogweed rose 1.2× |
| 1 | New sites projected from the reporting rate per complete checklist, plus open sites | 2,310, −12.5% | Observer growth removed; the textbook effort correction | The framework register: three districts' need exceeds their registered crew capacity |
| 2 | Each district capped at its registered capacity, the excess carried to the following season as the plan requires | 2,050, −22.3% | Feasible, plan-compliant, every district reconciled | The acknowledgement file: every flowering first treatment regrows the season after |
| 3 | **Decisive:** add last season's flowering first treatments as next season's regrowth, then cap by district | **2,640** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the figure down (−52%, then −11%), and the decisive move reverses them (+29%).
* **Partial correction priced (L3).** A solver who adds regrowth for every first treatment last season, flowering or not, lands at 3,330
  (+26%), further away than rung 2. A solver who adds the right regrowth but caps against total capacity instead of each district's lands
  at 2,900 (+9.8%), because the 260 deferred treatments come back.
* **Grid.** Effort (raw or corrected) × cap (none, total, district) × regrowth (none, all first treatments, flowering only) = 18 cells. The
  nearest wrong cell is 2,900 (+9.8%), reachable only with the regrowth found and the district limit misread.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The fact sheet says seed "can persist in soil". The plan schedules follow-ups "when regrowth is reported". No
   document links a flowering stage to a return the season after.
2. **Pattern B, absolute in the counterparty's record.** Regrowth in the following season reproduces 180 of 180 flowering first treatments
   and 0 of 3,490 vegetative ones in closed seasons. Rival intervals (two seasons on, any later season) and rival stages (all first
   treatments) each miss at least 120 cases. It is a residual, not a menu: the contractor's completions joined against the register and
   the report stream, with nothing labelling next season's regrowth.
3. **No arithmetic symptom.** Register counts tie to acknowledgements, reports tie to checklists, and every district reconciles with or
   without the regrowth.
4. **Not a row predicate.** It needs the season and stage of each site's first treatment from another organisation's file, a one-season
   offset recovered from closed cases, and an anti-join against the register and reports.
5. **The enumeration is arithmetic.** No column marks a site as due to regrow.
6. **No cutover date.** Regrowth runs at the same offset every season and steps no series.
7. **Survives deletion.** With every voice removed, the capped projection still stops at 2,050.

## 6. The calibration corpus

* **Form.** The contractor's acknowledgement file: 9,840 work orders over four seasons, each with its acknowledgement status, completion
  date and the stage found at first visit (flowering or vegetative).
* **What it certifies.** The treatment history the register summarises, so the solver uses it to reconcile completions.
* **What it pins.** The regrowth rule (above), absolute and single-valued.
* **Twin pair.** Districts Ashcombe and Brenley match on reports, complete checklists, reporting rate, open sites and capacity. Next
  season they need 520 and 260 treatments (2.0×); Ashcombe's 260 first treatments last season were flowering and Brenley's were
  vegetative.
* **Resemblance points at the decoy.** By report growth and open sites, the regrowth districts look like the quiet districts the
  projection already sizes.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme plan: the call-off commissions every site expected to need treatment next season, within each district's
  registered crew capacity, with demand beyond a district's capacity carried to the following season. The framework register gives each
  district's capacity.
* **Empirical pins.** The regrowth offset and stage, from the acknowledgements.
* **Voices.** The programme manager: "The app reports are our early warning; if it's out there, someone reports it." The finance officer:
  "We pay for what's in the queue, not for guesses."
* **Licensed wrong basis.** The plan records that the regional council's environment committee sizes the programme on raw report counts
  and will review the call-off on that basis.

## 8. Determinism by construction

* **Seasons.** Seasons run April to October, and every first treatment's season is unambiguous.
* **Stage.** The contractor records one stage per first visit, and no site is first-treated twice.
* **Capacity.** Capacities are whole treatments per district, and every regrowth site falls in a district with at least 70 treatments
  to spare.
* **Projection.** The reporting rate per complete checklist is flat to within 0.2 points across three seasons, so mean, last-season and
  trend projections give the same new-site figure.

## 9. Prompt sketch and deliverables

> The call-off goes to the contractor on 1 February, and the programme manager wants it sized to the app reports, which have tripled.
> Tell me how many site treatments we commission for next season, to the nearest 10, in one sentence for the call-off letter. Send
> `call_off_build.xlsx`, a chart `treatment_need.png`, and a one-page `call_off_note.pdf`.

* `call_off_build.xlsx` — the need build by district, the observer sheet (ask A), the response-time sheet (ask B) and the rung table
  (ask C).
* `treatment_need.png` — stacked bars by district of open sites, projected new sites and regrowth, against each district's capacity line,
  with deferred treatments hatched and the twin districts labelled.
* `call_off_note.pdf` — the committed figure and the readings a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine districts, distinct active observers in each of the last three seasons.
  *Device:* observers who added a second device appear under two IDs, and the app's account-merge file links them; counting raw IDs
  overstates observers by 11%.
* **Ask B (device-carried).** For each district, the median days from a site's first report to its first completed treatment last season.
  *Device:* re-issued work orders keep the base order number with a suffix, as the contractor's interface specification documents;
  matching on the base number takes the cancelled visit and overstates four districts. Re-issues occur only on vegetative sites.
* **Ask C (validity).** The call-off under each of the four rungs, and each district's need and capacity.
* **Decoupling.** Clearing the regrowth residual changes no figure in asks A or B.

## 11. Rubric arithmetic

9 districts × 3 seasons (ask A) + 9 medians (ask B) + 4 rungs and 9 × 2 district figures (ask C) + the committed figure, the regrowth
count and the deferred count + 5 named chart parts + 3 files ≈ 69 criteria.

## 12. World-building constraints

* Need components: 1,180 open, 1,130 projected new (3,680 on raw trend), 590 regrowth. Three districts defer 260 in total. Total capacity
  3,000.
* Closed seasons: 180 flowering first treatments, all regrowing in the following season; 3,490 vegetative never do. Last season's 590
  flowering first treatments are more than eight times any earlier season's.
* Rung figures 4,860 / 2,310 / 2,050 / 2,640; other cells 3,330 and 2,900. Ashcombe and Brenley match on every report and register
  column.
* With every infestation reported in the season it appears, rungs 0 and 1 project 2,370 and rung 2 caps at 2,110.
* Device merges and order suffixes never touch a flowering first treatment or a capacity line.
