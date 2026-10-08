# AD36 — How many ratings the Q3 integrity sweep removes, when two ring definitions both reproduce the published shares

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Product Analytics · marketplace trust and safety |
| Mirrors | Removal counts and prevalence in platform transparency reports (fake-account prevalence at Meta, fake-review removals at Amazon, review integrity on Google Play), where a published share estimated from a labelled sample is reproduced by more than one classifier |
| Decision shape | One figure committed at a date: the number of ratings expunged in the Q3 sweep, stated in the integrity notice of 1 December |
| Committed call | The count of ratings the sweep expunges, to the nearest hundred, as printed in the notice |
| Gap · Pattern | Gap 4 (rule: the construction only finer controls pin) over Gap 2 (population) · finer controls separate constructions that a salient control cannot, with a per-seller removal cap applied in the figure below it |
| Gate G mechanism | method_or_model_selection, with binding_constraint support |
| Measured traps engaged | #12 stops at the first control that passes · #10 notes a binding limit as a risk · #3 stops at a close but inexact match |
| Calibration form | Gold-standard verification subsample: the Q1 and Q2 random samples of 2,000 ratings each, labelled by expert investigators, whose labelled shares are the published prevalence figures |
| Driving force | A ring rating is one with no settled trade behind it. Swapping +10s is the visible tell, and a reciprocal-pair definition reproduces both published shares exactly, because its two errors cancel: it flags repeat partners whose ratings are backed by escrow trades and misses rings that rate in cycles and stars. Only a join of every rating to the escrow ledger, keeping ratings with no settled trade between the pair and linking them into components, reproduces all 4,000 labels, and in Q3, when a cycle ring grew and repeat trading rose, the two errors stop cancelling. |

## 1. Situation

A peer-to-peer trading platform lets users rate each other from −10 to +10 after trades settle through its escrow. Each quarter its trust
team sweeps for coordinated rating rings, suspends the accounts and expunges every rating they gave, and its integrity notice states the
number of ratings removed. Q3 holds 190,000 ratings. The moderation playbook caps removals so that no seller loses more than half its
quarter's received ratings in one sweep (the rest go to manual review). The platform's transparency report publishes each quarter's
prevalence from a labelled random sample; Q3's sample will not be labelled until January, after the notice. The head of trust trusts the
standard fairness algorithm.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the ratings, the escrow ledger, the labels and the published shares. The fairness scores are computed
  correctly, and the community manager is right that ring members swap +10s. Nothing is overturned; the difficulty is which definition of a
  ring the labels actually support.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the fairness scores. A reciprocal-pair build that reproduces both published shares and applies
  the cap is still the natural build and still prints 7,400.
* **Instrument repair.** Label every sampled rating perfectly: they are. The published shares stay exactly right and still cannot tell the
  two definitions apart; only the rating-level labels, joined to trades, can.
* **Lens swap.** The naive population is ratings exchanged in reciprocal pairs; the answer's is ratings with no trade behind them, which adds
  cycle and star rings and removes backed repeat partners. Different ratings, not one set under a new lens.

## 3. The driving force

