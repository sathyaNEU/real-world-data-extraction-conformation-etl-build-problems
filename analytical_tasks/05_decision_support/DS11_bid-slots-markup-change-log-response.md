# DS11 — Where a paving contractor spends next season's 46 bids, when the win rates at the new markups are measured, not modelled

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · public procurement and bidding |
| Mirrors | Allocating bid or sales effort across segments using the measured response to past price changes rather than a modelled one (Google and Amazon ad-auction bid changes with logged before-and-after win rates, cloud enterprise pricing desks, marketplace seller repricing) |
| Decision shape | An allocation under a cap: the estimating department's 46 bids across six letting classes next season |
| Committed call | Bids per class, and the expected realised profit of the plan, in $M to two decimals |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · measured #25's architecture (an effect the change log can measure, not assumed), under a reproduction clause, with a mixed segment split through a join (#6) at rung 2 |
| Gate G mechanism | method_or_model_selection, with binding_constraint |
| Measured traps engaged | #25 assumes an effect the log could measure · #6 treats a mixed segment all one way · #1 reports a failed back-test, ships anyway · #13 validates on one population, applies to another |
| Calibration form | Published control set with a reproduction clause: the board's bid-results report (wins by class for the last three seasons) and the planning standard's rule that a plan's win assumptions must reproduce it |
| Driving force | Next season's markups are up three points in resurfacing and two in bridge decks, so the plan needs win rates at prices the firm has not bid. The textbook model reads them off competitors' past bids and reproduces 11 of the board's 15 published win counts, missing every class-season that followed a markup change. The change log records those changes. Split by the pavement-warranty provision, a join to the contracts' special provisions, they show ordinary resurfacing wins collapsing (0.26 to 0.05), warranty resurfacing barely moving (0.52 to 0.50), and bridge decks holding at 0.30. No assumed elasticity produces that pattern. |

## 1. Situation

A highway paving contractor's estimating department can prepare 46 bids next season. The board has raised markups to 12% on resurfacing
(from 9%) and 14% on bridge-deck overlays (from 12%), and left the other classes unchanged. The agency's letting schedule lists next
season's lettings: 36 resurfacing (16 of them carrying a three-year pavement warranty in their special provisions), 10 bridge decks, 12
full-depth reconstructions, 20 intersection upgrades and 16 culvert replacements. The firm holds the agency's bid tabulations, its
closed-job cost reports, the change log of its own past markup changes, and the board's bid-results report. The chief estimator believes
resurfacing is the firm's bread and butter.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the tabulations, the cost reports, the
  change log, the board's report and the competitor-bid distributions behind the textbook model. The difficulty is that the plan needs win
  rates at new prices, the right ones were measured in the log, and the log's measurements split along a provision the tabulations do not
  carry.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chief estimator's view. The textbook model at the new markups, on realised margins and with warranty
  resurfacing split out, still spends 20 bids on ordinary resurfacing, and every figure ties to its source.
* **Instrument repair.** No file the ladder uses is suspect: the tabulations, cost reports, special provisions, change log and the
  board's report are complete and exact, and the warranty status sits correctly in the special provisions. Copying the provision onto the
  tabulations moves no rung (rung 0 bridge, full-depth and resurfacing; rung 1 bridge and resurfacing; rung 2 bridge, ordinary resurfacing
  and culverts), and the change-log measurement is still needed.
* **Lens swap.** The naive plan prices each class from competitors' past bids at the firm's past markups. The answer prices it from what
  happened after the firm moved its price: a different set of lettings, at a different moment.

## 3. The driving force

