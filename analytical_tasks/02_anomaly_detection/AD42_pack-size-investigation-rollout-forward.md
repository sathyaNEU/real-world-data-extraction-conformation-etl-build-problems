# AD42 — Which category gets next quarter's pack-size investigation, when last year's worst shrinkflation is already on every shelf

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Economics · consumer protection |
| Mirrors | Trust and catalogue teams choosing where an intervention can still stop a roll-out rather than where the harm has already landed (staged pack-size and price-per-unit changes on Amazon and Walmart marketplaces, staged feature roll-outs reviewed by Apple and Google app stores, region-by-region policy-evasion campaigns at Meta), where the harm already done ranks candidates almost in reverse of the harm still preventable |
| Decision shape | Which of N gets one scarce thing: the authority's single pack-size investigation next quarter goes to one of five product categories |
| Committed call | The category investigated, and the consumer detriment the investigation should prevent over the twelve months after it opens, to the nearest $100,000 |
| Gap · Pattern | Gap 1 (time: harm done against harm still preventable) over Gap 2 (population: the outlets a reduced pack has not reached) · Pattern A (past exceedance against forward yield), pinned by reproduction of the revision log (Pattern B), with the reduced line built from barcodes below it |
| Gate G mechanism | forecasting, with method_or_model_selection support |
| Measured traps engaged | #7 uses the ready-made measure · #2 counts file rows instead of the real unit · #1 reports a failed back-test, ships anyway |
| Calibration form | Revision log: the authority's investigation revision log, eight closed pack-size investigations (2019–2025), each with its opening estimate and the detriment prevented as revised at the twelve-month evaluation, with the scanner extracts and register snapshots behind both |
| Driving force | An investigation can stop a reduced pack reaching outlets it has not reached; it cannot take back the shelves already converted. The past twelve months' detriment, measured correctly outlet by outlet, is harm on converted shelves. Seven of cereals' eight smaller boxes have been on every shelf since May, so the largest past detriment has $0.4 million left to prevent. Confectionery's seven undeclared reductions converted one region in November and nowhere else yet, so 62% of their volume is still to come. Only detriment at the outlets that have not yet sold a line's reduced barcode, built outlet by outlet from first sales across each line's barcode change, reproduces all eight evaluated investigations, and it puts confectionery at $4.4 million against snacks' $1.3 million. |

## 1. Situation

A national consumer authority opens one pack-size investigation a quarter into a product category where packs shrank at unchanged prices,
and the outcome is undertakings from the manufacturers concerned. Its prioritisation framework values an investigation at the consumer
detriment it prevents over the twelve months after it opens, and admits an estimate only if its method reproduces every evaluated outcome in
the revision log within 5%. Five categories are shortlisted for the quarter opening on 1 October. The authority holds weekly scanner sales
for every outlet of the five largest grocery chains to the end of September, the national product register (barcode, line code, net
quantity, launch date and an optional successor barcode), the manufacturers' announced roll-out schedules filed with their launches, the
chains' listing files, household spend by category, the revision log, consumer complaints and shelf-label spot checks. The head of markets
says shoppers feel it most in toiletries.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the scanner sales, the register's quantities and links as declared, each category's past detriment,
  the schedules as announced, the listings and the evaluated outcomes. The chief economist is right that cereals carry the most detriment of
  the past year. Nothing is overturned; the difficulty is how much of each category's detriment is still to come at outlets the reduced
  packs have not reached.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the household spend table. The outlet-level past detriment, the authority's standard estimate,
  still names cereals.
* **Instrument repair.** Suspect files: the register's successor field (optional, and blank for 7 of confectionery's 11 reduced lines and 5
  of cereals' 8) and the manufacturers' announced schedules (filed at launch and since overtaken). Fill every successor link and replace the
  schedules with each manufacturer's current plan: rung 0 still names A on per-unit prices, rung 1 becomes rung 2 and names C, rung 2 still
  names C, and no rung reads the schedules. The forward construction is still needed: the past twelve months, measured perfectly, are still
  harm on shelves already converted.