A strong solver rejects the fairness algorithm because it misses both published shares, defines rings as components of reciprocal +10
pairs, sees that definition reproduce 6.1% and 5.8% to the decimal, applies the per-seller cap, and prints 7,400. Every step is correct, and
the salient control has been passed. The rating-level labels behind those shares are in the same archive. Read rating by rating, the
reciprocal definition misses 61 labelled ring ratings, given in cycles (A rates B, B rates C, C rates A) and stars (sockpuppets rating one
hub), and wrongly flags 46 ratings between repeat partners who traded through escrow before every rating. The errors offset in both quarters.
The labels are reproduced, all 4,000, only by joining each rating to the escrow ledger, keeping those with no settled trade between the pair,
and linking them into components. In Q3 the cycle ring grew and genuine repeat trading rose, so the offset breaks: more ring ratings, fewer
false ones, and the capped count rises to 9,600.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Fairness-goodness iteration, raters below 0.6 fairness, every rating they gave, no cap | 14,200, +48% | The published algorithm every marketplace cites | The published shares: it gives 8.9% and 8.4% on the Q1 and Q2 samples against 6.1% and 5.8% |
| 1 | Components of reciprocal +10 pairs, every rating their members gave, no cap | 11,200, +17% | Reproduces both published shares to the decimal | The playbook: no seller loses more than half its quarter's received ratings in one sweep |
| 2 | Reciprocal-pair components with the per-seller cap applied | 7,400, −23% | Passes the salient control and respects the binding limit | The rating-level labels: it misses 61 ring ratings and flags 46 escrow-backed ratings across the two samples |
| 3 | **Decisive:** ratings with no settled escrow trade between the pair, linked into components of four or more, every rating their members gave, with the cap | **9,600** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the figure down (−21%, then −34%), and the decisive move turns it back up by 30%.
* **Partial correction priced (L3).** A solver who joins the escrow ledger only to drop backed pairs from the reciprocal definition, without
  adding cycle and star rings, prints 6,300: 34% below the answer and further from it than rung 2.
* **Grid.** Construction (fairness, reciprocal, unbacked components) × cap (off or on) = 6 cells: 14,200 / 10,900, 11,200 / 7,400 and
  13,900 / 9,600, plus carrying Q2's 5.8% to Q3's volume (11,020, which cannot apply a per-seller cap). The nearest wrong cell is the capped
  fairness build, 13.5% above.
* **Cap dominance.** The cap removes 4,300 of the 13,900 unbacked-ring ratings, almost all of them received by ring members from each other,
  so the cap and the construction interact and neither can be applied alone to reach the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The integrity policy says ratings from accounts in a coordinated ring are expunged. The escrow ledger is filed as a
   payments record; no document links ratings to trades or defines a ring.
2. **Finer controls pin a construction, not a menu.** Both the reciprocal and the unbacked definitions reproduce the published shares. On the
   4,000 labelled ratings the unbacked components reproduce all 4,000 and the reciprocal pairs 3,893, with errors in both directions that
   net to the published share, so a solver checking only shares is confirmed. The unbacked test is a join on each rating's pair and time to
   the escrow ledger followed by components, not a threshold on a list.
3. **No arithmetic symptom.** Ratings, accounts and escrow trades reconcile; the reciprocal build ties to both published shares exactly.
4. **Not a row predicate.** Ring membership needs a join of 190,000 ratings to the ledger, a graph of unbacked ratings, components, and then
   a per-seller cap over the ratings those members gave.
5. **The enumeration is arithmetic.** Ring accounts are computed; no column flags them, and the community's reciprocal tell is wrong both ways.
6. **No cutover date.** The cycle ring grew steadily through Q2 and Q3; no series steps.
7. **Survives deletion.** Remove both voices and the fairness scores, and the reciprocal build is still the natural one.

## 6. The calibration corpus

* **Form.** The Q1 and Q2 verification samples: 2,000 ratings drawn at random each quarter and labelled ring or not by expert
  investigators, whose labelled shares are the published prevalence figures (6.1% and 5.8%).
* **What it pins.** The salient control (the shares) admits the reciprocal and unbacked definitions alike; the finer control (the labels)
  admits only the unbacked one, 4,000 of 4,000 against 3,893.
* **Every rule exercised.** The samples contain cycle-ring ratings, star-ring ratings and backed repeat-partner ratings, so each part of the
  construction is tested, and every unbacked component in them has four or more members.
* **Twin pair.** Sellers Kestrel and Larkspur each received 60 Q3 ratings, 30 of them reciprocal +10s from raters of the same tenure and
  fairness profile. Kestrel's reciprocal raters are escrow-backed repeat partners and Larkspur's are an unbacked star ring, so the sweep
  removes 15 of Kestrel's ratings and 30 of Larkspur's, 2.0× apart, separated only by the escrow join.
