# DA29 — Which model family gets the one corrosion engineering review, when a vehicle's test history is split across the registration marks it has carried

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Supply Chain & Logistics · after-sales warranty and reliability |
| Mirrors | Reliability and churn analytics where one entity's history splits across identifiers that change on an event (a device re-enrolled after a factory reset, a number ported between carriers, a marketplace seller re-onboarded under a new storefront ID) |
| Decision shape | Which of N gets one scarce thing: the body-engineering team can review one family's corrosion protection this year |
| Committed call | The family reviewed, and its share of vehicles with a structural corrosion failure by the eighth anniversary, to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · Pattern D (two grains: registration keys against vehicles), with the unit built from test rows at rung 1 (S1) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #18 joins only on the visible key · #2 counts file rows instead of the real unit · #13 validates on one population, applies to another |
| Calibration form | Change-log natural experiments: seven logged running changes to corrosion protection on predecessor families, each with before and after cohorts and the effect the engineering report measured |
| Driving force | The test record's key identifies a registration mark, not a vehicle. When an owner keeps a personal mark at sale, the vehicle continues under a new key, and its next corrosion failure is counted as a second first onset. The transfer register links the keys, a two-hop chain nothing invites. In the premium saloon a quarter of vehicles carry two keys by year eight. |

## 1. Situation

A manufacturer's body-engineering team has one corrosion-protection review this year, and the warranty policy sends it to the family whose
vehicles most often reach a structural corrosion failure within the extended warranty's eight years. Six families from 2008–2012
registrations are in scope. The pack holds the annual roadworthiness test records with failure items, the testing manual, the registration
transfer register, the change log of past running changes with their engineering reports, and the dealer council's notes.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each test row, each failure item, each transfer and each logged effect. Nobody reports a family
  ranking and nothing is overturned. The difficulty is what one vehicle is in a record keyed by its marks.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the dealer council's notes and both voices. The interval-censored estimate on test keys, certified by the
  change log, still names the premium saloon.
* **Instrument repair.** Record every test and mark perfectly: the key still follows the mark by design, and every row is right. The
  vehicle is a chain across two files, so a better test record leaves the construction to be done.
* **Lens swap.** The naive population is registration keys; the answer's population is vehicles, some of which are two keys. Counts,
  denominators and onsets all differ, not only the lens.

## 3. The driving force

A strong solver groups retests into annual cycles, builds each key's intervals between its last passing and first failing cycle, runs the
interval-censored estimator, and checks it against the change log: all seven logged effects reproduce. It names the premium saloon. But a
key is a mark. Owners of the saloon keep personal marks when they sell, so the car carries on under a new key. If the car had a corrosion
repair under its first mark, its next failure under the second is counted as a new first onset, and its early survival is counted twice.
The transfer register holds the chain from old mark to new mark at a dated transfer. Linked into vehicles, the saloon falls from 16.8% to
8.4%, and the van-derived MPV, whose owners almost never transfer, leads at 13.6%.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Corrosion-failing test rows ÷ test rows, ages 3 to 8 | A, Kestrel hatchback (15.0, 1.23× Marlin) | The dealer council's measure, read straight off the records | The warranty policy counts vehicles, and the testing manual groups retests into one annual cycle |
| 1 | First corrosion-failing cycle as onset, share of keys observed through year eight | D, Puffin city car (13.0, 1.23× Kestrel) | The right unit and a clean empirical share | The change log: this estimator misses every logged effect by 1.5 to 3.0 points |
| 2 | Interval-censored estimate on key histories (last passing to first failing cycle, right-censored keys kept) | C, Osprey saloon (16.8, 1.23× Tern) | Certified: it reproduces all seven logged running-change effects within 0.2 points | The transfer register: 9% of keys in scope continue a vehicle already tested under another mark |
| 3 | **Decisive:** the same estimator on vehicle histories linked across mark transfers | **E, Tern MPV (13.6, 1.24× Kestrel)** (5th of 6 on rung 0) | — | — |

* **Position table.** Tern ranks 5th on rung 0 (9.4), 4th on rung 1 (9.6) and 2nd on rung 2 (13.7, 1.23× behind the saloon, its only
  second place), and leads only rung 3.
* **Discriminator dominance.** The saloon carries 1.23× into rung 3. Linking keeps 0.99 of Tern's rung-2 share and 0.50 of the saloon's, an
  edge of 1.99×, against the 1.2 × 1.23 = 1.47 needed (1.35× headroom). The product, 1.99 / 1.23 = 1.62, is Tern's lead over the saloon
  on rung 3.
* **Partial correction priced (L3).** A solver who links only keys whose first test fails (the visible oddity) and leaves passing
  continuations unlinked still names the saloon, at 15.9, 1.17× Tern's 13.6, because the double-counted early survival stays in. A
  solver who drops late-starting keys as imports deletes the post-transfer years and names the Puffin city car at 13.0, 1.16× Tern's
  11.2. Neither half lands on Tern.
* **Grid.** Grain (rows or cycles) × estimator (empirical or interval-censored) × identity (keys or linked vehicles) = 8 cells. Seven name
  Kestrel, Puffin or Osprey. Only cycles, interval censoring and linking name Tern.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The test data guide defines the key as "a stable identifier for the registration mark under which the test was
   conducted". The transfer register's note describes marks moving between vehicles. No document joins the two or mentions histories.
