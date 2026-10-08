# RC27 — How many points of the star summary the Carrow retiree group cost, when a third of the group is reachable only through billing accounts

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · health-plan quality regulation |
| Mirrors | Account-quality scores banded against the peer field after a book of accounts is absorbed (Amazon seller performance after a seller takes over another storefront, Google Workspace domain health after a merger, app-store quality tiers after a publisher acquires a catalogue), where part of the absorbed book links to it only through a shared billing account |
| Decision shape | One figure committed at a date (a component): the share of the summary-score drop the Carrow group caused, filed before the renewal decision |
| Committed call | The points of this year's star summary the Carrow group cost, to two decimals, stated in the board paper on the Carrow renewal |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · S1 (the group the board means is not the roster the account team keeps), graded as a component, not as a correction |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #18 joins only on the visible key · #24 treats an unpublished figure as unknown · #11 beats the headline trap, misses the quiet one |
| Calibration form | Gold-standard verification subsample: the regulator's validation audit of 450 member records, each verified against source documents |
| Driving force | The Carrow group is the 9,000 retirees on the account team's roster plus 5,200 spouses enrolled in individual plans under their own member IDs. The spouses reach Carrow only through the retirees' family-tier billing accounts. The roster matches Carrow's eligibility file to the member, so it looks complete. The spouses sit in the denominator of the one triple-weighted measure the group pushed below a cut point, so a roster-only counterfactual misses most of what the group cost. |

## 1. Situation

Larkfield Health Plan's overall star rating fell from 4.5 to 4.0. Its unrounded summary dropped from 4.37 to 4.18, under the 4.25 line,
and took the quality bonus on next year's benchmark with it. At the start of the measurement year Larkfield took on the Carrow Steel retiree
group from another carrier. The Carrow contract is up for renewal, and the board decides on the 3rd whether to bid for it again. The CFO says
Carrow cost the bonus. The quality director says the field improved and the cut points rose. The board wants one figure: the summary points
the Carrow group cost this year.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the published measure scores, the cut points, the survey vendor's report, the group roster,
  the billing accounts and the audit. Both stakeholders are right. Carrow cost the bonus, and the cut points did rise. The task quantifies
  the CFO's cause and corrects no one's reading of their own numbers.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice. The roster still matches the eligibility file exactly, and the natural counterfactual removes
  9,000 people.
* **Instrument repair.** Suspect: the vendor's group table, where Carrow's survey cell is suppressed, and the audit, which samples only
  members enrolled for two years. Repair: publish the cell and audit a random sample of all members. Rung 0 still returns 0.13, rung 1 rises
  to 0.11 because the survey measures can now be re-starred, and rung 2 stays at 0.11; none reaches 0.18. The roster is not suspect: it
  lists Carrow's retirees exactly as Carrow's eligibility file does, a different attribute from the lives Carrow pays for, and no member
  record carries a group field. The group is built from complete enrolment and billing-account records, so that construction is still
  needed.
* **Lens swap.** The roster counterfactual and the answer remove different populations, 9,000 lives against 14,200, and they flip
  different measures.

## 3. The driving force

A strong solver does not argue about cut points. It builds the counterfactual. It drops Carrow's members from the audited member-level
measure output, re-stars every measure against this year's cut points and recomputes the summary. It takes Carrow's members from the
account team's roster, which matches Carrow's eligibility file member for member. That roster lists retirees. Carrow also pays a premium for
5,200 spouses, who enrolled in Larkfield's individual plans under their own member IDs. Their premiums are billed to the retirees'
family-tier accounts, as the billing guide documents, and nothing on a spouse's member record names Carrow. The spouses are concentrated in
the denominator of the triple-weighted review-completion measure, and Carrow's drag pushes that measure under its 4-star cut point. Removing
the roster alone leaves it there. Removing the whole group lifts it back.

## 4. The ladder

