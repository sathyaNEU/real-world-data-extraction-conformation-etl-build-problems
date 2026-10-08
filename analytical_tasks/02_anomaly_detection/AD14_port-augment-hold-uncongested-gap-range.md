# AD14 — Which interconnect gets this quarter's one port augment, when the strongest evening gap is one that uncongested ports have shown before

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Economics · internet interconnection and peering |
| Mirrors | Deciding whether a degradation is specific enough to buy capacity for, when the comparison it rests on varies between slices more than the test statistic admits (peering augments at streaming platforms, experiment readouts on day-clustered metrics at Meta, CDN capacity adds where evening slowdowns are event-driven) |
| Decision shape | Which of N gets one scarce thing, where the answer is a hold forced by a blocking quantity: the quarter's single 100G port augment |
| Committed call | The interconnect augmented this quarter, or that none is, with the quantity that decides it |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · hold forced by a computed blocking quantity (E28): the largest specificity gap against the range uncongested interconnects reach, from the close-out; the segment coarsened at the lower rung (E18) |
| Gate G mechanism | signal_vs_noise_or_hold, with method_or_model_selection |
| Measured traps engaged | #9 picks from the offered options when none passes · #14 coarsens the segment it was asked about · #1 reports a failed back-test, ships anyway |
| Calibration form | Prior-period close-out: the augment programme's close-out for the last two quarters, six funded augments with their gaps and results, and twelve monitored interconnect-quarters with no congestion |
| Driving force | The investment rule funds an augment where the evening slowdown is specific to the interconnect. The specificity gap, the interconnect's evening ratio against the same ISP's other paths in the metro, is significant for C on 9,800 tests. The close-out shows what that is worth: three augments funded on test-significant gaps of 0.14 to 0.19 changed nothing, and uncongested interconnects show gaps up to 0.21 from server placement and path mix. C's 0.17 sits inside that range, every other candidate lower, and no augment is justified this quarter. |

## 1. Situation

A video platform funds one 100G port augment a quarter at an interconnection point with a broadband ISP's network. Seven interconnects
(ISP × transit network × metro) show evening slowdowns in its speed-test panel this quarter. The investment rule says an augment is funded
where the evening slowdown is specific to the interconnect, and that the quarter's augment may be held if none is. The pack carries the
quarter's speed tests (client ISP, server site, transit network, metro, hour, throughput), the peering register listing all 14 interconnects,
the network dashboard's ISP-level evening ratios, and the programme's close-out.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each test, the register, the dashboard's ISP-level ratios and every close-out result. The peering
  manager's ISP really has the worst evening speeds. Nothing reported is overturned; the difficulty is that the strongest interconnect-level
  signal is one that interconnects without congestion produce routinely.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the peering manager's view and the dashboard. The tests still give C a gap of 0.17, significant at any test-level
  threshold, and a careful solver still funds C.
* **Instrument repair.** Double the speed-test panel; the test-level interval only narrows. The gap's comparison with uncongested slices
  does not change, because the 0.21 range comes from path and server differences, not sampling.
* **Lens swap.** The naive test asks whether C's gap differs from zero across tests; the answer asks whether it differs from what
  uncongested interconnect-quarters show, a different population of reference slices, and no candidate does.

## 3. The driving force

