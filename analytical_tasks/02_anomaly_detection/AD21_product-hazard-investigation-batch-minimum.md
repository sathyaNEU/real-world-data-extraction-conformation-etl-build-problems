# AD21 — Which product and hazard get the regulator's one full engineering investigation, when the worst rate belongs to one bad production batch

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · consumer product safety regulation |
| Mirrors | Telling a design flaw from a bad batch before committing an engineering investigation (field-failure triage at Apple and Google, where one supplier lot can dominate a model's return rate, marketplace safety teams separating a listing's bad shipment from a bad product, automaker recall engineering) |
| Decision shape | Which of N gets one scarce thing: next quarter's single full engineering investigation in the regulator's test laboratory |
| Committed call | The one product–hazard pair investigated, and its design rate: the lowest of its batch rates per 100,000 units |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · a minimum over sub-units (E30): a design hazard is the rate a pair shows in every production batch, each report placed in its batch through its purchase quarter and the shipment register; the price-list attribution of blank reports and the retailers' SKU join (E20) at the lower rungs |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #7 uses the ready-made measure · #17 guesses an attribution the data can settle · #18 joins only on the visible key |
| Calibration form | Retry or revision log: the case-version log of every report, in which each of the laboratory's 16 closed investigations records its finding as the final version of its cases, and 1,240 blank reports carry the model a follow-up supplied |
| Driving force | The investigation is for hazards of design; a hazard confined to a production batch goes to the recall desk. Every careful build ranks pairs on reports per 100,000 units, and once blank reports are placed through the retailers' price lists the K-200 kettle leads at 60. But 84% of its fires come from units of one quarterly batch, whose thermostat supplier changed. A design hazard is the rate a pair shows in every batch: each report placed in its batch through its purchase quarter and the shipment register, each batch's rate taken on its own production volume, and the minimum kept. The T-9 toaster's crumb-tray fires run at 29 to 33 per 100,000 in every batch, and only that law reproduces the laboratory's closed findings. |

## 1. Situation

A national product-safety regulator's laboratory can run one full engineering investigation next quarter, on one product–hazard pair.
The surveillance policy sends it to the pair with the highest rate of reports per 100,000 units sold over the last four quarters, counting
each case once at its latest version, and reserves it for hazards of design: a hazard confined to a production batch goes to the recall
desk. The pack carries the report database with every case version, the market data's units sold by model, the retailers' monthly price
lists and SKU catalogues, the manufacturers' production registers (units by quarterly batch), their shipment registers, and the revision
log.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each report as filed and as revised, the sales, the price lists, the production and shipment
  registers and every closed finding. The K-200's rate really is the highest. Nothing reported is overturned; the difficulty is which rate
  a design hazard has.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices. Counting cases at their latest version, every report attributed to its model, still names the
  K-200.
* **Instrument repair.** Suspect files: the report database's model field, blank on 41% of fire reports, and its superseded case versions.
  Repaired, every report names its model at its latest version: rungs 0 to 3 all name the K-200, and the batch construction is still
  needed to reach E. Purchase dates, the production and shipment registers and the price lists are complete, and a report that named its
  model would still not say whether its hazard is the design's or the batch's.
* **Lens swap.** The naive rate pools a pair's units across batches; the answer's is the rate in the batch where the pair is least
  hazardous, a different population of units for every pair, a thirteenth of the K-200's pooled figure would hold in its other batches.

## 3. The driving force

