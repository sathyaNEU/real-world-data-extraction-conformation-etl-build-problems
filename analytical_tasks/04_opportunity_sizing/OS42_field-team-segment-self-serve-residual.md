# OS42 — Which segment gets next year's field sales team, when many of the owners there already upgrade by card on their own

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · B2B go-to-market and sales capacity |
| Mirrors | Placing scarce sales capacity where it adds accounts rather than relabelling self-serve sign-ups (product-led software companies assigning account executives to segments whose users already upgrade by card, merchant-success teams at commerce platforms, cloud start-up programmes whose credits go to firms that would have signed up anyway) |
| Decision shape | Which of N gets one scarce thing, with the sizing graded: the eight-rep field team works one segment next year |
| Committed call | The segment that gets the field team, and the new annual contract value it adds next year, in dollars to the nearest $10,000 |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · E09 (a residual population between two correct records: self-serve upgrades are billing's new paying accounts less the CRM's closed-won bookings, and a field team absorbs 80% of them), with E17 below it (a field win rate validated on launch segments at 27% incumbency, applied to segments from 10% to 85%) |
| Gate G mechanism | decomposition_attribution, with forecasting |
| Measured traps engaged | #25 assumes an effect the log could measure · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Change-log natural experiments: the sales-operations change log of four field launches (2021–2024), with monthly closed-won bookings and billing's new paying accounts for twelve months before and after each |
| Driving force | A field team in a segment whose owners already upgrade by card mostly signs firms that would have paid anyway. Those upgrades sit in no stream: billing has no channel field and the CRM records only sales-assisted wins, so they exist as billing's new accounts less closed-won bookings, an exact residual. In all four logged launches that residual fell by 80% once the team arrived. Fitness studios produce 450 self-serve upgrades a year and landscaping contractors 15, so a fitness team adds 341 accounts, not 701, and a landscaping team adds 560. |

## 1. Situation

A scheduling-software company sells to service businesses at $400 per location a month. Small firms mostly find it themselves, start on
the free plan and upgrade by card. Next year an eight-rep field team will work one segment of firms with 10 to 99 employees, and the
company's sales-capacity policy places the team where it adds the most new annual contract value. The sales-operations change log records
four earlier field launches. The chief revenue officer is sure restaurants, the largest market in the country, are where a field team
belongs.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the census counts, the adoption survey, the CRM, billing and the change log. The chief revenue
  officer is right that restaurants are the largest market, and every launch really did win 5.0% of its prospects. Nothing reported is
  overturned. The difficulty is what a field win adds, which depends on firms that would have paid without one.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chief revenue officer's view and every voice. Field wins by segment, built from the change log's own win
  rates, still name fitness studios, and no document mentions self-serve upgrades.
* **Instrument repair.** Suspect file: billing, which carries no channel field. Repaired, self-serve upgrades become a column, but rungs 0,
  1 and 2 size field wins only and still name restaurants, home health and fitness. What a team adds is still its wins less the 80% of
  self-serve upgrades it absorbs, which only the change log measures, so the netting is still needed for landscaping.
* **Lens swap.** The answer counts firms whose paying depends on the team, a counterfactual population, not the field wins under another
  lens.

## 3. The driving force

A strong solver sizes each segment's prospects from census firm counts, removes existing customers and open opportunities, and refuses the
change log's pooled 5.0% win rate. Every launch segment had 27% of firms on a competitor's system, and the closed deals convert at 6.5%
without one and 1.0% against one, so it calibrates by each segment's incumbency from the adoption survey. That build names fitness studios.
The policy's verb is "adds". Fitness owners upgrade by card in large numbers, 450 firms a year in the band, and a field team calling on the
same firms signs most of them first. They are invisible: billing records every new paying account without a channel, and the CRM records
only the wins a rep closed. Their count is billing's new accounts less closed-won bookings, month by month. In each of the four launches
that residual fell by 80% of its pre-launch level, while field wins appeared in the CRM. A team adds its wins less 0.8 of the segment's
self-serve upgrades.

## 4. The ladder

