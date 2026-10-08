# DA49 — Which utility a reliability commission reviews this year, when the outage feed counts premises that can no longer take supply

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · utility regulation |
| Mirrors | Availability reporting that sets major incidents aside while the monitor keeps counting endpoints that can no longer be served (cloud SLA reports probing deleted resources, telecom availability counting lines whose premises are gone, uptime monitors still polling retired hosts), as cloud and network operators meet |
| Decision shape | Which of N gets one scarce thing: the commission's one full reliability performance review this year, among eight distribution utilities |
| Committed call | The utility reviewed, and its normal-operations SAIDI as a multiple of its benchmark, to two decimals |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · S2 (a residual population between correct records), with the major-event grain set by the unit of work at rung 1 (Pattern D) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection support |
| Measured traps engaged | #7 uses the ready-made measure · #14 coarsens the segment it was asked about · #25 assumes an effect the log could measure |
| Calibration form | Change-log natural experiments: the meter change log's 11 removal batches after past fires and floods, each with the feed, the section states and the open faults on both sides of the removal day |
| Driving force | The outage feed counts every meter reporting no supply. After a fire or a flood, meters at premises destroyed or disconnected for safety keep reporting no supply for months, on sections that are live again and with no fault open. They are not interrupted customers, and nothing says so until the meters are removed. Each one adds 1,440 minutes a day to normal operations. Recovered as the feed's count less customers on dead sections and open faults, they are half the normal-operations SAIDI of the utility that leads every careful reading, and the review goes elsewhere. |

## 1. Situation

A regional utility commission oversees eight electricity distribution utilities and has staff for one full reliability performance review
a year. Its rules send the review to the utility whose normal-operations SAIDI stands furthest above its benchmark. Major event days are
set aside by the 2.5β method, fitted on the five prior years, and SAIDI is measured on the outage feed. The pack holds six years of the
feed (meters without supply by county, every 15 minutes), the network records of section states and single-customer fault tickets, each
utility's operating manual, the commission's determinations file, the meter change log, the benchmarks, and the vegetation and
complaints extracts.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each feed snapshot, section state, fault ticket, determination and meter removal. Nobody ranks the
  utilities on the review's basis, and the consumer advocate's ranking on total SAIDI answers a different question. The difficulty is
  which meters without supply are interrupted customers.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the advocate's ranking and both voices. Feed-based normal SAIDI, with major events identified by operating
  area and their tails accrued to them, still reviews Coldharbour.
* **Instrument repair.** Make every meter, section record and ticket perfect: a meter at a destroyed home correctly reports no supply,
  and a perfect feed still counts it. Telling it from an interruption takes the other two records.
* **Lens swap.** The naive figure takes every meter without supply on a normal day as an interrupted customer. The answer takes only
  those on a dead section or with an open fault, a different population of customers.

## 3. The driving force

A strong solver computes daily SAIDI from the feed and fits each threshold on the five prior years. The mountain utility's local storms
vanish into its system average, and the operating manuals say each area is dispatched as its own system, so the solver identifies major
events by area. The determinations file shows past exclusions taking their tails with them, so it accrues each event's customers still
out after midnight to the event, using the section records. Coldharbour now leads and every figure ties. But the feed counts meters.
After Coldharbour's July fire, 190 meters at destroyed homes kept reporting no supply until year-end, on sections live again within days
and with no fault open. The meter change log shows what such meters are: on every past removal day the feed fell by exactly the meters
removed, and no section or fault changed. Netted out as the feed's count less customers on dead sections and open faults, they take
Coldharbour from 1.52 to 0.80. Eskdale, whose island sections take weeks to repair, stands furthest above its benchmark at 1.26.

## 4. The ladder