| Rung | Construction | Lands on (summary points Carrow cost) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The rating bridge: re-star this year's scores on last year's cut points, and book the own-performance part to Carrow | 0.13 (−29%) | The standard star bridge, read the CFO's way | The audited member-level output shows the original book's rates rose on four measures, so own performance is not Carrow |
| 1 | Counterfactual without the 9,000 roster retirees, admin measures re-starred. The survey measures are held because Carrow's survey cell is suppressed | 0.05 (−71%) | Member-level, audit-certified, and honest about what is unpublished | The vendor's group table publishes the group-segment total and the Brede and Ostrander cells with their completes, which pin Carrow's cell |
| 2 | The suppressed cell bounded: Carrow's survey cell solved from the published group total and the other two groups' cells, survey measures re-starred | 0.11 (−43%) | Every measure attributed, every control ties, and the survey's Carrow segment matches the roster's | The family-tier billing accounts carry 5,200 spouses whose premiums Carrow pays, enrolled under their own member IDs |
| 3 | **Decisive:** the group taken as every life Carrow pays a premium for (roster plus billing-linked spouses), all measures re-starred | **0.18** | — | — |

* **Figure shape.** Each rung above rung 1 adds Carrow members or Carrow measures, so the answer is the maximum cell of the grid and every
  partial application understates it. Without Carrow the summary would be 4.37, last year's figure, and the plan would have kept 4.5 stars.
* **Partial correction priced (L3).** A solver who looks for spouses by shared surname and address finds 2,300 of the 5,200. It also adds
  1,900 members of the retirement communities where Carrow retirees cluster. That moves no measure across a cut point, so it lands on rung
  2's 0.11, no nearer the answer.
* **Grid.** Method (bridge or counterfactual), then identification (roster, address-matched, billing-linked) × survey (held or solved) = 7
  cells. The nearest wrong cells are 0.13 (−29%): the bridge, and billing-linked spouses with the survey cell left unsolved. Every star flip
  is worth at least 1/38 of a point, 14% of the answer, so no rounding drift can close a gap.
* **Which guard binds.** A figure with no ranking, so separation binds. Per-rung offsets are −29%, −71%, −43%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The billing guide describes premium billing. No document connects billing accounts to quality measures, and no
   spouse record names Carrow.
2. **Corpus blind for a computable reason.** *In every audited record the member had been continuously enrolled for the two years before
   the measurement year, which is the audit's sampling rule, so no Carrow life, retiree or spouse, can appear in it.* The audit certifies the
   member-level build 450 of 450 and is silent on who belongs to a group.
3. **No arithmetic symptom.** The roster ties to Carrow's eligibility file, the member-level output reproduces every published score, the
   survey cells reconcile to the group total, and the spouses' premiums tie to billing.
4. **Not a row predicate.** Membership is a property of the billing account (account → covered lives), and the effect needs every measure's
   counterfactual re-starred against this year's cut points.
5. **The enumeration is arithmetic.** Which measures flip is computed. No member record carries a group field; the group exists only in
   the roster and the billing accounts.
6. **No cutover date.** Carrow's arrival and the cut-point rise hit the same rating year. No series separates them.
7. **Survives deletion.** Removing every voice leaves the roster as the obvious list.

## 6. The calibration corpus

* **Form.** The regulator's validation audit: 50 members for each of the nine member-level measures, each verified against source
  documents and filed with its numerator status.
* **What it certifies.** The member-level build. The audited measure output reproduces 450 of 450 verified statuses and every published
  score. The plan's dashboard extract, which counts any enrolled month instead of the full lookback, matches 402 of 450.
* **What it is blind to.** Group membership (property 2).
* **Twin pair.** Individual plans PBP 012 and PBP 015 are identical on enrolment (11,800), region mix and last year's composite admin rate
  (71.4%). Neither holds a roster retiree. Their composite rates fell 1.6 and 3.3 points, 2.06× apart. They hold 1,700 and 3,500 Carrow
  spouses, which only the billing link reveals.
* **Free training instance (O3).** The survey vendor segments members by billing account, so its Carrow cell already includes the spouses.
  The pattern is visible there and harmless, because the cell is solved from the group total either way.
* **Resemblance points at the decoy.** The only group lives in the audit are 61 Brede Foods retirees, enrolled for years, and they verified
  at the original book's rates. By resemblance, a retiree group costs little.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The group-business policy: "A group's book is every life the group pays a premium for." The regulator's technical notes
  fix the weights, the cut points and the rounding of scores to whole points before starring.