A strong solver distrusts the dashboard's ISP-level table, rebuilds evening-to-reference throughput ratios at the interconnect grain the
register lists, notices that B's slow evenings are shared by every path of B's ISP in that metro, and computes each interconnect's gap
against its ISP's other paths. C stands out at 0.17 with a test-level interval of ±0.02, and C is funded. Each step is competent. But tests
are not the unit that varies: two interconnects of the same ISP in the same metro differ by server site, transit path and test-population
mix every quarter, and those differences are not congestion. The close-out has measured them. Twelve monitored interconnect-quarters whose
transit statements showed no congestion produced gaps from −0.07 to 0.21. Three augments funded on gaps of 0.14 to 0.19, each significant on
thousands of tests, changed nothing. The three that worked had gaps of 0.24 to 0.31. C's 0.17 is inside the uncongested range, so the rule's
specificity test fails for every candidate and the quarter's augment is held.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The dashboard's ISP-level evening ratio; augment the worst ISP's busiest interconnect | A (ISP X at 0.74) | The network team's own table, and the ISP everyone complains about | The peering register: the rule's unit is the interconnect, and at that grain every one of ISP X's paths shows the same evening ratio |
| 1 | Evening-to-reference median throughput per interconnect, at least 300 tests per window | B (0.62; its drop 1.31× C's) | The segment the rule names, built from tests, with the sample floor applied | The same tests: B's ISP's other paths in that metro read 0.64, so B's slowdown is the ISP's access network, not the interconnect |
| 2 | Specificity gap against the ISP's other paths in the metro, test-level interval | C (0.17 ± 0.02; 1.55× D) | Specific, large and significant on 9,800 tests | The close-out: three augments funded on test-significant gaps of 0.14–0.19 changed nothing, and uncongested interconnect-quarters reach 0.21 |
| 3 | **Decisive:** every candidate's gap set against the close-out's uncongested range | **Hold: the largest gap, C's 0.17, is below the 0.21 uncongested ceiling** | — | — |

* **Blocking quantity.** C's specificity gap of 0.17 against the 0.21 ceiling of uncongested interconnect-quarters (0.81 of it); the
  effective augments' floor is 0.24. Every other candidate's gap is 0.11 or less.
* **Why each candidate fails.** A: gap 0.01, its ISP's slowdown is access. B: gap 0.06, access again. C: 0.17, inside the uncongested
  range. D: 0.11. E, F and G: 0.05 or less.
* **Partial correction priced (L3).** A solver who reads the close-out's three failed augments as bad luck and funds C anyway has shipped
  on a failed back-test; a solver who raises the bar to the failed augments' highest gap (0.19) still funds nobody, but for the wrong reason,
  and would fund an interconnect at 0.20 that the uncongested range covers.
* **Grid.** Grain (ISP or interconnect) × comparison (absolute ratio or specificity gap) × standard (test-level interval or uncongested
  range) gives eight cells; the ISP cells name A, absolute-ratio cells B, test-level gap cells C. Only the gap against the uncongested range
  holds, and the nearest wrong cell (C) needs the close-out's failed augments set aside.
* **Falsifiable.** The hold becomes a pick if any candidate's gap reaches 0.24, the effective floor: C would need 0.07 more. A transit
  statement showing loss on C's port would also settle it.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The investment rule says "specific to the interconnect" and licenses a hold; it gives no threshold and no reference
   population. The close-out reports results; it never states a standard.
2. **Corpus blind for a computable reason.** *In every close-out row the test-level interval excludes zero, because every funded or
   monitored interconnect ran at least 6,000 tests a quarter,* so test-level significance cannot tell the effective augments from the
   ineffective ones; only the gaps' level against the uncongested rows can.
3. **No arithmetic symptom.** Tests tie to the panel, ratios to medians, and C's interval is genuinely narrow; nothing fails.
4. **Not a row predicate.** It needs interconnect-level medians in two windows, a within-ISP, within-metro comparison, and a range drawn from
   a different file's slices.
5. **The enumeration is arithmetic.** The verdict is a comparison of computed gaps with a computed range; no field marks congestion.
6. **No cutover date.** Every slowdown is steady across the quarter; no series steps.
7. **Survives deletion.** With every voice and the dashboard removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The close-out for the last two quarters: six funded augments, each with its pre-augment specificity gap, its test count, and its
  evening ratio before and after; and twelve monitored interconnect-quarters whose transit statements showed no congestion, with their gaps.
* **What it pins.** Effective augments had gaps of 0.24, 0.27 and 0.31 and recovered 0.16 to 0.22 of evening ratio; ineffective ones had
  0.14, 0.16 and 0.19 and recovered 0.08 or less; uncongested slices span −0.07 to 0.21. Nothing lies between 0.21 and 0.24.
* **Twin pair.** Augments K-1 and K-6 are identical on the interconnect's evening ratio (0.66), test count, the ISP's dashboard ratio, metro
  size and server mix. K-1 recovered 0.18 of evening ratio and K-6 0.08 (2.25×): K-1's gap against its ISP's other paths was 0.27 and
  K-6's 0.14. Nothing at interconnect or ISP level separates them.
* **Every rule exercised.** One uncongested slice sits in the same metro as C, so the within-metro comparison is tested; one effective augment
  had only 6,100 tests, so test volume is not the separator.
* **Resemblance points at the decoy.** C's test profile most resembles the 2025 Q4 augment at 0.27, the programme's best result.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The investment rule: an augment is funded where the evening slowdown is specific to the interconnect, and the quarter's
  augment may be held if none is. Evening is 20:00–23:59 and reference 10:00–13:59 local time, weekdays; an interconnect needs 300 tests in
  each window. The peering register's list of interconnects.
* **Empirical pins.** The uncongested range and the effective floor, from the close-out.
* **Voices.** The peering manager: "ISP X has the worst evenings on the dashboard; that's where the port goes." The analytics lead: "With
  9,800 tests, anything at 0.17 is real."
* **Licensed wrong basis.** The rule records that the ISP's account team argues augments on ISP-level evening ratios and will bring them to
  the capacity review.

## 8. Determinism by construction

* **Windows.** Shifting the reference window to 09:00–12:59 moves every gap by under 0.01.
* **Medians.** Medians and trimmed means give the same order and the same verdict; no candidate's gap reaches 0.20 under either.
* **Range.** The uncongested range is the close-out's twelve slices as listed; dropping any one leaves the ceiling at 0.19 or above, still
  above C.
* **Sample floor.** All seven candidates exceed 300 tests in both windows, so the floor removes none.

## 9. Prompt sketch and deliverables

> We can fund one port augment this quarter at one of the interconnects showing evening slowdowns. Our peering manager is sure the problem
> is at the ISP with the worst evening speeds. Name the interconnect to augment, or tell me that none should be augmented this quarter, in
> one sentence for the capacity plan, with `augment_decision.xlsx` holding the sheets below, the chart `evening_gap.png`, and
> `capacity_plan_note.docx`.

* `augment_decision.xlsx` — the interconnect build, the session sheet (ask A), the complaints sheet (ask B) and the close-out table (ask C).
* `evening_gap.png` — the seven candidates' specificity gaps with their test-level intervals, beside the close-out's uncongested slices and
  six augments on the same axis, the 0.21 ceiling and the 0.24 effective floor drawn as lines, and C labelled.
* `capacity_plan_note.docx` — the committed verdict, the blocking quantity, and what would turn it into an augment.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 interconnects, BGP session resets in the quarter and total minutes down.
  *Device:* a reset on a bundled interconnect is logged once per member link, and the peering register lists each bundle's members. Counting
  log lines multiplies resets at the five bundled interconnects. The speed-test build never reads session logs.
* **Ask B (device-carried).** For each of the six ISPs, evening buffering complaints per 10,000 subscribers in each month of the quarter.
  *Device:* a complaint reopened within seven days keeps its ticket ID and increments a reopen counter, per the support guide. Counting
  ticket rows double-counts reopened complaints at the two ISPs with the slowest fixes.
* **Ask C (validity).** For each of the six closed augments, whether its gap was significant at test level and whether it cleared 0.21, and
  the recovery it delivered (6 × 2).
* **Decoupling.** Clearing the uncongested range changes no figure in asks A or B.

## 11. Rubric arithmetic

14 interconnects × 2 (ask A) + 6 ISPs × 3 months (ask B) + 6 augments × 2 (ask C) + the hold verdict, C's gap against the ceiling and the
gap still needed + 5 named chart parts + 3 files ≈ 69 criteria.

## 12. World-building constraints

* Candidate gaps: A 0.01, B 0.06, C 0.17, D 0.11, E 0.05, F 0.04, G 0.03; C's test-level interval ±0.02 on 9,800 tests.
* B reads 0.62 and its ISP's other paths in the metro 0.64; ISP X's paths all read about 0.74.
* Close-out: effective gaps 0.24, 0.27, 0.31 (recoveries 0.16–0.22); ineffective 0.14, 0.16, 0.19 (0.08, 0.02, 0.01); uncongested −0.07 to
  0.21; nothing between 0.21 and 0.24.
* K-1 and K-6 are identical on every interconnect-level and ISP-level column.
* Bundle member resets and reopened tickets never touch the speed tests or the close-out.
