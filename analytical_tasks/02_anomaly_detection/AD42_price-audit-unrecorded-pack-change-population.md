# AD42 — Which category gets next quarter's price-quality audit, when the biggest index error is in quotes whose price never moved

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Economics · consumer price statistics |
| Mirrors | Catalogue-quality and price-intelligence teams catching unrecorded pack-size changes (unit-price monitoring at Amazon and Walmart, product matching for Google Shopping), where the listing says "same product" and the barcode says otherwise |
| Decision shape | Which of N gets one scarce thing: the single quality-audit team for next quarter goes to one of five item categories |
| Committed call | The category audited, and the error in the all-items index the audit should remove, in thousandths of an index point |
| Gap · Pattern | Gap 2 (population: which quotes are truly comparable) over Gap 4 (rule) · the population a flag suggests (the collector's comparability indicator against each outlet's own switch date to a new barcode), with the outlet as the unit (shop codes linked across re-coding) below it |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection support |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #2 counts file rows instead of the real unit · #7 uses the ready-made measure |
| Calibration form | Retry or revision log: the quote revision log, including every correction from eight quality audits in 2023–2025 |
| Driving force | Every price screen judges prices, and the largest error in the index sits in quotes whose price never moved: a confectionery bar that shrank from 200 g to 190 g at the same price is still marked "comparable" by a collector looking at an identical wrapper. Comparability is defined by the product's specification, and a pack change shows only as a new barcode in the manufacturers' product register and in each outlet's scanner sales from the day that outlet first sold it. The affected quotes are those collected after their own outlet's switch date, a first-sale date per outlet and product that no quote field carries. |

## 1. Situation

