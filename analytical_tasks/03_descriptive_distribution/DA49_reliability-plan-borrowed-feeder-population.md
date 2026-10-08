# DA49 — Which utility a reliability commission puts on its one performance plan, when storm repairs leave customers on borrowed feeders through the plan year

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · utility regulation |
| Mirrors | Planning next period's service levels when an incident's workaround outlives the incident (traffic shifted to a backup region until a rebuild, users moved to a fallback cluster, orders rerouted to a farther depot), so next period's reliability depends on who is still on the workaround, a population no incident log carries |
| Decision shape | Which of N gets one scarce thing: the commission's one reliability performance plan for the coming year, among eight distribution utilities |
| Committed call | The utility placed on the plan, and its expected normal-operations SAIDI over the plan year as a multiple of its benchmark, to two decimals |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · S2 (a residual population between correct records, projected over the plan year), with the major-event grain set by the unit of work at rung 1 (Pattern D) |
| Gate G mechanism | forecasting, with decomposition_attribution support |
| Measured traps engaged | #25 assumes an effect the log could measure · #14 coarsens the segment it was asked about · #7 uses the ready-made measure |
| Calibration form | Change-log natural experiments: the switching change log's 23 past storm reconfigurations, each with the customers moved onto another feeder, the move and return dates, and those customers' normal-day minutes before, during and after |
| Driving force | After a storm, crews restore customers fast by switching them onto a neighbouring feeder, and they stay there until their own feeder is rebuilt. On the borrowed feeder, long and without a backup tie, they lose about four times their usual normal-day minutes, as all 23 logged reconfigurations show. Nothing records who is still borrowed: the population is the switching log's moves net of returns, read through the connectivity model's normal feeds. Eskdale's December ice storm left a third of its customers borrowed through the whole plan year, and its plan-year figure doubles. |

## 1. Situation

A regional utility commission oversees eight electricity distribution utilities and can run one reliability performance plan a year. Its
rules place the plan with the utility whose normal-operations SAIDI it expects to stand furthest above its benchmark over the plan year,
the coming calendar year. Major event days are set aside by the 2.5β method fitted on the five prior years. The pack holds six years of
the outage feed (customers out by operating area every 15 minutes), each utility's operating manual, the connectivity model of normal
feeds, the switching log, the capital plan with rebuild dates, the change log of past storm reconfigurations, the benchmarks, the
commission's performance archive, and the vegetation and complaints extracts.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each feed snapshot, switching operation, connectivity record and logged reconfiguration. Nobody
  forecasts the plan year, and the consumer advocate's ranking on last year's total SAIDI answers a different question. The difficulty is
  a population that exists only as moves net of returns.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the advocate's ranking and both voices. The three-year mean of normal-operations SAIDI, with major events
  identified by operating area, still places the plan with Coldharbour.
* **Instrument repair.** No file is suspect: the feed, the switching log, the connectivity model and the change log are complete and
  correct, the model recording each customer's normal feed as it claims. Replaced by an as-operated model that lists every borrowed
  customer, no rung moves, since none uses feeders: rung 0 still places the plan with Alderbank, rung 1 with Brisford and rung 2 with
  Coldharbour. The plan year's minutes are a forward quantity no instrument records, so the answer stays Eskdale and the projection is
  still needed.
* **Lens swap.** The naive figure carries past minutes forward. The answer adds the minutes borrowed customers will lose in the plan year,
  a population fixed at year-end and a moment that has not happened.

## 3. The driving force

A strong solver computes normal-operations SAIDI from the feed with the 2.5β thresholds and sees the mountain utility's local storms vanish
into its system average. The operating manuals say crews are dispatched by operating area, so it identifies major events by area. It
knows one year swings with weather and expects the plan year on the three-year mean, which the commission's archive shows predicts the next
year best. Coldharbour leads at 1.25. The change log shows what the mean cannot see. In all 23 past storm reconfigurations, customers
switched onto a neighbouring feeder lost 3.8 to 4.2 times their usual normal-day minutes until their own feeder was rebuilt, then went
back to their usual rate. Nothing lists who is borrowed now. Netting the switching log's moves against its returns, through the
connectivity model, leaves a third of Eskdale's customers on borrowed feeders since its 18 December ice storm, and the capital plan
rebuilds none of those feeders before the plan year ends. Their plan-year minutes take Eskdale to 1.95.

## 4. The ladder

