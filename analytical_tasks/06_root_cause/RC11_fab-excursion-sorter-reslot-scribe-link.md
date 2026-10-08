# RC11 — Which tool gets the fab's engineering week, when the wafer sorter quietly reshuffles which history each failing wafer carries

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · semiconductor manufacturing yield |
| Mirrors | Excursion triage on lines where items are re-sequenced between steps (wafer and panel lines at Apple and Google hardware suppliers, fulfilment totes re-sorted between pick and pack at Amazon), so the obvious record key ties each result to a neighbour's history |
| Decision shape | Which of N root causes gets the fix: one week of the yield engineering team on one tool or chamber |
| Committed call | The tool or chamber the engineering week goes to, and the excess failing wafers its wafers account for over the six excursion weeks |
| Gap · Pattern | Gap 2 (population) · E20 (an implicit join: sort results reach process history through the sorter's scribe-id log, not the lot-and-slot key), with E22 (the deciding comparison: isolated counterfactual excess) at rung 1 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #18 joins only on the visible key · #20 leaves the deciding comparison unstated · #4 never tests its reading against the control |
| Calibration form | Change-log natural experiments: fourteen closed excursions in the equipment change log, each with the chamber fixed and the yield before and after |
| Driving force | Process history records each wafer by its lot and slot at every step, and sort results by lot and slot at the end of the line. Since this quarter a sorter re-slots wafers before CMP by incoming film thickness, so for 38% of wafers the lot-and-slot join succeeds on every row and attaches the wrong history to each. The deposition chamber that thickens its wafers also gets them routed to one CMP head, which then looks guilty. Only the scribe id the sorter reads, a second identifier carried in its own log, ties each result to its own past. |

## 1. Situation

A logic fab's sort yield fell over six weeks: 2,200 more failing wafers than the baseline rate. The yield engineering team can spend one week on one tool
or chamber: etch tool E3 (A), scanner S4 (B), CMP polisher P1's carrier head 3 (C), deposition chamber D2-C (D) or implanter I2 (E). The fab manager
suspects a focus drift on the scanner, the etch module owner points at the etch bay, and the data scientist's wafer-level model puts the CMP head on
top. The yield board's charter governs how the week is assigned. The equipment change log records every past excursion and the fix that ended it.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: sort results, process history at every step, the sorter's log, the lot genealogy and the change log. The
  lot-and-slot key is the manufacturing system's documented key and is unique at every step. Nobody's reading of their own numbers is
  overturned; the difficulty is that the key joins correctly-recorded rows to the wrong wafers.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice and the licensed basis. The wafer-level model on the documented key still names the CMP head, and no
  join fails.
* **Instrument repair.** Make every record perfect: process history still keys wafers by slot at each step, as the system is designed, and the
  sorter still re-slots them. The link exists only through the scribe id in the sorter's log.
* **Lens swap.** The naive build attributes each failing wafer to the history of whichever wafer held its slot earlier; the answer attributes it
  to its own history: a different wafer population behind every pre-sorter step.

## 3. The driving force

A strong solver knows lot-level commonality is confounded by scheduling, so it fits a joint model with week effects and compares isolated
counterfactuals: the excess failing wafers each tool accounts for, holding the others fixed. At lot level that points at the scanner, because
every lot visits all four deposition chambers and the chamber cannot show. It moves to wafer level, joins sort results to process history on lot
and slot, and every row matches. The CMP head now leads. The CMP module's loading procedure assigns incoming wafers to carrier positions by
measured thickness, which a sorter does by moving them between slots, so for 38% of wafers the slot at deposition is not the slot at sort, and
the documented key quietly gives them a neighbour's deposition chamber. Chamber D2-C's degrading showerhead thickens its wafers; the sorter
routes thick wafers to head 3; so head 3 carries D2-C's failures while D2-C's own signal is diluted by mislinked neighbours. Linking through the
scribe id the sorter reads moves 640 excess wafers off the CMP head and puts D2-C at 900.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Lot-level commonality: failing-lot rate for lots through each tool against lots not through it | A, etch tool E3 (1.74×) | The standard commonality screen, run on the yield board's own lots | The week mix: E3 ran 70% of the excursion weeks' lots, and its ratio collapses with week effects |
| 1 | Lot-level joint model with week effects; each tool's isolated counterfactual excess failing wafers | B, scanner S4 (640 wafers) | Confounding removed and the deciding comparison computed, not read one tool at a time | The change log: lot-level models found the fixed chamber in 8 of 14 closed excursions, missing every chamber-level fault |
| 2 | Wafer-level joint model, sort results joined to process history on lot and slot | C, CMP head 3 (790) | Wafer grain, the documented key, every row matched, the excess sums to 2,200 | The sorter log: 38% of this quarter's wafers changed slot before CMP, each with its scribe id |
| 3 | **Decisive:** the same model with every wafer linked to its own history through the scribe id in the sorter log | **D, deposition chamber D2-C (900 wafers)** (5th of 5 on rung 0) | — | — |

* **Position table.** D ranks 5th on rungs 0 and 1 and 3rd on rung 2, and leads only rung 3. Rung leaders beat their runners-up by 1.26×,
  2.06×, 1.41× and 1.50× (900 against the scanner's 600).
* **Discriminator dominance.** The CMP head carries a 1.52× lead into rung 3 (790 against 520). Relinking multiplies D2-C's excess by 1.73 and
  the head's by 0.19, an edge of 9.1×, far above the required 1.2 × 1.52 = 1.82.
* **Partial correction priced (L3).** A solver who suspects identity problems but links through the lot genealogy table (splits and merges)
  changes nothing, because re-slotting creates no new lot: C 790 against B's 560 (1.41×), rung 2's answer. A solver who finds the sorter but
  drops the re-slotted wafers rather than relinking them throws away the thick wafers, and the thick wafers are D2-C's: 84% of its wafers were
  re-slotted against 23% of the rest, so its excess falls to 140 and the scanner leads, B 450 against A's 225 (2.0×), rung 1's answer.
  Scaling the kept 62% back up to all wafers changes no ranking.
* **Grid.** Grain (lot, wafer) × model (single-factor, joint) × link (lot and slot, genealogy, re-slotted dropped, scribe id) gives ten builds,
  the link mattering only at wafer grain. Every single-factor build names A, because E3's week mix tops every ratio (1.70 against D2-C's 1.42
  even on the scribe link); the lot-level joint model names B; wafer-level joint builds name C on the documented key or the genealogy and B
  with the re-slotted wafers dropped; only the joint model on the scribe link names D, at 900.
* **The deciding comparison (#20).** D2-C's 900 excess wafers against the scanner's 600 is the sentence the board note carries.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The CMP loading procedure says wafers are placed by thickness; the data dictionary says history is keyed by lot and
   slot. No document mentions slots changing, says the key changes meaning after the sorter, or names the scribe id as the link.
2. **Corpus blind for a computable reason.** *Every closed excursion predates the sorter's thickness routine, which began this quarter, so in
   every closed case each wafer's slot never changed between deposition and sort and the lot-and-slot key equals the scribe link.* The change
   log certifies the wafer-level joint model (14 of 14 fixed chambers found) and cannot see the relink.
3. **No arithmetic symptom.** The documented key matches 100% of rows, wafer counts tie at every step, and the joint model's excess sums to
   2,200 under both links.
4. **Not a row predicate.** Each wafer's history is assembled across steps by following its scribe id through the sorter event, a hop through a
   second identifier on a different log.
5. **The enumeration is arithmetic.** Which failing wafers passed D2-C is rebuilt for 38% of them; no column carries it.
6. **No cutover date.** D2-C's showerhead deposit grows steadily since its last clean; the dated event (the scanner's lens recalibration in
   week 2) is the decoy.
7. **Survives deletion.** With every voice gone, the wafer-level model on the documented key still names the CMP head.

## 6. The calibration corpus

* **Form.** Fourteen closed excursions in the equipment change log, each with its weeks, the chamber or tool fixed, and sort yield before and
  after the fix, plus the full wafer-level data of each excursion's weeks.
* **What it certifies.** The wafer-level joint model with isolated counterfactuals: it names the fixed chamber in 14 of 14 cases, the lot-level
  joint model in 8, lot-level single-factor ratios in 5. The yield recovered after each fix matches the model's excess for that chamber within
  7%.
* **What it is blind to.** The relink (above).
* **Twin pair.** Lots L-4471 and L-4519 followed identical lot-level routes through identical tools and chambers in the same week and failed 12
  and 6 wafers (2.0×). Only the scribe-linked history separates them: 12 of L-4471's wafers passed D2-C, 6 of L-4519's, though the lot-and-slot
  key gives both lots the same count.
* **Resemblance points at the decoy.** This excursion's lot-level profile matches EX-09, a closed CMP-head excursion, on product, weeks and
  failing-bin signature.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The yield board's charter: the engineering week goes to the tool or chamber whose wafers account for the most excess failing
  wafers over the excursion weeks, against the baseline rate. The CMP module's loading procedure: incoming wafers are assigned to carrier
  positions by measured film thickness to balance removal rates. Neither sentence mentions slots or keys.
* **Empirical pins.** The joint model's form, certified by the change log; each wafer's chamber from the scribe-linked history.
* **Voices.** The data scientist: "Every wafer-level model I run puts the CMP heads on top." The etch module owner: "At lot level the failing
  lots all came through my bay that week; it's a scheduling story."
* **Licensed wrong basis.** The charter records that corporate quality ranks tools by lot-level commonality and will present that ranking at
  the board.

## 8. Determinism by construction

* **Baseline.** The failing-wafer rate of the eight weeks before the excursion, by product; the board's charter fixes the window.
* **Model.** Additive excess by tool or chamber with week and product effects; the excesses sum to the total under every link.
* **Link.** Every re-slotted wafer has exactly one sorter event with a readable scribe id; no wafer was re-slotted twice.
* **Failing wafer.** A wafer fails when its final sort bin is a failing bin, per the binning guide; retests resolve to the last test.
* **Rounding.** Excess wafers to the nearest ten; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> Sort yield has been bleeding for six weeks and the yield team has one week to spend on one tool. The fab manager is sure the scanner's focus has
> drifted. Tell me which tool or chamber gets the week and how many of the excess failing wafers its wafers account for, set against the next
> candidate's, in a sentence for the yield board. Send `excursion_case.xlsx` and a chart `excess_by_tool.png`.

* `excursion_case.xlsx` — the five candidates under each construction, the SPC sheet (ask A), the equipment-state sheet (ask B) and the
  change-log back-test (ask C).
* `excess_by_tool.png` — paired bars of each candidate's excess failing wafers on the documented key and on the scribe link, with an inset
  flow diagram of D2-C's wafers through the sorter to the CMP heads, and the committed candidate and its runner-up labelled.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 inline metrology steps and each excursion week, out-of-control points on the SPC
  charts. *Device:* metrology records nine sites per wafer and the control charts are kept on the wafer mean, as the SPC plan documents;
  counting out-of-control sites overstates every step and reorders the worst three.
* **Ask B (device-carried).** For each of the five candidates, availability and unscheduled down events over the quarter. *Device:* the
  equipment-state log follows the industry state model, in which engineering time is neither productive nor down, as the state guide documents;
  counting engineering time as down understates availability for the two tools that ran qualification lots.
* **Ask C (validity).** For each of the fourteen closed excursions, the chamber each of the four constructions names against the chamber fixed;
  and each candidate's excess under each construction.
* **Decoupling.** Clearing the scribe link changes no figure in asks A or B.

## 11. Rubric arithmetic

12 steps × 6 weeks (ask A) + 5 candidates × 2 figures (ask B) + 14 excursions × 4 constructions + 5 candidates × 4 constructions (ask C) + the
committed candidate, its excess and the runner-up's + 5 named chart parts + 2 files ≈ 175 criteria.

## 12. World-building constraints

* 2,200 excess failing wafers. Lot-level ratios A 1.74, B 1.38, E 1.21, C 1.12, D 1.00; lot-level joint excess B 640, A 310, E 260, C 190, D 0;
  wafer-level on the documented key C 790, B 560, D 520, A 190, E 140; scribe-linked D 900, B 600, A 300, E 250, C 150.
* 38% of this quarter's wafers re-slotted before CMP: 84% of D2-C's wafers against 23% of the rest. D2-C's wafers are 2.4× more likely than
  others to be routed to head 3.
* Re-slotted wafers dropped (joint model, wafer level): B 450, A 225, E 190, D 140, C 110. Wafer-level single-factor ratios on the scribe link:
  A 1.70, D 1.42, B 1.30, E 1.15, C 1.05.
* Change log: 14 closed excursions, all before the sorter routine; wafer-level joint model 14/14, lot-level joint 8, single-factor 5.
* L-4471 and L-4519 identical on every lot-level column.
* SPC sites and engineering states touch no sort result, sorter event or process-history row.
