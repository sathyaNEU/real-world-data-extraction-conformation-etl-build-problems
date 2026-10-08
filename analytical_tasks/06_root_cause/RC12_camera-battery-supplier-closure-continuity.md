# RC12 — Which field action the security-camera line takes this quarter, when the cell supplier's closure notice did not end its cells

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Product Analytics · hardware field reliability |
| Mirrors | Battery and component field issues at device makers (Apple, Google Pixel, Meta Quest), where a supplier's closure notice reads as the end of the exposure while goods-receipt records show the same cells arriving under a successor vendor code |
| Decision shape | Which of N root causes gets the fix: one field action across the installed base this quarter |
| Committed call | The field action taken, and the battery failures it prevents over the next twelve months |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · E24 (continuity across a closure: the supplier's plant closure against goods receipts that carry its cells on), with E20 (an implicit join: retail complaints reach serial numbers only through the RMA log) at rung 1 |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #23 reads a closure notice as a market exit · #18 joins only on the visible key · #13 validates on one population, applies to another |
| Calibration form | Pilot log: last quarter's randomised battery-swap pilot on 4,000 cameras, with failures by arm and the quality board's filed decision |
| Driving force | Cameras built with one cell chemistry swell at four to ten months in service. The supplier filed a plant-closure notice three months ago, and procurement reads it as the end of those cells. Goods receipts show the same cell part number and lot prefix arriving since then under a successor's vendor code. Cameras built since the closure are too young to have failed, so no failure record can show it. They carry most of the forward risk, and only the receipts put them in scope. |

## 1. Situation

Battery complaints on a battery-powered home security camera roughly tripled in the two quarters after a power-management firmware release. The
software team has a rollback ready. The hardware quality board will take one field action this quarter: roll back the firmware (A), swap batteries
in cameras built with the affected cells (B), recall a charger batch (C), rework a thermal pad in one enclosure revision (D), or push a configuration
that turns off an always-on radio feature (E). The cell supplier changed its chemistry 14 months ago and filed a plant-closure notice three months ago;
a successor company took over its open orders. Last quarter the board ran a randomised battery-swap pilot.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: complaints, RMA records, warranty registrations, build records with each camera's cell lot, goods
  receipts, the closure notice and the pilot. The closure is real and procurement reads it accurately as a legal fact. Nothing is overturned;
  the forward population the swap must cover is not the population any closure-dated scope describes.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete procurement's view, the head of product's belief and the licensed basis. The build records still carry the old
  vendor code only up to the closure, and the cohort analysis still bounds the swap there.
* **Instrument repair.** Suspect file: the complaint form's serial field, blank on retail complaints that carry only an RMA number. Repaired so
  that every complaint carries its serial, rung 1 returns D (the enclosure rework, 3,300), as rung 2 does, and rung 0's calendar step still
  names A; none returns B. The build records' vendor code is correct (the successor has been the vendor of record since the closure) and every
  camera's cell lot is on its build record. The answer still needs the forward population: cameras built since the closure are under four months
  old, so no failure record, however complete, can show them, and only the receipts carry their cells' part number across the closure.
* **Lens swap.** The naive scope is cameras with the old vendor code, built before the closure; the answer adds cameras built since, which have
  no failure history at all: a different population at a different age.

## 3. The driving force

A strong solver sees the calendar step at the firmware date and does not trust it: it builds the age-by-build-month table and finds the excess
is a cohort effect, early-age swelling in cameras built after the chemistry change. Retail complaints carry only the retailer's RMA number, and
linking them to serials through the RMA log adds the newest cohorts, sold mostly through retail. With the full link, the swap's scope looks like
"cameras whose cells came from the old vendor code": built from the chemistry change to the plant closure, 2,100 forward failures, less than the
enclosure rework. That scope follows the closure notice, and the cohort table seems to agree: the last cohorts before the closure, built while
the plant wound down and the line dual-sourced, drew only 13% of their cells from the affected lots, so the effect looks as if it is fading.
Goods receipts since the closure show the same cell part number, the same lot-number prefix and the same open purchase orders, transferred to
the successor's vendor code. Of the cameras built in the last three months, 73% carry those cells. They are under four months old, so they have
no failures yet and the most risk ahead. With them in scope the swap prevents 5,600 failures.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Complaints before and after the firmware release, the excess projected forward as the rollback's benefit | A, firmware rollback (6,800) | The calendar step is large and sits on the release date | The age-by-build-month table: the excess follows build month at early ages, not calendar month |
| 1 | Age-by-build-month hazard on complaints linked to serials through the complaint form's serial field; each action's forward failures prevented | C, charger recall (2,600) | Cohort effect found, forward sizing on the installed base | The RMA log: 41% of battery complaints come through retailers with an RMA number and no serial, concentrated in the newest cohorts |
| 2 | The same with retail complaints linked through the RMA log; the swap scoped to cameras with old-vendor-code cells | D, enclosure rework (3,300) | Every complaint linked, the cohort model fitted, the swap scoped by the build records' supplier field | Goods receipts: since the closure the same cell part number and lot prefix arrive under the successor's code |
| 3 | **Decisive:** the swap scoped by cell lot and part number through goods receipts, so cameras built since the closure are included | **B, battery swap (5,600)** (5th of 5 on rung 0) | — | — |

* **Position table.** B ranks 5th on rung 0 and 3rd on rungs 1 and 2, and leads only rung 3. Rung leaders beat their runners-up by 2.96×,
  1.37×, 1.27× and 1.70×.
* **Discriminator dominance.** The enclosure rework carries a 1.57× lead into rung 3 (3,300 against 2,100). Continuity multiplies the swap's
  forward failures by 2.67 and leaves the rework's unchanged, an edge of 2.67×, above the required 1.2 × 1.57 = 1.89; the net margin is 1.70×.
* **Partial correction priced (L3).** Every half-applied continuity names D, rung 2's answer. A solver who suspects the successor but extends
  the swap only to cameras whose post-closure cells came from successor lots that have already shipped in a failed camera finds none (no
  post-closure camera is old enough): B stays at 2,100 against the enclosure's 3,300 (1.57×). One who doubts the closure but has no cell link
  projects the post-closure cameras at the trend of the last observable cohorts, which the wind-down's dual sourcing pulled to 13% affected
  cells: B 2,720 against 3,300 (1.21×). Giving them the affected cells' hazard needs to know they carry those cells, which is the receipts
  link itself.
* **Grid.** Attribution (calendar, cohort) × link (serial field, RMA log) × scope (vendor code, recent cameras at the trend hazard, cell lots)
  gives seven builds, scope mattering only to the cohort builds. Calendar names A. Cohort on the serial field names C under every scope: the
  retail-heavy newest cohorts look nearly clean there, so even cell-lot scope lifts B only to 2,150 against C's 2,600 (1.21×). Cohort on the
  full link names D by vendor code (1.57×) or by the trend (1.21×), and B only by cell lots, at 5,600.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The closure notice states a legal fact; the successor's onboarding letter names a new vendor code. No document says the
   cells are the same or that the successor took over the old part numbers.
2. **Corpus blind for a computable reason.** *Every camera in the pilot was built before the closure notice, because the pilot drew from cameras
   at least six months in service, so the successor's code appears in no pilot case and the pilot cannot say whether its cells carry the
   effect.* It certifies the cohort hazard and that a swap removes it.
3. **No arithmetic symptom.** Complaints, RMAs, serials, build records and receipts reconcile; the post-closure cohorts have no failures because
   they are young, which is what every cohort that age looks like.
4. **Not a row predicate.** Scope runs camera → build record → cell lot → goods receipt → part number and lot prefix, matched across a vendor
   code change, then weighted by each cohort's remaining age-specific hazard.
5. **The enumeration is arithmetic.** Forward failures are the remaining twelve-month hazard summed over in-scope cameras by age; no column
   marks a camera "affected".
6. **No cutover date.** The closure is a dated event, and it is the decoy: nothing in any outcome series steps at it.
7. **Survives deletion.** With every voice gone, the build records' supplier field still ends the scope at the closure.

## 6. The calibration corpus

* **Form.** The pilot log: 4,000 cameras from cohorts built after the chemistry change, randomised to a battery swap or not, with failures by
  arm over the following quarter and the board's filed decision to extend the programme.
* **What it certifies.** The cohort hazard (rung 2's model reproduces the control arm's failures within 3%) and the swap's effect (the
  treated arm fails at the pre-change base rate).
