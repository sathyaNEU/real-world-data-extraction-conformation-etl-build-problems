# AD25 — One forensic team, eight flagged contracting authorities: every red flag is explained, and the rigging shows on no screen

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · public procurement oversight |
| Mirrors | Integrity teams choosing where to send scarce investigators when every dashboard flag has a legitimate explanation (marketplace seller-collusion rings, coordinated review or engagement rings at Meta and Google, supplier bid rotation in hardware sourcing) |
| Decision shape | Which of N gets one scarce thing: the forensic team's twelve-month engagement |
| Committed call | The one authority whose next twelve months of tendering the team investigates |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · S7, every screen is right and the answer is what nothing flags, with Pattern B (the casebook pins the construction) |
| Gate G mechanism | method_or_model_selection, with signal_vs_noise_or_hold support |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #4 never tests its reading against the control · #18 joins only on the visible key |
| Calibration form | Existing-book actuals: the casebook of 30 closed investigations with their findings and investigated tender years |
| Driving force | The five monitor flags are each produced by documented, legitimate purchasing structures. Rigging lives at a grain the monitor cannot express: supplier pairs that keep co-bidding across lots and take turns to win. That is a construction across lots, and only it reproduces the closed casebook. |

## 1. Situation

The national audit office has one forensic team for next year. The screening committee shortlisted eight contracting authorities from the
office's red-flag monitor. The monitor's export reports five flags per authority, each a correct measure of the past four years: single-bid
share, short advertisement periods, non-open procedures, contract values just under thresholds, and repeat-winner share. The committee chair
wants the team sent to the authority with the strongest flag profile. The office's audit manual says the team goes where rigging is ongoing.

## 2. Gate G: why this is legal

* **Litmus.** Every flag is computed correctly and is labelled in-file as a measure of past exceedance, not a referral ranking. Every high
  flag has a documented, legitimate cause. Nothing reported is wrong, and the task is not to refute the monitor. It is to find a population
  the monitor's grain cannot express.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chair's preference and the monitor export itself. The tender and bid records still hide the ring at pair
  grain, and the natural authority-level analyses still miss it.
* **Instrument repair.** Recompute every flag perfectly; they are already correct. No better authority-level instrument reveals pair-level
  rotation.
* **Lens swap.** The flags describe authorities' purchasing profiles. The answer is a set of supplier pairs operating inside one authority:
  a different population.

## 3. The driving force

