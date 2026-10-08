# DS16 — Settle or go to trial? Trial win rates come from the cases that were not settled

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Decisions informed by outcomes observed only for escalated cases (support tickets that reach engineering, claims that go to litigation, deals that reach legal review) |
| Domain | Legal operations / corporate litigation |
| Task shape | 13 · Scenarios and the flip point (settlement offer × probability-of-win scenarios → expected value of trial versus settlement; the accept/reject call and the win probability at which it flips) |
| Core method | Outcome probabilities by nature of suit from all terminated cases (including dispositions before trial: dismissals, summary judgment, settlements) rather than trial verdicts alone; time to resolution distribution; expected value of continuing = Σ outcome probabilities × payoffs discounted by time, minus legal costs; compare with offer |
| Analytical stump | Plaintiffs' win rates at trial are high for some case types because weak cases are dismissed or settled earlier; using trial win rates for a case at the pleading stage overstates the value of continuing. Outcomes must be conditioned on the case's current stage using all dispositions |
| Primary sources | Federal Judicial Center Integrated Database (IDB) — civil cases |

## 1. The real-world situation

A company is defending a product-liability case at the early motion stage. Plaintiffs offer to settle for $1.2M. The litigation team's model used
the plaintiff win rate at trial for product-liability cases (from verdict data) and the median award, and concluded the company should settle. The
general counsel asked for a stage-appropriate model.

## 2. The decision (one deterministic recommendation)

**Accept or reject the $1.2M offer, with the expected cost of continuing and the plaintiff-success probability at which the decision flips.**

Rules (legal memo):

* Data: IDB civil terminations for nature-of-suit codes in the product-liability group, 2010–2022, federal district courts.
* Stage: cases that survived to the same procedural stage (no disposition before the memo's stage proxy, e.g., > 180 days without dismissal).
* Outcomes (from disposition and judgment fields): dismissed (no payment), settled (payment = memo's settlement multiple of demand), judgment for
  plaintiff at trial (award distribution from `award_reference.csv`), judgment for defendant.
* Probabilities: shares among stage-matched cases.
* Expected cost of continuing = P(settle later) × later settlement + P(plaintiff trial win) × E[award] + legal costs (memo per-month × median
  duration), discounted at 6% by median time to disposition.
* Accept if offer < expected cost of continuing.
* Flip point: plaintiff-win probability at trial at which costs are equal (holding other shares proportional).
* Contrast: trial-verdict-only model.

## 3. Why capable analysts get it wrong

* Verdict statistics are the most publicised outcome data.
* Trials are a selected subset; strong defence cases rarely reach trial.
* Stage matters: early-stage cases have many paths to resolution.
* Time and legal costs change expected values.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `cv<yy>.txt` (IDB civil, terminated cases) | Fixed-width/text | ~300k per year (all civil) | Federal Judicial Center IDB | U.S. Gov public domain | Case filings, dispositions, judgments |
| 2 | `idb_civil_codebook.pdf` | PDF | — | FJC | Public domain | Codes |
| 3 | `nature_of_suit_group.json` | JSON | ~10 | Task author | — | Product-liability codes |
| 4 | `award_reference.csv` | CSV | ~20 | Task author (from IDB amount fields and published verdict summaries; cite) | — | Award distribution |
| 5 | `legal_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `litigation_team_model.xlsx` | XLSX | — | Task author | — | Trial-only model |
| 7 | `case_profile.json` | JSON | — | Task author | — | Current case stage and demand |

## 5. Deterministic solution path

1. Filter cases; derive stage and outcomes from disposition/judgment codes.
2. Stage-matched outcome probabilities; durations.
3. Expected cost; decision; flip point.
4. Contrast with the trial-only model.

## 6. Wrong paths (method errors, not misreadings)

**A — trial win rates.** Selected sample.

**B — ignoring settlements as outcomes.** Misstates continuation value.

**C — undiscounted.** Overstates continuing cost.

**D — not matching stage.** Mixes early dismissals.

## 7. Why the stump is analytical, not semantic

Codes and rules are specified. The trap is using outcomes from a selected subset for an earlier-stage decision.

## 8. Draft task prompt (prose)

> Should we accept the $1.2M settlement? Build the stage-matched outcome model from IDB terminations as the legal memo specifies. Provide
> `outcome_model.csv` (outcome: probability, payoff, timing), `decision_tree.png`, and a one-page `settlement_recommendation.pdf` with the flip point.

## 9. Deliverables

* `outcome_model.csv`, `decision_tree.png`, `settlement_recommendation.pdf`.

## 10. Where 25+ rubric criteria come from

* Outcome probabilities (4) and payoffs; durations; expected cost; decision; flip point; trial-only contrast; case counts by stage.

## 11. Golden-output checklist

* NOS filter; stage proxy; outcome coding; discounting; decision rule; flip point.

## 12. Build notes (scope tuning)

* Confirm the trial-only model recommends the opposite decision.
