# FC49 — Which product line gets next quarter's extra vulnerability-triage analyst, when the backlog-corrected lead is smaller than the lead's own quarter-to-quarter swing

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Product Analytics · product security operations (network equipment) |
| Mirrors | Staffing vulnerability response from public CVE and NVD feeds (network vendors with bundled advisories, cloud platform security teams), where the backlog-corrected forecast is real but nowcast quarters carry none of the swing that actual quarters do |
| Decision shape | Which of N gets one scarce thing: the extra triage analyst for the first quarter, to one of five product lines, or held in the shared pool |
| Committed call | The product line that gets the analyst, or a hold, with the lead and the quarter-to-quarter standard deviation that decide it |
| Gap · Pattern | Gap 1 (time) over Gap 3 (objective) · hold forced by a computed blocking quantity (Part 6.4: a lead smaller than its own quarter-to-quarter swing), with two grains both flawless (Pattern D) at rung 2 |
| Gate G mechanism | signal_vs_noise_or_hold, with forecasting support |
| Measured traps engaged | #16 lets small shortcuts flip a thin margin · #2 counts file rows instead of the real unit · #7 uses the ready-made measure |
| Calibration form | Counterparty acknowledgement file: NVD's analysis acknowledgements for every CVE in the vendor's advisories since 2022, each with the date NVD analysed it and the score it gave |
| Driving force | The staffing policy assigns the analyst only when the leader's forecast lead exceeds the quarter-to-quarter standard deviation of that lead in the record. A strong solver builds that record by nowcasting the quarters NVD has not finished analysing, and a nowcast is an expectation: it carries none of the swing of real quarters, so the last eight quarters, half of them nowcast, show a deviation of 9 against routers' lead of 14. Shared-component CVEs reach routers and campus switches on different release trains, so in the eight most recent quarters NVD has fully acknowledged the lead swung with a deviation of 19. The lead sits inside one deviation: no line has earned the analyst. |

## 1. Situation

A network-equipment vendor's product-security team has one extra triage analyst for the first quarter. The staffing policy sends the
analyst to the product line with the most NVD-critical CVEs to triage next quarter, forecast as the mean of the last four quarters, and
only if that line's lead over the runner-up is larger than the lead's quarter-to-quarter standard deviation in the record; otherwise the
analyst stays in the shared pool. The triage standard counts one triage per CVE per affected product line. NVD's analysis backlog has
left many recent CVEs unscored. The pack holds the advisories with their affected-product lists, NVD's acknowledgement file, the security
dashboard, the release calendar and the policy. The staffing note is due on 10 December.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the advisories, NVD's acknowledgements and scores, the dashboard's counts of currently scored CVEs
  and the release calendar. No stakeholder's reading of their own numbers is overturned; routers really do face the most critical triages.
  The difficulty is whether the lead is larger than the record's own swing, which only actual quarters measure.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the finance partner's view and every voice. The backlog-corrected, pair-grain forecast still names routers by
  14, and the eight latest quarters still give a deviation of 9.
* **Instrument repair.** Imagine NVD with no backlog. The recent quarters would be actual counts and the swing would show; the difficulty
  survives in the forecast, because next quarter's counts will swing as much as any past quarter's, and a lead of 14 against a swing of 19
  is not a lead that holds.
* **Lens swap.** The naive read and the answer weigh different moments: a record whose recent half is smoothed expectations, against a
  record of quarters as they actually landed.

## 3. The driving force

