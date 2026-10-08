# RC32 — Which borrowing programme the debt committee changes, when the average rate's post-peak rise is retail notes coming back early

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Economics · public debt management |
| Mirrors | Stock metrics that lag flow metrics when a block of the stock changes character as rates rise (a bank's book yield when term depositors break deposits early, SaaS ARR when contracts with exit clauses churn at renewal, an installed base on leases with early-termination options) |
| Decision shape | Which of N root causes gets the fix: the one borrowing programme the debt committee changes this year, among five |
| Committed call | The programme whose financing pushed the average rate on marketable debt up most in the twelve months after auction yields peaked, with each programme's contribution in basis points |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · S4 (the forward window generated under a regime the closed window never reached): the retail put is out of the money in every pilot year |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #12 stops at the first control that passes · #11 beats the headline trap, misses the quiet one |
| Calibration form | Pilot log: the retail Citizen Notes pilot, six series over three years, each with its filed coupon decision and redemption record |
| Driving force | Citizen Notes carry a holder's put at par after twelve months. In every pilot series the coupon stayed above the market yield, nobody put, and the pilot certified the notes as stable funding. After the peak, yields rose through the coupons and holders put €175B back. The debt office refinanced them through long-bond syndications, so in the marketable data the cost sits on the syndication programme, with nothing to say why. Only the monthly financing identity ties the syndications' rate effect to the retail redemptions. |

## 1. Situation

Auction yields on the country's debt peaked a year ago, yet the average interest rate on its €1.9T of marketable debt has risen 40 basis
points since. Legislators want to know why. The debt committee changes one borrowing programme each year: the bill programme, the regular
coupon auctions, inflation-linked issuance, long-bond syndications or the retail Citizen Notes. Its charter says the programme changed is
the one whose financing contributed most to the change in the average rate over the review window. The committee chair believes the office
is still paying top-of-market rates on everything it sells.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: security-level outstanding, auction results, syndication results, the published average
  rates by class, the retail programme statements and the pilot log. No one's reading of their own figures is overturned. The difficulty
  is which programme a rate effect belongs to.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice. The marketable data still show the rise concentrated in nominal coupons and the syndications, and
  the pilot still certifies the retail notes as stable.
* **Instrument repair.** Publish every security's rate perfectly. The syndications still carry the rise, and why they were sized as they
  were is a fact about the retail book's holders, not about measurement.
* **Lens swap.** The naive grain is the programme that issued the debt. The answer is the programme whose holders' behaviour created the
  need, which is a different population of securities, non-marketable notes.

## 3. The driving force

A strong solver rebuilds the average rate from the security-level data. It picks the construction the published class averages accept,
which is amount-weighted yields across reopenings. It splits nominal coupons by programme and finds the regular auctions merely
refinancing maturities, while syndications of long bonds at about 4.25% carry most of the rise. That is a satisfying, dated story: each
syndication steps the rate on its settlement day. But the syndications were not sized to a duration target. The regular calendar covered
maturities and the budgeted deficit, and the syndications met everything else. Everything else was the retail book. Citizen Notes are
puttable at par, and once yields passed their coupons, holders of five of the six series put €175B in eight months. The pilot never
showed this, because in every pilot series the coupon stayed above the market and the put was worthless.

## 4. The ladder

| Rung | Construction | Names (bp of the 40) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Flow reading: each programme's gross issuance × (issue yield − average rate) | Bill programme (18; syndications 9) | The briefing's comparison of new yields with the stock | Security-level outstanding: bills repriced before the peak, and the post-peak rise sits in nominal coupons |
| 1 | Stock reconstruction by class, on the construction the finer controls accept | Regular coupon rollover (33) | Reproduces the published total and every class average | The auction and syndication records split nominal coupon issuance by programme, and the regular auctions only refinanced maturities |
| 2 | Nominal coupons split by issuing programme | Long-bond syndications (24 against 9) | Dated, programme-level and exact, and each syndication steps the rate | The funding plan, retail statements and maturity calendar: syndications met needs beyond the calendar, and the only such need was €175B of Citizen Note puts |
| 3 | **Decisive:** each month's financing identity, with the syndications' rate effect booked to the need they met | **Citizen Notes (19 against 9)**, 5th on rung 0 | — | — |

* **Position table.** Citizen Notes rank 5th on rungs 0, 1 and 2 and lead only rung 3. Margins are 2.00, 8.25, 2.67 and 2.11.
* **Discriminator dominance.** Syndications carry a 24 bp lead over the retail notes into rung 3. The identity moves 19 bp from one to the
  other, a 38 bp swing, which is 1.58× the carried lead. The floor is 1.2×, so the edge has 1.32× headroom.
* **Partial correction priced (L3).** A solver who finds the puts but values them with the pilot's behaviour, as stable funding refinanced
  at maturity, books nothing to the notes and names syndications at 24 bp, 2.67× the regular auctions. One who books the puts at the notes'
  own coupons, the rate the government stopped paying, credits the notes with a fall and names syndications again, at the same 2.67×.
  Neither half names the notes.
* **Grid.** Reconstruction (coupon, first-auction yield, amount-weighted) × attribution (class, issuing programme, financing need) = 9
  cells. Only amount-weighted yields with need-based attribution names the notes. Under the coupon construction, bills lead every
  attribution.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The funding plan says the calendar covers maturities and the budgeted deficit. No document says the syndications
   financed retail puts, or that the puts were exercised because yields rose.
2. **Corpus blind for a computable reason.** *In every pilot series the coupon stayed above the market yield for the whole pilot, so no
   holder gained by putting and early redemptions were zero.* The pilot certifies the notes as stable funding six times of six.
3. **No arithmetic symptom.** Marketable outstanding, auctions, syndications and the published averages reconcile under every rung, and the
   retail statement ties to its own redemptions.
4. **Not a row predicate.** The link is a monthly identity: regular auctions against maturities and deficit, the residual need, then
   syndication volume matched to that need, then its rate effect apportioned.
5. **The enumeration is arithmetic.** No syndication record names its purpose. The match comes out of the identity.
6. **No cutover date.** Puts arrived as yields crossed each series' coupon, at different times. The dated syndications are the decoy.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The pilot log: six Citizen Note series issued over three years, each with the committee's filed coupon decision (the three-year
  yield plus 15 bp at issue) and its monthly redemption record.
* **What it certifies.** The notes' cost and behaviour as the shallow rungs assume them: coupon at issue reproduces every series' cost to
  the basis point, and redemptions are zero before maturity in all six.
* **What it is blind to.** Put exercise (property 2).
* **Twin pair.** Months M+4 and M+7 after the peak are identical on regular auction sizes and yields, maturities, bill share and deficit.
  The average rate rose 2.0 and 4.1 bp in them (2.05×). In M+7 a €26B syndication refinanced Citizen Note puts. Only the financing identity
  reproduces both months.
* **Resemblance points at the decoy.** The post-peak syndications match the pre-peak ones on tenor, book size and the "programme financing"
  line in the results file, and those earlier syndications served the long-bond duration target.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The committee charter: "The programme changed is the one whose financing contributed most to the change in the average
  rate on marketable debt over the review window." The funding plan: "The regular calendar is sized to maturities and the budgeted deficit;
  syndications meet any other financing need." Retail terms: "Notes may be redeemed at par on any coupon date after twelve months."
* **Empirical pins.** The average-rate construction comes from the published class averages. The residual need comes from the monthly
  identity.
* **Voices.** Committee chair: "We are still paying top-of-market rates on everything we sell." Head of portfolio strategy: "This is the
  pandemic notes rolling off, nothing more." Head of syndications: "Investors wanted duration and we gave it to them; that costs what it
  costs."
* **Licensed wrong basis.** The charter records that the national audit office attributes changes in the average rate by instrument class
  (bills, nominal coupons, linkers) and will present the review on that basis.

## 8. Determinism by construction

* **The identity closes.** In every month of the window the regular calendar equals maturities plus the budgeted deficit to within €0.5B,
  and syndication proceeds equal Citizen Note puts to within €1B, so the attribution has no slack.
* **Construction.** Coupon, first-auction and amount-weighted yields all reproduce the published total within 1 bp. Only amount-weighted
  yields reproduce the note, bond and linker class averages within 0.5 bp. The others miss by 6 to 11 bp.
* **Apportionment.** The committee's decomposition rule (security-level contribution to the change in the outstanding-weighted rate) is
  fixed in the charter's annex, so programme shares do not depend on order.
* **Maturity.** Every put in the window settled, and every syndication priced and settled, before the review date.

## 9. Prompt sketch and deliverables

> The debt committee changes one borrowing programme this year, and I have to tell legislators which one and why the average rate kept
> climbing after yields peaked. The chair is sure we are still paying top-of-market rates on everything we sell. Tell me which programme's
> financing pushed the average rate up most, as a sentence for the committee, with each programme's contribution in basis points to one
> decimal. Send `rate_rise_attribution.xlsx`, a chart `rate_rise_by_programme.png`, and a one-page `committee_brief.pdf`.

* `rate_rise_attribution.xlsx` — the five programmes on every construction, the auction sheet (ask A), the cash sheet (ask B) and the
  construction check (ask C).
* `rate_rise_by_programme.png` — monthly average rate over the window with contributions stacked by programme. Syndication dates and
  cumulative Citizen Note puts are marked, the peak month carries a labelled reference line, and the title names the programme.
* `committee_brief.pdf` — the named programme and why the other four fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight regular auction tenors, the window's average bid-to-cover and average tail in
  basis points. *Device:* the results file's tendered amount includes the central bank's non-competitive rollover in flagged auctions, and
  the auction rules exclude it from cover. Including it overstates cover in the three tenors the central bank rolls into. Auction cover
  never enters the attribution.
* **Ask B (device-carried).** For each month, the debt office's end-of-month cash balance and its days of cover against the next month's
  outflows. *Device:* the central bank's overnight sweep posts as a separate same-day credit, as the account statement's notes state.
  Reading only the balance line understates cash in every month-end the sweep ran.
* **Ask C (validity).** For each of the three average-rate constructions, its fit to the published total and to each class average.
* **Decoupling.** Clearing the financing identity changes no figure in asks A or B. Ask C runs before any attribution.

## 11. Rubric arithmetic

8 tenors × 2 measures (ask A) + 12 months × 2 measures (ask B) + 3 constructions × 4 targets (ask C) + the named programme, five
contributions and the winning margin + 5 named chart parts + 3 files ≈ 67 criteria.

## 12. World-building constraints

* Marketable debt is €1.9T at a 2.0% average before the peak, and the rise over the window is 40 bp. True contributions are Citizen Notes
  19, regular rollover 9, syndications 5, linkers 4 and bills 3.
* Citizen Note puts total €175B over eight months, across five of six series, and are refinanced through syndications at about 4.25%.
* Every pilot series kept its coupon above the market yield, with zero puts.
* M+4 and M+7 are identical on every column of the monthly report except the €26B syndication.
* Rung leaders are bills, regular rollover, syndications and Citizen Notes, with margins of at least 2.00.
* Central-bank rollover flags and sweep postings never touch outstanding, yields or retail statements.
