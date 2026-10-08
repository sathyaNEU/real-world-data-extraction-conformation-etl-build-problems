# AD21 — Which product and hazard get the regulator's one full engineering investigation, when the reports that matter never name a model

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · consumer product safety regulation |
| Mirrors | Attributing unlabelled reports to products through a marker the reports already carry (crash reports matched to builds by signature at Apple and Google, marketplace complaints matched to listings by price and date at Amazon, warranty claims matched to production batches by purchase price) |
| Decision shape | Which of N gets one scarce thing: next quarter's single full engineering investigation in the regulator's test laboratory |
| Committed call | The one product–hazard pair investigated, and its report rate per 100,000 units sold |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · a latent attribution marker (E19): retailer, month and price paid identify the model exactly through the retailers' price lists, pinned by the revision log's follow-ups; an implicit SKU join at the lower rung (E20) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #17 guesses an attribution the data can settle · #18 joins only on the visible key · #7 uses the ready-made measure |
| Calibration form | Retry or revision log: the case-version log of every report, including 1,240 reports filed without a model whose model a later follow-up version supplied |
| Driving force | Most fire reports about the K-200 kettle come from shoppers at a discount chain who never note a model, so the pair looks ordinary on every count of named reports. Each such report gives the retailer, the month and the price paid, and in every retailer-month each model sold at its own price. Matching reports to the retailers' price lists assigns every one of them exactly, as the 1,240 later-resolved reports confirm, and K-200 fires rise to the top. |

## 1. Situation

A national product-safety regulator's laboratory can run one full engineering investigation next quarter, on one product–hazard pair. The
surveillance policy sends it to the pair with the highest rate of reports per 100,000 units sold over the last four quarters, counting each
case once at its latest version. The pack carries the report database with every case version, the market-data sales by model, the
retailers' monthly price lists and SKU catalogues, and the revision log.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each report as filed and as revised, the sales, the price lists and catalogues, and every follow-up.
  The head of surveillance's named-product reports are accurate. Nothing reported is overturned; the difficulty is an attribution the
  reports leave blank and other files settle.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices. Counting cases at their latest version, linked to models through the model field and the
  retailers' SKUs, still names the charger.
* **Instrument repair.** Make the report form perfect from now on; four quarters of reports are already filed. A better form for future
  reports does not name the model in the ones already received, and the files that do are not the form.
* **Lens swap.** The naive rate counts reports linked to a model by an identifier; the answer counts reports assigned by a price paid, a
  different population of reports that adds 312 fires to one pair.

## 3. The driving force

A strong solver drops superseded case versions, as the policy says, notices that retailers file under their own SKU and joins those reports
to models through the retailers' catalogues, divides by units sold and names the C-7 charger. Each step is competent. Left over are the
reports with no model and no SKU, 41% of all fire reports, which every natural reading drops, spreads by sales share or gives to each
retailer's best seller. Each of those reports records where it was bought, when, and what was paid. The retailers' price lists show that in
every retailer-month each model sold at its own price, so retailer, month and price name the model exactly. The revision log holds 1,240
reports first filed without a model and later completed by a follow-up, and the price match reproduces every one. Applied to the
quarter's blanks, it puts 312 fires on the K-200, sold almost entirely through a discount chain whose shoppers never write down a model.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Reports per 100,000 units for each pair, every row in the database | A, K-100 kettle and scalds (41) | The database's own counts on the policy's rate | The policy counts each case once at its latest version, and the revision log shows A's cases filed in up to five versions |
| 1 | Hygiene: each case at its latest version, linked by the model field | B, H-12 heater and overheating (29; 1.21× C) | Clean case counts on the policy's basis | The retailer reporting guide: retailers file under their own SKU, and their reports carry no model field |
| 2 | Retailer reports joined to models through the retailers' SKU catalogues | C, C-7 charger and fire (36; 1.24× B) | Every report with an identifier is now linked, and no guess is made for the rest | The revision log: 1,240 reports filed with no model were later completed by follow-ups, and they are spread nothing like sales or best sellers |
| 3 | **Decisive:** every report with no model and no SKU assigned through the retailer's price list for the month it records | **E, K-200 kettle and fire (47)** (5th of 8 on rung 0) | — | — |

* **Position table.** E ranks 5th on rungs 0, 1 and 2 (18, 17 and 19), and leads only rung 3, 1.27× C. Intermediate leaders hold margins of
  1.24×, 1.21× and 1.24×.
* **Discriminator dominance.** C carries a 1.89× advantage over E into rung 3 (36 against 19). The price match multiplies E's rate by 2.47 and
  C's by 1.03, an edge of 2.41 against the 1.2 × 1.89 = 2.27 required; net 1.27×.
* **Partial correction priced (L3).** A solver who spreads the blank reports by each model's sales share in the category names C again (38),
  because the K-200 sells little outside the discount chain. A solver who gives each blank to the retailer's best-selling model in the
  category names B, the heater the discount chain sells most.
* **Grid.** Versions (all or latest) × identifier joins (model field, plus SKU) × blanks (dropped, sales share, best seller, price match)
  gives sixteen cells: all-version cells name A; latest-version cells name B or C under every blank rule but the price match. Only the
  price match with both joins names E, and the nearest wrong cell (C at 38) needs the blanks spread by sales.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy counts cases; the reporting guide explains SKUs. Nothing says a price names a model, and the price lists
   are filed for retail pricing studies.
