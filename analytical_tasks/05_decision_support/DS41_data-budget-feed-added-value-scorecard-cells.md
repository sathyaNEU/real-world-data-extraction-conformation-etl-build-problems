# DS41 — Which application segments get a new repayment-history feed under a $2.4M data budget, when a source is worth only what it adds

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · consumer credit data procurement |
| Mirrors | Buying data or features judged on what they add to sources already in production (alternative data at card issuers, enrichment vendors for ad targeting at Meta and Google, third-party signals bought for marketplace risk and fraud models) |
| Decision shape | An allocation under a cap: the $2.4M data budget, buying the feed at $1.80 a pull for whole application segments |
| Committed call | The segments that get the feed, and next year's net profit uplift from the purchase, in $ millions to two decimals |
| Gap · Pattern | Gap 4 (rule) over Gap 3 (objective) · E16, finer controls separate constructions (the scorecard's segment cells reproduce only the value a source adds to the sources already deciding), with a subgroup recalibration (E17) at rung 1 |
| Gate G mechanism | method_or_model_selection, with binding_constraint |
| Measured traps engaged | #12 stops at the first control that passes · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Published control set with a reproduction clause: the latest decision-value scorecard for the three sources in production, by segment, which the purchase policy makes the test of any value method |
| Driving force | A data source is worth what it adds to the sources already making the decision. The feed's value standing alone is largest in thick-file segments, where the bureau already carries most of the same information. The scorecard ranks the three production sources the same way under standalone or added value, so the obvious check passes either; only its 18 segment cells, all reproduced by added value and 7 by standalone, tell them apart. |

## 1. Situation

A card issuer decides applications with three data sources in production: a bureau score, bank-transaction data and telco payment data. A
vendor offers a repayment-history feed at $1.80 a pull. The data-purchase policy gives new data $2.4 million next year, buys a source for
whole application segments in order of net decision value per pull until the budget is spent, and lets a value method be used only if it
reproduces every figure in the latest decision-value scorecard. Six segments will see 2.6 million applications. The data-science lead
points to the feed's AUC lift.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the AUCs, the holdout outcomes, the scorecard, the application forecast and the partner's customer
  profile. No stakeholder read is overturned: the feed does lift AUC most, and it does predict repayment well on its own. The difficulty is
  the value it adds to decisions already informed by three sources.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the AUC case and every voice. The feed's decision value measured on top of the base model still funds the
  branch thick-file segment.
* **Instrument repair.** No file the ladder uses is suspect: the holdout outcomes, the scorecard, the application forecast and the partner's
  profile are complete. Perfect repayment outcomes leave rung 0 on the AUC case, rung 1 on branch thick, online thin and branch thin, and
  rung 2 on partner, branch thick and online thin: the feed's standalone value becomes exact and still overstates what it adds to the other
  sources, so the added-value construction is still needed.
* **Lens swap.** The naive read and the answer differ in population: decisions made on the base model alone, against decisions already
  made with three sources, where only the applicants the feed moves count.

## 3. The driving force

A strong solver drops AUC, values the feed in decisions (approve where expected profit is positive, realised profit on the holdout),
recalibrates the new partner segment to next year's applicant profile, and funds segments by net value per pull. It values the feed against
the base model, because that is how the vendor's case and the obvious test are set up, and it checks its method against the scorecard,
which ranks bureau over transactions over telco. Its method reproduces that ranking. But the policy's test is every figure, and the
scorecard holds 18 segment cells. Measuring each production source on top of the base model reproduces 7 of them, every miss too high. Only
measuring each source as the value it adds to the other two, re-deciding the holdout with and without it, reproduces all 18. Under that
construction the feed adds little in thick-file segments, where the bureau and the transaction data between them already carry repayment
behaviour, and most where applicants have no bureau file at all.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The data-science case: AUC lift by segment, weighted by volume | Online thick and co-brand thick; case value $5.40M | The model team's own evidence, and a large lift | The purchase policy: sources are funded by net decision value per pull, not by model fit |
| 1 | Decision value of base model plus feed against base model, on last year's holdout mix, net of $1.80 | Branch thick, online thin, branch thin; $2.40M | Value in decisions, with realised outcomes, as the policy asks | The partner's published customer profile: next year's partner applicants are 70% new to the country, against 15% in last year's book |
| 2 | The same, recalibrated by file depth to next year's mix | Partner, branch thick, online thin; $2.93M | Forward mix, measured value, and the scorecard's ranking reproduced | The scorecard's 18 segment cells: base-plus-source value reproduces 7, every miss high |
| 3 | **Decisive:** the value the feed adds to the three production sources, the construction that reproduces all 18 cells, on next year's mix | **Partner, online thin, branch thin: $1.96M** | — | — |

* **Figure shape.** The answer is the minimum cell; every other construction credits the feed with value the bureau already supplies.
  Offsets: $5.40M (+176%), $2.40M (+22%), $2.93M (+49%).
* **Position table.** Branch thin, the segment that enters only at rung 3, is 5th of six on rung 0, 3rd funded on rung 1 and unfunded on
  rung 2. Branch thick, funded at rungs 1 and 2, leaves.
* **Discriminator dominance.** Branch thick carries a 1.18× net-value advantage over branch thin into rung 3 ($2.30 against $1.95 a pull).
  Measured as added value, branch thin is worth $1.60 and branch thick $0.40: branch thin keeps 0.82 of its value and branch thick 0.17,
  an edge of 4.7×, against the required 1.2 × 1.18 = 1.42 and well past the 1.84 that headroom asks.
* **Partial correction priced (L3).** No half-applied construction funds the answer's three. A solver who measures added value but keeps
  last year's partner mix, 15% new to the country, finds the partner worth $0.25 a pull and funds online thin, branch thin and branch
  thick for $1.19M (−39%): branch thick's $0.40 leads the partner by 1.6×. One who measures the feed's value added to the bureau alone,
  ignoring the transaction and telco sources, funds partner, branch thick and online thin for $2.74M (+40%), with branch thick at $2.10 a
  pull, 1.31× over branch thin.
* **Grid.** Value (AUC, standalone, added to bureau only, added to all three) × mix (last year, next year) = 8 cells. Only added-to-all on
  next year's mix funds partner, online thin and branch thin, for $1.96M; the nearest other figure is $2.15M (+10%), added to the bureau
  alone on last year's mix, which funds branch thick, online thin and branch thin.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy states the reproduction test; the scorecard prints its figures. No document says how a source's value
   is measured, or that it is measured against the other sources.
2. **The finer controls pin it, as a construction.** Added value reproduces 18 of 18 cells and all three source totals. Standalone value
   reproduces the ranking (the salient check) and 7 cells, overstating the totals by 31%. The construction re-decides the holdout with every
   production source and again with each removed, so the value depends on the whole set of sources, not on a setting.
3. **No arithmetic symptom.** Holdout outcomes, decisions, approvals and the scorecard's totals reconcile, and the obvious construction
   passes the check a solver writes first.
4. **Not a row predicate.** Added value needs two full decision passes per source over the holdout, realised profit on the applicants whose
   decision changes, and then a transport of per-applicant value by file depth.
5. **The enumeration is arithmetic.** No column says which applicants a source moves.
6. **No cutover date.** The partner mix is a forward profile; nothing in the holdout steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the base-plus-feed method still passes the ranking.

## 6. The calibration corpus

* **Form.** The latest decision-value scorecard: each production source's net decision value per pull in each of six segments (18 cells),
  three source totals and their ranking, with the holdout it was computed on.
* **What it pins.** The added-value construction (above), and the holdout, decision rule and economics it uses.
* **Twin pair.** The transaction source's cells in branch thick and online thick are identical on every column the scorecard and holdout
  show: applications, approval rate, default rate, the source's coverage and its standalone value of $1.10 a pull. Their published values
  are $0.62 and $0.31 (2.0×): in online thick the bureau already carries most of what transactions add. Only the added-value construction
  separates them.
* **Resemblance points at the decoy.** By approval rate and default rate, the partner segment's next-year profile most resembles the
  co-brand thick segment, where every source adds little.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The purchase policy: $2.4M for new data next year; a source is bought for whole segments, in order of net decision value
  per pull, until the budget is spent; a value method may be used only if it reproduces every figure in the latest scorecard. The risk memo:
  approve where expected profit is positive, at the filed margin, loss given default and exposure. The vendor quote: $1.80 a pull. The
  application forecast by segment.
* **Empirical pins.** The construction, from the scorecard. File depth for the partner segment, from the partner's published profile.
* **Voices.** The data-science lead: "The feed lifts AUC more than any source we have tested." The head of acquisition: "Thick-file customers
  are where our volume and margin are." The partnerships manager: "The new partner's customers look like our co-brand book."
* **Licensed wrong basis.** The policy records that the vendor will present the feed's uplift over the base model at the procurement
  review.

## 8. Determinism by construction

* **Models.** Model specification, seeds and calibration are filed, and the scorecard reproduces to the cent only under them; implementation
  differences move no segment's value by more than $0.03 a pull, against a smallest funding margin of $1.20 (branch thin over branch
  thick).