A strong solver distrusts the dashboard, which counts only CVEs NVD has already scored, and nowcasts each recent quarter from NVD's
acknowledgements: how long analysis takes and what share of analysed CVEs is critical. It then reads the triage standard and moves from
CVEs to CVE–line pairs, because a shared kernel or crypto-library CVE is triaged on every line it affects. Routers lead campus switching by
14 critical triages, and the standard deviation of the router-minus-campus difference over the last eight quarters is 9, so the analyst
goes to routers. Every step is correct except the record the deviation was measured on. Four of those eight quarters are nowcasts:
expected values, filled in where NVD has not yet scored, and an expected value does not swing. In actual quarters it swings a great deal,
because kernel CVEs reach routers on a quarterly release train and campus switches on a half-yearly one. In the eight most recent quarters
NVD has fully acknowledged, the lead's deviation is 19. A lead of 14 is inside one deviation of its own swing, so the analyst stays in the
pool.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The dashboard's currently scored critical CVEs, last quarter carried forward; lead against the dashboard's own eight-quarter deviation | B, DC switching (26 against firewalls' 18, 1.44×; lead 8 against 5) | The security team's own counts and the policy's test run as written | NVD's acknowledgement file: 61% of last quarter's CVEs are not yet analysed, and DC switching's are mostly listed as exploited, which NVD analyses first |
| 1 | Each recent quarter nowcast from the acknowledgements (delay to analysis, critical share), forecast as the four-quarter mean, counted by CVE | D, Firewalls (64 against routers' 52, 1.23×; lead 12 against 7) | Backlog-corrected with the counterparty's own analysis record, and the test passes | The triage standard: a CVE affecting several product lines is triaged once on each, and shared kernel and crypto-library CVEs affect up to four lines |
| 2 | Counted as CVE–line pairs, the standard's unit of work | C, Routers (96 against campus switching's 82, 1.17×; lead 14 against 9) | The right grain, backlog-corrected, and the test passes on the last eight quarters | The acknowledgement file: four of those eight quarters still hold unanalysed CVEs, so their counts are nowcasts, while 2023Q3–2025Q2 are fully acknowledged |
| 3 | **Decisive:** the lead's deviation measured on the eight most recent fully acknowledged quarters | **Hold: the analyst stays in the shared pool** (lead 14 against 19) | — | — |

* **The blocking quantity.** Routers' forecast lead over campus switching is 14 critical triages. The standard deviation of the quarterly
  router-minus-campus difference in the eight most recent fully acknowledged quarters is 19. The lead is 0.74 of one deviation, and every
  other pair of lines is closer, so no line's lead holds.
* **Falsifiability.** The answer would have been routers if their forecast had exceeded campus switching's by more than 19 (101 against
  82). Any window of six to ten fully acknowledged quarters gives a deviation between 17 and 21, every one above 14.
* **Partial correction priced (L3).** Every half-applied test names a line. Measuring the deviation on acknowledged quarters but counting
  by CVE gives firewalls a lead of 12 against 8 and assigns firewalls. Keeping the nowcast quarters but adding each one's projection
  variance raises the deviation to 12 and assigns routers (14 against 12).
* **Grid.** Counts (dashboard, nowcast) × grain (CVE, pair) × record for the deviation (latest eight quarters, fully acknowledged quarters)
  = 8 cells. Every dashboard cell names DC switching or firewalls, every CVE-grain cell names firewalls, and the pair-grain cell on the
  latest eight quarters names routers; only pair grain on acknowledged quarters holds.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy names the test and "the record"; no document says a nowcast is not record, that expectations do not
   swing, or which quarters NVD has finished.
2. **Corpus blind to the swing.** *In every quarter the dashboard and the nowcast both cover, the nowcast's filled-in share is an expected
   value with no quarter-to-quarter noise, because it is the same delay curve and critical share applied to each quarter's publications;
   so any record that includes nowcast quarters shows a smoother lead than the acknowledged record ever did.* Back-testing the nowcast
   against acknowledged quarters confirms its level within 4% while saying nothing about its swing.
3. **No arithmetic symptom.** Advisories reconcile to CVEs, pairs to affected-product lists, nowcasts to the acknowledgements; every rung's
   lead and deviation are computed correctly from the record it uses.
4. **Not a row predicate.** The deviation is a statistic over quarters of pair-grain counts, and which quarters count as record comes
   from completeness across every CVE in them.
5. **The enumeration is arithmetic.** No column marks a quarter as complete; completeness is computed from the acknowledgement file.
6. **No cutover date.** The backlog's growth is dated in NVD's notices, but nothing steps in the acknowledged quarters the decision rests
   on; release trains are a standing cadence.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** NVD's acknowledgement file: for every CVE in the vendor's advisories since 2022, the date NVD analysed it and its score, or no
  entry yet.
* **What it certifies.** The nowcast: the delay curve and critical share from the last four complete quarters reproduce every fully
  acknowledged quarter's critical count within 4% when replayed as of earlier dates.
* **What it pins.** Which quarters are record: 2023Q3–2025Q2 are fully acknowledged; every later quarter holds unanalysed CVEs.
* **Twin pair.** The archived dashboards for 2024Q2 and 2024Q4 carried the same router nowcast at the time (54) and the same campus
  nowcast (41). Fully acknowledged, routers ran 71 and 35 (2.0× apart), because a kernel release train shipped to routers in 2024Q2 and not
  in 2024Q4. Nothing in either nowcast separates them: the hold's reason in miniature.