| Rung | Construction (field-sold accounts next year) | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Census firms with 10 to 99 employees × the change log's pooled field win rate (5.0%) | A, Restaurants, 2,000 (2.50× Dental) | The company's own measured win rate on the full market | The adoption survey puts competitor incumbency at 10% to 85% by segment against 27% in every launch segment, and the launches' closed deals convert at 6.5% without an incumbent and 1.0% against one |
| 1 | Win rate by incumbent status, weighted by each segment's incumbency | B, Home health, 862.8 (1.17× Fitness) | The launches' rate transported correctly to segments that differ on one axis | The CRM: 40% of home health firms in the band are already customers or in open opportunities |
| 2 | Hygiene: existing customers and open opportunities removed from prospects | C, Fitness, 700.9 (1.20× Restaurants) | Clean prospects, calibrated rates, a complete field-bookings case | The change log: after each launch, billing's new accounts outside closed-won bookings fell by 80% of their pre-launch level |
| 3 | **Decisive:** field wins less 0.8 × the segment's self-serve upgrades (billing's new accounts less closed-won bookings) | **E, Landscaping, 560.0 (1.33× Home health)** (5th of 6 on rung 0) | — | — |

* **The answer.** Landscaping contractors. The team adds 560.0 accounts, or $2,688,192 of annual contract value, committed as $2,690,000.
* **Position table.** Landscaping ranks 5th on rung 0, 4th on rung 1 and 3rd on rung 2, and leads only rung 3. It is never 2nd. Rung
  leaders beat their runners-up by 2.50×, 1.17×, 1.20× and 1.33×.
* **Discriminator dominance.** Fitness carries a 1.23× lead into rung 3 (700.9 against 572.0). Fitness keeps 0.486 of its field wins as
  added accounts and landscaping 0.979, an edge of 2.01×, which is 1.37 times the required 1.2 × 1.23 = 1.47.
* **Partial correction priced (L3).** Every half-built netting keeps fitness first. Applying the change log's pooled cannibalisation (30%
  of field wins) to every segment gives fitness 490.6 against restaurants' 408.8 (1.20×), with landscaping 3rd. Netting the company-wide
  self-serve rate per firm (1.27%) instead of each segment's own residual gives fitness 568.5 against landscaping's 465.2 (1.22×).
* **Grid.** Win rate (pooled, by incumbency) × hygiene (off, on) × self-serve netting (none, segment residual) = 8 cells. Every non-answer
  cell names restaurants, home health or fitness. The nearest is the residual netting without hygiene, home health at 766.8 against
  landscaping's 583.9 (1.31×), reached by counting the segment's existing customers as prospects.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The capacity policy says "adds". No document mentions self-serve upgrades or what a field team does to them, and
   billing carries no channel field.
2. **Corpus pins it only as a residual.** *In each launch the CRM shows the field wins and billing shows new paying accounts, and the
   self-serve drop exists only as the difference between the two files before and after the launch.* Either file alone confirms rung 2:
   field wins match 5.0% of prospects in all four launches.
3. **No arithmetic symptom.** Every closed-won booking creates exactly one billing account in its month, so the two files reconcile on
   sales-assisted accounts, and billing ties to revenue.
4. **Not a row predicate.** Self-serve upgrades are a monthly residual by segment, and the team's effect on them is a before-and-after
   difference of that residual.
5. **The enumeration is arithmetic.** No column says self-serve, and no record says a field win would have happened anyway.
6. **No cutover date.** The launches are how the log measures the 80%. The forward decision turns on each segment's standing self-serve
   flow, flat for eight quarters, and no forward series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** Four field launches (salons 2021, auto repair 2022, physiotherapy 2023, childcare 2024), each with twelve months before and
  after of closed-won bookings from the CRM and new paying accounts from billing, by segment and month.
* **What it certifies.** The win rate: each launch won 5.0% of its prospects at 27% incumbency, and its closed deals convert at 6.5% and
  1.0% by incumbent status. A solver who back-tests rungs 0 to 2 against field wins is confirmed in all four.
* **What it pins.** The self-serve residual fell by 80% after every launch (0.78 to 0.82), and the field team's added accounts are its wins
  less that drop. Across the four launches the drop was 536 accounts against 1,770 wins, the pooled 30%.
* **Twin pair.** Physiotherapy and auto repair are identical on every column a lookup reaches: prospects (8,400), incumbency (27%),
  existing-customer share and field wins (420 each). New paying accounts rose by 204 and 412, 2.02× apart, because physiotherapy owners had
  been upgrading on their own at 270 a year and auto-repair owners at 10.
* **Resemblance points at the decoy.** By owner profile, appointment booking and card payment, fitness studios resemble the childcare
  launch, which booked the most field wins of the four.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The sales-capacity policy places the field team where it adds the most new annual contract value next year, among firms
  with 10 to 99 employees. Existing customers and open opportunities are not prospects. Price is $400 per location a month, and firms in
  the band hold one location.
