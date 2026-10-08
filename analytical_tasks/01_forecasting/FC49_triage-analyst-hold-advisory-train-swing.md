# FC49 — Which product line gets next quarter's extra vulnerability-triage analyst, when the lead is real but smaller than the swing each line's release train puts into its own triage quarters

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Product Analytics · product security operations (network equipment) |
| Mirrors | Staffing vulnerability response by product line (network vendors with bundled half-yearly advisories, platform security teams triaging shared-component CVEs per product), where the work lands when each line ships its advisory, not when the CVE is published |
| Decision shape | Which of N gets one scarce thing: the extra triage analyst for the first quarter, to one of five product lines, or held in the shared pool |
| Committed call | The product line that gets the analyst, or a hold, with the lead and the quarter-to-quarter standard deviation that decide it |
| Gap · Pattern | Gap 1 (time) over Gap 3 (objective) · hold forced by a computed blocking quantity (Part 6.4: a lead smaller than its own quarter-to-quarter swing), with two grains both flawless (Pattern D) at rung 2 |
| Gate G mechanism | signal_vs_noise_or_hold, with forecasting support |
| Measured traps engaged | #16 lets small shortcuts flip a thin margin · #2 counts file rows instead of the real unit · #7 uses the ready-made measure |
| Calibration form | Counterparty acknowledgement file: the national coordination centre's acknowledgement of every advisory the vendor has published since 2022, with its publication date and the CVEs and product lines it covers |
| Driving force | The staffing policy assigns the analyst only when the leader's forecast lead exceeds the quarter-to-quarter standard deviation of that lead. The triage standard counts one triage per CVE per affected line, done when that line's advisory ships. Dated by CVE publication, the router-minus-campus difference is steady, with a deviation of 9 against routers' lead of 14. But routers ship advisories every quarter and campus switching bundles a quarter of its year into half-yearly advisories, so dated by advisory, as the work actually lands, the difference swings with a deviation of 19. The lead sits inside one deviation: no line has earned the analyst. |

## 1. Situation

A network-equipment vendor's product-security team has one extra triage analyst for the first quarter. The staffing policy sends the
analyst to the product line with the most critical triages forecast for next quarter, forecast as the mean of the last four quarters, and
only if that line's lead over the runner-up is larger than the lead's quarter-to-quarter standard deviation over the last eight quarters;
otherwise the analyst stays in the shared pool. The triage standard counts one triage per CVE per affected product line, done as part of
that line's advisory. Every advisory carries the vendor's own severity score. The pack holds the CVE records, the advisories with their
affected-product lists, the coordination centre's acknowledgements, the security dashboard, each line's release calendar and the policy.
The staffing note is due on 10 December.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the CVE records, the advisories, the acknowledgements and the dashboard's counts of critical CVEs by
  publication month. No stakeholder's reading of their own numbers is overturned; routers really do face the most critical triages over a
  year. The difficulty is whether the lead is larger than the swing of the quarters the work actually lands in.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the finance partner's view and every voice. The pair-grain build dated by publication still names routers by
  14 against a deviation of 9, and every input to it is still correct.
* **Instrument repair.** Clean-data test. No file the ladder reads is incomplete, stale or narrower than it claims: every CVE carries its
  publication date, NVD's score and the vendor's, every advisory its date and affected lines, every acknowledgement its advisory; the
  dashboard records NVD-critical CVEs by publication month and primary line, a different attribute from the policy's triages, so reading it
  is an ordinary wrong rung. With nothing to repair, rung 0 names DC switching (lead 8 against 5), rung 1 firewalls (12 against 7) and rung 2 routers (14
  against 9), and dating each triage by its line's advisory is still needed, because no file stores a line's triage quarter.
* **Lens swap.** The naive read and the answer date the same work at different moments: when the CVE was published, against when each line
  ships the advisory that carries its triage.

## 3. The driving force