2. **Corpus blind for a computable reason.** *In every logged running change, linking changes nothing, because each change was measured on
   fleet registrations and fleet leases bar mark transfers before the eighth year.* The change log certifies rung 2 exactly and cannot see
   the split.
3. **No arithmetic symptom.** Each key's history is internally consistent: one first-use date, ages rising, cycles in order. Keys whose
   first test falls at year five or six look like imports or late registrations, which the guide also describes.
4. **Not a row predicate.** It needs key → mark → transfer row → previous mark → previous key, a merge of interval histories in date
   order, and the estimator rerun on vehicles.
5. **The enumeration is arithmetic.** Which keys are continuations is computed through the chain; no column flags them.
6. **No cutover date.** Transfers happen continuously at sale, and no series steps.
7. **Survives deletion.** With every voice removed, the certified estimator still names the saloon.

## 6. The calibration corpus

* **Form.** The change log: seven running changes to underbody protection on predecessor families, each with its cut-in date, before and
  after fleet cohorts of 1,800 to 6,200 vehicles, and the eight-year failure effect measured in the engineering report from fleet warranty
  repairs.
* **What it certifies.** The interval-censored estimator on cycles: 7 of 7 effects within 0.2 points. The empirical estimator misses all
  seven by 1.5 to 3.0 points, and the row grain by more, always toward a smaller effect.
* **What it is blind to.** Mark transfers (above).
* **Twin pair.** Two saloon sales cohorts, through Harcourt Motors (private buyers) and Linden Fleet, are identical on every key-level
  column: keys, cycles, failing cycles by age and intervals. Their linked eight-year shares are 6.8% and 13.6% (2.0×); 31% of Harcourt's
  keys are continuations and none of Linden's.
* **Resemblance points at the decoy.** On key-level failure curves, the saloon most resembles the logged cohorts with the fastest
  corrosion.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The warranty policy: the review goes to the family whose vehicles most often reach a structural corrosion failure within
  the extended warranty's eight years. The testing manual: a retest within 10 working days belongs to the failed test's cycle. The
  reliability memo lists the structural corrosion items in both item-code versions.
* **Empirical pins.** The estimator, from the change log. Vehicle identity, from the transfer register.
* **Voices.** The quality director: "The saloon is where corrosion shows first; it always has." The data team lead: "A key is a vehicle as
  far as the test record is concerned."
* **Licensed wrong basis.** The warranty policy records that the dealer council ranks families on corrosion failures per thousand tests and
  will present that at the review planning meeting.

## 8. Determinism by construction

* **Links.** Every transfer row resolves to exactly one previous key and one next key; no mark is reused within 90 days, so no link is
  ambiguous.
* **Cycles.** No two first tests of a vehicle fall within 60 days, so the cycle rule has one reading.
* **Estimator.** Converged to 1e-8. No interval endpoint lies within 0.1 years of the eighth anniversary, so flat-region conventions agree.
* **Scope.** First-use dates fix the 2008–2012 registrations; transferred vehicles keep their first-use date under every key.

## 9. Prompt sketch and deliverables

> Body engineering can take one family's corrosion protection this year and quality says it has to be the saloon. Tell me which family
> gets the review and what share of its vehicles reach a structural corrosion failure by year eight, to one decimal, in one line for the
> planning meeting. Send `corrosion_review.xlsx`, a chart `onset_curves.png`, and a one-page `review_choice.pdf`.

* `corrosion_review.xlsx` — the onset build for all six families, the failure-location sheet (ask A), the mileage sheet (ask B) and the
  change-log table (ask C).
* `onset_curves.png` — cumulative corrosion-failure curves to year eight for the six families on linked vehicles, with the saloon's
  key-level curve dashed beside its linked curve, the eight-year line labelled, and the reviewed family marked.
* `review_choice.pdf` — the committed family, its share, and why each other family falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each family, the most frequent structural corrosion location and its share of corrosion
  failures. *Device:* failure items were renumbered in 2018 and the item-detail file maps old codes to new ones; counting raw codes splits
  sills and subframe mounts in four families.
* **Ask B (device-carried).** For each family, the median annual distance between consecutive cycles in the latest year. *Device:* the
  odometer unit field marks 4% of readings in kilometres; ignoring it inflates three families' medians. The onset build never reads
  odometers.
* **Ask C (validity).** Each family's eight-year share under each rung, and each estimator's error on the seven logged effects.
* **Decoupling.** Clearing the linkage changes no figure in asks A or B.

## 11. Rubric arithmetic

6 families × 2 (ask A) + 6 medians (ask B) + 6 × 4 rungs and 7 × 3 estimator errors (ask C) + the committed family, its share and its
margin + 5 named chart parts + 3 files ≈ 74 criteria.

## 12. World-building constraints

* Eight-year shares (%): rung 0 A 15.0, B 12.2, C 11.5, D 10.6, E 9.4, F 8.1; rung 1 D 13.0, A 10.6, C 10.4, E 9.6, B 9.1, F 7.0; rung 2
  C 16.8, E 13.7, D 13.4, A 12.0, B 10.8, F 8.4; rung 3 E 13.6, A 11.0, B 10.5, D 10.2, C 8.4, F 8.0.
* Keys that continue an earlier vehicle by year eight: saloon 25%, city car 14%, hatchback 6%, MPV 1%; 9% of all keys in scope.
* No fleet-registered vehicle in the change log carries a transfer before year eight. Harcourt and Linden match on every key-level column.
* Item renumbering and odometer units never touch a structural corrosion item's presence or a cycle's date.