* **Budget.** Whole segments: the three funded segments use 990,000 pulls ($1.78M); the next segment would need 520,000 more, so no
  ordering convention changes the set.
* **File depth.** Next year's partner mix is the profile's 70% new to the country; the other segments keep last year's mix, which the
  forecast confirms.
* **Rounding.** $1.96M is mid-bin at two decimals.

## 9. Prompt sketch and deliverables

> We have $2.4 million next year for new data, and a repayment-history feed is on offer at $1.80 a pull. Our data-science lead says it
> lifts AUC more than anything we've tested. Tell me which application segments we buy it for and the net profit uplift it buys us next
> year, in $ millions to two decimals, as the line for the procurement paper. Send `data_allocation.xlsx`, a chart
> `added_value_by_segment.png`, and a one-page `procurement_paper.docx`.

* `data_allocation.xlsx` — the six segments' net value per pull under each rung construction with the scorecard reproduction counts (ask C),
  the activation sheet (ask A) and the bureau-cost sheet (ask B).
* `added_value_by_segment.png` — for each segment, the feed's standalone and added value per pull as paired bars, ordered, with the $1.80
  price line, the budget cut marked, and the twin cells annotated in an inset.
* `procurement_paper.docx` — the committed segments and uplift, and why the thick-file segments are not bought.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six segments, median days from approval to first purchase on last year's new
  accounts. *Device:* the first posted transaction is often the card fee or a balance transfer, which carry their own transaction codes,
  as the transaction guide documents. Taking the first posting understates the median in every segment, most where balance transfers are
  common.