| Rung | Construction | Reviews | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Feed-based normal SAIDI, major event days by 2.5β on each utility's system daily SAIDI | A, Alderbank (1.98, 1.21× Brisford) | The standard's method applied to each utility's daily figure | The operating manuals: each operating area is dispatched and restored as its own system, and Alderbank's mountain area has seven storm days its system average hides |
| 1 | Major event days identified on each operating area's daily SAIDI (Pattern D, the area grain) | B, Brisford (1.82, 1.17× Coldharbour) | Each area's storms judged on the system its crews work | The determinations file: every past excluded event took its customers still out after midnight with it until they were restored |
| 2 | Area major events, each event's tail (customers on sections it killed, still dead after midnight) accrued to it | C, Coldharbour (1.52, 1.21× Eskdale) | Events carry their tails as past determinations did, and every remaining minute is a meter without supply | The meter change log: on each of 11 removal days the feed fell by exactly the meters removed, with no section re-energised and no fault closed |
| 3 | **Decisive:** the same, counting only meters on a dead section or with an open fault (the feed's count less both, at every snapshot) | **E, Eskdale (1.26, 1.19× Brisford)** (5th of 8 on rung 0) | — | — |

* **Position table.** Eskdale ranks 5th on rung 0 (1.20), 3rd on rung 1 (1.30) and 2nd on rung 2 (1.26, 1.21× behind Coldharbour, its
  only second place), and leads only rung 3.
* **Discriminator dominance.** Coldharbour carries 1.206× into rung 3 (1.52 against 1.26). Netting out the meters that cannot take
  supply keeps 0.526 of Coldharbour's figure and all of Eskdale's, an edge of 1.90×, against the 1.2 × 1.206 = 1.45 needed (1.31×
  headroom). The product, 1.90 / 1.206 = 1.58, is Eskdale's lead over Coldharbour on rung 3 (1.26 against 0.80); Brisford is runner-up
  at 1.06.
* **Partial correction priced (L3).** A solver who drops meters out more than 14 days in a row removes most of Coldharbour's premises but
  also Eskdale's genuine multi-week outages on its island sections, and reviews Brisford at 1.10× Eskdale (1.06 against 0.96). One who
  clears meters only for 30 days after each major event leaves most of the fire's premises in and reviews Coldharbour at 1.10× Eskdale
  (1.38). One who nets out dead sections but not open faults strips Eskdale's service-drop faults and reviews Brisford at 1.10× Eskdale
  (1.01 against 0.92). No half lands on Eskdale.
* **Grid.** Event grain (system or area) × tails (calendar day or accrued) × meters without supply (all counted, cleared 30 days after
  events, 14-day cap, dead sections only, dead sections and open faults) = 20 cells. Nineteen review Alderbank, Brisford or Coldharbour.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rules define normal operations by major event days and measure on the feed. The feed's guide says a meter
   counts as out when it reports no supply. No document says a premises that cannot take supply is not interrupted, or how to find one.
2. **Pattern B, a residual the change log pins.** On all 11 logged removal days the feed's count fell by exactly the meters removed
   (2,960 of 2,960), while no section was re-energised and no fault closed. Before each removal, those meters were the exact residual in
   their counties at every snapshot since their event closed. A reading that treats them as long interruptions predicts restorations that
   never appear. The residual is a construction across three records at every snapshot, not a filter.
3. **No arithmetic symptom.** Every closed ticket and re-energised section ties to a fall in the feed, every event report closes, and the
   feed never exceeds the meters tracked. The premises sit inside each county's ordinary count.
4. **Not a row predicate.** The feed holds counts by county and snapshot, not meters. The residual is that count less the customers on
   dead sections and the open faults at the same snapshot, so no row carries it.
5. **The enumeration is arithmetic.** No column marks a premises as unable to take supply.
6. **No cutover date.** In the assessment year no affected meter has been removed; the residual sits under ordinary counts from each
   event's close to year-end, with nothing stepping.
7. **Survives deletion.** With every voice removed, the tail-accrued area figure still reviews Coldharbour.

## 6. The calibration corpus

* **Form.** The meter change log: 11 removal batches over five years after past fires and floods, 2,960 meters, each batch with the
  feed, the section states and the open faults in its counties on both sides of the removal day.
* **What it certifies.** That the feed is exact: on every removal day it falls by exactly the meters removed.
* **What it pins.** That those meters were never interrupted: they left the count with no section re-energised and no fault closed, and
  until then they were the residual every day since their event closed.
* **Twin pair.** Two operating-area-years in the log match on meters (96,000), feed-based normal SAIDI (212 minutes), major event days
  (4) and tail minutes. Their normal SAIDI on interrupted customers is 212 and 106 (2.0×): 64 premises a fire destroyed sat without
  supply in the second for 110 days.
* **Resemblance points at the decoy.** On every feed column, Coldharbour resembles the utilities the advocate calls the worst served: long
  outages, slow returns to baseline, high counts in rural counties.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The review rules: one review a year, to the utility whose normal-operations SAIDI is the largest multiple of its
  benchmark; normal operations exclude major event days identified by the 2.5β method on the five prior years; SAIDI is measured on the
  outage feed over the commission's filed customers served.
* **Empirical pins.** The event grain, from the operating manuals; tail accrual, from the determinations file; the residual, from the
  meter change log.
* **Voices.** The commission's reliability engineer: "A meter without supply is a customer without supply." The consumer advocate:
  "Whoever's customers sat in the dark longest this year should get the review."
* **Licensed wrong basis.** The rules record that the consumer advocate ranks utilities on total SAIDI, major events included, and will
  present that ranking at the hearing.

## 8. Determinism by construction

* **Thresholds.** No day lies within 10% of its area's threshold under either accrual or with or without the residual, so the set of
  major event days never changes.
* **Records.** Every meter maps to one section; section states are recorded at every snapshot; every genuine single-customer fault has a
  ticket open from the meter's first missed snapshot.
* **Denominator.** Customers served is the commission's filed average for each utility, unchanged by removals.
* **Rounding.** Every multiple is to two decimals, and Eskdale's 1.26 sits mid-bin.

## 9. Prompt sketch and deliverables

> The commission picks the one utility it reviews this year on the 3rd, and our reliability engineer says a meter without supply is a
> customer without supply. Tell me which utility we review and its normal-operations SAIDI as a multiple of its benchmark, to two
> decimals, in the line for the hearing notice. Send `review_choice.xlsx`, a chart `saidi_layers.png`, and a one-page `review_note.pdf`.

* `review_choice.xlsx` — every utility's figure under each rung, the vegetation sheet (ask A), the complaints sheet (ask B) and the
  residual and removal tables (ask C).
* `saidi_layers.png` — each utility's rung-0 figure as a stacked bar split into its four layers (event grain, tails, meters that cannot
  take supply, interrupted customers), with each benchmark as 1.00 and the reviewed utility marked.
