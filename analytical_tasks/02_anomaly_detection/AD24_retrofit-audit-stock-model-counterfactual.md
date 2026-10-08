# AD24 — Which partner area gets the fund's one field audit team, when a smooth counterfactual books a lump of identical flats as shading

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Nonprofit & Grant-making · home-energy retrofit grants |
| Mirrors | Detecting manipulation at an eligibility threshold when legitimate clusters sit just under the line (seller-rating cut-offs for marketplace badges at Amazon and eBay, means-tested benefit thresholds, emissions-test pass marks in vehicle inspection networks) |
| Decision shape | Which of N gets one scarce thing: the fund's single field audit team for next quarter |
| Committed call | The one partner area the audit team works in next quarter |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · the quiet second trap (E15): beyond the loud heaping and stock-shape story, a lump of identical dwellings inside the window that a smooth counterfactual books as shading, controlled by the stock model's scores for the same dwellings; a grant segment the register labels uniformly, split by route through the application file at the lower rung (E29) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #6 treats a mixed segment all one way · #7 uses the ready-made measure |
| Calibration form | Prior-period close-out: the close-out reports of the last four audit rounds, eight audited areas, each with every re-assessed certificate's lodged and re-assessed score |
| Driving force | Every bunching estimator a careful analyst reaches compares the lodged scores with a smooth curve, and a smooth curve cannot bend to a lump of identical dwellings. In March an assessor team surveyed C's Oak Lane estate, 640 identical electrically heated flats that genuinely score 36 to 38, and the curve books them as shading. The stock model scores the same dwellings by archetype before any assessor arrives; against that counterfactual, scaled outside the window, C's excess vanishes and E's, real shading spread across ordinary gas-heated houses, leads. |

## 1. Situation

A housing charity's warm-homes fund pays for retrofits in six partner areas. It runs two routes: on the rating route a home qualifies with
an energy rating of 38 or below on a certificate lodged by an accredited assessor; on the benefit route a household on means-tested
benefits qualifies at any rating. The fund's integrity policy sends its one field audit team, for next quarter, to the partner area where
the certificates the threshold applied to sit just below it in the greatest excess over what the area's housing would otherwise score, per
100 such certificates over the last twelve months. The pack carries the certificate register, the fund's application file, the stock
model (an archetype score for every dwelling in the six areas), the scheme rules, the integrity manual and the audit close-outs.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: every lodged certificate, every application's route, every modelled score and every close-out
  re-assessment. C's Oak Lane flats really score 36 to 38, and A's housing really sits near the line. Nothing reported is overturned and no
  stakeholder read is corrected; the difficulty is which counterfactual a lodged distribution is compared with.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices. The integrity manual's smooth counterfactual on the rating-route certificates, the natural careful
  build, still names C.
* **Instrument repair.** Make the register perfect; every lodged score is already what its assessor lodged. A better smooth curve still
  cannot bend to a lump of identical flats, and only the same dwellings' modelled scores show the lump was there before any assessor came.
* **Lens swap.** The naive comparison is the lodged distribution against a curve drawn through it; the answer compares rating-route
  certificates with the modelled scores of the same dwellings, a different reference population: dwellings before assessment, not
  certificates after it.

## 3. The driving force

A strong solver distrusts the raw share of certificates just under the line, which counts housing that simply sits near the band boundary,
and fits the integrity manual's smooth counterfactual, a polynomial outside the window with round-number dummies. Run on every grant
certificate, that names B. It then reads the scheme rules: benefit-route homes qualify at any rating, so only rating-route certificates
carry the incentive, and the application file splits a segment the register labels as one. On the rating route alone the smooth
counterfactual names C. Each step is competent, and the loud story, heaping and stock shape, is beaten. The quiet one is not. In March an
assessor team surveyed 640 ex-council flats on C's Oak Lane estate, identical electrically heated blocks that score 36 to 38 and genuinely
qualify; a smooth curve cannot bend to a lump of identical dwellings, so it books the lump as shading. The stock model scores every
dwelling in the six areas by archetype, and its scores for the same rating-route dwellings hold the lump before any assessor arrived.
Against that histogram, scaled outside the window, C's excess falls from 11.4 to 1.5 per 100 and E, where the shading is, leads at 7.8.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Share of grant certificates scoring 34–38, last twelve months | A (31%; 1.24× B) | The certificates just under the line, counted directly | The register: A's sale and rental certificates sit at 34–38 in the same share, so the share is A's housing |
| 1 | The integrity manual's smooth counterfactual (polynomial outside 34–43, round-number dummies) on every grant certificate; excess per 100 | B (6.2; 1.19× D) | The industry's bunching estimator, heaping and stock shape handled | The scheme rules and the application file: benefit-route homes qualify at any rating, and the benefit route is 58% of C's grant certificates and 55% of E's against 8% of B's |
| 2 | The smooth counterfactual on rating-route certificates | C (11.4; 1.20× D) | The estimator on the population the threshold binds | The stock model: 86% of C's excess is the Oak Lane flats, every one modelled at 36–38 before any assessor visited |
| 3 | **Decisive:** rating-route certificates against the stock model's scores for the same dwellings, the modelled histogram scaled to the lodged one outside the window; excess per 100 | **E (7.8)** (5th of 6 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (21%), 4th on rung 1 (3.6) and 3rd on rung 2 (8.0), and leads only rung 3, 1.22× B (6.4).
  Intermediate leaders hold margins of 1.24×, 1.19× and 1.20×.
