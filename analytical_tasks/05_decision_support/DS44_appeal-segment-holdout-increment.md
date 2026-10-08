# DS44 — Which donor segment gets the 40,000-piece year-end appeal, when the best responders would have given anyway

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Nonprofit & Grant-making · individual giving |
| Mirrors | Targeting by incremental rather than observed response (Meta and Google ads lift measurement, retention offers sent to customers who would have renewed, push notifications to users already active) |
| Decision shape | Which of N gets one scarce thing: the whole year-end appeal batch goes to one segment |
| Committed call | The segment mailed, and the net incremental income the mailing is expected to raise |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · S10 (the governing verb is causal, so the baseline is constructed from holdouts), with Pattern C (the serviceable share is the share not already giving by mandate) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #7 uses the ready-made measure · #15 follows the requester's hunch over the rule · #13 validates on one population, applies to another |
| Calibration form | Existing-book actuals: eight closed appeals, each with a randomised 10% holdout per segment |
| Driving force | A gift from a direct-debit donor arrives on schedule whether or not the appeal lands, so it registers as a response and raises nothing. Past holdouts measure the increment, and it is near zero for mandated donors. Each segment's mandate share sits in a separate register. The highest responders are the least incremental. |

## 1. Situation

A medical-research charity has 40,000 pieces left in its year-end print run and will send them to one of six donor segments. Its vendor's
response model ranks segments by predicted response, and the development director suspects large donors are being missed. The charity's
fundraising policy judges an appeal on the income it raises. Eight past appeals each held back a random 10% of every segment mailed.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: response rates, gift sizes, the vendor's scores, the holdout results and the mandate register. The
  vendor's score correctly predicts who will give in the window. The difficulty is that the decision is scored on what the appeal causes.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the vendor's scores and the director's view. Observed response by segment, the natural first construction, still
  points at the mandated segment.
* **Instrument repair.** Perfect gift tracking adds nothing, because the gift ledger already records every gift. Mandated gifts are real
  gifts.
* **Lens swap.** The answer is about donors whose giving changes when mailed: a counterfactual population, not the responders under another
  lens.

## 3. The driving force

A strong solver moves from response to expected gift to net value per piece, and each step is correct. The policy's verb is causal: an appeal
is judged on income it raises. Thirty-eight per cent of the donor file gives by direct-debit mandate, and their scheduled gifts fall inside
every appeal's response window. Their response rate is the highest on file and their increment in every holdout is about zero. Only the
holdouts, joined to the mandate register, separate the two. Every segment's increment is then a mix of a mandated share that adds nothing
and an unmandated share that responds. That mix differs by segment and is visible only through the join.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Vendor-style observed response rate per segment | A, monthly loyal | The vendor's model and the observed record agree | Expected gift per piece, not response, is what funds research; loyal donors give small amounts |
| 1 | Expected gift per piece (response × mean gift) | B, major-gift prospects | The two-part correction the director asked for | Net of print and postage after one piece per household, prospects' joint records halve their reach |
| 2 | Expected gift net of cost, one piece per household (hygiene: joint donor records deduplicated) | C, recent first-time donors | Clean, deduplicated, costed: a complete value-per-piece case | The holdouts show C's mailed and held-out groups giving within 0.9 points of each other |
| 3 | **Decisive:** holdout-measured increment by mandate status, transported to each segment's mandate share, net of cost | **E, lapsed mid-value donors** (5th of 6 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0, 4th on rung 1 and 2nd on rung 2 (1.22× behind C), and leads only rung 3. Rung leaders beat
  their runners-up by at least 1.25×.
* **Partial correction priced (L3).** A solver who uses each segment's own year-end holdout increment, where one exists, names C, because the
  lapsed segment has no year-end holdout. A solver who borrows lapsed's spring holdout computes E's net increment 27% low (spring gifts are
  smaller), which puts E below C's year-end increment, so it also names C. Every partial route lands on C, never on E.
* **Grid.** Response, expected gift or net value × increment (none, pooled by segment, mandate-conditioned) = 9 cells. Only the
  mandate-conditioned net increment names E at the committed figure.
* **Discriminator dominance.** C carries a 1.22× net-value advantage into rung 3. E's unmandated share (0.91) against C's (0.44), combined
  with a matching per-donor increment, gives E a 2.0× edge.
* **Figure.** The graded net incremental income for E is the extreme cell. Every partial application (for instance increments without
  mandate conditioning) lands at least 12% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy's "income it raises" is one verb in one clause. No document mentions mandates in relation to appeals.
2. **Corpus blind to the transport.** The holdouts certify segment-level increments for the segments as they were defined then. *In every
   closed appeal the lapsed segment was mailed in spring, never at year-end.* So no holdout reports a year-end increment for E directly; it
   has to be built from mandate-conditioned increments.