A strong solver drops superseded case versions as the policy says, joins retailer reports to models through the retailers' SKU catalogues,
and places the blank reports, which record retailer, month and price paid, through the price lists, where no two models shared a price at a
retailer in a month; the revision log's 1,240 follow-ups confirm every assignment. The K-200 kettle leads at 60 per 100,000. Each step is
right. But the laboratory investigates design hazards, and a batch defect goes to the recall desk. The K-200's fires sit 84% on units of
the second-quarter batch, built with a substitute thermostat; its other three batches run at 12 or 13. A design hazard is in every batch,
and its rate is the one every batch shows: the minimum over batches. Each report's batch follows from its purchase quarter, because every
batch shipped and sold within the quarter after it was built, and each batch's rate is its reports over its own production volume. On that
law the T-9 toaster, whose crumb-tray fires run at 29 to 33 per 100,000 in every batch, leads at 29.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Reports per 100,000 units for each pair, every row in the database, by the model field | A, K-100 kettle and scalds (41; 1.24× B) | The database's own counts on the policy's rate | The policy counts each case once at its latest version, and the revision log shows A's cases filed in up to five versions |
| 1 | Hygiene: each case at its latest version, linked by the model field | B, H-12 heater and fire (29; 1.21× C) | Clean case counts on the policy's basis | The retailer reporting guide: retailers file under their own SKU, and their reports carry no model field |
| 2 | Retailer reports joined to models through the retailers' SKU catalogues | C, C-7 charger and fire (36; 1.24× B) | Every report with an identifier linked, no guess made for the rest | The revision log: 1,240 reports filed with no model were later completed by follow-ups, every one matching the retailer's price list for its month |
| 3 | Blank reports assigned through the retailer's price list for the month they record | D, K-200 kettle and fire (60; 1.62× C) | Every report attributed exactly, the policy's rate on its own terms | The production and shipment registers: 84% of the K-200's fires are on units of the second-quarter batch, built with a substitute thermostat, and the policy sends batch hazards to the recall desk |
| 4 | **Decisive:** each pair's batch rates, reports placed in batches by purchase quarter through the shipment register over each batch's production volume, and the lowest kept | **E, T-9 toaster and fire (29)** (5th of 8 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (18) and 4th on rungs 1, 2 and 3 (17, 20 and 31), and leads only rung 4, 1.45× B (20).
  Intermediate leaders hold margins of 1.24×, 1.21×, 1.24× and 1.62×.
* **Discriminator dominance.** D carries a 1.94× advantage over E into rung 4 (60 against 31). The batch minimum keeps 0.94 of E's rate and
  0.20 of D's, an edge of 4.68 against the 1.2 × 1.94 = 2.32 required, 2.0× headroom.
* **Partial correction priced (L3).** A solver who screens out pairs with more than half their reports in one batch and ranks the rest on
  the pooled rate names C (37 against E's 31, 1.19×), whose two bad batches stay under the screen. A solver who takes the median batch rate
  names C (40.5 against B's 36). A solver who places reports in batches by report date instead of purchase quarter smears the K-200's bad
  batch across four quarters and names D again (45 against E's 30). No half lands on E.
* **Grid.** Attribution (model field, plus SKU, plus price list) × batch law (pooled, concentration screen, median, minimum) × batch dating
  (report date or purchase quarter): pooled cells name A to D by attribution, the screen and the median name C, report-date minimums name D.
  Only the minimum by purchase quarter on fully attributed reports names E, and the nearest wrong cell (C) needs only the screen in place
  of the minimum.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy separates design hazards from batch hazards in words. Nothing says how, and the production and shipment
   registers sit in the manufacturers' technical files for traceability.
2. **The corpus pins a construction, not a menu.** The minimum batch rate reproduces all 16 closed findings: design hazards at 20 or more
   per 100,000 in every batch, batch defects at 14 or less in some batch, nothing between. The pooled rate reproduces 9, the concentration
   screen 12 and the median 11, every rival calling some batch defect a design hazard. The law is a construction: reports placed in batches
   through a register they never cite, rates per batch, and a minimum, with no column carrying a design rate.
3. **No arithmetic symptom.** Cases reconcile to versions, attributions to the follow-ups, batch volumes to the market data's annual
   totals; every rung reconciles.
4. **Not a row predicate.** It needs each report's purchase quarter mapped to a batch, each batch's reports divided by its production
   volume, and a minimum per pair over its batches.
5. **The enumeration is arithmetic.** Each pair's design rate is computed; no field marks a hazard as design or batch.
6. **No cutover date.** The substitute thermostat went into one batch, and the dated batch sits under the decoy; E's fires run level
   through every batch.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The revision log: every version of every report over four years, among them the final versions recording the findings of the
  laboratory's 16 closed investigations, and 1,240 reports filed without a model whose model a follow-up later supplied.
* **What it pins.** The minimum-over-batches law, 16 of 16 findings, with an empty band between 14 and 20 per 100,000; the price-list
  attribution, 1,240 of 1,240.
* **Twin pair.** Closed investigations P-03 and P-11 are identical on pooled rate (24 per 100,000), reports, units sold, category and
  region mix. P-03 was found a design hazard and P-11 a batch defect: their lowest batch rates were 22 and 11 (2×). Only the batch law
  separates them.
* **Every rule exercised.** One closed pair had a batch that sold over two quarters, so the shipment register's dates are tested; one had
  three bad batches of four, so a high median with a low minimum is tested.
* **Resemblance points at the decoy.** By pooled rate and report profile the K-200 most resembles P-03, the corpus's clearest design hazard.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The surveillance policy: the investigation goes to the pair with the highest rate of reports per 100,000 units sold over
  the last four quarters, each case counted once at its latest version; it is for hazards of design, and a hazard confined to a production
  batch goes to the recall desk. The market data's units sold by model and quarter.
* **Empirical pins.** The minimum-over-batches law, from the closed findings; the price-list attribution, from the follow-ups.
* **Voices.** The head of market surveillance: "We act on what consumers tell us about named products." The laboratory manager: "K-100
  scalds fill our inbox every week."
* **Licensed wrong basis.** The policy records that the manufacturers' trade association ranks pairs on the pooled rate of named reports and
  will present its rates at the planning review.

## 8. Determinism by construction

* **Batches.** Every batch shipped and sold within the quarter after it was built, so purchase quarter names the batch exactly; no report
  falls in a quarter boundary week.
* **Prices.** In every retailer-month, every model in a category sold at a distinct price, so each blank report has one model.
* **Versions.** Version numbers are unique within a case, so the latest version is a key maximum.
* **Window and volumes.** Four quarters by report date; batch volumes from the production registers sum to the market data's units sold.

## 9. Prompt sketch and deliverables

> Our test laboratory has one full engineering investigation next quarter, and it goes to one product and one hazard. The head of market
> surveillance acts only on reports that name a product. Tell me the pair and the rate that puts it there, in a sentence for the
> surveillance plan, with `investigation_choice.xlsx` holding the sheets below, the chart `batch_rates.png`, and
> `surveillance_plan_note.docx`.

* `investigation_choice.xlsx` — the pair build with every report's attribution route and batch, the recall sheet (ask A), the channel sheet
  (ask B) and the findings back-test (ask C).
* `batch_rates.png` — each pair's four batch rates as dots on one row, the pooled rate as a tick and the minimum ringed, the K-200's
  second-quarter batch labelled, and the twin closed pairs as an inset.
* `surveillance_plan_note.docx` — the committed pair, its design rate, and why the pooled ranking and its leader are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the ten product categories, recall notices in the last two years and the median days
  from first report to recall. *Device:* a recall extended to further batches is published as an amendment under a new notice number
  linked to the original, per the recall register's notes. Counting notices overstates recalls in the four categories with extensions. The
  investigation build never reads the recall register.
* **Ask B (device-carried).** For each of the nine regions, reports filed in the last four quarters and the share filed by phone.
  *Device:* phone reports are keyed by call-centre staff into the web form, so they carry the web channel and a staff ID in the submitter
  field, per the intake guide. Reading the channel field alone understates phone reports everywhere.
* **Ask C (validity).** For each of the five rung constructions and the two batch screens (concentration and median), the closed findings
  it reproduces out of 16.
* **Decoupling.** Clearing the batch construction changes no figure in asks A or B.

## 11. Rubric arithmetic

10 categories × 2 (ask A) + 9 regions × 2 (ask B) + 7 constructions (ask C) + the committed pair, its design rate and the margin over B + 5
named chart parts + 3 files ≈ 56 criteria.

## 12. World-building constraints

* Rung leaders are A, B, C, D, E. E is 5th / 4th / 4th / 4th / 1st; intermediate margins are at least 1.21×; E leads rung 4 by 1.45×.
* Batch rates per 100,000: A 17–19, B 20–40, C 12–55, D 202 in the second-quarter batch and 12–13 in the others, E 29–33. Minimums: E 29,
  B 20, A 17, C 12, D 12.
* 41% of fire reports carry no model and no SKU; 455 match the K-200 by price; no two models share a price at a retailer in a month.
* The revision log holds 16 closed findings and 1,240 follow-up attributions; P-03 and P-11 are identical on every pooled column.
* Recall amendments and phone-keyed reports never touch the fire reports, their batches or the registers.
