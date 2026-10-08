# OS47 — What an overdraft fee cap puts at risk, when the banks' own announced changes take most of the money first

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · banking regulation and consumer finance |
| Mirrors | Attributing revenue at risk to a rule when the firms are already changing on their own (app-store commission rules assessed against the stores' announced fee cuts, interchange caps against issuers' own pricing moves, roaming rules against carriers' price changes already in train) |
| Decision shape | One figure committed at a date: the revenue-at-risk figure in the association's comment letter, filed on the 14th |
| Committed call | The overdraft revenue the rule puts at risk for covered banks in its first full year, to the nearest $10 million, set against what the banks' own announced changes take |
| Gap · Pattern | Gap 3 (objective) over Gap 1 (time) · E22 (the deciding comparison: the rule's take measured from what banks will charge after their own announced fee cuts, de minimis thresholds and grace windows, against what those changes take first; read one at a time against last year's book, the rule looks like the larger driver), with E33 below it (coverage by the rule's four-quarter average of assets, not the call report's latest size class) |
| Gate G mechanism | decomposition_attribution, with forecasting |
| Measured traps engaged | #20 leaves the deciding comparison unstated · #5 takes the population a flag or filter suggests · #7 uses the ready-made measure |
| Calibration form | Prior-period close-out: the association's signed close-out of last year's overdraft changes at four member banks, item by item for twelve months before and after |
| Driving force | Covered banks will charge next year under fee cuts, de minimis thresholds and grace windows they have already announced, all in force before the rule. Read one at a time against last year's book, the rule takes $5.82B and the banks' own changes $4.73B, so the rule looks like the larger driver. Run in sequence, the banks' changes take $4.73B first and the rule takes $1.78B of what remains. The items a bank will still charge come from its own item-amount and cure-time distributions under its own terms, which the close-out shows are charged absolutely or not at all. |

## 1. Situation

A bankers' association is commenting on a proposed rule that caps the fee a covered bank may charge for an overdraft at $6. Its letter,
due on the 14th, must state what the rule puts at risk for covered banks in its first full year and how that compares with what the banks'
own changes take. The rule covers banks whose total assets average $10 billion or more over the four quarter-ends before it takes effect,
and seven banks qualify. Five of them announced overdraft changes last spring that take effect on 1 January, nine months before the rule.
The association's chair believes the rule will end overdraft as a business.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the call reports, the members' data call, the announced fee schedules and the close-out. The chair's
  belief is a view of the industry, and the rule does cut the fee per item hard. Nothing reported is overturned. The difficulty is that the
  rule acts on what banks will charge after their own changes, which last year's book does not show.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chair's view and every voice. The rule applied to last year's book still takes $5.82B, more than the banks'
  own changes take from the same book.
* **Instrument repair.** Suspect file: the call report's size class, which records each bank's latest quarter rather than the rule's
  four-quarter average. Repaired to the rule's test, rung 0 becomes rung 1 ($5.82B), and rungs 1 and 2 stay at $5.82B and $3.34B. The data
  call, the announced schedules and the close-out are complete. What each bank will still charge next year is a forward quantity built
  from them, so the sequence is still needed for $1.78B.
* **Lens swap.** The answer prices the items banks will still charge under their own new terms next year, a different population and moment
  from last year's items.

## 3. The driving force

A strong solver takes the rule's coverage test as written rather than the regulator's size class, and it measures the cap from the fees
banks will actually charge: Bayline has announced $10, Cedar $15, Fairview $20, and Dunmore will charge nothing. But the announcements also
set de minimis thresholds and grace windows. Under them an overdraft below the threshold, or cured within the window, is never charged.
The close-out of last year's changes at four member banks shows this held for every item, with no partial cases. Which items a covered
bank will still charge depends on its own overdrafts: Arbor's item-amount distribution puts 24% under its $25 threshold, and its cure times
put 45% of the rest inside its 24-hour window. So the rule's take is a sequence. The banks' changes cut last year's $7,062M to $2,327M, and
the cap cuts that to $547M. The rule takes $1,780M, against $4,735M taken by the banks themselves. Measured on last year's book, the rule
looks like the larger driver; measured in sequence, the banks' own changes are 2.7 times the rule's.

## 4. The ladder

| Rung | Construction (overdraft revenue the cap removes, first full year) | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Banks the call report's size class marks at $10B or more; last year's items × (last year's fee − $6) | $6,330M, +255.6% | The rule applied to the book that exists, on the regulator's own size data | The rule's coverage test averages assets over four quarter-ends: Granite averages $9.6B and Harborside $10.3B |
| 1 | Coverage by the four-quarter average (E33) | $5,820M, +227.0% | The rule's own population and its own fee, on audited activity | The announced schedules, effective 1 January: Bayline to $10, Cedar to $15, Fairview to $20, Dunmore to no fee |
| 2 | Announced fees on last year's items | $3,340M, +87.6% | The cap measured from the fees banks will actually charge | The close-out: no item under a bank's de minimis threshold or cured within its grace window was charged, at any of the four banks |
| 3 | **Decisive:** the cap's take from each bank's announced fee on the items it will still charge (its own amount and cure-time distributions under its own terms), set against what its announced changes take first | **$1,779.9M, committed as $1,780M** | — | — |

* **Figure shape.** Every correction walks the figure down (−8.1%, −42.6%, −46.7%), and the answer is the minimum cell of the grid.
* **The deciding comparison (#20).** The banks' own changes take $4,735M of last year's $7,062M, and the rule takes $1,780M of the $2,327M
  that remains. Read one at a time against last year's book, the rule takes $5,820M and the banks' changes $4,735M. The letter has to set
  the sequential figures side by side.
* **Partial correction priced (L3).** Applying the close-out's pooled removal (45% of items at any bank with a threshold or window) gives
  $1,999M (+12.3%). Netting grace windows but not thresholds gives $2,215M (+24.4%), and thresholds but not windows $2,683M (+50.7%). Each
  half stays at least 12% from the answer.
* **Grid.** Coverage (size class, four-quarter test) × fee (last year's, announced) × items (last year's, still chargeable) = 8 cells. The
  nearest is the full sequence on the size class, $2,290M (+28.7%), reached by counting Granite and dropping Harborside.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rule caps a fee, and the announcements describe fee schedules. No document puts them in sequence or says which
   items a bank will still charge.
2. **The corpus pins the parts, not the comparison.** *In every closed case of the close-out the banks changed their own terms with no rule
   in force, so it measures what thresholds and windows remove and never what a cap takes from what remains.* It reproduces each bank's
   charged items exactly, 4 of 4.
3. **No arithmetic symptom.** Items, fees and revenue reconcile to the call reports and the data call on every rung, and both one-at-a-time
   effects are correct numbers.
4. **Not a row predicate.** Each bank's chargeable items come from its own amount and cure-time distributions under its own terms, and the
   cap then applies to the fee those terms set.
5. **The enumeration is arithmetic.** No column holds next year's chargeable items or the rule's increment.
6. **No cutover date.** 1 January and the rule's effective date are dated decoys. The comparison is an order of two sets of terms, not a
   step in a series.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The signed close-out of last year's changes at four member banks (two adopted a $50 de minimis threshold, one a 24-hour grace
  window, one both), item by item for twelve months before and after: amount, cure time, whether charged, and fee.
* **What it certifies.** The charging rule, absolute at every bank: no item under the threshold or cured within the window was charged, and
  every other item was. Applied to each bank's own distributions it reproduces each bank's charged items and fee revenue after the change,
  4 of 4.
* **What it is blind to.** The cap (above).
* **Twin pair.** Millbrook and Ashford, both of which adopted a $50 threshold, are identical on every column a lookup reaches: 4.0M items a
  year, a $34 fee, assets and terms. Millbrook's charged items fell 70% and Ashford's 35%, leaving 1.2M against 2.6M (2.2×), because
  Millbrook's overdrafts are mostly card purchases under $50. Only each bank's own item-amount distribution separates them; the pooled
  45% gives both the same.
* **Resemblance points at the decoy.** By size and fee, the covered banks resemble the national banks in the regulator's impact analysis,
  which measures the cap on last year's book, so a solver following it files rung 1.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The rule caps the overdraft fee at $6 for banks whose total assets average $10 billion or more over the four quarter-ends
  before its effective date. The letter's figure is the rule's first full year, holding last year's overdraft activity. The announced
  schedules take effect on 1 January.
* **Empirical pins.** Each covered bank's item-amount and cure-time distributions, from the data call; the charging rule, from the
  close-out.
* **Voices.** The chair: "This rule ends overdraft as a business." The policy director: "The regulator's impact analysis is the number
  everyone will quote."
* **Licensed wrong basis.** The association's comment protocol records that the regulator's impact analysis measures the cap on last year's
  book, and that the regulator will read the letter on that basis.

## 8. Determinism by construction

* **Coverage.** No bank's four-quarter average lies within $0.2 billion of the $10 billion line.
* **Thresholds and windows.** The data call bands item amounts and cure times exactly at $25, $50 and 24 hours, so no item straddles a
  threshold.
* **Activity.** Last year's overdraft activity is held, by the letter's filed basis.
* **Fees at or below the cap.** Dunmore charges nothing and contributes zero under every reading.
* **Rounding.** $1,779.9M sits $4.9M from the nearest $10M rounding boundary.

## 9. Prompt sketch and deliverables

> The comment period on the overdraft rule closes on the 14th, and our letter has to say what the rule puts at risk for covered banks in
> its first full year, to the nearest $10 million, and how that compares with what the banks' own announced changes take. Our chair
> believes the rule ends overdraft as a business. Send `revenue_at_risk.xlsx`, a chart `rule_versus_banks.png`, and a one-page
> `comment_letter_insert.pdf`.

* `revenue_at_risk.xlsx`: the seven covered banks under the four rung bases, the sequence of announced terms and cap, the returned-item
  sheet (ask A) and the closed-account sheet (ask B).
* `rule_versus_banks.png`: for each covered bank, last year's overdraft revenue split into what its own changes take, what the rule takes
  and what remains, as stacked horizontal bars, the rule's one-at-a-time take marked as a dot, and the two sequential totals in the title.
* `comment_letter_insert.pdf`: the committed figure and the comparison.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each covered bank, last year's returned-item fee income and the number of returned items.
  *Device:* a re-presented item that is returned again posts as a new row carrying the original trace number, and one item is one trace
  number, per the deposit operations guide. Counting rows overstates returned items by 30% at the three banks that re-present twice.
* **Ask B (device-carried).** For each covered bank, the number of checking accounts closed with a negative balance last year and the
  median balance written off. *Device:* an account reopened within 30 days under the same number is one account, and its write-off is
  reversed by a recovery row, per the charge-off guide. Counting closure rows overstates closures at the two banks with reopen programmes.
* **Ask C (validity).** The figure under each of the four rung bases; the close-out reproduced under the absolute charging rule (4 of 4);
  and the four comparison figures (each driver one at a time and in sequence).
* **Decoupling.** Clearing the sequence changes no figure in asks A or B, and neither touches overdraft items or fees.

## 11. Rubric arithmetic

7 banks × 2 (ask A) + 7 × 2 (ask B) + 4 bases, 1 reproduction count and 4 comparison figures (ask C) + the committed figure and each bank's
rule take (8) + 5 named chart parts + 3 files ≈ 53 criteria.

## 12. World-building constraints

* Covered banks (items last year / fee / announced fee / threshold / window / items still chargeable): Arbor 60M / $35 / $35 / $25 / 24h /
  25.08M; Bayline 45M / $34 / $10 / $50 / 24h / 14.355M; Cedar 30M / $35 / $15 / $50 / none / 17.4M; Dunmore 25M / $32 / none / – / – /
  0; Eastgate 20M / $35 / $35 / none / 24h / 11.0M; Fairview 15M / $30 / $20 / $25 / none / 11.4M; Harborside 12M / $36 / $36 / none /
  none / 12M. Granite (size class $10B+, average $9.6B): 30M items at $35.
* Shares removed, from each bank's own distributions: Arbor 24% under $25 and 45% of the rest within 24 hours; Bayline 42% under $50 and 45%
  of the rest; Cedar 42% under $50; Eastgate 45% within 24 hours; Fairview 24% under $25.
* Rung figures $6,330M / $5,820M / $3,340M / $1,780M; partials $1,999M, $2,215M and $2,683M; nearest other grid cell $2,290M.
* Sequence: last year $7,062M, after the banks' changes $2,327M, after the cap $547M. Millbrook and Ashford are identical on every lookup
  column.
* Re-presented items and reopened accounts never touch overdraft items, fees or the data call's distributions.