* **Ask B (device-carried).** For each month of last year, the bureau's billed cost per application. *Device:* the bureau bills one pull
  per applicant per 30 days, and repeat pulls inside the window appear in the pull log without a charge, as its billing terms set out.
  Pricing every logged pull overstates the cost in the online segments, where re-applications cluster.
* **Ask C (validity).** Each segment's net value per pull under the four rung constructions, and the scorecard hit count (of 18) for the
  standalone and added-value constructions.
* **Decoupling.** Clearing the added-value construction changes no figure in asks A or B. Transaction postings and the bureau's billing
  touch no holdout decision or scorecard record.

## 11. Rubric arithmetic

6 segments (ask A) + 12 months (ask B) + 6 segments × 4 constructions + 2 hit counts (ask C) + the three funded segments, the uplift, the
pulls used and the margin to the next segment + 5 named chart parts + 3 files ≈ 70 criteria.

## 12. World-building constraints

* Next-year volumes (thousands): branch thick 520, branch thin 260, online thick 610, online thin 330, co-brand thick 480, partner 400.
* Net value per pull. Standalone, last year's mix: branch thick 2.30, online thin 2.10, branch thin 1.95, online thick 1.40, partner 0.90,
  co-brand 0.60. Standalone, next year's mix: partner 2.60, others unchanged. Added value, next year's mix: partner 2.45, online thin 1.70,
  branch thin 1.60, branch thick 0.40, online thick 0.30, co-brand 0.10; on last year's mix the partner falls to 0.25. Added to the bureau
  alone, next year's mix: partner 2.50, branch thick 2.10, online thin 1.95, branch thin 1.60; on last year's mix the partner falls to
  0.45.
* Scorecard: 18 cells; 18 reproduced by added value, 7 by standalone; the twin cells match on every column.
* Postings and bureau billing are independent of every main-call record.