A strong solver ranks authorities on flags, adjusts for case mix, and weighs recency, and each step is competent. Rigging by rotation,
though, leaves authority-level rates looking normal. Tenders get several bids, procedures are open, and no supplier dominates. What betrays
it is a pair structure. The same six suppliers co-bid in lot after lot, the winner rotates in a fixed cycle, and the losing bids sit a
narrow, consistent margin above the winner. Seeing it means building the supplier-pair × lot table, which nothing in the pack invites. The
casebook's findings are reproduced by that construction and by none of the authority-level screens.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Composite of the five flags (standardised, equal weight) | A, a university hospital | The monitor is the office's own tool, and the composite is its natural summary | The casebook: composite rank reproduces 11 of 30 closed findings |
| 1 | Single-bid excess over the share expected from each authority's CPV-category × procedure mix | B, a port authority | The textbook correction for specialised buyers, and it removes the hospital | The casebook: 15 of 30 reproduced; specialised suppliers explain B's excess in the supplier register |
| 2 | Repeat-winner concentration in the last four quarters, adjusted for framework agreements | C, a regional roads agency | Captures ongoing favouritism and is recency-aware | The casebook: 21 of 30; C's concentration is one framework holder serving a mandated call-off contract |
| 3 | **Decisive:** rotation at supplier-pair grain — pairs co-bidding in at least 9 lots, with alternating wins and stable loser markups — still active in the latest two quarters | **E, a metropolitan housing authority** (5th of 8 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0, 4th on rung 1 and 3rd on rung 2, never leading an intermediate rung. Each rung's leader beats
  its runner-up by at least 1.25×.
* **Partial correction priced (L3).** A solver who builds pair-grain co-bidding but drops the active-in-the-latest-two-quarters test names F,
  a water utility whose ring dissolved two years ago when two members exited. That case is closed, and further from the answer than rung 2,
  because the audit manual sends the team where rigging is ongoing.
* **Grid.** Flags (composite or adjusted) × recency (all years or latest quarters) × grain (authority or supplier pair) = 8 cells. Every
  non-answer cell names A, B, C or F, and only pair grain with recency names E.
* **Discriminator dominance.** C carries a 1.4× advantage on repeat-winner concentration into rung 3. E's ring covers 31% of its lots by
  value against C's 0%, an edge far beyond 1.2 × 1.4.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The audit manual lists generic red flags and says the team goes where rigging is ongoing. Nothing mentions pairs,
   rotation or markups.
2. **No sweepable menu nominates it.** The casebook pins the construction only for a solver who builds pair-grain features. Every menu
   screen a solver can sweep (the five flags, their combinations, case-mix and recency variants) tops out at 21 of 30.
3. **No arithmetic symptom.** Bids reconcile to award notices, lots to tenders and suppliers to the register. No duplicate keys, no
   fan-out.
4. **Not a row predicate.** It needs a self-join of bidders within lots, aggregation to pairs, a within-pair ordering of wins over time and
   a markup ratio per lot.
5. **The enumeration is arithmetic.** Ring membership is computed. Ordinary pairs co-bid at most 5 times in four years and ring pairs 9 to
   14 times, with nothing in between, so the membership is the same at every co-bid threshold from 6 to 9.
6. **No cutover date.** The ring has run for four years with no step in any series.
7. **Survives deletion.** Removing every voice and the monitor export leaves the answer unchanged and the difficulty intact.

## 6. The calibration corpus

* **Form.** The casebook: 30 closed investigations, each with its authority's tender, lot and bid records for the investigated year and a
  finding (collusion confirmed or not).
* **What it pins.** The pair-rotation construction reproduces 30 of 30 findings. The best rival, repeat-winner concentration, reproduces 21
  of 30. The rivals' misses run in one direction (they all call confirmed cases clean), so no rival reconciles in aggregate either.
* **Twin pair.** Cases 2019-07 and 2020-03 are identical on all five flags, the case-mix excess, authority type, region and lot count.
  2019-07 confirmed collusion and 2020-03 did not, separated only by pair-grain rotation.
* **Every rule exercised.** One confirmed case has co-bidding without alternating wins (so co-bidding alone is not enough). One clean case
  has alternating wins between two framework holders on mandated call-offs, and the alternation stops when the framework is excluded.
* **Resemblance points at the decoy.** E's authority type and flag profile most resemble five clean closed cases.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The audit manual sets the purpose (the team investigates where rigging is ongoing over the engagement year) and the
  casebook's status as the office's record of findings. One sentence each.
* **Empirical pins.** The co-bid cut-off and the markup band come from the absolute split and the casebook, with nothing chosen.
* **Voices.** The committee chair: "Single-bid share has always been our best predictor." The regional auditor: "Hospitals look bad on every
  screen; that's what they buy."
* **Licensed wrong basis.** The manual records that the ministry's integrity unit ranks authorities on the composite red-flag index and will
  present it at the planning meeting.

## 8. Determinism by construction

* **Thresholds.** Co-bid thresholds from 6 to 9 return the same ring. Markup bands of ±2%, ±3% and ±4% return the same pairs.
* **Window.** Two-, three- and four-year windows identify the same ring, and the latest two quarters confirm it is still active.
* **Lot bundling.** Notices bundle lots. Every ring lot is single-lot or carries its own lot-level bids, so notice grain and lot grain
  agree on the ring.
* **Supplier identity.** No ring member re-registered or merged during the window, so supplier ID is stable for the main call.

## 9. Prompt sketch and deliverables

> I sign off where our only forensic team spends next year, and the chair would like it to go to the authority with the worst flags. Name the
> one authority the team should investigate, as a sentence I can put in the plan. Give me `authority_review.xlsx` with the sheets below,
> `cobid_network.png`, and a short `referral_memo.pdf` that commits to the name and says why the other seven are not it.

* `authority_review.xlsx` — the procedure-value sheet (ask A), the supplier count (ask B) and the screen reproduction table (ask C).
* `cobid_network.png` — the named authority's suppliers as a network: edges weighted by co-bids, ring pairs highlighted, the alternation
  order annotated, and the co-bid gap between 5 and 9 marked.
* `referral_memo.pdf` — the committed name, and why each of the other seven falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight authorities, the value awarded in the last four quarters under each
  procedure type (open, restricted, negotiated, framework call-off). *Device:* the procedure code list was revised mid-window, splitting
  call-offs into two codes, and the remap table is shipped. A solver using the raw code under-states call-offs in three authorities. The
  ring analysis never uses procedure codes.
* **Ask B (device-carried).** Distinct winning suppliers per authority over the window. *Device:* the supplier registry's merger history
  links re-registered companies by the same tax number, which matters for four non-ring winners.
* **Ask C (validity).** Hits out of 30 in the casebook for each of the four screens.
* **Decoupling.** Clearing the ring construction leaves asks A and B unchanged.

## 11. Rubric arithmetic

8 authorities × 4 procedure values (ask A) + 8 supplier counts (ask B) + 4 screens (ask C) + the committed name, ring size and active-quarter
evidence + 5 named chart parts + 3 files ≈ 55 criteria.

## 12. World-building constraints

* Each of the five flags is high in at least one shortlisted authority, every time for a legitimate documented reason: specialised
  medical buying, a flood emergency (now ended), mandated framework call-offs, regional supplier scarcity, and lot-splitting under the
  documented lot rule.
* E's ring is six suppliers rotating across 31% of E's lot value, with loser markups of 2–4% over the winning bid. Ordinary supplier pairs
  co-bid at most 5 times; ring pairs 9 to 14.
* The casebook holds 30 cases, 12 of them confirmed. The twin pair is identical on every authority-level field.
* Rung leaders are A, B, C, E, with margins of at least 1.25× at each rung. E is 5th, 4th and 3rd across rungs 0–2.
* Procedure-code remaps and supplier mergers never touch ring members or ring lots.
