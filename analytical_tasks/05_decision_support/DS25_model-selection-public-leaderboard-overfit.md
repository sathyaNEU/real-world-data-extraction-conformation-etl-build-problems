# DS25 — Picking the final model by the public leaderboard: the top of a reused test set is partly overfit

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Model selection against reused validation sets and benchmarks (internal leaderboards, offline metrics dashboards, LLM benchmark chasing) |
| Domain | Machine learning operations |
| Task shape | 07 · Grid of cells (competitions × selection policies → expected private-leaderboard rank; the selection policy adopted for internal model reviews) |
| Core method | Use historical competitions' submissions with public and private scores; compare selection policies for a team's final pick: (a) best public score, (b) best cross-validation-like proxy (median of a team's top-k public scores per memo), (c) public score penalised by the number of submissions (multiplicity correction per memo), (d) earliest submission within ε of the best; measure private-rank outcomes; estimate public–private shake-up |
| Analytical stump | Choosing the submission with the best public score maximises the influence of noise in a small public split, especially after many submissions; private performance regresses. Policies that account for multiplicity and noise select better final models. The adaptive data analysis effect is measurable from public versus private scores |
| Primary sources | Meta Kaggle (Kaggle's public metadata: competitions, submissions with public and private scores, teams) |

## 1. The real-world situation

An ML platform team runs internal model competitions on a fixed validation set and promotes the best-scoring model. Promoted models often
underperform in production. The team wants an evidence-based selection policy, using public data from Kaggle competitions where both a reused
public leaderboard and a held-out private leaderboard exist.

## 2. The decision (one deterministic recommendation)

**The selection policy adopted (the one with the best average private-percentile outcome across the competition sample), and the average
shake-up (public minus private percentile) of policy (a).**

Rules (platform memo):

* Data: Meta Kaggle competitions with ≥ 200 teams, public/private split, featured or research category, 2015–2022 (list in memo).
* Submissions: per team, all scored submissions with public and private scores (where available in Submissions.csv).
* Policies (per team, pick one submission): (a) best public; (b) the submission with best median public score over its 5 nearest submissions in time
  (memo's smoothing proxy); (c) best public − λ√(log submissions ÷ public test size) (λ per memo); (d) earliest submission within 0.1% of the team's
  best public.
* Outcome: private-leaderboard percentile of the chosen submission among all teams' final selections (memo uses teams' actual selections as the
  reference set).
* Average across teams and competitions; adopt the best policy; ties → simpler policy.

## 3. Why capable analysts get it wrong

* Best validation score is the natural choice.
* Repeated evaluation on the same set overfits it.
* Shake-up size depends on public split size and number of submissions.
* Policies should be compared on held-out outcomes, not public scores.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Competitions.csv` | CSV | ~5k | Meta Kaggle | Apache 2.0 | Competition metadata |
| 2 | `Submissions.csv` | CSV | ~15M | Meta Kaggle | Apache 2.0 | Submissions with public/private scores |
| 3 | `Teams.csv` | CSV | ~8M | Meta Kaggle | Apache 2.0 | Teams |
| 4 | `meta_kaggle_schema.md` | Markdown | — | Kaggle | Apache 2.0 | Schema |
| 5 | `competitions_in_scope.json` | JSON | ~60 | Task author | — | Sample |
| 6 | `platform_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `adaptive_overfitting_citation.pdf` | PDF | — | Roelofs et al., NeurIPS 2019 (cite) | Cite | Kaggle overfitting study |
| 8 | `score_direction.json` | JSON | ~60 | Task author | — | Metric direction per competition |

## 5. Deterministic solution path

1. Filter competitions; load submissions; harmonise score direction.
2. Apply policies per team; compute private percentiles.
3. Average outcomes; shake-up; choose policy.

## 6. Wrong paths (method errors, not misreadings)

**A — best public score.** Overfits.

**B — comparing policies on public scores.** Circular.

**C — ignoring metric direction.** Wrong picks.

**D — pooling competitions without per-competition percentiles.** Scale mismatch.

## 7. Why the stump is analytical, not semantic

Policies and outcomes are specified. The trap is selection on a reused noisy evaluation set.

## 8. Draft task prompt (prose)

> Which model-selection policy should our internal competitions use? Evaluate the candidate policies on Kaggle competitions with public and private
> leaderboards as the platform memo specifies. Provide `policy_grid.csv` (competition × policy: mean private percentile), `shakeup_vs_submissions.png`,
> and a one-page `selection_policy.pdf`.

## 9. Deliverables

* `policy_grid.csv`, `shakeup_vs_submissions.png`, `selection_policy.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 policies × overall mean; per-competition values (sampled 20); shake-up; policy choice.

## 11. Golden-output checklist

* Competition filter; direction; policies; percentiles; averaging; tie rule.

## 12. Build notes (scope tuning)

* Verify private scores are present for the sampled competitions; confirm policy (a) is not the best on private outcomes.
