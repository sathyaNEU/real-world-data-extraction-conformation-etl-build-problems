# AD41 — Cheat screening in online games: strong players play accurately, and one brilliant game proves nothing

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Trust-and-safety anti-cheat teams at online gaming platforms (chess sites, competitive shooters) screening for assistance without punishing skill |
| Domain | Online gaming integrity |
| Task shape | 01 · Ranked list under a cap (25 accounts for manual fair-play review) |
| Core method | Per-move centipawn loss from engine evaluations; expected accuracy conditional on rating band × time control × game phase from the population; account-level aggregation over ≥ 20 analysed games (sum of standardized game residuals ÷ √n); ranking by aggregated excess |
| Analytical stump | Raw accuracy ranks the strongest players first; single-game extremes are common among millions of games. Excess over the rating- and time-control-specific expectation, aggregated across many games, separates assistance from skill and luck |
| Primary sources | Lichess open database (monthly PGN files with engine evaluation annotations and clock times) |

## 1. The real-world situation

A gaming platform's fair-play team reviews **25** accounts a week by hand. Its automated screen ranks accounts by average accuracy in their
best five games; the list is filled with titled players and accounts that had one or two exceptional games.

## 2. The decision (one deterministic recommendation)

**The 25 accounts sent for manual review this week, ranked by aggregated excess accuracy, and the 26th.**

Rules (fair-play memo):

* Games: one month of rated blitz and rapid games with `[%eval]` annotations on every move; standard chess only.
* Move loss: centipawn loss = max(0, eval before − eval after) from the mover's perspective, evaluations capped at ±1000 and mate scores mapped
  to ±1000; moves 1–10 excluded (book).
* Game statistic: mean move loss for the player in the game.
* Expectation: for each rating band (100-point) × time control × player colour, mean and SD of the game statistic across all games in the month.
* Standardized residual per game: (expected − observed) ÷ SD (positive = more accurate than expected).
* Account score: Σ residuals ÷ √n over the account's analysed games; eligible with n ≥ 20.
* Rank by score; top 25; report #26.

## 3. Why capable analysts get it wrong

* Accuracy is the headline metric and rises with rating.
* Time control changes achievable accuracy; blitz and rapid differ systematically.
* Best-of-N selection picks extremes by construction.
* Aggregating without √n scaling favours high-volume accounts.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `lichess_db_standard_rated_<yyyy-mm>.pgn.zst` | PGN (compressed) | ~90M games (≈ 6% with evals) | Lichess open database | CC0 | Games with evals and clocks |
| 2 | `analysed_games_<yyyy-mm>.parquet` | Parquet | ~5M games | Derived | CC0 | Parsed analysed games |
| 3 | `move_evals_<yyyy-mm>.parquet` | Parquet | ~300M moves | Derived | CC0 | Per-move evals |
| 4 | `time_control_map.json` | JSON | ~30 | Task author (Lichess time-control categories) | — | Blitz/rapid classification |
| 5 | `fair_play_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `current_best5_accuracy_list.xlsx` | XLSX | 25 | Task author | — | Current screen |
| 7 | `closed_accounts_sample.csv` | CSV | ~500 | Task author (accounts later marked closed for fair-play, per public profile status at freeze date) | — | Validation |
| 8 | `pgn_spec_excerpt.txt` | Text | — | PGN standard | Public | Parsing |
| 9 | `expectation_table.csv` | CSV | ~120 | Derived | CC0 | Band × control × colour means/SDs |
| 10 | `reference_games.json` | JSON | ~10 | Task author | — | Hand-checked move losses |

## 5. Deterministic solution path

1. Parse analysed games; compute move losses with caps and exclusions.
2. Game statistics; expectation table; residuals.
3. Account scores with eligibility; rank; top 25 + #26.
4. Validation share in the closed-account sample; contrast with the current list.

## 6. Wrong paths (method errors, not misreadings)

**A — raw accuracy.** Strong players dominate.

**B — best-five games.** Selection of extremes.

**C — pooling time controls.** Misattributes accuracy differences.

**D — summing residuals without √n.** Volume dominates.

## 7. Why the stump is analytical, not semantic

Losses, expectations and aggregation are specified. The trap is conditioning on skill and context and aggregating evidence properly.

## 8. Draft task prompt (prose)

> Build this week's fair-play review list using the expectation-adjusted screen in the memo on one month of analysed Lichess games. Provide
> `account_scores.csv` (account: games, rating, score, rank), `score_vs_rating.png` (account score against rating with the list highlighted), and
> a one-page `review_queue.pdf` including the validation result.

## 9. Deliverables

* `account_scores.csv`, `score_vs_rating.png`, `review_queue.pdf`.

## 10. Where 25+ rubric criteria come from

* 25 accounts + #26; expectation values for 4 cells; scores for 5 accounts; validation share; contrast with current list.

## 11. Golden-output checklist

* Eval caps and mate mapping; opening exclusion; expectation by band/control/colour; residuals; scaling; eligibility.

## 12. Build notes (scope tuning)

* Validation labels are noisy (account closures have many causes); use them only as context.
* Confirm < 20% overlap with the current list.