* **Discriminator dominance.** C carries a 1.43× advantage over E into rung 3 (11.4 against 8.0). The stock-model counterfactual multiplies
  C's excess by 0.13 and E's by 0.98, an edge of 7.4 against the 1.2 × 1.43 = 1.71 required, 4.33× headroom.
* **Partial correction priced (L3).** A solver who spots the Oak Lane lump and drops the estate, keeping the smooth curve, names D (9.5
  against E's 8.0, 1.19×), whose own lump of solid-wall terraces the curve still counts. A solver who takes the counterfactual's shape from
  the area's sale and rental certificates names B (12.0 against E's 8.1, 1.48×), because B's sales are a new-build suburb with almost
  nothing at 34–38. A solver who compares each certificate with its own dwelling's modelled score and counts crossings names A (14.2
  against E's 10.6, 1.34×), because archetype error sends genuine band-F homes across the line in proportion to how many sit near it. A
  solver who uses the stock model on every grant certificate names B (5.9 against E's 3.5, 1.69×). No half lands on E.
* **Grid.** Population (every grant certificate or the rating route) × counterfactual (raw share, smooth curve, sale-and-rental shape,
  stock-model shape) gives eight cells: raw shares name A in both populations; the smooth curve names B on every certificate and C on the
  rating route; the sale-and-rental shape names B in both; the stock-model shape names B on every certificate and E on the rating route.
  Only the stock-model shape on the rating route names E, and the nearest wrong cell (B) needs only the route split skipped.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy asks for the excess over what the area's housing would otherwise score and names no reference. The
   integrity manual describes only the smooth curve, and the stock model is filed for targeting outreach letters.
2. **The corpus pins a construction, not a menu.** The stock-model shape on the rating route reproduces the confirmed excess of 8 of 8
   audited areas within 0.5 per 100; the smooth curve 5, the sale-and-rental shape 4 and dwelling-level crossings 2, and every rival
   overstates its misses, so each also overstates the rounds' total. The construction joins each certificate through its dwelling to an
   archetype score, scales one histogram to another outside the window and differences them inside it, and no column holds the excess.
3. **No arithmetic symptom.** Certificates tie to the register, routes to the application file and modelled scores to the stock model;
   every estimator runs cleanly and every fit converges.
4. **Not a row predicate.** It needs a join from certificate to dwelling to archetype score, two histograms per area, a scaling over the
   ranges outside the window, and a difference inside it.
5. **The enumeration is arithmetic.** Excess is a property of two histograms; no field marks a certificate as shaded.
6. **No cutover date.** E's shading runs steadily through the year. The only dated event, the March survey of Oak Lane, sits under the
   decoy.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The close-out reports of the last four audit rounds: eight audited areas, in each the rating-route certificates under the line
  that the team re-assessed, with each one's lodged and re-assessed score, and the round's confirmed excess per 100 rating-route
  certificates.
* **What it pins.** The stock-model shape on the rating route reproduces 8 of 8 confirmed excesses within 0.5 per 100; the smooth curve 5,
  overstating the three areas with estate lumps; the sale-and-rental shape 4; dwelling-level crossings 2.
* **Twin pair.** Round-two area Q-2 and round-four area Q-4 are identical on rating-route certificates (1,520), smooth-curve excess (9.4 per
  100), share under the line and route mix. Their close-outs confirmed 8.9 and 4.3 per 100 (2.07×): Q-4's window held 300 identical flats
  the stock model places at 36 and 37.
* **Every rule exercised.** One audited area had no benefit-route applicants, so the split is tested at its limit; one had an estate lump
  at 40–41, outside the window, so the scaling ranges are tested.
* **Resemblance points at the decoy.** By register profile C most resembles Q-2, the largest confirmed excess in the corpus.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The integrity policy: the audit team goes to the partner area where the certificates the threshold applied to sit just
  below it in the greatest excess over what the area's housing would otherwise score, per 100 such certificates over the last twelve
  months. The scheme rules: the rating route requires 38 or below; the benefit route has no rating condition. The application file
  records each certificate's route.
* **Empirical pins.** The stock-model counterfactual for the same dwellings, scaled outside the window, from the close-outs.
* **Voices.** The fund's grants manager: "Area A has the most homes just under the line; that's where the shading is." The accreditation
  body's quality lead: "Our bunching method is the industry standard; run it on every grant certificate."
* **Licensed wrong basis.** The policy records that the accreditation body measures shading with the smooth curve on every grant
  certificate and will review the audit choice on that basis.

## 8. Determinism by construction

* **Join.** Every rating-route certificate carries its dwelling's property reference, and every dwelling in the six areas is in the stock
  model, so the join is exact.
* **Scaling.** The modelled histogram is scaled to the lodged one over scores 20–33 and 44–60, as every close-out did; scaling over 15–33
  and 44–70 leaves the order and every rung leader unchanged.
* **Heaping.** Round-number heaping moves mass between neighbouring scores inside the window or inside a scaling range, so no total moves.
* **Window.** Twelve months by lodgement date; the threshold and the route rules were unchanged throughout.

## 9. Prompt sketch and deliverables

> Our one field audit team can spend next quarter re-assessing homes in a single partner area. Our grants manager is sure the area with the
> most certificates just under the line is the place to go. Name the area in a line for the trustees' integrity report, with
> `audit_area.xlsx` holding the sheets below, the chart `threshold_excess.png`, and a short `trustee_note.docx`.

* `audit_area.xlsx` — the area build under each population and counterfactual, the payments sheet (ask A), the guarantees sheet (ask B)
  and the close-out back-test (ask C).
* `threshold_excess.png` — for each area, the rating-route histogram of lodged scores against the stock-model counterfactual, the threshold
  marked, the Oak Lane lump labelled, and the excess shaded.
* `trustee_note.docx` — the committed area and why A, B and C are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each partner area, installer payments in each of the last four quarters, by quarter of job
  completion. *Device:* the fund holds back 10% of each payment until the installer's twelve-month workmanship check and releases it as a
  separate line, dated on release and carrying the job reference, per the payments guide. Summing lines by their own dates moves
  retentions out of their completion quarters in every area. The audit build never reads payments.
* **Ask B (device-carried).** For each partner area, homes whose walls were insulated under the fund last year. *Device:* a cavity-wall
  guarantee covers one building, so a semi-detached pair insulated in one job holds one guarantee listing both addresses, per the
  guarantee agency's rules. Counting guarantees undercounts homes in the three areas with semi-detached stock.
* **Ask C (validity).** For each of six constructions (the raw share, the smooth curve on every certificate and on the rating route, the
  sale-and-rental shape, dwelling-level crossings and the stock-model shape), the audited areas' confirmed excess it reproduces within 0.5
  per 100, out of 8.
* **Decoupling.** Clearing the stock-model counterfactual changes no figure in asks A or B.

## 11. Rubric arithmetic

6 areas × 4 quarters (ask A) + 6 areas (ask B) + 6 constructions (ask C) + the committed area, its excess and the margin over B + 5 named
chart parts + 3 files ≈ 47 criteria.

## 12. World-building constraints

* Rating-route and benefit-route certificates: A 1,900 and 800, B 2,300 and 200, C 1,450 and 2,000, D 1,650 and 1,350, E 1,600 and 1,950,
  F 1,500 and 1,000.
* Rung leaders are A, B, C, E. E is 5th / 4th / 3rd / 1st; intermediate margins are at least 1.19×; E leads rung 3 by 1.22×.
* Smooth-curve excess on the rating route: C 11.4, D 9.5, E 8.0, B 6.7, A 3.4, F 2.2. Stock-model excess: E 7.8, B 6.4, D 4.6, A 3.0, F 1.8,
  C 1.5.
* Oak Lane: 640 identical flats in C, modelled at 36–38 and surveyed in March. D's solid-wall terraces are modelled at 35–37. B's sales are
  dominated by a new-build suburb.
* The close-outs hold eight audited areas; Q-2 and Q-4 are identical on every register column.
* Retention releases and shared guarantees never touch certificates, routes or modelled scores.