* **Resemblance points at the decoy.** Q3's aggregate rating profile matches Q2's closely, so carrying Q2's published share to Q3 looks safe.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The integrity policy: every rating given by an account in a coordinated rating ring is expunged. The playbook: no seller
  loses more than half its quarter's received ratings in one sweep. The transparency methodology: the published share is the labelled share
  of the verification sample. One sentence each.
* **Empirical pins.** The ring construction, from the rating-level labels.
* **Voices.** The head of trust: "Fairness-goodness is peer-reviewed and every marketplace uses it." The community manager: "People who swap
  +10s with each other are the ring, full stop."
* **Licensed wrong basis.** The policy records that the platform's external auditor estimates removals by carrying the last published share
  to the quarter's volume and will check the notice against that figure.

## 8. Determinism by construction

* **Component size.** Every unbacked component in Q1–Q3 has four or more members, and unbacked ratings outside rings are isolated pairs, so
  size floors of three or four select the same accounts.
* **Backing.** Every backed rating has a settled trade between the pair within seven days before it and every ring rating has none at any
  time, so before-the-rating and any-time conventions agree.
* **The cap.** It is computed per seller on Q3 received ratings, and ratings held for manual review are outside the count, as the playbook
  states.
* **Rounding.** The figure is printed to the nearest hundred and the answer sits mid-bin.

## 9. Prompt sketch and deliverables

> The integrity notice goes out on 1 December and has to say how many ratings this sweep removes. Our head of trust is confident the
> standard fairness algorithm settles it. Give me the number, to the nearest hundred, in a sentence for the notice, and send
> `sweep_build.xlsx`, a chart `ring_components.png`, and a one-page `notice_note.pdf`.

* `sweep_build.xlsx` — the count under each rung's construction with its share and label reproduction (ask C), the support sheet (ask A)
  and the withdrawals sheet (ask B).
* `ring_components.png` — Q3's unbacked-rating components as a network, cycle, star and pair structures labelled, escrow-backed reciprocal
  pairs shown greyed for contrast, sellers at the cap marked, and the count in the title.
* `notice_note.pdf` — the committed count and the alternatives a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each week of Q3, rating-dispute tickets opened and the median time to first human response.
  *Device:* automatic acknowledgements are logged as replies from a system user ID listed in the support guide; counting them makes every
  response look instant. The sweep never uses support tickets.
* **Ask B (device-carried).** For each of the six fiat currencies, Q3 withdrawal volume and the share held for review. *Device:* a held
  withdrawal posts a release record, and the payments guide dates the withdrawal on release for volume reporting; dating on request moves a
  third of held volume into the wrong month and misstates three currencies.
* **Ask C (validity).** The count under each of the four rung constructions, with each construction's published-share and label reproduction.
* **Decoupling.** Clearing the escrow join and the cap changes no figure in asks A or B.

## 11. Rubric arithmetic

13 weeks × 2 (ask A) + 6 currencies × 2 (ask B) + 4 constructions × 3 (ask C) + the committed count, ring accounts suspended, sellers at the
cap and the uncapped ring-rating count + 5 named chart parts + 3 files ≈ 62 criteria.

## 12. World-building constraints

* Q3: 190,000 ratings. Unbacked ring ratings 13,900, capped to 9,600. Reciprocal definition 11,200, capped to 7,400. Fairness 14,200,
  capped to 10,900.
* Across the Q1 and Q2 samples the reciprocal definition misses 61 ring ratings and flags 46 backed ones, netting to the published shares.
* Every unbacked component has four or more members; every backed rating has a settled trade within seven days before it.
* Kestrel and Larkspur are identical on every rating-level column.
* Support tickets and withdrawals never touch ratings, labels or the escrow ledger.