* **Empirical pins.** The member-level build comes from the audit. Carrow's survey cell comes from the vendor's group table.
* **Voices.** CFO: "Carrow's retirees came from a carrier that never chased a gap; they cost us the bonus." Quality director: "Every plan in
  the region got better at once. The cut points did this." Group account manager: "Carrow is nine thousand retirees, and they're the
  best-documented group we have."
* **Licensed wrong basis.** The plan's quality policy records that the regulator's account team explains rating changes with the
  own-performance and cut-point bridge, and will present Larkfield's drop on that basis at the bonus review.

## 8. Determinism by construction

* **Cut points and rounding.** Every counterfactual score sits at least 0.4 points from the nearest cut point after whole-point rounding, so
  no tie rule matters.
* **Survey solve.** The vendor publishes unadjusted segment means with completes, so the group total is exactly the completes-weighted mean
  of its three cells, and Carrow's cell (164 completes) solves exactly.
* **Spouse link.** Each family-tier account lists its covered member IDs, and no member appears on two accounts.
* **Enrolment.** Every Carrow life, retiree or spouse, starts on the first day of the measurement year. None left before year-end, so
  continuous-enrolment rules treat the group identically under any reading.
* **Reward factor.** The plan earned none in either year, so it cannot move the summary.

## 9. Prompt sketch and deliverables

> The board meets on the 3rd to decide whether we bid for the Carrow renewal, and I have to give them one number: how many points of this
> year's star summary the Carrow group cost us, to two decimals. Our CFO is convinced Carrow alone cost us the bonus. Put the figure in a
> sentence I can lift into the board paper, and send `carrow_effect.xlsx`, a chart `measure_flips.png`, and a one-page `renewal_note.pdf`.

* `carrow_effect.xlsx` — the counterfactual build by measure, the appeals sheet (ask A), the call-centre sheet (ask B) and the audit
  back-test (ask C).
* `measure_flips.png` — a dot plot of every rated measure's score with and without Carrow, against this year's 3-, 4- and 5-star cut
  points. Triple-weighted measures are marked, the flipping measures annotated, and the title states the points Carrow cost.
* `renewal_note.pdf` — the committed figure and what the summary would have been without the group.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each month of the measurement year, the share of standard and of expedited reconsideration
  appeals decided within their deadline. *Device:* approved extensions sit in a separate extension table keyed on the case, as the appeals
  manual documents. Measuring raw days marks 9% of standard cases late and drops two months under the measure's 4-star cut. Appeals touch no
  member-level measure.
* **Ask B (device-carried).** For each month, the share of member-services and pharmacy help-desk calls answered within 30 seconds. *Device:*
  the telephony export writes each transferred call as legs under one call-chain ID. Counting legs as calls overstates fast answers in the
  pharmacy queue by about a sixth.
* **Ask C (validity).** For each of the nine member-level measures, the compliant count among its 50 audited members under your build,
  beside the auditor's verified count.
* **Decoupling.** Clearing the Carrow construction, spouses or roster, changes no figure in asks A or B. Ask C contains no Carrow life.

## 11. Rubric arithmetic

12 months × 2 appeal types (ask A) + 12 months × 2 queues (ask B) + 9 measures (ask C) + the committed figure, the four flipping measures and
the no-Carrow summary + 5 named chart parts + 3 files ≈ 72 criteria.

## 12. World-building constraints

* Measure weights total 38: 3 triple-weighted and 6 single-weighted member-level measures, 4 double-weighted survey measures and 15 points
  of operational measures. Summary point totals are 166 last year, 159 this year and 166 without Carrow.
* In weight-points, the drop splits into cut points −2, Carrow −7 and original book +2. The bridge's own-performance part is −5.
* Roster-only removal flips two single-weight measures. The survey solve flips one double-weight measure. Removing the spouses as well
  flips the triple-weighted review-completion measure.
* Carrow is 9,000 roster retirees plus 5,200 billing-linked spouses, 14,200 of 52,000 members. PBP 012 holds 1,700 spouses and PBP 015
  holds 3,500, and the two plans are otherwise identical.
* Carrow's survey cell has 164 completes, under the vendor's 200 floor. The group segment totals 606 completes with Brede (230) and Ostrander
  (212).
* Audit: 450 records, all continuously enrolled for two years, 61 of them Brede retirees. Appeal extensions and call legs never touch
  member-level rows.