2. **The corpus pins a construction, not a menu.** The price match reproduces 1,240 of 1,240 follow-up attributions; the best-seller rule
   reproduces 41%, and sales-share spreading assigns fractions no follow-up ever shows. The match is a construction: a three-key join from a
   report to a different file's price list for its month, unique only because no two models shared a price at a retailer in a month.
3. **No arithmetic symptom.** Cases reconcile to versions, SKUs to catalogues, sales to the market data; the blanks look like ordinary
   incomplete reports.
4. **Not a row predicate.** It needs each report's retailer and month matched to that retailer's price list, then the price matched to the
   single model sold at it, then case counts re-aggregated by pair and divided by sales.
5. **The enumeration is arithmetic.** Which model each blank report concerns is computed; no column holds it.
6. **No cutover date.** K-200 fires arrive steadily across the four quarters; no series steps.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The revision log: every version of every report over four years, among them 1,240 reports filed without a model whose model a
  consumer follow-up or an inspector's visit later supplied.
* **What it pins.** The price match assigns all 1,240 to the model the follow-up named; 8% of blank reports carry no price or retailer and
  stay unassigned under every rule, changing no rank.
* **Twin pair.** The discount chain's and a homeware chain's blank kettle-fire reports in the second quarter are identical on count (58),
  months, regions and descriptions. Follow-ups resolved 37 and 18 of them to the K-200 (2.06×); only the two chains' price lists separate
  them.
* **Every rule exercised.** One retailer changed a model's price mid-month, so the month boundary is tested; one model was sold under two
  SKUs at one retailer, so the SKU join is tested.
* **Resemblance points at the decoy.** By named reports, K-200 fires resemble the low-rate pairs closed without action last year.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The surveillance policy: the investigation goes to the pair with the highest rate of reports per 100,000 units sold over
  the last four quarters, each case counted once at its latest version. The market data's units sold by model and quarter.
* **Empirical pins.** The price-list attribution, from the revision log's follow-ups.
* **Voices.** The head of market surveillance: "We act on what consumers tell us about named products." The laboratory manager: "K-100
  scalds fill our inbox every week."
* **Licensed wrong basis.** The policy records that the manufacturers' trade association counts only reports naming a model and will
  present its rates at the planning review.

## 8. Determinism by construction

* **Prices.** In every retailer-month, every model in a category sold at a distinct price; mid-month price changes are dated in the lists,
  and no report falls on a change day.
* **Versions.** Version numbers are unique within a case, so the latest version is a key maximum.
* **Unassignable reports.** The 8% with no price or retailer are excluded under every rule and touch no leader.
* **Window and sales.** Four quarters by report date; units sold by model from the market data, which no rung varies.

## 9. Prompt sketch and deliverables

> Our test laboratory has one full engineering investigation next quarter, and it goes to one product and one hazard. The head of market
> surveillance acts only on reports that name a product. Tell me the pair and its report rate, in a sentence for the surveillance plan, with
> `investigation_choice.xlsx` holding the sheets below, the chart `report_attribution.png`, and `surveillance_plan_note.docx`.

* `investigation_choice.xlsx` — the pair build with every report's attribution route, the recall sheet (ask A), the channel sheet (ask B)
  and the attribution back-test (ask C).
* `report_attribution.png` — each pair's rate as a stacked bar by attribution route (model field, SKU, price match), the K-200 bar
  highlighted, and the twin chains' resolved splits as an inset.
* `surveillance_plan_note.docx` — the committed pair, its rate, and why the named-report ranking is not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the ten product categories, recall notices in the last two years and the median days
  from first report to recall. *Device:* a recall extended to further batches is published as an amendment under a new notice number
  linked to the original, per the recall register's notes. Counting notices overstates recalls in the four categories with extensions. The
  investigation build never reads the recall register.
* **Ask B (device-carried).** For each of the nine regions, reports filed in the last four quarters and the share filed by phone.
  *Device:* phone reports are keyed by call-centre staff into the web form, so they carry the web channel and a staff ID in the submitter
  field, per the intake guide. Reading the channel field alone understates phone reports everywhere.
* **Ask C (validity).** For each of the four blank-report rules (dropped, sales share, best seller, price match), the follow-up attributions
  it reproduces out of 1,240.
* **Decoupling.** Clearing the price match changes no figure in asks A or B.

## 11. Rubric arithmetic

10 categories × 2 (ask A) + 9 regions × 2 (ask B) + 4 rules (ask C) + the committed pair, its rate and the margin over C + 5 named chart parts +
3 files ≈ 53 criteria.

## 12. World-building constraints

* Rung leaders are A, B, C, E. E is 5th / 5th / 5th / 1st; intermediate margins are at least 1.21×; E leads rung 3 by 1.27×.
* 41% of fire reports carry no model and no SKU; 312 of them match the K-200 by price; the K-200 sells 87% through the discount chain.
* No two models share a price at a retailer in a month; 8% of blank reports have no price or retailer.
* The revision log holds 1,240 follow-up attributions; the two chains' second-quarter blank kettle-fire reports are identical on every
  report column.
* Recall amendments and phone-keyed reports never touch the fire reports' attributions.