A strong solver starts from the dashboard, then rebuilds the policy's four-quarter mean from the advisories, because the policy counts the
vendor's own severity and the dashboard pulls NVD's. It reads the triage standard and moves from CVEs to CVE–line pairs, because a shared
kernel or crypto-library CVE is triaged on every line it affects. Routers lead campus switching by 14 critical triages, and the standard
deviation of the router-minus-campus difference over the last eight quarters, dated by publication, is 9, so the analyst goes to routers.
Every step is correct except the date. The triage standard puts a triage in the quarter its line's advisory ships. Routers ship advisories
every quarter, so their triages track publication. Campus switching ships monthly patches and a half-yearly bundle in the first and third
quarters that carries a quarter of its year's triages. Dated by advisory, as the coordination centre's acknowledgements record them, the
difference swings by up to 41 between quarters, a deviation of 19. A lead of 14 is inside one deviation of its own swing, so the analyst
stays in the pool.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The dashboard's four-quarter mean of critical CVEs by primary line, critical by NVD's score; lead against the dashboard's own eight-quarter deviation | B, DC switching (48 against firewalls' 40, 1.20×; lead 8 against 5) | The security team's own counts and the policy's test run as written | The policy counts severity as the vendor scores it on each advisory, and NVD rates 31% of the vendor's critical firewall and router CVEs below critical |
| 1 | Four-quarter mean of critical CVEs by the vendor's score, by publication, each counted once under its primary line | D, Firewalls (64 against routers' 52, 1.23×; lead 12 against 7) | The policy's forecast built from the advisories' own scores, and the test passes | The triage standard: a CVE affecting several product lines is triaged once on each, and shared kernel and crypto-library CVEs affect up to four lines |
| 2 | Counted as CVE–line pairs, the standard's unit of work, dated by publication | C, Routers (96 against campus switching's 82, 1.17×; lead 14 against 9) | The right grain, the policy's forecast, and the test passes on the last eight quarters | The triage standard: a triage is done as part of its line's advisory, and the release calendar ships campus switching's in a half-yearly bundle plus monthly patches |
| 3 | **Decisive:** each CVE–line triage dated by the advisory that carried it, from the acknowledgements, and the lead's deviation measured on those quarters | **Hold: the analyst stays in the shared pool** (lead 14 against 19) | — | — |

* **The blocking quantity.** Routers' forecast lead over campus switching is 14 critical triages. Dated by advisory, the standard deviation
  of the quarterly router-minus-campus difference over the last eight quarters is 19. The lead is 0.74 of one deviation, and every other
  pair of lines is closer, so no line's lead holds.
* **Falsifiability.** The answer would have been routers if their forecast had exceeded campus switching's by more than 19 (101 against
  82). Windows of six to ten quarters give deviations of 17 to 21, every one above 14.
* **Partial correction priced (L3).** Every half-applied test names a line. Dating by advisory but counting each CVE once under its
  primary line gives firewalls a lead of 12 against 8 and assigns firewalls. Dating by advisory but spreading each half-yearly bundle over
  the six months its fixes were built gives a deviation of 10 and assigns routers (14 against 10).
* **Grid.** Severity (NVD's, the vendor's) × grain (CVE, pair) × dating (publication, advisory) = 8 cells. Every NVD-severity cell names
  DC switching or campus switching with a lead above its deviation, every vendor-severity CVE-grain cell names firewalls, and the
  vendor-severity pair-grain cell dated by publication names routers; only vendor-severity pairs dated by advisory hold.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy names the test; the triage standard ties a triage to its line's advisory; no document says the dating
   changes the deviation, or that a release train swings a line's quarters.
2. **Corpus blind to the swing at publication grain.** *In every closed quarter the publication-dated pair counts were smooth for every
   line, because CVEs are published evenly through the year whatever the release trains do; so the lead's deviation measured on
   publication dates was 9 in every eight-quarter window since 2022, and the test always passed.* The swing lives only in advisory dates.
3. **No arithmetic symptom.** CVEs reconcile to advisories, pairs to affected-product lists, advisories to acknowledgements; four-quarter
   totals agree within one triage under either dating, so every rung's forecast is internally consistent.
4. **Not a row predicate.** Each triage needs its CVE joined to every advisory that lists it, each advisory to its line and date, and the
   pairs regrouped into quarters before any deviation is taken.
5. **The enumeration is arithmetic.** No column holds a line's triage quarter; it is computed from the acknowledgements.
6. **No cutover date.** The release trains are a standing cadence; nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The coordination centre's acknowledgements since 2022: every advisory the vendor published, its date, and the CVEs and
  product lines it covers.
* **What it certifies.** The pair grain (every CVE–line pair appears in exactly one acknowledged advisory) and the four-quarter forecast,
  which agrees under either dating.