| Rung | Construction | Places the plan with | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Last year's normal-operations SAIDI, major event days by 2.5β on each utility's system daily SAIDI | A, Alderbank (1.84, 1.16× Brisford) | The standard's method on the latest year | The operating manuals: each operating area is dispatched and restored as its own system, and Alderbank's mountain area has seven storm days its system average hides |
| 1 | Major event days identified on each operating area's daily SAIDI (Pattern D, the area grain) | B, Brisford (1.76, 1.35× Dovecote) | Each area's storms judged on the system its crews work | The performance archive: one year's normal SAIDI predicted the next within 15% in 11 of 40 utility-years, the three-year mean in 31 |
| 2 | The plan year expected on the three-year mean, area major events | C, Coldharbour (1.25, 1.16× Dovecote) | Weather averaged out, on the archive's best simple predictor | The change log: in all 23 reconfigurations, customers moved onto another feeder lost 3.8 to 4.2 times their usual minutes until their feeder was rebuilt |
| 3 | **Decisive:** the three-year mean plus the plan-year minutes of customers still on borrowed feeders at year-end (switching moves net of returns, through the connectivity model) at the change log's multiple, until their rebuild | **E, Eskdale (1.95, 1.56× Coldharbour)** (5th of 8 on rung 0) | — | — |

* **Position table.** Eskdale ranks 5th on rung 0 (1.14), 4th on rung 1 (1.16) and 6th on rung 2 (0.98), and leads only rung 3.
* **Discriminator dominance.** Coldharbour carries 1.276× into rung 3 (1.25 against 0.98). The borrowed customers' increment raises
  Eskdale 1.99× and leaves Coldharbour unchanged, an edge of 1.99×, against the 1.2 × 1.276 = 1.53 needed (1.30× headroom). The product,
  1.99 / 1.276 = 1.56, is Eskdale's lead over Coldharbour on rung 3.
