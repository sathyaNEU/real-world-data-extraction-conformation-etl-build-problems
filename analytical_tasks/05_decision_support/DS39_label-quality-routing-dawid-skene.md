# DS39 — Which crowd labels need expert review? Majority vote trusts every worker equally

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Data-labelling QA at AI companies and content-moderation vendors (routing items to expert review, paying workers by quality) |
| Domain | Machine learning data operations |
| Task shape | 04 · Setting one dial (the posterior-confidence threshold below which items go to expert review, within an expert budget of 10% of items) |
| Core method | Dawid–Skene EM: estimate each worker's confusion matrix and item posteriors from all labels; route the 10% of items with lowest posterior max to experts; evaluate on the dataset's golden labels: accuracy after review versus majority vote with the same budget (routing by vote margin) |
| Analytical stump | Majority vote treats spammers and experts alike; vote margins mis-estimate uncertainty when a few prolific low-quality workers dominate some items. Worker-reliability-weighted posteriors identify the truly uncertain items and improve accuracy for the same review budget |
| Primary sources | Toloka Aggregation datasets (TlkAgg relevance labels with worker IDs and golden labels) |

## 1. The real-world situation

A search-quality team buys crowd relevance labels and can afford expert review for 10% of items. It routes items with the narrowest majority-vote
margins. Audits show that some confidently voted items are wrong because the same low-quality workers labelled them.

## 2. The decision (one deterministic recommendation)

**The routing rule (Dawid–Skene posterior threshold) that selects 10% of items, and the final accuracy on golden items versus majority-vote
routing with the same budget.**

Rules (data-ops memo):

* Data: Toloka relevance aggregation dataset (version in memo): worker ID, item ID, label; golden labels for evaluation items.
* Dawid–Skene: initialise with majority vote; EM until log-likelihood change < 1e-6 or 100 iterations; class priors estimated.
* Routing: items sorted by posterior max ascending; route the lowest 10% (ties by fewer labels); expert labels = golden (memo's simulation of
  perfect experts on evaluation items).
* Majority vote routing: items with smallest vote margin (ties by fewer labels), same 10%.
* Accuracy on golden items after routing for each approach; adopt Dawid–Skene if accuracy is higher by ≥ 1 point.

## 3. Why capable analysts get it wrong

* Majority vote is the default aggregation.
* Worker quality varies widely; some are adversarial or random.
* Uncertainty should reflect worker reliability, not just vote counts.
* EM convergence and initialisation must be specified for reproducibility.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `crowd_labels.tsv` | TSV | ~0.5–1M labels | Toloka Aggregation Relevance dataset | CC BY 4.0 | Worker labels |
| 2 | `golden_labels.tsv` | TSV | ~10k | Same | CC BY 4.0 | Ground truth for evaluation |
| 3 | `toloka_dataset_description.md` | Markdown | — | Same | CC BY 4.0 | Description |
| 4 | `data_ops_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `current_routing_results.xlsx` | XLSX | — | Task author | — | Majority-vote routing |
| 6 | `dawid_skene_1979_citation.pdf` | PDF | — | Cite | Cite | Method |

## 5. Deterministic solution path

1. Load labels; restrict to items with ≥ 3 labels.
2. Run Dawid–Skene; posteriors; route 10%.
3. Majority-vote routing; accuracies on golden items; decision.

## 6. Wrong paths (method errors, not misreadings)

**A — vote-margin routing.** Ignores worker quality.

**B — weighting workers by label count.** Rewards prolific spammers.

**C — evaluating on items used to set the threshold.** Optimistic.

**D — unconverged EM.** Unstable posteriors.

## 7. Why the stump is analytical, not semantic

Algorithms and budgets are specified. The trap is uniform trust in heterogeneous raters.

## 8. Draft task prompt (prose)

> How should we route crowd-labelled items to expert review? Compare Dawid–Skene-based routing with our majority-vote routing at a 10% budget as the
> data-ops memo specifies. Provide `routing_results.csv` (approach: routed, accuracy before/after), `worker_quality.png`, and a one-page
> `label_qa_policy.pdf`.

## 9. Deliverables

* `routing_results.csv`, `worker_quality.png`, `label_qa_policy.pdf`.

## 10. Where 25+ rubric criteria come from

* Threshold; accuracies (4); worker quality summaries (10 workers); class priors; convergence; decision.

## 11. Golden-output checklist

* Item filter; EM details; routing ties; evaluation; decision.

## 12. Build notes (scope tuning)

* Confirm the accuracy gap meets the adoption bar.