* **What it pins.** Each triage's quarter, and with it the deviation of the lead: 19 on advisory dates, 9 on publication dates.
* **Twin pair.** In 2024Q2 and 2024Q3 campus switching had identical publication-dated pair counts (80 each). Dated by advisory, its
  triages were 50 and 100 (2.0× apart), because the half-yearly bundle shipped in 2024Q3. Publication dating predicts them equal; only
  advisory dating reproduces both, and with them the swing behind the hold.
* **Resemblance points at the decoy.** By publication volume and line mix, next quarter most resembles the last four, whose
  publication-dated counts are the smoothest in the record.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The staffing policy: the analyst goes to the line with the most critical triages forecast for next quarter as the mean of
  the last four quarters, if its lead over the runner-up exceeds the lead's quarter-to-quarter standard deviation over the last eight
  quarters; otherwise the analyst stays in the shared pool. The triage standard: one triage per CVE per affected product line, done as part
  of that line's advisory. Severity is the vendor's own score on each advisory.
* **Empirical pins.** Each triage's quarter, from the acknowledgements. The affected lines, from each advisory's product list.
* **Voices.** The finance partner: "The dashboard shows critical CVEs falling; the analyst can go wherever is busiest." The security lead:
  "Routers always end up worst once the advisories are out." The firewall product manager: "Firewalls take the hardest hits every quarter."
* **Licensed wrong basis.** The policy records that the regional security council reviews staffing on the dashboard's monthly counts and
  will see the decision against them.

## 8. Determinism by construction

* **Dating.** Every CVE–line pair sits in exactly one acknowledged advisory, so its quarter has one reading.
* **Forecast.** Four-quarter totals under advisory and publication dating agree within one triage for every line, so the lead is 14 either
  way and only the deviation moves.
* **Deviation.** Sample or population deviation gives 18 or 19; windows of six to ten quarters give 17 to 21.
* **Leads.** Every rung's leader leads by at least 1.17×, and every lead clears that rung's deviation by at least 3, so no earlier rung is a
  near hold.
* **Severity.** The policy counts the vendor's score, which every advisory carries; NVD's score, complete for every CVE, enters only rung 0.

## 9. Prompt sketch and deliverables

> We have one extra triage analyst for next quarter, and the staffing policy sends them to the product line with the most critical work
> coming. Our finance partner says the dashboard shows critical CVEs falling anyway. Tell me which line gets the analyst, or whether none
> has earned it, in one sentence for the staffing note, and send `triage_case.xlsx` with the build and the sheets below, a chart
> `lead_vs_swing.png`, and a one-page `staffing_note.pdf`.

* `triage_case.xlsx` — quarterly counts by line under each construction, the lead and deviation for each, the fix-time sheet (ask A) and
  the support-case sheet (ask B).
* `lead_vs_swing.png` — the router-minus-campus difference by quarter, publication-dated as hollow points and advisory-dated as solid
  ones, a band of one deviation either side of zero for each dating, the campus bundle quarters shaded, and next quarter's forecast lead
  marked against both bands.
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
* **Decoupling.** Clearing the advisory dating changes no figure in asks A or B.

## 11. Rubric arithmetic

5 lines × 3 months (ask A) + 5 lines (ask B) + 4 constructions × 3 (ask C) + the committed hold, the lead, the deviation and the
falsifying lead + 5 named chart parts + 3 files ≈ 44 criteria.

## 12. World-building constraints

* Pair-grain forecast (critical triages, four-quarter mean): routers 96, campus switching 82, firewalls 71, DC switching 60, wireless 41.
  CVE-grain forecast: firewalls 64, routers 52, campus 40, DC switching 35, wireless 30. Dashboard (NVD severity, four-quarter mean): DC
  switching 48, firewalls 40; NVD rates 31% of the vendor's critical firewall and router CVEs below critical.
* Deviations of the leader's lead: dashboard 5; CVE grain 7 by publication, 8 by advisory; pair grain 9 by publication, 19 by advisory.
* Campus switching: monthly patches carry three quarters of its triages and a bundle in the first and third quarters the rest; routers
  ship every quarter. Spreading each bundle over its six months gives a deviation of 10.
* The twin quarters have identical publication-dated campus counts (80); advisory-dated 50 and 100.
* Release revisions and merged support cases touch no CVE, pair or advisory date in the test.