A national statistics office compiles its consumer price index from about 110,000 local price quotes a month. Its quality-audit team can
take one item category next quarter: re-check every quote's product identity and price, and back-correct the category index. The audit
charter scores an audit on the error it removes from the all-items index. Five categories are candidates. The office holds two years of
quotes with collectors' validity and comparability indicators, the shop register, the manufacturers' product register (barcode, net quantity
and launch date), scanner sales from every sampled outlet's chain, the category weights and the quote revision log. The validation lead points
at toiletries, where the flags pile up.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each quote's price, each collector's indicator as recorded, each screen's flags, the registers and the
  scanner sales. The validation lead is right that toiletries generate the most flags. Nothing reported is overturned; the difficulty is a
  population (quotes collected after their outlet's switch) that no indicator marks.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the validation lead's view and the legacy flag file. A within-outlet relative-change screen on linked outlets
  still names cereals.
* **Instrument repair.** Make every price exact and every indicator filled: they are. A collector's "comparable" is an honest record of a
  wrapper; the specification change lives in the product register and the outlet's sales, which no quote form records.
* **Lens swap.** The naive population is quotes the screens flag; the answer's is quotes collected after each outlet's switch to a smaller
  pack, a different set of quotes (mostly unflagged) defined by a date per outlet.

## 3. The driving force

A strong solver discards the cross-shop level rule (premium shops are not errors), validates each outlet's price against its own previous
quote, links outlets through the shop register when a chain re-codes its shops, and values each category by the index error its flagged
quotes carry. Every step is correct, and every step looks at prices. The office's manual defines a comparable quote as one whose product
specification, quantity included, is unchanged since the base month. In confectionery, a manufacturer cut eleven lines by 5–10% at the same
price, and collectors kept marking the quotes comparable because the wrapper did not change. The product register shows each new barcode and
its quantity; each outlet's scanner sales show the first day that outlet sold it, which differs by outlet as old stock ran down. Quotes
collected after the outlet's own first sale are non-comparable, and their per-unit price rose by the pack cut. That is a first-sale date per
outlet and product, joined back to the quotes.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Index error carried by quotes outside the cross-shop level rule (thousandths of an all-items point): A 4.1, B 3.4, C 2.9, D 2.6, E 2.2 | A, toiletries | The office's legacy screen and the flag volume | The quotes themselves: A's flagged outlets sit at the same distance from the median in every month, premium shops not errors |
| 1 | Error carried by quotes outside item-month fences on log relatives, matched on shop code: B 3.8, C 3.0, A 2.6, E 2.1, D 1.7 | B, soft drinks | Within-shop change is the right comparison | The shop register: a chain re-coded 140 outlets in March, so their quotes fall out of matching as "unmatched" and their errors go unseen |
| 2 | The same with outlets linked across re-coding through the shop register: C 3.6, E 2.9, B 2.6, A 2.4, D 1.8 | C, cereals | Every outlet matched to its own history | The product register: eleven confectionery lines changed barcode and net quantity at unchanged prices this year |
| 3 | **Decisive:** add the error in quotes collected after their outlet's first scanner sale of a new, smaller barcode, whatever the collector's indicator says: E 6.3, C 3.6, D 3.1, B 2.6, A 2.4 | **E, confectionery** (5th of 5 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0, 4th on rung 1 and 2nd on rung 2 (C leads it by 1.24×), and leads only rung 3. Rung leaders beat
  their runners-up by 1.21×, 1.27×, 1.24× and 1.75×.
* **Discriminator dominance.** C carries a 1.24× advantage into rung 3. E's error rises 2.17× when unrecorded pack changes are counted while
  C's is unchanged (no cereal line changed quantity), so the net is 2.17 / 1.24 = 1.75×.
* **Partial correction priced (L3).** A solver who finds the barcode changes but dates every outlet's switch at the manufacturer's launch date
  marks quotes non-comparable before outlets had sold through old stock and names D, whose launches were early and sell-through slow: a new
  wrong name, further from E than rung 2.
* **Grid.** Screen (level or relative) × outlet unit (shop code or linked) × comparable population (indicator, launch date, outlet first
  sale) = 12 cells. Level cells name A; relative cells name B or C under the indicator, D under launch dates, and E only with linked outlets and
  first-sale dates.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The manual defines comparability by specification; no document says collectors miss quantity changes, and the
   product register and scanner feeds are filed for the scanner-index project.
2. **Corpus blind for a computable reason.** *In every one of the eight audits in the revision log, no product in the audited category
   changed barcode during the audit window, because audits were scheduled outside the manufacturers' launch seasons.* The log's corrections
   are entry errors and re-coded outlets, which rung 2's construction reproduces in all eight, and it cannot show a pack change.
3. **No arithmetic symptom.** Prices are plausible, relatives sit inside fences, indicators are complete, and the affected quotes are
   arithmetically indistinguishable from unchanged ones.
4. **Not a row predicate.** Each outlet's switch date is the minimum sale date of the new barcode in that outlet's scanner sales, a group and
   a rank over another entity, joined back to the quotes by outlet and product.
5. **The enumeration is arithmetic.** 1,900 affected quotes are computed; no field marks any of them.
6. **No cutover date.** Outlets switched over five months as stock ran down, so no category series steps on a date.
7. **Survives deletion.** Remove both voices and the legacy flags, and the linked-outlet relative screen is still the natural build.

## 6. The calibration corpus

* **Form.** The quote revision log: every quote revised after validation in 2023–2025, with its original and revised price and indicator,
  its reason code, and the corrections from eight quality audits.
* **What it certifies.** The linked-outlet relative construction reproduces each audit's correction count and the index error it removed, so
  a back-tester is confirmed at rung 2. The level rule reproduces two of eight audits and the shop-code relative screen five.
* **What it is blind to.** Pack changes (above). The pin for the decisive rung is the manual's definition of comparability together with the
  registers, which enumerate the affected quotes exactly.
* **Twin pair.** Two confectionery lines, quoted at the same outlets, rose from £1.00 to £1.05 over the year and were marked comparable
  throughout. One moved to a 190 g barcode in May at those outlets, so its per-unit price rose 10.5% against the other's 5.0%, 2.1× apart,
  separated only by the outlet first-sale join.
* **Resemblance points at the decoy.** On every screen confectionery resembles the two categories whose audits found the least.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The audit charter: an audit is scored on the error it removes from the all-items index. The manual: a quote is comparable
  only when the product's specification, quantity included, is unchanged since the base month. The category weights. One sentence each.
* **Empirical pins.** Each outlet's switch date, from its scanner sales; each line's quantity change, from the product register.
* **Voices.** The validation lead: "Toiletries throw more flags than everything else put together." The field manager: "My collectors check
  every pack; if it says comparable, it is."
* **Licensed wrong basis.** The charter records that the national accounts liaison ranks categories by validation flag volume and will bring
  that ranking to the audit planning meeting.

## 8. Determinism by construction

* **Coverage.** Every sampled outlet in the five categories belongs to a chain that supplies scanner sales, so every switch date exists.
* **Switch dates.** No outlet sold the old and new barcode of one line on the same collection day, so first-sale and last-old-sale dates
  give the same quotes.
* **Per-unit change.** Net quantities come from the product register, so no size convention is chosen.
* **Rounding.** The committed figure is given to a tenth of a thousandth of a point; E's 6.3 sits mid-bin.

## 9. Prompt sketch and deliverables

> The quality-audit team can take one category next quarter, and five are on the list. Our validation lead points at toiletries, where the
> flags pile up. Tell me which category we audit and how much error it should take out of the all-items index, in thousandths of a point to
> one decimal, in a line for the planning meeting. Send `audit_case.xlsx`, a chart `per_unit_drift.png`, and a one-page `audit_note.pdf`.

* `audit_case.xlsx` — the five categories under each rung's basis (ask C), the field-time sheet (ask A) and the product-count sheet (ask B).
* `per_unit_drift.png` — for the eleven changed confectionery lines, quoted price and per-unit price by month, each outlet's switch date as a
  tick, the gap between the two lines shaded, and each category's removable error in a side panel.
* `audit_note.pdf` — the committed category and figure, and why each other category falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of twelve regions, collector-days last year and quotes per collector-day. *Device:* one
  region's legacy timesheets record half-days as 0.5 and the others as 4 hours, as the timesheet guide says; mixing them halves that region's
  productivity. The audit choice never uses timesheets.
* **Ask B (device-carried).** For each category, distinct products quoted and the share quoted at only one outlet. *Device:* product
  descriptions carry case and trailing-space variants of one description, which the glossary treats as identical; counting raw strings
  inflates distinct products in four categories. The decisive construction links quotes to barcodes through product codes, never descriptions.
* **Ask C (validity).** Each category's figure under each of the four rung bases.
* **Decoupling.** Clearing the switch-date population and the outlet linking changes no figure in asks A or B.

## 11. Rubric arithmetic

12 regions × 2 (ask A) + 5 categories × 2 (ask B) + 5 × 4 bases (ask C) + the committed category, its removable error, the runner-up and the
margin + 5 named chart parts + 3 files ≈ 66 criteria.

## 12. World-building constraints

* Rung figures as in the ladder; E is 5th, 4th, 2nd (1.24× behind C) and 1st.
* Eleven confectionery lines cut 5–10% at unchanged prices; 1,900 quotes collected after their outlet's switch, all marked comparable. No
  cereal line changed quantity; D's changes launched early and sold through slowly.
* 140 outlets re-coded in March, linked one to one in the shop register.
* The eight audits fall outside every launch season.
* Timesheets and product descriptions never touch quote prices, indicators, registers or scanner sales.