* **Lens swap.** The naive population is every outlet over the past twelve months; the answer's is the outlets a reduced pack has not
  reached, over the twelve months ahead, a different set of outlets at a different time.

## 3. The driving force

A strong solver sets aside per-unit price inflation (most of toiletries' rise is list prices on unchanged packs), finds every reduced line
by grouping barcodes on the register's line code rather than on the optional successor field, and measures each category's detriment over
the past twelve months outlet by outlet. Cereals lead at $3.6 million. Every step is correct, and the result is a record of harm done.
Back-tested against the revision log, it reproduces none of the eight evaluated outcomes: the two investigations opened after their
reductions were on every shelf prevented almost nothing, and the cases opened early in a roll-out prevented more than their opening
estimates. What reproduces all eight is each line's detriment at the outlets that had not yet sold its reduced barcode at opening, at those
outlets' own volume, over the full twelve months. That needs each outlet's first sale of each line's reduced barcode, which only the
line-code grouping can see. Cereals' seven complete lines have nothing left to stop. Confectionery's seven undeclared lines converted the
northern region in November, 38% of their volume, and the other three regions not yet.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Change in average price per kilogram or litre over the past twelve months × each category's household spend ($k): A 4,100, B 3,400, C 2,900, D 2,600, E 2,200 | A, toiletries | The ready-made measure of paying more per gram | The product register: A's per-unit rise is list-price increases on unchanged packs; one A line changed size |
| 1 | Detriment over the past twelve months on reduced lines linked through the register's declared successor barcodes, outlet by outlet: B 1,900, D 1,500, C 1,200, E 700, A 300 | B, soft drinks | The register's own link from each barcode to its replacement, applied as the authority's detriment method describes | The register's line codes: the successor field is optional, blank for 7 of E's 11 reduced lines and 5 of C's 8, and the line code ties every reduced barcode to the one it replaced; the confectionery trade body's return counts 11 reduced lines |
| 2 | The same with every reduced line found by line code: C 3,600, E 2,900, D 2,000, B 1,900, A 300 | C, breakfast cereals | Every reduced line followed across its barcode change, outlet by outlet: the authority's standard estimate, built exactly | The revision log: the past basis reproduces none of the eight evaluated outcomes, and the two investigations opened after their reductions were on every shelf prevented under 5% of their opening estimates |
| 3 | **Decisive:** each line's detriment over the twelve months after opening at the outlets that had not sold its reduced barcode by 30 September, at each outlet's own trailing volume: E 4,400, D 1,300, B 900, C 400, A 200 | **E, confectionery** (5th of 5 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0, 4th on rung 1 and 2nd on rung 2 (C leads it by 1.24×), and leads only rung 3. Rung leaders beat
  their runners-up by 1.21×, 1.27×, 1.24× and 3.4×.
* **Discriminator dominance.** C carries a 1.24× advantage into rung 3, so the required edge is 1.2 × 1.24 = 1.49×. E's preventable
  detriment is 1.52 times its past detriment and C's is 0.11 times, an edge of 13.6×, 9.2 times the requirement, and the net is 13.6 / 1.24
  = 11.0×.
* **Partial correction priced (L3).** A solver who goes forward but counts every outlet's next twelve months, converted or not, names C,
  $10.3 million against E's $8.3 million (1.25×). A solver who takes the outlets still to convert from the manufacturers' announced
  schedules books snacks' second wave, announced for November and in fact converted in July, and only the one confectionery region the
  manufacturer has announced, and names D, $2.6 million against E's $2.1 million (1.22×). A solver who reads conversion from the chains'
  listing files, where a chain lists a line nationally once any of its regions sells it, names D at $1.3 million against B's $0.9 million
  (1.43×), with E at $0.5 million. Each lands on a wrong category.
* **Grid.** Line grouping (declared successor or line code) × basis (past twelve months; forward at every outlet; forward by announced
  schedule; forward by chain listing; forward by outlet first sale) = 10 cells. Declared-successor cells name B on the past and D on every
  forward basis, because E's four declared lines are already on every shelf. Line-code cells name C on the past and at every outlet, D on
  the schedule and the listing, and E only by outlet first sale. The nearest wrong cell is the schedule basis, which keeps E second at
  1.22×.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The framework says an investigation is valued at the detriment it prevents; no document says what an investigation
   can stop, and the revision log records each case's figures, not its undertakings' terms.
2. **The revision log pins a construction, not a menu (Pattern B).** The outlet-level forward construction reproduces all eight evaluated
   outcomes within 5%. The best rivals, the announced-schedule forward and the declared-successor forward, reproduce five each and miss one
   case by 45% and 60%; the chain-listing forward reproduces four; the every-outlet forward reproduces one, the case opened before any
   outlet had sold its reduced packs; the past basis reproduces none. The winner needs each outlet's first sale of each line's reduced
   barcode, grouped by line code and joined back to the outlet's own volume, which no category-level parameter supplies.
3. **No arithmetic symptom.** Scanner sales tie to the chains' totals, every barcode carries a line code and a net quantity, and every
   rung's past figure reproduces exactly from sales.
4. **Not a row predicate.** An outlet's status for a line is the minimum sale week of the line's reduced barcode at that outlet, a group
   over barcodes and weeks joined back to the outlet's trailing sales of the old pack.
5. **The enumeration is arithmetic.** The 1,560 outlets still to receive confectionery's seven reduced lines are computed; no field marks
   them.
6. **No cutover date.** The decisive quantity is a population that has not converted. The northern region's conversion in November sits in
   the past detriment every rung already counts, and nothing in the forward window steps on a date.
7. **Survives deletion.** Remove both voices and the spend table, and the outlet-level past estimate is still the natural build and still
   names C.

## 6. The calibration corpus

* **Form.** The revision log: eight closed pack-size investigations from 2019 to 2025, each with its category, opening date, opening
  estimate (detriment over the past twelve months), the detriment prevented as revised at the twelve-month evaluation, and the scanner
  extracts and register snapshots for the 52 weeks either side of opening.
* **What it pins.** The forward construction and its convention: remaining outlets counted for the full twelve months at their trailing
  52-week volume (above). A one-month run-out allowance misses five of the eight by 6–9%.
* **Twin pair.** PS-04 (2021) and PS-17 (2024), two snacks cases, are identical on every column of the log and the register: opening
  estimate $0.5 million, six reduced lines, a 9% per-unit rise, five chains and 2,300 outlets, and an announced schedule showing one wave
  still to come. Their evaluated outcomes are $600k and $300k, 2.0× apart: at opening 40% of PS-04's reduced-line volume sat at outlets that
  had not sold the reduced barcodes, against 20% of PS-17's. Only outlet first sales separate them.
* **Resemblance points at the decoy.** On category and opening estimate, cereals most resemble PS-09, the log's largest evaluated outcome, a
  cereal case opened when its reductions had reached a fifth of outlets.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The prioritisation framework: an investigation is valued at the consumer detriment it prevents over the twelve months
  after it opens, by a method that reproduces every evaluated outcome in the revision log within 5%. The register's field guide: every
  barcode carries a line code and a net quantity, and the successor field is optional. The data agreement: scanner sales cover every outlet
  of the five chains. One sentence each.
* **Empirical pins.** The full-twelve-month convention and outlet-level status, from the log; each line's per-unit rise, from the register's
  net quantities.
* **Voices.** The head of markets: "Shoppers feel it most in toiletries; that is where we should be." The chief economist: "Cereals are the
  worst shrinkflation this country has seen; every box got smaller."
* **Licensed wrong basis.** The framework records that the ministry's consumer-policy unit ranks categories by detriment over the past
  twelve months and will bring its ranking to the planning meeting.

## 8. Determinism by construction

* **Status date.** Scanner sales run to 30 September and the investigation opens on 1 October. No outlet sold both a line's old and reduced
  packs in the same week, so first-sale and last-old-sale dates give the same status.
* **Horizon convention.** Remaining outlets count for the full twelve months at their trailing 52-week volume of the old pack, the only
  convention that reproduces all eight evaluations; seasonal lines are covered by the full 52 weeks.
* **Lines.** Each barcode carries one line code, and each reduced line holds exactly one old and one reduced barcode.
* **Per-unit rise.** Net quantities come from the register, and every reduced line kept its shelf price at every outlet at conversion
  (confectionery 100 g to 92 g, a rise of 8.7%).
* **Rounding.** E's figure is $4,402k, which rounds to $4.4 million with 48 to spare on either side.

## 9. Prompt sketch and deliverables

> We open one pack-size investigation next quarter, and five categories are on the shortlist. Our head of markets says shoppers feel it most
> in toiletries. Tell me which category we take and how much consumer detriment it should prevent over the twelve months after it opens, to
> the nearest $100,000, in a line for the planning meeting. Send `pack_case.xlsx`, a chart `rollout_by_outlet.png`, and a one-page
> `investigation_note.pdf`.

* `pack_case.xlsx` — the five categories under each rung's basis (ask C), the complaints sheet (ask A) and the shelf-label sheet (ask B).
* `rollout_by_outlet.png` — for each category, the share of reduced-line volume at converted and unconverted outlets as stacked bars, the
  past and the preventable detriment as paired bars, the eight closed cases' evaluated against reproduced outcomes as a scatter with the 5%
  band, and the chosen category highlighted.
* `investigation_note.pdf` — the committed category and figure, and why each other category falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each category, pack-size complaints received in the past twelve months and the share escalated
  to a second review. *Device:* an escalated complaint is re-filed under its number with a tier suffix (C-20417-T2), and the complaints
  guide counts one complaint per base number; counting rows inflates three categories. The decision never reads complaints.
* **Ask B (device-carried).** For each category, the share of last year's shelf-label spot checks whose displayed unit price was correct.
  *Device:* labels show unit prices per 100 g, except multipacks, which the unit-pricing order lets show per item; checking every label
  against a per-100 g price fails every multipack. Spot checks never touch scanner sales or the register.
* **Ask C (validity).** Each category's figure under each of the four rung bases.
* **Decoupling.** Clearing the line-code grouping and the outlet-level forward population changes no figure in asks A or B.

## 11. Rubric arithmetic

5 categories × 2 (ask A) + 5 × 2 (ask B) + 5 × 4 bases (ask C) + the committed category, its preventable detriment, the runner-up and the
margin + 5 named chart parts + 3 files ≈ 52 criteria.

## 12. World-building constraints

* Rung figures as in the ladder; E is 5th, 4th, 2nd (1.24× behind C) and 1st (3.4× ahead of D). The every-outlet forward gives C $10.3
  million and E $8.3 million; the schedule forward D $2.6 million and E $2.1 million; the listing forward D $1.3 million, B $0.9 million and
  E $0.5 million. Declared-successor forward cells give E nothing.
* E: 11 reduced lines at 100 g to 92 g. Four declared lines launched nationally in January and have been on every shelf since February
  (full-conversion detriment $1.17 million a year). Seven undeclared lines converted the northern region in November, 38% of their volume
  and 840 outlets, and no other outlet since (full-conversion detriment $7.1 million a year). The manufacturer has announced the next
  region, 30% of the seven lines' volume, for the new year. Every chain but one discounter (7% of that volume) lists the seven lines
  nationally.
* C: seven lines on every shelf since May (three declared, carrying a third of C's past detriment; $9.3 million a year at full conversion);
  an eighth, undeclared, launched in August and sold at outlets holding 60% of its volume ($1.0 million a year).
* D: five declared lines converted chain by chain through distribution centres, two chains in February and a third in July, 72% of volume;
  the schedule still shows the third chain for November and the last two for spring. A sixth, undeclared line is on every shelf.
* B: every line declared, 75% of volume converted, schedule accurate. A: one declared line.
* 2,400 outlets in five chains. The revision log's eight cases reproduce as in section 5, and PS-04 and PS-17 are identical on every column.
* Complaints and shelf-label checks never touch scanner sales, the register or the log.