3. **No arithmetic symptom.** Mailed, held-out and gift counts reconcile, and gift totals tie to the ledger.
4. **Not a row predicate.** Increments are differences between randomised groups, conditioned through a join to the mandate register and
   recombined at each segment's mandate share.
5. **The enumeration is arithmetic.** No column carries "incremental"; the segment file has no mandate field.
6. **No cutover date.** Mandates accumulate gradually; no series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** Eight closed appeals with randomised 10% holdouts per mailed segment, and 60-day gift outcomes for mailed and held-out donors.
* **What it pins.** Mandated donors: mailed minus held out is 0.4 points across all eight appeals. Unmandated donors: 7.9 points (6.8 to
  9.1 across appeals). A pooled increment per segment reproduces each appeal's segment rows but cannot be transported to a new segment.
* **Twin pair.** The 2021 recent-donor and 2022 event-participant cells are identical on response rate (14.2%), mean gift, size and
  recency. Their increments differ 2.2×, at mandate shares of 64% against 12%.
* **Every rule exercised.** One appeal includes a segment with no mandated donors (pure unmandated increment) and one with 90% mandated (near
  zero), so the conditioning is identified at both ends.
* **Resemblance points at the decoy.** By recency and size, the lapsed segment resembles the spring-appeal cells, which show modest
  observed response.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fundraising policy: an appeal is judged on the income it raises, net of print and postage. The mandate register is
  the finance system's authoritative list.
* **Empirical pins.** Mandate-conditioned increments, from the holdouts.
* **Voices.** The vendor account manager: "Our model has the best lift on response in the sector." The director: "We're under-mailing our big
  givers."
* **Licensed wrong basis.** The policy records that the board's audit committee reviews appeals on gross income per piece and will see it.

## 8. Determinism by construction

* **Response window.** 45-, 60- and 90-day windows give the same increments, because mandated gifts recur monthly and no unmandated gift
  falls between day 45 and day 90.
* **Household deduplication.** Joint records share a household key, so deduplicating by key or by address gives the same counts.
* **Gift Aid uplift.** Excluded from "income raised" by the policy's netting clause, and it is equal across the mailed and held-out groups.
* **Cost.** Print and postage per piece are flat across segments, so cost is not a fork.

## 9. Prompt sketch and deliverables

> We have 40,000 year-end pieces and they go to one segment. The director thinks we under-mail big givers; the vendor swears by its response
> model. Tell me which segment gets the run and the net income you expect it to raise for us, in one sentence for the board. Send
> `appeal_decision.xlsx`, a chart `segment_value.png`, and a one-page `appeal_memo.pdf`.

* `appeal_decision.xlsx` — the six segments on four measures, the Gift Aid sheet (ask A) and the returns sheet (ask B).
* `segment_value.png` — the six segments' observed response, expected gift per piece and net increment per piece, side by side, with the
  chosen segment marked.
* `appeal_memo.pdf` — the committed segment and its net incremental income.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Gift Aid reclaimable on each segment's last twelve months of gifts. *Device:* declarations carry an
  effective date and cover gifts up to four years back, as the Gift Aid register documents. Using the declaration date as the start
  under-reclaims in three segments.
* **Ask B (device-carried).** Direct-debit payments returned unpaid, by month, over the last year. *Device:* returns post as negative gifts
  dated on the return date, not the collection date. Netting by collection month misplaces a third of them.
* **Ask C (validity).** Each segment's net value per piece under each of the four rung bases.
* **Decoupling.** Clearing the mandate conditioning changes no figure in asks A or B.

## 11. Rubric arithmetic

6 segments × 4 measures + 6 Gift Aid figures + 12 monthly returns + 6 × 4 bases (ask C) + the committed segment, its net incremental income and
its margin + 5 named chart parts + 3 files ≈ 80 criteria.

## 12. World-building constraints

* 38% of the file holds a mandate. Mandated mailed-minus-held-out is 0.4 points in all eight appeals; unmandated is 6.8 to 9.1.
* Segment mandate shares range from 9% (lapsed mid-value) to 71% (monthly loyal).
* Rung leaders are A, B, C, E. E is 5th / 4th / 2nd (1.22× behind C) / 1st, and rung margins are at least 1.25× outside rung 2.
* The twin cells are identical on every visible segment attribute.
* Lapsed's spring-holdout increment, carried to year-end, sits 27% below its mandate-conditioned year-end figure and at least 1.15× below
  C's year-end increment.
* Gift Aid declarations and payment returns never change mandate status or the holdout outcomes.