* `review_note.pdf` — the committed utility, its multiple, and why the leaders of each careful reading fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each utility, tree-trimming miles completed against plan. *Device:* the vegetation
  contractor's log records a span re-trimmed after a failed quality inspection as a second entry under the same span ID; counting
  entries overstates three utilities.
* **Ask B (device-carried).** For each utility, reliability complaints per 10,000 customers. *Device:* a complaint escalated to the
  commission is re-filed under a commission reference that cites the utility's original; counting both double-counts two utilities.
* **Ask C (validity).** Each utility's multiple under each of the four rungs, and for each of the 11 removal batches the feed's fall
  against the meters removed.
* **Decoupling.** Clearing the residual changes no figure in asks A or B.

## 11. Rubric arithmetic

8 utilities (ask A) + 8 utilities (ask B) + 8 × 4 rung multiples and 11 removal checks (ask C) + the reviewed utility, its multiple and
its margin + 5 named chart parts + 3 files ≈ 70 criteria.

## 12. World-building constraints

* Multiples by rung: Alderbank 1.98 / 1.13 / 1.05 / 1.05; Brisford 1.64 / 1.82 / 1.06 / 1.06; Coldharbour 1.46 / 1.56 / 1.52 / 0.80;
  Dovecote 1.34 / 1.24 / 1.14 / 1.02; Eskdale 1.20 / 1.30 / 1.26 / 1.26; Ferrow 1.10 / 1.06 / 1.00 / 1.00; Glenmore 0.98 / 0.97 / 0.94 /
  0.94; Hartwell 0.90 / 0.90 / 0.88 / 0.88.
* Residuals: Coldharbour's fire, 190 meters for 158 days (0.72 of benchmark); Dovecote's flood, 61 meters disconnected for safety for 60
  days (0.12). Eskdale: island-section outages beyond 14 days worth 0.30 and service-drop faults worth 0.34 of its 1.26.
* Partial cells: Brisford 1.06 against Eskdale 0.96 (cap), Coldharbour 1.38 (30 days), Brisford 1.01 against Eskdale 0.92 (dead
  sections only). The twin area-years match on every feed column.
* Re-trimmed spans and re-filed complaints never touch a meter, a section or a fault.