* **What it is blind to.** Cameras built since the closure (above).
* **Twin pair.** Cameras built in September and in November of last year are identical on volume, enclosure revision, charger batch, firmware
  at ship and channel mix. Their four-to-ten-month failure rates are 1.9% and 0.9% (2.1×), because September's cameras drew 92% of their cells
  from the affected lots and November's 44% while the plant dual-sourced through a capacity shortfall. Only the cell-lot link reproduces both.
* **Resemblance points at the decoy.** The complaint mix (swelling reports clustered in summer) matches the closed enclosure-revision case, a
  heat-driven issue the board fixed two years ago.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The field-action standard: an action is judged on the battery failures it prevents across the installed base over the next
  twelve months. The build record carries each camera's cell lot.
* **Empirical pins.** The age-specific hazard from the cohort table and the pilot; scope from the cell lots in the receipts.
* **Voices.** The procurement manager: "The supplier shut that plant in July. Whatever their cells did, it stops with the July builds." The
  thermal engineer: "Revision C enclosures run hot in summer; that's what's swelling them."
* **Licensed wrong basis.** The standard records that the retail partners' quality team sizes field actions on calendar complaint rates and
  will present the rollback case on that basis.

## 8. Determinism by construction

* **Hazard.** Excess failures at ages 4–10 months only, estimated on cohorts observed through month 10; no cohort is partially censored inside
  the window it contributes.