* **Empirical pins.** Win rates by incumbent status from the launches' closed deals; incumbency by segment from the adoption survey; the
  80% from the change log; each segment's self-serve flow from billing less the CRM.
* **Voices.** The chief revenue officer: "Restaurants are the biggest market in the country; that's where a field team belongs." The vice
  president of sales: "Our field team has won five per cent in every launch." That is true.
* **Licensed wrong basis.** The policy records that the board's go-to-market committee reviews placements on projected field bookings and
  will see that basis.

## 8. Determinism by construction

* **Residual exactness.** Every closed-won booking opens one billing account in the same month, and no account is created by migration or
  merger, so the residual is exact.
* **Stability.** Each segment's self-serve residual has been within 3% of its level for eight quarters, so any window from four to eight
  quarters gives the same flow.
* **The 80%.** The four launches give 0.78 to 0.82, and no value in that range changes the ranking.
* **Incumbency.** The adoption survey is one filed wave, and incumbency is recorded per firm in the CRM's deal records.
* **Rounding.** $2,688,192 sits $3,192 from the nearest rounding boundary. Every launch's after-window is complete.

## 9. Prompt sketch and deliverables

> Next year's field team, eight reps, goes into one segment, and our chief revenue officer is convinced restaurants are where a field team
> belongs. Tell me which segment gets the team and the new annual contract value it should add, to the nearest $10,000, in a sentence for
> the go-to-market committee. Send `field_segment_case.xlsx`, a chart `segment_increment.png`, and a one-page `gtm_committee_note.pdf`.

* `field_segment_case.xlsx`: the six segments under the four rung bases, the four launches' before-and-after build, the support sheet (ask
  A) and the mobile sheet (ask B).
* `segment_increment.png`: for each segment, projected field wins and the self-serve upgrades the team would absorb as paired bars, the
  added accounts marked as a dot, segments sorted by added accounts, the chosen segment highlighted and each segment's incumbency printed.
* `gtm_committee_note.pdf`: the committed segment, the contract value it adds and why fitness studios are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each segment, last year's average monthly support tickets per paying account and the share
  escalated to engineering. *Device:* a merged ticket keeps both IDs with a merge pointer, and one ticket is the surviving ID, per the
  helpdesk guide. Counting rows overstates tickets by 15% in the three segments with phone support.
* **Ask B (device-carried).** For each segment, the share of paying accounts that used the mobile app in at least three weeks of each month,
  for each of the last four quarters. *Device:* the event export carries one row per user per device, and activity is counted per account
  per week, per the analytics guide. Counting device rows overstates the share in segments where managers carry two devices.
* **Ask C (validity).** Each segment's added accounts under each of the four rung bases, and for each launch the effect as field wins and
  as billing's change in new paying accounts (4 × 2).
* **Decoupling.** Clearing the self-serve netting changes no figure in asks A or B, and neither touches bookings or new-account counts.

## 11. Rubric arithmetic

6 segments × 2 (ask A) + 6 × 4 quarters (ask B) + 6 × 4 bases + 8 launch figures (ask C) + the committed segment, its contract value and its
margin + 5 named chart parts + 3 files ≈ 79 criteria.

## 12. World-building constraints

* Segments (firms with 10 to 99 employees / incumbency / existing or open share / self-serve upgrades a year): Restaurants 40,000 / 0.85 /
  0.20 / 600, Home health 14,500 / 0.10 / 0.40 / 120, Fitness 13,000 / 0.15 / 0.05 / 450, Dental 16,000 / 0.60 / 0.12 / 60, Landscaping
  10,500 / 0.15 / 0.04 / 15, Veterinary 7,000 / 0.45 / 0.08 / 40.
* Win rates 6.5% without an incumbent and 1.0% against one; 5.0% pooled at 27% incumbency. The team absorbs 0.80 of self-serve upgrades.
* Launches (prospects / field wins / self-serve before): salons 9,000 / 450 / 360, auto repair 8,400 / 420 / 10, physiotherapy 8,400 / 420
  / 270, childcare 9,600 / 480 / 30.
* Rung leaders restaurants, home health, fitness and landscaping with margins of 2.50×, 1.17×, 1.20× and 1.33×; half-built nettings name
  fitness (1.20× and 1.22×); all eight grid cells name as stated.
* Ticket merges and device rows never touch bookings, billing accounts or the census counts.