A strong solver builds win probability from the agency's tabulations: the distribution of the lowest competing bid relative to the
engineer's estimate, read at next season's markups. It replaces bid markup with realised margin, because won jobs overrun their estimates,
and it splits resurfacing on the warranty provision, because warranty claims cost five points of margin. Each step is competent. But the
textbook model assumes rivals' bids stay where they were when the firm moves its price, and the board's report refutes that. The model
reproduces 11 of 15 published class-season win counts, and its four misses are exactly the class-seasons after a markup change. The change
log records those changes. Joined to the special provisions, the before-and-after win rates split cleanly. In ordinary resurfacing, six to
nine rivals cluster just above the estimate, and a three-point increase cut wins from 0.26 to 0.05. Warranty lettings draw two bidders, and
wins went from 0.52 to 0.50. Bridge decks held at 0.30 after a two-point increase. Measured, not modelled, the plan drops ordinary
resurfacing and fills warranty resurfacing.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Expected profit per bid = textbook win probability × bid markup × contract value; resurfacing one class; fill 46 bids | Bridge 10, full-depth 12, resurfacing 24; $3.40M (+26%) | The textbook bid model on the agency's own tabulations | Closed-job cost reports: won jobs overran their estimates by 7.5 points in full-depth and 2.8 in resurfacing |
| 1 | Realised margins in place of bid markups (winner's curse) | Bridge 10, resurfacing 36; $2.37M (−12%) | Profit as the firm actually books it | Special provisions: 16 of the 36 resurfacing lettings carry the pavement warranty, and warranty claims cost 5.0 points |
| 2 | Resurfacing split on the warranty provision (#6) | Bridge 10, ordinary resurfacing 20, culverts 16; $2.27M (−16%) | Every margin now realised and risk-priced | The board's report: the textbook model reproduces 11 of 15 class-season win counts, failing every season after a markup change |
| 3 | **Decisive:** win probability at next season's markups measured from the change log's before-and-after seasons, by warranty status | **Bridge 10, warranty resurfacing 16, culverts 16, intersections 4; $2.71M** | — | — |

* **Figure shape.** The corrections walk the figure down (−30%, −4%), and the decisive move reverses them (+19%). Offsets from the answer:
  +26%, −12%, −16%.
* **Position.** Warranty resurfacing gets no bids at rungs 1 and 2 (it is the lowest class at rung 2) and 16 at rung 3. No intermediate
  rung's plan equals the answer, and the marginal class beats the first excluded one by at least 1.19× at every rung.
* **Discriminator dominance.** Ordinary resurfacing carries a 2.19× per-bid advantage over warranty resurfacing into rung 3 ($40.5k against
  $18.5k). Measured win rates move warranty resurfacing ×2.27 and ordinary resurfacing ×0.23, a relative swing of 10.0. Product: 0.46 ×
  10.0 = 4.6, which is where the pair ends ($42.0k against $9.2k).
* **Partial correction priced (L3).** Measuring the response from the log on resurfacing pooled (no warranty split) puts all 36
  resurfacing bids in the plan and claims $3.03M (+12%). Applying the measured rates to rung 2's plan without re-spending the bids delivers
  $2.10M (−22%).
* **Grid.** Warranty split (no, yes) × margin (bid, realised) × win rates (textbook, measured) gives 8 cells, each a different plan. The
  nearest wrong figures sit 12.1% above (pooled measured response) and 12.2% below (rung 1), each one omission away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The planning standard asks that win assumptions reproduce the board's report. No document says rivals respond to
   the firm's price, or that the response differs by warranty status.
2. **The reproducing rule is a construction, not a menu.** Measured win rates reproduce all 15 published class-season win counts within
   one win. The textbook model reproduces 11, over-predicting resurfacing after the increases and under-predicting bridge decks, 14% high on
   the total. The measurement has no parameter to scan. It is a before-and-after difference over the log's change seasons, taken separately
   for lettings whose special provisions carry the warranty, which needs a join the tabulations do not invite.
3. **No arithmetic symptom.** Lettings, bids, wins and margins reconcile to the tabulations, the cost reports and the board's report under
   every rung.
4. **Not a row predicate.** It needs the change log's seasons aligned to lettings, a join to special provisions, win rates grouped by
   class, season and warranty status, and a re-spent 46-bid plan.
5. **The enumeration is arithmetic.** No column holds a win rate at a new markup; the rates are computed from closed seasons.
6. **No cutover date.** The four changes sit in different classes and seasons, and the answer rests on their measured sizes, not on any
   one date.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The board's bid-results report: wins by class for each of the last three seasons, 15 published counts. The planning standard:
  a plan's win assumptions must reproduce them within one win.
* **What it pins.** Measured response over modelled. 15 of 15 against the textbook model's 11. A pooled measured response reproduces the
  report too, because the report pools resurfacing, so the warranty split is pinned by the cost reports (rung 2) and the twin pair, not by
  the report.
* **Twin pair.** Two resurfacing markup increases in the change log are identical on every log column: +3 points, districts of the same
  size, 22 lettings bid each, the same season. The win rates after are 0.095 and 0.21 (2.2×). One district's lettings were 10% warranty and
  the other's 35%. Only the special-provisions join separates them.
* **Every rule exercised.** The log holds two district resurfacing increases in one season (the twin pair), a firm-wide resurfacing
  increase the next season, a bridge increase, and a full-depth decrease whose wins rose by more than the textbook predicted (so the
  measured rule is not simply "rivals always undercut"). Those are the textbook's four missed class-seasons.
* **Resemblance points at the decoy.** On every tabulation column, next season's ordinary resurfacing looks like the two seasons in which
  resurfacing won most.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The board's decision: next season's markups by class. The planning standard: the estimating department prepares at most
  46 bids a season, bids go where expected realised profit per bid is highest, and win assumptions must reproduce the board's report. One
  sentence each.
* **Empirical pins.** Win rates at the new markups, from the change log. Warranty claims, from the cost reports.
* **Voices.** The chief estimator: "Resurfacing is our bread and butter; we bid all of it." The finance director: "Full-depth jobs are where
  the big margin dollars are." The board chair: "Our competitors don't watch our prices."
* **Licensed wrong basis.** The planning standard records that the firm's surety reviews bid plans on the textbook win model and will see
  that basis.

## 8. Determinism by construction

* **Change seasons.** Each logged change took effect on the first letting of a season, so before and after are whole seasons, with no
  partial-season fork.
* **Warranty status.** Every letting's special provisions either carry the warranty clause or do not, with no partial warranties.
* **Margins.** Overruns and warranty claims come from closed jobs only, so no open job's cost is estimated.
* **Integer bids.** Each class's lettings are filled whole, and only the last class is part-filled (intersections, 4 of 20). It beats the
  first excluded class by 1.19×.

## 9. Prompt sketch and deliverables

> We can put together 46 bids next season, and I need to decide where they go before the letting schedule opens. Our chief estimator says
> resurfacing is our bread and butter. Give me the number of bids for each class and the realised profit the plan should bring, in millions
> to two decimals, as the line for the board pack. Send `bid_plan.xlsx`, a chart `profit_per_bid.png`, and a one-page `board_pack.pdf`.

* `bid_plan.xlsx` — the plan under each construction, the bidders sheet (ask A), the notice-to-proceed sheet (ask B) and the reproduction
  sheet (ask C).
* `profit_per_bid.png` — the six classes' expected profit per bid under the four constructions as a dot plot, the 46-bid cut-off as a
  labelled line, the chosen plan's classes shaded, and the warranty and ordinary resurfacing win rates before and after their change
  annotated.
* `board_pack.pdf` — the committed plan and its profit, and why ordinary resurfacing gets no bids.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each class, the median number of firms bidding per letting over the last three seasons.
  *Device:* a joint-venture bid appears once in the tabulations, with its partners in the joint-venture table. Counting partner firms inflates
  the full-depth and bridge medians by one bidder.
* **Ask B (device-carried).** For each class, the mean days from letting to notice to proceed. *Device:* an amended contract re-issues the
  notice with a new date, and the contract-administration manual makes the first notice the operative one. Using the latest notice adds 9–14
  days in three classes.
* **Ask C (validity).** The 15 published win counts reproduced under the textbook and measured models, and expected profit per bid by class
  under each rung.
* **Decoupling.** Clearing the measured response and the warranty join changes no figure in asks A or B. Joint-venture partners and
  notices never enter a win rate or a margin.

## 11. Rubric arithmetic

6 classes (ask A) + 6 classes (ask B) + 2 hit counts + 6 × 4 per-bid values (ask C) + the plan (6 class counts) and its profit + 5 named
chart parts + 3 files ≈ 53 criteria.

## 12. World-building constraints

* Contract values ($M): resurfacing 2.0, bridge 3.5, full-depth 6.0, intersections 1.5, culverts 1.2. Overruns on won jobs (points):
  2.8, 0.9, 7.5, 1.0, 1.2. Warranty claims 5.0 points on warranty resurfacing.
* Textbook win rates at next season's markups: resurfacing 0.22, bridge 0.20, full-depth 0.16, intersections 0.19, culverts 0.24. Measured:
  ordinary resurfacing 0.05, warranty resurfacing 0.50, bridge 0.30, the others unchanged.
* Plans and figures: rung 0 $3.40M, rung 1 $2.37M, rung 2 $2.27M, answer $2.71M. The pooled measured cell claims $3.03M and the haircut
  delivers $2.10M.
* The twin increases are identical on every log column. Joint-venture rows and notices never touch lettings, wins or costs.