* **Scope.** A camera is in scope when its cell lot carries the affected part number; the lot prefix and the part number agree for every
  receipt.
* **Forward window.** Twelve months from the extract; every in-scope camera's remaining hazard is computed from its age at the extract.
* **Swap effect.** A swapped camera fails at the base rate, as the pilot shows; the swap is assumed done at the start of the window.
* **Rounding.** Failures to the nearest hundred; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> Battery complaints on the camera have tripled since the firmware release and the quality board takes one field action this quarter. Our head
> of product is sure the release did it. Tell me which action we take and how many battery failures it prevents over the next twelve months, to
> the nearest hundred, as the line I put to the board. Send `field_action_case.xlsx`, a chart `cohort_hazard.png` and a one-page `board_note.pdf`.

* `field_action_case.xlsx` — the five actions under each construction, the shipments sheet (ask A), the firmware sheet (ask B) and the pilot
  reproduction (ask C).
* `cohort_hazard.png` — a heatmap of failure rate by build month and age with the unobservable region greyed, the chemistry change and the
  closure marked as vertical lines, and a side bar of forward failures by build month split by cell source.
* `board_note.pdf` — the action, its figure, and why the closure does not bound it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the last 18 production months, cameras shipped by channel. *Device:* unsold retail
  stock returned to the distribution centre is booked as a negative shipment dated on its return, as the logistics guide documents; netting by
  ship month misplaces 7% of retail volume into later months.
* **Ask B (device-carried).** For each firmware version and week, the share of the active fleet running it. *Device:* a camera that has not
  checked in for 30 days keeps its last reported version with a stale flag, as the telemetry guide documents; counting stale cameras overstates
  the oldest version's share by a fifth.
* **Ask C (validity).** For each pilot cohort month, failures in the treated and control arms and what each construction predicts; and each
  action's forward failures under each construction.
* **Decoupling.** Clearing the receipts-based scope changes no figure in asks A or B.

## 11. Rubric arithmetic

18 months × 2 channels (ask A) + 6 versions × 12 weeks (ask B) + 12 pilot months × 3 figures + 5 actions × 4 constructions (ask C) + the action,
its figure and the runner-up's + 5 named chart parts + 3 files ≈ 175 criteria.

## 12. World-building constraints

* Forward failures prevented by rung (A / B / C / D / E): 6,800 / 900 / 1,500 / 1,200 / 2,300; 600 / 1,400 / 2,600 / 1,900 / 1,000; 600 /
  2,100 / 2,600 / 3,300 / 1,000; 600 / 5,600 / 2,600 / 3,300 / 1,000.
* The closure was three months before the extract; the failure mode begins at four months; post-closure cameras are 31% of in-scope units and
  62% of the swap's forward failures.
* 41% of battery complaints are retail RMAs without a serial on the form.
* September and November cohorts identical on every cohort-summary column.
* The last four pre-closure cohorts drew 13% of their cells from the affected lots; 73% of post-closure cameras carry successor cells of the
  affected part number, the rest a second supplier's. B under the partial builds: successor lots with failures 2,100; post-closure cameras at
  the trend hazard 2,720; serial field with cell lots 2,150.
* Retail returns and stale check-ins touch no complaint, build record or receipt.