* **Resemblance points at the decoy.** By publication volume and backlog share, next quarter most resembles the last two quarters, whose
  nowcasts are the smoothest in the record.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The staffing policy: the analyst goes to the line with the most NVD-critical triages forecast for next quarter as the mean
  of the last four quarters, if its lead over the runner-up exceeds the lead's quarter-to-quarter standard deviation in the record;
  otherwise the analyst stays in the shared pool. The triage standard: one triage per CVE per affected product line.
* **Empirical pins.** The delay curve and critical share, from the acknowledgements. The affected lines, from each advisory's product list.
* **Voices.** The finance partner: "The dashboard shows criticals falling; the analyst can go wherever is busiest." The security lead:
  "Routers always end up worst once NVD catches up." The firewall product manager: "Firewalls take the hardest hits every quarter."
* **Licensed wrong basis.** The policy records that the regional security council reviews staffing on the dashboard's monthly counts and
  will see the decision against them.

## 8. Determinism by construction

* **Record.** 2023Q3–2025Q2 are the eight most recent quarters with every CVE acknowledged; windows of six to ten such quarters give
  deviations of 17 to 21, and sample or population deviation gives 18 or 19.
* **Nowcast.** Delay curves from any four complete quarters agree within 3 points at every lag, so the forecast lead stays 13–15.
* **Pairs.** Every advisory lists its affected lines in full, so the pair count has one reading.
* **Leads.** Every rung's leader leads by at least 1.17×, and every lead clears that rung's deviation by at least 3, so no earlier rung is a
  near hold.
* **Scores.** The policy counts NVD's score; no CNA score enters any rung.

## 9. Prompt sketch and deliverables

> We have one extra triage analyst for next quarter, and the staffing policy sends them to the product line with the most critical CVEs
> coming. Our finance partner says the dashboard shows criticals falling anyway. Tell me which line gets the analyst, or whether none has
> earned it, in one sentence for the staffing note, and send `triage_case.xlsx` with the build and the sheets below, a chart
> `lead_vs_swing.png`, and a one-page `staffing_note.pdf`.

* `triage_case.xlsx` — quarterly counts by line under each construction, the lead and deviation for each, the fix-time sheet (ask A) and
  the support-case sheet (ask B).
* `lead_vs_swing.png` — the router-minus-campus difference by quarter, acknowledged quarters as solid points and nowcast quarters as
  hollow ones, a band of one deviation either side of zero drawn from each record, and next quarter's forecast lead marked against both
  bands.
* `staffing_note.pdf` — the committed call, the blocking quantity, and what lead would have earned the analyst.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the five product lines and each month of last quarter, the median days from an
  advisory's publication to its fixed release. *Device:* a fix moved to a later maintenance release keeps its original release date in the
  advisory table, with the revised date in the release-revision table, as the release-engineering guide documents; reading the advisory
  table understates time to fix for three lines. Fix times enter no part of the staffing test.
* **Ask B (device-carried).** For each product line, the customer support cases about vulnerabilities opened last quarter. *Device:* a
  case merged into a master case keeps its own ID, with the merge in the case-link table, as the support data guide documents; counting raw
  IDs overstates cases on every line. Support cases enter no part of the staffing test.
* **Ask C (validity).** The leader, its lead and the deviation under each of the four rung constructions.
* **Decoupling.** Clearing the acknowledged-record deviation changes no figure in asks A or B.

## 11. Rubric arithmetic

5 lines × 3 months (ask A) + 5 lines (ask B) + 4 constructions × 3 (ask C) + the committed hold, the lead, the deviation and the
falsifying lead + 5 named chart parts + 3 files ≈ 44 criteria.

## 12. World-building constraints

* Pair-grain forecast (critical triages, four-quarter mean): routers 96, campus switching 82, firewalls 71, DC switching 60, wireless 41.
  CVE-grain nowcast: firewalls 64, routers 52, campus 40, DC switching 35, wireless 30. Dashboard last quarter: DC switching 26, firewalls 18.
* Deviations of the leader's lead: dashboard 5; CVE grain on nowcast quarters 7, on acknowledged quarters 8; pair grain on the latest eight
  quarters 9 (12 with projection variance), on the eight fully acknowledged quarters 19.
* 61% of last quarter's CVEs unanalysed; nowcasts reproduce acknowledged quarters' levels within 4%.
* The twin quarters carried identical nowcasts at the time; acknowledged router counts 71 and 35.
* Release revisions and merged support cases touch no CVE, pair or acknowledgement in the test.