* **Partial correction priced (L3).** A solver who applies the multiple to every customer moved during the year, including those moved
  back, adds Dovecote's summer transfers and places the plan with Dovecote at 1.22× Eskdale (2.38). One who measures the multiple from
  Eskdale's own 13 days on borrowed feeders, a calm fortnight at 1.4 times, lands Eskdale at 1.11 and keeps Coldharbour, 1.13× Eskdale.
  One who counts borrowed feeders rather than customers (3 of Eskdale's 50) lands Eskdale at 1.16 and keeps Coldharbour, 1.08× Eskdale.
  No half lands on Eskdale.
* **Grid.** Event grain (system or area) × base (last year or three-year mean) × increment (none, every customer moved, own-fortnight
  multiple, net moves at the change log's multiple) = 16 cells. The four cells with the net-move increment all name Eskdale; the other
  twelve name Alderbank, Brisford, Coldharbour or Dovecote.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rules expect the plan year and set major events aside. The switching log records operations, the connectivity
   model normal feeds and the capital plan rebuild dates. No document says borrowed customers lose more minutes or lists who is borrowed.
2. **Pattern B, a multiple the change log measures.** In all 23 logged reconfigurations, borrowed customers lost 3.8 to 4.2 times their
   usual normal-day minutes until their rebuild and their usual rate after it. The three-year mean predicted the following year within
   10% in none of the 23 affected area-years and in 37 of 40 unaffected ones. The population is a construction: every switching operation
   applied to the model's topology, moves netted against returns customer by customer to year-end.
3. **No arithmetic symptom.** Feed counts tie to customers served, switching operations balance wherever a feeder was rebuilt, and every
   year's normal SAIDI reconciles to the archive.
4. **Not a row predicate.** Whether a customer is borrowed at year-end is the net of every operation on its feeders through the year,
   applied through the topology.
5. **The enumeration is arithmetic.** No column marks a customer or a feeder as borrowed.
6. **No cutover date.** The storm is past and no rebuild falls inside the plan year, so the increment is level across it.
7. **Survives deletion.** With every voice removed, the three-year mean still places the plan with Coldharbour.

## 6. The calibration corpus

* **Form.** The change log: 23 storm reconfigurations over six years across the eight utilities, each with the customers moved, the move
  and return dates, and their normal-day minutes before, during and after.
* **What it certifies.** That a borrowed customer's minutes return to their usual rate once its feeder is rebuilt, which every past year's
  archive figure already reflects.
* **What it pins.** The multiple, 3.8 to 4.2, stable across utilities, seasons and feeder types.
* **Twin pair.** Two operating-area-years in the archive match on customers (96,000), normal SAIDI (118 minutes), major event days (4)
  and feeder count. Their next-year normal SAIDI was 126 and 252 minutes (2.0×): a third of the second area's customers were still on
  borrowed feeders at year-end.
* **Resemblance points at the decoy.** On every archive column, Eskdale's last three years resemble the steady utilities the plan never
  needs.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The plan rules: one plan a year, placed with the utility whose normal-operations SAIDI the commission expects to stand
  furthest above its benchmark over the coming calendar year, as a multiple of benchmark; normal operations exclude major event days
  identified by the 2.5β method on the five prior years. The capital plan's rebuild dates are firm.
* **Empirical pins.** The event grain, from the operating manuals; the base, from the archive; the multiple, from the change log.
* **Voices.** The commission's reliability engineer: "Last year's record is what a utility should answer for." The consumer advocate:
  "Whoever's customers sat in the dark longest this year should get the plan."
* **Licensed wrong basis.** The rules record that the consumer advocate ranks utilities on last year's total SAIDI, major events included,
  and will present that ranking at the hearing.

## 8. Determinism by construction

* **Thresholds.** No day lies within 10% of its area's threshold, so the major event days are the same under every rung.
* **Borrowing.** Every move and return in the switching log transfers a whole feeder section; at year-end 33% of Eskdale's customers are
  borrowed and no other utility's are.
* **Rebuilds.** Every borrowed feeder's rebuild in the capital plan falls after the plan year, so the increment runs the whole year.
* **Rounding.** Multiples are to two decimals, and Eskdale's 1.95 sits mid-bin.

## 9. Prompt sketch and deliverables

> The commission places this year's performance plan on the 9th, and our reliability engineer says last year's record is what a utility
> should answer for. Tell me which utility gets the plan and its expected normal-operations SAIDI over the plan year as a multiple of its
> benchmark, to two decimals, in the line for the hearing notice. Send `plan_choice.xlsx`, a chart `borrowed_feeders.png`, and a one-page
> `plan_note.pdf`.

* `plan_choice.xlsx` — every utility's multiple under each rung, the vegetation sheet (ask A), the complaints sheet (ask B) and the
  borrowed-customer and change-log tables (ask C).
* `borrowed_feeders.png` — each utility's monthly normal-operations SAIDI over three years with the plan year projected, borrowed
  customers shaded from move to rebuild, the change log's multiple annotated, each benchmark drawn, and the planned utility marked.
* `plan_note.pdf` — the committed utility, its multiple, and why the leaders of each careful reading fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each utility, tree-trimming miles completed against plan. *Device:* the vegetation
  contractor's log records a span re-trimmed after a failed quality inspection as a second entry under the same span ID; counting
  entries overstates three utilities.
* **Ask B (device-carried).** For each utility, reliability complaints per 10,000 customers. *Device:* a complaint escalated to the
  commission is re-filed under a commission reference that cites the utility's original; counting both double-counts two utilities.
* **Ask C (validity).** Each utility's multiple under each of the four rungs, customers borrowed at year-end by utility, and the measured
  multiple in each of the 23 logged reconfigurations.
* **Decoupling.** Clearing the borrowed-customer increment changes no figure in asks A or B.

## 11. Rubric arithmetic

8 utilities (ask A) + 8 utilities (ask B) + 8 × 4 rung multiples, 8 borrowed counts and 23 logged multiples (ask C) + the planned
utility, its multiple and its margin + 5 named chart parts + 3 files ≈ 90 criteria.

## 12. World-building constraints

* Multiples by rung: Alderbank 1.84 / 1.12 / 1.05 / 1.05; Brisford 1.58 / 1.76 / 1.07 / 1.07; Coldharbour 1.30 / 1.27 / 1.25 / 1.25;
  Dovecote 1.36 / 1.30 / 1.08 / 1.08; Eskdale 1.14 / 1.16 / 0.98 / 1.95; Ferrow 1.06 / 1.06 / 1.02 / 1.02; Glenmore 0.97 / 0.97 / 0.96 /
  0.96; Hartwell 0.90 / 0.90 / 0.90 / 0.90.
* Eskdale: ice storm on 18 December; 33% of its customers on 3 of its 50 feeders borrowed; multiple 4.0. Dovecote: 40% of customers
  borrowed from July to September and returned in October.
* Partial cells: Dovecote 2.38 (every customer moved), Eskdale 1.11 (own fortnight) and 1.16 (feeder share). The twin area-years match
  on every archive column.
* Re-trimmed spans and re-filed complaints never touch a switching operation, a feeder or a feed count.
