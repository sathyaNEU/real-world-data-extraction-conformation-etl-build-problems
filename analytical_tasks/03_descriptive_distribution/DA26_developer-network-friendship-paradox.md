# DA26 — "Your connections have more connections than you": the network as users experience it

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Social platforms describing network size as experienced by users (feeds are filled by well-connected accounts), and marketplaces where buyers experience sellers weighted by sales |
| Domain | Developer communities / social networks |
| Task shape | 07 · Grid of cells (3 user segments × 4 statistics → mean degree, mean neighbour degree, share of users whose neighbours are better connected; the "seed" segment chosen for a feature launch) |
| Core method | Degree distribution; user-weighted mean degree E[k]; edge-weighted (neighbour) mean degree E[k²] ÷ E[k]; per-user mean neighbour degree and the share of users below their neighbours' mean (friendship paradox); segment-level comparisons |
| Analytical stump | The average number of followers-of-followers is not the average degree: sampling a neighbour samples users in proportion to their degree. Feature-diffusion planning that uses mean degree understates exposure via hubs; per-user neighbour averages and global neighbour averages also differ |
| Primary sources | MUSAE GitHub social network (mutual-follower network of developers, Rozemberczki et al.) |

## 1. The real-world situation

A developer-platform team will seed a collaboration feature to one user segment, expecting it to spread through mutual-follow links. Its
diffusion estimate used the segment's mean degree. A data scientist pointed out that what matters for spread is the degree of the people a
seeded user is connected to, which is systematically larger.

## 2. The decision (one deterministic recommendation)

**The seed segment (web developers, machine-learning developers or both-labelled) with the highest expected two-step reach per seeded user,
computed as mean degree × mean neighbour degree (edge-weighted) within the segment, with all segment statistics.**

Rules (growth memo):

* Graph: MUSAE GitHub mutual-follower edges (undirected); node labels: ML developer = 1, web developer = 0 (dataset target); "both" segment
  defined by the memo's feature rule.
* Degree k_i; for segment S: E_S[k] = mean degree of members; neighbour-weighted mean degree of members' neighbours = Σ over edges from S of
  k_neighbour ÷ number of such edge endpoints.
* Per-user mean neighbour degree m_i = mean of neighbours' degrees; paradox share = share of S members with k_i < m_i.
* Two-step reach proxy = E_S[k] × (edge-weighted neighbour mean degree − 1).
* Choose the segment with the highest proxy.

## 3. Why capable analysts get it wrong

* Mean degree is the headline network statistic.
* Neighbours are sampled proportionally to their degree (size-biased sampling).
* Averaging per-user neighbour means and pooling all neighbour edges give different numbers; the memo specifies which is used where.
* Hubs dominate exposure and differ across segments.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `musae_git_edges.csv` | CSV | ~289k edges | MUSAE GitHub (SNAP / Rozemberczki et al.) | Published research dataset (MIT per authors' repository; verify) | Edges |
| 2 | `musae_git_target.csv` | CSV | ~37.7k nodes | Same | Same | Labels |
| 3 | `musae_git_features.json` | JSON | ~37.7k | Same | Same | Node features |
| 4 | `rozemberczki_musae_citation.pdf` | PDF | — | Cite | Cite | Dataset description |
| 5 | `growth_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `diffusion_estimate_mean_degree.xlsx` | XLSX | 3 | Task author | — | Earlier estimate |
| 7 | `both_segment_rule.json` | JSON | — | Task author | — | Segment definition |
| 8 | `feld_1991_friendship_paradox_citation.pdf` | PDF | — | Cite | Cite | Paradox |
| 9 | `degree_table.parquet` | Parquet | ~37.7k | Derived | Same | Degrees |
| 10 | `toy_graph_checks.json` | JSON | — | Task author | — | Small-graph check values |

## 5. Deterministic solution path

1. Build the undirected graph; degrees; segments.
2. Segment mean degree; edge-weighted neighbour mean; per-user neighbour means; paradox shares.
3. Reach proxy; choose segment.
4. Contrast with the mean-degree estimate.

## 6. Wrong paths (method errors, not misreadings)

**A — mean degree only.** Exposure understated.

**B — mean of per-user neighbour means used as the edge-weighted quantity.** Mixes estimators.

**C — directed treatment of mutual follows.** Double counts.

**D — segment by neighbours' labels.** Wrong population.

## 7. Why the stump is analytical, not semantic

The statistics are defined. The trap is size-biased sampling of neighbours.

## 8. Draft task prompt (prose)

> Which segment should we seed the collaboration feature with? Compute the network statistics in the growth memo for the three segments and
> pick the one with the highest two-step reach proxy. Provide `segment_network_stats.csv` (segment: members, mean degree, edge-weighted neighbour
> degree, mean of neighbour means, paradox share, reach proxy), `degree_vs_neighbour_degree.png`, and a one-page `seed_segment.pdf`.

## 9. Deliverables

* `segment_network_stats.csv`, `degree_vs_neighbour_degree.png`, `seed_segment.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 segments × 5 statistics = 15; whole-graph statistics; choice; toy checks; earlier-estimate contrast.

## 11. Golden-output checklist

* Undirected degrees; segment definitions; estimators; proxy; choice.

## 12. Build notes (scope tuning)

* Confirm the segment ranking by mean degree differs from the ranking by reach proxy.
